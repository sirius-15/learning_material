# HLD Mock Interviews -- Comprehensive Self-Mock Scripts, Rubrics, and Practice Prompts

> Last reviewed: 2026-11 · Versions assumed: vendor-neutral building blocks (Redis, Kafka-style logs, and PostgreSQL are named only where a concrete mechanism helps); GPU numbers are AMD Instinct MI300X public datasheet values as tabulated in [ML Systems Design §3.1](../ml-gpu/ML_Systems_Design.md#31-accelerators); GPU telemetry concepts use ROCprofiler-SDK (`rocprofv3`), rocprof-compute, and `amd-smi`.

This file is for **practicing** system design interviews, not for learning designs from scratch. The worked designs live in [High Level Design](../computer-science/High_Level_Design.md#6-worked-system-designs) and [ML and HPC Systems Design](../ml-gpu/ML_Systems_Design.md). This file supplies the *interview* around them: a timed self-mock procedure, a rubric that says what mid, senior, and staff answers sound like, ten full mock scripts with the follow-up questions interviewers actually ask, twenty unsolved prompts with hint outlines, and a checklist of the mistakes that sink candidates.

See also: [HLD: A Repeatable Interview Process](../computer-science/High_Level_Design.md#2-a-repeatable-interview-process) · [ML/HPC design framework](../ml-gpu/ML_Systems_Design.md#2-a-framework-for-ml-and-hpc-design-interviews) · [Fermi Estimation](../computer-science/Math_Probability_Estimation.md#9-fermi-estimation) · [Virtual Whiteboarding for Design Rounds](../career/Interview_Loops_and_Logistics.md#12-virtual-whiteboarding-for-design-rounds) · [Night-Before Cheat Sheet](Night_Before_Cheat_Sheet.md)

## Table of Contents

1. [How to Use This File](#1-how-to-use-this-file)
2. [Running a 45-Minute Self-Mock](#2-running-a-45-minute-self-mock)
   - [2.1 Setup](#21-setup)
   - [2.2 Timer Checkpoints](#22-timer-checkpoints)
   - [2.3 A Prompt Randomizer](#23-a-prompt-randomizer)
   - [2.4 Running a Partner Mock](#24-running-a-partner-mock)
   - [2.5 Post-Mock Review and Error Log](#25-post-mock-review-and-error-log)
   - [2.6 Interview Questions](#26-interview-questions)
3. [Evaluation Rubric by Level](#3-evaluation-rubric-by-level)
   - [3.1 What Changes Between Levels](#31-what-changes-between-levels)
   - [3.2 Requirements](#32-requirements)
   - [3.3 Estimation](#33-estimation)
   - [3.4 High-Level Design](#34-high-level-design)
   - [3.5 Deep Dives](#35-deep-dives)
   - [3.6 Tradeoffs](#36-tradeoffs)
   - [3.7 Communication](#37-communication)
   - [3.8 Scoring Sheet](#38-scoring-sheet)
   - [3.9 Interview Questions](#39-interview-questions)
4. [Mock 1: URL Shortener](#4-mock-1-url-shortener)
5. [Mock 2: Rate Limiter](#5-mock-2-rate-limiter)
6. [Mock 3: News Feed](#6-mock-3-news-feed)
7. [Mock 4: Chat System](#7-mock-4-chat-system)
8. [Mock 5: Distributed Key-Value Store](#8-mock-5-distributed-key-value-store)
9. [Mock 6: Search Typeahead](#9-mock-6-search-typeahead)
10. [Mock 7: Distributed Job Scheduler](#10-mock-7-distributed-job-scheduler)
11. [Mock 8: Metrics and Monitoring System](#11-mock-8-metrics-and-monitoring-system)
12. [Mock 9: GPU Profiling Telemetry Service](#12-mock-9-gpu-profiling-telemetry-service)
13. [Mock 10: LLM Inference Serving](#13-mock-10-llm-inference-serving)
14. [Twenty Unsolved Practice Prompts](#14-twenty-unsolved-practice-prompts)
15. [Common Failure Modes Checklist](#15-common-failure-modes-checklist)
- [Answers](#answers)

Every mock (sections 4-13) has the same six parts: **Prompt** (what the interviewer says), **Hidden Expectations** (what they are actually grading), **Clarifying Questions** (with the answers a typical interviewer gives), **Model Answer Outline** (time-boxed, with numbers), **Follow-Ups With Model Answers**, and **Level Signals** (what separates mid, senior, and staff on this prompt).

---

## 1. How to Use This File

1. **Do not read a mock before you run it.** Read only the `X.1 Prompt` subsection, run the 45-minute procedure in [section 2](#2-running-a-45-minute-self-mock), and only then open the rest of the mock. Reading the model answer first turns a mock into a reading exercise, and recognition is much easier than recall.
2. **Score yourself with the rubric** in [section 3](#3-evaluation-rubric-by-level) at the level you are interviewing for. Be strict: "I would have said that if asked" scores zero; only what you said counts.
3. **Answer the follow-ups out loud** before reading the model answers. Follow-ups are where most hire/no-hire decisions are made, because they test whether you understand the design or memorized it.
4. **Repeat each mock after 7 days**, then after 21 days. The second attempt should finish the core design by minute 18, leaving more time for deep dives.
5. **Use the worked designs as references, not scripts.** Each mock links to the worked design. When your answer differs from it, decide whether your choice is defensible. Interviewers reward a well-argued different choice over a recited "standard" one.

Suggested order by target role:

| Target role | Start with | Then | Stretch |
|---|---|---|---|
| General big-tech SWE | 1 URL shortener, 2 rate limiter | 3 news feed, 4 chat, 6 typeahead | 5 KV store, 7 job scheduler |
| Systems C++ / infrastructure | 2 rate limiter, 5 KV store | 7 job scheduler, 8 metrics | 4 chat (connection scale) |
| GPU / HPC (AMD, NVIDIA, labs) | 8 metrics, 9 GPU profiling telemetry | 10 LLM serving, 7 job scheduler | 5 KV store |
| ML infrastructure | 10 LLM serving, 7 job scheduler | 8 metrics, 9 telemetry | 6 typeahead (ranking + freshness) |

For the GPU-specific mocks, read [ML Systems Design §3](../ml-gpu/ML_Systems_Design.md#3-numbers-every-ml-systems-engineer-should-know) first so the numbers come out of your mouth without hesitation.

---

## 2. Running a 45-Minute Self-Mock

### 2.1 Setup

- **Tool:** use the whiteboard tool you expect in the real loop (Excalidraw, a shared Google Doc or drawing, the company's own pad, or a physical whiteboard on video). Practicing on paper and interviewing on a laptop costs about five minutes of fumbling. See [Virtual Whiteboarding](../career/Interview_Loops_and_Logistics.md#12-virtual-whiteboarding-for-design-rounds).
- **Recording:** record screen and audio. Listening back is where you discover that you said "um, so basically" forty times or never stated a number.
- **Timer:** a visible countdown, not a stopwatch. Do not pause it.
- **Rules:** no notes, no searching, no AI. Speak continuously, as if an interviewer were listening. If you need to think, say what you are thinking about ("I am deciding between push and pull fan-out; let me compare the write cost").
- **Board layout:** reserve the top-left for requirements and numbers, the center for the diagram, and the right side for APIs, schemas, and the list of open questions. Interviewers re-read the top-left often.

### 2.2 Timer Checkpoints

| Clock | Phase | You are on track if, by the end of the phase... | If you are behind |
|---|---|---|---|
| 0:00-0:05 | Requirements | Functional list (3-5 items), non-functional list (scale, latency, availability, consistency, durability), and an explicit **out of scope** list are written down | Stop asking questions, state assumptions instead: "I will assume X; tell me if that is wrong" |
| 0:05-0:10 | Estimation and API | 3-5 numbers, each followed by "so the design must..."; 3-5 API calls with key semantics (idempotency key, cursor, version) | Drop the API details to one line each; never skip the numbers that drive design |
| 0:10-0:22 | High-level design | One diagram with every box justified; **one write path and one read path walked end to end** | Draw the simplest working version and say "I will scale it next"; do not add a cache or queue you cannot justify yet |
| 0:22-0:37 | Deep dives | 1-2 components designed to the level of data structures, algorithms, schemas, and numbers. If the interviewer chose a topic, that one first | Ask the interviewer: "Which part would you like me to go deeper on?" |
| 0:37-0:42 | Failure and scale | Answers to: a node dies, 10x traffic, hot key, multi-region, dependency slow | Pick the single most dangerous failure and handle it well |
| 0:42-0:45 | Summary | 30-60 s recap: how each requirement is met, biggest remaining risk, what you would build next | Never skip it; it is the last impression |

**Compressed 35-minute version.** Many loops lose 5 minutes to introductions and 5 minutes to your questions at the end. Practice a 35-minute variant too: 4 / 4 / 10 / 10 / 5 / 2 minutes. The order is the same; only the depth changes.

The three biggest time sinks, in order:

1. **Requirements ping-pong** past minute 7: asking question after question without committing. Fix: ask the 4-6 questions that change the architecture (listed in each mock's `X.3`), then state assumptions.
2. **Estimation theatre:** computing storage to three significant figures. Fix: round to one significant figure and say what the number decides.
3. **Drawing every box at once:** 14 boxes at minute 15, none explained. Fix: build the diagram incrementally, from the simplest working system to the scaled one, and narrate why each box appears.

### 2.3 A Prompt Randomizer

Picking your own prompt biases you toward the ones you like. This script picks a mock, prints the checkpoint clock times, and samples hidden follow-ups. A partner (or you, at +30 minutes) reads them out.

```python
"""Pick a random HLD mock prompt and print the timer checkpoints and hidden follow-ups."""
import argparse
import datetime as dt
import random

PROMPTS = {
    "URL shortener": ["Your cache node dies", "A link goes viral: 10x traffic on one key",
                      "Make it multi-region", "Count clicks exactly once"],
    "Rate limiter": ["The counter store is down", "One tenant is a hot key",
                     "Enforce a global quota across 3 regions", "Clients retry on 429"],
    "News feed": ["A celebrity with 100M followers posts", "The timeline cache cluster dies",
                  "Super Bowl: 10x reads", "A post is deleted after fan-out"],
    "Chat": ["A gateway with 200k sockets dies", "Exactly-once delivery?",
             "A group with 100k members", "Users in two regions chat"],
    "Distributed KV store": ["A replica is down during a write", "Network partition",
                             "Hot key at 1M reads/s", "Add 10 nodes without downtime"],
    "Typeahead": ["Trending queries within 5 minutes", "Remove an offensive suggestion now",
                  "Index grows 100x", "10x traffic during a live event"],
    "Distributed job scheduler": ["Scheduler instance dies", "Exactly-once execution?",
                                  "2M jobs due at 00:00", "Worker pauses for 60 s (GC)"],
    "Metrics/monitoring": ["Someone adds a user_id label", "An ingester dies",
                           "Who monitors the monitor?", "p99 across 1,000 hosts"],
    "GPU profiling telemetry": ["Profiler overhead is 15% on a customer job",
                                "Counters need 6 passes", "Detect a 3% regression",
                                "A 16k-GPU job floods the pipeline"],
    "LLM inference serving": ["A GPU node dies mid-stream", "10x traffic spike",
                              "128k-token prompts", "One tenant's system prompt is a hot prefix"],
}

CHECKPOINTS = [  # (minute offset, what must be on the board by then)
    (0, "Start: read the prompt once, then ask clarifying questions"),
    (5, "Functional + non-functional requirements and out-of-scope list written"),
    (10, "3-5 estimates, each with 'so the design must...'; API sketch done"),
    (22, "Full diagram; one write path and one read path walked end to end"),
    (37, "1-2 deep dives finished (interviewer's choice first)"),
    (42, "Failure modes, scaling, follow-ups answered"),
    (45, "Summary: how requirements are met, biggest risk, next step"),
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=None, help="repeatable selection")
    parser.add_argument("--followups", type=int, default=3)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    prompt = rng.choice(sorted(PROMPTS))
    followups = rng.sample(PROMPTS[prompt], k=min(args.followups, len(PROMPTS[prompt])))
    start = dt.datetime.now().replace(second=0, microsecond=0)

    print(f"PROMPT: {prompt}")
    for offset, goal in CHECKPOINTS:
        print(f"  {(start + dt.timedelta(minutes=offset)):%H:%M}  (+{offset:2d} min)  {goal}")
    print("Hidden follow-ups (have a partner read these at +30 min, or reveal them yourself):")
    for i, question in enumerate(followups, 1):
        print(f"  F{i}. {question}")


if __name__ == "__main__":
    main()
```

Run it with `python3 mock_runner.py` (or `--seed 7` to repeat a selection). The full follow-up lists, with model answers, are in each mock's `X.5` subsection.

### 2.4 Running a Partner Mock

If a friend plays interviewer, give them this script:

1. Read the prompt from `X.1` and nothing else. Do not volunteer requirements.
2. Answer clarifying questions with the answers in `X.3`. If the candidate does not ask, do not tell; note the omission.
3. At about minute 20-25, steer to a deep dive from `X.2` ("Let's go deeper on how you assign IDs").
4. From minute 30, ask 3-4 follow-ups from `X.5`. Push once on each answer ("What happens if that also fails?"). A good interviewer asks the second question; a candidate who only prepared the first answer is exposed.
5. Stay neutral. Do not nod at good answers or frown at bad ones; real interviewers often give no signal.
6. Score with [section 3.8](#38-scoring-sheet), then give feedback as **one thing to keep and two things to change**, with timestamps.

### 2.5 Post-Mock Review and Error Log

Immediately after the mock, before looking at the model answer:

1. Write down from memory what you think you covered.
2. Watch the recording at 1.5x speed. Mark the timestamp of each checkpoint and compare it with [the table above](#22-timer-checkpoints).
3. Score yourself with the [scoring sheet](#38-scoring-sheet).
4. Now read `X.2` to `X.6`. For every miss, add one row to an error log.

```text
| Date       | Mock          | What I missed                               | Category      | Fix (one sentence)                                  | Retest  |
|------------|---------------|---------------------------------------------|---------------|-----------------------------------------------------|---------|
| 2026-11-03 | Rate limiter  | Never said fail-open vs fail-closed         | Failure modes | Ask "what if the counter store is down?" every time | 11-10   |
| 2026-11-03 | Rate limiter  | Estimated memory, never said what it decides| Estimation    | Every number ends with "so the design must..."      | 11-10   |
```

After five mocks, count misses by category. The category with the most rows is your next week's focus. Typical patterns: engineers from infrastructure backgrounds miss product requirements and API semantics; engineers from product backgrounds miss failure modes and numbers.

### 2.6 Interview Questions

**Q1. The interviewer interrupts at minute 12 and asks about something you planned to cover at minute 30. Do you stick to your plan?**

No. Follow the interviewer. Their question tells you what they are grading, and the rubric rewards responsiveness more than completeness. Say "Good question, let me answer that now and then come back to the read path," answer it properly, and then resume. Write the deferred item in your open-questions list on the board so neither of you loses it. Ignoring an interruption to finish your script is one of the clearest negative signals in design rounds.

**Q2. Halfway through, you realize your design has a flaw (for example, your partition key creates a hot shard). What do you do?**

Say it out loud immediately: "I want to revisit the partition key. With `created_at` as the key, all writes hit the newest partition. I will switch to `hash(user_id)` and keep `created_at` as a sort key." Self-correction is a strong positive signal at every level, because real design work is iterative. Hiding the flaw and hoping the interviewer does not notice is a negative signal when they do notice, and they usually do.

**Q3. How much estimation is enough?**

Enough to make a decision. Typical decisions: does the data fit on one machine or in memory, is the workload read-heavy or write-heavy, how many servers or GPUs are needed, and is the bottleneck bandwidth, storage, or compute. Three to five numbers, each rounded to one significant figure, each followed by "so...", is the target. If the interviewer says "skip the math," skip it but still state the one or two numbers that drive the design ("this is about 60k reads per second, so a cache is required").

**Q4. The interviewer names a technology you have never used, such as "Would you use Cassandra here?"**

Answer at the level of mechanism, then be honest about experience: "I have not operated Cassandra, but as I understand it, it is a leaderless, LSM-based wide-column store with tunable quorum consistency. For this access pattern, which is a write-heavy append keyed by conversation, that fits. What I would check is how it handles very wide partitions for large groups." Pretending expertise is risky because the next follow-up will expose it.

**Q5. You finish the core design at minute 25 and the interviewer says nothing. What now?**

Drive. Propose the next topic yourself: "The riskiest part of this design is the fan-out for high-follower accounts. I would like to go deeper there unless you prefer something else." Silence is often a deliberate test of whether you can identify what matters without prompting, which is a senior and staff signal.

---

## 3. Evaluation Rubric by Level

Companies phrase their rubrics differently, but almost all of them grade the same six dimensions. The tables below give **concrete, observable signals**: things a note-taking interviewer can write down. "Good communication" is not a signal; "stated the read/write ratio and used it to justify a cache" is. Level names map roughly to Google L4/L5/L6, Meta E4/E5/E6, and Amazon SDE II / Senior / Principal; see [Leveling Equivalences](../career/Interview_Loops_and_Logistics.md#14-leveling-equivalences-across-companies) for details.

### 3.1 What Changes Between Levels

| | Mid | Senior | Staff |
|---|---|---|---|
| Who drives | Interviewer guides; candidate executes well | Candidate drives; interviewer mostly probes | Candidate drives and reframes; interviewer is a peer |
| Scope | A working design for the stated problem | A design that survives scale and failure | The right problem, the right design, and how it evolves and is operated |
| Depth | Correct use of standard components | Depth in 1-2 components, with numbers | Depth where it matters most, and an explanation of why that is where it matters |
| Failure handling | Handles failures when asked | Raises failure modes unprompted | Designs for failure from the start; quantifies blast radius and recovery time |
| Tradeoffs | Can name pros and cons when asked | Compares concrete alternatives against requirements | Ties tradeoffs to cost, team, migration, and long-term operability |

A staff-level candidate is not someone who draws more boxes. It is often someone who draws **fewer** boxes, because they can say which complexity is not yet justified and what would make it justified.

### 3.2 Requirements

| Level | Strong signals | Red flags at this level |
|---|---|---|
| Mid | Lists functional requirements, asks about scale and latency, writes them down; accepts the interviewer's scoping | Starts drawing within the first minute; never asks about scale; requirements exist only in the candidate's head |
| Senior | Separates functional from non-functional; asks the questions that change the architecture (consistency, ordering, durability, read/write ratio); states an explicit out-of-scope list; identifies the one or two requirements that make the problem hard | Asks 15 generic questions without prioritizing; treats every requirement as equally important; misses an implied requirement such as "messages must not be lost" |
| Staff | Reframes when useful ("Is the goal a short-link product or an internal link service? The answer changes abuse handling and analytics"); asks about users, SLOs, cost targets, and existing systems; names which requirements are negotiable and proposes a phased scope | Accepts an ambiguous prompt at face value; never asks who the customer is or what success looks like |

### 3.3 Estimation

| Level | Strong signals | Red flags at this level |
|---|---|---|
| Mid | Computes QPS and storage correctly with stated assumptions (86,400 s/day, peak factor) | Arithmetic errors of 10x or more; numbers computed and then ignored |
| Senior | Picks the numbers that matter (peak QPS, hot set size, fan-out writes, concurrent connections) and ties each to a decision: "6 GB index, so it fits in RAM and every node holds a full copy" | Estimates storage to three digits but never computes peak or fan-out; no "so the design must..." |
| Staff | Finds the binding constraint early (bandwidth, memory, fan-out, burst, GPU-hours, cost); sanity-checks numbers against known per-node capacities; revisits estimates when the design changes | Misses the number that dominates the problem (for example the top-of-hour burst in a scheduler, or KV-cache memory in LLM serving) |

### 3.4 High-Level Design

| Level | Strong signals | Red flags at this level |
|---|---|---|
| Mid | A coherent diagram with clear data flow, a source of truth, and reasonable storage choices; walks a request end to end | Boxes without data flow; "microservices" with no responsibilities; a cache or queue with no stated purpose |
| Senior | Starts simple and evolves; separates the data plane from background paths; names partition keys, idempotency, and ordering; every component is justified by a requirement or number | Over-engineering at minute 10 (Kafka, Kubernetes, and three caches before the first read path works); cannot say what is the source of truth and what is derived |
| Staff | Designs for operability (deployability, observability, migration, config rollout); identifies team or service boundaries; makes the expensive parts optional; explains how the design changes at 10x and 100x | A diagram that is correct but has no evolution story; no mention of how it is deployed, monitored, or migrated |

### 3.5 Deep Dives

| Level | Strong signals | Red flags at this level |
|---|---|---|
| Mid | Can explain one component in detail when asked (for example, a token-bucket algorithm or a schema with indexes) | Answers stay at box level ("the cache handles it") |
| Senior | Goes two levels deep in 1-2 components: data structures, algorithms, concurrency control, failure handling, with numbers; raises race conditions and correctness issues unprompted | Deep dive is a recitation of a known system ("Dynamo does X") without being able to explain why it works for this requirement |
| Staff | Chooses the deep dive that carries the most risk and says why; covers correctness under failure (fencing, idempotency, consistency anomalies), performance under load (tail latency, hot spots), and operational behavior (rebuild time, rollout) | Deep-dives into an easy, safe component while the risky one goes unexamined |

### 3.6 Tradeoffs

| Level | Strong signals | Red flags at this level |
|---|---|---|
| Mid | Names pros and cons of an alternative when asked (SQL vs NoSQL, push vs pull) | Only one option is ever considered; tradeoffs are generic ("NoSQL scales better") |
| Senior | Compares two concrete alternatives against the stated requirements and picks one, saying what would change the decision ("If ordering were global, I would need a single sequencer; it is per conversation, so I partition by conversation") | Says "it depends" without saying on what; picks the fashionable option without reasons |
| Staff | Weighs cost, operational burden, team expertise, reversibility, and time to market; distinguishes one-way-door from two-way-door decisions; states the risk accepted and how to detect it | Optimizes a dimension the business does not care about; cannot say what the design gives up |

### 3.7 Communication

| Level | Strong signals | Red flags at this level |
|---|---|---|
| Mid | Thinks out loud; responds to hints; diagram is legible | Long silences; ignores hints; defensive when challenged |
| Senior | Structures the session (announces phases), checks in at transitions, manages time, summarizes; handles pushback by engaging with the argument | Monologue for 20 minutes without checking in; runs out of time before failure handling |
| Staff | Communicates like a design-review lead: crisp framing, explicit decisions and open questions, invites disagreement, adapts depth to the interviewer's interest; a final summary that a director could act on | Talks down to the interviewer, or cannot explain a deep topic simply |

### 3.8 Scoring Sheet

Score each dimension 1-4: **1** = clear negative signal, **2** = below the level, **3** = meets the level, **4** = above the level. Copy this block into your notes for every mock.

```text
Mock: ____________   Date: ________   Target level: Mid / Senior / Staff   Duration used: __ min

Dimension            Score (1-4)   Evidence (quote or timestamp)
Requirements         ___           ______________________________________________
Estimation           ___           ______________________________________________
High-level design    ___           ______________________________________________
Deep dives           ___           ______________________________________________
Tradeoffs            ___           ______________________________________________
Communication        ___           ______________________________________________

Checkpoints hit:  [ ] 5:00 reqs  [ ] 10:00 numbers  [ ] 22:00 diagram + 2 paths  [ ] 37:00 deep dive  [ ] summary
Follow-ups:       F1 ___/4   F2 ___/4   F3 ___/4
Decision:  Strong no / Lean no / Lean hire / Strong hire
```

A reasonable self-calibration:

- **Lean hire at the target level:** no 1s, at least four 3s, and an average of at least 3.0.
- **Senior:** Deep dives and Tradeoffs must both be 3 or more; a 2 there is usually a down-level to mid even if everything else is strong.
- **Staff:** Requirements and Tradeoffs must both be 3 or more, with at least one 4 somewhere. Staff loops often contain two design rounds; one mediocre round is survivable, two are not.
- **Follow-ups** are weighted heavily in practice. A candidate who scores 4 on the main design but 2 on every follow-up is graded as someone who memorized a design.

### 3.9 Interview Questions

**Q1. Two candidates draw the same diagram. What makes one senior and the other mid?**

The senior candidate arrived there by reasoning from requirements and numbers and can defend every box ("the queue exists because fan-out is 230k writes per second and must not block the post request"). They raised failure modes before being asked, and in the deep dive they reached data structures, concurrency, and recovery details. The mid candidate drew the same boxes because they are the standard answer, and when asked "why a queue?" gives a generic reason. Interviewers grade the reasoning, not the picture.

**Q2. How do you demonstrate staff-level judgment in 45 minutes?**

Make a few deliberate, explained choices about what not to do: "I would not build a custom storage engine here; a managed log plus object storage meets the SLO, and the team's time is better spent on the ingestion limits that actually protect us." Quantify blast radius and recovery time for failures. Mention the operational lifecycle: how the system is rolled out, how config changes ship safely, what the first three dashboards and alerts are, and how you would migrate from the current system. Close with the biggest risk and how you would de-risk it early.

**Q3. Is it bad to say "I don't know"?**

No, if it is followed by reasoning: "I do not know the exact write throughput of that database, but a single primary with NVMe typically sustains on the order of tens of thousands of simple writes per second, so at 100k writes per second I would plan to shard." Interviewers distinguish an unknown fact (fine) from an inability to reason about it (not fine).

**Q4. The interviewer disagrees with your choice. Should you switch?**

Engage with the argument first. If their point exposes a requirement you missed, say so and switch: that is good judgment. If you still think your choice is better, explain why with the requirement it serves, and offer the condition under which their option would win. Switching instantly at every pushback looks like having no opinion; never switching looks like not listening. Interviewers sometimes push back on correct answers to test exactly this.

**Q5. How do GPU/HPC design rounds differ in what they grade?**

The same six dimensions apply, but the estimation dimension carries more weight and must use hardware numbers: FLOPs, HBM capacity and bandwidth, interconnect bandwidth, and failure rates. A strong answer finds the binding resource first ("decode is HBM-bandwidth-bound, so batching is the lever"). See [How ML System Design Differs from Classic HLD](../ml-gpu/ML_Systems_Design.md#1-how-ml-system-design-differs-from-classic-hld).

---

## 4. Mock 1: URL Shortener

Worked design: [HLD §6.1 URL Shortener](../computer-science/High_Level_Design.md#61-url-shortener). Do not reread it before the mock.

### 4.1 Prompt

> "Design a URL shortening service like bit.ly. Users paste a long URL and get a short link; anyone who opens the short link is redirected."

### 4.2 Hidden Expectations

The interviewer expects this to be the "easy" prompt and grades **judgment and precision**, not breadth:

- Recognize it as a **read-heavy key-value lookup** and keep the core design small. Over-engineering is the most common failure.
- **Key generation** done properly: code length derived from key-space math, collision handling, and whether codes are predictable.
- **Caching** of redirects, including what happens when a cache node dies and when one link goes viral (hot key).
- **Analytics off the critical path**, with an explicit statement of how many click events may be lost.
- Senior and above: **multi-region** uniqueness without global coordination, abuse handling, and the 301-vs-302 consequence for analytics.
- Trap: "MD5 the URL and take 7 characters" without addressing collisions, the same URL shortened by two users, or custom aliases.

### 4.3 Clarifying Questions

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| How many new links and redirects per day? | 10M new links/day; 1B redirects/day | Sets the read/write ratio (100:1) and cache need |
| How long are links kept? | 5 years; optional per-link expiry | Sets storage and code length |
| Custom aliases? | Yes, optional | Needs a uniqueness check on user-chosen keys |
| Does the same long URL always map to the same code? | No; each create gets its own code | Avoids a reverse index and lets each user own analytics |
| Analytics required? How fresh and how exact? | Click counts per link, minutes of delay is fine | Async pipeline; defines loss tolerance |
| Global users? Redirect latency target? | Global; redirect under ~20 ms server time | Regional read replicas and caches |
| Can links be private or unlisted? | Not in v1 | If yes, code randomness becomes a security property (see Q5) |

### 4.4 Model Answer Outline

**Requirements (0-5 min).** Functional: create (optionally custom alias, expiry), redirect, per-link click counts. Non-functional: redirect highly available and fast; creates can be slightly slower; codes unique forever; analytics eventually consistent. Out of scope: user accounts UI, link editing, QR codes.

**Estimates (5-10 min).**

```text
Writes:     10M/day ÷ 86,400 ≈ 115/s average, ~600/s peak (5x)         -> one database primary could take this
Reads:      1B/day ≈ 11.6k/s average, ~60k/s peak (5x)                -> cache in front of the store
Storage:    10M/day × 365 × 5 years ≈ 18B links × ~500 B ≈ 9 TB         -> partitioned KV store (27 TB with 3 replicas)
Key space:  base62: 62^6 ≈ 5.7e10, 62^7 ≈ 3.5e12
            18B / 5.7e10 ≈ 32% full with 6 chars -> frequent collisions on random codes late in life
            18B / 3.5e12 ≈ 0.5% full with 7 chars -> ~1 retry per 200 creates             => use 7 characters
Hot set:    ~100M distinct links read per day; top 20% × 500 B ≈ 10 GB -> fits in RAM; shard for throughput only
Bandwidth:  60k/s × ~500 B ≈ 30 MB/s -> not a concern
```

**API (in the same window).**

```text
POST /v1/links   Idempotency-Key: <uuid>   { long_url, custom_alias?, expires_at? }  -> 201 { code, short_url }
GET  /{code}                                -> 302 Location: <long_url>   (404 unknown, 410 expired/disabled)
GET  /v1/links/{code}/stats                 -> { clicks_total, clicks_by_day[] }   (owner only)
```

**High-level design (10-22 min).**

```text
Create:  Client -> LB -> Link API -> code generator -> KV store: PUT IF NOT EXISTS (code -> record)
Read:    Client -> (CDN/edge, optional) -> LB -> Redirect service -> in-process LRU -> cache cluster -> KV store
                                                         \-> async click event -> log -> aggregator -> stats store
```

Walk the read path: redirect service checks a small in-process LRU, then the shared cache, then the store; checks status and expiry; returns 302; emits a click event to a local buffer that is shipped asynchronously. Walk the write path: validate URL (scheme, length, blocklist), generate a code, conditional insert, return.

**Deep dive (22-37 min): key generation.** Compare three options:

| Option | How | Pros | Cons |
|---|---|---|---|
| Random 7-char base62 + conditional insert | `PUT IF NOT EXISTS`; retry on conflict | No coordination; codes not guessable in sequence | Extra round trip on the rare collision; needs a store with conditional writes |
| Counter + base62 | Each API server leases a block of 1M IDs from a ticket service | No collisions; compact | Sequential codes leak volume and are enumerable unless scrambled with a bijective permutation |
| Hash of URL, truncated | `base62(hash(url + salt))[:7]` | Deterministic | Still needs collision handling; same URL from two users needs different codes anyway |

Pick random codes with conditional insert (or leased counter ranges passed through a keyed permutation if the store lacks conditional writes). Custom aliases use the same conditional insert into the same key space, with a reserved-words blocklist.

**Second deep dive if time: caching and redirects.** In-process LRU (tens of thousands of entries, TTL 60 s) absorbs hot keys; shared cache uses consistent hashing; cache entries carry the link's expiry so a cached entry never outlives the link.

**Summary (42-45 min).** "A 100:1 read-heavy KV lookup. 7-character random codes with conditional insert give uniqueness without coordination. Two cache layers absorb 60k/s peak and viral links. Clicks are counted asynchronously with bounded loss. The biggest risk is abuse (malware links), handled by creation rate limits and safe-link scanning."

### 4.5 Follow-Ups With Model Answers

**Q1. One of your cache nodes dies. What happens?**

With consistent hashing over, say, 6 cache nodes, about 1/6 of keys start missing. At 60k reads/s and a 90% hit rate, the store normally sees 6k reads/s; losing one node adds about 60k × 0.9 / 6 = 9k/s, so the store briefly sees ~15k/s, 2.5x normal. The store must be provisioned for that (read replicas), or misses must be dampened: **request coalescing** (singleflight: concurrent misses for the same key wait for one fetch), the in-process LRU on each redirect server (which keeps serving the hottest keys), and a replacement node that refills naturally in minutes. No data is lost because the cache is not the source of truth. The wrong answer is modulo hashing (`hash % N`), which remaps almost every key when N changes and turns one node failure into a full cache flush.

**Q2. A link goes viral: 100k requests per second for one code.**

That is a **hot key**: every request maps to one cache shard, which may top out around 100k ops/s. Mitigations, in order: (1) the per-server in-process LRU means each of ~50 redirect servers fetches the key once per TTL, so the shared cache sees about 50 requests per minute for it; (2) allow the CDN or edge to cache the redirect response for a short time (`Cache-Control: max-age=60`) and feed edge logs into analytics so counts are preserved; (3) if a shared-cache hot key remains, replicate it under `code#1..code#k` and pick a suffix at random. The redirect tier is stateless, so it autoscales.

**Q3. Make it multi-region.**

Reads are easy: each region has a replica of the store and its own caches. Writes need **uniqueness without cross-region coordination**: partition the code space by region (for example, the first character encodes the home region, or each region leases disjoint counter ranges). Replicate asynchronously. The subtle problem is **read-after-create across regions**: a user in Virginia creates a link, posts it, and someone in Frankfurt clicks within a second, before replication. Handle it by treating a miss as "not yet replicated": the redirect service decodes the home region from the code and queries that region before returning 404. If a region fails, its links remain readable from replicas elsewhere, and new creates move to a surviving region with its own prefix.

**Q4. Product wants click counts to be exact. Can you do exactly-once?**

First define a click (bots? repeated clicks by the same user?). Exactly-once delivery over a network is not achievable, but **effectively-once processing** is: give every click event a unique ID at the redirect server, deliver at least once, and make aggregation idempotent by deduplicating on event ID within a bounded window (keyed state with a TTL longer than the maximum redelivery delay). The remaining loss is events buffered on a redirect server that crashes before shipping. Closing that gap means writing the event to a durable log before responding, which adds a few milliseconds to every redirect. Usually the right answer is "exact enough": bounded loss well under 0.1%, stated in the product contract. For unique visitors, use HyperLogLog (about 12 KB per counter for roughly 0.8% standard error) instead of storing visitor sets.

**Q5. Someone uses the service to spread malware, or to enumerate links.**

Malware: per-account and per-IP creation rate limits, synchronous checks against a blocklist, asynchronous scanning against a safe-browsing service, and an interstitial warning or disable flag at redirect time (cached entries must be invalidated when a link is disabled). Enumeration: at 0.5% key-space density, **one random guess in 200 hits a live link**, so randomness is not access control. If unlisted or private links matter, use longer codes for them (10+ characters puts density near 1e-8) or require authentication. Sequential codes are worse: they reveal total volume and let anyone walk the space.

**Q6. 301 or 302?**

A 301 (permanent) is cached by browsers, so repeat clicks never reach you: less load, but lost analytics and no way to disable or retarget the link for clients that cached it. A 302 or 307 (temporary) sends every click through the service, preserving analytics and control at the cost of more traffic. If analytics and abuse takedown are requirements, use 302 with a short `Cache-Control` lifetime; say explicitly that this is a product decision.

**Q7. How do you delete expired links when you have 18 billion of them?**

Do not scan the table on a schedule. Check expiry on read (an expired link returns 410 immediately, so correctness never depends on cleanup), and delete lazily: use the store's per-item TTL if it has one, or a background job that walks an index ordered by `expires_at`. Do not reuse expired codes: old links live on in documents and chats, and reusing a code would silently redirect them to someone else's content. The key space is big enough that reuse is unnecessary.

**Q8. A bulk customer wants to create 100M links per day through the API.**

That is about 1,200 creates/s on average, still modest for a partitioned store, but it would be 10x the current write rate and concentrated in one tenant. Offer a batch API (thousands of URLs per request, results delivered asynchronously as a file), give the tenant a dedicated quota, and run it on a lower-priority path so it cannot starve interactive creates. Check code-space usage: 100M/day for 5 years adds 180B links, about 5% of the 7-character space, so collision retries rise but stay cheap. Plan an 8-character tier if growth continues.

### 4.6 Level Signals

- **Mid:** correct QPS and storage estimates; KV store plus cache; random base62 codes with a collision check; knows 301 vs 302.
- **Senior:** derives code length from key-space math; quantifies cache-failure load and coalesces misses; handles hot keys with layered caching; analytics async with a stated loss bound; multi-region uniqueness via partitioned code space.
- **Staff:** questions product scope (enterprise custom domains, private links, takedown and legal requests); identifies abuse as the real operational cost; keeps the architecture deliberately small and says why; plans for code-length migration and retention policy.

---

## 5. Mock 2: Rate Limiter

Worked design: [HLD §6.2 Rate Limiter](../computer-science/High_Level_Design.md#62-rate-limiter). Object-oriented version: [LLD §10](../design-patterns/Low_Level_Design_Interview_Prep.md#10-worked-design-rate-limiter). Thread-safe implementation: [Concurrency Problems §12](../computer-science/Concurrency_Coding_Problems.md#12-thread-safe-token-bucket-rate-limiter).

### 5.1 Prompt

> "Design a rate limiter for our public API. It sits in front of all our backend services."

### 5.2 Hidden Expectations

- **Algorithm choice with tradeoffs:** fixed window, sliding log, sliding-window counter, token bucket (or GCRA), and their memory and burst behavior.
- **Distributed atomicity:** a read-then-write race lets concurrent requests all see "1 token left". The fix is an atomic server-side operation.
- **Hot-path cost:** the limiter adds latency to every request, so one round trip at most and a tight timeout.
- **Failure policy:** fail-open vs fail-closed, decided per endpoint.
- **Hot keys and multi-region accuracy.** These separate senior from mid.
- **Client contract:** HTTP 429, `Retry-After`, remaining-quota headers.
- Trap: a sliding log (every timestamp stored) at a million requests per second; or a limiter that becomes a new single point of failure.

### 5.3 Clarifying Questions

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| Library in each service, gateway middleware, or separate service? | Middleware in the API gateway | Decides where state lives and the latency budget |
| What is the limiting key? | API key per route; also per IP for unauthenticated calls | Key cardinality and hot keys |
| Example limits? Bursts allowed? | 1,000 req/min per key, bursts up to 100 | Token bucket fits "rate plus burst" |
| Total traffic and number of keys? | 1M req/s peak, 10M keys, ~1M active per minute | Sizing of the counter store |
| How accurate? Is 5% overshoot acceptable? | Soft limits; small overshoot is fine for most routes | Allows local or approximate counting |
| Global or per region? | Global per key, 3 regions | Cross-region coordination problem |
| Added latency budget? | Under 1 ms p99 | One in-region round trip at most |

### 5.4 Model Answer Outline

**Requirements.** Functional: enforce per-key, per-route limits with bursts; return 429 with retry information; limits configurable per tier without deploys. Non-functional: under 1 ms added p99, highly available, approximately accurate globally. Out of scope: DDoS protection at the network layer (state it: it is a separate layer).

**Estimates.**

```text
Traffic:    1M req/s peak across ~200 gateway instances (~5k req/s each)
State:      token bucket per key ≈ tokens (8 B) + last refill (8 B) + key (~40 B) + store overhead (~50 B) ≈ 100 B
            1M active keys × 100 B ≈ 100 MB; even all 10M keys ≈ 1 GB      -> memory is not the problem
Ops:        1 atomic op per request = 1M ops/s; ~100k ops/s per single-threaded shard -> ~10-20 shards + replicas
Latency:    in-region RTT ≈ 0.5 ms; budget 1 ms                             -> exactly one round trip, atomic script
```

The binding constraint is **operations per second and latency**, not memory.

**Algorithms.**

| Algorithm | State per key | Burst behavior | Accuracy | Verdict |
|---|---|---|---|---|
| Fixed window counter | 1 counter | Up to 2x the limit across a window boundary | Coarse | Simple; fine for daily quotas |
| Sliding log | Every timestamp | Exact | Exact | Memory O(limit) per key: too costly at scale |
| Sliding-window counter | 2 counters | Smooth | Approximate (weights the previous window) | Good default for per-minute limits |
| Token bucket | Tokens + timestamp | Allows bursts up to capacity, then steady rate | Exact for its model | Best fit for "rate plus burst" |
| GCRA | One timestamp (theoretical arrival time) | Same as token bucket | Exact | Token bucket with less state |

**Design.**

```text
Client -> Edge (volumetric/IP filtering) -> API Gateway [limiter middleware] -> Backend services
                                                 |   local policy cache (pushed from config service)
                                                 |   1 atomic call, 5 ms timeout, circuit breaker
                                                 v
                                     Counter store, sharded by hash(key), replicated
```

**Deep dive: atomic token bucket.** One server-side script per request, using the store's clock so gateway clock skew does not matter:

```lua
-- fragment: Redis token bucket. KEYS[1] = bucket key; ARGV = capacity, refill_per_sec, cost
local cap  = tonumber(ARGV[1])
local rate = tonumber(ARGV[2])
local cost = tonumber(ARGV[3])
local t    = redis.call('TIME')                        -- server clock, not the caller's
local now  = tonumber(t[1]) + tonumber(t[2]) / 1e6
local b    = redis.call('HMGET', KEYS[1], 'tokens', 'ts')
local tokens = tonumber(b[1]) or cap
local ts     = tonumber(b[2]) or now
tokens = math.min(cap, tokens + (now - ts) * rate)
local allowed = 0
if tokens >= cost then tokens = tokens - cost; allowed = 1 end
redis.call('HSET', KEYS[1], 'tokens', tokens, 'ts', now)
redis.call('EXPIRE', KEYS[1], math.ceil(cap / rate) * 2)  -- idle buckets disappear
return { allowed, tostring(tokens) }                      -- tostring: Lua floats would be truncated in the reply
```

The script runs atomically on the shard, so there is no read-modify-write race. (Calling `TIME` inside a script requires effect-based script replication, which is the default from Redis 5 and the only mode in Redis 7.)

**Summary.** "Token bucket per key and route, enforced in gateway middleware with one atomic call to a sharded in-memory store. Policies are cached locally. Fail-open with a local fallback for ordinary routes, fail-closed for sensitive ones. Hot keys use leased token batches. Global limits use per-region enforcement with periodic usage exchange and bounded overshoot."

### 5.5 Follow-Ups With Model Answers

**Q1. The counter store shard is down. What happens to traffic?**

The limiter must never be the reason the API is down. Calls to the store have a tight timeout (about 5 ms) and a circuit breaker. When the breaker opens, the gateway falls back to a **local in-memory token bucket** sized at `limit / number_of_gateways` (approximate, but it still stops runaway clients). Choose the policy per route: **fail open** (local fallback) for ordinary reads; **fail closed** for expensive or security-sensitive operations such as login attempts, SMS sends, or payment creation, where letting abuse through costs more than a brief rejection. Meanwhile, a replica is promoted within seconds. Losing some counter state is acceptable because limits are soft.

**Q2. One tenant sends 200k requests per second, all hitting one shard.**

That shard saturates on a single key. Use **leased token batches**: each gateway takes, say, 100 tokens at a time from the global bucket (one `DECRBY`-style call) and serves requests locally until the lease runs out. Store operations for that key drop 100x. The cost is bounded over-admission: at most `gateways × batch` tokens can be outstanding, so size batches from the tenant's rate (a few hundred milliseconds of traffic per gateway). An alternative is splitting the key into `k` sub-buckets, each with `limit / k`, with the gateway picking one at random; that is simpler but less accurate for bursty traffic.

**Q3. Enforce a single global limit across three regions.**

Synchronous cross-region checks cost 70-150 ms per request, which breaks the 1 ms budget. Options: (a) static split, `limit / 3` per region: simple, but wastes quota when traffic is uneven; (b) **local enforcement plus asynchronous usage exchange**: each region enforces locally and broadcasts its per-key usage every ~1 s, allowing `limit − (others' last reported usage)`; overshoot is bounded by about `rate × sync_interval × (regions − 1)`; (c) a global coordinator that hands out regional quota leases proportional to recent demand. Pick (b) or (c) and state the overshoot bound explicitly. If a contract truly requires exact global limits (billing, for example), enforce them in a home region per tenant and accept the latency for those calls only.

**Q4. Clients immediately retry on 429. What do you change?**

Return `Retry-After` and remaining-quota headers, and document exponential backoff with jitter in client SDKs. Make rejections cheap: a rejected request should cost one store operation or less. Keep a short-lived local **deny cache** ("key K is empty until T") so a hammering client does not even reach the store. Decide whether rejected requests consume quota; usually they do not for token buckets, but abusive volume is better handled by a coarse per-IP limit at the edge.

**Q5. Traffic jumps 10x in one minute. Does the limiter protect the backend?**

Only if it is cheaper than the work it protects, and only for traffic it can attribute to keys. A 10x jump of legitimate, under-quota traffic passes straight through, so the backend also needs **load shedding based on its own health** (concurrency limits, queue-length-based rejection, priority classes) independent of per-key quotas. Volumetric attacks belong at the edge (CDN or L4 filtering). The limiter's own store must scale with request rate; leased batches and the deny cache keep its load below the request rate.

**Q6. Why not a fixed window? It is the simplest.**

With a limit of 100 per minute, a client can send 100 requests at 0:59 and 100 at 1:00: 200 requests in two seconds, double the intended rate. If that matters, use a sliding-window counter (`estimate = current + previous × (1 − elapsed_fraction)`, two counters per key) or a token bucket. Fixed windows remain fine for coarse daily quotas where a boundary burst is harmless.

**Q7. How do you change a tenant's limit without a deploy?**

Policies live in a config service as versioned documents. Gateways cache them and receive pushes (or poll every few seconds). The bucket key includes the policy ID, or the script reads capacity and rate as arguments on every call, so the new limit takes effect on the next request. Roll out policy changes gradually and alert on a sudden rise in 429 rate per tenant, which is the usual symptom of a bad policy push.

**Q8. Gateway clocks disagree by 200 ms. Does it matter?**

It would if gateways computed refills from their own clocks: buckets would refill too fast or too slowly depending on which gateway served the request. Computing refills inside the store with its own clock, as in the script above, makes clock skew irrelevant for a single shard.

### 5.6 Level Signals

- **Mid:** explains token bucket and fixed window correctly; uses a shared store; returns 429.
- **Senior:** identifies the race and uses an atomic script; sizes ops per second, not just memory; chooses fail-open vs fail-closed per route; handles hot keys with leases or sub-buckets; quantifies multi-region overshoot.
- **Staff:** positions the limiter within layered overload protection (edge filtering, per-key quotas, adaptive load shedding, priority classes); covers policy lifecycle and safe rollout; asks whether limits are a business contract (billing) or a protection mechanism, because that changes the accuracy requirement.

---

## 6. Mock 3: News Feed

Worked design: [HLD §6.3 News Feed](../computer-science/High_Level_Design.md#63-news-feed).

### 6.1 Prompt

> "Design the home news feed for a social network. Users follow other users and see their posts in a feed."

### 6.2 Hidden Expectations

- **Fan-out on write vs fan-out on read, with numbers**, and the **celebrity problem** solved with a hybrid. This is the core of the question.
- Timeline storage sized in memory, plus **post hydration** and its hot keys.
- **Ranking** as a separate pipeline stage with a latency budget and a fallback.
- **Correctness details:** deleted posts and privacy changes after fan-out; cursor pagination when new posts arrive.
- Trap: pure fan-out on write without computing what one celebrity post costs, or pure fan-out on read without computing the read cost.

### 6.3 Clarifying Questions

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| DAU and feed opens per day? | 300M DAU, 10 feed opens/day | Read QPS |
| Posts per day? | 100M | Write and fan-out rate |
| Follow graph shape? | Average ~200 followers; some accounts have 100M | Celebrity problem |
| Chronological or ranked? | Ranked, but start chronological | Adds a ranking stage |
| Freshness? | New posts visible to followers within seconds to a minute | Allows async fan-out |
| Media? | Yes, via CDN; out of scope | Store references only |
| Edits, deletes, audience restrictions? | Yes, must be respected immediately | Filter at read time |

### 6.4 Model Answer Outline

**Estimates.**

```text
Feed reads:   300M × 10 = 3B/day ≈ 35k/s average, ~100k/s peak
Posts:        100M/day ≈ 1.2k/s average, ~4k/s peak
Fan-out:      100M posts × ~200 followers = 20B timeline inserts/day ≈ 230k/s average, ~700k/s peak
Celebrity:    one post by a 100M-follower account = 100M inserts; at 1M inserts/s that is ~100 s of the whole fleet
Timelines:    500 post IDs × 8 B = 4 KB per user × 300M ≈ 1.2 TB -> sharded in-memory store with replicas
Hydration:    100k pages/s × 20 posts = 2M post lookups/s -> post cache with batched multi-get
```

**Decision from the numbers:** push (fan-out on write) for ordinary accounts, because reads outnumber posts 30:1 and precomputed timelines make reads cheap; **pull for accounts above a follower threshold** (around 10k-100k, tuned by measurement), merged at read time. Skip fan-out to users inactive for 30+ days and rebuild their timelines when they return.

**Design.**

```text
Post:   Client -> Post service -> Post store (source of truth) -> event log
                                                            -> Fan-out workers (skip celebrities, skip inactive)
                                                                  -> Timeline store: user_id -> [post_id ...] (capped 500)
Read:   Client -> Feed service -> timeline (push part)  +  recent posts of followed celebrities (pull part)
                              -> candidate set (~500-800) -> ranker (budget ~50 ms; fallback chronological)
                              -> hydrate via post cache -> filter (deleted, blocked, audience) -> page + cursor
```

**Deep dive: the hybrid merge.** Each user follows on average a few dozen high-follower accounts. Their recent posts are a small, very hot set cached everywhere. The feed service merges `timeline[user]` with `recent_posts[c]` for each followed celebrity `c`, dedupes, and hands the candidates to ranking.

**Second deep dive: ranking.** Two stages: a cheap model scores ~500 candidates, then a heavier model reranks the top ~100. Features come from a feature store. If the ranker misses its deadline, return chronological order; a slightly worse feed beats an error.

### 6.5 Follow-Ups With Model Answers

**Q1. A celebrity with 100M followers posts. Walk me through it.**

The post is written once to the post store and added to the celebrity's recent-posts list, which is replicated to the caches of every feed-service region. No fan-out happens. When any follower opens the feed, the feed service merges that list in. The cost moves from 100M writes once to one cache read per follower feed load, which is cheap because the list is tiny and hot. Interviewers often push: "What about an account with 50k followers, just under the threshold?" Fan-out of 50k inserts at 1M inserts/s is 50 ms of fleet time, which is fine; the threshold is chosen where push write cost exceeds pull read cost.

**Q2. The timeline cache cluster loses a node, or the whole cluster.**

Timelines are **derived data**: they can be rebuilt from the post store and the follow graph. With replicas, a single node failure is a promotion. If timelines are lost for many users, the feed service falls back to **fan-out on read** for affected users: fetch recent posts of the 200 accounts they follow (a batched query against the post store by author and time), with a concurrency cap so the rebuild does not overload the post store. Rebuild lazily on first read, active users first. Meanwhile, return a degraded feed (top followed accounts only) rather than an error.

**Q3. Super Bowl night: reads go up 10x for an hour.**

Plan ahead: pre-scale stateless services before the event. During it: (1) cache the hydrated first page per user for a short TTL (30-60 s); (2) degrade ranking to the cheap model or chronological order when latency rises; (3) shed non-essential work (like counts, suggested posts); (4) one viral post becomes a hot key in the post cache, so keep an in-process cache on feed servers; (5) delay fan-out for less active users so write capacity is spent on people who are online. Name the metric you watch: feed p99 latency and post-cache hit rate.

**Q4. A post is deleted, or its audience changes, after it has been fanned out to 5M timelines.**

Do not chase 5M timeline entries synchronously. The post store is the source of truth, and **hydration checks it on every read**: deleted posts are dropped and audience rules are evaluated against the viewer. Publish a delete event that invalidates the post in all caches (with a short TTL as a safety net) and lazily cleans timelines in the background. This is why hydration and filtering belong on the read path even when timelines are precomputed.

**Q5. How does pagination work while new posts keep arriving?**

Offset pagination breaks: new posts shift everything down, causing duplicates. Use a cursor encoding the last item's sort key, `(score or timestamp, post_id)`, and fetch items strictly after it. For a ranked feed, scores change between page loads, so snapshot the ranked candidate list per session (store the ordered IDs with a TTL of ~30 minutes) and page through the snapshot. New posts appear through a "new posts" indicator that starts a fresh session.

**Q6. Make it multi-region.**

Home each user in a region. Replicate posts asynchronously to all regions; each region's fan-out workers insert into timelines of followers homed there. Follow-graph changes replicate the same way. **Read-your-writes** for authors: the feed service always merges the viewer's own recent posts from the home region, so authors see their posts immediately even if replication lags. A region failure moves users to another region, which can rebuild their timelines from replicated posts (Q2).

**Q7. Is fan-out exactly once? What if a worker crashes halfway through a list of followers?**

Fan-out is at-least-once: the worker checkpoints progress through the follower list, and after a crash the job resumes from the last checkpoint, re-inserting some entries. Timeline inserts are **idempotent** (a set keyed by post ID, such as a sorted set where re-adding an existing member does nothing), so duplicates are harmless. That is effectively-once without distributed transactions.

**Q8. A user follows a new account. When do that account's old posts show up?**

Fan-out only covers future posts, so either backfill the last N posts of the newly followed account into the follower's timeline asynchronously, or let the pull path merge them until the next refresh. Unfollow is similar: filter at read time immediately, and clean up the timeline asynchronously.

### 6.6 Level Signals

- **Mid:** explains push vs pull and picks hybrid when prompted; cursor pagination; post store as source of truth.
- **Senior:** computes fan-out writes and the celebrity cost unprompted; sizes the timeline store; filters deletes at hydration; idempotent fan-out; ranking with a fallback.
- **Staff:** treats feed quality and latency as product metrics; designs degradation modes for events; discusses tuning the push/pull threshold with data; considers the ranking platform as a separate system with its own owners and experiments; plans regional homing and rebuild costs.

---

## 7. Mock 4: Chat System

Worked design: [HLD §6.4 Chat System](../computer-science/High_Level_Design.md#64-chat-system).

### 7.1 Prompt

> "Design a chat application like WhatsApp or Messenger, with one-to-one and group conversations."

### 7.2 Hidden Expectations

- **Connection management at scale:** persistent connections (WebSockets), stateful gateways, a session registry, heartbeats, and reconnect storms.
- **Delivery semantics:** at-least-once with idempotent sends and client-side dedupe. A candidate who promises exactly-once delivery loses points.
- **Ordering per conversation** via a per-conversation sequence number, not timestamps.
- **Offline delivery and multi-device sync** with per-device cursors.
- **Group fan-out** and how it changes for very large groups.
- Presence that does not melt the system.
- Trap: polling a database for new messages; global ordering; acknowledging a send before it is durable.

### 7.3 Clarifying Questions

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| DAU, messages per user per day? | 100M DAU, 50 messages sent per user per day | Message rate and storage |
| Group size limit? | 500 for groups; large "channels" later | Fan-out strategy |
| Multiple devices per user? | Yes, phone plus desktop | Per-device sync cursors |
| History retention? | Forever, server-side | Storage growth |
| Media? | Yes, but out of scope (object storage plus references) | Keeps messages small |
| Read receipts, typing, presence? | Yes, best effort | Ephemeral path separate from durable path |
| End-to-end encryption? | Not in v1 | Changes search, moderation, multi-device |

### 7.4 Model Answer Outline

**Estimates.**

```text
Concurrent:   ~30% of DAU online at peak ≈ 30M connections (more with multi-device)
Messages:     100M × 50 = 5B/day ≈ 58k/s average, ~150k/s peak
Deliveries:   mostly 1:1 plus small groups, ~2 recipients per message on average -> ~300k deliveries/s peak
Gateways:     ~200k connections per gateway (tens of KB per idle TLS connection) -> ~150 gateways, ~200 with headroom
Heartbeats:   30M connections / 30 s = 1M heartbeats/s, absorbed by gateways, never by the database
Storage:      5B × ~200 B ≈ 1 TB/day ≈ 365 TB/year before replication -> partitioned wide-column or KV store
```

**Design.**

```text
Device <-> LB (L4) <-> Gateway (WebSocket, auth, heartbeats)
                         |  register(user, device) -> Session registry (in-memory KV, TTL refreshed by heartbeat)
                         v
                   Chat service: check membership -> assign per-conversation seq -> persist -> ack sender
                         |                                   |
                         |                                   v
                         |                     Message store: partition = conversation_id, sort = seq
                         v
                   Delivery router: recipients -> registry lookup -> owning gateway -> push to device
                         \-> offline devices: push notification service (APNs/FCM)
Reconnect / new device: "sync after cursor" per conversation (or per-user inbox) -> paginated deltas
```

**Deep dive: the send path and acknowledgment levels.**

1. Client sends `{conversation_id, client_msg_id, body}`. `client_msg_id` is a UUID generated once, so retries are idempotent.
2. Chat service checks membership, then does a conditional insert keyed by `(conversation_id, sender_device, client_msg_id)`. A retry hits the existing row and returns the same `seq`.
3. The partition owner of the conversation assigns `seq` (single writer per conversation), persists, then **acks the sender** with `seq`. That is the single tick: durable on the server.
4. The router pushes to online recipient devices. A device ack is the double tick (delivered); a read cursor update is "read".
5. Recipients order by `seq`; a gap (seq 41 then 43) triggers a fetch of the missing range.

**Deep dive: multi-device sync.** Two common models: per-conversation cursors (a device asks each conversation for messages after its last seq; simple, but a device with 300 conversations makes 300 queries), or a **per-user inbox** with its own monotonically increasing sequence (each message appends an entry to each recipient's inbox, so a device syncs with one "inbox entries after N" query). The inbox costs write amplification equal to group size, so it fits small groups; large groups are handled differently (Q4).

### 7.5 Follow-Ups With Model Answers

**Q1. A gateway holding 200k connections dies.**

Clients detect it through a TCP reset or missed heartbeats and reconnect through the load balancer to other gateways. Without care, 200k simultaneous reconnects (each with a TLS handshake and an auth check) overload the survivors, so clients use **exponential backoff with jitter** (spreading reconnects over 10-30 s), and the auth step accepts a cheap resumption token. Registry entries pointing at the dead gateway expire by TTL, or are overwritten by the new registration, which carries a higher session epoch so a stale entry cannot win. No messages are lost: every message was persisted before the sender was acked, and undelivered messages are picked up by the reconnecting device's sync from its last cursor.

**Q2. Can you guarantee exactly-once delivery?**

Not across an unreliable network: an ack can be lost after the message was delivered, and the sender cannot tell which happened. What users see can still be **effectively once**: senders retry with the same `client_msg_id`, the server dedupes on it so a message is persisted once, and devices dedupe on `seq` or message ID so a redelivered message is not shown twice. That is at-least-once delivery plus idempotent processing at each hop.

**Q3. How do you guarantee messages appear in the same order for everyone in a group?**

A single authority assigns a monotonically increasing `seq` per conversation, typically the leader of the partition that owns the conversation, or an atomic conditional increment on a per-conversation counter. All clients order by `seq`, never by device timestamps, which skew. Ordering across conversations is not required, which is what lets the system partition freely. If two members send "at the same time," the order is whichever the authority sequenced first, and everyone sees that same order.

**Q4. A group (channel) has 100k members.**

Per-member fan-out at 10 messages/s would be 1M inbox writes per second for one conversation. Switch large groups to **fan-out on read**: store each message once; online members receive it through a per-group pub/sub topic that each *gateway* subscribes to once on behalf of all its local members (fan-out becomes about 200 gateways, not 100k users); offline members fetch on open. Disable per-member read receipts (show aggregate counts), rate-limit posting, and possibly restrict who can post. The threshold between the two modes is a few hundred to a few thousand members.

**Q5. Two users in different regions chat with each other.**

Each user connects to the nearest region. Each conversation has a **home region** (for example, the creator's) that assigns `seq` and holds the primary copy. A message from a user in another region is forwarded to the home region (adding roughly 70-150 ms), persisted and sequenced there, and delivered through each recipient's local gateways. Replicate the message store asynchronously to other regions for reads and disaster recovery. If the home region fails, promote a replica; with asynchronous replication the last few hundred milliseconds of messages can be lost unless cross-region replication is synchronous, which costs latency on every send. State that tradeoff explicitly.

**Q6. Presence for 30M online users.**

Presence is **ephemeral and approximate**: heartbeats refresh a TTL entry in the registry; no database writes. The danger is broadcast: if every online/offline change were pushed to all contacts, users with 500 contacts flapping on mobile networks would generate a storm. Instead, clients subscribe to presence only for contacts currently on screen, gateways debounce changes (a user is "offline" only after missing heartbeats for ~30-60 s), and the list view uses coarse "last seen" values fetched lazily.

**Q7. A desktop device was offline for two weeks. What happens when it reconnects?**

It sends its last inbox cursor (or per-conversation cursors) and receives paginated deltas, newest conversations first so the UI is usable quickly. If the cursor is older than inbox retention (say 30 days), the server tells the device to do a full resync of recent conversations from the message store. Push notifications reached the phone during those two weeks; collapse keys stop the device from being flooded with notifications for old messages.

**Q8. Product now wants end-to-end encryption. What changes?**

The server stores and forwards ciphertext only. Clients establish keys with a protocol such as Signal's (an asynchronous key agreement using prekeys the server stores, then the Double Ratchet for forward secrecy). Each **device** has its own keys, so a sender encrypts every message per recipient device (or, for groups, distributes a sender key once and encrypts each message once). Consequences: no server-side search or content moderation, history backup must be client-encrypted, adding a new device needs a secure key-transfer flow, and "delivered" semantics are per device. Say that this is a product and legal decision as much as a technical one.

### 7.6 Level Signals

- **Mid:** WebSocket gateways, a message store partitioned by conversation, offline push, client message IDs.
- **Senior:** session registry with TTL and epochs; per-conversation sequencing; persist-before-ack; at-least-once plus dedupe stated precisely; reconnect storms handled with jitter; large-group mode switch.
- **Staff:** multi-region homing with an explicit loss window; presence and receipts designed as best-effort side channels with their own budgets; E2E encryption implications across product, moderation, and multi-device; operational concerns such as gateway deploys (draining 200k connections gradually rather than killing them).

---

## 8. Mock 5: Distributed Key-Value Store

Worked design: [HLD §6.8 Distributed Key-Value Store](../computer-science/High_Level_Design.md#68-distributed-key-value-store) (consistent hashing, quorums, hinted handoff, Merkle anti-entropy, LSM storage engine).

### 8.1 Prompt

> "Design a distributed key-value store. It should scale horizontally and stay available when machines fail."

### 8.2 Hidden Expectations

This is a **depth** question. The interviewer wants mechanisms, not product names:

- **Partitioning** with consistent hashing and virtual nodes, and why modulo hashing fails.
- **Replication and quorums:** N, R, W; what `R + W > N` does and does **not** guarantee.
- **Failure handling:** gossip-based membership, sloppy quorum, hinted handoff, read repair, Merkle-tree anti-entropy.
- **Conflict resolution:** last-writer-wins and its lost-update problem vs vector clocks with siblings.
- **Storage engine:** WAL, memtable, SSTables, compaction, Bloom filters, tombstones.
- Senior and above: the CP alternative (consensus per shard) and when to choose it; tail latency from compaction.

### 8.3 Clarifying Questions

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| Data size, key and value sizes? | 10B keys, ~1 KB values, up to 1 MB | Node count, storage engine |
| Read and write rates? | 500k reads/s, 100k writes/s at peak | Per-node load |
| Consistency requirement? | Tunable per request; availability preferred | AP design with quorums |
| Operations? | get, put, delete; no range scans or transactions | Hash partitioning is fine |
| Latency? | p99 under 10 ms in-region | Memory-resident hot data, speculative reads |
| Multi-datacenter? | Later; design so it is possible | Per-DC replica placement |

### 8.4 Model Answer Outline

**Estimates (from the worked design).** About 11 TB raw, 33 TB with N = 3, 40-50 TB on disk with LSM overhead. With 4 TB NVMe nodes kept under 50% full, that is about 30 nodes. Per node: about 10k replica writes/s and 33k replica reads/s, which an LSM engine with a block cache and Bloom filters handles. **The cluster is storage-capacity-bound, not CPU-bound**, so disk headroom sets node count.

**Design.** Any node can coordinate. The coordinator hashes the key onto a ring of virtual nodes, finds the preference list (the next N distinct physical nodes), writes to all N in parallel, and acknowledges after W durable WAL appends. Reads go to N replicas (or R plus speculative), return the newest version (or siblings), and repair stale replicas.

**Deep dive: quorum arithmetic.**

| N, W, R | Write survives | Read survives | Behavior |
|---|---|---|---|
| 3, 2, 2 | 1 replica down | 1 replica down | Default: overlapping quorums, balanced latency |
| 3, 1, 1 | 2 down | 2 down | Fastest, stale reads likely |
| 3, 3, 1 | 0 down | 2 down | Fast reads, writes blocked by any failure |
| 3, 1, 3 | 2 down | 0 down | Rarely useful |

**Deep dive: storage engine.** Writes go to the WAL (fsync policy is a durability knob), then the memtable; full memtables flush to immutable SSTables; compaction merges SSTables and drops overwritten values and expired tombstones. Reads check the memtable, then SSTables newest-first, skipping most of them with per-SSTable Bloom filters (about 10 bits per key gives a 1% false-positive rate).

### 8.5 Follow-Ups With Model Answers

**Q1. With N = 3 and W = 2, one replica is down during a write.**

The coordinator gets two acks and returns success. The write for the down replica goes to the next healthy node on the ring with a hint saying "this belongs to D" (**sloppy quorum**). When D's heartbeats resume in gossip, the hint holder replays it (**hinted handoff**). If D stays down longer than the hint window (hours), hints are dropped to bound their storage, and periodic **Merkle-tree anti-entropy** finds and streams the divergent ranges. Reads that touch D before repair see an old version and trigger read repair.

**Q2. A network partition splits the cluster in two.**

With sloppy quorums, both sides keep accepting writes for the same keys, so the system stays available and diverges. On healing, versions are reconciled: **LWW** keeps the higher timestamp and silently drops the other write; **vector clocks** detect that the writes are concurrent and return both as siblings for the application to merge (for example, union of shopping-cart items); **CRDTs** merge automatically for data types that support it (counters, sets). If the application cannot tolerate divergence for some keys, use strict quorums for them: the minority side then rejects writes, which is consistency over availability for those keys.

**Q3. Does `R + W > N` give linearizability?**

No, and saying so is a senior signal. Three reasons: (1) with sloppy quorums, the W nodes written and the R nodes read may not overlap at all; (2) during an in-flight write that has reached only some replicas, one reader can see the new value and a later reader the old one, unless read repair completes before the read returns; (3) LWW with skewed clocks can discard an acknowledged write. For operations that need linearizability, such as compare-and-set or unique-username claims, run a **consensus protocol** (Paxos or Raft) per key or key range. That costs extra round trips, so restrict it to the operations that need it.

**Q4. One key receives 1M reads per second.**

It lives on three replicas, each of which can serve perhaps 100k simple reads per second, so even reading from all of them falls short. Options: (1) a client-side or proxy cache with a short TTL, if a little staleness is acceptable (it usually is for a hot read key); (2) replicate the key under salted names `key#1..key#k` on different nodes, read a random copy, and write all copies; (3) coalesce identical concurrent reads at the coordinator. For a hot **write** key, such as a global counter, split it into k sub-counters and sum on read, or use a CRDT counter.

**Q5. Add 10 nodes without downtime.**

With virtual nodes (for example 256 tokens per node), each new node takes many small ranges from many existing nodes, so load stays balanced and streaming comes from many sources in parallel. During the move, writes for a moving range go to both the old and new owner; the new node streams SSTables for its ranges (throttled to protect foreground latency), then ownership flips through gossip and old owners clean up. Rough time: 45 TB over 40 nodes is about 1.1 TB per new node; at 100 MB/s that is about 3 hours, run in parallel. Add nodes one or a few at a time to limit simultaneous range movement.

**Q6. A node's disks die permanently.**

Do not re-replicate on every transient failure: a phi-accrual failure detector or a timeout (15-30 minutes) separates "slow or rebooting" from "gone," because re-replicating 1.5 TB for a reboot wastes bandwidth and can cascade. Once declared dead, a replacement node takes over its tokens and streams the data from the surviving replicas. While that runs, affected ranges have two copies; a second failure in the same range leaves one, so prioritize those ranges and alert. Virtual nodes spread the rebuild sources across the cluster, shortening the window of reduced redundancy.

**Q7. Why are deletes written as tombstones instead of removing the data?**

A replica that missed the delete still holds the old value. If the other replicas simply erased it, read repair or anti-entropy would see the old value as "newer than nothing" and **resurrect** it. A tombstone is a versioned delete marker that wins reconciliation. Tombstones are purged only after a grace period (Cassandra's default `gc_grace_seconds` is 10 days), so a full repair must complete within that window. Large numbers of tombstones also slow reads, because reads must scan past them; delete-heavy workloads such as queues are a classic misuse of LSM stores.

**Q8. p99 latency spikes every few minutes. What do you look at?**

Correlate the spikes with background work on the node: memtable flushes, compaction bursts (I/O saturation), JVM or allocator pauses if relevant, and repair streaming. Mitigations: throttle compaction, choose leveled compaction for read-heavy workloads (fewer SSTables per read, more write amplification) or size-tiered for write-heavy ones, separate WAL and data disks, and use **speculative retry**: if a replica has not answered by the p95 latency, send the read to another replica and take the first answer. See [Tail Latency and Fan-Out Amplification](../computer-science/Performance_Engineering.md#14-tail-latency-and-fan-out-amplification).

### 8.6 Level Signals

- **Mid:** consistent hashing, replication factor 3, quorum reads and writes, basic LSM description.
- **Senior:** explains sloppy quorum, hinted handoff, read repair, and Merkle trees and when each runs; knows quorums are not linearizable; covers tombstones and hot keys; does the node-count math.
- **Staff:** separates the AP and CP designs and says which customers need which; quantifies rebuild windows and their durability risk; covers operations (rolling upgrades, repair scheduling, capacity planning against compaction headroom); would run consensus only where needed.

---

## 9. Mock 6: Search Typeahead

Worked design: [HLD §6.9 Search Autocomplete (Typeahead)](../computer-science/High_Level_Design.md#69-search-autocomplete-typeahead).

### 9.1 Prompt

> "Design search autocomplete. As the user types in a search box, show the top 10 suggestions."

### 9.2 Hidden Expectations

- A **latency budget** split across client, network, and server (about 100 ms end to end leaves 10-20 ms for the server).
- The right data structure: a trie (or prefix map) with **precomputed top-K per node**, not a subtree walk per request and not `LIKE 'prefix%'` against a database.
- The insight that the index **fits in memory**, so it is replicated, not sharded.
- An **offline build pipeline** with versioned snapshots and atomic swap, separate from serving.
- Freshness (trending) and content safety (fast removal) as separate, faster paths.
- Trap: updating a shared trie in place under live traffic; ignoring the CDN for short prefixes.

### 9.3 Clarifying Questions

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| Users and searches? | 100M DAU, 10 searches/day | QPS after keystroke multiplication |
| Latency target? | Under 100 ms end to end | Server budget, CDN |
| Ranking signal? | Popularity with time decay | Offline aggregation |
| Freshness? | Hourly is fine; trending in minutes is a stretch goal | Batch build plus optional stream |
| Personalization, languages, spelling? | Not in v1 | Keep the index global |
| Content policy? | Offensive suggestions removed within minutes | Serve-time blocklist |

### 9.4 Model Answer Outline

**Estimates (from the worked design).** About 1B searches/day, about 6 requests per search after debounce, so about 70k QPS average and 200k QPS peak. The 10M most popular queries in a trie with top-10 lists take about 6 GB, which **fits in RAM**, so every server holds a full copy and about a dozen servers per region handle peak. Query logs are about 100 GB/day, which suits batch aggregation.

**Design.** Online: client debounce (100-150 ms) and local cache, then a CDN that caches 1-2 character prefixes, then stateless suggest servers that walk to the prefix node and return its precomputed list, filtered by a serve-time blocklist. Offline: logs, hourly aggregation with time decay, index build, an immutable versioned snapshot in object storage, then servers load the new version beside the old and swap a pointer.

**Deep dive: why precomputed top-K.** Walking the subtree under "a" touches millions of nodes. Storing the top-K query IDs at every node at build time makes each lookup O(prefix length). The cost is build time and memory (K IDs per node), both offline and bounded.

### 9.5 Follow-Ups With Model Answers

**Q1. Product wants trending queries to appear within five minutes.**

Add a streaming path beside the hourly build. A stream job counts queries in 5-minute tumbling windows. At about 12k searches/s average, exact per-query counts sharded by query are affordable; at higher volumes, use a Count-Min Sketch plus a top-K heap per window to find heavy hitters in bounded memory. Compare each query's current-window rate with its baseline (a ratio or z-score) to detect trending, build a small "fresh" index (thousands of queries) every minute, and merge its results with the main index at serve time with a score boost. The main index stays hourly and simple.

**Q2. An offensive suggestion is trending. Remove it now.**

Push the pattern to a **serve-time blocklist** that every suggest server applies to results, through the config push channel (seconds). Store about 15 suggestions per node instead of 10, so filtering still leaves 10. Responses cached at the CDN keep serving the bad suggestion until their TTL expires, so either purge affected prefixes or keep the CDN TTL short (a few minutes); say that the maximum exposure time equals the CDN TTL unless you purge. Add the pattern to the build-time filter so the next snapshot excludes it.

**Q3. The index grows 100x (all languages, a billion queries).**

At about 600 GB it no longer fits on one server, so shard. **Shard by locale** first, which is a natural partition with almost no cross-shard queries. Within a large locale, shard by **prefix range** so a request still hits exactly one shard; split hot ranges finer ("s" and "th" are much hotter than "x") and give hot shards more replicas. Avoid hashing whole queries across shards: every prefix lookup would become a scatter-gather across all shards.

**Q4. A live event drives 10x traffic for an hour.**

Most of the extra traffic is short prefixes, which the CDN absorbs. Suggest servers are stateless and the index is a file, so autoscaling is just starting more replicas (the snapshot loads in seconds from local disk or object storage). If capacity still runs short, the server can return a hint to raise the client debounce interval, and can shed long-prefix requests (users who keep typing will finish their query anyway).

**Q5. A new snapshot is bad: half of the suggestions are garbage.**

Prevent it with build-time validation gates: size within a few percent of the previous build, golden queries returning expected results, the blocklist applied. Deploy to a canary server first and compare its metrics (suggestion click-through rate, empty-result rate) with the fleet. Keep the previous snapshot loaded or on local disk so rollback is a pointer swap that takes seconds. Immutable, versioned snapshots are what make this rollback safe.

**Q6. Add personalization.**

Blend global suggestions with the user's recent searches. The cheapest and most private option is on the client: it keeps the last 100 queries and merges matches locally. A server-side option fetches per-user history from a KV store in parallel with the global lookup, inside the same 10-20 ms budget, and boosts matches. Personalized responses cannot be CDN-cached, so personalize only after the first two or three characters, where the CDN matters most.

**Q7. Handle typos: "gpu proflier".**

Fuzzy trie walks (allowing one edit) multiply the work per keystroke. Cheaper options: a spelling-correction map mined from logs (users who typed X and then searched Y), applied when the exact prefix has few results; or an n-gram index for candidate generation. Usually this lives in a separate spelling service, called only on poor results.

**Q8. How does it work across regions?**

Build once (or per region for locale-specific rankings), publish snapshots to object storage replicated to each region, and serve locally in every region. Query logs are aggregated regionally and merged globally for the build. Each region can roll out a snapshot independently, which also gives a natural canary order.

### 9.6 Level Signals

- **Mid:** trie with top-K, caching, an offline build.
- **Senior:** latency budget split; index-size math leading to full replication; snapshot swap and rollback; blocklist at serve time; CDN for short prefixes.
- **Staff:** separate freshness and safety paths with their own SLOs; build validation and canarying as first-class parts of the design; a sharding plan for growth that preserves single-shard lookups; measures success with product metrics (suggestion click-through).

---

## 10. Mock 7: Distributed Job Scheduler

Worked design: [HLD §6.12 Distributed Job Scheduler](../computer-science/High_Level_Design.md#612-distributed-job-scheduler). The GPU-cluster variant (gang scheduling, topology-aware placement) is [ML Systems Design §6](../ml-gpu/ML_Systems_Design.md#6-case-study-gpu-cluster-job-scheduler).

### 10.1 Prompt

> "Design a distributed job scheduler: a cron service for thousands of internal teams. It supports one-off and recurring jobs, retries, and recovery from worker failures."

### 10.2 Hidden Expectations

- A **durable schedule** and an efficient way to find due jobs (an index on `next_run_at`, partitioned across scheduler instances by lease, plus an in-memory timing wheel for the next minute).
- **Execution semantics stated precisely:** at-least-once, with leases, heartbeats, and **fencing tokens** so a stale worker cannot overwrite a newer attempt.
- The **top-of-hour burst**, which dominates capacity planning far more than the average rate.
- Retries with backoff, a dead-letter state, and per-tenant fairness.
- Time handling: time zones, DST, misfires after an outage, clock skew.
- Trap: one big cron machine; "exactly-once execution"; correctness that depends on synchronized clocks.

### 10.3 Clarifying Questions

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| How many jobs, how often? | 10M recurring (about hourly), 1M one-off per day | Run rate and burst |
| Start-time precision? | Within a few seconds normally | Lookahead loading, dispatch rate |
| Execution guarantee? | At-least-once; job owners make jobs idempotent | Leases and fencing, not transactions |
| Job duration? | Average 30 s, some run for hours | Worker slots via Little's law, heartbeats |
| What is a job? | Container image or HTTP call with payload | Worker types |
| Dependencies between jobs? | Stretch goal | DAG extension |
| Multi-tenant? | Yes, with quotas and priorities | Fair dispatch |

### 10.4 Model Answer Outline

**Estimates (from the worked design).** About 240M runs/day, or 2,800 runs/s average. If 20% of hourly jobs use `0 * * * *`, then about 2M runs are due in the same second; at 50k dispatches/s the last one starts 40 s late. Little's law gives about 84k concurrent worker slots on average (2,800/s × 30 s). Definitions are about 10 GB, which fits one replicated relational database; run history is about 48 GB/day. **The burst, not the average, drives the design.**

**Design.** Job API writes definitions with `next_run_at`. Scheduler instances hold leases on job partitions, query due-soon jobs, keep them in a timing wheel, and at fire time create the run row and advance `next_run_at` in one transaction (unique key `(job_id, scheduled_for, attempt)` makes this idempotent). Workers claim runs (`FOR UPDATE SKIP LOCKED` or a queue), heartbeat to extend the lease, and complete conditioned on the fencing token. A reaper retries runs with expired leases or dead-letters them.

**Deep dive: fencing tokens.** Each claim increments a token. Completion is `UPDATE ... WHERE run_id = ? AND fencing_token = ?`. A worker that stalled past its lease holds an old token, so its write matches zero rows.

### 10.5 Follow-Ups With Model Answers

**Q1. A scheduler instance dies.**

Its partition leases expire (lease TTL around 10-15 s), and other instances acquire them from the coordination service. The new owner's first scan includes overdue jobs (`next_run_at <= now + lookahead`, with no lower bound), so nothing is skipped; runs start late by at most the lease TTL plus one scan interval. If the "dead" instance was only paused and wakes up, it may try to fire the same jobs: the unique `(job_id, scheduled_for)` key makes duplicate run creation a no-op, and including the partition **lease epoch** in the transaction lets the database reject writes from an instance that no longer owns the partition.

**Q2. Can you guarantee each run executes exactly once?**

No. A worker can finish the job's side effect and crash before reporting completion; the scheduler cannot distinguish that from a crash before the side effect, so it must either retry (at-least-once) or not (at-most-once). Offer both as a per-job policy, with at-least-once as the default, and provide the tools for **effectively-once**: a stable `run_id` passed to the job as an idempotency key, the fencing token for writes to storage that can check it, and guidance to use transactional outbox patterns. Exactly-once is achievable only end to end, inside the job's own data model.

**Q3. Two million jobs are due at exactly midnight.**

Load them ahead of time: the lookahead scan puts runs due in the next 60 s into the timing wheel and pre-creates run rows, so midnight is pure dispatch. Spread work where tenants allow it: a default jitter window or a hashed start time (in the spirit of Jenkins' `H` cron syntax, which hashes the job name to a fixed minute), plus per-tenant dispatch rate limits and priority classes so one tenant's 500k jobs cannot delay everyone else's critical jobs. The worker pool cannot scale to 2M slots for a 30-second spike, so runs queue, and the SLO should say "starts within N seconds at p99, except for declared burst windows." Measure and report start delay per tenant.

**Q4. A worker freezes for 60 seconds (GC pause or VM migration), then wakes up and reports success.**

Its 30-second lease expired while it was frozen; the reaper created attempt 2 with a new, larger fencing token, and another worker is running it. When the first worker reports completion, the conditional update with its old token matches nothing, and the worker is told its lease was lost and must abort. The remaining risk is side effects the zombie already performed on **external** systems. Those systems must also check the token (accept writes only with a token greater than or equal to the last seen) or be idempotent on `run_id`. This is the core reason fencing exists: leases alone cannot stop a paused process.

**Q5. The database becomes the bottleneck.**

Count writes per run: create, claim, a few heartbeats, complete. At 2,800 runs/s that is roughly 15k writes/s plus heartbeats (84k running jobs every 10 s is 8.4k/s). Steps, in order: move heartbeats to an in-memory lease store or lengthen the heartbeat interval; batch claims; partition the run table by `hash(job_id)` across database shards, each owned by a subset of schedulers; and move the ready queue to a partitioned log or queue service, keeping the database as the system of record and using a transactional outbox to keep the two consistent. Drop old run-history partitions by day rather than deleting rows.

**Q6. Add DAG dependencies: job B runs after job A succeeds.**

Store edges and validate the graph for cycles at registration. Runs for a DAG share a logical date (the interval being processed). When A's run for date D succeeds, a transaction decrements B's pending-dependency counter for D; when it reaches zero, B's run is created. Define failure semantics (B is skipped or blocked when A fails), timeouts for upstreams that never finish, and backfill (re-running a range of logical dates in order). This is the model used by data-pipeline schedulers.

**Q7. Make it multi-region.**

The danger is **double firing**: two regions both believing they own a job. Simplest robust answer: active-passive scheduling. One region owns all partitions; leases live in a coordination service that is strongly consistent across regions (slow, but leases change rarely); workers can run anywhere. On region failure, leases move to the standby region, which reads the replicated job store. If the job store is asynchronously replicated, the standby may not see the last few seconds of `next_run_at` updates and may re-fire a few runs, which is acceptable under at-least-once and absorbed by idempotent run creation where the store allows it. Per-tenant home regions are the next step when one region's scheduling capacity is not enough.

**Q8. A job runs daily at 02:30 in `Europe/Berlin`. What happens on DST transition days?**

On the spring-forward day, 02:30 does not exist (clocks jump from 02:00 CET to 03:00 CEST); on the fall-back day, 02:30 happens twice (clocks go back from 03:00 CEST to 02:00 CET). The repeated hour is zone-specific: in US zones such as `America/Chicago` the fall-back goes from 02:00 CDT to 01:00 CST, so 01:00-01:59 repeats and a 02:30 job fires once while a 01:30 job would see two candidate times. The scheduler must compute next fire times in the job's time zone, then convert to UTC, and apply a documented policy: run at the next valid time (03:00) on spring-forward, and run only the first occurrence on fall-back. Storing schedules in UTC to "avoid the problem" is wrong for human-facing schedules: the job would shift by an hour relative to business time twice a year. Test both transitions explicitly.

### 10.6 Level Signals

- **Mid:** durable job table, workers polling, retries with backoff.
- **Senior:** leases plus fencing tokens; idempotent run creation; at-least-once stated and justified; burst math and smoothing; DST and misfire policies.
- **Staff:** separates control plane (scheduling) from data plane (execution); per-tenant SLOs and fairness; multi-region ownership without double firing; evolution path from one database to a partitioned queue; operator tooling (pause a tenant, bulk retry, backfill).

---

## 11. Mock 8: Metrics and Monitoring System

Worked design: [HLD §6.13 Metrics, Logging, and Monitoring System](../computer-science/High_Level_Design.md#613-metrics-logging-and-monitoring-system).

### 11.1 Prompt

> "Design a metrics and monitoring system for our fleet of 100,000 hosts: collection, dashboards, and alerting."

### 11.2 Hidden Expectations

- A **time-series data model** (metric name plus labels identify a series) and what that implies for indexing.
- A write path sized for about 10M samples/s: sharded ingesters, WAL, compressed in-memory head blocks, immutable blocks in object storage.
- **Cardinality** as the defining failure mode, with enforcement.
- **Downsampling/rollups** and query splitting for long ranges.
- **Alerting pipeline:** rule evaluation, deduplication, grouping, inhibition, routing; and **meta-monitoring**.
- Correct **percentile aggregation** (histograms or mergeable sketches, never averaging p99s).
- Trap: writing each sample as a row in a relational database; one global alert evaluator with no failure story.

### 11.3 Clarifying Questions

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| How many hosts and series per host? | 100k hosts, ~1,000 series each | 100M active series |
| Scrape or push interval? | 10 s | 10M samples/s |
| Retention and resolution? | Raw 15 days, rollups for 1-2 years | Tiered storage |
| Query latency? | Last hour under 1 s; last year in a few seconds | Rollups, caches |
| Alert latency? | Paged within about a minute of a condition | Evaluation interval |
| Logs and traces too? | Metrics first; logs briefly | Scope |
| Multi-tenant? | Yes, many teams | Per-tenant limits |

### 11.4 Model Answer Outline

**Estimates (from the worked design).** 100M active series and 10M samples/s; with Gorilla-style compression at about 1.5 bytes/sample, raw ingest is about 15 MB/s, or 1.3 TB/day. Index memory is about 2 KB per active series, roughly 200 GB, which means about 50 ingesters, or about 150 with three replicas. A year of one series is 3.15M points at 10 s but 8,760 at 1 h. **Cardinality is a memory budget, and rollups make long queries feasible.**

**Design.** Agents scrape locally and push batches; a gateway authenticates and enforces per-tenant rate and series limits; samples are hashed by series to three ingesters (WAL plus in-memory head); every two hours ingesters cut blocks to object storage; a compactor merges, deduplicates replicas, and builds rollups; a query frontend splits and caches; rule evaluators feed an alert manager; a separate meta-monitoring stack watches it all.

**Deep dive: cardinality enforcement.** Track active series per tenant and per metric in the gateway (approximate counts, for example with HyperLogLog, are enough). Accept samples for existing series, reject *new* series beyond the limit, and report which label is exploding.

### 11.5 Follow-Ups With Model Answers

**Q1. A team adds a `user_id` label to a request counter.**

With 10M users, that one change can create 10M new series. At about 2 KB each, that is 20 GB of ingester memory, enough to push ingesters out of memory and take down monitoring for everyone. Prevent it at three layers: (1) per-tenant and per-metric **active-series limits** at the gateway, which reject new series beyond the limit but keep accepting existing ones; (2) cardinality reporting (top metrics and labels by series count) so teams see the problem; (3) instrumentation review or CI lint rules that flag unbounded label values. High-cardinality detail belongs in logs, traces, or exemplars attached to metrics, not in metric labels.

**Q2. An ingester dies.**

Every sample went to three ingesters, so queries still see the data from the other two replicas and deduplicate. The restarted ingester replays its WAL to rebuild its in-memory head. If the node is gone for good, its hash-ring tokens move to other ingesters, which start receiving its series. Duplicates are harmless because a sample is identified by `(series, timestamp)`, so writing it twice is idempotent and the compactor merges replica blocks. The thing to watch is the replication factor during the recovery window: a second failure in the same replica set would lose recent unflushed data.

**Q3. Who monitors the monitoring system?**

A small, independent meta-monitoring stack in a different failure domain (another region or cluster) that scrapes the main system's health: ingestion lag, rule-evaluation failures, alert-delivery success. Plus a **dead man's switch**: an alert that always fires and is sent to an external paging service, which pages if the heartbeat *stops*. Add synthetic probes that write a known series and check that it can be queried. Without these, the failure mode is silence, which looks exactly like "everything is fine."

**Q4. A dashboard shows "p99 latency" for a service running on 1,000 hosts. How is it computed?**

Not by averaging per-host p99s, which is mathematically meaningless: the average of p99s is not the p99 of the union, and hosts with little traffic count as much as busy ones. Use **histograms** with fixed bucket boundaries: bucket counts are mergeable, so sum counts across hosts and then estimate the quantile from the merged buckets (the error is bounded by the bucket width around the quantile). Or use mergeable sketches such as t-digest or DDSketch (which gives a relative-error guarantee). Client-side summaries that pre-compute quantiles cannot be aggregated. See [Percentiles and Why the Mean Misleads](../computer-science/Performance_Engineering.md#13-percentiles-and-why-the-mean-misleads).

**Q5. Sample volume suddenly rises 10x.**

Usually this is a deploy that changed labels, or agents flushing a backlog after a network outage. Protect the system: gateways enforce per-tenant rate limits with backpressure (HTTP 429), agents buffer to local disk (bounded, for example two hours) and replay at a capped rate, and live data is prioritized over backfill so dashboards stay current. Ingesters keep headroom (run at 50-60% of capacity) because resharding under load moves series and makes things worse. Identify the source with per-tenant ingestion metrics, and shed low-priority tenants if needed.

**Q6. A one-year dashboard takes 40 seconds to load.**

Serve long ranges from rollups (1-hour resolution is 360x fewer points than 10 s). Split queries by day and cache completed days, which are immutable. Precompute expensive aggregations with recording rules. Cap the number of series a query may touch and fail fast with a clear error rather than overloading queriers. Check which resolution the query actually used: raw-resolution queries over a year are the usual culprit.

**Q7. A network partition causes 5,000 alerts to fire at once.**

That is an **alert storm**, and it buries the one alert that matters. The alert manager should **group** alerts (one notification per cluster and alert name), **inhibit** downstream alerts while an upstream "cluster unreachable" alert is active, **deduplicate** across its own HA replicas, and support silences for maintenance. Longer term, alert on user-facing symptoms such as SLO burn rate (multi-window: page when both a 1-hour and a 5-minute window burn the error budget fast) rather than on every cause.

**Q8. Make it multi-region.**

Ingest and store data in the region where it is produced, so a WAN partition does not stop collection, and **evaluate alert rules regionally** so alerting keeps working when the region is cut off from the rest. A global query layer federates across regions for dashboards, and cross-region aggregates are produced by recording rules that ship small, pre-aggregated series to a global store. The meta-monitoring stack for each region lives outside that region.

### 11.6 Level Signals

- **Mid:** agents, a time-series database, dashboards, threshold alerts.
- **Senior:** ingest sizing, compression, the inverted index, cardinality limits, rollups, histogram-based percentiles, alert grouping and inhibition.
- **Staff:** "the monitoring system must be more available than what it monitors" as a design principle; meta-monitoring and dead man's switch; regional independence; tenant governance (limits, chargeback, label hygiene); SLO-based alerting as an organizational practice.

---

## 12. Mock 9: GPU Profiling Telemetry Service

Worked design: [ML Systems Design §7 Fleet-Wide GPU Profiling and Telemetry Service](../ml-gpu/ML_Systems_Design.md#7-case-study-fleet-wide-gpu-profiling-and-telemetry-service) (overhead budget, counter collection at fleet scale, regression detection, privacy). Single-workload tooling background: [Project Deep Dive: rocprof-compute, Profile Mode and Counter Collection](../career/Project_Deep_Dive_rocprof-compute.md#6-profile-mode-and-counter-collection). This is the mock most likely to turn into a conversation about your own work, so practice it until the numbers are automatic.

### 12.1 Prompt

> "We run 10,000 GPU nodes with 8 GPUs each. Design a service that continuously collects GPU performance telemetry across the fleet, lets engineers drill into any job's kernels, and automatically detects performance regressions when we roll out new drivers or ROCm versions."

### 12.2 Hidden Expectations

- **Overhead as a first-class requirement.** The profiler must never be why a customer job is slow. A strong candidate states a budget (for example under 1% always-on) before drawing anything.
- **Tiered collection**: cheap device-level telemetry always on; kernel timing aggregated on the node; hardware counters sampled; full traces only on demand.
- **Volume math** showing that shipping raw kernel records is impossible, so aggregation happens on the node.
- Knowing why **hardware counters are hard in production**: few counter slots per hardware block per pass, application replay is impossible for a live job, and per-dispatch counter collection serializes kernels.
- **Regression detection with statistics and confounders**: clocks, power caps, thermal throttling, input shapes, and many simultaneous comparisons.
- **Privacy and multi-tenancy**: kernel names and shapes can reveal a customer's model.
- Trap: treating "GPU utilization" as a performance metric; designing a pipeline that blocks the job when the network is slow.

### 12.3 Clarifying Questions

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| Hardware and workloads? | MI300X-class, some mixed SKUs; training and inference; some external tenants | Per-SKU baselines; privacy |
| Overhead budget? | Always-on under 1% throughput; deeper profiling only opt-in or on a small sample | Tiered collection |
| Which questions must it answer? | "Why is job X slow?", "Did ROCm version Y regress kernel Z?", "Which nodes are unhealthy?" | Data model and indexes |
| Freshness? | Node health within a minute; regression report within a day of rollout start | Stream for health, batch for regressions |
| Retention? | Aggregates 1 year; raw traces 1-2 weeks | Storage tiers |
| Can we change workloads? | No code changes; the job launcher can inject environment and libraries | Profiling via a tool library loaded at launch |
| Who are the users? | Fleet SREs, kernel and compiler engineers, job owners | Access control and views |

### 12.4 Model Answer Outline

**Requirements.** Functional: always-on device telemetry, per-job kernel summaries, on-demand deep capture, fleet regression reports, node health alerts. Non-functional: under 1% overhead, never block or crash the job, tenant isolation, data loss tolerated for telemetry but not silently (gaps must be visible). Out of scope: automatic kernel tuning.

**Estimates.**

```text
Fleet:                10,000 nodes × 8 = 80,000 GPUs
Tier 1 device metrics (always on): ~50 metrics/GPU at 1 Hz (power, clocks, temperature, utilization, HBM used,
                      ECC and link error counts) -> 80k × 50 = 4M samples/s
                      ~1.5 B/sample compressed ≈ 6 MB/s ≈ 0.5 TB/day      -> same scale as Mock 8; reuse that TSDB
Tier 2 kernel timing: assume ~5,000 dispatches/s per busy GPU, ~100 B per raw record
                      raw: 500 KB/s/GPU × 80k ≈ 40 GB/s ≈ 3.5 PB/day        -> cannot ship raw
                      aggregate per (job, GPU, kernel signature, 60 s window) -> {count, sum, min, max, ~32-bucket histogram}
                      ~500 active signatures/GPU/min × ~300 B ≈ 2.5 KB/s/GPU -> 80k × 2.5 KB/s ≈ 200 MB/s ≈ 17 TB/day raw,
                      a few TB/day after columnar compression                -> ~200x reduction on the node
Tier 3 counters:      each GPU samples one counter group (fits in one pass) for 10 s every 10 min, groups rotated
Tier 4 deep capture:  on demand; kernel + API traces ≈ ~150 MB per GPU-minute (assumption)
                      2 minutes of a 512-GPU job ≈ 150 GB                   -> object storage, quota, 14-day retention
Overhead check:       if a dispatch record costs ~2 µs of host time, 5,000 dispatches/s = 10 ms/s = 1% of the launching thread's time
                      -> ~1% throughput loss only if the job is launch-bound (many tiny kernels); near 0% if the GPU queue stays full
                      -> overhead scales with dispatch rate, so small-kernel workloads need sampling
                      (ML Systems Design §7 assumes ~1 µs with buffered tracing; 2 µs here is deliberately pessimistic)
```

State the two assumptions that matter (dispatch rate and per-dispatch cost) and say you would measure both before committing.

**Design.**

```text
Job process: profiling tool library (ROCprofiler-SDK based, injected by the launcher)
             kernel timestamps -> bounded shared-memory ring buffer (drop oldest, never block)
Node agent (separate process, CPU/memory capped by cgroup):
             AMD SMI device metrics at 1 Hz; drains the ring; aggregates per minute; samples counter groups as told;
             bounded local disk buffer; ships batches; obeys control-plane config and kill switch
Control plane: config service (tier per cluster/job, counter-group rotation, sampling rates), on-demand capture API,
               global and per-job kill switches
Ingest:      gateway (auth, per-cluster quotas) -> durable log partitioned by node
             -> device metrics -> TSDB (alerts: thermal, ECC, link errors, stragglers -> scheduler drains bad nodes)
             -> kernel aggregates -> columnar store, partitioned by day, sorted by (kernel_sig, sku, rocm_version)
Deep traces: agent uploads files (rocpd database / Perfetto / OTF2) to object storage; metadata row indexed by job, rank, time
Joins:       scheduler (job <-> nodes and ranks), inventory (SKU, firmware), software versions reported by the agent
Users:       job view (per-rank timelines, top kernels, straggler ranks), fleet view, regression reports
```

**Deep dive 1: the overhead budget and tiers.**

| Tier | Data | Mechanism | Overhead | Scope |
|---|---|---|---|---|
| 1 | Power, clocks, temperature, utilization, memory, errors | AMD SMI library or `amd-smi metric` polling | Negligible (out of process) | Always, everywhere |
| 2 | Kernel names, durations, launch shapes | Kernel-dispatch tracing in the tool library, aggregated on node | Grows with dispatch rate; target well under 1% | Always, adaptively sampled |
| 3 | Hardware counters | Device-wide counter sampling over an interval (no per-kernel attribution) | Low | Rotating groups, fleet-wide |
| 4 | Full traces, per-dispatch counters, PC sampling | `rocprofv3` style capture (`--kernel-trace`, `--pmc`, PC sampling) or rocprof-compute | High: per-dispatch counters serialize kernels | Opt-in, minutes, few ranks |

**Deep dive 2: regression detection.** Define a **kernel signature** (kernel name hash plus grid size, workgroup size, and LDS size) so the same kernel with different shapes is not mixed. For each signature, compare duration distributions between cohorts that differ only in the software version: same SKU, same firmware, windows where the GPU was not power- or thermal-throttled (Tier 1 tells you), ideally the same job types across a rollout boundary. Use per-job medians as the unit of analysis (dispatches within a job are correlated). Detecting a 3% shift when per-job variation has a 10% coefficient of variation needs about `2 × (1.96 + 0.84)^2 × (10/3)^2 ≈ 175` jobs per cohort for 80% power at a 5% significance level. With thousands of signatures tested at once, control the false-discovery rate (Benjamini-Hochberg) and require a minimum effect size so the report is not noise. Integrate with the rollout: new drivers go to a 1% canary first, and the comparison gates the next stage.

### 12.5 Follow-Ups With Model Answers

**Q1. A customer says your profiler costs them 15% throughput.**

First, stop the bleeding: the per-job kill switch in the control plane disables Tiers 2-4 for that job within seconds. Then find the cause. A 15% hit is far above what Tier 1 or a sampled Tier 2 should cost, so likely suspects are (a) a workload with a very high dispatch rate (many tiny kernels, common in decode-heavy inference), where per-dispatch tracing cost scales up; or (b) per-dispatch counter collection left on, which serializes kernels and destroys concurrency. Fixes: the agent estimates overhead as `dispatch_rate × per-dispatch cost` and automatically drops to sampling (trace one window in N) when it exceeds the budget; Tier 4 always has a time limit. Prove the budget continuously: hold out a random 1% of nodes with Tiers 2-3 off and compare the throughput of comparable jobs. Overhead becomes a monitored SLO, not a claim.

**Q2. The counters you need take six passes, but you cannot replay a production job.**

Application replay is a tool for single workloads, not a fleet. Use **statistical multiplexing across the fleet**: split counters into groups that each fit in one pass (keeping every counter of a ratio metric in the same group, so the ratio comes from one measurement window), and assign different groups to different GPUs and time windows. With 80k GPUs rotating through six groups every 10 minutes, every common kernel signature or job type collects every group many times per day. This is the fleet-scale version of rocprof-compute's iteration multiplexing, with the same assumption: the sampled windows are statistically alike. Collect device-wide over an interval to avoid kernel serialization; per-kernel attribution of counters is reserved for opt-in Tier 4 captures.

**Q3. How would you detect a 3% regression in one kernel after a ROCm upgrade?**

As in deep dive 2: a precise kernel signature, matched cohorts that differ only in the software version, exclusion of throttled windows (or normalization by measured clock frequency), per-job medians as independent units, a sample size computed from measured variance (about 175 jobs per cohort at 10% CV), a test such as a bootstrap confidence interval on the ratio of medians or Mann-Whitney U, false-discovery-rate control across thousands of signatures, and a minimum effect size. Report the regression with evidence: before and after histograms, cohort sizes, and confounders checked. Validate the pipeline by injecting a known slowdown into a canary and checking that it is detected. See [Statistics for Engineers](../computer-science/Math_Probability_Estimation.md#6-statistics-for-engineers) and [A/B Methodology](../computer-science/Performance_Engineering.md#85-ab-methodology).

**Q4. One 16,000-GPU training job floods the pipeline.**

That job is 20% of the fleet. If ingest were partitioned by job ID, it would be a hot partition. Partition ingest by **node** instead, so its load spreads across all partitions, and aggregate per job in a second stage (node aggregates, then job aggregates). Its Tier 2 data is still only 20% of the 200 MB/s total, which the pipeline is sized for. For deep captures, do not trace all 16k ranks: capture a handful of ranks plus the stragglers identified from Tier 2 (ranks whose step time or collective wait time is an outlier). Precompute per-job summaries so the UI never scans raw rows for a job of that size.

**Q5. The agent crashes, or the node loses network for an hour.**

The agent is a separate process, so its crash cannot crash the job. The tool library in the job writes into a bounded shared-memory ring and **drops the oldest data rather than blocking** when the agent is gone; a restarted agent resumes draining. During a network outage the agent buffers to bounded local disk (for example 2 GB), dropping lowest-priority tiers first. Every batch carries an idempotency key `(node, gpu, tier, window_start)`, so replays after reconnection are deduplicated: delivery is at-least-once, aggregates are effectively-once. Gaps are recorded explicitly so a regression report never mistakes missing data for a performance change.

**Q6. An engineer asks why yesterday's 512-GPU job ran 20% slower than usual.**

Start in the job view: compare per-rank step times from Tier 2. If one rank is slower and the rest wait in collectives (time in RCCL kernels rises on every other rank), it is a **straggler**: check that node's Tier 1 data for lower clocks (thermal or power throttling), rising ECC or link error counts, or a different firmware version. If all ranks are uniformly slower, compare top kernels by total time against the job's previous runs: a changed kernel signature points at a software change (new library version, different shapes); unchanged kernels with longer durations point at the platform (driver, clocks). Then schedule a Tier 4 capture of the slow rank and one healthy rank on the next run for a side-by-side comparison.

**Q7. Kernel names reveal what model a customer is training. How do you handle privacy?**

Per-tenant access control: job owners see full data for their own jobs. Fleet-wide analysis uses **tokenized kernel signatures** (a keyed hash of the name plus shapes), so fleet engineers can see "signature 7f3a regressed 4% on ROCm version Y" without seeing the name; the tenant can be notified and can reveal it. Deep traces require tenant opt-in, are encrypted at rest, have short retention, and are audited on access. Cross-tenant aggregates are reported only for cohorts with a minimum number of tenants (k-anonymity), so one tenant's workload cannot be inferred.

**Q8. Several clusters in different regions.**

Telemetry volume is large, so ingest and store **per cluster**, close to the source; a WAN problem then does not stop collection or local alerting. Regression analysis needs fleet-wide data, but it only needs aggregates: daily per-signature, per-version summaries are small and replicate to a global store. The control plane is global, but agents cache their last configuration, so a control-plane outage changes nothing on the nodes; the kill switch is also deliverable per cluster.

### 12.6 Level Signals

- **Mid:** agents on nodes, a time-series store, dashboards, some notion of sampling.
- **Senior:** an explicit overhead budget; volume math forcing on-node aggregation; tiers; counter-slot limits and why replay does not work in production; never-block design; statistically sound regression detection.
- **Staff:** treats overhead and privacy as contracts with customers (measured, enforced, auditable); ties regression detection into the driver and ROCm rollout process as a release gate; designs for the organization: SREs, kernel engineers, and tenants get different views and permissions; knows which parts to reuse (the metrics system from Mock 8) instead of rebuilding.

---

## 13. Mock 10: LLM Inference Serving

Worked design: [ML Systems Design §4 LLM Inference Serving Platform](../ml-gpu/ML_Systems_Design.md#4-case-study-llm-inference-serving-platform), with deep dives on [continuous batching](../ml-gpu/ML_Systems_Design.md#45-deep-dive-continuous-batching-and-slos), [KV-cache memory](../ml-gpu/ML_Systems_Design.md#46-deep-dive-kv-cache-memory-management), and [prefill/decode disaggregation](../ml-gpu/ML_Systems_Design.md#48-deep-dive-prefilldecode-disaggregation). Model arithmetic: [§3.3](../ml-gpu/ML_Systems_Design.md#33-model-arithmetic).

### 13.1 Prompt

> "Design the serving system for a 70B-parameter chat model. We expect about a million daily users. You have MI300X GPUs."

### 13.2 Hidden Expectations

- **Physics first:** weights 141 GB in BF16; KV cache 320 KiB per token; decode is HBM-bandwidth-bound at small batch, which is why batching is the main lever.
- **Capacity math tied to SLOs** (TTFT and TPOT), using Little's law for concurrency and KV memory.
- **Continuous batching** with a KV-cache manager (paged allocation, admission control, preemption).
- **Router** decisions: load-aware, prefix-cache-aware, multi-tenant fairness.
- Choice of **tensor-parallel degree** and replica count from the numbers.
- Failure handling for long-lived streaming requests, and why autoscaling is slow.
- Trap: sizing by "GPU utilization"; ignoring prefill cost; assuming the model fits on one GPU without accounting for KV.

### 13.3 Clarifying Questions

| Ask | Typical answer | Why it changes the design |
|---|---|---|
| Model architecture? | Dense, Llama-3-70B-like: 80 layers, GQA with 8 KV heads | Weight and KV sizes |
| Traffic shape? | 1M DAU, 10 requests/user/day, ~1,000 prompt tokens, ~300 output tokens, 3x peak | Prefill vs decode load |
| SLOs? | TTFT p99 under 1 s; TPOT p99 under 30 ms (about 33 tokens/s per user) | Batch size limits |
| Context length? | 8k typical; 128k for some customers later | KV memory, routing pools |
| Precision? | BF16 now; FP8 acceptable if quality is verified | Memory and bandwidth halved |
| Tenancy? | Many API customers plus our own chat app | Fairness, quotas, priorities |
| Streaming? | Yes, token streaming | Long-lived connections, failure handling |

### 13.4 Model Answer Outline

**Physics (5-12 min).** Weights: 70.6B × 2 B = 141 GB. KV per token: `2 × 80 × 8 × 128 × 2 B` = 320 KiB. Inference FLOPs: about `2N` = 1.4e11 per token. Decode at small batch reads all weights per step and does about 1 FLOP per byte, far below the MI300X ridge point of about 247 FLOP/B, so it is bandwidth-bound and **batching is the throughput lever**. Prefill is compute-bound.

```python
"""Napkin math for Mock 10: a 70B dense model in BF16 on MI300X-class GPUs."""
GB = 1e9
N = 70.6e9                       # parameters (Llama-3-70B class)
WEIGHT_BYTES = 2 * N             # BF16
KV_PER_TOKEN = 320 * 1024        # 2 (K,V) x 80 layers x 8 KV heads x 128 dim x 2 B
FLOPS_PER_TOKEN = 2 * N          # forward pass; attention FLOPs ignored at ~1k context
PEAK = 1.307e15                  # MI300X dense BF16 FLOP/s
HBM_BW = 0.75 * 5.3e12           # assume ~75% of peak HBM bandwidth is achievable
HBM_CAP = 192 * GB
EFF = 0.5                        # assumed fraction of peak FLOP/s reached by prefill GEMMs

dau, reqs_per_user, prompt, output, peak_factor, tpot = 1e6, 10, 1000, 300, 3, 0.030

req_s = dau * reqs_per_user / 86_400 * peak_factor
prefill_tok_s, decode_tok_s = req_s * prompt, req_s * output
print(f"peak: {req_s:.0f} req/s, {prefill_tok_s:,.0f} prompt tok/s, {decode_tok_s:,.0f} output tok/s")
print(f"GPU-equivalents of FLOPs at {EFF:.0%} of peak: "
      f"prefill {prefill_tok_s * FLOPS_PER_TOKEN / (EFF * PEAK):.0f}, "
      f"decode {decode_tok_s * FLOPS_PER_TOKEN / (EFF * PEAK):.0f}")

concurrent = req_s * (output * tpot + 0.5)          # Little's law: rate x time in system
avg_ctx = prompt + output / 2
print(f"concurrent sequences ≈ {concurrent:,.0f}; KV in use ≈ "
      f"{concurrent * avg_ctx * KV_PER_TOKEN / GB:,.0f} GB")

total_gpus = 160
print(f"\nDecode step estimate with {total_gpus} GPUs (memory time vs compute time per step):")
for tp in (2, 4, 8):
    replicas = total_gpus // tp
    seqs = concurrent / replicas
    bytes_per_gpu = (WEIGHT_BYTES + seqs * avg_ctx * KV_PER_TOKEN) / tp
    mem_ms = bytes_per_gpu / HBM_BW * 1e3
    compute_ms = seqs * FLOPS_PER_TOKEN / tp / PEAK * 1e3
    hbm_used = bytes_per_gpu / HBM_CAP
    ttft_ms = prompt * FLOPS_PER_TOKEN / (tp * EFF * PEAK) * 1e3
    print(f"  TP={tp}: {replicas:3d} replicas, {seqs:4.0f} seqs each, step ≈ {mem_ms:4.1f} ms "
          f"(compute {compute_ms:.1f} ms), HBM used {hbm_used:4.0%}, prefill of one prompt ≈ {ttft_ms:.0f} ms")
```

Output:

```text
peak: 347 req/s, 347,222 prompt tok/s, 104,167 output tok/s
GPU-equivalents of FLOPs at 50% of peak: prefill 75, decode 23
concurrent sequences ≈ 3,299; KV in use ≈ 1,243 GB

Decode step estimate with 160 GPUs (memory time vs compute time per step):
  TP=2:  80 replicas,   41 seqs each, step ≈ 19.7 ms (compute 2.2 ms), HBM used  41%, prefill of one prompt ≈ 108 ms
  TP=4:  40 replicas,   82 seqs each, step ≈ 10.8 ms (compute 2.2 ms), HBM used  22%, prefill of one prompt ≈ 54 ms
  TP=8:  20 replicas,  165 seqs each, step ≈  6.4 ms (compute 2.2 ms), HBM used  13%, prefill of one prompt ≈ 27 ms
```

**What the numbers decide.**

- **Prefill dominates the FLOPs** (75 vs 23 GPU-equivalents) because prompts are 3x longer than outputs. Prefix caching of shared system prompts is the biggest cost lever, not decode tuning.
- About **100 GPU-equivalents** of compute at peak, so **160 GPUs** (20 nodes) gives roughly 40% headroom for burst, failures, and imperfect batching.
- **TP=4** (two replicas per 8-GPU node) keeps the decode step near 11 ms, leaving room under the 30 ms TPOT SLO for interleaved prefill chunks and all-reduce latency. TP=8 is faster per step but halves replica count and spends more on per-layer communication; TP=2 leaves too little TPOT headroom once prefill is interleaved. On the MI300X full mesh, a TP=4 group uses 3 of each GPU's 7 xGMI links.
- HBM is mostly free (22% used), so spend it on **prefix cache** and on headroom for long-context requests.
- These are napkin numbers: ignore communication, attention FLOPs, and scheduler inefficiency. Say you would validate with a load test before ordering hardware.

**Design (12-27 min).**

```text
Clients -> API gateway (auth, per-tenant token quotas, streaming over SSE/WebSocket)
        -> Router (load-aware + prefix-aware; picks a replica by queue depth, KV free, prefix-cache hit)
        -> Replica = 4 GPUs, one engine process:
             scheduler: continuous batching, chunked prefill, admission by free KV blocks, preemption
             KV manager: paged blocks, prefix cache (hash of token blocks), LRU eviction
             model executor: TP=4 kernels, all-reduce over xGMI
        -> tokens stream back through the router to the client
Control plane: model registry, weight distribution (local NVMe cache), autoscaler on queue wait and KV usage,
               health checks; metrics: TTFT, TPOT, queue wait, KV usage, preemptions, goodput, tokens/s per GPU
```

**Deep dives (27-40 min).** Continuous batching (requests join and leave the batch every step; chunked prefill keeps long prompts from stalling everyone's decode); KV paging (fixed-size blocks remove fragmentation; admission control by free blocks; preempt by swapping or recomputing). If prefill/decode interference still breaks TPOT, discuss **disaggregation**: separate prefill and decode pools, transferring about 330 MB of KV per 1,000-token prompt (about 6-7 ms over a 50 GB/s NIC).

### 13.5 Follow-Ups With Model Answers

**Q1. A GPU node dies while 160 requests are streaming from it.**

With TP=4 and two replicas per node, both replicas on the node are lost, along with their KV caches. The router sees the failed streams (RPC errors or missed health checks) and **re-dispatches each request to a healthy replica with the prompt plus the tokens already streamed**, so generation continues where it stopped; the client sees a pause of roughly one re-prefill plus queueing (tens to hundreds of milliseconds), not an error. The router must keep the streamed tokens per in-flight request to make this possible. Capacity comes from the ~40% headroom sized in §13.4 (one node is two of 40 replicas, 5% of capacity). Replacement capacity takes time: loading 141 GB of weights from local NVMe at about 6 GB/s takes about 25 s, and much longer from remote storage, so keep weights cached on local NVMe and keep a few warm spare replicas.

**Q2. Traffic spikes 10x in five minutes.**

GPUs cannot be added in seconds (provisioning plus model load, and the capacity may not exist), so the answer is **admission control and graceful degradation**, not autoscaling. Predict queue wait per request; if it would break the TTFT SLO, reject early with 429 and `Retry-After` rather than accept and time out. Prioritize: paid interactive traffic over free tier over batch, and preempt batch jobs. Temporarily cap `max_tokens`, and route overflow to a smaller or quantized model if the product allows. Do not let each replica's batch grow until KV runs out: by Little's law, 10x arrivals means 10x concurrency (12 TB of KV), which would cause preemption thrash and break TPOT for everyone. Meanwhile, scale up from a reserved pool and use predictive scaling for daily peaks.

**Q3. Some customers send 128k-token prompts.**

KV per sequence becomes `131,072 × 320 KiB = 40 GiB`, so a TP=4 replica (768 GB HBM minus 141 GB of weights) holds about 15 such sequences, versus hundreds of short ones. Prefill becomes expensive: at 128k tokens, attention adds about `4 × L × h × average_context` ≈ 1.7e11 FLOPs per token on top of the 1.4e11 for the weights, so roughly 4e16 FLOPs in total, about 15 s on one TP=4 replica at 50% efficiency. Responses: **route long-context requests to a separate pool** (more GPUs per replica, or context parallelism) so they do not wreck short-request latency; use chunked prefill; use prefix caching for documents sent repeatedly; consider FP8 KV (half the memory) after a quality check; and agree a different TTFT SLO for long contexts.

**Q4. One tenant's 4,000-token system prompt is in 30% of all requests.**

That is a hot prefix, and an opportunity: its KV (`4,000 × 320 KiB ≈ 1.2 GiB` (1.3 GB)) can be computed once per replica and reused. For those requests only the user-specific suffix needs prefill; if they average 4,500 prompt tokens, their prefill work drops by almost 90%, and prefill is the dominant cost in this workload. Route with **prefix affinity** (consistent hashing on the prefix hash, with bounded load so the hot prefix spreads over several replicas instead of melting one), and pin the hot prefix's blocks so LRU does not evict them. Measure prefix-cache hit rate per tenant.

**Q5. Serve users in the US, Europe, and Asia.**

Deploy replicas in each region; time to first token includes network round trips, and a 150 ms cross-ocean round trip is a visible fraction of a 1 s TTFT budget. A global load balancer sends users to the nearest region with capacity and spills over to another region when one is saturated, unless **data residency** rules (for example, EU prompts must stay in the EU) forbid it; residency is often the binding constraint, so ask. Prefix caches are regional, and multi-turn conversations should stick to one region (ideally one replica) to reuse the conversation's KV prefix.

**Q6. Billing must be exact even with retries and failures.**

Every request carries a client-supplied idempotency key. The engine meters prompt and generated tokens per request at completion (or at disconnect) and writes a usage record keyed by request ID to a durable log; billing aggregation deduplicates on that key, so a retried or re-dispatched request is billed once. Define the policy for partial work: for example, bill only tokens actually delivered to the client, and do not bill the re-prefill caused by your own node failure. Exactly-once billing comes from idempotent accounting, not from exactly-once execution.

**Q7. One tenant floods the system and everyone's latency suffers.**

Enforce **per-tenant token-rate quotas** at the gateway (counting prompt and output tokens, since prefill is the main cost), **weighted fair queuing** per tenant at the router, and per-tenant caps on concurrent sequences and KV share inside each replica's scheduler. Batch or offline traffic goes to a lower priority class that is preempted first. Report per-tenant TTFT and TPOT so noisy-neighbor effects are visible.

**Q8. Which metrics drive autoscaling and alerts? Is GPU utilization enough?**

No. "GPU utilization" reports the fraction of time any kernel is running, which can read 100% while decode uses a small fraction of peak FLOPs or bandwidth. Scale on **queue wait time** and **KV-cache usage** (leading indicators of SLO breach), alert on TTFT and TPOT percentiles per priority class, and track **goodput** (requests per second meeting both SLOs), tokens per second per GPU, preemption rate, and cost per million tokens. Because adding capacity takes minutes, combine reactive scaling with schedule-based scaling for the daily peak.

### 13.6 Level Signals

- **Mid:** knows the model needs several GPUs, uses batching, puts a load balancer in front, streams tokens.
- **Senior:** does the weight, KV, and FLOP arithmetic; identifies decode as bandwidth-bound and prefill as compute-bound; uses Little's law for concurrency and KV; explains continuous batching, paged KV, and admission control; picks a TP degree with reasons.
- **Staff:** turns the numbers into a cost model ($/1M tokens, the prefix-cache lever); designs separate pools for long context and batch traffic; plans for slow capacity (reserved pools, degradation ladders); covers multi-tenancy, residency, and billing correctness; decides when disaggregation is worth its complexity.

---

## 14. Twenty Unsolved Practice Prompts

Run these with the same 45-minute procedure. Hint outlines are in [Answers](#answers); read one only after your attempt. Prompts 17-20 are specific to GPU/HPC and tooling roles.

| # | Prompt (as the interviewer would say it) | Focus | Difficulty |
|---|---|---|---|
| P1 | "Design a distributed message queue (a durable, partitioned log) that ingests 1 GB/s and serves many independent consumer groups." | Replication, ordering, delivery semantics | Hard |
| P2 | "Design a collaborative document editor where many people edit the same document at once, including offline." | OT vs CRDT, sessions | Hard |
| P3 | "Design a file sync service like Dropbox." | Chunking, dedupe, metadata consistency, conflicts | Medium |
| P4 | "Design a photo-sharing service with albums, privacy settings, and image processing." | Upload pipeline, CDN, async processing | Medium |
| P5 | "Design a real-time leaderboard for a game with 100M players, including 'what is my rank?'" | Sorted structures, sharded ranking | Medium |
| P6 | "Design an ad-click aggregation pipeline. Advertisers are billed from these counts, so they must be exact." | Stream processing, exactly-once, late data | Hard |
| P7 | "Design a distributed in-memory cache service used by hundreds of internal services." | Hashing, eviction, stampedes, invalidation | Medium |
| P8 | "Design a service that generates unique IDs for every object in the company: a million IDs per second, roughly time-ordered." | Snowflake layout, clocks | Easy |
| P9 | "Design a 'nearby places' service: given a location, return the best restaurants within 2 km." | Geospatial indexing | Medium |
| P10 | "Design the order matching engine for a stock exchange." | Determinism, latency, replication by replay | Hard |
| P11 | "Design a distributed tracing system for 2,000 microservices." | Context propagation, sampling | Medium |
| P12 | "Design a remote build cache and distributed build execution service for a large C++ monorepo." | Content addressing, hermeticity | Medium |
| P13 | "Design a feature-flag and dynamic configuration service." | Local evaluation, safe rollout | Easy |
| P14 | "Design an online coding judge that compiles and runs untrusted submissions." | Sandboxing, burst scheduling | Medium |
| P15 | "Design live comments and reactions for a stream with 10M concurrent viewers." | Massive fan-out, sampling | Hard |
| P16 | "Design a vector search service for retrieval-augmented generation over 1B documents." | ANN indexes, sharding, recall vs latency | Hard |
| P17 | "Design the nightly performance-regression CI for a GPU math library across five GPU generations." | Benchmark noise, change detection, bisection | Medium |
| P18 | "Design a crash-reporting service that collects, symbolicates, and groups crashes from millions of installs." | Ingestion bursts, symbolication, grouping | Medium |
| P19 | "Design the rollout system for GPU driver and firmware updates across a 10,000-node fleet." | Staged rollout, health gates, draining | Medium |
| P20 | "Design a multi-tenant GPU notebook service: engineers click a button and get JupyterLab with 1-8 GPUs." | Scheduling, idle reclamation, isolation | Medium |

---

## 15. Common Failure Modes Checklist

Run through this list after every mock, and once more the night before an interview. Each item is a real reason candidates are rejected, with the fix.

### Process and time

- [ ] **Drawing before asking.** Symptom: a diagram at minute 2. Fix: say the requirements out loud and write them down first, even for a "simple" prompt.
- [ ] **Requirements ping-pong.** Symptom: still asking questions at minute 8. Fix: ask the 4-6 questions that change the architecture, then state assumptions and move on.
- [ ] **No summary.** Symptom: the interview ends mid-sentence in a deep dive. Fix: at minute 42, stop and summarize, whatever state you are in.
- [ ] **Ignoring the interviewer's steer.** Symptom: "I'll get to that later" when they ask about something. Fix: their question is the rubric; answer it now.

### Requirements and scope

- [ ] **No non-functional requirements.** Symptom: nothing written about latency, availability, consistency, or durability. Fix: always produce a non-functional list, even if short.
- [ ] **Missed implied requirement.** Symptom: chat messages acknowledged before being durable; payments without idempotency. Fix: for every write, ask "can this be lost or duplicated, and what does the user see?"
- [ ] **No out-of-scope list.** Symptom: the interviewer later asks about a feature and you are unsure whether it was included. Fix: write "out of scope" explicitly.

### Estimation

- [ ] **Numbers without consequences.** Symptom: storage computed, never mentioned again. Fix: end every number with "so the design must...".
- [ ] **Average instead of peak.** Symptom: sizing for the 2,800 runs/s average when 2M runs land at midnight. Fix: always ask what the burst looks like.
- [ ] **Order-of-magnitude slip.** Symptom: 1B/day computed as 1,200/s instead of about 12,000/s. Fix: memorize the anchors (1M/day ≈ 12/s; 1B/day ≈ 12k/s) and sanity-check against per-node capacities.
- [ ] **Hardware peaks as achievable.** Symptom: sizing GPUs at 100% of peak FLOPs. Fix: state an efficiency (for example 40-60% for GEMM-heavy work, 70-85% of peak HBM bandwidth for streaming).

### Design

- [ ] **Boxes without purpose.** Symptom: a cache, queue, and three microservices that you cannot justify when asked "why?". Fix: introduce each component only in response to a requirement or a number.
- [ ] **No source of truth.** Symptom: unclear whether the cache, the queue, or the database is authoritative. Fix: name the system of record for each entity and which stores are derived and rebuildable.
- [ ] **Paths not walked.** Symptom: a diagram with no traced request. Fix: walk one write and one read end to end, including where the client gets its response.
- [ ] **Partition key not stated or hot.** Symptom: sharding "by ID" with no thought to skew; time-based keys that funnel all writes to one partition. Fix: state the key, the expected skew, and the hot-key plan.
- [ ] **Over-engineering at minute 10.** Symptom: Kubernetes, Kafka, and a service mesh before the first read path works. Fix: simplest working design first, then scale it.

### Correctness and failure

- [ ] **"Exactly-once" claimed.** Fix: say "at-least-once delivery plus idempotent processing gives effectively-once," and show the idempotency key.
- [ ] **Retries without idempotency or backoff.** Fix: idempotency keys on writes, exponential backoff with jitter, retry budgets.
- [ ] **No failure story for the stateful component.** Symptom: the cache, gateway, or leader dies and the answer is "we restart it." Fix: quantify the impact (keys lost, load shifted, recovery time) and the mitigation.
- [ ] **Leases without fencing.** Symptom: a paused worker resumes and overwrites newer results. Fix: monotonically increasing fencing tokens checked by the storage layer.
- [ ] **Quorums described as linearizable.** Fix: know what `R + W > N` does and does not give, and when consensus is needed.
- [ ] **Clock-dependent correctness.** Symptom: last-writer-wins by wall clock for important data; ordering by device timestamps. Fix: sequence numbers, version vectors, or a single sequencer.
- [ ] **No overload behavior.** Symptom: a 10x spike answered only with "autoscale." Fix: admission control, load shedding, priorities, degradation modes, and the fact that scaling takes minutes.

### Tradeoffs and communication

- [ ] **Single-option design.** Fix: for every major decision, name one real alternative and the condition under which it would win.
- [ ] **"It depends" with no dependency.** Fix: say what it depends on and pick an answer for the stated requirements.
- [ ] **Long silences or a 20-minute monologue.** Fix: think out loud, and check in at each phase transition ("Does this level of detail work, or should I go deeper here?").
- [ ] **Defensiveness under pushback.** Fix: engage with the argument; switch if they found a real gap, defend with requirements if not.
- [ ] **Name-dropping instead of mechanism.** Symptom: "use Cassandra" with no explanation of why it fits. Fix: describe the property you need (leaderless, LSM, tunable quorums) and then the product.

### GPU and ML specific

- [ ] **"GPU utilization" as a capacity metric.** Fix: use FLOP/s or bandwidth achieved, MFU, goodput, queue wait, and KV usage.
- [ ] **Forgetting the KV cache.** Fix: compute KV per token and per sequence before choosing GPUs per replica.
- [ ] **No overhead budget for profiling.** Fix: state the budget, how you measure it, and the kill switch.
- [ ] **One GPU failure treated as rare.** Fix: failure rate scales with GPU count; design recovery time, not just checkpoint frequency.

### 15.1 Interview Questions

**Q1. Which three failure modes cost candidates the most offers?**

In practice: (1) running out of time before failure handling and the summary, which makes even a good design look incomplete; (2) unjustified complexity, which signals pattern-matching rather than reasoning; and (3) weak follow-up answers, which reveal a memorized design. All three are fixed by the same habit: build the simplest design that meets the numbers by minute 22, then spend the rest of the time on depth and failure.

**Q2. How do you practice failure modes specifically?**

Use the follow-up lists in this file as drills without designing anything: pick a random mock, read one follow-up, and answer it out loud in under two minutes with a structure of impact, mitigation, and tradeoff ("1/6 of keys miss, the store sees 2.5x load; coalesce misses and keep an in-process LRU; costs memory and a little staleness"). Ten of these take 20 minutes and build the reflex that interviewers grade.

---

## Answers

Hint outlines for [section 14](#14-twenty-unsolved-practice-prompts). Each lists the clarifications that matter, the numbers that drive the design, the core design, the deep dive the interviewer is likely to want, and the classic traps.

### A1. Distributed Message Queue

- **Clarify:** ordering scope (per partition, not global), retention (for example 7 days), delivery semantics, number of consumer groups, message size.
- **Numbers:** 1 GB/s × 86,400 s ≈ 86 TB/day; 7 days ≈ 600 TB; replication factor 3 ≈ 1.8 PB. If a partition sustains on the order of 10 MB/s, about 100+ partitions are needed for ingress alone; size brokers by disk throughput and network (each byte is written 3 times and read once per consumer group).
- **Core design:** topics split into partitions; each partition is an append-only log of segment files with a leader and followers; producers batch and compress; consumers pull by offset; consumer-group offsets stored durably (for example in an internal compacted log); a controller (consensus-based) manages leadership and metadata.
- **Deep dive:** replication: in-sync replica set, high watermark (consumers read only fully replicated data), `acks=all` plus a minimum ISR size for durability; idempotent producers (producer ID plus sequence numbers) and transactions for exactly-once within the log; why reads are fast (sequential I/O, page cache, zero-copy sends).
- **Traps:** promising global ordering; per-message delete as in a work queue; thousands of partitions per broker without considering metadata and recovery time; unclean leader election losing acknowledged data.

### A2. Collaborative Document Editor

- **Clarify:** concurrent editors per document (tens, not thousands), rich text or plain, offline editing, history and undo, comments.
- **Numbers:** 100 editors × 5 operations/s = 500 ops/s per document, easily handled by one process, so the scaling unit is the document session, not the operation.
- **Core design:** a stateful session server per active document (sticky routing by document ID) that orders operations, broadcasts them over WebSockets, and appends them to an operation log; periodic snapshots so loading does not replay the whole history; presence and cursors on an ephemeral channel.
- **Deep dive:** operational transformation (central server transforms concurrent operations against each other; simpler with a server) vs CRDTs (operations commute by construction; better for offline and peer-to-peer; costs metadata and tombstone growth). Session-server failover: rebuild from snapshot plus log; clients resend unacknowledged operations.
- **Traps:** last-writer-wins on the whole document; locking paragraphs; treating it as a simple CRUD app.

### A3. File Sync (Dropbox)

- **Clarify:** file sizes, number of devices, sharing, version history, conflict policy.
- **Numbers:** 100M users × 5 GB average ≈ 500 PB logical before dedupe; most changes are small edits to large files, so transfer deltas, not files.
- **Core design:** split files into blocks (for example 4 MB, or content-defined chunking so an insertion does not shift every block), address blocks by content hash, upload only unknown blocks to object storage, and commit a new file version (a list of block hashes) to a strongly consistent metadata service; devices learn about changes through long-poll or push notifications and download missing blocks.
- **Deep dive:** the commit protocol (upload blocks first, then atomically commit metadata with a version check), conflict handling (concurrent edits to the same base version produce a "conflicted copy" rather than silent loss), cross-user dedupe and its privacy implications.
- **Traps:** storing file bytes in the metadata database; re-uploading whole files on every change; ignoring the case of two devices editing offline.

### A4. Photo Sharing With Image Processing

- **Clarify:** uploads per day, photo size, derivative sizes, privacy model, feed or albums only.
- **Numbers:** 100M uploads/day × 3 MB ≈ 300 TB/day of originals plus derivatives; reads are far higher and are served from a CDN.
- **Core design:** clients upload directly to object storage with pre-signed URLs (resumable for large files); an upload-complete event triggers an asynchronous pipeline: validation, EXIF/location stripping, thumbnails and several resolutions, content moderation; metadata in a database; serving through a CDN; storage tiering for old originals.
- **Deep dive:** idempotent processing (keyed by photo ID and derivative type), retries and a dead-letter queue for bad images, private photos via signed, expiring CDN URLs (which interacts with cache hit rates).
- **Traps:** streaming image bytes through application servers; synchronous processing in the upload request; public CDN URLs for private photos.

### A5. Real-Time Leaderboard

- **Clarify:** score update rate, leaderboard scopes (global, friends, daily, weekly), exact rank for everyone or only top-K exactly.
- **Numbers:** 100M players × ~100 B ≈ 10 GB, so a single in-memory sorted set (skip list, O(log n) updates and rank queries) holds one leaderboard; the update rate (for example 200k/s) may exceed one node.
- **Core design:** sorted set keyed by leaderboard and time window (`lb:global:2026-W45`), with expiry for old windows; scores persisted durably elsewhere; top-K cached.
- **Deep dive:** sharding: partition by score range so rank = (count of players in higher ranges) + (rank within own range), with per-range counts cached; or shard by player and compute top-K by merging per-shard top-K lists, with approximate ranks for everyone else from a score histogram. Ties: break by earliest achievement time.
- **Traps:** `ORDER BY score` over 100M rows per request; not separating exact top-100 from approximate "you are in the top 12%".

### A6. Ad-Click Aggregation (Exactly Once)

- **Clarify:** aggregation windows (per minute per ad), latency to dashboard, how late events can arrive, fraud filtering, reconciliation requirements.
- **Numbers:** 1B clicks/day ≈ 12k/s average, about 50k/s at peak; aggregated output is small (ads × minutes).
- **Core design:** click events with unique IDs into a durable log; a stream processor keyed by ad ID computes tumbling one-minute windows, deduplicates click IDs, and writes aggregates to an OLAP store; a periodic batch job recomputes from raw logs for reconciliation and billing.
- **Deep dive:** exactly-once in stream processing: consistent state checkpoints that include input offsets, plus transactional or idempotent sinks (upsert keyed by `(ad, window)`), so a replay after failure produces identical results. Event time vs processing time, watermarks, allowed lateness, and how late corrections reach the billing system.
- **Traps:** `UPDATE count = count + 1` per click in a database; counting by processing time; no dedupe of client retries.

### A7. Distributed Cache Service

- **Clarify:** ops/s, value sizes, consistency expectations, multi-region, whether the cache may lose data.
- **Numbers:** for example 10M ops/s; at a few hundred thousand to around a million simple ops/s per node, tens of nodes; memory sized by the hot set.
- **Core design:** consistent hashing (client library or proxy routing), optional replication for hot or important data, LRU-style eviction with memory managed in size classes to limit fragmentation, TTLs.
- **Deep dive:** stampede control (leases or request coalescing so one client refills a missing key), hot keys (local near-caches, key replication), invalidation from the database's change stream so caches are not updated by racing application writes, warming a new cluster, multi-region invalidation.
- **Traps:** modulo hashing; using the cache as a source of truth; set-on-write races that leave stale data forever.

### A8. Unique ID Generator

- **Clarify:** ID size (64-bit?), ordering needs (roughly time-ordered vs strictly monotonic), throughput, whether IDs may reveal creation time or volume.
- **Numbers:** Snowflake-style 64-bit layout: 1 unused sign bit + 41 bits of milliseconds (2^41 ms ≈ 69.7 years from a custom epoch) + 10 bits of worker ID (1,024 workers) + 12 bits of sequence (4,096 IDs per millisecond per worker, about 4M/s per worker).
- **Core design:** stateless generators, each holding a unique worker ID leased from a coordination service; no per-ID coordination.
- **Deep dive:** clock moving backwards (refuse or wait until the clock passes the last timestamp; never reuse a timestamp-sequence pair); sequence exhaustion within a millisecond (wait for the next millisecond); worker ID reuse after a crash (lease expiry). Alternatives: UUIDv4 (random, no coordination, poor index locality), UUIDv7 (128-bit, millisecond timestamp prefix, time-ordered), database ticket servers or range leasing.
- **Traps:** a single auto-increment database as the global source; ignoring clock skew.

### A9. Nearby Places

- **Clarify:** number of places, query rate, radius, how often places change, ranking signal.
- **Numbers:** for example 200M places and 100k queries/s; places change slowly, so the index can be rebuilt or patched offline and replicated to every server.
- **Core design:** a geospatial index: geohash (for a 2 km radius use precision 5, cells about 4.9 km × 4.9 km, and search the cell plus its 8 neighbors; precision 6 cells, about 1.2 km × 0.6 km, would need about two rings of neighbors east-west and four north-south to cover 2 km, so pick the cell size to match the radius), a quadtree (adaptive cells, dense cities split deeper), or S2/H3 cell IDs; candidates filtered by exact distance and ranked by rating and distance; place details from a cache.
- **Deep dive:** why neighbors must be searched (a point near a cell edge), choosing precision from the radius, sharding by region if the index outgrows memory, handling dense areas (cap candidates, adaptive cells).
- **Traps:** computing distance to every place; a SQL bounding-box query without a spatial index.

### A10. Stock Exchange Matching Engine

- **Clarify:** order types, symbols, throughput, latency target (microseconds), fairness rules (price-time priority).
- **Numbers:** for example 1M orders/s across all symbols, but each symbol's book is handled by one thread, and a single in-memory match takes microseconds.
- **Core design:** gateways validate and risk-check orders; a sequencer assigns a global sequence number and journals every inbound message; one single-threaded matching engine per symbol (or symbol group) applies orders deterministically to an in-memory order book (price levels with FIFO queues); executions and market data are published from the sequenced output.
- **Deep dive:** determinism and replication by replay: a hot standby consumes the same sequenced input and reaches the same state, so failover is fast and consistent; recovery replays the journal from a snapshot; latency techniques (no locks or garbage collection on the hot path, pre-allocated memory, kernel-bypass networking).
- **Traps:** a database transaction per order; multi-threaded matching on one order book; nondeterministic inputs such as wall-clock reads inside the matcher.

### A11. Distributed Tracing

- **Clarify:** request rate, spans per request, retention, which questions users ask (slow requests, errors, dependency graph).
- **Numbers:** 1M requests/s × 20 spans × 500 B = 10 GB/s at 100% sampling, so sampling is mandatory.
- **Core design:** a span model (trace ID, span ID, parent, timing, attributes); context propagation through every hop (for example the W3C `traceparent` header); SDKs export to local agents, then collectors; storage keyed by trace ID with secondary indexes on service, operation, duration, and error.
- **Deep dive:** head-based sampling (decide at the root, propagate the decision; cheap but misses rare errors) vs tail-based sampling (buffer every span of a trace in one collector, routed by trace ID, for about 30 s, then keep errors and slow traces; expensive but useful). Linking traces to metrics through exemplars.
- **Traps:** independent sampling decisions per service, producing broken traces; storing everything.

### A12. Remote Build Cache and Distributed Execution

- **Clarify:** repository size, builds per day, cache hit-rate goal, platforms, trust model (who may write to the cache).
- **Numbers:** for example 50k CI builds/day and a large number of actions per build; a high hit rate (often 90%+ for incremental builds) is the main goal; cache size in the tens of TB with LRU eviction.
- **Core design:** content-addressable storage keyed by digest of content; an action cache mapping an action digest (command line, input-tree digest, environment, platform) to output digests; a scheduler dispatching uncached actions to sandboxed executors. The Bazel Remote Execution API is a standard protocol for this.
- **Deep dive:** hermeticity: an action that reads an undeclared input (the system compiler, an environment variable, the time) can poison the cache for everyone, so sandbox actions and include toolchains in the digest; trust: only CI writes to the shared cache, developers read; executor autoscaling for the morning peak.
- **Traps:** keying cache entries by file timestamps; letting developer machines write to the shared cache. See [CMake Fundamentals](../tools/CMake_Fundamentals.md) for local caching tools such as `ccache`.

### A13. Feature Flags and Dynamic Configuration

- **Clarify:** number of flags, evaluation rate, targeting rules, how fast changes must propagate, audit requirements.
- **Numbers:** evaluations happen billions of times per second across the fleet, so they must be **local** (in-process SDK); the server handles only configuration distribution to, for example, 100k SDK instances.
- **Core design:** a flag store with versioned rule sets; SDKs fetch a snapshot at startup and receive updates through streaming (or polling); percentage rollouts use a stable hash of `(flag, user_id)` so a user's assignment does not flip; full audit log.
- **Deep dive:** safety: validation of rule changes, staged rollout of configuration itself, instant kill switches, and last-known-good behavior when the flag service is down (SDKs keep serving their cached snapshot).
- **Traps:** a network call per flag evaluation; random (non-sticky) percentage assignment; a flag service outage taking down every product.

### A14. Online Coding Judge

- **Clarify:** languages, time and memory limits, contest peaks, how results are delivered.
- **Numbers:** steady load is modest, but the last minutes of a contest can bring thousands of submissions per minute, each needing seconds of isolated CPU time.
- **Core design:** submission API, a queue with priorities (contest over practice), worker pool running each submission in a sandbox (containers with seccomp filters and cgroup limits, or microVMs for stronger isolation), no network access, per-language compile and run images, results pushed to clients.
- **Deep dive:** security of running untrusted code (escape risks, resource exhaustion, fork bombs, disk filling); fair timing (CPU time rather than wall time, pinned cores, no noisy neighbors during measurement); burst handling via queueing plus pre-scaled workers before a contest.
- **Traps:** running submissions on the web servers; wall-clock time limits on shared machines.

### A15. Live Comments and Reactions for 10M Viewers

- **Clarify:** comment rate, whether every viewer must see every comment, reaction types, latency target.
- **Numbers:** 10k comments/s delivered to 10M viewers would be 1e11 deliveries/s, which is impossible and also unreadable. Each viewer sees perhaps 10 comments/s (about 2 KB/s), so total egress is about 20 GB/s, delivered through about 50 gateways at 200k connections each.
- **Core design:** comments ingested, moderated, and **sampled or ranked** (friends, top-voted, random sample) per viewer segment; reactions aggregated into per-second counts and broadcast as aggregates; a fan-out tree (origin, regional relays, edge gateways) so each message is published once per gateway, not once per viewer.
- **Deep dive:** the fan-out tree, backpressure for slow clients (drop, do not queue), and how a viewer still sees their own comment immediately (local echo plus server confirmation).
- **Traps:** one broker queue per viewer; trying to deliver every comment to everyone.

### A16. Vector Search for RAG

- **Clarify:** corpus size, embedding dimension, QPS, latency, freshness, metadata filters, recall target.
- **Numbers:** 1B documents × 768 dimensions × 4 bytes ≈ 3 TB of raw vectors; product quantization to about 96 bytes per vector brings the index to about 100 GB, at some cost in recall.
- **Core design:** shard by document; each shard holds an ANN index (HNSW for high recall in memory, or IVF-PQ for compression); queries scatter to all shards and merge the top-k; an exact rerank step (full-precision vectors or a cross-encoder model on GPUs) on the merged candidates; metadata filtering before or after the ANN search.
- **Deep dive:** recall vs latency knobs (HNSW search breadth, number of IVF lists probed), filtering pitfalls (post-filtering can return too few results), incremental inserts vs periodic rebuilds, hybrid search combining keyword (BM25) and vector scores.
- **Traps:** brute-force search over 1B vectors per query; ignoring that recall is a tunable quality metric that must be measured.

### A17. Nightly GPU Performance-Regression CI

- **Clarify:** number of benchmarks, GPU generations, repetitions, acceptable noise, how fast regressions must be reported, who triages.
- **Numbers:** 2,000 benchmarks × 5 SKUs × 10 repetitions × 30 s = 3M GPU-seconds ≈ 830 GPU-hours per night; in a 10-hour window that is about 17 dedicated GPUs per SKU.
- **Core design:** dedicated, quiesced machines (no other tenants, fixed power and clock settings where possible, warmup runs, consistent driver and firmware recorded as metadata); a results store keyed by (benchmark, SKU, commit, compiler, ROCm version, firmware); change detection per benchmark against its own noise model; automatic bisection over the commit range when a regression is confirmed.
- **Deep dive:** statistics: repetitions, medians, confidence intervals, minimum effect size, false-discovery control across thousands of benchmarks, and change-point detection over the time series rather than comparing only to yesterday; handling flaky benchmarks (quarantine with an owner). See [Controlling the Environment](../computer-science/Performance_Engineering.md#82-controlling-the-environment) and [A/B Methodology](../computer-science/Performance_Engineering.md#85-ab-methodology).
- **Traps:** single runs compared against a fixed threshold; running on shared machines; not recording the software stack with each result.

### A18. Crash Reporting and Symbolication

- **Clarify:** crash volume, dump sizes, platforms, how quickly new crash types must alert, PII rules.
- **Numbers:** for example 1M crashes/day with dumps of 100 KB to a few MB; a bad release can produce 100x bursts, so ingestion must sample per (app version, signature) under load.
- **Core design:** clients upload minidumps to an ingestion endpoint (accept quickly, store in object storage, queue for processing); a symbol server stores debug symbols by build ID (uploaded by CI at release); symbolication workers walk stacks and resolve addresses, caching symbol files locally; crashes are grouped into issues by a normalized stack signature; alerts on new issues and spikes.
- **Deep dive:** grouping quality (which frames to include, stripping addresses and inlined frames, avoiding over-grouping), symbol-file caching (symbol files can be gigabytes), scrubbing PII from dumps.
- **Traps:** symbolicating synchronously on upload; grouping by the full raw stack.

### A19. GPU Driver and Firmware Rollout

- **Clarify:** fleet size, update duration, how much capacity may be offline at once, whether firmware can be rolled back, and how jobs are protected.
- **Numbers:** 10k nodes, about 30 minutes per node including drain and reboot, at most 5% of capacity offline at once (500 nodes): 20 waves × 30 minutes ≈ 10 hours of pure update time, plus soak time between stages.
- **Core design:** an inventory of current versions per node; a desired-state declaration per cohort; staged waves (canary 1%, then 10%, 50%, 100%) with **health gates** from telemetry (job failure rate, GPU errors, the performance regressions of Mock 9); nodes drained through the scheduler (wait for jobs to finish or checkpoint) before updating; waves spread across failure domains so no rack or large job loses all nodes at once.
- **Deep dive:** the compatibility matrix (driver, firmware, ROCm user space), rollback when firmware cannot be downgraded (extra canary soak and a stop button), idempotent node agents that converge to desired state, and pausing the rollout automatically when a gate fails.
- **Traps:** updating nodes that are running jobs; a single global wave; no automatic pause.

### A20. Multi-Tenant GPU Notebook Service

- **Clarify:** number of users, GPUs per session, session length, storage persistence, isolation requirements, budget.
- **Numbers:** for example 2,000 users, 500 concurrent sessions at peak × 2 GPUs = 1,000 GPUs allocated, but interactive sessions often keep GPUs busy only a small fraction of the time, so idle reclamation is the main cost lever.
- **Core design:** a session API; a scheduler with per-team quotas and priorities placing sessions on nodes; container images with ROCm and frameworks pre-cached on nodes (a multi-GB image pull otherwise dominates start time); persistent home directories on network storage, scratch on local NVMe; an idle detector that snapshots and releases GPUs after a period of inactivity.
- **Deep dive:** isolation (containers with only the assigned GPU devices exposed, no host root, network policies), sharing small workloads through GPU partitioning modes where the hardware supports them (for example MI300X compute partitioning), fair reclamation without losing user work, and start-time SLOs.
- **Traps:** permanently reserving GPUs per user; ignoring image pull time; no quota enforcement. See [ML Systems Design §6](../ml-gpu/ML_Systems_Design.md#6-case-study-gpu-cluster-job-scheduler) for scheduling and quotas.
