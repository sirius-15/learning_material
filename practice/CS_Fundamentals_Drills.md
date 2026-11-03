# CS Fundamentals Drills -- Comprehensive Numeric Problems, Rapid-Fire Recall, and Follow-Up Chains

> Last reviewed: 2026-11 · Versions assumed: Linux 6.x, glibc 2.35+, GCC 13+ / Clang 17+ (`-std=c++20`), Python 3.12+, ROCm 6.x-7.x (HIP, ROCr, rocprofv3, rocprof-compute 3.x)

> A practice companion to [CS Fundamentals](../computer-science/CS_Fundamentals.md). Part 2 has numeric problems of the kind interviewers put on a whiteboard (EAT, cache bits, CPI, subnetting, BDP, quorums, IOPS, Little's law, IEEE 754, Gantt charts, Banker's, page replacement). Part 3 has 100 rapid-fire one-liners. Part 4 has four "and then what happens?" drill chains. Every answer, with step-by-step working, is in the final [Answers](#answers) section. Try each problem before you scroll.

---

## Table of Contents

1. [How to Use This File](#1-how-to-use-this-file)
2. [Numeric Problems](#2-numeric-problems)
   - [2.1 Effective Access Time with a TLB](#21-effective-access-time-with-a-tlb)
   - [2.2 Page-Table Sizing](#22-page-table-sizing)
   - [2.3 Cache Address Breakdown](#23-cache-address-breakdown)
   - [2.4 Cache Hit Rate and AMAT](#24-cache-hit-rate-and-amat)
   - [2.5 Pipeline CPI, Hazards, and Branch Penalties](#25-pipeline-cpi-hazards-and-branch-penalties)
   - [2.6 Amdahl's Law](#26-amdahls-law)
   - [2.7 Subnetting and CIDR](#27-subnetting-and-cidr)
   - [2.8 TCP Throughput and Bandwidth-Delay Product](#28-tcp-throughput-and-bandwidth-delay-product)
   - [2.9 Quorum Consistency](#29-quorum-consistency)
   - [2.10 Disk and SSD IOPS](#210-disk-and-ssd-iops)
   - [2.11 Little's Law](#211-littles-law)
   - [2.12 Back-of-Envelope QPS and Storage](#212-back-of-envelope-qps-and-storage)
   - [2.13 Floating-Point Representation](#213-floating-point-representation)
   - [2.14 Two's Complement](#214-twos-complement)
   - [2.15 CPU Scheduling Gantt Charts](#215-cpu-scheduling-gantt-charts)
   - [2.16 Banker's Algorithm](#216-bankers-algorithm)
   - [2.17 Page Replacement: FIFO, LRU, OPT, Belady](#217-page-replacement-fifo-lru-opt-belady)
3. [Rapid-Fire: 100 One-Liners](#3-rapid-fire-100-one-liners)
   - [3.1 Operating Systems (R1-R25)](#31-operating-systems-r1-r25)
   - [3.2 Networks (R26-R45)](#32-networks-r26-r45)
   - [3.3 Databases (R46-R62)](#33-databases-r46-r62)
   - [3.4 Computer Architecture (R63-R82)](#34-computer-architecture-r63-r82)
   - [3.5 Distributed Systems (R83-R100)](#35-distributed-systems-r83-r100)
4. [Follow-Up Drill Chains](#4-follow-up-drill-chains)
   - [Chain 1: What Happens When You Type a URL](#chain-1-what-happens-when-you-type-a-url)
   - [Chain 2: What Happens on malloc of 1 GB and Touching the Pages](#chain-2-what-happens-on-malloc-of-1-gb-and-touching-the-pages)
   - [Chain 3: What Happens When You Launch a HIP Kernel](#chain-3-what-happens-when-you-launch-a-hip-kernel)
   - [Chain 4: fork in a Multithreaded Program](#chain-4-fork-in-a-multithreaded-program)
5. [Interview Q&A: Working Numeric Problems Out Loud](#5-interview-qa-working-numeric-problems-out-loud)
- [Answers](#answers)
  - [A2.1 Effective Access Time with a TLB](#a21-effective-access-time-with-a-tlb)
  - [A2.2 Page-Table Sizing](#a22-page-table-sizing)
  - [A2.3 Cache Address Breakdown](#a23-cache-address-breakdown)
  - [A2.4 Cache Hit Rate and AMAT](#a24-cache-hit-rate-and-amat)
  - [A2.5 Pipeline CPI, Hazards, and Branch Penalties](#a25-pipeline-cpi-hazards-and-branch-penalties)
  - [A2.6 Amdahl's Law](#a26-amdahls-law)
  - [A2.7 Subnetting and CIDR](#a27-subnetting-and-cidr)
  - [A2.8 TCP Throughput and Bandwidth-Delay Product](#a28-tcp-throughput-and-bandwidth-delay-product)
  - [A2.9 Quorum Consistency](#a29-quorum-consistency)
  - [A2.10 Disk and SSD IOPS](#a210-disk-and-ssd-iops)
  - [A2.11 Little's Law](#a211-littles-law)
  - [A2.12 Back-of-Envelope QPS and Storage](#a212-back-of-envelope-qps-and-storage)
  - [A2.13 Floating-Point Representation](#a213-floating-point-representation)
  - [A2.14 Two's Complement](#a214-twos-complement)
  - [A2.15 CPU Scheduling Gantt Charts](#a215-cpu-scheduling-gantt-charts)
  - [A2.16 Banker's Algorithm](#a216-bankers-algorithm)
  - [A2.17 Page Replacement](#a217-page-replacement)
  - [A3 Rapid-Fire Answers](#a3-rapid-fire-answers)
  - [A4 Drill-Chain Model Answers](#a4-drill-chain-model-answers)

---

# 1. How to Use This File

| Goal | How |
|---|---|
| **Numeric fluency** (Part 2) | Time-box each problem to 3-5 minutes. Write the formula first, then plug in numbers, then sanity-check the units and the order of magnitude. Interviewers grade the setup more than the arithmetic. |
| **Recall speed** (Part 3) | Cover the answers and say each one aloud in one sentence. Mark any you hesitate on and re-drill them two days later. The same items are good candidates for `practice/Flashcards.csv`. |
| **Depth under pressure** (Part 4) | Have a friend read one chain question at a time and push "why?" or "what if it fails?" after each answer. A strong candidate can go 4-5 levels deep without hand-waving. |
| **Self-verification** | The answers include small Python/C++ programs (scheduling, page replacement, Banker's, IEEE 754, subnets) that reproduce the hand results. Run them, then change the inputs and predict the output before re-running. |

Conventions used in the problems:

- `KiB/MiB/GiB` are powers of two (2^10, 2^20, 2^30). `KB/MB/GB` and network rates (`Mbps`, `Gbps`) are powers of ten, unless a problem says otherwise. Interviewers usually accept either if you say which one you are using.
- "ns" and "cycles" are never mixed in one formula. Convert first.
- Scheduling: lower priority number means **higher** priority. Ties break by arrival time, then by process name.

> Theory refreshers live in [CS Fundamentals](../computer-science/CS_Fundamentals.md); the performance-modeling material (Amdahl, roofline, Little's law, cache-address breakdown) is expanded in [Performance Engineering](../computer-science/Performance_Engineering.md); estimation heuristics are in [Math, Probability, and Estimation](../computer-science/Math_Probability_Estimation.md#9-fermi-estimation).

---

# 2. Numeric Problems

## 2.1 Effective Access Time with a TLB

> Theory: [CS Fundamentals 1.3 Memory Management (TLB, EAT)](../computer-science/CS_Fundamentals.md#13-memory-management) · [7.6 Virtual Memory](../computer-science/CS_Fundamentals.md#76-virtual-memory) · Answers: [A2.1](#a21-effective-access-time-with-a-tlb)

**P1.** A system has a single-level page table held in memory. TLB lookup takes 10 ns and a memory access takes 100 ns. The TLB hit ratio is 80%. (a) What is the effective memory access time (EAT)? (b) What is it at a 98% hit ratio? (c) What is the slowdown versus a machine with no paging at all, in each case?

**P2.** An x86-64 machine uses 4-level page tables. TLB lookup is 1 ns, a memory access is 100 ns, and the TLB hit ratio is 99%. Assume no page-walk caches and that every page-table level is a memory access. What is the EAT? Then explain qualitatively how page-walk caches and huge pages change the answer.

**P3.** Ignore the TLB. Memory access time is 100 ns and servicing a page fault (disk read plus restart) takes 8 ms on average. What is the largest page-fault rate *p* (faults per memory access) that keeps the slowdown below 10%? Express it as "one fault every N accesses".

**P4.** A machine has a 2-level page table, a 20 ns TLB, and 100 ns memory. What TLB hit ratio is required for the EAT to be at most 130 ns?

**P5.** Combine everything. TLB time is negligible (overlapped with the cache), memory is 100 ns, the page table has 2 levels, the TLB hit ratio is 99%, and 1 in every 1,000,000 accesses causes a major page fault costing 10 ms. What is the EAT? Which term dominates, and what does that tell you about where to optimize?

## 2.2 Page-Table Sizing

> Theory: [CS Fundamentals 1.3 Paging](../computer-science/CS_Fundamentals.md#13-memory-management) · [7.6 Virtual Memory](../computer-science/CS_Fundamentals.md#76-virtual-memory) · Answers: [A2.2](#a22-page-table-sizing)

**P6.** A 32-bit virtual address space uses 4 KiB pages and 4-byte page-table entries (PTEs) in a single-level table. (a) How big is one process's page table? (b) How much memory do the page tables of 100 processes take?

**P7.** Same machine, but now a 2-level table with a 10/10/12 bit split (outer index / inner index / offset). A process uses 8 MiB of code+data starting at address 0, a 4 MiB heap immediately after it, and a 1 MiB stack at the top of the address space. How much memory do its page tables take? Compare with P6.

**P8.** x86-64 with 48-bit virtual addresses, 4 KiB pages, and 8-byte PTEs, where each table must fit in one 4 KiB page. (a) How many index bits per level and how many levels? (b) How large would a flat single-level table be? (c) How many bytes of page tables are needed to map 1 GiB of contiguous, 1 GiB-aligned memory with 4 KiB pages? With 2 MiB pages? With a 1 GiB page? (d) What changes with 57-bit addresses?

**P9.** (a) A machine has 16 GiB of physical memory, 4 KiB frames, and an inverted page table with 16-byte entries. How big is the table, and how does it scale with the number of processes? (b) Design a page table for a 40-bit virtual address space with 16 KiB pages and 8-byte PTEs, where each level must fit in one page. How many levels, and how many bits does each level use?

## 2.3 Cache Address Breakdown

> Theory: [CS Fundamentals 7.5 Cache](../computer-science/CS_Fundamentals.md#75-cache) · [Performance Engineering 5.2 Address Breakdown](../computer-science/Performance_Engineering.md#52-address-breakdown-tag-set-offset) · Answers: [A2.3](#a23-cache-address-breakdown)

Formulas you will use: `lines = capacity / line_size`, `sets = lines / ways`, `offset_bits = log2(line_size)`, `index_bits = log2(sets)`, `tag_bits = address_bits - index_bits - offset_bits`.

**P10.** A 32 KiB **direct-mapped** cache has 64-byte lines and 32-bit addresses. (a) Give the tag/index/offset widths. (b) Break address `0x12345678` into tag, index, and offset (in hex and decimal).

**P11.** A 32 KiB **4-way set-associative** cache has 64-byte lines and 48-bit physical addresses. (a) Give the widths. (b) Break down `0x7FFF12345ABC`.

**P12.** A 1 MiB **8-way** L2 has 64-byte lines and 40-bit physical addresses. Each line stores a tag, a valid bit, and a dirty bit; each set also has 7 bits of tree pseudo-LRU state. (a) Give the widths. (b) How much SRAM does the metadata take, in bytes and as a percentage of the data capacity?

**P13.** Two `float` arrays `a[4096]` and `b[4096]` start at physical addresses `0x10000` and `0x18000`. The loop is `for (i...) sum += a[i] * b[i];`. (a) With the 32 KiB direct-mapped cache from P10, what is the hit rate? Why? (b) What is the hit rate with a 32 KiB 2-way cache with the same line size? (c) Follow-up: why are L1 data caches so often exactly 32 KiB 8-way or 48 KiB 12-way with 4 KiB pages?

## 2.4 Cache Hit Rate and AMAT

> Theory: [CS Fundamentals 7.4 Memory Hierarchy](../computer-science/CS_Fundamentals.md#74-memory-hierarchy) · [Performance Engineering 5.3 Row-Major vs Column-Major](../computer-science/Performance_Engineering.md#53-row-major-vs-column-major-traversal) · Answers: [A2.4](#a24-cache-hit-rate-and-amat)

`AMAT = hit_time + miss_rate * miss_penalty`, applied recursively per level.

**P14.** L1 hit time is 1 ns, its miss rate is 5%, and the miss penalty (to memory) is 100 ns. (a) What is the AMAT? (b) What L1 hit rate gives an AMAT of 2 ns?

**P15.** L1: 4-cycle hit, 10% miss rate. L2: 12-cycle hit, 20% *local* miss rate. Memory: 200 cycles. (a) What is the AMAT? (b) What is the L2 *global* miss rate? (c) Which improvement helps more: halving the L1 miss rate, or halving memory latency?

**P16.** A 1024 x 1024 row-major `float` matrix (4 MiB) is summed. The L1 is 32 KiB, 8-way, with 64-byte lines. (a) What is the L1 hit rate for a row-wise traversal from a cold cache? (b) What is it for a column-wise traversal? Explain using the set index, not just "the cache is too small". (c) Name two fixes.

**P17.** A CPU has a base CPI of 1.0 with a perfect cache. Each instruction makes 1 instruction fetch and, on average, 0.4 data accesses. The I-cache miss rate is 2%, the D-cache miss rate is 5%, and the miss penalty is 100 cycles. (a) What is the real CPI? (b) How much faster would a perfect cache be?

## 2.5 Pipeline CPI, Hazards, and Branch Penalties

> Theory: [CS Fundamentals 7.3 Pipelining](../computer-science/CS_Fundamentals.md#73-pipelining) · [7.10 Out-of-Order Microarchitecture](../computer-science/CS_Fundamentals.md#710-out-of-order-superscalar-microarchitecture) · Answers: [A2.5](#a25-pipeline-cpi-hazards-and-branch-penalties)

`CPI = CPI_ideal + sum over stall sources (frequency * penalty)`; `time = instructions * CPI * cycle_time`.

**P18.** A classic 5-stage pipeline (IF ID EX MEM WB) has full forwarding. 20% of instructions are loads, and half of those are immediately followed by an instruction that uses the loaded value. 15% of instructions are branches, resolved in EX with predict-not-taken (2-cycle penalty when taken), and 60% of branches are taken. What is the CPI?

**P19.** A 4 GHz out-of-order core has a base CPI of 0.5 (IPC = 2). 20% of instructions are branches, prediction accuracy is 95%, and the misprediction penalty is 15 cycles. (a) What is the effective CPI, and what fraction of the performance is lost to mispredictions? (b) What if accuracy drops to 90% on a data-dependent branch? (c) How many instructions per second in each case?

**P20.** A non-pipelined datapath has stage delays of 200, 250, 150, 300, and 100 ps. Pipelining adds a 20 ps latch per stage. (a) What are the cycle time and the latency of one instruction, pipelined and unpipelined? (b) What is the speedup for 1,000,000 instructions? (c) Why is it not 5x?

**P21.** 20% of instructions are branches and 65% of those are taken. Design A resolves branches in MEM (3-cycle penalty, predict-not-taken). Design B moves resolution to ID (1-cycle penalty) but lengthens the clock period by 10%. Which design is faster, and by how much?

## 2.6 Amdahl's Law

> Theory: [Performance Engineering 2.2 Amdahl's Law](../computer-science/Performance_Engineering.md#22-amdahls-law) · [2.3 Gustafson's Law](../computer-science/Performance_Engineering.md#23-gustafsons-law) · Answers: [A2.6](#a26-amdahls-law)

`S(N) = 1 / ((1 - p) + p / N)`; Gustafson (scaled) `S(N) = N - s * (N - 1)` where `s` is the serial fraction of the *parallel* run.

**P22.** A program is 90% parallelizable. (a) What is the speedup on 16 cores, and the parallel efficiency? (b) What is the upper limit with infinitely many cores?

**P23.** You offload a kernel that is 70% of the runtime to a GPU, where it runs 20x faster. The host-device copies add time equal to 5% of the original runtime. (a) What is the overall speedup? (b) What would it be without the copy cost? (c) What one change would raise the ceiling most?

**P24.** (a) What parallel fraction do you need for an 8x speedup on 32 cores? (b) A weak-scaling run on 64 nodes spends 5% of its time in serial code. What is the Gustafson scaled speedup? (c) Why don't the two laws contradict each other?

## 2.7 Subnetting and CIDR

> Theory: [CS Fundamentals 2.5 IP Addressing](../computer-science/CS_Fundamentals.md#25-ip-addressing) · Answers: [A2.7](#a27-subnetting-and-cidr)

**P25.** For host `192.168.10.77/26`, give the subnet mask, network address, broadcast address, first and last usable host, and the number of usable hosts.

**P26.** Same questions for `10.20.30.40/20`.

**P27.** (VLSM) Split `172.16.0.0/24` into subnets for departments needing 100, 50, 20, and 2 hosts, allocating the largest first. List each subnet's CIDR and range. What address space is left?

**P28.** (a) Are `10.1.5.200/22` and `10.1.6.10/22` on the same subnet? (b) Summarize `192.168.0.0/24` through `192.168.3.0/24` into one route. (c) Can `192.168.1.0/24` and `192.168.2.0/24` be summarized into a single /23? Why or why not?

**P29.** (a) How many usable addresses are in an AWS VPC `/28` subnet, and why is that different from the textbook number? (b) What is special about `/31` and `/32`? (c) How many addresses are in an IPv6 `/64`, and why is `/64` the standard LAN size?

## 2.8 TCP Throughput and Bandwidth-Delay Product

> Theory: [CS Fundamentals 2.2 TCP vs UDP (congestion control)](../computer-science/CS_Fundamentals.md#22-tcp-vs-udp) · Answers: [A2.8](#a28-tcp-throughput-and-bandwidth-delay-product)

`throughput <= window / RTT`; `BDP = bandwidth * RTT`; Mathis et al. loss-limited throughput `~ (MSS / RTT) * (sqrt(3/2) / sqrt(p))`.

**P30.** A TCP connection has no window scaling (max window 65,535 bytes) and an RTT of 100 ms across a 1 Gbps path. What is the maximum throughput? What fraction of the link is that?

**P31.** A 10 Gbps link between two data centers has an 80 ms RTT. (a) What is the bandwidth-delay product? (b) What is the minimum window-scale shift? (c) On a Linux host with the default `net.ipv4.tcp_rmem` maximum of 6 MiB, roughly what throughput will one connection reach?

**P32.** A path has MSS = 1460 bytes, RTT = 50 ms, and a 0.01% packet-loss rate. Using the Mathis formula, what is the approximate maximum throughput of a single Reno-style TCP flow?

**P33.** Over a 100 Mbps, 50 ms RTT path (initial congestion window 10 segments of 1460 bytes, no loss), roughly how long does it take to (a) download a 1 GB file, and (b) download a 100 KB object on a fresh TCP connection (count RTTs)? (c) What does this tell you about small-object latency?

## 2.9 Quorum Consistency

> Theory: [CS Fundamentals 8.3 Replication Strategies (quorums)](../computer-science/CS_Fundamentals.md#83-replication-strategies) · [8.2 Consensus Algorithms](../computer-science/CS_Fundamentals.md#82-consensus-algorithms) · Answers: [A2.9](#a29-quorum-consistency)

**P34.** With N = 3 replicas, which of these (W, R) configurations guarantee that a read sees the latest acknowledged write: (2,2), (1,3), (3,1), (1,1), (2,1)? For each valid one, how many replica failures can reads and writes each tolerate?

**P35.** With N = 5: (a) for W = 3, R = 3, how many failures are tolerated? (b) For W = 4, R = 2? (c) Why do many systems also require W > N/2? (d) Name two ways a Dynamo-style system with W + R > N can still return stale data.

**P36.** Each node is independently up 99% of the time. What is the availability of a majority-quorum (Raft-style) cluster of 3, 4, and 5 nodes? What does the 4-node result tell you?

## 2.10 Disk and SSD IOPS

> Theory: [CS Fundamentals 7.7 Storage](../computer-science/CS_Fundamentals.md#77-storage) · Answers: [A2.10](#a210-disk-and-ssd-iops)

**P37.** A 7,200 RPM HDD has a 4 ms average seek time and 200 MB/s sustained transfer. (a) What is the average service time and IOPS for random 4 KiB reads? (b) What throughput is that in MB/s, compared with sequential reads?

**P38.** An NVMe SSD has 80 µs read latency at queue depth 1 and is rated at 1,000,000 random 4 KiB read IOPS. (a) What is the IOPS at QD1? (b) How many I/Os must be in flight to reach the rated IOPS? (c) What bandwidth does 1M IOPS x 4 KiB need, and is that plausible over PCIe 4.0 x4?

**P39.** Eight HDDs at 150 IOPS each are combined in RAID 0, RAID 10, RAID 5, and RAID 6. (a) Give the random-read and random-write IOPS of each. (b) For a 70% read / 30% write workload on RAID 5, what is the effective IOPS?

**P40.** A 3.84 TB SSD is rated at 1 drive write per day (DWPD) for 5 years. (a) What is its total-bytes-written (TBW) rating? (b) How long does it last if the host writes 2 TB/day? (c) What if an LSM-tree database writes 0.5 TB/day of user data with 10x write amplification?

## 2.11 Little's Law

> Theory: [Performance Engineering 4.1 Little's Law](../computer-science/Performance_Engineering.md#41-littles-law) · [4.4 Utilization vs Latency](../computer-science/Performance_Engineering.md#44-utilization-vs-latency-mm1-and-beyond) · Answers: [A2.11](#a211-littles-law)

`L = lambda * W` (items in system = arrival rate x time in system). For an M/M/1 queue, `R = S / (1 - rho)`.

**P41.** A web service handles 2,000 requests/s with a mean latency of 150 ms. (a) How many requests are in flight on average? (b) If it uses a thread-per-request model with a 200-thread pool, what is its maximum throughput, and what happens to latency when load exceeds it?

**P42.** DRAM latency is 100 ns. (a) If a core can track 16 outstanding 64-byte cache-line misses, what is its maximum memory bandwidth? (b) How many such cores does it take to saturate 200 GB/s? (c) An MI300X GPU has 5.3 TB/s of peak HBM bandwidth; assume a loaded memory latency of 500 ns. How many bytes must be in flight, and roughly how many per compute unit (304 CUs)? What does that imply for occupancy?

**P43.** (a) An app issues 4,000 DB queries/s, each holding a connection for 5 ms. What is the minimum connection-pool size, and what would you actually configure? (b) A single-server queue has a 10 ms service time. What is the mean response time at 50%, 90%, and 95% utilization (M/M/1)?

## 2.12 Back-of-Envelope QPS and Storage

> Theory: [CS Fundamentals 5.9 Back-of-the-Envelope Estimation](../computer-science/CS_Fundamentals.md#59-back-of-the-envelope-estimation) · [HLD 3. Estimate the Workload](../computer-science/High_Level_Design.md#3-estimate-the-workload) · [Powers of Two and Handy Numbers](../computer-science/Math_Probability_Estimation.md#10-powers-of-two-and-handy-numbers) · Answers: [A2.12](#a212-back-of-envelope-qps-and-storage)

**P44.** A photo-sharing app has 100M daily active users. Each uploads 0.1 photos/day on average (2 MB each) and views 50 photos/day (served as 200 KB resized versions). Estimate: upload QPS (average and peak), storage per day and over 5 years with 3x replication versus 1.5x erasure coding, read QPS, and egress bandwidth.

**P45.** A URL shortener creates 500M new links/month at about 500 bytes per record, with a 100:1 read:write ratio. Estimate the write QPS, read QPS, storage over 5 years, and whether 7 base62 characters are enough for the IDs.

**P46.** A fleet-wide GPU telemetry pipeline (think rocprof-style counters, always on): 10,000 GPUs each emit 200 counters sampled at 10 Hz, with 16 bytes per raw sample (8-byte timestamp + 8-byte value). Estimate points/s, raw ingest bandwidth, raw storage per day, and storage per day with Gorilla-style compression (about 1.37 bytes/point, as reported in Facebook's Gorilla paper).

## 2.13 Floating-Point Representation

> Theory: [CS Fundamentals 7.9 Endianness and Floating Point](../computer-science/CS_Fundamentals.md#79-endianness-and-floating-point) · [Performance Engineering 9. Floating-Point Numerics](../computer-science/Performance_Engineering.md#9-floating-point-numerics-and-reproducibility) · Answers: [A2.13](#a213-floating-point-representation)

FP32 layout: 1 sign bit, 8 exponent bits (bias 127), 23 fraction bits. `value = (-1)^s * 1.f * 2^(e - 127)` for normal numbers.

**P47.** Convert -13.625 to IEEE 754 single precision. Give the bit fields and the hex encoding.

**P48.** Decode these FP32 bit patterns: `0x3F800000`, `0xC0000000`, `0x40490FDB`, `0x7F800000`, `0x7FC00000`, `0x00800000`, `0x00000001`, `0x7F7FFFFF`.

**P49.** (a) Why is `0.1f` stored as `0x3DCCCCCD`, and what exact decimal value does it hold? (b) Why does `0.1 + 0.2 == 0.3` evaluate to false in double precision? (c) What is the largest integer N such that every integer in [0, N] is exactly representable in FP32? What happens to `16777217.0f`?

**P50.** Low precision, as used on GPUs. (a) Convert pi to FP16 and to BF16 (round to nearest even). (b) What does 100,000 become in FP16? (c) Give the spacing between 1.0 and the next representable number (ULP at 1.0) for FP32, FP16, and BF16, and the largest exactly-representable consecutive integer for FP16 and BF16. (d) What are the maximum finite values of FP8 E4M3 and E5M2 (OCP formats), and why do the two FP8 formats exist?

## 2.14 Two's Complement

> Theory: [CS Fundamentals 7.1 CPU Basics](../computer-science/CS_Fundamentals.md#71-cpu-basics) · Answers: [A2.14](#a214-twos-complement)

**P51.** (a) Encode -77 as an 8-bit two's-complement number (binary and hex). (b) What is the range of an n-bit signed integer? (c) Read `0xB3` as unsigned and as signed 8-bit. (d) Sign-extend the 8-bit value `0xF5` to 32 bits; what decimal value is it?

**P52.** In 8-bit arithmetic, compute (a) 100 + 50 and (b) -100 + -50. For each, give the 8-bit result, its signed value, and the carry (C) and overflow (V) flags. State the overflow-detection rule.

**P53.** Predict the output of this C++20 program, then explain each line. (The answer runs it.)

```cpp
#include <climits>
#include <cstdint>
#include <cstdio>

int main() {
    std::int8_t a = -77;
    std::printf("-77 as int8 bits   = 0x%02X\n", static_cast<unsigned>(static_cast<std::uint8_t>(a)));

    std::uint8_t u = 200;
    std::int8_t s = static_cast<std::int8_t>(u);   // modular since C++20; impl-defined before
    std::printf("(int8_t)200        = %d\n", s);

    std::int8_t x = static_cast<std::int8_t>(0xF5);
    std::int32_t widened = x;                       // sign extension
    std::printf("int8 0xF5 -> int32 = %d (0x%08X)\n", widened, static_cast<std::uint32_t>(widened));

    std::int8_t p = 100, q = 50;
    int promoted = p + q;                           // int8 operands promote to int: no overflow here
    std::int8_t wrapped = static_cast<std::int8_t>(p + q);
    std::printf("100 + 50: as int = %d, stored in int8 = %d\n", promoted, wrapped);

    int r;
    bool ovf = __builtin_add_overflow(INT_MAX, 1, &r);   // GCC/Clang builtin; INT_MAX + 1 itself is UB
    std::printf("INT_MAX + 1 overflow? %s (wrapped result %d)\n", ovf ? "yes" : "no", r);

    std::printf("-1 < 1u ? %s\n", (-1 < 1u) ? "true" : "false");   // -1 converts to UINT_MAX
    std::printf("-16 >> 2 = %d\n", -16 >> 2);                        // arithmetic shift (defined since C++20)
    std::printf("~5 = %d, -5 = %d\n", ~5, -5);                       // -x == ~x + 1
    return 0;
}
```

## 2.15 CPU Scheduling Gantt Charts

> Theory: [CS Fundamentals 1.2 CPU Scheduling](../computer-science/CS_Fundamentals.md#12-cpu-scheduling) · [1.12 The Linux Scheduler](../computer-science/CS_Fundamentals.md#112-the-linux-scheduler) · Answers: [A2.15](#a215-cpu-scheduling-gantt-charts)

Definitions: turnaround = completion - arrival; waiting = turnaround - burst; response = first run - arrival. For Round Robin, a process that arrives at the same instant a quantum expires joins the ready queue **before** the preempted process. Lower priority number = higher priority.

**Set A** (staggered arrivals):

| Process | Arrival | Burst | Priority |
|---|---|---|---|
| P1 | 0 | 8 | 3 |
| P2 | 1 | 4 | 1 |
| P3 | 2 | 9 | 2 |
| P4 | 3 | 5 | 4 |

**Set B** (all arrive at time 0):

| Process | Burst | Priority |
|---|---|---|
| P1 | 6 | 3 |
| P2 | 2 | 1 |
| P3 | 8 | 4 |
| P4 | 3 | 2 |
| P5 | 4 | 5 |

**P54.** For Set A, draw the Gantt chart and compute the average waiting and turnaround times under (a) FCFS, (b) non-preemptive SJF, and (c) SRTF (preemptive SJF).

**P55.** For Set A, do the same for (a) Round Robin with quantum 3 (also give the average response time) and (b) preemptive priority. Which process suffers under preemptive priority, and what fixes it?

**P56.** For Set B, compute the average waiting time under FCFS, SJF, non-preemptive priority, RR with q = 2, and RR with q = 4. Rank the policies.

**P57.** (Convoy effect) Three jobs arrive at time 0 in the order P1 (24), P2 (3), P3 (3). Compute the FCFS average waiting time, then the same with the order reversed (P2, P3, P1), then RR with q = 4. Explain the "convoy effect".

## 2.16 Banker's Algorithm

> Theory: [CS Fundamentals 1.4 Deadlocks (Banker's)](../computer-science/CS_Fundamentals.md#14-deadlocks) · Answers: [A2.16](#a216-bankers-algorithm)

Five processes share three resource types with totals A = 10, B = 6, C = 7.

| Process | Allocation (A B C) | Max (A B C) |
|---|---|---|
| P0 | 1 1 0 | 5 3 2 |
| P1 | 2 0 1 | 3 2 2 |
| P2 | 3 1 1 | 7 2 3 |
| P3 | 0 2 1 | 2 4 2 |
| P4 | 1 0 2 | 4 2 4 |

**P58.** (a) Compute the Need matrix and the Available vector. (b) Is the state safe? Give a safe sequence. (c) Starting from the original state each time, should each of these requests be granted: P3 requests (1,0,1); P2 requests (2,1,1); P4 requests (3,0,0); P0 requests (1,2,0); P1 requests (2,0,0)?

**P59.** (Single resource) A system has 12 tape drives. P0 holds 5 (max 10), P1 holds 2 (max 4), and P2 holds 2 (max 9). (a) Is the state safe? (b) If P2 requests and is granted one more drive, is the state still safe?

## 2.17 Page Replacement: FIFO, LRU, OPT, Belady

> Theory: [CS Fundamentals 1.3 Page Replacement Algorithms](../computer-science/CS_Fundamentals.md#13-memory-management) · Answers: [A2.17](#a217-page-replacement)

**P60.** For the reference string `7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1` with 3 frames (initially empty), count the page faults under FIFO, LRU, and OPT. Show the frame contents.

**P61.** (Belady's anomaly) For `1 2 3 4 1 2 5 1 2 3 4 5`, count FIFO faults with 3 frames and with 4 frames. Then do the same for LRU and OPT. Why can't LRU show the anomaly?

**P62.** Run the Clock (second-chance) algorithm on the P60 string with 3 frames. A page's reference bit is set when it is loaded and on every hit; the hand starts at frame 0. How many faults are there, and where does Clock land relative to FIFO and LRU?

**P63.** (a) Suppose the P60 string's LRU fault rate held for a real workload with 100 ns memory and 5 ms fault service. What would the EAT be? (b) What is the working set W(t, delta) at t = 10 (the 10th reference, 1-indexed) with delta = 5? What does the working-set model do with this number?

---

# 3. Rapid-Fire: 100 One-Liners

Answer each in one or two sentences, out loud, in under 15 seconds. Answers: [A3 Rapid-Fire Answers](#a3-rapid-fire-answers).

## 3.1 Operating Systems (R1-R25)

> Theory: [CS Fundamentals 1. Operating Systems](../computer-science/CS_Fundamentals.md#1-operating-systems)

- **R1.** What is the difference between a process and a thread?
- **R2.** What state does a context switch save and restore?
- **R3.** Why is a thread switch cheaper than a process switch?
- **R4.** What is a zombie process?
- **R5.** What is an orphan process, and who reaps it?
- **R6.** What does `fork()` return, and to whom?
- **R7.** What is copy-on-write?
- **R8.** What survives an `exec()` call?
- **R9.** Which two signals cannot be caught, blocked, or ignored?
- **R10.** What does "async-signal-safe" mean? Give one safe and one unsafe function.
- **R11.** What is the difference between a minor and a major page fault?
- **R12.** What is thrashing?
- **R13.** What is Belady's anomaly?
- **R14.** Internal vs external fragmentation?
- **R15.** Name the four Coffman conditions.
- **R16.** What is the most practical way to prevent deadlock in application code?
- **R17.** Mutex vs semaphore?
- **R18.** Why must a condition-variable wait sit inside a `while` loop?
- **R19.** What is priority inversion, and what is the standard fix?
- **R20.** What is a futex?
- **R21.** What exactly does the TLB cache?
- **R22.** Why are page tables multi-level?
- **R23.** What is the page cache?
- **R24.** What does `fsync` guarantee that `write` does not?
- **R25.** `MAP_SHARED` vs `MAP_PRIVATE`?

## 3.2 Networks (R26-R45)

> Theory: [CS Fundamentals 2. Computer Networks](../computer-science/CS_Fundamentals.md#2-computer-networks)

- **R26.** Name the four layers of the TCP/IP model.
- **R27.** Describe the TCP three-way handshake with sequence numbers.
- **R28.** Why does TIME_WAIT exist, which side enters it, and for how long on Linux?
- **R29.** A server has thousands of sockets in CLOSE_WAIT. What does that mean?
- **R30.** Flow control vs congestion control?
- **R31.** What is TCP slow start?
- **R32.** What does Nagle's algorithm do, and when do you disable it?
- **R33.** TCP vs UDP in one sentence?
- **R34.** Why does DNS mostly use UDP, and when does it use TCP?
- **R35.** A vs AAAA vs CNAME records?
- **R36.** How many usable hosts are in a /27?
- **R37.** What does ARP do?
- **R38.** What does NAT do?
- **R39.** The main improvement of HTTP/2 over HTTP/1.1?
- **R40.** Why does HTTP/3 run over QUIC instead of TCP?
- **R41.** How many round trips does a TLS 1.3 handshake take?
- **R42.** What does a TLS certificate prove?
- **R43.** L4 vs L7 load balancer?
- **R44.** What is the bandwidth-delay product, and why does it matter?
- **R45.** `select`/`poll` vs `epoll`?

## 3.3 Databases (R46-R62)

> Theory: [CS Fundamentals 3. Database Systems](../computer-science/CS_Fundamentals.md#3-database-systems)

- **R46.** What does ACID stand for?
- **R47.** List the four SQL isolation levels, weakest to strongest.
- **R48.** Which anomaly does snapshot isolation still allow?
- **R49.** Default isolation level in PostgreSQL vs MySQL InnoDB?
- **R50.** Clustered vs secondary (non-clustered) index?
- **R51.** Why do databases use B+ trees for indexes?
- **R52.** What is a covering index?
- **R53.** Given a composite index on `(a, b)`, does `WHERE b = ?` use it efficiently?
- **R54.** What is a write-ahead log (WAL)?
- **R55.** What is MVCC?
- **R56.** What is two-phase locking (2PL)?
- **R57.** How does optimistic locking work in SQL?
- **R58.** What does `SELECT ... FOR UPDATE` do?
- **R59.** Third normal form (3NF) in one line?
- **R60.** LSM tree vs B-tree?
- **R61.** What role do Bloom filters play in an LSM tree?
- **R62.** What is the N+1 query problem?

## 3.4 Computer Architecture (R63-R82)

> Theory: [CS Fundamentals 7. Computer Architecture](../computer-science/CS_Fundamentals.md#7-computer-architecture)

- **R63.** Name the "three C's" of cache misses (plus the fourth for multiprocessors).
- **R64.** Write-back vs write-through?
- **R65.** What are the MESI states?
- **R66.** What is false sharing, and how do you fix it?
- **R67.** Rough latencies of L1, L2, L3, and DRAM on a modern x86 server?
- **R68.** Wavefront size on AMD CDNA (Instinct) vs RDNA GPUs?
- **R69.** What is a VIPT cache, and how does it constrain L1 size?
- **R70.** Name the three data-hazard types. Which ones does register renaming remove?
- **R71.** What is forwarding (bypassing)?
- **R72.** What does a load-use hazard cost in a 5-stage pipeline with forwarding?
- **R73.** What does the reorder buffer (ROB) do?
- **R74.** Typical branch-misprediction penalty on a modern x86 core?
- **R75.** What is SMT?
- **R76.** RISC vs CISC today?
- **R77.** Little-endian vs big-endian? Which is network byte order?
- **R78.** What are the smallest positive normal FP32 value and FP32 machine epsilon?
- **R79.** Why is `0.1 + 0.2 != 0.3`?
- **R80.** Is floating-point addition associative? Why does it matter on GPUs?
- **R81.** What is a memory fence?
- **R82.** State Amdahl's law.

## 3.5 Distributed Systems (R83-R100)

> Theory: [CS Fundamentals 8. Distributed Systems](../computer-science/CS_Fundamentals.md#8-distributed-systems)

- **R83.** State the CAP theorem precisely.
- **R84.** What does PACELC add?
- **R85.** What quorum condition makes reads see the latest write?
- **R86.** How many failures does a 5-node Raft cluster tolerate?
- **R87.** Why are consensus clusters usually odd-sized?
- **R88.** What does the FLP impossibility result say?
- **R89.** How many nodes do you need to tolerate f Byzantine faults?
- **R90.** Linearizability vs sequential consistency?
- **R91.** Lamport clock vs vector clock?
- **R92.** What is the main weakness of two-phase commit?
- **R93.** What is a saga?
- **R94.** Is exactly-once delivery possible?
- **R95.** What does consistent hashing buy you?
- **R96.** What is a fencing token?
- **R97.** What is split brain, and how is it prevented?
- **R98.** How fast does a gossip protocol spread an update?
- **R99.** What is an idempotency key?
- **R100.** What are the three states of a circuit breaker?

---

# 4. Follow-Up Drill Chains

Each chain starts with an open question and then drills deeper. Indented questions are the follow-ups an interviewer asks after your previous answer. Practice answering a level fully before moving on, and be ready for "how would you observe that?" at any level. Model answers: [A4 Drill-Chain Model Answers](#a4-drill-chain-model-answers).

## Chain 1: What Happens When You Type a URL

> Theory: [CS Fundamentals 2.4 DNS](../computer-science/CS_Fundamentals.md#24-dns-domain-name-system) · [2.8 TLS/SSL Handshake](../computer-science/CS_Fundamentals.md#28-tlsssl-handshake) · [2.3 HTTP/HTTPS](../computer-science/CS_Fundamentals.md#23-http--https)

- **C1.1** You type `https://www.example.com/search?q=gpu` into a browser and press Enter. Walk me through what happens, end to end.
  - **C1.2** Before any packet leaves the machine, what does the browser check?
  - **C1.3** How is `www.example.com` resolved to an IP address?
    - **C1.3a** DNS uses UDP. What if the response does not fit?
    - **C1.3b** You changed the DNS record to fail over to a new IP, but some users still hit the old one for an hour. Why?
    - **C1.3c** How does a CDN send you to a nearby edge?
  - **C1.4** The resolver is at `8.8.8.8`. How does the first packet physically leave your laptop and get there?
  - **C1.5** Describe the TCP handshake. What happens if the SYN is lost?
  - **C1.6** Now TLS 1.3. What is in the ClientHello, and how is the server authenticated?
    - **C1.6a** An attacker controls the coffee-shop Wi-Fi. Why can't they read or alter your traffic?
    - **C1.6b** The server certificate expired yesterday. What happens?
  - **C1.7** Which HTTP version is used, and how is that negotiated?
  - **C1.8** Count the round trips before the first response byte on a cold connection, for TCP + TLS 1.3 and for QUIC. What about a resumed connection?
  - **C1.9** What happens on the server side, from the edge to the database?
  - **C1.10** The HTML arrives. What does the browser do to put pixels on screen?
  - **C1.11** Users say the page is slow. How do you find out where the time goes?

## Chain 2: What Happens on malloc of 1 GB and Touching the Pages

> Theory: [CS Fundamentals 1.11 Linux Memory Management Internals](../computer-science/CS_Fundamentals.md#111-linux-memory-management-internals) · [Performance Engineering 5.8 TLB Effects and Huge Pages](../computer-science/Performance_Engineering.md#58-tlb-effects-and-huge-pages)

- **C2.1** On x86-64 Linux with glibc, `char *p = static_cast<char*>(malloc(1UL << 30));`. What does glibc do?
  - **C2.2** What does the kernel do for that request? How do VSZ and RSS change?
  - **C2.3** Can this succeed on a machine with only 512 MB of free RAM? What controls that?
  - **C2.4** Now `memset(p, 0, 1UL << 30)`. Trace what happens on the very first byte written.
    - **C2.4a** How many page faults happen in total, and roughly how long do they take?
    - **C2.4b** What if the program only *reads* the buffer, never writes?
    - **C2.4c** On a 2-socket server, which NUMA node's memory backs the pages?
  - **C2.5** After the buffer is populated, a random-access loop over it is slow. What hardware structure is suffering, and how do you fix it?
  - **C2.6** Halfway through the `memset`, the machine runs out of memory. What happens?
  - **C2.7** You call `free(p)`. Does RSS go down? Would it for a 100-byte allocation?
  - **C2.8** `calloc(1, 1UL << 30)` versus `malloc` + `memset`: which is faster, and why?
  - **C2.9** You now `hipMemcpy` this buffer to the GPU. Why is it slower than copying from `hipHostMalloc` memory?
  - **C2.10** How would you observe each of these steps on a live process?

## Chain 3: What Happens When You Launch a HIP Kernel

> Theory: [Parallel and GPU Programming 26. HIP Programming Model](../ml-gpu/Parallel_GPU_Programming.md#26-hip-programming-model) · [22. Streams, Events, and Concurrency](../ml-gpu/Parallel_GPU_Programming.md#22-streams-events-and-concurrency) · [AMD GPU Architecture and Profiling](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md)

- **C3.1** `myKernel<<<grid, block, 0, stream>>>(d_out, d_in, n);` What does `hipcc` turn this line into?
  - **C3.2** Where does the GPU machine code live in the executable, and how does the runtime find the right version for the GPU in the machine?
  - **C3.3** What does the HIP runtime do when the launch call executes?
  - **C3.4** How does the dispatch reach the GPU? Is there a system call per launch?
  - **C3.5** What does the GPU do with the dispatch?
    - **C3.5a** What limits how many workgroups can be resident on one CU at a time?
  - **C3.6** When does the launch call return, and how does the host know the kernel finished?
  - **C3.7** The kernel writes out of bounds. When and where does the error show up, and how do you pin it to the right launch?
  - **C3.8** How expensive is a launch, and how do you reduce the overhead for many tiny kernels?
  - **C3.9** How does a profiler such as rocprofv3 or rocprof-compute see this launch?
    - **C3.9a** Why does collecting many hardware counters require running the application several times?
  - **C3.10** The first launch of a kernel is much slower than later ones. Why, and what does that mean for benchmarking?

## Chain 4: fork in a Multithreaded Program

> Theory: [CS Fundamentals 1.9 Linux Process Lifecycle, Signals, and File Descriptors](../computer-science/CS_Fundamentals.md#19-linux-process-lifecycle-signals-and-file-descriptors) · [Concurrency Coding Problems](../computer-science/Concurrency_Coding_Problems.md)

- **C4.1** A process with 8 threads calls `fork()`. What does the child contain?
  - **C4.2** At the moment of the fork, another thread held a mutex inside your logging library. What happens when the child logs a message?
  - **C4.3** So what is the child allowed to do before it calls `exec`?
  - **C4.4** What is `pthread_atfork`, and why is it rarely a complete fix?
  - **C4.5** What happens to file descriptors, and what race does `O_CLOEXEC` fix?
  - **C4.6** The parent is a 20 GiB in-memory database that forks to snapshot itself. What does the fork cost, and what can go wrong while the child runs?
  - **C4.7** What safer alternatives to `fork()` exist for "run a subprocess" in a threaded program?
  - **C4.8** What happens to signal handlers, the signal mask, pending signals, timers, and file locks?
  - **C4.9** The parent initialized HIP (or CUDA) and then forked worker processes that call `hipMalloc`. What goes wrong?
  - **C4.10** How does Python's `multiprocessing` deal with all this?

---

# 5. Interview Q&A: Working Numeric Problems Out Loud

**Q1.** The interviewer gives you an EAT problem but does not mention the TLB lookup time. What do you do?

State an assumption out loud and pick the one that matches the hardware: "Modern TLBs are looked up in parallel with the L1 cache, so I'll treat the TLB time as zero and count only memory accesses." Then show that the answer barely changes if the TLB took 1-2 ns. Interviewers mostly check that you know the miss path costs `levels + 1` memory accesses, not that you guess their hidden constant.

**Q2.** You get a number that seems off by 1000x. How do you check it quickly?

Do a units pass (ns vs µs vs ms; bits vs bytes; KiB vs KB) and an order-of-magnitude pass against anchors: 1 day is about 10^5 s, a memory access is about 100 ns, an SSD read is about 100 µs, a disk seek is about 5-10 ms, a same-region RTT is about 0.5 ms, and a cross-continent RTT is about 50-150 ms. Most "1000x" errors are a ms-vs-µs slip or a factor of 8 from bits vs bytes.

**Q3.** Why do interviewers like scheduling and page-replacement hand simulations if real kernels do not use these algorithms directly?

They test whether you can execute a precise algorithm without skipping steps (tie-breaking, arrival order, when a preempted job re-enters the queue), and they lead into real follow-ups: why SRTF is optimal for average waiting time but impractical, why Linux approximates LRU with active and inactive lists, and why CFS/EEVDF replaced fixed priorities. Say the tie-breaking rule before you start; it is the most common source of disagreement.

**Q4.** When should you stop computing exactly and round?

When the remaining precision cannot change a design decision. For capacity estimates, round to one significant figure, use 1 day of about 10^5 s, and carry powers of ten. For EAT, CPI, AMAT, and IEEE 754 problems, compute exactly, because the interviewer has a specific answer and the setup is the whole point.

**Q5.** What is the most common mistake in subnetting questions?

Forgetting that the network and broadcast addresses are not usable hosts (so /26 has 62 hosts, not 64), and computing the block size in the wrong octet. The fast method is `block = 256 - mask_octet` in the "interesting" octet; the network address is the largest multiple of the block not exceeding the host's octet value.

---

## Answers

### A2.1 Effective Access Time with a TLB

**P1.** On a hit, the cost is the TLB lookup plus one memory access. On a miss, it is the TLB lookup, then one access to read the PTE, then the data access.

```text
hit  = 10 + 100        = 110 ns
miss = 10 + 100 + 100  = 210 ns
(a) EAT = 0.80 * 110 + 0.20 * 210 = 88 + 42    = 130 ns   -> 30% slower than 100 ns
(b) EAT = 0.98 * 110 + 0.02 * 210 = 107.8 + 4.2 = 112 ns  -> 12% slower
```

Takeaway: the TLB's hit ratio is what makes paging affordable. Real data TLBs hit 99%+ on most workloads; the pathological cases are random access over huge footprints (hash tables, graph analytics, sparse GPU gathers).

**P2.** With 4 levels, a miss costs 4 page-table reads plus the data access.

```text
hit  = 1 + 100           = 101 ns
miss = 1 + 4 * 100 + 100 = 501 ns
EAT  = 0.99 * 101 + 0.01 * 501 = 99.99 + 5.01 = 105.0 ns
```

In practice the miss is far cheaper than 400 ns. **Paging-structure (page-walk) caches** hold upper-level entries (PML4/PDPT/PD), so most walks need only the last level. The PTEs themselves are ordinary cacheable data and often hit in L1/L2. Typical walk costs are tens of cycles, not hundreds of nanoseconds. **Huge pages** help twice: a 2 MiB page removes one level from the walk, and each TLB entry covers 512x more memory (64 entries x 4 KiB = 256 KiB of reach versus 64 x 2 MiB = 128 MiB). See [Performance Engineering 5.8](../computer-science/Performance_Engineering.md#58-tlb-effects-and-huge-pages).

**P3.**

```text
EAT = (1 - p) * 100 ns + p * 8,000,000 ns <= 110 ns
100 + 7,999,900 p <= 110
p <= 10 / 7,999,900 ~= 1.25e-6   -> at most one fault per ~800,000 accesses
```

This is why a workload that starts major-faulting falls off a cliff. Each disk-backed fault costs as much as 80,000 memory accesses (8 ms / 100 ns). With NVMe at ~100 µs the cliff is gentler but still about 1000x.

**P4.**

```text
hit  = 20 + 100            = 120 ns
miss = 20 + 2 * 100 + 100  = 320 ns
120 h + 320 (1 - h) <= 130  ->  320 - 200 h <= 130  ->  h >= 0.95
```

A TLB hit ratio of at least 95% is required.

**P5.**

```text
no-fault access = 0.99 * 100 + 0.01 * (2 * 100 + 100) = 99 + 3 = 102 ns
fault term      = 1e-6 * 10 ms = 1e-6 * 1e7 ns           = 10 ns
EAT ~= (1 - 1e-6) * 102 + 1e-6 * 1e7 ~= 112 ns
```

TLB misses add 2 ns over the ideal 100 ns. One major fault per million accesses adds 10 ns, five times more. Optimize the fault rate first (more RAM, `mlock`/pre-faulting, avoiding swap, smaller working set), then TLB reach (huge pages).

### A2.2 Page-Table Sizing

**P6.** `2^32 / 2^12 = 2^20` entries x 4 B = **4 MiB per process**. For 100 processes that is **400 MiB**, almost all of it describing unmapped address space. That waste is why flat tables are not used.

**P7.** The outer table has 1024 entries x 4 B = 4 KiB. Each inner table is also 4 KiB and maps 1024 x 4 KiB = 4 MiB of address space.

| Region | Range | Inner tables needed |
|---|---|---|
| Code + data | 0 - 8 MiB | 2 |
| Heap | 8 - 12 MiB | 1 |
| Stack | top 1 MiB | 1 (a whole 4 MiB slot) |
| Outer table | -- | 1 |

Total: 5 pages = **20 KiB**, about 200x less than the 4 MiB flat table. The point of a multi-level table is that page tables are allocated only for regions of address space that are actually used.

**P8.**
- (a) 4096 / 8 = 512 entries per table = **9 bits per level**. 48 - 12 = 36 bits of virtual page number, and 36 / 9 = **4 levels** (PML4, PDPT, PD, PT).
- (b) Flat: 2^36 entries x 8 B = **512 GiB** per process. That is impossible, hence the hierarchy.
- (c) Mapping 1 GiB, aligned:

| Page size | Leaf entries | Page-table memory |
|---|---|---|
| 4 KiB | 262,144 PTEs x 8 B = 2 MiB (512 PT pages) | 2 MiB + 1 PD + 1 PDPT + 1 PML4 = **2 MiB + 12 KiB** |
| 2 MiB | 512 PDEs = exactly one PD page | PD + PDPT + PML4 = **12 KiB** |
| 1 GiB | 1 PDPT entry | PDPT + PML4 = **8 KiB** |

- (d) With 57-bit addresses (Intel LA57, 5-level paging), 57 = 12 + 5 x 9, so there are **5 levels** (PML5 added) and 128 PiB of virtual address space. A TLB miss can now cost one more memory access, so Linux enables it only on hardware that supports it, and user space gets addresses above 47 bits only if it asks for them with an `mmap` hint.

**P9.**
- (a) 16 GiB / 4 KiB = 4 Mi frames x 16 B = **64 MiB**, about 0.4% of RAM. There is one table for the whole system, so its size depends on physical memory, not on the number of processes. The costs: a lookup must search by (PID, VPN), which in practice means a hash table plus collision chains, and shared memory is awkward because one frame has only one entry. PowerPC's hashed page table is the classic real-world example.
- (b) A 16 KiB page gives a 14-bit offset. Each table holds 16 KiB / 8 B = 2048 entries, so 11 bits per level. The VPN has 40 - 14 = 26 bits, and ceil(26 / 11) = **3 levels**, split as **4 + 11 + 11** (the top level has only 16 entries). Always put the partially used level at the top: the smaller table is the one that exists only once.

### A2.3 Cache Address Breakdown

**P10.** 32 KiB / 64 B = 512 lines; direct-mapped, so 512 sets.
- (a) offset = log2(64) = **6**, index = log2(512) = **9**, tag = 32 - 15 = **17** bits.
- (b) `0x12345678` = `0001 0010 0011 0100 0101 0110 0111 1000`

```text
offset = addr & 0x3F          = 0b111000          = 0x38  = 56
index  = (addr >> 6) & 0x1FF  = 0x159             = 345
tag    = addr >> 15           = 0x2468            = 9320
```

**P11.** 32 KiB / 64 B = 512 lines; 512 / 4 ways = 128 sets.
- (a) offset **6**, index **7**, tag 48 - 13 = **35** bits.
- (b) The low 13 bits of `0x7FFF12345ABC` are `0x1ABC` = `1 1010 1011 1100`.

```text
offset = low 6 bits         = 0b111100    = 0x3C = 60
index  = bits 12..6         = 0b1101010   = 0x6A = 106
tag    = addr >> 13                       = 0x3FFF891A2
```

**P12.** 1 MiB / 64 B = 16,384 lines; 16,384 / 8 = 2048 sets.
- (a) offset **6**, index **11**, tag 40 - 17 = **23** bits.
- (b) Metadata:

```text
per line : 23 tag + 1 valid + 1 dirty = 25 bits  -> 16,384 * 25 = 409,600 bits
per set  : 7 PLRU bits                           ->  2,048 *  7 =  14,336 bits
total    : 423,936 bits = 52,992 bytes ~= 51.75 KiB  ~= 5.1% of the 1 MiB data array
```

ECC and coherence state (MESI bits, snoop-filter or directory entries) add more. That is why "a 1 MiB cache" costs noticeably more than 1 MiB of SRAM.

**P13.**
- (a) `index(0x10000) = (0x10000 >> 6) & 0x1FF = 0x400 & 0x1FF = 0`, and `index(0x18000) = 0x600 & 0x1FF = 0`. The arrays are exactly 0x8000 = 32 KiB apart, which equals the cache size, so `a[i]` and `b[i]` always map to the same line slot. Each access evicts the line the other array just loaded. **Hit rate = 0%**: every access is a conflict miss, even though only two lines are live at a time.
- (b) With 2 ways (256 sets, 16 KiB per way), both lines still map to one set but now fit side by side. Each 64 B line holds 16 floats, so each array takes one compulsory miss per 16 elements: **15/16 = 93.75%**. The hardware prefetcher would bring the real number close to 100%.
- (c) **VIPT** (virtually indexed, physically tagged) L1s look up the set index in parallel with the TLB. That only works without aliasing if the index and offset bits lie inside the page offset (12 bits for 4 KiB pages), so `capacity / ways <= 4 KiB`. That gives 32 KiB = 8 x 4 KiB and 48 KiB = 12 x 4 KiB. A bigger L1 means more ways, which costs power and latency. Cores built for 16 KiB pages can have larger L1s for the same reason. Fixes for (a): pad one array by a line or more, or allocate them so that they don't sit a cache size apart.

### A2.4 Cache Hit Rate and AMAT

**P14.**
- (a) AMAT = 1 + 0.05 x 100 = **6 ns**.
- (b) 1 + m x 100 = 2 gives m = 1%, so a **99% hit rate**. Going from 95% to 99% hits cuts AMAT by 3x. Hit-rate improvements near 100% matter far more than they look.

**P15.**
- (a) AMAT = 4 + 0.10 x (12 + 0.20 x 200) = 4 + 0.10 x 52 = **9.2 cycles**.
- (b) Global L2 miss rate = 0.10 x 0.20 = **2%** of all accesses go to memory.
- (c) Halving the L1 miss rate gives 4 + 0.05 x 52 = **6.6**. Halving memory latency gives 4 + 0.10 x (12 + 0.2 x 100) = **7.2**. The L1 improvement wins, because it removes the L2 hit time *and* the memory component for those accesses.

**P16.**
- (a) Row-wise is sequential, with 16 floats per line: 1 miss per 16 accesses = **93.75%** (in practice about 100% with the stream prefetcher).
- (b) The L1 has 32 KiB / 64 B / 8 = **64 sets**, and `set = (addr / 64) mod 64`. A column step is 1024 x 4 = 4096 B = 64 lines, so `set` does not change: **every element of a column maps to the same set**. That set has 8 ways but the column touches 1024 lines, so by the time column j+1 needs row 0's line again it was evicted long ago. The L1 hit rate is **about 0%**. The same power-of-two stride also folds into a few L2 sets, and every access lands on a new 4 KiB page, so a column walks 1024 pages and thrashes the DTLB.
- (c) Fixes: loop interchange (iterate rows in the inner loop), tiling/blocking, padding the row pitch (1024 + 16 floats) to break the power-of-two stride, or transposing once up front. See [Performance Engineering 5.3](../computer-science/Performance_Engineering.md#53-row-major-vs-column-major-traversal) and [5.4](../computer-science/Performance_Engineering.md#54-loop-interchange-and-tiling-for-matmul).

**P17.**

```text
CPI = 1.0 + (1.0 fetch * 0.02 * 100) + (0.4 data * 0.05 * 100)
    = 1.0 + 2.0 + 2.0 = 5.0
```

A perfect cache would be **5x faster**. Memory stalls are 80% of execution time on this in-order model, which is why real cores spend so much area on out-of-order execution, memory-level parallelism, and prefetchers to overlap misses.

### A2.5 Pipeline CPI, Hazards, and Branch Penalties

**P18.**

```text
load-use stalls : 0.20 loads * 0.5 dependent * 1 cycle  = 0.10
branch stalls   : 0.15 branches * 0.6 taken * 2 cycles  = 0.18
CPI = 1 + 0.10 + 0.18 = 1.28
```

Forwarding cannot fully hide a load-use hazard in a 5-stage pipeline, because the loaded value only exists at the end of MEM while the dependent instruction needs it at the start of EX. The compiler can often schedule an independent instruction into the slot.

**P19.**
- (a) CPI = 0.5 + 0.20 x 0.05 x 15 = 0.5 + 0.15 = **0.65**. Mispredictions take 0.15 / 0.65 = **23%** of cycles, and the core runs 1.3x slower than its ideal.
- (b) CPI = 0.5 + 0.20 x 0.10 x 15 = **0.80**, and 37.5% of cycles are lost.
- (c) 4e9 / 0.5 = **8.0 G** instr/s ideal, 4e9 / 0.65 = **6.15 G**, 4e9 / 0.8 = **5.0 G**.

On a wide core the real cost is higher than the stall cycles alone, because every mispredict also squashes the work that was issued speculatively. Fixes: branchless code (`cmov`, arithmetic masks), sorting or partitioning data so branches become predictable, and profile-guided optimization. Measure with `perf stat -e branches,branch-misses`.

**P20.**
- (a) Unpipelined: one 1000 ps cycle, and latency 1000 ps. Pipelined: cycle = slowest stage + latch = 300 + 20 = **320 ps**, and the latency of one instruction rises to 5 x 320 = **1600 ps**.
- (b) Unpipelined: 1e6 x 1000 ps = 1 ms. Pipelined: (5 + 1e6 - 1) x 320 ps ~= 320.001 µs. Speedup ~= **3.125x**.
- (c) The ideal 5x assumes equal stages and free latches. Here the slowest stage (300 ps) is 1.5x the average (200 ps), and latch overhead adds 20 ps per stage. Hazards would reduce the gain further. Pipelining improves **throughput**, not the latency of one instruction.

**P21.**

```text
Design A: CPI = 1 + 0.20 * 0.65 * 3 = 1.39 ; time/instr = 1.39 * T
Design B: CPI = 1 + 0.20 * 0.65 * 1 = 1.13 ; time/instr = 1.13 * 1.1 T = 1.243 T
Speedup of B over A = 1.39 / 1.243 = 1.118  -> B is ~12% faster
```

This is the classic "CPI versus cycle time" trade-off. Always compare **time per instruction**, never CPI alone.

### A2.6 Amdahl's Law

**P22.**
- (a) S = 1 / (0.1 + 0.9 / 16) = 1 / 0.15625 = **6.4x**, and efficiency = 6.4 / 16 = **40%**.
- (b) The limit as N grows is 1 / 0.1 = **10x**. With 10% serial work, even 1000 cores cannot beat 10x.

**P23.**

```text
(a) new time = 0.30 (host) + 0.70 / 20 (GPU) + 0.05 (copies) = 0.30 + 0.035 + 0.05 = 0.385
    speedup = 1 / 0.385 = 2.60x
(b) without copies: 1 / 0.335 = 2.99x
(c) ceiling with an infinitely fast GPU and free copies: 1 / 0.30 = 3.33x
```

The 30% left on the host is the limit. The highest-leverage moves are porting more of the host work to the GPU, or overlapping it with GPU execution. Hiding the copies helps too: pinned memory plus async copies on separate streams overlapped with compute. A 20x kernel speedup buys only 2.6x end to end. Say exactly this when someone quotes kernel-only speedups. More in [Performance Engineering 2.2](../computer-science/Performance_Engineering.md#22-amdahls-law).

**P24.**
- (a) Solve 1 / (s + (1 - s) / 32) = 8, so s + (1 - s) / 32 = 0.125, so 32s + 1 - s = 4, so s = 3 / 31 = 9.68%. You need **p >= 90.3%**.
- (b) S = N - s(N - 1) = 64 - 0.05 x 63 = **60.85x** (scaled speedup).
- (c) They answer different questions. Amdahl fixes the **problem size** (strong scaling). Gustafson grows the problem with N (weak scaling) and measures the serial fraction *on the parallel run*, where the parallel part has grown. Both are correct within their assumptions. Say which kind of scaling the user cares about: time-to-solution for a fixed model, or a bigger model in the same time.

### A2.7 Subnetting and CIDR

The fast method: in the "interesting" octet, `block = 256 - mask_octet`. The network address is the largest multiple of the block that does not exceed the host's value in that octet. The broadcast address is network + block - 1.

**P25.** /26 gives mask **255.255.255.192** and block 64 in the last octet. 77 falls in [64, 127].
- Network **192.168.10.64**, broadcast **192.168.10.127**
- Hosts **.65 - .126**, which is 2^6 - 2 = **62** usable

**P26.** /20 gives mask **255.255.240.0** and block 16 in the third octet. 30 falls in [16, 31].
- Network **10.20.16.0**, broadcast **10.20.31.255**
- Hosts **10.20.16.1 - 10.20.31.254**, which is 2^12 - 2 = **4094** usable

**P27.** Allocate the largest subnet first so that every block stays aligned.

| Need | Prefix (usable) | Subnet | Range |
|---|---|---|---|
| 100 | /25 (126) | 172.16.0.0/25 | .0 - .127 |
| 50 | /26 (62) | 172.16.0.128/26 | .128 - .191 |
| 20 | /27 (30) | 172.16.0.192/27 | .192 - .223 |
| 2 | /30 (2) | 172.16.0.224/30 | .224 - .227 |

Left over: .228 - .255 (28 addresses), which decomposes into aligned blocks as **172.16.0.228/30, 172.16.0.232/29, 172.16.0.240/28**.

**P28.**
- (a) /22 has block 4 in the third octet. Both 5 and 6 fall in [4, 7], so both hosts are in **10.1.4.0/22** (broadcast 10.1.7.255): **same subnet**.
- (b) 192.168.0.0/24 to 192.168.3.0/24 summarize to **192.168.0.0/22**.
- (c) **No.** A /23 must start at an even third octet: 192.168.0.0/23 covers 0-1 and 192.168.2.0/23 covers 2-3. The pair 1 and 2 straddles that boundary. You either advertise two /24s or over-summarize to the /22, which also attracts traffic for .0 and .3.

**P29.**
- (a) A /28 has 16 addresses. AWS reserves **5** per subnet: the network address, .1 (VPC router), .2 (DNS), .3 (reserved for future use), and the last address. That leaves **11 usable**, versus 14 in the textbook.
- (b) **/31**: 2 addresses, both usable on point-to-point links (RFC 3021), because there is no need for network or broadcast addresses. **/32**: a single host route, used for loopbacks, VIPs, and host routes.
- (c) An IPv6 /64 has 2^64 ~= 1.8 x 10^19 addresses. SLAAC derives a 64-bit interface identifier, so /64 is the standard subnet size. Don't subnet smaller than /64 on a LAN.

Verification with Python's standard library:

```python
import ipaddress

for cidr in ("192.168.10.77/26", "10.20.30.40/20", "10.1.5.200/22", "10.1.6.10/22"):
    net = ipaddress.ip_interface(cidr).network
    hosts = list(net.hosts())
    print(f"{cidr:>18}: net {net}, mask {net.netmask}, bcast {net.broadcast_address}, "
          f"hosts {hosts[0]}-{hosts[-1]} ({len(hosts)})")
print(list(ipaddress.collapse_addresses(
    ipaddress.ip_network(f"192.168.{i}.0/24") for i in range(4))))
```

```text
  192.168.10.77/26: net 192.168.10.64/26, mask 255.255.255.192, bcast 192.168.10.127, hosts 192.168.10.65-192.168.10.126 (62)
    10.20.30.40/20: net 10.20.16.0/20, mask 255.255.240.0, bcast 10.20.31.255, hosts 10.20.16.1-10.20.31.254 (4094)
     10.1.5.200/22: net 10.1.4.0/22, mask 255.255.252.0, bcast 10.1.7.255, hosts 10.1.4.1-10.1.7.254 (1022)
      10.1.6.10/22: net 10.1.4.0/22, mask 255.255.252.0, bcast 10.1.7.255, hosts 10.1.4.1-10.1.7.254 (1022)
[IPv4Network('192.168.0.0/22')]
```

### A2.8 TCP Throughput and Bandwidth-Delay Product

**P30.** 65,535 B / 0.1 s = 655,350 B/s ~= **5.24 Mbit/s**, about **0.5%** of the 1 Gbps link. With no window scaling, a single flow on a long path is window-limited no matter how fast the link is.

**P31.**
- (a) BDP = 10 x 10^9 bit/s x 0.08 s = 8 x 10^8 bits = **100 MB**. That is how much unacknowledged data must be in flight to fill the pipe.
- (b) You need 65,535 x 2^s >= 10^8, so 2^s >= 1526 and **s = 11** (2^10 gives only 67 MB). The maximum shift is 14, about a 1 GiB window.
- (c) The window is capped near the 6 MiB autotuning maximum: 6 MiB / 0.08 s ~= 78.6 MB/s ~= **630 Mbit/s**, about 6% of the link. It is somewhat less in practice, because part of the buffer is accounting overhead. Fix: raise `net.ipv4.tcp_rmem` / `tcp_wmem` maxima to at least the BDP (autotuning uses these; `net.core.rmem_max` caps only explicit `SO_RCVBUF`), use parallel streams, or use a congestion controller such as BBR that copes better with long fat pipes.

**P32.**

```text
MSS / RTT        = 1460 * 8 bits / 0.05 s = 233,600 bit/s
sqrt(3/2)/sqrt(p) = 1.2247 / sqrt(1e-4)    = 122.47
throughput       ~= 233,600 * 122.47       ~= 28.6 Mbit/s
```

Even 0.01% loss caps a 50 ms Reno/CUBIC-style flow at about 29 Mbit/s. Throughput scales with 1/RTT and 1/sqrt(loss), which is why long-haul transfers use BBR, parallel streams, or loss-free fabrics (RDMA over lossless Ethernet or InfiniBand in HPC clusters).

**P33.**
- (a) 8 x 10^9 bits / 10^8 bit/s = **80 s**. Slow start must grow to the BDP (100 Mbps x 50 ms = 625 KB, about 428 segments), which takes about log2(428 / 10) ~= 6 RTTs = 0.3 s. Total about **80.4 s**: bandwidth-bound.
- (b) 100,000 B / 1460 ~= 69 segments. With cwnd = 10, 20, 40 the cumulative segments are 10, 30, 70, so the data needs **3 RTTs**, plus **1 RTT** for the TCP handshake: **4 RTTs = 200 ms**. Add 1 RTT for TLS 1.3 (250 ms) and the DNS lookup. The pure serialization time is only 100 KB x 8 / 100 Mbps = **8 ms**.
- (c) Small objects are **latency-bound**: 96% of the time is round trips. What helps is fewer RTTs (connection reuse, TLS 1.3 / QUIC, 0-RTT resumption, a larger initial window) and shorter RTTs (CDN edges). More bandwidth barely helps.

### A2.9 Quorum Consistency

**P34.** The condition is **W + R > N**: every read quorum must overlap every write quorum in at least one replica that holds the latest write.

| (W, R) | W + R > 3? | Write tolerates | Read tolerates |
|---|---|---|---|
| (2, 2) | 4, yes | 1 failure | 1 failure |
| (1, 3) | 4, yes | 2 | 0 (reads need every replica) |
| (3, 1) | 4, yes | 0 (writes need every replica) | 2 |
| (1, 1) | 2, no | -- | -- |
| (2, 1) | 3, no | -- | -- |

For (2, 1), the single replica a read contacts may be the one that missed the write, so the read can be stale.

**P35.**
- (a) W = 3, R = 3: both reads and writes tolerate **2** failures (5 - 3).
- (b) W = 4, R = 2: 6 > 5 still holds. Writes tolerate **1** failure and reads tolerate **3**. This favors read availability.
- (c) **W > N/2** makes any two write quorums intersect (W + W > N). Two conflicting writes then cannot both succeed on disjoint replica sets, so writes are effectively ordered and conflicts are detectable.
- (d) Stale reads despite W + R > N:
  - **Sloppy quorums with hinted handoff**: writes land on stand-in nodes outside the key's home replicas.
  - **Last-write-wins with clock skew** silently discards a newer write.
  - **A failed write** that reached fewer than W replicas is not rolled back, so later reads may or may not see it.
  - **Read repair racing with a concurrent write**, or a replica restored from an old backup.

  W + R > N alone does not give linearizability; see [CS Fundamentals 8.3](../computer-science/CS_Fundamentals.md#83-replication-strategies).

**P36.** With p = 0.99 per node and independent failures:

```text
3 nodes, need >= 2: p^3 + 3 p^2 (1-p)                = 0.970299 + 0.029403   = 0.999702   (~2.6 h down/yr)
4 nodes, need >= 3: p^4 + 4 p^3 (1-p)                = 0.960596 + 0.038812   = 0.999408   (~5.2 h down/yr)
5 nodes, need >= 3: sum_{k=3..5} C(5,k) p^k (1-p)^(5-k)                      = 0.99999015 (~5 min down/yr)
```

A **4-node cluster is less available than a 3-node one**. It still tolerates only 1 failure (majority = 3), but there is one more node that can fail. That is why consensus clusters are odd-sized. The big caveat: real failures are correlated (same rack, same bad deploy, same kernel bug), so in practice independence overstates the nines.

### A2.10 Disk and SSD IOPS

**P37.**

```text
rotational latency = 0.5 * 60 s / 7200 = 4.17 ms
transfer (4 KiB)   = 4096 B / 200 MB/s = 0.02 ms
service time       = 4 + 4.17 + 0.02  = 8.19 ms  ->  ~122 IOPS
throughput         = 122 * 4 KiB      ~= 0.5 MB/s   vs 200 MB/s sequential (~400x gap)
```

This gap is why databases use WAL, LSM trees, and log-structured file systems, which turn random writes into sequential ones.

**P38.**
- (a) At QD1, 1 / 80 µs = **12,500 IOPS**.
- (b) By Little's law, L = lambda x W = 10^6/s x 80 x 10^-6 s = **80 I/Os in flight**, and more in practice because latency rises under load. That is why `fio` benchmarks use, for example, `--iodepth=32 --numjobs=4`, and why you need async I/O (io_uring, libaio) or many threads to get rated IOPS.
- (c) 10^6 x 4096 B ~= **4.1 GB/s**. PCIe 4.0 x4 is 16 GT/s x 4 lanes x 128/130 / 8 ~= 7.9 GB/s raw, so this is **plausible**.

**P39.** Raw capacity is 8 x 150 = 1200 IOPS.

| Level | Random read IOPS | Random write IOPS | Why |
|---|---|---|---|
| RAID 0 | 1200 | 1200 | striping, no redundancy |
| RAID 10 | 1200 | 600 | each write goes to 2 mirrors (penalty 2) |
| RAID 5 | 1200 | 300 | read data, read parity, write data, write parity (penalty 4) |
| RAID 6 | 1200 | 200 | two parities (penalty 6) |

(b) For RAID 5 at 70/30: IOPS = 1200 / (0.7 x 1 + 0.3 x 4) = 1200 / 1.9 ~= **632 IOPS**.

**P40.**
- (a) TBW = 3.84 TB x 1 x 365 x 5 = **7,008 TB**, about 7 PB.
- (b) 7,008 / 2 = 3,504 days ~= **9.6 years**.
- (c) 0.5 TB x 10 = 5 TB/day, so 7,008 / 5 = 1,402 days ~= **3.8 years**. It wears out before the 5-year warranty ends. LSM compaction (and the SSD's own internal FTL write amplification) must be part of storage sizing; choose a higher-DWPD drive or tune compaction (for example, tiered instead of leveled).

### A2.11 Little's Law

**P41.**
- (a) L = 2000/s x 0.15 s = **300** requests in flight.
- (b) The maximum is 200 threads / 0.15 s = **1,333 req/s**. Beyond that, the queue grows at (arrival - 1,333) per second, latency climbs without bound, and timeouts and retries make it worse (a retry storm). Size the pool above 300 with headroom, or move to async I/O so in-flight requests don't each pin a thread.

**P42.**
- (a) 16 x 64 B / 100 ns = 1024 B / 100 ns = **10.24 GB/s** per core. Per-core bandwidth is latency-bound, not pin-bound.
- (b) Bytes in flight = 200 GB/s x 100 ns = 20,000 B = 312.5 lines, and 312.5 / 16 ~= **20 cores**. Fewer are needed if L2 prefetchers add more outstanding requests.
- (c) Bytes in flight = 5.3 x 10^12 B/s x 500 x 10^-9 s ~= **2.65 MB**, or about 2.65 MB / 304 ~= **8.7 KB per CU** (~136 outstanding 64 B requests per CU). A single wavefront cannot keep that much memory traffic in flight, so GPUs need many resident wavefronts (occupancy) and wide, coalesced loads to hide latency. See [Performance Engineering 4.2](../computer-science/Performance_Engineering.md#42-memory-level-parallelism-bytes-in-flight).

**P43.**
- (a) L = 4000/s x 0.005 s = **20** connections busy on average. Configure about **30-40** in total, to absorb bursts and p99 query times, split across the app instances, and alert on pool-wait time. Don't oversize: hundreds of connections hurt the database through context switches, memory per connection, and lock contention.
- (b) M/M/1 gives R = S / (1 - rho):

| Utilization | Mean response time |
|---|---|
| 50% | 10 / 0.5 = **20 ms** |
| 90% | 10 / 0.1 = **100 ms** |
| 95% | 10 / 0.05 = **200 ms** |

Latency explodes near saturation, which is why capacity plans target about 60-70% utilization for latency-sensitive services.

### A2.12 Back-of-Envelope QPS and Storage

**P44.** Use 1 day ~= 86,400 s ~= 10^5 s.

| Quantity | Calculation | Result |
|---|---|---|
| Uploads/day | 100M x 0.1 | 10M |
| Upload QPS | 10M / 86,400 | ~116/s average (~100 with 10^5), **~350/s peak** (3x) |
| New storage/day | 10M x 2 MB | **20 TB/day** |
| 5-year raw | 20 TB x 365 x 5 | 36.5 PB |
| With 3x replication | 36.5 x 3 | **~110 PB** |
| With 1.5x erasure coding (e.g. RS 6+3) | 36.5 x 1.5 | **~55 PB** |
| Views/day | 100M x 50 | 5B |
| Read QPS | 5B / 86,400 | **~58k/s average, ~175k/s peak** |
| Egress | 58k x 200 KB | **~11.6 GB/s ~= 93 Gbit/s average**, ~280 Gbit/s peak |

Design consequences: the read:write ratio is 500:1, so this is a CDN problem first (serve resized images from the edge). Originals go to blob storage with erasure coding, and hot or cold tiering cuts cost. Metadata at about 1 KB per photo is only about 10 GB/day, which a sharded database handles easily.

**P45.**
- Writes: 500M / (30 x 86,400) ~= **193/s** (~200/s). Reads at 100:1: **~19k/s** (~20k/s).
- Storage: 500M x 500 B = 250 GB/month, so 3 TB/year and **15 TB in 5 years** before replication. That is small; the hard part is the read QPS, which caches solve.
- IDs: 500M x 60 months = 3 x 10^10 links. 62^7 ~= 3.5 x 10^12, which is about **117x headroom**. 62^6 ~= 5.7 x 10^10 would also work, but with only 1.9x headroom.

**P46.**

| Quantity | Calculation | Result |
|---|---|---|
| Points/s | 10,000 x 200 x 10 | **2 x 10^7** (20M/s) |
| Raw ingest | 20M x 16 B | **320 MB/s** (~2.6 Gbit/s) |
| Raw per day | 320 MB x 86,400 | **~27.6 TB/day** |
| Gorilla-compressed | 20M x 1.37 B x 86,400 | **~2.4 TB/day** (~12x smaller) |

Gorilla gets its ratio from **delta-of-delta timestamps**, which compress to about 1 bit when the sampling is regular, and **XOR-encoded floats**, which are tiny when consecutive counter values are similar. Design implications: aggregate and compress on each node before shipping, shard ingestion by GPU or host ID, keep full resolution for days and 1 Hz or 1-minute rollups for months, and make the sampling interval configurable. Profiling every kernel dispatch is a different, much bigger problem than periodic sampling.


### A2.13 Floating-Point Representation

**P47.**

```text
13.625 = 8 + 4 + 1 + 0.5 + 0.125 = 1101.101b = 1.101101b * 2^3
sign     = 1                          (negative)
exponent = 3 + 127 = 130              = 1000 0010
fraction = 101101 then 17 zeros       = 1011 0100 0000 0000 0000 000
bits     = 1 10000010 10110100000000000000000
         = 1100 0001 0101 1010 0000 0000 0000 0000 = 0xC15A0000
```

**P48.**

| Bits | Fields | Value |
|---|---|---|
| `0x3F800000` | s=0, e=127, f=0 | **1.0** |
| `0xC0000000` | s=1, e=128, f=0 | **-2.0** |
| `0x40490FDB` | s=0, e=128, f=0x490FDB | 1.5707964 x 2 = **3.14159274** (pi rounded to FP32) |
| `0x7F800000` | e=255, f=0 | **+infinity** |
| `0x7FC00000` | e=255, f != 0, top fraction bit set | **quiet NaN** |
| `0x00800000` | e=1, f=0 | smallest normal, 2^-126 ~= **1.18e-38** |
| `0x00000001` | e=0, f=1 | smallest subnormal, 2^-149 ~= **1.4e-45** |
| `0x7F7FFFFF` | e=254, f=all ones | largest finite, (2 - 2^-23) x 2^127 ~= **3.40e38** |

**P49.**
- (a) 0.1 = 0.000110011001100...b (the `0011` block repeats forever) = 1.100110011...b x 2^-4. The exponent is -4 + 127 = 123 = `01111011`. The 23-bit fraction is `10011001100110011001100` followed by `11001...`, so it rounds **up** to `...1101`. The encoding is `0 01111011 10011001100110011001101` = `0x3DCCCCCD`, whose exact value is **0.100000001490116119384765625**, slightly above 0.1.
- (b) In double precision, 0.1 is stored as 0.1000000000000000055511151231257827... and 0.2 has a similar error. Their rounded sum is **0.30000000000000004441**, but the literal 0.3 rounds to **0.29999999999999998890**, one ULP lower. Compare with a tolerance (`math.isclose`, rtol/atol, ULP distance); see [Performance Engineering 9.7](../computer-science/Performance_Engineering.md#97-comparing-floats-ulp-rtol-atol).
- (c) FP32 has a 24-bit significand (23 stored bits + the hidden 1), so every integer up to **2^24 = 16,777,216** is exact. 16,777,217 needs 25 bits and is a tie, which rounds to even, giving **16,777,216**. A `float` counter therefore stops incrementing at 2^24, a classic bug in float accumulators and timestamps.

**P50.**
- (a) **FP16** has 1 sign, 5 exponent (bias 15), and 10 fraction bits. Pi = 1.5708 x 2^1, and in [2, 4) the spacing is 2^-9 = 0.001953125. Pi / spacing = 1608.5..., so the candidates are 1608 x 2^-9 = 3.140625 (0.000968 away) and 3.142578 (0.000985 away). The result is **3.140625 = `0x4248`**. **BF16** has 1 sign, 8 exponent, and 7 fraction bits, and is the top half of FP32. Take `0x40490FDB` and round the low 16 bits `0x0FDB` (< `0x8000`) down, giving **`0x4049` = 3.140625**. It is a coincidence that both land on the same value.
- (b) The FP16 maximum is **65504**, so 100,000 **overflows to +inf** (`0x7C00`). This is why FP16 training needs loss scaling, while BF16, which has FP32's exponent range, usually does not.
- (c) ULP at 1.0: FP32 2^-23 ~= **1.19e-7**; FP16 2^-10 ~= **9.77e-4**; BF16 2^-7 = **0.0078125**. The largest run of exact consecutive integers ends at **2048** for FP16 (2049 rounds to 2048) and at **256** for BF16 (257 rounds to 256). Never accumulate counts or long sums in BF16; accumulate in FP32, as MFMA/Tensor-Core instructions do.
- (d) **E4M3** has a maximum of **448** (1.75 x 2^8). It has no infinity: the all-ones mantissa at the top exponent is NaN, and the format trades range for precision. **E5M2** has a maximum of **57,344** (1.75 x 2^15) and is IEEE-like, with inf and NaN. E4M3's extra mantissa bit suits weights and activations (forward pass); E5M2's range suits gradients (backward pass). Both need scaling factors (per-tensor, delayed, or per-block "MX" scaling) to keep values in range.

Verification (standard library only):

```python
"""Check the IEEE 754, BF16, and subnetting answers with the standard library only."""
import ipaddress
import struct


def f32_bits(x):
    return struct.unpack(">I", struct.pack(">f", x))[0]


def f32_from_bits(b):
    return struct.unpack(">f", struct.pack(">I", b))[0]


def f16(x):
    raw = struct.pack(">e", x)                     # raises OverflowError past 65504
    return struct.unpack(">e", raw)[0], struct.unpack(">H", raw)[0]


def bf16(x):
    u = f32_bits(x)
    r = ((u + 0x7FFF + ((u >> 16) & 1)) >> 16) & 0xFFFF   # round to nearest even
    return f32_from_bits(r << 16), r


print(f"-13.625 -> 0x{f32_bits(-13.625):08X}")
for b in (0x3F800000, 0xC0000000, 0x40490FDB, 0x7F800000, 0x7FC00000,
          0x00800000, 0x00000001, 0x7F7FFFFF):
    print(f"0x{b:08X} -> {f32_from_bits(b)!r}")
print("0.1f bits:", hex(f32_bits(0.1)), "| 16777217.0f ->", f32_from_bits(f32_bits(16777217.0)))
val, bits = f16(3.14159265)
print(f"pi FP16 = {val} (0x{bits:04X})")
val, bits = bf16(3.14159265)
print(f"pi BF16 = {val} (0x{bits:04X})")
try:
    f16(1e5)
except OverflowError:
    print("1e5 does not fit in FP16 (max 65504) -> +inf on hardware conversion")
print("FP16(2049) =", f16(2049.0)[0], "| BF16(257) =", bf16(257.0)[0])
```

```text
-13.625 -> 0xC15A0000
0x3F800000 -> 1.0
0xC0000000 -> -2.0
0x40490FDB -> 3.1415927410125732
0x7F800000 -> inf
0x7FC00000 -> nan
0x00800000 -> 1.1754943508222875e-38
0x00000001 -> 1.401298464324817e-45
0x7F7FFFFF -> 3.4028234663852886e+38
0.1f bits: 0x3dcccccd | 16777217.0f -> 16777216.0
pi FP16 = 3.140625 (0x4248)
pi BF16 = 3.140625 (0x4049)
1e5 does not fit in FP16 (max 65504) -> +inf on hardware conversion
FP16(2049) = 2048.0 | BF16(257) = 256.0
```

### A2.14 Two's Complement

**P51.**
- (a) 77 = `0100 1101`. Invert to get `1011 0010`, then add 1 to get **`1011 0011` = `0xB3`**. Check: 256 - 77 = 179 = `0xB3`.
- (b) An n-bit signed integer ranges over **[-2^(n-1), 2^(n-1) - 1]**; for 8 bits, -128 to 127. The asymmetry is why `-INT_MIN` and `abs(INT_MIN)` overflow.
- (c) `0xB3` is **179** unsigned and **-77** signed (179 - 256).
- (d) `0xF5` = `1111 0101`. The sign bit is 1, so extend with ones to get **`0xFFFFFFF5` = -11** (245 - 256).

**P52.**

| Operation | Bits | 8-bit result | Signed value | C (unsigned carry) | V (signed overflow) |
|---|---|---|---|---|---|
| 100 + 50 | `0x64 + 0x32 = 0x96` | `0x96` | **-106** | 0 | **1**: two positives gave a negative |
| -100 + -50 | `0x9C + 0xCE = 0x16A` | `0x6A` | **106** | 1 | **1**: two negatives gave a positive |

Rule: **V = (carry into the MSB) XOR (carry out of the MSB)**. Equivalently, overflow happens exactly when both operands have the same sign and the result's sign differs. Adding operands of opposite signs can never overflow. C means unsigned overflow and V means signed overflow; the hardware computes both and the compiler picks the flag (for example `jo` vs `jc`).

**P53.** Output (GCC 15, `-std=c++20`; `-Wall` warns about the deliberate signed/unsigned comparison):

```text
-77 as int8 bits   = 0xB3
(int8_t)200        = -56
int8 0xF5 -> int32 = -11 (0xFFFFFFF5)
100 + 50: as int = 150, stored in int8 = -106
INT_MAX + 1 overflow? yes (wrapped result -2147483648)
-1 < 1u ? false
-16 >> 2 = -4
~5 = -6, -5 = -5
```

- **Line 1:** -77 is stored as `0xB3`. Casting to `uint8_t` reinterprets the same bits modulo 256.
- **Line 2:** 200 does not fit in `int8_t`; C++20 defines the conversion as modular: 200 - 256 = -56. Before C++20 it was implementation-defined.
- **Line 3:** widening a negative signed value copies the sign bit into the new high bits.
- **Line 4:** integer promotion: `int8_t + int8_t` is computed in `int`, so 150 is exact. Only the narrowing store wraps, to -106.
- **Line 5:** signed overflow (`INT_MAX + 1`) is **undefined behavior**, and optimizers exploit it, for example by assuming `x + 1 > x`. `__builtin_add_overflow` checks safely, returns true on overflow, and stores the wrapped value (-2147483648). The standard alternatives behave differently: C++26 `std::add_sat` saturates (it returns INT_MAX here), and C23 `ckd_add` is the standard checked add in C.
- **Line 6:** the usual arithmetic conversions turn -1 into `UINT_MAX`, so `-1 < 1u` is false. This is the source of many `size_t` loop bugs.
- **Line 7:** right-shifting a negative value is arithmetic, filling with sign bits, and is guaranteed since C++20. Note that -16 >> 2 = -4, but -15 >> 2 = -4 too, whereas -15 / 4 = -3: shifting rounds toward negative infinity and division truncates toward zero.
- **Line 8:** `~x == -x - 1`, which is the identity behind "invert and add one".

### A2.15 CPU Scheduling Gantt Charts

**P54 (Set A).**

(a) **FCFS**

```text
| P1       | P2   | P3         | P4     |
0          8      12           21       26
```

| | P1 | P2 | P3 | P4 | Average |
|---|---|---|---|---|---|
| Waiting | 0 | 7 | 10 | 18 | **8.75** |
| Turnaround | 8 | 11 | 19 | 23 | **15.25** |

(b) **SJF (non-preemptive):** at t = 0 only P1 has arrived, so it runs to completion. At t = 8 the shortest is P2 (4), then P4 (5), then P3 (9).

```text
| P1       | P2   | P4     | P3         |
0          8      12       17           26
```

| | P1 | P2 | P3 | P4 | Average |
|---|---|---|---|---|---|
| Waiting | 0 | 7 | 15 | 9 | **7.75** |
| Turnaround | 8 | 11 | 24 | 14 | **14.25** |

(c) **SRTF:** at t = 1, P2 (4) preempts P1 (7 left). At t = 3, P4 (5) does not preempt P2 (2 left). At t = 5, P4 (5) beats P1 (7) and P3 (9).

```text
| P1 | P2   | P4     | P1       | P3         |
0    1      5        10         17           26
```

| | P1 | P2 | P3 | P4 | Average |
|---|---|---|---|---|---|
| Waiting | 9 | 0 | 15 | 2 | **6.5** |
| Turnaround | 17 | 4 | 24 | 7 | **13.0** |

SRTF is provably optimal for average waiting time, but it needs future burst lengths (estimated in practice by exponential averaging of past bursts) and can starve long jobs.

**P55 (Set A).**

(a) **RR, q = 3.** Ready-queue trace:

```text
t=0   run P1 (0-3)          arrivals P2@1, P3@2, P4@3      queue after: P2 P3 P4 P1
t=3   run P2 (3-6), 1 left                                 queue after: P3 P4 P1 P2
t=6   run P3 (6-9), 6 left                                 queue after: P4 P1 P2 P3
t=9   run P4 (9-12), 2 left                                queue after: P1 P2 P3 P4
t=12  run P1 (12-15), 2 left                               queue after: P2 P3 P4 P1
t=15  run P2 (15-16) done
t=16  run P3 (16-19), 3 left                               queue after: P4 P1 P3
t=19  run P4 (19-21) done
t=21  run P1 (21-23) done
t=23  run P3 (23-26) done
```

```text
| P1 | P2 | P3 | P4 | P1 |P2| P3 | P4 | P1 | P3 |
0    3    6    9    12   15 16   19   21   23   26
```

| | P1 | P2 | P3 | P4 | Average |
|---|---|---|---|---|---|
| Waiting | 15 | 11 | 15 | 13 | **13.5** |
| Turnaround | 23 | 15 | 24 | 18 | **20.0** |
| Response | 0 | 2 | 4 | 6 | **3.0** |

RR has the worst waiting time here but the best response time: every job starts within 6 time units.

(b) **Preemptive priority** (P2 = 1 > P3 = 2 > P1 = 3 > P4 = 4):

```text
| P1 | P2   | P3         | P1       | P4     |
0    1      5            14         21       26
```

| | P1 | P2 | P3 | P4 | Average |
|---|---|---|---|---|---|
| Waiting | 13 | 0 | 3 | 18 | **8.5** |
| Turnaround | 21 | 4 | 12 | 23 | **15.0** |

**P4 suffers**: it is short (5) but has the lowest priority, so it waits 18. With a steady stream of higher-priority arrivals it would **starve**. The fix is **aging**: raise a process's effective priority the longer it waits. Linux's CFS/EEVDF avoid the problem structurally, because every runnable task accrues virtual runtime and eventually becomes the most deserving.

**P56 (Set B, all arrive at 0).**

| Policy | Gantt | Waiting (P1..P5) | Avg wait |
|---|---|---|---|
| FCFS | P1 0-6, P2 6-8, P3 8-16, P4 16-19, P5 19-23 | 0, 6, 8, 16, 19 | **9.8** |
| SJF | P2 0-2, P4 2-5, P5 5-9, P1 9-15, P3 15-23 | 9, 0, 15, 2, 5 | **6.2** |
| Priority | P2 0-2, P4 2-5, P1 5-11, P3 11-19, P5 19-23 | 5, 0, 11, 2, 19 | **7.4** |
| RR q=2 | P1 0-2, P2 2-4, P3 4-6, P4 6-8, P5 8-10, P1 10-12, P3 12-14, P4 14-15, P5 15-17, P1 17-19, P3 19-23 | 13, 2, 15, 12, 13 | **11.0** (avg response 4.0) |
| RR q=4 | P1 0-4, P2 4-6, P3 6-10, P4 10-13, P5 13-17, P1 17-19, P3 19-23 | 13, 4, 15, 10, 13 | **11.0** (avg response 6.6) |

Ranking by average waiting time: **SJF (6.2) < Priority (7.4) < FCFS (9.8) < RR (11.0)**. A smaller quantum improved response time (4.0 vs 6.6) without changing average waiting here. In a real system the smaller quantum would also pay for more context switches.

**P57 (convoy effect).**

| Order / policy | Waiting times | Average |
|---|---|---|
| FCFS P1(24), P2(3), P3(3) | 0, 24, 27 | **17.0** |
| FCFS P2, P3, P1 | 0, 3, 6 | **3.0** |
| RR q=4 (P1 0-4, P2 4-7, P3 7-10, P1 10-30) | P1 6, P2 4, P3 7 | **5.67** |

The **convoy effect**: under FCFS, short (often I/O-bound) jobs queue behind one long CPU-bound job, like cars behind a truck. Average waiting time balloons and I/O devices sit idle, because the I/O-bound jobs cannot issue their next request. Preemption (RR) or shortest-first ordering breaks the convoy.

A simulator that reproduces every chart above:

```python
"""Unit-time CPU scheduling simulator: FCFS, SJF, SRTF, PRIO, PPRIO, RR."""
from collections import deque


def simulate(procs, policy, quantum=2):
    """procs: list of (name, arrival, burst, priority); lower number = higher priority.
    Returns (gantt, stats) where gantt is a list of (name, start, end)."""
    arr = {n: a for n, a, b, p in procs}
    burst = {n: b for n, a, b, p in procs}
    prio = {n: p for n, a, b, p in procs}
    order = {n: i for i, (n, *_rest) in enumerate(procs)}
    rem = dict(burst)
    done, first = {}, {}
    t, cur, slice_used = 0, None, 0
    rq = deque()             # RR ready queue
    timeline = []
    arrived = set()

    def admit(now):
        for n, a, b, p in sorted(procs, key=lambda x: (x[1], order[x[0]])):
            if a <= now and n not in arrived:
                arrived.add(n)
                rq.append(n)

    while len(done) < len(procs):
        admit(t)
        ready = [n for n in arrived if n not in done]
        if policy == "RR":
            if cur is not None and (rem[cur] == 0 or slice_used == quantum):
                if rem[cur] > 0:
                    rq.append(cur)   # preempted job goes behind jobs that arrived by now
                cur = None
            if cur is None:
                while rq and rem[rq[0]] == 0:
                    rq.popleft()
                cur = rq.popleft() if rq else None
                slice_used = 0
        else:
            keep = cur is not None and rem[cur] > 0
            preemptive = policy in ("SRTF", "PPRIO")
            if not keep or preemptive:
                key = {
                    "FCFS": lambda n: (arr[n], order[n]),
                    "SJF": lambda n: (burst[n], arr[n], order[n]),
                    "SRTF": lambda n: (rem[n], n != cur, arr[n], order[n]),
                    "PRIO": lambda n: (prio[n], arr[n], order[n]),
                    "PPRIO": lambda n: (prio[n], n != cur, arr[n], order[n]),
                }[policy]
                cur = min(ready, key=key) if ready else None
        if cur is None:
            timeline.append("idle")
            t += 1
            continue
        first.setdefault(cur, t)
        timeline.append(cur)
        rem[cur] -= 1
        slice_used += 1
        t += 1
        if rem[cur] == 0:
            done[cur] = t
            if policy != "RR":
                cur = None

    gantt = []
    for i, n in enumerate(timeline):
        if gantt and gantt[-1][0] == n:
            gantt[-1] = (n, gantt[-1][1], i + 1)
        else:
            gantt.append((n, i, i + 1))
    stats = {n: dict(completion=done[n], turnaround=done[n] - arr[n],
                     waiting=done[n] - arr[n] - burst[n], response=first[n] - arr[n])
             for n in burst}
    return gantt, stats


def report(title, procs, policy, quantum=2):
    gantt, stats = simulate(procs, policy, quantum)
    print(f"== {title}")
    print(" | ".join(f"{n} {s}-{e}" for n, s, e in gantt))
    for n, s in stats.items():
        print(f"  {n}: CT={s['completion']:>2} TAT={s['turnaround']:>2} "
              f"WT={s['waiting']:>2} RT={s['response']:>2}")
    k = len(stats)
    print(f"  avg WT = {sum(s['waiting'] for s in stats.values()) / k:.2f}, "
          f"avg TAT = {sum(s['turnaround'] for s in stats.values()) / k:.2f}, "
          f"avg RT = {sum(s['response'] for s in stats.values()) / k:.2f}")


if __name__ == "__main__":
    A = [("P1", 0, 8, 3), ("P2", 1, 4, 1), ("P3", 2, 9, 2), ("P4", 3, 5, 4)]
    for pol in ("FCFS", "SJF", "SRTF"):
        report(f"Set A {pol}", A, pol)
    report("Set A RR q=3", A, "RR", 3)
    report("Set A PPRIO", A, "PPRIO")
    B = [("P1", 0, 6, 3), ("P2", 0, 2, 1), ("P3", 0, 8, 4), ("P4", 0, 3, 2), ("P5", 0, 4, 5)]
    for pol in ("FCFS", "SJF", "PRIO"):
        report(f"Set B {pol}", B, pol)
    report("Set B RR q=2", B, "RR", 2)
    report("Set B RR q=4", B, "RR", 4)
    C = [("P1", 0, 24, 1), ("P2", 0, 3, 1), ("P3", 0, 3, 1)]
    report("Convoy FCFS", C, "FCFS")
    report("Convoy reversed", [C[1], C[2], C[0]], "FCFS")
    report("Convoy RR q=4", C, "RR", 4)
```

### A2.16 Banker's Algorithm

**P58.**

(a) Need = Max - Allocation. Allocation column sums are A = 7, B = 4, C = 5, so **Available = (10-7, 6-4, 7-5) = (3, 2, 2)**.

| Process | Need (A B C) |
|---|---|
| P0 | 4 2 2 |
| P1 | 1 2 1 |
| P2 | 4 1 2 |
| P3 | 2 2 1 |
| P4 | 3 2 2 |

(b) Safety check, scanning from P0 each time and taking the first process whose Need fits in Work:

```text
Work = (3,2,2)
P1 need (1,2,1) <= (3,2,2)  -> Work = (3,2,2) + alloc (2,0,1) = (5,2,3)
P0 need (4,2,2) <= (5,2,3)  -> Work = (6,3,3)
P2 need (4,1,2) <= (6,3,3)  -> Work = (9,4,4)
P3 need (2,2,1) <= (9,4,4)  -> Work = (9,6,5)
P4 need (3,2,2) <= (9,6,5)  -> Work = (10,6,7)   = totals, all finish
```

The state is **safe**, with sequence **<P1, P0, P2, P3, P4>**. Others exist, such as <P1, P3, P0, P2, P4>; any one is enough.

(c) For each request, first check that it is within the process's Need (else error) and within Available (else wait). Then pretend to grant it and run the safety check.

| Request | Within Need? | Within Available? | Pretend state | Safe? | Decision |
|---|---|---|---|---|---|
| P3 (1,0,1) | yes | yes | Avail (2,2,1); P3 need (1,2,0) | <P1, P0, P2, P3, P4> | **Grant** |
| P2 (2,1,1) | yes | yes | Avail (1,1,1); P2 need (2,0,1) | no Need fits (1,1,1): P1 needs B=2, P2 needs A=2 | **Deny, P2 waits** |
| P4 (3,0,0) | yes | yes | Avail (0,2,2); P4 need (0,2,2) | <P4, P0, P1, P2, P3>: P4 can finish immediately | **Grant** |
| P0 (1,2,0) | yes | yes | Avail (2,0,2); P0 need (3,0,2) | nothing fits: B is exhausted and P0 needs A=3 | **Deny, P0 waits** |
| P1 (2,0,0) | **no**: Need A = 1 | -- | -- | -- | **Error**: exceeds declared maximum |

P4's request is instructive: it takes *all* of resource A, yet it is safe, because it leaves P4 able to finish and return everything. "Unsafe" does not mean "deadlocked"; it means the OS can no longer *guarantee* that every process can finish.

**P59.**
- (a) Available = 12 - (5 + 2 + 2) = 3, and Need = P0: 5, P1: 2, P2: 7. P1 (2 <= 3) finishes, giving 5; P0 (5 <= 5) finishes, giving 10; P2 (7 <= 10) finishes. **Safe, <P1, P0, P2>.**
- (b) After P2 gets one more drive: Available = 2, and P2 holds 3 and needs 6. P1 (2 <= 2) finishes, giving 4. Now P0 needs 5 > 4 and P2 needs 6 > 4. **Unsafe**, so the request must wait even though a drive is free.

Banker's is rarely used in general-purpose OSes: it needs maximum claims up front, a fixed process set, and O(m x n^2) work per request. It does appear in reservation-style admission control (GPU memory or job schedulers that know each job's peak).

```python
"""Banker's algorithm: safety check and resource-request check."""


def is_safe(available, alloc, need):
    work = list(available)
    finish = [False] * len(alloc)
    seq = []
    progress = True
    while progress:
        progress = False
        for i in range(len(alloc)):            # scan in index order, take first that fits
            if not finish[i] and all(n <= w for n, w in zip(need[i], work)):
                work = [w + a for w, a in zip(work, alloc[i])]
                finish[i] = True
                seq.append(f"P{i}")
                print(f"  run P{i}: need {need[i]} <= work -> work = {work}")
                progress = True
                break                          # restart the scan from P0
    return all(finish), seq


def request(i, req, available, alloc, need):
    if any(r > n for r, n in zip(req, need[i])):
        return "error: request exceeds declared need"
    if any(r > a for r, a in zip(req, available)):
        return "wait: not enough available"
    avail2 = [a - r for a, r in zip(available, req)]
    alloc2 = [row[:] for row in alloc]
    need2 = [row[:] for row in need]
    alloc2[i] = [a + r for a, r in zip(alloc2[i], req)]
    need2[i] = [n - r for n, r in zip(need2[i], req)]
    safe, seq = is_safe(avail2, alloc2, need2)
    return f"grant (safe: {seq})" if safe else "deny: resulting state is unsafe"


if __name__ == "__main__":
    total = [10, 6, 7]
    alloc = [[1, 1, 0], [2, 0, 1], [3, 1, 1], [0, 2, 1], [1, 0, 2]]
    mx = [[5, 3, 2], [3, 2, 2], [7, 2, 3], [2, 4, 2], [4, 2, 4]]
    need = [[m - a for m, a in zip(mr, ar)] for mr, ar in zip(mx, alloc)]
    available = [t - sum(col) for t, col in zip(total, zip(*alloc))]
    print("need =", need, "available =", available)
    print("initial:", is_safe(available, alloc, need))
    for i, req in [(3, [1, 0, 1]), (2, [2, 1, 1]), (4, [3, 0, 0]), (0, [1, 2, 0]), (1, [2, 0, 0])]:
        print(f"P{i} requests {req}:", request(i, req, available, alloc, need))
```

### A2.17 Page Replacement

**P60.** 3 frames, `F` marks a fault. Each column shows the frame contents *after* the reference.

```text
FIFO, 3 frames: 15 faults
ref    7  0  1  2  0  3  0  4  2  3  0  3  2  1  2  0  1  7  0  1
f0     7  7  7  2  2  2  2  4  4  4  0  0  0  0  0  0  0  7  7  7
f1        0  0  0  0  3  3  3  2  2  2  2  2  1  1  1  1  1  0  0
f2           1  1  1  1  0  0  0  3  3  3  3  3  2  2  2  2  2  1
fault  F  F  F  F     F  F  F  F  F  F        F  F        F  F  F

LRU, 3 frames: 12 faults
ref    7  0  1  2  0  3  0  4  2  3  0  3  2  1  2  0  1  7  0  1
f0     7  7  7  2  2  2  2  4  4  4  0  0  0  1  1  1  1  1  1  1
f1        0  0  0  0  0  0  0  0  3  3  3  3  3  3  0  0  0  0  0
f2           1  1  1  3  3  3  2  2  2  2  2  2  2  2  2  7  7  7
fault  F  F  F  F     F     F  F  F  F        F     F     F

OPT, 3 frames: 9 faults
ref    7  0  1  2  0  3  0  4  2  3  0  3  2  1  2  0  1  7  0  1
f0     7  7  7  2  2  2  2  2  2  2  2  2  2  2  2  2  2  7  7  7
f1        0  0  0  0  0  0  4  4  4  0  0  0  0  0  0  0  0  0  0
f2           1  1  1  3  3  3  3  3  3  3  3  1  1  1  1  1  1  1
fault  F  F  F  F     F     F        F        F           F
```

**FIFO = 15, LRU = 12, OPT = 9 faults.** OPT evicts the page whose next use is farthest in the future, so it is the lower bound used to judge real policies. LRU uses the past as a proxy for the future and lands in between.

**P61 (Belady's anomaly).**

```text
FIFO, 3 frames: 9 faults
ref    1  2  3  4  1  2  5  1  2  3  4  5
f0     1  1  1  4  4  4  5  5  5  5  5  5
f1        2  2  2  1  1  1  1  1  3  3  3
f2           3  3  3  2  2  2  2  2  4  4
fault  F  F  F  F  F  F  F        F  F

FIFO, 4 frames: 10 faults
ref    1  2  3  4  1  2  5  1  2  3  4  5
f0     1  1  1  1  1  1  5  5  5  5  4  4
f1        2  2  2  2  2  2  1  1  1  1  5
f2           3  3  3  3  3  3  2  2  2  2
f3              4  4  4  4  4  4  3  3  3
fault  F  F  F  F        F  F  F  F  F  F

LRU 3 frames: 10 | 4 frames: 8
OPT 3 frames: 7 | 4 frames: 6
```

FIFO gets **worse** with more memory: 9 faults with 3 frames, 10 with 4. LRU (10, then 8) and OPT (7, then 6) cannot do that because they are **stack algorithms**: the set of pages resident with n frames is always a subset of the set resident with n + 1 frames (the *inclusion property*), so any hit with n frames is also a hit with n + 1. FIFO's resident set depends on load order, so it lacks this property.

**P62 (Clock).**

```text
CLOCK, 3 frames: 14 faults
ref    7  0  1  2  0  3  0  4  2  3  0  3  2  1  2  0  1  7  0  1
f0     7  7  7  2  2  2  2  4  4  4  4  3  3  3  3  0  0  0  0  0
f1        0  0  0  0  0  0  0  2  2  2  2  2  1  1  1  1  7  7  7
f2           1  1  1  3  3  3  3  3  0  0  0  0  2  2  2  2  2  1
fault  F  F  F  F     F     F  F     F  F     F  F  F     F     F
```

**14 faults**, between LRU (12) and FIFO (15). Clock approximates LRU with one hardware-set reference bit per page instead of a timestamp per access. Linux uses more refined approximations (active/inactive lists, and the multi-generational LRU since 6.1), because exact LRU would need work on every memory access.

**P63.**
- (a) The fault rate is 12/20 = 0.6, so EAT = 0.4 x 100 ns + 0.6 x 5 ms ~= **3 ms per access**, about 30,000x slower than memory. Toy reference strings fault absurdly often. Real workloads must stay near 10^-6 faults per access (see P3), which is why the working set must fit in RAM.
- (b) References 6 through 10 are `3 0 4 2 3`, so **W(10, 5) = {0, 2, 3, 4}** and its size is 4. With only 3 frames this process would thrash. The working-set model allocates each process at least |W| frames, and if the sum of all working sets exceeds physical memory it **suspends (swaps out) whole processes** rather than letting every process thrash.

```python
"""Page-replacement simulator: FIFO, LRU, OPT, CLOCK. Prints a frame table per reference."""
from collections import deque


def simulate(refs, nframes, policy):
    frames = []               # list of resident pages, slot order preserved for display
    fifo = deque()            # arrival order for FIFO
    last_use = {}             # page -> last time used (LRU)
    ref_bit = {}              # CLOCK reference bits
    hand = 0                  # CLOCK hand (index into frames)
    faults, rows = 0, []
    for t, p in enumerate(refs):
        hit = p in frames
        if hit:
            ref_bit[p] = 1
        else:
            faults += 1
            if len(frames) < nframes:
                frames.append(p)
                if policy == "CLOCK":
                    hand = len(frames) % nframes
            else:
                if policy == "FIFO":
                    victim = fifo.popleft()
                elif policy == "LRU":
                    victim = min(frames, key=lambda q: last_use[q])
                elif policy == "OPT":
                    def next_use(q):
                        try:
                            return refs.index(q, t + 1)
                        except ValueError:
                            return float("inf")
                    # farthest next use; ties (never used again) -> lowest slot
                    victim = max(frames, key=lambda q: (next_use(q), -frames.index(q)))
                elif policy == "CLOCK":
                    while ref_bit[frames[hand]]:
                        ref_bit[frames[hand]] = 0
                        hand = (hand + 1) % nframes
                    victim = frames[hand]
                    hand = (hand + 1) % nframes
                frames[frames.index(victim)] = p
            fifo.append(p)
            ref_bit[p] = 1
        last_use[p] = t
        rows.append((p, list(frames), "" if hit else "F"))
    return faults, rows


def show(refs, nframes, policy):
    faults, rows = simulate(refs, nframes, policy)
    print(f"{policy}, {nframes} frames: {faults} faults")
    print("ref   " + " ".join(f"{p:>2}" for p, _, _ in rows))
    for slot in range(nframes):
        print(f"f{slot}    " + " ".join(
            f"{fr[slot]:>2}" if slot < len(fr) else "  " for _, fr, _ in rows))
    print("fault " + " ".join(f"{f:>2}" for _, _, f in rows))
    print()


if __name__ == "__main__":
    s1 = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    for pol in ("FIFO", "LRU", "OPT", "CLOCK"):
        show(s1, 3, pol)
    s2 = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    show(s2, 3, "FIFO")
    show(s2, 4, "FIFO")
    for pol in ("LRU", "OPT"):
        print(pol, "3 frames:", simulate(s2, 3, pol)[0], "| 4 frames:", simulate(s2, 4, pol)[0])
```

### A3 Rapid-Fire Answers

#### Operating Systems

- **R1.** A process owns resources: an address space, a file-descriptor table, and credentials. A thread is a schedulable execution context (registers, stack, thread-local storage) that shares its process's address space and resources.
- **R2.** It saves and restores the general-purpose registers, the program counter, stack pointer, and flags, the FPU/SIMD state (often lazily), and the kernel stack pointer. A process switch also loads a new page-table root (CR3 on x86).
- **R3.** No address-space switch is needed, so there is no page-table root reload and no TLB flush (PCID/ASID tags reduce that cost anyway), and the caches stay warm with shared data.
- **R4.** A zombie is a process that has exited but whose parent has not yet called `wait()`. Its PID and exit status remain in the process table until it is reaped.
- **R5.** An orphan is a process whose parent exited first. It is reparented to PID 1, or to the nearest "subreaper" (`PR_SET_CHILD_SUBREAPER`), which reaps it when it exits.
- **R6.** `fork()` returns 0 in the child, the child's PID in the parent, and -1 in the parent on failure (no child created).
- **R7.** After `fork()`, parent and child share physical pages mapped read-only. The first write to a page faults, and the kernel copies just that page for the writer.
- **R8.** These survive: the PID and parent PID, open file descriptors without `FD_CLOEXEC`, the current directory, umask, resource limits, the signal mask, and ignored signals. The address space is replaced, and caught signal handlers are reset to the default.
- **R9.** `SIGKILL` and `SIGSTOP`.
- **R10.** A function is async-signal-safe if it can be called from a signal handler even when the handler interrupted arbitrary code. `write()`, `_exit()`, and `sigaction()` are safe; `malloc()`, `printf()`, and mutex locking are not.
- **R11.** A minor fault is resolved without I/O: the page is already in the page cache, it is a COW copy, or it is a fresh zero page. A major fault needs a disk or swap read and costs microseconds to milliseconds.
- **R12.** Thrashing is when the combined working sets exceed RAM, so processes spend their time paging instead of executing. CPU utilization collapses while the disk is saturated.
- **R13.** Belady's anomaly is when FIFO replacement produces *more* page faults with *more* frames. Stack algorithms (LRU, OPT) are immune.
- **R14.** Internal fragmentation is waste inside an allocated unit (rounding up to a page or size class). External fragmentation is enough total free memory that is split into holes too small to use.
- **R15.** Mutual exclusion, hold and wait, no preemption, and circular wait.
- **R16.** Acquire locks in one global order, which breaks circular wait. Use `std::scoped_lock` / `std::lock` when you must take several locks at once.
- **R17.** A mutex has an owner (only the locker may unlock) and protects a critical section. A semaphore is a counter with no owner, used to count resources or to signal between threads.
- **R18.** Spurious wakeups are allowed, and another thread may consume the condition between the notify and your wakeup. Always re-check the predicate: `cv.wait(lock, pred)`.
- **R19.** Priority inversion: a high-priority task waits on a lock held by a low-priority task, which is preempted by a medium-priority task, so the high-priority task waits indefinitely. Fix it with priority inheritance or priority ceiling. Mars Pathfinder (1997) is the famous case.
- **R20.** A futex ("fast userspace mutex") is a 32-bit word on which uncontended lock and unlock are pure user-space atomics. The `futex()` syscall is used only to sleep or wake on contention. `pthread_mutex` and `std::mutex` are built on it.
- **R21.** Virtual-page-number to physical-frame translations, plus permission bits (and an ASID/PCID tag).
- **R22.** Address spaces are huge and sparse. Multi-level tables allocate page-table pages only for the regions in use (a flat 48-bit table would be 512 GiB).
- **R23.** The page cache is the kernel's RAM cache of file contents. Reads are served from it, writes dirty pages in it, and background writeback flushes them. "Free" memory on a busy Linux box is mostly page cache, which is reclaimable.
- **R24.** `write` only copies data into the page cache. `fsync` blocks until the file's data and metadata are on stable storage, including a device cache flush. New file names also need an `fsync` of the directory.
- **R25.** With `MAP_SHARED`, stores are visible to other mappers and written back to the file. With `MAP_PRIVATE`, stores trigger copy-on-write into private anonymous pages that the file never sees.

#### Networks

- **R26.** Link, Internet (IP), Transport (TCP/UDP), and Application.
- **R27.** Client sends SYN (seq = x). Server replies SYN-ACK (seq = y, ack = x+1). Client sends ACK (ack = y+1). Random initial sequence numbers (ISNs) defend against spoofing and against confusion with segments from old connections.
- **R28.** The side that closes first enters TIME_WAIT for 2 x MSL, so that a lost final ACK can be retransmitted and delayed segments from the old connection die before the 4-tuple is reused. On Linux it lasts 60 s.
- **R29.** The peer sent FIN but your application never called `close()` on the socket. It is an application bug, typically a leaked fd or a missing close on an error path.
- **R30.** Flow control (the receiver's advertised window, rwnd) protects the receiver. Congestion control (cwnd) protects the network. The sender sends at most min(rwnd, cwnd).
- **R31.** Slow start begins cwnd at about 10 MSS (Linux initcwnd) and doubles it every RTT (exponential growth) until it hits ssthresh or a loss, then switches to congestion avoidance.
- **R32.** Nagle's algorithm holds back small segments while unacknowledged data is outstanding, coalescing them. Disable it with `TCP_NODELAY` for latency-sensitive request/response protocols that send small writes, because it interacts badly with delayed ACKs (adding ~40 ms stalls).
- **R33.** TCP is a reliable, ordered, congestion-controlled byte stream over a connection. UDP is connectionless, unordered, unreliable datagrams with message boundaries and minimal overhead.
- **R34.** A lookup is one small request and reply, so a handshake would double the latency. DNS uses TCP for zone transfers and when a response is truncated (TC bit set; EDNS0 raises the UDP limit). DNS-over-TLS and DNS-over-HTTPS also run over TCP (or QUIC).
- **R35.** A maps a name to an IPv4 address, AAAA to an IPv6 address, and CNAME makes the name an alias of another name (not allowed at the zone apex).
- **R36.** 2^5 - 2 = **30**.
- **R37.** ARP resolves an IPv4 address to a MAC address on the local link, using a broadcast request and a unicast reply. IPv6 uses NDP instead.
- **R38.** NAT rewrites private source addresses and ports to a public address and port, keeping a translation table so return traffic can be mapped back.
- **R39.** HTTP/2 multiplexes many concurrent streams over one TCP connection using binary framing, plus HPACK header compression. This removes HTTP-level head-of-line blocking and the need for 6 parallel connections.
- **R40.** On TCP, one lost packet stalls every HTTP/2 stream (TCP-level head-of-line blocking). QUIC runs independent streams over UDP, combines the transport and TLS 1.3 handshakes into 1 RTT, and supports connection migration across IP changes.
- **R41.** **1 RTT** for a full handshake. **0-RTT** resumption is possible, but that early data can be replayed, so it must be idempotent.
- **R42.** That a CA you trust vouches that the public key belongs to the named domain within its validity period. The client also checks the chain, the hostname (SAN), and revocation, and the server proves it owns the private key by signing the handshake.
- **R43.** An L4 balancer routes on IP and port (TCP/UDP) without reading the payload: fast and protocol-agnostic. An L7 balancer parses HTTP and can route by path, header, or cookie, terminate TLS, and retry.
- **R44.** BDP = bandwidth x RTT, the number of bytes that must be in flight to keep the link full. If the window is smaller than the BDP, the link is underused regardless of its speed.
- **R45.** `select`/`poll` pass and scan the whole fd set on every call, which is O(n). `epoll` registers interest once in the kernel and returns only the ready fds, which is O(ready). That is what makes 10k+ connections per thread feasible.

#### Databases

- **R46.** Atomicity, Consistency, Isolation, Durability.
- **R47.** Read uncommitted, read committed, repeatable read, serializable.
- **R48.** **Write skew**: two transactions read overlapping data, write disjoint rows, and together violate an invariant (for example, two on-call doctors both go off call).
- **R49.** PostgreSQL defaults to **read committed**; MySQL InnoDB defaults to **repeatable read**.
- **R50.** A clustered index stores the table rows themselves in key order (at most one per table; the InnoDB primary key). A secondary index is a separate structure whose entries point to the row (or, in InnoDB, to the primary key).
- **R51.** High fan-out (hundreds of keys per page) keeps the tree 3-4 levels deep even for billions of rows, so lookups take few page reads. The linked leaves make range scans sequential.
- **R52.** An index that contains every column a query needs, so the query is answered by an index-only scan with no table lookups.
- **R53.** Generally **no**, because of the leftmost-prefix rule. The index is sorted by `a` first. Some engines can do a "skip scan" when `a` has few distinct values.
- **R54.** A write-ahead log is an append-only log in which each change's record is made durable *before* the modified data page is written. Crash recovery replays it (redo) and rolls back uncommitted work (undo), and it turns random writes into sequential ones.
- **R55.** Multi-version concurrency control keeps multiple row versions so each transaction reads a consistent snapshot. Readers don't block writers and writers don't block readers; old versions are garbage-collected later (VACUUM, purge).
- **R56.** In two-phase locking, each transaction acquires locks in a growing phase and releases them in a shrinking phase, never acquiring after releasing. Strict 2PL holds write locks until commit. It guarantees serializability but can deadlock.
- **R57.** Store a `version` column. Update with `UPDATE ... SET ..., version = version + 1 WHERE id = ? AND version = ?`. If 0 rows were affected, someone else won the race: re-read and retry.
- **R58.** It takes row-level write locks on the selected rows until the transaction ends, so concurrent writers (and other `FOR UPDATE` readers) block. This is pessimistic locking for read-modify-write.
- **R59.** Every non-key attribute depends on "the key, the whole key, and nothing but the key" (no partial or transitive dependencies).
- **R60.** An LSM tree appends writes to a WAL and an in-memory memtable, flushes them as sorted immutable SSTables, and compacts in the background: fast writes, but read and space amplification. A B-tree updates pages in place: fast, predictable reads, but random-write I/O and page-level write amplification.
- **R61.** A per-SSTable Bloom filter answers "definitely not here" so point reads skip SSTables that cannot contain the key. It can return false positives but never false negatives.
- **R62.** Fetching N parent rows and then issuing one query per row for its children: N+1 round trips. Fix it with a JOIN, a batched `WHERE id IN (...)`, or eager loading in the ORM.

#### Computer Architecture

- **R63.** Compulsory (cold), capacity, and conflict misses. The fourth is coherence misses (invalidations from other cores).
- **R64.** Write-back writes to the cache, marks the line dirty, and writes to memory on eviction (less traffic). Write-through writes every store to the next level too (simpler coherence, more traffic), usually with a write buffer.
- **R65.** **M**odified (dirty, exclusive), **E**xclusive (clean, only copy), **S**hared (clean, possibly in other caches), **I**nvalid. MOESI and MESIF add Owned and Forward.
- **R66.** False sharing is when threads write *different* variables that sit on the same cache line, so the line ping-pongs between cores. Fix it with padding or `alignas(64)` (or `std::hardware_destructive_interference_size`), or with per-thread accumulators. Detect it with `perf c2c`.
- **R67.** Roughly L1 ~1 ns (4-5 cycles), L2 ~3-5 ns (12-16 cycles), L3 ~10-20 ns (40-70 cycles), local DRAM ~80-120 ns, and remote-NUMA DRAM ~150+ ns.
- **R68.** CDNA (Instinct MI-series) uses **64**-lane wavefronts. RDNA supports wave32 (the default for most compute) and wave64.
- **R69.** A VIPT cache is indexed with virtual-address bits and tagged with physical-address bits, so the set lookup overlaps the TLB lookup. To avoid aliasing, index + offset must fit in the page offset, so capacity / ways <= page size (32 KiB / 8 ways = 4 KiB).
- **R70.** RAW (true dependence), WAR (anti-dependence), and WAW (output dependence). Register renaming removes WAR and WAW; only RAW is fundamental.
- **R71.** Forwarding routes a result from a later pipeline stage (EX/MEM output) straight to a dependent instruction's ALU input, without waiting for write-back to the register file.
- **R72.** One stall (bubble) cycle, because the load's data is available only after MEM.
- **R73.** The reorder buffer holds in-flight instructions in program order. Results complete out of order but **retire** in order, which gives precise exceptions and lets the core squash wrong-path work after a mispredict.
- **R74.** About 15-20 cycles, plus the lost speculative work, which matters more on wide cores.
- **R75.** Simultaneous multithreading: one physical core runs 2 (or more) hardware threads that share the execution units and caches, filling issue slots one thread leaves idle. It gives typically 0-30% more throughput, and it adds noise to benchmarks.
- **R76.** RISC uses fixed-length, simple load/store instructions; CISC uses variable-length instructions with memory operands. Modern x86 decodes CISC instructions into RISC-like micro-ops, so the difference now lies mostly in decode cost and ISA baggage.
- **R77.** Little-endian stores the least significant byte at the lowest address (x86, and ARM in practice). Big-endian stores the most significant byte first. **Network byte order is big-endian** (`htonl`/`ntohl`).
- **R78.** The smallest normal FP32 value is 2^-126 ~= 1.18e-38. Machine epsilon (the ULP at 1.0) is 2^-23 ~= 1.19e-7.
- **R79.** Neither 0.1 nor 0.2 is exactly representable in binary, and their rounded sum lands one ULP above the double nearest to 0.3.
- **R80.** **No.** Rounding makes (a + b) + c differ from a + (b + c). Parallel reductions and floating-point atomics on GPUs sum in a nondeterministic order, so results vary slightly from run to run. Use deterministic reduction trees or tolerances. See [Performance Engineering 9.5](../computer-science/Performance_Engineering.md#95-why-parallel-and-gpu-reductions-are-non-deterministic).
- **R81.** A memory fence is an instruction or compiler barrier that orders memory operations across it (for example x86 `mfence`, ARM `dmb`, `std::atomic_thread_fence`). It controls ordering, not "flushing to memory".
- **R82.** S(N) = 1 / ((1 - p) + p / N): the serial fraction caps speedup at 1 / (1 - p).

#### Distributed Systems

- **R83.** During a network **partition**, a replicated system must choose between consistency (linearizability) and availability (every non-failed node answers). Without a partition you can have both.
- **R84.** **E**lse, with no partition, the trade-off is **L**atency versus **C**onsistency: synchronous replication costs latency.
- **R85.** **W + R > N**, so every read quorum overlaps every write quorum.
- **R86.** **2**, because a majority of 3 must stay up.
- **R87.** An even size adds no fault tolerance (4 nodes tolerate 1 failure, like 3) but adds cost and failure probability, and it risks even splits.
- **R88.** In an asynchronous system where even one process may crash, no deterministic algorithm can guarantee that consensus terminates. Real systems use timeouts (partial synchrony) or randomization and keep safety unconditional.
- **R89.** **3f + 1** nodes (PBFT), versus 2f + 1 for crash faults.
- **R90.** Linearizability respects real time: once a write completes, every later read sees it. Sequential consistency only requires *some* total order consistent with each process's program order, which may lag real time.
- **R91.** A Lamport clock is one counter: if a happened-before b then L(a) < L(b), but not the converse, so it cannot detect concurrency. Vector clocks keep one counter per node and can tell "happened-before" apart from "concurrent".
- **R92.** It **blocks**: if the coordinator crashes after participants vote yes, they must hold their locks until it recovers. It also has many round trips and a coordinator single point of failure.
- **R93.** A saga is a long-running transaction made of local transactions, each with a **compensating action** that is run in reverse on failure. It is orchestrated or choreographed, with no global locks.
- **R94.** Not end to end in general (the two generals problem). In practice you build "effectively once" from at-least-once delivery plus idempotent processing or deduplication, or from transactional consume-process-produce, as in Kafka transactions.
- **R95.** Adding or removing a node remaps only about K/N keys instead of nearly all of them. Virtual nodes smooth the load and allow weighting by capacity.
- **R96.** A fencing token is a monotonically increasing number issued with each lock or lease grant. The storage layer rejects writes carrying an older token, so a paused "zombie" former lock holder cannot corrupt data.
- **R97.** Split brain is when a partition leads two nodes to each believe they are leader and accept writes. Prevent it by requiring a majority quorum to lead (the minority side cannot), and use fencing tokens or STONITH for shared resources.
- **R98.** In O(log N) rounds: each round roughly doubles the number of informed nodes.
- **R99.** An idempotency key is a client-generated unique ID sent with a mutating request. The server stores the outcome under that key and returns the stored result on retries instead of re-executing, as in payment APIs.
- **R100.** **Closed** passes calls through and counts failures. **Open** fails fast for a cool-down period. **Half-open** lets a few trial calls through and closes again on success.

### A4 Drill-Chain Model Answers

#### Chain 1 Answers: URL

**C1.1** (The 60-second overview, which you then expand on request.) The browser parses the URL and checks its caches and HSTS. It resolves the name through DNS, opens a TCP connection (or QUIC), and negotiates TLS 1.3, using ALPN to choose HTTP/2 or HTTP/3. It sends `GET /search?q=gpu` with headers and cookies. The request travels through anycast, CDN, and load balancers to an application server, which may hit caches and databases. The response streams back, and the browser parses HTML, fetches subresources, builds the DOM and CSSOM, runs JavaScript, then lays out, paints, and composites. State up front that you will go layer by layer and ask where they want depth.

**C1.2** The browser:
- Decides whether the input is a URL or a search query.
- Applies **HSTS**: if the domain is on the preload list or sent an HSTS header before, it upgrades to HTTPS without trying plain HTTP.
- Checks a **service worker**, which may answer from its cache.
- Checks the **HTTP cache**: a fresh entry under `Cache-Control: max-age` means no network at all, while a stale one leads to a conditional request (`If-None-Match` / `If-Modified-Since`).
- Checks for an existing **pooled connection** to the origin, which would skip DNS, TCP, and TLS entirely.

**C1.3** The lookup goes through, in order:
1. The browser's DNS cache.
2. The OS stub resolver: `/etc/hosts` per `nsswitch.conf`, then the local cache (`systemd-resolved`, nscd).
3. The configured **recursive resolver** (ISP, 8.8.8.8, or corporate). On a cache miss it walks the hierarchy: a **root** server returns a referral to the `.com` **TLD** servers, which return a referral to `example.com`'s **authoritative** servers, which answer with A/AAAA records (often after following a CNAME to a CDN hostname).

Each answer carries a TTL and is cached at each level. Modern browsers may use DNS-over-HTTPS straight to a resolver, bypassing the OS.
- **C1.3a** Classic DNS over UDP is limited to 512 bytes. **EDNS0** advertises a larger UDP buffer (1232 bytes is the common safe default, to avoid IP fragmentation). If the answer still doesn't fit, the server sets the **TC (truncated)** bit and the client retries over **TCP**.
- **C1.3b** **TTL caching.** Resolvers, OSes, browsers, and some applications (old JVMs cached forever) keep the old answer until its TTL expires, and some ignore the TTL. For planned failovers, lower the TTL well in advance (for example, from 3600 to 60 s) or fail over behind a stable anycast or load-balancer IP instead of through DNS.
- **C1.3c** Two mechanisms. **GeoDNS / latency-based DNS** answers with an edge IP close to the resolver's location (EDNS Client Subnet sharpens this). **Anycast** advertises the same IP from many locations via BGP, so routing delivers packets to the topologically nearest edge.

**C1.4** The kernel looks up `8.8.8.8` in its **routing table**. It isn't on-link, so the packet goes to the **default gateway**. The kernel needs the gateway's MAC address, which comes from the **ARP** cache or an ARP request (NDP for IPv6). It builds an Ethernet/Wi-Fi frame addressed to the gateway's MAC and the destination IP. The home router **NATs** the private source address and port to its public IP. Each router hop then forwards by longest-prefix match, decrementing the TTL, and between ISPs the paths are chosen by **BGP**.

**C1.5** The exchange is SYN (client ISN), SYN-ACK (server ISN, ack), ACK, and the two sides also negotiate MSS, window scaling, SACK, and timestamps in the options. If the SYN is lost, the client retransmits after the initial RTO of **1 s** (RFC 6298), then backs off exponentially (2, 4, 8, ... s), up to `net.ipv4.tcp_syn_retries` (6 by default, about 127 s in total). That is why a blackholed port "hangs" instead of failing fast, while a closed port fails immediately with RST. Servers under SYN floods use **SYN cookies** so they need no state until the final ACK.

**C1.6** The ClientHello contains supported TLS versions, cipher suites, **key shares** (ephemeral ECDHE public keys, for example X25519, plus hybrid post-quantum groups such as X25519MLKEM768 in current browsers), **SNI** (the hostname, so the server picks the right certificate), **ALPN** (`h2`, `http/1.1`), and signature algorithms. The server replies with its key share; both sides derive the handshake keys. The server then sends its **certificate chain** and a **CertificateVerify**, a signature over the handshake transcript made with the certificate's private key, plus `Finished`. The client validates the chain up to a trusted root, checks the hostname against the SAN, the validity dates, and revocation (OCSP stapling, CRLs), and verifies the signature. That completes in 1 RTT, with forward secrecy from the ephemeral keys.
- **C1.6a** The attacker can intercept packets but cannot produce a valid certificate for `example.com` signed by a CA the browser trusts, nor a CertificateVerify signature without the private key. So impersonating the server fails validation. ECDHE means passive recording doesn't reveal the keys, and AEAD encryption (AES-GCM, ChaCha20-Poly1305) means tampering is detected. HSTS stops SSL-stripping downgrades. The residual risks are a compromised CA or a user clicking through a warning; Certificate Transparency logs help detect mis-issuance.
- **C1.6b** Validation fails, and the browser shows a full-page interstitial error (`NET::ERR_CERT_DATE_INVALID`). With HSTS, the user cannot click through. Non-browser clients (curl, gRPC) abort the handshake. Operationally this is a classic outage cause; the cure is automated renewal (ACME / Let's Encrypt) plus expiry monitoring.

**C1.7** HTTP/2 is negotiated inside the TLS handshake via **ALPN** (the client offers `h2`, `http/1.1`). HTTP/3 is discovered through an **Alt-Svc** response header or an **HTTPS DNS record** advertising `h3`. The browser then tries QUIC over UDP/443, often racing it against TCP, and falls back if UDP is blocked.

**C1.8** On a cold connection, beyond the DNS lookup:

| Setup | RTTs to first response byte |
|---|---|
| TCP + TLS 1.2 | 1 (TCP) + 2 (TLS) + 1 (HTTP) = **4** |
| TCP + TLS 1.3 | 1 + 1 + 1 = **3** |
| QUIC (HTTP/3) | 1 (combined transport + TLS) + 1 (HTTP) = **2** |
| TLS 1.3 / QUIC 0-RTT resumption | request sent with the first flight: **1** over QUIC (TCP still needs its handshake RTT, unless TCP Fast Open is used) |

At a 100 ms RTT, the difference between 4 and 2 RTTs is 200 ms, which is why CDNs terminate TLS close to users.

**C1.9** Anycast or GeoDNS steers the client to an edge point of presence, where a **CDN** may serve a cached response. Otherwise the request goes to an **L4 load balancer** (ECMP / Maglev-style consistent hashing), then an **L7 proxy** (TLS termination, routing, auth, rate limiting), then an **app server**. The app server consults an in-memory cache (Redis or Memcached), calls other services over RPC with timeouts, and queries a database (read replicas for searches) or a search index. The response is compressed (gzip/brotli) and streamed back. Observability spans this whole path: a trace ID is propagated in headers.

**C1.10** The browser:
1. Parses HTML incrementally into the **DOM**, while a preload scanner fetches CSS, JS, and images early.
2. Builds the **CSSOM** from CSS. CSS is render-blocking, and synchronous `<script>` blocks parsing (unless `defer` or `async`).
3. Runs JavaScript, which may mutate the DOM.
4. Combines DOM and CSSOM into the **render tree**, computes geometry (**layout**), **paints** layers, and has the GPU **composite** them.

Later DOM or CSS changes may trigger reflow or repaint; animations that only use `transform`/`opacity` stay on the compositor.

**C1.11** Measure, don't guess.
- **Client side:** the DevTools network waterfall, and the Navigation/Resource Timing APIs break each request into DNS, connect, TLS, TTFB, and download. Core Web Vitals (LCP, INP, CLS) come from real-user monitoring.
- If **TTFB** dominates, look at **server-side distributed traces** to find the slow span (a DB query, a cold cache, a downstream call). If DNS, connect, or TLS dominate, it's network or edge placement. If download or render dominates, look at bytes, render-blocking resources, and main-thread JavaScript.
- Always compare the p50 with the p99 and segment by geography and device.

#### Chain 2 Answers: malloc of 1 GB

**C2.1** 1 GiB is far above glibc's **mmap threshold**: 128 KiB by default, adjusted dynamically up to 32 MiB on 64-bit systems after large frees. So `malloc` skips the heap arenas and calls `mmap(NULL, 1 GiB + header, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0)`, rounded up to whole pages. It writes a small chunk header (size plus the `IS_MMAPPED` bit) at the start and returns the address just past the 16-byte header. The arena locks are never touched.

**C2.2** The kernel creates a new **VMA** (`vm_area_struct`) describing the range, its permissions, and that it is anonymous and private, and checks the overcommit policy. **It allocates no physical pages and fills in no PTEs.** VSZ grows by about 1 GiB immediately; **RSS barely changes**. The call is fast, in the microseconds. See [CS Fundamentals 1.11](../computer-science/CS_Fundamentals.md#111-linux-memory-management-internals).

**C2.3** Usually **yes**. `vm.overcommit_memory = 0` (the default heuristic) refuses only allocations that obviously cannot be satisfied (roughly more than RAM plus swap). `1` always says yes. `2` (strict) enforces a commit limit of swap + RAM x `overcommit_ratio` and would refuse once `Committed_AS` exceeds `CommitLimit`. `RLIMIT_AS` (`ulimit -v`) or a cgroup memory limit can also cause failures, but note that cgroup v2's `memory.max` is enforced at fault time, not at `mmap` time. The consequence: a successful `malloc` does **not** mean the memory exists, and failure shows up later as the OOM killer, not as `NULL`.

**C2.4** The first store hits a virtual address with no valid PTE, and the MMU raises a **page fault**. The kernel's fault handler finds the VMA covering the address and checks that a write is allowed. Because the region is anonymous and the page was never touched, it allocates a free page (from the buddy allocator via per-CPU lists, on the local NUMA node), **zeroes** it (for security), installs the PTE (allocating intermediate page-table pages if needed), updates the RSS counters and the LRU lists, and returns. The faulting instruction is then **re-executed** and succeeds. This is a **minor fault**: no I/O was involved.
- **C2.4a** 1 GiB / 4 KiB = **262,144** faults. Each costs on the order of 0.5-1 µs (trap, allocation, zeroing 4 KiB, PTE update), so the total is about **0.1-0.3 s**, often more than the `memset` itself. With **THP** enabled and the region 2 MiB-aligned, the kernel can fault in **2 MiB pages: only 512 faults** (zeroing still costs the same bandwidth). You can avoid faults in the critical path with `MAP_POPULATE`, `madvise(MADV_POPULATE_WRITE)` (Linux 5.14+), or pre-touching during initialization. Measure with `perf stat -e page-faults,minor-faults,major-faults`.
- **C2.4b** Read faults on untouched anonymous memory map the shared **zero page** read-only, so no new memory is allocated per page and RSS does not grow for those pages. The first *write* to each page then takes another fault (copy-on-write from the zero page) to get a private page. Benchmarks that "touch" memory by reading therefore measure the wrong thing.
- **C2.4c** Under the default policy, the node local to the **CPU that first touched** each page (**first-touch**). If one thread does the `memset` and 64 threads on two sockets later use the buffer, half of them make remote accesses. Fixes: initialize in parallel with the same thread layout as the compute (first touch matched to use), or use `numactl --interleave`, `mbind`, or `set_mempolicy`. See [Performance Engineering 7.2](../computer-science/Performance_Engineering.md#72-first-touch-placement).

**C2.5** The **TLB**. 1 GiB of 4 KiB pages is 262,144 translations, while a core's L2 TLB holds roughly 2-3K entries (a few MiB of reach), so random access misses the TLB on nearly every access and pays a page walk each time. Fixes: **huge pages** (THP via `madvise(MADV_HUGEPAGE)`, or explicit hugetlbfs 2 MiB / 1 GiB pages), which give 2 MiB pages 512x the reach, and making access patterns more local. Confirm with `perf stat -e dTLB-load-misses` (or the vendor's page-walk events).

**C2.6** The page allocator falls below its watermarks. **kswapd** starts background reclaim: it evicts clean page-cache pages, writes back dirty ones, and swaps out anonymous pages if swap exists. The faulting thread may then do **direct reclaim**, stalling. If reclaim cannot free enough, the **OOM killer** chooses a victim by `oom_score` (roughly the share of memory it uses, adjusted by `oom_score_adj`), likely this process, and sends **SIGKILL**. No error is returned to `memset`; the process just dies, and `dmesg` shows "Out of memory: Killed process ...". Under a cgroup limit, the cgroup's own OOM handling kills within the container. With `overcommit_memory = 2`, the earlier `malloc` would have returned NULL instead.

**C2.7** **Yes, immediately**: mmapped chunks are returned with `munmap`, which removes the VMA, frees the pages, and shoots down TLB entries on other CPUs. glibc raises its dynamic mmap threshold only when the freed mmapped chunk is at most 32 MiB (DEFAULT_MMAP_THRESHOLD_MAX), so freeing this 1 GiB chunk leaves the threshold unchanged. Freeing, say, a 4 MiB mmapped chunk would raise it to 4 MiB (and the trim threshold to 8 MiB). A **100-byte** allocation comes from an arena (the `brk` heap or a per-thread arena). `free` puts it in a bin for reuse, and memory goes back to the OS only when the top of the heap is free (trimmed beyond `M_TRIM_THRESHOLD`) or when `malloc_trim()` is called. Fragmentation can therefore keep RSS high long after the program frees most objects. jemalloc and tcmalloc handle this better with `madvise(MADV_DONTNEED/MADV_FREE)` purging.

**C2.8** `calloc` is faster for fresh large allocations. glibc knows that freshly mmapped anonymous pages are already zeroed by the kernel, so it **skips the explicit memset**, and pages are zeroed lazily, only when touched. Untouched pages cost nothing. `malloc` + `memset` touches and writes every page up front: 262,144 faults *plus* a redundant second zeroing pass. (For small `calloc` from a reused arena chunk, glibc does have to memset.)

**C2.9** Pageable memory can be swapped or moved, so the GPU's DMA engine cannot safely read it directly. The HIP runtime **stages** the copy, copying chunks into an internal **pinned** (page-locked) bounce buffer with the CPU and then DMAing from there. That adds an extra memcpy, limits overlap, and makes `hipMemcpy` effectively synchronous. Memory from `hipHostMalloc`, or registered with `hipHostRegister`, is pinned and mapped for the device, so DMA reads it directly at close to PCIe/xGMI peak and `hipMemcpyAsync` can overlap with kernels. The cost: pinned memory is unswappable, and allocating lots of it is slow and can starve the OS. Pin a reusable staging pool, not everything. See [Parallel and GPU Programming 26](../ml-gpu/Parallel_GPU_Programming.md#26-hip-programming-model).

**C2.10** Tools for each step:
- `strace -e trace=mmap,munmap,brk ./app` shows the 1 GiB `mmap`.
- `/proc/<pid>/status` (VmSize vs VmRSS) and `/proc/<pid>/smaps` (per-VMA `Rss`, `AnonHugePages`) show the memory state.
- `perf stat -e page-faults,minor-faults,major-faults,dTLB-load-misses` counts faults and TLB misses.
- `/usr/bin/time -v` reports the max RSS and fault counts.
- `numastat -p <pid>` shows NUMA placement.
- `grep -E 'Committed_AS|CommitLimit' /proc/meminfo` shows the overcommit state.
- `dmesg` shows OOM kills.

See [Debugging and Profiling Tools 12. strace and ltrace](../tools/Debugging_and_Profiling_Tools.md#12-strace-and-ltrace) and [8. perf Fundamentals](../tools/Debugging_and_Profiling_Tools.md#8-perf-fundamentals-and-hardware-counters).

#### Chain 3 Answers: HIP Kernel Launch

**C3.1** `hipcc` (Clang with the HIP toolchain) compiles the source twice: once for the host (x86-64) and once per GPU target (`--offload-arch=gfx942`, for example). In host code, the triple-chevron launch is lowered to a call that pushes the launch configuration (grid, block, shared memory, stream) via `__hipPushCallConfiguration`, then calls a compiler-generated **host stub** (`__device_stub__myKernel`). The stub calls `__hipPopCallConfiguration` to retrieve grid, block, shared memory and stream, packs pointers to the arguments, and calls **`hipLaunchKernel`** with the kernel handle. In current Clang the handle is a global variable named after the kernel symbol, not the stub function. Exact symbols vary by ROCm/Clang version. `hipLaunchKernelGGL(...)` is the macro form of the same launch.

**C3.2** The device code objects (AMDGPU ELF files, one per target architecture) are bundled into an **offload bundle** ("fat binary") embedded in the host executable, in the `.hip_fatbin` section. Compiler-generated static constructors call `__hipRegisterFatBinary` and `__hipRegisterFunction`, mapping each host stub to its device kernel symbol. At load time or first use, the runtime picks the code object whose target ID matches the installed GPU (for example `gfx942`, including features such as `xnack`) and loads it onto the device. If no compatible code object exists, the launch fails with a "no binary for GPU" / invalid-device-function error. This is a classic deployment bug when a build omits the target architecture. Each kernel has a **kernel descriptor** (the `<name>.kd` symbol) recording VGPR/SGPR counts, LDS size, scratch size, and the entry point.

**C3.3** `hipLaunchKernel`:
1. Validates the configuration (block size at most the device limit, usually 1024 threads; enough LDS) and resolves the stream.
2. Looks up the loaded kernel for the stub.
3. Copies the argument values into a **kernarg buffer** in GPU-visible memory, following the kernel's argument layout.
4. Builds an **AQL kernel-dispatch packet** (64 bytes): workgroup and grid sizes, private-segment (scratch) and group-segment (LDS) sizes, the **kernel object** (address of the kernel descriptor), the **kernarg address**, a **completion signal**, and header bits for barrier and acquire/release fence scopes.

The HIP runtime (part of the CLR, built on ROCclr) does this on top of the **ROCr** HSA runtime.

**C3.4** **There is no syscall per launch.** At stream creation, the runtime asks the kernel driver (**amdkfd**, through ioctls on `/dev/kfd`) to create a **user-mode queue**: a ring buffer in memory visible to both host and GPU, plus a **doorbell**. To launch, the runtime reserves a slot by atomically incrementing the queue's write index, writes the packet body, publishes the header last with release semantics so the GPU never sees a half-written packet, and **rings the doorbell**: a store to a memory-mapped doorbell page that tells the GPU's command processor there is new work. This user-space submission path is why launches cost microseconds rather than tens of microseconds.

**C3.5** The **command processor** (packet processor) reads the AQL packet and honors the barrier bit and acquire fence (for example, invalidating caches so the kernel sees host writes). It then hands the grid to the **workgroup dispatcher**, which splits it into workgroups and assigns each to a compute unit (CU) that has room. On the CU, each workgroup becomes wavefronts of **64 lanes** on CDNA. Registers (VGPRs/SGPRs) and **LDS** are allocated, and the wavefronts are scheduled on the SIMD units, which interleave many wavefronts to hide memory latency. When all workgroups finish, the end-of-kernel **release fence** makes results visible at the requested scope (writing back caches as needed), and the **completion signal** is decremented.
- **C3.5a** **Occupancy** limits, per CU or per SIMD: **VGPRs** per wavefront (the register file is split among resident waves; more VGPRs per wave means fewer waves), **SGPRs**, **LDS** per workgroup (64 KiB per CU on CDNA3 is shared among resident workgroups), the hardware maximum waves per SIMD and workgroup slots, plus scratch availability. The tightest one wins. The compiler's resource usage (`-Rpass-analysis=kernel-resource-usage`, or the `.kd` metadata) and the profiler's occupancy metrics show which one is binding. See [AMD GPU Architecture and Profiling](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md).

**C3.6** Immediately after the packet is enqueued, because launches are **asynchronous**. Work in the same stream executes in order; different streams may overlap. The host learns of completion through the packet's **completion signal**. `hipStreamSynchronize`, `hipEventSynchronize` (after `hipEventRecord`), or `hipDeviceSynchronize` wait on it, by spinning or by blocking on an interrupt-backed wait depending on flags. `hipStreamQuery` and `hipEventQuery` poll without blocking. Host timers around the launch call alone measure only enqueue time; use events or a profiler. See [Parallel and GPU Programming 22](../ml-gpu/Parallel_GPU_Programming.md#22-streams-events-and-concurrency).

**C3.7** **Asynchronously and late.** The launch itself returns success. The fault happens while the kernel runs: the GPU raises a memory-access fault, the driver and runtime report it (typically a "Memory access fault by GPU node-N ... on address ..." message), and the process is usually aborted, or later API calls return errors. Either way it surfaces at some later sync or API call, not at the faulting launch. To localize it:
- Set **`AMD_SERIALIZE_KERNEL=3`** (and `AMD_SERIALIZE_COPY=3`) so the runtime waits around each launch and the host backtrace points at the right launch site.
- Check `hipGetLastError()` / `hipPeekAtLastError()` after launches in debug builds, plus `hipDeviceSynchronize()`.
- Use **ROCgdb** to stop on the faulting wavefront, and build with address sanitizer for GPU (`-fsanitize=address` with `xnack+` targets) to find the exact out-of-bounds access.
- Raise **`AMD_LOG_LEVEL`** to see which API calls preceded the fault.

**C3.8** On the order of **a few microseconds** of host-side enqueue cost per launch, plus GPU-side dispatch latency. That is negligible for a 1 ms kernel and dominant for a 5 µs one. Remedies:
- **Fuse kernels** (fewer, bigger launches).
- **HIP graphs** (`hipStreamBeginCapture` / `hipGraphLaunch`): record a sequence once and replay it with much lower per-node overhead.
- **Persistent kernels** that pull work from a device-side queue.
- Do more work per thread, and avoid synchronous calls between launches (`hipMemcpy` or `hipMalloc` in the loop).

In profiles, this pattern looks like gaps between short kernels on the timeline.

**C3.9** **API tracing:** rocprofiler-sdk (used by `rocprofv3`) intercepts the HIP and HSA runtime API tables, so every `hipLaunchKernel` call is recorded with host timestamps and correlation IDs. **Kernel dispatch tracing:** it intercepts the HSA queue so each AQL packet can be observed, with profiling-enabled completion signals giving GPU start and end timestamps per dispatch, correlated back to the API call. **Counter collection:** around each dispatch the tool configures hardware performance counters (in the shader engines, texture/L2 units, and so on) and reads them back after completion. This usually requires serializing kernels, because counters are per-device state. `rocprof-compute` builds on this, collecting large counter sets per kernel and deriving metrics (roofline, occupancy, cache hit rates, pipeline utilization) from them.
- **C3.9a** Each hardware block has only a **small number of counter registers**, and some counters cannot be scheduled together. A full analysis needs hundreds of raw counters, so the profiler partitions them into **passes** and **reruns the application (or replays the kernel) once per pass**, collecting a different counter group each time. The consequences: run-to-run variation between passes, workloads must be deterministic, and very long applications need filtering (by kernel name or dispatch range) to keep profiling time reasonable. Profiling also perturbs timing: the observer effect, see [Performance Engineering 8.8](../computer-science/Performance_Engineering.md#88-profiler-overhead-and-the-observer-effect).

**C3.10** The first launch may include:
- **Lazy runtime and device initialization**: context creation, queue creation through KFD ioctls, kernarg pool allocation.
- **Loading the code object** onto the device.
- First-touch page faults on host and device allocations, or migrations for managed memory.
- Instruction-cache and TLB warm-up.
- Possibly JIT compilation (for example in frameworks that compile kernels at first use).

For benchmarking: run **warm-up iterations**, time with **events** over many iterations, report median and spread, and keep one-time costs out of steady-state numbers (but report them separately, since users feel startup latency). See [Performance Engineering 8.7 Timing GPUs](../computer-science/Performance_Engineering.md#87-timing-gpus).

#### Chain 4 Answers: fork in a Multithreaded Program

**C4.1** A copy of the **entire address space** (copy-on-write), meaning every thread's stack, every heap object, and every **mutex in whatever state it was in**, but **only one thread**: the one that called `fork()`. The other 7 threads simply do not exist in the child. The child also gets a duplicate fd table (sharing open file descriptions), the signal dispositions and the calling thread's signal mask, and its own new PID. See [CS Fundamentals 1.9](../computer-science/CS_Fundamentals.md#19-linux-process-lifecycle-signals-and-file-descriptors).

**C4.2** **The child deadlocks.** The mutex was copied in its locked state, and the thread that would unlock it does not exist in the child, so the first `lock()` in the child blocks forever. The same applies to any lock held at fork time: in third-party libraries, in iostream or locale internals, in a GPU runtime. glibc does protect its *own* malloc arenas: its fork implementation takes the arena locks before forking and resets them in the child. So plain `malloc` in the child works on glibc, but that is a libc courtesy, not a guarantee for your code. Data structures can also be left **half-modified** mid-update, which is worse than a held lock.

**C4.3** POSIX says that after `fork()` in a multithreaded process, the child may call only **async-signal-safe** functions until it calls one of the `exec` functions. In practice: adjust fds (`dup2`, `close`), maybe `setsid`, `chdir`, or `setrlimit`, then `execve` immediately, or `_exit` on failure. Don't log, allocate, or take locks.

**C4.4** `pthread_atfork(prepare, parent, child)` registers handlers. `prepare` runs in the parent before the fork, in reverse registration order, and typically locks all of a library's mutexes so none is mid-critical-section. `parent` and `child` run after the fork and unlock or reinitialize them. It is rarely complete because **every** library with internal locks would need to register correct handlers in a consistent lock order. Handlers can't fix state beyond locks (threads the library expected to exist, open GPU contexts, condition-variable waiters). Calling non-async-signal-safe functions in the child handler is itself problematic. POSIX's own rationale concedes it is of limited use. The real fix is not to fork a threaded process except to `exec` immediately.

**C4.5** The child gets **copies of the fd table entries pointing to the same open file descriptions**, so file offsets and status flags are shared. If both processes write to one fd without `O_APPEND`, they race on the offset. The race `O_CLOEXEC` fixes: thread A calls `open()` and plans to set `FD_CLOEXEC` with `fcntl` afterward, but thread B forks and execs in between, so the new fd **leaks** into an unrelated program (holding files open, keeping sockets alive, leaking privileges). Passing **`O_CLOEXEC` / `SOCK_CLOEXEC` / `pipe2(O_CLOEXEC)` / `accept4(SOCK_CLOEXEC)` atomically** at creation closes the window. Make close-on-exec the default in threaded programs.

**C4.6** `fork()` must **copy the page tables** (and VMAs) even though the data pages are shared COW. 20 GiB / 4 KiB = 5,242,880 PTEs x 8 B ~= **40 MiB of page tables**, which takes on the order of 0.2 s (Redis measures roughly 10 ms per GB of RSS on bare metal, and far more on some Xen VMs), during which the parent is stalled. That is a visible latency spike for something like Redis `BGSAVE`; huge pages shrink it 512x. While the child runs, every page the parent **writes** triggers a COW fault and a **copy**. A write-heavy parent can nearly double its memory use, which can trigger the OOM killer, or a fork failure under `overcommit_memory = 2`. On kernels before 5.8, a COW fault on a transparent huge page copied the whole 2 MiB. Since 5.8 the kernel splits the PMD and copies only the 4 KiB page, but Redis still recommends `transparent_hugepage=never`, because THP-backed memory makes post-fork COW and fault latency and memory growth worse.

**C4.7** Alternatives:
- **`posix_spawn`**: glibc implements it with `clone(CLONE_VM | CLONE_VFORK)`, so no page tables are copied and no unsafe code runs in between. It is the right default for "run a program".
- **`vfork`** shares the address space and suspends the parent until `exec`, with strict rules about what the child may do.
- **`clone3`** gives fine-grained control.
- A **fork server / zygote** is a small helper process created *early*, before any threads start, that forks workers on request over a pipe or socket.
- Avoid `system()`, which runs a shell; Python's `subprocess` already uses `posix_spawn` or `vfork` when it can.

**C4.8** Signal **dispositions** (handlers, ignored signals) are inherited, as is the calling thread's **signal mask**. **Pending signals** are cleared in the child. Timers (`alarm`, `setitimer`, POSIX timers) are **not** inherited. `fcntl` record locks (POSIX locks) are **not** inherited, while `flock` locks are associated with the shared open file description. Memory locks (`mlock`) and async I/O are not inherited, and the child's resource-usage counters start at zero.

**C4.9** GPU runtime state does **not survive fork**. The child inherits the parent's memory image, including the runtime's internal structures, handles to `/dev/kfd` and `/dev/dri`, queue mappings, and device-memory mappings, but the KFD driver associates queues, doorbells, and GPU virtual address spaces with the *parent* process. In the child these structures are stale: calls may fail, hang, or corrupt state. HIP, like CUDA, does not support using the runtime in a child forked after initialization. The rule: **initialize the GPU runtime after forking, in each worker**, or use the `spawn` or `forkserver` start method. The PyTorch symptom is "RuntimeError: Cannot re-initialize CUDA in forked subprocess. To use CUDA with multiprocessing, you must use the 'spawn' start method", which also appears on ROCm builds, because PyTorch exposes HIP through the `torch.cuda` API.

**C4.10** `multiprocessing` offers three start methods: **`fork`** (fast, but has every problem above), **`spawn`** (a fresh interpreter that re-imports the main module, so it is slower but safe), and **`forkserver`** (a clean single-threaded server process started early forks the workers). Since **Python 3.12**, `os.fork()` emits a `DeprecationWarning` when it detects multiple threads. In **Python 3.14** the default start method on Linux and other POSIX platforms changed from `fork` to **`forkserver`** (macOS has defaulted to `spawn` since 3.8). Pass the method explicitly (`multiprocessing.get_context("spawn")`) for portable, GPU-safe code; the arguments must then be picklable. See [Python Fundamentals](../languages/Python_Fundamentals.md) for the GIL and multiprocessing background.

---

*Back to [Table of Contents](#table-of-contents) · Theory: [CS Fundamentals](../computer-science/CS_Fundamentals.md) · Related practice: [Concurrency Coding Problems](../computer-science/Concurrency_Coding_Problems.md), [HLD Mock Interviews](HLD_Mock_Interviews.md), [Flashcards](Flashcards.csv), [Night-Before Cheat Sheet](Night_Before_Cheat_Sheet.md)*
