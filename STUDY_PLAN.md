# Study Plan -- Comprehensive 8-Week Interview Preparation Roadmap

> Last reviewed: 2026-11 · Assumes about 2.5 hours on weekdays, 4 hours on Saturday, and 2 hours on Sunday (about 18 hours a week)

> One schedule for the whole repository. It covers three target tracks, a fixed daily cadence, a week-by-week plan that links to the exact section to read, a compressed two-week emergency plan, a per-document progress checklist, and a weekly self-assessment template. Coding practice follows the [Coding Problem List](practice/Coding_Problem_List.md) protocol (timed attempts, grades A-D, day-3/day-14 re-solves). Design practice follows [HLD Mock Interviews](practice/HLD_Mock_Interviews.md). Behavioral prep follows [Behavioral Interview Prep](career/Behavioral_Interview_Prep.md).

---

## Table of Contents

1. [How to Use This Plan](#1-how-to-use-this-plan)
2. [Choosing Your Track](#2-choosing-your-track)
3. [Daily and Weekly Cadence](#3-daily-and-weekly-cadence)
    - [3.1 Weekday (about 2.5 hours)](#31-weekday-about-25-hours)
    - [3.2 Weekend](#32-weekend)
    - [3.3 Weekly volume by track](#33-weekly-volume-by-track)
    - [3.4 The weekly mock ladder](#34-the-weekly-mock-ladder)
4. [Eight-Week Overview](#4-eight-week-overview)
5. [Week-by-Week Plan](#5-week-by-week-plan)
    - [5.1 Week 1: Foundations and the Story Bank](#51-week-1-foundations-and-the-story-bank)
    - [5.2 Week 2: Memory, Concurrency, and Linear Structures](#52-week-2-memory-concurrency-and-linear-structures)
    - [5.3 Week 3: Graphs, Performance Models, and the First Design Mock](#53-week-3-graphs-performance-models-and-the-first-design-mock)
    - [5.4 Week 4: Heaps, Backtracking, and Tooling Internals](#54-week-4-heaps-backtracking-and-tooling-internals)
    - [5.5 Week 5: Dynamic Programming and Operating Systems](#55-week-5-dynamic-programming-and-operating-systems)
    - [5.6 Week 6: Greedy, Bits, and Distributed Design](#56-week-6-greedy-bits-and-distributed-design)
    - [5.7 Week 7: Company Lists, Build/Test/Ship, and Full Loops](#57-week-7-company-lists-buildtestship-and-full-loops)
    - [5.8 Week 8: Consolidation and Taper](#58-week-8-consolidation-and-taper)
6. [Two-Week Emergency Plan](#6-two-week-emergency-plan)
7. [Round-to-Document Map and Track Priorities](#7-round-to-document-map-and-track-priorities)
    - [7.1 Round-to-document map](#71-round-to-document-map)
    - [7.2 Track priorities](#72-track-priorities)
8. [Per-Document Progress Checklist](#8-per-document-progress-checklist)
    - [8.1 career](#81-career)
    - [8.2 computer-science](#82-computer-science)
    - [8.3 design-patterns](#83-design-patterns)
    - [8.4 languages](#84-languages)
    - [8.5 ml-gpu](#85-ml-gpu)
    - [8.6 practice](#86-practice)
    - [8.7 tools](#87-tools)
9. [Weekly Self-Assessment Template](#9-weekly-self-assessment-template)
    - [9.1 Decision rules](#91-decision-rules)

---

## 1. How to Use This Plan

The repository has roughly 60,000 lines of reference material. Reading it front to back would take longer than eight weeks and would not prepare you to perform under time pressure. This plan answers three questions every day: **what to practice**, **what to read**, and **how to tell whether it worked**.

**The rules:**

1. **Practice beats reading.** Every reading block ends with the section's **Q** blocks answered aloud *before* you look at the written answer. If you cannot answer a Q cold, mark the section `- [ ]` again in [Section 8](#8-per-document-progress-checklist) even if you have read it.
2. **One track is primary.** Pick a primary track in [Section 2](#2-choosing-your-track). All tracks share the coding, behavioral, and mock spine. Tracks differ in the fundamentals and design/domain blocks.
3. **Re-solves are not optional.** The [spaced-repetition schedule](practice/Coding_Problem_List.md#71-review-schedule) is what turns a solved problem into a retained pattern. If you fall behind, cut new problems, not re-solves.
4. **Measure weekly.** Fill in the [self-assessment](#9-weekly-self-assessment-template) every Sunday and use its decision rules to rebalance the next week.
5. **Interview language.** Tracks A and B should code in **C++** (systems and GPU loops often expect it; see the [NVIDIA/AMD/HPC mock variant](practice/Coding_Problem_List.md#91-format-two-random-mediums-in-45-minutes)). Track C may use Python. Use one language for all timed practice, and reserve the other for output quizzes.

**What "done" means for a section:** you can (a) answer every Q block in it without notes, (b) explain the key tradeoff table from memory, and (c) for code-heavy sections, re-type the central snippet from a blank file. Reading alone is not done.

**Q1. Why a fixed cadence instead of studying whatever feels weakest each day?**

Because self-assessed weakness is biased toward topics that feel uncomfortable, not toward topics that are scored. A fixed cadence guarantees daily coding reps (the round with the most weight in nearly every loop), keeps fundamentals and design from being postponed until the last week, and makes the weekly self-assessment comparable week to week. The weekly review is where you *do* rebalance, using data from the error log and mock scores rather than mood.

**Q2. How much of the material should I expect to finish?**

For your primary track, every "Core" document in the [priority table](#72-track-priorities) at least once, plus the Q blocks of every "Recommended" document. "Optional" documents are reference material: open them when a mock or a job description points at them. For the Track A owner, finishing about 60% of the repository with high retention beats skimming 100%.

---

## 2. Choosing Your Track

| Track | Target roles | Interview loop emphasis | Primary language |
|---|---|---|---|
| **A: GPU/HPC/profiling tools engineer** (primary for the owner) | GPU software, ROCm/CUDA tools, HPC performance, compiler/runtime-adjacent, AI accelerator teams at AMD, NVIDIA, Intel, hyperscaler GPU teams | coding (often C++ in a plain editor), GPU architecture and performance deep dive, project deep dive (rocprof-compute), concurrency, a systems or ML-systems design round, behavioral | C++ (Python for tooling questions) |
| **B: Systems C++ / infrastructure** | storage, databases, networking, trading infra, OS/runtime, build/CI infra, ML infra platform teams | coding, C++ language depth (object model, UB, memory model), concurrency coding, low-level design, distributed-systems HLD | C++ |
| **C: General big-tech SWE** | Google, Meta, Amazon, Microsoft generalist loops | two to four coding rounds, one or two HLD rounds (mid/senior), behavioral (Amazon LPs, Googleyness), sometimes LLD | Python or C++ |

**How to pick.** Count the rounds in your target loops ([Company Loop Profiles](career/Interview_Loops_and_Logistics.md#3-company-loop-profiles)). If more than one round is GPU/HPC domain, choose A. If the loop has a C++ language round or a concurrency coding round, choose B. Otherwise choose C. Many people run **A as primary with C's HLD blocks substituted on weeks 3, 4, and 6** when they are interviewing at big tech and GPU companies at the same time. The week tables make that substitution easy because each cell is self-contained.

**Mixing tracks.** Keep the coding and behavioral spine. Swap whole fundamentals or design cells, never half a cell, because each cell is sized to 45 minutes a day for a week.

**Q1. I am interviewing for an ML-infrastructure role. A or B?**

Start from B and replace the design cells on weeks 5-7 with Track A's ML-systems cells ([ML Systems Design](ml-gpu/ML_Systems_Design.md) sections 4-7). ML-infra loops usually look like systems loops (C++ or Python coding, distributed-systems design) plus one round on training or serving systems. They rarely ask for GPU microarchitecture depth, so Track A's [AMD GPU Architecture](ml-gpu/AMD_GPU_Architecture_and_Profiling.md) sections 1-3 become optional, but [Training Memory Math](ml-gpu/ML_AI_Frameworks.md#45-training-memory-math-zero-activations-and-offload) and [Prefill, Decode, and the KV Cache](ml-gpu/LLM_and_ML_Fundamentals.md#9-prefill-decode-and-the-kv-cache) become core.

**Q2. I work on GPU profiling tools today. Why spend any Track A time on fundamentals I use daily?**

Daily use is not the same as explaining under questioning. Interviewers for tools roles probe *why* (why does counter collection need multiple passes, why does serializing dispatches perturb timing, why does occupancy not always help). The [Project Deep Dive](career/Project_Deep_Dive_rocprof-compute.md) and [How GPU Profilers Work Internally](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#6-how-gpu-profilers-work-internally) sections exist to turn tacit knowledge into crisp, quantitative answers. The usual failure mode for an expert is rambling, not lack of knowledge.

---

## 3. Daily and Weekly Cadence

### 3.1 Weekday (about 2.5 hours)

| Block | Time | Content | Rules |
|---|---|---|---|
| **Coding** | 60-70 min | **2 new problems** from the week's patterns (Track C: 3) + any re-solves due today | timed per [Time targets](practice/Coding_Problem_List.md#61-time-targets) (Easy 15, Medium 25, Hard 40 min); log every attempt in the [error log](practice/Coding_Problem_List.md#72-error-log-template) |
| **Fundamentals** | 40-45 min | the week's fundamentals cell for your track | read one section, then answer its Q blocks aloud before reading the answers |
| **Design / domain** | 40-45 min | the week's design/domain cell for your track | draw or write something every day: a diagram, an estimate, a counter formula, a class sketch |
| **Recall** | 10 min | 15-20 cards from [Flashcards](practice/Flashcards.csv) or 10 one-liners from [Rapid-Fire](practice/CS_Fundamentals_Drills.md#3-rapid-fire-100-one-liners) | spaced repetition; mark misses |

If you only have **90 minutes** on a weekday: coding (1 new problem + re-solves, 45 min), then alternate fundamentals and design/domain on odd and even days (45 min).

### 3.2 Weekend

| Day | Time | Content |
|---|---|---|
| **Saturday** | about 4 h | **Weekly mock** (see each week's table) 60-120 min; 4 new problems (or catch-up); review the mock recording and log root causes |
| **Sunday** | about 2 h | re-solves due; behavioral block (45 min); [self-assessment](#9-weekly-self-assessment-template) (20 min); plan next week's two focus pairs (pattern + root cause) |

### 3.3 Weekly volume by track

| Track | New problems/week | 8-week total (approx.) | Problem source |
|---|---|---|---|
| A | 14 | 90-100 | [Core 75](practice/Coding_Problem_List.md#3-core-75-subset) + [NVIDIA/AMD/HPC list](practice/Coding_Problem_List.md#55-nvidia--amd--hpc-systems-flavored) + [Concurrency bonus](practice/Coding_Problem_List.md#41-concurrency-systems-c-and-gpuhpc-loops) |
| B | 14 | 90-100 | Core 75 + Concurrency bonus + [Concurrency Coding Problems](computer-science/Concurrency_Coding_Problems.md) |
| C | 19 | about 150 | the full [150-problem checklist](practice/Coding_Problem_List.md#2-the-150-problem-checklist-by-pattern) + one [company list](practice/Coding_Problem_List.md#5-company-flavored-lists-commonly-reported) |

These numbers follow the pattern order of the [Six-Week Coding Schedule](practice/Coding_Problem_List.md#8-six-week-coding-schedule), stretched to eight weeks so that week 7 holds company lists and week 8 holds only re-solves and mocks.

### 3.4 The weekly mock ladder

| Week | Coding mock | Second mock (by track) |
|---|---|---|
| 1 | 1 medium in 30 min, arrays/strings only | all: record the 90-second intro ([template](career/Behavioral_Interview_Prep.md#7-tell-me-about-yourself-the-90-second-template)) |
| 2 | two mediums in 45 min ([format](practice/Coding_Problem_List.md#91-format-two-random-mediums-in-45-minutes)) | A/B/C: 2 behavioral stories timed at 2-3 min each |
| 3 | two mediums in 45 min | A: [Project Deep Dive 10-minute walkthrough](career/Project_Deep_Dive_rocprof-compute.md#23-10-minute-walkthrough-whiteboard-plan); B/C: [45-minute HLD self-mock](practice/HLD_Mock_Interviews.md#2-running-a-45-minute-self-mock), Mock 1 |
| 4 | two mediums in 45 min | A: counter-diagnosis mock (explain [the worked example](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#54-worked-example-from-raw-counters-to-a-diagnosis) without notes); B/C: LLD mock (one worked design from [LLD](design-patterns/Low_Level_Design_Interview_Prep.md) in 45 min) |
| 5 | company-style variant | A: HLD Mock 9 (GPU profiling telemetry); B: concurrency coding mock (2 problems in 45 min); C: HLD Mock 3 or 4 |
| 6 | **mini loop**: 2 coding + 1 design + 1 behavioral, back to back | track-specific design round inside the loop |
| 7 | **full loop** (4-5 rounds) in your target company's format | A: domain round as one of the rounds; B: C++ language round; C: second HLD |
| 8 | two full loops early in the week, then taper | none in the final 48 hours |

Score coding mocks with the [coding rubric](practice/Coding_Problem_List.md#93-rubric) and design mocks with the [HLD rubric](practice/HLD_Mock_Interviews.md#3-evaluation-rubric-by-level). A partner mock is worth about two self-mocks; aim for at least two partner mocks (weeks 6 and 7).

**Q1. Why only two new problems a day for Tracks A and B?**

Because the retained number matters more than the attempted number. Two new problems plus due re-solves is about 60-70 minutes once the error log fills up (by week 3 you will typically have two or three re-solves due per day). Tracks A and B also need the fundamentals and domain blocks more than Track C does. Their loops spend one or two rounds on C++ depth, GPU architecture, or concurrency, which are not covered by LeetCode volume.

**Q2. What do I do on a day when coding takes the whole session?**

Stop at the [hard stop](practice/Coding_Problem_List.md#62-the-attempt---hint---solution---re-solve-loop), read the solution, re-type it, log it, and still do the 10-minute recall block. Skip that day's design/domain block and do not try to "catch up" later by doubling. The weekly table has slack on Saturday for one missed block. Two missed blocks in a week is a signal for the self-assessment, not a reason to work later.

---

## 4. Eight-Week Overview

| Week | Coding patterns | Track A focus | Track B focus | Track C focus | Behavioral (all) |
|---|---|---|---|---|---|
| 1 | hashing, two pointers, sliding window, prefix sum, stack parsing | C++ memory and the CDNA compute unit | C++ object model, RAII, Rule of 0/3/5 | arrays, hashing, Python data model, LLD method | STAR/CARL, story bank, 90-second intro |
| 2 | binary search, linked lists, cyclic sort, intervals, line sweep | concurrency, GPU memory model, latency hiding, roofline | C++ concurrency, concurrency coding 1-10, LLD | trees, heaps, graphs (DS), OOP, LLD worked designs | rocprof-compute pitches |
| 3 | DFS, BFS, union-find, topological sort | ROCm tools, counter methodology, first kernels | templates, STL, performance, HLD process | graph algorithms, databases, HLD process | question bank by competency |
| 4 | heaps, top K, K-way merge, monotonic stack, trie, backtracking | profiler internals, debugging, project deep dive | modern C++, UB, HLD core designs | tries, union-find, system-design primitives | failure/conflict frameworks |
| 5 | dynamic programming | GEMM/fusion kernels, LLM inference math, Triton | OS, networking, distributed systems | DP, OS, concurrency | company values mapping |
| 6 | greedy, bit manipulation, matrix | MPI/collectives, multi-GPU, ML systems design | perf tools, concurrency patterns, LLD infra designs | networks, security, distributed systems, more HLD | senior/staff signals |
| 7 | design problems, company list, concurrency bonus | build/test/ship for ROCm, serving and scheduling design | CMake, testing, Git, containers, Rust/Go (optional) | probability, estimation, quizzes, unsolved HLD prompts | offers and negotiation |
| 8 | re-solves and random mocks only | Q banks, cheat sheet, mocks | Q banks, cheat sheet, mocks | Q banks, cheat sheet, mocks | rehearsal plan, day-of checklist |

---

## 5. Week-by-Week Plan

Each week lists: the **coding** patterns (shared), the three track cells for **fundamentals** and **design/domain** (45 minutes a day each, Monday to Friday), the shared **behavioral** block (Sunday), the **Saturday mock**, and an **exit check**. The exit check is a short oral quiz. If you fail more than one item, carry that item into next week's Monday and Tuesday slots before starting new material.

### 5.1 Week 1: Foundations and the Story Bank

**Coding (all tracks).** Patterns: [Hashing & Array Classics](practice/Coding_Problem_List.md#222-hashing--array-classics), [Two Pointers](practice/Coding_Problem_List.md#21-two-pointers), [Sliding Window](practice/Coding_Problem_List.md#22-sliding-window), [Prefix Sum](practice/Coding_Problem_List.md#221-prefix-sum--difference-array), [Stack-based Parsing](practice/Coding_Problem_List.md#224-stack-based-parsing). Theory: [LeetCode Patterns 1-2](computer-science/LeetCode_Patterns.md#1-two-pointers), [21-22](computer-science/LeetCode_Patterns.md#21-prefix-sum--difference-array), [24](computer-science/LeetCode_Patterns.md#24-stack-based-parsing). Before the first problem, read [How to Use This List](practice/Coding_Problem_List.md#1-how-to-use-this-list) and the [constraint-to-complexity cheat sheet](practice/Coding_Problem_List.md#15-constraint-to-complexity-cheat-sheet).

| Block | Track A: GPU/HPC/profiling | Track B: systems C++ / infra | Track C: general SWE |
|---|---|---|---|
| **Fundamentals** | [C++ 2: Pointers and const](languages/Cpp_Fundamentals.md#2-pointers-references-and-const-correctness); [C++ 3: Memory Management](languages/Cpp_Fundamentals.md#3-memory-management); [C++ 5: Move Semantics](languages/Cpp_Fundamentals.md#5-move-semantics-and-perfect-forwarding); [CS 7.4 Memory Hierarchy](computer-science/CS_Fundamentals.md#74-memory-hierarchy), [7.5 Cache](computer-science/CS_Fundamentals.md#75-cache), [7.6 Virtual Memory](computer-science/CS_Fundamentals.md#76-virtual-memory) | [C++ 1: Type System](languages/Cpp_Fundamentals.md#1-type-system-and-fundamentals) through [C++ 5: Move Semantics](languages/Cpp_Fundamentals.md#5-move-semantics-and-perfect-forwarding); [C++ 4: OOP](languages/Cpp_Fundamentals.md#4-object-oriented-programming) (vtables, slicing) | [DSA 1-5](computer-science/DSA_Fundamentals.md#1-arrays-and-dynamic-arrays) (arrays through hash tables); [DSA 25: Complexity Cheat Sheet](computer-science/DSA_Fundamentals.md#25-master-complexity-cheat-sheet); [Python 1-7](languages/Python_Fundamentals.md#1-python-data-model--object-system) + [Part 1 questions](languages/Python_Fundamentals.md#part-1-interview-questions) |
| **Design / domain** | [AMD GPU 1: CDNA Compute Unit](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#1-cdna-compute-unit-and-chip-architecture) (all of 1.1-1.13, especially [occupancy math](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#14-vgprs-agprs-and-occupancy-math)); [Parallel GPU 17: GPU Architecture Fundamentals](ml-gpu/Parallel_GPU_Programming.md#17-gpu-architecture-fundamentals); [18: Programming Model](ml-gpu/Parallel_GPU_Programming.md#18-cuda-programming-model) | [Design Patterns C++ 1-3](design-patterns/Design_Patterns_Cpp.md#1-what-design-patterns-are-and-are-not); [27: RAII](design-patterns/Design_Patterns_Cpp.md#27-raii----resource-acquisition-is-initialization); [30: Rule of 0/3/5](design-patterns/Design_Patterns_Cpp.md#30-rule-of-035-and-copy-and-swap); [29: pImpl](design-patterns/Design_Patterns_Cpp.md#29-pimpl----pointer-to-implementation) | [LLD 1-3](design-patterns/Low_Level_Design_Interview_Prep.md#1-what-low-level-design-interviews-evaluate) (what is evaluated, method, principles); [CS 4: OOP and Patterns](computer-science/CS_Fundamentals.md#4-object-oriented-programming-and-design-patterns) |
| **Language drill (Fri)** | [C++ quiz 2-3](practice/Cpp_Output_Quiz.md#2-object-model-inheritance-and-layout) | [C++ quiz 2-3](practice/Cpp_Output_Quiz.md#2-object-model-inheritance-and-layout) | [Python quiz 2-4](practice/Python_Output_Quiz.md#2-functions-closures--default-arguments) |

**Behavioral (Sunday, all).** [What Behavioral Rounds Assess](career/Behavioral_Interview_Prep.md#1-what-behavioral-rounds-assess), [STAR and CARL](career/Behavioral_Interview_Prep.md#2-answer-formats-star-and-carl), [Building Your Story Bank](career/Behavioral_Interview_Prep.md#3-building-your-story-bank). Track A: use the [prompts for a GPU profiling-tools engineer](career/Behavioral_Interview_Prep.md#33-guiding-prompts-for-a-gpu-profiling-tools-engineer). Deliverable: 8 story cards, each a bullet list, not prose. Draft the [90-second intro](career/Behavioral_Interview_Prep.md#7-tell-me-about-yourself-the-90-second-template).

**Saturday mock.** One medium in 30 minutes from this week's patterns, recorded. Then record the 90-second intro twice and keep the better take.

**Exit check.**

- State the sliding-window validity condition for "longest substring with at most k distinct characters" and why the left pointer never moves backward.
- (A) Compute occupancy for a kernel using 96 VGPRs per lane (no AGPRs) on CDNA3 and say which resource limits it. (Answer: floor(512 / 96) = 5 waves per SIMD out of a maximum of 8, so VGPRs are the limiter unless LDS or SGPRs are tighter.)
- (B) Explain when the compiler generates a move constructor and when it silently falls back to copy.
- (C) Explain why a Python dict lookup is O(1) on average and what makes it degrade.

### 5.2 Week 2: Memory, Concurrency, and Linear Structures

**Coding (all tracks).** Patterns: [Modified Binary Search](practice/Coding_Problem_List.md#211-modified-binary-search), [Fast and Slow Pointers](practice/Coding_Problem_List.md#23-fast-and-slow-pointers), [In-place Linked List Reversal](practice/Coding_Problem_List.md#26-in-place-linked-list-reversal), [Cyclic Sort](practice/Coding_Problem_List.md#25-cyclic-sort), [Merge Intervals](practice/Coding_Problem_List.md#24-merge-intervals), [Line Sweep](practice/Coding_Problem_List.md#225-line-sweep--advanced-intervals). Theory: [LeetCode Patterns 3-6](computer-science/LeetCode_Patterns.md#3-fast-and-slow-pointers), [11](computer-science/LeetCode_Patterns.md#11-modified-binary-search), [25](computer-science/LeetCode_Patterns.md#25-line-sweep--advanced-intervals), [28: Binary Search on the Answer](computer-science/LeetCode_Patterns.md#28-binary-search-on-the-answer).

| Block | Track A: GPU/HPC/profiling | Track B: systems C++ / infra | Track C: general SWE |
|---|---|---|---|
| **Fundamentals** | [C++ 12: Multithreading](languages/Cpp_Fundamentals.md#12-multithreading-and-concurrency); [CS 6.2 Synchronization Primitives](computer-science/CS_Fundamentals.md#62-synchronization-primitives), [6.9 Memory Models](computer-science/CS_Fundamentals.md#69-memory-models-and-visibility); [Concurrency Coding 1-8](computer-science/Concurrency_Coding_Problems.md#1-toolbox-primitives-templates-and-testing) (one problem per day, coded in C++) | [C++ 12: Multithreading](languages/Cpp_Fundamentals.md#12-multithreading-and-concurrency); [CS 6: Concurrency](computer-science/CS_Fundamentals.md#6-concurrency-and-multithreading) (6.1-6.11); [Concurrency Coding 1-10](computer-science/Concurrency_Coding_Problems.md#1-toolbox-primitives-templates-and-testing) | [DSA 6-9](computer-science/DSA_Fundamentals.md#6-trees-binary-trees--bsts) (trees, balanced BSTs, heaps, graphs); [DSA 14-15](computer-science/DSA_Fundamentals.md#14-sorting-algorithms) (sorting, searching); [Python 8-12](languages/Python_Fundamentals.md#8-classes--oop-fundamentals) + [Part 2 questions](languages/Python_Fundamentals.md#part-2-interview-questions) |
| **Design / domain** | [AMD GPU 2: Memory Model](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#2-gpu-memory-model); [3: Latency Hiding](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#3-latency-hiding-quantified); [Parallel GPU 19-21](ml-gpu/Parallel_GPU_Programming.md#19-cuda-memory-model) (memory model, memory optimization, synchronization); [Perf Eng 3: Roofline](computer-science/Performance_Engineering.md#3-roofline-model); [4: Little's Law](computer-science/Performance_Engineering.md#4-littles-law-and-queueing) | [LLD 1-4](design-patterns/Low_Level_Design_Interview_Prep.md#1-what-low-level-design-interviews-evaluate) (method, principles, concurrency and failure); [LLD 10: Rate Limiter](design-patterns/Low_Level_Design_Interview_Prep.md#10-worked-design-rate-limiter); [LLD 11: Cache](design-patterns/Low_Level_Design_Interview_Prep.md#11-worked-design-cache) | [LLD 5: Parking Lot](design-patterns/Low_Level_Design_Interview_Prep.md#5-worked-design-parking-lot), [6: Elevator](design-patterns/Low_Level_Design_Interview_Prep.md#6-worked-design-elevator-system), [9: Splitwise](design-patterns/Low_Level_Design_Interview_Prep.md#9-worked-design-splitwise-expense-sharing); skim [Design Patterns Python 1-3](design-patterns/Design_Patterns_Python.md#1-what-design-patterns-are-and-are-not) and the [Pattern Cheat Sheet](design-patterns/Design_Patterns_Python.md#47-pattern-cheat-sheet) |
| **Language drill (Fri)** | [C++ quiz 4-6](practice/Cpp_Output_Quiz.md#4-integers-characters-and-floating-point) | [C++ quiz 4-6](practice/Cpp_Output_Quiz.md#4-integers-characters-and-floating-point) | [Python quiz 5-7](practice/Python_Output_Quiz.md#5-copying-sorting--strings) |

**Behavioral (Sunday, all).** Track A and B: [The Pitches](career/Project_Deep_Dive_rocprof-compute.md#2-the-pitches) (30-second, 2-minute) and [What Problem It Solves](career/Project_Deep_Dive_rocprof-compute.md#3-what-problem-it-solves). Track C: write the 2-minute pitch for your own most significant project using the same structure. All: read [Confidentiality](career/Behavioral_Interview_Prep.md#35-confidentiality-talking-about-current-work-safely) before rehearsing anything about current work.

**Saturday mock.** [Two mediums in 45 minutes](practice/Coding_Problem_List.md#91-format-two-random-mediums-in-45-minutes). Then tell two story cards aloud, timed at 2-3 minutes each.

**Exit check.**

- Write the binary-search template with a monotonic predicate and state its loop invariant.
- Explain why `std::condition_variable::wait` must be called in a loop (or with a predicate).
- (A) Using Little's Law, how many bytes must be in flight on MI300X to sustain 80% of its 5.3 TB/s peak (4.24 TB/s) at an assumed 800 ns loaded latency? (Answer: 4.24e12 x 800e-9 = about 3.4 MB, roughly 11 KiB per CU across 304 CUs; see [3.2](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#32-worked-example-saturating-hbm).)
- (B) Sketch a thread-safe LRU cache interface and say where the lock goes.
- (C) Draw the class diagram for the parking lot in 5 minutes.

### 5.3 Week 3: Graphs, Performance Models, and the First Design Mock

**Coding (all tracks).** Patterns: [DFS](practice/Coding_Problem_List.md#28-dfs-depth-first-search), [BFS](practice/Coding_Problem_List.md#27-bfs-breadth-first-search), [Union Find](practice/Coding_Problem_List.md#216-union-find-disjoint-set), [Topological Sort](practice/Coding_Problem_List.md#214-topological-sort). Theory: [LeetCode Patterns 7-8](computer-science/LeetCode_Patterns.md#7-bfs-breadth-first-search), [14](computer-science/LeetCode_Patterns.md#14-topological-sort), [16](computer-science/LeetCode_Patterns.md#16-union-find-disjoint-set); [DSA 16: Graph Traversals](computer-science/DSA_Fundamentals.md#16-graph-traversals).

| Block | Track A: GPU/HPC/profiling | Track B: systems C++ / infra | Track C: general SWE |
|---|---|---|---|
| **Fundamentals** | [Perf Eng 5: Memory Hierarchy Programming](computer-science/Performance_Engineering.md#5-memory-hierarchy-programming); [6: SIMD](computer-science/Performance_Engineering.md#6-simd-and-vectorization); [Perf Eng 1-2](computer-science/Performance_Engineering.md#1-latency-vs-throughput-percentiles-and-tail-latency) (percentiles, Amdahl/Gustafson); [C++ 13: Compilation and Linking](languages/Cpp_Fundamentals.md#13-compilation-linking-and-the-preprocessor) | [C++ 6: Templates](languages/Cpp_Fundamentals.md#6-templates); [7: STL Containers](languages/Cpp_Fundamentals.md#7-stl-containers); [8: Iterators and Lambdas](languages/Cpp_Fundamentals.md#8-iterators-algorithms-and-lambdas); [Perf Eng 5](computer-science/Performance_Engineering.md#5-memory-hierarchy-programming) | [DSA 16-18](computer-science/DSA_Fundamentals.md#16-graph-traversals) (traversals, shortest paths, MST); [CS 3.1-3.5](computer-science/CS_Fundamentals.md#31-relational-database-concepts) (relational model, SQL, normalization, indexing, ACID); [SQL exercises E1-E11](practice/SQL_and_Pandas_Exercises.md#3-exercises-ranking-top-n-and-medians) |
| **Design / domain** | [AMD GPU 4: ROCm Profiling Tools](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#4-rocm-profiling-tools); [5: Counter-Driven Methodology](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#5-counter-driven-performance-methodology); [Kernel Case Studies 0-2](ml-gpu/GPU_Kernel_Case_Studies.md#0-conventions-hardware-numbers-and-measurement-harness) (harness, reduction ladder, transpose); [Parallel GPU 25-30](ml-gpu/Parallel_GPU_Programming.md#25-hip-fundamentals-and-portability) (HIP), skim | [HLD 1-4](computer-science/High_Level_Design.md#1-what-high-level-design-covers) (process, estimation, building blocks); [HLD 6.1 URL Shortener](computer-science/High_Level_Design.md#61-url-shortener); [6.2 Rate Limiter](computer-science/High_Level_Design.md#62-rate-limiter) | [HLD 1-4](computer-science/High_Level_Design.md#1-what-high-level-design-covers); [HLD 6.1 URL Shortener](computer-science/High_Level_Design.md#61-url-shortener); [CS 5.1-5.9](computer-science/CS_Fundamentals.md#51-scalability) (scalability through estimation) |
| **Language drill (Fri)** | [C++ quiz 7-8](practice/Cpp_Output_Quiz.md#7-move-semantics-and-copy-elision) | [C++ quiz 7-8](practice/Cpp_Output_Quiz.md#7-move-semantics-and-copy-elision) | [Python quiz 8-9](practice/Python_Output_Quiz.md#8-iterators-generators--comprehensions) |

**Behavioral (Sunday, all).** [Question Bank by Competency](career/Behavioral_Interview_Prep.md#5-question-bank-by-competency): answer one question from each of 5.1-5.6 aloud with your story cards; fill in the [coverage matrix](career/Behavioral_Interview_Prep.md#36-coverage-matrix).

**Saturday mock.** Coding: two mediums in 45 minutes (graphs allowed). Second mock: Track A delivers the [10-minute walkthrough](career/Project_Deep_Dive_rocprof-compute.md#23-10-minute-walkthrough-whiteboard-plan) of rocprof-compute to a timer and a recording. Tracks B and C run [HLD Mock 1: URL Shortener](practice/HLD_Mock_Interviews.md#4-mock-1-url-shortener) using the [45-minute self-mock](practice/HLD_Mock_Interviews.md#2-running-a-45-minute-self-mock).

**Exit check.**

- Kahn's algorithm: how does it detect a cycle?
- (A) Compute the arithmetic intensity of a float32 vector add (`c = a + b`) and say whether it is memory- or compute-bound on MI300X. (Answer: 1 FLOP per 12 bytes, about 0.083 FLOP/byte; deeply memory-bound.)
- (A) Name the ROCm tool you would use for (i) a timeline of kernels and API calls, (ii) per-kernel speed-of-light analysis, (iii) a whole-application CPU+GPU trace.
- (B/C) Estimate QPS and 5-year storage for a URL shortener with 100 M new URLs per month and a 100:1 read:write ratio.

### 5.4 Week 4: Heaps, Backtracking, and Tooling Internals

**Coding (all tracks).** Patterns: [Two Heaps](practice/Coding_Problem_List.md#29-two-heaps), [Top K](practice/Coding_Problem_List.md#212-top-k-elements), [K-way Merge](practice/Coding_Problem_List.md#213-k-way-merge), [Monotonic Stack / Queue](practice/Coding_Problem_List.md#215-monotonic-stack--queue), [Trie](practice/Coding_Problem_List.md#217-trie-prefix-tree), [Subsets / Backtracking](practice/Coding_Problem_List.md#210-subsets--backtracking). Theory: [LeetCode Patterns 9-10](computer-science/LeetCode_Patterns.md#9-two-heaps), [12-13](computer-science/LeetCode_Patterns.md#12-top-k-elements), [15](computer-science/LeetCode_Patterns.md#15-monotonic-stack--queue), [17](computer-science/LeetCode_Patterns.md#17-trie-prefix-tree).

| Block | Track A: GPU/HPC/profiling | Track B: systems C++ / infra | Track C: general SWE |
|---|---|---|---|
| **Fundamentals** | [Debugging Tools 8-11](tools/Debugging_and_Profiling_Tools.md#8-perf-fundamentals-and-hardware-counters) (perf, flame graphs, false sharing); [Perf Eng 8: Benchmarking Rigor](computer-science/Performance_Engineering.md#8-benchmarking-rigor); [9: Floating-Point Numerics](computer-science/Performance_Engineering.md#9-floating-point-numerics-and-reproducibility) | [C++ 9-11](languages/Cpp_Fundamentals.md#9-c1114-features) (C++11 through C++20); [C++ 14: Exceptions](languages/Cpp_Fundamentals.md#14-exception-handling-and-error-management); [15: Undefined Behavior](languages/Cpp_Fundamentals.md#15-undefined-behavior-implementation-defined-and-best-practices) | [DSA 10: Tries](computer-science/DSA_Fundamentals.md#10-tries-prefix-trees); [8: Heaps](computer-science/DSA_Fundamentals.md#8-heaps); [13: Union-Find](computer-science/DSA_Fundamentals.md#13-disjoint-set-union-union-find); [23: Backtracking](computer-science/DSA_Fundamentals.md#23-backtracking); [Python 13-18](languages/Python_Fundamentals.md#13-error-handling--exceptions) + [Part 3 questions](languages/Python_Fundamentals.md#part-3-interview-questions) |
| **Design / domain** | [AMD GPU 6: How GPU Profilers Work Internally](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#6-how-gpu-profilers-work-internally); [7: GPU Debugging](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#7-gpu-debugging); [Project Deep Dive 5-8](career/Project_Deep_Dive_rocprof-compute.md#5-architecture-overview) (architecture, profile mode, analyze mode, roofline); [Kernel Case Studies 3-5](ml-gpu/GPU_Kernel_Case_Studies.md#3-prefix-scan) (scan, histogram, softmax/LayerNorm) | [HLD 5: Cross-Cutting Decisions](computer-science/High_Level_Design.md#5-cross-cutting-design-decisions); [HLD 6.8 Distributed KV Store](computer-science/High_Level_Design.md#68-distributed-key-value-store); [6.12 Job Scheduler](computer-science/High_Level_Design.md#612-distributed-job-scheduler); [Concurrency Coding 11-17](computer-science/Concurrency_Coding_Problems.md#11-thread-safe-lru-cache) | [HLD 5](computer-science/High_Level_Design.md#5-cross-cutting-design-decisions); [HLD 6.2 Rate Limiter](computer-science/High_Level_Design.md#62-rate-limiter), [6.3 News Feed](computer-science/High_Level_Design.md#63-news-feed), [6.4 Chat](computer-science/High_Level_Design.md#64-chat-system); [LLD 11: Cache](design-patterns/Low_Level_Design_Interview_Prep.md#11-worked-design-cache) |
| **Language drill (Fri)** | [C++ quiz 9-10](practice/Cpp_Output_Quiz.md#9-smart-pointers-and-exceptions); [C++ 16: implement unique_ptr from scratch](languages/Cpp_Fundamentals.md#16-implement-from-scratch-exercises) | [C++ quiz 9-10](practice/Cpp_Output_Quiz.md#9-smart-pointers-and-exceptions); [C++ 16: implement-from-scratch](languages/Cpp_Fundamentals.md#16-implement-from-scratch-exercises) (`unique_ptr`, `shared_ptr`, `vector`) | [Python quiz 10-11](practice/Python_Output_Quiz.md#10-classes-attributes--the-mro) |

**Behavioral (Sunday, all).** [Frameworks for Failure and Conflict Answers](career/Behavioral_Interview_Prep.md#6-frameworks-for-failure-and-conflict-answers), including [the weakness question](career/Behavioral_Interview_Prep.md#64-the-weakness-question). Track A also does [Key Design Tradeoffs](career/Project_Deep_Dive_rocprof-compute.md#10-key-design-tradeoffs).

**Saturday mock.** Coding: two mediums in 45 minutes. Second mock: Track A explains the [raw-counters-to-diagnosis worked example](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#54-worked-example-from-raw-counters-to-a-diagnosis) without notes, then the [decision tree](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#55-decision-tree-from-symptom-to-bottleneck), in 20 minutes. Tracks B and C pick one unread worked design from [LLD](design-patterns/Low_Level_Design_Interview_Prep.md) (for example [Task Scheduler](design-patterns/Low_Level_Design_Interview_Prep.md#13-worked-design-task-scheduler) or [Movie Ticket Booking](design-patterns/Low_Level_Design_Interview_Prep.md#17-worked-design-movie-ticket-booking-bookmyshow)) and do it in 45 minutes using the [machine-coding playbook](design-patterns/Low_Level_Design_Interview_Prep.md#27-machine-coding-round-playbook), then compare.

**Exit check.**

- Why is a min-heap of size k the right structure for "top k largest", and what is the complexity?
- (A) Explain why collecting 200 counters on one kernel needs multiple replay passes, and what that does to run-to-run variance.
- (A) Walk through what happens between `hipLaunchKernel` and the first wave starting (AQL packet, doorbell, command processor).
- (B) Name three distinct kinds of UB a sanitizer catches and one it cannot.
- (C) Explain fan-out-on-write vs fan-out-on-read for a news feed and when you switch.

### 5.5 Week 5: Dynamic Programming and Operating Systems

**Coding (all tracks).** Pattern: [Dynamic Programming](practice/Coding_Problem_List.md#218-dynamic-programming). Theory: [LeetCode Patterns 18](computer-science/LeetCode_Patterns.md#18-dynamic-programming); [DSA 20: Dynamic Programming](computer-science/DSA_Fundamentals.md#20-dynamic-programming). Write state, transition, and base case as a comment before coding every DP problem.

| Block | Track A: GPU/HPC/profiling | Track B: systems C++ / infra | Track C: general SWE |
|---|---|---|---|
| **Fundamentals** | [CS 1.1 Processes and Threads](computer-science/CS_Fundamentals.md#11-processes-and-threads), [1.3 Memory Management](computer-science/CS_Fundamentals.md#13-memory-management), [1.7 System Calls](computer-science/CS_Fundamentals.md#17-system-calls), [1.9 Process Lifecycle and Signals](computer-science/CS_Fundamentals.md#19-linux-process-lifecycle-signals-and-file-descriptors), [1.11 Linux Memory Internals](computer-science/CS_Fundamentals.md#111-linux-memory-management-internals); [Linux 9: Env Vars, Shared Libraries, GPU Visibility](tools/Linux_Command_Line.md#9-environment-variables-shared-libraries-and-gpu-visibility) | [CS 1: Operating Systems](computer-science/CS_Fundamentals.md#1-operating-systems) (1.1-1.14, especially [1.10 epoll](computer-science/CS_Fundamentals.md#110-io-multiplexing-and-event-driven-servers)); [CS 2.2 TCP vs UDP](computer-science/CS_Fundamentals.md#22-tcp-vs-udp), [2.9 TCP Internals](computer-science/CS_Fundamentals.md#29-tcp-internals-deep-dive); [Linux 1-8](tools/Linux_Command_Line.md#1-how-the-shell-parses-a-command-line) | [CS 1: Operating Systems](computer-science/CS_Fundamentals.md#1-operating-systems) (1.1-1.4, 1.14); [CS 6.1-6.5](computer-science/CS_Fundamentals.md#61-threads-vs-processes); [Python 19-23](languages/Python_Fundamentals.md#19-the-gil--threading) (GIL, multiprocessing, asyncio) + [Part 4 questions](languages/Python_Fundamentals.md#part-4-interview-questions) |
| **Design / domain** | [Kernel Case Studies 6: Tiled GEMM](ml-gpu/GPU_Kernel_Case_Studies.md#6-tiled-gemm-progression), [7: Fusion and Launch Overhead](ml-gpu/GPU_Kernel_Case_Studies.md#7-elementwise-fusion-and-kernel-launch-overhead); [LLM 5-9](ml-gpu/LLM_and_ML_Fundamentals.md#5-attention) (attention, decoder block, FLOP accounting, FlashAttention, KV cache); [ML Frameworks 25-28: Triton](ml-gpu/ML_AI_Frameworks.md#25-triton-fundamentals) | [CS 8.1 Consistency Models](computer-science/CS_Fundamentals.md#81-consistency-models), [8.2 Consensus](computer-science/CS_Fundamentals.md#82-consensus-algorithms), [8.12 Raft in Depth](computer-science/CS_Fundamentals.md#812-consensus-theory-and-raft-in-depth), [8.13 Leases and Fencing](computer-science/CS_Fundamentals.md#813-consistency-guarantees-split-brain-leases-and-fencing); [HLD 6.13 Metrics and Monitoring](computer-science/High_Level_Design.md#613-metrics-logging-and-monitoring-system) | [HLD 6.5-6.9](computer-science/High_Level_Design.md#65-video-streaming-platform) (video, ride-sharing, payments, KV store, typeahead); [HLD Mock 3: News Feed](practice/HLD_Mock_Interviews.md#6-mock-3-news-feed) |
| **Language drill (Fri)** | [Python 19: GIL](languages/Python_Fundamentals.md#19-the-gil--threading) and [Python 31: C/C++ Interop](languages/Python_Fundamentals.md#31-python-and-cc-interop) (rocprof-compute is Python-heavy) | [C++ quiz](practice/Cpp_Output_Quiz.md#11-topic-index): redo every item missed so far | [Python quiz](practice/Python_Output_Quiz.md#12-topic-index): redo every item missed so far |

**Behavioral (Sunday, all).** [Mapping Stories to Company Values](career/Behavioral_Interview_Prep.md#4-mapping-stories-to-company-values) for each target company; rehearse [one story, many framings](career/Behavioral_Interview_Prep.md#46-one-story-many-framings).

**Saturday mock.** Coding: a company-style variant from the [mock format table](practice/Coding_Problem_List.md#91-format-two-random-mediums-in-45-minutes) (Track A: NVIDIA/AMD/HPC-style in C++ with sanitizers). Second mock: Track A runs [HLD Mock 9: GPU Profiling Telemetry Service](practice/HLD_Mock_Interviews.md#12-mock-9-gpu-profiling-telemetry-service); Track B does two problems from [Concurrency Coding](computer-science/Concurrency_Coding_Problems.md) not yet solved, in 45 minutes; Track C runs [HLD Mock 4: Chat System](practice/HLD_Mock_Interviews.md#7-mock-4-chat-system).

**Exit check.**

- Derive the recurrence for edit distance and its space-optimized form.
- What happens on a page fault, step by step, from the TLB miss to the instruction restart?
- (A) KV-cache bytes per token for a 70B-class model with 80 layers, 8 KV heads, head dimension 128, FP16: 2 x 80 x 8 x 128 x 2 bytes = 327,680 bytes, about 0.33 MB per token. Say why decode is memory-bound.
- (B) Explain Raft's leader-election safety rule (vote only for a candidate whose log is at least as up to date).
- (C) Explain idempotency keys for a payment API.

### 5.6 Week 6: Greedy, Bits, and Distributed Design

**Coding (all tracks).** Patterns: [Greedy](practice/Coding_Problem_List.md#219-greedy), [Bit Manipulation](practice/Coding_Problem_List.md#220-bit-manipulation), [Matrix Manipulation](practice/Coding_Problem_List.md#223-matrix-manipulation). Theory: [LeetCode Patterns 19-20](computer-science/LeetCode_Patterns.md#19-greedy), [23](computer-science/LeetCode_Patterns.md#23-matrix-manipulation); [DSA 22: Greedy](computer-science/DSA_Fundamentals.md#22-greedy-algorithms), [24: Bit Manipulation](computer-science/DSA_Fundamentals.md#24-bit-manipulation).

| Block | Track A: GPU/HPC/profiling | Track B: systems C++ / infra | Track C: general SWE |
|---|---|---|---|
| **Fundamentals** | [Parallel GPU 1-3](ml-gpu/Parallel_GPU_Programming.md#1-mpi-fundamentals) (MPI basics, point-to-point, collectives); [34: Collective Algorithms and Cost Model](ml-gpu/Parallel_GPU_Programming.md#34-collective-communication-algorithms-and-cost-model); [35: Multi-GPU](ml-gpu/Parallel_GPU_Programming.md#35-multi-gpu-programming-beyond-peer-copies-hip); [CS 2.10 HPC Interconnects](computer-science/CS_Fundamentals.md#210-hpc-and-datacenter-interconnects); [Perf Eng 7: NUMA](computer-science/Performance_Engineering.md#7-numa) | [Perf Eng 1-4](computer-science/Performance_Engineering.md#1-latency-vs-throughput-percentiles-and-tail-latency), [7-8](computer-science/Performance_Engineering.md#7-numa); [Debugging Tools 3-14](tools/Debugging_and_Profiling_Tools.md#3-gdb-essentials) (GDB, core dumps, perf, strace, sanitizers) | [CS 2: Computer Networks](computer-science/CS_Fundamentals.md#2-computer-networks); [CS 9: Security](computer-science/CS_Fundamentals.md#9-security); [CS 8: Distributed Systems](computer-science/CS_Fundamentals.md#8-distributed-systems) (8.1-8.10) |
| **Design / domain** | [ML Systems Design 1-3](ml-gpu/ML_Systems_Design.md#1-how-ml-system-design-differs-from-classic-hld) (framework, numbers); [5: Distributed Training of a 70B Model](ml-gpu/ML_Systems_Design.md#5-case-study-distributed-training-of-a-70b-model-on-512-mi300x); [7: Fleet-Wide GPU Profiling Service](ml-gpu/ML_Systems_Design.md#7-case-study-fleet-wide-gpu-profiling-and-telemetry-service); [ML Frameworks 45: Training Memory Math](ml-gpu/ML_AI_Frameworks.md#45-training-memory-math-zero-activations-and-offload); [HLD 2-3](computer-science/High_Level_Design.md#2-a-repeatable-interview-process) (process, estimation) | [Design Patterns C++ 39-52](design-patterns/Design_Patterns_Cpp.md#39-producer-consumer) (producer-consumer through RCU); [LLD 13: Task Scheduler](design-patterns/Low_Level_Design_Interview_Prep.md#13-worked-design-task-scheduler), [19: Logging Framework](design-patterns/Low_Level_Design_Interview_Prep.md#19-worked-design-logging-framework), [20: Pub-Sub Broker](design-patterns/Low_Level_Design_Interview_Prep.md#20-worked-design-pub-sub-message-broker) | [HLD 6.10-6.15](computer-science/High_Level_Design.md#610-web-crawler) (crawler, notifications, scheduler, metrics, object storage, ticket booking); [LLD 17: Movie Ticket Booking](design-patterns/Low_Level_Design_Interview_Prep.md#17-worked-design-movie-ticket-booking-bookmyshow) |
| **Language drill (Fri)** | [CPP Testing 41: Testing GPU/HIP Code](languages/CPP_Testing.md#41-testing-gpu--hip-code); [43: Google Benchmark](languages/CPP_Testing.md#43-microbenchmarking-with-google-benchmark) | [C++ quiz](practice/Cpp_Output_Quiz.md#11-topic-index) full pass, timed | [Python 24-27](languages/Python_Fundamentals.md#24-memory-management--garbage-collection) + [Part 5 questions](languages/Python_Fundamentals.md#part-5-interview-questions) |

**Behavioral (Sunday, all).** [Senior and Staff-Level Signals](career/Behavioral_Interview_Prep.md#8-senior-and-staff-level-signals); uplevel your three strongest stories using [8.3](career/Behavioral_Interview_Prep.md#83-upleveling-a-story). Re-read [Anti-Patterns](career/Behavioral_Interview_Prep.md#9-anti-patterns).

**Saturday mock (mini loop, back to back, recorded).** Two coding rounds (45 minutes each), one design round (Track A: [ML Systems Design practice prompt](ml-gpu/ML_Systems_Design.md#12-practice-prompts); Track B: [HLD Mock 5: Distributed KV Store](practice/HLD_Mock_Interviews.md#8-mock-5-distributed-key-value-store); Track C: [HLD Mock 6: Search Typeahead](practice/HLD_Mock_Interviews.md#9-mock-6-search-typeahead)), and one 30-minute behavioral round. Use a partner for at least one round this week.

**Exit check.**

- Why does `n & (n - 1)` clear the lowest set bit? Use it to count bits.
- (A) Ring all-reduce time for N GPUs and message size M on link bandwidth B: about 2(N-1)/N x M/B plus latency terms. Say when a tree beats a ring.
- (A) Memory per parameter for mixed-precision Adam without ZeRO (about 16 bytes: 2 for weights, 2 for gradients, 12 for FP32 master weights and two moments), and what ZeRO stages 1-3 shard.
- (B) Explain the ABA problem and one fix.
- (C) Explain what TLS 1.3 saves compared with TLS 1.2 in round trips.

### 5.7 Week 7: Company Lists, Build/Test/Ship, and Full Loops

**Coding (all tracks).** [Design Problems](practice/Coding_Problem_List.md#226-design-problems) (LRU from scratch in under 20 minutes in your interview language), then your target company list: [Google](practice/Coding_Problem_List.md#51-google), [Meta](practice/Coding_Problem_List.md#52-meta), [Amazon](practice/Coding_Problem_List.md#53-amazon), [Microsoft](practice/Coding_Problem_List.md#54-microsoft), or [NVIDIA/AMD/HPC](practice/Coding_Problem_List.md#55-nvidia--amd--hpc-systems-flavored). Tracks A and B add the [concurrency bonus list](practice/Coding_Problem_List.md#41-concurrency-systems-c-and-gpuhpc-loops). Theory: [LeetCode Patterns 26: Design Problems](computer-science/LeetCode_Patterns.md#26-design-problems).

| Block | Track A: GPU/HPC/profiling | Track B: systems C++ / infra | Track C: general SWE |
|---|---|---|---|
| **Fundamentals** | [CMake 64: HIP and ROCm](tools/CMake_Fundamentals.md#64-hip-and-rocm-with-cmake); [CMake 8: PUBLIC/PRIVATE/INTERFACE](tools/CMake_Fundamentals.md#8-target-properties-and-the-publicprivateinterface-model); [Containers 10: ROCm Containers](tools/Containers_and_CI.md#10-running-rocm-containers), [18: Matrix Builds](tools/Containers_and_CI.md#18-matrix-builds-compilers-rocm-versions-and-gpu-architectures), [20: Self-Hosted GPU Runners](tools/Containers_and_CI.md#20-self-hosted-gpu-runners); [Git 12: Bisect](tools/Git_Fundamentals.md#12-bisect-finding-the-commit-that-broke-it) | [CMake 7-11](tools/CMake_Fundamentals.md#7-add_executable-add_library-and-library-types), [28](tools/CMake_Fundamentals.md#28-find_package-module-mode-vs-config-mode), [36-38](tools/CMake_Fundamentals.md#36-the-install-command), [65: RPATH](tools/CMake_Fundamentals.md#65-rpath-and-runpath), [67-68](tools/CMake_Fundamentals.md#67-symbol-visibility-and-export-control); [CPP Testing 19-25](languages/CPP_Testing.md#19-test-doubles) (mocks), [33: Sanitizers](languages/CPP_Testing.md#33-sanitizers-with-googletest), [40: Concurrent Code](languages/CPP_Testing.md#40-testing-concurrent-code); [Git 1-9](tools/Git_Fundamentals.md#1-mental-model-snapshots-a-dag-and-three-trees); [Containers 1-8](tools/Containers_and_CI.md#1-what-a-container-really-is) | [Math 1-4](computer-science/Math_Probability_Estimation.md#1-how-to-approach-math-and-probability-questions) (counting, probability, expectation); [Math 9-10](computer-science/Math_Probability_Estimation.md#9-fermi-estimation) (Fermi estimation, powers of two); [CS Drills 2: Numeric Problems](practice/CS_Fundamentals_Drills.md#2-numeric-problems) |
| **Design / domain** | [ML Systems Design 4: LLM Inference Serving](ml-gpu/ML_Systems_Design.md#4-case-study-llm-inference-serving-platform), [6: GPU Cluster Scheduler](ml-gpu/ML_Systems_Design.md#6-case-study-gpu-cluster-job-scheduler); [ML Frameworks 47: ROCm ML Stack](ml-gpu/ML_AI_Frameworks.md#47-the-rocm-ml-stack), [48: Debugging a Slow Training Step](ml-gpu/ML_AI_Frameworks.md#48-debugging-a-slow-training-step); [Design Patterns C++ 48: Plugin and Registry](design-patterns/Design_Patterns_Cpp.md#48-plugin-and-registry-architecture); [Project Deep Dive 11-13](career/Project_Deep_Dive_rocprof-compute.md#11-likely-interviewer-follow-ups) | [HLD 6.14 Object Storage](computer-science/High_Level_Design.md#614-object-storage-s3-like); [HLD Mock 7: Job Scheduler](practice/HLD_Mock_Interviews.md#10-mock-7-distributed-job-scheduler), [Mock 8: Metrics](practice/HLD_Mock_Interviews.md#11-mock-8-metrics-and-monitoring-system); [LLD 27: Machine-Coding Playbook](design-patterns/Low_Level_Design_Interview_Prep.md#27-machine-coding-round-playbook); optional: [Rust and Go 1-7](languages/Rust_and_Go_for_Cpp_Programmers.md#1-positioning-three-answers-to-the-same-problems), [18](languages/Rust_and_Go_for_Cpp_Programmers.md#18-why-not-rust----a-balanced-answer) | [HLD 7: Checklists and Pitfalls](computer-science/High_Level_Design.md#7-interview-checklists-and-pitfalls); [HLD Mock 14: Unsolved Prompts](practice/HLD_Mock_Interviews.md#14-twenty-unsolved-practice-prompts) (one per day, 30 minutes, outline only); [Interview Loops 3: Company Profiles](career/Interview_Loops_and_Logistics.md#3-company-loop-profiles) |
| **Language drill (Fri)** | [Debugging Tools 21: Cross-Cutting Questions](tools/Debugging_and_Profiling_Tools.md#21-cross-cutting-interview-questions) | [CMake 72: Interview Q&A](tools/CMake_Fundamentals.md#72-interview-questions-and-answers); [CPP Testing 39](languages/CPP_Testing.md#39-interview-questions-and-answers) | [Python Output Quiz](practice/Python_Output_Quiz.md#1-how-to-use-this-quiz) full pass, timed |

**Behavioral (Sunday, all).** [Offer Evaluation](career/Interview_Loops_and_Logistics.md#13-offer-evaluation-compensation-mechanics), [Leveling Equivalences](career/Interview_Loops_and_Logistics.md#14-leveling-equivalences-across-companies), [Negotiation](career/Interview_Loops_and_Logistics.md#15-negotiation-strategy-and-scripts). Prepare [questions to ask](career/Behavioral_Interview_Prep.md#10-questions-to-ask-the-interviewer) for each interviewer type.

**Saturday mock (full loop).** Simulate the real loop of your top target company (4-5 rounds, with breaks of the same length as the real ones). Track A: one round is a domain deep dive driven by [Domain and Deep-Dive Rounds for GPU and HPC Roles](career/Interview_Loops_and_Logistics.md#11-domain-and-deep-dive-rounds-for-gpu-and-hpc-roles) and the [GPU profiling-tools question bank](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#8-interview-qa-for-a-gpu-profiling-tools-role). Track B: one round is a C++ language round from the [C++ quiz](practice/Cpp_Output_Quiz.md) plus a [debug-this-code](career/Interview_Loops_and_Logistics.md#9-debug-this-code-rounds) exercise. Track C: two HLD rounds. Use a partner for at least two rounds.

**Exit check.**

- LRU cache with O(1) get/put from a blank file in under 20 minutes.
- (A) Size a decode-serving deployment: given a KV-cache budget per GPU and bytes per token, how many concurrent sequences of 4K tokens fit? Show the arithmetic.
- (A/B) What does `target_link_libraries(foo PUBLIC bar)` propagate that `PRIVATE` does not?
- (B) `git rebase` vs `git merge` for a shared branch; how to recover a lost commit with the reflog.
- (C) Expected number of rolls of a fair die to see all six faces (6 x H6 = 14.7).

### 5.8 Week 8: Consolidation and Taper

No new material. The goal is retrieval speed and calm.

| Day | Coding | Review (all tracks) | Track-specific review |
|---|---|---|---|
| Mon | retire remaining C/D grades from the [error log](practice/Coding_Problem_List.md#72-error-log-template) | [Night-Before Cheat Sheet](practice/Night_Before_Cheat_Sheet.md) first pass | A: [AMD GPU 8: Q bank](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#8-interview-qa-for-a-gpu-profiling-tools-role); B: [C++ 15: UB](languages/Cpp_Fundamentals.md#15-undefined-behavior-implementation-defined-and-best-practices) Q blocks; C: [HLD 7](computer-science/High_Level_Design.md#7-interview-checklists-and-pitfalls) |
| Tue | **full loop mock** | [Rapid-Fire 100 One-Liners](practice/CS_Fundamentals_Drills.md#3-rapid-fire-100-one-liners) | review mock recording |
| Wed | 3 random retired problems ([picker](practice/Coding_Problem_List.md#92-random-problem-picker)) | [Follow-Up Drill Chains](practice/CS_Fundamentals_Drills.md#4-follow-up-drill-chains) | A: [Project Deep Dive 11: Follow-Ups](career/Project_Deep_Dive_rocprof-compute.md#11-likely-interviewer-follow-ups); B: [Concurrency 18: Pitfalls](computer-science/Concurrency_Coding_Problems.md#18-pitfalls-checklist); C: [HLD Mock 15: Failure Modes](practice/HLD_Mock_Interviews.md#15-common-failure-modes-checklist) |
| Thu | **full loop mock** (partner if possible) | [Flashcards](practice/Flashcards.csv): all cards marked missed | A: [Perf Eng 10: Q&A](computer-science/Performance_Engineering.md#10-interview-qa); B: [Debugging Tools 20: Quick Reference](tools/Debugging_and_Profiling_Tools.md#20-quick-reference-card); C: [Math 11: Quick Reference](computer-science/Math_Probability_Estimation.md#11-quick-reference) |
| Fri | 2 easy-medium problems for confidence | [Rehearsal Plan and Final Checklist](career/Behavioral_Interview_Prep.md#11-rehearsal-plan-and-final-checklist) | pitches aloud: [30-second and 2-minute](career/Project_Deep_Dive_rocprof-compute.md#2-the-pitches) |
| Sat | light: 1 problem | [Preparation Checklists](career/Interview_Loops_and_Logistics.md#17-preparation-checklists); [day-of checklist](career/Behavioral_Interview_Prep.md#112-day-of-checklist) | environment check: editor, camera, audio, [virtual whiteboard](career/Interview_Loops_and_Logistics.md#12-virtual-whiteboarding-for-design-rounds) |
| Sun | rest | [Night-Before Cheat Sheet](practice/Night_Before_Cheat_Sheet.md) final pass (30 min max) | sleep |

**Exit check (readiness).** You are ready when, over the last two weeks: coding-mock rubric scores average at least 13/16 per problem with no dimension at 1; at least 80% of retired problems re-solve at grade A; you can deliver both pitches and five story cards without notes; and design mocks score "hire" on the [rubric](practice/HLD_Mock_Interviews.md#3-evaluation-rubric-by-level) for your target level on at least two of the last three attempts.

**Q1. Why stop learning new material in the last week?**

New material in the final week has the worst return: it will be shallowly encoded, and studying it displaces the retrieval practice that makes known material available under stress. Interview performance at that point is limited by retrieval speed, communication, and fatigue, not by coverage. Full-loop mocks on Tuesday and Thursday also expose stamina problems (the fourth round is usually the weakest) while there is still time to adjust pacing and breaks.

**Q2. An interview gets scheduled for the end of week 5. What changes?**

Switch to the [two-week emergency plan](#6-two-week-emergency-plan) for the last two weeks, but skip its days covering patterns you have already retired. Use the freed slots for the week 6-7 track cells that matter most for that loop (for Track A, usually ML Systems Design sections 4-7 and the domain question bank). Keep at least one full-loop mock.

---

## 6. Two-Week Emergency Plan

Use this when an interview is 14 days away. Assumes about 4 hours a day. The coding spine is the [Core 75](practice/Coding_Problem_List.md#3-core-75-subset) in high-yield order, about 4 problems a day (Track C: 5). **What to skip:** cyclic sort, line sweep, segment and Fenwick trees, advanced graphs, all "Optional" documents in [Section 7.2](#72-track-priorities), and any section whose Q blocks you already answer cold.

| Day | Coding (Core 75 patterns) | Track A | Track B | Track C |
|---|---|---|---|---|
| 1 | [hashing](practice/Coding_Problem_List.md#222-hashing--array-classics), [two pointers](practice/Coding_Problem_List.md#21-two-pointers) | [Project Deep Dive 2-3](career/Project_Deep_Dive_rocprof-compute.md#2-the-pitches) (pitches, problem); story bank: 6 cards ([3.4](career/Behavioral_Interview_Prep.md#34-story-card-template)) | [C++ 3](languages/Cpp_Fundamentals.md#3-memory-management), [5](languages/Cpp_Fundamentals.md#5-move-semantics-and-perfect-forwarding); story bank: 6 cards | [DSA 25-26](computer-science/DSA_Fundamentals.md#25-master-complexity-cheat-sheet); story bank: 6 cards |
| 2 | [sliding window](practice/Coding_Problem_List.md#22-sliding-window), [prefix sum](practice/Coding_Problem_List.md#221-prefix-sum--difference-array) | [AMD GPU 1.1-1.4](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#11-the-cu-at-a-glance), [1.6](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#16-lds-size-banks-and-conflicts), [1.13 Qs](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#113-interview-questions) | [C++ 12](languages/Cpp_Fundamentals.md#12-multithreading-and-concurrency); [CS 6.9](computer-science/CS_Fundamentals.md#69-memory-models-and-visibility) | [HLD 2-3](computer-science/High_Level_Design.md#2-a-repeatable-interview-process) |
| 3 | [binary search](practice/Coding_Problem_List.md#211-modified-binary-search), [stack parsing](practice/Coding_Problem_List.md#224-stack-based-parsing) | [Perf Eng 3: Roofline](computer-science/Performance_Engineering.md#3-roofline-model); [AMD GPU 3](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#3-latency-hiding-quantified) | [Concurrency Coding 8](computer-science/Concurrency_Coding_Problems.md#8-bounded-blocking-queue-leetcode-1188), [11](computer-science/Concurrency_Coding_Problems.md#11-thread-safe-lru-cache), [13](computer-science/Concurrency_Coding_Problems.md#13-thread-pool-with-futures) | [HLD 4](computer-science/High_Level_Design.md#4-architecture-building-blocks); [HLD Mock 1](practice/HLD_Mock_Interviews.md#4-mock-1-url-shortener) |
| 4 | [linked lists](practice/Coding_Problem_List.md#26-in-place-linked-list-reversal), [fast/slow](practice/Coding_Problem_List.md#23-fast-and-slow-pointers), [intervals](practice/Coding_Problem_List.md#24-merge-intervals) | [AMD GPU 4-5](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#4-rocm-profiling-tools) (tools, counters) | [C++ 15: UB](languages/Cpp_Fundamentals.md#15-undefined-behavior-implementation-defined-and-best-practices); [C++ quiz 2-6](practice/Cpp_Output_Quiz.md#2-object-model-inheritance-and-layout) | [HLD 5](computer-science/High_Level_Design.md#5-cross-cutting-design-decisions); [HLD 6.3](computer-science/High_Level_Design.md#63-news-feed) |
| 5 | [DFS](practice/Coding_Problem_List.md#28-dfs-depth-first-search) (trees) | [AMD GPU 6](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#6-how-gpu-profilers-work-internally) (profiler internals); [Project Deep Dive 6-7](career/Project_Deep_Dive_rocprof-compute.md#6-profile-mode-and-counter-collection) | [LLD 2](design-patterns/Low_Level_Design_Interview_Prep.md#2-a-repeatable-interview-method), [11](design-patterns/Low_Level_Design_Interview_Prep.md#11-worked-design-cache) | [LLD 2](design-patterns/Low_Level_Design_Interview_Prep.md#2-a-repeatable-interview-method), [5](design-patterns/Low_Level_Design_Interview_Prep.md#5-worked-design-parking-lot) |
| 6 | [BFS](practice/Coding_Problem_List.md#27-bfs-breadth-first-search), [topological sort](practice/Coding_Problem_List.md#214-topological-sort), [union-find](practice/Coding_Problem_List.md#216-union-find-disjoint-set) | [Kernel Case Studies 1](ml-gpu/GPU_Kernel_Case_Studies.md#1-reduction-ladder), [6](ml-gpu/GPU_Kernel_Case_Studies.md#6-tiled-gemm-progression) | [HLD 2-4](computer-science/High_Level_Design.md#2-a-repeatable-interview-process) | [CS 1.1-1.4](computer-science/CS_Fundamentals.md#11-processes-and-threads); [CS 6.1-6.4](computer-science/CS_Fundamentals.md#61-threads-vs-processes) |
| 7 | **mock**: two mediums in 45 min + re-solves | **mock**: [10-minute walkthrough](career/Project_Deep_Dive_rocprof-compute.md#23-10-minute-walkthrough-whiteboard-plan) | **mock**: [HLD Mock 5](practice/HLD_Mock_Interviews.md#8-mock-5-distributed-key-value-store) | **mock**: [HLD Mock 3](practice/HLD_Mock_Interviews.md#6-mock-3-news-feed) |
| 8 | [heaps / top K](practice/Coding_Problem_List.md#212-top-k-elements), [K-way merge](practice/Coding_Problem_List.md#213-k-way-merge) | [ML Systems Design 2-3](ml-gpu/ML_Systems_Design.md#2-a-framework-for-ml-and-hpc-design-interviews), [7](ml-gpu/ML_Systems_Design.md#7-case-study-fleet-wide-gpu-profiling-and-telemetry-service) | [CS 1.10](computer-science/CS_Fundamentals.md#110-io-multiplexing-and-event-driven-servers), [1.11](computer-science/CS_Fundamentals.md#111-linux-memory-management-internals); [CS 2.9](computer-science/CS_Fundamentals.md#29-tcp-internals-deep-dive) | [CS 3.4-3.5](computer-science/CS_Fundamentals.md#34-indexing); [CS 8.1-8.2](computer-science/CS_Fundamentals.md#81-consistency-models) |
| 9 | [backtracking](practice/Coding_Problem_List.md#210-subsets--backtracking), [monotonic stack](practice/Coding_Problem_List.md#215-monotonic-stack--queue) | [LLM 7-9](ml-gpu/LLM_and_ML_Fundamentals.md#7-flop-accounting-and-scaling-laws); [ML Systems Design 4](ml-gpu/ML_Systems_Design.md#4-case-study-llm-inference-serving-platform) | [CS 8.12-8.13](computer-science/CS_Fundamentals.md#812-consensus-theory-and-raft-in-depth); [HLD 6.12](computer-science/High_Level_Design.md#612-distributed-job-scheduler) | [HLD 6.4](computer-science/High_Level_Design.md#64-chat-system), [6.9](computer-science/High_Level_Design.md#69-search-autocomplete-typeahead) |
| 10 | [DP](practice/Coding_Problem_List.md#218-dynamic-programming) (1-D) | [Parallel GPU 34](ml-gpu/Parallel_GPU_Programming.md#34-collective-communication-algorithms-and-cost-model); [ML Frameworks 45](ml-gpu/ML_AI_Frameworks.md#45-training-memory-math-zero-activations-and-offload) | [Perf Eng 5](computer-science/Performance_Engineering.md#5-memory-hierarchy-programming); [Debugging Tools 8-11](tools/Debugging_and_Profiling_Tools.md#8-perf-fundamentals-and-hardware-counters) | [Behavioral 4](career/Behavioral_Interview_Prep.md#4-mapping-stories-to-company-values) for the target company |
| 11 | [DP](practice/Coding_Problem_List.md#218-dynamic-programming) (2-D), [greedy](practice/Coding_Problem_List.md#219-greedy) | [AMD GPU 8: Q bank](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#8-interview-qa-for-a-gpu-profiling-tools-role) | [Design Patterns C++ 39-43](design-patterns/Design_Patterns_Cpp.md#39-producer-consumer); [C++ 16](languages/Cpp_Fundamentals.md#16-implement-from-scratch-exercises) (`unique_ptr`) | [Python quiz](practice/Python_Output_Quiz.md#1-how-to-use-this-quiz) |
| 12 | [bits](practice/Coding_Problem_List.md#220-bit-manipulation), [design: LRU](practice/Coding_Problem_List.md#226-design-problems); A/B: [concurrency bonus](practice/Coding_Problem_List.md#41-concurrency-systems-c-and-gpuhpc-loops) | [Project Deep Dive 10-11](career/Project_Deep_Dive_rocprof-compute.md#10-key-design-tradeoffs); [Behavioral 6](career/Behavioral_Interview_Prep.md#6-frameworks-for-failure-and-conflict-answers) | [Behavioral 6](career/Behavioral_Interview_Prep.md#6-frameworks-for-failure-and-conflict-answers); [HLD 7](computer-science/High_Level_Design.md#7-interview-checklists-and-pitfalls) | [Behavioral 6](career/Behavioral_Interview_Prep.md#6-frameworks-for-failure-and-conflict-answers); [HLD 7](computer-science/High_Level_Design.md#7-interview-checklists-and-pitfalls) |
| 13 | **full loop mock** (all rounds of the target loop) | domain round as part of the loop | C++ language round as part of the loop | two HLD rounds as part of the loop |
| 14 | 2 easy re-solves only | [Night-Before Cheat Sheet](practice/Night_Before_Cheat_Sheet.md); [day-of checklist](career/Behavioral_Interview_Prep.md#112-day-of-checklist) | same | same |

Every day also includes: re-solves due, 15 minutes of [Flashcards](practice/Flashcards.csv), and one story told aloud. Behavioral needs about 5 hours in total across the two weeks; the [two-week behavioral plan](career/Behavioral_Interview_Prep.md#111-a-two-week-plan) fits inside the daily story slot.

**Q1. With only two weeks, should I still do re-solves?**

Yes, but compress the schedule: re-solve every C/D grade on day+1 and day+4 instead of day 3 and day 14 (there is no day 14). A problem you failed once and re-solved twice is far more likely to transfer to a variant in the interview than two new problems you saw once. If time collapses, cut new problems on days 8-11 down to the Core 75 items tagged for your target company.

**Q2. Track A with two weeks: which single document gives the most return?**

[AMD GPU Architecture and Profiling](ml-gpu/AMD_GPU_Architecture_and_Profiling.md), sections 1, 3, 5, and 6, plus the [Project Deep Dive](career/Project_Deep_Dive_rocprof-compute.md). Together they cover the domain round and the project round, which for a profiling-tools role are usually the rounds that decide the level. Coding rounds are typically pass/fail filters; domain depth is where an internal-tools engineer stands out.

---

## 7. Round-to-Document Map and Track Priorities

### 7.1 Round-to-document map

| Interview round | Read | Practice |
|---|---|---|
| Coding (DSA) | [LeetCode Patterns](computer-science/LeetCode_Patterns.md), [DSA Fundamentals](computer-science/DSA_Fundamentals.md) | [Coding Problem List](practice/Coding_Problem_List.md) |
| Concurrency coding | [CS 6](computer-science/CS_Fundamentals.md#6-concurrency-and-multithreading), [C++ 12](languages/Cpp_Fundamentals.md#12-multithreading-and-concurrency) | [Concurrency Coding Problems](computer-science/Concurrency_Coding_Problems.md) |
| C++ language depth | [C++ Fundamentals](languages/Cpp_Fundamentals.md), [Design Patterns C++](design-patterns/Design_Patterns_Cpp.md) | [C++ Output Quiz](practice/Cpp_Output_Quiz.md), [C++ 16 exercises](languages/Cpp_Fundamentals.md#16-implement-from-scratch-exercises) |
| Python language depth | [Python Fundamentals](languages/Python_Fundamentals.md), [Design Patterns Python](design-patterns/Design_Patterns_Python.md) | [Python Output Quiz](practice/Python_Output_Quiz.md) |
| Data / SQL | [CS 3](computer-science/CS_Fundamentals.md#3-database-systems), [Pandas](languages/Pandas.md) | [SQL and Pandas Exercises](practice/SQL_and_Pandas_Exercises.md) |
| CS fundamentals rapid-fire | [CS Fundamentals](computer-science/CS_Fundamentals.md), [Performance Engineering](computer-science/Performance_Engineering.md) | [CS Fundamentals Drills](practice/CS_Fundamentals_Drills.md), [Flashcards](practice/Flashcards.csv) |
| Low-level design / machine coding | [LLD Interview Prep](design-patterns/Low_Level_Design_Interview_Prep.md) | [Machine-coding playbook](design-patterns/Low_Level_Design_Interview_Prep.md#27-machine-coding-round-playbook) |
| High-level design | [High Level Design](computer-science/High_Level_Design.md), [CS 5](computer-science/CS_Fundamentals.md#5-system-design), [CS 8](computer-science/CS_Fundamentals.md#8-distributed-systems) | [HLD Mock Interviews](practice/HLD_Mock_Interviews.md) |
| ML / HPC systems design | [ML Systems Design](ml-gpu/ML_Systems_Design.md), [ML AI Frameworks](ml-gpu/ML_AI_Frameworks.md), [LLM and ML Fundamentals](ml-gpu/LLM_and_ML_Fundamentals.md) | [ML Systems practice prompts](ml-gpu/ML_Systems_Design.md#12-practice-prompts), [HLD Mocks 9-10](practice/HLD_Mock_Interviews.md#12-mock-9-gpu-profiling-telemetry-service) |
| GPU / HPC domain | [AMD GPU Architecture and Profiling](ml-gpu/AMD_GPU_Architecture_and_Profiling.md), [Parallel GPU Programming](ml-gpu/Parallel_GPU_Programming.md), [Performance Engineering](computer-science/Performance_Engineering.md) | [GPU Kernel Case Studies](ml-gpu/GPU_Kernel_Case_Studies.md), [kernel exercise list](ml-gpu/GPU_Kernel_Case_Studies.md#8-kernel-exercise-list) |
| Project deep dive | [Project Deep Dive: rocprof-compute](career/Project_Deep_Dive_rocprof-compute.md) | [Rehearsal checklist](career/Project_Deep_Dive_rocprof-compute.md#13-rehearsal-checklist-and-pitfalls) |
| Debugging / tooling / infra | [Debugging and Profiling Tools](tools/Debugging_and_Profiling_Tools.md), [Linux Command Line](tools/Linux_Command_Line.md), [CMake](tools/CMake_Fundamentals.md), [Git](tools/Git_Fundamentals.md), [Containers and CI](tools/Containers_and_CI.md), [CPP Testing](languages/CPP_Testing.md) | [Production scenarios](tools/Debugging_and_Profiling_Tools.md#19-production-debugging-scenarios), [Linux troubleshooting](tools/Linux_Command_Line.md#17-troubleshooting-scenarios), [Containers scenarios](tools/Containers_and_CI.md#24-scenario-interview-questions) |
| Behavioral | [Behavioral Interview Prep](career/Behavioral_Interview_Prep.md) | [Rehearsal plan](career/Behavioral_Interview_Prep.md#11-rehearsal-plan-and-final-checklist) |
| Process, offers | [Interview Loops and Logistics](career/Interview_Loops_and_Logistics.md) | [Preparation checklists](career/Interview_Loops_and_Logistics.md#17-preparation-checklists) |
| Math / probability / estimation | [Math, Probability, Estimation](computer-science/Math_Probability_Estimation.md) | [Classic puzzles](computer-science/Math_Probability_Estimation.md#7-classic-probability-puzzles) |
| Other languages | [Rust and Go for C++ Programmers](languages/Rust_and_Go_for_Cpp_Programmers.md) | [Cross-cutting Q&A](languages/Rust_and_Go_for_Cpp_Programmers.md#19-cross-cutting-interview-qa) |

### 7.2 Track priorities

**Core** = finish all sections and all Q blocks. **Rec.** = read the sections named in the week tables and answer every Q block. **Opt.** = reference only.

| Document | A | B | C |
|---|---|---|---|
| [Behavioral Interview Prep](career/Behavioral_Interview_Prep.md) | Core | Core | Core |
| [Project Deep Dive: rocprof-compute](career/Project_Deep_Dive_rocprof-compute.md) | Core | Rec. | Opt. (use as a template for your own project) |
| [Interview Loops and Logistics](career/Interview_Loops_and_Logistics.md) | Core | Core | Core |
| [CS Fundamentals](computer-science/CS_Fundamentals.md) | Core (1, 6, 7) | Core | Core |
| [DSA Fundamentals](computer-science/DSA_Fundamentals.md) | Rec. | Rec. | Core |
| [LeetCode Patterns](computer-science/LeetCode_Patterns.md) | Core (patterns 1-26) | Core (patterns 1-26) | Core |
| [High Level Design](computer-science/High_Level_Design.md) | Rec. | Core | Core |
| [Performance Engineering](computer-science/Performance_Engineering.md) | Core | Core | Opt. |
| [Concurrency Coding Problems](computer-science/Concurrency_Coding_Problems.md) | Core | Core | Rec. |
| [Math, Probability, Estimation](computer-science/Math_Probability_Estimation.md) | Opt. | Opt. | Rec. |
| [Design Patterns C++](design-patterns/Design_Patterns_Cpp.md) | Rec. | Core | Opt. |
| [Design Patterns Python](design-patterns/Design_Patterns_Python.md) | Opt. | Opt. | Rec. |
| [LLD Interview Prep](design-patterns/Low_Level_Design_Interview_Prep.md) | Rec. | Core | Core |
| [C++ Fundamentals](languages/Cpp_Fundamentals.md) | Core | Core | Rec. (Core if coding in C++) |
| [CPP Testing](languages/CPP_Testing.md) | Rec. | Rec. | Opt. |
| [Python Fundamentals](languages/Python_Fundamentals.md) | Rec. | Opt. | Core (if coding in Python) |
| [Python Libraries](languages/Python_Libraries.md) | Rec. (NumPy 1-12) | Opt. | Opt. |
| [Pandas](languages/Pandas.md) | Rec. (rocprof-compute analysis is pandas-based) | Opt. | Opt. |
| [Rust and Go for C++ Programmers](languages/Rust_and_Go_for_Cpp_Programmers.md) | Opt. | Rec. | Opt. |
| [ML AI Frameworks](ml-gpu/ML_AI_Frameworks.md) | Rec. (1-2, 7-8, 25-28, 45-48) | Opt. | Opt. |
| [Parallel GPU Programming](ml-gpu/Parallel_GPU_Programming.md) | Core | Opt. | Opt. |
| [AMD GPU Architecture and Profiling](ml-gpu/AMD_GPU_Architecture_and_Profiling.md) | Core | Opt. | Opt. |
| [GPU Kernel Case Studies](ml-gpu/GPU_Kernel_Case_Studies.md) | Core | Opt. | Opt. |
| [LLM and ML Fundamentals](ml-gpu/LLM_and_ML_Fundamentals.md) | Rec. | Opt. | Opt. |
| [ML Systems Design](ml-gpu/ML_Systems_Design.md) | Core | Opt. (Rec. for ML infra) | Opt. |
| [Coding Problem List](practice/Coding_Problem_List.md) | Core | Core | Core |
| [C++ Output Quiz](practice/Cpp_Output_Quiz.md) | Core | Core | Opt. |
| [Python Output Quiz](practice/Python_Output_Quiz.md) | Rec. | Opt. | Rec. |
| [SQL and Pandas Exercises](practice/SQL_and_Pandas_Exercises.md) | Opt. | Opt. | Rec. |
| [CS Fundamentals Drills](practice/CS_Fundamentals_Drills.md) | Core | Core | Core |
| [HLD Mock Interviews](practice/HLD_Mock_Interviews.md) | Rec. (Mocks 9-10 Core) | Core | Core |
| [Flashcards](practice/Flashcards.csv) | Core | Core | Core |
| [Night-Before Cheat Sheet](practice/Night_Before_Cheat_Sheet.md) | Core | Core | Core |
| [CMake Fundamentals](tools/CMake_Fundamentals.md) | Rec. | Core | Opt. |
| [Git Fundamentals](tools/Git_Fundamentals.md) | Rec. | Rec. | Rec. |
| [Linux Command Line](tools/Linux_Command_Line.md) | Core | Core | Rec. |
| [Debugging and Profiling Tools](tools/Debugging_and_Profiling_Tools.md) | Core | Core | Opt. |
| [Containers and CI](tools/Containers_and_CI.md) | Rec. | Rec. | Opt. |

---

## 8. Per-Document Progress Checklist

Tick a box only when the section meets the "done" bar in [Section 1](#1-how-to-use-this-plan): Q blocks answered cold, key table explained from memory, central code re-typed. Optionally append the date and a confidence score, for example `- [x] ... (2026-11-12, 4/5)`. Untick a box if a later self-assessment or mock shows the section has decayed.

### 8.1 career

**[Behavioral Interview Prep](career/Behavioral_Interview_Prep.md)**

- [ ] [1. What Behavioral Rounds Assess](career/Behavioral_Interview_Prep.md#1-what-behavioral-rounds-assess)
- [ ] [2. Answer Formats: STAR and CARL](career/Behavioral_Interview_Prep.md#2-answer-formats-star-and-carl)
- [ ] [3. Building Your Story Bank](career/Behavioral_Interview_Prep.md#3-building-your-story-bank)
- [ ] [4. Mapping Stories to Company Values](career/Behavioral_Interview_Prep.md#4-mapping-stories-to-company-values)
- [ ] [5. Question Bank by Competency](career/Behavioral_Interview_Prep.md#5-question-bank-by-competency)
- [ ] [6. Frameworks for Failure and Conflict Answers](career/Behavioral_Interview_Prep.md#6-frameworks-for-failure-and-conflict-answers)
- [ ] [7. Tell Me About Yourself: The 90-Second Template](career/Behavioral_Interview_Prep.md#7-tell-me-about-yourself-the-90-second-template)
- [ ] [8. Senior and Staff-Level Signals](career/Behavioral_Interview_Prep.md#8-senior-and-staff-level-signals)
- [ ] [9. Anti-Patterns](career/Behavioral_Interview_Prep.md#9-anti-patterns)
- [ ] [10. Questions to Ask the Interviewer](career/Behavioral_Interview_Prep.md#10-questions-to-ask-the-interviewer)
- [ ] [11. Rehearsal Plan and Final Checklist](career/Behavioral_Interview_Prep.md#11-rehearsal-plan-and-final-checklist)

**[Project Deep Dive: rocprof-compute](career/Project_Deep_Dive_rocprof-compute.md)**

- [ ] [1. How to Use This Document](career/Project_Deep_Dive_rocprof-compute.md#1-how-to-use-this-document)
- [ ] [2. The Pitches](career/Project_Deep_Dive_rocprof-compute.md#2-the-pitches)
- [ ] [3. What Problem It Solves](career/Project_Deep_Dive_rocprof-compute.md#3-what-problem-it-solves)
- [ ] [4. History and Version Timeline](career/Project_Deep_Dive_rocprof-compute.md#4-history-and-version-timeline)
- [ ] [5. Architecture Overview](career/Project_Deep_Dive_rocprof-compute.md#5-architecture-overview)
- [ ] [6. Profile Mode and Counter Collection](career/Project_Deep_Dive_rocprof-compute.md#6-profile-mode-and-counter-collection)
- [ ] [7. Analyze Mode and the Metric Engine](career/Project_Deep_Dive_rocprof-compute.md#7-analyze-mode-and-the-metric-engine)
- [ ] [8. Speed-of-Light, Memory Chart, and Roofline](career/Project_Deep_Dive_rocprof-compute.md#8-speed-of-light-memory-chart-and-roofline)
- [ ] [9. User Interfaces and Outputs](career/Project_Deep_Dive_rocprof-compute.md#9-user-interfaces-and-outputs)
- [ ] [10. Key Design Tradeoffs](career/Project_Deep_Dive_rocprof-compute.md#10-key-design-tradeoffs)
- [ ] [11. Likely Interviewer Follow-Ups](career/Project_Deep_Dive_rocprof-compute.md#11-likely-interviewer-follow-ups)
- [ ] [12. Your Story Templates](career/Project_Deep_Dive_rocprof-compute.md#12-your-story-templates)
- [ ] [13. Rehearsal Checklist and Pitfalls](career/Project_Deep_Dive_rocprof-compute.md#13-rehearsal-checklist-and-pitfalls)
- [ ] [14. Glossary](career/Project_Deep_Dive_rocprof-compute.md#14-glossary)

**[Interview Loops and Logistics](career/Interview_Loops_and_Logistics.md)**

- [ ] [1. How to Use This Guide](career/Interview_Loops_and_Logistics.md#1-how-to-use-this-guide)
- [ ] [2. Anatomy of a Tech Interview Loop](career/Interview_Loops_and_Logistics.md#2-anatomy-of-a-tech-interview-loop)
- [ ] [3. Company Loop Profiles](career/Interview_Loops_and_Logistics.md#3-company-loop-profiles)
- [ ] [4. Online Assessments](career/Interview_Loops_and_Logistics.md#4-online-assessments)
- [ ] [5. Take-Home Assignments](career/Interview_Loops_and_Logistics.md#5-take-home-assignments)
- [ ] [6. Live-Coding Environment Etiquette](career/Interview_Loops_and_Logistics.md#6-live-coding-environment-etiquette)
- [ ] [7. The Coding-Round Communication Framework](career/Interview_Loops_and_Logistics.md#7-the-coding-round-communication-framework)
- [ ] [8. Worked Coding Round: Subarray Sum Equals K](career/Interview_Loops_and_Logistics.md#8-worked-coding-round-subarray-sum-equals-k)
- [ ] [9. Debug-This-Code Rounds](career/Interview_Loops_and_Logistics.md#9-debug-this-code-rounds)
- [ ] [10. Code-Review Rounds](career/Interview_Loops_and_Logistics.md#10-code-review-rounds)
- [ ] [11. Domain and Deep-Dive Rounds for GPU and HPC Roles](career/Interview_Loops_and_Logistics.md#11-domain-and-deep-dive-rounds-for-gpu-and-hpc-roles)
- [ ] [12. Virtual Whiteboarding for Design Rounds](career/Interview_Loops_and_Logistics.md#12-virtual-whiteboarding-for-design-rounds)
- [ ] [13. Offer Evaluation: Compensation Mechanics](career/Interview_Loops_and_Logistics.md#13-offer-evaluation-compensation-mechanics)
- [ ] [14. Leveling Equivalences Across Companies](career/Interview_Loops_and_Logistics.md#14-leveling-equivalences-across-companies)
- [ ] [15. Negotiation Strategy and Scripts](career/Interview_Loops_and_Logistics.md#15-negotiation-strategy-and-scripts)
- [ ] [16. Questions to Ask Your Interviewers](career/Interview_Loops_and_Logistics.md#16-questions-to-ask-your-interviewers)
- [ ] [17. Preparation Checklists](career/Interview_Loops_and_Logistics.md#17-preparation-checklists)

### 8.2 computer-science

**[CS Fundamentals](computer-science/CS_Fundamentals.md)**

- [ ] [1. Operating Systems](computer-science/CS_Fundamentals.md#1-operating-systems)
    - [ ] [1.1 Processes and Threads](computer-science/CS_Fundamentals.md#11-processes-and-threads)
    - [ ] [1.2 CPU Scheduling](computer-science/CS_Fundamentals.md#12-cpu-scheduling)
    - [ ] [1.3 Memory Management](computer-science/CS_Fundamentals.md#13-memory-management)
    - [ ] [1.4 Deadlocks](computer-science/CS_Fundamentals.md#14-deadlocks)
    - [ ] [1.5 File Systems](computer-science/CS_Fundamentals.md#15-file-systems)
    - [ ] [1.6 Inter-Process Communication (IPC)](computer-science/CS_Fundamentals.md#16-inter-process-communication-ipc)
    - [ ] [1.7 System Calls](computer-science/CS_Fundamentals.md#17-system-calls)
    - [ ] [1.8 I/O Systems](computer-science/CS_Fundamentals.md#18-io-systems)
    - [ ] [1.9 Linux Process Lifecycle, Signals, and File Descriptors](computer-science/CS_Fundamentals.md#19-linux-process-lifecycle-signals-and-file-descriptors)
    - [ ] [1.10 I/O Multiplexing and Event-Driven Servers](computer-science/CS_Fundamentals.md#110-io-multiplexing-and-event-driven-servers)
    - [ ] [1.11 Linux Memory Management Internals](computer-science/CS_Fundamentals.md#111-linux-memory-management-internals)
    - [ ] [1.12 The Linux Scheduler](computer-science/CS_Fundamentals.md#112-the-linux-scheduler)
    - [ ] [1.13 Containers and Virtualization: Isolation Theory](computer-science/CS_Fundamentals.md#113-containers-and-virtualization-isolation-theory)
    - [ ] [1.14 Operating Systems -- Interview Questions](computer-science/CS_Fundamentals.md#114-operating-systems----interview-questions)
- [ ] [2. Computer Networks](computer-science/CS_Fundamentals.md#2-computer-networks)
    - [ ] [2.1 OSI Model and TCP/IP Model](computer-science/CS_Fundamentals.md#21-osi-model-and-tcpip-model)
    - [ ] [2.2 TCP vs UDP](computer-science/CS_Fundamentals.md#22-tcp-vs-udp)
    - [ ] [2.3 HTTP / HTTPS](computer-science/CS_Fundamentals.md#23-http--https)
    - [ ] [2.4 DNS (Domain Name System)](computer-science/CS_Fundamentals.md#24-dns-domain-name-system)
    - [ ] [2.5 IP Addressing](computer-science/CS_Fundamentals.md#25-ip-addressing)
    - [ ] [2.6 Routing](computer-science/CS_Fundamentals.md#26-routing)
    - [ ] [2.7 Application Layer Protocols](computer-science/CS_Fundamentals.md#27-application-layer-protocols)
    - [ ] [2.8 TLS/SSL Handshake](computer-science/CS_Fundamentals.md#28-tlsssl-handshake)
    - [ ] [2.9 TCP Internals Deep Dive](computer-science/CS_Fundamentals.md#29-tcp-internals-deep-dive)
    - [ ] [2.10 HPC and Datacenter Interconnects](computer-science/CS_Fundamentals.md#210-hpc-and-datacenter-interconnects)
    - [ ] [2.11 Computer Networks -- Interview Questions](computer-science/CS_Fundamentals.md#211-computer-networks----interview-questions)
- [ ] [3. Database Systems](computer-science/CS_Fundamentals.md#3-database-systems)
    - [ ] [3.1 Relational Database Concepts](computer-science/CS_Fundamentals.md#31-relational-database-concepts)
    - [ ] [3.2 SQL Essentials](computer-science/CS_Fundamentals.md#32-sql-essentials)
    - [ ] [3.3 Normalization](computer-science/CS_Fundamentals.md#33-normalization)
    - [ ] [3.4 Indexing](computer-science/CS_Fundamentals.md#34-indexing)
    - [ ] [3.5 Transactions and ACID](computer-science/CS_Fundamentals.md#35-transactions-and-acid)
    - [ ] [3.6 NoSQL Databases](computer-science/CS_Fundamentals.md#36-nosql-databases)
    - [ ] [3.7 CAP Theorem and PACELC](computer-science/CS_Fundamentals.md#37-cap-theorem-and-pacelc)
    - [ ] [3.8 Sharding, Replication, and Partitioning](computer-science/CS_Fundamentals.md#38-sharding-replication-and-partitioning)
    - [ ] [3.9 Storage Engine Internals](computer-science/CS_Fundamentals.md#39-storage-engine-internals)
    - [ ] [3.10 Concurrency Control in Depth](computer-science/CS_Fundamentals.md#310-concurrency-control-in-depth)
    - [ ] [3.11 Database Systems -- Interview Questions](computer-science/CS_Fundamentals.md#311-database-systems----interview-questions)
- [ ] [4. Object-Oriented Programming and Design Patterns](computer-science/CS_Fundamentals.md#4-object-oriented-programming-and-design-patterns)
    - [ ] [4.1 Four Pillars of OOP](computer-science/CS_Fundamentals.md#41-four-pillars-of-oop)
    - [ ] [4.2 SOLID Principles](computer-science/CS_Fundamentals.md#42-solid-principles)
    - [ ] [4.3 Design Patterns at a Glance](computer-science/CS_Fundamentals.md#43-design-patterns-at-a-glance)
    - [ ] [4.4 Composition vs Inheritance](computer-science/CS_Fundamentals.md#44-composition-vs-inheritance)
    - [ ] [4.5 Coupling and Cohesion](computer-science/CS_Fundamentals.md#45-coupling-and-cohesion)
    - [ ] [4.6 OOP & Design Patterns -- Interview Questions](computer-science/CS_Fundamentals.md#46-oop--design-patterns----interview-questions)
- [ ] [5. System Design](computer-science/CS_Fundamentals.md#5-system-design)
    - [ ] [5.1 Scalability](computer-science/CS_Fundamentals.md#51-scalability)
    - [ ] [5.2 Load Balancing](computer-science/CS_Fundamentals.md#52-load-balancing)
    - [ ] [5.3 Caching](computer-science/CS_Fundamentals.md#53-caching)
    - [ ] [5.4 Content Delivery Network (CDN)](computer-science/CS_Fundamentals.md#54-content-delivery-network-cdn)
    - [ ] [5.5 Message Queues](computer-science/CS_Fundamentals.md#55-message-queues)
    - [ ] [5.6 Microservices vs Monolith](computer-science/CS_Fundamentals.md#56-microservices-vs-monolith)
    - [ ] [5.7 API Design](computer-science/CS_Fundamentals.md#57-api-design)
    - [ ] [5.8 Consistent Hashing](computer-science/CS_Fundamentals.md#58-consistent-hashing)
    - [ ] [5.9 Back-of-the-Envelope Estimation](computer-science/CS_Fundamentals.md#59-back-of-the-envelope-estimation)
    - [ ] [5.10 Observability and Production Debugging](computer-science/CS_Fundamentals.md#510-observability-and-production-debugging)
    - [ ] [5.11 System Design -- Interview Questions](computer-science/CS_Fundamentals.md#511-system-design----interview-questions)
- [ ] [6. Concurrency and Multithreading](computer-science/CS_Fundamentals.md#6-concurrency-and-multithreading)
    - [ ] [6.1 Threads vs Processes](computer-science/CS_Fundamentals.md#61-threads-vs-processes)
    - [ ] [6.2 Synchronization Primitives](computer-science/CS_Fundamentals.md#62-synchronization-primitives)
    - [ ] [6.3 Race Conditions and Critical Sections](computer-science/CS_Fundamentals.md#63-race-conditions-and-critical-sections)
    - [ ] [6.4 Deadlock, Livelock, and Starvation](computer-science/CS_Fundamentals.md#64-deadlock-livelock-and-starvation)
    - [ ] [6.5 Classic Concurrency Problems](computer-science/CS_Fundamentals.md#65-classic-concurrency-problems)
    - [ ] [6.6 Thread Pools and Executors](computer-science/CS_Fundamentals.md#66-thread-pools-and-executors)
    - [ ] [6.7 Async/Await and Event Loops](computer-science/CS_Fundamentals.md#67-asyncawait-and-event-loops)
    - [ ] [6.8 Lock-Free and Wait-Free Data Structures](computer-science/CS_Fundamentals.md#68-lock-free-and-wait-free-data-structures)
    - [ ] [6.9 Memory Models and Visibility](computer-science/CS_Fundamentals.md#69-memory-models-and-visibility)
    - [ ] [6.10 Lock Implementation Internals](computer-science/CS_Fundamentals.md#610-lock-implementation-internals)
    - [ ] [6.11 Concurrency and Multithreading -- Interview Questions](computer-science/CS_Fundamentals.md#611-concurrency-and-multithreading----interview-questions)
- [ ] [7. Computer Architecture](computer-science/CS_Fundamentals.md#7-computer-architecture)
    - [ ] [7.1 CPU Basics](computer-science/CS_Fundamentals.md#71-cpu-basics)
    - [ ] [7.2 Instruction Set Architecture (ISA)](computer-science/CS_Fundamentals.md#72-instruction-set-architecture-isa)
    - [ ] [7.3 Pipelining](computer-science/CS_Fundamentals.md#73-pipelining)
    - [ ] [7.4 Memory Hierarchy](computer-science/CS_Fundamentals.md#74-memory-hierarchy)
    - [ ] [7.5 Cache](computer-science/CS_Fundamentals.md#75-cache)
    - [ ] [7.6 Virtual Memory](computer-science/CS_Fundamentals.md#76-virtual-memory)
    - [ ] [7.7 Storage](computer-science/CS_Fundamentals.md#77-storage)
    - [ ] [7.8 Parallelism](computer-science/CS_Fundamentals.md#78-parallelism)
    - [ ] [7.9 Endianness and Floating Point](computer-science/CS_Fundamentals.md#79-endianness-and-floating-point)
    - [ ] [7.10 Out-of-Order Superscalar Microarchitecture](computer-science/CS_Fundamentals.md#710-out-of-order-superscalar-microarchitecture)
    - [ ] [7.11 Computer Architecture -- Interview Questions](computer-science/CS_Fundamentals.md#711-computer-architecture----interview-questions)
- [ ] [8. Distributed Systems](computer-science/CS_Fundamentals.md#8-distributed-systems)
    - [ ] [8.1 Consistency Models](computer-science/CS_Fundamentals.md#81-consistency-models)
    - [ ] [8.2 Consensus Algorithms](computer-science/CS_Fundamentals.md#82-consensus-algorithms)
    - [ ] [8.3 Replication Strategies](computer-science/CS_Fundamentals.md#83-replication-strategies)
    - [ ] [8.4 Partitioning / Sharding](computer-science/CS_Fundamentals.md#84-partitioning--sharding)
    - [ ] [8.5 Distributed Transactions](computer-science/CS_Fundamentals.md#85-distributed-transactions)
    - [ ] [8.6 Clock Synchronization and Ordering](computer-science/CS_Fundamentals.md#86-clock-synchronization-and-ordering)
    - [ ] [8.7 Failure Detection](computer-science/CS_Fundamentals.md#87-failure-detection)
    - [ ] [8.8 MapReduce](computer-science/CS_Fundamentals.md#88-mapreduce)
    - [ ] [8.9 Gossip Protocol](computer-science/CS_Fundamentals.md#89-gossip-protocol)
    - [ ] [8.10 Resilience Patterns](computer-science/CS_Fundamentals.md#810-resilience-patterns)
    - [ ] [8.11 Key Distributed Systems](computer-science/CS_Fundamentals.md#811-key-distributed-systems)
    - [ ] [8.12 Consensus Theory and Raft in Depth](computer-science/CS_Fundamentals.md#812-consensus-theory-and-raft-in-depth)
    - [ ] [8.13 Consistency Guarantees, Split Brain, Leases, and Fencing](computer-science/CS_Fundamentals.md#813-consistency-guarantees-split-brain-leases-and-fencing)
    - [ ] [8.14 Distributed Systems -- Interview Questions](computer-science/CS_Fundamentals.md#814-distributed-systems----interview-questions)
- [ ] [9. Security](computer-science/CS_Fundamentals.md#9-security)
    - [ ] [9.1 Symmetric vs Asymmetric Encryption](computer-science/CS_Fundamentals.md#91-symmetric-vs-asymmetric-encryption)
    - [ ] [9.2 Hashing](computer-science/CS_Fundamentals.md#92-hashing)
    - [ ] [9.3 TLS/SSL](computer-science/CS_Fundamentals.md#93-tlsssl)
    - [ ] [9.4 Authentication](computer-science/CS_Fundamentals.md#94-authentication)
    - [ ] [9.5 Authorization](computer-science/CS_Fundamentals.md#95-authorization)
    - [ ] [9.6 Common Vulnerabilities (OWASP Top 10)](computer-science/CS_Fundamentals.md#96-common-vulnerabilities-owasp-top-10)
    - [ ] [9.7 CORS (Cross-Origin Resource Sharing)](computer-science/CS_Fundamentals.md#97-cors-cross-origin-resource-sharing)
    - [ ] [9.8 Public Key Infrastructure (PKI)](computer-science/CS_Fundamentals.md#98-public-key-infrastructure-pki)
    - [ ] [9.9 API Security](computer-science/CS_Fundamentals.md#99-api-security)
    - [ ] [9.10 Secure Coding Practices](computer-science/CS_Fundamentals.md#910-secure-coding-practices)
    - [ ] [9.11 Systems and Memory-Safety Security](computer-science/CS_Fundamentals.md#911-systems-and-memory-safety-security)
    - [ ] [9.12 Security -- Interview Questions](computer-science/CS_Fundamentals.md#912-security----interview-questions)

**[Data Structures & Algorithms](computer-science/DSA_Fundamentals.md)**

- [ ] [1. Arrays and Dynamic Arrays](computer-science/DSA_Fundamentals.md#1-arrays-and-dynamic-arrays)
- [ ] [2. Linked Lists](computer-science/DSA_Fundamentals.md#2-linked-lists)
- [ ] [3. Stacks](computer-science/DSA_Fundamentals.md#3-stacks)
- [ ] [4. Queues](computer-science/DSA_Fundamentals.md#4-queues)
- [ ] [5. Hash Tables](computer-science/DSA_Fundamentals.md#5-hash-tables)
- [ ] [6. Trees (Binary Trees & BSTs)](computer-science/DSA_Fundamentals.md#6-trees-binary-trees--bsts)
- [ ] [7. Balanced BSTs (AVL & Red-Black Trees)](computer-science/DSA_Fundamentals.md#7-balanced-bsts-avl--red-black-trees)
- [ ] [8. Heaps](computer-science/DSA_Fundamentals.md#8-heaps)
- [ ] [9. Graphs](computer-science/DSA_Fundamentals.md#9-graphs)
- [ ] [10. Tries (Prefix Trees)](computer-science/DSA_Fundamentals.md#10-tries-prefix-trees)
- [ ] [11. Segment Trees](computer-science/DSA_Fundamentals.md#11-segment-trees)
- [ ] [12. Fenwick Trees (Binary Indexed Trees)](computer-science/DSA_Fundamentals.md#12-fenwick-trees-binary-indexed-trees)
- [ ] [13. Disjoint Set Union (Union-Find)](computer-science/DSA_Fundamentals.md#13-disjoint-set-union-union-find)
- [ ] [14. Sorting Algorithms](computer-science/DSA_Fundamentals.md#14-sorting-algorithms)
- [ ] [15. Searching Algorithms](computer-science/DSA_Fundamentals.md#15-searching-algorithms)
- [ ] [16. Graph Traversals](computer-science/DSA_Fundamentals.md#16-graph-traversals)
- [ ] [17. Shortest Path Algorithms](computer-science/DSA_Fundamentals.md#17-shortest-path-algorithms)
- [ ] [18. Minimum Spanning Tree](computer-science/DSA_Fundamentals.md#18-minimum-spanning-tree)
- [ ] [19. String Algorithms](computer-science/DSA_Fundamentals.md#19-string-algorithms)
- [ ] [20. Dynamic Programming](computer-science/DSA_Fundamentals.md#20-dynamic-programming)
- [ ] [21. Divide and Conquer](computer-science/DSA_Fundamentals.md#21-divide-and-conquer)
- [ ] [22. Greedy Algorithms](computer-science/DSA_Fundamentals.md#22-greedy-algorithms)
- [ ] [23. Backtracking](computer-science/DSA_Fundamentals.md#23-backtracking)
- [ ] [24. Bit Manipulation](computer-science/DSA_Fundamentals.md#24-bit-manipulation)
- [ ] [25. Master Complexity Cheat Sheet](computer-science/DSA_Fundamentals.md#25-master-complexity-cheat-sheet)
- [ ] [26. Which Data Structure Should I Use?](computer-science/DSA_Fundamentals.md#26-which-data-structure-should-i-use)
- [ ] [27. Space-Time Tradeoff Summary](computer-science/DSA_Fundamentals.md#27-space-time-tradeoff-summary)
- [ ] [28. Advanced Graph Algorithms](computer-science/DSA_Fundamentals.md#28-advanced-graph-algorithms)
- [ ] [29. Number Theory and Modular Arithmetic](computer-science/DSA_Fundamentals.md#29-number-theory-and-modular-arithmetic)
- [ ] [30. Randomized Algorithms](computer-science/DSA_Fundamentals.md#30-randomized-algorithms)

**[LeetCode Patterns](computer-science/LeetCode_Patterns.md)**

- [ ] [1. Two Pointers](computer-science/LeetCode_Patterns.md#1-two-pointers)
- [ ] [2. Sliding Window](computer-science/LeetCode_Patterns.md#2-sliding-window)
- [ ] [3. Fast and Slow Pointers](computer-science/LeetCode_Patterns.md#3-fast-and-slow-pointers)
- [ ] [4. Merge Intervals](computer-science/LeetCode_Patterns.md#4-merge-intervals)
- [ ] [5. Cyclic Sort](computer-science/LeetCode_Patterns.md#5-cyclic-sort)
- [ ] [6. In-place Linked List Reversal](computer-science/LeetCode_Patterns.md#6-in-place-linked-list-reversal)
- [ ] [7. BFS (Breadth-First Search)](computer-science/LeetCode_Patterns.md#7-bfs-breadth-first-search)
- [ ] [8. DFS (Depth-First Search)](computer-science/LeetCode_Patterns.md#8-dfs-depth-first-search)
- [ ] [9. Two Heaps](computer-science/LeetCode_Patterns.md#9-two-heaps)
- [ ] [10. Subsets / Backtracking](computer-science/LeetCode_Patterns.md#10-subsets--backtracking)
- [ ] [11. Modified Binary Search](computer-science/LeetCode_Patterns.md#11-modified-binary-search)
- [ ] [12. Top K Elements](computer-science/LeetCode_Patterns.md#12-top-k-elements)
- [ ] [13. K-way Merge](computer-science/LeetCode_Patterns.md#13-k-way-merge)
- [ ] [14. Topological Sort](computer-science/LeetCode_Patterns.md#14-topological-sort)
- [ ] [15. Monotonic Stack / Queue](computer-science/LeetCode_Patterns.md#15-monotonic-stack--queue)
- [ ] [16. Union Find (Disjoint Set)](computer-science/LeetCode_Patterns.md#16-union-find-disjoint-set)
- [ ] [17. Trie (Prefix Tree)](computer-science/LeetCode_Patterns.md#17-trie-prefix-tree)
- [ ] [18. Dynamic Programming](computer-science/LeetCode_Patterns.md#18-dynamic-programming)
- [ ] [19. Greedy](computer-science/LeetCode_Patterns.md#19-greedy)
- [ ] [20. Bit Manipulation](computer-science/LeetCode_Patterns.md#20-bit-manipulation)
- [ ] [21. Prefix Sum & Difference Array](computer-science/LeetCode_Patterns.md#21-prefix-sum--difference-array)
- [ ] [22. Hashing & Array Classics](computer-science/LeetCode_Patterns.md#22-hashing--array-classics)
- [ ] [23. Matrix Manipulation](computer-science/LeetCode_Patterns.md#23-matrix-manipulation)
- [ ] [24. Stack-based Parsing](computer-science/LeetCode_Patterns.md#24-stack-based-parsing)
- [ ] [25. Line Sweep & Advanced Intervals](computer-science/LeetCode_Patterns.md#25-line-sweep--advanced-intervals)
- [ ] [26. Design Problems](computer-science/LeetCode_Patterns.md#26-design-problems)
- [ ] [27. Weighted Shortest Path Patterns](computer-science/LeetCode_Patterns.md#27-weighted-shortest-path-patterns)
- [ ] [28. Binary Search on the Answer](computer-science/LeetCode_Patterns.md#28-binary-search-on-the-answer)
- [ ] [29. Ordered Containers](computer-science/LeetCode_Patterns.md#29-ordered-containers)
- [ ] [30. String Hashing & Matching in Practice](computer-science/LeetCode_Patterns.md#30-string-hashing--matching-in-practice)
- [ ] [31. Randomized Algorithms](computer-science/LeetCode_Patterns.md#31-randomized-algorithms)
- [ ] [32. Math & Number Theory](computer-science/LeetCode_Patterns.md#32-math--number-theory)
- [ ] [33. Meet-in-the-Middle & Bidirectional BFS](computer-science/LeetCode_Patterns.md#33-meet-in-the-middle--bidirectional-bfs)
- [ ] [34. Pattern Selection Flowchart](computer-science/LeetCode_Patterns.md#pattern-selection-flowchart)
- [ ] [35. Quick Reference Cheat Sheet](computer-science/LeetCode_Patterns.md#quick-reference-cheat-sheet)

**[High Level Design](computer-science/High_Level_Design.md)**

- [ ] [1. What High Level Design Covers](computer-science/High_Level_Design.md#1-what-high-level-design-covers)
- [ ] [2. A Repeatable Interview Process](computer-science/High_Level_Design.md#2-a-repeatable-interview-process)
- [ ] [3. Estimate the Workload](computer-science/High_Level_Design.md#3-estimate-the-workload)
- [ ] [4. Architecture Building Blocks](computer-science/High_Level_Design.md#4-architecture-building-blocks)
- [ ] [5. Cross-Cutting Design Decisions](computer-science/High_Level_Design.md#5-cross-cutting-design-decisions)
- [ ] [6. Worked System Designs](computer-science/High_Level_Design.md#6-worked-system-designs)
- [ ] [7. Interview Checklists and Pitfalls](computer-science/High_Level_Design.md#7-interview-checklists-and-pitfalls)
- [ ] [8. Practice Prompts](computer-science/High_Level_Design.md#8-practice-prompts)

**[Performance Engineering](computer-science/Performance_Engineering.md)**

- [ ] [1. Latency vs Throughput, Percentiles, and Tail Latency](computer-science/Performance_Engineering.md#1-latency-vs-throughput-percentiles-and-tail-latency)
- [ ] [2. Amdahl's and Gustafson's Laws](computer-science/Performance_Engineering.md#2-amdahls-and-gustafsons-laws)
- [ ] [3. Roofline Model](computer-science/Performance_Engineering.md#3-roofline-model)
- [ ] [4. Little's Law and Queueing](computer-science/Performance_Engineering.md#4-littles-law-and-queueing)
- [ ] [5. Memory Hierarchy Programming](computer-science/Performance_Engineering.md#5-memory-hierarchy-programming)
- [ ] [6. SIMD and Vectorization](computer-science/Performance_Engineering.md#6-simd-and-vectorization)
- [ ] [7. NUMA](computer-science/Performance_Engineering.md#7-numa)
- [ ] [8. Benchmarking Rigor](computer-science/Performance_Engineering.md#8-benchmarking-rigor)
- [ ] [9. Floating-Point Numerics and Reproducibility](computer-science/Performance_Engineering.md#9-floating-point-numerics-and-reproducibility)
- [ ] [10. Interview Q&A](computer-science/Performance_Engineering.md#10-interview-qa)

**[Concurrency Coding Problems](computer-science/Concurrency_Coding_Problems.md)**

- [ ] [1. Toolbox: Primitives, Templates, and Testing](computer-science/Concurrency_Coding_Problems.md#1-toolbox-primitives-templates-and-testing)
- [ ] [2. Print in Order (LeetCode 1114)](computer-science/Concurrency_Coding_Problems.md#2-print-in-order-leetcode-1114)
- [ ] [3. Print FooBar Alternately (LeetCode 1115)](computer-science/Concurrency_Coding_Problems.md#3-print-foobar-alternately-leetcode-1115)
- [ ] [4. Print Zero Even Odd (LeetCode 1116)](computer-science/Concurrency_Coding_Problems.md#4-print-zero-even-odd-leetcode-1116)
- [ ] [5. Building H2O (LeetCode 1117)](computer-science/Concurrency_Coding_Problems.md#5-building-h2o-leetcode-1117)
- [ ] [6. Fizz Buzz Multithreaded (LeetCode 1195)](computer-science/Concurrency_Coding_Problems.md#6-fizz-buzz-multithreaded-leetcode-1195)
- [ ] [7. The Dining Philosophers (LeetCode 1226)](computer-science/Concurrency_Coding_Problems.md#7-the-dining-philosophers-leetcode-1226)
- [ ] [8. Bounded Blocking Queue (LeetCode 1188)](computer-science/Concurrency_Coding_Problems.md#8-bounded-blocking-queue-leetcode-1188)
- [ ] [9. Reader-Writer Lock](computer-science/Concurrency_Coding_Problems.md#9-reader-writer-lock)
- [ ] [10. Spinlocks and a Futex-Based Mutex](computer-science/Concurrency_Coding_Problems.md#10-spinlocks-and-a-futex-based-mutex)
- [ ] [11. Thread-Safe LRU Cache](computer-science/Concurrency_Coding_Problems.md#11-thread-safe-lru-cache)
- [ ] [12. Thread-Safe Token-Bucket Rate Limiter](computer-science/Concurrency_Coding_Problems.md#12-thread-safe-token-bucket-rate-limiter)
- [ ] [13. Thread Pool with Futures](computer-science/Concurrency_Coding_Problems.md#13-thread-pool-with-futures)
- [ ] [14. Reusable Barrier](computer-science/Concurrency_Coding_Problems.md#14-reusable-barrier)
- [ ] [15. Web Crawler Multithreaded (LeetCode 1242)](computer-science/Concurrency_Coding_Problems.md#15-web-crawler-multithreaded-leetcode-1242)
- [ ] [16. Async Web Crawler with Bounded Concurrency](computer-science/Concurrency_Coding_Problems.md#16-async-web-crawler-with-bounded-concurrency)
- [ ] [17. Parallel Merge Sort and Parallel Prefix Sum](computer-science/Concurrency_Coding_Problems.md#17-parallel-merge-sort-and-parallel-prefix-sum)
- [ ] [18. Pitfalls Checklist](computer-science/Concurrency_Coding_Problems.md#18-pitfalls-checklist)
- [ ] [19. Interview Q&A](computer-science/Concurrency_Coding_Problems.md#19-interview-qa)

**[Math, Probability, and Estimation](computer-science/Math_Probability_Estimation.md)**

- [ ] [1. How to Approach Math and Probability Questions](computer-science/Math_Probability_Estimation.md#1-how-to-approach-math-and-probability-questions)
- [ ] [2. Counting and Combinatorics](computer-science/Math_Probability_Estimation.md#2-counting-and-combinatorics)
- [ ] [3. Probability Fundamentals](computer-science/Math_Probability_Estimation.md#3-probability-fundamentals)
- [ ] [4. Expectation, Variance, and Indicator Variables](computer-science/Math_Probability_Estimation.md#4-expectation-variance-and-indicator-variables)
- [ ] [5. Distributions Cheat Sheet](computer-science/Math_Probability_Estimation.md#5-distributions-cheat-sheet)
- [ ] [6. Statistics for Engineers](computer-science/Math_Probability_Estimation.md#6-statistics-for-engineers)
- [ ] [7. Classic Probability Puzzles](computer-science/Math_Probability_Estimation.md#7-classic-probability-puzzles)
- [ ] [8. Monte Carlo Simulation Toolkit](computer-science/Math_Probability_Estimation.md#8-monte-carlo-simulation-toolkit)
- [ ] [9. Fermi Estimation](computer-science/Math_Probability_Estimation.md#9-fermi-estimation)
- [ ] [10. Powers of Two and Handy Numbers](computer-science/Math_Probability_Estimation.md#10-powers-of-two-and-handy-numbers)
- [ ] [11. Quick Reference](computer-science/Math_Probability_Estimation.md#11-quick-reference)

### 8.3 design-patterns

**[Design Patterns in C++](design-patterns/Design_Patterns_Cpp.md)**

- [ ] [1. What Design Patterns Are (and Are Not)](design-patterns/Design_Patterns_Cpp.md#1-what-design-patterns-are-and-are-not)
- [ ] [2. Design Principles: SOLID and Beyond](design-patterns/Design_Patterns_Cpp.md#2-design-principles-solid-and-beyond)
- [ ] [3. Pattern Categories and How to Choose](design-patterns/Design_Patterns_Cpp.md#3-pattern-categories-and-how-to-choose)
- [ ] [4. Singleton](design-patterns/Design_Patterns_Cpp.md#4-singleton)
- [ ] [5. Factory Method](design-patterns/Design_Patterns_Cpp.md#5-factory-method)
- [ ] [6. Abstract Factory](design-patterns/Design_Patterns_Cpp.md#6-abstract-factory)
- [ ] [7. Builder](design-patterns/Design_Patterns_Cpp.md#7-builder)
- [ ] [8. Prototype](design-patterns/Design_Patterns_Cpp.md#8-prototype)
- [ ] [9. Adapter](design-patterns/Design_Patterns_Cpp.md#9-adapter)
- [ ] [10. Bridge](design-patterns/Design_Patterns_Cpp.md#10-bridge)
- [ ] [11. Composite](design-patterns/Design_Patterns_Cpp.md#11-composite)
- [ ] [12. Decorator](design-patterns/Design_Patterns_Cpp.md#12-decorator)
- [ ] [13. Facade](design-patterns/Design_Patterns_Cpp.md#13-facade)
- [ ] [14. Flyweight](design-patterns/Design_Patterns_Cpp.md#14-flyweight)
- [ ] [15. Proxy](design-patterns/Design_Patterns_Cpp.md#15-proxy)
- [ ] [16. Chain of Responsibility](design-patterns/Design_Patterns_Cpp.md#16-chain-of-responsibility)
- [ ] [17. Command](design-patterns/Design_Patterns_Cpp.md#17-command)
- [ ] [18. Interpreter](design-patterns/Design_Patterns_Cpp.md#18-interpreter)
- [ ] [19. Iterator](design-patterns/Design_Patterns_Cpp.md#19-iterator)
- [ ] [20. Mediator](design-patterns/Design_Patterns_Cpp.md#20-mediator)
- [ ] [21. Memento](design-patterns/Design_Patterns_Cpp.md#21-memento)
- [ ] [22. Observer](design-patterns/Design_Patterns_Cpp.md#22-observer)
- [ ] [23. State](design-patterns/Design_Patterns_Cpp.md#23-state)
- [ ] [24. Strategy](design-patterns/Design_Patterns_Cpp.md#24-strategy)
- [ ] [25. Template Method](design-patterns/Design_Patterns_Cpp.md#25-template-method)
- [ ] [26. Visitor](design-patterns/Design_Patterns_Cpp.md#26-visitor)
- [ ] [27. RAII -- Resource Acquisition Is Initialization](design-patterns/Design_Patterns_Cpp.md#27-raii----resource-acquisition-is-initialization)
- [ ] [28. CRTP -- Curiously Recurring Template Pattern](design-patterns/Design_Patterns_Cpp.md#28-crtp----curiously-recurring-template-pattern)
- [ ] [29. pImpl -- Pointer to Implementation](design-patterns/Design_Patterns_Cpp.md#29-pimpl----pointer-to-implementation)
- [ ] [30. Rule of 0/3/5 and Copy-and-Swap](design-patterns/Design_Patterns_Cpp.md#30-rule-of-035-and-copy-and-swap)
- [ ] [31. Type Erasure](design-patterns/Design_Patterns_Cpp.md#31-type-erasure)
- [ ] [32. Policy-Based Design and Tag Dispatch](design-patterns/Design_Patterns_Cpp.md#32-policy-based-design-and-tag-dispatch)
- [ ] [33. NVI -- Non-Virtual Interface](design-patterns/Design_Patterns_Cpp.md#33-nvi----non-virtual-interface)
- [ ] [34. MVC, MVP, and MVVM](design-patterns/Design_Patterns_Cpp.md#34-mvc-mvp-and-mvvm)
- [ ] [35. Layered and Hexagonal Architecture](design-patterns/Design_Patterns_Cpp.md#35-layered-and-hexagonal-architecture)
- [ ] [36. Repository Pattern](design-patterns/Design_Patterns_Cpp.md#36-repository-pattern)
- [ ] [37. Dependency Injection and IoC](design-patterns/Design_Patterns_Cpp.md#37-dependency-injection-and-ioc)
- [ ] [38. Event-Driven and Publish-Subscribe](design-patterns/Design_Patterns_Cpp.md#38-event-driven-and-publish-subscribe)
- [ ] [39. Producer-Consumer](design-patterns/Design_Patterns_Cpp.md#39-producer-consumer)
- [ ] [40. Thread Pool](design-patterns/Design_Patterns_Cpp.md#40-thread-pool)
- [ ] [41. Active Object](design-patterns/Design_Patterns_Cpp.md#41-active-object)
- [ ] [42. Monitor Object](design-patterns/Design_Patterns_Cpp.md#42-monitor-object)
- [ ] [43. Future/Promise](design-patterns/Design_Patterns_Cpp.md#43-futurepromise)
- [ ] [44. Reactor](design-patterns/Design_Patterns_Cpp.md#44-reactor)
- [ ] [45. Actor Model](design-patterns/Design_Patterns_Cpp.md#45-actor-model)
- [ ] [46. Object Pool and Resource Pools](design-patterns/Design_Patterns_Cpp.md#46-object-pool-and-resource-pools)
- [ ] [47. Null Object](design-patterns/Design_Patterns_Cpp.md#47-null-object)
- [ ] [48. Plugin and Registry Architecture](design-patterns/Design_Patterns_Cpp.md#48-plugin-and-registry-architecture)
- [ ] [49. Lock-Free SPSC Ring Buffer](design-patterns/Design_Patterns_Cpp.md#49-lock-free-spsc-ring-buffer)
- [ ] [50. Double Buffering](design-patterns/Design_Patterns_Cpp.md#50-double-buffering)
- [ ] [51. Work Stealing](design-patterns/Design_Patterns_Cpp.md#51-work-stealing)
- [ ] [52. RCU and Read-Mostly Patterns](design-patterns/Design_Patterns_Cpp.md#52-rcu-and-read-mostly-patterns)
- [ ] [53. Pattern Cheat Sheet](design-patterns/Design_Patterns_Cpp.md#53-pattern-cheat-sheet)
- [ ] [54. Anti-Patterns](design-patterns/Design_Patterns_Cpp.md#54-anti-patterns)
- [ ] [55. Decision Guide](design-patterns/Design_Patterns_Cpp.md#55-decision-guide)

**[Design Patterns in Python](design-patterns/Design_Patterns_Python.md)**

- [ ] [1. What Design Patterns Are (and Are Not)](design-patterns/Design_Patterns_Python.md#1-what-design-patterns-are-and-are-not)
- [ ] [2. Design Principles: SOLID and Beyond](design-patterns/Design_Patterns_Python.md#2-design-principles-solid-and-beyond)
- [ ] [3. Why Python Changes the Pattern Calculus](design-patterns/Design_Patterns_Python.md#3-why-python-changes-the-pattern-calculus)
- [ ] [4. Singleton](design-patterns/Design_Patterns_Python.md#4-singleton)
- [ ] [5. Factory Method](design-patterns/Design_Patterns_Python.md#5-factory-method)
- [ ] [6. Abstract Factory](design-patterns/Design_Patterns_Python.md#6-abstract-factory)
- [ ] [7. Builder](design-patterns/Design_Patterns_Python.md#7-builder)
- [ ] [8. Prototype](design-patterns/Design_Patterns_Python.md#8-prototype)
- [ ] [9. Adapter](design-patterns/Design_Patterns_Python.md#9-adapter)
- [ ] [10. Bridge](design-patterns/Design_Patterns_Python.md#10-bridge)
- [ ] [11. Composite](design-patterns/Design_Patterns_Python.md#11-composite)
- [ ] [12. Decorator](design-patterns/Design_Patterns_Python.md#12-decorator)
- [ ] [13. Facade](design-patterns/Design_Patterns_Python.md#13-facade)
- [ ] [14. Flyweight](design-patterns/Design_Patterns_Python.md#14-flyweight)
- [ ] [15. Proxy](design-patterns/Design_Patterns_Python.md#15-proxy)
- [ ] [16. Chain of Responsibility](design-patterns/Design_Patterns_Python.md#16-chain-of-responsibility)
- [ ] [17. Command](design-patterns/Design_Patterns_Python.md#17-command)
- [ ] [18. Interpreter](design-patterns/Design_Patterns_Python.md#18-interpreter)
- [ ] [19. Iterator](design-patterns/Design_Patterns_Python.md#19-iterator)
- [ ] [20. Mediator](design-patterns/Design_Patterns_Python.md#20-mediator)
- [ ] [21. Memento](design-patterns/Design_Patterns_Python.md#21-memento)
- [ ] [22. Observer](design-patterns/Design_Patterns_Python.md#22-observer)
- [ ] [23. State](design-patterns/Design_Patterns_Python.md#23-state)
- [ ] [24. Strategy](design-patterns/Design_Patterns_Python.md#24-strategy)
- [ ] [25. Template Method](design-patterns/Design_Patterns_Python.md#25-template-method)
- [ ] [26. Visitor](design-patterns/Design_Patterns_Python.md#26-visitor)
- [ ] [27. Duck Typing and Protocols](design-patterns/Design_Patterns_Python.md#27-duck-typing-and-protocols)
- [ ] [28. Decorators (Function and Class)](design-patterns/Design_Patterns_Python.md#28-decorators-function-and-class)
- [ ] [29. Context Managers](design-patterns/Design_Patterns_Python.md#29-context-managers)
- [ ] [30. Descriptors and Properties](design-patterns/Design_Patterns_Python.md#30-descriptors-and-properties)
- [ ] [31. Metaclasses](design-patterns/Design_Patterns_Python.md#31-metaclasses)
- [ ] [32. functools: singledispatch, lru_cache, partial](design-patterns/Design_Patterns_Python.md#32-functools-singledispatch-lru_cache-partial)
- [ ] [33. Dataclasses and First-Class Functions](design-patterns/Design_Patterns_Python.md#33-dataclasses-and-first-class-functions)
- [ ] [34. MVC, MVP, and MVVM](design-patterns/Design_Patterns_Python.md#34-mvc-mvp-and-mvvm)
- [ ] [35. Layered and Hexagonal Architecture](design-patterns/Design_Patterns_Python.md#35-layered-and-hexagonal-architecture)
- [ ] [36. Repository Pattern](design-patterns/Design_Patterns_Python.md#36-repository-pattern)
- [ ] [37. Dependency Injection and IoC](design-patterns/Design_Patterns_Python.md#37-dependency-injection-and-ioc)
- [ ] [38. Event-Driven and Publish-Subscribe](design-patterns/Design_Patterns_Python.md#38-event-driven-and-publish-subscribe)
- [ ] [39. Producer-Consumer](design-patterns/Design_Patterns_Python.md#39-producer-consumer)
- [ ] [40. Thread and Process Pools](design-patterns/Design_Patterns_Python.md#40-thread-and-process-pools)
- [ ] [41. Future and Async/Await](design-patterns/Design_Patterns_Python.md#41-future-and-asyncawait)
- [ ] [42. Actor Model](design-patterns/Design_Patterns_Python.md#42-actor-model)
- [ ] [43. The GIL and Choosing a Concurrency Model](design-patterns/Design_Patterns_Python.md#43-the-gil-and-choosing-a-concurrency-model)
- [ ] [44. Free-Threaded Python: What Changes for Patterns](design-patterns/Design_Patterns_Python.md#44-free-threaded-python-what-changes-for-patterns)
- [ ] [45. Pipeline (Staged) Concurrency](design-patterns/Design_Patterns_Python.md#45-pipeline-staged-concurrency)
- [ ] [46. Shared-Memory Buffer Pool Across Processes](design-patterns/Design_Patterns_Python.md#46-shared-memory-buffer-pool-across-processes)
- [ ] [47. Pattern Cheat Sheet](design-patterns/Design_Patterns_Python.md#47-pattern-cheat-sheet)
- [ ] [48. Anti-Patterns](design-patterns/Design_Patterns_Python.md#48-anti-patterns)
- [ ] [49. Decision Guide](design-patterns/Design_Patterns_Python.md#49-decision-guide)

**[Low Level Design Interview Prep](design-patterns/Low_Level_Design_Interview_Prep.md)**

- [ ] [1. What Low Level Design Interviews Evaluate](design-patterns/Low_Level_Design_Interview_Prep.md#1-what-low-level-design-interviews-evaluate)
- [ ] [2. A Repeatable Interview Method](design-patterns/Low_Level_Design_Interview_Prep.md#2-a-repeatable-interview-method)
- [ ] [3. Design Principles and Modeling Tools](design-patterns/Low_Level_Design_Interview_Prep.md#3-design-principles-and-modeling-tools)
- [ ] [4. Designing for Concurrency and Failure](design-patterns/Low_Level_Design_Interview_Prep.md#4-designing-for-concurrency-and-failure)
- [ ] [5. Worked Design: Parking Lot](design-patterns/Low_Level_Design_Interview_Prep.md#5-worked-design-parking-lot)
- [ ] [6. Worked Design: Elevator System](design-patterns/Low_Level_Design_Interview_Prep.md#6-worked-design-elevator-system)
- [ ] [7. Worked Design: Vending Machine](design-patterns/Low_Level_Design_Interview_Prep.md#7-worked-design-vending-machine)
- [ ] [8. Worked Design: Library Management](design-patterns/Low_Level_Design_Interview_Prep.md#8-worked-design-library-management)
- [ ] [9. Worked Design: Splitwise Expense Sharing](design-patterns/Low_Level_Design_Interview_Prep.md#9-worked-design-splitwise-expense-sharing)
- [ ] [10. Worked Design: Rate Limiter](design-patterns/Low_Level_Design_Interview_Prep.md#10-worked-design-rate-limiter)
- [ ] [11. Worked Design: Cache](design-patterns/Low_Level_Design_Interview_Prep.md#11-worked-design-cache)
- [ ] [12. Worked Design: Notification Service](design-patterns/Low_Level_Design_Interview_Prep.md#12-worked-design-notification-service)
- [ ] [13. Worked Design: Task Scheduler](design-patterns/Low_Level_Design_Interview_Prep.md#13-worked-design-task-scheduler)
- [ ] [14. Worked Design: Chess](design-patterns/Low_Level_Design_Interview_Prep.md#14-worked-design-chess)
- [ ] [15. Worked Design: Tic-Tac-Toe](design-patterns/Low_Level_Design_Interview_Prep.md#15-worked-design-tic-tac-toe)
- [ ] [16. Worked Design: Snake and Ladder](design-patterns/Low_Level_Design_Interview_Prep.md#16-worked-design-snake-and-ladder)
- [ ] [17. Worked Design: Movie Ticket Booking (BookMyShow)](design-patterns/Low_Level_Design_Interview_Prep.md#17-worked-design-movie-ticket-booking-bookmyshow)
- [ ] [18. Worked Design: ATM](design-patterns/Low_Level_Design_Interview_Prep.md#18-worked-design-atm)
- [ ] [19. Worked Design: Logging Framework](design-patterns/Low_Level_Design_Interview_Prep.md#19-worked-design-logging-framework)
- [ ] [20. Worked Design: Pub-Sub Message Broker](design-patterns/Low_Level_Design_Interview_Prep.md#20-worked-design-pub-sub-message-broker)
- [ ] [21. Worked Design: In-Memory File System](design-patterns/Low_Level_Design_Interview_Prep.md#21-worked-design-in-memory-file-system)
- [ ] [22. Worked Design: Hotel Booking](design-patterns/Low_Level_Design_Interview_Prep.md#22-worked-design-hotel-booking)
- [ ] [23. Worked Design: Meeting Room Scheduler](design-patterns/Low_Level_Design_Interview_Prep.md#23-worked-design-meeting-room-scheduler)
- [ ] [24. Worked Design: In-Memory Key-Value Store with Transactions](design-patterns/Low_Level_Design_Interview_Prep.md#24-worked-design-in-memory-key-value-store-with-transactions)
- [ ] [25. Worked Design: Stack Overflow (Q&A Site)](design-patterns/Low_Level_Design_Interview_Prep.md#25-worked-design-stack-overflow-qa-site)
- [ ] [26. Worked Design: Inventory and Order Management](design-patterns/Low_Level_Design_Interview_Prep.md#26-worked-design-inventory-and-order-management)
- [ ] [27. Machine-Coding Round Playbook](design-patterns/Low_Level_Design_Interview_Prep.md#27-machine-coding-round-playbook)
- [ ] [28. Interview Communication and Practice Checklist](design-patterns/Low_Level_Design_Interview_Prep.md#28-interview-communication-and-practice-checklist)

### 8.4 languages

**[C++ Fundamentals](languages/Cpp_Fundamentals.md)**

- [ ] [1. Type System and Fundamentals](languages/Cpp_Fundamentals.md#1-type-system-and-fundamentals)
- [ ] [2. Pointers, References, and Const Correctness](languages/Cpp_Fundamentals.md#2-pointers-references-and-const-correctness)
- [ ] [3. Memory Management](languages/Cpp_Fundamentals.md#3-memory-management)
- [ ] [4. Object-Oriented Programming](languages/Cpp_Fundamentals.md#4-object-oriented-programming)
- [ ] [5. Move Semantics and Perfect Forwarding](languages/Cpp_Fundamentals.md#5-move-semantics-and-perfect-forwarding)
- [ ] [6. Templates](languages/Cpp_Fundamentals.md#6-templates)
- [ ] [7. STL Containers](languages/Cpp_Fundamentals.md#7-stl-containers)
- [ ] [8. Iterators, Algorithms, and Lambdas](languages/Cpp_Fundamentals.md#8-iterators-algorithms-and-lambdas)
- [ ] [9. C++11/14 Features](languages/Cpp_Fundamentals.md#9-c1114-features)
- [ ] [10. C++17 Features](languages/Cpp_Fundamentals.md#10-c17-features)
- [ ] [11. C++20 Features](languages/Cpp_Fundamentals.md#11-c20-features)
- [ ] [12. Multithreading and Concurrency](languages/Cpp_Fundamentals.md#12-multithreading-and-concurrency)
- [ ] [13. Compilation, Linking, and the Preprocessor](languages/Cpp_Fundamentals.md#13-compilation-linking-and-the-preprocessor)
- [ ] [14. Exception Handling and Error Management](languages/Cpp_Fundamentals.md#14-exception-handling-and-error-management)
- [ ] [15. Undefined Behavior, Implementation-Defined, and Best Practices](languages/Cpp_Fundamentals.md#15-undefined-behavior-implementation-defined-and-best-practices)
- [ ] [16. Implement-from-scratch Exercises](languages/Cpp_Fundamentals.md#16-implement-from-scratch-exercises)

**[C++ Testing](languages/CPP_Testing.md)**

- [ ] [1. Why Unit Testing in C++?](languages/CPP_Testing.md#1-why-unit-testing-in-c)
- [ ] [2. GoogleTest Setup and Project Layout](languages/CPP_Testing.md#2-googletest-setup-and-project-layout)
- [ ] [3. Test Anatomy](languages/CPP_Testing.md#3-test-anatomy)
- [ ] [4. Assertions: ASSERT vs EXPECT](languages/CPP_Testing.md#4-assertions-assert-vs-expect)
- [ ] [5. Built-in Assertions](languages/CPP_Testing.md#5-built-in-assertions)
- [ ] [6. EXPECT_THAT and the Matcher Library](languages/CPP_Testing.md#6-expect_that-and-the-matcher-library)
- [ ] [7. Custom Matchers](languages/CPP_Testing.md#7-custom-matchers)
- [ ] [8. PrintTo and Pretty-Printing](languages/CPP_Testing.md#8-printto-and-pretty-printing)
- [ ] [9. Test Fixtures](languages/CPP_Testing.md#9-test-fixtures)
- [ ] [10. Suite-level and Program-level Lifecycle](languages/CPP_Testing.md#10-suite-level-and-program-level-lifecycle)
- [ ] [11. Sharing Resources Across Tests](languages/CPP_Testing.md#11-sharing-resources-across-tests)
- [ ] [12. Value-Parameterized Tests](languages/CPP_Testing.md#12-value-parameterized-tests)
- [ ] [13. Typed Tests](languages/CPP_Testing.md#13-typed-tests)
- [ ] [14. Type-Parameterized Tests](languages/CPP_Testing.md#14-type-parameterized-tests)
- [ ] [15. Death Tests](languages/CPP_Testing.md#15-death-tests)
- [ ] [16. Exception-Based Tests](languages/CPP_Testing.md#16-exception-based-tests)
- [ ] [17. SCOPED_TRACE, Skipping, and Disabled Tests](languages/CPP_Testing.md#17-scoped_trace-skipping-and-disabled-tests)
- [ ] [18. Custom Main and Event Listeners](languages/CPP_Testing.md#18-custom-main-and-event-listeners)
- [ ] [19. Test Doubles](languages/CPP_Testing.md#19-test-doubles)
- [ ] [20. Creating Mock Classes](languages/CPP_Testing.md#20-creating-mock-classes)
- [ ] [21. Setting Expectations](languages/CPP_Testing.md#21-setting-expectations)
- [ ] [22. Actions](languages/CPP_Testing.md#22-actions)
- [ ] [23. Cardinalities](languages/CPP_Testing.md#23-cardinalities)
- [ ] [24. Sequences and Ordering](languages/CPP_Testing.md#24-sequences-and-ordering)
- [ ] [25. NiceMock, StrictMock, and NaggyMock](languages/CPP_Testing.md#25-nicemock-strictmock-and-naggymock)
- [ ] [26. Mock Lifetime and Leak Detection](languages/CPP_Testing.md#26-mock-lifetime-and-leak-detection)
- [ ] [27. CMake Integration](languages/CPP_Testing.md#27-cmake-integration)
- [ ] [28. Bazel Integration](languages/CPP_Testing.md#28-bazel-integration)
- [ ] [29. CTest and Test Discovery](languages/CPP_Testing.md#29-ctest-and-test-discovery)
- [ ] [30. GoogleTest Command-Line Interface](languages/CPP_Testing.md#30-googletest-command-line-interface)
- [ ] [31. CI Reporters and JUnit XML](languages/CPP_Testing.md#31-ci-reporters-and-junit-xml)
- [ ] [32. Code Coverage](languages/CPP_Testing.md#32-code-coverage)
- [ ] [33. Sanitizers with GoogleTest](languages/CPP_Testing.md#33-sanitizers-with-googletest)
- [ ] [34. Valgrind](languages/CPP_Testing.md#34-valgrind)
- [ ] [35. Fuzz Testing and Property-Based Approaches](languages/CPP_Testing.md#35-fuzz-testing-and-property-based-approaches)
- [ ] [36. Test Design Best Practices](languages/CPP_Testing.md#36-test-design-best-practices)
- [ ] [37. Designing for Testability](languages/CPP_Testing.md#37-designing-for-testability)
- [ ] [38. Common Pitfalls](languages/CPP_Testing.md#38-common-pitfalls)
- [ ] [39. Interview Questions and Answers](languages/CPP_Testing.md#39-interview-questions-and-answers)
- [ ] [40. Testing Concurrent Code](languages/CPP_Testing.md#40-testing-concurrent-code)
- [ ] [41. Testing GPU / HIP Code](languages/CPP_Testing.md#41-testing-gpu--hip-code)
- [ ] [42. Golden-File, Snapshot, and Approval Testing](languages/CPP_Testing.md#42-golden-file-snapshot-and-approval-testing)
- [ ] [43. Microbenchmarking with Google Benchmark](languages/CPP_Testing.md#43-microbenchmarking-with-google-benchmark)
- [ ] [44. Test-Driven Development (TDD)](languages/CPP_Testing.md#44-test-driven-development-tdd)
- [ ] [45. Catch2 v3 and doctest Compared with GoogleTest](languages/CPP_Testing.md#45-catch2-v3-and-doctest-compared-with-googletest)
- [ ] [46. Mutation Testing with Mull](languages/CPP_Testing.md#46-mutation-testing-with-mull)

**[Python Fundamentals](languages/Python_Fundamentals.md)**

- [ ] [1. Python Data Model & Object System](languages/Python_Fundamentals.md#1-python-data-model--object-system)
- [ ] [2. Built-in Data Types & Structures](languages/Python_Fundamentals.md#2-built-in-data-types--structures)
- [ ] [3. Strings & Text Processing](languages/Python_Fundamentals.md#3-strings--text-processing)
- [ ] [4. Control Flow & Looping](languages/Python_Fundamentals.md#4-control-flow--looping)
- [ ] [5. Functions In Depth](languages/Python_Fundamentals.md#5-functions-in-depth)
- [ ] [6. Comprehensions & Generator Expressions](languages/Python_Fundamentals.md#6-comprehensions--generator-expressions)
- [ ] [7. Iterators & Generators](languages/Python_Fundamentals.md#7-iterators--generators)
- [ ] [Part 1 Interview Questions](languages/Python_Fundamentals.md#part-1-interview-questions)
- [ ] [8. Classes & OOP Fundamentals](languages/Python_Fundamentals.md#8-classes--oop-fundamentals)
- [ ] [9. Inheritance & MRO](languages/Python_Fundamentals.md#9-inheritance--mro)
- [ ] [10. Magic (Dunder) Methods](languages/Python_Fundamentals.md#10-magic-dunder-methods)
- [ ] [11. Abstract Base Classes & Protocols](languages/Python_Fundamentals.md#11-abstract-base-classes--protocols)
- [ ] [12. Descriptors & Metaclasses](languages/Python_Fundamentals.md#12-descriptors--metaclasses)
- [ ] [Part 2 Interview Questions](languages/Python_Fundamentals.md#part-2-interview-questions)
- [ ] [13. Error Handling & Exceptions](languages/Python_Fundamentals.md#13-error-handling--exceptions)
- [ ] [14. Context Managers](languages/Python_Fundamentals.md#14-context-managers)
- [ ] [15. Decorators](languages/Python_Fundamentals.md#15-decorators)
- [ ] [16. Functional Programming](languages/Python_Fundamentals.md#16-functional-programming)
- [ ] [17. Type Hints & Static Typing](languages/Python_Fundamentals.md#17-type-hints--static-typing)
- [ ] [18. Modules, Packages & Import System](languages/Python_Fundamentals.md#18-modules-packages--import-system)
- [ ] [Part 3 Interview Questions](languages/Python_Fundamentals.md#part-3-interview-questions)
- [ ] [19. The GIL & Threading](languages/Python_Fundamentals.md#19-the-gil--threading)
- [ ] [20. Multiprocessing](languages/Python_Fundamentals.md#20-multiprocessing)
- [ ] [21. Asyncio & Async/Await](languages/Python_Fundamentals.md#21-asyncio--asyncawait)
- [ ] [22. concurrent.futures](languages/Python_Fundamentals.md#22-concurrentfutures)
- [ ] [23. Performance & Optimization](languages/Python_Fundamentals.md#23-performance--optimization)
- [ ] [Part 4 Interview Questions](languages/Python_Fundamentals.md#part-4-interview-questions)
- [ ] [24. Memory Management & Garbage Collection](languages/Python_Fundamentals.md#24-memory-management--garbage-collection)
- [ ] [25. Copy Semantics](languages/Python_Fundamentals.md#25-copy-semantics)
- [ ] [26. Python Internals (CPython)](languages/Python_Fundamentals.md#26-python-internals-cpython)
- [ ] [27. Common Gotchas & Best Practices](languages/Python_Fundamentals.md#27-common-gotchas--best-practices)
- [ ] [28. Testing](languages/Python_Fundamentals.md#28-testing)
- [ ] [Part 5 Interview Questions](languages/Python_Fundamentals.md#part-5-interview-questions)
- [ ] [29. Built-in Functions Cheat Sheet](languages/Python_Fundamentals.md#29-built-in-functions-cheat-sheet)
- [ ] [30. Standard Library Highlights](languages/Python_Fundamentals.md#30-standard-library-highlights)
- [ ] [Part 6 Interview Questions](languages/Python_Fundamentals.md#part-6-interview-questions)
- [ ] [31. Python and C/C++ Interop](languages/Python_Fundamentals.md#31-python-and-cc-interop)
- [ ] [32. Debugging, Logging & Warnings](languages/Python_Fundamentals.md#32-debugging-logging--warnings)
- [ ] [Part 7 Interview Questions](languages/Python_Fundamentals.md#part-7-interview-questions)

**[Python Libraries](languages/Python_Libraries.md)**

- [ ] [1. ndarray Fundamentals](languages/Python_Libraries.md#1-ndarray-fundamentals)
- [ ] [2. Indexing and Slicing](languages/Python_Libraries.md#2-indexing-and-slicing)
- [ ] [3. Reshaping and Manipulating](languages/Python_Libraries.md#3-reshaping-and-manipulating)
- [ ] [4. Broadcasting](languages/Python_Libraries.md#4-broadcasting)
- [ ] [5. Vectorized Operations and ufuncs](languages/Python_Libraries.md#5-vectorized-operations-and-ufuncs)
- [ ] [6. Linear Algebra](languages/Python_Libraries.md#6-linear-algebra)
- [ ] [7. Random Module](languages/Python_Libraries.md#7-random-module)
- [ ] [8. Performance and Memory](languages/Python_Libraries.md#8-performance-and-memory)
- [ ] [9. NumPy Common Pitfalls and Interview Questions](languages/Python_Libraries.md#9-numpy-common-pitfalls-and-interview-questions)
- [ ] [10. Advanced NumPy Operations](languages/Python_Libraries.md#10-advanced-numpy-operations)
- [ ] [11. NumPy Vectorization Exercise Set](languages/Python_Libraries.md#11-numpy-vectorization-exercise-set)
- [ ] [12. GPU Array Ecosystem and Zero-Copy Interop](languages/Python_Libraries.md#12-gpu-array-ecosystem-and-zero-copy-interop)
- [ ] [13. Pandas Quick Reference (Summary of Pandas.md)](languages/Python_Libraries.md#13-pandas-quick-reference-summary-of-pandasmd)
- [ ] [14. SciPy Essentials](languages/Python_Libraries.md#14-scipy-essentials)
- [ ] [15. matplotlib Essentials](languages/Python_Libraries.md#15-matplotlib-essentials)
- [ ] [16. pydantic v2 -- Data Validation](languages/Python_Libraries.md#16-pydantic-v2----data-validation)
- [ ] [17. Command-Line Interfaces: click and typer](languages/Python_Libraries.md#17-command-line-interfaces-click-and-typer)
- [ ] [18. HTTP Clients: requests and httpx](languages/Python_Libraries.md#18-http-clients-requests-and-httpx)
- [ ] [19. Qt Architecture and Core Concepts](languages/Python_Libraries.md#19-qt-architecture-and-core-concepts)
- [ ] [20. Widgets](languages/Python_Libraries.md#20-widgets)
- [ ] [21. Layouts](languages/Python_Libraries.md#21-layouts)
- [ ] [22. Signals and Slots](languages/Python_Libraries.md#22-signals-and-slots)
- [ ] [23. Dialogs and Menus](languages/Python_Libraries.md#23-dialogs-and-menus)
- [ ] [24. Model/View Architecture](languages/Python_Libraries.md#24-modelview-architecture)
- [ ] [25. Custom Widgets and Painting](languages/Python_Libraries.md#25-custom-widgets-and-painting)
- [ ] [26. Threading in Qt](languages/Python_Libraries.md#26-threading-in-qt)
- [ ] [27. Styling](languages/Python_Libraries.md#27-styling)
- [ ] [28. PyQt Common Patterns and Interview Questions](languages/Python_Libraries.md#28-pyqt-common-patterns-and-interview-questions)

**[Pandas](languages/Pandas.md)**

- [ ] [1. Pandas Overview, Setup, and Display Options](languages/Pandas.md#1-pandas-overview-setup-and-display-options)
- [ ] [2. Series](languages/Pandas.md#2-series)
- [ ] [3. DataFrame](languages/Pandas.md#3-dataframe)
- [ ] [4. Index and MultiIndex](languages/Pandas.md#4-index-and-multiindex)
- [ ] [5. The Pandas dtype System](languages/Pandas.md#5-the-pandas-dtype-system)
- [ ] [6. Missing Data Semantics](languages/Pandas.md#6-missing-data-semantics)
- [ ] [7. PyArrow Backend](languages/Pandas.md#7-pyarrow-backend)
- [ ] [8. The Four Indexers](languages/Pandas.md#8-the-four-indexers)
- [ ] [9. Boolean Selection, query, eval, where, mask](languages/Pandas.md#9-boolean-selection-query-eval-where-mask)
- [ ] [10. MultiIndex Slicing Patterns](languages/Pandas.md#10-multiindex-slicing-patterns)
- [ ] [11. Copy-on-Write, Views, and SettingWithCopyWarning](languages/Pandas.md#11-copy-on-write-views-and-settingwithcopywarning)
- [ ] [12. Sorting, Ranking, Duplicates](languages/Pandas.md#12-sorting-ranking-duplicates)
- [ ] [13. Type Conversion](languages/Pandas.md#13-type-conversion)
- [ ] [14. The .str Accessor](languages/Pandas.md#14-the-str-accessor)
- [ ] [15. The .dt Accessor](languages/Pandas.md#15-the-dt-accessor)
- [ ] [16. Categorical Deep Dive](languages/Pandas.md#16-categorical-deep-dive)
- [ ] [17. Transformation Toolkit](languages/Pandas.md#17-transformation-toolkit)
- [ ] [18. GroupBy: Split-Apply-Combine](languages/Pandas.md#18-groupby-split-apply-combine)
- [ ] [19. agg vs transform vs filter vs apply](languages/Pandas.md#19-agg-vs-transform-vs-filter-vs-apply)
- [ ] [20. Named Aggregations, crosstab, pivot_table](languages/Pandas.md#20-named-aggregations-crosstab-pivot_table)
- [ ] [21. Window Functions](languages/Pandas.md#21-window-functions)
- [ ] [22. Reshaping: pivot, melt, stack, unstack](languages/Pandas.md#22-reshaping-pivot-melt-stack-unstack)
- [ ] [23. concat](languages/Pandas.md#23-concat)
- [ ] [24. merge and join](languages/Pandas.md#24-merge-and-join)
- [ ] [25. merge_asof, merge_ordered, compare, align](languages/Pandas.md#25-merge_asof-merge_ordered-compare-align)
- [ ] [26. SQL to pandas Translation](languages/Pandas.md#26-sql-to-pandas-translation)
- [ ] [27. Timestamps, Periods, Timedeltas](languages/Pandas.md#27-timestamps-periods-timedeltas)
- [ ] [28. Date Ranges, Resampling, Shifting, Windows](languages/Pandas.md#28-date-ranges-resampling-shifting-windows)
- [ ] [29. Timezones, Business Days, Calendars](languages/Pandas.md#29-timezones-business-days-calendars)
- [ ] [30. I/O Formats](languages/Pandas.md#30-io-formats)
- [ ] [31. Plotting and Styling](languages/Pandas.md#31-plotting-and-styling)
- [ ] [32. Performance](languages/Pandas.md#32-performance)
- [ ] [33. Memory Optimization](languages/Pandas.md#33-memory-optimization)
- [ ] [34. Pandas Internals and Testing](languages/Pandas.md#34-pandas-internals-and-testing)
- [ ] [35. Ecosystem and When to Switch](languages/Pandas.md#35-ecosystem-and-when-to-switch)
- [ ] [36. Idioms and Method Chaining Recipes](languages/Pandas.md#36-idioms-and-method-chaining-recipes)
- [ ] [37. Common Pitfalls and Interview Questions](languages/Pandas.md#37-common-pitfalls-and-interview-questions)

**[Rust and Go for C++ Programmers](languages/Rust_and_Go_for_Cpp_Programmers.md)**

- [ ] [1. Positioning: Three Answers to the Same Problems](languages/Rust_and_Go_for_Cpp_Programmers.md#1-positioning-three-answers-to-the-same-problems)
- [ ] [2. Ownership, Borrowing, and Lifetimes vs RAII and Move Semantics](languages/Rust_and_Go_for_Cpp_Programmers.md#2-ownership-borrowing-and-lifetimes-vs-raii-and-move-semantics)
- [ ] [3. Smart Pointers: Box, Rc, Arc, RefCell vs unique_ptr and shared_ptr](languages/Rust_and_Go_for_Cpp_Programmers.md#3-smart-pointers-box-rc-arc-refcell-vs-unique_ptr-and-shared_ptr)
- [ ] [4. Traits vs Concepts and Virtual Functions](languages/Rust_and_Go_for_Cpp_Programmers.md#4-traits-vs-concepts-and-virtual-functions)
- [ ] [5. Enums and match vs std::variant](languages/Rust_and_Go_for_Cpp_Programmers.md#5-enums-and-match-vs-stdvariant)
- [ ] [6. Result and ? vs Exceptions and std::expected](languages/Rust_and_Go_for_Cpp_Programmers.md#6-result-and--vs-exceptions-and-stdexpected)
- [ ] [7. Send, Sync, and Fearless Concurrency](languages/Rust_and_Go_for_Cpp_Programmers.md#7-send-sync-and-fearless-concurrency)
- [ ] [8. unsafe Rust](languages/Rust_and_Go_for_Cpp_Programmers.md#8-unsafe-rust)
- [ ] [9. Cargo and the Toolchain](languages/Rust_and_Go_for_Cpp_Programmers.md#9-cargo-and-the-toolchain)
- [ ] [10. FFI with C and C++: extern C, bindgen, cbindgen, cxx](languages/Rust_and_Go_for_Cpp_Programmers.md#10-ffi-with-c-and-c-extern-c-bindgen-cbindgen-cxx)
- [ ] [11. Goroutines and the GMP Scheduler](languages/Rust_and_Go_for_Cpp_Programmers.md#11-goroutines-and-the-gmp-scheduler)
- [ ] [12. Channels and select](languages/Rust_and_Go_for_Cpp_Programmers.md#12-channels-and-select)
- [ ] [13. The sync Package and context Cancellation](languages/Rust_and_Go_for_Cpp_Programmers.md#13-the-sync-package-and-context-cancellation)
- [ ] [14. Interfaces and Structural Typing](languages/Rust_and_Go_for_Cpp_Programmers.md#14-interfaces-and-structural-typing)
- [ ] [15. Garbage Collection and Escape Analysis](languages/Rust_and_Go_for_Cpp_Programmers.md#15-garbage-collection-and-escape-analysis)
- [ ] [16. Error Handling and Modules](languages/Rust_and_Go_for_Cpp_Programmers.md#16-error-handling-and-modules)
- [ ] [17. Side-by-Side Examples: C++ / Rust / Go](languages/Rust_and_Go_for_Cpp_Programmers.md#17-side-by-side-examples-c--rust--go)
- [ ] [18. "Why Not Rust?" -- A Balanced Answer](languages/Rust_and_Go_for_Cpp_Programmers.md#18-why-not-rust----a-balanced-answer)
- [ ] [19. Cross-Cutting Interview Q&A](languages/Rust_and_Go_for_Cpp_Programmers.md#19-cross-cutting-interview-qa)

### 8.5 ml-gpu

**[Parallel and GPU Programming](ml-gpu/Parallel_GPU_Programming.md)**

- [ ] [1. MPI Fundamentals](ml-gpu/Parallel_GPU_Programming.md#1-mpi-fundamentals)
- [ ] [2. Point-to-Point Communication](ml-gpu/Parallel_GPU_Programming.md#2-point-to-point-communication)
- [ ] [3. Collective Communication](ml-gpu/Parallel_GPU_Programming.md#3-collective-communication)
- [ ] [4. MPI Data Types and Derived Types](ml-gpu/Parallel_GPU_Programming.md#4-mpi-data-types-and-derived-types)
- [ ] [5. Communicator Management and Topologies](ml-gpu/Parallel_GPU_Programming.md#5-communicator-management-and-topologies)
- [ ] [6. One-Sided Communication (RMA)](ml-gpu/Parallel_GPU_Programming.md#6-one-sided-communication-rma)
- [ ] [7. MPI I/O (Parallel File I/O)](ml-gpu/Parallel_GPU_Programming.md#7-mpi-io-parallel-file-io)
- [ ] [8. Advanced MPI Topics](ml-gpu/Parallel_GPU_Programming.md#8-advanced-mpi-topics)
- [ ] [9. OpenMP Fundamentals](ml-gpu/Parallel_GPU_Programming.md#9-openmp-fundamentals)
- [ ] [10. Work-Sharing Constructs](ml-gpu/Parallel_GPU_Programming.md#10-work-sharing-constructs)
- [ ] [11. Data Environment and Scoping](ml-gpu/Parallel_GPU_Programming.md#11-data-environment-and-scoping)
- [ ] [12. Synchronization](ml-gpu/Parallel_GPU_Programming.md#12-synchronization)
- [ ] [13. Tasking Model](ml-gpu/Parallel_GPU_Programming.md#13-tasking-model)
- [ ] [14. SIMD and Vectorization](ml-gpu/Parallel_GPU_Programming.md#14-simd-and-vectorization)
- [ ] [15. OpenMP Target Offloading (GPU)](ml-gpu/Parallel_GPU_Programming.md#15-openmp-target-offloading-gpu)
- [ ] [16. OpenMP Best Practices](ml-gpu/Parallel_GPU_Programming.md#16-openmp-best-practices)
- [ ] [17. GPU Architecture Fundamentals](ml-gpu/Parallel_GPU_Programming.md#17-gpu-architecture-fundamentals)
- [ ] [18. CUDA Programming Model](ml-gpu/Parallel_GPU_Programming.md#18-cuda-programming-model)
- [ ] [19. CUDA Memory Model](ml-gpu/Parallel_GPU_Programming.md#19-cuda-memory-model)
- [ ] [20. Memory Optimization](ml-gpu/Parallel_GPU_Programming.md#20-memory-optimization)
- [ ] [21. Thread Synchronization and Cooperation](ml-gpu/Parallel_GPU_Programming.md#21-thread-synchronization-and-cooperation)
- [ ] [22. Streams, Events, and Concurrency](ml-gpu/Parallel_GPU_Programming.md#22-streams-events-and-concurrency)
- [ ] [23. Performance Optimization](ml-gpu/Parallel_GPU_Programming.md#23-performance-optimization)
- [ ] [24. Advanced CUDA](ml-gpu/Parallel_GPU_Programming.md#24-advanced-cuda)
- [ ] [25. HIP Fundamentals and Portability](ml-gpu/Parallel_GPU_Programming.md#25-hip-fundamentals-and-portability)
- [ ] [26. HIP Programming Model](ml-gpu/Parallel_GPU_Programming.md#26-hip-programming-model)
- [ ] [27. HIP Memory Management](ml-gpu/Parallel_GPU_Programming.md#27-hip-memory-management)
- [ ] [28. HIP Streams, Events, and Synchronization](ml-gpu/Parallel_GPU_Programming.md#28-hip-streams-events-and-synchronization)
- [ ] [29. CUDA-to-HIP Porting](ml-gpu/Parallel_GPU_Programming.md#29-cuda-to-hip-porting)
- [ ] [30. HIP Performance Tuning for AMD GPUs](ml-gpu/Parallel_GPU_Programming.md#30-hip-performance-tuning-for-amd-gpus)
- [ ] [31. ROCm Ecosystem and Libraries](ml-gpu/Parallel_GPU_Programming.md#31-rocm-ecosystem-and-libraries)
- [ ] [32. Hybrid Programming Patterns](ml-gpu/Parallel_GPU_Programming.md#32-hybrid-programming-patterns)
- [ ] [33. Comprehensive Comparison Tables](ml-gpu/Parallel_GPU_Programming.md#33-comprehensive-comparison-tables)
- [ ] [34. Collective Communication Algorithms and Cost Model](ml-gpu/Parallel_GPU_Programming.md#34-collective-communication-algorithms-and-cost-model)
- [ ] [35. Multi-GPU Programming Beyond Peer Copies (HIP)](ml-gpu/Parallel_GPU_Programming.md#35-multi-gpu-programming-beyond-peer-copies-hip)
- [ ] [36. Portable Programming Models and AMD Wave-Level Primitives](ml-gpu/Parallel_GPU_Programming.md#36-portable-programming-models-and-amd-wave-level-primitives)

**[AMD GPU Architecture and Profiling](ml-gpu/AMD_GPU_Architecture_and_Profiling.md)**

- [ ] [1. CDNA Compute Unit and Chip Architecture](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#1-cdna-compute-unit-and-chip-architecture)
- [ ] [2. GPU Memory Model](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#2-gpu-memory-model)
- [ ] [3. Latency Hiding Quantified](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#3-latency-hiding-quantified)
- [ ] [4. ROCm Profiling Tools](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#4-rocm-profiling-tools)
- [ ] [5. Counter-Driven Performance Methodology](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#5-counter-driven-performance-methodology)
- [ ] [6. How GPU Profilers Work Internally](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#6-how-gpu-profilers-work-internally)
- [ ] [7. GPU Debugging](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#7-gpu-debugging)
- [ ] [8. Interview Q&A for a GPU Profiling-Tools Role](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#8-interview-qa-for-a-gpu-profiling-tools-role)

**[GPU Kernel Case Studies](ml-gpu/GPU_Kernel_Case_Studies.md)**

- [ ] [0. Conventions, Hardware Numbers, and Measurement Harness](ml-gpu/GPU_Kernel_Case_Studies.md#0-conventions-hardware-numbers-and-measurement-harness)
- [ ] [1. Reduction Ladder](ml-gpu/GPU_Kernel_Case_Studies.md#1-reduction-ladder)
- [ ] [2. Matrix Transpose](ml-gpu/GPU_Kernel_Case_Studies.md#2-matrix-transpose)
- [ ] [3. Prefix Scan](ml-gpu/GPU_Kernel_Case_Studies.md#3-prefix-scan)
- [ ] [4. Histogram](ml-gpu/GPU_Kernel_Case_Studies.md#4-histogram)
- [ ] [5. Softmax and LayerNorm](ml-gpu/GPU_Kernel_Case_Studies.md#5-softmax-and-layernorm)
- [ ] [6. Tiled GEMM Progression](ml-gpu/GPU_Kernel_Case_Studies.md#6-tiled-gemm-progression)
- [ ] [7. Elementwise Fusion and Kernel Launch Overhead](ml-gpu/GPU_Kernel_Case_Studies.md#7-elementwise-fusion-and-kernel-launch-overhead)
- [ ] [8. Kernel Exercise List](ml-gpu/GPU_Kernel_Case_Studies.md#8-kernel-exercise-list)

**[LLM and ML Fundamentals](ml-gpu/LLM_and_ML_Fundamentals.md)**

- [ ] [1. Supervised Learning, Generalization, and Regularization](ml-gpu/LLM_and_ML_Fundamentals.md#1-supervised-learning-generalization-and-regularization)
- [ ] [2. Backpropagation](ml-gpu/LLM_and_ML_Fundamentals.md#2-backpropagation)
- [ ] [3. Normalization and Optimizers](ml-gpu/LLM_and_ML_Fundamentals.md#3-normalization-and-optimizers)
- [ ] [4. Evaluation, Data Leakage, and Cross-Validation](ml-gpu/LLM_and_ML_Fundamentals.md#4-evaluation-data-leakage-and-cross-validation)
- [ ] [5. Attention](ml-gpu/LLM_and_ML_Fundamentals.md#5-attention)
- [ ] [6. The Transformer Decoder Block](ml-gpu/LLM_and_ML_Fundamentals.md#6-the-transformer-decoder-block)
- [ ] [7. FLOP Accounting and Scaling Laws](ml-gpu/LLM_and_ML_Fundamentals.md#7-flop-accounting-and-scaling-laws)
- [ ] [8. FlashAttention](ml-gpu/LLM_and_ML_Fundamentals.md#8-flashattention)
- [ ] [9. Prefill, Decode, and the KV Cache](ml-gpu/LLM_and_ML_Fundamentals.md#9-prefill-decode-and-the-kv-cache)
- [ ] [10. Serving Metrics and Scheduling](ml-gpu/LLM_and_ML_Fundamentals.md#10-serving-metrics-and-scheduling)
- [ ] [11. Quantization for Inference](ml-gpu/LLM_and_ML_Fundamentals.md#11-quantization-for-inference)
- [ ] [12. Floating-Point Formats for ML](ml-gpu/LLM_and_ML_Fundamentals.md#12-floating-point-formats-for-ml)
- [ ] [13. Mixed-Precision Training](ml-gpu/LLM_and_ML_Fundamentals.md#13-mixed-precision-training)
- [ ] [14. Formula Cheat Sheet](ml-gpu/LLM_and_ML_Fundamentals.md#14-formula-cheat-sheet)

**[ML and HPC Systems Design](ml-gpu/ML_Systems_Design.md)**

- [ ] [1. How ML System Design Differs from Classic HLD](ml-gpu/ML_Systems_Design.md#1-how-ml-system-design-differs-from-classic-hld)
- [ ] [2. A Framework for ML and HPC Design Interviews](ml-gpu/ML_Systems_Design.md#2-a-framework-for-ml-and-hpc-design-interviews)
- [ ] [3. Numbers Every ML Systems Engineer Should Know](ml-gpu/ML_Systems_Design.md#3-numbers-every-ml-systems-engineer-should-know)
- [ ] [4. Case Study: LLM Inference Serving Platform](ml-gpu/ML_Systems_Design.md#4-case-study-llm-inference-serving-platform)
- [ ] [5. Case Study: Distributed Training of a 70B Model on 512 MI300X](ml-gpu/ML_Systems_Design.md#5-case-study-distributed-training-of-a-70b-model-on-512-mi300x)
- [ ] [6. Case Study: GPU Cluster Job Scheduler](ml-gpu/ML_Systems_Design.md#6-case-study-gpu-cluster-job-scheduler)
- [ ] [7. Case Study: Fleet-Wide GPU Profiling and Telemetry Service](ml-gpu/ML_Systems_Design.md#7-case-study-fleet-wide-gpu-profiling-and-telemetry-service)
- [ ] [8. Case Study: Feature Store](ml-gpu/ML_Systems_Design.md#8-case-study-feature-store)
- [ ] [9. Case Study: Distributed Checkpointing Service](ml-gpu/ML_Systems_Design.md#9-case-study-distributed-checkpointing-service)
- [ ] [10. Case Study: Recommendation System Serving](ml-gpu/ML_Systems_Design.md#10-case-study-recommendation-system-serving)
- [ ] [11. Cross-Case Checklists and Pitfalls](ml-gpu/ML_Systems_Design.md#11-cross-case-checklists-and-pitfalls)
- [ ] [12. Practice Prompts](ml-gpu/ML_Systems_Design.md#12-practice-prompts)

**[ML and AI Frameworks](ml-gpu/ML_AI_Frameworks.md)**

- [ ] [1. Tensor Fundamentals](ml-gpu/ML_AI_Frameworks.md#1-tensor-fundamentals)
- [ ] [2. Autograd and Computational Graphs](ml-gpu/ML_AI_Frameworks.md#2-autograd-and-computational-graphs)
- [ ] [3. Neural Network Modules (torch.nn)](ml-gpu/ML_AI_Frameworks.md#3-neural-network-modules-torchnn)
- [ ] [4. Optimizers and Learning Rate Scheduling](ml-gpu/ML_AI_Frameworks.md#4-optimizers-and-learning-rate-scheduling)
- [ ] [5. Data Loading and Preprocessing](ml-gpu/ML_AI_Frameworks.md#5-data-loading-and-preprocessing)
- [ ] [6. Model Saving, Loading, and Export](ml-gpu/ML_AI_Frameworks.md#6-model-saving-loading-and-export)
- [ ] [7. Distributed Training](ml-gpu/ML_AI_Frameworks.md#7-distributed-training)
- [ ] [8. Performance Optimization](ml-gpu/ML_AI_Frameworks.md#8-performance-optimization)
- [ ] [9. PyTorch Ecosystem and Interview Questions](ml-gpu/ML_AI_Frameworks.md#9-pytorch-ecosystem-and-interview-questions)
- [ ] [10. TensorFlow Architecture and Eager vs Graph Execution](ml-gpu/ML_AI_Frameworks.md#10-tensorflow-architecture-and-eager-vs-graph-execution)
- [ ] [11. Tensors and Variables](ml-gpu/ML_AI_Frameworks.md#11-tensors-and-variables)
- [ ] [12. Keras API and Model Building](ml-gpu/ML_AI_Frameworks.md#12-keras-api-and-model-building)
- [ ] [13. Data Pipelines (tf.data)](ml-gpu/ML_AI_Frameworks.md#13-data-pipelines-tfdata)
- [ ] [14. SavedModel, Serving, and Deployment](ml-gpu/ML_AI_Frameworks.md#14-savedmodel-serving-and-deployment)
- [ ] [15. Distributed Training in TensorFlow](ml-gpu/ML_AI_Frameworks.md#15-distributed-training-in-tensorflow)
- [ ] [16. TensorFlow Performance and XLA](ml-gpu/ML_AI_Frameworks.md#16-tensorflow-performance-and-xla)
- [ ] [17. TensorFlow Ecosystem and Interview Questions](ml-gpu/ML_AI_Frameworks.md#17-tensorflow-ecosystem-and-interview-questions)
- [ ] [18. JAX Fundamentals](ml-gpu/ML_AI_Frameworks.md#18-jax-fundamentals)
- [ ] [19. Transformations: jit, grad, vmap, pmap](ml-gpu/ML_AI_Frameworks.md#19-transformations-jit-grad-vmap-pmap)
- [ ] [20. Sharding and Distributed Computing](ml-gpu/ML_AI_Frameworks.md#20-sharding-and-distributed-computing)
- [ ] [21. Advanced JAX](ml-gpu/ML_AI_Frameworks.md#21-advanced-jax)
- [ ] [22. Flax and Optax](ml-gpu/ML_AI_Frameworks.md#22-flax-and-optax)
- [ ] [23. JAX for HPC and Scientific Computing](ml-gpu/ML_AI_Frameworks.md#23-jax-for-hpc-and-scientific-computing)
- [ ] [24. JAX Ecosystem and Interview Questions](ml-gpu/ML_AI_Frameworks.md#24-jax-ecosystem-and-interview-questions)
- [ ] [25. Triton Fundamentals](ml-gpu/ML_AI_Frameworks.md#25-triton-fundamentals)
- [ ] [26. Writing Triton Kernels](ml-gpu/ML_AI_Frameworks.md#26-writing-triton-kernels)
- [ ] [27. Key Triton Kernels: MatMul, Attention, Softmax](ml-gpu/ML_AI_Frameworks.md#27-key-triton-kernels-matmul-attention-softmax)
- [ ] [28. Triton Performance and Debugging](ml-gpu/ML_AI_Frameworks.md#28-triton-performance-and-debugging)
- [ ] [29. Triton Ecosystem and Interview Questions](ml-gpu/ML_AI_Frameworks.md#29-triton-ecosystem-and-interview-questions)
- [ ] [30. vLLM Architecture and PagedAttention](ml-gpu/ML_AI_Frameworks.md#30-vllm-architecture-and-pagedattention)
- [ ] [31. Serving and API](ml-gpu/ML_AI_Frameworks.md#31-serving-and-api)
- [ ] [32. Scheduling and Batching](ml-gpu/ML_AI_Frameworks.md#32-scheduling-and-batching)
- [ ] [33. Quantization and Model Optimization](ml-gpu/ML_AI_Frameworks.md#33-quantization-and-model-optimization)
- [ ] [34. vLLM Distributed Inference and Interview Questions](ml-gpu/ML_AI_Frameworks.md#34-vllm-distributed-inference-and-interview-questions)
- [ ] [35. SGLang Architecture and Runtime](ml-gpu/ML_AI_Frameworks.md#35-sglang-architecture-and-runtime)
- [ ] [36. Programming Model](ml-gpu/ML_AI_Frameworks.md#36-programming-model)
- [ ] [37. Performance Features](ml-gpu/ML_AI_Frameworks.md#37-performance-features)
- [ ] [38. SGLang Deployment and Interview Questions](ml-gpu/ML_AI_Frameworks.md#38-sglang-deployment-and-interview-questions)
- [ ] [39. Megatron-LM Architecture](ml-gpu/ML_AI_Frameworks.md#39-megatron-lm-architecture)
- [ ] [40. Tensor Parallelism](ml-gpu/ML_AI_Frameworks.md#40-tensor-parallelism)
- [ ] [41. Pipeline Parallelism](ml-gpu/ML_AI_Frameworks.md#41-pipeline-parallelism)
- [ ] [42. Sequence Parallelism and Context Parallelism](ml-gpu/ML_AI_Frameworks.md#42-sequence-parallelism-and-context-parallelism)
- [ ] [43. Megatron-LM Training Recipes and Interview Questions](ml-gpu/ML_AI_Frameworks.md#43-megatron-lm-training-recipes-and-interview-questions)
- [ ] [44. Comprehensive Comparison Tables](ml-gpu/ML_AI_Frameworks.md#44-comprehensive-comparison-tables)
- [ ] [45. Training Memory Math: ZeRO, Activations, and Offload](ml-gpu/ML_AI_Frameworks.md#45-training-memory-math-zero-activations-and-offload)
- [ ] [46. Mixture of Experts and Expert Parallelism](ml-gpu/ML_AI_Frameworks.md#46-mixture-of-experts-and-expert-parallelism)
- [ ] [47. The ROCm ML Stack](ml-gpu/ML_AI_Frameworks.md#47-the-rocm-ml-stack)
- [ ] [48. Debugging a Slow Training Step](ml-gpu/ML_AI_Frameworks.md#48-debugging-a-slow-training-step)

### 8.6 practice

**[Coding Problem List](practice/Coding_Problem_List.md)**

- [ ] [1. How to Use This List](practice/Coding_Problem_List.md#1-how-to-use-this-list)
- [ ] [2. The 150-Problem Checklist by Pattern](practice/Coding_Problem_List.md#2-the-150-problem-checklist-by-pattern)
- [ ] [3. Core 75 Subset](practice/Coding_Problem_List.md#3-core-75-subset)
- [ ] [4. Bonus Lists: Concurrency, Strings, Shortest Paths](practice/Coding_Problem_List.md#4-bonus-lists-concurrency-strings-shortest-paths)
- [ ] [5. Company-Flavored Lists (Commonly Reported)](practice/Coding_Problem_List.md#5-company-flavored-lists-commonly-reported)
- [ ] [6. Timed Practice Protocol](practice/Coding_Problem_List.md#6-timed-practice-protocol)
- [ ] [7. Spaced Repetition and the Error Log](practice/Coding_Problem_List.md#7-spaced-repetition-and-the-error-log)
- [ ] [8. Six-Week Coding Schedule](practice/Coding_Problem_List.md#8-six-week-coding-schedule)
- [ ] [9. Self-Practice Mock Interview Format](practice/Coding_Problem_List.md#9-self-practice-mock-interview-format)
- [ ] [10. Unsolved Practice Sets by Pattern](practice/Coding_Problem_List.md#10-unsolved-practice-sets-by-pattern)

**[C++ Output Quiz](practice/Cpp_Output_Quiz.md)**

- [ ] [1. How to Use This Quiz](practice/Cpp_Output_Quiz.md#1-how-to-use-this-quiz)
- [ ] [2. Object Model, Inheritance, and Layout](practice/Cpp_Output_Quiz.md#2-object-model-inheritance-and-layout)
- [ ] [3. Initialization, Parsing, and Evaluation Order](practice/Cpp_Output_Quiz.md#3-initialization-parsing-and-evaluation-order)
- [ ] [4. Integers, Characters, and Floating Point](practice/Cpp_Output_Quiz.md#4-integers-characters-and-floating-point)
- [ ] [5. Overload Resolution, Templates, and `constexpr`](practice/Cpp_Output_Quiz.md#5-overload-resolution-templates-and-constexpr)
- [ ] [6. Lifetime, Temporaries, and Dangling](practice/Cpp_Output_Quiz.md#6-lifetime-temporaries-and-dangling)
- [ ] [7. Move Semantics and Copy Elision](practice/Cpp_Output_Quiz.md#7-move-semantics-and-copy-elision)
- [ ] [8. Containers and Iterators](practice/Cpp_Output_Quiz.md#8-containers-and-iterators)
- [ ] [9. Smart Pointers and Exceptions](practice/Cpp_Output_Quiz.md#9-smart-pointers-and-exceptions)
- [ ] [10. Aliasing and the One Definition Rule](practice/Cpp_Output_Quiz.md#10-aliasing-and-the-one-definition-rule)
- [ ] [11. Topic Index](practice/Cpp_Output_Quiz.md#11-topic-index)

**[Python Output Quiz](practice/Python_Output_Quiz.md)**

- [ ] [1. How to Use This Quiz](practice/Python_Output_Quiz.md#1-how-to-use-this-quiz)
- [ ] [2. Functions, Closures & Default Arguments](practice/Python_Output_Quiz.md#2-functions-closures--default-arguments)
- [ ] [3. Lists, Tuples & Aliasing](practice/Python_Output_Quiz.md#3-lists-tuples--aliasing)
- [ ] [4. Dicts, Sets & Unpacking](practice/Python_Output_Quiz.md#4-dicts-sets--unpacking)
- [ ] [5. Copying, Sorting & Strings](practice/Python_Output_Quiz.md#5-copying-sorting--strings)
- [ ] [6. Identity, Equality & Numbers](practice/Python_Output_Quiz.md#6-identity-equality--numbers)
- [ ] [7. Control Flow & Exceptions](practice/Python_Output_Quiz.md#7-control-flow--exceptions)
- [ ] [8. Iterators, Generators & Comprehensions](practice/Python_Output_Quiz.md#8-iterators-generators--comprehensions)
- [ ] [9. Scope Rules](practice/Python_Output_Quiz.md#9-scope-rules)
- [ ] [10. Classes, Attributes & the MRO](practice/Python_Output_Quiz.md#10-classes-attributes--the-mro)
- [ ] [11. Concurrency & Async](practice/Python_Output_Quiz.md#11-concurrency--async)
- [ ] [12. Topic Index](practice/Python_Output_Quiz.md#12-topic-index)

**[SQL and Pandas Exercises](practice/SQL_and_Pandas_Exercises.md)**

- [ ] [1. How to Use This File](practice/SQL_and_Pandas_Exercises.md#1-how-to-use-this-file)
- [ ] [2. Sample Schema and Data](practice/SQL_and_Pandas_Exercises.md#2-sample-schema-and-data)
- [ ] [3. Exercises: Ranking, Top-N, and Medians](practice/SQL_and_Pandas_Exercises.md#3-exercises-ranking-top-n-and-medians)
- [ ] [4. Exercises: Duplicates, Anti-Joins, and NULL Traps](practice/SQL_and_Pandas_Exercises.md#4-exercises-duplicates-anti-joins-and-null-traps)
- [ ] [5. Exercises: Self-Joins, Hierarchies, and Relational Division](practice/SQL_and_Pandas_Exercises.md#5-exercises-self-joins-hierarchies-and-relational-division)
- [ ] [6. Exercises: Sequences, Streaks, and Sessions](practice/SQL_and_Pandas_Exercises.md#6-exercises-sequences-streaks-and-sessions)
- [ ] [7. Exercises: Time-Series Metrics](practice/SQL_and_Pandas_Exercises.md#7-exercises-time-series-metrics)
- [ ] [8. Exercises: Shares, Reshaping, and Distributions](practice/SQL_and_Pandas_Exercises.md#8-exercises-shares-reshaping-and-distributions)
- [ ] [9. Exercises: Product Analytics](practice/SQL_and_Pandas_Exercises.md#9-exercises-product-analytics)
- [ ] [10. Pattern Cheat Sheet](practice/SQL_and_Pandas_Exercises.md#10-pattern-cheat-sheet)
- [ ] [11. Interview Follow-Up Questions](practice/SQL_and_Pandas_Exercises.md#11-interview-follow-up-questions)

**[CS Fundamentals Drills](practice/CS_Fundamentals_Drills.md)**

- [ ] [1. How to Use This File](practice/CS_Fundamentals_Drills.md#1-how-to-use-this-file)
- [ ] [2. Numeric Problems](practice/CS_Fundamentals_Drills.md#2-numeric-problems)
- [ ] [3. Rapid-Fire: 100 One-Liners](practice/CS_Fundamentals_Drills.md#3-rapid-fire-100-one-liners)
- [ ] [4. Follow-Up Drill Chains](practice/CS_Fundamentals_Drills.md#4-follow-up-drill-chains)
- [ ] [5. Interview Q&A: Working Numeric Problems Out Loud](practice/CS_Fundamentals_Drills.md#5-interview-qa-working-numeric-problems-out-loud)

**[HLD Mock Interviews](practice/HLD_Mock_Interviews.md)**

- [ ] [1. How to Use This File](practice/HLD_Mock_Interviews.md#1-how-to-use-this-file)
- [ ] [2. Running a 45-Minute Self-Mock](practice/HLD_Mock_Interviews.md#2-running-a-45-minute-self-mock)
- [ ] [3. Evaluation Rubric by Level](practice/HLD_Mock_Interviews.md#3-evaluation-rubric-by-level)
- [ ] [4. Mock 1: URL Shortener](practice/HLD_Mock_Interviews.md#4-mock-1-url-shortener)
- [ ] [5. Mock 2: Rate Limiter](practice/HLD_Mock_Interviews.md#5-mock-2-rate-limiter)
- [ ] [6. Mock 3: News Feed](practice/HLD_Mock_Interviews.md#6-mock-3-news-feed)
- [ ] [7. Mock 4: Chat System](practice/HLD_Mock_Interviews.md#7-mock-4-chat-system)
- [ ] [8. Mock 5: Distributed Key-Value Store](practice/HLD_Mock_Interviews.md#8-mock-5-distributed-key-value-store)
- [ ] [9. Mock 6: Search Typeahead](practice/HLD_Mock_Interviews.md#9-mock-6-search-typeahead)
- [ ] [10. Mock 7: Distributed Job Scheduler](practice/HLD_Mock_Interviews.md#10-mock-7-distributed-job-scheduler)
- [ ] [11. Mock 8: Metrics and Monitoring System](practice/HLD_Mock_Interviews.md#11-mock-8-metrics-and-monitoring-system)
- [ ] [12. Mock 9: GPU Profiling Telemetry Service](practice/HLD_Mock_Interviews.md#12-mock-9-gpu-profiling-telemetry-service)
- [ ] [13. Mock 10: LLM Inference Serving](practice/HLD_Mock_Interviews.md#13-mock-10-llm-inference-serving)
- [ ] [14. Twenty Unsolved Practice Prompts](practice/HLD_Mock_Interviews.md#14-twenty-unsolved-practice-prompts)
- [ ] [15. Common Failure Modes Checklist](practice/HLD_Mock_Interviews.md#15-common-failure-modes-checklist)

**[Flashcards](practice/Flashcards.csv)**

- [ ] All cards reviewed at least once
- [ ] Second pass: miss rate under 10%

**[Night-Before Cheat Sheet](practice/Night_Before_Cheat_Sheet.md)**

- [ ] [1. How to Use This Sheet](practice/Night_Before_Cheat_Sheet.md#1-how-to-use-this-sheet)
- [ ] [2. Complexities](practice/Night_Before_Cheat_Sheet.md#2-complexities)
- [ ] [3. Pattern Triggers and the Coding-Round Flow](practice/Night_Before_Cheat_Sheet.md#3-pattern-triggers-and-the-coding-round-flow)
- [ ] [4. OS and Network Numbers](practice/Night_Before_Cheat_Sheet.md#4-os-and-network-numbers)
- [ ] [5. Latency, Bandwidth, and Estimation Numbers](practice/Night_Before_Cheat_Sheet.md#5-latency-bandwidth-and-estimation-numbers)
- [ ] [6. Concurrency Rules](practice/Night_Before_Cheat_Sheet.md#6-concurrency-rules)
- [ ] [7. C++ Rules of Thumb](practice/Night_Before_Cheat_Sheet.md#7-c-rules-of-thumb)
- [ ] [8. Python Gotchas](practice/Night_Before_Cheat_Sheet.md#8-python-gotchas)
- [ ] [9. Design Checklist](practice/Night_Before_Cheat_Sheet.md#9-design-checklist)
- [ ] [10. GPU Performance Checklist](practice/Night_Before_Cheat_Sheet.md#10-gpu-performance-checklist)
- [ ] [11. Behavioral STAR Reminder](practice/Night_Before_Cheat_Sheet.md#11-behavioral-star-reminder)
- [ ] [12. Rapid Self-Check](practice/Night_Before_Cheat_Sheet.md#12-rapid-self-check)

### 8.7 tools

**[Linux Command Line](tools/Linux_Command_Line.md)**

- [ ] [1. How the Shell Parses a Command Line](tools/Linux_Command_Line.md#1-how-the-shell-parses-a-command-line)
- [ ] [2. Exit Codes, Strict Mode, and Traps](tools/Linux_Command_Line.md#2-exit-codes-strict-mode-and-traps)
- [ ] [3. Variables, Parameter Expansion, Arrays, and Here-Docs](tools/Linux_Command_Line.md#3-variables-parameter-expansion-arrays-and-here-docs)
- [ ] [4. Redirection, Pipes, and Subshells](tools/Linux_Command_Line.md#4-redirection-pipes-and-subshells)
- [ ] [5. Process and Job Control](tools/Linux_Command_Line.md#5-process-and-job-control)
- [ ] [6. Files, Permissions, and Links](tools/Linux_Command_Line.md#6-files-permissions-and-links)
- [ ] [7. The Text-Processing Toolkit](tools/Linux_Command_Line.md#7-the-text-processing-toolkit)
- [ ] [8. Twenty One-Liner Interview Tasks](tools/Linux_Command_Line.md#8-twenty-one-liner-interview-tasks)
- [ ] [9. Environment Variables, Shared Libraries, and GPU Visibility](tools/Linux_Command_Line.md#9-environment-variables-shared-libraries-and-gpu-visibility)
- [ ] [10. SSH: Keys, Config, Agents, Tunnels, and Jump Hosts](tools/Linux_Command_Line.md#10-ssh-keys-config-agents-tunnels-and-jump-hosts)
- [ ] [11. tmux](tools/Linux_Command_Line.md#11-tmux)
- [ ] [12. systemd, journalctl, and cron](tools/Linux_Command_Line.md#12-systemd-journalctl-and-cron)
- [ ] [13. Disk and Memory Diagnostics](tools/Linux_Command_Line.md#13-disk-and-memory-diagnostics)
- [ ] [14. Networking Tools](tools/Linux_Command_Line.md#14-networking-tools)
- [ ] [15. What Happens When You Type a URL, and How to Debug Each Hop](tools/Linux_Command_Line.md#15-what-happens-when-you-type-a-url-and-how-to-debug-each-hop)
- [ ] [16. HPC Job Scheduling with Slurm](tools/Linux_Command_Line.md#16-hpc-job-scheduling-with-slurm)
- [ ] [17. Troubleshooting Scenarios](tools/Linux_Command_Line.md#17-troubleshooting-scenarios)

**[Debugging and Profiling Tools](tools/Debugging_and_Profiling_Tools.md)**

- [ ] [1. The Toolbox at a Glance](tools/Debugging_and_Profiling_Tools.md#1-the-toolbox-at-a-glance)
- [ ] [2. Building for Debuggability](tools/Debugging_and_Profiling_Tools.md#2-building-for-debuggability)
- [ ] [3. GDB Essentials](tools/Debugging_and_Profiling_Tools.md#3-gdb-essentials)
- [ ] [4. Watchpoints, Catchpoints, and Advanced GDB](tools/Debugging_and_Profiling_Tools.md#4-watchpoints-catchpoints-and-advanced-gdb)
- [ ] [5. Attaching to Live Processes and Debugging Hangs](tools/Debugging_and_Profiling_Tools.md#5-attaching-to-live-processes-and-debugging-hangs)
- [ ] [6. Core Dumps](tools/Debugging_and_Profiling_Tools.md#6-core-dumps)
- [ ] [7. LLDB Equivalents and GPU Debuggers](tools/Debugging_and_Profiling_Tools.md#7-lldb-equivalents-and-gpu-debuggers)
- [ ] [8. perf Fundamentals and Hardware Counters](tools/Debugging_and_Profiling_Tools.md#8-perf-fundamentals-and-hardware-counters)
- [ ] [9. Sampling Profiles: perf record, report, top, and annotate](tools/Debugging_and_Profiling_Tools.md#9-sampling-profiles-perf-record-report-top-and-annotate)
- [ ] [10. Flame Graphs and Off-CPU Analysis](tools/Debugging_and_Profiling_Tools.md#10-flame-graphs-and-off-cpu-analysis)
- [ ] [11. perf c2c and False Sharing](tools/Debugging_and_Profiling_Tools.md#11-perf-c2c-and-false-sharing)
- [ ] [12. strace and ltrace](tools/Debugging_and_Profiling_Tools.md#12-strace-and-ltrace)
- [ ] [13. binutils and ELF Inspection](tools/Debugging_and_Profiling_Tools.md#13-binutils-and-elf-inspection)
- [ ] [14. Valgrind, Sanitizers, and Heap Profilers](tools/Debugging_and_Profiling_Tools.md#14-valgrind-sanitizers-and-heap-profilers)
- [ ] [15. eBPF and bpftrace](tools/Debugging_and_Profiling_Tools.md#15-ebpf-and-bpftrace)
- [ ] [16. Python Debugging and Profiling](tools/Debugging_and_Profiling_Tools.md#16-python-debugging-and-profiling)
- [ ] [17. The USE Method and the RED Method](tools/Debugging_and_Profiling_Tools.md#17-the-use-method-and-the-red-method)
- [ ] [18. Scientific Debugging and Bisecting](tools/Debugging_and_Profiling_Tools.md#18-scientific-debugging-and-bisecting)
- [ ] [19. Production Debugging Scenarios](tools/Debugging_and_Profiling_Tools.md#19-production-debugging-scenarios)
- [ ] [20. Quick Reference Card](tools/Debugging_and_Profiling_Tools.md#20-quick-reference-card)
- [ ] [21. Cross-Cutting Interview Questions](tools/Debugging_and_Profiling_Tools.md#21-cross-cutting-interview-questions)

**[Git Fundamentals](tools/Git_Fundamentals.md)**

- [ ] [1. Mental Model: Snapshots, a DAG, and Three Trees](tools/Git_Fundamentals.md#1-mental-model-snapshots-a-dag-and-three-trees)
- [ ] [2. Internals: The Object Database](tools/Git_Fundamentals.md#2-internals-the-object-database)
- [ ] [3. Refs, HEAD, and Revision Syntax](tools/Git_Fundamentals.md#3-refs-head-and-revision-syntax)
- [ ] [4. The Index (Staging Area)](tools/Git_Fundamentals.md#4-the-index-staging-area)
- [ ] [5. Packfiles, Garbage Collection, and Scaling Large Repos](tools/Git_Fundamentals.md#5-packfiles-garbage-collection-and-scaling-large-repos)
- [ ] [6. Branching and Merging](tools/Git_Fundamentals.md#6-branching-and-merging)
- [ ] [7. Rebase and History Editing](tools/Git_Fundamentals.md#7-rebase-and-history-editing)
- [ ] [8. Conflict Resolution and rerere](tools/Git_Fundamentals.md#8-conflict-resolution-and-rerere)
- [ ] [9. Cherry-pick, Revert, and Reset](tools/Git_Fundamentals.md#9-cherry-pick-revert-and-reset)
- [ ] [10. Reflog and Object Recovery](tools/Git_Fundamentals.md#10-reflog-and-object-recovery)
- [ ] [11. Stash](tools/Git_Fundamentals.md#11-stash)
- [ ] [12. Bisect: Finding the Commit That Broke It](tools/Git_Fundamentals.md#12-bisect-finding-the-commit-that-broke-it)
- [ ] [13. History Archaeology: blame, Pickaxe, and Line History](tools/Git_Fundamentals.md#13-history-archaeology-blame-pickaxe-and-line-history)
- [ ] [14. Remotes, Fetch, Push, and Force-Push Safety](tools/Git_Fundamentals.md#14-remotes-fetch-push-and-force-push-safety)
- [ ] [15. Worktrees](tools/Git_Fundamentals.md#15-worktrees)
- [ ] [16. Submodules vs Subtrees](tools/Git_Fundamentals.md#16-submodules-vs-subtrees)
- [ ] [17. Hooks](tools/Git_Fundamentals.md#17-hooks)
- [ ] [18. .gitattributes: Line Endings, Diff and Merge Drivers](tools/Git_Fundamentals.md#18-gitattributes-line-endings-diff-and-merge-drivers)
- [ ] [19. Large Files: Git LFS, Partial Clone, and History Rewriting](tools/Git_Fundamentals.md#19-large-files-git-lfs-partial-clone-and-history-rewriting)
- [ ] [20. Commit and Tag Signing](tools/Git_Fundamentals.md#20-commit-and-tag-signing)
- [ ] [21. Team Workflows: Trunk-Based, GitFlow, and Stacked PRs](tools/Git_Fundamentals.md#21-team-workflows-trunk-based-gitflow-and-stacked-prs)
- [ ] [22. Configuration Cheat Sheet](tools/Git_Fundamentals.md#22-configuration-cheat-sheet)
- [ ] [23. "I Messed Up" Recovery Recipes](tools/Git_Fundamentals.md#23-i-messed-up-recovery-recipes)
- [ ] [24. Interview Q&A](tools/Git_Fundamentals.md#24-interview-qa)

**[CMake Fundamentals](tools/CMake_Fundamentals.md)**

- [ ] [1. Why CMake? Build Systems and Meta-Build Systems](tools/CMake_Fundamentals.md#1-why-cmake-build-systems-and-meta-build-systems)
- [ ] [2. The CMake Pipeline: Configure, Generate, Build, Install](tools/CMake_Fundamentals.md#2-the-cmake-pipeline-configure-generate-build-install)
- [ ] [3. Installing CMake and the Tooling Family](tools/CMake_Fundamentals.md#3-installing-cmake-and-the-tooling-family)
- [ ] [4. The Minimal CMakeLists](tools/CMake_Fundamentals.md#4-the-minimal-cmakelists)
- [ ] [5. In-Source vs Out-of-Source Builds](tools/CMake_Fundamentals.md#5-in-source-vs-out-of-source-builds)
- [ ] [6. Policies and Backwards Compatibility](tools/CMake_Fundamentals.md#6-policies-and-backwards-compatibility)
- [ ] [7. add_executable, add_library, and Library Types](tools/CMake_Fundamentals.md#7-add_executable-add_library-and-library-types)
- [ ] [8. Target Properties and the PUBLIC/PRIVATE/INTERFACE Model](tools/CMake_Fundamentals.md#8-target-properties-and-the-publicprivateinterface-model)
- [ ] [9. The target_* Command Family](tools/CMake_Fundamentals.md#9-the-target_-command-family)
- [ ] [10. Object, Interface, and Imported Libraries](tools/CMake_Fundamentals.md#10-object-interface-and-imported-libraries)
- [ ] [11. Alias Targets and Namespace Conventions](tools/CMake_Fundamentals.md#11-alias-targets-and-namespace-conventions)
- [ ] [12. Variable Scopes](tools/CMake_Fundamentals.md#12-variable-scopes)
- [ ] [13. The Cache, option, and FORCE](tools/CMake_Fundamentals.md#13-the-cache-option-and-force)
- [ ] [14. Lists, Strings, Files, and Paths](tools/CMake_Fundamentals.md#14-lists-strings-files-and-paths)
- [ ] [15. Control Flow, Functions, and Macros](tools/CMake_Fundamentals.md#15-control-flow-functions-and-macros)
- [ ] [16. Anatomy of Generator Expressions](tools/CMake_Fundamentals.md#16-anatomy-of-generator-expressions)
- [ ] [17. Common Generator Expressions](tools/CMake_Fundamentals.md#17-common-generator-expressions)
- [ ] [18. Conditional Linking and Per-Config Flags](tools/CMake_Fundamentals.md#18-conditional-linking-and-per-config-flags)
- [ ] [19. BUILD_INTERFACE vs INSTALL_INTERFACE](tools/CMake_Fundamentals.md#19-build_interface-vs-install_interface)
- [ ] [20. Build Configurations and Multi-Config Generators](tools/CMake_Fundamentals.md#20-build-configurations-and-multi-config-generators)
- [ ] [21. The C++ Standard](tools/CMake_Fundamentals.md#21-the-c-standard)
- [ ] [22. Toolchain Files and Cross-Compilation](tools/CMake_Fundamentals.md#22-toolchain-files-and-cross-compilation)
- [ ] [23. CMake Presets](tools/CMake_Fundamentals.md#23-cmake-presets)
- [ ] [24. Generators: Ninja, Make, Visual Studio, Xcode](tools/CMake_Fundamentals.md#24-generators-ninja-make-visual-studio-xcode)
- [ ] [25. Ninja Deep Dive](tools/CMake_Fundamentals.md#25-ninja-deep-dive)
- [ ] [26. Compiler Caches: ccache and sccache](tools/CMake_Fundamentals.md#26-compiler-caches-ccache-and-sccache)
- [ ] [27. Distributed Builds](tools/CMake_Fundamentals.md#27-distributed-builds)
- [ ] [28. find_package: Module Mode vs Config Mode](tools/CMake_Fundamentals.md#28-find_package-module-mode-vs-config-mode)
- [ ] [29. Writing FindXxx Modules](tools/CMake_Fundamentals.md#29-writing-findxxx-modules)
- [ ] [30. Writing XxxConfig Files](tools/CMake_Fundamentals.md#30-writing-xxxconfig-files)
- [ ] [31. FetchContent Deep Dive](tools/CMake_Fundamentals.md#31-fetchcontent-deep-dive)
- [ ] [32. ExternalProject_Add](tools/CMake_Fundamentals.md#32-externalproject_add)
- [ ] [33. vcpkg Integration](tools/CMake_Fundamentals.md#33-vcpkg-integration)
- [ ] [34. Conan Integration](tools/CMake_Fundamentals.md#34-conan-integration)
- [ ] [35. CPM.cmake and Hybrid Approaches](tools/CMake_Fundamentals.md#35-cpmcmake-and-hybrid-approaches)
- [ ] [36. The install Command](tools/CMake_Fundamentals.md#36-the-install-command)
- [ ] [37. GNUInstallDirs and FHS Layout](tools/CMake_Fundamentals.md#37-gnuinstalldirs-and-fhs-layout)
- [ ] [38. Exporting Targets and Generating Config Files](tools/CMake_Fundamentals.md#38-exporting-targets-and-generating-config-files)
- [ ] [39. ABI and SOVERSION](tools/CMake_Fundamentals.md#39-abi-and-soversion)
- [ ] [40. CPack: TGZ, DEB, RPM, NSIS, WIX](tools/CMake_Fundamentals.md#40-cpack-tgz-deb-rpm-nsis-wix)
- [ ] [41. Generating pkg-config Files](tools/CMake_Fundamentals.md#41-generating-pkg-config-files)
- [ ] [42. enable_testing and add_test](tools/CMake_Fundamentals.md#42-enable_testing-and-add_test)
- [ ] [43. Test Properties](tools/CMake_Fundamentals.md#43-test-properties)
- [ ] [44. Parallel Test Execution](tools/CMake_Fundamentals.md#44-parallel-test-execution)
- [ ] [45. gtest_discover_tests and catch_discover_tests](tools/CMake_Fundamentals.md#45-gtest_discover_tests-and-catch_discover_tests)
- [ ] [46. CTest Dashboards and CDash](tools/CMake_Fundamentals.md#46-ctest-dashboards-and-cdash)
- [ ] [47. Code Coverage Integration](tools/CMake_Fundamentals.md#47-code-coverage-integration)
- [ ] [48. add_custom_command vs add_custom_target](tools/CMake_Fundamentals.md#48-add_custom_command-vs-add_custom_target)
- [ ] [49. Code Generation: Protobuf, Qt, Flatbuffers](tools/CMake_Fundamentals.md#49-code-generation-protobuf-qt-flatbuffers)
- [ ] [50. configure_file and Header Generation](tools/CMake_Fundamentals.md#50-configure_file-and-header-generation)
- [ ] [51. CMake Script Mode](tools/CMake_Fundamentals.md#51-cmake-script-mode)
- [ ] [52. Per-Target vs Global Flags](tools/CMake_Fundamentals.md#52-per-target-vs-global-flags)
- [ ] [53. Sanitizers](tools/CMake_Fundamentals.md#53-sanitizers)
- [ ] [54. Hardening and Security Flags](tools/CMake_Fundamentals.md#54-hardening-and-security-flags)
- [ ] [55. LTO and IPO](tools/CMake_Fundamentals.md#55-lto-and-ipo)
- [ ] [56. Warning Levels and Warnings-as-Errors](tools/CMake_Fundamentals.md#56-warning-levels-and-warnings-as-errors)
- [ ] [57. compile_commands.json for clangd](tools/CMake_Fundamentals.md#57-compile_commandsjson-for-clangd)
- [ ] [58. clang-tidy, clang-format, and Friends](tools/CMake_Fundamentals.md#58-clang-tidy-clang-format-and-friends)
- [ ] [59. IDE Support](tools/CMake_Fundamentals.md#59-ide-support)
- [ ] [60. Reducing Configure Time](tools/CMake_Fundamentals.md#60-reducing-configure-time)
- [ ] [61. Unity Builds and Precompiled Headers](tools/CMake_Fundamentals.md#61-unity-builds-and-precompiled-headers)
- [ ] [62. C++20 Modules Support](tools/CMake_Fundamentals.md#62-c20-modules-support)
- [ ] [63. Refactoring Legacy CMake](tools/CMake_Fundamentals.md#63-refactoring-legacy-cmake)
- [ ] [64. HIP and ROCm with CMake](tools/CMake_Fundamentals.md#64-hip-and-rocm-with-cmake)
- [ ] [65. RPATH and RUNPATH](tools/CMake_Fundamentals.md#65-rpath-and-runpath)
- [ ] [66. Building Python Extensions](tools/CMake_Fundamentals.md#66-building-python-extensions)
- [ ] [67. Symbol Visibility and Export Control](tools/CMake_Fundamentals.md#67-symbol-visibility-and-export-control)
- [ ] [68. Static Library Link Order and Circular Dependencies](tools/CMake_Fundamentals.md#68-static-library-link-order-and-circular-dependencies)
- [ ] [69. Project Layout and Conventions](tools/CMake_Fundamentals.md#69-project-layout-and-conventions)
- [ ] [70. Cheatsheet](tools/CMake_Fundamentals.md#70-cheatsheet)
- [ ] [71. Common Pitfalls](tools/CMake_Fundamentals.md#71-common-pitfalls)
- [ ] [72. Interview Questions and Answers](tools/CMake_Fundamentals.md#72-interview-questions-and-answers)

**[Containers and CI](tools/Containers_and_CI.md)**

- [ ] [1. What a Container Really Is](tools/Containers_and_CI.md#1-what-a-container-really-is)
- [ ] [2. Namespaces in Practice](tools/Containers_and_CI.md#2-namespaces-in-practice)
- [ ] [3. cgroups v2 Controllers](tools/Containers_and_CI.md#3-cgroups-v2-controllers)
- [ ] [4. OverlayFS and Union Filesystems](tools/Containers_and_CI.md#4-overlayfs-and-union-filesystems)
- [ ] [5. Images, Layers, and the OCI Specifications](tools/Containers_and_CI.md#5-images-layers-and-the-oci-specifications)
- [ ] [6. Container Runtimes and the Docker Stack](tools/Containers_and_CI.md#6-container-runtimes-and-the-docker-stack)
- [ ] [7. Containers vs VMs and Hypervisors](tools/Containers_and_CI.md#7-containers-vs-vms-and-hypervisors)
- [ ] [8. Dockerfile Best Practices](tools/Containers_and_CI.md#8-dockerfile-best-practices)
- [ ] [9. docker run Essentials](tools/Containers_and_CI.md#9-docker-run-essentials)
- [ ] [10. Running ROCm Containers](tools/Containers_and_CI.md#10-running-rocm-containers)
- [ ] [11. NVIDIA Container Toolkit Compared](tools/Containers_and_CI.md#11-nvidia-container-toolkit-compared)
- [ ] [12. Apptainer and Singularity on HPC](tools/Containers_and_CI.md#12-apptainer-and-singularity-on-hpc)
- [ ] [13. Kubernetes Architecture and Core Objects](tools/Containers_and_CI.md#13-kubernetes-architecture-and-core-objects)
- [ ] [14. Resource Requests, Limits, and QoS](tools/Containers_and_CI.md#14-resource-requests-limits-and-qos)
- [ ] [15. GPU Scheduling: Device Plugins, Node Selectors, and Taints](tools/Containers_and_CI.md#15-gpu-scheduling-device-plugins-node-selectors-and-taints)
- [ ] [16. Jobs, CronJobs, and Batch Workloads](tools/Containers_and_CI.md#16-jobs-cronjobs-and-batch-workloads)
- [ ] [17. CI/CD Pipeline Design](tools/Containers_and_CI.md#17-cicd-pipeline-design)
- [ ] [18. Matrix Builds: Compilers, ROCm Versions, and GPU Architectures](tools/Containers_and_CI.md#18-matrix-builds-compilers-rocm-versions-and-gpu-architectures)
- [ ] [19. Caching in CI](tools/Containers_and_CI.md#19-caching-in-ci)
- [ ] [20. Self-Hosted GPU Runners](tools/Containers_and_CI.md#20-self-hosted-gpu-runners)
- [ ] [21. Flaky Tests and Quarantine](tools/Containers_and_CI.md#21-flaky-tests-and-quarantine)
- [ ] [22. Artifacts, Supply Chain, and Release Automation](tools/Containers_and_CI.md#22-artifacts-supply-chain-and-release-automation)
- [ ] [23. A Complete GitHub Actions Workflow](tools/Containers_and_CI.md#23-a-complete-github-actions-workflow)
- [ ] [24. Scenario Interview Questions](tools/Containers_and_CI.md#24-scenario-interview-questions)
- [ ] [25. Quick Reference Cheat Sheet](tools/Containers_and_CI.md#25-quick-reference-cheat-sheet)

---

## 9. Weekly Self-Assessment Template

Copy this block into a private notes file every Sunday (keep your personal log out of the repository if it mentions employers or interview details). Fill it in from data (the error log, mock recordings, the checklist), not from memory.

```text
WEEK __ SELF-ASSESSMENT                    Date: ____-__-__   Track: A / B / C
Planned hours: __   Actual hours: __   Blocks missed: __ (which: ________)

1. CODING
   New problems attempted: __ (target A/B 14, C 19)
   Grades:  A __  B __  C __  D __          A-rate on mediums: __%
   Median time on mediums: __ min (target 25)
   Re-solves due: __   done: __   passed at A: __
   Top 2 root causes (from error log):   1. __________  2. __________
   Patterns finished this week: ______________________________

2. MOCKS (rubric scores)
   Coding mock:  problem solving _/4  coding _/4  verification _/4  communication _/4  = __/16
   Second mock:  type ________   score/verdict: ________
   Longest silence on the recording: __ s   Biggest single mistake: ____________

3. FUNDAMENTALS AND DOMAIN (1 = cannot explain, 5 = could teach it)
   Sections ticked in STUDY_PLAN Section 8 this week: __
   Cold-recall test (5 random Q blocks from this week's sections): __/5
   Area ratings:  ______ _/5   ______ _/5   ______ _/5

4. BEHAVIORAL
   Story cards complete: __/8+    Told aloud this week: __
   Pitches (30 s / 2 min / 10 min) delivered without notes: Y/N  Y/N  Y/N

5. RECALL
   Flashcards reviewed: __   miss rate: __%   Rapid-fire one-liners: __/__

6. DECISIONS FOR NEXT WEEK
   Focus pair 1 (pattern + root cause): __________________
   Focus pair 2 (pattern + root cause): __________________
   Carry-over items from the exit check: __________________
   One thing to stop doing: __________________
```

### 9.1 Decision rules

| Signal | Threshold | Action next week |
|---|---|---|
| A-rate on mediums | below 50% after week 3 | drop to 1 new problem a day; spend the time on re-solves of that week's patterns |
| Median medium time | over 35 min | do 3 timed re-solves of retired problems per day (speed, not novelty) |
| Re-solve backlog | more than 10 overdue | no new problems until the backlog is under 5 |
| Rubric "verification" | 1-2 on two consecutive mocks | force a written dry-run with one edge case before every submit |
| Rubric "communication" or silence over 30 s | any mock | narrate every practice problem aloud for a week, including re-solves |
| Cold-recall test | 3/5 or lower | re-do this week's fundamentals cell before starting next week's |
| Blocks missed | 3 or more | shrink next week's plan to the 90-minute variant ([3.1](#31-weekday-about-25-hours)); protect coding and the mock |
| Stories told aloud | fewer than 2 | move the behavioral block from Sunday to two weekday recall slots |
| Same exit-check item failed twice | any | write a flashcard for it and add it to the [Night-Before Cheat Sheet](practice/Night_Before_Cheat_Sheet.md) notes |

**Q1. What is the single most useful number in the template?**

The rubric score for "verification" and "communication" across mocks, more than the A-rate. Most candidates who solve problems in practice but fail loops do so on those two dimensions: they code silently, skip the dry run, and submit with an edge-case bug. These are also the cheapest to fix: one week of forced narration and written dry runs usually moves both dimensions by a full point.

**Q2. How do I know the plan is not working and should be changed rather than followed harder?**

If two consecutive self-assessments show the same top root cause and a flat or falling A-rate, the method is wrong, not the effort. Typical fixes: switch from reading solutions to deriving them with hints (the [hint ladder](practice/Coding_Problem_List.md#62-the-attempt---hint---solution---re-solve-loop)), go back one pattern (for example, DP struggles are often weak recursion or DFS), or swap a self-mock for a partner mock to get outside feedback. Change one variable per week so the next self-assessment can tell you whether the change helped.
