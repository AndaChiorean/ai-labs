import time
import random
import numpy as np
import matplotlib.pyplot as plt
from tsp_utils import load_berlin52, tour_distance, nearest_neighbor_tour
from tabu_search import tabu_search
from simulated_annealing import simulated_annealing
from genetic_algorithm import genetic_algorithm


OPTIMAL = 7542
NUM_RUNS = 10


def run_benchmark(coords):
    results = {
        "Tabu Search": {"distances": [], "times": [], "histories": []},
        "Simulated Annealing": {"distances": [], "times": [], "histories": []},
        "Genetic Algorithm": {"distances": [], "times": [], "histories": []},
    }

    nn_tour = nearest_neighbor_tour(coords)
    nn_dist = tour_distance(nn_tour, coords)
    print(f"Nearest Neighbor baseline: {nn_dist:.2f}")
    print(f"Known optimal: {OPTIMAL}")
    print(f"\nRunning {NUM_RUNS} runs for each algorithm...\n")

    for run in range(NUM_RUNS):
        seed = run * 17 + 3

        # Tabu Search
        start = time.time()
        _, dist, history = tabu_search(coords, max_iterations=3000, tabu_tenure=10, seed=seed)
        elapsed = time.time() - start
        results["Tabu Search"]["distances"].append(dist)
        results["Tabu Search"]["times"].append(elapsed)
        results["Tabu Search"]["histories"].append(history)

        # Simulated Annealing
        start = time.time()
        _, dist, history, _ = simulated_annealing(coords, T0=10000, alpha=0.9995, max_iterations=100000, seed=seed)
        elapsed = time.time() - start
        results["Simulated Annealing"]["distances"].append(dist)
        results["Simulated Annealing"]["times"].append(elapsed)
        results["Simulated Annealing"]["histories"].append(history)

        # Genetic Algorithm
        start = time.time()
        _, dist, history = genetic_algorithm(coords, pop_size=200, generations=500, mutation_rate=0.02, seed=seed)
        elapsed = time.time() - start
        results["Genetic Algorithm"]["distances"].append(dist)
        results["Genetic Algorithm"]["times"].append(elapsed)
        results["Genetic Algorithm"]["histories"].append(history)

        print(f"Run {run+1}/{NUM_RUNS} done")

    return results


def print_results_table(results):
    print("\n" + "=" * 80)
    print("BENCHMARK RESULTS")
    print("=" * 80)
    print(f"{'Algorithm':<25} {'Best':>8} {'Avg':>8} {'Worst':>8} {'Std':>8} {'Avg Time':>10} {'Gap%':>8}")
    print("-" * 80)

    for name, data in results.items():
        dists = data["distances"]
        times = data["times"]
        best = min(dists)
        avg = np.mean(dists)
        worst = max(dists)
        std = np.std(dists)
        avg_time = np.mean(times)
        gap = (best / OPTIMAL - 1) * 100
        print(f"{name:<25} {best:>8.1f} {avg:>8.1f} {worst:>8.1f} {std:>8.1f} {avg_time:>9.2f}s {gap:>7.1f}%")


def plot_convergence(results):
    fig, ax = plt.subplots(figsize=(12, 7))
    colors = {'Tabu Search': 'red', 'Simulated Annealing': 'blue', 'Genetic Algorithm': 'green'}

    for name, data in results.items():
        # use the best run's history
        best_run = np.argmin(data["distances"])
        history = data["histories"][best_run]
        ax.plot(range(len(history)), history, label=name, color=colors[name], alpha=0.8)

    ax.axhline(y=OPTIMAL, color='black', linestyle='--', label=f'Optimal ({OPTIMAL})', alpha=0.5)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Best Distance')
    ax.set_title('Convergence Comparison (Best Run)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('convergence_comparison.png', dpi=100)
    plt.close()


def plot_boxplot(results):
    fig, ax = plt.subplots(figsize=(10, 6))
    data = [results[name]["distances"] for name in results]
    labels = list(results.keys())

    bp = ax.boxplot(data, labels=labels, patch_artist=True)
    colors = ['#ff6b6b', '#4dabf7', '#51cf66']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)

    ax.axhline(y=OPTIMAL, color='black', linestyle='--', label=f'Optimal ({OPTIMAL})', alpha=0.5)
    ax.set_ylabel('Tour Distance')
    ax.set_title(f'Distribution of Results ({NUM_RUNS} runs)')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('boxplot_comparison.png', dpi=100)
    plt.close()


def plot_bar_chart(results):
    fig, ax = plt.subplots(figsize=(10, 6))
    names = list(results.keys())
    avgs = [np.mean(results[n]["distances"]) for n in names]
    stds = [np.std(results[n]["distances"]) for n in names]
    colors = ['#ff6b6b', '#4dabf7', '#51cf66']

    bars = ax.bar(names, avgs, yerr=stds, capsize=10, color=colors, alpha=0.7, edgecolor='black')
    ax.axhline(y=OPTIMAL, color='black', linestyle='--', label=f'Optimal ({OPTIMAL})', alpha=0.5)

    for bar, avg in zip(bars, avgs):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
                f'{avg:.0f}', ha='center', va='bottom', fontsize=11)

    ax.set_ylabel('Average Tour Distance')
    ax.set_title(f'Average Performance Comparison ({NUM_RUNS} runs)')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('bar_comparison.png', dpi=100)
    plt.close()


def main():
    coords = load_berlin52()
    print(f"Berlin52 TSP Benchmark")
    print(f"Cities: {len(coords)}")
    print(f"Runs per algorithm: {NUM_RUNS}\n")

    results = run_benchmark(coords)
    print_results_table(results)

    plot_convergence(results)
    plot_boxplot(results)
    plot_bar_chart(results)

    print("\nPlots saved:")
    print("  - convergence_comparison.png")
    print("  - boxplot_comparison.png")
    print("  - bar_comparison.png")

    print("\n" + "=" * 80)
    print("ANALYSIS")
    print("=" * 80)
    print("""
Tabu Search:
  - Deterministic neighborhood exploration (all 2-opt swaps each iteration)
  - Uses memory (tabu list) to avoid revisiting recent solutions
  - Good at escaping local optima through the tabu mechanism
  - Slower per iteration due to exhaustive neighborhood search

Simulated Annealing:
  - Stochastic - samples one random neighbor per iteration
  - Accepts worse solutions with decreasing probability (temperature)
  - Fast per iteration, but needs many iterations
  - Very sensitive to cooling schedule (alpha parameter)

Genetic Algorithm:
  - Population-based - maintains diversity
  - Order crossover preserves relative city ordering
  - Mutation prevents premature convergence
  - More parameters to tune (pop size, mutation rate, tournament size)
  - Good balance between exploration and exploitation

General observations:
  - SA and GA tend to find better solutions than Tabu Search on berlin52
  - Tabu Search is more consistent (lower variance) but often gets stuck
  - GA benefits from population diversity and crossover
  - All methods significantly improve over the nearest neighbor heuristic
""")


if __name__ == "__main__":
    main()
