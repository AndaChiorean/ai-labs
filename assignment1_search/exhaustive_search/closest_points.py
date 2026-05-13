import random
import math
import time
import matplotlib.pyplot as plt


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def brute_force_closest(points):
    n = len(points)
    min_dist = float('inf')
    closest = None
    for i in range(n):
        for j in range(i + 1, n):
            d = distance(points[i], points[j])
            if d < min_dist:
                min_dist = d
                closest = (points[i], points[j])
    return min_dist, closest


def strip_closest(strip, d):
    min_dist = d
    closest = None
    strip.sort(key=lambda p: p[1])

    for i in range(len(strip)):
        j = i + 1
        while j < len(strip) and (strip[j][1] - strip[i][1]) < min_dist:
            dist = distance(strip[i], strip[j])
            if dist < min_dist:
                min_dist = dist
                closest = (strip[i], strip[j])
            j += 1

    return min_dist, closest


def closest_rec(points_sorted_x):
    n = len(points_sorted_x)
    if n <= 3:
        return brute_force_closest(points_sorted_x)

    mid = n // 2
    mid_point = points_sorted_x[mid]

    left = points_sorted_x[:mid]
    right = points_sorted_x[mid:]

    dl, cl = closest_rec(left)
    dr, cr = closest_rec(right)

    if dl < dr:
        d = dl
        closest = cl
    else:
        d = dr
        closest = cr

    strip = [p for p in points_sorted_x if abs(p[0] - mid_point[0]) < d]

    ds, cs = strip_closest(strip, d)
    if cs is not None and ds < d:
        return ds, cs
    return d, closest


def divide_and_conquer_closest(points):
    sorted_points = sorted(points, key=lambda p: p[0])
    return closest_rec(sorted_points)


def generate_points(n):
    return [(random.uniform(0, 10000), random.uniform(0, 10000)) for _ in range(n)]


def main():
    random.seed(42)

    # test correctness
    print("=== Correctness Test ===")
    test_points = generate_points(100)
    bf_dist, bf_pair = brute_force_closest(test_points)
    dc_dist, dc_pair = divide_and_conquer_closest(test_points)
    print(f"Brute force: distance = {bf_dist:.6f}, points = {bf_pair}")
    print(f"Divide & Conquer: distance = {dc_dist:.6f}, points = {dc_pair}")
    print(f"Results match: {abs(bf_dist - dc_dist) < 1e-9}")

    # timing comparison
    print("\n=== Timing Comparison ===")
    sizes = [100, 500, 1000, 2000, 5000, 10000, 20000]
    bf_times = []
    dc_times = []

    for n in sizes:
        points = generate_points(n)

        if n <= 10000:
            start = time.time()
            brute_force_closest(points)
            bf_time = time.time() - start
        else:
            bf_time = None
        bf_times.append(bf_time)

        start = time.time()
        divide_and_conquer_closest(points)
        dc_time = time.time() - start
        dc_times.append(dc_time)

        bf_str = f"{bf_time:.4f}s" if bf_time is not None else "skipped"
        print(f"n = {n:>6}: BF = {bf_str}, D&C = {dc_time:.4f}s")

    # plot
    plt.figure(figsize=(10, 6))

    bf_x = [s for s, t in zip(sizes, bf_times) if t is not None]
    bf_y = [t for t in bf_times if t is not None]
    plt.plot(bf_x, bf_y, 'ro-', label='Brute Force O(n²)')
    plt.plot(sizes, dc_times, 'bs-', label='Divide & Conquer O(n log n)')

    plt.xlabel('Number of Points')
    plt.ylabel('Time (seconds)')
    plt.title('Closest Points - Brute Force vs Divide & Conquer')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('closest_points_comparison.png', dpi=100)
    plt.show()

    print("\n=== Complexity Analysis ===")
    print("Brute Force: O(n^2) - checks all pairs")
    print("Divide & Conquer: O(n log n) - splits points by x-coordinate,")
    print("  recurse on each half, then check strip of width 2d around midline.")
    print("  Strip check is O(n) because each point only needs to compare")
    print("  with at most 7 others (geometric argument).")


if __name__ == "__main__":
    main()
