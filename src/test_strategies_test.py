import unittest
import sys
import networkx as nx
from random import sample
from test_strategies import update_positive_tests


class TestUpdatePositiveTests(unittest.TestCase):
	def setUp(self):
		""" Create basic graph to test """
		F=nx.path_graph(10)
		G=nx.Graph()

		for (u, v) in F.edges():
		    G.add_edge(u,v,weight=1)
		nx.set_node_attributes(G, False, name = "confirmed positive")
		nx.set_node_attributes(G, False, name = "tested")
		nx.set_node_attributes(G, False, name = "infected")
		nx.set_node_attributes(G, {5: True, 9: True, 8: True}, name = "infected")
		self.G = G

	def test_1(self):
		''' Test only confirmed negative  ''' 
		update_positive_tests(self.G, [], [2])
		expected_confirmed_pos  = [False, False, False, False, False, False, False, False, False, False]
		expected_tested = [False, False, True, False, False, False, False, False, False, False]
		expected_edge_weights = [1, 1.1, 1.1, 1, 1, 1, 1, 1, 1]
		self.assertEqual([self.G.nodes[n]["confirmed positive"] for n in self.G.nodes], expected_confirmed_pos)
		self.assertEqual([self.G.nodes[n]["tested"] for n in self.G.nodes], expected_tested)
		weight = nx.get_edge_attributes(self.G, "weight")
		self.assertEqual([weight[e] for e in self.G.edges], expected_edge_weights)


	def test_2(self):
		''' Test a single confirmed positive ''' 
		update_positive_tests(self.G, [5], [])
		expected_confirmed_pos  = [False, False, False, False, False, True, False, False, False, False]
		expected_tested = [False, False, True, False, False, True, False, False, False, False]
		expected_edge_weights = [1, 1.1, 1.1, 1, .1, .1, 1, 1, 1]
		self.assertEqual([self.G.nodes[n]["confirmed positive"] for n in self.G.nodes], expected_confirmed_pos)
		self.assertEqual([self.G.nodes[n]["tested"] for n in self.G.nodes], expected_tested)
		weight = nx.get_edge_attributes(self.G, "weight")
		self.assertEqual([weight[e] for e in self.G.edges], expected_edge_weights)


	def test_2(self):
		''' Test multiple confirmed negatives and positives, with multiplicative weight effects '''
		update_positive_tests(self.G, [8,9], [1, 7])
		expected_confirmed_pos  = [False, False, False, False, False, True, False, False, True, True]
		expected_tested = [False, True, True, False, False, True, False, True, True, True]
		expected_edge_weights = [1.1, 1.21, 1.1, 1, .1, .1, 1.1, .11, .01]
		self.assertEqual([self.G.nodes[n]["confirmed positive"] for n in self.G.nodes], expected_confirmed_pos)
		self.assertEqual([self.G.nodes[n]["tested"] for n in self.G.nodes], expected_tested)
		weight = nx.get_edge_attributes(self.G, "weight")
		self.assertEqual([weight[e] for e in self.G.edges], expected_edge_weights)


if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)



