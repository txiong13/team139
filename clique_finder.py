#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 13:05:49 2020

@author: cxyang
"""

import pickle
import networkx as nx
import numpy as np
import pickle

graph = {}
with open('fb_graph.pkl', 'rb') as f:
    graph = pickle.load(f)
G = nx.from_dict_of_dicts(graph)
        
cliques = list(nx.find_cliques(G))

max_clique_dict = {}
for clique in cliques:
    if len(clique) not in max_clique_dict:
        max_clique_dict[len(clique)] = [clique]
    else:
        max_clique_dict[len(clique)].append(clique)

f = open("cliques_dict.pkl","wb")
pickle.dump(max_clique_dict,f)
f.close()