# HLD Practice Problems -- Twenty System Design Problems with Full Solutions

> Last reviewed: 2026-11 · Versions assumed: vendor-neutral building blocks (Kafka-style logs, Redis, PostgreSQL, S3-style object storage, and WebRTC are named only where a concrete mechanism helps). Capacity numbers are napkin-math orders of magnitude, derived in each answer; benchmark figures quoted from the literature are labeled approximate.

This file is for **practicing** system design rounds with a full model answer to compare against. The method, estimation numbers, and building blocks are in [High Level Design](../computer-science/High_Level_Design.md), which also has 15 worked designs. The timed self-mock procedure and the scoring rubric are in [HLD Mock Interviews](HLD_Mock_Interviews.md). This file adds twenty problems that are not worked anywhere else in the repo. Problems 1-11 are full solutions to prompts that [HLD Mock Interviews §14](HLD_Mock_Interviews.md#14-twenty-unsolved-practice-prompts) only outlines as hints; problems 12-20 are new.

Each problem has the interviewer's prompt, what the interviewer is actually grading, and the clarifying questions to ask (with the answers a typical interviewer gives). Each answer in [Answers](#answers) has the same nine parts: **Requirements and assumptions**, **Capacity estimate** (with what the numbers decide), **Interfaces and data**, **Architecture and flow**, two to four **Deep dives**, **Failure modes and mitigations**, **Tradeoffs**, **Follow-ups with model answers**, and **Level signals** (what separates mid, senior, and staff answers).

See also: [HLD: A Repeatable Interview Process](../computer-science/High_Level_Design.md#2-a-repeatable-interview-process) · [Estimate the Workload](../computer-science/High_Level_Design.md#3-estimate-the-workload) · [Architecture Building Blocks](../computer-science/High_Level_Design.md#4-architecture-building-blocks) · [Evaluation Rubric by Level](HLD_Mock_Interviews.md#3-evaluation-rubric-by-level) · [LLD Practice Problems](LLD_Practice_Problems.md)

## Table of Contents

1. [How to Use This File](#1-how-to-use-this-file)
2. [Problem Index](#2-problem-index)
3. [Problems](#3-problems)
   - [P1. Distributed Message Queue](#p1-distributed-message-queue)
   - [P2. Collaborative Document Editor](#p2-collaborative-document-editor)
   - [P3. File Sync Service (Dropbox)](#p3-file-sync-service-dropbox)
   - [P4. Photo Sharing Service (Instagram)](#p4-photo-sharing-service-instagram)
   - [P5. Real-Time Leaderboard](#p5-real-time-leaderboard)
   - [P6. Ad-Click Aggregation](#p6-ad-click-aggregation)
   - [P7. Distributed Cache Service](#p7-distributed-cache-service)
   - [P8. Nearby Places (Yelp)](#p8-nearby-places-yelp)
   - [P9. Stock Exchange Matching Engine](#p9-stock-exchange-matching-engine)
   - [P10. Online Coding Judge](#p10-online-coding-judge)
   - [P11. Live Comments and Reactions](#p11-live-comments-and-reactions)
   - [P12. Vacation Rental Marketplace (Airbnb)](#p12-vacation-rental-marketplace-airbnb)
   - [P13. Flash Sale Checkout](#p13-flash-sale-checkout)
   - [P14. Maps and Navigation](#p14-maps-and-navigation)
   - [P15. Video Conferencing (Zoom)](#p15-video-conferencing-zoom)
   - [P16. Top-K Trending Topics](#p16-top-k-trending-topics)
   - [P17. Distributed Lock Service](#p17-distributed-lock-service)
   - [P18. Web Search Engine](#p18-web-search-engine)
   - [P19. Email Service (Gmail)](#p19-email-service-gmail)
   - [P20. Food Delivery Platform (DoorDash)](#p20-food-delivery-platform-doordash)
- [Answers](#answers)
   - [A1. Distributed Message Queue](#a1-distributed-message-queue)
   - [A2. Collaborative Document Editor](#a2-collaborative-document-editor)
   - [A3. File Sync Service (Dropbox)](#a3-file-sync-service-dropbox)
   - [A4. Photo Sharing Service (Instagram)](#a4-photo-sharing-service-instagram)
   - [A5. Real-Time Leaderboard](#a5-real-time-leaderboard)
   - [A6. Ad-Click Aggregation](#a6-ad-click-aggregation)
   - [A7. Distributed Cache Service](#a7-distributed-cache-service)
   - [A8. Nearby Places (Yelp)](#a8-nearby-places-yelp)
   - [A9. Stock Exchange Matching Engine](#a9-stock-exchange-matching-engine)
   - [A10. Online Coding Judge](#a10-online-coding-judge)
   - [A11. Live Comments and Reactions](#a11-live-comments-and-reactions)
   - [A12. Vacation Rental Marketplace (Airbnb)](#a12-vacation-rental-marketplace-airbnb)
   - [A13. Flash Sale Checkout](#a13-flash-sale-checkout)
   - [A14. Maps and Navigation](#a14-maps-and-navigation)
   - [A15. Video Conferencing (Zoom)](#a15-video-conferencing-zoom)
   - [A16. Top-K Trending Topics](#a16-top-k-trending-topics)
   - [A17. Distributed Lock Service](#a17-distributed-lock-service)
   - [A18. Web Search Engine](#a18-web-search-engine)
   - [A19. Email Service (Gmail)](#a19-email-service-gmail)
   - [A20. Food Delivery Platform (DoorDash)](#a20-food-delivery-platform-doordash)

---

## 1. How to Use This File

1. **Read only the problem statement.** Run the [45-minute self-mock](HLD_Mock_Interviews.md#2-running-a-45-minute-self-mock) out loud on a blank whiteboard or document. Ask the clarifying questions from the table yourself and use the "typical answer" column as the interviewer's reply.
2. **Write the capacity block before drawing boxes.** Every answer here starts from numbers and states which number drove which component. If your estimate differs by more than 10x, find out why before reading on.
3. **Compare, do not copy.** Open the answer only after your attempt. Check that you hit each item in "What the interviewer is actually grading", then read the deep dives. A different design is fine if you can defend it against the answer's tradeoff table.
4. **Answer the follow-ups out loud before reading the model answers.** Follow-ups are where most hire/no-hire decisions are made.
5. **Score yourself** with the [rubric by level](HLD_Mock_Interviews.md#3-evaluation-rubric-by-level) and the "Level signals" at the end of each answer, and log the misses in the [post-mock error log](HLD_Mock_Interviews.md#25-post-mock-review-and-error-log).
6. **Repeat after 7 and 21 days.** The second attempt should finish the core design by minute 18, leaving time for two deep dives.

Suggested order by target role:

| Target role | Start with | Then | Stretch |
|---|---|---|---|
| General big-tech SWE | 4 photo sharing, 3 file sync, 8 nearby places | 11 live comments, 12 Airbnb, 13 flash sale, 19 email | 2 collaborative editor, 14 maps |
| Systems C++ / infrastructure | 7 distributed cache, 1 message queue | 17 lock service, 9 stock exchange, 18 search engine | 6 ad-click aggregation |
| GPU / HPC (AMD, NVIDIA, labs) | 1 message queue, 16 top-K trending | 7 distributed cache, 10 coding judge (sandboxing and burst scheduling) | 9 stock exchange (latency budgets) |
| ML infrastructure | 6 ad-click aggregation, 16 top-K trending | 18 search engine (ranking), 20 food delivery (dispatch and ETA) | 14 maps (ETA prediction) |

---

## 2. Problem Index

| # | Problem | Focus | Difficulty | Source |
|---|---|---|---|---|
| [P1](#p1-distributed-message-queue) | Distributed Message Queue | Partitioned replicated log, ISR and high watermark, consumer groups, exactly-once | Hard | [Mock prompt P1](HLD_Mock_Interviews.md#a1-distributed-message-queue) |
| [P2](#p2-collaborative-document-editor) | Collaborative Document Editor | OT vs CRDT, per-document session ownership, offline merge | Hard | [Mock prompt P2](HLD_Mock_Interviews.md#a2-collaborative-document-editor) |
| [P3](#p3-file-sync-service-dropbox) | File Sync Service (Dropbox) | Content-defined chunking, dedupe, metadata journal, conflicts | Medium | [Mock prompt P3](HLD_Mock_Interviews.md#a3-file-sync-dropbox) |
| [P4](#p4-photo-sharing-service-instagram) | Photo Sharing Service (Instagram) | Async image pipeline, CDN and storage tiering, privacy at the CDN | Medium | [Mock prompt P4](HLD_Mock_Interviews.md#a4-photo-sharing-with-image-processing) |
| [P5](#p5-real-time-leaderboard) | Real-Time Leaderboard | Sharded ranking, approximate rank, windows, tie-breaking | Medium | [Mock prompt P5](HLD_Mock_Interviews.md#a5-real-time-leaderboard) |
| [P6](#p6-ad-click-aggregation) | Ad-Click Aggregation | Event-time windows, dedupe, exactly-once end to end, reconciliation | Hard | [Mock prompt P6](HLD_Mock_Interviews.md#a6-ad-click-aggregation-exactly-once) |
| [P7](#p7-distributed-cache-service) | Distributed Cache Service | Consistent hashing, failover, slab memory, invalidation leases | Medium | [Mock prompt P7](HLD_Mock_Interviews.md#a7-distributed-cache-service) |
| [P8](#p8-nearby-places-yelp) | Nearby Places (Yelp) | Geospatial index, in-memory replicated index, ranking | Medium | [Mock prompt P9](HLD_Mock_Interviews.md#a9-nearby-places) |
| [P9](#p9-stock-exchange-matching-engine) | Stock Exchange Matching Engine | Sequencer, deterministic replay, microsecond latency, market data | Hard | [Mock prompt P10](HLD_Mock_Interviews.md#a10-stock-exchange-matching-engine) |
| [P10](#p10-online-coding-judge) | Online Coding Judge | Sandboxing, CPU-time measurement, burst scheduling, rejudge | Medium | [Mock prompt P14](HLD_Mock_Interviews.md#a14-online-coding-judge) |
| [P11](#p11-live-comments-and-reactions) | Live Comments and Reactions | Massive fan-out, connection tier, sampling, aggregation | Hard | [Mock prompt P15](HLD_Mock_Interviews.md#a15-live-comments-and-reactions-for-10m-viewers) |
| [P12](#p12-vacation-rental-marketplace-airbnb) | Vacation Rental Marketplace (Airbnb) | Geo plus availability search, range booking, payment holds | Hard | New |
| [P13](#p13-flash-sale-checkout) | Flash Sale Checkout | Hot inventory counters, admission control, async orders | Hard | New |
| [P14](#p14-maps-and-navigation) | Maps and Navigation | Tile pyramids, contraction hierarchies and CRP, live traffic, ETA | Hard | New |
| [P15](#p15-video-conferencing-zoom) | Video Conferencing (Zoom) | SFU topology, simulcast and SVC, NAT traversal, cascading | Hard | New |
| [P16](#p16-top-k-trending-topics) | Top-K Trending Topics | Heavy hitters, sliding windows, two-stage aggregation | Medium | New |
| [P17](#p17-distributed-lock-service) | Distributed Lock Service | Consensus, sessions and leases, fencing, linearizable reads | Hard | New |
| [P18](#p18-web-search-engine) | Web Search Engine | Inverted index, document sharding, posting compression, ranking | Hard | New |
| [P19](#p19-email-service-gmail) | Email Service (Gmail) | SMTP store-and-forward, spam filtering, per-user storage, sync | Hard | New |
| [P20](#p20-food-delivery-platform-doordash) | Food Delivery Platform (DoorDash) | Saga across services, batched dispatch, ETA prediction | Hard | New |

---

## 3. Problems

Read one problem, then close the file and run the mock. Each problem links to its answer.

### P1. Distributed Message Queue

**Difficulty:** Hard · **Focus:** partitioned replicated log, ISR and high watermark, consumer groups, delivery semantics, storage layout · **Related reading:** [Queues and event streams](../computer-science/High_Level_Design.md#44-queues-and-event-streams), [Replication Strategies](../computer-science/CS_Fundamentals.md#83-replication-strategies), [Split Brain, Leases, and Fencing](../computer-science/CS_Fundamentals.md#813-consistency-guarantees-split-brain-leases-and-fencing)

> "Design a distributed message queue, really a durable partitioned log like Kafka. It must ingest 1 GB/s, keep data for a week, and serve many independent consumer groups that each read at their own pace."

**What the interviewer is actually grading:**
- Choosing the **log abstraction** (append-only, consumers track offsets) over a delete-on-ack work queue, and explaining why it makes many consumer groups cheap.
- A replication protocol you can defend under failure: in-sync replica set, high watermark, `acks=all` with a minimum ISR size, leader epochs, and what **unclean leader election** costs.
- Throughput reasoning from disk and network numbers: replication factor multiplies writes, consumer fan-out multiplies reads, and page cache plus zero-copy is why reads are cheap.
- Consumer-group mechanics: partition assignment, offset commits, generation IDs that fence zombies, and the cost of rebalancing.
- Precise delivery semantics: at-least-once by default, and what "exactly-once" really covers (idempotent producer, transactions, read-committed consumers) and does not cover (external side effects).
- Trap: promising global ordering, or "every message is fsynced before ack" as the durability story. Ordering is per partition, and durability comes from replication across failure domains.

**Clarifying questions to ask:**

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| What ordering is required? | Per key (for example per user or per order), not global | Partition by key; one partition is the unit of order and of consumer parallelism |
| Retention: time, size, or forever by key? | 7 days for event topics; some keyed topics keep the latest value forever | Time retention deletes whole segments; "latest per key" needs log compaction |
| Message size and rate? | ~1 KB average, 1 GB/s average, 2x peak | ~1M msgs/s; sets partition count, broker count, and batching |
| How many consumer groups, and do they read the tail or replay? | 5-10 groups on the tail; occasional full replays | Egress dominates; replays read cold data from disk and can evict the page cache |
| Can an acknowledged message ever be lost? | No, for acknowledged writes, even if one AZ fails | RF=3 across AZs, `acks=all`, `min.insync.replicas=2`, no unclean election |
| Delivery semantics? | At-least-once; exactly-once for stream-processing pipelines | Idempotent producer by default; transactions only where needed |
| Single region or multi-region? | One region, three AZs; DR copy in a second region | Synchronous replication inside the region, asynchronous mirroring across regions |

Solution: [A1](#a1-distributed-message-queue)

---

### P2. Collaborative Document Editor

**Difficulty:** Hard · **Focus:** OT vs CRDT, per-document session ownership, op log and snapshots, offline merge, presence · **Related reading:** [Chat System](../computer-science/High_Level_Design.md#64-chat-system), [Event Sourcing and the Outbox](../computer-science/High_Level_Design.md#412-change-data-capture-event-sourcing-cqrs-and-the-outbox), [Split Brain, Leases, and Fencing](../computer-science/CS_Fundamentals.md#813-consistency-guarantees-split-brain-leases-and-fencing)

> "Design a collaborative document editor like Google Docs. Many people edit the same document at the same time and see each other's changes and cursors live. People can also keep editing on a plane and merge when they land."

**What the interviewer is actually grading:**
- Recognizing that the **document session**, not the operation, is the scaling unit: per-document throughput is tiny, so one owner process can order all edits.
- A concrete concurrency-control algorithm: you can transform two concurrent inserts by hand (OT), or explain unique position identifiers and tombstones (CRDT), and say when each wins.
- Durability and ordering: an op is acknowledged only after it is durably appended, revisions are assigned by one owner, and a failed-over owner is **fenced** so two servers never assign the same revision.
- Snapshots plus an op log so that opening a document does not replay years of keystrokes, and version history falls out of the log.
- Offline editing that converges without silent loss, plus presence and permissions that change while a session is open.
- Trap: last-writer-wins on the whole document, paragraph locking, or "store the document in a database row and save every keystroke with an UPDATE".

**Clarifying questions to ask:**

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| How many simultaneous editors per document? | Usually 1-5; cap at 100 editors, thousands of viewers | One session owner per document is enough; viewers need a separate fan-out path |
| Plain text or rich text (styles, tables, images)? | Rich text | Operations need attributes and structure; CRDT rich text is harder (formatting spans) |
| Offline editing: how long? | Hours to a few days | Long divergence favors CRDT or requires composing server history before transforming |
| Version history and restore? | Yes, browsable history with named versions | The op log is kept and compacted, not discarded after snapshotting |
| Latency target for remote edits? | Visible to others within ~200 ms in-region | WebSocket push from the session owner; group commit of a few ms is acceptable |
| Permissions model? | Owner, editor, commenter, viewer; link sharing; revocation takes effect quickly | ACL checked at join and enforced per op; revocation must reach open sessions |
| Peer-to-peer or always through a server? | Always through a server | Central ordering makes OT practical and simplifies correctness |

Solution: [A2](#a2-collaborative-document-editor)

---

### P3. File Sync Service (Dropbox)

**Difficulty:** Medium · **Focus:** content-defined chunking, dedupe, metadata journal and cursors, sync protocol, conflicts, direct-to-storage uploads · **Related reading:** [Object Storage (S3-like)](../computer-science/High_Level_Design.md#614-object-storage-s3-like), [Notification System](../computer-science/High_Level_Design.md#611-notification-system), [Bloom Filters and Merkle Trees](../computer-science/High_Level_Design.md#49-bloom-filters-and-merkle-trees)

> "Design a file sync service like Dropbox. A user has a folder on their laptop, phone, and work desktop; any change on one device shows up on the others, and folders can be shared with other people."

**What the interviewer is actually grading:**
- **Separating metadata from bytes:** blocks addressed by content hash in object storage, and a strongly consistent metadata service that records which blocks make up which file version.
- Chunking that keeps uploads proportional to the change: why fixed-size blocks re-upload everything after an insertion, and how content-defined chunking fixes it, with numbers.
- A sync protocol that scales to hundreds of millions of devices: an ordered **per-namespace journal**, a client cursor, a cheap "something changed" notification, and a delta fetch.
- A commit protocol that never loses data: upload blocks first, then commit metadata with a version check; concurrent edits produce a **conflicted copy**, not a silent overwrite.
- Bandwidth and cost awareness: dedupe ratio, delta transfer, LAN sync, and keeping app servers out of the byte path with presigned URLs.
- Trap: storing file bytes in the metadata database, re-uploading whole files on every save, or granting access to a block just because the client knows its hash.

**Clarifying questions to ask:**

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| How many users, devices, and how much data? | 100M active users, ~3 devices each, ~5 GB per user | ~500 PB logical; dedupe and storage tiering matter; metadata is tens of TB |
| File size distribution and edit pattern? | Mostly small files; some multi-GB files edited in place | Chunking and delta sync for large files; batching for many small files |
| Shared folders? How many members? | Yes; usually a few, sometimes thousands | A shared folder is its own namespace with its own journal; fan-out of notifications |
| Version history? | 30 days of versions, restore deleted files | Old block lists and blocks are retained; garbage collection is reference-counted |
| Conflict policy? | Never lose a user's bytes; no automatic merge of file contents | Conflicted copies; the server rejects a commit whose parent version is stale |
| How fast must a change appear on other devices? | Seconds when online | Long-poll or push notifications plus delta fetch, not periodic full listing |
| Client-side encryption required? | No (server can read content for previews and search) | Allows cross-user dedupe and server-side previews; end-to-end encryption would not |

Solution: [A3](#a3-file-sync-service-dropbox)

---

### P4. Photo Sharing Service (Instagram)

**Difficulty:** Medium · **Focus:** presigned uploads, async image pipeline, CDN and storage tiering, privacy at the CDN, hot counters · **Related reading:** [News Feed](../computer-science/High_Level_Design.md#63-news-feed), [Object Storage (S3-like)](../computer-science/High_Level_Design.md#614-object-storage-s3-like), [Cache Stampede and Hot Keys](../computer-science/High_Level_Design.md#413-cache-stampede-and-hot-keys)

> "Design a photo-sharing service like Instagram. Users upload photos, which show up in their followers' feeds; accounts can be private; people like and comment on posts."

**What the interviewer is actually grading:**
- An upload path that keeps bytes off application servers (presigned, resumable uploads) and processes images **asynchronously and idempotently**: validation, EXIF stripping, multiple resolutions, moderation.
- Storage and CDN reasoning with numbers: originals vs derivatives, egress, CDN hit ratio, and **tiering cost math** that shows where the money goes.
- Reusing the news-feed design rather than re-deriving it, and spending the time on what is specific to photos.
- Privacy enforced at **read time** and at the **CDN** (signed, expiring URLs) without destroying the cache hit ratio, and a clear statement of how long revocation takes.
- Like and comment counters that survive a celebrity post: idempotent likes, sharded or batched counters, approximate display counts, and hot-key handling.
- Trap: streaming image bytes through the API tier, resizing synchronously inside the upload request, or serving private photos from permanent public CDN URLs.

**Clarifying questions to ask:**

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| Uploads per day and average photo size? | 100M/day, ~3 MB original | ~300 TB/day of originals; storage cost is a first-order concern |
| DAU and images viewed per user per day? | 500M DAU, ~100 images each | ~50B image views/day; egress and CDN hit ratio dominate serving cost |
| Which sizes do clients need? | Thumbnail, feed, and full-screen sizes; modern formats where supported | Precompute 3-4 derivatives; rare sizes on demand at an image proxy |
| Privacy model? | Public or private accounts; blocks; close-friends audiences | Read-time authorization; signed URLs for non-public media |
| How fast must a deletion or privacy change take effect? | Within minutes; legal takedowns faster | Bounds signed-URL lifetime and requires a CDN purge path |
| Must like counts be exact? | Exact for the liker ("you liked this"); display count may lag seconds | Unique (post, user) like rows for truth; aggregated counters for display |
| Moderation requirements? | Block known illegal content before it is visible; classifier review for the rest | Hash matching is synchronous in the pipeline, before the post becomes visible |

Solution: [A4](#a4-photo-sharing-service-instagram)

---

### P5. Real-Time Leaderboard

**Difficulty:** Medium · **Focus:** sorted sets, sharded ranking, approximate rank from histograms, windows, tie-breaking, anti-cheat · **Related reading:** [Partitioning and replication](../computer-science/High_Level_Design.md#45-partitioning-and-replication), [Cache Stampede and Hot Keys](../computer-science/High_Level_Design.md#413-cache-stampede-and-hot-keys), [Probabilistic Counting](../computer-science/High_Level_Design.md#410-probabilistic-counting-hyperloglog-and-count-min-sketch)

> "Design a real-time leaderboard for a game with 100M players. Show the global top 100, and let any player ask 'what is my rank?' and see it update right after a match. We also want daily, weekly, and seasonal boards and a friends leaderboard."

**What the interviewer is actually grading:**
- Knowing the right data structure (a sorted set, a skip list with O(log n) rank) and then showing, with numbers, **why one sorted set on one node is not enough** for 100M players at a high write rate across several boards.
- Two sharding strategies and their real costs: by user (cheap writes, scatter-gather rank) vs by score range (local rank plus counts of higher shards, but skew and boundary moves).
- Separating **exact top-K** from **approximate or bucketed rank for everyone else**, and stating the error.
- Deterministic tie-breaking and window handling (daily, weekly, seasonal resets, late events, final snapshots).
- A validation path so that a cheater cannot write a fabricated score into the top 100, plus a durable source of truth so the in-memory boards can be rebuilt.
- Trap: `SELECT COUNT(*) FROM scores WHERE score > ?` or `ORDER BY score` over 100M rows per request, or accepting scores posted directly by game clients.

**Clarifying questions to ask:**

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| Score update rate? | ~100k/s average, ~300k/s peak during events | Multiplied by the number of boards each update touches; decides sharding |
| Exact rank for everyone, or exact only near the top? | Exact top 1,000; "rank ~4,213,000 (top 5%)" is fine for others | Allows a small exact top tier plus histogram-based rank |
| How fresh must rank be? | Own score immediately; rank within a few seconds | Rank can be computed from periodically merged counts |
| Score semantics: best-ever, cumulative, or latest? | Cumulative within a window; best-ever for all-time | Changes update logic (ZINCRBY vs ZADD GT) and how windows reset |
| How are ties ordered? | Earlier achiever ranks higher | Composite score encoding or a secondary sort key |
| Where do scores come from? | Authoritative game servers report match results | Clients never write scores; server-side validation before top-tier entry |
| Friends per player? | Up to a few hundred, capped at 5,000 | Friends board computed on read from a few hundred point lookups |

Solution: [A5](#a5-real-time-leaderboard)

---

### P6. Ad-Click Aggregation

**Difficulty:** Hard · **Focus:** Event-time stream processing, dedupe, exactly-once end to end, late data, reconciliation · **Related reading:** [HLD 4.11 Stream Processing](../computer-science/High_Level_Design.md#411-stream-processing), [HLD 4.12 CDC and the Outbox](../computer-science/High_Level_Design.md#412-change-data-capture-event-sourcing-cqrs-and-the-outbox), [Mock hint A6](HLD_Mock_Interviews.md#a6-ad-click-aggregation-exactly-once)

> "We serve ads and bill advertisers per click. Design the pipeline that turns raw click events into per-ad, per-minute click counts. Advertisers watch these numbers on a dashboard and we invoice from them, so they must be exact."

**What the interviewer is actually grading:**
- Defining "exact": what counts as one billable click (transport retries vs a user double-clicking), and a dedupe key that enforces that definition.
- Event-time windows with watermarks, and a concrete, tiered policy for late events that reaches the bill without rewriting closed invoices.
- An end-to-end exactly-once argument that covers every hop: producer, log, operator state, and sink. "Kafka has exactly-once" is not an argument.
- A reconciliation path from an immutable raw archive, and a clear statement of which number is the billing source of truth.
- Hot ads and the query store: pre-aggregation before the shuffle, and a columnar store sized from the row count.
- Trap: `UPDATE ad SET clicks = clicks + 1` per click, or deduplicating against an external store (Redis) that is not rolled back when the stream job restores a checkpoint.

**Clarifying questions to ask:**

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| Click volume and peak? | 1B clicks/day, peaks around 50k/s | Ingress is small (MB/s); the design is driven by correctness, not throughput |
| What is one billable click? | At most one per ad impression; retries and double clicks count once | Dedupe on impression ID, not only click ID, and the state horizon that implies |
| How fresh must the dashboard be? How final must the bill be? | Dashboard within about a minute; invoice closes daily at T+1 | Separates the fast stream path from the authoritative batch path |
| How late can events arrive? | Most within seconds; edge outages can delay some by hours | Watermark delay, allowed lateness, and the side-output-to-batch tier |
| Is fraud (invalid traffic) filtered? Synchronously? | Simple rules inline; click-farm detection hours later | Late fraud verdicts become corrections and invoice adjustments |
| Query patterns and retention? | Per-minute for 90 days, hourly and daily for years; filter by advertiser and ad | OLAP store with rollups; partition and sort keys |
| Multiple regions? | Click edges in every region | Where dedupe and aggregation run, and what happens when a region is cut off |

Solution: [A6](#a6-ad-click-aggregation)

---

### P7. Distributed Cache Service

**Difficulty:** Medium · **Focus:** Consistent hashing and routing, replication and failover, slab memory management, invalidation races and leases, multi-tenancy · **Related reading:** [HLD 4.13 Cache Stampede and Hot Keys](../computer-science/High_Level_Design.md#413-cache-stampede-and-hot-keys), [HLD 6.8 Distributed Key-Value Store](../computer-science/High_Level_Design.md#68-distributed-key-value-store), [Mock hint A7](HLD_Mock_Interviews.md#a7-distributed-cache-service)

> "Hundreds of internal services each run their own little Redis or memcached cluster, and it is a mess. Design a shared, multi-tenant distributed cache service that all of them can use."

**What the interviewer is actually grading:**
- Sizing from memory and from ops/s separately, and noticing which one sizes the cluster.
- Routing: consistent hashing, where it runs (client library, proxy, or server redirect), and how a cluster map change reaches 20k clients safely.
- What happens to the backing databases when a node, or a whole zone, of cache disappears, with the extra load computed.
- Memory efficiency: per-item overhead, slab classes, fragmentation, and eviction that does not let a scan flush the hot set.
- Consistency with the database: the cache-aside stale-set race, why writers delete instead of set, and how leases or a CDC-driven invalidation stream close the gaps.
- Trap: "write-through keeps the cache consistent", or letting a node that was down rejoin with its old contents.

**Clarifying questions to ask:**

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| Aggregate ops/s and read/write mix? | About 10M ops/s at peak, 90% reads | Node count by throughput; per-node headroom for hot keys |
| Total working set and item sizes? | About 20 TB; median value 300 B, a long tail up to 1 MB | Node count by memory; slab classes; large-value limits |
| May the cache lose data? | Yes, it is a cache; but some tenants' databases cannot absorb a cold cache | Replication only for pools whose backing store needs it |
| Staleness tolerance after a database write? | Seconds, never indefinitely | Delete-on-write plus a reliable CDC invalidation path and leases |
| Multi-tenant isolation requirements? | Quotas per team; one tenant must not evict another's data | Per-tenant pools, rate limits, and per-tenant metrics |
| Multiple regions? | Three regions, each with a local database replica | Per-region clusters, invalidation from each region's replication stream |
| Client languages and lifetimes? | Long-lived Go, Java, and C++ services, plus short-lived jobs and scripts | Smart client library vs a proxy tier |

Solution: [A7](#a7-distributed-cache-service)

---

### P8. Nearby Places (Yelp)

**Difficulty:** Medium · **Focus:** Geospatial indexing, in-memory replicated index, ranking, text plus geo search, update propagation · **Related reading:** [HLD 4.8 Geospatial Indexing](../computer-science/High_Level_Design.md#48-geospatial-indexing), [HLD 6.6 Ride-Sharing Service](../computer-science/High_Level_Design.md#66-ride-sharing-service), [Mock hint A9](HLD_Mock_Interviews.md#a9-nearby-places)

> "Design the backend for a Yelp-style app. Given the user's location, return the best places within a radius, optionally filtered by category, price, 'open now', or a text query like 'ramen'. Users also write reviews and upload photos."

**What the interviewer is actually grading:**
- Choosing a geospatial index for the access pattern (static points, read-heavy) and computing its size, which leads to replicating it in memory rather than sharding it.
- Handling the edge cases of cell-based search: neighbor cells, over-fetch ratio, dense downtowns, large radii.
- A ranking function that is defensible: distance, a rating that does not let a single 5-star review win, review count, and "open now" done correctly across time zones.
- How place edits, new reviews, and rating changes reach the index, with a stated freshness.
- Combining text relevance with a geo filter without scanning the world.
- Trap: `SELECT ... WHERE lat BETWEEN ... AND lng BETWEEN ... ORDER BY rating` on a B-tree, or computing the distance to every place.

**Clarifying questions to ask:**

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| How many places, and how fast do they change? | 200M places worldwide; about 100k new or edited per day | Index size; updates can be minutes-fresh, so no transactional index |
| Search QPS and latency target? | 100k searches/s at peak; p99 under 200 ms server-side | CPU per query decides the number of index replicas |
| Radius range? | Default 2 km, maximum 25 km | Cell levels for the covering; precomputed top lists for large radii |
| What does "best" mean? | Rating, review count, distance; sponsored results are separate | Ranking features to keep in the index |
| Is text search required? | Yes: names, categories, dish keywords | A text index with a geo filter, sharded by region |
| Freshness of reviews and ratings? | A new review should affect the rating within minutes | Asynchronous aggregation through an outbox |
| Moving places (food trucks)? | Out of scope for v1 | If in scope, use the moving-object design from ride-sharing |

Solution: [A8](#a8-nearby-places-yelp)

---

### P9. Stock Exchange Matching Engine

**Difficulty:** Hard · **Focus:** Sequencing, deterministic state machine replication, microsecond latency, market data fan-out, pre-trade risk · **Related reading:** [CS 8.13 Leases and Fencing](../computer-science/CS_Fundamentals.md#813-consistency-guarantees-split-brain-leases-and-fencing), [Kernel Bypass](../computer-science/CS_Fundamentals.md#why-the-kernel-network-stack-is-too-slow-and-kernel-bypass), [LLD A7 Order Book](LLD_Practice_Problems.md#a7-order-book-matching-engine)

> "Design the core of a stock exchange: members send buy and sell orders, we match them with price-time priority, send execution reports back, and publish market data. Latency is measured in microseconds."

**What the interviewer is actually grading:**
- Recognizing that the matching engine is a deterministic, single-threaded state machine per symbol, and that a sequenced input log is both the source of truth and the replication mechanism.
- A latency budget in microseconds, per hop, and the engineering that keeps the tail flat (kernel bypass, pinned cores, no allocation or locks on the hot path).
- Failover without losing or duplicating executions: hot standby by replay, fencing of the old primary, and idempotent outputs.
- Market data distribution to thousands of subscribers: multicast, sequence numbers, gap recovery, and snapshot plus incremental for late joiners.
- Pre-trade risk and fairness: where checks run, what they cost, and what "fair" means at microsecond scale.
- Trap: a database transaction per order, a multi-threaded matcher with locks on the book, or reading the wall clock inside the matcher.

**Clarifying questions to ask:**

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| Message rate, overall and for the hottest symbol? | 1M messages/s overall; about 100k/s for the busiest symbol | Per-core budget per message; how symbols are spread over engines |
| Latency target? | Order in to acknowledgment out: p50 about 20 µs, p99 under 100 µs | Kernel bypass, no disk fsync on the critical path, single fabric hops |
| Order types? | Limit, market, IOC, cancel, cancel/replace | Book operations; which modifications keep time priority |
| Durability requirement? | No acknowledged order or execution may be lost | Replicate the sequenced log before acting on it |
| Market data consumers? | Thousands of colocated subscribers plus delayed retail feeds | UDP multicast with A/B feeds; a separate conflated tier |
| Auctions, clearing, settlement? | Settlement out of scope; auctions are a follow-up | Keep the core to continuous trading; outputs feed clearing |
| Cross-symbol orders? | Not in v1 | If needed, related instruments must live in one engine partition |

Solution: [A9](#a9-stock-exchange-matching-engine)

---

### P10. Online Coding Judge

**Difficulty:** Medium · **Focus:** Sandboxing untrusted code, CPU-time measurement, job queues with priorities, burst capacity, rejudge consistency · **Related reading:** [Containers 2.3 Capabilities, seccomp, and Rootless](../tools/Containers_and_CI.md#23-capabilities-seccomp-and-rootless), [CS 1.13 Containers and Virtualization](../computer-science/CS_Fundamentals.md#113-containers-and-virtualization-isolation-theory), [HLD 6.12 Distributed Job Scheduler](../computer-science/High_Level_Design.md#612-distributed-job-scheduler)

> "Design an online judge like LeetCode. Users submit code in any of about 20 languages; we compile it, run it against hidden test cases with time and memory limits, and return a verdict. We also host weekly contests."

**What the interviewer is actually grading:**
- A threat model for hostile code and layered isolation: namespaces, cgroups, a seccomp allowlist, no network, and when a microVM boundary is worth its cost.
- Time limits that are fair and reproducible: CPU time vs wall time, pinned cores, frequency control, and what to do near the limit.
- A judging pipeline with leases and idempotent verdict writes, test data cached on workers and never visible to the submission.
- Capacity math for a contest spike of about 10x, and a plan that pre-scales rather than reacting.
- Rejudging and verdict history, so that a fixed test case or a compiler change does not silently rewrite contest results.
- Trap: running submissions in the API servers or in a plain Docker container with the default profile, or using wall-clock time limits on a shared host.

**Clarifying questions to ask:**

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| Submission volume, normal and contest? | 2M/day normally; a contest brings about 10x the normal peak for an hour | Pool size and pre-scaling schedule |
| Languages and limits? | About 20 languages; typical 1-2 s and 256 MB, with per-language multipliers | Per-language images, warm pools, and limit calibration |
| Verdict latency target? | p95 under 15 s in practice; under 30 s queue wait during contests | Priority lanes and admission control |
| Does contest rank depend on judge time? | No: rank uses submission time | Queue delay hurts feedback, not ranking |
| Custom input "Run" as well as "Submit"? | Yes, and it is the majority of requests | Separate, lower-priority lane; sheddable during contests |
| Interactive or special-checker problems? | Some problems use a custom checker or an interactor | The checker is also sandboxed; two-process pipes |
| Plagiarism checks? | After each contest | Offline fingerprinting job, not in the judging path |

Solution: [A10](#a10-online-coding-judge)

---

### P11. Live Comments and Reactions

**Difficulty:** Hard · **Focus:** massive fan-out, connection tier, sampling, aggregation, backpressure · **Related reading:** [HLD 6.4 Chat System](../computer-science/High_Level_Design.md#64-chat-system), [HLD 5.8 Backpressure and Load Shedding](../computer-science/High_Level_Design.md#58-backpressure-and-load-shedding), [Mock hint A15](HLD_Mock_Interviews.md#a15-live-comments-and-reactions-for-10m-viewers)

> "Design live comments and reactions for a single live stream with 10 million concurrent viewers, like a World Cup final. Viewers can post comments and tap reactions, and everyone should feel the room."

**What the interviewer is actually grading:**
- The arithmetic that kills the naive design: every comment to every viewer is about 1e11 deliveries per second, and no human can read 10,000 comments per second anyway.
- A hierarchical fan-out (origin, relays, edge gateways) where a message is published once per gateway, and the per-viewer cost is paid only at the last hop.
- Sampling and ranking as a first-class component with a stated policy, and reactions aggregated into per-second counts rather than forwarded one by one.
- Slow-client handling: bounded per-connection buffers that drop stale batches instead of queueing.
- Moderation placed so that it is cheap on the write path but strict on what is actually displayed, plus replay for late joiners and VOD.
- Trap: one broker queue or topic subscription per viewer, or "put it in Kafka and have every client consume", which multiplies the broker load by 10 million.

**Clarifying questions to ask:**

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| Must every viewer see every comment? | No; viewers should see a representative, fresh, safe sample, plus their own and their friends' comments | Turns an impossible broadcast into a sampling problem |
| Peak comment and reaction rates? | Comments: 10k/s peak after a goal; reactions: up to 1M taps/s | Sizes ingest, moderation, and the aggregation layer |
| Latency target from post to display? | Under 2-3 s for others; own comment appears instantly | Allows 200-500 ms batching at each hop |
| Are comments persisted and shown on the VOD afterward? | Yes, synchronized to video time | Comments need a media timestamp, not just wall-clock time |
| Moderation requirements? | No slurs or spam on screen; legal takedowns within minutes | Synchronous cheap filter, stricter check on the displayed sample, retraction messages |
| Languages and regions? | Global audience, dozens of languages | Segment the sampled lanes by language and region |
| One giant stream or many streams? | Both: one 10M-viewer event plus thousands of small streams | Gateways subscribe per stream; small streams can deliver every comment |

Solution: [A11](#a11-live-comments-and-reactions)

---

### P12. Vacation Rental Marketplace (Airbnb)

**Difficulty:** Hard · **Focus:** geo plus date-availability search, range booking without double booking, payment holds and payouts, state machines · **Related reading:** [HLD 4.8 Geospatial Indexing](../computer-science/High_Level_Design.md#48-geospatial-indexing), [HLD 6.15 Ticket Booking](../computer-science/High_Level_Design.md#615-ticket-booking-seat-reservation), [HLD 6.7 Payment Processing](../computer-science/High_Level_Design.md#67-payment-processing)

> "Design a vacation rental marketplace like Airbnb. Guests search for places to stay by location, dates, and price, then book. Hosts manage their listings and calendars and get paid."

**What the interviewer is actually grading:**
- A search design that combines geography with **date-range availability**, and an honest answer to "how fresh is availability in the search index?"
- An availability representation sized with numbers (per-listing calendar bitmaps fit in memory) and a fast range check.
- Booking that can never double-book a night: conditional writes on per-night rows or a range exclusion constraint, in one single-partition transaction.
- The booking state machine for instant book versus request-to-book, with timeouts, and how payment authorization, capture, refunds, and delayed host payout fit into it.
- Integration edges: external iCal calendars, reviews gated on completed stays, price quotes that do not change under the guest.
- Trap: treating it as the ticket booking problem. Contention per listing is tiny; the hard parts are search over availability and the long-lived money flow, not a hot partition.

**Clarifying questions to ask:**

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| How many listings and how far ahead can guests book? | ~7M active listings; up to 2 years ahead | Sizes the availability index (listing x night) |
| Search and booking volume? | ~100M searches/day; ~300k bookings/day | Look-to-book of ~300:1: optimize the read path, writes are small |
| Instant book, request-to-book, or both? | Both, chosen per listing; host has 24 h to respond | Two booking state machines; whether a pending request blocks dates |
| When is the guest charged and the host paid? | Guest charged at booking; host paid ~24 h after check-in | Platform holds funds for weeks; needs a ledger and scheduled payouts |
| Do hosts list on other platforms? | Yes, many sync calendars via iCal | External blocks arrive late; cross-platform double booking is possible |
| How fresh must search availability be? | Seconds to a minute is fine; booking must be exact | Search index is eventually consistent; booking re-checks the source of truth |
| Reviews? | Both sides review after checkout, revealed together | Eligibility tied to a completed reservation; double-blind reveal |

Solution: [A12](#a12-vacation-rental-marketplace-airbnb)

---

### P13. Flash Sale Checkout

**Difficulty:** Hard · **Focus:** hot inventory counters, admission control, async order pipeline, idempotency, bot defense · **Related reading:** [HLD 6.15 Ticket Booking](../computer-science/High_Level_Design.md#615-ticket-booking-seat-reservation), [HLD 4.13 Cache Stampede and Hot Keys](../computer-science/High_Level_Design.md#413-cache-stampede-and-hot-keys), [HLD 5.8 Backpressure and Load Shedding](../computer-science/High_Level_Design.md#58-backpressure-and-load-shedding)

> "We are running a flash sale: 10,000 units of a limited-edition sneaker go on sale at noon, and we expect a million users to try to buy in the first few seconds. Design checkout so we never oversell and the site stays up."

**What the interviewer is actually grading:**
- Recognizing a hot-counter problem and showing why one database row cannot absorb hundreds of thousands of decrements per second.
- A fast, atomic inventory gate (Redis Lua or sharded counters) and a durable source of truth, with a reconciliation story for when the two disagree.
- Admission control (a waiting room) that meters demand to what the backend can serve, and cheap rejection after sellout.
- Reservation with expiry: unpaid reservations return units to inventory, and payment results that arrive late are handled.
- Idempotency on every step and per-user purchase limits enforced durably.
- Trap: "use a distributed lock around the inventory check", which serializes everyone through a lock service and still oversells if the lock lease expires mid-update.

**Clarifying questions to ask:**

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| How many units, SKUs, and buyers? | One SKU, 10k units (or a few sizes); ~1M users in 10 s | 100:1 demand; 99% of users must fail fast and cheaply |
| Units per customer? | Limit 1 (or 2) per account | Per-user limit check must be atomic with the reservation |
| How long does a buyer have to pay? | 10 minutes | Reservations expire and units are returned to the pool |
| Is overselling ever acceptable? | Never; underselling briefly is acceptable | Favors a conservative gate plus reconciliation that returns stragglers |
| Fairness model: first come, or lottery? | First come after the waiting room; random order for early arrivals | Queue design and bot incentives |
| Are bots and resellers a concern? | Yes, a major one | Proof of humanity, account and card limits, post-hoc cancellation |
| Is this the same platform as normal checkout? | Yes, and normal shopping must not degrade | Isolate the sale path: separate admission, counters, and queues |

Solution: [A13](#a13-flash-sale-checkout)

---

### P14. Maps and Navigation

**Difficulty:** Hard · **Focus:** tile pyramids and CDN, continent-scale routing (contraction hierarchies, CRP), streaming traffic, ETA · **Related reading:** [HLD 4.8 Geospatial Indexing](../computer-science/High_Level_Design.md#48-geospatial-indexing), [HLD 4.11 Stream Processing](../computer-science/High_Level_Design.md#411-stream-processing), [DSA: Shortest Path Algorithms](../computer-science/DSA_Fundamentals.md#17-shortest-path-algorithms)

> "Design a maps and navigation product like Google Maps: users pan and zoom a map, search for places, get driving directions with an ETA that accounts for live traffic, and get turn-by-turn navigation with rerouting."

**What the interviewer is actually grading:**
- Map rendering as a static-content problem: a zoom pyramid of vector tiles, sized with numbers, served from a CDN with versioned URLs.
- Knowing that plain Dijkstra or A* on a continental graph takes seconds, and explaining a speedup technique (contraction hierarchies or customizable route planning) in terms of preprocessing versus query time.
- How live traffic reaches the router: GPS probes, map matching, per-edge speed aggregation in a stream processor, and weight updates without re-running hours of preprocessing.
- ETA as traffic plus historical profiles plus an ML correction, with an accuracy metric.
- Navigation sessions and rerouting: when the client recomputes, when the server pushes a better route, and how to avoid sending everyone down the same side street.
- Trap: "store the road graph in a graph database and run Dijkstra per request", or treating tiles as dynamically rendered per request.

**Clarifying questions to ask:**

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| Scale of users and navigation sessions? | ~1B MAU; ~10M concurrent navigating at peak | Sizes tile egress, route QPS, and probe ingest |
| Which travel modes? | Driving first; walking and transit later | Driving needs live traffic; transit is a different (timetable) graph |
| How fresh must traffic be? | Reflected in routes within 1-2 minutes | Streaming aggregation and frequent weight customization |
| Global routes or within a continent? | Within a continent (ferries aside) | Partition the graph by continent; no cross-server search |
| Vector or raster tiles? Offline maps? | Vector tiles; offline download of regions | Style-independent tiles, client rendering, region packages |
| ETA accuracy target? | Most trips within 10% of actual | Justifies historical profiles and ML correction |
| Privacy constraints on location data? | Probes anonymized, no raw trip retention | Drop identifiers, trim trip ends, aggregate per edge |

Solution: [A14](#a14-maps-and-navigation)

---

### P15. Video Conferencing (Zoom)

**Difficulty:** Hard · **Focus:** SFU media topology, simulcast and SVC, WebRTC signaling and NAT traversal, cascading, congestion control · **Related reading:** [CS Fundamentals: TCP vs UDP](../computer-science/CS_Fundamentals.md#22-tcp-vs-udp), [CS Fundamentals: NAT](../computer-science/CS_Fundamentals.md#nat-network-address-translation), [HLD 6.5 Video Streaming Platform](../computer-science/High_Level_Design.md#65-video-streaming-platform)

> "Design a video conferencing service like Zoom. People join meetings from laptops and phones anywhere in the world, with meetings ranging from two people to a thousand, and webinars with tens of thousands of viewers."

**What the interviewer is actually grading:**
- Choosing the media topology with bandwidth math: why mesh fails past a handful of people, why an MCU is CPU-expensive, and why an SFU is the default.
- Simulcast or SVC with per-subscriber layer selection driven by each receiver's bandwidth estimate.
- Real-time transport knowledge: UDP, RTP/RTCP, NACK versus FEC, jitter buffers, keyframe requests, and a mouth-to-ear latency budget.
- Signaling and connectivity: SDP offer/answer, ICE, STUN, TURN, and why talking to a server with a public IP simplifies NAT traversal.
- Global meetings with cascaded SFUs, and switching very large audiences to a streaming (HLS/LL-HLS) path.
- Trap: sending media over TCP or WebSockets by default, or putting an MCU on every meeting "for simplicity".

**Clarifying questions to ask:**

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| Meeting size distribution? | Most meetings 2-10; up to 1,000 interactive; webinars 50k+ view-only | SFU for interactive; streaming path for broadcast scale |
| Concurrency at peak? | ~10M concurrent participants, heavy spikes at the top of each hour | Sizes the media fleet and the join (signaling) burst |
| Latency target? | Mouth-to-ear under ~150 ms in-region, under ~300 ms intercontinental | Rules out TCP retransmission and large buffers; drives placement |
| Clients? | Native apps, browsers (WebRTC), phone dial-in | Codec choices, PSTN gateway, browser constraints |
| Recording, transcription? | Cloud recording yes; live captions nice to have | Server must be able to see media, which conflicts with E2EE |
| End-to-end encryption? | Optional per meeting | E2EE disables server-side recording, transcription, and dial-in |
| Corporate networks? | Many block UDP | TCP/TLS 443 fallback through relays, at a quality cost |

Solution: [A15](#a15-video-conferencing-zoom)

---

### P16. Top-K Trending Topics

**Difficulty:** Medium · **Focus:** stream aggregation, heavy hitters, sliding windows, anomaly scoring · **Related reading:** [4.10 Probabilistic Counting](../computer-science/High_Level_Design.md#410-probabilistic-counting-hyperloglog-and-count-min-sketch), [4.11 Stream Processing](../computer-science/High_Level_Design.md#411-stream-processing), [6.9 Search Autocomplete](../computer-science/High_Level_Design.md#69-search-autocomplete-typeahead)

> "Design the 'Trending now' box for a social network. Every post with a hashtag and every search query is an event, about 1M events per second at peak. Show the top trending topics per country for the last 5 minutes, the last hour, and the last 24 hours."

**What the interviewer is actually grading:**
- Whether you separate **"most popular"** (raw count) from **"trending"** (count relative to a baseline), and define the score before drawing boxes.
- A two-stage aggregation pipeline that survives a single viral hashtag (hot key) without a single counter becoming the bottleneck.
- A correct argument about **merging partial top-K lists**: when it is exact, when it misses items, and how to bound or repair the error.
- Sliding windows built from tumbling sub-windows, with the memory cost of each window stated in numbers.
- Abuse resistance: a bot farm must not be able to buy a trending slot cheaply.
- Trap: "keep a Redis sorted set and `ZINCRBY` every event". At 1M events/s that is one hot key per topic, unbounded memory for the long tail, and no notion of windows or baselines.

**Clarifying questions to ask:**

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| Trending means most frequent, or unusually frequent compared with normal? | Unusually frequent; "#monday" every Monday is not news | Needs a per-topic baseline store and a velocity score, not just a counter |
| How fresh must the 5-minute list be? | Updated every 30-60 s; end-to-end lag under a minute | Sets sub-window size and refresh interval |
| How many regions, and how many items per list? | ~50 countries plus global; show 10, compute 50 | Number of independent top-K lists and the over-fetch factor |
| Do counts shown to users need to be exact? | No, "12.3K posts" rounding is fine; ranking must not miss a true top-10 topic | Allows sketches with bounded error, but you must argue the bound |
| Count events or distinct users? | Distinct users; one account posting 1,000 times counts once | Dedup must happen before counts are combined, which drives partitioning |
| Personalized trending? | Not in v1, per-region only | Results are tiny shared lists that can be cached globally |
| Is policy filtering required before display? | Yes, blocked topics and a safety check on candidates | Adds a moderation step on a small candidate set, not on the full stream |

Solution: [A16](#a16-top-k-trending-topics)

---

### P17. Distributed Lock Service

**Difficulty:** Hard · **Focus:** consensus, sessions and leases, fencing, linearizable reads, coordination recipes · **Related reading:** [CS 8.12 Raft in Depth](../computer-science/CS_Fundamentals.md#812-consensus-theory-and-raft-in-depth), [CS 8.13 Leases and Fencing](../computer-science/CS_Fundamentals.md#813-consistency-guarantees-split-brain-leases-and-fencing)

> "Our services need distributed locks and leader election. Design a coordination service like Chubby, ZooKeeper, or etcd that thousands of services in a region can depend on."

**What the interviewer is actually grading:**
- A replicated state machine on a majority quorum, with the number of replicas and their placement across failure domains justified.
- **Sessions with leases and keepalives**, ephemeral nodes that vanish with the session, and watches, plus what the client must do when it cannot renew.
- **Fencing tokens**: you explain why a lease alone is unsafe under a process pause and where the token is checked.
- Read scaling without giving up linearizability where it matters (follower reads, ReadIndex, lease reads).
- Realistic numbers: a few thousand writes per second is enough, and you can explain why the service sits on the control plane, not the data path.
- Trap: "use Redis `SET NX PX`" or "use Redlock" for a correctness lock. Asynchronous replication and process pauses both produce two holders, and there is no fencing token.

**Clarifying questions to ask:**

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| How many client processes, and how often do they take locks? | ~50k sessions; locks are coarse (leader election, shard ownership), held minutes to days | Keepalive rate dominates load, not lock acquisitions |
| What must the lock protect: efficiency or correctness? | Correctness: two writers corrupt data | Requires fencing tokens and a resource that checks them |
| What failures must it survive? | Any one zone in a 3-zone region | Five replicas spread 2/2/1 across zones |
| Read consistency? | Linearizable on request; slightly stale reads acceptable for config | Follower reads by default, ReadIndex when asked |
| Is it one region or global? | One cell per region; cross-region use is rare | Keeps commit latency at intra-region RTT; global locks are a separate discussion |
| How large is the stored data? | Small: config and lock nodes, under a few GB total | Whole state fits in RAM on every replica; snapshots stay fast |
| Do clients need change notifications? | Yes, watches on config and lock nodes | Needs a watch mechanism that cannot miss events across reconnects |

Solution: [A17](#a17-distributed-lock-service)

---

### P18. Web Search Engine

**Difficulty:** Hard · **Focus:** inverted index, sharding, posting compression, top-k retrieval, ranking, tail latency · **Related reading:** [6.10 Web Crawler](../computer-science/High_Level_Design.md#610-web-crawler), [5.7 Tail-Latency Amplification](../computer-science/High_Level_Design.md#57-tail-latency-amplification)

> "Design the indexing and query-serving side of a web search engine over 50 billion pages. Assume the crawler already exists and hands you fetched pages."

**What the interviewer is actually grading:**
- Napkin math that sizes the index (postings count, bytes per posting after compression) and derives the shard count from it.
- **Document sharding vs term sharding**, with a clear reason why document sharding wins for serving.
- Query evaluation that does not touch every posting: dynamic pruning (WAND / Block-Max WAND), static-rank document ordering, tiered indexes.
- A multi-stage ranker: cheap BM25 plus static signals at the leaves, an expensive learned ranker on a few hundred candidates at the root.
- Tail latency at a fan-out of ~1,000 shards: you compute the probability a query hits a slow shard and name the mitigations.
- Trap: putting the index in a general-purpose search cluster ("just use Elasticsearch") without sizing it, or sharding by term because "a query only touches a few terms".

**Clarifying questions to ask:**

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| Query volume and latency target? | ~100k QPS average, 200k peak; p99 under 300 ms server-side | Sets replica count per shard and the per-shard time budget |
| Freshness? | News within minutes; most pages within days | Adds a small real-time tier next to a batch-built main index |
| Phrase and proximity queries? | Yes | Positions must be stored, roughly doubling index size |
| Languages and query understanding? | Many languages; spelling correction and synonyms expected | Query rewriting service before retrieval; per-language tokenization |
| Do we own ranking signals like link graph and clicks? | Yes, link graph from the crawl; click logs available | Static rank for document ordering and a learned second-stage ranker |
| Snippets? | Yes, query-dependent snippets for the top 10 | Needs a document store separate from the inverted index |
| Personalization? | Light (locale, language) only | Keeps the result cache effective |

Solution: [A18](#a18-web-search-engine)

---

### P19. Email Service (Gmail)

**Difficulty:** Hard · **Focus:** SMTP store-and-forward, abuse filtering, per-user partitioning, blob vs metadata storage, sync · **Related reading:** [6.14 Object Storage](../computer-science/High_Level_Design.md#614-object-storage-s3-like), [6.11 Notification System](../computer-science/High_Level_Design.md#611-notification-system)

> "Design a consumer email service like Gmail for over a billion users: receive mail from the internet, send mail out, store mailboxes, search them, and keep web, mobile, and IMAP clients in sync."

**What the interviewer is actually grading:**
- Understanding of SMTP as **store-and-forward**: when it is safe to reply `250 OK`, and how sender retries give you backpressure and tolerance for short inbound outages.
- A layered spam and malware pipeline ordered from cheap to expensive, and correct use of **SPF, DKIM, and DMARC** (what each one authenticates and where each breaks).
- Storage split: message bodies and attachments in object storage, metadata (labels, threads, flags) in a store partitioned by user, with attachment dedupe and the exabyte-scale numbers.
- Per-user search and incremental sync (history IDs, IMAP IDLE, mobile push), contrasted with global web search.
- Outbound deliverability: IP reputation, warming, per-user send limits to contain compromised accounts.
- Trap: one global relational schema with a `messages` table joined to `users`, or a single shared search index across all users.

**Clarifying questions to ask:**

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| Users and mail volume? | 1.5B accounts, 500M DAU, ~20 received and ~4 sent per user per day | Inbound rate (~1M/s peak) and storage growth |
| Storage quota and average mailbox size? | 15 GB free quota; average mailbox ~4 GB | Exabytes of storage, so cost and tiering dominate |
| Which clients? | Web, mobile apps, third-party IMAP clients | Need both a sync API with change IDs and IMAP semantics (UIDs, IDLE) |
| Delivery latency target? | Inbox within seconds of acceptance for most mail | Synchronous filter budget during the SMTP session vs async later stages |
| Durability promise? | Never lose mail after acknowledging it to the sender | Replicate before `250 OK`; idempotent delivery to absorb sender retries |
| Search requirements? | Full-text over the user's own mail with operators (`from:`, `has:attachment`) | Per-user index, partitioned with the mailbox |
| Custom domains and enterprise? | Out of scope for v1, mention later | Affects DMARC, routing, and admin policy but not the core |

Solution: [A19](#a19-email-service-gmail)

---

### P20. Food Delivery Platform (DoorDash)

**Difficulty:** Hard · **Focus:** three-sided marketplace, saga across services, batched dispatch, ETA prediction, location ingestion · **Related reading:** [6.6 Ride-Sharing Service](../computer-science/High_Level_Design.md#66-ride-sharing-service), [4.12 CDC, Event Sourcing, CQRS, and the Outbox](../computer-science/High_Level_Design.md#412-change-data-capture-event-sourcing-cqrs-and-the-outbox), [LLD: Food Delivery App](LLD_Practice_Problems.md#a2-food-delivery-app)

> "Design a food delivery platform like DoorDash. Customers order from restaurants, restaurants prepare the food, and independent couriers (Dashers) pick it up and deliver it. Cover ordering, dispatch, and live tracking."

**What the interviewer is actually grading:**
- Recognizing the **three-sided marketplace** (customer, merchant, Dasher) and why food prep time makes dispatch different from ride-sharing.
- An explicit order state machine that spans payment, merchant, and dispatch services, implemented as a saga with idempotent steps and compensations.
- **Dispatch as batched matching**: a cost function based on ETAs and food-ready time, solved every few seconds per market, and why greedy nearest-Dasher is worse.
- ETA prediction decomposed into prep time, travel time, and handoff, with how errors are measured and fed back.
- Location ingestion and tracking numbers derived from Dasher count and update interval.
- Trap: a single distributed transaction across order, payment, and dispatch, or charging the card and creating the order as two independent writes.

**Clarifying questions to ask:**

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| Order volume and peak shape? | 10M orders/day; dinner hour carries ~15% of the day | Peak order rate is only hundreds per second; correctness, not QPS, is hard |
| Dashers online at peak and GPS interval? | 500k at peak, every 4 s on an active delivery | 125k location updates/s, the largest write stream |
| Can one Dasher carry multiple orders? | Yes, up to 2-3 when pickups and drop-offs are close | Dispatch must consider order bundles, not only 1:1 matches |
| When is the customer charged? | Authorize at checkout, capture at delivery; adjust for substitutions and tips | Two payment steps with compensations in the saga |
| How do merchants receive orders? | Tablet app for most; POS API integrations for chains | Merchant confirmation is an unreliable external step with timeouts |
| Delivery fee pricing? | Dynamic by zone when Dashers are scarce, plus Dasher pay boosts | Needs per-zone supply and demand signals and price quotes that hold at checkout |
| Scheduled orders and grocery? | Out of scope for v1 | Scheduled orders change dispatch timing; grocery adds picking and substitutions |

Solution: [A20](#a20-food-delivery-platform-doordash)

---

## Answers

Full model answers for [section 3](#3-problems). Read one only after your timed attempt.

### A1. Distributed Message Queue

#### Requirements and assumptions

- **Functional:** producers append records (optional key, value, headers) to a **topic**; topics are split into **partitions**; consumers in a **consumer group** split the partitions among themselves and read by offset; each group tracks its own position, so groups are independent. Retention by time (7 days) or size, and **log compaction** (keep the latest value per key) for keyed topics.
- **Ordering:** total order **within a partition** only. Records with the same key go to the same partition, so per-key order holds. No global order.
- **Throughput:** 1 GB/s average ingest, 2 GB/s peak; ~1 KB average record, so ~1M records/s. 5-10 consumer groups read the tail; occasional groups replay days of history.
- **Durability:** an acknowledged write (with `acks=all`) survives the loss of any single broker or an entire AZ. RPO = 0 for acknowledged writes inside the region.
- **Latency:** p99 produce-ack under ~20 ms with `acks=all` in-region; end-to-end (produce to consumer fetch) p99 under ~100 ms.
- **Availability:** 99.95% for produce and fetch per partition; partition leader failover in seconds.
- **Delivery:** at-least-once by default; exactly-once for read-process-write pipelines that stay inside the log.
- **Out of scope:** per-message delete or ack (work-queue semantics, see Q3), message priorities, server-side filtering.

#### Capacity estimate

```text
Ingest:          1 GB/s avg, 2 GB/s peak; ~1 KB records       -> ~1M records/s avg, 2M/s peak
Batching:        producers send ~64 KB compressed batches      -> ~16k produce requests/s (cheap for a cluster)
Retention:       1 GB/s × 86,400 s = 86.4 TB/day; × 7 days     ≈ 605 TB per copy
Replicated:      × RF 3                                         ≈ 1.8 PB on disk (before compression;
                                                                  zstd/lz4 batches often save 2-4x on JSON)
Disk writes:     every byte lands on 3 brokers                  = 3 GB/s avg, 6 GB/s peak, cluster-wide
Replication:     followers pull 2 extra copies                  = 2 GB/s avg, 4 GB/s peak, mostly cross-AZ
Consumer egress: 5 tail groups × 1 GB/s                         = 5 GB/s avg, 10 GB/s peak

Broker budget (run at ~50% utilization): 250 MB/s of disk writes, 25 GbE NIC (~3 GB/s)
  Brokers for writes:  6 GB/s peak ÷ 250 MB/s                   ≈ 24 brokers (8 per AZ)
  Network out/broker:  (10 + 4) GB/s peak ÷ 24                  ≈ 580 MB/s ≈ 4.7 Gb/s  -> fits 25 GbE
  Disk per broker:     1.8 PB ÷ 24                              ≈ 75 TB -> 6 × 16 TB HDD at ~80% fill
  Rebuild a broker:    75 TB ÷ 250 MB/s                         ≈ 300,000 s ≈ 83 hours  (!)
Partitions:      one partition feeds one consumer in a group; at ~5 MB/s per consumer,
                 2 GB/s peak ÷ 5 MB/s ≈ 400 partitions for the busiest group's parallelism
                 plan ~3,000 partitions × RF 3 = 9,000 replicas ÷ 24 ≈ 375 replicas per broker
Page cache:      each broker leads 1/24 of ingest ≈ 83 MB/s peak; 10 min of tail ≈ 50 GB
                 -> on 128 GB brokers, consumers within ~10 min of the head never touch disk
Offset commits:  10 groups × 3,000 partitions, committed every 5 s ≈ 6k small records/s  -> trivial
```

**What the numbers decide:** this is a **disk-bandwidth and network** problem, not a CPU problem. Replication triples write bandwidth, and consumer fan-out makes egress 5-10x ingest, so reads must come from the page cache with zero-copy sends. The 83-hour rebuild time for a 75 TB broker is the operational risk: it argues for **tiered storage** (keep ~1 day on local disk, older closed segments in object storage), which cuts local data to about 11 TB per broker and rebuild time to about 12 hours.

#### Interfaces and data

```text
Produce(topic, partition, acks, transactional_id?, producer_id, producer_epoch,
        record_batches[ base_sequence, records[key, value, headers, ts] ])
     -> { base_offset, log_append_time } | NOT_LEADER | NOT_ENOUGH_REPLICAS | OUT_OF_ORDER_SEQUENCE | PRODUCER_FENCED
Fetch(replica_id or -1 for consumers, max_wait_ms, min_bytes, isolation_level,
      [(topic, partition, fetch_offset, current_leader_epoch, max_bytes)])
     -> per partition: { records, high_watermark, last_stable_offset, aborted_txns }
Metadata(topics)                      -> per partition: { leader, leader_epoch, replicas[], isr[] }
JoinGroup / SyncGroup / Heartbeat / LeaveGroup(group_id, member_id, generation_id, ...)
OffsetCommit(group_id, generation_id, member_id, [(topic, partition, offset, leader_epoch)])
OffsetFetch(group_id, partitions)     -> committed offsets

Record batch (stored on disk exactly as sent): base_offset, length, partition_leader_epoch, crc,
  attributes (compression, transactional, control), last_offset_delta, first/max timestamp,
  producer_id, producer_epoch, base_sequence, records[]
Cluster metadata (controller quorum, Raft log):
  topic(topic_id, name UNIQUE, partition_count, config)
  partition(topic_id, index, replicas[], isr[], leader, leader_epoch, partition_epoch)
  broker(broker_id, rack/AZ, endpoints, registration_epoch)
__consumer_offsets: compacted topic, 50 partitions by hash(group_id);
  key (group, topic, partition) -> value (offset, leader_epoch, commit_ts)
__transaction_state: compacted topic by hash(transactional_id);
  key transactional_id -> (producer_id, epoch, state, partitions[])
```

The **partition** is the unit of ordering, replication, leadership, and consumer parallelism. The producer picks it as `hash(key) % partition_count` (or round-robin batches for unkeyed records), so per-key order holds without coordination. Internal state (group offsets, transaction state) is stored in compacted topics, so it is replicated by the same mechanism as user data and partitioned by group or transaction ID, which spreads coordinator work across brokers.

#### Architecture and flow

```text
Producers (batch, compress, idempotent)                     Consumers (group members, pull)
   | Produce -> partition leader                                    ^ Fetch(offset) from leader
   v                                                                |   (or rack-local follower)
+----------------------- Broker cluster: 24 brokers, 8 per AZ ------------------------------+
|  Broker 1 (AZ a)              Broker 9 (AZ b)              Broker 17 (AZ c)               |
|  leader   orders-7            follower orders-7            follower orders-7              |
|  follower orders-3            leader   orders-3            follower orders-3              |
|  log segments + page cache    followers Fetch from leaders like consumers do              |
|  group coordinator for some groups, transaction coordinator for some transactional IDs    |
+-------------------------------------------------------------------------------------------+
   ^ heartbeats, ISR changes                      |
   | leader and ISR decisions                     v closed segments (optional tier)
Controller quorum (3-5 nodes across AZs,     Object storage: segments older than ~1 day
  Raft-replicated metadata log)
```

**Write path:**

1. The producer looks up the partition leader from cached metadata, appends records to a per-partition batch, and sends it when it reaches ~64 KB or `linger.ms` (5-10 ms) expires.
2. The leader validates the producer ID and sequence number (deduplication), assigns offsets, and appends the batch to the active segment (a write to the page cache, not an fsync).
3. Followers in other AZs are continuously long-polling `Fetch` from the leader; they append the batch and report their new log end offset (LEO) on the next fetch.
4. When every member of the ISR has the batch, the leader advances the **high watermark** past it and, for `acks=all`, responds to the producer.

**Read path:**

1. A consumer group member fetches from its assigned partitions starting at the committed offset.
2. The leader returns batches below the high watermark (below the last stable offset for `read_committed`), served from the page cache with `sendfile` when possible.
3. After processing, the consumer commits the next offset to its group coordinator, which appends it to `__consumer_offsets`.

#### Deep dive: replication, high watermark, and leader election

Each partition has a leader and followers (RF = 3, one per AZ). Followers fetch from the leader exactly like consumers. The leader tracks each follower's LEO and keeps the **in-sync replica set (ISR)**: replicas that have caught up to the leader's end within `replica.lag.time.max.ms` (default 30 s). The **high watermark (HW)** is the minimum LEO across the ISR; consumers never see records above it, so a consumer can never read a record that a leader failover could erase.

```text
RF = 3, min.insync.replicas = 2, producer acks = all
t0  Leader A LEO = 105    follower B LEO = 105    follower C LEO = 100   ISR = {A, B, C}
    HW = min(105, 105, 100) = 100 -> consumers read offsets < 100; ack for offset 104 waits
t1  C stalls (GC pause, slow disk) for more than 30 s -> A shrinks ISR to {A, B} via the controller
    HW = 105 -> the producer's ack for offset 104 is sent (ISR size 2 >= min ISR 2)
t2  B fails too -> ISR = {A}; size 1 < min ISR 2
    produce with acks=all fails NOT_ENOUGH_REPLICAS; reads below HW still work
t3  A fails. Live replicas: C only (out of sync, LEO = 100)
    unclean.leader.election = false -> partition stays offline until A or B returns (no loss)
    unclean.leader.election = true  -> C becomes leader; acknowledged offsets 100-104 are lost,
                                       and when A returns it truncates to C's log
```

Key mechanisms to name:

| Setting or mechanism | What it guarantees | Cost |
|---|---|---|
| `acks=0` | Nothing; fire and forget | Loses data on any failure |
| `acks=1` | Leader has appended it | Loses the unreplicated tail if the leader dies before followers fetch |
| `acks=all` + `min.insync.replicas=2` | At least 2 replicas in different AZs have it | Ack waits for the slowest ISR member (one follower fetch round trip, ~1-5 ms cross-AZ); writes stop if only one replica is in sync |
| **Leader epoch** | Each leader change increments an epoch stored with every batch | A returning replica asks the new leader "where does my last epoch end?" and truncates exactly there |
| No unclean election | Only an ISR member can become leader | A partition can be unavailable until an ISR member recovers |

Why leader epochs and not the HW for truncation: a follower learns the HW only on its next fetch, so its local HW lags. If a follower restarts and truncates to its stale HW, then becomes leader, it can discard a record that was already acknowledged. Truncating to the end offset of the epoch, as reported by the current leader, avoids that divergence (Kafka KIP-101).

**Leader election:** brokers heartbeat to the controller quorum. When a broker's session expires (about 10 s), the controller picks a new leader for each partition it led from that partition's ISR (preferring the first live replica in the assignment list), bumps the leader epoch, and publishes the change. Producers get `NOT_LEADER`, refresh metadata, and retry. With idempotent producers the retries do not create duplicates. The controller itself is a Raft group, so the metadata about who is leader is agreed by majority; see [Raft in depth](../computer-science/CS_Fundamentals.md#812-consensus-theory-and-raft-in-depth).

Why the ISR model rather than majority quorum per partition: with an external, consensus-backed authority deciding ISR membership, **f + 1 replicas tolerate f failures** (a majority quorum needs 2f + 1). The price is that an ack waits for the slowest ISR member until it is evicted, so a sick follower raises p99 for up to 30 s. Majority quorums (as in Raft-based logs, or the quorum reads and writes of a [Distributed Key-Value Store](../computer-science/High_Level_Design.md#68-distributed-key-value-store)) ignore the slowest replica but need more copies for the same fault tolerance.

#### Deep dive: consumer groups, offsets, and delivery semantics

**Group membership.** The group coordinator is the broker leading partition `hash(group_id) % 50` of `__consumer_offsets`. Members send `JoinGroup`; the coordinator picks one member as group leader, which computes an assignment (range, round-robin, or sticky); `SyncGroup` distributes it. Each completed rebalance increments the **generation ID**. Offset commits carry the generation, and the coordinator rejects commits from an older generation, which **fences a zombie consumer** that was kicked out (for example after a long GC pause) and still thinks it owns a partition. Two timeouts detect failure: `session.timeout.ms` (heartbeats, ~45 s) for dead processes and `max.poll.interval.ms` (~5 min) for live processes stuck in processing.

**Rebalancing cost.** The classic eager protocol revokes every partition from every member, so a 200-member group stops consuming for the whole rebalance (seconds to tens of seconds), and a rolling deploy triggers 200 of them. Fixes, in order of impact:

- **Cooperative sticky assignment:** only partitions that actually move are revoked; everyone else keeps consuming.
- **Static membership** (`group.instance.id`): a member that restarts within the session timeout gets its old partitions back with no rebalance at all.
- **Broker-side incremental assignment** (Kafka's newer consumer protocol, KIP-848): the coordinator computes assignments and reconciles members one at a time.

**Offset commit semantics.** The committed offset is the next record to read. Commit **after** processing for at-least-once (a crash replays the records since the last commit); commit before processing for at-most-once. For an external sink, store the offset in the **same database transaction** as the results and seek to it on startup; that gives effectively-once output without broker transactions. Monitor **lag** in both records (`log_end_offset - committed_offset`) and time (age of the oldest unconsumed record), because 1M records of lag means seconds on one topic and hours on another.

**Exactly-once inside the log:**

- **Idempotent producer** (on by default): the broker assigns a producer ID; each batch carries `(producer_id, epoch, partition, base_sequence)`. The leader remembers the last 5 batch sequences per producer and partition. A retried batch with a known sequence is acknowledged with its original offset and not appended again; a gap returns `OUT_OF_ORDER_SEQUENCE`. This removes duplicates from producer retries while allowing 5 in-flight requests with ordering preserved.
- **Transactions** for consume-transform-produce: a stable `transactional.id` maps to a producer ID; `InitProducerId` bumps the epoch, so an older instance with the same ID is **fenced** (`PRODUCER_FENCED`). The producer registers partitions with its transaction coordinator, writes output records, and adds the consumed offsets to the same transaction (`sendOffsetsToTransaction`). Commit is two-phase: the coordinator writes `PREPARE_COMMIT` to `__transaction_state` (the decision point), writes a COMMIT **control marker** into every involved partition, then records `COMPLETE_COMMIT`.
- **Read committed:** consumers with `isolation.level=read_committed` read only up to the **last stable offset** (LSO, the first offset of the oldest open transaction) and skip records of aborted transactions using the per-segment aborted-transaction index. A long-open transaction stalls the LSO, so `transaction.timeout.ms` bounds it.

The boundary matters: this is exactly-once **from input topics to output topics plus offsets**. Sending an email or writing to an external database from inside the loop is still at-least-once; make that sink idempotent with a key like `(topic, partition, offset)` or route it through an outbox ([4.12](../computer-science/High_Level_Design.md#412-change-data-capture-event-sourcing-cqrs-and-the-outbox)).

#### Deep dive: storage layout and why it is fast

```text
/data/orders-7/                                  (one directory per partition replica)
  00000000000041230000.log        closed segment: record batches, append-only, rolled at 1 GB or 7 days
  00000000000041230000.index      sparse offset index: relative offset (4 B) -> file position (4 B), every ~4 KB
  00000000000041230000.timeindex  timestamp (8 B) -> relative offset (4 B)
  00000000000041230000.txnindex   aborted transaction ranges (for read_committed)
  00000000000042380000.log        active segment (the only file being written)
  leader-epoch-checkpoint         (epoch, start_offset) pairs used for truncation

Index size:  1 GB segment ÷ 4 KB = 262,144 entries × 8 B ≈ 2 MB per segment, memory-mapped
Lookup of offset 41,500,123: binary search segment base offsets (in memory)
             -> binary search that segment's .index -> scan at most ~4 KB of the .log
```

- **Sequential I/O only.** Appends go to the end of one file per partition; reads of the tail are sequential too. HDDs deliver 150+ MB/s sequentially versus under 1 MB/s for random 4 KB writes (~150 IOPS × 4 KB).
- **The page cache is the cache.** The broker keeps no record cache on its heap: the OS caches recent segment pages, which avoids double caching, survives a broker process restart warm, and uses all free RAM.
- **Zero-copy.** Batches are stored in the exact compressed format producers send and consumers receive, so the broker never decompresses or re-serializes them. For plaintext connections it hands file pages to the socket with `sendfile`, skipping user space. TLS forces a user-space copy unless kernel TLS is available, which is a real CPU cost at 10 GB/s of egress.
- **No fsync per write.** At 1M records/s, synchronous flushes are impossible on HDDs. Durability comes from replicas in other AZs, and the OS flushes in the background. After an unclean shutdown, a broker validates CRCs in the active segment and rebuilds its indexes.
- **Retention is file deletion.** A segment whose newest timestamp is older than 7 days is deleted in one operation. There is no per-message delete, which is why this is a log and not a work queue.
- **Compaction** (for keyed topics such as `__consumer_offsets`, changelogs, and CDC tables): a cleaner builds a map of the latest offset per key over the "dirty" part of the log and rewrites older segments keeping only the latest record per key. Offsets are preserved, so gaps appear. A **tombstone** (null value) deletes a key and is kept for `delete.retention.ms` (for example 24 h) so slow consumers observe the delete.
- **Replays vs the tail.** A group replaying 7 days reads ~600 TB from disk and evicts the page cache that tail consumers depend on. Mitigate with fetch quotas per client, fetching from rack-local followers, and serving tiered (object-storage) segments through a separate read path.

#### Failure modes and mitigations

| Failure | Impact | Mitigation |
|---|---|---|
| Broker crash | Partitions it led are unwritable for ~10 s | Controller elects new leaders from the ISR; producers retry; idempotence removes duplicates |
| AZ outage | One third of brokers gone; every partition loses one replica | Rack-aware placement (one replica per AZ); ISR drops to 2 = min ISR, so writes continue; alert, since one more loss stops writes |
| Slow follower (GC, failing disk) | `acks=all` p99 rises until the follower is evicted from the ISR | Tune `replica.lag.time.max.ms`; alert on ISR shrink/expand rate and under-replicated partitions; replace the disk |
| Controller quorum loses majority | No leader changes or topic changes; existing leaders keep serving | 3 or 5 controllers across AZs; data path does not depend on the controller in steady state |
| Consumer crashes mid-batch | Records since the last commit are reprocessed | At-least-once with idempotent handlers, or offsets stored with results |
| Poison record | One consumer retries forever; partition lag grows | Bounded retries, then publish to a dead-letter topic with the original topic, partition, and offset |
| Hot key | One partition saturates while others idle | Detect skew from per-partition byte rates; split the key (`key#n`) if order across it is not needed |
| Disk full | Log directory goes offline; leadership moves away | Size-based retention as a backstop, disk alerts at 70-80%, tiered storage |

#### Tradeoffs

| Decision | Chosen | Alternative | Why |
|---|---|---|---|
| Data model | Append-only log with consumer offsets | Queue with per-message ack and delete | Many groups read the same bytes; replay is free; the broker keeps no per-message state |
| Replication | Leader plus followers, controller-managed ISR | Majority quorum per partition | f + 1 copies tolerate f failures; quorum avoids waiting for a slow follower but needs 2f + 1 copies |
| Durability | Replicate across AZs, fsync in background | fsync every batch | Per-batch fsync caps throughput on HDDs; a correlated power loss across 3 AZs is the accepted risk |
| Consumer model | Pull with long-poll | Broker push | Consumers control batch size and pace; slow consumers do not need broker-side buffers |
| Retention | Local hot tier plus object-storage tier | Everything on local disk | Cuts broker rebuild time from ~83 h to ~12 h and lowers cost; adds a second read path |
| Default semantics | At-least-once with idempotent producer; transactions opt-in | Exactly-once everywhere | Transactions add latency (commit interval) and LSO stalls; most consumers can be idempotent |

**Main interview tradeoff:** **durability and availability pull in opposite directions at the ISR boundary.** `acks=all` with `min.insync.replicas=2` and no unclean election means an acknowledged record is never lost, but a partition can refuse writes (fewer than 2 in sync) or go offline (no ISR member alive). Enabling unclean election or `acks=1` keeps the partition writable at the cost of losing acknowledged data. The right answer is per topic: payments and CDC topics choose durability; metrics and clickstream topics may choose availability. Say which, and why.

#### Follow-ups with model answers

**Q1. A product team insists on global ordering across all events. What do you tell them?**

Global order means one partition, which caps the topic at one leader's throughput (tens of MB/s) and one consumer per group, nowhere near 1 GB/s. Ask what they actually need ordered: almost always it is per entity (per account, per order), which per-key partitioning provides. If they need a consistent cut across entities (for example, "all events before time T"), use event timestamps plus watermarks in the consumer ([4.11](../computer-science/High_Level_Design.md#411-stream-processing)). If they truly need a total order for a low-volume stream (a ledger of configuration changes), give that stream one partition and accept its limit.

**Q2. How many partitions should a topic have, and can you add more later?**

Take the maximum of peak throughput divided by per-partition throughput (bounded by the slowest consumer's processing rate, not by the broker) and the consumer parallelism the busiest group needs, then add headroom for 1-2 years. Adding partitions later is cheap for the broker but changes `hash(key) % n`, so new records for a key may land in a different partition than old ones and per-key order breaks across the change; keyed topics are therefore over-provisioned up front or migrated to a new topic. Too many partitions costs open file handles (several per segment), controller metadata, longer failover (every partition on a dead broker needs a new leader), and more replication fetch overhead. A few thousand replicas per broker is a comfortable range.

**Q3. One consumer team wants work-queue semantics: per-message acks, delayed retries, and more consumers than partitions.**

The log does not track per-message state, so emulate it or add it. Common pattern: on failure, publish the record to retry topics with increasing delays (`orders.retry.1m`, `orders.retry.10m`) whose consumers sleep until the record's due time, and finally to a dead-letter topic. More consumers than partitions requires per-record leases rather than partition ownership; Kafka's share groups (KIP-932) add exactly that, or a classic queue (SQS, RabbitMQ) can be fed from the log. Ordering is given up in all of these, which is the price of per-message parallelism.

**Q4. Add disaster recovery in a second region.**

Mirror topics asynchronously (MirrorMaker 2 or cluster linking): per-partition order is preserved, and RPO equals replication lag (seconds). Offsets differ between clusters, so the mirroring tool emits **offset translation checkpoints** that let a consumer group resume near its position after failover, reprocessing a little (at-least-once). A stretched cluster with synchronous replication across regions gives RPO = 0 but adds the inter-region round trip (30-80 ms) to every `acks=all` write. For active-active, prefix mirrored topics with the source cluster name to prevent replication loops.

**Q5. Some producers want to send 20 MB messages.**

Large records hurt everyone on the broker: they bloat producer batches, replication fetches, and page cache usage, and a single slow record delays the partition. Use the **claim-check** pattern: store the payload in object storage under a content hash and send a small record with the reference, size, and checksum. Keep the broker's `max.message.bytes` at ~1 MB so the limit is enforced, not merely recommended.

#### Level signals

- **Mid:** partitions and consumer groups with offsets; per-partition ordering; replication factor 3; correct storage and throughput arithmetic.
- **Senior:** ISR, high watermark, `acks=all` with min ISR, and the unclean-election tradeoff, with a timeline; consumer-group generations and rebalancing costs; idempotent producer and what exactly-once covers; page cache and zero-copy tied to the egress number.
- **Staff:** finds broker rebuild time as the operational risk and proposes tiered storage with numbers; sets per-topic durability policy with product owners; plans partition counts for growth and migration; discusses quotas and multi-tenant isolation, DR with offset translation, and how the system is upgraded without downtime.

See also: [Queues and event streams](../computer-science/High_Level_Design.md#44-queues-and-event-streams), [Replication Strategies](../computer-science/CS_Fundamentals.md#83-replication-strategies), [Split Brain, Leases, and Fencing](../computer-science/CS_Fundamentals.md#813-consistency-guarantees-split-brain-leases-and-fencing), [Mock hint outline](HLD_Mock_Interviews.md#a1-distributed-message-queue)

---

### A2. Collaborative Document Editor

#### Requirements and assumptions

- **Functional:** create, open, and edit rich-text documents; see other editors' changes, cursors, and selections live; comments anchored to text; browsable version history with restore; share with users or by link as owner, editor, commenter, or viewer.
- **Concurrency:** usually 1-5 simultaneous editors per document; cap at 100 editors, with up to thousands of read-only viewers.
- **Offline:** a client can keep editing for hours to days without a connection and merge on reconnect without losing either side's text.
- **Scale:** 500M documents, 30M DAU, peak 10M connected clients and 5M open documents.
- **Latency:** local edits render immediately (optimistic); remote edits visible within 200 ms p95 in-region; opening a document under 1 s p95.
- **Durability:** an operation acknowledged to its author is never lost (RPO = 0 for acknowledged ops). All replicas of a document **converge** to the same content.
- **Out of scope:** spreadsheets and drawings (same session model, different operation types), full-text search over documents, real-time voice.

#### Capacity estimate

```text
Connections:     10M WebSockets at peak ÷ ~100k per gateway node           ≈ 100 gateway nodes (+ headroom)
Typing:          5% of connected clients typing at any moment               = 500k typists
                 client coalesces keystrokes into one op every ~500 ms     ≈ 2 ops/s per typist
                 500k × 2                                                   = 1M ops/s globally
Op log:          ~100 B per op with metadata                                ≈ 100 MB/s ≈ 8.6 TB/day raw
One busy doc:    100 editors × 2 ops/s = 200 ops/s in; each broadcast to 99 others ≈ 20k msgs/s out
                 -> a single core handles it; never split one document across machines
Session memory:  5M open docs × ~200 KB (doc model, recent ops, client table) ≈ 1 TB RAM
                 ÷ ~50 GB usable per session server                         ≈ 20 servers for memory
Session CPU:     1M ops/s ÷ ~20k ops/s per server (transform, persist, broadcast) ≈ 50 servers -> plan ~60
Op-log store:    1M appends/s × RF 3 ÷ ~50k small writes/s per node         ≈ 60 nodes (wide-column, by doc_id)
Snapshots:       every 1,000 ops or after 10 idle minutes
                 open = load snapshot + replay ≤ 1,000 ops (~100 KB)       -> well under 50 ms server time
Storage:         500M docs × ~50 KB current snapshot                        ≈ 25 TB
                 history (fine-grained ops for 30 days, then coalesced revisions) ≈ 10x ≈ 250 TB
```

**What the numbers decide:** the hardest document sees a few hundred ops per second, so **one owner process per document** can order every edit with no distributed coordination; the scaling unit is the document session, and the fleet scales by spreading sessions. The fleet-level problems are the 10M long-lived connections (a dedicated gateway tier) and the 1M durable appends per second (a write-optimized log store partitioned by document). Snapshots every 1,000 ops bound open time regardless of document age.

#### Interfaces and data

```text
GET  /v1/docs/{doc_id}             -> { snapshot, rev, role, session_token }      (ACL checked here)
WS   /v1/docs/{doc_id}/session?rev=N&token=...
  client -> server  { type: "op", client_id, client_seq, base_rev, ops: [retain 5, insert "x" {bold}, delete 3] }
                    { type: "presence", rev, cursor, selection }                   (ephemeral, throttled)
  server -> client  { type: "ack", client_seq, rev }
                    { type: "op", rev, author, ops }                               (already transformed to rev-1)
                    { type: "presence", user, cursor, selection }
                    { type: "role_changed" | "revoked" }
POST /v1/docs/{doc_id}/acl         { principal, role }       GET /v1/docs/{doc_id}/revisions?before=...
POST /v1/docs/{doc_id}/restore     { rev }                   -> applied as a new op, history is never rewritten

document(doc_id PK, owner_id, title, latest_snapshot_rev, owner_epoch, acl_version, created_at)
op_log(doc_id, rev, author_id, client_id, client_seq, ops_blob, ts)
       PRIMARY KEY (doc_id, rev); UNIQUE (doc_id, client_id, client_seq)      -- idempotent resend
snapshot(doc_id, rev, blob_ref, created_at)   PRIMARY KEY (doc_id, rev)        -- blobs in object storage
acl(doc_id, principal_id, role)               PRIMARY KEY (doc_id, principal_id)
comment(doc_id, comment_id, anchor_rev, anchor_start, anchor_end, thread...)
session_lease (coordination store): doc_id -> { server_id, epoch, expires_at }
```

Everything is partitioned by `doc_id`. A document's op log, snapshots, ACL, and comments live together, so the session owner's appends are single-partition conditional writes and opening a document is one range read (latest snapshot, then ops after it). There is no query that spans documents on the hot path; "documents shared with me" is a separate index keyed by user.

#### Architecture and flow

```text
Clients (local doc model, one in-flight op, pending buffer, IndexedDB for offline)
   | HTTPS (open) + WebSocket (session)
   v
Edge LB --> WebSocket gateways (stateless: auth, session token, route doc_id -> owner)
                 |                                         ^
                 v                                         | ops + presence to each client
       Session servers: one OWNER per open document <------+
       (in-memory doc, assigns rev, transforms, broadcasts; presence kept in memory only)
          |  conditional append (doc_id, rev, owner_epoch)        \
          v                                                        -> per-doc pub/sub topic (large viewer audiences)
       Op-log store (wide-column, partitioned by doc_id, RF 3)
          |  change stream
          +--> Snapshotter (snapshot every 1,000 ops; compacts old history) --> Object storage
          +--> Search indexer, notifications, "recent docs"
       Lease registry (etcd-like): doc_id -> (server, epoch)        ACL service (DB) --> revocation events
```

**Write path (Alice types "X"):**

1. Alice's editor applies the insert locally at once, then sends it as `{client_seq: 42, base_rev: 10, ops}` (only one op in flight; later keystrokes are buffered and composed).
2. The gateway forwards it to the document's owner. The owner transforms the op against any ops with rev 11..head that Alice has not seen, assigns the next rev, and appends it to the op log conditioned on its `owner_epoch` (group commit every few ms).
3. After the append is durable, the owner acks Alice with the rev and broadcasts the transformed op to every other client in the session.

**Read path (Bob opens the document):** the HTTP open checks the ACL, returns the latest snapshot plus the ops after it, and a session token. Bob's client connects the WebSocket with `rev=N`; the owner sends any ops after N and the current presence list, and Bob is live.

#### Deep dive: OT vs CRDT, with a worked example

**Operational transformation (OT).** Each operation is expressed against a specific revision. When two operations are concurrent (made against the same revision), the one ordered second is **transformed** to account for the first. With a central server that imposes a total order, only one property is needed (TP1: applying `a` then `transform(b, a)` equals applying `b` then `transform(a, b)`), which is why server-ordered OT (Jupiter, Google Wave, Google Docs) is practical, while peer-to-peer OT needs a much harder property (TP2) that many published transform functions fail.

Worked example. The document is `abc` at rev 10.

```text
Alice: insert "X" at 1  (base_rev 10)  -> her screen shows "aXbc"
Bob:   insert "Y" at 2  (base_rev 10)  -> his screen shows "abYc"

Server receives Alice's op first: it becomes rev 11. Document "aXbc".
Server receives Bob's op (base_rev 10). It must apply after rev 11:
   transform(Bob ins@2, Alice ins@1): Alice inserted 1 char at position 1 <= 2  -> shift Bob to 3
   rev 12 = insert "Y" at 3. Document "aXbYc". Bob gets ack(rev 12); Alice gets "insert Y at 3".
Alice applies insert Y at 3 to "aXbc"                                         -> "aXbYc"
Bob receives rev 11 (Alice ins@1) while his own op is still unacknowledged. His client transforms
   the incoming op against his pending op: transform(Alice ins@1, Bob ins@2): 2 > 1 -> no shift
   Bob applies insert X at 1 to "abYc"                                        -> "aXbYc"   converged
Same position (both insert at 1): break the tie by site ID so both sides choose the same order.
```

A minimal plain-text version of the transform (production editors use the same idea over retain/insert/delete runs with attributes):

```python
"""ot_demo.py -- insert/delete transform for plain-text OT with server ordering."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Op:
    kind: str       # "ins" | "del"
    pos: int
    text: str = ""  # inserted text; a delete removes one character
    site: str = ""  # tie-break for inserts at the same position


def apply(doc: str, op: Op) -> str:
    if op.kind == "ins":
        return doc[:op.pos] + op.text + doc[op.pos:]
    return doc[:op.pos] + doc[op.pos + 1:] if op.pos >= 0 else doc


def transform(a: Op, b: Op) -> Op:
    """Rewrite a so it applies after b (a and b were concurrent on the same base)."""
    if b.kind == "ins":
        shift = b.pos < a.pos or (b.pos == a.pos and (a.kind == "del" or b.site < a.site))
        return Op(a.kind, a.pos + len(b.text) if shift else a.pos, a.text, a.site)
    if b.pos < a.pos:                                   # b deleted a char before a
        return Op(a.kind, a.pos - 1, a.text, a.site)
    if b.pos == a.pos and a.kind == "del":              # both deleted the same char
        return Op("del", -1, "", a.site)                # no-op
    return a


if __name__ == "__main__":
    base = "abc"                                        # revision 10
    alice = Op("ins", 1, "X", "alice")                  # "aXbc"
    bob = Op("ins", 2, "Y", "bob")                      # "abYc"
    # Server receives Alice first (rev 11), then transforms Bob's op against it (rev 12).
    server = apply(apply(base, alice), transform(bob, alice))
    # Bob already shows "abYc"; his client transforms the incoming rev 11 against his pending op.
    bob_view = apply(apply(base, bob), transform(alice, bob))
    print(server, bob_view)                             # aXbYc aXbYc
    assert server == bob_view == "aXbYc"
    # Same position: the site ID breaks the tie identically on both sides.
    a2, b2 = Op("ins", 1, "X", "alice"), Op("ins", 1, "Y", "bob")
    assert apply(apply(base, a2), transform(b2, a2)) == apply(apply(base, b2), transform(a2, b2)) == "aXYbc"
    # Insert and delete at the same position: the delete still removes the original character.
    ins, dele = Op("ins", 1, "X", "alice"), Op("del", 1)
    assert apply(apply(base, ins), transform(dele, ins)) == apply(apply(base, dele), transform(ins, dele)) == "aXc"
```

**CRDTs.** A sequence CRDT (RGA, YATA as in Yjs, Fugue) gives every character a unique, immutable ID such as `(site_id, counter)`. An insert says "put this after character ID p", a delete marks an ID as a **tombstone**, and concurrent inserts after the same ID are ordered by comparing IDs. Merges are commutative, associative, and idempotent, so replicas converge regardless of delivery order and no server needs to transform anything.

| | Server-ordered OT | CRDT |
|---|---|---|
| Needs a central server | Yes (it defines the order) | No; works peer-to-peer or through a relay |
| Offline for days | Works, but the merge is one large transform against composed history | Natural: merge the two op sets |
| Memory and storage | Plain document plus op log | IDs and tombstones per character: naively 16-32 B per char; run-length encoding of consecutive inserts (Yjs, Automerge) brings typical documents to a small multiple of the text |
| Garbage collection | Trivial (snapshots) | Tombstones can be dropped only when every replica has seen the delete; a long-offline replica blocks it |
| Rich text and intent | Mature (decades in production editors) | Formatting spans and interleaving of concurrent inserts need newer algorithms (Peritext, Fugue) |
| Correctness risk | Transform functions are subtle; the server order keeps it to TP1 | Convergence is by construction; the algorithm itself is the risk |

**Choice for this prompt:** a server is always in the loop and offline periods are bounded, so **server-ordered OT** is simpler to operate and keeps storage compact. Choose a CRDT if the product is offline-first or peer-to-peer, or if documents must be edited through multiple regional relays at once. Either answer is acceptable when the reasons are tied to the requirements.

#### Deep dive: session ownership, durability, and failover

- **One owner per document.** A session server takes a lease on `doc_id` in the lease registry (TTL ~10 s, renewed every 3 s) and receives a monotonically increasing **epoch**. It writes `owner_epoch` into the document row with a conditional update. Gateways route by the registry, caching entries and refreshing on a "not owner" reply.
- **Fenced appends.** Every op-log append is conditional: `INSERT (doc_id, rev) IF NOT EXISTS AND document.owner_epoch = my_epoch`. A paused or partitioned old owner (a zombie whose lease expired) fails its next append and drops its sessions, so two servers can never assign the same rev; see [fencing tokens](../computer-science/CS_Fundamentals.md#813-consistency-guarantees-split-brain-leases-and-fencing).
- **Ack and broadcast only after the append is durable.** If the owner broadcast rev 11 before persisting it and then crashed, the next owner would assign rev 11 to a different op and clients would diverge permanently. A 5-10 ms group commit amortizes the cost and stays well inside the 200 ms budget.
- **Idempotent resend.** The unique `(doc_id, client_id, client_seq)` constraint means a client that resends an op after a disconnect gets the original rev back instead of a duplicate insert.
- **Failover timeline.** Owner crashes; the lease expires within ~10 s; the next server to receive a connection for the document takes the lease with epoch + 1, loads the latest snapshot and the ops after it (tens of milliseconds), and accepts reconnects. Each client reconnects with `rev=N` and its unacknowledged ops; the server sends ops after N, then processes the resends. Users see "reconnecting" for about 10 s but keep typing locally, so nothing is lost.
- **Snapshots and history.** A snapshotter consumes the op-log change stream, applies ops to the last snapshot, and writes a new snapshot every 1,000 ops; it never blocks the owner. Version history is a view over the log: ops grouped by author and time into revisions. Fine-grained ops are kept for 30 days, then coalesced, which is where the 10x history estimate comes from. Restoring an old version computes the diff from the current state and applies it as a **new op**, so collaborators and offline clients converge normally.
- **Large audiences.** For a document with thousands of viewers, the owner publishes each rev once to a per-document pub/sub topic; gateways subscribe and fan out to their local viewers. The owner's work stays proportional to the editors, not the viewers.

#### Deep dive: offline editing, presence, and permissions

**Offline editing.** The client stores the last synced snapshot, its rev, and all local ops in IndexedDB. On reconnect it composes its pending ops into one op `P` (base rev N). The server composes everything after N into one op `S`. Composition is the key trick: the composed op is bounded by the document size, not by the number of ops, so transforming `P` against 50,000 server ops costs about as much as transforming two ops over a 100 KB document. The server applies `transform(P, S)`, and the client applies `transform(S, P)`. Intent is the weak spot: if a collaborator deleted the paragraph that the offline user rewrote, the inserted text survives at the deletion point and may read oddly. Show a "your offline changes were merged" notice and record a pre-merge revision so either side can be restored. If the client was offline longer than fine-grained history is kept (30 days), or its access was revoked meanwhile, the server refuses the merge and saves the offline content as a copy rather than guessing.

**Presence and cursors.** Cursors and selections are ephemeral: they go through the session owner but never enter the op log or the rev order. A cursor is a `(rev, position)` pair, and every client transforms remote cursors through incoming ops exactly like an insert of length zero, so cursors move with the text. Throttle to ~10 updates/s per user, batch outgoing presence per recipient every 100 ms, and drop to 2/s when more than 20 editors are present; the 100-editor worst case would otherwise be 100 × 10 × 99 ≈ 99k messages/s. Presence entries expire after ~30 s without a heartbeat, and a session failover simply loses them (clients resend). Comments use the same anchoring: a stored `(anchor_rev, start, end)` range is transformed forward when loaded.

**Permissions.** The ACL service is the source of truth. The open request checks it and issues a short-lived session token carrying the role and `acl_version`. The owner enforces the role on every op: viewers cannot send content ops, commenters can only create comment anchors. An ACL change emits an event (through an outbox); the owner of an open document applies it within seconds, sending `role_changed` or closing the connection with `revoked`. Link sharing maps an unguessable link token to a role and is revoked by rotating the token. An offline client re-authenticates on reconnect before its ops are accepted.

#### Failure modes and mitigations

| Failure | Impact | Mitigation |
|---|---|---|
| Session server crash | Its documents stall for ~10 s | Lease expiry, new owner loads snapshot + log; clients resend unacknowledged ops; idempotent by `(client_id, client_seq)` |
| Zombie owner after a network partition | Two servers both think they own a document | Epoch-fenced conditional appends; the zombie's first append fails and it drops its sessions |
| Op-log store slow or degraded | Acks and remote updates delayed | Clients keep editing locally and show "saving"; session server applies backpressure; alert on append latency |
| Gateway crash | Its clients disconnect | Clients reconnect through another gateway with `rev=N`; sessions are unaffected |
| Transform bug causes divergence | Clients silently disagree | Clients send a checksum of their content with their rev every few seconds; on mismatch the client reloads from the server state |
| Snapshotter falls behind | Opening documents replays more ops | Alert on ops-since-snapshot; owners can request a snapshot inline for documents over a threshold |
| Viral document with 10k viewers | Owner overwhelmed by fan-out | Viewer fan-out through a per-document pub/sub topic and gateways |

#### Tradeoffs

| Decision | Chosen | Alternative | Why |
|---|---|---|---|
| Concurrency control | Server-ordered OT | CRDT | Server is always present, offline is bounded; plain document storage; switch if offline-first or P2P |
| Ordering authority | One leased owner per document | Multi-writer with merge | Per-document load is tiny; a single owner gives a simple total order and simple failover |
| Ack point | After durable append | After in-memory apply | Prevents rev reuse after a crash; costs a few ms of group commit |
| Persistence | Op log + periodic snapshots | Save the whole document on each change | History and undo come free; appends are small; open time bounded by snapshot interval |
| Presence | Ephemeral, throttled, not logged | Stored with ops | Presence is high-volume and worthless after seconds; logging it would multiply writes |
| Transport | WebSocket through stateless gateways | Long-poll or SSE plus POST | Bidirectional, low overhead per message; gateways isolate connection count from session logic |

**Main interview tradeoff:** **a central ordering authority versus coordination-free merging.** Server-ordered OT keeps the data model compact and the algorithm tractable, at the price of needing the owner online and a careful failover with fencing. CRDTs remove the ordering authority and make offline and peer-to-peer natural, at the price of per-character metadata, tombstone garbage collection, and newer, less battle-tested rich-text semantics. Pick based on how central offline and multi-region editing are to the product.

#### Follow-ups with model answers

**Q1. How does undo work when other people are editing too?**

Undo must be **local**: Ctrl+Z undoes my last change, not the last change in the document. The client keeps an undo stack of its own ops; undo takes the inverse of my op and transforms it through every op applied since (mine and others'), then sends the result as a new op. If someone else already deleted the text I inserted, the transformed inverse becomes a no-op. Global undo (reverting someone else's change) is a history restore, not Ctrl+Z.

**Q2. A company-wide sign-up sheet gets 1,000 simultaneous editors. What breaks?**

Ops in: 1,000 × 2 = 2,000 ops/s, still fine for one core. Fan-out: 2,000 × 999 ≈ 2M messages/s, which breaks one owner. Move editor fan-out to the pub/sub path used for viewers (owner publishes once per rev; gateways fan out), batch broadcasts every 50-100 ms into one message per recipient, and cut presence to a sampled summary ("37 people editing"). Transform cost also rises because each client's in-flight op is more often concurrent with many others; batching on the client (one op per second) keeps it bounded. Product can also cap editors and make the rest viewers.

**Q3. You chose a CRDT instead. How do you garbage-collect tombstones?**

A tombstone can be removed only when every replica that might still reference its ID has seen the delete (causal stability). With a server, define stability against the server: the server snapshot contains everything; a client that has been away longer than the retention window (for example 30 days) must discard its local state and re-sync from the snapshot (its unsynced edits saved as a copy). The server then compacts tombstones older than the window in its snapshots. Without that rule, one laptop in a drawer blocks garbage collection forever.

**Q4. Users on two continents edit the same document. Where does the owner run?**

Each document has one home region, initially where it was created, and its owner and op log live there. Remote editors pay the cross-region round trip (~150 ms) for acks and remote updates, but local echo hides it for their own typing. Track where the active editors are and migrate ownership (lease handoff plus log replication) when most of them are elsewhere. The op log is replicated asynchronously to a second region for disaster recovery, so a region loss costs seconds of acknowledged ops unless that replication is made synchronous for critical documents. A CRDT design could relay through regional servers with no single home, which is one of the few strong reasons to choose it here.

**Q5. How do you know clients have not silently diverged?**

Make divergence detectable: every few seconds each client sends a hash of its document content together with the rev it reflects; the owner compares with its own state at that rev (it keeps recent hashes). On mismatch, the client is told to reload from the server's authoritative state, the event is logged with both op sequences, and a fuzz test reproducer is generated. Randomized property tests of the transform functions (all interleavings of small op sets converge) run in CI.

#### Level signals

- **Mid:** WebSockets to a server, an op log rather than whole-document saves, a basic description of OT or CRDT, snapshots for load time.
- **Senior:** transforms a concurrent insert pair by hand and explains tie-breaking; one owner per document with sticky routing; ack-after-durable-append and idempotent resend; snapshot cadence tied to open latency; offline merge via composed history; presence kept out of the log.
- **Staff:** fencing of zombie owners with epochs; divergence detection and recovery as an operational feature; quantifies fan-out for large audiences and moves it off the owner; picks OT vs CRDT from product requirements (offline-first, multi-region) and explains the migration cost of changing later; history retention and tombstone policy as explicit product decisions.

See also: [Chat System](../computer-science/High_Level_Design.md#64-chat-system), [Event Sourcing and the Outbox](../computer-science/High_Level_Design.md#412-change-data-capture-event-sourcing-cqrs-and-the-outbox), [Split Brain, Leases, and Fencing](../computer-science/CS_Fundamentals.md#813-consistency-guarantees-split-brain-leases-and-fencing), [Mock hint outline](HLD_Mock_Interviews.md#a2-collaborative-document-editor)

---

### A3. File Sync Service (Dropbox)

#### Requirements and assumptions

- **Functional:** a sync folder on each device mirrors the user's cloud tree; changes on any device (create, edit, rename, move, delete) propagate to the others; shared folders with other users; 30 days of version history and restore of deleted files; web and mobile access.
- **Scale:** 100M active users (50M DAU), ~3 devices each, ~5 GB per user, ~2,000 files per user; up to 30M devices online at peak.
- **Latency:** a small change appears on other online devices within ~5 s p95. Large files stream as fast as the user's link allows.
- **Correctness:** never lose a user's bytes. Concurrent edits produce two files, not a silent overwrite. Metadata for a namespace is strongly consistent and totally ordered.
- **Durability:** 11 nines for stored blocks (erasure-coded object storage). Availability 99.9% for sync; reads of existing files may continue from replicas during metadata incidents.
- **Out of scope:** real-time co-editing inside a file (see [A2](#a2-collaborative-document-editor)), end-to-end encryption (see Q4), full-text search.

#### Capacity estimate

```text
Devices:        100M users × 3 = 300M devices; ~30M online at peak
Logical data:   100M × 5 GB                                   = 500 PB
Dedupe:         versions of the same file, copies, common files; assume ~30% saved -> ~350 PB unique
Physical:       erasure coding RS(10,4), ×1.4                 ≈ 490 PB raw   (3x replication: 1.05 EB)
Files:          100M × 2,000 = 200B file entries × ~300 B     ≈ 60 TB of latest-file metadata (+ versions, replicas)
New bytes:      50M DAU × ~20 MB of new unique chunks/day     = 1 PB/day ≈ 11.6 GB/s avg, ~25 GB/s peak
Downloads:      each new chunk fetched by ~2 other devices     ≈ 2 PB/day ≈ 23 GB/s avg
Commits:        50M DAU × 40 file changes/day                  = 2B/day ≈ 23k/s avg, ~70k/s peak
Notifications:  70k commits/s × ~3 other devices               ≈ 210k "changed" signals/s at peak
Long-polls:     30M open polls, 90 s timeout                   ≈ 330k cheap re-polls/s
                ÷ ~500k mostly idle connections per node        ≈ 60 notification nodes (+ headroom)

Chunk size vs metadata (350 PB unique):
  4 MB average:   ~87B chunks × 64 B (SHA-256, location, refcount) ≈ 5.6 TB chunk index
  1 MB average:   ~350B chunks × 64 B                            ≈ 22 TB
  64 KB average:  ~5.5T chunks × 64 B                            ≈ 350 TB  -> too much metadata per byte saved
```

**What the numbers decide:** 500 PB of bytes and ~60 TB of metadata are two different systems: bytes go to content-addressed object storage, metadata to a strongly consistent sharded database. Upload bandwidth (25 GB/s peak) is the main cost driver, which is why chunk-level dedupe and delta transfer matter more than raw storage. A 1 MB average chunk keeps the chunk index around 22 TB while still localizing edits. 30M idle connections are cheap per connection but need their own tier, separate from the metadata API.

#### Interfaces and data

```text
POST /v1/blocks/upload_urls     { ns_id, hashes[] }
     -> [{ hash, url }]   presigned PUT, 15 min expiry, SHA-256 checksum header required
POST /v1/commit_batch           { ns_id, entries: [{ path, parent_rev | null, blocklist: [h1, h2, ...],
                                  size, mtime, client_mtime }] }
     -> 200 { entries: [{ path, rev, journal_id }] }
      | 409 { need_blocks: [h3, h7] }                (upload them, then retry the same commit)
      | 409 { conflict: { path, current_rev } }
GET  /v1/list_folder/continue?cursor=...  -> { entries[], cursor, has_more }   (delta since cursor)
GET  /v1/longpoll?cursor=...&timeout=90   -> { changes: true | false, backoff_s? }
POST /v1/blocks/download_urls   { ns_id, hashes[] } -> presigned GETs (only hashes referenced in ns_id)

namespace(ns_id PK, kind ROOT | SHARED, owner_id, created_at)
mount(user_id, ns_id, mount_path, role)                  PRIMARY KEY (user_id, ns_id)
journal(ns_id, journal_id, file_id, path, rev, blocklist, size, mtime, deleted, device_id, ts)
       PRIMARY KEY (ns_id, journal_id)                    -- journal_id strictly increasing per namespace
file_latest(ns_id, path_lower, file_id, rev, journal_id, blocklist, size, is_dir)
       PRIMARY KEY (ns_id, path_lower)                    -- one live entry per case-folded path
block(hash PK, size, storage_key, refcount, first_seen)   -- global chunk index
client cursor (opaque, signed): { ns_id -> last journal_id seen } for every namespace the user mounts
```

The metadata database is sharded by **namespace** (a user's root folder or one shared folder). A commit touches one namespace, so it is a single-shard transaction: check `parent_rev`, insert the journal row with the next `journal_id`, update `file_latest`, all atomically. A user's view is the union of the namespaces they mount, so their cursor is a small vector of per-namespace positions. A global journal would be a single bottleneck; per-user journals would turn one write to a 10,000-member shared folder into 10,000 journal writes.

#### Architecture and flow

```text
Client: file watcher, chunker, local metadata DB, local chunk cache, LAN sync peer
   | metadata API (HTTPS)          | chunk PUT/GET (presigned URLs)       | long-poll
   v                               v                                       v
API gateway --> Metadata service   Object storage                         Notification servers
               (commit, list,      (key = blocks/<sha256>; RS(10,4);     (30M open polls,
                cursor, ACL)        checksum verified on PUT)              subscribe by ns_id)
                  |      \                ^                                    ^
                  v       \               | block existence check              |
       Metadata DB         +--> Chunk index (hash -> storage key, refcount)    |
       (sharded by ns_id:                                                      |
        journal + file_latest) -- journal append event --> pub/sub by ns_id ---+
                  +--> preview and thumbnail workers, version GC, audit log
```

**Upload path (laptop saves `report.docx`):**

1. The watcher sees the change; the client chunks the file with content-defined chunking and hashes each chunk (SHA-256).
2. It tries `commit_batch` with the new block list and `parent_rev = 7`. The server replies `need_blocks: [h3]` because only that chunk is new in this namespace.
3. The client asks for an upload URL for `h3` and PUTs the bytes directly to object storage; the store rejects the PUT if the content does not match the declared SHA-256.
4. The client retries the commit. The server verifies `h3` exists, checks `parent_rev = 7` is still current, appends journal entry 1,042 (rev 8), updates `file_latest`, increments chunk refcounts, and publishes "ns 55 changed".

**Download path (phone):**

1. The phone's long-poll on the notification server returns `changes: true` within a second.
2. The phone calls `list_folder/continue` with its cursor and receives journal entries after its position, plus a new cursor.
3. For each changed file it fetches only chunks missing from its local chunk cache, writes them to a temporary file, verifies hashes, and atomically renames it into place. Then it advances its stored cursor.

#### Deep dive: content-defined chunking and dedupe

**Why fixed blocks fail.** Insert 100 bytes at the start of a 1 GB file. With fixed 4 MB blocks every boundary shifts, all 256 blocks get new hashes, and the client re-uploads 1 GB. (Dropbox's production answer is fixed 4 MB blocks plus rsync-style binary deltas inside changed blocks; content-defined chunking solves the same problem at the chunk layer and also helps cross-file dedupe.)

**Content-defined chunking (CDC).** Slide a rolling hash (Rabin, or the faster Gear hash used by FastCDC) over a ~48-byte window and declare a chunk boundary wherever `hash & mask == 0`. With a 20-bit mask, a boundary occurs on average every 2^20 bytes = 1 MiB. Enforce a minimum (256 KB) and maximum (4 MB) chunk size so pathological content (all zeros) cannot create millions of tiny chunks or one giant one. Because boundaries depend on content, not offsets, the insertion changes only the chunk that contains it (occasionally its neighbor too); every later boundary re-synchronizes.

```text
Edit: insert 100 B at offset 0 of a 1 GB file
  Fixed 4 MB blocks:    256 of 256 blocks change         -> upload ~1 GB
  CDC, 1 MB average:    1-2 of ~1,024 chunks change       -> upload ~1-2 MB + a new 1,024-entry block list (~33 KB)
Client CPU:  Gear rolling hash ~1-2 GB/s per core; SHA-256 ~1-2 GB/s per core with SHA extensions
             -> re-chunking and hashing a 1 GB file takes about 1 s; small files are trivial
Collisions:  ~4e11 chunks, SHA-256: P(any collision) ≈ n^2 / 2^257 ≈ 1.6e23 / 2.3e77 ≈ 1e-54 -> ignore
```

**Where dedupe happens, and the security trap.** If the server skipped an upload because *anyone* had stored that hash, two problems appear: (1) a client that merely knows a hash could claim the chunk and then download someone else's file (the "hash as capability" bug), and (2) the skipped upload reveals that the content exists somewhere (a confirmation side channel for known documents). So client-visible dedupe (`need_blocks`) is scoped to **namespaces the user can already read**, which captures the big win (new versions of the user's own files), and `download_urls` only signs hashes referenced by a namespace the caller can read. Cross-user dedupe still happens **server-side after upload**: the chunk index notices the hash already exists, keeps one physical copy, and increments its refcount. That saves storage but not upload bandwidth, which is the price of not leaking information.

**Garbage collection.** A chunk is deletable when no retained version (30 days of history) references it. Refcounts are maintained on commit and on version expiry, plus a periodic mark-and-sweep that recomputes them because refcounts drift under bugs and retries. A chunk uploaded but not yet committed has refcount 0; GC must give it a **grace period** (for example 24 h after upload) or it can delete a chunk that a commit is about to reference. The commit's existence check is the backstop.

#### Deep dive: metadata consistency and the sync protocol

- **Per-namespace total order.** Each namespace has a journal with a strictly increasing `journal_id`. All changes to the namespace are serialized by its shard primary, so every device replays the same sequence. This is a small, strongly consistent log per namespace, not a global one.
- **Cursor = position in the journals.** A client's cursor records the last `journal_id` it applied in each mounted namespace. `list_folder/continue` returns entries after that position, paginated. Because the cursor is a position in a durable log, a client that was offline for a week simply resumes; one that was gone longer than the retained journal window gets a "reset" and does a full listing comparison against its local state.
- **Notifications are hints, not data.** The notification server only says "something in a namespace you watch changed". The client then fetches deltas with its cursor. A lost or duplicated notification costs at most a delay or an extra empty fetch; nothing is missed, because correctness lives in the cursor. On reconnect, the client always does one `list_folder/continue` before long-polling.
- **Long-poll vs push.** A long-poll with a ~90 s timeout works through proxies and corporate firewalls, and on mobile it is replaced by OS push notifications that wake the app. A WebSocket per device is equivalent in cost; the important property is that the server holds idle connections cheaply and fans out by `ns_id` via pub/sub ([Notification System](../computer-science/High_Level_Design.md#611-notification-system)).
- **Commit is the linearization point.** Chunks are uploaded first (idempotent, content-addressed, can be retried forever), and the file becomes visible only when the metadata commit succeeds. A crash between the two leaves orphan chunks for GC, never a half-written file.
- **Moves across namespaces** (from a shared folder into the user's root) touch two shards. Implement as copy-then-delete with a move ID, so a crash leaves a duplicate rather than a loss, and the client renders the pair as a move.

#### Deep dive: conflicts, the upload path, and bandwidth

**Conflict handling.** Every commit carries `parent_rev`, and the shard accepts it only if `parent_rev` equals the current rev (an optimistic, conditional write).

```text
rev 7 of report.docx is on laptop and phone; both go offline and edit it
laptop reconnects: commit(parent_rev = 7) -> accepted as rev 8
phone reconnects:  commit(parent_rev = 7) -> 409 conflict (current_rev = 8)
phone client:      commits its bytes as "report (Phone's conflicted copy 2026-11-04).docx" (new path)
                   downloads rev 8 into report.docx
result:            both versions exist on every device; the user merges by hand
```

Policy for other cases: edit vs delete keeps the edited file (resurrect it); delete of a folder whose child was edited elsewhere restores that child; two files whose names differ only by case collide on `path_lower` and the second becomes a conflicted copy. Never auto-merge file contents in a general-purpose sync service: the server does not understand most file formats, and a wrong merge is silent data loss.

**Upload path.** Clients PUT chunks straight to object storage with presigned URLs, so application servers never carry the ~25 GB/s of upload traffic. The object key is the content hash (`blocks/<sha256>`), so a retried PUT is idempotent. The presigned URL requires a SHA-256 checksum header, so the store rejects content that does not match its claimed hash; without that, a client could upload garbage under someone else's popular hash and corrupt every file that references it. Upload 4-8 chunks in parallel; a large upload is naturally resumable because a retry re-sends only chunks the server reports missing. Encrypt at rest with per-chunk data keys wrapped by a key-management service.

**Bandwidth.** In order of payoff:

- **Delta sync:** only new chunks move (the CDC numbers above).
- **Compression:** zstd per chunk before upload, skipped for already-compressed types (JPEG, MP4, ZIP).
- **LAN sync:** clients announce the namespaces they hold on the local network; a peer that already has a chunk serves it over TLS authenticated with a per-namespace certificate. A 1 GB file in a folder shared by 50 machines in one office is downloaded from the cloud once and copied over the LAN 49 times, saving ~49 GB of WAN.
- **Batching:** thousands of small files are committed in one `commit_batch` and uploaded in pipelined requests, because per-file round trips dominate for small files.
- **User controls:** upload and download rate limits, "Wi-Fi only" on mobile, and selective sync so laptops do not download folders they never open.

#### Failure modes and mitigations

| Failure | Impact | Mitigation |
|---|---|---|
| Metadata shard primary fails | Commits for its namespaces fail for seconds | Synchronous replica and automatic failover; clients retry with backoff; reads continue from replicas |
| Notification server crash | Its devices stop hearing about changes | Clients reconnect to another node and immediately run `list_folder/continue`; notifications are only hints |
| Chunks uploaded, commit never happens | Orphan chunks consume storage | Refcount 0 plus upload grace period, then GC |
| Client crashes mid-download | Partially written file | Write to a temporary file, verify hashes, atomic rename; resume from the local chunk cache |
| Buggy client deletes thousands of files | Deletes sync everywhere | Mass-delete detection with confirmation, 30-day version history, one-click restore of a folder to a point in time |
| Corrupt chunk on disk | Wrong bytes served | Checksums verified on read; erasure-coded reconstruction; background scrubbing |
| Shared folder with 10k members gets a burst of edits | Notification fan-out spike | Coalesce notifications per namespace per second; members fetch deltas once per burst |

#### Tradeoffs

| Decision | Chosen | Alternative | Why |
|---|---|---|---|
| Chunking | Content-defined, ~1 MB average | Fixed 4 MB blocks plus binary deltas | Localizes inserts without a per-file delta protocol; costs a rolling hash on the client |
| Client-visible dedupe scope | Namespaces the user can read | Global by hash | Prevents hash-as-capability and existence leaks; cross-user dedupe still saves storage server-side |
| Metadata ordering | Strongly consistent journal per namespace | Global log, or per-user journals | Single-shard commits; cursors as positions; no fan-out writes for shared folders |
| Change discovery | Long-poll or push hint plus delta fetch | Periodic full listing | Seconds of latency at ~zero cost for idle devices; correctness from the cursor, not the notification |
| Conflicts | Conflicted copy | Last writer wins, or content merge | Never loses bytes; the server cannot merge arbitrary formats |
| Storage | Erasure coding RS(10,4) | 3x replication | ~490 PB vs ~1.05 EB raw for the same durability target |

**Main interview tradeoff:** **chunk size** sets the balance between transfer savings and metadata cost. Smaller chunks localize edits and dedupe better but multiply the chunk index (350 TB at 64 KB vs 22 TB at 1 MB) and per-chunk request overhead; larger chunks are cheap to track but re-upload more per edit. Content-defined chunking at ~1 MB, with min and max bounds, gets most of the transfer savings while keeping metadata small. Say what you would measure (bytes uploaded per edit, chunk-index growth) to tune it.

#### Follow-ups with model answers

**Q1. A user installs the client on a new laptop with 200,000 files in their account. How does the first sync go?**

Start from an empty cursor: `list_folder` pages through `file_latest` for each mounted namespace (cheaper than replaying the journal), and returns a cursor at the current journal position. Download in priority order (recently used and small files first, so the folder is usable quickly) with many parallel chunk fetches, and pull from LAN peers when available. Changes made during the initial sync are picked up by the cursor afterward. For 5 GB at 100 Mb/s that is about 7 minutes of transfer; selective sync lets the user skip large folders.

**Q2. Why a journal per namespace and not one per user?**

A shared folder with 10,000 members would turn every edit into 10,000 journal writes, and a user's per-user journal would mix entries from many shards, losing single-shard commits. With per-namespace journals, an edit is one write in one shard, and each member's cursor includes that namespace's position. The cost is that a client tracks a vector of positions (one per mounted namespace), which is small.

**Q3. How would you add end-to-end encryption?**

The client encrypts each chunk with a key the server never sees. Cross-user dedupe disappears (identical plaintext produces different ciphertext); convergent encryption (key derived from the content hash) restores it but leaks whether two users hold the same file, which defeats much of the point. Server-side previews, thumbnails, and search stop working, and shared folders need key distribution (wrap the folder key for each member's public key; rotate it when someone is removed). Offer it as an opt-in vault, not the default.

**Q4. How do you cut the storage bill?**

Most bytes are cold. Move chunks referenced only by versions older than ~30 days, or by files not opened in 90 days, to a colder storage class with cheaper disks or wider erasure codes (for example RS(20,4), 1.2x), and keep hot chunks on the faster tier. Measure the real dedupe ratio per content type, and compress chunks that compress well. Because chunks are content-addressed and immutable, moving them between tiers only changes the chunk index entry, not any file metadata.

**Q5. Two devices rename the same folder to different names at the same time.**

Folder renames are journal entries on the folder's entry with a `parent_rev` check, so one wins and the other gets a conflict. The losing device re-reads the namespace, sees the folder under the winning name, and applies its own pending changes inside it. Clients identify files by `file_id`, not just path, so edits to files inside the renamed folder are not lost; they are re-pathed under the new name.

#### Level signals

- **Mid:** separates metadata from blocks, uploads only changed blocks, uses a notification to trigger sync, mentions conflicts.
- **Senior:** content-defined chunking with numbers; commit protocol (blocks first, then conditional metadata commit); per-namespace journal and cursor; notifications as hints; conflicted copies; presigned uploads with checksum enforcement.
- **Staff:** catches the hash-as-capability and dedupe side-channel problems; GC races and grace periods; chunk-size tradeoff against index size; LAN sync and storage tiering with cost; mass-delete protection and recovery as product features.

See also: [Object Storage (S3-like)](../computer-science/High_Level_Design.md#614-object-storage-s3-like), [Notification System](../computer-science/High_Level_Design.md#611-notification-system), [Bloom Filters and Merkle Trees](../computer-science/High_Level_Design.md#49-bloom-filters-and-merkle-trees), [Mock hint outline](HLD_Mock_Interviews.md#a3-file-sync-dropbox)

---

### A4. Photo Sharing Service (Instagram)

#### Requirements and assumptions

- **Functional:** upload one or more photos with a caption; photos appear on the author's profile and in followers' feeds; public or private accounts, blocks, and close-friends audiences; likes and comments with counts; delete a post.
- **Scale:** 500M DAU; 100M photo uploads/day at ~3 MB per original; each user views ~100 images/day.
- **Latency:** upload acknowledged as soon as bytes land; photo visible to followers within ~10 s p95 of upload completing; feed images start rendering within 200 ms p95 (CDN edge hit).
- **Durability:** an accepted photo is never lost (11-nines object storage); likes are never double-counted for the same user.
- **Privacy:** a viewer who is not allowed to see a post must not get its metadata from the API, and must not be able to fetch its bytes for longer than a stated window (for example 1 hour) after losing access. Deletions and legal takedowns propagate within minutes.
- **Out of scope:** the feed ranking model (reuse [News Feed](../computer-science/High_Level_Design.md#63-news-feed)), video (see Q2), direct messages, search and explore.

#### Capacity estimate

```text
Uploads:       100M/day ÷ 86,400 ≈ 1,160/s avg, ~3,500/s peak (3x)
Ingress:       100M × 3 MB = 300 TB/day ≈ 3.5 GB/s avg, ~10 GB/s peak
Derivatives:   4 sizes (150 px ~15 KB, 320 px ~40 KB, 640 px ~100 KB, 1080 px ~250 KB)
               in JPEG + AVIF ≈ 0.6 MB per photo -> 60 TB/day
Storage/year:  originals 300 TB × 365 ≈ 110 PB; derivatives 60 TB × 365 ≈ 22 PB
Views:         500M × 100 = 50B images/day ≈ 580k/s avg, ~1.7M/s peak
Egress:        ~100 KB per delivered image × 50B = 5 PB/day ≈ 58 GB/s ≈ 460 Gb/s avg, ~1.4 Tb/s peak
Origin load:   95% CDN hit ratio -> 5% of 580k/s ≈ 29k req/s and ~2.9 GB/s to the origin shield
Processing:    ~1 core-second per photo (decode 12 MP, 4 resizes, JPEG + AVIF encode; AVIF dominates)
               3,500/s peak ≈ 3,500 cores; moderation classifiers ~5 ms GPU each, batched ≈ 20 GPUs
Likes:         500M × 10/day = 5B/day ≈ 58k/s avg, ~175k/s peak; a celebrity post: up to ~30k likes/s
Post metadata: 100M posts/day × ~1 KB ≈ 100 GB/day ≈ 36 TB/year

Storage cost (assumed prices per TB-month: hot $20, infrequent access $10, cold archive $2):
  One year of originals, all hot:          110,000 TB × $20               ≈ $2.2M/month
  Tiered: last 30 days hot, the rest cold: 9,000 × $20 + 101,000 × $2     ≈ $180k + $202k ≈ $382k/month
  Derivatives: 90 days hot, rest infrequent: 5,400 × $20 + 16,600 × $10   ≈ $108k + $166k ≈ $274k/month
                                            (vs 22,000 × $20 = $440k all hot)
  CDN egress at an assumed $0.005/GB:      5 PB/day × 30 = 150 PB/month    ≈ $750k/month
```

**What the numbers decide:** reads outnumber uploads 500 to 1, and egress is ~1.4 Tb/s at peak, so the design is **a CDN with an upload pipeline behind it**: the CDN hit ratio and image byte size drive serving cost, and application servers must never carry image bytes. Originals are 5x the bytes of derivatives but are almost never read after processing, so tiering them to cold storage after 30 days saves about $1.8M per month on one year of data. Processing is a few thousand cores and is naturally asynchronous and horizontally scalable.

#### Interfaces and data

```text
POST /v1/uploads              { content_type, byte_size, sha256 }
     -> { upload_id, photo_id, put_url | resumable_session_url, expires_at }
PUT  <presigned staging URL>  (bytes go straight to object storage; resumable for mobile)
POST /v1/uploads/{upload_id}/complete         -> 202 { photo_id, state: "PROCESSING" }
POST /v1/posts   { photo_ids[], caption, audience: PUBLIC | FOLLOWERS | CLOSE_FRIENDS, idempotency_key }
     -> 201 { post_id, state: PENDING | PUBLISHED }   (PENDING until all photos are READY)
GET  /v1/posts/{post_id}       -> { author, caption, media: [{ size, format, url }], like_count, liked_by_me }
PUT  /v1/posts/{post_id}/likes/me    DELETE /v1/posts/{post_id}/likes/me      (idempotent)
GET  /v1/posts/{post_id}/comments?cursor=...   POST /v1/posts/{post_id}/comments

photo(photo_id PK [random 128-bit], owner_id, state UPLOADING|PROCESSING|READY|REJECTED|DELETED,
      original_key, sha256, width, height, taken_at?, moderation_state, created_at)
derivative(photo_id, size, format, object_key, bytes)     PRIMARY KEY (photo_id, size, format)
post(post_id PK, author_id, photo_ids[], caption, audience, state, created_at)   -- sharded by post_id
like(post_id, user_id, created_at)        PRIMARY KEY (post_id, user_id)          -- sharded by post_id
liked_by_user(user_id, post_id, created_at) PRIMARY KEY (user_id, post_id)        -- sharded by user_id
post_counters(post_id PK, likes, comments, updated_at)    -- derived, rebuilt from like/comment tables
comment(post_id, comment_id [time-ordered], author_id, text, state)  PRIMARY KEY (post_id, comment_id)
```

Post, like, and comment data are sharded by `post_id`, so everything about one post (including its likes, for uniqueness) is one partition; the `liked_by_user` copy, sharded by user, answers "did I like these 20 posts?" with one batched lookup per page. Photo IDs are random 128-bit values because they appear in media URLs: they must not be enumerable. Object keys are deterministic (`photos/{photo_id}/{size}.{format}`), which makes reprocessing idempotent.

#### Architecture and flow

```text
Mobile/web client
  | 1 POST /uploads         | 2 PUT bytes (presigned)        | 7 GET images (CDN URLs, signed if private)
  v                         v                                v
API gateway -> Upload svc   Object storage: staging bucket   CDN edge POPs --> Origin shield --> Image origin
                 |          (lifecycle: delete after 7 days)  (validates URL signature at the edge) |
                 |                 | 3 object-created event                                       v
                 |                 v                                     Object storage: derivatives (hot -> IA),
                 |          Processing queue --> Image workers (sandboxed)   originals (hot 30 d -> cold)
                 |                                 validate, strip EXIF, hash match,
                 |                                 resize + encode, classifiers
                 |                                 | 4 photo READY (conditional update)
                 v                                 v
            Photo/Post DB  <---------------- photo.ready event --> Post svc publishes PENDING posts
                 | 5 post.published (outbox)
                 v
            Feed fan-out (News Feed 6.3) --> timelines
  Reads: Feed/Post API --> 6 hydrate posts + authorize viewer + sign media URLs --> client
  Likes: Like svc --> like table (unique) --> outbox --> counter aggregator --> post_counters
```

**Write path:**

1. The client requests an upload; the upload service creates a `photo` row (UPLOADING) and returns a presigned, size-limited URL for the staging bucket.
2. The client uploads bytes directly to object storage (resumable on mobile) and calls `complete`.
3. The object-created event (or `complete`) enqueues `process(photo_id)`.
4. A worker validates, strips EXIF, matches against known-illegal-content hash lists, writes derivatives, runs classifiers, and moves the photo `PROCESSING -> READY` with a conditional update.
5. The post service publishes any post waiting on that photo and emits `post.published` through an outbox; feed fan-out proceeds as in [News Feed](../computer-science/High_Level_Design.md#63-news-feed).

**Read path:**

6. The feed or post API hydrates post IDs into posts, drops any the viewer may not see, and returns media URLs (plain for public posts, signed and expiring for non-public ones).
7. The client picks the size that matches its screen and fetches from the CDN; misses go through the origin shield to the derivatives bucket.

#### Deep dive: the upload and processing pipeline

```text
State machine: UPLOADING -> PROCESSING -> READY
                                       \-> REJECTED (validation failed, known illegal content)
               READY -> DELETED (user or takedown)        moderation_state: ok | limited | in_review | removed

Worker steps (each idempotent; the job is keyed by photo_id; the queue delivers at least once):
  1 Validate   magic bytes and format allowlist (JPEG, HEIC, PNG, WebP); byte size <= 50 MB;
               pixel count <= 100 MP before full decode (decompression-bomb guard)
  2 Normalize  decode, apply the EXIF orientation, convert color profile to sRGB
  3 Strip      remove all EXIF/XMP (GPS, device serial); keep taken_at only as a DB field
  4 Match      perceptual hash vs known-illegal-content lists -> REJECTED + report, never visible
  5 Derive     4 sizes × {JPEG, AVIF} -> photos/{photo_id}/{size}.{format}   (overwrite-safe keys)
  6 Classify   nudity, violence, spam scores -> ok | limited distribution | queue for human review
  7 Commit     UPDATE photo SET state='READY' WHERE photo_id=? AND state='PROCESSING'; emit photo.ready
```

- **Why asynchronous:** a 12 MP decode plus AVIF encodes takes about a second of CPU; doing it in the request ties up connections, makes latency depend on image size, and fails the whole upload on a transient error. The client shows its local copy immediately, so the user does not wait for processing.
- **Idempotency:** derivative keys are deterministic and the final transition is conditional, so a redelivered job overwrites identical objects and the second `READY` update affects zero rows. Retries with backoff; after N failures the job goes to a dead-letter queue, the photo becomes `REJECTED`, and the user is told the upload failed.
- **Isolation:** image decoders are a classic attack surface. Run workers in sandboxes (no network except the object store, seccomp, memory and time limits), so a malicious file crashes one worker instead of compromising it.
- **Ordering of checks:** known-illegal-content matching runs **before** the photo can become visible, because "remove it later" is not acceptable for that category. Classifier-based moderation may run after publishing with limited distribution, because false positives on a blocking check would delay millions of legitimate posts.
- **Priorities and backlog:** at 3,500 photos/s, a 10-minute worker outage builds a 2M-job backlog. Autoscale on queue age, not length, and process fresh uploads before backfills (separate queues), so a backlog never delays what users are waiting for.
- **Staging cleanup:** staging objects that never complete are deleted by a 7-day lifecycle rule; originals of accepted photos move to the originals bucket.

#### Deep dive: storage tiers, CDN, and privacy at the edge

**Tiering.** Originals are read only for reprocessing and for "download your data", so they move to a cold tier after 30 days (the ~$1.8M/month saving above). Derivatives follow a power law: most views happen in a post's first days, so they stay hot for 90 days, then move to infrequent access; a CDN miss on an old photo pays a slightly slower, slightly more expensive read, which is fine at the long tail's volume. A product question worth raising: if the app never displays more than 1080 px, storing a high-quality 2048 px master (~1 MB) instead of the 3 MB original cuts the largest storage line by about two thirds.

**CDN.** Images are immutable (a new edit gets a new photo ID), so they are served with `Cache-Control: public, max-age=31536000, immutable`. An **origin shield** (a regional mid-tier cache) collapses misses from hundreds of edge POPs into one origin fetch per object. Clients choose size and format (AVIF where supported, typically 30-50% smaller than JPEG), which reduces egress directly. Rare sizes can be generated on demand by an image proxy at the shield and cached, rather than precomputed for 100M photos a day.

**Privacy is enforced in two places:**

- **At read time in the API.** Every hydration path (feed, profile grid, post page, comments, search) checks `can_view(viewer, post)`: public author, or an accepted follower for a private account, or a member of the post's audience list, and no block in either direction. The check uses a cached follow and block graph and is batched per page (20 posts, one multi-get). Feed timelines built when the account was public may still contain the post ID; hydration filters it, so going private never requires rewriting millions of timelines.
- **At the CDN.** A media URL is a capability: whoever holds it can fetch the bytes. Public posts use plain URLs with unguessable photo IDs. Non-public posts get **signed, expiring URLs**: `https://img.example/p/{photo_id}/640.avif?exp=1762300800&kid=7&sig=HMAC(key7, path|exp)`. The edge validates the signature and expiry before serving, and the **cache key excludes `exp`, `kid`, and `sig`**, so every authorized viewer shares one cached object and the hit ratio is unaffected. Expiry is rounded up to the hour so the same URL is reused (and browser-cached) within that hour.
- **Revocation window.** When a user blocks someone or goes private, URLs already issued to that viewer keep working until they expire (at most ~1-2 hours with hourly rounding). State that bound explicitly. For deletion and legal takedown, mark the photo `DELETED` (the API stops issuing URLs), delete the derivative objects, and **purge the CDN by key**, which takes seconds to minutes.
- Signed cookies covering a whole path are cheaper to issue but cannot express per-photo authorization; per-URL signatures cost one HMAC (about a microsecond), which is negligible even at 1.7M images/s.

#### Deep dive: likes, comments, and hot posts

- **Likes are a set, counts are derived.** `PUT /likes/me` inserts `(post_id, user_id)` with the primary key making it idempotent: a double tap or a retry cannot like twice. The same transaction writes an outbox event (`liked` or `unliked`). `liked_by_user` is updated from the event stream and serves "liked by me" for a page of posts in one batched lookup.
- **Counters are aggregated, not incremented per like.** A stream aggregator keyed by `post_id` sums like and unlike events over 1-second windows and applies one `UPDATE post_counters SET likes = likes + :delta` per active post per second ([Stream Processing](../computer-science/High_Level_Design.md#411-stream-processing)). A celebrity post receiving 30k likes/s costs one counter write per second instead of 30k contended row updates. Events carry IDs so the aggregator deduplicates redeliveries; a nightly job reconciles `post_counters` against `COUNT(*)` on the like table.
- **Display counts tolerate seconds of lag.** The app shows "1.2M likes", so a counter that is a second behind is invisible; the liker's own state comes from `liked_by_user` and is exact immediately (read-your-writes for the actor, eventual for everyone else).
- **Alternative: sharded counters.** Split a hot post's counter into 16 rows (`post_id#0..15`), increment a random one, and sum on read. Simpler than a stream job but adds read fan-out; good for a smaller system.
- **Comments** are rows partitioned by `post_id`, ordered by a time-ordered ID for cursor pagination. A post with 500k comments shows a ranked first page (computed asynchronously and cached) and paginates the rest. Rate limits and a spam classifier run on write.
- **Hot posts.** The image is a CDN hot object, which CDNs handle well. The post's metadata and counters are a **hot key** for the cache: hydration servers keep a 1-5 s in-process cache with request coalescing, and the shared cache can replicate the key under `post:{id}#k` ([Cache Stampede and Hot Keys](../computer-science/High_Level_Design.md#413-cache-stampede-and-hot-keys)). The first comments page is cached for a second or two.

#### Failure modes and mitigations

| Failure | Impact | Mitigation |
|---|---|---|
| Processing backlog (worker outage, bad deploy) | New posts stay PENDING | Autoscale on queue age; separate queues for fresh uploads and backfills; client keeps showing the local copy |
| Malicious image crashes or exploits the decoder | Worker compromise or crash loop | Sandboxed workers, pixel-count check before decode, DLQ after N attempts |
| CDN provider outage | Images fail to load globally | Multi-CDN with DNS or client-side failover; the origin shield protects the origin from the miss storm |
| URL signing key leaked | Anyone can mint URLs for private photos | Key IDs in URLs, rotation through `kid`, edge accepts only current and previous keys |
| Moderation false negative | Harmful content visible | User reports, post-hoc takedown: state change, object delete, CDN purge by key |
| Counter store lost or corrupted | Wrong like counts | Counters are derived: rebuild from like tables; nightly reconciliation |
| Viral post | Hot cache key, counter contention | In-process caches with coalescing, replicated cache keys, aggregated counter writes |

#### Tradeoffs

| Decision | Chosen | Alternative | Why |
|---|---|---|---|
| Upload path | Presigned direct-to-storage, resumable | Stream through API servers | Keeps ~10 GB/s off the app tier; retries are cheap and resumable |
| Derivatives | Precompute 4 common sizes; rare sizes on demand | All on demand, or precompute everything | Common sizes are hit constantly; on-demand avoids storing unused variants |
| Private media | Signed, expiring URLs; cache key ignores the signature | Proxy every private image through an auth service | Keeps CDN hit ratio; accepts a bounded revocation window |
| Originals | Cold tier after 30 days (or a 2048 px master) | Keep everything hot | ~$1.8M/month saved on one year of data; reprocessing becomes a batch job |
| Like counts | Unique like rows plus 1 s aggregated counters | Increment a counter row per like | Survives 30k likes/s on one post; counts lag by about a second |
| Moderation | Hash matching blocking; classifiers after publish with limited reach | Everything blocking | Blocking classifiers would delay every post on model latency and false positives |

**Main interview tradeoff:** **privacy versus cacheability.** The cheapest way to serve images is a public, immutable URL cached forever at the edge; the safest is to authorize every byte at an origin proxy. Signed, expiring URLs with a signature-free cache key keep the CDN economics while bounding how long a revoked viewer can still fetch bytes. The cost is a revocation window (an hour or two) and a purge path for urgent removals; say both numbers explicitly.

#### Follow-ups with model answers

**Q1. A user deletes a post. Walk through what happens and how fast it disappears.**

The post moves to `DELETED` in the database (synchronously), so every hydration path stops returning it immediately and stops issuing URLs. A `post.deleted` event removes it from cached first pages and counters; feed timelines still hold the ID, but hydration drops it, so no timeline rewrite is needed. Derivative objects are deleted and purged from the CDN by key within minutes; the original follows the same path (or is kept for a legally required retention period in a restricted bucket, if policy says so). State the residual exposure: a viewer who already has a signed URL could fetch the image until purge completes.

**Q2. Product wants short videos too.**

The upload half is the same (presigned resumable uploads, an async pipeline, moderation), but processing becomes transcoding into an adaptive bitrate ladder (HLS or DASH segments at several resolutions), which costs orders of magnitude more compute than image resizing and is often done on GPU or dedicated encoders. Serving shifts to segment delivery from the CDN with the player choosing bitrate. Reuse [Video Streaming Platform](../computer-science/High_Level_Design.md#65-video-streaming-platform) rather than re-deriving it, and keep the same privacy model (signed URLs over the manifest and segments).

**Q3. Users upload the same meme millions of times. Do you dedupe?**

Exact duplicates can be detected by the SHA-256 of the uploaded bytes and stored once, with each photo row pointing at shared derivatives; that saves storage for re-shares of identical files. Near duplicates (re-encoded or resized copies) need a perceptual hash, which is better used for moderation and spam detection than storage savings, because sharing physical objects across users complicates deletion (one user's delete must not remove another's photo) and privacy (a private photo must not be reachable through a public duplicate's URL). Dedupe storage only, never URLs.

**Q4. You want to re-encode the whole back catalog to a new, smaller format. Is it worth it?**

Do the math first. 100B existing photos × ~1 core-second each = 1e11 core-seconds ≈ 28M core-hours; at an assumed $0.02 per core-hour that is ~$560k, plus reading cold originals (retrieval fees). Most views go to recent and popular photos, so re-encode lazily instead: when a photo's derivative is requested N times in a day, enqueue it for re-encoding at low priority. That captures most of the egress savings for a small fraction of the compute.

**Q5. How do you make sure a private account's photo never shows up in a public surface?**

Put authorization at the boundary every surface must cross: the hydration layer that turns post IDs into responses. Feeds, search, explore, notifications, and embeds all receive post IDs from their own indexes, which may be stale, and all call the same `can_view` check with the viewer's identity. Index builders also exclude private posts, but that is defense in depth, not the guarantee. Test it with a privacy regression suite that creates private posts and asserts that no surface returns them to a non-follower.

#### Level signals

- **Mid:** presigned uploads to object storage, async thumbnail generation, CDN for images, metadata in a database, likes in a table.
- **Senior:** idempotent pipeline with a state machine and DLQ; EXIF and decompression-bomb handling; egress and storage numbers drive the design; signed URLs with a signature-free cache key; aggregated or sharded counters for hot posts; reuses the feed design instead of re-deriving it.
- **Staff:** storage-tier cost math and the "do we need originals" product question; explicit revocation windows and takedown purge path; moderation ordering (blocking hash match vs post-publish classifiers); lazy back-catalog re-encoding with a cost estimate; a single authorization boundary for all surfaces.

See also: [News Feed](../computer-science/High_Level_Design.md#63-news-feed), [Object Storage (S3-like)](../computer-science/High_Level_Design.md#614-object-storage-s3-like), [Cache Stampede and Hot Keys](../computer-science/High_Level_Design.md#413-cache-stampede-and-hot-keys), [Mock hint outline](HLD_Mock_Interviews.md#a4-photo-sharing-with-image-processing)

---

### A5. Real-Time Leaderboard

#### Requirements and assumptions

- **Functional:** global top 100 (with names and scores); "what is my rank?" for any player; daily, weekly, and seasonal boards plus an all-time board; per-region boards; a friends leaderboard; players see their new score and rank right after a match.
- **Scale:** 100M players on the global boards, 30M DAU, 5M concurrent at peak.
- **Write rate:** 100k score updates/s average, 300k/s peak (match results from game servers). Each update touches ~5 boards (daily, weekly, season, all-time, region).
- **Read rate:** ~50k/s top-100 views, ~100k/s "my rank" at peak (every match end), ~20k/s friends boards.
- **Freshness:** own score immediately; own rank within ~2 s; top 100 within ~1 s.
- **Exactness:** exact order for the top 1,000 (prizes depend on it); for everyone else an exact rank at score granularity ("#4,213,118, tied with 812 others") or a percentile is acceptable.
- **Integrity:** scores come only from authoritative game servers; implausible scores never reach the visible top tier unverified. Scores are durable; the in-memory structures are rebuildable.
- **Out of scope:** matchmaking, rating systems (Elo, Glicko), reward fulfillment beyond computing final ranks.

#### Capacity estimate

```text
Memory:          sorted-set entry (skip-list node + hash entry + member) ≈ 100 B
                 100M players × 100 B ≈ 10 GB per board; 5 active boards ≈ 50 GB -> memory is NOT the problem
Board writes:    300k updates/s peak × 5 boards                          = 1.5M sorted-set writes/s
One sorted set:  ZADD is O(log n); log2(1e8) ≈ 27 skip-list levels, most of them cache misses
                 assume ~100-200k ZADD/s per Redis instance on a 100M-member set (single-threaded execution)
                 a key cannot be split across shards: 1.5M/s ÷ ~150k/s ≈ 10x over one instance
Rank reads:      100k ZREVRANK/s peak would share the same thread as the writes
Failover:        a 10 GB key: reload from snapshot ≈ 1-2 min; a full replica resync ships 10 GB
Rebuild:         100M player_score rows ≈ 5 GB scan; reinserting at ~1M/s ≈ 100 s per board
Histogram:       integer scores 0..1,000,000 -> 1M buckets × 8 B = 8 MB per board; merging 32 partial
                 histograms and recomputing prefix sums ≈ 32M additions ≈ tens of ms per second
Top tier:        players with score >= T, T chosen so ~100k qualify: 100k × 100 B = 10 MB per board;
                 updates that land in it: well under 1% of all updates -> a few thousand writes/s
Friends board:   ~200 friends -> 200 point reads per request; 20k req/s × 200 = 4M point reads/s
                 (cache each viewer's friends board for ~10 s)
```

**What the numbers decide:** a single sorted set holds 100M players easily, but **write throughput** (1.5M/s across boards on a single-threaded key that cannot be split), rank reads on the same thread, and a minutes-long failover make it the wrong primary structure. Only the top of the board needs exact order, and it is tiny (~10 MB). Everyone else's rank can come from an **8 MB score histogram** that is cheap to update, cheap to merge across shards, and answers rank in O(1).

#### Interfaces and data

```text
POST /internal/v1/score_events     (game servers only: mTLS + signed match result)
     { event_id, match_id, player_id, kind: DELTA | VALUE, amount, achieved_at, server_sig } -> 202
GET  /v1/leaderboards/{board_id}/top?limit=100        -> { as_of, entries: [{ rank, player_id, name, score }] }
GET  /v1/leaderboards/{board_id}/players/{player_id}  -> { score, rank, tied_with, rank_exact, percentile, as_of }
GET  /v1/leaderboards/{board_id}/friends/{player_id}  -> [{ rank_among_friends, player_id, score }]
board_id = "{game}:{scope}:{window}"   e.g. g1:global:season-12, g1:global:2026-11-04, g1:eu:2026-W45

score_event log (partitioned by player_id, 30-day retention)      -- ordered input, replayable
player_score(board_id, player_id, score, achieved_at, last_event_id, version)
       PRIMARY KEY (board_id, player_id)                         -- durable truth, sharded by player_id
processed_match(player_id, match_id)  PRIMARY KEY                -- dedupe of cumulative deltas
lb:{board}:top        sorted set: only players with score >= T(board), ~100k members, exact order
hist:{board}:{p}      bucket counts per aggregator partition p (score -> count), merged every 1 s
board_meta(board_id, window_start, window_end, state OPEN | FROZEN | FINAL, threshold_T, final_snapshot_ref)
```

Everything per player is partitioned by `player_id`: one partition of the event log and one updater own each player, so a player's updates are applied in order without locks, and the old-to-new score transition needed by the histogram is computed in one place. The structures keyed by board (top tier, merged histogram) are small and are replicated to readers rather than sharded.

#### Architecture and flow

```text
Game servers (authoritative) --signed match result--> Score ingest --> Validation (signature, dedupe,
                                                                         plausibility, rate limits)
                                                                          | accepted        | suspicious
                                                                          v                 v
                                                    score_event log (by player_id)     Anti-cheat review
                                                                          |
                                                                          v
                                    Score updaters (one per log partition): per board, old -> new score,
                                    upsert player_score (conditional on version), emit (board, old, new)
                                          |                               |                         |
                                          v                               v                         v
                                 player_score store             Histogram aggregators        Top-tier writer
                                 (sharded by player_id)         (bucket deltas, 32 parts)    (new >= T and verified)
                                          ^                               | merge every 1 s          |
                                          |                               v                          v
Clients --> Leaderboard API --------------+------ my rank ------> Rank servers (prefix sums,   Top-tier sorted set
               | friends board: graph + multi-get                  8 MB per board, replicated) per board (+ replica)
               +--- top 100 (cached 1 s, CDN for public JSON) ------------------------------------+
```

**Write path:**

1. A game server submits a signed match result. Ingest verifies the signature, drops duplicate `event_id`s, runs cheap plausibility checks, and appends to the score log (partition = `player_id`).
2. The updater for that partition dedupes on `(player_id, match_id)`, computes the new score for each affected board (cumulative within a window; best-ever for all-time), and writes `player_score` with a version check.
3. It emits `(board, old_score, new_score)` to the histogram aggregator for its partition, and, if `new_score >= T` and the score is verified, updates the board's top-tier sorted set (removing the player if they fell below T).

**Read path:**

1. **Top 100:** `ZREVRANGE lb:{board}:top 0 99 WITHSCORES`, cached for 1 s with request coalescing, so 50k views/s cost about one read per second per board.
2. **My rank:** the API reads the player's score from `player_score`. If it is at least T, it returns the exact `ZREVRANK` from the top tier; otherwise it asks a rank server for `1 + count(score > s)` from the merged histogram.
3. **Friends:** fetch the friend list, multi-get their `player_score` rows (grouped by shard, pipelined), sort ~200 entries in memory, and cache the result for the viewer for ~10 s.

#### Deep dive: why one sorted set does not scale, and how to shard

A sorted set (skip list plus hash) is the right primitive: `ZADD`, `ZREVRANK`, and `ZREVRANGE` are O(log n). The problem is purely operational: one key lives on one shard, Redis executes commands on one thread, and every board write, every rank query, and every replication byte for that board funnel through it. The options:

| Approach | Writes | Top K | "My rank" | Weak spots |
|---|---|---|---|---|
| **One sorted set per board** | All on one thread (~150k/s) | One `ZREVRANGE` | One `ZREVRANK` | ~10x short of 1.5M writes/s; minutes-long failover; reads compete with writes |
| **Shard by player** (`hash(player) % 32`) | Spread evenly (~47k/s per shard) | Merge 32 × top-100 lists every second | Sum of `ZCOUNT(s, +inf)` over 32 shards | 32 calls per rank query: 100k/s × 32 = 3.2M commands/s; ranks are sums of slightly different instants |
| **Shard by score range** (shard i holds `[b_i, b_i+1)`) | Local, plus a move (ZREM + ZADD on two shards) when a score crosses a boundary | Top shard only | `ZREVRANK` in own shard + cached member counts of higher shards | Skew: most players have low scores; boundaries must track quantiles; a season reset puts everyone in one shard; non-atomic moves |
| **Exact top tier + score histogram** (chosen) | Histogram deltas are O(log B) array updates; top tier sees under 1% of writes | Top-tier `ZREVRANGE` | Top tier exact; everyone else `1 + count(score > s)` from prefix sums | Order among tied players is unknown; tier threshold must be maintained |

Shard-by-player sorted sets remain useful as an **optional exact path** (rate-limited, for support tools or "show my exact position among ties") and as a way to list neighbors; they are not the main read path.

#### Deep dive: rank from a histogram, the top tier, and ties

**Histogram rank.** Keep, per board, a count of players at each integer score. The number of players **strictly above** score `s` is a suffix sum, so a player's standard competition rank is `1 + count(score > s)`, **exact at score granularity**. Each aggregator partition maintains a partial histogram (it owns 1/32 of the players, so it can apply `-1` at the old score and `+1` at the new score without coordination). Every second the rank servers sum the 32 partial arrays and rebuild prefix sums (tens of milliseconds); a rank query is then one array lookup. With continuous or unbounded scores, use log-scale buckets and interpolate within a bucket; the error is bounded by the bucket's population, and the API returns `rank_exact: false`.

A Fenwick tree gives the same answers with O(log B) updates and queries, which is convenient inside an aggregator:

```python
"""rank_histogram.py -- exact "players strictly above me" from a score histogram (Fenwick tree)."""
import random


class ScoreHistogram:
    def __init__(self, max_score: int) -> None:
        self.n = max_score + 1
        self.tree = [0] * (self.n + 1)          # 1-based Fenwick tree over score buckets
        self.total = 0

    def _add(self, score: int, delta: int) -> None:
        i = score + 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    def _prefix(self, score: int) -> int:        # players with score <= `score`
        i, s = score + 1, 0
        while i > 0:
            s += self.tree[i]
            i -= i & -i
        return s

    def update(self, old: int | None, new: int) -> None:
        if old is not None:
            self._add(old, -1)
        else:
            self.total += 1
        self._add(new, +1)

    def rank(self, score: int) -> int:           # 1 + number of players strictly above
        return 1 + self.total - self._prefix(score)


if __name__ == "__main__":
    rng = random.Random(7)
    hist, scores = ScoreHistogram(max_score=10_000), {}
    for _ in range(50_000):                       # a stream of score updates
        player, new = rng.randrange(5_000), rng.randrange(10_001)
        hist.update(scores.get(player), new)
        scores[player] = new
    for player in rng.sample(sorted(scores), 20):  # compare against a brute-force sort
        s = scores[player]
        assert hist.rank(s) == 1 + sum(1 for v in scores.values() if v > s)
    print("players:", hist.total, "rank of score 9000:", hist.rank(9_000))
```

Histograms are also **mergeable**: per-partition, per-region, or per-shard arrays simply add, which is what makes this design shard and replicate cleanly (see Q4). Related ideas for approximate counting at scale are in [Probabilistic Counting](../computer-science/High_Level_Design.md#410-probabilistic-counting-hyperloglog-and-count-min-sketch).

**The top tier.** Prizes and the visible top 100 need a total order, including ties, so the top of each board lives in an exact sorted set. Choose the threshold T from the histogram so that about 100k players qualify (`count(score >= T) ≈ 100k`), and recompute it every few minutes. Only updates with a new score at least T touch the tier, and the tier is trimmed with `ZREMRANGEBYSCORE` when T rises. At 100k members it is 10 MB, reloads in well under a second, and can be rebuilt from `player_score WHERE score >= T`.

**Tie-breaking.** "Earlier achiever ranks higher" must be encoded in the sort key. Redis scores are IEEE doubles, which represent integers exactly up to 2^53. Pack both fields:

```text
composite = score × 2^32 + (2^32 - 1 - t)      t = seconds since the season started (fits in 32 bits)
  higher score sorts first; for equal scores, smaller t (earlier) gives a larger composite
  exact while score < 2^21 ≈ 2.1M, because 21 + 32 = 53 bits
example: score 1,500, t = 86,400 (1 day in)  -> 1,500 × 4,294,967,296 + 4,294,880,895 = 6,446,745,824,895
```

If scores can exceed 2^21, keep the raw score in the sorted-set score and put the tie-break in the member (Redis orders equal scores by member bytes), for example a fixed-width `(MAX_T - t)` prefix followed by the player ID. Outside the top tier, the histogram already reports "tied with N others" honestly instead of inventing an order.

#### Deep dive: windows, friends boards, and anti-cheat

- **Windows are separate boards, not resets.** Each window has its own `board_id`. An event updates every board whose window contains the event's `achieved_at` (not its arrival time). Starting a new day creates new, empty structures; nothing deletes 100M members at midnight. Daily boards only contain players active that day (~30M, ~3 GB in a sorted set; 8 MB as a histogram).
- **Closing a window.** Accept late events until `window_end + grace` (for example 5 minutes, enough for game servers to flush), then mark the board `FROZEN`; updaters drop later events for it. Snapshot the top tier and the histogram to durable storage as the **final standings** and compute rewards from that snapshot in an idempotent batch job keyed by `(board, player)`. Old boards expire from memory after archiving.
- **Friends boards are computed on read.** Precomputing a board per player would fan out every score change to every friend's board (200 writes per update, 60M writes/s at peak). Reading ~200 scores and sorting them costs a few milliseconds; caching the result per viewer for ~10 s keeps the point-read load manageable. Cap friend lists (for example 5,000) so the worst case stays bounded.
- **Never trust the client.** Only game servers submit scores, signed with a fleet key, and each result carries a `match_id` that is deduplicated (cumulative scores make duplicate deltas a real bug, since `ZINCRBY` is not idempotent).
- **Validation path.** Cheap synchronous checks at ingest: signature, rate per player, score per minute of match time, impossible stats. Asynchronous anomaly detection looks at distributions (for example a player suddenly in the 99.99th percentile with a new device). **Gate the top tier:** any update that would enter it, or jump a player by more than a large percentile step, is held as "pending" until verified (server-side replay of the match log, or review); the player sees their own pending score, others do not.
- **Removal.** Banning a cheater removes them from every top tier, subtracts them from every histogram (an update with `new = none`), marks their `player_score` rows banned, and, if a window is already final, triggers a recompute of that window's rewards from the corrected snapshot.

#### Failure modes and mitigations

| Failure | Impact | Mitigation |
|---|---|---|
| Top-tier node fails | Top 100 and exact top ranks unavailable | Replica promotion; or rebuild ~100k rows from `player_score` in about a second |
| Histogram aggregator crashes | Its partition's deltas stop; ranks drift slightly stale | Restore partial histogram from a checkpoint stored with the log offset and replay; hourly full recompute from `player_score` (~100M rows, a minute or two) corrects any drift |
| Duplicate score events | Cumulative scores double-counted | `event_id` dedupe at ingest, `(player_id, match_id)` dedupe in the updater, versioned upserts |
| Event log lag during a tournament | Ranks behind reality | Responses carry `as_of`; autoscale updaters; prioritize partitions by lag |
| Season-end read spike on the top 100 | Hot key on the top tier | 1 s cache with coalescing; serve the public top-100 JSON through the CDN |
| Cheater reaches the visible top | Trust and prize integrity | Top-tier gate requires verification; removal path recomputes final standings |
| Late events after a window closes | Inconsistent final standings | Grace period, then `FROZEN` state checked by updaters; final snapshot is the only input to rewards |

#### Tradeoffs

| Decision | Chosen | Alternative | Why |
|---|---|---|---|
| Rank structure | Exact top tier + score histogram | One sorted set per board | 1.5M writes/s cannot go through one single-threaded key; only the top needs exact order |
| Sharding | By player for truth and updates; boards as small replicated summaries | Shard sorted sets by score range | No boundary moves or skew; histograms merge by addition |
| Rank for most players | Exact at score granularity, ties reported | Exact position among ties | Ordering 812 tied players at rank 4M has no product value and real cost |
| Tie-breaking | Composite score (earlier wins) in the top tier | Arbitrary member order | Deterministic and explainable; matters where prizes are decided |
| Windows | New board per window, freeze and snapshot | Reset scores in place | No mass deletes; final standings are reproducible |
| Friends board | Computed on read, cached 10 s | Precomputed per player | Avoids 200x write fan-out per score change |

**Main interview tradeoff:** **exactness versus cost of rank.** An exact global order for 100M players needs one ordered structure that every write goes through, or a scatter-gather on every rank query. Restricting exact order to the small top tier where it matters (prizes, the visible top 100), and answering everyone else with a histogram that is exact at score granularity and a second stale, removes the bottleneck. State the error contract to the product team: exact top 100k, exact "players above you" for everyone, unknown order within ties.

#### Follow-ups with model answers

**Q1. Show the five players directly above and below me.**

For a top-tier player, `ZREVRANGE` around their rank answers it directly. For everyone else, the neighbors are the players with the nearest scores: keep a secondary index on `(board_id, score, player_id)` in each `player_score` shard, query the 5 nearest above and below on every shard, and merge (32 shards × 10 rows). It is a scatter-gather, so cache it per player for ~30 s and rate-limit it; the histogram still provides the rank number.

**Q2. Can you just use a relational database with an index on score?**

`SELECT COUNT(*) FROM player_score WHERE board_id = ? AND score > ?` walks every index entry above the score, because ordinary B-trees do not store subtree counts. For a player ranked 50 millionth, that is a 50M-entry scan per request; at 100k requests/s it is hopeless. Order-statistic trees (skip lists with span counts, as in Redis sorted sets) or precomputed histograms make rank O(log n) or O(1). The database stays useful as the durable truth and for rebuilding.

**Q3. The season ends. How are rewards computed for 100M players?**

Freeze the board after the grace period and snapshot the top tier and histogram as the final standings. Reward tiers are mostly percentile-based ("top 1%", "top 10%"), which come straight from histogram suffix sums; exact prizes for the top 1,000 come from the frozen top tier with its tie-break. A batch job writes grants keyed by `(season, player)` so reruns are idempotent. If a cheater is banned afterward, recompute from the corrected snapshot and adjust only the affected grants.

**Q4. Players are spread over three regions. How do you build a global board?**

Ingest and score updates stay in each player's home region. Each region publishes its histogram per board every second; the global histogram is the element-wise sum, so a global rank is still `1 + count(score > s)` over the summed array, a few seconds stale. The global top tier is the merge of each region's top tier (top-K of the union). No cross-region coordination is needed on the write path, which is the main advantage of mergeable summaries.

**Q5. The score is a race time where lower is better, measured in milliseconds.**

Invert the comparison (count players strictly faster). Times are bounded (for example under 10 minutes = 600,000 ms), so a 600k-bucket histogram at millisecond resolution is still under 5 MB and remains exact. For unbounded values, use log-scale buckets (for example 1% wide) and interpolate within a bucket, returning `rank_exact: false` outside the top tier.

#### Level signals

- **Mid:** a sorted set with `ZADD`, `ZREVRANK`, and `ZREVRANGE`; separate keys per window; durable scores elsewhere; knows `ORDER BY` over 100M rows per request is wrong.
- **Senior:** shows with numbers why one sorted set is not enough; compares shard-by-player and shard-by-score-range with their costs; separates exact top-K from bucketed rank; deterministic tie-breaking; idempotent cumulative updates; window freeze and snapshot.
- **Staff:** defines the exactness contract with product; uses mergeable histograms to make sharding, multi-region, and rebuilds simple; designs the anti-cheat gate around the top tier and the removal and reward-recompute path; plans rebuild times and the season-end spike.

See also: [Partitioning and replication](../computer-science/High_Level_Design.md#45-partitioning-and-replication), [Cache Stampede and Hot Keys](../computer-science/High_Level_Design.md#413-cache-stampede-and-hot-keys), [Probabilistic Counting](../computer-science/High_Level_Design.md#410-probabilistic-counting-hyperloglog-and-count-min-sketch), [Mock hint outline](HLD_Mock_Interviews.md#a5-real-time-leaderboard)

---

### A6. Ad-Click Aggregation

#### Requirements and assumptions

- **Input:** click events from click-edge servers. The ad server signs an **impression token** when it renders an ad; the click URL carries that token, and the edge server records the click and redirects the user to the advertiser's page.
- **Output:** valid click counts per ad per minute (event time), rolled up to hour and day, per advertiser and campaign.
- **Billing definition:** at most **one billable click per impression**. Transport retries (same click ID) and user double clicks or reloads (new click ID, same impression) count once. Tokens expire 1 hour after the impression is served; clicks on expired tokens are recorded as invalid, not billed.
- **Scale:** 1B clicks/day, peak about 50k/s. Up to 1M distinct ads clicked in one peak minute.
- **Freshness:** dashboard numbers within about 1 minute of the minute closing (p99 under 2 minutes).
- **Exactness:** the daily billable total per ad is exact with respect to the raw archive: every valid click counted once, reproducibly. The invoice closes at T+1 06:00 UTC; anything learned later becomes an explicit adjustment on the next invoice, never a silent rewrite of a closed day.
- **Durability:** a click acknowledged by the edge (the redirect served after a successful log write) is never lost. Raw events are kept forever in an archive for audits and disputes.
- **Out of scope:** ad serving and auctions, budget pacing (it consumes this stream), fraud-model training.

#### Capacity estimate

```text
Clicks:        1B/day ÷ 86,400 ≈ 11.6k/s average; peak ≈ 50k/s
Impressions:   ~100B/day at 1% CTR ≈ 1.16M/s -- NOT ingested here; tokens are verified statelessly by signature
Event size:    ~250 B (click_id 16 B, impression token ~100 B, ad/campaign/advertiser ids, timestamps, ip/ua hashes)
Ingress:       50k/s × 250 B = 12.5 MB/s peak; 1B × 250 B = 250 GB/day raw
Log:           7-day retention × 250 GB × RF 3 ≈ 5.3 TB across the cluster
Partitions:    12.5 MB/s fits in ~2 partitions at 10 MB/s each; use 64 for parallelism and headroom
Archive:       250 GB/day ≈ 91 TB/year raw, ~20-30 TB/year as compressed Parquet

Dedupe state:  key = impression_id; must outlive token lifetime (1 h) + stream lateness (1 h) -> keep 3 h
               peak-hour bound: 50k/s × 10,800 s = 540M keys; typical 11.6k/s × 10,800 ≈ 125M keys
               × ~40 B per entry in RocksDB ≈ 5 GB typical, 22 GB worst case; ÷ 64 tasks ≈ 80-340 MB each
Window state:  ≤ 1M ads × 61 open minutes (60 min allowed lateness) × ~50 B ≈ 3 GB worst case
Output rows:   distinct (ad, minute) pairs: ~300k/minute average × 1,440 ≈ 430M rows/day
               ≤ 1M upserts/minute ≈ 17k upserts/s at peak, plus corrections
OLAP storage:  430M rows × ~40 B compressed ≈ 17 GB/day; 90 days at minute grain ≈ 1.5 TB; hourly rollups beyond
```

**What the numbers decide:** ingress (12.5 MB/s) is trivial, so throughput is not the design driver; correctness is. Dedupe state is a few GB, so it fits as **local keyed state inside the stream job**, checkpointed together with the counts, instead of a remote lookup per click. The output (hundreds of millions of rows per day, queried by advertiser and time range) needs a **columnar OLAP store** with rollups, not an OLTP database.

#### Interfaces and data

```text
Click edge:
  GET /c?t=<impression_token>&u=<dest_url_id>  -> 302 Location: advertiser landing page
      verify HMAC(token) with key id kid; assign click_id (UUIDv7); produce to clicks.raw (acks=all,
      idempotent producer); on log failure spool to local disk; then redirect

impression_token = base64( impression_id | ad_id | campaign_id | advertiser_id | served_at | expires_at | kid
                           | HMAC-SHA256(k_kid, all previous fields) )

ClickEvent (Protobuf, topic clicks.raw, 64 partitions, key = impression_id, RF 3, 7 days):
  { click_id, impression_id, ad_id, campaign_id, advertiser_id,
    event_time_ms (edge server clock at click), ingest_time_ms, ip_prefix, ua_hash, token_status, schema_v }

Query API:
  GET /v1/advertisers/{id}/clicks?ad_ids=..&from=..&to=..&granularity=minute|hour|day
      -> [{ ad_id, window_start, clicks, invalid_clicks, version, final: bool }]

ad_clicks_minute (OLAP, e.g. ClickHouse ReplacingMergeTree(version)):
  PARTITION BY toDate(window_start)  ORDER BY (advertiser_id, ad_id, window_start)
  columns: clicks, invalid_clicks, version, source ('stream'|'batch'), pipeline_version
  logical unique key (ad_id, window_start); highest version wins
billing_ledger (PostgreSQL): PRIMARY KEY (advertiser_id, ad_id, day)
  billable_clicks, cost_micros, run_id, closed_at
billing_adjustment (PostgreSQL): adjustment_id PK, advertiser_id, ad_id, day, delta_clicks, reason, invoice_id
archive_manifest: (topic, partition, hour) PK, first_offset, last_offset, object_key, row_count
```

Partition the raw topic by **impression_id**, not ad ID: it spreads load uniformly (a viral ad cannot create a hot partition) and puts all clicks of one impression in one task, so dedupe is local. Counting by ad happens after a second, much smaller shuffle of partial counts. The OLAP table is ordered by advertiser first because every dashboard query filters by advertiser.

#### Architecture and flow

```text
Browser/app --click--> Click edge (every region; stateless; verifies token signature)
                         | produce, acks=all, idempotent producer; local disk spool if the log is unreachable
                         v
             Log: clicks.raw (64 partitions, key = impression_id, RF 3, 7 days)
               |                                               \
               v                                                \--> Archiver --> object store: hourly Parquet
   Stream job (Flink-style; checkpoint every 10 s; exactly-once state)        + archive_manifest (offset ranges)
     stage 1 (keyed by impression_id):                                                  |
        token/expiry/fraud rules -> dedupe (RocksDB, 3 h TTL) -> partial count per      |
        (ad, minute) per task, event-time windows, watermark = max seen - 30 s          |
     stage 2 (keyed by ad_id): sum partials; allowed lateness 60 min -> corrections     |
     side outputs: very late -> clicks.late ; invalid -> clicks.invalid                 v
               |                                                   Batch reconciliation (hourly + daily T+1)
               v                                                   same dedupe/fraud library over the archive
   OLAP store: upsert (ad_id, window_start, version)  <---- batch overwrite (source='batch') ---|
               |                                                                            v
   Query service + 30 s result cache --> advertiser dashboards      Billing ledger (closed daily) + adjustments
```

**Write path:**

1. The user clicks; the edge verifies the token signature and expiry, stamps `event_time` from its own NTP-disciplined clock, assigns `click_id`, and produces to `clicks.raw` with `acks=all`. Only then does it return the 302. If the log is unreachable it appends to a local spool (fsync batched every 10 ms) and redirects; a spool shipper replays later, and those events arrive late.
2. Stage 1 validates, applies inline fraud rules, and checks keyed state `seen[impression_id]`. A first click is recorded and counted into the task's partial window for `(ad_id, minute)`; repeats are counted only as `duplicate` metrics.
3. When the watermark passes a minute's end, each stage-1 task emits its partial `(ad_id, minute, count)` records keyed by `ad_id`. Stage 2 sums them and upserts the absolute total, with a version, into the OLAP store.
4. A late event inside allowed lateness re-emits the partial and stage 2 upserts a corrected total with a higher version. Beyond that it goes to `clicks.late`.
5. The archiver writes every raw event, untouched, to hourly files and records exact offset ranges in the manifest.

**Read path:** the dashboard queries the OLAP store through the query service (`argMax(clicks, version)` or `FINAL` so unmerged duplicates of a row are not double counted), with results cached for 30 s per query. Finance reads only the billing ledger.

#### Deep dive: what counts, and deduplicating it

There are two different kinds of duplicates, and a design that handles only one is wrong:

| Duplicate | Cause | Same click_id? | Handled by |
|---|---|---|---|
| Transport | Producer retry, spool replay after edge crash, consumer replay after restore | Yes | Idempotent producer (within a session), plus impression dedupe for everything else |
| Semantic | Double click, page reload, back-and-forward, bot hammering one ad | No | One billable click per `impression_id` |

Deduplicating on `impression_id` covers both. The **signed token** is what makes the impression ID trustworthy: the edge verifies an HMAC with a rotating key (the `kid` field selects it), so nobody can mint clicks for arbitrary ads or replay a token after it expires, and the edge does so without looking anything up in the 1.16M/s impression stream.

**Where the dedupe state lives matters more than how it is stored.** Keep it as keyed state in the same job as the counts, so it is checkpointed atomically with them and with the source offsets. Consider the alternative, a Redis `SETNX seen:{impression_id}`: the job processes a click, sets the key, then crashes before the next checkpoint. On restore it replays from the last checkpoint's offsets, the click arrives again, Redis says "seen", and the click is dropped. Counts are now low by every click processed in the lost interval. External side effects are not rolled back by a checkpoint restore, which is the core reason exactly-once frameworks insist on managed state.

State size is bounded by a TTL: an impression can produce a billable click only within its 1-hour token lifetime, and the stream accepts events up to 1 hour late, so 3 hours of keys (5-22 GB, computed above) is enough. Do not use a Bloom filter as the only check: a 1% false-positive rate means 1% of genuine clicks are silently not billed. A Bloom filter in front of RocksDB as a "definitely new" fast path is fine ([4.9](../computer-science/High_Level_Design.md#49-bloom-filters-and-merkle-trees)).

#### Deep dive: event time, watermarks, and late data

Windows use **event time from the edge server**, never the client device clock (which can be wrong by hours or forged) and never processing time (which would change results on replay). The mechanics of tumbling windows, watermarks, and allowed lateness are in [HLD 4.11](../computer-science/High_Level_Design.md#411-stream-processing); here are the choices and why:

- **Watermark:** per log partition, `max event time seen - 30 s`, minimum across inputs. Partitions with no traffic for 60 s are marked idle so they do not stall every window. The 30 s comes from the measured p99.9 of `ingest_time - event_time` in normal operation (cross-region mirroring is the main contributor). A minute's first result therefore lands about 30-45 s after the minute ends.
- **Allowed lateness: 60 minutes.** Late events within it update the window, and stage 2 upserts a corrected total. Each additional hour costs another ~60 open windows per active ad, so the state grows linearly; hours of edge outage are handled by the batch tier, not by more lateness.
- **Lateness tiers, end to end:**

| Arrival delay (ingest minus event time) | Path | Visible on dashboard | On the invoice |
|---|---|---|---|
| Under 30 s | On-time window firing | Within ~1 minute | Yes |
| 30 s to 61 min | Correction upsert, version + 1 | Within ~1 minute of arrival | Yes |
| 61 min until the day closes (T+1 06:00 UTC) | Side output `clicks.late`; hourly batch recount from the archive overwrites the affected rows with `source='batch'` | Within ~1 hour | Yes |
| After the day closes | Daily batch for the closed day finds a positive delta | Batch overwrite | Adjustment line on the next invoice |

Late **fraud** verdicts follow the same shape. A click-farm detector that runs on hours of data emits a list of invalid impression IDs; the batch recount excludes them, the dashboard row is overwritten, and if the day was already invoiced the difference becomes a negative adjustment (a credit).

#### Deep dive: exactly-once end to end, and reconciliation

Walk every hop; the chain is only as strong as its weakest link:

1. **Edge to log:** `acks=all` with `min.insync.replicas=2` means an acknowledged write survives a broker loss. The idempotent producer (producer ID plus per-partition sequence numbers) discards retried batches within a producer session. A crash and restart starts a new session, so a resend can still duplicate; impression dedupe absorbs that.
2. **Log to job:** source offsets are stored in the checkpoint, not committed independently.
3. **Job state:** barrier-aligned checkpoints every 10 s snapshot dedupe state, partial windows, stage-2 sums, and offsets as one consistent cut. A failure restores the cut and replays at most ~10 s plus restart time of input.
4. **Job to sink:** stage 2 writes **absolute** totals keyed by `(ad_id, window_start)`, never increments. A replay writes the same key again; the final value converges to the same sum because the set of events in the window is the same. During the replay, a dashboard can briefly show an older total for a minute it already displayed. That is acceptable for the dashboard because billing never reads the stream rows. If even that is unacceptable, use a **transactional sink**: stage 2 writes to an output topic inside a transaction committed with each checkpoint, and the OLAP store ingests with `read_committed`. Nothing uncommitted is ever visible, at the cost of up to one checkpoint interval (10 s) of extra latency.

**Reconciliation** is the lambda-style safety net, and it is the billing source of truth:

- The archiver's manifest records, per partition and hour, the exact offset range written. Before a batch run counts an hour, it checks that the ranges are contiguous with no gaps and that row counts equal offset deltas. An archiver bug therefore stops the close instead of silently under-billing.
- The batch job runs the **same dedupe and fraud library** (one versioned artifact, compiled into both the stream job and the batch job, or the stream job run in batch mode over the archive) over all events with event time in the day, including everything that arrived late.
- It compares per-ad daily totals with the stream totals. Expected differences come only from the late and fraud tiers; an unexplained difference above 0.01% for any advertiser pages the on-call engineer and blocks that advertiser's close.
- The batch writes `billing_ledger` rows with the run ID, code version, and input manifest, so any invoice can be reproduced bit for bit during a dispute.

**Hot ads.** Stage 1 is keyed by impression ID, so a Super Bowl ad drawing 20k clicks/s is spread across all 64 tasks (about 300/s each). Each task pre-aggregates, so stage 2 receives at most 64 partial records per ad per minute, regardless of click volume. Without the combiner, keying by `ad_id` would put 20k/s of RocksDB updates on one task and one partition. On the read side, a popular advertiser's dashboard is served from the 30 s result cache and from hourly rollups for long ranges.

**Query store sizing.** A typical query, "per-minute clicks for 50 ads over 7 days", reads 50 × 10,080 = 504k rows from a table ordered by `(advertiser_id, ad_id, window_start)`, which a columnar store scans in milliseconds. Materialized hourly and daily rollups serve ranges beyond 90 days, when minute rows expire.

#### Failure modes and mitigations

| Failure | Impact | Mitigation |
|---|---|---|
| Edge cannot reach the log | Clicks would be lost | Local disk spool with fsync; replay later as late data; alert on spool age; a lost disk loses only unshipped clicks (bounded, measured) |
| Stream task crash | Up to ~10 s of input reprocessed | Restore checkpoint; absolute-value upserts make replays harmless |
| One idle partition stalls the watermark | No windows fire; dashboard freezes | Idleness detection; alert on watermark lag above 2 minutes |
| Bug in dedupe or fraud rules deployed | Wrong counts | Reconciliation diff pages on mismatch; fix, replay from the log (7 days) or archive into a new `pipeline_version`, then switch the query alias |
| OLAP store unavailable | Sink backpressures; dashboard stale | Checkpoints continue with sink buffering, or the transactional output topic buffers; billing unaffected |
| Archiver gap | Batch would under-bill | Manifest completeness check blocks the close until the gap is re-archived from the log |
| Edge clock skew | Clicks land in wrong minutes | NTP monitoring; reject or clamp `event_time` more than 5 s ahead of `ingest_time`; quarantine skewed edges |
| Token signing key leaked | Forged clicks | Rotate `kid`, reject the old key, credit affected advertisers from the archive |

#### Tradeoffs

| Decision | Chosen | Alternative | Why |
|---|---|---|---|
| Dedupe key | `impression_id` (one billable click per impression) | `click_id` only | Click ID catches transport retries but not double clicks, which are the bigger billing dispute |
| Dedupe state | Keyed state in the job, checkpointed with counts | External Redis or database lookups | Only managed state is rolled back consistently on restore; also avoids 50k/s remote calls |
| Sink | Absolute-value idempotent upsert | Transactional 2PC sink | Simpler and lower latency; billing does not read transient stream values |
| Billing source of truth | Daily batch over the immutable archive | Stream totals | Includes very late and fraud corrections; reproducible for audits |
| Partition key of raw topic | `impression_id` | `ad_id` | Uniform load and local dedupe; hot ads handled by pre-aggregation |
| Allowed lateness | 60 minutes in the stream | Hours or days | State grows linearly with lateness; the batch tier covers the long tail cheaply |

**Main interview tradeoff:** freshness against finality. The stream gives advertisers a number within a minute, and it is exactly-once with respect to the events it has seen, but it cannot see events that arrive hours late or fraud verdicts computed later. The batch tier sees everything and is reproducible, but only after the day ends. Running both, with the same code and an explicit rule that invoices come from the batch and later discoveries become adjustments, is the honest answer. Pretending one pipeline can be both instantly fresh and permanently final is the mistake.

#### Follow-ups with model answers

**Q1. Why not just increment a counter in a database for each click?**

At 50k/s, every increment for a popular ad hits one row, which serializes on a row lock at a few thousand updates per second. Worse, a retried request increments twice, and there is no record of which clicks were counted, so there is nothing to dedupe against, replay, or audit. Counts would be neither exact nor reproducible. Aggregating from an immutable log keeps the raw facts and makes the count a deterministic function of them.

**Q2. An advertiser disputes their bill for one day. How do you answer?**

The ledger row records the batch run ID, the code version, and the archive manifest it read. Re-run that exact version over the same archive files to reproduce the number, then produce the evidence: the list of billable click IDs with timestamps and impression IDs, and the excluded clicks grouped by reason (duplicate impression, expired token, fraud rule ID). If the dispute reveals a bug, the correction is an adjustment on the next invoice, computed by the fixed version over the same inputs.

**Q3. Product also wants unique users per ad per day. Same pipeline?**

Same input, but not billing-grade. Exact distinct counts per ad per day would need a set of user hashes per ad, which is large. Use HyperLogLog per `(ad, day)`: about 12 KB per sketch for roughly 0.8% standard error, mergeable across minutes and partitions, so hourly sketches roll up into daily ones. Label it as an estimate on the dashboard. See [HLD 4.10](../computer-science/High_Level_Design.md#410-probabilistic-counting-hyperloglog-and-count-min-sketch).

**Q4. How do you deploy a new version of the fraud rules without corrupting counts?**

Treat it as a new pipeline version, not an in-place change. Start the new job from a savepoint (or from the log at a chosen offset), writing rows with `pipeline_version = n + 1` into a shadow table. Compare it with the current version for a few hours: differences should be explainable by the rule change alone. Then switch the query alias and stop the old job. The batch reconciliation picks up the new library version on the next close, and the version is recorded in the ledger for reproducibility.

**Q5. Clicks come from five regions. Where do you aggregate?**

Mirror every region's raw topic to one aggregation region: total ingress is 12.5 MB/s, so cross-region bandwidth is negligible, and a single job sees every click of an impression, which keeps dedupe correct even if a user's clicks are routed to two regions. Keep a warm standby job in a second region consuming its own mirror, with checkpoints replicated to object storage there. If the aggregation region fails, the standby restores from the latest replicated checkpoint and continues; mirroring delay makes some clicks late, which the lateness tiers already handle. Per-region aggregation with a global sum is possible, but then cross-region duplicate impressions need a second dedupe stage.

#### Level signals

- **Mid:** log plus stream processor plus OLAP store; windows per minute; dedupe on click ID; knows the batch job exists.
- **Senior:** distinguishes transport and semantic duplicates; dedupe state checkpointed with counts and explains why external dedupe breaks on replay; event-time windows with a justified watermark and tiered late-data policy; absolute-value upserts; pre-aggregation for hot ads; sizes state.
- **Staff:** defines the billing contract (closed days, adjustments, dispute reproducibility); makes reconciliation a gate with manifest completeness checks and diff thresholds; runs one versioned library in stream and batch to prevent drift; plans pipeline-version migrations and regional failover.

See also: [HLD 4.11 Stream Processing](../computer-science/High_Level_Design.md#411-stream-processing), [HLD 4.12 CDC and the Outbox](../computer-science/High_Level_Design.md#412-change-data-capture-event-sourcing-cqrs-and-the-outbox), [HLD 4.10 Probabilistic Counting](../computer-science/High_Level_Design.md#410-probabilistic-counting-hyperloglog-and-count-min-sketch), [Mock hint A6](HLD_Mock_Interviews.md#a6-ad-click-aggregation-exactly-once)

---

### A7. Distributed Cache Service

#### Requirements and assumptions

- **Operations:** `get`, `get_multi`, `set` with TTL, `add`, `cas`, `delete`, `touch`, and lease-based `lease_get`/`lease_set` for stampede and stale-set protection. Opaque byte values; keys up to 250 B; values up to 1 MB.
- **Tenants:** about 300 internal services (20k client processes). Each tenant gets one or more **pools** with a memory quota, an ops/s quota, and a replication setting.
- **Scale:** 10M ops/s at peak, 90% reads. Working set about 20 TB across all pools.
- **Latency:** in-zone `get` p50 under 300 µs, p99 under 1 ms.
- **Availability:** 99.99% for reads. A single node loss must not push any backing database above about 1.2x its normal load.
- **Consistency:** the cache is never the source of truth. After a database write, the cached value is invalidated within seconds (p99 under 5 s), and a stale value must never survive indefinitely.
- **Regions:** three regions, each with its own cache cluster and a local database replica; one primary database region for writes.
- **Out of scope:** persistence (pools that need it should use a real key-value store), rich data structures beyond what memcached offers.

#### Capacity estimate

```text
Ops:          10M ops/s peak: 9M gets, 1M sets/deletes
Item:         median 300 B value + 50 B key + 48 B header ≈ 400 B; mean ~1 KB (tail up to 1 MB)
Node:         256 GB RAM, ~200 GB for items after OS, connection buffers, and slab overhead; 32 cores; 25 GbE
By memory:    20 TB ÷ 200 GB = 100 nodes; ~25% of data in replicated pools (RF 2) -> +25 nodes = 125 nodes
By ops:       10M ÷ 125 = 80k ops/s per node; a multithreaded memcached-class node does several hundred
              thousand to 1M+ gets/s -> 4-10x headroom, which absorbs hot keys and failover
Network:      10M × ~1 KB = 10 GB/s cluster-wide ÷ 125 ≈ 80 MB/s ≈ 0.64 Gb/s per node; a 10x hot node is still < 25 GbE
Items/node:   200 GB ÷ 1 KB ≈ 200M items; headers 200M × 48 B ≈ 9.6 GB (~5%); hash table 200M × 8 B ≈ 1.6 GB
Connections:  20k clients × 125 nodes = 2.5M connections; ~20k per node (fine for epoll, but costly for short-lived clients)

Backing database load (95% hit rate):
  normal misses:   9M × 5% = 450k reads/s spread across all tenants' databases
  lose 1 node:     +9M × 0.95 ÷ 125 ≈ 68k/s (+15%)               -> tolerable
  lose 1 zone:     +9M × 0.95 ÷ 3   ≈ 2.85M/s (+630%)            -> catastrophic without cross-zone replicas
```

**What the numbers decide:** memory, not throughput, sets the node count, which leaves ample per-node ops headroom. A single node loss is harmless, but a **zone loss would multiply database load by about 7x**, so pools whose databases cannot absorb that must keep a replica in another zone. Connection fan-out (2.5M) argues for a proxy option for short-lived and small clients.

#### Interfaces and data

```text
Data plane (memcached binary protocol compatible, mTLS; tenant derived from the client certificate):
  get(key) -> (value, flags, cas) | MISS
  get_multi(keys[]) -> {key: value}
  set(key, value, ttl_s) | add(key, value, ttl_s) | cas(key, value, cas_token) | delete(key) | touch(key, ttl_s)
  lease_get(key) -> HIT(value) | MISS(lease_token) | WAIT(retry_after_ms) | STALE(value)   (hot-miss protection)
  lease_set(key, value, lease_token, ttl_s) -> STORED | LEASE_INVALID
  every request carries the client's cluster-map epoch; a node that does not own the key replies WRONG_EPOCH

Control plane:
  POST /v1/pools { tenant, memory_gb, ops_quota, replication: 1|2, max_item_kb, near_cache: bool, regions[] }
  cluster map (in etcd): pool -> slots[0..16383] -> { primary node, replica node }, epoch (monotonic)

Physical key:  "<tenant>:<pool>:<user key>"   (prefix enforces isolation and per-tenant accounting)
Item layout:   [LRU prev/next 16 B][hash-chain next 8 B][cas 8 B][exptime 4 B][flags 4 B]
               [key_len 1 B][val_len 4 B][slab class 1 B][pad] [key][value]       ≈ 48 B header
```

Partition each pool into 16,384 hash slots (`slot = hash(key) mod 16384`), and assign slots to nodes in the cluster map. A fixed slot count is easier to move and reason about than raw ring tokens: rebalancing moves whole slots, and the map stays small (16k entries per pool). Large tenants get pools placed on dedicated nodes; small tenants share nodes with per-pool memory limits inside each node.

#### Architecture and flow

```text
Tenant process
 +-- client library (Go/Java/C++): cluster map + epoch, slot routing, optional near-cache (L1, 1 s TTL for
 |   hot keys), singleflight, lease handling, retries with backoff, per-tenant metrics
 |        | direct TCP to the owning node (long-lived services)
 |        v
 |   [cache node] [cache node] ... [cache node]    (125 nodes over 3 zones; replica slot owners in another zone)
 |        ^
 +-- or local sidecar / proxy tier (short-lived jobs, scripts, other languages): routing, pooling, replication fan-out

Control plane: etcd (cluster map, epochs) <- health checker (heartbeats) <- rebalancer, quota manager, autoscaler
Gutter pool:   a few small nodes used only while a primary is down (short TTL)

Invalidation:  Primary DB --(binlog/WAL)--> DB replica in each region --(CDC)--> invalidation daemon
               --> delete(key) to slot owners and replicas in that region
```

**Read path:**

1. The client hashes the key to a slot, looks up the owner in its cached map (epoch E), and sends `get` (or `lease_get` for cache-aside loads).
2. Hit: return. Miss with a lease token: read the database (preferably the region's local replica), then `lease_set`. Miss with `WAIT`: another client holds the lease, so retry after a few milliseconds and usually hit.
3. `WRONG_EPOCH`: refresh the map from etcd (or from the node's piggybacked map) and retry once.

**Write path (application data changes):**

1. The service commits the write to the database.
2. It sends `delete(key)` to the cache (fast path, best effort).
3. The CDC invalidation daemon in every region sees the row change in that region's replica stream and deletes the derived keys again (reliable path, at least once, idempotent because it is a delete).

#### Deep dive: routing, rebalancing, and client vs proxy

The hashing itself is covered in [HLD 6.8](../computer-science/High_Level_Design.md#deep-dive-partitioning-with-consistent-hashing) and [CS 5.8](../computer-science/CS_Fundamentals.md#58-consistent-hashing): any scheme where adding a node moves about 1/N of keys works, and modulo hashing does not. The interesting decision is where routing runs:

| Option | How | Pros | Cons |
|---|---|---|---|
| Smart client library | Client holds the map and talks straight to nodes | One network hop; no extra tier to operate | Library per language; 20k clients must all learn map changes; 2.5M connections |
| Proxy tier (mcrouter or twemproxy style) | Clients talk to a local or nearby proxy that routes | Thin clients; connection pooling; replication and failover logic in one place | Extra hop (~50-100 µs if remote, a few µs as a sidecar); proxies to scale |
| Server-side redirect (Redis Cluster style) | Any node answers `MOVED slot node` | No external map distribution | Extra round trip on every stale map; clients still need slot logic |

Offer both the library (for the large, latency-sensitive services) and a sidecar proxy (for everything else). Make map changes safe with **epochs**: the control plane bumps the epoch on every change, nodes know which slots they own at which epoch, and a node rejects a request for a slot it no longer owns. A client with a stale map therefore gets an error and refreshes, rather than silently reading from or writing to the wrong node.

**Rebalancing** (adding nodes, moving a tenant): moving a slot to an empty node would turn its keys into misses all at once. Instead, migrate warm: during the move the new owner serves gets by checking itself and, on a miss, fetching from the old owner and storing locally ("read-through from old owner"), while deletes go to both. After a few minutes, or once the old owner's copy is drained, the epoch flips and the old owner drops the slot. Move a few slots at a time so no database sees more than a small burst of misses.

#### Deep dive: replication and failover

Most pools run with **one copy**: a cache miss is a performance event, not data loss, and the computation above shows one node loss adds about 15% database load. Pools whose databases cannot absorb a zone loss use **RF 2 with the replica in a different zone**:

- **Writes and deletes** go to both owners (the library or proxy fans out; deletes must reach both or a replica serves stale data after failover). Reads go to the zone-local copy.
- **Failure detection:** nodes heartbeat to the health checker every 500 ms; three misses mark a node down and bump the epoch. Clients see `WRONG_EPOCH` or connection errors and re-route.
- **Unreplicated pools use a gutter pool** (from Facebook's memcache design): while a node is down, its keys are read and filled through a small dedicated gutter pool with a 10 s TTL, instead of being rehashed onto healthy nodes. Rehashing would double the load on neighbors and leave them holding entries that later become stale; the gutter's short TTL bounds staleness and memory.
- **Cold rejoin rule:** a node that was unreachable has missed deletes, so its contents are untrustworthy. It must flush everything before taking traffic again. The epoch enforces this: a returning node starts with no slots and receives them through the normal assignment path.
- **Restarts and deploys:** rolling restarts empty one node at a time. For a large cluster that is fine; for a small replicated pool, restart the replica, wait for it to warm (or copy the warm primary's hot set), then the primary.

#### Deep dive: memory efficiency and eviction

A general-purpose `malloc` with millions of variable-size items fragments badly over days. Memcached-style **slab allocation** avoids that: memory is carved into 1 MB pages, each page belongs to a **slab class** with a fixed chunk size, and classes grow by a factor of 1.25 (96 B, 120 B, 152 B, ... up to 1 MB). An item goes into the smallest chunk that fits:

```text
Waste per item:    chunk size - item size; with a 1.25 growth factor the worst case is ~20% of the chunk
                   and the average is roughly 10% for item sizes spread evenly within a class
Header overhead:   48 B on a 400 B median item = 12%; on 1 KB = 5%
Usable fraction:   ~200 GB of a 256 GB node holds items; ~85% of that is key + value bytes
```

Two problems follow. **Slab calcification:** pages assigned to a class stay there, so when a tenant's value sizes shift (a new 2 KB field), the 2 KB class starves and evicts aggressively while other classes hold idle memory. A background **slab rebalancer** moves pages from classes with low eviction pressure to classes with high pressure. **Lock and scan behavior:** a single LRU per class, bumped on every hit, is a contention point and lets one scan of cold keys flush the hot set. Use a **segmented LRU** (hot, warm, cold queues per class): new items enter hot, items move to warm only if hit again, eviction takes from the tail of cold, and an item is bumped at most once per 60 s. Expired items are reclaimed lazily on access and by a background crawler, so TTL-heavy pools do not hold dead items until eviction reaches them.

Per-tenant isolation in memory: each pool's items are accounted and evicted within its quota, so one tenant's burst cannot evict another's hot set. Eviction rate per pool is the key signal for a tenant to request more memory.

#### Deep dive: consistency with the database

Cache-aside has three classic races, and each needs a specific mechanism:

```text
Race 1, stale set (reader and writer interleave):
  t1  Reader R: get(k) -> MISS
  t2  R reads DB -> v1
  t3  Writer W: UPDATE DB -> v2 ; delete(k)
  t4  R: set(k, v1)          <- cache now holds v1 indefinitely (until TTL)

Race 2, set-on-write (two writers):
  W1 writes DB v1, W2 writes DB v2, W2 sets cache v2, W1 sets cache v1   <- stale indefinitely
  Fix: writers DELETE, they never SET. Only readers fill, and readers fill through leases.

Race 3, lost delete:
  W commits to DB, then crashes (or the delete RPC times out) before delete(k)
  Fix: CDC invalidation daemon deletes from the replication stream, at least once
```

**Leases** close race 1. `lease_get(k)` on a miss returns a 64-bit lease token bound to the key. A `delete(k)` invalidates any outstanding lease for `k`. When R finally calls `lease_set(k, v1, token)` at t4, the token is no longer valid and the set is rejected. The same mechanism controls stampedes: the server issues at most one lease per key every 10 s (configurable), and other missers receive `WAIT` or, if the pool allows, the just-deleted value marked `STALE`. One database read per hot key per interval, fleet-wide. The broader stampede and hot-key toolkit (XFetch, near caches, key replication) is in [HLD 4.13](../computer-science/High_Level_Design.md#413-cache-stampede-and-hot-keys); the library implements singleflight and a near-cache that is enabled per key when the server's top-K sampler flags it as hot.

**Replica lag** creates a variant of race 1: R reads a lagging database replica after W's delete and fills an old value. Running the invalidation daemon off **each region's own replica stream** fixes this ordering: the delete happens after that replica has applied the write, so any read that follows the delete sees the new value. The app-side delete is still worth sending, because it shortens the window in the primary region.

Mapping row changes to cache keys: each tenant registers key templates per table (`user:{id}:profile` from `users.id`), or embeds the keys to invalidate in the transaction (written to an invalidation column or outbox table that the CDC stream carries; see [HLD 4.12](../computer-science/High_Level_Design.md#412-change-data-capture-event-sourcing-cqrs-and-the-outbox)). A TTL on every item (hours, with jitter) is the final backstop if any mapping is wrong.

**Multi-region:** each region's cache is filled only from its local replica and invalidated only from its local replica stream, so regions never make cross-region cache calls. A user who writes in a non-primary region and immediately reads would see their old data while replication catches up. Handle read-your-writes with a short-lived **remote marker**: on write, set `marker:k` in the local cache; a reader that sees the marker reads from the primary region's database instead of the local replica until the marker expires or the invalidation arrives.

#### Failure modes and mitigations

| Failure | Impact | Mitigation |
|---|---|---|
| One node down | ~1/125 of keys miss; +15% database reads | Gutter pool or zone replica; no rehash onto neighbors |
| Zone down | ~1/3 of keys miss; database load up to ~7x | RF 2 across zones for pools that need it; load shedding at the database; leases cap per-key misses |
| Node returns after a partition | Serves values whose deletes it missed | Cold rejoin: flush and re-acquire slots through a new epoch |
| CDC invalidation daemon lags or stops | Stale values beyond the 5 s target | Alert on replication-slot lag; TTL backstop; daemon restarts from its stored log position (deletes are idempotent) |
| Stale cluster map in some clients | Requests to the wrong node | Epoch check on every request returns `WRONG_EPOCH`; clients refresh |
| Hot key overloads one node | Latency for all keys on that node | Top-K detection, client near-cache with 1 s TTL, key replication `k#0..k#7` |
| Tenant bursts far over quota | Noisy neighbor on shared nodes | Per-pool token-bucket ops limit at node and proxy; per-pool memory accounting |

#### Tradeoffs

| Decision | Chosen | Alternative | Why |
|---|---|---|---|
| Routing | Smart client plus sidecar proxy option | Proxy-only or server redirects | Lowest latency for big services, thin clients for the rest |
| Replication | Per pool: RF 1 default, RF 2 cross-zone where the DB needs it | RF 2 everywhere | Doubles memory cost; most databases can absorb a node's misses |
| Write policy | Delete on write; fill on read via leases | Set on write / write-through | Set-on-write races leave stale data indefinitely |
| Invalidation | App delete plus CDC from each region's replica stream | App delete only | Survives app crashes and orders correctly against replica lag |
| Memory management | Slab classes with rebalancer, segmented LRU | `malloc` per item, single LRU | Bounded fragmentation; scan resistance; less lock contention |
| Node failure handling | Gutter pool | Consistent-hash rehash to neighbors | Avoids cascading overload and long-lived stale copies |

**Main interview tradeoff:** freshness against database protection. Short TTLs and aggressive invalidation keep data fresh but raise the miss rate, and every miss is database load; long TTLs protect the database but rely entirely on invalidation being correct. The design leans on correct invalidation (leases, delete-not-set, CDC from the local replica) so that TTLs can stay long, and on replication only where the miss load from a failure would be dangerous.

#### Follow-ups with model answers

**Q1. Why do writers delete the key instead of writing the new value into the cache?**

Two concurrent writers can apply their database writes in one order and their cache sets in the other, leaving the older value in the cache with nothing to correct it until the TTL. A delete is idempotent and order-insensitive: whichever delete lands last, the next reader fetches the current value from the database. Deletes cost one extra miss per write, which is cheap for read-heavy keys. For write-heavy keys, consider not caching them at all.

**Q2. A tenant asks for a "strongly consistent" cache. What do you tell them?**

A cache in front of a database cannot be linearizable without coordinating every write with the cache, which removes most of its value. What it can offer: bounded staleness (invalidation within seconds), read-your-writes for the writer (markers or reading through to the primary after a write), and no indefinitely stale entries. If they truly need linearizable reads at cache latency, they need a replicated key-value store with consensus as their source of truth, not a cache. See [CS 8.13](../computer-science/CS_Fundamentals.md#813-consistency-guarantees-split-brain-leases-and-fencing).

**Q3. How do you bring up a new region's cache cluster without crushing its database?**

Do not shift traffic to an empty cache. Warm it first: replay a sample of the existing region's read keys against the new cluster (a "shadow read" phase that fills through leases at a capped rate), or bulk-copy the hottest slots' contents while the invalidation daemon is already running so copies cannot go stale. Then shift traffic gradually (1%, 10%, 50%, 100%) while watching the database miss rate. A cold start at full traffic is a stampede of every key at once.

**Q4. Memcached-style engine or Redis-style engine?**

Memcached-style (multithreaded, slab allocator, simple values) gives the highest gets per node and predictable memory, which suits a pure cache service. Redis-style adds data structures (sorted sets, hashes), Lua, and persistence, but each shard executes commands on one thread (about 100k-200k simple ops/s), so more shards are needed for the same throughput. Offer the memcached-style engine as the default and a separate Redis-compatible pool type for tenants who need structures, with the same routing, tenancy, and invalidation tooling.

**Q5. What metrics would you put on the tenant dashboard?**

Hit rate (and misses per second, which is the database's view), evictions per second and the age of evicted items (a young eviction age means the pool is too small), memory used vs quota, ops/s vs quota with throttled requests, p99 latency by operation, lease `WAIT` and `STALE` counts (stampede pressure), invalidation lag from the CDC daemon, and top keys by ops and by bytes. Eviction age and invalidation lag are the two that tenants most often lack.

#### Level signals

- **Mid:** consistent hashing, LRU eviction, TTLs, cache-aside; knows the cache can lose data.
- **Senior:** sizes by memory and by ops separately; computes database load for node and zone loss; client vs proxy routing with epochs; delete-not-set and leases for the stale-set race; slab classes and fragmentation; gutter pool or cold rejoin.
- **Staff:** treats it as a platform: tenancy, quotas, chargeback, and per-tenant observability; invalidation from each region's replica stream to handle replica lag; warm migrations and region bring-up; decides which pools deserve replication from their databases' headroom.

See also: [HLD 4.13 Cache Stampede and Hot Keys](../computer-science/High_Level_Design.md#413-cache-stampede-and-hot-keys), [HLD 6.8 Distributed Key-Value Store](../computer-science/High_Level_Design.md#68-distributed-key-value-store), [CS 5.3 Caching](../computer-science/CS_Fundamentals.md#53-caching), [Mock hint A7](HLD_Mock_Interviews.md#a7-distributed-cache-service)

---

### A8. Nearby Places (Yelp)

#### Requirements and assumptions

- **Search:** given `(lat, lng)`, a radius (default 2 km, maximum 25 km), optional filters (category, price, open now), and an optional text query, return the best 20 places with a cursor for more. Each result card shows name, rating, review count, distance, price, open status, and a thumbnail.
- **Place pages:** details, hours, top reviews, photos.
- **Writes:** owners edit place details; users add reviews (one per user per place) and photos. About 100k place edits or additions per day, 2M reviews per day, 1M photos per day.
- **Scale:** 200M places worldwide; 100k searches/s at peak; 30k place-page views/s.
- **Latency:** search p99 under 200 ms server-side, with the geo retrieval stage under 30 ms.
- **Freshness:** place edits and rating changes visible in search within minutes; a review is visible on the place page immediately to its author and within seconds to others.
- **Out of scope:** moving places, sponsored-result auctions (blended in by a separate service), personalization beyond a simple user-preference boost.

#### Capacity estimate

```text
Place records (source of truth): 200M × ~1 KB (address, hours, attributes) ≈ 200 GB -> sharded relational DB

Search index entry (in memory, per place):
  S2 cell id 8 B + place_id 8 B + lat/lng as 2 × float32 8 B (~1 m precision)
  + rating, review count, price, flags 8 B + category bitmap 8 B + tz id 2 B
  + weekly hours bitmap in local time, 7 × 96 quarter-hours = 672 bits = 84 B      ≈ 128 B
  200M × 128 B ≈ 25.6 GB; with sort arrays and overlay ≈ 32 GB  -> fits in one 128 GB server
  => replicate the WHOLE index on every search node; no geo sharding of the geo index

Candidates per query (dense downtown, worst common case):
  ~1,400 places/km² × 12.6 km² (2 km circle) ≈ 18k places; S2 covering over-fetch ~1.5x ≈ 27k entries scanned
  scan + exact-distance filter at ~20 ns/entry ≈ 0.5 ms; rank top 200 with a small model ≈ 1 ms
  average query (suburbs, filters) is far cheaper; budget ~2 ms CPU per query including RPC overhead
Search CPU:   100k/s × 2 ms = 200 cores; each region sized for 50% of global traffic (to absorb a region loss)
              = 100 cores ÷ (32 cores × 50% target utilization) ≈ 7 -> ~8 index nodes per region
Text index:   ~30% of searches carry text ≈ 30k/s; 200M docs × ~1 KB (postings, doc values, geo points) ≈ 200 GB
              -> ~40 shards of ~5 GB, sharded by geographic region, 2 replicas
Reviews:      1B stored × ~1 KB ≈ 1 TB; 2M/day ≈ 23 writes/s (trivial); first page per place cached
Photos:       500M × (2 MB original + ~300 KB derivatives) ≈ 1.15 PB object storage; 1M/day × 2 MB ≈ 2 TB/day in
Thumbnails:   100k searches/s × 20 cards ≈ 2M image requests/s ≈ 40 GB/s at 20 KB each -> CDN, not origin
```

**What the numbers decide:** the geo index is about 32 GB, so the right shape is a **fully replicated in-memory index** scaled by adding replicas for QPS, not a sharded geo database. Search cost is dominated by candidate count in dense areas, which drives the choice of a tight cell covering and caps for large radii. Text search is a different, larger index and is sharded by region. Writes are tiny, so updates can flow asynchronously.

#### Interfaces and data

```text
GET  /v1/search?lat=40.741&lng=-73.989&radius_m=2000&q=ramen&category=restaurants&open_now=1&price=1,2&limit=20
     -> { results: [{ place_id, name, rating, review_count, distance_m, price, open_now, thumb_url }], cursor }
GET  /v1/search?cursor=...                     -> next page from the cached result list
GET  /v1/places/{place_id}                     -> details, hours, stats, first page of reviews, photo urls
POST /v1/places/{place_id}/reviews  { rating: 1..5, text, idempotency_key }       -> 201 { review_id }
POST /v1/places/{place_id}/photos   { content_type, size }  -> { upload_url (pre-signed), photo_id }
PATCH /v1/places/{place_id}  If-Match: <version>  { hours, phone, attributes ... }  (owner)

place        (sharded by place_id): place_id PK, name, lat, lng, s2_cell BIGINT, address, category_ids,
             price, hours_local JSON, tz, status, version, updated_at
place_stats  (sharded by place_id): place_id PK, rating_sum, rating_count, bayes_rating, updated_at
review       (sharded by place_id): PRIMARY KEY (place_id, review_id), user_id, rating, text, status, created_at
             UNIQUE (place_id, user_id); index (place_id, created_at DESC)
review_by_user (sharded by user_id): (user_id, created_at, place_id, review_id)  -- "my reviews" page
photo        (sharded by place_id): PRIMARY KEY (place_id, photo_id), object_key, uploader_id, status, created_at
special_hours: PRIMARY KEY (place_id, date), open_intervals   -- holidays override the weekly bitmap
```

Shard every place-owned table by `place_id`, so the place page (details, stats, reviews, photos) is a set of single-shard reads. The search index is not a table: it is a derived, read-only structure rebuilt from these tables and patched by their change stream.

#### Architecture and flow

```text
Clients --> CDN (photos, thumbnails, static assets)
        --> API gateway --> Search service (stateless: parse, fan out, rank, paginate)
                               |  no text query                    |  text query
                               v                                   v
                       Geo index nodes                     Text search cluster
                       (full in-memory replica:            (inverted index + geo filter,
                        S2-sorted arrays + overlay)         sharded by region, 2 replicas)
                               |  candidates (<= ~30k) -> prefilter -> top 200
                               v
                          Ranker (in process): distance, Bayesian rating, review count, open now
                               |
                          Result cache (cursor -> top 100 ids, 5 min) ; Place card cache <- place DB

Writes:  Place service --> place DB --CDC--> place-changes topic --+--> Geo index nodes (apply deltas every ~5 s)
         Review service --> review DB + outbox --> stats aggregator |--> Text index updater
                                     --> place_stats --CDC---------+--> Snapshot builder (every 6 h)
         Photo upload --> object storage (pre-signed URL) --> processing (derivatives, moderation) --> photo table
```

**Search path:**

1. The search service converts the circle into an S2 covering (at most 8-16 cells, levels chosen to fit the radius) and sends it, with filters, to one geo index node (any replica).
2. The node binary-searches each cell range in its cell-sorted array, checks filters on the packed entries (category bitmap, price, open-now bit), computes exact haversine distance, drops points outside the circle, and keeps the top 200 by a cheap prefilter score. It applies the overlay (recent edits and deletions) as it scans.
3. The ranker scores the 200 candidates fully and returns the top 100; the service caches that list under a cursor and returns the first 20. Place cards come from the details cache.
4. With a text query, the service sends the query plus the circle to the text shard(s) covering it, which return text-relevant place IDs inside the circle with relevance scores; the ranker blends relevance with the same features.

**Write path:** a place edit commits to the place DB with a version check; CDC publishes the change; every index node applies it to its overlay within seconds. A review inserts into the review shard plus an outbox row in one transaction; the stats aggregator updates `place_stats` (idempotent by `review_id`), and that change flows to the index the same way.

#### Deep dive: geospatial index choice and the in-memory layout

The comparison of geohash, quadtree, S2, and H3 is in [HLD 4.8](../computer-science/High_Level_Design.md#48-geospatial-indexing). For this workload (static points, read-heavy, radius queries from 200 m to 25 km), the decision is:

- **S2 cell IDs in a sorted array.** Each place is stored once, keyed by its level-30 (leaf) cell ID, which preserves Hilbert-curve locality. Any coarser cell is a contiguous ID range of leaves, so a covering cell becomes one binary search plus a sequential scan. The array is flat, cache-friendly, trivially serialized, and can be memory-mapped from a snapshot file.
- **Tight coverings.** A 2 km circle (12.6 km²) covered by up to 8 cells at levels 12-14 (average areas 5.07, 1.27, and 0.32 km²) over-fetches roughly 1.5-2x. A geohash-5 cell plus its 8 neighbors covers about 216 km², a 17x over-fetch: in a downtown that is hundreds of thousands of candidates per query instead of tens of thousands. Coarse geohash is fine for a sparse country, not for Manhattan.
- **Quadtree** would also work in memory and adapts to density, but it is a pointer structure: harder to snapshot, ship, and update atomically. **PostGIS** remains a good tool for the write side and for polygon questions (delivery zones), not for 100k ranked radius queries per second.
- S2 is computed on the sphere, so the antimeridian and the poles need no special cases, which geohash does need.

**Read-heavy scaling.** Index nodes are interchangeable, so QPS scales linearly by adding replicas (about 8 per region at peak, computed above). Two caches cut the work further. A **result cache** keyed by `(S2 level-16 cell of the query point, radius bucket, filters, query text)` with a 60 s TTL absorbs repeated searches from the same street corner (a level-16 cell is about 150 m across, so nearby users share entries, and the distance error that introduces is negligible next to a 2 km radius). A **place-card cache** holds the rendered result cards for the most viewed places, so the search service does not touch the place database at all on the hot path. Neither cache needs invalidation beyond its TTL, because minutes of staleness is within the freshness requirement.

**Large radii.** A 25 km circle around a city can contain 500k places, too many to scan per query. Precompute, per S2 level-10 cell (about 81 km²) and per top-level category, the top 200 places by a distance-free quality score. A large-radius query covers the circle with level-10 cells (a few dozen), merges their top lists, then applies distance-aware ranking. The result is "the best places in the area", which is what users want at that zoom level.

**Updates without rebuilding.** Each node holds an immutable base snapshot plus an **overlay**: a hash map of `place_id -> new entry or tombstone`, and a small cell-sorted array of overlay entries. Scans merge base and overlay and skip base entries that the overlay supersedes. A place that moves becomes a tombstone at its old position and an overlay entry at the new one. Every 6 hours a builder produces a new snapshot (from the database plus the change stream up to a recorded offset), uploads it to object storage, and nodes swap atomically after loading it alongside the old one (temporarily 2 × 32 GB), then replay the change topic from the snapshot's offset. A restarting node loads 32 GB from local NVMe at ~3 GB/s in about 11 s.

#### Deep dive: ranking

Rank in two stages: cheap retrieval over all candidates, then a fuller model over the top 200.

- **Rating, corrected for small samples.** Use a Bayesian average: `bayes = (C × m + sum of ratings) / (C + n)`, with global mean `m = 3.7` and prior weight `C = 20`. A place with one 5-star review scores (74 + 5) / 21 = 3.76; a place with 500 reviews averaging 4.6 scores (74 + 2,300) / 520 = 4.57. Raw averages would rank the single 5-star review first.
- **Popularity:** `log(1 + review_count)`, so the 10,000th review matters less than the 10th.
- **Distance:** a decay such as `exp(-d / d0)` with `d0` about half the radius, so a slightly better place 1.8 km away can beat a mediocre one next door, but not by much.
- **Open now:** either a filter (when the user asked) or a boost. Store hours in **local time** with the place's time zone, and evaluate `bitmap[local_quarter_hour(now, tz)]` per candidate. This avoids rebuilding UTC bitmaps at every daylight-saving change and handles places near time-zone borders correctly. Holiday hours come from the `special_hours` overlay.
- **Learned model:** with logged clicks and conversions, replace the hand weights with a gradient-boosted model over the same features plus text relevance and user preference. Keep the hand formula as the fallback.

**Pagination stability:** the cursor references a cached list of the top 100 IDs for 5 minutes, so page 2 is consistent with page 1 even if ratings change in between. Beyond 100, re-query with an exclusion list.

#### Deep dive: reviews, photos, and text plus geo

**Reviews.** Insert the review and an outbox event in one transaction on the place's shard; `UNIQUE (place_id, user_id)` enforces one review per user per place, and the idempotency key makes a retried POST return the same review. The stats aggregator consumes outbox events and applies `rating_sum += r, rating_count += 1` together with an inbox row keyed by `review_id` in the same transaction, so redelivery cannot double count ([HLD 4.12](../computer-science/High_Level_Design.md#412-change-data-capture-event-sourcing-cqrs-and-the-outbox)). The author sees their review immediately because the place page reads the review shard directly for the author's own review. A review flagged as fake later is removed through the same path with a negative delta.

**Photos.** Clients upload directly to object storage with a pre-signed URL; an upload-complete event triggers derivative generation (thumbnail, card, full-screen), EXIF location stripping, and moderation; only then does the photo row become `ACTIVE`. Serve through the CDN with content-addressed URLs (immutable, long cache lifetime). See [HLD 6.14](../computer-science/High_Level_Design.md#614-object-storage-s3-like) for the storage layer.

**Text plus geo.** Three options:

| Option | How | Fits |
|---|---|---|
| Geo first, then text filter | Retrieve geo candidates, filter by a small per-place token set (name words, category, top dish terms) | Category browsing and short name queries; no extra system |
| Text engine with a geo filter | Inverted index plus a geo-point field (BKD tree); query = text match AND distance filter | Free-text queries; relevance scoring built in |
| Intersect two systems | Text returns IDs, geo returns IDs, intersect | Rarely worth it: two large result sets to join per query |

Use the first for queries without text and the second for text queries. Shard the text index by **region** (groups of S2 level-5 cells, about 83k km² each, balanced by place count) rather than by place ID: a local query then hits one shard, or two to four near a boundary, instead of all 40.

#### Failure modes and mitigations

| Failure | Impact | Mitigation |
|---|---|---|
| Geo index node crash | Queries to it fail | Stateless retry to another replica; restart loads the local snapshot in ~11 s |
| CDC or change topic lag | Edits and ratings stale in search | Alert on lag; search still serves (staleness is minutes, not errors); place pages read the DB directly |
| Bad snapshot (builder bug) | Missing or wrong places | Validate counts and sample queries before publishing; nodes keep the previous snapshot and refuse to swap on validation failure |
| Text cluster degraded | Text queries slow or failing | Fall back to geo search with the name and category token filter; mark results as approximate |
| Dense-area query explosion | CPU spikes, tail latency | Cap scanned candidates; switch to finer cells or precomputed top lists; rank only the top 200 |
| Review spam burst on one place | Rating manipulated | Rate limits per user and device, fraud scoring before stats update, delayed inclusion for new accounts |
| Region outage | Lost capacity | Every region sized for 50% of global traffic; full index replicas in every region |

#### Tradeoffs

| Decision | Chosen | Alternative | Why |
|---|---|---|---|
| Index distribution | Full replica on every node | Shard the geo index by region | 32 GB fits in RAM; replicas scale QPS with no fan-out or boundary queries |
| Spatial scheme | S2 cell IDs in a sorted array | Geohash prefixes; quadtree; PostGIS | Tight coverings and flat, snapshot-friendly layout |
| Update model | Immutable snapshot plus overlay | In-place mutable tree | Lock-free reads, atomic swap, easy rollback |
| Rating signal | Bayesian average | Raw mean | Prevents tiny samples from dominating |
| Text search | Separate engine sharded by region | Text in the geo nodes | Different size and scoring needs; local queries hit one shard |
| Freshness | Seconds to minutes via CDC | Synchronous index update on write | Writes are rare and nobody needs a new review in search within milliseconds |

**Main interview tradeoff:** compute the index size before choosing a sharding strategy. At about 128 bytes per place, the whole world fits on one server, so the design replicates a read-only structure and scales by adding replicas, which removes cross-shard fan-out, boundary handling, and rebalancing. The price is that updates are asynchronous and every node needs about 64 GB of headroom during a snapshot swap. If places were moving objects or the per-place record were 10x larger, sharding by region would win instead.

#### Follow-ups with model answers

**Q1. The user zooms the map out and the app wants pins for every place in view. 50,000 pins?**

Never send 50,000 pins. Precompute counts (and a representative top place) per S2 cell at several levels, and return clusters: "312 places" per cell at the current zoom, with the cell centroid as the pin. As the user zooms in, cells split until individual places appear. The counts are a cheap aggregation over the same snapshot.

**Q2. How would the design change for food trucks that move during the day?**

Static-place assumptions break: positions change every few minutes, so an immutable snapshot is wrong. Keep moving entities in a separate in-memory structure (`entity -> cell, position, ts` and `cell -> set of entities`), updated on every location report and expired when reports stop, exactly as in [ride-sharing](../computer-science/High_Level_Design.md#66-ride-sharing-service). Query both structures and merge. The number of moving places is small, so this side index stays tiny.

**Q3. Why not just use PostGIS with a GiST index?**

It answers the radius query correctly and is the right first version at small scale. At 100k ranked queries per second, each query reads tens of thousands of rows, computes features, and sorts: that is many database replicas doing work that a purpose-built in-memory scan does in about a millisecond. Keep PostGIS (or the relational store) as the source of truth and for polygon queries, and derive the serving index from it.

**Q4. How do you stop a business from buying fake 5-star reviews?**

Ranking defenses reduce the payoff: the Bayesian prior blunts small bursts, and review weight can depend on the reviewer's history (account age, review count, verified visits). Detection catches the rest: bursts of reviews from new accounts, shared devices or IP ranges, and text similarity. Suspicious reviews are hidden from the rating (still visible to their author, so spammers learn less), and confirmed fraud is removed with a negative stats delta. All of it flows through the same review pipeline, so ranking updates within minutes.

**Q5. What breaks at the antimeridian or near the poles?**

Geohash and plain lat/lng bounding boxes treat longitude as a line, so a circle crossing 180° splits into two boxes and neighbor computation needs special cases; near the poles, cells become extremely narrow. S2 works on the sphere: coverings cross the antimeridian naturally and cells have bounded distortion everywhere. Distance must be haversine (or great-circle), never Euclidean on degrees.

#### Level signals

- **Mid:** a spatial index (geohash with neighbors or a quadtree), exact-distance filtering, a cache for place details, reviews in a database.
- **Senior:** computes index size and replicates it instead of sharding; covering and over-fetch math; Bayesian rating; open-now with local time and time zones; CDC-driven updates with an overlay; outbox for rating aggregation; text engine sharded by region.
- **Staff:** large-radius strategy with precomputed per-cell top lists; snapshot validation and rollback; capacity per region for regional failover; ranking evaluation (offline metrics, click logs, A/B testing) and abuse economics; knows when the design would flip to sharding.

See also: [HLD 4.8 Geospatial Indexing](../computer-science/High_Level_Design.md#48-geospatial-indexing), [HLD 6.6 Ride-Sharing Service](../computer-science/High_Level_Design.md#66-ride-sharing-service), [HLD 4.12 CDC and the Outbox](../computer-science/High_Level_Design.md#412-change-data-capture-event-sourcing-cqrs-and-the-outbox), [Mock hint A9](HLD_Mock_Interviews.md#a9-nearby-places)

---

### A9. Stock Exchange Matching Engine

#### Requirements and assumptions

- **Orders:** limit, market, IOC (immediate or cancel), cancel, cancel/replace. Continuous matching with **price-time priority**: best price first, then earliest arrival at that price.
- **Replace semantics:** reducing quantity keeps time priority; changing price or increasing quantity loses it (treated as cancel plus new).
- **Members:** about 500 member firms, a few thousand binary sessions, colocated in the exchange's data center.
- **Scale:** 10k symbols; 1M inbound messages/s at peak, about 70% cancels and replaces (market makers re-quote constantly); the busiest symbol bursts to 100k messages/s.
- **Latency:** order in at the gateway NIC to acknowledgment out, p50 about 20 µs, p99 under 100 µs. Jitter matters as much as the median.
- **Correctness:** no acknowledged order or execution lost (RPO 0); no execution ever duplicated or reordered; deterministic and auditable (any state at any sequence number can be reproduced).
- **Availability:** failover of any component within about a second without losing state; if correctness is in doubt, halt the affected symbols rather than guess.
- **Outputs:** private execution reports to members; public market data (every order event and trades) to thousands of subscribers; drop copies and a clearing feed.
- **Out of scope:** clearing, end-of-day settlement, member onboarding, market surveillance (consumes the journal), auctions (see Q3).

#### Capacity estimate

```text
Inbound:        1M msgs/s peak × ~64 B (fixed-layout binary, no text parsing) = 64 MB/s
Journal:        6.5 h session × ~300k msgs/s average × 64 B = 23,400 s × 300k × 64 B ≈ 450 GB/day
                -> async sequential NVMe writes (several GB/s per drive) are not a bottleneck
Per-symbol:     hottest symbol 100k msgs/s -> 10 µs per message on one thread;
                a match or cancel takes ~0.5-2 µs -> 5-20x headroom on a single pinned core
Engines:        10k symbols over 16 partitions (one pinned core each, plus hot standbys)
                -> ~62k msgs/s per partition on average at peak; the hottest symbols get their own partitions
Book memory:    10k symbols × ~5k resting orders × 64 B ≈ 3.2 GB, plus pre-allocated pools -> all in RAM

Market data:    ~1.5 updates per inbound message ≈ 1.5M updates/s × ~40 B ≈ 60 MB/s per feed
                2,000 subscribers × 60 MB/s over unicast TCP = 120 GB/s from the publishers: impossible
                UDP multicast: publisher sends once, switches replicate -> 60 MB/s per feed

Replay speed:   a recovering engine replays ~5M msgs/s; hourly snapshots bound replay to
                ~300k/s × 3,600 s ≈ 1.1B msgs ≈ 220 s worst case; a hot standby needs no replay at all
```

```text
Latency budget, one way through the exchange (kernel-bypass NICs, cut-through switches, pinned cores):
  NIC rx + gateway decode, session and throttle checks      1-2 µs
  pre-trade risk (in-memory, per account)                   1-2 µs
  gateway -> sequencer (one switch hop + stack)             2-5 µs
  sequence + replicate to standby sequencer (rack RTT)      3-8 µs
  sequencer -> matching engine                               2-5 µs
  match and generate outputs                                 0.5-2 µs
  engine -> gateway -> NIC tx (execution report)            3-6 µs
  -----------------------------------------------------------------
  total                                                     ~13-30 µs typical; p99 < 100 µs
```

**What the numbers decide:** bandwidth is small everywhere except market data fan-out, which forces multicast. The binding constraint is **per-message latency and jitter**, so every hop is in memory over kernel-bypass networking, nothing on the critical path waits for a disk, and one core per partition is enough throughput. Durability therefore comes from **replicating the sequenced log to a second machine before acting on it**, not from fsync.

#### Interfaces and data

```text
Member protocol (binary, OUCH/FIX-like, fixed-width little-endian fields, one TCP session per connection):
  NewOrder     { cl_ord_id (unique per session), symbol_id, side BUY|SELL, qty, price_ticks int64,
                 type LIMIT|MARKET, tif DAY|IOC, account }
  Cancel       { cl_ord_id, orig_cl_ord_id }
  Replace      { cl_ord_id, orig_cl_ord_id, new_qty, new_price_ticks }
  -> Ack { order_id, seq } | Reject { reason } | Fill { exec_id, qty, price_ticks, leaves_qty }
     | CancelAck | ReplaceAck { new_order_id }
  Session layer: per-session outbound sequence numbers; on reconnect the member requests replay from N

Sequenced input record (journal, one stream per partition):
  { seq uint64 (gap-free), gw_rx_ts (NIC hardware timestamp), gateway_id, session_id, msg }
Output record:
  { out_seq, in_seq, event: Accepted|Rejected|Executed|Canceled|..., exec_id = (partition, in_seq, k) }

Market data (multicast; per channel = group of symbols):
  { channel_seq, symbol_id, AddOrder|OrderExecuted|OrderCanceled|Trade|StateChange, fields... }
  + snapshot channel (full book images tagged with channel_seq) + TCP retransmission service

All prices are integer ticks and all quantities integers; no floating point anywhere in the core.
```

Partition by **symbol**: each symbol lives in exactly one partition for the trading day, assigned before the open from the previous day's volume, so hot symbols get dedicated partitions. Nothing in continuous trading needs atomicity across symbols, so partitions never coordinate. Per-session duplicate detection (`cl_ord_id`) is part of the sequenced state, so it survives failover.

#### Architecture and flow

```text
Members (colocation; equal-length cross-connects)
   | binary TCP sessions
   v
Gateways (kernel-bypass NIC, busy-polling pinned cores): sessions, decode, throttles, pre-trade risk per account
   | dedicated low-latency fabric
   v
Sequencer primary (per partition) ----replicate----> Sequencer standby (other rack, other power feed)
   | assign seq; forward once the standby has the record; journal to NVMe asynchronously
   v sequenced stream (internal multicast)
Matching engine primary (single thread, pinned core)      Matching engine hot standby (same input, outputs held)
   | sequenced outputs
   +--> Gateways --> members (acks, fills)                 Arbiter (3 nodes, consensus): who is primary, fencing epoch
   +--> Market data publishers --> multicast feed A and feed B (separate networks), snapshots, retransmit servers
   +--> Drop copy, clearing feed, surveillance, audit store (consume the journals)
```

**Order path:**

1. A member sends `NewOrder`. The gateway decodes the fixed-layout message, checks the session sequence and duplicate `cl_ord_id` (fast in-memory check), applies throttles and pre-trade risk, and forwards it to the sequencer for that symbol's partition.
2. The sequencer stamps the next `seq`, replicates the record to its standby, and on the standby's acknowledgment publishes it to the matching engines (primary and hot standby).
3. The primary engine applies the message to the in-memory book: matches against resting orders at the best opposite prices, rests any remainder, and emits outputs tagged with the input `seq`.
4. Gateways send acknowledgments and fills to members; market data publishers emit the book changes and trades on multicast; the journal writer and downstream feeds consume the same outputs.

**Cancel path** is identical; a cancel that arrives after its order fully executed is rejected deterministically, because both events are ordered by `seq`.

#### Deep dive: sequencing, determinism, and replication by replay

The matching engine is a **deterministic state machine**: `(book state, input message) -> (new state, outputs)`. If two replicas start from the same state and apply the same sequenced input, they produce identical state and identical outputs. That single property gives replication, failover, recovery, and audit:

- **Replication:** the hot standby applies every sequenced message as it arrives and stays microseconds behind the primary, with its outputs suppressed.
- **Recovery:** load the latest snapshot (taken by a standby, so the primary never pauses) and replay the journal from the snapshot's `seq`.
- **Audit:** regulators can reproduce the exact book at any `seq` by replaying the journal.

Determinism is a discipline, and every rule exists because someone broke it:

| Rule | Why |
|---|---|
| No wall-clock reads inside the engine; time comes from the sequenced record | Two replicas reading their own clocks would expire a DAY order or an auction at different points in the stream |
| Order and execution IDs derived from `seq` | Counters or random IDs would differ between replicas |
| Integer ticks and quantities only | Floating-point results can differ with compiler flags and instruction selection |
| No iteration over hash maps whose order depends on addresses or seeds | Order of iteration must be identical everywhere |
| Single thread per partition; no shared state with other threads | Thread interleavings are the main source of nondeterminism |
| Same binary and configuration on primary and standby | Different code means different outputs from the same input |

**Detecting divergence.** Primary and standby each compute a running hash of their outputs and compare it every 10k messages. A mismatch means a determinism bug; halt the affected symbols and investigate rather than trading on a book that may be wrong.

**Durability before acting.** The sequencer forwards a message only after the standby sequencer holds it in memory (a few microseconds on a dedicated link), so a single machine loss cannot lose a sequenced, acted-upon message. Both write the journal to NVMe asynchronously; losing both machines before the flush is the residual risk, mitigated by separate racks and power. A refinement used by low-latency systems: let the engine process immediately but **hold its outputs** until the replication acknowledgment for that `seq` arrives, which overlaps replication with matching.

**Failover and fencing.** An external arbiter (a 3-node consensus group, outside the latency path) decides which sequencer and engine are primary and issues an increasing **epoch**. A standby promotes only after the arbiter grants it the new epoch, and gateways and publishers drop messages stamped with an old epoch, so a primary that was merely stalled (by a page fault or a system management interrupt; pauses happen even without garbage collection) cannot keep publishing alongside the new one ([CS 8.13](../computer-science/CS_Fundamentals.md#813-consistency-guarantees-split-brain-leases-and-fencing)). The new primary engine has already applied every sequenced message, so it resumes publishing outputs from the first `seq` whose outputs were not confirmed delivered; downstream consumers deduplicate by `(in_seq, k)` exec IDs, so the overlap is harmless.

**One sequencer or many?** A single global sequencer (the LMAX-style design) gives one total order across all symbols and handles a few million messages per second on one core; it is simpler for audit. Per-partition sequencers scale further and isolate failures to a symbol group. Either is defensible; at 1M messages/s, one sequencer per partition was chosen here for failure isolation.

#### Deep dive: the order book and matching

The data structures are covered with code in [LLD A7 Order Book Matching Engine](LLD_Practice_Problems.md#a7-order-book-matching-engine); the HLD-relevant points:

```text
Per symbol, per side:
  price levels:  array indexed by (price_ticks - band_low), covering the daily price band (e.g. ±20% of reference)
                 -> O(1) access to any level; best bid/ask kept as indexes, advanced past empty levels
  each level:    intrusive FIFO doubly linked list of orders + total quantity at the level
  order index:   order_id -> order node (open-addressing hash, pre-sized) -> O(1) cancel
  memory:        all nodes from pre-allocated pools; no allocation, no locks, no syscalls on the hot path

Incoming BUY limit L for qty Q:
  while Q > 0 and best_ask <= L: fill against the head of the best ask level (price = resting order's price),
                                 emit Executed for both sides, remove filled resting orders, advance best_ask
  if Q > 0 and tif == DAY: append to the tail of bid level L (time priority = position in the list)
  if Q > 0 and tif == IOC: cancel the remainder
```

Resting order price wins (the aggressor gets price improvement). Self-trade prevention (a member's buy matching its own sell) is checked at fill time by comparing account IDs and canceling one side according to the member's chosen policy. Price collars reject limit prices outside the band before they reach the book.

#### Deep dive: latency engineering, market data, and pre-trade risk

**Keeping the tail flat** ([kernel bypass](../computer-science/CS_Fundamentals.md#why-the-kernel-network-stack-is-too-slow-and-kernel-bypass)):

- Kernel-bypass NICs (DPDK or vendor user-space stacks) with busy-polling threads, so no interrupts, syscalls, or context switches on the data path.
- Cores isolated from the scheduler (`isolcpus`, `nohz_full`), IRQs moved elsewhere, threads pinned, memory on the local NUMA node, huge pages to avoid TLB misses, everything pre-faulted at startup.
- Stages connected by single-producer single-consumer ring buffers (Disruptor-style) rather than locked queues.
- Hardware timestamps at every NIC, recorded per hop into latency histograms; the p99.9 and the maximum are tracked per minute, because a single 2 ms stall during a burst matters more than the median.
- Gateways and risk checks are candidates for FPGAs when software cannot reach the budget.

**Market data fan-out.** Publish over **UDP multicast** on two independent networks (feed A and feed B); subscribers take whichever copy of each `channel_seq` arrives first, so a single packet loss on one network is invisible. A gap on both triggers recovery from a **retransmission server** (TCP, rate-limited, for small gaps) or a **snapshot**: a late joiner subscribes to the incremental channel, buffers it, reads a snapshot tagged with `channel_seq = S`, applies buffered messages with `channel_seq > S`, and is then live. Offer depth tiers: full order-by-order (every add, execute, cancel), aggregated price levels, and top of book. Retail and web consumers get a separate conflated feed (latest state per symbol every 100 ms) over TCP or WebSocket from a distribution tier, never from the core publishers.

**Pre-trade risk at the gateway:**

- Fat-finger checks: maximum order quantity and notional, price collar against the reference price.
- Credit: per account, `open buy notional + executed buy notional <= limit` (and the same for sells). Each account is owned by exactly one risk thread, which updates its exposure when it sends an order and when execution reports come back, so the check is a few in-memory additions with no locks.
- Throttles per session (messages per second) and a **kill switch**: a member or the exchange can trigger a mass cancel, which is itself a sequenced message, so it is ordered deterministically against in-flight orders.

**Fairness.** Priority is defined by sequence order at the sequencer. Fairness therefore means equal paths to it: equal-length cables in colocation, identical gateway hardware, and no member-specific fast lanes. Some venues add a deliberate fixed delay (a "speed bump") on inbound orders to reduce the advantage of the very fastest participants; that is a market-structure decision, not a technical requirement.

#### Failure modes and mitigations

| Failure | Impact | Mitigation |
|---|---|---|
| Gateway crash | Sessions on it drop | Members reconnect to another gateway and resynchronize by session sequence; duplicate `cl_ord_id`s are rejected by sequenced state |
| Sequencer primary failure | Partition stops sequencing | Arbiter promotes the standby with a new epoch; old-epoch messages are dropped; sub-second |
| Matching engine primary failure | Outputs stop | Hot standby promoted; resumes from last confirmed output; consumers dedupe by exec ID |
| Primary and standby diverge | Book possibly wrong | Output hash comparison detects it; halt the affected symbols; recover from the journal with a fixed build |
| Market data packet loss | Subscribers' books gap | A/B feed arbitration, retransmission service, snapshots |
| Runaway member algorithm | Floods the book, risk breach | Session throttles, credit limits, kill switch as a sequenced mass cancel |
| Journal disk failure | Async durability lost | Mirrored journals on both sequencers; alert and fail over before the second copy is at risk |

#### Tradeoffs

| Decision | Chosen | Alternative | Why |
|---|---|---|---|
| Matching concurrency | One thread per partition | Multi-threaded book with locks | Deterministic, no lock contention, and a single core has 5-20x headroom |
| Durability | Replicate the sequenced log in memory to a standby | fsync per message, or a database transaction per order | Microsecond budget; one disk flush alone can exceed it |
| Replication | Deterministic replay of the input log | Replicating state changes | Inputs are smaller and simpler, and replay doubles as recovery and audit |
| Failover authority | External consensus arbiter with epochs | Standby self-promotes on missed heartbeats | Prevents two primaries publishing after a pause |
| Market data | UDP multicast, A/B feeds, snapshots | TCP unicast per subscriber | 120 GB/s of unicast is impossible; multicast is fair and cheap |
| Sequencer topology | Per-partition sequencers | One global sequencer | Failure isolation; a global sequencer is also valid at this rate |

**Main interview tradeoff:** the design gives up parallelism inside a symbol to gain determinism. One thread per book makes matching simple, lock-free, and fast enough, and determinism turns replication, failover, recovery, and audit into one mechanism: replay the sequenced log. The cost is that throughput per symbol is capped by one core, and every source of nondeterminism (clocks, threads, floating point, hash order) must be engineered out. At about 1-2 µs per message, the cap is far above any single symbol's real rate.

#### Follow-ups with model answers

**Q1. Why not store orders in a database and match with transactions?**

A single commit with synchronous replication costs hundreds of microseconds to milliseconds, which is 10-100x the whole latency budget, and the hottest symbol's 100k messages/s would all contend on one book's rows. More fundamentally, matching is a sequential computation over an ordered stream, which a database would serialize anyway, just slower. The log plus in-memory state machine is the database here: the journal is the write-ahead log and the book is the materialized state.

**Q2. Could you use multiple threads to match one hot symbol faster?**

Price-time priority is a total order over the symbol's messages, so the work is inherently sequential; parallel threads would need locks around the book and would make results depend on thread scheduling, breaking determinism and replay. Use parallelism across symbols (partitions) and across pipeline stages (decode, risk, sequence, match, publish on different cores connected by ring buffers), not within one book.

**Q3. How would you add the opening auction?**

During the pre-open, orders are accepted into the book but not matched. At the scheduled time, a **scheduler** injects an `Uncross` command into the sequenced stream (never a timer inside the engine). The engine computes the single price that maximizes executable volume (ties broken by minimum imbalance, then closeness to the reference price), executes all crossing orders at that price, publishes the result, and switches the symbol to continuous trading. Because the trigger is a sequenced message, every replica uncrosses at exactly the same point.

**Q4. A member says their order should have been filled before someone else's. How do you investigate?**

The journal has every input with its sequence number and the gateway's NIC receive timestamp, and every output with the input sequence that produced it. Replay the symbol's journal up to the moment in question to reconstruct the exact book, then show where each order sat in the price level's queue and why. If the dispute concerns arrival order, compare gateway hardware timestamps with sequence order to check for unfair path differences.

**Q5. How do you support a spread order (buy A, sell B atomically)?**

Atomic multi-symbol execution needs both books in one deterministic state machine. Place related instruments (for example a future and its calendar spreads, or an option chain) in the same partition, and implement implied matching there. Spreads across partitions would need a coordinator and two-phase protocol inside a microsecond budget, which is why exchanges group by product family instead.

#### Level signals

- **Mid:** in-memory order book with price levels and FIFO queues; one engine per symbol; persistence through a log.
- **Senior:** sequencer plus deterministic single-threaded engine; replication by replay to a hot standby; latency budget per hop; multicast with sequence numbers and snapshots; pre-trade risk at the gateway with ownership per account.
- **Staff:** enumerates determinism rules and divergence detection; fencing with epochs from an external arbiter; output gating to overlap replication; fairness as path equality and market-structure choices (speed bumps, auctions as sequenced events); halts as the safe failure mode.

See also: [LLD A7 Order Book Matching Engine](LLD_Practice_Problems.md#a7-order-book-matching-engine), [CS 8.13 Leases and Fencing](../computer-science/CS_Fundamentals.md#813-consistency-guarantees-split-brain-leases-and-fencing), [Kernel Bypass](../computer-science/CS_Fundamentals.md#why-the-kernel-network-stack-is-too-slow-and-kernel-bypass), [Mock hint A10](HLD_Mock_Interviews.md#a10-stock-exchange-matching-engine)

---

### A10. Online Coding Judge

#### Requirements and assumptions

- **Submissions:** source code in one of about 20 languages for one of 3,000 problems. Two modes: **Run** (compile and run on the user's custom input) and **Submit** (all hidden tests, stop at the first failure).
- **Verdicts:** Accepted, Wrong Answer, Time Limit Exceeded, Memory Limit Exceeded, Runtime Error, Compile Error, Output Limit Exceeded; with CPU time, peak memory, and the first failing visible test where allowed.
- **Limits:** per problem (typically 1-2 s CPU, 256 MB), scaled per language by calibrated multipliers. Some problems use a custom checker (floating-point tolerance, multiple correct answers) or an interactor.
- **Scale:** 2M judge requests/day normally; a weekly contest with 60k participants brings about 10x the normal peak for its first and last 15 minutes.
- **Latency:** practice verdict p95 under 15 s; during contests, queue wait p95 under 30 s.
- **Security:** submissions are hostile. They must not escape to the host, reach the network, read test data, other users' code, or the judge's credentials, or degrade other submissions' timing.
- **Fairness:** the same submission gets the same verdict every time (time measurement reproducible within about ±5%); contest ranking uses **submission time**, not judging time.
- **Out of scope:** the problem-authoring tool, editorial content, the discussion forum.

#### Capacity estimate

```text
Practice:     2M requests/day ÷ 86,400 ≈ 23/s average; peak ≈ 60/s
Contest:      60k participants × ~4 requests per 10 minutes in the opening and closing rush
              = 240k ÷ 600 s = 400/s, bursts to ~600/s  (≈ 10x the practice peak)

Cost per request, in core-seconds on a pinned core:
  sandbox restore from a warm snapshot 0.05-0.2 s
  compile: C++ ~2 s, Java ~1.5 s, Python/JS 0 s
  tests:   ~50 tests × ~20 ms = ~1 s, stopping at the first failure
  Submit ≈ 3 core-s; Run (one input) ≈ 1 core-s; blended ≈ 2.5 core-s

Slots (Little's law: busy slots = arrival rate × service time):
  practice peak:  60/s × 2.5 s  = 150 slots
  contest peak:   600/s × 2.5 s = 1,500 slots, + practice ≈ 1,650 slots
Hosts:        16 physical cores, SMT disabled, 12 judge slots each (4 cores for the agent, IRQs, compile spillover)
              practice: 150 ÷ 12 ≈ 13 hosts (run ~20); contest: 1,650 ÷ 12 ≈ 138 hosts (provision ~160)
Under-provisioned contest: 1,200 slots -> 1,200 ÷ 2.5 = 480/s served; arrivals 600/s -> backlog grows 120/s
              -> after 10 minutes, 72k queued ≈ 150 s of wait at the full drain rate: users stop getting feedback
Test data:    3,000 problems × ~50 tests × ~200 KB ≈ 30 GB (plus a few large-input problems) -> on every host's NVMe
Source code:  2M × ~2 KB ≈ 4 GB/day ≈ 1.5 TB/year
```

**What the numbers decide:** the steady state needs about 20 hosts, but a contest needs about 160, and reactive autoscaling (minutes to boot hosts and warm sandboxes) is too slow for a spike that begins at a known second. So **pre-scale on the contest schedule**. Each request costs seconds of a dedicated core, so the queue is the main control point: priority lanes, admission control, and shedding of low-value work. Test data is small enough to cache everywhere.

#### Interfaces and data

```text
POST /v1/submissions { problem_id, language, source, mode: RUN|SUBMIT, custom_input?, contest_id?, idempotency_key }
     -> 202 { submission_id }                          (rate limit: e.g. 1 request per 5 s per user)
GET  /v1/submissions/{id} -> { status: QUEUED|COMPILING|RUNNING|DONE, verdict, passed, total,
                               cpu_ms, peak_kb, first_failed?: { input_excerpt, expected, got } }
WS   /v1/submissions/{id}/events                       (status pushes; polling is the fallback)
POST /admin/rejudge { problem_id | submission_ids[], test_set_version, priority }

submission (sharded by submission_id; secondary index on (user_id, created_at) and (contest_id, problem_id)):
  submission_id (time-ordered 64-bit) PK, user_id, problem_id, contest_id, language, source_key,
  submitted_at (server time; contest ranking uses this), mode, status, current_run_id
judge_run: PRIMARY KEY (submission_id, run_id), attempt, test_set_version, judge_image_digest,
           verdict, cpu_ms, peak_kb, worker_id, started_at, finished_at
judge_job (queue message): { submission_id, run_id, attempt, lane: CONTEST|SUBMIT|RUN|REJUDGE, language,
           problem_id, test_set_version, limits: { cpu_ms, wall_ms, mem_mb, output_kb, pids } }
problem_testset: PRIMARY KEY (problem_id, version), bundle_digest (sha256), checker_digest,
           base_time_limit_ms, per-language multipliers
```

Shard submissions by `submission_id` (writes are spread evenly), with secondary indexes for "my submissions" and contest views. The verdict lives in `judge_run` rows, never overwritten: a rejudge adds a run and moves `current_run_id`, so history and audit are preserved.

#### Architecture and flow

```text
Users --> API (auth, per-user rate limits) --> Submission service --> DB (submission + judge_run QUEUED) + outbox
                                                                             |
                                                                             v
                          Judge queue: lanes CONTEST > SUBMIT > RUN > REJUDGE (leases with visibility timeout)
                                                                             |
                                       pull: a worker takes a job only when a slot is free
                                                                             v
   Judge host (SMT off, fixed CPU frequency, 12 pinned slots) -- host agent:
     test-data cache (content-addressed bundles on NVMe, verified by sha256)
     per slot: microVM restored from a per-language snapshot
        compile sandbox (time 10 s, 512 MB) --> run sandbox per test (stdin from file, stdout to capped file)
        --> checker sandbox (diff, tolerance, or custom checker) --> verdict
                                                                             |
                                    verdict event (submission_id, run_id, attempt)
                                                                             v
   Result service --> conditional update of judge_run --> push to the user (WebSocket) --> contest scoreboard
   Control plane: contest scheduler (pre-scale, prefetch, warm), calibration jobs, host recycling
```

**Submit path:**

1. The API validates the request (problem exists, language allowed, source under 64 KB, rate limit), stores the source in object storage, inserts `submission` and `judge_run` rows plus an outbox event in one transaction, and returns `202` with the ID. The idempotency key makes a double click return the same submission.
2. The outbox relay enqueues a `judge_job` in the right lane.
3. A host agent with a free slot pulls the highest-priority job, acquiring a lease. It restores a clean microVM for the language, compiles, then runs each test: input piped to stdin, output captured to a size-capped file, CPU time and peak memory read from the sandbox's cgroup.
4. The checker compares output with the expected answer, outside the submission's sandbox. On the first failure (Submit) or after all tests, the agent publishes the verdict and destroys the microVM.
5. The result service applies the verdict with a conditional update and pushes it to the user; contest verdicts also update the scoreboard.

#### Deep dive: sandboxing untrusted code

**Threat model.** A submission may try to: exploit a kernel bug through syscalls; read files (test answers, other submissions, credentials); open network connections (exfiltrate tests, attack internal services, mine cryptocurrency); exhaust resources (fork bombs, memory, disk, gigabytes of output, millions of threads); sleep forever to hold a slot; or measure neighbors through timing side channels. Every layer below exists for one of these.

**Per-test process sandbox** (what tools like nsjail or isolate assemble; details in [Containers 2.3](../tools/Containers_and_CI.md#23-capabilities-seccomp-and-rootless), [Containers 3](../tools/Containers_and_CI.md#3-cgroups-v2-controllers), and [CS 1.13](../computer-science/CS_Fundamentals.md#113-containers-and-virtualization-isolation-theory)):

- **Namespaces:** new PID, mount, IPC, UTS, and user namespace (root inside maps to an unprivileged UID outside), and an **empty network namespace** (only a down loopback): no network at all.
- **Filesystem:** read-only root with only the language runtime; a size-limited tmpfs for `/tmp` (for example 64 MB); no test files mounted. Input arrives on stdin through a pipe and output leaves through stdout, so expected answers never exist inside the sandbox.
- **cgroups v2:** `memory.max` at the limit plus a small runtime allowance, `memory.swap.max = 0`, `pids.max = 64` (fork bombs fail at the 65th task), `cpuset` pinned to the slot's core, `io.max` on the scratch device.
- **seccomp-bpf allowlist** per language: only the syscalls that runtime needs (dozens, not hundreds); anything else kills the process with `SIGSYS`, which is reported as Runtime Error and logged as a security event. `no_new_privs` and all capabilities dropped.
- **rlimits** as backstops: `RLIMIT_CPU` slightly above the limit, `RLIMIT_FSIZE` for output, `RLIMIT_NOFILE`, `RLIMIT_CORE = 0`.

**The outer boundary.** A container shares the host kernel, so one exploitable syscall in the allowlist compromises the host and every other submission on it. For hostile code at this volume, add a second boundary:

| Boundary | How it isolates | Start cost | Runtime overhead | What an attacker must break |
|---|---|---|---|---|
| Container only (namespaces, cgroups, seccomp) | Filters syscalls to the shared host kernel | ~50-100 ms | Negligible | One kernel bug reachable through the allowed syscalls |
| gVisor | A user-space kernel implements syscalls; only a small set reaches the host | ~100s of ms | Large for syscall-heavy code, small for pure computation | gVisor itself, then its narrow host interface |
| Firecracker microVM | Hardware virtualization (KVM) with a minimal device model | ~125 ms boot; faster from a snapshot | ~5 MB memory per VM; near-native CPU | The hypervisor: a much smaller attack surface |

Choose **one microVM per slot, restored from a per-language snapshot for every submission and destroyed afterwards**, with the process sandbox inside it for each test. No state survives between users, and an escape from the process sandbox lands in a disposable VM with no network and no credentials. Hosts are recycled (reimaged) every 24 hours and run only the agent, whose credentials allow pulling jobs and test bundles and nothing else. Compare [Containers 7](../tools/Containers_and_CI.md#7-containers-vs-vms-and-hypervisors) for the general container-vs-VM tradeoff.

#### Deep dive: resource limits and accurate CPU-time measurement

**CPU time, not wall time.** Wall time on a shared machine includes waiting for other work. Measure the cgroup's `cpu.stat usage_usec` after the process exits: it includes every thread and child, so spawning threads cannot hide work, and user plus system time both count. Also enforce a **wall limit** (for example `2 × cpu_limit + 1 s`) to catch programs that sleep or block on input forever.

**Making one second mean the same everywhere** (sources of noise in [Perf 8.1](../computer-science/Performance_Engineering.md#81-sources-of-noise)):

- One slot per **physical core**, SMT disabled (a sibling hyperthread can slow a program by 20-40%), and each microVM's vCPU pinned to that core.
- Fixed CPU frequency: `performance` governor, turbo disabled. With turbo, the same program runs faster on an idle host than on a busy one.
- Fewer slots than cores (12 of 16) to leave headroom for memory bandwidth and the host agent; a homogeneous hardware model per judging pool.
- **Near-limit reruns:** interference only ever adds time, so if a test's CPU time lands within ±10% of the limit, rerun it up to twice and take the **minimum**. This removes most verdicts that flip between Accepted and TLE on resubmission.
- **Calibration:** every night, each host runs a fixed set of reference solutions; a host whose times deviate by more than 5% from the fleet median is quarantined (thermal problems, a bad BIOS setting, a noisy neighbor in a cloud VM).

**Memory:** `memory.max` enforces the limit; an OOM kill increments `oom_kill` in `memory.events`, which maps to Memory Limit Exceeded rather than a generic runtime error. Peak usage comes from `memory.peak`. Managed runtimes need runtime flags that match the limit (for example a Java heap maximum below the cgroup limit), or they fail confusingly. **Output:** stdout goes to a file capped by `RLIMIT_FSIZE` (for example 64 MB); exceeding it is Output Limit Exceeded.

**Language fairness:** set the limit from the author's reference solution (for example 2-3x its time) and calibrated per-language multipliers (interpreted languages get more), and exclude a measured runtime startup baseline for languages with heavy startup.

#### Deep dive: the judging pipeline, contest bursts, and rejudges

**Queue and leases.** Workers **pull**: a host agent asks for a job only when a slot is free, so no host is ever overcommitted. A pulled job is leased with a visibility timeout (for example 60 s, extended by heartbeats for long test suites); if the host dies, the lease expires and the job is redelivered with `attempt + 1`. The verdict write is fenced by attempt, so a slow "zombie" worker from an expired lease cannot overwrite a newer result:

```text
UPDATE judge_run SET status = 'DONE', verdict = ?, cpu_ms = ?, peak_kb = ?, finished_at = now()
 WHERE submission_id = ? AND run_id = ? AND attempt = ? AND status <> 'DONE'
```

The same claim-and-fence pattern is in [HLD 6.12](../computer-science/High_Level_Design.md#deep-dive-claiming-work-safely).

**Test data on workers.** Each problem's test set is an immutable, content-addressed bundle (`sha256` in `problem_testset`). Hosts cache bundles on NVMe and verify the digest on download. A new test set is a new version, never an in-place edit, so a host can never judge with half-updated tests.

**Contest bursts:**

- **Pre-scale on the schedule:** 30 minutes before the start, grow the pool to the forecast (registered participants × historical requests per participant × 2.5 core-s, plus 20% headroom), restore warm microVM snapshots for the top languages, and prefetch the contest's test bundles to every host.
- **Priority lanes:** contest jobs strictly before practice Submit, then Run, then rejudges. During the peak, practice Run requests from non-participants are rate-limited further or paused with a clear message; this is the sheddable load ([HLD 5.8](../computer-science/High_Level_Design.md#58-backpressure-and-load-shedding)).
- **Per-user concurrency:** one in-flight contest submission per user, so a participant cannot flood the queue.
- **Autoscale on queue wait, not CPU:** CPU is always near 100% when busy; the signal that matters is how long jobs wait. Show users their queue position so a delay is visible, not mysterious.
- Ranking uses `submitted_at`, so queue delay never changes standings; it only delays feedback.

**Rejudges and result consistency.** A wrong test case, a checker bug, or a judge image change requires judging submissions again. Enqueue a new `judge_run` per affected submission in the REJUDGE lane (or a high-priority lane during a live contest), keep the old runs, then move `current_run_id` and recompute standings from current verdicts. Pin compilers and runtimes by **image digest** and record it in every run; never upgrade a compiler during a contest, since a different optimizer can change both timing and the behavior of programs with undefined behavior.

**Plagiarism detection (offline, after each contest).** For each problem, tokenize accepted submissions and normalize them (strip comments and whitespace, rename identifiers to placeholders, canonicalize literals), hash every k-token sequence, and keep a winnowed subset of fingerprints (the minimum hash in each sliding window, as in MOSS). An inverted index from fingerprint to submissions finds candidate pairs without comparing all 60k × 60k pairs. Ignore fingerprints that appear in more than about 1% of submissions (shared templates and textbook code), score pairs by fingerprint overlap, and send pairs above a threshold to human review.

#### Failure modes and mitigations

| Failure | Impact | Mitigation |
|---|---|---|
| Host dies mid-judge | Job stalls | Lease expires; redelivered with `attempt + 1`; attempt-fenced verdict write |
| Sandbox escape attempt | Potential host compromise | seccomp kills unexpected syscalls; microVM boundary; no credentials or network inside; hosts recycled daily; security alerts on `SIGSYS` patterns |
| Contest backlog | Users wait minutes for feedback | Pre-scaling, strict lane priority, shedding practice Run, per-user concurrency limit, visible queue position |
| Timing drift on a host | Verdicts flip between AC and TLE | Fixed frequency, SMT off, nightly calibration with quarantine, near-limit reruns taking the minimum |
| Wrong test case found mid-contest | Incorrect verdicts | New test-set version, rejudge lane with high priority, standings recomputed from current runs |
| Corrupt test bundle | Mass Wrong Answer | Digest verification on download; canary judge of the reference solution before a bundle is used |
| Push channel dropped | User sees no result | Client falls back to polling `GET /v1/submissions/{id}` |

#### Tradeoffs

| Decision | Chosen | Alternative | Why |
|---|---|---|---|
| Isolation | microVM per slot, process sandbox per test | Containers only | Hostile code at scale; a shared-kernel bug would expose every submission and the host |
| Time measurement | cgroup CPU time on pinned, fixed-frequency cores | Wall time on shared hosts | Reproducible verdicts; wall time mixes in other work |
| Dispatch | Workers pull with leases | Central push scheduler | Never overcommits a host; simple failure handling |
| Capacity | Pre-scale on the contest schedule | Reactive autoscaling | The spike starts at a known second; warmup takes minutes |
| Verdict storage | Append-only runs with a current pointer | Overwrite the verdict | Rejudges are auditable and reversible |
| Test delivery | Stdin and stdout pipes; tests never inside the sandbox | Mount test files read-only | The program cannot read expected answers |

**Main interview tradeoff:** isolation strength against cost and latency. Plain containers are cheap and start fast, but every submission talks directly to the shared kernel, and an online judge executes millions of programs written specifically by people who may try to break it. A microVM per slot costs a little memory and about 100 ms per submission, which is small next to seconds of compile and test time. Similarly, dedicating physical cores and disabling turbo wastes peak performance in exchange for reproducible verdicts, which is the product's core promise.

#### Follow-ups with model answers

**Q1. Why not just run each submission in a Docker container with the default profile?**

The default profile is designed for trusted applications: it allows networking (unless you disable it), allows hundreds of syscalls, does not limit pids or output size by default, and shares the host kernel. Even hardened (no network, strict seccomp allowlist, user namespace, cgroup limits), one kernel vulnerability reachable through an allowed syscall compromises the host and every concurrent submission. Hardened containers are the inner layer; the microVM (or gVisor) is what bounds the blast radius.

**Q2. A submission forks 10,000 processes, allocates 100 GB, and prints 10 GB. What happens?**

`pids.max = 64` makes the 65th `fork` fail with `EAGAIN`; the program typically crashes, which is a Runtime Error. Allocation beyond `memory.max` triggers a cgroup OOM kill, detected through `memory.events` and reported as Memory Limit Exceeded; with swap disabled, it cannot thrash the host. Output beyond `RLIMIT_FSIZE` raises `SIGXFSZ`, reported as Output Limit Exceeded, and the scratch tmpfs has its own size cap. None of it affects other slots because each limit is per cgroup and per microVM.

**Q3. How do you support interactive problems, where the program talks to an interactor?**

Run the interactor in its own sandbox and connect the two with a pair of pipes (program stdout to interactor stdin and back). Both have limits, and the verdict comes from the interactor's exit code. Time the submission's CPU time only, because the interactor's time is not the user's fault, and enforce a wall limit on the pair to catch deadlocks where each side waits for the other. Output flushing is the classic user mistake; the problem statement must say so.

**Q4. How would you make Python competitive with C++ under the same limits?**

You cannot make them equal; you make them fair enough. Calibrate per-language multipliers from reference solutions written idiomatically in each language, and for each problem verify that an intended-complexity Python solution passes with margin. Some judges also offer PyPy as a separate language. Document the multipliers so users can choose. What you must not do is vary limits per submission or per host.

**Q5. A host is compromised anyway. What can the attacker reach?**

Very little by design: the microVM has no network and no credentials; the host agent has a short-lived credential scoped to pulling jobs and test bundles for the current problems, and to publishing verdicts for jobs it holds a lease on. Test bundles for upcoming contests are fetched only at the prefetch time, limiting early exposure. Hosts are reimaged daily, verdicts from a suspect host can be rejudged elsewhere, and the attempt-fenced write prevents it from overwriting verdicts it does not hold leases for.

#### Level signals

- **Mid:** queue plus worker pool; runs code in containers with time and memory limits; no network; stores verdicts.
- **Senior:** layered sandbox with a specific threat model; CPU time from cgroups with pinned cores and fixed frequency; leases with attempt-fenced verdict writes; Little's-law sizing for the contest and pre-scaling; priority lanes; test data never visible to the program.
- **Staff:** chooses the isolation boundary with cost and attack-surface reasoning; calibration and near-limit reruns for verdict stability; append-only verdict history with pinned image digests for rejudges; contest operations end to end (forecasting, prefetch, shedding, communication); offline plagiarism detection at scale.

See also: [Containers 2.3 Capabilities, seccomp, and Rootless](../tools/Containers_and_CI.md#23-capabilities-seccomp-and-rootless), [CS 1.13 Containers and Virtualization](../computer-science/CS_Fundamentals.md#113-containers-and-virtualization-isolation-theory), [HLD 6.12 Distributed Job Scheduler](../computer-science/High_Level_Design.md#612-distributed-job-scheduler), [Mock hint A14](HLD_Mock_Interviews.md#a14-online-coding-judge)

---

### A11. Live Comments and Reactions

#### Requirements and assumptions

- **Functional:** viewers of a live stream post comments and tap reactions (heart, laugh, wow, and so on). Every viewer sees a live, readable comment feed, a live reaction meter, their own comments immediately, and their friends' comments. Moderators and the creator can pin, delete, and slow down the feed. After the event, the VOD replays comments in sync with the video.
- **Scale:** one event with **10M concurrent viewers**, plus a long tail of thousands of small streams on the same system.
- **Rates:** comments peak at **10k/s** for a few seconds after a key moment (about 2k/s sustained); reactions peak at about **1M taps/s**.
- **Latency:** another viewer sees a comment within about 2-3 s; the author sees it instantly (local echo); reaction totals update about once per second.
- **Delivery semantics:** best effort. Comments are ephemeral on the live feed; a viewer who misses some is fine. Every accepted comment is persisted for moderation, analytics, and VOD.
- **Safety:** nothing on the shared feed that fails moderation; takedowns propagate to clients within seconds.
- **Out of scope:** the video pipeline itself (see [6.5 Video Streaming Platform](../computer-science/High_Level_Design.md#65-video-streaming-platform)), direct messages, and payments for paid comments (mentioned only as a ranking signal).

#### Capacity estimate

```text
Viewers:        10M concurrent on one stream (plus a long tail of small streams)
Comments in:    10k/s peak, ~2k/s sustained; ~300 B each with metadata
                10k × 300 B = 3 MB/s of ingest -> one log partition can hold the hottest stream
Naive fan-out:  10k comments/s × 10M viewers = 1e11 deliveries/s -> impossible, and unreadable
Readable rate:  a fast-scrolling chat pane shows ~5-10 comments/s; cap at 10/s per viewer
Per viewer:     10 comments/s × ~200 B (trimmed wire format) = 2 KB/s, + reaction totals ~100 B/s
Egress:         10M × ~2.1 KB/s ≈ 21 GB/s ≈ 170 Gb/s, all of it at the last hop
Connections:    plan 200k per edge gateway (6.4 uses 250k; keep headroom for broadcast bursts)
                10M ÷ 200k = 50 gateways; run ~70 across regions for N+1 and uneven load
Per gateway:    200k × 2.1 KB/s ≈ 420 MB/s ≈ 3.4 Gb/s egress -> fine on a 25 Gb/s NIC
                flush a batch every 250 ms -> 4 frames/s × 200k = 800k socket writes/s
                ≈ 25k writes/s per core on 32 cores
Memory:         200k × ~20 KB (TLS state + small send buffer) ≈ 4 GB per gateway
Join storm:     2M viewers join in the 2 minutes before kickoff ≈ 17k connects/s
                ÷ 70 gateways ≈ 240 TLS handshakes/s each -> fine
Gateway loss:   200k clients reconnect with jitter over 30 s ≈ 6.7k/s spread over the survivors
Reactions in:   10% of viewers tapping in a peak second = 1M taps/s
                clients coalesce taps into ≤ 1 message/s -> ≤ 1M msgs/s ÷ 70 ≈ 14k/s per gateway
                gateways sum per type per 250 ms -> 70 × 4 = 280 aggregate msgs/s upstream
Tree traffic:   displayed lane ~50 comments/s × 300 B × 70 gateways ≈ 1 MB/s -> trivial
Storage:        2k/s × 3 h × 300 B ≈ 21.6M comments ≈ 6.5 GB for the whole event
```

**What the numbers decide:** everything upstream of the gateways is megabytes per second; all the cost (170 Gb/s, 800k writes/s per gateway) is at the last hop. So the design has three parts: a **sampler** that turns 10k comments/s into a few dozen per lane, a **fan-out tree** that moves each selected comment once per gateway, and **gateways** that serialize each batch once and write the same bytes to every subscribed socket. Reactions are aggregated at the gateways, which cuts 1M taps/s to hundreds of messages per second.

#### Interfaces and data

```text
WS   wss://live.example.com/v1/streams/{stream_id}/feed?lang=es&resume_seq=...
     server -> client frame every ~250 ms:
       { seq, media_ts_ms,
         comments:    [{ comment_id, author, text, badges }],
         reactions:   { heart: 18234, laugh: 950 },          -- totals for the last second
         retractions: [comment_id],
         viewers:     9870000 }
     client -> server: { reactions: { heart: 7 }, window_end_ms }   (at most 1 per second)
POST /v1/streams/{stream_id}/comments
     { client_comment_id, text, media_ts_ms } -> 202 { comment_id, status: ACCEPTED | HELD }
GET  /v1/streams/{stream_id}/lanes/{lane}/chunks/{n}.json   -> displayed comments for VOD (CDN)

comment(stream_id, comment_id (time-ordered ID), author_id, text, lang, media_ts_ms,
        created_at, moderation_state, score, displayed BOOL)
        -- log partitioned by stream_id; archived by (stream_id, created_at)
        UNIQUE (author_id, client_comment_id)                 -- idempotent posting
lane_batch(stream_id, lane_id, seq, media_ts_ms, comment_ids[])
        -- lane_id = language/region segment; archived per 10 s of media time for VOD
reaction_agg(stream_id, second, type, count)                  -- per-second totals for analytics
presence(stream_id, user_id -> gateway_id)                    -- in-memory, TTL, for friend routing
```

Comments are partitioned by `stream_id`. The hottest stream's 3 MB/s fits in one log partition, and one partition gives the sampler a single ordered input; if a stream ever outgrows it, split by author hash and let the sampler merge partitions. Gateways subscribe to a topic per `(stream_id, lane_id)`, so small streams cost the big one nothing. The lane archive is keyed by media time, not wall-clock time, because that is how a VOD player looks it up.

#### Architecture and flow

```text
Viewers (10M)
   | WebSocket or SSE down; HTTPS POST (or WS frame) up
   v
Edge gateways (~70 x 200k conns) --reaction sums every 250 ms--> Reaction aggregator
   |        ^                                                          |
   |        | lane batches, reaction totals, retractions               | totals per second
   |        +---- Regional relays (~8, in-memory pub/sub) <---- Origin publisher <---+
   |        +---- Personal router (own + friends' comments, direct to a gateway)   ^
   | POST comment                                                                   |
   v                                                                                |
Comment ingest -----> Fast filter -----> Comment log --------> Sampler / ranker ----+
(auth, rate limit,    (blocklist,        (partition per        (per lane, every 250 ms)
 idempotency key)      spam score,        stream_id)                  |
                       slow mode)              |                      +--> Strict moderation on candidates
                                               +--> Comment archive   +--> Lane archive -> object store -> CDN (VOD)
```

**Write path (posting a comment):**

1. The client renders the comment locally at once (local echo) and POSTs it with a `client_comment_id`.
2. Ingest authenticates, applies the per-user rate limit (for example 1 comment per 2 s, tighter in slow mode), and deduplicates on `(author_id, client_comment_id)`.
3. The fast filter (blocklist, regex, a small spam model under 5 ms) runs on every comment. Rejected comments are stored but marked; only the author still sees theirs (a shadow ban is invisible to the author).
4. Accepted comments go to the comment log. The personal router delivers them straight to the gateways of the author's friends who are watching.
5. The sampler reads the log, picks each lane's comments for the next 250 ms window, sends the candidates through strict moderation, and hands the survivors to the origin publisher.

**Read path (watching):**

1. The client opens one connection to a gateway chosen by the load balancer (by region, then least connections; for small streams, by stream hash, see below).
2. The gateway subscribes to the `(stream_id, lane_id)` topic on its regional relay if it is not already subscribed, and immediately sends the last ~20 displayed comments from its ring buffer.
3. Every 250 ms the gateway builds one frame per lane (comments, reaction totals, retractions), serializes it once, and writes it to every subscribed connection.
4. The client holds each comment until its own playhead reaches the comment's `media_ts_ms`, then renders it.

#### Deep dive: connection tier and hierarchical fan-out

**Protocol.** Traffic is overwhelmingly server-to-client. **Server-Sent Events** over HTTP/2 are enough for the downstream (simple, proxy-friendly, automatic reconnect with `Last-Event-ID`), with comments posted over ordinary HTTPS. **WebSocket** is the choice when reactions also flow upstream on the same connection; native apps use it, browsers can use either. See [WebSockets vs HTTP](../computer-science/CS_Fundamentals.md#websockets-vs-http). Disable per-connection compression (`permessage-deflate`): it costs tens of KB of state per connection and defeats sharing one serialized buffer across 200k sockets.

**Gateway internals.** One event loop per core (epoll), connections pinned to cores. On each 250 ms tick, a gateway serializes each lane's frame **once** into a reference-counted buffer and enqueues a pointer to it on each subscribed connection. Per-connection work is then TLS encryption and the `write`, which is unavoidable but cheap (AES-GCM runs at GB/s per core). Heartbeats terminate at the gateway, exactly as in [6.4 Chat System](../computer-science/High_Level_Design.md#64-chat-system).

**The tree.** The origin publisher emits each lane batch once to about 8 regional relays; each relay fans out to the 5-15 gateways in its region. Each layer multiplies by about 10, and only the last hop multiplies by 200k. Relays are plain in-memory pub/sub (no durability): a lost batch is simply a gap, and the durable record is the comment log. The tree also means a batch crosses an ocean once per region, not once per gateway.

```text
Origin (1) --> Relays (8) --> Gateways (70) --> Viewers (10M)
  fan-out:  x8            x~9              x~143k on average
  per tick: 8 msgs        70 msgs          10M socket writes (spread over 70 machines)
```

**Small streams.** With random placement, a 300-viewer stream would put one viewer on each of 70 gateways, so every gateway would subscribe to every stream topic. Instead, the load balancer routes by consistent hashing of `stream_id` onto a small gateway set sized to the stream's audience (1-2 gateways for small streams, all gateways for the 10M event). Gateway subscriptions then scale with viewers, not with streams.

**Slow clients.** Each connection has a bounded send queue of about two frames. If the queue is full when a new frame arrives, the gateway **drops the older comment frame** and keeps the newest; reaction totals and viewer counts are snapshots, so the latest one supersedes the others. A connection that stays behind for 10 s gets a lower lane rate, and then is closed. Never buffer without bound: one slow client must not cost memory proportional to the event's length. This is load shedding at the edge ([5.8 Backpressure and Load Shedding](../computer-science/High_Level_Design.md#58-backpressure-and-load-shedding)).

#### Deep dive: sampling, throttling, and reaction aggregation

**Lanes.** A lane is a `(stream, language or region)` segment, for example 30 lanes for the final. Each lane has a target display rate of R = 10 comments/s (clients can ask for a slower lane). The sampler works in 250 ms windows: if a window has at most R/4 candidates, all pass. Otherwise it selects R/4 of them.

**Selection policy.** A pure ranking (top-scored only) shows the same verified accounts all match; a pure random sample shows spam and repetition. Use **weighted random sampling**: weight = f(quality model score, author reputation, verified or creator badge, early likes, paid highlight), and select with weighted reservoir sampling (A-Res: key = u^(1/w) for u uniform in (0, 1), keep the k largest keys), which is one pass with O(k) memory. Add diversity rules: at most one comment per author per 30 s on a lane, and collapse near-duplicates. A count-min sketch over normalized text in a 5 s window ([4.10 Probabilistic Counting](../computer-science/High_Level_Design.md#410-probabilistic-counting-hyperloglog-and-count-min-sketch)) spots "GOOOAAAL" posted 40,000 times; emit one synthetic item ("40k people: GOAL") instead of 40,000 rejections.

**Personal items bypass the sampler.** The author's own comment is rendered locally and confirmed by `comment_id`. Friends' comments go through the personal router: the presence index (10M entries × ~50 B ≈ 500 MB, in memory, refreshed by gateway heartbeats) says which of the author's friends are watching and on which gateway. At 10k comments/s with about 5 watching friends each, that is about 50k targeted deliveries/s, small next to the broadcast. Creator and moderator pins are injected into every lane with priority.

**Reactions.** Forwarding 1M taps/s would be pointless: nobody can see individual taps. Aggregate at every layer:

1. The client coalesces taps and sends at most one message per second (`{heart: 7}`), capped per connection (for example 20 counted taps/s) so a script cannot inflate the meter.
2. Each gateway sums per `(stream, type)` per 250 ms and sends 280 messages/s in total upstream.
3. The aggregator sums across gateways per second and publishes totals down the same tree, inside the regular frames.
4. The client animates a number of floating icons proportional to the log of the count, so 18k hearts and 25k hearts both look like "a lot".

Counts lost when a gateway crashes are acceptable for the live meter. Per-second aggregates are also written to `reaction_agg` for analytics; exact counts for billing would need the idempotent pipeline discussed in the follow-ups.

#### Deep dive: moderation, replay, and VOD sync

**Moderate what you display, strictly.** All 10k/s pass the cheap fast filter. Only sampled candidates (about 50/s per lane × 30 lanes = 1,500/s) go through the expensive toxicity model (about 20 ms each, so about 30 core-seconds per second; a few GPUs or 60 cores). Running the heavy model on every comment would cost about 7× more for comments nobody else sees. A comment that fails is dropped from the lane, and the sampler picks a replacement from the same window.

**Takedown.** A moderator or legal deletion publishes a retraction (`comment_id`) down the tree; clients remove it from the pane, the archive marks it, and the affected VOD chunk is regenerated.

**Late joiners and reconnects.** Each gateway keeps a ring buffer of the last 30 s of frames per lane (30 s × 4 frames/s × ~2 KB ≈ 240 KB per lane), so a new viewer sees a populated pane at once. A reconnect sends `resume_seq`; the gateway replays from the ring buffer if it can, otherwise it jumps to live. Gaps are acceptable because the feed is ephemeral.

**Media-time sync.** Viewers watch at different delays: LL-HLS at about 3 s, standard HLS at 20-30 s. If comments are shown on arrival, a viewer 25 s behind reads "GOAL!" before seeing the goal. So each comment carries the **author's playhead position** (`media_ts_ms`), each frame carries the lane's media time, and the client releases comments only when its own playhead reaches that position (a local buffer of up to about 30 s).

**VOD.** The lane archive is written as one small JSON chunk per lane per 10 s of media time (a 3-hour event is 1,080 chunks per lane, about 5 KB each) to object storage behind the CDN. The VOD player fetches the chunk for its current position. Because the archive stores the displayed lane rather than all comments, replay looks like the live experience.

#### Failure modes and mitigations

| Failure | Impact | Mitigation |
|---|---|---|
| Edge gateway crashes | 200k viewers lose the feed for a few seconds | Clients reconnect with jittered backoff to other gateways; ring buffer repopulates the pane; capacity is N+1 per region |
| Relay or origin publisher dies | Lanes stall for every gateway below it | Two relays per region (gateways subscribe to both and dedupe by `seq`); publisher has a hot standby reading the same log |
| Comment surge (100k/s from a raid or bots) | Ingest and fast filter overload | Per-user and per-IP rate limits, slow mode, shed by account age; the sampler's output rate is fixed regardless of input |
| Slow or mobile clients | Unbounded buffers, gateway memory blowup | Two-frame send queue, drop stale comment frames, downgrade then disconnect laggards |
| Strict moderation service slow | Lanes thin out or stall | Timeout and fall back to a conservative policy: show only comments from trusted authors until it recovers |
| Spoilers for delayed viewers | Bad experience | Release comments by media timestamp, not arrival time |
| Reconnect storm after a regional network blip | Millions of TLS handshakes at once | Jittered backoff, gateway handshake rate cap, TLS session resumption |

#### Tradeoffs

| Decision | Chosen | Alternative | Why |
|---|---|---|---|
| What viewers see | Sampled, ranked lane per segment | Every comment | 1e11 deliveries/s is impossible and unreadable |
| Fan-out transport | In-memory relay tree, best effort | Durable broker with a subscription per viewer | Durability adds nothing for an ephemeral feed; per-viewer queues multiply broker load by 10M |
| Moderation placement | Cheap filter on all, strict model on displayed candidates | Strict model on everything | About 7× cheaper, and it covers everything other viewers can see |
| Reactions | Aggregated counts per second | Individual reaction events | 1M/s of identical tiny events carry no information beyond the count |
| Slow clients | Drop stale frames | Queue until caught up | A late comment is worthless; queues turn slowness into memory exhaustion |
| Downstream protocol | WebSocket (SSE where only downstream is needed) | Long polling | 10M polls per second of request overhead |

**Main interview tradeoff:** **completeness versus readability and cost.** Delivering every comment is both physically impossible at this scale and worse for users, so the system deliberately shows each viewer a sample. The cost is fairness: most comments are never seen by anyone except the author and friends. The design makes that explicit with a ranking policy, local echo, friend routing, and synthetic "40k people said..." items, so the room still feels alive and each viewer still feels heard.

#### Follow-ups with model answers

**Q1. How does a viewer see their own comment immediately, and what if moderation rejects it?**

The client renders the comment optimistically with a pending marker as soon as it is submitted, then replaces the marker when the 202 returns a `comment_id`. Whether the comment is also sampled into the shared lane is independent. If the fast filter rejects it for spam or a blocklist hit, the author still sees it locally (a shadow ban), which avoids teaching spammers what triggers the filter. Clear policy violations, such as slurs, are rejected with an explicit error instead. Idempotency on `(author_id, client_comment_id)` means a retried POST on a flaky network never creates a duplicate.

**Q2. A gateway with 200k viewers dies during the final. Walk through it.**

Clients notice within one heartbeat interval (or immediately on TCP reset), wait a random 0-30 s backoff, and reconnect through the load balancer to the surviving gateways: about 6.7k handshakes/s spread over 69 machines, which TLS session resumption makes cheap. Each new gateway is already subscribed to the lane, so it sends its ring buffer and the viewer sees a populated pane. Viewers lose a few seconds of comments, which nobody notices. Reaction taps counted on the dead gateway in its last 250 ms are lost, which is within the meter's tolerance. Capacity planning must assume one gateway down per region (N+1); otherwise the reconnect pushes survivors past their connection limit and the failure cascades.

**Q3. Product says, "Every comment should be seen by at least some viewers." How?**

Split each lane into sub-lanes: assign viewers to one of k sub-lanes by hash, and let the sampler pick a different sample for each. With k = 100 sub-lanes at 10/s each, the system can display 1,000 distinct comments per second per language, each to about 1% of that lane's viewers. At 10k comments/s that still leaves most comments unseen, so pair it with ranking (high-quality comments go to more sub-lanes) and with synthetic aggregation for duplicates. The fan-out cost is unchanged; each gateway just subscribes to more sub-lane topics and serializes more frames.

**Q4. A sponsor pays per reaction. How do you make the count exact?**

The live meter stays approximate; billing gets a separate, idempotent pipeline. Each client batch carries `(connection_id, window_seq)`, and the gateway appends batches to a durable log before acknowledging them. A stream processor deduplicates on that key and aggregates by event time, which gives effectively-once counts (see [4.11 Stream Processing](../computer-science/High_Level_Design.md#411-stream-processing)). Then define what counts: per-connection caps, bot filtering, and whether ten taps by one person count as ten. Those definitions matter more for the sponsor than the plumbing does.

**Q5. How does this design change for 50,000 streams with 200 viewers each?**

Total viewers are the same (10M), but there is no fan-out problem: 200 viewers can see every comment of a stream that gets one comment per second, so the sampler passes everything through. The pressure moves to the subscription layer, which is why stream-affine gateway placement matters: each small stream lives on one or two gateways, and relays carry 50,000 low-rate topics instead of a few hot ones. The same code handles both regimes because the sampler only throttles when the input rate exceeds the lane's display rate.

#### Level signals

- **Mid:** WebSocket gateways with a pub/sub layer, persists comments, notices that 10M connections need many gateway servers.
- **Senior:** shows the 1e11 deliveries/s arithmetic and samples per lane; aggregates reactions; sizes gateways (connections, egress, writes/s); bounded send queues that drop stale frames; local echo for the author.
- **Staff:** treats the sampling policy as a product decision with fairness implications; moderates the displayed set strictly and cheaply; aligns comments to media time for delayed viewers and VOD; stream-affine placement for the long tail; separates the approximate live meter from an exact billing pipeline.

See also: [HLD 6.4 Chat System](../computer-science/High_Level_Design.md#64-chat-system), [HLD 5.8 Backpressure and Load Shedding](../computer-science/High_Level_Design.md#58-backpressure-and-load-shedding), [HLD 4.10 Probabilistic Counting](../computer-science/High_Level_Design.md#410-probabilistic-counting-hyperloglog-and-count-min-sketch), [Mock hint A15](HLD_Mock_Interviews.md#a15-live-comments-and-reactions-for-10m-viewers)

---

### A12. Vacation Rental Marketplace (Airbnb)

#### Requirements and assumptions

- **Functional (guest):** search by place or map viewport, check-in and check-out dates, guest count, price range, and filters (property type, amenities); view a listing with an exact price quote; book (instant book or request-to-book); cancel under the listing's policy; review after the stay.
- **Functional (host):** create listings, manage a calendar of available nights and nightly prices, accept or decline requests, sync calendars with other platforms via iCal, receive payouts.
- **Scale:** ~7M active listings, bookable up to 2 years ahead; ~100M searches/day; ~300k bookings/day.
- **Latency:** search p99 under 300 ms; quote under 200 ms; booking under 2 s excluding the payment provider.
- **Consistency:** **no night is ever sold twice** (hard). Search availability may lag the source of truth by up to about a minute; the booking path re-checks authoritatively.
- **Money:** charges, refunds, fees, taxes, and payouts are exact to the cent, idempotent, and auditable for years. The host is paid about 24 h after check-in.
- **Out of scope:** messaging between guest and host, photo processing, fraud scoring internals, experiences.

#### Capacity estimate

```text
Listings:       7M active; calendar horizon 2 years = 730 nights
Searches:       100M/day ÷ 86,400 ≈ 1,200/s avg -> ~4k/s peak (evenings, map panning)
Listing views:  ~300M/day ≈ 3.5k/s avg -> ~10k/s peak (mostly from cache)
Bookings:       300k/day ≈ 3.5/s avg -> ~30/s peak; look-to-book ≈ 100M ÷ 300k ≈ 330:1
Calendar rows:  7M × 730 = 5.1B listing-nights × ~50 B ≈ 255 GB (+ indexes) -> shard by listing_id
Availability:   1 bit per night: 730 bits ≈ 92 B per listing; × 7M ≈ 640 MB -> RAM on every search node
Nightly prices: dense: 7M × 730 × 4 B ≈ 20 GB; real calendars are a base price plus a few overrides
                -> base + sparse overrides ≈ 7M × ~200 B ≈ 1.4 GB
Search docs:    7M × ~2 KB (geo, type, capacity, amenity bitset, rating, ranking features) ≈ 14 GB
Calendar churn: bookings + host edits + iCal imports ≈ 10M changes/day ≈ 120/s avg
iCal polling:   ~2M listings with external feeds, refreshed every 30 min ≈ 1,100 fetches/s
Per query:      a city viewport matches ~5k-20k listings; the date-range check is a masked
                compare on the bitmap (~50 ns) -> 20k × 50 ns = 1 ms
                pricing and ranking the survivors dominate: budget ~20 ms CPU per query
Search CPU:     4k/s × 20 ms = 80 cores -> ~10 replicas of 16 cores, x2 for headroom
Money moves:    charges + refunds + payouts ≈ 1M/day ≈ 12/s -> a modest sharded ledger
```

**What the numbers decide:** writes are tiny and the read path dominates. The entire availability index (640 MB) and all search documents (14 GB) fit in one machine's memory, so search shards exist only to parallelize each query, and replicas exist for QPS. Contention per listing is close to zero, so a relational database with per-night rows and a conditional write is enough: no waiting room, no counters. The real engineering is **freshness**: about 120 availability changes per second must reach every search replica within seconds, and the booking path must tolerate search being slightly wrong.

#### Interfaces and data

```text
GET  /v1/search?bbox=...|place_id=...&checkin=2026-12-20&checkout=2026-12-27&guests=4
          &price_max_cents=30000&amenities=wifi,pool&cursor=...
     -> { results: [{ listing_id, total_price_cents, nightly_avg_cents, rating, lat, lng }], cursor }
GET  /v1/listings/{id}/quote?checkin=&checkout=&guests=
     -> { quote_id, nights[{ date, price_cents }], fees, taxes, total_cents, currency, expires_at }
POST /v1/reservations { quote_id, payment_method_token, message?, idempotency_key }
     -> 201 { reservation_id, state: CONFIRMED | PENDING_HOST } | 409 { reason: DATES_UNAVAILABLE }
POST /v1/reservations/{id}/accept | /decline            (host, request-to-book)
POST /v1/reservations/{id}/cancel                        (guest or host; refund per policy)
PUT  /v1/listings/{id}/calendar { ranges: [{ from, to, available, price_cents }] }
POST /v1/reservations/{id}/reviews { rating, text }       (after checkout)
GET  /v1/listings/{id}/calendar.ics?token=...             (iCal export)

listing(listing_id PK, host_id, lat, lng, s2_cell, tz, instant_book BOOL, max_guests,
        min_nights, max_nights, base_price_cents, currency, cancellation_policy, ...)
calendar_night(listing_id, night DATE,            -- local date in the listing's time zone
               status AVAILABLE|BLOCKED|EXTERNAL|HELD|BOOKED, price_cents NULL,
               reservation_id NULL, hold_expires_at NULL,
               PRIMARY KEY (listing_id, night))                  -- shard by listing_id
reservation(reservation_id PK, listing_id, guest_id, checkin, checkout, guests, state,
            quote_id, total_cents, currency, payment_id, expires_at, created_at,
            UNIQUE (guest_id, idempotency_key))                  -- shard by listing_id
ledger_entry(entry_id, reservation_id, account, amount_cents, currency, kind, created_at)
payout(payout_id, host_id, reservation_id UNIQUE, amount_cents, currency, release_at, state)
review(reservation_id, author_role GUEST|HOST, rating, text, submitted_at, visible_at,
       PRIMARY KEY (reservation_id, author_role))
ical_feed(listing_id, url, etag, last_fetched_at, next_fetch_at)
```

`calendar_night` and `reservation` share `listing_id` as the partition key, so booking a date range is a **single-shard transaction** over a few adjacent rows. The guest's "my trips" view needs the opposite key, so a secondary `guest_id -> reservation_id` index is maintained from change data capture. The search index is a separate read model keyed by `listing_id` and built entirely from the change stream (CQRS; see [4.12 CDC, Event Sourcing, CQRS, and the Outbox](../computer-science/High_Level_Design.md#412-change-data-capture-event-sourcing-cqrs-and-the-outbox)).

#### Architecture and flow

```text
Guest app --> CDN (photos, static pages)
          --> API gateway
               |                     |                          |
               v                     v                          v
         Search service        Listing + Quote service     Reservation service ------> Payment service (6.7)
         (scatter to index     (listing cache, pricing     (state machine; conditional      | authorize, capture,
          shards, merge,        engine, signed quotes)      write on calendar_night          | void, refund
          rank, paginate)                                    rows in one listing shard)      v
               ^                                                   |                  Ledger + payout scheduler
               |                                                   v                  (release check-in + 24 h)
         Search index replicas <---- Index updaters <---- CDC / outbox stream <---- Listing + Calendar DB
         (in memory: S2 cells,       (apply per-listing                             (sharded by listing_id)
          bitmaps, prices, docs)      deltas in seconds)                                    ^
                                                                                            |
Host app ---> Calendar API --------------------------------------------------------------+
Other platforms <-- iCal export          iCal importer (poll with ETag) --> EXTERNAL nights --+
```

**Search (read path):**

1. Resolve the place to a region and compute an S2 covering of the viewport ([4.8 Geospatial Indexing](../computer-science/High_Level_Design.md#48-geospatial-indexing)).
2. Scatter to the index shards. Each shard filters its candidates by capacity, amenities, availability for every night in `[checkin, checkout)`, and the min/max-night rules, then prices the survivors and returns its top few hundred by a cheap score.
3. The search service merges, runs the expensive ranking model on the top ~200, and returns a page.

**Booking (write path, instant book):**

1. The guest opens the listing; the quote service reads the authoritative calendar and returns a signed quote valid for about 15 minutes.
2. `POST /reservations` runs one transaction on the listing's shard: idempotency check, conditional update of every night from `AVAILABLE` to `HELD`, insert the reservation and an outbox row.
3. The payment service authorizes the card with the `reservation_id` as idempotency key.
4. On success, a second transaction flips the nights `HELD -> BOOKED` (conditioned on the same `reservation_id`) and the reservation to `CONFIRMED`; payment is captured.
5. The outbox event updates the search index, notifies the host, and schedules the payout.

#### Deep dive: the availability search index

**Per-listing layout on each index shard** (struct-of-arrays for cache locality):

```text
s2_cell u64 | max_guests u8 | amenities u128 bitset | min_nights u8 | max_nights u16
avail[12] u64      -- 730+ bits, bit i = night (epoch_day + i) is bookable
checkin_dow u8     -- allowed check-in weekdays
base_price u32 + sparse overrides [(night, price)] + weekly/monthly discount
rating, review_count, ranking features
```

**Date-range check.** For a stay of n nights starting at offset i, the listing is available if bits i through i + n - 1 are all set. With stays of at most 30 nights the range touches at most two 64-bit words, so the check is a shift, a mask, and a compare: about 50 ns. Amenity filters are `(listing & wanted) == wanted`. Flexible queries ("any 5 nights in March") test each possible start, about 30 cheap checks per listing.

**Pricing in the index.** Total price = sum of nightly prices (base or override) + cleaning fee + service fee + taxes, minus length-of-stay discounts. The index computes an estimate good enough for filtering and sorting; the quote service computes the exact, signed price.

**Sharding.** Hash-shard by `listing_id` into about 4 shards (about 4 GB each) with 10+ replicas each, and scatter-gather every query. Geo-sharding gives locality but creates hot shards (Paris in August, New York at New Year) and viewports that straddle boundaries. Because the whole index fits on a node, hash sharding plus replication is simpler and evenly loaded.

**Freshness.** Calendar changes flow from the database through CDC into a log keyed by `listing_id`. Index updaters on every replica apply the bit flips and price changes, with p99 lag under 10 s. Each update carries the listing's version so an out-of-order delta is ignored. Search can still show a listing that was booked 3 seconds ago; the quote and booking re-check the database, and the client shows "these dates were just booked" with alternatives. Track the **search-to-quote unavailability rate** as the freshness SLI. The bitmap epoch rolls forward nightly by rebuilding each shard from a snapshot plus the log.

#### Deep dive: booking date ranges without double booking

**Option A: per-night rows and one conditional update** (chosen). The same pattern as the seat hold in [6.15 Ticket Booking](../computer-science/High_Level_Design.md#615-ticket-booking-seat-reservation), applied to nights:

```sql
BEGIN;
UPDATE calendar_night
   SET status = 'HELD', reservation_id = :rid, hold_expires_at = now() + interval '15 minutes'
 WHERE listing_id = :lid AND night >= :checkin AND night < :checkout
   AND (status = 'AVAILABLE' OR (status = 'HELD' AND hold_expires_at < now()));
-- if rowcount <> (:checkout - :checkin): ROLLBACK and return 409
INSERT INTO reservation (reservation_id, listing_id, guest_id, checkin, checkout, state, ...)
     VALUES (:rid, :lid, :gid, :checkin, :checkout, 'HELD', ...);
INSERT INTO outbox (...) VALUES (...);
COMMIT;
```

The row count catches both a taken night and a missing row, so nights must be **materialized** for the whole horizon: a daily job appends one night per listing (7M inserts/day, about 81/s). Expiry is part of the predicate, so a stale hold never blocks a booking even if the sweeper is late. Two overlapping requests serialize on the first shared row lock; the loser re-evaluates the predicate and gets a short row count.

**Option B: one row per stay with an exclusion constraint** (PostgreSQL):

```sql
CREATE EXTENSION btree_gist;
CREATE TABLE stay (
  listing_id BIGINT, reservation_id BIGINT, period DATERANGE, state TEXT,
  EXCLUDE USING gist (listing_id WITH =, period WITH &&)
    WHERE (state IN ('HELD', 'BOOKED', 'BLOCKED', 'EXTERNAL'))
);
```

The index rejects any overlapping insert atomically, with one row per stay instead of one per night. The catch: index predicates must be immutable, so `now()` cannot appear in them and an expired hold keeps blocking until something flips its state. On a conflict, the service must check whether the blocker is an expired hold, expire it, and retry. It also ties the design to one database engine. Option A is portable and keeps per-night prices in the same rows.

**Booking state machine:**

```text
Instant book:
  HELD (nights HELD, 15 min) --auth ok--> CONFIRMED (nights BOOKED, capture)
  HELD --auth declined or hold expired--> EXPIRED (nights released)

Request-to-book (nights are NOT blocked while pending):
  PENDING_HOST (card authorized) --host accepts within 24 h--> conditional AVAILABLE -> BOOKED
        --rowcount ok--> CONFIRMED (capture)
        --rowcount short--> DECLINED_UNAVAILABLE (void authorization, suggest alternatives)
  PENDING_HOST --host declines or 24 h timeout--> DECLINED or EXPIRED (void authorization)

CONFIRMED --cancel--> CANCELLED (refund per policy; nights released; payout clawed back if already paid)
CONFIRMED --checkout date passes--> COMPLETED (review window opens)
```

Pending requests do not block the calendar; blocking for 24 h per request would let one indecisive guest freeze a listing. The acceptance runs the same conditional write, so the host can accept only a request whose nights are still free, and competing requests for those nights decline automatically. Every transition is a conditional update on `state`, so a timeout sweeper and a late host click cannot both win.

#### Deep dive: money, pricing, reviews, and external calendars

**Charge and payout.** Card authorizations expire after about 7 days on many networks, and stays are booked months ahead. So capture at confirmation (or capture a deposit now and the balance closer to the stay), and hold the funds as a platform liability. Each money movement is a balanced double-entry ledger write: guest charge debits cash and credits `host_payable`, `platform_fee`, and `tax_payable`. A payout scheduler finds `CONFIRMED` reservations whose check-in plus 24 h has passed, inserts a `payout` row (unique on `reservation_id`, so reruns are harmless), and calls the payout provider with `payout_id` as the idempotency key. The delay protects guests from no-shows and misrepresented listings. A cancellation after payout creates a negative host balance that is netted from future payouts. Exchange rates are locked at booking time and stored with the quote. See [6.7 Payment Processing](../computer-science/High_Level_Design.md#67-payment-processing).

**Pricing and quotes.** The quote is HMAC-signed over `(listing_id, dates, guests, total, currency, expires_at)`. The reservation service verifies the signature and honors the quoted price until expiry, even if the host edits prices in between, so the guest never sees the price change at the pay button.

**Reviews.** A review is allowed only for a `COMPLETED` reservation, at most one per `(reservation_id, author_role)` (the primary key enforces it), within 14 days of checkout. Reviews are double-blind: `visible_at` is set when both sides have submitted or the window closes, whichever is first, so neither side can retaliate. Rating aggregates update the search document asynchronously.

**iCal sync.** Export is a per-listing `.ics` URL generated from the calendar and cached until the next calendar change. Import polls each external feed with `If-None-Match` (most polls return 304), parses events into `EXTERNAL` nights through the same conditional write, and polls more often for listings with near-term demand. Polling leaves a window (up to the poll interval) in which another platform can sell the same night; if an imported block collides with a confirmed booking, alert the host immediately. Shrinking that window requires push-based channel-manager APIs; polling cannot close it.

#### Failure modes and mitigations

| Failure | Impact | Mitigation |
|---|---|---|
| Search index lags (CDC consumer stalled) | Guests see booked listings; failed quotes rise | Alert on lag and on search-to-quote unavailability rate; booking path re-checks the DB, so correctness holds |
| Payment authorized but confirm fails (hold expired) | Guest charged without a stay | Void the authorization (or refund) automatically; extend the hold when checkout starts |
| Host accepts after the 24 h timeout fired | Two conflicting outcomes | Both transitions are conditional on `state = PENDING_HOST`; exactly one wins |
| Listing shard primary fails | Bookings for those listings fail for seconds | Synchronous replica with automatic failover (RPO 0); search keeps serving from replicas |
| Payout job runs twice | Host paid twice | `UNIQUE (reservation_id)` on payout plus provider idempotency key |
| External iCal feed down or malformed | Stale external blocks; possible cross-platform double booking | Keep last good import; alert host; flag listing as sync-degraded |
| Daily night-materialization job skipped | Far-future nights not bookable | Job is idempotent and alerts on horizon gap; booking returns a clear error, never a wrong success |

#### Tradeoffs

| Decision | Chosen | Alternative | Why |
|---|---|---|---|
| Availability in search | In-memory bitmaps on every replica, CDC-updated | Query the calendar DB per search | 4k/s × 20k candidates × date ranges would crush the DB; bitmaps fit in 640 MB |
| Search sharding | Hash by listing, full replication | Geo-sharding | Even load and no boundary queries; the index fits in memory |
| Range booking | Conditional update on per-night rows | Exclusion constraint on date ranges | Portable, expiry in the predicate, per-night prices live in the same rows |
| Request-to-book | Pending does not block nights | Block nights for 24 h | Keeps calendars sellable; acceptance still uses the conditional write |
| Charge timing | Capture at confirmation, delayed payout | Authorize only until check-in | Authorizations expire within days; stays are booked months ahead |
| Calendar sync | Poll iCal with ETags | Push APIs only | Universal support; accept and surface the residual double-booking window |

**Main interview tradeoff:** **search freshness versus cost.** Making search exactly consistent would mean querying the authoritative calendar for thousands of candidates per search. Instead, search is an eventually consistent read model that is usually seconds behind, and correctness lives in one place: the single-shard conditional write at booking. The visible cost is an occasional "just booked" message, which is measured and kept low.

#### Follow-ups with model answers

**Q1. Why not reuse the ticket-booking design with a waiting room?**

The shapes differ. Ticketing has one event with tens of thousands of fungible or adjacent seats and millions of simultaneous buyers, a hot partition. Here, each listing is its own tiny inventory, bookings average 3.5/s across 7M listings, and two guests rarely contend for the same listing at the same moment. The hard parts are search over date availability and the long-lived money flow. The atomic hold mechanism is the same (conditional update on rows in one partition), but nothing else from the on-sale design is needed.

**Q2. A guest books a 7-night stay. Exactly what prevents a double booking with an overlapping 3-night request?**

Both requests run the conditional update over their own night ranges on the same listing shard. They share at least one night row; whichever transaction locks it first proceeds, and the other blocks on that row lock. When the first commits, the second re-evaluates its predicate on the locked rows, finds `HELD`, and updates fewer rows than nights requested. It rolls back and returns 409, so no partial hold survives. Because the row count is compared with the number of nights, a missing row (an unmaterialized night) also fails safely.

**Q3. The host raises the price after the guest got a quote. What does the guest pay?**

The quoted price, if they book before the quote expires. The quote is signed, so the reservation service can verify it without recomputing, and the booking stores `quote_id` and the quoted total. After expiry, the client fetches a fresh quote and shows the new price before payment. This is a product decision; the system makes it enforceable by never computing the charged amount from mutable calendar prices at payment time.

**Q4. Search for Paris in August is slow. What do you do?**

Measure where the time goes. Usually the viewport matches too many candidates (50k+), so pricing and ranking blow the budget. Options: tighten the S2 covering to the visible map; pre-filter with a cheap prior (rating, conversion rate) and stop scanning after enough good candidates; cache result pages for popular `(place, date range, guests)` tuples for 30-60 s; and add replicas for the hot season. Do not geo-shard Paris onto its own nodes: that concentrates the hotspot instead of spreading it.

**Q5. How do you handle time zones for nights?**

A night is a local calendar date of the listing, stored as `DATE` with the listing's IANA time zone on the listing row. Check-in and checkout are dates, not timestamps. Time zones matter only for deadlines: hold expiry and review windows use UTC timestamps; "free cancellation until 48 h before check-in" is computed from check-in time in the listing's zone. Mixing the guest's zone into night arithmetic produces off-by-one-night bugs around midnight.

#### Level signals

- **Mid:** listings DB plus a search engine with geo filtering; a reservations table; basic overlap check.
- **Senior:** per-listing availability bitmaps sized with numbers; CDC-fed search index with stated staleness; conditional per-night update in one shard; instant book versus request-to-book state machines; idempotent payment flow.
- **Staff:** separates the read model from the authoritative calendar and measures freshness; weighs exclusion constraints against per-night rows (immutable predicates, expiry); designs the money flow as a ledger with delayed payout and clawback; admits the iCal double-booking window and how to shrink it.

See also: [HLD 4.8 Geospatial Indexing](../computer-science/High_Level_Design.md#48-geospatial-indexing), [HLD 6.15 Ticket Booking](../computer-science/High_Level_Design.md#615-ticket-booking-seat-reservation), [HLD 6.7 Payment Processing](../computer-science/High_Level_Design.md#67-payment-processing), [HLD 5.10 Transactions Applied to Designs](../computer-science/High_Level_Design.md#510-transactions-applied-to-designs)

---

### A13. Flash Sale Checkout

#### Requirements and assumptions

- **Functional:** at noon a sale opens for one SKU (or a few sizes) with **10,000 units**, limit one per account. Users wait in a waiting room, get admitted, click buy, receive a reservation, and have 10 minutes to pay. Unpaid reservations return their units to the pool. Everyone else sees "sold out" quickly.
- **Never oversell.** Briefly underselling (a unit stuck in an abandoned reservation for a few minutes) is acceptable.
- **Load:** about **1M users** arrive within about 10 s of the start, many refreshing repeatedly.
- **Latency:** the buy click answers in under 200 ms (win or lose); the product page loads from the edge.
- **Isolation:** the regular store must not degrade during the sale.
- **Fairness and abuse:** randomized order for users present before the start, first come after that; bots and resellers are actively fought.
- **Out of scope:** the payment provider internals (see [6.7 Payment Processing](../computer-science/High_Level_Design.md#67-payment-processing)) and fulfillment.

#### Capacity estimate

```text
Supply:         10,000 units, limit 1 per account
Demand:         1M users within ~10 s of noon -> ~100k arrivals/s at the edge
Page loads:     ~5 refreshes per user in the first minute -> 5M loads, peaking ~500k req/s
                -> static page from the CDN + a stock badge object cached for 1 s
Buy attempts:   without admission control, 1M clicks within ~5 s = 200k attempts/s
DB hot row:     one counter row under row locks: ~2-5k updates/s (the 6.15 figure)
                -> 40-100x short of 200k/s; 20 sub-counter rows still fall short
Redis:          one shard does ~100k+ simple ops/s, a short Lua script ~50-100k/s
                -> one key is borderline at 200k/s; 16 bucket keys over 8 shards gives headroom
With a waiting room admitting 20k users/s (~70% click buy):
                ~14k attempts/s -> easy for the Redis gate
                sellout ≈ 10k ÷ 14k/s ≈ 1 s after admission starts
Winners:        10k reservations -> 10k order rows in the first seconds
                burst of ~10k/s for ~1 s -> queue it; the DB drains 2-5k/s in a few seconds
Losers:         ~990k users need a cheap "sold out": answer from local memory or the CDN
Payment:        10k authorizations spread over ~10 min; burst of a few thousand concurrent
                provider calls in the first minute (async I/O, per-provider pools)
Returns:        ~10-20% of reservations expire unpaid -> 1-2k units recycled after 10 min
```

**What the numbers decide:** the durable work is tiny (10k orders); the problem is **rejecting a million people cheaply and correctly**. A database row cannot gate 200k decrements per second, so the gate is an atomic counter in memory (Redis), sharded into buckets, behind a waiting room that meters arrivals. The database stays the source of truth for the 10k winners, writes to it are asynchronous through a queue, and after sellout no request should reach Redis at all.

#### Interfaces and data

```text
GET  /sale/{sale_id}                   -> static HTML from the CDN
GET  /sale/{sale_id}/status            -> { state: UPCOMING|LIVE|SOLD_OUT, approx_remaining }  (max-age=1)
POST /v1/waiting-room/{sale_id}/join   -> { ticket, position_estimate }          (bot checks here)
GET  /v1/waiting-room/{sale_id}/poll   -> { admitted: false, eta_s } | { admission_token }
POST /v1/sales/{sale_id}/reservations  Admission-Token: ...   Idempotency-Key: ...
     { sku, qty: 1 } -> 201 { reservation_id, expires_at } | 409 SOLD_OUT | 409 LIMIT_REACHED
GET  /v1/reservations/{id}             -> { state: RESERVED | CONFIRMING | REJECTED | PAID | EXPIRED }
POST /v1/reservations/{id}/checkout    { payment_method_token, address_id, idempotency_key }
     -> 202 { order_id, state: PAYMENT_PENDING }

Redis (gate, per sale; hash tags keep a bucket's keys on one shard):
  inv:{s42:b7}     integer units left in bucket 7 (16 buckets × 625 units)
  res:{s42:b7}     hash reservation_id -> user_id for units taken from bucket 7
  soldout:{s42}    flag, also pushed to every API server's memory and to the status object

DB (source of truth):
  sale_bucket(sale_id, bucket, total, allocated, PRIMARY KEY (sale_id, bucket))
  reservation(reservation_id PK, sale_id, user_id, bucket,
              state RESERVED|CONFIRMING|PAID|EXPIRED|REJECTED|CANCELLED, expires_at,
              UNIQUE (sale_id, user_id))                        -- durable per-account limit
  orders(order_id PK, reservation_id UNIQUE, user_id, amount_cents, payment_id, state)
```

The `reservation_id` is deterministic, for example `hash(sale_id, user_id)`, so a retried click produces the same ID at every layer. Inventory rows are keyed by `(sale_id, bucket)`; orders and reservations are sharded by `user_id` for the normal store, with the sale's reservations on a dedicated, pre-scaled shard during the event so the sale cannot starve regular checkout.

#### Architecture and flow

```text
Users --> CDN: product page (static), status object (1 s TTL), waiting-room page
      --> Waiting room service (6.15): positions, bot checks, signed admission tokens at a set rate
      --> API gateway (verify token; per-account, per-IP limits; local SOLD_OUT flag)
             |
             v
      Reservation API --1--> Redis gate: Lua decrement on bucket b (16 buckets, 8 shards)
             |                    | won
             |                    v
             +--2--> Reservation queue (partitioned by user_id)
                                  |
                                  v
                     Order writer: INSERT reservation (UNIQUE sale,user)
                                   + conditional UPDATE sale_bucket allocated < total
                                  |
      Checkout API --3--> Payment service (idempotency key = reservation_id) --4--> RESERVED -> PAID
                                  |
      Expiry sweeper --5--> RESERVED -> EXPIRED, allocated - 1, Lua return unit to bucket
      Status ticker --> sums buckets every second --> status object at CDN, SOLD_OUT broadcast
```

1. An admitted user clicks buy. The API checks the token and the local sold-out flag, computes `reservation_id`, picks a starting bucket from it, and runs the Lua gate. If the bucket is empty it probes the next bucket, up to all 16; if every bucket is empty the sale is sold out.
2. On a win, the API enqueues the reservation and returns 201 at once. The order writer inserts the reservation and increments `allocated` conditionally; that write is authoritative.
3. The checkout page polls the reservation state (normally `RESERVED` within 100 ms), then the user pays. The payment service authorizes with `reservation_id` as idempotency key.
4. On a successful payment, `RESERVED -> PAID` runs conditioned on `expires_at >= now()`, and the order is created in the same transaction.
5. Unpaid reservations expire; the sweeper returns their units to the database and to Redis exactly once.

#### Deep dive: the inventory gate without overselling

**Why not the database alone.** `UPDATE ... SET allocated = allocated + 1 WHERE allocated < total` is correct, but every buyer contends on one row lock: a few thousand per second at best. Splitting into sub-counter rows ([6.15, general admission](../computer-science/High_Level_Design.md#615-ticket-booking-seat-reservation)) multiplies that by the bucket count, still short of 200k/s, and every loser still costs a database round trip.

**The Redis gate.** Each bucket's check-and-decrement is one Lua script. Redis runs a script atomically on its single command thread, so no other command interleaves between the read and the decrement:

```lua
-- KEYS[1] = inv:{s42:b7}   KEYS[2] = res:{s42:b7}   ARGV[1] = reservation_id   ARGV[2] = user_id
if redis.call('HEXISTS', KEYS[2], ARGV[1]) == 1 then return 1 end   -- retry: already won here
local left = tonumber(redis.call('GET', KEYS[1]) or '0')
if left <= 0 then return 0 end                                       -- bucket empty: probe the next
redis.call('DECR', KEYS[1])
redis.call('HSET', KEYS[2], ARGV[1], ARGV[2])
return 1
```

The hash makes a retried click idempotent within a bucket, and the deterministic probe order makes retries land in the same bucket. Sixteen buckets of 625 units on 8 shards spread the load; near sellout, requests probe several empty buckets, which is cheap. When all buckets are empty, the API sets `soldout:{s42}` and broadcasts it, and every API server keeps the flag in memory, so the remaining ~990k requests are rejected in microseconds without touching Redis.

**Why the database must still decide.** Redis replicates asynchronously. If a shard's primary fails, the promoted replica may have missed the last few milliseconds of decrements, so the gate briefly believes more units remain than were actually handed out. The order writer's conditional `allocated < total` on `sale_bucket` is the hard guarantee: an extra winner from Redis is rejected there (`REJECTED`, the user sees "sorry, sold out"), never oversold. Two further protections:

- After a Redis failover, pause the sale for a few seconds and **reload** each bucket from the database (`total - allocated`, minus in-flight queue entries) before reopening.
- `WAIT 1 5` after the script (wait for one replica acknowledgment, up to 5 ms) shrinks the loss window at the cost of a millisecond per winner. Only winners pay it, so it is cheap.

The per-account limit is enforced durably by `UNIQUE (sale_id, user_id)` in the database; a duplicate that slipped through the gate (for example, a retry that probed a refilled bucket) fails the insert, and the writer returns that unit to Redis.

**Reconciliation.** A job compares, per bucket, Redis `res` entries with database reservations. A Redis entry with no database row older than a minute (the API crashed after the gate but before enqueueing) gets its unit returned. The invariant to monitor: `units_in_redis + allocated_in_db = total` per bucket, within the in-flight queue depth.

#### Deep dive: admission, async orders, and expiry

**Admission control.** Reuse the waiting room from [6.15 Ticket Booking](../computer-science/High_Level_Design.md#615-ticket-booking-seat-reservation): randomized positions for everyone present before noon, signed admission tokens bound to account and device with a 2-minute expiry, and an admission rate that the downstream can sustain. Two differences for a flash sale: the admission rate can be **high** (20k/s rather than 500/s) because losing is a microsecond flag check, and the waiting room should switch to "sold out" (or "join the waitlist for returned units") the moment the flag flips, so a million browsers stop polling.

**Async order creation.** The 201 response means "you have a reservation", backed by the Redis gate; the durable row follows through a queue within about 100 ms. The queue turns a 10k/s burst into a steady drain the database can handle, and a consumer crash is harmless because the insert is idempotent on `reservation_id`. The checkout endpoint refuses to charge until the durable row exists, so no one pays for a reservation the database later rejects.

**Payment timeouts and returned units.** Reservations last 10 minutes; when checkout starts, the state moves to `CONFIRMING` with a 5-minute extension so a slow payment does not race the expiry (the same fix as 6.15). The sweeper runs:

```sql
UPDATE reservation SET state = 'EXPIRED'
 WHERE state IN ('RESERVED', 'CONFIRMING') AND expires_at < now()
RETURNING reservation_id, bucket;
-- same transaction: UPDATE sale_bucket SET allocated = allocated - 1 WHERE ...; INSERT INTO outbox ...
```

Only the transaction that flips the reservation to `EXPIRED` returns the unit, so a unit is returned once. The outbox consumer returns it to Redis with a script that does `HDEL res rid` and increments `inv` only if the `HDEL` removed an entry, so a redelivered event does nothing. If a payment succeeds after expiry, the conditional `RESERVED|CONFIRMING -> PAID` fails and the authorization is voided. Returned units clear the sold-out flag and are offered to the waitlist in order.

**Contrast with ticket booking.**

| Aspect | Flash sale (fungible units) | Ticket booking (specific seats) |
|---|---|---|
| Inventory model | A counter; any unit satisfies any buyer | Rows per seat; the buyer wants particular seats |
| Spreading contention | Shard the counter into buckets freely | Cannot split a multi-seat hold across partitions |
| Hot path | Redis Lua decrement, DB for winners only | Conditional update on seat rows in one event partition |
| Contention pattern | Everyone wants "one unit": pure counter race | Everyone wants the same good seats: "best available" helps |
| Seat map | None; a single approximate stock badge | Section-level availability cache |
| Shared pieces | Waiting room, holds with expiry, idempotency keys, bot defense | Same |

**Bot defense.** Most sold units go to bots unless the design resists them. Gate at the waiting room (proof-of-work or a challenge, device attestation, account age and purchase history), bind admission tokens to account and device, enforce one per account in the database, then check after the fact: cancel orders sharing a card fingerprint, shipping address, or device cluster, and release those units to the waitlist. Rate limits per IP and per account at the edge stop the crudest scripts before they reach anything expensive.

**Product page.** The page is static and served by the CDN. The stock badge is a tiny JSON object rewritten once per second by the status ticker and cached at the edge with `max-age=1`, so 500k page loads per second become about one origin request per second per CDN node. Never compute stock per request; that turns a hot product into a hot key (see [4.13 Cache Stampede and Hot Keys](../computer-science/High_Level_Design.md#413-cache-stampede-and-hot-keys)).

#### Failure modes and mitigations

| Failure | Impact | Mitigation |
|---|---|---|
| Redis primary fails mid-sale | Lost decrements: gate may admit extra winners | DB conditional write rejects extras; pause, reload buckets from DB, reopen; `WAIT` narrows the window |
| API crashes after the gate, before enqueue | Unit stuck in Redis with no order | Reconciliation returns units with no DB row after a minute |
| Order queue backs up | Winners wait to pay | Checkout polls state; autoscale writers; alert on queue age; the queue is bounded by 10k winners |
| Payment provider slow | Reservations expire mid-payment | `CONFIRMING` state with extended deadline; void authorization if confirm fails |
| Bot swarm at the waiting room | Real users crowded out | Challenges, token binding, per-account limits, post-hoc cancellation |
| Sold-out flag not propagated | Load keeps hitting Redis after sellout | Flag in API memory via pub/sub plus a short TTL check; CDN status object shows SOLD_OUT |
| Sale traffic spills into the regular store | Normal checkout degrades | Separate admission, Redis cluster, queue, and DB shard for the sale; bulkhead the shared gateway |

#### Tradeoffs

| Decision | Chosen | Alternative | Why |
|---|---|---|---|
| Inventory gate | Redis Lua on 16 buckets | DB conditional update only | DB row locks top out at a few thousand/s; losers should not touch the DB |
| Source of truth | DB with conditional `allocated < total` | Redis alone | Async replication can lose decrements; DB guarantees no oversell |
| Order creation | Async via queue after the gate | Synchronous DB write per click | Smooths the winners' burst; response time stays low |
| Admission | Waiting room at a high rate | No queue, or a slow queue | Bounds load and blocks bots, while fast rejection lets admission be generous |
| Returned units | Return on expiry to waitlist | Never return (accept undersell) | 10-20% of units would go unsold otherwise |
| Fairness | Random among early arrivals, FIFO after | Pure FIFO | Refreshing early or scripting earns nothing |

**Main interview tradeoff:** **speed of the gate versus durability of the decision.** An in-memory counter answers a million users in milliseconds but can forget decrements on failover; a database is durable but serializes on one row. The design uses both for what they are good at: Redis decides quickly who is probably a winner, the database decides who actually is, and the only user-visible cost of a disagreement is a rare "sorry" after a reservation, never an oversold unit.

#### Follow-ups with model answers

**Q1. Why not use `DECR` and check for a negative result instead of Lua?**

That works: `DECR` is atomic, and a result below zero means you lost, so you `INCR` it back. The downside is that the counter dips negative under load, so any reader (the status ticker, a reconciliation job) sees nonsense mid-flight, and the compensating `INCR` is a second command that can be lost if the API crashes. The Lua version never goes below zero and records the winner in the same atomic step, which also makes retries idempotent. Both are correct as a gate as long as the database remains the final authority.

**Q2. The business wants no waiting room: "just let everyone in". What breaks?**

The gate survives: 200k attempts/s over 16 buckets on 8 shards is about 25k/s per shard, within budget. What breaks first is everything around it: 500k page loads/s if the page is not fully static, TLS handshake rates at the load balancers, and bots, which now compete directly with humans. Without a waiting room, fairness is whoever has the lowest latency to the data center. Keep at least a thin admission layer (token issuance with bot checks) even if it admits everyone immediately.

**Q3. How do you show "only 12 left!" accurately?**

You cannot cheaply, and you should not try. Sum the buckets once per second and publish an approximate number with a 1 s cache. Near zero, show "almost gone" rather than a precise count, because the number shown is stale by the time the user reads it and returned units can make it go up again. Exact numbers only create support tickets ("it said 3 left").

**Q4. Multiple sizes, each with its own stock. Does the design change?**

Each `(sale, sku)` gets its own buckets, sized to its stock (a size with 200 units may need only 2 buckets). The per-account limit is now across SKUs if the rule is "one pair per person", which stays on the `UNIQUE (sale_id, user_id)` constraint in the database. Popular sizes sell out separately, so the sold-out flag is per SKU, and the waiting room may admit users who can still buy the remaining sizes.

**Q5. How would you test this before noon?**

A load test against a staging copy with the production topology, replaying the expected arrival curve (1M users in 10 s) from distributed load generators, including bot-like clients. Inject failures during the test: kill a Redis primary, a queue consumer, and an API server mid-sale, and assert the invariant `sold + available + in_flight = total` and no duplicate accounts. Also run a game-day "dark launch" of a cheap product a week earlier, which exercises the real CDN, waiting room, and payment provider limits.

#### Level signals

- **Mid:** recognizes the oversell race; uses a conditional update or atomic decrement; caches the product page.
- **Senior:** quantifies why one DB row fails; Redis Lua gate with buckets plus DB conditional write as the authority; async order creation; reservation expiry that returns units exactly once; links the waiting room instead of re-deriving it.
- **Staff:** reasons about Redis failover losing decrements and how to detect and reconcile; isolates the sale from the regular store; designs fairness and bot defense as policy; plans load and failure testing; contrasts fungible counters with seat inventory.

See also: [HLD 6.15 Ticket Booking](../computer-science/High_Level_Design.md#615-ticket-booking-seat-reservation), [HLD 4.13 Cache Stampede and Hot Keys](../computer-science/High_Level_Design.md#413-cache-stampede-and-hot-keys), [HLD 5.8 Backpressure and Load Shedding](../computer-science/High_Level_Design.md#58-backpressure-and-load-shedding), [HLD 6.7 Payment Processing](../computer-science/High_Level_Design.md#67-payment-processing)

---

### A14. Maps and Navigation

#### Requirements and assumptions

- **Functional:** pan and zoom a world map; search for places and addresses (geocoding) and resolve a position to an address (reverse geocoding); get driving routes with alternatives and an ETA that reflects live traffic; turn-by-turn navigation with automatic rerouting and ETA updates; offline maps for a region.
- **Scale:** ~1B MAU, ~500M map sessions/day, ~10M concurrent navigation sessions at peak.
- **Latency:** visible tiles within ~200 ms (from the CDN); route response p99 under 500 ms including alternatives; reroute under 1 s.
- **Freshness:** live traffic reflected in routes and ETAs within 1-2 minutes; map data edits (new roads, closures) live within hours, urgent closures within minutes.
- **Quality:** ETA within ±10% of the actual trip time for most trips.
- **Privacy:** location probes anonymized; no raw trips retained beyond aggregation.
- **Out of scope:** transit routing (a timetable graph), Street View imagery, map-data editing tools.

#### Capacity estimate

```text
Tiles:          vector tiles z0-z14 (clients overzoom past 14); tiles at zoom z = 4^z
                z14: 4^14 ≈ 268M tiles; z0..z14 ≈ 4/3 × 268M ≈ 358M
                ~70% are ocean or empty -> ~110M real tiles (empty ones share one object)
                × ~20 KB average (dense city tiles 100+ KB) ≈ 2.2 TB per map version
Tile traffic:   500M sessions × ~60 tiles ≈ 30B tiles/day ≈ 350k/s avg -> ~1M/s peak
                1M/s × 20 KB ≈ 20 GB/s ≈ 160 Gb/s at peak, from the CDN
                98% hit ratio (city tiles are Zipfian) -> ~20k/s to the tile origin
Road graph:     world routable graph ≈ 300M nodes, 700M directed edges (degree-2 shape
                points folded into edge geometry)
                300M × 16 B + 700M × 16 B ≈ 16 GB; overlay/shortcuts roughly double it -> ~30-40 GB
                -> fits in RAM; partition by continent anyway (a continent is a few to ~10 GB)
Route QPS:      ~1B route requests/day ≈ 12k/s avg -> ~40k/s peak, × ~3 alternatives
Dijkstra:       on a ~20M-node continental graph a long query settles most of the graph: ~1-3 s
                40k/s × 2 s = 80k cores -> not viable
Speedup:        CRP query ~1-5 ms: 40k × 3 × 5 ms ≈ 600 cores; contraction hierarchies < 1 ms
Probes:         10M navigating devices × 1 point / 5 s = 2M GPS points/s × ~50 B ≈ 100 MB/s
Map matching:   HMM/Viterbi ~50 µs per point -> 100 core-seconds/s ≈ 100-300 cores
Live speeds:    ~5M edges change speed meaningfully per minute × 8 B ≈ 40 MB/min of deltas
History:        15-min time-of-week slots = 672 per edge; 700M × 672 × 1 B ≈ 470 GB raw
                -> cluster into ~1,000 shared speed profiles; per edge: profile id + free-flow
                speed ≈ 4 B × 700M ≈ 2.8 GB
Reroute checks: 10M sessions re-evaluated every 2 min ≈ 83k cheap ETA re-sums/s
                ~5% need a full route query ≈ 4k/s extra
```

**What the numbers decide:** tiles are pre-generated static content (2 TB per version) and the problem is CDN egress, not computation. The road graph fits in memory, so each routing server holds a full continental graph and no query crosses machines; the constraint is **query time**, which forces a preprocessing-based speedup. Traffic changes edge weights every minute, so the speedup must allow cheap weight updates without hours of re-preprocessing, which selects customizable route planning (CRP) or customizable contraction hierarchies. Probe ingest is moderate in bytes but CPU-bound and per-device stateful (map matching).

#### Interfaces and data

```text
GET  https://tiles.example.com/v{map_version}/{z}/{x}/{y}.mvt
     -> vector tile (immutable; Cache-Control: max-age=31536000)
GET  /v1/geocode?q=...&near=lat,lng           -> [{ place_id, name, lat, lng, score }]
GET  /v1/reverse_geocode?lat=&lng=            -> { address, place_id }
POST /v1/routes { origin, destination, mode: DRIVE, depart_at?, avoid: [TOLLS] }
     -> { routes: [{ route_id, polyline, eta_s, distance_m, steps[], edge_ids (compressed),
                     traffic_spans[] }] }
WS   /v1/nav/{session_id}
     client -> { lat, lng, heading, speed, ts } every 5 s (doubles as a traffic probe)
     server -> { eta_s, better_route?, incident_ahead? }

Per continent, per map version (immutable build artifacts):
  nodes(node_id, lat, lng)
  edges(edge_id, from, to, length_m, road_class, speed_limit, access_flags, geometry)
  turns(from_edge, to_edge, cost_s | forbidden)
  partition(level, cell_id, boundary_nodes[])           -- metric independent
  overlay(level, cell_id, metric_version, clique[])      -- rebuilt by customization
Traffic:
  edge_speed_live(edge_id, window_end, speed_kph, samples, confidence)   -- keyed by edge_id
  edge_profile(edge_id, profile_id, free_flow_kph)                         -- historical
Places index: (place_id, name tokens, category, s2_cell, popularity)       -- sharded by region
```

The graph is partitioned **by continent** and replicated: every routing server in a region holds the whole continental graph and overlay in memory, so a query never leaves one process. Map matching is keyed by device (a trace must be matched in order), and speed aggregation is keyed by `edge_id`. Tiles are keyed by `(version, z, x, y)` in object storage. Places are sharded by region with a global index for well-known landmarks searched from far away.

#### Architecture and flow

```text
Map data pipeline (vendor + OSM-style sources + edits)
   |--> Tile builder (batch, per version) --> Object storage --> Tile origin --> CDN --> clients
   |--> Graph builder: partition + metric-independent preprocessing --> graph artifact per continent
   |--> Places/geocoder index builder --> Places service

Clients --route--> Route API --> Routing servers (per continent; graph + overlay in RAM)
                        |              ^ customization every ~60 s with new edge weights
                        v              |
                    ETA service --> Traffic snapshot (live speeds + historical profiles)
                    (ML correction)            ^
                                               | per-edge speeds every 60 s
Navigating clients --WS--> Nav session service --> Probe log --> Map matcher --> Speed aggregator
(position every 5 s)       (reroute checks)        (by region)   (keyed by       (keyed by edge_id,
                                                                  device)         sliding windows)
```

**Viewing the map:** the client computes which tiles cover the viewport at the current zoom, fetches them from the CDN by versioned URL, and renders vector data with a style locally (labels, colors, dark mode); beyond z14 it overzooms the z14 tiles.

**Getting a route:**

1. Geocode origin and destination; snap each to the nearest road edge (an S2 index over edges, see [4.8 Geospatial Indexing](../computer-science/High_Level_Design.md#48-geospatial-indexing)).
2. The route API sends the query to a routing replica for that continent, which runs the CRP query on the current customized overlay and returns up to three alternatives.
3. The ETA service evaluates each route with time-dependent speeds and the ML correction; the client shows the routes with traffic coloring.

**Navigating:** the client follows the route locally, sends its position every 5 s (which also feeds traffic), and receives ETA updates and better-route offers from the nav session service.

#### Deep dive: tiles

**The pyramid.** At zoom z the world (in Web Mercator) is a 2^z × 2^z grid, so each level has 4× the tiles of the one above. Vector tiles carry geometry and attributes (roads, buildings, labels) in a compact protobuf encoding; the client styles them, so one tile set serves every style, language, and dark mode, and rotation and smooth zoom work. Raster tiles would need a full set per style and per screen density.

**Generation.** Each zoom level includes only what is visible at that scale (motorways at z5, residential streets at z12, buildings at z14), with geometry simplified per level (Douglas-Peucker) so a tile stays under a size budget. A full build is a large batch job over ~110M tiles; incremental builds regenerate only tiles touched by edits: one road edit touches one tile per zoom level, about 15 tiles.

**Serving.** Tile URLs include the map version, so tiles are immutable and cached for a year; a release switches clients to a new version prefix instead of purging the CDN. Most of the ocean is one shared "empty" tile. Urgent changes (a closure) do not wait for a tile release: they arrive as a small dynamic overlay layer with a short TTL, on top of the immutable base tiles. Offline maps are a package of a region's tiles at selected zooms plus a routing-graph extract.

#### Deep dive: routing on a continental road graph

**Why the textbook algorithms fail.** [Dijkstra](../computer-science/DSA_Fundamentals.md#dijkstras-algorithm) settles every node closer than the destination, so a long cross-country query touches most of a ~20M-node graph: seconds of CPU and poor cache behavior. [A*](../computer-science/DSA_Fundamentals.md#a-search-algorithm) with a straight-line heuristic helps little, because with travel-time weights the heuristic must assume the fastest possible road everywhere, which badly underestimates. Landmark heuristics (ALT) gain about an order of magnitude, still not enough at 40k queries/s.

**Contraction hierarchies (CH).** Preprocessing orders nodes by "importance" (residential junctions low, motorway interchanges high) and contracts them one by one: removing node v adds a **shortcut** edge u -> w whenever u -> v -> w was the only shortest path between u and w. A query runs a bidirectional Dijkstra in which both searches only move **upward** in the hierarchy; they meet near the top, typically after settling a few hundred nodes. Shortcuts store their middle node, so the full path is unpacked recursively afterward. The catch: shortcuts encode shortest paths under one set of weights, so any change in traffic weights invalidates them and requires re-contraction (minutes per continent).

**Customizable route planning (CRP)** splits preprocessing into three phases:

1. **Metric-independent partition (hours, per map version):** recursively partition the graph into cells at several levels (for example cells of ~2^8 to ~2^20 nodes) with a balanced partitioner that minimizes boundary edges. Road networks have small natural cuts (rivers, mountains, motorways), so boundaries are small.
2. **Customization (seconds, per metric):** for each cell, compute shortest-path distances between all of its boundary nodes under the current weights, bottom-up across levels. This is the overlay graph. It parallelizes across cells, and after a traffic update only cells containing changed edges need recomputation.
3. **Query (milliseconds):** bidirectional Dijkstra that uses original edges inside the source and target cells and the highest-level overlay cliques everywhere else.

```text
Orders of magnitude for a ~20M-node continental graph (route-planning literature, varies by hardware):
                    Preprocess           Weight update       Query
Dijkstra            none                 free                ~1-3 s
ALT (landmarks)     minutes              recompute lmarks    ~50-100 ms
CH                  minutes              full re-contraction ~0.1-1 ms
CRP                 partition: hours     ~1 s customization  ~1-5 ms
Customizable CH     minutes              ~1 s customization  ~0.5-1 ms
```

**Choice:** CRP (or customizable CH). Both give millisecond queries and a customization step cheap enough to run every minute with live traffic, and per-user metrics (avoid tolls, avoid highways) are just another customization. Turn restrictions and turn costs are handled by modeling turns explicitly (an edge-based graph or turn tables at nodes). **Alternatives** come from "via-node" candidates found in the same search space, filtered so that each alternative is substantially different, locally optimal, and not much longer than the best route.

#### Deep dive: live traffic, ETA, and rerouting

**Map matching.** Raw GPS is noisy (5-20 m, worse in urban canyons). A hidden Markov model treats candidate road edges within ~50 m of each fix as hidden states; emission probability falls with distance from the fix, and transition probability favors pairs whose on-road distance matches the straight-line distance between fixes. Viterbi over a sliding window yields the edge sequence and entry and exit times per edge. This stage is keyed by device so each trace is processed in order.

**Speed aggregation.** Matched traversals (`edge_id, enter_ts, exit_ts`) go to a stream processor keyed by `edge_id` with a 5-minute sliding window by event time and a watermark that drops batches more than ~2 minutes late (a phone that was offline). Use a robust estimate (median or trimmed mean) to discard drivers stopped for coffee, and attach a confidence from the sample count. See [4.11 Stream Processing](../computer-science/High_Level_Design.md#411-stream-processing). Blend with the historical profile for the current time slot: `speed = w × live + (1 - w) × historical` with `w = n / (n + k)` for n samples, so a single probe cannot swing a motorway's speed. Publish only edges with at least k distinct devices (privacy), and only changed edges, as a 60 s snapshot delta to every routing replica, which then runs customization.

**ETA.** Route time = sum over edges of traversal time + turn costs + intersection delays, evaluated **time-dependently**: an edge you reach in 5 minutes uses live speed, an edge you reach in 50 minutes uses mostly the historical profile for that future slot. An ML model trained on completed trips then corrects the residual (features: road-class mix, time of day, weather, events, how much of the route had live coverage, region), and outputs a multiplicative correction. Track accuracy per region as the fraction of trips within ±10% and the mean absolute percentage error; regressions block model rollout.

**Rerouting.** Two triggers:

- **Off route (client-side):** the map-matched position is more than ~30-50 m from the route for two or more fixes. The client requests a new route from its current position with its heading as a constraint (no instant U-turns).
- **Better route (server-side):** the nav session service re-sums the remaining route's ETA every ~2 minutes against the latest snapshot (cheap, about 83k/s), and runs a full route query only when the ETA worsened past a threshold or an incident appeared on the route (about 4k/s). It offers a switch only if it saves more than max(2 minutes, 10%).

**Herding.** If every driver gets the same detour, the side street jams. Mitigations: stagger offers, assign alternatives probabilistically when savings are similar, and feed the predicted load of active navigation sessions into the edge weights for the next minutes.

#### Failure modes and mitigations

| Failure | Impact | Mitigation |
|---|---|---|
| Traffic pipeline stalls | Routes use stale live speeds | Snapshots expire after ~5 minutes and the router falls back to historical profiles; alert on snapshot age |
| Bad map-data release (broken road, wrong turn restriction) | Wrong or impossible routes | Validation suite of known routes per region; canary release by region; keep previous graph and tile version for instant rollback |
| Routing replica out of memory or slow customization | Queries fail or use old weights | Customize into a new overlay buffer and swap atomically; N+1 replicas per continent |
| CDN region outage | Tiles fail to load | Multi-CDN with DNS steering; clients keep a disk cache of recently viewed tiles |
| GPS noise or spoofed probes | False jams on empty roads | Robust aggregation, minimum distinct devices per edge, anomaly detection per device |
| Herding onto one detour | New congestion created by routing | Probabilistic assignment and predicted session load in weights |
| Geocoder returns wrong place | User navigates to the wrong city | Bias by viewport and user location; show disambiguation when scores are close |

#### Tradeoffs

| Decision | Chosen | Alternative | Why |
|---|---|---|---|
| Tile format | Vector tiles, client-styled | Server-rendered raster | One set for all styles and densities; smaller; rotation and smooth zoom |
| Tile freshness | Immutable versioned URLs + dynamic overlay | Per-tile purge on change | No CDN invalidation storms; urgent data still live within minutes |
| Routing algorithm | CRP / customizable CH | Plain CH | Weight updates in seconds, needed for per-minute traffic |
| Graph placement | Full continental graph per replica | Graph partitioned across servers | Fits in RAM; no cross-machine search; scale by replication |
| ETA | Time-dependent evaluation + ML correction | Live speeds only | Live speeds say nothing about the edge you reach in 50 minutes |
| Reroute checks | Cheap ETA re-sum, full query on trigger | Full route query every interval | 20× less routing CPU for 10M sessions |

**Main interview tradeoff:** **preprocessing versus freshness.** The more you precompute about shortest paths, the faster queries get, but the more a weight change invalidates. Plain CH gives the fastest queries but cannot absorb per-minute traffic; CRP and customizable CH split the work so the expensive, metric-independent part runs once per map version and the metric-dependent part runs in seconds. The same theme repeats at the tile layer (immutable base tiles plus a small live overlay) and in ETA (live speeds near-term, historical profiles far-term).

#### Follow-ups with model answers

**Q1. Why not run A* with a good heuristic and skip all this preprocessing?**

A* is only as good as its heuristic, and for travel time the only admissible straight-line heuristic is distance divided by the fastest speed anywhere, which grossly underestimates on most roads, so A* still explores most of the area between the endpoints. Landmark-based heuristics (ALT) are much tighter and give about an order of magnitude, but a continental query still costs tens of milliseconds and degrades when traffic weights diverge from the weights the landmarks were computed with. At 40k queries/s with alternatives, the difference between 50 ms and 2 ms is the difference between thousands of cores and hundreds.

**Q2. A bridge closes due to an accident. How fast do routes avoid it, and how?**

The closure arrives from an incident feed or is inferred when probe speeds on the bridge drop to zero with high confidence. It is set as infinite weight in the next traffic snapshot, and routing replicas customize only the cells containing that edge, within about a minute. Active navigation sessions whose remaining route crosses the bridge get an `incident_ahead` push and a full reroute immediately, rather than waiting for their periodic check. The tile overlay shows the closure on the map without a tile release.

**Q3. How do you make geocoding work for "pizza near me" and for "10 Downing Street"?**

Two paths over one places index. Address queries are parsed into components (house number, street, locality, postcode) and matched against an address index; house numbers missing from the data are interpolated along the street segment's known number range. Category and name queries ("pizza") are a search problem: retrieve candidates by token and S2 proximity to the viewport, then rank by distance, popularity, rating, and open-now status. Both use typeahead with prefix indexes biased to the user's location (see [6.9 Search Autocomplete](../computer-science/High_Level_Design.md#69-search-autocomplete-typeahead)).

**Q4. How do you protect user privacy while collecting 2M GPS points per second?**

Probes carry rotating ephemeral IDs instead of account IDs, which change every trip or every few minutes so traces cannot be stitched together. The first and last few hundred meters of each trip are dropped on the device, so home and work locations never leave it. Aggregation publishes only edges with at least k distinct devices in a window, and raw matched traces are deleted after aggregation, keeping only per-edge statistics. Users can opt out of contributing traffic data while still receiving it.

**Q5. How would you predict ETA for a trip that departs tomorrow at 8 a.m.?**

Live traffic is irrelevant that far ahead, so use the historical profiles for the time-of-week slots the trip will pass through, evaluated time-dependently as the simulated vehicle advances along the route. The ML correction adds known future effects: holidays, scheduled events, weather forecasts. Return a range (for example 35-50 minutes) rather than a point estimate, since uncertainty is much larger than for a trip starting now, and recompute when the user actually starts navigating.

#### Level signals

- **Mid:** tiles on a CDN; Dijkstra or A* on a road graph; GPS updates for traffic; ETA from distance and speed.
- **Senior:** zoom-pyramid tile math with versioned immutable URLs; explains why Dijkstra is too slow and how CH works; streaming per-edge speed aggregation with map matching; time-dependent ETA; client-side off-route detection.
- **Staff:** chooses CRP or customizable CH because of the preprocessing-versus-freshness tension; designs rollback for map releases; anticipates herding and privacy; treats ETA accuracy as a measured product metric with ML correction and per-region monitoring.

See also: [HLD 4.8 Geospatial Indexing](../computer-science/High_Level_Design.md#48-geospatial-indexing), [HLD 4.11 Stream Processing](../computer-science/High_Level_Design.md#411-stream-processing), [HLD 6.6 Ride-Sharing Service](../computer-science/High_Level_Design.md#66-ride-sharing-service), [DSA: Shortest Path Algorithms](../computer-science/DSA_Fundamentals.md#17-shortest-path-algorithms)

---

### A15. Video Conferencing (Zoom)

#### Requirements and assumptions

- **Functional:** schedule and join meetings by link; audio, video, and screen sharing; gallery and active-speaker layouts; mute and roster controls; chat; cloud recording; phone dial-in; webinars where a few panelists present to a large view-only audience.
- **Meeting sizes:** most meetings 2-10 participants; interactive meetings up to 1,000; webinars 50k+ viewers.
- **Scale:** ~10M concurrent participants at peak in ~2M meetings, with join spikes at the top of each hour.
- **Latency:** mouth-to-ear under ~150 ms within a region and under ~300 ms between continents; joining takes under ~3 s.
- **Quality:** degrade gracefully on bad networks: audio first, then lower video resolution or frame rate, never freezing everyone for one participant's bad link.
- **Security:** media always encrypted in transit; optional end-to-end encryption (E2EE) per meeting, with documented feature loss.
- **Out of scope:** calendar integrations, whiteboards, billing.

#### Capacity estimate

```text
Concurrency:    10M concurrent participants in ~2M meetings (median 3-5 people)
Bitrates:       720p ≈ 1.5 Mb/s; 360p ≈ 500 kb/s; 180p ≈ 150 kb/s; Opus audio ≈ 40 kb/s
Mesh, N = 10:   each client sends 9 × 1.5 = 13.5 Mb/s and receives 13.5 Mb/s
                -> exceeds most home uplinks (often 5-20 Mb/s); 9 congestion loops per client
MCU, N = 10:    client 1.5 up / 1.5 down; server decodes 10 streams and encodes a composed
                layout per receiver (or per layout): ~0.5-1 core per 720p encode
                -> ~5-10 cores per meeting, + 50-150 ms of decode/compose/encode latency
SFU, N = 10:    client uploads simulcast once: 1.5 + 0.5 + 0.15 ≈ 2.15 Mb/s
                downloads speaker at 1.5 + 8 thumbnails × 0.15 = 2.7 Mb/s
                server forwards packets, no decoding
SFU node:       25 Gb/s NIC at ~40% target ≈ 10 Gb/s of media
                ~5 Mb/s per active-video participant (in + out) -> ~2,000 participants per node
                5 Mb/s ÷ (8 × 1,200 B packets) ≈ 520 packets/s each -> ~1M packets/s per node
                SRTP decrypt + re-encrypt per packet per receiver -> plan ~10-20 cores
Fleet:          ~50% send video; blended ~1 Mb/s up + ~2 Mb/s down ≈ 3 Mb/s per participant
                10M × 3 Mb/s = 30 Tb/s through media servers ÷ 10 Gb/s ≈ 3,000 SFU nodes (+ N+1)
Join burst:     ~5M joins in the 2 minutes around the hour ≈ 40k joins/s
                × ~5-10 signaling messages (auth, SDP offer/answer, ICE, roster) ≈ 300k msgs/s
TURN:           ~10-15% of participants need relayed media (UDP blocked, strict NAT)
                1.5M × 3 Mb/s ≈ 4.5 Tb/s through relays -> a real fleet, colocated with SFUs
Latency budget: capture + encode 30 ms, uplink 20 ms, SFU 2 ms, backbone 0-100 ms,
                downlink 20 ms, jitter buffer 30-80 ms, decode + render 20 ms
                ≈ 120 ms in-region, ≈ 250 ms intercontinental
Recording:      5% of meetings recorded: 100k × ~1 Mb/s composite ≈ 100 Gb/s, ~450 MB per hour each
Webinar:        50k viewers × 1.5 Mb/s = 75 Gb/s from one presenter: a CDN job, not an SFU job
```

**What the numbers decide:** mesh is limited by client uplinks past 3-4 people, and an MCU costs cores per meeting plus latency, so the **SFU** is the default: clients upload once, the server forwards without decoding, and each receiver gets layers sized to its own bandwidth. The fleet is sized by **bandwidth and packet rate** (30 Tb/s, ~1M packets/s per node), not storage or QPS. The latency budget leaves no room for TCP retransmission stalls or deep buffers, so media runs over UDP, with relays only as a fallback. Webinars at 50k+ are a streaming problem and leave the SFU path.

#### Interfaces and data

```text
POST /v1/meetings { topic, start_at, settings: { e2ee, recording, waiting_room } }
     -> { meeting_id, join_url, passcode }
POST /v1/meetings/{id}/join { display_name, auth_token }
     -> { participant_id, signaling_url, media_endpoints[{ region, sfu_addr }],
          ice_servers[{ urls: [stun:, turn:], username, credential (short-lived) }] }
WSS  signaling (per participant):
     offer/answer SDP, trickle ICE candidates, ice_restart,
     subscribe { publisher_id, track, max_width, max_fps }, active_speaker, roster, mute, layout
Media: SRTP/SRTCP over UDP (keys from DTLS-SRTP); fallback TURN over TCP or TLS on 443
     RTCP: transport-wide congestion feedback, NACK, PLI/FIR (keyframe requests), receiver reports

meeting(meeting_id PK, host_id, settings, passcode_hash, created_at)
meeting_session(meeting_id, session_id, started_at, controller_id, lease_expires_at,
                sfus[{ region, sfu_id }])                 -- strongly consistent KV, leased owner
participant(session_id, participant_id, user_id, role HOST|PANELIST|ATTENDEE,
            sfu_id, joined_at, left_at)
recording(recording_id, session_id, mode COMPOSITE|PER_TRACK, object_keys[], state)
```

Each live meeting has exactly one **meeting controller** (an in-memory owner chosen by a lease on `meeting_session`), which holds the roster, the SFU assignment, and the layer policy. Partitioning by `meeting_id` keeps all control for a meeting in one place; media is partitioned by meeting and region onto SFU nodes, and a large or global meeting spans several SFUs.

#### Architecture and flow

```text
Client --HTTPS--> Meeting API (auth, passcode, waiting room) --> Meeting DB
   |
   +--WSS--> Signaling edge --> Meeting controller (one per live meeting; roster, layer policy)
   |                                     |
   |                                     v
   |                              SFU allocator (region by RTT probe; load, packet rate per node)
   |
   +==UDP SRTP==> SFU (region A) <==== cascade over private backbone ====> SFU (region B) <==UDP==> clients in B
   |                 |   |   \
   |                 |   |    +--> Recorder (joins as hidden subscriber) --> Object storage
   |                 |   +-------> Streaming bridge (compose -> RTMP/SRT) --> live pipeline (6.5) --> CDN (LL-HLS)
   |                 +-----------> PSTN gateway (SIP <-> RTP, mixed audio for phone users)
   |
   +==TCP/TLS 443==> TURN relay (when UDP is blocked) ==> SFU
```

**Joining:**

1. The client calls the meeting API, which checks auth, passcode, and the waiting room, and returns a signaling URL, candidate media endpoints, and short-lived TURN credentials.
2. The client measures RTT to a few candidate regions; the controller assigns an SFU in the best region for this participant (creating a cascade link if the meeting already lives elsewhere).
3. Over signaling, the client and SFU exchange SDP: codecs, simulcast layers, header extensions. The SFU has a public IP and runs ICE-lite; the client's connectivity checks reach it directly, or through TURN when UDP is blocked.
4. DTLS completes, SRTP keys are derived, and the client publishes its audio and video and subscribes to the tracks its layout needs.

**During the meeting:** the SFU forwards packets to subscribers, choosing per subscriber which simulcast or SVC layer to send, and terminates RTCP feedback per hop (NACKs, bandwidth estimates, keyframe requests).

#### Deep dive: media topology, simulcast, and layer selection

| Topology | Client uplink | Client downlink | Server cost | Latency | Use |
|---|---|---|---|---|---|
| **Mesh (P2P)** | (N - 1) × stream | (N - 1) × stream | none | lowest | 1:1 calls, maybe 3 people |
| **MCU (mix)** | 1 stream | 1 composed stream | decode N + compose + encode: cores per meeting | +50-150 ms | Legacy room systems, phone dial-in audio mixing, weak clients |
| **SFU (forward)** | 1 stream (+ simulcast layers) | chosen layers per publisher | forward packets; SRTP re-encrypt | +1-5 ms | Default for everything interactive |

**Simulcast** has each publisher encode the same video at 2-3 resolutions (for example 720p, 360p, 180p), each as a separate RTP stream. **SVC** (scalable video coding, VP9 or AV1 with spatial and temporal layers) encodes one stream whose packets can be dropped to yield lower resolutions or frame rates. With SVC the SFU can step down at any packet boundary; with simulcast, switching to another stream requires a keyframe on that stream.

**Per-subscriber layer selection.** For each subscriber the SFU knows (a) its estimated downlink bandwidth, from transport-wide congestion feedback, and (b) the size at which it renders each publisher, which the client sends ("I show Alice at 1280×720, Bob at 320×180"). Each allocation round (every few hundred milliseconds), it fills the budget greedily in priority order:

```text
1. audio for the 3 loudest speakers (always)
2. screen share at the layer that fits
3. active speaker at the layer matching its rendered size
4. thumbnails at the lowest layer, most recently active first
5. leftover budget: upgrade one layer at a time, but only after a bandwidth probe succeeds
```

Then the SFU rewrites RTP sequence numbers and timestamps on the selected layer so the receiver sees one continuous stream across switches. On an upswitch with simulcast it sends a PLI (picture loss indication) to the publisher for a keyframe, rate-limited to one per publisher per ~500 ms, because one keyframe request per subscriber would flood the publisher with expensive keyframes. If nobody subscribes to a publisher's 720p layer, the SFU tells the publisher to stop encoding it, which saves the publisher's uplink and CPU.

**Audio in large meetings.** Forwarding 1,000 audio streams to everyone is 1,000 × 40 kb/s = 40 Mb/s per receiver. The SFU reads the audio-level RTP header extension (no decoding) and forwards only the top ~3 speakers, which is also what makes active-speaker detection cheap.

#### Deep dive: signaling, NAT traversal, and real-time transport

**Signaling** is a small control channel (WSS) for SDP offer/answer, trickle ICE candidates, subscriptions, and roster. It must absorb the top-of-hour burst (~300k messages/s), so it is stateless at the edge and routes by `meeting_id` to the meeting controller.

**NAT traversal.** Most clients sit behind NAT ([NAT](../computer-science/CS_Fundamentals.md#nat-network-address-translation)). ICE gathers candidates: host addresses, server-reflexive addresses learned from a **STUN** server (the public address the NAT maps to), and relay addresses on a **TURN** server. Peer-to-peer calls need hole punching between two NATs, which fails for symmetric NATs. Connecting to an SFU with a public IP is much simpler: the client's outbound packets create the NAT mapping, so direct UDP works for most clients. The fallback ladder is UDP direct, then TURN over UDP, then TURN over TCP, then TURN over TLS on port 443, which looks like HTTPS to corporate firewalls.

**Why UDP.** Media is useless when late. Over TCP, one lost packet stalls everything behind it until the retransmission arrives (head-of-line blocking, see [TCP vs UDP](../computer-science/CS_Fundamentals.md#22-tcp-vs-udp)), and TCP's congestion response halves the rate on loss. RTP over UDP lets the application decide per packet: retransmit, conceal, or skip. TCP fallback works, but quality on lossy links is visibly worse.

**Congestion control.** The sender runs delay-based congestion control (Google Congestion Control: rising one-way delay signals a filling queue before loss happens) driven by transport-wide feedback from the SFU, and adjusts the encoder's target bitrate, resolution, and frame rate. Unlike [TCP congestion control](../computer-science/CS_Fundamentals.md#tcp-congestion-control), the target is low queueing delay, not maximum throughput. Each SFU hop runs its own estimate per subscriber, so one participant on a weak link gets lower layers without affecting anyone else.

**Loss recovery.**

- **NACK and retransmission:** the receiver asks for missing sequence numbers; worthwhile when the RTT is well below the jitter-buffer depth. The SFU keeps about 1 s of recent packets per stream and answers NACKs from the nearest hop, so a loss on the last mile is repaired from the SFU, not from the publisher across the ocean.
- **FEC:** forward error correction packets (FlexFEC for video; Opus in-band FEC and redundant encoding for audio) add 10-50% overhead sized from the measured loss rate, and recover without waiting a round trip. Preferred on long-RTT or high-loss links.
- **Keyframe request:** when a frame cannot be recovered, the receiver sends PLI; the SFU coalesces requests so a lossy subscriber does not trigger a keyframe storm for everyone.
- **Jitter buffer:** an adaptive buffer that grows with measured jitter (30-80 ms typically) and shrinks when the network calms; audio uses packet-loss concealment and time-stretching to hide small gaps. Audio always gets priority over video.

#### Deep dive: placement, cascading, and large meetings

**Placement.** Each participant connects to an SFU in the region with the lowest measured RTT. A meeting whose participants are all in one region lives on one SFU node; when it outgrows a node (packet rate, not just bandwidth), the controller adds a second node in the same region and cascades them.

**Cascading across regions.** A meeting with 40 people in the US, 40 in Europe, and 20 in Asia runs on three SFUs, one per region, linked over the private backbone. Each SFU forwards a local publisher's stream to a remote SFU **once**, only if someone there subscribes, and the remote SFU fans it out locally. Without cascading, 60 remote participants would each pull streams across oceans over the public internet; with it, each subscribed stream crosses each ocean once, and loss is repaired per hop. Cascade links carry the highest layer any remote subscriber needs.

**Webinars.** Up to about 1,000 interactive participants, a cascaded SFU tree works. For 50k+ view-only attendees, forwarding individual streams is wasteful because they all watch the same thing. A streaming bridge subscribes to the panelists like a participant, composes the program view once, and pushes it over RTMP or SRT into the live-streaming pipeline: ABR transcode, LL-HLS segments, CDN ([6.5 Video Streaming Platform](../computer-science/High_Level_Design.md#65-video-streaming-platform)). Viewers get 2-5 s latency instead of 200 ms, which is fine for watching. Q&A goes over the chat channel, and promoting an attendee to panelist moves them from the HLS player to an SFU connection.

**Recording.** A recorder joins as a hidden subscriber. **Composite mode** decodes, lays out, and encodes one MP4 in real time (MCU-like CPU cost, simple output). **Per-track mode** writes each participant's RTP stream to object storage as-is and composes later in a batch job. That is cheaper during the top-of-hour peak, flexible (re-layout, transcription per speaker), and slower to deliver.

#### Failure modes and mitigations

| Failure | Impact | Mitigation |
|---|---|---|
| SFU node crashes | Its participants lose media | Clients detect no RTP/RTCP for ~2 s; controller assigns a new SFU; ICE restart; ~3-5 s glitch; roster survives in the controller |
| Meeting controller dies | No roster changes or new joins for that meeting | Lease expires; a new controller rebuilds state from `meeting_session` and SFU reports; media keeps flowing meanwhile |
| Participant on lossy Wi-Fi | Their video freezes for others | Their uplink estimate drops; publisher sends lower layers; FEC and NACK per hop; others unaffected |
| UDP blocked by firewall | Cannot connect | TURN over TCP or TLS 443; warn the user that quality may suffer |
| Keyframe storm (many PLIs) | Publisher bitrate spikes, everyone stutters | SFU coalesces and rate-limits PLIs per publisher |
| Top-of-hour join spike | Signaling and allocator overload | Stateless signaling edge, pre-warmed SFU capacity before the hour, admission queueing of a few hundred ms |
| Backbone link between regions degrades | Cascaded streams lose quality | Reroute cascade through another region; fall back to lower layers on the cascade link |

#### Tradeoffs

| Decision | Chosen | Alternative | Why |
|---|---|---|---|
| Topology | SFU, cascaded across regions | Mesh or MCU | Mesh breaks client uplinks; MCU costs cores and latency per meeting |
| Layering | Simulcast (SVC where codecs allow) | Single stream | Per-receiver quality without transcoding |
| Transport | RTP over UDP, TURN TCP/443 fallback | WebSocket or TCP for media | Head-of-line blocking and TCP backoff break the latency budget |
| Loss recovery | NACK per hop on short RTT, FEC on long RTT or high loss | One mechanism everywhere | Retransmission is cheap when RTT is low; FEC avoids a round trip when it is not |
| Large audiences | Compose to LL-HLS on a CDN | SFU tree to 50k viewers | Same content for everyone; CDN egress is cheaper and simpler |
| Recording | Per-track capture, compose later | Real-time composite | Cheaper at peak; flexible; slower delivery |

**Main interview tradeoff:** **server visibility versus privacy and cost.** An SFU that sees only packets is cheap and fast, but every server-side feature (recording, transcription, dial-in mixing, webinar composition) requires the server to decode media. End-to-end encryption removes exactly that ability. The design keeps the SFU decoding-free on the hot path and confines decoding to opt-in side components (recorder, streaming bridge, PSTN gateway), which is also why E2EE meetings must disable those features.

#### Follow-ups with model answers

**Q1. How does end-to-end encryption work with an SFU, and what do you give up?**

Clients encrypt each media frame with a key shared only among participants (insertable streams with SFrame), and keys are distributed through a group key agreement such as MLS, with the server only relaying opaque handshake messages. The SFU still sees RTP headers and the codec's dependency descriptor, so it can still select layers and forward without reading content. You give up cloud recording, live transcription, PSTN dial-in (the phone network cannot decrypt), server-composed webinars, and server-side noise suppression. Keys must rotate when someone leaves, which costs a little time on each departure.

**Q2. A participant is on hotel Wi-Fi with 5% loss and 250 ms RTT. What does the system do?**

The congestion controller sees delay growth and loss and lowers that participant's send bitrate; with simulcast they stop sending 720p. Because the RTT is long, NACK retransmissions often arrive too late for the jitter buffer, so the sender raises FEC overhead (about 20-30% at 5% loss) and audio uses in-band FEC plus redundancy. Their downlink allocation drops to audio, the active speaker at 360p, and thumbnails paused. Everyone else in the meeting is unaffected because each subscriber's layers are chosen independently at the SFU.

**Q3. How do you run a 10,000-person all-hands where anyone might be unmuted?**

Split roles. Presenters and the few people who are unmuted at any moment are on the SFU path; everyone else watches the LL-HLS stream (2-5 s behind) with chat and raise-hand. When the host unmutes someone, signaling promotes them to the SFU path; there is a short audio gap while their client connects. If the product insists on everyone being interactive, run a cascaded SFU tree with audio limited to the top 3 speakers and video only for active speakers. That is feasible but costly, and the composed stream gives most viewers the same experience.

**Q4. What exactly happens when an SFU node dies mid-meeting?**

Clients and peer SFUs notice missing RTP and RTCP within about 2 seconds. Clients report it over signaling (which runs on separate machines), and the controller allocates a replacement SFU in the same region and sends each affected client an ICE restart. The clients reconnect and republish, and cascade links are re-established. The meeting sees about 3-5 seconds of frozen video and silence from affected participants. No meeting state is lost because the roster lives in the controller, not the SFU. To reduce impact, keep per-node blast radius bounded (do not pack one giant meeting onto one node without a cascade peer).

**Q5. How do you choose where to host a meeting that has not started yet?**

Do not choose up front. Place the meeting where the first participant joins, then let each later joiner pick their own nearest region and cascade, so placement emerges from who actually shows up. Rebalance only if the first region is far from everyone else (for example, one person in Sydney and 30 in Europe), by adding a European SFU and letting new joins land there. Moving existing participants is optional, because it costs a reconnect.

#### Level signals

- **Mid:** WebRTC, knows mesh does not scale, proposes a media server and a signaling server, mentions STUN/TURN.
- **Senior:** SFU with simulcast and bandwidth math for mesh/MCU/SFU; per-subscriber layer selection; UDP with NACK, FEC, and jitter buffers; cascading SFUs for global meetings; webinar via LL-HLS.
- **Staff:** sizes the fleet by bandwidth and packet rate; explains keyframe-storm and PLI coalescing; designs controller failover separately from media; frames E2EE as a feature tradeoff with the server-visibility boundary; plans for the top-of-hour join burst.

See also: [HLD 6.5 Video Streaming Platform](../computer-science/High_Level_Design.md#65-video-streaming-platform), [CS Fundamentals: TCP vs UDP](../computer-science/CS_Fundamentals.md#22-tcp-vs-udp), [CS Fundamentals: NAT](../computer-science/CS_Fundamentals.md#nat-network-address-translation), [CS Fundamentals: WebSockets vs HTTP](../computer-science/CS_Fundamentals.md#websockets-vs-http)

---

### A16. Top-K Trending Topics

#### Requirements and assumptions

- **Input:** every hashtag in a post and every normalized search query is an event `(topic, user_id, region, event_time)`. Peak 1M events/s, average 400k/s.
- **Output:** per region (~50 countries plus "global") and per window (5 min, 1 h, 24 h), the top 10 **trending** topics. Internally rank 50 so the moderation step can drop some.
- **Trending, not popular:** a topic trends when its current rate is far above its own baseline for that time of week. "#monday" on a Monday is not trending; "#earthquake" at 40× its normal rate is.
- **Counting unit:** distinct users per sub-window, not raw events. One account posting a tag 1,000 times counts once.
- **Freshness:** the 5-minute list refreshes every 30 s with end-to-end lag under 60 s. The 1 h and 24 h lists refresh every minute.
- **Accuracy:** displayed counts may be rounded. The ranking must not miss a topic whose true count is in the top 10 by more than a small, stated error.
- **Reads:** the trending box is on every home page load, about 200k reads/s, identical for everyone in a region.
- Out of scope: personalized trending (a follow-up), semantic clustering of near-duplicate topics beyond normalization.

#### Capacity estimate

```text
Events:            1M/s peak, 400k/s avg × 86,400   ≈ 35B events/day
Event size:        ~100 B on the wire                 -> 100 MB/s peak ingest, ~3.5 TB/day raw log
                   keep 48 h in the log for replay    ≈ 7 TB
Distinct topics:   ~100M (topic, region) pairs per day; ~3M per minute; Zipf-distributed
                   the top 1% of topics carry most of the events; most topics appear once or twice

Naive exact 24 h map: 100M pairs × ~50 B (key, count, hash-map overhead) ≈ 5 GB per window copy,
                   updated 1M times/s at one place        -> fine for memory, impossible for one hot key

Stage 1 (dedupe + combine), partitioned by user_id:
  64 workers × ~16k events/s each; flush partial counts every 2 s
  dedupe set per worker: 16k/s × 30 s sub-window ≈ 480k (user, topic) fingerprints × ~24 B ≈ 12 MB
  a viral tag at 50k events/s becomes ≤ 64 workers ÷ 2 s = 32 records/s downstream
  long tail does not compress: ~400k partial-count records/s out (~2.5× reduction overall)

Stage 2 (window state), partitioned by hash(topic):
  64 partitions × ~6k records/s each -> CPU is trivial; memory is the question
  sub-windows: 5 min = 10 × 30 s,  1 h = 60 × 1 min,  24 h = 96 × 15 min
  1 h state:  60 buckets × ~60k entries per partition × 40 B ≈ 150 MB
  24 h state: 96 buckets × ~400k entries × 40 B ≈ 1.5 GB; prune entries with count < 3 in closed
              15-min buckets (≈ 80% of entries) -> ~300 MB per partition, max undercount 2 × 96 = 192
Results:           ~51 regions × 3 windows × 50 items × ~100 B ≈ 765 KB total -> cache everywhere
```

**What the numbers decide:** the problem is not raw throughput (100 MB/s is small) but **skew**: a single viral topic would melt a per-topic counter. A combiner stage absorbs the skew before data is keyed by topic. Memory is driven by the long tail in the 24 h window, so closed buckets are pruned with a stated undercount bound (192 is negligible against a top-10 threshold in the tens of thousands). The output is under 1 MB, so serving is a cache problem, not a database problem.

#### Interfaces and data

```text
Ingest (internal):  Kafka topic "topic-events", key = user_id, 128 partitions
                    { topic_id, raw_topic, user_id, region, event_time, client, account_age_days }
Read API:           GET /v1/trending?region=FR&window=1h -> { generated_at, version,
                        items: [{ topic, display_count, score, rank }] }
Admin:              POST /v1/trending/blocklist { topic, scope, reason }

Stage-2 state (in the stream processor, checkpointed):
  bucket[(region, window_kind, bucket_start)] : map topic_id -> distinct_user_count
  running[(region, window_kind)]              : map topic_id -> sum over live buckets
Baseline store (KV):  key (topic_id, region) -> 168 hour-of-week EWMA rates, last_updated
                      only for pairs that ever crossed a minimum count (~10M pairs × 168 × 4 B ≈ 7 GB)
Published lists (KV + in-process cache): key (region, window) -> list, version
```

Stage 1 is keyed by **user_id** because per-user dedupe and per-user rate caps need all of one user's events in one place. Stage 2 is keyed by **topic_id** because a topic's count must be complete in one place for the merge to be exact. The combiner between them is what makes re-keying by topic safe under skew.

#### Architecture and flow

```text
Posts / Search --> Event log (Kafka, key=user_id) --> Stage 1 workers (64)
                                                      | normalize topic (case fold, NFKC, alias map)
                                                      | per-user dedupe per sub-window, rate cap,
                                                      | account-reputation weight
                                                      | combine: (topic, region, sub-window) -> partial count
                                                      v every 2 s
                                    Partial counts (Kafka, key=topic_id)
                                                      |
                                                      v
                              Stage 2 window operators (64, keyed by topic)
                              ring of tumbling buckets per window; running sums;
                              local top-500 per (region, window) every 30 s
                                                      |
                                                      v
                              Ranker: merge local lists -> top 1,000 candidates by count
                              -> fetch baselines -> velocity score -> min-volume gate
                              -> safety classifier + blocklist -> top 50
                                                      |
                                                      v
                              Publisher: versioned lists -> KV (replicated to every serving region)
                                                      |
                                                      v
Clients --> Trending API (in-process cache, TTL 30 s, refreshed from the KV)
```

**Write path:**

1. Producers write each event to the log keyed by `user_id`.
2. A stage-1 worker normalizes the topic, drops the event if this user already counted for this topic in the current 30 s sub-window, and applies a per-user cap (for example 30 distinct topics per minute).
3. It adds the weighted count into a local map keyed by `(topic, region, sub-window)` and also under region "global". Every 2 s it flushes the map as partial-count records keyed by `topic_id`.
4. A stage-2 operator adds each partial count into the open bucket for that topic and updates the running sum for each window that contains the bucket.
5. Every 30 s each stage-2 partition emits its local top 500 by running sum per `(region, window)`.
6. The ranker merges the 64 lists, scores the top 1,000 by velocity, filters, and publishes the final 50.

**Read path:** the API server reads `(region, window)` from its in-process cache, refreshed from the replicated KV every 30 s. No request touches the pipeline.

#### Deep dive: exact vs approximate counting

| Approach | Memory | Error | When it fits |
|---|---|---|---|
| Exact map keyed by topic (after a combiner) | Proportional to distinct topics in the window | None | When the distinct set fits after pruning, as here |
| Count-Min Sketch + min-heap of size K | Fixed, for example 5 × 2,719 counters ≈ 54 KB | Overestimates by ≤ ε·N with probability 1 − δ | Very high cardinality, or point lookups ("how many posts for #foo?") |
| Space-Saving / Misra-Gries with m counters | m entries | Every item with frequency > N/m is kept; count error ≤ N/m | Deterministic heavy hitters in bounded memory; summaries are mergeable |
| Lossy counting / prune small counts | Shrinks with the threshold | Undercount ≤ threshold × buckets | Long windows built from many buckets |

The mechanics of CMS, the heap, and Space-Saving are in [4.10](../computer-science/High_Level_Design.md#410-probabilistic-counting-hyperloglog-and-count-min-sketch). The decision here:

- **Exact counts for the head, pruning for the tail.** After keying by topic, each stage-2 partition holds ~60k entries per 1-minute bucket. Exact maps are cheap at that size, and exact counts make the merge trivially correct.
- **Space-Saving as the safety valve.** If a bot wave or a new market inflates cardinality, cap each bucket at m = 100k counters per partition. With N ≈ 1M events/s × 60 s × 2 (country + global) ÷ 64 partitions ≈ 1.9M counted events per partition-minute, the guarantee is error ≤ N/m ≈ 19, far below any top-10 threshold.
- **CMS for point lookups only.** The product page "12.3K posts about #foo in the last hour" for an arbitrary topic is answered from a per-region CMS per hour, not from the top-K state.

Why not CMS + heap as the primary structure? It works, but the heap only holds candidates seen while they were large, and sliding a CMS window requires keeping one sketch per bucket and summing them (sketches add element-wise). At this cardinality exact maps cost about the same memory and remove the error analysis from every downstream discussion.

#### Deep dive: two-stage aggregation and merging top-K lists

**When merging is exact.** Stage 2 is partitioned by topic, so every topic's full count lives in exactly one partition. The global top-K is then contained in the union of the local top-K lists: merge, sort, cut. No item can be missed.

**When merging misses items.** If partial top-K lists come from partitions that each see only a **slice** of every topic (stage-1 workers keyed by user, or three datacenters computing local trends), an item can be just below the cut everywhere and first overall. With local top-2 lists:

```text
            local top-2 sent      not sent
DC1:        A=100, B=90           X=80
DC2:        C=100, D=90           X=80
DC3:        E=100, F=90           X=80
Merged lists: A,C,E=100 ... X never appears, yet X's true total is 240 (rank 1).
```

**How to bound it.** Each source also reports its threshold `t_i`, the count of its last listed item. Any unlisted item has at most `t_i` at source i. So:

- An item missing from every list has a total of at most `Σ t_i` (270 above).
- An item seen in some lists has lower bound = sum of reported counts, upper bound = that plus `t_i` for each source that did not list it.
- If the current K-th lower bound is ≥ `Σ t_i` and ≥ every candidate's upper bound outside the top K, the result is **certified exact**.

When it is not certified, run the TPUT repair (three-phase uniform threshold): take τ = the K-th lower bound from phase 1 (100 above), ask each source for every item with local count ≥ τ / P (here 100 / 3 ≈ 34), which returns X from all three, then fetch exact counts for remaining candidates whose upper bound ≥ τ. In practice, over-fetching (send top 10K to answer top K) makes the certificate pass almost always, and the repair round is the fallback.

In this design the cross-datacenter "global" list avoids the problem by shipping stage-1 partial counts to one region (400k records/s × 32 B ≈ 13 MB/s, cheap), so the merge stays keyed and exact. The bound matters when you cannot ship counts, for example when merging per-device or per-tenant summaries.

#### Deep dive: sliding windows, velocity, and abuse

**Sliding windows from tumbling buckets.** A true per-event sliding window needs every event timestamp. Instead keep a ring of B tumbling buckets per window. When a bucket closes, add it to the running sum and subtract the bucket that fell out. The window is then accurate to one bucket width: the "5 minute" window is the last 10 closed 30 s buckets, exactly 5 minutes long but ending up to 30 s in the past. Buckets are by **event time** with a watermark of max event time minus 10 s; events later than the bucket's allowed lateness are dropped and counted ([4.11](../computer-science/High_Level_Design.md#411-stream-processing)). Coarser buckets for longer windows (15 min for 24 h) keep memory flat: 10 + 60 + 96 buckets instead of 2,880 thirty-second buckets for a day.

**Velocity score.** For candidate topic t in window w, with current distinct-user count `c` and expected count `E` from the baseline store (EWMA of the same hour-of-week over 4 weeks, scaled to the window length):

```text
score = (c − E) / sqrt(E + α)        α = 50, a prior that stops tiny baselines from exploding
gate:   c ≥ min_volume(region, window), for example 200 users in 5 min for a large country

#monday:      E = 50,000/h, c = 55,000  -> 5,000 / sqrt(50,050) ≈ 22
#earthquake:  E = 10/h,     c = 8,000   -> 7,990 / sqrt(60)     ≈ 1,031
#newtag:      E = 0,        c = 40      -> fails the min-volume gate
```

This is a Poisson z-score: under normal behavior `c − E` has standard deviation about `sqrt(E)`. Candidates come from the top 1,000 by count, so the baseline store is read about 150 lists × 1,000 candidates every 30 s ≈ 5k lookups/s. A daily batch job updates baselines from the raw log. A topic that trended yesterday has a raised baseline today, which naturally retires stale trends.

**Spam and bot filtering**, in pipeline order:

- Count **distinct users** per sub-window (stage-1 dedupe) and cap topics per user per minute.
- Weight by account reputation: new or unverified accounts count 0.1, accounts flagged by the abuse system count 0.
- Diversity checks on candidates: distinct users ÷ events, entropy of IPs, ASNs, and client types, share of accounts created in the last 7 days. A topic pushed by 5,000 accounts created yesterday on 3 ASNs is demoted.
- Policy: blocklist, a safety classifier on the ~1,000 candidates per list (cheap because it runs on candidates, not on the 1M/s stream), and human review before a topic enters the global top 10.

#### Failure modes and mitigations

| Failure | Impact | Mitigation |
|---|---|---|
| Stage-2 partition crashes | Its topics vanish from lists until recovery | Checkpoint state and log offsets (Flink-style); restore ~300 MB and replay; serve the last published lists meanwhile |
| Viral topic (hot key) | One stage-2 partition overloaded | Stage-1 combiner bounds per-topic records to workers ÷ flush interval (32/s) regardless of event rate |
| Stage-1 lag during a spike | Lists go stale | Lag alarm; publish `generated_at`; the API keeps serving the previous version rather than an empty box |
| Late or reordered mobile events | Counts land in the wrong bucket or are dropped | Event-time buckets with a watermark and allowed lateness; drop counter as an SLI |
| Coordinated bot campaign | Fake topic trends | Distinct-user counting, reputation weights, diversity checks, human review for global slots |
| Bug in normalization or scoring | Wrong lists published | 48 h log retention; replay into a shadow pipeline and compare before switching |
| Baseline store unavailable | No velocity scores | Fall back to cached baselines; if missing, rank by count with a stricter min-volume gate |

#### Tradeoffs

| Decision | Chosen | Alternative | Why |
|---|---|---|---|
| Counting structure | Exact maps after a combiner, pruned tail, Space-Saving cap | CMS + heap everywhere | Exact maps fit after keying; merge correctness is then trivial |
| Partitioning | User-keyed stage 1, topic-keyed stage 2 | Single keyed stage | Dedupe needs user locality; exact merge needs topic locality |
| Window mechanics | Tumbling buckets summed into windows | Per-event sliding window | Bounded memory; error of one bucket width is acceptable |
| Trend score | z-score against hour-of-week baseline | Raw count, or ratio c / E | Raw count shows evergreen topics; pure ratios explode on tiny baselines |
| Serving | Precomputed lists in a replicated cache | Query the pipeline on read | Under 1 MB of output; reads must not depend on stream health |

**Main interview tradeoff:** **freshness versus stability and abuse resistance.** Shorter buckets and lower volume gates surface real events faster, but they also let small coordinated campaigns and statistical noise reach the box. Longer buckets, distinct-user counting, and human review make the list trustworthy but slower. The usual answer is fast, automated lists per country with stricter gates and review for the global list.

#### Follow-ups with model answers

**Q1. Why not a Redis sorted set with `ZINCRBY` per event?**

It is a fine prototype at 1k events/s. At 1M/s it fails three ways: a viral topic makes one key (one shard) absorb tens of thousands of increments per second; the sorted set grows with every long-tail topic and has no windows, so you need one set per bucket plus expiry; and it counts events, not distinct users. Put a combiner in front and you could still use sorted sets as the stage-2 state store, but you have rebuilt the stream design with an extra network hop per update.

**Q2. How would you personalize trending?**

Compute candidate lists per region and per interest cluster (a few hundred clusters from the social graph or embeddings), using the same pipeline with cluster as another region-like key. At read time, take the user's top 3 clusters, union their lists with the region list, and rerank lightly by the user's affinity. This keeps the expensive aggregation shared, at a few hundred lists rather than one per user. Pure per-user trending is mostly noise because individual baselines are too small.

**Q3. The product wants exact counts shown next to each trend.**

Make the displayed number come from an exact path: once a topic is in the published top 50, run an exact distinct-user count for it (an HLL with p = 14 is 0.81% error, or an exact set if the count is small) and show that number rounded. The ranking can stay approximate because the certification argument bounds missed items, and the number the user sees is exact enough. A nightly batch over the raw log reconciles analytics.

**Q4. How do you test a new trending score before launch?**

Replay the last 48 h of events (or longer from cold storage) through a shadow pipeline with the new score, and compare lists offline: churn, how early known news events surfaced, and how many abuse-flagged topics appeared. Then run an online experiment by region with engagement and report-rate metrics. Replayability is why the raw log is retained and the pipeline is deterministic given the same input and watermark settings.

**Q5. What changes at 10M events/s?**

Stage 1 scales horizontally with log partitions. The per-topic record rate into stage 2 is bounded by workers ÷ flush interval, so lengthen the flush to 5 s or add a second combine tier per rack. Stage-2 memory grows with cardinality, so the Space-Saving cap becomes the normal mode instead of the fallback. The ranker, baseline store, and serving tier do not change, because their inputs are candidate lists, not events.

#### Level signals

- **Mid:** defines a time-windowed count, uses a stream processor and a heap for top-K, caches the output, and estimates ingest bandwidth.
- **Senior:** separates trending from popular with a baseline score; designs the combiner to defeat hot keys; explains when merging local top-K lists is exact and when it is not; builds sliding windows from buckets with stated memory.
- **Staff:** certifies or repairs non-keyed merges (thresholds, TPUT), treats abuse as a first-class requirement with distinct-user counting and review, and designs for replayable evaluation of scoring changes.

See also: [4.10 Probabilistic Counting](../computer-science/High_Level_Design.md#410-probabilistic-counting-hyperloglog-and-count-min-sketch), [4.11 Stream Processing](../computer-science/High_Level_Design.md#411-stream-processing), [4.13 Cache Stampede and Hot Keys](../computer-science/High_Level_Design.md#413-cache-stampede-and-hot-keys), [Mock 6: Search Typeahead](HLD_Mock_Interviews.md#9-mock-6-search-typeahead).

---

### A17. Distributed Lock Service

#### Requirements and assumptions

- **Data model:** a hierarchical namespace of small nodes (typically under 1 KB, hard limit 1 MB) with versions; create, get, set with expected version, delete, list children, and multi-operation transactions with compare guards.
- **Sessions:** each client process opens a session with a TTL (for example 10 s) and keeps it alive. **Ephemeral** nodes are deleted when their session ends. **Sequential** nodes get a monotonically increasing suffix.
- **Watches:** clients subscribe to changes on a node or prefix and never miss an event across reconnects.
- **Recipes built on these:** exclusive locks with fencing tokens, leader election, shard ownership, service discovery, dynamic config.
- **Consistency:** all writes linearizable. Reads linearizable on request, otherwise sequentially consistent with per-session monotonicity (a client never sees an older state than one it already saw).
- **Availability:** survive the loss of any one zone in a three-zone region; leader failover within a few seconds. The service is CP: a minority partition refuses writes.
- **Scale per cell:** ~50k client sessions, ~2k writes/s typical and 5k/s peak, ~100k reads/s, under a few GB of data.
- Out of scope: storing bulk data, being a general database, a single globally replicated cell (discussed in a follow-up).

#### Capacity estimate

```text
Sessions:        50k sessions, TTL 10 s, keepalive every ~3 s     ≈ 17k keepalives/s
                 keepalives are handled by the leader in memory, NOT written through the Raft log
Writes:          lock acquire/release, elections, config: ~2k/s typical, 5k/s peak
Write cost:      leader appends + fsync, replicates to 4 followers, commits on 2 follower acks (3 of 5)
                 intra-region RTT ~0.5-1 ms + fsync ~0.1-1 ms (NVMe with power-loss protection)
                 -> commit latency ≈ 2-4 ms; batching amortizes fsync across many writes
Replication bw:  5k writes/s × ~1 KB × 4 followers ≈ 20 MB/s -> trivial
Data:            ~1M nodes × ~1 KB ≈ 1 GB, held fully in RAM on every replica
Snapshot:        1 GB snapshot to a new or lagging follower at ~500 MB/s ≈ 2 s of transfer
Reads:           100k/s; one replica serves ~30-50k reads/s from memory -> spread across all 5
Watches:         50k sessions × ~10 watches ≈ 500k registered watches
                 one hot config key watched by 50k clients -> 50k notifications per change
Failover:        heartbeat 100 ms, election timeout 1 s -> new leader in ~1-2 s
```

**What the numbers decide:** write throughput is in the low thousands per second, bounded by a quorum round trip and fsync, and that is enough because the service sits on the **control plane**: a client takes a lock once and then does minutes of data-plane work under it. Keepalives are the largest request stream, so they must not go through consensus. The whole state fits in RAM, so recovery is bounded by snapshot transfer (seconds), which is why the data size limit is a design rule, not a suggestion.

#### Interfaces and data

```text
OpenSession(ttl_s)                               -> session_id (a lease)
KeepAlive(stream session_id)                     -> ttl_remaining
Create(path, data, flags {EPHEMERAL, SEQUENTIAL}) -> actual_path, create_revision
Get(path, consistency {LINEARIZABLE, SEQUENTIAL}) -> data, version, mod_revision
Set(path, data, expected_version)                -> new_version | ERR_BAD_VERSION
Delete(path, expected_version)
List(path)                                       -> children
Watch(path | prefix, start_revision)             -> stream of {type, path, revision}
Txn(compares[], then_ops[], else_ops[])          -> succeeded, results
Client library recipes: Lock(name) -> {lock_path, fencing_token}; Unlock; Campaign(election, value); Observe

node(path PK, data, version, create_revision, mod_revision, ephemeral_owner session_id NULL)
session(session_id PK, ttl_s)                     -- replicated on grant and revoke only
session_expiry(session_id -> expires_at)          -- leader memory only, reset on leader change
revision: one global counter, incremented by every committed write (the Raft-ordered sequence)
```

A single cell is one Raft group holding the whole namespace: every write goes through one log, which gives a **global total order** and a single monotonically increasing revision. That revision is the fencing token. If one cell is not enough, partition by namespace (one cell per team or per service tier) rather than splitting one namespace across groups, because cross-group transactions and watches lose the total order.

#### Architecture and flow

```text
          Zone A                    Zone B                    Zone C
     +-----------+             +-----------+             +-----------+
     | Replica 1 | <---------> | Replica 3 | <---------> | Replica 5 |
     |  LEADER   |   Raft log  | follower  |             | follower  |
     | Replica 2 |             | Replica 4 |             +-----------+
     +-----------+             +-----------+
          ^   each replica: WAL on local SSD, in-memory tree, snapshotter, watch hub
          |
   Client library (in every service process)
     - one gRPC connection to any replica; writes forwarded to the leader
     - session keepalive stream to the leader
     - local cache of read nodes, invalidated by watch events
     - recipes: lock, election, barrier
   Optional: non-voting learners in other regions for local stale reads
```

Five voters spread 2/2/1 across zones: losing any one zone leaves at least 3 of 5. Three voters also survive one zone loss but then cannot tolerate a further node failure during repairs.

**Lock acquisition (write path):**

1. The client opens a session and creates `/locks/orders-shard-7/lock-` with EPHEMERAL | SEQUENTIAL. The leader appends the operation, replicates it, and commits on a majority. The node becomes `lock-0000000042` with `create_revision = 918,113`.
2. The client lists the children. If its node has the lowest sequence number, it holds the lock and uses `create_revision` as its **fencing token**.
3. Otherwise it watches only the node immediately before its own. When that node is deleted (released or session expired), it re-checks. Watching only the predecessor avoids the herd where every waiter wakes on every release.
4. Release is `Delete(lock_path)`. A crashed holder's node disappears when its session expires.

**Read path:** sequential reads are served by whichever replica the client is connected to, provided that replica has applied at least the last revision this client saw (the client sends it). Linearizable reads use ReadIndex (below).

#### Deep dive: replicated state machine, sessions, and watches

The core is a Raft log of operations applied in order to an in-memory tree. Leader election, log matching, and commit rules are covered in [CS 8.12](../computer-science/CS_Fundamentals.md#812-consensus-theory-and-raft-in-depth). Design points specific to a lock service:

- **Keepalives bypass the log.** Session grant and revoke are log entries, but renewals only update the leader's in-memory expiry. On leader change, the new leader does not know recent renewal times, so it **resets every session's expiry to a full TTL** from its election. That can extend a dead client's session by one TTL (safe: delays a takeover) but never shortens a live one. Expiry itself is a log entry ("revoke session S, delete its ephemerals"), so all replicas delete the same nodes at the same log position.
- **Client-side lease timer.** The client measures its session from when it **sent** the keepalive, not when the reply arrived, and treats the session as possibly lost after, for example, 2/3 of the TTL without a successful renewal. At that point it must stop acting as lock holder or leader. The server waits the full TTL before expiring. The gap between the client's 6.7 s and the server's 10 s absorbs clock-rate drift. It does not absorb process pauses, which is why fencing exists.
- **Watches that cannot miss events.** Every event carries the revision that produced it. A client reconnecting after a network blip resumes with `Watch(prefix, start_revision = last_seen + 1)`. The server keeps a history window of recent revisions (for example the last 1M or last 10 minutes). If the client is older than the compacted history, the server returns "compacted" and the client must re-read the current state, then watch from that revision. ZooKeeper's one-shot watches achieve the same by requiring a re-read on each fire.
- **Watch fan-out.** A change to a key watched by 50k clients produces 50k notifications. Coalesce them in a per-replica watch hub (one stream per client connection, many watches multiplexed), spread clients across all replicas, and advise teams to put widely-watched config behind a single version key rather than many small keys.

#### Deep dive: fencing tokens and why Redis locks are not enough

A lease guarantees that the **service** will not grant the lock to someone else before the lease expires. It cannot guarantee that the **holder** still believes the truth when it acts. The standard failure:

```text
t=0     client 1 acquires lock, token 918,113; session TTL 10 s
t=1     client 1 starts a 15 s stop-the-world GC pause
t=11    server expires client 1's session, deletes its node; client 2 acquires, token 918,402
t=12    client 2 writes shard 7 with token 918,402; storage records max_token = 918,402
t=16    client 1 resumes, still "holds the lock" in its own memory, writes with token 918,113
        storage compares 918,113 < 918,402 -> REJECTED
```

The token works only if the **protected resource checks it**: the storage layer keeps the highest token seen per resource and rejects lower ones, or the write is a conditional update (`UPDATE ... WHERE fence <= :token`). If the resource lives in the lock service itself, use a transaction guarded by the lock node's revision: `Txn(compare lock_path.create_revision == token, then Put(...))`. The full argument and a runnable demo are in [CS 8.13](../computer-science/CS_Fundamentals.md#813-consistency-guarantees-split-brain-leases-and-fencing).

Why not Redis for correctness locks:

- **Single Redis node with `SET key value NX PX 10000`.** Atomic and fast, but replication to the replica is asynchronous. The primary acknowledges the lock, crashes before replicating it, the replica is promoted without the key, and a second client acquires the same lock. Two holders, no error anywhere.
- **Redlock** (acquire on a majority of N independent masters within the validity time). It removes the single-failover problem but still assumes bounded network delay, bounded process pauses, and well-behaved clocks. An NTP step on one master expires a key early, and a GC pause after acquisition is invisible to it. Its random lock value is not monotonic, so it cannot serve as a fencing token.
- **Verdict:** Redis locks are fine as **efficiency locks** (avoid two workers doing the same idempotent job; a rare double is harmless). For **correctness locks**, use a consensus-backed service with fencing tokens, or skip the lock and use a conditional write on the resource itself.

#### Deep dive: read scaling and leader election as a client use case

| Read mode | Mechanism | Cost | Guarantee |
|---|---|---|---|
| Leader read, naive | Leader answers from its state | Cheap | **Unsafe**: a deposed leader on the minority side of a partition can serve stale data |
| ReadIndex | Leader records commit index, confirms leadership with one heartbeat round to a majority, waits until applied, answers | 1 RTT, no disk write | Linearizable |
| Follower ReadIndex | Follower asks leader for the commit index, waits to apply it locally, answers | 1 RTT to leader; read load moves to followers | Linearizable |
| Lease read | Leader skips the heartbeat round while within a lease shorter than the election timeout | No extra RTT | Linearizable if clock drift is bounded |
| Sequential read | Any replica that has applied the client's last-seen revision | Local | Stale but monotonic per session |

Default to sequential reads for config and discovery, which is 90%+ of traffic, and let callers ask for linearizable reads before acting on a decision. ReadIndex details are in [CS 8.12](../computer-science/CS_Fundamentals.md#812-consensus-theory-and-raft-in-depth).

**Leader election for a client service** is the lock recipe with a value: candidates create `/election/payments-scheduler/n-` as EPHEMERAL | SEQUENTIAL with their address as data. The lowest sequence number is the leader; others watch their predecessor. Followers and callers discover the leader by reading the lowest child. The leader's fencing token is its node's `create_revision`, attached to every write it makes to shared state. The leader must step down (stop issuing writes) as soon as its client-side lease timer says the session may be lost, even before the service confirms it.

#### Deep dive: what clients see during a leader failover

```text
t=0.0 s   leader (replica 1) crashes; clients' keepalive streams and in-flight writes to it fail
t=0.0-1.0 followers stop receiving heartbeats (100 ms interval); randomized election timeouts (1.0-2.0 s)
t~1.3 s   replica 3 times out first, becomes candidate, wins votes from 3 of the 4 survivors
          (a voter grants only if the candidate's log is at least as up to date as its own)
t~1.4 s   new leader commits a no-op entry in its term, which also commits any entries left over
          from the old term; it resets every session's expiry to now + full TTL (10 s)
t~1.5 s   client libraries reconnect with jittered backoff, re-open keepalive streams, and resume
          watches from their last seen revision; writes that failed are retried
          (Create of a sequential lock node is NOT blindly retried: the client first lists its own
           session's nodes, because the original create may have committed before the crash)
Result:   ~1-2 s with no writes; no session expired; no lock changed hands; no watch event lost
```

The subtle point is the **ambiguous write**: a request that timed out may or may not have committed. Idempotent operations (set with expected version, delete with version) can be retried safely. Non-idempotent ones (sequential create) need a check first, which is why lock recipes tag their nodes with the session ID. Clients whose own lease timer expired during the gap (a 10 s TTL makes that unlikely in a 2 s failover) treat the lock as lost and re-acquire, getting a new fencing token.

#### Failure modes and mitigations

| Failure | Impact | Mitigation |
|---|---|---|
| Leader crash | Writes stall for ~1-2 s until election | Election timeout 1 s; client library retries writes with idempotent operations; sessions extended by a full TTL on the new leader |
| Network partition isolating the old leader | Old leader cannot commit; naive leader reads could be stale | Writes need a majority; reads use ReadIndex or lease reads; old leader steps down when heartbeats fail |
| Client GC pause or VM migration | Client acts on an expired lock | Fencing tokens checked by the resource; client-side lease timer shorter than server TTL |
| Slow fsync on one replica's disk | If it is the leader, every commit slows; heartbeats can miss and trigger elections | Dedicated SSDs, monitor fsync p99, move leadership away from slow nodes |
| Reconnect storm after failover | 50k clients reconnect at once | Jittered exponential backoff in the client library; sessions survive because expiry was reset |
| Someone stores large blobs | Snapshots grow, followers take minutes to catch up | Enforce 1 MB value limit and per-tenant quotas; total data size alarms |
| Watch history compacted during a long disconnect | Client cannot resume | Return "compacted"; client re-lists, then watches from the new revision |

#### Tradeoffs

| Decision | Chosen | Alternative | Why |
|---|---|---|---|
| Consensus | Raft, one group per cell | Leaderless quorums | Locks need a total order and a monotonic token; quorums alone give neither |
| Replica count | 5 voters across 3 zones | 3 voters | Survives a zone loss plus one more failure; writes need 3 acks instead of 2 |
| Session renewals | Leader memory only, reset on failover | Replicate every keepalive | 17k/s through the log would dwarf real writes; reset is conservative |
| Lock primitive | Ephemeral sequential nodes + predecessor watch | Server-side lock queue API | Same safety, fewer server concepts, no herd effect; etcd also offers a server-side helper |
| Default read | Sequential with session monotonicity | Always linearizable | Most reads are config; linearizable on request costs one RTT |
| Scaling beyond one cell | More cells by namespace | Shard one namespace across Raft groups | Keeps a single total order per namespace |

**Main interview tradeoff:** **safety versus availability during partitions.** The service refuses writes on the minority side, so a client cut off from the majority cannot take or renew locks and must stop working after its lease timer runs out. That is correct: an available lock service that grants the same lock on both sides of a partition is worse than none. The cost is that the lock service's availability bounds the availability of every system that depends on it, which is why it is kept small, boring, and on the control plane.

#### Follow-ups with model answers

**Q1. Why five replicas and not seven, or four?**

Majority quorums need 2f + 1 nodes to tolerate f failures. Four nodes tolerate only one failure, the same as three, with a larger quorum, so even counts buy nothing. Five tolerates two, which covers a zone outage plus one unrelated failure. Seven tolerates three but needs four acks per write and more cross-zone traffic, raising commit latency and election churn for failures that rarely happen together. For more read capacity, add non-voting learners instead of voters.

**Q2. A team wants 100k lock acquisitions per second, one per customer order.**

That is a data-plane lock, and the answer is not a bigger lock service. Per-order mutual exclusion belongs in the order store: a conditional update on the order row (`WHERE version = ?`) or a per-order lease column with a fencing check. If they truly need a coordination primitive, partition the lock namespace across many cells by hash of the lock name, accepting that there is no ordering across cells. Usually the better fix is to make the work idempotent so a rare double execution is harmless.

**Q3. Can a client hold a lock across regions?**

A cell whose voters span regions pays a cross-region RTT (tens to 100+ ms) on every write and every ReadIndex, and leader placement matters. Prefer one cell per region and design so cross-region coordination is rare: assign ownership of a resource to a region, and use a global cell only for low-rate decisions such as which region owns which shard. If a global lock is needed, place voters in three or five regions so a single region loss still leaves a majority, and expect write latency of one cross-region RTT plus fsync.

**Q4. The lock holder can reach storage but not the lock service. What happens?**

It cannot renew its session. Its client-side timer fires at about 2/3 of the TTL and it must stop writing. The server expires the session at the full TTL, deletes the ephemeral node, and the next waiter acquires the lock with a higher token. If the old holder ignores its timer (bug, pause), storage rejects its lower token. Without fencing, this is exactly how two writers corrupt data.

**Q5. How is this different from using the database's `SELECT ... FOR UPDATE`?**

A row lock lives inside one database and ends with the transaction or the connection, which is ideal when the protected state is in that database. A coordination service provides locks over resources that span systems (a shard on many machines, a scheduler role), sessions that outlive a single connection, watches for waiting without polling, and a fencing token that other systems can check. If everything protected is in one database, use the database.

#### Level signals

- **Mid:** knows a lock service needs consensus and replicas; describes acquire, release, and lock expiry; mentions heartbeats.
- **Senior:** designs sessions with keepalives off the log, ephemeral sequential nodes with predecessor watches, fencing tokens checked by the resource, and explains why Redis or Redlock is unsafe for correctness; distinguishes ReadIndex from follower reads.
- **Staff:** reasons about lease timing on both sides (client timer vs server TTL, reset on failover), watch resumption and compaction, data-size limits as a recovery-time rule, and pushes back on data-plane locking by moving mutual exclusion into the resource.

See also: [CS 8.12 Consensus Theory and Raft in Depth](../computer-science/CS_Fundamentals.md#812-consensus-theory-and-raft-in-depth), [CS 8.13 Leases and Fencing](../computer-science/CS_Fundamentals.md#813-consistency-guarantees-split-brain-leases-and-fencing), [6.12 Distributed Job Scheduler](../computer-science/High_Level_Design.md#612-distributed-job-scheduler), [Mock 5: Distributed Key-Value Store](HLD_Mock_Interviews.md#8-mock-5-distributed-key-value-store).

---

### A18. Web Search Engine

#### Requirements and assumptions

- **Corpus:** 50B pages supplied by the crawler ([6.10](../computer-science/High_Level_Design.md#610-web-crawler)), which emits a "page fetched" event and stores raw pages in object storage.
- **Queries:** 100k QPS average, 200k peak. Return the top 10 results with title, URL, and a query-dependent snippet.
- **Latency:** p50 under 100 ms and p99 under 300 ms server-side, including spelling correction, retrieval, ranking, and snippets.
- **Query features:** multi-term free text, phrase queries (`"exact phrase"`), site and language filters.
- **Freshness:** breaking news searchable within minutes of being crawled; ordinary pages within a few days.
- **Quality:** ranking combines text relevance, link signals, and a learned model trained on clicks and human ratings; spam pages demoted.
- Out of scope: crawling (exists), ads, image and video verticals, typeahead ([6.9](../computer-science/High_Level_Design.md#69-search-autocomplete-typeahead)), deep personalization.

#### Capacity estimate

```text
Corpus:           50B docs; ~600 indexable tokens, ~300 distinct terms per doc after boilerplate removal
Postings:         50B × 300                               = 1.5e13 (15 trillion) (term, doc) pairs
  uncompressed:   4 B docID + 4 B term frequency          = 8 B × 1.5e13 = 120 TB
  compressed:     delta-coded docIDs + small tf ≈ 1.5 B   -> ≈ 22.5 TB
Positions:        50B × 600 = 3e13 positions × ~1.5 B      ≈ 45 TB (needed for phrases and proximity)
Index total:      ≈ 70 TB per full copy
Doc store:        50B × ~3 KB compressed text              ≈ 150 TB (snippets; separate service)
Static features:  50B × ~200 B (PageRank, spam, language, quality) ≈ 10 TB

Shard count:      50M docs per shard -> 1,000 shards
  per shard:      22.5 GB postings (RAM) + 45 GB positions (NVMe) + 10 GB features (RAM)

Serving (peak 200k QPS, result cache hit ~50% -> 100k QPS reach the index):
  shard-query cost ≈ 5 ms of one core (Block-Max WAND over in-RAM postings, 2-4 terms)
  one 64-core server at 60% target ≈ 64 × 0.6 ÷ 0.005 ≈ 7.7k shard-queries/s
  Tier 1: best 5B docs by static rank, 100 shards; every query visits all 100
          100k/s per shard ÷ 7.7k ≈ 13 replicas -> 100 × 13       ≈ 1,300 servers
  Tier 2: all 50B docs, 1,000 shards; ~20% of queries fall through = 20k QPS
          20k ÷ 7.7k ≈ 3 replicas, +1 for failures = 4 -> 1,000 × 4 ≈ 4,000 servers
  Fresh:  last ~24 h of crawl, ~500M docs, 10 shards, every query ≈ 13 replicas × 10 ≈ 130 servers
```

**What the numbers decide:** 70 TB of index cannot live on a few machines, and 15 trillion postings cannot be scanned per query, so the design needs **sharding** (1,000 shards of a size whose postings fit in RAM), **compression** (5x smaller, which is what makes RAM residency possible), and **pruning** (most postings are never decoded). Replica count is set by query load, not data size. The tiered index is the biggest cost lever: 80% of queries are answered by 100 shards instead of 1,000.

#### Interfaces and data

```text
GET /search?q=...&hl=en&gl=FR&start=0&num=10 -> { results: [{url, title, snippet}], spell_suggestion? }

Internal RPCs:
  Root -> Aggregator -> Leaf: Search(shard_id, parsed_query, k=20, deadline_ms) -> [(doc_id, score, features)]
  Root -> DocServer:          Snippet(doc_id, query_terms) -> {title, url, snippet}

Per-shard index files (immutable, versioned):
  term dictionary:   term -> (df, offset into postings, max_score_upper_bound)   (sorted, front-coded)
  postings:          blocks of 128 docID gaps + tfs, PForDelta-coded; per block (last_docid, block_max_score)
  positions:         per (term, doc): delta-coded token offsets
  doc table:         local doc_id -> (global_doc_id, length, static_rank, spam, lang, url_hash)
  deleted bitmap:    1 bit per doc (50M bits ≈ 6 MB) for docs replaced or removed since the build
Global stats file:   term -> global df; average doc length per field (shipped to every shard)
Doc store:           doc_id -> compressed extracted text, title, URL (sharded by doc_id)
Result cache:        key (normalized query, locale, safe_search, page) -> results, ttl
```

Documents are assigned to shards by `hash(url)`, which spreads quality and topics evenly, so every shard is a statistically similar miniature engine. **Within** a shard, local doc IDs are assigned in **descending static rank**, so posting lists are ordered best-first and query evaluation can stop early.

#### Architecture and flow

```text
OFFLINE / NEAR-LINE
Crawler page store --> Doc processing (parse, dedupe via SimHash, lang, spam score)
                   --> Link graph jobs: PageRank, anchor-text join (anchors attached to the TARGET doc)
                   --> Index build (MapReduce per shard) --> versioned shard files on distributed FS
                   --> Global stats (df, avg length)       --> pushed to all shards with the index
Crawler "page fetched" events --> Real-time indexer --> Fresh tier segments (searchable in minutes)

ONLINE
User --> Front end: tokenize, spell-correct, synonyms, language --> Result cache (hit ~50%) --+
                                                                                            | miss
                                                         Root (deadline 250 ms) <-----------+
                       +-------------------+---------------------+
                       v                   v                     v
                 Fresh tier (10)     Tier-1 aggregators    Tier-2 aggregators (only if tier 1
                                     (100 leaves)          has too few good results; 32 x ~32 leaves)
                                           |
                       Leaves: Block-Max WAND, BM25F + static rank -> top 20 + features per shard
                                           |
              Root: merge ~1,600 candidates -> learned ranker (GBDT) on top 1,000
                    -> neural reranker on top 50 -> top 10 -> DocServers: snippets -> cache fill
```

**Index build (write path):**

1. Doc processing extracts text by field (title, URL tokens, headings, body) and drops near-duplicates.
2. Link jobs compute PageRank and join anchor text onto target documents (a MapReduce keyed by target URL; see [CS 8.8 MapReduce](../computer-science/CS_Fundamentals.md#88-mapreduce)).
3. For each shard, a reducer sorts that shard's `(term, local_doc_id, tf, positions)` tuples and writes compressed postings, skip data, and the term dictionary.
4. Serving replicas download the new version, load it next to the old one on a drained replica, verify checksums and canary queries, then switch. The previous version stays on disk for rollback.

**Query (read path):** the root checks the result cache, fans out to the fresh tier and tier 1 in parallel through a two-level aggregation tree, falls through to tier 2 only when tier 1 returns too few results above a quality threshold, merges candidates, reranks, fetches snippets for the final 10, and caches the page.

#### Deep dive: index sharding by document vs by term

| | By document (chosen) | By term |
|---|---|---|
| What a shard holds | Full inverted index for 1/1,000 of the docs | Full posting lists for 1/1,000 of the terms |
| Query fan-out | Every shard | Only shards owning the query's terms (2-4) |
| Network per query | Each shard returns ~20 scored docs (a few KB) | Posting lists must be shipped to one place to intersect: "the" alone has ~10s of billions of postings |
| Load balance | Even, by construction | Hot terms create hot shards; query mix shifts load |
| Failure | Lose 0.1% of documents for that query | Lose every query containing the dead shard's terms |
| Index updates | A new doc touches one shard | A new doc touches ~300 shards |
| Scoring | Shard has everything for a doc (all terms, positions, features) | Multi-term scoring and phrases need cross-shard data |

Term sharding reduces fan-out, which looks attractive, but it moves the expensive part (intersecting and scoring large lists) onto the network and turns popular terms into hot spots. Document sharding keeps each query's heavy work local and parallel and sends only tiny top-k results upstream. The cost is fan-out to every shard, which is handled by tiering and tail-latency control. One detail: with document sharding, IDF must use **global** document frequencies (shipped with the build); per-shard df would make scores slightly incomparable across shards.

#### Deep dive: posting list compression

Store docIDs as **gaps** (differences between consecutive sorted IDs), which are small for common terms, then encode the gaps with a variable-width code.

```text
Shard of 50M docs. Term "weather", df = 2.5M (5% of docs):
  raw docIDs:       2.5M × 4 B                       = 10 MB
  average gap:      50M ÷ 2.5M                       = 20 -> ~5 bits
  PForDelta:        blocks of 128 gaps at bit width b = 5, outliers stored as exceptions
                    2.5M × 5 bits                    ≈ 1.6 MB
  term frequencies: mostly 1-3 -> ~3 bits each       ≈ 0.9 MB
  total ≈ 2.5 MB vs 20 MB uncompressed (4 B docID + 4 B tf): 8x smaller

Term "bioluminescent", df = 500:
  average gap 100k -> 17 bits -> varint 3 bytes (7 payload bits per byte: <128 = 1 B, <16,384 = 2 B,
  <2,097,152 = 3 B) -> 500 × 3 B = 1.5 KB; rare terms are cheap whatever the codec

Across the corpus, postings are dominated by common terms (Zipf), so the average is ~1-1.5 B per
posting including tf: 1.5e13 postings -> ~22.5 TB instead of 120 TB.
```

**Varint** (one byte per 7 bits) is simple but decodes byte by byte with a branch per byte. **PForDelta** picks one bit width per block of 128 so ~90% of values fit, packs them, and patches exceptions; it decodes with SIMD at billions of integers per second, which matters because decode speed is part of the 5 ms per-shard budget. Each 128-posting block also records its last docID (a **skip pointer**) and its **maximum score contribution**, which make the next two techniques possible.

#### Deep dive: query evaluation, ranking, and freshness

**Top-k with WAND (weak AND).** Exhaustive OR evaluation scores every doc containing any query term, which for `new york weather` means millions of postings per shard. WAND keeps a min-heap of the best k scores so far; its minimum is the threshold θ. Each term has an upper bound UB on its score contribution. Sort the term cursors by their current docID and find the **pivot**: the first cursor where the cumulative UB reaches θ. No doc before the pivot's docID can beat θ, so all earlier cursors skip ahead to it using skip pointers (`next_geq`), decoding only the blocks they land in. Only when the leading cursors align on one docID is it fully scored. **Block-Max WAND** uses the per-block maximum instead of the global UB, a much tighter bound, and typically fully scores only a few percent of candidate docs. Because docIDs are in static-rank order, good documents are found early, θ rises fast, and pruning gets stronger.

**Tiered index and early termination.** Tier 1 holds the 5B docs with the best static rank. If tier 1 returns at least k results with scores above a quality threshold, tier 2 is skipped. Roughly 80% of queries (head and torso queries) stop at tier 1. Tail queries with rare terms fall through.

**Ranking in stages:**

```text
Stage           Where     Candidates      Model                                     Budget
Retrieval       Leaf      millions -> 20  BM25F (title, URL, anchor, body) + static rank   ~5 ms
First rerank    Root      ~1,000          GBDT (LambdaMART), hundreds of features:         ~20 ms
                                          proximity, PageRank, anchor match, click stats,
                                          freshness, spam score, URL depth
Final rerank    Root      ~50             Neural cross-encoder on query + passage           ~20 ms on accelerators

BM25(t, d) = IDF(t) × tf × (k1 + 1) / (tf + k1 × (1 − b + b × |d| / avgdl)),   k1 = 1.2, b = 0.75
PageRank:  PR(p) = (1 − d)/N + d × Σ PR(q)/outdeg(q) over pages q linking to p,  d = 0.85
```

Anchor text is one of the strongest signals: the words other sites use to link to a page often describe it better than the page itself, which is why the build joins anchors onto target documents. The learned ranker is trained on human relevance ratings plus click logs corrected for position bias.

**Freshness tier.** The crawler's "page fetched" events feed a real-time indexer that writes small in-memory segments, flushes them every minute, and merges them in the background (LSM style). The fresh tier holds about the last 24 h of crawl in 10 shards and is queried in parallel with tier 1. When a document changes, the new version is indexed in the fresh tier and the old one is marked in its main shard's **deleted bitmap**, so results never show both. The next main build absorbs it.

**Caching.** Query frequency is Zipf-like, so a result cache keyed by normalized query, locale, and page gets roughly 50% hits. TTL is minutes for ordinary queries and tens of seconds for queries classified as news-seeking. On an index version swap, warm the cache by replaying the top 1M queries against the new version before switching, instead of letting a cold cache double the index load.

#### Deep dive: tail latency at a fan-out of 1,000

```text
Leaf p99 = 50 ms. A tier-2 query waits for the slowest of 1,000 leaves:
  P(at least one leaf above its p99)     = 1 − 0.99^1000    ≈ 99.996%   -> leaf p99 is the query's median
  P(at least one leaf above its p99.999) = 1 − 0.99999^1000 ≈ 1%        -> query p99 ≈ leaf p99.999
```

The leaf's p99.999 therefore sets the query's p99. Mitigations ([5.7](../computer-science/High_Level_Design.md#57-tail-latency-amplification), [Tail Latency and Fan-Out](../computer-science/Performance_Engineering.md#14-tail-latency-and-fan-out-amplification)):

- **Hedged requests:** if a leaf has not answered by its p95 (~15 ms), send the same request to another replica and take the first answer. About 5% extra load buys a large cut in the tail.
- **Partial results:** each aggregator answers at its deadline with whatever arrived. A missing shard is 0.1% of the corpus, and with random doc assignment the global top 10 rarely depends on one shard. Mark such responses partial and do not cache them.
- **Two-level aggregation** (root -> 32 aggregators -> ~32 leaves) caps fan-in per node and keeps merge CPU off the root.
- **Deadline propagation:** leaves drop requests whose deadline already passed instead of doing useless work during a spike.
- **Isolate background work:** index loading and segment merges run on drained replicas or with strict CPU limits, and leaves are written in a language without stop-the-world GC.
- Why top 20 per shard is enough: the global top 1,000 candidates spread about 1 per shard on average, so a shard holding more than 20 of them is vanishingly rare.

#### Failure modes and mitigations

| Failure | Impact | Mitigation |
|---|---|---|
| Leaf replica dies | Queries routed to it time out | Health-checked replica sets; hedging hides the transition; N+1 replicas per shard |
| All replicas of one shard down | 0.1% of documents missing | Partial results with a flag; spread replicas across racks and power domains |
| Bad index build (corrupt shard or ranking regression) | Wrong or missing results everywhere | Checksums, canary queries with known answers, gradual rollout by replica, keep previous version for instant rollback |
| "Query of death" crashes leaves | Every replica crashes on retry, cascading outage | Send a new query shape to one replica first; if it crashes, blacklist the query; process isolation per request |
| Cache cold after an index swap | Index load doubles | Warm the cache by replaying top queries before switching versions |
| Query spike (breaking news) | Leaves saturate | Load shedding at the root (drop tier-2 fall-through first), serve slightly stale cached results |
| SEO spam or link farms | Low-quality results ranked high | Spam classifier as a static feature, link-graph anomaly detection, demotion in ranking |

#### Tradeoffs

| Decision | Chosen | Alternative | Why |
|---|---|---|---|
| Sharding | By document, hash of URL | By term | Local scoring, tiny responses, balanced load, graceful failure |
| Doc ordering in shard | By static rank | By crawl order or URL | Enables early termination and faster-rising WAND thresholds |
| Index layout | Tier 1 (5B best) + tier 2 (all) + fresh | One flat index | 80% of queries touch 100 shards instead of 1,000 |
| Retrieval | Block-Max WAND, top 20 per shard | Exhaustive scoring | Decodes a small fraction of postings; safe because it is exact for the first-stage score |
| Updates | Periodic rebuild + fresh tier + delete bitmaps | Fully incremental main index | Immutable shards compress better, are easy to verify, and roll back cleanly |
| Completeness | Partial results at the deadline | Wait for every shard | One slow shard would otherwise set every query's latency |

**Main interview tradeoff:** **fan-out versus locality.** Document sharding means every query touches every shard of a tier, which makes tail latency and replica cost the central problems, but it keeps scoring local and failure graceful. The design accepts the fan-out and then attacks its cost from three directions: fewer shards per query (tiering), less work per shard (compression, static-rank order, WAND), and less waiting on stragglers (hedging, partial results).

#### Follow-ups with model answers

**Q1. How do phrase queries work?**

First evaluate the query as a conjunction of its terms with WAND to get candidates, then, for the top few hundred candidates per shard, read the position lists of each term for that doc and check that positions are consecutive (`p_new = p_york − 1`). Positions live on NVMe, not RAM, so this verification is limited to candidates. Very common phrases ("new york") can be indexed as bigram terms, trading index size for speed.

**Q2. A major event happens. How fast can a new page appear in results?**

The crawler prioritizes news sources and sitemaps (minutes to fetch), the real-time indexer makes the page searchable in the fresh tier within about a minute of the fetch, and news-intent queries use short result-cache TTLs so cached pages do not hide it. Ranking needs a freshness feature for such queries, because a brand-new page has no links or clicks yet and would lose on static rank.

**Q3. When would term partitioning make sense?**

When the corpus is small enough that posting lists are short, queries are highly selective (rare terms whose lists are tiny to ship), and the cluster is network-rich. Some systems use a hybrid: document-partitioned shards, but a term-partitioned cache of intersections for frequent term pairs. For a 50B-page engine with common-term queries, shipping lists is prohibitive.

**Q4. How do you know a ranking change is better?**

Offline, compute NDCG@10 against human relevance judgments on a fixed query sample, stratified by head, torso, and tail queries. Online, use **interleaving** (merge results from the old and new rankers into one list and see which side's results get clicked), which needs far less traffic than an A/B test, then confirm with an A/B test on longer-term metrics such as abandonment and query reformulation rate.

**Q5. Why not run the whole thing on a general search cluster?**

General engines are document-sharded inverted indexes too, and they are the right choice up to billions of documents. At 50B docs and 200k QPS, the custom parts pay for themselves: static-rank doc ordering, tiering, custom codecs, a deadline-aware aggregation tree with partial results, and an index build pipeline that produces immutable, verified shards. The answer is to state the numbers at which the general tool stops being the cheap option.

#### Level signals

- **Mid:** builds an inverted index, shards it, merges per-shard results, ranks with TF-IDF or BM25, and caches popular queries.
- **Senior:** sizes postings with compression math, chooses document sharding with reasons, uses WAND or tiering to avoid full scans, describes multi-stage ranking, and computes the tail-latency effect of 1,000-way fan-out with hedging and partial results.
- **Staff:** designs the build and swap lifecycle (immutable versions, canaries, rollback, cache warming), the freshness tier with delete bitmaps, global statistics for comparable scores, and evaluation methodology for ranking changes.

See also: [6.10 Web Crawler](../computer-science/High_Level_Design.md#610-web-crawler), [5.7 Tail-Latency Amplification](../computer-science/High_Level_Design.md#57-tail-latency-amplification), [6.9 Search Autocomplete](../computer-science/High_Level_Design.md#69-search-autocomplete-typeahead), [CS 8.8 MapReduce](../computer-science/CS_Fundamentals.md#88-mapreduce).

---

### A19. Email Service (Gmail)

#### Requirements and assumptions

- **Receive** mail from the internet over SMTP for 1.5B accounts; **send** mail to our users and to external domains.
- **Mailbox:** list by label (Inbox, Sent, user labels), conversation threads, read/starred flags, archive, delete, 15 GB quota per user shared with other products.
- **Search** over the user's own mail with operators (`from:`, `to:`, `has:attachment`, `before:`, `label:`).
- **Sync** web, mobile, and third-party IMAP clients with near-real-time push of new mail and flag changes.
- **Spam and malware** filtering, sender authentication (SPF, DKIM, DMARC), and protection against our own users sending spam.
- **Durability:** once we answer `250 OK` to a sending server, the message is never lost. **Latency:** most mail visible in the inbox within a few seconds of acceptance; inbox listing p99 under 200 ms; search p99 under 500 ms.
- **Availability:** reading and sending 99.9%+. Inbound SMTP can tolerate short outages because senders queue and retry for days.
- Out of scope: custom domains and enterprise admin, calendar and chat integration, end-to-end encryption.

#### Capacity estimate

```text
Accounts / DAU:    1.5B / 500M
Inbound delivered: 1.5B × 20/day = 30B/day ≈ 350k/s avg, ~1M/s peak (3×)
SMTP attempts:     ~2× more rejected at connect or RCPT (spam sources, unknown users)
Outbound:          500M × 4 sent/day = 2B/day ≈ 23k/s; ~half to external domains ≈ 12k/s on egress MTAs

Message size:      median ~15 KB, mean ~75 KB (attachments skew it)
Daily ingest:      30B × 75 KB ≈ 2.25 PB/day logical
                   bulk-mail and attachment dedupe + compression ≈ 2× -> ~1.1 PB/day
                   erasure coding at 1.5× -> ~1.7 PB/day of raw disk
Stored mail:       1.5B × ~4 GB average mailbox ≈ 6 EB logical

Metadata:          ~15k messages per mailbox × 1.5B ≈ 2.25e13 messages × ~1 KB ≈ 22 PB (before replication)
Delivery writes:   message row + 2-3 label-index rows + thread + history + quota ≈ 7 row writes/message
                   × 1M/s peak = 7M row writes/s -> ~700 storage nodes at ~10k writes/s each (before replication)
Search index:      ~30% of text; 15k messages × ~4 KB text × 0.3 ≈ 20 MB per user -> ~30 PB total
Client reads:      500M DAU × ~40 API calls/day = 20B/day ≈ 230k/s avg, ~700k/s peak
Push:              ~1B devices registered with mobile push; ~50M IMAP IDLE connections
                   at ~100k connections per server ≈ 500 IMAP front-end servers
```

**What the numbers decide:** cost is dominated by **storage** (exabytes), so bodies and attachments go to erasure-coded object storage with dedupe and cold tiering, and only small metadata goes to the low-latency store. Every user operation touches one user's data, so **partition everything by user**: a delivery, a listing, a search, and a sync are all single-partition. Inbound volume is high but stateless until the durable spool, so MTAs scale horizontally.

#### Interfaces and data

```text
External protocols:  SMTP port 25 (MX ingress), 587 (authenticated submission), IMAP 993
REST API:
  POST /v1/users/me/messages/send   { raw_mime | draft_id, idempotency_key }       -> { msg_id, thread_id }
  GET  /v1/users/me/messages?label=INBOX&page_token=...                          -> [{ msg_id, snippet, ... }]
  GET  /v1/users/me/messages/{id}?format=full|metadata
  POST /v1/users/me/messages/{id}/modify    { add_labels[], remove_labels[] }
  GET  /v1/users/me/messages?q=from:alice has:attachment before:2026/01/01
  GET  /v1/users/me/history?start_history_id=...                                 -> changes[] | 404 (resync)
  POST /v1/users/me/watch           { push_channel }

Metadata store (wide-column, rows keyed by user_id prefix, single-user transactions):
  user(user_id)                              quota_used, next_history_id, settings
  message(user_id, msg_id)                   thread_id, internal_date, header summary, size, labels[],
                                             flags, inline_body (if < 16 KB) | blob_refs[]
  label_index(user_id, label_id, internal_date DESC, msg_id)   -> snippet   (inbox listing = range scan)
  thread(user_id, thread_id)                 msg_ids[], labels union, last_date
  rfc_index(user_id, rfc822_message_id)      msg_id, thread_id   (threading + duplicate delivery check)
  history(user_id, history_id)               change record; retained ~30 days
Blob store (object storage, 6.14): key = SHA-256(content) -> encrypted bytes; reference-tracked for GC
Search index: per-user segments keyed (user_id, segment_id)
```

All rows for a user share the `user_id` prefix, so they are contiguous and usually live in one tablet. Delivery writes the message row, its label-index rows, the thread row, a history row, and the quota counter in **one single-user transaction**, so listings, counts, and sync never disagree. Partitioning by message ID instead would turn every inbox listing into a cross-partition query.

#### Architecture and flow

```text
Internet MTAs --MX--> Ingress MTAs (stateless; TLS; IP reputation; per-IP rate limits;
                      RCPT check: 550 for unknown users; synchronous SPF/DKIM/DMARC + fast spam score)
                         | write to durable spool (replicated across zones), THEN reply 250 OK
                         v
                   Spool queue --> Async filtering: full ML spam model, attachment malware scan,
                                   URL reputation, per-user filters and blocks
                         v
                   Delivery service --(single-user txn)--> Metadata store (by user_id)
                         |  \----------------------------> Blob store (content-addressed, EC, tiered)
                         +--> Search indexer (per-user index, async, seconds)
                         +--> Change notifier (user_id, history_id) --> Push gateways:
                                    web sessions, IMAP IDLE servers, mobile push providers

Clients: Web / Mobile --> API front ends --+--> Mailbox service --> metadata store, blob store
         IMAP clients --> IMAP front ends --+    Search service --> per-user index

Outbound: Submission (API / port 587) --> outbound spam check + per-user rate limits
          --> egress queue per destination domain --> Egress MTAs (DKIM sign, IP pools, TLS, retries)
          --> Internet; bounces (DSNs) delivered back to the sender's mailbox
```

**Inbound (write path):**

1. A remote MTA looks up our MX record and connects to an ingress MTA. Connection-level checks (IP reputation, rate limits) reject the worst sources before any data is read.
2. At `RCPT TO`, unknown recipients get `550` immediately, so we never accept mail we would later have to bounce.
3. After `DATA`, the MTA verifies SPF, DKIM, and DMARC and runs a fast spam score. Clear spam is rejected with `550` during the session.
4. The message is written to a spool replicated across zones, and only then does the MTA answer `250 OK`.
5. Async workers run the expensive checks, then the delivery service checks `rfc_index` for a duplicate (senders retry after timeouts), stores the body in the blob store, and commits the single-user transaction.
6. The change notifier publishes `(user_id, history_id)` to the user's connected clients.

**Read path:** listing the inbox is a range scan on `label_index(user_id, INBOX, ...)` for 50 rows, with snippets stored in the index rows, so no blob reads. Opening a message reads the message row and, for large bodies, the blob.

#### Deep dive: SMTP, authentication, and the filtering pipeline

**`250 OK` is a promise.** SMTP is store-and-forward: a sender that gets `4xx` or no answer keeps the message and retries for up to about five days. That gives two useful properties. Short inbound outages lose nothing, and **tempfail is backpressure**: if the spool or a user's partition is overloaded, answering `451` or `421` pushes the queueing back onto senders. The flip side: once we say `250`, we own the message, so durability must come first. Rejecting during the session is also better than bouncing later, because a later bounce goes to a possibly forged sender (backscatter).

**Sender authentication:**

| Mechanism | What it authenticates | How | Where it breaks |
|---|---|---|---|
| SPF | The envelope sender domain (`MAIL FROM`) | DNS TXT record lists IPs allowed to send for the domain | Forwarding: the forwarder's IP is not in the original domain's list |
| DKIM | The signing domain (`d=`) | Signature over chosen headers and a body hash; public key at `selector._domainkey.domain` | Mailing lists that modify the subject or body invalidate the signature |
| DMARC | The visible `From:` domain | Passes if SPF or DKIM passes **and** that domain aligns with `From:`; publishes policy none, quarantine, or reject, plus aggregate reports | Forwarding plus modification breaks both; ARC lets trusted forwarders vouch for original results |

Only DMARC protects the address users actually see. Outbound, we DKIM-sign every message, publish SPF, and use a DMARC `p=reject` policy for our own domain.

**Filtering pipeline, cheap to expensive:**

```text
Stage                    Cost          Decision options
Connection (IP, rDNS)    microseconds  reject connection, rate limit
Envelope (RCPT, SPF)     ~1 ms DNS     550 unknown user, soft signals
Content fast path        ~10 ms        DKIM/DMARC, fast classifier, known-bad hashes -> 550 in session
Full ML model            ~50 ms        sender reputation, text, URLs, user feedback ("report spam")
Attachment malware       100 ms - min  signatures; risky types detonated in a sandbox, attachment held
Per-user rules           ~1 ms         user filters, blocks, contacts whitelist
Outcome: reject in session | quarantine | spam folder | inbox; URLs rewritten for time-of-click checks
```

User "report spam" and "not spam" clicks feed both the global model and per-sender reputation, which is the most valuable signal because spammers adapt content quickly but cannot quickly build reputation.

#### Deep dive: mailbox storage, dedupe, and quota

- **Metadata vs blobs.** Labels, flags, and threads change constantly and are read on every listing, so they live in the low-latency store as small rows. Bodies are immutable and large, so they go to object storage ([6.14](../computer-science/High_Level_Design.md#614-object-storage-s3-like)). Bodies under ~16 KB are stored inline in the message row, which avoids a small-object overhead for the median message.
- **Labels, not folders.** A message has a set of labels. Archive removes `INBOX`; moving to a label adds it. Each label membership is one `label_index` row sorted by date, so any label listing is a range scan, and the change is in the same transaction as the message row.
- **Threads** are assigned at delivery from `In-Reply-To` and `References` headers via `rfc_index`, falling back to normalized subject plus participants within a time window.
- **Attachment dedupe.** A newsletter with a 1 MB image sent to 10M users is 10 TB without dedupe and 1 MB with it. Blobs are keyed by content hash; each message row references the hash. Garbage collection is mark-and-sweep over references rather than reference counts, because a lost decrement would leak and a duplicated one would delete live data. Dedupe across users must not be observable (no "this file already exists" timing), and content keyed by user-specific encryption keys cannot be deduped, so dedupe is limited to service-encrypted bulk content.
- **Tiering.** Most reads hit mail from the last 30 days, so blobs older than about a year move to a cheaper, slower storage class.
- **Quota** is the logical size: `quota_used` is updated in the delivery transaction, and a deduped attachment still counts fully for each recipient. Over quota, inbound gets `552` after a grace period and sending is blocked.

#### Deep dive: search, sync, and hot mailboxes

**Per-user search.** Each user's index is small (~20 MB), so a search reads one user's segments, evaluates terms plus structured filters (labels and dates come from metadata), and sorts by date. There is no fan-out across users, unlike web search, which shards documents from everyone ([A18](#a18-web-search-engine)). Indexing runs a few seconds after delivery; to hide that gap, the query also scans the handful of messages delivered since the last index flush. Segments of inactive users stay on disk; active users' segments are cached.

**Sync with history IDs.** Every change to a mailbox increments the user's `history_id` in the same transaction and writes a history row. Clients store the last `history_id` they processed and call `history?start_history_id=X` to get only the delta; if X is older than the 30-day retention, the server returns 404 and the client does a full resync. Push only says "something changed, history_id = Y":

- **Mobile:** a mobile push message (no content, or a minimal preview), then the app pulls the delta.
- **Web:** a long-lived connection to a push gateway subscribed to the user's channel.
- **IMAP:** IDLE keeps a connection open, and the server sends `EXISTS` and `EXPUNGE` updates. IMAP needs per-label UIDs and `UIDVALIDITY`, maintained in the label index, and `MODSEQ` maps directly to `history_id`.

The fan-out of change events reuses the notification system pattern ([6.11](../computer-science/High_Level_Design.md#611-notification-system)), keyed by `user_id` so all of a user's devices are reached from one subscription.

**Hot and huge mailboxes.** A mailbox with 2M messages still lists in O(page) because of the sorted label index, and unread counts are maintained counters, never computed by scanning. A mail bomb (thousands of messages per second to one user) is capped by a **per-recipient inbound rate limit** that answers `451` tempfail, pushing the load back to senders. Shared role addresses with very high volume (`support@`) are throttled by batching their deliveries into group commits. The storage layer splits very large users' row ranges across tablets, at the cost of transactions spanning tablets for those users only.

#### Deep dive: outbound deliverability

Other providers judge our mail by the **reputation of the sending IP and the DKIM domain**. Protect it:

- **IP pools:** separate pools for user mail, transactional system mail, and anything bulk, so one class cannot damage the others.
- **IP warming:** a new IP starts at about 2,000 messages per day to each major provider and doubles daily while bounce rates stay under ~2% and complaint rates under ~0.1%. It reaches ~1M/day in about 9 days (2,000 × 2^9 ≈ 1M).
- **Per-destination queues** respect each provider's rate limits and back off on `421` and `4xx` responses; permanent `5xx` failures generate a bounce to the sender and add the address to a suppression list.
- **Contain compromised accounts:** per-user limits (for example 500 external recipients per day for consumer accounts), outbound spam scoring, and anomaly detection on sudden volume or new-recipient bursts.

#### Failure modes and mitigations

| Failure | Impact | Mitigation |
|---|---|---|
| Async filter or delivery backlog | Delayed mail, spool grows | Spool is durable; autoscale workers; near capacity, answer `451` so senders queue |
| Metadata partition unavailable | Deliveries and reads fail for some users | Deliveries stay in the spool and retry; reads served from replicas read-only |
| Sender retries after a lost `250` | Duplicate messages | Dedupe via `rfc_index` and body hash per user before commit |
| Malware found after `250` | Cannot reject anymore | Quarantine or strip the attachment and notify; never bounce to a likely forged sender |
| Our egress IP gets blocklisted | Outbound mail to a provider rejected | Shift traffic to clean pools, find the compromised accounts, request delisting |
| Push provider outage | Clients miss real-time updates | Clients poll `history` on app open and periodically; no data loss |
| Blob store region outage | Old message bodies unreadable | Cross-region replication of blobs; metadata and snippets still list |

#### Tradeoffs

| Decision | Chosen | Alternative | Why |
|---|---|---|---|
| Partition key | `user_id` for all mailbox data | Hash of message ID | Every operation is single-user; listing and sync become single-partition |
| Body storage | Object storage, inline if < 16 KB | All in the metadata store | Exabytes of immutable data belong on erasure-coded, tiered storage |
| When to filter | Cheap checks in session, expensive ones after `250` | Everything after `250` | Rejecting in session avoids backscatter and wasted storage |
| Search | Per-user index | One global index | Queries never cross users; indexes are small and follow the mailbox |
| Sync | History IDs + content-free push | Push full messages | Push providers are lossy; the history log makes missed pushes harmless |
| Dedupe | Content-addressed blobs for bulk content | No dedupe, or per-user encrypted only | Large savings on newsletters; privacy limits where it applies |

**Main interview tradeoff:** **accept fast versus filter thoroughly.** Every millisecond of checks during the SMTP session holds a connection open at 1M messages/s, but every message accepted is one we must store and can no longer reject. The design does the cheap, high-confidence checks in session, takes durable ownership with `250`, and does expensive analysis afterwards with quarantine as the fallback.

#### Follow-ups with model answers

**Q1. Why is a 10-minute inbound outage acceptable, but not a 10-minute read outage?**

Inbound SMTP has retry built into the protocol: sending servers keep the message and retry with backoff for days, so mail arrives late but intact. Reading has no such buffer: a user who cannot open mail sees an outage immediately. That is why inbound can shed load with `4xx` responses while the read path needs replicas and degradation modes (serve cached listings, disable search before disabling reading).

**Q2. How would you implement "undo send" and scheduled send?**

Undo send holds the message in the outbound queue with a `not_before` time 5 to 30 seconds in the future; undo deletes it from the queue before an egress worker picks it up. Scheduled send is the same with a longer delay, stored durably in a time-indexed queue (a distributed job scheduler pattern), with the message already in the user's Sent label marked "scheduled".

**Q3. One of our users sends a message to a 50,000-member internal mailing list.**

Store the body once in the blob store, then fan out delivery jobs per recipient partition, batching recipients that share a storage tablet. Each recipient gets their own metadata rows (their own labels, read state, and thread). The 50,000 writes spread across partitions, and a per-sender fan-out budget prevents one list from starving normal delivery.

**Q4. How do you move a user's mailbox to another region?**

Copy metadata in the background while recording the history ID at which the copy started, then replay history rows from that point until the copy is within seconds. Briefly pause writes for that user (inbound waits in the spool, which is free under SMTP semantics), apply the last changes, flip the user's home-region pointer, and resume. Blobs can stay where they are and be migrated lazily, because they are immutable and content-addressed.

**Q5. What does "report spam" actually change?**

It moves the message to Spam for that user immediately, adds a strong negative signal to the sender's domain and IP reputation and to the content features in the global model, and can create an implicit per-user rule. Reputation updates are aggregated across users and decay over time, so one user cannot block a legitimate sender for everyone.

#### Level signals

- **Mid:** MTAs, a message store, a mailbox database, and a search index; knows SMTP and IMAP exist; estimates storage.
- **Senior:** partitions by user with single-user transactions, splits blobs from metadata with dedupe, explains `250 OK` durability and in-session rejection, explains SPF, DKIM, and DMARC correctly, and designs history-ID sync with push hints.
- **Staff:** treats storage cost and deliverability reputation as first-class constraints, uses SMTP tempfail as backpressure, handles mail bombs and compromised senders, and plans mailbox migration and tiering at exabyte scale.

See also: [6.14 Object Storage](../computer-science/High_Level_Design.md#614-object-storage-s3-like), [6.11 Notification System](../computer-science/High_Level_Design.md#611-notification-system), [6.12 Distributed Job Scheduler](../computer-science/High_Level_Design.md#612-distributed-job-scheduler).

---

### A20. Food Delivery Platform (DoorDash)

#### Requirements and assumptions

- **Customers** browse and search stores and menus near them, get a delivery fee and ETA quote, check out, pay, and track the order live.
- **Merchants** receive orders on a tablet or through a POS integration, confirm or reject, and mark food ready; they can pause the store or mark items out of stock.
- **Dashers** (couriers) go online, receive offers, accept or decline, pick up, and deliver. One Dasher may carry 2-3 orders when routes align.
- **Correctness:** never send an unpaid order to a merchant, never charge twice, never assign one order to two Dashers at once, and every paid order is either delivered or refunded.
- **Scale:** 10M orders/day, dinner peak hour ~15% of daily orders; 500k Dashers online at peak; 700k merchants; 50M DAU.
- **Latency:** store list and search p99 under 300 ms; checkout p99 under 1 s; live location on the customer's map within ~5 s of the Dasher's position.
- Out of scope: scheduled orders, grocery picking, Dasher payouts and tax, merchant onboarding. The object-level design of orders, carts, and state is the LLD version: [LLD: Food Delivery App](LLD_Practice_Problems.md#a2-food-delivery-app).

#### Capacity estimate

```text
Orders:          10M/day ÷ 86,400 ≈ 116/s avg; dinner hour ≈ 15% × 10M = 1.5M/h ≈ 420/s
Order writes:    ~15 transitions + payment + outbox rows ≈ 30 row writes/order -> 420 × 30 ≈ 12.6k writes/s peak
In flight:       Little's law: 420/s × 2,700 s (45 min order-to-door) ≈ 1.1M active orders at peak

Dasher GPS:      500k online × 1 update / 4 s = 125k updates/s × ~100 B ≈ 12.5 MB/s
                 idle Dashers at 1 per 15 s would cut this by about half
Tracking push:   ~half of active orders watched: 550k ÷ 4 s ≈ 140k pushes/s
Connections:     500k Dashers + ~550k watching customers ≈ 1M persistent connections
                 at ~200k per gateway node ≈ 5 nodes + headroom per region
Location history: 250k avg online × 86,400 ÷ 4 ≈ 5.4B points/day × 100 B ≈ 540 GB/day

Dispatch (largest market ≈ 5% of orders): 21 new orders/s
                 batch every 20 s -> ~420 new + ~600 deferred = ~1,000 open orders, ~3,000 nearby Dashers
                 prune to ~30 candidate Dashers per order -> ~30k (order, Dasher) cost cells per batch
                 each cell needs an ETA -> 30k ETAs per 20 s ≈ 1.5k ETA lookups/s per market

Browse:          50M DAU × 30 requests/day ≈ 1.5B/day ≈ 17k/s avg, ~60k/s at dinner
Catalog:         700k merchants × ~150 items × ~2 KB ≈ 210 GB -> fits a modest search cluster
```

**What the numbers decide:** orders are only hundreds per second, so the order database is not the bottleneck: **correctness across services** is the hard part (saga, idempotency, conditional transitions). The heaviest flows are GPS ingest (125k/s) and tracking pushes (140k/s), which get their own path, as in ride-sharing. Dispatch is **compute-bound per market**, not QPS-bound, so it is partitioned by market and run as a periodic batch optimization.

#### Interfaces and data

```text
Customer:  GET  /v1/stores?lat=..&lng=..&q=..                  -> stores with fee, ETA range
           POST /v1/quotes   { cart, address }                 -> { quote_id, items_total, fee, eta, expires_at }
           POST /v1/orders   { quote_id, payment_method, idempotency_key } -> { order_id, status }
           POST /v1/orders/{id}/cancel
           WS   /v1/orders/{id}/track                          -> status changes, Dasher location every ~4 s
Merchant:  POST /v1/merchant/orders/{id}/confirm { prep_minutes } | /reject | /ready
           PUT  /v1/merchant/items/{id}/availability
Dasher:    WS   /v1/dasher/stream   (location up; offers down)
           POST /v1/offers/{id}/accept | /decline
           POST /v1/deliveries/{id}/pickup | /dropoff  { proof }

order(order_id PK, customer_id, store_id, quote_id, state, version, amounts in cents, payment_id,
      idempotency_key, UNIQUE(customer_id, idempotency_key), created_at)    -- sharded by order_id
delivery(delivery_id PK, order_id UNIQUE, market_id, state, dasher_id NULL, assignment_version,
         predicted_ready_at, promised_at)                                    -- sharded by market_id
outbox(event_id, aggregate_id, type, payload, created_at)                    -- same DB as its aggregate
dasher_live(dasher_id -> market, lat, lng, ts, status, active_delivery_ids)  -- in-memory geo index
menu(store_id, item_id, name, price_cents, available, ...)                   -- source of truth; CDC to search
```

**Order** (what the customer bought and paid for) and **delivery** (who carries it and when) are separate aggregates with separate state machines. They change for different reasons at different rates: a delivery can be reassigned three times while the order stays `CONFIRMED`. Orders are sharded by `order_id`; deliveries by `market_id`, so a market's dispatcher reads and writes one shard.

#### Architecture and flow

```text
Customer app --> API gateway --> Store/Search service (geo filter, ranking) <-- CDC <-- Menu DB
                       |
                       +--> Quote service (fee, ETA; dynamic pricing per zone) --> quote cache
                       +--> Order service (saga orchestrator) --> Order DB + outbox
                                 |   ^                                   |
                    authorize/   |   | replies (events)                  v
                    capture      v   |                           Event bus (keyed by order_id)
                          Payment service (6.7)    Merchant service --> tablet / POS
                                                   Dispatch service (per market) --> Delivery DB + outbox
                                                         ^       |
                                                         |       +--> offers --> Dasher gateway
Dasher app --> Dasher gateway (persistent conns) --> Location stream (key = dasher_id)
                                                         |--> Live geo index per market (dispatch, ETA)
                                                         |--> Tracking fan-out --> customer WS
                                                         +--> History (object storage) --> ETA training
ETA service: prep-time model + routing engine with live traffic (used by quote, search, dispatch)
```

**Checkout (write path):**

1. The client sends `POST /orders` with a `quote_id` (fee and prices locked for ~10 minutes) and an idempotency key. A retry with the same key returns the same order.
2. The order service inserts the order as `PENDING_PAYMENT` and calls the payment service to **authorize** the total, using `order_id` as the payment idempotency key.
3. On success it runs `UPDATE order SET state='AUTHORIZED' WHERE order_id=? AND state='PENDING_PAYMENT'` and writes an `OrderPlaced` outbox row in the same transaction.
4. The outbox relay publishes the event. The merchant service pushes the order to the tablet; the dispatch service creates a delivery in `UNASSIGNED`.
5. Merchant confirmation, Dasher assignment, pickup, and drop-off arrive as events that move each state machine with conditional updates. On drop-off, the order service **captures** the final amount (tip and substitutions adjusted, never above the authorization without a new one).

**Tracking (read path):** the customer's WebSocket subscribes to the order's channel. Status events come from the event bus; location points for the assigned Dasher come from the location stream, filtered to the subscribed orders.

#### Deep dive: order saga and payment consistency

There is no distributed transaction across payment, merchant, and dispatch. The order service orchestrates a saga ([CS 8.5](../computer-science/CS_Fundamentals.md#85-distributed-transactions)): it stores the saga's progress in the order row, sends each command through the transactional outbox ([4.12](../computer-science/High_Level_Design.md#412-change-data-capture-event-sourcing-cqrs-and-the-outbox)), and consumes replies idempotently.

```text
Order states:    PENDING_PAYMENT -> AUTHORIZED -> SENT_TO_MERCHANT -> CONFIRMED -> PICKED_UP
                 -> DELIVERED -> COMPLETED (captured)
                 side exits: PAYMENT_FAILED; CANCELED (with compensations below)
Delivery states: UNASSIGNED -> OFFERED -> ASSIGNED -> AT_STORE -> PICKED_UP -> DELIVERED
                 OFFERED -> UNASSIGNED on decline or offer timeout (30-60 s)
                 ASSIGNED -> UNASSIGNED if the Dasher drops the order before pickup

Step  Service    Action                                       Compensation
1     Order      create PENDING_PAYMENT, lock quote           mark CANCELED
2     Payment    authorize total (key = order_id)             void authorization
3     Merchant   send order, wait for confirm (timeout 5 min) send cancel; pay merchant if already cooking
4     Dispatch   create delivery, assign Dasher               unassign; pay Dasher a cancel fee if en route
5     Payment    capture final amount at drop-off             refund (full or partial)
```

Rules that make it correct:

- **Every transition is a conditional update** on the expected state and version. A duplicate or late event (the merchant's "confirm" arriving after the order timed out and was canceled) affects 0 rows and is logged, not applied.
- **The merchant only ever sees authorized orders**, because the only path to the merchant command is the outbox row written with the `AUTHORIZED` transition.
- **Crash between authorize and the state update:** a reconciler scans orders in `PENDING_PAYMENT` older than a minute and asks the payment service for the result by idempotency key, then completes the transition or voids the authorization. No order is left charged but invisible.
- **Timeouts are durable timers** (a scheduled event per saga step), not in-memory sleeps, so a restarted orchestrator still cancels an order the merchant never confirmed.
- **Authorize, then capture** keeps the money safe across a long, failure-prone flow: canceling before pickup is a void (no money moved), and the final amount can differ from the quote.

#### Deep dive: dispatch as batched matching

**Why it differs from ride-sharing ([6.6](../computer-science/High_Level_Design.md#66-ride-sharing-service)):**

| | Ride-sharing | Food delivery |
|---|---|---|
| Who waits | Rider at the curb: match within seconds | Food needs 10-30 min to cook: assignment can wait and batch |
| Parties | Rider, driver | Customer, merchant, Dasher; merchant prep time is uncertain |
| Capacity | One trip per driver (pooling aside) | Stacking 2-3 orders per Dasher is common |
| Objective | Minimize pickup ETA | Dasher arrives as food becomes ready; minimize lateness and food wait |

**Greedy is myopic.** Assigning each order on arrival to its nearest free Dasher ignores the next order:

```text
Minutes from Dasher to store:      Order A   Order B
                     Dasher X         2         3
                     Dasher Y         4        10
Greedy (A arrives first, takes X):  A->X 2 + B->Y 10 = 12 minutes
Batched optimum:                    A->Y 4 + B->X 3  =  7 minutes
```

**Batch every ~20 s per market.** Collect open orders (including ones deliberately deferred) and available Dashers (idle, or finishing a delivery soon near the store), then solve a min-cost assignment. Cost of giving order (or bundle) o to Dasher d:

```text
t_arrive = now + ETA(d -> store)          t_ready = predicted food-ready time
t_pickup = max(t_arrive, t_ready)
cost = w_late × max(0, t_pickup + drive(store -> customer) + handoff − promised_time)
     + w_food × max(0, t_arrive − t_ready)        food sits and gets cold
     + w_idle × max(0, t_ready − t_arrive)        Dasher waits at the counter
     + w_dist × extra driving distance
     − w_acc  × log P(d accepts o)                 learned from offer history
Defer o if even the best t_arrive is far earlier than t_ready (keep Dashers flexible), unless supply is scarce.
```

**Solving it.** A dense Hungarian solve on 1,000 × 3,000 is about 10^10 operations, too slow for a 20 s cycle. Pruning to ~30 candidates per order leaves a sparse graph of ~30k edges, which min-cost flow solves in tens of milliseconds. **Bundles** (two orders from the same or adjacent stores with compatible ready times and drop-offs in the same direction) are added as extra columns with their own cost, under the constraint that each order is covered at most once; that becomes a small set-partitioning problem solved with a MIP solver or a heuristic within the time budget.

**After solving,** the dispatcher sends offers and records `OFFERED` with an `assignment_version`. Accept is a conditional update (`WHERE state='OFFERED' AND dasher_id=? AND assignment_version=?`), so a late accept for an offer that already timed out fails cleanly. Declines and timeouts return the order to the next batch. The batch interval is the main tuning knob: longer batches see more options but delay assignment.

#### Deep dive: ETA, location tracking, search, and pricing

**ETA = prep + travel + handoffs.**

```text
ETA_customer = max(t_arrive_store, t_ready) + store_handoff (parking, finding the bag: ~3-5 min)
             + drive(store -> customer) + dropoff (parking, apartments: ~2-5 min)
```

- **Prep time** is the hardest term. A gradient-boosted model uses store history, hour and weekday, order size and items, the store's current open-order count, and how fast it confirmed. Merchants press "ready" inconsistently, so labels also come from Dasher wait time at the store: a Dasher who arrived and waited 8 minutes shows the food was ready about 8 minutes after arrival.
- **Travel** comes from a routing engine over the road graph with live traffic, corrected by a model trained on actual Dasher trips (the 540 GB/day of location history).
- Show a range (p50 to p80), measure calibration (the share of orders delivered within the range) and late-order rate, and retrain continuously.

**Location ingestion.** Dashers stream GPS over the persistent gateway connection every 4 s on an active delivery and every 15 s when idle. Points go to a log keyed by `dasher_id` (per-Dasher ordering), and three consumers read it: the **live geo index** per market (overwrite latest position, drop points older than the latest, expire after 60 s of silence; [4.8](../computer-science/High_Level_Design.md#48-geospatial-indexing)), the **tracking fan-out** that forwards points only for Dashers with watched orders, and the **history writer** to object storage.

**Store and menu search.** The menu DB is the source of truth; CDC streams changes into a search index so an "out of stock" toggle is searchable within seconds. A query first filters by delivery zone (stores whose zone contains the customer, typically 1-5k), then ranks by text relevance, predicted ETA, rating, price, and personalization. Store list pages for a geohash cell are cacheable for ~30 s; ETA and fee are attached per request from the quote path.

**Dynamic delivery fees.** Every minute, per H3 hexagon zone, compare demand (open orders plus a 30-minute forecast) to supply (idle Dashers plus those finishing soon, weighted by time to free). When supply is short, raise the customer delivery fee and offer Dasher pay boosts, with smoothing and caps so prices do not oscillate. The fee shown is bound to a `quote_id` that the order references, so the charged amount always equals the shown amount even if the zone price changes during checkout.

#### Failure modes and mitigations

| Failure | Impact | Mitigation |
|---|---|---|
| Payment provider timeout during authorize | Order stuck in `PENDING_PAYMENT` | Reconciler queries by idempotency key, completes or voids; the client polls the order status |
| Merchant tablet offline | Order never confirmed | Fallback phone call (IVR) after ~2 min; auto-cancel and void at 5-8 min; pause the store in search |
| Dasher goes offline after accepting | Food sits, order late | No location for 60 s -> alert Dasher; before pickup, unassign and re-dispatch with priority |
| Dispatch process for a market crashes | No new assignments in that market | Standby takes over; state rebuilt from the delivery DB and live index; greedy fallback if the solver misses its deadline |
| Location stream lag | Stale positions, bad assignments | Ignore points older than 30 s for dispatch; widen ETA ranges; alert on consumer lag |
| Outbox relay stalls | Merchants and dispatch do not hear of new orders | Alert on age of oldest unpublished outbox row; it is the key health metric |
| Duplicate or reordered events | Double transitions | Conditional updates on state and version; consumers dedupe by `event_id` |

#### Tradeoffs

| Decision | Chosen | Alternative | Why |
|---|---|---|---|
| Cross-service consistency | Orchestrated saga + outbox | Distributed transaction (2PC) | Payment providers and tablets cannot join a 2PC; compensations are natural here |
| Dispatch | Batched min-cost matching every ~20 s | Greedy on order arrival | Better global cost and bundling; food prep time makes the delay free |
| Aggregates | Separate order and delivery | One order record with everything | Different lifecycles; reassignment does not touch payment state |
| Payment | Authorize at checkout, capture at delivery | Charge at checkout | Cancellations become voids, and final amounts can change |
| Location path | Dedicated stream + in-memory geo index | Writes to the order DB | 125k/s of overwrite-heavy, short-lived data does not belong in the transactional store |
| Fee pricing | Per-zone dynamic, locked by quote | Flat fees | Balances supply and demand at peaks; quote lock keeps the charge honest |

**Main interview tradeoff:** **global optimality versus responsiveness.** Longer dispatch batches and deferred assignments let the optimizer bundle orders and time arrivals to food readiness, lowering cost per delivery, but they delay offers, and a wrong prep-time prediction turns a deferral into a late order. Short batches and greedy assignment are predictable but waste Dasher time. The batch interval and deferral threshold are tuned per market with experiments, and the prep-time model quality determines how aggressive deferral can be.

#### Follow-ups with model answers

**Q1. The customer cancels after the merchant started cooking.**

Policy decides who pays, the saga decides how. Before merchant confirmation, the cancel is a void: no charge. After confirmation, the order service runs compensations: cancel to the merchant (who is paid for food already made), unassign the Dasher (with a cancel fee if en route), and capture a partial amount from the authorization instead of voiding it. Each compensation is idempotent and keyed by order ID so retries are safe.

**Q2. How do you pick the batch interval?**

Simulate and experiment. Replay a day of orders and Dasher positions through the dispatcher with intervals of 5, 10, 20, and 40 s and measure delivery time, lateness, Dasher utilization, and food wait. Longer intervals help in dense markets with many simultaneous orders; in sparse markets there is little to optimize and the delay only hurts, so the interval is per market and can shorten during low load.

**Q3. How do you A/B test a dispatch change when all orders share the same Dashers?**

Splitting customers 50/50 is biased: treatment orders compete with control orders for the same Dashers, so the groups interfere. Use **switchback experiments**: randomize the algorithm by (market, time window), for example 30-minute windows, so each window runs one algorithm on the whole marketplace, then compare windows with matched time-of-day and day-of-week. Simulation runs first, to catch regressions before real orders are affected.

**Q4. A popular restaurant gets 300 orders in 20 minutes during a promotion.**

Prep time explodes, and the prep model's "current open orders" feature must reflect it, otherwise Dashers arrive far too early and crowd the store. Throttle at ordering time: the store service raises the quoted ETA and, past a capacity threshold, pauses new orders for that store. Dispatch should bundle orders from that store aggressively, because several are ready at the same time.

**Q5. Why not reuse the ride-sharing matching service as is?**

The location ingest, geo index, and offer and accept mechanics can be shared, and should be. The matching objective cannot: ride-sharing minimizes pickup time for a waiting rider, while delivery must time the Dasher's arrival to an uncertain food-ready time, consider bundling, and trade lateness against food wait. Share the infrastructure, keep the optimizer separate.

#### Level signals

- **Mid:** order, merchant, and Dasher services; order states; nearest-Dasher assignment; GPS updates to a location store; payment at checkout.
- **Senior:** separates order and delivery aggregates, runs an orchestrated saga with outbox and conditional transitions, uses authorize-then-capture, designs batched matching with an ETA-based cost and shows why greedy loses, and derives location and tracking rates.
- **Staff:** models prep-time uncertainty and deferral, bundling as set partitioning, quote-locked dynamic pricing, and switchback experiments for marketplace changes; knows which parts to share with ride-sharing and which to keep separate.

See also: [6.6 Ride-Sharing Service](../computer-science/High_Level_Design.md#66-ride-sharing-service), [4.12 CDC, Event Sourcing, CQRS, and the Outbox](../computer-science/High_Level_Design.md#412-change-data-capture-event-sourcing-cqrs-and-the-outbox), [6.7 Payment Processing](../computer-science/High_Level_Design.md#67-payment-processing), [LLD: Food Delivery App](LLD_Practice_Problems.md#a2-food-delivery-app).
