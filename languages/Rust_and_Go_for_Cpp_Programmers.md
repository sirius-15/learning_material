# Rust and Go for C++ Programmers -- Comprehensive Comparison Reference

> Last reviewed: 2026-11 · Versions assumed: C++23 (GCC 15 / Clang 20), Rust 1.9x with edition 2024, Go 1.25+ (examples use `sync.WaitGroup.Go`; Green Tea GC default since Go 1.26)

> A compact map from C++ concepts to their Rust and Go counterparts, for a systems C++ engineer who has to answer "how would this look in Rust/Go?" or "why not Rust?" in an interview. Each section has a comparison table, runnable code, and interview Q&A. Complete programs compile as written (`g++ -std=c++23 -pthread`, `rustc --edition 2024`, `go run`); fragments are marked on their first line.

---

## Table of Contents

### Part 1: Rust

1. [Positioning: Three Answers to the Same Problems](#1-positioning-three-answers-to-the-same-problems)
2. [Ownership, Borrowing, and Lifetimes vs RAII and Move Semantics](#2-ownership-borrowing-and-lifetimes-vs-raii-and-move-semantics)
3. [Smart Pointers: Box, Rc, Arc, RefCell vs unique_ptr and shared_ptr](#3-smart-pointers-box-rc-arc-refcell-vs-unique_ptr-and-shared_ptr)
4. [Traits vs Concepts and Virtual Functions](#4-traits-vs-concepts-and-virtual-functions)
5. [Enums and match vs std::variant](#5-enums-and-match-vs-stdvariant)
6. [Result and ? vs Exceptions and std::expected](#6-result-and--vs-exceptions-and-stdexpected)
7. [Send, Sync, and Fearless Concurrency](#7-send-sync-and-fearless-concurrency)
8. [unsafe Rust](#8-unsafe-rust)
9. [Cargo and the Toolchain](#9-cargo-and-the-toolchain)
10. [FFI with C and C++: extern C, bindgen, cbindgen, cxx](#10-ffi-with-c-and-c-extern-c-bindgen-cbindgen-cxx)

### Part 2: Go

11. [Goroutines and the GMP Scheduler](#11-goroutines-and-the-gmp-scheduler)
12. [Channels and select](#12-channels-and-select)
13. [The sync Package and context Cancellation](#13-the-sync-package-and-context-cancellation)
14. [Interfaces and Structural Typing](#14-interfaces-and-structural-typing)
15. [Garbage Collection and Escape Analysis](#15-garbage-collection-and-escape-analysis)
16. [Error Handling and Modules](#16-error-handling-and-modules)

### Part 3: Side by Side and Interview Framing

17. [Side-by-Side Examples: C++ / Rust / Go](#17-side-by-side-examples-c--rust--go)
18. ["Why Not Rust?" -- A Balanced Answer](#18-why-not-rust----a-balanced-answer)
19. [Cross-Cutting Interview Q&A](#19-cross-cutting-interview-qa)

---

# Part 1: Rust

---

# 1. Positioning: Three Answers to the Same Problems

All three languages compile to native code. They differ in *who* guarantees memory safety and *when*.

| Concern | C++ | Rust | Go |
|---|---|---|---|
| Memory management | RAII + manual; programmer proves safety | Ownership + borrow checker; compiler proves safety | Tracing GC; runtime guarantees safety |
| Use-after-free / dangling | UB, caught (sometimes) by ASan | Compile error in safe code | Impossible (GC keeps object alive) |
| Data races | UB, caught (sometimes) by TSan | Compile error in safe code (`Send`/`Sync`) | Possible; detected at runtime by `-race` |
| Null | Raw/smart pointers can be null | No null references; `Option<T>` | `nil` pointers, maps, interfaces, channels |
| Error handling | Exceptions, error codes, `std::expected` | `Result<T, E>` + `?`; `panic!` for bugs | `error` return values; `panic` for bugs |
| Generics | Templates (+ concepts), monomorphized | Generics + traits, monomorphized, type-checked at definition | Type parameters (1.18+), GC-shape stenciling + dictionaries |
| Runtime polymorphism | `virtual` (vptr in object) | `dyn Trait` (fat pointer) | Interfaces (two-word value), structural |
| Concurrency primitive | `std::thread` (1:1 OS threads), C++20 stackless coroutines | OS threads + `async` futures (runtime like Tokio is a library) | Goroutines (M:N, runtime-scheduled) |
| Build / packages | CMake + vcpkg/Conan (fragmented) | Cargo + crates.io (one tool) | `go` tool + modules (one tool) |
| Compile speed | Slow (headers, templates) | Slow (monomorphization, borrowck, LLVM) | Very fast |
| Typical niche | Everything; HPC, GPU runtimes, games, LLVM | Safe systems code, infra, CLIs, kernels/drivers | Network services, cloud infra (Kubernetes, Docker, Prometheus) |

**Mental model:** Rust is "C++ with the Core Guidelines enforced by the compiler, and destructive moves". Go is "C with a GC, CSP-style concurrency, and a deliberately small language".

See also: [C++ Memory Management](Cpp_Fundamentals.md#3-memory-management), [Concurrency and Multithreading](../computer-science/CS_Fundamentals.md#6-concurrency-and-multithreading).

---

# 2. Ownership, Borrowing, and Lifetimes vs RAII and Move Semantics

## 2.1 Ownership and Destructive Moves

Rust's rules: (1) every value has exactly one owner; (2) when the owner goes out of scope the value is dropped (the `Drop` trait is the destructor -- this *is* RAII); (3) assignment or pass-by-value of a non-`Copy` type **moves** it.

| Aspect | C++ move | Rust move |
|---|---|---|
| Mechanism | `std::move` is a cast to `T&&`; a user-written move constructor runs | Always a shallow bitwise copy (`memcpy`); no user code runs |
| Source after move | Still alive, "valid but unspecified"; destructor still runs | Statically dead; compiler rejects any use; no destructor runs on it |
| Moved-from bugs | Compile fine; `unique_ptr` becomes null -> UB if dereferenced | Compile error `E0382: use of moved value` |
| `noexcept` concerns | `vector` reallocation copies unless move ctor is `noexcept` | N/A -- moves cannot fail |
| Self-referential types | Fix up pointers in move ctor | Not movable safely; needs `Pin` (used by `async`) |
| Conditional move | Object always destroyed at scope end | Compiler inserts hidden "drop flags" |

Because moves never run code and the source is gone, a Rust type does not need an "empty" state just to be movable (C++ `unique_ptr` must have a null state; Rust `Box<T>` is never null).

## 2.2 Borrowing: Aliasing XOR Mutability

A *borrow* is a reference that does not own. At any point a value can have **either** any number of shared borrows `&T` **or** exactly one exclusive borrow `&mut T`, never both. Since Rust 2018 borrows are "non-lexical": a borrow ends at its last use, not at the closing brace.

The classic C++ bug (iterator/reference invalidation) becomes a compile error:

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v{1, 2, 3};
    int& first = v[0];
    v.push_back(4);              // may reallocate -> 'first' dangles
    std::cout << first << '\n';  // compiles; undefined behavior
}
```

```rust
// fragment -- intentionally fails to compile
fn main() {
    let mut v = vec![1, 2, 3];
    let first = &v[0];        // shared borrow of v starts
    v.push(4);                // error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
    println!("{first}");      // shared borrow still live here
}
```

Why the rule exists: if nothing can mutate while you read, and nothing can read while you mutate, then iterator invalidation, aliasing-related optimizer surprises (the compiler can treat `&mut T` like C's `restrict`), and data races are all ruled out by the same check.

## 2.3 Lifetimes

A lifetime annotation **does not change how long anything lives**; it states a relationship the compiler then checks. "The returned reference lives no longer than both inputs":

```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() >= y.len() { x } else { y }
}

struct Parser<'src> {
    input: &'src str, // a struct that borrows must name the lifetime
    pos: usize,
}

impl<'src> Parser<'src> {
    fn next_word(&mut self) -> Option<&'src str> {
        let rest = &self.input[self.pos..];
        let rest_trim = rest.trim_start();
        if rest_trim.is_empty() { return None; }
        let start = self.pos + (rest.len() - rest_trim.len());
        let end = rest_trim.find(' ').map_or(self.input.len(), |i| start + i);
        self.pos = end;
        Some(&self.input[start..end])
    }
}

fn main() {
    let a = String::from("rocprof");
    let r;
    {
        let b = String::from("omniperf-legacy");
        r = longest(&a, &b);
        println!("{r}");
    }
    // println!("{r}"); // error[E0597]: `b` does not live long enough
    let mut p = Parser { input: "a bb ccc", pos: 0 };
    while let Some(w) = p.next_word() { print!("[{w}]"); }
    println!();
}
```

**Elision rules** (why most functions need no annotations): (1) each reference parameter gets its own lifetime; (2) if there is exactly one input lifetime, it is assigned to all output references; (3) if a parameter is `&self`/`&mut self`, its lifetime is assigned to the outputs. `'static` means "valid for the whole program" (string literals, leaked boxes, owned data with no borrows).

The C++ analog is returning a `std::string_view` or reference to a temporary. It compiles; Clang's `[[clang::lifetimebound]]` and `-Wdangling` catch a subset of cases.

## 2.4 Copy vs Clone

| | C++ | Rust |
|---|---|---|
| Implicit copy | Every copyable type, including deep copies (`std::vector` copy = O(n) allocation) | Only `Copy` types: bitwise, no `Drop` (integers, `&T`, small POD structs that opt in) |
| Explicit deep copy | Same syntax as implicit copy | `.clone()` -- visible in code review |
| Opt-out | `= delete` copy ctor | Default: types are move-only unless they derive `Clone`/`Copy` |

**Interview point:** C++ defaults to copy and makes move opt-in (`std::move`); Rust defaults to move and makes copy explicit. Hidden O(n) copies are a common C++ performance bug that Rust makes visible.

**Q1.** What is the practical difference between C++ and Rust move semantics?

C++ moves are non-destructive: `std::move` only casts to an rvalue reference, a move constructor runs user code, and the source object remains alive in a valid-but-unspecified state and is later destroyed. That forces every movable type to have a "moved-from" state (null `unique_ptr`, empty `vector`), makes `noexcept` on move constructors matter (`vector` falls back to copying otherwise), and permits use-after-move bugs that compile cleanly. Rust moves are destructive bitwise copies: no user code runs, moves cannot fail, the source is statically inaccessible (E0382), and its destructor does not run. The cost is that self-referential types cannot be moved naively, which is why `Pin` exists.

**Q2.** Does Rust's borrow checker run at runtime? What does it cost?

No. Borrow checking and lifetime checking are purely compile-time; references compile to plain pointers with zero overhead. Runtime checks exist only where you opt in: `RefCell` (borrow counter), slice indexing (bounds checks, often elided by the optimizer, avoidable with iterators or `get_unchecked` in `unsafe`), and integer overflow checks (on in debug, off in release by default).

**Q3.** Why might correct-looking code be rejected by the borrow checker?

The checker is conservative. Common cases: borrowing two fields through a method call (`self.a_mut()` and `self.b()` borrow all of `self`, while direct field access `&mut self.a` / `&self.b` is fine); mutating a collection while iterating it (use indices, `retain`, or collect changes first); graphs with back-pointers (use indices into a `Vec` arena, `Rc`/`Weak`, or `unsafe`). The fix is usually restructuring ownership, not fighting the checker.

---

# 3. Smart Pointers: Box, Rc, Arc, RefCell vs unique_ptr and shared_ptr

| Rust | Closest C++ | Notes |
|---|---|---|
| `Box<T>` | `std::unique_ptr<T>` | Never null (`Option<Box<T>>` is the nullable form, still 8 bytes via niche optimization) |
| `Rc<T>` | `std::shared_ptr<T>` with a non-atomic count | Single-threaded only; `!Send`, so the compiler stops it from crossing threads |
| `Arc<T>` | `std::shared_ptr<T>` | Atomic refcount; one allocation (like `make_shared`); pointer is 8 bytes vs 16 for `shared_ptr` |
| `Weak<T>` | `std::weak_ptr<T>` | Breaks cycles; `upgrade()` returns `Option<Rc<T>>` |
| `&T` / `&mut T` | `const T&` / `T&` / non-owning `T*` | Checked by the borrow checker; never null |
| `Cell<T>` | `mutable` member | Get/set/replace by value; never hands out references to the inner value (`get` needs `T: Copy`, `replace`/`take` work for any `T`) |
| `RefCell<T>` | No equivalent | Borrow rules checked **at runtime**; violation panics (`BorrowMutError`) |
| `Mutex<T>`, `RwLock<T>` | `std::mutex` + the data it guards | Rust's mutex **owns** the data; the only access path is through the lock guard |
| `OnceLock<T>`, `LazyLock<T>` | `std::call_once`, function-local `static` | Thread-safe lazy init (stable since 1.70 / 1.80) |
| `*const T` / `*mut T` | Raw `T*` | Creating is safe; dereferencing requires `unsafe` |

**Key idea -- interior mutability.** `Rc<T>` gives *shared* access, so it only hands out `&T`. To mutate shared data you wrap it: `Rc<RefCell<T>>` (single-threaded, runtime-checked) or `Arc<Mutex<T>>` (multi-threaded, lock-checked). The "aliasing XOR mutability" rule still holds; it just moves from compile time to run time.

```rust
use std::cell::RefCell;
use std::rc::{Rc, Weak};

#[derive(Debug)]
struct Node {
    name: String,
    parent: RefCell<Weak<Node>>,      // weak back-pointer: no cycle leak
    children: RefCell<Vec<Rc<Node>>>,
}

fn main() {
    let root = Rc::new(Node { name: "root".into(), parent: RefCell::new(Weak::new()), children: RefCell::new(vec![]) });
    let leaf = Rc::new(Node { name: "leaf".into(), parent: RefCell::new(Weak::new()), children: RefCell::new(vec![]) });

    root.children.borrow_mut().push(Rc::clone(&leaf));
    *leaf.parent.borrow_mut() = Rc::downgrade(&root);

    let p = leaf.parent.borrow().upgrade().map(|p| p.name.clone());
    println!("leaf parent = {p:?}");                       // Some("root")
    println!("root strong={} weak={}", Rc::strong_count(&root), Rc::weak_count(&root)); // 1, 1
    println!("leaf strong={}", Rc::strong_count(&leaf));   // 2 (local + root.children)

    let guard = root.children.borrow();     // shared runtime borrow
    let ok = root.children.try_borrow_mut(); // would panic with borrow_mut()
    println!("second mutable borrow allowed? {}", ok.is_ok()); // false
    drop(guard);
}
```

**Q1.** Why does Rust have both `Rc` and `Arc` when C++ has only `shared_ptr`?

Atomic increments cost more than plain ones (an uncontended `lock xadd` on x86 is ~20 cycles vs ~1 for a plain increment, and far more when the cache line bounces between cores), and many shared-ownership uses are single-threaded. C++ cannot safely offer a non-atomic `shared_ptr` because nothing stops you from passing it to another thread. Rust can, because `Rc` is `!Send`: `thread::spawn(move || rc.clone())` is a compile error. The type system makes the cheaper option safe.

**Q2.** When would you use `RefCell` and what is the risk?

When ownership is shared (e.g., `Rc` graph nodes, observer callbacks) or when a `&self` method must mutate a cache. The risk is moving errors from compile time to run time: a second `borrow_mut()` while a borrow is alive panics. Keep borrows short (do not hold a `Ref` across calls that might re-enter), and prefer `try_borrow_mut` in re-entrant code. It is `!Sync`; the thread-safe analogs are `Mutex`/`RwLock`/atomics.

---

# 4. Traits vs Concepts and Virtual Functions

A Rust trait plays three C++ roles at once: an abstract base class (when used as `dyn Trait`), a concept (when used as a generic bound), and a customization point (like `std::hash` specialization or ADL `swap`).

```rust
use std::f64::consts::PI;

trait Shape {
    fn area(&self) -> f64;
    fn name(&self) -> String { String::from("shape") } // default method
}

struct Circle { r: f64 }
struct Rect { w: f64, h: f64 }

impl Shape for Circle {
    fn area(&self) -> f64 { PI * self.r * self.r }
    fn name(&self) -> String { "circle".into() }
}
impl Shape for Rect {
    fn area(&self) -> f64 { self.w * self.h }
}

// Static dispatch: monomorphized per T, like a constrained template.
fn describe<T: Shape>(s: &T) -> String { format!("{} {:.2}", s.name(), s.area()) }

// Dynamic dispatch: &dyn Shape is a fat pointer (data ptr + vtable ptr).
fn total_area(shapes: &[Box<dyn Shape>]) -> f64 { shapes.iter().map(|s| s.area()).sum() }

fn main() {
    println!("{}", describe(&Circle { r: 1.0 }));
    let v: Vec<Box<dyn Shape>> = vec![Box::new(Circle { r: 1.0 }), Box::new(Rect { w: 2.0, h: 3.0 })];
    println!("{:.3}", total_area(&v)); // 9.142
    println!("{} bytes", std::mem::size_of::<&dyn Shape>()); // 16
}
```

| Aspect | C++ virtual | C++ templates + concepts | Rust traits |
|---|---|---|---|
| Dispatch | Dynamic | Static | Both: `T: Trait` static, `dyn Trait` dynamic |
| vtable location | `vptr` stored **inside each object** | N/A | In the **fat pointer**; object layout unchanged |
| Add interface to existing type | No (must inherit) | Yes (concepts are structural) | Yes, `impl MyTrait for i32`, subject to the orphan rule |
| Body type-checked | Yes | **At instantiation** (concepts constrain callers, not the body) | **At definition** -- generic body may only use what the bounds promise |
| Error messages | Good | Better with concepts, still long | Usually short: "the trait bound `T: Shape` is not satisfied" |
| Implementation inheritance | Yes | N/A | No; default methods + supertraits (`trait B: A`) + composition |
| Restrictions on runtime use | None | N/A | Trait must be *dyn-compatible* (formerly "object safe"): no generic methods, no `Self` in parameter/return types other than the receiver (opt such methods out with `where Self: Sized`), no associated consts, no `Sized` supertrait |

**Orphan rule (coherence):** you may write `impl Trait for Type` only if the trait or the type is defined in your crate. This guarantees there is at most one implementation of a trait for a type program-wide -- no ODR-style conflicts between libraries. The workaround is the newtype pattern (`struct Meters(f64);`).

Common derivable traits: `Debug` (printing), `Clone`, `Copy`, `PartialEq`/`Eq`, `PartialOrd`/`Ord`, `Hash`, `Default`. Operator overloading is trait implementation (`std::ops::Add`, `Index`, `Deref`).

**Q1.** How are Rust generics different from C++ templates?

Both monomorphize (one copy of machine code per concrete type, enabling inlining). The difference is checking: a C++ template body is only fully type-checked when instantiated, so errors surface deep in instantiation stacks, and even a C++20 concept does not stop the body from using operations the concept does not mention. A Rust generic function is checked once against its trait bounds, so a misuse is reported at the definition and every instantiation that satisfies the bounds is guaranteed to compile. Rust gives up some flexibility for this: no SFINAE or duck-typed expression templates, specialization is still unstable, and const generics are more limited than non-type template parameters.

**Q2.** Why does Rust put the vtable pointer in the reference rather than the object?

Objects do not pay 8 bytes of `vptr` unless they are used polymorphically, a type can implement many traits without multiple-inheritance layout tricks, and you can make an existing type (even `i32`) usable as `dyn Trait` without changing its layout. The cost is that `&dyn Trait` and `Box<dyn Trait>` are 16 bytes, and you cannot recover the concrete type without `Any`.

---

# 5. Enums and match vs std::variant

Rust `enum` is a tagged union (a sum type) whose variants carry data; `match` must be exhaustive.

```rust
#[derive(Debug)]
enum Event {
    KernelLaunch { name: String, grid: (u32, u32, u32) },
    MemCopy { bytes: u64, to_device: bool },
    Marker(String),
    Shutdown,
}

fn summarize(e: &Event) -> String {
    match e {
        Event::KernelLaunch { name, grid: (x, 1, 1) } => format!("1-D launch {name} x={x}"),
        Event::KernelLaunch { name, grid } => format!("launch {name} {grid:?}"),
        Event::MemCopy { bytes, to_device: true } if *bytes >= 1 << 20 => format!("large H2D {} MiB", bytes >> 20),
        Event::MemCopy { bytes, .. } => format!("copy {bytes} B"),
        Event::Marker(s) => format!("marker {s}"),
        Event::Shutdown => "shutdown".to_string(),
        // Removing a catch-all arm (e.g. Marker or Shutdown) -> error[E0004]: non-exhaustive patterns;
        // guarded arms never count toward exhaustiveness
    }
}

fn main() {
    let evs = [
        Event::KernelLaunch { name: "gemm".into(), grid: (128, 1, 1) },
        Event::KernelLaunch { name: "conv".into(), grid: (8, 8, 2) },
        Event::MemCopy { bytes: 64 << 20, to_device: true },
        Event::MemCopy { bytes: 512, to_device: false },
        Event::Marker("epoch".into()),
        Event::Shutdown,
    ];
    for e in &evs { println!("{}", summarize(e)); }
    // Niche optimization: Option<&T> and Option<Box<T>> use null as None.
    println!("{} {}", std::mem::size_of::<Option<&u64>>(), std::mem::size_of::<Option<u32>>()); // 8 8
}
```

The C++17 equivalent is `std::variant<KernelLaunch, MemCopy, Shutdown>` visited with `std::visit` and the "overloaded" lambda idiom (`template <class... Ts> struct overloaded : Ts... { using Ts::operator()...; };`); omitting a lambda is a compile error, but there are no nested patterns or guards.

| Aspect | `std::variant` | Rust `enum` + `match` |
|---|---|---|
| Exhaustiveness | `std::visit` fails to compile if an alternative is unhandled; `holds_alternative`/`get_if` chains are not checked | Always checked (`E0004`) |
| Nested patterns, guards, bindings | No (C++ pattern matching did not make C++26) | Yes: destructuring, `if` guards, ranges, `@` bindings |
| Same type twice | Awkward (index-based) | Variants are named |
| Invalid state | `valueless_by_exception` | None |
| Null | Pointers / `std::optional` | `Option<T>`; with niche optimization `Option<&T>` costs nothing |
| Recursive types | Needs `unique_ptr` indirection | Needs `Box` indirection |

**Q1.** Why does Rust not have null, and what does it cost?

References and `Box` are guaranteed non-null; absence is modeled as `Option<T>`, which forces the caller to handle `None` before getting a `T` (`match`, `if let`, `?`, `unwrap_or`). Because the compiler knows `&T` is never 0, it uses 0 to encode `None`, so `Option<&T>` and `Option<Box<T>>` are the same size as a raw pointer -- the safety is free at run time. `Option<u32>` has no spare bit pattern, so it needs a separate tag (8 bytes with padding).

---

# 6. Result and ? vs Exceptions and std::expected

Rust splits failures into two kinds:

- **Recoverable** errors return `Result<T, E>`; `?` returns early with the error, first converting it with `From::from`.
- **Bugs** (`unwrap` on `None`, out-of-bounds index, overflow in debug builds) `panic!`. A panic unwinds and runs `Drop` (like an exception) or aborts if `panic = "abort"` is set in the profile. `catch_unwind` exists for isolation at boundaries (thread pools, FFI), not for control flow.

| Aspect | C++ exceptions | C++23 `std::expected<T,E>` | Rust `Result<T,E>` | Go `error` |
|---|---|---|---|---|
| Visible in signature | No (`noexcept` only says "never") | Yes | Yes | Yes (by convention, last return value) |
| Happy-path cost | ~Zero (table-based unwinding) | A branch per check | A branch per check | A branch per check |
| Error-path cost | High (allocation + unwinding, microseconds) | Cheap | Cheap | Cheap (unless wrapping allocates) |
| Propagation syntax | Automatic | Manual `if (!r) return std::unexpected(r.error());` or `.and_then()` | `?` | `if err != nil { return ..., err }` |
| Forgetting to check | Impossible (propagates) | `[[nodiscard]]` warning | `#[must_use]` warning; can't get `T` without handling `E` | Easy (`_ =`), linters catch some |
| Composition | try/catch | Monadic `and_then`, `transform`, `or_else` (C++23) | `map`, `and_then`, `map_err`, `ok_or` | `errors.Is` / `errors.As` / `%w` wrapping |
| Common in | Most application C++ | New code, `-fno-exceptions` codebases | All Rust | All Go |

Library ecosystem: `thiserror` (derive `Display`/`From` for library error enums) and `anyhow` (type-erased `anyhow::Error` with `.context("...")` for applications). Full side-by-side code is in [17.4](#174-error-propagation).

**Q1.** Why did Rust choose `Result` over exceptions?

Explicitness and composability: the error type is part of the signature, `?` keeps propagation to one character so the "explicit errors are verbose" objection mostly disappears, and the compiler forces handling before the value is usable. There is no hidden control flow, so reasoning about invariants (and `unsafe` code) is easier -- though panics still unwind, which is why unsafe code must stay "panic-safe" just as C++ code must be exception-safe. Costs: error types must be designed and converted (`From` impls), and deep call stacks pay a branch per level.

See also: [C++ Exception Handling](Cpp_Fundamentals.md#14-exception-handling-and-error-management).

---

# 7. Send, Sync, and Fearless Concurrency

Two marker traits, auto-derived from a type's fields:

- **`Send`**: ownership of a `T` may be transferred to another thread.
- **`Sync`**: `&T` may be shared between threads. Formally `T: Sync` iff `&T: Send`.

| Type | Send | Sync | Why |
|---|---|---|---|
| `i32`, `String`, `Vec<T: Send>` | Yes | Yes | Plain owned data |
| `Rc<T>` | No | No | Non-atomic refcount |
| `Arc<T>` | If `T: Send + Sync` | If `T: Send + Sync` | Atomic refcount, shared `&T` |
| `Cell<T>`, `RefCell<T>` | If `T: Send` | No | Unsynchronized interior mutability |
| `Mutex<T>` | If `T: Send` | If `T: Send` | Lock makes shared mutation safe |
| `MutexGuard<'_, T>` | No | If `T: Sync` | Some platforms require unlock on the locking thread |
| `*const T`, `*mut T` | No | No | Conservative default; wrappers opt in with `unsafe impl Send` |

`std::thread::spawn` requires its closure to be `Send + 'static`, so you cannot accidentally share a non-thread-safe object or a dangling stack reference. `std::thread::scope` (1.63+) lifts the `'static` requirement by guaranteeing all threads are joined before the scope returns.

```rust
// fragment -- intentionally fails to compile
use std::rc::Rc;
fn main() {
    let shared = Rc::new(vec![1, 2, 3]);
    let s2 = Rc::clone(&shared);
    std::thread::spawn(move || println!("{:?}", s2));
    // error[E0277]: `Rc<Vec<i32>>` cannot be sent between threads safely
    // fix: use std::sync::Arc
}
```

**What "fearless concurrency" does and does not guarantee:**

| Prevented at compile time (safe Rust) | NOT prevented |
|---|---|
| Data races (unsynchronized access, at least one write) | Deadlocks (lock-order inversion still possible) |
| Accessing lock-protected data without the lock | Higher-level race conditions (check-then-act across two lock acquisitions) |
| Sending non-thread-safe types to other threads | Wrong memory orderings on atomics (logic bug, but not UB) |
| Dangling references to another thread's stack | Starvation, livelock, leaks (`mem::forget` and `Rc` cycles are safe) |

Atomics use the C++20 memory model directly: `Ordering::{Relaxed, Acquire, Release, AcqRel, SeqCst}` (no `consume`). If you know `std::memory_order`, you know Rust atomics.

**async Rust in one paragraph:** `async fn` compiles to a state machine implementing `Future` (stackless, like C++20 coroutines). Futures are lazy -- nothing runs until polled by an executor, and the standard library ships no executor; Tokio (multi-threaded, work-stealing) is the de facto runtime. Spawning on a multi-threaded runtime requires `Send` futures, so holding a `std::sync::MutexGuard` or an `Rc` across `.await` produces a compile error. Cancellation is "drop the future", which is simple but means any `.await` point is a potential cancellation point.

**Q1.** If Rust prevents data races, can a Rust program still have a race condition?

Yes. A data race is a specific memory-model violation (concurrent unsynchronized accesses, at least one a write) and is UB in C++; safe Rust rules it out. A race condition is a logic bug where the outcome depends on timing, e.g. `if map.lock().get(k).is_none() { map.lock().insert(k, v) }` -- each access is synchronized, but another thread can insert between the two locks. Deadlocks are also possible. Rust narrows the bug class from "UB that corrupts memory" to "wrong but well-defined behavior".

**Q2.** Why does a Rust `Mutex` wrap the data instead of sitting beside it?

In C++ the association between `std::mutex m` and the fields it protects is a comment; nothing stops access without the lock (Clang's `GUARDED_BY` thread-safety annotations are the closest tool). `Mutex<T>` makes the guard the only path to `&mut T`, and the guard's lifetime ties the reference to the lock being held, so "forgot to lock" and "kept a pointer after unlock" are compile errors. Rust mutexes also *poison* if a thread panics while holding the lock, which is why `lock()` returns a `Result`.

See also: [C++ Multithreading](Cpp_Fundamentals.md#12-multithreading-and-concurrency), [Concurrency Coding Problems](../computer-science/Concurrency_Coding_Problems.md).

---

# 8. unsafe Rust

`unsafe` does **not** turn off the borrow checker or type checking. It unlocks exactly five extra operations:

1. Dereference a raw pointer.
2. Call an `unsafe fn` (including FFI functions).
3. Access or modify a mutable `static`.
4. Implement an `unsafe trait` (e.g., `unsafe impl Send for MyType {}`).
5. Access fields of a `union`.

The idiom is to build a **safe abstraction** whose public API cannot cause UB however it is called, with the `unsafe` block justified by a `// SAFETY:` comment. The standard library's `split_at_mut` is the textbook example -- the borrow checker cannot prove two `&mut` halves are disjoint, so the implementation asserts it:

```rust
fn split_at_mut(v: &mut [i32], mid: usize) -> (&mut [i32], &mut [i32]) {
    let len = v.len();
    assert!(mid <= len);
    let p = v.as_mut_ptr();
    // SAFETY: [0, mid) and [mid, len) are disjoint and in bounds of the same
    // allocation, and both returned borrows inherit `v`'s lifetime.
    unsafe { (std::slice::from_raw_parts_mut(p, mid), std::slice::from_raw_parts_mut(p.add(mid), len - mid)) }
}

fn main() {
    let mut data = [1, 2, 3, 4, 5];
    let (a, b) = split_at_mut(&mut data, 2);
    a[0] = 10;
    b[0] = 30;
    println!("{data:?}"); // [10, 2, 30, 4, 5]
}
```

**UB in Rust** (only reachable through `unsafe`): two live `&mut` to the same memory, a `&T` to memory mutated by someone else, dangling/unaligned/null references, invalid values (`bool` that is 2, out-of-range enum discriminant, uninitialized integers), data races, and violating an `unsafe fn`'s documented contract. Rust's aliasing rules are *stricter* than C++'s, so naively porting pointer-juggling C++ into `unsafe` Rust can be more dangerous than the original.

**Tools:** Miri (`cargo +nightly miri test`) interprets MIR and detects most UB including aliasing-model violations (Stacked/Tree Borrows); sanitizers via `-Zsanitizer=address|thread` on nightly; `cargo geiger` counts `unsafe` in dependencies. Edition 2024 tightened the rules: `unsafe` operations inside an `unsafe fn` need their own `unsafe {}` block (lint warns), `extern` blocks must be written `unsafe extern`, and references to `static mut` are denied by default.

**Q1.** Does using `unsafe` mean Rust gives no more guarantees than C++?

No. The guarantee becomes "UB can only originate in code marked `unsafe`, or in safe code whose correctness an `unsafe` block depends on (e.g., the module that maintains a `Vec`'s `len <= capacity` invariant)". That shrinks the audit surface from the whole program to a few hundred annotated lines, which can be reviewed intensively and tested with Miri. Empirically, large Rust codebases (Android, Chromium components, the Linux kernel's Rust drivers) keep `unsafe` to a small fraction of lines, concentrated at FFI and low-level data-structure boundaries.

---

# 9. Cargo and the Toolchain

| Task | Rust (one tool) | C++ (typical) |
|---|---|---|
| Toolchain install / pin | `rustup`, `rust-toolchain.toml` | Distro packages, modules, containers |
| New project | `cargo new app` / `cargo new --lib lib` | Hand-written `CMakeLists.txt` |
| Build | `cargo build [--release]` | `cmake -B build && cmake --build build` |
| Dependencies | `Cargo.toml` + crates.io; `Cargo.lock` pins exact versions | vcpkg / Conan / FetchContent / git submodules |
| Tests | `cargo test` (unit tests in the same file under `#[cfg(test)]`, integration tests in `tests/`, doc-tests in comments) | GoogleTest/Catch2 + CTest |
| Benchmarks | `cargo bench` (Criterion crate on stable) | Google Benchmark |
| Lint / format | `cargo clippy`, `cargo fmt` | clang-tidy, clang-format |
| Docs | `cargo doc` (rustdoc) | Doxygen |
| Feature flags | `[features]` -- additive, unified across the dependency graph | `option()` / `#ifdef` |
| Build scripts | `build.rs` (compile C code, run bindgen, emit `cargo:rustc-link-lib=...`) | CMake custom commands |
| Monorepo | `[workspace]` with a shared lockfile and target dir | `add_subdirectory` |

```toml
# Cargo.toml (fragment)
[package]
name = "trace-tool"
version = "0.1.0"
edition = "2024"
rust-version = "1.85"      # MSRV

[dependencies]
serde = { version = "1", features = ["derive"] }
anyhow = "1"

[profile.release]
lto = "fat"                # whole-program optimization
codegen-units = 1          # slower build, better code
panic = "abort"            # no unwinding tables; smaller, slightly faster
debug = "line-tables-only" # symbolized profiles without full debuginfo
```

**Editions** (2015/2018/2021/2024) are opt-in per crate, and crates of different editions link together freely -- Rust's answer to evolving syntax without breaking old code, something C++ cannot do per translation unit. There is **no stable Rust ABI**: Rust crates are linked from source compiled by the same compiler; stable binary interfaces go through `extern "C"`.

**Q1.** What do you miss going from Cargo back to CMake, and vice versa?

From Cargo: one standard layout, dependency resolution with a lockfile, built-in test/bench/doc, and reproducible builds with one command. From CMake: mature support for mixed-language builds (C, C++, HIP/CUDA, Fortran), toolchain files for cross-compiling GPU/embedded targets, and integration with system packages and existing C++ binary distributions. In mixed projects, `corrosion` (CMake imports Cargo crates) or the `cc`/`cmake` crates (Cargo builds C/C++) bridge the two.

See also: [CMake Fundamentals](../tools/CMake_Fundamentals.md).

---

# 10. FFI with C and C++: extern C, bindgen, cbindgen, cxx

The stable bridge between Rust and anything else is the **C ABI**. C++ classes, templates, exceptions, and `std::` types do not cross it directly.

| Direction / Tool | What it does |
|---|---|
| `unsafe extern "C" { fn f(...); }` | Declare C functions callable from Rust (edition 2024 requires `unsafe extern`; individual items can be marked `safe fn`) |
| `#[unsafe(no_mangle)] pub extern "C" fn` | Export a Rust function with an unmangled C symbol (edition 2024 syntax; older editions use `#[no_mangle]`) |
| `#[repr(C)]` | Lay out a struct/enum exactly as C would; default Rust layout may reorder fields |
| `bindgen` | Generates Rust `extern` declarations and `#[repr(C)]` structs from C (and simple C++) headers via libclang, usually from `build.rs` |
| `cbindgen` | The reverse: generates a C/C++ header from Rust `extern "C"` items |
| `cxx` | A `#[cxx::bridge]` module declares both sides; generates matching Rust and C++ glue so `std::string`, `std::unique_ptr`, `std::vector`, `rust::String`, `rust::Vec`, `rust::Box`, slices, and opaque types cross safely with no `unsafe` at call sites |
| `autocxx` | Builds on bindgen + cxx to bind existing C++ headers with less hand-written bridge code |

Export from Rust and call from C++ (complete; build steps in the comment):

```rust
// stats.rs -- build: rustc --edition 2024 --crate-type staticlib -O stats.rs
#[repr(C)]
pub struct Stats {
    pub count: u64,
    pub mean: f64,
}

#[unsafe(no_mangle)]
pub extern "C" fn stats_compute(ptr: *const f64, len: usize) -> Stats {
    if ptr.is_null() || len == 0 {
        return Stats { count: 0, mean: 0.0 };
    }
    // SAFETY: caller guarantees ptr points to `len` initialized f64 values.
    let xs = unsafe { std::slice::from_raw_parts(ptr, len) };
    Stats { count: len as u64, mean: xs.iter().sum::<f64>() / len as f64 }
}
```

```cpp
// main.cpp -- build: g++ -std=c++23 main.cpp libstats.a -o demo   (add -lpthread -ldl -lm on older toolchains)
#include <cstddef>
#include <cstdint>
#include <iostream>
#include <vector>

extern "C" {
struct Stats { std::uint64_t count; double mean; };  // must match #[repr(C)]
Stats stats_compute(const double* ptr, std::size_t len);
}

int main() {
    std::vector<double> v{1.0, 2.0, 3.0, 4.0};
    Stats s = stats_compute(v.data(), v.size());
    std::cout << s.count << " values, mean " << s.mean << '\n';  // 4 values, mean 2.5
}
```

A `cxx` bridge looks like this (needs the `cxx` crate and `cxx-build` in `build.rs`):

```rust
// fragment -- requires the cxx crate
#[cxx::bridge(namespace = "prof")]
mod ffi {
    struct Sample { pc: u64, count: u32 }        // shared struct, same layout both sides

    extern "Rust" {
        fn summarize(samples: &[Sample]) -> String; // implemented in Rust, callable from C++
    }
    unsafe extern "C++" {
        include!("prof/collector.h");
        type Collector;                            // opaque C++ class
        fn make_collector(device: i32) -> UniquePtr<Collector>;
        fn drain(self: Pin<&mut Collector>) -> Vec<Sample>;
    }
}
```

**FFI rules that come up in interviews:**

- **Panics must not unwind across `extern "C"`.** Since Rust 1.81 a panic escaping an `extern "C"` function aborts the process; use `extern "C-unwind"` only if both sides intend to propagate unwinding. Similarly, C++ exceptions must not escape into Rust frames through `extern "C"`. Catch at the boundary and convert to an error code.
- **Free memory with the allocator that allocated it.** Export `thing_free(ptr)` from Rust (`drop(Box::from_raw(ptr))`) rather than letting C++ `delete` a Rust allocation.
- **Strings:** `CString`/`CStr` for NUL-terminated C strings; Rust `&str` is pointer + length and not NUL-terminated.
- **Nullable pointers:** `Option<&T>`, `Option<Box<T>>`, and `Option<extern "C" fn(...)>` are guaranteed to have the same ABI as a nullable C pointer.
- **Ownership is documented, not checked**, across the boundary: wrap raw handles in a Rust type with `Drop` immediately.

**Q1.** How would you introduce Rust into a large C++ codebase?

Pick a leaf component with a narrow interface and a clear safety payoff (a parser of untrusted input, a file-format reader, a network-facing daemon). Define the boundary as a C ABI or a `cxx` bridge, keep data crossing it simple (POD structs, slices, opaque handles), build the crate as a static library from CMake (Corrosion), and run both sides' tests in CI with sanitizers on the C++ side and Miri on the `unsafe` Rust. Avoid bidirectional chatty calls across the boundary, since every crossing loses inlining and each language's guarantees.

**Q2.** Why can't Rust call C++ templates or classes directly?

C++ has no stable ABI across compilers, name mangling is compiler-specific, templates do not exist until instantiated (and instantiation requires the C++ front end), and semantics such as non-trivial move constructors, exceptions, and overload resolution have no Rust equivalent. Tools therefore either bind a C-like subset (bindgen), generate C++ shims that instantiate what you need (`cxx`, `autocxx`), or require you to write an `extern "C"` facade.

---

# Part 2: Go

---

# 11. Goroutines and the GMP Scheduler

A goroutine is a user-space thread managed by the Go runtime. It starts with a **2 KB stack** that grows by **copying** to a larger contiguous stack (and shrinks during GC). Compare a Linux `std::thread`: 8 MB of reserved virtual stack (default `ulimit -s`), a kernel task, and roughly 10 µs or more to create and join. Hundreds of thousands of goroutines are routine.

The scheduler is M:N, built from three entities:

| Entity | Meaning | Count |
|---|---|---|
| **G** | Goroutine: stack, instruction pointer, status | Unbounded |
| **M** | Machine: an OS thread | Grows as needed (default cap 10,000) |
| **P** | Processor: the right to run Go code; owns a local run queue (256 slots), a `runnext` slot, and a per-P memory cache | `GOMAXPROCS` |

- **Finding work:** `runnext` -> local queue -> global queue (checked every 61st schedule against starvation) -> netpoller -> **steal half** of a random other P's queue.
- **Blocking syscall:** the M blocks with its G and the P is handed to another M, so other goroutines keep running. **Network I/O** never blocks an M: the G parks and the netpoller (epoll/kqueue/IOCP) wakes it, so blocking-style code scales like an event loop.
- **Preemption:** prologue checks plus **async signal-based preemption** (Go 1.14+); `sysmon` flags goroutines running > ~10 ms.
- **GOMAXPROCS** defaults to logical CPUs; since **Go 1.25** on Linux it respects the cgroup CPU limit (no more `GOMAXPROCS=64` in a 2-CPU container).
- **cgo calls** are treated like syscalls (tens of ns; Go 1.26 cut baseline overhead ~30%), and C code cannot keep pointers into goroutine stacks because stacks move.

| Model | Scheduling | Stack | Cancellation |
|---|---|---|---|
| C++ `std::thread` | Kernel, 1:1 | Fixed, large | Cooperative (`std::stop_token`, C++20) |
| C++20 coroutines | Your executor | Stackless frame (heap or elided) | Library-defined |
| Rust `async` + Tokio | Work-stealing runtime (library) | Stackless state machine | Drop the future |
| Go goroutines | Runtime GMP, preemptive | Growable, copied | `context.Context` |

**Q1.** What happens when 10,000 goroutines all call a blocking `read()` on regular files?

Regular-file I/O is not handled by the netpoller on Linux, so each blocked goroutine pins an M. The runtime hands each P to a new M, so the thread count can climb toward thousands (and hit the 10,000-thread limit, which crashes the program). Mitigations: bound concurrency with a semaphore (buffered channel) or worker pool, and remember network sockets do not have this problem. Interviewers use this to check that you know goroutines are cheap but syscalls still consume OS threads.

**Q2.** How is the GMP design similar to a GPU's wave scheduler?

Both oversubscribe cheap execution contexts onto a fixed number of execution resources and switch to another ready context when one stalls -- goroutines on I/O, wavefronts on memory latency. The difference is cost and granularity: a GPU switches waves every cycle in hardware with registers statically partitioned (occupancy), while Go switches in software at scheduling points, costing ~100-200 ns, with stacks in memory.

---

# 12. Channels and select

"Do not communicate by sharing memory; instead, share memory by communicating." A channel is a typed, synchronized queue (internally a mutex-protected ring buffer plus wait queues of senders/receivers).

| Operation | `nil` channel | Open channel | Closed channel |
|---|---|---|---|
| Send `ch <- v` | Blocks forever | Blocks until a receiver takes it (unbuffered) or buffer has space | **Panics** |
| Receive `<-ch` | Blocks forever | Blocks until a value is available | Returns remaining buffered values, then zero value immediately; `v, ok := <-ch` gives `ok == false` |
| `close(ch)` | **Panics** | Succeeds; wakes all receivers | **Panics** |

- **Unbuffered** channels are a rendezvous: the send completes only when a receiver takes the value, which gives a happens-before edge in both directions.
- **Buffered** `make(chan T, n)` decouples up to `n` items; a buffered channel of `struct{}` is a counting semaphore.
- **Only the sender closes.** Close means "no more values", not "free resources"; with many senders, a separate goroutine closes after a `WaitGroup` says all senders are done.
- `for v := range ch` loops until the channel is closed and drained.

`select` waits on several channel operations; if several are ready it picks one **uniformly at random** (prevents starvation); `default` makes it non-blocking; a case on a `nil` channel is never selected (the idiom for disabling a case: set `results = nil` after its last value); `case <-time.After(d)` adds a timeout; `close(quit)` broadcasts to every receiver. A complete `select` program is in [Section 13](#13-the-sync-package-and-context-cancellation).

**Goroutine leaks** are Go's memory leak: a goroutine blocked forever on a channel nobody will send to or receive from is never collected. Every goroutine needs a defined exit path (channel close or `ctx.Done()`). Go 1.26 adds an experimental `goroutineleak` pprof profile.

**Q1.** Channel or mutex?

Channels for transferring ownership of data or coordinating stages (pipelines, fan-out/fan-in, worker pools, signaling completion); mutexes for protecting shared state that many goroutines read/modify in place (caches, counters, maps). A mutex-protected counter is roughly an order of magnitude cheaper than routing increments through a channel (~20 ns uncontended lock vs ~50-100 ns plus a goroutine switch per channel op). The Go wiki's advice is "use whichever is most expressive and/or most simple".

**Q2.** Why does sending on a closed channel panic instead of returning an error?

Because it is always a program bug: the protocol says only the owner/sender closes, after its last send. Making it a panic surfaces the ownership violation immediately. Receiving from a closed channel, by contrast, is the normal end-of-stream signal, so it returns the zero value with `ok == false`.

---

# 13. The sync Package and context Cancellation

| Tool | Purpose | C++ analog | Gotcha |
|---|---|---|---|
| `sync.Mutex` | Mutual exclusion | `std::mutex` | Not reentrant; zero value is ready; **must not be copied** after use (`go vet` copylocks) |
| `sync.RWMutex` | Many readers / one writer | `std::shared_mutex` | Writer-preferring; recursive read-locking can deadlock |
| `sync.WaitGroup` | Wait for N goroutines | `std::latch` / joining threads | Call `Add` before `go`; Go 1.25 `wg.Go(f)` does `Add`/`Done` for you |
| `sync.Once`, `OnceFunc`, `OnceValue` | One-time init | `std::call_once` | `OnceFunc`/`OnceValue` since Go 1.21 |
| `sync.Cond` | Condition variable | `std::condition_variable` | Rarely needed; channels usually clearer |
| `sync.Map` | Concurrent map | -- | Only wins for write-once/read-many or disjoint key sets; otherwise `map` + `Mutex` |
| `sync.Pool` | Reuse temporary objects | Free list | Per-P caches; pooled objects are released across GC cycles, so never use it as a cache of state |
| `sync/atomic` | `atomic.Int64`, `atomic.Pointer[T]` (1.19+) | `std::atomic<T>` | All Go atomics are sequentially consistent; no relaxed ordering |
| `errgroup` (`golang.org/x/sync`) | WaitGroup + first error + cancel siblings | -- | Use when one failure should cancel the rest |

The **race detector** (`go test -race`, `go run -race`) is ThreadSanitizer-based; it typically costs 5-10x memory and 2-20x CPU and only reports races that actually execute, so run it on tests that exercise concurrency.

`context.Context` carries cancellation, deadlines, and request-scoped values down a call tree. Conventions: first parameter named `ctx`; never store it in a struct; always `defer cancel()` (otherwise the timer/child links leak until the parent is cancelled -- `go vet` lostcancel flags this). Cancelling a parent cancels all children; `ctx.Done()` is a channel closed on cancellation; `ctx.Err()` is `context.Canceled` or `context.DeadlineExceeded`.

```go
package main

import (
	"context"
	"errors"
	"fmt"
	"time"
)

// worker simulates a long job that checks for cancellation between steps.
func worker(ctx context.Context, id int, steps int) error {
	for i := 0; i < steps; i++ {
		select {
		case <-ctx.Done():
			return fmt.Errorf("worker %d stopped at step %d: %w", id, i, ctx.Err())
		case <-time.After(10 * time.Millisecond): // one unit of work
		}
	}
	return nil
}

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 35*time.Millisecond)
	defer cancel() // release resources even on the success path

	errs := make(chan error, 2)
	go func() { errs <- worker(ctx, 1, 2) }()   // finishes in ~20 ms
	go func() { errs <- worker(ctx, 2, 100) }() // would take ~1 s; cancelled
	for range 2 {
		err := <-errs
		switch {
		case err == nil:
			fmt.Println("a worker finished")
		case errors.Is(err, context.DeadlineExceeded):
			fmt.Println("deadline:", err)
		}
	}
}
```

C++20's `std::jthread` + `std::stop_token` is the closest standard C++ analog (cooperative, the callee must poll); in Rust/Tokio you drop the future or use `tokio_util::sync::CancellationToken`.

**Q1.** Why is copying a `sync.Mutex` a bug?

A Go `Mutex` is a value type holding its state inline. Copying a locked mutex (e.g., passing a struct containing it by value, or a value-receiver method) gives the copy the "locked" state with no owner, or makes two goroutines lock different copies thinking they share one. Embed the mutex in a struct used via pointer, use pointer receivers, and run `go vet`. In C++ `std::mutex` is non-copyable, so the compiler catches this; Go relies on vet.

---

# 14. Interfaces and Structural Typing

A Go type satisfies an interface **implicitly** by having its methods -- no `implements` keyword. This is structural typing: conformance is checked at compile time when a concrete type is assigned to an interface (and at run time only for type assertions/switches), much like C++ concepts, but dispatch is dynamic through the itab. Idiomatic interfaces are tiny and defined by the consumer: `io.Reader` (`Read(p []byte) (int, error)`), `io.Writer`, `fmt.Stringer`, `error`.

Representation: an interface value is **two words** -- (type/itab pointer, data pointer) -- similar to Rust's `&dyn Trait`, unlike C++'s in-object `vptr`. Storing a non-pointer value in an interface may allocate ("boxing").

```go
package main

import (
	"errors"
	"fmt"
)

type Shape interface{ Area() float64 }

type Rect struct{ W, H float64 }

func (r Rect) Area() float64 { return r.W * r.H } // value receiver: Rect and *Rect both satisfy Shape

type Counter struct{ n int }

func (c *Counter) Inc() { c.n++ } // pointer receiver: only *Counter has Inc

var _ Shape = Rect{}                  // compile-time "implements" assertion
var _ interface{ Inc() } = (*Counter)(nil)

type MyErr struct{}

func (*MyErr) Error() string { return "my error" }

func mayFail(fail bool) error {
	var p *MyErr // typed nil pointer
	if fail {
		p = &MyErr{}
	}
	return p // BUG: interface holds (type=*MyErr, value=nil) -> non-nil error
}

// Generics (Go 1.18+): constraints are interfaces describing type sets.
type Number interface{ ~int | ~int64 | ~float64 }

func Sum[T Number](xs []T) T {
	var s T
	for _, x := range xs {
		s += x
	}
	return s
}

func main() {
	shapes := []Shape{Rect{2, 3}, &Rect{1, 1}}
	for _, s := range shapes {
		fmt.Println(s.Area())
	}
	err := mayFail(false)
	fmt.Println("err != nil?", err != nil) // true -- the classic gotcha
	var target *MyErr
	fmt.Println("errors.As:", errors.As(err, &target))
	fmt.Println(Sum([]int{1, 2, 3}), Sum([]float64{1.5, 2.5}))
}
```

| Aspect | Go | C++ | Rust |
|---|---|---|---|
| Satisfaction | Implicit (structural) | `virtual`: explicit inheritance; concepts: structural | Explicit `impl Trait for T` |
| Reuse | Struct **embedding** promotes methods (composition; no virtual call back into the outer type) | Inheritance | Default methods, composition |
| Generics implementation | GC-shape stenciling + runtime dictionaries (not full monomorphization; pointer types share one instantiation) | Full monomorphization | Full monomorphization |
| Retroactive conformance | Yes, any type in any package can satisfy your interface | Concepts yes, virtual no | Yes, within the orphan rule |

**Q1.** Explain the "nil interface is not nil" bug.

An interface is nil only when **both** words are nil. Returning a nil `*MyErr` through an `error` return produces (type = `*MyErr`, data = nil), which compares non-nil, so callers think an error occurred. Fix: return a literal `nil` on success (`if fail { return &MyErr{} }; return nil`) and never declare a concrete error-typed variable to return through an interface.

**Q2.** Why are Go generics sometimes slower than hand-written code, unlike C++ templates?

Go compiles one instantiation per *GC shape* (all pointer types share one), passing a dictionary with type information at run time. Method calls on type parameters with pointer shapes become indirect calls through the dictionary and may block inlining, so a generic `Max[T]` over pointer types can be slower than a specialized version. C++ and Rust generate fully specialized code per type at the cost of binary size and compile time. Go chose fast compiles and smaller binaries.

---

# 15. Garbage Collection and Escape Analysis

Go's collector is a **concurrent, tri-color, mark-sweep** collector: **non-moving** (pointers stay valid; no compaction), **non-generational**, with a write barrier enabled during marking and two short stop-the-world phases (typically well under 1 ms). Since **Go 1.26** the **Green Tea** collector is the default: it marks small objects span-by-span (page-oriented) rather than chasing individual objects, improving locality, and uses vector instructions on newer amd64 CPUs; the Go team reports 10-40% lower GC overhead on real programs, with little gain or slight regressions on low-fan-out pointer-chasing heaps.

Tuning knobs:

| Knob | Meaning |
|---|---|
| `GOGC=100` (default) | Next GC triggers when the heap grows 100% over the live heap after the last cycle -> peak heap ~2x live. `GOGC=200` halves GC frequency at the cost of more memory; `off` disables |
| `GOMEMLIMIT` (1.19+) | Soft memory limit; the GC runs more often as the limit approaches. Set ~90% of the container limit to avoid OOM kills |
| Mark assists | Goroutines that allocate during marking are drafted to help mark -- the main source of GC-induced latency |
| Background marking | Targets ~25% of `GOMAXPROCS` during a cycle |
| `GODEBUG=gctrace=1` | One line per GC: heap sizes, pause times, CPU percent |

**Escape analysis** decides whether a value lives on the goroutine stack (free) or the heap (GC-managed). Returning `&local` is legal and safe -- the value simply escapes to the heap -- whereas in C++ it is a dangling pointer. Inspect decisions with `go build -gcflags=-m`. Common escape causes: storing in an interface, capturing in a closure that outlives the frame, sending a pointer on a channel, slices whose size is unknown at compile time.

| | C++ / Rust (no GC) | Go (tracing GC) |
|---|---|---|
| Deallocation timing | Deterministic (scope exit / last owner) | Nondeterministic; `defer` for non-memory resources |
| Memory overhead | Allocator fragmentation only | ~`GOGC`% headroom over live heap |
| CPU overhead | malloc/free, refcount atomics | Typically a few % to ~25% during marking |
| Tail latency | Large frees can cascade (destroying a big tree) | Mark assists, STW pauses (sub-ms) |
| Cycles | Leak with `shared_ptr`/`Rc` unless `weak` | Collected |
| Programmer effort | Ownership design | Low; reduce allocations when profiling says so |

Reducing GC cost in Go mirrors reducing `malloc` cost in C++: preallocate slices (`make([]T, 0, n)`), reuse buffers (`sync.Pool`), avoid boxing into interfaces in hot loops, prefer values over pointers in large slices (fewer pointers to scan), and profile with `pprof` (`-memprofile`, `alloc_space`).

**Q1.** Your Go service in a 4 GiB container is OOM-killed under load, though the live heap is 2.5 GiB. Why, and what do you do?

With `GOGC=100` the heap target is ~2x the live heap (~5 GiB), above the container limit, and the GC does not know about the cgroup limit. Set `GOMEMLIMIT` to ~3.6 GiB so the GC collects more aggressively near the limit (accepting more GC CPU), reduce live heap (smaller caches, fewer pointers), or raise the container limit. Also check goroutine leaks (each holds its stack and whatever it references) with the goroutine profile.

---

# 16. Error Handling and Modules

## 16.1 Errors

`error` is the interface `interface{ Error() string }`, returned as the last result. Idioms:

- **Wrap** with context: `fmt.Errorf("open %s: %w", path, err)` (`%w` preserves the chain; multiple `%w` and `errors.Join` since Go 1.20).
- **Inspect** the chain: `errors.Is(err, fs.ErrNotExist)` for sentinel values; `errors.As(err, &pathErr)` to extract a typed error -- the Go analog of `catch (const std::filesystem::filesystem_error& e)`.
- **Sentinel errors**: `var ErrNotFound = errors.New("not found")` exported for comparison.
- **panic/recover** is for bugs and impossible states. `recover()` works only inside a deferred function; an unrecovered panic in **any** goroutine terminates the whole process -- the same as an exception escaping a `std::thread` (which calls `std::terminate`); a recover in `main` or in the parent goroutine does not catch a panic in a child goroutine.
- **`defer`** runs at **function** exit (not block exit), LIFO, with arguments evaluated at the `defer` statement. `defer f.Close()` inside a loop over 10,000 files keeps 10,000 files open until the function returns -- wrap the loop body in a function.

## 16.2 Modules

| File / concept | Role | C++/Rust analog |
|---|---|---|
| `go.mod` | Module path, `go` language version, `toolchain`, `require`, `replace`, `exclude`, `tool` (1.24+) | `Cargo.toml` / `vcpkg.json` |
| `go.sum` | Cryptographic hashes of every dependency, verified against the public checksum DB (`sum.golang.org`) | Part of `Cargo.lock` |
| **Minimal Version Selection** | Chooses, for each module, the **maximum of the minimum versions** required anywhere in the graph; never "latest", so builds are reproducible without a lockfile | Cargo picks the newest semver-compatible version, then locks |
| Semantic import versioning | Major v2+ changes the import path (`example.com/lib/v2`), so v1 and v2 can coexist | Cargo allows multiple major versions in a graph |
| `GOPROXY` | Default `https://proxy.golang.org,direct`; module mirror for availability and immutability | crates.io |
| `go work` | Multi-module local workspace (1.18+) | Cargo workspace |
| `go mod tidy` / `vendor` | Sync requirements / copy dependencies into `vendor/` | `cargo vendor` |

Build outputs are single static binaries by default when `CGO_ENABLED=0` (no libc dependency), which is why Go dominates container-native tooling: `FROM scratch` images and trivial cross-compilation (`GOOS=linux GOARCH=arm64 go build`).

**Q1.** What are the arguments for and against Go's `if err != nil` style?

For: errors are values, visible in every signature and every call site, cheap, and trivially inspectable; there is no hidden control flow, so reading a function tells you every exit path. Against: verbosity (often a third of the lines), easy to drop an error silently by assigning to `_`, and no compiler enforcement that errors are checked (linters like `errcheck` fill the gap). Compared with Rust, Go lacks a `?` operator and sum types, so "either a value or an error" is a convention, not a type.

See also: [Containers and CI](../tools/Containers_and_CI.md).

---

# Part 3: Side by Side and Interview Framing

---

# 17. Side-by-Side Examples: C++ / Rust / Go

## 17.1 Ownership Transfer

```cpp
#include <iostream>
#include <memory>
#include <utility>
#include <vector>

struct Buffer {
    std::vector<int> data;
    explicit Buffer(std::size_t n) : data(n, 0) {}
    ~Buffer() { std::cout << "free " << data.size() << " ints\n"; }
};

void consume(std::unique_ptr<Buffer> b) {        // takes ownership
    std::cout << "consumed " << b->data.size() << '\n';
}                                                 // Buffer destroyed here

int main() {
    auto b = std::make_unique<Buffer>(1024);
    consume(std::move(b));
    // b is a null unique_ptr ("moved-from"); b->data compiles and is UB.
    std::cout << (b ? "still owned" : "moved-from: null") << '\n';
}
```

```rust
struct Buffer {
    data: Vec<i32>,
}

impl Drop for Buffer {
    fn drop(&mut self) { println!("free {} ints", self.data.len()); }
}

fn consume(b: Buffer) {                 // takes ownership (no Box needed)
    println!("consumed {}", b.data.len());
}                                       // b dropped here

fn borrow(b: &Buffer) -> usize { b.data.len() } // borrows, does not own

fn main() {
    let b = Buffer { data: vec![0; 1024] };
    println!("borrowed len {}", borrow(&b));
    consume(b);                         // move: a memcpy of 3 words (ptr, cap, len)
    // println!("{}", b.data.len());    // error[E0382]: borrow of moved value: `b`
    println!("after consume");
}
```

```go
package main

import "fmt"

type Buffer struct{ data []int }

func consume(b *Buffer) { fmt.Println("consumed", len(b.data)) }

func main() {
	b := &Buffer{data: make([]int, 1024)}
	consume(b)
	// No ownership concept: both caller and callee may keep using b.
	// The GC frees the Buffer once it is unreachable; there is no destructor,
	// so non-memory resources use explicit Close() + defer.
	fmt.Println("caller still sees", len(b.data))
}
```

| | C++ | Rust | Go |
|---|---|---|---|
| Who frees | Last `unique_ptr` owner, at scope exit | Owner, at scope exit (`Drop`) | GC, at some later time |
| Use after transfer | Compiles; null deref is UB | Compile error | Allowed and safe (shared) |
| Ownership visible in signature | `unique_ptr<T>` by value | `T` by value vs `&T` / `&mut T` | No |

## 17.2 Thread-Safe Counter

```cpp
#include <atomic>
#include <iostream>
#include <mutex>
#include <thread>
#include <vector>

int main() {
    constexpr int kThreads = 8, kIters = 100'000;
    std::atomic<long> atomic_count{0};
    long locked_count = 0;   // association with 'm' is only a convention
    std::mutex m;
    {
        std::vector<std::jthread> ts;  // jthread joins in its destructor (C++20)
        for (int t = 0; t < kThreads; ++t)
            ts.emplace_back([&] {
                for (int i = 0; i < kIters; ++i) {
                    atomic_count.fetch_add(1, std::memory_order_relaxed);
                    std::lock_guard lk(m);
                    ++locked_count;    // dropping the lock_guard line still compiles: data race, UB
                }
            });
    }
    std::cout << atomic_count << ' ' << locked_count << '\n';  // 800000 800000
}
```

```rust
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::Mutex;
use std::thread;

fn main() {
    const THREADS: usize = 8;
    const ITERS: u64 = 100_000;

    // Scoped threads may borrow locals; all are joined at scope end.
    let atomic_count = AtomicU64::new(0);
    let locked_count = Mutex::new(0u64);          // the Mutex owns the counter
    thread::scope(|s| {
        for _ in 0..THREADS {
            s.spawn(|| {
                for _ in 0..ITERS {
                    atomic_count.fetch_add(1, Ordering::Relaxed);
                    *locked_count.lock().unwrap() += 1; // only path to the u64
                }
            });
        }
    });
    println!("{} {}", atomic_count.load(Ordering::Relaxed), locked_count.into_inner().unwrap()); // 800000 800000
}
```

With `thread::spawn` instead of `thread::scope`, the closure must be `'static`, so the counter needs shared ownership: `Arc<Mutex<u64>>` with an `Arc::clone` per thread (`Rc` would not compile).

```go
package main

import (
	"fmt"
	"sync"
	"sync/atomic"
)

func main() {
	const threads, iters = 8, 100_000
	var atomicCount atomic.Int64
	var mu sync.Mutex
	lockedCount := 0 // nothing ties it to mu; forgetting Lock compiles, -race catches it at run time

	var wg sync.WaitGroup
	for range threads {
		wg.Go(func() { // Go 1.25+: Add(1) + go + defer Done()
			for range iters {
				atomicCount.Add(1)
				mu.Lock()
				lockedCount++
				mu.Unlock()
			}
		})
	}
	wg.Wait()
	fmt.Println(atomicCount.Load(), lockedCount) // 800000 800000
}
```

Performance note for all three: 8 threads hammering one counter are bottlenecked on one cache line bouncing between cores (~50-100 ns per contended RMW). The scalable fix is identical in every language: per-thread local counts, combined once at the end (or a sharded counter with cache-line padding).

## 17.3 Producer-Consumer (bounded, multiple producers and consumers)

Three producers each send 100 items (`p*1000 + i`); two consumers sum them. Expected `sum = 315150`.

**C++:** the standard library has no blocking queue, so you hand-write a monitor: one `std::mutex`, a `std::deque`, two `std::condition_variable`s (`not_full_` for producers, `not_empty_` for consumers, each waited on with a predicate), and a `closed_` flag that `close()` sets before `notify_all()` on both, so `pop()` returns `std::nullopt` once closed and drained. The main thread joins the producers, calls `close()`, then joins the consumers. The complete, tested implementation is in [Bounded Blocking Queue](../computer-science/Concurrency_Coding_Problems.md#8-bounded-blocking-queue-leetcode-1188).

```rust
use std::sync::mpsc;
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let (tx, rx) = mpsc::sync_channel::<i64>(4);   // bounded: send blocks when full
    let rx = Arc::new(Mutex::new(rx));             // mpsc = single consumer; share it for 2

    let consumers: Vec<_> = (0..2)
        .map(|_| {
            let rx = Arc::clone(&rx);
            thread::spawn(move || {
                let mut local = 0i64;
                loop {
                    let msg = rx.lock().unwrap().recv(); // guard dropped at end of statement
                    match msg {
                        Ok(v) => local += v,
                        Err(_) => break,             // every Sender dropped -> closed
                    }
                }
                local
            })
        })
        .collect();

    let producers: Vec<_> = (0..3)
        .map(|p| {
            let tx = tx.clone();
            thread::spawn(move || {
                for i in 1..=100 { tx.send(p * 1000 + i).unwrap(); }
            })                                       // this clone dropped here
        })
        .collect();
    drop(tx);                                        // drop the original, or recv never ends

    for p in producers { p.join().unwrap(); }
    let sum: i64 = consumers.into_iter().map(|c| c.join().unwrap()).sum();
    println!("sum = {sum}");
}
```

(Production Rust would use `crossbeam-channel` or `flume`, whose receivers are cloneable MPMC, instead of a `Mutex<Receiver>`; holding the mutex while blocked in `recv` serializes the consumers.)

```go
package main

import (
	"fmt"
	"sync"
)

func main() {
	jobs := make(chan int, 4) // bounded buffer

	var producers sync.WaitGroup
	for p := range 3 { // per-iteration loop variable since Go 1.22
		producers.Go(func() {
			for i := 1; i <= 100; i++ {
				jobs <- p*1000 + i
			}
		})
	}
	go func() { producers.Wait(); close(jobs) }() // single closer, after all senders

	results := make(chan int)
	var consumers sync.WaitGroup
	for range 2 {
		consumers.Go(func() {
			local := 0
			for v := range jobs { // ends when jobs is closed and drained
				local += v
			}
			results <- local
		})
	}
	go func() { consumers.Wait(); close(results) }()

	sum := 0
	for r := range results {
		sum += r
	}
	fmt.Println("sum =", sum)
}
```

| | C++ | Rust (std) | Go |
|---|---|---|---|
| Lines of queue code | ~40 (hand-written) | 0 (`sync_channel`) | 0 (`chan`) |
| "Closed" signal | Explicit `close()` flag | Last `Sender` dropped (RAII) | `close(ch)` by the sender side |
| Classic bug | Lost wakeup, `if` instead of predicate `wait` | Forgetting `drop(tx)` -> consumers hang | Closing twice / sending after close -> panic; leaked goroutines |

## 17.4 Error Propagation

Read a thread count from a config file: I/O error, parse error, or range error.

```cpp
#include <charconv>
#include <expected>
#include <fstream>
#include <iostream>
#include <string>
#include <system_error>

enum class ConfigError { FileNotFound, ParseError, OutOfRange };

std::expected<std::string, ConfigError> read_first_line(const std::string& path) {
    std::ifstream in(path);
    if (!in) return std::unexpected(ConfigError::FileNotFound);
    std::string s;
    std::getline(in, s);
    return s;
}

std::expected<int, ConfigError> parse_int(const std::string& s) {
    int v{};
    auto [p, ec] = std::from_chars(s.data(), s.data() + s.size(), v);
    if (ec != std::errc{} || p != s.data() + s.size()) return std::unexpected(ConfigError::ParseError);
    return v;
}

std::expected<int, ConfigError> load_threads(const std::string& path) {
    return read_first_line(path)          // C++23 monadic chaining; no '?' operator
        .and_then(parse_int)
        .and_then([](int n) -> std::expected<int, ConfigError> {
            if (n < 1 || n > 1024) return std::unexpected(ConfigError::OutOfRange);
            return n;
        });
}

int main() {
    auto r = load_threads("/nonexistent/threads.cfg");
    if (r) std::cout << "threads = " << *r << '\n';
    else   std::cout << "error code " << static_cast<int>(r.error()) << '\n';  // error code 0
}
```

```rust
use std::fmt;
use std::num::ParseIntError;

#[derive(Debug)]
enum ConfigError {
    Io(std::io::Error),
    Parse(ParseIntError),
    OutOfRange(i64),
}

impl fmt::Display for ConfigError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ConfigError::Io(e) => write!(f, "io: {e}"),
            ConfigError::Parse(e) => write!(f, "parse: {e}"),
            ConfigError::OutOfRange(n) => write!(f, "{n} not in 1..=1024"),
        }
    }
}
impl std::error::Error for ConfigError {}

// These From impls are what `?` calls; thiserror's #[from] generates them.
impl From<std::io::Error> for ConfigError {
    fn from(e: std::io::Error) -> Self { ConfigError::Io(e) }
}
impl From<ParseIntError> for ConfigError {
    fn from(e: ParseIntError) -> Self { ConfigError::Parse(e) }
}

fn load_threads(path: &str) -> Result<i64, ConfigError> {
    let text = std::fs::read_to_string(path)?;  // io::Error -> ConfigError
    let n: i64 = text.trim().parse()?;          // ParseIntError -> ConfigError
    if !(1..=1024).contains(&n) {
        return Err(ConfigError::OutOfRange(n));
    }
    Ok(n)
}

fn main() {
    match load_threads("/nonexistent/threads.cfg") {
        Ok(n) => println!("threads = {n}"),
        Err(ConfigError::Io(e)) if e.kind() == std::io::ErrorKind::NotFound => {
            println!("missing config, using default")
        }
        Err(e) => println!("error: {e}"),
    }
}
```

```go
package main

import (
	"errors"
	"fmt"
	"io/fs"
	"os"
	"strconv"
	"strings"
)

var ErrOutOfRange = errors.New("thread count out of range")

func loadThreads(path string) (int, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return 0, fmt.Errorf("load threads: %w", err) // wrap, keep the chain
	}
	n, err := strconv.Atoi(strings.TrimSpace(string(data)))
	if err != nil {
		return 0, fmt.Errorf("parse %s: %w", path, err)
	}
	if n < 1 || n > 1024 {
		return 0, fmt.Errorf("%d: %w", n, ErrOutOfRange)
	}
	return n, nil
}

func main() {
	_, err := loadThreads("/nonexistent/threads.cfg")
	if errors.Is(err, fs.ErrNotExist) { // walks the %w chain
		fmt.Println("missing config, using default")
	}
	var pathErr *fs.PathError
	if errors.As(err, &pathErr) { // typed extraction, like catch-by-type
		fmt.Println("failed path:", pathErr.Path)
	}
	fmt.Println(err) // load threads: open /nonexistent/threads.cfg: no such file or directory
}
```

---

# 18. "Why Not Rust?" -- A Balanced Answer

Interviewers ask this to see whether you can weigh engineering tradeoffs rather than recite slogans. A strong answer acknowledges the safety case, then grounds the decision in the specific codebase.

**The case for Rust (state it fairly):**

- Memory-safety bugs are the majority of severe security bugs in large C/C++ codebases: Microsoft and Chromium have each reported ~70%. Google reported Android's share of memory-safety vulnerabilities fell from 76% (2019) to 24% (2024) as new code shifted to memory-safe languages -- without rewriting old code, because vulnerabilities concentrate in new code.
- Data races become compile errors; refactoring concurrent code is far less risky.
- Performance is on par with C++ (same LLVM backend, monomorphization, no GC), and Cargo removes a whole category of build/dependency pain.

**The case against (or "not yet") for a C++-heavy GPU/HPC stack such as ROCm:**

| Factor | Why it matters |
|---|---|
| Existing investment | Millions of lines of C++ (LLVM, HIP runtime, profiler SDKs, math libraries); a rewrite adds risk and delays features |
| Interop cost | C++ templates and classes do not cross into Rust; every boundary needs a C ABI or `cxx` shim, and safety stops at that boundary |
| Device code | GPU kernels are written in HIP/CUDA C++, Triton, or assembly; Rust GPU kernel support (rust-gpu, Rust-CUDA, `nvptx`/`amdgpu` targets) is experimental compared with HIP |
| Ecosystem / vendors | Vendor SDKs, debuggers, and profilers expose C/C++ APIs first |
| People | Hiring and training cost; the borrow checker's learning curve is real (weeks to months) |
| Awkward patterns | Graphs with back-pointers, intrusive lists, arena/self-referential structures, and callback-heavy APIs need indices, `Rc<RefCell>`, or `unsafe` |
| Compile times | Comparable to heavy C++ template code; slower than Go |
| `unsafe` at the edges | FFI- and hardware-heavy code (driver ioctls, mmaped ring buffers) is largely `unsafe`, shrinking the benefit |

**A balanced conclusion you can say out loud:**

> "I would not rewrite a working C++ profiler in Rust. I would use Rust for new, well-isolated components where the safety payoff is high -- parsers of untrusted trace files, a network-facing collection daemon, a CLI -- behind a C ABI or `cxx` bridge, and keep kernels and tightly coupled runtime code in C++/HIP. In parallel I would harden the C++: sanitizers in CI, hardened standard library modes (`-D_GLIBCXX_ASSERTIONS`, libc++ hardening), `-Wdangling`/`lifetimebound`, clang-tidy, fuzzing, and C++26 features like erroneous behavior for uninitialized reads and standard library hardening as compilers support them. That gets most of the risk reduction at a fraction of the cost."

**"Why not Go?"** is easier: Go is excellent for services and tooling (Kubernetes operators, schedulers, telemetry pipelines in ML infra), but its GC, goroutine stacks that move (complicating C interop), cgo overhead, limited control over memory layout and SIMD, and lack of GPU programming support rule it out for runtimes, drivers, and kernels.

See also: [Undefined Behavior in C++](Cpp_Fundamentals.md#15-undefined-behavior-implementation-defined-and-best-practices), [Debugging and Profiling Tools](../tools/Debugging_and_Profiling_Tools.md), [Project Deep Dive](../career/Project_Deep_Dive_rocprof-compute.md).

---

# 19. Cross-Cutting Interview Q&A

**Q1.** Map `unique_ptr`, `shared_ptr`, `weak_ptr`, and raw pointers to Rust and Go.

`unique_ptr<T>` -> `Box<T>` (never null; `Option<Box<T>>` for nullable). `shared_ptr<T>` -> `Arc<T>` across threads or `Rc<T>` within one thread. `weak_ptr` -> `Weak<T>`. A non-owning raw pointer or reference -> `&T`/`&mut T` (checked) or `*const T`/`*mut T` (unchecked, `unsafe` to dereference). In Go every pointer is a GC-traced shared reference; there is no owning vs. non-owning distinction, and cycles are collected.

**Q2.** Is Rust's `Drop` the same as a C++ destructor? Any differences?

Same purpose (RAII), and locals drop in reverse declaration order as in C++. Differences: struct fields drop in **declaration** order (C++ destroys members in reverse order); drop runs only on values that were not moved out (tracked statically or by drop flags), never on moved-from husks; you cannot call `drop` methods directly (use `std::mem::drop(x)`, which just takes ownership); leaking is safe (`mem::forget`, `Rc` cycles), so `unsafe` code cannot rely on a destructor running for soundness (the "leakpocalypse" that removed the old scoped-thread API); and a type cannot be both `Copy` and `Drop`.

**Q3.** How does Go achieve memory safety without ownership, and what does it give up?

A tracing GC keeps every reachable object alive, bounds checks prevent overflow, there is no pointer arithmetic (outside `unsafe`), and escape analysis moves anything whose address outlives its frame to the heap. It gives up deterministic destruction (resources need `Close` + `defer`), predictable memory footprint (GC headroom), some CPU, and data-race safety -- Go programs with data races are memory-unsafe in edge cases (racy writes to interface values or slices can tear multi-word values).

**Q4.** Compare a goroutine, a `std::thread`, a C++20 coroutine, and a Rust `async` task.

`std::thread` is a kernel thread: ~8 MB virtual stack, ~10 µs or more to create and join, kernel-scheduled, good for CPU-bound parallelism with few threads. A goroutine is a runtime-scheduled green thread: 2 KB growable stack, sub-µs creation, preemptive M:N scheduling, can block in ordinary-looking code. C++20 coroutines and Rust `async fn` are stackless state machines: the frame holds only live variables across suspension points, they suspend only at `co_await`/`.await`, and they need an executor (Asio, folly, Tokio). Stackless is the most memory-efficient but "colors" functions (async vs sync); goroutines avoid coloring at the cost of a runtime.

**Q5.** What is a data race in each language, and what happens?

C++: concurrent conflicting non-atomic accesses -> undefined behavior; the optimizer may assume none exist. Rust: impossible in safe code; in `unsafe` code it is UB, as in C++. Go: the memory model makes most races on single-word values yield one of the written values, but races on multi-word values (strings, slices, interfaces) can produce torn values and memory corruption; the race detector finds them dynamically.

**Q6.** Why do `Rc` and `RefCell` exist if the borrow checker is supposed to handle everything?

The borrow checker enforces tree-shaped, statically-scoped ownership. Some designs are inherently graph-shaped or have lifetimes determined at run time (GUI widget trees with parent links, caches shared by callbacks, doubly-linked structures). `Rc` provides shared ownership with runtime counting; `RefCell` defers the aliasing check to runtime. They are explicit opt-ins, so the cost and the potential panic are visible in the types.

**Q7.** How would you explain lifetimes to a C++ developer in one sentence?

A lifetime is a compile-time name for "the region of code during which this reference must stay valid", and the compiler checks that every reference's region fits inside its referent's region -- the static version of what AddressSanitizer checks dynamically for stack-use-after-return.

**Q8.** What is the Go equivalent of RAII?

`defer`: `f, err := os.Open(p); if err != nil { return err }; defer f.Close()`. It is function-scoped, not block-scoped, and must be written at each acquisition site (no type-level guarantee), so forgetting it is a leak that only linters catch. `sync.Mutex` likewise uses `mu.Lock(); defer mu.Unlock()`. Finalizers and `runtime.AddCleanup` (Go 1.24) run at unpredictable times, if at all, and are not substitutes for `Close`.

**Q9.** How do traits, Go interfaces, and C++ concepts differ on "who declares conformance"?

C++ concepts and Go interfaces are structural: any type with the right operations/methods conforms, with no declaration (concepts at compile time, Go interfaces checked at compile time for static assignments and at run time for type assertions). Rust traits are nominal: conformance requires an explicit `impl Trait for Type`, which avoids accidental conformance (a `draw()` meaning "render" vs "draw a card") and enables coherence guarantees, at the cost of the orphan rule.

**Q10.** Your team wants to write a new trace-ingestion service. C++, Rust, or Go?

Frame it by requirements. If it is a network service parsing untrusted input with moderate latency goals and a team comfortable with cloud tooling, Go gives fast delivery, great observability (`pprof`), and a single static binary. If it needs C++-level throughput (multi-GB/s parsing), tight memory control, or will be embedded in the C++ profiler as a library, Rust gives safety on untrusted input with no GC, linked through a C ABI. C++ wins if it must share large amounts of code and types with the existing C++ runtime or call template-heavy C++ APIs directly. State the deciding factors explicitly rather than picking a favorite.

**Q11.** What does `Pin` solve, and what is the C++ analog?

`async` state machines can hold references into their own frame (a local borrowed across `.await`). Since Rust moves are memcpys, moving such a future would leave dangling internal pointers. `Pin<P>` promises the pointee will not move again until dropped, which makes self-references sound. C++ handles the same problem by making coroutine frames heap-allocated (non-movable) and by letting types delete or customize their move constructors.

**Q12.** Explain Go's minimal version selection and why it does not need a lockfile.

Each module lists the minimum versions of its dependencies. MVS selects, for every module, the highest of those minimums across the whole graph -- never a newer release that nobody asked for. Because the result depends only on the `go.mod` files (which are immutable once published and hash-verified by `go.sum`), the same build list is computed every time; upgrading is an explicit `go get` that edits `go.mod`. Cargo and npm instead pick the newest compatible versions and need a lockfile to freeze them.

**Q13.** A C++ engineer says "with smart pointers and sanitizers, modern C++ is as safe as Rust." How do you respond?

Modern C++ removes most leaks and many use-after-free bugs, and sanitizers catch bugs that tests execute. But dangling references (`string_view`, iterators, lambdas capturing by reference, `this` captured in async callbacks), iterator invalidation, data races, and integer/bounds errors remain expressible in idiomatic modern C++, and sanitizers only find what your tests hit (with 2-15x overhead, so not in production). Rust rejects those programs at compile time for all inputs. The fair conclusion: modern C++ plus tooling greatly reduces risk; it does not provide a guarantee, and the difference matters most for code handling untrusted input.
