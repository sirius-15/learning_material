# Concurrency Coding Problems -- Comprehensive Interview Problem Set

> Implement-from-scratch concurrency problems that come up in systems, C++, HPC/GPU-tooling, and general SWE loops: the LeetCode concurrency set (1114, 1115, 1116, 1117, 1195, 1226, 1188, 1242) plus the classic "build it yourself" primitives (reader-writer lock, spinlock, futex mutex, barrier, thread pool, thread-safe LRU, rate limiter, crawlers, parallel sort/scan). Every problem has a statement, approach, pitfalls, a complete **C++20** program, a complete **Python** program, and a correctness/complexity argument.
>
> Toolchain assumed: `g++ -std=c++20 -pthread` (GCC 11+ or Clang 14+ with libstdc++), Python 3.11+ (the asyncio examples use `TaskGroup`). Every complete program in this file builds and terminates on its own; blocks whose first line is `// fragment` or `# fragment` are intentionally partial.

See also: [CS Fundamentals: Classic Concurrency Problems](CS_Fundamentals.md#65-classic-concurrency-problems) (theory) · [C++ Fundamentals: Part 5 Concurrency](../languages/Cpp_Fundamentals.md#123-condition-variables) · [Python Fundamentals: GIL & Threading](../languages/Python_Fundamentals.md#19-the-gil--threading) · [Python asyncio](../languages/Python_Fundamentals.md#21-asyncio--asyncawait) · [Low Level Design: Designing for Concurrency](../design-patterns/Low_Level_Design_Interview_Prep.md#4-designing-for-concurrency-and-failure) · [Debugging and Profiling Tools](../tools/Debugging_and_Profiling_Tools.md)

---

## Table of Contents

1. [Toolbox: Primitives, Templates, and Testing](#1-toolbox-primitives-templates-and-testing)
2. [Print in Order (LeetCode 1114)](#2-print-in-order-leetcode-1114)
3. [Print FooBar Alternately (LeetCode 1115)](#3-print-foobar-alternately-leetcode-1115)
4. [Print Zero Even Odd (LeetCode 1116)](#4-print-zero-even-odd-leetcode-1116)
5. [Building H2O (LeetCode 1117)](#5-building-h2o-leetcode-1117)
6. [Fizz Buzz Multithreaded (LeetCode 1195)](#6-fizz-buzz-multithreaded-leetcode-1195)
7. [The Dining Philosophers (LeetCode 1226)](#7-the-dining-philosophers-leetcode-1226)
8. [Bounded Blocking Queue (LeetCode 1188)](#8-bounded-blocking-queue-leetcode-1188)
9. [Reader-Writer Lock](#9-reader-writer-lock)
10. [Spinlocks and a Futex-Based Mutex](#10-spinlocks-and-a-futex-based-mutex)
11. [Thread-Safe LRU Cache](#11-thread-safe-lru-cache)
12. [Thread-Safe Token-Bucket Rate Limiter](#12-thread-safe-token-bucket-rate-limiter)
13. [Thread Pool with Futures](#13-thread-pool-with-futures)
14. [Reusable Barrier](#14-reusable-barrier)
15. [Web Crawler Multithreaded (LeetCode 1242)](#15-web-crawler-multithreaded-leetcode-1242)
16. [Async Web Crawler with Bounded Concurrency](#16-async-web-crawler-with-bounded-concurrency)
17. [Parallel Merge Sort and Parallel Prefix Sum](#17-parallel-merge-sort-and-parallel-prefix-sum)
18. [Pitfalls Checklist](#18-pitfalls-checklist)
19. [Interview Q&A](#19-interview-qa)

---

## How to Use This File

| Round type | Problems to drill first | What the interviewer is really testing |
|---|---|---|
| LeetCode-style concurrency (online judge) | 2-7 | Choosing the smallest correct primitive; ordering guarantees; no busy-waiting |
| Systems / C++ "build a primitive" | 8, 9, 10, 13, 14 | Condition-variable discipline, memory ordering, shutdown, exception safety |
| Machine-coding / LLD with concurrency | 11, 12, 13, 15 | Lock granularity, contention, API design, testability (injectable clock) |
| HPC / GPU / performance | 10, 14, 17 | Cache-coherence cost, barriers, work/span, scaling limits |
| Python / backend | 12, 15, 16 | GIL implications, asyncio vs threads, bounded concurrency, cancellation |

**Recommended workflow:** read the statement, write the solution in your interview language without looking, then compare. For each problem, be able to answer: *What is the invariant? Who waits on what predicate? Who signals? How does it shut down? What happens on a spurious wakeup?*

---

## 1. Toolbox: Primitives, Templates, and Testing

### 1.1 Primitive Map: C++20 vs Python

| Need | C++20 | Python `threading` | Python `asyncio` |
|---|---|---|---|
| Mutual exclusion | `std::mutex` + `std::lock_guard` / `std::unique_lock` / `std::scoped_lock` | `threading.Lock` (`with lock:`) | `asyncio.Lock` |
| Re-entrant lock | `std::recursive_mutex` | `threading.RLock` | (none) |
| Shared/exclusive lock | `std::shared_mutex` + `std::shared_lock` | (none -- build it, Section 9) | (none) |
| Wait for a predicate | `std::condition_variable` (+ `_any` for any lockable / `stop_token`) | `threading.Condition` (`wait_for(pred)`) | `asyncio.Condition` |
| Counting permits | `std::counting_semaphore<N>`, `std::binary_semaphore` | `threading.Semaphore`, `BoundedSemaphore` | `asyncio.Semaphore`, `BoundedSemaphore` |
| One-shot signal | `std::latch{1}`, `std::promise<void>`, `std::atomic<bool>::wait` | `threading.Event` | `asyncio.Event` |
| Count-down to zero | `std::latch` | (none -- `Barrier` or `Event` + counter) | (none) |
| Reusable rendezvous | `std::barrier` (with completion function) | `threading.Barrier` (with `action`) | `asyncio.Barrier` (3.11+) |
| Result handoff | `std::promise` / `std::future` / `std::packaged_task` | `concurrent.futures.Future` | `asyncio.Future` |
| Lock-free word | `std::atomic<T>` (+ `wait`/`notify_one` in C++20) | none exposed (GIL is not a substitute) | n/a (single-threaded loop) |
| Thread handle | `std::thread` (must join/detach), `std::jthread` (joins, has `stop_token`) | `threading.Thread` (`daemon=True` to not block exit) | `asyncio.Task` |

### 1.2 Which Primitive for Which Shape of Problem

| Problem shape | Best fit | Why |
|---|---|---|
| "B must run after A" (a fixed handoff between specific threads) | Semaphore / Event / latch | A semaphore *remembers* a release that happens before the acquire, so there is no lost-wakeup window |
| "Wait until some condition over shared state holds" | Mutex + condition variable with a predicate | Arbitrary predicates; one mutex protects all state the predicate reads |
| "At most K at a time" | Counting semaphore | The count *is* the invariant |
| "N threads meet, then all continue; repeat" | Barrier | Generation/phase handling is built in |
| A single counter or flag with no compound invariant | `std::atomic` | No lock needed; but two atomics are not one atomic invariant |
| Producer/consumer pipeline | Bounded blocking queue | Back-pressure for free |

### 1.3 The Condition-Variable Template (Memorize This)

```cpp
// fragment -- the only correct shape for waiting on a condition variable
std::unique_lock<std::mutex> lk(m);           // 1. lock the mutex that guards the predicate state
cv.wait(lk, [&] { return predicate(); });     // 2. loops: while (!pred) cv.wait(lk); handles spurious wakeups
mutate_shared_state();                        // 3. still holding the lock
lk.unlock();                                  // 4. optional: unlock before notifying (fewer wasted wakeups)
cv.notify_one();                              // 5. or notify_all() if waiters have DIFFERENT predicates
```

```python
# fragment -- same shape in Python
with cond:                                    # cond = threading.Condition(lock)
    cond.wait_for(lambda: predicate())        # re-checks the predicate after every wakeup
    mutate_shared_state()
    cond.notify_all()                         # Python requires holding the lock to notify
```

Three rules that prevent almost every condition-variable bug:

1. **Always wait with a predicate (or in a `while` loop).** Wakeups can be spurious, and by the time a woken thread reacquires the mutex another thread may have consumed the state change ("stolen wakeup").
2. **Modify the predicate state while holding the same mutex the waiter uses -- even if that state is an `std::atomic`.** Otherwise the waiter can check the predicate (false), get preempted, the signaller sets it and notifies (nobody is waiting yet), and the waiter then blocks forever: a *lost wakeup*.
3. **Use `notify_all` when waiters wait for different predicates on the same condition variable** (or use one condition variable per predicate). `notify_one` may wake a thread whose predicate is still false; it goes back to sleep and the thread that could have progressed is never woken.

### 1.4 How to Test Concurrent Code

```bash
# Normal build
g++ -std=c++20 -O2 -Wall -Wextra -pthread solution.cpp -o solution
# ThreadSanitizer: detects data races and lock-order inversions (potential deadlocks)
g++ -std=c++20 -O1 -g -pthread -fsanitize=thread solution.cpp -o solution_tsan
# Stress: many runs, each with a timeout so a deadlock is reported instead of hanging CI
for i in $(seq 200); do timeout 10 ./solution_tsan > /dev/null || { echo "failed or hung on run $i"; break; }; done
# A hung process: dump every thread's stack
gdb -p "$(pgrep -n solution)" -batch -ex "thread apply all bt"
# Python: dump all thread stacks of a running interpreter (pip install py-spy)
py-spy dump --pid "$(pgrep -n -f solution.py)"
```

Techniques that make tests meaningful:

- **Randomize start order** (shuffle which thread starts first) and repeat thousands of times; most ordering bugs need a specific interleaving.
- **Check invariants, not output timing**: count totals, verify every item is consumed exactly once, verify mutual exclusion with an "occupancy" atomic that must never exceed 1.
- **Inject the clock** for anything time-based (rate limiters, timeouts) so tests are deterministic.
- **Use a latch/barrier to line up threads** so they really start contending at the same time.
- In Python, `faulthandler.dump_traceback_later(timeout, exit=True)` turns a hang into a stack dump.

### 1.5 Interview Questions

**Q1. Mutex vs binary semaphore -- aren't they the same thing?**

No. A mutex has **ownership**: the thread that locks it must unlock it (unlocking a `std::mutex` from another thread is undefined behavior), which enables priority inheritance, recursive variants, and deadlock detection by owner. A semaphore is a **counter with no owner**: any thread may `release`, which is exactly what makes it a *signaling* primitive ("A tells B it may proceed", as in Print in Order). Use a mutex to protect data; use a semaphore to count resources or to signal between threads.

**Q2. Why is `cv.wait(lk, pred)` preferred over `if (!pred) cv.wait(lk);`?**

Because a wakeup does not mean the predicate is true: (1) POSIX and C++ allow spurious wakeups; (2) with `notify_all` several waiters wake, but only the first to reacquire the mutex may find the predicate true -- the others must go back to sleep; (3) a thread that was not waiting at all can grab the mutex between the notify and the waiter's reacquisition and consume the state. The predicate overload is exactly `while (!pred()) wait(lk);`.

**Q3. Does Python's GIL make my shared counter thread-safe?**

No. `counter += 1` compiles to separate load, add, and store bytecodes; the interpreter can switch threads between them (the switch interval is 5 ms by default, `sys.getswitchinterval()`), so increments are lost. The GIL only guarantees that individual bytecodes (and many single built-in operations like `list.append` or `dict[key] = value`) do not corrupt interpreter state. Compound read-modify-write needs a `Lock`. On free-threaded builds (`python3.13t`, officially supported from 3.14) there is no GIL at all, so the same code is even more exposed.

---

## 2. Print in Order (LeetCode 1114)

### 2.1 Problem

One `Foo` instance is shared by three threads: thread A calls `first()`, B calls `second()`, C calls `third()`. The threads start in an arbitrary order. Guarantee that the output is always `firstsecondthird`.

### 2.2 Approach

This is a pure **happens-before** problem: `second` must wait for a signal from `first`, and `third` for a signal from `second`. Two one-shot signals are needed. A semaphore initialized to 0 is ideal: if `first` releases before `second` even starts, the permit is *remembered*, so there is no lost-wakeup window.

Options, from simplest to most general:

| Mechanism | C++ | Python |
|---|---|---|
| Two semaphores initialized to 0 | `std::binary_semaphore{0}` x 2 | `threading.Semaphore(0)` x 2 |
| Two one-shot events | `std::promise<void>` / `std::latch{1}` | `threading.Event` x 2 |
| One stage counter + condition variable | `std::mutex` + `std::condition_variable` + `int stage` | `threading.Condition` |
| One atomic stage counter + C++20 wait/notify | `std::atomic<int>::wait` | n/a |

### 2.3 C++20 Solution

```cpp
// print_in_order.cpp -- g++ -std=c++20 -O2 -pthread print_in_order.cpp
#include <algorithm>
#include <cstdio>
#include <functional>
#include <random>
#include <semaphore>
#include <string>
#include <thread>
#include <vector>

class Foo {
    std::binary_semaphore firstDone_{0};   // 0 = "not yet signalled"
    std::binary_semaphore secondDone_{0};

public:
    void first(const std::function<void()>& printFirst) {
        printFirst();
        firstDone_.release();              // publishes everything first() did
    }
    void second(const std::function<void()>& printSecond) {
        firstDone_.acquire();              // blocks until first() released
        printSecond();
        secondDone_.release();
    }
    void third(const std::function<void()>& printThird) {
        secondDone_.acquire();
        printThird();
    }
};

int main() {
    std::mt19937 rng(12345);
    std::vector<int> order{0, 1, 2};
    std::string out;
    constexpr int kTrials = 2000;
    for (int trial = 0; trial < kTrials; ++trial) {
        std::shuffle(order.begin(), order.end(), rng);
        Foo foo;
        out.clear();
        // No mutex around `out`: release() -> acquire() is a synchronizes-with edge, so the
        // three appends are ordered by happens-before and there is no data race.
        std::vector<std::thread> threads;
        for (int which : order) {
            if (which == 0) threads.emplace_back([&] { foo.first([&] { out += "first"; }); });
            if (which == 1) threads.emplace_back([&] { foo.second([&] { out += "second"; }); });
            if (which == 2) threads.emplace_back([&] { foo.third([&] { out += "third"; }); });
        }
        for (auto& t : threads) t.join();
        if (out != "firstsecondthird") {
            std::printf("FAIL: %s\n", out.c_str());
            return 1;
        }
    }
    std::printf("%s\n%d random start orders OK\n", out.c_str(), kTrials);
}
```

The C++20 `std::atomic` wait/notify variant is worth knowing because it shows a subtle API detail -- `wait(old)` blocks only *while the value equals `old`*, so a waiter for stage 2 must loop:

```cpp
// fragment -- atomic stage counter with C++20 wait/notify
std::atomic<int> stage{0};
void first(auto print)  { print(); stage.store(1, std::memory_order_release); stage.notify_all(); }
void second(auto print) { stage.wait(0, std::memory_order_acquire);           // returns once stage != 0
                          print(); stage.store(2, std::memory_order_release); stage.notify_all(); }
void third(auto print)  { int s;
                          while ((s = stage.load(std::memory_order_acquire)) < 2) stage.wait(s);
                          print(); }
```

### 2.4 Python Solution

```python
# print_in_order.py
import random
import threading


class Foo:
    def __init__(self) -> None:
        self.first_done = threading.Event()
        self.second_done = threading.Event()

    def first(self, printFirst) -> None:
        printFirst()
        self.first_done.set()

    def second(self, printSecond) -> None:
        self.first_done.wait()
        printSecond()
        self.second_done.set()

    def third(self, printThird) -> None:
        self.second_done.wait()
        printThird()


def run_trial(order: list[int]) -> str:
    foo, out = Foo(), []
    calls = [
        lambda: foo.first(lambda: out.append("first")),
        lambda: foo.second(lambda: out.append("second")),
        lambda: foo.third(lambda: out.append("third")),
    ]
    threads = [threading.Thread(target=calls[i]) for i in order]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return "".join(out)


if __name__ == "__main__":
    rng = random.Random(7)
    for _ in range(500):
        order = [0, 1, 2]
        rng.shuffle(order)
        assert run_trial(order) == "firstsecondthird", order
    print("firstsecondthird")
    print("500 random start orders OK")
```

### 2.5 Correctness and Complexity

- **Safety:** `second` cannot print until `firstDone` has a permit, which only `first` creates *after* printing; same for `third`. Hence the order is forced regardless of start order.
- **Liveness:** each semaphore gets exactly one release and one acquire, so nobody blocks forever.
- **Memory visibility:** in C++, `release()` strongly happens-before an `acquire()` that observes it, so the shared `out` string needs no extra lock. In Python, `Event.set()`/`wait()` go through an internal lock, which gives the same guarantee.
- **Cost:** O(1) work per call; at most two blocking waits (no spinning).

### 2.6 Pitfalls

- **Busy-waiting on a plain `bool`** (`while (!done) {}`) is a data race (undefined behavior); the compiler may hoist the load and spin forever. `volatile` does not fix it in C++ -- it provides no inter-thread ordering.
- **Condition variable without a predicate:** if `first` notifies before `second` starts waiting, the notification is lost and `second` sleeps forever. Semaphores and events do not have this problem because they hold state.
- **Spinning with `std::this_thread::yield()`** "works" on LeetCode but burns a core and gets flagged in interviews.

### 2.7 Interview Questions

**Q1. Which ordering guarantee lets `third()` see the effects of `first()`, even though they never synchronize directly?**

Happens-before is transitive. `first`'s writes happen-before `firstDone.release()`, which synchronizes-with `second`'s `acquire()`; `second`'s release synchronizes-with `third`'s acquire. Chaining these edges gives `first` happens-before `third`.

**Q2. How would you generalize this to N stages?**

Keep one `std::atomic<int> stage` (or `mutex` + `int` + `condition_variable`). Stage `k` waits for `stage == k`, does its work, sets `stage = k + 1`, and calls `notify_all` (waiters have different predicates). Alternatively, use an array of N-1 binary semaphores, where stage `k` acquires `sem[k-1]` and releases `sem[k]` -- each wakeup then targets exactly one thread.

---

## 3. Print FooBar Alternately (LeetCode 1115)

### 3.1 Problem

Two threads share one `FooBar(n)` object: thread A calls `foo()` which prints `"foo"` n times, thread B calls `bar()` which prints `"bar"` n times. Make the output `foobar` repeated n times.

### 3.2 Approach

Strict alternation is a **turn** variable: `fooTurn = true` initially; `foo` waits for `fooTurn`, prints, flips it, and signals; `bar` waits for `!fooTurn`. Two semaphores do the same thing (a "ping-pong" pair): `fooSem = 1`, `barSem = 0`; `foo` acquires `fooSem` and releases `barSem`, and vice versa.

### 3.3 C++20 Solution (mutex + condition variable)

```cpp
// foobar.cpp -- g++ -std=c++20 -O2 -pthread foobar.cpp
#include <condition_variable>
#include <cstdio>
#include <functional>
#include <mutex>
#include <string>
#include <thread>

class FooBar {
    int n_;
    std::mutex m_;
    std::condition_variable cv_;
    bool fooTurn_ = true;   // guarded by m_

public:
    explicit FooBar(int n) : n_(n) {}

    void foo(const std::function<void()>& printFoo) {
        for (int i = 0; i < n_; ++i) {
            std::unique_lock lk(m_);
            cv_.wait(lk, [this] { return fooTurn_; });
            printFoo();
            fooTurn_ = false;
            lk.unlock();
            cv_.notify_one();   // exactly one other thread exists, so notify_one is enough
        }
    }

    void bar(const std::function<void()>& printBar) {
        for (int i = 0; i < n_; ++i) {
            std::unique_lock lk(m_);
            cv_.wait(lk, [this] { return !fooTurn_; });
            printBar();
            fooTurn_ = true;
            lk.unlock();
            cv_.notify_one();
        }
    }
};

std::string run(int n) {
    FooBar fb(n);
    std::string out;   // appends are serialized by the turn protocol (both happen under m_)
    std::thread b([&] { fb.bar([&] { out += "bar"; }); });   // start bar first on purpose
    std::thread a([&] { fb.foo([&] { out += "foo"; }); });
    a.join();
    b.join();
    return out;
}

int main() {
    std::printf("%s\n", run(3).c_str());   // foobarfoobarfoobar
    std::string expected;
    for (int i = 0; i < 20000; ++i) expected += "foobar";
    std::printf("n=20000 %s\n", run(20000) == expected ? "OK" : "FAIL");
}
```

### 3.4 Python Solution (semaphores, plus an asyncio version)

```python
# foobar.py
import asyncio
import threading


class FooBar:
    def __init__(self, n: int) -> None:
        self.n = n
        self.foo_sem = threading.Semaphore(1)   # foo goes first
        self.bar_sem = threading.Semaphore(0)

    def foo(self, printFoo) -> None:
        for _ in range(self.n):
            self.foo_sem.acquire()
            printFoo()
            self.bar_sem.release()

    def bar(self, printBar) -> None:
        for _ in range(self.n):
            self.bar_sem.acquire()
            printBar()
            self.foo_sem.release()


def run_threads(n: int) -> str:
    fb, out = FooBar(n), []
    tb = threading.Thread(target=fb.bar, args=(lambda: out.append("bar"),))
    ta = threading.Thread(target=fb.foo, args=(lambda: out.append("foo"),))
    tb.start(); ta.start()
    ta.join(); tb.join()
    return "".join(out)


async def run_async(n: int) -> str:
    """Same protocol with asyncio primitives: coroutines instead of threads."""
    foo_sem, bar_sem, out = asyncio.Semaphore(1), asyncio.Semaphore(0), []

    async def foo() -> None:
        for _ in range(n):
            await foo_sem.acquire()
            out.append("foo")
            bar_sem.release()

    async def bar() -> None:
        for _ in range(n):
            await bar_sem.acquire()
            out.append("bar")
            foo_sem.release()

    async with asyncio.TaskGroup() as tg:
        tg.create_task(bar())
        tg.create_task(foo())
    return "".join(out)


if __name__ == "__main__":
    print(run_threads(3))
    assert run_threads(5000) == "foobar" * 5000
    assert asyncio.run(run_async(5000)) == "foobar" * 5000
    print("threads and asyncio OK")
```

### 3.5 Correctness and Complexity

- **Invariant (semaphore version):** `foo_sem + bar_sem <= 1` at all times, and exactly one of them holds the permit between operations. So at most one thread is in its print section, and they alternate.
- **Liveness:** each thread performs exactly n acquires and n releases of the *other* semaphore, so both loops complete.
- **Cost:** 2n context switches minimum -- strict alternation is inherently serial; it measures handoff latency (~2-10 us per futex wakeup on Linux), not throughput.

### 3.6 Pitfalls

- Using `notify_one` with **more than two** threads on one condition variable (e.g. FooBar with two foo-threads) can wake the wrong one; then use `notify_all` or separate condition variables.
- Forgetting the initial permit (`fooSem{1}`) deadlocks immediately; giving both semaphores 1 permits `barfoo...` orderings.
- In Python, do not use `threading.Lock` as a semaphore by releasing it from another thread "because it works": `Lock` technically allows it, but `RLock` does not, and readers will assume ownership semantics. Say "semaphore" when you mean signalling.

### 3.7 Interview Questions

**Q1. Which version is faster, the condition-variable one or the semaphore one?**

Usually the semaphore pair: each handoff is one `release` (one atomic increment and, if the peer is asleep, one futex wake) and the woken thread does not have to reacquire a mutex. The condition-variable version needs mutex lock/unlock on both sides, plus the wake. Both are dominated by the context switch, so the difference is small; for the absolute minimum handoff latency between two pinned threads, spin on an atomic (at the cost of two busy cores).

**Q2. How would you make three threads print `ABCABC...`?**

Generalize the turn to `int turn` modulo 3 with `notify_all` (different predicates on one condition variable), or use a ring of three semaphores `s[0]=1, s[1]=0, s[2]=0` where thread k acquires `s[k]` and releases `s[(k+1)%3]`. The semaphore ring wakes exactly the next thread, avoiding thundering-herd wakeups.

---

## 4. Print Zero Even Odd (LeetCode 1116)

### 4.1 Problem

`ZeroEvenOdd(n)` is shared by three threads: A calls `zero(printNumber)`, B calls `even(printNumber)`, C calls `odd(printNumber)`. Output must be `0 1 0 2 0 3 ... 0 n` concatenated, e.g. `n = 5` gives `0102030405`.

### 4.2 Approach

The sequence is: `zero` always goes, then hands the turn to `odd` or `even` depending on the next number, who hands it back to `zero`. With semaphores: `zeroSem = 1`, `oddSem = 0`, `evenSem = 0`. `zero` loops `i = 1..n`: acquire `zeroSem`, print 0, release `oddSem` if `i` is odd else `evenSem`. `odd` loops over `1, 3, 5, ...`: acquire `oddSem`, print, release `zeroSem`. `even` likewise over `2, 4, ...`.

Each thread knows exactly how many iterations it performs, so there is no termination problem. (If you write `while (true)` loops instead, you need a shutdown flag and a final release to wake the other threads.)

### 4.3 C++20 Solution (semaphores)

```cpp
// zero_even_odd.cpp -- g++ -std=c++20 -O2 -pthread zero_even_odd.cpp
#include <cstdio>
#include <functional>
#include <semaphore>
#include <string>
#include <thread>

class ZeroEvenOdd {
    int n_;
    std::binary_semaphore zero_{1}, odd_{0}, even_{0};

public:
    explicit ZeroEvenOdd(int n) : n_(n) {}

    void zero(const std::function<void(int)>& printNumber) {
        for (int i = 1; i <= n_; ++i) {
            zero_.acquire();
            printNumber(0);
            (i % 2 == 1 ? odd_ : even_).release();   // hand the turn to whoever prints i
        }
    }
    void even(const std::function<void(int)>& printNumber) {
        for (int i = 2; i <= n_; i += 2) {
            even_.acquire();
            printNumber(i);
            zero_.release();
        }
    }
    void odd(const std::function<void(int)>& printNumber) {
        for (int i = 1; i <= n_; i += 2) {
            odd_.acquire();
            printNumber(i);
            zero_.release();
        }
    }
};

std::string run(int n) {
    ZeroEvenOdd z(n);
    std::string out;   // exactly one thread holds the "turn" at a time -> no race
    auto print = [&](int x) { out += std::to_string(x); };
    std::thread te([&] { z.even(print); });
    std::thread to([&] { z.odd(print); });
    std::thread tz([&] { z.zero(print); });
    tz.join(); te.join(); to.join();
    return out;
}

int main() {
    std::printf("n=5 -> %s\n", run(5).c_str());   // 0102030405
    std::printf("n=1 -> %s\n", run(1).c_str());   // 01
    std::string expected;
    for (int i = 1; i <= 5000; ++i) expected += "0" + std::to_string(i);
    std::printf("n=5000 %s\n", run(5000) == expected ? "OK" : "FAIL");
}
```

### 4.4 Python Solution (one Condition with a turn variable)

The Python version deliberately uses the *other* technique -- one condition variable plus explicit state -- to show why `notify_all` is required when waiters have different predicates.

```python
# zero_even_odd.py
import threading

ZERO, ODD, EVEN = 0, 1, 2


class ZeroEvenOdd:
    def __init__(self, n: int) -> None:
        self.n = n
        self.cv = threading.Condition()
        self.turn = ZERO   # guarded by self.cv

    def _step(self, my_turn: int, value: int, next_turn: int, printNumber) -> None:
        with self.cv:
            self.cv.wait_for(lambda: self.turn == my_turn)
            printNumber(value)
            self.turn = next_turn
            self.cv.notify_all()   # notify_one could wake the wrong waiter -> hang

    def zero(self, printNumber) -> None:
        for i in range(1, self.n + 1):
            self._step(ZERO, 0, ODD if i % 2 else EVEN, printNumber)

    def even(self, printNumber) -> None:
        for i in range(2, self.n + 1, 2):
            self._step(EVEN, i, ZERO, printNumber)

    def odd(self, printNumber) -> None:
        for i in range(1, self.n + 1, 2):
            self._step(ODD, i, ZERO, printNumber)


def run(n: int) -> str:
    z, out = ZeroEvenOdd(n), []
    p = lambda x: out.append(str(x))
    ts = [threading.Thread(target=f, args=(p,)) for f in (z.even, z.odd, z.zero)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    return "".join(out)


if __name__ == "__main__":
    print("n=5 ->", run(5))
    assert run(5) == "0102030405" and run(1) == "01"
    assert run(2000) == "".join(f"0{i}" for i in range(1, 2001))
    print("OK")
```

### 4.5 Correctness and Complexity

- **Invariant:** exactly one of the three semaphores holds a permit (or `turn` names exactly one thread), so exactly one thread may print next, and the hand-off encodes the required successor.
- **Liveness:** `zero` performs n hand-offs: ceil(n/2) to odd and floor(n/2) to even, matching exactly the iteration counts of the `odd` and `even` loops.
- **Cost:** 2n hand-offs. The `notify_all` version wakes 2 threads per step (one goes back to sleep), roughly doubling wakeups versus targeted semaphores.

### 4.6 Pitfalls

- Using `notify_one` with a shared condition variable: `zero` might wake `even` when `odd` is next; `even` re-sleeps and nobody wakes `odd` -- a hang that only appears under some schedules.
- Off-by-one on `n` odd vs even: test `n = 1` and `n = 2`.
- Printing outside the protected region in the condition-variable version: two threads could interleave prints.

### 4.7 Interview Questions

**Q1. When is a semaphore ring better than a single condition variable, and when is it worse?**

Better when the successor is known at hand-off time: each release wakes exactly one specific thread (no thundering herd, no wasted wakeups). Worse when the next runner depends on a complex predicate over shared state, or when the set of threads is dynamic; then a mutex + condition variable (or one condition variable per predicate) is easier to get right.

**Q2. What happens if `printNumber` throws in the semaphore version?**

The thread exits without releasing the next semaphore, so the others block forever. In production code, release in a scope guard (RAII), or propagate the failure by setting a "broken" flag and releasing all semaphores so waiters can observe it -- the same design as `threading.Barrier`'s broken state.

---

## 5. Building H2O (LeetCode 1117)

### 5.1 Problem

Hydrogen and oxygen threads arrive in any order. Each must call `releaseHydrogen()`/`releaseOxygen()` only as part of a complete molecule: threads must pass the barrier in groups of exactly **two H and one O**, and all three threads of one molecule must release before any thread of the next molecule does. Equivalently, every consecutive group of three outputs contains exactly 2 `H` and 1 `O`.

### 5.2 Approach

Two separate constraints:

1. **Composition:** at most 2 H and 1 O may be "in the current molecule" -- counting semaphores `hSlots = 2` and `oSlot = 1`.
2. **Grouping:** the three admitted threads must wait for each other before releasing -- a barrier of size 3.

A thread returns its slot only *after* it has released, so the next molecule cannot form until all three members of the current one are done. That is what keeps molecules from interleaving.

### 5.3 C++20 Solution (`counting_semaphore` + `barrier`)

```cpp
// h2o.cpp -- g++ -std=c++20 -O2 -pthread h2o.cpp
#include <algorithm>
#include <barrier>
#include <cstdio>
#include <functional>
#include <mutex>
#include <random>
#include <semaphore>
#include <string>
#include <thread>
#include <vector>

class H2O {
    std::counting_semaphore<2> hSlots_{2};
    std::binary_semaphore oSlot_{1};
    std::barrier<> bond_{3};

public:
    void hydrogen(const std::function<void()>& releaseHydrogen) {
        hSlots_.acquire();            // at most two H in the current molecule
        bond_.arrive_and_wait();      // wait until 2H + 1O are present
        releaseHydrogen();
        hSlots_.release();            // only now may the next molecule's H enter
    }
    void oxygen(const std::function<void()>& releaseOxygen) {
        oSlot_.acquire();
        bond_.arrive_and_wait();
        releaseOxygen();
        oSlot_.release();
    }
};

int main() {
    std::mt19937 rng(2024);
    for (int trial = 0; trial < 200; ++trial) {
        const int molecules = 10;
        std::string water;
        for (int i = 0; i < molecules; ++i) water += "HHO";
        std::shuffle(water.begin(), water.end(), rng);

        H2O h2o;
        std::mutex outM;
        std::string out;
        auto emit = [&](char c) { std::lock_guard g(outM); out += c; };
        std::vector<std::thread> threads;
        for (char c : water) {
            if (c == 'H') threads.emplace_back([&] { h2o.hydrogen([&] { emit('H'); }); });
            else          threads.emplace_back([&] { h2o.oxygen([&] { emit('O'); }); });
        }
        for (auto& t : threads) t.join();

        for (std::size_t i = 0; i < out.size(); i += 3) {
            if (std::count(out.begin() + i, out.begin() + i + 3, 'O') != 1) {
                std::printf("FAIL trial %d: %s\n", trial, out.c_str());
                return 1;
            }
        }
        if (trial == 0) std::printf("input  %s\noutput %s\n", water.c_str(), out.c_str());
    }
    std::printf("200 trials OK\n");
}
```

### 5.4 Python Solution (`Semaphore` + `Barrier`)

```python
# h2o.py
import random
import threading


class H2O:
    def __init__(self) -> None:
        self.h_slots = threading.Semaphore(2)
        self.o_slot = threading.Semaphore(1)
        self.bond = threading.Barrier(3)

    def hydrogen(self, releaseHydrogen) -> None:
        with self.h_slots:          # acquire ... release after releaseHydrogen()
            self.bond.wait()
            releaseHydrogen()

    def oxygen(self, releaseOxygen) -> None:
        with self.o_slot:
            self.bond.wait()
            releaseOxygen()


def run(water: str) -> str:
    h2o, out, out_lock = H2O(), [], threading.Lock()

    def emit(c: str) -> None:
        with out_lock:
            out.append(c)

    threads = [
        threading.Thread(target=h2o.hydrogen, args=(lambda: emit("H"),)) if c == "H"
        else threading.Thread(target=h2o.oxygen, args=(lambda: emit("O"),))
        for c in water
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return "".join(out)


if __name__ == "__main__":
    rng = random.Random(1)
    for trial in range(100):
        atoms = list("HHO" * 8)
        rng.shuffle(atoms)
        out = run("".join(atoms))
        assert all(out[i:i + 3].count("O") == 1 for i in range(0, len(out), 3)), out
        if trial == 0:
            print(f"input  {''.join(atoms)}\noutput {out}")
    print("100 trials OK")
```

### 5.5 Correctness and Complexity

- **Composition:** at any instant at most 2 H threads and 1 O thread hold slots. The barrier needs 3 arrivals, and only slot holders can arrive, so each barrier phase contains exactly 2 H + 1 O.
- **No interleaving between molecules:** molecule k+1 needs both H slots and the O slot, which are returned only after the corresponding member of molecule k has called its release function. So all three releases of molecule k precede any release of molecule k+1.
- **Liveness:** with exactly 2m H and m O threads, every phase completes; the input guarantee is what prevents a stranded thread at the end.
- **Cost:** O(1) per thread plus one barrier phase per molecule.

### 5.6 Pitfalls

- **Returning the slot before releasing** (i.e. `acquire; barrier; release slot; releaseHydrogen()`) lets molecule k+1 overtake molecule k: outputs like `HHHOO...` appear rarely and only under load.
- **Counting without a barrier** (e.g. "oxygen waits until hCount >= 2") composes molecules correctly but does not stop the next molecule from releasing first.
- Python's `threading.Barrier` raises `BrokenBarrierError` in every waiter if one waiter times out or `abort()` is called -- handle it if you add timeouts.

### 5.7 Interview Questions

**Q1. How would you solve it without a barrier primitive?**

Use a mutex + condition variable with counters `hWaiting`, `oWaiting`, and a "molecule in progress" phase: the thread that completes a group (sees 2 H and 1 O) moves 2 H and 1 O into a `released` budget and `notify_all`s; each waiter waits for budget of its type. You still need the "next molecule waits until this one finished releasing" rule, so track `releasedInPhase` and reset it when it reaches 3. The semaphore + barrier version is shorter because the barrier already implements the generation logic (Section 14).

**Q2. What changes if the input may contain leftover atoms (e.g. 5 H and 2 O)?**

The leftover H thread blocks forever in `acquire`/the barrier. Real systems need a shutdown path: a timeout on the barrier (`threading.Barrier.wait(timeout)`), or a "closing" flag plus `abort()`/`arrive_and_drop()` so stragglers are released with an error rather than hanging.

---

## 6. Fizz Buzz Multithreaded (LeetCode 1195)

### 6.1 Problem

Four threads share `FizzBuzz(n)`: `fizz()` prints `fizz` for numbers divisible by 3 but not 5, `buzz()` prints `buzz` for divisible by 5 but not 3, `fizzbuzz()` prints `fizzbuzz` for divisible by 15, and `number()` prints every other number. The combined output must be the normal FizzBuzz sequence from 1 to n.

### 6.2 Approach

Shared state is a single counter `cur` (next number to print). Each thread waits until either `cur > n` (time to exit) or `cur` belongs to its category; then it prints, increments `cur`, and wakes everybody (`notify_all`, because the four threads wait on different predicates). The termination condition is part of the predicate, so the final increment wakes every thread to exit.

An alternative with targeted wakeups: the `number` thread acts as a dispatcher iterating 1..n and releases the semaphore of the thread that owns `i`, then waits for that thread to signal back -- n hand-offs and no wasted wakeups, but more code.

### 6.3 C++20 Solution

```cpp
// fizzbuzz.cpp -- g++ -std=c++20 -O2 -pthread fizzbuzz.cpp
#include <condition_variable>
#include <cstdio>
#include <functional>
#include <mutex>
#include <string>
#include <thread>

class FizzBuzz {
    int n_;
    int cur_ = 1;   // next number to emit; guarded by m_
    std::mutex m_;
    std::condition_variable cv_;

    template <class Mine, class Act>
    void loop(Mine mine, Act act) {
        for (;;) {
            std::unique_lock lk(m_);
            cv_.wait(lk, [&] { return cur_ > n_ || mine(cur_); });
            if (cur_ > n_) return;     // done: the thread that passed n woke us
            act(cur_);                 // print while holding the lock -> output order == cur_ order
            ++cur_;
            lk.unlock();
            cv_.notify_all();          // 4 waiters with 4 different predicates
        }
    }

public:
    explicit FizzBuzz(int n) : n_(n) {}
    void fizz(const std::function<void()>& printFizz) {
        loop([](int i) { return i % 3 == 0 && i % 5 != 0; }, [&](int) { printFizz(); });
    }
    void buzz(const std::function<void()>& printBuzz) {
        loop([](int i) { return i % 5 == 0 && i % 3 != 0; }, [&](int) { printBuzz(); });
    }
    void fizzbuzz(const std::function<void()>& printFizzBuzz) {
        loop([](int i) { return i % 15 == 0; }, [&](int) { printFizzBuzz(); });
    }
    void number(const std::function<void(int)>& printNumber) {
        loop([](int i) { return i % 3 != 0 && i % 5 != 0; }, [&](int i) { printNumber(i); });
    }
};

std::string run(int n) {
    FizzBuzz fb(n);
    std::string out;   // all appends happen under fb's mutex
    auto add = [&](const std::string& s) { out += s; out += ' '; };
    std::thread t1([&] { fb.fizz([&] { add("fizz"); }); });
    std::thread t2([&] { fb.buzz([&] { add("buzz"); }); });
    std::thread t3([&] { fb.fizzbuzz([&] { add("fizzbuzz"); }); });
    std::thread t4([&] { fb.number([&](int i) { add(std::to_string(i)); }); });
    t1.join(); t2.join(); t3.join(); t4.join();
    return out;
}

std::string expected(int n) {
    std::string s;
    for (int i = 1; i <= n; ++i) {
        s += i % 15 == 0 ? "fizzbuzz" : i % 3 == 0 ? "fizz" : i % 5 == 0 ? "buzz" : std::to_string(i);
        s += ' ';
    }
    return s;
}

int main() {
    std::printf("%s\n", run(15).c_str());
    for (int n : {1, 2, 3, 5, 15, 1000})
        if (run(n) != expected(n)) { std::printf("FAIL n=%d\n", n); return 1; }
    std::printf("all n OK\n");
}
```

### 6.4 Python Solution

```python
# fizzbuzz.py
import threading


class FizzBuzz:
    def __init__(self, n: int) -> None:
        self.n = n
        self.cur = 1
        self.cv = threading.Condition()

    def _loop(self, mine, act) -> None:
        while True:
            with self.cv:
                self.cv.wait_for(lambda: self.cur > self.n or mine(self.cur))
                if self.cur > self.n:
                    return
                act(self.cur)
                self.cur += 1
                self.cv.notify_all()

    def fizz(self, printFizz) -> None:
        self._loop(lambda i: i % 3 == 0 and i % 5 != 0, lambda i: printFizz())

    def buzz(self, printBuzz) -> None:
        self._loop(lambda i: i % 5 == 0 and i % 3 != 0, lambda i: printBuzz())

    def fizzbuzz(self, printFizzBuzz) -> None:
        self._loop(lambda i: i % 15 == 0, lambda i: printFizzBuzz())

    def number(self, printNumber) -> None:
        self._loop(lambda i: i % 3 != 0 and i % 5 != 0, printNumber)


def run(n: int) -> list[str]:
    fb, out = FizzBuzz(n), []
    targets = [
        (fb.fizz, lambda: out.append("fizz")),
        (fb.buzz, lambda: out.append("buzz")),
        (fb.fizzbuzz, lambda: out.append("fizzbuzz")),
        (fb.number, lambda i: out.append(str(i))),
    ]
    ts = [threading.Thread(target=f, args=(cb,)) for f, cb in targets]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    return out


def expected(n: int) -> list[str]:
    return ["fizzbuzz" if i % 15 == 0 else "fizz" if i % 3 == 0 else "buzz" if i % 5 == 0
            else str(i) for i in range(1, n + 1)]


if __name__ == "__main__":
    print(" ".join(run(15)))
    for n in (1, 2, 3, 5, 15, 500):
        assert run(n) == expected(n), n
    print("all n OK")
```

### 6.5 Correctness and Complexity

- **Safety:** `cur` is read and incremented only under the mutex, and a thread prints only when `cur` is in its category, so each number is emitted exactly once, by the right thread, in increasing order.
- **Liveness and termination:** for every `cur <= n` exactly one thread's predicate is true; whoever increments `cur` notifies all, so that thread wakes. When `cur` becomes `n + 1`, the predicate `cur > n` is true for everybody.
- **Cost:** n steps; each step wakes all 3 other threads, so about 3n wakeups (thundering herd). The dispatcher-with-semaphores variant needs about 2n targeted wakeups for the non-number values.

### 6.6 Pitfalls

- **Exit condition not in the predicate:** a thread waiting for "my number" will never see one after `cur > n` and hangs at the end. This is the most common bug in this problem.
- Printing after unlocking: another thread can print the next value first, so output order breaks.
- Precedence: test `% 15` before `% 3` and `% 5` (or use the explicit "and not" forms as above).

### 6.7 Interview Questions

**Q1. Why `notify_all` here, when Section 1 says unlock-then-`notify_one` is cheaper?**

Because the four waiters wait for *different* predicates on the same condition variable. `notify_one` might wake `buzz` when `cur` is a fizz number; `buzz` re-sleeps and the fizz thread is never woken, so the program hangs. Either `notify_all` or one condition variable per category (with the incrementer notifying the right one) is required.

**Q2. Is a multithreaded FizzBuzz faster than a single-threaded one?**

No -- it is strictly sequential, so it is slower (every step is a cross-thread hand-off costing microseconds versus nanoseconds for a modulo). The problem tests coordination, not parallelism. Say so in the interview; it shows you can tell the two apart.

---

## 7. The Dining Philosophers (LeetCode 1226)

### 7.1 Problem

Five philosophers sit at a round table with one fork between each pair. Philosopher `p` needs both adjacent forks to eat: we number fork `p` as their left fork and fork `(p + 1) % 5` as their right fork. Implement `wantsToEat(philosopher, pickLeftFork, pickRightFork, eat, putLeftFork, putRightFork)` so that no fork is ever held by two philosophers, there is no deadlock, and every philosopher eventually eats. Each philosopher calls `wantsToEat` many times, concurrently.

### 7.2 Why the Naive Solution Deadlocks

"Lock left, then lock right" satisfies all four **Coffman conditions**: mutual exclusion (a fork has one holder), hold-and-wait (holding left while waiting for right), no preemption (forks are not taken away), and **circular wait** (if all five pick up their left fork simultaneously, each waits for its right neighbor -- a cycle of length 5). Deadlock avoidance means breaking at least one condition:

| Strategy | Condition broken | How | Pros | Cons |
|---|---|---|---|---|
| **1. Resource ordering** | Circular wait | Always lock the lower-numbered fork first (philosopher 4 locks fork 0 before fork 4) | No extra state; generalizes to any lock set (lock hierarchy) | Requires a global order known in advance; philosopher 4 contends harder for fork 0 |
| **2. Limit diners (waiter / semaphore of N-1)** | Circular wait (a cycle needs all N) | `counting_semaphore<4>` admits at most 4 to the table | Trivial to add; keeps naive left-then-right code | One more synchronization point; reduces max parallelism slightly |
| **3. Atomic acquisition of both forks** | Hold-and-wait | `std::scoped_lock(left, right)` (try-and-back-off), or a monitor that grants both forks only when both are free | Never holds one fork while blocking on the other | `std::lock` can spin/retry under contention; monitor serializes decisions through one mutex |
| (Also) Chandy/Misra | Circular wait via dirty/clean forks + requests | Message passing between neighbors | Fair, distributed | Too long for an interview; mention by name |

None of these, by itself, guarantees **fairness**: `std::mutex` is not FIFO, so a philosopher can lose every race (starvation is possible in theory, rare in practice). Strict fairness needs FIFO locks (ticket locks, Section 10) or a monitor that serves requests in arrival order.

### 7.3 C++20 Solution (all three strategies, with a mutual-exclusion checker)

```cpp
// dining_philosophers.cpp -- g++ -std=c++20 -O2 -pthread dining_philosophers.cpp
#include <algorithm>
#include <array>
#include <atomic>
#include <cstdio>
#include <functional>
#include <mutex>
#include <semaphore>
#include <thread>
#include <vector>

using Action = std::function<void()>;
constexpr int N = 5;

// Strategy 1: resource ordering -- lower-numbered fork first breaks the cycle.
class DiningOrdered {
    std::array<std::mutex, N> forks_;
public:
    void wantsToEat(int p, const Action& pickLeft, const Action& pickRight, const Action& eat,
                    const Action& putLeft, const Action& putRight) {
        const int left = p, right = (p + 1) % N;
        std::lock_guard first(forks_[std::min(left, right)]);
        std::lock_guard second(forks_[std::max(left, right)]);
        pickLeft(); pickRight(); eat(); putLeft(); putRight();
    }
};

// Strategy 2: a "waiter" admits at most N-1 philosophers; naive left-then-right is then safe.
class DiningWaiter {
    std::array<std::mutex, N> forks_;
    std::counting_semaphore<N - 1> seats_{N - 1};
public:
    void wantsToEat(int p, const Action& pickLeft, const Action& pickRight, const Action& eat,
                    const Action& putLeft, const Action& putRight) {
        seats_.acquire();
        {
            std::lock_guard l(forks_[p]);
            std::lock_guard r(forks_[(p + 1) % N]);
            pickLeft(); pickRight(); eat(); putLeft(); putRight();
        }
        seats_.release();
    }
};

// Strategy 3: take both forks atomically. std::scoped_lock uses std::lock's deadlock-avoidance
// algorithm (lock one, try_lock the rest, back off and retry in a different order on failure).
class DiningBoth {
    std::array<std::mutex, N> forks_;
public:
    void wantsToEat(int p, const Action& pickLeft, const Action& pickRight, const Action& eat,
                    const Action& putLeft, const Action& putRight) {
        std::scoped_lock both(forks_[p], forks_[(p + 1) % N]);
        pickLeft(); pickRight(); eat(); putLeft(); putRight();
    }
};

template <class Table>
bool simulate(const char* name, int mealsEach) {
    Table table;
    std::array<std::atomic<int>, N> forkUsers{};   // must never exceed 1
    std::atomic<int> eating{0}, maxEating{0}, meals{0};
    std::atomic<bool> violation{false};

    auto philosopher = [&](int p) {
        const int left = p, right = (p + 1) % N;
        auto pick = [&](int f) { if (forkUsers[f].fetch_add(1) != 0) violation = true; };
        auto put = [&](int f) { forkUsers[f].fetch_sub(1); };
        for (int i = 0; i < mealsEach; ++i) {
            table.wantsToEat(
                p, [&] { pick(left); }, [&] { pick(right); },
                [&] {
                    int now = ++eating;
                    int prev = maxEating.load();
                    while (now > prev && !maxEating.compare_exchange_weak(prev, now)) {}
                    std::this_thread::yield();   // widen the window for overlap
                    --eating;
                    ++meals;
                },
                [&] { put(left); }, [&] { put(right); });
        }
    };
    std::vector<std::thread> ts;
    for (int p = 0; p < N; ++p) ts.emplace_back(philosopher, p);
    for (auto& t : ts) t.join();

    const bool ok = !violation && meals == N * mealsEach && maxEating <= N / 2;
    std::printf("%-22s meals=%d maxConcurrentEaters=%d %s\n", name, meals.load(),
                maxEating.load(), ok ? "OK" : "FAIL");
    return ok;
}

int main() {
    bool ok = simulate<DiningOrdered>("resource ordering", 5000);
    ok &= simulate<DiningWaiter>("waiter (N-1 seats)", 5000);
    ok &= simulate<DiningBoth>("scoped_lock both", 5000);
    return ok ? 0 : 1;
}
```

### 7.4 Python Solution (all three strategies)

Python has no `std::lock` equivalent, so strategy 3 is written as a **monitor**: one condition variable guards a `fork_free` array, and a philosopher waits until *both* forks are free, then takes them in one step (Tanenbaum's classic solution).

```python
# dining_philosophers.py
import threading

N = 5


class DiningOrdered:
    def __init__(self) -> None:
        self.forks = [threading.Lock() for _ in range(N)]

    def wantsToEat(self, p, pickLeft, pickRight, eat, putLeft, putRight) -> None:
        left, right = p, (p + 1) % N
        lo, hi = min(left, right), max(left, right)
        with self.forks[lo], self.forks[hi]:     # always lower-numbered first
            pickLeft(); pickRight(); eat(); putLeft(); putRight()


class DiningWaiter:
    def __init__(self) -> None:
        self.forks = [threading.Lock() for _ in range(N)]
        self.seats = threading.Semaphore(N - 1)

    def wantsToEat(self, p, pickLeft, pickRight, eat, putLeft, putRight) -> None:
        with self.seats, self.forks[p], self.forks[(p + 1) % N]:
            pickLeft(); pickRight(); eat(); putLeft(); putRight()


class DiningMonitor:
    def __init__(self) -> None:
        self.cv = threading.Condition()
        self.fork_free = [True] * N

    def wantsToEat(self, p, pickLeft, pickRight, eat, putLeft, putRight) -> None:
        left, right = p, (p + 1) % N
        with self.cv:
            self.cv.wait_for(lambda: self.fork_free[left] and self.fork_free[right])
            self.fork_free[left] = self.fork_free[right] = False   # take both at once
        pickLeft(); pickRight(); eat(); putLeft(); putRight()       # eat outside the monitor
        with self.cv:
            self.fork_free[left] = self.fork_free[right] = True
            self.cv.notify_all()   # both neighbours may now be able to eat


def simulate(table, meals_each: int = 300) -> None:
    users = [0] * N
    guard = threading.Lock()                 # protects the checker's own counters
    state = {"meals": 0, "violation": False}

    def pick(f: int) -> None:
        with guard:
            users[f] += 1
            state["violation"] |= users[f] > 1

    def put(f: int) -> None:
        with guard:
            users[f] -= 1

    def eat() -> None:
        with guard:
            state["meals"] += 1

    def philosopher(p: int) -> None:
        left, right = p, (p + 1) % N
        for _ in range(meals_each):
            table.wantsToEat(p, lambda: pick(left), lambda: pick(right), eat,
                             lambda: put(left), lambda: put(right))

    ts = [threading.Thread(target=philosopher, args=(p,)) for p in range(N)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    assert not state["violation"] and state["meals"] == N * meals_each
    print(f"{type(table).__name__:15} meals={state['meals']} OK")


if __name__ == "__main__":
    for table in (DiningOrdered(), DiningWaiter(), DiningMonitor()):
        simulate(table)
```

### 7.5 Correctness and Complexity

- **Ordering:** a deadlock needs a cycle in the wait-for graph. If every thread acquires locks in increasing global order, every wait-for edge goes from a lower-numbered held lock to a higher-numbered wanted lock, so a cycle would need a lock strictly greater than itself -- impossible.
- **Waiter:** with at most 4 philosophers holding or wanting 5 forks, by pigeonhole at least one seated philosopher can get both forks, so someone always makes progress.
- **Atomic acquisition:** nobody waits while holding a fork, so hold-and-wait never occurs. The monitor version decides both forks under one mutex, so the check-and-take is atomic.
- **Parallelism:** at most `floor(5 / 2) = 2` philosophers can eat at once; all three strategies can achieve 2.
- **Cost:** O(1) lock operations per meal; contention is local (each fork is shared by only two philosophers), except the monitor, which funnels every decision through one lock.

### 7.6 Pitfalls

- **`try_lock` the second fork, release, retry immediately** avoids deadlock but can **livelock** (everyone picks left, fails right, puts down, repeats in lockstep). Add randomized backoff, or use `std::scoped_lock`, which already does try-and-back-off internally.
- **Odd/even asymmetry** ("even philosophers pick left first, odd pick right first") is just resource ordering in disguise -- fine, but be ready to explain why it works.
- **Holding the monitor's mutex while eating** in strategy 3 serializes the whole table (only one philosopher eats at a time); take forks inside, eat outside.
- In Python, `with a, b:` acquires `a` then `b` -- the same as nested `with` statements, so the ordering argument applies.
- **ThreadSanitizer flags strategy 2** with `lock-order-inversion (potential deadlock)`: its lock graph really contains the cycle fork0 -> fork1 -> ... -> fork4 -> fork0, and TSan does not know that the semaphore makes the full cycle unreachable. Strategies 1 and 3 run clean under `-fsanitize=thread`. This is a useful interview point: strategy 2's safety rests on a *non-local* invariant (the seat count), which tools and future maintainers cannot see; lock ordering is locally checkable.

### 7.7 Interview Questions

**Q1. How does `std::scoped_lock` (or `std::lock`) avoid deadlock for an arbitrary set of mutexes?**

The standard only requires "a deadlock-avoidance algorithm such as try-and-back-off". libstdc++ blocks on one mutex, then `try_lock`s the others; if any `try_lock` fails, it releases everything it holds and retries, blocking first on the mutex that was busy (so it waits on the contended one rather than spinning). Because it never blocks while holding another of *these* mutexes, it cannot participate in a cycle among them. It does not protect against cycles involving other locks acquired elsewhere.

**Q2. How would you detect a potential deadlock in a large codebase rather than avoid it by design?**

Build a lock-order graph at runtime: on each acquisition, add an edge from every lock currently held by the thread to the new lock and report a cycle (this is what ThreadSanitizer's "lock-order-inversion" report and the Linux kernel's `lockdep` do). For a live hang, take `thread apply all bt` in gdb and look for threads blocked in `pthread_mutex_lock`/`futex_wait` while holding each other's locks.

**Q3. Strategy 2 uses N-1 seats. Would N-2 also work? Why not use N-2?**

It works (any limit below N breaks the cycle), but it unnecessarily lowers throughput: you want the largest limit that still prevents the full cycle, which is N-1.

---

## 8. Bounded Blocking Queue (LeetCode 1188)

### 8.1 Problem

Implement a thread-safe `BoundedBlockingQueue(capacity)` with `enqueue(element)` (blocks while the queue is full), `dequeue()` (blocks while empty, returns the front element), and `size()`. Multiple producer and consumer threads use it concurrently. Common follow-ups: graceful shutdown (`close()`), timeouts, and why two condition variables.

### 8.2 Approach

Classic monitor: one mutex guards a `deque`; two condition variables express the two wait conditions -- `notFull` (producers wait on it) and `notEmpty` (consumers wait on it). Because each condition variable has only one *kind* of waiter, `notify_one` is safe and efficient: after an enqueue exactly one consumer can make progress, and after a dequeue exactly one producer can.

The textbook alternative uses two counting semaphores plus a mutex (`emptySlots = capacity`, `fullSlots = 0`): `enqueue` does `emptySlots.acquire(); lock; push; unlock; fullSlots.release()`. It is elegant but makes shutdown and timeouts awkward, so the monitor is what most interviewers expect.

### 8.3 C++20 Solution (with close and timed dequeue)

```cpp
// bounded_blocking_queue.cpp -- g++ -std=c++20 -O2 -pthread bounded_blocking_queue.cpp
#include <chrono>
#include <condition_variable>
#include <cstdio>
#include <deque>
#include <mutex>
#include <optional>
#include <thread>
#include <vector>

template <class T>
class BoundedBlockingQueue {
public:
    explicit BoundedBlockingQueue(std::size_t capacity) : capacity_(capacity) {}

    // Blocks while full. Returns false (and drops the item) if the queue was closed.
    bool enqueue(T item) {
        std::unique_lock lk(m_);
        notFull_.wait(lk, [&] { return q_.size() < capacity_ || closed_; });
        if (closed_) return false;
        q_.push_back(std::move(item));
        lk.unlock();
        notEmpty_.notify_one();          // exactly one consumer can use one new item
        return true;
    }

    // Blocks while empty. Returns nullopt only when closed AND drained.
    std::optional<T> dequeue() {
        std::unique_lock lk(m_);
        notEmpty_.wait(lk, [&] { return !q_.empty() || closed_; });
        return popLocked(lk);
    }

    // Returns nullopt on timeout or when closed and drained.
    template <class Rep, class Period>
    std::optional<T> dequeue_for(std::chrono::duration<Rep, Period> timeout) {
        std::unique_lock lk(m_);
        if (!notEmpty_.wait_for(lk, timeout, [&] { return !q_.empty() || closed_; }))
            return std::nullopt;         // predicate still false after the timeout
        return popLocked(lk);
    }

    std::size_t size() const {
        std::lock_guard g(m_);
        return q_.size();
    }

    // Wake everybody: producers fail fast, consumers drain what is left then get nullopt.
    void close() {
        {
            std::lock_guard g(m_);
            closed_ = true;
        }
        notFull_.notify_all();
        notEmpty_.notify_all();
    }

private:
    std::optional<T> popLocked(std::unique_lock<std::mutex>& lk) {
        if (q_.empty()) return std::nullopt;   // closed and drained
        T item = std::move(q_.front());
        q_.pop_front();
        lk.unlock();
        notFull_.notify_one();                 // one slot freed -> one producer may proceed
        return item;
    }

    mutable std::mutex m_;
    std::condition_variable notFull_, notEmpty_;
    std::deque<T> q_;
    const std::size_t capacity_;
    bool closed_ = false;
};

int main() {
    constexpr int kProducers = 4, kConsumers = 3, kItemsEach = 50000;
    BoundedBlockingQueue<long> q(16);   // small capacity -> lots of blocking on both sides

    std::vector<std::thread> producers, consumers;
    std::vector<long> consumedSum(kConsumers, 0), consumedCount(kConsumers, 0);
    for (int c = 0; c < kConsumers; ++c)
        consumers.emplace_back([&, c] {
            while (auto item = q.dequeue()) {
                consumedSum[c] += *item;
                ++consumedCount[c];
            }
        });
    for (int p = 0; p < kProducers; ++p)
        producers.emplace_back([&] {
            for (long i = 1; i <= kItemsEach; ++i) q.enqueue(i);
        });
    for (auto& t : producers) t.join();
    q.close();                          // all items are in; let consumers drain and exit
    for (auto& t : consumers) t.join();

    long sum = 0, count = 0;
    for (int c = 0; c < kConsumers; ++c) { sum += consumedSum[c]; count += consumedCount[c]; }
    const long expectedSum = long(kProducers) * kItemsEach * (kItemsEach + 1) / 2;
    std::printf("consumed %ld items, sum %ld (expected %ld) -> %s\n", count, sum, expectedSum,
                count == long(kProducers) * kItemsEach && sum == expectedSum ? "OK" : "FAIL");

    auto timedOut = q.dequeue_for(std::chrono::milliseconds(10));
    std::printf("dequeue on closed+empty queue: %s, enqueue after close: %s\n",
                timedOut ? "item" : "nullopt", q.enqueue(1) ? "accepted" : "rejected");
}
```

### 8.4 Python Solution

Two `Condition` objects can share **one** `Lock` -- that is how you get "two condition variables, one mutex" in Python.

```python
# bounded_blocking_queue.py
import collections
import threading


class QueueClosed(Exception):
    pass


class BoundedBlockingQueue:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self._q: collections.deque = collections.deque()
        self._lock = threading.Lock()
        self._not_full = threading.Condition(self._lock)
        self._not_empty = threading.Condition(self._lock)
        self._closed = False

    def enqueue(self, element) -> None:
        with self._not_full:
            self._not_full.wait_for(lambda: len(self._q) < self.capacity or self._closed)
            if self._closed:
                raise QueueClosed
            self._q.append(element)
            self._not_empty.notify()

    def dequeue(self, timeout: float | None = None):
        with self._not_empty:
            if not self._not_empty.wait_for(lambda: self._q or self._closed, timeout):
                raise TimeoutError
            if not self._q:
                raise QueueClosed          # closed and drained
            item = self._q.popleft()
            self._not_full.notify()
            return item

    def size(self) -> int:
        with self._lock:
            return len(self._q)

    def close(self) -> None:
        with self._lock:
            self._closed = True
            self._not_full.notify_all()
            self._not_empty.notify_all()


if __name__ == "__main__":
    q = BoundedBlockingQueue(8)
    producers_n, consumers_n, items_each = 4, 3, 5000
    totals = [0] * consumers_n

    def producer() -> None:
        for i in range(1, items_each + 1):
            q.enqueue(i)

    def consumer(c: int) -> None:
        try:
            while True:
                totals[c] += q.dequeue()
        except QueueClosed:
            pass

    cons = [threading.Thread(target=consumer, args=(c,)) for c in range(consumers_n)]
    prods = [threading.Thread(target=producer) for _ in range(producers_n)]
    for t in cons + prods:
        t.start()
    for t in prods:
        t.join()
    q.close()
    for t in cons:
        t.join()
    expected = producers_n * items_each * (items_each + 1) // 2
    assert sum(totals) == expected, (sum(totals), expected)
    print(f"sum={sum(totals)} OK")
```

In production Python, use `queue.Queue(maxsize=...)` (it is exactly this design: one lock, conditions `not_empty`, `not_full`, `all_tasks_done`). Python 3.13 added `Queue.shutdown()` and the `queue.ShutDown` exception, which play the role of `close()` above.

### 8.5 Correctness and Complexity

- **Invariant:** `0 <= q.size() <= capacity`, enforced because pushes happen only after observing `size < capacity` under the lock and pops only after observing non-empty.
- **No lost wakeups:** every state change that can make a predicate true is followed by a notify on the matching condition variable, and the state change is made under the same mutex the waiter checks under.
- **Shutdown:** `close()` flips a flag that is part of *both* predicates, then `notify_all`s both condition variables, so every blocked thread wakes and returns. Consumers still drain remaining items (the nullopt case requires `closed && empty`).
- **Cost:** O(1) per operation; one mutex is the scalability limit (~10-50 M ops/s uncontended, far fewer under heavy contention). For higher throughput: per-producer SPSC rings, or a lock-free MPMC ring (e.g. Vyukov's bounded queue).

### 8.6 Pitfalls

- **`if` instead of `while`/predicate:** a consumer woken by `notify_all` finds the queue already emptied by another consumer and pops from an empty deque.
- **One condition variable + `notify_one`:** a producer's notify can wake another producer (whose predicate is false), which re-sleeps; the consumer that should have run is never woken -> hang under load. With one condition variable you must `notify_all`.
- **Shutdown via a sentinel value** (pushing `None`/`-1`) works for a single consumer but needs one sentinel per consumer, and fails when producers are blocked on a full queue. A `closed` flag in the predicates handles both sides.
- **`size()` is only a snapshot**: never write `if (q.size() > 0) q.dequeue();` -- check-then-act races; use `try_dequeue`-style APIs instead.

### 8.7 Interview Questions

**Q1. Should you notify while holding the lock or after releasing it?**

Both are correct as long as the predicate state was modified under the lock. Notifying after unlocking avoids the "hurry up and wait" effect (the woken thread runs, immediately blocks on the still-held mutex, and sleeps again). Notify *under* the lock when the condition variable's lifetime might end as soon as the waiter returns (e.g. the waiter destroys the object containing it), or when you rely on a strict fairness property of your platform. Python forces you to hold the lock to notify (`RuntimeError` otherwise).

**Q2. How would you make `enqueue` non-blocking when the queue is full (load shedding)?**

Add `try_enqueue(item) -> bool` that takes the lock, checks `size < capacity`, and returns false immediately if full; or `enqueue_for(item, timeout)` using `wait_for` with the same predicate. Blocking provides back-pressure (the producer slows down); dropping or returning an error is the right choice when latency matters more than completeness (e.g. telemetry/profiling samples).

**Q3. How does a lock-free bounded MPMC queue differ?**

It replaces the mutex with per-slot sequence numbers and CAS on head/tail indices (Vyukov's design): a producer claims slot `tail` via CAS, writes the item, then publishes it by storing `seq = tail + 1` with release semantics; consumers wait for that sequence. It never blocks in the kernel, so it needs a separate strategy for "wait when empty" (spin, then park on a futex/eventfd). It is much harder to make correct and to test, so only use it when the mutex is measured to be the bottleneck.

---

## 9. Reader-Writer Lock

### 9.1 Problem

Implement a lock that allows **many concurrent readers or one writer**. Provide `lock_shared()/unlock_shared()` for readers and `lock()/unlock()` for writers (these names make it usable with `std::shared_lock` and `std::unique_lock`). Implement two policies:

- **Reader-preferring:** readers enter whenever no writer is *active*. Maximizes read throughput; a continuous stream of readers can **starve writers**.
- **Writer-preferring:** new readers are blocked while any writer is *waiting*. Writers cannot starve; a continuous stream of writers can **starve readers**.

### 9.2 Approach

State, guarded by one mutex: `readers` (active readers), `writer` (is a writer active), and for the writer-preferring version `waitingWriters`.

| Operation | Reader-preferring wait predicate | Writer-preferring wait predicate |
|---|---|---|
| `lock_shared` | `!writer` | `!writer && waitingWriters == 0` |
| `lock` | `!writer && readers == 0` | `!writer && readers == 0` (and count itself in `waitingWriters` while waiting) |
| `unlock_shared` | if `readers` drops to 0: wake a writer | same |
| `unlock` | wake everyone | wake one waiting writer if any, else all readers |

### 9.3 C++20 Solution (both policies)

```cpp
// rw_lock.cpp -- g++ -std=c++20 -O2 -pthread rw_lock.cpp
#include <atomic>
#include <condition_variable>
#include <cstdio>
#include <mutex>
#include <shared_mutex>
#include <thread>
#include <vector>

class ReaderPrefRWLock {
    std::mutex m_;
    std::condition_variable cv_;
    int readers_ = 0;
    bool writer_ = false;

public:
    void lock_shared() {
        std::unique_lock lk(m_);
        cv_.wait(lk, [&] { return !writer_; });   // ignores waiting writers -> readers win
        ++readers_;
    }
    void unlock_shared() {
        std::unique_lock lk(m_);
        if (--readers_ == 0) {
            lk.unlock();
            cv_.notify_one();   // while readers_ > 0, writer_ is false, so only writers can be waiting
        }
    }
    void lock() {
        std::unique_lock lk(m_);
        cv_.wait(lk, [&] { return !writer_ && readers_ == 0; });
        writer_ = true;
    }
    void unlock() {
        {
            std::lock_guard g(m_);
            writer_ = false;
        }
        cv_.notify_all();       // all waiting readers (and possibly a writer) may proceed
    }
};

class WriterPrefRWLock {
    std::mutex m_;
    std::condition_variable readersCv_, writersCv_;
    int readers_ = 0;
    int waitingWriters_ = 0;
    bool writer_ = false;

public:
    void lock_shared() {
        std::unique_lock lk(m_);
        readersCv_.wait(lk, [&] { return !writer_ && waitingWriters_ == 0; });
        ++readers_;
    }
    void unlock_shared() {
        std::unique_lock lk(m_);
        if (--readers_ == 0 && waitingWriters_ > 0) {
            lk.unlock();
            writersCv_.notify_one();
        }
    }
    void lock() {
        std::unique_lock lk(m_);
        ++waitingWriters_;      // from now on, new readers queue behind us
        writersCv_.wait(lk, [&] { return !writer_ && readers_ == 0; });
        --waitingWriters_;
        writer_ = true;
    }
    void unlock() {
        std::unique_lock lk(m_);
        writer_ = false;
        const bool writersWaiting = waitingWriters_ > 0;
        lk.unlock();
        if (writersWaiting) writersCv_.notify_one();   // hand off writer-to-writer
        else readersCv_.notify_all();                  // release the whole reader batch
    }
};

// Shared data protected by the RW lock: the invariant is a == b.
struct Data { long a = 0, b = 0; };

template <class RW>
bool stress(const char* name) {
    RW rw;
    Data d;
    std::atomic<int> activeReaders{0}, activeWriters{0}, maxReaders{0};
    std::atomic<bool> violation{false};
    std::atomic<long> reads{0};

    auto reader = [&] {
        for (int i = 0; i < 20000; ++i) {
            std::shared_lock lk(rw);                       // works: RW has lock_shared/unlock_shared
            int r = ++activeReaders;
            int prev = maxReaders.load();
            while (r > prev && !maxReaders.compare_exchange_weak(prev, r)) {}
            if (activeWriters.load() != 0 || d.a != d.b) violation = true;
            --activeReaders;
            ++reads;
        }
    };
    auto writer = [&] {
        for (int i = 0; i < 5000; ++i) {
            std::unique_lock lk(rw);                       // works: RW has lock/unlock
            if (++activeWriters != 1 || activeReaders.load() != 0) violation = true;
            ++d.a; ++d.b;
            --activeWriters;
        }
    };
    std::vector<std::thread> ts;
    for (int i = 0; i < 4; ++i) ts.emplace_back(reader);
    for (int i = 0; i < 2; ++i) ts.emplace_back(writer);
    for (auto& t : ts) t.join();

    const bool ok = !violation && d.a == 2 * 5000 && d.b == d.a;
    std::printf("%-18s writes=%ld reads=%ld maxConcurrentReaders=%d %s\n", name, d.a,
                reads.load(), maxReaders.load(), ok ? "OK" : "FAIL");
    return ok;
}

int main() {
    bool ok = stress<ReaderPrefRWLock>("reader-preferring");
    ok &= stress<WriterPrefRWLock>("writer-preferring");
    ok &= stress<std::shared_mutex>("std::shared_mutex");
    return ok ? 0 : 1;
}
```

### 9.4 Python Solution (both policies, with context managers)

```python
# rw_lock.py
import contextlib
import threading


class ReaderPrefRWLock:
    def __init__(self) -> None:
        self._cv = threading.Condition()
        self._readers = 0
        self._writer = False

    def acquire_read(self) -> None:
        with self._cv:
            self._cv.wait_for(lambda: not self._writer)
            self._readers += 1

    def release_read(self) -> None:
        with self._cv:
            self._readers -= 1
            if self._readers == 0:
                self._cv.notify_all()

    def acquire_write(self) -> None:
        with self._cv:
            self._cv.wait_for(lambda: not self._writer and self._readers == 0)
            self._writer = True

    def release_write(self) -> None:
        with self._cv:
            self._writer = False
            self._cv.notify_all()

    @contextlib.contextmanager
    def read_locked(self):
        self.acquire_read()
        try:
            yield
        finally:
            self.release_read()

    @contextlib.contextmanager
    def write_locked(self):
        self.acquire_write()
        try:
            yield
        finally:
            self.release_write()


class WriterPrefRWLock(ReaderPrefRWLock):
    def __init__(self) -> None:
        super().__init__()
        self._waiting_writers = 0

    def acquire_read(self) -> None:
        with self._cv:
            self._cv.wait_for(lambda: not self._writer and self._waiting_writers == 0)
            self._readers += 1

    def acquire_write(self) -> None:
        with self._cv:
            self._waiting_writers += 1
            self._cv.wait_for(lambda: not self._writer and self._readers == 0)
            self._waiting_writers -= 1
            self._writer = True


def stress(rw) -> None:
    data = {"a": 0, "b": 0}
    errors = []

    def reader() -> None:
        for _ in range(3000):
            with rw.read_locked():
                if data["a"] != data["b"]:
                    errors.append("torn read")

    def writer() -> None:
        for _ in range(1000):
            with rw.write_locked():
                data["a"] += 1
                data["b"] += 1

    ts = [threading.Thread(target=reader) for _ in range(4)]
    ts += [threading.Thread(target=writer) for _ in range(2)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    assert not errors and data["a"] == data["b"] == 2000
    print(f"{type(rw).__name__:17} OK")


if __name__ == "__main__":
    stress(ReaderPrefRWLock())
    stress(WriterPrefRWLock())
```

The Python version uses a single condition variable with `notify_all` for simplicity; the C++ writer-preferring version uses two condition variables so that a writer hand-off wakes exactly one writer instead of every reader.

### 9.5 Correctness and Complexity

- **Mutual exclusion:** a writer sets `writer = true` only when `readers == 0 && !writer`, and readers increment `readers` only when `!writer`; both checks and updates happen under the mutex, so "writer active" and "readers > 0" are never true at the same time.
- **No lost wakeups:** the only transitions that can make a waiter's predicate true are `readers -> 0` (wake a writer), `writer -> false` (wake writers/readers), and in the writer-preferring lock `waitingWriters -> 0`, which coincides with a writer becoming active, whose `unlock` then wakes readers.
- **Starvation:** reader-preferring can starve writers (readers keep `readers > 0` forever); writer-preferring can starve readers. A **fair (phase-fair)** lock alternates: when a writer is waiting, new readers wait; when the writer finishes, *all readers that were waiting* go before the next writer.
- **Cost:** every `lock_shared` still takes the internal mutex and writes `readers` -- a shared cache line. Under many cores, read-mostly workloads can scale *worse* than a plain mutex because of this cache-line ping-pong. Scalable alternatives: per-CPU reader counters ("big reader" locks), seqlocks (readers retry instead of writing), or RCU.

### 9.6 Pitfalls

- **Upgrading a read lock to a write lock** by calling `lock()` while holding `lock_shared()` deadlocks as soon as two readers try it (each waits for the other's read lock to go away). Release and reacquire, then re-validate; or use an explicit "upgradable" mode that only one thread may hold.
- **Recursive read locks under writer preference:** thread A holds a read lock, a writer starts waiting, A requests the read lock again -> A waits for the writer, the writer waits for A. This is why glibc ignores `PTHREAD_RWLOCK_PREFER_WRITER_NP` and you must use `PTHREAD_RWLOCK_PREFER_WRITER_NONRECURSIVE_NP` to get writer preference.
- `std::shared_mutex`'s policy is **unspecified** by the standard. On Linux with libstdc++ it wraps `pthread_rwlock_t`, whose glibc default kind is `PTHREAD_RWLOCK_PREFER_READER_NP`, so writers can starve under heavy read load.
- RW locks only pay off when critical sections are long relative to the lock overhead and reads dominate. For a few-nanosecond read of a small struct, a plain mutex or a seqlock is usually faster.

### 9.7 Interview Questions

**Q1. When is an RW lock slower than a plain mutex?**

When read critical sections are short. Each `lock_shared`/`unlock_shared` performs an atomic read-modify-write on the same reader-count cache line, which must bounce between cores in exclusive (M) state; with 32 reader threads that line becomes the bottleneck and readers serialize on cache-coherence traffic anyway, while paying for the more complex logic. Measure before switching.

**Q2. What is a seqlock and when would you use it instead?**

A seqlock has a sequence counter: the writer increments it (odd = write in progress), writes the data, increments again (even). Readers read the counter, copy the data, re-read the counter, and retry if it changed or was odd. Readers never write shared memory, so reads scale perfectly; writers never wait for readers. It suits small, frequently read, rarely written data (the Linux kernel uses it for timekeeping). Caveats: readers can observe torn data mid-copy (they must not dereference it before validating), so the data must be trivially copyable, and in C++ the racy copy must use atomics/fences to be well-defined.

---

## 10. Spinlocks and a Futex-Based Mutex

### 10.1 Problem

"Implement a lock using only atomics." Expected progression in a systems interview: (1) a test-and-set (TAS) spinlock, (2) explain why it scales badly and fix it with test-and-test-and-set (TTAS) plus exponential backoff, (3) a FIFO ticket lock for fairness, and (4) explain how a real mutex avoids burning CPU -- the **futex** fast path / slow path -- and implement it.

### 10.2 Approach and Hardware Background

| Lock | Acquire | Coherence traffic while waiting | Fair? | Best for |
|---|---|---|---|---|
| TAS | `while (flag.test_and_set(acquire)) ;` | Every spin is an atomic RMW, which needs the cache line in **exclusive (M/E)** state -> the line ping-pongs between all spinning cores | No | Never, except as a teaching step |
| TTAS + backoff | Spin on a plain `load` until free, then one `exchange`; on failure back off exponentially | Spinners share the line in **S** state and spin in their own L1; traffic only when the lock is released | No | Very short critical sections, threads <= cores |
| Ticket lock | `my = next.fetch_add(1)`; spin until `serving == my` | All waiters re-read `serving` on each release (O(waiters) invalidations per hand-off) | **FIFO** | Fairness needed, low core counts |
| MCS / CLH queue lock | Each waiter spins on its *own* node | O(1) per hand-off | FIFO | High core counts (kernel `qspinlock` is MCS-based) |
| Futex mutex | CAS fast path; on contention sleep in the kernel | None while asleep | No (barging) | General purpose (this is how `pthread_mutex_t` works) |

**Memory ordering:** `lock()` needs **acquire** (no read/write in the critical section may be reordered before the lock is taken) and `unlock()` needs **release** (all critical-section writes become visible before the lock appears free). Acquire on the successful RMW and release on the store is exactly sufficient; `seq_cst` is correct but stronger than needed. The read-only "test" spin can be `relaxed` because the subsequent `exchange(acquire)` is what synchronizes.

**Why spinlocks are dangerous in user space:** if the holder is preempted (more runnable threads than cores), every waiter burns its full time slice spinning on a lock that cannot be released. The kernel can disable preemption while holding a spinlock; user space cannot. Hence user-space locks **spin briefly, then sleep** (adaptive mutexes), and the TTAS below falls back to `yield()`.

**Futex (fast userspace mutex):** the lock word lives in user memory. Uncontended lock/unlock is a single atomic instruction with **no system call**. Only on contention does a thread call `futex(addr, FUTEX_WAIT, expected)`: the kernel atomically re-checks `*addr == expected` and puts the thread to sleep on a wait queue keyed by the address; if the value already changed, it returns immediately -- that atomic check-and-sleep is what prevents lost wakeups. `unlock` calls `FUTEX_WAKE` only if the lock word says there may be waiters. Ulrich Drepper's paper *Futexes Are Tricky* gives the three-state mutex below: `0` unlocked, `1` locked with no waiters, `2` locked with possible waiters.

### 10.3 C++20 Solution (TAS, TTAS + backoff, ticket lock, futex mutex)

`std::atomic<int>::wait/notify_one` (C++20) is the portable futex interface: on Linux, libstdc++ implements it for 4-byte types directly with the `futex` system call (after a short spin).

```cpp
// spinlocks.cpp -- g++ -std=c++20 -O2 -pthread spinlocks.cpp
#include <algorithm>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <mutex>
#include <thread>
#include <vector>

#if defined(__x86_64__) || defined(__i386__)
#include <immintrin.h>
inline void cpu_relax() { _mm_pause(); }   // PAUSE: saves power, avoids memory-order mis-speculation
#elif defined(__aarch64__)
inline void cpu_relax() { asm volatile("yield" ::: "memory"); }
#else
inline void cpu_relax() { std::this_thread::yield(); }
#endif

// Spin a little, then give the core away (protects against a preempted lock holder).
struct SpinWait {
    unsigned n = 0;
    void operator()() {
        if (++n < 128) cpu_relax();
        else std::this_thread::yield();
    }
};

// 1. Test-and-set: every iteration is a read-modify-write on the shared line.
class TASLock {
    std::atomic_flag flag_;   // C++20: default-initialized to clear
public:
    void lock() {
        SpinWait w;
        while (flag_.test_and_set(std::memory_order_acquire)) w();
    }
    bool try_lock() { return !flag_.test_and_set(std::memory_order_acquire); }
    void unlock() { flag_.clear(std::memory_order_release); }
};

// 2. Test-and-test-and-set with exponential backoff.
class TTASLock {
    std::atomic<bool> locked_{false};
public:
    void lock() {
        unsigned backoff = 1;
        constexpr unsigned kMaxBackoff = 1024;
        for (;;) {
            SpinWait w;
            while (locked_.load(std::memory_order_relaxed)) w();          // test: local, read-only
            if (!locked_.exchange(true, std::memory_order_acquire)) return; // test-and-set
            for (unsigned i = 0; i < backoff; ++i) cpu_relax();           // lost the race: back off
            backoff = std::min(backoff * 2, kMaxBackoff);
        }
    }
    bool try_lock() {
        return !locked_.load(std::memory_order_relaxed) &&
               !locked_.exchange(true, std::memory_order_acquire);
    }
    void unlock() { locked_.store(false, std::memory_order_release); }
};

// 3. Ticket lock: FIFO fairness, like a deli counter.
class TicketLock {
    std::atomic<std::uint32_t> next_{0};
    std::atomic<std::uint32_t> serving_{0};
public:
    void lock() {
        const std::uint32_t my = next_.fetch_add(1, std::memory_order_relaxed);
        SpinWait w;
        while (serving_.load(std::memory_order_acquire) != my) w();
    }
    void unlock() {
        // Only the holder writes serving_, so a plain load + store (not an RMW) is enough.
        serving_.store(serving_.load(std::memory_order_relaxed) + 1, std::memory_order_release);
    }
};

// 4. Futex-style mutex (Drepper, "Futexes Are Tricky", mutex #3).
class FutexMutex {
    std::atomic<int> state_{0};   // 0 unlocked, 1 locked/no waiters, 2 locked/maybe waiters
public:
    void lock() {
        int c = 0;
        if (state_.compare_exchange_strong(c, 1, std::memory_order_acquire))
            return;                                            // fast path: one CAS, no syscall
        if (c != 2) c = state_.exchange(2, std::memory_order_acquire);
        while (c != 0) {                                       // slow path
            state_.wait(2, std::memory_order_relaxed);         // ~ futex_wait(&state_, 2)
            c = state_.exchange(2, std::memory_order_acquire); // claim it, pessimistically marking "waiters"
        }
    }
    void unlock() {
        if (state_.fetch_sub(1, std::memory_order_release) != 1) {  // was 2: someone may sleep
            state_.store(0, std::memory_order_release);
            state_.notify_one();                                    // ~ futex_wake(&state_, 1)
        }
    }
};

template <class Lock>
void bench(const char* name, int threads, long itersEach) {
    Lock lock;
    long counter = 0;   // plain long: protected only by `lock`
    auto t0 = std::chrono::steady_clock::now();
    std::vector<std::thread> ts;
    for (int t = 0; t < threads; ++t)
        ts.emplace_back([&] {
            for (long i = 0; i < itersEach; ++i) {
                std::lock_guard g(lock);
                ++counter;
            }
        });
    for (auto& t : ts) t.join();
    auto ms = std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
    std::printf("%-12s counter=%ld (%s) %8.1f ms\n", name, counter,
                counter == threads * itersEach ? "OK" : "FAIL", ms);
}

int main() {
    const int threads = 4;
    const long iters = 100000;
    bench<TASLock>("TAS", threads, iters);
    bench<TTASLock>("TTAS+backoff", threads, iters);
    bench<TicketLock>("ticket", threads, iters);
    bench<FutexMutex>("futex mutex", threads, iters);
    bench<std::mutex>("std::mutex", threads, iters);
}
```

Interpreting the benchmark (absolute numbers vary by machine; this is 4 threads on a large x86 server): TAS, TTAS, the futex mutex, and `std::mutex` all finish in a few to a few tens of milliseconds, while the **ticket lock is often 10-50x slower**. The reason is hand-off policy, not instruction count: unfair locks let the releasing thread immediately re-acquire the lock while its cache line is still hot ("lock stickiness"), so most acquisitions are uncontended. A FIFO ticket lock forces a cross-core hand-off on *every* release -- the line migrates each time, and if the next ticket holder is descheduled, everyone waits. Fairness costs throughput.

What `atomic::wait/notify_one` boil down to on Linux, if asked to write the system calls yourself:

```cpp
// fragment -- raw futex calls (Linux only); glibc provides no futex() wrapper
#include <linux/futex.h>
#include <sys/syscall.h>
#include <unistd.h>
#include <atomic>

// Sleeps only if *addr still equals `expected` (checked atomically by the kernel).
long futex_wait(std::atomic<int>* addr, int expected) {
    return syscall(SYS_futex, reinterpret_cast<int*>(addr), FUTEX_WAIT_PRIVATE, expected,
                   nullptr /*timeout*/, nullptr, 0);
}
// Wakes up to n threads sleeping on addr; returns how many were woken.
long futex_wake(std::atomic<int>* addr, int n) {
    return syscall(SYS_futex, reinterpret_cast<int*>(addr), FUTEX_WAKE_PRIVATE, n, nullptr, nullptr, 0);
}
```

### 10.4 Python Solution (spinlock on top of a non-blocking acquire)

Python exposes no CAS, but `Lock.acquire(blocking=False)` is an atomic test-and-set, and `Lock.locked()` is a cheap read -- enough to express TTAS with backoff. The benchmark shows why you should not do this in CPython: a spinning thread holds the GIL, so the lock holder cannot run until the spinner's switch interval expires or it sleeps.

```python
# spinlock.py
import threading
import time


class SpinLock:
    """TTAS + exponential backoff. acquire(blocking=False) plays the role of test-and-set."""

    def __init__(self) -> None:
        self._flag = threading.Lock()

    def acquire(self) -> None:
        backoff = 1e-6
        while not self._flag.acquire(blocking=False):   # test-and-set
            while self._flag.locked():                   # test (read-only)
                time.sleep(backoff)                      # sleeping releases the GIL
                backoff = min(backoff * 2, 1e-3)

    def release(self) -> None:
        self._flag.release()

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, *exc) -> None:
        self.release()


def bench(lock, threads: int = 4, iters: int = 20000) -> None:
    counter = 0

    def work() -> None:
        nonlocal counter
        for _ in range(iters):
            with lock:
                counter += 1          # read-modify-write: needs the lock even with a GIL

    ts = [threading.Thread(target=work) for _ in range(threads)]
    t0 = time.perf_counter()
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    ms = (time.perf_counter() - t0) * 1e3
    assert counter == threads * iters
    print(f"{type(lock).__name__:10} counter={counter} OK {ms:8.1f} ms")


if __name__ == "__main__":
    bench(SpinLock())
    bench(threading.Lock())
```

### 10.5 Correctness and Complexity

- **TAS/TTAS mutual exclusion:** `test_and_set`/`exchange` is an atomic RMW; exactly one thread observes the transition `false -> true`. The relaxed pre-check in TTAS is only a hint; correctness rests on the `exchange`.
- **Ticket lock:** `fetch_add` hands out unique, increasing tickets; only the thread whose ticket equals `serving_` proceeds, and `unlock` advances `serving_` by one, so entry order equals ticket order (FIFO, no starvation). 32-bit wraparound is harmless as long as fewer than 2^32 threads wait at once.
- **Futex mutex:** state `0 -> 1` by the fast path means "locked, nobody sleeping". Any thread that fails the fast path sets the state to `2` before sleeping, so the holder's `fetch_sub` returns 2 and it knows to wake someone. A woken thread sets `2` again (it cannot know if others still sleep) -- this costs at most one unnecessary wake later, never a lost one. `wait(2)` returns immediately if the state already changed, closing the check-then-sleep window.
- **Cost:** uncontended futex lock/unlock is one atomic RMW each (~10-20 ns); a contended hand-off costs a syscall plus a context switch (~2-10 us). Spinlocks hand off in ~100 ns when the waiter is running on another core, but waste a core while waiting.

### 10.6 Pitfalls

- **`volatile bool` or a plain `bool` as the lock flag** is a data race (undefined behavior) and gives no atomicity.
- **Spinning with `seq_cst` RMWs in the wait loop** (pure TAS) creates a coherence storm; benchmark TAS vs TTAS with 16+ threads to see a large gap.
- **Ticket locks under oversubscription:** if the next ticket holder is preempted, *everyone* waits for it to be rescheduled (convoy). FIFO fairness has a throughput price.
- **The unlock/destroy race in the futex mutex:** after `state_.store(0)`, another thread may lock, unlock, and destroy the mutex before our `notify_one` runs on its address. The kernel tolerates `FUTEX_WAKE` on stale memory, but in strict C++ it is a use-after-free; glibc's real mutexes are designed so that the last access to the lock word is the atomic RMW itself.
- **Priority inversion:** a low-priority holder preempted by a medium-priority thread blocks a high-priority waiter indefinitely. Fix with priority inheritance (`PTHREAD_PRIO_INHERIT`, which uses `FUTEX_LOCK_PI`) or by avoiding locks across priority levels.

### 10.7 Interview Questions

**Q1. Why is TTAS faster than TAS under contention, at the cache-coherence level?**

Under MESI, an atomic RMW requires exclusive ownership of the cache line, so N TAS spinners continuously steal the line from each other (and from the holder, who needs it to unlock), generating a flood of invalidations and read-for-ownership requests on the interconnect. In TTAS, spinners read the line, get it in Shared state, and then spin on their own L1 copy without bus traffic. When the holder releases, the line is invalidated once, everyone re-reads it, and they race on one `exchange`. Backoff further spreads out that race so most losers do not immediately retry.

**Q2. How does `pthread_mutex_lock` avoid a system call in the common case?**

The mutex is an integer in user memory. Locking does a CAS from 0 to 1; if it succeeds, there was no contention and no kernel involvement. Only if the CAS fails does the thread mark the lock as contended and call `futex(FUTEX_WAIT)`. Unlocking does an atomic decrement/exchange and only calls `futex(FUTEX_WAKE)` if the old value said there were waiters. So an uncontended lock/unlock pair is two atomic instructions -- this is why "use a mutex" is usually cheaper than people expect.

**Q3. When would you actually use a spinlock in user space?**

When the critical section is a few dozen instructions, threads are pinned with at most one thread per core (no oversubscription), and wake-up latency matters more than CPU usage -- for example, a real-time audio thread, a DPDK-style polling data plane, or a GPU-runtime submission path. Even then, prefer an adaptive lock (spin for ~1 us, then park on a futex). In the kernel, spinlocks are standard because preemption and interrupts can be disabled while holding them.

---

## 11. Thread-Safe LRU Cache

### 11.1 Problem

Implement an LRU cache with `get(key)` and `put(key, value)` in O(1), safe for concurrent use by many threads. Follow-ups: reduce contention; avoid computing the same missing value many times concurrently ("cache stampede"); explain why a reader-writer lock does not help.

### 11.2 Approach

Single-threaded core: a doubly linked list ordered by recency (front = most recent) plus a hash map from key to list node. `get` moves the node to the front (`std::list::splice` is O(1) and keeps iterators valid); `put` inserts at the front and evicts from the back when over capacity.

Concurrency options:

| Design | Get path | Scalability | Exactness |
|---|---|---|---|
| One mutex around everything | lock, lookup, splice | Serializes all ops; fine to ~1-5 M ops/s | Exact global LRU |
| RW lock | `get` still mutates the list -> must take the **write** lock | No better than a mutex | Exact |
| **Sharded** (N independent LRUs, shard = hash(key) % N) | lock one shard | ~N times less contention | Approximate: LRU per shard, total capacity split across shards |
| CLOCK / second-chance with atomic reference bits | lookup + relaxed store of a bit (no list mutation) | Reads nearly contention-free | Approximates LRU |
| Buffered recency (Caffeine-style) | record access in a per-thread buffer, apply in batches under the lock | Very high | Approximate |

The key insight interviewers look for: **`get` is a write** in an LRU, so "use a shared lock for reads" is wrong.

### 11.3 C++20 Solution (mutex-protected LRU + sharded wrapper)

```cpp
// lru_cache.cpp -- g++ -std=c++20 -O2 -pthread lru_cache.cpp
#include <atomic>
#include <cstdio>
#include <functional>
#include <list>
#include <memory>
#include <mutex>
#include <optional>
#include <random>
#include <thread>
#include <unordered_map>
#include <utility>
#include <vector>

template <class K, class V>
class LRUCache {
public:
    explicit LRUCache(std::size_t capacity) : capacity_(capacity) {}

    std::optional<V> get(const K& key) {
        std::lock_guard g(m_);
        auto it = index_.find(key);
        if (it == index_.end()) return std::nullopt;
        items_.splice(items_.begin(), items_, it->second);   // O(1) move-to-front
        return it->second->second;                           // copy out while still locked
    }

    void put(const K& key, V value) {
        std::lock_guard g(m_);
        if (capacity_ == 0) return;
        if (auto it = index_.find(key); it != index_.end()) {
            it->second->second = std::move(value);
            items_.splice(items_.begin(), items_, it->second);
            return;
        }
        if (items_.size() == capacity_) {                    // evict least recently used
            index_.erase(items_.back().first);
            items_.pop_back();
        }
        items_.emplace_front(key, std::move(value));
        index_.emplace(key, items_.begin());
    }

    std::size_t size() const {
        std::lock_guard g(m_);
        return index_.size();
    }

private:
    using Node = std::pair<K, V>;
    mutable std::mutex m_;
    std::list<Node> items_;                                          // front = most recent
    std::unordered_map<K, typename std::list<Node>::iterator> index_;
    const std::size_t capacity_;
};

// N independent LRUs; a key always maps to the same shard, so per-key semantics are preserved.
template <class K, class V>
class ShardedLRUCache {
public:
    ShardedLRUCache(std::size_t capacity, std::size_t shards) {
        const std::size_t per = (capacity + shards - 1) / shards;
        for (std::size_t i = 0; i < shards; ++i) shards_.push_back(std::make_unique<LRUCache<K, V>>(per));
    }
    std::optional<V> get(const K& key) { return shard(key).get(key); }
    void put(const K& key, V value) { shard(key).put(key, std::move(value)); }
    std::size_t size() const {
        std::size_t s = 0;
        for (auto& sh : shards_) s += sh->size();
        return s;
    }

private:
    LRUCache<K, V>& shard(const K& key) {
        // Mix the hash: std::hash<int> is the identity on libstdc++, so low bits alone are poor.
        std::size_t h = std::hash<K>{}(key) * 0x9E3779B97F4A7C15ull;
        return *shards_[(h >> 32) % shards_.size()];
    }
    std::vector<std::unique_ptr<LRUCache<K, V>>> shards_;   // LRUCache holds a mutex: not movable
};

int main() {
    // Semantics check (single-threaded): classic LeetCode 146 sequence.
    LRUCache<int, int> c(2);
    c.put(1, 1); c.put(2, 2);
    bool ok = c.get(1) == 1;          // 1 becomes most recent
    c.put(3, 3);                      // evicts 2
    ok &= !c.get(2).has_value();
    c.put(4, 4);                      // evicts 1
    ok &= !c.get(1).has_value() && c.get(3) == 3 && c.get(4) == 4;
    std::printf("LRU semantics: %s\n", ok ? "OK" : "FAIL");

    // Concurrency check: values are always key*10; the cache must never return anything else.
    ShardedLRUCache<int, long> cache(1000, 16);
    std::atomic<long> hits{0}, misses{0};
    std::atomic<bool> bad{false};
    std::vector<std::thread> ts;
    for (int t = 0; t < 8; ++t)
        ts.emplace_back([&, t] {
            std::mt19937 rng(t);
            std::uniform_int_distribution<int> key(0, 3000);
            for (int i = 0; i < 100000; ++i) {
                int k = key(rng);
                if (auto v = cache.get(k)) {
                    ++hits;
                    if (*v != k * 10L) bad = true;
                } else {
                    ++misses;
                    cache.put(k, k * 10L);
                }
            }
        });
    for (auto& t : ts) t.join();
    std::printf("hits=%ld misses=%ld size=%zu (<= 1008) %s\n", hits.load(), misses.load(),
                cache.size(), !bad && cache.size() <= 1008 ? "OK" : "FAIL");
}
```

### 11.4 Python Solution (with single-flight `get_or_compute`)

```python
# lru_cache.py
import threading
import time
from collections import OrderedDict
from concurrent.futures import Future


class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self._data: OrderedDict = OrderedDict()   # last = most recently used
        self._lock = threading.Lock()
        self._inflight: dict = {}                 # key -> Future for single-flight loads

    def get(self, key, default=None):
        with self._lock:
            if key not in self._data:
                return default
            self._data.move_to_end(key)
            return self._data[key]

    def put(self, key, value) -> None:
        with self._lock:
            self._put_locked(key, value)

    def _put_locked(self, key, value) -> None:
        self._data[key] = value
        self._data.move_to_end(key)
        if len(self._data) > self.capacity:
            self._data.popitem(last=False)        # evict least recently used

    def get_or_compute(self, key, compute):
        """Only one thread computes a missing key; concurrent callers wait for its result."""
        with self._lock:
            if key in self._data:
                self._data.move_to_end(key)
                return self._data[key]
            fut = self._inflight.get(key)
            owner = fut is None
            if owner:
                fut = self._inflight[key] = Future()
        if not owner:
            return fut.result()                   # wait outside the lock
        try:
            value = compute(key)                  # slow work outside the lock
        except BaseException as exc:
            with self._lock:
                del self._inflight[key]
            fut.set_exception(exc)
            raise
        with self._lock:
            self._put_locked(key, value)
            del self._inflight[key]
        fut.set_result(value)
        return value


def main() -> None:
    c = LRUCache(2)
    c.put(1, 1); c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)                                   # evicts 2
    assert c.get(2) is None and c.get(3) == 3
    print("LRU semantics OK")

    calls = 0
    calls_lock = threading.Lock()

    def slow_square(k: int) -> int:
        nonlocal calls
        with calls_lock:
            calls += 1
        time.sleep(0.05)                          # e.g. a database query
        return k * k

    cache = LRUCache(100)
    results = []
    ts = [threading.Thread(target=lambda: results.append(cache.get_or_compute(7, slow_square)))
          for _ in range(16)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    assert results == [49] * 16 and calls == 1, (results, calls)
    print(f"16 concurrent misses -> compute called {calls} time(s) OK")


if __name__ == "__main__":
    main()
```

`functools.lru_cache` is also thread-safe in the sense that its internal structure stays consistent, but the documentation notes that the wrapped function may be called more than once for the same arguments if another thread calls before the first call has finished and been cached -- it does not de-duplicate concurrent misses. That is what `get_or_compute` adds.

### 11.5 Correctness and Complexity

- **Linearizability:** every operation runs entirely under one mutex (per shard), so each operation appears to take effect atomically at some point between its call and return.
- **Sharding preserves per-key semantics:** a key always hashes to the same shard, so a `put` followed by a `get` of the same key sees the value. What changes is *which* key gets evicted: eviction is LRU within the shard, and the global capacity is `shards * ceil(capacity / shards)`.
- **Single-flight:** the first miss registers a `Future` under the lock; later callers find it under the same lock and wait on it, so `compute` runs once per key per miss window. Errors propagate to all waiters and the in-flight entry is removed so the next call retries.
- **Cost:** O(1) average per operation; hash-map rehash is O(n) occasionally (reserve up front in C++). Memory: one list node + one hash entry per item (~80-100 bytes overhead per entry in C++ with `std::list`).

### 11.6 Pitfalls

- **Returning a reference or pointer to the cached value** from `get`: another thread may evict or overwrite it as soon as the lock is released. Return a copy, or store `std::shared_ptr<const V>` and return that.
- **Calling user code (the loader) while holding the cache lock** serializes all misses behind one slow load and risks deadlock if the loader touches the cache. Load outside the lock (single-flight as above).
- **Using `std::shared_mutex` for `get`:** data race on the recency list -- TSan will catch it.
- **Unbounded `_inflight` growth** if a compute never finishes: add timeouts.

### 11.7 Interview Questions

**Q1. Your mutex-protected LRU is the top lock in a profile at 64 threads. What do you do?**

First confirm the critical section is minimal (no allocation or value copies of large objects under the lock -- use `shared_ptr` values). Then shard by key hash (e.g. 64-256 shards) to cut contention roughly by the shard count. If reads dominate, switch the eviction policy to CLOCK so a hit only sets an atomic "referenced" bit without touching shared list pointers, or buffer recency updates per thread and apply them in batches (try-lock; drop updates if the buffer is full -- recency is a heuristic). Measure hit rate before and after, because approximate LRU can change it.

**Q2. How do you prevent a cache stampede when a hot key expires?**

Single-flight (one loader per key; others wait on its future), plus either serving the stale value while one thread refreshes in the background (stale-while-revalidate), or probabilistic early expiration (each reader refreshes slightly before TTL with a probability that grows as expiry approaches), so the refresh does not happen at one instant for every caller. See also [High Level Design: caching](High_Level_Design.md).

---

## 12. Thread-Safe Token-Bucket Rate Limiter

### 12.1 Problem

Implement a rate limiter that allows on average `rate` requests per second with bursts of up to `burst` requests. It must be thread-safe, provide a non-blocking `try_acquire()` and a blocking `acquire()`, and be testable without real sleeps. Follow-up: make it lock-free.

### 12.2 Approach

**Token bucket with lazy refill:** store `tokens` (a double) and `last` (time of last refill). On every call, refill `tokens = min(burst, tokens + (now - last) * rate)`, set `last = now`, then take a token if available. No background thread is needed -- refill is computed on demand in O(1).

**Blocking acquire:** compute the wait time `(n - tokens) / rate` **under** the lock, **sleep without** the lock, then retry (another thread may have taken the token meanwhile).

**Lock-free variant -- GCRA (Generic Cell Rate Algorithm):** keep a single 64-bit "theoretical arrival time" (TAT). Emission interval `T = 1 / rate`, tolerance `tau = burst * T`. A request at time `now` is allowed iff `max(TAT, now) + T - now <= tau`; if allowed, `TAT = max(TAT, now) + T`. One word of state means one CAS loop -- no mutex. GCRA admits exactly the same traffic as a token bucket with the same rate and burst.

Worked example (rate 10/s, burst 5, so `T = 100 ms`, `tau = 500 ms`): at `t = 0`, five requests pass (TAT goes 100, 200, ..., 500 ms) and the sixth fails (`600 - 0 > 500`). At `t = 100 ms`, one passes (`600 - 100 = 500 <= 500`). At `t = 1 s`, the bucket is full again and 5 pass.

### 12.3 C++20 Solution (token bucket + lock-free GCRA, injectable time)

```cpp
// rate_limiter.cpp -- g++ -std=c++20 -O2 -pthread rate_limiter.cpp
#include <algorithm>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <mutex>
#include <stdexcept>
#include <thread>
#include <type_traits>
#include <vector>

using Clock = std::chrono::steady_clock;
using Nanos = std::chrono::nanoseconds;

class TokenBucket {
public:
    TokenBucket(double ratePerSec, double burst, Clock::time_point start = Clock::now())
        : rate_(ratePerSec), burst_(burst), tokens_(burst), last_(start) {}

    // `now` is a parameter so tests can drive time deterministically.
    bool try_acquire(double n = 1.0, Clock::time_point now = Clock::now()) {
        std::lock_guard g(m_);
        refillLocked(now);
        if (tokens_ < n) return false;
        tokens_ -= n;
        return true;
    }

    void acquire(double n = 1.0) {
        if (n > burst_) throw std::invalid_argument("request larger than burst can never succeed");
        for (;;) {
            std::chrono::duration<double> wait;
            {
                std::lock_guard g(m_);
                refillLocked(Clock::now());
                if (tokens_ >= n) { tokens_ -= n; return; }
                wait = std::chrono::duration<double>((n - tokens_) / rate_);
            }
            std::this_thread::sleep_for(wait);   // never sleep while holding the lock
        }
    }

private:
    void refillLocked(Clock::time_point now) {
        // `now` was read before taking the lock, so another thread may already have refilled
        // with a later timestamp: never move time backwards.
        if (now <= last_) return;
        const double elapsed = std::chrono::duration<double>(now - last_).count();
        tokens_ = std::min(burst_, tokens_ + elapsed * rate_);
        last_ = now;
    }

    std::mutex m_;
    const double rate_, burst_;
    double tokens_;
    Clock::time_point last_;
};

// Lock-free GCRA: the whole state is one atomic 64-bit "theoretical arrival time".
class GcraLimiter {
public:
    GcraLimiter(double ratePerSec, double burst)
        : interval_(static_cast<std::int64_t>(1e9 / ratePerSec)),
          tolerance_(static_cast<std::int64_t>(burst * 1e9 / ratePerSec)) {}

    bool try_acquire(std::int64_t nowNs) {
        std::int64_t tat = tat_.load(std::memory_order_relaxed);
        for (;;) {
            const std::int64_t newTat = std::max(tat, nowNs) + interval_;
            if (newTat - nowNs > tolerance_) return false;            // would exceed the burst
            if (tat_.compare_exchange_weak(tat, newTat, std::memory_order_relaxed)) return true;
            // CAS failed: `tat` now holds the current value; recompute and retry.
        }
    }
    bool try_acquire() {
        return try_acquire(std::chrono::duration_cast<Nanos>(Clock::now().time_since_epoch()).count());
    }

private:
    const std::int64_t interval_, tolerance_;
    std::atomic<std::int64_t> tat_{0};
};

int main() {
    using namespace std::chrono_literals;
    // 1. Deterministic tests with a fake clock: rate 10/s, burst 5.
    const Clock::time_point t0{};   // fake epoch
    TokenBucket tb(10, 5, t0);
    GcraLimiter gc(10, 5);
    auto ns = [&](Clock::time_point t) { return std::chrono::duration_cast<Nanos>(t - t0).count(); };
    auto countAllowed = [&](Clock::time_point t, int attempts, auto& lim) {
        int ok = 0;
        for (int i = 0; i < attempts; ++i) {
            if constexpr (std::is_same_v<std::decay_t<decltype(lim)>, TokenBucket>) ok += lim.try_acquire(1.0, t);
            else ok += lim.try_acquire(ns(t));
        }
        return ok;
    };
    for (int pass = 0; pass < 2; ++pass) {
        int a, b, c;
        if (pass == 0) { a = countAllowed(t0, 8, tb); b = countAllowed(t0 + 100ms, 3, tb); c = countAllowed(t0 + 1s, 8, tb); }
        else           { a = countAllowed(t0, 8, gc); b = countAllowed(t0 + 100ms, 3, gc); c = countAllowed(t0 + 1s, 8, gc); }
        std::printf("%s: t=0 -> %d/8, t=100ms -> %d/3, t=1s -> %d/8 %s\n", pass ? "GCRA        " : "token bucket",
                    a, b, c, a == 5 && b == 1 && c == 5 ? "OK" : "FAIL");
    }

    // 2. Real clock, 8 threads hammering: allowed <= burst + rate * elapsed.
    const auto start = Clock::now();
    TokenBucket live(1000, 50, start);
    std::atomic<long> allowed{0};
    std::vector<std::thread> ts;
    for (int i = 0; i < 8; ++i)
        ts.emplace_back([&] {
            while (Clock::now() - start < 200ms) allowed += live.try_acquire();
        });
    for (auto& t : ts) t.join();
    const double elapsed = std::chrono::duration<double>(Clock::now() - start).count();
    const double bound = 50 + 1000 * elapsed;
    std::printf("live: allowed=%ld in %.3fs, upper bound %.0f %s\n", allowed.load(), elapsed, bound,
                allowed <= bound + 1 ? "OK" : "FAIL");

    // 3. Blocking acquire: 20 tokens at 100/s with burst 1 takes about 190 ms.
    TokenBucket slow(100, 1);
    const auto s0 = Clock::now();
    std::vector<std::thread> ws;
    for (int i = 0; i < 4; ++i) ws.emplace_back([&] { for (int k = 0; k < 5; ++k) slow.acquire(); });
    for (auto& t : ws) t.join();
    const double took = std::chrono::duration<double>(Clock::now() - s0).count();
    std::printf("blocking: 20 acquires took %.3fs (>= 0.19) %s\n", took, took >= 0.185 ? "OK" : "FAIL");
}
```

### 12.4 Python Solution (injectable clock, blocking acquire)

```python
# rate_limiter.py
import threading
import time


class TokenBucket:
    def __init__(self, rate: float, burst: float, clock=time.monotonic) -> None:
        self.rate, self.burst, self.clock = rate, burst, clock
        self._tokens = burst
        self._last = clock()
        self._lock = threading.Lock()

    def _refill_locked(self, now: float) -> None:
        if now > self._last:
            self._tokens = min(self.burst, self._tokens + (now - self._last) * self.rate)
            self._last = now

    def try_acquire(self, n: float = 1.0) -> bool:
        with self._lock:
            self._refill_locked(self.clock())
            if self._tokens >= n:
                self._tokens -= n
                return True
            return False

    def acquire(self, n: float = 1.0) -> None:
        if n > self.burst:
            raise ValueError("request larger than burst can never succeed")
        while True:
            with self._lock:
                self._refill_locked(self.clock())
                if self._tokens >= n:
                    self._tokens -= n
                    return
                wait = (n - self._tokens) / self.rate
            time.sleep(wait)                     # outside the lock


class FakeClock:
    def __init__(self) -> None:
        self.t = 0.0

    def __call__(self) -> float:
        return self.t


if __name__ == "__main__":
    clk = FakeClock()
    tb = TokenBucket(rate=10, burst=5, clock=clk)
    a = sum(tb.try_acquire() for _ in range(8))
    clk.t = 0.1
    b = sum(tb.try_acquire() for _ in range(3))
    clk.t = 1.0
    c = sum(tb.try_acquire() for _ in range(8))
    assert (a, b, c) == (5, 1, 5), (a, b, c)
    print(f"fake clock: {a}/8, {b}/3, {c}/8 OK")

    slow = TokenBucket(rate=100, burst=1)
    t0 = time.monotonic()
    ts = [threading.Thread(target=lambda: [slow.acquire() for _ in range(5)]) for _ in range(4)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    took = time.monotonic() - t0
    assert took >= 0.185, took
    print(f"blocking: 20 acquires in {took:.3f}s OK")
```

For asyncio code, the same class works with `asyncio.Lock` and `await asyncio.sleep(wait)` -- never call `time.sleep` inside a coroutine (it blocks the whole event loop).

### 12.5 Correctness and Complexity

- **Rate bound:** tokens are created only by refill at `rate` per second and capped at `burst`, so over any interval of length `t` at most `burst + rate * t` requests succeed -- the property the live test asserts.
- **Thread safety:** refill and take happen in the same critical section (check-then-act is atomic). Out-of-order timestamps are ignored rather than producing negative refill.
- **GCRA lock-freedom:** each CAS failure means another thread's CAS succeeded, so the system as a whole always makes progress (lock-free, though not wait-free).
- **Cost:** O(1) per call, no background thread, 2-3 words of state per limiter -- which is why per-user limiters can be kept in a hash map (or in Redis with a Lua script for a distributed limiter).

### 12.6 Pitfalls

- **Using the wall clock** (`system_clock`, `time.time()`) -- NTP adjustments can move it backwards or jump forward. Use `steady_clock` / `time.monotonic()`.
- **Sleeping while holding the lock** in `acquire`: every other caller, including `try_acquire`, stalls.
- **Integer token counts with integer-millisecond refill** lose fractional tokens at low rates (e.g. 0.5 req/s never refills); use doubles or keep time in nanoseconds.
- **Thundering herd after a long sleep**: many blocked threads wake at the same instant and contend; with a FIFO requirement, use a ticketed queue or reserve future tokens ("wait until your reserved slot") instead of retrying.

### 12.7 Interview Questions

**Q1. Token bucket vs leaky bucket vs sliding window -- which and why?**

Token bucket allows bursts up to `burst` and enforces an average rate; it is the usual API rate-limit choice. A leaky bucket (as a queue) smooths output to a constant rate -- good for shaping traffic to a downstream that cannot absorb bursts. A sliding-window log is exact ("at most N in any 60 s window") but stores a timestamp per request; the sliding-window counter approximates it with two counters. GCRA is a token bucket in one word of state, ideal for lock-free or Redis implementations. See [Low Level Design: Rate Limiter](../design-patterns/Low_Level_Design_Interview_Prep.md#10-worked-design-rate-limiter).

**Q2. How do you rate limit across 20 servers?**

Either centralize the state (Redis `INCR`/`EXPIRE` for fixed windows, or a Lua script implementing GCRA atomically per key -- one round trip per request), or give each server a local bucket with `rate / 20` and accept imprecision when load is uneven, or periodically rebalance local quotas from a coordinator. Mention failure mode: if Redis is down, fail open (allow) or fail closed (deny) depending on whether the limiter protects revenue or protects the backend.

---

## 13. Thread Pool with Futures

### 13.1 Problem

Implement a fixed-size thread pool: `submit(f, args...)` returns a future for the result (or the exception), workers pull tasks from a shared queue, and shutdown finishes queued work and joins all threads. Follow-ups: why can a pool deadlock, how to size it, and how work stealing helps.

### 13.2 Approach

- **Task queue:** a `std::queue<std::function<void()>>` guarded by a mutex and a condition variable (a blocking queue, Section 8, without a capacity bound).
- **Futures:** wrap the callable in a `std::packaged_task<R()>`; its `get_future()` is returned to the caller. `packaged_task` is move-only but `std::function` requires a copyable callable, so hold it in a `std::shared_ptr` (C++23's `std::move_only_function` removes this workaround).
- **Exceptions:** `packaged_task` catches anything the task throws and stores it in the shared state; `future.get()` rethrows it in the caller's thread. Workers never die from a task exception.
- **Shutdown:** set `stopping = true` under the lock, `notify_all`, join. Workers exit only when `stopping && queue.empty()`, so queued work is drained first.

### 13.3 C++20 Solution

```cpp
// thread_pool.cpp -- g++ -std=c++20 -O2 -pthread thread_pool.cpp
#include <algorithm>
#include <atomic>
#include <chrono>
#include <condition_variable>
#include <cstdio>
#include <functional>
#include <future>
#include <memory>
#include <mutex>
#include <queue>
#include <stdexcept>
#include <thread>
#include <type_traits>
#include <vector>

class ThreadPool {
public:
    explicit ThreadPool(std::size_t n = std::max(1u, std::thread::hardware_concurrency())) {
        workers_.reserve(n);
        for (std::size_t i = 0; i < n; ++i) workers_.emplace_back([this] { workerLoop(); });
    }
    ~ThreadPool() { shutdown(); }
    ThreadPool(const ThreadPool&) = delete;
    ThreadPool& operator=(const ThreadPool&) = delete;

    template <class F, class... Args>
    auto submit(F&& f, Args&&... args) {
        using R = std::invoke_result_t<std::decay_t<F>, std::decay_t<Args>...>;
        auto task = std::make_shared<std::packaged_task<R()>>(
            [fn = std::forward<F>(f), ... as = std::forward<Args>(args)]() mutable {
                return std::invoke(std::move(fn), std::move(as)...);
            });
        std::future<R> result = task->get_future();
        {
            std::lock_guard g(m_);
            if (stopping_) throw std::runtime_error("submit() on a stopped ThreadPool");
            tasks_.emplace([task] { (*task)(); });
        }
        cv_.notify_one();
        return result;
    }

    // Runs all already-queued tasks, then joins the workers. Idempotent.
    // Must not be called from inside a task (a worker cannot join itself).
    void shutdown() {
        {
            std::lock_guard g(m_);
            stopping_ = true;
        }
        cv_.notify_all();
        for (auto& w : workers_)
            if (w.joinable()) w.join();
    }

private:
    void workerLoop() {
        for (;;) {
            std::function<void()> task;
            {
                std::unique_lock lk(m_);
                cv_.wait(lk, [this] { return stopping_ || !tasks_.empty(); });
                if (tasks_.empty()) return;          // stopping_ and fully drained
                task = std::move(tasks_.front());
                tasks_.pop();
            }
            task();                                  // run WITHOUT the lock
        }
    }

    std::mutex m_;
    std::condition_variable cv_;
    std::queue<std::function<void()>> tasks_;
    bool stopping_ = false;
    std::vector<std::thread> workers_;               // declared last: threads start after members exist
};

int main() {
    using namespace std::chrono_literals;
    ThreadPool pool(4);

    // 1. Results through futures.
    std::vector<std::future<long>> futs;
    for (long i = 1; i <= 100; ++i) futs.push_back(pool.submit([](long x) { return x * x; }, i));
    long sum = 0;
    for (auto& f : futs) sum += f.get();
    std::printf("sum of squares 1..100 = %ld (%s)\n", sum, sum == 338350 ? "OK" : "FAIL");

    // 2. Exceptions propagate to the caller; the worker survives.
    auto bad = pool.submit([] { throw std::runtime_error("task failed"); return 0; });
    try {
        bad.get();
    } catch (const std::exception& e) {
        std::printf("caught from future: %s\n", e.what());
    }

    // 3. Parallelism: 8 tasks x 50 ms on 4 workers -> about 100 ms, not 400 ms.
    auto t0 = std::chrono::steady_clock::now();
    std::vector<std::future<void>> sleeps;
    for (int i = 0; i < 8; ++i) sleeps.push_back(pool.submit([] { std::this_thread::sleep_for(50ms); }));
    for (auto& f : sleeps) f.get();
    auto ms = std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
    std::printf("8 x 50ms tasks on 4 workers took %.0f ms (%s)\n", ms, ms < 300 ? "OK" : "SLOW");

    // 4. Shutdown drains the queue: tasks submitted before shutdown() still run.
    std::atomic<int> ran{0};
    for (int i = 0; i < 1000; ++i) pool.submit([&] { ++ran; });
    pool.shutdown();
    std::printf("ran %d/1000 queued tasks before shutdown completed (%s)\n", ran.load(),
                ran == 1000 ? "OK" : "FAIL");
}
```

### 13.4 Python Solution (pool built on `queue.SimpleQueue` and `concurrent.futures.Future`)

```python
# thread_pool.py
import queue
import threading
import time
from concurrent.futures import Future, as_completed


class ThreadPool:
    def __init__(self, workers: int) -> None:
        self._tasks: queue.SimpleQueue = queue.SimpleQueue()
        self._lock = threading.Lock()
        self._shutdown = False
        self._threads = [threading.Thread(target=self._worker, daemon=True) for _ in range(workers)]
        for t in self._threads:
            t.start()

    def submit(self, fn, /, *args, **kwargs) -> Future:
        fut: Future = Future()
        with self._lock:                       # makes "check shutdown + enqueue" atomic
            if self._shutdown:
                raise RuntimeError("submit() after shutdown()")
            self._tasks.put((fut, fn, args, kwargs))
        return fut

    def _worker(self) -> None:
        while True:
            item = self._tasks.get()
            if item is None:                   # poison pill
                return
            fut, fn, args, kwargs = item
            if not fut.set_running_or_notify_cancel():
                continue                       # cancelled while queued
            try:
                fut.set_result(fn(*args, **kwargs))
            except BaseException as exc:       # propagate to the caller via the future
                fut.set_exception(exc)

    def shutdown(self, wait: bool = True) -> None:
        with self._lock:
            if self._shutdown:
                return
            self._shutdown = True
            for _ in self._threads:            # FIFO: pills come after every queued task
                self._tasks.put(None)
        if wait:
            for t in self._threads:
                t.join()

    def __enter__(self):
        return self

    def __exit__(self, *exc) -> None:
        self.shutdown()


if __name__ == "__main__":
    with ThreadPool(4) as pool:
        futs = [pool.submit(lambda x: x * x, i) for i in range(1, 101)]
        assert sum(f.result() for f in as_completed(futs)) == 338350

        bad = pool.submit(lambda: 1 / 0)
        try:
            bad.result()
        except ZeroDivisionError as e:
            print("caught from future:", repr(e))

        t0 = time.perf_counter()
        for f in [pool.submit(time.sleep, 0.05) for _ in range(8)]:
            f.result()
        ms = (time.perf_counter() - t0) * 1e3
        print(f"8 x 50ms sleeps on 4 workers: {ms:.0f} ms")   # ~100 ms: sleep releases the GIL
    print("OK")
```

In real code use `concurrent.futures.ThreadPoolExecutor` (I/O-bound) or `ProcessPoolExecutor` (CPU-bound pure Python, because of the GIL); the class above follows the same basic design as `ThreadPoolExecutor`: a shared work queue of `_WorkItem` objects that each hold a future and the call to run, with a `None` sentinel for shutdown. The one difference is how shutdown wakes the workers. This pool enqueues one pill per worker. CPython's `shutdown()` enqueues a single `None`, and each worker that sees it re-enqueues `None` before exiting so the next idle worker wakes up too (see `_worker` in `concurrent/futures/thread.py`).

### 13.5 Correctness and Complexity

- **No lost tasks:** submit enqueues under the lock and notifies; a worker waits on `stopping || !empty`, so a task enqueued before the worker sleeps is seen by the predicate check, and one enqueued after triggers the notify.
- **Drain-then-exit:** a worker returns only when the queue is empty *and* stopping is set; tasks submitted before `shutdown()` therefore always run. Submissions after `shutdown()` are rejected under the same lock, so there is no window where a task is enqueued after the last worker exited.
- **Destruction order:** `workers_` is declared last so the threads start after the mutex/queue exist, and the destructor joins them before members are destroyed.
- **Cost:** one lock + one notify per submit and per dequeue; the single queue is the contention point at very high task rates (>1 M tasks/s). Work-stealing pools (per-worker deques; idle workers steal from the opposite end) remove most of that contention -- this is how TBB, Rayon, Go's scheduler, and Java's `ForkJoinPool` work.

### 13.6 Pitfalls

- **Pool-induced deadlock:** a task that `submit`s a subtask to the same pool and then blocks on its future. With all k workers doing this, every worker waits for a subtask that sits in the queue with no free worker to run it. Fixes: never block inside a pool task (use continuations), use a separate pool for the subtasks, or have a waiting worker run queued tasks while it waits ("help while waiting", as work-stealing schedulers do).
- **`std::async` is not a pool:** with `std::launch::async` it creates a new thread per call in libstdc++, and the future it returns blocks in its destructor -- a discarded `std::async(...)` result runs synchronously.
- **Sizing:** CPU-bound pools want about `cores` threads; I/O-bound pools want `cores * (1 + wait_time / compute_time)` (e.g. 8 cores, 90 ms waiting per 10 ms compute -> ~80 threads). Oversizing CPU-bound pools adds context switches and cache thrashing.
- **Long-running or blocking tasks starve short ones** in a FIFO pool; use separate pools per workload class (bulkheading).

### 13.7 Interview Questions

**Q1. How would you add task priorities and cancellation?**

Replace the FIFO queue with a `std::priority_queue` keyed by (priority, sequence number) -- the sequence number keeps FIFO order within a priority and avoids starvation only if you also add aging. For cancellation, give each task a shared `std::atomic<bool> cancelled` (or a C++20 `std::stop_token`): the worker checks it before running, and long tasks poll it cooperatively. Python's `Future.cancel()` works the same way: it succeeds only if the task has not started (`set_running_or_notify_cancel` returns false for cancelled futures).

**Q2. How does `std::jthread` simplify this pool?**

`std::jthread` joins automatically in its destructor and carries a `std::stop_source`. Workers can wait with `std::condition_variable_any::wait(lock, stop_token, predicate)`, which wakes when a stop is requested, so you do not need your own `stopping_` flag and `notify_all` for shutdown. Note that the default "request stop" semantics abandon queued tasks unless the loop drains explicitly.

---

## 14. Reusable Barrier

### 14.1 Problem

Implement a barrier for N threads: `arrive_and_wait()` blocks until all N threads have arrived, then releases all of them. The barrier must be **reusable** for repeated phases (iterative algorithms: compute, barrier, exchange, barrier, ...), and optionally run a completion function exactly once per phase.

### 14.2 Approach

A counter alone is not enough for reuse: a fast thread could leave phase k, arrive at phase k+1, and decrement the counter before slow threads from phase k have woken up. The fix is a **generation (phase) number**: each waiter remembers the generation it arrived in and waits until it changes. The last arriver resets the count, bumps the generation, and notifies all. Waiting for "generation changed" (not "count == 0") is also what makes spurious wakeups harmless.

For HPC-style busy-waiting there is the **sense-reversing barrier**: one atomic counter and one shared boolean "sense". Each arriving thread computes the sense value the barrier will flip to; the last arriver resets the counter and flips the sense; everyone else spins (or futex-waits) until the sense equals their expected value. The flip alternates, so consecutive phases cannot be confused.

### 14.3 C++20 Solution (generation barrier, sense-reversing barrier, and `std::barrier`)

```cpp
// barrier.cpp -- g++ -std=c++20 -O2 -pthread barrier.cpp
#include <atomic>
#include <barrier>
#include <condition_variable>
#include <cstdio>
#include <functional>
#include <mutex>
#include <thread>
#include <vector>

class CyclicBarrier {
public:
    explicit CyclicBarrier(int parties, std::function<void()> onPhaseComplete = {})
        : parties_(parties), onComplete_(std::move(onPhaseComplete)) {}

    void arrive_and_wait() {
        std::unique_lock lk(m_);
        const unsigned long myGeneration = generation_;
        if (++arrived_ == parties_) {
            if (onComplete_) onComplete_();   // exactly once per phase, before anyone is released
            arrived_ = 0;
            ++generation_;
            lk.unlock();
            cv_.notify_all();
            return;
        }
        cv_.wait(lk, [&] { return generation_ != myGeneration; });
    }

private:
    std::mutex m_;
    std::condition_variable cv_;
    const int parties_;
    int arrived_ = 0;
    unsigned long generation_ = 0;
    std::function<void()> onComplete_;
};

class SenseBarrier {
public:
    explicit SenseBarrier(int parties) : parties_(parties), remaining_(parties) {}

    void arrive_and_wait() {
        // The value `sense_` will have once this phase completes (it cannot flip before we arrive).
        const bool target = !sense_.load(std::memory_order_relaxed);
        if (remaining_.fetch_sub(1, std::memory_order_acq_rel) == 1) {
            remaining_.store(parties_, std::memory_order_relaxed);   // reset before releasing anyone
            sense_.store(target, std::memory_order_release);          // publish all phase writes
            sense_.notify_all();
        } else {
            // C++20 atomic wait: spins briefly, then sleeps on a futex while sense_ == !target.
            while (sense_.load(std::memory_order_acquire) != target)
                sense_.wait(!target, std::memory_order_acquire);
        }
    }

private:
    const int parties_;
    std::atomic<int> remaining_;
    std::atomic<bool> sense_{false};
};

// Each round: every thread writes its slot, barrier, every thread checks ALL slots, barrier.
// The second barrier stops a fast thread from overwriting its slot for round r+1 while a slow
// thread is still checking round r.
template <class Barrier>
bool exercise(const char* name, Barrier& barrier, int threads, int rounds) {
    std::vector<long> slots(threads, -1);   // plain longs: ordered only by the barrier
    std::atomic<bool> bad{false};
    std::vector<std::thread> ts;
    for (int t = 0; t < threads; ++t)
        ts.emplace_back([&, t] {
            for (int r = 0; r < rounds; ++r) {
                slots[t] = r * 1000L + t;
                barrier.arrive_and_wait();
                for (int i = 0; i < threads; ++i)
                    if (slots[i] != r * 1000L + i) bad = true;
                barrier.arrive_and_wait();
            }
        });
    for (auto& th : ts) th.join();
    std::printf("%-15s %d threads x %d rounds %s\n", name, threads, rounds, bad ? "FAIL" : "OK");
    return !bad;
}

int main() {
    const int threads = 6, rounds = 2000;
    int phases = 0;
    CyclicBarrier cyc(threads, [&] { ++phases; });   // completion runs under the barrier's lock
    SenseBarrier sense(threads);
    std::barrier<> stdb(threads);
    bool ok = exercise("CyclicBarrier", cyc, threads, rounds);
    ok &= exercise("SenseBarrier", sense, threads, rounds);
    ok &= exercise("std::barrier", stdb, threads, rounds);
    std::printf("completion function ran %d times (expected %d) %s\n", phases, 2 * rounds,
                phases == 2 * rounds ? "OK" : "FAIL");
    return ok && phases == 2 * rounds ? 0 : 1;
}
```

### 14.4 Python Solution

```python
# barrier.py
import threading


class CyclicBarrier:
    def __init__(self, parties: int, action=None) -> None:
        self.parties = parties
        self.action = action
        self._cv = threading.Condition()
        self._arrived = 0
        self._generation = 0

    def wait(self) -> None:
        with self._cv:
            gen = self._generation
            self._arrived += 1
            if self._arrived == self.parties:
                if self.action:
                    self.action()            # once per phase
                self._arrived = 0
                self._generation += 1
                self._cv.notify_all()
                return
            self._cv.wait_for(lambda: self._generation != gen)


def exercise(barrier_wait, threads: int = 5, rounds: int = 300) -> None:
    slots = [-1] * threads
    errors = []

    def run(t: int) -> None:
        for r in range(rounds):
            slots[t] = r * 1000 + t
            barrier_wait()
            if any(slots[i] != r * 1000 + i for i in range(threads)):
                errors.append((t, r))
            barrier_wait()

    ts = [threading.Thread(target=run, args=(t,)) for t in range(threads)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    assert not errors, errors[:3]


if __name__ == "__main__":
    phases = []
    mine = CyclicBarrier(5, action=lambda: phases.append(1))
    exercise(mine.wait)
    assert len(phases) == 2 * 300
    exercise(threading.Barrier(5).wait)
    print("CyclicBarrier and threading.Barrier OK; phases =", len(phases))
```

`threading.Barrier` adds what production code needs: `wait(timeout)`, `abort()`, and a **broken** state -- if any waiter times out or the action raises, every current and future waiter gets `BrokenBarrierError` instead of hanging.

### 14.5 Correctness and Complexity

- **Phase separation:** a waiter is released only when `generation` differs from the one it arrived in, which happens exactly when the N-th arrival of that phase occurs. A thread that races ahead into the next phase increments the *reset* counter of the new generation, so it cannot release anyone early.
- **Memory visibility:** everything a thread wrote before arriving happens-before everything any thread does after leaving: the mutex (or the release-store/acquire-load of `sense_` together with the acq_rel `fetch_sub` chain) provides the edges. That is why `slots` needs no atomics.
- **Cost:** the condition-variable barrier costs O(N) wakeups per phase through one mutex. A centralized sense barrier has all N threads hitting one cache line; at hundreds of threads, **tree or dissemination barriers** (O(log N) rounds, each thread spinning on its own flag) scale better -- this is what OpenMP and MPI runtimes use.

### 14.6 Pitfalls

- **Single-barrier reuse bug:** `count == 0` as the wait predicate, without a generation, fails on reuse (fast thread re-arrives before slow ones woke) or on spurious wakeups.
- **Barrier inside divergent control flow:** if one thread skips the barrier (an early `return`, an exception), all others wait forever. On GPUs the same bug is `__syncthreads()` inside a branch not taken by every thread of the block -- undefined behavior that typically hangs. See [Parallel GPU Programming: Block-Level Synchronization](../ml-gpu/Parallel_GPU_Programming.md#211-block-level-synchronization).
- **Number of participants must match exactly.** `std::barrier::arrive_and_drop()` lets a thread leave permanently (decrementing the expected count for later phases).
- **Completion function cost:** it runs while everyone waits; keep it short. `std::barrier` requires it to be `noexcept`.

### 14.7 Interview Questions

**Q1. `std::latch` vs `std::barrier`?**

A latch is a single-use countdown: `count_down()` from any threads (not necessarily the waiters), `wait()` until zero; it cannot be reset. Use it for "start all threads at once" or "wait until N initializations are done". A barrier is reusable across phases, the same set of threads arrives each time, and it can run a completion function per phase. Python has no latch; `threading.Barrier` or an `Event` plus a counter fill that role.

**Q2. How is a barrier used in GPU kernels and what is different there?**

`__syncthreads()` (HIP/CUDA) is a hardware-assisted barrier for all threads of one workgroup/block; it also acts as a memory fence for shared memory (LDS). There is no cheap barrier across *blocks* within a kernel launch because blocks are not guaranteed to be co-resident; grid-wide sync needs a cooperative launch (`grid.sync()`) or ending the kernel (a kernel boundary is the global barrier). A CPU barrier is the analog of a kernel boundary in a multi-phase algorithm such as the prefix sum in Section 17.

---

## 15. Web Crawler Multithreaded (LeetCode 1242)

### 15.1 Problem

Given `startUrl` and an `HtmlParser` whose `getUrls(url)` is a **blocking, slow** call returning the links on a page, return all URLs reachable from `startUrl` that have the **same hostname** as `startUrl`. URLs look like `http://hostname/path`, and each URL must be fetched at most once. The single-threaded BFS is too slow; use multiple threads.

### 15.2 Approach

Concurrent BFS over a graph whose edge lookups are slow I/O. Shared state: `seen` (hash set), `frontier` (queue). The hard part is **termination detection**: an empty frontier does *not* mean the crawl is finished, because another thread may be in the middle of `getUrls` and about to add new URLs. Track `inFlight` (URLs dequeued but not yet expanded); the crawl is over exactly when `frontier.empty() && inFlight == 0`.

Two standard designs:

| Design | Shared state | Termination | Notes |
|---|---|---|---|
| Fixed worker threads + shared queue (C++ below) | `seen`, `frontier`, `inFlight` under one mutex | Workers wait for `!frontier.empty() || inFlight == 0` | No per-URL thread creation; classic interview answer |
| Executor + futures, main thread owns `seen` (Python below) | None shared -- only the main thread touches `seen` | `while pending futures:` | Thread confinement: no locks at all for the crawl state |

### 15.3 C++20 Solution (worker threads + shared frontier)

```cpp
// web_crawler.cpp -- g++ -std=c++20 -O2 -pthread web_crawler.cpp
#include <algorithm>
#include <chrono>
#include <condition_variable>
#include <cstdio>
#include <deque>
#include <mutex>
#include <string>
#include <thread>
#include <unordered_map>
#include <unordered_set>
#include <vector>

std::string hostname(const std::string& url) {      // "http://host/path" -> "host"
    const auto start = url.find("//") + 2;
    const auto end = url.find('/', start);
    return url.substr(start, end == std::string::npos ? std::string::npos : end - start);
}

// Simulated LeetCode HtmlParser: thread-safe (read-only map) and slow (5 ms per call).
class HtmlParser {
public:
    explicit HtmlParser(std::unordered_map<std::string, std::vector<std::string>> g) : graph_(std::move(g)) {}
    std::vector<std::string> getUrls(const std::string& url) const {
        std::this_thread::sleep_for(std::chrono::milliseconds(5));
        auto it = graph_.find(url);
        return it == graph_.end() ? std::vector<std::string>{} : it->second;
    }
private:
    std::unordered_map<std::string, std::vector<std::string>> graph_;
};

std::vector<std::string> crawl(const std::string& startUrl, const HtmlParser& parser, int numThreads) {
    const std::string host = hostname(startUrl);
    std::mutex m;
    std::condition_variable cv;
    std::deque<std::string> frontier{startUrl};
    std::unordered_set<std::string> seen{startUrl};
    int inFlight = 0;                                 // dequeued but not yet expanded

    auto worker = [&] {
        for (;;) {
            std::string url;
            {
                std::unique_lock lk(m);
                cv.wait(lk, [&] { return !frontier.empty() || inFlight == 0; });
                if (frontier.empty()) return;          // inFlight == 0 too: nobody can add work
                url = std::move(frontier.front());
                frontier.pop_front();
                ++inFlight;
            }
            std::vector<std::string> links = parser.getUrls(url);   // slow I/O, no lock held
            std::erase_if(links, [&](const std::string& u) { return hostname(u) != host; });
            {
                std::lock_guard g(m);
                for (auto& u : links)
                    if (seen.insert(u).second) frontier.push_back(std::move(u));
                --inFlight;
            }
            cv.notify_all();                           // new work, or the termination condition
        }
    };

    std::vector<std::thread> threads;
    for (int i = 0; i < numThreads; ++i) threads.emplace_back(worker);
    for (auto& t : threads) t.join();
    return {seen.begin(), seen.end()};
}

int main() {
    // LeetCode example 1 plus a larger synthetic site.
    std::unordered_map<std::string, std::vector<std::string>> g = {
        {"http://news.yahoo.com/news/topics/", {"http://news.yahoo.com/news", "http://news.yahoo.com"}},
        {"http://news.yahoo.com/news", {"http://news.google.com"}},
        {"http://news.yahoo.com", {"http://news.yahoo.com/us"}},
        {"http://news.google.com", {"http://news.yahoo.com/us"}},
    };
    const int kPages = 120;
    for (int i = 0; i < kPages; ++i) {
        auto page = "http://site.example/p" + std::to_string(i);
        g[page] = {"http://site.example/p" + std::to_string((i * 7 + 1) % kPages),
                   "http://site.example/p" + std::to_string((i * 13 + 5) % kPages),
                   "http://other.example/x" + std::to_string(i)};   // different host: skipped
    }
    HtmlParser parser(g);

    auto r = crawl("http://news.yahoo.com/news/topics/", parser, 4);
    std::sort(r.begin(), r.end());
    for (auto& u : r) std::printf("  %s\n", u.c_str());

    for (int threads : {1, 8}) {
        auto t0 = std::chrono::steady_clock::now();
        auto pages = crawl("http://site.example/p0", parser, threads);
        auto ms = std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
        std::printf("threads=%d found %zu pages in %.0f ms\n", threads, pages.size(), ms);
    }
}
```

### 15.4 Python Solution (executor + futures; crawl state confined to the main thread)

```python
# web_crawler.py
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait


def hostname(url: str) -> str:
    return url.split("/")[2]          # "http://host/path" -> ["http:", "", "host", "path"]


class HtmlParser:
    def __init__(self, graph: dict[str, list[str]]) -> None:
        self.graph = graph

    def getUrls(self, url: str) -> list[str]:
        time.sleep(0.005)             # blocking I/O releases the GIL -> threads overlap
        return self.graph.get(url, [])


def crawl(start_url: str, parser: HtmlParser, workers: int = 8) -> list[str]:
    host = hostname(start_url)
    seen = {start_url}                # touched only by this (main) thread: no lock needed
    with ThreadPoolExecutor(max_workers=workers) as pool:
        pending = {pool.submit(parser.getUrls, start_url)}
        while pending:
            done, pending = wait(pending, return_when=FIRST_COMPLETED)
            for fut in done:
                for url in fut.result():
                    if url not in seen and hostname(url) == host:
                        seen.add(url)
                        pending.add(pool.submit(parser.getUrls, url))
    return sorted(seen)


if __name__ == "__main__":
    g = {
        "http://news.yahoo.com/news/topics/": ["http://news.yahoo.com/news", "http://news.yahoo.com"],
        "http://news.yahoo.com/news": ["http://news.google.com"],
        "http://news.yahoo.com": ["http://news.yahoo.com/us"],
        "http://news.google.com": ["http://news.yahoo.com/us"],
    }
    n = 120
    for i in range(n):
        g[f"http://site.example/p{i}"] = [f"http://site.example/p{(i * 7 + 1) % n}",
                                          f"http://site.example/p{(i * 13 + 5) % n}",
                                          f"http://other.example/x{i}"]
    parser = HtmlParser(g)
    print(crawl("http://news.yahoo.com/news/topics/", parser))
    for w in (1, 8):
        t0 = time.perf_counter()
        pages = crawl("http://site.example/p0", parser, workers=w)
        print(f"workers={w} found {len(pages)} pages in {(time.perf_counter() - t0) * 1e3:.0f} ms")
```

### 15.5 Correctness and Complexity

- **Each URL fetched once:** a URL is enqueued only by the thread whose `seen.insert` succeeded (C++), or only by the main thread after a membership check (Python).
- **Termination:** in C++, `inFlight` is incremented in the same critical section that removes a URL, and decremented in the same critical section that publishes its children. So `frontier.empty() && inFlight == 0` can only be observed when no URL is queued or being expanded -- no more work can ever appear. The final `notify_all` wakes every idle worker to observe it.
- **Speedup:** with V pages and latency L per fetch, sequential time is about V * L; with T threads it approaches max(V * L / T, depth * L), because BFS levels are a critical path (a page cannot be fetched before a page linking to it).
- **Cost:** O(V + E) total work; one mutex acquisition per dequeue and per expansion.

### 15.6 Pitfalls

- **Terminating when the queue is empty** (`if (frontier.empty()) return;` without `inFlight`) -- threads quit while others are still fetching, and pages go missing nondeterministically.
- **Holding the lock during `getUrls`** serializes the crawl, defeating the purpose.
- **Check-then-insert race:** `if (!seen.count(u)) { ...unlock...; seen.insert(u); }` lets two threads fetch the same page. Use the atomic result of `insert(...).second` under one lock.
- **Hostname parsing:** `http://news.yahoo.com` has no trailing slash; `find('/')` returns `npos` -- handle it (above). Ports and user-info are out of scope for LeetCode, but mention `urllib.parse.urlsplit` in real code.

### 15.7 Interview Questions

**Q1. How would you scale this to billions of pages across many machines?**

Partition the URL space by hostname hash so that one machine owns each host (keeps politeness/rate limits local and makes `seen` a local set per partition); discovered URLs for other partitions are sent through a queue (e.g. Kafka topic per partition). Use a Bloom filter or a disk-backed key-value store for `seen` at that scale, robots.txt caching, per-host rate limits (token buckets, Section 12), retries with backoff, and checkpointing of the frontier. See [High Level Design](High_Level_Design.md).

**Q2. Threads or asyncio for a crawler?**

The workload is I/O-bound with thousands of concurrent connections, which favors an event loop (asyncio, epoll-based C++ such as Asio): each in-flight request costs a few KB rather than a thread stack (8 MB virtual by default on Linux) and a kernel scheduling entity. Parsing HTML is CPU-bound, so a production crawler combines an async fetch loop with a process pool for parsing (in Python) to sidestep the GIL. Section 16 shows the asyncio version.

---

## 16. Async Web Crawler with Bounded Concurrency

### 16.1 Problem

Write an `asyncio` crawler that fetches pages concurrently but **never has more than K requests in flight**, applies a per-request timeout, tolerates failing pages, and terminates when the site is exhausted (or a page budget is reached). Demonstrate that the concurrency bound holds.

### 16.2 Approach

Two idiomatic shapes:

1. **Task per URL + `asyncio.Semaphore(K)`:** spawn a task for every discovered URL inside an `asyncio.TaskGroup`; each task does `async with sem:` around the fetch. The `TaskGroup` waits for all tasks, including ones created while it is waiting, so termination is automatic. Simple, but the number of *pending* tasks is unbounded (fine for thousands, not for millions).
2. **K workers + `asyncio.Queue`:** start K worker coroutines that loop `url = await q.get()`, fetch, enqueue new links, `q.task_done()`. `await q.join()` returns when every enqueued URL has been processed; then cancel the workers. Memory is bounded by the queue contents, not by task objects.

Because the event loop is single-threaded, `if url not in seen: seen.add(url)` is atomic **as long as there is no `await` between the check and the add** -- no lock needed. This is the main mental-model difference from threads.

### 16.3 Python Solution (both shapes, with a fake network)

```python
# async_crawler.py -- Python 3.11+ (TaskGroup, asyncio.timeout)
import asyncio
import random
import time


def hostname(url: str) -> str:
    return url.split("/")[2]


class FakeWeb:
    """Simulated network: ~10 ms per page, one page always hangs, one always errors."""

    def __init__(self, pages: int) -> None:
        rng = random.Random(0)
        self.links = {f"http://site.example/p{i}": [f"http://site.example/p{rng.randrange(pages)}"
                                                     for _ in range(4)] + [f"http://other.example/{i}"]
                      for i in range(pages)}
        self.links["http://site.example/p0"] += [f"http://site.example/p{i}" for i in range(1, pages, 10)]
        self.in_flight = 0
        self.max_in_flight = 0

    async def fetch_links(self, url: str) -> list[str]:
        self.in_flight += 1
        self.max_in_flight = max(self.max_in_flight, self.in_flight)
        try:
            if url.endswith("/p13"):
                await asyncio.sleep(10)                 # hangs: must be cut off by the timeout
            if url.endswith("/p17"):
                raise ConnectionError("simulated reset")
            await asyncio.sleep(0.01)
            return self.links.get(url, [])
        finally:
            self.in_flight -= 1


async def crawl_semaphore(start: str, fetch, limit: int, timeout: float = 0.2) -> set[str]:
    host, seen, sem = hostname(start), {start}, asyncio.Semaphore(limit)

    async def visit(url: str, tg: asyncio.TaskGroup) -> None:
        try:
            async with sem:                             # at most `limit` fetches in flight
                async with asyncio.timeout(timeout):
                    links = await fetch(url)
        except (TimeoutError, ConnectionError):         # one bad page must not kill the crawl
            return
        for link in links:
            if link not in seen and hostname(link) == host:   # no await in between: atomic
                seen.add(link)
                tg.create_task(visit(link, tg))

    async with asyncio.TaskGroup() as tg:
        tg.create_task(visit(start, tg))
    return seen


async def crawl_workers(start: str, fetch, workers: int, timeout: float = 0.2) -> set[str]:
    host, seen = hostname(start), {start}
    q: asyncio.Queue[str] = asyncio.Queue()
    q.put_nowait(start)

    async def worker() -> None:
        while True:
            url = await q.get()
            try:
                async with asyncio.timeout(timeout):
                    links = await fetch(url)
                for link in links:
                    if link not in seen and hostname(link) == host:
                        seen.add(link)
                        q.put_nowait(link)              # enqueued BEFORE task_done below
            except (TimeoutError, ConnectionError):
                pass
            finally:
                q.task_done()

    tasks = [asyncio.create_task(worker()) for _ in range(workers)]
    await q.join()                                      # unfinished count reached 0
    for t in tasks:
        t.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    return seen


async def main() -> None:
    for name, crawler in (("semaphore+TaskGroup", crawl_semaphore), ("workers+Queue", crawl_workers)):
        web = FakeWeb(300)
        t0 = time.perf_counter()
        seen = await crawler("http://site.example/p0", web.fetch_links, 10)
        ms = (time.perf_counter() - t0) * 1e3
        assert web.max_in_flight <= 10 and all(hostname(u) == "site.example" for u in seen)
        print(f"{name:20} pages={len(seen)} max_in_flight={web.max_in_flight} time={ms:.0f} ms")


if __name__ == "__main__":
    asyncio.run(main())
```

With a real HTTP client the fetch function looks like this (requires `pip install aiohttp`; share **one** session so connections are pooled):

```python
# fragment -- real fetch with aiohttp
import re
import aiohttp

HREF = re.compile(r'href="(http[^"]+)"')

async def fetch_links(session: aiohttp.ClientSession, url: str) -> list[str]:
    async with session.get(url) as resp:
        resp.raise_for_status()
        return HREF.findall(await resp.text())

# async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
#     await crawl_semaphore(start, lambda u: fetch_links(session, u), limit=20)
```

### 16.4 C++20 Solution (level-synchronous BFS, `std::counting_semaphore` bounds in-flight fetches)

C++ has no standard event loop yet (production code uses Boost.Asio or io_uring), so the C++ counterpart bounds concurrency with a counting semaphore around a blocking fetch. Each BFS level is fetched concurrently; an RAII permit guarantees the slot is returned even if the fetch throws.

```cpp
// bounded_crawler.cpp -- g++ -std=c++20 -O2 -pthread bounded_crawler.cpp
#include <algorithm>
#include <atomic>
#include <chrono>
#include <cstdio>
#include <future>
#include <semaphore>
#include <string>
#include <thread>
#include <unordered_map>
#include <unordered_set>
#include <vector>

std::string hostname(const std::string& url) {
    const auto start = url.find("//") + 2;
    const auto end = url.find('/', start);
    return url.substr(start, end == std::string::npos ? std::string::npos : end - start);
}

struct FakeWeb {
    std::unordered_map<std::string, std::vector<std::string>> links;
    std::atomic<int> inFlight{0}, maxInFlight{0};
    std::vector<std::string> fetch(const std::string& url) {
        const int now = ++inFlight;
        int prev = maxInFlight.load();
        while (now > prev && !maxInFlight.compare_exchange_weak(prev, now)) {}
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
        --inFlight;
        auto it = links.find(url);
        return it == links.end() ? std::vector<std::string>{} : it->second;
    }
};

class Permit {   // RAII: acquire in the constructor, release in the destructor
public:
    explicit Permit(std::counting_semaphore<>& s) : s_(s) { s_.acquire(); }
    ~Permit() { s_.release(); }
    Permit(const Permit&) = delete;
    Permit& operator=(const Permit&) = delete;
private:
    std::counting_semaphore<>& s_;
};

std::unordered_set<std::string> crawl(const std::string& start, FakeWeb& web, int limit) {
    const std::string host = hostname(start);
    std::counting_semaphore<> slots(limit);
    std::unordered_set<std::string> seen{start};    // touched only by this thread
    std::vector<std::string> frontier{start};
    while (!frontier.empty()) {
        std::vector<std::future<std::vector<std::string>>> futs;
        for (const auto& url : frontier)
            futs.push_back(std::async(std::launch::async, [&web, &slots, url] {
                Permit p(slots);                    // at most `limit` fetches run at once
                return web.fetch(url);
            }));
        std::vector<std::string> next;
        for (auto& f : futs)
            for (auto& u : f.get())
                if (hostname(u) == host && seen.insert(u).second) next.push_back(u);
        frontier = std::move(next);
    }
    return seen;
}

int main() {
    FakeWeb web;
    const int n = 200;
    for (int i = 0; i < n; ++i)
        web.links["http://site.example/p" + std::to_string(i)] = {
            "http://site.example/p" + std::to_string((i * 2 + 1) % n),
            "http://site.example/p" + std::to_string((i * 2 + 2) % n),
            "http://other.example/" + std::to_string(i)};
    const auto t0 = std::chrono::steady_clock::now();
    auto seen = crawl("http://site.example/p0", web, 10);
    const auto ms = std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
    std::printf("pages=%zu maxInFlight=%d (limit 10) time=%.0f ms %s\n", seen.size(),
                web.maxInFlight.load(), ms, seen.size() == n && web.maxInFlight <= 10 ? "OK" : "FAIL");
}
```

### 16.5 Correctness and Complexity

- **Concurrency bound:** every fetch happens inside `async with sem` / a `Permit`, so at most K fetches overlap; the fake network records the maximum to prove it.
- **Termination (TaskGroup):** the group exits only when all child tasks -- including those created by other children -- have finished. **(Queue):** each URL is `put` before its parent's `task_done()`, so the unfinished-task count cannot reach zero while work remains.
- **Failure isolation:** timeouts and connection errors are caught per page. In a `TaskGroup`, an *uncaught* exception cancels all sibling tasks -- deliberately structured concurrency, but fatal for a crawler if you forget the `try`.
- **Throughput:** with K slots and latency L, throughput is about K / L pages/s (Little's law: in-flight = throughput x latency). Here K = 10, L = 10 ms -> ~1000 pages/s, so 200-300 pages take ~0.3 s plus the timeout.
- **Level-synchronous straggler effect (C++ version):** each BFS level waits for its slowest page; the worker-queue design does not have this problem.

### 16.6 Pitfalls

- **Calling blocking code in a coroutine** (`requests.get`, `time.sleep`, heavy parsing) freezes the entire event loop. Use an async client, `await asyncio.to_thread(fn, ...)` for blocking calls, or a process pool for CPU-heavy parsing.
- **Fire-and-forget `asyncio.create_task` without keeping a reference:** the event loop holds only a weak reference to tasks, so an unreferenced task can be garbage-collected mid-flight. `TaskGroup` holds references for you.
- **`await` between the `seen` check and the add** reintroduces the race even on one thread (another coroutine runs at the `await`).
- **Semaphore acquired outside the timeout** vs inside: put `asyncio.timeout` *inside* `async with sem` if waiting for a slot should not count against the request timeout.
- **Unbounded fan-out:** task-per-URL creates a task object per discovered URL immediately; for very large crawls use the worker-queue design or a bounded `asyncio.Queue(maxsize=...)`.

### 16.7 Interview Questions

**Q1. `asyncio.Semaphore` vs a worker pool -- which bounds concurrency better?**

Both bound in-flight requests at K. The semaphore version bounds *active* work but not *pending* tasks (memory grows with discovered URLs); the worker pool bounds both active work and coroutine count, and gives a natural place for per-worker state (sessions, rate limiters). The semaphore pattern is better when tasks are naturally independent and you want structured cancellation through a `TaskGroup`.

**Q2. How would you add per-host politeness (at most 2 concurrent requests and 5 req/s per host)?**

Keep a `dict[host, asyncio.Semaphore(2)]` and a `dict[host, TokenBucket]` (Section 12 with `asyncio.Lock`/`asyncio.sleep`), acquiring the global semaphore, then the host semaphore, then a token -- always in the same order to avoid deadlock. Also honor `robots.txt` crawl-delay, and back off exponentially on HTTP 429/503.

---

## 17. Parallel Merge Sort and Parallel Prefix Sum

### 17.1 Problem

(a) Sort a large array using multiple threads. (b) Compute the inclusive prefix sum (`out[i] = in[0] + ... + in[i]`) of a large array using P threads. For both, state the work and span (critical path) and explain what limits the speedup.

### 17.2 Approach

**Parallel merge sort (fork-join):** split in half, sort the left half in a new task while the current thread sorts the right half, join, merge. Stop spawning below a size cutoff (e.g. 16K elements) or beyond a depth limit (about log2 of the core count) -- tasks smaller than that cost more to spawn than they save.

| Variant | Work T1 | Span T-inf | Parallelism T1 / T-inf |
|---|---|---|---|
| Parallel recursion, **serial merge** | O(n log n) | O(n) (the top-level merge alone is n) | O(log n) -- poor |
| Parallel recursion, **parallel merge** (split the larger run at its median, binary-search the split point in the other run, merge the halves in parallel) | O(n log n) | O(log^3 n) | ~n / log^2 n |
| Sample sort / chunk-sort + k-way merge | O(n log n) | O(n / P + P log P) in practice | ~P -- what real libraries do |

**Parallel prefix sum (three-phase blocked scan):** split into P contiguous blocks.

1. Each thread computes the inclusive scan of its own block (and thus the block total).
2. One thread computes the exclusive scan of the P block totals -> each block's offset. (P is small; O(P) serial work.)
3. Each thread adds its block's offset to every element of its block.

Work about 2n, span O(n / P + P). Phase 2 is exactly what a `std::barrier` completion function is for: it runs once, after everyone finishes phase 1 and before anyone starts phase 3.

Worked example, `in = [3, 1, 4, 1, 5, 9, 2, 6]`, P = 2: phase 1 gives `[3, 4, 8, 9 | 5, 14, 16, 22]` with block sums `[9, 22]`; phase 2 gives offsets `[0, 9]`; phase 3 gives `[3, 4, 8, 9, 14, 23, 25, 31]`.

### 17.3 C++20 Solution

```cpp
// parallel_sort_scan.cpp -- g++ -std=c++20 -O2 -pthread parallel_sort_scan.cpp
#include <algorithm>
#include <barrier>
#include <bit>
#include <chrono>
#include <cstdio>
#include <future>
#include <numeric>
#include <random>
#include <thread>
#include <vector>

template <class It>
void parallelMergeSort(It first, It last, int depth) {
    const auto n = last - first;
    if (n <= (1 << 14) || depth <= 0) {          // cutoff: below this, spawning costs more than it saves
        std::sort(first, last);
        return;
    }
    It mid = first + n / 2;
    auto left = std::async(std::launch::async, [=] { parallelMergeSort(first, mid, depth - 1); });
    parallelMergeSort(mid, last, depth - 1);     // this thread takes the right half
    left.get();                                  // join; rethrows if the left half threw
    std::inplace_merge(first, mid, last);        // serial O(n) merge: the span bottleneck
}

// `out` must already have in.size() elements (allocated by the caller, outside the timing).
void parallelInclusiveScan(const std::vector<long>& in, std::vector<long>& out, int P) {
    const std::size_t n = in.size();
    std::vector<long> blockSum(P), blockOffset(P);
    auto computeOffsets = [&]() noexcept {       // phase 2: once, after all threads finish phase 1
        long running = 0;
        for (int b = 0; b < P; ++b) {
            blockOffset[b] = running;
            running += blockSum[b];
        }
    };
    std::barrier sync(P, computeOffsets);

    auto worker = [&](int b) {
        const std::size_t lo = n * b / P, hi = n * (b + 1) / P;
        long s = 0;                              // accumulate in a register, not in shared memory
        for (std::size_t i = lo; i < hi; ++i) out[i] = (s += in[i]);   // phase 1: local scan
        blockSum[b] = s;
        sync.arrive_and_wait();                  // completion function runs here
        const long off = blockOffset[b];
        for (std::size_t i = lo; i < hi; ++i) out[i] += off;          // phase 3: add offset
    };
    std::vector<std::thread> ts;
    for (int b = 0; b < P; ++b) ts.emplace_back(worker, b);
    for (auto& t : ts) t.join();                 // join BEFORE the caller reads `out`
}

template <class F>
double timeMs(F&& f) {
    auto t0 = std::chrono::steady_clock::now();
    f();
    return std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
}

int main() {
    const unsigned hw = std::max(1u, std::min(16u, std::thread::hardware_concurrency()));
    std::mt19937_64 rng(42);

    // (a) merge sort
    std::vector<long> data(1 << 22);
    for (auto& x : data) x = static_cast<long>(rng() % 1000000);
    auto a = data, b = data;
    const int depth = static_cast<int>(std::bit_width(hw));   // ~2*hw leaf tasks
    double serial = timeMs([&] { std::sort(a.begin(), a.end()); });
    double par = timeMs([&] { parallelMergeSort(b.begin(), b.end(), depth); });
    std::printf("sort %zu: std::sort %.0f ms, parallel %.0f ms (%u threads) %s\n", data.size(), serial,
                par, hw, a == b ? "OK" : "FAIL");

    // (b) prefix sum
    std::vector<long> v(1 << 24);
    for (auto& x : v) x = static_cast<long>(rng() % 100);
    std::vector<long> expect(v.size());
    double s1 = timeMs([&] { std::inclusive_scan(v.begin(), v.end(), expect.begin()); });
    std::vector<long> got(v.size());
    double s2 = timeMs([&] { parallelInclusiveScan(v, got, static_cast<int>(hw)); });
    std::printf("scan %zu: serial %.0f ms, parallel %.0f ms %s\n", v.size(), s1, s2,
                got == expect ? "OK" : "FAIL");

    std::vector<long> tinyIn{3, 1, 4, 1, 5, 9, 2, 6}, tiny(tinyIn.size());
    parallelInclusiveScan(tinyIn, tiny, 2);
    for (long x : tiny) std::printf("%ld ", x);   // 3 4 8 9 14 23 25 31
    std::printf("\n");
}
```

### 17.4 Python Solution (processes, because of the GIL)

CPU-bound pure-Python code does not speed up with threads on a standard (GIL) build, so the parallel versions use a `ProcessPoolExecutor`. The data must be pickled to and from the workers, which is often more expensive than the computation itself -- in practice you would call `sorted()` / `numpy.sort` and `itertools.accumulate` / `numpy.cumsum`. The point of this code is to demonstrate the *algorithm structure* in Python.

```python
# parallel_sort_scan.py -- run as a script (process pools re-import the main module)
import heapq
import itertools
import random
from concurrent.futures import ProcessPoolExecutor


def chunks(xs: list, k: int) -> list[list]:
    n = len(xs)
    return [xs[n * i // k: n * (i + 1) // k] for i in range(k)]


def parallel_sort(xs: list[int], pool: ProcessPoolExecutor, k: int) -> list[int]:
    sorted_parts = list(pool.map(sorted, chunks(xs, k)))   # k independent sorts
    return list(heapq.merge(*sorted_parts))                  # k-way merge: O(n log k)


def block_total(block: list[int]) -> int:
    return sum(block)


def block_scan(block: list[int], offset: int) -> list[int]:
    return list(itertools.accumulate(block, initial=offset))[1:]


def parallel_prefix_sum(xs: list[int], pool: ProcessPoolExecutor, k: int) -> list[int]:
    blocks = chunks(xs, k)
    totals = list(pool.map(block_total, blocks))                       # phase 1
    offsets = list(itertools.accumulate(totals, initial=0))[:-1]       # phase 2 (serial, tiny)
    out: list[int] = []
    for part in pool.map(block_scan, blocks, offsets):                 # phase 3
        out.extend(part)
    return out


if __name__ == "__main__":
    rng = random.Random(0)
    data = [rng.randrange(1_000_000) for _ in range(200_000)]
    with ProcessPoolExecutor(max_workers=4) as pool:
        assert parallel_sort(data, pool, 4) == sorted(data)
        assert parallel_prefix_sum(data, pool, 4) == list(itertools.accumulate(data))
        print(parallel_prefix_sum([3, 1, 4, 1, 5, 9, 2, 6], pool, 2))   # [3, 4, 8, 9, 14, 23, 25, 31]
    print("parallel sort and prefix sum OK")
```

This phase-1 variant computes only block *totals* (a reduction) and does the full scan in phase 3, so it reads the input twice but writes the output once -- 3 passes of memory traffic instead of the C++ version's 4 (phase 1 writes `out`, phase 3 reads and writes it again). Both are correct; for a memory-bound kernel the reduce-then-scan form is usually faster.

### 17.5 Correctness and Complexity

- **Merge sort:** each recursive call sorts a disjoint sub-range, so the two halves never race; `left.get()` establishes happens-before from the left task's writes to the merge. Work O(n log n); span O(n) because of the serial top-level `inplace_merge`; so speedup saturates at a small factor (expect ~3-6x on 16 threads for 4M elements, not 16x).
- **Scan:** block b's final values are `offset[b] + local_scan`, and `offset[b] = sum of all elements before block b`, which is exactly the inclusive prefix sum. The barrier guarantees phase-1 writes to `blockSum` are visible to the completion function, and its writes to `blockOffset` are visible to phase 3.
- **What actually limits the scan:** it does ~1 add per 8 bytes loaded, so it is **memory-bandwidth bound**: speedup flattens once the threads saturate DRAM bandwidth (often at 4-8 cores per socket), regardless of core count. The roofline model makes this precise -- see [Performance Engineering: Roofline Model](Performance_Engineering.md#3-roofline-model).
- **GPU version:** the same reduce-then-scan structure appears hierarchically (wave -> workgroup -> grid), with Hillis-Steele (O(n log n) work, O(log n) span) or Blelloch (O(n) work, O(log n) span) inside a workgroup, and decoupled look-back for single-pass grid scans. See [GPU Kernel Case Studies](../ml-gpu/GPU_Kernel_Case_Studies.md) and [MPI_Scan](../ml-gpu/Parallel_GPU_Programming.md#mpi_scan-prefix-scan).

### 17.6 Pitfalls

- **No cutoff:** spawning a thread per recursive call creates millions of threads (and `std::async` creates a real thread per call in libstdc++). Always bound depth or size.
- **Reading results before joining:** the workers write `out`; nobody may read it until they are joined. Here is a subtle version. A function creates a local `std::vector<std::jthread>` and then does `return out;` by value. The return value is moved or copied out of `out` *before* the local jthreads' destructors join. That means the workers are still writing while `out` is being moved or copied. With a move, they keep indexing a moved-from, empty vector (UB). With a copy, the result is a torn snapshot. The caller never sees running threads, because the destructors finish before control returns. The bug is inside the function, and it only works by accident when NRVO elides the move. Join explicitly before returning.
- **Timing allocation and first touch:** an earlier version of this benchmark allocated `out` (128 MB, value-initialized on one thread) inside the timed function and was about 3x *slower* than the serial scan -- the page faults and zeroing dominated. Allocate outside the timed region, or let each worker first-touch its own block (which also places pages on the right NUMA node).
- **False sharing:** accumulating into `blockSum[b]` inside the loop would make every thread write the same few cache lines continuously; accumulate in a local variable and store once.
- **`std::sort(std::execution::par, ...)`** exists, but with GCC's libstdc++ it requires linking Intel TBB (`-ltbb`); without TBB it silently runs serially. Know this before claiming "C++17 parallel algorithms" in an interview.
- **Python:** thread-based parallel sort gives no speedup on a GIL build (and pickling cost can make the process version slower than `sorted()`).

### 17.7 Interview Questions

**Q1. Your parallel scan is only 2x faster on 16 cores. Why, and what do you check?**

Do the bandwidth arithmetic. The serial scan of 16M longs reads 128 MB and writes 128 MB; on the test machine above it takes ~6 ms, i.e. ~43 GB/s -- already close to what one core can stream. The three-phase parallel scan moves about twice the bytes (~512 MB: one read of `in` and one write of `out` in phase 1, then a read-modify-write of `out` in phase 3), so even at a socket's ~150-200 GB/s it needs ~3 ms: about 2x, which is what the benchmark shows. More cores cannot help a bandwidth-bound kernel. Check with STREAM or hardware counters (`perf stat` memory-bandwidth events, or a roofline view). Fixes: fewer passes (reduce-then-scan), narrower types, fusing the scan with its producer or consumer, and NUMA-aware placement (first-touch from the threads that use the data).

**Q2. State Amdahl's law and apply it to the merge sort.**

Speedup(P) = 1 / (s + (1 - s) / P) where s is the serial fraction. If the final serial merge is ~5% of the single-threaded time, the speedup on 16 cores is at most 1 / (0.05 + 0.95 / 16) = 1 / 0.109 = ~9.1x, and never more than 20x on any number of cores. Gustafson's law is the counterpoint: if the problem grows with P, the parallel part dominates and scaled speedup is nearly linear.

---

## 18. Pitfalls Checklist

Run through this list before declaring a concurrent solution done -- in an interview, saying "let me check for lost wakeups and lock ordering" out loud is itself a positive signal.

| # | Pitfall | Symptom | Fix | Sections |
|---|---|---|---|---|
| 1 | **Spurious / stolen wakeups** | Consumer pops from an empty queue; occasional crashes | Wait in a loop or with the predicate overload | 1.3, 8 |
| 2 | **Lost wakeup** | Rare permanent hang | Change predicate state under the waiter's mutex; prefer semaphores/events for one-shot signals | 1.3, 2 |
| 3 | **Wrong `notify_one`** with mixed waiters on one condition variable | Hang under some schedules | `notify_all`, or one condition variable per predicate | 4, 6, 8 |
| 4 | **Lock-order inversion** | Deadlock (A holds m1 wants m2, B holds m2 wants m1) | Global lock order / hierarchy; `std::scoped_lock`; never call unknown code while holding a lock | 7 |
| 5 | **Notify/destroy race** | Use-after-free on a condition variable or futex word | Notify under the lock when the waiter may destroy the object; manage lifetime with `shared_ptr` | 8.7, 10.6 |
| 6 | **ABA** in CAS loops | Corrupted lock-free stack/list | Tagged pointers, hazard pointers, epoch reclamation | 18.5 |
| 7 | **Data race on "just a flag"** | Works in debug, hangs at `-O2` | `std::atomic` with acquire/release (never `volatile`) | 2.6, 18.6 |
| 8 | **Check-then-act** (`if (!map.count(k)) map[k] = ...` across two critical sections) | Duplicate work or lost updates | One critical section, or atomic APIs (`insert().second`, `setdefault`) | 11, 15 |
| 9 | **Holding a lock during I/O or callbacks** | Throughput collapse; re-entrancy deadlock | Copy what you need, unlock, then call out | 11.6, 12.6, 15.6 |
| 10 | **Exception while holding a lock / permit** | Lock never released; hang | RAII (`lock_guard`, `scoped_lock`, `with`), RAII permits | 4.7, 16.4 |
| 11 | **Thread lifetime** | `std::terminate` (joinable `std::thread` destroyed), dangling references from detached threads | Join everything; `std::jthread`; never detach threads that capture locals by reference | 13, 17.6 |
| 12 | **False sharing** | Parallel code slower than serial | Accumulate locally; pad per-thread data to 64 bytes (`alignas(64)`) | 17.6 |
| 13 | **Oversubscription with spinning** | CPU at 100%, little progress | Spin-then-park; never pure-spin with more threads than cores | 10 |
| 14 | **No shutdown path** | Program hangs at exit | Closed flag in every wait predicate + `notify_all`; poison pills; `stop_token` | 8, 13 |
| 15 | **Python: assuming the GIL makes `x += 1` atomic** | Lost increments | `threading.Lock`; on free-threaded builds this matters even more | 1.5 |
| 16 | **asyncio: blocking call in a coroutine** | Whole program stalls | `await asyncio.to_thread(...)`, async libraries | 16.6 |

### 18.1 Spurious and Stolen Wakeups

A wait can return without a matching notify: POSIX allows it, futex-based implementations may return on signal interruption or on a racing wake, and with `notify_all` many threads wake for one unit of work. Separately, a third thread can grab the mutex between the notify and the waiter's reacquisition and consume the state ("stolen wakeup"). Both are handled identically: re-check the predicate after every return from `wait`.

### 18.2 Lost Wakeups

```cpp
// fragment -- BUG: `ready` is atomic, but it is modified without holding `m`
std::atomic<bool> ready{false};

void waiter() {
    std::unique_lock lk(m);
    cv.wait(lk, [] { return ready.load(); });   // (1) checks: false ... (3) goes to sleep
}
void signaller() {
    ready = true;        // (2a) lands after the waiter's check but before it blocks
    cv.notify_one();     // (2b) nobody is waiting yet -> the notification is lost forever
}

// FIX: make the state change inside the mutex the waiter holds while checking.
void signaller_fixed() {
    { std::lock_guard g(m); ready = true; }
    cv.notify_one();
}
```

The mutex makes "check predicate, then atomically release the mutex and sleep" indivisible with respect to "set predicate". Without it, the change can fall into the gap. Semaphores, events, futexes (`FUTEX_WAIT` compares the value in the kernel), and C++20 `atomic::wait(old)` avoid the gap by design.

### 18.3 Lock Ordering

```cpp
// fragment -- classic transfer deadlock and two fixes
void transfer_bug(Account& a, Account& b, long amt) {
    std::lock_guard la(a.m);            // T1: transfer(x, y) locks x then y
    std::lock_guard lb(b.m);            // T2: transfer(y, x) locks y then x -> deadlock
    a.balance -= amt; b.balance += amt;
}
void transfer_ordered(Account& a, Account& b, long amt) {
    Account& first = a.id < b.id ? a : b;     // global order by a stable key (id, not address
    Account& second = a.id < b.id ? b : a;    // if objects can move)
    std::lock_guard l1(first.m), l2(second.m);
    a.balance -= amt; b.balance += amt;
}
void transfer_scoped(Account& a, Account& b, long amt) {
    std::scoped_lock both(a.m, b.m);          // deadlock-avoidance algorithm inside
    a.balance -= amt; b.balance += amt;
}
```

Also handle `a == b` (locking the same non-recursive mutex twice is undefined behavior / self-deadlock). In large systems, assign each lock a level and assert at runtime that a thread only acquires locks of strictly increasing level (a "lock hierarchy").

### 18.4 Notify Under the Lock or After?

| | Notify while holding the mutex | Notify after unlocking |
|---|---|---|
| Correctness | Always correct | Correct if the predicate was changed under the mutex |
| Performance | Woken thread may immediately block on the mutex ("hurry up and wait") | Usually fewer context switches |
| Lifetime safety | Safe when the waiter may destroy the condition variable right after waking | Unsafe in that case: you may touch a destroyed condition variable |
| Python | Required (`notify` without holding the lock raises `RuntimeError`) | Not allowed |

Default to "modify under lock, unlock, notify"; switch to notify-under-lock when object lifetime is tied to the wait.

### 18.5 The ABA Problem

```cpp
// fragment -- Treiber stack pop with an ABA bug
struct Node { int value; Node* next; };
std::atomic<Node*> head{nullptr};

bool pop(int& out) {
    Node* old = head.load(std::memory_order_acquire);
    while (old && !head.compare_exchange_weak(old, old->next,      // reads old->next
                                              std::memory_order_acq_rel,
                                              std::memory_order_acquire)) {}
    if (!old) return false;
    out = old->value;
    delete old;                                                     // address may be reused
    return true;
}
```

Interleaving: T1 reads `head = A` and `A->next = B`, then is preempted. T2 pops A, pops B (deleting both), then pushes a new node that the allocator places at A's old address, with `next = C`. T1 resumes: its CAS compares `head == A` -- true, the *address* matches -- and installs `B`, a freed node. The stack is now corrupted (and T1's read of `old->next` was already a use-after-free).

Fixes:

- **Version tag:** CAS a `{pointer, counter}` pair (16-byte CAS, `cmpxchg16b` on x86-64) or pack a counter into unused high pointer bits; every successful CAS increments the counter, so a recycled address no longer matches.
- **Safe memory reclamation:** don't free a node while any thread may still hold a pointer to it -- hazard pointers or epoch-based reclamation/RCU (both standardized for C++26 as `std::hazard_pointer` and `std::rcu`), or a garbage collector (Java/Go don't have this half of the problem).
- **LL/SC** (ARM, POWER, RISC-V) fails if the location was written at all, not just changed in value -- but C++ exposes CAS semantics, so do not rely on it in portable code.

### 18.6 Memory Ordering for Flags That Publish Data

```cpp
// fragment -- message passing: relaxed is NOT enough when the flag publishes other data
int payload = 0;
std::atomic<bool> ready{false};
void producer() { payload = 42; ready.store(true, std::memory_order_release); }
void consumer() {
    while (!ready.load(std::memory_order_acquire)) { /* spin or wait */ }
    assert(payload == 42);   // guaranteed: release store synchronizes-with the acquire load
}
```

With `memory_order_relaxed` on both sides, the consumer may see `ready == true` and still read `payload == 0` (allowed by the C++ model; actually observable on ARM/POWER, and the compiler may reorder even on x86). x86's TSO hardware already keeps store->store and load->load order, so the release/acquire cost there is essentially zero -- it mostly constrains the compiler.

### 18.7 Interview Questions

**Q1. You have a hang in production. Walk through how you diagnose it.**

Capture all thread stacks without killing the process: `gdb -p PID -batch -ex "thread apply all bt"` (or `eu-stack -p PID`, `py-spy dump --pid PID` for Python, `jstack` for Java). Look for threads blocked in `futex_wait`/`pthread_mutex_lock`/`pthread_cond_wait` and identify which lock each holds (gdb can print a `pthread_mutex_t`'s `__owner` field, which is the owning thread's TID). A cycle among holders means deadlock; all threads waiting on condition variables with nobody runnable suggests a lost wakeup or missing shutdown signal; 100% CPU with no progress suggests livelock or spinning. Then reproduce under ThreadSanitizer or with stress plus randomized sleeps, and add the fix plus a regression test with a timeout. See [Debugging and Profiling Tools](../tools/Debugging_and_Profiling_Tools.md).

**Q2. Deadlock vs livelock vs starvation?**

Deadlock: threads blocked forever waiting on each other (no CPU used). Livelock: threads actively change state in response to each other but make no progress (e.g. dining philosophers who all put down their left fork and retry in lockstep); CPU is busy. Starvation: the system makes progress, but a particular thread is perpetually denied (writers under a reader-preferring RW lock; a thread that keeps losing an unfair mutex). Fixes: lock ordering for deadlock; randomized backoff for livelock; fairness (FIFO queues, aging, writer preference) for starvation.

---

## 19. Interview Q&A

**Q1. Lock-free vs wait-free vs obstruction-free -- and is lock-free always faster?**

Obstruction-free: a thread makes progress if it runs in isolation. Lock-free: some thread always makes progress (a CAS failure means another thread's CAS succeeded); individual threads can starve. Wait-free: every thread completes in a bounded number of its own steps. Lock-free is not automatically faster: CAS loops under heavy contention retry repeatedly and bounce cache lines just like locks, and safe memory reclamation adds overhead. The real advantages are robustness (no thread can block others by being preempted while holding a lock, no priority inversion, usable in signal handlers) and lower tail latency. Default to a mutex; go lock-free when profiling shows lock contention or when blocking is unacceptable.

**Q2. What is false sharing and how do you fix it?**

Two threads write different variables that share a 64-byte cache line; the coherence protocol moves the whole line back and forth, so independent writes behave like contended ones, often making parallel code slower than serial. Fix by accumulating in locals or registers and writing once, or padding per-thread data: `struct alignas(64) Counter { std::atomic<long> v; };`. C++17's `std::hardware_destructive_interference_size` names this constant, but GCC warns (`-Winterference-size`) that its value can differ between compiler flags, so many codebases hard-code 64 (128 on some ARM cores, and adjacent-line prefetching on Intel makes 128 safer). Detect it with `perf c2c`. See [Performance Engineering: False Sharing](Performance_Engineering.md#56-false-sharing-and-alignas64).

**Q3. Why is double-checked locking broken without atomics, and what should you use in C++?**

`if (!p) { lock; if (!p) p = new T; }` -- the unlocked first read races with the write. Without acquire/release, another thread can see a non-null `p` before the constructor's writes to `*p` are visible, and the plain read is a data race (undefined behavior) anyway. Correct versions: make `p` a `std::atomic<T*>` with acquire load / release store, or better, use a function-local `static` (C++11 guarantees thread-safe one-time initialization, "magic statics") or `std::call_once` with `std::once_flag`.

**Q4. Condition variable vs semaphore vs C++20 atomic wait -- when do you pick each?**

Condition variable: waiting for an arbitrary predicate over several pieces of state that a mutex already protects (queues, pools). Semaphore: counting resources or one-to-one signals between threads; it remembers signals, so no lost wakeups and no mutex required. `atomic::wait/notify`: a single word of state changes and you want futex-like efficiency without a mutex (flags, phase counters, building your own locks and barriers). If two threads must agree on a compound invariant, you need a mutex regardless.

**Q5. What is priority inversion and how is it solved?**

A high-priority thread H waits for a lock held by low-priority L, while a medium-priority M (not needing the lock) preempts L; H is effectively blocked by M indefinitely. The 1997 Mars Pathfinder resets were caused by this. Solutions: **priority inheritance** (L temporarily runs at H's priority while holding the lock; `PTHREAD_PRIO_INHERIT`, backed by `FUTEX_LOCK_PI` on Linux), **priority ceiling** (the lock raises its holder to a predefined ceiling), or avoid sharing locks across priority levels (lock-free queues between real-time and non-real-time threads).

**Q6. How would you design a concurrent hash map?**

Start with **lock striping**: an array of S mutexes, where bucket i is protected by mutex `i % S`, so operations on different stripes run in parallel. Resizing needs all stripes (acquire them in index order to avoid deadlock) or incremental migration. For read-heavy workloads, make reads lock-free: buckets as atomically published immutable nodes or open addressing with atomic slots, and writers use CAS; reclamation needs hazard pointers or epochs (Section 18.5). Mention real designs: Java's `ConcurrentHashMap` (CAS on empty bins, per-bin locks, cooperative resize), Intel TBB's `concurrent_hash_map`, Folly's `ConcurrentHashMap`. In Python, a `dict` + `Lock` (or sharded dicts) is the pragmatic answer.

**Q7. Threads, processes, or asyncio in Python?**

| Workload | Choice | Why |
|---|---|---|
| Many concurrent network calls (I/O-bound, high fan-out) | `asyncio` | Thousands of cheap coroutines, one thread, explicit `await` points |
| Blocking I/O libraries, moderate concurrency | `ThreadPoolExecutor` | Blocking calls release the GIL; easy to retrofit |
| CPU-bound pure Python | `ProcessPoolExecutor` / `multiprocessing` | Bypasses the GIL; pay for pickling and process startup |
| CPU-bound NumPy / C extensions that release the GIL | Threads | The heavy work runs outside the GIL |
| Free-threaded build (3.13t+) | Threads for CPU-bound work | No GIL -- but now every shared mutable structure needs explicit locking |

**Q8. Amdahl's law: 95% of a program parallelizes perfectly. Max speedup on 16 cores? On infinite cores?**

Speedup = 1 / (0.05 + 0.95 / 16) = 1 / 0.109375 = **9.14x** on 16 cores, and 1 / 0.05 = **20x** at most on any number of cores. Real speedups are lower due to synchronization, load imbalance, and memory bandwidth (Section 17).

**Q9. How do you make a flaky concurrency bug reproducible?**

Increase interleaving pressure: run thousands of iterations, more threads than cores, randomized `sleep`/`yield` injection at suspected race points, and CPU stress in parallel. Use deterministic tools: ThreadSanitizer finds races that have not yet manifested; `rr record --chaos` records and replays a failing execution; model checkers / systematic schedulers (e.g. Relacy, CHESS, Loom for Rust, `pytest-repeat` for brute force in Python) explore interleavings. Make time injectable so timing-dependent logic can be driven deterministically.

**Q10. What is the difference between `std::mutex`, `std::recursive_mutex`, `std::timed_mutex`, and `std::shared_mutex`?**

`std::mutex`: non-recursive, exclusive; relocking from the same thread is undefined behavior (usually deadlock). `std::recursive_mutex`: the owning thread may relock; it must unlock the same number of times -- often a design smell (it hides unclear lock ownership and makes invariants hard to reason about, since you may re-enter with the invariant broken). `std::timed_mutex`: adds `try_lock_for/try_lock_until`. `std::shared_mutex`: adds shared (reader) mode, with an implementation-defined fairness policy (Section 9).

**Q11. How do GPU synchronization primitives differ from CPU ones?**

GPU threads in a wavefront/warp execute in lockstep (SIMT), so a spinlock where lanes of one wave wait for each other can deadlock on GPUs without independent thread scheduling, which means all AMD GCN/CDNA/RDNA wavefronts (including gfx942/MI300) and NVIDIA before Volta (and it is inefficient everywhere); barriers exist only within a workgroup (`__syncthreads()`), and atomics have **scopes** (wavefront, workgroup, agent/device, system) that determine which observers see the result. Grid-wide synchronization usually means ending the kernel. Prefer reductions and scans (hierarchical, Section 17) over locks. See [Parallel GPU Programming: Synchronization Scope Summary](../ml-gpu/Parallel_GPU_Programming.md#215-synchronization-scope-summary) and [AMD GPU Architecture and Profiling](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md).

**Q12. You built a profiler/tracing library that records events from many application threads. How do you make recording cheap and thread-safe?**

Never take a global lock on the hot path. Give each thread its own buffer (`thread_local` pointer to a per-thread ring buffer registered once under a lock), so recording is a plain store plus a relaxed index update; a background thread or the flush at exit drains the buffers. If an SPSC handoff to a collector thread is needed, use a single-producer/single-consumer ring with acquire/release indices. Timestamps come from a cheap monotonic source (`clock_gettime(CLOCK_MONOTONIC)` via the vDSO, or `rdtsc` with calibration). Handle thread exit (flush in a `thread_local` destructor) and fork (reinitialize in the child). The same idea -- per-thread or per-CPU buffers instead of a shared lock -- underlies `perf`'s per-CPU ring buffers and LTTng; be ready to compare it with how the tool you work on records events.

---

## See Also

- [CS Fundamentals: Concurrency theory (6.1-6.10)](CS_Fundamentals.md#65-classic-concurrency-problems)
- [C++ Fundamentals: Atomic Operations](../languages/Cpp_Fundamentals.md#124-atomic-operations) and [Thread Pool](../languages/Cpp_Fundamentals.md#128-thread-pool-simplified-implementation)
- [Python Fundamentals: GIL & Threading](../languages/Python_Fundamentals.md#19-the-gil--threading), [Multiprocessing](../languages/Python_Fundamentals.md#20-multiprocessing), [asyncio](../languages/Python_Fundamentals.md#21-asyncio--asyncawait), [`concurrent.futures`](../languages/Python_Fundamentals.md#22-concurrentfutures)
- [Low Level Design: Rate Limiter](../design-patterns/Low_Level_Design_Interview_Prep.md#10-worked-design-rate-limiter) and [Cache](../design-patterns/Low_Level_Design_Interview_Prep.md#11-worked-design-cache)
- [C++ Testing](../languages/CPP_Testing.md) -- testing strategies and sanitizers
- Performance Engineering: [Amdahl's Law](Performance_Engineering.md#22-amdahls-law), [Roofline Model](Performance_Engineering.md#3-roofline-model), [False Sharing](Performance_Engineering.md#56-false-sharing-and-alignas64)
- [Coding Problem List](../practice/Coding_Problem_List.md) and [Flashcards](../practice/Flashcards.csv)
