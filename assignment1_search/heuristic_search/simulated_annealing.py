import random
import math
import time
from tsp_utils import load_berlin52, tour_distance, two_opt_swap, nearest_neighbor_tour, plot_tour


def simulated_annealing(coords, T0=10000, alpha=0.9995, max_iterations=100000, seed=None):
    if seed is not None:
        random.seed(seed)

    n = len(coords)
    current_tour = nearest_neighbor_tour(coords)
    current_dist = tour_distance(current_tour, coords)

    best_tour = current_tour[:]
    best_dist = current_dist

    T = T0
    history = [best_dist]
    temp_history = [T]

    for iteration in range(max_iterations):
        # random 2-opt swap
        i = random.randint(1, n - 2)
        j = random.randint(i + 1, n - 1)

        neighbor = two_opt_swap(current_tour, i, j)
        neighbor_dist = tour_distance(neighbor, coords)

        delta = neighbor_dist - current_dist

        if delta < 0 or random.random() < math.exp(-delta / T):
            current_tour = neighbor
            current_dist = neighbor_dist

            if current_dist < best_dist:
                best_tour = current_tour[:]
                best_dist = current_dist

        T = T * alpha
        history.append(best_dist)
        temp_history.append(T)

        if T < 0.01:
            break

        if iteration % 10000 == 0:
            print(f"  Iteration {iteration}: T = {T:.2f}, best = {best_dist:.2f}, current = {current_dist:.2f}")

    return best_tour, best_dist, history, temp_history


def main():
    coords = load_berlin52()
    print(f"Loaded {len(coords)} cities")
    print(f"Known optimal: 7542\n")

    print("Running Simulated Annealing...")
    start = time.time()
    tour, dist, history, temp_history = simulated_annealing(
        coords, T0=10000, alpha=0.9995, max_iterations=100000, seed=42
    )
    elapsed = time.time() - start

    print(f"\nBest distance: {dist:.2f}")
    print(f"Gap from optimal: {(dist / 7542 - 1) * 100:.1f}%")
    print(f"Time: {elapsed:.2f}s")

    # test different cooling rates
    print("\n=== Hyperparameter analysis: Cooling Rate (alpha) ===")
    for alpha in [0.999, 0.9995, 0.9999, 0.99995]:
        _, dist_a, _, _ = simulated_annealing(
            coords, T0=10000, alpha=alpha, max_iterations=200000, seed=42
        )
        print(f"  alpha = {alpha}: distance = {dist_a:.2f}")

    # test different initial temperatures
    print("\n=== Hyperparameter analysis: Initial Temperature ===")
    for T0 in [100, 1000, 5000, 10000, 50000]:
        _, dist_t, _, _ = simulated_annealing(
            coords, T0=T0, alpha=0.9995, max_iterations=100000, seed=42
        )
        print(f"  T0 = {T0:>6}: distance = {dist_t:.2f}")

    plot_tour(tour, coords, "Simulated Annealing - berlin52", "sa_tour.png")
    print("\nTour plot saved to sa_tour.png")


if __name__ == "__main__":
    main()
