# CHEAT SHEET — Print This Page

> **Use this in the last 24 hours before the exam.** If you can recite this from memory you're ready.

---

## THE FOUR DEFINITIONS (memorize verbatim)

| Term | Definition |
|------|------------|
| **Algorithm** | Finite succession of steps that solves a problem |
| **Problem** | Finite succession of input + output variables |
| **Program** | Data + Code (finite succession of instructions) |
| **Informatics** | Science of solving problems with minimum energy (min steps) |
| **Agent** | Entity that models environment, has rules, has will |
| **Intelligence** | Flow of information from beginning to end |

---

## ENTROPY — THE CORE FORMULAS

```
Shannon (information):    H = -Σᵢ pᵢ · log₂ pᵢ            [bits]
Boltzmann (mechanics):    S = k_B · ln W                    [J/K]
Multinomial W:            W = N! / (n₁! · n₂! · ... · n_k!)
Stirling approx:          ln N! ≈ N·ln N - N
```

- **Max entropy** = uniform distribution
- **Zero entropy** = certain event (p=1)
- **CMB** = max-entropy structure in cosmos

---

## NEURAL NETWORK QUICK-REF

### Activation functions
```
Step:       f(x) = 1 if x≥0 else 0          (not differentiable)
Sigmoid:    σ(x) = 1/(1+e^-x)                ∈ (0,1)
Sigmoid':   σ'(x) = σ(x)·(1-σ(x))            
tanh:       (e^x - e^-x)/(e^x + e^-x)        ∈ (-1,1)
ReLU:       max(0, x)                        modern default
Trapezoid:  piecewise linear, robust to noise
```

### Perceptron + backprop (squared error, sigmoid)
```
a = w₀·x₀ + w₁·x₁ + b
σ = f(a) = 1/(1+e^-a)
E = ½(σ - y)²

∂E/∂w₀ = (σ - y) · σ(1-σ) · x₀
∂E/∂w₁ = (σ - y) · σ(1-σ) · x₁

Update:  w ← w - η · ∂E/∂w     (η ∈ (0,1) = learning rate)
∇E = [∂E/∂w₀, ∂E/∂w₁]
```

### Chain rule path
```
∂E/∂w = ∂E/∂σ · ∂σ/∂a · ∂a/∂w
      = (σ-y)  · σ(1-σ) ·  x
```

---

## ALGORITHM PARADIGMS

| Paradigm | Strategy | Example | Lab |
|----------|----------|---------|-----|
| Brute force | Try all | Closest pair O(n²), TSP all perms | ✓ |
| Backtracking | DFS + prune | N-queens, decision trees | ✓ |
| Divide & Conquer | Split + recurse | FFT, closest-pair O(n log n) | ✓ |
| Greedy | Best local | Dijkstra, nearest-neighbor | ✓ |
| Dynamic Prog | Cache subproblems | Needleman-Wunsch | ✓ |
| Heuristic | Educated guess | Hill climbing, Tabu | ✓ |
| Stochastic | Randomness | SA, GA, PSO, ACO | ✓ |

---

## SEARCH

```
Exhaustive   = guaranteed optimum, slow      (BFS, DFS, brute force)
Heuristic    = uses domain knowledge          (A*, hill climb, Tabu)
Stochastic   = uses randomness                (SA, GA, swarm)

BFS = queue, finds shortest in edges
DFS = stack/recursion, low memory

Complexity (brute):  O(∏ |Dᵢ|)  (product of domain sizes)
```

---

## NUMBER SYSTEMS

```
ℕ ⊆ ℤ ⊆ ℚ ⊆ ℝ ⊆ ℂ

|ℕ| = |ℤ| = |ℚ| = ℵ₀   (countably infinite)
|ℝ| = 𝔠 = 2^ℵ₀          (uncountable, Cantor diagonal)

Float = [sign | exponent | mantissa]
        1b      8b/11b     23b/52b
```

---

## SETS, RELATIONS, FUNCTIONS

```
Cartesian product:  A × B = {(a,b) | a∈A, b∈B}
{0,1} × {0,1} = {(0,0), (0,1), (1,0), (1,1)}   ← 2-bit truth table

Relation R ⊆ A × B  (any subset of Cartesian product)
Function f: A → B  (relation where each a has exactly one b)
Bijective f         (one-to-one AND onto, has inverse)
                     → can serve as a CODE (encode/decode)
```

---

## TSP & METAHEURISTICS

```
TSP: shortest Hamiltonian cycle in weighted complete graph
Search space: (n-1)!/2 tours
NP-hard.  Berlin52 optimum = 7542

Hill climbing → can get stuck (local optimum)
Tabu Search:    + memory of recent moves (forbidden)
                + aspiration: override if beats global best
Simulated Annealing: accept worse with P = exp(-ΔE/T)
                     T = T·α, α ∈ [0.99, 0.9999]
Genetic Algorithm:   population, fitness, selection, crossover (OX), mutation
PSO: particles remember personal + global best
ACO: pheromone trails, shorter paths reinforced
```

---

## KEY PEOPLE — ONE-LINERS

| Year | Who | What |
|------|-----|------|
| ~825 | **Al-Khwarizmi** | "Algorithm" comes from his name; founded algebra |
| 384 BC | **Aristotle** | Formal logic (laws of thought) |
| 1596 | **Descartes** | Cartesian coords (fly-on-ceiling story); cogito ergo sum |
| 1815 | **Lovelace** | First algorithm (Bernoulli numbers, for Babbage) |
| 1791 | **Babbage** | Analytical Engine (designed, not built) |
| 1854 | **Boole** | Algebraic form of Aristotelian logic |
| 1844 | **Boltzmann** | Statistical entropy S = k·ln W |
| 1879 | **Einstein** | E = m·c²; light = photons |
| 1903 | **von Neumann** | Computer architecture (CPU + memory + I/O) |
| 1912 | **Turing** | Turing machine, test, halting problem |
| 1916 | **Shannon** | Information theory (Bell Labs, 1948) |
| 1928 | **Rosenblatt** | Perceptron (Mark I, Cornell, 1958) |
| 1822 | **Mendel** | Inheritance (pea plants) |
| 1809 | **Darwin** | Evolution by natural selection |
| 1934 | **Goodall** | Chimpanzee studies → agency concept |
| 2017 | **Vaswani et al.** | "Attention is All You Need" (Transformer) |

---

## THE FOUR DICHOTOMIES (he loves these)

| ←──── | ────→ |
|-------|-------|
| **Continuous** (waves, ℝ, sigmoid, regression) | **Discrete** (particles, ℤ, step, classification) |
| **Abstract** (algorithm, step, idea) | **Concrete** (program, instruction, implementation) |
| **Local** (greedy, hill climb) | **Global** (brute force, exhaustive) |
| **Exhaustive** (brute) | **Heuristic** vs. **Stochastic** |

---

## PHILOSOPHY → AI PIPELINE

```
Idea ─ Philosophy ─ Logic ─ Math ─ Algebra ─ Informatics ─ AI ─ ?
       Socrates    Aristotle Pythagoras Al-Khwarizmi Boole/Turing today
```

---

## DECISION TREE / ID3

```
1. Compute H(S)  [entropy of current subset]
2. For each attr A:  IG(S, A) = H(S) - Σ (|Sᵥ|/|S|) · H(Sᵥ)
3. Pick attr with max IG → split
4. Recurse on each branch
5. Stop: pure subset / no attrs / min samples

Fuzzy DT (prof's PhD):
  - Replace hard splits with triangular memberships
  - Fuzzy entropy uses membership-weighted counts
  - Instance flows down multiple branches with different degrees
```

---

## CELL = FIRST AGENT

```
Environment ── stimuli (+/−) ──→ Cell
                                  │
                                  ├── eat / move / reproduce / fight or flight
                                  │
                                  └── "should I stay or should I go?"
```

Positive stimuli (++): food, sexual partner
Negative stimuli (−−): predator, toxin

---

## LLM / GPT QUICK FACTS

- **GPT** = Generative Pretrained Transformer
- Paper: **"Attention is All You Need"** (Vaswani et al., 2017)
- Architecture: Transformer (encoder-decoder; GPT = decoder-only)
- Key mechanism: **self-attention** (each token attends to all others)
- Training: pretrain on huge text + **RLHF** (reinforcement learning from human feedback)

---

## ONE-LINE ANSWERS

| If asked... | Say... |
|-------------|--------|
| What is AI? | Building agents that exhibit flow of information from input to decision |
| What is entropy? | Measure of disorder/uncertainty (Boltzmann in physics, Shannon in info) |
| What is an algorithm? | A finite succession of steps that solves a problem (from Al-Khwarizmi) |
| Why XOR matters? | Not linearly separable → forced invention of multilayer networks |
| Why is TSP hard? | NP-hard; brute force is O(n!); use metaheuristics |
| What is gradient descent? | Iterative w ← w − η · ∇E to minimize loss |
| What is overfitting? | Model memorizes training, fails on test. Fix: regularize, more data, early stop |
| What is an agent? | Models env + has rules + has will (objects have none) |
| Boole = ? | Aristotelian logic in algebraic form |
| Shannon = ? | Information theory (1948) — bit, entropy of info |
| LUCA = ? | Last Universal Common Ancestor (~4 Gya) |
| CMB = ? | Cosmic Microwave Background — max-entropy relic of Big Bang |

---

## FINAL MANTRA

> **Intelligence is the flow of information from a beginning to an end. Philosophy gave the idea, logic the rules, math the language, biology the example, algorithms the implementation. Every algorithm is a finite succession of steps. AI is the formal study of building agents that exhibit this flow.**
