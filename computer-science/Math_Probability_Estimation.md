# Math, Probability, and Estimation -- Comprehensive Interview Reference

> An interview-focused reference for the "math round" that shows up in Google/Meta generalist loops, quant-adjacent and HPC teams, and ML-infra capacity discussions. It covers counting, probability, expectation tricks, a distributions cheat sheet, statistics for engineers who benchmark things, 33 classic puzzles with full solutions, runnable Monte Carlo checks, Fermi estimation with eight worked examples, and the handy numbers you should know cold. It complements *DSA Fundamentals* (algorithms), *High Level Design* (capacity math), and *Performance Engineering* (measurement).

---

## Table of Contents

1. [How to Approach Math and Probability Questions](#1-how-to-approach-math-and-probability-questions)
2. [Counting and Combinatorics](#2-counting-and-combinatorics)
3. [Probability Fundamentals](#3-probability-fundamentals)
4. [Expectation, Variance, and Indicator Variables](#4-expectation-variance-and-indicator-variables)
5. [Distributions Cheat Sheet](#5-distributions-cheat-sheet)
6. [Statistics for Engineers](#6-statistics-for-engineers)
7. [Classic Probability Puzzles](#7-classic-probability-puzzles)
8. [Monte Carlo Simulation Toolkit](#8-monte-carlo-simulation-toolkit)
9. [Fermi Estimation](#9-fermi-estimation)
10. [Powers of Two and Handy Numbers](#10-powers-of-two-and-handy-numbers)
11. [Quick Reference](#11-quick-reference)

---

## 1. How to Approach Math and Probability Questions

Interviewers rarely care whether you remember a formula. They want to see whether you can **define the sample space precisely**, pick a technique that fits, and **sanity-check** the answer. A wrong answer with a clean method and a self-caught error often scores better than a memorized right answer with no reasoning.

### 1.1 A repeatable process

1. **Restate and pin down the randomness.** "Uniformly at random over what?" Many paradoxes (Bertrand's chord, boy-girl, Monty Hall) are entirely about an under-specified random process.
2. **Try a tiny case by hand.** n = 1, 2, 3. Enumerate outcomes. This often reveals the pattern and catches off-by-one errors.
3. **Choose a technique:**

| Signal in the question | Technique to reach for |
|---|---|
| "How many ways ..." | Product rule, permutations/combinations, stars and bars, bijection |
| "At least one ..." | Complement: 1 - P(none) |
| "None of ... / exactly k ... with overlaps" | Inclusion-exclusion |
| "Expected number of ..." | Linearity of expectation with indicator variables |
| "Expected time / steps until ..." | First-step analysis (condition on the first move, write a recurrence) |
| "Given that ... what is the probability ..." | Bayes; draw a tree or use natural frequencies |
| "Optimal strategy / when to stop" | Backward induction (dynamic programming over states) |
| Geometry with uniform points | Draw the region; probability = area ratio |
| Hard to compute exactly | Symmetry argument, or say "I would verify with a Monte Carlo simulation" |

4. **Sanity-check.** Is the probability in [0, 1]? Does it go the right direction as parameters change? Does it match the n = 2 case? Does a quick simulation agree?
5. **Say the answer as a number** (fraction and decimal), then mention generalizations.

### 1.2 Common pitfalls

| Pitfall | Example | Fix |
|---|---|---|
| Treating dependent events as independent | P(two cards both aces) = (4/52)^2 | Use conditional: (4/52)(3/51) |
| Double counting | Counting committees with "pick a leader then others" when roles do not matter | Divide by the overcount, or count unordered objects directly |
| Confusing P(A given B) with P(B given A) | "The test is 99% accurate, so a positive means 99% sick" | Bayes with the base rate |
| Assuming "uniform" without stating over what | Random chord of a circle | Define the generating process explicitly |
| Averaging ratios or percentiles | Average of per-server p99 latencies | Aggregate raw data or histograms, then compute |
| Forgetting the complement shortcut | P(at least one 6 in 4 rolls) by summing cases | 1 - (5/6)^4 |

**See also:** [High Level Design: Estimate the Workload](High_Level_Design.md#3-estimate-the-workload) for capacity-estimation formulas, and [Performance Engineering: Roofline Model](Performance_Engineering.md#3-roofline-model) for estimation applied to kernels.

---

## 2. Counting and Combinatorics

### 2.1 The two basic rules

- **Product rule:** if a task is a sequence of independent choices with n1, n2, ..., nk options, there are n1 * n2 * ... * nk outcomes. Example: 8-character passwords over 62 alphanumerics: 62^8 ≈ 2.18 × 10^14.
- **Sum rule:** if outcomes fall into disjoint cases, add the counts of each case.

Most counting mistakes come from applying the product rule when the "choices" are not actually distinct (overcounting) or when cases overlap (use inclusion-exclusion instead of the sum rule).

### 2.2 Permutations and combinations

| Object | Order matters? | Repetition? | Count | Example |
|---|---|---|---|---|
| Permutation of n items | Yes | No | n! | Orderings of 5 tasks: 120 |
| k-permutation | Yes | No | P(n,k) = n!/(n-k)! | Gold/silver/bronze from 10 runners: 720 |
| Sequence with repetition | Yes | Yes | n^k | 4-digit PINs: 10^4 |
| Combination | No | No | C(n,k) = n!/(k!(n-k)!) | 5-card hands: C(52,5) = 2,598,960 |
| Multiset (combination with repetition) | No | Yes | C(n+k-1, k) | 3 scoops from 10 flavors: C(12,3) = 220 |
| Multiset permutation | Yes | Fixed counts | n!/(n1! n2! ... nr!) | Arrangements of MISSISSIPPI |
| Circular arrangement | Rotations equal | No | (n-1)! | 6 people at a round table: 120 |
| Necklace (rotations and flips equal), distinct beads | -- | No | (n-1)!/2 for n ≥ 3 | 6 distinct beads: 60 |

**Worked: MISSISSIPPI.** 11 letters: M×1, I×4, S×4, P×2. Arrangements = 11!/(1! 4! 4! 2!) = 39,916,800 / 1,152 = **34,650**. Why divide: swapping two identical S's gives the same string, so each distinct string was counted 4! times for the S's, 4! for the I's, 2! for the P's.

**Useful identities:**

| Identity | Why it is true (combinatorial argument) |
|---|---|
| C(n,k) = C(n, n-k) | Choosing who is in equals choosing who is out |
| C(n,k) = C(n-1,k-1) + C(n-1,k) (Pascal) | Either item n is chosen or it is not |
| Σ_k C(n,k) = 2^n | Each item is in or out of a subset |
| Σ_k C(m,k) C(n,r-k) = C(m+n, r) (Vandermonde) | Choose r from two groups, split by how many come from the first |
| k C(n,k) = n C(n-1,k-1) | Choose a committee and its chair, in two orders |
| Lattice paths from (0,0) to (m,n) with right/up steps = C(m+n, n) | Choose which of the m+n steps are "up" |

**Worked: poker full house.** Choose the rank for the triple (13), its 3 suits (C(4,3) = 4), the rank for the pair (12 remaining), its 2 suits (C(4,2) = 6): 13 × 4 × 12 × 6 = **3,744** hands. P = 3,744 / 2,598,960 ≈ **0.144%**.

**Worked: committee with at least one woman.** 4 women, 6 men, choose 4. Total C(10,4) = 210; all-men C(6,4) = 15; answer **195**. The tempting wrong answer "pick 1 woman (4 ways) then any 3 of the remaining 9 (84)" = 336 overcounts committees with multiple women.

### 2.3 Stars and bars

The number of ways to write n as an ordered sum of k **non-negative** integers (x1 + ... + xk = n, xi ≥ 0) is

```text
C(n + k - 1, k - 1)
```

Picture n stars and k-1 bars in a row of n+k-1 slots; choosing the bar positions determines every xi. If each xi ≥ 1, give each variable one star first: C(n - 1, k - 1).

| Problem | Translation | Answer |
|---|---|---|
| Distribute 10 identical GPUs across 3 jobs (a job may get 0) | x1+x2+x3 = 10, xi ≥ 0 | C(12,2) = 66 |
| Same, each job gets at least 1 | xi ≥ 1 | C(9,2) = 36 |
| Number of monomials of degree 4 in 3 variables | exponents sum to 4 | C(6,2) = 15 |
| Outcomes when rolling 3 identical dice (multisets) | counts of each face sum to 3, 6 faces | C(8,5) = 56 |
| Each job gets at most 4 of the 10 | upper bounds -> inclusion-exclusion (below) | 6 |

**Worked: upper bounds with inclusion-exclusion.** Count x1+x2+x3 = 10 with 0 ≤ xi ≤ 4.
- All non-negative solutions: C(12,2) = 66.
- Solutions with x1 ≥ 5: substitute y1 = x1 - 5, so y1+x2+x3 = 5: C(7,2) = 21. Three variables: 3 × 21 = 63.
- Two variables both ≥ 5: remaining sum 0: C(2,2) = 1 each, 3 pairs: 3.
- All three ≥ 5: sum would be -5, impossible: 0.
- Answer: 66 - 63 + 3 - 0 = **6**. Check by listing: permutations of (4,4,2) and (4,3,3), 3 each.

### 2.4 Inclusion-exclusion

```text
|A ∪ B| = |A| + |B| - |A ∩ B|
|A ∪ B ∪ C| = |A| + |B| + |C| - |A∩B| - |A∩C| - |B∩C| + |A∩B∩C|
General: |A1 ∪ ... ∪ An| = Σ|Ai| - Σ|Ai∩Aj| + Σ|Ai∩Aj∩Ak| - ... + (-1)^(n+1)|A1∩...∩An|
```

**Worked: integers in 1..100 divisible by 2, 3, or 5.** 50 + 33 + 20 - 16 (by 6) - 10 (by 10) - 6 (by 15) + 3 (by 30) = **74**.

**Worked: derangements** (permutations with no fixed point; "hat check" problem). Let Ai be "item i is fixed". |Ai1 ∩ ... ∩ Aik| = (n-k)!. So

```text
D(n) = n! - C(n,1)(n-1)! + C(n,2)(n-2)! - ... = n! Σ_{k=0..n} (-1)^k / k!  ≈ n!/e
Recurrence: D(n) = (n-1)(D(n-1) + D(n-2)),  D(1) = 0, D(2) = 1
Values: D(3)=2, D(4)=9, D(5)=44, D(6)=265, D(7)=1854
```

The probability a random permutation is a derangement tends to 1/e ≈ 0.3679 very quickly (already 0.3681 at n = 6).

**Worked: surjections.** The number of onto functions from an n-set to a k-set is Σ_{j=0..k} (-1)^j C(k,j) (k-j)^n. Example: assign 5 distinct jobs to 3 machines so every machine gets at least one: 3^5 - 3·2^5 + 3·1^5 = 243 - 96 + 3 = **150**.

### 2.5 Pigeonhole principle

If n+1 objects go into n boxes, some box holds at least 2. Generalized: some box holds at least ⌈N/n⌉.

| Problem | Pigeons -> holes | Conclusion |
|---|---|---|
| Socks: 10 black, 10 white in the dark, how many to guarantee a pair? | socks -> 2 colors | 3 |
| Among 367 people, two share a birthday | people -> 366 days | Guaranteed (contrast with the 23-person *probabilistic* result) |
| 5 points in a unit square: two are within √2/2 | points -> four 1/2 × 1/2 sub-squares | Two points share a sub-square whose diagonal is √2/2 |
| Any n+1 numbers from {1, ..., 2n}: one divides another | numbers -> odd part (n possible odd parts) | Two numbers with the same odd part differ by a power of 2, so one divides the other |
| No lossless compressor shrinks every input | 2^n inputs of length n -> 2^n - 1 shorter strings | Some input must not shrink |
| A hash from 64-bit keys to 32-bit values collides | 2^64 keys -> 2^32 buckets | Collisions are inevitable; design for them |
| Any sequence of n^2+1 distinct numbers has a monotone subsequence of length n+1 (Erdős-Szekeres) | each element -> (longest increasing ending here, longest decreasing ending here) | If both ≤ n there are only n^2 labels, but labels are distinct |

### 2.6 Catalan numbers

```text
C_n = C(2n, n) / (n + 1) = C(2n, n) - C(2n, n + 1)
C_0..C_10 = 1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796
Recurrence: C_0 = 1,  C_{n+1} = Σ_{i=0..n} C_i · C_{n-i}
Growth: C_n ~ 4^n / (n^{3/2} √π)
```

Catalan numbers count, for size n:
- Balanced strings of n pairs of parentheses (LeetCode 22 generates them).
- Structurally distinct binary search trees with n keys (LeetCode 96).
- Full binary trees with n+1 leaves; ways to parenthesize a product of n+1 matrices.
- Triangulations of a convex polygon with n+2 vertices.
- Monotone lattice paths from (0,0) to (n,n) that never go above the diagonal (Dyck paths).
- Stack-sortable permutations / valid push-pop sequences of n items.

**Why C(2n,n) - C(2n,n+1) (reflection argument).** Paths of n "(" and n ")" number C(2n,n). A bad path first dips to -1 at some step; reflect every step after that point ("(" ↔ ")"). The reflected path ends at -2, meaning it has n-1 "(" and n+1 ")". This is a bijection between bad paths and all paths with n+1 ")", of which there are C(2n, n+1). So good = C(2n,n) - C(2n,n+1) = C(2n,n)/(n+1).

**Why the recurrence:** the first "(" matches some ")" at position 2i+1; inside are i balanced pairs and after are n-i. Same split as "root of a BST has i nodes on the left".

### 2.7 Counting code that runs

```python
from itertools import product
from math import comb, factorial


def stars_and_bars(n: int, k: int) -> int:
    """Non-negative integer solutions to x1 + ... + xk = n."""
    return comb(n + k - 1, k - 1)


def bounded_solutions(n: int, k: int, cap: int) -> int:
    """Solutions with 0 <= xi <= cap, via inclusion-exclusion."""
    total = 0
    for j in range(k + 1):
        rest = n - j * (cap + 1)
        if rest < 0:
            break
        total += (-1) ** j * comb(k, j) * comb(rest + k - 1, k - 1)
    return total


def catalan(n: int) -> int:
    return comb(2 * n, n) // (n + 1)


def derangements(n: int) -> int:
    d = [1, 0]  # D(0) = 1, D(1) = 0
    for m in range(2, n + 1):
        d.append((m - 1) * (d[m - 1] + d[m - 2]))
    return d[n]


# Brute-force cross-checks on small inputs
brute = sum(1 for xs in product(range(11), repeat=3) if sum(xs) == 10)
assert brute == stars_and_bars(10, 3) == 66
brute_capped = sum(1 for xs in product(range(5), repeat=3) if sum(xs) == 10)
assert brute_capped == bounded_solutions(10, 3, 4) == 6
assert [catalan(i) for i in range(8)] == [1, 1, 2, 5, 14, 42, 132, 429]
assert [derangements(i) for i in range(1, 7)] == [0, 1, 2, 9, 44, 265]
assert factorial(11) // (factorial(4) ** 2 * factorial(2)) == 34650
print("all counting checks passed")
```

For nCr modulo a prime (the competitive-programming variant with 10^9+7), precompute factorials and inverse factorials using Fermat's little theorem: inv(a) = a^(p-2) mod p, computed with Python's `pow(a, p - 2, p)`.

### 2.8 Interview Questions

**Q1.** How many ways can you climb n stairs taking 1 or 2 steps, and how does this relate to counting?

The count f(n) satisfies f(n) = f(n-1) + f(n-2) (the last step is a 1 or a 2), with f(1) = 1, f(2) = 2, so f(n) = Fib(n+1). Combinatorially, a climb using j two-steps has n - j moves in total, of which you choose which j are two-steps: f(n) = Σ_j C(n-j, j). For n = 5: C(5,0) + C(4,1) + C(3,2) = 1 + 4 + 3 = 8 = Fib(6). The follow-up is usually "allow steps of size 1..k", which is the same recurrence with k terms. Computed in O(n) time with O(k) memory using a sliding window.

**Q2.** How many distinct binary search trees can be built from keys 1..n, and why?

C_n, the nth Catalan number. If key i is the root, the left subtree is a BST on keys 1..i-1 and the right on i+1..n, independently, giving T(n) = Σ_i T(i-1) T(n-i), which is the Catalan recurrence. For n = 3 there are 5; for n = 10 there are 16,796. The pitfall is to answer n! (the number of insertion orders); many insertion orders produce the same tree shape.

**Q3.** A grid is 6 wide and 4 tall. How many shortest paths go from the bottom-left to the top-right corner, and how many avoid a blocked cell at (2,2)?

Every shortest path has 6 rights and 4 ups, so C(10,4) = 210. Paths through (2,2): C(4,2) to get there × C(6,2) from there to (6,4) = 6 × 15 = 90. Avoiding: 210 - 90 = 120. With multiple blocked cells, use DP on the grid (or inclusion-exclusion over sorted obstacles, which is LeetCode-hard territory).

**Q4.** Why is pigeonhole relevant to hashing and checksums?

Any hash from a larger domain to a smaller range must have collisions, so correctness can never rely on "different inputs give different hashes". A hash table must handle collisions (chaining or probing), and checksum or content-addressed systems pick output sizes large enough that collisions are improbable (birthday bound, Section 7.2), not impossible. The same principle proves no compressor can shrink every input.

**Q5.** Count the number of ways to put 7 distinct balls into 3 distinct boxes so that no box is empty. What changes if the balls are identical?

Distinct balls: surjections, 3^7 - 3·2^7 + 3·1^7 = 2187 - 384 + 3 = 1806. Identical balls: stars and bars with each box ≥ 1, C(6,2) = 15. A common follow-up is identical boxes with distinct balls: divide the surjection count by 3! because boxes are unlabeled and all non-empty, giving 301 (the Stirling number S(7,3)).

---

## 3. Probability Fundamentals

### 3.1 Axioms and basic rules

| Rule | Formula | Note |
|---|---|---|
| Complement | P(not A) = 1 - P(A) | The fastest route for "at least one" |
| Union | P(A ∪ B) = P(A) + P(B) - P(A ∩ B) | Inclusion-exclusion |
| Union bound | P(A1 ∪ ... ∪ An) ≤ Σ P(Ai) | Tight when events rarely overlap; used constantly in algorithm analysis |
| Conditional | P(A given B) = P(A ∩ B) / P(B) | Restrict the sample space to B |
| Multiplication | P(A ∩ B) = P(A given B) P(B) | Chain rule generalizes to many events |
| Total probability | P(A) = Σ_i P(A given Bi) P(Bi) for a partition {Bi} | "Condition on the cases" |
| Bayes | P(B given A) = P(A given B) P(B) / P(A) | Flips the direction of conditioning |
| Independence | P(A ∩ B) = P(A) P(B) | Equivalent to P(A given B) = P(A) when P(B) > 0 |

**Mutually exclusive is not independent.** If A and B are disjoint with positive probability, learning that A happened tells you B did not, so they are maximally dependent.

**Pairwise independence does not imply mutual independence.** Flip two fair coins. A = "first is H", B = "second is H", C = "both coins match". Each pair is independent (P = 1/4 = 1/2 × 1/2), but P(A ∩ B ∩ C) = 1/4, not 1/8. Knowing A and B determines C. This matters for hashing: pairwise-independent hash families give weaker guarantees than fully random ones.

### 3.2 Conditional probability by enumeration

**Example.** Two dice are rolled; at least one shows a 6. What is the probability both are 6?
Outcomes with at least one 6: 11 (6 with first = 6, 6 with second = 6, minus the double-counted (6,6)). Exactly one of them is (6,6). Answer **1/11**, not 1/6. The structure is identical to the boy-girl paradox (Section 7.26).

### 3.3 Bayes' theorem with a worked false-positive example

```text
P(H given E) = P(E given H) · P(H) / [ P(E given H) · P(H) + P(E given not H) · P(not H) ]

Odds form:  posterior odds = prior odds × likelihood ratio,
            likelihood ratio LR = P(E given H) / P(E given not H)
```

**Problem.** A disease affects 1 in 1,000 people. A test has 99% sensitivity (P(positive given sick) = 0.99) and a 1% false-positive rate (P(positive given healthy) = 0.01). You test positive. What is the probability you are sick?

**Formula:**

```text
P(sick given +) = 0.99 × 0.001 / (0.99 × 0.001 + 0.01 × 0.999)
                = 0.00099 / (0.00099 + 0.00999)
                = 0.00099 / 0.01098
                ≈ 0.090  (about 9%)
```

**Natural frequencies (the clearest way to explain it out loud):** Of 100,000 people, 100 are sick and 99 of them test positive. Of the 99,900 healthy people, 1% = 999 test positive. Positives total 1,098, of which 99 are sick: 99 / 1,098 ≈ **9.0%**. The test is "99% accurate" yet a positive is wrong 91% of the time, because healthy people vastly outnumber sick ones.

**Odds form:** prior odds 1 : 999. LR = 0.99 / 0.01 = 99. Posterior odds 99 : 999 ≈ 1 : 10.1, so P ≈ 99/1098 ≈ 9.0%.

**Follow-up: test again (independently) and it is positive again.** Prior odds are now 99 : 999. Multiply by LR 99 again: 9,801 : 999, so P = 9801 / 10800 ≈ **90.75%**. Each independent positive multiplies the odds by 99. The independence assumption is the weak point: if the false positive is caused by something persistent (a cross-reacting antibody, a deterministic bug), a repeat test adds almost no information.

**Engineering version: alert precision.** A performance-regression detector fires on 1% of good commits (false-positive rate) and catches 95% of real regressions. Real regressions are 1 in 200 commits. Precision = 0.95 × 0.005 / (0.95 × 0.005 + 0.01 × 0.995) = 0.00475 / 0.014700 ≈ **32%**. Two out of three pages are false alarms, which is why alert design focuses on false-positive rate when base rates are low, and why requiring confirmation on a re-run (if noise is independent between runs) is so effective.

### 3.4 Independence in practice

| Scenario | Independent? | Why it matters |
|---|---|---|
| Two disks in the same chassis failing | Not fully: shared power, heat, firmware batch | RAID/replication math assuming independence underestimates correlated loss |
| Successive benchmark runs on the same node | Often not: thermal state, frequency boost, cache warmth | Treat runs as a time series; randomize order; use warm-up |
| Hash values of distinct keys under a good hash | Approximately | Basis of expected O(1) hash-table operations |
| Pseudo-random numbers from one seeded generator | Deterministic but designed to look independent | Fine for simulation; use a CSPRNG for security |
| Requests from the same user | No | Per-user rate limits; heavy-tailed workloads |

### 3.5 Interview Questions

**Q1.** You draw two cards from a standard deck without replacement. What is the probability that the second card is an ace?

1/13. By symmetry, before you look at anything, every position in a shuffled deck is equally likely to hold any card, so the second card is an ace with probability 4/52. Explicitly by total probability: (4/52)(3/51) + (48/52)(4/51) = (12 + 192)/2652 = 204/2652 = 1/13. Interviewers use this to check whether you reach for symmetry before brute-force conditioning.

**Q2.** Explain why a "99% accurate" test can give mostly false positives.

Accuracy describes P(result given condition), but the patient needs P(condition given result). Bayes says the posterior depends on the base rate. When the condition is rare (1 in 1,000), the 1% of healthy people who falsely test positive (about 999 per 100,000) swamp the true positives (99 per 100,000), giving roughly 9% precision. The fix is a higher prior (test only symptomatic people), a lower false-positive rate, or independent confirmatory tests, each multiplying odds by the likelihood ratio.

**Q3.** P(A) = 0.6, P(B) = 0.5, P(A ∪ B) = 0.8. Are A and B independent?

P(A ∩ B) = 0.6 + 0.5 - 0.8 = 0.3 = 0.6 × 0.5, so yes. A useful follow-up: then A and not-B are also independent: P(A ∩ not B) = 0.6 - 0.3 = 0.3 = 0.6 × 0.5.

**Q4.** A fleet has 1,000 nodes; each fails independently on a given day with probability 0.001. What is the probability that at least one fails? What if failures are correlated?

1 - 0.999^1000 ≈ 1 - e^-1 ≈ 0.632. The expected number of failures is 1 and the count is approximately Poisson(1). If failures are correlated (shared rack power, a bad kernel driver rollout), the expected count is unchanged by linearity, but the variance rises: there are more days with zero failures and more days with many simultaneous failures. Capacity and replication plans must be sized for the tail, not the mean, which is why placement spreads replicas across failure domains.

**Q5.** What is the difference between P(A given B) and P(A and B)? Give an example where confusing them matters.

P(A and B) is the probability both happen in the whole sample space; P(A given B) renormalizes to the world where B happened: P(A and B)/P(B). Example: P(a request is slow and hits shard 7) might be 0.1%, but P(slow given shard 7) might be 20% if shard 7 gets 0.5% of traffic. Looking at the joint hides that shard 7 is the problem; conditioning reveals it. This is exactly how latency dashboards should be sliced.

---

## 4. Expectation, Variance, and Indicator Variables

### 4.1 Definitions

```text
E[X]      = Σ x · P(X = x)            (discrete)      = ∫ x f(x) dx   (continuous)
Var(X)    = E[(X - E[X])^2] = E[X^2] - (E[X])^2
SD(X)     = sqrt(Var(X))
Cov(X,Y)  = E[XY] - E[X]E[Y]
Var(X+Y)  = Var(X) + Var(Y) + 2 Cov(X,Y)
Var(aX+b) = a^2 Var(X)

Tail-sum formula for non-negative integer X:  E[X] = Σ_{k≥1} P(X ≥ k)
Law of total expectation:                      E[X] = E[ E[X given Y] ] = Σ_y E[X given Y=y] P(Y=y)
```

**Example: one fair die.** E = 3.5. E[X^2] = (1+4+9+16+25+36)/6 = 91/6. Var = 91/6 - 12.25 = 35/12 ≈ 2.917.

### 4.2 Linearity of expectation

**E[X1 + X2 + ... + Xn] = E[X1] + ... + E[Xn] always, even when the Xi are dependent.** This single fact solves a large fraction of interview "expected number of ..." questions. Variance is additive only for uncorrelated (for example, independent) variables.

**The indicator trick.** Write the count you care about as a sum of indicators Ii = 1 if "event i happens" else 0. Then E[Ii] = P(event i) and E[count] = Σ P(event i). You never need the joint distribution.

| Question | Indicator | Answer |
|---|---|---|
| Expected fixed points of a random permutation of n | Ii = 1 if π(i) = i, P = 1/n | n · 1/n = **1** (for every n) |
| Expected inversions in a random permutation | Iij = 1 if pair (i < j) is out of order, P = 1/2 | **n(n-1)/4** (the average-case cost of insertion sort) |
| Expected left-to-right maxima ("new records") in a random order | Ii = 1 if element i is the max of the first i, P = 1/i | **H_n ≈ ln n + 0.577** (how often a running max is updated) |
| Expected colliding pairs when hashing n keys into m buckets | Iij = 1 if keys i, j collide, P = 1/m | **C(n,2)/m** |
| Expected empty buckets | Ib = 1 if bucket b is empty, P = (1 - 1/m)^n | **m(1 - 1/m)^n ≈ m e^(-n/m)** (n = m gives ~36.8% empty) |
| Expected distinct values in n rolls of a k-sided die | Iv = 1 if value v appears, P = 1 - (1-1/k)^n | **k(1 - (1-1/k)^n)** |
| Expected runs in n fair coin flips | first flip starts a run; flip i ≥ 2 starts a run if it differs, P = 1/2 | **1 + (n-1)/2** |
| Expected number of "HH" occurrences (overlapping) in n flips | Ii = 1 if flips i, i+1 are HH, P = 1/4 | **(n-1)/4** |
| Expected comparisons in randomized quicksort | Iij = 1 if the i-th and j-th smallest are compared, P = 2/(j-i+1) | **2(n+1)H_n - 4n ≈ 1.39 n log2 n** (Section 7.32) |

The indicators in these examples are **dependent** (for example, fixed points), yet linearity still applies. Interviewers often follow up with the variance, which does require pairwise joint probabilities: for fixed points, Var = 1 as well.

### 4.3 First-step analysis (expected time to absorption)

For "expected steps until X", define E_s = expected remaining steps from state s, condition on the first step, and solve the linear system.

**Example: expected rolls of a die to see a 6.** E = 1 + (5/6)E, so E = 6. In general a geometric wait with success probability p takes 1/p trials.

**Example: expected flips to get HH.** States: S0 (no progress), S1 (last flip was H).

```text
E0 = 1 + (1/2) E1 + (1/2) E0
E1 = 1 + (1/2) · 0 + (1/2) E0
=> E0 = 6
```

Section 7.5 compares this with HT (answer 4) and explains why they differ.

### 4.4 Variance and concentration you should know

| Inequality | Statement | Typical use |
|---|---|---|
| Markov | P(X ≥ a) ≤ E[X]/a for X ≥ 0 | Crude tail bound with only the mean ("at most 1/10 of runs take 10× the mean time") |
| Chebyshev | P(abs(X - μ) ≥ kσ) ≤ 1/k^2 | Any distribution with finite variance; why averaging n runs shrinks error as 1/√n |
| Chernoff/Hoeffding | P(sum deviates from mean by ≥ t) ≤ 2 exp(-2t^2/n) for n independent [0,1] variables | Exponentially small tails; load balancing, sampling guarantees |
| Jensen | E[f(X)] ≥ f(E[X]) for convex f | E[1/X] ≥ 1/E[X]: average throughput ≠ 1 / average latency |

**Engineering consequence of Jensen:** if per-request latency varies, the mean of per-request throughput (1/latency) overstates the true throughput. Always compute rates as total work / total time.

### 4.5 Interview Questions

**Q1.** n people put their hats in a pile and each takes one at random. What is the expected number who get their own hat? What is the probability nobody does?

Expected number is exactly 1 for every n, by linearity: each person has probability 1/n of their own hat, and there are n people. The probability nobody gets their own hat is D(n)/n! = Σ_{k=0..n} (-1)^k/k!, which converges to 1/e ≈ 0.368. The count of matches is approximately Poisson(1) for large n.

**Q2.** You hash 1,000 keys into 1,000 buckets with a good hash. How many buckets do you expect to be empty, and how many collisions?

Empty: 1000 (1 - 1/1000)^1000 ≈ 1000/e ≈ 368. Colliding pairs: C(1000,2)/1000 ≈ 499.5. Non-empty buckets ≈ 632, so about 368 keys are "extra" beyond the first in their bucket. The maximum load grows as Θ(ln n / ln ln n) (the leading term gives 3.6 for n = 1000; simulations typically show 5 or 6); using "power of two choices" (insert into the less-loaded of two random buckets) cuts the max load to about ln ln n / ln 2 + O(1), an exponential improvement used in load balancers.

**Q3.** Why can you add expectations of dependent random variables but not variances?

Expectation is a linear operator on the sum: E[X+Y] = Σ (x+y) P(x,y) splits into Σ x P(x,y) + Σ y P(x,y) = E[X] + E[Y], with no independence needed. Variance is quadratic: Var(X+Y) = Var(X) + Var(Y) + 2Cov(X,Y), and the covariance term vanishes only when the variables are uncorrelated. Example: X = Y gives Var(2X) = 4Var(X), not 2Var(X).

**Q4.** A process reports a new running maximum each time it sees a value larger than all previous ones. For a random stream of n distinct values, how many updates do you expect?

H_n ≈ ln n + 0.577. Element i is a new maximum with probability 1/i (it is the largest of the first i, all orders equally likely), and linearity sums these. For n = 10^6 that is about 14.4 updates. This is why "update the running max under a lock only when larger" is cheap in concurrent code: contention on the update path is logarithmic, not linear.

**Q5.** What is E[max(X, Y)] for X, Y independent Uniform(0,1)? E[min]?

P(max ≤ t) = t^2, so the density is 2t and E[max] = ∫ 2t^2 dt = 2/3. E[min] = 1/3 (since max + min = X + Y, which has mean 1). For n uniforms: E[max] = n/(n+1), E[min] = 1/(n+1), and the n points split [0,1] into n+1 gaps each of expected length 1/(n+1).

---

## 5. Distributions Cheat Sheet

| Distribution | Models | PMF / PDF | Mean | Variance | Notes |
|---|---|---|---|---|---|
| Bernoulli(p) | One trial, success prob p | P(1) = p, P(0) = 1-p | p | p(1-p) | Max variance 1/4 at p = 1/2 |
| Binomial(n, p) | Successes in n independent trials | C(n,k) p^k (1-p)^(n-k) | np | np(1-p) | Sum of n Bernoullis |
| Geometric(p) (trials until first success, k ≥ 1) | Retries until success | (1-p)^(k-1) p | 1/p | (1-p)/p^2 | Memoryless (discrete). Some texts count failures (k ≥ 0, mean (1-p)/p) |
| Negative binomial (trials until r successes) | Waiting for r successes | C(k-1, r-1) p^r (1-p)^(k-r) | r/p | r(1-p)/p^2 | Sum of r geometrics |
| Hypergeometric(N, K, n) | Successes in n draws without replacement, K good of N | C(K,k)C(N-K,n-k)/C(N,n) | nK/N | n(K/N)(1-K/N)(N-n)/(N-1) | Finite-population correction (N-n)/(N-1) |
| Poisson(λ) | Count of rare independent events in an interval | e^(-λ) λ^k / k! | λ | λ | Limit of Binomial(n, λ/n); requests per second at low utilization |
| Discrete uniform {a..b} | Fair die, random index | 1/(b-a+1) | (a+b)/2 | ((b-a+1)^2 - 1)/12 | Die: mean 3.5, var 35/12 |
| Continuous uniform [a, b] | Random point, random phase | 1/(b-a) | (a+b)/2 | (b-a)^2/12 | Uniform(0,1): var 1/12 |
| Exponential(λ) | Time between Poisson events | λ e^(-λx), x ≥ 0 | 1/λ | 1/λ^2 | Memoryless (continuous); min of exponentials is Exponential(Σ λi) |
| Normal(μ, σ^2) | Sums/averages of many small effects | (1/(σ√(2π))) e^(-(x-μ)^2/(2σ^2)) | μ | σ^2 | 68-95-99.7 rule; sum of independent normals is normal |
| Log-normal | Products of many factors: file sizes, latencies | ln X ~ Normal(μ, σ^2) | e^(μ+σ^2/2) | (e^(σ^2) - 1) e^(2μ+σ^2) | Right-skewed; mean > median = e^μ |
| Pareto / power law | Heavy tails: request sizes, popularity | ∝ x^-(α+1) | α x_m/(α-1) for α > 1 | Infinite if α ≤ 2 | Averages are unstable; report percentiles |

### 5.1 Relationships worth knowing

- **Binomial -> Poisson:** n large, p small, np = λ moderate. Example: 10,000 requests each failing with p = 0.0003 gives errors ≈ Poisson(3); P(0 errors) ≈ e^-3 ≈ 5%.
- **Binomial -> Normal:** when np(1-p) ≳ 10, use Normal(np, np(1-p)) with a continuity correction.
- **Poisson process:** arrival counts in disjoint intervals are independent Poisson; gaps are i.i.d. Exponential(λ). Merging Poisson streams adds rates; randomly splitting (thinning) a Poisson stream with probability p gives Poisson(pλ).
- **Memorylessness:** P(X > s + t given X > s) = P(X > t). Exponential (continuous) and geometric (discrete) are the only memoryless distributions. A disk with exponential lifetime is "as good as new" at every age, which real hardware is not (bathtub curve), so do not over-apply it.
- **Sum of independent normals:** μ's add, σ^2's add (standard deviations do NOT add): the SD of the sum of two independent SD-3 noises is √18 ≈ 4.24, not 6.

### 5.2 Normal distribution numbers

| Within ± kσ | Probability | Outside (two-sided) | One-sided tail beyond +kσ |
|---|---|---|---|
| 1σ | 68.27% | 31.7% | 15.9% |
| 1.645σ | 90% | 10% | 5% |
| 1.96σ | 95% | 5% | 2.5% |
| 2σ | 95.45% | 4.55% | 2.3% |
| 2.576σ | 99% | 1% | 0.5% |
| 3σ | 99.73% | 0.27% | 0.135% |
| 6σ | 99.9999998% | 2 × 10^-9 | 1 × 10^-9 |

### 5.3 Interview Questions

**Q1.** A web server receives an average of 2 requests per second, modeled as a Poisson process. What is the probability of no requests in one second? What is the expected wait for the next request if none has arrived in the last 5 seconds?

P(0) = e^-2 ≈ 0.135. Because inter-arrival times are exponential and memoryless, the expected wait is still 1/λ = 0.5 s regardless of how long you have already waited. Pitfall: answering 0 or "it is overdue". Follow-up: P(at least 5 in a second) = 1 - Σ_{k=0..4} e^-2 2^k/k! = 1 - e^-2(1 + 2 + 2 + 4/3 + 2/3) = 1 - 7e^-2 ≈ 0.053.

**Q2.** When is a Poisson model for request arrivals wrong?

When arrivals are correlated or bursty: retries after a failure (retry storms), cron jobs firing at the top of the hour, batch jobs, diurnal load, and synchronized clients. Real traffic is often over-dispersed (variance > mean), so a Poisson-based capacity plan underestimates peaks. Use measured peak-to-mean ratios and add jitter to scheduled clients.

**Q3.** You have two independent noise sources in a benchmark with standard deviations 3 ms and 4 ms. What is the standard deviation of their sum?

Variances add: 9 + 16 = 25, so SD = 5 ms. Standard deviations add only for perfectly correlated sources (giving 7 ms). This is why independent small noise sources combine less badly than intuition suggests, and why a single dominant source (4 ms here) determines most of the total.

**Q4.** A geometric distribution models retries with success probability 0.2 per attempt. What are the mean and standard deviation of attempts? What is the probability of needing more than 10?

Mean 1/p = 5 attempts. Variance (1-p)/p^2 = 0.8/0.04 = 20, SD ≈ 4.47. P(more than 10) = P(first 10 all fail) = 0.8^10 ≈ 0.107. The SD nearly equals the mean, which is why retry loops need a cap and why tail latency of retried operations is poor.

---

## 6. Statistics for Engineers

### 6.1 Descriptive statistics and why the mean misleads

| Statistic | Formula / definition | When to use |
|---|---|---|
| Mean | Σx / n | Total-cost questions (throughput, total GPU-hours) |
| Median (p50) | Middle value | Typical experience; robust to outliers |
| Percentiles (p90/p99/p99.9) | Value below which that fraction falls | Latency SLOs; tail behavior |
| Sample variance | s^2 = Σ(x - x̄)^2 / (n - 1) | Divide by n-1 (Bessel's correction) because x̄ is estimated from the same data, which makes deviations look smaller |
| Standard error of the mean | s / √n | Uncertainty of the mean itself, not of individual runs |
| Coefficient of variation | s / x̄ | Comparing noise across benchmarks of different scales; under ~1-2% is a stable microbenchmark |
| MAD (median absolute deviation) | median(abs(x - median)) | Robust spread when outliers exist |

**Percentiles do not average.** The mean of per-host p99 latencies is not the fleet p99. Merge histograms (or t-digest / HDR histogram sketches) and compute percentiles from the merged distribution.

**Fan-out amplifies the tail.** If a request fans out to 100 independent backends and each is slow (above its p99) 1% of the time, then P(the request waits on at least one slow backend) = 1 - 0.99^100 ≈ **63%**. The service's median is governed by the backends' p99. Mitigations: hedged requests, tied requests, reduced fan-out.

### 6.2 Central Limit Theorem (CLT)

If X1..Xn are i.i.d. with mean μ and finite variance σ^2, then the sample mean X̄ is approximately Normal(μ, σ^2/n) for large n, **regardless of the shape of the original distribution**.

- Error of a mean shrinks as 1/√n: 4× more runs halve the error bar.
- "Large n" depends on skew: ~30 is fine for mildly skewed data; heavy-tailed latency distributions may need thousands, and if the variance is infinite (Pareto α ≤ 2) the CLT does not apply.
- The CLT is about the **mean**, not about individual samples. Latencies stay skewed no matter how many you collect.

### 6.3 Confidence intervals

```text
Mean, large n:        x̄ ± z · s/√n            z = 1.96 for 95%
Mean, small n:        x̄ ± t_{n-1} · s/√n      t_{9} = 2.262, t_{29} = 2.045 for 95%
Proportion:           p̂ ± 1.96 · sqrt(p̂(1 - p̂)/n)
Zero events in n:     95% upper bound ≈ 3/n     ("rule of three")
Difference of means:  (x̄1 - x̄2) ± 1.96 · sqrt(s1^2/n1 + s2^2/n2)
```

**Correct interpretation:** "If we repeated this procedure many times, 95% of the intervals constructed would contain the true value." It is *not* "there is a 95% probability the true value is in this particular interval" (that is a Bayesian credible interval, which needs a prior).

**Worked: kernel timing.** 10 runs, mean 412 µs, s = 6 µs. 95% CI = 412 ± 2.262 × 6/√10 = 412 ± 4.3 µs. A change measured at 405 µs from a similar 10-run sample: difference 7 µs, SE of difference = sqrt(36/10 + 36/10) ≈ 2.68 µs, t ≈ 2.6 with ~18 degrees of freedom: significant at 5%. But check for drift (thermal, clocks) before believing it.

**Worked: A/B conversion.** 10,000 users, 5% convert. SE = sqrt(0.05 × 0.95 / 10000) ≈ 0.00218. 95% CI = 5.0% ± 0.43 percentage points.

**Worked: rule of three.** A new driver build ran 1,500 jobs with zero hangs. A 95% upper bound on the hang rate is 3/1500 = 0.2%. "Zero observed" does not mean "zero rate".

**Sample size for detecting a difference (80% power, α = 0.05, two-sided):** n per arm ≈ 16 σ^2 / δ^2, where δ is the minimum detectable difference. For proportions σ^2 = p(1-p). Detecting a lift from 5.0% to 5.5% (δ = 0.005): 16 × 0.0475 / 0.000025 ≈ **30,400 users per arm**. Halving δ quadruples n.

### 6.4 Hypothesis tests and p-value caveats

A **p-value** is P(data at least this extreme given the null hypothesis is true). It is not P(null is true), not the probability the result is a fluke, and not a measure of effect size.

| Caveat | What goes wrong | Mitigation |
|---|---|---|
| Multiple comparisons | 20 independent tests at α = 0.05 give P(at least one false positive) = 1 - 0.95^20 ≈ 64% | Bonferroni (α/m), Holm, or false-discovery-rate control (Benjamini-Hochberg) |
| Peeking / optional stopping | Checking a running A/B test daily and stopping at the first p < 0.05 inflates false positives far beyond 5% | Fix sample size in advance, or use sequential tests designed for peeking |
| Statistical vs practical significance | With millions of samples, a 0.01% latency change is "significant" but irrelevant | Report effect size with a CI; pre-define the minimum meaningful effect |
| Non-independent samples | Repeated runs on one warm node, or many requests from one user, look like more evidence than they are | Randomize run order, interleave A/B builds, use multiple nodes; cluster-level analysis |
| Wrong test for the distribution | t-test on heavy-tailed latency | Compare medians/percentiles with bootstrap CIs or Mann-Whitney U |
| Absence of evidence | p = 0.3 does not prove "no regression" | Report the CI: "the change is within ±1.5%" |
| Simpson's paradox | A variant wins in every segment but loses overall due to different segment mixes | Stratify by the confounder; check traffic allocation |

### 6.5 Benchmarking checklist (where this shows up for GPU/HPC roles)

1. Warm up (JIT compilation, first-touch page faults, GPU clocks ramping, caches).
2. Pin clocks or record them; on GPUs, power/thermal throttling changes frequency during a run.
3. Interleave A and B (ABABAB) instead of AAA then BBB, so drift affects both equally.
4. Report median and a spread (IQR or bootstrap CI), not only the mean; show the distribution if bimodal.
5. Use enough repetitions that the CI is smaller than the effect you care about.
6. Check that the measured quantity is the bottleneck you think (counters, roofline position), not the timer overhead.

**Bootstrap CI in pure Python (runs as is):**

```python
import random
import statistics

random.seed(42)
# Simulated kernel times (µs): mostly ~400 with occasional slow outliers
samples = [random.gauss(400, 5) for _ in range(95)] + [random.uniform(450, 600) for _ in range(5)]


def bootstrap_ci(data, stat=statistics.median, reps=5000, alpha=0.05):
    """Percentile bootstrap confidence interval for any statistic."""
    n = len(data)
    estimates = sorted(stat(random.choices(data, k=n)) for _ in range(reps))
    lo = estimates[int(reps * alpha / 2)]
    hi = estimates[int(reps * (1 - alpha / 2)) - 1]
    return lo, hi


mean = statistics.fmean(samples)
median = statistics.median(samples)
print(f"mean   = {mean:7.2f} µs  (pulled up by outliers)")
print(f"median = {median:7.2f} µs")
lo, hi = bootstrap_ci(samples)
print(f"95% CI for median: ({lo:.2f}, {hi:.2f})")
lo, hi = bootstrap_ci(samples, stat=statistics.fmean)
print(f"95% CI for mean:   ({lo:.2f}, {hi:.2f})")
```

**See also:** [Performance Engineering](Performance_Engineering.md) for measurement methodology, and [Debugging and Profiling Tools](../tools/Debugging_and_Profiling_Tools.md) for the tools that produce these samples.

### 6.6 Interview Questions

**Q1.** Why divide by n - 1 in the sample variance?

Deviations are measured from the sample mean x̄, which is itself fitted to the data and is closer to the data than the true mean μ is. So Σ(x - x̄)^2 is systematically smaller than Σ(x - μ)^2; its expectation is (n-1)σ^2. Dividing by n-1 makes s^2 unbiased. Equivalently, one degree of freedom was spent estimating the mean. For n = 1000 the difference is negligible; for n = 5 it is 25%.

**Q2.** Your benchmark shows a 3% speedup with p = 0.04 after you tried 15 different compiler flags. Do you believe it?

Not yet. With 15 comparisons at α = 0.05, the chance of at least one false positive is 1 - 0.95^15 ≈ 54%. Bonferroni would require p < 0.0033. Re-run the winning configuration on fresh data (a held-out confirmation run), interleaved with the baseline, and check it reproduces on other nodes. Also check whether 3% exceeds run-to-run noise (CV) and whether the mechanism makes sense in counters.

**Q3.** State the Central Limit Theorem and one situation where relying on it is dangerous.

The mean of n i.i.d. samples with finite variance is approximately normal with SD σ/√n. It is dangerous for heavy-tailed data (for example, request sizes with Pareto tails or latencies with rare multi-second stalls): convergence is slow, sample variance is dominated by a few points, and with infinite variance the theorem fails. It is also misused for individual observations: a p99 SLO is about the tail of the raw distribution, which the CLT says nothing about.

**Q4.** How many samples do you need to estimate a probability near 1% to within ±0.1 percentage point at 95% confidence?

Solve 1.96 sqrt(p(1-p)/n) = 0.001 with p = 0.01: n = 1.96^2 × 0.0099 / 10^-6 ≈ 38,000. Rare-event estimation needs a lot of samples because the absolute error must be small relative to a small p. For very rare events (10^-6), use importance sampling or analytic bounds instead of brute force.

**Q5.** Explain Simpson's paradox with an engineering example.

A new scheduler has lower average job latency on both small and large clusters, yet higher overall average latency. This happens if the new scheduler handled a larger share of jobs on the (slow) large clusters: the aggregate mixes groups in different proportions. The fix is to compare within strata (per cluster size) or reweight to a common mix. The lesson is that aggregate comparisons are only valid when the treatment assignment is independent of the confounder, which randomization ensures.

---

## 7. Classic Probability Puzzles

Each puzzle states the problem, the answer, the reasoning, and the usual follow-ups. Answers marked "(simulated in Section 8)" are checked by the Monte Carlo script.

| # | Puzzle | Answer |
|---|---|---|
| 7.1 | Birthday problem | 23 people for > 50% |
| 7.2 | Birthday bound for hashes | ~1.18 √N items for 50% collision |
| 7.3 | Coupon collector | n·H_n (14.7 rolls for all six faces) |
| 7.4 | Monty Hall | Switch: 2/3 |
| 7.5 | Expected flips to HH vs HT | 6 vs 4 |
| 7.6 | Which pattern appears first | HH vs HT: 1/2 each; THH beats HHH 7/8 |
| 7.7 | Runs of heads / double six | 2^(n+1) - 2; 42 rolls |
| 7.8 | Gambler's ruin | k/N; duration k(N-k) |
| 7.9 | Drunk near a cliff | p/(1-p) if p < 1/2, else 1 |
| 7.10 | Two envelopes | No gain from switching |
| 7.11 | St. Petersburg paradox | Infinite EV; ~$31 with a $1B bank |
| 7.12 | rand7 from rand5 | Rejection sampling, ~2.38 calls |
| 7.13 | Fair coin from a biased coin | Von Neumann trick, 1/(p(1-p)) flips |
| 7.14 | Shuffle correctness | Fisher-Yates; naive swap is biased |
| 7.15 | Reservoir sampling | Keep item i with prob k/i |
| 7.16 | Expected max of dice | 161/36 ≈ 4.47 for two dice |
| 7.17 | Dice re-roll game | 4.25 with one re-roll |
| 7.18 | Broken stick triangle | 1/4 |
| 7.19 | Secretary problem | Skip n/e, success → 1/e |
| 7.20 | Egg drop | 14 drops for 2 eggs, 100 floors |
| 7.21 | Hat check / Secret Santa | → 1/e nobody matched |
| 7.22 | Uniforms summing past 1 | e draws on average |
| 7.23 | Points in a semicircle | n / 2^(n-1) |
| 7.24 | Ants on a polygon / stick | 1/4 for a triangle |
| 7.25 | Bertrand's box | 2/3 |
| 7.26 | Boy or girl paradox | 1/3, 1/2, 13/27 |
| 7.27 | Russian roulette | Do not spin: 3/4 vs 2/3 |
| 7.28 | Chevalier de Méré | 0.518 vs 0.491 |
| 7.29 | Inspection (bus waiting) paradox | Wait 10 min, not 5 |
| 7.30 | 100 prisoners | ≈ 31% with the cycle strategy |
| 7.31 | Bertrand's chord paradox | 1/3, 1/2, or 1/4 |
| 7.32 | Quicksort expected comparisons | ≈ 1.39 n log2 n |
| 7.33 | Ballot problem | (a-b)/(a+b) |

### 7.1 Birthday problem

**Problem.** How many people are needed for a better-than-even chance that two share a birthday (365 equally likely days)?

**Answer: 23** (P ≈ 50.7%).

```text
P(all distinct among n) = (365/365)(364/365)...((365-n+1)/365) = Π_{i=0..n-1} (1 - i/365)
                        ≈ exp(-Σ i/365) = exp(-n(n-1)/(2·365))
n = 23: exp(-253/365) = exp(-0.693) ≈ 0.50
```

| n | P(shared birthday) |
|---|---|
| 23 | 50.7% |
| 30 | 70.6% |
| 40 | 89.1% |
| 50 | 97.0% |
| 57 | 99.0% |
| 70 | 99.9% |

**Why it is surprising:** there are C(23,2) = 253 pairs, each matching with probability 1/365, so the expected number of matching pairs is 0.69. People intuitively compare against themselves (22 comparisons), not all pairs.

**Follow-up: how many people until someone shares *your* birthday with probability 1/2?** Solve (364/365)^n = 1/2: n = ln 2 / -ln(364/365) ≈ **253**. Quadratic vs linear: pairs grow as n^2.

### 7.2 Birthday bound for hash collisions

**Problem.** With an ideal b-bit hash (N = 2^b values), how many items until a collision is likely?

```text
P(collision among n) ≈ 1 - exp(-n^2 / (2N))
50% at n ≈ sqrt(2 ln 2 · N) ≈ 1.177 sqrt(N)
For small P: n ≈ sqrt(2N·P)
```

| Hash width | 50% collision at about | Practical meaning |
|---|---|---|
| 32-bit | 77,000 items | Never use a 32-bit hash as a unique ID for large sets |
| 64-bit | 5.1 × 10^9 items | Fine for dedup of millions; risky at web scale |
| 128-bit (UUIDv4 has 122 random bits) | ~2.7 × 10^18 (for 122 bits) | Effectively unique |
| 256-bit (SHA-256) | ~4 × 10^38 | Content addressing (Git with SHA-256, Merkle trees) |

**Why it matters:** this is why a hash with b bits gives only b/2 bits of collision resistance, and why kernel-dedup caches, trace-ID schemes, and content-addressed stores pick 64 to 256 bits.

### 7.3 Coupon collector

**Problem.** Each cereal box has one of n coupons uniformly at random. Expected boxes to collect all n?

**Answer: n·H_n = n(1 + 1/2 + ... + 1/n) ≈ n ln n + 0.577n.** For a six-sided die to show all faces: 6 × 2.45 = **14.7 rolls** (simulated in Section 8).

**Reasoning.** Split the process into phases. When you have i-1 distinct coupons, each new box is new with probability (n-i+1)/n, so phase i is geometric with mean n/(n-i+1). Sum by linearity: n(1/n + 1/(n-1) + ... + 1/1) = n H_n.

**Follow-ups.**
- Variance ≈ π^2 n^2 / 6, so the SD is about 1.28 n: the tail is long (the last coupon alone takes n expected draws).
- **Hash load balancing:** throwing n·ln n balls is what it takes to make every one of n bins non-empty, which is why random assignment needs many more tasks than workers before every worker is busy.
- **Testing:** if a fuzzer hits one of n code paths uniformly at random, covering all takes ~n ln n runs; non-uniform paths take far longer.

### 7.4 Monty Hall

**Problem.** Three doors: one car, two goats. You pick door 1. The host, **who knows** where the car is and **always** opens a goat door you did not pick (choosing at random if he has two options), opens door 3. Should you switch?

**Answer: switch; you win with probability 2/3** (simulated in Section 8).

**Reasoning.** Your first pick is right with probability 1/3, and the host's action never changes that because he can always show a goat. Switching wins exactly when your first pick was wrong: 2/3. Bayes check: P(car behind 2 given host opens 3) = P(open 3 given car 2)·(1/3) / P(open 3) = (1 · 1/3) / (1/3 · 1/2 + 1/3 · 1 + 0) = (1/3)/(1/2) = 2/3.

**Follow-ups.**
- **100 doors**, host opens 98 goats: switching wins 99/100. This makes the intuition obvious.
- **Ignorant host** who opens a random other door and happens to show a goat: now 1/2. The host's reveal carries information only because of his constraint. "Same observation, different process, different answer" is the whole lesson.
- **Host who opens a door only when you picked the car** (adversarial): switching always loses. Model the decision process, not just the outcome.

### 7.5 Expected flips to HH vs HT

**Problem.** Flip a fair coin until you see HH. Expected flips? Same for HT?

**Answers: HH = 6, HT = 4** (simulated in Section 8).

**HH (states: S0 = no progress, S1 = last flip H):**

```text
E0 = 1 + ½E1 + ½E0
E1 = 1 + ½·0 + ½E0          (T resets all progress)
=> E0 = 6
```

**HT:**

```text
E0 = 1 + ½E1 + ½E0
E1 = 1 + ½·0 + ½E1          (H keeps us in S1: we still have a trailing H)
=> E1 = 2, E0 = 4
```

**Why they differ:** after a failed attempt at HH (you see HT), you lose all progress. After a failed attempt at HT (you see HH), the second H is still useful. Patterns that overlap with themselves take longer.

**General formula (Conway's correlation):** for a fair coin, E[wait for pattern] = Σ 2^k over every k such that the length-k prefix equals the length-k suffix (including k = full length).

| Pattern | Self-overlaps (k) | Expected flips |
|---|---|---|
| HT | 2 | 4 |
| HH | 1, 2 | 6 |
| HTH | 1, 3 | 10 |
| HHT | 3 | 8 |
| HHH | 1, 2, 3 | 14 |

This is the same self-overlap structure as the KMP failure function.

### 7.6 Which pattern appears first

**Problem.** Flip until either HH or HT appears. Which is more likely first?

**Answer: equally likely, 1/2 each.** Both need an H first; the very next flip decides. Lesson: shorter expected waiting time does not imply "more likely to appear first".

**Follow-up (Penney's game).** HHH vs THH: THH wins with probability **7/8**. HHH can win only if the first three flips are HHH (1/8). Otherwise, the first time HHH would occur, it is preceded by a T, so THH has already appeared. For any length-3 pattern your opponent picks, there is a length-3 pattern that beats it with probability at least 2/3 (the game is non-transitive).

### 7.7 Runs: n heads in a row and two sixes in a row

**Problem.** Expected fair-coin flips to get n heads in a row? Expected die rolls for two consecutive sixes?

**Answers: 2^(n+1) - 2 flips; 42 rolls.**

**Reasoning.** Let E_n be the expected flips to reach n in a row. To get n, first get n-1 in a row (E_{n-1}), then flip once more: with probability p you are done, otherwise you restart: E_n = E_{n-1} + 1 + (1-p)E_n, so E_n = (E_{n-1} + 1)/p. With p = 1/2: E_1 = 2, E_2 = 6, E_3 = 14, giving 2^(n+1) - 2. With p = 1/6 and n = 2: E_1 = 6, E_2 = (6 + 1) × 6 = **42**. Closed form: (1 - p^n) / ((1-p) p^n).

### 7.8 Gambler's ruin and random walks

**Problem.** You have $k and bet $1 per round on a fair coin until you reach $N or $0. P(reach N)? Expected rounds?

**Answers: P = k/N; expected duration = k(N - k).**

**Reasoning (martingale argument).** Your fortune X_t is a fair game (martingale), so its expected value at the stopping time equals the start: P·N + (1-P)·0 = k, giving P = k/N. Also X_t^2 - t is a martingale, so E[X_T^2] - E[T] = k^2, i.e., P·N^2 - E[T] = k^2, giving E[T] = kN - k^2 = k(N - k).

**Example.** $10, target $20, fair bets: 50% success, 100 rounds expected.

**Unfair game** (win probability p, q = 1 - p, r = q/p ≠ 1): P(reach N from k) = (1 - r^k)/(1 - r^N). At American roulette (p = 18/38), starting at $10 and aiming for $20 with $1 bets: r = 10/9, P ≈ **25.9%**, versus 50% in a fair game. The house edge compounds with the number of bets; in an unfavorable game "bold play" (bet as much as needed in few bets) maximizes the chance of reaching the target.

**Random-walk facts:**
- A symmetric 1D or 2D random walk returns to the origin with probability 1 (recurrent), but the expected return time is infinite.
- In 3D it returns with probability about 0.34 (transient) -- Pólya's theorem.
- After n steps, the expected distance from the origin grows as √n (RMS distance exactly √n for ±1 steps).

### 7.9 Drunk near a cliff

**Problem.** A drunk stands 1 step from a cliff edge. Each step goes toward the cliff with probability p and away with 1-p. Probability he eventually falls?

**Answer: 1 if p ≥ 1/2, otherwise p/(1-p).**

**Reasoning.** Let x = P(ever reaching one step closer to the cliff), which is the same from any position by translation. From position 1: fall immediately with p, or step to 2 (prob 1-p), from which you must come back twice: x = p + (1-p)x^2. Roots: x = 1 and x = p/(1-p). When p < 1/2 the correct root is the smaller one, p/(1-p) (the walk drifts away and can escape). Example: p = 1/3 gives 1/2.

### 7.10 Two envelopes

**Problem.** One envelope holds twice the other. You open one and see $X. "The other has 2X or X/2 with equal probability, so its expected value is 1.25X; always switch." What is wrong?

**Answer: switching does not help (without extra information).** If the pair is {a, 2a}, then holding a you gain a by switching and holding 2a you lose a, each with probability 1/2: expected gain 0. The paradoxical argument treats X as if, for every observed X, the pairs {X/2, X} and {X, 2X} were equally likely. That would require a uniform prior over all powers of 2 (or all amounts), which is not a valid probability distribution. With any proper prior, the probability that you hold the smaller envelope depends on X, and the 1.25X calculation is wrong (for large X you are probably holding the larger one).

**Follow-up.** With a known proper prior, a threshold strategy (switch if X < T) is optimal and does have positive expected gain. Even with an unknown prior, switching when X is below a random threshold drawn from a distribution with full support wins with probability strictly above 1/2.

### 7.11 St. Petersburg paradox

**Problem.** Flip until the first head; if it comes on flip k you win $2^k. What is the fair price to play?

**Answer: the expected value is infinite** (Σ_k 2^-k · 2^k = 1 + 1 + ... ), yet nobody pays more than a few dollars.

**Resolutions.**
- **Finite bankroll:** if the counterparty can pay at most $2^30 ≈ $1.07B, the expected value is 30 (for k ≤ 30) + 2^-30 · 2^30 (the capped tail) = **$31**.
- **Utility:** with logarithmic utility the expected utility is finite.
- **Engineering lesson:** heavy-tailed payoffs (or latencies) make the mean dominated by rare events and estimation unstable. Use medians, percentiles, or truncation.

### 7.12 rand7 from rand5 (and rand10 from rand7)

**Problem.** Given `rand5()` uniform on 1..5, implement `rand7()` uniform on 1..7.

**Answer: rejection sampling on a uniform grid.** Two calls make 25 equally likely outcomes. Accept the first 21 (a multiple of 7) and map them 3-to-1; reject 22..25 and retry.

```python
import random
from collections import Counter


def rand5() -> int:
    return random.randint(1, 5)


def rand7() -> int:
    while True:
        x = 5 * (rand5() - 1) + rand5()  # uniform on 1..25
        if x <= 21:                      # 21 = 3 * 7 outcomes accepted
            return (x - 1) % 7 + 1


def rand10() -> int:
    """LeetCode 470 (rand10 from rand7): 7*(a-1)+b is uniform on 1..49; accept <= 40."""
    while True:
        x = 7 * (rand7() - 1) + rand7()
        if x <= 40:
            return (x - 1) % 10 + 1


if __name__ == "__main__":
    random.seed(0)
    counts = Counter(rand7() for _ in range(70_000))
    print(sorted(counts.items()))  # each value about 10,000
    print(sorted(Counter(rand10() for _ in range(50_000)).items()))  # each about 5,000
```

**Expected calls:** each attempt uses 2 calls and succeeds with probability 21/25, so 2 × 25/21 ≈ **2.38** calls. For rand10 from rand7: 2 × 49/40 = 2.45. You can reduce calls by recycling the rejected remainder (22..25 is a uniform value in 1..4, which you can combine with another rand5 call).

**Why `rand5() + rand5()` (or any fixed formula) fails:** a sum is triangular, not uniform. More fundamentally, any algorithm using exactly k calls has 5^k equally likely outcomes, and 5^k is never divisible by 7, so no **bounded** number of calls can be exactly uniform; rejection (unbounded worst case, bounded expectation) is required.

### 7.13 Fair coin from a biased coin

**Problem.** A coin lands heads with unknown probability p (0 < p < 1). Produce a fair bit.

**Answer (von Neumann).** Flip twice. HT → output 1, TH → output 0, HH or TT → discard and repeat. P(HT) = P(TH) = p(1-p), so the output is exactly fair. Each pair succeeds with probability 2p(1-p), costing 2 flips, so the expected number of flips is **1/(p(1-p))** (4 when p = 1/2; 11.1 when p = 0.9).

**Follow-up: the reverse.** To simulate a coin with bias p from a fair coin, generate the binary expansion of a uniform U bit by bit and compare with the binary expansion of p; you stop at the first differing bit, which takes 2 flips on average.

### 7.14 Shuffle correctness (Fisher-Yates)

**Problem.** Write an unbiased shuffle. Is this one correct?

```python
# fragment -- the buggy "naive" shuffle under discussion
for i in range(n):
    j = random.randint(0, n - 1)   # BUG: should be randint(i, n - 1) or randint(0, i)
    a[i], a[j] = a[j], a[i]
```

**Answer: No.** The naive loop has n^n equally likely execution paths. For a uniform result each of the n! permutations needs the same number of paths, so n! must divide n^n. For n = 3, 27 paths cannot split evenly over 6 permutations. The exact enumeration below shows the bias.

**Fisher-Yates (Knuth) shuffle:** for i from n-1 down to 1, pick j uniformly from 0..i and swap a[i], a[j]. Paths: n · (n-1) · ... · 2 = n!, one per permutation. Proof by induction: position n-1 receives each element with probability 1/n; the rest is a uniform shuffle of the remaining n-1 elements. O(n) time, in place.

```python
from collections import Counter
from itertools import product


def naive_outcomes(n: int) -> Counter:
    """Enumerate every path of the naive shuffle exactly (no randomness)."""
    counts = Counter()
    for choices in product(range(n), repeat=n):
        a = list(range(n))
        for i, j in enumerate(choices):
            a[i], a[j] = a[j], a[i]
        counts[tuple(a)] += 1
    return counts


def fisher_yates_outcomes(n: int) -> Counter:
    counts = Counter()
    ranges = [range(i + 1) for i in range(n - 1, 0, -1)]  # j in 0..i for i = n-1..1
    for choices in product(*ranges):
        a = list(range(n))
        for i, j in zip(range(n - 1, 0, -1), choices):
            a[i], a[j] = a[j], a[i]
        counts[tuple(a)] += 1
    return counts


print("naive:       ", dict(naive_outcomes(3)))         # counts 4 or 5 out of 27: biased
print("fisher-yates:", dict(fisher_yates_outcomes(3)))  # every permutation exactly once
```

For n = 3 the naive shuffle produces three permutations with count 5/27 and three with 4/27.

**Other shuffle pitfalls interviewers ask about:**
- `sort` with a random comparator (`lambda a, b: random.choice([-1, 1])`) is biased and can violate the sort's consistency assumptions. Sorting by an independent random key per element is unbiased (ties aside) but O(n log n).
- `rand() % n` has **modulo bias** unless RAND_MAX + 1 is a multiple of n; use rejection or `std::uniform_int_distribution`.
- **PRNG state size:** 52! ≈ 2^225.6, so a generator seeded with 32 bits can produce at most 2^32 of the possible deck orders. Fine for simulation, unacceptable for online card games.

C++ version with the standard library (complete program):

```cpp
#include <array>
#include <cstdio>
#include <map>
#include <random>
#include <utility>

int main() {
    std::mt19937 rng(12345);
    std::map<std::array<int, 3>, int> counts;
    const int trials = 600000;
    for (int t = 0; t < trials; ++t) {
        std::array<int, 3> a{0, 1, 2};
        for (int i = 2; i >= 1; --i) {  // Fisher-Yates
            std::uniform_int_distribution<int> dist(0, i);  // no modulo bias
            std::swap(a[i], a[dist(rng)]);
        }
        ++counts[a];
    }
    for (const auto& [perm, c] : counts) {
        std::printf("%d%d%d: %.4f\n", perm[0], perm[1], perm[2], static_cast<double>(c) / trials);
    }
    // Each of the 6 permutations prints about 0.1667. In real code prefer std::shuffle(begin, end, rng).
    return 0;
}
```

### 7.15 Reservoir sampling (with proof)

**Problem.** Choose k items uniformly at random from a stream of unknown length n, in one pass with O(k) memory.

**Algorithm R.** Keep the first k items. For item i (1-indexed, i > k), draw j uniform in 1..i; if j ≤ k, replace reservoir slot j with item i.

**Proof that every item ends in the sample with probability k/n.**
- Item i (i > k) enters the reservoir with probability k/i.
- At a later step m > i, the item is evicted only if item m is selected (prob k/m) **and** it picks this item's slot (prob 1/k): eviction probability 1/m, survival (m-1)/m.
- Survival through steps i+1..n telescopes: (i/(i+1)) · ((i+1)/(i+2)) · ... · ((n-1)/n) = i/n.
- Total: (k/i) · (i/n) = **k/n**. For the first k items, entry probability is 1 and survival from step k+1 to n is k/n. All items: k/n.

Uniformity of each item's marginal probability is not quite enough on its own; the stronger claim (every k-subset equally likely) also holds and follows by the same induction on n.

```python
import random
from collections import Counter


def reservoir_sample(stream, k: int, rng: random.Random):
    reservoir = []
    for i, item in enumerate(stream, start=1):
        if i <= k:
            reservoir.append(item)
        else:
            j = rng.randint(1, i)
            if j <= k:
                reservoir[j - 1] = item
    return reservoir


rng = random.Random(7)
counts = Counter()
trials = 50_000
for _ in range(trials):
    counts.update(reservoir_sample(range(10), 3, rng))
print({x: round(c / trials, 3) for x, c in sorted(counts.items())})  # each about 0.3
```

**Follow-ups.**
- **Weighted sampling (A-Res, Efraimidis-Spirakis):** give item i the key u^(1/w_i) with u uniform(0,1) and keep the k largest keys in a min-heap.
- **Distributed:** give each item an independent uniform random key; each shard keeps its k smallest keys; merge shards by keeping the global k smallest. Same result as one pass over the union.
- **Skipping (Algorithm L):** compute how many items to skip with a geometric-like draw, reducing random-number calls to O(k(1 + log(n/k))). Useful when the stream is fast and RNG is the bottleneck.
- **Profiler relevance:** sampling a bounded number of kernel dispatches or trace events uniformly from an unbounded run is exactly reservoir sampling.

### 7.16 Expected maximum of dice

**Problem.** Roll two fair dice. Expected value of the larger?

**Answer: 161/36 ≈ 4.47.**

**Reasoning (CDF trick).** P(max ≤ k) = (k/6)^2. Using the tail sum E[M] = Σ_{k=1..6} P(M ≥ k) = Σ_{k=1..6} (1 - ((k-1)/6)^2) = 6 - (0+1+4+9+16+25)/36 = 6 - 55/36 = **161/36**.

**General:** for n dice, E[max] = 6 - Σ_{k=1..5} (k/6)^n. Three dice: 6 - 225/216 = 119/24 ≈ 4.96. For n continuous Uniform(0,1) values, E[max] = n/(n+1). The trick "P(max ≤ x) = P(all ≤ x) = product of CDFs" is the key idea; for the minimum use P(min > x) = product of survival functions.

### 7.17 Dice re-roll game

**Problem.** Roll a die and receive its value in dollars. You may re-roll once, but then you must take the second roll. Optimal strategy and expected value? With two optional re-rolls?

**Answer: 4.25 with one re-roll; 14/3 ≈ 4.67 with two.**

**Backward induction.** With no re-roll left, the value is 3.5. With one re-roll left, keep the roll if it beats 3.5, i.e., keep 4, 5, 6: E = (1/2)(average of 4,5,6 = 5) + (1/2)(3.5) = **4.25**. With two re-rolls, keep a roll only if it beats 4.25 (keep 5, 6): E = (1/3)(5.5) + (2/3)(4.25) = **14/3**. This is optimal stopping: compare the current value against the expected value of continuing.

### 7.18 Broken stick triangle

**Problem.** Break a unit stick at two independent uniform points. Probability the three pieces form a triangle?

**Answer: 1/4** (simulated in Section 8).

**Reasoning.** Three lengths summing to 1 form a triangle iff every piece is shorter than 1/2 (triangle inequality). Let the cut points be X < Y (half of the unit square by symmetry, area 1/2). Conditions: X < 1/2, Y > 1/2, Y - X < 1/2. That region is a triangle with vertices (0, 1/2), (1/2, 1/2), (1/2, 1), area 1/8. Probability = (1/8)/(1/2) = **1/4**.

**Alternative argument.** The pieces are uniform on the simplex; "piece i ≥ 1/2" has probability (1/2)^2 = 1/4 for each i, and these three events are disjoint, so P(no triangle) = 3/4.

**Follow-up.** Break once uniformly, then break the **longer** piece uniformly: P(triangle) = 2 ln 2 - 1 ≈ **0.386**.

### 7.19 Secretary problem

**Problem.** n candidates arrive in random order; after each interview you must hire or reject immediately and irrevocably. You want the single best. Strategy?

**Answer: reject the first r ≈ n/e candidates (about 37%), then hire the first candidate better than all seen so far. P(success) → 1/e ≈ 0.368.** For n = 100 the optimal r is 37 and P ≈ 0.371 (simulated in Section 8).

**Derivation.** With cutoff r, you succeed iff the best is at position i > r and the best among the first i-1 is in the first r (otherwise you would have stopped earlier on someone else):

```text
P(r) = Σ_{i=r+1..n} (1/n) · r/(i-1)  ≈  x ∫_x^1 dt/t = -x ln x,   with x = r/n
d/dx(-x ln x) = -ln x - 1 = 0  =>  x = 1/e,  P = 1/e
```

**Follow-ups.** If you want to maximize the expected rank instead, the optimal strategy is different (with expected rank about 3.87 as n → ∞). If candidates have known value distributions (not just ranks), threshold rules from optimal stopping do better. The "37% rule" also appears in explore/exploit framing.

### 7.20 Egg drop

**Problem.** With 2 eggs and a 100-floor building, find the highest floor from which an egg survives, minimizing the worst-case number of drops.

**Answer: 14 drops.**

**Reasoning (think in reverse).** With d drops and 2 eggs, the first drop should be at floor d: if it breaks, you scan the d-1 floors below with one egg (d-1 more drops). If not, you have d-1 drops left, so the next drop goes d-1 floors higher, then d-2, and so on. Floors covered: d + (d-1) + ... + 1 = d(d+1)/2 ≥ 100 → d = 14 (105 ≥ 100; 13 gives 91). Drop sequence: 14, 27, 39, 50, 60, 69, 77, 84, 90, 95, 99, 100.

**General DP (LeetCode 887 "Super Egg Drop").** Let f(d, e) = maximum number of floors you can fully resolve with d drops and e eggs. Drop once: if it breaks, you can resolve f(d-1, e-1) floors below; if not, f(d-1, e) above; plus the floor you dropped from:

```text
f(d, e) = f(d-1, e-1) + f(d-1, e) + 1,   f(0, e) = f(d, 0) = 0
Closed form: f(d, e) = Σ_{i=1..e} C(d, i)
Answer: smallest d with f(d, e) ≥ N.   O(e · d) time; d = O(log N) when e ≥ log2 N.
```

```python
def min_drops(eggs: int, floors: int) -> int:
    f = [0] * (eggs + 1)  # f[e] = floors resolvable with current number of drops
    drops = 0
    while f[eggs] < floors:
        drops += 1
        for e in range(eggs, 0, -1):  # iterate downward so f[e-1] is still the previous row
            f[e] = f[e - 1] + f[e] + 1
    return drops


assert min_drops(1, 100) == 100
assert min_drops(2, 100) == 14
assert min_drops(3, 100) == 9
assert min_drops(7, 100) == 7  # enough eggs: binary search, ceil(log2(101)) = 7
print("egg drop checks passed")
```

**Pitfall.** The naive DP over (eggs, floors) that tries every drop floor is O(e·N^2); the "floors per drops" reformulation above is the intended optimization.

### 7.21 Hat check and Secret Santa

**Problem.** n people draw names from a hat for Secret Santa. Probability nobody draws their own name? If you redraw until valid, how many draws on average?

**Answer:** P(derangement) = D(n)/n! → **1/e ≈ 0.368** (within 0.001 once n ≥ 6). Redraws are geometric, so on average about **e ≈ 2.72 full draws**. Expected number of self-draws in a single draw is exactly 1 (Section 4.2). Derivation of D(n) is in Section 2.4.

### 7.22 Uniforms summing past 1

**Problem.** Draw Uniform(0,1) values until the sum exceeds 1. Expected number of draws?

**Answer: e ≈ 2.718** (simulated in Section 8).

**Reasoning.** Let N be the number of draws. N > n iff U1 + ... + Un ≤ 1, and the volume of that simplex is 1/n!. Tail sum: E[N] = Σ_{n≥0} P(N > n) = Σ_{n≥0} 1/n! = **e**.

### 7.23 Points in a semicircle

**Problem.** n points are placed uniformly on a circle. Probability that all lie in some semicircle?

**Answer: n / 2^(n-1).** For n = 3: 3/4.

**Reasoning.** Let Ei be "all other points lie in the semicircle starting at point i going clockwise". P(Ei) = (1/2)^(n-1). These events are disjoint (with probability 1 at most one point can be the "first" point of such a semicircle), and their union is the event we want. Sum: n/2^(n-1).

**Follow-up.** A triangle from 3 random points on a circle contains the center iff the points are not in a semicircle: 1 - 3/4 = **1/4**. In 3D, a tetrahedron from 4 random points on a sphere contains the center with probability 1/8.

### 7.24 Ants on a polygon and on a stick

**Problem A.** Three ants sit at the corners of a triangle and each walks along an edge in a random direction. Probability no two collide?

**Answer: 1/4.** No collision iff all go clockwise or all counterclockwise: 2 of 2^3 outcomes. For an n-gon: 2/2^n.

**Problem B.** 100 ants are placed on a 1 m stick, each walking left or right at 1 cm/s. When two meet, both reverse. How long until all have fallen off, in the worst case?

**Answer: at most 100 s.** Two ants bouncing off each other is indistinguishable (as a set of positions) from passing through each other. So each "ant trajectory" just walks straight off, taking at most 100 cm / (1 cm/s) = 100 s. The trick, swapping identities to remove interactions, appears in many simulation and concurrency arguments.

### 7.25 Bertrand's box

**Problem.** Three cards: red/red, red/white, white/white. A random card is placed on the table with a random side up; it shows red. Probability the other side is red?

**Answer: 2/3, not 1/2.** Count **faces**, not cards: there are three red faces equally likely to be showing; two of them belong to the red/red card.

### 7.26 Boy or girl paradox

**Problem.** A family has two children (each independently a boy or girl with probability 1/2).
1. At least one is a boy. P(both boys)?
2. The older child is a boy. P(both boys)?
3. At least one is a boy born on a Tuesday. P(both boys)?

**Answers: 1/3, 1/2, 13/27.**

1. Equally likely: BB, BG, GB, GG. Condition removes GG: 1 of 3.
2. The condition fixes the older child: the younger is a boy with 1/2.
3. Each child is one of 14 equally likely (sex, weekday) types: 196 pairs. Pairs with at least one Tuesday-boy: 196 - 13^2 = 27. Of those, both boys: 7^2 - 6^2 = 13. **13/27** ≈ 0.48.

**The real lesson:** answers depend on *how* the information was obtained. If instead a random child was observed and was a boy, the answer to (1) is 1/2. Always ask what process generated the observation.

### 7.27 Russian roulette

**Problem.** A six-chamber revolver has two **adjacent** bullets. The cylinder is spun, your opponent fires at himself and survives. You may spin again or fire the next chamber. Which is safer?

**Answer: do not spin; survive with 3/4 versus 2/3.**

**Reasoning.** Label the chambers B B E E E E in a cycle. Your opponent was at one of the 4 empty chambers, each equally likely. The next chamber after them is E, E, E, B respectively: 3/4 safe. Spinning gives 4/6 = 2/3. If the bullets were **not** adjacent (for example B E B E E E), the next chamber after the four empties contains B in 2 of 4 cases: 1/2 safe vs 2/3 spinning, so spin.

### 7.28 Chevalier de Méré

**Problem.** Which is more likely: at least one 6 in 4 rolls of a die, or at least one double-six in 24 rolls of two dice?

**Answer: the first.** 1 - (5/6)^4 ≈ **0.518**; 1 - (35/36)^24 ≈ **0.491**. The naive linear reasoning (4 × 1/6 = 24 × 1/36 = 2/3) ignores overlapping events. Using the complement makes the comparison immediate. This historically motivated Pascal and Fermat's correspondence on probability.

### 7.29 Inspection (bus waiting) paradox

**Problem.** Buses arrive as a Poisson process with an average of one every 10 minutes. You arrive at a random time. Expected wait?

**Answer: 10 minutes, not 5.** By memorylessness, the time to the next bus is Exponential with mean 10 regardless of the past. The interval you land in is not a typical interval: you are more likely to arrive during a long gap. For a general gap distribution G, the expected wait is E[G^2] / (2 E[G]). Deterministic 10-minute gaps give 5; exponential gaps (E[G^2] = 200) give 200/20 = 10.

**Where engineers see it:**
- **Sampling profilers:** a time-based sampler hits a function or kernel with probability proportional to its duration, so the "average duration of sampled kernels" is length-biased (E[L^2]/E[L]), not the true mean kernel duration. Use dispatch-level tracing for per-call averages and sampling for "where does time go".
- **Average class size:** students experience a larger average class size than the university's reported average.
- **Request latency from the client's view:** a random moment in time is more likely to be inside a long GC pause than an average pause length suggests.

### 7.30 100 prisoners

**Problem.** 100 numbered prisoners, 100 boxes each containing a random distinct prisoner number. Each prisoner may open 50 boxes; all go free only if every prisoner finds their own number. They may agree on a strategy beforehand but cannot communicate later. Best strategy?

**Answer: follow the cycle; success ≈ 31.2%** (versus (1/2)^100 for random guessing).

**Strategy.** Prisoner i opens box i, then the box whose number was inside, and so on. Prisoner i follows the cycle of the permutation that contains i, so he finds his number iff that cycle has length ≤ 50. Everyone succeeds iff the permutation has no cycle longer than 50.

**Probability.** For k > n/2, a permutation can contain at most one cycle of length k, and the number of permutations with one is n!/k. So P(longest cycle > 50) = Σ_{k=51..100} 1/k = H_100 - H_50 ≈ 0.688, giving success ≈ **0.312**. As n → ∞ it tends to 1 - ln 2 ≈ 0.307. The strategy works because it makes the prisoners' fates highly correlated: they all succeed or many fail together.

### 7.31 Bertrand's chord paradox

**Problem.** Choose a "random chord" of a circle. Probability it is longer than the side of the inscribed equilateral triangle?

**Answer: it depends on what "random" means:**

| Method | Probability |
|---|---|
| Two uniform random endpoints on the circle | 1/3 |
| Random radius, uniform point on it, chord perpendicular through that point | 1/2 |
| Uniform random midpoint inside the disk | 1/4 |

**Lesson:** "uniformly at random" is meaningless until you specify the generating process. In an interview, say which process you assume, and (for a bonus) mention the others.

### 7.32 Quicksort expected comparisons

**Problem.** Randomized quicksort on n distinct keys: expected comparisons?

**Answer: 2(n+1)H_n - 4n ≈ 2n ln n ≈ 1.39 n log2 n.**

**Indicator proof.** Let z1 < z2 < ... < zn be the sorted keys. zi and zj (i < j) are compared iff the first pivot chosen from {zi, ..., zj} is zi or zj (any pivot strictly between separates them forever; any pivot outside leaves them together). That has probability 2/(j - i + 1). Summing: Σ_{i<j} 2/(j-i+1) ≈ 2n H_n. The same argument shows that randomized quickselect uses at most 4n comparisons in expectation (O(n)).

### 7.33 Ballot problem

**Problem.** Candidate A gets a votes and B gets b votes, a > b, and the ballots are counted in uniformly random order. Probability A is strictly ahead throughout the count?

**Answer: (a - b)/(a + b).** For a = 3, b = 2: 1/5 (only AAABB and AABAB of the 10 orders).

**Reasoning (reflection).** Sequences starting with B are always bad. Bad sequences starting with A are in bijection with sequences starting with B (reflect the prefix up to the first tie), so bad = 2 × (sequences starting with B) = 2 × C(a+b-1, a). Good fraction = 1 - 2b/(a+b) = (a-b)/(a+b). This is the same reflection principle used for Catalan numbers in Section 2.6.

### 7.34 Interview Questions

**Q1.** In Monty Hall, why does it matter whether the host knows where the car is?

The posterior depends on the likelihood of the host's action under each hypothesis. A knowing host always opens a goat door, so seeing a goat has probability 1 when you picked a goat and 1 when you picked the car; the reveal is uninformative about your door, which stays at 1/3, and the remaining door absorbs 2/3. An ignorant host reveals a goat with probability 1/2 when you picked a goat (he might have revealed the car), so seeing a goat raises the chance that you picked the car to 1/2. Same observation, different likelihoods, different posteriors.

**Q2.** Your teammate's shuffle uses `j = rand() % (i + 1)` in a Fisher-Yates loop with a 15-bit `rand()`. What is wrong?

Two things. First, modulo bias: 32,768 is not divisible by i+1 for most i, so small residues are slightly more likely; for i+1 = 10,000, residues 0..2,767 get 4 preimages and the rest get 3, a 33% relative bias. Second, a 15-bit (or any small-state) generator cannot reach most permutations of a large array. Fix: `std::shuffle` with `std::mt19937_64` (or a CSPRNG for security-sensitive cases), which uses `uniform_int_distribution` internally to avoid modulo bias.

**Q3.** How would you sample 1,000 log lines uniformly from a multi-terabyte log spread across 500 machines?

Run reservoir sampling with random keys: on each machine, stream the logs and assign every line an independent Uniform(0,1) key, keeping the 1,000 lines with the smallest keys in a max-heap. Send each machine's 1,000 (key, line) pairs to a coordinator, which keeps the 1,000 smallest keys overall. Every line has the same probability of having one of the globally smallest 1,000 keys, so the result is a uniform sample without replacement. Cost is one streaming pass, O(k) memory per machine, and O(machines × k) network.

**Q4.** What is the expected number of flips to get HTH, and why is it larger than for HHT?

Use Conway's correlation: HTH overlaps itself at k = 1 (H) and k = 3, so E = 2 + 8 = 10. HHT has no proper self-overlap (prefix H ≠ suffix T; prefix HH ≠ suffix HT), so E = 8. When HTH fails at the last flip (HTT), all progress is lost; when it succeeds partially, the overlap means occurrences cluster, and clustered occurrences with the same long-run frequency (1/8 per position) imply longer gaps between clusters.

**Q5.** You have 3 eggs and 1,000 floors. How many drops in the worst case?

Find the smallest d with C(d,1) + C(d,2) + C(d,3) ≥ 1000. d = 18: 18 + 153 + 816 = 987 (not enough). d = 19: 19 + 171 + 969 = 1159 ≥ 1000. Answer: **19**. With 2 eggs it would be 45 (45 × 46/2 = 1035), and with 10 eggs it would be 10 (binary search: 2^10 = 1024 ≥ 1001 outcomes).

---

## 8. Monte Carlo Simulation Toolkit

When you are unsure of an answer, say so and propose a simulation. In a take-home or a shared editor, writing one in five minutes is a strong signal. The key facts:

- The estimate p̂ from N independent trials has standard error sqrt(p(1-p)/N). For p ≈ 0.5: N = 10^4 gives ±1% (95%), N = 10^6 gives ±0.1%. **Each extra decimal digit costs 100× more trials.**
- Seed the RNG for reproducibility, and report the estimate with its confidence interval.
- Simulate the **process as described**, not your mental model of it (for Monty Hall, actually code the host's choice). Most "the simulation disagrees with the math" bugs come from simulating a different process.
- For speed, vectorize with NumPy (`rng = np.random.default_rng(seed)`) or parallelize independent trials; Monte Carlo is embarrassingly parallel and a classic GPU workload (one trial per thread, a counter-based RNG such as Philox per thread).

### 8.1 Simulation script for Section 7 puzzles

Standard library only; runs in a few seconds and prints each estimate next to the exact answer.

```python
"""Monte Carlo checks for classic probability puzzles (standard library only)."""
import math
import random
import statistics

rng = random.Random(2026)


def estimate(trial, n_trials):
    """Run trial() n_trials times; return (mean, 95% CI half-width)."""
    values = [trial() for _ in range(n_trials)]
    mean = statistics.fmean(values)
    half = 1.96 * statistics.stdev(values) / math.sqrt(n_trials)
    return mean, half


def birthday(n=23, days=365):
    seen = set()
    for _ in range(n):
        d = rng.randrange(days)
        if d in seen:
            return 1
        seen.add(d)
    return 0


def coupon_collector(n=6):
    seen, draws = set(), 0
    while len(seen) < n:
        seen.add(rng.randrange(n))
        draws += 1
    return draws


def monty_hall(switch: bool):
    car = rng.randrange(3)
    pick = rng.randrange(3)
    # Host knowingly opens a goat door that is not the contestant's pick.
    host = rng.choice([d for d in range(3) if d != pick and d != car])
    if switch:
        pick = next(d for d in range(3) if d != pick and d != host)
    return int(pick == car)


def flips_until(pattern: str):
    window, flips = "", 0
    while not window.endswith(pattern):
        window = (window + rng.choice("HT"))[-len(pattern):]
        flips += 1
    return flips


def broken_stick():
    x, y = sorted((rng.random(), rng.random()))
    return int(max(x, y - x, 1 - y) < 0.5)


def secretary(n=100, r=37):
    ranks = list(range(n))  # higher is better; n-1 is the best
    rng.shuffle(ranks)
    best_seen = max(ranks[:r])
    for value in ranks[r:]:
        if value > best_seen:
            return int(value == n - 1)
    return 0  # never hired anyone better: failure


def uniforms_past_one():
    total, count = 0.0, 0
    while total <= 1.0:
        total += rng.random()
        count += 1
    return count


H6 = sum(1 / k for k in range(1, 7))
checks = [
    ("Birthday, 23 people", lambda: birthday(), 0.5073, 100_000),
    ("Coupon collector, d6", lambda: coupon_collector(), 6 * H6, 100_000),
    ("Monty Hall, stay", lambda: monty_hall(False), 1 / 3, 100_000),
    ("Monty Hall, switch", lambda: monty_hall(True), 2 / 3, 100_000),
    ("Flips until HH", lambda: flips_until("HH"), 6.0, 100_000),
    ("Flips until HT", lambda: flips_until("HT"), 4.0, 100_000),
    ("Broken stick triangle", broken_stick, 0.25, 100_000),
    ("Secretary n=100 r=37", lambda: secretary(), 0.3710, 50_000),
    ("Uniforms until sum > 1", uniforms_past_one, math.e, 100_000),
]

print(f"{'puzzle':28s} {'estimate':>18s} {'exact':>8s}")
for name, trial, exact, n in checks:
    mean, half = estimate(trial, n)
    flag = "" if abs(mean - exact) <= 1.5 * half + 1e-12 else "  <-- check"
    print(f"{name:28s} {mean:9.4f} ± {half:6.4f} {exact:8.4f}{flag}")
```

Expected output: no line is flagged; each estimate is within about 1.5 CI half-widths of the exact value (with seed 2026 the secretary estimate is 0.3757 ± 0.0042, about 2.2 SE from 0.3710, which shows that a 95% CI misses about 1 time in 20). A failure flag (or a value far outside the CI) means the simulation models a different process from the puzzle; the flag threshold is about 2.9 standard errors (roughly 99.7% coverage per check), so with 9 checks an occasional flag from pure chance is still possible, which is itself a multiple-comparisons lesson (Section 6.4).

### 8.2 Estimating π (the canonical Monte Carlo example)

```python
import math
import random

rng = random.Random(1)
for n in (1_000, 100_000, 1_000_000):
    inside = sum(1 for _ in range(n) if rng.random() ** 2 + rng.random() ** 2 <= 1.0)
    est = 4 * inside / n
    se = 4 * math.sqrt((math.pi / 4) * (1 - math.pi / 4) / n)
    print(f"n={n:>9,}  pi≈{est:.5f}  error={abs(est - math.pi):.5f}  expected SE≈{se:.5f}")
```

The error shrinks like 1/√n: 1,000× more samples buys about 1.5 more correct digits. Quasi-Monte Carlo (low-discrepancy sequences such as Sobol) and variance reduction (antithetic variates, control variates, importance sampling) improve on this in practice.

### 8.3 Interview Questions

**Q1.** Your simulation of a puzzle gives 0.52 with 10,000 trials, while your derivation says 0.50. Which do you trust?

Compute the Monte Carlo standard error first: sqrt(0.25/10000) = 0.005, so 0.52 is 4 standard errors away, which is very unlikely by chance (p < 10^-4). Something is wrong with either the derivation or the simulation. Check that the simulation implements the stated process (who chooses what, with replacement or not, off-by-one in loop bounds), then test both on a tiny case you can enumerate exactly. If 0.52 had come from 1,000 trials (SE 0.016), it would be consistent with 0.50.

**Q2.** How would you parallelize a Monte Carlo simulation on a GPU, and what can go wrong with the random numbers?

Assign one trial (or a batch) per thread and reduce the per-thread results with a tree or atomic reduction. The RNG is the subtle part: threads must not share state (contention and correlated streams) and must not be seeded with consecutive seeds in a weak generator (correlated streams). Use a counter-based generator such as Philox (`rocrand_state_philox4x32_10` / `curandStatePhilox4_32_10_t`; note that the library defaults are XORWOW, and Philox is what PyTorch uses for its GPU generator, while JAX defaults to Threefry, another counter-based generator), keyed by a seed with the counter derived from (thread id, trial id), which gives independent, reproducible streams. Also watch reduction precision: summing 10^9 values in FP32 loses accuracy, so accumulate in FP64 or use pairwise/Kahan summation.

**Q3.** How many trials are needed to estimate a probability of about 10^-6 with 10% relative error?

Relative SE ≈ sqrt((1-p)/(Np)) ≈ 1/sqrt(Np). Setting 1/sqrt(Np) = 0.1 gives Np = 100, so N = 10^8 trials (about 100 events observed). For rarer events use importance sampling: sample from a distribution that makes the event common and reweight by the likelihood ratio. The rule "you need about 100 events for 10% precision" is worth memorizing.

---

## 9. Fermi Estimation

### 9.1 The method

1. **Clarify the question and units.** "Storage per year, raw or replicated? Peak or average QPS?"
2. **Decompose** into factors you can estimate: population × fraction × rate × size.
3. **Estimate each factor with round numbers** and say them out loud. Use powers of 10; keep one significant figure.
4. **Combine** with order-of-magnitude arithmetic (add exponents).
5. **Sanity-check** against a known reference point or a different decomposition (top-down vs bottom-up).
6. **Bound the answer.** Give a range or note which assumption dominates the uncertainty. For a very uncertain factor, use the geometric mean of your low and high guesses (between 10 and 1,000, guess 100).
7. **Say what decision the number drives** ("so one Postgres instance is enough", "so we must sample traces").

Errors in independent factors tend to partially cancel, which is why a chain of rough guesses often lands within 2-3× of the truth.

### 9.2 Worked example 1: piano tuners in Chicago (the classic)

| Factor | Estimate | Running total |
|---|---|---|
| Chicago population | 3 × 10^6 | |
| People per household | 2.5 | 1.2 × 10^6 households |
| Households with a piano | 1 in 20 | 6 × 10^4 pianos |
| Plus schools, churches, venues | +10% | ~6.5 × 10^4 pianos |
| Tunings per piano per year | 1 | 6.5 × 10^4 tunings/year |
| Tunings per tuner per day | 4 (1.5 h each plus travel) | |
| Working days per year | 250 | 1,000 tunings per tuner-year |
| **Tuners** | 6.5 × 10^4 / 10^3 | **~65 (range 30-150)** |

The biggest uncertainty is the piano-ownership fraction. Stating that is part of a good answer.

### 9.3 Worked example 2: golf balls in a school bus

- Bus interior: 10 m long × 2.4 m wide × 2 m tall ≈ 50 m^3.
- Golf ball diameter ≈ 4.3 cm, so volume ≈ (4/3)π(2.15 cm)^3 ≈ 41 cm^3 ≈ 4 × 10^-5 m^3.
- Random packing fills about 64% of space, so each ball effectively occupies 4 × 10^-5 / 0.64 ≈ 6.4 × 10^-5 m^3.
- Empty bus: 50 / 6.4 × 10^-5 ≈ 7.8 × 10^5. Seats, wheel wells, and the driver area take roughly a third.
- **Answer: ~500,000 balls (order 10^5 to 10^6).**

The packing-fraction step is what interviewers look for: spheres do not tile space (max 74% for a perfect lattice, ~64% random).

### 9.4 Worked example 3: QPS of a web search engine

- Internet users: ~5 × 10^9. Fraction who search on a given day: ~60%. Searches per searching user per day: ~3.
- Searches/day ≈ 5 × 10^9 × 0.6 × 3 ≈ 9 × 10^9.
- Average QPS = 9 × 10^9 / 86,400 ≈ 10^5 (use 10^5 seconds/day for quick math: **~100,000 QPS**).
- Peak: diurnal peaks are tempered by global time zones, so about 2× average: **~200,000 QPS**.
- Sanity check: public estimates for the largest engine are commonly quoted at several billion searches per day, consistent with ~10^5 QPS.
- **Backend implications:** a result cache may serve a substantial share of queries (popular queries repeat). If each cache miss fans out to ~1,000 index shards (assumption), that is on the order of 10^7-10^8 leaf RPCs/second, which is why tail latency at the leaves (Section 6.1, fan-out) dominates the design and why hedged requests exist.

### 9.5 Worked example 4: one year of GPU profiling traces across a fleet

**Question.** "We want continuous profiling for a 100,000-GPU training fleet. How much storage per year?" Clarify: three data tiers with very different volumes.

**Tier 1: always-on counter telemetry** (utilization, power, clocks, memory bandwidth, temperatures).

| Factor | Estimate |
|---|---|
| Metrics per GPU | 100 |
| Sample interval | 10 s → 8,640 samples/day |
| Bytes per sample (timestamp + value + series-id overhead, columnar) | 16 B |
| Per GPU per day | 100 × 8,640 × 16 B ≈ 14 MB |
| Fleet per day | 14 MB × 10^5 ≈ 1.4 TB |
| Per year raw | ≈ 500 TB |
| After time-series compression (delta-of-delta timestamps, XOR floats, ~10×) | **≈ 50 TB/year** |

**Tier 2: kernel-dispatch traces** (one record per kernel launch: start/end timestamps, kernel id, grid/workgroup sizes, queue id, correlation id).

| Factor | Estimate |
|---|---|
| Kernel dispatches per GPU-second (LLM training, many small kernels) | 2,000 |
| Bytes per record | 64 B |
| Per traced GPU | 128 KB/s ≈ 11 GB/day |
| If every GPU were always traced | 10^5 × 11 GB ≈ 1.1 PB/day ≈ 400 PB/year (infeasible) |
| Sample 1% of GPU-time (rotate which jobs/nodes are traced) | ≈ 11 TB/day ≈ 4 PB/year raw |
| After compression (dictionary-encoded kernel names, delta timestamps, ~4×) | **≈ 1 PB/year** |

**Tier 3: on-demand deep profiles** (many hardware counters per kernel, which need multiple replay passes because only a limited number of counters can be collected per pass -- the rocprof-compute style of analysis).

| Factor | Estimate |
|---|---|
| Profiling sessions per day across the org | 200 |
| Data per session (thousands of kernels × hundreds of counters, plus metadata) | ~2 GB |
| Per year | 200 × 2 GB × 365 ≈ **150 TB/year** |

**Total.** Raw ≈ 0.5 + 4 + 0.15 ≈ 4.7 PB/year; stored compressed ≈ 1.2 PB/year, before redundancy (×1.3-1.5 for erasure coding, ×3 for triple replication).

**What the estimate tells you:**
- Tier 2 dominates (about 5× the other two tiers combined, and 20× tier-1 telemetry), so the **trace sampling rate is the main cost knob**. Going from 1% to 0.1% saves ~0.9 PB/year.
- Retention policy matters more than compression: keep raw dispatch traces 30 days (≈ 90 TB compressed), roll them up into per-kernel histograms (count, total time, p50/p99 per kernel per job) that are kilobytes per job, and keep those for the full year.
- Ingest bandwidth for tier 2 is ≈ 11 TB/day ≈ 130 MB/s average: modest for an object store, but the per-node write path must not perturb the workload (buffer in host memory, write asynchronously, bound overhead to ~1%).
- Sanity check: 14 MB/GPU/day of telemetry is negligible next to checkpoint sizes (a 70B model checkpoint with optimizer state is roughly a terabyte).

**See also:** [AMD GPU Architecture and Profiling](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md) for what the counters mean, and [Project Deep Dive: rocprof-compute](../career/Project_Deep_Dive_rocprof-compute.md) for how to present this kind of trade-off from your own work.

### 9.6 Worked example 5: GPUs needed to train a 70B-parameter model in 30 days

- Training compute ≈ **6 · N · D** FLOPs (forward ≈ 2ND, backward ≈ 4ND) for a dense transformer with N parameters on D tokens.
- N = 7 × 10^10, D = 2 × 10^12 tokens: 6 × 7 × 10^10 × 2 × 10^12 = 8.4 × 10^23 FLOPs.
- Per-GPU throughput: a current datacenter accelerator offers on the order of 10^15 dense BF16 FLOP/s peak; at 40% model FLOPs utilization (MFU) that is 4 × 10^14 FLOP/s.
- GPU-seconds = 8.4 × 10^23 / 4 × 10^14 = 2.1 × 10^9. Thirty days = 2.6 × 10^6 s.
- **GPUs ≈ 2.1 × 10^9 / 2.6 × 10^6 ≈ 800**; budget ~1,000 for restarts, checkpointing, and failed nodes.
- Sensitivity: MFU is the biggest lever. 30% MFU means ~1,100 GPUs; 50% means ~650. This is why profiling tools that find MFU losses (communication stalls, small-kernel launch overhead, memory-bound ops) translate directly into money.

### 9.7 Worked example 6: memory to serve a 70B model with a KV cache

- Weights in BF16: 7 × 10^10 × 2 B = **140 GB**.
- KV cache per token = 2 (K and V) × layers × KV heads × head dim × bytes. For a Llama-2-70B-like config (80 layers, 8 KV heads with grouped-query attention, head dim 128, BF16): 2 × 80 × 8 × 128 × 2 B = 327,680 B ≈ **320 KB per token**.
- 32 concurrent sequences × 4,096 tokens = 131,072 tokens × 320 KB ≈ **42 GB**.
- Total ≈ 140 + 42 + activations/workspace (~10%) ≈ **~200 GB**: it fits on one 192 GB-class GPU only with a smaller batch or a quantized (FP8) KV cache or weights; otherwise use tensor parallelism across 2+ GPUs.
- Without GQA (64 KV heads) the KV cache would be 8× larger (~2.6 MB/token, ~340 GB for the same batch), which is exactly why GQA/MQA were adopted.

**See also:** [LLM and ML Fundamentals](../ml-gpu/LLM_and_ML_Fundamentals.md) and [ML Systems Design](../ml-gpu/ML_Systems_Design.md).

### 9.8 Worked example 7: gradient all-reduce time for data-parallel training

- Model: 7 × 10^9 parameters, BF16 gradients: 14 GB per step.
- Ring all-reduce: each GPU sends and receives 2(N-1)/N × size ≈ 2 × 14 = 28 GB (reduce-scatter plus all-gather), nearly independent of the number of GPUs N.
- Inter-node network: 400 Gb/s per GPU = 50 GB/s.
- Time ≈ 28 / 50 ≈ **0.56 s per step** at line rate (more in practice due to protocol overhead and congestion).
- If a step's compute takes 2 s, communication is ~28% of compute and must be overlapped with the backward pass (bucketed all-reduce) to avoid idle GPUs. ZeRO-1/2 use reduce-scatter + all-gather with the same total volume as all-reduce; ZeRO-3/FSDP full sharding also re-gathers parameters in the backward pass, about 1.5× the communication volume, in exchange for much lower memory per GPU.

### 9.9 Worked example 8: how long to scan 1 TB

| Medium | Throughput (order of magnitude) | Time for 1 TB |
|---|---|---|
| HDD (sequential) | 200 MB/s | ~83 min |
| SATA SSD | 550 MB/s | ~30 min |
| NVMe SSD (PCIe Gen4 x4) | 7 GB/s | ~2.4 min |
| 10 Gb/s network | 1.25 GB/s | ~13 min |
| 100 Gb/s network | 12.5 GB/s | ~80 s |
| DRAM (one socket, streaming) | ~100 GB/s | ~10 s |
| HBM on one GPU | ~5 TB/s | ~0.2 s (but 1 TB does not fit in one GPU's memory) |

**Follow-up: "how long to grep 1 TB of logs?"** A simple regex scan runs at roughly 1 GB/s per core, so 1 TB is ~1,000 core-seconds; on 64 cores that is ~16 s of CPU, so a single NVMe drive (~140 s) is the bottleneck. Spread the data over 10-20 drives to reach about 10-15 s of I/O, at which point the 64 cores (about 16 s) become the bottleneck; going faster needs more machines. Identifying the bottleneck resource is the point of the exercise.

### 9.10 Interview Questions

**Q1.** Estimate how many servers you need to serve 100,000 QPS where each request takes 20 ms of CPU time.

CPU-seconds per second = 10^5 × 0.02 = 2,000 cores busy on average. Run cores at ~50-60% utilization to keep queueing delay low (latency rises sharply as utilization approaches 100%: an M/M/1 queue's mean response time is service time / (1 - ρ)), so provision ~3,500-4,000 cores. With 64-core servers that is ~60 servers, plus N+2 per region for failures and headroom for 2× peak: ~120-150 servers. State the utilization assumption explicitly; it changes the answer by 2×.

**Q2.** You estimated 50 piano tuners and the interviewer says the real number is 150. Is your estimate bad?

Within 3× on a chain of five uncertain factors is a good Fermi estimate; the goal is the right order of magnitude and a transparent model. The useful response is to identify which assumption most likely caused the gap (ownership rate or institutional pianos, or tuners working part-time doing fewer tunings), and say how you would refine it with one data point (for example, the number of listings for tuners).

**Q3.** How much storage does a 1,000-node cluster need per year for logs if each node writes 1 MB/min?

1 MB/min × 1,440 min/day ≈ 1.4 GB/day per node; × 1,000 ≈ 1.4 TB/day; × 365 ≈ 525 TB/year raw. Logs compress 5-10× with zstd, so ~50-100 TB stored, ×1.5 for erasure coding. The design conclusion: keep 7-30 days hot and searchable (indexes can double the hot footprint), move the rest to cheap object storage, and sample or drop DEBUG-level logs at the source.

**Q4.** What are the most common mistakes in Fermi questions?

Silent assumptions (state every number), mixing units (bits vs bytes, per-second vs per-day), false precision (reporting 63,214 instead of ~60,000), forgetting peak vs average and replication/indexing overhead, and not sanity-checking against a known anchor. Another common mistake is computing a number without stating the design decision it drives.

---

## 10. Powers of Two and Handy Numbers

### 10.1 Powers of two

| Power | Exact value | Approximation | Where it shows up |
|---|---|---|---|
| 2^7 | 128 | ~10^2 | ASCII range; signed int8 max is 127 |
| 2^8 | 256 | | byte values; bf16 represents integers exactly only up to 256 |
| 2^10 | 1,024 | ~10^3 (KiB) | |
| 2^11 | 2,048 | | fp16 represents integers exactly up to 2,048 |
| 2^16 | 65,536 | ~6.5 × 10^4 | uint16; TCP/UDP ports; fp16 max finite value is 65,504 |
| 2^20 | 1,048,576 | ~10^6 (MiB) | |
| 2^24 | 16,777,216 | ~1.7 × 10^7 | float32 represents integers exactly up to 2^24 |
| 2^30 | 1,073,741,824 | ~10^9 (GiB) | |
| 2^31 - 1 | 2,147,483,647 | ~2.1 × 10^9 | INT32_MAX: overflow in index math, `(lo + hi) / 2` |
| 2^32 | 4,294,967,296 | ~4.3 × 10^9 | uint32; IPv4 address count; 32-bit address space = 4 GiB |
| 2^40 | ~1.1 × 10^12 | ~10^12 (TiB) | |
| 2^50 | ~1.13 × 10^15 | ~10^15 (PiB) | |
| 2^53 | 9,007,199,254,740,992 | ~9 × 10^15 | float64 exact integers; JavaScript `Number.MAX_SAFE_INTEGER` is 2^53 - 1 |
| 2^63 - 1 | 9,223,372,036,854,775,807 | ~9.2 × 10^18 | INT64_MAX; nanoseconds overflow after ~292 years |
| 2^64 | ~1.8 × 10^19 | | uint64; 64-bit hash space (birthday bound ~5 × 10^9) |
| 2^128 | ~3.4 × 10^38 | | UUID / IPv6 space |

**Quick conversions:** log2(10^3) ≈ 10, log2(10^6) ≈ 20, log2(10^9) ≈ 30; so a balanced tree or binary search over 10^9 items takes ~30 steps. 10^k ≈ 2^(3.32k). KB/MB/GB (10^3 steps) vs KiB/MiB/GiB (2^10 steps) differ by 2.4% at kilo, 7.4% at giga, 10% at tera.

### 10.2 Time

| Quantity | Value | Quick-math version |
|---|---|---|
| Seconds per minute / hour | 60 / 3,600 | |
| Seconds per day | 86,400 | ~10^5 |
| Seconds per month (30 days) | 2,592,000 | ~2.6 × 10^6 |
| Seconds per year | 31,536,000 | ~π × 10^7 ≈ 3 × 10^7 |
| 1 million requests/day | ~12 QPS | |
| 1 billion requests/day | ~12,000 QPS | |
| 1 QPS sustained | 86,400/day, ~2.6M/month, ~31.5M/year | |
| CPU cycles per second at 3 GHz | 3 × 10^9 | 1 cycle ≈ 0.33 ns |

### 10.3 Availability ("nines")

| Availability | Downtime per year | Downtime per 30-day month |
|---|---|---|
| 99% | 3.65 days | 7.2 hours |
| 99.9% | 8.76 hours | 43.2 minutes |
| 99.95% | 4.38 hours | 21.6 minutes |
| 99.99% | 52.6 minutes | 4.3 minutes |
| 99.999% | 5.26 minutes | 26 seconds |

Serial dependencies multiply availabilities: three 99.9% services in series give 99.7%. Redundant replicas (independent failures) multiply unavailabilities: two 99% replicas give 1 - 0.01^2 = 99.99%, but correlated failures erase most of that gain.

### 10.4 Latency numbers (order of magnitude, modern hardware)

| Operation | Approximate time |
|---|---|
| CPU cycle at 3 GHz | 0.3 ns |
| L1 cache hit | ~1 ns |
| Branch mispredict | ~5 ns (15-20 cycles) |
| L2 cache hit | ~4 ns |
| Last-level cache hit | ~10-40 ns |
| Uncontended mutex lock/unlock | ~20 ns |
| Main memory (DRAM) access | ~80-100 ns |
| System call (simple) | ~0.1-1 µs |
| Thread context switch | ~1-5 µs |
| GPU kernel launch overhead (host side) | a few µs |
| Read 1 MB sequentially from DRAM | ~10-50 µs |
| NVMe 4 KB random read | ~10-100 µs |
| Round trip within a datacenter | ~100-500 µs |
| HDD seek | ~5-10 ms |
| Round trip across a continent | ~30-80 ms |
| Round trip across the Atlantic or Pacific | ~80-150 ms |

Memorize ratios rather than exact values: DRAM is ~100× L1; an in-datacenter RPC is ~1,000× a DRAM access; a cross-ocean round trip is ~1,000× an in-datacenter one.

### 10.5 Bandwidth and capacity anchors (as of 2026; check current specs)

| Item | Approximate value |
|---|---|
| PCIe Gen4 x16 / Gen5 x16 (per direction) | ~32 GB/s / ~64 GB/s theoretical |
| Ethernet / InfiniBand NIC 400 Gb/s | 50 GB/s |
| DDR5 per channel | ~40-50 GB/s |
| AMD Instinct MI300X HBM3 | 192 GB at ~5.3 TB/s peak |
| NVMe SSD (Gen4 / Gen5) | ~7 / ~14 GB/s sequential |
| AMD CDNA wavefront size | 64 lanes (NVIDIA warp: 32) |

### 10.6 Math constants and approximations

| Constant / approximation | Value | Use |
|---|---|---|
| e | 2.71828 | Uniforms-past-one, compound growth |
| 1/e | 0.3679 | Derangements, secretary problem, empty buckets when n = m |
| 1 - 1/e | 0.632 | P(at least one) when expected count is 1 |
| ln 2 | 0.693 | Half-life, birthday bound (√(2 ln 2) ≈ 1.177), rule of 70 |
| ln 10 | 2.303 | Converting log bases |
| log2(10) | 3.32 | Decimal digits to bits |
| √2, √3 | 1.414, 1.732 | Geometry |
| π | 3.14159 | π × 10^7 seconds in a year |
| Euler-Mascheroni γ | 0.5772 | H_n ≈ ln n + γ |
| (1 - 1/n)^n | ≈ 1/e | Probability a given bucket stays empty |
| (1 + x)^n | ≈ e^(nx) for small x | Compounding, failure probabilities |
| 1 - (1-p)^n | ≈ np when np is small | Union-bound regime |
| Stirling | n! ≈ √(2πn) (n/e)^n | log2(52!) ≈ 225.6 |
| Rule of 72 (or 70) | Doubling time ≈ 72 / (percent growth rate) | 10%/month growth doubles in ~7 months |
| Harmonic H_n | H_10 ≈ 2.93, H_100 ≈ 5.19, H_1000 ≈ 7.49 | Coupon collector, quicksort |

### 10.7 Interview Questions

**Q1.** Why does `int mid = (lo + hi) / 2;` overflow, and at what size?

If lo and hi are 32-bit signed ints and both exceed ~1.07 × 10^9 (2^30), their sum exceeds INT32_MAX (2^31 - 1 ≈ 2.1 × 10^9), which is undefined behavior in C++ and in practice wraps to a negative number. Use `lo + (hi - lo) / 2` or `std::midpoint` (C++20). This was a real bug in the JDK's binary search for years, found once arrays with over 2^30 elements became common.

**Q2.** A float32 accumulator counts events and stops increasing at 16,777,216. Why?

float32 has a 24-bit significand (23 stored bits plus the implicit leading 1), so above 2^24 the spacing between representable values is 2; adding 1 to 16,777,216 rounds back to 16,777,216 (round-to-nearest-even). Use integer counters, float64 (exact to 2^53), or Kahan/pairwise summation for floating-point sums. On GPUs, FP32 atomicAdd on large sums has the same problem plus non-deterministic ordering.

**Q3.** A service has a 99.95% SLO. How long can it be down per month, and what does that mean for deploys?

0.05% of 30 days ≈ 21.6 minutes per month. If a bad deploy takes 10 minutes to detect and 5 to roll back, two bad deploys exhaust the error budget. That pushes you toward canarying (limit blast radius to a few percent of traffic, so a bad deploy burns budget at a few percent of the rate), automated rollback, and progressive rollout.

**Q4.** Without a calculator, estimate how many 4 KB pages are in 64 GiB and how many entries a 4-level page table walk spans.

64 GiB / 4 KiB = 2^36 / 2^12 = 2^24 ≈ 16.8 million pages. With x86-64 4-level paging, each level indexes 9 bits (512 entries of 8 bytes in a 4 KiB table), plus a 12-bit page offset: 4 × 9 + 12 = 48-bit virtual addresses = 256 TiB. Huge pages (2 MiB = 2^21) reduce 64 GiB to 32,768 mappings, which is why they cut TLB misses for large GPU host buffers and databases.

---

## 11. Quick Reference

```text
COUNTING
  P(n,k) = n!/(n-k)!          C(n,k) = n!/(k!(n-k)!)         multiset perms: n!/(n1!...nr!)
  stars and bars: C(n+k-1, k-1) (xi ≥ 0),  C(n-1, k-1) (xi ≥ 1)
  derangements D(n) ≈ n!/e;   Catalan C_n = C(2n,n)/(n+1) = 1,1,2,5,14,42,132,429,1430
  lattice paths (m right, n up): C(m+n, n);  surjections n -> k: Σ (-1)^j C(k,j)(k-j)^n

PROBABILITY
  Bayes: posterior odds = prior odds × P(E given H)/P(E given not H)
  at least one: 1 - (1-p)^n ≈ 1 - e^(-np)
  linearity: E[Σ Xi] = Σ E[Xi] (no independence needed); indicators: E[count] = Σ P(event)
  tail sum: E[X] = Σ_{k≥1} P(X ≥ k);   max of n: P(max ≤ x) = F(x)^n

WAITING TIMES
  geometric: 1/p trials;  coupon collector: n H_n;  HH: 6, HT: 4, n heads: 2^(n+1)-2
  gambler's ruin (fair): P = k/N, duration k(N-k);  uniforms past 1: e

STATISTICS
  SE of mean = s/√n;  95% CI ≈ ±1.96 SE;  proportion SE = sqrt(p(1-p)/n);  zero events: ≤ 3/n
  sample size per arm ≈ 16 σ²/δ²;  P(any false positive in m tests) = 1 - (1-α)^m
  fan-out tail: 1 - 0.99^100 ≈ 63%

ESTIMATION
  86,400 s/day ≈ 10^5;  3 × 10^7 s/year;  1M/day ≈ 12 QPS;  2^10 ≈ 10^3
  training FLOPs ≈ 6 N D;  KV cache/token = 2 × layers × kv_heads × head_dim × bytes
  ring all-reduce bytes/GPU ≈ 2 × message size
```

**See also:**
- [DSA Fundamentals: Dynamic Programming](DSA_Fundamentals.md#20-dynamic-programming) (egg drop, optimal stopping as DP) and [Bit Manipulation](DSA_Fundamentals.md#24-bit-manipulation).
- [LeetCode Patterns: Subsets / Backtracking](LeetCode_Patterns.md#10-subsets--backtracking) for enumerating combinatorial objects.
- [High Level Design: Estimate the Workload](High_Level_Design.md#3-estimate-the-workload) and [HLD Mock Interviews](../practice/HLD_Mock_Interviews.md) for estimation in design rounds.
- [CS Fundamentals: Computer Architecture](CS_Fundamentals.md#7-computer-architecture) for the hardware behind the latency numbers.
- [Night Before Cheat Sheet](../practice/Night_Before_Cheat_Sheet.md) and [Flashcards](../practice/Flashcards.csv) for spaced review.
