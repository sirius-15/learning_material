# Learning Material -- Interview Preparation Reference for GPU/HPC, Systems C++, ML Infra, and Big-Tech SWE Roles

> Last reviewed: 2026-11 · Section links are to the file layout as of this date. Each fast-moving document (ROCm, GPU, ML, and tooling) has its own "Versions assumed" line under its title.

## Table of Contents

1. [Purpose](#1-purpose)
2. [Start Here](#2-start-here)
3. [Round-to-File Map](#3-round-to-file-map)
4. [Directory Overview](#4-directory-overview)
5. [Practice Material](#5-practice-material)
6. [Using This Repo with Spaced Repetition](#6-using-this-repo-with-spaced-repetition)
7. [Printable HTML (scripts/md_to_html.py)](#7-printable-html-scriptsmd_to_htmlpy)
8. [Conventions](#8-conventions)

---

## 1. Purpose

This repository is a self-contained, markdown-only interview reference. It is written for a software engineer who works on GPU profiling tools (rocprof-compute / ROCm) and is preparing for four kinds of roles: GPU/HPC engineering, systems C++, ML infrastructure, and general big-tech software engineering. It covers the coding round (data structures, algorithms, and 33 problem patterns), CS fundamentals, Linux and systems, concurrency, C++ and Python language depth, low- and high-level design, ML/HPC system design, the GPU and profiling domain round, ML and LLM fundamentals, behavioral and project deep-dive rounds, and loop logistics and offer negotiation. Every major section ends with interview Q&A that has full answers. The `practice/` directory has timed drills, output quizzes, mock-interview scripts, and flashcards. Use this README to find the right file and section for each round.

---

## 2. Start Here

1. Read **[STUDY_PLAN.md](STUDY_PLAN.md)**. It gives a prioritized multi-week schedule, a reading order for each target role, and a progress checklist.
2. Skim [Interview Loops and Logistics -- Anatomy of a Tech Interview Loop](career/Interview_Loops_and_Logistics.md#2-anatomy-of-a-tech-interview-loop) and [Company Loop Profiles](career/Interview_Loops_and_Logistics.md#3-company-loop-profiles) to learn which rounds your target companies run.
3. Use the [Round-to-File Map](#3-round-to-file-map) below to go from a round to the exact sections to study.
4. Start the daily coding habit right away, using the [Coding Problem List](practice/Coding_Problem_List.md#1-how-to-use-this-list) and its [six-week schedule](practice/Coding_Problem_List.md#8-six-week-coding-schedule). Coding skill takes the longest to build.
5. Write your story bank early: [Behavioral Interview Prep -- Building Your Story Bank](career/Behavioral_Interview_Prep.md#3-building-your-story-bank) and the [rocprof-compute pitches](career/Project_Deep_Dive_rocprof-compute.md#2-the-pitches).
6. Review the [Night-Before Cheat Sheet](practice/Night_Before_Cheat_Sheet.md) the evening before each loop.

---

## 3. Round-to-File Map

Each row lists the **primary** sections to study first, then **supporting** material and **practice**. All links are relative to the repo root.

| Interview round | What it tests | Primary sections | Supporting sections | Practice |
|---|---|---|---|---|
| **Coding (DSA / LeetCode)** | Pattern recognition, correct code in 20-40 min, complexity analysis, communication | [LeetCode Patterns](computer-science/LeetCode_Patterns.md) (all 33 patterns), especially the [Pattern Selection Flowchart](computer-science/LeetCode_Patterns.md#pattern-selection-flowchart) and [Quick Reference Cheat Sheet](computer-science/LeetCode_Patterns.md#quick-reference-cheat-sheet) | [DSA Fundamentals -- Master Complexity Cheat Sheet](computer-science/DSA_Fundamentals.md#25-master-complexity-cheat-sheet), [Which Data Structure Should I Use?](computer-science/DSA_Fundamentals.md#26-which-data-structure-should-i-use), [Coding-Round Communication Framework](career/Interview_Loops_and_Logistics.md#7-the-coding-round-communication-framework), [Worked Coding Round](career/Interview_Loops_and_Logistics.md#8-worked-coding-round-subarray-sum-equals-k) | [Coding Problem List](practice/Coding_Problem_List.md) (300 problems, Core 75, [timed protocol](practice/Coding_Problem_List.md#6-timed-practice-protocol)), with every problem's solution in [LeetCode Patterns](computer-science/LeetCode_Patterns.md) or [LeetCode Solutions](practice/LeetCode_Solutions.md) |
| **CS fundamentals** | OS, networking, databases, architecture, security, quick numeric reasoning | [CS Fundamentals](computer-science/CS_Fundamentals.md): [Operating Systems](computer-science/CS_Fundamentals.md#1-operating-systems), [Computer Networks](computer-science/CS_Fundamentals.md#2-computer-networks), [Database Systems](computer-science/CS_Fundamentals.md#3-database-systems), [Computer Architecture](computer-science/CS_Fundamentals.md#7-computer-architecture), [Security](computer-science/CS_Fundamentals.md#9-security) | [Math, Probability, and Estimation](computer-science/Math_Probability_Estimation.md) (puzzles, [Fermi estimation](computer-science/Math_Probability_Estimation.md#9-fermi-estimation), [powers of two](computer-science/Math_Probability_Estimation.md#10-powers-of-two-and-handy-numbers)), [Performance Engineering -- Latency vs Throughput](computer-science/Performance_Engineering.md#1-latency-vs-throughput-percentiles-and-tail-latency) | [CS Fundamentals Drills](practice/CS_Fundamentals_Drills.md) (numeric problems, 100 one-liners, follow-up chains) |
| **Systems / Linux** | Process model, memory, scheduler, shell fluency, debugging a live box | [CS Fundamentals 1.9-1.12](computer-science/CS_Fundamentals.md#19-linux-process-lifecycle-signals-and-file-descriptors) (process lifecycle, [I/O multiplexing](computer-science/CS_Fundamentals.md#110-io-multiplexing-and-event-driven-servers), [Linux memory](computer-science/CS_Fundamentals.md#111-linux-memory-management-internals), [scheduler](computer-science/CS_Fundamentals.md#112-the-linux-scheduler)), [Linux Command Line](tools/Linux_Command_Line.md), especially [Troubleshooting Scenarios](tools/Linux_Command_Line.md#17-troubleshooting-scenarios) | [Debugging and Profiling Tools -- Production Debugging Scenarios](tools/Debugging_and_Profiling_Tools.md#19-production-debugging-scenarios), [USE and RED Methods](tools/Debugging_and_Profiling_Tools.md#17-the-use-method-and-the-red-method), [What a Container Really Is](tools/Containers_and_CI.md#1-what-a-container-really-is), [Performance Engineering -- Memory Hierarchy Programming](computer-science/Performance_Engineering.md#5-memory-hierarchy-programming), [NUMA](computer-science/Performance_Engineering.md#7-numa) | [Twenty One-Liner Interview Tasks](tools/Linux_Command_Line.md#8-twenty-one-liner-interview-tasks), [CS Fundamentals Drills -- Follow-Up Chains](practice/CS_Fundamentals_Drills.md#4-follow-up-drill-chains) |
| **Concurrency** | Correct synchronization under pressure, memory models, lock-free reasoning, live coding of classic problems | [Concurrency Coding Problems](computer-science/Concurrency_Coding_Problems.md) (start with the [Toolbox](computer-science/Concurrency_Coding_Problems.md#1-toolbox-primitives-templates-and-testing) and the [Pitfalls Checklist](computer-science/Concurrency_Coding_Problems.md#18-pitfalls-checklist)), [CS Fundamentals -- Concurrency and Multithreading](computer-science/CS_Fundamentals.md#6-concurrency-and-multithreading) | [Memory Models and Visibility](computer-science/CS_Fundamentals.md#69-memory-models-and-visibility), [C++ Multithreading and Concurrency](languages/Cpp_Fundamentals.md#12-multithreading-and-concurrency), [Python GIL and Threading](languages/Python_Fundamentals.md#19-the-gil--threading), [Asyncio](languages/Python_Fundamentals.md#21-asyncio--asyncawait), [Design Patterns in C++ 39-52](design-patterns/Design_Patterns_Cpp.md#39-producer-consumer) (producer-consumer through RCU), [Testing Concurrent Code](languages/CPP_Testing.md#40-testing-concurrent-code) | [Concurrency Q&A](computer-science/Concurrency_Coding_Problems.md#19-interview-qa), concurrency bonus list in the [Coding Problem List](practice/Coding_Problem_List.md#4-bonus-lists-concurrency-strings-shortest-paths) |
| **C++ deep dive** | Object model, lifetimes, move semantics, templates, UB, implementing standard components from scratch | [C++ Fundamentals](languages/Cpp_Fundamentals.md): [Memory Management](languages/Cpp_Fundamentals.md#3-memory-management), [Move Semantics](languages/Cpp_Fundamentals.md#5-move-semantics-and-perfect-forwarding), [Templates](languages/Cpp_Fundamentals.md#6-templates), [Undefined Behavior](languages/Cpp_Fundamentals.md#15-undefined-behavior-implementation-defined-and-best-practices), [Implement-from-scratch Exercises](languages/Cpp_Fundamentals.md#16-implement-from-scratch-exercises) | [C++ idioms: RAII, CRTP, pImpl, Rule of 0/3/5, type erasure](design-patterns/Design_Patterns_Cpp.md#27-raii----resource-acquisition-is-initialization), [Compilation and Linking](languages/Cpp_Fundamentals.md#13-compilation-linking-and-the-preprocessor), [CMake Interview Q&A](tools/CMake_Fundamentals.md#72-interview-questions-and-answers), [C++ Testing Q&A](languages/CPP_Testing.md#39-interview-questions-and-answers), [SIMD and Vectorization](computer-science/Performance_Engineering.md#6-simd-and-vectorization), ["Why Not Rust?"](languages/Rust_and_Go_for_Cpp_Programmers.md#18-why-not-rust----a-balanced-answer) | [C++ Output Quiz](practice/Cpp_Output_Quiz.md) (55 puzzles) |
| **Python deep dive** | Data model, GIL and concurrency, CPython internals, gotchas, data wrangling | [Python Fundamentals](languages/Python_Fundamentals.md): [Data Model](languages/Python_Fundamentals.md#1-python-data-model--object-system), [GIL](languages/Python_Fundamentals.md#19-the-gil--threading), [Memory and GC](languages/Python_Fundamentals.md#24-memory-management--garbage-collection), [CPython Internals](languages/Python_Fundamentals.md#26-python-internals-cpython), [Common Gotchas](languages/Python_Fundamentals.md#27-common-gotchas--best-practices) | [Python and C/C++ Interop](languages/Python_Fundamentals.md#31-python-and-cc-interop), [NumPy Pitfalls and Q&A](languages/Python_Libraries.md#9-numpy-common-pitfalls-and-interview-questions), [Pandas Pitfalls and Q&A](languages/Pandas.md#37-common-pitfalls-and-interview-questions), [The GIL and Choosing a Concurrency Model](design-patterns/Design_Patterns_Python.md#43-the-gil-and-choosing-a-concurrency-model) | [Python Output Quiz](practice/Python_Output_Quiz.md) (49 puzzles), [SQL and Pandas Exercises](practice/SQL_and_Pandas_Exercises.md) |
| **LLD / machine coding** | Class modeling, extensibility, patterns used on purpose, working code in 60-90 min | [Low Level Design Interview Prep](design-patterns/Low_Level_Design_Interview_Prep.md): [A Repeatable Interview Method](design-patterns/Low_Level_Design_Interview_Prep.md#2-a-repeatable-interview-method), [Machine-Coding Round Playbook](design-patterns/Low_Level_Design_Interview_Prep.md#27-machine-coding-round-playbook), worked designs ([Parking Lot](design-patterns/Low_Level_Design_Interview_Prep.md#5-worked-design-parking-lot) through [Inventory and Order Management](design-patterns/Low_Level_Design_Interview_Prep.md#26-worked-design-inventory-and-order-management)) | [Designing for Concurrency and Failure](design-patterns/Low_Level_Design_Interview_Prep.md#4-designing-for-concurrency-and-failure), [C++ Pattern Cheat Sheet](design-patterns/Design_Patterns_Cpp.md#53-pattern-cheat-sheet), [C++ Decision Guide](design-patterns/Design_Patterns_Cpp.md#55-decision-guide), [Python Pattern Cheat Sheet](design-patterns/Design_Patterns_Python.md#47-pattern-cheat-sheet), [SOLID](design-patterns/Design_Patterns_Cpp.md#2-design-principles-solid-and-beyond) | [LLD Practice Problems](practice/LLD_Practice_Problems.md) (20 timed machine-coding problems with runnable C++20/Python solutions), [LLD Communication and Practice Checklist](design-patterns/Low_Level_Design_Interview_Prep.md#28-interview-communication-and-practice-checklist), [Design Problems in LeetCode Patterns](computer-science/LeetCode_Patterns.md#26-design-problems) |
| **HLD / system design** | Requirements, estimation, architecture, tradeoffs, deep dives, failure handling | [High Level Design](computer-science/High_Level_Design.md): [Repeatable Process](computer-science/High_Level_Design.md#2-a-repeatable-interview-process), [Estimate the Workload](computer-science/High_Level_Design.md#3-estimate-the-workload), [Building Blocks](computer-science/High_Level_Design.md#4-architecture-building-blocks), [Cross-Cutting Decisions](computer-science/High_Level_Design.md#5-cross-cutting-design-decisions), [15 Worked Designs](computer-science/High_Level_Design.md#6-worked-system-designs) | [CS Fundamentals -- Distributed Systems](computer-science/CS_Fundamentals.md#8-distributed-systems), [Little's Law and Queueing](computer-science/Performance_Engineering.md#4-littles-law-and-queueing), [Tail Latency](computer-science/Performance_Engineering.md#1-latency-vs-throughput-percentiles-and-tail-latency), [Virtual Whiteboarding](career/Interview_Loops_and_Logistics.md#12-virtual-whiteboarding-for-design-rounds), [Checklists and Pitfalls](computer-science/High_Level_Design.md#7-interview-checklists-and-pitfalls) | [HLD Mock Interviews](practice/HLD_Mock_Interviews.md) (10 scripted mocks, [rubric by level](practice/HLD_Mock_Interviews.md#3-evaluation-rubric-by-level), 20 unsolved prompts), [HLD Practice Problems](practice/HLD_Practice_Problems.md) (20 problems with full model answers) |
| **ML / HPC system design** | Accelerator napkin math, parallelism choices, serving SLOs, cluster scheduling, telemetry at fleet scale | [ML and HPC Systems Design](ml-gpu/ML_Systems_Design.md): [Framework](ml-gpu/ML_Systems_Design.md#2-a-framework-for-ml-and-hpc-design-interviews), [Numbers to Know](ml-gpu/ML_Systems_Design.md#3-numbers-every-ml-systems-engineer-should-know), case studies on [LLM Serving](ml-gpu/ML_Systems_Design.md#4-case-study-llm-inference-serving-platform), [70B Training on 512 MI300X](ml-gpu/ML_Systems_Design.md#5-case-study-distributed-training-of-a-70b-model-on-512-mi300x), [GPU Cluster Scheduler](ml-gpu/ML_Systems_Design.md#6-case-study-gpu-cluster-job-scheduler), [Fleet-Wide GPU Profiling Service](ml-gpu/ML_Systems_Design.md#7-case-study-fleet-wide-gpu-profiling-and-telemetry-service) | [Training Memory Math: ZeRO](ml-gpu/ML_AI_Frameworks.md#45-training-memory-math-zero-activations-and-offload), [Collective Algorithms and Cost Model](ml-gpu/Parallel_GPU_Programming.md#34-collective-communication-algorithms-and-cost-model), [Megatron Tensor/Pipeline Parallelism](ml-gpu/ML_AI_Frameworks.md#40-tensor-parallelism), [HPC Interconnects](computer-science/CS_Fundamentals.md#210-hpc-and-datacenter-interconnects), [Slurm](tools/Linux_Command_Line.md#16-hpc-job-scheduling-with-slurm), [GPU Scheduling in Kubernetes](tools/Containers_and_CI.md#15-gpu-scheduling-device-plugins-node-selectors-and-taints) | [ML Systems Practice Prompts](ml-gpu/ML_Systems_Design.md#12-practice-prompts), HLD mocks [9: GPU Profiling Telemetry](practice/HLD_Mock_Interviews.md#12-mock-9-gpu-profiling-telemetry-service) and [10: LLM Inference Serving](practice/HLD_Mock_Interviews.md#13-mock-10-llm-inference-serving) |
| **GPU / HIP / profiling domain** | CDNA architecture, memory hierarchy, occupancy and latency hiding, counter-driven optimization, how profilers work, kernel tuning | [AMD GPU Architecture and Profiling](ml-gpu/AMD_GPU_Architecture_and_Profiling.md) (all sections, especially [Counter-Driven Methodology](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#5-counter-driven-performance-methodology), [How GPU Profilers Work Internally](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#6-how-gpu-profilers-work-internally), and the [Profiling-Tools Role Q&A](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#8-interview-qa-for-a-gpu-profiling-tools-role)), [GPU Kernel Case Studies](ml-gpu/GPU_Kernel_Case_Studies.md) | [Roofline Model](computer-science/Performance_Engineering.md#3-roofline-model), [Parallel and GPU Programming -- GPU Architecture](ml-gpu/Parallel_GPU_Programming.md#17-gpu-architecture-fundamentals), [HIP sections 25-30](ml-gpu/Parallel_GPU_Programming.md#25-hip-fundamentals-and-portability), [Wave-Level Primitives](ml-gpu/Parallel_GPU_Programming.md#36-portable-programming-models-and-amd-wave-level-primitives), [Timing GPUs](computer-science/Performance_Engineering.md#87-timing-gpus), [GPU Debuggers](tools/Debugging_and_Profiling_Tools.md#7-lldb-equivalents-and-gpu-debuggers), [Testing GPU/HIP Code](languages/CPP_Testing.md#41-testing-gpu--hip-code), [HIP and ROCm with CMake](tools/CMake_Fundamentals.md#64-hip-and-rocm-with-cmake), [Domain and Deep-Dive Rounds for GPU and HPC Roles](career/Interview_Loops_and_Logistics.md#11-domain-and-deep-dive-rounds-for-gpu-and-hpc-roles) | [Kernel Exercise List](ml-gpu/GPU_Kernel_Case_Studies.md#8-kernel-exercise-list) |
| **ML / LLM fundamentals** | Backprop, attention, transformer FLOP and memory math, KV cache, quantization, number formats, framework internals | [LLM and ML Fundamentals](ml-gpu/LLM_and_ML_Fundamentals.md), especially [Attention](ml-gpu/LLM_and_ML_Fundamentals.md#5-attention), [FLOP Accounting](ml-gpu/LLM_and_ML_Fundamentals.md#7-flop-accounting-and-scaling-laws), [FlashAttention](ml-gpu/LLM_and_ML_Fundamentals.md#8-flashattention), [Prefill, Decode, and the KV Cache](ml-gpu/LLM_and_ML_Fundamentals.md#9-prefill-decode-and-the-kv-cache), [Formula Cheat Sheet](ml-gpu/LLM_and_ML_Fundamentals.md#14-formula-cheat-sheet) | [ML and AI Frameworks](ml-gpu/ML_AI_Frameworks.md): [Autograd](ml-gpu/ML_AI_Frameworks.md#2-autograd-and-computational-graphs), [PyTorch Performance](ml-gpu/ML_AI_Frameworks.md#8-performance-optimization), [Triton](ml-gpu/ML_AI_Frameworks.md#25-triton-fundamentals), [vLLM and PagedAttention](ml-gpu/ML_AI_Frameworks.md#30-vllm-architecture-and-pagedattention); [Floating-Point Numerics](computer-science/Performance_Engineering.md#9-floating-point-numerics-and-reproducibility) | Q&A blocks at the end of each section; [Statistics for Engineers](computer-science/Math_Probability_Estimation.md#6-statistics-for-engineers) |
| **Behavioral** | Ownership, conflict, failure, influence, ambiguity, level-appropriate scope | [Behavioral Interview Prep](career/Behavioral_Interview_Prep.md): [STAR and CARL](career/Behavioral_Interview_Prep.md#2-answer-formats-star-and-carl), [Story Bank](career/Behavioral_Interview_Prep.md#3-building-your-story-bank), [Company Values](career/Behavioral_Interview_Prep.md#4-mapping-stories-to-company-values), [Question Bank](career/Behavioral_Interview_Prep.md#5-question-bank-by-competency) | [Failure and Conflict Frameworks](career/Behavioral_Interview_Prep.md#6-frameworks-for-failure-and-conflict-answers), [Tell Me About Yourself](career/Behavioral_Interview_Prep.md#7-tell-me-about-yourself-the-90-second-template), [Senior and Staff Signals](career/Behavioral_Interview_Prep.md#8-senior-and-staff-level-signals), [Anti-Patterns](career/Behavioral_Interview_Prep.md#9-anti-patterns) | [Rehearsal Plan and Final Checklist](career/Behavioral_Interview_Prep.md#11-rehearsal-plan-and-final-checklist) |
| **Project deep dive** | Explaining your own system end to end: architecture, design tradeoffs, your contribution, what you would change | [Project Deep Dive: rocprof-compute](career/Project_Deep_Dive_rocprof-compute.md): [The Pitches](career/Project_Deep_Dive_rocprof-compute.md#2-the-pitches), [Architecture Overview](career/Project_Deep_Dive_rocprof-compute.md#5-architecture-overview), [Key Design Tradeoffs](career/Project_Deep_Dive_rocprof-compute.md#10-key-design-tradeoffs), [Likely Interviewer Follow-Ups](career/Project_Deep_Dive_rocprof-compute.md#11-likely-interviewer-follow-ups) | [Profile Mode](career/Project_Deep_Dive_rocprof-compute.md#6-profile-mode-and-counter-collection), [Analyze Mode and the Metric Engine](career/Project_Deep_Dive_rocprof-compute.md#7-analyze-mode-and-the-metric-engine), [Speed-of-Light and Roofline](career/Project_Deep_Dive_rocprof-compute.md#8-speed-of-light-memory-chart-and-roofline), [How GPU Profilers Work Internally](ml-gpu/AMD_GPU_Architecture_and_Profiling.md#6-how-gpu-profilers-work-internally), [ML Systems: Fleet-Wide Profiling Service](ml-gpu/ML_Systems_Design.md#7-case-study-fleet-wide-gpu-profiling-and-telemetry-service) | [Your Story Templates](career/Project_Deep_Dive_rocprof-compute.md#12-your-story-templates), [Rehearsal Checklist](career/Project_Deep_Dive_rocprof-compute.md#13-rehearsal-checklist-and-pitfalls) |
| **Logistics / negotiation** | Loop formats, OAs, take-homes, debug and code-review rounds, leveling, compensation, negotiation | [Interview Loops and Logistics](career/Interview_Loops_and_Logistics.md): [Anatomy of a Loop](career/Interview_Loops_and_Logistics.md#2-anatomy-of-a-tech-interview-loop), [Company Loop Profiles](career/Interview_Loops_and_Logistics.md#3-company-loop-profiles), [Offer Evaluation](career/Interview_Loops_and_Logistics.md#13-offer-evaluation-compensation-mechanics), [Leveling Equivalences](career/Interview_Loops_and_Logistics.md#14-leveling-equivalences-across-companies), [Negotiation Strategy and Scripts](career/Interview_Loops_and_Logistics.md#15-negotiation-strategy-and-scripts) | [Online Assessments](career/Interview_Loops_and_Logistics.md#4-online-assessments), [Take-Homes](career/Interview_Loops_and_Logistics.md#5-take-home-assignments), [Debug-This-Code Rounds](career/Interview_Loops_and_Logistics.md#9-debug-this-code-rounds), [Code-Review Rounds](career/Interview_Loops_and_Logistics.md#10-code-review-rounds), [Questions to Ask](career/Interview_Loops_and_Logistics.md#16-questions-to-ask-your-interviewers) | [Preparation Checklists](career/Interview_Loops_and_Logistics.md#17-preparation-checklists), [Night-Before Cheat Sheet](practice/Night_Before_Cheat_Sheet.md) |

Tooling questions (Git, CMake, containers, CI) come up inside the C++, systems, and domain rounds rather than as a round of their own. For those, use the Q&A sections of [Git Fundamentals](tools/Git_Fundamentals.md#24-interview-qa), [CMake Fundamentals](tools/CMake_Fundamentals.md#72-interview-questions-and-answers), and [Containers and CI](tools/Containers_and_CI.md#24-scenario-interview-questions).

---

## 4. Directory Overview

### Top level

| File | Description |
|---|---|
| [README.md](README.md) | This index: round-to-file map, directory overview, and how to use the repo. |
| [STUDY_PLAN.md](STUDY_PLAN.md) | Prioritized multi-week study schedule, reading order for each target role, and a progress checklist. |
| [AGENTS.md](AGENTS.md) | Repository guidance for automated assistants (for example: do not generate HTML unless asked). |
| [scripts/md_to_html.py](scripts/md_to_html.py) | Converts every markdown file to standalone print-friendly HTML (see [Section 7](#7-printable-html-scriptsmd_to_htmlpy)). |
| [styles/print.css](styles/print.css) | Stylesheet that the HTML converter inlines into each page. |

### career/

| File | Description |
|---|---|
| [Behavioral_Interview_Prep.md](career/Behavioral_Interview_Prep.md) | STAR/CARL formats, story-bank construction, mapping stories to company values, 50+ questions by competency, senior/staff signals, and a rehearsal plan. |
| [Project_Deep_Dive_rocprof-compute.md](career/Project_Deep_Dive_rocprof-compute.md) | 30-second, 2-minute, and 10-minute pitches, architecture, profile/analyze modes, metric engine, roofline, design tradeoffs, and likely follow-ups for rocprof-compute. |
| [Interview_Loops_and_Logistics.md](career/Interview_Loops_and_Logistics.md) | Loop anatomy and company profiles, OAs, take-homes, coding/debug/code-review round execution, GPU/HPC domain rounds, comp mechanics, leveling, and negotiation scripts. |

### computer-science/

| File | Description |
|---|---|
| [CS_Fundamentals.md](computer-science/CS_Fundamentals.md) | Nine-part reference: OS (with Linux internals), networks (TCP internals, HPC interconnects), databases, OOP, system design basics, concurrency, computer architecture, distributed systems (Raft, leases, fencing), and security. |
| [DSA_Fundamentals.md](computer-science/DSA_Fundamentals.md) | Data structures and algorithms from arrays to max flow, with complexity cheat sheets, a data-structure chooser, number theory, and randomized algorithms. |
| [LeetCode_Patterns.md](computer-science/LeetCode_Patterns.md) | 33 coding patterns, each with when-to-use signals, templates, and worked problems, plus a pattern-selection flowchart and a quick-reference cheat sheet. |
| [High_Level_Design.md](computer-science/High_Level_Design.md) | System-design method, estimation numbers, building blocks (IDs, geo, Bloom filters, streams, CDC), cross-cutting concerns (SLOs, backpressure, deployment), and 15 worked designs. |
| [Performance_Engineering.md](computer-science/Performance_Engineering.md) | Latency percentiles, Amdahl/Gustafson, roofline, Little's law, cache-aware programming, SIMD, NUMA, benchmarking rigor, and floating-point reproducibility. |
| [Concurrency_Coding_Problems.md](computer-science/Concurrency_Coding_Problems.md) | LeetCode concurrency problems and classic live-coding tasks (blocking queue, RW lock, futex mutex, thread-safe LRU, thread pool, barrier, crawlers) in C++ and Python. |
| [Math_Probability_Estimation.md](computer-science/Math_Probability_Estimation.md) | Combinatorics, probability, expectation, distributions, statistics for engineers, classic puzzles, Monte Carlo checks, Fermi estimation, and handy numbers. |

### design-patterns/

| File | Description |
|---|---|
| [Design_Patterns_Cpp.md](design-patterns/Design_Patterns_Cpp.md) | SOLID, all 23 GoF patterns, C++ idioms (RAII, CRTP, pImpl, type erasure, NVI), architectural and concurrency patterns (thread pool, reactor, SPSC ring buffer, work stealing, RCU), and a decision guide. |
| [Design_Patterns_Python.md](design-patterns/Design_Patterns_Python.md) | The same pattern catalog in idiomatic Python, plus Python-specific idioms (protocols, decorators, descriptors, metaclasses, functools) and choosing a concurrency model under the GIL. |
| [Low_Level_Design_Interview_Prep.md](design-patterns/Low_Level_Design_Interview_Prep.md) | LLD method and evaluation criteria, concurrency and failure in object designs, 19 worked designs (parking lot to meeting scheduler), and a machine-coding playbook. |

### languages/

| File | Description |
|---|---|
| [Cpp_Fundamentals.md](languages/Cpp_Fundamentals.md) | C++ type system, pointers, memory, OOP, move semantics, templates, STL, C++11-20 features, concurrency, compilation and linking, UB, and implement-from-scratch exercises. |
| [CPP_Testing.md](languages/CPP_Testing.md) | GoogleTest and GoogleMock in depth, CMake/Bazel/CTest integration, coverage, sanitizers, fuzzing, testing concurrent and HIP code, golden files, Google Benchmark, Catch2/doctest, and mutation testing. |
| [Python_Fundamentals.md](languages/Python_Fundamentals.md) | Python data model, types, functions, generators, OOP and MRO, descriptors, typing, imports, GIL, multiprocessing, asyncio, CPython internals, gotchas, and C/C++ interop. |
| [Python_Libraries.md](languages/Python_Libraries.md) | NumPy in depth, GPU array interop (DLPack, CuPy), a pandas summary that points to Pandas.md, SciPy, matplotlib, pydantic v2, click/typer, requests/httpx, and PyQt. |
| [Pandas.md](languages/Pandas.md) | pandas from Series to internals: dtypes and Arrow, indexers, copy-on-write, groupby, reshaping, merges, time series, SQL-to-pandas translation, and performance. |
| [Rust_and_Go_for_Cpp_Programmers.md](languages/Rust_and_Go_for_Cpp_Programmers.md) | Rust ownership, traits, Result, Send/Sync, unsafe, FFI; Go goroutines, channels, context, interfaces, GC; side-by-side C++/Rust/Go code and a balanced "why not Rust?" answer. |

### ml-gpu/

| File | Description |
|---|---|
| [AMD_GPU_Architecture_and_Profiling.md](ml-gpu/AMD_GPU_Architecture_and_Profiling.md) | CDNA CU and chip architecture, GPU memory model, latency hiding, ROCm profiling tools, counter-driven methodology, profiler internals, GPU debugging, and a profiling-tools-role Q&A. |
| [GPU_Kernel_Case_Studies.md](ml-gpu/GPU_Kernel_Case_Studies.md) | Step-by-step HIP optimization ladders (reduction, transpose, scan, histogram, softmax/LayerNorm, tiled GEMM, fusion), each with a measurement harness, plus a kernel exercise list. |
| [Parallel_GPU_Programming.md](ml-gpu/Parallel_GPU_Programming.md) | MPI, OpenMP (including target offload), CUDA, HIP, CUDA-to-HIP porting, ROCm libraries, hybrid patterns, collective cost models, and multi-GPU HIP. |
| [ML_AI_Frameworks.md](ml-gpu/ML_AI_Frameworks.md) | PyTorch, TensorFlow, JAX, Triton, vLLM, SGLang, and Megatron-LM internals, with comparison tables and training memory math (ZeRO, activations, offload). |
| [LLM_and_ML_Fundamentals.md](ml-gpu/LLM_and_ML_Fundamentals.md) | ML basics, backprop, normalization and optimizers, attention and the decoder block, FLOP accounting, FlashAttention, KV cache, serving metrics, quantization, ML number formats, and mixed precision. |
| [ML_Systems_Design.md](ml-gpu/ML_Systems_Design.md) | ML/HPC design framework, accelerator and collective numbers, and case studies: LLM serving, 70B training, GPU cluster scheduler, fleet profiling telemetry, feature store, checkpointing, and recsys serving. |

### practice/

| File | Description |
|---|---|
| [Coding_Problem_List.md](practice/Coding_Problem_List.md) | 300-problem checklist by pattern (the original 150 plus 150 `ext` problems), each linked to its solution. Also Core 75, company-flavored lists, timed protocol, error log with spaced-repetition schedule, and a six-week coding plan. |
| [LeetCode_Solutions.md](practice/LeetCode_Solutions.md) | Python and C++ solutions, with intuition, complexity, and pitfalls, for the 111 checklist problems not worked in LeetCode Patterns. |
| [Cpp_Output_Quiz.md](practice/Cpp_Output_Quiz.md) | 55 "what does this print?" C++ puzzles on the object model, initialization, integers and floats, overloads, lifetimes, moves, containers, and ODR. |
| [Python_Output_Quiz.md](practice/Python_Output_Quiz.md) | 49 "what does this print?" Python puzzles on closures, aliasing, dicts, identity, exceptions, generators, scope, MRO, and async. |
| [SQL_and_Pandas_Exercises.md](practice/SQL_and_Pandas_Exercises.md) | 30 exercises on one sample schema, each solved in both SQL and pandas: ranking, anti-joins, NULL traps, hierarchies, streaks, sessions, time series, and product analytics. |
| [CS_Fundamentals_Drills.md](practice/CS_Fundamentals_Drills.md) | Numeric whiteboard problems (EAT, cache bits, subnetting, BDP, quorums, IEEE 754), 100 rapid-fire one-liners, and follow-up drill chains. |
| [HLD_Mock_Interviews.md](practice/HLD_Mock_Interviews.md) | A 45-minute self-mock format, a rubric by level, 10 scripted mocks (including GPU telemetry and LLM serving), and 20 unsolved prompts. |
| [HLD_Practice_Problems.md](practice/HLD_Practice_Problems.md) | 20 system design problems with full model answers (capacity math, APIs and schemas, architecture, deep dives, failure modes, tradeoffs, follow-ups, level signals): message queue, Google Docs, Dropbox, leaderboard, ad-click aggregation, stock exchange, Airbnb, flash sale, maps, Zoom, lock service, search engine, email, and more. |
| [LLD_Practice_Problems.md](practice/LLD_Practice_Problems.md) | 20 timed machine-coding problems with full solutions (class and flow diagrams, patterns, concurrency, runnable C++20/Python code with asserts, Q&A): ride-sharing, wallet ledger, order book, text editor, spreadsheet, circuit breaker, load balancer, workflow DAG, GPU caching allocator, profiler counter collection, and more. |
| [Flashcards.csv](practice/Flashcards.csv) | Question/answer flashcards covering the reference files, in CSV form for import into Anki or any spaced-repetition tool. |
| [Night_Before_Cheat_Sheet.md](practice/Night_Before_Cheat_Sheet.md) | Condensed last-minute review for the evening before a loop. |

### tools/

| File | Description |
|---|---|
| [Linux_Command_Line.md](tools/Linux_Command_Line.md) | Shell parsing, strict mode, expansions, redirection, job control, text-processing toolkit, SSH, tmux, systemd, disk/memory/network diagnostics, Slurm, and troubleshooting scenarios. |
| [Debugging_and_Profiling_Tools.md](tools/Debugging_and_Profiling_Tools.md) | GDB/LLDB, core dumps, hang debugging, perf and flame graphs, perf c2c, strace, ELF tools, Valgrind and sanitizers, eBPF/bpftrace, Python profilers, USE/RED, and bisecting. |
| [Git_Fundamentals.md](tools/Git_Fundamentals.md) | Git object model and internals, refs, index, packfiles, merge vs rebase, rerere, reflog recovery, bisect, worktrees, submodules, hooks, LFS, signing, and team workflows. |
| [CMake_Fundamentals.md](tools/CMake_Fundamentals.md) | Modern target-based CMake: targets and usage requirements, generator expressions, presets, toolchains, find_package and dependency managers, install/export, testing, sanitizers, HIP/ROCm, and RPATH. |
| [Containers_and_CI.md](tools/Containers_and_CI.md) | Namespaces, cgroups v2, OverlayFS, OCI, Docker, ROCm containers, Apptainer, Kubernetes with GPUs, CI/CD design, matrix builds, GPU runners, flaky tests, and supply chain. |

---

## 5. Practice Material

Reference files explain concepts. Practice files train recall and speed under time pressure. Every practice file keeps its solutions in a final `## Answers` section, so you can attempt each item before looking. The one exception is the coding checklist: its solutions are in [LeetCode Patterns](computer-science/LeetCode_Patterns.md) and [LeetCode_Solutions.md](practice/LeetCode_Solutions.md), and each checklist line links to its solution.

| Goal | File | Suggested cadence |
|---|---|---|
| Coding fluency | [Coding_Problem_List.md](practice/Coding_Problem_List.md), solutions in [LeetCode_Solutions.md](practice/LeetCode_Solutions.md) | 2-3 problems per day; follow the [timed protocol](practice/Coding_Problem_List.md#6-timed-practice-protocol) and log every attempt |
| C++ language traps | [Cpp_Output_Quiz.md](practice/Cpp_Output_Quiz.md) | 10 puzzles per session; write your predicted output before checking |
| Python language traps | [Python_Output_Quiz.md](practice/Python_Output_Quiz.md) | 10 puzzles per session |
| Data and SQL rounds | [SQL_and_Pandas_Exercises.md](practice/SQL_and_Pandas_Exercises.md) | Solve each exercise in SQL first, then pandas |
| CS recall and numeric reasoning | [CS_Fundamentals_Drills.md](practice/CS_Fundamentals_Drills.md) | 20 one-liners daily; 2 numeric problems on paper |
| System design | [HLD_Mock_Interviews.md](practice/HLD_Mock_Interviews.md), then [HLD_Practice_Problems.md](practice/HLD_Practice_Problems.md) | 1-2 timed 45-minute self-mocks per week, scored with the rubric |
| LLD / machine coding | [LLD_Practice_Problems.md](practice/LLD_Practice_Problems.md) | 1 problem per 60-90 minute session in your interview language; re-implement from a blank file after 7 days |
| ML/HPC design | [ML_Systems_Design.md -- Practice Prompts](ml-gpu/ML_Systems_Design.md#12-practice-prompts) | 1 per week for GPU/ML-infra targets |
| GPU kernels | [GPU_Kernel_Case_Studies.md -- Kernel Exercise List](ml-gpu/GPU_Kernel_Case_Studies.md#8-kernel-exercise-list) | Write, profile, and explain one kernel per week |
| Concurrency live coding | [Concurrency_Coding_Problems.md](computer-science/Concurrency_Coding_Problems.md) | Re-implement one primitive per session from a blank file |
| Long-term retention | [Flashcards.csv](practice/Flashcards.csv) | Daily reviews (see [Section 6](#6-using-this-repo-with-spaced-repetition)) |
| Final review | [Night_Before_Cheat_Sheet.md](practice/Night_Before_Cheat_Sheet.md) | The evening before each loop |

Mock interviews with another person are still the best check. Use the [self-practice mock format](practice/Coding_Problem_List.md#9-self-practice-mock-interview-format) and the [HLD rubric](practice/HLD_Mock_Interviews.md#3-evaluation-rubric-by-level) to score them.

---

## 6. Using This Repo with Spaced Repetition

Reading this material once does not mean you will recall it in an interview. Recall needs **active retrieval at growing intervals**. Use this workflow:

1. **Three item types, one schedule.** Every reference section ends with `**Q1.** ...` interview questions that have full answers. Together with the flashcards, the output quizzes, and logged coding problems, these are your review items.
2. **Retrieve, then check.** Cover the answer, say or write your answer in full (out loud for interview questions), and then compare. Grade yourself honestly: *A* (complete and fast), *B* (correct but slow or missing a follow-up), *C* (partial), *D* (could not answer).
3. **Schedule by grade.** A good default for the review intervals is **1, 3, 7, 14, and 30 days**. Items you grade A can skip ahead. A C or D sends the item back to day 1. Coding problems use the more detailed table in [Coding Problem List -- Spaced Repetition and the Error Log](practice/Coding_Problem_List.md#7-spaced-repetition-and-the-error-log), which includes a "due today" script.
4. **Flashcards in Anki (or similar).** Import [practice/Flashcards.csv](practice/Flashcards.csv) with File > Import (Anki 2.1.54 or later). The first four lines are Anki file headers (`#separator:comma`, `#html:false`, `#columns:front,back,tags`, `#tags column:3`), so Anki picks the separator, maps column 1 to Front and column 2 to Back, reads column 3 as tags (for example `cs::os`, a hierarchical tag), and treats `<` and `>` in answers as plain text. There is no header row of column names, so no bogus card is created. Other tools: delete the four `#` lines first, then import the rest as a three-column CSV. Anki's scheduler then handles the intervals. When you miss a Q&A item or a quiz puzzle, add a card for the specific trick you missed. Do not add a card for the whole topic.
5. **Keep one error log.** Record misses from every source (coding, quizzes, mocks, Q&A) in one CSV. Each Sunday, tally the root causes and pick next week's two focus areas. Feed what you learn back into the [STUDY_PLAN.md](STUDY_PLAN.md) progress checklist.
6. **Interleave.** Mix topics within each daily session, for example 2 coding problems, 10 flashcards, 5 quiz puzzles, and 2 Q&A answers from different files. Interleaving gives better retention for mixed-topic interview loops than studying one topic in a block.
7. **Taper before the loop.** In the last 3-4 days, stop learning new material. Review only items you have graded C or D, along with the [Night-Before Cheat Sheet](practice/Night_Before_Cheat_Sheet.md).

---

## 7. Printable HTML (scripts/md_to_html.py)

[scripts/md_to_html.py](scripts/md_to_html.py) turns every markdown file into a standalone, print-friendly HTML page, which you can print or save as PDF from a browser.

```bash
# One-time setup: Python-Markdown is required; Pygments is optional and adds syntax colors.
python3 -m pip install markdown pygments

# Run from anywhere. The script finds the repo root from its own location.
python3 scripts/md_to_html.py
```

What it does:

- Recursively finds every `*.md` file under the repo root, including this README.
- Converts each one with Python-Markdown (tables, fenced code, code highlighting, and heading ids via the `toc` extension).
- Caveat: Python-Markdown's default slug rules differ from GitHub's. They collapse runs of hyphens (GitHub keeps `--`, as in `#27-raii----resource-acquisition-is-initialization`) and suffix duplicate headings with `_1` instead of `-1`. Some in-page table-of-contents links therefore do not resolve in the HTML. GitHub rendering is the reference for anchors; the HTML is meant for printing and reading, not navigation.
- Inlines [styles/print.css](styles/print.css), so each page is a single self-contained file.
- Writes `Name.html` **next to** `Name.md`. For example, `languages/Cpp_Fundamentals.md` becomes `languages/Cpp_Fundamentals.html`.

The generated HTML is **local only**. `*.html` is listed in [.gitignore](.gitignore), so the output never shows up in commits. The markdown files are the only source of truth. Edit the `.md` files and regenerate. Never edit the HTML. Links between files still point to the `.md` targets, so for cross-file navigation, use the markdown on GitHub or in an editor.

---

## 8. Conventions

These conventions apply to every document in the repo, which makes the files easy to skim and to review:

- **Title and TOC.** Each file opens with a `# Title -- ...` heading and a `## Table of Contents` that uses GitHub-style anchors. Sections are numbered.
- **Versioned facts.** Each fast-moving file (`ml-gpu/*`, ROCm and tooling material, CMake) has a `> Last reviewed: ... · Versions assumed: ...` line under its title. Check it before relying on a specific flag or tool name.
- **Code.** Fenced blocks are tagged with their language (`cpp`, `python`, `bash`, `sql`, `mermaid`, `text`). Complete programs compile or run as written. Intentional fragments start with a `// fragment` or `# fragment` comment.
- **Interview Q&A.** `**Q1.** ...` blocks close each major section, with full answers, common follow-ups, and pitfalls.
- **Cross-links.** "See also" lines link related sections across files using relative paths.
- **Markdown only.** The repo contains no committed HTML and no raw HTML elements in documents. Practice files keep their solutions in a final `## Answers` section.
