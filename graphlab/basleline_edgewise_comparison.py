import graphlab as gl
import graphlab.aggregate as agg

baseline_path = "/home/jim/dev/rumor_analytics/baseline_jan6_e_wNames.csv"
rumor_path = "/home/jim/dev/rumor_analytics/time_test_compare_e.csv"
rumor_vert_path = "/home/jim/dev/rumor_analytics/time_test_compare_v.csv"

baseline_edges = gl.SFrame.read_csv(baseline_path, True)
rumor_edges = gl.SFrame.read_csv(rumor_path, True)
rumor_verts = gl.SFrame.read_csv(rumor_vert_path, True)

#Let's see what we have imported.
baseline_edges.head()
rumor_edges.head()

#To get the subgraph of the baseline data
#which corresponds to our rumor data, we will filter the baseline edge-list
#by both of the 'Word' columns of our rumor data.

rumor_words = rumor_edges.select_column("Word 1") #Get the first word column.
rumor_words = rumor_words.append(rumor_edges.select_column("Word 2")) #Glue the second word column to the end of the first.
rumor_words = rumor_words.unique() #Remove the duplicates.

filtered_baseline = baseline_edges.filter_by(rumor_words, "Word 1").filter_by(rumor_words, "Word 2")
filtered_baseline.rename({'Co-occurrence':'Baseline'})

#Lets look at the result:
filtered_baseline.head()

#Now let's join the counts into one SFrame (We will join a row if the pair of words matches.)
combined_order = filtered_baseline.join(rumor_edges, on={'Word 1':'Word 1', 'Word 2':'Word 2'}) #All in ordr matches match.
combined_reverse = filtered_baseline.join(rumor_edges, on={'Word 1':'Word 2', 'Word 2':'Word 1'}) #All reverse matches.


combined = combined_order.append(combined_reverse)

combined.head()

#We will take the difference between the baseline and the rumor data for each co-occurence pair.
edge_difference = combined.apply(lambda x: int(x['Co-occurrence']) - int(x['Baseline']))
combined.add_column(edge_difference,'Difference')

combined.head()

#Now we'll find some interesting rows to look at by looking for big differences.
#Using topk() to get the highest difference values.
#***It might be interesting to look at high magnitude negative values as well in the future.
interesting = combined.topk('Difference', 100)

#Get the word-names for our interesting rows.
temp = interesting.select_column('Word 1').append(interesting.select_column('Word 2')).unique()
verts = rumor_verts.filter_by(temp,'id')

#Create an SGraph so we can visualize the data:
differenceGraph = gl.SGraph(vertices=verts,edges=interesting, vid_field='id',src_field='Word 1', dst_field='Word 2')

#Now lets take a look:
differenceGraph.show(vlabel='word', vlabel_hover=False)
