import graphlab as gl
import graphlab.aggregate as agg
import hashlib
import os
from graphlab.toolkits.feature_engineering import FeatureBinner

'''
Function:
        Creates a hash from the provided string.
        Strings composed of two equal-length parts will recieve the same hash:
            hash(<a><b>) == hash(<b><a>) if len(<a>) == len(<b>)

            Ex:
                hash('foobar') == hash('barfoo')
                hash('anna') == hash('naan')
                hash('fizzbar') != hash('barfizz')

Parameters:
    item <string>: The item to be hashed.
'''
def couple_hash(item):
    if type(item) != str:
        try:
            item = str(item)
        except:
            raise TypeError('item cannot be coverted to str')
    #Our Hash
    h = 0
    l = len(item)
    if l % 2 != 0:
        half = l/2
        item += chr(l)
        l += 1
    for i in xrange(l/2 -1):
        char_val = ord(item[i]) + ord(item[(l/2) + i])
        h = 33 * h ^ char_val
    return h

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
    def __init__(self, radius=1000000, k_limit=None, rep_fn='in_degree', caching=True):
        self.sf = None
        self.label = None
        self.bin_sfs = None
        self.radius = radius
        self.k_limit = k_limit
        self.rep_fn = rep_fn
        self.reps = gl.SArray(dtype=str)
        self.hier_graph = None
        self.caching = caching
        self.num_bins = 0

    def __split_bins__(self, sf, split_column, num_bins=10):
        sf.rename({split_column: 'bin'})
        binner = gl.feature_engineering.create(
            sf, FeatureBinner(features=['bin'], strategy='quantile', num_bins=num_bins))
        binner_sf = binner.fit_transform(sf)
        bin_sfs = []

        for b in binner_sf['bin'].unique():
            bin_sfs.append(binner_sf.filter_by([b], 'bin'))

        return binner_sf, bin_sfs

    '''
    Function: Removes loops and duplicate edges from the edgelist provided.
    Parameters:
        sf <SFrame>: The edgelist.
        delete_loops <bool>: Whether loops should be deleted.
    '''
    def __clean_edgelist__(self, sf):
        # This new column contains None for loops and a hash for edges.
        # Hashes for edges between the same vertices are identical:
        #       hash(A -> B) == hash(B -> A)
        sf['cleaning'] = sf.apply(
                lambda x: None if x['query_label'] == x['reference_label'] 
                            else couple_hash(x['query_label']+x['reference_label']))
        keepers = sf['cleaning'].dropna().unique()
        # We drop the None values(loops), and filter by unique edges.
        clean_sf = sf.filter_by(keepers, 'cleaning')

        return clean_sf

    def __get_bin_neighbors__(self, sf, label, delete_loops=True, hier=False):

        # Get feature column list.
        features = sf.column_names()
        features.remove(label)
        features.remove('bin')

        # Compute the nearest neighbors
        nn = gl.nearest_neighbors.create(sf, label=label, features=features)
        if hier:
            radius = None
            # This will try to give a similar number of connected components at the hier level.
            # To what we would see in each individual bucket.
            avg_component_count = sf.num_rows() / self.num_bins
            k = sf.num_rows() / avg_component_count
            print '!!! Hier Step !!! Using K = ', k
        else:
            radius = self.radius
            k = None

        results = nn.query(sf, label=label, k=k, radius=radius)

        print 'Before Culling'
        print results

        if delete_loops:
            # Remove loops from the result
            print 'Deleting Loops...'
            results['non_loop'] = results.apply(
                lambda x: None if x['query_label'] == x['reference_label'] else True)
            results = results.dropna

        print 'After Culling'
        print results

        return results

    # sf is the bin dataset
    def __construct_bin_graph__(self, sf, nn_sf, label):
        verts = nn_sf['query_label'].append(nn_sf['reference_label'])
        verts = verts.unique()
        g = gl.SGraph(sf, nn_sf,
                      vid_field='mongo_id',
                      src_field='query_label',
                      dst_field='reference_label')
        return g

    # Adds a field 'component_id' to the vertices of the graph 'g'.
    def __add_bin_component_ids__(self, g, hier=False):
        # The name of the new column to be added.
        col_name = 'component_id'
        if hier:
            col_name = 'hier_id'
        cc = gl.connected_components.create(g)
        tmp = cc['graph'].vertices['component_id'].astype(dtype=str) + '_'
        if hier:
            g.vertices[col_name] = tmp + 'h'
        else:
             g.vertices[col_name] = tmp + g.vertices['bin']

        print 'Items:\t',g.vertices.num_rows(),'Components:\t', len(g.vertices['component_id'].unique())

        return g

    # Returns an SArray with the ids of the representatives.
    def __bin_representatives__(self, g):
        # Define representative functions.
        # !!! Add new representative functions here !!!
        # !!! (and add an entry to the rep_fns dict below)!!!
        def in_degree(g):
            m = gl.degree_counting.create(g)
            g.vertices['in_degree'] = m['graph'].vertices['in_degree']
            reps = g.vertices.groupby(
                'component_id', {'rep': agg.ARGMAX('in_degree', '__id')})

            # TODO: Find a way to avoid adding and deleting this column.
            del g.vertices['in_degree']
            
            return reps['rep']

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
    Propagates the upper-hierarchy component_id labels to the entire dataset sf.

    Parameters:
        g <SGraph>: The upper-hierarchy graph which should be mapped onto the dataset
        sf <SFrame>: The dataset onto which the heirarchy labels will be mapped.
    '''
    def __map_hierarchy__(self, g, sf):
        # Map the hier_graph results to the whole dataset.
        hier_verts = g.vertices[['component_id','hier_id']]
        hier_members = sf.join(hier_verts,on='component_id')

        return hier_members

    def __cache_progress__(self, data_items, step):
        print 'Caching...'
        for d in zip(data_items):
            d.save('NNGH_cache/'+n)
        
        with open('NNGH_cache/step', 'wb') as f:
            f.write(str(step))

    def __hash_dataset__(self, path):
        BLOCKSIZE = 65536
        hasher = hashlib.md5()
        paths = [ os.path.join(path,f) for f in os.listdir(path) 
                    if os.path.isfile(os.path.join(path,f)) ]
        
        for p in paths:
            with open(p, 'rb') as f:
                buf = f.read(BLOCKSIZE)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = f.read(BLOCKSIZE)
        
        return hasher.hexdigest()


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
        self.sf, self.bin_sfs = self.__split_bins__(
            sf, split_column, num_bins)
        self.num_bins = int(num_bins)

        # We will place the results of processing each bucket
        # into this SFrame so when the loop completes it will
        # contain the original sf, along with component ids.
        proccessed_sf = gl.SFrame()
        # For each bin...
        for i, b in enumerate(self.bin_sfs):
            print 'Processing bin ' + str(i) + ' of ' + str(self.num_bins)
            # Construct a nearest neighbors graph.
            nn = self.__get_bin_neighbors__(b, label)
            g = self.__construct_bin_graph__(sf=b, nn_sf=nn, label=label)
            # Find the connected components.
            g = self.__add_bin_component_ids__(g)
            # Find the component representatives and store them in the model.
            self.reps = self.reps.append(self.__bin_representatives__(g))
            proccessed_sf = proccessed_sf.append(g.get_vertices())

        del self.bin_sfs

        # DEBUG: Check to see if we have preserved sf length.
        length_comparison = sf.num_rows() == proccessed_sf.num_rows()
        print '#DEBUG:\tlen(sf) == len(proccessed_sf):\t', length_comparison
        if not length_comparison:
            print 'sf: ', sf.num_rows()
            print 'proccessed_sf: ', proccessed_sf.num_rows()

        proccessed_sf.rename({'__id': 'mongo_id'})
        self.sf = proccessed_sf
        del proccessed_sf
        print 'Constructing Hierarchy Graph...'
        # Get an SFrame containing only the representatives.
        rep_sf = self.sf.filter_by(self.reps, 'mongo_id')
        print rep_sf
        # Construct the nearest neighbors graph for the
        # union of all the representatives.
        nn = self.__get_bin_neighbors__(rep_sf, label, hier=True)
        g = self.__construct_bin_graph__(sf=rep_sf, nn_sf=nn, label=label)
        g = self.__add_bin_component_ids__(g, hier=True)
        self.hier_graph = g
        self.hier_graph.save('final/hier_graph')

        print 'Sorting Components...'
        #Store a list of which components belong to which upper-heirarchy component.
        self.hier_membership = g.vertices[['component_id','hier_id']].groupby(
            'hier_id',{'members': agg.CONCAT('component_id')})
        self.hier_membership.save('final/hier_membership')

        print 'Propagating labels...'
        # Propagate the hierarchy labels to all of the data.
        self.sf = self.__map_hierarchy__(g,self.sf)

def accuracy_report(sf, component_col='hier_id'):
    print 'Calculating Accuracy...'
    rel = gl.SFrame.read_csv('sydney_rumors.csv')
    rumors = rel['rumor'].unique()
    rt = {}

    for r in rumors:
        rt[r] = rel.filter_by([r], 'rumor')['mongo_id']

    accuracy = {}
    for k, v in rt.iteritems():
        results = sf.filter_by(v, 'mongo_id')
        rel_counts = results.groupby(
            'component_id', operations={'count': agg.COUNT()}).sort('count', False)
        accuracy[k] = str(rel_counts['count'].sketch_summary())

    with open('accuracy_results.txt', 'wb') as f:
        line = '-'*40
        for k, v in accuracy.iteritems():
            f.write(str(k)+'\n\n\n'+v+'\n'+line)


def test():
    sf = gl.load_sframe('sydney_processed')
    
    # Use 10% of the data.
    sf = sf.random_split(0.01)[0]

    # Find a good radius
    print 'Finding radius...'
    tmp = sf.random_split(0.1)[0]
    label = 'mongo_id'
    features = sf.column_names()
    features.remove(label)
    k_nn = gl.nearest_neighbors.create(tmp, label=label, features=features)
    results = k_nn.query(sf, label=label, k=100)
    results['non_loop'] = results.apply(
                lambda x: None if x['query_label'] == x['reference_label'] else True)
    results = results.dropna(columns='non_loop')
    del results['non_loop']
    radius = results['distance'].mean() + (results['distance'].std() * 1.)
    print 'Using Radius:\t', radius

    del k_nn
    del results
    del tmp

    # Run the algorithm
    nnh = NNGraphHierarchy(radius=radius)
    nnh.fit(sf, label=label, split_column='time', num_bins=100)
    nnh.sf.save('final/final_results')
    accuracy_report(nnh.sf)
    print 'Success!'
    exit()

if __name__ == '__main__':
        test()
