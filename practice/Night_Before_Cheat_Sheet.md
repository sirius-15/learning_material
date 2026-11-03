# Night-Before Cheat Sheet -- Comprehensive Cross-Domain Recap

> Last reviewed: 2026-11 · Versions assumed: C++20 (GCC 13+ / Clang 17+), Python 3.12+, Linux 6.x, ROCm 6.4-7.x (rocprofv3, rocprof-compute 3.x), AMD Instinct MI300X (CDNA3) / MI355X (CDNA4) vendor-published peaks

> One dense pass over everything an interviewer can ask in a GPU/HPC, systems C++, ML-infra, or big-tech SWE loop: complexities, pattern triggers, OS and network numbers, latency numbers, concurrency rules, C++ and Python traps, a design checklist, a GPU performance checklist, and the STAR reminder. Every row links to the section that explains the *why*. Nothing here is new: if a line surprises you, follow its link instead of memorizing it. The [Rapid Self-Check](#12-rapid-self-check) at the end has answers in [Answers](#answers).

---

## Table of Contents

1. [How to Use This Sheet](#1-how-to-use-this-sheet)
2. [Complexities](#2-complexities)
3. [Pattern Triggers and the Coding-Round Flow](#3-pattern-triggers-and-the-coding-round-flow)
4. [OS and Network Numbers](#4-os-and-network-numbers)
5. [Latency, Bandwidth, and Estimation Numbers](#5-latency-bandwidth-and-estimation-numbers)
6. [Concurrency Rules](#6-concurrency-rules)
7. [C++ Rules of Thumb](#7-c-rules-of-thumb)
8. [Python Gotchas](#8-python-gotchas)
9. [Design Checklist](#9-design-checklist)
10. [GPU Performance Checklist](#10-gpu-performance-checklist)
11. [Behavioral STAR Reminder](#11-behavioral-star-reminder)
12. [Rapid Self-Check](#12-rapid-self-check)
- [Answers](#answers)

---

## 1. How to Use This Sheet

- **The night before:** read top to bottom once (about 30 minutes). Mark every line you cannot *explain* (not just recite). Open the linked deep section for those lines only.
- **The morning of:** reread only the section for each round on your schedule (coding: 2-3, systems: 4-7, design: 5 and 9, GPU: 10, behavioral: 11).
- **In the round:** numbers are for sanity checks, not for showing off. Derive them aloud ("5.3 TB/s times 600 ns is about 3 MB in flight") instead of quoting them. A derived number survives the follow-up question; a memorized one does not.
- **Logistics and the full day-of checklist:** [Interview Loops: Preparation Checklists](../career/Interview_Loops_and_Logistics.md#17-preparation-checklists) and [Behavioral: Day-of checklist](../career/Behavioral_Interview_Prep.md#112-day-of-checklist).

---

## 2. Complexities

**Data structures** ([DSA 25](../computer-science/DSA_Fundamentals.md#25-master-complexity-cheat-sheet), [which structure](../computer-science/DSA_Fundamentals.md#26-which-data-structure-should-i-use))

| Structure (C++ / Python) | Core operations | Trap to mention | Deep dive |
|---|---|---|---|
| Dynamic array (`vector` / `list`) | Index O(1); append O(1) amortized (geometric growth); insert/erase in the middle O(n) | `list.pop(0)` is O(n): use `deque`; reallocation invalidates every `vector` iterator | [DSA 1](../computer-science/DSA_Fundamentals.md#1-arrays-and-dynamic-arrays) |
| Hash map (`unordered_map` / `dict`) | Find/insert/erase O(1) average, O(n) worst | Adversarial keys and bad hashes; rehash invalidates iterators (not references in `unordered_map`) | [DSA 5](../computer-science/DSA_Fundamentals.md#5-hash-tables) |
| Balanced BST (`std::map`, `std::set`) | Find/insert/erase O(log n); ordered iteration; `lower_bound` | Python has no built-in: `sortedcontainers.SortedList` or bisect on a list (O(n) insert) | [DSA 7](../computer-science/DSA_Fundamentals.md#7-balanced-bsts-avl--red-black-trees), [Ordered containers](../computer-science/LeetCode_Patterns.md#29-ordered-containers) |
| Binary heap (`priority_queue` / `heapq`) | Push/pop O(log n); top O(1); build O(n) | `priority_queue` is a max-heap, `heapq` a min-heap; add a counter tie-breaker to tuples | [DSA 8](../computer-science/DSA_Fundamentals.md#8-heaps) |
| Deque / linked list | O(1) at both ends; O(1) erase at a known node; O(n) search | Linked lists lose to arrays in practice (cache misses) | [DSA 2](../computer-science/DSA_Fundamentals.md#2-linked-lists), [DSA 4](../computer-science/DSA_Fundamentals.md#4-queues) |
| Trie | O(L) per operation, L = key length | Memory: O(alphabet x nodes) | [DSA 10](../computer-science/DSA_Fundamentals.md#10-tries-prefix-trees) |
| Union-Find | O(alpha(n)), effectively constant, with path compression **and** union by rank/size | Either optimization alone gives O(log n) | [DSA 13](../computer-science/DSA_Fundamentals.md#13-disjoint-set-union-union-find) |
| Prefix sums / Fenwick / segment tree | Prefix: O(n) build, O(1) static range query. Fenwick and segment tree: O(log n) query and point update; segment tree with lazy propagation for range updates | Off-by-one: `sum(l..r) = P[r+1] - P[l]` | [DSA 11](../computer-science/DSA_Fundamentals.md#11-segment-trees), [DSA 12](../computer-science/DSA_Fundamentals.md#12-fenwick-trees-binary-indexed-trees) |

**Algorithms**

| Algorithm | Time | Space / property | Deep dive |
|---|---|---|---|
| Comparison sort lower bound | Omega(n log n) | Counting O(n+k) and radix O(d(n+k)) escape it by not comparing | [DSA 14](../computer-science/DSA_Fundamentals.md#14-sorting-algorithms) |
| Quicksort / merge sort / heapsort | Avg n log n; quicksort worst n^2 | Quick: O(log n) stack, unstable. Merge: O(n) extra, **stable**. Heap: O(1) extra, unstable | [DSA 14](../computer-science/DSA_Fundamentals.md#14-sorting-algorithms) |
| `std::sort` / `std::stable_sort` / Python `sorted` | O(n log n) worst (introsort) / O(n log n) / Timsort O(n log n), O(n) on sorted input | Only `stable_sort` and Timsort are stable | [Python Part 6 Q1](../languages/Python_Fundamentals.md#part-6-interview-questions) |
| Binary search | O(log n) | Use half-open `[lo, hi)` and `lo + (hi - lo) / 2` | [DSA 15](../computer-science/DSA_Fundamentals.md#15-searching-algorithms) |
| BFS / DFS / topological sort | O(V + E) | BFS gives unweighted shortest paths; Kahn's algorithm detects cycles (output size < V) | [DSA 16](../computer-science/DSA_Fundamentals.md#16-graph-traversals) |
| Dijkstra (binary heap) | O((V + E) log V) | Non-negative weights only; skip stale heap entries | [DSA 17](../computer-science/DSA_Fundamentals.md#17-shortest-path-algorithms) |
| 0-1 BFS / Bellman-Ford / Floyd-Warshall | O(V + E) / O(VE) / O(V^3) | Bellman-Ford handles negative edges and detects negative cycles; Floyd-Warshall is all-pairs | [Weighted shortest path](../computer-science/LeetCode_Patterns.md#27-weighted-shortest-path-patterns) |
| Kruskal / Prim | O(E log E) / O(E log V) | Kruskal = sort edges + Union-Find | [DSA 18](../computer-science/DSA_Fundamentals.md#18-minimum-spanning-tree) |
| DP classics | LIS O(n log n); LCS / edit distance O(mn); 0/1 knapsack O(nW) (pseudo-polynomial); bitmask DP O(2^n n) | Define state, transition, base case, order; then compress space | [DSA 20](../computer-science/DSA_Fundamentals.md#20-dynamic-programming), [LC 18](../computer-science/LeetCode_Patterns.md#18-dynamic-programming) |
| Master theorem `T(n) = aT(n/b) + f(n)` | Compare f(n) with n^(log_b a): merge sort `2T(n/2) + n` = n log n; binary search `T(n/2) + 1` = log n | Does not apply to uneven splits such as `T(n-1) + n` (that is n^2) | [Master theorem](../computer-science/DSA_Fundamentals.md#master-theorem) |

---

## 3. Pattern Triggers and the Coding-Round Flow

**Constraint to target complexity** (~10^8 simple operations per second is a safe budget) ([LC quick guide](../computer-science/LeetCode_Patterns.md#quick-reference-cheat-sheet)):

| n up to | 10-12 | 20 | 40 | 500 | 5,000 | 10^5 | 10^6-10^7 | 10^9+ |
|---|---|---|---|---|---|---|---|---|
| Target | n!, 2^n | 2^n n | 2^(n/2) n | n^3 | n^2 | n log n | n | log n or O(1) |
| Likely | Backtracking | Bitmask DP | Meet in the middle | Interval DP | 2-D DP | Sort, heap, binary search | Two pointers, window, hashing | Math, binary search |

**Keyword to pattern** ([full flowchart](../computer-science/LeetCode_Patterns.md#pattern-selection-flowchart))

| Signal in the prompt | Reach for | Deep dive |
|---|---|---|
| Sorted array, pair/triplet with a target sum | Two pointers | [LC 1](../computer-science/LeetCode_Patterns.md#1-two-pointers) |
| Longest/shortest contiguous subarray or substring, non-negative values | Sliding window (expand right, shrink left) | [LC 2](../computer-science/LeetCode_Patterns.md#2-sliding-window) |
| "Exactly K distinct" | `atMost(K) - atMost(K-1)` | [LC 2](../computer-science/LeetCode_Patterns.md#2-sliding-window) |
| Subarray sum equals / divisible by k, **negatives allowed** | Prefix sum + hash map of counts (seed `{0: 1}`) | [LC 21](../computer-science/LeetCode_Patterns.md#21-prefix-sum--difference-array) |
| Many range updates, then read | Difference array | [LC 21](../computer-science/LeetCode_Patterns.md#21-prefix-sum--difference-array) |
| Linked-list cycle or middle | Fast and slow pointers | [LC 3](../computer-science/LeetCode_Patterns.md#3-fast-and-slow-pointers) |
| Overlapping intervals; max concurrent meetings | Sort by start and merge; sweep +1/-1 events or a min-heap of end times | [LC 4](../computer-science/LeetCode_Patterns.md#4-merge-intervals), [LC 25](../computer-science/LeetCode_Patterns.md#25-line-sweep--advanced-intervals) |
| Values in `[1, n]`, find missing/duplicate in O(1) space | Cyclic sort or index marking | [LC 5](../computer-science/LeetCode_Patterns.md#5-cyclic-sort) |
| Shortest path, unweighted / grid | BFS (multi-source if many starts) | [LC 7](../computer-science/LeetCode_Patterns.md#7-bfs-breadth-first-search) |
| All subsets / permutations / combinations | Backtracking: choose, explore, unchoose | [LC 10](../computer-science/LeetCode_Patterns.md#10-subsets--backtracking) |
| Rotated array; "first index where..." | Modified binary search | [LC 11](../computer-science/LeetCode_Patterns.md#11-modified-binary-search) |
| "Minimize the maximum" / "smallest X such that" | Binary search on the answer with a monotone `feasible(x)` | [LC 28](../computer-science/LeetCode_Patterns.md#28-binary-search-on-the-answer) |
| Top K / K-th largest | Size-K heap, O(n log k); quickselect O(n) average | [LC 12](../computer-science/LeetCode_Patterns.md#12-top-k-elements) |
| Merge K sorted lists | Min-heap of K heads, O(N log K) | [LC 13](../computer-science/LeetCode_Patterns.md#13-k-way-merge) |
| Running median | Two heaps (max-heap low half, min-heap high half) | [LC 9](../computer-science/LeetCode_Patterns.md#9-two-heaps) |
| Dependencies / ordering / course schedule | Topological sort (Kahn) | [LC 14](../computer-science/LeetCode_Patterns.md#14-topological-sort) |
| Next greater/smaller; histogram area; sliding-window max | Monotonic stack / deque | [LC 15](../computer-science/LeetCode_Patterns.md#15-monotonic-stack--queue) |
| Dynamic connectivity; count components while adding edges | Union-Find | [LC 16](../computer-science/LeetCode_Patterns.md#16-union-find-disjoint-set) |
| Prefix lookup, autocomplete, word search on a board | Trie | [LC 17](../computer-science/LeetCode_Patterns.md#17-trie-prefix-tree) |
| Count ways / min cost / max value with overlapping subproblems | DP (greedy only with an exchange argument) | [LC 18](../computer-science/LeetCode_Patterns.md#18-dynamic-programming), [LC 19](../computer-science/LeetCode_Patterns.md#19-greedy) |
| Single number, subsets as masks, power of two | Bit manipulation (`x & (x - 1)` clears the lowest set bit) | [LC 20](../computer-science/LeetCode_Patterns.md#20-bit-manipulation) |
| Nested brackets, expression evaluation, decode string | Stack-based parsing | [LC 24](../computer-science/LeetCode_Patterns.md#24-stack-based-parsing) |
| LRU cache, O(1) insert/delete/getRandom | Hash map + doubly linked list; array + index map | [LC 26](../computer-science/LeetCode_Patterns.md#26-design-problems) |

**Coding-round flow** ([framework](../career/Interview_Loops_and_Logistics.md#7-the-coding-round-communication-framework)): clarify inputs, sizes, negatives, duplicates, and output format -> work 2 examples by hand (one tricky) -> state brute force and its complexity -> find the bottleneck and optimize -> state the invariant and get agreement -> code -> dry-run on your example -> edge cases -> complexity and follow-ups. **Edge cases to say aloud:** empty, one element, all equal, duplicates, negatives and zero, overflow (`int` sums past 2^31), sorted and reverse-sorted, disconnected graph or cycle, very large n. **Stuck?** Go back to brute force, list what it recomputes, and ask which structure removes the recomputation ([what to do when stuck](../career/Interview_Loops_and_Logistics.md#710-what-to-do-when-stuck)).

---

## 4. OS and Network Numbers

| Fact | Value and why it matters | Deep dive |
|---|---|---|
| Page / huge page / cache line (x86-64) | 4 KiB / 2 MiB and 1 GiB / 64 B. Huge pages raise TLB reach 512x per entry | [CS 1.11](../computer-science/CS_Fundamentals.md#111-linux-memory-management-internals), [Perf 5.8](../computer-science/Performance_Engineering.md#58-tlb-effects-and-huge-pages) |
| Context switch | ~1-5 us direct, plus cold caches and TLB afterwards | [CS 1.12](../computer-science/CS_Fundamentals.md#112-the-linux-scheduler), [Perf 1.2](../computer-science/Performance_Engineering.md#12-latency-numbers-to-know) |
| Uncontended mutex lock + unlock | ~15-25 ns: two atomic RMWs in user space. The futex syscall happens only under contention | [CS 6.10](../computer-science/CS_Fundamentals.md#610-lock-implementation-internals) |
| `fork()` | Copies page tables, not pages (copy-on-write); ~20 MB of page tables for a 10 GB resident process, hence `posix_spawn` / `vfork` | [CS 1.9](../computer-science/CS_Fundamentals.md#19-linux-process-lifecycle-signals-and-file-descriptors) |
| Deadlock (Coffman) | All four must hold: mutual exclusion, hold and wait, no preemption, circular wait. Break one (usually circular wait, via lock ordering) | [CS 1.4](../computer-science/CS_Fundamentals.md#14-deadlocks) |
| `select`/`poll` vs `epoll` vs `io_uring` | O(fds) scan per call vs O(ready) readiness events vs completion rings (batched or zero syscalls) | [CS 1.10](../computer-science/CS_Fundamentals.md#110-io-multiplexing-and-event-driven-servers) |
| `write` vs `fsync` | `write` lands in the page cache; durability needs `fsync`/`fdatasync` | [CS 1.11](../computer-science/CS_Fundamentals.md#111-linux-memory-management-internals) |
| Handshake RTTs before the first request | TCP 1 RTT; TCP + TLS 1.3 = 2 RTT; TCP + TLS 1.2 = 3 RTT; QUIC 1 RTT, or 0-RTT on resumption (replayable, so idempotent requests only) | [CS 2.9](../computer-science/CS_Fundamentals.md#29-tcp-internals-deep-dive), [CS 2.8](../computer-science/CS_Fundamentals.md#28-tlsssl-handshake) |
| Slow start | Linux initial window 10 MSS (MSS 1460 B on a 1500 B MTU); cwnd doubles per RTT, so small transfers are RTT-bound, not bandwidth-bound | [CS 2.9](../computer-science/CS_Fundamentals.md#29-tcp-internals-deep-dive) |
| TCP throughput | `<= min(rwnd, cwnd) / RTT`. BDP = bandwidth x RTT: 10 Gb/s x 50 ms = 62.5 MB in flight. Without window scaling (64 KiB) the same path gives ~10.5 Mb/s | [Flow vs congestion control](../computer-science/CS_Fundamentals.md#flow-control-vs-congestion-control) |
| TIME_WAIT | 60 s on Linux, held by the active closer. Ephemeral ports 32768-60999 = 28,232, so ~470 new connections/s to one destination 4-tuple. Fix with connection pooling / keep-alive | [TIME_WAIT](../computer-science/CS_Fundamentals.md#time_wait-why-it-exists-and-when-it-hurts) |
| Nagle + delayed ACK | Write-write-read pattern stalls ~40 ms per request on Linux; fix with `TCP_NODELAY` or one `send` per message | [Nagle](../computer-science/CS_Fundamentals.md#nagles-algorithm-delayed-acks-and-tcp_nodelay) |
| Headers / packet rate | TCP 20-60 B, UDP 8 B. 100 Gb/s with 1500 B frames is ~8.1 Mpps, ~123 ns per packet: less than one DRAM miss, hence kernel bypass and RDMA | [CS 2.10](../computer-science/CS_Fundamentals.md#210-hpc-and-datacenter-interconnects) |
| Isolation levels | Read committed stops dirty reads; repeatable read also stops non-repeatable reads; serializable also stops phantoms. Snapshot isolation still allows write skew | [CS 3.5](../computer-science/CS_Fundamentals.md#35-transactions-and-acid), [CS 3.10](../computer-science/CS_Fundamentals.md#310-concurrency-control-in-depth) |
| Quorums and consensus | `W + R > N` makes read and write sets overlap (not linearizable by itself). Raft/Paxos with 2f+1 nodes tolerate f failures | [CS 8.3](../computer-science/CS_Fundamentals.md#83-replication-strategies), [CS 8.12](../computer-science/CS_Fundamentals.md#812-consensus-theory-and-raft-in-depth) |
| CAP / PACELC | During a partition choose C or A; else trade latency vs consistency | [CS 3.7](../computer-science/CS_Fundamentals.md#37-cap-theorem-and-pacelc) |

Drill these as numeric problems in [CS Fundamentals Drills](CS_Fundamentals_Drills.md#2-numeric-problems).

---

## 5. Latency, Bandwidth, and Estimation Numbers

**Latency ladder** (memorize ratios, not digits) ([Perf 1.2](../computer-science/Performance_Engineering.md#12-latency-numbers-to-know), [HLD: latency numbers](../computer-science/High_Level_Design.md#latency-numbers-to-know), [measured ladder](../computer-science/Performance_Engineering.md#51-the-latency-ladder-measured))

| Operation | Rough figure | Operation | Rough figure |
|---|---|---|---|
| L1 hit | ~1 ns (4-5 cycles) | Context switch | ~1-5 us |
| Branch mispredict | ~3-5 ns | GPU kernel launch | a few us |
| L2 hit | ~3-4 ns | Send 1 KB at 1 Gb/s | ~8 us |
| L3 hit | ~10 ns | NVMe 4 KB random read (QD1) | ~20-100 us |
| Uncontended mutex | ~15-25 ns | Datacenter round trip | ~100-500 us (kernel TCP); 2-5 us RDMA |
| Local DRAM | ~80-130 ns | Read 1 MB sequentially from NVMe | ~150-350 us |
| Remote-socket DRAM | ~1.5-2x local | HDD seek | ~4-10 ms |
| GPU HBM load seen by a wave | several hundred ns to ~1 us | Cross-continent round trip | ~70-150 ms |

**Bandwidths** ([HLD: hardware bandwidths](../computer-science/High_Level_Design.md#hardware-bandwidths-memory-gpu-and-interconnect), [ML numbers](../ml-gpu/ML_Systems_Design.md#3-numbers-every-ml-systems-engineer-should-know)): DDR5-4800 channel 38.4 GB/s (12 channels ~460 GB/s per socket) · HBM3 MI300X 5.3 TB/s, MI355X 8.0 TB/s · PCIe 4.0 x16 ~32 GB/s and PCIe 5.0 x16 ~64 GB/s **per direction** · MI300X xGMI ~64 GB/s per direction per link, ~448 GB/s per direction over all 7 links · 400 Gb/s NIC = 50 GB/s · NVMe Gen4 ~7 GB/s. Ratios: HBM/PCIe5 ~80x; in-node/scale-out ~9x.

**Estimation conversions** ([HLD 3](../computer-science/High_Level_Design.md#3-estimate-the-workload), [Fermi](../computer-science/Math_Probability_Estimation.md#9-fermi-estimation), [powers of two](../computer-science/Math_Probability_Estimation.md#10-powers-of-two-and-handy-numbers)): 86,400 s/day (use 10^5) · 1M/day ~ 12/s · 100M/day ~ 1,200/s · 1B/day ~ 12,000/s · peak = 3-5x average · 2^10 ~ 10^3, 2^20 ~ 10^6, 2^30 ~ 10^9, 2^32 ~ 4.3 x 10^9 · 1 KB x 1B records ~ 1 TB before indexes and replicas.

**Availability** ([HLD: nines](../computer-science/High_Level_Design.md#availability-nines-and-downtime)): 99.9% = 8.77 h/year = 43.2 min/month · 99.99% = 52.6 min/year = 4.32 min/month · 99.999% = 5.26 min/year. Serial dependencies multiply (0.999^10 ~ 99.0%); redundant replicas in parallel give `1 - (1 - a)^k`.

**Laws** (state the formula, then plug in)

| Law | Formula | Worked number | Deep dive |
|---|---|---|---|
| Little's law | `L = lambda x W` | 2,000 req/s x 50 ms = 100 in flight; a 50-thread pool at 50 ms caps at 1,000 req/s | [Perf 4](../computer-science/Performance_Engineering.md#4-littles-law-and-queueing) |
| Amdahl | `S = 1 / ((1 - p) + p / N)`, max `1 / (1 - p)` | p = 0.95: at most 20x however many cores | [Perf 2.2](../computer-science/Performance_Engineering.md#22-amdahls-law) |
| Gustafson | `S = (1 - p) + p N` (problem grows with N) | Weak scaling; why big clusters still pay | [Perf 2.3](../computer-science/Performance_Engineering.md#23-gustafsons-law) |
| M/M/1 queue | `W = S / (1 - rho)`; p99 ~ 4.6 W | rho = 0.9 gives 10x the service time on average, 46x at p99 | [Perf 4.4](../computer-science/Performance_Engineering.md#44-utilization-vs-latency-mm1-and-beyond) |
| Fan-out tail | `P(slow) = 1 - (1 - q)^N` | N = 100 leaves at q = 1%: 63% of requests see a leaf p99 | [Perf 1.4](../computer-science/Performance_Engineering.md#14-tail-latency-and-fan-out-amplification) |
| Percentiles | Never average percentiles; merge histograms or sketches | Avg of p99s 115 ms vs true merged p99 205 ms | [Perf 1.3](../computer-science/Performance_Engineering.md#13-percentiles-and-why-the-mean-misleads) |

---

## 6. Concurrency Rules

([Pitfalls checklist](../computer-science/Concurrency_Coding_Problems.md#18-pitfalls-checklist), [CS 6](../computer-science/CS_Fundamentals.md#6-concurrency-and-multithreading), [C++ memory model](../languages/Cpp_Fundamentals.md#129-the-c-memory-model))

1. **Wait in a loop** on the predicate (`cv.wait(lk, pred)`): spurious and stolen wakeups are real.
2. **Change the predicate under the waiter's mutex**, even if the flag is atomic, or the notification can be lost forever.
3. **Mixed waiters on one condition variable** need `notify_all`, or use one condition variable per predicate.
4. **One global lock order** (by stable id, not address); `std::scoped_lock(a, b)` for two at once; handle `a == b`.
5. **Never hold a lock across I/O, callbacks, or unknown code.** Copy what you need, unlock, then call out.
6. **RAII for every lock and permit** (`lock_guard`, `scoped_lock`, `with`), so exceptions cannot leak a lock.
7. **A flag that publishes data needs release/acquire.** `relaxed` is fine for pure counters; `volatile` is never synchronization.
8. **Check-then-act is a race** across two critical sections; do it in one (`try_emplace`, `setdefault`).
9. **Join every thread** (`std::jthread`); a joinable `std::thread` destructor calls `std::terminate`.
10. **False sharing:** accumulate locally and pad per-thread data to 64 B (`alignas(64)`) ([Perf 5.6](../computer-science/Performance_Engineering.md#56-false-sharing-and-alignas64)).
11. **Every blocking wait needs a shutdown path:** a closed flag in the predicate plus `notify_all`, poison pills, or `stop_token`.
12. **CAS loops suffer ABA** when memory is recycled: tagged pointers, hazard pointers, or epoch reclamation.
13. **Spin only when the critical section is shorter than a context switch** and threads are pinned; otherwise spin-then-park.
14. **Pool sizing:** CPU-bound ~ cores; I/O-bound ~ `cores x (1 + wait / compute)` ([CS 6.6](../computer-science/CS_Fundamentals.md#66-thread-pools-and-executors)).
15. **Vocabulary:** deadlock = blocked, no CPU; livelock = busy, no progress; starvation = others progress, one thread never does. Lock-free = *some* thread always progresses; wait-free = *every* thread finishes in bounded steps. Lock-free is not automatically faster.
16. **Debug a hang:** `gdb -p PID -batch -ex "thread apply all bt"` (or `py-spy dump`), find who holds what, then reproduce under TSan with stress ([Debugging hangs](../tools/Debugging_and_Profiling_Tools.md#5-attaching-to-live-processes-and-debugging-hangs)).

---

## 7. C++ Rules of Thumb

| Rule | Why | Deep dive |
|---|---|---|
| Rule of 0 by default; if you write any of destructor/copy/move, consider all five | Owning members (`unique_ptr`, `vector`) give correct special members for free | [C++ 4.5](../languages/Cpp_Fundamentals.md#45-the-rule-of-zero--three--five) |
| Mark move constructor and move assignment `noexcept` | `vector` reallocation uses `move_if_noexcept`; a throwing move gets **copied** to keep the strong guarantee | [C++ 14.4](../languages/Cpp_Fundamentals.md#144-noexcept) |
| Polymorphic base needs a virtual (or protected non-virtual) destructor | `delete base_ptr` on a derived object is UB otherwise | [C++ 4.3](../languages/Cpp_Fundamentals.md#43-destructors) |
| `unique_ptr` by default; `shared_ptr` only for real shared ownership; `weak_ptr` breaks cycles | `shared_ptr` costs a control block and atomic refcounts; `make_shared` uses one allocation | [C++ 3.4](../languages/Cpp_Fundamentals.md#34-smart-pointers) |
| `std::move` is only a cast; do not `return std::move(local)` | It blocks NRVO; C++17 guarantees elision for prvalues | [C++ 5.3](../languages/Cpp_Fundamentals.md#53-stdmove), [C++ 5.5](../languages/Cpp_Fundamentals.md#55-return-value-optimization-rvo-and-named-rvo-nrvo) |
| `std::forward<T>` only on forwarding references (`T&&` with deduced `T`) | Preserves the value category | [C++ 5.4](../languages/Cpp_Fundamentals.md#54-stdforward-and-perfect-forwarding) |
| Iterator invalidation: `vector` reallocation invalidates everything; `unordered_*` rehash invalidates iterators but not references; `map`/`set`/`list` only the erased element; `deque` push at the ends invalidates iterators, not references | Most "random crash after insert" bugs | [C++ 8.2](../languages/Cpp_Fundamentals.md#82-iterator-invalidation-rules) |
| `string_view` / `span` / lambdas capturing by reference must not outlive the owner | `std::string_view sv = std::string("tmp");` dangles immediately | [C++ 10.6](../languages/Cpp_Fundamentals.md#106-stdstring_view), [Output quiz 6](Cpp_Output_Quiz.md#6-lifetime-temporaries-and-dangling) |
| Know the common UB list | Signed overflow, out-of-bounds, use-after-free, data race, uninitialized read, strict-aliasing violation (use `memcpy` / `std::bit_cast`) | [C++ 15.2](../languages/Cpp_Fundamentals.md#152-common-sources-of-undefined-behavior), [C++ 15.3](../languages/Cpp_Fundamentals.md#153-strict-aliasing-rule) |
| `map[k]` inserts a default value | Use `find`, `contains` (C++20), or `at` for lookups | [C++ 7.3](../languages/Cpp_Fundamentals.md#73-associative-containers-ordered), [Output quiz P49](Cpp_Output_Quiz.md#p49-looking-up-keys-in-a-stdmap) |
| `reserve` when the size is known; `emplace_back` constructs in place | Avoids reallocation and its invalidation | [C++ 7.2](../languages/Cpp_Fundamentals.md#72-sequence-containers) |
| Exception guarantees: nothrow, strong (commit or roll back; copy-and-swap), basic (valid but unspecified) | Destructors are `noexcept` by default; throwing from one during unwinding terminates | [C++ 14.3](../languages/Cpp_Fundamentals.md#143-exception-safety-guarantees) |
| Function-local statics are thread-safe since C++11 | Meyers singleton; avoids the static-initialization-order fiasco | [C++ 12.6](../languages/Cpp_Fundamentals.md#126-thread-safe-singleton-meyers-singleton) |
| ODR: header-defined functions and variables need `inline`; `extern "C"` turns off mangling | Duplicate-symbol link errors, or silent ODR violations | [C++ 13.2](../languages/Cpp_Fundamentals.md#132-translation-units-and-the-one-definition-rule-odr), [C++ 13.5](../languages/Cpp_Fundamentals.md#135-name-mangling-and-extern-c) |
| Build tests with `-fsanitize=address,undefined`; run TSan in a separate build | ASan and TSan cannot be combined | [Testing: sanitizers](../languages/CPP_Testing.md#33-sanitizers-with-googletest) |
| `volatile` is not atomic | Use `std::atomic` and a memory order | [C++ 2.4](../languages/Cpp_Fundamentals.md#24-volatile) |

**Self-test.** Run the timed 60-minute C++/CMake/testing mock in [Output Quiz 12](Cpp_Output_Quiz.md#12-timed-mock-interview-c-cmake-and-testing) at least once in the week before the loop. The night before, re-read only its [warm-up answers](Cpp_Output_Quiz.md#round-a-answers-warm-up) and your error log from that mock.

---

## 8. Python Gotchas

| Gotcha | Example and fix | Deep dive |
|---|---|---|
| Mutable default argument | `def f(x, acc=[])` shares one list across calls: use `acc=None` | [Py 27.1](../languages/Python_Fundamentals.md#271-mutable-default-arguments) |
| Late-binding closures | `[lambda: i for i in range(3)]` all return 2: bind with `lambda i=i: i` | [Py 27.2](../languages/Python_Fundamentals.md#272-late-binding-closures) |
| `is` vs `==` | `is` only for `None`/sentinels; small ints -5..256 are cached, so `is` "works" by accident | [Py 27.3](../languages/Python_Fundamentals.md#273-is-vs-), [Py 27.4](../languages/Python_Fundamentals.md#274-integer-caching-surprises) |
| Aliasing | `[[0] * 3] * 3` repeats one inner list; `a = b = []` is one list; `a += [x]` mutates a shared list but `t += (x,)` rebinds | [Py 27.7](../languages/Python_Fundamentals.md#277-chained-assignment-and-augmented-assignment), [Py 25](../languages/Python_Fundamentals.md#25-copy-semantics) |
| Shallow copy | `list(x)`, `x[:]`, `copy.copy` copy one level; nested data needs `copy.deepcopy` | [Py 25](../languages/Python_Fundamentals.md#25-copy-semantics) |
| Scope | Assigning to a name anywhere in a function makes it local (`UnboundLocalError`); use `nonlocal` / `global` | [Output quiz 9](Python_Output_Quiz.md#9-scope-rules) |
| Generators are single-use | A second `sum(gen)` returns 0 | [Py 7](../languages/Python_Fundamentals.md#7-iterators--generators) |
| Mutating while iterating | Resizing a dict during iteration raises `RuntimeError`; iterate over `list(d)` | [Output quiz 4](Python_Output_Quiz.md#4-dicts-sets--unpacking) |
| Integer and float arithmetic | `-7 // 2 == -4` and `-7 % 2 == 1` (floor semantics); `0.1 + 0.2 != 0.3`: use `math.isclose` | [Output quiz 6](Python_Output_Quiz.md#6-identity-equality--numbers) |
| Hidden O(n) | `list.pop(0)`, `x in list`, string `+=` in a loop, `sum(lists, [])`: use `deque`, `set`, `"".join`, `itertools.chain` | [Py Part 6 Q3](../languages/Python_Fundamentals.md#part-6-interview-questions) |
| `heapq` | Min-heap only; equal priorities compare payloads (`TypeError` on dicts): push `(prio, next(counter), item)` | [Py Part 6 Q2](../languages/Python_Fundamentals.md#part-6-interview-questions) |
| Recursion limit | Default 1000: deep DFS needs an explicit stack (or `sys.setrecursionlimit` plus care) | [OA pitfalls](../career/Interview_Loops_and_Logistics.md#4-online-assessments) |
| GIL | Threads help I/O, not CPU-bound pure Python: use `multiprocessing` / `ProcessPoolExecutor` or native code that releases the GIL. `x += 1` is **not** atomic | [Py 19](../languages/Python_Fundamentals.md#19-the-gil--threading), [Py 43 patterns](../design-patterns/Design_Patterns_Python.md#43-the-gil-and-choosing-a-concurrency-model) |
| asyncio | One blocking call (`time.sleep`, `requests.get`) stalls the whole loop: `await asyncio.to_thread(...)` or async libraries | [Py 21](../languages/Python_Fundamentals.md#21-asyncio--asyncawait) |
| Ordering facts | `dict` keeps insertion order (3.7+); `sorted` / `list.sort` are stable Timsort | [Py 2](../languages/Python_Fundamentals.md#2-built-in-data-types--structures) |

More traps as puzzles: [Python Output Quiz](Python_Output_Quiz.md), [pandas pitfalls](../languages/Pandas.md#37-common-pitfalls-and-interview-questions).

---

## 9. Design Checklist

**High-level design, 45 minutes** ([HLD 2](../computer-science/High_Level_Design.md#2-a-repeatable-interview-process), [HLD 7](../computer-science/High_Level_Design.md#7-interview-checklists-and-pitfalls), [rubric](HLD_Mock_Interviews.md#3-evaluation-rubric-by-level))

| Minutes | Step | Say out loud |
|---|---|---|
| 0-5 | Requirements | Functional list and explicit non-goals; scale, read/write ratio, latency SLO, availability, consistency, retention |
| 5-10 | Estimates and API | QPS (average and peak), storage x retention x replication, bandwidth; 3-5 endpoints with idempotency and pagination; core entities |
| 10-30 | Simplest architecture, then data flow | Trace one write and one read end to end; name the source of truth and what is derived |
| 30-40 | Scale and failure | Partition key and hot keys; cache with staleness and invalidation; queue with retries, DLQ, ordering; timeouts, retries with backoff and jitter, idempotency keys, backpressure, load shedding |
| 40-45 | Tradeoffs and summary | One alternative and why not; the biggest remaining risk; the metric that warns of saturation |

**Always cover:** observability (golden signals, USE, RED) ([HLD 5.4](../computer-science/High_Level_Design.md#54-observability-and-operations)), security and quotas ([HLD 5.3](../computer-science/High_Level_Design.md#53-security-and-privacy)), deployment safety ([HLD 5.9](../computer-science/High_Level_Design.md#59-deployment-safety)), cache stampede and hot keys ([HLD 4.13](../computer-science/High_Level_Design.md#413-cache-stampede-and-hot-keys)). **Per-node planning numbers** ([HLD: per-node throughput](../computer-science/High_Level_Design.md#typical-per-node-throughput)): app server 1k-10k req/s; Redis shard ~100k-200k ops/s; Postgres primary ~1k-20k small commits/s; Kafka partition ~10 MB/s conservative.

**Low-level design** ([LLD 2](../design-patterns/Low_Level_Design_Interview_Prep.md#2-a-repeatable-interview-method)): clarify -> public operations and errors -> invariants -> responsibilities (composition over inheritance; interfaces only at real seams) -> class diagram plus one sequence -> correctness under duplicate, concurrent, and failed operations -> tradeoffs -> summary. Pattern lookup: [C++ pattern cheat sheet](../design-patterns/Design_Patterns_Cpp.md#53-pattern-cheat-sheet), [SOLID](../design-patterns/Design_Patterns_Cpp.md#2-design-principles-solid-and-beyond).

**ML and HPC design** ([ML Sys 2](../ml-gpu/ML_Systems_Design.md#2-a-framework-for-ml-and-hpc-design-interviews), [checklists](../ml-gpu/ML_Systems_Design.md#11-cross-case-checklists-and-pitfalls)): start from the bottleneck resource (HBM capacity, HBM bandwidth, interconnect, or storage), size it with the numbers in [section 10](#10-gpu-performance-checklist), then place parallelism: tensor parallel inside a node, data parallel across nodes.

---

## 10. GPU Performance Checklist

**Roofline** ([Perf 3](../computer-science/Performance_Engineering.md#3-roofline-model), [rocprof-compute roofline](../career/Project_Deep_Dive_rocprof-compute.md#8-speed-of-light-memory-chart-and-roofline))

- `I = FLOPs / bytes`; `P = min(P_peak, I x B_peak)`; ridge `I* = P_peak / B_peak`. Left of the ridge: move fewer bytes. Right: use faster math. Far below both roofs: latency, occupancy, launch overhead, or divergence.
- **MI300X ridge points** (5.3 TB/s): FP64 vector 81.7 TF -> 15.4 FLOP/B · FP32 vector and matrix 163.4 TF -> 30.8 · BF16 matrix 1307.4 TF -> 246.7 · FP8 2614.9 TF -> 493.4 ([Perf 3.3](../computer-science/Performance_Engineering.md#33-ridge-points-mi300x-and-a-cpu)).
- **Kernel intensities (FP32):** vector add 1/12 = 0.083 · SAXPY 2/12 = 0.167 · GEMV ~0.5 · GEMM with ideal reuse n/6; with T x T tiles, T/4. Batch-1 LLM decode is GEMV-like, so memory-bound.
- **Time from first principles:** `bytes / bandwidth`. SAXPY on 2^28 floats = 3.22 GB / 5.3 TB/s = 608 us minimum; at 800 us it already reaches 76% of peak, so the only remaining win is fusion.
- The 163.4 TF FP32 vector peak needs **packed** FP32 (`v_pk_fma_f32`); scalar-per-lane FP32 tops out near 81.7 TF ([AMD 1.2](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md#12-simd16-x-4-and-the-four-cycle-wave64-cadence)).

**Occupancy (CDNA3/CDNA4, wave64)** ([AMD 1.4](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md#14-vgprs-agprs-and-occupancy-math))

- CU = 4 SIMD16; a wave64 VALU op takes 4 cycles; max 8 waves per SIMD (32 per CU). A masked-off lane still costs its slot (divergence).
- 512 VGPRs per lane per SIMD, shared by arch VGPRs and AGPRs, allocated in granules of 8: `waves/SIMD = min(8, floor(512 / VGPRs), LDS limit, ...)`. Cliffs: <=64 -> 8, <=96 -> 5, <=128 -> 4, <=256 -> 2.
- LDS limit: `WGs/CU = floor(LDS per CU / LDS per WG)`, with 64 KiB per CU on MI300X and 160 KiB on MI355X. Example: 24 KiB per 256-thread WG -> 2 WGs/CU -> 2 waves/SIMD = 25% on MI300X.
- `ScratchSize > 0` means spills to memory. Capping registers to raise occupancy can lose. Occupancy is a means: good GEMMs run 1-2 waves/SIMD and hide latency with ILP.
- Read resources from `--save-temps` / `-Rpass-analysis=kernel-resource-usage` or the rocprofv3 kernel trace (`VGPR_Count`, `LDS_Block_Size`, `Scratch_Size`).

**Latency hiding** ([AMD 3](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md#3-latency-hiding-quantified), [Perf 4.2](../computer-science/Performance_Engineering.md#42-memory-level-parallelism-bytes-in-flight)): bytes in flight = bandwidth x latency = 5.3 TB/s x ~600 ns ~ 3.2 MB ~ 10.5 KB per CU. Get there with more waves **or** more independent loads per thread (ILP, unrolling, 16-byte loads).

**Coalescing** ([AMD coalescing](../ml-gpu/Parallel_GPU_Programming.md#304-memory-coalescing-on-amd), [CUDA 20.1](../ml-gpu/Parallel_GPU_Programming.md#201-global-memory-coalescing)): consecutive lanes should touch consecutive addresses. 64 lanes x 4 B = 256 B = two 128 B vL1D lines; `float4` / `global_load_dwordx4` moves 16 B per lane. Prefer SoA to AoS; strided or random access multiplies transactions. Signals: high TA busy with low achieved bandwidth.

**LDS banks** ([AMD 1.6](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md#16-lds-size-banks-and-conflicts), [CUDA 20.2](../ml-gpu/Parallel_GPU_Programming.md#202-shared-memory-bank-conflicts)): 32 banks x 4 B, `bank = (byte_addr / 4) % 32`. Different addresses in one bank serialize; the same address broadcasts. Pad tiles (`tile[64][64 + 1]`) for column access. rocprof-compute "LDS Bank Conflicts/Access" (from `SQ_LDS_BANK_CONFLICT`) should be ~0. Worked transpose: [Case studies 2](../ml-gpu/GPU_Kernel_Case_Studies.md#2-matrix-transpose).

**Diagnosis order** ([AMD 5.5](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md#55-decision-tree-from-symptom-to-bottleneck), [AMD 4.4](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md#44-rocprof-compute)):

1. **Timeline first** (`rocprofv3 --runtime-trace` / rocprof-sys): gaps between kernels or many kernels under ~10 us means launch-bound -> fuse, HIP graphs, remove syncs ([fusion](../ml-gpu/GPU_Kernel_Case_Studies.md#7-elementwise-fusion-and-kernel-launch-overhead)).
2. **Speed-of-Light** (rocprof-compute block 2): the unit closest to its peak is the first suspect. Memory near roof -> cut bytes. VALU/MFMA near roof -> MFMA, packed math, lower precision.
3. **Nothing above ~50%:** latency-bound. Check occupancy limiter, grid size (`SQ_WAVES` vs CUs x 4 x target; 304 CUs on MI300X), tail effect, `s_waitcnt` hotspots in PC sampling, barriers, atomics.
4. **Check the traps:** VALU FLOPs assume full EXEC masks (check VALU Active Threads, ideal 64); L2-Fabric BW above HBM peak means Infinity Cache hits; occupancy is unreliable for very short kernels ([AMD 5.3](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md#53-derived-metrics-and-their-formulas)).
5. **Measure honestly:** warm up, time with events, report the median of many runs, and remember the profiler perturbs what it measures ([Perf 8.7](../computer-science/Performance_Engineering.md#87-timing-gpus), [AMD 5.7](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md#57-profiler-overhead-and-perturbation)).

**Correctness reminders:** wave size is 64 on CDNA, so ballots are 64-bit and `warpSize` must not be hard-coded to 32 ([wave64 porting](../ml-gpu/Parallel_GPU_Programming.md#367-porting-warp32-code-to-wave64-ballot-masks-and-other-traps)); cross-workgroup visibility needs scoped atomics and fences ([AMD 2](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md#2-gpu-memory-model)); float atomics and parallel reductions are non-deterministic because FP addition is not associative ([Perf 9.5](../computer-science/Performance_Engineering.md#95-why-parallel-and-gpu-reductions-are-non-deterministic)).

**ML numbers** ([LLM 14](../ml-gpu/LLM_and_ML_Fundamentals.md#14-formula-cheat-sheet), [ML Sys 3.3](../ml-gpu/ML_Systems_Design.md#3-numbers-every-ml-systems-engineer-should-know)): inference ~2N FLOPs/token; training ~6ND · KV cache per token = `2 x layers x kv_heads x head_dim x bytes` (70B GQA: 320 KiB BF16) · mixed-precision Adam = 16 B/param (70B: 1.12 TB before activations) · batch-1 decode step ~ weight bytes / HBM BW = 141 GB / 5.3 TB/s ~ 27 ms · ring all-reduce sends `2(p - 1)/p x S` per rank ([collectives](../ml-gpu/Parallel_GPU_Programming.md#343-ring-allreduce--reduce-scatter--all-gather)).

---

## 11. Behavioral STAR Reminder

([STAR and CARL](../career/Behavioral_Interview_Prep.md#2-answer-formats-star-and-carl), [anti-patterns](../career/Behavioral_Interview_Prep.md#9-anti-patterns), [project pitches](../career/Project_Deep_Dive_rocprof-compute.md#2-the-pitches))

| Part | Share of a 2-3 minute answer (~300-450 words) | Content |
|---|---|---|
| **S**ituation | ~10-15% | Team, system, stakes: two or three sentences |
| **T**ask | ~5-10% | *Your* responsibility and why it was hard |
| **A**ction | ~55-65% | What *I* did, options considered, why this one, how I handled people |
| **R**esult | ~15-20% | Numbers before and after, what happened next, one learning |

- **Say "I" for your actions and "we" only for team outcomes.** Quantify every result. Stop after the result and let them drill down.
- **Failure and feedback questions:** STAR + Learning (CARL); use the own-fix-prevent frame ([6.1](../career/Behavioral_Interview_Prep.md#61-failure-answers-the-own-fix-prevent-frame)). **Conflict:** understand-align-resolve-repair ([6.2](../career/Behavioral_Interview_Prep.md#62-conflict-answers-the-understand-align-resolve-repair-frame)). **Technical disagreement:** evidence ladder, data before opinions ([6.3](../career/Behavioral_Interview_Prep.md#63-technical-disagreement-the-evidence-ladder)).
- **Story bank:** 10-12 stories covering conflict, failure, ambiguity, influence, ownership, mentoring, prioritization, deadline, customer, and disagreement ([coverage matrix](../career/Behavioral_Interview_Prep.md#36-coverage-matrix)). Know each story's one-line headline and its numbers.
- **"Tell me about yourself" in ~90 s:** present (30 s) -> past (25 s) -> strengths (15 s) -> why here (15 s) -> handoff ([template](../career/Behavioral_Interview_Prep.md#7-tell-me-about-yourself-the-90-second-template)).
- **Confidentiality:** abstract unreleased details and say "that is not public" ([3.5](../career/Behavioral_Interview_Prep.md#35-confidentiality-talking-about-current-work-safely)). Have 3-4 questions ready for each interviewer ([10](../career/Behavioral_Interview_Prep.md#10-questions-to-ask-the-interviewer)).

---

## 12. Rapid Self-Check

Answer each aloud in under 60 seconds, then check [Answers](#answers).

**Q1.** n = 10^5 and you need the number of subarrays with sum exactly k; values can be negative. Which pattern, and why not a sliding window?

**Q2.** A client opens a new TCP connection per request to one server and starts failing above roughly 470 requests per second. Why?

**Q3.** A kernel uses 100 VGPRs, no AGPRs, and 16 KiB of LDS per 256-thread workgroup on MI300X. What is its occupancy, and which resource binds?

**Q4.** Why does `std::vector<T>` copy instead of move elements on reallocation for some `T`?

**Q5.** A page fans out to 50 backends in parallel, each with a 1% chance of exceeding its p99. What fraction of page loads see at least one slow backend?

**Q6.** What does `[f() for f in [lambda: i for i in range(3)]]` return, and how do you fix it?

**Q7.** Is an FP32 elementwise kernel `y = a*x + b` on MI300X compute-bound or memory-bound? What is the only way to make it substantially faster?

**Q8.** A 32 x 32 FP32 tile in LDS is read column-wise by 32 lanes. How many lanes conflict, and what is the fix?

---

## Answers

**A1.** Prefix sum plus a hash map of prefix counts, seeded with `{0: 1}`: for each prefix `P`, add `count[P - k]`, then increment `count[P]`. O(n) time, O(n) space. A sliding window needs monotonicity: with non-negative values, growing the window never decreases the sum, so you can shrink from the left safely. Negative values break that, so a window cannot decide when to shrink ([LC 21](../computer-science/LeetCode_Patterns.md#21-prefix-sum--difference-array), [worked round](../career/Interview_Loops_and_Logistics.md#8-worked-coding-round-subarray-sum-equals-k)).

**A2.** Ephemeral-port exhaustion caused by TIME_WAIT. The active closer (the client) holds each 4-tuple for 60 s on Linux, and the default ephemeral range 32768-60999 has 28,232 ports, so one source IP can open about 28,232 / 60 = ~470 new connections per second to one destination IP and port. The real fix is connection pooling or keep-alive. `tcp_tw_reuse`, a wider port range, or more source IPs only add linear headroom ([TIME_WAIT](../computer-science/CS_Fundamentals.md#time_wait-why-it-exists-and-when-it-hurts)).

**A3.** VGPRs: 100 rounds up to 104 (granule 8), and `floor(512 / 104) = 4` waves/SIMD. LDS: `floor(64 KiB / 16 KiB) = 4` workgroups per CU x 4 waves each = 16 waves per CU = 4 waves/SIMD. Both limits give 4 of 8, so occupancy is 50%, with VGPRs and LDS tied. Reducing only one of them gains nothing. Check `ScratchSize` before forcing fewer registers ([AMD 1.4](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md#14-vgprs-agprs-and-occupancy-math)).

**A4.** Reallocation offers the strong exception guarantee: if anything throws, the old buffer is unchanged. Moving elements destroys the source state, so a move constructor that might throw halfway through would leave the vector unrecoverable. `vector` therefore uses `std::move_if_noexcept`: it moves only if the move constructor is `noexcept` (or the type is not copyable) and copies otherwise. Declare move operations `noexcept` ([C++ 14.4](../languages/Cpp_Fundamentals.md#144-noexcept), [C++ 16.3](../languages/Cpp_Fundamentals.md#163-vectort-placement-new-growth-and-the-strong-guarantee)).

**A5.** `1 - 0.99^50 = 1 - 0.605 = ~39.5%`. Leaf tails become the page's common case; mitigations are hedged requests, fewer dependencies on the critical path, and per-call deadlines with partial results ([Perf 1.4](../computer-science/Performance_Engineering.md#14-tail-latency-and-fan-out-amplification)).

**A6.** `[2, 2, 2]`. Each lambda looks up `i` when it is *called*, and by then the comprehension's `i` is 2. Bind the current value at definition time: `lambda i=i: i` (or `functools.partial`) ([Py 27.2](../languages/Python_Fundamentals.md#272-late-binding-closures)).

**A7.** Memory-bound by a factor of about 120. It does 2 FLOPs (one FMA) per 8 bytes (read `x`, write `y`), so `I = 0.25 FLOP/B`, against an FP32 ridge point of 30.8 FLOP/B (30.8 / 0.25 = ~123). Attainable throughput is `0.25 x 5.3 TB/s = 1.3 TFLOP/s`. Faster math is irrelevant; the wins are moving fewer bytes, mainly fusing it into the producer or consumer kernel, or using a smaller data type, plus coalesced 16-byte loads to reach achievable bandwidth ([Perf 3.2](../computer-science/Performance_Engineering.md#32-arithmetic-intensity-worked-examples)).

**A8.** With a row stride of 32 words, element `[r][c]` sits at word `32r + c`, so `bank = (32r + c) % 32 = c`. All 32 lanes reading column `c` hit the same bank at different addresses: a 32-way conflict, so the access serializes into 32 LDS cycles. Pad the row to 33 words (`tile[32][33]`): the bank becomes `(33r + c) % 32 = (r + c) % 32`, which differs for every row, so the access is conflict-free. Verify with the LDS bank-conflict metric ([AMD 1.6](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md#16-lds-size-banks-and-conflicts), [transpose ladder](../ml-gpu/GPU_Kernel_Case_Studies.md#2-matrix-transpose)).

---

**See also:** [Flashcards](Flashcards.csv) for spaced repetition · [CS Fundamentals Drills](CS_Fundamentals_Drills.md) · [Coding Problem List](Coding_Problem_List.md) · [HLD Mock Interviews](HLD_Mock_Interviews.md) · [C++ Output Quiz](Cpp_Output_Quiz.md) · [Python Output Quiz](Python_Output_Quiz.md) · [Interview Loops and Logistics](../career/Interview_Loops_and_Logistics.md)
