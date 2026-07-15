import networkx as nx

# Example PPI interactions
edges = [
    ("P53", "MDM2"),
    ("P53", "BAX"),
    ("MDM2", "RB1"),
    ("BAX", "CASP3")
]

# Create graph
G = nx.Graph()
G.add_edges_from(edges)

# Degree calculation
degree = dict(G.degree())

# Betweenness centrality calculation
betweenness = nx.betweenness_centrality(G)

print("Protein\tDegree\tBetweenness")
for node in G.nodes():
    print(node, "\t", degree[node], "\t", betweenness[node])
