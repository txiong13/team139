import networkx as nx
from random import sample

def test_strat_random_sample(graph, n):
    '''
    Randomly select n nodes of the graph to be tested; tests those nodes and mutates graph accordingly.

    Paramters: 
        "graph" : NetworkX graph to be analyzed
        "n" : Number of nodes to be tested; nonnegative integer and must be no larger than the number of nodes in the graph.
    Returns:
        list of nodes that were tested
    '''

    tested_nodes = sample(list(graph.nodes()), n)
    #update_positive_test(graph, random_nodes)
    return tested_nodes

def test_strat_high_contact(graph, d):
    '''
    Test all nodes with degree greater than or equal to d in graph and mutates graph accordingly.

    Paramters: 
        "graph" : NetworkX graph to be analyzed
        "d" : nonnegative integer; nodes with degree greater than or equal to d will be tested.
    Returns:
        list of nodes that were tested

    '''
    node_deg_pairs = list(graph.degree())
    
    tested_nodes = []
    for node, deg in node_deg_pairs:
        if deg >= d:
            tested_nodes.append(node)
    #update_postiive_test(graph, tested_nodes)
    return tested_nodes


g = nx.Graph()
g.add_edge(1,2)
g.add_edge(1,3)
g.add_edge(1,4)
g.add_edge(1,5)
g.add_edge(5,6)

print(test_strat_random_sample(g, 1))
print(test_strat_high_contact(g, 4))

