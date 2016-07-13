import graphlab as gl
from nngh import NNGraphHierarchy

def main(args):
    # Load the dataset.
    sf = gl.load_sframe(args.dataset)
    # Get the pos_tag count column names.
    tag_cols = [i for i in sf.column_names() if i.startswith('pos_count')]
    # Set up some distance metrics
    # [('bigrams',), 'jaccard', 1],
    dists = [
             [('pos_bigrams', 'tfidf'), 'weighted_jaccard', 1],
             [('doc_vecs',), 'cosine', 1],
             [tuple(['time'] + tag_cols), 'euclidean', 1]
            ]
    # If a valid sample size was provided
    # then replace the full dataset with a sample.
    if 0. < args.sample_size < 1.:
        sf = sf.sample(args.sample_size)
    # Create and fit the model.
    nnh = NNGraphHierarchy()
    nnh.fit_sliding(
        sf,
        label=args.label,
        split_column=args.split_column,
        radius=args.radius,
        cache_radius=args.cache_radius,
        distance=dists,
        k=args.num_neighbors,
        window_size=args.win_size,
        window_offset=args.win_offset
    )
    # Save the results.
    nnh.save(args.output)
    print 'Success!'
    exit()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Attempts to find clusters of related data via a multi-step approach.')
    parser.add_argument(
        'dataset', help='Path to the dataset (SFrame on disk)',
        type=str)
    parser.add_argument(
        'label', help='The name of the label column in the dataset',
        type=str)
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
        '-cr', '--cache_radius', help="The maximum distance to cache edges for.",
        type=float, default=None)
    parser.add_argument(
        '-k', '--num_neighbors', help="How many nearest neighbors to find if not using a radius.",
        type=int, default=None)
    parser.add_argument(
        '-ws', '--win_size', help='The size of each window as a percentage of the data.',
        type=float, default=0.1)
    parser.add_argument(
        '-wo', '--win_offset', help='How much to offest each window. (0 is no overlap, 1 is complete overlap)',
        type=float, default=0.5)

    args = parser.parse_args()
    main(args)