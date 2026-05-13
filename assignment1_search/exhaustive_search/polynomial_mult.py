import cmath
import time
import random
import matplotlib.pyplot as plt


def brute_force_multiply(A, B):
    n = len(A)
    m = len(B)
    result = [0] * (n + m - 1)
    for i in range(n):
        for j in range(m):
            result[i + j] += A[i] * B[j]
    return result


def fft(coeffs):
    n = len(coeffs)
    if n == 1:
        return coeffs

    even = fft(coeffs[0::2])
    odd = fft(coeffs[1::2])

    w = cmath.exp(-2j * cmath.pi / n)
    result = [0] * n
    wk = 1
    for k in range(n // 2):
        result[k] = even[k] + wk * odd[k]
        result[k + n // 2] = even[k] - wk * odd[k]
        wk *= w

    return result


def ifft(values):
    n = len(values)
    if n == 1:
        return values

    even = ifft(values[0::2])
    odd = ifft(values[1::2])

    w = cmath.exp(2j * cmath.pi / n)
    result = [0] * n
    wk = 1
    for k in range(n // 2):
        result[k] = even[k] + wk * odd[k]
        result[k + n // 2] = even[k] - wk * odd[k]
        wk *= w

    return [x / 2 for x in result]


def next_power_of_2(n):
    p = 1
    while p < n:
        p *= 2
    return p


def fft_multiply(A, B):
    result_len = len(A) + len(B) - 1
    n = next_power_of_2(result_len)

    # pad with zeros
    fa = A + [0] * (n - len(A))
    fb = B + [0] * (n - len(B))

    fa = fft(fa)
    fb = fft(fb)

    fc = [fa[i] * fb[i] for i in range(n)]

    result = ifft(fc)
    result = [round(x.real) for x in result[:result_len]]
    return result


def poly_to_string(coeffs):
    terms = []
    for i, c in enumerate(coeffs):
        if c == 0:
            continue
        if i == 0:
            terms.append(str(c))
        elif i == 1:
            terms.append(f"{c}x")
        else:
            terms.append(f"{c}x^{i}")
    return " + ".join(terms) if terms else "0"


def main():
    # correctness test
    print("=== Correctness Test ===")
    A = [1, 2, 3]       # 1 + 2x + 3x^2
    B = [4, 5]           # 4 + 5x
    bf_result = brute_force_multiply(A, B)
    fft_result = fft_multiply(A, B)

    print(f"A(x) = {poly_to_string(A)}")
    print(f"B(x) = {poly_to_string(B)}")
    print(f"Brute force: {poly_to_string(bf_result)}")
    print(f"FFT:         {poly_to_string(fft_result)}")
    print(f"Match: {bf_result == fft_result}")

    A2 = [3, -2, 1, 5]    # 3 - 2x + x^2 + 5x^3
    B2 = [1, 0, -1, 2]    # 1 - x^2 + 2x^3
    bf2 = brute_force_multiply(A2, B2)
    fft2 = fft_multiply(A2, B2)
    print(f"\nA(x) = {poly_to_string(A2)}")
    print(f"B(x) = {poly_to_string(B2)}")
    print(f"Brute force: {poly_to_string(bf2)}")
    print(f"FFT:         {poly_to_string(fft2)}")
    print(f"Match: {bf2 == fft2}")

    # timing comparison
    print("\n=== Timing Comparison ===")
    sizes = [64, 128, 256, 512, 1024, 2048, 4096, 8192]
    bf_times = []
    fft_times = []

    for n in sizes:
        A = [random.randint(-10, 10) for _ in range(n)]
        B = [random.randint(-10, 10) for _ in range(n)]

        if n <= 4096:
            start = time.time()
            brute_force_multiply(A, B)
            bf_time = time.time() - start
        else:
            bf_time = None
        bf_times.append(bf_time)

        start = time.time()
        fft_multiply(A, B)
        fft_time = time.time() - start
        fft_times.append(fft_time)

        bf_str = f"{bf_time:.4f}s" if bf_time else "skipped"
        print(f"degree {n:>5}: BF = {bf_str}, FFT = {fft_time:.4f}s")

    # plot
    plt.figure(figsize=(10, 6))
    bf_x = [s for s, t in zip(sizes, bf_times) if t is not None]
    bf_y = [t for t in bf_times if t is not None]
    plt.plot(bf_x, bf_y, 'ro-', label='Brute Force O(n²)')
    plt.plot(sizes, fft_times, 'bs-', label='FFT O(n log n)')
    plt.xlabel('Polynomial Degree')
    plt.ylabel('Time (seconds)')
    plt.title('Polynomial Multiplication - Brute Force vs FFT')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('polynomial_mult_comparison.png', dpi=100)
    plt.show()

    print("\n=== Comparison with Closest Points ===")
    print("Both problems use Divide and Conquer to go from O(n^2) to O(n log n).")
    print("")
    print("Closest Points D&C:")
    print("  - Splits points spatially (by x-coordinate)")
    print("  - Combines by checking a strip of width 2*d around midline")
    print("  - Geometrical observation: at most 7 comparisons per point in strip")
    print("")
    print("FFT for Polynomial Multiplication:")
    print("  - Splits coefficients into even/odd indexed terms")
    print("  - Uses roots of unity as evaluation points")
    print("  - Combines using the butterfly operation")
    print("  - Transforms from coefficient to point-value representation")
    print("")
    print("Key difference: Closest Points divides the geometric space,")
    print("while FFT divides the algebraic structure of the polynomial.")
    print("Both achieve O(n log n) by ensuring the combine step is O(n).")


if __name__ == "__main__":
    main()
