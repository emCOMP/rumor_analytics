from sklearn.cluster import MiniBatchKMeans
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from pymongo import MongoClient
from bson.objectid import ObjectId
import numpy as np
import json

print 'Loading matrix...'
loader = np.load('csr_data.npz')
m = csr_matrix(( loader['data'], loader['indices'], loader['indptr']), shape = loader['shape'])

row_to_id = dict()
with open('csr_row_ids.txt','rb') as rows:
	for l in rows:
		line = l.strip().split('\t')
		row_to_id[line[0]] = line[1]

print 'Load Complete\n'

print 'Calculating Neighbors...'
nn = NearestNeighbors(n_neighbors=10).fit(m)
reps = dict()
for i in range(3,20,2):
	print '\nTraining model...\tK = '+str(i)
	model = MiniBatchKMeans(n_clusters=i)
	result = model.fit_predict(m)
	centers = model.cluster_centers_

	topk = []
	for cent in centers:
		distances, indices = nn.kneighbors(cent)
		distances = distances.tolist()
		indices = indices.tolist()[0]
		indices = map(lambda x: row_to_id[str(x)], indices)
		topk.append(indices)

	reps['k'+str(i)] = topk


	fname = 'kmeans/'+str(i)+'_classes'

	with open(fname, 'wb') as cfile:
		np.save(cfile, result)

with open('k_reps.txt','wb') as reps_f:
	reps_f.write(json.dumps(reps))

print 'Complete.'

#Mongo Setup
dbclient = MongoClient('z')
db = dbclient.new_boston
mongo_config = db.tweets

def get_tweet(oid_string):
	oid = ObjectId(oid_string)
	t = list(mongo_config.find({"_id":oid},{"text":1, "_id":1}) )
	t = t[0]['text']
	return t

for k in reps.keys():
	print k,'==========\n'
	for clust in reps[k]:
		for oid in clust:
			print get_tweet(oid)	
		print '----------\n'
