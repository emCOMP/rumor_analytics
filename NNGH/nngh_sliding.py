import graphlab as gl
import graphlab.aggregate as agg


class NNGraphHierarchy(object):
        """
        sf_path (str): Path to a previously trained SFrame
        g_path (str): Path to a previously trianed SGraph
        cache_max (float): The quantile of distances to cache.
        """

    def __init__(self, sf_path=None, g_path=None, cache_max=):
        self.sf = None
        self.label = None
        self.bin_sfs = None
        self.reps = gl.SArray(dtype=str)
        self.hier_graph = None
        self.num_bins = 0
        self.features = None
        self.distance = None
        if g_path:
            self.g = gl.load_sgraph(g_path)
            self.sf = self.g.vertices
        elif sf_path:
            self.sf = gl.load_sframe(sf_path)

    def _find_radius(self, sf, quantile, fname='sample_dist'):
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
            tmp,
            label=self.label,
            features=self.features,
            distance=self.distance)
        print k_nn['distance']
        sample = k_nn.query(tmp, label=self.label)

        # Remove loops.
        # sample = self._remove_loops(sample)
        radius = gl.Sketch(sample['distance']).quantile(quantile)

        print 'Using Radius:\t', radius
        sample['distance'].save(fname)

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

        return bin_sfs

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
            k=None,
            src_field='query_label',
            dst_field='reference_label'):
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
            sf, label=self.label, features=self.features, distance=self.distance)
        edgelist = nn.query(
            sf, label=self.label, k=k, radius=radius)

        # Remove loops from the edgelist.
        # edgelist = self._remove_loops(edgelist)

        print 'Constructing graph...'
        # Make the graph.
        g = gl.SGraph(
            sf,
            edgelist,
            vid_field=self.label,
            src_field=src_field,
            dst_field=dst_field)
        return g

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

    def _remove_symmetrical_edges(self, g):
        def sort_concat(item1, item2):
            return ''.join(sorted([item1, item2]))
        edges = g.edges.add_row_number('id')
        edges['hash'] = g.edges.apply(
            lambda x: sort_concat(x['__src_id'], x['__dst_id']))
        uniques = edges.groupby('id', agg.ARGMIN('distance', 'id'))
        filtered_edges = edges.filter_by(uniques['id'], 'id')

        return gl.SGraph(vertices=g.vertices, edges=filtered_edges)


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

        # !!!! Old code using highest in-degree as rep!!!!!
        # Calculate the degree of each vertex
        # m = gl.degree_counting.create(g)
        # g.vertices['in_degree'] = m['graph'].vertices['in_degree']
        # Find the vertex of highest in-degree for each component
        # reps = g.vertices.groupby(
        #     c_id_header, {'rep': agg.ARGMAX('in_degree', '__id')})
        # return reps['rep'].astype(self.label_type)

        # Calculate the mean distances between the vertices in each component.
        distances = g.edges.groupby(
            '__src_id', {'mean_distance': agg.MEAN('distance')})
        new_verts = g.vertices.join(distances, on={'__id':'__src_id'}, how='left')

        # Choose the vertex in each component which the lowest mean distance.
        reps = new_verts.groupby(
            c_id_header, {'rep': agg.ARGMIN('mean_distance', '__id')})

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

        hier_verts = hier_verts.select_columns(['bin_component', 'hier_id'])

        return sf.join(hier_verts, on='bin_component')

    def fit(self,
            sf,
            label,
            split_column,
            window_size,
            window_offset,
            path,
            quantile=0.5,
            k=None,
            radius=None,
            features=None,
            dist=None,
            kmax=30):
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
        if features and dist:
            self.features = features
            self.distance = dist
        else:
            self.features = None
            self.distance = None
        if not k:
            if radius is None:
                # Use a heurisitc to find a radius.
                self.radius = self._find_radius(sf, quantile=quantile)
            else:
                self.radius = radius
        else:
            self.radius = None

        sf = sf.sort(split_column)

        # These will serve as window boundaries.
        window_width = int(window_size * sf.num_rows())
        window_begin = 0
        window_end = window_width
        edgelist = None

        while window_begin < sf.num_rows():
            print 'Processing...', 100 * float(window_begin)/ sf.num_rows(), 'percent complete.'
            # Grab the points in the current window
            if window_end <= sf.num_rows():
                cur_window = sf[window_begin:window_end]
            else:
                cur_window = sf[window_begin:]
            # Get the nn-graph for this window.
            g = self._radius_neighbors_graph(cur_window, radius=self.radius, k=k)
            # Add the edges to the edgelist.
            if not edgelist:
                edgelist = g.get_edges(src_ids=[None], dst_ids=[None])
            else:
                edgelist = edgelist.append(g.get_edges(src_ids=[None], dst_ids=[None]))

            window_begin = window_end - (window_offset * window_width)
            window_end = window_begin + window_width

        edgelist = edgelist.unique()
        g = gl.SGraph(vertices=sf, edges=edgelist, vid_field=label)
        g = self._find_components(g, c_id_header='hier_id')
        kc = gl.kcore.create(g, kmax=kmax)
        g.vertices['kcore_id'] = kc['graph'].vertices['core_id']

        self.g = g
        self.sf = g.vertices

    def save(self, outpath):
        self.sf.save(outpath+'.sf')
        self.g.save(outpath+'.graph')

    def kcore_graph(self, kmin):
        if not self.g:
            raise Exception(
                'Cannot construct kcore graph without initial model graph.\n\
                Please fit the model or load a saved model graph before \
                calling kcore_graph()!')
        print 'Reconstructing graph...'
        verts = self.g.vertices[self.g.vertices['kcore_id'] >= kmin]
        leftover = verts['__id'].unique()
        edges = self.g.edges.filter_by(leftover, '__src_id').filter_by(leftover, '__dst_id')
        kg = gl.SGraph(vertices=verts, edges=edges)
        print 'Locating new components...'
        cc = gl.connected_components.create(kg, verbose=False)
        kg.vertices['component_id'] = cc['graph'].vertices['component_id']
        return kg

    def split_components(self, threshold=2):
        if not self.g:
            raise Exception(
                'Cannot construct kcore graph without initial model graph.\n\
                Please fit the model or load a saved model graph before \
                calling kcore_graph()!')
        print 'Locating fringe points...'
        deg = gl.degree_counting.create(self.g)
        counts = deg['graph'].vertices[['__id', 'in_degree']]
        fringe = counts[counts['in_degree'] <= threshold]['__id']
        print 'Culling edges...'
        edges = self.g.edges.filter_by(fringe, '__src_id').append(
                self.g.edges.filter_by(fringe, '__dst_id'))


    def query_filter(self, query_ids, label='__id', component_label='component_id', kmin=None):
        result = self.sf.filter_by(query_ids, label)
        result_ids = result[component_label].unique()
        filtered_set = self.sf.filter_by(result_ids, component_label)
        if kmin:
            filtered_set = filtered_set[filtered_set['kcore_id'] >= kmin]
        return filtered_set

    def query(self, query_ids, label='__id', component_label='component_id'):
        query_rows = self.sf.filter_by(
            query_ids, label).select_columns([label, component_label])
        result = query_rows.join(self.sf.select_columns(
            [label, component_label]), on=component_label, how='inner')
        result.rename({label: 'query_id', label + '.1': 'reference_id'})
        return result.sort(['query_id', 'reference_id'])

    def get_components(self,
                       query_set,
                       label='__id',
                       component_label='component_id'):
        '''
        Takes either an SFrame of query data, or a list of query
        component ids, and returns an SFrame containing the components
        which match the query.
        '''
        if isinstance(query_set, gl.SFrame):
            query_ids = query_set[component_label].unique()
        elif type(query_set) == list and len(query_set):
            query_ids = query_set
        return self.sf.filter_by(query_ids, component_label)
