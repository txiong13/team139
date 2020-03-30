import networkx as nx
from random import sample
import random
from scipy.stats import norm

quarantine_infectivity = 0.1
confirmed_negative_infectivity = 1.1

FAMILY_CLIQUE_SIZE = 3

# distribution of days until attempting to get test once infected is assumed to be normal with the parameters below
SYMPTOM_DIST_MEAN = 3
SYMPTOM_DIST_SD = 1
###

def update_positive_tests(graph, confirmed_positive_nodes, confirmed_negative_nodes):
    '''
    Takes a graph and a list of confirmed positves and confirmed negativess and updates the 
    node and weight attributes to reflect that they were tested 
    
    graph: networkx graph from model
    confirmed_positive_nodes: Nodes that were confirmed to be positive via testing 
    confirmed_negative nodes: Nodes that were confirmed to be negative via testing

    mutates the graph (edges and weights) to reflect probable behavior changes after testing

    NOTE: Currently it is not multaplicative for things of the same type, but it is for things of different 
    type

    '''

    # Set confirmed attribute for confirmed postive
    confirmed_pos_dic = {n : True for n in confirmed_positive_nodes}
    nx.set_node_attributes(graph, confirmed_pos_dic, name = "confirmed positive")

    # Set tested attribute for confirmed negative
    confirmed_neg_dic = {n : True for n in confirmed_negative_nodes}
    nx.set_node_attributes(graph, confirmed_pos_dic, name = "tested")
    nx.set_node_attributes(graph, confirmed_neg_dic, name = "tested")

    # Set edge weights for confirmed positive
    cp_edges = graph.edges(confirmed_positive_nodes)
    weight = nx.get_edge_attributes(graph, "weight")
    cp_edges = (e if e in weight else (e[1], e[0]) for e in cp_edges)
    updated_edges = {e: weight[e]*quarantine_infectivity for e in cp_edges}
    nx.set_edge_attributes(graph, name = "weight", values = updated_edges)

    # Set edge weights for confirmed negative 
    cn_edges = graph.edges(confirmed_negative_nodes)
    weight = nx.get_edge_attributes(graph, "weight")
    cn_edges = (e if e in weight else (e[1], e[0]) for e in cn_edges)
    updated_edges = {e: weight[e]*confirmed_negative_infectivity for e in cn_edges}
    nx.set_edge_attributes(graph, name = "weight", values = updated_edges)


def perform_test(graph, tested_nodes):
    '''
    Tests each node of tested_nodes in graph.

    Parameters:
        'graph' : NetworkX graph to be analyzed
        'tested_nodes' : list of nodes to be tested

    Returns:
        positive_nodes, negative_nodes : lists of nodes that tested positive and negative, respectively
    '''
    positive_nodes = []
    negative_nodes = []
    for node in tested_nodes:
        if graph.nodes[node]['status'] == 'I':
            positive_nodes.append(node)
        else:
            negative_nodes.append(node)
    return positive_nodes, negative_nodes

def perform_clique_test(graph, tested_nodes):
    '''
    Tests each node of each clique of tested_nodes in graph.

    Parameters:
        'graph' : NetworkX graph to be analyzed
        'tested_nodes' : list of cliques (which are lists of nodes) to be tested

    Returns:
        positive_nodes, negative_nodes : lists of nodes that tested positive and negative, respectively
    '''
    positive_nodes = []
    negative_nodes = []
    for clique in tested_nodes:
        for node in clique:
            if graph.nodes[node]['status'] == 'I':
                positive_nodes += clique
                break
        negative_nodes += clique
    return positive_nodes, negative_nodes

def test_strat_random_sample(graph, num_tests):
    '''
    Randomly select n nodes of the graph to be tested; tests those nodes and mutates graph accordingly.

    Parameters: 
        "graph" : NetworkX graph to be analyzed
        "num_tests" : Number of nodes to be tested; nonnegative integer
    Returns:
        list of nodes that were tested, number of tests that were used, number of extra tests
    '''
    extra_tests = max(num_tests - len(graph),0)

    tested_nodes = sample(list(graph.nodes()), num_tests - extra_tests)
    positive_nodes, negative_nodes = perform_test(graph, tested_nodes)
    update_positive_tests(graph, positive_nodes, negative_nodes)
    return tested_nodes, len(tested_nodes), extra_tests

def test_strat_high_contact(graph, d = 0, num_tests = None, recently_tested = set()):
    '''
    If num_tests is None, test all nodes with degree greater than or equal to d in graph and mutates graph accordingly.
    If num_tests is not None, test the num_tests highest degree nodes.

    Parameters: 
        "graph" : NetworkX graph to be analyzed
        "d" : nonnegative integer.
        "num_tests" : Number of nodes to be tested. If None, test all nodes with degree greater than or equal to d
    Returns:
        list of nodes that were tested, number of tests that were used, number of extra tests
    '''
    node_deg_pairs = list(graph.degree())
    if num_tests is None:
        tested_nodes = [node for node, deg in node_deg_pairs if deg >= d and node not in recently_tested]
        extra_tests = 0
    else:
        tested_nodes = graph.graph['node_degrees'][:num_tests]
        extra_tests = num_tests - len(tested_nodes)
    positive_nodes, negative_nodes = perform_test(graph, tested_nodes)
    update_positive_tests(graph, positive_nodes, negative_nodes)
    return tested_nodes, len(tested_nodes), extra_tests

def test_strat_pool(graph, clique_size = FAMILY_CLIQUE_SIZE, num_tests = None):
    '''
    Test all nodes that are part of families (defined as maximal cliques of specified size or greater) in graph. Mutates graph accordingly.

    Parameters:
        "graph" : NetworkX graph to be analyzed
        "clique_size" : nonnegative integer >= 2.
        "num_tests" : Number of nodes to be tested; if None, test all cliques of size greater than or equal to clique_size

    Returns:
        list of cliques (each a list of nodes) that were tested
    '''

    tested_nodes = []
    #max_cliques = nx.find_cliques(graph)
    if num_tests is None:
        for size in graph.graph['clique_sizes']:
            if size >= clique_size:
                tested_nodes += graph.graph['clique_dict'][size]
    else:
        for size in graph.graph['clique_sizes']:
            next_nodes = graph.graph['clique_dict'][size]
            if len(tested_nodes) + len(next_nodes) > num_tests:
                tested_nodes += next_nodes[:num_tests-len(tested_nodes)]
                break
            else:
                tested_nodes += next_nodes
        
    extra_tests = max(num_tests - len(tested_nodes), 0)
    positive_nodes, negative_nodes = perform_clique_test(graph, tested_nodes)
    update_positive_tests(graph, positive_nodes, negative_nodes)
    return tested_nodes, len(tested_nodes), extra_tests

def test_strat_most_infected(graph, num_tests):
    '''
    Preferentially test the nodes who have been infected for the longest (defined as people who have been infected for >= 3 days), only a certain percent
    of these are "true" infected, which can be defined seperately
    
    Parameters:
        "graph" : NetworkX graph to be analyzed

    Returns:
        list of nodes that we tested
    '''
    tested_nodes = []
    I_n = [n for n,v in graph.nodes(data=True) if v['status'] == 'I']
    I_checked = 0
    attempt_tested_dist = norm(SYMPTOM_DIST_MEAN, SYMPTOM_DIST_SD)
    for infected in I_n:
        days_since_I = graph.nodes[infected]['days_since_I']
        if random.random() < attempt_tested_dist.pdf(days_since_I):
            tested_nodes.append(infected)
    if len(tested_nodes) > num_tests:
        tested_nodes.sort(key = graph.nodes[infected]['days_since_I'])
        tested_nodes = tested_nodes[:num_tests]
    elif len(tested_nodes) < num_tests:
        extra_tested_nodes = test_strat_random_sample(graph, num_tests - len(tested_nodes))

    positive_nodes, negative_nodes = perform_test(graph, tested_nodes)
    update_positive_tests(graph, positive_nodes, negative_nodes)
    return tested_nodes

g = nx.Graph()
g.add_edge(1,2)
g.add_edge(1,3)
g.add_edge(1,4)
g.add_edge(1,5)
g.add_edge(5,6)
g.add_edge(2,3)


for i in range(1,7):
    g.nodes[i]['status'] = 'I'

for edge in g.edges():
    g.edges[edge]['weight'] = 1

print(test_strat_random_sample(g, 1))
print(test_strat_high_contact(g, 4))

dist = norm(0,1)

print(dist.pdf(2))
