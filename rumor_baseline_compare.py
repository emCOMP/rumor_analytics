import graphlab as gl

base_name = 'sunil_1h'
base_path = '/home/jim/dev/rumor_analytics/data/'
baseline_path = base_path + "girl_running_baseline_1h_e_wNames.csv"
rumor_path = base_path + base_name + "_e_wNames.csv"
rumor_vert_path = base_path + base_name + "_v.csv"
full_out = 'data/sunil_running_compare_1h.csv'

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

#All of the words in the rumor set.
rumor_words = rumor_words.unique()

#All of the words which appear in BOTH sets.
filtered_baseline = baseline_edges.filter_by(rumor_words, "Word 1").filter_by(rumor_words, "Word 2")

#All baseline words.
baseline_words = filtered_baseline.select_column("Word 1").append(filtered_baseline.select_column("Word 2"))
baseline_words = baseline_words.unique()

#Words which appear ONLY IN THE RUMOR SET
rumor_only1 = rumor_edges.filter_by(baseline_words,"Word 1", exclude=True)
rumor_only2 = rumor_edges.filter_by(baseline_words,"Word 2", exclude=True)
rumor_only = rumor_only1.append(rumor_only2)
rumor_only.show()

#Now we'll add the terms that only occur in the rumor set to the baseline with a count of 0.
rumor_only.remove_column('Co-occurrence')
rumor_only.add_column(gl.SArray.from_const('0', rumor_only.num_rows()),'Co-occurrence') #Add a column of zeros.
print rumor_only
print 'Filtered', rumor_only.filter_by(['sunil'],'Word 1')
filtered_baseline = filtered_baseline.append(rumor_only)
print 'Before', filtered_baseline.filter_by(['craft'],'Word 1')

#Change the name of co-occurence so we can tell the rumor and baseline counts appart.
filtered_baseline.rename({'Co-occurrence':'Baseline'})

#Remove search terms and rt terms.
rumor_edges = rumor_edges.filter_by(["boston", "marathon", "bomb", "explos", "blast", 'r', 'rt'],"Word 1", exclude=True)
rumor_edges = rumor_edges.filter_by(["boston", "marathon", "bomb", "explos", "blast", 'r', 'rt'],"Word 2", exclude=True)


#Debug check
print 'After', filtered_baseline.filter_by(['craft'],'Word 1')

#Now let's join the counts into one SFrame (We will join a row if the pair of words matches.)
combined_order = filtered_baseline.join(rumor_edges, on={'Word 1':'Word 1', 'Word 2':'Word 2'}) #All in ordr matches match.
combined_reverse = filtered_baseline.join(rumor_edges, on={'Word 1':'Word 2', 'Word 2':'Word 1'}) #All reverse matches.


combined = combined_order.append(combined_reverse)

combined.head()

#We will take the difference between the baseline and the rumor data for each co-occurence pair.
edge_difference = combined.apply(lambda x: float(x['Co-occurrence']) - float(x['Baseline']))
combined.add_column(edge_difference,'Difference')

#Find the point where
combined_diff = combined.select_column('Difference')
combined_max = combined_diff.max()

combined_mean = combined_diff.mean()
combined_std = combined_diff.std()
z_threshold = combined_mean + (2*combined_std) #Z-Score of +2

#Filter our combined edgeset so we are left with the outliers from the right-side of the distribution.
outlier_col = combined.apply(lambda x: bool(x['Difference']>= z_threshold))
combined.add_column(outlier_col,'is_outlier')
print combined.head()



interesting = combined.filter_by([True],'is_outlier')

# gephi code
combined.remove_columns(['Co-occurrence','Baseline','is_outlier'])
combined.rename({'Word 1':'source','Word 2':'target','Difference':'weight'})
combined.save(full_out,format='csv')

interesting_gl = interesting.topk('Difference', 110)

#Get the word-names for our interesting rows.
temp = interesting_gl.select_column('Word 1').append(interesting_gl.select_column('Word 2')).unique()
verts = rumor_verts.filter_by(temp,'word')
verts.rename({'word':'__id'})


#Create an SGraph so we can visualize the data:
differenceGraph = gl.SGraph(vertices=verts, edges=interesting_gl, vid_field='__id',src_field='Word 1', dst_field='Word 2')

#Now lets take a look:
differenceGraph.show(vlabel='__id', elabel='Co-occurrence', elabel_hover=True)

#Export the edgelist.

#--------------GEPHI RENAMING
#interesting.rename({'Word 1':'Source','Word 2':'Target','Difference':'Weight'})

interesting.remove_columns(['Co-occurrence','Baseline','is_outlier'])
interesting.save('boston_outliers.csv',format='csv')
