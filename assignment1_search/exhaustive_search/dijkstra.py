import heapq


def dijkstra(graph, source):
    distances = {node: float('inf') for node in graph}
    distances[source] = 0
    predecessors = {node: None for node in graph}
    pq = [(0, source)]
    visited = set()

    while pq:
        dist, u = heapq.heappop(pq)

        if u in visited:
            continue
        visited.add(u)

        for v, weight in graph[u].items():
            new_dist = dist + weight
            if new_dist < distances[v]:
                distances[v] = new_dist
                predecessors[v] = u
                heapq.heappush(pq, (new_dist, v))

    return distances, predecessors


def reconstruct_path(predecessors, target):
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = predecessors[current]
    return list(reversed(path))


def main():
    print("=" * 50)
    print("DIJKSTRA'S ALGORITHM")
    print("=" * 50)

    graph = {
        'A': {'B': 4, 'C': 1},
        'B': {'A': 4, 'C': 2, 'D': 5},
        'C': {'A': 1, 'B': 2, 'D': 8, 'E': 10},
        'D': {'B': 5, 'C': 8, 'E': 2, 'F': 6},
        'E': {'C': 10, 'D': 2, 'F': 3},
        'F': {'D': 6, 'E': 3},
    }

    print("\nGraph (adjacency list):")
    for node in sorted(graph.keys()):
        edges = ", ".join(f"{v}({w})" for v, w in graph[node].items())
        print(f"  {node}: {edges}")

    source = 'A'
    distances, predecessors = dijkstra(graph, source)

    print(f"\nShortest distances from '{source}':")
    for node in sorted(distances.keys()):
        path = reconstruct_path(predecessors, node)
        path_str = " -> ".join(path)
        print(f"  {source} -> {node}: distance = {distances[node]}, path = {path_str}")

    # second example - larger graph
    print("\n" + "=" * 50)
    print("SECOND EXAMPLE - LARGER GRAPH")
    print("=" * 50)

    graph2 = {
        '0': {'1': 7, '2': 9, '5': 14},
        '1': {'0': 7, '2': 10, '3': 15},
        '2': {'0': 9, '1': 10, '3': 11, '5': 2},
        '3': {'1': 15, '2': 11, '4': 6},
        '4': {'3': 6, '5': 9},
        '5': {'0': 14, '2': 2, '4': 9},
    }

    distances2, predecessors2 = dijkstra(graph2, '0')
    print(f"\nShortest distances from '0':")
    for node in sorted(distances2.keys()):
        path = reconstruct_path(predecessors2, node)
        path_str = " -> ".join(path)
        print(f"  0 -> {node}: distance = {distances2[node]}, path = {path_str}")

    print("\n" + "=" * 50)
    print("HOW DIJKSTRA COMBINES GREEDY AND DYNAMIC PROGRAMMING")
    print("=" * 50)
    print("""
GREEDY aspect:
  At each step, Dijkstra picks the unvisited node with the smallest
  known distance. This is the greedy choice - we commit to the fact
  that this node's shortest path has been found.

DYNAMIC PROGRAMMING aspect:
  The algorithm builds optimal solutions from smaller subproblems.
  The shortest path to node v through node u is:
    dist(v) = dist(u) + weight(u, v)
  This is the optimal substructure property. We reuse previously
  computed shortest distances to compute new ones.

  The relaxation step (updating distances) is essentially the
  Bellman equation: d[v] = min(d[v], d[u] + w(u,v))

Why it works:
  Because all edge weights are non-negative, once we process a node
  (extract it from the priority queue), its distance is guaranteed
  to be optimal. No future path through unvisited nodes can be shorter.
""")


if __name__ == "__main__":
    main()
