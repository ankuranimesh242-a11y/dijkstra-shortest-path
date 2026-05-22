# ============================================================
# Dijkstra's Algorithm - Shortest Path Finder
# MA4030 Discrete Mathematics - Project Assignment 4
# Group 5: Ankur Animesh & Carl Jarving
# Halmstad University, VT26
# ============================================================

import itertools  # to generate those tiebreaker numbers , because if 2 nodes have the same value (distance) then we need to chose either one of them , hence the code doesn't break or get confused 
from heapq import heappush, heappop # from heapq import heappush, heappop : heapq is Python's built-in heap module. We import two functions from it:
                                                                            # heappush — adds an item to the heap and keeps it sorted (smallest on top)
                                                                            # heappop — removes and returns the smallest item            


# ============================================================
# PRIORITY QUEUE
# ============================================================
# We are not using heapq directly because that would need a lot more
# explanation first, so instead we used this from Python's official docs [4].
# It basically works as a priority queue using a heap internally,
# we just put it in a class and adjusted it a bit to fit our needs.
# The whole point is that it always gives us the node with the smallest
# distance when we pop, which is exactly what Dijkstra needs.

class PriorityQueue:

    def __init__(self):                    # We use self to create a variable, also called an attribute, inside the function so that it is stored in the whole class object and is not lost when the function finishes running. This makes the variable permanent for that object.
        self.pq = []                       # the actual heap list
        self.entry_finder = {}             # maps each task to its entry so we can find it
        self.counter = itertools.count()   # tie-breaker when two nodes have the same cost

    def __len__(self):
        return len(self.pq)               # so "while queue:" works

    def add(self, priority, task):
        if task in self.entry_finder:
            entry = self.entry_finder[task]
            count = next(self.counter)
            entry[0], entry[1] = priority, count
            return
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heappush(self.pq, entry)

    def pop(self):
        while self.pq:
            priority, count, task = heappop(self.pq)
            del self.entry_finder[task]
            return priority, task


# ============================================================
# EDGE AND GRAPH
# ============================================================

class Edge:
    def __init__(self, distance, vertex):    # we write self because we want this function or the attributes inside this function to stay even when the class is done running
        self.distance = distance   # weight of this edge
        self.vertex = vertex       # the ONE node this edge leads to
                                   # NOT a list. if a node connects to 3 others, it has 3 separate Edge objects in its list. 

class Graph:
    def __init__(self):
        self.adjacency_list = {}   # holds all vertices and their edges
                                   # we use self so it stays alive in the object

    def add_vertex(self, vertex):    
        self.adjacency_list[vertex] = []    # we add it as a new key in the dictionary with an empty list as its value the empty list will later be filled with Edge objects when we call add_edge 
                                            # self.adjacency_list["A"] = []   ← THIS created A's list
    def add_edge(self, v1, v2, distance):
        # Example: g.add_edge("A", "B", 3) does TWO things:
        #   1. creates Edge(3, "B") and adds it to A's list
        #   2. creates Edge(3, "A") and adds it to B's list
        # we do both because the graph is undirected (A->B means B->A too)
        self.adjacency_list[v1].append(Edge(distance, v2))
        self.adjacency_list[v2].append(Edge(distance, v1))       


# ============================================================
# DIJKSTRA'S ALGORITHM
# ============================================================
# These are new dictionaries created to store information about each vertex, such as whether it was visited, its previous node, and its current shortest distance. 
# We use graph.adjacency_list.keys() so Python automatically gets all the vertices already present in the graph instead of us manually writing every vertex ourselves.

def dijkstra(graph, start):
    distances = {v: float("inf") for v in graph.adjacency_list}   # {key : value for item in iterable}
    previous  = {v: None        for v in graph.adjacency_list}    
    visited   = {v: False       for v in graph.adjacency_list}    # for every node in the graph, create an entry in visited and set it initially to False  

    distances[start] = 0          # set the distance of the starting vertex to be 0 
    queue = PriorityQueue()
    queue.add(0, start)
    visit_order = []                # records the order nodes get visited, used by the animation only

# create a piority queue and add the start vertex and its distance 

    while queue:                        # multiple assignment / unpacking : queue.pop removes two values at once : removed_distance = 3 removed = "B" 
                                        # Because Python allows unpacking multiple returned values. Example: a, b = (10, 20). Remove the node with the smallest distance from the priority queue, 
                                        # then store its distance and node separately into two variables.   
        cost_u, u = queue.pop()         # Pop from the queue, saving the vertex and its distance
        if visited[u]:
            continue
        visited[u] = True               # Mark the removed vertex as visited
        visit_order.append(u)

        for edge in graph.adjacency_list[u]:        # Start a loop over all the neighbors of the removed vertex
            if visited[edge.vertex]:                   # If the current vertex is visited, skip to the next
                continue
            new_dist = cost_u + edge.distance        # Cost(v) = Cost(u) + Dist(u->v) otherwise, calculate the distance to it
            if new_dist < distances[edge.vertex]:       # If the new distance is smaller
                distances[edge.vertex] = new_dist       # Update distances table
                previous[edge.vertex] = u               # Update previous table - I arrived at this vertex through u.
                queue.add(new_dist, edge.vertex)        # Push into the queue the neighbor and its distance

    return distances, previous, visit_order


def shortest_path(previous, start, end):  # exlain to me how this function works 
    path = []                               # first we initialize a variable called path then me make an empty list 
    node = end                              # node = a vertex. we start at the END 
    while node is not None:                    # while loop till we have nothing in node , right now we just have the last node in it 
        path.append(node)                       # in path list add the last node 
        node = previous[node]                   # then the value of node is updated to the value stored in previous , look up F in the previous dict, it says E 
    path.reverse()                              # flip it
    return path if (path and path[0] == start) else []   # This just checks two things: (1) is the path not empty, and (2) does it actually start at our source vertex? 
                                                            # If both are true, return the path. If not, return an empty list meaning "no path exists." It's a safety check in case the destination wasn't reachable from the start.


# ============================================================
# MAIN
# ============================================================
# if __name__ == "__main__" means:
#   only run this code if the file is run directly.
#   if someone imports this file, the code below will NOT run.

if __name__ == "__main__":

    # The graph from the our notes:
    #         D
    #        / \
    #   A---B   F
    #    \ / \ /
    #     C---E

# STEP 1: Create empty graph
    g = Graph()                                 # creates an empty adjacency_list = {}
    for v in ["A", "B", "C", "D", "E", "F"]:
        # STEP 2: Add vertices
        g.add_vertex(v)                         # g.adjacency_list["A"] = []. It adds "A" as a key with an empty list. # adjacency_list = {"A": [], "B": []} and so on 
# STEP 3: Add edges (this FILLS the lists)
    g.add_edge("A", "B", 3)      
    g.add_edge("A", "C", 6)
    g.add_edge("A", "D", 4)
    g.add_edge("B", "C", 2)
    g.add_edge("B", "E", 3)
    g.add_edge("C", "E", 3)
    g.add_edge("C", "F", 3)
    g.add_edge("D", "F", 6)
    g.add_edge("E", "F", 1)

    source      = "A"
    destination = "F"

    dist, prev, order = dijkstra(g, source)   # unpacking : The dijkstra function returns THREE things at the end (return distances, previous, visit_order), so we catch all three in one line:
                                              # dist catches distances — the dictionary with shortest distance to every vertex
                                              # prev catches previous — the dictionary with "who did I come from" for every vertex
                                              # order catches visit_order — the list of which vertex was visited in what order (for animation) - optional, not necessary

    path = shortest_path(prev, source, destination)

   # The print statements below just display it nicely.
    print("=" * 40)
    print(f"  Dijkstra  |  {source} -> {destination}")
    print("=" * 40)
    if path:
        print(f"Path     : {' -> '.join(path)}")
        print(f"Distance : {dist[destination]}")
    else:
        print(f"No path from {source} to {destination}")
    print(f"\n{'Vertex':<8} {'Distance':<10} {'Previous':<8}")
    print("-" * 26)
    for v in sorted(dist):
        d = dist[v] if dist[v] != float("inf") else "inf"
        print(f"{v:<8} {str(d):<10} {prev[v] or '-':<8}")

    # Animation is in a separate file to keep things clean
    from animate import animate
    animate(g, dist, prev, source, destination, order)
