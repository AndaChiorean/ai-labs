import csv
import math
import random
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np


def load_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        data = []
        for row in reader:
            converted = {}
            for key, val in row.items():
                try:
                    converted[key] = float(val)
                except ValueError:
                    converted[key] = val
            data.append(converted)
    return data


# triangular membership function
def triangular(x, a, b, c):
    if x <= a or x >= c:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a)
    else:
        return (c - x) / (c - b)


MEMBERSHIP_PARAMS = {
    "Temperature": {
        "cold": (-5, 0, 15),
        "mild": (10, 17, 25),
        "hot": (20, 30, 40),
    },
    "Humidity": {
        "low": (0, 20, 50),
        "medium": (40, 55, 75),
        "high": (65, 80, 100),
    },
    "WindSpeed": {
        "calm": (0, 0, 15),
        "moderate": (10, 20, 30),
        "strong": (25, 35, 55),
    },
    "Pressure": {
        "low": (985, 990, 1008),
        "normal": (1003, 1012, 1020),
        "high": (1018, 1025, 1030),
    },
}


def fuzzify(value, params):
    result = {}
    for term, (a, b, c) in params.items():
        result[term] = triangular(value, a, b, c)
    return result


def fuzzy_entropy(data, target_col, weights):
    total_w = sum(weights)
    if total_w == 0:
        return 0.0

    class_weights = {}
    for i, row in enumerate(data):
        cls = row[target_col]
        class_weights[cls] = class_weights.get(cls, 0) + weights[i]

    entropy = 0.0
    for w in class_weights.values():
        p = w / total_w
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy


def fuzzy_information_gain(data, attribute, term, target_col, weights):
    params = MEMBERSHIP_PARAMS[attribute]
    a, b, c = params[term]

    membership_degrees = []
    for row in data:
        membership_degrees.append(triangular(row[attribute], a, b, c))

    # weights for samples belonging to this term
    w_in = [weights[i] * membership_degrees[i] for i in range(len(data))]
    # weights for samples not belonging
    w_out = [weights[i] * (1 - membership_degrees[i]) for i in range(len(data))]

    total_in = sum(w_in)
    total_out = sum(w_out)
    total = total_in + total_out
    if total == 0:
        return 0

    parent_entropy = fuzzy_entropy(data, target_col, weights)
    child_entropy = 0.0
    if total_in > 0:
        child_entropy += (total_in / total) * fuzzy_entropy(data, target_col, w_in)
    if total_out > 0:
        child_entropy += (total_out / total) * fuzzy_entropy(data, target_col, w_out)

    return parent_entropy - child_entropy


def build_fuzzy_tree(data, attributes, target_col, weights, depth=0, max_depth=5, min_samples=5):
    total_w = sum(weights)
    if total_w < min_samples or depth >= max_depth:
        return get_weighted_majority(data, target_col, weights)

    class_weights = {}
    for i, row in enumerate(data):
        cls = row[target_col]
        class_weights[cls] = class_weights.get(cls, 0) + weights[i]

    if len(class_weights) <= 1:
        return list(class_weights.keys())[0] if class_weights else "Unknown"

    best_gain = -1
    best_attr = None
    best_term = None

    for attr in attributes:
        for term in MEMBERSHIP_PARAMS[attr]:
            gain = fuzzy_information_gain(data, attr, term, target_col, weights)
            if gain > best_gain:
                best_gain = gain
                best_attr = attr
                best_term = term

    if best_gain <= 0.001:
        return get_weighted_majority(data, target_col, weights)

    params = MEMBERSHIP_PARAMS[best_attr]
    a, b, c = params[best_term]

    membership_degrees = [triangular(row[best_attr], a, b, c) for row in data]
    w_in = [weights[i] * membership_degrees[i] for i in range(len(data))]
    w_out = [weights[i] * (1 - membership_degrees[i]) for i in range(len(data))]

    node = {
        "attribute": best_attr,
        "term": best_term,
        "gain": best_gain,
    }

    node["yes"] = build_fuzzy_tree(data, attributes, target_col, w_in, depth + 1, max_depth, min_samples)
    node["no"] = build_fuzzy_tree(data, attributes, target_col, w_out, depth + 1, max_depth, min_samples)

    return node


def get_weighted_majority(data, target_col, weights):
    class_weights = {}
    for i, row in enumerate(data):
        cls = row[target_col]
        class_weights[cls] = class_weights.get(cls, 0) + weights[i]
    if not class_weights:
        return "Unknown"
    return max(class_weights, key=class_weights.get)


def classify_fuzzy(tree, sample):
    if isinstance(tree, str):
        return tree

    attr = tree["attribute"]
    term = tree["term"]
    params = MEMBERSHIP_PARAMS[attr]
    a, b, c = params[term]

    degree = triangular(sample[attr], a, b, c)

    if degree >= 0.5:
        return classify_fuzzy(tree["yes"], sample)
    else:
        return classify_fuzzy(tree["no"], sample)


def print_fuzzy_tree(tree, indent=0):
    if isinstance(tree, str):
        print(" " * indent + "-> " + tree)
        return
    attr = tree["attribute"]
    term = tree["term"]
    gain = tree["gain"]
    print(" " * indent + f"[{attr} is {term}?] (IG={gain:.4f})")
    print(" " * (indent + 2) + "Yes:")
    print_fuzzy_tree(tree["yes"], indent + 4)
    print(" " * (indent + 2) + "No:")
    print_fuzzy_tree(tree["no"], indent + 4)


# --- crisp decision tree for comparison ---
def crisp_entropy(data, target_col):
    counts = Counter(row[target_col] for row in data)
    total = len(data)
    entropy = 0.0
    for count in counts.values():
        p = count / total
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy


def find_best_split(data, attribute, target_col):
    values = sorted(set(row[attribute] for row in data))
    best_gain = -1
    best_threshold = None

    for i in range(len(values) - 1):
        threshold = (values[i] + values[i+1]) / 2
        left = [r for r in data if r[attribute] <= threshold]
        right = [r for r in data if r[attribute] > threshold]

        if len(left) == 0 or len(right) == 0:
            continue

        parent_e = crisp_entropy(data, target_col)
        child_e = (len(left)/len(data)) * crisp_entropy(left, target_col) + \
                  (len(right)/len(data)) * crisp_entropy(right, target_col)
        gain = parent_e - child_e
        if gain > best_gain:
            best_gain = gain
            best_threshold = threshold

    return best_gain, best_threshold


def build_crisp_tree(data, attributes, target_col, depth=0, max_depth=5, min_samples=5):
    if len(data) < min_samples or depth >= max_depth:
        counts = Counter(row[target_col] for row in data)
        return counts.most_common(1)[0][0] if counts else "Unknown"

    classes = set(row[target_col] for row in data)
    if len(classes) == 1:
        return list(classes)[0]

    best_gain = -1
    best_attr = None
    best_threshold = None

    for attr in attributes:
        gain, threshold = find_best_split(data, attr, target_col)
        if gain > best_gain:
            best_gain = gain
            best_attr = attr
            best_threshold = threshold

    if best_gain <= 0.001:
        counts = Counter(row[target_col] for row in data)
        return counts.most_common(1)[0][0]

    left = [r for r in data if r[best_attr] <= best_threshold]
    right = [r for r in data if r[best_attr] > best_threshold]

    return {
        "attribute": best_attr,
        "threshold": best_threshold,
        "left": build_crisp_tree(left, attributes, target_col, depth+1, max_depth, min_samples),
        "right": build_crisp_tree(right, attributes, target_col, depth+1, max_depth, min_samples),
    }


def classify_crisp(tree, sample):
    if isinstance(tree, str):
        return tree
    if sample[tree["attribute"]] <= tree["threshold"]:
        return classify_crisp(tree["left"], sample)
    else:
        return classify_crisp(tree["right"], sample)


def main():
    data = load_csv("weather_data.csv")
    target = "Rainfall"
    attributes = [col for col in data[0].keys() if col != target]

    random.seed(42)
    random.shuffle(data)
    split = int(0.8 * len(data))
    train_data = data[:split]
    test_data = data[split:]

    print(f"Dataset: {len(data)} samples ({len(train_data)} train, {len(test_data)} test)")
    print(f"Attributes: {attributes}")
    print(f"Target: {target}")
    print()

    # --- Fuzzy Decision Tree ---
    print("=" * 50)
    print("FUZZY DECISION TREE")
    print("=" * 50)
    print("\nMembership functions:")
    for attr, terms in MEMBERSHIP_PARAMS.items():
        print(f"  {attr}:")
        for term, (a, b, c) in terms.items():
            print(f"    {term}: triangle({a}, {b}, {c})")

    weights = [1.0] * len(train_data)
    fuzzy_tree = build_fuzzy_tree(train_data, attributes, target, weights)

    print("\nFuzzy tree structure:")
    print_fuzzy_tree(fuzzy_tree)

    correct_train = sum(1 for row in train_data if classify_fuzzy(fuzzy_tree, row) == row[target])
    correct_test = sum(1 for row in test_data if classify_fuzzy(fuzzy_tree, row) == row[target])
    print(f"\nFuzzy DT - Train accuracy: {correct_train}/{len(train_data)} ({100*correct_train/len(train_data):.1f}%)")
    print(f"Fuzzy DT - Test accuracy: {correct_test}/{len(test_data)} ({100*correct_test/len(test_data):.1f}%)")

    # --- Crisp Decision Tree ---
    print("\n" + "=" * 50)
    print("CRISP DECISION TREE (for comparison)")
    print("=" * 50)

    crisp_tree = build_crisp_tree(train_data, attributes, target)

    correct_train_c = sum(1 for row in train_data if classify_crisp(crisp_tree, row) == row[target])
    correct_test_c = sum(1 for row in test_data if classify_crisp(crisp_tree, row) == row[target])
    print(f"Crisp DT - Train accuracy: {correct_train_c}/{len(train_data)} ({100*correct_train_c/len(train_data):.1f}%)")
    print(f"Crisp DT - Test accuracy: {correct_test_c}/{len(test_data)} ({100*correct_test_c/len(test_data):.1f}%)")

    # --- Comparison ---
    print("\n" + "=" * 50)
    print("COMPARISON")
    print("=" * 50)
    print(f"{'Method':<20} {'Train Acc':>12} {'Test Acc':>12}")
    print("-" * 44)
    print(f"{'Fuzzy DT':<20} {100*correct_train/len(train_data):>11.1f}% {100*correct_test/len(test_data):>11.1f}%")
    print(f"{'Crisp DT':<20} {100*correct_train_c/len(train_data):>11.1f}% {100*correct_test_c/len(test_data):>11.1f}%")

    print("\nKey difference: Fuzzy DT uses membership degrees (partial belonging)")
    print("while Crisp DT uses hard thresholds. Fuzzy DT handles boundary cases")
    print("more gracefully since a sample can partially belong to multiple categories.")

    # --- Feature Importance Analysis ---
    print("\n" + "=" * 50)
    print("FEATURE IMPORTANCE ANALYSIS")
    print("=" * 50)

    # fuzzy: compute IG for each attribute+term pair
    weights_all = [1.0] * len(train_data)
    print("\nFuzzy DT - Information Gain per attribute/term:")
    fuzzy_importance = {}
    for attr in attributes:
        fuzzy_importance[attr] = 0
        for term in MEMBERSHIP_PARAMS[attr]:
            ig = fuzzy_information_gain(train_data, attr, term, target, weights_all)
            print(f"  {attr:>15} [{term:<10}]: IG = {ig:.4f}")
            fuzzy_importance[attr] = max(fuzzy_importance[attr], ig)

    print("\n  Summary (max IG per attribute):")
    for attr in sorted(fuzzy_importance, key=fuzzy_importance.get, reverse=True):
        print(f"    {attr:<15}: {fuzzy_importance[attr]:.4f}")

    # crisp: compute best split IG for each attribute
    print("\nCrisp DT - Best split IG per attribute:")
    crisp_importance = {}
    for attr in attributes:
        gain, threshold = find_best_split(train_data, attr, target)
        crisp_importance[attr] = gain
        print(f"  {attr:<15}: IG = {gain:.4f} (threshold = {threshold:.1f})")

    # extract split order from trees
    print("\n--- Split order (which feature is used first) ---")
    def get_split_order_fuzzy(tree, order=None):
        if order is None:
            order = []
        if isinstance(tree, str):
            return order
        order.append(f"{tree['attribute']} [{tree['term']}]")
        get_split_order_fuzzy(tree["yes"], order)
        get_split_order_fuzzy(tree["no"], order)
        return order

    def get_split_order_crisp(tree, order=None):
        if order is None:
            order = []
        if isinstance(tree, str):
            return order
        order.append(f"{tree['attribute']} (<= {tree['threshold']:.1f})")
        get_split_order_crisp(tree["left"], order)
        get_split_order_crisp(tree["right"], order)
        return order

    fuzzy_order = get_split_order_fuzzy(fuzzy_tree)
    crisp_order = get_split_order_crisp(crisp_tree)
    print(f"  Fuzzy DT splits: {' -> '.join(fuzzy_order[:5])}")
    print(f"  Crisp DT splits: {' -> '.join(crisp_order[:5])}")

    # --- plot feature importance comparison ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    sorted_attrs = sorted(attributes, key=lambda a: fuzzy_importance[a], reverse=True)
    x = np.arange(len(sorted_attrs))
    fuzzy_vals = [fuzzy_importance[a] for a in sorted_attrs]
    crisp_vals = [crisp_importance[a] for a in sorted_attrs]

    width = 0.35
    ax1.bar(x - width/2, fuzzy_vals, width, label='Fuzzy DT', color='#4dabf7', alpha=0.8)
    ax1.bar(x + width/2, crisp_vals, width, label='Crisp DT', color='#ff6b6b', alpha=0.8)
    ax1.set_xticks(x)
    ax1.set_xticklabels(sorted_attrs, rotation=30, ha='right')
    ax1.set_ylabel('Information Gain')
    ax1.set_title('Feature Importance: Fuzzy vs Crisp DT')
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')

    # plot membership functions
    for i, attr in enumerate(sorted_attrs):
        vals = sorted(set(row[attr] for row in data))
        x_range = np.linspace(min(vals) - 2, max(vals) + 2, 200)

        for term, (a, b, c) in MEMBERSHIP_PARAMS[attr].items():
            y = [triangular(x, a, b, c) for x in x_range]
            ax2.plot(x_range, y, label=f"{attr}: {term}" if i == 0 or attr == sorted_attrs[0] else None)

    ax2.set_xlabel('Feature Value')
    ax2.set_ylabel('Membership Degree')
    ax2.set_title(f'Membership Functions ({sorted_attrs[0]})')
    # only show membership functions for the most important feature
    ax2.clear()
    best_attr = sorted_attrs[0]
    vals = sorted(set(row[best_attr] for row in data))
    x_range = np.linspace(min(vals) - 5, max(vals) + 5, 300)
    colors = ['#4dabf7', '#51cf66', '#ff6b6b']
    for j, (term, (a, b, c)) in enumerate(MEMBERSHIP_PARAMS[best_attr].items()):
        y = [triangular(x, a, b, c) for x in x_range]
        ax2.plot(x_range, y, label=term, color=colors[j % len(colors)], linewidth=2)
        ax2.fill_between(x_range, y, alpha=0.15, color=colors[j % len(colors)])
    ax2.set_xlabel(best_attr)
    ax2.set_ylabel('Membership Degree')
    ax2.set_title(f'Triangular Membership Functions: {best_attr}')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 1.1)

    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=150)
    plt.close()
    print("\nSaved feature importance plot to feature_importance.png")


if __name__ == "__main__":
    main()
