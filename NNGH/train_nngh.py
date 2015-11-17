import graphlab as gl
from nngh import NNGraphHierarchy
from nngh_evaluation import rumor_component_distribution
from nngh_evaluation import top_level_report

def main(args):
    # Load the dataset.
    sf = gl.load_sframe(args.dataset)

    # If a valid sample size was provided
    # then replace the full dataset with a sample.
    if 0. < args.sample_size < 1.:
        sf = sf.sample(args.sample_size)

    # Create and fit the model.
    nnh = NNGraphHierarchy()
    nnh.fit(
        sf,
        label=args.label,
        features=args.features,
        split_column=args.split_column,
        num_bins=args.bins,
        path=args.output,
        quantile=args.quantile,
        k=args.num_neighbors,
        radius=args.radius,
    )

    # Save the results.
    nnh.sf.save(args.output)

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
        type=int, default=50)
    parser.add_argument(
        '-b', '--bins', help='How many bins to use (for chunking).',
        type=int, default=100)
    parser.add_argument(
        '-f', '--features', help='A dictionary of {feature: distance} mappings.',
        type=dict, default={'unigrams':'jaccard','bigrams':'jaccard','time':'euclidean','doc_vecs':'cosine','text':'levenshtein'})
    parser.add_argument(
        '-rel', '--rel_path', help='Path to a csv containing the ids of rumor-related tweets. (for checking accuracy)',
        type=str, default='sydney_rumors.csv')

    args = parser.parse_args()
    main(args)