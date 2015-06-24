import graphlab as gl
import graphlab.aggregate as agg
from graphlab.toolkits.feature_engineering import FeatureBinner

'''
===================================
Nearest Neighbors Graph Hierarchy |
===================================
This model takes in a matrix of unlabeled data where the rows are examples
and the columns are numeric features, and produces a hierarchical graph of
nearest nieghbors following this proceedure:

1. Divide the data up into 'bins' based one of the feature columns.
   (Usually time)

2. Locate all Nearest Neighbors for each example within a given radius,
   processing each bucket separately.

3. Construct a directed graph using the list of
   nieghbors from step 2 as an edgelist.

4. Locate the connected components of the graph.

5. Select a 'representative' node for each component.
   (Typical criteria would be the node of highest in-degree)

6. Compute the nearest neighbors between the set of all representatives.

7. Treat components who's representatives are in the same component as
   time-snapshots of the same component.

TODO: Do representatives need to be separated by bin if the bin_id
      is baked into the component_id?
'''


class NNGraphHierarchy(object):

    '''
    Parameters:
        radius <float>: The maximum distance threshold when
                        finding nearest neighbors.

        k_limit <integer>: The maximum number of nearest nieghbors
                           to find per row.

        rep_fn <string>: The name of the function which should be
                         used to find a representative node for each
                         connected component of the graph hierarchy.
    '''

    def __init__(self, radius=0.95, k_limit=None, rep_fn='in_degree'):
        self.sf = None
        self.label = None
        self.bin_sfs = None
        self.radius = radius
        self.k_limit = k_limit
        self.rep_fn = rep_fn
        self.reps = gl.SArray(dtype=str)
        self.hier_graph = None

    def split_bins(self, sf, split_column, num_bins=10):
        sf.rename({split_column: 'bin'})
        binner = gl.feature_engineering.create(
            sf, FeatureBinner(features=['bin'], num_bins=num_bins))
        binner_sf = binner.fit_transform(sf)
        bin_sfs = []

        for b in binner_sf['bin'].unique():
            bin_sfs.append(sf.filter_by([b], 'bin'))

        return binner_sf, bin_sfs

    # label='mongo_id'
    # features = ['user_id', 'bow']
    def get_bin_neighbors(self, sf, label, k_limit=None, delete_loops=True):
        # Get feature column list.
        features = sf.column_names()
        features.remove(label)
        features.remove('bin')

        # Compute the nearest neighbors
        nn = gl.nearest_neighbors.create(sf, label=label, features=features)
        results = nn.query(sf, label=label, k=k_limit, radius=self.radius)

        if delete_loops:
            # Remove loops from the result
            print 'Deleting Loops...'
            results['loops'] = results.apply(
                lambda x: x['query_label'] == x['reference_label'])
            results = results.filter_by([0], 'loops')
            del results['loops']
        return results

    # label='mongo_id'
    # sf is the bin dataset
    def construct_bin_graph(self, sf, nn_sf, label):
        verts = nn_sf['query_label'].append(nn_sf['reference_label'])
        verts = verts.unique()
        g = gl.SGraph(sf, nn_sf,
                      vid_field='mongo_id',
                      src_field='query_label',
                      dst_field='reference_label')
        return g

    # Adds a field 'component_id' to the vertices of the graph 'g'.
    def add_bin_component_ids(self, g, hier=False):
        
        # The name of the new column to be added.
        col_name = 'component_id'
        if hier:
            col_name = 'hier_id'

        cc = gl.connected_components.create(g)
        tmp = cc['graph'].vertices['component_id'] + gl.SArray.from_const('_')
        g.vertices[col_name] = tmp + g.vertices['bin']
        return g

    # Returns an SArray with the ids of the representatives.
    def bin_representatives(self, g):
        # Define representative functions.
        # !!! Add new representative functions here !!!
        # !!! (and add an entry to the rep_fns dict below)!!!
        def in_degree(self, g):
            m = gl.degree_counting.create(g)
            g.vertices['in_degree'] = m['graph'].vertices['in_degree']
            reps = g.vertices.groupby(
                'component_id', {'rep': agg.ARGMAX('in_degree', '__id')})
            return reps['__id']

        # Switch to map rep_fn parameter to the functions.
        rep_fns = {'in_degree': in_degree
                   }

        # If the provided function name is supported
        # pass the graph to the appropriate function
        # and return the result.
        if self.rep_fn in rep_fns:
            return rep_fns[self.rep_fn](g)
        else:
            raise NotImplementedError(
                'The representative function you requested\
                 has not been implemented.'
            )

    '''
    Parameters:
        sf <SFrame>: The dataset which the model will be fit to
                     (rows are examples, columns are numeric features).

        label <string>: The name of the id column in sf (column
                        will be ignored for nearest nieghbors calculations)

        split_column <string>: The name of the column which should be used to
                               split the data into bins. (column will be
                               ignored for nearest nieghbors calculations)

        num_bins <integer>: The number of bins to split the dataset into.
    '''

    def fit(self, sf, label, split_column, num_bins):
        # Split the data into bins.
        self.sf, self.bin_sfs = self.split_bins(
            self.sf, split_column, num_bins)
        num_bins = str(len(self.bin_sfs))

        # We will place the results of processing each bucket
        # into this SFrame so when the loop completes it will
        # contain the original sf, along with component ids.
        proccessed_sf = gl.SFrame()
        # For each bin...
        for i, b in enumerate(self.bin_sfs):
            print 'Processing bin ' + str(i) + 'of ' + num_bins
            # Construct a nearest neighbors graph.
            nn = self.get_bin_neighbors(b, label)
            g = self.construct_bin_graph(sf=b, nn_sf=nn, label=label)
            # Find the connected components.
            g = self.add_bin_component_ids(g)
            # Find the component representatives and store them in the model.
            self.reps = self.reps.append(self.bin_representatives(g))
            proccessed_sf = proccessed_sf.append(g.vertices)

        # DEBUG: Check to see if we have preserved sf length.
        length_comparison = sf.num_rows() == proccessed_sf.num_rows()
        print 'len(sf) == len(proccessed_sf):\t', length_comparison
        if not length_comparison:
            print 'sf: ', sf.num_rows()
            print 'proccessed_sf: ', proccessed_sf.num_rows()

        self.sf = proccessed_sf

        print 'Constructing Hierarchy Graph...'
        # Get an SFrame containing only the representatives.
        rep_sf = proccessed_sf.filter_by(self.reps, 'mongo_id')
        # Construct the nearest neighbors graph for the
        # union of all the representatives.
        nn = self.get_bin_neighbors(rep_sf, label)
        g = self.construct_bin_graph(sf=rep_sf, nn_sf=nn, label=label)
        g = self.add_bin_component_ids(g, hier=True)
        self.hier_graph = g
