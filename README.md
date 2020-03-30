# Modeling COVID-19 Transmission and Testing through Social Networks

## Background 
In light of the COVID-19 outbreak, and the limited test kits avalible, we decided to create a graph based SEIR model that could be used to ask questions about the effect of different testing methods.  We used facebook friend connections from the Stanford SNAP group as a proxy for physical contacts between people that would allow the disease to spread.

## Data
The Facebook dataset is was downloaded from [Stanford SNAP](https://snap.stanford.edu/data/ego-Facebook.html) and is contained in the file facebook_combined.txt.

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

## Model 
We used an SEIR model.  In this framework, succeptile (S) individuals can become exposed (E) with some probability if they share an edge with an infected (I) individual.  Exposed individuals either develop the disease with some probability after sometime causing them to become infected (I) or they do not develop the disease in which case they return to being succeptible (S).  Infected indivuduals will transition to recovered after having the disease for some time.  

## Testing Strategies 
We considered 4 different testing regimes: 
* No tests preformed
* The most symptomatic individual are tested 
* The most connected individuals are tested
* Tests are preformed randomly 
With each strategy the user can choose how many tests to allocate to each strategy, which allows flexibility of the model to consider different combinations of testing strategies as well

## Code
