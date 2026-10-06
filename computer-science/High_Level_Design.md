# High Level Design -- System Design Interview Reference

> A progressive, vendor-neutral guide to designing distributed systems in technical interviews. It starts with the interview process and core architecture building blocks, then applies them to seven common system design problems. Complements the system design overview in [CS Fundamentals](CS_Fundamentals.md#5-system-design).

## Table of Contents

1. [What High Level Design Covers](#1-what-high-level-design-covers)
2. [A Repeatable Interview Process](#2-a-repeatable-interview-process)
3. [Estimate the Workload](#3-estimate-the-workload)
4. [Architecture Building Blocks](#4-architecture-building-blocks)
5. [Cross-Cutting Design Decisions](#5-cross-cutting-design-decisions)
6. [Worked System Designs](#6-worked-system-designs)
   - [URL Shortener](#61-url-shortener)
   - [Rate Limiter](#62-rate-limiter)
   - [News Feed](#63-news-feed)
   - [Chat System](#64-chat-system)
   - [Video Streaming Platform](#65-video-streaming-platform)
   - [Ride-Sharing Service](#66-ride-sharing-service)
   - [Payment Processing](#67-payment-processing)
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

Assume 10 million new links per day and 100 reads per created link per day. That is roughly 100 million redirects/day, or about 1,200 average reads/second. With a 5× peak, design for roughly 6,000 reads/second. This read-heavy profile supports a cache in front of a key-value lookup. It does not, by itself, require a complex microservice architecture.

### What estimates should influence

- **High read repetition:** consider a cache or CDN, while defining staleness and invalidation behavior.
- **Large object payloads:** keep blobs in object storage and metadata in a database.
- **High write rate:** inspect partition keys, batching, append-oriented storage, and asynchronous work.
- **Global users:** consider regional placement, replication lag, and how writes are routed.
- **Long retention:** include lifecycle, archival, and deletion costs in the design.

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

### 5.5 Common tradeoff pairs

| Choice | Benefits | Costs |
|---|---|---|
| Monolith vs microservices | Simpler deployment and in-process calls vs independent ownership and scaling | Coupling and release coordination vs network failures and operational overhead |
| Synchronous vs asynchronous | Immediate result and simpler flow vs lower coupling and burst absorption | Caller latency and dependency coupling vs delayed completion and retry complexity |
| Normalize vs denormalize | Fewer duplicate facts and simpler updates vs simpler reads at scale | More joins vs more storage and consistency work on updates |
| Push vs pull | Low delivery latency vs fewer background deliveries | Fan-out cost and connection state vs polling load and freshness delay |
| One region vs multiple regions | Simpler consistency and operations vs lower geographic latency and regional resilience | Regional failure exposure vs replication conflicts and failover complexity |

---

## 6. Worked System Designs

Each design follows the same outline: requirements, interfaces and data, architecture and flows, then scaling and failure concerns. Treat the numbers as example assumptions, not facts about a particular company.

### 6.1 URL Shortener

#### Requirements and assumptions

- Create a short link for a long URL and redirect when the short link is opened.
- Reads greatly outnumber writes; links may optionally expire or be disabled.
- Redirects should be fast, and the short key must be unique.
- Click analytics can be eventually consistent.

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

1. Design a collaborative document editor with concurrent updates and offline clients.
2. Design a search autocomplete service for a large product catalog.
3. Design a notification platform that sends email, push, and SMS with user preferences.
4. Design a photo-sharing application with albums, privacy controls, and image processing.
5. Design a distributed job scheduler with recurring jobs, retries, and worker health checks.
6. Design a metrics ingestion and alerting platform with high write volume and time-based queries.

After drawing a design, explain one alternative, one failure scenario, and the metric that would tell you the system is approaching its limit.

