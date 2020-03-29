## Data
The Facebook dataset is facebook_combined.txt.

## Preprocessing
The Facebook data is loaded into a NetworkX graph. The graph is stored in fb_graph.pkl. To load the graph, run:
```python
import pickle
import networkx as nx
graph = {}
with open('fb_graph.pkl', 'rb') as f:
    graph = pickle.load(f)
G = nx.from_dict_of_dicts(graph)
```

## Code
