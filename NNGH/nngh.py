import graphlab as gl
import graphlab.aggregate as agg
import os
import json
import warnings


class NNGraphHierarchy(object):
    """
    Args:
        model_path (str): Path to a previously trianed SGraph
    """
    def __init__(self, model_path=None):
        if model_path:
            self.g = gl.load_sgraph(os.path.join(model_path, 'model.graph'))
            self.cache = gl.load_sframe(os.path.join(model_path, 'model.cache'))
            try:
                with open(os.path.join(model_path,'model.settings'), 'rb') as f:
                    self.settings = json.load(f)
                    dist = self.settings['distance']
                    for i in range(len(dist)):
                        dist[i][0] = map(str, dist[i][0])
                        dist[i][1] = str(dist[i][1])
                        dist[i][2] = float(dist[i][2])
            except Exception as e:
                warnings.warn("Error occured reading settings file.", RuntimeWarning)
                print e
            try:
                self.collapse_mapping = gl.load_sframe(os.path.join(model_path,'model.c_map'))
            except Exception as e:
                    warnings.warn("Error occured reading collapse mapping.", RuntimeWarning)
                    print e

    
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

    def _collapse_verts(self):
        '''
        Collapses the vertices of the model's graph over the unique connected components, 
        taking one representative for each component. Creating a new "dataset" using only
        the representatives.
        
        Returns:
            (SFrame, SFrame): (the new dataset, the '__id' mapping from the original dataset
                                to the new one).
        '''
        # Make sure the model has a cache and graph before we try to collapse the vertices
        if not self.cache:
            raise RuntimeError('Cannot access cached egdges or vertices')
        elif not self.g:
            raise RuntimeError('Cannot access model graph')
        collapsed_verts = self.g.vertices.groupby('hier_id', {'collapsed_id':agg.SELECT_ONE('__id')})
        # Create a new "dataset" using only the representatives, remove the hier_id field 
        # since it will be recalculated.
        collapsed_sf = self.g.vertices.filter_by(collapsed_verts['collapsed_id'].unique(), '__id').remove_columns(['hier_id'])
        collapsed_sf.rename({'__id': 'collapsed_id'})
        # Join the representative id onto the original ids so we can keep track.
        collapse_mapping = self.g.vertices.join(collapsed_verts[['hier_id', 'collapsed_id']], on='hier_id', how='left')[['__id', 'collapsed_id']]
        
        return (collapsed_sf, collapse_mapping)


    def fit_sliding(self,
                     sf,
                     label,
                     split_column,
                     radius,
                     cache_radius,
                     distance,
                     k=None,
                     window_size=0.1,
                     window_offset=0.5,
                     collapse=True):
        # Record what settings were passed so we can see them later.
        self.settings = {k: v for k, v in locals().iteritems() if k != 'self' and k != 'sf'}
        
        if "__id" in sf.column_names():
            raise RuntimeError("Unsupported Column Name: please rename column '__id'")

        sf = sf.sort(split_column).sort(label).add_row_number("__id")
        # These will serve as window boundaries.
        window_width = int(window_size * sf.num_rows())
        window_begin = 0
        window_end = window_width
        edgelist = None
        # i = 0
        # step_size = int(window_width * (1. - window_offset))
        while window_begin < sf.num_rows():
            print 'Processing...', 100 * float(window_begin)/ sf.num_rows(), 'percent complete.'
            # Grab the points in the current window
            if window_end <= sf.num_rows():
                cur_window = sf[window_begin:window_end]
            else:
                cur_window = sf[window_begin:]
            
            # Get the nn-graph for this window.
            g = self._radius_neighbors_graph(cur_window, label="__id", distance=distance, radius=cache_radius, k=k)
            
            # Add the edges to the edgelist.
            if not edgelist:
                edgelist = g.get_edges()
            else:
                edgelist = edgelist.append(g.get_edges())
            # src_min = i * step_size
            # src_max = int(src_min + window_width - 1)
            # print "Window:\t{} to {}".format(cur_window['__id'].min(),cur_window['__id'].max())
            # print "Window:\t{} to {}".format(src_min,src_max)
            window_begin = window_end - (window_offset * window_width)
            window_end = window_begin + window_width
            # i += 1

        # Trim any duplicate edges from window-overlaps.
        del edgelist['rank']
        edgelist = edgelist.unique()
        
        # Set the model's cache and graph
        self.cache = edgelist
        self.g = gl.SGraph(vertices=sf, edges=edgelist, vid_field="__id")
        self.g = self.get_graph(radius)

        # Collapse the vertices
        if collapse:
            # Collapse the vertices
            collapsed_sf, self.collapse_mapping = self._collapse_verts()
            # Run the model again with the collapsed vertices
            self.fit_sliding(
                         collapsed_sf,
                         label,
                         split_column,
                         radius,
                         cache_radius,
                         distance,
                         k=k,
                         window_size=window_size,
                         window_offset=window_offset,
                         collapse=False)


    def get_graph(self, radius, ws=None, wo=None, split_col='time', label='__id'):
        # Returns whether or not an edge from src_row to dst_row
        # is valid, given a window width and window offset.
        def valid_edge(src_row, dst_row, window_width, step_size):
            # Calculate the window bounds for both src and dst.
            src_min = int(src_row / step_size) * step_size
            src_max = int(src_min + window_width - 1)
            dst_min = int(dst_row / step_size) * step_size
            dst_max = int(dst_min + window_width - 1)
            # If the windows overlap, it is a valid edge.
            if (src_min <= dst_row <= src_max) or (dst_min <= src_row <= dst_max):
                return True
            else:
                return None

        if not self.cache:
            raise RuntimeError('Cannot access cached egdges or vertices')
        elif radius > self.settings['cache_radius']:
            raise ValueError('Requested radius is larger than cached radius')
        # Prune the cached edges down to the desired radius.
        edges = self.cache[self.cache['distance'] <= radius]
        if ws and wo and (ws != self.settings['window_size'] or wo != self.settings['window_offset']):
            verts = self.g.vertices.sort('__id')
            old_width = int(self.settings['window_size'] * verts.num_rows())
            new_width = int(ws * verts.num_rows())
            old_overlap = old_width * self.settings['window_offset']
            new_overlap = new_width * wo
            overlap_diff = int(old_overlap - new_overlap)
            old_step_size = int(old_width - old_overlap)
            new_step_size = int(new_width - new_overlap)
            features = []
            [features.extend(list(i[0])) for i in self.settings['distance']]
            # Calculate any missing edges
            start = old_step_size
            end = start + old_width
            steps = 1
            while start < verts.num_rows():
                # Calcuate the new left and right bounds for the window.
                old_left = start
                new_left = start + (overlap_diff * steps)
                old_right = end
                new_right = end + (overlap_diff * steps)

                if new_right <= verts.num_rows():
                    window = verts[new_left: new_right]
                else:
                    window = verts[new_left:]
                # If the difference is negative we are calculating missing
                # edges on the left side of the window.
                if overlap_diff < 0:
                    q_set = verts[new_left:old_left]
                # Otherwise the missing edges are on the right
                else:
                    q_set = verts[old_right:new_right]

                if window.num_rows() and q_set.num_rows():
                    nn = gl.nearest_neighbors.create(
                        window, label='__id', features=features, distance=self.settings['distance'])
                    new_edges = nn.query(
                        q_set, label='__id', k=self.settings['k'], radius=radius)
                    new_edges.rename({"query_label": "__src_id", "reference_label": "__dst_id"})
                    edges = edges.append(new_edges.remove_columns(['rank']).unique())
                    start += old_step_size + overlap_diff
                    end += old_step_size + overlap_diff
                steps += 1
            edges = edges.unique()
            edges['filter'] = edges.apply(lambda x: valid_edge(int(x['__src_id']), int(x['__dst_id']), new_width, new_step_size))
            edges = edges.dropna('filter')
            del edges['filter']
        g = gl.SGraph(vertices=self.g.vertices, edges=edges, vid_field='__id')
        # Add connected component IDs to the graph.
        g = self._find_components(g, c_id_header='hier_id')
        return g

    def save(self, outpath):
        self.g.save(os.path.join(outpath,'model.graph'))
        self.cache.save(os.path.join(outpath,'model.cache'))
        if self.collapse_mapping:
            self.collapse_mapping.save(os.path.join(outpath,'model.c_map'))
        with open(os.path.join(outpath,'model.settings'), 'wb') as f:
            json.dump(self.settings, f)


    def query_filter(self, query_ids, label='__id', component_label='component_id', kmin=None):
        result = self.g.vertices.filter_by(query_ids, label)
        result_ids = result[component_label].unique()
        filtered_set = self.g.vertices.filter_by(result_ids, component_label)
        if kmin:
            filtered_set = filtered_set[filtered_set['kcore_id'] >= kmin]
        return filtered_set

    def query(self, query_ids, label='__id', component_label='component_id'):
        query_rows = self.g.vertices.filter_by(
            query_ids, label).select_columns([label, component_label])
        result = query_rows.join(self.g.vertices.select_columns(
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
        else:
            return None
        return self.g.vertices.filter_by(query_ids, component_label)
