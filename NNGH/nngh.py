import graphlab as gl
import graphlab.aggregate as agg
from nngh_evaluation import rumor_component_distribution
from nngh_evaluation import top_level_report


class NNGraphHierarchy(object):

    def __init__(self,
                 k_limit=None,
                 rep_fn='in_degree'):
        self.sf = None
        self.label = None
        self.bin_sfs = None
        self.k_limit = k_limit
        self.rep_fn = rep_fn
        self.reps = gl.SArray(dtype=str)
        self.hier_graph = None
        self.num_bins = 0

    def _find_radius(self, sf, connectivity, quantile):
        """
        Finds an acceptable radius to use for nearest neighbors
        on the given dataset by generating a sample set of distances
        (running k=100 nearest neighbors on 10-percent of the data),
        and using the value at the <quantile>th quantile of the sample.

        Args:
            sf <SFrame>: The dataset for which to find a good radius.
            quantile <float>: The quantile of the distance sample to take.
                              (float between 0.0 and 1.0)

        Returns:
            (float): The radius found using the above method.
        """
        print 'Finding radius...'

        # Take 10-percent of the data.
        tmp = sf.sample(0.1)

        # Create the model and perform the query.
        k_nn = gl.nearest_neighbors.create(
            tmp, label=self.label, features=self.features)
        sample = k_nn.query(tmp, label=self.label, k=connectivity)

        # # Remove loops.
        # # sample = self._remove_loops(sample)
        radius = gl.Sketch(sample['distance']).quantile(quantile)

        print 'Using Radius:\t', radius
        sample['distance'].save('sample_dist')

        return radius

    def _split_bins(self, sf, split_column, num_bins):
        """
        Splits the dataset 'sf' into 'num_bins' bins based on
        the values in the column 'split_column'.

        Args:
            sf (SFrame): The dataset.
            split_column (str): the name of the column to split on.

        Returns:
            <Tuple(SFrame, [SFrame, ...])>:
                A tuple containing:
                    1. The input 'sf' with 'split_column' replaced with
                        integers corresponding to bins.
                    2. A list containing an SFrame for each bin.
        """
        # Sort the data so we can break it up easily.
        sf = sf.sort(split_column, True)

        total_rows = sf.num_rows()
        rows_per_bin = total_rows / num_bins

        # See if the number of rows is evenly divisible into num_buckets.
        evenly_divisible = bool(rows_per_bin * num_bins == total_rows)

        # This will hold the SFrames containing the
        # individual bins
        bin_sfs = []

        for i in xrange(num_bins):
            # Handle the extra rows at the end if
            # the dataset doesn't fit evenly into the bins.
            if not evenly_divisible and i == (num_bins - 1):
                # Take the extras into account when separating
                # the SFrame.
                bin_start = i * rows_per_bin
                cur_bin = sf[bin_start:]
                cur_bin['bin'] = gl.SArray.from_const(i, cur_bin.num_rows())
                bin_sfs.append(cur_bin)
            else:
                # Separate the bin into its own SFrame
                bin_start = i * rows_per_bin
                bin_end = (i + 1) * rows_per_bin
                cur_bin = sf[bin_start:bin_end]
                # Add bin labels to the bin itself.
                cur_bin['bin'] = gl.SArray.from_const(i, rows_per_bin)
                bin_sfs.append(cur_bin)

        return sf, bin_sfs

    def _remove_loops(self,
                      sf,
                      src_col='query_label',
                      dst_col='reference_label'):
        """
        Removes loops from a graph edgelist.

        Args:
            sf (SFrame): the edgelist to remove loops from
            src_col (str): the name of the column contianing
                           the source vertices.
            dst_col (str): the name of the column contianing
                           the destination vertices.

        Returns:
            (SFrame): the input SFrame with the rows contianing
                      loops removed.
        """
        # Remove loops from the result
        print 'Deleting Loops...'
        # Add a marker column
        sf['non_loop'] = sf.apply(
            lambda x: None if x[src_col] == x[dst_col] else True)
        results = sf.dropna(columns='non_loop')

        # Delete the marker column
        del results['non_loop']

        return results

    # sf is the bin dataset
    def _radius_neighbors_graph(
            self,
            sf,
            radius,
            src_col='query_label',
            dst_col='reference_label'):
        """
        Generates a network graph where all vertices with a
        distance less-than <radius> are connected.

        First we find all of the nearest neighbors for each row
        in the dataset <sf> which are within <radius> distance of
        each other. These neighbor relationships are used as
        the edgelist of a network graph where the rows of <sf>
        are vertices.

        Args:
            sf (SFrame): the dataset for which to build the graph
                         (rows = examples, columns = features)
            radius (float): the radius to use as threshold for
                            graph connectivity.
                            (larger radius = denser graph)
            src_col (str): the name of the column contianing
                           the source vertices.
            dst_col (str): the name of the column contianing
                           the destination vertices.

        Returns:
            (SGraph): a radius nieghbors graph (as described above)
        """

        print 'Determining edges...'
        # Compute the edgelist via nearest neighbors.
        nn = gl.nearest_neighbors.create(
            sf, label=self.label, features=self.features)
        edgelist = nn.query(
            sf, label=self.label, k=None, radius=radius)

        # Remove loops from the edgelist.
        # edgelist = self._remove_loops(edgelist)

        print 'Constructing graph...'
        # Make the graph.
        g = gl.SGraph(
            sf,
            edgelist,
            vid_field=self.label,
            src_field=src_col,
            dst_field=dst_col)
        return g

    # Adds a field 'component_id' to the vertices of the graph 'g'.
    def _find_components(self, g, c_id_header='component_id'):
        """
        Finds the connected components in the graph <g> and
        adds a column to the graph's vertices containing
        the component_id of each vertex.

        Args:
            g (SGraph): the graph for which to find connected components
            c_id_header (str): the desired name for the component_id
                                column which will be added to <g>.

        Returns:
            (SGraph): the input graph <g> with component_id labels
                      added to the vertex SFrame.
        """
        print 'Locating connected components...'
        # Find the connected components.
        cc = gl.connected_components.create(g, verbose=False)
        # Add the label column.
        g.vertices[c_id_header] = cc['graph'].vertices['component_id']
        print 'Items:\t', g.vertices.num_rows()
        print 'Components:\t', cc['component_size'].num_rows()

        return g

    def _get_representatives(self, g, c_id_header='component_id'):
        """
        Finds a representative vertex for each component in the
        graph <g>. (The vertex with the highest in-degree for a
        given component is considered the representative).

        Args:
            g (SGraph): the graph for which to find connected components
            c_id_header (str): the name of the column containing the
                                component_id labels for the vertices
                                of <g>

        Returns:
            (SArray): the labels of the representatives for this graph
        """
        # Calculate the degree of each vertex
        m = gl.degree_counting.create(g)
        g.vertices['in_degree'] = m['graph'].vertices['in_degree']
        # Find the vertex of highest in-degree for each component
        reps = g.vertices.groupby(
            c_id_header, {'rep': agg.ARGMAX('in_degree', '__id')})

        return reps['rep'].astype(self.label_type)

    def _propagate_hier_labels(self, sf, hier_g):
        """
        Propagates the top-level component_ids from the representatives
        to all of the examples in the componenets which they represent.

        Args:
            sf (SFrame): The proccessed dataset to map the ids onto.
            hier_g (SGraph): The top-level graph from which to pull the
                             component_ids.

        Returns:
            (SFrame): the input dataset <sf> with the appropriate top-level
                      component_ids added to each example.
        """
        print 'Propagating hierarchy labels...'
        # Get the relavent information out of the graph's vertices.
        hier_verts = hier_g.vertices[['bin', 'component_id', 'hier_id']]

        # Create a column in containing both the bin and the low-level
        # component_id in each of the SFrames.
        # (Necessary since component_ids are not unique across bins)
        bin_ids = sf['bin'].astype(str)
        c_ids = sf['component_id'].astype(str)
        sf['bin_component'] = bin_ids + '_' + c_ids
        g_bin_ids = hier_verts['bin'].astype(str)
        g_c_ids = hier_verts['component_id'].astype(str)
        hier_verts['bin_component'] = g_bin_ids + '_' + g_c_ids

        return sf.join(hier_verts, on='bin_component')

    def fit(self,
            sf,
            label,
            split_column,
            num_bins,
            path,
            connectivity,
            quantile=0.5,
            radius=None,
            features=None):
        """
        Fits the model.

        Args:
            sf (SFrame): the dataset to fit the model to.
            label (str): the name of the column containing the
                         data's 'id' label.
            split_column (str): the name of the column which should
                                be used to split the data into bins.
            num_bins (int): the number of bins the data should be
                            split into.
            path (str): the path to save progress and output to.
            radius (float): the radius which should be used to threshold
                            the nearest_neighbors calculations.
            quantile (float): quantile to use for the radius-finding heurisitc.
            features ([str,]): a list of column names denoting which columns
                                   contain features to be used for
                                   nearest_neighbors calculations.

        Returns:
            (SFrame): an SFrame containing the input dataset, with both bin and
                      component labels added for each row.
                      (Each row recieves 'bin', 'component_id', 'hier_id'):
                            bin: the id of the bin this row was put into
                            component_id: the id of this row's component in the
                                          graph for the INDIVIDUAL BIN
                            hier_id: the id of the top-level component this row
                                     belongs to. (The component in the graph of
                                     representatives)

        Modifies:
            self.sf (SFrame): Upon completion sets the model's 'sf' attribute
                              to be the SFrame described above.
        """
        self.label = label
        self.label_type = type(sf[self.label][0])
        # If no list of feature columns is provided
        # assume all columns except the label are features.
        if features is None:
            self.features = sf.column_names()
            self.features.remove(label)
        else:
            self.features = features

        # Find a radius if one is not provided.
        if radius is None:
            # Use a heurisitc to find a radius.
            self.radius = self._find_radius(sf,
                                            connectivity=connectivity,
                                            quantile=quantile)
        else:
            self.radius = radius

        # Split the data into bins.
        sf, bins = self._split_bins(sf, split_column, num_bins)

        # A new copy of the dataset containing data (component_ids, etc.)
        # generated as the model proceeds.
        processed_sf = gl.SFrame()
        # Representative nodes chosen from each bin
        reps = gl.SArray(dtype=self.label_type)
        for i, b in enumerate(bins):
            print 'Processing bin ' + str(i) + ' of ' + str(num_bins)
            # Construct a nearest neighbors graph.
            g = self._radius_neighbors_graph(b, radius=self.radius)
            # Find the connected components.
            g = self._find_components(g)
            # Find the component representatives.
            reps = reps.append(self._get_representatives(g))
            processed_sf = processed_sf.append(g.get_vertices())

        # We're done with the individual bin SFrames now.
        del self.bin_sfs

        # DEBUG: Check to see if we have preserved sf length.
        # length_comparison = sf.num_rows() == processed_sf.num_rows()
        # print '#DEBUG:\tlen(sf) == len(processed_sf):\t', length_comparison
        # if not length_comparison:
        #     print 'sf: ', sf.num_rows()
        #     print 'processed_sf: ', processed_sf.num_rows()

        processed_sf.rename({'__id': label})

        print '\nConstructing Hierarchy Graph...\n'
        # Get an SFrame containing only the representatives.
        # (This contains the representatives for components in all bins).
        rep_sf = processed_sf.filter_by(reps, label)

        # --- Generally, the radius we used for the bins isn't a good choice
        # --- for the representatives, so we find a new one.

        # Try to have about the same ratio of components to examples as
        # the buckets.
        # connectivity_ratio = float(connectivity) / processed_sf.num_rows()
        # rep_connectivity = int(rep_sf.num_rows() * connectivity_ratio)
        # rep_connectivity = int(processed_sf['in_degree'].mean())
        # rep_radius = self._find_radius(rep_sf,
        #                                connectivity=rep_connectivity,
        #                                z_val=z_val)
        rep_radius = self.radius

        # Construct a radius graph for the representatives.
        g = self._radius_neighbors_graph(rep_sf, radius=rep_radius)
        # Label the components in the new graph.
        g = self._find_components(g, c_id_header='hier_id')
        self.hier_graph = g

        # Propagate the top-level component labels from the represenatives
        # to all of the vertices in their respective components.
        result = self._propagate_hier_labels(processed_sf, self.hier_graph)

        # Assign the model's SFrame to the final result.
        self.sf = result


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
        split_column=args.split_column,
        num_bins=args.bins,
        path=args.output,
        connectivity=args.connectivity,
        quantile=args.quantile,
        radius=args.radius
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
    hier_report = top_level_report(nnh.sf)
    hier_report.save(args.output + '_hier_report.csv')

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
        '-c', '--connectivity', help="The desired average degree of a node in a bin graph.",
        type=int, default=80)
    parser.add_argument(
        '-r', '--radius', help="The desired radius to be used in finding nearest neighbors.",
        type=float, default=None)
    parser.add_argument(
        '-q', '--quantile', help="The quantile to use for determining the model's radius.",
        type=float, default=0.5)
    parser.add_argument(
        '-b', '--bins', help='How many bins to use (for chunking).',
        type=int, default=100)
    parser.add_argument(
        '-rel', '--rel_path', help='Path to a csv containing the ids of rumor-related tweets. (for checking accuracy)',
        type=str, default='sydney_rumors.csv')

    args = parser.parse_args()
    main(args)
