import struct
import math


def float_to_bits(f):
    packed = struct.pack('f', f)
    return struct.unpack('I', packed)[0]


def bits_to_float(i):
    packed = struct.pack('I', i)
    return struct.unpack('f', packed)[0]


def show_ieee754(f):
    bits = float_to_bits(f)
    binary = format(bits, '032b')
    sign = binary[0]
    exponent = binary[1:9]
    mantissa = binary[9:]
    print(f"  Value: {f}")
    print(f"  Binary: {sign} | {exponent} | {mantissa}")
    print(f"  Sign: {sign} ({'negative' if sign == '1' else 'positive'})")
    print(f"  Exponent: {exponent} (biased: {int(exponent, 2)}, actual: {int(exponent, 2) - 127})")
    print(f"  Mantissa: {mantissa}")


def fast_inverse_sqrt(number):
    x2 = number * 0.5
    i = float_to_bits(number)

    # the magic constant
    i = 0x5f3759df - (i >> 1)

    y = bits_to_float(i)

    # one iteration of Newton's method
    # f(y) = 1/y^2 - x = 0
    # y = y * (1.5 - x2 * y * y)
    y = y * (1.5 - (x2 * y * y))

    return y


def newtons_method_poly_root(coefficients, a, b, tol=1e-10, max_iter=100):
    """
    Find root of polynomial P(x) in [a,b].
    coefficients[i] = coefficient of x^i
    Polynomial is strictly increasing and convex, so starting from b converges.
    """
    def evaluate(x):
        result = 0
        for i, c in enumerate(coefficients):
            result += c * (x ** i)
        return result

    def evaluate_derivative(x):
        result = 0
        for i, c in enumerate(coefficients):
            if i > 0:
                result += i * c * (x ** (i - 1))
        return result

    x = b
    print(f"  Starting Newton's method from x = {x}")

    for iteration in range(max_iter):
        fx = evaluate(x)
        fpx = evaluate_derivative(x)
        if abs(fpx) < 1e-15:
            break
        x_new = x - fx / fpx
        print(f"  Iteration {iteration + 1}: x = {x_new:.12f}, f(x) = {fx:.2e}")
        if abs(x_new - x) < tol:
            return x_new, iteration + 1
        x = x_new

    return x, max_iter


def nth_root_newton(x, n, tol=1e-12, max_iter=100):
    """
    Compute x^(1/n) using Newton's method.
    Solve f(t) = t^n - x = 0
    f'(t) = n * t^(n-1)
    t_{k+1} = t_k - (t_k^n - x) / (n * t_k^(n-1))
            = t_k * (1 - 1/n) + x / (n * t_k^(n-1))
    """
    if x <= 0:
        return 0.0, 0

    t = x / n if x > 1 else x
    if t == 0:
        t = 1.0

    for iteration in range(max_iter):
        t_new = t - (t**n - x) / (n * t**(n - 1))
        if abs(t_new - t) < tol:
            return t_new, iteration + 1
        t = t_new

    return t, max_iter


def main():
    # --- Fast Inverse Square Root ---
    print("=" * 60)
    print("QUAKE III FAST INVERSE SQUARE ROOT")
    print("=" * 60)

    print("\nIEEE 754 Float Representation:")
    print("A 32-bit float is stored as: [1 sign][8 exponent][23 mantissa]")
    print("Value = (-1)^sign * 2^(exponent-127) * (1 + mantissa/2^23)")
    print()

    test_values = [0.15625, 1.0, 2.0, 4.0, 100.0]
    for val in test_values:
        print(f"IEEE 754 breakdown for {val}:")
        show_ieee754(val)
        print()

    print("Fast Inverse Square Root results:")
    print(f"{'x':>10} {'fast_isqrt':>15} {'actual':>15} {'error%':>10}")
    print("-" * 55)

    for x in [0.25, 1.0, 2.0, 4.0, 16.0, 100.0, 1234.56]:
        fast = fast_inverse_sqrt(x)
        actual = 1.0 / math.sqrt(x)
        error = abs(fast - actual) / actual * 100
        print(f"{x:>10.2f} {fast:>15.10f} {actual:>15.10f} {error:>9.4f}%")

    print("\nThe magic constant 0x5f3759df works because:")
    print("  log2(1/sqrt(x)) = -0.5 * log2(x)")
    print("  The integer representation of a float approximates log2(x)")
    print("  So bit-shifting right by 1 and subtracting from a constant")
    print("  gives a good initial approximation for Newton's method.")

    # --- Newton's Method for Polynomial Root ---
    print("\n" + "=" * 60)
    print("NEWTON'S METHOD - POLYNOMIAL ROOT")
    print("=" * 60)

    # P(x) = x^3 + 2x - 5 (strictly increasing convex for x > 0)
    # has a root near x = 1.3288
    coefficients = [-5, 2, 0, 1]  # -5 + 2x + x^3
    print("\nP(x) = x^3 + 2x - 5")
    print("Finding root in [1, 2]:")
    root, iters = newtons_method_poly_root(coefficients, 1, 2)
    print(f"\n  Root found: {root:.12f} in {iters} iterations")
    val = root**3 + 2*root - 5
    print(f"  Verification: P({root:.8f}) = {val:.2e}")

    # P(x) = x^2 + 3x - 10 (root at x=2)
    coefficients2 = [-10, 3, 1]
    print("\nP(x) = x^2 + 3x - 10")
    print("Finding root in [0, 5]:")
    root2, iters2 = newtons_method_poly_root(coefficients2, 0, 5)
    print(f"\n  Root found: {root2:.12f} in {iters2} iterations")

    # --- Newton's Method for Nth Root ---
    print("\n" + "=" * 60)
    print("NEWTON'S METHOD - NTH ROOT")
    print("=" * 60)

    test_cases = [
        (27, 3),    # cube root of 27 = 3
        (16, 4),    # 4th root of 16 = 2
        (100, 2),   # sqrt of 100 = 10
        (1024, 10), # 10th root of 1024 = 2
        (7.5, 3),   # cube root of 7.5
    ]

    print(f"\n{'x':>8} {'n':>4} {'Newton':>15} {'Python':>15} {'Iters':>6}")
    print("-" * 52)

    for x, n in test_cases:
        result, iters = nth_root_newton(x, n)
        python_result = x ** (1.0 / n)
        print(f"{x:>8.1f} {n:>4} {result:>15.10f} {python_result:>15.10f} {iters:>6}")


if __name__ == "__main__":
    main()
