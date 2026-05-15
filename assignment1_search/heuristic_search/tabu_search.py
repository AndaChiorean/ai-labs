import random
import time
from tsp_utils import load_berlin52, tour_distance, two_opt_swap, nearest_neighbor_tour, plot_tour


def tabu_search(coords, max_iterations=10000, tabu_tenure=10, seed=None):
    if seed is not None:
        random.seed(seed)

    n = len(coords)
    current_tour = nearest_neighbor_tour(coords)
    current_dist = tour_distance(current_tour, coords)

    best_tour = current_tour[:]
    best_dist = current_dist

    tabu_list = []
    history = [best_dist]

    for iteration in range(max_iterations):
        best_neighbor = None
        best_neighbor_dist = float('inf')
        best_move = None

        # check all 2-opt neighbors
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                move = (i, j)

                neighbor = two_opt_swap(current_tour, i, j)
                neighbor_dist = tour_distance(neighbor, coords)

                # accept if not tabu, or if it beats global best (aspiration)
                is_tabu = move in tabu_list or (j, i) in tabu_list
                aspiration = neighbor_dist < best_dist

                if (not is_tabu or aspiration) and neighbor_dist < best_neighbor_dist:
                    best_neighbor = neighbor
                    best_neighbor_dist = neighbor_dist
                    best_move = move

        if best_neighbor is None:
            break

        current_tour = best_neighbor
        current_dist = best_neighbor_dist

        tabu_list.append(best_move)
        if len(tabu_list) > tabu_tenure:
            tabu_list.pop(0)

        if current_dist < best_dist:
            best_tour = current_tour[:]
            best_dist = current_dist

        history.append(best_dist)

        if iteration % 1000 == 0:
            print(f"  Iteration {iteration}: best = {best_dist:.2f}")

    return best_tour, best_dist, history


def main():
    coords = load_berlin52()
    print(f"Loaded {len(coords)} cities")
    print(f"Known optimal: 7542\n")

    print("Running Tabu Search...")
    start = time.time()
    tour, dist, history = tabu_search(coords, max_iterations=5000, tabu_tenure=10, seed=42)
    elapsed = time.time() - start

    print(f"\nBest distance: {dist:.2f}")
    print(f"Gap from optimal: {(dist / 7542 - 1) * 100:.1f}%")
    print(f"Time: {elapsed:.2f}s")

    # test different tabu tenures
    print("\n=== Hyperparameter analysis: Tabu Tenure ===")
    for tenure in [5, 10, 15, 20, 30]:
        tour_t, dist_t, _ = tabu_search(coords, max_iterations=3000, tabu_tenure=tenure, seed=42)
        print(f"  Tenure = {tenure:>3}: distance = {dist_t:.2f}")

    plot_tour(tour, coords, "Tabu Search - berlin52", "tabu_search_tour.png")
    print("\nTour plot saved to tabu_search_tour.png")


if __name__ == "__main__":
    main()
