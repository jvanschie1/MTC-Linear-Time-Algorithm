import networkx as nx
import random

def generate_random_network(n, r):
    """
    Generate a random phylogenetic network with n leaves and r reticulations.
    Starts from a tree with n leaves, then randomly adds reticulation edges.
    """
    network = nx.DiGraph()

    # Generate a tree with n leaves
    network.add_edges_from([(0, 1), (0, 2)])
    num_leaves = 2
    max_idx = 2
    leaf_set = [1, 2]

    while num_leaves < n:
        leaf = random.choice(leaf_set)
        leaf_set.remove(leaf)
        leaf_set.append(max_idx + 1)
        leaf_set.append(max_idx + 2)
        network.add_edges_from([(leaf, max_idx + 1), (leaf, max_idx + 2)])
        num_leaves = num_leaves + 1
        max_idx = max_idx + 2

    # Add r reticulations to the tree
    for i in range(r):
        while True:
            e1, e2 = random.sample(list(network.edges), 2)
            u1, v1 = e1
            u2, v2 = e2
            if not nx.has_path(network, v2, u1):
                break

        new_node1, new_node2 = max(network.nodes()) + 1, max(network.nodes()) + 2
        network.remove_edge(u1, v1)
        network.remove_edge(u2, v2)
        network.add_edges_from([
            (u1, new_node1),
            (new_node1, v1),
            (u2, new_node2),
            (new_node2, v2),
            (new_node1, new_node2),
        ])

    return network


if __name__ == "__main__":
    n = int(input("Number of leaves (n): "))
    r = int(input("Number of reticulations (r): "))
    num_networks = int(input("Number of networks to generate: "))
    output_file = f"generated_networks_n{n}_r{r}.txt"

    with open(output_file, "w") as f:
        for i in range(num_networks):
            print(f"Generating network {i + 1}/{num_networks}...")
            G = generate_random_network(n, r)
            edges = sorted(G.edges())

            f.write(f"# NETWORK {i + 1}\n")
            f.write("G.add_edges_from([\n")
            for edge in edges:
                f.write(f"    {edge},\n")
            f.write("])\n")
            f.write(f"# END NETWORK {i + 1}\n\n")

    print(f"All {num_networks} networks written to {output_file}")