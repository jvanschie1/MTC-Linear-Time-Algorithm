import time
import networkx as nx
import matplotlib.pyplot as plt
import pydot
from networkx.drawing.nx_pydot import graphviz_layout
import math

start_time = time.time()
# Create a directed graph
G = nx.DiGraph()

# Add edges (example)
G.add_edges_from([(5, 11), (11, 54), (54, 27), (27, 31), (31, 30), (30, 43), (43, 36), (36, 40), (40, 33), (33, 41), 
(33, 55), (40, 14), (14, 59), (14, 16), (36, 38), (38, 21), (43, 15), (15, 22), (22, 51), (22, 57), 
(30, 18), (18, 60), (60, 61), (61, 20), (31, 52), (52, 26), (26, 50), (27, 56), (56, 19), (54, 23), 
(23, 56), (11, 39), (5, 49), (49, 24), (49, 4), (4, 23), (4, 1), (1, 2), (2, 44), (2, 25), 
(1, 42), (42, 52), (42, 45), (45, 6), (6, 61), (6, 58), (58, 29), (58, 38), (45, 28), (28, 18), 
(28, 53), (53, 34), (53, 3), (3, 7), (3, 8), (8, 26), (8, 35), (35, 60), (35, 46), (46, 10), 
(10, 37), (10, 32), (46, 48), (48, 47), (48, 9), (9, 15), (9, 12), (12, 17), (12, 13)
])

# Sort nodes in ascending order and calculate degrees
sorted_nodes = sorted(G.nodes)

# Define an empty set for Reticulation nodes
Reticulation = set()
# Define an empty set for Tree nodes
TreeVert = set()
# Define an empty set for Leaves
Leaf = set()
def planar_layout(G):
    # Generate the planar layout
    pos = nx.planar_layout(G)
    return pos

def visualize_phylogenetic_network(G, title, reticulation_nodes, tree_nodes, leaf_nodes):
    """
    Visualize the graph with a planar layout (non-crossing edges), with reticulations, tree vertices, and leaves.
    
    Args:
    - G: The graph to visualize.
    - title: Title of the plot.
    - reticulation_nodes: Set of reticulation nodes.
    - tree_nodes: Set of tree nodes.
    - leaf_nodes: Set of leaf nodes.
    """
    plt.figure(figsize=(10, 8))
    
    # Use planar layout
    pos = planar_layout(G)  # Planar layout
    
    # Assign colors to node categories
    node_colors = []
    for node in G.nodes:
        if node in reticulation_nodes:
            node_colors.append("red")
        elif node in tree_nodes:
            node_colors.append("green")
        elif node in leaf_nodes:
            node_colors.append("blue")
        else:
            node_colors.append("gray")  # For any uncategorized nodes
    
    # Draw the graph with the planar layout
    nx.draw(
        G, pos, with_labels=True, node_size=700, node_color=node_colors,
        font_size=12, font_weight='bold', edge_color='gray', arrows=True
    )
    
    # Add title
    plt.title(title)
    plt.show()

# Example usage (before and after visualization):
# visualize_phylogenetic_network(G, "Phylogenetic Network Before Operations", Reticulation, TreeVert, Leaf)
# visualize_phylogenetic_network(G, "Phylogenetic Network After Operations", Reticulation, TreeVert, Leaf)

print("Node degrees before splitting:")
for node in G.nodes:
    print(f"Node {node}: In-Degree = {G.in_degree(node)}, Out-Degree = {G.out_degree(node)}")

# Obtain the Reticulation set
for node in sorted_nodes:
    if G.in_degree(node) >= 2:
        Reticulation.add(node)
print(f"Reticulation Vertices (Before Operation): ", Reticulation)
# Obtain the Tree Vertex set
for node in sorted_nodes:
    if G.out_degree(node) >= 2:
        TreeVert.add(node)
print(f"Tree Vertices (Before Operation): ", TreeVert)
# Obtain the Leaf set
for node in sorted_nodes:
    if G.in_degree(node) == 1 and G.out_degree(node) == 0:
        Leaf.add(node) 
print(f"Leaves: ", Leaf)

#visualize_phylogenetic_network(G, "Phylogenetic Network Before Operations", Reticulation, TreeVert, Leaf)

# Identify nodes that need splitting
nodes_to_split = Reticulation.intersection(TreeVert)

# Split nodes
for node in nodes_to_split:
    v_in = f"{node}_in"
    v_out = f"{node}_out"

    G.add_node(v_in)
    G.add_node(v_out)

    # Redirect incoming edges to v_in
    for neighbor in list(G.predecessors(node)):
        G.add_edge(neighbor, v_in)
    # Redirect outgoing edges to v_out
    for neighbor in list(G.successors(node)):
        G.add_edge(v_out, neighbor)
    
    # Connect v_in to v_out
    G.add_edge(v_in, v_out)
    # Remove the original node
    G.remove_node(node)

# Recompute sets after splitting
Reticulation = {node for node in G.nodes if G.in_degree(node) >= 2}
TreeVert = {node for node in G.nodes if G.out_degree(node) >= 2}

# Update Reticulation set after splitting and check for merges
merged_reticulation = set()

def merge_reticulations(node):
    neighbors = list(G.successors(node)) + list(G.predecessors(node))
    for neighbor in neighbors:
        if neighbor in Reticulation and neighbor not in merged_reticulation:
            # Transfer incoming edges
            for pred in list(G.predecessors(neighbor)):
                if pred != node:  # Avoid self-loops
                    G.add_edge(pred, node)
            # Transfer outgoing edges
            for succ in list(G.successors(neighbor)):
                if succ != node:  # Avoid self-loops
                    G.add_edge(node, succ)
            # Remove the connecting edge
            if G.has_edge(node, neighbor):
                G.remove_edge(node, neighbor)
            # Remove the neighbor node
            G.remove_node(neighbor)
            # Mark the neighbor as merged
            merged_reticulation.add(neighbor)
            # Recursively merge reticulations
            merge_reticulations(node)

# Only merge when there are consecutive reticulations
for node in list(Reticulation):
    if node not in merged_reticulation:
        merge_reticulations(node)

# Update Reticulation set after merging
Reticulation = {node for node in G.nodes if G.in_degree(node) >= 2}

#visualize_phylogenetic_network(G, "Phylogenetic Network After Operations", Reticulation, TreeVert, Leaf)

# Find the maximum in-degree value
max_in_degree_value = max(G.in_degree(node) for node in G.nodes)

# Find all nodes with the maximum in-degree value
max_in_degree_nodes = [node for node in G.nodes if G.in_degree(node) == max_in_degree_value]

# Find the maximum out-degree value
max_out_degree_value = max(G.out_degree(node) for node in G.nodes)

# Find all nodes with the maximum out-degree value
max_out_degree_nodes = [node for node in G.nodes if G.out_degree(node) == max_out_degree_value]

if math.ceil(max_out_degree_value / 2) < max_in_degree_value:
    ET = max_in_degree_value

else:
    ET = math.ceil(max_out_degree_value / 2)
# Print degrees for each node in ascending order
#for node in sorted_nodes:
#    in_edges = G.in_degree(node)
#    out_edges = G.out_degree(node)
#    print(f"Vertex {node}: In-Degree = {in_edges}, Out-Degree = {out_edges}")
if merged_reticulation != Reticulation:
    print(f"Reticulation Vertices (After Operations): ", Reticulation)
print(f"Tree Vertices (After Operations): ", TreeVert)
print(f"Reticulation with the highest in-degree: {max_in_degree_nodes}, Value: {max_in_degree_value}")
print(f"Tree Vertex with the highest out-degree: {max_out_degree_nodes}, Value: {max_out_degree_value}")
print(f"Minimum number of Embedded Trees k: ", ET)
#print(f"Leaves: ", Leaf)
end_time = time.time()
elapsed_time = end_time - start_time

print(f"Program execution time: {elapsed_time:.5f} seconds")