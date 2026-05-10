import csv
import math
from collections import Counter


def load_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    return data


def compute_entropy(data, target_col):
    counts = Counter(row[target_col] for row in data)
    total = len(data)
    entropy = 0.0
    for count in counts.values():
        p = count / total
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy


def compute_information_gain(data, attribute, target_col):
    total_entropy = compute_entropy(data, target_col)
    values = set(row[attribute] for row in data)
    total = len(data)

    weighted_entropy = 0.0
    for val in values:
        subset = [row for row in data if row[attribute] == val]
        weight = len(subset) / total
        weighted_entropy += weight * compute_entropy(subset, target_col)

    ig = total_entropy - weighted_entropy
    return ig


def majority_class(data, target_col):
    counts = Counter(row[target_col] for row in data)
    return counts.most_common(1)[0][0]


def build_tree(data, attributes, target_col):
    classes = set(row[target_col] for row in data)
    if len(classes) == 1:
        return list(classes)[0]

    if len(attributes) == 0:
        return majority_class(data, target_col)

    gains = {}
    for attr in attributes:
        gains[attr] = compute_information_gain(data, attr, target_col)

    best_attr = max(gains, key=gains.get)
    print(f"Splitting on '{best_attr}' (IG = {gains[best_attr]:.4f})")
    for attr in attributes:
        print(f"  {attr}: IG = {gains[attr]:.4f}")

    tree = {best_attr: {}}
    values = set(row[best_attr] for row in data)
    remaining_attrs = [a for a in attributes if a != best_attr]

    for val in values:
        subset = [row for row in data if row[best_attr] == val]
        if len(subset) == 0:
            tree[best_attr][val] = majority_class(data, target_col)
        else:
            tree[best_attr][val] = build_tree(subset, remaining_attrs, target_col)

    return tree


def classify(tree, sample):
    if isinstance(tree, str):
        return tree
    attr = list(tree.keys())[0]
    val = sample.get(attr)
    if val in tree[attr]:
        return classify(tree[attr][val], sample)
    else:
        return "Unknown"


def print_tree(tree, indent=0):
    if isinstance(tree, str):
        print(" " * indent + "-> " + tree)
        return
    attr = list(tree.keys())[0]
    for val, subtree in tree[attr].items():
        print(" " * indent + f"[{attr} = {val}]")
        print_tree(subtree, indent + 4)


def main():
    data = load_csv("play_tennis.csv")
    target = "PlayTennis"
    attributes = [col for col in data[0].keys() if col != target]

    print("=== Building Decision Tree (ID3) ===")
    print(f"Dataset size: {len(data)} samples")
    print(f"Attributes: {attributes}")
    print(f"Target: {target}")
    print(f"Initial entropy: {compute_entropy(data, target):.4f}")
    print()

    tree = build_tree(data, attributes, target)

    print("\n=== Decision Tree Structure ===")
    print_tree(tree)

    print("\n=== Classifying training data ===")
    correct = 0
    for row in data:
        prediction = classify(tree, row)
        actual = row[target]
        match = "OK" if prediction == actual else "WRONG"
        if prediction != actual:
            print(f"  {row} -> predicted: {prediction}, actual: {actual} [{match}]")
        correct += (prediction == actual)

    print(f"\nTraining accuracy: {correct}/{len(data)} ({100*correct/len(data):.1f}%)")

    print("\n=== Testing with new samples ===")
    test_samples = [
        {"Outlook": "Sunny", "Temperature": "Cool", "Humidity": "High", "Wind": "Strong"},
        {"Outlook": "Overcast", "Temperature": "Mild", "Humidity": "Normal", "Wind": "Weak"},
        {"Outlook": "Rain", "Temperature": "Hot", "Humidity": "Normal", "Wind": "Weak"},
    ]
    for sample in test_samples:
        result = classify(tree, sample)
        print(f"  {sample} -> {result}")


if __name__ == "__main__":
    main()
