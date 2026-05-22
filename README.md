# Dijkstra's Shortest Path Algorithm

A clean Python implementation of **Dijkstra's algorithm** with a step-by-step animated visualization. Watch the algorithm explore the graph in real time and highlight the shortest path at the end.

---

## What it does

- Finds the shortest path between any two vertices in a weighted undirected graph
- Animates the algorithm step by step on a black background — nodes turn green as they get visited, and the shortest path lights up in bright green at the end
- Prints a full distance and predecessor table in the terminal

---

## Demo

```
Graph used:
        D
       / \
  A---B   F
   \ / \ /
    C---E

Edges: A-B:3, A-C:6, A-D:4, B-C:2, B-E:3, C-E:3, C-F:3, D-F:6, E-F:1

Result:
  Path     : A -> B -> E -> F
  Distance : 7

  Vertex   Distance   Previous
  --------------------------
  A        0          -
  B        3          A
  C        5          B
  D        4          A
  E        6          B
  F        7          E
```

---

## Files

| File | Description |
|------|-------------|
| `dijkstra_project.py` | Core algorithm — PriorityQueue, Edge, Graph, dijkstra(), shortest_path() and main |
| `animate.py` | Step-by-step animated visualization using matplotlib |

---

## How to run

### 1. Install dependencies
```bash
pip install matplotlib networkx
```

### 2. Run
```bash
python3 dijkstra_project.py
```

A window will pop up showing the animation. The terminal will also print the results table.

---

## Use it for any graph

Open `dijkstra_project.py` and change the edges at the bottom:

```python
g = Graph()
for v in ["X", "Y", "Z", "W"]:
    g.add_vertex(v)

g.add_edge("X", "Y", 5)
g.add_edge("Y", "Z", 2)
g.add_edge("X", "W", 8)
g.add_edge("W", "Z", 1)

source      = "X"
destination = "Z"
```

Everything else works automatically.

---

## How the algorithm works

1. Set distance of source to 0, all others to infinity
2. Add source to a priority queue
3. Pop the vertex with the smallest distance
4. For each unvisited neighbour calculate: `new_dist = current_dist + edge_weight`
5. If cheaper than known distance, update it
6. Repeat until all vertices are visited

The shortest path is reconstructed by following `previous` pointers backwards from destination to source, then reversing.

---

## Time complexity

| Graph type | Edges | Complexity |
|---|---|---|
| Tree / Path | V - 1 | O(V log V) |
| Sparse graph | O(V) | O(V log V) |
| Dense graph | O(V^2) | O(V^2 log V) |

Uses a binary min-heap (Python's heapq) for the priority queue.

---

## Limitations

- Does **not** work with negative edge weights — use Bellman-Ford instead
- Built for undirected graphs — for directed graphs remove the reverse edge in `add_edge`

---

## Built with

- Python 3
- [NetworkX](https://networkx.org/)
- [Matplotlib](https://matplotlib.org/)

---

**Ankur Animesh & Carl Jarving — Halmstad University, Sweden**
