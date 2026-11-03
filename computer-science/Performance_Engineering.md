# Performance Engineering -- Comprehensive Interview Reference

> Last reviewed: 2026-11 · Versions assumed: GCC 13-15 / Clang 17+ (`-std=c++20`), Linux 6.x, AMD Instinct MI300X (CDNA 3) vendor-published peaks, rocprof-compute 3.x, Google Benchmark 1.8+

> An interview-focused reference for reasoning about performance quantitatively: latency and tail latency, scaling laws, the roofline model, Little's law and queueing, cache- and NUMA-aware C++, SIMD, rigorous benchmarking statistics, and floating-point reproducibility. Every section ends with interview questions and full answers. Targeted at GPU/HPC, systems C++, ML-infra, and general big-tech SWE loops.

All complete C++ programs in this file compile with `g++ -std=c++20 -O2` (add `-mavx2 -mfma`, `-fopenmp`, or `-pthread` where the build line says so). Measured numbers come from one 2-socket AMD EPYC (Zen 5) Linux server, with the process pinned via `taskset`. Treat them as *illustrations of ratios*. Your absolute numbers will differ.

---

## Table of Contents

1. [Latency vs Throughput, Percentiles, and Tail Latency](#1-latency-vs-throughput-percentiles-and-tail-latency)
    - [1.1 Latency, Throughput, Bandwidth](#11-latency-throughput-bandwidth)
    - [1.2 Latency Numbers to Know](#12-latency-numbers-to-know)
    - [1.3 Percentiles and Why the Mean Misleads](#13-percentiles-and-why-the-mean-misleads)
    - [1.4 Tail Latency and Fan-Out Amplification](#14-tail-latency-and-fan-out-amplification)
    - [1.5 Interview Questions](#15-interview-questions)
2. [Amdahl's and Gustafson's Laws](#2-amdahls-and-gustafsons-laws)
    - [2.1 Speedup, Efficiency, Cost](#21-speedup-efficiency-cost)
    - [2.2 Amdahl's Law](#22-amdahls-law)
    - [2.3 Gustafson's Law](#23-gustafsons-law)
    - [2.4 Strong vs Weak Scaling](#24-strong-vs-weak-scaling)
    - [2.5 Overheads, Karp-Flatt, and Load Imbalance](#25-overheads-karp-flatt-and-load-imbalance)
    - [2.6 Interview Questions](#26-interview-questions)
3. [Roofline Model](#3-roofline-model)
    - [3.1 The Model](#31-the-model)
    - [3.2 Arithmetic Intensity Worked Examples](#32-arithmetic-intensity-worked-examples)
    - [3.3 Ridge Points: MI300X and a CPU](#33-ridge-points-mi300x-and-a-cpu)
    - [3.4 Hierarchical and Cache-Aware Roofline](#34-hierarchical-and-cache-aware-roofline)
    - [3.5 Measured vs Theoretical Ceilings](#35-measured-vs-theoretical-ceilings)
    - [3.6 Interview Questions](#36-interview-questions)
4. [Little's Law and Queueing](#4-littles-law-and-queueing)
    - [4.1 Little's Law](#41-littles-law)
    - [4.2 Memory-Level Parallelism: Bytes in Flight](#42-memory-level-parallelism-bytes-in-flight)
    - [4.3 Sizing a Server with Little's Law](#43-sizing-a-server-with-littles-law)
    - [4.4 Utilization vs Latency: M/M/1 and Beyond](#44-utilization-vs-latency-mm1-and-beyond)
    - [4.5 Interview Questions](#45-interview-questions)
5. [Memory Hierarchy Programming](#5-memory-hierarchy-programming)
    - [5.1 The Latency Ladder (Measured)](#51-the-latency-ladder-measured)
    - [5.2 Address Breakdown: Tag, Set, Offset](#52-address-breakdown-tag-set-offset)
    - [5.3 Row-Major vs Column-Major Traversal](#53-row-major-vs-column-major-traversal)
    - [5.4 Loop Interchange and Tiling for Matmul](#54-loop-interchange-and-tiling-for-matmul)
    - [5.5 AoS vs SoA](#55-aos-vs-soa)
    - [5.6 False Sharing and alignas(64)](#56-false-sharing-and-alignas64)
    - [5.7 Prefetching](#57-prefetching)
    - [5.8 TLB Effects and Huge Pages](#58-tlb-effects-and-huge-pages)
    - [5.9 Interview Questions](#59-interview-questions)
6. [SIMD and Vectorization](#6-simd-and-vectorization)
    - [6.1 SIMD Widths and ISA Extensions](#61-simd-widths-and-isa-extensions)
    - [6.2 Intrinsics: SSE, AVX2, AVX-512](#62-intrinsics-sse-avx2-avx-512)
    - [6.3 Runtime Dispatch](#63-runtime-dispatch)
    - [6.4 Auto-Vectorization and Compiler Reports](#64-auto-vectorization-and-compiler-reports)
    - [6.5 Aliasing, restrict, and Alignment](#65-aliasing-restrict-and-alignment)
    - [6.6 Interview Questions](#66-interview-questions)
7. [NUMA](#7-numa)
    - [7.1 NUMA Topology](#71-numa-topology)
    - [7.2 First-Touch Placement](#72-first-touch-placement)
    - [7.3 numactl, Binding, and APIs](#73-numactl-binding-and-apis)
    - [7.4 NUMA and GPUs](#74-numa-and-gpus)
    - [7.5 Interview Questions](#75-interview-questions)
8. [Benchmarking Rigor](#8-benchmarking-rigor)
    - [8.1 Sources of Noise](#81-sources-of-noise)
    - [8.2 Controlling the Environment](#82-controlling-the-environment)
    - [8.3 A Minimal Honest Harness](#83-a-minimal-honest-harness)
    - [8.4 Statistics: Mean, Median, Variance, Confidence Intervals, Outliers](#84-statistics-mean-median-variance-confidence-intervals-outliers)
    - [8.5 A/B Methodology](#85-ab-methodology)
    - [8.6 Google Benchmark](#86-google-benchmark)
    - [8.7 Timing GPUs](#87-timing-gpus)
    - [8.8 Profiler Overhead and the Observer Effect](#88-profiler-overhead-and-the-observer-effect)
    - [8.9 Interview Questions](#89-interview-questions)
9. [Floating-Point Numerics and Reproducibility](#9-floating-point-numerics-and-reproducibility)
    - [9.1 Precision Cheat Sheet](#91-precision-cheat-sheet)
    - [9.2 Non-Associativity](#92-non-associativity)
    - [9.3 Catastrophic Cancellation](#93-catastrophic-cancellation)
    - [9.4 Compensated and Pairwise Summation](#94-compensated-and-pairwise-summation)
    - [9.5 Why Parallel and GPU Reductions Are Non-Deterministic](#95-why-parallel-and-gpu-reductions-are-non-deterministic)
    - [9.6 Reproducibility Strategies](#96-reproducibility-strategies)
    - [9.7 Comparing Floats: ULP, rtol, atol](#97-comparing-floats-ulp-rtol-atol)
    - [9.8 Denormals, FMA Contraction, and fast-math](#98-denormals-fma-contraction-and-fast-math)
    - [9.9 Interview Questions](#99-interview-questions)
10. [Interview Q&A](#10-interview-qa)

- [Further Reading](#further-reading)

---

# 1. Latency vs Throughput, Percentiles, and Tail Latency

---

## 1.1 Latency, Throughput, Bandwidth

| Term | Definition | Units | Example |
|---|---|---|---|
| **Latency** | Time for *one* operation from start to finish | s, ms, us, ns, cycles | One DRAM load ~100 ns; one HTTP request 20 ms |
| **Throughput** | Operations completed per unit time | ops/s, req/s, FLOP/s | 50k req/s; 160 TFLOP/s |
| **Bandwidth** | Throughput measured in bytes | B/s | HBM3 on MI300X: 5.3 TB/s peak |
| **Concurrency** | Operations in progress at the same time | count | 100 requests in flight; 24 outstanding cache misses |

The three are linked by **Little's law** (Section 4): `concurrency = throughput x latency`. That one formula explains most of performance engineering:

- **Pipelining and parallelism raise throughput without lowering latency.** A GPU has a *worse* single-load latency than a CPU, but it keeps tens of thousands of loads in flight, so its bandwidth is about 10x higher.
- **Batching trades latency for throughput.** LLM serving batches requests to raise GPU utilization, and each request waits longer.
- **Lowering latency raises throughput only when concurrency is fixed.** A single-threaded pointer chase is an example: the next load cannot start until the current one returns.

```text
latency-bound:     A ----> B ----> C ----> D        (each step waits for the previous)
throughput-bound:  A ---->
                     B ---->
                       C ---->                       (overlapped; rate limited by a resource)
                         D ---->
```

**How to tell which one you have.** If doubling the available concurrency (threads, outstanding requests, waves per CU) nearly doubles throughput, you were latency-bound. If throughput stays flat, a shared resource is saturated (DRAM bandwidth, a lock, a NIC, an ALU pipe), and you are throughput-bound.

## 1.2 Latency Numbers to Know

These are orders of magnitude, so memorize the ratios rather than the digits. The cache and DRAM rows were measured with the pointer-chase program in [5.1](#51-the-latency-ladder-measured).

| Operation | Approximate latency | Notes |
|---|---|---|
| Register op / L1 hit | ~1 ns (4-5 cycles) | Measured 0.9 ns for a 16 KiB working set |
| L2 hit | ~3 ns | Measured 3.1 ns for 64-256 KiB |
| L3 hit | ~10 ns | Measured 10-12 ns for 4-16 MiB |
| Local DRAM | ~80-130 ns | Measured 90-130 ns for 64 MiB-1 GiB; includes TLB misses |
| Remote-socket DRAM (NUMA) | ~1.5-2x local | See Section 7 |
| GPU HBM load (from a wave) | Several hundred ns to ~1 us | Higher than CPU DRAM; hidden by occupancy |
| GPU kernel launch (host to start) | A few us | Why tiny kernels and CUDA/HIP Graphs matter |
| Mutex lock/unlock, uncontended | ~10-25 ns | Contended locks cost far more |
| Context switch | ~1-5 us direct | Plus cold caches and TLB afterwards |
| NVMe SSD random read | ~10-100 us | |
| Same-datacenter round trip | ~0.1-0.5 ms | |
| Cross-continent round trip | ~70-150 ms | Bounded by the speed of light in fibre |

## 1.3 Percentiles and Why the Mean Misleads

Latency distributions are **right-skewed and often multimodal**. Typical causes are cache hits vs misses, GC pauses, retries, and lock convoys. The mean mixes the modes together and describes almost no real request. For that reason latency is reported as percentiles:

- **p50 (median):** the typical request.
- **p99 / p99.9:** the tail. At 1M requests/day, the slowest 0.1% beyond p99.9 is still 1,000 requests every day (and with many requests per page or session, a much larger share of users).
- **max:** useful as an alarm, but too noisy to set an SLO on.

**Nearest-rank definition:** the p-th percentile is the smallest sample `x` such that at least `p%` of the samples are `<= x`.

```python
"""pct.py -- percentiles, why the mean misleads, and why you cannot average percentiles."""
import math
import random
import statistics as st


def percentile(sorted_xs, p):
    """Nearest-rank percentile: smallest sample with at least p% of samples <= it."""
    k = max(1, math.ceil(p / 100 * len(sorted_xs)))
    return sorted_xs[k - 1]


rng = random.Random(0)
# Host A is healthy; host B has a 2% slow path (e.g. GC pause, cache miss to a remote store).
a = sorted(rng.lognormvariate(math.log(10), 0.3) for _ in range(10_000))
b = sorted(rng.lognormvariate(math.log(10), 0.3) + (200 if rng.random() < 0.02 else 0)
           for _ in range(10_000))
both = sorted(a + b)

for name, xs in (("A", a), ("B", b), ("A+B", both)):
    print(f"{name:3s} mean={st.mean(xs):6.1f}  p50={percentile(xs, 50):5.1f}  "
          f"p99={percentile(xs, 99):6.1f}  p99.9={percentile(xs, 99.9):6.1f}  ms")
print(f"average of per-host p99s = {(percentile(a, 99) + percentile(b, 99)) / 2:.1f} ms  (wrong)")
print(f"p99 of merged samples    = {percentile(both, 99):.1f} ms  (right)")
```

```text
A   mean=  10.5  p50= 10.0  p99=  20.0  p99.9=  24.2  ms
B   mean=  14.6  p50= 10.0  p99= 209.7  p99.9= 214.5  ms
A+B mean=  12.6  p50= 10.0  p99= 205.5  p99.9= 213.4  ms
average of per-host p99s = 114.9 ms  (wrong)
p99 of merged samples    = 205.5 ms  (right)
```

Takeaways:

1. **The mean (12.6 ms) hides a 200 ms mode that 1% of all users hit.** The p50 is identical on both hosts. Only the tail shows the problem.
2. **Percentiles cannot be averaged.** Averaging percentiles is not the same as taking the percentile of the union. Dashboards that show "average p99 across hosts" are wrong. Aggregate **histograms** instead, using fixed-bucket histograms such as HdrHistogram or Prometheus histograms, or mergeable sketches such as t-digest or DDSketch, and compute the percentile from the merged structure.
3. **Coordinated omission.** A closed-loop load generator ("send the next request after the previous one returns") stops sending while the server is stalled. It therefore records one slow sample instead of the hundreds that real, open-loop users would have experienced, and the tail is under-reported by orders of magnitude. Use open-loop (fixed-rate) load generators such as wrk2, or correct the recorded data.
4. **You need enough samples.** Estimating p99.9 needs well over 1,000 samples (rule of thumb: at least 10/(1-p), so 10,000 for p99.9). Below that, you are mostly reading the maximum.

## 1.4 Tail Latency and Fan-Out Amplification

A front-end request that fans out to `N` leaf servers in parallel must wait for **the slowest leaf**. Suppose each leaf independently exceeds its own p99 latency with probability `q = 0.01`:

```text
P(request is slow) = P(at least one leaf is slow) = 1 - (1 - q)^N
```

| Fan-out N | P(request sees >= 1 leaf-p99 event) |
|---|---|
| 1 | 1.0% |
| 10 | 9.6% |
| 100 | **63.4%** |
| 1000 | ~100% |

So with 100 leaves, **the leaf p99 becomes the median user experience**. This is the central argument of Dean and Barroso's "The Tail at Scale" (CACM 2013).

**Inverting the formula (an SLO budgeting question).** For the request-level p99 to stay within the leaf latency `L`, each leaf must satisfy `(1 - q)^N >= 0.99`, so `q <= 1 - 0.99^(1/N) ~= 0.01/N`. For `N = 100`, `q ~= 0.0001`. **The leaves must meet `L` at p99.99**, two more nines than the front-end.

**Mitigations:**

| Technique | Idea | Cost |
|---|---|---|
| **Hedged requests** | After the p95 latency, send a duplicate to another replica and use whichever returns first | ~5% extra load; cuts the tail dramatically |
| **Tied requests** | Enqueue on two replicas; when one starts, it cancels the other | Cancellation messages |
| **Micro-partitioning** | Many small shards per server, so a slow server can shed work at fine grain | Metadata, rebalancing |
| **Partial results / deadlines** | Return what is ready by the deadline (search, ads) | Lower quality for a fraction of requests |
| **Reduce variance at the source** | Isolate background work (GC, compaction, log rotation), use priority queues, avoid head-of-line blocking | Engineering effort |

**The same math in HPC and GPU work.** A bulk-synchronous step (an MPI or RCCL all-reduce, or a training iteration across 512 GPUs) completes at `max` over ranks. A single straggler (thermal throttling, a noisy neighbour, a slow NIC) slows the whole job. That is fan-out amplification with `N = number of ranks`. Inside one GPU kernel the same effect appears as the **tail effect**: the last partial wave of workgroups runs while most CUs sit idle (see [2.5](#25-overheads-karp-flatt-and-load-imbalance)).

> **See also:** [High-Level Design -- Observability and operations](./High_Level_Design.md#54-observability-and-operations) for SLO/SLI framing; [Math, Probability, and Estimation](./Math_Probability_Estimation.md) for more probability practice.

## 1.5 Interview Questions

**Q1.** Your service's mean latency improved by 10% after a change, but users complain it feels slower. How is that possible?

The mean is dominated by the bulk of the distribution. The change probably made the common case faster and the tail slower. A new cache could do this: hits got faster, but misses now pay a cache lookup plus the original cost, or a new lock causes rare convoys. Users notice the tail, and with fan-out the tail of a dependency becomes the typical latency of a page. Compare the full distributions (p50, p90, p99, p99.9, and a histogram or CDF) before and after, preferably with an A/B run under identical load. Also check whether throughput changed. A faster mean at lower load says nothing about latency at peak load because of queueing (Section 4).

**Q2.** A page calls 40 backends in parallel. Each backend's p99 is 50 ms and p50 is 5 ms. Roughly what is the page's median latency?

P(no backend exceeds its p99) = `0.99^40 ~= 0.669`. So about 33% of page loads see at least one call slower than 50 ms, and the page's p67 is roughly 50 ms or more. The page median is set by the maximum of 40 draws. That is about the `0.5^(1/40) ~= 98.3`th percentile of a single backend, which here lies between the backend's p50 and p99 and much closer to the p99. Fixes: hedge requests to the slowest dependencies, cut the fan-out (batch, cache, precompute), or set per-call deadlines with graceful degradation.

**Q3.** Why must percentile metrics be aggregated with histograms instead of being averaged?

A percentile is a non-linear order statistic. The p99 of a union depends on the whole shape of each distribution, not on each host's p99 alone. With one healthy host (p99 = 20 ms) and one bad host (p99 = 210 ms), the merged p99 is about 205 ms, while the average of the two p99s is 115 ms. Histograms with fixed buckets, or mergeable sketches, can be summed across hosts and time windows, and the merged histogram then gives exact (bucketed) percentiles. A related trap is averaging per-minute p99s over an hour. Again, merge the histograms.

**Q4.** What is coordinated omission, and how do you avoid it in a load test?

In a closed-loop load test, each virtual user sends a request only after the previous one completes. When the server stalls for 1 s, a user scheduled to send every 10 ms sends nothing for 1 s and records **one** slow sample. Real open-loop traffic would have produced about 100 requests, each waiting on average 0.5 s. The recorded tail is too optimistic. Fixes: (a) use an open-loop, constant-arrival-rate generator (wrk2, or k6 with the constant-arrival-rate executor); (b) measure latency from the *intended* send time, not the actual send time; (c) correct the histogram afterwards (HdrHistogram has `recordValueWithExpectedInterval`).

---

# 2. Amdahl's and Gustafson's Laws

---

## 2.1 Speedup, Efficiency, Cost

| Quantity | Formula | Meaning |
|---|---|---|
| Speedup | `S(N) = T(1) / T(N)` | How many times faster with N workers |
| Parallel efficiency | `E(N) = S(N) / N` | Fraction of ideal; 1.0 = perfect linear scaling |
| Cost | `C(N) = N x T(N)` | Total resource-time (core-hours, GPU-hours) |
| Superlinear speedup | `S(N) > N` | Usually a cache effect: N workers have N times the aggregate cache, so the working set starts fitting |

`T(1)` should be the time of the **best serial implementation**, not the parallel code run on one thread. Otherwise parallel overheads inflate the reported speedup. Interviewers like to probe this point.

## 2.2 Amdahl's Law

**Setup (fixed problem size).** Normalize the serial runtime to 1. A fraction `p` of it is perfectly parallelizable, and `1 - p` is inherently serial.

**Derivation:**

```text
T(1) = (1 - p) + p                  = 1
T(N) = (1 - p) + p / N              (serial part unchanged; parallel part divided by N)

S(N) = T(1) / T(N) = 1 / ((1 - p) + p / N)

lim_{N -> inf} S(N) = 1 / (1 - p)   <- hard ceiling set by the serial fraction
```

**Worked numbers (speedup):**

| Parallel fraction p | N = 2 | N = 8 | N = 64 | N = 1024 | N -> inf |
|---|---|---|---|---|---|
| 0.50 | 1.33 | 1.78 | 1.97 | 2.00 | 2 |
| 0.90 | 1.82 | 4.71 | 8.77 | 9.91 | 10 |
| 0.95 | 1.90 | 5.93 | 15.42 | 19.64 | 20 |
| 0.99 | 1.98 | 7.48 | 39.26 | 91.18 | 100 |

With 5% serial code, 64 cores give only 15.4x (24% efficiency), and no number of cores gives more than 20x.

**General form: accelerating part of a program.** If a fraction `p` of the runtime is sped up by a factor `s` (by a GPU, a better algorithm, or SIMD), then:

```text
S = 1 / ((1 - p) + p / s)
```

**Worked GPU offload example.** An application takes 100 s, and 80 s of that is a kernel. Porting it to a GPU makes the kernel 40x faster, but each run adds 3 s of host-to-device and device-to-host copies:

```text
T_new = 20 (unchanged CPU part) + 80/40 (kernel) + 3 (transfers) = 25 s
S     = 100 / 25 = 4.0x
Ceiling with an infinitely fast GPU and free transfers: 1 / 0.2 = 5x
```

The lesson is to profile the **whole application** (the "speed-of-light" view) before optimizing a kernel. After the port, 80% of the time is outside the kernel, so the next 2x has to come from the CPU part and the transfers: overlap the copies with streams, keep data resident on the device, and port the remaining CPU code.

## 2.3 Gustafson's Law

Amdahl assumes a **fixed problem**. In practice, a bigger machine is used for a **bigger problem** (finer mesh, larger batch, bigger model) solved in about the same wall time. Gustafson (1988) measures the serial fraction **on the parallel machine**.

**Derivation.** On N processors the run takes time 1: a serial part `s` plus a parallel part `1 - s`. Running the same scaled problem on one processor would take `s + N(1 - s)`, because the parallel work is N times larger than one processor can do in that time.

```text
S_scaled(N) = (s + N (1 - s)) / 1 = N - s (N - 1)
```

**Worked number.** With `s = 0.05` and `N = 64`: `S = 64 - 0.05 x 63 = 60.85` (95% efficiency). Under Amdahl the same 5% serial fraction gives only 15.4x. **The two laws do not contradict each other.** They answer different questions:

| | Amdahl | Gustafson |
|---|---|---|
| Question | How much faster does *this* problem get? | How much *bigger* a problem can I solve in the same time? |
| Fixed quantity | Problem size | Time per worker (work per worker) |
| Serial fraction measured on | 1 processor | N processors |
| Scaling study | Strong scaling | Weak scaling |
| Pessimism | Saturates at 1/(1-p) | Grows linearly in N |
| Typical domain | Latency-critical job (inference request, interactive query) | Throughput science and training (bigger mesh or model) |

The hidden assumption in Gustafson's law is that the serial part does **not** grow with the problem. If setup, I/O, or a global reduction grows with N, scaled speedup also bends over.

## 2.4 Strong vs Weak Scaling

| | Strong scaling | Weak scaling |
|---|---|---|
| Setup | Fixed **total** problem; increase N | Fixed problem **per worker**; total grows with N |
| Ideal | `T(N) = T(1)/N` | `T(N) = T(1)` (flat line) |
| Efficiency | `E = T(1) / (N T(N))` | `E = T(1) / T(N)` |
| Governing law | Amdahl | Gustafson |
| What kills it | Serial fraction, communication that does not shrink, work per worker becoming too small (GPU under-occupancy, launch overhead) | Communication that grows with N (all-reduce log N or latency terms), global synchronization, I/O |

**Example strong-scaling study** (a stencil code on a fixed 1024^3 grid):

| Nodes | Time (s) | Speedup | Efficiency |
|---|---|---|---|
| 1 | 800 | 1.0 | 100% |
| 2 | 410 | 1.95 | 98% |
| 4 | 215 | 3.72 | 93% |
| 8 | 118 | 6.78 | 85% |
| 16 | 70 | 11.4 | 71% |
| 32 | 48 | 16.7 | 52% |

Why it bends: under 3D domain decomposition, each rank owns a subdomain of side `n / N^(1/3)`. Compute scales with **volume** `(n/N^(1/3))^3 = n^3/N`. Halo exchange scales with **surface** `6 (n/N^(1/3))^2`. The communication-to-computation ratio therefore grows like `N^(1/3) / n`. As N grows, each rank does less compute per byte communicated, and latency terms (per-message overhead) start to dominate. Under weak scaling, each rank's subdomain stays the same, so the surface-to-volume ratio stays constant. That is why weak scaling usually looks much better.

**A simple performance model with communication:**

```text
T(N) = T_serial + T_parallel / N + T_comm(N)
     T_comm(N) ~ alpha * log2(N) + beta * bytes        (tree or recursive-doubling collective)

dT/dN = -T_parallel / N^2 + alpha / (N ln 2) = 0   ->   N* = T_parallel * ln 2 / alpha
```

Past `N*`, adding workers makes the job **slower**. Interviewers like to ask: "Why did going from 32 to 64 GPUs make training slower?"

## 2.5 Overheads, Karp-Flatt, and Load Imbalance

**Karp-Flatt metric (experimentally determined serial fraction).** Given a measured speedup `S` on `N` processors:

```text
e = (1/S - 1/N) / (1 - 1/N)
```

Example: `S = 6` on `N = 8` gives `e = (0.1667 - 0.125) / 0.875 = 0.048`, so the code behaves like Amdahl's law with about 4.8% serial work. Compute `e` at several N:

- **e constant as N grows:** a true serial fraction. Parallelize that serial code.
- **e increasing with N:** overhead that grows with N (communication, synchronization, contention, load imbalance). Fix the parallel algorithm, not the serial code.

**Load imbalance.** With a barrier at the end of each phase, the phase takes as long as the slowest worker:

```text
T_phase   = max_i t_i
Efficiency <= mean_i(t_i) / max_i(t_i)
Imbalance  = max/mean - 1       (0% = perfect)
```

Example: 8 threads, 7 of them get 1 unit of work and 1 gets 2 units. Mean = 9/8 = 1.125, max = 2, so efficiency <= 56%. Fixes: dynamic scheduling or work stealing (`schedule(dynamic, chunk)` in OpenMP, TBB), over-decomposition (many more tasks than workers), cost-aware partitioning (balance by nnz, not rows, for sparse matrices), and sorting tasks longest first (LPT scheduling).

**GPU wave quantization (tail effect).** A kernel launches `G` workgroups, and the hardware can run `R` concurrently (CUs x workgroups per CU at the achieved occupancy). The kernel runs in `ceil(G / R)` "waves". On MI300X (304 CUs), suppose the occupancy allows 1 workgroup per CU, so `R = 304`:

```text
G = 304  -> 1 wave,  100% of slots used
G = 320  -> 2 waves; second wave has 16 workgroups -> efficiency = 320 / (2 x 304) = 52.6%
```

Fixes: pick tile sizes so that `G` is a multiple of `R`, use persistent kernels (launch exactly `R` workgroups that loop over the work), use split-K or stream-K for GEMM, or use smaller tiles to raise `G` (more waves make the last partial wave relatively cheaper).

```python
"""scaling.py -- Amdahl, Gustafson, Karp-Flatt calculators."""


def amdahl(p, n):
    return 1.0 / ((1.0 - p) + p / n)


def gustafson(s, n):
    return n - s * (n - 1)


def karp_flatt(speedup, n):
    return (1.0 / speedup - 1.0 / n) / (1.0 - 1.0 / n)


if __name__ == "__main__":
    for n in (8, 64, 1024):
        print(f"N={n:5d}  Amdahl(p=0.95)={amdahl(0.95, n):6.2f}  Gustafson(s=0.05)={gustafson(0.05, n):8.2f}")
    measured = {2: 1.95, 4: 3.72, 8: 6.78, 16: 11.4, 32: 16.7}   # strong-scaling table above
    for n, s in measured.items():
        print(f"N={n:2d}  S={s:5.2f}  E={s / n:5.1%}  Karp-Flatt e={karp_flatt(s, n):.4f}")
```

```text
N=    8  Amdahl(p=0.95)=  5.93  Gustafson(s=0.05)=    7.65
N=   64  Amdahl(p=0.95)= 15.42  Gustafson(s=0.05)=   60.85
N= 1024  Amdahl(p=0.95)= 19.64  Gustafson(s=0.05)=  972.85
N= 2  S= 1.95  E=97.5%  Karp-Flatt e=0.0256
N= 4  S= 3.72  E=93.0%  Karp-Flatt e=0.0251
N= 8  S= 6.78  E=84.8%  Karp-Flatt e=0.0257
N=16  S=11.40  E=71.2%  Karp-Flatt e=0.0269
N=32  S=16.70  E=52.2%  Karp-Flatt e=0.0296
```

Here `e` is about 2.5% and creeps up past N = 16. That pattern means a real serial fraction plus a communication overhead that starts to bite at larger N.

> **See also:** [Parallel GPU Programming -- Performance Optimization](../ml-gpu/Parallel_GPU_Programming.md#23-performance-optimization) (occupancy, divergence); [Parallel GPU Programming -- OpenMP Best Practices](../ml-gpu/Parallel_GPU_Programming.md#16-openmp-best-practices) (scheduling, affinity); [ML Systems Design](../ml-gpu/ML_Systems_Design.md) for scaling distributed training.

## 2.6 Interview Questions

**Q1.** 90% of a program is parallelizable. What is the maximum speedup on 16 cores, and on infinitely many?

`S(16) = 1 / (0.1 + 0.9/16) = 1 / 0.15625 = 6.4x`. As N goes to infinity, `S = 1/0.1 = 10x`. The follow-up: "Is it worth buying 64 cores?" `S(64) = 8.77x`, so 4x the hardware buys only 37% more speed (efficiency drops from 40% to 14%). Spend the effort on shrinking the serial 10% first: halving it to 5% lifts the 16-core speedup to 9.1x.

**Q2.** You measured a speedup of 9.5x on 8 cores. Explain.

That is superlinear speedup, and the common causes are: (1) **cache effects**: the per-core working set now fits in L2 or L3, so each core runs faster than the single core did on the full problem; (2) **NUMA**: the parallel version spreads its memory over both sockets' bandwidth, while the serial baseline was bound to one socket's memory; (3) **a bad baseline**, for example the parallel code run with 1 thread, or a serial baseline with a different algorithm or compiler flags; (4) **search problems**, where parallel exploration finds the answer earlier. Report it honestly and explain the cause. Use the best serial code as `T(1)`.

**Q3.** Strong vs weak scaling: which one do you show for an LLM training framework, and why?

Both, because they answer different stakeholder questions. **Weak scaling** (fixed per-GPU micro-batch, growing global batch) shows whether the framework adds GPUs without per-step overhead blowing up. That is the regime most pre-training runs use, and gradient all-reduce cost is the main thing to watch. **Strong scaling** (fixed global batch) matters when the global batch cannot grow for convergence reasons, or for time-to-solution and inference latency. Under strong scaling, per-GPU work shrinks until the GPUs are under-occupied and communication or launch overhead dominates. Report tokens/s/GPU and MFU alongside the speedup curves.

**Q4.** What is the Karp-Flatt metric used for?

It back-solves Amdahl's law from a measured speedup to get the "effective serial fraction" `e = (1/S - 1/N)/(1 - 1/N)`. The trend is diagnostic. A constant `e` points to inherently serial code. An `e` that grows with N points to parallel overhead (communication, synchronization, imbalance) that grows with N. The two cases need different fixes.

**Q5.** A GPU kernel launches 400 workgroups on a GPU that runs 304 concurrently. What efficiency loss do you expect, and what can you do?

There will be `ceil(400/304) = 2` waves, and the second wave holds only 96 workgroups. Assuming uniform workgroup runtimes, utilization = `400 / (2 x 304) = 66%`. Options: retile so the grid is a multiple of 304 (or so each wave is full); use a persistent-kernel or stream-K schedule; use smaller tiles so there are many waves and the partial last wave matters less; or raise occupancy so more workgroups fit per CU (raises `R`). With split-K GEMM, the K dimension is divided among more workgroups, at the cost of a final reduction.

---

# 3. Roofline Model

---

## 3.1 The Model

The **roofline model** (Williams, Waterman, Patterson, CACM 2009) bounds a kernel's attainable performance using two machine numbers and one kernel number:

```text
                 FLOPs performed
I  (arithmetic   ------------------------        [FLOP/byte]
   intensity) =  bytes moved to/from DRAM

P_attainable = min( P_peak ,  I x B_peak )        [FLOP/s]

Ridge point  I* = P_peak / B_peak                 [FLOP/byte]
```

```text
 log P (FLOP/s)
   ^
   |                       ______________________  P_peak (compute roof)
   |                     /
   |                   /   <- slope = B_peak (memory roof)
   |                 /
   |               /   .  kernel at (I, achieved P): the gap to the roof is headroom
   |             /
   |           /
   +----------|-----------------------------------> log I (FLOP/byte)
              I* (ridge point)
   memory-bound  <--|-->  compute-bound
```

- **Left of the ridge (`I < I*`), memory-bound.** The kernel cannot exceed `I x B_peak` no matter how fast the ALUs are. To go faster, move fewer bytes (fusion, caching or tiling, smaller data types, compression) or reach higher achieved bandwidth (coalescing, more bytes in flight).
- **Right of the ridge, compute-bound.** To go faster, use faster instructions (MFMA or tensor cores, FMA, SIMD), cut instruction overhead, or lower precision.
- **Far below both roofs** means neither bound applies. The problem is latency, occupancy, synchronization, launch overhead, divergence, or a bad instruction mix. Profile further.

A roofline plot is drawn on **log-log axes**. The memory roof is a straight 45-degree line on those axes, which is why it is called a roofline.

## 3.2 Arithmetic Intensity Worked Examples

The convention is that an FMA counts as **2 FLOPs**. Bytes means the minimum compulsory DRAM traffic unless stated otherwise.

**Vector add** `c[i] = a[i] + b[i]`, FP32:

```text
FLOPs per element : 1
Bytes per element : read a (4) + read b (4) + write c (4) = 12
I = 1/12 = 0.083 FLOP/B
CPU with write-allocate (the store first reads the line it will overwrite): 16 B -> I = 0.0625
```

**SAXPY** `y[i] = a * x[i] + y[i]`, FP32:

```text
FLOPs: 2 (one FMA).  Bytes: read x (4) + read y (4) + write y (4) = 12.   I = 2/12 = 0.167 FLOP/B
```

**GEMV** `y = A x` (n x n, FP32): `2n^2` FLOPs, and every element of A is read once (`4n^2` bytes; the x and y vectors are O(n)). `I ~= 0.5 FLOP/B`. **Batch-1 LLM decode is GEMV-like**, which is why it is memory-bound (see [ML Frameworks -- Prefill vs Decode](../ml-gpu/ML_AI_Frameworks.md#322-prefill-vs-decode-phases)).

**GEMM** `C = A B` (all n x n, FP32): `2n^3` FLOPs.

| Variant | DRAM traffic | Intensity | n = 4096 |
|---|---|---|---|
| Ideal (each matrix touched once) | `3 n^2 x 4 B` | `2n^3 / 12n^2 = n/6` | 683 FLOP/B |
| Naive, no cache reuse (every FMA loads A[i][k] and B[k][j]) | `2 n^3 x 4 B` | `2 / 8 = 0.25` | 0.25 FLOP/B |
| Tiled with T x T tiles in fast memory | `~ 2 n^3 / T x 4 B` | `T / 4` | T=32: 8; T=128: 32 |

**Derivation of the tiled traffic.** Use `T x T` tiles. For each of the `(n/T)^2` output tiles, stream `n/T` tile pairs (one from A, one from B), each pair being `2T^2` elements:

```text
elements loaded = (n/T)^2 x (n/T) x 2T^2 = 2 n^3 / T
bytes           = 8 n^3 / T            (FP32)
I               = 2 n^3 / (8 n^3 / T) = T / 4  FLOP/B
```

Intensity therefore grows **linearly with tile size**, and tile size is limited by fast-memory capacity `M`: three tiles must fit, so `3 T^2 x 4 B <= M` and `T <= sqrt(M/12)`. That bound gives T ~= 64 for 48 KiB of L1, T ~= 295 for 1 MiB of L2, and T ~= 73 for 64 KiB of GPU LDS. This is the I/O lower bound of Hong and Kung: any matmul schedule moves `Omega(n^3 / sqrt(M))` words. Real GEMMs stack tiles at **every** level (registers, LDS or L1, L2) so that each level's intensity exceeds that level's ridge point.

**3D 7-point stencil** (FP64), `out[i] = c0*u[i] + c1*(u[i±1] + u[i±nx] + u[i±nx*ny])`:

```text
FLOPs per point: 6 adds (sum of 6 neighbours, plus centre term) + 2 multiplies = 8
Bytes per point:
   ideal reuse (each u read once, out written once):       8 + 8      = 16  -> I = 0.50
   with CPU write-allocate on out:                          8 + 8 + 8  = 24  -> I = 0.33
   no reuse (all 7 neighbours from DRAM):                   7*8 + 8    = 64  -> I = 0.125
```

Stencils are bandwidth-bound on every modern machine. Spatial blocking gets close to the ideal 16 B per point. **Temporal blocking** (applying several time steps to a block while it is in cache) is the main way to push intensity past 0.5.

**Summary table (minimum compulsory traffic):**

| Kernel | Precision | FLOP/B | Bound on MI300X | Bound on a 96-core CPU |
|---|---|---|---|---|
| Vector add | FP32 | 0.083 | Memory | Memory |
| SAXPY / AXPY | FP32 | 0.167 | Memory | Memory |
| GEMV | FP32 | 0.5 | Memory | Memory |
| 7-point stencil | FP64 | 0.5 | Memory | Memory |
| Softmax / LayerNorm (elementwise + reduce) | FP16 | ~1-5 | Memory | Memory |
| GEMM, n = 4096 | FP32 | 683 | Compute | Compute |
| GEMM, n = 4096 | FP16 | 1365 | Compute | -- |

## 3.3 Ridge Points: MI300X and a CPU

**AMD Instinct MI300X** (CDNA 3, 304 CUs, 192 GB HBM3). Vendor-published theoretical dense peaks (AMD data sheet and product page): FP64 vector **81.7 TFLOP/s**, FP64 matrix 163.4, FP32 vector **163.4**, FP32 matrix 163.4, TF32 653.7, FP16/BF16 matrix **1307.4**, FP8 matrix 2614.9 (structured sparsity doubles the low-precision numbers). Peak HBM3 bandwidth is **5.3 TB/s**.

| MI300X roof | Peak (TFLOP/s) | Ridge point = peak / 5.3 TB/s |
|---|---|---|
| FP64 vector | 81.7 | **15.4 FLOP/B** |
| FP64 / FP32 matrix, FP32 vector | 163.4 | **30.8 FLOP/B** |
| FP16 / BF16 matrix (dense) | 1307.4 | **246.7 FLOP/B** |
| FP8 matrix (dense) | 2614.9 | **493.4 FLOP/B** |

**Worked CPU example** (estimated from first principles, the way you would do it at a whiteboard): a single-socket Zen 4-class server CPU with 96 cores at a 2.4 GHz all-core clock. Each core has 2 x 256-bit FMA pipes, so it does `2 pipes x 4 doubles x 2 FLOP = 16 FP64 FLOP/cycle`. Memory is 12 channels of DDR5-4800 at 8 bytes per transfer.

```text
P_peak(FP64) = 96 x 16 x 2.4e9      = 3.69 TFLOP/s     (FP32: 7.37 TFLOP/s)
B_peak       = 12 x 4.8e9 x 8 B      = 460.8 GB/s
Ridge (FP64) = 3.69e12 / 460.8e9     = 8.0 FLOP/B      (FP32: 16.0)
```

GPUs have a **higher ridge point** than CPUs, especially for matrix-core precisions. More kernels are therefore memory-bound on a GPU, and data reuse (tiling into LDS and registers, kernel fusion) matters even more there.

```python
"""roofline.py -- attainable performance = min(peak compute, arithmetic intensity x bandwidth)."""

# Vendor-published theoretical peaks (dense). The CPU row is a worked estimate:
# 96 cores x 16 FP64 FLOP/cycle (2 x 256-bit FMA pipes) x 2.4 GHz; 12 channels x DDR5-4800 x 8 B.
MACHINES = {
    "MI300X": {"bw": 5.3e12, "fp64": 81.7e12, "fp32": 163.4e12, "fp16": 1307.4e12},
    "CPU-96c": {"bw": 12 * 4800e6 * 8, "fp64": 96 * 16 * 2.4e9, "fp32": 96 * 32 * 2.4e9},
}

KERNELS = [  # (name, dtype, FLOPs, bytes) per output element (or per element-equivalent)
    ("vector add c=a+b", "fp32", 1, 12),
    ("SAXPY y=a*x+y", "fp32", 2, 12),
    ("GEMV y=Ax", "fp32", 2, 4),             # each A element read once, 1 FMA
    ("7-pt stencil (ideal reuse)", "fp64", 8, 16),
    ("GEMM n=4096 (ideal reuse)", "fp32", 2 * 4096, 12),   # 2n^3 / (3 n^2 * 4 B) = n/6
    ("GEMM n=4096 (ideal reuse)", "fp16", 2 * 4096, 6),    # n/3
]

if __name__ == "__main__":
    for m, spec in MACHINES.items():
        bw = spec["bw"]
        ridges = ", ".join(f"{d}={spec[d] / bw:.1f}" for d in ("fp64", "fp32", "fp16") if d in spec)
        print(f"{m}: BW={bw / 1e12:.3f} TB/s  ridge points (FLOP/B): {ridges}")
        for name, dt, flops, nbytes in KERNELS:
            if dt not in spec:
                continue
            ai, peak = flops / nbytes, spec[dt]
            att = min(peak, ai * bw)
            kind = "memory" if ai * bw < peak else "compute"
            print(f"  {name:27s} {dt}  AI={ai:7.3f}  -> {att / 1e12:8.3f} TFLOP/s ({att / peak:6.1%} of peak, {kind}-bound)")
```

```text
MI300X: BW=5.300 TB/s  ridge points (FLOP/B): fp64=15.4, fp32=30.8, fp16=246.7
  vector add c=a+b            fp32  AI=  0.083  ->    0.442 TFLOP/s (  0.3% of peak, memory-bound)
  SAXPY y=a*x+y               fp32  AI=  0.167  ->    0.883 TFLOP/s (  0.5% of peak, memory-bound)
  GEMV y=Ax                   fp32  AI=  0.500  ->    2.650 TFLOP/s (  1.6% of peak, memory-bound)
  7-pt stencil (ideal reuse)  fp64  AI=  0.500  ->    2.650 TFLOP/s (  3.2% of peak, memory-bound)
  GEMM n=4096 (ideal reuse)   fp32  AI=682.667  ->  163.400 TFLOP/s (100.0% of peak, compute-bound)
  GEMM n=4096 (ideal reuse)   fp16  AI=1365.333  -> 1307.400 TFLOP/s (100.0% of peak, compute-bound)
CPU-96c: BW=0.461 TB/s  ridge points (FLOP/B): fp64=8.0, fp32=16.0
  vector add c=a+b            fp32  AI=  0.083  ->    0.038 TFLOP/s (  0.5% of peak, memory-bound)
  SAXPY y=a*x+y               fp32  AI=  0.167  ->    0.077 TFLOP/s (  1.0% of peak, memory-bound)
  GEMV y=Ax                   fp32  AI=  0.500  ->    0.230 TFLOP/s (  3.1% of peak, memory-bound)
  7-pt stencil (ideal reuse)  fp64  AI=  0.500  ->    0.230 TFLOP/s (  6.2% of peak, memory-bound)
  GEMM n=4096 (ideal reuse)   fp32  AI=682.667  ->    7.373 TFLOP/s (100.0% of peak, compute-bound)
```

**Worked "time from first principles" example.** SAXPY on `n = 2^28` FP32 elements on MI300X moves `12 x 2^28 = 3.22 GB`, so it takes at least `3.22e9 / 5.3e12 = 608 us`. A kernel that measures 800 us reaches `3.22 GB / 800 us = 4.0 TB/s`, which is 76% of the theoretical peak and is probably near the **achievable** peak (see 3.5). Optimizing its arithmetic is pointless. The only real win is to **fuse** it with the producer or consumer kernel so the data is not round-tripped through HBM.

## 3.4 Hierarchical and Cache-Aware Roofline

The basic roofline counts only DRAM bytes. Real kernels move data through several levels (registers, L1/LDS, L2, Infinity Cache/LLC, HBM), and each level has its own bandwidth ceiling. There are two common extensions.

| | Hierarchical roofline (Yang, Williams et al., NERSC) | Cache-Aware Roofline Model (CARM; Ilic, Pratas, Sousa 2014) |
|---|---|---|
| Intensity | One AI **per memory level**: `FLOPs / bytes moved at that level` | One AI: `FLOPs / bytes requested by the core` (all loads and stores) |
| Ceilings | One bandwidth roof per level | One bandwidth roof per level, applied to the same AI |
| Plot | The same kernel appears as several dots (L1, L2, HBM) at one height | One dot, compared against several roofs |
| What it tells you | The **spread** between a kernel's L1, L2, and HBM dots measures cache reuse | Which level's bandwidth bounds the core-side traffic |

**Reading a hierarchical roofline** (this is what rocprof-compute's roofline view plots):

- **HBM dot far to the right of the L2 and L1 dots:** good reuse. Most bytes are served from caches and only a small fraction reaches HBM.
- **All dots stacked at nearly the same AI:** no cache reuse. Every byte the CUs request comes all the way from HBM. Look at the access pattern (coalescing, strides) or tile the data into LDS.
- **The binding level** is the dot closest to its own roof. A kernel can be L2-bandwidth-bound even when it looks fine against HBM.
- **The vertical gap** between the dot and the nearest roof is the headroom. A dot far below every roof is latency- or occupancy-bound, not throughput-bound.

**Workflow with rocprof-compute** (3.x). Flags change between releases, so confirm them with `rocprof-compute profile --help`:

```bash
# Collect roofline counters and run the empirical roofline microbenchmarks (writes roofline.csv)
rocprof-compute profile -n saxpy --roof-only -- ./saxpy

# Analyze: per-kernel AI and achieved FLOP/s vs empirical ceilings (HBM, L2, vL1D, LDS)
rocprof-compute analyze -p workloads/saxpy/MI300X_A1/
```

## 3.5 Measured vs Theoretical Ceilings

Vendor peaks are `units x clock x ops-per-cycle` products. **Empirical** ceilings, measured with microbenchmarks (STREAM-like copy or triad kernels for bandwidth, long FMA chains for compute; rocprof-compute's roofline benchmark does this), are always lower:

| Reason measured < theoretical | Affects |
|---|---|
| Clocks under load fall below the peak boost clock (power cap, thermals); spec FLOPs assume the peak engine clock (2,100 MHz on MI300X) | Compute roof |
| DRAM refresh, bank and row conflicts, read/write turnaround, protocol and ECC overhead | Bandwidth roof (achievable is often ~70-90% of spec) |
| The peak assumes FMA every cycle on every lane; adds and multiplies alone give half | Compute roof ("no-FMA ceiling" = peak/2) |
| Peak assumes full SIMD width / MFMA; scalar or VALU-only code has a much lower roof | Lower "ceilings" under the roof |
| Not enough bytes in flight (low occupancy, dependent loads) -- see Little's law | Achieved bandwidth well below the roof |
| Measurement window includes launch overhead or tail effect | Both |

**Pitfalls interviewers probe:**

1. **Counting FLOPs.** Count from the algorithm (`2n^3` for GEMM) or from hardware instruction counters, and say which. Counters count *executed* operations, including padding and redundant work, which can inflate "achieved" FLOP/s.
2. **Counting bytes.** Use measured DRAM traffic (counters), not the algorithmic minimum, when diagnosing. The gap between the two is exactly your cache inefficiency.
3. **The roofline ignores latency.** A kernel with tiny `n` never reaches either roof. Launch latency and the tail effect dominate.
4. **Mixed precision.** Each data type and instruction class (FP64 VALU, FP32 VALU, FP16 MFMA) has its own compute roof. Plot against the one the kernel actually uses.
5. **Integer and address arithmetic** does not count as FLOPs, but it consumes issue slots. A kernel can be "instruction-bound" well below the FLOP roof.

> **See also:** [AMD GPU Architecture and Profiling](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md) for counters and the top-down rocprof-compute workflow; [GPU Kernel Case Studies](../ml-gpu/GPU_Kernel_Case_Studies.md) for worked profile -> fix -> re-profile loops; [Parallel GPU Programming -- Profiling Tools](../ml-gpu/Parallel_GPU_Programming.md#237-profiling-tools); [Project Deep Dive: rocprof-compute](../career/Project_Deep_Dive_rocprof-compute.md).

## 3.6 Interview Questions

**Q1.** Define arithmetic intensity and the ridge point. Compute the ridge point of MI300X for FP32 vector and FP16 matrix work.

Arithmetic intensity is FLOPs performed per byte moved to or from (by default) DRAM. The ridge point is the AI at which the memory roof meets the compute roof: `I* = P_peak / B_peak`. For MI300X: FP32 vector `163.4 TFLOP/s / 5.3 TB/s = 30.8 FLOP/B`; FP16 matrix `1307.4 / 5.3 = 247 FLOP/B`. A kernel needs more than 247 FLOPs per HBM byte to be compute-bound on the matrix cores. Only large GEMMs, convolutions, and well-fused attention get there. Almost every elementwise, normalization, or reduction kernel is memory-bound.

**Q2.** Your SAXPY kernel achieves 0.6 TFLOP/s on MI300X, which is 0.4% of FP32 peak. Is it a bad kernel?

No, not by that measure. SAXPY's AI is `2/12 = 0.167 FLOP/B`, so its roof is `0.167 x 5.3 TB/s = 0.88 TFLOP/s`. At 0.6 TFLOP/s it moves `0.6e12 x 6 B/FLOP = 3.6 TB/s`, which is 68% of peak bandwidth. The right metric for a memory-bound kernel is **achieved bandwidth as a percentage of achievable bandwidth**, not percentage of peak FLOPs. Next steps: compare against an empirical copy-kernel bandwidth; check coalescing, vector width (`float4` loads), and grid size; but the big win is fusing SAXPY with its neighbours.

**Q3.** How does tiling change the arithmetic intensity of matrix multiply? Derive it.

Without reuse, each FMA loads one A element and one B element: 2 FLOPs per 8 bytes = 0.25 FLOP/B (FP32). With `T x T` tiles, each output tile loops over `n/T` tile pairs of `2T^2` elements, so total loads are `(n/T)^2 x (n/T) x 2T^2 = 2n^3/T` elements, or `8n^3/T` bytes. Since FLOPs = `2n^3`, AI = `T/4`. Tile size is limited by fast-memory capacity (`3T^2 x 4 B <= M`), which gives the Hong-Kung bound `Q = Omega(n^3/sqrt(M))`. Production GEMMs tile at the register, LDS/L1, and L2 levels, each sized for that level's capacity and ridge point.

**Q4.** What is the difference between hierarchical roofline and the cache-aware roofline?

The hierarchical roofline computes a separate AI per memory level (FLOPs divided by bytes moved at L1, L2, and HBM), so each kernel appears as multiple points. The horizontal spread between them measures cache reuse, and you identify the level whose point is closest to its own ceiling. CARM uses a single AI based on all core-issued loads and stores, and draws one roof per level. It asks which level's bandwidth can sustain the core's request stream. rocprof-compute and NERSC-style analyses use the hierarchical form, with empirically measured ceilings.

**Q5.** Why is measured peak bandwidth lower than the data sheet, and which one should you plot?

DRAM refresh, bank and row conflicts, read/write turnaround, and controller and protocol overheads mean that even a perfect streaming kernel achieves less than the pin bandwidth. Under load, clocks also fall below the boost clock on which the FLOP peaks are based. Plot **both**. Use empirical ceilings (from microbenchmarks on the same machine and driver) to judge how close a kernel is to the achievable limit, and theoretical ceilings to judge hardware and design headroom. Say clearly which one you are using.

**Q6.** Batch-1 decode of a 7B-parameter FP16 model on one MI300X: what is the best-case tokens/s?

Each token must read all the weights: `7e9 x 2 B = 14 GB`. The AI is about 1 FLOP/B (GEMV-like: 2 FLOPs per 2-byte weight), so the step is memory-bound. Time per token >= `14 GB / 5.3 TB/s = 2.64 ms`, so at most about **379 tokens/s**, ignoring KV-cache reads (which make it worse) and assuming 100% of peak bandwidth (realistically 70-85%). Ways to improve throughput: batch more sequences (the weights are read once per step for B tokens, which raises AI by about B), quantize the weights (INT8 or FP8 halves the bytes), or use speculative decoding.

---

# 4. Little's Law and Queueing

---

## 4.1 Little's Law

For any **stable** system (arrivals equal departures over the long run), regardless of arrival distribution, service distribution, or scheduling order:

```text
L = lambda x W

L      = average number of items in the system (in flight, in queue + in service)
lambda = average throughput (arrival rate = completion rate)
W      = average time an item spends in the system (latency)
```

**Why it holds (proof sketch).** Plot "number of items in the system" over a long window `[0, T]`. The area under that curve equals the sum of all items' time in the system, which is `(number of items) x W = lambda T x W`. Dividing the area by `T` gives the time-average `L`. So `L = lambda W`. Nothing about distributions enters the argument, which is why the law is so robust.

Rearranged, it gives the three most useful performance equations:

| Form | Use it to... |
|---|---|
| `throughput = concurrency / latency` | Find the max throughput a fixed pool of threads, connections, or outstanding misses can deliver |
| `concurrency = throughput x latency` | Size thread pools, connection pools, queue depths, **bytes in flight** |
| `latency = concurrency / throughput` | Infer queueing delay from a measured queue length |

## 4.2 Memory-Level Parallelism: Bytes in Flight

For a memory system, `L` is **bytes (or requests) in flight**, `lambda` is bandwidth, and `W` is memory latency:

```text
bytes_in_flight = bandwidth x latency
```

**Worked: MI300X HBM.** Assume a loaded HBM latency of about 600 ns as seen from a wave (an assumption for arithmetic; real values depend on load and path):

```text
5.3e12 B/s x 600e-9 s = 3.18 MB must be in flight to saturate HBM
   / 304 CUs                      = ~10.5 KB in flight per CU
   / 256 B per wave64 load (4 B/lane) = ~41 outstanding wave-level loads per CU
   with float4 loads (1 KiB/wave)  = ~10 per CU
```

That is why **occupancy** (more waves resident per CU) and **ILP** (several independent loads per thread before the first use, unrolling, wider `float4`/`dwordx4` loads) matter for memory-bound GPU kernels. With 8 waves per CU each issuing one 256-byte load and then waiting, a CU has only 2 KB in flight, about 20% of what is needed. The kernel is **latency-bound** and sits far below the bandwidth roof.

**Worked: one CPU core vs a socket.** At ~100 ns DRAM latency:

```text
one core at 20 GB/s  needs  20e9 x 100e-9 =  2 KB  = ~31 cache lines in flight
whole socket 460 GB/s needs 460e9 x 100e-9 = 46 KB = ~720 cache lines in flight
```

A core has a limited number of outstanding L1 misses (fill buffers or MSHRs, on the order of 16-24 depending on the microarchitecture). The L2 hardware prefetchers add deeper queues for **sequential** streams. That is why (a) a single core cannot saturate socket bandwidth, so you need many cores streaming (compare the NUMA triad in [7.2](#72-first-touch-placement), which used 192 threads), and (b) random access gets less bandwidth than streaming, because the prefetchers cannot help.

**Little's law applied to our own measurement.** The gather loop in [5.7](#57-prefetching) completed one random DRAM load every `56.6 ms / 16.8M = 3.4 ns`, while the latency ladder in [5.1](#51-the-latency-ladder-measured) measured about 120-130 ns per dependent DRAM load. So about `125 / 3.4 = ~37` misses were in flight at once. The out-of-order core found that memory-level parallelism automatically, because the loads were independent. A **pointer chase** has an MLP of exactly 1, which is why it runs at full latency.

## 4.3 Sizing a Server with Little's Law

**Worked example.** A service must sustain `lambda = 2,000 req/s` at an average latency of `W = 50 ms`:

```text
L = 2000 x 0.050 = 100 requests in flight on average
```

- A thread-per-request server therefore needs **at least 100 worker threads** at the average. Size for the peak rate and leave headroom (Section 4.4), so 150-200.
- If each request holds a DB connection for 10 ms: `2000 x 0.010 = 20` connections busy on average. Size the pool at about 30 to keep connection utilization near 65-70%.
- Conversely, a pool of 50 threads with 50 ms latency can never exceed `50 / 0.05 = 1,000 req/s`. **When latency goes up (a slow dependency), a fixed-size pool's throughput goes down.** That feedback loop is how cascading failures start, so add timeouts, bulkheads, and load shedding.

The same arithmetic applies to GPUs: an inference server with a 40 ms step and a batch of 32 serves at most `32 / 0.040 = 800` sequences-steps/s per replica.

## 4.4 Utilization vs Latency: M/M/1 and Beyond

**M/M/1 queue:** Poisson arrivals at rate `lambda`, exponential service with mean `S = 1/mu`, one FIFO server. Utilization is `rho = lambda / mu = lambda S < 1`.

```text
W  (mean response time) = S / (1 - rho) = 1 / (mu - lambda)
Wq (mean wait in queue) = rho S / (1 - rho)
L  (mean number in system) = rho / (1 - rho)          (Little: L = lambda W)
Response time is exponential with rate (mu - lambda)  ->  p99 = W x ln(100) = 4.6 W
```

| Utilization rho | Mean latency W (multiples of S) | p99 (multiples of S) |
|---|---|---|
| 0.50 | 2 | 9.2 |
| 0.80 | 5 | 23 |
| 0.90 | 10 | 46 |
| 0.95 | 20 | 92 |
| 0.99 | 100 | 461 |

```text
 W/S
 100 |                                                   *
     |                                                   |
  20 |                                              *    |
  10 |                                          *
   5 |                                  *
   2 |               *
   1 +----+----+----+----+----+----+----+----+----+----+--> rho
     0   0.1            0.5            0.8  0.9 0.95  0.99
```

**The knee.** Latency doubles from 50% to 75% utilization and doubles again from 75% to 87.5%. Near saturation, **a 5% traffic increase can double latency**. Latency-sensitive services are therefore provisioned to run around 50-70% utilization at peak, and batch systems run hot.

**Simulation that checks the formula:**

```python
"""queueing.py -- M/M/1 latency vs utilization (formula + simulation) and fan-out tail amplification."""
import math
import random


def mm1_sim(lam, mu, n=1_000_000, seed=1):
    """Single FIFO server, Poisson arrivals (rate lam), exponential service (rate mu)."""
    rng = random.Random(seed)
    t_arrive = t_free = 0.0
    lat = []
    for _ in range(n):
        t_arrive += rng.expovariate(lam)
        start = max(t_arrive, t_free)            # wait if the server is busy
        t_free = start + rng.expovariate(mu)
        lat.append(t_free - t_arrive)            # response time = queueing + service
    lat.sort()
    return sum(lat) / n, lat[int(0.99 * n)]


if __name__ == "__main__":
    S = 1.0                                       # mean service time = 1 ms -> mu = 1/ms
    print(" rho   W=S/(1-rho)  sim mean   p99 formula  sim p99")
    for rho in (0.5, 0.8, 0.9, 0.95):
        w = S / (1 - rho)
        mean, p99 = mm1_sim(lam=rho / S, mu=1 / S)
        print(f"{rho:4.2f} {w:10.1f} {mean:10.2f} {w * math.log(100):12.1f} {p99:8.1f}")

    # Fan-out: a request waits for ALL n leaves; each leaf is slow with probability p.
    for n in (1, 10, 100, 1000):
        print(f"fan-out {n:4d}: P(request hits >=1 leaf p99) = {1 - 0.99 ** n:7.2%}")
```

```text
 rho   W=S/(1-rho)  sim mean   p99 formula  sim p99
0.50        2.0       2.00          9.2      9.2
0.80        5.0       4.97         23.0     22.9
0.90       10.0       9.91         46.1     45.2
0.95       20.0      20.48         92.1    104.2
fan-out    1: P(request hits >=1 leaf p99) =   1.00%
fan-out   10: P(request hits >=1 leaf p99) =   9.56%
fan-out  100: P(request hits >=1 leaf p99) =  63.40%
fan-out 1000: P(request hits >=1 leaf p99) = 100.00%
```

The simulation still disagrees with the formula at `rho = 0.95` after a million requests. That is itself a lesson: near saturation, the latency **variance** is so large that short benchmarks of a busy system are unreliable.

**Variability matters too: Kingman's approximation for G/G/1:**

```text
Wq ~= ( rho / (1 - rho) ) x ( (ca^2 + cs^2) / 2 ) x S
ca, cs = coefficients of variation (stddev/mean) of inter-arrival and service times
```

M/M/1 has `ca = cs = 1`. Deterministic service (`cs = 0`) halves the queueing delay. Bursty arrivals or heavy-tailed service times (`cs >> 1`) multiply it. **Reducing variance is as effective as adding capacity.** Separating long requests into their own queue, capping batch sizes, and chunked prefill in LLM serving all reduce variance.

**Pooling beats partitioning (M/M/c).** Two servers each fed by its own queue at `rho = 0.8` give `W = 5S`. One shared queue feeding both servers (M/M/2, same total load) gives `W ~= 2.8S` (from the Erlang C formula: `P(wait) = 0.711`, `Wq = 0.711 / (2 mu - lambda) = 1.78 S`). This is why a shared work queue beats per-thread queues (absent locality concerns), and why work stealing helps.

> **See also:** [High-Level Design -- Estimate the Workload](./High_Level_Design.md#3-estimate-the-workload); [CS Fundamentals -- Back-of-the-Envelope Estimation](./CS_Fundamentals.md#59-back-of-the-envelope-estimation); [ML Systems Design](../ml-gpu/ML_Systems_Design.md) for batching against latency SLOs.

## 4.5 Interview Questions

**Q1.** State Little's law and use it to compute how many bytes must be in flight to saturate MI300X HBM.

`L = lambda W`. The average number in the system equals throughput times time in the system, for any stable system. For memory: bytes in flight = bandwidth x latency. With 5.3 TB/s and an assumed ~600 ns loaded latency, about 3.2 MB must be in flight, roughly 10 KB per CU across 304 CUs, or about forty 256-byte wave loads per CU. A kernel with low occupancy and one dependent load per thread cannot reach that, so it is latency-bound. Fixes: raise occupancy (fewer VGPRs or less LDS per workgroup), issue several independent loads per thread (unroll), and use 16-byte vector loads.

**Q2.** Why do SREs keep latency-sensitive services at 50-70% CPU utilization instead of 95%?

Queueing delay grows like `rho / (1 - rho)`. At 50% the mean response time is 2x service time; at 90% it is 10x and the p99 is about 46x (M/M/1). Near saturation, small load increases (a 10% traffic spike, one replica failing) produce huge latency increases, and the variance makes behaviour unpredictable. Headroom absorbs bursts, failover, and GC. Batch systems with no latency SLO can run near 100%.

**Q3.** A service handles 500 req/s at 200 ms average latency. How many concurrent requests are there? The downstream DB gets slow and latency rises to 1 s. What happens with a 128-thread pool?

`L = 500 x 0.2 = 100` concurrent requests, which fits in 128 threads. At 1 s latency, sustaining 500 req/s needs 500 concurrent requests, but the pool caps concurrency at 128, so throughput falls to `128 / 1 s = 128 req/s`. The other ~372 req/s queue up without bound (latency grows until timeouts fire) or get rejected. Mitigations: timeouts below the client's timeout, a circuit breaker on the DB, load shedding (reject early with 503), separate bulkhead pools per dependency, and asynchronous I/O so threads are not tied up while waiting.

**Q4.** One shared queue with 4 workers, or 4 queues with 1 worker each? Why?

With identical load, the single shared queue (M/M/4) has much lower mean and tail latency. A worker never sits idle while another worker's queue has a backlog. Separate queues are justified when you need locality (cache-hot per-core state, NUMA), when the shared queue's lock or cache line becomes a contention point, or when you need isolation (priority classes). Work stealing gets most of both: local queues plus balancing.

**Q5.** Throughput is flat at 1.2M ops/s whether you run 8 or 16 threads. What does Little's law suggest?

If the threads were latency-bound, doubling concurrency would double throughput. Flat throughput means a shared resource is saturated, so extra concurrency only adds queueing: per-op latency doubles from `8/1.2M = 6.7 us` to `16/1.2M = 13.3 us`. Find the bottleneck: a lock (check contention profiles), memory bandwidth (compare against STREAM), a single hot cache line, a NIC or disk, or a serial section (Amdahl). `perf`, lock profilers, and the USE method (Utilization, Saturation, Errors per resource) locate it.

---

# 5. Memory Hierarchy Programming

---

Programs are fast when they **use every byte of every cache line they fetch** (spatial locality), **reuse data while it is still cached** (temporal locality), and **keep enough independent misses in flight** (MLP). The examples below make each principle concrete. Cache theory (associativity, the 3 C's, MESI) is covered in [CS Fundamentals -- Cache](./CS_Fundamentals.md#75-cache).

## 5.1 The Latency Ladder (Measured)

A **pointer chase** through a random cyclic permutation measures load-to-use latency: each load's address depends on the previous load, so MLP = 1 and prefetchers cannot predict the next address. Growing the working set walks down the hierarchy.

```cpp
// latency_ladder.cpp -- dependent-load latency vs working-set size (cache + TLB staircase)
// g++ -std=c++20 -O2 latency_ladder.cpp -o latency_ladder && ./latency_ladder [--huge]
#include <sys/mman.h>
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <numeric>
#include <random>
#include <vector>

int main(int argc, char** argv) {
    const bool huge = argc > 1 && std::strcmp(argv[1], "--huge") == 0;
    constexpr std::size_t kLine = 64, kMaxBytes = std::size_t{1} << 30;    // up to 1 GiB
    constexpr std::size_t kAlign = std::size_t{2} << 20;                   // 2 MiB
    auto* buf = static_cast<char*>(std::aligned_alloc(kAlign, kMaxBytes));
    if (!buf) return 1;
    if (huge) madvise(buf, kMaxBytes, MADV_HUGEPAGE);                      // ask for THP
    std::mt19937_64 rng(42);

    for (std::size_t bytes = 16 << 10; bytes <= kMaxBytes; bytes *= 4) {
        // Build a random cyclic permutation of cache lines: each line stores the next pointer.
        const std::size_t lines = bytes / kLine;
        std::vector<std::size_t> order(lines);
        std::iota(order.begin(), order.end(), 0);
        std::shuffle(order.begin() + 1, order.end(), rng);
        for (std::size_t i = 0; i < lines; ++i) {
            char* cur = buf + order[i] * kLine;
            char* nxt = buf + order[(i + 1) % lines] * kLine;
            std::memcpy(cur, &nxt, sizeof nxt);
        }
        const std::size_t steps = 20'000'000;
        char* p = buf;
        auto t0 = std::chrono::steady_clock::now();
        for (std::size_t i = 0; i < steps; ++i) p = *reinterpret_cast<char**>(p);  // serial chain
        double ns = std::chrono::duration<double, std::nano>(std::chrono::steady_clock::now() - t0).count();
        std::printf("%10zu KiB  %6.1f ns/load  (%p)\n", bytes >> 10, ns / steps, static_cast<void*>(p));
    }
    std::free(buf);
}
```

Measured (Zen 5 core, `taskset -c 5`), with 4 KiB pages vs transparent huge pages (`--huge`):

| Working set | 4 KiB pages (ns/load) | 2 MiB THP (ns/load) | Level |
|---|---|---|---|
| 16 KiB | 0.9 | 0.9 | L1 |
| 64-256 KiB | 3.1 | 3.1 | L2 |
| 1 MiB | 5.3 | 3.2 | L2 (+ TLB misses with 4 KiB pages) |
| 4-16 MiB | 10.9-12.0 | 9.6-10.6 | L3 |
| 64 MiB | 89.6 | 82.5 | DRAM (+ L3 partially) |
| 1 GiB | 130.5 | 116.0 | DRAM + page walks |

Printing `p` keeps the compiler from deleting the chase loop, which has no other side effect (see [8.3](#83-a-minimal-honest-harness)).

## 5.2 Address Breakdown: Tag, Set, Offset

Hardware-company interviews often ask you to split an address. **Example cache:** 32 KiB, 8-way set-associative, 64-byte lines.

```text
lines   = 32 KiB / 64 B          = 512
sets    = 512 / 8 ways           = 64
offset bits = log2(64 B)         = 6      (bits  5..0)
index bits  = log2(64 sets)      = 6      (bits 11..6)
tag bits    = remaining high bits of the PHYSICAL address (e.g. bits 51..12 for a 52-bit PA;
              for VIPT the index comes from VA bits 11..6, which equal the PA bits
              because they lie inside the 4 KiB page offset)

address 0x7ffd1234 (treated as the physical address, so tag = addr >> 12 is the PA tag):
   offset = 0x7ffd1234 & 0x3f          = 0x34 = 52
   set    = (0x7ffd1234 >> 6) & 0x3f   = 8
   tag    = 0x7ffd1234 >> 12           = 0x7ffd1
```

Note that `offset + index = 12 bits = 4 KiB = page size`. That is deliberate: the L1 can be **virtually indexed, physically tagged (VIPT)**, so the set lookup proceeds in parallel with the TLB lookup. It is also why L1 size per way is commonly 4 KiB (32 KiB / 8 ways, or 48 KiB / 12 ways).

**Power-of-two stride conflict misses.** Addresses that differ by a multiple of `sets x line = 4 KiB` map to the **same set**. Walking down a column of a row-major `float[4096][4096]` uses a stride of 16 KiB, so every access lands in one set and only **8 lines** (the associativity) can be cached at once, however large the cache is. The fix is to **pad the leading dimension** (for example, allocate rows of `4096 + 16` floats) so successive rows map to different sets. BLAS APIs expose `lda` for exactly this reason. FFT and stencil codes pad too.

## 5.3 Row-Major vs Column-Major Traversal

C and C++ arrays are **row-major**: `m[i][j]` and `m[i][j+1]` are adjacent. Fortran, MATLAB, and Julia are column-major. NumPy supports both (`order='C'` / `'F'`).

```cpp
// traversal.cpp -- row-major vs column-major traversal of the same matrix
// g++ -std=c++20 -O2 traversal.cpp -o traversal && ./traversal
#include <chrono>
#include <cstdio>
#include <vector>

int main() {
    constexpr std::size_t N = 4096;                 // 4096 x 4096 floats = 64 MiB
    std::vector<float> m(N * N, 1.0f);              // row-major: m[i*N + j]

    auto time_it = [](auto&& fn) {
        auto t0 = std::chrono::steady_clock::now();
        double s = fn();
        auto t1 = std::chrono::steady_clock::now();
        std::printf("  sum=%.0f  %.1f ms\n", s,
                    std::chrono::duration<double, std::milli>(t1 - t0).count());
    };

    std::puts("row-major order (stride 4 B, every byte of each 64 B line used):");
    time_it([&] {
        double s = 0;
        for (std::size_t i = 0; i < N; ++i)
            for (std::size_t j = 0; j < N; ++j) s += m[i * N + j];
        return s;
    });

    std::puts("column-major order (stride 16 KiB, one float used per line fetched):");
    time_it([&] {
        double s = 0;
        for (std::size_t j = 0; j < N; ++j)
            for (std::size_t i = 0; i < N; ++i) s += m[i * N + j];
        return s;
    });
}
```

```text
row-major order (stride 4 B, every byte of each 64 B line used):
  sum=16777216  8.1 ms
column-major order (stride 16 KiB, one float used per line fetched):
  sum=16777216  90.0 ms
```

**About 11x** for the same arithmetic. In the column walk, each 64-byte line yields one useful float (1/16 utilization). The 16 KiB stride also hits the 4 KiB-aliasing set conflict from 5.2, and every access touches a different 4 KiB page, so TLB misses pile up too. The fix is to **interchange the loops** (the compiler rarely does it for you when the loop body has a floating-point reduction) or to transpose the data once.

## 5.4 Loop Interchange and Tiling for Matmul

```cpp
// matmul.cpp -- naive (ijk), loop-interchanged (ikj), and tiled matmul
// g++ -std=c++20 -O2 matmul.cpp -o matmul && ./matmul 1024
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <vector>

using Mat = std::vector<double>;   // row-major, n x n

void matmul_ijk(const Mat& A, const Mat& B, Mat& C, int n) {
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j) {
            double acc = 0;
            for (int k = 0; k < n; ++k)
                acc += A[i * n + k] * B[k * n + j];      // B walked down a column: stride n
            C[i * n + j] = acc;
        }
}

void matmul_ikj(const Mat& A, const Mat& B, Mat& C, int n) {
    std::fill(C.begin(), C.end(), 0.0);
    for (int i = 0; i < n; ++i)
        for (int k = 0; k < n; ++k) {
            const double a = A[i * n + k];
            for (int j = 0; j < n; ++j)
                C[i * n + j] += a * B[k * n + j];        // unit stride on B and C: vectorizes
        }
}

void matmul_tiled(const Mat& A, const Mat& B, Mat& C, int n, int T) {
    std::fill(C.begin(), C.end(), 0.0);
    for (int ii = 0; ii < n; ii += T)
        for (int kk = 0; kk < n; kk += T)
            for (int jj = 0; jj < n; jj += T) {
                // T x T blocks of A, B, C (3 * T*T*8 bytes) stay in L1/L2 while reused T times
                const int ie = std::min(ii + T, n), ke = std::min(kk + T, n), je = std::min(jj + T, n);
                for (int i = ii; i < ie; ++i)
                    for (int k = kk; k < ke; ++k) {
                        const double a = A[i * n + k];
                        const double* b = &B[k * n];
                        double* c = &C[i * n];
                        for (int j = jj; j < je; ++j) c[j] += a * b[j];
                    }
            }
}

int main(int argc, char** argv) {
    const int n = argc > 1 ? std::atoi(argv[1]) : 1024;
    Mat A(n * n), B(n * n), C(n * n), ref(n * n);
    for (int i = 0; i < n * n; ++i) { A[i] = (i % 7) * 0.5; B[i] = (i % 5) * 0.25; }

    auto run = [&](const char* name, auto&& fn) {
        auto t0 = std::chrono::steady_clock::now();
        fn();
        double s = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
        std::printf("%-14s %8.1f ms  %6.2f GFLOP/s\n", name, s * 1e3, 2.0 * n * n * n / s / 1e9);
    };
    run("ijk (naive)", [&] { matmul_ijk(A, B, ref, n); });   // slow: ~30 s at n=2048
    run("ikj", [&] { matmul_ikj(A, B, C, n); });
    run("tiled T=64", [&] { matmul_tiled(A, B, C, n, 64); });

    double maxdiff = 0;
    for (int i = 0; i < n * n; ++i) maxdiff = std::max(maxdiff, std::abs(C[i] - ref[i]));
    std::printf("max |tiled - naive| = %g\n", maxdiff);
}
```

Measured, single core, FP64 (`n = 3000` measured with the same loops, without the naive version):

| Variant | n = 1024 (8 MiB per matrix) | n = 3000 (69 MiB per matrix) |
|---|---|---|
| ijk (naive) | 0.7 GFLOP/s | (too slow to bother) |
| ikj (loop interchange) | 8.6 GFLOP/s | 6.2 GFLOP/s |
| tiled, T = 64 | 6.1 GFLOP/s | 8.4 GFLOP/s |

How to read the results (and what to say in an interview):

1. **Loop interchange is the biggest single win (12x).** In `ijk`, the inner loop walks B down a column with a stride of `n x 8 B = 8 KiB`, which is a power of two and so causes conflict misses (5.2). It also cannot vectorize. In `ikj`, the innermost loop streams B and C with unit stride, broadcasts `a`, and auto-vectorizes.
2. **Tiling helps only once the reused data no longer fits in cache.** At `n = 1024`, all of B (8 MiB) fits in this CPU's L3, so `ikj` already streams from L3 with good prefetching. Tiling there adds loop overhead and shorter inner loops. At `n = 3000`, B (69 MiB) exceeds L3, `ikj` re-reads it from DRAM for every row `i`, and tiling wins by 35%.
3. **Neither is close to peak.** A single Zen 5 core can do on the order of 100 FP64 GFLOP/s. Optimized BLAS (OpenBLAS, BLIS, MKL, AOCL) reach a large fraction of that by adding **register blocking** (an `mr x nr` micro-kernel of accumulators held in SIMD registers), **packing** tiles into contiguous buffers (no TLB or conflict misses), multi-level tiling (L1/L2/L3), and FMA intrinsics. **In production, call BLAS.** Hand-written matmul is an interview vehicle for explaining locality.
4. **Always validate.** `max |tiled - naive| = 0` here because the inputs are small multiples of 0.25 and 0.5, which are exactly representable. With general inputs, reordering the sums changes the last bits (Section 9), so compare with a tolerance.

## 5.5 AoS vs SoA

```cpp
// aos_soa.cpp -- Array-of-Structs vs Struct-of-Arrays when a loop touches one field
// g++ -std=c++20 -O2 aos_soa.cpp -o aos_soa && ./aos_soa
#include <chrono>
#include <cstdio>
#include <vector>

struct ParticleAoS {            // 32 bytes: a 64 B line holds 2 particles
    float x, y, z;
    float vx, vy, vz;
    float mass;
    int   id;
};

struct ParticlesSoA {           // each field contiguous: a 64 B line holds 16 x-values
    std::vector<float> x, y, z, vx, vy, vz, mass;
    std::vector<int> id;
    explicit ParticlesSoA(std::size_t n)
        : x(n), y(n), z(n), vx(n), vy(n), vz(n), mass(n), id(n) {}
};

int main() {
    constexpr std::size_t N = 1 << 24;           // 16M particles (512 MiB as AoS)
    std::vector<ParticleAoS> aos(N, ParticleAoS{1, 2, 3, 0.5f, 0, 0, 1, 0});
    ParticlesSoA soa(N);
    for (std::size_t i = 0; i < N; ++i) { soa.x[i] = 1; soa.vx[i] = 0.5f; }

    constexpr float dt = 0.01f;
    auto t0 = std::chrono::steady_clock::now();
    for (auto& p : aos) p.x += p.vx * dt;        // uses 8 of every 32 bytes loaded
    auto t1 = std::chrono::steady_clock::now();
    for (std::size_t i = 0; i < N; ++i) soa.x[i] += soa.vx[i] * dt;   // uses every byte; vectorizes
    auto t2 = std::chrono::steady_clock::now();

    using ms = std::chrono::duration<double, std::milli>;
    std::printf("AoS update x: %.1f ms   (moves %zu MiB)\n", ms(t1 - t0).count(), 2 * N * sizeof(ParticleAoS) >> 20);
    std::printf("SoA update x: %.1f ms   (moves %zu MiB)\n", ms(t2 - t1).count(), 3 * N * sizeof(float) >> 20);
    std::printf("check: %.3f %.3f\n", aos[N / 2].x, soa.x[N / 2]);
}
```

```text
AoS update x: 16.8 ms   (moves 1024 MiB)
SoA update x: 3.8 ms   (moves 192 MiB)
check: 1.005 1.005
```

The SoA version moves 5.3x fewer bytes and runs 4.4x faster, as the roofline predicts for a bandwidth-bound loop. The AoS loop has to read and write back whole 64-byte lines, even though it only needs 8 bytes per particle.

| Layout | Best when | Drawbacks |
|---|---|---|
| **AoS** | Code touches most fields of one object together (OOP style, random access by entity) | Wastes bandwidth when a loop uses few fields; hard to vectorize (strided gathers) |
| **SoA** | Hot loops touch one or a few fields across many objects; SIMD and GPU coalescing | Accessing one whole object touches many arrays (many streams, more TLB pressure); awkward API |
| **AoSoA** (for example, blocks of 8 or 16 elements per field) | You want SIMD-width chunks with locality per object | More complex indexing |
| **Hot/cold split** | A few hot fields plus rarely used cold fields | Extra indirection for cold data |

On GPUs the same argument becomes **coalescing**: adjacent lanes should access adjacent addresses. See [Parallel GPU Programming -- Global Memory Coalescing](../ml-gpu/Parallel_GPU_Programming.md#201-global-memory-coalescing).

## 5.6 False Sharing and alignas(64)

The coherence protocol tracks ownership **per cache line**. When two cores write different variables that live in the same line, the line bounces between their caches (MESI invalidations), even though the threads share no data logically.

```cpp
// false_sharing.cpp -- per-thread counters packed into one cache line vs padded to 64 B
// g++ -std=c++20 -O2 -pthread false_sharing.cpp -o false_sharing && ./false_sharing
#include <atomic>
#include <chrono>
#include <cstdio>
#include <thread>
#include <vector>

constexpr int kThreads = 4;
constexpr long kIters = 50'000'000;

struct Packed {                       // 4 x 8 B = 32 B contiguous: all counters sit in one (at most two) 64 B cache lines
    std::atomic<long> v{0};
};
struct alignas(64) Padded {           // each counter owns a full 64 B line
    std::atomic<long> v{0};
};
static_assert(sizeof(Packed) == 8 && sizeof(Padded) == 64);

template <class Counter>
double run() {
    std::vector<Counter> counters(kThreads);   // C++17: vector honours over-aligned types
    auto t0 = std::chrono::steady_clock::now();
    std::vector<std::thread> ts;
    for (int t = 0; t < kThreads; ++t)
        ts.emplace_back([&counters, t] {
            for (long i = 0; i < kIters; ++i)
                counters[t].v.fetch_add(1, std::memory_order_relaxed);   // no logical sharing
        });
    for (auto& th : ts) th.join();
    return std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
}

int main() {
    std::printf("packed (false sharing): %7.1f ms\n", run<Packed>());
    std::printf("padded (alignas(64))  : %7.1f ms\n", run<Padded>());
}
```

```text
packed (false sharing):  1344.8 ms
padded (alignas(64))  :   221.5 ms
```

That is a 6x difference with zero logical sharing (4 threads pinned to 4 cores of one CCD). Notes:

- **`std::hardware_destructive_interference_size`** (C++17, `<new>`) is the portable name for "padding to avoid false sharing". GCC warns (`-Winterference-size`) when it is used in a header, because its value can change with `-mtune` and would then silently change struct layout across translation units, an ABI hazard. Many codebases simply hard-code 64. Some use **128**, because some Intel cores have an adjacent-line prefetcher that pulls cache lines in pairs, and Apple M-series cores use 128-byte lines.
- **Detecting it:** `perf c2c record/report` shows cache lines with HITM (hit-modified) traffic from multiple cores. The symptom is that adding threads makes the program *slower*.
- **The better fix** is often structural: accumulate in a thread-local variable (a register) and write once at the end. That is what OpenMP `reduction` does.
- **GPU analogue:** atomics from many lanes on one address serialize. Use a per-wave reduction (shuffles), then one atomic per wave or block. See [Parallel GPU Programming -- Atomic Operations](../ml-gpu/Parallel_GPU_Programming.md#213-atomic-operations).

## 5.7 Prefetching

**Hardware prefetchers** detect sequential and constant-stride streams (next-line, stride, and stream prefetchers at L1 and L2) and fetch ahead automatically. They cannot predict **data-dependent** addresses: indirect `a[idx[i]]`, pointer chasing, hash tables. **Software prefetch** (`__builtin_prefetch(addr, rw, locality)` in GCC and Clang, which compiles to `prefetcht0/t1/t2/nta` on x86) requests a line early without blocking.

```cpp
// prefetch.cpp -- software prefetch for an indirect (gather) access pattern
// g++ -std=c++20 -O2 prefetch.cpp -o prefetch && ./prefetch
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <random>
#include <vector>

template <int Distance>
double gather_sum(const std::vector<double>& data, const std::vector<std::uint32_t>& idx) {
    double s = 0;
    const std::size_t n = idx.size();
    for (std::size_t i = 0; i < n; ++i) {
        if constexpr (Distance > 0)
            if (i + Distance < n)
                __builtin_prefetch(&data[idx[i + Distance]], /*rw=*/0, /*locality=*/1);
        s += data[idx[i]];          // hardware prefetchers cannot predict idx[i]
    }
    return s;
}

int main() {
    constexpr std::size_t kData = 1 << 26;      // 64M doubles = 512 MiB, far larger than LLC
    constexpr std::size_t kIdx = 1 << 24;
    std::vector<double> data(kData, 1.0);
    std::vector<std::uint32_t> idx(kIdx);
    std::mt19937 rng(1);
    std::uniform_int_distribution<std::uint32_t> dist(0, kData - 1);
    for (auto& i : idx) i = dist(rng);

    auto time = [&](const char* name, auto fn) {
        auto t0 = std::chrono::steady_clock::now();
        double s = fn();
        double ms = std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
        std::printf("%-22s %7.1f ms  (sum=%.0f)\n", name, ms, s);
    };
    time("no prefetch", [&] { return gather_sum<0>(data, idx); });
    time("prefetch distance 16", [&] { return gather_sum<16>(data, idx); });
    time("prefetch distance 64", [&] { return gather_sum<64>(data, idx); });
}
```

Two consecutive runs:

```text
no prefetch               68.8 ms  (sum=16777216)      <- run 1: includes warm-up effects
prefetch distance 16      58.3 ms  (sum=16777216)
prefetch distance 64      42.4 ms  (sum=16777216)
no prefetch               56.6 ms  (sum=16777216)      <- run 2
prefetch distance 16      58.2 ms  (sum=16777216)
prefetch distance 64      42.0 ms  (sum=16777216)
```

Lessons:

1. **The gain is modest (~1.35x), not 10x.** The loads are independent, so the out-of-order core already overlaps about 37 misses (Little's law, 4.2). Prefetch helps by reaching **further ahead** than the reorder window. Gains are larger when each iteration does a lot of work (the window fills with compute) or in pointer chases where you can prefetch a node's children.
2. **Choosing the distance:** `distance ~= memory latency / time per iteration`. At ~120 ns latency and ~2.5-3.5 ns per iteration, that is about 40, so 16 is too short. Too long a distance evicts lines before use.
3. **Costs:** prefetch instructions consume issue slots and fill buffers. A prefetch for a line that is already cached is pure overhead. Always measure.
4. **Notice the first "no prefetch" run (68.8 vs 56.6 ms):** a warm-up effect. Section 8 covers why benchmarks need warm-up runs and repetitions.

## 5.8 TLB Effects and Huge Pages

Every access needs a virtual-to-physical translation. **TLB reach** is `entries x page size`:

| Structure (typical server core) | Entries | Reach at 4 KiB | Reach at 2 MiB |
|---|---|---|---|
| L1 DTLB | ~64-96 | ~256-384 KiB | ~128-192 MiB |
| L2 (shared) TLB | ~2K-4K | ~8-16 MiB | ~4-8 GiB |

A TLB miss triggers a **page walk** (up to 4-5 dependent memory accesses, partly cached in page-walk caches). In the latency ladder (5.1), the 1 MiB working set took 5.3 ns per load with 4 KiB pages but 3.2 ns with huge pages (L1 DTLB misses removed), and at 1 GiB huge pages saved about 15 ns per load.

**Getting huge pages on Linux:**

```bash
cat /sys/kernel/mm/transparent_hugepage/enabled     # [always] madvise never
# In code: madvise(ptr, len, MADV_HUGEPAGE) on a 2 MiB-aligned region (see latency_ladder.cpp)
grep -i huge /proc/meminfo                           # AnonHugePages: how much THP is in use
# Explicit (pre-reserved) huge pages for hugetlbfs / MAP_HUGETLB:
echo 1024 | sudo tee /proc/sys/vm/nr_hugepages
```

Tradeoffs: THP can cause latency spikes from compaction (`khugepaged`) and memory bloat, which is why some databases recommend `madvise` mode rather than `always`. GPUs have TLBs too (UTCL1/UTCL2 on AMD). Large contiguous allocations and big fragment sizes reduce GPU translation misses, and the translation cost is very visible for scattered access over huge buffers or for unified/host memory.

> **See also:** [CS Fundamentals -- Virtual Memory / TLB](./CS_Fundamentals.md#76-virtual-memory); [Linux Command Line](../tools/Linux_Command_Line.md); [Debugging and Profiling Tools](../tools/Debugging_and_Profiling_Tools.md) for `perf stat -e dTLB-load-misses`, `perf c2c`.

## 5.9 Interview Questions

**Q1.** Why is iterating a 2D C array column-by-column slower than row-by-row, by how much, and how would you fix it?

C arrays are row-major, so the column walk has a stride of one row (`N x 4 B = 16 KiB` for a 4096-wide float matrix). Each fetched 64-byte line delivers 4 useful bytes instead of 64 (1/16 utilization). Every access touches a new page (TLB misses), and with a power-of-two stride all accesses map to the same cache set, so only the associativity's worth of lines survive. Measured slowdown here: about 11x. Fixes: interchange the loops, transpose once if the access pattern requires columns, pad the leading dimension to break the set aliasing, or tile so that a block of columns is processed while its lines are cached.

**Q2.** Explain loop tiling for matrix multiply. How do you choose the tile size?

Tiling restructures the loops so that a `T x T` block of each matrix is reused `T` times while it sits in a fast level of the hierarchy, cutting DRAM traffic from `O(n^3)` to `O(n^3/T)` and raising arithmetic intensity to about `T/4` FLOP/B (FP32). Choose `T` so the working set (three tiles, `3T^2 x element size`) fits in the target level with room for other data. For example, `T ~= 64` for a 48 KiB L1 in FP32. In practice, tile at multiple levels (registers, L1, L2), make `T` a multiple of the SIMD width, and autotune, because associativity, prefetchers, and TLB reach all interact. Packing tiles into contiguous buffers removes conflict and TLB misses. Library GEMMs do all of this.

**Q3.** What is false sharing, how do you detect it, and how do you fix it?

Two threads write to different variables in the same cache line. Coherence forces the line to bounce between the cores' caches, so each write turns into a cross-core invalidation (tens of ns) instead of an L1 hit. Symptoms: poor scaling, or *negative* scaling, with no logical sharing. Detection: `perf c2c` (HITM on shared lines), or VTune/uProf memory-access analysis. Fixes: `alignas(64)` (or 128) padding per thread; `std::hardware_destructive_interference_size`; accumulating in thread-local variables and combining once; making per-thread data structurally separate (arrays of per-thread structs, each padded). Measured here: 6x.

**Q4.** When does software prefetching help, and when does it hurt?

It helps for access patterns that hardware prefetchers cannot predict (indirect gathers, pointer-based structures, hash probes), when the prefetch distance roughly matches the latency, and when the out-of-order window cannot already see far enough ahead. It hurts when data is already cached (wasted slots), when the distance is too long (lines evicted before use) or too short (the data still arrives late), when it competes for fill buffers with demand misses, or when the loop is compute-bound. Always A/B measure. Gains are typically 1.2-2x, not 10x.

**Q5.** What are huge pages and why do they help some workloads?

Huge pages (2 MiB or 1 GiB on x86-64) let each TLB entry cover 512x or 262,144x more memory, so large working sets with poor locality (random access over GBs: hash tables, graphs, databases, JVM heaps) suffer far fewer TLB misses and page walks. Costs: internal fragmentation, compaction stalls with THP, and allocation failures when memory is fragmented. Use `madvise(MADV_HUGEPAGE)` for specific large regions, or pre-reserved hugetlbfs pages for predictable latency.

**Q6.** Break address `0x0001_2345` into tag, set, and offset for a 64 KiB, 4-way cache with 64 B lines.

Lines = 64 KiB / 64 = 1024; sets = 1024 / 4 = 256, so there are 6 offset bits and 8 index bits. Offset = `0x12345 & 0x3F = 0x05`. Set = `(0x12345 >> 6) & 0xFF = 0x48D & 0xFF = 0x8D = 141`. Tag = `0x12345 >> 14 = 0x4`.

---

# 6. SIMD and Vectorization

---

## 6.1 SIMD Widths and ISA Extensions

| Extension | Register width | FP32 lanes | FP64 lanes | Notable features |
|---|---|---|---|---|
| SSE / SSE2 (x86-64 baseline) | 128-bit `xmm` | 4 | 2 | Every x86-64 CPU has it |
| AVX | 256-bit `ymm` | 8 | 4 | FP only (integer 256-bit came with AVX2) |
| AVX2 + FMA3 | 256-bit | 8 | 4 | 256-bit integer ops, gathers, fused multiply-add |
| AVX-512 (F, VL, BW, DQ, ...) | 512-bit `zmm` | 16 | 8 | 32 registers, **mask registers** `k0-k7` (predication, tail handling), scatter, compress/expand |
| Arm NEON / SVE | 128 / scalable 128-2048 | 4 / VL-dependent | 2 / VL-dependent | SVE is vector-length agnostic |

`-march=x86-64-v3` means AVX2 + FMA + BMI and so on. `-march=x86-64-v4` adds AVX-512 F/BW/CD/DQ/VL. Implementation notes interviewers sometimes probe: some older Intel server cores lowered their clock frequency when running heavy AVX-512 code; Zen 4 executes 512-bit ops on 256-bit datapaths (double-pumped); and Zen 5 server parts have full 512-bit datapaths. **The ISA width is not the same as the execution throughput**, so measure.

**Peak FLOPs per core** = `FMA units x lanes x 2`. For two 256-bit FMA pipes in FP64: `2 x 4 x 2 = 16 FLOP/cycle`. Reaching it also needs enough **independent** FMAs in flight: `latency x throughput = 4 cycles x 2 per cycle = 8` independent accumulators. A single-accumulator dot product runs at 1/8 of peak even when it is fully vectorized.

## 6.2 Intrinsics: SSE, AVX2, AVX-512

```cpp
// simd.cpp -- SAXPY and dot product with SSE, AVX2+FMA and (if available) AVX-512 intrinsics
// g++ -std=c++20 -O2 -mavx2 -mfma simd.cpp -o simd && ./simd
// add -mavx512f to also build the AVX-512 path (run only on a CPU that supports it)
#include <immintrin.h>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <vector>

// y[i] = a * x[i] + y[i]  -- scalar reference
void saxpy_scalar(std::size_t n, float a, const float* x, float* y) {
    for (std::size_t i = 0; i < n; ++i) y[i] = a * x[i] + y[i];
}

// SSE: 4 floats per 128-bit register
void saxpy_sse(std::size_t n, float a, const float* x, float* y) {
    const __m128 va = _mm_set1_ps(a);
    std::size_t i = 0;
    for (; i + 4 <= n; i += 4) {
        __m128 vx = _mm_loadu_ps(x + i);                 // unaligned load is fine on modern cores
        __m128 vy = _mm_loadu_ps(y + i);
        _mm_storeu_ps(y + i, _mm_add_ps(_mm_mul_ps(va, vx), vy));
    }
    for (; i < n; ++i) y[i] = a * x[i] + y[i];           // scalar remainder ("tail")
}

// AVX2 + FMA: 8 floats per 256-bit register, fused multiply-add
void saxpy_avx2(std::size_t n, float a, const float* x, float* y) {
    const __m256 va = _mm256_set1_ps(a);
    std::size_t i = 0;
    for (; i + 8 <= n; i += 8) {
        __m256 vy = _mm256_fmadd_ps(va, _mm256_loadu_ps(x + i), _mm256_loadu_ps(y + i));
        _mm256_storeu_ps(y + i, vy);
    }
    for (; i < n; ++i) y[i] = std::fma(a, x[i], y[i]);  // same rounding as the vector body
}

// Dot product: 4 independent accumulators hide the 4-cycle FMA latency (ILP),
// then a horizontal reduction collapses 8 lanes to 1.
float dot_avx2(std::size_t n, const float* x, const float* y) {
    __m256 acc0 = _mm256_setzero_ps(), acc1 = acc0, acc2 = acc0, acc3 = acc0;
    std::size_t i = 0;
    for (; i + 32 <= n; i += 32) {
        acc0 = _mm256_fmadd_ps(_mm256_loadu_ps(x + i),      _mm256_loadu_ps(y + i),      acc0);
        acc1 = _mm256_fmadd_ps(_mm256_loadu_ps(x + i + 8),  _mm256_loadu_ps(y + i + 8),  acc1);
        acc2 = _mm256_fmadd_ps(_mm256_loadu_ps(x + i + 16), _mm256_loadu_ps(y + i + 16), acc2);
        acc3 = _mm256_fmadd_ps(_mm256_loadu_ps(x + i + 24), _mm256_loadu_ps(y + i + 24), acc3);
    }
    __m256 acc = _mm256_add_ps(_mm256_add_ps(acc0, acc1), _mm256_add_ps(acc2, acc3));
    __m128 lo = _mm256_castps256_ps128(acc), hi = _mm256_extractf128_ps(acc, 1);
    __m128 s = _mm_add_ps(lo, hi);                         // 8 -> 4 lanes
    s = _mm_add_ps(s, _mm_movehl_ps(s, s));                // 4 -> 2
    s = _mm_add_ss(s, _mm_shuffle_ps(s, s, 0x1));          // 2 -> 1
    float r = _mm_cvtss_f32(s);
    for (; i < n; ++i) r += x[i] * y[i];
    return r;
}

#ifdef __AVX512F__
// AVX-512: 16 floats per 512-bit register; masked tail instead of a scalar loop
void saxpy_avx512(std::size_t n, float a, const float* x, float* y) {
    const __m512 va = _mm512_set1_ps(a);
    std::size_t i = 0;
    for (; i + 16 <= n; i += 16)
        _mm512_storeu_ps(y + i, _mm512_fmadd_ps(va, _mm512_loadu_ps(x + i), _mm512_loadu_ps(y + i)));
    if (i < n) {
        const __mmask16 m = static_cast<__mmask16>((1u << (n - i)) - 1);
        __m512 vy = _mm512_fmadd_ps(va, _mm512_maskz_loadu_ps(m, x + i), _mm512_maskz_loadu_ps(m, y + i));
        _mm512_mask_storeu_ps(y + i, m, vy);
    }
}
#endif

int main() {
    const std::size_t n = 1003;                          // deliberately not a multiple of 8/16
    std::vector<float> x(n), y0(n), y1, y2;
    for (std::size_t i = 0; i < n; ++i) { x[i] = 0.001f * i; y0[i] = 1.0f; }
    y1 = y0; y2 = y0;
    saxpy_scalar(n, 2.0f, x.data(), y0.data());
    saxpy_sse(n, 2.0f, x.data(), y1.data());
    saxpy_avx2(n, 2.0f, x.data(), y2.data());
    float maxdiff = 0;
    for (std::size_t i = 0; i < n; ++i)
        maxdiff = std::fmax(maxdiff, std::fmax(std::fabs(y0[i] - y1[i]), std::fabs(y0[i] - y2[i])));
    std::printf("saxpy max diff vs scalar: %g\n", maxdiff);
    std::printf("dot avx2 = %.4f\n", dot_avx2(n, x.data(), y0.data()));
#ifdef __AVX512F__
    {   // a binary built with -mavx512f may use AVX-512 anywhere: run it only on AVX-512 CPUs
        std::vector<float> y3(n, 1.0f);
        saxpy_avx512(n, 2.0f, x.data(), y3.data());
        std::printf("avx512 y[n-1] = %.4f (scalar %.4f)\n", y3[n - 1], y0[n - 1]);
    }
#endif
}
```

```text
saxpy max diff vs scalar: 0
dot avx2 = 1174.1820
avx512 y[n-1] = 3.0040 (scalar 3.0040)
```

Points to make when walking through this code:

- **The tail.** `n` is rarely a multiple of the vector width. Options: a scalar remainder loop (SSE/AVX2), **masked** loads and stores (AVX-512 `__mmask16`, also SVE and GPU EXEC masks), or padding the allocation.
- **Multiple accumulators** in `dot_avx2` break the loop-carried dependency on the FMA latency. With one accumulator, the loop issues one FMA every 4 cycles. With four, it approaches the throughput limit (raise to 8 for two FMA pipes). This is also why the vectorized dot product's result differs in the last bits from the scalar one: **a different summation order** (Section 9).
- **FMA changes rounding.** `fma(a, x, y)` rounds once and `a*x + y` rounds twice, so an FMA vector body and a non-FMA scalar tail can disagree in the last bit. That is why the AVX2 tail uses `std::fma`.
- **Intrinsics are a last resort.** Prefer (1) a library (BLAS, Eigen, oneDNN, Highway, xsimd, `std::experimental::simd`), (2) auto-vectorization with a clean loop plus `#pragma omp simd`, and (3) intrinsics only for hot kernels where (1) and (2) fail. Intrinsics tie the code to one ISA and need runtime dispatch.

## 6.3 Runtime Dispatch

Distributing a binary built with `-mavx2` crashes with `SIGILL` on CPUs without AVX2. Instead, compile individual functions for specific targets and choose one at runtime:

```cpp
// dispatch.cpp -- one portable binary, AVX2 path chosen at runtime
// g++ -std=c++20 -O2 dispatch.cpp -o dispatch && ./dispatch      (note: no -mavx2 needed)
#include <immintrin.h>
#include <cstdio>
#include <vector>

__attribute__((target("avx2,fma")))
void scale_avx2(float* y, const float* x, float a, std::size_t n) {
    std::size_t i = 0;
    for (; i + 8 <= n; i += 8)
        _mm256_storeu_ps(y + i, _mm256_mul_ps(_mm256_set1_ps(a), _mm256_loadu_ps(x + i)));
    for (; i < n; ++i) y[i] = a * x[i];
}

void scale_generic(float* y, const float* x, float a, std::size_t n) {
    for (std::size_t i = 0; i < n; ++i) y[i] = a * x[i];   // SSE2 baseline (x86-64)
}

using ScaleFn = void (*)(float*, const float*, float, std::size_t);

ScaleFn pick_scale() {
    __builtin_cpu_init();
    return __builtin_cpu_supports("avx2") && __builtin_cpu_supports("fma") ? scale_avx2 : scale_generic;
}

int main() {
    static const ScaleFn scale = pick_scale();             // resolve once, call many times
    std::vector<float> x(100, 1.5f), y(100);
    scale(y.data(), x.data(), 2.0f, x.size());
    std::printf("y[99]=%.1f via %s\n", y[99], scale == scale_avx2 ? "avx2" : "generic");
}
```

GCC and Clang can also generate the clones and the dispatcher automatically with `__attribute__((target_clones("avx512f", "avx2", "default")))` (resolved once at load time via an IFUNC). glibc's `memcpy`/`strlen` use the same IFUNC mechanism; oneDNN and PyTorch's ATen CPU kernels do their own runtime CPU-capability dispatch.

## 6.4 Auto-Vectorization and Compiler Reports

GCC vectorizes at `-O2` since GCC 12, using a "very cheap" cost model that refuses anything needing runtime checks. At `-O3` it uses the full cost model. Clang vectorizes at `-O2`. **Always read the report** rather than guessing:

```cpp
// vec_report.cpp -- loops to inspect with the compiler's vectorization report
// g++ -std=c++20 -O2 -c vec_report.cpp -fopt-info-vec-optimized -fopt-info-vec-missed
// clang++ -std=c++20 -O2 -c vec_report.cpp -Rpass=loop-vectorize -Rpass-missed=loop-vectorize -Rpass-analysis=loop-vectorize
#include <cstddef>

// (1) May alias: compiler must version the loop with a runtime overlap check (or give up).
void add_may_alias(float* dst, const float* a, const float* b, std::size_t n) {
    for (std::size_t i = 0; i < n; ++i) dst[i] = a[i] + b[i];
}

// (2) __restrict__ promises no overlap: straight vector code, no runtime check.
void add_restrict(float* __restrict__ dst, const float* __restrict__ a,
                  const float* __restrict__ b, std::size_t n) {
    for (std::size_t i = 0; i < n; ++i) dst[i] = a[i] + b[i];
}

// (3) FP reduction: NOT vectorized at -O2 without reassociation permission
//     (-ffast-math / -fassociative-math, or #pragma omp simd reduction(+:s) with -fopenmp-simd).
float sum(const float* a, std::size_t n) {
    float s = 0;
    for (std::size_t i = 0; i < n; ++i) s += a[i];
    return s;
}

// (4) Loop-carried dependence: a[i] depends on a[i-1], cannot be vectorized as written.
void prefix(float* a, std::size_t n) {
    for (std::size_t i = 1; i < n; ++i) a[i] += a[i - 1];
}
```

GCC 15 output, abbreviated:

```text
$ g++ -std=c++20 -O2 -c vec_report.cpp -fopt-info-vec-optimized
vec_report.cpp:14:31: optimized: loop vectorized using 16 byte vectors           <- only (2)

$ g++ -std=c++20 -O3 -c vec_report.cpp -fopt-info-vec-optimized
vec_report.cpp:8:31: optimized: loop vectorized using 16 byte vectors
vec_report.cpp:8:31: optimized:  loop versioned for vectorization because of possible aliasing
vec_report.cpp:14:31: optimized: loop vectorized using 16 byte vectors
vec_report.cpp:21:31: optimized: loop vectorized using 16 byte vectors           <- see warning below

$ g++ -std=c++20 -O3 -march=x86-64-v3 -c vec_report.cpp -fopt-info-vec-optimized
vec_report.cpp:8:31: optimized: loop vectorized using 32 byte vectors            <- AVX2 width
```

How to read it:

1. **At `-O2`, the may-alias loop (1) is not vectorized at all.** The very-cheap model will not emit the runtime overlap check. `__restrict__` (2) or `-O3` fixes it. At `-O3`, GCC **versions** the loop: a vector version when the pointers do not overlap, a scalar version otherwise.
2. **"Vectorized" does not always mean fast.** For the float sum (3), GCC 15 at `-O3` reports "vectorized", but the assembly shows a vector load followed by four **sequential scalar `addss`** instructions per iteration. That is an in-order ("fold-left") reduction that preserves the source order, so the add latency chain is still serial. Real speedup needs permission to reassociate: `-ffast-math` (too broad), `-fassociative-math -fno-signed-zeros -fno-trapping-math`, or, more precisely, `#pragma omp simd reduction(+:s)` with `-fopenmp-simd`. **Check the assembly** (`objdump -d`, Compiler Explorer) or the IR.
3. **The prefix sum (4) has a true dependence.** It needs an algorithm change (a blocked scan) to vectorize.
4. **Width:** `16 byte vectors` means SSE. To get 32-byte AVX2 vectors, pass `-march=x86-64-v3`, `-mavx2`, or `-march=native` (the last only for binaries that run on the build machine).

**Common vectorization blockers:**

| Blocker | Fix |
|---|---|
| Possible pointer aliasing | `__restrict__`, `#pragma omp simd`, `#pragma GCC ivdep`, or copy to locals |
| FP reduction (reassociation not allowed) | `#pragma omp simd reduction(+:s)`, `-fassociative-math`, or manual multiple accumulators |
| Function calls in the body | Inline them; `#pragma omp declare simd`; use vector math libraries (libmvec, SLEEF) |
| Complex control flow / early `break` | Restructure; the compiler can if-convert simple branches into blends or masks |
| Non-unit stride, indirect `a[idx[i]]` | Change the data layout (SoA); gathers exist but are slow |
| Loop-carried dependence | Change the algorithm (blocked scan, reorder the loops) |
| Mixed types and conversions | Keep types uniform (for example, all `float`, avoiding implicit `double` promotion from literals like `0.5`) |
| Unknown or small trip count | Usually fine (the compiler emits checks); very short loops may not be worth vectorizing |

## 6.5 Aliasing, restrict, and Alignment

**Aliasing.** If `dst` might overlap `a` (`dst == a + 1`), then vectorizing `dst[i] = a[i] + b[i]` would read values before the scalar loop would have written them. The compiler must prove there is no overlap, check at runtime, or give up.

- `__restrict__` (a GCC/Clang extension; MSVC spells it `__restrict`; `restrict` is standard only in C99) is **a promise**. Violating it is undefined behaviour, and the program silently produces wrong results.
- **Strict aliasing** (type-based) is a separate rule: the compiler may assume a `float*` and an `int*` never point to the same object. It is broken by type punning through pointer casts. Use `std::bit_cast` (C++20) or `memcpy` instead.

**Alignment.**

```cpp
// fragment
#include <cstdlib>
#include <memory>

alignas(64) float buf[1024];                                  // static/stack: 64 B aligned
float* p = static_cast<float*>(std::aligned_alloc(64, 4096)); // size must be a multiple of alignment
float* q = std::assume_aligned<64>(p);                        // C++20: promise to the optimizer
// _mm256_load_ps(q) requires 32 B alignment (faults otherwise); _mm256_loadu_ps works for any address
std::free(p);
```

On modern x86 cores, unaligned vector loads (`loadu`) cost about the same as aligned ones **unless the access crosses a cache-line boundary** (and crossing a page boundary is worse). Aligning hot arrays to 64 bytes avoids split loads. Aligned versions such as `_mm256_load_ps` fault on misaligned addresses, so use them only when alignment is guaranteed. GPU buffers from `hipMalloc` are at least 256-byte aligned, and vector loads (`float4`) require natural alignment.

> **See also:** [Parallel GPU Programming -- SIMD and Vectorization (OpenMP)](../ml-gpu/Parallel_GPU_Programming.md#14-simd-and-vectorization); [C++ Fundamentals](../languages/Cpp_Fundamentals.md) for undefined behaviour and strict aliasing; [CMake Fundamentals](../tools/CMake_Fundamentals.md) for per-target `-march` flags.

## 6.6 Interview Questions

**Q1.** Your loop `for (i) dst[i] = a[i] + b[i];` is not vectorized at `-O2` with GCC. Why, and what are your options?

The compiler cannot prove that `dst` does not overlap `a` or `b`. GCC's `-O2` "very-cheap" cost model refuses to emit the runtime overlap check (loop versioning). Options: mark the pointers `__restrict__` if they truly never alias; use `#pragma omp simd` (with `-fopenmp-simd`) to assert independence; compile with `-O3`, which versions the loop with a runtime check; or restructure the API (pass spans of distinct buffers). Confirm with `-fopt-info-vec-optimized`/`-missed` (GCC) or `-Rpass=loop-vectorize`/`-Rpass-missed=loop-vectorize` (Clang).

**Q2.** Why does the compiler refuse to vectorize a floating-point sum, and what are the consequences of forcing it?

Vectorizing a sum computes several partial sums and combines them at the end, which **reorders** the additions. FP addition is not associative, so the result can change, and the compiler must preserve the source semantics unless allowed to reassociate. Forcing it (`-ffast-math`, `-fassociative-math`, `#pragma omp simd reduction`) gives 4-16x on the reduction and slightly different results, which depend on the vector width and so on the ISA and the build flags. That is usually fine, but tests need tolerances and reproducibility needs a fixed build. `-ffast-math` additionally assumes no NaN or Inf, enables flush-to-zero, and can break algorithms such as Kahan summation, so prefer the narrowest flag or a pragma.

**Q3.** What does `-march=native` do, and why is it dangerous for a distributed binary?

It enables every instruction set the build machine supports (for example, AVX-512) and tunes for that CPU. A binary built that way can crash with SIGILL on older or different CPUs, and it can produce different floating-point results (FMA contraction, vector width). For distribution, target a baseline (`-march=x86-64-v2` or `-v3`) and use function multiversioning or runtime dispatch (`target_clones`, `__builtin_cpu_supports`) for hot kernels.

**Q4.** Explain how AVX-512 masking helps compared with AVX2.

AVX-512 has 8 mask registers. Most instructions take a mask that disables lanes, with zeroing or merging semantics. That handles loop tails without a scalar remainder loop, vectorizes loops with `if` conditions (predication instead of blend sequences), and enables compress and expand operations. AVX2 has to emulate these with blends or `maskload`/`maskstore` and extra instructions. GPU SIMT does the same thing in hardware with the EXEC mask, which is why divergence costs lanes rather than correctness.

**Q5.** How many accumulators do you need in a vectorized dot product to reach peak FMA throughput?

Enough to cover `FMA latency x FMA issue rate`. With a 4-cycle latency and 2 FMA pipes, 8 independent vector accumulators are needed. With one accumulator, each FMA waits for the previous one, so you get 1/8 of peak (the loop is latency-bound). Unrolling with multiple accumulators trades a few registers for ILP. For long arrays the dot product is memory-bound anyway (AI = 2 FLOPs / 8 bytes in FP32), so the accumulators matter most for cache-resident data.

---

# 7. NUMA

---

## 7.1 NUMA Topology

In a **Non-Uniform Memory Access** system, each socket (or chiplet group) has its own memory controllers. Accessing memory attached to another node crosses the inter-socket fabric (AMD Infinity Fabric, Intel UPI), with higher latency and lower bandwidth.

```bash
numactl --hardware          # nodes, CPUs per node, memory per node, distance matrix
lscpu | grep -i numa        # NUMA node to CPU mapping
lstopo                      # (hwloc) full topology: sockets, caches, cores, PCIe devices
numastat -p <pid>           # per-node memory usage of a running process
```

Example from the 2-socket server used for this document:

```text
node distances:
node     0    1
   0:   10   32
   1:   32   10
```

Distances are relative (10 = local). A remote access typically costs **~1.5-2x local latency**, and cross-socket bandwidth is a fraction of local DRAM bandwidth. AMD EPYC can also expose multiple NUMA nodes **per socket** ("NPS" = nodes per socket: NPS1, NPS2, NPS4 BIOS settings), so even a single-socket box can be NUMA.

## 7.2 First-Touch Placement

Linux's default policy is **first touch**: `malloc`/`new` only reserves virtual address space, and a physical page is allocated **on the NUMA node of the thread that first writes to it**. If one thread initializes a big array, every page ends up on that thread's node, and the other socket's threads then make remote accesses.

```cpp
// first_touch.cpp -- NUMA first-touch: who initializes memory decides where it lives
// g++ -std=c++20 -O2 -fopenmp first_touch.cpp -o first_touch
// OMP_NUM_THREADS=<all cores> OMP_PROC_BIND=spread OMP_PLACES=cores ./first_touch
#include <omp.h>
#include <chrono>
#include <cstdio>
#include <memory>

double triad_gbs(double* a, const double* b, const double* c, long n) {
    auto t0 = std::chrono::steady_clock::now();
    for (int rep = 0; rep < 10; ++rep) {
#pragma omp parallel for schedule(static)
        for (long i = 0; i < n; ++i) a[i] = b[i] + 3.0 * c[i];      // STREAM triad
    }
    double s = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
    return 10.0 * 3 * n * sizeof(double) / s / 1e9;                // ignores write-allocate
}

int main() {
    const long n = 1L << 27;                                        // 3 arrays x 1 GiB
    // new double[n] (no "()") does NOT touch the pages: physical placement is decided later.
    std::unique_ptr<double[]> a1(new double[n]), b1(new double[n]), c1(new double[n]);
    std::unique_ptr<double[]> a2(new double[n]), b2(new double[n]), c2(new double[n]);

    // BAD: serial init -> every page is first touched by thread 0 -> all on thread 0's node
    for (long i = 0; i < n; ++i) { a1[i] = 0; b1[i] = 1; c1[i] = 2; }

    // GOOD: parallel init with the SAME static schedule as the compute loop
#pragma omp parallel for schedule(static)
    for (long i = 0; i < n; ++i) { a2[i] = 0; b2[i] = 1; c2[i] = 2; }

    triad_gbs(a1.get(), b1.get(), c1.get(), n);                     // warm up both
    triad_gbs(a2.get(), b2.get(), c2.get(), n);
    std::printf("threads=%d\n", omp_get_max_threads());
    std::printf("serial first touch  : %6.1f GB/s\n", triad_gbs(a1.get(), b1.get(), c1.get(), n));
    std::printf("parallel first touch: %6.1f GB/s\n", triad_gbs(a2.get(), b2.get(), c2.get(), n));
}
```

```text
$ OMP_NUM_THREADS=192 OMP_PROC_BIND=spread OMP_PLACES=cores ./first_touch
threads=192
serial first touch  :  234.4 GB/s
parallel first touch:  791.1 GB/s
```

**3.4x from changing only the initialization loop.** With serial initialization, all 3 GiB sit on node 0. Half the threads read remotely, and even the local half competes for one socket's memory controllers.

Pitfalls:

- `std::vector<double> v(n)` **value-initializes**, which zeroes the memory serially in the constructor, so it is first-touched by the constructing thread. For NUMA-sensitive buffers, use an uninitialized allocation (`new double[n]`, `std::make_unique_for_overwrite<double[]>(n)` in C++20, or a custom allocator) and initialize in parallel.
- The initialization schedule must match the compute schedule (`schedule(static)` in both), and threads must be **pinned** (`OMP_PROC_BIND`, `OMP_PLACES`). Otherwise the OS can migrate a thread away from its pages.
- `calloc` and big `malloc`s may get pre-zeroed pages from `mmap`, which are still placed lazily on first touch, so the same rule applies.
- **Automatic NUMA balancing** (`/proc/sys/kernel/numa_balancing`) migrates pages toward the threads that access them. It helps unpinned workloads, but it adds run-to-run variance to benchmarks.

## 7.3 numactl, Binding, and APIs

```bash
numactl --cpunodebind=0 --membind=0 ./app     # run on node 0 CPUs, allocate only from node 0
numactl --physcpubind=0-7 --localalloc ./app  # specific cores; allocate on the local node
numactl --interleave=all ./app                # round-robin pages over all nodes (bandwidth-bound,
                                              #   unpartitionable shared data; avoids hot node)
numactl --preferred=1 ./app                   # prefer node 1, fall back if full
taskset -c 0-15 ./app                         # CPU affinity only (no memory policy)

# OpenMP thread placement
export OMP_PLACES=cores            # one place per physical core
export OMP_PROC_BIND=close         # pack threads near the master (share caches)
export OMP_PROC_BIND=spread        # spread over sockets (maximize aggregate bandwidth)

# MPI: one rank per NUMA node (or per GPU), bound -- e.g. Open MPI
mpirun -np 2 --map-by numa --bind-to numa ./app
```

Programmatic control (link with `-lnuma`):

```cpp
// fragment -- libnuma / syscalls
#include <numa.h>
void* p = numa_alloc_onnode(bytes, /*node=*/1);   // physical pages on node 1
numa_free(p, bytes);
// mbind(addr, len, MPOL_BIND, nodemask, maxnode, flags)  -- set policy for a range
// move_pages(pid, count, pages, nodes, status, flags)    -- migrate / query page locations
// sched_setaffinity / pthread_setaffinity_np             -- pin threads
```

| Strategy | When |
|---|---|
| Partition data per node + first touch + pinning | Data-parallel loops (stencils, STREAM, OpenMP for loops) |
| Interleave | Shared read-mostly data that every thread accesses uniformly; hash tables; when you cannot partition |
| One process per NUMA node (MPI rank / service instance) | Simplest path to locality; avoids cross-node sharing entirely |
| Replicate read-only data per node | Lookup tables or model weights read by all threads |

## 7.4 NUMA and GPUs

- **PCIe locality:** each GPU hangs off a specific socket's root complex. Host threads feeding a GPU, and the pinned host buffers used for transfers, should be on **the GPU's NUMA node**. Otherwise H2D/D2H copies cross the socket interconnect.

  ```bash
  cat /sys/bus/pci/devices/0000:c1:00.0/numa_node   # NUMA node of a PCIe device (BDF from lspci)
  lstopo                                            # (hwloc) shows which GPUs/NICs hang off which node
  ```

- **GPU-internal NUMA:** MI300X is built from 8 XCDs (accelerator dies), each with its own L2, sharing the HBM stacks and Infinity Cache. It supports compute partitioning modes (for example, SPX, which exposes one GPU, and CPX, which exposes each XCD as a separate GPU) and memory partitioning (NPS1/NPS4). Workgroup-to-XCD placement affects L2 locality. Details are in [AMD GPU Architecture and Profiling](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md).
- **Multi-GPU:** GPU-to-GPU traffic over xGMI/Infinity Fabric or NVLink is far faster than staging through the host. Topology-aware rank placement matters for collectives (`rocm-smi --showtopo` / `amd-smi topology`, `nvidia-smi topo -m`).

> **See also:** [Parallel GPU Programming -- NUMA Awareness](../ml-gpu/Parallel_GPU_Programming.md#163-numa-awareness) and [Thread Affinity and Binding](../ml-gpu/Parallel_GPU_Programming.md#162-thread-affinity-and-binding); [Linux Command Line](../tools/Linux_Command_Line.md).

## 7.5 Interview Questions

**Q1.** What is the first-touch policy, and how can it ruin the scaling of a parallel program?

Linux allocates a physical page on the NUMA node of the thread that first writes to it, not the thread that called `malloc`. If the main thread initializes all arrays serially (including through `std::vector`'s zeroing constructor), every page lands on node 0. During the parallel phase, threads on the other socket access memory remotely, and all threads compete for node 0's memory controllers. Bandwidth-bound loops then scale only to one socket's bandwidth or worse (3.4x lost in the measured triad). Fix: initialize in parallel with the same static schedule and pinned threads, or use `numactl --interleave` when the access pattern cannot be partitioned.

**Q2.** When would you use `numactl --interleave=all` instead of local allocation?

When the data is shared and accessed uniformly by threads on all nodes, and you cannot partition it (a large hash table, a shared read-mostly index, a memory-bound program you cannot modify), or when local allocation would put everything on one node because of serial initialization. Interleaving spreads the bandwidth demand across all memory controllers. Every thread then sees an average latency (part local, part remote) rather than the best case. For partitionable data, local placement plus pinning wins.

**Q3.** A benchmark's results vary by 30% from run to run on a 2-socket server. What NUMA-related causes do you check?

Unpinned threads migrating across sockets; memory placed on whichever node the process happened to start on; automatic NUMA balancing migrating pages mid-run; page cache or other processes occupying a node's memory, which forces remote allocation; THP availability differing per node; and, for GPU benchmarks, the host thread or pinned buffers landing on the far socket from the GPU. Fixes: `numactl --cpunodebind --membind` (or `OMP_PROC_BIND`/`OMP_PLACES`), disable `numa_balancing` for the benchmark, and record the topology (`numactl -H`, `numastat`) with the results.

**Q4.** How do you place host threads and buffers for a multi-GPU node?

Find each GPU's NUMA node (`/sys/bus/pci/devices/<BDF>/numa_node`, `lstopo`). Run one rank or process per GPU, pinned to cores on that node. Allocate pinned host staging buffers there (allocate after pinning, or with `numa_alloc_onnode`), and set `HIP_VISIBLE_DEVICES`/`CUDA_VISIBLE_DEVICES` per rank to match. Also consider NIC locality for GPUDirect RDMA, so the GPU and NIC share a PCIe switch or root complex.

---

# 8. Benchmarking Rigor

---

"It got 7% faster" is a statistical claim about noisy measurements. For a profiling-tools engineer, **how you measure** is itself a core interview topic: warm-up, variance, robust statistics, environmental control, and the perturbation the measurement tool introduces.

## 8.1 Sources of Noise

| Source | Effect | Mitigation |
|---|---|---|
| **Cold start** (cache, TLB, page faults on first touch, lazy symbol binding, allocator growth, JIT, GPU code-object load and first-launch setup) | First iterations much slower | Warm-up iterations; pre-fault memory; report steady state and cold start separately if both matter |
| **CPU frequency scaling** (governor, turbo/boost, thermal and power limits) | Same code runs at 2.4 or 5 GHz depending on load, temperature, and other cores | `performance` governor, disable boost for A/B, monitor frequency (`turbostat`), or count cycles instead of time |
| **Idle states (C-states)** | Wake-up latency adds to short-request latency | Limit deep C-states for latency benchmarks |
| **Other tenants / background daemons / interrupts** | Random outliers, bimodal results | Dedicated machine; `isolcpus`/`nohz_full`; pin away from IRQ-heavy cores; repeat and use robust statistics |
| **SMT siblings** | A sibling hyperthread steals core resources | Pin to one logical CPU per core, or disable SMT |
| **Memory layout / ASLR / environment size / link order** | Different code and stack alignment changes performance by several percent (Mytkowicz et al., "Producing Wrong Data Without Doing Anything Obviously Wrong!", ASPLOS 2009) | Randomize layout across runs (multiple builds, link orders, `setarch -R` to control ASLR) and report the spread |
| **NUMA placement / page migration** | Run-to-run differences of 10-50% | Pin CPU and memory (`numactl`), disable `numa_balancing` |
| **Dead-code elimination / constant folding** | "0 ns" benchmarks: the compiler deleted the work | `DoNotOptimize`-style escapes; consume results; feed inputs the compiler cannot see |
| **Timer resolution and overhead** | Timing a 20 ns operation with a 25 ns clock read | Batch many iterations per timing sample |
| **GPU: async launch, clock ramp, power cap, warm caches** | CPU timers measure launch, not execution; first kernels run at idle clocks; repeated kernels hit the 256 MB Infinity Cache | GPU events or synchronization; warm-up; clock control; flush or rotate buffers (8.7) |

## 8.2 Controlling the Environment

```bash
# CPU frequency: fixed governor; disable boost for low-variance A/B (re-enable afterwards!)
sudo cpupower frequency-set -g performance
cat /sys/devices/system/cpu/cpufreq/boost                 # acpi-cpufreq / amd-pstate: 1 = boost on
echo 0 | sudo tee /sys/devices/system/cpu/cpufreq/boost
echo 1 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo    # intel_pstate systems
sudo turbostat --quiet --interval 1                       # watch actual frequency while benchmarking

# Placement: pin the benchmark to one core (or one NUMA node), away from core 0's interrupts
taskset -c 5 ./bench
numactl --cpunodebind=0 --membind=0 ./bench
echo 0 | sudo tee /proc/sys/kernel/numa_balancing

# Layout: run without ASLR to reduce variance (or deliberately WITH it, to sample layouts)
setarch "$(uname -m)" -R ./bench

# Hardware counters: repeat 10x and report mean +- stddev
perf stat -r 10 -e task-clock,cycles,instructions,cache-misses ./bench

# File I/O benchmarks only: drop the page cache for cold-cache runs
sync; echo 3 | sudo tee /proc/sys/vm/drop_caches
```

**Measure cycles, not just seconds.** `perf stat` cycles and instructions (IPC) are far less sensitive to frequency changes than wall time. Report both, along with the machine, compiler, flags, kernel, and driver versions.

## 8.3 A Minimal Honest Harness

```cpp
// bench_harness.cpp -- minimal, honest microbenchmark harness: warmup, repetitions, robust stats
// g++ -std=c++20 -O2 bench_harness.cpp -o bench_harness && ./bench_harness
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdio>
#include <numeric>
#include <vector>

// Keep the optimizer from deleting work whose result is unused (same idea as
// benchmark::DoNotOptimize): the empty asm "uses" the value and clobbers memory.
template <class T>
inline void do_not_optimize(T const& value) { asm volatile("" : : "r,m"(value) : "memory"); }

struct Stats { double min, median, mean, stddev, mad, p95; };

Stats summarize(std::vector<double> v) {
    std::sort(v.begin(), v.end());
    auto pct = [&](double p) { return v[static_cast<std::size_t>(p * (v.size() - 1) + 0.5)]; };
    const double mean = std::accumulate(v.begin(), v.end(), 0.0) / v.size();
    double ss = 0;
    for (double x : v) ss += (x - mean) * (x - mean);
    const double med = pct(0.5);
    std::vector<double> dev(v.size());
    std::transform(v.begin(), v.end(), dev.begin(), [&](double x) { return std::fabs(x - med); });
    std::nth_element(dev.begin(), dev.begin() + dev.size() / 2, dev.end());
    return {v.front(), med, mean, std::sqrt(ss / (v.size() - 1)), dev[dev.size() / 2], pct(0.95)};
}

template <class F>
Stats bench(F&& fn, int warmup = 5, int reps = 31, int inner = 100) {
    for (int i = 0; i < warmup; ++i) fn();                      // caches, page faults, clocks, JIT/lazy init
    std::vector<double> us;
    for (int r = 0; r < reps; ++r) {
        auto t0 = std::chrono::steady_clock::now();             // monotonic, not system_clock
        for (int i = 0; i < inner; ++i) fn();                   // batch so timer resolution is negligible
        auto t1 = std::chrono::steady_clock::now();
        us.push_back(std::chrono::duration<double, std::micro>(t1 - t0).count() / inner);
    }
    return summarize(std::move(us));
}

int main() {
    std::vector<float> data(1 << 16, 1.0f);
    Stats s = bench([&] {
        float acc = 0;
        for (float x : data) acc += x;
        do_not_optimize(acc);
    });
    std::printf("min %.2f  median %.2f  mean %.2f  sd %.2f  MAD %.2f  p95 %.2f  (us/iter)\n",
                s.min, s.median, s.mean, s.stddev, s.mad, s.p95);
}
```

```text
min 28.78  median 28.82  mean 28.83  sd 0.03  MAD 0.02  p95 28.88  (us/iter)
```

65,536 serial float adds in 28.8 us is 0.44 ns per add. That is the **FP add latency** (a few cycles at about 5 GHz), not throughput, because `acc += x` is a loop-carried dependency the compiler may not reorder (Section 6.4). The harness tells you *what* the time is, and the roofline and latency reasoning tell you *why*.

Design choices to explain in an interview:

- **`steady_clock`**: monotonic. `system_clock` can jump (NTP). `high_resolution_clock` is often an alias of one of the two. For cycle-level work, `rdtsc`/`rdtscp` (invariant TSC) or `perf` counters.
- **Batching (`inner`)**: each sample covers about 3 ms, so the ~20-50 ns of timer overhead is negligible.
- **Many samples, robust summary**: report the median and a spread (MAD or IQR), not a single number.
- **`do_not_optimize`**: without it, `-O2` may delete the loop entirely, because `acc` is unused.

## 8.4 Statistics: Mean, Median, Variance, Confidence Intervals, Outliers

**Benchmark timings are not normally distributed.** They have a hard lower bound (the noise-free time) and a long right tail (interrupts, preemption, cache interference), and they are often **multimodal** (two code layouts, two frequency states).

| Statistic | Use it for | Caveat |
|---|---|---|
| **Minimum** | Deterministic CPU microbenchmarks: noise only adds time, so min estimates the noise-free cost | Optimistic; meaningless for latency SLOs or for code whose variance is real (allocation, I/O, contention) |
| **Median** | Default "typical" value; robust to outliers | Ignores the tail you may care about |
| **Mean** | Throughput and capacity planning (total time = n x mean); comparing totals | Dragged by outliers; needs many samples when the tail is heavy |
| **Stddev / CoV (sd/mean)** | Noise level; CoV above ~1-2% on a microbenchmark means the environment needs work | Inflated by outliers |
| **MAD / IQR** | Robust spread | Less familiar to audiences |
| **p95 / p99** | Latency-sensitive paths | Needs many samples (Section 1.3) |

**Confidence interval for the mean** (approximately valid for iid samples by the central limit theorem when n is moderately large):

```text
CI_95 = mean +- t_{0.975, n-1} x s / sqrt(n)

Example: n = 30 runs, mean = 10.00 ms, s = 0.40 ms, t_{0.975,29} = 2.045
         half-width = 2.045 x 0.40 / sqrt(30) = 0.149 ms   ->   [9.85, 10.15] ms
```

**How many runs?** To estimate the mean within `+-E` with about 95% confidence: `n ~= (1.96 sigma / E)^2`. With 2% run-to-run noise and a target of +-0.5%, `n ~= (1.96 x 2 / 0.5)^2 ~= 62` runs. **Halving the error needs 4x the runs**, so it is usually cheaper to reduce the noise (Section 8.2) than to add runs.

**When the iid assumption fails.** Thermal drift and background jobs make consecutive runs correlated. Run **A and B interleaved** (ABABAB... or randomized order) so drift affects both equally, and prefer a **bootstrap CI for the median** or for the ratio of medians, which makes no distributional assumption.

**Outliers.** Detect them with a robust rule such as the modified z-score `|0.6745 (x - median) / MAD| > 3.5`, or Tukey fences (`> Q3 + 1.5 IQR`). Then **investigate**: an outlier is data (a GC pause, a page-fault storm, preemption). Never silently drop outliers. Report how many there were and why. If the production system suffers them too, they belong in the result.

## 8.5 A/B Methodology

1. **Same everything except the change:** machine (ideally the same physical host), compiler and flags, inputs, data placement, and driver and firmware versions. Record all of them.
2. **Interleave runs** and use **fresh processes** for each run, so layout effects (ASLR) and between-process variance are sampled rather than frozen in.
3. **Enough repetitions** for the precision you need (8.4). Report an **effect size with a CI** ("B/A = 0.954, 95% CI [0.936, 0.971]"), not just "faster".
4. **Use a non-parametric test** if you need a p-value: Mann-Whitney U compares rank distributions and is robust to skew and outliers. Watch for multiple comparisons: test 20 benchmarks at p < 0.05 and expect one false positive.
5. **Practical significance:** decide a threshold up front (for example, ignore anything under 1%). A statistically significant 0.2% change may not matter, and a 0.2% change may also be a layout artifact.
6. **Check for layout bias** before believing a small win: rebuild with a different link order, or run with randomized stack and heap layouts. If the "win" flips sign, it was alignment luck.
7. **CI regression gating:** compare against a rolling baseline on a dedicated, quiet runner, with thresholds above the measured noise floor. Re-run suspected regressions before alerting, to keep false positives from eroding trust.

```python
"""ab_compare.py -- compare two sets of benchmark timings with robust statistics (stdlib only)."""
import random
import statistics as st


def bootstrap_ci(xs, stat=st.median, n_boot=10_000, alpha=0.05, seed=0):
    """Percentile-bootstrap confidence interval for any statistic (no normality assumption)."""
    rng = random.Random(seed)
    boots = sorted(stat(rng.choices(xs, k=len(xs))) for _ in range(n_boot))
    return boots[int(alpha / 2 * n_boot)], boots[int((1 - alpha / 2) * n_boot) - 1]


def ratio_ci(a, b, n_boot=10_000, alpha=0.05, seed=0):
    """CI for median(b) / median(a): 'how much faster/slower is B than A'."""
    rng = random.Random(seed)
    boots = sorted(st.median(rng.choices(b, k=len(b))) / st.median(rng.choices(a, k=len(a)))
                   for _ in range(n_boot))
    return boots[int(alpha / 2 * n_boot)], boots[int((1 - alpha / 2) * n_boot) - 1]


def mad_outliers(xs, k=3.5):
    """Modified z-score (Iglewicz-Hoaglin): flag |0.6745 (x - median) / MAD| > k. Report, don't silently drop."""
    med = st.median(xs)
    mad = st.median(abs(x - med) for x in xs) or 1e-12
    return [x for x in xs if abs(0.6745 * (x - med) / mad) > k]


if __name__ == "__main__":
    rng = random.Random(42)
    # Simulated timings (ms): right-skewed noise + rare large outliers, typical of real systems.
    base = [10.0 + rng.expovariate(1 / 0.3) + (25 if rng.random() < 0.03 else 0) for _ in range(40)]
    cand = [9.6 + rng.expovariate(1 / 0.3) + (25 if rng.random() < 0.03 else 0) for _ in range(40)]

    for name, xs in (("baseline", base), ("candidate", cand)):
        lo, hi = bootstrap_ci(xs)
        print(f"{name:9s} mean={st.mean(xs):6.2f} median={st.median(xs):6.2f} "
              f"95% CI(median)=[{lo:.2f}, {hi:.2f}] outliers={[round(x, 1) for x in mad_outliers(xs)]}")
    lo, hi = ratio_ci(base, cand)
    print(f"candidate/baseline median ratio 95% CI: [{lo:.3f}, {hi:.3f}]",
          "-> significant" if hi < 1 or lo > 1 else "-> not distinguishable from noise")
    try:
        from scipy.stats import mannwhitneyu      # optional: rank-based test, robust to outliers
        print("Mann-Whitney U p-value:", mannwhitneyu(base, cand, alternative="two-sided").pvalue)
    except ImportError:
        pass
```

```text
baseline  mean= 12.19 median= 10.27 95% CI(median)=[10.11, 10.45] outliers=[35.3, 35.2, 35.5, 11.4]
candidate mean=  9.95 median=  9.78 95% CI(median)=[9.70, 9.87] outliers=[11.4, 11.3, 10.7, 11.2]
candidate/baseline median ratio 95% CI: [0.936, 0.971] -> significant
```

The baseline's three 35 ms outliers inflate its mean by 19% (12.19 vs 10.27). Comparing means would report an 18% speedup, while the robust estimate is about 4.8% (CI 2.9-6.4%). This is the classic way a benchmark "win" comes from noise in the baseline run.

## 8.6 Google Benchmark

For C++ microbenchmarks, use a framework rather than a hand-rolled harness. Google Benchmark picks iteration counts automatically, provides `DoNotOptimize`/`ClobberMemory`, runs repetitions with aggregates, emits JSON, and ships a comparison tool. Full coverage (setup, fixtures, CI integration) is in [C++ Testing -- Microbenchmarking with Google Benchmark](../languages/CPP_Testing.md#43-microbenchmarking-with-google-benchmark).

```cpp
// fragment -- link with -lbenchmark -lpthread
#include <benchmark/benchmark.h>
#include <numeric>
#include <vector>

static void BM_Sum(benchmark::State& state) {
    std::vector<float> v(state.range(0), 1.0f);
    for (auto _ : state) {
        float s = std::accumulate(v.begin(), v.end(), 0.0f);
        benchmark::DoNotOptimize(s);           // value escapes: the loop cannot be deleted
    }
    state.SetBytesProcessed(state.iterations() * v.size() * sizeof(float));   // reports GB/s
}
BENCHMARK(BM_Sum)->RangeMultiplier(8)->Range(1 << 10, 1 << 24);   // L1 ... DRAM sizes
BENCHMARK_MAIN();
```

```bash
./bench --benchmark_repetitions=20 --benchmark_enable_random_interleaving=true \
        --benchmark_report_aggregates_only=true --benchmark_out=new.json --benchmark_out_format=json
# A/B with the bundled tool (prints time deltas and a Mann-Whitney U test across repetitions)
python3 benchmark/tools/compare.py benchmarks old.json new.json
```

If the library prints `***WARNING*** CPU scaling is enabled, the benchmark real time measurements may be noisy`, fix the governor (8.2) before trusting the numbers.

## 8.7 Timing GPUs

- **Launches are asynchronous.** `auto t0 = now(); kernel<<<...>>>(); auto t1 = now();` measures the **launch** (a few us), not the kernel. Either synchronize before reading the clock, or (better) use GPU events recorded on the same stream:

  ```cpp
  // fragment -- HIP (compile with hipcc)
  hipEvent_t start, stop;
  hipEventCreate(&start);
  hipEventCreate(&stop);
  for (int i = 0; i < 3; ++i) my_kernel<<<grid, block, 0, stream>>>(args);   // warm-up
  hipEventRecord(start, stream);
  for (int i = 0; i < iters; ++i) my_kernel<<<grid, block, 0, stream>>>(args);
  hipEventRecord(stop, stream);
  hipEventSynchronize(stop);
  float ms = 0;
  hipEventElapsedTime(&ms, start, stop);       // ms / iters = average per launch (includes gaps)
  ```

- **The first launch is special.** Code-object loading, lazy initialization of the runtime and context, and memory-pool growth happen on the first call. Always warm up.
- **Clocks ramp and vary.** An idle GPU runs at low clocks and ramps under load. Long runs hit power and thermal limits, so clocks drop. For low-variance comparisons, cap clocks: on AMD Instinct, `sudo amd-smi set --perf-determinism <SCLK_MHz>` (legacy `rocm-smi --setperfdeterminism`) caps GFXCLK. Support differs by product (AMD documents it as defeatured on MI350), so verify with `amd-smi metric`. On NVIDIA, `nvidia-smi --lock-gpu-clocks=<min>,<max>`, and note that Nsight Compute locks to **base** clocks by default (`--clock-control base`), so its durations are not directly comparable with unprofiled runs at boost clocks. Always report the clock policy.
- **Warm caches lie about bandwidth.** Re-running a kernel on the same 100 MB buffer on MI300X reads it from the 256 MB Infinity Cache, not HBM, and "achieves" more than 5.3 TB/s. For HBM numbers, use buffers several times larger than the last-level cache, or rotate through multiple buffers between iterations.
- **Measure what users see.** Kernel time excludes launch gaps, synchronization, and host overhead. For end-to-end numbers, time the whole step and look at a timeline trace (rocprofv3 or rocprof-sys, Perfetto, PyTorch profiler).
- **Multi-GPU:** time collectives at the slowest rank (Section 1.4), and barrier before starting the clock.

## 8.8 Profiler Overhead and the Observer Effect

Every measurement tool perturbs what it measures. Knowing how much, and in which direction, is part of the job of a profiling-tools engineer.

| Technique | How it perturbs | Typical magnitude and mitigation |
|---|---|---|
| **API tracing** (intercepting HIP/CUDA, MPI, or library calls) | Adds work per call, plus buffer flushes | Small for coarse calls, large for microsecond-scale launches; buffer asynchronously; report per-call overhead |
| **Hardware counter collection** | Limited counter registers mean many counters need **multiple passes** (replay of the kernel or of the whole application). Kernels are typically **serialized** so counters can be attributed, which removes overlap between concurrent kernels | Per-kernel durations become "isolated kernel" numbers, and total wall time can grow by several times. Combining passes assumes **deterministic** replays, so nondeterministic apps give inconsistent derived metrics. Collect only the counters you need |
| **Counter multiplexing (CPU `perf`)** | More events than counters means time-slicing, and counts are scaled estimates | `perf stat` shows the percentage of time each event was counted; keep event groups small for accuracy |
| **Sampling** (CPU `perf record`, GPU PC sampling) | Interrupts at the sampling rate; skid attributes samples to nearby instructions | Overhead scales with rate; statistical error scales with 1/sqrt(samples) |
| **Instrumentation** (compiler-inserted probes, manual timers, `-pg`) | Changes code size, inlining, and register allocation, so the measured binary is not the shipped one | Instrument coarse regions only; validate against an uninstrumented run |
| **Debug builds / sanitizers** | 2-20x slowdown, different code | Never benchmark them |

**How to quantify and report overhead:**

1. Run the application **with and without** the tool under identical conditions (both with warm-up and repetitions). Overhead = `(T_profiled - T_base) / T_base`, reported with its variance.
2. Microbenchmark the per-event cost: for example, 100k empty kernel launches with and without tracing gives the added cost per launch.
3. Check **perturbation of the result**, not just the slowdown. Does the kernel time distribution under counter collection match unprofiled event timing? Does serialization change which kernel dominates?
4. Document it: "Counter collection runs N passes; kernel durations are measured in serialized mode; expect X% overhead for tracing."

> **See also:** [C++ Testing -- Microbenchmarking with Google Benchmark](../languages/CPP_Testing.md#43-microbenchmarking-with-google-benchmark) for Google Benchmark and test infrastructure; [Debugging and Profiling Tools](../tools/Debugging_and_Profiling_Tools.md) for `perf`, rocprofv3, rocprof-sys, and uProf/VTune; [Containers and CI](../tools/Containers_and_CI.md) for perf regression gating; [Project Deep Dive: rocprof-compute](../career/Project_Deep_Dive_rocprof-compute.md).

## 8.9 Interview Questions

**Q1.** You benchmark a change: baseline 100 ms, new version 95 ms, one run each. Is it faster?

You cannot tell. One sample per side says nothing about noise. Typical run-to-run variance on a shared machine is 1-5%, and layout effects alone can move results by several percent. Do: warm up; take 20-30+ interleaved runs of each in fresh processes; pin CPUs and fix the frequency; report the median with a bootstrap CI on the ratio (or a Mann-Whitney U test); check that the CI excludes 1.0 and that the effect exceeds a practical threshold. If the effect is small, confirm it survives a rebuild with a different link order.

**Q2.** Mean, median, or minimum: which do you report?

It depends on the question. For a deterministic CPU microbenchmark, the **minimum** approximates the noise-free cost (noise only adds time), and the median is a robust "typical". For user-facing latency, report the **median and tail percentiles**. For throughput and capacity planning, the **mean** matters because total time = n x mean. In every case, report a spread (IQR or MAD, or a CI), the sample count, and the environment. Never a single number.

**Q3.** How does CPU frequency scaling corrupt a benchmark, and what do you do about it?

Turbo or boost frequency depends on how many cores are active, on temperature, and on power, so the same code can run 20-50% faster or slower between runs, or even within a run (the first iterations at low clock, then thermal throttling). A/B comparisons become comparisons of thermal states. Fixes: the `performance` governor; disabling boost for A/B work; pinning; letting the machine reach a steady state; interleaving A/B; and reporting cycles (`perf stat`) as well as time. For the GPU equivalent, cap clocks (`amd-smi set --perf-determinism`, `nvidia-smi --lock-gpu-clocks`) or at least record clocks during the run.

**Q4.** Why might a profiler report different kernel durations from your application's own timing?

(1) **Serialization:** counter collection usually serializes kernels, so overlap disappears and each kernel runs alone, often slightly faster (no contention) or slower (no overlap). (2) **Replay:** with multi-pass collection, the reported time may come from one pass; cache state differs between passes. (3) **Clock control:** some profilers lock clocks to base frequency. (4) **Overhead** added around launches by tracing. (5) **Measurement boundaries:** the profiler times GPU execution, while app timers often include launch latency and queueing. Validate with GPU events in an unprofiled run, and document which mode produced each number.

**Q5.** A benchmark of `std::accumulate` reports 0.3 ns for summing a million floats. What happened?

The compiler removed the work. The result was unused, so the loop was dead code. Or the input was a compile-time constant and the sum was folded. A million floats cannot be read in 0.3 ns: that would be 13 PB/s. Fix: consume the result (`benchmark::DoNotOptimize`, an `asm volatile` escape, or print it), and make the inputs opaque to the optimizer. Then sanity-check the result against the roofline: 4 MB per call at about 50 GB/s single-core bandwidth means about 80 us when the data comes from DRAM.

**Q6.** How many repetitions do you need?

Enough that the CI on the quantity you care about is narrower than the effect you want to detect. For means: `n ~= (1.96 sigma / E)^2`. With 2% noise and a resolution target of +-0.5%, that is about 62 runs. Reducing sigma (pinning, frequency control, quiet machine) is quadratically cheaper than adding runs. For tail percentiles, you need about `10/(1-p)` samples (10k for p99.9).

---

# 9. Floating-Point Numerics and Reproducibility

---

Performance work constantly reorders arithmetic: vectorization, parallel reductions, tiling, FMA, and lower precision. Every reordering changes floating-point results. You need to know **why**, **how much**, and **what to do about it**, both to validate optimizations and to explain to a user why the "same" GPU computation gives different bits on two runs. The IEEE 754 format itself is covered in [CS Fundamentals -- Endianness and Floating Point](./CS_Fundamentals.md#79-endianness-and-floating-point).

## 9.1 Precision Cheat Sheet

| Format | Significand bits (incl. implicit) | Machine epsilon (2^-(p-1)) | ~Decimal digits | Max finite | Where used |
|---|---|---|---|---|---|
| FP64 | 53 | 2.2e-16 | 15.9 | 1.8e308 | HPC, reference results |
| FP32 | 24 | 1.2e-7 | 7.2 | 3.4e38 | Default GPU compute, accumulators |
| TF32 | 11 | 9.8e-4 | 3.3 | 3.4e38 | Matrix-unit input format |
| FP16 | 11 | 9.8e-4 | 3.3 | 65504 | Inference, mixed precision (needs loss scaling) |
| BF16 | 8 | 7.8e-3 | 2.4 | 3.4e38 | Training (FP32 range, low precision) |
| FP8 E4M3 / E5M2 | 4 / 3 | 0.125 / 0.25 | ~1 | 448 / 57344 (OCP); MI300's FNUZ E4M3 variant: 240 | Inference and training GEMMs with per-tensor or per-block scaling |

Useful facts:

- **Unit roundoff** `u = eps/2`. Each correctly rounded operation satisfies `fl(a op b) = (a op b)(1 + delta)` with `|delta| <= u`.
- **Consecutive integers** are exact up to `2^24 = 16,777,216` in FP32 and `2^53` in FP64. In FP32, `16777216.0f + 1.0f == 16777216.0f`. A float counter silently stops incrementing there.
- **0.1 is not representable** in binary, so `0.1 + 0.2 != 0.3` in double. The sum is `0.30000000000000004`.

## 9.2 Non-Associativity

Each operation rounds, so `(a + b) + c` and `a + (b + c)` round at different points:

```text
a = 1e16, b = -1e16, c = 1.0   (double)
(a + b) + c = 0 + 1         = 1.0
a + (b + c) = 1e16 + (-1e16) = 0.0       (-1e16 + 1 rounds back to -1e16: ulp(1e16) = 2)
```

So **any change in evaluation order can change the result**: vectorization (lane-wise partial sums), loop tiling, thread count, OpenMP or MPI reduction order, GPU block scheduling and atomics, compiler reassociation under `-ffast-math`, and library algorithm choice (split-K GEMM, different BLAS kernels per matrix shape). Multiplication is not associative either, and distributivity fails too.

## 9.3 Catastrophic Cancellation

Subtracting two nearly equal numbers cancels their leading digits. The result is exact relative to the operands, but the operands' **previous rounding errors** are now large relative to the small difference.

```text
relative error of (x - y) is roughly  u x (|x| + |y|) / |x - y|      <- amplification factor
```

```python
"""cancel.py -- catastrophic cancellation and how to avoid it."""
import math

import numpy as np

# 1) Rewriting the formula: (1 - cos x) / x^2 -> 0.5 as x -> 0
for x in (1e-4, 1e-6, 1e-8):
    naive = (1 - math.cos(x)) / x**2
    stable = 2 * math.sin(x / 2) ** 2 / x**2          # same identity, no subtraction of near-equals
    print(f"x={x:.0e}  naive={naive:.10f}  stable={stable:.10f}")

# 2) Variance: E[x^2] - E[x]^2 subtracts two huge, nearly equal numbers
data = np.float32(1e4) + np.random.default_rng(0).standard_normal(100_000).astype(np.float32)
mean = data.mean(dtype=np.float32)
one_pass = (data * data).mean(dtype=np.float32) - mean * mean
two_pass = ((data - mean) ** 2).mean(dtype=np.float32)


def welford(xs):
    """Single pass AND numerically stable (streaming-friendly)."""
    n, m, m2 = 0, 0.0, 0.0
    for x in xs:
        n += 1
        d = x - m
        m += d / n
        m2 += d * (x - m)
    return m2 / n


print(f"true var ~ 1.0   one-pass={one_pass:.4f}   two-pass={two_pass:.4f}   welford={welford(data.tolist()):.4f}")

# 3) Comparing floats
print(math.isclose(0.1 + 0.2, 0.3), math.isclose(1e-9, 0.0),
      math.isclose(1e-9, 0.0, abs_tol=1e-8), bool(np.isclose(1e-9, 0.0)))  # True False True True
```

```text
x=1e-04  naive=0.4999999970  stable=0.4999999996
x=1e-06  naive=0.5000444503  stable=0.5000000000
x=1e-08  naive=0.0000000000  stable=0.5000000000
true var ~ 1.0   one-pass=-8.0000   two-pass=1.0003   welford=1.0003
True False True True
```

The one-pass "textbook" variance formula gives a **negative variance** in FP32: `E[x^2] ~= 1e8`, where the FP32 ulp is 8, so the true answer (1.0) is below the rounding noise. Remedies: algebraic rewrites (`1 - cos x = 2 sin^2(x/2)`, `sqrt(x+1) - sqrt(x) = 1/(sqrt(x+1) + sqrt(x))`, the stable quadratic formula), shifting data by an estimate of the mean, Welford's online algorithm, and higher-precision accumulation. The same issue appears in LayerNorm/BatchNorm kernels and in profiler metrics computed as differences of large counters (sample timestamps or cumulative counters close together).

## 9.4 Compensated and Pairwise Summation

**Error bounds** for summing `n` numbers (to first order; `u` = unit roundoff):

| Algorithm | Worst-case error bound | Cost |
|---|---|---|
| Naive recursive | `(n - 1) u sum|x_i|` | 1 add per element |
| Pairwise (tree) | `~ u log2(n) sum|x_i|` | Same adds; natural for parallel and GPU reductions |
| Kahan (compensated) | `~ 2u sum|x_i| + O(n u^2)`: independent of n to first order | 4 flops per element |
| Neumaier (improved Kahan) | Same, and also handles `|x_i| > |s|` | ~4 flops + a compare |
| Higher-precision accumulator (FP32 data, FP64 sum) | Error of the wider type, then one rounding | Often free when memory-bound |

The **condition number** of a sum is `kappa = sum|x_i| / |sum x_i|`. Relative error is about `kappa x (bound / sum|x_i|)`. Sums with heavy cancellation (`kappa` large) are inherently sensitive, however careful the algorithm.

```cpp
// fp_sum.cpp -- non-associativity, naive vs pairwise vs Kahan vs Neumaier summation, ULP compare
// g++ -std=c++20 -O2 fp_sum.cpp -o fp_sum && ./fp_sum      (do NOT add -ffast-math: it deletes Kahan)
#include <bit>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <random>
#include <vector>

float naive_sum(const std::vector<float>& v) {
    float s = 0.0f;
    for (float x : v) s += x;
    return s;
}

// Pairwise (cascade) summation: error grows O(eps * log n) instead of O(eps * n).
float pairwise_sum(const float* p, std::size_t n) {
    if (n <= 8) { float s = 0; for (std::size_t i = 0; i < n; ++i) s += p[i]; return s; }
    const std::size_t h = n / 2;
    return pairwise_sum(p, h) + pairwise_sum(p + h, n - h);
}

// Kahan: carry the low-order bits lost in each addition in a compensation term c.
float kahan_sum(const std::vector<float>& v) {
    float s = 0.0f, c = 0.0f;
    for (float x : v) {
        float y = x - c;        // apply the correction from the previous step
        float t = s + y;        // big + small: low bits of y are lost here...
        c = (t - s) - y;        // ...and recovered here (algebraically 0, numerically the error)
        s = t;
    }
    return s;
}

// Neumaier: Kahan variant that is also correct when |x| > |s| (e.g. 1, 1e8, 1, -1e8).
float neumaier_sum(const std::vector<float>& v) {
    float s = 0.0f, c = 0.0f;
    for (float x : v) {
        float t = s + x;
        c += (std::fabs(s) >= std::fabs(x)) ? (s - t) + x : (x - t) + s;
        s = t;
    }
    return s + c;
}

// Distance in units-in-the-last-place between two finite floats of any sign.
std::int64_t ulp_distance(float a, float b) {
    auto key = [](float f) {                     // map to a monotonic integer line
        std::int32_t i = std::bit_cast<std::int32_t>(f);
        return i < 0 ? std::int64_t{INT32_MIN} - i : std::int64_t{i};
    };
    return std::llabs(key(a) - key(b));
}

bool almost_equal(double a, double b, double rtol = 1e-6, double atol = 1e-12) {
    return std::fabs(a - b) <= atol + rtol * std::fmax(std::fabs(a), std::fabs(b));   // symmetric
}

int main() {
    // 1) Non-associativity
    double a = 1e16, b = -1e16, c = 1.0;
    std::printf("(a+b)+c = %.1f   a+(b+c) = %.1f\n", (a + b) + c, a + (b + c));
    std::printf("0.1+0.2 == 0.3 ? %s  (0.1+0.2 = %.17g)\n", (0.1 + 0.2 == 0.3) ? "yes" : "no", 0.1 + 0.2);

    // 2) Summing 10M values of 0.1f: exact answer computed in double
    std::vector<float> v(10'000'000, 0.1f);
    double exact = 10'000'000.0 * static_cast<double>(0.1f);
    std::printf("exact     %.4f\n", exact);
    std::printf("naive     %.4f\n", naive_sum(v));
    std::printf("pairwise  %.4f\n", pairwise_sum(v.data(), v.size()));
    std::printf("kahan     %.4f\n", kahan_sum(v));
    std::printf("neumaier  %.4f\n", neumaier_sum(std::vector<float>{1.0f, 1e8f, 1.0f, -1e8f}));
    std::printf("kahan     %.4f  (same 4 values; plain Kahan loses both 1s)\n",
                kahan_sum(std::vector<float>{1.0f, 1e8f, 1.0f, -1e8f}));

    // 3) Order dependence: the same multiset summed in a different order gives a different float
    std::mt19937 rng(7);
    std::uniform_real_distribution<float> d(-1.0f, 1.0f);
    std::vector<float> w(1'000'000);
    for (auto& x : w) x = d(rng) * std::pow(10.0f, d(rng) * 6);
    float fwd = naive_sum(w);
    std::vector<float> rev(w.rbegin(), w.rend());
    float bwd = naive_sum(rev);
    std::printf("forward %.6g  reverse %.6g  ulp distance %lld  almost_equal(1e-5)=%d\n",
                fwd, bwd, static_cast<long long>(ulp_distance(fwd, bwd)), almost_equal(fwd, bwd, 1e-5));
    std::printf("ulp(1.0f, nextafter) = %lld, ulp(-0.0f, +0.0f) = %lld\n",
                static_cast<long long>(ulp_distance(1.0f, std::nextafter(1.0f, 2.0f))),
                static_cast<long long>(ulp_distance(-0.0f, 0.0f)));
}
```

```text
(a+b)+c = 1.0   a+(b+c) = 0.0
0.1+0.2 == 0.3 ? no  (0.1+0.2 = 0.30000000000000004)
exact     1000000.0149
naive     1087937.0000
pairwise  1000000.0000
kahan     1000000.0000
neumaier  2.0000
kahan     0.0000  (same 4 values; plain Kahan loses both 1s)
forward -2.18852e+07  reverse -2.18865e+07  ulp distance 646  almost_equal(1e-5)=0
ulp(1.0f, nextafter) = 1, ulp(-0.0f, +0.0f) = 0
```

What this shows:

- **Naive FP32 summation of 10M copies of `0.1f` is 8.8% off.** Once the running sum is large, its ulp is 0.0625-0.125, so each `+= 0.1f` is rounded to a multiple of that ulp, and the error is **systematic** (the same direction every step), so it grows linearly with n. Pairwise and Kahan are both essentially exact here.
- **Plain Kahan fails on `{1, 1e8, 1, -1e8}`** because the compensation assumes `|s| >= |x|`. Neumaier handles it.
- **Reversing the order of 1M mixed-magnitude floats changed the result by 646 ulps** (relative 6e-5), which is enough to fail a naive `rtol = 1e-5` check. Tolerances must scale with `n` and `kappa`.
- **`-ffast-math` silently breaks Kahan.** With reassociation allowed, the compiler simplifies `c = (t - s) - y` to 0. Rebuilt with `-ffast-math`, this program printed the same wrong value (975599.1) for both naive and Kahan. If you need compensated summation, do not use fast-math for that translation unit, or use `-fno-associative-math` / `#pragma float_control` / `volatile` barriers.

## 9.5 Why Parallel and GPU Reductions Are Non-Deterministic

| Cause | Mechanism |
|---|---|
| **Thread count and partitioning** | `reduction(+:s)` gives each thread a partial sum over a different slice; different thread counts give different trees |
| **Combine order** | OpenMP leaves the order in which partial sums are combined unspecified; MPI_Reduce may use different algorithms (tree, ring) by message size and process count |
| **Floating-point atomics** | `atomicAdd(&sum, x)` from thousands of GPU threads applies the additions in **arrival order**, which depends on scheduling, clocks, and contention, so it differs run to run even with identical inputs |
| **Dynamic scheduling** | Work stealing or `schedule(dynamic)` assigns chunks by timing |
| **Library heuristics** | BLAS/DNN libraries pick kernels by shape, workspace, and hardware: split-K GEMM (partial sums over K, then reduced, possibly atomically), autotuned convolution algorithms |
| **Different hardware or build** | Vector width, FMA contraction, different `libm` implementations (transcendentals are not required to be correctly rounded), GPU architecture |

Demonstration with OpenMP, compared against two reproducible alternatives:

```cpp
// repro.cpp -- parallel float reductions depend on thread count; two reproducible alternatives
// g++ -std=c++20 -O2 -fopenmp repro.cpp -o repro && ./repro
#include <omp.h>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <random>
#include <vector>

float omp_sum(const std::vector<float>& v, int threads) {
    float s = 0.0f;
#pragma omp parallel for reduction(+ : s) num_threads(threads) schedule(static)
    for (long i = 0; i < static_cast<long>(v.size()); ++i) s += v[i];
    return s;   // partial sums are combined in an unspecified order and partition depends on threads
}

// (a) Fixed decomposition: always 256 chunks, combined in index order -> same bits for any thread count.
float fixed_tree_sum(const std::vector<float>& v, int threads) {
    constexpr int kChunks = 256;
    std::vector<double> partial(kChunks, 0.0);
    const long n = static_cast<long>(v.size());
#pragma omp parallel for num_threads(threads) schedule(dynamic)
    for (int c = 0; c < kChunks; ++c)
        for (long i = n * c / kChunks; i < n * (c + 1) / kChunks; ++i) partial[c] += v[i];
    double s = 0;
    for (double p : partial) s += p;      // serial, fixed order
    return static_cast<float>(s);
}

// (b) Integer (fixed-point) accumulation: integer addition IS associative, so any order gives the
//     same bits. Requires a known range; here 2^-24 resolution with a 64-bit accumulator.
float fixed_point_sum(const std::vector<float>& v, int threads) {
    constexpr double kScale = 1 << 24;
    std::int64_t acc = 0;
#pragma omp parallel for reduction(+ : acc) num_threads(threads)
    for (long i = 0; i < static_cast<long>(v.size()); ++i) acc += std::llround(v[i] * kScale);
    return static_cast<float>(acc / kScale);
}

int main() {
    std::mt19937 rng(3);
    std::uniform_real_distribution<float> d(-1.0f, 1.0f);
    std::vector<float> v(10'000'000);
    for (auto& x : v) x = d(rng);
    std::printf("threads   omp reduction     fixed tree        fixed point\n");
    for (int t : {1, 2, 3, 8, 64})
        std::printf("%7d   %.9g   %.9g   %.9g\n", t, omp_sum(v, t), fixed_tree_sum(v, t), fixed_point_sum(v, t));
}
```

```text
threads   omp reduction     fixed tree        fixed point
      1   1782.38147   1782.37134   1782.37134
      2   1782.39673   1782.37134   1782.37134
      3   1782.36719   1782.37134   1782.37134
      8   1782.36426   1782.37134   1782.37134
     64   1782.38257   1782.37134   1782.37134
```

The plain OpenMP reduction gives a different answer for every thread count, all wrong in the 5th-6th significant digit (FP32 accumulation of 10M values). The fixed-decomposition version **decouples the arithmetic order from the thread count**: the chunks are dynamically scheduled, but each chunk's sum and the final combine order are fixed. It also accumulates in FP64. The fixed-point version relies on integer associativity. The two agree here because both happen to be accurate to FP32 precision.

## 9.6 Reproducibility Strategies

| Strategy | How | Cost |
|---|---|---|
| **Fixed reduction order** | Decompose the work independently of the thread or block count; combine in a fixed tree; two-pass GPU reductions (per-block partials to a buffer, then one deterministic final pass) instead of float atomics | Extra pass or buffer; may limit load balancing |
| **Deterministic library modes** | PyTorch `torch.use_deterministic_algorithms(True)` (raises an error on ops without a deterministic implementation), `torch.backends.cudnn.deterministic = True` (also used for MIOpen on ROCm builds); fixed seeds; pinned library versions | Some ops slower or unavailable |
| **Integer / fixed-point accumulation** | Scale to integers, accumulate in int64 (associative), convert back | Needs a known dynamic range |
| **Reproducible summation algorithms** | Binned or pre-rounded summation (ReproBLAS-style) that gives bitwise identical results for any order | ~2-4x the cost of a plain sum |
| **Higher-precision accumulation** | FP32 accumulators for FP16/BF16 data (matrix cores do this), FP64 for FP32 | Smaller differences, but not deterministic by itself |
| **Pin the environment** | Same binary, `-ffp-contract=off` or a fixed `-march`, no `-ffast-math`, same thread and GPU counts, same library versions | Portability limits |
| **Accept and test with tolerances** | Validate against a high-precision reference with tolerances justified by an error analysis | Requires reasoning about kappa and n |

**Practical stance:** bitwise reproducibility across hardware is rarely worth its cost. **Run-to-run** reproducibility on fixed hardware and configuration is often required (debugging, regression tests, regulated domains) and is achievable. Everything else should be validated with tolerances.

## 9.7 Comparing Floats: ULP, rtol, atol

Never use `==` on computed floats (except deliberately, for bitwise-reproducibility tests). Three styles:

| Method | Test | Good for | Fails for |
|---|---|---|---|
| **Absolute** | `|a - b| <= atol` | Values near zero, known absolute scale | Large magnitudes (too strict) or tiny ones (too loose) |
| **Relative** | `|a - b| <= rtol x max(|a|, |b|)` | Most values | Near zero: the relative error blows up |
| **Combined** | `|a - b| <= atol + rtol x max(|a|, |b|)` | General default | Need to choose both |
| **ULP distance** | Number of representable floats between a and b | Library and math-function testing ("within 4 ulp") | Near zero across signs, and after cancellation (few ulps of a tiny result is meaningless) |

Library defaults to know:

| API | Rule | Defaults |
|---|---|---|
| Python `math.isclose(a, b)` | `|a-b| <= max(rel_tol x max(|a|,|b|), abs_tol)` (symmetric) | `rel_tol=1e-9`, `abs_tol=0.0`, so `isclose(1e-9, 0.0)` is **False** |
| `numpy.isclose(a, b)` / `allclose` | `|a-b| <= atol + rtol x |b|` (**asymmetric**: `b` is the reference) | `rtol=1e-5`, `atol=1e-8`, so `isclose(1e-9, 0.0)` is **True** |
| `torch.testing.assert_close` | Combined, with defaults chosen per dtype | FP32: `rtol=1.3e-6, atol=1e-5`; FP16: `rtol=1e-3, atol=1e-5`; BF16: `rtol=1.6e-2, atol=1e-5` |
| GoogleTest `EXPECT_FLOAT_EQ` / `EXPECT_DOUBLE_EQ` | Within **4 ULPs** | -- |
| GoogleTest `EXPECT_NEAR(a, b, abs_error)` | Absolute | -- |

**Choosing tolerances from first principles.** For a length-`n` FP32 dot product compared with an FP64 reference, the error bound is about `n u x sum|x_i y_i|`. For `n = 4096` and `u = 6e-8`, that is `~2.4e-4 x sum|x_i y_i|`, so `rtol ~1e-4` relative to the absolute-value sum (not to the result, if there is cancellation). For FP16 inputs with FP32 accumulation, the input rounding dominates (`u_fp16 ~= 4.9e-4`). Always handle NaN explicitly (`NaN != NaN`; numpy has `equal_nan`), and decide whether `-0.0 == +0.0` matters (it compares equal, but `1/x` differs).

> **See also:** [C++ Testing -- Floating-Point Assertions](../languages/CPP_Testing.md#54-floating-point-assertions); [ML Frameworks -- Mixed Precision Training](../ml-gpu/ML_AI_Frameworks.md#82-mixed-precision-training); [Parallel GPU Programming -- Atomic Operations](../ml-gpu/Parallel_GPU_Programming.md#213-atomic-operations) and [Reduction Clause](../ml-gpu/Parallel_GPU_Programming.md#112-reduction-clause); [LLM and ML Fundamentals](../ml-gpu/LLM_and_ML_Fundamentals.md) for low-precision formats.

## 9.8 Denormals, FMA Contraction, and fast-math

- **Denormals (subnormals)** are values below the smallest normal (`~1.18e-38` in FP32). They provide gradual underflow. On many CPUs, operations that produce or consume them take a slow microcode-assisted path (historically 10-100x slower per operation). Setting **FTZ/DAZ** (flush-to-zero, denormals-are-zero; MXCSR bits on x86) removes the cliff and changes results near zero. GCC's `-ffast-math` at link time adds startup code (`crtfastmath.o`) that sets FTZ/DAZ **for the whole process**, including code not compiled with fast-math. GPU compilers expose separate denormal-mode controls per precision (for example, HIP-Clang's `-fgpu-flush-denormals-to-zero`).
- **FMA contraction:** `a*b + c` can be fused into one FMA (one rounding instead of two). It is more accurate, but **different**. Verified with GCC 15: even with `-std=c++20`, GCC contracts by default when the target has FMA (`-ffp-contract=fast` is the default except in ISO C modes), so building the same source with `-march=x86-64` vs `-march=x86-64-v3` can change results. Clang's default for C/C++ is `-ffp-contract=on` (fuse within a single expression). Pin `-ffp-contract=off` when you need cross-build reproducibility.
- **`-ffast-math`** = `-fassociative-math`, `-freciprocal-math`, `-ffinite-math-only`, `-fno-signed-zeros`, `-fno-trapping-math`, `-fno-math-errno`, and more. Consequences: reassociation (vectorized reductions, but results differ); `x != x` NaN checks may be optimized away (`isnan` can stop working); compensated summation breaks; FTZ is set process-wide. Prefer enabling the narrow flag you need, or local pragmas, over global fast-math.

## 9.9 Interview Questions

**Q1.** Why can a GPU reduction give different results on two runs with the same input?

FP addition is not associative, so the result depends on the order of operations. On a GPU, the order varies when the reduction uses floating-point **atomics** (the order of `atomicAdd`s depends on which workgroup finishes first, which depends on scheduling, clocks, and contention); when the number of workgroups or the split depends on hardware or occupancy; or when a library's heuristics pick different kernels (split-K GEMM, autotuned algorithms). Fixes: a two-pass reduction (per-block partials stored to memory, then a fixed-order final reduction), deterministic library modes, integer or fixed-point accumulation, or reproducible summation algorithms. Each costs some performance.

**Q2.** Implement and explain Kahan summation. When does it fail?

Keep a running compensation `c`: `y = x - c; t = s + y; c = (t - s) - y; s = t;`. `(t - s)` recovers the part of `y` that actually made it into `s`, so `(t - s) - y` is the negated lost low-order part, which is subtracted from the next input. The error bound becomes about `2u sum|x_i|`, independent of `n` to first order. It fails or degrades when (1) `|x| > |s|` (use Neumaier's variant); (2) the compiler is allowed to reassociate (`-ffast-math` simplifies `c` to 0); (3) extended-precision intermediate registers (x87) are used inconsistently. It is also inherently sequential. In parallel, use per-thread Kahan plus a compensated combine, or pairwise summation.

**Q3.** How do you compare floating-point results in tests?

With a combined tolerance `|a - b| <= atol + rtol x max(|a|, |b|)`, where `rtol` is justified by the algorithm's error bound (about `n u` for sums or dot products, scaled by the condition number) and `atol` handles values near zero. ULP-based comparison (GoogleTest's 4 ULPs) suits elementwise math functions, not long reductions. Know the library semantics: `numpy.isclose` is asymmetric with `atol=1e-8` (so `1e-9 ~ 0` passes), while `math.isclose` defaults to `abs_tol=0` (so it fails). Compare against a higher-precision reference rather than another low-precision run, handle NaN and Inf explicitly, and for nondeterministic kernels, test against the tolerance rather than bitwise equality.

**Q4.** What is catastrophic cancellation? Give an example from ML kernels.

Subtracting nearly equal numbers removes the leading matching digits, so earlier rounding errors dominate the result. Example: computing variance as `E[x^2] - E[x]^2` in FP32 for activations with a large mean. The two terms are about `1e8` and agree in all their significant digits, so the difference (the variance) is noise and can even be negative (shown above: -8.0 instead of 1.0). This matters for LayerNorm and BatchNorm, so implementations use Welford's algorithm or a two-pass mean-then-variance with FP32 accumulation. Another example is softmax without max-subtraction, which is an overflow problem rather than cancellation, and is solved by subtracting the row max.

**Q5.** Your optimized kernel's output differs from the reference by 1e-6 relative. Bug or not?

Possibly neither. Estimate the expected error first. For an FP32 reduction of length `n`, the bound is about `n u kappa`. With `n = 1e4`, that is up to about `6e-4 kappa`, so a 1e-6 difference is well within the noise of reordering. Check: (1) does the difference scale with `n` and with the condition number as theory predicts? (2) Compare both versions against an FP64 reference: is the new one *less* accurate, or just different? (3) Test adversarial inputs (large dynamic range, cancellation, denormals, NaN or Inf propagation). A real bug usually shows errors far above the bound, or on specific indices (boundary tiles, tails).

**Q6.** Why is a float counter dangerous?

FP32 represents consecutive integers exactly only up to `2^24 = 16,777,216`. Past that, `x + 1.0f == x`, so a float counter or accumulator silently stops increasing (more generally, small increments to large sums get rounded away; see the 0.1f example). Use integer counters, FP64, or compensated or pairwise accumulation for long-running sums such as profiler metrics, loss averages, and timers.

---

# 10. Interview Q&A

---

These questions combine several sections. They are the kind of open-ended performance questions asked in GPU/HPC, ML-infra, and systems loops.

**Q1.** Walk me through how you would find out why a GPU application is slow.

Work top-down, and measure before forming theories. (1) **Whole application:** wall-clock time and a timeline trace (rocprofv3 or rocprof-sys, PyTorch profiler, Perfetto). What fraction is GPU kernels, copies, host code, idle gaps, and synchronization? Amdahl says to optimize the biggest slice, and the slice is often not a kernel: it may be launch gaps, host-to-device copies, or a CPU-side data loader. (2) **Top kernels by total time:** for each, compute achieved FLOP/s and bytes/s and place it on the roofline (`rocprof-compute profile --roof-only`, then `analyze`). (3) **Classify:** near the memory roof means reduce bytes (fuse, tile, lower precision); near the compute roof means better instructions (MFMA, lower precision) or less work; far below both means latency-bound (occupancy, dependent loads, too few bytes in flight), launch-bound, or imbalanced (tail effect). (4) **Counters for the hypothesis:** cache hit rates, LDS bank conflicts, VALU/MFMA utilization, occupancy limiters (VGPRs, LDS), wave stalls. (5) **Fix one thing, then re-measure** with proper repetitions (Section 8). Stop when you reach the roof that applies or when the slice no longer dominates.

**Q2.** An FP16 GEMM with M = N = K = 4096 takes 200 us on MI300X. How good is that?

FLOPs = `2 x 4096^3 = 137.4 GFLOP`, so achieved = `137.4e9 / 200e-6 = 687 TFLOP/s`, which is **52.6%** of the 1307.4 TFLOP/s dense FP16 peak. The AI is about `n/3 = 1365 FLOP/B`, far above the 247 FLOP/B ridge point, so the kernel should be compute-bound and has headroom. Suspects: (1) **wave quantization:** 256 x 256 output tiles give `16 x 16 = 256` workgroups on 304 CUs, so 48 CUs (16%) sit idle for the whole kernel. Smaller tiles, stream-K, or split-K would fix that. (2) Clocks under load below the 2,100 MHz peak engine clock assumed by the spec. (3) MFMA pipeline bubbles from LDS bank conflicts or insufficient software pipelining of global-to-LDS loads. (4) Epilogue cost. Compare against hipBLASLt for the same shape, and look at MFMA utilization counters.

**Q3.** You need to sum 1e9 floats. Estimate the time on one CPU core, on a whole CPU socket, and on an MI300X.

Data = 4 GB. **One core:** if the loop is a serial `float` sum, it is latency-bound at about 0.4 ns per add (the measured harness in 8.3), so about 400 ms. Vectorized with several accumulators, it becomes bandwidth-bound at about 20-50 GB/s for a single core, so 80-200 ms. **Whole socket** (about 460 GB/s): about 9 ms if parallelized with NUMA-aware placement. **MI300X** (5.3 TB/s): about 0.75 ms, **but** if the data starts in host memory, copying 4 GB over PCIe Gen5 x16 (about 64 GB/s theoretical per direction, around 50 GB/s achievable) takes about 80 ms. Offloading only pays if the data already lives on the GPU or will be reused there. This combines Amdahl (transfers are the serial part), the roofline (AI = 0.25 FLOP/B, so memory-bound everywhere), and latency vs throughput (the dependency chain).

**Q4.** Adding threads made the program slower. List the causes you would investigate.

(1) **False sharing** on per-thread counters or adjacent array elements (check `perf c2c`). (2) **Lock contention** or a single hot atomic, where the critical section's serialized throughput is the limit and contention adds cache-line ping-pong. (3) **Memory bandwidth saturation:** more threads add queueing, not throughput (Little's law), and the per-thread working sets now overflow the shared L3. (4) **NUMA:** threads spill onto the second socket, but the data was first-touched on socket 0. (5) **Oversubscription:** more threads than cores, so context switches and spinning locks waste time; nested parallelism (OpenMP inside TBB, or BLAS threads inside your threads). (6) **Frequency:** all-core turbo is lower than single-core turbo. (7) **SMT siblings** competing for one core's execution units. (8) **Load imbalance** combined with barriers. Measure: scaling curve, `perf stat` (IPC, cache misses), `perf c2c`, lock profilers, `numastat`.

**Q5.** Why does a GPU tolerate memory latency better than a CPU, even though its DRAM latency is higher?

Little's law: bandwidth = bytes in flight / latency. A CPU core keeps a few dozen cache misses in flight (fill buffers plus prefetchers) and relies on caches and out-of-order execution to avoid stalls. A GPU keeps tens of thousands of memory requests in flight by holding many waves resident per CU and switching to a ready wave at zero cost whenever one stalls. Higher latency is fine as long as `occupancy x per-wave outstanding bytes` covers `bandwidth x latency` (about 3 MB on MI300X). When occupancy is too low (too many VGPRs or too much LDS per workgroup) or each thread issues dependent loads, the GPU becomes latency-bound and the high latency shows.

**Q6.** In LLM serving, why does increasing the decode batch size raise throughput almost for free, up to a point?

In decode, each step reads all the weights to produce one token per sequence. With batch B, the weight bytes are read once and used for B tokens, so the AI of the weight GEMMs is about B FLOP/B in FP16 (2 FLOPs per 2-byte weight per token). As long as `B` is below the ridge point (about 247 on MI300X for FP16 matrix work), the step time is set by weight bandwidth and stays nearly constant, while throughput grows linearly with B. Past the ridge, the GEMMs become compute-bound and step time grows. Two other limits arrive first in practice: **KV-cache reads** grow with `B x context` and do not get amortized (attention stays memory-bound), and **latency SLOs** (Little's law plus queueing: larger batches mean longer waits to form a batch and longer steps). See [ML Systems Design](../ml-gpu/ML_Systems_Design.md).

**Q7.** Someone reports average speedups across 10 benchmarks as the arithmetic mean of the ratios. What is wrong?

The arithmetic mean of ratios is not consistent. A 2x speedup on one benchmark and a 0.5x slowdown on another average to 1.25x, which claims a gain, while swapping baseline and candidate also gives 1.25x. Use the **geometric mean** of ratios (here 1.0x), which is symmetric under inversion (Fleming and Wallace, 1986). If the benchmarks represent a real workload mix, compare **total time** for the weighted mix instead. Report per-benchmark CIs too: a geomean can hide a large regression on one important case.

**Q8.** Strong scaling of your MPI code flattens after 16 nodes. What do you measure, and what can you do?

Measure per-rank time split into compute, communication, and waiting (MPI profiling via PMPI tools, or traces), plus the max/mean imbalance per phase. Compute Karp-Flatt `e` vs N: a rising `e` means overhead that grows with N. Typical findings: the surface-to-volume ratio grows (halo exchange no longer shrinks as fast as compute), latency-dominated small messages, collectives scaling as log N or worse, load imbalance, or a serial I/O or setup phase. Fixes: overlap communication with computation (non-blocking halos, compute the interior first), aggregate messages, use topology-aware rank placement, pick a better decomposition (2D/3D instead of 1D slabs), and use hierarchical collectives. Alternatively, accept that strong scaling ends there and switch to weak scaling with a bigger problem (Gustafson).

**Q9.** Design a microbenchmark that measures L2 bandwidth on a CPU core.

Sweep the working-set size across the L1-to-L2 range (for example, 64 KiB to 1 MiB), allocated 64-byte aligned and pre-faulted. Use a streaming read kernel with several independent vector accumulators (so neither latency nor the add chain limits it), unrolled, repeated many times over the same buffer so the data stays L2-resident after warm-up. Pin the thread, fix the frequency, and report bytes per cycle (from `perf stat` cycles) as well as GB/s. Keep the result alive (`DoNotOptimize`). Validate with counters (L1 misses that hit in L2, few L2 misses) and look for the plateau between the L1 and L3 cliffs. Report median and spread over repetitions. Pitfalls: hardware prefetchers bringing data from L3 if the size is borderline, write-allocate for store tests, and TLB effects for sizes beyond L1 DTLB reach.

**Q10.** A profiler metric for the same kernel varies 3% run to run, and a user files a bug. How do you respond?

First check whether the variation is in the **workload** or the **tool**. Run the application without the profiler, using GPU-event timing and repetitions: if kernel time itself varies 3% (clocks, power, thermal state, neighbours, nondeterministic data-dependent work, atomics), the metric is faithfully reporting real variance. If the variation comes from the tool: counters collected across **multiple replay passes** are combined, so derived metrics mix passes taken under different cache and clock states; check whether metrics computed within one pass are stable; and look for counter multiplexing or sampling error. Mitigations: cap clocks for profiling runs, report the variance (and the number of passes) alongside metrics, collect sensitive ratios within a single pass, and document the expected noise floor. Then reply with data rather than an opinion.

**Q11.** The p99 latency of an inference service got worse after you doubled the maximum batch size, even though throughput improved. Why?

Larger batches raise throughput by amortizing weight reads (Q6), but (1) each step takes longer (more compute, more KV-cache reads), so every request in the batch waits for the longer step; (2) requests may wait in the queue for a batch to fill or for a slot; (3) mixing long prompts (prefill) with decodes stalls decodes behind big prefills, which is head-of-line blocking and high service-time variance (Kingman). Fixes: cap the batch by a latency budget rather than by count, continuous batching with chunked prefill, separate prefill and decode pools, and admission control to keep utilization below the knee of the latency curve.

**Q12.** Your vectorized loop is 4x faster on your workstation but no faster in CI. Give possible reasons.

(1) **ISA:** built with `-march=native` locally (AVX2 or AVX-512) but the CI binary targets the baseline (SSE2), or the reverse. Check `-fopt-info-vec` in both builds. (2) **Memory-bound in CI:** CI uses larger inputs that do not fit in cache, so SIMD speeds up arithmetic that is not the bottleneck. (3) **Noisy CI runners:** shared VMs with frequency scaling and noisy neighbours, so the effect drowns in variance. (4) **Different compiler or version** that vectorizes the baseline too, so both are fast. (5) **Alignment or aliasing** differences, so the loop is versioned and the scalar fallback runs. (6) **Debug or sanitizer builds** in CI. Compare the generated assembly and `perf stat` cycles and instructions between the two environments.

**Q13.** Why is "average CPU utilization 40%" not evidence that a service has headroom?

Averages hide bursts: 40% over a minute can be 100% for 20 seconds, during which queueing explodes (the M/M/1 knee). Utilization is per resource, so the CPU can be at 40% while one lock, one core (a single-threaded event loop), the NIC, a DB connection pool, or memory bandwidth is saturated. Hyperthreads inflate apparent capacity (100% of the logical CPUs is not 2x the work of 50%). Look at **saturation** signals (run-queue length, queue depths, latency percentiles vs load) and per-resource utilization (USE method), and load-test to find the knee directly.

**Q14.** How would you explain to a user why their kernel shows "2% of peak FLOPs" in rocprof-compute, and whether that is bad?

Peak FLOPs is the wrong yardstick for a memory-bound kernel. Compute the arithmetic intensity: for an elementwise kernel (about 0.1-0.5 FLOP/B), the roofline caps attainable performance at `AI x 5.3 TB/s`, which is 0.3-2% of peak FP32 FLOPs on MI300X. The right question is **what fraction of achievable HBM bandwidth it reaches**, which the roofline view shows directly as the distance from the memory roof. If it is at 80% of the empirical HBM ceiling, it is near optimal, and the only further win is to reduce bytes (fusion, lower precision) or to change the algorithm. If it is at 20%, look for poor coalescing, low occupancy, or too few bytes in flight.

---

## Further Reading

- S. Williams, A. Waterman, D. Patterson, "Roofline: An Insightful Visual Performance Model for Multicore Architectures", CACM 2009.
- J. Dean, L. A. Barroso, "The Tail at Scale", CACM 2013.
- G. Amdahl (1967); J. Gustafson, "Reevaluating Amdahl's Law", CACM 1988; A. Karp, H. Flatt, CACM 1990.
- U. Drepper, "What Every Programmer Should Know About Memory", 2007.
- N. Higham, *Accuracy and Stability of Numerical Algorithms*, 2nd ed., SIAM 2002 (summation error bounds).
- T. Mytkowicz et al., "Producing Wrong Data Without Doing Anything Obviously Wrong!", ASPLOS 2009.
- AMD Instinct MI300X data sheet and the [MI300 microarchitecture page](https://rocm.docs.amd.com/en/latest/reference/gpu-arch/mi300.html); rocprof-compute documentation (roofline analysis).
- Brendan Gregg, *Systems Performance*, 2nd ed. (USE method, Linux tooling).
