import time
import networkx as nx
import math

def parse_networks(filename):
    """
    Parse the combined networks file and return a list of edge lists,
    one per network.
    """
    networks = []
    current_edges = []
    in_network = False

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("# NETWORK"):
                current_edges = []
                in_network = True
            elif line.startswith("# END NETWORK"):
                networks.append(current_edges)
                in_network = False
            elif in_network and line.startswith("("):
                # Parse edge tuple, e.g. "(0, 1),"
                line = line.rstrip(",").strip()
                parts = line.strip("()").split(",")
                u, v = int(parts[0].strip()), int(parts[1].strip())
                current_edges.append((u, v))

    return networks


def compute_k(G):
    """
    Compute the minimum number of embedded trees k(N) for a phylogenetic
    network G using the algorithm from the paper.
    Returns k and additional info.
    """
    # Classify vertices
    Reticulation = {node for node in G.nodes if G.in_degree(node) >= 2}
    TreeVert = {node for node in G.nodes if G.out_degree(node) >= 2}
    Leaf = {node for node in G.nodes if G.in_degree(node) == 1 and G.out_degree(node) == 0}

    # Step 1: Vertex-split nodes with both indeg > 1 and outdeg > 1
    nodes_to_split = Reticulation.intersection(TreeVert)
    for node in nodes_to_split:
        v_in = f"{node}_in"
        v_out = f"{node}_out"
        G.add_node(v_in)
        G.add_node(v_out)

        for neighbor in list(G.predecessors(node)):
            G.add_edge(neighbor, v_in)
        for neighbor in list(G.successors(node)):
            G.add_edge(v_out, neighbor)

        G.add_edge(v_in, v_out)
        G.remove_node(node)

    # Recompute sets after splitting
    Reticulation = {node for node in G.nodes if G.in_degree(node) >= 2}
    TreeVert = {node for node in G.nodes if G.out_degree(node) >= 2}

    # Step 2: Contract reticulation-reticulation edges (merge stack-reticulations)
    merged_reticulation = set()

    def merge_reticulations(node):
        neighbors = list(G.successors(node)) + list(G.predecessors(node))
        for neighbor in neighbors:
            if neighbor in Reticulation and neighbor not in merged_reticulation:
                for pred in list(G.predecessors(neighbor)):
                    if pred != node:
                        G.add_edge(pred, node)
                for succ in list(G.successors(neighbor)):
                    if succ != node:
                        G.add_edge(node, succ)
                if G.has_edge(node, neighbor):
                    G.remove_edge(node, neighbor)
                G.remove_node(neighbor)
                merged_reticulation.add(neighbor)
                merge_reticulations(node)

    for node in list(Reticulation):
        if node not in merged_reticulation:
            merge_reticulations(node)

    # Recompute after merging
    Reticulation = {node for node in G.nodes if G.in_degree(node) >= 2}

    # Step 3: Compute k = max(din, ceil(dout / 2))
    max_in_degree = max(G.in_degree(node) for node in G.nodes)
    max_out_degree = max(G.out_degree(node) for node in G.nodes)

    k = max(max_in_degree, math.ceil(max_out_degree / 2))

    return k, max_in_degree, max_out_degree, len(G.nodes), len(G.edges)


def main():
    input_file = "./100000EDataSet/generated_networks_n6501_r29000.txt"
    output_file = "./100000EDataSet/retheavy_results.txt"

    print(f"Parsing networks from {input_file}...")
    networks = parse_networks(input_file)
    print(f"Found {len(networks)} networks.\n")

    total_start = time.time()

    with open(output_file, "w") as out:
        out.write("Minimum Tree-Cover Problem - Results\n")
        out.write("=" * 50 + "\n\n")

        for i, edges in enumerate(networks):
            G = nx.DiGraph()
            G.add_edges_from(edges)

            num_vertices = len(G.nodes)
            num_edges = len(G.edges)

            start = time.time()
            k, max_in, max_out, final_v, final_e = compute_k(G)
            elapsed = time.time() - start

            line = (f"Graph {i + 1}: k(N{i + 1}) = {k}  "
                    f"|V| = {num_vertices}, |E| = {num_edges}, "
                    f"max_indeg = {max_in}, max_outdeg = {max_out}, "
                    f"time = {elapsed:.5f}s")

            print(line)
            out.write(line + "\n")

        total_elapsed = time.time() - total_start
        summary = f"\nTotal execution time: {total_elapsed:.5f}s"
        print(summary)
        out.write(summary + "\n")

    print(f"\nResults saved to {output_file}")


if __name__ == "__main__":
    main()