import networkx as nx
from random import sample

def test_strat_random_sample(graph, n):
    '''
    Randomly select n nodes of the graph to be tested and updated accordingly.
    Paramters: 
        "graph" : NetworkX graph to be analyzed
        "n" : Number of nodes to be tested; must be no larger than the number of nodes in the graph.
    '''

    random_nodes = sample(list(graph.nodes()), n)
    #update_positive_test(graph, graph.nodes())
    return random_nodes


g = nx.Graph()
g.add_edge(1,2)
g.add_edge(1,3)
g.add_edge(1,4)
g.add_edge(1,5)
g.add_edge(5,6)

print(test_strat_random_sample(g, 7))

