# A Linear-Time Algorithm for Computing the Minimum Number of Trees to Cover the Edges of Phylogenetic Networks

This repository contains the implementation of the program from the accompanying paper  
**"A Linear-Time Algorithm for Computing the Minimum Number of Trees to Cover the Edges of Phylogenetic Networks"** (SIURO submission 2025).

The program takes an input directed phylogenetic network and computes the **minimum number _k_** of embedded trees required to edge-cover all edges of the network in **O(|V| + |E|)** time.

---

## Overview

The algorithm implements the theoretical results proved in the paper:
```
k(N) = max{max in-degree, ⌈max out-degree / 2⌉}
```

It applies to any directed acyclic phylogenetic network *N* by performing:

1. **Vertex-splits** for nodes with both in-degree > 1 and out-degree > 1
2. **Edge-contractions** for consecutive reticulations ("stack-reticulations")
3. Computation of _k_ from degree properties

---

## Requirements

- Python ≥ 3.9
- Required Python packages:
```bash
  pip install networkx matplotlib pydot
```

- **Optional (for visualization):** Graphviz must be installed:
```bash
  # macOS
  brew install graphviz
  
  # Linux
  sudo apt install graphviz
```

---

## Installation

1. Clone or download this repository:
```bash
   git clone <repository-url>
   cd <repository-directory>
```

2. Install dependencies:
```bash
   pip install networkx matplotlib pydot
```

---

## Usage

Run the program:
```bash
python Iteration1.py
# or
python3 Iteration1.py
```

### Output

The script will print:
- Reticulation, tree, and leaf vertices (before/after operations)
- Vertices with the highest in- and out-degree
- The computed **minimum number of embedded trees _k_**
- Total runtime in seconds

### Example Output
```
Node degrees before splitting:
Node 1: In-Degree = 1, Out-Degree = 3
...
Reticulation Vertices (After Operations): {54, 56, ...}
Tree Vertices (After Operations): {14, 27, 31, ...}
Reticulation with the highest in-degree: [54], Value: 5
Tree Vertex with the highest out-degree: [14], Value: 8
Minimum number of Embedded Trees k: 5
Program execution time: 0.00402 seconds
```

---

## Visualization (Optional)

To enable visualization:

1. Open `Iteration1.py`
2. Uncomment the following lines:
```python
   visualize_phylogenetic_network(G, "Phylogenetic Network Before Operations", Reticulation, TreeVert, Leaf)
   visualize_phylogenetic_network(G, "Phylogenetic Network After Operations", Reticulation, TreeVert, Leaf)
```
3. Run the script again

**Color legend:**
- 🔴 Red: Reticulation vertices
- 🟢 Green: Tree vertices
- 🔵 Blue: Leaf vertices

---

## Default Example Network

The default graph constructed in the script (`G.add_edges_from([...])`) is a non-binary phylogenetic network of approximately 60 nodes and 70 directed edges. It includes:
- Multiple reticulations
- High-out-degree tree vertices
- Several leaves

This network corresponds to the complex example analyzed in **Example 8.1 (Figure 14)** of the paper, where the algorithm yields _k_ = 5. It demonstrates correctness and linear-time performance on realistic phylogenetic data.

---

## Using Custom Networks

You can analyze your own networks by replacing the default edge list in `Iteration1.py`:
```python
# Replace this block in Iteration1.py
G.add_edges_from([
    (A, B), (B, C), ...
])
```

**Requirements:**
1. The graph must be **directed** and **acyclic**
2. Vertices must be labeled consistently (string or integer)

Run the script again to calculate _k_ for your new network.

---

## Citation

If you use this code or results, please cite (if accepted):
```
J. Van Schie, "A Linear-Time Algorithm for Computing the Minimum Number of Trees 
to Cover the Edges of Phylogenetic Networks," SIAM Undergraduate Research Online 
(SIURO), 2025.
```

Otherwise, reference accordingly.

---

## Contact

**Author:** Jurre van Schie  
**Affiliation:** Department of Pure & Applied Mathematics, Faculty of Science and Engineering, Waseda University  
**Email:** jurre.vanschie@akane.waseda.jp
