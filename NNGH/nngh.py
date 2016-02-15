import graphlab as gl
import graphlab.aggregate as agg
import os


class NNGraphHierarchy(object):
    """
    Args:
        model_path (str): Path to a previously trianed SGraph
    """
    def __init__(self, model_path=None):
        if model_path:
            self.g = gl.load_sgraph(os.path.join(model_path, 'model.graph'))
            self.verts = self.g.vertices
            self.cache = gl.load_sframe(os.path.join(model_path, 'model.cache'))

    # sf is the bin dataset
    def _radius_neighbors_graph(
            self,
            sf,
            label,
            distance,
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
            label (str): the name of the column in sf containing the row labels
            distance (list): a list describing a GraphLab composite distance
                             measure.
            radius (float): the radius to use as threshold for
                            graph connectivity.
                            (larger radius = denser graph)
            src_field (str): the name of the column contianing
                           the source vertices.
            dst_field (str): the name of the column contianing
                           the destination vertices.

        Returns:
            (SGraph): a radius nieghbors graph (as described above)
        """

        # Get a feature list.
        features = []
        [features.extend(list(i[0])) for i in distance]


        print 'Determining edges...'
        # Compute the edgelist via nearest neighbors.
        nn = gl.nearest_neighbors.create(
            sf, label=label, features=features, distance=distance)
        edgelist = nn.query(
            sf, label=label, k=k, radius=radius)

        # Remove loops from the edgelist.
        # edgelist = self._remove_loops(edgelist)

        print 'Constructing graph...'
        # Make the graph.
        g = gl.SGraph(
            sf,
            edgelist,
            vid_field=label,
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

    def fit_sliding(self,
                     sf,
                     label,
                     radius,
                     cache_radius,
                     split_column,
                     distance,
                     k=None,
                     window_size=0.1,
                     window_offset=0.5):
        
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
            g = self._radius_neighbors_graph(cur_window, label=label, distance=distance, radius=cache_radius, k=k)
            
            # Add the edges to the edgelist.
            if not edgelist:
                edgelist = g.get_edges(src_ids=[None], dst_ids=[None])
            else:
                edgelist = edgelist.append(g.get_edges(src_ids=[None], dst_ids=[None]))

            window_begin = window_end - (window_offset * window_width)
            window_end = window_begin + window_width

        # Trim any duplicate edges from window-overlaps.
        edgelist = edgelist.unique()
        
        # Set the model's cache, graph, and vert
        self.cache = edgelist
        self.verts = sf
        self.g = self.get_graph(label, radius) 

    def get_graph(self, label, radius):
        if not self.verts or not self.cache:
            raise RuntimeError('Cannot access cached egdges or vertices.')

        # Prune the cached edges down to the desired radius.
        pruned = self.cache[self.cache['distance'] <= radius]
        g = gl.SGraph(vertices=self.verts, edges=pruned, vid_field=label)
        # Add connected component IDs to the graph.
        g = self._find_components(g, c_id_header='hier_id')
        return g

    def save(self, outpath):
        self.g.save(os.path.join(outpath,'model.graph'))
        self.cache.save(os.path.join(outpath,'model.cache'))


    def query_filter(self, query_ids, label='__id', component_label='component_id', kmin=None):
        result = self.verts.filter_by(query_ids, label)
        result_ids = result[component_label].unique()
        filtered_set = self.verts.filter_by(result_ids, component_label)
        if kmin:
            filtered_set = filtered_set[filtered_set['kcore_id'] >= kmin]
        return filtered_set

    def query(self, query_ids, label='__id', component_label='component_id'):
        query_rows = self.verts.filter_by(
            query_ids, label).select_columns([label, component_label])
        result = query_rows.join(self.verts.select_columns(
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
        return self.verts.filter_by(query_ids, component_label)
