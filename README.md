# A Linear-Time Algorithm for Computing the Minimum Number of Trees to Cover the Edges of Phylogenetic Networks

This repository contains the implementation and experimental data for the paper  
**"A Linear-Time Algorithm for Computing the Minimum Number of Trees to Cover the Edges of Phylogenetic Networks"** by Jurre van Schie (SIURO, 2026).

The program takes a directed phylogenetic network as input and computes the **minimum number *k*** of embedded trees required to edge-cover all edges of the network in **O(|V| + |E|)** time.

---

## Overview

The algorithm implements the theoretical results proved in the paper (Theorems 5.5, 6.2, and 7.1):

```
k(N) = max{ max in-degree, ⌈max out-degree / 2⌉ }
```

It applies to any directed acyclic phylogenetic network *N* by performing:

1. **Vertex-splits** for nodes with both in-degree > 1 and out-degree > 1
2. **Edge-contractions** for consecutive reticulations (stack-reticulations)
3. Computation of *k* from the resulting degree properties

---

## Repository Structure

```
.
├── Iteration1.py                  # Main algorithm — computes k(N) for batch input
├── random_network_generator.py    # Generates random phylogenetic networks
├── 100EDataSet/                   # Networks and results for |E| ≈ 99
├── 500EDataSet/                   # Networks and results for |E| ≈ 497
├── 1000EDataSet/                  # Networks and results for |E| ≈ 999
├── 5000EDataSet/                  # Networks and results for |E| ≈ 4997
├── 10000EDataSet/                 # Networks and results for |E| ≈ 9999
├── 50000EDataSet/                 # Networks and results for |E| ≈ 50000
├── 100000EDataSet/                # Networks and results for |E| ≈ 99999
└── README.md
```

Each data folder contains:
- **Input files:** Generated network files (edge lists) produced by `random_network_generator.py`
- **Result files:** Output from running `Iteration1.py`, including *k*, vertex/edge counts, degree information, and runtime for each network

These datasets were used to produce the scalability results reported in Section 8 and Figure 15 of the paper. Networks were generated at three reticulation ratios (16.7%, 33.4%, 50.1%), with 100 networks per edge count.

---

## Requirements

- Python ≥ 3.9
- Required Python packages:

```bash
pip install networkx
```

---

## Usage

### Computing k(N)

`Iteration1.py` reads a batch of networks from a text file, computes *k* for each, and writes the results to an output file.

1. Set the `input_file` and `output_file` paths in the `main()` function of `Iteration1.py`
2. Run:

```bash
python Iteration1.py
```

**Output per network:**
```
Graph 1: k(N1) = 5  |V| = 65, |E| = 72, max_indeg = 5, max_outdeg = 4, time = 0.00402s
```

### Generating Random Networks

`random_network_generator.py` generates random phylogenetic networks with a specified number of leaves and reticulations.

```bash
python random_network_generator.py
```

You will be prompted for:
- Number of leaves (*n*)
- Number of reticulations (*r*)
- Number of networks to generate

The generator starts from a random binary tree with *n* leaves and adds *r* reticulation edges, following the method adapted from Suzuki & Hayamizu (2025) [18].

### Using a Custom Network

To analyze a single custom network, replace the edge list read in `Iteration1.py` or create an input file in the expected format:

```
# NETWORK 1
    (0, 1),
    (0, 2),
    (1, 3),
    ...
# END NETWORK 1
```

The graph must be **directed** and **acyclic** with a single root.

---

## Reproducing the Experimental Results

To reproduce the scalability experiment from Section 8 of the paper:

1. Generate networks using `random_network_generator.py` with the desired parameters
2. Run `Iteration1.py` on each generated file
3. The paper reports results for 700 networks (100 per size) at a balanced reticulation ratio of 33.4%, across |E| ∈ {99, 497, 999, 4997, 9999, 50000, 99999}

Pre-generated networks and their results are included in the data folders listed above.

---

## Citation

If you use this code or results, please cite:

```
J. van Schie, "A Linear-Time Algorithm for Computing the Minimum Number of Trees
to Cover the Edges of Phylogenetic Networks," SIAM Undergraduate Research Online
(SIURO), 2026.
```

---

## Contact

**Author:** Jurre van Schie  
**Supervisor:** Prof. Momoko Hayamizu  
**Affiliation:** Department of Pure & Applied Mathematics, Faculty of Science and Engineering, Waseda University  
**Email:** jurre.vanschie@akane.waseda.jp
