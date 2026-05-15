import random
import time
from tsp_utils import load_berlin52, tour_distance, two_opt_swap, nearest_neighbor_tour, plot_tour


def hill_climbing_2opt(coords, max_iterations=50000, seed=None):
    if seed is not None:
        random.seed(seed)

    n = len(coords)
    current_tour = nearest_neighbor_tour(coords)
    current_dist = tour_distance(current_tour, coords)

    best_tour = current_tour[:]
    best_dist = current_dist
    history = [best_dist]
    stuck_count = 0

    for iteration in range(max_iterations):
        improved = False

        # try all 2-opt swaps, take the first improvement
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                neighbor = two_opt_swap(current_tour, i, j)
                neighbor_dist = tour_distance(neighbor, coords)

                if neighbor_dist < current_dist:
                    current_tour = neighbor
                    current_dist = neighbor_dist
                    improved = True
                    break
            if improved:
                break

        if current_dist < best_dist:
            best_tour = current_tour[:]
            best_dist = current_dist

        history.append(best_dist)

        if not improved:
            stuck_count += 1
            if stuck_count >= 5:
                break
        else:
            stuck_count = 0

    return best_tour, best_dist, history


def hill_climbing_random_restart(coords, restarts=10, max_iterations=50000, seed=None):
    if seed is not None:
        random.seed(seed)

    best_tour = None
    best_dist = float('inf')
    all_histories = []

    for r in range(restarts):
        n = len(coords)
        tour = list(range(n))
        random.shuffle(tour)

        current_tour = tour
        current_dist = tour_distance(current_tour, coords)
        history = [current_dist]

        for iteration in range(max_iterations):
            improved = False
            for i in range(1, n - 1):
                for j in range(i + 1, n):
                    neighbor = two_opt_swap(current_tour, i, j)
                    neighbor_dist = tour_distance(neighbor, coords)
                    if neighbor_dist < current_dist:
                        current_tour = neighbor
                        current_dist = neighbor_dist
                        improved = True
                        break
                if improved:
                    break
            history.append(current_dist)
            if not improved:
                break

        if current_dist < best_dist:
            best_tour = current_tour[:]
            best_dist = current_dist
        all_histories.append(history)

    return best_tour, best_dist, all_histories


def main():
    coords = load_berlin52()
    print(f"Loaded {len(coords)} cities")
    print(f"Known optimal: 7542\n")

    # basic hill climbing
    print("=== Hill Climbing (2-opt, first improvement) ===")
    start = time.time()
    tour, dist, history = hill_climbing_2opt(coords, seed=42)
    elapsed = time.time() - start
    print(f"Best distance: {dist:.2f}")
    print(f"Gap from optimal: {(dist / 7542 - 1) * 100:.1f}%")
    print(f"Iterations: {len(history)}")
    print(f"Time: {elapsed:.2f}s")

    # hill climbing with random restarts
    print("\n=== Hill Climbing with Random Restarts (10 restarts) ===")
    start = time.time()
    tour_r, dist_r, histories = hill_climbing_random_restart(coords, restarts=10, seed=42)
    elapsed = time.time() - start
    all_final = [h[-1] for h in histories]
    print(f"Best across restarts: {dist_r:.2f}")
    print(f"Average: {sum(all_final)/len(all_final):.2f}")
    print(f"Worst: {max(all_final):.2f}")
    print(f"Gap from optimal: {(dist_r / 7542 - 1) * 100:.1f}%")
    print(f"Time: {elapsed:.2f}s")

    print("\n=== Why Hill Climbing Gets Stuck ===")
    print("Pure 2-opt hill climbing only accepts improvements.")
    print("Once it reaches a local optimum, it cannot escape.")
    print("This is why we need metaheuristics:")
    print("  - Tabu Search: uses memory to avoid revisiting solutions")
    print("  - Simulated Annealing: accepts worse solutions probabilistically")
    print("  - Genetic Algorithms: maintain population diversity")
    print("Even with random restarts, hill climbing typically finds")
    print("worse solutions than these more sophisticated methods.")

    plot_tour(tour, coords, "Hill Climbing (2-opt) - berlin52", "hill_climbing_tour.png")
    print("\nTour plot saved to hill_climbing_tour.png")


if __name__ == "__main__":
    main()
