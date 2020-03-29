import unittest
import sys
import networkx as nx
from random import sample
from test_strategies import update_positive_tests, perform_test, test_strat_random_sample, test_strat_high_contact


class TestUpdatePositiveTests(unittest.TestCase):
	'''
	Limited test set for the update_positive_tests function
	'''
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
		quarantine_infectivity = 0.1
		confirmed_negative_infectivity = 1.1
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
		quarantine_infectivity = 0.1
		confirmed_negative_infectivity = 1.1
		update_positive_tests(self.G, [5], [])
		expected_confirmed_pos  = [False, False, False, False, False, True, False, False, False, False]
		expected_tested = [False, False, False, False, False, True, False, False, False, False]
		expected_edge_weights = [1, 1, 1, 1, .1, .1, 1, 1, 1]
		self.assertEqual([self.G.nodes[n]["confirmed positive"] for n in self.G.nodes], expected_confirmed_pos)
		self.assertEqual([self.G.nodes[n]["tested"] for n in self.G.nodes], expected_tested)
		weight = nx.get_edge_attributes(self.G, "weight")
		self.assertEqual([weight[e] for e in self.G.edges], expected_edge_weights)


	def test_3(self):
		''' Test multiple confirmed negatives and positives, with multiplicative weight effects '''
		quarantine_infectivity = 0.1
		confirmed_negative_infectivity = 1.1
		update_positive_tests(self.G, [8,9], [1, 2, 7])
		expected_confirmed_pos  = [False, False, False, False, False, False, False, False, True, True]
		expected_tested = [False, True, True, False, False, False, False, True, True, True]
		expected_edge_weights = [1.1, 1.1, 1.1, 1, 1, 1, 1.1, 1*.1*1.1, .1]
		self.assertEqual([self.G.nodes[n]["confirmed positive"] for n in self.G.nodes], expected_confirmed_pos)
		self.assertEqual([self.G.nodes[n]["tested"] for n in self.G.nodes], expected_tested)
		weight = nx.get_edge_attributes(self.G, "weight")
		self.assertEqual([weight[e] for e in self.G.edges], expected_edge_weights)

class TestStratRandomSampleTest(unittest.TestCase):
	''' Limited test set for the test_strat_random_sample testing strategy '''
	def setUp(self):
		""" Create basic graph to test """
		F=nx.path_graph(10)
		G=nx.Graph()

		for (u, v) in F.edges():
		    G.add_edge(u,v,weight=1)
		nx.set_node_attributes(G, False, name = "confirmed positive")
		nx.set_node_attributes(G, False, name = "tested")
		nx.set_node_attributes(G, False, name = "infected")
		nx.set_node_attributes(G, \
			{0: True, 1: False, 2: False, 3: True, 4: False, 5: False, 6: True, 7: True, 8: False, 9: False},\
			name = "status")
		nx.set_node_attributes(G, {5: True, 9: True, 8: True}, name = "infected")
		self.G = G
	
	def test_1(self):
		'''
		 Test n = 0 
		 expect to see no change in the graph
		 '''
		quarantine_infectivity = 0.1
		confirmed_negative_infectivity = 1.1
		prev_graph = self.G.copy()
		test_strat_random_sample(self.G, 0)

		self.assertEqual(self.G.nodes, prev_graph.nodes)
		self.assertEqual(self.G.edges, prev_graph.edges)
		self.assertEqual([self.G.nodes[n]["confirmed positive"] for n in self.G.nodes], \
			[prev_graph.nodes[n]["confirmed positive"] for n in prev_graph.nodes])
		self.assertEqual([self.G.nodes[n]["tested"] for n in self.G.nodes], \
			[prev_graph.nodes[n]["tested"] for n in prev_graph.nodes])
		weight = nx.get_edge_attributes(self.G, "weight")
		prev_weight = nx.get_edge_attributes(prev_graph, "weight")
		self.assertEqual([weight[e] for e in self.G.edges], [prev_weight[e] for e in prev_graph.edges])


	def test_2(self):
		''' Test n = 1 '''
		quarantine_infectivity = 0.1
		confirmed_negative_infectivity = 1.1
		test_strat_random_sample(self.G, 1)
		self.assertTrue(all([self.G.nodes[n]["status"] == "I" if self.G.nodes[n]["confirmed positive"] \
			else self.G.nodes[n]["status"] != "I" for n in self.G.nodes]))
		tested_nodes = [i for i, tested in enumerate([self.G.nodes[n]["tested"] for n in self.G.nodes]) if tested] 
		self.assertEqual(len(tested_nodes), 1)
		if self.G.nodes[tested_nodes[0]]["status"] == "I":
			self.assertTrue([d["weight"] == 0.1 for u, v, d in self.G.edges(tested_nodes, data = True)])
		else: 
			self.assertTrue([d["weight"] == 0.1 for u, v, d in self.G.edges(tested_nodes, data = True)])

	def test_3(self):
		''' Test n = 2 '''
		quarantine_infectivity = 0.1
		confirmed_negative_infectivity = 1.1
		test_strat_random_sample(self.G, 2)
		self.assertTrue(all([self.G.nodes[n]["status"] == "I" if self.G.nodes[n]["confirmed positive"] \
			else self.G.nodes[n]["status"] != "I" for n in self.G.nodes]))
		tested_nodes = [i for i, tested in enumerate([self.G.nodes[n]["tested"] for n in self.G.nodes]) if tested] 
		self.assertEqual(len(tested_nodes), 2)
		self.assertTrue([d["weight"] != 0.1 for u, v, d in self.G.edges(tested_nodes, data = True)])

class TestStratHighContactTest(unittest.TestCase):
	''' Limited test set for the test_strat_high_contact testing strategy '''
	def setUp(self):
		""" Create basic graph to test """
		F=nx.path_graph(10)
		G=nx.Graph()

		for (u, v) in F.edges():
		    G.add_edge(u,v,weight=1)
		nx.set_node_attributes(G, False, name = "confirmed positive")
		nx.set_node_attributes(G, False, name = "tested")
		nx.set_node_attributes(G, False, name = "infected")
		nx.set_node_attributes(G, \
			{0: "I", 1: "S", 2: "S", 3: "I", 4: "S", 5: "S", 6: "I", 7: "I", 8: "S", 9: "S"},\
			name = "status")
		nx.set_node_attributes(G, {5: True, 9: True, 8: True}, name = "infected")
		self.G = G

	def test_1(self):
		''' d > the highest degree ''' 
		quarantine_infectivity = 0.1
		confirmed_negative_infectivity = 1.1
		prev_graph = self.G.copy()
		test_strat_high_contact(self.G, 10)

		self.assertEqual(set(self.G.nodes), set(prev_graph.nodes))
		self.assertEqual(set(self.G.edges), set(prev_graph.edges))
		self.assertEqual([self.G.nodes[n]["confirmed positive"] for n in self.G.nodes], \
			[prev_graph.nodes[n]["confirmed positive"] for n in prev_graph.nodes])
		self.assertEqual([self.G.nodes[n]["tested"] for n in self.G.nodes], \
			[prev_graph.nodes[n]["tested"] for n in prev_graph.nodes])
		weight = nx.get_edge_attributes(self.G, "weight")
		prev_weight = nx.get_edge_attributes(prev_graph, "weight")
		self.assertEqual([weight[e] for e in self.G.edges], [prev_weight[e] for e in prev_graph.edges])

	def test_2(self):
		''' some nodes tested but not '''
		quarantine_infectivity = 0.1
		confirmed_negative_infectivity = 1.1
		test_strat_high_contact(self.G, 2)

		self.assertEqual([self.G.nodes[n]["confirmed positive"] for n in self.G.nodes], \
			[False, False, False, True, False, False, True, True, False, False])
		self.assertEqual([self.G.nodes[n]["tested"] for n in self.G.nodes], \
			[False, True, True, True, True, True, True, True, True, False])
		weight = nx.get_edge_attributes(self.G, "weight")
		self.assertTrue(all([weight[e] != 1 for e in self.G.edges]))

	def test_3(self):
		''' all nodes tested '''
		quarantine_infectivity = 0.1
		confirmed_negative_infectivity = 1.1
		prev_graph = self.G.copy()
		test_strat_high_contact(self.G, 0)

		self.assertEqual(set(self.G.nodes), set(prev_graph.nodes))
		self.assertEqual(set(self.G.edges), set(prev_graph.edges))
		self.assertEqual([self.G.nodes[n]["confirmed positive"] for n in self.G.nodes], \
			[prev_graph.nodes[n]["status"] == "I" for n in prev_graph.nodes])
		self.assertEqual([self.G.nodes[n]["tested"] for n in self.G.nodes], \
			[True for i in range(10)])
		weight = nx.get_edge_attributes(self.G, "weight")
		self.assertTrue(all([weight[e] != 1 for e in self.G.edges]))


if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)



