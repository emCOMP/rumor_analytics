import csv
import networkx as nx
from networkx.algorithms.approximation import clique

class GraphAnalysis(object):

    def __init__(self,fname=None):
        self.graph = self.graph_from_file(fname)

    def graph_from_file(self,fname=None):
        if not fname:
            print 'enter edgeset file name'
            fname = raw_input('>> ')
        graph = nx.read_edgelist(fname,
                                 delimiter=',',
                                 nodetype=str,
                                 data=(('weight',float),))
        return graph

    def top_neighbors(self, ego):
        neighbors_iter = nx.all_neighbors(self.graph,ego)
        neighbors_list = [node for node in neighbors_iter]
        neighbors_list.sort(key=lambda x: self.graph[ego][x]['weight'], reverse=False)
        for node in neighbors_list:
            print node, self.graph[ego][node]


def main():
    g = GraphAnalysis(fname='data/sunil_running_compare_1h.csv')
    print g.graph.number_of_nodes()
    print g.graph.number_of_edges()
    ego = '"sandi"'
    remove = [node for node in nx.nodes(g.graph) if nx.degree(g.graph,node) > 500]
    #g.graph.remove_nodes_from(remove)
    print nx.is_connected(g.graph)
    print nx.number_connected_components(g.graph)
    for graphs in nx.connected_component_subgraphs(g.graph):
        print graphs.number_of_nodes()
        print graphs.number_of_edges()
        print '---'
    degree = sorted(nx.nodes(g.graph),key=lambda x: nx.degree(g.graph,x))
    weight = sorted(nx.edges(g.graph),key=lambda x: g.graph.get_edge_data(x[0],x[1]),reverse=False)
    for node in degree:
        print node,nx.degree(g.graph,node)
    g.top_neighbors(ego)
    #print nx.degree(g.graph,'"girl"')
    #print nx.degree(g.graph,'"8"')
    #print nx.degree(g.graph,'"year"')
    #print nx.degree(g.graph,'"old"')
    for edge in weight:
        print edge,g.graph.get_edge_data(edge[0],edge[1])
    #print clique.max_clique(g.graph)
    #print nx.node_clique_number(g.graph, nodes=ego, cliques=None)
    #node_list = nx.k_clique_communities(g.graph, 25)
    #for kcore in node_list:
    #    print kcore
    #g.top_neighbors(ego=ego)

if __name__ == "__main__":
    main()
