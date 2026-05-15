import math
import matplotlib.pyplot as plt
import os


def load_berlin52(filepath=None):
    if filepath is None:
        filepath = os.path.join(os.path.dirname(__file__), "berlin52.tsp")

    coords = []
    reading = False
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line == "NODE_COORD_SECTION":
                reading = True
                continue
            if line == "EOF":
                break
            if reading:
                parts = line.split()
                coords.append((float(parts[1]), float(parts[2])))
    return coords


def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def tour_distance(tour, coords):
    total = 0
    n = len(tour)
    for i in range(n):
        total += euclidean_distance(coords[tour[i]], coords[tour[(i + 1) % n]])
    return total


def two_opt_swap(tour, i, j):
    new_tour = tour[:i] + tour[i:j+1][::-1] + tour[j+1:]
    return new_tour


def nearest_neighbor_tour(coords):
    n = len(coords)
    visited = [False] * n
    tour = [0]
    visited[0] = True

    for _ in range(n - 1):
        last = tour[-1]
        best_dist = float('inf')
        best_city = -1
        for city in range(n):
            if not visited[city]:
                d = euclidean_distance(coords[last], coords[city])
                if d < best_dist:
                    best_dist = d
                    best_city = city
        tour.append(best_city)
        visited[best_city] = True

    return tour


def plot_tour(tour, coords, title="TSP Tour", filename=None):
    fig, ax = plt.subplots(figsize=(10, 8))

    x = [coords[tour[i]][0] for i in range(len(tour))]
    y = [coords[tour[i]][1] for i in range(len(tour))]
    x.append(x[0])
    y.append(y[0])

    ax.plot(x, y, 'b-', linewidth=0.8)
    ax.plot([coords[c][0] for c in tour], [coords[c][1] for c in tour], 'ro', markersize=4)

    dist = tour_distance(tour, coords)
    ax.set_title(f"{title}\nDistance: {dist:.2f}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, alpha=0.3)

    if filename:
        plt.savefig(filename, dpi=100, bbox_inches='tight')
    plt.close()
    return fig


if __name__ == "__main__":
    coords = load_berlin52()
    print(f"Loaded {len(coords)} cities")

    nn_tour = nearest_neighbor_tour(coords)
    nn_dist = tour_distance(nn_tour, coords)
    print(f"Nearest neighbor tour distance: {nn_dist:.2f}")
    print(f"Known optimal: 7542")
    print(f"Gap: {(nn_dist / 7542 - 1) * 100:.1f}%")
