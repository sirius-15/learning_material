# High Level Design -- System Design Interview Reference

> A progressive, vendor-neutral guide to designing distributed systems in technical interviews. It starts with the interview process and core architecture building blocks, then applies them to fifteen common system design problems. Complements the system design overview in [CS Fundamentals](CS_Fundamentals.md#5-system-design).

## Table of Contents

1. [What High Level Design Covers](#1-what-high-level-design-covers)
2. [A Repeatable Interview Process](#2-a-repeatable-interview-process)
3. [Estimate the Workload](#3-estimate-the-workload)
   - [Latency Numbers to Know](#latency-numbers-to-know) · [Availability: Nines and Downtime](#availability-nines-and-downtime) · [Typical Per-Node Throughput](#typical-per-node-throughput) · [Hardware Bandwidths: Memory, GPU, and Interconnect](#hardware-bandwidths-memory-gpu-and-interconnect) · [Estimation Interview Questions](#estimation-interview-questions)
4. [Architecture Building Blocks](#4-architecture-building-blocks)
   - [4.1 Request Entry](#41-request-entry-and-application-services) · [4.2 Storage Choices](#42-storage-choices) · [4.3 Cache](#43-cache) · [4.4 Queues and Event Streams](#44-queues-and-event-streams) · [4.5 Partitioning and Replication](#45-partitioning-and-replication) · [4.6 Sync and Async Work](#46-synchronous-calls-and-asynchronous-work)
   - [4.7 Unique ID Generation](#47-unique-id-generation) (auto-increment, ticket server, UUIDv4/v7, Snowflake, base62)
   - [4.8 Geospatial Indexing](#48-geospatial-indexing) (geohash, quadtree, S2, H3)
   - [4.9 Bloom Filters and Merkle Trees](#49-bloom-filters-and-merkle-trees)
   - [4.10 Probabilistic Counting: HyperLogLog and Count-Min Sketch](#410-probabilistic-counting-hyperloglog-and-count-min-sketch)
   - [4.11 Stream Processing](#411-stream-processing) (windows, watermarks, late data, exactly-once, Lambda vs Kappa)
   - [4.12 Change Data Capture, Event Sourcing, CQRS, and the Outbox](#412-change-data-capture-event-sourcing-cqrs-and-the-outbox)
   - [4.13 Cache Stampede and Hot Keys](#413-cache-stampede-and-hot-keys)
   - [4.14 Interview Questions](#414-interview-questions)
5. [Cross-Cutting Design Decisions](#5-cross-cutting-design-decisions)
   - [5.1 Availability](#51-availability-reliability-and-graceful-degradation) · [5.2 Consistency](#52-consistency-and-correctness) · [5.3 Security](#53-security-and-privacy) · [5.4 Observability](#54-observability-and-operations) · [5.5 Tradeoff Pairs](#55-common-tradeoff-pairs)
   - [5.6 SLIs, SLOs, SLAs, and Error Budgets](#56-slis-slos-slas-and-error-budgets)
   - [5.7 Tail-Latency Amplification](#57-tail-latency-amplification)
   - [5.8 Backpressure and Load Shedding](#58-backpressure-and-load-shedding)
   - [5.9 Deployment Safety](#59-deployment-safety) (canary, blue-green, feature flags, rollback)
   - [5.10 Transactions Applied to Designs](#510-transactions-applied-to-designs) (FOR UPDATE vs optimistic versioning, write skew)
   - [5.11 Interview Questions](#511-interview-questions)
6. [Worked System Designs](#6-worked-system-designs)
   - [URL Shortener](#61-url-shortener)
   - [Rate Limiter](#62-rate-limiter)
   - [News Feed](#63-news-feed)
   - [Chat System](#64-chat-system)
   - [Video Streaming Platform](#65-video-streaming-platform)
   - [Ride-Sharing Service](#66-ride-sharing-service)
   - [Payment Processing](#67-payment-processing)
   - [Distributed Key-Value Store](#68-distributed-key-value-store)
   - [Search Autocomplete (Typeahead)](#69-search-autocomplete-typeahead)
   - [Web Crawler](#610-web-crawler)
   - [Notification System](#611-notification-system)
   - [Distributed Job Scheduler](#612-distributed-job-scheduler)
   - [Metrics, Logging, and Monitoring System](#613-metrics-logging-and-monitoring-system)
   - [Object Storage (S3-like)](#614-object-storage-s3-like)
   - [Ticket Booking (Seat Reservation)](#615-ticket-booking-seat-reservation)
7. [Interview Checklists and Pitfalls](#7-interview-checklists-and-pitfalls)
8. [Practice Prompts](#8-practice-prompts)

---

## 1. What High Level Design Covers

**High Level Design (HLD)** describes the major parts of a system, the data they own, and how requests and events flow between them. In an interview, the goal is to show how the design satisfies its requirements and where its important tradeoffs lie.

An HLD usually includes:

- Functional requirements: what users and operators need the system to do.
- Non-functional requirements: scale, latency, availability, durability, privacy, and consistency expectations.
- Public APIs and key data entities.
- Services, databases, caches, queues, and external systems.
- Synchronous request paths and asynchronous workflows.
- Partitioning, replication, failure handling, and operational signals.

HLD is not a detailed class diagram or a line-by-line implementation. Those are low-level design concerns. Mention an algorithm or data structure when it changes system behavior or scale, but keep the discussion focused on components, boundaries, data flow, and tradeoffs.

### The central design question

For each major requirement, ask: **which component is responsible, what data does it need, and what happens when that component is slow or unavailable?** This ties the architecture to concrete behavior instead of producing a list of fashionable technologies.

---

## 2. A Repeatable Interview Process

Treat the interview as a sequence of decisions. State assumptions aloud and invite the interviewer to correct them.

### Step 1: Clarify the requirements

Separate essential behavior from optional features. Then identify the constraints that affect architecture.

| Area | Questions to ask |
|---|---|
| Users and actions | Who uses the system, and what are the main reads and writes? |
| Scale | How many users, requests, records, or concurrent connections should it handle? |
| Latency | Which operations are interactive, and what response time is acceptable? |
| Availability | Is a brief outage acceptable? Can reads continue during a write outage? |
| Consistency | Must a read immediately see the latest write, or is bounded staleness acceptable? |
| Data | How long is data retained? Can it be deleted or corrected? |
| Scope | Which features are explicitly excluded from this design? |

Write down a short list of functional requirements and a short list of important non-functional requirements. For example, for a chat system: users can send direct messages, messages persist, and online recipients receive them quickly; group chat, voice calls, and end-to-end encryption may be either required or explicitly out of scope.

### Step 2: Identify the critical user journeys

Describe the most important request flows before drawing services. A system may have a write path, a read path, and one or more background paths. Focus first on the operation that defines the product, such as creating a short URL or delivering a message.

### Step 3: Estimate scale

Use rough, stated assumptions to find architectural pressure points. Do not spend interview time pretending estimates are precise. See [Estimate the Workload](#3-estimate-the-workload).

### Step 4: Define APIs and core data

Sketch a small set of APIs and the entities they read or change. This exposes missing requirements and helps determine the storage access pattern. The interface should make important semantics clear, such as pagination, idempotency, ordering, and authorization.

### Step 5: Draw the simplest viable architecture

Start with clients, an entry point, application services, durable storage, and any required asynchronous workers. Add a cache, queue, search index, or specialized service only when a requirement or workload justifies it.

### Step 6: Walk through the data flow

Follow one important request end to end. State where data is validated, authorized, written, acknowledged, cached, and eventually consumed. Include the response to the client and identify any work deferred to the background.

### Step 7: Find bottlenecks and failure modes

Ask what becomes saturated first, what happens when a dependency is slow, and which data can be rebuilt. Add mitigations such as partitioning, replication, backpressure, retries, timeouts, or graceful degradation as needed.

### Step 8: Explain tradeoffs and summarize

Compare the chosen design with a plausible alternative. Close by restating how the design meets the main requirements and naming its largest remaining constraint.

### Suggested time allocation

For a 45-minute interview, a useful starting split is 5 minutes for requirements, 5 for estimates and interfaces, 20 for the core design and flows, 10 for scaling and failure handling, and 5 for a concise summary. Adjust to the interviewer's direction; the design discussion matters more than following a timer exactly.

---

## 3. Estimate the Workload

Back-of-the-envelope math helps decide whether one database is enough, whether traffic is read-heavy, or whether a large object needs separate storage. Keep inputs explicit and round aggressively.

### Useful conversions

| Quantity | Approximation |
|---|---:|
| Seconds per day | 86,400 (about 100,000 for quick math) |
| 1 million requests per day | about 12 requests/second |
| 100 million requests per day | about 1,200 requests/second |
| 1 billion requests per day | about 12,000 requests/second |
| 1 KB × 1 billion records | about 1 TB before indexes and replicas |

### Core formulas

```text
average requests/second = requests/day ÷ 86,400
peak requests/second   = average requests/second × peak factor
storage                = records/day × average bytes/record × retention days
bandwidth               = requests/second × average bytes/request or response
```

If the prompt does not provide a peak factor, state an assumption such as 3× or 5× average traffic. Account for indexes, replication, metadata, and growth qualitatively; do not imply that raw payload size equals provisioned storage.

### Example: short-link reads

Assume 1 million new links per day and 100 reads per created link. That is roughly 100 million redirects/day, or about 1,200 average reads/second. With a 5× peak, design for roughly 6,000 reads/second. This read-heavy profile supports a cache in front of a key-value lookup. It does not, by itself, require a complex microservice architecture.

### What estimates should influence

- **High read repetition:** consider a cache or CDN, while defining staleness and invalidation behavior.
- **Large object payloads:** keep blobs in object storage and metadata in a database.
- **High write rate:** inspect partition keys, batching, append-oriented storage, and asynchronous work.
- **Global users:** consider regional placement, replication lag, and how writes are routed.
- **Long retention:** include lifecycle, archival, and deletion costs in the design.

### Latency numbers to know

The classic list (Jeff Dean and Peter Norvig, circa 2010) is still the vocabulary interviewers use. Hardware has moved since then, so learn the classic figure, a modern rough figure, and **how to derive it from bandwidth**. A derived number survives a follow-up question; a memorized one does not. For CPU-level numbers measured on real hardware, see [Latency Numbers to Know](Performance_Engineering.md#12-latency-numbers-to-know); the shorter table in [CS Fundamentals 5.9](CS_Fundamentals.md#59-back-of-the-envelope-estimation) uses some extrapolated values.

| Operation | Classic figure | Modern rough figure | Derivation or note |
|---|---:|---:|---|
| L1 cache reference | 0.5 ns | ~1 ns | 4–5 cycles at 4 GHz |
| Branch mispredict | 5 ns | ~3–5 ns | ~15–20 cycles of discarded pipeline work |
| L2 cache reference | 7 ns | ~3–4 ns | |
| **Mutex lock + unlock, uncontended** | 25 ns | ~15–25 ns | Two atomic read-modify-writes on a cache line this core already owns. Contended: microseconds (futex syscall, sleep, wake, context switch) |
| Main memory reference | 100 ns | ~80–130 ns | |
| **Compress 1 KB (Snappy/LZ4-class)** | 3 µs | ~1–3 µs | 1 KB ÷ ~0.5–1 GB/s per core for fast codecs; zstd/gzip are several times slower |
| **Send 1 KB over a 1 Gb/s link** | 10 µs | 8 µs | 1,024 B × 8 bits ÷ 10⁹ bits/s = 8.2 µs serialization. At 10 Gb/s: 0.8 µs. At 100 Gb/s: 82 ns, so propagation and software stack costs dominate |
| **Read 4 KB randomly from SSD** | 150 µs | ~20–100 µs (NVMe, queue depth 1) | Flash read latency dominates. Throughput comes from parallelism: ~1M random 4 KB IOPS per NVMe drive at high queue depth ≈ 4 GB/s |
| Read 1 MB sequentially from memory | 250 µs | ~50–100 µs on one core | 1 MB ÷ 10–20 GB/s single-thread bandwidth. A whole socket streams 300+ GB/s (≈ 3 µs per MB), which is the figure some "updated" tables quote |
| Round trip within a datacenter | 500 µs | ~100–500 µs (kernel TCP); ~2–5 µs (RDMA in a rack) | Software stack and switches, not the speed of light |
| Read 1 MB sequentially from SSD | 1 ms | ~150–350 µs | 1 MB ÷ 3–7 GB/s (NVMe Gen3–Gen4) |
| HDD seek | 10 ms | ~4–10 ms | Mechanical; unchanged in 20 years |
| Read 1 MB sequentially from HDD | 20 ms | ~5 ms | 1 MB ÷ ~200 MB/s |
| Packet California → Netherlands → California | 150 ms | ~150 ms | Light in fiber ≈ 200,000 km/s; 2 × 8,800 km ÷ 200,000 km/s ≈ 88 ms minimum, plus non-straight routes and queuing |

Design consequences: one cross-region round trip (about 100 ms) costs as much as about 200 in-datacenter round trips, so a request path should never make sequential cross-region calls. An uncontended lock is cheap, so the cost of a lock is **contention**, not the lock itself. Compressing 1 KB costs less than sending it over a 1 Gb/s link, so compressing network payloads usually pays off, but it rarely matters at 100 Gb/s.

### Availability: nines and downtime

| Availability | Downtime per year | Per 30-day month | Per day | Typical meaning |
|---|---:|---:|---:|---|
| 99% ("two nines") | 3.65 days | 7.2 hours | 14.4 min | Internal tools, batch systems |
| 99.5% | 1.83 days | 3.6 hours | 7.2 min | |
| 99.9% ("three nines") | 8.77 hours | 43.2 min | 1.44 min | Typical single-region web service |
| 99.95% | 4.38 hours | 21.6 min | 43.2 s | Common cloud service SLA tier |
| 99.99% ("four nines") | 52.6 min | 4.32 min | 8.6 s | Multi-zone, automated failover; humans cannot respond in time |
| 99.999% ("five nines") | 5.26 min | 25.9 s | 0.86 s | Telecom-grade; needs multi-region and very conservative change management |

Arithmetic: a year is 365.25 × 24 = 8,766 hours, so 0.1% of it is 8.77 hours. A 30-day month is 43,200 minutes, so 0.1% of it is 43.2 minutes.

**Composition rules:**

- **Serial dependencies multiply:** a request needing A (99.9%) and B (99.9%) gets at most 0.999 × 0.999 ≈ 99.8%. Ten serial 99.9% dependencies give about 99.0%. That is why deep synchronous call chains cannot be highly available.
- **Redundant replicas multiply the unavailability:** two independent replicas at 99% each give 1 − 0.01² = 99.99%, *if* failures are independent and failover works. Correlated failures (the same bad deploy, the same zone, the same configuration) break the independence assumption, which is why real systems fall far short of the formula.
- **Four nines leaves 4.3 minutes a month:** by the time someone is paged and logs in, the budget is gone. Four nines and above require automated detection and failover. SLOs and error budgets are covered in [5.6](#56-slis-slos-slas-and-error-budgets).

### Typical per-node throughput

Order-of-magnitude **planning ranges** for one commodity server (tens of cores, NVMe, 25–100 GbE). Real numbers depend heavily on payload size, query shape, durability settings, and tuning, so state assumptions and benchmark before committing. In an interview, these ranges are for deciding "one node, ten, or a thousand?"

| Component | Rough range per node | What limits it |
|---|---|---|
| Stateless app server (JSON API with business logic) | 1k–10k req/s | CPU per request, serialization, downstream calls |
| nginx or another L7 proxy (small responses, keep-alive) | Tens of thousands to 100k+ req/s | CPU and packets per second. New TLS handshakes cost far more than requests on reused connections |
| Relational database primary (PostgreSQL, MySQL) | Cached point reads: 10k–100k+/s. Small write transactions: ~1k–20k commits/s. Complex joins and reports: tens to hundreds/s | WAL fsync and group commit, lock contention, synchronous replication round trips, buffer-cache hit rate |
| Redis-class in-memory store (one shard) | ~100k–200k simple ops/s; 1M+ with pipelining | Single-threaded command execution; network round trips per command |
| Memcached-class (multithreaded) | Several hundred thousand to 1M+ gets/s | NIC packet rate, CPU |
| Kafka-class log, **per partition** | ~10 MB/s as a conservative planning number; tens of MB/s when measured and tuned | One leader appends in order; the consumer is often the real bottleneck. Partitions needed ≥ max(target ÷ producer rate per partition, target ÷ consumer rate per partition) |
| Kafka-class log, per broker | Hundreds of MB/s in; keep partition replicas per broker in the low thousands | NIC, disk, replication traffic (each byte is written RF times) |
| LSM key-value node (Cassandra-class) | ~10k–50k writes/s; reads depend on cache hit rate | Compaction I/O, CPU |
| NIC | 10 / 25 / 100 / 400 GbE ≈ 1.25 / 3.1 / 12.5 / 50 GB/s per direction | At small packet sizes, packets per second limit throughput before bytes do |

Worked use: "10M writes/s of 200-byte events into a log" is 2 GB/s. At 10 MB/s per partition, that is about 200 partitions, spread over brokers each taking a few hundred MB/s including replication, so **20–30 brokers**. "One Redis for 2M ops/s" is wrong by about 10×: use ~20 shards, or batch operations with pipelining.

### Hardware bandwidths: memory, GPU, and interconnect

For GPU/HPC and ML-infrastructure designs, the bandwidth hierarchy decides where data must live and which transfers are acceptable. These are vendor-published peaks (checked November 2026). Measured throughput is typically 70–90% of peak. Network figures are per direction; GPU link figures are often quoted bidirectionally, so check which one a datasheet means.

| Path | Peak bandwidth | Notes |
|---|---:|---|
| DDR5-4800, one channel | 38.4 GB/s | 4,800 MT/s × 8 B. 12 channels per socket ≈ 460 GB/s |
| HBM3, AMD MI300X | 5.3 TB/s | 192 GB per GPU |
| HBM3E, AMD MI325X / MI355X | 6.0 / 8.0 TB/s | 256 GB / 288 GB per GPU |
| HBM3 / HBM3E, NVIDIA H100 SXM / H200 | 3.35 / 4.8 TB/s | 80 GB / 141 GB per GPU |
| PCIe 4.0 x16 | ~32 GB/s per direction | 16 GT/s × 16 lanes × 128/130 encoding ÷ 8 bits ≈ 31.5 GB/s |
| PCIe 5.0 x16 | ~64 GB/s per direction | Datasheets often say "128 GB/s", which is bidirectional. GPU ↔ host path |
| PCIe 6.0 x16 | ~128 GB/s per direction | |
| AMD Infinity Fabric (xGMI), MI300X | 896 GB/s aggregate bidirectional per GPU | 7 links × 128 GB/s bidirectional (≈ 64 GB/s per direction per link) in a full mesh of 8 GPUs |
| AMD Infinity Fabric, MI355X | ~1.1 TB/s aggregate bidirectional per GPU | 7 links; published per-link figures differ between sources, so check AMD's platform datasheet |
| NVIDIA NVLink 4 (H100) / NVLink 5 (B200) | 900 GB/s / 1.8 TB/s bidirectional per GPU | Through NVSwitch, so any pair of GPUs can use the full bandwidth |
| InfiniBand HDR / NDR / XDR | 200 / 400 / 800 Gb/s per port = 25 / 50 / 100 GB/s per direction | NDR is typical for MI300X and H100 clusters; XDR (Quantum-X800) is the current generation |
| 400 GbE (RoCE) | 50 GB/s per direction | Common alternative to InfiniBand for scale-out |
| NVMe SSD, Gen4 / Gen5 | ~7 / ~14 GB/s sequential read per drive | |

What the ratios tell you:

- **HBM vs PCIe:** 5.3 TB/s ÷ 64 GB/s ≈ **80×**. Data that crosses PCIe on every step (host staging, small kernel inputs copied each iteration) wastes the GPU, so keep working sets resident in HBM and overlap the transfers that remain.
- **In-node vs scale-out:** about 450 GB/s per direction per GPU inside a node (xGMI mesh or NVLink) versus 50 GB/s per GPU on a 400G NIC is roughly **9×**. That is why tensor parallelism stays inside a node and data parallelism crosses nodes.
- **Loading weights:** 140 GB of BF16 weights (a 70B-parameter model) take 140 ÷ 7 ≈ 20 s from one Gen4 NVMe drive, about 2.2 s over PCIe 5.0 at 64 GB/s, and 140 GB ÷ 5.3 TB/s ≈ 26 ms to read once from HBM. Cold-start time for an inference replica is set by storage and PCIe, not by the GPU.
- **MI300X mesh caveat:** a single pair of GPUs talks over one xGMI link (~64 GB/s per direction), so point-to-point patterns (pipeline-parallel sends, KV-cache transfer) are slower on a mesh than on a switch, even though aggregate bandwidth is similar.

For collective-communication cost models, ridge points, and ML-specific numbers, see [ML Systems Design: Numbers Every ML Systems Engineer Should Know](../ml-gpu/ML_Systems_Design.md#3-numbers-every-ml-systems-engineer-should-know) and [Ridge Points: MI300X and a CPU](Performance_Engineering.md#33-ridge-points-mi300x-and-a-cpu). For CDNA hardware details, see [AMD GPU Architecture and Profiling](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md).

### Estimation interview questions

**Q1. Your service promises 99.95% monthly availability. It calls an auth service (99.99%), a database (99.95%), and a recommendation service (99.9%) synchronously on every request. Can you meet the promise?**

No. Serial availability is at most 0.9999 × 0.9995 × 0.999 ≈ 99.84%, which is 69 minutes of downtime a month against a budget of 21.6 minutes, before counting your own failures. Fixes: make recommendations optional (degrade to a cached or default list when they fail), which removes the 99.9% term and leaves 0.9999 × 0.9995 ≈ 99.94%. That is still short, so also cache auth tokens locally (validate signed tokens without calling auth), and run the database with automatic failover across zones to raise its effective availability. The general lesson: every synchronous hard dependency must be more available than your own target.

**Q2. How long does it take to copy 1 TB between two datacenters over a 10 Gb/s link? Over 1 Gb/s?**

1 TB = 8 × 10¹² bits. At 10 Gb/s that is 800 s, about 13 minutes at line rate. Realistically, at about 70% efficiency (TCP over a high-latency path, protocol overhead), it takes about 20 minutes. At 1 Gb/s it is 8,000 s, about 2.2 hours, or around 3 hours in practice. Follow-ups: for 1 PB at 10 Gb/s you need about 9 days at line rate, so physically shipping drives becomes competitive. Parallel streams help on high-latency paths, because one TCP flow is limited by window size ÷ RTT: a 16 MB window at 100 ms RTT caps one flow at about 160 MB/s.

**Q3. Estimate how many cache nodes you need for 3M reads/s of 2 KB values with a 500 GB working set.**

Memory: 500 GB ÷ (about 64 GB usable per node after overhead and headroom) ≈ 8 nodes, plus replicas. Ops: about 150k ops/s per single-threaded shard means 3M ÷ 150k = 20 shards. Several shards can run per machine, one per core, but bandwidth must also fit: 3M × 2 KB = 6 GB/s ≈ 48 Gb/s in total, so with 25 GbE nodes you need at least 2–3 nodes for bandwidth alone, and more at a safe utilization of about 50%. **Ops/s sets the shard count** (about 20 shards). **Memory sets the node count**: at least 8 nodes for 500 GB. Pack the 20 shards onto 8–10 nodes (2–3 shards per node, about 50–60 GB each). With 10 nodes, each carries 48 Gb/s ÷ 10 ≈ 5 Gb/s, well under a 25 GbE link at 50% utilization. With one replica per shard, that is 16–20 nodes. Check the hot-key distribution as well, since one hot key can exceed a shard regardless of the total.

**Q4. Why do the "send 1 KB over 1 Gb/s = 10 µs" and "datacenter round trip = 500 µs" numbers differ by 50×, and why does it matter?**

The first is **serialization delay**, the time to put 8,192 bits onto a 1 Gb/s wire. The second is a full **round trip**: kernel network stacks on both sides, NIC interrupts, several switch hops, and the application's scheduling. The design consequence is that small messages are dominated by fixed per-message costs, not by bandwidth. Sending 1,000 small messages one at a time costs about 1,000 round trips, while batching them into one message costs about one round trip plus 1 MB of serialization (about 8 ms at 1 Gb/s, 0.8 ms at 10 Gb/s). This is why multi-get, pipelining, and batching are the first tools for fan-out-heavy designs, and why RDMA, which removes the kernel stack and gives microsecond round trips, matters for HPC and ML collectives.

---

## 4. Architecture Building Blocks

### 4.1 Request entry and application services

| Component | Responsibility | Design questions |
|---|---|---|
| DNS and edge layer | Route users to a nearby or healthy entry point | How is traffic shifted during a regional outage? |
| CDN | Cache static or cacheable content close to users | What is cacheable, and how is old content invalidated? |
| Load balancer | Distribute connections or requests across healthy servers | Is routing based on connection health, request path, or both? |
| API gateway | Centralize routing and selected cross-cutting checks | Does it become a bottleneck or single operational dependency? |
| Stateless service | Validate requests and implement business operations | Can any instance handle the next request? |

Keep business ownership in services that can enforce its rules. An API gateway can authenticate or route requests, but it should not become the home for all application logic.

### 4.2 Storage choices

Choose storage from the access pattern, consistency needs, data relationships, and operational constraints.

| Storage type | Often fits | Main considerations |
|---|---|---|
| Relational database | Transactions, constraints, joins, and structured records | Indexes, write contention, schema changes, and sharding complexity |
| Key-value store | Lookup by a known key at high scale | Key design, hot partitions, query limitations, and consistency options |
| Wide-column store | Large distributed datasets with known query patterns | Partition-key quality, clustering order, and denormalized writes |
| Document database | Records with flexible or nested shapes | Index design, query support, and cross-record transaction limits |
| Search index | Text search, filtering, and relevance ranking | Usually derived from a source of truth; indexing may be delayed |
| Object storage | Large blobs such as images, media, and backups | Metadata lookup, upload authorization, lifecycle, and CDN delivery |
| Time-series store | Timestamped metrics or events | Retention, aggregation, write volume, and time-based partitioning |

These are broad tendencies, not guarantees. Product implementations differ, so explain required properties instead of relying on a database brand name.

### 4.3 Cache

A cache reduces repeat reads and latency but introduces stale data, eviction, and invalidation questions.

**Cache-aside flow:**

1. The service reads the cache.
2. On a miss, it reads the source of truth.
3. It stores the result with an expiry and returns it.
4. A write updates the source of truth and either invalidates or refreshes the cached value.

Define what happens when the cache is unavailable, when many callers miss for the same key, and when a cached value is older than allowed. Cache data that can be reconstructed; do not silently make a volatile cache the only copy of critical data.

For write policies (write-through, write-behind, write-around) and eviction policies, see [Caching](CS_Fundamentals.md#53-caching). For what to do when many callers miss the same key at once, and for single keys that overload one shard, see [Cache Stampede and Hot Keys](#413-cache-stampede-and-hot-keys).

### 4.4 Queues and event streams

Queues and streams separate a producer from work that can happen later. They absorb bursts, enable retries, and support independent consumers.

| Queue or task queue | Event stream |
|---|---|
| A message usually represents work for one consumer in a group. | An event can be retained and read by multiple consumer groups. |
| Useful for jobs such as sending an email or generating a thumbnail. | Useful for event history, analytics pipelines, and multiple downstream projections. |
| Acknowledge completion; retry or dead-letter failed work. | Track consumer offsets and define retention and replay behavior. |

Assume delivery can be repeated unless the chosen system and workflow provide a stronger guarantee. Make handlers idempotent, bound retries, and monitor queue age as well as queue size.

### 4.5 Partitioning and replication

- **Partitioning (sharding)** divides records among nodes. Choose a key that supports common reads and spreads load. A poor key can create hot partitions or require expensive cross-shard queries.
- **Replication** keeps copies of data for availability and read capacity. It introduces lag and conflict handling, especially across regions.
- **Repartitioning** changes key placement as the system grows. Consider how data moves and how traffic behaves during the move.
- **Hot keys** need explicit attention. A popular item can overload one partition even when total capacity appears adequate.

Avoid introducing sharding before the workload needs it. A single well-indexed database is often the simplest starting point and can be easier to operate correctly.

### 4.6 Synchronous calls and asynchronous work

Use a synchronous call when the caller needs an immediate result to continue. Use asynchronous work when it can complete later and the product can acknowledge an accepted request first.

For an asynchronous flow, define the durable handoff. If a database write and event publish must agree, consider a transactional outbox: commit the business update and an outbox record in one database transaction, then publish the event with a retrying worker. Consumers should deduplicate repeated events where necessary.

The outbox, change data capture, event sourcing, and CQRS are compared in [4.12](#412-change-data-capture-event-sourcing-cqrs-and-the-outbox).

### 4.7 Unique ID Generation

Almost every design needs IDs: short-link codes, post and message IDs, payment IDs. First ask which properties the ID needs:

- **Unique** across all writers, including across shards and regions.
- **Sortable by time** (roughly). This keeps B-tree inserts at the right edge of the index, which gives good cache locality and few page splits, and it makes cursor pagination (`WHERE id < :cursor`) cheap.
- **Compact:** 64-bit integers are cheaper than 128-bit values in indexes, foreign keys, and caches.
- **Coordination-free:** generated without a network call on the write path.
- **Not guessable:** sequential public IDs reveal volume ("order 10,482") and invite enumeration.

| Scheme | Size | Time-sortable | Coordination | Throughput | Pitfalls |
|---|---|---|---|---|---|
| **Database auto-increment** | 64-bit | Yes | Single primary | Limited by that primary | Single point of failure; reveals volume; multi-primary needs offset/step tricks (`id = k × N + node`) and merging shards is painful |
| **Ticket server** (central counter, range leasing) | 64-bit | Roughly | One service, but only once per range | Very high if each app server leases 1,000 IDs at a time | A crash wastes the rest of a range (gaps are fine); the ticket server must be replicated |
| **UUIDv4** | 128-bit | No | None | Unlimited | Random inserts scatter across the whole index (page splits, poor cache hit rate); 36-character text form |
| **UUIDv7** (RFC 9562, 2024) | 128-bit | Yes, to the millisecond | None | Unlimited | Reveals creation time; still 128 bits |
| **Snowflake-style** | 64-bit | Yes (k-sorted across workers) | A unique worker ID per process | 4,096 per ms per worker | Clock moving backwards; worker-ID assignment; 41-bit timestamp lasts about 69 years from the custom epoch |
| **Content hash** | 128–256 bit | No | None | Unlimited | Same content gives the same ID (useful for deduplication, harmful if you want distinct IDs) |

**Snowflake bit layout** (Twitter's original design; many variants change the split):

```text
 63  62                                            22 21              12 11              0
+---+-----------------------------------------------+------------------+-----------------+
| 0 |   41-bit timestamp, ms since a custom epoch    |  10-bit worker   |  12-bit sequence |
+---+-----------------------------------------------+------------------+-----------------+
       2^41 ms ≈ 69.7 years                            1,024 workers      4,096 per ms per worker
```

Per worker, the maximum is 4,096 × 1,000 = **4.1M IDs/s**. IDs from different workers interleave within the same millisecond, so they are sortable by time only to about 1 ms plus clock skew ("k-sorted"). Worker IDs come from configuration, a coordination service lease, or the pod ordinal. Two processes sharing a worker ID will eventually issue duplicates.

**UUIDv7 layout** (RFC 9562): 48-bit Unix timestamp in milliseconds, 4-bit version (`7`), 12 random bits, 2-bit variant (`10`), and 62 random bits. That leaves 74 random bits per millisecond, so collisions are negligible without coordination. Choose UUIDv7 over UUIDv4 for database primary keys. Python 3.14 added `uuid.uuid7()`. The code below builds the layout by hand so it runs on older versions too.

**Base62 encoding** turns an integer into a short URL-safe string using `0-9A-Za-z`. Code length versus capacity: 62⁶ ≈ 56.8 billion, 62⁷ ≈ 3.52 trillion, 62⁸ ≈ 218 trillion. A 63-bit Snowflake ID needs up to 11 characters, which is why URL shorteners usually encode a smaller counter or a random value instead. **Sequential counters encoded in base62 are enumerable** (`abc123`, `abc124`, ...). If that matters, pass the counter through a keyed bijection (for example a small Feistel network over the ID space) before encoding, or use random codes with a uniqueness check. For random codes, the chance that a new code collides equals the fraction of the space already used. By the birthday bound, the first collision is expected after about √(π/2 × 62⁷) ≈ 2.4M codes, so an insert-with-unique-constraint plus retry is mandatory. See [Birthday Bound for Hash Collisions](Math_Probability_Estimation.md#72-birthday-bound-for-hash-collisions).

```python
"""ids.py -- base62, a Snowflake-style generator, and UUIDv7 built by hand."""
import os
import threading
import time
import uuid

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def base62_encode(n: int) -> str:
    if n == 0:
        return ALPHABET[0]
    digits = []
    while n:
        n, r = divmod(n, 62)
        digits.append(ALPHABET[r])
    return "".join(reversed(digits))


def base62_decode(s: str) -> int:
    n = 0
    for ch in s:
        n = n * 62 + ALPHABET.index(ch)
    return n


class Snowflake:
    """64-bit IDs: 1 unused sign bit | 41-bit ms timestamp | 10-bit worker | 12-bit sequence."""

    EPOCH_MS = 1_704_067_200_000  # custom epoch 2024-01-01T00:00:00Z extends the 69-year range

    def __init__(self, worker_id: int) -> None:
        if not 0 <= worker_id < 1024:
            raise ValueError("worker_id must fit in 10 bits")
        self.worker_id = worker_id
        self.last_ms = -1
        self.seq = 0
        self.lock = threading.Lock()

    @staticmethod
    def _now_ms() -> int:
        return time.time_ns() // 1_000_000

    def next_id(self) -> int:
        with self.lock:
            now = self._now_ms()
            if now < self.last_ms:                    # wall clock stepped backwards (NTP)
                if self.last_ms - now > 5:
                    raise RuntimeError("clock moved backwards; refusing to issue IDs")
                while now < self.last_ms:             # small step: wait it out
                    now = self._now_ms()
            if now == self.last_ms:
                self.seq = (self.seq + 1) & 0xFFF     # 4,096 IDs per ms per worker
                if self.seq == 0:                     # exhausted: spin to the next ms
                    while now <= self.last_ms:
                        now = self._now_ms()
            else:
                self.seq = 0
            self.last_ms = now
            return ((now - self.EPOCH_MS) << 22) | (self.worker_id << 12) | self.seq

    @classmethod
    def decode(cls, sid: int) -> tuple[int, int, int]:
        return (sid >> 22) + cls.EPOCH_MS, (sid >> 12) & 0x3FF, sid & 0xFFF


def uuid7() -> uuid.UUID:
    """RFC 9562 layout: 48-bit unix ms | ver=7 | 12 random | variant=0b10 | 62 random."""
    ms = time.time_ns() // 1_000_000
    rand = int.from_bytes(os.urandom(10), "big")      # 80 random bits; 74 are used
    value = (ms & ((1 << 48) - 1)) << 80
    value |= 0x7 << 76                                # version
    value |= ((rand >> 62) & 0xFFF) << 64             # rand_a
    value |= 0b10 << 62                               # variant
    value |= rand & ((1 << 62) - 1)                   # rand_b
    return uuid.UUID(int=value)


if __name__ == "__main__":
    gen = Snowflake(worker_id=37)
    ids = [gen.next_id() for _ in range(10_000)]
    assert ids == sorted(ids) and len(set(ids)) == len(ids)
    ts, worker, seq = Snowflake.decode(ids[-1])
    print("snowflake:", ids[-1], "worker:", worker, "base62:", base62_encode(ids[-1]))
    assert base62_decode(base62_encode(ids[-1])) == ids[-1]

    print("62^6 =", f"{62**6:,}", " 62^7 =", f"{62**7:,}")
    print("code for id 125:", base62_encode(125), " for 3.5T-1:", base62_encode(62**7 - 1))

    u = [uuid7() for _ in range(3)]
    print("uuid7:", u[0], "version:", u[0].version, "variant ok:", u[0].variant == uuid.RFC_4122)
    print("uuid4:", uuid.uuid4(), "(random everywhere -> no index locality)")
```

Sample output (IDs depend on the current time):

```text
snowflake: 376083007519481152 worker: 37 base62: RmSmFN0ffU
62^6 = 56,800,235,584  62^7 = 3,521,614,606,208
code for id 125: 21  for 3.5T-1: zzzzzzz
uuid7: 01a1a2c7-f6d6-7efc-9255-9982bcfb8c01 version: 7 variant ok: True
uuid4: 174d8a4f-8eee-498f-998c-9b0c9ce56468 (random everywhere -> no index locality)
```

**Clock pitfalls.** Snowflake trusts the wall clock. If NTP steps the clock back, a naive generator reissues old timestamps and can collide with IDs it already issued. Options: wait out small steps (as above), refuse to issue IDs and fail over on large steps, or keep a "last timestamp" that never decreases and borrow sequence space. Run NTP in slew mode on ID-generating hosts so it adjusts the clock gradually instead of stepping it.

### 4.8 Geospatial Indexing

"Find available drivers within 2 km" cannot use an ordinary index well. A B-tree on latitude returns a band around the whole planet, which must then be filtered by longitude. Spatial indexes map 2D positions to keys that keep nearby points close together.

| Technique | Idea | Strengths | Weaknesses |
|---|---|---|---|
| **Geohash** | Interleave longitude and latitude bits (a Z-order curve) and encode them in base32. A shared prefix means the same cell | Plain strings: works with any ordered key-value store or B-tree via prefix or range scans | Cells are rectangles that distort with latitude; nearby points across a cell edge can share no prefix, so you must also query neighbor cells |
| **Quadtree** | Recursively split a region into 4 quadrants until each holds at most K points | Adapts to density (deep in Manhattan, shallow in a desert); good for in-memory k-nearest-neighbor search | Rebalancing as points move; harder to distribute; mostly an in-memory structure |
| **S2** (Google) | Project the sphere onto the 6 faces of a cube, order each face with a Hilbert curve, use 64-bit cell IDs at levels 0–30 | Better locality than Z-order; a "region coverer" turns a circle or polygon into a few cell-ID ranges to scan | More complex; square-ish cells vary in area |
| **H3** (Uber) | Hexagonal hierarchical grid: 122 base cells, 16 resolutions (0–15) | All 6 neighbors are equidistant, which is ideal for aggregation and smoothing (surge pricing per hexagon, demand heat maps); `grid_disk(k)` gives rings of neighbors | Children do not exactly tile their parent; not a spatial index for arbitrary polygons by itself |
| **R-tree** (PostGIS GiST and similar) | Balanced tree of bounding rectangles | Polygons, spatial joins, "which delivery zone contains this point" | Lives inside a database; heavy update rates of moving points are costly |

**Geohash cell sizes** (at the equator). Each character adds 5 bits, alternating longitude and latitude bits starting with longitude:

| Characters | Bits (lng/lat) | Cell size | Typical use |
|---|---|---|---|
| 4 | 10/10 | 39 km × 20 km | Region or metro shard |
| 5 | 13/12 | 4.9 km × 4.9 km | City-district search |
| 6 | 15/15 | 1.2 km × 0.6 km | Nearby drivers in a city |
| 7 | 18/17 | 153 m × 153 m | Block level |
| 8 | 20/20 | 38 m × 19 m | Building level |

The arithmetic for 5 characters: 25 bits split as 13 longitude and 12 latitude. 360° ÷ 2¹³ = 0.044° of longitude and 180° ÷ 2¹² = 0.044° of latitude. At about 111 km per degree, that is about 4.9 km in each direction.

**Radius search recipe:** pick the precision whose cell is at least as large as the search radius, take the query point's cell and its 8 neighbors, scan those prefixes, then filter candidates by exact (haversine) distance. With 5-character cells for a 2 km radius, the 9 cells cover about 14.7 km × 14.7 km ≈ 216 km², while the circle covers π × 2² ≈ 12.6 km², so you over-fetch about 17×. In dense areas, use finer cells and more of them, which is what S2's region coverer does automatically.

```python
"""geo.py -- geohash encoding, cell size, and the cell-boundary problem."""
import math

BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz"  # geohash alphabet (no a, i, l, o)


def geohash(lat: float, lng: float, precision: int) -> str:
    lat_lo, lat_hi, lng_lo, lng_hi = -90.0, 90.0, -180.0, 180.0
    bits, bit_count, out, even = 0, 0, [], True     # even bit -> longitude
    while len(out) < precision:
        if even:
            mid = (lng_lo + lng_hi) / 2
            bit = lng >= mid
            lng_lo, lng_hi = (mid, lng_hi) if bit else (lng_lo, mid)
        else:
            mid = (lat_lo + lat_hi) / 2
            bit = lat >= mid
            lat_lo, lat_hi = (mid, lat_hi) if bit else (lat_lo, mid)
        bits = (bits << 1) | bit
        even = not even
        bit_count += 1
        if bit_count == 5:                          # 5 bits per base32 character
            out.append(BASE32[bits])
            bits, bit_count = 0, 0
    return "".join(out)


def cell_size_m(precision: int) -> tuple[float, float]:
    """(width, height) in metres at the equator."""
    total = 5 * precision
    lng_bits, lat_bits = (total + 1) // 2, total // 2
    deg_m = 111_320                                  # metres per degree at the equator
    return 360 / 2**lng_bits * deg_m, 180 / 2**lat_bits * deg_m


def haversine_m(a: tuple[float, float], b: tuple[float, float]) -> float:
    (la1, lo1), (la2, lo2) = map(lambda p: (math.radians(p[0]), math.radians(p[1])), (a, b))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6_371_000 * math.asin(math.sqrt(h))


if __name__ == "__main__":
    for p in range(4, 9):
        w, h = cell_size_m(p)
        print(f"precision {p}: {w:9,.0f} m x {h:9,.0f} m")
    sf = (37.7749, -122.4194)
    print("San Francisco:", geohash(*sf, 7))
    a, b = (0.0001, 10.0), (-0.0001, 10.0)            # straddle the equator
    print(f"{haversine_m(a, b):.0f} m apart:", geohash(*a, 7), geohash(*b, 7))
```

```text
precision 4:    39,136 m x    19,568 m
precision 5:     4,892 m x     4,892 m
precision 6:     1,223 m x       611 m
precision 7:       153 m x       153 m
precision 8:        38 m x        19 m
San Francisco: 9q8yyk8
22 m apart: s0p0581 kpzpgxc
```

The last line is the edge problem in its most extreme form: two points 22 m apart on either side of the equator share **no** prefix at all. Prefix search alone is wrong. Always include the neighbor cells.

**Moving objects (ride-sharing, delivery).** Keep `driver -> (cell, position, ts)` and `cell -> set(driver)` in memory. On each 4-second update, overwrite the position, and move the driver between cell sets only when the cell changes, which most updates do not. Expire drivers whose last update is older than about 30 s. Some in-memory stores provide this directly. For example, Redis's GEO commands store a 52-bit geohash as a sorted-set score, and `GEOSEARCH` does a radius query. Shard by region or city (a coarse geohash prefix or S2 cell), and query neighboring shards for searches near a boundary. See [Ride-Sharing Service](#66-ride-sharing-service).

### 4.9 Bloom Filters and Merkle Trees

**Bloom filter:** a bit array of m bits and k hash functions. `add(x)` sets k bits. `contains(x)` returns "definitely not present" if any of those bits is 0, otherwise "probably present". It has **no false negatives**, a tunable false-positive rate, and no deletion. For n items:

```text
false-positive rate  p ≈ (1 − e^(−k·n/m))^k
optimal hash count   k = (m/n) · ln 2
bits needed          m = −n · ln p / (ln 2)²   ≈ 9.6 bits/key at 1%, 14.4 at 0.1%, 19.2 at 0.01%
```

Each additional 4.8 bits per key cuts the false-positive rate by 10×. Worked example: 1 billion keys at 1% need 9.6 Gbit ≈ **1.2 GB**, against about 8 GB for a set of 64-bit fingerprints and much more for the keys themselves.

Derivation and amplification context: [Bloom Filters](CS_Fundamentals.md#bloom-filters).

| Use | Why a Bloom filter fits |
|---|---|
| LSM-tree reads ([6.8](#deep-dive-storage-engine-lsm-tree)) | Skip SSTables that certainly lack the key; a false positive costs one wasted disk read |
| Crawler "URL already seen" ([6.10](#610-web-crawler)) | A false positive skips a new URL, which is acceptable; a false negative is impossible |
| CDN "one-hit wonders" | Cache an object only on its second request, so objects requested once never evict useful ones |
| Cache penetration defense | Reject lookups for IDs that do not exist before they reach the database |
| Joins across machines | Ship a small filter of join keys instead of the keys themselves (a semi-join) |

Variants: a **counting Bloom filter** (small counters instead of bits) supports deletion at about 4× the space. A **cuckoo filter** supports deletion and is more space-efficient below about 3% false positives. **Scalable Bloom filters** add layers as n grows past the size estimate.

**Merkle tree:** a hash tree in which each leaf hashes a data block and each parent hashes its children. Equal roots mean equal data. A difference is found by descending only into subtrees whose hashes differ, so O(d · log n) hashes are exchanged for d differing blocks. An **inclusion proof** that a block belongs to a tree with a known root needs only the log₂ n sibling hashes on the path: for 1 million leaves, that is 20 SHA-256 hashes, or 640 bytes.

| Use | What the tree buys |
|---|---|
| Replica anti-entropy ([6.8](#deep-dive-hinted-handoff-read-repair-and-anti-entropy)) | Compare two replicas' key ranges by exchanging a few hashes, not every key |
| Git, content-addressed storage | Commit and tree objects form a Merkle DAG; identical subtrees are stored once |
| File sync (Dropbox-style), BitTorrent | Verify and transfer only the blocks that changed or are corrupt |
| Certificate Transparency, ledgers | Anyone can verify that an entry is in an append-only log from a small proof |
| ZFS / Btrfs | End-to-end checksums detect silent disk corruption |

```python
"""bloom.py -- a sized Bloom filter and a Merkle inclusion proof."""
import hashlib
import math


class BloomFilter:
    def __init__(self, n_items: int, fp_rate: float) -> None:
        self.m = math.ceil(-n_items * math.log(fp_rate) / math.log(2) ** 2)  # bits
        self.k = max(1, round(self.m / n_items * math.log(2)))              # hash functions
        self.bits = bytearray((self.m + 7) // 8)

    def _positions(self, item: str):
        # Double hashing (Kirsch-Mitzenmacher): g_i = h1 + i*h2 is as good as k independent hashes.
        d = hashlib.blake2b(item.encode(), digest_size=16).digest()
        h1, h2 = int.from_bytes(d[:8], "little"), int.from_bytes(d[8:], "little") | 1
        return ((h1 + i * h2) % self.m for i in range(self.k))

    def add(self, item: str) -> None:
        for p in self._positions(item):
            self.bits[p >> 3] |= 1 << (p & 7)

    def __contains__(self, item: str) -> bool:
        return all(self.bits[p >> 3] & (1 << (p & 7)) for p in self._positions(item))


def h(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def merkle_levels(leaves: list[bytes]) -> list[list[bytes]]:
    level = [h(b"\x00" + x) for x in leaves]          # domain-separate leaves from nodes
    levels = [level]
    while len(level) > 1:
        nxt = [h(b"\x01" + level[i] + level[i + 1]) for i in range(0, len(level) - 1, 2)]
        if len(level) % 2:
            nxt.append(level[-1])                     # promote the odd node; do not duplicate it
        level = nxt
        levels.append(level)
    return levels


def proof(levels: list[list[bytes]], index: int) -> list[tuple[bytes, bool]]:
    path = []
    for level in levels[:-1]:
        sibling = index ^ 1
        if sibling < len(level):                         # a promoted odd node has no sibling
            path.append((level[sibling], sibling < index))   # (hash, sibling_is_left)
        index //= 2
    return path


def verify(leaf: bytes, path: list[tuple[bytes, bool]], root: bytes) -> bool:
    acc = h(b"\x00" + leaf)
    for sib, sib_is_left in path:
        acc = h(b"\x01" + sib + acc) if sib_is_left else h(b"\x01" + acc + sib)
    return acc == root


if __name__ == "__main__":
    n = 100_000
    bf = BloomFilter(n, 0.01)
    for i in range(n):
        bf.add(f"user:{i}")
    assert all(f"user:{i}" in bf for i in range(n))          # never a false negative
    fps = sum(f"other:{i}" in bf for i in range(n))
    print(f"m={bf.m:,} bits ({bf.m / n:.1f} bits/key, {bf.m / 8 / 1024:.0f} KiB), k={bf.k}, "
          f"measured FP rate={fps / n:.2%}")

    blocks = [f"block-{i}".encode() for i in range(1_000)]
    levels = merkle_levels(blocks)
    root = levels[-1][0]
    p = proof(levels, 437)
    print(f"1,000 leaves -> proof of {len(p)} hashes ({len(p) * 32} bytes); "
          f"valid={verify(blocks[437], p, root)}, tampered={verify(b'evil', p, root)}")
```

```text
m=958,506 bits (9.6 bits/key, 117 KiB), k=7, measured FP rate=1.07%
1,000 leaves -> proof of 10 hashes (320 bytes); valid=True, tampered=False
```

The leaf and node prefixes (`0x00`, `0x01`) are **domain separation**. Without them, an attacker can present an internal node's two child hashes as if they were a leaf (a second-preimage attack). Certificate Transparency (RFC 6962) uses the same prefixes.

The code **promotes** an odd node to the next level instead of duplicating it. Bitcoin-style duplication (`level + [level[-1]]`) lets `[a, b, c]` and `[a, b, c, c]` share a root (CVE-2012-2459), which breaks "equal roots mean equal data". RFC 6962 avoids the problem by splitting at the largest power of two below n. If you must keep duplication, also commit to the leaf count.

### 4.10 Probabilistic Counting: HyperLogLog and Count-Min Sketch

Exact answers to "how many distinct users?" or "which hashtags are trending?" need memory proportional to the number of distinct items. Sketches give answers with a bounded, known error using a small fixed amount of memory. They are also **mergeable**, so per-shard or per-minute sketches combine into global or daily ones.

| Question | Exact approach | Sketch | Memory | Error |
|---|---|---|---|---|
| How many distinct X? | Hash set | **HyperLogLog** | 12 KB (16,384 registers × 6 bits) | ~0.81% standard error, whatever the cardinality |
| How often did X occur? Which X are most frequent? | Hash map of counters | **Count-Min Sketch** (+ a top-K heap) | d × w counters (for example 5 × 2,719 ≈ 54 KB) | Overestimates by at most ε·N with probability 1 − δ |
| Is X in the set? | Hash set | **Bloom filter** ([4.9](#49-bloom-filters-and-merkle-trees)) | ~10 bits per item at 1% | False positives only |
| Latency quantiles | All samples | t-digest, DDSketch, HDR histograms | KBs | Relative or rank error bound |

**HyperLogLog (HLL).** Hash each item. In a uniformly random hash, a run of r leading zeros occurs with probability 2^−r, so seeing a long run suggests many distinct items. One observation is very noisy. HLL therefore splits the hash: the first p bits pick one of m = 2^p registers, and each register keeps the longest run seen. The estimate is a bias-corrected harmonic mean over the registers, with standard error **1.04 / √m**. With m = 16,384, that is 0.81%. The **union** of two HLLs is the register-wise maximum, which is exact, so per-day sketches merge into weekly and monthly unique counts. **Intersections are not supported directly**: inclusion-exclusion (|A| + |B| − |A ∪ B|) subtracts large noisy numbers, and the error explodes when the overlap is small.

Why it matters: counting daily unique visitors for each of 10M pages with exact sets of 64-bit IDs could take terabytes. With HLL it is 10M × 12 KB = 120 GB, and much less in practice, because implementations use a sparse encoding for small cardinalities (most pages have few visitors).

**Count-Min Sketch (CMS).** d rows of w counters, with one hash function per row. `add(x)` increments one counter per row. `estimate(x)` returns the minimum over the rows. Collisions only add counts, so the estimate **never underestimates**. With `w = ⌈e/ε⌉` and `d = ⌈ln(1/δ)⌉`, the overestimate is at most ε·N (N is the total count) with probability 1 − δ. Worked example: ε = 0.1% and δ = 1% give w = 2,719 and d = 5, which is 13,595 counters, or about 54 KB at 4 bytes each, regardless of how many distinct items there are.

**Heavy hitters (top-K).** CMS answers "how many times did X occur?" but cannot list items. Pair it with a min-heap of size K. For each arriving item, update the CMS, and if its estimate beats the heap minimum, insert it or update its entry. Alternatives with deterministic guarantees: **Misra-Gries** and **Space-Saving** keep k counters and find every item with frequency above N/k. In a distributed design: each node keeps a CMS plus top-K per time window, a merger sums the CMS matrices (sketches with the same dimensions and hashes add element-wise) and re-ranks the union of the candidates, and an exact batch job can correct the result later if precision matters.

```python
"""sketches.py -- HyperLogLog (distinct counts) and Count-Min Sketch + heap (heavy hitters)."""
import hashlib
import heapq
import math
import random
from collections import Counter


def hash64(item: str, salt: bytes = b"") -> int:
    return int.from_bytes(hashlib.blake2b(item.encode(), digest_size=8, salt=salt).digest(), "big")


class HyperLogLog:
    def __init__(self, p: int = 14) -> None:              # m = 2^14 = 16,384 registers
        self.p, self.m = p, 1 << p
        self.reg = bytearray(self.m)

    def add(self, item: str) -> None:
        x = hash64(item)
        idx = x >> (64 - self.p)                           # first p bits pick a register
        rest = x & ((1 << (64 - self.p)) - 1)              # remaining 50 bits
        rank = (64 - self.p) - rest.bit_length() + 1       # position of the leftmost 1-bit
        self.reg[idx] = max(self.reg[idx], rank)

    def merge(self, other: "HyperLogLog") -> None:         # union = register-wise max
        self.reg = bytearray(map(max, self.reg, other.reg))

    def count(self) -> float:
        alpha = 0.7213 / (1 + 1.079 / self.m)
        est = alpha * self.m ** 2 / sum(2.0 ** -r for r in self.reg)
        zeros = self.reg.count(0)
        if est <= 2.5 * self.m and zeros:                  # small-range correction
            est = self.m * math.log(self.m / zeros)
        return est


class CountMinSketch:
    def __init__(self, eps: float, delta: float) -> None:
        self.w = math.ceil(math.e / eps)                   # error <= eps * N ...
        self.d = math.ceil(math.log(1 / delta))            # ... with probability 1 - delta
        self.rows = [[0] * self.w for _ in range(self.d)]
        self.salts = [i.to_bytes(8, "little") for i in range(self.d)]

    def add(self, item: str, n: int = 1) -> int:
        est = math.inf
        for row, salt in zip(self.rows, self.salts):
            j = hash64(item, salt) % self.w
            row[j] += n
            est = min(est, row[j])
        return est                                         # never underestimates


def top_k(stream, k: int, cms: CountMinSketch) -> list[tuple[int, str]]:
    heap: list[tuple[int, str]] = []                       # min-heap of (estimate, item)
    members: set[str] = set()
    for item in stream:
        est = cms.add(item)
        if item in members:                                # O(k) refresh; fine for small k
            heap = [(est if it == item else c, it) for c, it in heap]
            heapq.heapify(heap)
        elif len(heap) < k:
            heapq.heappush(heap, (est, item))
            members.add(item)
        elif est > heap[0][0]:
            _, evicted = heapq.heapreplace(heap, (est, item))
            members.discard(evicted)
            members.add(item)
    return sorted(heap, reverse=True)


if __name__ == "__main__":
    a, b = HyperLogLog(), HyperLogLog()
    for i in range(600_000):
        a.add(f"user:{i}")
    for i in range(400_000, 1_000_000):                    # overlaps a on 200k users
        b.add(f"user:{i}")
    a.merge(b)
    est = a.count()
    print(f"HLL: true 1,000,000  est {est:,.0f}  error {abs(est - 1e6) / 1e6:.2%}  "
          f"memory {a.m * 6 // 8 // 1024} KiB at 6 bits/register (std err {1.04 / math.sqrt(a.m):.2%})")

    rng = random.Random(7)
    words = [f"#tag{i}" for i in range(50_000)]
    weights = [1 / (i + 1) ** 1.1 for i in range(len(words))]   # Zipf-like popularity
    stream = rng.choices(words, weights, k=200_000)
    cms = CountMinSketch(eps=0.001, delta=0.01)
    print(f"CMS: {cms.d} x {cms.w} counters = {cms.d * cms.w * 4 // 1024} KiB at 4 B/counter")
    exact = Counter(stream).most_common(5)
    approx = top_k(stream, 5, cms)
    for (t, c), (e, item) in zip(exact, approx):
        print(f"  exact {t:9s} {c:6,}   sketch {item:9s} {e:6,}")
```

```text
HLL: true 1,000,000  est 996,610  error 0.34%  memory 12 KiB at 6 bits/register (std err 0.81%)
CMS: 5 x 2719 counters = 53 KiB at 4 B/counter
  exact #tag0     27,837   sketch #tag0     27,842
  exact #tag1     13,119   sketch #tag1     13,129
  exact #tag2      8,311   sketch #tag2      8,315
  exact #tag3      6,062   sketch #tag3      6,069
  exact #tag4      4,710   sketch #tag4      4,717
```

The sketch's counts are slightly **high**, never low, as the theory promises. With a skewed (Zipf-like) stream, the heavy hitters stand far above the collision noise, so the top-K list is correct.

Where these appear in designs: unique visitors and DAU (HLL), trending topics and top-K queries for autocomplete ([6.9](#69-search-autocomplete-typeahead)), hot-key detection ([4.13](#413-cache-stampede-and-hot-keys)), heavy-hitter source IPs for DDoS mitigation, and cardinality estimation in metrics systems ([6.13](#613-metrics-logging-and-monitoring-system)).

### 4.11 Stream Processing

Batch jobs compute over bounded data ("yesterday's clicks"). Stream processors compute continuously over unbounded data ("clicks per ad per minute, updated as they arrive"). The difficult parts are time, state, and failure.

**Event time vs processing time.** Event time is when something happened, stamped by the producer. Processing time is when the processor sees it. Mobile clients buffer events offline, and networks and partitions reorder them, so the two can differ by seconds to days. Aggregate by **event time** whenever correctness matters (billing, ad counts). Processing time is simpler, but results then change if you replay the same data.

**Windows:**

| Window | Definition | Example |
|---|---|---|
| Tumbling | Fixed size, non-overlapping: `[0,60)`, `[60,120)`, ... | Clicks per ad per minute |
| Hopping (sliding) | Fixed size, advancing by a smaller step; windows overlap | 5-minute average updated every minute |
| Session | Per key; closes after a gap of inactivity | User session ends after 30 minutes idle |
| Global + trigger | One window; emit on a count or timer | Running totals |

**Watermarks.** A watermark with value T asserts "no more events with event time < T are expected". A window `[s, e)` fires when the watermark passes e. A common heuristic is `watermark = max event time seen − allowed out-of-orderness` (for example 10 s). Too small, and many events arrive late. Too large, and every result is delayed. Sources that know their ordering (for example, a partitioned log written in order) can produce better watermarks per partition, and the operator takes the minimum across its inputs. One idle partition can therefore stall the watermark, so frameworks mark idle sources.

**Late data** (event time below the watermark) has three policies:

1. **Drop it**, and count the drops as a metric.
2. **Allowed lateness:** keep window state for an extra period. A late event updates the window and the processor emits a **correction**, so the sink must accept upserts (keyed by window and key), not just appends.
3. **Side output:** route very late events to a separate stream, to be reconciled by a batch job.

```python
"""windows.py -- event-time tumbling windows with a watermark, allowed lateness, and late output."""
from collections import defaultdict

WINDOW = 60            # 1-minute tumbling windows, in event-time seconds
MAX_DELAY = 10         # watermark = max event time seen - 10 s (bounded out-of-orderness)
ALLOWED_LATENESS = 60  # keep a fired window's state 60 s longer to absorb stragglers

# (event_time_s, ad_id) in ARRIVAL order: mostly ordered, some late, one very late.
arrivals = [(5, "ad1"), (12, "ad2"), (30, "ad1"), (58, "ad1"), (65, "ad2"), (61, "ad1"),
            (55, "ad2"),   # 55 arrives after 65: out of order, but before the watermark passes 60
            (72, "ad1"), (90, "ad1"),
            (40, "ad1"),   # late: window [0,60) already fired; within allowed lateness -> update
            (130, "ad2"), (185, "ad1"),
            (20, "ad2")]   # very late: past end + allowed lateness -> side output

counts: dict[int, dict[str, int]] = defaultdict(lambda: defaultdict(int))
fired: set[int] = set()
watermark = float("-inf")

for t, ad in arrivals:
    start = t - t % WINDOW
    if watermark >= start + WINDOW + ALLOWED_LATENESS:
        print(f"  late side-output: ({t}, {ad})  window [{start},{start + WINDOW}) state is gone")
        continue
    counts[start][ad] += 1
    if start in fired:                                  # late but allowed: emit a correction
        print(f"  UPDATE window [{start},{start + WINDOW}): {dict(counts[start])}")
    watermark = max(watermark, t - MAX_DELAY)
    for s in sorted(counts):
        if s not in fired and watermark >= s + WINDOW:  # on-time firing
            fired.add(s)
            print(f"wm={watermark:>4}: FIRE window [{s},{s + WINDOW}): {dict(counts[s])}")
        if watermark >= s + WINDOW + ALLOWED_LATENESS:  # garbage-collect state
            del counts[s]
```

```text
wm=  62: FIRE window [0,60): {'ad1': 3, 'ad2': 2}
  UPDATE window [0,60): {'ad1': 4, 'ad2': 2}
wm= 120: FIRE window [60,120): {'ad2': 1, 'ad1': 3}
  late side-output: (20, ad2)  window [0,60) state is gone
```

The out-of-order event at t = 55 was counted on time, because the watermark (55) had not yet passed 60. The event at t = 40 arrived after the window fired, but within allowed lateness, so the window was re-emitted with a correction. The event at t = 20 arrived after the state was garbage-collected, so it went to the side output. (Window `[120,180)` has not fired because the watermark never reached 180. A real job flushes open windows at end of input.)

**State and exactly-once.** Window counts are operator state, partitioned by key across workers. Frameworks such as Flink take periodic consistent snapshots: barriers flow through the dataflow graph, every operator checkpoints its state when the barrier passes, and the snapshot records the source offsets. On failure, the job restores the last snapshot and replays the source from those offsets. That gives **exactly-once state**: each event affects the counts once, even though some events are processed twice physically. **End-to-end exactly-once** also needs the sink to cooperate:

- **Idempotent sink:** upsert keyed by `(window, key)`, so a replay rewrites the same value. This is the simplest and most common option.
- **Transactional sink:** write output inside a transaction committed with the checkpoint (two-phase commit). Kafka transactions do this for read-process-write pipelines, committing consumer offsets and produced records atomically, together with idempotent producers that deduplicate retried sends.
- **Anything else** (sending an email, calling a payment API) is at-least-once. Make the receiver idempotent with an event ID.

**Lambda vs Kappa:**

| | Lambda | Kappa |
|---|---|---|
| Structure | Batch layer (complete, accurate) + speed layer (fast, approximate), merged at query time | One streaming pipeline over a replayable log; reprocess by replaying the log into a new version of the job |
| Strength | Batch recomputation corrects any streaming bug or late data | One codebase, one set of semantics |
| Weakness | Two implementations of the same logic that drift apart | Needs long log retention (or tiered storage) and a stream engine good enough for exact results |
| Fits | Billing-grade numbers where a nightly batch is the source of truth | Most modern pipelines with event-time windows and exactly-once state |

**Worked sizing: ad-click aggregation.** Assume 1B clicks/day, which averages about 11.6k/s, with peaks around 50k/s, aggregated into per-ad, per-minute counts. At about 200 B per event, peak input is 50k × 200 B ≈ 10 MB/s, about one or two log partitions' worth of bandwidth. Use 32–64 partitions anyway, for parallelism and headroom. State: if 1M ads are active per minute and allowed lateness is 1 hour, there are up to 60 open windows per ad. That is 1M × 60 × ~50 B ≈ 3 GB of state, spread across workers. Output: about 1M rows/minute ≈ 17k upserts/s into the serving store, keyed by `(ad_id, minute)`. Late mobile clicks beyond 1 hour go to a side output, and a daily batch job reconciles the billing totals.

### 4.12 Change Data Capture, Event Sourcing, CQRS, and the Outbox

All four answer one question: **how do other systems learn reliably that data changed?** The naive answer is the **dual write**: commit to the database, then publish to a message broker. That is broken. A crash between the two steps loses the event. Publishing first and then failing the commit announces a change that never happened. Retries reorder events.

| Pattern | Source of truth | How changes flow out | Use when |
|---|---|---|---|
| **Transactional outbox** | Normal tables | An outbox row is written in the **same transaction**; a relay publishes it | A service must publish domain events reliably (orders, payments) |
| **Change data capture (CDC)** | Normal tables | A connector reads the database's replication log (PostgreSQL WAL via logical decoding, MySQL binlog) and emits row changes | Feeding caches, search indexes, warehouses; migrating databases; services you cannot modify |
| **Event sourcing** | An append-only log of domain events | The events are the data; projections subscribe to them | Strong audit needs, temporal queries ("balance on March 3"), complex domain workflows |
| **CQRS** | Write model (commands) | Read models are built asynchronously from changes | Read and write shapes differ greatly; many query views of the same data |

**Outbox in SQL:**

```sql
-- fragment: one local transaction updates state and records the event atomically
BEGIN;
UPDATE orders SET status = 'PAID' WHERE order_id = 42 AND status = 'PENDING';
INSERT INTO outbox (event_id, aggregate_type, aggregate_id, event_type, payload, created_at)
VALUES (gen_random_uuid(), 'order', '42', 'OrderPaid',
        '{"order_id": 42, "amount_cents": 1999}', now());
COMMIT;
```

The relay publishes outbox rows in one of two ways:

- **Polling publisher:** `SELECT ... FROM outbox WHERE published_at IS NULL ORDER BY created_at LIMIT 100 FOR UPDATE SKIP LOCKED`, publish, then mark the rows published or delete them. It is simple, but it adds polling load and latency.
- **Log tailing:** a CDC connector reads the outbox table's inserts from the WAL. This has lower latency and adds no query load. Debezium, for example, provides an outbox event router for this pattern.

The relay can crash after publishing and before marking, so delivery is **at-least-once**. Consumers deduplicate by `event_id`, for example with an "inbox" table that has a unique constraint, inserted in the same transaction as the consumer's own update. Use `aggregate_id` as the message key, so all events for one order go to one partition in order.

**CDC vs outbox.** CDC on business tables needs no application changes, but it publishes your **internal schema**. Renaming a column breaks every consumer. The outbox publishes an explicit, versioned event contract. A common combination: the outbox for domain events, and CDC for internal derived stores (search index, cache invalidation, analytics). CDC pitfalls: an initial snapshot is needed before streaming starts, schema changes must propagate, and a slow or stopped connector prevents the database from discarding old WAL, so disk can fill up on the primary. Monitor replication-slot lag.

**Event sourcing.** Store `OrderPlaced`, `ItemAdded`, `OrderPaid`, and so on, never the current row. Current state = fold(events). Appends use **optimistic concurrency on the stream version** (a unique `(stream_id, version)` constraint), so two commands based on the same state cannot both commit. Costs:

- **Rebuild time:** take a **snapshot** every N events (for example 100), so loading needs the snapshot plus at most N events.
- **Schema evolution:** events are immutable and live forever, so readers must understand every past version. Use "upcasters" that convert old versions on read.
- **Deletion and privacy:** you cannot edit history. Use **crypto-shredding**: encrypt personal fields with a per-user key, and delete the key to forget the user.
- **Queries:** the event log is bad at "all orders over $100 this week", so you need projections, which means CQRS.

**CQRS.** Commands validate invariants against the write model. Projections consume changes and maintain read models shaped for each query (a search index, a denormalized document, a counter table). Read models are eventually consistent. For **read-your-writes**, return the write's version or log position to the client, and either have the read path wait until the projection reaches it, or serve that user's next read from the write model.

```python
"""es.py -- event sourcing with optimistic concurrency and a rebuildable CQRS projection."""
from dataclasses import dataclass


class ConcurrencyError(Exception):
    pass


@dataclass(frozen=True)
class Event:
    stream: str
    version: int          # position within the stream (1, 2, 3, ...)
    kind: str
    amount: int


class EventStore:
    def __init__(self) -> None:
        self.log: list[Event] = []                 # global append-only log (the source of truth)
        self.heads: dict[str, int] = {}

    def append(self, stream: str, expected_version: int, kind: str, amount: int) -> Event:
        # In SQL: UNIQUE (stream, version) makes a concurrent append with the same version fail.
        if self.heads.get(stream, 0) != expected_version:
            raise ConcurrencyError(f"{stream}: expected v{expected_version}, "
                                   f"found v{self.heads.get(stream, 0)}")
        ev = Event(stream, expected_version + 1, kind, amount)
        self.log.append(ev)
        self.heads[stream] = ev.version
        return ev

    def load(self, stream: str) -> tuple[int, int]:
        """Rebuild the write model: fold the stream's events into (balance, version)."""
        balance = version = 0
        for ev in self.log:
            if ev.stream == stream:
                balance += ev.amount if ev.kind == "Deposited" else -ev.amount
                version = ev.version
        return balance, version


def withdraw(store: EventStore, account: str, amount: int) -> None:
    balance, version = store.load(account)         # command side enforces the invariant
    if amount > balance:
        raise ValueError("insufficient funds")
    store.append(account, version, "Withdrew", amount)


def project_balances(log: list[Event]) -> dict[str, int]:
    """Read model (CQRS): a denormalized view that can be dropped and rebuilt from the log."""
    view: dict[str, int] = {}
    for ev in log:
        view[ev.stream] = view.get(ev.stream, 0) + (ev.amount if ev.kind == "Deposited" else -ev.amount)
    return view


if __name__ == "__main__":
    store = EventStore()
    store.append("acct-1", 0, "Deposited", 100)
    withdraw(store, "acct-1", 30)

    # Two concurrent withdrawals both read version 2 (balance 70) and each tries to take 60.
    _, v = store.load("acct-1")
    store.append("acct-1", v, "Withdrew", 60)      # first one wins
    try:
        store.append("acct-1", v, "Withdrew", 60)  # second one used a stale version
    except ConcurrencyError as e:
        print("rejected:", e)                      # caller reloads, re-checks, and fails
    print("balance from events:", store.load("acct-1")[0])
    print("projection rebuilt :", project_balances(store.log))
```

```text
rejected: acct-1: expected v2, found v3
balance from events: 10
projection rebuilt : {'acct-1': 10}
```

Without the version check, both withdrawals of 60 from a balance of 70 would have succeeded: a lost update that leaves the balance at −50.

### 4.13 Cache Stampede and Hot Keys

**Cache stampede** (thundering herd, dog-piling): a popular key expires, and every concurrent request misses and recomputes it at once. By Little's law, a key read 10,000 times/s with a 200 ms recompute produces up to 10,000 × 0.2 = **2,000 concurrent identical database queries**, against a database sized for a 99% hit rate. The same thing happens at a **cold start** (empty cache after a deploy or failover) and when many keys written together **expire together**.

| Technique | How it works | Strengths | Weaknesses |
|---|---|---|---|
| **Request coalescing (singleflight)** | Concurrent misses for a key in one process share one in-flight load | Simple, no coordination; N processes means at most N loads | Per process only; does not help across a large fleet by itself |
| **Distributed lock or lease** | The first misser takes `SET lock:key token NX PX 5000`; others wait briefly, retry, or serve stale | One recompute fleet-wide | Lock holder can die (needs a TTL); waiting adds latency. Memcache *leases* (Facebook, NSDI 2013) also prevent stale sets after a concurrent invalidation |
| **Probabilistic early expiration (XFetch)** | Each reader recomputes early with a probability that rises as expiry approaches | No coordination; spreads refreshes before expiry | Still a few redundant recomputes; needs the recompute time (delta) stored with the value |
| **Stale-while-revalidate** | Serve the expired value and refresh it asynchronously | Users never wait on a recompute | Serves stale data for a bounded time; needs a "soft" and a "hard" TTL |
| **TTL jitter** | `ttl = base × uniform(0.9, 1.1)` | Prevents synchronized expiry of keys written together | Does not help a single hot key |
| **Refresh-ahead / pre-warming** | A background job refreshes known-hot keys before they expire, and warms caches before traffic shifts | No miss ever reaches users | Must know which keys are hot; wasted work for keys that cooled down |
| **Negative caching** | Cache "not found" for a short TTL (or use a Bloom filter of existing IDs) | Stops repeated misses for non-existent keys ("cache penetration") | Newly created items appear missing until the negative TTL expires |

A good default stack: coalescing in every process, plus stale-while-revalidate or XFetch for hot keys, plus TTL jitter everywhere. Add a lease when one recompute is very expensive.

```python
"""stampede.py -- request coalescing (singleflight) and probabilistic early expiration (XFetch)."""
import math
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor


class SingleFlight:
    """Concurrent callers for the same key share one in-flight load."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._calls: dict[str, tuple[threading.Event, dict]] = {}

    def do(self, key: str, fn):
        with self._lock:
            call = self._calls.get(key)
            leader = call is None
            if leader:
                call = (threading.Event(), {})
                self._calls[key] = call
        done, result = call
        if leader:
            try:
                result["value"] = fn()
            except Exception as e:                   # followers see the same failure
                result["error"] = e
            finally:
                with self._lock:
                    del self._calls[key]
                done.set()
        else:
            done.wait()
        if "error" in result:
            raise result["error"]
        return result["value"]


db_queries = 0
db_lock = threading.Lock()


def load_from_db() -> str:
    global db_queries
    with db_lock:
        db_queries += 1
    time.sleep(0.2)                                  # slow, expensive query
    return "rendered-homepage"


def xfetch_should_refresh(expiry: float, delta: float, now: float, beta: float = 1.0) -> bool:
    """Vattani et al. (VLDB 2015): refresh early with probability rising toward expiry.
    delta = how long the recompute takes; -log(U) is an Exp(1) sample, so the expected head
    start is beta * delta, and slow recomputes start earlier."""
    return now - delta * beta * math.log(1.0 - random.random()) >= expiry


if __name__ == "__main__":
    sf = SingleFlight()
    with ThreadPoolExecutor(max_workers=200) as pool:
        results = list(pool.map(lambda _: sf.do("home", load_from_db), range(200)))
    print(f"200 concurrent misses -> {db_queries} DB query; all got: {set(results)}")

    random.seed(1)
    expiry, delta = 100.0, 2.0                       # value expires at t=100 s; recompute takes 2 s
    for now in (90.0, 97.0, 99.0, 99.9):
        p = sum(xfetch_should_refresh(expiry, delta, now) for _ in range(100_000)) / 100_000
        print(f"t={now:5.1f}s: P(this request refreshes early) = {p:.3f}")
```

```text
200 concurrent misses -> 1 DB query; all got: {'rendered-homepage'}
t= 90.0s: P(this request refreshes early) = 0.007
t= 97.0s: P(this request refreshes early) = 0.224
t= 99.0s: P(this request refreshes early) = 0.606
t= 99.9s: P(this request refreshes early) = 0.951
```

The XFetch probability is `exp(−(expiry − now) / (β·δ))`. That is about 0.7% at 10 s before expiry when the recompute takes 2 s. At 10,000 reads/s, the first early refresh therefore happens about 20 s before expiry, when the per-request probability is around 5×10⁻⁵ (solve 10,000 reads/s × 2 s × e^(−x/2) = 1). A few readers may trigger refreshes in the same window, so combine XFetch with coalescing.

**Hot keys.** Consistent hashing spreads *keys*, not *load*. One celebrity profile, flash-sale item, or global config key lands on one cache shard (or its N replicas). A shard of a single-threaded in-memory store handles roughly 100k–200k simple ops/s, so a key read 500k times/s cannot be served by one shard no matter how big the cluster is.

- **Detect:** sample requests at clients or proxies and feed a top-K sketch ([4.10](#410-probabilistic-counting-hyperloglog-and-count-min-sketch)); export per-shard ops/s and alert on imbalance.
- **Local (L1) cache in each app server** with a short TTL (1–5 s). With 200 app servers and a 1 s TTL, the shard sees at most about 200 reads/s for that key, whatever the user traffic. The cost is up to 1 s of staleness.
- **Replicate the key:** write it as `key#0 ... key#7` on different shards and read a random copy. Reads scale 8×, but writes must update all copies (or tolerate brief divergence).
- **Split the value:** a huge value (a 5 MB list) is also a bandwidth hot spot. Shard it into pieces, or cache only the first page.
- **Hot writes** (a global like counter): shard the counter into sub-counters and sum them on read, or buffer increments locally and flush every second. See [General admission and hot counters](#deep-dive-general-admission-and-hot-counters) in 6.15.

### 4.14 Interview Questions

**Q1. Design an ID scheme for a globally distributed chat service: IDs must be unique, roughly time-ordered per conversation, and 64-bit.**

Use a Snowflake-style layout: 41 bits of milliseconds since a custom epoch, 10 bits of worker ID, and 12 bits of sequence, giving 4,096 IDs per ms per worker. Assign worker IDs with leases from a coordination service (or region + host ordinal), so no two live processes share one. Global ordering is only approximate (k-sorted, within clock skew), so for **per-conversation** ordering, which users actually see, the conversation's owning partition assigns a monotonically increasing sequence number, and the Snowflake ID serves only as a unique key. Handle clock steps by waiting out small ones and refusing to issue IDs on large ones. If 64 bits were not required, UUIDv7 would remove the worker-ID assignment problem.

**Q2. Why not use UUIDv4 as the primary key in a large B-tree table?**

Random keys insert at random leaf pages, so every insert touches a random page. The working set becomes the whole index rather than its right edge, cache hit rates fall, and page splits leave pages half full. The index also takes more space (16 bytes per key versus 8), and every secondary index carries the primary key. Time-ordered IDs (UUIDv7, Snowflake, or a sequence) append near the right edge. Keep a random ID only where unguessability matters, or store both: an internal sequential key and a random public ID.

**Q3. Find the 10 nearest restaurants to a user. Walk through a geohash-based approach and its edge cases.**

Compute the user's geohash at a precision where a cell is about as large as the expected search radius (6 characters ≈ 1.2 km × 0.6 km in a city). Query that cell and its 8 neighbors with prefix range scans. Compute exact haversine distances and keep the 10 smallest. If fewer than 10 results are found, or the 10th is farther than the distance to the edge of the searched area, widen the search: drop to a coarser precision or add the next ring of cells. Edge cases: points near cell edges (hence the neighbors), longitude wraparound at ±180°, distortion near the poles, and very dense areas where a cell holds thousands of entries (use finer cells or a quadtree there). S2 or H3 handle much of this with region coverers and k-ring queries.

**Q4. You need daily unique visitors per page for 50M pages, and the ability to report weekly uniques. How?**

Keep one HyperLogLog per page per day. Most pages are small, so use a sparse encoding that grows to the dense 12 KB form only for popular pages. Weekly uniques are the register-wise max of the 7 daily sketches. This is exact for the union operation, and the result has the same ~0.81% standard error. Writes go through a stream processor that updates sketches per (page, day). Do not sum daily uniques: a user visiting on two days would be counted twice. Do not try to compute "visited on Monday AND Tuesday" from HLLs, because intersection error is large. If you need intersections, use a different sketch (for example, theta sketches) or exact batch computation.

**Q5. A dashboard shows clicks per ad per minute. Mobile clients send clicks up to 2 hours late. How do you keep counts correct without delaying the dashboard by 2 hours?**

Aggregate in event time. Use a watermark with a small out-of-orderness bound (say 30 s), so each minute's count is emitted about 30 s after the minute ends. That covers almost all clicks, and the dashboard is fresh. Configure allowed lateness of 2 hours: late clicks update their window, and the job emits corrected counts as upserts keyed by `(ad_id, minute)`. Make the serving store an upsert table, not an append log. Clicks later than 2 hours go to a side output, and a nightly batch job reconciles billing totals from the raw log. Window state for 2 hours of lateness is bounded and can be estimated, for example 1M active ads × 120 windows × 50 B ≈ 6 GB across the cluster.

**Q6. The order service writes to its database and then publishes `OrderPlaced` to a message broker. Sometimes downstream services never see the event. Fix it.**

That is the dual-write problem: a crash, timeout, or broker outage between commit and publish loses the event. Write an outbox row in the same transaction as the order, then publish from a relay (polling with `FOR UPDATE SKIP LOCKED`, or CDC tailing of the outbox table). Delivery becomes at-least-once, so consumers deduplicate by `event_id`, and the message key is `order_id` to keep per-order ordering. Monitor outbox age (oldest unpublished row) as the health metric. Do not "fix" it with distributed two-phase commit between the database and the broker. Most brokers do not participate, and it couples their availability.

**Q7. The home page cache entry expires every 60 s, and at each expiry the database CPU spikes to 100%. Explain and fix.**

Every request that arrives during the recompute misses. With 5,000 req/s and a 300 ms recompute, about 1,500 identical queries hit the database at each expiry. Fixes, layered: (1) singleflight in each app server, which cuts the load to one query per server; (2) stale-while-revalidate, with a soft TTL of 60 s and a hard TTL of 10 minutes, so users get the old page while one background refresh runs; or XFetch, so the refresh starts before expiry; (3) a short-lived lock or lease so only one server in the fleet recomputes; (4) TTL jitter for other keys written at the same time. Also check that the cache sits in front of every read path, and that a deploy or cache flush does not cold-start everything at once (warm up gradually).

**Q8. One cache key receives 400k reads/s and the shard holding it is at 100% CPU while the others idle. What do you do now, and what do you do long term?**

Now: enable or shorten an in-process L1 cache for that key on the app servers (TTL of a few seconds). That cuts shard traffic to roughly one request per app server per TTL. If it is configuration-like data, push it to the servers instead of pulling it. Long term: detect hot keys automatically (sampling plus a top-K sketch), replicate detected hot keys under suffixed names across shards with random-replica reads, and split very large values. For hot write keys, shard the counter or batch increments. Rebalancing the cluster does not help: the problem is one key, not an unlucky distribution of keys.

---

## 5. Cross-Cutting Design Decisions

### 5.1 Availability, reliability, and graceful degradation

Availability is the fraction of time a service can successfully serve requests. Redundancy helps only when the system can detect unhealthy components and route around them without overwhelming what remains.

- Use health checks to remove unhealthy instances from traffic.
- Set timeouts for dependency calls; a caller should not wait forever.
- Retry transient failures with backoff and jitter, but avoid retry storms.
- Use circuit breakers or load shedding to protect a failing dependency.
- Decide which features can degrade independently. For example, a feed might show cached content when recommendations are unavailable.
- Define recovery objectives: **RTO** is acceptable recovery time; **RPO** is acceptable data loss measured in time.

Redundancy across zones or regions improves resilience but adds replication and failover complexity. State what failures the design aims to survive.

### 5.2 Consistency and correctness

Consistency is a product decision, not a universal setting. A social feed may tolerate slightly stale counts; a payment must avoid charging twice.

| Technique | Helps with | Does not automatically solve |
|---|---|---|
| Strongly consistent read/write | Reading the latest committed value within a defined scope | Global availability during partitions or multi-system transactions |
| Eventual consistency | High availability and asynchronous replication | User-visible stale reads or conflicting updates |
| Idempotency key | Safe retries of a logical operation | Deduplication forever unless retention and scope are defined |
| Optimistic concurrency/version | Detecting concurrent updates | Choosing how to resolve a conflict |
| At-least-once delivery | Avoiding silent loss of queued work | Duplicate effects at the consumer |

Do not promise “exactly once” as a blanket property. Describe the boundary where deduplication or transactionality is enforced and what happens after that boundary.

### 5.3 Security and privacy

Security is part of the architecture, especially at data and trust boundaries.

- Authenticate callers and authorize each resource operation.
- Encrypt data in transit and protect sensitive data at rest.
- Keep credentials and signing keys out of source code; define rotation and access controls.
- Validate input and apply rate limits to protect expensive endpoints.
- Minimize personal data, define retention, and support deletion where required.
- Audit sensitive actions without logging secrets or full payment credentials.

### 5.4 Observability and operations

Instrument the system so operators can find failures and capacity problems.

- **Metrics:** request rate, error rate, latency percentiles, saturation, queue age, cache hit rate, and replication lag.
- **Logs:** structured events with request or trace identifiers; redact secrets and personal data.
- **Traces:** follow a request across service boundaries and asynchronous work.
- **Alerts:** page on user impact or a leading signal that threatens an objective, not every noisy metric.
- **Capacity and recovery:** monitor storage growth, backup success, restore time, and the ability to drain or replay queues.

Turning these signals into targets and paging rules is covered in [5.6 SLIs, SLOs, SLAs, and Error Budgets](#56-slis-slos-slas-and-error-budgets); rollout-time signals are in [5.9 Deployment Safety](#59-deployment-safety). A worked design of the monitoring system itself is [6.13](#613-metrics-logging-and-monitoring-system).

### 5.5 Common tradeoff pairs

| Choice | Benefits | Costs |
|---|---|---|
| Monolith vs microservices | Simpler deployment and in-process calls vs independent ownership and scaling | Coupling and release coordination vs network failures and operational overhead |
| Synchronous vs asynchronous | Immediate result and simpler flow vs lower coupling and burst absorption | Caller latency and dependency coupling vs delayed completion and retry complexity |
| Normalize vs denormalize | Fewer duplicate facts and simpler updates vs simpler reads at scale | More joins vs more storage and consistency work on updates |
| Push vs pull | Low delivery latency vs fewer background deliveries | Fan-out cost and connection state vs polling load and freshness delay |
| One region vs multiple regions | Simpler consistency and operations vs lower geographic latency and regional resilience | Regional failure exposure vs replication conflicts and failover complexity |

### 5.6 SLIs, SLOs, SLAs, and Error Budgets

These three terms are often confused in interviews. Define them precisely, then show the arithmetic.

Definitions and the nines table also appear in [CS Fundamentals: SLIs, SLOs, SLAs, and Error Budgets](CS_Fundamentals.md#slis-slos-slas-and-error-budgets); this section adds request-based budgets, policy, and composition.

| Term | What it is | Example | Who cares |
|---|---|---|---|
| **SLI** (indicator) | A measured ratio: good events ÷ valid events | Fraction of `GET /feed` requests, measured at the load balancer, that return non-5xx in under 300 ms | Engineers |
| **SLO** (objective) | A target for an SLI over a window | 99.9% of feed requests are good over a rolling 30 days | Engineering and product |
| **SLA** (agreement) | A contract with consequences (credits, refunds) | 99.5% monthly availability or 10% service credit | Customers and legal |
| **Error budget** | `1 − SLO`: the unreliability you are allowed to spend | 0.1% of requests, or 43.2 minutes per 30 days | Release and on-call policy |

Rules of thumb:

- **Measure SLIs as close to the user as you can** (load balancer or client telemetry, not the server's own success counter, which misses requests that never arrived). Define one SLI per critical user journey, not per microservice.
- **The SLA is looser than the SLO**, so you get warned and can react before you owe money. Internal services usually have SLOs but no SLA.
- **Never target 100%.** Users cannot tell 99.999% from 100% through their own unreliable networks and devices, and a 100% target forbids every change.
- **Request-based budgets beat time-based ones** for high-traffic services. At 99.9% and 100M requests per 30 days, the budget is **100,000 failed requests**. A 10-minute total outage at that traffic (about 23k requests) spends 23% of it. A 0.2% error rate that lasts all month spends 200%.

**Error-budget policy.** When the budget is spent, feature launches freeze and the team works on reliability until the rolling window recovers. When plenty of budget is left, the team can take more release risk. This turns "move fast" against "be stable" into a number both sides agreed to in advance.

**Burn-rate alerting.** Burn rate = observed error rate ÷ (1 − SLO). A burn rate of 1 spends exactly the whole budget over the window. Alerting on a raw error-rate threshold either pages on brief blips or misses slow leaks. The multiwindow, multi-burn-rate scheme from the Google SRE Workbook, for a 30-day window:

| Severity | Burn rate | Long window | Short window | Budget spent when it fires |
|---|---|---|---|---|
| Page | 14.4 | 1 h | 5 min | 2% (14.4 × 1 h ÷ 720 h) |
| Page | 6 | 6 h | 30 min | 5% (6 × 6 h ÷ 720 h) |
| Ticket | 1 | 3 days | 6 h | 10% (1 × 72 h ÷ 720 h) |

An alert fires only when **both** windows exceed the burn rate. The long window proves the problem is significant. The short window proves it is still happening, so the alert resets quickly after a fix. Worked example: with a 99.9% SLO and a 1.44% error rate, the burn rate is 1.44% ÷ 0.1% = 14.4, and the whole 30-day budget would be gone in 720 h ÷ 14.4 = **50 hours**.

**Composing SLOs.** A request that needs three serial dependencies, each 99.9% available, is at best 0.999³ ≈ **99.7%** available. You cannot promise 99.95% on top of them without redundancy, caching, or graceful degradation. See the nines table in [Section 3](#availability-nines-and-downtime).

### 5.7 Tail-Latency Amplification

When one user request fans out to N backends in parallel, it waits for the slowest. If each backend exceeds its p99 with probability 0.01, the request is slow with probability `1 − 0.99^N`: about 10% at N = 10 and **63% at N = 100**. With large fan-out, a backend's p99 becomes the user's median. The derivation, the inverse budgeting formula, and the mitigation table (hedged requests, tied requests, micro-partitioning, partial results) are in [Tail Latency and Fan-Out Amplification](Performance_Engineering.md#14-tail-latency-and-fan-out-amplification). Do not average percentiles across hosts; see [Percentiles and Why the Mean Misleads](Performance_Engineering.md#13-percentiles-and-why-the-mean-misleads).

Design-level consequences to state in an interview:

- **Propagate deadlines, not just timeouts.** The edge sets a total budget, for example 300 ms. Each hop passes the remaining budget downstream (gRPC deadlines do this), and a service drops work whose deadline has already passed instead of finishing a response no one will read.
- **Retries multiply across layers.** If three layers each make up to 3 attempts, one user request can become 3³ = **27** calls on the bottom service, exactly when it is already struggling. Retry at one layer only (usually the closest to the failure), and cap retries with a **retry budget** (for example, retries at most 10% of requests per client).
- **Set timeouts from the dependency's tail, not its mean.** A timeout just above the dependency's p99.9 cuts off pathological cases without failing healthy slow requests. Hedge after the p95 instead of waiting for the timeout.
- **Reduce fan-out where you can:** batch per-item calls into one multi-get, cache, or precompute (the news feed's hydration step in [6.3](#63-news-feed) is the classic offender).

The same math applies to bulk-synchronous GPU work: an all-reduce across 512 GPUs finishes at the speed of the slowest rank, so a single straggler sets the step time.

### 5.8 Backpressure and Load Shedding

**Backpressure** means a slow consumer slows its producers, instead of letting work pile up in unbounded buffers until memory runs out or every queued request has already timed out. **Load shedding** means rejecting excess work early and cheaply, so the work you do accept still meets its deadline.

| Mechanism | How it pushes back | Where you see it |
|---|---|---|
| Bounded queue, blocking put | The producer waits for space | In-process pipelines, thread pools with bounded work queues |
| Bounded queue, reject when full | Caller gets HTTP 429 or 503 with `Retry-After` | Service ingress, API gateways |
| Credit or window flow control | The receiver grants credits; the sender stops when they run out | TCP receive window, HTTP/2 and gRPC flow-control windows, Reactive Streams `request(n)` |
| Pull-based consumption | Consumers fetch at their own pace; **lag** grows instead of the consumer overloading | Kafka-style logs (alert on consumer lag and lag growth rate) |
| Adaptive concurrency limit | Lower the in-flight limit when latency rises (AIMD, like TCP congestion control) | Service meshes, client libraries |
| Priority shedding | Under overload, drop low-priority traffic first (prefetch, analytics, batch) | Front ends with request criticality tags |
| Queue-age shedding, LIFO under overload | Drop requests that have waited longer than the client will wait; serve newest first | CoDel-style admission, overloaded RPC servers |

**Sizing a queue with Little's law.** If the workers drain 1,000 requests/s and clients time out after 2 s, a request at queue position 2,000 starts just as its client gives up. Any queue longer than about `drain rate × (deadline − service time)` holds only work that will be wasted. So bound the queue near that value, or lower, and reject beyond it. An unbounded queue turns a short overload into a long outage: latency rises for everyone, clients time out and retry, and the queue grows further. See [Little's Law and Queueing](Performance_Engineering.md#4-littles-law-and-queueing).

A runnable illustration. The producer offers 1,000 items/s, and the consumer handles 100 items/s:

```python
"""backpressure.py -- a bounded queue slows the producer to the consumer's pace; a full queue
can instead shed load immediately (reject) rather than queue work that will miss its deadline."""
import asyncio
import time


async def run(mode: str) -> None:
    q: asyncio.Queue[int] = asyncio.Queue(maxsize=10)
    accepted = rejected = 0

    async def consumer() -> None:
        while True:
            await q.get()
            await asyncio.sleep(0.01)              # service rate: 100 items/s
            q.task_done()

    worker = asyncio.create_task(consumer())
    start = time.perf_counter()
    for i in range(300):                           # offered load: 1,000 items/s for 0.3 s
        if mode == "block":
            await q.put(i)                         # backpressure: producer waits for space
            accepted += 1
        else:
            try:
                q.put_nowait(i)                    # load shedding: fail fast (HTTP 429/503)
                accepted += 1
            except asyncio.QueueFull:
                rejected += 1
            await asyncio.sleep(0.001)
    await q.join()
    worker.cancel()
    print(f"{mode:6s}: accepted={accepted:3d} rejected={rejected:3d} "
          f"elapsed={time.perf_counter() - start:.2f}s  max queue=10")


asyncio.run(run("block"))
asyncio.run(run("shed"))
```

```text
block : accepted=300 rejected=  0 elapsed=3.03s  max queue=10
shed  : accepted= 40 rejected=260 elapsed=0.42s  max queue=10
```

With blocking, every item is processed, but the producer is slowed to the consumer's rate (3 s instead of 0.3 s). That is right for a batch pipeline and wrong for an interactive service, where callers wait. With shedding, the 40 accepted items finish quickly and the rest fail fast, so the caller can retry later, degrade, or go elsewhere. Exact counts vary slightly between runs. Either way, memory stays bounded.

**Interview point:** backpressure must reach the **source** of the work. A queue between two services only moves the problem unless the producer ultimately slows down, sheds, or is told to retry later. Pair shedding with client retry budgets and jittered backoff (see [Resilience Patterns](CS_Fundamentals.md#810-resilience-patterns) for circuit breakers and bulkheads), or the rejected work comes straight back as a retry storm.

### 5.9 Deployment Safety

Most production incidents are caused by changes: code, configuration, schema, or infrastructure. A design is only as safe as the way it is rolled out.

| Strategy | How it works | Rollback | Cost and risk |
|---|---|---|---|
| **Rolling update** | Replace instances in batches (for example 10% at a time) behind the load balancer | Roll forward or back in batches; minutes | Old and new versions serve together, so they must be compatible |
| **Blue-green** | Stand up a full new environment (green), switch traffic from blue at the router | Switch back: seconds | 2× capacity during the switch; the switch is all-or-nothing unless combined with weights |
| **Canary** | Send 1% → 5% → 25% → 100% of traffic to the new version, comparing it with the old (baseline) at each step | Route traffic back to baseline | Needs enough traffic per step to detect regressions; needs automated analysis |
| **Feature flag** | Ship code dark; enable behavior per user, tenant, or percentage at runtime | Turn the flag off: seconds, no deploy | Flag debt; untested flag combinations; the flag service becomes a dependency |
| **Shadow (dark) traffic** | Mirror real requests to the new version and discard its responses | Nothing to roll back | Side effects must be disabled; doubles load on dependencies |

**Canary analysis needs statistics.** Compare the canary against a **baseline** started at the same time with the same traffic share, not against the whole fleet (which has warm caches and older pods). Check error rate, p99 latency, saturation, and business metrics. Worked example: at 10k requests/s, a 1% canary for 30 minutes sees 10,000 × 1% × 1,800 s = **180k requests**. If the error rate rises from 0.1% to 0.5%, that is 180 expected errors versus 900, an obvious difference. A service with 1 request/s would see only 18 canary requests in the same period, which is far too few to detect anything. Low-traffic services need longer bake times, synthetic traffic, or staged rollout by cell or region.

**Rules that prevent most rollout incidents:**

- **Version N and N−1 must run side by side.** That covers rolling updates, canaries, and rollbacks. It applies to APIs, message formats, and database schemas.
- **Schema changes use expand and contract:** (1) add the new column or table, nullable; (2) deploy code that writes both old and new; (3) backfill; (4) switch reads to the new field; (5) stop writing the old one; (6) drop it in a later release. Each step is independently deployable and reversible. A single "rename column" migration is not.
- **Configuration is code.** Config pushes cause a large share of outages. Validate them, version them, and roll them out progressively like binaries.
- **Roll out by failure domain:** one cell, then one zone, then one region, then the rest, with bake time between them. Never change every region at once.
- **Keep the previous artifact ready.** Build once and promote the same artifact through environments, so rollback means redeploying a known digest. Roll forward with a fix when that is faster, but never make it the only option. See [CI/CD Pipeline Design](../tools/Containers_and_CI.md#17-cicd-pipeline-design) and [Artifacts, Supply Chain, and Release Automation](../tools/Containers_and_CI.md#22-artifacts-supply-chain-and-release-automation).
- **Kill switches** for expensive or risky features let operators shed them under load without a deploy.

### 5.10 Transactions Applied to Designs

The isolation levels and their definitions are in [Transactions and ACID](CS_Fundamentals.md#35-transactions-and-acid), and cross-service transactions (2PC, sagas) are in [Distributed Transactions](CS_Fundamentals.md#85-distributed-transactions). This subsection shows how to use them when a design says "atomically reserve" or "conditionally update".

**Two anomalies the basic isolation table does not show:**

| Anomaly | What happens | Example | Prevented by |
|---|---|---|---|
| **Lost update** | Two transactions read the same value, both modify it, and the second write overwrites the first | Two clerks read stock = 5, each sells 1, both write 4 | Atomic `UPDATE ... SET x = x - 1`; `SELECT ... FOR UPDATE`; a version check; PostgreSQL REPEATABLE READ (aborts the second writer). MySQL InnoDB REPEATABLE READ does **not** catch read-then-write lost updates done with a plain `SELECT` |
| **Write skew** | Two transactions read an overlapping set of rows, check a rule, and write **different** rows. Each is valid alone, but together they break the rule | Two on-call doctors each see "2 on call" and both go off call, leaving 0. Two users book overlapping times for the same room | True SERIALIZABLE (PostgreSQL's SSI; MySQL SERIALIZABLE); `FOR UPDATE` on every row the rule reads; materialized conflicts; a database constraint |

**Snapshot isolation allows write skew.** Each transaction reads a consistent snapshot, and the two write sets do not overlap, so first-committer-wins never fires. That is why "we use REPEATABLE READ" is not an answer to "can two bookings overlap?"

**Seat booking, pessimistic.** Lock the rows, check, write, commit. The lock is held from the `SELECT` until `COMMIT`:

```sql
-- fragment: PostgreSQL, inside the booking service
BEGIN;
SELECT seat_id, status
  FROM seat
 WHERE event_id = 7 AND seat_id IN ('A1', 'A2')
 ORDER BY seat_id          -- lock rows in a consistent order so two holds cannot deadlock
   FOR UPDATE;             -- other writers (and other FOR UPDATE readers) now wait
-- application verifies both rows are AVAILABLE; otherwise ROLLBACK and return 409
UPDATE seat
   SET status = 'HELD', hold_id = 'h-123', hold_expires_at = now() + interval '10 minutes'
 WHERE event_id = 7 AND seat_id IN ('A1', 'A2');
COMMIT;
```

Variants worth naming: `FOR UPDATE NOWAIT` fails immediately instead of queueing behind another hold, which suits a UI that should just say "taken". `FOR UPDATE SKIP LOCKED` lets "best available" allocation grab *any* free seats without waiting on rows other buyers are holding:

```sql
-- fragment: best-available allocation under contention
SELECT seat_id FROM seat
 WHERE event_id = 7 AND section = '104' AND status = 'AVAILABLE'
 ORDER BY row_no, seat_no
 LIMIT 2
   FOR UPDATE SKIP LOCKED;
```

**Seat booking, optimistic.** Read without locks, then write only if nothing changed:

```sql
-- fragment: optimistic concurrency with a version column
SELECT status, version FROM seat WHERE event_id = 7 AND seat_id = 'A1';   -- AVAILABLE, 41
UPDATE seat
   SET status = 'HELD', hold_id = 'h-123', version = version + 1
 WHERE event_id = 7 AND seat_id = 'A1' AND version = 41;
-- 1 row updated: success. 0 rows: someone else changed it -- re-read, then retry or return 409.
```

| | Pessimistic (`FOR UPDATE`) | Optimistic (version check) |
|---|---|---|
| Best when | Contention is high and the critical section is short | Contention is low, or the read happens long before the write (a user's think time) |
| Under contention | Requests queue on the lock and succeed one at a time | With c concurrent attempts on one row, one succeeds and c − 1 retry: wasted work and retry storms |
| Failure modes | Deadlocks (fix with lock ordering), lock waits that inflate p99, long transactions holding locks | Starvation under heavy contention; you must bound retries |
| Fits | Ticket on-sales, inventory decrement, account transfers | Editing a profile or document, admin config, carts |

For the full ticket-booking walkthrough, including the single-statement conditional update and a runnable SQLite demo, see [Making the hold atomic](#deep-dive-making-the-hold-atomic) in 6.15.

**When the conflicting row does not exist yet (phantoms).** "No two bookings for room 12 may overlap" reads a *range*. `FOR UPDATE` locks only rows that exist, so two transactions inserting new overlapping bookings lock nothing in common. Three fixes:

1. **Let the database enforce it.** PostgreSQL exclusion constraint:

   ```sql
   CREATE EXTENSION IF NOT EXISTS btree_gist;
   CREATE TABLE room_booking (
       room_id int       NOT NULL,
       during  tstzrange NOT NULL,
       EXCLUDE USING gist (room_id WITH =, during WITH &&)   -- no overlapping ranges per room
   );
   ```

2. **Materialize the conflict:** pre-create one row per room per 15-minute slot, then `SELECT ... FOR UPDATE` the slot rows the booking covers. Now there is something to lock.
3. **Run the transaction at SERIALIZABLE** and retry on serialization failure (SQLSTATE `40001`). This is correct for any invariant but adds aborts under contention, so every caller needs a bounded retry loop.

**Payments and transfers.** Debit with a guarded atomic update, `UPDATE account SET balance = balance - :amt WHERE id = :from AND balance >= :amt`, and check that one row changed. If a transaction must lock two accounts, lock them in **ascending account ID order** so two opposite transfers cannot deadlock. Store money movements as append-only double-entry ledger rows, with the balance as a derived or cached value. Make the request idempotent with a unique constraint on `(merchant_id, idempotency_key)` and `INSERT ... ON CONFLICT DO NOTHING`, then return the stored result on conflict (see [6.7](#67-payment-processing)).

### 5.11 Interview Questions

**Q1. Your service has a 99.9% availability SLO over 30 days and serves 50M requests per day. How much error budget do you have, and what should page someone?**

Over 30 days that is 1.5B requests, so the budget is 0.1%, or **1.5M failed requests**. Time-based, it is 43.2 minutes of total outage. Page on multiwindow burn rate: page if the 1-hour and 5-minute error rates both exceed 14.4 × 0.1% = 1.44% (2% of the budget spent in an hour), or if the 6-hour and 30-minute rates both exceed 6 × 0.1% = 0.6%. Open a ticket if the 3-day and 6-hour rates exceed 0.1%. Do not page on a single 5xx spike or on CPU usage. Those are causes, not user-visible symptoms.

**Q2. Every service in a call chain retries 3 times on timeout. What goes wrong during a partial outage?**

Retries multiply: with 4 attempts per layer (1 + 3 retries) across three layers, one user request can produce 4³ = 64 calls on the bottom service, exactly when it is overloaded. That turns a brownout into a full outage (a retry storm), and the system may stay down after the original fault clears, because the retry load alone exceeds capacity (a metastable failure). Fixes: retry at one layer only; use a retry budget (for example, at most 10% extra load); use exponential backoff with jitter; do not retry non-idempotent operations without an idempotency key; propagate deadlines so a lower layer does not retry work the caller has already abandoned; and use circuit breakers so callers fail fast while the dependency recovers.

**Q3. A queue between the API and workers keeps growing during peak hours. Is a bigger queue the fix?**

No. If the arrival rate exceeds the service rate, any finite queue fills, and a bigger one only adds latency. By Little's law, waiting time = queue length ÷ drain rate, so 100k queued items at 1,000/s is 100 s of delay, past most client deadlines. Decide which fix applies: add capacity (autoscale on queue age, not just queue length); make the work cheaper; shed or defer low-priority work; or push back on producers (429 with `Retry-After`, or slower producer polling). Bound the queue at roughly the drain rate times the useful deadline, and alert on the age of the oldest item, which measures what users actually experience.

**Q4. How would you roll out a change that renames a database column used by 40 service instances?**

Never rename in place, because old and new code run side by side during the rollout. Expand: add the new column. Deploy code that writes both columns and still reads the old one. Backfill the new column in batches, throttled to protect production load. Deploy code that reads the new column, behind a feature flag so the switch is instantly reversible. After a bake period, stop writing the old column, and later drop it in a separate release. Every step is backward compatible with the previous version, so any step can be rolled back by redeploying the previous artifact.

**Q5. Two users try to book the last seat at the same moment, and the database runs at REPEATABLE READ (snapshot isolation). Is a "check then insert into bookings" transaction safe?**

Not if the check reads rows that the insert does not update. Both transactions see "seat free" in their snapshots and each inserts its own booking row. The write sets differ, so snapshot isolation commits both. That is write skew, and the seat is double-booked. Safe options: (1) a single conditional `UPDATE seat SET status='HELD' ... WHERE status='AVAILABLE'` with a row-count check, so both writers touch the same row and the second sees 0 rows; (2) `SELECT ... FOR UPDATE` on the seat row before inserting; (3) a unique constraint on `(event_id, seat_id)` in the bookings table, so the second insert fails; (4) SERIALIZABLE isolation with a retry loop. Option (1) or (3) is the usual answer, because the database enforces the rule, not application logic.

**Q6. Canary or blue-green for a stateless API with 50k requests/s? What about a service that processes 20 requests/hour?**

For the high-traffic API, use a **canary** with automated analysis against a same-age baseline. A 1% canary sees 500 requests/s, enough to detect error-rate and latency regressions within minutes, so you can promote in steps (1% → 10% → 50% → 100%) with a small blast radius. Blue-green adds instant cutover and rollback, but it exposes everyone at once and needs double capacity. For a 20 requests/hour service, a canary cannot gather statistically meaningful data, so rely on pre-production integration tests, synthetic transactions, a feature flag for the new behavior, and **blue-green** (or a simple rolling update) with a fast, rehearsed rollback.

---

## 6. Worked System Designs

Each design follows the same outline: requirements, interfaces and data, architecture and flows, then scaling and failure concerns. Treat the numbers as example assumptions, not facts about a particular company.

Every design includes an explicit **capacity estimate** (QPS, storage, bandwidth, connections, and the design decision each number drives). Designs 6.8 through 6.15 also include a **deep dive** into the mechanism interviewers usually probe, and **interview questions** with full answers. The mechanisms that several designs share (ID generation, geo indexing, sketches, stream processing, caching under load, and transactions) are explained once in [Section 4](#4-architecture-building-blocks) and [Section 5](#5-cross-cutting-design-decisions). The estimates use the formulas in [Estimate the Workload](#3-estimate-the-workload); the point is to show how a number changes the architecture, not to be precise.

### 6.1 URL Shortener

#### Requirements and assumptions

- Create a short link for a long URL and redirect when the short link is opened.
- Reads greatly outnumber writes; links may optionally expire or be disabled.
- Redirects should be fast, and the short key must be unique.
- Click analytics can be eventually consistent.

#### Capacity estimate

```text
Assumptions:  1M new links/day, 100 redirects per link (same workload as Section 3),
              10-year retention, peak = 5× average

Writes:       1M ÷ 86,400                                   ≈ 12/s avg   -> ≈ 60/s peak
Reads:        100M redirects/day ÷ 86,400                   ≈ 1,160/s avg -> ≈ 6,000/s peak
Records:      1M/day × 365 × 10 years                       ≈ 3.65B links
Record size:  7 B code + ~100–200 B long URL + owner, timestamps, status ≈ 300 B
              budget ~500 B with index and storage overhead
Storage:      3.65B × 500 B                                 ≈ 1.8 TB -> × 3 replicas ≈ 5.5 TB
Key space:    base62, 7 chars: 62^7                         ≈ 3.5 trillion codes
              3.65B ÷ 3.5T                                  ≈ 0.1% used after 10 years
              (6 chars: 62^6 ≈ 56.8B -> 6.4% used; random codes would retry ~1 in 16 inserts)
Hot cache:    links created in the last month, top 20% by traffic (serves ~80% of reads):
              30M × 20% × 500 B                             ≈ 3 GB -> one cache node's RAM
Egress:       6,000/s × ~500 B redirect response            ≈ 3 MB/s ≈ 24 Mb/s
Analytics:    100M click events/day × ~200 B                ≈ 20 GB/day ≈ 7 TB/year
```

**What the numbers decide:** 60 writes/s and 5.5 TB fit one replicated database, so sharding is a growth plan, not a day-one need. The 3 GB hot set means a single small cache cluster absorbs most of the 6,000 reads/s. **Seven characters** is the right code length: the key space stays more than 99.9% empty, so random codes almost never collide (see [Unique ID generation](#47-unique-id-generation)). The click-analytics stream (7 TB/year) outgrows the link table itself, which is why it gets its own asynchronous pipeline. **Follow-up at 100× scale** (100M links/day): 6k writes/s and 600k reads/s at peak, 550 TB replicated over 10 years, and 365B links would fill 10% of the 7-character space (move to 8 characters or keep random-code retries cheap). Now the store must be sharded (hash of the short code), edge caching becomes essential, and sequential ID allocation should move to range-leased ticket servers or Snowflake-style IDs.

#### Interfaces and data

```text
POST /v1/links                 { long_url, expires_at? } -> { short_code, short_url }
GET  /{short_code}             -> redirect to long_url
GET  /v1/links/{short_code}    -> link metadata (owner-authorized)
```

Store a link record keyed by `short_code`, with the destination, creator, creation time, optional expiry, and status. Record redirect events asynchronously if analytics are required.

#### Architecture and flow

```text
Create: Client -> API -> Link Service -> Link Store
Read:   Client -> Edge/Load Balancer -> Redirect Service -> Cache -> Link Store
                                                     \-> Event Queue -> Analytics
```

For creation, validate URL scheme and length, generate a candidate code, and insert it with a uniqueness constraint. If a random code collides, generate another; alternatively allocate IDs and encode them, while managing ID service availability and enumeration concerns. For redirect, check cache, load the record on a miss, verify status and expiry, and return the redirect response. Cache entries should expire no later than the link itself.

#### Scaling and tradeoffs

- Cache popular mappings and serve cacheable redirects at the edge where product and privacy rules allow.
- Partition records by short code or a hash of it; avoid a sequential partition key if it creates a hot range.
- A 301 may be cached aggressively by clients; a 302 or 307 offers more control. Choose based on whether redirects or analytics need to reflect changes.
- Send click events asynchronously so analytics work does not slow the redirect path. Define whether a lost analytics event is acceptable.
- Protect creation endpoints from abuse and malware links; consider an allow/deny policy and safe-link scanning.

**Main interview tradeoff:** simple ID allocation produces compact codes but adds coordination and can reveal volume; random codes avoid central sequencing but need collision handling and enough key space.

### 6.2 Rate Limiter

#### Requirements and assumptions

- Allow at most a configured number of requests per user, API key, IP, or route over a period.
- Reject excess requests with a clear response, commonly HTTP 429.
- Support burst behavior appropriate to the product.
- In a multi-instance service, decisions must account for requests handled by other instances.

#### Capacity estimate

```text
Assumptions:  API platform at 1M requests/s peak through 100 gateway nodes;
              10M distinct limiter keys active per hour; 1 limiter check per request

Checks:       1M/s, each an atomic read-modify-write on the counter store
Shards:       one single-threaded in-memory shard ≈ 100k–200k simple ops/s
              1M/s ÷ (100k/s × 50% target utilization)     ≈ 20 shards (+ a replica each)
Memory:       per key: ~50 B key + 16 B (tokens, last refill) + ~80 B store overhead ≈ 150 B
              10M keys × 150 B                              ≈ 1.5 GB total (~75 MB per shard)
Network:      1M/s × ~150 B (request + reply)               ≈ 150 MB/s ≈ 1.2 Gb/s cluster-wide
Latency:      +1 in-datacenter round trip per request       ≈ 0.2–0.5 ms on every request
Connections:  100 gateways × 20 shards × 8 pooled connections = 16,000 (800 per shard)
Sliding log:  storing every timestamp for a 1,000 req/min key = 1,000 × 8 B = 8 KB per key
              × 10M keys                                    = 80 GB (vs 1.5 GB for counters)
```

**What the numbers decide:** the counter store is sized by **operations per second, not memory**: 1.5 GB fits anywhere, but 1M atomic ops/s needs about 20 shards. To cut that load, a gateway can **lease tokens in batches** (take 100 tokens from the central bucket, spend them locally). Central operations then drop by up to 100× for busy keys, at the cost of slight over-admission if a gateway dies holding tokens. The sliding-log line explains why sliding-window counters are preferred over storing timestamps. Adding 0.2–0.5 ms per request is fine for public APIs, but too much for sub-millisecond internal RPCs, which should use local limiters with approximate global quotas.

#### Interfaces and data

The limiter may be middleware rather than a public product API. A policy can be represented as `(scope, limit, interval, algorithm)`. Return allow/deny plus remaining quota and retry information when those values are available.

The key design is typically a tuple such as `(tenant_id, route_id)`. Avoid using a raw untrusted identifier as a storage key without normalization and abuse controls.

#### Architecture and flow

```text
Client -> API Gateway / Middleware -> Distributed Counter Store
              | allowed                         | denied
              v                                  v
         Application                         HTTP 429
```

For a fixed window, atomically increment a counter and set its expiration on first use. This is simple but can allow a burst around a window boundary. For a token bucket, store token balance and last-refill time; an atomic operation refills up to capacity, then consumes a token if one is available. A sliding-window counter reduces boundary bursts without storing every timestamp.

#### Scaling and failure concerns

- Use an atomic server-side operation so concurrent requests cannot all observe the same remaining quota.
- Partition by limiter key; a very large tenant or public IP can still become hot.
- Cache policy configuration locally with versioning, while keeping counter updates coordinated at the required scope.
- Define fail-open versus fail-closed behavior if the counter store is unavailable. Low-risk public reads may fail open; expensive or security-sensitive operations may fail closed or use a conservative local limit.
- For multi-region enforcement, choose between globally coordinated counters, approximate regional quotas, or a home region per key. Each trades latency, precision, and availability differently.
- Prevent the limiter itself from becoming an attack surface through bounded key cardinality and short-lived state.

**Main interview tradeoff:** stricter global accuracy requires coordination on the request path; local or regional limits are faster and more available but may exceed the nominal global quota.

### 6.3 News Feed

#### Requirements and assumptions

- Users publish posts and read a personalized, paginated feed.
- Reads are much more frequent than writes; feed freshness is near-real-time but may be eventually consistent.
- Users follow other users. Media is stored separately from post metadata.
- Ranking can begin as reverse chronological and later incorporate a ranking service.

#### Capacity estimate

```text
Assumptions:  500M DAU; 10 feed loads per user per day; 0.2 posts per user per day;
              average 200 followers; timeline cache keeps the 500 newest entries; peak = 3× average

Feed reads:   500M × 10 = 5B/day ÷ 86,400                   ≈ 58k/s avg  -> ≈ 175k/s peak
Posts:        500M × 0.2 = 100M/day ÷ 86,400                ≈ 1,160/s avg -> ≈ 3.5k/s peak
Fan-out:      100M posts × 200 followers                     = 20B timeline inserts/day
              20B ÷ 86,400                                  ≈ 230k inserts/s avg -> ≈ 700k/s peak
Celebrity:    one post to 50M followers                      = 50M inserts
              at ~700k inserts/s of total fan-out capacity  ≈ 70 s of the whole cluster's work
Timeline RAM: 500M users × 500 entries × 16 B (post_id + score) ≈ 4 TB raw
              × ~2 data-structure overhead × 2 replicas      ≈ 16 TB RAM ≈ 130 nodes at 128 GB
Hydration:    175k feed reads/s × 20 posts per page          = 3.5M post lookups/s (batched multi-get)
Post store:   100M × ~1 KB (text + metadata)                 ≈ 100 GB/day ≈ 36 TB/year (+ replicas)
Media:        10% of posts × 500 KB image                    ≈ 5 TB/day -> object storage + CDN
Feed egress:  175k/s × 20 posts × ~1 KB of JSON              ≈ 3.5 GB/s ≈ 28 Gb/s (media excluded)
```

**What the numbers decide:** fan-out on write multiplies each post by 200, about 700k inserts/s at peak, but turns each of the 175k reads/s into one timeline fetch. The celebrity line shows why pure fan-out on write fails: one post would occupy the entire fan-out tier for over a minute. So accounts above a follower threshold (for example 100k) are **merged at read time** (the hybrid). 16 TB of timeline RAM argues for storing only IDs and only for recently active users. Inactive users get their timeline rebuilt on login. 3.5M post lookups/s must be served almost entirely from a post cache with batched multi-gets, never by the post database, and a viral post is a hot key ([4.13](#413-cache-stampede-and-hot-keys)).

#### Interfaces and data

```text
POST /v1/posts                         { text, media_ids? } -> { post_id }
GET  /v1/feed?cursor=...&limit=...      -> { posts, next_cursor }
POST /v1/users/{id}/follow             { followed_user_id }
```

Core records include users, follow relationships, posts, and feed entries. A feed entry can contain `(user_id, post_id, created_at, score?)`. Store media blobs in object storage and refer to them by ID.

#### Architecture and flow

```text
Publish -> Post Service -> Post Store -> Event Stream
                                  \-> Fan-out Workers -> Feed Store
Read -> Feed Service -> Feed Store -> Post Store / Cache -> Client
                                            \-> Ranking Service (optional)
```

When a user publishes, persist the post and emit a durable event. Workers distribute the post reference to followers' feed timelines. On read, fetch feed entries by user and cursor, hydrate post details, remove deleted or unauthorized content, and return a page.

#### Scaling and tradeoffs

- **Fan-out on write:** fast reads because timelines are precomputed, but expensive for users with many followers.
- **Fan-out on read:** cheap publishing, but every feed read must merge followed users' posts.
- **Hybrid:** precompute ordinary users' feeds and merge posts from high-follower accounts at read time.
- Use cursor pagination based on stable sort fields such as `(created_at, post_id)`; offset pagination becomes costly and unstable at large depth.
- Feed entries are derived data and can be rebuilt from posts and follow edges, but rebuild capacity and freshness need planning.
- Cache the first page for active users if needed; invalidate or update it when new posts arrive.
- Apply privacy and deletion checks during fan-out or hydration so stale feed entries do not expose removed content.

**Main interview tradeoff:** fan-out on write spends storage and write work to reduce read latency; fan-out on read saves precomputation but makes reads more expensive.

### 6.4 Chat System

#### Requirements and assumptions

- Support direct and group text messaging, persistent history, and online delivery.
- A recipient may be offline; messages must be delivered later.
- Ordering is required within a conversation, not necessarily across all conversations.
- Presence and read receipts may be approximate or eventually consistent.

#### Capacity estimate

```text
Assumptions:  200M DAU; 40 messages sent per user per day; 25% of DAU online at peak;
              average 2 recipient devices per message (mostly 1:1, some groups); peak = 3× average

Messages:     200M × 40 = 8B/day ÷ 86,400                  ≈ 93k/s avg  -> ≈ 280k/s peak
Deliveries:   280k/s × 2 recipient devices                  ≈ 560k deliveries/s at peak
Storage:      8B × ~200 B (100 B body + ids, timestamps, metadata) ≈ 1.6 TB/day ≈ 580 TB/year
              × 3 replicas                                  ≈ 1.75 PB/year
Connections:  200M × 25%                                    = 50M concurrent WebSockets
              plan ~250k connections per gateway node (memory, TLS state, and blast radius
              limit you before the kernel does): 10–20 KB/conn × 250k ≈ 2.5–5 GB RAM
              50M ÷ 250k                                    = 200 gateway nodes (+ N+1 per zone)
Heartbeats:   50M connections ÷ 30 s interval                ≈ 1.7M pings/s (more than messages!)
Reconnects:   one gateway dies -> 250k clients reconnect; with jittered backoff over 30 s
              ≈ 8k new TLS connections/s landing on the surviving gateways
Sessions:     50M user/device -> gateway mappings × ~100 B   ≈ 5 GB in a replicated in-memory store
Bandwidth:    560k/s × ~300 B on the wire                    ≈ 170 MB/s ≈ 1.3 Gb/s
```

**What the numbers decide:** the **connection count**, not the message rate, sizes the gateway fleet. Heartbeats outnumber messages, so they terminate at the gateway and never reach backend services. Presence publishes only online/offline transitions, rate-limited, never every ping. The reconnect storm after a gateway failure is a real load spike, so clients use jittered backoff and gateways cap the TLS handshake rate. Storage grows by about 1.75 PB/year, so message history is partitioned by `conversation_id` with time bucketing, and old history moves to cheaper storage. Bandwidth is small.

#### Interfaces and data

```text
WebSocket SEND { conversation_id, client_message_id, body }
GET /v1/conversations/{id}/messages?cursor=... -> message page
POST /v1/conversations/{id}/read               { last_read_message_id }
```

Store conversations, membership, and messages. A message has a conversation-scoped sequence or sortable ID, sender, body or encrypted payload, timestamp, and delivery metadata. Use a client-generated idempotency identifier to make reconnect retries safe.

#### Architecture and flow

```text
Clients <-> WebSocket Gateways -> Chat Service -> Message Store
                                         |             |
                                         |             +-> History reads
                                         v
                                    Delivery Queue -> Recipient Gateway
                                         |
                                         +-> Push Notification Service (offline)
```

The gateway authenticates a connection and maintains a mapping from user/device to gateway. On send, the service checks conversation membership, assigns an ordering position, persists the message, then routes it to active recipient connections. If a recipient is offline, retain the message and trigger a push notification. Clients can fetch history after reconnecting and deduplicate by message ID.

#### Scaling and failure concerns

- Route a conversation to an ordering authority or partition so sequence assignment is consistent within that conversation.
- Partition message history by conversation and time or sequence; account for very large group conversations and uneven activity.
- WebSocket gateways hold connection state. Use heartbeats, reconnect backoff, and resume cursors; do not treat a live socket as durable delivery.
- Persist before acknowledging successful send if message durability is part of the requirement.
- Use at-least-once delivery with client/server deduplication rather than claiming one-time delivery across every network boundary.
- Keep presence ephemeral and approximate; it should not block durable message delivery.
- End-to-end encryption changes search, moderation, backup, and recovery capabilities; clarify whether it is in scope.

**Main interview tradeoff:** stronger ordering and durable delivery require coordination and storage on the send path; optimizing for low latency may allow temporary client-visible reorder or delayed persistence.

### 6.5 Video Streaming Platform

#### Requirements and assumptions

- Creators upload video; viewers browse metadata and stream playback.
- Uploads may be large and interrupted. Playback must adapt to network bandwidth.
- Transcoding and thumbnail generation are asynchronous; original and derived files are durable.
- Popular media must be delivered efficiently across regions.

#### Capacity estimate

```text
Assumptions:  mid-size platform: 50k hours uploaded/day; 100M views/day; 10 min average watch;
              3 Mb/s average delivered bitrate; peak = 2.5× average; CDN hit ratio 95%

Source size:  ~5 Mb/s 1080p source -> 5e6 ÷ 8 B/s × 3,600 s  ≈ 2.25 GB per hour of video
Uploads:      50k h × 2.25 GB                              ≈ 112 TB/day ≈ 1.3 GB/s ingress avg
Renditions:   ABR ladder (1080p ... 240p) ≈ 1.5× source     ≈ 170 TB/day
Storage:      (112 + 170) TB × 365                          ≈ 100 PB/year before replication or EC
Transcode:    assume ~20 vCPU-hours per source hour for the full ladder (software encoder;
              codec, preset, and GPU/ASIC encoders change this by 10× -- measure it)
              50k × 20 = 1M vCPU-h/day ÷ 24 h                ≈ 42k vCPUs busy around the clock
Egress:       100M views × 600 s × 3 Mb/s ÷ 8 bits/B         ≈ 22.5 PB/day
              22.5 PB ÷ 86,400 s                             ≈ 260 GB/s ≈ 2.1 Tb/s avg -> ≈ 5 Tb/s peak
Origin load:  5% CDN misses × 260 GB/s                       ≈ 13 GB/s avg from origin/mid-tier
Concurrency:  Little's law: (100M ÷ 86,400 s) × 600 s        ≈ 700k concurrent streams avg -> 1.7M peak
Segment GETs: 1.7M streams ÷ 4 s segments                    ≈ 430k segment requests/s at peak
Metadata API: 100M views × ~5 calls ÷ 86,400                 ≈ 6k/s avg
```

**What the numbers decide:** egress (terabits per second) dwarfs everything else, so a multi-tier CDN, possibly with caches inside ISP networks, is the design, and the origin is sized for the 5% miss stream. Storage of about 100 PB/year forces **tiering by popularity**: most views go to a small fraction of videos, so cold videos can keep fewer renditions, use erasure coding instead of 3× replication, and have rare renditions transcoded on demand. A transcoding fleet of tens of thousands of vCPUs needs a queue with autoscaling, and splitting each upload into chunks transcoded in parallel shortens time-to-publish. The metadata API (6k/s) is an ordinary web service.

#### Interfaces and data

```text
POST /v1/videos                    { title, visibility } -> { video_id, upload_url }
POST /v1/videos/{id}/complete      { upload_id } -> { status: "processing" }
GET  /v1/videos/{id}               -> metadata and playback manifest URL
```

Store video metadata and processing status in a database. Store original and transcoded segments in object storage. A manifest references multiple bitrate and resolution variants.

#### Architecture and flow

```text
Creator -> Upload Service -> Object Storage -> Upload Complete Event
                                               -> Transcode Queue -> Workers
                                                                  -> Object Storage
Viewer -> API (metadata/manifest) -> CDN -> Video Segments in Object Storage
```

The upload service issues a time-limited upload URL, often for multipart upload directly to object storage. On completion, it emits an event. Workers validate and transcode the source into adaptive-bitrate segments, generate thumbnails, and update processing status. A viewer retrieves metadata and a manifest, then streams segments from a CDN.

#### Scaling and failure concerns

- Direct-to-object-storage upload avoids routing large payloads through application servers.
- Make processing jobs idempotent; retries should not create conflicting outputs or mark incomplete work as ready.
- Use a queue to absorb upload spikes and autoscale workers against queue age and processing cost.
- Keep media metadata separate from blob bytes; replicas and backups of metadata do not replace durable blob storage.
- CDN cache keys and invalidation must account for visibility, version, and geographic restrictions.
- Protect upload URLs with authorization, size/type limits, expiration, and malware/content checks as needed.
- Track processing failures, startup latency, rebuffer rate, CDN hit rate, and storage costs.

**Main interview tradeoff:** aggressive transcoding and replication improve playback quality and reach but increase processing time and storage cost.

### 6.6 Ride-Sharing Service

#### Requirements and assumptions

- Riders request trips; nearby drivers receive offers and can accept one.
- The system tracks frequently changing driver locations and trip state.
- Matching must be quick, while payment, notifications, and receipts can involve asynchronous work.
- Exact location precision and retention are privacy-sensitive.

#### Capacity estimate

```text
Assumptions:  1M drivers online at global peak (~500k average); location update every 4 s;
              20M trips/day; peak = 3× average; average trip 20 min

Location in:  1M ÷ 4 s                                     = 250k updates/s at peak
              × ~100 B (driver_id, lat, lng, heading, speed, ts) ≈ 25 MB/s ingest
Geo index:    1M drivers × ~100 B                           ≈ 100 MB -> fits in one node's RAM
Biggest city: ~50k drivers online ÷ 4 s                      ≈ 12.5k updates/s for one city shard
Trip requests: 20M ÷ 86,400                                 ≈ 230/s avg  -> ≈ 700/s peak
Matching:     each request = 1 nearby search (~9 cells) + rank ~20 candidates with ETA
              700/s × 20                                    = 14k ETA computations/s
Active trips: Little's law: 700/s × 1,200 s                 ≈ 840k concurrent trips at peak
Tracking:     driver position pushed to each rider every 4 s: 840k ÷ 4 ≈ 210k pushes/s
History:      500k avg drivers × 86,400 s ÷ 4 s              ≈ 10.8B points/day × 100 B ≈ 1 TB/day
Connections:  ~1M drivers + ~1M riders with the app open      ≈ 2M persistent connections
              at ~200k per gateway node                      ≈ 10 nodes (+ headroom per region)
```

**What the numbers decide:** the live geo index is tiny (100 MB), so memory is not why you partition. You partition by **city or region** for write throughput, locality, and failure isolation: the largest city's 12.5k updates/s fits one in-memory shard with a replica (indexing options are compared in [4.8 Geospatial Indexing](#48-geospatial-indexing)). Updates **overwrite** the driver's latest position. History (1 TB/day) is written asynchronously to an append-only store, off the hot path. The heaviest steady flow is **trip tracking** (210k pushes/s), about 300× the matching rate, so it gets its own push path over the persistent connections rather than going through the matching service.

#### Interfaces and data

```text
POST /v1/rides                   { pickup, destination } -> { ride_id, status }
POST /v1/drivers/location        { location, timestamp }
POST /v1/rides/{id}/accept       { driver_id, offer_id } -> { status }
GET  /v1/rides/{id}              -> ride status and assigned driver
```

Store durable ride state and payment references in a transactional database. Driver location is high-churn, time-sensitive data, so keep current locations in a geo-indexed in-memory or specialized store with timestamps and TTLs. Historical location retention should follow product and privacy requirements.

#### Architecture and flow

```text
Driver App -> Location Ingest -> Geo Index
Rider App -> Ride Service -> Ride Store -> Matching Service -> Nearby Drivers
                                                 |                  |
                                                 +<- Accept/Claim ---+
Ride Events -> Queue -> Notifications / ETA / Billing / Analytics
```

On request, validate pickup and destination, find nearby available drivers, rank candidates, and send offers. Use an atomic claim or compare-and-set on ride/driver state so two drivers cannot both win the same ride. Publish ride-state changes for notifications and downstream systems.

#### Scaling and failure concerns

- Partition location traffic geographically; account for boundary searches and drivers moving between regions.
- Discard stale location updates and expire inactive drivers from the geo index.
- Limit offer fan-out and use timeouts so a request does not wait forever for a driver.
- Make ride transitions explicit and valid: requested, offered, accepted, in progress, completed, canceled.
- Use idempotent event handling for retries, billing, and notifications.
- Keep location access permissioned, encrypted, retention-limited, and auditable.
- If a matching region fails, decide whether nearby regions can accept the work and what accuracy or latency degrades.

**Main interview tradeoff:** broader search can improve match probability but adds latency and load; tighter geographic partitioning is efficient but needs careful boundary handling.

### 6.7 Payment Processing

#### Requirements and assumptions

- Accept a payment request, contact a payment provider, and report a durable outcome.
- Client and provider retries must not cause duplicate charges.
- Payments have auditable state transitions; reconciliation must detect mismatches.
- Card data handling is minimized by using tokenized provider references where possible.

#### Capacity estimate

```text
Assumptions:  50M payments/day; peak = 10× average (holiday sale); provider p99 latency ≈ 2 s;
              ~10 row writes per payment (payment row, idempotency key, 4–5 state transitions,
              2 double-entry ledger rows, outbox rows); 7-year audit retention

Payments:     50M ÷ 86,400                               ≈ 580/s avg  -> ≈ 6,000/s peak
DB writes:    6,000/s × 10 rows                           = 60,000 row writes/s at peak
              one RDBMS primary ≈ 1k–20k small commits/s (Section 3); plan on ~10k
                                                          -> shard by merchant_id or payment_id
              (4–8 shards with headroom), and write each step's rows in one transaction
In flight:    Little's law: 6,000/s × 2 s provider latency = 12,000 concurrent provider calls
Storage:      ~2.5 KB per payment (1 KB record + transitions + ledger rows + index overhead)
              50M × 2.5 KB                                ≈ 125 GB/day ≈ 45 TB/year
              × 7 years × 3 replicas                      ≈ 1 PB over the retention period
Idempotency:  50M/day × 7-day key window × ~150 B          ≈ 50 GB of unique-indexed keys
Webhooks:     ~2–3 provider events per payment             ≈ 12k–18k/s at peak, each deduplicated
Bandwidth:    6,000/s × ~5 KB across API and provider calls ≈ 30 MB/s (not a constraint)
```

**What the numbers decide:** bandwidth and raw storage are easy. The constraints are **write transactions at peak** and **in-flight provider calls**. 60k row writes/s exceeds one primary, so shard payment state, keeping all rows for one payment (and its ledger entries) on one shard so each transition is a local transaction. 12,000 concurrent provider calls rules out one blocking thread per call; use asynchronous I/O with per-provider connection pools and respect provider rate limits, queueing the excess rather than retrying into them. The 10× peak argues for accepting the request, persisting `PENDING` plus an outbox row, and processing asynchronously. Seven-year retention means an append-only, time-partitioned ledger with hot (about 90 days) and archive tiers.

#### Interfaces and data

```text
POST /v1/payments { order_id, amount, currency, payment_method_token,
                    idempotency_key } -> { payment_id, status }
GET  /v1/payments/{id}                         -> current payment status
POST /v1/provider-webhooks/{provider}           -> acknowledge provider event
```

Store a payment record with a unique idempotency scope, order reference, amount/currency, provider reference, current state, and timestamps. Record state transitions or an immutable ledger entry for financial audit needs. Never store raw card details unless the system is specifically designed and authorized to handle that data.

#### Architecture and flow

```text
Client -> Payment API -> Payment Store + Outbox -> Provider Adapter -> Payment Provider
                                      ^                  ^                    |
                                      |                  +<-- Webhook --------+
                                      +-> Event Queue -> Order Service / Ledger / Receipt
```

Validate and reserve the idempotency key before contacting the provider. Persist a pending payment and an outbox event transactionally if processing continues asynchronously. The provider adapter calls the external provider with a stable idempotency token. Webhooks and polling update the payment state through validated, idempotent transitions. Notify the order service only from a durable state change.

#### Scaling and failure concerns

- A timeout from the provider is ambiguous: the charge may have succeeded even when the response was lost. Query or reconcile using the provider reference; do not blindly issue a new charge.
- Enforce unique idempotency keys and define their tenant/order scope and retention period.
- Verify webhook signatures, deduplicate event IDs, and tolerate events arriving more than once or out of order.
- Use explicit states such as created, pending, authorized, captured, failed, and refunded; disallow invalid transitions.
- Reconcile internal records with provider reports to find missed webhooks or inconsistent outcomes.
- Keep financial audit records durable and access-controlled. Monitor pending duration, failure reasons, duplicate attempts, and reconciliation differences.
- If an order flow spans inventory and payment, model it as a saga with compensating actions rather than assuming a distributed ACID transaction.

**Main interview tradeoff:** synchronous provider confirmation gives a simpler immediate response but increases user latency and couples availability to the provider; asynchronous processing improves resilience but requires pending states and clear user-facing semantics.

### 6.8 Distributed Key-Value Store

This is the classic "design a Dynamo-style store" prompt. Interviewers use it to probe partitioning, replication, consistency, failure detection, and storage-engine internals in a single design.

#### Requirements and assumptions

- `put(key, value)`, `get(key)`, `delete(key)`. Keys up to 256 bytes; values usually about 1 KB, up to 1 MB.
- Horizontal scale to tens of TB, with nodes added or removed without downtime.
- High availability for reads and writes, including during a node or zone failure. Writes should be accepted even when some replicas are unreachable (AP-leaning).
- Tunable consistency per request: fast eventual reads, or quorum reads that see the latest acknowledged write in the common case.
- In-region p99 latency under 10 ms. Range scans, secondary indexes, and multi-key transactions are out of scope.

#### Capacity estimate

```text
Keys:              10 billion
Avg record:        1 KB value + ~100 B key/metadata  ≈ 1.1 KB
Raw data:          10e9 × 1.1 KB                     ≈ 11 TB
Replication N=3:   11 TB × 3                          ≈ 33 TB
LSM space amp:     × ~1.1–1.5 (compaction, tombstones) ≈ 40–50 TB on disk
Node:              4 TB NVMe, keep ≤ 50% full for compaction + rebalancing headroom
Nodes:             ~45 TB ÷ 2 TB usable              ≈ 23  -> provision ~30

Peak traffic:      500k reads/s, 100k writes/s (client operations)
Replica writes:    100k × N=3                          = 300k/s  -> ~10k/s per node
Replica reads:     500k × R=2                          = 1M/s    -> ~33k/s per node
Network:           1.3M replica ops/s × ~1.1 KB         ≈ 1.4 GB/s cluster-wide ≈ 50 MB/s per node
```

**What the numbers decide:** about 10k writes/s per node is comfortable for an append-oriented LSM engine. About 33k reads/s per node needs most hot reads served from memory (memtable plus block cache) and Bloom filters, so most SSTables are skipped rather than read from disk. Per-node network is small, so the cluster is storage-capacity-bound first. That is why disk fill headroom, not CPU, sets the node count.

#### Interfaces and data

```text
PUT    /v1/kv/{key}?w=QUORUM        body=<bytes>, If-Match: <version>?  -> { version }
GET    /v1/kv/{key}?r=ONE|QUORUM    -> { value, version } | { siblings: [...] }
DELETE /v1/kv/{key}?w=QUORUM        -> writes a tombstone, not an immediate erase

Internal (node-to-node):
  replicate(key, value, version), hint(target_node, key, value, version),
  merkle_root(range), merkle_children(range, node_path), stream_range(range)
```

Each stored record is `(key, value | tombstone, version, write_timestamp)`. The version is either a **vector clock** (or dotted version vector), which can detect true concurrent writes and return siblings, or a **hybrid/physical timestamp** for last-writer-wins (LWW). Cluster metadata holds the ring: the token-to-node mapping, node states, and replication factor. It is gossiped between nodes or stored in a small strongly consistent configuration service.

#### Architecture and flow

```text
                       +-------------------- Gossip / membership / failure detector ----------------+
                       |                                                                             |
Client --> (any node acts as) Coordinator --hash(key)--> Ring: preference list [B, C, D]             |
                 |        \                                                                          |
                 |         +--> replica B: WAL -> memtable -> (flush) SSTables + Bloom filters        |
                 |         +--> replica C: same                                                      |
                 |         +--> replica D: unreachable -> write to E with hint "for D" (sloppy quorum)
                 v
        ack after W replies; return to client
Background: read repair (on reads), hinted handoff replay (when D returns),
            Merkle-tree anti-entropy (periodic, per key range), compaction (per node)
```

**Write:** the client (or a smart client library) sends the request to any node. That node becomes the **coordinator**. It hashes the key onto the ring, finds the **preference list** (the first N distinct physical nodes clockwise), and sends the write to all N in parallel. It acknowledges once **W** replicas have durably appended to their write-ahead log (WAL). Remaining replicas still receive the write asynchronously.

**Read:** the coordinator sends the read to N replicas (or R with speculative retries) and waits for **R** responses. It returns the newest version, or siblings if vector clocks show the versions are concurrent. Any stale replica gets **read repair**.

#### Deep dive: partitioning with consistent hashing

With `hash(key) % num_nodes`, changing the node count remaps almost every key. Consistent hashing places nodes and keys on the same hash ring. A key belongs to the first node clockwise from its position, so adding a node moves only about `1/(nodes)` of the keys. **Virtual nodes** (many tokens per physical node) smooth out load and let a new or recovering node stream data from many peers in parallel instead of from one neighbor. Heterogeneous hardware gets proportionally more tokens. See also [Consistent Hashing](CS_Fundamentals.md#58-consistent-hashing).

```python
import bisect
import hashlib


def token(s: str) -> int:
    """64-bit position on the ring (any well-mixed hash works)."""
    return int.from_bytes(hashlib.md5(s.encode()).digest()[:8], "big")


class Ring:
    def __init__(self, vnodes_per_node: int = 128) -> None:
        self.vnodes = vnodes_per_node
        self.tokens: list[int] = []      # sorted ring positions
        self.owner: dict[int, str] = {}  # position -> physical node

    def add(self, node: str) -> None:
        for i in range(self.vnodes):
            t = token(f"{node}#{i}")
            self.owner[t] = node
            bisect.insort(self.tokens, t)

    def preference_list(self, key: str, n: int = 3) -> list[str]:
        """First n DISTINCT physical nodes clockwise from the key's position."""
        start = bisect.bisect_right(self.tokens, token(key))
        replicas: list[str] = []
        for i in range(len(self.tokens)):
            node = self.owner[self.tokens[(start + i) % len(self.tokens)]]
            if node not in replicas:
                replicas.append(node)
                if len(replicas) == n:
                    break
        return replicas


if __name__ == "__main__":
    ring = Ring()
    for name in ["A", "B", "C", "D"]:
        ring.add(name)
    keys = [f"user:{i}" for i in range(100_000)]
    before = {k: ring.preference_list(k, 1)[0] for k in keys}
    ring.add("E")
    after = {k: ring.preference_list(k, 1)[0] for k in keys}
    moved = sum(before[k] != after[k] for k in keys)
    print(f"keys moved after adding E: {moved / len(keys):.1%} (ideal 1/5 = 20%)")
    print("all moved keys went to E:", all(after[k] == "E" for k in keys if before[k] != after[k]))
    print("replicas for user:42:", ring.preference_list("user:42"))
```

Running it prints about 19% moved, all to the new node. With `hash % N`, going from 4 to 5 nodes would move about 80% of keys. In production, also make the preference list **rack- or zone-aware**: skip a node whose failure domain is already represented, so all three replicas cannot sit in one zone.

#### Deep dive: quorums and what they do and do not guarantee

With replication factor **N**, write quorum **W**, and read quorum **R**, the condition **R + W > N** makes every read set intersect every acknowledged write set.

| N, W, R | Overlap? | Tolerates for writes / reads | Typical use |
|---|---|---|---|
| 3, 1, 1 | No (2 ≤ 3) | 2 replicas down / 2 down | Lowest latency, caches, idempotent counters, eventual consistency |
| 3, 2, 2 | Yes (4 > 3) | 1 down / 1 down | Default "quorum" balance |
| 3, 3, 1 | Yes | 0 down / 2 down | Read-heavy, rarely written config |
| 3, 1, 3 | Yes | 2 down / 0 down | Write-heavy, rarely read logs |

Quorum also helps tail latency. With W = 2 of 3, the write waits only for the second-fastest replica, so one slow disk does not set the latency.

Pitfalls interviewers expect you to know:

- **R + W > N is not linearizability.** With a sloppy quorum (below), the W nodes may not be the "home" replicas, so a later read can miss them. A write that fails after reaching only one replica is not rolled back and may surface later. With LWW, concurrent writes resolve by timestamp, so clock skew can silently drop the "later" write. Linearizable operations need consensus (Raft/Paxos per key range) or compare-and-set built on it.
- **Conflict resolution:** with vector clocks, the store returns siblings and the application merges them (for example, a shopping cart takes the union). With LWW there are no siblings, but concurrent updates are lost. CRDT values (counters, sets) merge automatically.

#### Deep dive: hinted handoff, read repair, and anti-entropy

Three repair mechanisms work at three time scales:

| Mechanism | Trigger | Repairs | Limitation |
|---|---|---|---|
| **Hinted handoff** | A write's home replica is down | Writes taken by a stand-in node are replayed to the home node when it returns | Hints are kept for a bounded window (often hours). If the stand-in also dies or the window expires, the hint is lost. |
| **Read repair** | A read sees divergent versions among the R (or N) replicas | Only the keys that are actually read | Cold keys never get repaired |
| **Merkle-tree anti-entropy** | Periodic background job per key range | Everything, including cold keys and expired hints | Costs CPU and I/O; trees must be rebuilt or maintained incrementally |

**Sloppy quorum and hinted handoff:** if replica D in the preference list is down, the coordinator writes to the next healthy node E and tags the write "intended for D". The write still counts toward W. That keeps writes available during failures, at the cost of the overlap guarantee described above. When D recovers, E streams the hinted writes to D and deletes them.

**Merkle trees:** each replica builds a hash tree per key range. Leaves hash buckets of keys, and each parent hashes its children. Two replicas compare roots. If the roots match, the range is identical. If not, they recurse only into the children that differ. Worked example: a range of 1 million keys with 32,768 leaf buckets (about 30 keys per leaf) has a 15-level tree. If one key differs, the replicas exchange about 2 hashes per level, roughly 30 hashes, and then sync about 30 keys. Without the tree they would compare all 1 million keys. The cost is that the tree must be rebuilt (or updated incrementally) as data changes, and a range move invalidates it. That is one reason to align trees with fixed token ranges.

**Deletes and tombstones:** a delete writes a tombstone. If tombstones were purged before every replica saw them, a replica that missed the delete would "resurrect" the value during anti-entropy. So tombstones must outlive the maximum time a replica can be out of sync (the repair interval plus slack), and full repair must run within that window.

#### Deep dive: storage engine (LSM tree)

Each replica uses a **log-structured merge (LSM) tree**, because it turns random writes into sequential I/O.

```text
write -> append to WAL (fsync policy) -> insert into memtable (sorted, e.g., skip list) -> ack
memtable full (e.g., 64–256 MB) -> flush as immutable SSTable: sorted data blocks + sparse index + Bloom filter
read  -> memtable -> immutable memtables -> SSTables newest to oldest (skip a table if its Bloom filter says "absent")
background compaction -> merge SSTables, drop overwritten values and expired tombstones
```

- **Bloom filter sizing:** false-positive rate p ≈ (1 − e^(−k·n/m))^k. With m/n = 10 bits per key and k = 7 hash functions, p ≈ 0.8%. A point read for a missing key then touches disk in less than 1% of SSTables. For 10 billion keys ÷ 30 nodes × 3 replicas = 1 billion keys per node, that costs about 1.25 GB of filter memory per node.
- **Compaction strategy:** *size-tiered* merges similar-sized tables. It has low write amplification but up to about 2× transient space amplification, and more tables to check per read. *Leveled* keeps each level about 10× the previous and non-overlapping. It has low space amplification (about 1.1×) and reads touch about one table per level, but write amplification is much higher (often tens of times). Choose by workload: write-heavy favors tiered, read-heavy or space-constrained favors leveled.

For amplification math and compaction variants (leveled, tiered, TWCS), see [Storage Engine Internals](CS_Fundamentals.md#39-storage-engine-internals).

| | LSM tree | B+ tree |
|---|---|---|
| Writes | Sequential appends; high ingest rate | In-place page updates; random I/O and page splits |
| Point reads | May check several tables (mitigated by Bloom filters, caches) | One root-to-leaf path, about 3–4 page reads |
| Space | Temporary duplicates until compaction | Fragmentation from partly filled pages |
| Write amplification | Compaction rewrites data repeatedly | Whole page rewritten for a small update |
| Latency stability | Compaction can cause p99 spikes; needs throttling | More predictable |
| Fits | Write-heavy KV, time series, logs | Read-heavy OLTP, range-heavy indexes |

#### Scaling and failure concerns

- **Membership and failure detection:** gossip spreads heartbeats and node state. A phi-accrual or timeout-based detector marks peers as suspect. Distinguish *temporary* unavailability (handled by hints) from *permanent* removal (an operator or automation decision that triggers re-replication), so a network blip does not cause a storm of data movement.
- **Adding a node:** it takes ownership of token ranges and streams them from current owners while those owners keep serving traffic. Throttle streaming so it does not hurt foreground p99.
- **Hot keys:** consistent hashing spreads keys, not load. A celebrity key still lands on N nodes. Mitigate with a client-side or proxy cache, read from any replica at R = 1 for that key, or split the key (`key#0..key#7`) and merge on read.
- **Multi-region:** replicate asynchronously across regions, using local quorums for latency. Accept cross-region conflicts (resolved by LWW or CRDTs), or route each key's writes to a home region.
- **Durability knobs:** WAL fsync per write (safest, slowest), group commit every few milliseconds (common), or periodic (fastest, loses the last window on power loss). Replication across zones covers most single-node durability loss.

**Main interview tradeoff:** a leaderless, sloppy-quorum AP design stays writable through failures and has a low tail latency, but offers only eventual consistency plus conflict handling. A leader-per-range design with consensus (CP) gives linearizable reads and writes and simpler semantics, but a range is briefly unavailable during leader election, and every write pays a round trip to a majority.

#### Interview questions

**Q1. If R + W > N, why can a quorum read still return stale data?**

There are several reasons. (1) Under a **sloppy quorum**, the W acknowledgments may come from stand-in nodes outside the preference list, so the R nodes read later need not overlap them. (2) A **failed write** may land on fewer than W replicas. The client sees an error, but the value is not rolled back, so later reads may or may not see it. (3) With **LWW and clock skew**, a write with a lower timestamp is discarded even though it happened later in real time. (4) A read concurrent with a write may see the new value on one replica and the old on another. Without a write-back (read repair before returning), a later read can go back to the old value. That is a non-linearizable "flicker". A strict quorum, read repair before return, and consensus-based writes progressively remove these cases.

**Q2. Walk through what happens when a replica is down for 30 minutes and then for 3 days.**

For 30 minutes, the failure detector marks it suspect, coordinators write to stand-ins with hints, and quorums still succeed with W = 2 of the remaining replicas. When it returns, hinted handoff replays the missed writes, and read repair catches anything else on hot keys. For 3 days, the hint window has expired and hints were dropped. The node is still in the ring, so on return it serves stale data until a full **Merkle-tree repair** syncs each of its ranges. Alternatively, operators declare it dead, its ranges are re-replicated to other nodes from the surviving replicas, and it rejoins empty. The repair must run before the tombstone grace period ends, or deleted data can resurrect.

**Q3. Why choose an LSM tree here instead of a B-tree, and what does it cost on reads?**

The workload is write-heavy and the values are small. An LSM tree turns every write into a WAL append plus a memory insert, and later into sequential flushes and compactions. That sustains much higher ingest than random in-place page writes. The costs are read amplification (a point read may consult several SSTables), space amplification before compaction, and compaction I/O that competes with foreground traffic. Mitigations: Bloom filters (about 1% false positives at 10 bits/key) so most tables are skipped, block and row caches for hot data, leveled compaction when reads dominate, and compaction rate limiting to protect p99.

**Q4. How would you support a conditional write ("set if version = 7")?**

A leaderless store cannot do a safe compare-and-set. Two coordinators can both see version 7 on different quorums and both succeed. Options: route conditional operations for a key range through a **leader elected by consensus** (Raft/Paxos), which serializes them, or run a single-key Paxos round per conditional write (higher latency, but no permanent leader). State that this makes those operations CP: they fail when a majority is unreachable.

**Q5. A single key receives 200k reads/s. What breaks and how do you fix it?**

Its N = 3 replicas each take tens of thousands of extra reads per second, saturating their CPU and network while the rest of the cluster idles. Fixes, from least to most invasive: a cache in the client or a proxy tier with a short TTL; reading at R = 1 spread across all replicas; adding read-only replicas for hot ranges; or splitting the key into sub-keys (`key#i`) and aggregating on read. Writes to a hot counter can be sharded the same way and summed on read.

See also: [CAP Theorem and PACELC](CS_Fundamentals.md#37-cap-theorem-and-pacelc), [Sharding, Replication, and Partitioning](CS_Fundamentals.md#38-sharding-replication-and-partitioning), [Performance Engineering](Performance_Engineering.md) for tail-latency reasoning.

### 6.9 Search Autocomplete (Typeahead)

#### Requirements and assumptions

- As the user types, return the top 10 completions for the current prefix, ranked mostly by popularity, with some freshness boost.
- The experience must feel instant: p99 under about 100 ms end to end, so the server budget is about 10–20 ms.
- Suggestions can lag real query trends by an hour or so. A trending-now boost of minutes is a nice-to-have.
- Offensive, illegal, or private suggestions must be removable quickly, within minutes, without waiting for a rebuild.
- Out of scope initially: spelling correction, per-user personalization, and multiple languages. Mention them as extensions.

#### Capacity estimate

```text
Users:             100M DAU × 10 searches/day           = 1B searches/day
Keystroke calls:   ~6 requests per search after client debounce (~100–150 ms)
Requests:          1B × 6 = 6B/day ÷ 86,400              ≈ 70k QPS avg, ~200k QPS peak (3×)
Cacheable share:   1–2 character prefixes are identical for everyone -> CDN/browser cache absorbs a large share

Serving index:     keep the 10M most popular queries (long tail adds little value)
                   10M × ~20 chars ≤ 200M prefix nodes; prefix sharing -> ~50M nodes
                   ~120 B/node (child links + top-10 list of 4-byte query IDs + overhead) ≈ 6 GB
                   + query strings 10M × 20 B ≈ 200 MB    -> fits in RAM on one server

Serving fleet:     assume ~20k QPS per server (in-memory lookup, RPC-bound)
                   200k ÷ 20k = 10 servers at peak per region, + N+2 spare -> ~12, every server holds a full copy
Query logs:        1B searches × ~100 B ≈ 100 GB/day into the aggregation pipeline
```

**What the numbers decide:** the index is small enough to **replicate in full** rather than shard. Scaling is horizontal for QPS only, which avoids hot shards (prefix "s" is much hotter than prefix "x"). Peak QPS is dominated by short prefixes, so edge caching gives the best return. The log volume is batch-friendly, so a periodic offline build is the simplest correct choice.

#### Interfaces and data

```text
GET /v1/suggest?q=gpu%20pr&limit=10&locale=en-US
    -> { "prefix": "gpu pr", "suggestions": [ { "text": "gpu profiler", "score": 0.93 }, ... ],
         "index_version": "2026-11-03T10" }

Offline data:
  query_log(ts, normalized_query, locale, session_id?)        -- raw events, short retention
  query_stats(query, locale, decayed_count, last_seen)        -- aggregated
  blocklist(pattern, added_at, reason)                         -- applied at build and at serve time
  index snapshot: immutable file in object storage, versioned
```

Normalize queries before counting: lowercase, trim and collapse whitespace, Unicode normalization. Otherwise "GPU  profiler" and "gpu profiler" split their counts.

#### Architecture and flow

```text
                       +-------------------- Online path --------------------+
Browser (debounce, local cache) -> CDN (caches short prefixes, TTL ~minutes) -> LB
                                                                             -> Suggest Service (in-memory trie snapshot)
                                                                                   + serve-time blocklist filter
                       +-------------------- Offline path -------------------+
Suggest/search events -> Log stream -> Aggregator (hourly batch: counts with time decay)
                                        -> Index Builder (filter, rank, build trie with top-K per node)
                                        -> Object storage: snapshot vN
                                        -> Serving nodes download vN, warm, atomically swap pointer
Optional: Trending stream job (counts per 5-minute window) -> small "fresh" index merged at serve time
```

**Read flow:** the client debounces keystrokes and checks its local cache. The CDN answers popular short prefixes. On a miss, a suggest server walks the trie to the prefix node, returns its precomputed top-K list, applies the blocklist, and responds.

**Build flow:** every hour, the aggregator computes `score = Σ count × 0.5^(age_days / 7)` (a one-week half-life). The builder keeps the top 10M queries, builds a new trie, and publishes an immutable versioned snapshot. Servers load it beside the old one and switch over, which is a blue/green swap with instant rollback.

#### Deep dive: trie with precomputed top-K

A plain trie answers "top 10 for prefix p" by walking every completion below p. That is millions of nodes for the prefix "a". Precomputing the top-K list at each node at build time makes a lookup O(len(prefix)), independent of how many completions exist.

```python
import heapq
from dataclasses import dataclass, field

K = 3  # suggestions kept per prefix (10 in production)


@dataclass
class Node:
    children: dict[str, "Node"] = field(default_factory=dict)
    top: list[tuple[int, str]] = field(default_factory=list)  # (score, query), best first


def build(counts: dict[str, int]) -> Node:
    """Offline build: insert every query, then fill each node's top-K bottom-up."""
    root = Node()
    terminal: dict[int, tuple[int, str]] = {}  # id(node) -> (score, query) if a query ends here
    for query, score in counts.items():
        node = root
        for ch in query:
            node = node.children.setdefault(ch, Node())
        terminal[id(node)] = (score, query)

    def fill(node: Node) -> list[tuple[int, str]]:
        candidates = [terminal[id(node)]] if id(node) in terminal else []
        for child in node.children.values():
            candidates.extend(fill(child))  # each child list already holds at most K items
        node.top = heapq.nlargest(K, candidates)
        return node.top

    fill(root)
    return root


def suggest(root: Node, prefix: str) -> list[str]:
    """Serving path: O(len(prefix)) walk, then return the precomputed list."""
    node = root
    for ch in prefix:
        node = node.children.get(ch)
        if node is None:
            return []
    return [q for _, q in node.top]


if __name__ == "__main__":
    counts = {"gpu": 900, "gpu profiler": 400, "gpu memory": 650, "git": 1200,
              "github": 1500, "gpt": 2000, "graph": 300}
    root = build(counts)
    print(suggest(root, "g"))    # ['gpt', 'github', 'git']
    print(suggest(root, "gpu"))  # ['gpu', 'gpu memory', 'gpu profiler']
    print(suggest(root, "x"))    # []
```

The bottom-up build costs O(nodes × K log K), because each node merges at most K candidates per child. Memory is the cost: K entries at every node. Production variants cut it down:

- Store 4-byte query IDs instead of strings.
- Compress single-child chains (a radix trie).
- Precompute lists only for prefixes up to about 15–20 characters, and compute deeper prefixes on the fly because their subtrees are tiny.
- Replace the trie with a **sorted array of queries**: binary search finds the contiguous range of strings that share the prefix, and a range-maximum structure returns the top-K in that range.

#### Scaling and failure concerns

- **Replicate, then shard only if needed.** If personalization, locales, or a larger corpus push the index past one machine's RAM, shard by **prefix range chosen from traffic data** (for example `a–al`, `am–az`), not by first letter. Alternatively, shard by query hash and scatter-gather the top-K from every shard. That costs fan-out on every keystroke.
- **Freshness:** a full hourly rebuild is simple. For breaking trends, a streaming job keeps windowed counts for recently surging queries in a small secondary index, and the server merges the two top-K lists at request time.
- **Fast removal:** the serve-time blocklist is replicated to every server within seconds (a small versioned config). The next build drops the term permanently. Never rely only on the next rebuild for legal or safety removals.
- **Abuse:** bots repeating a query to promote it. Count distinct users or sessions per query per window rather than raw requests, and cap each client's contribution.
- **Failure:** if the suggest service is down, the search box still works without suggestions. Autocomplete should **fail open to "no suggestions"**, never block search. Keep the last N snapshots so a bad build can be rolled back in seconds.
- **Client behavior:** debounce, cancel in-flight requests when a newer keystroke arrives, and ignore responses whose prefix no longer matches the box. Otherwise a slow response for "gp" overwrites the results for "gpu".

**Main interview tradeoff:** precomputing top-K per prefix buys O(prefix) lookups and predictable latency, but costs memory and staleness until the next build. Computing completions at query time saves memory and is always fresh, but is far too slow for short, high-traffic prefixes.

#### Interview questions

**Q1. Why not answer suggestions with `SELECT query FROM stats WHERE query LIKE 'gp%' ORDER BY count DESC LIMIT 10`?**

A B-tree index can find the range of rows with the prefix, but it then has to read every matching row to sort by count. For a 1–2 character prefix that is millions of rows per keystroke, at 200k QPS. The ranking is effectively precomputable because the data changes slowly, so moving the work offline (top-K per prefix) turns each request into a memory lookup. A database is fine as the *source* of aggregated counts, not as the serving path.

**Q2. How would you add personalization without blowing up memory?**

Keep the global index, and blend in a small per-user candidate set at request time. Sources include the user's recent queries (stored client-side or in a per-user key-value record) and possibly cohort-level indexes (locale, interest segment) that are themselves replicated. The server fetches the global top-K plus the user's top matches for the prefix, re-scores them with a simple weighted formula or a light model, and returns 10. Per-user tries for 100M users would be prohibitively large, and most users have little history.

**Q3. How do you support typo tolerance ("gpu porfiler")?**

Exact-prefix tries cannot match typos. Options: (1) fuzzy trie traversal that allows edit distance ≤ 1–2 (branching factor grows quickly, so cap it); (2) generate candidate corrections offline from query logs ("users who typed X then searched Y") and add them as aliases in the index; (3) fall back to a search index with n-gram tokenization when the exact prefix returns few results. In an interview, offer (2) for common typos and (3) as a fallback, and keep the hot path exact.

**Q4. A suggestion needs to be removed for legal reasons right now. How?**

Add it to the serve-time blocklist. That is a small, versioned list pushed to every suggest server and edge filter, applied after the top-K lookup. Request one extra result (K + a few) so filtering does not leave empty slots. The build pipeline also applies the blocklist, so the next snapshot excludes the term permanently. Purge or shorten the CDN TTL for affected prefixes, and audit-log the removal.

**Q5. How would you shard if the index grows to 200 GB?**

Split by prefix ranges sized by **traffic and memory**, using last week's distribution. A routing table maps prefix ranges to shard groups, each replicated for QPS. Every request then touches exactly one shard, because a prefix determines its range. For very hot short prefixes, either serve them from a replicated "head" index on all servers or rely on the edge cache. Avoid hash sharding of queries, because a single keystroke would then have to scatter to all shards.

See also: [Tries](DSA_Fundamentals.md#10-tries-prefix-trees), [Trie pattern problems](LeetCode_Patterns.md#17-trie-prefix-tree), [Caching](CS_Fundamentals.md#53-caching).

### 6.10 Web Crawler

#### Requirements and assumptions

- Start from seed URLs, fetch HTML pages, extract links, and keep discovering. Store raw pages for a downstream indexer.
- Target 1 billion pages per month, plus recrawls of pages that change often.
- **Politeness is a hard requirement:** obey `robots.txt`, keep at most one connection per host at a time, and leave a delay between fetches to the same host.
- Avoid duplicate work. Do not fetch the same URL twice in a cycle, and detect pages whose content duplicates another URL.
- Survive crawler traps (infinite calendars, session IDs in URLs), slow or malicious servers, and crawler node crashes without losing the frontier.
- Out of scope: JavaScript rendering (mention it as an expensive extension), indexing, and ranking.

#### Capacity estimate

```text
Fetch rate:       1B pages/month ÷ (30 × 86,400 s ≈ 2.6M s) ≈ 385 pages/s avg -> design for ~1,000 pages/s
Page size:        ~100 KB raw HTML, ~4–5× smaller compressed
Inbound bandwidth: 1,000 × 100 KB = 100 MB/s ≈ 0.8 Gbit/s
Storage:          1B × 100 KB = 100 TB/month raw ≈ 25 TB/month compressed
                  keep latest version + 12 months history ≈ 300 TB, × 1.5 erasure-coding overhead ≈ 450 TB

In-flight fetches (Little's law, L = λ × W):
                  λ = 1,000 pages/s, W ≈ 1 s average fetch (DNS + connect + download; long tail)
                  L ≈ 1,000 concurrent connections -> async I/O on ~10 nodes, ~100 each
Politeness:       2 s minimum gap per host => ≤ 0.5 pages/s per host
                  => need ≥ 1,000 ÷ 0.5 = 2,000 distinct hosts "ready" at any moment

URL-seen set:     ~10B known URLs
                  exact: 10B × 8-byte fingerprint ≈ 80 GB -> shard over 10 nodes ≈ 8 GB each
                  Bloom: 10B × 10 bits ≈ 12.5 GB at ~1% false positives (1% of new URLs wrongly skipped)
Links discovered: ~50 outlinks/page × 1,000 pages/s = 50k URLs/s into the dedup filter
```

**What the numbers decide:** bandwidth and storage are modest. The real constraints are **politeness** (which forces a wide spread of hosts and per-host queues) and **dedup at 50k URLs/s**, which forces an in-memory, sharded seen-set. Little's law gives the concurrency and therefore the async I/O design. A thread per connection would need about 1,000 threads.

#### Interfaces and data

There is no user-facing API. The interfaces are internal:

```text
frontier.enqueue(url, priority, earliest_fetch_time)       frontier.next_ready() -> url
seen.check_and_add(url_fingerprint) -> bool                 content_seen.check(simhash) -> nearest_dup?
fetch(url, if_modified_since?, etag?) -> (status, headers, body)

url_state(url_fp, url, host, last_fetch, last_status, etag, content_hash, change_rate, next_fetch_at)
host_state(host, robots_rules, robots_fetched_at, crawl_delay, next_allowed_at, error_count)
page_store: object storage, key = (url_fp, fetch_time), value = compressed body + headers
```

#### Architecture and flow

```text
Seeds --> URL Frontier ---------------------------------------------------------------+
           | front queues: by priority (PageRank-ish, freshness need)                  |
           | back queues: one per host, heap keyed by next_allowed_at (politeness)     |
           v                                                                           |
        Fetcher workers (async I/O) --- DNS cache --- robots.txt cache                 |
           |                                                                           |
           +--> Page store (object storage, compressed)                                |
           +--> Parser / link extractor --> URL normalizer --> URL-seen filter --------+
           +--> Content dedup (exact hash + SimHash)        (new URLs only, routed to owning node)
           +--> Event stream "page fetched" --> downstream indexer

Partitioning: crawler node = hash(host) mod nodes (or consistent hashing), so one node owns each host's
              politeness state, robots cache, and back queue.
```

**Fetch loop:**

1. The frontier pops the host whose `next_allowed_at` is earliest and takes that host's next URL.
2. The fetcher resolves DNS from its cache and checks the cached robots rules for the host.
3. It sends a GET with `If-Modified-Since`/`ETag` when recrawling. A 304 reply saves bandwidth.
4. It stores the page, extracts links, normalizes them (lowercase scheme and host, remove fragments, resolve relative paths, strip known tracking parameters), and checks them against the seen-set.
5. New URLs go to the frontier of the node that owns their host, batched to save RPCs.
6. The node sets the host's `next_allowed_at = now + max(crawl_delay, 10 × last_response_time)`, so slow servers automatically get a longer gap.

#### Deep dive: the URL frontier (priority plus politeness)

A single FIFO queue fails twice. It is dominated by whichever host has the most links, which hammers that host, and it ignores importance. The classic two-tier design (Mercator style) separates the concerns:

- **Front queues (prioritization):** F queues by priority class. A selector biases toward high-priority queues but still drains low ones, so nothing starves.
- **Back queues (politeness):** B queues, each holding URLs from **one host only**, with a min-heap keyed by the time each host may next be contacted. A fetch thread pops the heap top, waits until that time if necessary, fetches one URL, then pushes the host back with a new time. A rule of thumb is about 3× more back queues than fetch threads, so threads rarely wait on politeness.
- **Spill to disk:** the frontier can hold billions of URLs, far more than RAM. Keep only the head of each queue in memory, and keep the rest in append-only disk segments or a key-value store.

#### Deep dive: dedup and trap avoidance

| Problem | Technique | Notes |
|---|---|---|
| Same URL seen again | Fingerprint (64-bit hash) of the normalized URL in a sharded set or Bloom filter | A Bloom filter has no false negatives (no refetch), but false positives skip some new URLs. Acceptable for a crawler, not for billing. |
| Same content at a different URL | SHA-256 of the normalized body for exact duplicates | Mirrors, `?ref=` variants, http/https duplicates |
| Nearly the same content | **SimHash**: a 64-bit fingerprint where similar documents differ in few bits; treat Hamming distance ≤ 3 as a duplicate | Boilerplate-heavy pages with different timestamps or ads |
| Crawler traps | Max URL length, max path depth, max URLs per host per cycle, detect repeating path segments, and per-host budgets that are cut when the page-novelty rate drops | Calendars, faceted search, session IDs |
| Spam or link farms | Lower priority for hosts with low-quality signals, per-domain budgets | Protects the crawl budget |

**Recrawl scheduling:** estimate each URL's change rate from history. If the content hash changed since the last fetch, halve the interval. If not, double it, bounded between, say, 1 hour and 30 days. News homepages converge to hourly, and archived pages to monthly. Sitemaps and `Last-Modified` headers give hints for free.

#### Scaling and failure concerns

- **Host-based partitioning** keeps politeness local. No global lock is needed to ensure one connection per host. The tradeoff is skew: a giant host (a large hosting platform) is pinned to one node, so split very large hosts by subdomain or path prefix while keeping a shared rate budget.
- **Crash recovery:** checkpoint frontier segments and the seen-set to durable storage periodically. On a crash, the node's host partitions move to other nodes, which reload the checkpoint. A few URLs may be fetched twice, which is harmless because writes to the page store are keyed by `(url_fp, fetch_time)` and are idempotent.
- **DNS** is often the hidden bottleneck. Run a local caching resolver per node and respect TTLs, but prefetch for queued hosts.
- **Hostile servers:** set connect and read timeouts, a maximum body size (for example 10 MB), a cap on redirect chains, and a limit on content types. Parse in a sandboxed process, because parsers handle untrusted input.
- **Identity and etiquette:** use a clear User-Agent with a contact URL, honor `robots.txt` (cache it for about a day and treat a 5xx on robots as "do not crawl" for a while), and back off when a host returns 429/503.
- **Geography:** crawl from regions near the hosts to cut latency (W in Little's law). That reduces the number of concurrent connections needed.

**Main interview tradeoff:** with a fixed bandwidth and politeness budget, **coverage** (discovering new pages) competes with **freshness** (recrawling known pages). Priority, change-rate estimation, and per-host budgets decide how the budget is split. Stricter politeness protects the web and your reputation but lowers per-host throughput.

#### Interview questions

**Q1. How do you guarantee only one connection per host when 10 crawler nodes run in parallel?**

Make a single node own each host by partitioning on `hash(host)`. That node keeps the host's back queue and `next_allowed_at`, and only one fetch thread at a time is assigned to that queue. URLs discovered on other nodes are forwarded to the owner instead of fetched locally. A global distributed lock per host would add a coordination round trip to every fetch and would fail badly under partitions. When ownership moves (node failure, rebalancing), the new owner starts with a conservative delay.

**Q2. Bloom filter or exact set for URL dedup?**

An exact set of 10B URLs at 8 bytes per fingerprint is about 80 GB, which is fine when sharded across nodes. It also supports deletion and per-URL state. A Bloom filter is about 12.5 GB at 1% false positives with no deletion. A false positive means a new URL is never crawled, and false negatives cannot happen. In practice, use a fingerprint-keyed store, because we need per-URL state anyway (last fetch, ETag, change rate). A Bloom filter can sit in front of it to cheaply reject the many links we have already seen before touching the store.

**Q3. How would you add JavaScript rendering for single-page apps?**

Rendering a page in a headless browser costs about 10–100× the CPU of fetching static HTML and takes seconds. Keep the main pipeline static. Route only pages that signal client-side rendering (a near-empty body, known frameworks, low text-to-script ratio) into a separate **render queue** with its own worker pool and budget. Cache shared static resources (scripts, styles) across pages to cut fetches, and still enforce politeness for every sub-resource request.

**Q4. The crawl rate dropped from 1,000 to 300 pages/s. How do you debug it?**

Use Little's law. Throughput = concurrency ÷ latency, so check whether average fetch latency rose (slow hosts, DNS timeouts) or whether in-flight concurrency fell (fetchers blocked). Then check whether the frontier has too few **ready hosts**: if most queued URLs belong to a few hosts, politeness caps the rate. Also look at the robots fetch error rate, the 429/503 rate (hosts throttling us), parser CPU saturation, and page-store write latency causing backpressure. Per-stage metrics (queue depth, time-in-stage) find the stage that is saturated.

See also: [Performance Engineering](Performance_Engineering.md) (Little's law and throughput analysis), [Hash Tables](DSA_Fundamentals.md#5-hash-tables).

### 6.11 Notification System

#### Requirements and assumptions

- Internal services send notifications to users over **mobile push, email, SMS, and in-app** channels.
- There are two traffic classes. **Transactional** messages (one-time passwords, order shipped, security alerts) are high priority and latency-sensitive, with seconds as the target. **Bulk** campaigns (marketing, digests) reach millions of users and can take minutes to hours.
- Respect user preferences: per-channel opt-in or opt-out, per-category opt-out, quiet hours in the user's time zone, and legal unsubscribe requirements.
- Templates with localization and variables. Per-user frequency caps so users are not spammed.
- Delivery is at-least-once to the provider, with deduplication so a retry does not send a visible duplicate. Track status as sent, delivered, opened, bounced, or failed.
- Third-party providers (push gateways, email relays, SMS aggregators) have their own rate limits, outages, and costs.

#### Capacity estimate

```text
Users:             50M, ~2 devices each for push
Transactional:     100M notifications/day ÷ 86,400 ≈ 1,200/s avg, ~6,000/s peak (5×)
Campaign:          50M recipients within 1 hour ≈ 14,000/s for that hour
Channel fan-out:   ~1.5 sends per notification (multi-device, push + in-app)
                   peak overlap ≈ (6,000 + 14,000) × 1.5 ≈ 30k provider calls/s

Workers (Little's law): provider call ≈ 100 ms; with 200 concurrent calls per worker,
                   one worker ≈ 200 ÷ 0.1 s = 2,000 sends/s -> 30k/s needs ~15 workers + headroom
Notification log:  150M records/day × ~500 B ≈ 75 GB/day; 90-day retention ≈ 7 TB (time-partitioned)
Preferences:       50M × ~1 KB ≈ 50 GB -> fits in a replicated cache; read on every send
Device tokens:     100M × ~200 B ≈ 20 GB
SMS cost check:    1M SMS/day × a few cents ≈ tens of thousands of dollars/day -> SMS only when needed
```

**What the numbers decide:** a 50M-recipient campaign is far bigger than transactional traffic. Without **separate queues per priority**, a campaign would delay one-time passwords by many minutes. That is the core design point. Preferences are read 30k times per second, so they must be cached. SMS cost makes channel selection a business decision, not only a technical one.

#### Interfaces and data

```text
POST /v1/notifications
  { "idempotency_key": "order-123-shipped", "user_id": "u42", "category": "order_update",
    "template_id": "shipped_v3", "params": { "order": "123" }, "priority": "high",
    "channels": ["push", "email"]?, "send_after": "..."? }        -> 202 { "notification_id": "..." }
POST /v1/campaigns { "segment_id": "...", "template_id": "...", "schedule": "...", "rate_limit": 5000 }
GET  /v1/notifications/{id}                                       -> per-channel status
PUT  /v1/users/{id}/preferences  { "email": { "marketing": false }, "quiet_hours": "22:00-07:00" }
POST /v1/provider-callbacks/{provider}                            -> delivery receipts, bounces

notification(id, idempotency_key UNIQUE(producer, key), user_id, category, template_id, params,
             priority, created_at, state)
delivery(id, notification_id, channel, device_or_address, provider, provider_msg_id, attempt, status, ts)
preference(user_id, channel, category, enabled, quiet_hours, timezone, updated_at)
device(user_id, device_id, platform, push_token, last_seen, valid)
template(template_id, version, locale, channel, body)
```

#### Architecture and flow

```text
Producers (order, auth, marketing) --> Notification API (authN, validate, idempotency check) --> Intake queue
                                                                                                    |
Campaign Service --> Segment expansion workers (page through audience in batches) ------------------+
                                                                                                    v
                                     Orchestrator: load prefs (cache) -> filter opt-outs / quiet hours
                                     -> frequency cap -> choose channels -> render template -> enqueue
                                                                                                    |
           +---------------------+---------------------+---------------------+---------------------+
           v                     v                     v                     v
   push.high / push.low   email.high / email.low   sms.high / sms.low     in-app (write to inbox store)
           |                     |                     |
     Push workers           Email workers          SMS workers   -- per-provider rate limiter + circuit breaker
           |                     |                     |
   Push gateways          Email relays          SMS aggregators  --> callbacks --> Status service --> notification log
Retries: exponential backoff with jitter -> after N attempts -> dead-letter queue (+ alert)
```

**Transactional flow (OTP):**

1. Auth calls the API with `idempotency_key = "otp-<session>-<attempt>"`. The API inserts the notification row (a unique constraint enforces idempotency) and enqueues it on the high-priority path.
2. The orchestrator reads preferences. Security categories may bypass marketing opt-outs but never a legal block. It picks SMS, renders the message, and enqueues it on `sms.high`.
3. An SMS worker calls the provider and records `provider_msg_id`. The delivery receipt later updates the status.
4. If the provider times out, the worker retries with the **same** client reference where the provider supports idempotency. If not, it checks status before resending. After N failures, it fails over to a secondary provider.

**Campaign flow:** segment expansion pages through the audience (for example, 10,000 users per batch) and creates notification records with `idempotency_key = campaign_id + user_id`. That makes a restarted expansion safe. Batches go to the `*.low` queues. A per-campaign token bucket limits the overall rate, and email ramps up gradually to protect sender reputation.

#### Scaling and failure concerns

- **Priority isolation:** separate queues and worker pools (or weighted fair consumption) per priority and channel. Monitor **queue age** for the high-priority queues as an SLO, for example p99 under 5 s.
- **Provider limits and outages:** a per-provider token bucket enforces the contracted rate. A circuit breaker opens on error spikes. Multiple providers per channel allow weighted routing and failover. Respect provider backpressure (429) with backoff.
- **Idempotency layers:** (1) the API dedups on `(producer, idempotency_key)`; (2) the orchestrator dedups on `notification_id` when the intake queue redelivers; (3) the worker records `(notification_id, channel, device)` before calling the provider and checks it on retry. A narrow window remains where the provider accepted but we crashed before recording. That is the at-least-once residue, so state it explicitly.
- **Token hygiene:** when a push provider says a token is invalid or unregistered, mark the device invalid immediately. Stale tokens waste capacity and can hurt sender standing.
- **Quiet hours and scheduling:** compute the next allowed send time in the user's time zone and park the message in a delay queue or a scheduled store (see [Distributed Job Scheduler](#612-distributed-job-scheduler)). Transactional security messages are exempt by policy.
- **Hot spots:** a celebrity post that triggers 50M "new post" notifications is a campaign-shaped burst on the transactional path. Route fan-out events through the bulk pipeline.
- **Compliance:** honor unsubscribe within the legally required time, include unsubscribe links, keep an audit trail of consent, and minimize PII in logs. Message bodies may contain sensitive data, so retain them only briefly.

**Main interview tradeoff:** at-least-once delivery with dedup can occasionally send a duplicate, but never silently drops a one-time password. At-most-once avoids duplicates but loses messages on crashes. Choose per category: critical messages retry aggressively (and may fall back to another channel), while marketing messages give up quickly.

#### Interview questions

**Q1. A marketing campaign is delaying password-reset emails. What went wrong and how do you fix it?**

Both shared one queue and one worker pool, so the OTP waited behind millions of campaign messages. That is head-of-line blocking. Fix it with separate queues per priority, ideally per channel, plus reserved worker capacity or weighted fair scheduling for the high class. Add a per-campaign rate limit, and keep provider quotas so bulk traffic cannot consume the whole provider rate limit. Alert on high-priority queue age, not just queue length.

**Q2. How do you prevent duplicate notifications when the queue redelivers a message?**

Use an idempotent pipeline. Producers supply an idempotency key that is unique per `(producer, key)` in the notification table, and the orchestrator and workers check a durable "sent" record keyed by `(notification_id, channel, recipient)` before calling the provider, then update it after. Where the provider supports a client message reference, pass it so the provider dedups too. A tiny window between the provider accepting and our record being written remains, so state that the guarantee is "effectively once" with rare duplicates, not exactly once.

**Q3. How would you support "send at 9 AM local time" for a global campaign?**

Group recipients by time zone (or UTC offset bucket) during segment expansion. Schedule each bucket as a delayed job at 09:00 in that zone, and spread it over a window (for example 09:00–09:30) to smooth load. The scheduler releases each bucket into the low-priority queue at its time. Per-user quiet hours are still checked at send time, because preferences may change between scheduling and sending.

**Q4. The push provider is down for 20 minutes. What happens?**

The circuit breaker opens after errors exceed a threshold, and workers stop calling the provider, which protects our threads and avoids hammering it. Messages stay in `push.*` queues; they are not acknowledged. Queue age grows and alerts fire. For critical categories, the orchestrator may fall back to SMS or email after a deadline. Campaign messages can wait, or expire if they are time-sensitive (a "flash sale ends in 1 hour" message is pointless 2 hours later, so give notifications a TTL). When the breaker half-opens and probes succeed, drain at the provider's rate limit, not as fast as possible.

See also: [LLD: Notification Service](../design-patterns/Low_Level_Design_Interview_Prep.md#12-worked-design-notification-service), [Message Queues](CS_Fundamentals.md#55-message-queues), [Rate Limiter](#62-rate-limiter).

### 6.12 Distributed Job Scheduler

#### Requirements and assumptions

- Tenants register **one-off jobs** ("run at T") and **recurring jobs** (cron expression plus time zone). A job is a payload plus a target, such as a container image or an HTTP endpoint.
- A job should start within a few seconds of its scheduled time under normal load.
- **At-least-once execution** with configurable retries (backoff, maximum attempts), a per-run timeout, and a dead-letter state. Jobs are expected to be idempotent, or to use the provided run ID for deduplication.
- Detect dead workers (heartbeats) and reschedule their runs. A stale worker must not overwrite a newer attempt's result.
- Per-tenant quotas and priorities. Run history is visible for 30 days.
- Optional extensions: DAG dependencies (B runs after A succeeds), a concurrency policy (allow, forbid, or replace overlapping runs), and a misfire policy for runs missed during an outage.

#### Capacity estimate

```text
Registered jobs:   10M recurring, average once per hour; plus ~1M one-off/day
Runs:              10M × 24 ≈ 240M runs/day ÷ 86,400 ≈ 2,800 runs/s average

Top-of-hour burst: humans love "0 * * * *": assume 20% of hourly jobs fire at :00
                   => 2M runs due in the same second
                   at 50k dispatches/s, the last one starts 2M ÷ 50k = 40 s late
Worker slots:      avg job runtime 30 s => concurrent runs = 2,800/s × 30 s ≈ 84k slots (Little's law)
                   the :00 burst alone would want 2M slots for 30 s -> must be smoothed

Job definitions:   10M × ~1 KB ≈ 10 GB -> one replicated relational database is enough
Run history:       240M/day × ~200 B ≈ 48 GB/day; 30 days ≈ 1.4 TB -> partition by day, drop old partitions
```

**What the numbers decide:** average throughput is modest, but the **synchronized burst** dominates. The design must spread start times by adding jitter, allowing a dispatch window ("within 60 s of :00") when the tenant permits it, and pre-loading due runs into a ready queue before their time. Worker capacity follows from Little's law, not from the number of registered jobs.

#### Interfaces and data

```text
POST   /v1/jobs   { "name", "schedule": "*/5 * * * *" | "at": "...", "timezone": "America/Chicago",
                    "target": {...}, "timeout_s": 300, "retry": { "max_attempts": 5, "backoff": "exp" },
                    "concurrency": "forbid", "misfire": "run_once", "jitter_s": 30 }   -> { job_id }
GET    /v1/jobs/{id}/runs?cursor=...          -> run history
POST   /v1/jobs/{id}:trigger                  -> manual run
DELETE /v1/jobs/{id}                          -> stop future runs

Worker protocol:
  claim(worker_id, capacity) -> [ { run_id, payload, lease_expires_at, fencing_token } ]
  heartbeat(run_id, fencing_token) -> extends lease | "lost"
  complete(run_id, fencing_token, status, output_ref)

job(job_id, tenant_id, schedule, timezone, target, retry_policy, timeout_s, next_run_at, version, enabled)
run(run_id, job_id, scheduled_for, not_before, priority, attempt, state, worker_id, lease_expires_at, fencing_token,
    started_at, finished_at, error)         -- UNIQUE(job_id, scheduled_for, attempt)
```

The unique key `(job_id, scheduled_for, attempt)` makes run creation idempotent. If two scheduler instances race to create the 10:00 run, only one row wins.

#### Architecture and flow

```text
Clients --> Job API --> Job Store (definitions + index on next_run_at) <------------------------------+
                                ^                                                                     |
                                | scan due-soon (partitioned by job_id hash; each scheduler owns some |
                                | partitions via a lease from a coordination service)                 |
                       Scheduler instances (timing wheel / min-heap for the next ~60 s)               |
                                | create run row + advance next_run_at in ONE transaction             |
                                v                                                                     |
                       Ready queue (per tenant/priority; "not before" timestamps)                     |
                                |                                                                     |
                       Workers: claim -> execute -> heartbeat -> complete --------> Run Store ---------+
                                                                                   ^
                       Reaper: finds runs with expired leases -> retry (attempt+1, backoff) or dead-letter
```

**Scheduling loop:** each scheduler instance holds leases on a set of job partitions. Every few seconds it queries jobs in its partitions with `next_run_at <= now + 60 s` and loads them into an in-memory timing wheel. When a slot fires, it creates the `run` row (state `READY`), computes the next fire time from the cron expression in the job's time zone, and updates `next_run_at` with a version check, all in one transaction. Then it enqueues the run, or workers poll the run table directly.

**Execution:** a worker claims a run, which sets `RUNNING` with `lease_expires_at = now + 30 s` and a new, larger `fencing_token`. It heartbeats every 10 s. On completion it writes the result **conditioned on the fencing token**. If the worker dies, the reaper sees the expired lease and creates the next attempt with backoff. A zombie worker that wakes up later cannot commit, because its token is stale.

#### Deep dive: claiming work safely

For a database-backed queue, the claim must be atomic so two workers never take the same run. Locking rows while skipping those already locked lets many workers claim in parallel without blocking each other. `FOR UPDATE SKIP LOCKED` is supported by PostgreSQL 9.5+ and MySQL 8.0+.

```sql
-- fragment (PostgreSQL): claim up to 10 ready runs for this worker
WITH picked AS (
  SELECT run_id
  FROM run
  WHERE state = 'READY' AND not_before <= now()
  ORDER BY priority DESC, not_before
  LIMIT 10
  FOR UPDATE SKIP LOCKED
)
UPDATE run r
SET state = 'RUNNING',
    worker_id = $1,
    lease_expires_at = now() + interval '30 seconds',
    fencing_token = nextval('fencing_seq')
FROM picked
WHERE r.run_id = picked.run_id
RETURNING r.run_id, r.fencing_token;

-- completion is accepted only from the current lease holder
UPDATE run SET state = $3, finished_at = now()
WHERE run_id = $1 AND fencing_token = $2 AND state = 'RUNNING';
```

This scales to thousands of claims per second on one primary. Beyond that, move the ready queue to a partitioned log or queue service and keep the database as the system of record. Polling the database is simple and durable. A dedicated queue raises throughput at the cost of keeping the two in sync, typically with a transactional outbox.

#### Deep dive: time is the hard part

- **Time zones and DST:** store the schedule in the tenant's zone and compute the next fire time in that zone, then convert to UTC. A 02:30 daily job does not exist on the spring-forward day and occurs twice on fall-back. Define the policy (skip, or run once at the next valid time; run only the first occurrence) and test it.
- **Misfires:** after a 2-hour scheduler outage, should an every-5-minutes job run 24 times? Usually not. Policies are `run_once` (one catch-up run), `skip` (resume at the next slot), or `run_all` (backfill, for data pipelines with per-interval semantics).
- **Clock skew:** schedulers and workers compare against their local clocks. Keep NTP-disciplined clocks, add margins (lease durations far above the skew), and never rely on two machines agreeing to the millisecond. Fencing tokens make correctness independent of clock accuracy.
- **Overlap policy:** if the 10:00 run is still going at 10:05, `forbid` skips the new run, `allow` runs both, and `replace` cancels the old one. Enforce it with a per-job state check inside the run-creation transaction.

#### Scaling and failure concerns

- **Scheduler high availability:** partition jobs by `hash(job_id)` into, for example, 1,024 partitions. Scheduler instances take leases on partitions through a coordination service, using consensus-backed leases. If an instance dies, its leases expire and others take over. Duplicate run creation during a handover is harmless because of the unique `(job_id, scheduled_for, attempt)` key.
- **Exactly-once is not available end to end.** A worker can finish the side effect and crash before reporting. Provide `run_id` to the job as an idempotency key, and document at-least-once.
- **Fairness and quotas:** per-tenant concurrency limits and weighted fair queues stop one tenant's 1M-job backfill from starving everyone. Use priority classes, preempting low priority only when the job is checkpointable.
- **Retries:** exponential backoff with jitter (`base × 2^attempt ± random`), a cap, and dead-lettering with an alert after the maximum attempts. Classify errors. Do not retry validation failures.
- **Observability:** schedule lag (actual start minus scheduled time) as the primary SLO, queue age, lease expirations (worker crashes), retry rate, and dead-letter count per tenant.
- **DAGs:** store the dependency edges. When a run succeeds, decrement the dependents' pending-parent counters in the same transaction, and mark a node `READY` when its counter reaches 0. That is Kahn's algorithm applied incrementally.

**Main interview tradeoff:** a **database-polling** scheduler (with an indexed `next_run_at` and `SKIP LOCKED` claims) is simple, transactional, and easy to reason about, but tops out at thousands of operations per second per shard. An **in-memory timing wheel fed from a durable log** scales to far higher rates and lower latency, but needs careful recovery, deduplication, and partition ownership to avoid lost or doubled runs.

#### Interview questions

**Q1. How do you make sure a job is not run twice when a worker is slow, not dead?**

Leases plus fencing. The worker holds a lease that it renews by heartbeat. If heartbeats stop (a GC pause or network partition), the reaper reassigns the run with a higher fencing token. The old worker may still be executing, so the system cannot prevent the side effect from happening twice. It can only ensure the stale worker's completion write is rejected (`WHERE fencing_token = mine`), and downstream systems that receive the token can reject stale writes too. The other half is making jobs idempotent by `run_id`. This is why the requirement says at-least-once.

**Q2. 2 million jobs are scheduled for exactly midnight. How do you handle it?**

(1) Spread the load: honor a per-job `jitter_s`, or a platform default dispatch window, so starts are spread over, say, 60 s. (2) Prepare ahead: schedulers create run rows and enqueue them minutes before with `not_before = 00:00`, so midnight is just a queue release, not 2M transactions. (3) Shape it: per-tenant concurrency caps, priority ordering, and autoscaling workers ahead of known peaks (the schedule is known in advance). (4) Measure schedule lag per priority and tell tenants the guarantee, such as "starts within 60 s at p99".

**Q3. Why not just run `cron` on a single big machine?**

It is a single point of failure: when it reboots, jobs are missed with no record. It has no retries, no history, and no visibility, and it cannot scale past one machine's capacity. It also has no concept of worker failure or idempotency. It is fine for a handful of internal jobs. The distributed design adds durable state (job store), high availability (partitioned schedulers with leases), separate execution capacity (workers), and correctness under failure (unique run keys, fencing, at-least-once with idempotency).

**Q4. How would you implement "run B after A succeeds, and C after both A and B"?**

Model a workflow as a DAG version that is immutable once started. Each workflow run creates node runs with a `pending_parents` count. When a node completes successfully, a transaction marks it done and decrements each child's counter; a child at 0 is enqueued. If a node fails after its retries, mark its downstream nodes `UPSTREAM_FAILED` (or apply the configured trigger rule). Detect cycles at submit time with a topological sort. Re-running a single failed node later must reuse its upstream outputs, so persist the outputs or references.

See also: [LLD: Task Scheduler](../design-patterns/Low_Level_Design_Interview_Prep.md#13-worked-design-task-scheduler), [Concurrency Coding Problems](Concurrency_Coding_Problems.md) (in-process scheduler and timer implementations), [Transactions and ACID](CS_Fundamentals.md#35-transactions-and-acid).

### 6.13 Metrics, Logging, and Monitoring System

This prompt is directly relevant to profiling and tooling roles: it is the fleet-scale version of collecting hardware counters, aggregating them, and answering questions about them quickly.

#### Requirements and assumptions

- Collect **metrics** (numeric time series identified by a name plus labels) from about 100k hosts and containers, including services, OS, and accelerator telemetry.
- Dashboards: query the last hour at 10 s resolution in under 1 s, and the last year at 1-hour resolution in a few seconds.
- **Alerting:** evaluate rules every 30–60 s, and route deduplicated alerts to on-call within about a minute of a condition becoming true.
- **Logs:** ingest structured logs, search them by service, host, and time range plus a text filter, with 30 days hot and longer in cold storage.
- Multi-tenant with per-tenant limits, especially on **cardinality**.
- The monitoring system must be **more available than the systems it monitors**, and it must detect its own failure.
- Distributed tracing is out of scope; mention it as the third pillar.

#### Capacity estimate

```text
Metrics
  Active series:     100k hosts × ~1,000 series/host                 = 100M active series
  Samples:           100M ÷ 10 s scrape interval                     = 10M samples/s
  Compressed size:   ~1.5 bytes/sample (delta-of-delta timestamps + XOR values)
  Raw ingest:        10M × 1.5 B = 15 MB/s ≈ 1.3 TB/day
  Retention tiers:   raw 10 s for 15 days          ≈ 20 TB
                     5-min rollups for 90 days:  100M × 25,920 points × 5 aggregates × 1.5 B ≈ 19 TB
                     1-h rollups for 2 years:    100M × 17,520 points × 5 aggregates × 1.5 B ≈ 13 TB
  Index memory:      ~2 KB per active series (labels, postings, head chunk) ≈ 200 GB
                     -> ~2M series per ingester => ~50 ingesters; × 3 replicas => ~150 ingesters
  Per ingester:      10M samples/s × 3 replicas ÷ 150 ≈ 200k samples/s

Logs
  Volume:            100k hosts × ~1 KB/s = 100 MB/s ≈ 8.6 TB/day raw, ~0.9 TB/day compressed (~10×)
  Hot 30 days:       ≈ 26 TB compressed (+ index; full-text indexing can add as much again or more)

Why rollups matter:  1 year of one series at 10 s = 3.15M points; at 1 h = 8,760 points (360× fewer)
```

**What the numbers decide:** at 10M samples/s, ingest must be sharded by series and appended in memory (a write-ahead log plus compressed in-memory head blocks), not written row by row to a database. About 200 GB of series index means **cardinality is a memory budget** to enforce per tenant. Rollups make long-range queries feasible. Raw log volume is about 7× the compressed metric ingest (100 MB/s vs 15 MB/s), and a full-text index can add as much again or more, so whether to build a full-text index is the main cost decision.

#### Interfaces and data

```text
Ingest:   POST /v1/metrics:write  (batched, compressed; tenant from auth)
          series = { __name__="gpu_utilization", cluster="c7", host="n123", gpu="3" }
          samples = [(ts_ms, float64), ...]
          POST /v1/logs:write     { stream_labels, [(ts_ns, line)] }
Query:    GET  /v1/query_range?expr=avg by (cluster)(rate(http_requests_total[5m]))&start&end&step
          GET  /v1/logs?selector={service="api",level="error"}&contains="timeout"&start&end
Rules:    alert HighErrorRate: expr  = sum by (svc)(rate(errors[5m])) / sum by (svc)(rate(requests[5m])) > 0.02
                               for   = 5m        labels = { severity="page" }

Storage model (metrics):
  series_id = hash(sorted label set)
  inverted index: label=value -> sorted list of series_ids (posting list); intersect for selectors
  chunks: per series, ~2 h of samples compressed together; immutable blocks of all series per time window
  rollup blocks: per series per window {min, max, sum, count, last}
```

#### Architecture and flow

```text
Hosts: agent (scrape local exporters / receive push, buffer to disk, batch, compress)
   |
   v
Ingest gateway (auth, per-tenant rate + cardinality limits, validation)
   |
   v   partition by hash(tenant, series_id); replicate ×3
Durable log/stream ----> Ingesters: WAL + in-memory head (last ~2 h, compressed chunks)
                              |  every 2 h: cut immutable block
                              v
                         Object storage: blocks (chunks + index) <---- Compactor: merge blocks,
                              ^                                         dedupe replicas, build rollups,
                              |                                         apply retention
Query frontend (split by time, result cache, per-tenant query limits)
   |--> Queriers --> recent data from ingesters + historical from store gateways (index/chunk caches)
   |
Rule evaluator (recording + alerting rules, every 30–60 s) --> Alert manager (dedupe, group, inhibit,
                                                                silence, route) --> paging / Notification System
Logs: agent --> gateway --> log ingesters (compress per stream into chunks) --> object storage
                         \-> optional full-text indexer --> search index (hot tier only)
Meta-monitoring: separate, small monitoring stack in another failure domain + "watchdog" alert
```

**Write path:** agents scrape every 10 s, batch about 1 s of samples, and send them. The gateway rejects tenants over their limits early, which is cheap. Each sample is appended to the WAL of three ingesters chosen by consistent hashing of the series, then to the in-memory head chunk. Every 2 hours, ingesters cut blocks and upload them to object storage. The compactor deduplicates the three replicas and merges blocks into larger time ranges.

**Read path:** the frontend splits a 7-day query into daily subqueries, serves completed days from the result cache (past data is immutable), and picks the resolution from the range: raw for 2 days or less, 5-minute rollups for 90 days or less, hourly beyond that. Queriers resolve label selectors through the inverted index (intersecting posting lists), fetch chunks, decompress them, and evaluate.

#### Deep dive: time-series compression

Consecutive samples are highly regular, so encode differences:

- **Timestamps, delta-of-delta:** scrapes arrive at t, t+10 s, t+20 s and so on. The deltas are 10, 10, 10, so the delta-of-delta is 0 and is stored in **1 bit**. Jitter produces small values in a few bits.
- **Values, XOR with the previous float:** an unchanged value XORs to 0 (**1 bit**). A slowly changing value shares sign, exponent, and leading mantissa bits, so only the meaningful middle bits are stored.
- The result is about 1.3–2 bytes per sample instead of 16 (an 8-byte timestamp plus an 8-byte float). That is roughly 10× less memory and disk. The tradeoff is that a chunk must be decoded sequentially, which is fine because queries scan ranges.

#### Deep dive: downsampling done correctly

- Store **min, max, sum, count** (and **last** for counters) per window. The average over a coarser window is `Σsum / Σcount`. Averaging the averages is wrong when windows have different counts, for example after missed scrapes.
- **Counters** reset when a process restarts. `rate()` detects decreases and compensates, so rollups must keep enough information (last value plus reset-adjusted increase) for that.
- **Percentiles do not compose:** the p99 of an hour is *not* the average or maximum of twelve 5-minute p99 values. Record **histograms** with fixed buckets (bucket counts are summable across time and hosts) or mergeable sketches, and compute quantiles at query time.
- Peaks vanish in averages. A one-minute 100% CPU spike disappears in a 1-hour average, so dashboards over long ranges should show max alongside avg.

#### Deep dive: cardinality, the failure mode of metrics systems

The number of series is the **product of label-value counts that actually co-occur**.

```text
http_requests_total{service, endpoint, method, status, pod}
  per service: 20 endpoints × 2 methods × 5 status codes × 30 pods  = 6,000 series
  × 200 services                                                     = 1.2M series      (fine)
add user_id (1M active users, each touching ~3 endpoints on ~2 pods with ~2 statuses):
  1M × 3 × 2 × 2                                                     ≈ 12M new series   (10× the metric)
add request_id                                                       => a new series per request (unbounded)
```

Each series costs index memory (about 2 KB here), so one bad label can exhaust ingesters and slow every query that touches the metric. Defenses:

- Enforce per-tenant and per-metric series limits at the gateway, rejecting with a clear error.
- Drop or relabel unbounded labels in the agent.
- Publish cardinality reports ("top metrics by series count").
- Teach the rule: **bounded labels go in metrics; per-request or per-user detail goes in logs or traces**, linked by exemplars or trace IDs.
- **Series churn** (pods replaced on every deploy) creates new series even when the active count is stable. It inflates the index for the retention period, so prefer stable labels (deployment, not pod) where per-pod detail is not needed.

#### Deep dive: logs, index everything or index labels

| Approach | Ingest cost | Storage | Query | Fits |
|---|---|---|---|---|
| Full-text inverted index on every field | High CPU per line | Index can rival or exceed the compressed data | Fast arbitrary search | Security, audit, ad-hoc search on smaller volumes |
| Index only a few stream labels; compress lines into chunks; scan at query time | Low | Small index, cheap object storage | Fast when labels narrow the time range and streams; slow for "grep everything" | High-volume operational logs |

Common hybrid: label-index everything, full-text index only a hot subset (errors, audit logs) for a few days, and keep everything compressed in object storage. Also sample or rate-limit debug logs at the source, because the cheapest byte is the one never shipped.

#### Scaling and failure concerns

- **Pull vs push:** pull (the server scrapes targets) makes target health observable (a failed scrape is itself a signal) and lets the server control the rate. Push suits short-lived jobs, devices behind NAT, and very large fleets where agents forward to a gateway. Most large designs use local agents that scrape locally and push upstream.
- **Backpressure:** agents buffer to local disk (for example 1–2 hours) when the gateway is unavailable, and the gateway sheds load by priority (alerting-critical metrics first). Never let telemetry take down the workload: cap the agent's CPU and memory.
- **Replication and dedup:** three-way ingest replication survives ingester loss. Queries deduplicate replica samples by series and timestamp, and the compactor deduplicates permanently.
- **Hot tenants or queries:** per-tenant query concurrency limits, a maximum number of series touched per query, query timeouts, and result caching. A dashboard auto-refreshing every 5 s for 500 viewers needs caching, not more queriers.
- **Alert quality:** use `for:` durations to avoid flapping, alert on symptoms (SLO burn rate) rather than causes, and use grouping and inhibition so one zone outage pages once, not 5,000 times.
- **Meta-monitoring:** a separate minimal stack in another failure domain monitors the main one, and an always-firing **watchdog** alert goes to an external receiver. If the watchdog stops arriving, the pipeline is broken. Without this, the monitoring system fails silently exactly when you need it.

**Main interview tradeoff:** **label richness versus cost**. More labels and higher resolution let you slice problems precisely, but the series count multiplies memory, index size, and query cost. Metrics stay aggregated and bounded; high-cardinality detail goes to logs or traces, which are cheaper per event to store but slower to aggregate.

#### Interview questions

**Q1. Ingesters are running out of memory after a deploy. What happened and how do you prevent it?**

Almost always a cardinality explosion. A new label with unbounded values (user ID, request path with IDs, error message text) or high pod churn created millions of new series, each with index and head-chunk memory. Immediate fix: find the metric with the cardinality report, then drop or relabel the label at the agent or gateway, or reject that metric. Prevention: per-tenant and per-metric series limits enforced at ingest, CI linting of instrumentation, and dashboards for series count and churn per metric.

**Q2. How would you store and query the p99 latency of a service over the last 30 days?**

Do not store p99 values and average them, because quantiles do not aggregate. Record a **histogram** (cumulative bucket counters, for example 5 ms ... 10 s). Rollups keep per-bucket increases. At query time, sum the bucket increases over 30 days across all instances, then interpolate the 99th percentile from the cumulative distribution. Accuracy depends on bucket boundaries, so place more buckets near the SLO threshold, or use mergeable sketches with bounded relative error if supported.

**Q3. Pull or push for 100k ephemeral containers that live 2 minutes?**

Pure pull struggles with ephemeral targets: service discovery has to find each container and scrape it at least a few times before it dies, and the final counter values are lost at exit. Use a **node-local agent** that both scrapes long-lived processes and receives pushes from short-lived ones (or reads cgroup stats directly), then forwards upstream in batches. Short batch jobs push final values on exit. Keep `pod` out of long-retention labels to limit churn.

**Q4. How do you know the monitoring system itself is healthy?**

Meta-monitor it from a separate failure domain. Watch ingest lag, dropped and rejected samples, rule-evaluation duration and missed evaluations, and alert-delivery latency. Configure an always-firing **watchdog** alert routed to an external heartbeat receiver, which pages if the heartbeat stops. Periodically inject a synthetic failure (a canary target that goes "down") and verify the page arrives end to end.

See also: [Notification System](#611-notification-system) for alert delivery, [Debugging and Profiling Tools](../tools/Debugging_and_Profiling_Tools.md), [Project Deep Dive: rocprof-compute](../career/Project_Deep_Dive_rocprof-compute.md) (counter collection and analysis at device scale), [ML Systems Design](../ml-gpu/ML_Systems_Design.md) (GPU fleet telemetry).

### 6.14 Object Storage (S3-like)

#### Requirements and assumptions

- Buckets contain objects addressed by key. Operations: `PUT`, `GET` (including byte ranges), `DELETE`, `HEAD`, and `LIST` by prefix with a delimiter (pseudo-directories).
- Object sizes range from bytes to multiple TB. Large uploads use **multipart upload**: independent, retryable parts, then an atomic "complete".
- **Durability** target of "eleven nines" annual object durability (a design target, not a guarantee). Availability of 99.9–99.99%.
- **Consistency:** after a successful PUT, subsequent GETs and LISTs return the new object (strong read-after-write). Overwrites are atomic: readers see the old object or the new one, never a mix.
- Optional: versioning, lifecycle rules (expire or move to a colder tier), and server-side encryption.
- Out of scope: POSIX semantics (rename, append, locking). Object stores deliberately avoid them.

#### Capacity estimate

```text
Logical data:      100 PB, 100 billion objects (mean 1 MB; median far smaller -- size distribution is skewed)
Metadata:          100B objects × ~500 B (key, version, size, checksum, placement, ACL ref) ≈ 50 TB
                   × 3 replicas ≈ 150 TB -> needs its own sharded, strongly consistent store
Data, 3× replication:     100 PB × 3   = 300 PB raw
Data, erasure RS(10,4):   100 PB × 1.4 = 140 PB raw   -> saves 160 PB
Drives:            140 PB ÷ 20 TB HDD = 7,000 drives; at 80% max fill ≈ 8,750 drives

Requests:          50k GET/s, 10k PUT/s; mean bytes per GET ~500 KB (many small objects, range reads)
Egress:            50k × 500 KB = 25 GB/s ≈ 200 Gbit/s
Disk IOPS check:   HDD ≈ 100–200 random IOPS
                   if every GET touched 10 data fragments: 50k × 10 = 500k IOPS ÷ 150 ≈ 3,300 drives just for IOPS
                   if a small object lives inside ONE fragment:  50k × 1 = 50k IOPS ≈ 330 drives
```

**What the numbers decide:** metadata alone (about 50 TB, billions of keys, strongly consistent, with ordered listing) is a distributed database problem, so **separate metadata from data**. Erasure coding saves about 160 PB of disk compared with triple replication, which justifies its complexity. The IOPS check shows that small objects must not be striped across 10 disks. Pack small objects into large extents, and erasure-code the *extent*, so a small read touches one disk.

#### Interfaces and data

```text
PUT    /{bucket}/{key}                 body, Content-Length, checksum header -> 200 { etag, version_id? }
GET    /{bucket}/{key}  Range: bytes=0-1048575                              -> 206 partial content
DELETE /{bucket}/{key}                                                     -> 204 (tombstone / delete marker)
GET    /{bucket}?list-type=2&prefix=logs/2026/11/&delimiter=/&continuation-token=...
POST   /{bucket}/{key}?uploads                     -> { upload_id }
PUT    /{bucket}/{key}?partNumber=7&uploadId=...   -> { part_etag }
POST   /{bucket}/{key}?uploadId=...  [ (part_number, part_etag), ... ]     -> commit (atomic)

Metadata (sharded by (bucket, key) RANGE so LIST by prefix is a range scan):
  bucket(bucket_id, name UNIQUE, owner, region, versioning, policy, created_at)
  object(bucket_id, key, version_id, is_latest, size, etag/checksum, content_type,
         created_at, delete_marker, manifest)
  manifest = [ { extent_id, offset, length } , ... ]     -- where the bytes live
Data plane:
  extent(extent_id, stripe = [ (fragment_index, storage_node, disk, checksum) × 14 ], state)
```

#### Architecture and flow

```text
Client --> DNS / LB --> Front-end fleet (auth, signature check, throttling, request routing; stateless)
                         |                                   |
                         | metadata ops                      | data streaming
                         v                                   v
             Metadata service                       Placement / cluster map service
             (range-partitioned, replicated          (which nodes/disks hold which extents;
              with consensus per partition)           failure domains: disk -> host -> rack -> zone)
                         ^                                   |
                         |                                   v
                         |                 Storage nodes: append-only extents on local disks,
                         |                 per-fragment checksums, background scrubbing
                         |
Background: Garbage collector (unreferenced extents), Repair service (re-create lost fragments),
            Lifecycle worker (expire/tier), Usage metering, Compaction of extents with deleted space
```

**PUT (large object):**

1. The front end authenticates and authorizes the request.
2. It asks placement for an open extent stripe: 14 fragments on 14 different racks, ideally spread across zones.
3. It streams the body in chunks, encodes each stripe into 10 data + 4 parity fragments, and writes them in parallel. It verifies the client-supplied checksum end to end.
4. Once all fragments are durable (or at least k + safety margin, with the rest repaired later per policy), it **commits the metadata row** pointing to the manifest.
5. **The metadata commit is the linearization point.** Before it, the object does not exist. After it, every GET sees it. Data written but never committed (a crash mid-upload) is orphaned and reclaimed by garbage collection.

**GET:** look up metadata (cached on the front end for hot keys, with versioning so overwrites are not served stale), get the manifest, and read the needed byte range directly from the data fragments. Decoding is needed only if a data fragment is slow or lost; then read any 10 of the 14 and decode. Stream the result to the client.

**DELETE:** write a tombstone or delete marker in metadata (immediately invisible). The garbage collector later decrements the extent reference counts and reclaims space when an extent is mostly dead, by rewriting its live objects elsewhere.

#### Deep dive: erasure coding vs replication

**Reed-Solomon RS(k, m)** splits data into k fragments and computes m parity fragments. **Any k of the k + m** fragments reconstruct the data.

| | 3× replication | RS(10,4) erasure coding |
|---|---|---|
| Storage overhead | 3.0× | 1.4× |
| Failures tolerated per object | 2 | 4 |
| Normal read | 1 disk | 1 disk if the range is within one data fragment; else several |
| Degraded read (a fragment lost) | Read another copy | Read 10 fragments and decode (CPU + 10× I/O) |
| Repair one lost disk | Copy its data from survivors (1× read) | For each stripe, read 10 fragments to rebuild 1 (10× read amplification) |
| Write | 3 full copies (3× network) | 1.4× network, plus encoding CPU |
| Fits | Hot, small, latency-sensitive data; metadata | Warm or cold bulk data; large objects |

**Rough durability intuition** (independent failures; real systems must also handle correlated failures):

```text
Drive annual failure rate 2%, repair window 24 h:
  P(given drive fails within window) ≈ 0.02 ÷ 365 ≈ 5.5e-5

3× replication, after one copy is lost:
  P(both remaining copies fail before repair) ≈ (5.5e-5)^2 ≈ 3e-9 per loss event

RS(10,4), after one fragment is lost:
  P(4 more of the remaining 13 fail before repair) ≈ C(13,4) × (5.5e-5)^4 ≈ 715 × 9e-18 ≈ 6.5e-15 per loss event
```

The levers that matter are visible in these formulas: **faster repair** (a shorter window, achieved by spreading each disk's fragments across many peers so thousands of disks rebuild in parallel), **more parity**, and **independent failure domains** (never two fragments of a stripe on the same host or rack). Correlated failures (a bad firmware batch, a power event) usually dominate real data loss, which is why fragments are also spread across zones and drives from different batches.

#### Scaling and failure concerns

- **Metadata hot spots:** keys with sequential prefixes (`logs/2026-11-03T10:00:01`) all land in one range partition. Split partitions automatically by load, not just size. Advise clients to put high-entropy prefixes first if extreme rates are needed. LIST is a range scan with continuation tokens, so a 1M-key listing is a series of pages, never one call.
- **Small objects:** pack them into large append-only extents (for example 1 GB), erasure-code the extent once it is sealed, and keep it replicated while it is open. This avoids the per-object fragment and IOPS overhead shown in the estimate.
- **Integrity:** keep checksums per fragment and end to end (the client checksum is verified at write and returned on read). A background **scrubber** reads every fragment periodically (for example every few weeks) to find silent corruption and repairs it from parity.
- **Multipart upload:** parts are stored as independent extents, and "complete" atomically writes one metadata row that lists them. Incomplete uploads are expired by a lifecycle rule; otherwise they leak storage.
- **Overwrites and consistency:** an overwrite writes new data to new extents, then atomically swaps the metadata pointer. Readers never see a torn object, and the old extents are garbage-collected after in-flight reads finish (with a grace period).
- **Hot objects:** one popular object can saturate its few disks. Front-end caching, a CDN for public content, and temporary extra replicas of hot extents help.
- **Region failure:** asynchronous cross-region replication on a per-bucket policy. State the RPO (seconds to minutes of lag) and that strong consistency is per region.

**Main interview tradeoff:** **erasure coding versus replication**. EC cuts raw storage roughly in half or better at equal or higher fault tolerance, but makes repair, degraded reads, and small-object access more expensive in I/O and CPU. Replication is simpler and faster for hot, small data. Most real systems use both: replicate new or hot data and metadata, and erasure-code sealed bulk extents.

#### Interview questions

**Q1. Why separate the metadata service from the data servers?**

They have opposite profiles. Metadata is small per object, needs strong consistency, transactions (atomic overwrite, multipart complete), and ordered range scans for LIST. Data is large, immutable once written, and needs bandwidth and cheap capacity. Separating them lets metadata use a replicated, range-partitioned consensus-backed store, and lets data use dumb, append-only storage nodes with erasure coding. It also makes the metadata commit a single, clear point of atomicity for each object.

**Q2. How do you provide read-after-write consistency for overwrites when front ends cache metadata?**

Either do not cache "latest version" lookups (cache only immutable version-to-manifest mappings, and resolve the latest version from the metadata service, which is strongly consistent per partition), or validate cached entries cheaply with a per-partition version or lease. Data extents are immutable, so the only thing that can go stale is the pointer. Keep that pointer authoritative and cache the immutable parts freely.

**Q3. A storage node with 20 disks dies permanently. Walk through recovery.**

The cluster map marks it failed after a grace period (to avoid repairing data during a reboot). The repair service lists every stripe with a fragment on those disks. For EC, it reads 10 surviving fragments per stripe, re-encodes the missing one, and writes it to a new node in an unused failure domain. Because fragments are spread widely, thousands of disks participate in parallel, so 400 TB rebuilds in hours, not the days a single replacement disk would take. Prioritize stripes that have lost the most fragments, and throttle repair so foreground latency stays within SLO.

**Q4. How would you implement LIST with a delimiter efficiently?**

Metadata is sorted by `(bucket, key)`, so `prefix=photos/&delimiter=/` is a range scan from `photos/`. When the scan meets a key with another `/` after the prefix (for example `photos/2026/a.jpg`), it emits the common prefix `photos/2026/` once, then **seeks past** all keys with that common prefix (to `photos/2026/` followed by the next possible character) rather than reading them. Return pages of up to 1,000 entries with a continuation token holding the last key, so the scan resumes without server-side cursors.

See also: [Video Streaming Platform](#65-video-streaming-platform) (direct-to-object-storage uploads), [Distributed Key-Value Store](#68-distributed-key-value-store) (replication and repair), [Math, Probability, and Estimation](Math_Probability_Estimation.md) (failure-probability reasoning).

### 6.15 Ticket Booking (Seat Reservation)

Movie, concert, and event booking platforms all share this shape: a small, fixed inventory, extreme contention during on-sales, and money involved.

#### Requirements and assumptions

- Users browse events, view a **seat map** with availability, select specific seats (reserved seating) or a quantity (general admission), and pay.
- **No double booking, ever.** This is the one hard-consistency requirement.
- Selected seats are **held** for a limited time (for example 10 minutes) while the user pays. If payment does not complete, the hold expires and the seats return to inventory.
- Retries (double clicks, flaky mobile networks, payment callbacks) must not create two bookings or charge twice.
- Survive **flash on-sales**: millions of users arriving within minutes for tens of thousands of seats, with fair ordering and protection from bots.
- Seat-map availability may be slightly stale (about a second). The hold operation itself must be authoritative.

#### Capacity estimate

```text
Normal load:       1M bookings/day ÷ 86,400 ≈ 12 bookings/s; browsing ~100× that -> trivial
Inventory:         100k events/year × 20k seats × ~100 B ≈ 200 GB/year of seat rows

Flash on-sale (the real design driver):
  Seats:           50,000 for one event
  Arrivals:        2M users in the first 10 minutes ≈ 3,300 users/s
  Seat-map reads:  ~10 per user over the session      ≈ 33k reads/s, all for ONE event
  Hold attempts:   ~2 per user (first choice often taken) ≈ 6,600 holds/s, all on ONE event's rows
  Demand/supply:   2M users × ~2.5 seats each = 5M seats wanted for 50k => 99% of users will fail

Single-partition write capacity: assume one primary sustains ~2–5k short write transactions/s
  (the low end of the Section 3 range, because every transaction hits the same hot rows)
  -> 6,600 holds/s on one event exceeds it, and contention on popular sections makes it worse
Admission rate:    admit ~500 users/s through a waiting room => ~1,000 holds/s (safe margin)
  50k seats ÷ ~2.5 seats per buyer = 20k buyers; at 500 admitted/s with ~50% converting
  ≈ 80 s to sell out once admission starts (minutes in practice, as users dawdle on the seat map)
```

**What the numbers decide:** steady state is easy. The on-sale is a **hot-partition problem**: all writes target one event. You cannot shard your way out, because seats of one event must be checked atomically. Instead, **meter demand** with a virtual waiting room, serve seat maps from a cache, and keep the hold transaction tiny and single-partition.

#### Interfaces and data

```text
GET  /v1/events/{event_id}/seatmap            -> { sections, seats: [{ seat_id, status }], version }
POST /v1/events/{event_id}/holds
     { "seat_ids": ["A1","A2"], "idempotency_key": "..." }  (admission token in header during on-sales)
     -> 201 { hold_id, expires_at } | 409 { unavailable: ["A2"] }
POST /v1/holds/{hold_id}/checkout { payment_method_token, idempotency_key }  -> { booking_id, status }
DELETE /v1/holds/{hold_id}                                                   -> release early

event(event_id, venue_id, starts_at, on_sale_at, status)
seat(event_id, seat_id, section, row, price_tier, status AVAILABLE|HELD|SOLD,
     hold_id, hold_expires_at, booking_id, version)        -- PRIMARY KEY (event_id, seat_id)
hold(hold_id, event_id, user_id, seat_ids, expires_at, idempotency_key UNIQUE(user_id, key), state)
booking(booking_id, hold_id UNIQUE, user_id, event_id, amount, payment_id, state, created_at)
```

Partition every inventory table by `event_id`, so a multi-seat hold is a **single-partition transaction**. Never let a hold span partitions.

#### Architecture and flow

```text
Users --> CDN (static assets, cached event pages)
      --> Waiting room (on-sale only): queue position, signed admission token with expiry, bot checks
      --> API gateway (auth, rate limits per user/IP/token)
           |                     |                               |
           v                     v                               v
     Seat-map service      Booking service ----------------> Payment service (idempotent; see 6.7)
     (reads from cache;    hold: conditional UPDATE on              |
      cache refreshed by    seat rows (one event partition)         | payment result (sync or webhook)
      change events)       confirm: HELD -> SOLD if hold valid <----+
           ^                     |
           |                     +--> Inventory DB (partitioned by event_id; primary + sync replica)
           |                     +--> Outbox --> Event stream: seat changes, booking confirmed
           +---------------------------------------- (updates seat-map cache, emails, analytics)
     Hold expiry sweeper: releases expired holds (the predicate already treats them as free)
```

**Hold flow:** a user picks A1 and A2. The booking service runs one conditional update that flips both seats to `HELD` only if each is available or its hold has expired. If the affected row count is less than the requested count, roll back and return 409 with the unavailable seats. **The database decides the winner**, not the application reading and then writing.

**Checkout flow:** the client calls checkout with an idempotency key. The service verifies the hold is still valid and charges through the payment service, using the `hold_id` as the payment idempotency key. On success it runs `HELD -> SOLD` conditioned on the same `hold_id` and an unexpired hold, then writes the booking and an outbox event in the same transaction.

#### Deep dive: making the hold atomic

Three common ways to implement the hold:

| Approach | How | Pros | Cons |
|---|---|---|---|
| **Pessimistic lock** | `SELECT ... FROM seat WHERE event_id=? AND seat_id IN (...) FOR UPDATE`, check, update, commit | Simple reasoning; readable code | Lock waits under contention; must lock rows in a consistent order (sort seat IDs) to avoid deadlocks |
| **Conditional update** | A single `UPDATE ... WHERE status is free`; check the affected row count | One round trip, short critical section, no read-then-write gap | Works for "these exact rows" predicates; harder for constraints across rows |
| **Optimistic version** | Read seats with `version`; `UPDATE ... WHERE version = read_version`; retry on conflict | No locks held across user think-time | Retry storms under heavy contention: poor for on-sales |

A runnable demonstration of the conditional-update approach, using SQLite so it needs no server:

```python
import sqlite3

HOLD_SECONDS = 600


def setup() -> sqlite3.Connection:
    db = sqlite3.connect(":memory:", isolation_level=None)  # explicit BEGIN/COMMIT below
    db.execute("""CREATE TABLE seats (
        event_id INTEGER, seat_id TEXT,
        status TEXT NOT NULL DEFAULT 'AVAILABLE',  -- AVAILABLE | HELD | SOLD
        hold_id TEXT, hold_expires_at INTEGER, booking_id TEXT,
        PRIMARY KEY (event_id, seat_id))""")
    db.executemany("INSERT INTO seats (event_id, seat_id) VALUES (1, ?)",
                   [("A1",), ("A2",), ("A3",)])
    return db


def hold(db, event_id: int, seats: list[str], hold_id: str, now: int) -> bool:
    """All-or-nothing hold. Re-sending the same hold_id is idempotent."""
    marks = ",".join("?" * len(seats))
    db.execute("BEGIN IMMEDIATE")  # take the write lock before reading
    cur = db.execute(f"""
        UPDATE seats SET status = 'HELD', hold_id = ?,
            hold_expires_at = CASE WHEN hold_id = ? AND hold_expires_at >= ?
                                   THEN hold_expires_at ELSE ? END  -- retry does not extend
        WHERE event_id = ? AND seat_id IN ({marks})
          AND (status = 'AVAILABLE'
               OR (status = 'HELD' AND (hold_expires_at < ? OR hold_id = ?)))""",
        [hold_id, hold_id, now, now + HOLD_SECONDS, event_id, *seats, now, hold_id])
    if cur.rowcount != len(seats):  # someone else holds or bought at least one seat
        db.execute("ROLLBACK")
        return False
    db.execute("COMMIT")
    return True


def confirm(db, hold_id: str, booking_id: str, now: int) -> bool:
    """Called after payment succeeds; fails if the hold already expired."""
    cur = db.execute("""UPDATE seats SET status = 'SOLD', booking_id = ?
                        WHERE hold_id = ? AND status = 'HELD' AND hold_expires_at >= ?""",
                     [booking_id, hold_id, now])
    return cur.rowcount > 0


if __name__ == "__main__":
    db = setup()
    t = 1_000
    print(hold(db, 1, ["A1", "A2"], "h-alice", t))        # True
    print(hold(db, 1, ["A2", "A3"], "h-bob", t + 1))      # False: A2 is held
    print(hold(db, 1, ["A1", "A2"], "h-alice", t + 2))    # True: idempotent retry
    print(hold(db, 1, ["A2", "A3"], "h-bob", t + 700))    # True: alice's hold expired
    print(confirm(db, "h-alice", "b-1", t + 701))         # False: too late, refund/release
    print(confirm(db, "h-bob", "b-2", t + 702))           # True
    print(db.execute("SELECT seat_id, status, hold_id FROM seats").fetchall())
```

Points to call out:

- Expiry is **part of the predicate** (`hold_expires_at < now`). Correctness does not depend on a sweeper running on time; the sweeper only tidies rows for the seat map.
- Expiry checks use `<` for stealing and `>=` for confirming, so for any instant exactly one of "steal" and "confirm" can succeed. In a real deployment, `now` must come from the database clock, not from each app server, so skewed app clocks cannot disagree.
- **Write skew:** a rule like "do not leave a single empty seat between two sold seats" depends on *neighboring* rows that the update does not touch. Two concurrent holds under snapshot isolation can each see the rule satisfied and together violate it. Either lock the whole row segment (`FOR UPDATE` on the neighbors too), run that transaction at SERIALIZABLE isolation, or enforce the rule asynchronously. See [Transactions and ACID](CS_Fundamentals.md#35-transactions-and-acid).

#### Deep dive: general admission and hot counters

Without assigned seats, inventory is a counter: `UPDATE inventory SET remaining = remaining - :n WHERE event_id = ? AND remaining >= :n`. Every buyer then contends on **one row**, which serializes at the row lock (a few thousand updates per second at best). Split the counter into, for example, 20 **sub-counters** of 2,500 tickets each. A request picks a random sub-counter and moves to another when it is empty. That gives up to 20× the concurrency, and the total can never go negative because each sub-counter is guarded independently. Near sell-out, requests probe several empty buckets, which is acceptable.

#### Scaling and failure concerns

- **Waiting room:** assign queue positions at arrival (randomize everyone who arrived before the on-sale opens, so refreshing early earns nothing). Admit at a rate the booking backend can sustain, and issue a short-lived signed **admission token** that the booking API requires. This turns an uncontrolled spike into a metered flow, and it is the single most important on-sale defense.
- **Seat-map reads:** serve from a cache updated by seat-change events, aggregated per section ("Section 104: 37 left") at high load. A stale "available" seat just leads to a fast 409 on hold, and the client refreshes that section.
- **Spread contention:** offer "best available" allocation (the server picks seats within a section and price tier) instead of everyone clicking the same front-row seats. This reduces failed holds dramatically.
- **Payment and hold expiry race:** if payment is slow and the hold expires mid-checkout, either (a) extend the hold once the checkout starts (a "payment in progress" state with its own longer deadline) or (b) if confirmation fails after a successful charge, automatically refund. Never mark a seat sold for two bookings; the conditional `HELD -> SOLD` update guarantees that.
- **Idempotency:** the hold has a unique `(user_id, idempotency_key)`, the booking has a unique `hold_id`, and the payment idempotency key is derived from `hold_id`. Retrying any step returns the original result. See [Payment Processing](#67-payment-processing).
- **Abuse:** per-account and per-payment-instrument purchase limits, bot detection at the waiting room, and holds that count against a user's concurrent-hold limit (so a script cannot hold the whole venue).
- **Database failure during an on-sale:** a synchronous replica with automatic failover keeps RPO = 0 for bookings. Pause admission from the waiting room during failover instead of letting clients retry-storm the new primary.

**Main interview tradeoff:** **holding seats at selection time** gives a good user experience (your seats are yours while you pay) but locks inventory behind users who abandon checkout. Shorter holds and per-user hold limits mitigate that. **Allocating only at payment** keeps inventory liquid but makes many users fail after entering payment details. At on-sale scale, a waiting room plus short holds is the usual balance: correctness comes from single-partition conditional updates, and survivability comes from metering demand rather than scaling the hot partition.

#### Interview questions

**Q1. Two users click "hold" on seat A1 at the same millisecond. Exactly what prevents a double booking?**

Both requests run `UPDATE seat SET status='HELD', hold_id=? WHERE event_id=? AND seat_id='A1' AND (status='AVAILABLE' OR (status='HELD' AND hold_expires_at < now()))`. The status guard matters: without it, the stale expired timestamp on a SOLD seat would make it re-holdable. The database takes a row lock for the first update. The second waits, then re-evaluates the predicate against the committed new row (or, under some isolation implementations, aborts with a serialization error and retries). Either way it now sees `HELD` and affects 0 rows. The application sees `rowcount = 0` and returns 409. A read ("is A1 free?") followed by a separate write would be the bug: both reads succeed before either write.

**Q2. Why not keep holds only in an in-memory store with TTL keys?**

You can, and it is fast: `SET seat:{event}:{id} hold_id NX EX 600` gives an atomic hold with automatic expiry. But then two stores must agree. The in-memory store says held while the database is the source of truth for sold, and a failover of the in-memory store can lose holds, so two users get the same seat. If you use it, keep the final `HELD -> SOLD` (or `AVAILABLE -> SOLD`) transition as a conditional write in the durable database, so the worst case is a failed checkout, not a double sale. Many teams use the cache to absorb contention and the database for correctness.

**Q3. Payment succeeded but the confirm update returned 0 rows. What now?**

The hold expired (or was released) between payment authorization and confirm, and someone else may now hold the seat. The booking must not be created for that seat. Options, by preference: if the payment was only **authorized** (not captured), void the authorization; otherwise issue an automatic refund. Tell the user clearly, and optionally offer comparable seats with a new hold. To make this rare, put the hold in a "payment in progress" state with an extended deadline when checkout begins, and authorize before capture.

**Q4. How do you make the on-sale fair and keep bots out?**

Use the waiting room as the fairness boundary. Randomize positions for everyone present before the on-sale time, then use first-come order after that. Require proof-of-humanity or account-level reputation before issuing an admission token, and bind the token to the account and device so it cannot be shared. Enforce per-account ticket limits at the hold and booking level, rate limit by account, IP, and payment instrument, and verify after the fact (cancel bookings that share a suspicious payment instrument). Fairness is a product decision, so say which policy you chose.

See also: [Payment Processing](#67-payment-processing), [LLD: Designing for Concurrency and Failure](../design-patterns/Low_Level_Design_Interview_Prep.md#4-designing-for-concurrency-and-failure), [HLD Mock Interviews](../practice/HLD_Mock_Interviews.md).

---

## 7. Interview Checklists and Pitfalls

### Before drawing

- [ ] State the most important functional requirements and exclusions.
- [ ] Clarify scale, latency, availability, consistency, and retention expectations.
- [ ] Identify the highest-value read and write paths.
- [ ] State assumptions and invite correction.

### While designing

- [ ] Keep each service's responsibility and data ownership clear.
- [ ] Explain the source of truth and which stores are derived or disposable.
- [ ] Trace at least one write and one read end to end.
- [ ] Define API semantics, authorization, and idempotency where retries matter.
- [ ] Explain partition keys, hot keys, ordering, and pagination when relevant.
- [ ] Show where asynchronous work is durably handed off.
- [ ] Cover dependency failures, retries, timeouts, and recovery.
- [ ] Connect every scale change to a measured or stated workload need.

### Common pitfalls

- **Starting with technologies:** name the requirement and access pattern first, then choose a component.
- **Building too much too soon:** a cache, queue, or microservice adds operating cost and new failure modes.
- **Ignoring data semantics:** state consistency, retention, deletion, and ordering requirements explicitly.
- **Treating retries as harmless:** retries can duplicate writes and amplify overload without idempotency and backoff.
- **Using a queue as a magic fix:** queues need capacity, retry, poison-message, ordering, and monitoring policies.
- **Calling every cache consistent:** specify staleness tolerance and invalidation behavior.
- **Ignoring abuse and security:** include authentication, authorization, quotas, and sensitive data handling.
- **Designing only the happy path:** explain what clients see during partial failure and how work recovers.
- **Overfocusing on estimates:** use rough math to guide decisions, then spend time on system behavior.

---

## 8. Practice Prompts

For each prompt, begin with the requirements and workload before selecting components.

1. Design a collaborative document editor with concurrent updates and offline clients. (Full solution: [HLD Practice A2](../practice/HLD_Practice_Problems.md#a2-collaborative-document-editor).)
2. Design a search autocomplete service for a large product catalog. (Attempt first, then compare with [6.9](#69-search-autocomplete-typeahead).)
3. Design a notification platform that sends email, push, and SMS with user preferences. (Attempt first, then compare with [6.11](#611-notification-system).)
4. Design a photo-sharing application with albums, privacy controls, and image processing. (Full solution: [HLD Practice A4](../practice/HLD_Practice_Problems.md#a4-photo-sharing-service-instagram).)
5. Design a distributed job scheduler with recurring jobs, retries, and worker health checks. (Attempt first, then compare with [6.12](#612-distributed-job-scheduler).)
6. Design a metrics ingestion and alerting platform with high write volume and time-based queries. (Attempt first, then compare with [6.13](#613-metrics-logging-and-monitoring-system).)

After drawing a design, explain one alternative, one failure scenario, and the metric that would tell you the system is approaching its limit.

### Where to practice next

- **Timed mock interviews with model answers:** [HLD Mock Interviews](../practice/HLD_Mock_Interviews.md) has a [45-minute self-mock procedure](../practice/HLD_Mock_Interviews.md#2-running-a-45-minute-self-mock), an [evaluation rubric by level](../practice/HLD_Mock_Interviews.md#3-evaluation-rubric-by-level) (what separates mid-level, senior, and staff answers), and full mock scripts with follow-up questions and model answers. Do at least one per week under a timer, out loud.
- **Twenty more problems with full model answers:** [HLD Practice Problems](../practice/HLD_Practice_Problems.md) (message queue, collaborative editor, Dropbox, leaderboard, ad-click aggregation, distributed cache, stock exchange, Airbnb, flash sale, maps, Zoom, lock service, search engine, email, food delivery, and more).
- **ML and HPC infrastructure prompts:** [ML Systems Design](../ml-gpu/ML_Systems_Design.md) covers [LLM inference serving](../ml-gpu/ML_Systems_Design.md#4-case-study-llm-inference-serving-platform), [distributed training on 512 MI300X](../ml-gpu/ML_Systems_Design.md#5-case-study-distributed-training-of-a-70b-model-on-512-mi300x), and a [GPU cluster job scheduler](../ml-gpu/ML_Systems_Design.md#6-case-study-gpu-cluster-job-scheduler). Those designs use the same process as this file, plus [ML-specific numbers](../ml-gpu/ML_Systems_Design.md#3-numbers-every-ml-systems-engineer-should-know).
- **Estimation drills:** [Fermi Estimation](Math_Probability_Estimation.md#9-fermi-estimation) for the arithmetic habits behind every capacity estimate in Section 6.
- **Self-check for each prompt above:** write the capacity block first (QPS, storage, bandwidth, connections) in the style of [6.1](#61-url-shortener), then name which number drove which component.

