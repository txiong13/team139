import networkx as nx
from random import sample

quarentine_infectivity = 0.1
confirmed_negative_infectivity = 1.1
def update_positive_tests(graph, confirmed_positive_nodes, confirmed_negative_nodes):
    '''
    Takes a graph and a list of confirmed positves and confirmed negativess and updates the 
    node and weight attributes to reflect that they were tested 
    
    graph: networkx graph from model
    confirmed_positive_nodes: Nodes that were confirmed to be positive via testing 
    confirmed_negative nodes: Nodes that were confirmed to be negative via testing

    mutates the graph (edges and weights) to reflect probable behavior changes after testing

    '''

    # Set confirmed attribute for confirmed postive
    confirmed_pos_dic = {n : True for n in confirmed_positive_nodes}
    nx.set_node_attributes(graph, confirmed_pos_dic, name = "confirmed positive")

    # Set tested attribute for confirmed negative
    confirmed_neg_dic = {n : True for n in confirmed_negative_nodes}
    nx.set_node_attributes(graph, confirmed_pos_dic, name = "tested")
    nx.set_node_attributes(graph, confirmed_neg_dic, name = "tested")

    # Set edge weights for confirmed positive
    cp_edges = G.edges(confirmed_positive_nodes)
    weight = nx.get_edge_attributes(G, "weight")
    cp_edges = (e if e in weight else (e[1], e[0]) for e in cp_edges)
    updated_edges = {e: weight[e]*quarentine_infectivity for e in cp_edges}
    nx.set_edge_attributes(G, name = "weight", values = updated_edges)

    # Set edge weights for confirmed negative 
    cn_edges = G.edges(confirmed_negative_nodes)
    weight = nx.get_edge_attributes(G, "weight")
    cn_edges = (e if e in weight else (e[1], e[0]) for e in cn_edges)
    updated_edges = {e: weight[e]*confirmed_negative_infectivity for e in cn_edges}
    nx.set_edge_attributes(G, name = "weight", values = updated_edges)

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

