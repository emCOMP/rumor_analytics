import graphlab as gl

#Takes two SFrames, one with verticies, one with edges.
#Returns (Vertex SFrame, Edge SFrame) where each has rows <= 1000
def n_by_n(vFrame, eFrame, n): 

	#Trim to the 1000 highest weighted edges.
	topEdges = eFrame.sort('Co-occurrence', False)
	topEdges = topEdges.head(n)

	#Get the incident verticies of those 1000 edges.
	topWords = topEdges.select_column('Word 1').append(topEdges.select_column('Word 2')).unique()


	#Keep trimming the lowest weight edge and removing the incident vertices until we have 1000 vertices.
	trim = n-1
	while topWords.size() > n:
		topEdges = topEdges.head(trim)
		topWords = topEdges.select_column('Word 1').append(topEdges.select_column('Word 2')).unique()
		trim -= 1

	#Get the SFrame for the top verts.
	topVerts = vFrame.filter_by(topWords, 'id');

	return (topVerts, topEdges)


#Returns the kth subgraph containing only nodes in the kth k-core.
def kth_subgraph(cores, edges, k, kmax):

	newVerts = cores.filter_by(range(k, kmax),'core_id')
	print "After", newVerts.sort('__id').head(5)
	vertIds = newVerts.select_column('__id')
	newEdges = edges.filter_by(vertIds, 'Word 1').filter_by(vertIds, 'Word 2')
	return gl.SGraph(newVerts, newEdges, '__id', src_fieldname, dst_fieldname)


#vertPath = raw_input('Path to vertex file: ');
#edgePath = raw_input('Path to edge file: ');
kThreshold = int(raw_input('Maxiumum k-cores to compute: '))
vertPath = 'csv/million_newFilter_vertices_GL.csv'
vid_fieldname = 'id'
edgePath = 'csv/million_newFilter_edges_GL.csv'
src_fieldname = 'Word 1'
dst_fieldname = 'Word 2'

vertFrame = gl.SFrame.read_csv(vertPath, True)
edgeFrame = gl.SFrame.read_csv(edgePath, True)

#topVerts, topEdges = n_by_n(vertFrame, edgeFrame, threshold)

topVerts = vertFrame
topEdges = edgeFrame

#Create Graph
g = gl.SGraph(topVerts, topEdges, vid_fieldname, src_fieldname, dst_fieldname)
kModel = gl.kcore.create(g, kmax=kThreshold)
kmax = kModel.get('kmax')
cores = kModel.get('core_id')

#print "Before", topVerts.sort('id').head(5)
#this might not work correctly.
cores = cores.sort('__id').add_column(topVerts.sort('id').select_column('word'),'word')
#print "After", cores.sort('__id').head(5)

#g.show(vlabel='word', vlabel_hover=False, elabel='Co-occurrence', elabel_hover=True, node_size=300)

#Wait for the user to quit.
while True:
	userIn = raw_input('Enter a k-core number to dispay or enter q to quit: ');
	if userIn == 'q':
		break;

	else:
		userIn = int(userIn)
		k = kth_subgraph(cores, topEdges, userIn, kmax)
		k.show(vlabel='word', vlabel_hover=False, elabel='Co-occurrence', elabel_hover=True, node_size=300)

exit()


