import graphlab as gl
from nngh_sliding import NNGraphHierarchy
from nngh_evaluation import rumor_component_distribution
from nngh_evaluation import top_level_report

def main(args):
    # Load the dataset.
    sf = gl.load_sframe(args.dataset)

    # Get the pos_tag count column names.
    tag_cols = [i for i in sf.column_names() if i.startswith('pos_count')]
    
    # Set up some distance metrics
    dists = [[('unigrams', 'bigrams'), 'jaccard', 1],
             [('pos_bigrams',), 'weighted_jaccard', 1],
             [('doc_vecs',), 'cosine', 1],
             [tuple(['time'] + tag_cols), 'euclidean', 1]
            ]
    feats = []
    [feats.extend(list(i[0])) for i in dists]
    # If a valid sample size was provided
    # then replace the full dataset with a sample.
    if 0. < args.sample_size < 1.:
        sf = sf.sample(args.sample_size)

    # Create and fit the model.
    nnh = NNGraphHierarchy()
    nnh.fit(
        sf,
        label=args.label,
        features=feats,
        dist=dists,
        split_column=args.split_column,
        window_size=args.win_size,
        window_offset=args.win_offset,
        path=args.output,
        quantile=args.quantile,
        k=args.num_neighbors,
        radius=args.radius,
    )

    # Save the results.
    nnh.sf.save(args.output)
    nnh.g.save(args.output+'.graph')

    # If a path to rumor-related tweets was provided
    # then run an analysis of rumor-tweet distribution
    # across top-level components.
    if args.rel_path:
        # Load the list of related tweet ids for each rumor.
        related = gl.SFrame.read_csv(args.rel_path)
        rumor_report = rumor_component_distribution(
            nnh.sf,
            related,
        )
        rumor_report.save(args.output + 'rumor_report.csv', format='csv')

    # Save a report containing various information about
    # the top-level components.
    #hier_report = top_level_report(nnh.sf)
    #hier_report.save(args.output + '_hier_report.csv')

    print 'Success!'
    exit()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Attempts to find clusters of related data via a multi-step approach.')
    parser.add_argument(
        'dataset', help='Path to the dataset (SFrame on disk)',
        type=str)
    # sydney_processed
    parser.add_argument(
        'label', help='The name of the label column in the dataset',
        type=str)
    # mongo_id
    parser.add_argument(
        '-sc', '--split_column', help='The name of the label column to use for chunking.',
        type=str, default='time')
    parser.add_argument(
        '-o', '--output', help='Path to write results to.',
        type=str, default='NNGH_result')
    parser.add_argument(
        '-ss', '--sample_size', help="What percentage of the input dataset to use.",
        type=float, default=1.)
    parser.add_argument(
        '-r', '--radius', help="The desired radius to be used in finding nearest neighbors.",
        type=float, default=None)
    parser.add_argument(
        '-q', '--quantile', help="The quantile to use for determining the model's radius.",
        type=float, default=0.5)
    parser.add_argument(
        '-k', '--num_neighbors', help="How many nearest neighbors to find if not using a radius.",
        type=int, default=None)
    parser.add_argument(
        '-ws', '--win_size', help='The size of each window as a percentage of the data.',
        type=float, default=0.1)
    parser.add_argument(
        '-wo', '--win_offset', help='How much to offest each window. (0 is no overlap, 1 is complete overlap)',
        type=float, default=0.5)
    parser.add_argument(
        '-f', '--features', help='A dictionary of {feature: distance} mappings.',
        type=dict, default={'unigrams':'jaccard','bigrams':'jaccard','time':'euclidean','doc_vecs':'cosine'})
    parser.add_argument(
        '-rel', '--rel_path', help='Path to a csv containing the ids of rumor-related tweets. (for checking accuracy)',
        type=str, default='data/sydney_rumors.csv')

    args = parser.parse_args()
    main(args)