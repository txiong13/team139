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
We used an SEIR model.  In this framework, succeptile (S) individuals can become exposed (E) with some probability if they share an edge with an infected
(I) individual.  Exposed individuals either develop the disease with some probability after sometime causing them to become infected (I) or they do not 
develop the disease in which case they are recovered (R).  Infected indivuduals can transition to being hospitalized and then either dead or recovered (R).
Conversely individuals can go from infected to recovered (R) if they have the disease for long enough but do not become hospitalized.

## Testing Strategies 
We considered 4 different testing regimes: 
* No tests preformed
* The most symptomatic individual are tested 
* The most connected individuals are tested
* Tests are preformed randomly 
With each strategy the user can choose how many tests to allocate to each strategy, which allows flexibility of the model to consider different combinations of testing strategies as well

## Parameters
R_0 = 2.8 ([Lou Et al. March 20, average of 14 other R0 studies](https://www.ncbi.nlm.nih.gov/pubmed/32007643)) <br>
TOTAL_DURATION_OF_INFECTION = 14 (WHO China join mission on COVID pg 14) <br>
HOSPITALIZED_DURATION_OF_INFECTION = 20 IQR: 17-24, (Zhou Et al. Lancet 2020) <br>
DIST_INCUBATION_MEAN = 1.621 (Lauer Et al., Annals of Internal Medicine, March 2020) <br>
DIST_INCUBATION_SD = .481 (Lauer Et al., Annals of Internal Medicine, March 2020) <br>
PROB_ALWAYS_ASYMPTOMATIC = 82.1% (Mizumoto et al., Eurosurveilance, March 2020) <br>
DIST_HOSPITAL_MEAN = 8 days IQR: 4-10 (Wang et al. JAMA Network, Feb 2020) <br>
DIST_HOSPITAL_SD = 1 <br>
PROB_HOSPITAL = .1755 (https://www.cdc.gov/mmwr/volumes/69/wr/mm6912e2.htm?s_cid=mm6912e2_w) <br>
PROB_DEATH_IF_HOSPITAL = .01 (https://www.cdc.gov/mmwr/volumes/69/wr/mm6912e2.htm?s_cid=mm6912e2_w) <br>

## Assumptions
Period of time before social isolation follows the same distribution as incubation period
All connections are equally likely to get coronavirus from an infected person
All members of the network are between 22-40 years old
DIST_HOSPITAL_SD = 1 -- no distribution could be found

## Code
