## Data
The Facebook dataset is facebook_combined.txt.

## Preprocessing
The Facebook data was loaded into a NetworkX graph. Each node contains the attribute "status", which is currently set to "S" for all nodes. The graph is stored in fb_graph.pkl. To load the graph, run:
```python
graph = {}
with open('fb_graph.pkl', 'rb') as f:
    graph = pickle.load(f)
G = nx.from_dict_of_dicts(graph)
```

