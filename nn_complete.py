import graphlab as gl

cands = gl.SArray('cand_words')
sf = gl.load_sframe('sydney_sf')
sf['bow'] = gl.text_analytics.count_words(sf['text'])
# Trim the keys to only the 'highly unusual ones'.
sf['bow'] = sf['bow'].dict_trim_by_keys(cands, exclude=False)
# Delete rows with no keys left.
sf['bow_key'] = sf['bow'].dict_keys()
sf = sf.filter_by([[]], 'bow_key', exclude=True)
del sf['bow_key']
del sf['text']
del sf['retweeted']
del sf['time']

# Convert user IDs to sparse boolean format
sf['user_id'] = sf['user_id'].apply(lambda x: {x: 1})

buckets = gl.load_sframe('time_buckets')

for b in buckets.column_names():
    print 'Computing Neighbors for: ', b
    cur_ids = buckets[b].unique()
    cur_sf = sf.filter_by(cur_ids, 'mongo_id')
    nn = gl.nearest_neighbors.create(
        cur_sf, label='mongo_id', features=['user_id', 'bow'])
    results = nn.query(cur_sf, label='mongo_id', k=None, radius=0.95)
    print results.head(5)
    print 'Deleting Loops...'
    results['loops'] = results.apply(
        lambda x: x['query_label'] == x['reference_label'])
    results = results.filter_by([0], 'loops')
    del results['loops']
    results.save('buckets/' + b)
print 'Nearest Neighbors Complete!\n'
# Create Graphs

# reload the SFrame
sf = gl.load_sframe('sydney_sf')

print 'Creating Graphs...'
for i in range(1, 671):
    print 'Creating Graph for B' + str(i)
    cur_edges = gl.load_sframe('buckets/B' + str(i))
    edge_verts = cur_edges['query_label'].append(cur_edges['reference_label'])
    edge_verts = edge_verts.unique()
    cur_verts = sf.filter_by(edge_verts, 'mongo_id')
    g = gl.SGraph(cur_verts, cur_edges,
                  vid_field='mongo_id',
                  src_field='query_label',
                  dst_field='reference_label')
    g.save('graphs/B' + str(i))
print 'Graph Creation Complete!\n'

# Calculate Components
print 'Calculating Components...'
for i in range(1, 671):
    print 'Calculating Components for for B' + str(i)
    g = gl.load_sgraph('graphs/B' + str(i))
    cc = gl.connected_components.create(g)
    cc.save('components/B' + str(i))
print 'Success!'
exit()
