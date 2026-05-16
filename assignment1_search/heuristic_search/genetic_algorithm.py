import random
import time
from tsp_utils import load_berlin52, tour_distance, nearest_neighbor_tour, plot_tour


def create_population(n_cities, pop_size, coords):
    population = []
    # add nearest neighbor as one individual
    nn = nearest_neighbor_tour(coords)
    population.append(nn)

    for _ in range(pop_size - 1):
        tour = list(range(n_cities))
        random.shuffle(tour)
        population.append(tour)

    return population


def fitness(tour, coords):
    return 1.0 / tour_distance(tour, coords)


def tournament_selection(population, fitnesses, k=5):
    indices = random.sample(range(len(population)), k)
    best_idx = max(indices, key=lambda i: fitnesses[i])
    return population[best_idx][:]


def order_crossover(parent1, parent2):
    n = len(parent1)
    start = random.randint(0, n - 2)
    end = random.randint(start + 1, n - 1)

    child = [-1] * n
    child[start:end+1] = parent1[start:end+1]

    used = set(child[start:end+1])
    pos = (end + 1) % n
    for i in range(n):
        gene = parent2[(end + 1 + i) % n]
        if gene not in used:
            child[pos] = gene
            pos = (pos + 1) % n

    return child


def swap_mutation(tour, mutation_rate=0.02):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(tour)), 2)
        tour[i], tour[j] = tour[j], tour[i]
    return tour


def genetic_algorithm(coords, pop_size=200, generations=1000, mutation_rate=0.02,
                      tournament_k=5, elitism=2, seed=None):
    if seed is not None:
        random.seed(seed)

    n_cities = len(coords)
    population = create_population(n_cities, pop_size, coords)

    best_tour = None
    best_dist = float('inf')
    history = []

    for gen in range(generations):
        fitnesses = [fitness(tour, coords) for tour in population]
        distances = [tour_distance(tour, coords) for tour in population]

        # update best
        gen_best_idx = min(range(len(distances)), key=lambda i: distances[i])
        if distances[gen_best_idx] < best_dist:
            best_dist = distances[gen_best_idx]
            best_tour = population[gen_best_idx][:]

        history.append(best_dist)

        # elitism
        sorted_indices = sorted(range(len(distances)), key=lambda i: distances[i])
        new_population = [population[i][:] for i in sorted_indices[:elitism]]

        # create rest of new population
        while len(new_population) < pop_size:
            parent1 = tournament_selection(population, fitnesses, tournament_k)
            parent2 = tournament_selection(population, fitnesses, tournament_k)
            child = order_crossover(parent1, parent2)
            child = swap_mutation(child, mutation_rate)
            new_population.append(child)

        population = new_population

        if gen % 100 == 0:
            avg_dist = sum(distances) / len(distances)
            print(f"  Gen {gen:>4}: best = {best_dist:.2f}, avg = {avg_dist:.2f}")

    return best_tour, best_dist, history


def main():
    coords = load_berlin52()
    print(f"Loaded {len(coords)} cities")
    print(f"Known optimal: 7542\n")

    print("Running Genetic Algorithm...")
    start = time.time()
    tour, dist, history = genetic_algorithm(
        coords, pop_size=200, generations=1000, mutation_rate=0.02, seed=42
    )
    elapsed = time.time() - start

    print(f"\nBest distance: {dist:.2f}")
    print(f"Gap from optimal: {(dist / 7542 - 1) * 100:.1f}%")
    print(f"Time: {elapsed:.2f}s")

    # hyperparameter analysis
    print("\n=== Hyperparameter analysis: Population Size ===")
    for pop in [50, 100, 200, 500]:
        _, dist_p, _ = genetic_algorithm(coords, pop_size=pop, generations=500, seed=42)
        print(f"  Pop size = {pop:>4}: distance = {dist_p:.2f}")

    print("\n=== Hyperparameter analysis: Mutation Rate ===")
    for mr in [0.005, 0.01, 0.02, 0.05, 0.1]:
        _, dist_m, _ = genetic_algorithm(coords, pop_size=200, generations=500, mutation_rate=mr, seed=42)
        print(f"  Mutation rate = {mr:.3f}: distance = {dist_m:.2f}")

    print("\n=== Hyperparameter analysis: Tournament Size ===")
    for k in [2, 3, 5, 10]:
        _, dist_k, _ = genetic_algorithm(coords, pop_size=200, generations=500, tournament_k=k, seed=42)
        print(f"  Tournament k = {k:>2}: distance = {dist_k:.2f}")

    plot_tour(tour, coords, "Genetic Algorithm - berlin52", "ga_tour.png")
    print("\nTour plot saved to ga_tour.png")


if __name__ == "__main__":
    main()
