# Complete Study Guide — AI with Prof. Mircea Ioan-Gabriel

This is the full structured & enriched version of your seminar + lecture notes. Topics are reorganized for studying (not in the order he taught them). Each section: **his notes** (what you wrote) → **enriched explanation** → **exam angle**.

---

# PART I — FOUNDATIONS: What is Intelligence?

## 1.1 Intelligence, Information, AI

**Your notes:** `inteligență → informație`, `început → final`, AT&T Bell Labs, Aristotelian logic.

**Enriched:**
- **Intelligence** (his definition): the flow of *information* from a beginning state to a (possibly never-reached) final state. The "?" between is what AI tries to fill.
- **Information** ≠ data. Information = data + meaning. Etymology: Latin *informare* = "to give form to". The Greek root is *logos* (λόγος) = word, meaning, principle.
- **AT&T Bell Labs**: birthplace of much modern info theory. Claude Shannon (1948) defined info theory there; the transistor (1947) was invented there.
- **Aristotelian logic** (Aristotle, 384–322 BC): the three laws — identity (A = A), non-contradiction (¬(A ∧ ¬A)), excluded middle (A ∨ ¬A). This is exactly Boolean algebra reformulated 2200 years later.

**Exam angle:** "Define intelligence." Answer: connect philosophy → information → flow → decisions. Mention Aristotle, Shannon, AT&T Bell Labs.

---

## 1.2 The Greek Chain: Socrates → Plato → Aristotle → Alexander

**Your notes:** strategy, discernment (`discernământ`), logical thinking, decision, "we know nothing".

**Enriched:**
| Figure | Years (BC) | Contribution |
|--------|-----------|--------------|
| **Socrates** | 470–399 | "I know that I know nothing." Method: questioning (dialectic). Foundation of skepticism. |
| **Plato** | 428–348 | Theory of Forms (abstract reality > physical). Created the *graphical concept* (drawing letters on clay tablets, hence the term "graphics"). Founded the Academy. |
| **Aristotle** | 384–322 | Formal logic. Categorized everything. Wrote *Organon* (logic) and *Metaphysics*. |
| **Alexander the Great** | 356–323 | Aristotle's student. Used **strategy** (στρατηγία) — making rational decisions under uncertainty. Spread Greek learning to Egypt → Library of Alexandria. |

**The chain matters because:** discernment → logical thinking → decisions = exactly what an AI agent must do.

**Exam angle:** "Trace the philosophical roots of AI." Use this table.

---

## 1.3 Test Turing & The Imitation Game

**Your notes:** Alan Turing, "the calculation machine", Imitation Game film, Test Turing.

**Enriched:**
- **Alan Turing** (1912–1954): British mathematician. Concepts:
  - **Turing machine** (1936): abstract model of computation. Tape + read/write head + states. Proven equivalent to any computable function (Church-Turing thesis).
  - **Halting problem** (1936): undecidable — no algorithm can determine if an arbitrary program halts. → Death = the only certain halt.
  - **Turing Test** (1950, paper "Computing Machinery and Intelligence"): if a human judge cannot reliably tell a machine from a human via text-only conversation, the machine is "intelligent."
- **The Imitation Game** (2014 film): dramatization of Turing breaking the Enigma cipher at Bletchley Park, WWII.
- **Koko the gorilla**: a real example — primate that learned sign language and asked questions. Used in the lecture as the *animal* counterpoint to the *machine* in the Turing test.

**Exam angle:** "Describe the Turing test and its limitations." Include: indistinguishability via text, behavioral definition (not internal state), Searle's Chinese Room counter-argument.

---

## 1.4 Pioneers of Computing

**Your notes:** Ada Lovelace, Charles Babbage, George Boole, J.F. Neumann, Alan Turing.

**Enriched timeline:**
| Year | Person | Contribution |
|------|--------|-------------|
| ~825 | **Al-Khwarizmi** | Wrote *Al-Jabr* (algebra). Name → "algorithm". |
| 1815–1852 | **Ada Lovelace** | First algorithm intended for a machine (Bernoulli numbers, for Babbage's Analytical Engine — which was never built!). First programmer. |
| 1791–1871 | **Charles Babbage** | Designed the Analytical Engine (mechanical computer). Never finished. |
| 1815–1864 | **George Boole** | *Laws of Thought* (1854): Boolean algebra. Formalized Aristotelian logic algebraically. |
| 1903–1957 | **John von Neumann** | Father of modern computer architecture. Born in Hungary, Manhattan Project, game theory, cellular automata. "Father of AI." |
| 1912–1954 | **Alan Turing** | Turing machine, Turing test, Enigma. |
| 1916–2001 | **Claude Shannon** | Information theory (1948). Entropy of information. |
| 1928– | **Frank Rosenblatt** | Perceptron (1958). First artificial neuron. Built on Mark I Perceptron (Cornell). |

**Exam angle:** Be ready to name **at least 5** of these and what they did.

---

# PART II — MATHEMATICAL FOUNDATIONS

## 2.1 Sets, Relations, Functions

**Your notes:** `{0,1} × {0,1} = {(0,0), (0,1), (1,0), (1,1)}`, Cartesian product, Descartes, relations as subsets, functions as relations.

**Enriched:**

### Set
- A collection of distinct elements: `A = {0, 1}`.
- `|A|` = cardinality (size).

### Cartesian product
- `A × B = {(a, b) | a ∈ A, b ∈ B}`.
- Named after **René Descartes** (1596–1650). The famous "fly on the ceiling" story: he watched a fly and wondered how to specify its position → invented coordinates → algebra + geometry merged.
- Example: `{0,1} × {0,1} = {(0,0), (0,1), (1,0), (1,1)}` — exactly the truth table of two boolean variables.

### Relation
- A relation R from A to B is a *subset* of A × B.
- Order relation (≤), equality (=), inequality (≠), strict (<, >).

### Function
- A function f: A → B is a relation where every a ∈ A has *exactly one* b ∈ B.
- **Bijective function** = injective (one-to-one) + surjective (onto). Has an inverse.
- Any bijective function can be used as a **code/cipher** (encode → decode).

### Encoding & Decoding
```
   domain ──encoding──> codomain
   domain <──decoding── codomain
```
A code is a bijection between meaning and representation.

**Exam angle:** "What's the difference between a relation and a function?" "Why is a Cartesian product important in CS?" Answer: it's the structure underlying truth tables, databases (joins), and feature spaces.

---

## 2.2 Algebra vs. Logic vs. Informatics vs. Geometry

**Your notes:** Venn diagram — algebra ⊃ logic ⊃ informatics ⊃ geometry (he drew it nested).

**Enriched:**
- **Algebra** (al-jabr, "reunion of broken parts"): operations on symbols. (ℕ, +, ×) is an algebra.
- **Logic** (Aristotelian → Boolean): operations on truth values. ({0,1}, ∧, ∨, ¬) is an algebra over Booleans.
- **Informatics**: science of solving problems algorithmically with finite resources.
- **Geometry** (γεωμετρία, "earth-measure"): study of shape, space. Descartes united it with algebra.

**Key insight he repeats:** **Boolean algebra ≡ Aristotelian logic**. Boole rewrote 2200-year-old logic in algebraic form (∧ ≡ ×, ∨ ≡ +, ¬ ≡ 1-x).

**Definition he wants:**
> **Informatics** = the science of solving problems using algorithms, with the available resources and **minimum energy spent** (i.e., minimum number of steps).

**Exam angle:** "What is the relationship between math and CS?" Answer: CS is algebra applied to discrete, finite structures, formalized via algorithms. Mention Boole = Aristotle.

---

## 2.3 Number Systems

**Your notes:** ℕ ⊆ ℤ ⊆ ℚ ⊆ ℝ ⊆ ℂ, `|ℕ| = |ℤ| = |ℚ| < |ℝ| = |ℂ|`, Babylonians, Pythagoras, Euclid, Cantor.

**Enriched:**

### The hierarchy
- **ℕ** (Naturals): 0, 1, 2, 3, … — *Babylonians, Egyptians, Greeks*. Used for counting.
- **ℤ** (Integers): …, −2, −1, 0, 1, 2, … — *includes debts (negative)*.
- **ℚ** (Rationals): p/q where p ∈ ℤ, q ∈ ℕ*. *Pythagoras*: discovered fractions through music (half-notes on a string).
- **ℝ** (Reals): ℚ + irrationals. **Pythagoras' theorem** (Babylonians actually had it first, on clay tablets) → √2 is irrational → crisis in his cult.
- **ℂ** (Complex): ℝ + imaginary axis. (Not deeply covered, but mentioned.)

### Cardinality (Cantor's diagonal argument)
- |ℕ| = |ℤ| = |ℚ| = ℵ₀ (countably infinite). You can list them.
- |ℝ| = 2^ℵ₀ = 𝔠 (uncountable). Cantor proved you cannot list them — for any list, you can construct a real not on it.

### Pythagoras and music
- He learned from Egyptians/Persians.
- Discovered that musical harmony comes from ratios (e.g., 2:1 = octave, 3:2 = fifth).
- → Connection: harmony in nature = mathematical structure.

### Prime numbers
- `p > 1`, divisible only by 1 and itself.
- Multiply all primes up to P then add 1 → result is either prime or has a new prime factor → **infinity of primes** (Euclid's proof).
- **Eratosthenes**: sieve algorithm for finding primes.

### Float representation (IEEE 754)
```
[sign | exponent | mantissa]
  1b  |   8b     |   23b      (single precision)
  1b  |  11b     |   52b      (double precision)
```
- Value = (-1)^sign × 1.mantissa × 2^(exponent − bias)
- Bias = 127 (single) or 1023 (double).
- This is what the **Quake fast inverse square root** trick exploits (your lab!).

**Exam angle:** "Prove there are infinitely many primes." Use Euclid's argument. "What's the difference between |ℚ| and |ℝ|?" Cantor's diagonal.

---

## 2.4 The Bijection: ℝ → (-1, 1)

**Your notes:** the diagram with arrow from (-∞, ∞) to (-1, 1), tanh, sigmoid.

**Enriched:**

In ML you need to **normalize** inputs to a bounded range. Two famous bijections:

### Sigmoid (logistic)
- σ(x) = 1 / (1 + e^(-x))
- Range: (0, 1)
- Derivative: σ'(x) = σ(x) · (1 − σ(x)) — beautifully simple
- Used as activation function and probability output

### tanh
- tanh(x) = (e^x − e^(-x)) / (e^x + e^(-x))
- Range: (−1, 1)
- Centered at 0 (better gradients than sigmoid in deep nets)

### Why bijection matters
- Inputs can be from ℝ (any size). Activation functions map them to a finite range so we can combine them safely.
- "Normalization" = applying a bijection.

**Exam angle:** Know both formulas. Know sigmoid's derivative trick. Know why we normalize.

---

# PART III — INFORMATION & ENTROPY

## 3.1 Information Theory (Claude Shannon)

**Your notes:** Shannon, error detection, error correction, error replication, bit = unit of information.

**Enriched:**
- **Claude Shannon** (1916–2001), *A Mathematical Theory of Communication* (1948). The single most important paper in CS history.
- He defined:
  - **Bit** = binary digit, unit of information = 1 yes/no answer
  - **Channel** = path that carries info from A → B
  - **Noise** = anything that corrupts the signal
  - **Error correction**: redundancy added so receiver can detect/fix corruption
  - **Channel capacity** = max info bits/second
- Internet cables encode bits → packets → travel → some corrupt → checksum/CRC detects → resend
- Three operations on info: **copy, move, replicate**.

### Information vs. Entropy
- More uncertainty (high entropy) = more information needed to specify outcome.
- "What will the coin show?" — 1 bit of entropy. Need 1 bit to answer.
- "What will the die show?" — log₂(6) ≈ 2.58 bits.

**Exam angle:** Define bit. Define entropy of info. Connect to Boltzmann.

---

## 3.2 Entropy: The Two Formulas

This is **central**. He will ask. Memorize both.

### Shannon entropy (information)
$$H(X) = -\sum_{i=1}^{n} p_i \log_2 p_i$$
- Unit: bits
- For a fair coin: H = -[0.5·log₂(0.5) + 0.5·log₂(0.5)] = 1 bit
- For a die: H = log₂(6) ≈ 2.58 bits
- For a deterministic event (p=1): H = 0
- Maximum entropy: uniform distribution

### Boltzmann entropy (thermodynamics)
$$S = k_B \cdot \ln W$$
- k_B = Boltzmann constant ≈ 1.381 × 10⁻²³ J/K
- W = number of microstates consistent with the macrostate
- For your particle sim: W = N! / (n₁! · n₂! · … · n_k!) — the number of ways particles can be distributed in subcubes given counts (n₁, …, n_k)
- Use **Stirling's approximation**: ln(N!) ≈ N·ln(N) − N

### The connection
- Both measure **disorder** / **uncertainty**.
- Shannon's formula is the **discrete analog** of Boltzmann's.
- Universe tends to maximum entropy (2nd law of thermodynamics).
- CMB (Cosmic Microwave Background) = most entropic structure we know.

**Exam angle:** Write both formulas. Explain why they're "the same thing." Give an example calculation.

---

## 3.3 The Big-Bang / CMB Connection

**Your notes:** CMB, universe flat (curvature 0), Boltzmann in mechanics, Shannon in informatics, atoms, stars.

**Enriched:**
- **CMB** (Cosmic Microwave Background): leftover radiation from ~380,000 years after the Big Bang. Discovered 1964 (Penzias & Wilson, Bell Labs again!).
- It's nearly uniform (max entropy) — supports the Big Bang theory.
- **Stars** form when gravity collapses matter; particles speed up → temperature → eventual fusion.
- **Atom** (ἄτομος, "uncuttable") — the term assumed indivisibility, but we now know atoms have nuclei (protons, neutrons) and electrons.
- Mass ≈ all in nucleus (electrons negligible).
- E = m·c²: energy & mass equivalence.

**Exam angle:** Why does the universe being mostly CMB matter? Because it's the **max-entropy reference** — informs us where physical entropy "lives."

---

# PART IV — ALGORITHMS & SEARCH

## 4.1 What is an Algorithm? What is a Problem?

**His preferred definitions (memorize verbatim):**

> **Algorithm** = a finite succession of steps that solves a problem.
>
> **Problem** = a finite succession (or set) of input + output variables.
>
> **Program** = data + code = a finite succession of instructions, executable on a machine.

Key distinctions:
| Algorithm | Program |
|-----------|---------|
| Abstract | Concrete |
| Steps | Instructions |
| Number of steps (complexity) | Milliseconds (real time) |
| Theoretical | Implementable |

**Etymology:**
- "Algorithm" ← Al-Khwarizmi (~780–850), Persian mathematician at the House of Wisdom in Baghdad.
- His book *Al-Kitāb al-mukhtaṣar fī ḥisāb al-jabr wa-l-muqābala* gave us "algebra".

**Variable vs constant:**
- Variable: has an address, a data type, a label/name, and a (mutable) value.
- Constant: same but immutable.

**Exam angle:** "Define algorithm and problem." Word-for-word. Then say where the name comes from.

---

## 4.2 Algorithm Design Paradigms

| Paradigm | Idea | Example |
|----------|------|---------|
| **Brute Force** | Try all possibilities | Closest pair (n²), TSP via all permutations |
| **Backtracking** | DFS with pruning when constraint violated | N-Queens, Sudoku |
| **Divide & Conquer** | Split, recurse, combine | Merge sort, FFT, closest-points D&C |
| **Greedy** | Take best local choice | Dijkstra, Kruskal, nearest-neighbor TSP |
| **Dynamic Programming** | Cache subproblem results | Needleman-Wunsch, Fibonacci, LCS |
| **Heuristic** | Use educated guess | Hill climbing, A*, Tabu |
| **Stochastic / Metaheuristic** | Use randomness | Simulated annealing, GA, PSO, ACO |

**Greedy = first sign of intelligence** (he said this).
**Backtracking = first sign of intelligence in code** (re: decision trees).

**Exam angle:** Be able to give an example of each. Especially D&C (used in closest-points and FFT — your labs).

---

## 4.3 Search

**Your notes:** BFS vs DFS, breadth-first, depth-first, complexity, search space.

**Enriched:**

### The search problem
Find `x = (x₁, …, x_n)`, where each `xᵢ ∈ Dᵢ` (domain), such that `x` is a solution (satisfies given constraints / minimizes given cost).

**Complexity (brute force):** O(|D₁| × |D₂| × … × |D_n|) = O(∏|Dᵢ|).

### BFS (Breadth-First Search)
- Use a **queue** (FIFO).
- Explore all nodes at depth d before any at depth d+1.
- Finds shortest path (in edges) on unweighted graphs.

### DFS (Depth-First Search)
- Use a **stack** (or recursion).
- Go deep first, backtrack on dead end.
- Lower memory than BFS for deep trees.

### Search spaces
- Variable ⊆ List ⊆ Graph ⊆ Multigraph
- Tree = acyclic connected graph

### Exhaustive vs. Heuristic vs. Stochastic
- **Exhaustive**: BFS, DFS, brute force, backtracking — guaranteed optimal but slow.
- **Heuristic**: A*, hill climbing, Tabu — uses domain knowledge.
- **Stochastic**: SA, GA, PSO, ACO — uses randomness, can escape local optima.

**Exam angle:** Differentiate BFS vs DFS. Differentiate exhaustive/heuristic/stochastic with one example each.

---

## 4.4 Heuristic & Metaheuristic Algorithms

(Covered in your labs in depth. Brief recap.)

### Hill Climbing
- Start with a solution, swap with best neighbor, repeat until no improvement.
- **Local optimum trap.**
- Fix: random restart (multiple runs from random starts).

### Tabu Search (Glover, 1986)
- Hill climbing + memory: **tabu list** of recently visited solutions/moves to forbid revisiting.
- **Aspiration**: override tabu if move beats global best.
- Parameters: tabu tenure, max iterations.

### Simulated Annealing (Kirkpatrick, 1983)
- Inspired by metallurgy: heat a metal, cool slowly → atoms find low-energy configuration.
- Accept worse moves with probability `exp(-ΔE/T)` where T cools over time.
- Cooling: `T = T · α` (α ∈ [0.99, 0.9999]).

### Genetic Algorithm (Holland, 1975)
- Inspired by Darwin's evolution.
- Population of solutions → fitness → selection → crossover → mutation → next gen.
- Encoding: bit strings or permutations.
- For TSP: Order Crossover (OX) preserves permutation structure.

### Swarm: PSO, ACO
- **PSO** (Particle Swarm Optimization): birds/fish flocking. Each particle remembers its best + group's best.
- **ACO** (Ant Colony Optimization): ants lay pheromone trails; shorter paths get reinforced.

**Exam angle:** Compare GA vs SA vs Tabu. Explain when each is preferred.

---

## 4.5 TSP (Travelling Salesman Problem)

**Your notes:** complete graph, Hamiltonian cycle, n! ways, minimize cost.

**Enriched:**
- **Problem:** given n cities with pairwise distances, find the shortest tour that visits each city exactly once and returns to start.
- **Solution:** a **Hamiltonian cycle** with minimum total weight.
- **Search space:** (n-1)!/2 distinct tours (fix starting city, divide by 2 for direction).
- **NP-hard** — no known polynomial-time exact algorithm.
- **Berlin52** (TSPLIB): standard benchmark, 52 cities in Berlin, optimal = 7542.
- **Approaches:**
  - Brute force: O(n!) — infeasible past ~15 cities
  - Exact (Held-Karp DP): O(n²·2ⁿ) — to ~25 cities
  - Heuristic (nearest-neighbor): O(n²), within ~25% of optimal
  - Metaheuristic (SA, GA, Tabu): within ~1–10% of optimal
  - Lin-Kernighan: best known heuristic (within 5% almost always)

**Exam angle:** Why is TSP hard? Because brute force is n! and the problem is NP-hard. Show search-space size.

---

## 4.6 Decision Trees

**Your notes:** Brute force/backtracking, Divide et Impera, Greedy → leads to decision trees.

**Enriched:**

### Idea
- Recursive structure: at each node, split data by some attribute → branches → leaves with predictions.
- **Greedy**: at each node, pick the attribute that maximizes **information gain** (or minimizes entropy/Gini).

### ID3 algorithm (Iterative Dichotomiser 3, Quinlan 1986)
1. Compute entropy of current subset.
2. For each attribute, compute information gain.
3. Pick attribute with highest gain → split.
4. Recurse on each subset.
5. Stop: pure subset, no attributes left, or min samples.

### Information Gain
- IG(S, A) = H(S) − Σ (|S_v|/|S|) · H(S_v) for each value v of A.

### Fuzzy Decision Trees (PROFESSOR'S PHD AREA — KNOW THIS!)
- Replaces hard splits with **fuzzy memberships**.
- For continuous attribute: define triangular membership functions (e.g., "cold", "mild", "hot").
- Compute **fuzzy entropy** using membership-weighted counts.
- An instance can belong to multiple branches with different degrees.
- Aggregate leaf predictions weighted by membership at leaf.
- Better for continuous, noisy, or imprecise data.

**Exam angle:** Build a small ID3 tree. Compare crisp vs fuzzy. Mention his WeaMyL weather ML project.

---

# PART V — MACHINE LEARNING

## 5.1 Datasets, Features, Targets

**Your notes:** training dataset, label/target, feature, training instance, categorical (discrete) → classification, continuous → regression.

**Enriched:**

### Vocabulary
- **Instance / Sample / Point**: one row of data.
- **Feature / Attribute / Column**: one input variable.
- **Label / Target / Output**: what we want to predict.
- **Training set**: data used to fit the model.
- **Test set**: held-out data used to evaluate.
- **Validation set**: used to tune hyperparameters.

### Data types
- **Categorical** (discrete): {red, blue, green} → **classification**.
- **Continuous** (real-valued) → **regression**.
- **Binary**: special case of categorical with 2 classes.

### Data quality issues
- **Noise**: random errors in measurements.
- **Missing values**: gaps in data.
- **Scarcity**: too few samples.
- → Fixes: data preprocessing, data augmentation, data visualization.

**Exam angle:** Differentiate classification vs regression. What's a feature? An instance? A label?

---

## 5.2 The Perceptron (Frank Rosenblatt, 1958)

**Your notes:** Mark I Harvard Navy, first artificial neuron, perceptron.

**Enriched:**

### Structure
```
   x₀──w₀──┐
            ├──Σ──a──f──σ─── output
   x₁──w₁──┘
```
- Inputs: x₀, x₁ (could be more)
- Weights: w₀, w₁ (learned)
- Sum: a = x₀·w₀ + x₁·w₁ (+ bias)
- Activation: σ = f(a)
- Output: σ

### Math (binary classification)
- Linear combination: a = Σ xᵢ·wᵢ + b
- Activation f: step (early), sigmoid (later)
- Decision boundary: a = 0 → hyperplane in input space

### Linearly separable problems
- AND, OR: linearly separable ✓
- **XOR: NOT linearly separable** ✗ (this killed perceptron research in the 1970s — Minsky & Papert's book)
- Solution: multilayer perceptron (MLP) = feedforward neural network with hidden layers.

### Training (delta rule)
1. Initialize weights randomly (small values).
2. For each training instance: compute prediction, compute error.
3. Update weights: wᵢ ← wᵢ − η · ∂E/∂wᵢ
4. Repeat until error converges.

### Mark I Perceptron
- Built 1957–1958 at Cornell Aeronautical Laboratory.
- 400 photocells, motor-driven potentiometers as weights.
- Could recognize simple shapes.

**Exam angle:** Draw the perceptron. Explain the XOR problem. Why was the perceptron a big deal?

---

## 5.3 Activation Functions

**Your notes:** step function, sigmoid (logistic), tanh, trapezoid (more robust to noise).

**Enriched:**

### Step function (Heaviside)
- f(x) = 1 if x ≥ 0, else 0
- Not differentiable → can't use gradient descent
- Used in original perceptron

### Sigmoid / Logistic
- σ(x) = 1 / (1 + e^(-x))
- Range: (0, 1)
- σ'(x) = σ(x) · (1 − σ(x))
- Smooth, differentiable
- Saturates at extremes (gradient vanishes) → vanishing gradient problem

### tanh
- tanh(x) = (e^x − e^(-x)) / (e^x + e^(-x))
- Range: (−1, 1)
- Centered at 0
- Also saturates

### Trapezoidal (fuzzy)
- Piecewise linear: 0 → linear up → 1 → linear down → 0
- Two thresholds (a, b): fully activated between them
- **More robust to noise** than step function
- Used in fuzzy systems

### ReLU (modern, not in your notes but worth knowing)
- f(x) = max(0, x)
- Non-saturating for x > 0 → trains deep nets better
- Used in nearly all modern neural networks

**Exam angle:** Draw step, sigmoid, tanh, trapezoid. Give one pro and one con of each.

---

## 5.4 Loss / Error Functions

**Your notes:** y − σ = error, |y − σ| = absolute error, ½(y − σ)² = squared error (for derivation).

**Enriched:**

### Error / Loss / Cost
| Name | Formula | When |
|------|---------|------|
| Absolute error | \|y − σ\| | Robust to outliers |
| Squared error | ½(y − σ)² | Differentiable, standard for regression |
| Cross-entropy | −Σ y log σ | Classification (paired with sigmoid/softmax) |
| Hinge | max(0, 1 − y·σ) | SVM |

### Why ½ in front?
Derivative of ½·x² is x — cleaner. The ½ disappears.

### Squared error gradient
- E = ½(σ − y)²
- ∂E/∂σ = (σ − y)

**Exam angle:** Derive ∂E/∂σ for squared error.

---

## 5.5 Backpropagation & Gradient Descent

**Your notes:** chain rule, ∂E/∂w₀ = ∂E/∂σ · ∂σ/∂a · ∂a/∂w₀ = (σ−y)·σ(1−σ)·x₀

**Enriched:**

### Chain rule (the heart of backprop)
For a perceptron with sigmoid:
- a = w₀·x₀ + w₁·x₁
- σ = f(a) = 1 / (1 + e^(-a))
- E = ½(σ − y)²

Then:
- ∂E/∂σ = (σ − y)
- ∂σ/∂a = σ(1 − σ)
- ∂a/∂w₀ = x₀
- → ∂E/∂w₀ = (σ − y) · σ(1 − σ) · x₀
- → ∂E/∂w₁ = (σ − y) · σ(1 − σ) · x₁

### Gradient
∇E = [∂E/∂w₀, ∂E/∂w₁]

The gradient points in the direction of **steepest increase**. To **minimize**, go opposite:

### Gradient descent update
```
w₀ ← w₀ − η · ∂E/∂w₀
w₁ ← w₁ − η · ∂E/∂w₁
```
- η = **learning rate**, η ∈ (0, 1)
- Too small: slow convergence
- Too large: oscillates, may diverge

### Geometric intuition
- E(w₀, w₁) is a surface (bowl-shaped for convex case).
- Gradient descent = roll downhill.
- Minimum = bottom of bowl.

### Overfitting
- Model fits training data too well, fails on new data.
- Symptoms: training error low, test error high.
- Causes: too many parameters, too few data, training too long.
- Fixes: regularization, dropout, early stopping, more data, learning-rate decay.

**Exam angle:** Derive the gradient for a 2-input perceptron with sigmoid + squared error. State the update rule. Explain overfitting.

---

## 5.6 Linear Separability & Classification

**Your notes:** 2D drawing of points with separating line, 3D plane (hyperplane), XOR not learnable.

**Enriched:**

### Linearly separable
- Two classes can be separated by a hyperplane (line in 2D, plane in 3D).
- AND, OR are linearly separable.
- XOR is NOT.

### Hyperplane equation
- In 2D: a·x + b·y + c = 0
- In nD: w·x + b = 0 where w, x ∈ ℝⁿ

### Decision rule
- If w·x + b > 0: class 1
- If w·x + b < 0: class 0
- If = 0: on boundary

### Beyond linear: SVM, kernels, neural nets
- **SVM** (Support Vector Machine): finds the hyperplane with **maximum margin** (largest gap between classes). With kernel trick: nonlinear separation.
- **MLP** (multilayer perceptron): solves XOR by stacking layers.

**Exam angle:** Why can't a single perceptron learn XOR? Draw XOR on a 2D plot, show no line separates the classes.

---

## 5.7 SVM & PCA (mentioned, not deep)

### SVM (Support Vector Machine)
- Find the hyperplane that **maximizes margin** between classes.
- Support vectors: points closest to the boundary.
- Soft-margin SVM allows some misclassification.
- **Kernel trick**: map to higher dimension where data is separable (RBF, polynomial).

### PCA (Principal Component Analysis)
- Dimensionality reduction.
- Finds directions of maximum variance (eigenvectors of covariance matrix).
- Project data onto top k components → reduced features.
- Used for: visualization, noise reduction, speedup, deduplication.

**Exam angle:** What is PCA used for? When would you use SVM over a neural net?

---

# PART VI — MODERN AI

## 6.1 Agents (Lecture 12)

**Your notes:** Jane Goodall, agent = models environment + has rules + has will, object ≠ agent.

**Enriched:**

### Definitions
- **Agent**: an entity that perceives, decides, and acts. Has:
  1. A **model** of the environment
  2. A **set of rules** (decision policy)
  3. **Will** (chooses actions; non-deterministic in general)
- **Object**: no will, no rules, just exists.
- **Environment**: everything outside the agent.

### Cycle
```
   Environment ── stimulus ──> Agent ── action ──> Environment'
              ^                                            │
              └────────────────  feedback  ────────────────┘
```

### Jane Goodall reference
- Anthropologist / primatologist (1934–).
- Studied chimpanzees → showed they make tools, have emotions, behave like simple agents.
- The lecture's point: **agency exists on a spectrum** — cells, animals, humans, computers.

### Koko the gorilla
- Sign language–trained gorilla. Demonstrated *communication*, *concept formation*.
- → Sign language = a set of symbols = words = logos = information.

### Agent in game theory
- **Players** = agents.
- **Umpires** = referees / "high priests" who enforce rules.
- **Rules** = words (logos) = information that defines valid actions.
- **Game** = environment + rules + agents + reward/penalty function.

**Exam angle:** Define agent. Distinguish agent vs object. Give examples at different scales (cell, human, AI).

---

## 6.2 LLMs, GPT, Attention

**Your notes:** LLM, attention mechanism + trained, GPT = Generative Pretrained Transformer, "Attention is All You Need", reinforcement learning.

**Enriched:**

### Transformer architecture
- Paper: **"Attention is All You Need"** (Vaswani et al., Google, 2017). ← read this title.
- Replaced RNNs (LSTM, GRU) for most NLP tasks.
- Core idea: **self-attention** — each token can attend to every other token in the sequence.

### Attention
- For each input position, compute weights (attention scores) over all other positions → weighted sum.
- Allows long-range dependencies (vs RNN, which forgets).
- Multi-head: multiple attention "heads" capture different relationships.

### GPT (Generative Pretrained Transformer)
- OpenAI, 2018+.
- **G**enerative: produces text.
- **P**retrained: trained on huge corpus of text (unsupervised).
- **T**ransformer: uses attention.
- Decoder-only transformer.
- Models: GPT-2 (2019), GPT-3 (2020), GPT-4 (2023), …

### Reinforcement Learning from Human Feedback (RLHF)
- After pretraining: fine-tune with human ratings.
- Reward when correct/aligned, punish when wrong/misaligned.
- Used in ChatGPT, Claude, Gemini.

### LLM "intelligence"
- Pattern matching on massive scale.
- Emergent behavior at scale.
- Limitations: hallucination, no real understanding (Chinese Room argument applies).

**Exam angle:** What is attention? What does GPT stand for? Name one big AI paper.

---

## 6.3 Ant Colonies & Swarm Intelligence

**Your notes:** ant colonies problem, low diversity (single mom = queen), simple agents, hive mentality, China analogy.

**Enriched:**
- **Ant colony**: thousands of simple agents (workers), single reproducing queen.
- **Low genetic diversity** → vulnerable to environmental change.
- But: **emergent intelligence** through collective behavior (pheromone trails, division of labor).
- → Inspired **ACO** algorithm (Ant Colony Optimization).
- "Hive mentality" — agents acting in coordination without central control.

**Why "China" reference:** he's making a sociological analogy — large coordinated populations can act swarm-like.

**Exam angle:** Explain swarm intelligence with an example.

---

# PART VII — BIOLOGY & COGNITION

## 7.1 LUCA & Evolution

**Your notes:** LUCA = Last Universal Common Ancestor, first life forms, fossils, water, Euglena verde, chlorophyll, chloroplast.

**Enriched:**

### LUCA
- The most recent organism that all current life on Earth descended from.
- Lived ~3.5–4 billion years ago.
- Likely a prokaryote (no nucleus).

### Early life
- First fossils: stromatolites (cyanobacteria).
- **Euglena viridis**: single-celled aquatic organism, has chlorophyll (photosynthesizes) but can also eat (animal-like).
- Chlorophyll in chloroplasts: information system — converts light + nutrients to energy.

### Cell as info system
- DNA stores info (genes A-T-G-C).
- RNA carries info to ribosomes.
- Proteins are the output (do work).
- All this is **information processing**.

### Darwin's evolution
- **Charles Darwin** (1809–1882). *On the Origin of Species* (1859).
- Mechanisms: variation, inheritance, selection, time.
- "Only the fit survive."
- Modern synthesis: + Mendel's genetics.

### Gregor Mendel
- Augustinian friar (1822–1884).
- Pea plant experiments → laws of inheritance.
- Discovered units of heredity (later called genes).

**Exam angle:** What is LUCA? What is the relationship between biology and AI? (Answer: evolution → evolutionary algorithms; neurons → neural networks; swarm behavior → swarm algorithms; cells as info processors → agents.)

---

## 7.2 The Cell as the First Agent

**Your notes:** ENVIRONMENT → STIMULI → reaction, food = positive stimuli, death = negative, "should I stay or should I go?", flagellus.

**Enriched:**

### The cell's decision loop
1. **Sense** environment (chemical stimuli via biochemistry → ions → membrane changes).
2. **Decide** based on stored info (genetic + epigenetic).
3. **Act**: eat, reproduce, move (flagellum), fight or flight.

### Categories of stimuli
- **Positive (++)**: food, sexual partner.
- **Negative (−−)**: predator, toxin.

### Cell-to-cell communication
- Plants: through roots (mycorrhizal networks).
- Animals: chemicals, hormones, nervous signals.
- Cells in colony: share food, signal danger.

### The "song" mnemonic
Prof. literally quotes The Clash:
> *"Should I stay or should I go?"* — the question every cell (and every agent) asks.

**Exam angle:** Why is the cell considered the "first agent"? Connect to AI agent definition.

---

## 7.3 Consciousness & Ethics

**Your notes:** consciousness = science of self, where is consciousness stored?, soul/spirit, ethics, Descartes "cogito ergo sum".

**Enriched:**

### Where is consciousness stored?
- **Neurons** store information (chemical + electrical).
- But: no specific "consciousness center" found.
- Competing theories: Global Workspace Theory, Integrated Information Theory (IIT), Higher-Order Thought, etc.
- **Open question** — the "hard problem" of consciousness (Chalmers).

### Descartes' "cogito"
- **Dubito ergo cogito** ("I doubt, therefore I think")
- **Cogito ergo sum** ("I think, therefore I am")
- Foundation of modern epistemology.
- Implication for AI: does an AI that "thinks" therefore "exist"?

### Ethics
- Greek *ηθική* = "character".
- The branch of philosophy concerning right/wrong.
- AI ethics: bias, fairness, accountability, safety, alignment.

### The future
- A star **might** exhibit consciousness (he says this — pure speculation).
- Anything made of atoms can, in principle, be intelligent — *given enough complexity*.

**Exam angle:** What is consciousness? Where is it stored? (Honest answer: we don't know — but be ready to discuss the question.)

---

## 7.4 Free Will

**Your notes:** "WILL" (circled), free will, agents have will, objects don't.

**Enriched:**

### What is free will?
- The capacity to choose between possible actions.
- Compatibilist vs. libertarian vs. determinist views.
- Required for moral responsibility.

### In AI
- AI systems make "choices" based on inputs + weights.
- Are these choices "free"? No (deterministic given seed).
- Stochastic AI (random sampling) introduces non-determinism but not "freedom" in the philosophical sense.

### In biology
- Even simple cells "choose" based on stimuli + internal state.
- Where does free will begin? Open question.

**Exam angle:** Distinguish agent vs object using will. Discuss whether AI has free will.

---

# APPENDICES (RECAP CONNECTIONS)

## A. Algorithm Examples by Paradigm

| Algorithm | Paradigm | Complexity | Used For |
|-----------|----------|------------|----------|
| Brute-force closest pair | Brute force | O(n²) | Geometry |
| D&C closest pair | Divide & Conquer | O(n log n) | Geometry |
| FFT (Cooley-Tukey) | Divide & Conquer | O(n log n) | Polynomial mult, signal processing |
| Brute polynomial mult | Brute force | O(n²) | Polynomial mult |
| Quake fast inv sqrt | Bit manipulation + Newton | O(1) | Computer graphics |
| Newton's method | Iterative numerical | O(log log ε) | Root finding |
| Dijkstra | Greedy + DP | O((V+E) log V) | Shortest path |
| Needleman-Wunsch | DP | O(m·n) | Seq. alignment |
| ID3 Decision Tree | Greedy | depends | Classification |
| Fuzzy DT | Greedy + fuzzy | depends | Continuous data |
| Hill climbing | Greedy local | depends | Optimization (baseline) |
| Tabu Search | Local + memory | depends | TSP, scheduling |
| Simulated Annealing | Stochastic | depends | TSP, VLSI |
| Genetic Algorithm | Evolutionary | depends | TSP, scheduling, design |
| PSO | Swarm | depends | Continuous opt. |
| ACO | Swarm | depends | TSP, routing |

## B. Key Names & Years (memorize 8–10)

- ~825: **Al-Khwarizmi** (algorithm, algebra)
- 384 BC: **Aristotle** (logic)
- 1596: **Descartes** (Cartesian coordinates)
- 1815: **Lovelace** (first programmer) / Boole (born this year too)
- 1844: **Boltzmann** (statistical mechanics, entropy)
- 1879: **Einstein** (E=mc²)
- 1903: **von Neumann** (computer architecture)
- 1912: **Turing** (Turing machine, test, halting)
- 1916: **Shannon** (information theory)
- 1928: **Rosenblatt** (perceptron)
- 1934: **Goodall** (chimpanzee → agent concept)
- 2017: **Vaswani et al.** ("Attention is All You Need")

## C. Formulas to Memorize

```
Shannon entropy:    H = -Σ pᵢ log₂ pᵢ
Boltzmann entropy:  S = k_B · ln W
Sigmoid:            σ(x) = 1/(1+e^-x);  σ'(x) = σ(1-σ)
tanh:               tanh(x) = (e^x - e^-x)/(e^x + e^-x)
Perceptron:         σ = f(Σ wᵢxᵢ + b)
Gradient descent:   w ← w - η · ∂E/∂w
Squared error:      E = ½(σ - y)²
Backprop (1-layer): ∂E/∂wᵢ = (σ-y) · σ(1-σ) · xᵢ
Newton's method:    x_{k+1} = x_k - f(x_k)/f'(x_k)
Euclidean dist:     d = √Σ(xᵢ - yᵢ)²
Hamiltonian cycle:  closed loop visiting each vertex exactly once
F = m·a (Newton)
E = m·c² (Einstein)
```

## D. The Professor's One-Sentence Definitions

- **Algorithm** = finite succession of steps that solves a problem.
- **Problem** = finite succession of input + output variables.
- **Program** = data + code (= a finite succession of instructions).
- **Informatics** = science of solving problems with minimum energy / steps.
- **Intelligence** = flow of information from beginning to end.
- **Bit** = unit of information.
- **Code** = bijection between meaning and representation.
- **Agent** = entity that models environment, has rules, has will.
- **Object** = entity with no will.
- **Search** = finding x = (x₁,...,xₙ) such that x is a solution.

---

Good luck, Anda! Trace the ideas, not just the formulas.
