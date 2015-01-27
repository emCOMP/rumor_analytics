import networkx as nx

#Import our graph to NetworkX
g = None
headers = None
with open('boston_diff_filtered.csv','rb') as f:
    headers = f.readline()
    g = nx.read_weighted_edgelist(f, comments='#', delimiter=',', encoding='utf-8')
    
print nx.info(g)

cliques = list(nx.find_cliques(g))
count = sum(1 for c in cliques)
print count, " cliques identified."

with open('clique_results.csv', 'wb') as out:
	for c in cliques:
		print c
		line = ''
		for e in c:
			line = line + str(e)
			line = line + ','
		
		#Remove trailing comma, add newline.
		line = line[:-1]
		line = line + '\n'
		out.write(line)

print 'Writing complete.'
exit()