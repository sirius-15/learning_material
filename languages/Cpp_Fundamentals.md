# C++ Fundamentals -- Comprehensive Reference

> A deep-dive reference covering every major C++ topic from core language mechanics to modern features. Each section includes conceptual explanations, comparison tables, code examples, and common interview questions with detailed answers. Complements the *CS Fundamentals*, *DSA Fundamentals*, and *LeetCode Patterns* guides.

---

## Table of Contents

### Part 1: Core Language

1. [Type System and Fundamentals](#1-type-system-and-fundamentals)
2. [Pointers, References, and Const Correctness](#2-pointers-references-and-const-correctness)
3. [Memory Management](#3-memory-management)
    - [3.7 Allocators and Custom Memory Management](#37-allocators-and-custom-memory-management) -- allocator model, `allocator_traits` and rebind, `std::pmr` resources, arena/bump allocators, class-specific `operator new`, aligned `new`, `std::launder`
    - [3.8 Production Allocators: tcmalloc, jemalloc, mimalloc](#38-production-allocators-tcmalloc-jemalloc-mimalloc)
4. [Object-Oriented Programming](#4-object-oriented-programming)
5. [Move Semantics and Perfect Forwarding](#5-move-semantics-and-perfect-forwarding)

### Part 2: Templates and Generic Programming

6. [Templates](#6-templates)

### Part 3: Standard Template Library

7. [STL Containers](#7-stl-containers)
    - [7.7 Container Internals](#77-container-internals) -- vector growth and amortized analysis, deque block map, node overheads, `unordered_map` buckets vs open addressing (`absl::flat_hash_map`), SSO, small vectors, introsort
8. [Iterators, Algorithms, and Lambdas](#8-iterators-algorithms-and-lambdas)
    - [8.2 Iterator Invalidation Rules](#82-iterator-invalidation-rules) -- iterators vs references/pointers, per container and operation

### Part 4: Modern C++ Features

9. [C++11/14 Features](#9-c1114-features)
10. [C++17 Features](#10-c17-features)
11. [C++20 Features](#11-c20-features)
    - [11.3 Coroutines](#113-coroutines) -- promise_type lifecycle, awaitables, frame allocation, symmetric transfer, `task<T>`, generator
    - [11.4 Modules](#114-modules) -- interface/implementation units, partitions, header units, `import std`, build-system support
    - [11.10 C++23 Features](#1110-c23-features) -- `std::expected`, `std::print`, `std::mdspan`, deducing `this`, `std::generator`, `if consteval`, `std::flat_map`, ranges additions

### Part 5: Concurrency

12. [Multithreading and Concurrency](#12-multithreading-and-concurrency)
    - [12.2 Mutexes](#122-mutexes) (incl. `std::shared_mutex` in depth) and [12.3 Condition Variables](#123-condition-variables) (incl. lost/spurious wakeup pitfalls)
    - [12.9 The C++ Memory Model](#129-the-c-memory-model) -- sequenced-before, synchronizes-with, happens-before, litmus tests, fences, `consume`
    - [12.10 Compare-and-Swap Loops](#1210-compare-and-swap-loops) -- weak vs strong, spurious failure, spinlocks
    - [12.11 Lock-Free Data Structures and Memory Reclamation](#1211-lock-free-data-structures-and-memory-reclamation) -- Treiber stack, ABA, hazard pointers, epochs, SPSC ring buffer
    - [12.12 C++20 Synchronization Primitives](#1212-c20-synchronization-primitives) -- `latch`, `barrier`, `counting_semaphore`, atomic wait/notify
    - [12.13 Once-Only Init, Lock Ordering, and Thread-Local Storage](#1213-once-only-init-lock-ordering-and-thread-local-storage)

### Part 6: Compilation and Runtime

13. [Compilation, Linking, and the Preprocessor](#13-compilation-linking-and-the-preprocessor)
    - [13.6 Object Files and ELF Sections](#136-object-files-and-elf-sections) -- `.text`/`.data`/`.bss`/`.rodata`, sections vs segments
    - [13.7 Symbols, Binding, and Weak Symbols](#137-symbols-binding-and-weak-symbols) -- symbol tables, resolution rules, COMDAT, weak hooks
    - [13.8 Position-Independent Code, the PLT/GOT, and Lazy Binding](#138-position-independent-code-the-pltgot-and-lazy-binding)
    - [13.9 Runtime Loading: dlopen and dlsym](#139-runtime-loading-dlopen-and-dlsym) -- plugins, static init across shared libraries
    - [13.10 Symbol Interposition and LD_PRELOAD](#1310-symbol-interposition-and-ld_preload) -- wrapping `malloc` and `hipMalloc`, how GPU profilers hook runtimes
    - [13.11 Symbol Visibility and Export Control](#1311-symbol-visibility-and-export-control) -- `-fvisibility=hidden`, export macros, version scripts
    - [13.12 Library Search Paths: RPATH, RUNPATH, and $ORIGIN](#1312-library-search-paths-rpath-runpath-and-origin)
    - [13.13 ABI Stability and the libstdc++ Dual ABI](#1313-abi-stability-and-the-libstdc-dual-abi) -- what breaks ABI, `_GLIBCXX_USE_CXX11_ABI`
    - [13.14 Calling Conventions and the System V x86-64 ABI](#1314-calling-conventions-and-the-system-v-x86-64-abi) -- argument and return registers, caller- vs callee-saved, red zone, struct classification, Windows x64 / AArch64 / syscall conventions
    - [13.15 Stack Frames: Prologue, Epilogue, and Unwinding](#1315-stack-frames-prologue-epilogue-and-unwinding) -- frame layout, canaries, `-fomit-frame-pointer` and CFI, tail calls, walking the `rbp` chain, stack size and overflow
    - [13.16 Process Virtual Address-Space Layout](#1316-process-virtual-address-space-layout) -- text/data/bss/heap/mmap/stack, `/proc/self/maps`, vDSO, TLS, ASLR
14. [Exception Handling and Error Management](#14-exception-handling-and-error-management)
15. [Undefined Behavior, Implementation-Defined, and Best Practices](#15-undefined-behavior-implementation-defined-and-best-practices)

### Part 7: Practice

16. [Implement-from-scratch Exercises](#16-implement-from-scratch-exercises) -- `unique_ptr`, `shared_ptr`/`weak_ptr` with a control block, `vector<T>` with the strong guarantee, a Rule-of-Five `String`, a bounded blocking queue, `std::function`-style type erasure, `any`

> **Practice:** test yourself with the 55 "what does this print?" puzzles in [C++ Output Quiz](../practice/Cpp_Output_Quiz.md), and the threading problems in [Concurrency Coding Problems](../computer-science/Concurrency_Coding_Problems.md). Tool-side companions: [Debugging and Profiling Tools](../tools/Debugging_and_Profiling_Tools.md) (gdb, perf, `nm`/`objdump`/`readelf`) and [CMake Fundamentals](../tools/CMake_Fundamentals.md).

---

# Part 1: Core Language

---

# 1. Type System and Fundamentals

---

## 1.1 Fundamental Types

C++ provides a rich set of built-in types. The standard guarantees **minimum** sizes, but exact sizes are implementation-defined. On most modern 64-bit platforms:

| Type | Typical Size | Minimum Range (Standard Guarantee) |
|---|---|---|
| `bool` | 1 byte | `true` / `false` |
| `char` | 1 byte | At least 8 bits; may be signed or unsigned |
| `signed char` | 1 byte | -128 to 127 |
| `unsigned char` | 1 byte | 0 to 255 |
| `short` | 2 bytes | -32,768 to 32,767 |
| `unsigned short` | 2 bytes | 0 to 65,535 |
| `int` | 4 bytes | At least 16 bits (typically 32) |
| `unsigned int` | 4 bytes | 0 to 4,294,967,295 |
| `long` | 4 or 8 bytes | At least 32 bits |
| `long long` | 8 bytes | At least 64 bits |
| `float` | 4 bytes | ~7 decimal digits precision (IEEE 754) |
| `double` | 8 bytes | ~15 decimal digits precision (IEEE 754) |
| `long double` | 8-16 bytes | At least as precise as `double` |

**Size guarantees from the standard:**

```
1 == sizeof(char) <= sizeof(short) <= sizeof(int) <= sizeof(long) <= sizeof(long long)
```

For exact-width types, use `<cstdint>`:

```cpp
#include <cstdint>
int8_t   a;   // exactly 8 bits
int16_t  b;   // exactly 16 bits
int32_t  c;   // exactly 32 bits
int64_t  d;   // exactly 64 bits
uint32_t e;   // exactly 32 bits, unsigned
size_t   f;   // unsigned, large enough to represent size of any object
ptrdiff_t g;  // signed, result of pointer subtraction
```

## 1.2 Type Modifiers

| Modifier | Effect |
|---|---|
| `signed` | Value can be negative (default for `int`, `short`, `long`, `long long`) |
| `unsigned` | Non-negative values only; doubles positive range |
| `short` | Reduces storage (at least 16 bits) |
| `long` | Increases storage (at least 32 bits) |
| `long long` | At least 64 bits (C++11) |

**Implicit conversion pitfall -- signed/unsigned mixing:**

```cpp
unsigned int u = 1;
int s = -1;
if (s < u) {
    // This branch is NOT taken!
    // s is implicitly converted to unsigned: (unsigned)-1 == 4294967295
    // So the comparison becomes: 4294967295 < 1 → false
}
```

## 1.3 `auto` and `decltype`

### `auto` -- Type Deduction from Initializer

`auto` deduces the type of a variable from its initializer. It follows template argument deduction rules, which means it **strips top-level `const` and references** by default:

```cpp
int x = 42;
const int& rx = x;

auto a = x;       // int          (copy, not reference)
auto b = rx;      // int          (const and & stripped)
auto& c = rx;     // const int&   (reference preserved, const follows)
const auto& d = x; // const int&
auto&& e = x;     // int&         (forwarding reference binds to lvalue)
auto&& f = 42;    // int&&        (forwarding reference binds to rvalue)
```

### `decltype` -- Type of an Expression

`decltype` inspects the declared type of an expression **without evaluating it**:

```cpp
int x = 0;
int& r = x;
const int cx = 0;

decltype(x)    a;   // int
decltype(r)    b;   // int&         (preserves reference)
decltype(cx)   c;   // const int    (preserves const)
decltype((x))  d;   // int&         (parenthesized lvalue → reference)
decltype(x+0)  e;   // int          (prvalue → no reference)
```

**Key difference:** `auto` strips references and top-level `const`; `decltype` preserves them exactly. `decltype(auto)` (C++14) gives the `decltype` semantics in variable declarations:

```cpp
int x = 0;
int& rx = x;

decltype(auto) a = rx;   // int& (preserves reference, unlike plain auto)
decltype(auto) b = (x);  // int& (parenthesized lvalue)
```

## 1.4 Type Casting

C++ provides four named cast operators, each with a distinct purpose. They replace the unsafe C-style cast `(Type)expr`.

| Cast | Purpose | Runtime Check | Compile-Time Check | Safe? |
|---|---|---|---|---|
| `static_cast<T>` | Well-defined conversions (numeric, up/down hierarchy) | No | Yes | Mostly |
| `dynamic_cast<T>` | Safe polymorphic downcast (requires virtual functions) | **Yes** (RTTI) | Partial | Yes |
| `const_cast<T>` | Add or remove `const` / `volatile` | No | Yes | Risky |
| `reinterpret_cast<T>` | Bit-level reinterpretation of pointer/reference types | No | Minimal | Dangerous |

### `static_cast`

Used for conversions the compiler can verify at compile time:

```cpp
double d = 3.14;
int i = static_cast<int>(d);          // 3 -- truncates decimal

Base* bp = new Derived();
Derived* dp = static_cast<Derived*>(bp); // downcast -- no runtime check
// Undefined behavior if bp does not actually point to a Derived

void* vp = static_cast<void*>(&i);    // any pointer → void*
int* ip = static_cast<int*>(vp);      // void* → original type
```

### `dynamic_cast`

Safe downcast using Run-Time Type Information (RTTI). The base class **must** have at least one virtual function:

```cpp
class Base { virtual ~Base() {} };
class Derived : public Base { };

Base* bp = new Derived();
Derived* dp = dynamic_cast<Derived*>(bp); // returns valid pointer

Base* bp2 = new Base();
Derived* dp2 = dynamic_cast<Derived*>(bp2); // returns nullptr (failed)

// With references: throws std::bad_cast on failure
try {
    Derived& dr = dynamic_cast<Derived&>(*bp2);
} catch (std::bad_cast& e) {
    // handle failure
}
```

### `const_cast`

Adds or removes `const` (or `volatile`). Modifying an originally `const` object through the result is **undefined behavior**:

```cpp
const int ci = 10;
int* p = const_cast<int*>(&ci);
*p = 20;  // UB! ci was declared const

void legacy_api(char* s);             // C API that doesn't modify s
const std::string str = "hello";
legacy_api(const_cast<char*>(str.c_str())); // OK if legacy_api truly doesn't write
```

### `reinterpret_cast`

Reinterprets the bit pattern. Almost no guarantees. Used for low-level operations:

```cpp
int i = 42;
int* p = &i;
uintptr_t addr = reinterpret_cast<uintptr_t>(p);  // pointer → integer
int* p2 = reinterpret_cast<int*>(addr);            // integer → pointer

// Type punning (usually UB -- prefer memcpy or std::bit_cast)
float f = 1.0f;
int bits = reinterpret_cast<int&>(f);  // technically UB (strict aliasing violation)
```

### C-Style Cast

A C-style cast `(Type)expr` tries each named cast in order: `const_cast`, `static_cast`, `static_cast` + `const_cast`, `reinterpret_cast`, `reinterpret_cast` + `const_cast`. It silently picks the first that succeeds, which makes it dangerous because you can't tell what it actually did:

```cpp
// Avoid in C++ -- use named casts instead
int* p = (int*)malloc(sizeof(int));          // reinterpret_cast
double d = (double)42;                       // static_cast
const int ci = 10; int* q = (int*)&ci;       // const_cast -- silent and dangerous
```

## 1.5 `typedef` vs `using`

Both create type aliases. `using` (C++11) is strictly more powerful because it works with templates:

```cpp
// Equivalent for simple aliases
typedef unsigned long ulong;
using ulong = unsigned long;

// Only 'using' supports template aliases
template <typename T>
using Vec = std::vector<T>;       // OK

// typedef cannot do this directly:
// template <typename T>
// typedef std::vector<T> Vec;    // ERROR
```

## 1.6 `enum` vs `enum class`

| Feature | `enum` (unscoped) | `enum class` (scoped, C++11) |
|---|---|---|
| Scope | Enumerators leak into enclosing scope | Enumerators scoped to enum name |
| Implicit conversion to `int` | Yes | No (requires `static_cast`) |
| Underlying type | Implementation-defined | `int` by default, can specify |
| Forward declaration | Only with explicit underlying type | Always allowed |

```cpp
// Unscoped enum -- pollutes namespace
enum Color { Red, Green, Blue };
int x = Red;  // OK, implicit conversion

// Scoped enum -- type-safe
enum class Direction : uint8_t { North, South, East, West };
// int y = Direction::North;                     // ERROR
int y = static_cast<int>(Direction::North);      // OK
Direction d = Direction::East;
```

---

## Common Interview Questions -- Type System

**Q: What is the difference between `static_cast` and `dynamic_cast`?**

`static_cast` performs compile-time checked conversions (numeric, known hierarchy traversals) with no runtime overhead, but does not verify the actual runtime type. `dynamic_cast` uses RTTI to verify at runtime that a downcast is valid; it returns `nullptr` (for pointers) or throws `std::bad_cast` (for references) on failure. `dynamic_cast` requires the base class to have at least one virtual function.

**Q: Why should you prefer `enum class` over `enum`?**

`enum class` provides type safety (no implicit conversion to integers), prevents name collisions (enumerators are scoped), and allows forward declaration without specifying an underlying type. It eliminates a whole class of bugs where enum values are accidentally compared across different enum types.

**Q: When does `auto` not deduce the type you might expect?**

`auto` strips top-level `const` and references: `auto x = cref;` where `cref` is `const int&` gives `int`, not `const int&`. Use `auto&`, `const auto&`, or `decltype(auto)` to preserve qualifiers. With braced-init-lists, `auto x = {1, 2, 3};` deduces `std::initializer_list<int>`, which is often surprising.

---

# 2. Pointers, References, and Const Correctness

---

## 2.1 Raw Pointers

A **pointer** stores the memory address of an object. It has its own address in memory and can be reassigned:

```
Variable:    int x = 42;
Memory:      ┌──────────┐
             │    42    │  ← address 0x1000
             └──────────┘
Pointer:     int* p = &x;
             ┌──────────┐
             │  0x1000  │  ← address 0x2000  (p stores x's address)
             └──────────┘
```

### Pointer Arithmetic

Pointer arithmetic operates in units of the pointed-to type's size:

```cpp
int arr[] = {10, 20, 30, 40, 50};
int* p = arr;        // points to arr[0]

*(p + 2);            // 30 -- advances by 2 * sizeof(int) bytes
p[3];                // 40 -- equivalent to *(p + 3)
p++;                 // now points to arr[1]

ptrdiff_t diff = &arr[4] - &arr[1];  // 3 (in elements, not bytes)
```

### Null Pointers: `nullptr` vs `NULL` vs `0`

| Expression | Type | Recommended? |
|---|---|---|
| `nullptr` | `std::nullptr_t` (C++11) | **Yes** |
| `NULL` | Macro, typically `0` or `((void*)0)` | No |
| `0` | `int` | No |

```cpp
void f(int);
void f(int*);

f(0);        // calls f(int)      -- ambiguous intent
f(NULL);     // calls f(int)      -- NULL is 0, same problem
f(nullptr);  // calls f(int*)     -- unambiguous
```

## 2.2 References

A **reference** is an alias for an existing object. It must be initialized on declaration and cannot be reseated:

```cpp
int x = 10;
int& r = x;     // r is an alias for x
r = 20;          // modifies x; x is now 20
// int& r2;     // ERROR: references must be initialized
```

### Lvalue References vs Rvalue References

| Aspect | Lvalue Reference (`T&`) | Rvalue Reference (`T&&`) |
|---|---|---|
| Binds to | Lvalues (named objects) | Rvalues (temporaries, `std::move` results) |
| Purpose | Aliasing, pass by reference | Move semantics, perfect forwarding |
| Extend lifetime? | `const T&` extends temporary lifetime | Yes, extends temporary lifetime |
| Introduced | C++98 | C++11 |

```cpp
int x = 42;
int& lr = x;          // OK: lvalue ref binds to lvalue
// int& lr2 = 42;     // ERROR: can't bind non-const lvalue ref to rvalue

const int& clr = 42;  // OK: const lvalue ref extends temporary lifetime

int&& rr = 42;        // OK: rvalue ref binds to rvalue
// int&& rr2 = x;     // ERROR: can't bind rvalue ref to lvalue
int&& rr3 = std::move(x);  // OK: std::move casts x to rvalue
```

### Pointer vs Reference Comparison

| Feature | Pointer | Reference |
|---|---|---|
| Can be null | Yes | No (must alias a valid object) |
| Can be reassigned | Yes | No (bound at initialization) |
| Has its own address | Yes (`&p` is the pointer's address) | No (acts as the object itself) |
| Levels of indirection | Multiple (`int**`) | Single only |
| Arithmetic | Supports pointer arithmetic | No arithmetic |
| Syntax for access | `*p` or `p->member` | Direct: `r` or `r.member` |
| Size | Platform pointer size (8 bytes on 64-bit) | Typically same (compiler may optimize away) |
| Use in containers | Yes (`vector<int*>`) | No (`vector<int&>` is illegal; use `reference_wrapper`) |

## 2.3 Const Correctness

`const` is a promise that a value will not be modified. The compiler enforces this promise.

### Const with Pointers -- Read Right to Left

```cpp
int x = 10;
const int* p1 = &x;        // pointer to const int     -- can't modify *p1
int const* p2 = &x;        // same as above (const int*)
int* const p3 = &x;        // const pointer to int     -- can't reassign p3
const int* const p4 = &x;  // const pointer to const int -- neither
```

**Mnemonic:** read the declaration **right to left**:
- `const int*` → "pointer to int that is const" → can't modify the int
- `int* const` → "const pointer to int" → can't change the pointer

### Const Member Functions

A `const` member function promises not to modify the object's state. It can be called on `const` objects:

```cpp
class Widget {
    int value_;
public:
    int getValue() const { return value_; }   // doesn't modify object
    void setValue(int v) { value_ = v; }       // modifies object

    // Can overload on const
    int& data() { return value_; }             // called on non-const Widget
    const int& data() const { return value_; } // called on const Widget
};

const Widget cw;
cw.getValue();   // OK
// cw.setValue(5); // ERROR: setValue is non-const

Widget w;
w.getValue();    // OK -- non-const object can call const methods
w.setValue(5);   // OK
```

### `mutable` Keyword

`mutable` allows a member to be modified even inside a `const` member function. Used for caches, mutexes, and other logically non-observable state:

```cpp
class CachedComputer {
    mutable int cache_ = -1;
    mutable bool cache_valid_ = false;

    int expensive_compute() const { /* ... */ return 42; }
public:
    int get() const {
        if (!cache_valid_) {
            cache_ = expensive_compute();  // OK: mutable
            cache_valid_ = true;
        }
        return cache_;
    }
};
```

## 2.4 `volatile`

`volatile` tells the compiler that a variable's value may change at any time (hardware register, signal handler, memory-mapped I/O) and should not be optimized away:

```cpp
volatile int* hardware_reg = reinterpret_cast<volatile int*>(0xFFFF0000);
int a = *hardware_reg;  // compiler must perform the read (no caching in register)
int b = *hardware_reg;  // compiler must read again (value may have changed)
```

`volatile` does **not** provide thread safety. For concurrent access, use `std::atomic`.

## 2.5 Function Pointers and `std::function`

### Function Pointers

```cpp
int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }

int (*op)(int, int) = &add;   // function pointer
int result = op(3, 4);         // 7
op = &sub;
result = op(3, 4);             // -1

// Typedef / using for readability
using BinaryOp = int(*)(int, int);
BinaryOp op2 = &add;
```

### Member Function Pointers

```cpp
class Calculator {
public:
    int multiply(int a, int b) { return a * b; }
};

int (Calculator::*mfp)(int, int) = &Calculator::multiply;
Calculator calc;
int r = (calc.*mfp)(3, 4);     // 12

Calculator* cp = &calc;
int r2 = (cp->*mfp)(5, 6);     // 30
```

### `std::function` -- Type-Erased Callable Wrapper

`std::function` wraps any callable (function, lambda, functor, member function) with a given signature. It uses type erasure internally, which involves heap allocation and virtual dispatch:

```cpp
#include <functional>

int add(int a, int b) { return a + b; }

std::function<int(int, int)> fn = add;             // function
fn = [](int a, int b) { return a * b; };           // lambda
fn = std::multiplies<int>{};                       // functor

struct Adder {
    int offset;
    int operator()(int a, int b) { return a + b + offset; }
};
fn = Adder{10};
fn(3, 4);  // 17
```

**Performance note:** `std::function` has overhead (heap allocation, virtual call). For hot paths, prefer templates or `auto` with lambdas.

---

## Common Interview Questions -- Pointers and References

**Q: What is the difference between a pointer and a reference?**

A pointer is a variable that stores a memory address. It can be null, reassigned, and supports arithmetic. A reference is an alias for an existing object. It must be initialized on creation, cannot be null, and cannot be reseated to refer to a different object. Under the hood, compilers typically implement references as pointers, but semantically they are distinct.

**Q: What does `const int* const p` mean?**

Reading right to left: `p` is a `const` pointer (the pointer itself cannot be reassigned) to a `const int` (the integer it points to cannot be modified through `p`). Neither `p = &other` nor `*p = 5` would compile.

**Q: Why use `nullptr` instead of `NULL`?**

`NULL` is typically defined as `0` (an `int`), which causes ambiguity in overload resolution (e.g., `f(int)` vs `f(int*)`). `nullptr` has its own type `std::nullptr_t` that converts to any pointer type but not to integers, eliminating the ambiguity.

**Q: Is `volatile` useful for multithreading?**

No. `volatile` prevents compiler optimizations on reads/writes but provides no atomicity or memory ordering guarantees. For multithreaded code, use `std::atomic` or synchronization primitives (`std::mutex`, etc.).

---

# 3. Memory Management

---

## 3.1 Memory Layout of a C++ Program

```
High Address ┌───────────────────────┐
             │     Command-line      │
             │   args & environment  │
             ├───────────────────────┤
             │                       │
             │        Stack          │  ← grows downward
             │   (local variables,   │    function frames,
             │    return addresses)  │    LIFO allocation
             │          │            │
             │          ▼            │
             │                       │
             │       (free)          │
             │                       │
             │          ▲            │
             │          │            │
             │        Heap           │  ← grows upward
             │  (dynamic allocation) │    new/malloc
             │                       │
             ├───────────────────────┤
             │   BSS (uninitialized  │  ← zero-initialized globals/statics
             │     global data)      │
             ├───────────────────────┤
             │   Data (initialized   │  ← globals/statics with initial values
             │     global data)      │
             ├───────────────────────┤
             │   Text (Code)         │  ← machine instructions, read-only
Low Address  └───────────────────────┘
```

| Segment | Contents | Lifetime | Growth |
|---|---|---|---|
| Text | Machine code, string literals | Entire program | Fixed |
| Data | Initialized global/static variables | Entire program | Fixed |
| BSS | Uninitialized global/static variables (zero-filled) | Entire program | Fixed |
| Heap | Dynamically allocated objects (`new`, `malloc`) | Until `delete`/`free` | Upward |
| Stack | Local variables, function parameters, return addresses | Function scope (automatic) | Downward |

This is the textbook picture. A real 64-bit Linux process also has shared libraries, thread stacks, `mmap`ed allocations, the vDSO, and TLS, all placed by ASLR: see [13.16 Process Virtual Address-Space Layout](#1316-process-virtual-address-space-layout), and [13.15](#1315-stack-frames-prologue-epilogue-and-unwinding) for what a single stack frame contains.

## 3.2 Stack vs Heap

| Aspect | Stack | Heap |
|---|---|---|
| Allocation speed | Extremely fast (pointer increment) | Slower (allocator bookkeeping) |
| Deallocation | Automatic when scope exits | Manual (`delete`/`free`) or smart pointer |
| Size | Limited (typically 1-8 MB) | Large (limited by virtual memory) |
| Fragmentation | None (LIFO) | Yes (over time) |
| Cache locality | Excellent (contiguous, hot in cache) | Poor (scattered addresses) |
| Thread safety | Each thread has its own stack | Shared; allocator needs synchronization |
| Lifetime control | Automatic (scope-based) | Programmer-controlled |

```cpp
void example() {
    int x = 10;                      // stack: automatic lifetime
    int* p = new int(20);            // heap: manual lifetime
    std::vector<int> v = {1, 2, 3};  // v is on stack; its internal buffer is on heap
    delete p;                        // must manually free
}   // x and v destroyed automatically; v's destructor frees internal buffer
```

## 3.3 `new`/`delete` vs `malloc`/`free`

| Feature | `new` / `delete` | `malloc` / `free` |
|---|---|---|
| Language | C++ operator | C library function |
| Type safety | Returns correct type (`T*`) | Returns `void*` (must cast) |
| Constructor/Destructor | Calls constructor / destructor | Does **not** call them |
| Overloadable | Yes (global and per-class) | No |
| Failure behavior | Throws `std::bad_alloc` (default) | Returns `NULL` |
| Size calculation | Automatic | Manual: `malloc(sizeof(T))` |
| Array form | `new T[n]` / `delete[] p` | Single interface |
| Reallocation | No built-in realloc | `realloc()` available |
| Header needed | None (built-in) | `<cstdlib>` |

```cpp
// C++ style
int* p = new int(42);           // allocate + initialize to 42
delete p;

int* arr = new int[100];       // allocate array
delete[] arr;                  // MUST use delete[] for arrays

// C style (avoid in C++ unless interfacing with C APIs)
int* q = static_cast<int*>(malloc(sizeof(int)));
if (q) { *q = 42; }
free(q);
```

**Critical rule:** Never mix `new` with `free`, or `malloc` with `delete`. Never use `delete` on an array allocated with `new[]` (use `delete[]`).

### Placement `new`

Constructs an object at a pre-allocated memory location:

```cpp
#include <new>

alignas(Widget) unsigned char buffer[sizeof(Widget)];
Widget* w = new (buffer) Widget(args...);  // construct in buffer
w->~Widget();                               // must manually call destructor
// do NOT call delete w -- memory was not allocated by new
```

## 3.4 Smart Pointers

Smart pointers (from `<memory>`) automate ownership and lifetime management, eliminating manual `delete`.

### `std::unique_ptr` -- Exclusive Ownership

A `unique_ptr` owns its resource exclusively. It cannot be copied, only moved:

```cpp
#include <memory>

auto p = std::make_unique<int>(42);    // preferred creation
std::unique_ptr<int> p2(new int(10));  // direct construction (less preferred)

// p2 = p;                             // ERROR: cannot copy
std::unique_ptr<int> p3 = std::move(p); // OK: transfer ownership
// p is now nullptr

// Custom deleter
auto file_deleter = [](FILE* f) { if (f) fclose(f); };
std::unique_ptr<FILE, decltype(file_deleter)> fp(fopen("data.txt", "r"), file_deleter);

// Arrays
auto arr = std::make_unique<int[]>(100);  // unique_ptr to array
arr[0] = 42;
```

**Overhead:** Zero. Same size and performance as a raw pointer (unless custom deleter has state).

### `std::shared_ptr` -- Shared Ownership

Multiple `shared_ptr`s can own the same resource. A reference count tracks owners. The resource is destroyed when the last `shared_ptr` is destroyed:

```cpp
auto sp1 = std::make_shared<Widget>(args...);  // preferred (single allocation)
std::shared_ptr<Widget> sp2 = sp1;              // copy: ref count → 2

sp1.reset();    // ref count → 1; resource still alive
sp2.reset();    // ref count → 0; Widget destroyed and memory freed

sp1.use_count(); // 0
```

**Internal structure of `shared_ptr`:**

```
shared_ptr sp1              Control Block               Object
┌──────────────┐           ┌─────────────────┐         ┌────────┐
│ ptr ─────────┼──────────►│ strong_count: 2 │         │ Widget │
│ ctrl_block ──┼──────►    │ weak_count:   1 │    ┌───►│  data  │
└──────────────┘           │ ptr ────────────┼────┘    └────────┘
                           │ deleter         │
shared_ptr sp2             │ allocator       │
┌──────────────┐           └─────────────────┘
│ ptr ─────────┼──────────────────────────────────────►
│ ctrl_block ──┼──────►
└──────────────┘
```

**Overhead:** Control block (typically 2 pointers + 2 atomic counters). `make_shared` allocates the control block and object together, improving cache locality and reducing allocations from 2 to 1.

### `std::weak_ptr` -- Non-Owning Observer

A `weak_ptr` observes a `shared_ptr`-managed resource without affecting its lifetime. Used to break circular references:

```cpp
auto sp = std::make_shared<Widget>();
std::weak_ptr<Widget> wp = sp;     // does NOT increment strong_count

if (auto locked = wp.lock()) {     // try to get shared_ptr
    // locked is a valid shared_ptr; object is alive
    locked->doSomething();
} else {
    // object has been destroyed
}

sp.reset();            // strong_count → 0; Widget destroyed
wp.expired();          // true
wp.lock();             // returns empty shared_ptr
```

**Circular reference problem:**

```cpp
struct Node {
    std::shared_ptr<Node> next;   // if A→B and B→A, neither is ever freed
    // Fix: use weak_ptr for back-pointers
    std::weak_ptr<Node> parent;
};
```

### Smart Pointer Comparison

| Feature | `unique_ptr` | `shared_ptr` | `weak_ptr` |
|---|---|---|---|
| Ownership | Exclusive | Shared (ref-counted) | None (observer) |
| Copyable | No | Yes | Yes |
| Movable | Yes | Yes | Yes |
| Overhead | Zero | Control block + atomic ops | Control block access |
| Thread-safe ref count | N/A | Yes (count is atomic) | Yes |
| Custom deleter | Template param (zero overhead) | Type-erased (stored in ctrl block) | N/A |
| Array support | `unique_ptr<T[]>` | `shared_ptr<T[]>` (C++17) | N/A |
| Use case | Default choice, sole ownership | Multiple owners needed | Break cycles, caches |

## 3.5 RAII (Resource Acquisition Is Initialization)

RAII ties resource lifetime to object lifetime: acquire in the constructor, release in the destructor. When the object goes out of scope, the destructor runs automatically and the resource is freed -- even if an exception is thrown.

```cpp
class FileHandle {
    FILE* fp_;
public:
    FileHandle(const char* path, const char* mode) : fp_(fopen(path, mode)) {
        if (!fp_) throw std::runtime_error("Cannot open file");
    }
    ~FileHandle() { if (fp_) fclose(fp_); }

    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;

    FILE* get() const { return fp_; }
};

void process() {
    FileHandle fh("data.txt", "r");   // resource acquired
    // ... use fh.get() ...
    // if an exception is thrown here, ~FileHandle() still runs
}   // fh destroyed → fclose called automatically
```

**RAII is the foundation of C++ resource management.** All standard library types (`vector`, `string`, `fstream`, smart pointers, lock guards) follow RAII.

## 3.6 Common Memory Pitfalls

| Bug | Description | Prevention |
|---|---|---|
| Memory leak | Allocated memory never freed | Use smart pointers, RAII |
| Dangling pointer | Pointer to freed memory | Don't return pointers to locals; use smart pointers |
| Double free | Freeing the same memory twice | Smart pointers; set raw pointers to `nullptr` after `delete` |
| Use-after-free | Accessing freed memory | Smart pointers, ASAN |
| Buffer overflow | Writing past array bounds | Use `std::vector`, bounds checking |
| Wild pointer | Using uninitialized pointer | Always initialize pointers |
| Mismatched new/delete | `new[]` with `delete`, or `new` with `free` | Consistent pairing; prefer smart pointers |

```cpp
// Dangling pointer
int* dangle() {
    int local = 42;
    return &local;      // local is destroyed after return → dangling!
}

// Double free
int* p = new int(10);
delete p;
delete p;               // UB: double free

// Use-after-free
std::vector<int> v = {1, 2, 3};
int& ref = v[0];
v.push_back(4);         // may reallocate → ref is dangling
ref = 10;               // UB
```

## 3.7 Allocators and Custom Memory Management

General-purpose `malloc`/`new` is a compromise. Its fast path (a thread-cache hit) costs tens of nanoseconds, but slow paths can cost microseconds: contention on an arena lock, `mmap`/`munmap` for large blocks, and page faults on first touch. It also cannot know your lifetimes, so it fragments and scatters related objects across memory. Custom allocation is worth it when you know something the allocator does not:

| You know that... | Technique | Example |
|---|---|---|
| Many objects die together (per frame, per request, per parse) | **Arena / bump** allocation, freed in O(1) with `reset()` | Compiler ASTs, per-kernel-dispatch metadata in a profiler |
| Objects are all the same size | **Pool / free list** | Tree and list nodes, network buffers |
| A hot path must never touch the heap | Stack buffer plus `monotonic_buffer_resource`, with `null_memory_resource` upstream | Real-time audio, trading, interrupt-like callbacks |
| Objects need special alignment or memory | Aligned `new`, a custom resource over `hipHostMalloc`/huge pages | Cache-line-padded counters, pinned host staging buffers |
| You want to measure allocation | A counting allocator or resource | Tests asserting "no allocation in this loop" |

### The Allocator Model: `std::allocator`, `allocator_traits`, and rebind

Every allocator-aware container (all except `std::array`) takes an `Allocator` template parameter and **never calls it directly**. It goes through `std::allocator_traits<Alloc>`, which supplies defaults for everything the allocator omits. A C++11 allocator therefore needs only five things:

| Member | Required? | Default supplied by `allocator_traits` |
|---|---|---|
| `value_type` | Yes | -- |
| `T* allocate(size_t n)` | Yes | -- |
| `void deallocate(T*, size_t n)` | Yes | -- |
| Converting constructor `Alloc(const Alloc<U>&)` | Yes (needed for rebind) | -- |
| `operator==` | Yes | -- |
| `pointer`, `size_type`, ... | No | `T*`, `size_t`, ... (fancy pointers such as offset pointers are possible) |
| `construct(p, args...)` / `destroy(p)` | No | Placement-`new` / `p->~T()` (C++20: `std::construct_at` / `std::destroy_at`) |
| `rebind_alloc<U>` | No | `Alloc<U, Rest...>` for `Alloc<T, Rest...>` templates |
| `propagate_on_container_copy_assignment` / `_move_assignment` / `_swap` | No | `false_type` |
| `is_always_equal` | No | `true` if the allocator class is empty |
| `select_on_container_copy_construction()` | No | Returns a copy of the allocator |

**Rebind** is why node containers work. `std::list<int, A<int>>` never allocates an `int`: it allocates `_List_node<int>` (prev + next + value). It obtains `A<_List_node<int>>` via `allocator_traits<A<int>>::rebind_alloc<_List_node<int>>`, constructed from the original with the converting constructor. The same happens for `map` (tree nodes) and `unordered_map` (nodes, plus the bucket array of node pointers).

```cpp
// tracking_allocator.cpp -- g++ -std=c++20 -Wall -Wextra tracking_allocator.cpp
#include <cstddef>
#include <cstdio>
#include <list>
#include <map>
#include <memory>
#include <new>
#include <type_traits>
#include <vector>

// The minimal C++11 allocator: value_type, allocate, deallocate, a converting
// constructor (for rebind) and ==. std::allocator_traits supplies the rest:
// pointer types, construct/destroy, rebind_alloc, propagate_on_* (= false), ...
template <class T>
struct TrackingAllocator {
    using value_type = T;
    std::size_t* live;                                    // stateful: points at a shared counter

    explicit TrackingAllocator(std::size_t* counter) noexcept : live(counter) {}
    template <class U>
    TrackingAllocator(const TrackingAllocator<U>& o) noexcept : live(o.live) {}   // rebind copy

    T* allocate(std::size_t n) {
        *live += n * sizeof(T);
        std::printf("  allocate %zu x %zu B\n", n, sizeof(T));
        return static_cast<T*>(::operator new(n * sizeof(T)));
    }
    void deallocate(T* p, std::size_t n) noexcept {
        *live -= n * sizeof(T);
        ::operator delete(p, n * sizeof(T));
    }
    template <class U>
    bool operator==(const TrackingAllocator<U>& o) const noexcept { return live == o.live; }
};

int main() {
    using A = TrackingAllocator<int>;
    using Traits = std::allocator_traits<A>;
    static_assert(std::is_same_v<Traits::pointer, int*>);
    static_assert(std::is_same_v<Traits::rebind_alloc<double>, TrackingAllocator<double>>);
    static_assert(!Traits::propagate_on_container_move_assignment::value);   // defaulted
    static_assert(!Traits::is_always_equal::value);       // non-empty class => may differ

    std::size_t live = 0;
    std::puts("vector<int>: allocates int arrays");
    {
        std::vector<int, A> v{A(&live)};
        for (int i = 0; i < 5; ++i) v.push_back(i);
    }
    std::puts("list<int>: allocator REBOUND to the node type (prev + next + int)");
    {
        std::list<int, A> l{A(&live)};
        l.push_back(1);
        l.push_back(2);
    }
    std::puts("map<int,int>: rebound to the red-black tree node");
    {
        using P = std::pair<const int, int>;
        std::map<int, int, std::less<>, TrackingAllocator<P>> m{TrackingAllocator<P>(&live)};
        m[1] = 10;
        std::printf("  live bytes with one entry: %zu\n", live);
    }
    std::printf("live bytes at end: %zu\n", live);
}
```

```text
vector<int>: allocates int arrays
  allocate 1 x 4 B
  allocate 2 x 4 B
  allocate 4 x 4 B
  allocate 8 x 4 B
list<int>: allocator REBOUND to the node type (prev + next + int)
  allocate 1 x 24 B
  allocate 1 x 24 B
map<int,int>: rebound to the red-black tree node
  allocate 1 x 40 B
  live bytes with one entry: 40
live bytes at end: 0
```

(GCC 15 / libstdc++, x86-64. The 40-byte map node is a 32-byte red-black header plus the 8-byte `pair<const int,int>`. See [7.7](#77-container-internals).)

**The problem with classic allocators: the allocator is part of the type.** `std::vector<int, ArenaAlloc<int>>` and `std::vector<int>` are different types. A function taking `const std::vector<int>&` cannot accept the arena version, so the allocator infects every interface. Stateful allocators also raise questions the propagation traits must answer. When you move-assign a container whose allocator compares unequal and `propagate_on_container_move_assignment` is false, the container cannot steal the buffer. It must allocate from its own allocator and move element by element, which is O(n) and may throw. `swap` with unequal, non-propagating allocators is undefined behavior.

### `std::pmr`: Polymorphic Memory Resources (C++17)

`<memory_resource>` solves the type problem with one runtime indirection. `std::pmr::polymorphic_allocator<T>` holds a `std::pmr::memory_resource*`, and the resource is an abstract class with three virtual functions: `do_allocate(bytes, align)`, `do_deallocate(p, bytes, align)`, and `do_is_equal(other)`. Every `std::pmr::vector<T>` has the **same type** (`std::vector<T, std::pmr::polymorphic_allocator<T>>`) whatever resource backs it.

| Resource | Behavior | Use it for |
|---|---|---|
| `new_delete_resource()` | Forwards to `::operator new`/`delete` | Default upstream |
| `null_memory_resource()` | Every allocation throws `std::bad_alloc` | Upstream that turns "accidental heap use" into a loud failure |
| `monotonic_buffer_resource` | Bump pointer into an initial buffer, then into geometrically growing chunks from upstream. `deallocate` is a **no-op**. Everything is freed by `release()` or the destructor | Short-lived, build-then-discard data: per request, per frame, parsing |
| `unsynchronized_pool_resource` | Pools of fixed-size blocks per size class, carved from upstream chunks. Freed blocks are reused. **Not thread-safe** | Long-lived, churny, single-threaded node containers |
| `synchronized_pool_resource` | The same with internal locking | Shared across threads |
| `get_default_resource()` / `set_default_resource()` | Process-wide default (initially `new_delete_resource()`) | Tests, or a global policy switch |

```cpp
// pmr_demo.cpp -- g++ -std=c++20 -Wall -Wextra pmr_demo.cpp
#include <array>
#include <cstddef>
#include <cstdio>
#include <memory_resource>
#include <new>
#include <string>
#include <vector>

// A memory_resource that counts and forwards to an upstream resource.
class CountingResource : public std::pmr::memory_resource {
public:
    explicit CountingResource(std::pmr::memory_resource* up = std::pmr::new_delete_resource())
        : up_(up) {}
    std::size_t allocs = 0, bytes = 0;
private:
    void* do_allocate(std::size_t n, std::size_t align) override {
        ++allocs; bytes += n;
        return up_->allocate(n, align);
    }
    void do_deallocate(void* p, std::size_t n, std::size_t align) override { up_->deallocate(p, n, align); }
    bool do_is_equal(const memory_resource& o) const noexcept override { return this == &o; }
    std::pmr::memory_resource* up_;
};

int main() {
    // 1) monotonic_buffer_resource: bump-pointer allocation from a stack buffer.
    //    deallocate() is a no-op; memory is reclaimed all at once by release()/destructor.
    alignas(std::max_align_t) std::array<std::byte, 4096> stack_buf;
    CountingResource heap;                                       // only used on overflow
    std::pmr::monotonic_buffer_resource arena(stack_buf.data(), stack_buf.size(), &heap);

    std::pmr::vector<std::pmr::string> names(&arena);            // "uses-allocator construction":
    names.reserve(8);                                            // each element string gets &arena too
    for (const char* s : {"SQ_WAVES", "SQ_INSTS_VALU", "TCC_HIT_sum_long_counter_name", "GRBM_GUI_ACTIVE"})
        names.emplace_back(s);
    std::printf("element uses arena: %s, heap allocs so far: %zu\n",
                names[2].get_allocator().resource() == &arena ? "yes" : "no", heap.allocs);

    std::pmr::vector<int> big(&arena);
    big.resize(2000);                                            // 8000 B > what is left -> upstream
    std::printf("after overflow: heap allocs=%zu bytes=%zu\n", heap.allocs, heap.bytes);

    // GOTCHA: copy construction does NOT propagate the resource (select_on_container_copy_construction
    // returns a default polymorphic_allocator -> get_default_resource(), normally new/delete).
    std::pmr::vector<std::pmr::string> copy = names;
    std::printf("copy uses default resource: %s\n",
                copy.get_allocator().resource() == std::pmr::get_default_resource() ? "yes" : "no");

    // 2) unsynchronized_pool_resource: per-size-class pools carved from upstream chunks;
    //    freed blocks are REUSED (unlike monotonic). Single-threaded; synchronized_pool_resource
    //    is the thread-safe variant.
    CountingResource up2;
    {
        std::pmr::unsynchronized_pool_resource pool(&up2);
        for (int round = 0; round < 1000; ++round) {
            std::pmr::vector<int> tmp(&pool);
            tmp.resize(16);                                      // same size class every round
        }
        std::printf("pool: 1000 vectors -> upstream allocs=%zu\n", up2.allocs);
    }

    // 3) null_memory_resource as upstream: a hard "no heap on this path" guarantee.
    alignas(std::max_align_t) std::array<std::byte, 256> tiny;
    std::pmr::monotonic_buffer_resource strict(tiny.data(), tiny.size(), std::pmr::null_memory_resource());
    std::pmr::vector<int> v(&strict);
    try {
        v.resize(1000);
    } catch (const std::bad_alloc&) {
        std::puts("strict arena exhausted -> std::bad_alloc (no silent heap fallback)");
    }
}
```

```text
element uses arena: yes, heap allocs so far: 0
after overflow: heap allocs=1 bytes=8064
copy uses default resource: yes
pool: 1000 vectors -> upstream allocs=3
strict arena exhausted -> std::bad_alloc (no silent heap fallback)
```

PMR pitfalls interviewers probe:

- **Lifetime.** The resource must outlive every container that uses it. A `pmr::vector` returned from a function whose local `monotonic_buffer_resource` has died is a use-after-free.
- **Copies do not propagate.** `polymorphic_allocator` has all `propagate_on_*` traits false, and copy construction picks the *default* resource, as shown. Pass the resource explicitly: `std::pmr::vector<T> copy(src, &arena);`.
- **Monotonic plus growth wastes memory.** A `vector` that doubles inside a monotonic resource leaves every old buffer allocated until `release()`, roughly 2x the final size. `reserve` first, or use a pool resource.
- **Virtual-call cost.** Each allocation is an indirect call. That is negligible next to `malloc`, but the allocator is no longer inlinable, unlike a template allocator.
- **Nested containers.** `pmr::vector<std::string>` (non-pmr string) silently puts every string's heap buffer on the global heap. Use `pmr::string` so uses-allocator construction passes the resource down.

### Arena Allocators, Class-Specific `operator new`, Aligned `new`, and `std::launder`

```cpp
// custom_new.cpp -- g++ -std=c++20 -Wall -Wextra custom_new.cpp
#include <cassert>
#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <memory>
#include <new>
#include <utility>
#include <vector>

// ---------- 1. Bump (arena) allocator ----------
class Arena {
public:
    static constexpr std::align_val_t kBufAlign{64};             // 64-aligned base => deterministic padding
    explicit Arena(std::size_t cap)
        : buf_(static_cast<std::byte*>(::operator new(cap, kBufAlign))), cap_(cap) {}  // throws bad_alloc
    ~Arena() { ::operator delete(buf_, kBufAlign); }
    Arena(const Arena&) = delete;
    Arena& operator=(const Arena&) = delete;

    void* allocate(std::size_t n, std::size_t align = alignof(std::max_align_t)) {
        auto base = reinterpret_cast<std::uintptr_t>(buf_);
        std::uintptr_t p = base + used_;
        p = (p + align - 1) & ~std::uintptr_t(align - 1);         // round up (align = power of 2)
        if (p - base + n > cap_) throw std::bad_alloc();
        used_ = p - base + n;
        return reinterpret_cast<void*>(p);
    }
    template <class T, class... Args>
    T* make(Args&&... args) {                                     // caller destroys non-trivial T
        return ::new (allocate(sizeof(T), alignof(T))) T(std::forward<Args>(args)...);
    }
    void reset() noexcept { used_ = 0; }                          // O(1) "free everything"
    std::size_t used() const noexcept { return used_; }

private:
    std::byte* buf_;
    std::size_t cap_;
    std::size_t used_ = 0;
};

// ---------- 2. Class-specific operator new/delete: a free-list for one node type ----------
struct TreeNode final {
    int key;
    TreeNode* left = nullptr;
    TreeNode* right = nullptr;
    explicit TreeNode(int k) : key(k) {}

    static void* operator new(std::size_t sz) {                  // implicitly static
        ++class_news;
        if (sz == sizeof(TreeNode) && free_list) {
            void* p = free_list;
            free_list = free_list->next;
            ++reused;
            return p;
        }
        return ::operator new(sz);
    }
    static void operator delete(void* p, std::size_t sz) noexcept {   // sized form
        if (sz != sizeof(TreeNode)) { ::operator delete(p); return; }
        auto* f = static_cast<FreeSlot*>(p);                        // reuse the dead object's bytes
        f->next = free_list;
        free_list = f;
    }

    struct FreeSlot { FreeSlot* next; };
    static inline FreeSlot* free_list = nullptr;                    // not thread-safe; never returned to OS
    static inline int class_news = 0, reused = 0;
};

// ---------- 3. Over-aligned type (C++17 aligned new) ----------
struct alignas(64) PerThreadCounter { std::uint64_t value = 0; };   // one per cache line

// ---------- 4. std::launder ----------
struct Sample { const int id; double v; };

int main() {
    Arena arena(1 << 16);
    auto* a = arena.make<int>(7);
    auto* line = arena.make<PerThreadCounter>();
    assert(*a == 7 && reinterpret_cast<std::uintptr_t>(line) % 64 == 0);
    std::printf("arena used after int + 64B-aligned counter: %zu bytes\n", arena.used());
    arena.reset();                                                // both gone (trivial dtors)

    for (int i = 0; i < 3; ++i) { auto* n = new TreeNode(i); delete n; }
    std::printf("TreeNode: class operator new calls=%d, reused from free list=%d\n",
                TreeNode::class_news, TreeNode::reused);

    auto sp = std::make_shared<TreeNode>(42);                     // GOTCHA: bypasses TreeNode::operator new
    std::printf("after make_shared: class operator new calls=%d (unchanged)\n", TreeNode::class_news);

    std::printf("__STDCPP_DEFAULT_NEW_ALIGNMENT__ = %zu\n", std::size_t{__STDCPP_DEFAULT_NEW_ALIGNMENT__});
    auto* counters = new PerThreadCounter[4];                     // -> operator new[](size, align_val_t{64})
    assert(reinterpret_cast<std::uintptr_t>(counters) % 64 == 0);
    delete[] counters;                                            // -> matching aligned delete[]
    std::vector<PerThreadCounter> vc(8);                          // std::allocator honours it too (C++17)
    assert(reinterpret_cast<std::uintptr_t>(vc.data()) % 64 == 0);

    alignas(Sample) std::byte storage[sizeof(Sample)];
    Sample* s1 = ::new (storage) Sample{1, 0.5};
    s1->~Sample();
    ::new (storage) Sample{2, 1.5};                               // reuse the storage
    // A pointer obtained by casting the BYTE buffer does not point to the Sample object;
    // std::launder produces a pointer that does. (Or simply keep placement-new's return value.)
    Sample* s2 = std::launder(reinterpret_cast<Sample*>(storage));
    std::printf("relaunched sample id=%d\n", s2->id);
    s2->~Sample();
}
```

```text
arena used after int + 64B-aligned counter: 128 bytes
TreeNode: class operator new calls=3, reused from free list=2
after make_shared: class operator new calls=3 (unchanged)
__STDCPP_DEFAULT_NEW_ALIGNMENT__ = 16
relaunched sample id=2
```

What each part demonstrates:

1. **Arena (bump) allocator.** Allocation is "round the cursor up to the alignment, add n". That is a handful of instructions with no per-object header and no free. Objects allocated together sit together in memory, which helps the cache, and `reset()` frees everything in O(1). The costs: you cannot free individual objects, destructors do not run unless you call them (keep arenas for trivially destructible data or track destructors yourself), and the arena has a fixed lifetime. The int plus the 64-byte-aligned counter used 128 bytes because the cursor was rounded up from offset 4 to offset 64 (the buffer itself is 64-aligned). The arena aligns *absolute* addresses, so with a plain `std::malloc` buffer (only 16-byte aligned) the padding would depend on `base % 64` and the total could be anywhere from 80 to 128 bytes. `std::pmr::monotonic_buffer_resource` is the standard version.
2. **Class-specific `operator new`/`delete`** are implicitly `static` members, found by `new T` before the global ones. A free list reuses the dead object's own bytes as the "next" link, which needs no extra memory. Rules: also provide the matching `operator delete` (the sized form receives `sizeof(T)`). Handle `sz != sizeof(T)`, which happens when a derived class inherits the operator (here prevented with `final`). Add `operator new[]` if arrays are needed. Note that `::new T` (qualified) skips the class version.
3. **`std::make_shared` bypasses class-specific `operator new`.** It allocates one block for the control block plus the object with `std::allocator` and constructs `T` by placement-new inside it. Use `std::allocate_shared` with an allocator to control that allocation.
4. **Aligned `new` (C++17).** If `alignof(T) > __STDCPP_DEFAULT_NEW_ALIGNMENT__` (16 on x86-64 Linux), `new T` calls `operator new(std::size_t, std::align_val_t)`, and `delete` calls the matching aligned overload. Before C++17, `new` of an `alignas(64)` type silently returned 16-byte-aligned memory, which broke false-sharing padding and AVX-512 aligned loads. `std::allocator<T>` follows the same rule. For raw memory use `std::aligned_alloc(align, size)` (size must be a multiple of align, free with `std::free`) or `posix_memalign`.
5. **`std::launder` (C++17).** If you placement-new an object into storage, the pointer returned by `new` is the one that points to the object. A pointer obtained some other way, such as `reinterpret_cast<T*>(byte_buffer)`, points to the bytes, and the compiler may assume it does not alias the new object. `std::launder` returns a pointer to the object that now lives at that address. In practice you need it in hand-written `optional`/`variant`/small-buffer storage that re-derives `T*` from the buffer (see [16.6](#166-functionsig-type-erasure-with-small-buffer-optimization)). Before C++20 it was also needed after replacing an object that has `const` or reference members, even through the old pointer. C++20 relaxed that rule, but laundering the buffer pointer is still required.

**`operator new` overload map.** Replaceable global: `operator new(size_t)`, `new[]`, the `nothrow_t` forms, the `align_val_t` forms (C++17), and sized `operator delete(void*, size_t)` (C++14). Not replaceable: placement `operator new(size_t, void*)`. Defining the replaceable ones in your executable replaces them process-wide, including calls from inside `libstdc++.so`. That works by symbol interposition ([13.10](#1310-symbol-interposition-and-ld_preload)).

## 3.8 Production Allocators: tcmalloc, jemalloc, mimalloc

| Allocator | Core design | Strengths | Watch out for |
|---|---|---|---|
| **glibc ptmalloc2** (default on Linux) | Multiple arenas (up to 8 x cores on 64-bit), each with bins and a lock. A per-thread **tcache** (glibc 2.26+) holds by default up to 7 chunks per size class for requests up to about 1 KiB (`glibc.malloc.tcache_count` / `tcache_max`; glibc 2.42 allows raising the max to 4 MiB). Large requests (default threshold 128 KiB, adaptive) use `mmap` | Always there, decent general performance | RSS bloat with many threads (many arenas), and fragmentation that is never returned to the OS. Tune with `MALLOC_ARENA_MAX`, `glibc.malloc.*` tunables, and `malloc_trim` |
| **tcmalloc** (Google; current version in `google/tcmalloc`, older one in gperftools) | Size classes. Per-**CPU** caches using restartable sequences (`rseq`, Linux) in the current version, per-thread caches in gperftools. Central free lists, page heap | Very fast small allocations, low lock contention, sampling heap profiler | The per-CPU mode needs a recent kernel. Memory release is tunable |
| **jemalloc** (FreeBSD, Meta; Rust's default allocator until 1.32) | Threads assigned to arenas round-robin, thread caches, size classes, extent-based large allocations, background purge threads | Low fragmentation for long-running servers, rich stats and heap profiling (`MALLOC_CONF=prof:true`) | Many tuning knobs. Decay settings trade RSS against CPU |
| **mimalloc** (Microsoft) | Free-list *sharding*: per-page free lists, separate lists for local and cross-thread frees, segments per thread | Small and fast, good locality, easy drop-in | Cross-thread free patterns behave differently from the others |

How to swap without code changes: `LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so.2 ./app` (this works because `malloc`/`free`/`operator new` are interposable, see [13.10](#1310-symbol-interposition-and-ld_preload)), or link with `-ljemalloc` / `-ltcmalloc` / `-lmimalloc`. Always A/B test with the real workload: compare p50/p99 latency **and** peak RSS.

**GPU-side analogue.** `hipMalloc` and `hipFree` are expensive: they can synchronize the device and take milliseconds. The first call also pays runtime initialization (80 ms in the [13.10](#1310-symbol-interposition-and-ld_preload) run). Frameworks therefore put a **caching allocator** on top: PyTorch's CUDA/HIP caching allocator keeps freed blocks per stream and splits and coalesces them, the same idea as a pool resource. HIP also offers stream-ordered `hipMallocAsync` with memory pools. See [Parallel GPU Programming](../ml-gpu/Parallel_GPU_Programming.md) and [ML Systems Design](../ml-gpu/ML_Systems_Design.md).

> **See also:** [Object Pool and Resource Pools](../design-patterns/Design_Patterns_Cpp.md#46-object-pool-and-resource-pools) · [Memory hierarchy programming](../computer-science/Performance_Engineering.md#5-memory-hierarchy-programming) · [Heap profilers: Valgrind, heaptrack, jemalloc prof](../tools/Debugging_and_Profiling_Tools.md#14-valgrind-sanitizers-and-heap-profilers)

---

## Common Interview Questions -- Memory Management

**Q: What is RAII and why is it important?**

RAII binds the lifetime of a resource (memory, file handle, lock, socket) to the lifetime of an object. The resource is acquired in the constructor and released in the destructor, which runs automatically when the object goes out of scope. This guarantees cleanup even when exceptions are thrown, making code both leak-free and exception-safe without manual cleanup logic.

**Q: When should you use `shared_ptr` vs `unique_ptr`?**

Default to `unique_ptr` -- it has zero overhead and expresses exclusive ownership clearly. Use `shared_ptr` only when ownership genuinely needs to be shared among multiple owners whose lifetimes are not hierarchically nested. Common `shared_ptr` use cases: shared caches, observer patterns, and objects whose lifetime is managed by multiple independent subsystems.

**Q: What does `make_shared` do differently from `shared_ptr<T>(new T(...))`?**

`make_shared<T>(args...)` performs a single memory allocation for both the object and the control block (reference counts), improving cache locality and reducing allocation overhead. `shared_ptr<T>(new T(...))` performs two separate allocations. `make_shared` is also exception-safe in complex expressions. The downside is that `make_shared` keeps the object's memory allocated until all `weak_ptr`s are also destroyed (since the control block and object share the same allocation).

**Q: How does `shared_ptr` reference counting work with threads?**

The reference count itself is an `std::atomic` integer, so incrementing/decrementing the count (copying/destroying `shared_ptr`s) is thread-safe. However, the pointed-to object is **not** automatically thread-safe -- concurrent reads/writes to the managed object still require explicit synchronization.

### Advanced Questions -- Allocators and Memory Resources

**Q1.** You pass `MyAlloc<int>` to `std::list<int, MyAlloc<int>>`, but your logging shows `MyAlloc` allocating 24-byte objects, never 4-byte ints. Why?

The list never stores a bare `int`. It allocates nodes holding prev, next, and the value. The container *rebinds* the allocator with `std::allocator_traits<MyAlloc<int>>::rebind_alloc<Node>`, which by default is `MyAlloc<Node>`, built through your converting constructor `template<class U> MyAlloc(const MyAlloc<U>&)`. That is why the converting constructor is mandatory and why a stateful allocator's state must be shareable across rebound copies (store a pointer to the shared state, not the state itself). `map` rebinds to tree nodes. `unordered_map` rebinds twice: to nodes and to the bucket array of node pointers.

**Q2.** What do `propagate_on_container_move_assignment` and `is_always_equal` control, and what goes wrong with stateful allocators?

They decide whether the allocator follows the data. If `a = std::move(b)` and POCMA is true, `a` takes `b`'s allocator and steals the buffer in O(1). If POCMA is false and `a.get_allocator() != b.get_allocator()`, `a` cannot free memory that came from `b`'s allocator, so it must allocate its own buffer and move the elements one by one. That is O(n), may throw, and is why such move assignments are not `noexcept`. `is_always_equal` (true for empty allocators like `std::allocator`) lets the library skip the comparison. `swap` with non-propagating, unequal allocators is undefined behavior. `polymorphic_allocator` has every propagate trait false, so in a pmr world memory never silently migrates between resources. The price is O(n) moves across resources and copies that land on the default resource unless you pass one.

**Q3.** When would you choose `monotonic_buffer_resource` over `unsynchronized_pool_resource`, and how can monotonic blow up memory?

Monotonic suits "allocate a lot, then drop everything": building a per-request response, a per-frame scene graph, or parsing one file. Allocation is a pointer bump, and individual `deallocate` calls are no-ops, so memory only goes back on `release()` or destruction. That is also its failure mode. Anything that frees and reallocates inside it leaks until the end: a growing `vector` leaves each old buffer behind, about 2x the final size in total, and a long-lived map with churn grows without bound. Pool resources keep per-size free lists and reuse freed blocks, which fits long-lived node containers with insert/erase churn. They cost more per operation and are not thread-safe unless you use the `synchronized_` variant. A common production pattern is one pool or monotonic resource per thread or per request, which needs no locks and has no cross-thread frees.

**Q4.** What did `new` do for an `alignas(64)` struct before C++17, and what does it do now?

Before C++17, `new T` called `operator new(sizeof(T))`, which guarantees only `alignof(std::max_align_t)` (16 on x86-64). The `alignas(64)` was silently ignored on the heap, which broke padding meant to avoid false sharing and crashed aligned SIMD loads (`_mm512_load_ps`). C++17 added `operator new(std::size_t, std::align_val_t)`. When `alignof(T) > __STDCPP_DEFAULT_NEW_ALIGNMENT__`, the compiler calls the aligned overload, and `delete` the matching aligned `operator delete`. `std::allocator<T>` does the same, so `std::vector<alignas(64) type>` is correctly aligned. Follow-up: a custom allocator must handle this itself by checking `alignof(T)` and calling the aligned overload, as the [16.3 Vector](#163-vectort-placement-new-growth-and-the-strong-guarantee) solution does.

**Q5.** When is `std::launder` actually required?

When you have a pointer whose *value* is the right address but which was not obtained from the expression that created the object. The typical case is `reinterpret_cast<T*>(&buffer)` in an `optional`/`variant`/small-buffer implementation after a placement-new into `buffer`. The cast yields a pointer to the byte array, and the compiler may reason that it does not point to the `T` (for example, it may cache an earlier value of a `const` member). `std::launder(p)` is an optimization barrier that returns a pointer to the object living at that address. Before C++20 it was also required when reusing storage of an object with `const` or reference members even through the original pointer. C++20 relaxed that. The simplest way to avoid it is to keep the pointer returned by placement new. You do not need `launder` for objects returned by `new`, or for pointers that stay within one object's lifetime.

**Q6.** A service's RSS grows for days, but ASan, Valgrind, and heaptrack all report no leak. What is going on, and what do you try?

Likely causes: (1) **Fragmentation**: freed chunks are scattered among live ones, so the allocator cannot return whole pages. (2) **Per-thread arenas** in glibc: each of many threads gets its own arena (up to 8 x cores), each holding free memory. (3) **Caches that are logically leaking**: a map that only grows, which a leak checker sees as reachable. (4) The allocator holding freed memory by design (thread caches, delayed purge). Diagnosis: `malloc_stats()`/`malloc_info()`, jemalloc `stats.print`, heaptrack's "peak consumption" view, and comparing `RssAnon` against the live heap. Fixes: `MALLOC_ARENA_MAX=2` to `4`, periodic `malloc_trim(0)`, switching to jemalloc or tcmalloc (A/B via `LD_PRELOAD`), arena allocation for request-scoped data so it dies all at once, and size-bounded caches.

**Q7.** Why does `std::make_shared<T>()` ignore `T::operator new`, and why might you still prefer `std::shared_ptr<T>(new T)`?

`make_shared` makes one allocation holding both the control block and the `T`, using `std::allocator` (or your allocator for `allocate_shared`), and placement-constructs `T` inside it. `T::operator new` is never consulted. The single allocation is usually better (one `malloc`, better locality). Prefer `shared_ptr<T>(new T)` when (a) the class's `operator new` must be used (a pool, special memory), (b) `T` is large and `weak_ptr`s may outlive the last `shared_ptr` by a long time. With `make_shared`, the object's memory is released only when the *control block* dies, which requires the weak count to reach zero as well. Or (c) you need a custom deleter.

---

# 4. Object-Oriented Programming

---

## 4.1 Classes vs Structs

In C++, `class` and `struct` are almost identical. The **only** difference is the default access level:

| Feature | `struct` | `class` |
|---|---|---|
| Default member access | `public` | `private` |
| Default inheritance | `public` | `private` |

```cpp
struct Point {
    int x, y;             // public by default
};

class Point2 {
    int x, y;             // private by default
public:
    Point2(int x, int y) : x(x), y(y) {}
};
```

Convention: use `struct` for plain data aggregates (POD-like types) and `class` for types with invariants, encapsulation, or complex behavior.

## 4.2 Constructors

### Types of Constructors

```cpp
class Widget {
    int id_;
    std::string name_;
public:
    // Default constructor
    Widget() : id_(0), name_("default") {}

    // Parameterized constructor
    Widget(int id, std::string name) : id_(id), name_(std::move(name)) {}

    // Copy constructor
    Widget(const Widget& other) : id_(other.id_), name_(other.name_) {}

    // Move constructor
    Widget(Widget&& other) noexcept
        : id_(other.id_), name_(std::move(other.name_)) {
        other.id_ = 0;
    }

    // Delegating constructor (C++11) -- calls another constructor
    Widget(int id) : Widget(id, "unnamed") {}
};
```

### Member Initializer List

Members are initialized in the **order they are declared** in the class, not the order in the initializer list. Always match the list order to the declaration order to avoid subtle bugs:

```cpp
class Danger {
    int b_;
    int a_;   // declared after b_
public:
    Danger(int val) : a_(val), b_(a_) {}
    // BUG: b_ is initialized first (declaration order), but a_ isn't set yet
    // b_ gets garbage value
};
```

### `explicit` Keyword

Prevents implicit conversions and copy-initialization:

```cpp
class Meter {
public:
    explicit Meter(double val) : val_(val) {}
private:
    double val_;
};

Meter m1(5.0);          // OK: direct initialization
// Meter m2 = 5.0;      // ERROR: implicit conversion blocked by explicit
// void f(Meter m);
// f(5.0);              // ERROR: implicit conversion blocked
```

**Rule of thumb:** mark single-argument constructors `explicit` unless implicit conversion is intentionally desired.

## 4.3 Destructors

The destructor `~ClassName()` is called when an object's lifetime ends. It should release resources and is invoked in the reverse order of construction:

```cpp
class Resource {
    int* data_;
public:
    Resource() : data_(new int[100]) {}
    ~Resource() { delete[] data_; }   // cleanup
};

// Order of destruction
class A { public: ~A() { std::cout << "~A\n"; } };
class B { public: ~B() { std::cout << "~B\n"; } };

class Composite {
    A a_;    // destroyed second (reverse order)
    B b_;    // destroyed first
public:
    ~Composite() { std::cout << "~Composite\n"; }
};
// Output: ~Composite  ~B  ~A
```

### Virtual Destructors

If a class is intended to be used as a base class with polymorphic deletion, its destructor **must** be `virtual`. Otherwise, deleting a derived object through a base pointer causes **undefined behavior**:

```cpp
class Base {
public:
    virtual ~Base() = default;  // MUST be virtual for polymorphic types
};

class Derived : public Base {
    std::vector<int> data_;
};

Base* bp = new Derived();
delete bp;   // Without virtual destructor: ~Derived() is NOT called → leak
             // With virtual destructor: ~Derived() then ~Base() → correct
```

**Guideline:** If a class has any virtual function, give it a virtual destructor.

## 4.4 Copy Semantics

### Copy Constructor and Copy Assignment

```cpp
class Buffer {
    size_t size_;
    int* data_;
public:
    Buffer(size_t size) : size_(size), data_(new int[size]) {}

    // Copy constructor -- deep copy
    Buffer(const Buffer& other) : size_(other.size_), data_(new int[other.size_]) {
        std::copy(other.data_, other.data_ + size_, data_);
    }

    // Copy assignment -- deep copy with self-assignment check
    Buffer& operator=(const Buffer& other) {
        if (this != &other) {
            delete[] data_;
            size_ = other.size_;
            data_ = new int[size_];
            std::copy(other.data_, other.data_ + size_, data_);
        }
        return *this;
    }

    ~Buffer() { delete[] data_; }
};
```

### Copy-and-Swap Idiom

A safer, exception-safe implementation of copy assignment using a swap:

```cpp
class Buffer {
    size_t size_;
    int* data_;
public:
    Buffer(size_t size) : size_(size), data_(new int[size]) {}
    Buffer(const Buffer& other) : size_(other.size_), data_(new int[other.size_]) {
        std::copy(other.data_, other.data_ + size_, data_);
    }
    ~Buffer() { delete[] data_; }

    friend void swap(Buffer& a, Buffer& b) noexcept {
        using std::swap;
        swap(a.size_, b.size_);
        swap(a.data_, b.data_);
    }

    Buffer& operator=(Buffer other) {  // pass by value (copy made here)
        swap(*this, other);             // swap with the copy
        return *this;                   // old data destroyed with 'other'
    }
};
```

## 4.5 The Rule of Zero / Three / Five

| Rule | When | What to Define |
|---|---|---|
| **Rule of Zero** | Class manages no resources directly | Define none -- use smart pointers and standard containers |
| **Rule of Three** | Class manages a resource (pre-C++11) | Destructor + Copy Constructor + Copy Assignment Operator |
| **Rule of Five** | Class manages a resource (C++11+) | Rule of Three + Move Constructor + Move Assignment Operator |

```cpp
// Rule of Zero -- preferred when possible
class Employee {
    std::string name_;
    std::vector<int> scores_;
    // Compiler-generated special members do the right thing
};

// Rule of Five -- needed when managing raw resources
class Buffer {
    size_t size_;
    int* data_;
public:
    Buffer(size_t s) : size_(s), data_(new int[s]) {}
    ~Buffer() { delete[] data_; }                                      // 1. Destructor
    Buffer(const Buffer& o) : size_(o.size_), data_(new int[o.size_]) { // 2. Copy ctor
        std::copy(o.data_, o.data_ + size_, data_);
    }
    Buffer& operator=(const Buffer& o) {                               // 3. Copy assign
        if (this != &o) { Buffer tmp(o); swap(*this, tmp); }
        return *this;
    }
    Buffer(Buffer&& o) noexcept : size_(o.size_), data_(o.data_) {    // 4. Move ctor
        o.size_ = 0; o.data_ = nullptr;
    }
    Buffer& operator=(Buffer&& o) noexcept {                          // 5. Move assign
        if (this != &o) { delete[] data_; size_ = o.size_; data_ = o.data_; o.size_ = 0; o.data_ = nullptr; }
        return *this;
    }
    friend void swap(Buffer& a, Buffer& b) noexcept {
        using std::swap; swap(a.size_, b.size_); swap(a.data_, b.data_);
    }
};
```

## 4.6 Inheritance

### Single Inheritance

```cpp
class Animal {
protected:
    std::string name_;
public:
    Animal(std::string name) : name_(std::move(name)) {}
    virtual std::string speak() const { return "..."; }
    virtual ~Animal() = default;
};

class Dog : public Animal {
public:
    Dog(std::string name) : Animal(std::move(name)) {}
    std::string speak() const override { return name_ + " says Woof!"; }
};
```

### Access Specifiers and Inheritance

| Base Member Access | `public` Inheritance | `protected` Inheritance | `private` Inheritance |
|---|---|---|---|
| `public` | `public` | `protected` | `private` |
| `protected` | `protected` | `protected` | `private` |
| `private` | Not accessible | Not accessible | Not accessible |

### Multiple Inheritance and the Diamond Problem

```
        Animal
       /      \
   Mammal    WingedAnimal
       \      /
         Bat
```

Without `virtual` inheritance, `Bat` contains **two copies** of `Animal`'s subobject, causing ambiguity:

```cpp
class Animal {
public:
    int age;
};

class Mammal : public Animal {};         // has its own Animal subobject
class WingedAnimal : public Animal {};   // has its own Animal subobject

class Bat : public Mammal, public WingedAnimal {};

Bat b;
// b.age = 5;   // ERROR: ambiguous -- which Animal::age?
b.Mammal::age = 5;        // OK: explicit qualification
b.WingedAnimal::age = 10; // OK: different copy

// Fix with virtual inheritance:
class Mammal : virtual public Animal {};
class WingedAnimal : virtual public Animal {};
class Bat : public Mammal, public WingedAnimal {};

Bat b2;
b2.age = 5;  // OK: single shared Animal subobject
```

**Virtual inheritance** ensures a single shared base subobject. The most-derived class is responsible for calling the virtual base's constructor.

## 4.7 Polymorphism

### Compile-Time Polymorphism (Static)

Resolved at compile time through **function overloading** and **templates**:

```cpp
// Function overloading
int area(int side) { return side * side; }
double area(double radius) { return 3.14159 * radius * radius; }
int area(int length, int width) { return length * width; }

// Templates
template <typename T>
T max(T a, T b) { return (a > b) ? a : b; }
```

### Runtime Polymorphism (Dynamic)

Resolved at runtime through **virtual functions** and **base class pointers/references**:

```cpp
class Shape {
public:
    virtual double area() const = 0;   // pure virtual
    virtual ~Shape() = default;
};

class Circle : public Shape {
    double radius_;
public:
    Circle(double r) : radius_(r) {}
    double area() const override { return 3.14159 * radius_ * radius_; }
};

class Rectangle : public Shape {
    double w_, h_;
public:
    Rectangle(double w, double h) : w_(w), h_(h) {}
    double area() const override { return w_ * h_; }
};

void print_area(const Shape& s) {
    std::cout << s.area() << "\n";   // calls the correct override at runtime
}
```

## 4.8 Virtual Function Table (vtable) Internals

When a class has virtual functions, the compiler creates a **vtable** (virtual function table) -- a static array of function pointers. Each object of that class contains a hidden **vptr** (virtual pointer) that points to the class's vtable:

```
                      Circle vtable
                    ┌──────────────────────┐
                    │ &Circle::area        │ slot 0
Object (Circle)     │ &Circle::~Circle     │ slot 1
┌────────────┐      └──────────────────────┘
│ vptr ──────┼──────►
│ radius_    │         Rectangle vtable
└────────────┘      ┌──────────────────────┐
                    │ &Rectangle::area     │ slot 0
Object (Rectangle)  │ &Rectangle::~Rectangle│ slot 1
┌────────────┐      └──────────────────────┘
│ vptr ──────┼──────►
│ w_         │
│ h_         │
└────────────┘
```

**How a virtual call works:**

```cpp
Shape* s = new Circle(5.0);
s->area();
// 1. Compiler loads s->vptr
// 2. Looks up vtable[slot_for_area]  → finds &Circle::area
// 3. Calls Circle::area(s)
```

**Cost of virtual functions:**
- Extra indirection per call (vptr → vtable → function)
- Prevents inlining (compiler generally cannot inline virtual calls through base pointers)
- Each object carries one vptr (typically 8 bytes on 64-bit)
- One vtable per class (static, shared among all instances)

## 4.9 Abstract Classes and Pure Virtual Functions

A class with at least one pure virtual function is **abstract** and cannot be instantiated:

```cpp
class Shape {
public:
    virtual double area() const = 0;     // pure virtual → Shape is abstract
    virtual double perimeter() const = 0;
    virtual ~Shape() = default;
};

// Shape s;  // ERROR: cannot instantiate abstract class

class Circle : public Shape {
    double r_;
public:
    Circle(double r) : r_(r) {}
    double area() const override { return 3.14159 * r_ * r_; }
    double perimeter() const override { return 2 * 3.14159 * r_; }
};
```

An abstract class serves as an **interface** defining a contract that derived classes must fulfill.

## 4.10 Operator Overloading

### Rules and Guidelines

| Guideline | Details |
|---|---|
| Cannot create new operators | Only overload existing C++ operators |
| Cannot change arity | Unary stays unary, binary stays binary |
| Cannot overload `::`, `.`, `.*`, `?:` | These four are never overloadable |
| Preserve semantics | `+` should mean addition-like behavior |
| Return types | `+` returns by value; `+=` returns `*this` by reference |
| Symmetry | If you overload `==`, also overload `!=` (pre-C++20) |

```cpp
class Vec2 {
    double x_, y_;
public:
    Vec2(double x, double y) : x_(x), y_(y) {}

    // Member: compound assignment
    Vec2& operator+=(const Vec2& rhs) {
        x_ += rhs.x_; y_ += rhs.y_;
        return *this;
    }

    // Non-member friend: binary arithmetic
    friend Vec2 operator+(Vec2 lhs, const Vec2& rhs) {
        return lhs += rhs;
    }

    // Non-member friend: equality
    friend bool operator==(const Vec2& a, const Vec2& b) {
        return a.x_ == b.x_ && a.y_ == b.y_;
    }
    friend bool operator!=(const Vec2& a, const Vec2& b) {
        return !(a == b);
    }

    // Stream output
    friend std::ostream& operator<<(std::ostream& os, const Vec2& v) {
        return os << "(" << v.x_ << ", " << v.y_ << ")";
    }

    // Subscript
    double& operator[](int idx) { return idx == 0 ? x_ : y_; }
    const double& operator[](int idx) const { return idx == 0 ? x_ : y_; }

    // Function call (functor)
    double operator()(double scale) const { return x_ * scale + y_ * scale; }
};
```

## 4.11 `friend` Functions and Classes

A `friend` declaration grants a non-member function or another class access to private and protected members:

```cpp
class Matrix {
    std::vector<std::vector<double>> data_;
    friend Matrix operator*(const Matrix& a, const Matrix& b);
    friend class MatrixSerializer;  // entire class has access
};
```

Use sparingly. `friend` breaks encapsulation intentionally and should be limited to tightly coupled collaborators like operators and serializers.

---

## Common Interview Questions -- OOP

**Q: What is the difference between `class` and `struct` in C++?**

The only technical difference is the default access level: `struct` defaults to `public`, `class` defaults to `private`. This applies both to member access and inheritance. By convention, `struct` is used for simple aggregates and `class` for types with encapsulation.

**Q: Why should base class destructors be virtual?**

When you delete a derived object through a base pointer (`Base* p = new Derived(); delete p;`), if the base destructor is not virtual, only `~Base()` is called, skipping `~Derived()`. This leaks any resources managed by the derived class and is technically undefined behavior. A virtual destructor ensures the correct destructor chain is called.

**Q: What is the diamond problem and how do you solve it?**

The diamond problem occurs in multiple inheritance when two base classes inherit from the same grandparent. Without virtual inheritance, the most-derived class contains two copies of the grandparent subobject, causing ambiguity. Virtual inheritance (`class B : virtual public A`) ensures a single shared copy of the grandparent, eliminating the ambiguity.

**Q: Explain the Rule of Five.**

If a class manages a resource (raw pointer, file handle), you should explicitly define five special member functions: destructor, copy constructor, copy assignment operator, move constructor, and move assignment operator. If you define any one of these, the compiler's implicit generation of the others becomes unreliable, so you should define all five (or explicitly `= default` / `= delete` them).

**Q: What is object slicing?**

When a derived object is assigned or copied to a base object by value, the derived part is "sliced off":

```cpp
Derived d;
Base b = d;  // slicing: only Base part is copied; Derived data is lost
b.virtualMethod();  // calls Base::virtualMethod, NOT Derived::
```

Always use pointers or references for polymorphic behavior.

---

# 5. Move Semantics and Perfect Forwarding

---

## 5.1 Value Categories

Every C++ expression has a **value category** that determines whether it can be moved from:

```
               expression
              /          \
          glvalue       rvalue
         /      \      /     \
      lvalue   xvalue      prvalue
```

| Category | Has Identity? | Can Be Moved? | Examples |
|---|---|---|---|
| **lvalue** | Yes | No (unless cast) | Named variable `x`, `*ptr`, `arr[0]`, string literal |
| **prvalue** | No | Yes | `42`, `x + y`, `std::string("hi")`, function returning by value |
| **xvalue** | Yes | Yes | `std::move(x)`, `static_cast<T&&>(x)`, member of an rvalue |
| **glvalue** | Yes | - | lvalue or xvalue |
| **rvalue** | - | Yes | prvalue or xvalue |

**Practical rule:** If it has a name, it's an lvalue (even if declared as `T&&`):

```cpp
void f(Widget&& w) {
    // w has a name → w is an lvalue!
    // To treat it as an rvalue again, use std::move(w)
    g(std::move(w));
}
```

## 5.2 Move Constructor and Move Assignment

Move operations **steal** resources from a source object instead of copying, leaving the source in a valid-but-unspecified state:

```cpp
class Buffer {
    size_t size_;
    int* data_;
public:
    // Move constructor
    Buffer(Buffer&& other) noexcept
        : size_(other.size_), data_(other.data_) {
        other.size_ = 0;
        other.data_ = nullptr;   // source must be left in a destructible state
    }

    // Move assignment
    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            delete[] data_;       // release current resource
            size_ = other.size_;
            data_ = other.data_;
            other.size_ = 0;
            other.data_ = nullptr;
        }
        return *this;
    }
};
```

**Performance comparison -- copying vs moving a vector of 1 million elements:**

| Operation | Time | Work Done |
|---|---|---|
| Copy | O(n) | Allocate new buffer, copy all elements |
| Move | O(1) | Swap three pointers (data, size, capacity) |

## 5.3 `std::move`

`std::move` does **not** move anything. It is an unconditional cast to an rvalue reference:

```cpp
// Simplified implementation
template <typename T>
constexpr std::remove_reference_t<T>&& move(T&& t) noexcept {
    return static_cast<std::remove_reference_t<T>&&>(t);
}
```

It enables a move by making the expression an rvalue, which allows move constructors/assignment operators to be selected by overload resolution:

```cpp
std::string a = "hello";
std::string b = std::move(a);  // calls string's move constructor
// a is now in a valid-but-unspecified state (likely empty)
```

**Key insight:** After `std::move`, do not use the source object except to assign to it or destroy it.

## 5.4 `std::forward` and Perfect Forwarding

`std::forward` preserves the value category of a forwarding (universal) reference argument. It is a **conditional** cast -- it casts to rvalue only if the argument was originally an rvalue:

```cpp
template <typename T>
void wrapper(T&& arg) {
    // Without forward: arg is always an lvalue (it has a name)
    // With forward: preserves original value category
    target(std::forward<T>(arg));
}

Widget w;
wrapper(w);             // T = Widget&,  forwards as lvalue
wrapper(Widget{});      // T = Widget,   forwards as rvalue
wrapper(std::move(w));  // T = Widget,   forwards as rvalue
```

**Reference collapsing rules** (what makes forwarding references work):

| Template Param `T` | `T&&` Becomes | Explanation |
|---|---|---|
| `Widget&` | `Widget& &&` → `Widget&` | & + && = & |
| `Widget&&` | `Widget&& &&` → `Widget&&` | && + && = && |
| `Widget` | `Widget&&` | Plain rvalue reference |

**Rule:** Any `&` in the collapse produces `&`. Only `&&` + `&&` produces `&&`.

## 5.5 Return Value Optimization (RVO) and Named RVO (NRVO)

The compiler is allowed (and in C++17, **required** for prvalues) to construct the return value directly in the caller's memory, eliminating copy/move entirely:

```cpp
Widget createWidget() {
    return Widget(args...);    // RVO: constructed directly in caller's variable
}
Widget w = createWidget();     // no copy, no move (guaranteed in C++17)

Widget createNamed() {
    Widget w(args...);
    // ... modify w ...
    return w;                  // NRVO: compiler may elide the copy/move
}
Widget w2 = createNamed();     // usually no copy/move, but not guaranteed
```

| Optimization | When | Guaranteed? |
|---|---|---|
| RVO (unnamed return) | `return Widget(...)` | Yes (C++17 mandatory copy elision) |
| NRVO (named return) | `return local_variable` | No (but almost always applied) |

**Do not write `return std::move(local);`** -- this *prevents* NRVO because it changes the return type from `Widget` to `Widget&&`, disabling the optimization.

## 5.6 When Moves Happen Implicitly

Moves are selected automatically in these situations:

1. **Returning a local variable:** `return local;` -- compiler first tries move, then copy
2. **Throwing a local variable:** `throw local;` -- same as return
3. **Initializing from a temporary:** `Widget w = Widget(...)` -- move (or elision)
4. **Passing a temporary to a function:** `f(Widget(...))` -- move
5. **Inserting into containers:** `vec.push_back(Widget(...))` -- move
6. **After explicit `std::move`:** `vec.push_back(std::move(w))` -- move

```cpp
std::vector<std::string> strs;
std::string s = "hello world";

strs.push_back(s);              // copies s (s is an lvalue)
strs.push_back(std::move(s));   // moves s (s is now empty)
strs.push_back("temporary");    // moves (string literal → temporary string → move)
strs.emplace_back("in-place");  // constructs directly in vector (no move needed)
```

---

## Common Interview Questions -- Move Semantics

**Q: What does `std::move` actually do?**

`std::move` performs an unconditional `static_cast` to an rvalue reference (`T&&`). It doesn't move anything -- it just signals that the object may be moved from. The actual move happens when a move constructor or move assignment operator accepts the resulting rvalue reference.

**Q: What is the difference between `std::move` and `std::forward`?**

`std::move` unconditionally casts to `T&&` (always produces an rvalue). `std::forward<T>` conditionally casts: it forwards lvalues as lvalues and rvalues as rvalues, based on how the template parameter `T` was deduced. Use `std::move` when you know you want to move; use `std::forward` in templates to perfectly forward arguments.

**Q: Why should move constructors be `noexcept`?**

STL containers (e.g., `std::vector` during reallocation) will only use move constructors if they are `noexcept`. If the move constructor might throw, the container falls back to copying to maintain the strong exception guarantee. Marking moves `noexcept` enables significant performance gains.

**Q: What state is a moved-from object in?**

The standard requires moved-from objects to be in a "valid but unspecified" state. You can safely destroy them or assign new values to them, but you should not rely on their contents. For standard library types, this typically means an empty or default state (e.g., a moved-from `std::string` is empty, a moved-from `std::vector` has size 0).

---

# Part 2: Templates and Generic Programming

---

# 6. Templates

---

## 6.1 Function Templates

A function template defines a family of functions parameterized by one or more types:

```cpp
template <typename T>
T max_val(T a, T b) {
    return (a > b) ? a : b;
}

max_val(3, 7);           // T = int (deduced)
max_val(3.14, 2.72);     // T = double (deduced)
max_val<std::string>("a", "b");  // T = std::string (explicit)
```

### Template Argument Deduction

The compiler deduces template arguments from function arguments. Deduction does **not** perform implicit conversions (except array/function-to-pointer decay and top-level `const` addition):

```cpp
template <typename T>
T max_val(T a, T b);

max_val(3, 7);       // OK: T = int
// max_val(3, 7.0);  // ERROR: T deduced as both int and double
max_val<double>(3, 7.0);  // OK: explicit template argument
```

## 6.2 Class Templates

```cpp
template <typename T, size_t N>
class FixedArray {
    T data_[N];
public:
    T& operator[](size_t i) { return data_[i]; }
    const T& operator[](size_t i) const { return data_[i]; }
    constexpr size_t size() const { return N; }
};

FixedArray<int, 10> arr;      // array of 10 ints
FixedArray<double, 5> darr;   // array of 5 doubles
```

### Variable Templates (C++14)

```cpp
template <typename T>
constexpr T pi = T(3.14159265358979323846L);

double d = pi<double>;   // 3.14159265358979...
float f = pi<float>;     // 3.14159f
```

## 6.3 Template Specialization

### Full (Explicit) Specialization

Provides a completely different implementation for specific types:

```cpp
template <typename T>
struct Serializer {
    static std::string serialize(const T& val) {
        return std::to_string(val);  // generic: works for numeric types
    }
};

// Full specialization for std::string
template <>
struct Serializer<std::string> {
    static std::string serialize(const std::string& val) {
        return "\"" + val + "\"";    // wrap strings in quotes
    }
};

Serializer<int>::serialize(42);              // "42"
Serializer<std::string>::serialize("hello"); // "\"hello\""
```

### Partial Specialization (Class Templates Only)

Specializes for a subset of template parameters:

```cpp
// Primary template
template <typename T, typename U>
struct Pair {
    T first;
    U second;
};

// Partial specialization: both types are the same
template <typename T>
struct Pair<T, T> {
    T first, second;
    T sum() const { return first + second; }  // only available when types match
};

// Partial specialization: second type is a pointer
template <typename T, typename U>
struct Pair<T, U*> {
    T first;
    U* second;
    U deref() const { return *second; }
};
```

**Note:** Function templates cannot be partially specialized -- use overloading or `if constexpr` instead.

## 6.4 Non-Type Template Parameters

Templates can accept compile-time constant values, not just types:

```cpp
template <typename T, int Rows, int Cols>
class Matrix {
    T data_[Rows][Cols];
public:
    static constexpr int rows = Rows;
    static constexpr int cols = Cols;

    T& operator()(int r, int c) { return data_[r][c]; }
};

Matrix<double, 3, 3> m;  // 3×3 matrix of doubles, all sizes known at compile time
```

Allowed non-type parameter types: integers, enums, pointers, references, `auto` (C++17), floating-point (C++20), and literal class types (C++20).

## 6.5 Variadic Templates

Accept any number of template parameters using parameter packs:

```cpp
// Base case
template <typename T>
T sum(T value) {
    return value;
}

// Recursive expansion
template <typename T, typename... Args>
T sum(T first, Args... rest) {
    return first + sum(rest...);
}

sum(1, 2, 3, 4, 5);  // 15
```

### Fold Expressions (C++17)

Simplify variadic template operations without recursion:

```cpp
// Unary right fold: (pack op ...)
template <typename... Args>
auto sum(Args... args) {
    return (args + ...);    // ((a1 + a2) + a3) + ...
}

// Unary left fold: (... op pack)
template <typename... Args>
auto sum_left(Args... args) {
    return (... + args);    // a1 + (a2 + (a3 + ...))
}

// Binary fold with init value: (init op ... op pack)
template <typename... Args>
void print_all(Args... args) {
    (std::cout << ... << args) << "\n";  // cout << a1 << a2 << a3 ...
}

// Fold with comma operator: apply function to each
template <typename F, typename... Args>
void for_each_arg(F f, Args&&... args) {
    (f(std::forward<Args>(args)), ...);
}
```

| Fold Type | Syntax | Expansion |
|---|---|---|
| Unary right fold | `(pack op ...)` | `(a1 op (a2 op (... op aN)))` |
| Unary left fold | `(... op pack)` | `(((a1 op a2) op ...) op aN)` |
| Binary right fold | `(pack op ... op init)` | `(a1 op (a2 op (... op (aN op init))))` |
| Binary left fold | `(init op ... op pack)` | `((((init op a1) op a2) op ...) op aN)` |

## 6.6 SFINAE (Substitution Failure Is Not An Error)

When substituting template arguments causes an invalid type, the template is silently removed from the overload set rather than causing a compilation error:

```cpp
#include <type_traits>

// Only enabled for integral types
template <typename T>
std::enable_if_t<std::is_integral_v<T>, T>
double_val(T x) {
    return x * 2;
}

// Only enabled for floating-point types
template <typename T>
std::enable_if_t<std::is_floating_point_v<T>, T>
double_val(T x) {
    return x * 2.0;
}

double_val(5);     // calls integral version
double_val(3.14);  // calls floating-point version
// double_val("hi"); // ERROR: no matching overload
```

### `void_t` Trick (C++17)

Detect whether a type has certain properties:

```cpp
// Detect if T has a .size() method
template <typename, typename = void>
struct has_size : std::false_type {};

template <typename T>
struct has_size<T, std::void_t<decltype(std::declval<T>().size())>>
    : std::true_type {};

static_assert(has_size<std::vector<int>>::value);  // true
static_assert(!has_size<int>::value);               // true
```

## 6.7 `if constexpr` (C++17)

Compile-time `if` that discards the false branch entirely:

```cpp
template <typename T>
auto get_value(T t) {
    if constexpr (std::is_pointer_v<T>) {
        return *t;           // only compiled when T is a pointer
    } else {
        return t;            // only compiled when T is not a pointer
    }
}

int x = 42;
get_value(&x);   // returns 42 (dereferences pointer)
get_value(x);    // returns 42 (returns directly)
```

This replaces many SFINAE patterns with cleaner syntax.

## 6.8 Concepts (C++20)

Concepts provide readable, first-class constraints on template parameters:

```cpp
#include <concepts>

// Define a concept
template <typename T>
concept Arithmetic = std::is_arithmetic_v<T>;

template <typename T>
concept Printable = requires(T t) {
    { std::cout << t } -> std::convertible_to<std::ostream&>;
};

template <typename T>
concept Hashable = requires(T t) {
    { std::hash<T>{}(t) } -> std::convertible_to<std::size_t>;
};

// Use concepts as constraints
template <Arithmetic T>
T add(T a, T b) { return a + b; }

// Equivalent syntaxes:
auto multiply(Arithmetic auto a, Arithmetic auto b) { return a * b; }

template <typename T>
    requires Arithmetic<T>
T subtract(T a, T b) { return a - b; }

// Combining constraints
template <typename T>
    requires Arithmetic<T> && Printable<T>
void compute_and_print(T a, T b) {
    std::cout << (a + b) << "\n";
}
```

### Standard Library Concepts (`<concepts>`)

| Concept | Meaning |
|---|---|
| `std::same_as<T, U>` | `T` and `U` are the same type |
| `std::derived_from<D, B>` | `D` is derived from `B` |
| `std::convertible_to<From, To>` | `From` converts to `To` |
| `std::integral<T>` | `T` is an integral type |
| `std::floating_point<T>` | `T` is a floating-point type |
| `std::default_initializable<T>` | `T` is default constructible |
| `std::copyable<T>` | `T` is copy constructible and assignable |
| `std::movable<T>` | `T` is move constructible and assignable |
| `std::equality_comparable<T>` | `T` supports `==` and `!=` |
| `std::totally_ordered<T>` | `T` supports `<`, `<=`, `>`, `>=` |
| `std::invocable<F, Args...>` | `F` is callable with `Args...` |

## 6.9 CRTP (Curiously Recurring Template Pattern)

A class derives from a template instantiated with itself as the template argument. Achieves static polymorphism (no vtable overhead):

```cpp
template <typename Derived>
class Comparable {
public:
    bool operator>(const Derived& other) const {
        return other < static_cast<const Derived&>(*this);
    }
    bool operator<=(const Derived& other) const {
        return !(static_cast<const Derived&>(*this) > other);
    }
    bool operator>=(const Derived& other) const {
        return !(static_cast<const Derived&>(*this) < other);
    }
};

class Temperature : public Comparable<Temperature> {
    double degrees_;
public:
    Temperature(double d) : degrees_(d) {}
    bool operator<(const Temperature& other) const {
        return degrees_ < other.degrees_;
    }
};

Temperature t1(20), t2(30);
t1 < t2;   // true -- defined in Temperature
t1 > t2;   // false -- generated by CRTP base
t1 <= t2;  // true -- generated by CRTP base
```

**Use cases:** static polymorphism, mixin classes (adding shared functionality), compile-time interface enforcement.

## 6.10 Template Metaprogramming

Templates are Turing-complete -- computation at compile time:

```cpp
// Compile-time factorial
template <int N>
struct Factorial {
    static constexpr int value = N * Factorial<N - 1>::value;
};
template <>
struct Factorial<0> {
    static constexpr int value = 1;
};

static_assert(Factorial<5>::value == 120);

// Modern alternative: constexpr (preferred)
constexpr int factorial(int n) {
    return n <= 1 ? 1 : n * factorial(n - 1);
}
static_assert(factorial(5) == 120);
```

### Common Type Traits (`<type_traits>`)

| Trait | Checks For |
|---|---|
| `std::is_integral_v<T>` | Integer type |
| `std::is_floating_point_v<T>` | Floating-point type |
| `std::is_pointer_v<T>` | Pointer type |
| `std::is_reference_v<T>` | Reference type |
| `std::is_const_v<T>` | `const`-qualified type |
| `std::is_same_v<T, U>` | Same type |
| `std::is_base_of_v<Base, Derived>` | Inheritance relationship |
| `std::is_constructible_v<T, Args...>` | Constructible from `Args...` |
| `std::is_trivially_copyable_v<T>` | Safe to `memcpy` |
| `std::remove_reference_t<T>` | Strips reference from type |
| `std::remove_const_t<T>` | Strips `const` from type |
| `std::decay_t<T>` | Applies array/function/reference/const decay |
| `std::conditional_t<B, T, F>` | `T` if `B` is true, `F` otherwise |

---

## Common Interview Questions -- Templates

**Q: What is the difference between function overloading and template specialization?**

Overloading creates multiple distinct functions that the compiler selects using overload resolution. Template specialization provides alternative implementations for specific template arguments. Function templates cannot be partially specialized, so overloading is usually preferred for function-level customization. The compiler considers non-template overloads before template specializations.

**Q: What is SFINAE and when is it useful?**

SFINAE means "Substitution Failure Is Not An Error." When a template parameter substitution produces an invalid type, the template is removed from the overload set rather than causing a compile error. This enables compile-time function dispatch based on type properties, e.g., enabling a function only for types that have a `.size()` method. In modern C++ (C++20+), concepts are the preferred replacement for most SFINAE patterns.

**Q: What is CRTP and when would you use it?**

CRTP (Curiously Recurring Template Pattern) is when a class inherits from a template instantiated with itself: `class Derived : public Base<Derived>`. It enables static polymorphism (no vtable overhead), mixin behavior, and compile-time interface enforcement. Use it when you need polymorphic-like behavior in performance-critical code where virtual dispatch is too costly.

**Q: What are the trade-offs of using templates?**

Advantages: zero-overhead abstraction, type safety, compile-time computation. Disadvantages: longer compile times, code bloat (each instantiation generates separate code), complex error messages, all implementation must be in headers (traditionally). Concepts (C++20) significantly improve error messages.

**Q: Why must template definitions usually live in headers, and what does explicit instantiation (`extern template`) buy you?**

A template is not code; it is a recipe. The compiler generates `Matrix<float>::trace()` only in a TU that (a) uses it and (b) can see the definition at that point. Each `.cpp` is compiled separately, so if `trace()` is defined in `matrix.cpp` and used in `main.cpp`, `main.o` gets an undefined reference that nobody fills in, and the link fails with `undefined reference to Matrix<float>::trace() const`. Putting the definition in the header lets every user instantiate it. The duplicates are emitted as weak/COMDAT symbols (`W` in `nm`), and the linker keeps one copy.

The price is that every TU that uses `Matrix<float>` re-instantiates and re-optimizes the same code, and the linker throws all but one copy away. Explicit instantiation fixes that:

```cpp
// fragment -- three files
// matrix.h
template <class T>
class Matrix {
public:
    explicit Matrix(std::size_t n) : n_(n), a_(n * n, T{1}) {}
    T trace() const;
private:
    std::size_t n_;
    std::vector<T> a_;
};
template <class T>
T Matrix<T>::trace() const { T s{}; for (std::size_t i = 0; i < n_; ++i) s += a_[i * n_ + i]; return s; }

extern template class Matrix<float>;   // explicit instantiation DECLARATION: "another TU emits Matrix<float>"

// matrix.cpp
#include "matrix.h"
template class Matrix<float>;          // explicit instantiation DEFINITION: emitted exactly once, here

// main.cpp
#include "matrix.h"
int main() {
    Matrix<float>  m(4);               // uses matrix.o's copy: nm -C main.o shows  U Matrix<float>::trace() const
    Matrix<double> d(3);               // not covered: implicitly instantiated here (W Matrix<double>::trace() const)
    return static_cast<int>(m.trace() + d.trace());
}
```

What it buys you: (1) **compile time and object size**, because heavy instantiations (`Matrix<float>`, `std::basic_string<char>` inside libstdc++ itself) are compiled once instead of in every TU. (2) **Hiding the definition** for a closed set of types: keep the definition in the `.cpp`, explicitly instantiate `float`, `double`, and `half` there, and users get a link error for anything else. Math libraries that support a fixed list of element types use this pattern. Pitfalls: `extern template` does not stop the compiler from instantiating *inline* members for inlining (the standard allows it), so it is a build-time optimization, not a guarantee. If you forget the explicit instantiation definition, every user fails to link. And with `-fvisibility=hidden`, an explicitly instantiated template in a `.so` needs an export macro on the instantiation, or the symbols stay hidden ([13.11](#1311-symbol-visibility-and-export-control)).

**Q: SFINAE vs concepts vs `if constexpr`: when do you use which, and how do the error messages differ?**

All three select code based on properties of a type at compile time, but they work at different levels:

```cpp
// dispatch.cpp -- g++ -std=c++20 -Wall -Wextra dispatch.cpp
#include <concepts>
#include <cstddef>
#include <cstdio>
#include <string>
#include <type_traits>
#include <vector>

// (1) SFINAE (C++11): the overload silently drops out if t.size() is ill-formed.
template <class T, class = decltype(std::declval<const T&>().size())>
std::size_t count_sfinae(const T& t) { return t.size(); }

// (2) Concept (C++20): same constraint, named, with a readable diagnostic.
template <class T>
concept Sized = requires(const T& t) { { t.size() } -> std::convertible_to<std::size_t>; };

std::size_t count_concept(const Sized auto& t) { return t.size(); }
std::size_t count_concept(const auto&) { return 1; }      // less constrained: chosen for non-Sized

// (3) if constexpr (C++17): ONE function, branch chosen inside the body.
template <class T>
std::size_t count_ifc(const T& t) {
    if constexpr (Sized<T>) return t.size();
    else if constexpr (std::is_arithmetic_v<T>) return 1;
    else static_assert(!sizeof(T), "count_ifc: unsupported type");  // fires only if instantiated
}

int main() {
    std::vector<int> v{1, 2, 3};
    std::string s = "hip";
    std::printf("%zu %zu %zu %zu %zu\n", count_sfinae(v), count_concept(s), count_concept(42),
                count_ifc(v), count_ifc(3.5));    // prints: 3 3 1 3 1
}
```

| | SFINAE | Concepts | `if constexpr` |
|---|---|---|---|
| Works on | The overload set: a failed substitution removes the candidate | The overload set: an unsatisfied constraint removes the candidate | Statements inside one function body |
| Choosing between alternatives | Hard: overlapping `enable_if` conditions are ambiguous, so you write mutually exclusive conditions | Built in: the *more constrained* overload wins (subsumption), so a generic fallback "just works" | `if` / `else if` chain, first match wins |
| Extensible by other code | Yes (add an overload) | Yes (add an overload) | No: closed set, you edit the function |
| Error for `count_x(42)` with no fallback | GCC 15: "no matching function ... template argument deduction/substitution failed: request for member 'size' in ... which is of non-class type 'const int'" (and the real reason is often buried in a long list of candidates) | GCC 15: "constraints not satisfied ... required for the satisfaction of 'Sized<auto:1>' [with auto:1 = int] ... the required expression 't.size()' is invalid" | Whatever you write in the `static_assert`, or a hard error deep inside the body |
| Minimum standard | C++11 (`void_t` C++17) | C++20 | C++17 |

Rules of thumb: use **concepts** for constraining interfaces in C++20 code (they document intent and give the best errors), **`if constexpr`** when the variation is an implementation detail of one function (small tweaks per type, no need for others to extend it), and **SFINAE** only when you are stuck before C++20 or in code that must also compile as C++17. Follow-ups: (1) `if constexpr` only skips instantiating the discarded branch when the condition depends on a template parameter. Outside a template, both branches must compile. (2) `static_assert(false, "...")` in a discarded branch was ill-formed (no diagnostic required) before P2593 made it valid for C++23 (applied as a defect report, supported in GCC 13 and Clang 17). The `!sizeof(T)` trick above is the portable workaround. (3) SFINAE only covers the *immediate context* (the signature). An error inside the function body is a hard error, not a substitution failure.

**Q: What is two-phase name lookup, and why do you need `this->`, `typename`, and `template` in dependent contexts?**

A template is checked twice. **Phase 1** happens at the point of definition: the compiler parses the template and looks up every *non-dependent* name (one that does not involve a template parameter) right away. **Phase 2** happens at instantiation: *dependent* names (whose meaning depends on `T`) are looked up then, including ADL at the point of instantiation. The consequences:

```cpp
// twophase.cpp -- g++ -std=c++20 -Wall -Wextra twophase.cpp
#include <cstdio>

template <class T>
struct Base {
    using value_type = T;
    void emit() const { std::puts("Base::emit"); }
    template <int N> int get() const { return N; }
};

template <class T>
struct Derived : Base<T> {
    void f() const {
        // emit();                               // error: dependent base Base<T> is not searched in phase 1
        this->emit();                            // OK: 'this' is dependent, so lookup waits for phase 2
        Base<T>::emit();                         // also OK (but suppresses virtual dispatch if emit were virtual)
        typename Base<T>::value_type v{};        // 'typename': Base<T>::value_type is a dependent TYPE
        int n = this->template get<2>();         // 'template': get is a dependent member TEMPLATE
        std::printf("v=%d n=%d\n", static_cast<int>(v), n);
    }
};

int main() { Derived<int>{}.f(); }
```

1. **Dependent base classes are not searched in phase 1.** `Base<T>` could be specialized later so that it has no `emit` at all, so the compiler cannot look inside it yet. A bare `emit()` is a non-dependent name, and GCC reports "there are no arguments to 'emit' that depend on a template parameter, so a declaration of 'emit' must be available". Worse, if a global function named `emit` exists, phase 1 silently binds to *that* one. `this->emit()` makes the name dependent and defers the lookup.
2. **`typename`**: in phase 1 the parser cannot know whether `Base<T>::value_type` is a type, a static member, or a function. It assumes "not a type" unless you write `typename`. (C++20 relaxed this in contexts where only a type can appear, such as `using X = Base<T>::value_type;` or a return type, but writing it is always fine.)
3. **`template`**: in `this->get<2>()`, the `<` would otherwise parse as less-than. `this->template get<2>()` says "get names a template". The same applies to `std::get` on a dependent tuple-like member, e.g. `obj.template get<0>()`.

Follow-ups: older MSVC did not implement two-phase lookup and accepted code like the bare `emit()`. `/permissive-` (on by default for new projects since Visual Studio 2017 15.5) enables conforming behavior, so "it compiled on Windows" is a classic porting bug. Non-dependent errors are reported even if the template is never instantiated, while dependent errors appear only on instantiation.

---

# Part 3: Standard Template Library

---

# 7. STL Containers

---

## 7.1 Container Taxonomy

```
                              STL Containers
                   ┌──────────────┼──────────────┐
              Sequence       Associative      Unordered
             Containers      Containers    (Hash) Containers
            ┌────┼────┐    ┌────┼────┐    ┌────┼────┐
         vector  deque list set  map   unordered_set  unordered_map
         array   forward_list  multiset multimap  unordered_multiset
                                                  unordered_multimap

              Container Adapters (wrappers over other containers):
              stack    queue    priority_queue
```

## 7.2 Sequence Containers

### Complexity Comparison

| Operation | `vector` | `deque` | `list` | `forward_list` | `array` |
|---|---|---|---|---|---|
| Access by index | O(1) | O(1) | O(n) | O(n) | O(1) |
| Front insert/remove | O(n) | **O(1)** | O(1) | O(1) | N/A |
| Back insert/remove | **O(1) amort.** | **O(1)** | O(1) | O(n) | N/A |
| Middle insert/remove | O(n) | O(n) | **O(1)** | **O(1)** | N/A |
| Find (unsorted) | O(n) | O(n) | O(n) | O(n) | O(n) |
| Memory layout | Contiguous | Chunked | Scattered nodes | Scattered nodes | Contiguous |
| Cache performance | Excellent | Good | Poor | Poor | Excellent |
| Iterator invalidation | On realloc | On insert/erase | Only erased element | Only erased element | N/A |

### `std::vector` -- The Default Container

Contiguous dynamic array. Preferred unless you have a specific reason to use something else:

```cpp
#include <vector>

std::vector<int> v = {1, 2, 3, 4, 5};
v.push_back(6);              // amortized O(1)
v.emplace_back(7);           // constructs in-place
v[2];                        // O(1) access, no bounds check
v.at(2);                     // O(1) access, throws std::out_of_range
v.size();                    // 7
v.capacity();                // >= 7 (may be larger due to growth)
v.reserve(100);              // pre-allocate to avoid reallocations
v.shrink_to_fit();           // request to reduce capacity to size
v.erase(v.begin() + 2);     // O(n) -- shifts elements
v.insert(v.begin(), 0);     // O(n) -- shifts elements
v.clear();                   // removes all, capacity unchanged
```

**Growth strategy:** when `size == capacity`, the vector allocates a new buffer (typically 2x), copies/moves all elements, and frees the old buffer. This gives O(1) amortized push_back.

### `std::deque` -- Double-Ended Queue

Non-contiguous storage (array of fixed-size blocks). O(1) insert/remove at both ends:

```cpp
#include <deque>

std::deque<int> dq = {1, 2, 3};
dq.push_front(0);   // O(1) -- not possible with vector
dq.push_back(4);    // O(1)
dq.pop_front();     // O(1)
dq[2];              // O(1) random access (slightly slower than vector)
```

### `std::list` / `std::forward_list`

Doubly-linked / singly-linked lists. O(1) insert/remove anywhere (given an iterator), but no random access and poor cache performance:

```cpp
#include <list>

std::list<int> lst = {3, 1, 4, 1, 5};
auto it = std::find(lst.begin(), lst.end(), 4);
lst.insert(it, 99);     // O(1) insert before iterator
lst.erase(it);           // O(1) remove at iterator
lst.sort();              // O(n log n) -- special member sort (not std::sort)
lst.splice(lst.end(), other_list);  // O(1) move elements between lists
```

### `std::array` -- Fixed-Size Array

Stack-allocated, fixed size known at compile time. Zero overhead over C arrays:

```cpp
#include <array>

std::array<int, 5> arr = {1, 2, 3, 4, 5};
arr[0];         // O(1)
arr.at(0);      // O(1) with bounds check
arr.size();     // 5 (constexpr)
arr.fill(0);    // set all elements to 0
```

## 7.3 Associative Containers (Ordered)

Implemented as **balanced BSTs** (typically red-black trees). All operations are O(log n). Elements are always sorted by key:

| Operation | `set` | `multiset` | `map` | `multimap` |
|---|---|---|---|---|
| Insert | O(log n) | O(log n) | O(log n) | O(log n) |
| Find | O(log n) | O(log n) | O(log n) | O(log n) |
| Erase | O(log n) | O(log n) | O(log n) | O(log n) |
| Duplicates | No | Yes | No (keys) | Yes (keys) |
| Underlying structure | Red-black tree | Red-black tree | Red-black tree | Red-black tree |

```cpp
#include <set>
#include <map>

std::set<int> s = {3, 1, 4, 1, 5};    // {1, 3, 4, 5} -- sorted, no dupes
s.insert(2);                            // {1, 2, 3, 4, 5}
s.count(3);                             // 1 (0 or 1 for set)
s.find(3);                              // iterator to element, or s.end()
s.lower_bound(3);                       // iterator to first >= 3
s.upper_bound(3);                       // iterator to first > 3

std::map<std::string, int> m;
m["alice"] = 90;
m["bob"] = 85;
m.insert({"charlie", 92});
m.emplace("dave", 88);

for (const auto& [name, score] : m) {   // structured binding (C++17)
    std::cout << name << ": " << score << "\n";
}

// m is sorted by key: alice, bob, charlie, dave
```

## 7.4 Unordered Containers (Hash-Based)

Implemented as **hash tables** with separate chaining. Average O(1), worst-case O(n):

| Operation | Average | Worst Case |
|---|---|---|
| Insert | O(1) | O(n) (rehash) |
| Find | O(1) | O(n) (all keys hash to same bucket) |
| Erase | O(1) | O(n) |

```cpp
#include <unordered_set>
#include <unordered_map>

std::unordered_set<int> us = {3, 1, 4, 1, 5};
us.insert(2);
us.count(3);     // O(1) average
us.bucket_count();      // number of buckets
us.load_factor();       // elements / buckets
us.max_load_factor(0.7); // trigger rehash when exceeded
us.reserve(1000);       // pre-allocate buckets

std::unordered_map<std::string, int> um;
um["key"] = 42;
um.contains("key");     // C++20
```

### Custom Hash Functions

For user-defined types, you must provide a hash function:

```cpp
struct Point {
    int x, y;
    bool operator==(const Point& other) const = default;
};

struct PointHash {
    size_t operator()(const Point& p) const {
        auto h1 = std::hash<int>{}(p.x);
        auto h2 = std::hash<int>{}(p.y);
        return h1 ^ (h2 << 1);  // combine hashes
    }
};

std::unordered_set<Point, PointHash> points;
```

## 7.5 Container Adapters

Wrappers that restrict an underlying container's interface:

| Adapter | Default Container | Operations |
|---|---|---|
| `std::stack` | `deque` | `push`, `pop`, `top` (LIFO) |
| `std::queue` | `deque` | `push`, `pop`, `front`, `back` (FIFO) |
| `std::priority_queue` | `vector` | `push`, `pop`, `top` (max-heap by default) |

```cpp
#include <stack>
#include <queue>

std::stack<int> stk;
stk.push(1); stk.push(2); stk.push(3);
stk.top();   // 3
stk.pop();   // removes 3

std::priority_queue<int> pq;                           // max-heap
pq.push(3); pq.push(1); pq.push(4);
pq.top();   // 4

std::priority_queue<int, std::vector<int>,
                    std::greater<int>> min_pq;         // min-heap
min_pq.push(3); min_pq.push(1); min_pq.push(4);
min_pq.top();   // 1
```

## 7.6 When to Use Which Container

| Use Case | Container |
|---|---|
| Default choice, dynamic array | `std::vector` |
| Fixed size known at compile time | `std::array` |
| Insert/remove at both ends | `std::deque` |
| Frequent insert/remove in middle (with iterator) | `std::list` |
| Sorted unique keys | `std::set` |
| Sorted key-value pairs | `std::map` |
| Fast lookup (O(1) average) | `std::unordered_map` / `std::unordered_set` |
| Max/min extraction | `std::priority_queue` |
| LIFO order | `std::stack` |
| FIFO order | `std::queue` |
| Multiple values per key, sorted | `std::multimap` |

## 7.7 Container Internals

Complexity tables hide constant factors that dominate real performance: allocations per element, bytes per element, and dependent cache misses per lookup. All numbers below were measured with GCC 15 / libstdc++ on x86-64 using the program at the end of this section.

### `std::vector`: Growth Factor and Amortized O(1) `push_back`

When `size() == capacity()`, `push_back` allocates a buffer `g` times larger, moves or copies the elements over, constructs the new element, and frees the old buffer.

| Implementation | Growth factor `g` | Observed capacities |
|---|---|---|
| libstdc++ (GCC) | 2 | 1 2 4 8 16 ... 1024 |
| libc++ (Clang) | 2 | 1 2 4 8 ... |
| MSVC STL | 1.5 | 1 2 3 4 6 9 13 19 28 ... |
| folly `fbvector` | 1.5 | (plus `realloc` for relocatable types) |

**Amortized analysis (aggregate method).** Push `n` elements with `g = 2` starting from capacity 1. Reallocations happen at sizes 1, 2, 4, ..., n/2, and copy 1 + 2 + 4 + ... + n/2 = n - 1 elements in total. Add the n constructions and the total work is under 2n, so O(1) per `push_back` amortized. For a general `g`, the copies are n/g + n/g² + ... = **n/(g-1)**: n for g = 2 and 2n for g = 1.5. Worked example: 1,000,000 `push_back`s of `int` with g = 2 cause 20 reallocations (2^20 = 1,048,576) and about 1M element copies in total. If capacity instead grew by a constant `+k`, there would be n/k reallocations copying k, 2k, 3k, ... elements: O(n²/k) total, so O(n) per push.

**Why 1.5 rather than 2?** With g = 2, each new block (2^k) is larger than the sum of all previous blocks (2^k - 1), so the allocator can never reuse the freed predecessors for the next growth, even if they are adjacent. With g below the golden ratio (about 1.618), the freed blocks eventually add up to enough for a new request. The cost is more reallocations (2n copies instead of n). Peak waste just after a growth is (g - 1)/g of capacity: 50% for g = 2 and 33% for g = 1.5.

**`std::move_if_noexcept`.** `push_back` gives the **strong guarantee**: if it throws, the vector is unchanged. When relocating, the vector therefore *moves* elements only if the move constructor is `noexcept` (or the type is not copyable). Otherwise it *copies*, so a throw midway leaves the old buffer intact. A class with a user-written move constructor that is not `noexcept` silently gets copied on every reallocation. Mark move constructors `noexcept`, and `static_assert(std::is_nothrow_move_constructible_v<T>)` for hot types. Puzzle: [Output Quiz A50](../practice/Cpp_Output_Quiz.md#a50-vector-reallocation-copies-unless-the-move-constructor-is-noexcept). Full implementation: [16.3](#163-vectort-placement-new-growth-and-the-strong-guarantee).

Other `vector` facts that come up:

- `v.push_back(v[0])` must work even when it reallocates. Implementations construct the new element in the new buffer *before* moving the old ones.
- `reserve(n)` reallocates only if `n > capacity()`. `clear()` keeps the capacity. `shrink_to_fit()` is a non-binding request (libstdc++ honours it). The pre-C++11 idiom `std::vector<T>(v).swap(v)` does the same.
- `vector<bool>` is a space-optimized specialization: it stores bits, `operator[]` returns a proxy object rather than `bool&`, and it is not a real container (`&v[0]` is not a `bool*`). Use `std::vector<char>` or `boost::dynamic_bitset` when you need real references.

### `std::deque`: A Map of Fixed-Size Blocks

```text
 deque object (80 B in libstdc++: map ptr, map size, start iterator, finish iterator)
      │
      ▼  "map": array of block pointers (grows by reallocation, kept centred)
 ┌─────┬─────┬─────┬─────┬─────┬─────┐
 │  -  │  ●  │  ●  │  ●  │  -  │  -  │
 └─────┴──┼──┴──┼──┴──┼──┴─────┴─────┘
          ▼     ▼     ▼
       [....xx][xxxxxx][xxx...]      each block: 512 B in libstdc++ (128 ints)
          ▲                 ▲
        start             finish     iterator = {cur, first, last, node}: 4 pointers
```

- **Block size**: libstdc++ 512 bytes (one element per block if `sizeof(T) > 512`). libc++ 4096 bytes (minimum 16 elements). MSVC 16 bytes, which means a single element per block for any `T` over 8 bytes. That makes MSVC's `deque` a slow, pointer-chasing container.
- `push_front`/`push_back` never move existing elements. They fill the end block or allocate a new one, and sometimes reallocate the *map* of pointers. So **references stay valid but iterators are invalidated**: an iterator contains a pointer into the map, and the map may move.
- Random access is `map[(offset + i) / B][(offset + i) % B]`, two dependent loads instead of one, and loops over a deque vectorize poorly. `std::stack` and `std::queue` default to `deque` for the O(1) ends and stable references. A ring buffer over a `vector` is faster when capacity is bounded.

### `std::list` / `std::forward_list`

- Node = prev + next + `T`: 24 bytes for `list<int>`, which glibc `malloc` rounds up to a 32-byte chunk. That is 8x the payload, plus one cache miss per hop. `forward_list` saves one pointer and has no `size()`.
- `size()` is O(1) since C++11 (a stored count). This is one reason libstdc++ needed the dual ABI ([13.13](#1313-abi-stability-and-the-libstdc-dual-abi)). Consequence: `splice` of a *range* from a *different* list is O(n), because the count must be recomputed. Splicing a whole list or a single element is O(1).
- Use `list` when you need stable iterators and references with O(1) erase-by-iterator, as in an LRU cache (`list` + `unordered_map` of iterators), or O(1) splicing. Even then, an intrusive list or index-based free list in a `vector` is usually faster.

### `std::map` / `std::set`: Red-Black Tree Nodes

- libstdc++ node header = color (4 B, padded to 8) + parent + left + right = **32 bytes**, then the value. `map<int,int>` nodes are 40 bytes (48-byte malloc chunk) to store 8 bytes of payload: 6x overhead.
- Red-black height is at most 2·log2(n+1). For n = 1M that bounds the height at 40, with about 20 levels typical. Each level is a dependent load. Once the top levels are cached, a lookup in a cold 1M-entry map still takes roughly 10 or more DRAM misses at about 80 ns each, on the order of 1 µs. A sorted `vector` with `lower_bound` performs the same comparisons over contiguous memory (and prefetches better). `absl::btree_map` packs many keys per node.
- Insert does at most 2 rotations and erase at most 3 (plus recoloring). `++it` follows parent pointers: amortized O(1), worst case O(log n).
- C++14 transparent comparators (`std::map<std::string, int, std::less<>>`) allow `m.find(std::string_view{...})` without constructing a temporary `std::string`. C++17 `extract`/`merge`/`insert(node_handle)` move nodes between maps without reallocating, and can even change a key in place.
- C++23 `std::flat_map` is a pair of sorted vectors (keys and values): O(n) insert, but cache-friendly lookup and iteration. See [11.10](#1110-c23-features).

### `std::unordered_map`: Nodes and Buckets vs Open Addressing

libstdc++ stores **all nodes in one singly linked list**. Each bucket holds a pointer to the node *before* the bucket's first node, which is what lets a singly linked list erase in O(1):

```text
 buckets[] (bucket_count pointers)          one global singly linked list of nodes
 ┌────┐
 │ b0 │──► (before-begin sentinel) ──► [next|hash?|k=13,v] ──► [next|k=26,v] ──┐
 │ b1 │──► nullptr                                                            │
 │ b2 │──► (node before k=2) ────────────────────────────────────────────────► [next|k=2,v] ──► ...
 └────┘
 node = next pointer + pair<const K, V> (+ cached hash code if the hash is not "fast")
```

Measured: an `unordered_map<int,int>` node is 16 B (next + pair, with no cached hash because `std::hash<int>` is considered fast). An `unordered_map<std::string,int>` node is 56 B (next 8 + string 32 + int 4 + padding 4 + cached hash 8). The bucket array is a separate allocation (8 B per bucket). `max_load_factor()` defaults to 1.0. Bucket counts are primes: 1 → 13 → 29 → 59 → 127 → 257 → 541 → 1109, roughly doubling. The prime modulo costs an integer division per lookup, which is why power-of-two tables use a mask (and must mix the hash well).

**Why the standard effectively mandates chaining.** The interface guarantees that references and pointers to elements survive a rehash, and it exposes the bucket API (`bucket(key)`, `begin(n)`, `bucket_size(n)`). Both force one heap node per element. A lookup is then hash → bucket slot → predecessor node → node: 2 to 3 dependent cache misses, and one `malloc` per insert.

**Open addressing (Swiss tables: `absl::flat_hash_map`, `boost::unordered_flat_map`).** Elements live inline in a slot array, with a parallel array of 1-byte **control bytes**. Each control byte is EMPTY, DELETED, or 7 bits of the hash (H2). The remaining hash bits (H1) choose a starting group of 16 slots. One SSE2 compare checks 16 control bytes at once, and only candidates whose H2 matches are key-compared. The maximum load factor is 7/8. A typical lookup is one cache line of metadata plus one slot.

| Per-element memory, `<int,int>` | Approximate bytes |
|---|---|
| `std::unordered_map` | 32 (16-B node in a 32-B malloc chunk) + 8 to 16 (bucket pointer at load 1.0 to 0.5) ≈ **40 to 48** |
| `absl::flat_hash_map` | (8 B slot + 1 B control) / load (0.44 to 0.875) ≈ **10 to 21** |
| `std::map` | 48-B chunk ≈ **48** |
| Sorted `std::vector<std::pair<int,int>>` | **8** (up to 16 with capacity slack) |

Swiss-table trade-offs: **no reference stability** (a rehash moves elements; use `absl::node_hash_map` when you need it); erased slots become tombstones until the next rehash; large values make the slot array large and rehashes expensive. Hash quality also matters more. `std::hash<int>` is the identity in libstdc++ and libc++, which is fine with prime modulo but catastrophic with a power-of-two mask on keys that are multiples of 2^k. Abseil and Boost mix the hash bits first. **Hash flooding**: adversarial keys that all collide turn O(1) into O(n). Use a seeded or randomized hash for untrusted input.

### `std::string`: Small String Optimization (SSO)

| Implementation | `sizeof(std::string)` (64-bit) | Inline capacity |
|---|---|---|
| libstdc++ (GCC 5+) | 32 | 15 chars |
| libc++ | 24 | 22 chars |
| MSVC | 32 | 15 chars |

libstdc++'s layout is `{char* ptr; size_t size; union { size_t capacity; char buf[16]; }}`. For short strings `ptr` points at `buf` inside the object, so no allocation happens. libc++ packs a flag bit into the size/capacity so it can use 23 of its 24 bytes. Before GCC 5, libstdc++ used reference-counted **copy-on-write** strings. C++11 effectively banned COW: for example, non-const `operator[]` may not invalidate references, and COW also causes surprises under concurrency. The result was libstdc++'s dual ABI.

SSO consequences:

- Moving a short string copies its bytes (still O(1), at most 15 chars), and the source keeps a valid but unspecified value.
- **Dangling bugs that depend on length.** Take a `string_view` (or `const char*`) into `vec[i]`, then let `vec` reallocate. For a long string, the moved-to string adopted the same heap buffer, so the view still "works" by accident. For a short string, the characters lived *inside* the old `std::string` object, which is now destroyed, so the view dangles. Tests with long strings pass, and production keys of 8 characters crash. ASan catches it.

### Small Vectors and Inline Storage

The SSO idea generalized: `llvm::SmallVector<T, N>`, `boost::container::small_vector<T, N>`, `absl::InlinedVector<T, N>`, and `folly::small_vector`. They store up to N elements inline and spill to the heap beyond that. Layout: `{T* begin; size; capacity; alignas(T) std::byte inline_buf[N * sizeof(T)]}`, inline while `begin == inline_buf`. Costs: `sizeof` grows with N; moving an inline small vector moves N elements one by one (O(N), not three pointer swaps); and iterators and pointers do **not** survive a move, unlike `std::vector`, where a move transfers the buffer. C++26 adds `std::inplace_vector<T, N>`: fixed capacity, never allocates, `try_push_back` reports failure. These types are common in compilers and profilers for "usually 1 to 4 items" lists such as operands or per-kernel counter sets.

### Sorting in the STL

| Algorithm | Implementation (libstdc++) | Complexity | Stable? |
|---|---|---|---|
| `std::sort` | **Introsort**: median-of-3 quicksort; switches to heapsort when recursion depth exceeds 2·log2(n); partitioning stops at 16 elements and one final insertion sort finishes the nearly sorted array | O(n log n) worst case (guaranteed since C++11) | No |
| `std::stable_sort` | Merge sort with a temporary buffer; in-place merge if allocation fails | O(n log n) with a buffer, O(n log² n) without | Yes |
| `std::partial_sort` | Heap select | O(n log k) | No |
| `std::nth_element` | Introselect | O(n) average | No |
| `list::sort` | Merge sort on nodes | O(n log n) | Yes |

**The comparator must be a strict weak ordering.** `std::sort(v.begin(), v.end(), [](int a, int b) { return a <= b; })` is undefined behavior. libstdc++'s unguarded insertion sort relies on `comp(x, x) == false` as a sentinel, so with many equal elements it can walk off the front of the array and crash. Use `<`, and for multi-key ordering use `std::tie(a.x, a.y) < std::tie(b.x, b.y)` or `<=>`.

### Measuring It Yourself

```cpp
// internals.cpp -- g++ -std=c++20 -O2 internals.cpp && ./a.out   (numbers below: GCC 15 / libstdc++, x86-64)
#include <cstdio>
#include <deque>
#include <list>
#include <map>
#include <memory>
#include <string>
#include <unordered_map>
#include <vector>

// Allocator that reports the size of whatever type the container rebinds it to.
template <class T>
struct Spy {
    using value_type = T;
    Spy() = default;
    template <class U> Spy(const Spy<U>&) {}
    T* allocate(std::size_t n) {
        std::printf("    allocate %zu x %zu B\n", n, sizeof(T));
        return std::allocator<T>{}.allocate(n);
    }
    void deallocate(T* p, std::size_t n) { std::allocator<T>{}.deallocate(p, n); }
    friend bool operator==(Spy, Spy) { return true; }
};

int main() {
    // --- std::string SSO ---
    std::string s;
    std::string shorty = "fifteen chars!!";                 // 15 chars: still inline
    std::string longer = "sixteen chars!!!";                // 16 chars: heap
    auto inside = [](const std::string& x) {
        auto* obj = reinterpret_cast<const char*>(&x);
        return x.data() >= obj && x.data() < obj + sizeof x;
    };
    std::printf("sizeof(string)=%zu  empty capacity=%zu  15 chars inline=%d  16 chars inline=%d\n",
                sizeof s, s.capacity(), inside(shorty), inside(longer));

    // --- vector growth ---
    std::vector<int> v;
    std::size_t cap = v.capacity();
    std::printf("vector capacities:");
    for (int i = 0; i < 1000; ++i) {
        v.push_back(i);
        if (v.capacity() != cap) std::printf(" %zu", cap = v.capacity());
    }
    std::printf("\n");

    // --- node sizes, via the rebound allocator ---
    std::puts("list<int> node:");
    { std::list<int, Spy<int>> l; l.push_back(1); }
    std::puts("map<int,int> node:");
    { std::map<int, int, std::less<int>, Spy<std::pair<const int, int>>> m; m[1] = 1; }
    std::puts("unordered_map<int,int> (node, then bucket array):");
    { std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, Spy<std::pair<const int, int>>> m; m[1] = 1; }
    std::puts("unordered_map<string,int> node (hash code cached in node):");
    { std::unordered_map<std::string, int, std::hash<std::string>, std::equal_to<std::string>,
                         Spy<std::pair<const std::string, int>>> m; m["k"] = 1; }
    std::puts("deque<int> (block map, then one 512-byte block):");
    { std::deque<int, Spy<int>> d; d.push_back(1); }

    // --- unordered_map rehash schedule (prime bucket counts, max_load_factor 1.0) ---
    std::unordered_map<int, int> u;
    std::size_t b = u.bucket_count();
    std::printf("unordered_map buckets: %zu ->", b);
    for (int i = 0; i < 1000; ++i) {
        u[i] = i;
        if (u.bucket_count() != b) std::printf(" %zu", b = u.bucket_count());
    }
    std::printf("  (max_load_factor=%.1f)\n", u.max_load_factor());
}
```

```text
sizeof(string)=32  empty capacity=15  15 chars inline=1  16 chars inline=0
vector capacities: 1 2 4 8 16 32 64 128 256 512 1024
list<int> node:
    allocate 1 x 24 B
map<int,int> node:
    allocate 1 x 40 B
unordered_map<int,int> (node, then bucket array):
    allocate 1 x 16 B
    allocate 13 x 8 B
unordered_map<string,int> node (hash code cached in node):
    allocate 1 x 56 B
    allocate 13 x 8 B
deque<int> (block map, then one 512-byte block):
    allocate 8 x 8 B
    allocate 128 x 4 B
unordered_map buckets: 1 -> 13 29 59 127 257 541 1109  (max_load_factor=1.0)
```

> **See also:** [Hash tables: load factor, rehashing, open addressing](../computer-science/DSA_Fundamentals.md#5-hash-tables) · [Memory hierarchy and cache lines](../computer-science/Performance_Engineering.md#5-memory-hierarchy-programming) · [Containers and iterators quiz](../practice/Cpp_Output_Quiz.md#8-containers-and-iterators)

---

# 8. Iterators, Algorithms, and Lambdas

---

## 8.1 Iterator Categories

Iterators abstract traversal over containers. Each category supports an increasing set of operations:

| Category | Operations Supported | Examples |
|---|---|---|
| **Input** | Read, single-pass forward (`++`, `*`, `==`) | `istream_iterator` |
| **Output** | Write, single-pass forward (`++`, `*`) | `ostream_iterator`, `back_inserter` |
| **Forward** | Read/write, multi-pass forward | `forward_list::iterator`, `unordered_set::iterator` |
| **Bidirectional** | Forward + backward (`--`) | `list::iterator`, `set::iterator`, `map::iterator` |
| **Random Access** | Bidirectional + arithmetic (`+`, `-`, `[]`, `<`) | `vector::iterator`, `deque::iterator`, `array::iterator` |
| **Contiguous** (C++17) | Random access + elements contiguous in memory | `vector::iterator`, `array::iterator`, raw pointers |

```
Input/Output → Forward → Bidirectional → Random Access → Contiguous
```

### `iterator_traits` and C++20 Iterator Concepts

Generic code asks an iterator about itself through `std::iterator_traits<It>`: `value_type`, `difference_type`, `reference`, `pointer`, and `iterator_category`. A raw pointer gets these from a partial specialization. A class type gets them from nested typedefs. Before C++20, algorithms used **tag dispatch** on `iterator_category`. For example, `std::advance` is O(1) for random-access iterators and O(n) otherwise. C++20 replaces the tags with **concepts** (`std::input_iterator`, `std::forward_iterator`, `std::bidirectional_iterator`, `std::random_access_iterator`, `std::contiguous_iterator`). Ranges and constrained algorithms check these concepts at compile time. They read `iterator_concept` first and fall back to `iterator_category`.

To satisfy `std::forward_iterator` or a stronger concept, a custom iterator needs:
- a default constructor
- copyability
- `operator==` (C++20 synthesizes `!=`)
- `value_type` and `difference_type`
- both pre- and post-increment

For `std::random_access_iterator` it also needs `+=`, `-=`, `+`, `-` (both iterator - n and iterator - iterator), `[]`, and a total order (`<=>`). `static_assert` the concept next to the class, so a missing operator gives one clear error instead of a page of template noise deep inside `std::sort`.

**Interview exercise: a conforming iterator for a ring buffer.** The iterator stores a *logical* index (0 is the oldest element) and maps it to a physical slot only when dereferenced. Comparison and difference then stay trivial, and wraparound is handled in one place. A single template parameterized on `bool Const` produces both `iterator` and `const_iterator`, with an implicit conversion from the mutable one to the const one.

```cpp
#include <algorithm>
#include <cstddef>
#include <iostream>
#include <iterator>
#include <numeric>
#include <ranges>

// Fixed-capacity ring buffer exposing a conforming random-access iterator.
template <typename T, std::size_t N>
class Ring {
    T data_[N]{};
    std::size_t head_ = 0, size_ = 0;

public:
    void push(const T& v) {
        data_[(head_ + size_) % N] = v;
        if (size_ < N) ++size_; else head_ = (head_ + 1) % N;  // overwrite oldest
    }

    template <bool Const>
    class Iter {
        using RingPtr = std::conditional_t<Const, const Ring*, Ring*>;
        RingPtr r_ = nullptr;
        std::ptrdiff_t i_ = 0;  // logical index: 0 == oldest element

    public:
        using iterator_concept  = std::random_access_iterator_tag;
        using iterator_category = std::random_access_iterator_tag;
        using value_type        = T;
        using difference_type   = std::ptrdiff_t;
        using reference         = std::conditional_t<Const, const T&, T&>;

        Iter() = default;  // required: iterators must be default-initializable
        Iter(RingPtr r, std::ptrdiff_t i) : r_(r), i_(i) {}
        operator Iter<true>() const { return {r_, i_}; }  // iterator -> const_iterator

        reference operator*() const { return r_->data_[(r_->head_ + i_) % N]; }
        reference operator[](difference_type n) const { return *(*this + n); }

        Iter& operator++() { ++i_; return *this; }
        Iter operator++(int) { auto t = *this; ++i_; return t; }
        Iter& operator--() { --i_; return *this; }
        Iter operator--(int) { auto t = *this; --i_; return t; }
        Iter& operator+=(difference_type n) { i_ += n; return *this; }
        Iter& operator-=(difference_type n) { i_ -= n; return *this; }
        friend Iter operator+(Iter it, difference_type n) { return it += n; }
        friend Iter operator+(difference_type n, Iter it) { return it += n; }
        friend Iter operator-(Iter it, difference_type n) { return it -= n; }
        friend difference_type operator-(const Iter& a, const Iter& b) { return a.i_ - b.i_; }
        friend bool operator==(const Iter& a, const Iter& b) { return a.i_ == b.i_; }
        friend auto operator<=>(const Iter& a, const Iter& b) { return a.i_ <=> b.i_; }
    };
    using iterator = Iter<false>;
    using const_iterator = Iter<true>;

    iterator begin() { return {this, 0}; }
    iterator end() { return {this, static_cast<std::ptrdiff_t>(size_)}; }
    const_iterator begin() const { return {this, 0}; }
    const_iterator end() const { return {this, static_cast<std::ptrdiff_t>(size_)}; }
};

static_assert(std::random_access_iterator<Ring<int, 4>::iterator>);
static_assert(std::random_access_iterator<Ring<int, 4>::const_iterator>);
static_assert(std::ranges::random_access_range<Ring<int, 4>>);

int main() {
    Ring<int, 4> r;
    for (int v : {1, 2, 3, 4, 5, 6}) r.push(v);  // holds 3 4 5 6
    std::sort(r.begin(), r.end(), std::greater<>{});         // classic algorithm
    for (int v : r) std::cout << v << ' ';                   // 6 5 4 3
    std::cout << '\n' << std::accumulate(r.begin(), r.end(), 0) << '\n';  // 18
    for (int v : r | std::views::reverse | std::views::take(2)) std::cout << v << ' ';  // 3 4
    std::cout << '\n';
}
```

Common follow-ups:
- **Why a logical index, not a raw pointer into the buffer?** Wraparound makes physical addresses non-monotonic, so `<` and `-` on pointers would be wrong.
- **Is this a `contiguous_iterator`?** No. Elements are not contiguous in logical order, so it must not claim `std::contiguous_iterator_tag`.
- **What invalidates it?** It holds a `Ring*` and an index. `push` on a full ring shifts `head_`, so existing iterators silently refer to different elements. Document this the same way the standard documents the rules in 8.2.

## 8.2 Iterator Invalidation Rules

Interviewers usually follow up with "and what about references and pointers?". The answers differ. An iterator may contain more than a pointer to the element (a `deque` iterator also points into the block map), and a hash-table iterator's meaning depends on bucket order. A reference or pointer is invalidated only when the element itself moves or dies.

| Container | Operation | Iterators | References / pointers |
|---|---|---|---|
| `vector`, `string` | `push_back`/`insert`/`emplace`/`resize`/`reserve` **with reallocation** (`size() > old capacity()`) | **All** | **All** |
| | Same, **without** reallocation | At or after the insertion point, plus `end()` | At or after the insertion point |
| | `erase` / `pop_back` | At or after the erased element, plus `end()` | At or after the erased element |
| | `clear`, `shrink_to_fit` (if it reallocates) | All | All |
| `deque` | `push_front`/`push_back`/`emplace_front`/`emplace_back` | **All** (the block map may reallocate) | **None** (elements never move) |
| | `insert`/`emplace` in the middle | All | All |
| | `pop_front` / `pop_back`, or `erase` of the first/last element | Only the erased element's (and `end()` for back erasure) | Only the erased element's |
| | `erase` in the middle, `shrink_to_fit` | All | All |
| `list`, `forward_list` | Any insert, `splice` | None (spliced elements' iterators stay valid but now refer into the destination list) | None |
| | `erase`, `remove` | Only the erased elements' | Only the erased elements' |
| `set`/`map`/`multiset`/`multimap` | Any insert, `merge` | None | None |
| | `erase` | Only the erased element's | Only the erased element's |
| | `extract` (C++17) | The extracted element's | Stay valid, now owned by the node handle |
| `unordered_*` | Insert **causing rehash** (`size() > max_load_factor() * bucket_count()`), `rehash`, `reserve` | **All** | **None** (nodes never move) |
| | Insert without rehash | None | None |
| | `erase` | Only the erased element's | Only the erased element's |
| `array` | -- | Never (fixed storage) | Never |
| Open-addressing maps (`absl::flat_hash_map`) | Insert that grows the table | All | **All** (elements move) |

Corollaries worth stating explicitly:

- **`deque` push/pop at the ends**: keep `T&`/`T*` to elements across `push_back`, but never an iterator. This is why `std::queue<T>` over `deque` can hand out stable references.
- **`unordered_map` rehash**: a pointer to a value (`&m[k]`) survives any number of inserts, but a range-for loop that inserts into the map it iterates over is undefined behavior.
- **Swapping and moving containers.** After `a.swap(b)` or `b = std::move(a)` (with propagating or equal allocators), iterators and references stay valid but refer into the *other* container. `std::string` is the exception: with SSO the characters live inside the object, so `swap` and move invalidate them ([7.7](#77-container-internals)).
- **Non-owning views dangle by the same rules.** A `std::string_view`, `std::span`, or range view over a `vector` is invalidated exactly when the vector's references are. `std::string_view sv = std::string("tmp");` dangles immediately, because the temporary dies at the end of the full expression.
- **Debug help**: `-D_GLIBCXX_DEBUG` (libstdc++) or `-D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_DEBUG` (libc++) turn many invalid-iterator uses into immediate aborts. ASan catches the use-after-free when the memory was actually released.

```cpp
// invalidation.cpp -- g++ -std=c++20 -Wall -Wextra -fsanitize=address,undefined invalidation.cpp
#include <cassert>
#include <cstdint>
#include <cstdio>
#include <deque>
#include <string>
#include <unordered_map>
#include <vector>

int main() {
    // deque: push_back invalidates ITERATORS (the block map may be reallocated)
    // but never REFERENCES (elements are never moved between blocks).
    std::deque<int> d{1};
    int& first = d.front();
    for (int i = 0; i < 100000; ++i) d.push_back(i);   // many new blocks, several map reallocations
    first = 99;                                        // OK: reference still valid
    assert(d.front() == 99);

    // unordered_map: rehash invalidates ITERATORS (bucket order changes) but not
    // REFERENCES/POINTERS (nodes are never moved).
    std::unordered_map<int, std::string> m{{0, "zero"}};
    std::string& zero = m.at(0);
    std::size_t buckets = m.bucket_count();
    for (int i = 1; i < 10000; ++i) m.emplace(i, "v");
    assert(m.bucket_count() != buckets);               // rehashed several times
    zero += "!";                                       // OK
    assert(m.at(0) == "zero!");

    // vector: reallocation invalidates iterators AND references AND pointers.
    std::vector<int> v{1};
    auto before = reinterpret_cast<std::uintptr_t>(&v[0]);   // keep only the address value
    for (int i = 0; i < 1000; ++i) v.push_back(i);
    std::printf("vector moved its storage: %s\n",
                reinterpret_cast<std::uintptr_t>(&v[0]) != before ? "yes" : "no");
    std::puts("invalidation demo passed");
}
```

**Common bug pattern -- erasing during iteration:**

```cpp
// WRONG: invalidates iterator
std::vector<int> v = {1, 2, 3, 4, 5};
for (auto it = v.begin(); it != v.end(); ++it) {
    if (*it % 2 == 0) v.erase(it);  // BUG: it is invalidated
}

// CORRECT: erase returns next valid iterator
for (auto it = v.begin(); it != v.end(); ) {
    if (*it % 2 == 0)
        it = v.erase(it);   // erase returns iterator to next element
    else
        ++it;
}

// BEST: use erase-remove idiom
v.erase(std::remove_if(v.begin(), v.end(),
    [](int x) { return x % 2 == 0; }), v.end());

// C++20: std::erase_if
std::erase_if(v, [](int x) { return x % 2 == 0; });
```

## 8.3 Key Algorithms (`<algorithm>`)

### Sorting and Ordering

```cpp
std::vector<int> v = {5, 2, 8, 1, 9, 3};

std::sort(v.begin(), v.end());                  // {1, 2, 3, 5, 8, 9}
std::sort(v.begin(), v.end(), std::greater<>{}); // {9, 8, 5, 3, 2, 1}

std::stable_sort(v.begin(), v.end());           // preserves relative order of equal elements

std::partial_sort(v.begin(), v.begin()+3, v.end()); // top 3 sorted, rest unspecified

std::nth_element(v.begin(), v.begin()+2, v.end()); // v[2] is in its sorted position;
                                                     // elements before are <=, after are >=
```

### Searching (on sorted ranges)

```cpp
std::vector<int> v = {1, 2, 3, 5, 8, 9};

std::binary_search(v.begin(), v.end(), 5);       // true
std::lower_bound(v.begin(), v.end(), 5);          // iterator to first >= 5
std::upper_bound(v.begin(), v.end(), 5);          // iterator to first > 5
auto [lo, hi] = std::equal_range(v.begin(), v.end(), 5); // [lower_bound, upper_bound)
```

### Searching (unsorted)

```cpp
std::find(v.begin(), v.end(), 5);                 // iterator to 5, or end()
std::find_if(v.begin(), v.end(), [](int x) { return x > 4; }); // first > 4
std::count(v.begin(), v.end(), 5);                // number of 5s
std::count_if(v.begin(), v.end(), [](int x) { return x > 4; });
std::any_of(v.begin(), v.end(), [](int x) { return x > 8; });   // true
std::all_of(v.begin(), v.end(), [](int x) { return x > 0; });   // true
std::none_of(v.begin(), v.end(), [](int x) { return x < 0; });  // true
```

### Transforming

```cpp
std::vector<int> src = {1, 2, 3, 4, 5};
std::vector<int> dst(5);

std::transform(src.begin(), src.end(), dst.begin(),
    [](int x) { return x * x; });  // dst = {1, 4, 9, 16, 25}

std::for_each(src.begin(), src.end(), [](int& x) { x *= 2; });  // in-place

int sum = std::accumulate(src.begin(), src.end(), 0);  // from <numeric>

std::reverse(src.begin(), src.end());
std::rotate(src.begin(), src.begin()+2, src.end()); // rotate left by 2
std::fill(dst.begin(), dst.end(), 0);
std::iota(dst.begin(), dst.end(), 1);  // {1, 2, 3, 4, 5} from <numeric>
```

### Removing (Erase-Remove Idiom)

`std::remove` / `std::remove_if` moves unwanted elements to the end and returns an iterator to the new logical end. You must call `erase` to actually shrink the container:

```cpp
std::vector<int> v = {1, 2, 3, 2, 4, 2, 5};

// Remove all 2s
auto new_end = std::remove(v.begin(), v.end(), 2);
v.erase(new_end, v.end());  // v = {1, 3, 4, 5}

// In one line:
v.erase(std::remove_if(v.begin(), v.end(),
    [](int x) { return x < 3; }), v.end());
```

### Partitioning

```cpp
std::vector<int> v = {5, 2, 8, 1, 9, 3};

auto pivot = std::partition(v.begin(), v.end(),
    [](int x) { return x < 5; });  // elements < 5 before pivot, >= 5 after

std::stable_partition(v.begin(), v.end(),
    [](int x) { return x % 2 == 0; }); // preserves relative order within partitions
```

## 8.4 Lambda Expressions

### Syntax

```
[capture](parameters) mutable -> return_type { body }
```

```cpp
auto add = [](int a, int b) -> int { return a + b; };
add(3, 4);  // 7

auto greet = [] { std::cout << "Hello!\n"; };
greet();
```

### Capture Modes

| Capture | Meaning |
|---|---|
| `[]` | Nothing captured |
| `[=]` | All local variables by value (copy) |
| `[&]` | All local variables by reference |
| `[x]` | Capture `x` by value |
| `[&x]` | Capture `x` by reference |
| `[=, &x]` | All by value except `x` by reference |
| `[&, x]` | All by reference except `x` by value |
| `[this]` | Capture `this` pointer (access members by reference) |
| `[*this]` | Capture `*this` by value (copy the object) (C++17) |

```cpp
int multiplier = 3;
auto times = [multiplier](int x) { return x * multiplier; };
times(5);  // 15

int total = 0;
std::for_each(v.begin(), v.end(), [&total](int x) { total += x; });

// Mutable: allows modifying captured-by-value variables (the copy, not the original)
int count = 0;
auto counter = [count]() mutable { return ++count; };
counter();  // 1
counter();  // 2
// count is still 0 (lambda modified its internal copy)
```

### Generic Lambdas (C++14)

Use `auto` parameters for template-like behavior:

```cpp
auto print = [](const auto& x) { std::cout << x << "\n"; };
print(42);        // int
print("hello");   // const char*
print(3.14);      // double
```

### Immediately Invoked Lambda Expression (IILE)

Useful for complex initialization of `const` variables:

```cpp
const auto config = [&]() {
    Config c;
    c.width = parse_width(args);
    c.height = parse_height(args);
    c.fullscreen = check_flag(args, "--fullscreen");
    return c;
}();  // note the () -- invoked immediately
```

## 8.5 `std::function` and Type Erasure

`std::function<R(Args...)>` stores any callable with a matching signature. It uses **type erasure** -- internally employing virtual dispatch and potentially heap allocation:

```cpp
#include <functional>

std::function<int(int, int)> op;
op = [](int a, int b) { return a + b; };   // lambda
op = std::plus<int>{};                       // functor
op = &free_function;                         // function pointer

// Use case: storing callbacks
class Button {
    std::function<void()> on_click_;
public:
    void set_callback(std::function<void()> cb) { on_click_ = std::move(cb); }
    void click() { if (on_click_) on_click_(); }
};
```

**When to avoid `std::function`:** In hot loops or performance-critical code, prefer templates (zero overhead) over `std::function` (virtual dispatch + possible heap allocation).

## 8.6 Ranges (C++20)

Ranges compose operations lazily using the pipe (`|`) operator:

```cpp
#include <ranges>
#include <vector>

std::vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

auto result = v
    | std::views::filter([](int x) { return x % 2 == 0; })  // {2, 4, 6, 8, 10}
    | std::views::transform([](int x) { return x * x; })     // {4, 16, 36, 64, 100}
    | std::views::take(3);                                     // {4, 16, 36}

for (int x : result) {
    std::cout << x << " ";  // 4 16 36
}

// Views are lazy -- no intermediate containers are created
// Operations are applied element-by-element as you iterate
```

### Common Views

| View | Description |
|---|---|
| `std::views::filter(pred)` | Keep elements satisfying predicate |
| `std::views::transform(fn)` | Apply function to each element |
| `std::views::take(n)` | First n elements |
| `std::views::drop(n)` | Skip first n elements |
| `std::views::reverse` | Reverse order |
| `std::views::keys` | Keys of a map-like range |
| `std::views::values` | Values of a map-like range |
| `std::views::iota(start)` | Infinite sequence: start, start+1, ... |
| `std::views::zip(r1, r2)` | Pair up elements from two ranges (C++23) |
| `std::views::split(delim)` | Split range by delimiter |
| `std::views::join` | Flatten nested ranges |

---

## Common Interview Questions -- STL

**Q: When would you use `std::map` vs `std::unordered_map`?**

Use `std::unordered_map` when you need O(1) average lookup and don't need ordered traversal. Use `std::map` when you need elements sorted by key, need `lower_bound`/`upper_bound` queries, or the hash function for your key type is expensive or produces many collisions. `std::map` guarantees O(log n) worst case; `std::unordered_map` can degrade to O(n) with bad hash distribution.

**Q: What is the erase-remove idiom?**

`std::remove` doesn't actually erase elements from a container -- it moves elements to be kept to the front and returns an iterator to the new logical end. You must call `container.erase(new_end, container.end())` to actually remove the dead elements. C++20 introduced `std::erase` and `std::erase_if` which combine both steps.

**Q: Why is `std::vector` usually preferred over `std::list`?**

Despite `std::list` having O(1) insert/remove, `std::vector`'s contiguous memory layout makes it much more cache-friendly, leading to faster iteration in practice. The O(n) shift cost of `vector` insert/erase is often cheaper than the cache-miss cost of traversing a linked list. Stroustrup's benchmarks show vector outperforming list even for workloads with frequent middle insertions up to surprisingly large sizes.

**Q: What are the capture semantics of C++ lambdas?**

`[=]` captures all referenced local variables by copy; `[&]` captures by reference. You can mix modes: `[=, &x]` captures everything by value except `x` by reference. Capture-by-reference lambdas that outlive the captured variables cause dangling references. `[this]` captures the enclosing object's pointer; `[*this]` (C++17) captures a copy of the object.

### Advanced Questions -- Container Internals and Invalidation

**Q1.** Prove that `vector::push_back` is amortized O(1). Why not grow by a fixed 1000 elements instead?

With growth factor g, reallocations happen at capacities 1, g, g², ..., and the elements copied over all of them sum to n/g + n/g² + ... = n/(g-1), a geometric series. With g = 2 that is fewer than n copies for n pushes, so total work under 2n, which is O(1) per push. (Potential-function argument: charge 3 units per push, 1 to insert and 2 banked to pay for moving itself and one older element at the next doubling.) With fixed growth `+k`, there are n/k reallocations copying k, 2k, ..., n elements: Θ(n²/k) total, which is Θ(n) per push for fixed k. Pushing 10M elements with k = 1000 means 10,000 reallocations and about 5·10^10 element copies, compared with about 10^7 for doubling. Follow-up: g = 1.5 trades about 2n copies for the chance to reuse freed memory (g below the golden ratio) and at most 33% slack instead of 50%.

**Q2.** A `std::vector<Widget>` reallocation profile shows `Widget`'s copy constructor, although `Widget` has a move constructor. Why?

`vector` reallocation uses `std::move_if_noexcept`: it moves only when the move constructor is `noexcept` (or the type is move-only). Otherwise a throw halfway through would leave some elements moved-from in the old buffer and break `push_back`'s strong guarantee, so the vector copies instead. A user-written `Widget(Widget&&)` without `noexcept`, or an implicitly generated move constructor that is not `noexcept` because a member's move can throw, triggers the copy path. Fix: declare `Widget(Widget&&) noexcept`, or `= default` it when all members are nothrow-movable, and enforce it with `static_assert(std::is_nothrow_move_constructible_v<Widget>)`.

**Q3.** Why does `deque::push_back` invalidate iterators but not references?

A deque is a "map" (array) of pointers to fixed-size blocks. `push_back` either constructs into the current last block or allocates a new block, so existing elements never move and references stay valid. When the map itself is full, it is reallocated (re-centred) to make room for more block pointers. A deque iterator stores `{cur, first, last, node}`, where `node` points *into the map*, so every iterator is invalidated even though no element moved. Insertion in the middle shifts elements and invalidates both.

**Q4.** Why can't `std::unordered_map` use open addressing like `absl::flat_hash_map`, and when would you choose each?

The standard requires that references and pointers to elements survive rehashing, and it exposes the bucket interface (`bucket()`, local iterators, `bucket_size()`). Both effectively require one heap node per element with chaining. Open addressing stores elements inline, so a rehash or (in some designs) an erase moves them. Choose `flat_hash_map` for lookup-heavy maps with small keys and values: roughly 2x to 3x less memory and 1 to 2 cache misses per lookup instead of 2 to 3. Choose `std::unordered_map` (or `absl::node_hash_map`) when you hold pointers to values across inserts, when values are huge or immovable, or when you need `extract`/`merge`.

**Q5.** For a lookup table of 200 integer keys that is built once and queried millions of times, which container would you pick?

Measure, but the likely winner is a **sorted `std::vector<std::pair<int,V>>` with `std::lower_bound`** (or C++23 `std::flat_map`). 200 pairs fit in a few KB and stay in L1/L2. A binary search is about 8 well-predicted comparisons over contiguous memory, with no hashing, no modulo, and no pointer chasing. `unordered_map` costs a hash, a division by a prime, and 2 to 3 dependent loads into separately allocated nodes. `std::map` costs about 8 dependent node loads. For dense small keys, a direct-indexed `std::array<V, N>` beats everything. For string keys, a perfect hash or a flat hash map is the usual answer.

**Q6.** What is SSO, how big is it, and show a bug that only happens with short strings.

Small string optimization stores short strings inside the `std::string` object instead of on the heap: 15 chars in libstdc++ and MSVC (`sizeof` = 32) and 22 in libc++ (`sizeof` = 24). Bug: `std::vector<std::string> names; ... std::string_view first = names[0]; names.push_back(x);`. If `names[0]` was long, the reallocation *moved* the string, and the new string adopted the same heap buffer, so `first` still points at valid characters by luck. If `names[0]` was short, its characters lived inside the old string object, which reallocation destroyed, so `first` dangles. The test suite with long names passes, and production with 8-char kernel names crashes. ASan reports heap-use-after-free on the old vector buffer.

**Q7.** Your `std::sort` call crashes with a segfault inside libstdc++, only for some inputs. What do you look for first?

The comparator. `std::sort` requires a *strict weak ordering*: irreflexive (`comp(a,a)` is false), transitive, with transitive equivalence. Common violations: `<=` instead of `<`; comparing floats that include NaN; a comparator using mutable or random state; or "compare by x, then by y" written wrongly (`a.x < b.x || a.y < b.y`). libstdc++'s introsort uses *unguarded* insertion sort and partition loops that rely on `comp(pivot, pivot) == false` as a sentinel, so a bad comparator walks past the array bounds. Fix with `std::tie(a.x, a.y) < std::tie(b.x, b.y)` or a defaulted `<=>`. Use `std::ranges::sort` with a projection where possible, and catch these in debug builds with `-D_GLIBCXX_DEBUG`, which checks irreflexivity.

**Q8.** Estimate the memory of `std::map<int, int>` vs `std::unordered_map<int, int>` vs `absl::flat_hash_map<int, int>` with 10 million entries.

`std::map`: 40-byte nodes in 48-byte malloc chunks, about **480 MB**. `std::unordered_map`: 16-byte nodes in 32-byte chunks (320 MB) plus a bucket array of about 10M x 8 B (80 MB, since the bucket count is at least the size at load factor 1.0), about **400 MB**. `absl::flat_hash_map`: capacity is the next 2^k - 1 that keeps load at or below 7/8, which is about 16.8M (2^24 - 1) slots x (8 B + 1 control byte), about **150 MB**. A sorted `std::vector<std::pair<int,int>>`: **80 MB**. The raw payload is 80 MB in every case, so the node-based containers carry 5x to 6x overhead, mostly malloc headers and pointers.

**Q9.** How do you erase elements from an `unordered_map` (or `map`) while iterating?

Use the iterator returned by `erase`: `for (auto it = m.begin(); it != m.end(); ) { if (pred(*it)) it = m.erase(it); else ++it; }`. Erasing invalidates only the erased element's iterator, and `erase` never triggers a rehash, so the returned iterator is valid. Simpler since C++20: `std::erase_if(m, pred)`. *Inserting* while iterating an unordered container is the dangerous case, because any insert can rehash and invalidate every iterator.

---

# Part 4: Modern C++ Features

---

# 9. C++11/14 Features

---

C++11 was a transformative release -- often called "Modern C++." C++14 added incremental improvements.

## 9.1 `auto` and `decltype`

Covered in detail in [Section 1.3](#13-auto-and-decltype). Key additions in C++14:

```cpp
// C++14: auto return type deduction for functions
auto add(int a, int b) {
    return a + b;  // compiler deduces return type as int
}

// C++14: decltype(auto)
decltype(auto) get_ref(std::vector<int>& v) {
    return v[0];  // returns int&, not int (preserves reference)
}

// C++14: generic lambdas
auto identity = [](auto x) { return x; };
```

## 9.2 Range-Based `for` Loop

Iterates over anything that provides `begin()` and `end()`:

```cpp
std::vector<int> v = {1, 2, 3, 4, 5};

for (int x : v) { /* x is a copy */ }
for (int& x : v) { x *= 2; /* modifies v */ }
for (const auto& x : v) { /* read-only, no copy -- preferred */ }

// Works with initializer lists, arrays, and any range-like type
for (int x : {10, 20, 30}) { /* ... */ }
int arr[] = {1, 2, 3};
for (int x : arr) { /* ... */ }
```

## 9.3 `nullptr`

Type-safe null pointer constant. See [Section 2.1](#21-raw-pointers) for details.

## 9.4 Uniform Initialization (Brace Initialization)

Curly braces `{}` provide a universal initialization syntax:

```cpp
int x{42};                          // direct initialization
int y = {42};                       // copy-list-initialization
std::vector<int> v{1, 2, 3};       // initializer_list constructor
std::pair<int, double> p{1, 3.14};

struct Point { int x, y; };
Point pt{10, 20};                  // aggregate initialization
```

### Narrowing Conversions -- Prevented by Braces

```cpp
int a = 3.14;    // OK: silently truncates to 3 (narrowing)
// int b{3.14};  // ERROR: narrowing conversion not allowed in braces
// int c{1000};  // OK if int can hold 1000
```

### `std::initializer_list` Trap

When a constructor accepts `std::initializer_list`, braces **strongly prefer** it:

```cpp
std::vector<int> v1(5, 1);    // 5 elements, each = 1: {1, 1, 1, 1, 1}
std::vector<int> v2{5, 1};    // 2 elements: {5, 1}  -- initializer_list wins!

// auto deduction with braces
auto x = {1, 2, 3};  // std::initializer_list<int> -- often surprising
auto y = {42};        // std::initializer_list<int>, NOT int
```

## 9.5 `constexpr`

Marks functions and variables that **can** be evaluated at compile time:

```cpp
constexpr int square(int x) { return x * x; }
constexpr int val = square(5);    // computed at compile time: 25

// C++11: constexpr functions limited to a single return statement
// C++14: allows loops, local variables, multiple statements
constexpr int factorial(int n) {
    int result = 1;
    for (int i = 2; i <= n; ++i)
        result *= i;
    return result;
}
static_assert(factorial(5) == 120);

// constexpr variables must be initialized with a constant expression
constexpr double pi = 3.14159265358979;
```

**Key insight:** `constexpr` functions can be called at runtime too -- `constexpr` means "can be evaluated at compile time," not "must be."

## 9.6 `static_assert`

Compile-time assertion that produces a clear error message:

```cpp
static_assert(sizeof(int) == 4, "int must be 4 bytes");
static_assert(sizeof(void*) == 8, "64-bit platform required");

template <typename T>
void process(T value) {
    static_assert(std::is_integral_v<T>, "T must be an integral type");
    // ...
}
```

## 9.7 `override` and `final`

```cpp
class Base {
public:
    virtual void foo() const;
    virtual void bar(int);
    virtual void baz() const;
};

class Derived : public Base {
public:
    void foo() const override;       // OK: matches Base::foo
    // void foo() override;          // ERROR: signature mismatch (missing const)
    void bar(int) override;          // OK
    void baz() const final;          // OK: cannot be overridden further
};

class LeafClass final : public Derived {  // no class can inherit from LeafClass
    // void baz() const override;   // ERROR: baz is final in Derived
};
```

`override` catches signature mismatches at compile time. `final` prevents further overriding (or further inheritance when applied to a class).

## 9.8 Delegating and Inheriting Constructors

### Delegating Constructors

One constructor calls another in the same class:

```cpp
class Connection {
    std::string host_;
    int port_;
    bool secure_;
public:
    Connection(std::string host, int port, bool secure)
        : host_(std::move(host)), port_(port), secure_(secure) {}

    Connection(std::string host, int port)
        : Connection(std::move(host), port, false) {}  // delegates

    Connection(std::string host)
        : Connection(std::move(host), 80) {}            // chains delegation
};
```

### Inheriting Constructors

Bring base class constructors into derived class:

```cpp
class Base {
public:
    Base(int x);
    Base(int x, int y);
};

class Derived : public Base {
public:
    using Base::Base;  // inherits all Base constructors
    // Derived(int x) : Base(x) {} -- no longer needed
};

Derived d(42);  // calls Base(int)
```

## 9.9 `std::initializer_list`

Enables functions and constructors to accept brace-enclosed lists:

```cpp
#include <initializer_list>

class IntSet {
    std::vector<int> data_;
public:
    IntSet(std::initializer_list<int> il) : data_(il) {}
    void add(std::initializer_list<int> il) {
        data_.insert(data_.end(), il.begin(), il.end());
    }
};

IntSet s = {1, 2, 3, 4, 5};
s.add({6, 7, 8});
```

## 9.10 Other C++11/14 Features

| Feature | Description |
|---|---|
| `= default` / `= delete` | Explicitly default or delete special member functions |
| User-defined literals | `operator""_km`, `operator""_s` for custom suffixes |
| `noexcept` | Specifier and operator for exception specifications |
| `thread_local` | Thread-local storage duration |
| `alignas` / `alignof` | Control and query alignment |
| `[[deprecated]]` | Mark entities as deprecated |
| Digit separators (C++14) | `int x = 1'000'000;` for readability |
| Binary literals (C++14) | `int b = 0b1010;` |
| `std::make_unique` (C++14) | Factory for `unique_ptr` |

---

# 10. C++17 Features

---

## 10.1 Structured Bindings

Decompose aggregates, pairs, tuples, and structs into named variables:

```cpp
// With pairs/tuples
std::map<std::string, int> scores = {{"alice", 90}, {"bob", 85}};
for (const auto& [name, score] : scores) {
    std::cout << name << ": " << score << "\n";
}

// With custom structs
struct Point { double x, y, z; };
Point p{1.0, 2.0, 3.0};
auto [x, y, z] = p;  // x=1.0, y=2.0, z=3.0

// With arrays
int arr[] = {10, 20, 30};
auto [a, b, c] = arr;

// Useful for multi-return values
auto [iter, inserted] = mymap.insert({"key", 42});
if (inserted) { /* newly inserted */ }
```

## 10.2 `if` / `switch` with Initializers

Limit variable scope to the `if`/`switch` block:

```cpp
// Before C++17
auto it = mymap.find("key");
if (it != mymap.end()) {
    use(it->second);
}
// 'it' still visible here

// C++17
if (auto it = mymap.find("key"); it != mymap.end()) {
    use(it->second);
}
// 'it' not visible here

if (auto [iter, ok] = mymap.insert({"key", 42}); ok) {
    std::cout << "Inserted: " << iter->second << "\n";
}
```

## 10.3 `std::optional`

Represents a value that may or may not be present (replaces sentinel values and output parameters):

```cpp
#include <optional>

std::optional<int> find_index(const std::vector<int>& v, int target) {
    for (size_t i = 0; i < v.size(); ++i) {
        if (v[i] == target) return i;
    }
    return std::nullopt;
}

auto result = find_index(v, 42);
if (result) {                    // or result.has_value()
    std::cout << *result;        // or result.value()
}

result.value_or(-1);             // returns -1 if empty
```

## 10.4 `std::variant`

Type-safe union -- holds exactly one of the specified types:

```cpp
#include <variant>

std::variant<int, double, std::string> data;

data = 42;                                // holds int
data = 3.14;                              // now holds double
data = "hello";                           // now holds string

// Access
std::get<std::string>(data);              // "hello"
// std::get<int>(data);                   // throws std::bad_variant_access

std::get_if<int>(&data);                  // returns nullptr (not holding int)
std::get_if<std::string>(&data);          // returns pointer to string

data.index();                             // 2 (0-based index of active type)

// Visitor pattern
std::visit([](auto&& val) {
    std::cout << val << "\n";
}, data);

// Overloaded visitor (with helper)
template<class... Ts> struct overloaded : Ts... { using Ts::operator()...; };

std::visit(overloaded{
    [](int i)                { std::cout << "int: " << i << "\n"; },
    [](double d)             { std::cout << "double: " << d << "\n"; },
    [](const std::string& s) { std::cout << "string: " << s << "\n"; }
}, data);
```

## 10.5 `std::any`

Type-safe container for any single value. More flexible but less efficient than `variant`:

```cpp
#include <any>

std::any a = 42;
a = std::string("hello");
a = 3.14;

double d = std::any_cast<double>(a);          // OK
// int i = std::any_cast<int>(a);             // throws std::bad_any_cast

if (a.type() == typeid(double)) { /* ... */ }
a.has_value();   // true
a.reset();       // empty
```

## 10.6 `std::string_view`

Non-owning, lightweight view into a contiguous character sequence. Avoids copying strings for read-only access:

```cpp
#include <string_view>

void process(std::string_view sv) {
    sv.substr(0, 5);       // returns a new string_view (no allocation)
    sv.find("world");
    sv.size();
    sv.remove_prefix(3);   // "lo world" -- modifies the view, not the data
}

process("hello world");                    // no string construction
std::string s = "hello world";
process(s);                                // no copy
process(std::string_view(s.data(), 5));    // view of first 5 chars
```

**Warning:** `string_view` does not own the data. If the underlying string is destroyed, the view dangles.

## 10.7 Class Template Argument Deduction (CTAD)

Compiler deduces class template arguments from constructor arguments:

```cpp
std::pair p{1, 3.14};                 // std::pair<int, double>
std::vector v{1, 2, 3};              // std::vector<int>
std::optional o{42};                  // std::optional<int>
std::tuple t{1, "hello", 3.14};      // std::tuple<int, const char*, double>
std::lock_guard lk{mutex};           // std::lock_guard<std::mutex>
```

## 10.8 Fold Expressions

Covered in [Section 6.5](#65-variadic-templates).

## 10.9 Filesystem Library

```cpp
#include <filesystem>
namespace fs = std::filesystem;

fs::path p = "/home/user/docs/file.txt";
p.filename();       // "file.txt"
p.extension();      // ".txt"
p.parent_path();    // "/home/user/docs"
p.stem();           // "file"

fs::exists(p);
fs::file_size(p);
fs::is_regular_file(p);
fs::is_directory(p);

fs::create_directories("/tmp/a/b/c");
fs::copy("src.txt", "dst.txt");
fs::remove("file.txt");
fs::rename("old.txt", "new.txt");

// Iterate directory
for (const auto& entry : fs::directory_iterator("/tmp")) {
    std::cout << entry.path() << "\n";
}

// Recursive iteration
for (const auto& entry : fs::recursive_directory_iterator("/tmp")) {
    if (entry.is_regular_file() && entry.path().extension() == ".cpp") {
        std::cout << entry.path() << "\n";
    }
}
```

## 10.10 Attributes

| Attribute | Purpose |
|---|---|
| `[[nodiscard]]` | Warn if return value is discarded |
| `[[maybe_unused]]` | Suppress unused variable/parameter warnings |
| `[[fallthrough]]` | Indicate intentional fall-through in `switch` |
| `[[deprecated("msg")]]` | Mark as deprecated |

```cpp
[[nodiscard]] int compute() { return 42; }
// compute();  // WARNING: discarding return value

void handler([[maybe_unused]] int error_code) {
    // no warning even though error_code is unused
}

switch (x) {
    case 1:
        do_something();
        [[fallthrough]];   // no warning for missing break
    case 2:
        do_both();
        break;
}
```

## 10.11 Other C++17 Features

| Feature | Description |
|---|---|
| `std::byte` | Type for raw byte manipulation |
| `std::invoke` | Uniform callable invocation |
| `std::apply` | Apply tuple elements as function arguments |
| `std::clamp(val, lo, hi)` | Clamp a value to a range |
| `std::gcd`, `std::lcm` | Greatest common divisor, least common multiple |
| Nested namespaces | `namespace A::B::C { }` |
| `inline` variables | Define variables in headers without ODR violations |
| `if constexpr` | Covered in [Section 6.7](#67-if-constexpr-c17) |

---

# 11. C++20 Features

---

## 11.1 Concepts

Covered in detail in [Section 6.8](#68-concepts-c20). Concepts replace SFINAE with readable constraints:

```cpp
template <std::integral T>
T gcd(T a, T b) {
    while (b) { a %= b; std::swap(a, b); }
    return a;
}
```

## 11.2 Ranges

Covered in [Section 8.6](#86-ranges-c20). Composable, lazy view adaptors replace raw iterator pairs.

## 11.3 Coroutines

Coroutines are functions that can suspend and resume execution. Three new keywords:

| Keyword | Purpose |
|---|---|
| `co_await` | Suspend until an awaitable completes |
| `co_yield` | Suspend and produce a value |
| `co_return` | Complete the coroutine with a final value |

```cpp
#include <coroutine>
#include <iostream>

// Simple generator
template <typename T>
struct Generator {
    struct promise_type {
        T current_value;
        Generator get_return_object() {
            return Generator{std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        std::suspend_always initial_suspend() { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        std::suspend_always yield_value(T value) {
            current_value = value;
            return {};
        }
        void return_void() {}
        void unhandled_exception() { std::terminate(); }
    };

    std::coroutine_handle<promise_type> handle;

    Generator(std::coroutine_handle<promise_type> h) : handle(h) {}
    ~Generator() { if (handle) handle.destroy(); }

    bool next() {
        handle.resume();
        return !handle.done();
    }
    T value() const { return handle.promise().current_value; }
};

Generator<int> fibonacci() {
    int a = 0, b = 1;
    while (true) {
        co_yield a;
        int next = a + b;
        a = b;
        b = next;
    }
}

// Usage
auto gen = fibonacci();
for (int i = 0; i < 10 && gen.next(); ++i) {
    std::cout << gen.value() << " ";  // 0 1 1 2 3 5 8 13 21 34
}
```

The example above is the "hello world". Interviews for systems roles go one level deeper: *what does the compiler actually generate, who owns the frame, and when does it die?*

### How the Compiler Transforms a Coroutine

A function is a coroutine if its body contains `co_await`, `co_yield`, or `co_return`. The compiler looks up `std::coroutine_traits<ReturnType, Params...>::promise_type` (by default `ReturnType::promise_type`) and rewrites the body roughly as:

```cpp
// fragment -- approximate lowering of   R f(Params... ps) { <body> }
R f(Params... ps) {
    auto* frame = new coroutine_frame;                 // (1) promise_type::operator new if declared
    frame->params = std::move(ps)...;                  // (2) by-value params moved INTO the frame
    promise_type& p = frame->promise;                  // (3) constructed (with ps... if such a ctor exists)
    R result = p.get_return_object();                  // (4) handed to the caller at first suspension
    co_await p.initial_suspend();                      // (5) suspend_always => lazy, suspend_never => eager
    try {
        <body>                                         // (6) co_yield e  ==> co_await p.yield_value(e)
                                                       //     co_return e ==> p.return_value(e); goto final;
                                                       //     co_return;  ==> p.return_void();   goto final;
    } catch (...) {
        p.unhandled_exception();                       // (7) store, rethrow, or terminate
    }
final:
    co_await p.final_suspend();                        // (8) MUST be noexcept
    // (9) if final_suspend did not suspend: destroy promise, params, free frame
}
```

| Step | Hook | What to know |
|---|---|---|
| Frame allocation | `promise_type::operator new(size_t [, params...])` | Default is global `operator new`. Frame holds the promise, copies of parameters, and every local that lives across a suspension point. Size is only known after optimization, which is why it is not `sizeof`-able |
| Allocation failure | `static R get_return_object_on_allocation_failure()` | If declared, the compiler uses `operator new(size, std::nothrow)` and returns this on failure |
| Parameters | -- | **By-value parameters are moved into the frame; reference parameters stay references.** A `const std::string&` bound to a temporary dangles after the first suspension |
| Return object | `get_return_object()` | Usually wraps `coroutine_handle<promise_type>::from_promise(*this)` |
| Start policy | `initial_suspend()` | `suspend_always` = lazy (task does nothing until awaited, which makes continuation wiring race-free); `suspend_never` = eager |
| Values | `yield_value(e)`, `return_value(e)` / `return_void()` | A promise has **either** `return_value` **or** `return_void`, never both. Flowing off the end of a coroutine whose promise has no `return_void` is UB |
| Exceptions | `unhandled_exception()` | Typically `error = std::current_exception();` and rethrow in `await_resume` |
| End | `final_suspend() noexcept` | If it suspends, the frame lives until someone calls `handle.destroy()`. If it does not suspend, the frame self-destroys and every outstanding handle dangles |

### Awaitables: `await_ready`, `await_suspend`, `await_resume`

`co_await expr` first obtains an *awaiter*: `promise.await_transform(expr)` if the promise declares it, then `operator co_await` if one exists, otherwise `expr` itself. The awaiter's three methods drive suspension:

```cpp
// fragment -- what  auto r = co_await awaiter;  expands to
if (!awaiter.await_ready()) {              // false => we need to suspend
    /* coroutine is now suspended: locals saved in the frame */
    <result of awaiter.await_suspend(this_handle)>;   // see table below
    /* <resume point> */
}
auto r = awaiter.await_resume();           // value of the co_await expression
```

| `await_suspend` returns | Meaning |
|---|---|
| `void` | Stay suspended; control returns to whoever called `resume()` (or to the original caller) |
| `bool` | `true` = stay suspended; `false` = cancel the suspension and resume immediately (useful when the operation completed synchronously) |
| `std::coroutine_handle<P>` | **Symmetric transfer**: resume *that* coroutine as a tail call. Return `std::noop_coroutine()` to mean "just return to the resumer" |

The standard library ships two trivial awaiters: `std::suspend_always` (`await_ready` returns `false`) and `std::suspend_never` (returns `true`).

A custom awaitable that moves the rest of the coroutine onto another thread (the classic "switch executor" pattern):

```cpp
// Build: g++ -std=c++20 -O2 -pthread await.cpp
#include <coroutine>
#include <exception>
#include <iostream>
#include <stdexcept>
#include <thread>

auto resume_on_new_thread(std::jthread& out) {
    struct awaiter {
        std::jthread* out;
        bool await_ready() const noexcept { return false; }        // always suspend
        void await_suspend(std::coroutine_handle<> h) {            // void: stay suspended
            std::jthread& o = *out;                                // copy what we need to locals FIRST
            if (o.joinable()) throw std::runtime_error("busy");
            std::jthread th([h] { h.resume(); });                  // resume on new thread
            o = std::move(th);
            // Never touch *this after the thread starts: this awaiter lives in the
            // coroutine frame, which the other thread may already have run to
            // completion and freed (final_suspend is suspend_never).
        }
        void await_resume() const noexcept {}                      // co_await yields void
    };
    return awaiter{&out};
}

// Fire-and-forget coroutine type: eager start, frame frees itself at the end.
struct fire_and_forget {
    struct promise_type {
        fire_and_forget get_return_object() noexcept { return {}; }
        std::suspend_never initial_suspend() noexcept { return {}; }  // run immediately
        std::suspend_never final_suspend() noexcept { return {}; }    // auto-destroy frame
        void return_void() noexcept {}
        void unhandled_exception() { std::terminate(); }
    };
};

fire_and_forget work(std::jthread& out) {
    std::cout << "before: " << std::this_thread::get_id() << '\n';
    co_await resume_on_new_thread(out);
    std::cout << "after:  " << std::this_thread::get_id() << '\n';   // different id
}

int main() {
    std::jthread t;
    work(t);
}   // ~jthread joins the thread that runs the rest of work()
```

> **Why `await_suspend` copies `out` into a local first.** The original one-liner `*out = std::jthread([h]{ h.resume(); });` starts the thread *before* it reads `this->out` for the assignment. The new thread can resume `work`, finish it, and free the frame (which contains the awaiter) before that read happens: a use-after-free that ThreadSanitizer reports on essentially every run. The rule: once the handle has been handed to another thread, treat the awaiter and everything else in the frame as gone. With Clang + `-fsanitize=thread` the fixed version is clean; GCC 15 + TSan may still flag a race on the frame's internal resume index here, which is a compiler codegen issue, not a bug in this code.

### Coroutine Frame Allocation and HALO

- Every coroutine call allocates a frame on the heap by default (tens to hundreds of bytes; big local arrays that live across a `co_await` make it big).
- **HALO** (Heap Allocation eLision Optimization): when the compiler can prove the coroutine's lifetime is strictly nested inside the caller and it can see the frame size (the coroutine body is inlinable), it places the frame in the caller's frame. Clang's `CoroElide` pass does this for simple lazy-task patterns; treat it as a bonus, never as a guarantee.
- **Custom allocation**: declare `operator new`/`operator delete` in `promise_type` (for example, carve frames from a per-thread pool or arena). If `operator new` takes `(std::size_t, Params...)`, it receives the coroutine's arguments, which is how `std::generator` supports `std::allocator_arg_t, alloc` leading parameters.
- Performance rule of thumb: a coroutine call costs an allocation plus an indirect call per resume, so do not make a tight inner loop body a coroutine.

### Symmetric Transfer

Problem: if task A awaits task B and B finishes synchronously, a naive `final_suspend` that calls `continuation.resume()` makes A run *inside* B's stack frame. A loop of 1,000,000 synchronously-completing `co_await`s then needs 1,000,000 nested stack frames and overflows.

Fix: have `await_suspend` **return** the next handle. The compiler then resumes it as a tail call, so the stack stays flat. The standard describes this as "resume the target coroutine", and leaving the tail call to the implementation makes it quality-of-implementation. In testing with GCC 15.2, a 100,000-deep await chain ran fine at `-O2` but overflowed the stack at `-O0` and under ASan, because those builds do not emit the tail call. Keep that in mind when a coroutine test crashes only in debug builds.

### A Minimal `task<T>` (Lazy, Awaitable, Symmetric Transfer)

```cpp
// Build: g++ -std=c++20 -O2 task.cpp
#include <coroutine>
#include <cstdio>
#include <exception>
#include <optional>
#include <stdexcept>
#include <utility>

template <typename T>
class task {
public:
    struct promise_type {
        std::optional<T> value;
        std::exception_ptr error;
        std::coroutine_handle<> continuation = std::noop_coroutine();

        task get_return_object() {
            return task{std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        std::suspend_always initial_suspend() noexcept { return {}; }  // lazy start

        // At the end, resume whoever awaited us by RETURNING its handle
        // (symmetric transfer) instead of calling .resume() (nested stack frames).
        struct final_awaiter {
            bool await_ready() noexcept { return false; }
            std::coroutine_handle<> await_suspend(
                std::coroutine_handle<promise_type> h) noexcept {
                return h.promise().continuation;
            }
            void await_resume() noexcept {}
        };
        final_awaiter final_suspend() noexcept { return {}; }

        template <typename U>
        void return_value(U&& v) { value.emplace(std::forward<U>(v)); }
        void unhandled_exception() { error = std::current_exception(); }
    };

    task(task&& o) noexcept : h_(std::exchange(o.h_, {})) {}
    task(const task&) = delete;
    ~task() { if (h_) h_.destroy(); }   // frame is suspended at final_suspend: safe

    // Awaiter interface: lets one task co_await another.
    bool await_ready() const noexcept { return false; }
    std::coroutine_handle<> await_suspend(std::coroutine_handle<> awaiting) noexcept {
        h_.promise().continuation = awaiting;  // who to resume when we finish
        return h_;                             // symmetric transfer: start the child
    }
    T await_resume() {
        if (h_.promise().error) std::rethrow_exception(h_.promise().error);
        return std::move(*h_.promise().value);
    }

    // Blocking entry point for main(). Single-threaded demo: everything completes
    // synchronously, so one resume() runs the whole chain to the end.
    T sync_wait() {
        h_.resume();
        return await_resume();
    }

private:
    explicit task(std::coroutine_handle<promise_type> h) : h_(h) {}
    std::coroutine_handle<promise_type> h_;
};

task<int> leaf(int x) { co_return x * 2; }

task<int> middle(int x) {
    int a = co_await leaf(x);       // suspends middle, transfers to leaf
    int b = co_await leaf(x + 1);   // leaf's final_suspend transfers back
    co_return a + b;
}

task<int> deep(int n) {             // n-deep await chain: each hop is a tail call
    if (n == 0) co_return 0;        // when the compiler emits one (see above)
    co_return 1 + co_await deep(n - 1);
}

task<int> may_throw(bool fail) {
    if (fail) throw std::runtime_error("boom");
    co_return 7;
}

int main() {
    std::printf("middle(10) = %d\n", middle(10).sync_wait());   // 20 + 22 = 42
    std::printf("deep(1000) = %d\n", deep(1000).sync_wait());   // 1000
    try {
        may_throw(true).sync_wait();
    } catch (const std::exception& e) {
        std::printf("caught: %s\n", e.what());                  // caught: boom
    }
}
```

What a production `task<T>` (cppcoro, folly::coro, libunifex, `std::execution` in C++26) adds: a real scheduler/executor, `task<void>` and `task<T&>` specializations, cancellation, a thread-safe `sync_wait` that blocks on a latch, and allocator support.

### A Range-For Generator (Pre-C++23)

C++23 standardizes this as `std::generator` ([11.10](#1110-c23-features)). Writing one by hand shows how iterators drive `resume()`:

```cpp
// Build: g++ -std=c++20 -O2 gen.cpp
#include <coroutine>
#include <cstddef>
#include <cstdio>
#include <exception>
#include <memory>
#include <utility>

template <typename T>
class generator {
public:
    struct promise_type {
        const T* current = nullptr;   // points into the suspended frame: no copy
        std::exception_ptr error;

        generator get_return_object() {
            return generator{std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        std::suspend_always initial_suspend() noexcept { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }  // keep frame for done()
        std::suspend_always yield_value(const T& v) noexcept {
            current = std::addressof(v);   // v outlives the suspension
            return {};
        }
        void return_void() noexcept {}
        void unhandled_exception() { error = std::current_exception(); }
        void await_transform() = delete;   // forbid co_await inside a generator
    };

    struct sentinel {};
    class iterator {
        std::coroutine_handle<promise_type> h_;
    public:
        using value_type = T;
        using difference_type = std::ptrdiff_t;
        explicit iterator(std::coroutine_handle<promise_type> h) : h_(h) {}
        const T& operator*() const { return *h_.promise().current; }
        iterator& operator++() {
            h_.resume();
            if (h_.done() && h_.promise().error) std::rethrow_exception(h_.promise().error);
            return *this;
        }
        void operator++(int) { ++*this; }
        bool operator==(sentinel) const { return h_.done(); }
    };

    iterator begin() {
        h_.resume();   // run to the first co_yield
        if (h_.done() && h_.promise().error) std::rethrow_exception(h_.promise().error);
        return iterator{h_};
    }
    sentinel end() noexcept { return {}; }

    generator(generator&& o) noexcept : h_(std::exchange(o.h_, {})) {}
    ~generator() { if (h_) h_.destroy(); }   // destroying a suspended frame runs
                                             // the destructors of its live locals
private:
    explicit generator(std::coroutine_handle<promise_type> h) : h_(h) {}
    std::coroutine_handle<promise_type> h_;
};

generator<unsigned long long> fibonacci(int n) {
    unsigned long long a = 0, b = 1;
    for (int i = 0; i < n; ++i) {
        co_yield a;
        a = std::exchange(b, a + b);
    }
}

int main() {
    for (auto v : fibonacci(10)) std::printf("%llu ", v);   // 0 1 1 2 3 5 8 13 21 34
    std::puts("");
}
```

### Coroutine Pitfalls

| Pitfall | Why it breaks | Fix |
|---|---|---|
| Reference parameter to a temporary: `task<> f(const std::string& s)` called as `f("x")` | The temporary dies at the end of the full-expression in the caller; the lazy coroutine reads `s` later | Take parameters **by value** in coroutines |
| Lambda coroutine with captures: `[x]() -> task<> { co_await y; use(x); }()` | The closure object is *not* copied into the frame; `this`-like access to captures dangles once the temporary lambda dies | Pass data as parameters, keep the lambda alive, or (C++23) use `this auto self` by value |
| Holding a `std::lock_guard` across `co_await` | The coroutine may resume on another thread; unlocking a `std::mutex` from a thread that does not own it is UB. Even on one thread it serializes everything | Release before `co_await`, or use an async mutex (e.g., `cppcoro::async_mutex`) |
| `thread_local` across `co_await` | Resuming on a different thread silently changes which instance you see | Store per-coroutine state in the frame, not in TLS |
| `final_suspend` not `noexcept` | Ill-formed | Mark it `noexcept` |
| Resuming a coroutine that is `done()`, or destroying one that is running | UB | Track ownership in one RAII handle type |
| Forgetting to `destroy()` a frame suspended at `final_suspend` | Memory leak (sanitizers report it) | RAII wrapper as above |
| Touching the awaiter (or any frame-resident state) in `await_suspend` after handing the handle to another thread | The other thread may resume the coroutine, run it to completion and destroy the frame first: use-after-free | Copy what you need into locals first; make starting the other thread the last thing that reads `*this` |

### Stackless (C++20) vs Stackful Coroutines

| | C++20 coroutines (stackless) | Stackful (Boost.Context/Fiber, ucontext, Go goroutines) |
|---|---|---|
| Suspend from | Only the coroutine body itself (not from a nested normal call) | Anywhere in the call stack |
| Memory | One heap frame sized to the live-across-suspension state (often < 1 KiB) | A whole stack per coroutine (KiB-MiB, often guard-paged) |
| Switch cost | A function call/return | Register save/restore + stack switch |
| "Function coloring" | Yes: callers must also be coroutines to `co_await` | No |
| Scale | Millions of concurrent tasks are cheap | Limited by stack memory |

> **See also:** [Python generator functions](./Python_Fundamentals.md#72-generator-functions) (the same lazy-sequence idea with a stackless frame object).

## 11.4 Modules

Modules replace header files, providing faster compilation, better encapsulation, and no macro leakage:

```cpp
// math.cppm (module interface unit)
export module math;

export int add(int a, int b) { return a + b; }
export int multiply(int a, int b) { return a * b; }

int internal_helper() { return 42; }  // not exported -- invisible to importers

// main.cpp
import math;

int main() {
    add(3, 4);       // OK
    multiply(5, 6);  // OK
    // internal_helper(); // ERROR: not exported
}
```

| Feature | Headers | Modules |
|---|---|---|
| Include model | Textual copy-paste | Compiled binary interface |
| Compilation speed | Slow (re-parsed every TU) | Fast (parsed once) |
| Macro isolation | Macros leak across headers | No macro leakage |
| Include order matters | Yes | No |
| ODR risk | High | Low |

### Module Unit Kinds

A *named module* is made of several translation units ("module units"):

| Unit kind | Declaration | Role |
|---|---|---|
| Primary module interface unit | `export module M;` | Exactly one per module; defines what importers of `M` see |
| Module implementation unit | `module M;` | Function bodies, private helpers. Implicitly imports `M`. Cannot be imported. Editing it does not force importers to recompile |
| Module interface partition | `export module M:part;` | Splits a large interface across files. Must be re-exported by the primary interface (`export import :part;`) |
| Module implementation (internal) partition | `module M:part;` | Internal declarations shared between units of `M`; never visible to importers |
| Global module fragment | `module;` ... before the module declaration | The correct place to `#include` legacy headers (an `#include` after `export module M;` would attach the header's declarations to `M`); their declarations belong to the "global module" and their macros do not leak to importers |
| Private module fragment | `module :private;` | Lets a single-file module keep implementation details in the same file (only allowed in a primary interface that is the module's only unit) |

### A Multi-File Module with Partitions

```cpp
// fragment -- five files shown together; build commands follow
// ---- geometry-shapes.cppm : interface partition
export module geometry:shapes;
export struct Rect {
    double w, h;
    double area() const { return w * h; }
};

// ---- geometry-detail.cpp : internal (implementation) partition
module geometry:detail;
double clamp_positive(double x) { return x < 0 ? 0 : x; }

// ---- geometry.cppm : primary interface unit
module;                        // global module fragment
#include <cmath>               // macros from here do NOT leak to importers
export module geometry;
export import :shapes;         // re-export the partition
import :detail;                // visible here, not to importers
export double hypotenuse(double a, double b);       // defined in the impl unit
export inline double scaled_area(const Rect& r, double k) {
    return r.area() * clamp_positive(k);
}

// ---- geometry_impl.cpp : implementation unit
module;
#include <cmath>
module geometry;
double hypotenuse(double a, double b) { return std::sqrt(a * a + b * b); }

// ---- main.cpp
#include <cstdio>
import geometry;
int main() {
    Rect r{3, 4};
    std::printf("area=%g hyp=%g scaled=%g\n", r.area(), hypotenuse(3, 4), scaled_area(r, 2));
    // clamp_positive(1.0);   // error: not visible (internal partition)
}
```

Manual build with GCC 15. Order matters: a unit can only be compiled after the BMIs it imports exist. GCC writes BMIs to `gcm.cache/`:

```bash
g++ -std=c++20 -fmodules -c geometry-shapes.cppm   # -> gcm.cache/geometry-shapes.gcm
g++ -std=c++20 -fmodules -c geometry-detail.cpp    # -> gcm.cache/geometry-detail.gcm
g++ -std=c++20 -fmodules -c geometry.cppm          # needs both partitions' BMIs
g++ -std=c++20 -fmodules -c geometry_impl.cpp      # needs geometry.gcm
g++ -std=c++20 -fmodules -c main.cpp
g++ *.o -o app && ./app                            # area=12 hyp=5 scaled=24
```

The same project with CMake (3.28+, Ninja 1.11+ or Visual Studio 2022 generator):

```cmake
cmake_minimum_required(VERSION 3.28)
project(geometry_demo LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(geometry)
target_sources(geometry
    PUBLIC FILE_SET CXX_MODULES FILES   # every interface unit AND every partition
        geometry.cppm geometry-shapes.cppm geometry-detail.cpp
    PRIVATE geometry_impl.cpp)          # plain implementation unit

add_executable(app main.cpp)
target_link_libraries(app PRIVATE geometry)
```

### Header Units and `import std`

| Mechanism | Syntax | Macros leak? | Status (2026-11) |
|---|---|---|---|
| Named module | `import geometry;` | No | Compilers: GCC 11+ (`-fmodules-ts`; GCC 15 also accepts `-fmodules`), Clang 15+, MSVC 19.28+. CMake's `FILE_SET CXX_MODULES` scanning requires GCC 14+, Clang 16+, MSVC 19.34+ |
| Header unit | `import <vector>;` / `import "my.h";` | **Yes** (a header unit exports its macros) | Compiler support exists, for example `g++ -std=c++20 -fmodules -x c++-system-header vector`. **CMake does not support header units** |
| Standard library module (C++23) | `import std;` / `import std.compat;` (also puts C names like `::printf` in the global namespace) | No (use `<cassert>`/`<cstdio>` for macros like `assert`, `EOF`) | GCC 15+, Clang 18+ with libc++, MSVC 17.5+. CMake: `CXX_MODULE_STD` target property (added 3.30), still behind the `CMAKE_EXPERIMENTAL_CXX_IMPORT_STD` gate as of CMake 4.2 |

```bash
# GCC 15: build the std module once, then import it (tested with g++ 15.2)
g++ -std=c++23 -fmodules -fsearch-include-path -c bits/std.cc   # -> gcm.cache/std.gcm + std.o
g++ -std=c++23 -fmodules hello.cpp std.o -o hello                # hello.cpp: import std;
```

### Why Modules Are a Build-System Problem

- **Dependency scanning.** With headers, every TU compiles independently. With modules, `main.cpp` cannot be compiled until `geometry.gcm` exists, and you only learn that by *scanning* sources for `import`. Compilers emit scan results in the P1689 JSON format (`clang-scan-deps`, GCC `-fdeps-format=p1689r5`, MSVC `/scanDependencies`), and Ninja's `dyndep` feature lets CMake add those edges at build time (CMake requires Ninja 1.11+ for this).
- **Reduced parallelism.** Module dependencies serialize part of the build graph. A deep chain of modules can make clean builds slower on 64 cores even though each TU is cheaper.
- **BMIs are not portable.** A BMI (`.gcm`, `.pcm`, `.ifc`) is tied to the exact compiler, version, and many flags (`-std`, `-fno-exceptions`, defines). Libraries ship interface *sources* (`install(TARGETS ... FILE_SET CXX_MODULES DESTINATION ...)`), and every consumer rebuilds the BMI.
- **Semantics change slightly.** Member functions defined inside a class body in a named module are *not* implicitly `inline` (P1779). Non-exported entities have module linkage, so two modules can each have a private `helper()` without an ODR clash.
- **Visibility vs reachability.** A non-exported type returned from an exported function is *reachable* (you can call its members through `auto`) but not *visible* (you cannot name it).

> **See also:** [CMake -- C++20 Modules Support](../tools/CMake_Fundamentals.md#62-c20-modules-support) for `FILE_SET CXX_MODULES` details and scanning configuration.

## 11.5 Three-Way Comparison (`<=>`) -- Spaceship Operator

Generates all six comparison operators from a single declaration:

```cpp
#include <compare>

struct Point {
    int x, y;
    auto operator<=>(const Point&) const = default;
    // Compiler generates: ==, !=, <, >, <=, >=
};

Point a{1, 2}, b{1, 3};
a < b;    // true  (lexicographic: x compared first, then y)
a == b;   // false
a != b;   // true

// Custom spaceship
struct CaseInsensitiveString {
    std::string s;
    std::strong_ordering operator<=>(const CaseInsensitiveString& other) const {
        auto to_lower = [](char c) { return std::tolower(c); };
        return std::lexicographical_compare_three_way(
            s.begin(), s.end(), other.s.begin(), other.s.end(),
            [&](char a, char b) { return to_lower(a) <=> to_lower(b); });
    }
    bool operator==(const CaseInsensitiveString& other) const {
        return (*this <=> other) == 0;
    }
};
```

### Comparison Categories

| Category | Meaning | Example Types |
|---|---|---|
| `std::strong_ordering` | Exactly one of `<`, `==`, `>` | `int`, `string` |
| `std::weak_ordering` | Equivalent but not necessarily identical | Case-insensitive strings |
| `std::partial_ordering` | May be unordered | `float` (NaN) |

## 11.6 `std::format`

Type-safe, Python-like string formatting:

```cpp
#include <format>

std::string s = std::format("Hello, {}!", "world");          // "Hello, world!"
std::string n = std::format("{:06.2f}", 3.14159);            // "003.14"
std::string t = std::format("{0} is {1}, {0} is {1}!", "C++", "great");
                                                              // "C++ is great, C++ is great!"
// Fill, align, width
std::format("{:<10}", "left");    // "left      "
std::format("{:>10}", "right");   // "     right"
std::format("{:^10}", "center");  // "  center  "

// Integer formats
std::format("{:d}", 42);     // "42"
std::format("{:x}", 255);    // "ff"
std::format("{:o}", 8);      // "10"
std::format("{:b}", 10);     // "1010"
std::format("{:#x}", 255);   // "0xff"
```

## 11.7 `consteval` and `constinit`

| Keyword | Meaning |
|---|---|
| `constexpr` | **Can** be evaluated at compile time |
| `consteval` | **Must** be evaluated at compile time (C++20) |
| `constinit` | Variable must be **initialized** at compile time, but can be modified at runtime (C++20) |

```cpp
consteval int compile_time_only(int x) { return x * x; }
constexpr int maybe_compile_time(int x) { return x * x; }

constexpr int a = compile_time_only(5);  // OK: compile time
// int b = compile_time_only(runtime_val); // ERROR: must be compile time

constinit int global = compile_time_only(10);  // initialized at compile time
// No static initialization order fiasco
void foo() { global = 42; }  // OK: can modify at runtime
```

## 11.8 `std::span`

Non-owning view over a contiguous sequence of elements (like `string_view` but for any type):

```cpp
#include <span>

void process(std::span<const int> data) {
    for (int x : data) { /* ... */ }
    data.size();
    data[0];
    data.subspan(1, 3);     // view of elements [1, 4)
    data.first(3);           // view of first 3 elements
    data.last(2);            // view of last 2 elements
}

std::vector<int> v = {1, 2, 3, 4, 5};
process(v);                  // implicit conversion

int arr[] = {1, 2, 3};
process(arr);                // works with C arrays

std::array<int, 5> a = {1, 2, 3, 4, 5};
process(a);                  // works with std::array
```

**Fixed-size spans:** `std::span<int, 5>` guarantees exactly 5 elements at compile time.

## 11.9 Other C++20 Features

| Feature | Description |
|---|---|
| `std::jthread` | Joining thread -- automatically joins on destruction |
| `std::stop_token` | Cooperative thread cancellation |
| `std::counting_semaphore` | Semaphore synchronization primitive (see [12.12](#1212-c20-synchronization-primitives)) |
| `std::latch` / `std::barrier` | Thread coordination primitives (see [12.12](#1212-c20-synchronization-primitives)) |
| `std::source_location` | Replacement for `__FILE__`, `__LINE__` |
| `constexpr` containers | `std::vector` and `std::string` in constexpr contexts |
| `std::bit_cast` | Type-safe reinterpretation of bit patterns |
| `using enum` | Import enum values into current scope |
| Designated initializers | `Point{.x = 1, .y = 2}` |
| `char8_t` | UTF-8 character type |
| Template lambdas | `[]<typename T>(T x) { ... }` |

## 11.10 C++23 Features

C++23 is a "finish C++20" release: it completes ranges and coroutines library support and adds several features that interviewers now expect you to know. Compile with `-std=c++23`.

### Compiler Support Snapshot (GCC / libstdc++)

| Feature | First GCC | Notes |
|---|---|---|
| `if consteval`, multidimensional `operator[]`, `std::expected`, `std::move_only_function` | 12 | |
| `views::zip`, `views::enumerate`, `chunk`, `slide`, `stride`, `ranges::fold_left`, `ranges::contains` | 13 | |
| Deducing `this`, `std::print`/`std::println`, `std::generator`, `ranges::to` | 14 | |
| `std::flat_map`/`flat_set`, formatting ranges (`println("{}", vec)`), `import std` | 15 | |
| `std::mdspan` | 16 | Clang/libc++ and MSVC shipped it earlier |
| `std::stacktrace` | 12 | Link with `-lstdc++exp` (GCC 14+) |

Clang/libc++ and MSVC differ feature by feature (libc++ was still missing `std::generator` at the time of writing). Check the cppreference "C++23 compiler support" page before relying on a feature in portable code.

### `std::expected<T, E>` -- Value or Error, Without Exceptions

`expected` holds either a `T` or an `E`. Unlike `optional`, the failure case carries *why*. Unlike exceptions, the error path is visible in the signature and costs nothing extra when it is taken. The monadic operations chain fallible steps without `if` ladders:

| Member | Callable signature | Use |
|---|---|---|
| `and_then(f)` | `T -> expected<U, E>` | Next fallible step |
| `transform(f)` | `T -> U` | Map the value, keep the error |
| `or_else(f)` | `E -> expected<T, E2>` | Recover from or translate an error |
| `transform_error(f)` | `E -> E2` | Map the error type (e.g., errno -> domain enum) |
| `value_or(v)`, `*e`, `e.error()`, `if (e)` | -- | Access. `*e` on an error is UB, while `.value()` throws `bad_expected_access` |

### `std::print` / `std::println`

`std::format` syntax, written straight to `stdout` (or a `FILE*`): `std::println(stderr, "x = {}", x);`. It avoids iostream's stateful manipulators and per-`<<` call overhead, is type-safe unlike `printf`, and handles Unicode output correctly on Windows consoles. Format strings are checked at compile time.

### Deducing `this` (Explicit Object Parameter)

A member function can name its object parameter explicitly: `void f(this Self&& self)`. One template then covers `&`, `const&`, `&&`, and `const&&`:

| Problem before C++23 | With deducing `this` |
|---|---|
| Duplicate `const`/non-`const` (and `&&`) overloads of accessors | One `template <class Self> auto&& get(this Self&& self)` |
| CRTP needed just so a base can call the derived class | `this auto& self` in the base deduces the derived type |
| Recursive lambdas needed `std::function` or a Y-combinator | `[](this auto const& self, int n) { ... self(n - 1) ... }` |
| Taking `*this` by value for small types | `this Point self` (by-value object parameter) |

Inside such a function there is no implicit `this` pointer: members are accessed through `self.`.

### `if consteval`

Branches on whether the current evaluation is a constant evaluation. It replaces `if (std::is_constant_evaluated())` and fixes its classic trap: `if constexpr (std::is_constant_evaluated())` is **always true**, because the `if constexpr` condition itself is constant-evaluated. Inside the `if consteval` branch you may call `consteval` functions.

### `std::generator<T>`

The standard coroutine generator from [11.3](#113-coroutines). It is a `std::ranges::view`, so it composes with views: `fib() | views::take(10)`. It supports recursive yielding with `co_yield std::ranges::elements_of(other_gen)`. The consumer then resumes the innermost generator directly instead of bouncing through every level, which matters for recursive tree walks. Its reference type defaults to `T&&`, and yielded lvalues are copied.

### `std::flat_map` / `std::flat_set`

A sorted associative container adapter over two contiguous sequences (by default `std::vector<Key>` and `std::vector<T>`):

| | `std::map` | `std::flat_map` | `std::unordered_map` |
|---|---|---|---|
| Layout | Red-black tree, one node per element | Two sorted vectors (keys and values) | Buckets of nodes |
| Lookup | O(log n), pointer chasing (cache misses) | O(log n) binary search over contiguous keys (cache-friendly) | O(1) average |
| Insert/erase | O(log n) | **O(n)** (shifts elements) | O(1) average |
| Iterator/reference stability | Stable | Invalidated by insert/erase | Iterators invalidated on rehash |
| Memory per element | ~3 pointers + color + payload | Payload only | Node + bucket overhead |
| Best for | Frequent mutation, stable references | Build once, look up often; small maps | Large maps, no ordering needed |

Tip: bulk-build with the `std::sorted_unique` constructor tag to avoid O(n^2) repeated inserts.

### Ranges Additions

| Addition | Example | Result |
|---|---|---|
| `std::ranges::to<C>()` | `v \| views::filter(even) \| ranges::to<std::vector>()` | Materialize a view into a container |
| `views::enumerate` | `for (auto [i, x] : v \| views::enumerate)` | `(index, element)` pairs |
| `views::zip`, `zip_transform` | `views::zip(a, b)` | Tuples of corresponding elements |
| `views::adjacent<N>`, `pairwise` | `v \| views::pairwise` | Sliding tuples of N neighbours |
| `views::chunk(n)`, `chunk_by(pred)` | `v \| views::chunk(4)` | Sub-ranges of n (last may be short) |
| `views::slide(n)` | `v \| views::slide(3)` | Overlapping windows |
| `views::stride(n)` | `v \| views::stride(2)` | Every n-th element |
| `views::join_with(sep)` | `words \| views::join_with(' ')` | Join with a delimiter |
| `views::cartesian_product`, `repeat`, `as_rvalue`, `as_const` | -- | Misc. view factories/adaptors |
| `ranges::fold_left/right`, `contains`, `starts_with`, `ends_with`, `find_last` | `ranges::fold_left(v, 0, std::plus{})` | Algorithms (`fold_left` replaces `std::accumulate` for ranges) |

### Complete C++23 Tour

```cpp
// Build: g++ -std=c++23 -O2 cpp23.cpp   (tested with GCC 15.2)
#include <charconv>
#include <expected>
#include <flat_map>
#include <functional>
#include <generator>
#include <print>
#include <ranges>
#include <string>
#include <string_view>
#include <utility>
#include <vector>

// ---- std::expected: value OR error, monadic chaining.
enum class ParseError { empty, not_a_number, out_of_range };

std::expected<int, ParseError> parse_int(std::string_view s) {
    if (s.empty()) return std::unexpected(ParseError::empty);
    int v{};
    auto [ptr, ec] = std::from_chars(s.data(), s.data() + s.size(), v);
    if (ec == std::errc::result_out_of_range) return std::unexpected(ParseError::out_of_range);
    if (ec != std::errc{} || ptr != s.data() + s.size())
        return std::unexpected(ParseError::not_a_number);
    return v;
}

std::expected<int, ParseError> checked_permille(std::string_view s) {
    return parse_int(s)
        .and_then([](int v) -> std::expected<int, ParseError> {   // T -> expected<U, E>
            if (v < 0 || v > 100) return std::unexpected(ParseError::out_of_range);
            return v;
        })
        .transform([](int v) { return v * 10; });                   // T -> U
}

// ---- deducing this: one body for const / non-const / rvalue objects.
struct Buffer {
    std::vector<int> data{1, 2, 3};
    template <typename Self>
    auto&& at(this Self&& self, std::size_t i) {        // replaces 3-4 overloads
        return std::forward<Self>(self).data[i];
    }
};

// ...and recursive lambdas without std::function:
auto fib = [](this auto const& self, int n) -> int {
    return n < 2 ? n : self(n - 1) + self(n - 2);
};

// ---- if consteval: different code for compile time and run time.
constexpr double fast_sqrt(double x) {
    if consteval {
        double r = x;                                    // Newton iterations at compile time
        for (int i = 0; i < 30; ++i) r = 0.5 * (r + x / r);
        return r;
    } else {
        return __builtin_sqrt(x);                        // hardware sqrt at run time
    }
}
static_assert(fast_sqrt(16.0) == 4.0);

// ---- std::generator: a standard coroutine generator that is also a view.
std::generator<int> squares(int n) {
    for (int i = 0; i < n; ++i) co_yield i * i;
}

int main() {
    std::println("hello {} {:>6.2f}", "C++23", 3.14159);            // hello C++23   3.14

    for (std::string_view s : {"42", "", "abc", "250"}) {
        if (auto r = checked_permille(s)) std::println("'{}' -> {}", s, *r);
        else std::println("'{}' -> error {}", s, std::to_underlying(r.error()));
    }   // '42' -> 420 / '' -> error 0 / 'abc' -> error 1 / '250' -> error 2

    Buffer b;
    b.at(0) = 10;                                        // Self = Buffer&
    const Buffer& cb = b;
    std::println("at: {} {}  fib(10)={}", cb.at(0), cb.at(2), fib(10));   // 10 3 55

    std::flat_map<std::string, int> fm{{"b", 2}, {"a", 1}, {"c", 3}};
    fm["d"] = 4;
    for (const auto& [k, v] : fm) std::print("{}={} ", k, v);           // a=1 b=2 c=3 d=4
    std::println("");

    std::vector<int> v{1, 2, 3, 4, 5, 6};
    auto evens = v | std::views::filter([](int x) { return x % 2 == 0; })
                   | std::ranges::to<std::vector>();
    std::println("evens={} sum={} has4={}", evens,
                 std::ranges::fold_left(v, 0, std::plus{}), std::ranges::contains(v, 4));
    for (auto [i, x] : v | std::views::enumerate | std::views::take(2))
        std::println("enumerate {}:{}", i, x);                          // 0:1, 1:2
    std::println("chunk(4)={} slide(3)={} stride(2)={}",
                 v | std::views::chunk(4), v | std::views::slide(3), v | std::views::stride(2));
    // chunk(4)=[[1, 2, 3, 4], [5, 6]] slide(3)=[[1, 2, 3], [2, 3, 4], ...] stride(2)=[1, 3, 5]
    std::vector<char> letters{'a', 'b', 'c'};
    std::println("zip={}", std::views::zip(v, letters));   // [(1, 'a'), (2, 'b'), (3, 'c')]
    std::println("squares={}", squares(6) | std::views::drop(1) | std::ranges::to<std::vector>());
}
```

### `std::mdspan` -- Multidimensional Views (HPC/GPU Relevant)

`mdspan<T, Extents, LayoutPolicy, AccessorPolicy>` is a non-owning view: a pointer plus a shape (extents) plus a mapping from indices to offsets. It came out of the Kokkos/Sandia HPC world, and it is the vocabulary type for C++26 `<linalg>` (BLAS-style algorithms).

- **Extents**: static (`std::extents<size_t, 3, 4>`, which stores nothing), dynamic (`std::dextents<size_t, 2>`), or mixed. With all-static extents, `sizeof(mdspan) == sizeof(T*)`.
- **Layouts**: `layout_right` (C/row-major, the last index varies fastest), `layout_left` (Fortran/column-major, which is also what BLAS/rocBLAS/cuBLAS assume by default), and `layout_stride` (arbitrary strides, for sub-matrices and transposes).
- **Accessors**: customize how elements are loaded. This is the hook for atomic access, restrict/aligned hints, or non-host memory.
- On GPUs it is useful because it is trivially copyable and only *views* memory, so it can be passed by value to a HIP/CUDA kernel wrapping a device pointer (when the toolchain's standard library headers are usable in device code).

```cpp
// Build: g++ -std=c++23 md.cpp   (needs libstdc++ 16+ / GCC 16; libc++ and MSVC also ship it)
#include <cstddef>
#include <cstdio>
#include <mdspan>

using Mat  = std::mdspan<float, std::dextents<std::size_t, 2>>;        // row-major
using CMat = std::mdspan<const float, std::dextents<std::size_t, 2>>;

void matmul(CMat A, CMat B, Mat C) {
    for (std::size_t i = 0; i < C.extent(0); ++i)
        for (std::size_t j = 0; j < C.extent(1); ++j) {
            float acc = 0;
            for (std::size_t k = 0; k < A.extent(1); ++k) acc += A[i, k] * B[k, j];
            C[i, j] = acc;                                // C++23 multidimensional []
        }
}

int main() {
    float a[] = {1, 2, 3, 4, 5, 6};                       // 2x3
    float b[] = {1, 0, 0, 1, 1, 1};                       // 3x2
    float c[4] = {};                                      // 2x2
    matmul(CMat(a, 2, 3), CMat(b, 3, 2), Mat(c, 2, 2));
    std::printf("%g %g\n%g %g\n", c[0], c[1], c[2], c[3]);   // 4 5 / 10 11

    // Same storage viewed column-major with compile-time extents:
    std::mdspan<float, std::extents<std::size_t, 2, 2>, std::layout_left> cm(c);
    std::printf("cm[0,1] = %g\n", cm[0, 1]);                 // c[2] = 10
    static_assert(sizeof(cm) == sizeof(float*));             // static extents: just a pointer
}
```

### Other C++23 Features Worth Knowing

| Feature | One-liner |
|---|---|
| `std::unreachable()` | Tells the optimizer a path cannot happen (UB if it does). For example, the `default:` of an exhaustive `switch` |
| `[[assume(expr)]]` | Optimizer hint; the expression is not evaluated. UB if false |
| `std::to_underlying(e)` | `static_cast<std::underlying_type_t<E>>(e)` without the boilerplate |
| `static operator()` / `static operator[]` | Stateless function objects with no `this` pointer to pass |
| `auto(x)` / `auto{x}` | Language-level decay-copy (a prvalue copy of `x`) |
| `std::move_only_function` | `std::function` that can hold move-only callables (for example, a lambda capturing a `unique_ptr`), with no const-correctness hole |
| `std::stacktrace` | Capture or print the current call stack (`std::stacktrace::current()`) |
| `std::byteswap`, `std::out_ptr`, `string::contains`, `string::resize_and_overwrite` | Small but handy library additions |
| `size_t` literal suffix `uz` | `for (auto i = 0uz; i < v.size(); ++i)` with no sign-compare warning |
| `#elifdef`, `#elifndef`, `#warning` | Preprocessor conveniences |

**Looking ahead to C++26** (WG21 finalized it in March 2026): static reflection, contracts (`pre`/`post`/`contract_assert`), `std::execution` (senders/receivers for async and GPU work), `<hazard_pointer>` and `<rcu>` (see [12.11](#1211-lock-free-data-structures-and-memory-reclamation)), `std::simd`, `std::inplace_vector`, `<linalg>`, and `submdspan`. `memory_order::consume` is deprecated.

---

## Common Interview Questions -- Modern C++

**Q: What is `std::optional` and when would you use it?**

`std::optional<T>` holds either a value of type `T` or nothing (`std::nullopt`). It replaces patterns like returning sentinel values (`-1`, `nullptr`), using output parameters, or throwing exceptions for expected missing values. It makes the absence of a value explicit in the type system and forces callers to handle both cases.

**Q: What is the spaceship operator (`<=>`)?**

The three-way comparison operator `<=>` returns an ordering category (`strong_ordering`, `weak_ordering`, or `partial_ordering`) from a single comparison. When defaulted (`auto operator<=>(const T&) const = default;`), the compiler automatically generates all six relational operators (`==`, `!=`, `<`, `>`, `<=`, `>=`) by performing member-wise comparison.

**Q: What is `std::string_view` and what are the risks?**

`std::string_view` is a non-owning, lightweight reference to a contiguous character sequence. It avoids unnecessary copies when you only need to read a string. The main risk is that it does not own the data -- if the underlying string is destroyed or reallocated, the view becomes dangling. Never store a `string_view` that outlives the data it references.

**Q: What problem do modules solve?**

Modules address three major issues with the `#include` model: (1) slow compilation due to repeated parsing of header contents, (2) macro leakage across translation units, and (3) fragile include-order dependencies. Modules are compiled once into a binary format and imported without re-parsing, significantly improving build times and encapsulation.

### Advanced Questions -- Coroutines, Modules, and C++23

**Q1.** Walk through everything that happens when you call a coroutine `task<int> f(std::string s)`.

The compiler allocates a frame with `promise_type::operator new`, or with global `new` if the promise has none. It moves `s` into the frame and constructs the promise. It calls `promise.get_return_object()` to build the `task` that the caller will receive. It then evaluates `co_await promise.initial_suspend()`. For a lazy task, that suspends, and control returns to the caller with the `task` object. The body runs when someone resumes the handle, usually by `co_await`ing the task. `co_return v` calls `promise.return_value(v)`, and an escaping exception goes to `unhandled_exception()`. The coroutine then evaluates `co_await promise.final_suspend()`, which must be `noexcept`. If that suspends, the frame stays alive until the owning `task` calls `handle.destroy()`. Destruction runs the destructors of the promise and the parameters, then frees the frame. Follow-up: *if `f` took `const std::string&` instead*, the frame would store only the reference, and calling `f("hi")` would dangle once the lazy task finally runs.

**Q2.** What are `await_ready`, `await_suspend`, and `await_resume`? What does it mean when `await_suspend` returns a `coroutine_handle`?

`await_ready()` is a fast path. If it returns `true`, the result is already available and the coroutine does not suspend. `await_suspend(h)` runs *after* the coroutine is suspended, which makes it safe to hand `h` to another thread. A `void` return keeps the coroutine suspended. A `bool` return can cancel the suspension by returning `false`. A returned handle is resumed immediately as a tail call (symmetric transfer). `await_resume()` produces the value of the `co_await` expression or rethrows an error. Symmetric transfer is what lets task A start child B and lets B resume A when it finishes without the stack growing by one frame per hop. Without it, long chains of synchronously-completing awaits overflow the stack.

**Q3.** Why are coroutine frames heap-allocated, and how do you avoid the cost?

A frame must outlive the call that created it, because the coroutine is suspended and resumed later, possibly on another thread. Its size also depends on which locals live across suspension points, and that is only known after optimization. Mitigations: (1) HALO, where the compiler elides the allocation when the coroutine is provably nested in the caller and its body is visible (Clang does this, but it is not guaranteed). (2) A custom `promise_type::operator new` that uses a pool or arena. (3) Do not use coroutines for tiny, hot functions.

**Q4.** Name three coroutine lifetime bugs.

(1) Reference parameters bound to temporaries, which are gone by the time a lazy coroutine runs. (2) A lambda coroutine reading its captures after the closure temporary is destroyed, because captures are not copied into the frame. (3) Holding a `std::mutex` lock across `co_await` and resuming on another thread, so the unlock happens on a non-owning thread (UB). Also: `thread_local` values change when a coroutine resumes on another thread, and a frame suspended at `final_suspend` leaks if nobody calls `destroy()`.

**Q5.** What is the difference between a module interface partition, an implementation partition, and an implementation unit?

An interface partition (`export module M:p;`) contributes exported declarations and must be re-exported from the primary interface (`export import :p;`). An implementation partition (`module M:p;`) holds internal declarations that other units of `M` can import (`import :p;`) but that importers of `M` never see. An implementation unit (`module M;`) cannot be imported at all: it holds definitions. Changing it recompiles only that file, which is the modules equivalent of editing a `.cpp` file instead of a header.

**Q6.** Why does CMake need Ninja 1.11+ (or Visual Studio) to build modules, and why can't you just ship `.gcm`/`.pcm` files?

The build order depends on `import` statements that are only discovered by scanning sources. CMake runs the compiler's P1689 dependency scanner and feeds the results into Ninja's dynamic dependencies (`dyndep`) so BMIs are built before their importers. BMIs are compiler-, version-, and flag-specific, so libraries install module interface *sources*, and each consumer builds its own BMIs.

**Q7.** Do macros leak through `import`?

Not through named modules: `import geometry;` brings no macros, and that is one of the main benefits. Header units (`import <vector>;`) *do* export macros, because they are a compiled form of a header. `import std;` exports no macros, so you still `#include <cassert>` for `assert`.

**Q8.** When would you return `std::expected` instead of throwing, returning `std::optional`, or returning an error code?

Use `expected<T, E>` when failure is an ordinary, anticipated outcome that the caller should handle locally (parsing, I/O lookups, validating user input). Examples include hot paths where exception cost or binary-size rules matter, and codebases built with `-fno-exceptions`. Use `optional` when "no value" needs no explanation. Use exceptions for rare failures that unwind many frames or that occur inside constructors and operators, which cannot return a status. Plain error codes are the C ABI fallback, but they make it easy to ignore the error and they do not carry a value. Pitfall: `*e` on an error is UB, while `e.value()` throws `bad_expected_access<E>`.

**Q9.** What does deducing `this` replace?

It replaces (1) duplicated `const`/non-`const`/`&&` overloads (one template with `this Self&& self` plus `std::forward<Self>(self).member`), (2) many CRTP uses (`this auto& self` in a base function deduces the most-derived type), and (3) the `std::function` or Y-combinator workaround for recursive lambdas. A follow-up is that there is no implicit `this` inside, so members must be accessed via `self.`. Such functions also cannot be `virtual`.

**Q10.** Why does HPC care about `std::mdspan`, and what is a layout policy?

HPC code has long passed `float* data, int ld, int rows, int cols` and computed `data[i * ld + j]` by hand, and getting the layout wrong is a classic bug. `mdspan` packages the pointer, the extents (static or dynamic), and the index mapping in a zero-overhead, trivially copyable view. The layout policy is that mapping: `layout_right` (row-major), `layout_left` (column-major, the default for BLAS/rocBLAS), or `layout_stride`. With static extents the compiler sees constant strides and can vectorize or unroll. C++26 builds `<linalg>` and `submdspan` on top of it.

**Q11.** `flat_map` vs `map` vs `unordered_map`: which do you choose?

`flat_map` stores sorted keys and values in contiguous vectors. Lookups are binary searches with excellent cache behavior, but insert and erase are O(n) and invalidate iterators. It is best for maps built once and read many times, and for small maps. `map` is best when you mutate often or need stable iterators and references. `unordered_map` gives O(1) average lookups for large maps without ordering, at the cost of a node per element and rehash pauses.

**Q12.** What is wrong with `if constexpr (std::is_constant_evaluated())`?

The condition of `if constexpr` is always constant-evaluated, so `is_constant_evaluated()` returns `true` and the runtime branch is discarded. C++23 `if consteval { ... } else { ... }` expresses the intent directly. Its first branch is an immediate-function context, so it can call `consteval` functions with arguments that are not constant expressions in the enclosing `constexpr` function.

---

# Part 5: Concurrency

---

# 12. Multithreading and Concurrency

---

## 12.1 `std::thread`

```cpp
#include <thread>

void worker(int id) {
    std::cout << "Thread " << id << " running\n";
}

std::thread t1(worker, 1);        // launch thread with function + args
std::thread t2([]{ /* ... */ });  // launch with lambda

t1.join();    // block until t1 finishes
t2.detach();  // let t2 run independently (daemon thread)

// CRITICAL: every std::thread must be joined or detached before destruction
// Destroying a joinable thread calls std::terminate()

std::thread::hardware_concurrency();  // number of logical CPU cores (hint)
```

### `std::jthread` (C++20)

Automatically joins on destruction and supports cooperative cancellation:

```cpp
#include <thread>
#include <stop_token>

void worker(std::stop_token stoken, int id) {
    while (!stoken.stop_requested()) {
        // do work
    }
}

{
    std::jthread jt(worker, 42);  // launches thread
    // ... do other work ...
}   // jt destroyed → automatically requests stop and joins
```

## 12.2 Mutexes

A **mutex** (mutual exclusion) protects shared data from concurrent access:

| Mutex Type | Description |
|---|---|
| `std::mutex` | Basic non-recursive mutex |
| `std::recursive_mutex` | Can be locked multiple times by the same thread |
| `std::timed_mutex` | Supports `try_lock_for` and `try_lock_until` |
| `std::shared_mutex` (C++17) | Multiple readers or single writer |

```cpp
#include <mutex>

std::mutex mtx;
int shared_data = 0;

void increment() {
    mtx.lock();
    ++shared_data;
    mtx.unlock();     // must unlock even if exception occurs -- prefer RAII wrappers
}
```

### RAII Lock Guards

Always use lock wrappers instead of raw `lock()`/`unlock()`:

| Lock Wrapper | Features |
|---|---|
| `std::lock_guard<M>` | Simple RAII lock -- locks on construction, unlocks on destruction |
| `std::unique_lock<M>` | Movable, supports deferred locking, try_lock, timed lock, condition variables |
| `std::scoped_lock<M...>` (C++17) | Locks multiple mutexes simultaneously (deadlock-free) |
| `std::shared_lock<M>` (C++17) | Shared (reader) lock for `shared_mutex` |

```cpp
// lock_guard -- simplest, sufficient for most cases
void safe_increment() {
    std::lock_guard<std::mutex> lock(mtx);
    ++shared_data;
}   // automatically unlocked

// unique_lock -- needed for condition variables and flexible locking
void flexible() {
    std::unique_lock<std::mutex> lock(mtx, std::defer_lock);
    // ... do non-critical work ...
    lock.lock();    // lock when ready
    ++shared_data;
    lock.unlock();  // unlock early if desired
}

// scoped_lock -- lock multiple mutexes (prevents deadlock)
std::mutex m1, m2;
void transfer() {
    std::scoped_lock lock(m1, m2);  // locks both atomically
    // ... safe to access data protected by m1 and m2 ...
}
```

### Read-Write Lock Pattern

```cpp
#include <shared_mutex>

class ThreadSafeCache {
    mutable std::shared_mutex mutex_;
    std::unordered_map<std::string, int> cache_;
public:
    int read(const std::string& key) const {
        std::shared_lock lock(mutex_);   // multiple readers allowed
        auto it = cache_.find(key);
        return it != cache_.end() ? it->second : -1;
    }

    void write(const std::string& key, int value) {
        std::unique_lock lock(mutex_);   // exclusive writer access
        cache_[key] = value;
    }
};
```

### `std::shared_mutex` in Depth

| Aspect | Detail |
|---|---|
| API | `lock()`/`unlock()`/`try_lock()` (exclusive) and `lock_shared()`/`unlock_shared()`/`try_lock_shared()` (shared). `std::shared_timed_mutex` (C++14) adds `try_lock_for`/`try_lock_shared_until` |
| Fairness | **Unspecified.** libstdc++ on Linux wraps `pthread_rwlock_t`, and glibc's default rwlock kind prefers readers, so a steady stream of readers can starve a writer. Other implementations, such as MSVC's SRWLOCK, behave differently |
| No upgrade | There is no shared-to-exclusive upgrade. Calling `lock()` while holding `lock_shared()` on the same mutex self-deadlocks (UB). Release, then re-acquire exclusively, then **re-check** the condition |
| No recursion | Re-locking in the same thread, whether shared or exclusive, is UB |
| Cost | Even a shared acquire is an atomic RMW on the lock word, so with many cores every reader bounces the same cache line. For short critical sections (a hash lookup), a plain `std::mutex` or sharded mutexes are often as fast or faster |
| When it wins | Reads dominate (>90%), critical sections are long enough to amortize the RMW, and there are enough readers to overlap |
| Alternatives for read-mostly data | Copy-on-write with `std::atomic<std::shared_ptr<const T>>` (readers do one atomic load), seqlocks, RCU (C++26 `<rcu>`), sharding by key hash |

The get-or-compute pattern, with the release-and-re-check step that interviewers look for:

```cpp
// fragment -- member of ThreadSafeCache above
int get_or_compute(const std::string& key) {
    {
        std::shared_lock rl(mutex_);
        if (auto it = cache_.find(key); it != cache_.end()) return it->second;
    }                                            // release shared: no upgrade exists
    int value = expensive_compute(key);          // compute outside any lock
    std::unique_lock wl(mutex_);
    auto it = cache_.try_emplace(key, value).first;   // re-check: another writer may
    return it->second;                                 // have inserted first; keep theirs
}
```

## 12.3 Condition Variables

Allow threads to wait for a condition to become true. Always used with a mutex and a predicate:

```cpp
#include <condition_variable>

std::mutex mtx;
std::condition_variable cv;
std::queue<int> buffer;
constexpr int MAX_SIZE = 10;

// Producer
void producer() {
    for (int i = 0; i < 100; ++i) {
        std::unique_lock lock(mtx);
        cv.wait(lock, [] { return buffer.size() < MAX_SIZE; });  // wait while full
        buffer.push(i);
        lock.unlock();
        cv.notify_one();  // wake one consumer
    }
}

// Consumer
void consumer() {
    while (true) {
        std::unique_lock lock(mtx);
        cv.wait(lock, [] { return !buffer.empty(); });  // wait while empty
        int val = buffer.front();
        buffer.pop();
        lock.unlock();
        cv.notify_one();  // wake producer
        process(val);
    }
}
```

**Why the predicate overload?** `cv.wait(lock, pred)` handles **spurious wakeups** -- the thread may be woken without `notify` being called. The predicate is re-checked after every wakeup.

### Condition Variable Pitfalls

`cv.wait(lk, pred)` is exactly `while (!pred()) cv.wait(lk);`. Every rule below follows from the fact that **a condition variable has no memory**: a `notify` with no waiter is simply lost, and only the shared state remembers anything.

| Pitfall | What goes wrong | Fix |
|---|---|---|
| **Lost wakeup**: waiting without checking state first, or modifying the state without holding the mutex | The consumer checks `ready == false`, the producer sets `ready = true` and notifies *before the consumer has blocked*, then the consumer blocks forever | Always wait with a predicate, and always modify the predicate's state **while holding the same mutex**, even if the flag is `std::atomic` |
| **Spurious wakeup**: `if (!ready) cv.wait(lk);` | `wait` may return with no notify (futex/EINTR behavior, and permitted by the standard), so the code proceeds with `ready == false` | Use a `while` loop or the predicate overload |
| **Stolen wakeup** | Between the notify and the woken thread re-acquiring the mutex, another thread can consume the item | The predicate re-check handles it |
| **Wrong `notify_one` target** | One cv shared by producers (waiting "not full") and consumers (waiting "not empty"): `notify_one` can wake a thread of the wrong kind, which goes back to sleep, and the system stalls | Use two cvs (`not_full_`, `not_empty_`) or `notify_all` |
| **No shutdown path** | Consumers wait forever for an item that never comes, and `join()` hangs | Put `closed_` in the predicate (`return closed_ \|\| !q.empty();`) and `notify_all` on close, or use `condition_variable_any` with a `std::stop_token` |
| **Work under the lock** | Processing an item while holding the mutex serializes all consumers | Pop under the lock, `unlock()`, then process |
| **Timed waits with `system_clock`** | Wall-clock jumps (NTP) shorten or extend the wait | `wait_until(lk, steady_clock::now() + timeout, pred)`. It returns the predicate's value, so a timeout with the condition true still counts as success |

**Notify inside or outside the lock?** Both are correct *as long as the state change happened under the lock*. Notifying after `unlock()` avoids "hurry up and wait", where the woken thread immediately blocks on the mutex the notifier still holds (glibc mitigates this partly). The exception: if the waiter may **destroy the condition variable** as soon as it wakes (for example, the cv lives in an object the waiter deletes when the count hits zero), notify while still holding the lock, so the cv cannot be destroyed mid-notify.

`std::condition_variable` works only with `std::unique_lock<std::mutex>`. `std::condition_variable_any` works with any lockable (for example, `shared_lock`) and has C++20 `std::stop_token` overloads, which makes cancellation clean:

```cpp
// Build: g++ -std=c++20 -O2 -pthread cv.cpp
#include <chrono>
#include <condition_variable>
#include <cstdio>
#include <mutex>
#include <queue>
#include <stop_token>
#include <thread>

std::mutex m;
std::condition_variable_any cv;   // _any: has the stop_token overloads
std::queue<int> q;

void consumer(std::stop_token st) {
    while (true) {
        std::unique_lock lk(m);
        // Predicate is checked BEFORE the first sleep (no lost wakeup) and after
        // every wakeup (no spurious wakeup). request_stop() also wakes the wait.
        if (!cv.wait(lk, st, [] { return !q.empty(); }))
            return;                            // stop requested and queue empty
        int v = q.front();
        q.pop();
        lk.unlock();                           // never process while holding the lock
        std::printf("consumed %d\n", v);
    }
}

int main() {
    std::jthread c(consumer);
    for (int i = 0; i < 3; ++i) {
        {
            std::lock_guard lk(m);             // modify shared state UNDER the lock
            q.push(i);
        }
        cv.notify_one();                       // notify after unlocking
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(20));
}   // ~jthread: request_stop() wakes the stoppable wait, then join()
```

> **See also:** [Producer-Consumer pattern](../design-patterns/Design_Patterns_Cpp.md#39-producer-consumer) for a bounded blocking queue, and [Concurrency Coding Problems](../computer-science/Concurrency_Coding_Problems.md) for interview-style exercises (print in order, H2O, dining philosophers).

## 12.4 Atomic Operations

`std::atomic<T>` provides lock-free (on most platforms) thread-safe operations:

```cpp
#include <atomic>

std::atomic<int> counter{0};

void increment() {
    counter++;                    // atomic increment
    counter.fetch_add(1);         // equivalent
    counter.store(42);            // atomic write
    int val = counter.load();     // atomic read
}

// Compare-and-swap (CAS) -- foundation of lock-free algorithms
std::atomic<int> shared{0};
int expected = 0;
bool swapped = shared.compare_exchange_strong(expected, 42);
// If shared == expected (0): sets shared = 42, returns true
// If shared != expected: sets expected = shared's value, returns false

// Atomic flag (guaranteed lock-free)
std::atomic_flag flag = ATOMIC_FLAG_INIT;
while (flag.test_and_set()) { /* spin */ }  // spinlock
flag.clear();
```

### Memory Orderings

| Ordering | Guarantee | Use Case |
|---|---|---|
| `memory_order_relaxed` | No ordering guarantees; only atomicity | Counters, statistics |
| `memory_order_acquire` | Reads after this see writes before the matching release | Load side of publish-subscribe |
| `memory_order_release` | Writes before this are visible after the matching acquire | Store side of publish-subscribe |
| `memory_order_acq_rel` | Both acquire and release | Read-modify-write operations |
| `memory_order_seq_cst` | Full sequential consistency (default) | Default; safest, slowest |

```cpp
std::atomic<bool> ready{false};
int data = 0;

// Thread 1 (publisher)
data = 42;                                           // non-atomic write
ready.store(true, std::memory_order_release);         // publish

// Thread 2 (subscriber)
while (!ready.load(std::memory_order_acquire)) {}     // subscribe
assert(data == 42);  // guaranteed to see 42 due to acquire-release pairing
```

The formal rules behind this example (happens-before, release sequences, fences, litmus tests) are in [12.9](#129-the-c-memory-model). CAS retry loops are in [12.10](#1210-compare-and-swap-loops), and lock-free structures in [12.11](#1211-lock-free-data-structures-and-memory-reclamation).

## 12.5 Async, Futures, and Promises

### `std::async` -- Simplest Way to Run Asynchronous Tasks

```cpp
#include <future>

int expensive_computation(int x) {
    std::this_thread::sleep_for(std::chrono::seconds(2));
    return x * x;
}

// Launch asynchronously (may use a thread pool or new thread)
std::future<int> f = std::async(std::launch::async, expensive_computation, 42);

// Do other work while computation runs...

int result = f.get();  // blocks until result is ready; returns 1764

// Launch policies
std::async(std::launch::async, func);     // must run on new thread
std::async(std::launch::deferred, func);  // lazy: runs when get()/wait() is called
std::async(std::launch::async | std::launch::deferred, func); // implementation decides (default)
```

### `std::promise` and `std::future` -- Manual Channel

```cpp
std::promise<int> prom;
std::future<int> fut = prom.get_future();

std::thread producer([&prom] {
    int result = compute();
    prom.set_value(result);     // fulfill the promise
});

int val = fut.get();  // blocks until value is set
producer.join();

// Exception propagation
std::promise<int> prom2;
auto fut2 = prom2.get_future();
prom2.set_exception(std::make_exception_ptr(std::runtime_error("fail")));
try {
    fut2.get();  // rethrows the exception
} catch (const std::runtime_error& e) {
    // handle error
}
```

### `std::packaged_task` -- Wraps a Callable with a Future

```cpp
std::packaged_task<int(int, int)> task([](int a, int b) { return a + b; });
std::future<int> result = task.get_future();

std::thread t(std::move(task), 3, 4);
t.join();
int sum = result.get();  // 7
```

## 12.6 Thread-Safe Singleton (Meyers' Singleton)

```cpp
class Singleton {
public:
    static Singleton& instance() {
        static Singleton s;  // C++11 guarantees thread-safe initialization
        return s;
    }

    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;

private:
    Singleton() = default;
};
```

The C++11 standard guarantees that local static variable initialization is thread-safe ("magic statics"). No mutex needed.

## 12.7 Common Concurrency Bugs

| Bug | Description | Prevention |
|---|---|---|
| **Data race** | Two threads access shared data concurrently, at least one writes | Mutex, atomic, or immutable data |
| **Deadlock** | Two threads each hold a lock and wait for the other's lock | Lock ordering, `std::scoped_lock`, `std::lock` |
| **Livelock** | Threads keep responding to each other without making progress | Randomized backoff |
| **Starvation** | A thread never gets to run due to scheduling unfairness | Fair locking, priority management |
| **Race condition** | Outcome depends on non-deterministic ordering of operations | Proper synchronization |

### Deadlock Example and Fix

```cpp
std::mutex m1, m2;

// DEADLOCK: Thread A locks m1→m2, Thread B locks m2→m1
void threadA() { std::lock_guard l1(m1); std::lock_guard l2(m2); }
void threadB() { std::lock_guard l1(m2); std::lock_guard l2(m1); }

// FIX 1: consistent lock ordering
void threadA_fixed() { std::lock_guard l1(m1); std::lock_guard l2(m2); }
void threadB_fixed() { std::lock_guard l1(m1); std::lock_guard l2(m2); }

// FIX 2: std::scoped_lock (C++17) -- deadlock-free
void threadA_best() { std::scoped_lock lock(m1, m2); }
void threadB_best() { std::scoped_lock lock(m2, m1); }  // order doesn't matter
```

For `std::lock` internals, lock hierarchies that catch ordering bugs at run time, and the four Coffman conditions, see [12.13](#1213-once-only-init-lock-ordering-and-thread-local-storage).

## 12.8 Thread Pool (Simplified Implementation)

```cpp
#include <thread>
#include <queue>
#include <mutex>
#include <condition_variable>
#include <functional>
#include <vector>
#include <future>

class ThreadPool {
    std::vector<std::thread> workers_;
    std::queue<std::function<void()>> tasks_;
    std::mutex mutex_;
    std::condition_variable cv_;
    bool stop_ = false;

public:
    ThreadPool(size_t num_threads) {
        for (size_t i = 0; i < num_threads; ++i) {
            workers_.emplace_back([this] {
                while (true) {
                    std::function<void()> task;
                    {
                        std::unique_lock lock(mutex_);
                        cv_.wait(lock, [this] { return stop_ || !tasks_.empty(); });
                        if (stop_ && tasks_.empty()) return;
                        task = std::move(tasks_.front());
                        tasks_.pop();
                    }
                    task();
                }
            });
        }
    }

    template <typename F, typename... Args>
    auto enqueue(F&& f, Args&&... args) -> std::future<std::invoke_result_t<F, Args...>> {
        using return_type = std::invoke_result_t<F, Args...>;
        auto task = std::make_shared<std::packaged_task<return_type()>>(
            std::bind(std::forward<F>(f), std::forward<Args>(args)...));
        std::future<return_type> result = task->get_future();
        {
            std::lock_guard lock(mutex_);
            tasks_.emplace([task] { (*task)(); });
        }
        cv_.notify_one();
        return result;
    }

    ~ThreadPool() {
        { std::lock_guard lock(mutex_); stop_ = true; }
        cv_.notify_all();
        for (auto& w : workers_) w.join();
    }
};

// Usage
ThreadPool pool(4);
auto future = pool.enqueue([](int x) { return x * x; }, 42);
int result = future.get();  // 1764
```

## 12.9 The C++ Memory Model

The memory model answers one question: **which values may a load return?** Compilers (hoisting, register caching, store sinking) and CPUs (store buffers, out-of-order execution, non-coherent-looking caches on weak architectures) both reorder memory operations. The C++ model defines the reorderings a program can observe, independently of the hardware.

> **See also:** [CS Fundamentals -- Memory Models and Visibility](../computer-science/CS_Fundamentals.md#69-memory-models-and-visibility) covers the hardware side: why reordering happens, the MP and SB litmus tests with a runnable SB program, and the x86-TSO vs ARM vs POWER vs GPU tables with instruction mappings. This section is the language-level view.

### The Relations You Must Be Able to Define

| Relation | Definition | Example |
|---|---|---|
| **Sequenced-before** | Intra-thread evaluation order given by the language rules ([15.8](#158-evaluation-order-c17)) | In `a = 1; b = 2;`, the write to `a` is sequenced-before the write to `b` |
| **Synchronizes-with** | An inter-thread edge created by the library or by atomics. A *release* operation on atomic `M` synchronizes-with an *acquire* operation on `M` that **reads the value written** by the release (or by a later RMW in its release sequence) | `ready.store(true, release)` then `ready.load(acquire)` returns `true` |
| **Happens-before** | (Roughly) the transitive closure of sequenced-before and synchronizes-with | `data = 42` is sequenced-before the release store, which synchronizes-with the acquire load, which is sequenced-before `assert(data == 42)` |
| **Modification order** | Every atomic object has one total order of all writes to it, and all threads agree on it, **even with `relaxed`** (per-object coherence) | Two relaxed `fetch_add(1)`s never lose an update |
| **Single total order S** | All `seq_cst` operations appear in one global order consistent with happens-before | Makes the SB litmus outcome `r1 == r2 == 0` impossible |

Synchronizes-with edges that do not involve user atomics are just as important:

| Source of the edge | Synchronizes with |
|---|---|
| `mutex.unlock()` | The next `lock()` of the same mutex that acquires it |
| `std::thread` constructor | Start of the thread function (arguments are visible) |
| Thread function completion | Return from `join()` |
| `promise.set_value()` / `packaged_task` call | `future.get()` / `wait()` returning |
| `latch.count_down()` / `barrier.arrive()` | Return from the corresponding `wait()` |
| `semaphore.release()` | An `acquire()` that observes it |
| `atomic::notify_*` | Nothing by itself. The ordering comes from the store that changed the value |

**Data race (formal):** two accesses to the same memory location, at least one a write, at least one non-atomic, in different threads, and **neither happens-before the other**. A data race is undefined behavior for the *whole program*, not just a "stale read". That is why the compiler may, for example, hoist a non-atomic `while (!flag)` load out of the loop and spin forever.

### Release Sequences

After a release store `S` to atomic `M`, the *release sequence* headed by `S` is `S` followed by the unbroken run of **read-modify-writes** on `M` (from any thread) that come after it in modification order. An acquire load that reads a value written by any of those RMWs still synchronizes-with `S`. This is why a reference count works: many threads do `fetch_sub(1, release)`, and the thread that sees the count reach zero does an acquire and sees *all* previous owners' writes. C++20 (P0982R1) removed same-thread plain stores from release sequences, so only RMWs extend one now.

### Memory Orders, Precisely

| Order | Valid on | Forbids | Typical use |
|---|---|---|---|
| `relaxed` | load, store, RMW | Nothing beyond atomicity and per-object coherence | Counters, statistics, IDs, `shared_ptr` increment |
| `consume` | load | Reordering of *data-dependent* later reads (see below) | Nothing in practice: treated as `acquire` |
| `acquire` | load, RMW | Any later read/write in this thread moving **before** it | Reading a published flag or pointer, taking a lock |
| `release` | store, RMW | Any earlier read/write in this thread moving **after** it | Publishing data, releasing a lock |
| `acq_rel` | RMW | Both | CAS that both consumes and publishes (stack push/pop, refcount drop to 0) |
| `seq_cst` | all | Acquire/release plus participation in the single total order S, which also forbids store-to-load reordering | The default. Needed for Dekker/Peterson-style "write mine, read yours" |

`release` on a load or `acquire` on a store is not allowed (UB; GCC warns with `-Winvalid-memory-model`).

### `memory_order_consume`: Status

`consume` was meant to exploit *dependency ordering* (on ARM/POWER, `p->field` after loading `p` is ordered for free, without a barrier, which is what Linux RCU's `rcu_dereference` relies on). Nobody managed to implement the standard's "carries a dependency" tracking through optimizers, so **every major compiler promotes `consume` to `acquire`**. It has been officially discouraged since C++17 (P0371R1), and C++26 deprecates it via P3475R2, which also removes `[[carries_dependency]]`. Interview answer: "Don't use it. It is `acquire` in practice."

### Litmus Tests Beyond MP and SB

Read each as "initially `x = y = 0`; can the listed outcome happen?" Here `x` and `y` are atomics, and each column says which order *every* access uses (in the acquire/release column, loads are `acquire` and stores are `release`):

| Test | Threads | Outcome in question | `relaxed` | `acquire`/`release` | `seq_cst` |
|---|---|---|---|---|---|
| **MP** (message passing) | T1: `x=1; y=1` / T2: `r1=y; r2=x` | `r1==1 && r2==0` | Allowed | **Forbidden** | Forbidden |
| **SB** (store buffering) | T1: `x=1; r1=y` / T2: `y=1; r2=x` | `r1==0 && r2==0` | Allowed | **Allowed** (seen on x86!) | **Forbidden** |
| **LB** (load buffering) | T1: `r1=x; y=1` / T2: `r2=y; x=1` | `r1==1 && r2==1` | Allowed by the model (out-of-thin-air rules aside; observed on some ARM/POWER parts) | Forbidden | Forbidden |
| **IRIW** (independent reads of independent writes) | W1: `x=1` / W2: `y=1` / R1: `r1=x; r2=y` / R2: `r3=y; r4=x` | `r1==1, r2==0, r3==1, r4==0` (readers disagree on write order) | Allowed | **Allowed** (observable on POWER, which is not multi-copy atomic) | **Forbidden** |
| **CoRR** (coherence) | T1: `x=1` / T2: `r1=x; r2=x` | `r1==1 && r2==0` | **Forbidden** (coherence holds even for relaxed) | Forbidden | Forbidden |

Takeaways: acquire/release is enough for one-directional *publication* (MP). Any pattern where each thread writes its own flag and then reads the other's (SB: Dekker, Peterson, "set my state then check yours" in work-stealing deques) needs `seq_cst` or a `seq_cst` fence. Run the SB program in the CS link above. On an x86 desktop it shows thousands of `0/0` results with release/acquire and zero with `seq_cst`.

### Fences: `std::atomic_thread_fence`

A fence is a standalone ordering point that applies to *all* surrounding atomic operations, not just one:

- **Release fence `F` before relaxed store `X`**, paired with **relaxed load `Y` (reading X's value) before acquire fence `G`**: `F` synchronizes-with `G`. Mixed forms (release fence plus acquire load, or release store plus acquire fence) also work.
- **`seq_cst` fence**: between `x.store(1, relaxed)` and `r1 = y.load(relaxed)` on both threads, it forbids the SB outcome. On x86, GCC 15 emits `lock or $0,(%rsp)` for it (cheaper than `mfence`). Acquire and release fences emit **no instruction** on x86 (compiler barrier only), and `dmb ish`/`dmb ishld` on ARMv8.
- **`std::atomic_signal_fence`**: compiler-only barrier, for ordering with a signal handler on the same thread.
- When fences pay off: one acquire fence after reading *many* relaxed flags (for example, polling N queues), or a release fence before a batch of relaxed stores.
- **Tooling caveat:** ThreadSanitizer does not model fences. GCC prints `'atomic_thread_fence' is not supported with '-fsanitize=thread'`, and TSan may report false races in fence-based code.

### `volatile` Is Not a Synchronization Primitive

`volatile` only stops the compiler from eliding or merging accesses to that object (for MMIO registers, `setjmp`, and signal handlers with `volatile sig_atomic_t`). It provides **no atomicity** (`++v` is load, add, store) and **no inter-thread ordering**, so concurrent access to a `volatile int` is still a data race (UB). The exception is MSVC's non-standard `/volatile:ms` mode on x86. Use `std::atomic`. To read device memory written by a GPU or DMA engine, use atomics (or `std::atomic_ref`) with the right scope or ordering, plus the vendor's cache-coherence rules.

### Atomic Types: Lock-Freedom, `atomic_ref`, `atomic<shared_ptr>`

```cpp
// Build: g++ -std=c++20 -O2 -pthread misc.cpp -latomic
#include <atomic>
#include <cstdio>
#include <memory>
#include <thread>
#include <vector>

struct Pair { long a, b; };      // 16 bytes
struct Big  { long v[4]; };      // 32 bytes

int main() {
    std::printf("atomic<int>  always_lock_free=%d\n", std::atomic<int>::is_always_lock_free); // 1
    std::printf("atomic<Pair> is_lock_free=%d\n", std::atomic<Pair>{}.is_lock_free());         // 0 (GCC)
    std::printf("atomic<Big>  is_lock_free=%d\n", std::atomic<Big>{}.is_lock_free());          // 0
    std::printf("atomic<shared_ptr<int>> is_lock_free=%d\n",
                std::atomic<std::shared_ptr<int>>{}.is_lock_free());                           // 0 (libstdc++)

    // atomic_ref (C++20): atomic ops on a plain object, e.g., a histogram filled in
    // parallel and later read single-threaded with zero atomic overhead.
    std::vector<int> hist(4, 0);
    {
        std::vector<std::jthread> ts;
        for (int t = 0; t < 4; ++t)
            ts.emplace_back([&] {
                for (int i = 0; i < 100000; ++i)
                    std::atomic_ref<int>(hist[i % 4]).fetch_add(1, std::memory_order_relaxed);
            });
    }   // join = happens-before edge: plain reads below are race-free
    std::printf("hist: %d %d %d %d\n", hist[0], hist[1], hist[2], hist[3]);   // 100000 x4

    // Fence-based message passing: relaxed atomics + release/acquire FENCES.
    int payload = 0;
    std::atomic<bool> flag{false};
    std::jthread producer([&] {
        payload = 42;
        std::atomic_thread_fence(std::memory_order_release);  // orders payload before...
        flag.store(true, std::memory_order_relaxed);          // ...this relaxed store
    });
    while (!flag.load(std::memory_order_relaxed)) {}
    std::atomic_thread_fence(std::memory_order_acquire);      // pairs with release fence
    std::printf("payload=%d\n", payload);                      // guaranteed 42
}
```

| Facility | Notes |
|---|---|
| `is_always_lock_free` (C++17, `constexpr`) vs `is_lock_free()` | Use the former in `static_assert` for code that must not take hidden locks (signal handlers, shared memory between processes, GPU host-device flags) |
| Non-native sizes | `std::atomic<16-byte struct>` is implemented in `libatomic` with a lock table. Link `-latomic`, otherwise you get `undefined reference to __atomic_is_lock_free`. GCC reports 16-byte atomics as not lock-free even on CPUs with `cmpxchg16b` |
| `std::atomic_ref<T>` (C++20) | The object must be aligned to `atomic_ref<T>::required_alignment`, and while any `atomic_ref` to it exists, all concurrent accesses must go through `atomic_ref` |
| `std::atomic<std::shared_ptr<T>>` (C++20) | Replaces the deprecated `std::atomic_load(&sp)` free functions. Correct and convenient (it solves reclamation for you), but **not lock-free** in libstdc++ or MSVC |
| `std::atomic<float/double>::fetch_add` (C++20) | A CAS loop on most CPUs. GPUs have native float atomics |
| `std::atomic_flag::test()` (C++20) | Read without modifying, enabling test-and-test-and-set with `atomic_flag` |

## 12.10 Compare-and-Swap Loops

```cpp
// fragment -- signature
bool compare_exchange_weak(T& expected, T desired,
                           std::memory_order success, std::memory_order failure);
// Atomically: if (*this == expected) { *this = desired; return true; }
//             else { expected = *this; return false; }   <- expected is UPDATED
```

- Comparison is **bitwise** (value representation), like `memcmp`, not `operator==`. For `float`, `+0.0` and `-0.0` differ and a NaN can compare equal to itself. Since C++20 (P0528), padding bits do not participate.
- The `failure` order applies to the load done on failure. It cannot be `release` or `acq_rel`. Since C++17 (P0418) it may be stronger than `success`.

### Weak vs Strong, and Spurious Failure

| | `compare_exchange_weak` | `compare_exchange_strong` |
|---|---|---|
| May fail even though `*this == expected` | **Yes (spurious failure)** | No |
| x86-64 | `lock cmpxchg` (identical) | `lock cmpxchg` |
| ARMv8.0 / POWER / RISC-V (LL/SC) | One `ldaxr`/`stlxr` attempt. The store-conditional fails if the reservation is lost (interrupt, context switch, cache-line eviction, another core touching the line) | Wraps the LL/SC pair in its own retry loop |
| ARMv8.1+ with LSE | Single `cas`/`casal` instruction (no spurious failure in practice) | Same |
| Use when | **Inside a retry loop**: you are looping anyway, so a spurious failure just costs one more iteration and you avoid a nested loop | **Single attempt** where failure must mean "someone else changed it" (state-machine transitions, `try_lock`), or when recomputing `desired` is expensive |

### The Canonical Retry Loop

```cpp
// Build: g++ -std=c++20 -O2 -pthread cas.cpp
#include <atomic>
#include <cassert>
#include <cstdio>
#include <thread>
#include <vector>

// There is no hardware "fetch_multiply", so build any RMW from CAS.
int fetch_multiply(std::atomic<int>& a, int factor) {
    int expected = a.load(std::memory_order_relaxed);
    // On failure, compare_exchange_weak writes the CURRENT value into `expected`,
    // so the next iteration recomputes from fresh data: no extra load needed.
    while (!a.compare_exchange_weak(expected, expected * factor,
                                    std::memory_order_acq_rel,    // success
                                    std::memory_order_relaxed)) { // failure
        // spurious failure or lost race: retry
    }
    return expected;  // previous value, like fetch_add
}

// Atomic max with early exit: no write (and no cache-line steal) if not needed.
void atomic_max(std::atomic<int>& a, int v) {
    int cur = a.load(std::memory_order_relaxed);
    while (cur < v && !a.compare_exchange_weak(cur, v, std::memory_order_relaxed)) {
    }
}

int main() {
    std::atomic<int> prod{1}, mx{0};
    {
        std::vector<std::jthread> ts;
        for (int t = 0; t < 4; ++t)
            ts.emplace_back([&, t] {
                for (int i = 0; i < 5; ++i) fetch_multiply(prod, 2);    // 20 doublings
                for (int i = 0; i < 100'000; ++i) atomic_max(mx, t * 100'000 + i);
            });
    }
    assert(prod.load() == (1 << 20));
    assert(mx.load() == 399'999);
    std::printf("prod=%d max=%d\n", prod.load(), mx.load());   // prod=1048576 max=399999
}
```

### CAS Pitfalls and a Correct Spinlock

- **Forgetting that `expected` is overwritten.** In `bool e = false; while (!lock.compare_exchange_weak(e, true)) {}`, after the first failure `e` becomes `true`, and the next CAS "succeeds" by swapping `true` for `true`, so **two threads hold the lock**. Reset `e = false` inside the loop, or use `exchange`.
- **CAS under contention is not free.** Every attempt needs the cache line in exclusive state, roughly 50-100+ ns per transfer across cores and more across sockets or chiplets (CCDs). With N threads hammering one CAS loop, most attempts fail. Prefer a single-instruction RMW (`fetch_add` = `lock xadd`, which never fails), shard the counter per thread or core, or back off.
- **Spinning with RMWs.** A spinlock that loops on `exchange(true)` keeps stealing the line. Use *test-and-test-and-set* (TTAS): spin on a plain load and only try the RMW when the lock looks free.

```cpp
// fragment -- needs <atomic>, <thread>, <immintrin.h> on x86
class SpinLock {
    std::atomic<bool> locked_{false};
public:
    void lock() noexcept {
        for (;;) {
            if (!locked_.exchange(true, std::memory_order_acquire)) return;   // try once
            while (locked_.load(std::memory_order_relaxed))                    // wait on a
                _mm_pause();    // read-only shared copy; pause = SMT-friendly, saves power
        }
    }
    bool try_lock() noexcept {
        return !locked_.load(std::memory_order_relaxed) &&
               !locked_.exchange(true, std::memory_order_acquire);
    }
    void unlock() noexcept { locked_.store(false, std::memory_order_release); }
};
```

Spinlocks are only appropriate when critical sections are a few hundred cycles, threads are not oversubscribed, and you control the scheduling (kernel code, pinned real-time threads). In user space, `std::mutex` (a futex: a CAS fast path that then sleeps in the kernel) is almost always the better default, because a preempted spinlock holder makes every waiter burn a full time slice.

## 12.11 Lock-Free Data Structures and Memory Reclamation

### Progress Guarantees

| Guarantee | Definition | Example |
|---|---|---|
| **Blocking** | A thread suspended at the wrong moment (holding a lock) can stop all others | `std::mutex`, spinlocks |
| **Obstruction-free** | A thread makes progress if it runs **in isolation** for long enough | Some STM designs |
| **Lock-free** | **Some** thread completes an operation in a finite number of system-wide steps; individual threads may starve | CAS-loop stack/queue, `fetch_multiply` above |
| **Wait-free** | **Every** thread completes in a bounded number of its own steps | `fetch_add` on x86 (`lock xadd`), SPSC ring buffer below |

"Lock-free" does **not** mean "faster". Lock-free structures avoid convoying and priority inversion and are safe in signal handlers. But they do more atomic RMWs, contend on one hot cache line (the stack head), and need complex memory reclamation. A well-implemented mutex-protected `std::vector` often wins at low contention. Benchmark before choosing.

### The Treiber Stack (with Correct Orderings)

```cpp
// Build: g++ -std=c++20 -O2 -pthread treiber.cpp
// Reclamation: popped nodes are RETIRED, never freed while the stack is live. That
// makes pop() memory-safe and ABA-free but lets memory grow. Production code
// replaces the retired list with hazard pointers or epochs (see below).
#include <atomic>
#include <cassert>
#include <cstdio>
#include <optional>
#include <thread>
#include <vector>

template <typename T>
class TreiberStack {
    struct Node {
        T value;
        Node* next;          // written once before publication, then immutable
        Node* retired_next;  // link in the retired list
    };
    std::atomic<Node*> head_{nullptr};
    std::atomic<Node*> retired_{nullptr};  // push-only stack: no pop, so no ABA

public:
    TreiberStack() = default;
    TreiberStack(const TreiberStack&) = delete;
    TreiberStack& operator=(const TreiberStack&) = delete;

    void push(T v) {
        Node* n = new Node{std::move(v), nullptr, nullptr};
        n->next = head_.load(std::memory_order_relaxed);
        // release: publishes n->value and n->next to whoever acquires head_.
        // On failure, n->next is refreshed with the current head; retry.
        while (!head_.compare_exchange_weak(n->next, n,
                                            std::memory_order_release,
                                            std::memory_order_relaxed)) {
        }
    }

    std::optional<T> pop() {
        // acquire (also on failure): we dereference `old` (old->next), so we must
        // synchronize with the push that published it.
        Node* old = head_.load(std::memory_order_acquire);
        while (old && !head_.compare_exchange_weak(old, old->next,
                                                   std::memory_order_acquire,
                                                   std::memory_order_acquire)) {
        }
        if (!old) return std::nullopt;
        std::optional<T> result{std::move(old->value)};  // only the CAS winner gets here
        retire(old);  // NOT delete: another thread may still be reading old->next
        return result;
    }

    ~TreiberStack() {  // by contract, no concurrent users remain
        for (Node* n = head_.load(); n;) { Node* nx = n->next; delete n; n = nx; }
        for (Node* n = retired_.load(); n;) { Node* nx = n->retired_next; delete n; n = nx; }
    }

private:
    void retire(Node* n) {
        n->retired_next = retired_.load(std::memory_order_relaxed);
        while (!retired_.compare_exchange_weak(n->retired_next, n,
                                               std::memory_order_relaxed)) {
        }
    }
};

int main() {
    TreiberStack<int> s;
    constexpr int kThreads = 4, kPerThread = 200'000;
    std::atomic<long long> popped_sum{0};
    std::atomic<int> popped_count{0};
    {
        std::vector<std::jthread> ts;
        for (int t = 0; t < kThreads; ++t)
            ts.emplace_back([&, t] {
                for (int i = 0; i < kPerThread; ++i) {
                    s.push(t * kPerThread + i);
                    if (auto v = s.pop()) {
                        popped_sum.fetch_add(*v, std::memory_order_relaxed);
                        popped_count.fetch_add(1, std::memory_order_relaxed);
                    }
                }
            });
    }
    while (auto v = s.pop()) { popped_sum += *v; ++popped_count; }
    const long long n = 1LL * kThreads * kPerThread;
    assert(popped_count == n);
    assert(popped_sum == n * (n - 1) / 2);   // every value popped exactly once
    std::printf("ok: %d values, sum %lld\n", popped_count.load(), popped_sum.load());
}
```

Why each order is what it is:

- `push` CAS **success = `release`**: the node's `value` and `next` must be visible to any thread that later acquires `head_` and dereferences the node. **Failure = `relaxed`**: we only reuse the observed pointer as `n->next`, without dereferencing it.
- `pop` load and CAS **= `acquire`** (including failure): we read `old->next` right after, so the push that wrote it must happen-before our read.
- Successive pushes form a chain of RMWs on `head_`, which extends release sequences, so an acquire in `pop` that reads any later head value still synchronizes with earlier pushes.
- The program is clean under `-fsanitize=thread`. Delete the `retire()` call and replace it with `delete old` to watch TSan or ASan catch the use-after-free described next.

### Why `delete old` in `pop()` Is Broken: Use-After-Free and ABA

1. **Use-after-free.** Thread B loads `old = head` and is about to read `old->next`. Thread A pops the same node and deletes it. B then reads freed memory.
2. **ABA.** The stack is `A -> B -> C`:

| Step | Thread 1 | Thread 2 | Stack |
|---|---|---|---|
| 1 | `pop`: reads `old = A`, `next = B`, then is preempted | | A -> B -> C |
| 2 | | `pop` A (frees A), `pop` B (frees B) | C |
| 3 | | `push(X)`: the allocator **reuses A's address** | A' -> C |
| 4 | CAS(head, expected A, desired B) **succeeds**: head is "A" again | | head = B (**freed** memory); X and C are unreachable (lost), and the next pop dereferences freed B |

The CAS compares *addresses*, not identities, so A -> B -> A' looks unchanged.

### Fixing ABA and Reclamation

| Technique | Idea | Cost / caveats |
|---|---|---|
| **Tagged (versioned) pointers** | Pair the pointer with a counter incremented on every change, and CAS both together: either a 16-byte CAS (`cmpxchg16b`, ARM `casp`) or the counter packed into unused high bits of a 64-bit pointer | Fixes ABA only, not use-after-free (you still need type-stable memory such as a free list that never returns memory to the OS). 16-byte atomics may not be lock-free in your toolchain (see 12.9). High-bit packing breaks with 5-level paging (57-bit VAs) and conflicts with ARM TBI/MTE pointer tags |
| **Hazard pointers** (Michael, 2004) | Before dereferencing, a thread publishes the pointer in a per-thread "hazard" slot, then re-validates that it is still reachable. Retired nodes are freed only when no hazard slot holds them | Bounded garbage (O(threads x slots)). Each protected load needs a store plus a `seq_cst` fence (or an asymmetric fence such as `membarrier`). Standardized in **C++26 `<hazard_pointer>`** (P2530); folly has a production implementation |
| **Epoch-based reclamation (EBR)** | A global epoch counter. Threads announce the epoch on entering a read-side critical section, and retired nodes are freed once every active thread has moved two epochs past them | Very cheap reads (one store per critical section, not per pointer). **One stalled thread blocks all reclamation**, so memory is unbounded. Used by crossbeam (Rust) |
| **RCU** (read-copy-update) | Readers run lock-free with near-zero overhead. Writers copy, modify, publish a new pointer, and free the old version after a *grace period* in which all pre-existing readers have finished | The Linux kernel workhorse. Best for read-mostly data. **C++26 `<rcu>`** (P2545) |
| **Reference counting** | `std::atomic<std::shared_ptr<Node>>`, or split (external/internal) counts | Simplest to get right, but every read is a write to the count (cache-line contention), and libstdc++'s implementation uses an internal lock bit |
| **Garbage collection** | Java/Go: a node cannot be reused while anyone holds a reference | ABA on node identity is impossible. This is why lock-free code is easier in GC languages |

The reference-counted stack is a few lines and correct (not lock-free in libstdc++, but a good interview answer when asked for "safe and simple"):

```cpp
// fragment -- needs <atomic>, <memory>, <optional>
template <typename T>
class SharedPtrStack {
    struct Node { T value; std::shared_ptr<Node> next; };
    std::atomic<std::shared_ptr<Node>> head_;
public:
    void push(T v) {
        auto n = std::make_shared<Node>(std::move(v), head_.load());
        while (!head_.compare_exchange_weak(n->next, n)) {}
    }
    std::optional<T> pop() {
        auto old = head_.load();
        while (old && !head_.compare_exchange_weak(old, old->next)) {}
        if (!old) return std::nullopt;
        return std::move(old->value);    // node freed when the last shared_ptr drops
    }
};
```

### SPSC Ring Buffer (Wait-Free, Acquire/Release Only)

The single-producer/single-consumer queue is the most practical lock-free structure. It appears in audio and trading pipelines, in logging and tracing back ends (a profiler's per-thread event buffer drained by a writer thread), and in GPU host-device command rings. Each index has exactly **one writer**, so no CAS is needed.

```cpp
// Build: g++ -std=c++20 -O2 -pthread spsc.cpp
#include <array>
#include <atomic>
#include <cassert>
#include <cstddef>
#include <cstdio>
#include <optional>
#include <thread>

template <typename T, std::size_t N>
class SpscQueue {
    static_assert(N >= 2 && (N & (N - 1)) == 0, "N must be a power of two");
    static constexpr std::size_t kMask = N - 1;
    static constexpr std::size_t kLine = 64;   // cache-line size on x86-64 and most ARM

    // Indices grow monotonically; slot = index & kMask; size = tail - head.
    alignas(kLine) std::atomic<std::size_t> head_{0};  // written by consumer only
    alignas(kLine) std::size_t cached_tail_{0};        // consumer-private copy of tail_
    alignas(kLine) std::atomic<std::size_t> tail_{0};  // written by producer only
    alignas(kLine) std::size_t cached_head_{0};        // producer-private copy of head_
    alignas(kLine) std::array<T, N> buf_{};

public:
    bool try_push(const T& v) {                        // producer thread only
        const std::size_t t = tail_.load(std::memory_order_relaxed);   // own index
        if (t - cached_head_ == N) {                                    // looks full
            cached_head_ = head_.load(std::memory_order_acquire);       // refresh
            if (t - cached_head_ == N) return false;                    // really full
        }
        buf_[t & kMask] = v;                              // 1. write the slot
        tail_.store(t + 1, std::memory_order_release);    // 2. publish it
        return true;
    }

    std::optional<T> try_pop() {                       // consumer thread only
        const std::size_t h = head_.load(std::memory_order_relaxed);   // own index
        if (h == cached_tail_) {                                        // looks empty
            cached_tail_ = tail_.load(std::memory_order_acquire);       // refresh
            if (h == cached_tail_) return std::nullopt;                 // really empty
        }
        T v = buf_[h & kMask];                            // 1. read the slot
        head_.store(h + 1, std::memory_order_release);    // 2. hand the slot back
        return v;
    }
};

int main() {
    static SpscQueue<long, 1024> q;   // static: keep the 8 KiB buffer off the stack
    constexpr long kItems = 10'000'000;
    std::thread producer([] {
        for (long i = 0; i < kItems; ++i)
            while (!q.try_push(i)) { /* spin; real code: backoff or atomic wait */ }
    });
    long expected = 0, sum = 0;
    while (expected < kItems) {
        if (auto v = q.try_pop()) {
            assert(*v == expected);   // FIFO order preserved
            sum += *v;
            ++expected;
        }
    }
    producer.join();
    std::printf("received %ld items in order, sum=%ld\n", expected, sum);
}
```

Design points interviewers probe:

- **Orderings.** The producer's `release` store of `tail_` publishes the slot write, and the consumer's `acquire` load of `tail_` makes it visible before reading the slot. Symmetrically, the consumer's `release` store of `head_` guarantees it has *finished reading* a slot before the producer (acquiring `head_`) overwrites it. Each thread loads its own index `relaxed`, since nobody else writes it. If `tail_.store` were `relaxed`, the consumer could see the new tail before the slot contents, which is a stale read on ARM and a data race (UB) everywhere.
- **Monotonic indices.** `tail - head` distinguishes full (`== N`) from empty (`== 0`) without wasting a slot. Unsigned wrap-around at 2^64 is well-defined, and since `N` divides 2^64, `index & kMask` stays consistent across the wrap.
- **False sharing.** `head_` and `tail_` are written by different cores. On the same 64-byte line, every write would invalidate the other core's copy. `alignas(64)` separates them. `std::hardware_destructive_interference_size` is the portable name, but GCC warns (`-Winterference-size`) that its value can change with `-mtune`, which makes it unsafe in ABI-visible layouts. Apple M-series cores use 128-byte lines, and Intel's adjacent-line prefetcher effectively pairs 64-byte lines, which is why folly and others pad to 128 bytes.
- **Cached indices.** Without them, every push reads `head_`, so its cache line ping-pongs between the cores on every operation. With them, the producer touches `head_` only when the queue *looks* full. On a desktop x86 machine, the program above moves 10 M items in about 0.16 s (roughly 60 M items/s, an end-to-end figure that is very hardware-dependent).
- **Extensions.** Batch push/pop (publish many slots with one release store), blocking with `tail_.wait()`/`notify_one()` instead of spinning, and MPMC via Dmitry Vyukov's bounded queue (a per-slot sequence number plus a CAS on the enqueue/dequeue position).

> **See also:** [CS Fundamentals -- Lock-Free and Wait-Free Data Structures](../computer-science/CS_Fundamentals.md#68-lock-free-and-wait-free-data-structures), [Concurrency Coding Problems](../computer-science/Concurrency_Coding_Problems.md) (implement-it-yourself drills), [Performance Engineering -- False Sharing and alignas(64)](../computer-science/Performance_Engineering.md#56-false-sharing-and-alignas64) (cache-line effects measured), and [CUDA memory model](../ml-gpu/Parallel_GPU_Programming.md#19-cuda-memory-model) for scoped GPU atomics.

## 12.12 C++20 Synchronization Primitives

| Primitive | Header | Reusable? | Semantics | Typical use |
|---|---|---|---|---|
| `std::latch` | `<latch>` | No (single use) | Counter decremented by `count_down(n)`. `wait()` blocks until it reaches 0. `arrive_and_wait()` = count_down + wait | "Wait until N workers finished init"; start gun; fan-in of N tasks |
| `std::barrier<F>` | `<barrier>` | **Yes** (phases) | N participants call `arrive_and_wait()`. When all arrive, the completion function `F` (must be `noexcept`) runs **once** on one of the participating threads, then everyone is released and the next phase starts. `arrive_and_drop()` leaves permanently | Iterative/bulk-synchronous algorithms (stencils, per-iteration reductions); the CPU analog of `__syncthreads()` |
| `std::counting_semaphore<Max>` | `<semaphore>` | Yes | `acquire()` decrements (blocks at 0), `release(n)` increments. **No ownership**: any thread may release | Limit concurrency (N connections, N in-flight GPU uploads); signal between threads |
| `std::binary_semaphore` | `<semaphore>` | Yes | `counting_semaphore<1>` | Lightweight one-shot signal, ping-pong |
| `atomic<T>::wait(old)` / `notify_one()` / `notify_all()` | `<atomic>` | Yes | `wait(old)` blocks **while** the value equals `old` (re-checks, so spurious wakeups are hidden). libstdc++ uses a futex on Linux for suitable sizes and a hashed waiter table otherwise | Build your own latches, events, and blocking queues without a mutex + condvar |

```cpp
// Build: g++ -std=c++20 -O2 -pthread sync20.cpp
#include <atomic>
#include <barrier>
#include <chrono>
#include <cstdio>
#include <latch>
#include <semaphore>
#include <thread>
#include <vector>

using namespace std::chrono_literals;

// 1) std::latch: "wait until all workers are initialized", plus a start gun.
void latch_demo() {
    constexpr int kWorkers = 4;
    std::latch ready(kWorkers);
    std::latch go(1);
    std::vector<std::jthread> ts;
    for (int i = 0; i < kWorkers; ++i)
        ts.emplace_back([&, i] {
            // ... per-thread init (allocate buffers, pin CPU, warm caches) ...
            ready.count_down();   // decrement, do not block
            go.wait();            // block until main fires the start gun
            std::printf("worker %d running\n", i);
        });
    ready.wait();                 // main blocks until all 4 counted down
    std::puts("all workers initialized");
    go.count_down();              // release everyone at once
}

// 2) std::barrier: reusable phases; the completion function runs once per phase
//    (on one arriving thread) before anyone is released.
void barrier_demo() {
    constexpr int kThreads = 3, kPhases = 2;
    std::vector<int> partial(kThreads);
    int phase = 0;
    auto on_completion = [&]() noexcept {
        int total = 0;
        for (int p : partial) total += p;   // safe: all writers have arrived
        std::printf("phase %d reduced total = %d\n", phase++, total);
    };
    std::barrier sync(kThreads, on_completion);
    std::vector<std::jthread> ts;
    for (int t = 0; t < kThreads; ++t)
        ts.emplace_back([&, t] {
            for (int p = 0; p < kPhases; ++p) {
                partial[t] = (t + 1) * (p + 1);  // compute this phase's slice
                sync.arrive_and_wait();          // all slices done -> reduce -> next
            }
        });
}

// 3) counting_semaphore: cap concurrency at 2.
void semaphore_demo() {
    std::counting_semaphore<2> slots(2);   // template arg = max, ctor arg = initial
    std::atomic<int> in_flight{0}, peak{0};
    std::vector<std::jthread> ts;
    for (int i = 0; i < 6; ++i)
        ts.emplace_back([&] {
            slots.acquire();
            int now = in_flight.fetch_add(1) + 1;
            int p = peak.load();
            while (now > p && !peak.compare_exchange_weak(p, now)) {}
            std::this_thread::sleep_for(10ms);
            in_flight.fetch_sub(1);
            slots.release();
        });
    ts.clear();                            // join all
    std::printf("peak concurrency = %d (limit 2)\n", peak.load());
}

// 4) binary_semaphore ping-pong: strict alternation.
void ping_pong() {
    std::binary_semaphore ping(1), pong(0);
    std::jthread a([&] { for (int i = 0; i < 3; ++i) { ping.acquire(); std::puts("ping"); pong.release(); } });
    std::jthread b([&] { for (int i = 0; i < 3; ++i) { pong.acquire(); std::puts("pong"); ping.release(); } });
}

// 5) atomic wait/notify: futex-style blocking on a value.
void atomic_wait_demo() {
    std::atomic<int> state{0};
    std::jthread waiter([&] {
        state.wait(0);   // blocks while state == 0
        std::printf("waiter saw state = %d\n", state.load());
    });
    std::this_thread::sleep_for(5ms);
    state.store(1, std::memory_order_release);
    state.notify_one();
}

int main() {
    latch_demo();       // all workers initialized, then 4 x "worker i running"
    barrier_demo();     // phase 0 reduced total = 6, phase 1 reduced total = 12
    semaphore_demo();   // peak concurrency = 2 (limit 2)
    ping_pong();        // ping pong ping pong ping pong
    atomic_wait_demo(); // waiter saw state = 1
}
```

Things to say in an interview:

- **Latch vs barrier**: a latch is one-shot, and threads that count down need not wait (producers count down, a consumer waits). A barrier is cyclic, every participant both arrives and waits, and it has a completion step. Wrong choice smell: re-creating a latch every loop iteration.
- **Semaphore vs mutex**: a mutex has an *owner* (only the locker may unlock, and some implementations check). A semaphore is a counter that any thread may release. That makes it right for signaling and resource counting, and wrong for mutual exclusion that needs ownership-based debugging or priority inheritance.
- **Atomic wait pitfall**: `wait(old)` compares *values*, so an A -> B -> A change that happens while the waiter is asleep can be missed and the waiter keeps sleeping. Use a monotonically increasing counter (a generation number) when every event matters.
- `barrier`'s completion function runs while every other participant is blocked, which makes it the ideal place for a serial step (reduction, swapping double buffers, a convergence check) without an extra synchronization round.

> **See also:** [CUDA thread synchronization and cooperation](../ml-gpu/Parallel_GPU_Programming.md#21-thread-synchronization-and-cooperation) (`__syncthreads`, cooperative groups: the GPU analog of `std::barrier`) and [OpenMP synchronization](../ml-gpu/Parallel_GPU_Programming.md#12-synchronization).

## 12.13 Once-Only Init, Lock Ordering, and Thread-Local Storage

### One-Time Initialization: Three Correct Ways

| Mechanism | Use when | Notes |
|---|---|---|
| Function-local `static` ("magic statics", [12.6](#126-thread-safe-singleton-meyers-singleton)) | Lazily initializing a global or singleton | Simplest and fastest. The compiler emits a guard variable with an acquire-load fast path |
| `std::call_once(flag, f)` with a `std::once_flag` | Once per *object* (the flag is a member) or when init is not a single variable | If `f` throws, the flag is **not** set and the next caller retries. All callers synchronize-with the completed call. The `once_flag` member makes the class non-copyable and non-movable |
| Double-checked locking with an atomic | Hand-rolled lazy publication (rarely needed now) | Must use acquire/release, as below. The pre-C++11 version with a plain pointer is broken: another thread can see the pointer before the constructor's writes |

```cpp
// fragment -- correct double-checked locking (C++11 and later)
std::atomic<Widget*> g_widget{nullptr};
std::mutex g_widget_mutex;

Widget& get_widget() {
    Widget* p = g_widget.load(std::memory_order_acquire);    // fast path: no lock
    if (!p) {
        std::lock_guard lk(g_widget_mutex);
        p = g_widget.load(std::memory_order_relaxed);         // re-check under the lock
        if (!p) {
            p = new Widget;                                   // construct fully...
            g_widget.store(p, std::memory_order_release);     // ...then publish
        }
    }
    return *p;
}
```

### Deadlock Avoidance

A deadlock requires all four **Coffman conditions**: mutual exclusion, hold-and-wait, no preemption, and circular wait. Break any one of them:

| Strategy | Breaks | How |
|---|---|---|
| Global lock order | Circular wait | Rank every mutex (by documented level, or by address with `std::less<>` for same-type objects) and always lock in ascending order |
| `std::scoped_lock(m1, m2, ...)` / `std::lock(l1, l2, ...)` | Hold-and-wait | All-or-nothing acquisition. libstdc++ locks one mutex, `try_lock`s the rest, and on failure releases everything and retries starting from the one that failed. Correct for any argument order, so `transfer(a, b)` and `transfer(b, a)` cannot deadlock |
| `try_lock_for(timeout)` with back-off | No preemption | Give up and release what you hold. Add randomized back-off to avoid livelock |
| Never call unknown code while holding a lock | Hold-and-wait | Callbacks, virtual calls, and signal emission under a lock are the most common real-world deadlock source |
| Lock hierarchy (checked at run time) | Circular wait | See `HierarchicalMutex` below: violations throw immediately instead of deadlocking one time in a million |

Tooling: ThreadSanitizer reports **lock-order inversions** ("potential deadlock") even when the deadlock did not happen in that run, and Abseil's `absl::Mutex` has built-in deadlock detection. Self-transfer bug: `std::scoped_lock lk(a.m, a.m)` locks the same mutex twice, which is UB, so check `&from == &to` first.

### thread_local Storage

`thread_local` gives each thread its own instance with *thread storage duration*:

- **Initialization**: a block-scope `thread_local` is initialized the first time each thread passes its declaration. A namespace-scope `thread_local` with dynamic initialization is initialized before its first use in each thread, which the compiler implements with a per-access wrapper call (a TLS init function). Prefer constant-initialized TLS (`constinit thread_local int x = 0;`) on hot paths.
- **Destruction**: at thread exit, in reverse order of construction.
- **Use cases**: per-thread scratch buffers and allocators; per-thread RNGs (`std::mt19937` is not thread-safe); sharded statistics counters summed on demand; the current lock level (below); profiler and tracer per-thread event buffers that avoid a global lock on every event and are flushed by a collector thread; `errno`.
- **Pitfalls**: (1) Thread pools reuse threads, so TLS state leaks from one task to the next. (2) Coroutines resumed on another thread see a different instance. (3) Memory scales with the thread count (64 threads x 1 MiB scratch = 64 MiB). (4) TLS defined in a shared library (built with `-fPIC`) defaults to the general/local-dynamic model, which calls `__tls_get_addr` per access (glibc has a fast path when the module's TLS sits in the static TLS block, but it is still a call), and that is slower than the executable's local-exec TLS. This applies to every `-fPIC` library, including ones loaded at startup via `DT_NEEDED`, not only `dlopen`ed ones. Use `-ftls-model=initial-exec` or `__attribute__((tls_model("initial-exec")))` for hot TLS in libraries that are not `dlopen`ed late. (5) A pointer to another thread's TLS dangles when that thread exits.

```cpp
// Build: g++ -std=c++20 -O2 -pthread locks.cpp
#include <climits>
#include <cstdio>
#include <mutex>
#include <stdexcept>
#include <thread>
#include <vector>

// ---- std::call_once: exactly-once init, even under contention.
struct Config { int gpu_count = 0; };
std::once_flag config_once;
Config* g_config = nullptr;

const Config& config() {
    std::call_once(config_once, [] { g_config = new Config{8}; });
    return *g_config;               // happens-after the init: safe without atomics
}

// ---- scoped_lock / std::lock: deadlock-free multi-lock in any argument order.
struct Account {
    std::mutex m;
    long balance = 0;
};

void transfer(Account& from, Account& to, long amount) {
    if (&from == &to) return;             // locking one mutex twice = UB
    std::scoped_lock lk(from.m, to.m);    // C++17
    from.balance -= amount;
    to.balance += amount;
}

void transfer_cpp11(Account& from, Account& to, long amount) {
    if (&from == &to) return;
    std::unique_lock a(from.m, std::defer_lock);
    std::unique_lock b(to.m, std::defer_lock);
    std::lock(a, b);                       // all-or-nothing with back-off
    from.balance -= amount;
    to.balance += amount;
}

// ---- Lock hierarchy: a thread may only lock a mutex whose level is strictly LOWER
// than the lowest level it already holds, so a cycle cannot form.
class HierarchicalMutex {
    std::mutex m_;
    const unsigned level_;
    unsigned prev_level_ = 0;
    static thread_local unsigned this_thread_level_;   // lowest level held

    void check() const {
        if (this_thread_level_ <= level_) throw std::logic_error("lock hierarchy violated");
    }
public:
    explicit HierarchicalMutex(unsigned level) : level_(level) {}
    void lock() {
        check();
        m_.lock();
        prev_level_ = this_thread_level_;
        this_thread_level_ = level_;
    }
    void unlock() {                        // assumes LIFO unlock (true with RAII)
        this_thread_level_ = prev_level_;
        m_.unlock();
    }
    bool try_lock() {
        check();
        if (!m_.try_lock()) return false;
        prev_level_ = this_thread_level_;
        this_thread_level_ = level_;
        return true;
    }
};
thread_local unsigned HierarchicalMutex::this_thread_level_ = UINT_MAX;

HierarchicalMutex device_mutex(1000);   // acquire first
HierarchicalMutex queue_mutex(500);     // then this

// ---- thread_local: one instance per thread.
thread_local int tls_counter = 0;

int main() {
    {
        std::vector<std::jthread> ts;
        for (int i = 0; i < 4; ++i) ts.emplace_back([] { (void)config(); });
    }
    std::printf("gpu_count=%d\n", config().gpu_count);                 // 8

    Account a, b;
    a.balance = b.balance = 1000;
    {
        std::jthread t1([&] { for (int i = 0; i < 100000; ++i) transfer(a, b, 1); });
        std::jthread t2([&] { for (int i = 0; i < 100000; ++i) transfer_cpp11(b, a, 1); });
    }
    std::printf("a=%ld b=%ld\n", a.balance, b.balance);               // a=1000 b=1000

    {
        std::scoped_lock ok1(device_mutex);    // level 1000
        std::scoped_lock ok2(queue_mutex);     // 500 < 1000: allowed
    }
    try {
        std::scoped_lock l1(queue_mutex);      // 500
        std::scoped_lock l2(device_mutex);     // 1000 >= 500: violation
    } catch (const std::logic_error& e) {
        std::printf("caught: %s\n", e.what());  // caught: lock hierarchy violated
    }

    std::jthread w1([] { for (int i = 0; i < 5; ++i) ++tls_counter; std::printf("w1 tls=%d\n", tls_counter); });
    std::jthread w2([] { for (int i = 0; i < 7; ++i) ++tls_counter; std::printf("w2 tls=%d\n", tls_counter); });
}   // prints w1 tls=5 and w2 tls=7 (in either order): separate instances
```

> **See also:** [Thread Pool pattern](../design-patterns/Design_Patterns_Cpp.md#40-thread-pool), [TSan example](./CPP_Testing.md#335-tsan-example) for catching races and lock-order inversions in tests, and [Debugging and Profiling Tools](../tools/Debugging_and_Profiling_Tools.md) for diagnosing hangs (`thread apply all bt` in gdb).

---

## Common Interview Questions -- Concurrency

**Q: What is the difference between a mutex and an atomic?**

A mutex provides exclusive access to a critical section of code -- any number of operations between lock and unlock are protected. An `std::atomic` provides atomic (indivisible) access to a single variable without locking. Atomics are faster (often lock-free hardware instructions) but only protect individual operations on a single variable. Use a mutex when multiple variables must be updated consistently; use atomics for simple counters, flags, and lock-free data structures.

**Q: What is a deadlock and how do you prevent it?**

A deadlock occurs when two or more threads are each waiting for a lock held by another, forming a circular dependency. Prevention strategies: (1) always acquire locks in the same order, (2) use `std::scoped_lock` which acquires multiple locks atomically using a deadlock-avoidance algorithm, (3) use `try_lock` with timeout and retry, (4) minimize the scope and duration of locks.

**Q: What is `std::async` and how does it differ from `std::thread`?**

`std::async` is a higher-level abstraction that returns a `std::future` for getting the result. It can run the task on a new thread (`launch::async`) or defer it (`launch::deferred`). `std::thread` gives lower-level control but requires manual result passing (via shared state, promises, etc.) and explicit `join()` or `detach()`. `std::async` also propagates exceptions through the future.

**Q: What are memory orderings and why do they matter?**

Memory orderings control how atomic operations are seen by other threads. The default `seq_cst` (sequentially consistent) provides the strongest guarantee: all threads observe operations in the same order. Weaker orderings (`acquire`, `release`, `acq_rel`, and the weakest, `relaxed`) provide weaker but faster guarantees. They matter because modern CPUs and compilers reorder instructions for performance; memory orderings define which reorderings are visible across threads.

### Advanced Questions -- Memory Model, Lock-Free, and Synchronization

**Q1.** Define happens-before and explain how it determines whether a program has a data race.

Within a thread, *sequenced-before* orders evaluations. Across threads, *synchronizes-with* edges come from a release operation whose value is read by an acquire, or from library operations like unlock-to-lock, thread creation, `join`, and `future.get`. Happens-before is (roughly) the transitive closure of the two. Two conflicting accesses (same location, at least one write, at least one non-atomic) that are **not** ordered by happens-before form a data race, which is UB for the whole program. So "is this racy?" means "can I draw a chain of sequenced-before and synchronizes-with edges from the write to the read?". In the flag-publication example the chain is `data = 42` -> (sb) `store(release)` -> (sw) `load(acquire)` returning true -> (sb) read of `data`.

**Q2.** `compare_exchange_weak` vs `compare_exchange_strong`: what is a spurious failure and which one do you put in a loop?

On LL/SC architectures (ARMv8.0, POWER, RISC-V), CAS is a load-linked/store-conditional pair. The store-conditional fails if the reservation is lost, for example due to an interrupt, a context switch, or eviction of the cache line, even though the value still matched. `weak` exposes that as a spurious `false`. `strong` hides it by looping internally. On x86 both are `lock cmpxchg`. In a retry loop, use `weak`: you loop anyway, so you avoid a loop inside a loop. Use `strong` for a single attempt where `false` must mean "the value really differed", such as a state-machine transition or `try_lock`. Both write the observed value into `expected` on failure, so do not reload it yourself. A classic bug is a spinlock that never resets `expected = false`.

**Q3.** Explain the ABA problem with a concrete interleaving and give three fixes.

Thread 1 reads `head = A` and `A->next = B`, then stalls. Thread 2 pops A, pops B, frees both, and pushes a new node that the allocator places at A's old address. Thread 1's CAS(head, A, B) succeeds because the address matches, and installs freed node B as head. Fixes: (1) tagged pointers, where a version counter is CASed together with the pointer (16-byte CAS or high-bit packing). (2) Safe memory reclamation, so A's memory cannot be reused while anyone may still compare against it: hazard pointers (bounded memory, C++26 `<hazard_pointer>`), epoch-based reclamation (cheap reads but unbounded memory if a thread stalls), or RCU. (3) Reference counting with `std::atomic<std::shared_ptr>` (simple, not lock-free in practice). Tagged pointers alone do not prevent use-after-free when reading `A->next`.

**Q4.** Why can the store-buffering test (`x=1; r1=y` / `y=1; r2=x`) end with `r1 == r2 == 0` on x86, and how do you prevent it in C++?

x86-TSO lets a load complete before an earlier store to a *different* address becomes globally visible, because the store waits in the core's store buffer. Release/acquire does not forbid that ordering (release orders *earlier* accesses before the store, acquire orders *later* accesses after the load, and neither constrains store-then-load). Make all four accesses `seq_cst` (x86: the stores become `xchg`), or put `atomic_thread_fence(seq_cst)` between the store and the load in each thread. This pattern underlies Dekker's and Peterson's algorithms and "set my flag, then check yours" handshakes.

**Q5.** What does `memory_order_consume` do today?

In theory it orders only the operations that *data-depend* on the loaded value, which is free on ARM and POWER. In practice compilers could not track dependencies through optimizations, so GCC, Clang, and MSVC all treat it as `acquire`. It has been discouraged since C++17 (P0371R1), and C++26 deprecates it (P3475R2). Linux RCU gets dependency ordering through `READ_ONCE`/`rcu_dereference` conventions instead of the C++ model.

**Q6.** Lock-free vs wait-free: is a CAS loop wait-free? Is `std::atomic<T>` always lock-free?

Lock-free means some thread always makes progress. Wait-free means every thread finishes in a bounded number of its own steps. A CAS retry loop is lock-free but not wait-free, because one thread can lose every race indefinitely. `fetch_add` on x86 (`lock xadd`) and the SPSC ring buffer are wait-free. `std::atomic<T>` is not always lock-free: large or odd-sized `T` (for example, a 16-byte struct on GCC) falls back to a lock table in `libatomic`, and `std::atomic<std::shared_ptr<T>>` is not lock-free in libstdc++ or MSVC. Check with `static_assert(std::atomic<T>::is_always_lock_free)` when it matters (signal handlers, inter-process shared memory).

**Q7.** Design an SPSC queue. Which memory orders do you need, and what breaks if the producer's index store is `relaxed`?

Use a power-of-two ring with monotonically increasing `head_` (written only by the consumer) and `tail_` (written only by the producer). The producer writes the slot and then stores `tail_` with `release`. The consumer loads `tail_` with `acquire` and then reads the slot. Symmetrically, the consumer's `release` store of `head_` pairs with the producer's `acquire` load of `head_`, so the producer cannot overwrite a slot that is still being read. No CAS is needed because each index has a single writer. Put the indices on separate cache lines and cache the other side's index to reduce coherence traffic. If `tail_.store` is `relaxed`, there is no synchronizes-with edge: the consumer may see the new index but stale slot contents (observable on ARM), and the slot access is a data race, which is UB even on x86.

**Q8.** When would you use `atomic_thread_fence` instead of ordering individual operations?

Use one when a single fence can order many relaxed operations. For example, a consumer polls N relaxed flags and then issues one acquire fence before reading all the payloads, or a producer issues one release fence before publishing a batch with relaxed stores. A `seq_cst` fence is also the standard way to fix SB-style patterns while keeping relaxed accesses. Downsides: fences are harder to reason about, they order *all* surrounding accesses (so they can cost more than one targeted acquire), and TSan does not model them.

**Q9.** What is a lost wakeup? Should you call `notify_one` while holding the mutex?

A lost wakeup happens when the notify occurs after the waiter checked the condition but before it blocked. A condition variable has no memory, so the waiter sleeps forever. It occurs when the shared state is modified without holding the mutex, or when the waiter checks the state without the lock or without a predicate. Fix: modify the state under the mutex and always wait with a predicate (which also handles spurious wakeups). Notifying inside or outside the lock are both correct once the state change happened under the lock. Notifying after unlocking avoids waking a thread that immediately blocks on the mutex. Notify under the lock when the waiter might destroy the condition variable as soon as it wakes.

**Q10.** Implement `std::latch` with a mutex and a condition variable.

```cpp
// fragment -- needs <mutex>, <condition_variable>, <cstddef>
class Latch {
    std::mutex m_;
    std::condition_variable cv_;
    std::ptrdiff_t count_;
public:
    explicit Latch(std::ptrdiff_t n) : count_(n) {}
    void count_down(std::ptrdiff_t n = 1) {
        std::lock_guard lk(m_);
        if ((count_ -= n) == 0) cv_.notify_all();   // notify under the lock: a waiter
    }                                               // may destroy *this once released
    void wait() {
        std::unique_lock lk(m_);
        cv_.wait(lk, [&] { return count_ == 0; });
    }
    void arrive_and_wait(std::ptrdiff_t n = 1) {
        std::unique_lock lk(m_);
        if ((count_ -= n) == 0) { cv_.notify_all(); return; }
        cv_.wait(lk, [&] { return count_ == 0; });
    }
};
```

Follow-ups: `notify_all` (not `notify_one`) because every waiter must proceed. A barrier additionally needs a *generation* counter, so that threads from phase k+1 do not slip through phase k's release.

**Q11.** `std::call_once` vs function-local `static` vs double-checked locking?

A function-local `static` is the simplest and fastest choice for one global object, because the compiler emits a guard with an acquire fast path. `call_once` is for per-object or multi-step one-time init: if the callable throws, the flag stays unset and the next caller retries. Double-checked locking is correct only with an atomic pointer, an `acquire` load on the fast path, a re-check under the lock, and a `release` store *after* construction. The pre-C++11 plain-pointer version is broken because the pointer store can become visible before the object's fields.

**Q12.** You must lock two mutexes whose order is chosen by the caller (`transfer(a, b)` and `transfer(b, a)`). How do you avoid deadlock?

Use `std::scoped_lock lk(a.m, b.m);` (or `std::lock` on two deferred `unique_lock`s), which acquires all or nothing and backs off. Alternatively, impose a global order by address (`std::less<std::mutex*>{}(&a.m, &b.m)`) or by account ID. Guard against `a == b`, since locking the same mutex twice is UB. In a large codebase, add a lock hierarchy or rely on TSan's lock-order-inversion reports to catch violations in testing.

**Q13.** Is `std::shared_mutex` always better for read-heavy workloads?

No. Every `lock_shared()` is still an atomic RMW on one shared cache line, so with short critical sections and many cores, readers serialize on cache-coherence traffic and a plain mutex is often just as fast. Fairness is unspecified (glibc prefers readers by default, so writers can starve), and there is no upgrade path. For read-mostly data, consider copy-on-write with `atomic<shared_ptr<const T>>`, RCU, seqlocks, or sharding.

**Q14.** What goes wrong with `thread_local` in thread pools and coroutines?

Pool threads are reused, so TLS left over from task A is visible to task B (stale caches, wrong "current request" IDs). A coroutine suspended on one thread and resumed on another sees a different TLS instance. Other problems: per-thread memory multiplies by the thread count, dynamic TLS initialization adds a wrapper call on every access, and TLS defined in any `-fPIC` shared library (not only `dlopen`ed ones) defaults to the general/local-dynamic model, which calls `__tls_get_addr` per access and is slower than the executable's local-exec TLS. For hot TLS in a library that is not `dlopen`ed late, use `-ftls-model=initial-exec` or `__attribute__((tls_model("initial-exec")))`. Pass context explicitly, or reset TLS at task boundaries.

**Q15.** Can you use `volatile` for inter-thread communication in C++?

No. `volatile` only prevents the compiler from optimizing away or merging accesses to that object. It gives no atomicity (`++v` can lose updates) and no ordering relative to other memory, so concurrent `volatile` accesses are a data race (UB). It exists for memory-mapped I/O, `setjmp`/`longjmp`, and `sig_atomic_t` in signal handlers. Java's `volatile` *is* a synchronization primitive, which is the source of the confusion. The C++ equivalent is `std::atomic` with `seq_cst`.

**Q16.** In the Treiber stack, why does `pop()` need `acquire`, and why can't it simply `delete` the popped node?

`pop` dereferences the head node (`old->next`), so it must synchronize with the `release` CAS in `push` that published the node's fields. Otherwise it could read an uninitialized `next`. It cannot `delete` the node immediately because other threads may have loaded the same `old` pointer and be about to read `old->next` (use-after-free). And if the memory is reused, their CAS can succeed incorrectly (ABA). You need a reclamation scheme: hazard pointers, epochs, RCU, reference counting, or (as in the example) deferring frees until the structure is destroyed.

---

# Part 6: Compilation and Runtime

---

# 13. Compilation, Linking, and the Preprocessor

---

## 13.1 The C++ Compilation Pipeline

```
Source files (.cpp)
       │
       ▼
┌──────────────┐
│ Preprocessor │   #include expansion, macro substitution, conditional compilation
└──────┬───────┘
       │  preprocessed source (.ii)
       ▼
┌──────────────┐
│   Compiler   │   Syntax/semantic analysis, optimization, code generation
└──────┬───────┘
       │  assembly (.s)
       ▼
┌──────────────┐
│  Assembler   │   Translates assembly to machine code
└──────┬───────┘
       │  object files (.o / .obj)
       ▼
┌──────────────┐
│    Linker    │   Resolves symbols, combines object files and libraries
└──────┬───────┘
       │
       ▼
  Executable or Library
```

| Stage | Input | Output | Tool (GCC) |
|---|---|---|---|
| Preprocessing | `.cpp` + headers | `.ii` (preprocessed) | `g++ -E` |
| Compilation | `.ii` | `.s` (assembly) | `g++ -S` |
| Assembly | `.s` | `.o` (object file) | `g++ -c` or `as` |
| Linking | `.o` + libraries | executable / `.so` / `.a` | `g++` or `ld` |

## 13.2 Translation Units and the One Definition Rule (ODR)

A **translation unit** (TU) is a single `.cpp` file after all `#include` directives are expanded. It is the basic unit of compilation.

**One Definition Rule (ODR):**
1. Within a single TU: each entity can have at most one definition
2. Across the entire program: non-inline functions and non-inline variables must have exactly one definition
3. Exception: `inline` functions/variables, class definitions, templates, and `constexpr` functions may be defined in multiple TUs, but all definitions must be **identical**

```cpp
// header.h
inline int helper() { return 42; }  // OK: inline, can appear in multiple TUs
extern int global_var;               // declaration only (definition in one .cpp)

// util.cpp
int global_var = 10;  // definition -- exactly one TU

// main.cpp
#include "header.h"
// int global_var = 20;  // ERROR: ODR violation (already defined in util.cpp)
```

## 13.3 Header Files and Include Guards

Headers declare interfaces shared between translation units. Include guards prevent multiple inclusion:

```cpp
// widget.h -- include guard (traditional)
#ifndef WIDGET_H
#define WIDGET_H

class Widget {
public:
    void doWork();
};

#endif // WIDGET_H

// widget.h -- pragma once (non-standard but universally supported)
#pragma once

class Widget {
public:
    void doWork();
};
```

| Approach | Standard? | Pros | Cons |
|---|---|---|---|
| `#ifndef` / `#define` / `#endif` | Yes | Portable, standard-conforming | Verbose, name collision risk |
| `#pragma once` | No (but de facto standard) | Concise, no name collisions | Not technically standard |

### Header vs Source File Contents

| Put in Header (`.h` / `.hpp`) | Put in Source (`.cpp`) |
|---|---|
| Class declarations | Function definitions (non-inline, non-template) |
| Function declarations | Static/global variable definitions |
| Inline function definitions | Private implementation details |
| Template definitions | |
| `constexpr` / `consteval` functions | |
| Type aliases, enums | |

## 13.4 Static vs Dynamic Linking

| Aspect | Static Linking (`.a` / `.lib`) | Dynamic Linking (`.so` / `.dll`) |
|---|---|---|
| When resolved | At compile/link time | At load time or runtime |
| Executable size | Larger (library code copied in) | Smaller (references external file) |
| Memory usage | Each process has its own copy | Shared across processes |
| Deployment | Single file, self-contained | Must distribute library files |
| Update library | Must recompile | Replace `.so`/`.dll` file |
| Load time | Faster (no runtime resolution) | Slower (symbol resolution at load) |
| Cross-library calls | Direct `call`, inlinable with LTO | Indirect through the PLT/GOT ([13.8](#138-position-independent-code-the-pltgot-and-lazy-binding)), not inlinable |
| Symbol interposition (`LD_PRELOAD`) | Impossible | Possible ([13.10](#1310-symbol-interposition-and-ld_preload)) |
| Unused code | Only the archive *members* that resolve an undefined symbol are pulled in | The whole `.so` is mapped (pages load lazily) |
| Global state | Duplicated if two `.so`s each link the same `.a` (two singletons!) | One copy per process |

```bash
# Static library
g++ -c util.cpp -o util.o
ar rcs libutil.a util.o
g++ main.cpp -L. -lutil -o program    # links statically

# Dynamic library (shared object)
g++ -fPIC -shared util.cpp -o libutil.so
g++ main.cpp -L. -lutil -o program    # links dynamically
# At run time the loader must find libutil.so: embed a search path at link time with
# -Wl,-rpath,'$ORIGIN' (see 13.12), install it to a system path + ldconfig, or set LD_LIBRARY_PATH.
```

**How the static linker uses archives.** A `.a` is just a bundle of `.o` files with an index. GNU `ld` processes the command line **left to right**, keeping a set of currently undefined symbols. When it reaches an archive, it extracts only the members that define a symbol in that set, then moves on and never looks back. Consequences:

- `g++ -lutil main.o` fails with "undefined reference": when `libutil.a` was scanned, nothing was undefined yet. Libraries go **after** the objects that use them, and dependents before their dependencies (`-lhigh -llow`).
- Circular dependencies between archives need `-Wl,--start-group -la -lb -Wl,--end-group` (rescans until stable) or listing a library twice.
- An object that is referenced by nobody, such as a self-registering plugin, test, or factory whose only effect is a static constructor, is **never pulled in**, so its registration silently disappears. Fix: `-Wl,--whole-archive -lplugins -Wl,--no-whole-archive`, or in CMake `$<LINK_LIBRARY:WHOLE_ARCHIVE,plugins>` or an OBJECT library. See [CMake: static library link order](../tools/CMake_Fundamentals.md#68-static-library-link-order-and-circular-dependencies) and [self-registering factories](../design-patterns/Design_Patterns_Cpp.md#481-factory-registry-with-static-self-registration).
- Shared libraries do not have this problem, because a `.so` is linked as a whole. `--as-needed` (default on Ubuntu) does drop a `DT_NEEDED` entry for a `.so` that resolves no symbol, though.

## 13.5 Name Mangling and `extern "C"`

C++ mangles function names to encode type information for overloading. C does not. To call C++ from C (or vice versa), use `extern "C"`:

```cpp
// In a C++ header meant to be used from C
#ifdef __cplusplus
extern "C" {
#endif

void c_compatible_function(int x);

#ifdef __cplusplus
}
#endif
```

```
// Name mangling example (GCC):
// void foo(int)         → _Z3fooi
// void foo(double)      → _Z3food
// void foo(int, double) → _Z3fooid
// extern "C" void foo() → foo  (no mangling)
```

Demangle with `c++filt` or `nm -C`. Mangling (Itanium C++ ABI on Linux) encodes namespaces, parameter types, cv-qualifiers, template arguments, and **ABI tags** such as `[abi:cxx11]`, but *not* the return type of non-template functions. So `int f(int)` and `long f(int)` collide at link time, while a changed `std::string` layout produces a different name ([13.13](#1313-abi-stability-and-the-libstdc-dual-abi)).

## 13.6 Object Files and ELF Sections

On Linux, every `.o`, `.so`, executable, and core dump is an **ELF** file. The header's `e_type` says which: `ET_REL` (relocatable `.o`), `ET_DYN` (shared object *or* position-independent executable), `ET_EXEC` (non-PIE executable), or `ET_CORE`. ELF has two views of the same bytes:

- **Sections** (`readelf -S`) are the *linker's* view: named pieces such as `.text` and `.data`, with flags (A = alloc, W = write, X = exec).
- **Segments** (`readelf -l`, program headers) are the *loader's* view: `PT_LOAD` ranges to `mmap` with R/W/X permissions, plus `PT_INTERP` (the dynamic loader's path), `PT_DYNAMIC`, `PT_GNU_RELRO`, and `PT_TLS`. The linker packs many sections into a few segments.

| Section | Contents | Flags / notes |
|---|---|---|
| `.text` | Machine code | AX (read + execute) |
| `.rodata` | String literals, `const` tables, jump tables | A (read-only) |
| `.data` | Initialized, writable globals and statics | WA |
| `.bss` | Zero-initialized globals and statics | WA, type `NOBITS`: **takes no space in the file**, the loader maps zero pages |
| `.data.rel.ro` | Data that needs relocation, then becomes read-only (vtables in PIC code, `const` pointer tables) | Made read-only by RELRO after relocation |
| `.tdata` / `.tbss` | `thread_local` initial images | Copied per thread |
| `.init_array` / `.fini_array` | Pointers to static constructors and destructors (and `__attribute__((constructor))`) | Run by the loader or libc ([13.9](#139-runtime-loading-dlopen-and-dlsym)) |
| `.eh_frame`, `.gcc_except_table` | Stack-unwinding tables for exceptions and backtraces | Present even with `-fno-exceptions` unless disabled |
| `.symtab` / `.strtab` | Full symbol table (all functions, including `static` ones) | Removed by `strip`; not needed at run time |
| `.dynsym` / `.dynstr` | **Dynamic** symbols: exported and imported | Needed at run time; `nm -D` |
| `.rela.dyn` / `.rela.plt` | Relocations the dynamic loader must apply | |
| `.plt`, `.plt.sec`, `.got`, `.got.plt` | Procedure linkage table stubs and the global offset table | [13.8](#138-position-independent-code-the-pltgot-and-lazy-binding) |
| `.dynamic` | `DT_NEEDED`, `DT_SONAME`, `DT_RUNPATH`, `DT_FLAGS` ... | `readelf -d` |
| `.debug_*` | DWARF debug info | Often bigger than the code; split with `objcopy --only-keep-debug` |
| `.note.gnu.build-id` | Unique build hash | Matches binaries to debug info and symbol servers |

Which section does each C++ entity land in?

```cpp
// sections.cpp -- g++ -std=c++20 -O0 -c sections.cpp && nm -C sections.o && readelf -SW sections.o
#include <cstdio>

int counter = 42;                    // .data   (initialized, writable)
int zeroed;                          // .bss    (zero-initialized: no bytes in the file)
static int file_local = 7;           // .data, LOCAL binding (lowercase 'd' in nm)
const char banner[] = "rocprof";     // .rodata (const at namespace scope => internal linkage)
extern const int exported_limit = 64;// .rodata, GLOBAL (extern overrides const's internal linkage)
static int big_table[1 << 20];       // .bss: 4 MiB in memory, 0 bytes in the file

int add(int a, int b) { return a + b; }          // .text, GLOBAL ('T')
static int helper(int x) { return x * 2; }       // .text, LOCAL ('t') -- if not inlined away
inline int twice(int x) { return 2 * x; }        // emitted in a COMDAT group, WEAK ('W')

int main() {
    big_table[5] = helper(file_local) + twice(counter) + zeroed;
    std::printf("%s %d %d\n", banner, add(counter, big_table[5]), exported_limit);
}
```

```text
$ nm -C sections.o
0000000000000000 D counter
0000000000000008 R exported_limit
000000000000002a T main
                 U printf
0000000000000000 T add(int, int)
0000000000000000 W twice(int)
0000000000000000 B zeroed
0000000000000004 d file_local
0000000000000000 r banner
0000000000000018 t helper(int)
0000000000000020 b big_table
$ readelf -SW sections.o | grep -E ' \.(text|data|bss|rodata)'
  [ 2] .text             PROGBITS        0000000000000000 000048 0000a6 00  AX  0   0  1
  [ 4] .data             PROGBITS        0000000000000000 0000f0 000008 00  WA  0   0  4
  [ 5] .bss              NOBITS          0000000000000000 0000f8 400020 00  WA  0   0 32
  [ 6] .rodata           PROGBITS        0000000000000000 0000f8 000016 00   A  0   0  8
  [ 7] .text._Z5twicei   PROGBITS        0000000000000000 00010e 000012 00 AXG  0   0  1
$ g++ sections.o -o sections && size sections && ls -l sections
   text	   data	    bss	    dec	    hex	filename
   1668	    608	4194368	4196644	 400924	sections
-rwxrwxr-x 1 user user 16288 Nov  3 19:01 sections
```

Things to notice: `.bss` is 4 MiB in memory but the executable is 16 KB. `twice` lives in its own section `.text._Z5twicei` with the `G` (group) flag. Every TU that uses an `inline` function or template instantiation emits a copy in a **COMDAT group**, and the linker keeps one and discards the rest, which is how the ODR exception for `inline` and templates works mechanically. The `U printf` entry is an undefined reference for the linker to resolve. The tools are covered in depth in [Debugging and Profiling Tools: binutils and ELF inspection](../tools/Debugging_and_Profiling_Tools.md#13-binutils-and-elf-inspection).

## 13.7 Symbols, Binding, and Weak Symbols

Each symbol-table entry has a name, value (address or offset), size, **type** (`FUNC`, `OBJECT`, `TLS`, `IFUNC`, ...), **binding**, **visibility**, and section index (`UND` if undefined).

| Binding / visibility | Meaning | `nm` letter |
|---|---|---|
| `LOCAL` | `static` functions and variables, anonymous-namespace entities: invisible outside the object | lowercase (`t`, `d`, `b`, `r`) |
| `GLOBAL` | Normal external-linkage definitions | uppercase (`T`, `D`, `B`, `R`) |
| `WEAK` | Global, but may be overridden, and may stay undefined | `W`/`w` (functions), `V`/`v` (objects) |
| `GNU_UNIQUE` | Static locals of inline functions and static data members of templates: one copy per process even across `RTLD_LOCAL` libraries | `u` |
| Visibility `DEFAULT` / `HIDDEN` / `PROTECTED` | Whether a global symbol is **exported** from the `.so`/executable ([13.11](#1311-symbol-visibility-and-export-control)) | Hidden symbols are not in `.dynsym` |

**Static-link resolution rules** (`ld` combining `.o` files):

1. Two **strong** (GLOBAL) definitions of the same name: `multiple definition of 'x'` error.
2. One strong and any number of **weak** definitions: the strong one wins, silently.
3. Only weak definitions: one of them is picked (normally the first). COMDAT groups for inline functions and templates behave like this.
4. A **weak undefined** reference that nobody defines resolves to address 0 instead of failing the link.

```cpp
// weak_demo.cpp -- g++ -std=c++20 weak_demo.cpp -o weak_demo
//                  g++ -std=c++20 weak_demo.cpp strong_hooks.cpp -o weak_demo2
#include <cstdio>

// 1) Weak DEFINITION: a default that any strong definition elsewhere replaces at link time.
extern "C" __attribute__((weak)) void on_kernel_complete(const char* name) {
    std::printf("default hook: %s\n", name);
}

// 2) Weak UNDEFINED reference: links even if nobody defines it; address is then null.
extern "C" __attribute__((weak)) void optional_tracer_flush();

int main() {
    on_kernel_complete("gemm_f16");
    if (optional_tracer_flush) optional_tracer_flush();   // must test before calling
    else std::puts("no tracer linked in");
}
```

```cpp
// strong_hooks.cpp -- strong definitions win over the weak ones at static link time
#include <cstdio>
extern "C" void on_kernel_complete(const char* name) { std::printf("custom hook: %s\n", name); }
extern "C" void optional_tracer_flush() { std::puts("tracer flushed"); }
```

```text
$ ./weak_demo
default hook: gemm_f16
no tracer linked in
$ ./weak_demo2
custom hook: gemm_f16
tracer flushed
$ nm weak_demo | grep -E 'on_kernel|optional'
0000000000001179 W on_kernel_complete
                 w optional_tracer_flush
```

Weak-symbol pitfalls:

- **The dynamic loader does not prefer strong over weak.** At run time, glibc's `ld.so` binds to the *first* definition in search order, weak or not (`LD_DYNAMIC_WEAK=1` restores the old behavior). Weak-overrides-strong is a *static-link* rule only.
- **Archives are not searched for weak undefined references.** If the only reference to `optional_tracer_flush` is weak, the linker will not extract `libtracer.a(flush.o)` to satisfy it, so the hook stays null. Link the object directly or add a strong reference.
- Calling a weak undefined function without the null check jumps to address 0 and segfaults.
- Uses: default hooks that applications can override (allocator hooks, `__attribute__((weak)) main`-style test hooks); optional integration with a library that may not be linked; and libc's own internal aliases. Replacing global `operator new` is a related mechanism. The replacement works because the executable's definition is found first at link and load time, not because libstdc++'s version is weak.

## 13.8 Position-Independent Code, the PLT/GOT, and Lazy Binding

A shared library is mapped at a different address in every process (ASLR), yet its code pages are shared read-only between processes, so they cannot be patched per process. **Position-independent code** (`-fPIC`) solves this with two rules:

1. Code refers to its own code and data **PC-relatively** (x86-64 `lea sym(%rip)`), which works at any load address.
2. Anything whose address is only known at load time, such as a function or variable in another `.so` or an interposable symbol of its own, is reached **through a table of addresses in writable data**: the **Global Offset Table (GOT)**. The dynamic loader fills it in per process.

Function calls go through a small stub in the **Procedure Linkage Table (PLT)**: `call foo@plt` → `jmp *GOT[foo]`. With **lazy binding**, `GOT[foo]` initially points back into the PLT. The first call pushes a relocation index and jumps to `PLT0`, which calls `_dl_runtime_resolve` in `ld.so`. That routine looks the symbol up, writes the real address into `GOT[foo]`, and jumps there. Every later call is a single indirect jump.

```cpp
// libgreet.cpp -- g++ -fPIC -shared libgreet.cpp -o libgreet.so
#include <cstdio>
extern "C" void greet(const char* who) { std::printf("hello, %s\n", who); }
```

```cpp
// app.cpp -- g++ app.cpp -L. -lgreet -Wl,-rpath,'$ORIGIN' -Wl,-z,lazy -o app_lazy
//            g++ app.cpp -L. -lgreet -Wl,-rpath,'$ORIGIN' -o app_now     (Ubuntu default: -z now)
extern "C" void greet(const char* who);
int main() { greet("first"); greet("second"); }
```

```text
$ objdump -d --no-show-raw-insn app_lazy        (abridged)
0000000000001020 <.plt>:                           PLT0: common resolver trampoline
    1020: push   0x2fca(%rip)        # 3ff0 <_GLOBAL_OFFSET_TABLE_+0x8>    (link_map*)
    1026: jmp    *0x2fcc(%rip)       # 3ff8 <_GLOBAL_OFFSET_TABLE_+0x10>   (_dl_runtime_resolve)
    1030: endbr64
    1034: push   $0x0                                                       (relocation index of greet)
    1039: jmp    1020 <_init+0x20>
0000000000001050 <greet@plt>:                      (.plt.sec: IBT/CET-style stub)
    1050: endbr64
    1054: jmp    *0x2fa6(%rip)       # 4000 <greet>  <- GOT slot: first time -> 1030, later -> greet
0000000000001149 <main>:
    ...
    115b: call   1050 <greet@plt>

$ readelf -rW app_lazy | grep -A2 rela.plt
Relocation section '.rela.plt' at offset 0x600 contains 1 entry:
0000000000004000  0000000300000007 R_X86_64_JUMP_SLOT     0000000000000000 greet + 0

$ LD_DEBUG=bindings ./app_lazy 2>&1 | grep -E 'calling init: /tmp|greet'
     calling init: /tmp/cppf/elf/libgreet.so
     binding file ./app_lazy [0] to /tmp/cppf/elf/libgreet.so [0]: normal symbol `greet'   <- at FIRST CALL
$ LD_DEBUG=bindings ./app_now 2>&1 | grep -E 'calling init: /tmp|greet'
     binding file ./app_now [0] to /tmp/cppf/elf/libgreet.so [0]: normal symbol `greet'    <- at LOAD time
     calling init: /tmp/cppf/elf/libgreet.so
$ readelf -d app_now | grep FLAGS
 0x000000000000001e (FLAGS)              BIND_NOW
 0x000000006ffffffb (FLAGS_1)            Flags: NOW PIE
```

| Knob | Effect | Why |
|---|---|---|
| Lazy binding (`-z lazy`; glibc's traditional default) | Resolve each function on first call | Faster startup for programs that call a small fraction of thousands of imports |
| `-z now` / `LD_BIND_NOW=1` | Resolve everything at load | Fail fast on missing symbols; no first-call latency spikes (important in profilers and real-time code); required for full RELRO. Ubuntu's GCC defaults to it, as shown |
| `-z relro` + `-z now` = **full RELRO** | GOT is made read-only (`mprotect`) after relocation | Blocks GOT-overwrite exploits |
| `-fno-plt` | Calls become `call *foo@GOTPCREL(%rip)` with no PLT stub | One fewer jump; implies eager binding for those calls |
| `-fvisibility=hidden`, `-fno-semantic-interposition`, `-Wl,-Bsymbolic` | Calls to the library's *own* functions bind directly | Allows inlining and direct calls inside the `.so` ([13.11](#1311-symbol-visibility-and-export-control)) |

**Costs.** On x86-64, PIC itself is nearly free thanks to RIP-relative addressing. On 32-bit x86 it reserved a register. The real cost is that every cross-library call is indirect and cannot be inlined, and that, by default, a `-fPIC` library's calls to its *own* exported functions also go through the PLT because they *might* be interposed. Fedora 32 reported CPython running 5% to 27% faster (Red Hat later quoted up to 30% for RHEL 8.2) after building `libpython` with `-fno-semantic-interposition`.

**Data references and copy relocations.** When a non-PIC (or PIE) executable references a global *variable* defined in a `.so`, the linker reserves space for it in the executable's `.bss` and emits an `R_X86_64_COPY` relocation. At load, the variable's initial value is copied there, and the library's own accesses (through its GOT) are redirected to the executable's copy. This is why the **size of an exported variable is part of the ABI**: grow it in the library and the executable's copy is too small.

## 13.9 Runtime Loading: dlopen and dlsym

`dlopen` loads a shared object (and its `DT_NEEDED` dependencies) at run time, and `dlsym` looks up a symbol by name. This is how plugin systems, Python extension modules, and profiler tool libraries are loaded. Since glibc 2.34 these functions live in `libc.so.6`, so `-ldl` is no longer required (it is harmless).

```cpp
// counter_plugin.h -- the ONLY contract between host and plugin
#pragma once
#include <cstdint>

struct CounterPlugin {                       // abstract interface: vtable crosses the boundary
    virtual ~CounterPlugin() = default;
    virtual const char* name() const = 0;
    virtual std::uint64_t sample(std::uint64_t cycles) = 0;
};

// C-linkage factory: unmangled, stable name the host can dlsym() for.
extern "C" {
using create_fn  = CounterPlugin* (*)();
using destroy_fn = void (*)(CounterPlugin*);
inline constexpr std::uint32_t kPluginAbiVersion = 1;
}
```

```cpp
// occupancy_plugin.cpp -- g++ -std=c++20 -fPIC -shared -fvisibility=hidden occupancy_plugin.cpp -o libocc.so
#include "counter_plugin.h"
#include <cstdio>

namespace {
struct Occupancy final : CounterPlugin {
    std::uint64_t total = 0;
    const char* name() const override { return "occupancy"; }
    std::uint64_t sample(std::uint64_t cycles) override { return total += cycles / 2; }
};
struct LoadBanner {                     // runs when dlopen maps the library (.init_array)
    LoadBanner()  { std::puts("[plugin] static init"); }
    ~LoadBanner() { std::puts("[plugin] static fini"); }  // runs at dlclose (or exit)
} banner;
}  // namespace

#define PLUGIN_API extern "C" __attribute__((visibility("default")))
PLUGIN_API std::uint32_t plugin_abi_version() { return kPluginAbiVersion; }
PLUGIN_API CounterPlugin* create_plugin() { return new Occupancy; }
PLUGIN_API void destroy_plugin(CounterPlugin* p) { delete p; }   // free in the same module that allocated
```

```cpp
// host.cpp -- g++ -std=c++20 host.cpp -o host   (glibc >= 2.34: no -ldl needed)
#include "counter_plugin.h"
#include <cstdio>
#include <dlfcn.h>
#include <memory>

int main(int argc, char** argv) {
    const char* path = argc > 1 ? argv[1] : "./libocc.so";

    // RTLD_NOW: resolve every undefined symbol now (fail here, not mid-run).
    // RTLD_LOCAL: plugin's symbols are not added to the global scope.
    void* h = dlopen(path, RTLD_NOW | RTLD_LOCAL);
    if (!h) { std::fprintf(stderr, "dlopen: %s\n", dlerror()); return 1; }

    dlerror();  // clear stale error; a symbol's value may legitimately be NULL
    auto version = reinterpret_cast<std::uint32_t (*)()>(dlsym(h, "plugin_abi_version"));
    auto create  = reinterpret_cast<create_fn>(dlsym(h, "create_plugin"));
    auto destroy = reinterpret_cast<destroy_fn>(dlsym(h, "destroy_plugin"));
    if (const char* err = dlerror()) { std::fprintf(stderr, "dlsym: %s\n", err); return 1; }
    if (version() != kPluginAbiVersion) { std::fprintf(stderr, "ABI mismatch\n"); return 1; }

    {
        std::unique_ptr<CounterPlugin, destroy_fn> p(create(), destroy);
        p->sample(100);
        std::printf("%s -> %llu\n", p->name(), static_cast<unsigned long long>(p->sample(40)));
    }   // destroy the object BEFORE unmapping its code (vtable + destructor live in the .so)

    dlclose(h);
    std::puts("[host] done");
}
```

```text
$ ./host
[plugin] static init
occupancy -> 70
[plugin] static fini
[host] done
$ nm -DC --defined-only libocc.so          # -fvisibility=hidden: only the 3 entry points are exported
0000000000001249 T create_plugin
000000000000128a T destroy_plugin
0000000000001204 T plugin_abi_version
```

| Flag / handle | Meaning |
|---|---|
| `RTLD_LAZY` / `RTLD_NOW` | Bind functions on first call, or all at `dlopen` (fails early, preferred for plugins) |
| `RTLD_LOCAL` (default) / `RTLD_GLOBAL` | Whether the library's symbols join the global lookup scope for libraries loaded *later*. Python loads extensions `RTLD_LOCAL`, which is why two extensions bundling different versions of one library can coexist |
| `RTLD_NODELETE` | `dlclose` never unmaps (safe when callbacks or `thread_local`s may outlive it) |
| `RTLD_NOLOAD` | Only return a handle if it is already loaded ("is the HIP runtime in this process?") |
| `RTLD_DEEPBIND` | Prefer the library's own symbols over global ones. Isolates the library, but breaks `LD_PRELOAD` interposition and sanitizers |
| `RTLD_DEFAULT` / `RTLD_NEXT` (pseudo-handles to `dlsym`) | Search the global scope / the next object after the caller ([13.10](#1310-symbol-interposition-and-ld_preload)) |

Plugin rules that interviewers like to probe:

- **Expose `extern "C"` factories**, not mangled C++ names. The mangled name depends on the compiler and ABI, and `dlsym` needs an exact string. Version the ABI explicitly (`plugin_abi_version`), or pass a struct whose first member is its `size` so it can grow compatibly.
- **Destroy every object created by the plugin before `dlclose`**. Its vtable, its destructor code, and any `std::function` targets live in the unmapped pages, and a later call crashes at an address that belongs to no mapping.
- **Free memory in the module that allocated it** (`destroy_plugin`). On Linux both usually share one `malloc`, but statically linked runtimes, custom allocators, and Windows CRTs do not.
- **RTTI and exceptions across the boundary** need the `type_info` objects to be the same or comparable. Give interface and exception types default visibility (export them) so `dynamic_cast` and `catch` work in the host.
- `dlclose` decrements a reference count and may not unload at all: libraries with `GNU_UNIQUE` symbols, `RTLD_NODELETE`, or pending `thread_local` destructors stay mapped.
- Casting `void*` to a function pointer is "conditionally supported" in ISO C++, and POSIX requires it to work.

### Static Initialization and Shared Libraries

- At load, `ld.so` runs each object's initializers (`DT_INIT` / `.init_array`, which is where namespace-scope constructors go) in **dependency order**: a library's dependencies are initialized before it. The executable's own static constructors run **after** all initially loaded libraries, from `__libc_start_main`. With `dlopen`, the plugin's initializers run inside the `dlopen` call (`[plugin] static init` above), and its destructors in `dlclose` or at exit.
- So a library's static constructor must not depend on the executable's globals already being constructed, and constructors in two libraries with no dependency relation run in an unspecified relative order. This is the static initialization order fiasco across `.so` boundaries. The cure is the same as within a program: construct on first use (function-local statics, which are thread-safe since C++11).
- `__attribute__((constructor(N)))` sets priorities only *within* one linked object. `LD_DEBUG=libs` prints `calling init: ...` lines showing the actual order.
- Profiler tool libraries rely on this. A tool can do its setup in a constructor that runs when it is preloaded, before the application's `main`, but it must not call into runtimes (HIP/HSA) that are not initialized yet.

## 13.10 Symbol Interposition and LD_PRELOAD

When the dynamic loader resolves a symbol reference, from the executable *or from inside any library*, it searches the **global lookup scope** in order and takes the **first** definition:

```text
executable  →  LD_PRELOAD libraries (in order)  →  DT_NEEDED libraries (breadth-first, load order)  →  RTLD_GLOBAL dlopen'ed libs
```

So a preloaded library that defines `malloc` replaces glibc's `malloc` for the program *and* for `libstdc++`, `libamdhip64`, and every other library that calls `malloc` through its PLT/GOT. This is **symbol interposition**. It is how `jemalloc` or `tcmalloc` drop in without relinking, how `libfaketime` fakes the clock, and how many tracing tools work. The wrapper reaches the real implementation with `dlsym(RTLD_NEXT, "malloc")`: "the next definition in search order after me".

Rules and limits:

- `LD_PRELOAD` takes a colon- or space-separated list. `/etc/ld.so.preload` applies system-wide. In **secure-execution mode** (setuid/setgid binaries), only libraries in standard directories that are themselves setuid are honoured.
- Only references resolved **through the dynamic symbol table** can be interposed. These are missed: calls inside a library to its own functions that were bound directly (`-fvisibility=hidden`, `-Bsymbolic`, `-fno-semantic-interposition`, or `static`/inline functions); statically linked code; system calls made directly; and libraries loaded with `RTLD_DEEPBIND`.
- A wrapper **must not recurse**. `printf`, `new`, `std::string`, and even `dlsym` may call `malloc`. Keep the hook minimal, use a re-entrancy guard, and serve bootstrap allocations from a static buffer.
- Wrapping `malloc` and `free` alone is incomplete: `calloc`, `realloc`, `posix_memalign`, `aligned_alloc`, `memalign`, `valloc`, `malloc_usable_size` (and `operator new` if you count C++ separately) must be consistent. A real allocator replacement overrides all of them.

### Example 1: Counting Every `malloc` in an Unmodified Program

```cpp
// mallocspy.cpp -- count every malloc/free in an unmodified program.
// Build: g++ -std=c++20 -O2 -fPIC -shared mallocspy.cpp -o libmallocspy.so
// Use:   LD_PRELOAD=$PWD/libmallocspy.so ls /
#include <atomic>
#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <dlfcn.h>
#include <unistd.h>

namespace {
using malloc_fn = void* (*)(std::size_t);
using free_fn   = void (*)(void*);

malloc_fn real_malloc = nullptr;
free_fn   real_free   = nullptr;
std::atomic<std::size_t> n_malloc{0}, n_free{0}, n_bytes{0};

// dlsym() may itself allocate (e.g. for an error string) -> serve those
// requests from a static buffer instead of recursing into ourselves.
alignas(std::max_align_t) char bootstrap[4096];
std::atomic<std::size_t> boot_used{0};
bool in_bootstrap(void* p) { return p >= bootstrap && p < bootstrap + sizeof bootstrap; }

void resolve() {
    // initial-exec TLS lives in the static TLS block: touching it never calls malloc.
    static thread_local bool resolving __attribute__((tls_model("initial-exec"))) = false;
    if (resolving) return;
    resolving = true;
    real_malloc = reinterpret_cast<malloc_fn>(dlsym(RTLD_NEXT, "malloc"));  // next definition after us
    real_free   = reinterpret_cast<free_fn>(dlsym(RTLD_NEXT, "free"));
    resolving = false;
}
}  // namespace

extern "C" void* malloc(std::size_t n) {
    if (!real_malloc) {
        resolve();
        if (!real_malloc) {                                  // called from inside dlsym
            std::size_t off = boot_used.fetch_add((n + 15) & ~std::size_t{15});
            return off + n <= sizeof bootstrap ? bootstrap + off : nullptr;
        }
    }
    n_malloc.fetch_add(1, std::memory_order_relaxed);
    n_bytes.fetch_add(n, std::memory_order_relaxed);
    return real_malloc(n);   // NEVER call printf/new here: they may call malloc -> infinite recursion
}

extern "C" void free(void* p) {
    if (!p || in_bootstrap(p)) return;
    if (!real_free) resolve();
    n_free.fetch_add(1, std::memory_order_relaxed);
    real_free(p);
}

// Runs when the library is unloaded at exit. Use write(2) + snprintf into a stack
// buffer rather than stdio, which may already be torn down or may allocate.
__attribute__((destructor)) static void report() {
    char buf[160];
    int len = std::snprintf(buf, sizeof buf, "[mallocspy] malloc=%zu free=%zu bytes=%zu\n",
                            n_malloc.load(), n_free.load(), n_bytes.load());
    if (len > 0) {
        ssize_t rc = write(STDERR_FILENO, buf, static_cast<std::size_t>(len));
        (void)rc;
    }
}
```

```text
$ cat t.cpp
#include <string>
#include <vector>
int main() { std::vector<std::string> v; for (int i = 0; i < 1000; ++i) v.emplace_back(64, 'x'); }
$ g++ -std=c++20 t.cpp -o t && LD_PRELOAD=$PWD/libmallocspy.so ./t
[mallocspy] malloc=1012 free=1011 bytes=204232
$ LD_PRELOAD=$PWD/libmallocspy.so python3 -c pass
[mallocspy] malloc=2417 free=2420 bytes=3221858       <- free > malloc: calloc/realloc are not wrapped
```

The C++ program made 1000 string allocations plus 11 vector growths (capacity 1 → 1024) plus one allocation from libstdc++ startup (the emergency exception-handling pool, never freed, hence `free = malloc - 1`). `operator new` reached our `malloc` from inside `libstdc++.so` without any relinking: that is interposition.

### Example 2: Wrapping a HIP Runtime API

The same technique works for any C API exported by a shared library. HIP's runtime API is declared `extern "C"`, so the symbols are unmangled:

```cpp
// hipspy.cpp -- log hipMalloc/hipFree of an UNMODIFIED HIP application.
// Build: g++ -std=c++20 -O2 -fPIC -shared hipspy.cpp -o libhipspy.so   (no HIP headers needed)
// Use:   LD_PRELOAD=$PWD/libhipspy.so ./my_hip_app
#include <chrono>
#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <dlfcn.h>

extern "C" {
using hipError_t = int;              // a C enum in hip_runtime_api.h: same ABI as int on x86-64 Linux
}

template <class Fn>
static Fn next_symbol(const char* name) {
    void* sym = dlsym(RTLD_NEXT, name);   // the definition that WOULD have been used (libamdhip64.so)
    if (!sym) { std::fprintf(stderr, "[hipspy] cannot resolve %s: %s\n", name, dlerror()); std::abort(); }
    return reinterpret_cast<Fn>(sym);
}

// The HIP C API is declared extern "C", so the exported names are unmangled.
extern "C" hipError_t hipMalloc(void** ptr, std::size_t size) {
    static const auto real = next_symbol<hipError_t (*)(void**, std::size_t)>("hipMalloc");
    auto t0 = std::chrono::steady_clock::now();
    hipError_t rc = real(ptr, size);
    double us = std::chrono::duration<double, std::micro>(std::chrono::steady_clock::now() - t0).count();
    std::fprintf(stderr, "[hipspy] hipMalloc(%zu B) -> %p rc=%d (%.1f us)\n", size, rc == 0 ? *ptr : nullptr, rc, us);
    return rc;
}

extern "C" hipError_t hipFree(void* ptr) {
    static const auto real = next_symbol<hipError_t (*)(void*)>("hipFree");
    std::fprintf(stderr, "[hipspy] hipFree(%p)\n", ptr);
    return real(ptr);
}
```

```text
$ nm -D /opt/rocm/lib/libamdhip64.so | grep -E ' hip(Malloc|Free)@'     # (a ROCm nightly here)
000000000049bbd0 T hipFree@@hip_4.2
00000000004bcf20 T hipMalloc@@hip_4.2
$ LD_PRELOAD=$PWD/libhipspy.so ./app                 # app: hipMalloc 1 MiB, then hipFree
[hipspy] hipMalloc(1048576 B) -> 0x7cfcd3a00000 rc=0 (80005.3 us)
[hipspy] hipFree(0x7cfcd3a00000)
app: rc=0
```

Notes: the first `hipMalloc` took 80 ms because it also initialized the runtime and the device. That is a classic profiling artifact, so warm up before measuring. The library exports *versioned* symbols (`hipMalloc@@hip_4.2`), and an unversioned definition in the preloaded library still satisfies the application's versioned reference. `fprintf` is safe here, unlike inside a `malloc` hook.

### How Production GPU Profilers Hook Runtimes

`LD_PRELOAD` wrappers are the simplest interception technique, but they are fragile. You must wrap every entry point by hand with an exactly matching signature. Calls the runtime makes to itself are missed. The approach depends on load order and breaks with static linking or `RTLD_DEEPBIND`. And every tool that wants the same function competes for one slot. ROCm's tooling therefore uses **dispatch (intercept) tables**:

1. Each ROCm runtime (HIP, HSA, ROCTx, ...) routes every public API call through a **table of function pointers**: `hipMalloc` is a thin stub that calls `table->hipMalloc_fn`.
2. At initialization, each runtime registers its table with **rocprofiler-register**. That library checks whether a tool is present: some loaded library exports `rocprofiler_configure` (for example, one preloaded into the process), or the `ROCP_TOOL_LIBRARIES` environment variable names one.
3. If a tool is present, **rocprofiler-sdk** saves the original pointers and installs wrappers that emit callback-tracing or buffered records, then call the saved original. Tools that want raw access can receive the table itself (`rocprofiler_at_intercept_table_registration`) and chain their own wrappers, the same "save the next pointer and call it" pattern as `RTLD_NEXT`. `rocprofv3` is built on this SDK.
4. The older mechanism was the HSA runtime loading the libraries named in `HSA_TOOLS_LIB` and handing them its API table (`OnLoad`). That required a race to set environment variables before the runtime initialized, which is what rocprofiler-register replaced.

| Technique | How it works | Pros | Cons / used by |
|---|---|---|---|
| `LD_PRELOAD` + `RTLD_NEXT` | Interpose exported symbols | No rebuild; any C API | Fragile; misses internal calls. ltrace-style tools, allocator swaps |
| Dispatch-table interception | Runtime calls through a patchable table | Catches all API calls, chains tools, low overhead | Runtime must be designed for it. rocprofiler-sdk, CUPTI (CUDA) |
| `-Wl,--wrap=sym` | Link-time: references to `sym` go to `__wrap_sym`, and `__real_sym` is the original | Zero runtime magic | Requires relinking; only rewrites undefined references in the objects being linked (not calls from inside other shared libraries or intra-object calls) |
| GOT patching at run time | Rewrite a loaded object's GOT entries | Per-library targeting, after load | Platform-specific. E.g. LLNL GOTCHA |
| `LD_AUDIT` (`la_symbind64`) | glibc's rtld-audit interface sees every symbol binding | Can redirect any binding | Overhead, rarely used outside tooling |
| Binary instrumentation / trampolines | Rewrite instructions at function entry | Works on internal, non-exported functions | Complex. Dyninst (used by rocprof-sys, formerly Omnitrace), Frida, uprobes/eBPF |

> **See also:** [AMD GPU architecture and profiling](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md) · [rocprof-compute project deep dive](../career/Project_Deep_Dive_rocprof-compute.md) · [ROCm profiling tools](../ml-gpu/Parallel_GPU_Programming.md#305-rocm-profiling-tools) · [strace and ltrace](../tools/Debugging_and_Profiling_Tools.md#12-strace-and-ltrace)

## 13.11 Symbol Visibility and Export Control

On ELF, **every non-`static` symbol in a shared library is exported by default**, the opposite of Windows DLLs, which export nothing unless marked `__declspec(dllexport)`. Exporting everything has real costs:

- A larger `.dynsym` and more relocations, so slower load and symbol lookup.
- Every exported function is **interposable**, so the compiler must call even the library's own functions through the PLT and cannot inline them across TUs (semantic interposition).
- An accidental ABI surface: users start depending on your internals.
- **Symbol clashes**: if two `.so`s in one process each statically include a different version of the same library (LLVM, protobuf, fmt), the exported duplicates interpose on each other and you get ODR violations that crash at run time.

The fix is to hide by default and export deliberately:

```cpp
// metrics.h -- public header of libmetrics.so
#pragma once
#include <string>
#include <vector>

#if defined(METRICS_BUILDING)          // set only while compiling the library itself
#  define METRICS_API __attribute__((visibility("default")))
#else
#  define METRICS_API                  // consumers: plain declaration (on Windows: dllimport)
#endif

namespace metrics {
class METRICS_API Collector {          // exported class: vtable, typeinfo, members
public:
    virtual ~Collector();
    void add(double v);
    double mean() const;
private:
    std::vector<double> values_;
};
METRICS_API std::string version();
}  // namespace metrics
```

```cpp
// metrics.cpp -- build:
//   g++ -std=c++20 -O2 -fPIC -shared -fvisibility=hidden -fvisibility-inlines-hidden -DMETRICS_BUILDING metrics.cpp -o libmetrics.so
#include "metrics.h"
#include <numeric>

namespace metrics {
namespace detail {                       // not exported: hidden by -fvisibility=hidden
double sum(const std::vector<double>& v) { return std::accumulate(v.begin(), v.end(), 0.0); }
}
Collector::~Collector() = default;
void Collector::add(double v) { values_.push_back(v); }
double Collector::mean() const { return values_.empty() ? 0.0 : detail::sum(values_) / values_.size(); }
std::string version() { return "1.2.0"; }
}  // namespace metrics
```

```text
$ nm -DC --defined-only libmetrics.so          # hidden by default + explicit exports
0000000000001430 T metrics::version[abi:cxx11]()
0000000000001280 T metrics::Collector::add(double)
00000000000011f0 T metrics::Collector::~Collector()
00000000000011c0 T metrics::Collector::~Collector()
00000000000011c0 T metrics::Collector::~Collector()
00000000000013c0 T metrics::Collector::mean() const
0000000000003dc8 V typeinfo for metrics::Collector
0000000000002020 V typeinfo name for metrics::Collector
0000000000003dd8 V vtable for metrics::Collector

# Same source at -O0: default visibility exports 93 symbols (76 of them std:: template
# instantiations such as vector<double>::_M_realloc_append); -fvisibility=hidden alone
# still exports 92 (libstdc++ declares namespace std with default visibility);
# adding -fvisibility-inlines-hidden brings it to 9.
```

| Tool | Effect |
|---|---|
| `-fvisibility=hidden` | Default visibility of definitions in this TU becomes hidden. Does not override explicit visibility attributes or pragmas in headers, e.g. libstdc++'s `namespace std` (declared with `_GLIBCXX_VISIBILITY(default)`), which is why `-fvisibility-inlines-hidden` is also needed to hide inline `std::` template instantiations |
| `-fvisibility-inlines-hidden` | Inline member functions (including template instantiations from headers) are hidden |
| `__attribute__((visibility("default")))` on a class | Exports its members, vtable, and typeinfo. Needed for exceptions and `dynamic_cast` across the boundary |
| `#pragma GCC visibility push(hidden)` ... `pop` | Region-wide default, e.g. around third-party headers |
| `-Wl,--exclude-libs,ALL` | Hide every symbol that came from static archives linked into this `.so`, which prevents the duplicate-library clash above |
| Linker **version script** (`-Wl,--version-script=lib.map`) | Whitelist exports with wildcards, and attach **symbol versions** (`hipMalloc@@hip_4.2`, `memcpy@GLIBC_2.14`) so one `.so` can keep old behavior for old binaries |
| `visibility("protected")` | Exported but not interposable from inside the library. Rarely used: it interacts badly with copy relocations |

In CMake, use `CXX_VISIBILITY_PRESET hidden`, `VISIBILITY_INLINES_HIDDEN ON`, and `GenerateExportHeader`. See [CMake: Symbol Visibility and Export Control](../tools/CMake_Fundamentals.md#67-symbol-visibility-and-export-control).

## 13.12 Library Search Paths: RPATH, RUNPATH, and $ORIGIN

For each `DT_NEEDED` name without a slash, `ld.so` searches in order: **`DT_RPATH`** (only if there is no `DT_RUNPATH`; inherited by libraries loaded on that object's behalf) → **`LD_LIBRARY_PATH`** (ignored for setuid) → **`DT_RUNPATH`** (applies only to that object's *direct* dependencies) → **`/etc/ld.so.cache`** (built by `ldconfig`) → default directories (`/lib`, `/usr/lib`, and multiarch variants).

- `-Wl,-rpath,DIR` writes `DT_RUNPATH` on modern toolchains (`--enable-new-dtags` is the default on most distros) and `DT_RPATH` with `--disable-new-dtags`. RUNPATH can be overridden by the user's `LD_LIBRARY_PATH`. RPATH cannot.
- **`$ORIGIN`** expands at load time to the directory of the object that contains the entry, so `-Wl,-rpath,'$ORIGIN/../lib'` makes an install tree relocatable (ROCm, conda, and wheels bundled by auditwheel all use this). Quote it so the shell does not expand it, and write `$$ORIGIN` inside Makefiles.
- **The transitive trap**: the executable's RUNPATH does not apply to its libraries' dependencies, so every `.so` that needs siblings must carry its own `$ORIGIN` runpath.
- `dlopen("libfoo.so")` uses the RUNPATH of the object that *calls* `dlopen`, which matters for plugin loaders and profiler tools.
- Diagnose with `readelf -d app | grep -E 'NEEDED|RUNPATH'`, `LD_DEBUG=libs ./app`, `ldd` (not on untrusted binaries), and experiment with `patchelf --set-rpath`.

Full treatment, including CMake's build vs install RPATH and a troubleshooting table: [CMake: RPATH and RUNPATH](../tools/CMake_Fundamentals.md#65-rpath-and-runpath). Command-level inspection: [readelf and ldd](../tools/Debugging_and_Profiling_Tools.md#133-readelf-and-ldd-dependencies-and-loading).

## 13.13 ABI Stability and the libstdc++ Dual ABI

The **API** is what source code compiles against. The **ABI** is what *already compiled* binaries rely on: symbol names (mangling), calling conventions, object sizes and layouts, vtable layouts, `type_info` and exception-handling formats, and the semantics of inline code that callers have compiled in. On Linux, GCC and Clang follow the **Itanium C++ ABI**, so they interoperate. MSVC uses a different ABI.

**What breaks ABI** (old binaries + new library = crash or link error):

| Change to a library type or function | Breaks? | Why |
|---|---|---|
| Add, remove, reorder, or retype a non-static data member | **Yes** | `sizeof` and member offsets are compiled into callers (stack allocation, `new`, inline accessors, copy relocations) |
| Add a virtual function (even at the end) | **Yes** | vtable slots shift for derived classes; callers index the vtable by slot number |
| Reorder virtual functions, add or remove a virtual base, change a base class | **Yes** | vtable or object layout changes |
| Change a function's parameter types, cv-qualification, or namespace | **Yes** (link error) | Mangled name changes |
| Change a return type | **Yes** (silent!) | Not part of the mangled name for non-templates, so it links and then misbehaves |
| Make a function inline, or change an inline function's body | **Yes** (silent) | Old callers keep their inlined copy, so two behaviors coexist (an ODR violation across versions) |
| Change default arguments | Source-compatible, but old callers keep the old default | Defaults are compiled into the call site |
| Change an enum's underlying type, or add `noexcept` (part of the function *type* since C++17) | Can break | Affects layout and the mangling of function pointer types |
| Change template definitions | **Yes** for instantiations already compiled into clients | Instantiated code lives in the client |
| Add a non-virtual member function, a new free function, a new class, or a static member | No | New symbols only |
| Change private non-virtual, non-inline function bodies | No | Callers only know the symbol |

**Techniques for a stable ABI:**

- **pImpl**: the public class holds only `std::unique_ptr<Impl>`, so the data layout can change freely and `sizeof` stays one pointer. See [pImpl](../design-patterns/Design_Patterns_Cpp.md#29-pimpl----pointer-to-implementation).
- **A C API at the boundary**: `extern "C"` functions, opaque handles, and plain structs. HIP, HSA, and rocprofiler-sdk all expose C APIs for this reason. Make structs extensible by putting their size first (rocprofiler-sdk's `rocprofiler_tool_configure_result_t` starts with a `size` field) or by using reserved fields.
- **SONAME versioning**: `libfoo.so.2`. Bump the major version on every ABI break, so old and new can be installed side by side ([CMake: ABI and SOVERSION](../tools/CMake_Fundamentals.md#39-abi-and-soversion)).
- **Symbol versioning** with version scripts (glibc keeps `memcpy@GLIBC_2.2.5` *and* `memcpy@@GLIBC_2.14`), and **inline namespaces** (`inline namespace v2 { ... }` changes every mangled name).
- **Check it in CI**: `abidw`/`abidiff` (libabigail) or `abi-compliance-checker` compare two builds and report layout and symbol changes.

### The libstdc++ Dual ABI (`_GLIBCXX_USE_CXX11_ABI`)

C++11 forbade copy-on-write `std::string` and required O(1) `std::list::size()`. Both changes altered the layouts of these types. GCC 5 therefore shipped **both** implementations: the new ones live in the inline namespace `std::__cxx11`, which changes their mangled names, and the macro `_GLIBCXX_USE_CXX11_ABI` (default `1`) picks which one your code uses. Functions that *return* a new-ABI string with no new-ABI parameter get an `[abi:cxx11]` tag instead (see `metrics::version[abi:cxx11]()` above).

Mixing the two shows up as a link error:

```cpp
// report.cpp -- built as a library with the OLD ABI:
//   g++ -std=c++20 -D_GLIBCXX_USE_CXX11_ABI=0 -fPIC -shared report.cpp -o libreport.so
#include <string>
std::string make_report(const std::string& kernel) { return "kernel: " + kernel; }
```

```cpp
// main.cpp -- built with the default (new) ABI:
//   g++ -std=c++20 main.cpp -L. -lreport -Wl,-rpath,'$ORIGIN' -o main
#include <cstdio>
#include <string>
std::string make_report(const std::string& kernel);
int main() { std::puts(make_report("gemm").c_str()); }
```

```text
$ nm -DC libreport.so | grep make_report
0000000000002819 T make_report(std::string const&)                   <- _Z11make_reportRKSs (old ABI)
$ g++ -std=c++20 main.cpp -L. -lreport -Wl,-rpath,'$ORIGIN' -o main
/usr/bin/ld: main.cpp:(.text+0x4f): undefined reference to
  `make_report(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)'
```

Rebuild everything with the same setting. You meet this in practice with prebuilt C++ binaries: for years PyTorch's pip wheels were built with `_GLIBCXX_USE_CXX11_ABI=0` (manylinux2014). The Linux wheels moved to the new ABI (manylinux_2_28) around PyTorch 2.7. A C++ extension or a libtorch-linking tool must match: check `torch._C._GLIBCXX_USE_CXX11_ABI`. The related runtime error `version 'GLIBCXX_3.4.32' not found` is different: it means a binary built with a *newer* GCC is running against an *older* `libstdc++.so.6`. That library is backward compatible only (old binaries keep working with a new library, not the reverse), so build on the oldest target distro or ship the runtime.

> **See also:** [nm/objdump/readelf/ldd workflows](../tools/Debugging_and_Profiling_Tools.md#13-binutils-and-elf-inspection) · [CMake: Symbol Visibility](../tools/CMake_Fundamentals.md#67-symbol-visibility-and-export-control) · [CMake: RPATH](../tools/CMake_Fundamentals.md#65-rpath-and-runpath) · [Containers and CI (manylinux images)](../tools/Containers_and_CI.md)

## 13.14 Calling Conventions and the System V x86-64 ABI

A **calling convention** is the part of the ABI ([13.13](#1313-abi-stability-and-the-libstdc-dual-abi)) that lets separately compiled functions call each other. It fixes where arguments go, where the return value comes back, which registers a call may destroy, and how the stack must look at the call instruction. Linux, macOS, and the BSDs on x86-64 use the **System V AMD64 psABI**. C++ adds the **Itanium C++ ABI** on top of it for `this`, class types, and exceptions. A mismatch does not cause a compile error. The program reads garbage from the wrong register, so the convention has to be right in hand-written assembly, JIT compilers, FFI layers (`ctypes`, `cffi`), and binary instrumentation.

### Registers: Arguments, Return Values, and Who Saves What

| Purpose | Registers (System V x86-64) |
|---|---|
| Integer and pointer arguments 1-6 | `rdi`, `rsi`, `rdx`, `rcx`, `r8`, `r9` (in that order) |
| Floating-point and vector arguments 1-8 | `xmm0` - `xmm7` (counted separately from the integer registers) |
| Further arguments | On the stack, pushed right to left, so the 7th integer argument sits at `[rsp+8]` on entry (just above the return address) |
| Integer return value | `rax` (and `rdx` for the second eightbyte: `__int128`, two-word structs) |
| Floating-point return value | `xmm0` (and `xmm1`). `long double` comes back in x87 `st0`. |
| Large struct return | Caller passes a hidden pointer in `rdi`. The callee writes the result there and returns the same pointer in `rax`. |
| Variadic calls (`printf`) | `al` = upper bound on the number of vector registers used, so the callee's prologue knows whether to spill `xmm0-7` |
| `this` (C++) | Implicit first argument, so it takes `rdi` and the declared arguments shift by one |
| **Caller-saved** (volatile, "scratch") | `rax`, `rcx`, `rdx`, `rsi`, `rdi`, `r8` - `r11`, all `xmm`/`ymm`/`zmm` registers |
| **Callee-saved** (non-volatile) | `rbx`, `rbp`, `r12` - `r15`, `rsp` (plus the x87 control word and MXCSR control bits) |

**Why both kinds exist.** If every register were caller-saved, every value that is live across a call would have to be spilled to memory around each call. If every register were callee-saved, every function would have to save every register it touches, even leaf functions that call nothing. The split lets short-lived temporaries live in scratch registers for free, and long-lived values pay a save/restore once per function (in the prologue and epilogue) rather than once per call.

**Stack alignment.** `rsp` must be a multiple of 16 *at the `call` instruction*. The `call` pushes an 8-byte return address, so at function entry `rsp + 8` is 16-byte aligned. A function that calls others must re-align before doing so (a `push`, or `sub rsp, 8 + 16k`). Hand-written assembly or a JIT that gets this wrong crashes later, inside some unrelated library function, on an aligned SSE instruction such as `movaps`. The crash site is far from the bug.

**Red zone.** The 128 bytes *below* `rsp` are reserved for the current function: signal handlers and interrupts must not clobber them. A leaf function can keep its locals there without adjusting `rsp` at all. The Linux kernel builds with `-mno-red-zone`, because a hardware interrupt in kernel mode pushes its frame onto the current stack and would overwrite the zone. For user-space signals the kernel skips 128 bytes below `rsp` before it builds the signal frame.

### What the Compiler Actually Emits

```cpp
// abi.cpp -- g++ -std=c++20 -O2 -S -masm=intel -fcf-protection=none -fno-asynchronous-unwind-tables abi.cpp
#include <cstddef>
#include <memory>
#include <string_view>

long sum8(long a, long b, long c, long d, long e, long f, long g, long h) {
    return a + b + c + d + e + f + g + h;          // a..f in rdi..r9; g, h on the stack
}

double mix(int i, double x, long j, float y) {     // i=edi, x=xmm0, j=rsi, y=xmm1
    return i * x + j * y;                          // result in xmm0
}

struct Small { long id; double val; };             // 16 B: one INTEGER and one SSE eightbyte
double take_small(Small s) { return s.id + s.val; }  // s.id in rdi, s.val in xmm0

struct Big { long a, b, c; };                      // 24 B > 16 B: MEMORY class
Big make_big(long x) { return {x, x + 1, x + 2}; } // hidden result pointer in rdi, x in rsi

std::size_t len(std::string_view sv) { return sv.size(); }  // {size, data} in rdi, rsi

int deref_raw(int* p) { return *p; }                          // p in rdi
int deref_unique(std::unique_ptr<int> p) { return *p; }       // rdi = ADDRESS of a unique_ptr
```

```text
; output piped through c++filt; .cfi and other directives trimmed
sum8(long, long, long, long, long, long, long, long):
        add     rdi, rsi
        add     rdi, rdx
        add     rdi, rcx
        add     rdi, r8
        lea     rax, [rdi+r9]
        add     rax, QWORD PTR 8[rsp]      ; 7th argument: just above the return address
        add     rax, QWORD PTR 16[rsp]     ; 8th argument
        ret
mix(int, double, long, float):             ; ints and floats are numbered independently:
        movapd  xmm2, xmm0                 ;   x is the 1st FP arg (xmm0), y the 2nd (xmm1),
        pxor    xmm0, xmm0                 ;   j is the 2nd integer arg (rsi)
        cvtsi2sd xmm0, edi
        ...
take_small(Small):                         ; struct split across an integer and an SSE register
        movapd  xmm1, xmm0
        pxor    xmm0, xmm0
        cvtsi2sd xmm0, rdi
        addsd   xmm0, xmm1
        ret
make_big(long):                            ; sret: write through rdi, return rdi in rax
        lea     rdx, 1[rsi]
        mov     QWORD PTR [rdi], rsi
        add     rsi, 2
        mov     rax, rdi
        mov     QWORD PTR 8[rdi], rdx
        mov     QWORD PTR 16[rdi], rsi
        ret
len(std::basic_string_view<char, std::char_traits<char> >):
        mov     rax, rdi                   ; size is the first member in libstdc++
        ret
deref_raw(int*):
        mov     eax, DWORD PTR [rdi]       ; one load
        ret
deref_unique(std::unique_ptr<int, std::default_delete<int> >):
        mov     rax, QWORD PTR [rdi]       ; load the pointer out of the caller's temporary...
        mov     eax, DWORD PTR [rax]       ; ...then the int: an extra memory round trip
        ret
```

### How Aggregates Are Classified

The psABI splits a struct of up to 16 bytes into **eightbytes** and classifies each one: **INTEGER** (goes in the next free general-purpose register), **SSE** (next free `xmm`), or **MEMORY** (the whole object goes on the stack). Some results:

| Type | Size | Passed as | Returned in |
|---|---|---|---|
| `struct { long id; double val; }` | 16 B | `rdi` + `xmm0` | `rax` + `xmm0` |
| `struct { double a, b; }` | 16 B | `xmm0` + `xmm1` | `xmm0` + `xmm1` |
| `struct { float x, y, z, w; }` | 16 B | `xmm0` (x,y packed) + `xmm1` (z,w) | same |
| `std::string_view`, `std::span<T>` | 16 B, trivially copyable | two GPRs | `rax` + `rdx` |
| `struct { long a, b, c; }` | 24 B | copied onto the stack | hidden pointer (`rdi` in, `rax` out) |
| Any struct with a member that does not fit the two-register scheme (> 16 B, unaligned fields) | | MEMORY | hidden pointer |
| **C++: non-trivial copy/move constructor or destructor** (`std::unique_ptr`, `std::string`, `std::vector`, `std::shared_ptr`) | any | **by invisible reference**: caller materializes a temporary and passes its address | hidden pointer |

The last row is the Itanium C++ ABI rule for types that are **"non-trivial for the purposes of calls"**. Such an object cannot be bit-copied into a register, because its copy constructor or destructor must run on a real address. So `std::unique_ptr<int>` by value costs a stack temporary and an extra load, even though it is one pointer wide. Under the Itanium ABI the *caller* also destroys that temporary after the call returns (MSVC makes the callee destroy it), so the caller still emits a null check and a `delete` path and its exception cleanup. Clang offers `[[clang::trivial_abi]]` to opt a class out of this (libc++ can build `unique_ptr` that way under an ABI-breaking flag). GCC has no equivalent. That is why "pass `string_view`/`span` by value, but `unique_ptr` only when you transfer ownership" is real advice, not style.

### Other Conventions Worth Knowing

| | System V x86-64 (Linux, macOS) | Windows x64 | AArch64 AAPCS64 (Linux, macOS Arm) | Linux x86-64 `syscall` |
|---|---|---|---|---|
| Integer args | `rdi rsi rdx rcx r8 r9` | `rcx rdx r8 r9` | `x0` - `x7` | `rax` = syscall number, args `rdi rsi rdx r10 r8 r9` |
| FP args | `xmm0` - `xmm7` (separate count) | `xmm0` - `xmm3`, **by position** (2nd arg is `rdx` *or* `xmm1`) | `v0` - `v7` | none |
| Return | `rax`/`rdx`, `xmm0`/`xmm1` | `rax`, `xmm0` | `x0`/`x1`, `v0`-`v3` | `rax`; `-4095..-1` means `-errno` |
| Callee-saved | `rbx rbp r12-r15` | `rbx rbp rdi rsi r12-r15`, `xmm6-xmm15` | `x19-x28`, `x29` (FP), low 64 bits of `v8-v15` | everything except `rax`, `rcx`, `r11` |
| Stack extras | 128-byte red zone | 32-byte **shadow space** the caller reserves for the 4 register args; no red zone | Return address in link register `x30`, not on the stack; `x8` = indirect result pointer | `syscall` writes the return RIP to `rcx` and RFLAGS to `r11`, hence `r10` for arg 4 |

The 32-bit x86 conventions (`cdecl`, `stdcall`, `fastcall`, `thiscall`) mostly passed arguments on the stack. They matter only for legacy Windows code.

GPU code has its own conventions. On AMDGPU, a kernel's arguments are not in registers: the dispatch packet points at a **kernarg segment** in memory, and a pointer to it is preloaded into SGPRs when the wave starts, from which the kernel loads its arguments. Device-function calls are inlined aggressively. A real (non-inlined) call needs a stack in **scratch** (private) memory, which shows up as scratch usage in the compiler's resource report and in profiler counters. See [AMD GPU Architecture and Profiling](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md).

## 13.15 Stack Frames: Prologue, Epilogue, and Unwinding

Each active call owns a **frame** on the stack. The stack grows toward lower addresses. With frame pointers enabled, a System V x86-64 frame looks like this:

```text
 higher addresses
 ┌────────────────────────────────┐
 │  caller's frame ...            │
 │  stack argument 8              │  [rbp+24]
 │  stack argument 7              │  [rbp+16]   (caller's rsp was 16-byte aligned here, at the call)
 │  return address                │  [rbp+8]    pushed by "call"
 ├────────────────────────────────┤  ◄── CFA (canonical frame address) = rbp+16
 │  saved rbp of the caller       │  [rbp]      ◄── rbp points here: the frame-pointer chain
 │  saved callee-saved registers  │             (rbx, r12-r15 if this function uses them)
 │  stack canary                  │             (-fstack-protector*)
 │  locals, spill slots           │
 │  outgoing stack arguments      │
 │                                │  ◄── rsp (16-byte aligned before any call this function makes)
 ├────────────────────────────────┤
 │  red zone: 128 bytes           │  usable by a leaf function without moving rsp
 └────────────────────────────────┘
 lower addresses
```

### Prologue and Epilogue at `-O0`

```cpp
// frame.cpp -- g++ -O0 -fno-omit-frame-pointer -fstack-protector-strong -fcf-protection=none -masm=intel -S frame.cpp
int callee(int a, int b);

int caller(int x) {
    int local[4] = {x, x + 1, x + 2, x + 3};   // a local array, so -fstack-protector-strong adds a canary
    return callee(local[0], local[3]);
}
```

```text
caller(int):
        push    rbp                        ; prologue 1: save the caller's frame pointer
        .cfi_def_cfa_offset 16             ;   (CFI: CFA is now rsp+16)
        .cfi_offset 6, -16                 ;   (CFI: caller's rbp is saved at CFA-16)
        mov     rbp, rsp                   ; prologue 2: rbp = this frame's base
        .cfi_def_cfa_register 6            ;   (CFI: from here on, CFA = rbp+16)
        sub     rsp, 48                    ; prologue 3: reserve locals; 8 (ret) + 8 (rbp) + 48 keeps 16-alignment
        mov     DWORD PTR -36[rbp], edi    ; -O0 spills the argument to memory
        mov     rax, QWORD PTR fs:40       ; load the canary from the thread control block...
        mov     QWORD PTR -8[rbp], rax     ; ...and store it just below the saved rbp
        xor     eax, eax
        ...                                ; fill local[0..3] at -32..-20[rbp]
        mov     esi, edx                   ; arguments for callee go in esi, edi
        mov     edi, eax
        call    callee(int, int)@PLT
        mov     rdx, QWORD PTR -8[rbp]     ; epilogue: check the canary
        sub     rdx, QWORD PTR fs:40
        je      .L3
        call    __stack_chk_fail@PLT       ; overwritten canary: abort ("stack smashing detected")
.L3:
        leave                              ; = mov rsp, rbp ; pop rbp
        .cfi_def_cfa 7, 8                  ;   (CFI: CFA = rsp+8 again)
        ret                                ; pop the return address into rip
```

The canary value comes from the 16 random bytes the kernel passes in the auxiliary vector (`AT_RANDOM`). glibc copies it into the thread control block, which `fs` points at, so the check is one load and one compare per protected function. A linear buffer overflow that reaches the return address must overwrite the canary on the way there.

### What Changes at `-O2`

```cpp
// keep.cpp -- g++ -O2 -fcf-protection=none -masm=intel -S keep.cpp
int g(int);
int keep(int x) {
    int a = g(x);      // x is needed after the call, and edi is caller-saved...
    return a + x;      // ...so the compiler parks x in a callee-saved register (rbx)
}
```

```text
keep(int):
        push    rbx                ; save callee-saved rbx (this also re-aligns rsp to 16 for the call)
        .cfi_def_cfa_offset 16
        .cfi_offset 3, -16
        mov     ebx, edi           ; x survives the call in rbx
        call    g(int)@PLT
        add     eax, ebx
        pop     rbx                ; restore it for our caller
        .cfi_def_cfa_offset 8
        ret
```

Three things happened. (1) **No frame pointer.** GCC and Clang default to `-fomit-frame-pointer` at `-O1` and above on x86-64, which frees `rbp` as a 16th general register. Locals are addressed relative to `rsp`. (2) **Callee-saved register use.** `x` must survive the call, so the compiler saves `rbx` once and keeps `x` in it. If the value lived in a caller-saved register, it would need a spill and reload around every call. (3) **CFI instead of a frame chain.** The `.cfi_*` directives become the `.eh_frame` table. For any instruction address, it tells an unwinder how to compute the **CFA** (the value `rsp` had before the `call`) and where each saved register lives. The return address is always at `CFA - 8`. C++ exception unwinding, gdb, and `perf --call-graph dwarf` all work this way.

Two other `-O2` effects show up in debuggers and profilers:

- **Tail calls.** The body of `caller` above becomes `lea esi, 3[rdi]` followed by `jmp callee`. The call turns into a jump and `caller`'s frame is gone, so a backtrace from inside `callee` shows `caller`'s *parent* directly. `-fno-optimize-sibling-calls` disables this when you need complete stacks.
- **Red-zone locals.** A leaf function that needs a little stack does not move `rsp` at all:

```cpp
// leaf.cpp -- g++ -O2 -fno-stack-protector -fcf-protection=none -masm=intel -S leaf.cpp
int leaf(int x) {
    volatile int buf[4];                 // volatile forces real stores to memory
    for (int i = 0; i < 4; ++i) buf[i] = x + i;
    return buf[3];
}
```

```text
leaf(int):                                 ; default                 ; with -mno-red-zone
        lea     eax, 1[rdi]                ;                         ; sub  rsp, 24
        mov     DWORD PTR -24[rsp], edi    ; below rsp: red zone     ; mov  DWORD PTR [rsp], edi
        mov     DWORD PTR -20[rsp], eax    ;                         ; ...
        ...                                ;                         ; add  rsp, 24
        ret
```

### Walking the Frame-Pointer Chain by Hand

With frame pointers, `[rbp]` holds the caller's `rbp` and `[rbp+8]` holds the return address into the caller, so the frames form a linked list. This is the whole algorithm behind `perf record -g` and eBPF stack collection, and the reason a library built without frame pointers breaks the chain ([Debugging and Profiling Tools 2.2](../tools/Debugging_and_Profiling_Tools.md#22-frame-pointers-and-stack-unwinding)).

```cpp
// fpwalk.cpp -- walk the rbp chain by hand, the way perf/eBPF frame-pointer unwinding does.
// g++ -std=c++20 -O0 -fno-omit-frame-pointer -rdynamic fpwalk.cpp -o fpwalk && ./fpwalk | c++filt
#include <cstdio>
#include <cstring>
#include <dlfcn.h>     // dladdr (glibc: in libc since 2.34; older glibc needs -ldl)

struct Frame {             // what [rbp] points at after "push rbp; mov rbp, rsp"
    Frame* caller_rbp;     // [rbp + 0] saved rbp of the caller
    void*  return_addr;    // [rbp + 8] pushed by the caller's "call"
};

__attribute__((noinline)) void walk() {
    auto* f = static_cast<Frame*>(__builtin_frame_address(0));
    for (int depth = 0; f != nullptr && depth < 16; ++depth) {
        Dl_info info{};
        const char* name = (dladdr(f->return_addr, &info) && info.dli_sname) ? info.dli_sname : "??";
        std::printf("#%d  rbp=%p  ret=%p  in %s\n", depth, static_cast<void*>(f), f->return_addr, name);
        if (std::strcmp(name, "main") == 0) break;     // frames above main are libc's, often built without FP
        if (f->caller_rbp <= f) break;                  // the stack grows down: callers live at higher addresses
        f = f->caller_rbp;
    }
}

__attribute__((noinline)) void level2() { walk(); }
__attribute__((noinline)) void level1() { level2(); }

int main() { level1(); }
```

```text
$ ./fpwalk | c++filt
#0  rbp=0x7ffe61a26e10  ret=0x620f060f22b8  in level2()
#1  rbp=0x7ffe61a26e20  ret=0x620f060f22c8  in level1()
#2  rbp=0x7ffe61a26e30  ret=0x620f060f22d8  in main
$ g++ -std=c++20 -O2 -fno-omit-frame-pointer -rdynamic fpwalk.cpp -o fpwalk2 && ./fpwalk2
#0  rbp=0x7ffead7871f0  ret=0x57669b8f40cd  in main
```

Each frame is 16 bytes above the previous one, since these functions have no locals. At `-O2` the frames of `level1` and `level2` disappear even with frame pointers on: both calls are in tail position, so they became `jmp`s. `-rdynamic` exports the executable's symbols into `.dynsym` so that `dladdr` can name them.

### Stack Size and Overflow

| Fact | Value / mechanism |
|---|---|
| Main-thread stack limit | `ulimit -s` (`RLIMIT_STACK`), usually 8 MiB. The kernel grows the `[stack]` mapping on demand up to it. |
| glibc thread stacks | Fixed-size `mmap` regions. The default size is taken from `RLIMIT_STACK` (so 8 MiB typically). Set it per thread with `pthread_attr_setstacksize`. |
| musl (Alpine containers) | **128 KiB** default thread stack (80 KiB before musl 1.1.21). Deep recursion that works on glibc overflows on Alpine. Fix with `pthread_attr_setstacksize` or link with `-Wl,-z,stack-size=N`. |
| macOS | 8 MiB main thread, 512 KiB for secondary threads |
| Overflow detection | A **guard page** (`PROT_NONE`) below each thread stack, and a guard gap below the main stack (`stack_guard_gap`, 256 pages = 1 MiB since the 2017 Stack Clash fixes). Touching it raises `SIGSEGV`. |
| Large frames | A frame larger than the guard can jump *over* it into another mapping ("stack clash"). `-fstack-clash-protection` (default on several distros) probes every page of a large frame or `alloca`. |
| Finding big frames | `-fstack-usage` writes per-function `.su` files; `-Wframe-larger-than=N` and `-Wstack-usage=N` warn at compile time |

A stack overflow usually crashes in the *function prologue* (the `sub rsp, N` succeeds, and the first store into the new frame faults) or at a `call`, whose push faults. A `SIGSEGV` with a fault address just below a stack mapping is the signature. The handler for that `SIGSEGV` must run on an alternate stack (`sigaltstack`), because the normal one is exhausted.

> **See also:** [Debugging and Profiling Tools: Frame Pointers and Stack Unwinding](../tools/Debugging_and_Profiling_Tools.md#22-frame-pointers-and-stack-unwinding) · [Reading the kernel's segfault line](../tools/Debugging_and_Profiling_Tools.md#64-no-core-reading-the-kernels-segfault-line) · [14. Exception Handling](#14-exception-handling-and-error-management) (uses the same `.eh_frame` tables)

## 13.16 Process Virtual Address-Space Layout

[Section 3.1](#31-memory-layout-of-a-c-program) shows the textbook picture: text, data, BSS, heap, and stack. A real 64-bit Linux process has more regions, and most of them are placed at random by ASLR. On x86-64 with 4-level paging, user space gets the lower 47 bits of the address range (128 TiB, up to `0x00007fffffffffff`). The kernel lives in the upper half starting at `0xffff800000000000`. Everything in between is **non-canonical**, and touching it raises a general-protection fault, not a page fault.

```text
0xffffffffffffffff ┌──────────────────────────────────────────┐
                   │ kernel space (same mapping in every      │  not accessible from user mode
0xffff800000000000 │ process; [vsyscall] legacy page here)    │
                   ├──────────────────────────────────────────┤
                   │ non-canonical hole (~16 million TiB)     │  any access: #GP -> SIGSEGV
0x00007fffffffffff ├──────────────────────────────────────────┤
                   │ [stack] of the main thread               │  grows down; random base
                   │   argv/envp strings, auxv, argc at top   │
                   │ ··· random gap ···                       │
                   │ mmap area, allocated top-down:           │  ~0x7f..., random base
                   │   ld-linux-x86-64.so.2                   │
                   │   [vdso] + [vvar]                        │  kernel-provided, user-mode syscalls
                   │   libc.so.6, libstdc++.so.6, libm ...    │  r--p / r-xp / r--p (RELRO) / rw-p each
                   │   thread stacks (+ guard pages)          │
                   │   malloc arenas of other threads (64 MiB)│
                   │   large malloc blocks (>= 128 KiB)       │
                   │   file mappings, shared memory, GPU VA   │
                   │                 ▼                        │
                   │ ··· free ···                             │
                   │                 ▲                        │
                   │ [heap] (brk)                             │  grows up; random gap above .bss
                   │ .bss  (rw-p, zero pages)                 │
                   │ .data, .got (rw-p)                       │  executable (PIE): ~0x55..., random
                   │ .data.rel.ro, .got after RELRO (r--p)    │
                   │ .rodata, .eh_frame (r--p)                │
                   │ .text (r-xp)                             │
                   │ ELF headers (r--p)                       │
                   ├──────────────────────────────────────────┤
                   │ unmappable low region                    │  vm.mmap_min_addr (65536 on most distros),
0x0000000000000000 └──────────────────────────────────────────┘  so a null dereference always faults
```

### Seeing It on a Real Process

```cpp
// vmmap.cpp -- where does everything live? Compare the addresses with /proc/self/maps.
// g++ -std=c++20 -O0 -pthread vmmap.cpp -o vmmap && ./vmmap
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
#include <thread>
#include <sys/auxv.h>   // getauxval(AT_SYSINFO_EHDR): base address of the vDSO

int initialized_global = 42;       // .data
int zero_global;                   // .bss
const char* literal = "rocprof";   // the pointer is in .data; the characters are in .rodata
thread_local int tls_var = 1;      // .tdata: one copy per thread

static void show(const char* what, const void* p) { std::printf("%-28s %p\n", what, p); }

int main() {
    int on_stack = 0;
    void* small = std::malloc(64);           // below the mmap threshold: brk heap
    void* large = std::malloc(1 << 20);      // 1 MiB >= M_MMAP_THRESHOLD (128 KiB default): own mmap

    show("main (.text)", reinterpret_cast<const void*>(&main));
    show("string literal (.rodata)", literal);
    show("initialized_global (.data)", &initialized_global);
    show("zero_global (.bss)", &zero_global);
    show("malloc(64) (heap/brk)", small);
    show("malloc(1 MiB) (mmap)", large);
    show("printf (libc.so .text)", reinterpret_cast<const void*>(&std::printf));
    show("tls_var (main thread TLS)", &tls_var);
    std::thread([] { int t = 0; show("thread-stack local", &t); }).join();
    show("local (main stack)", &on_stack);
    show("vDSO (AT_SYSINFO_EHDR)", reinterpret_cast<const void*>(getauxval(AT_SYSINFO_EHDR)));

    std::ifstream maps("/proc/self/maps");
    for (std::string line; std::getline(maps, line);) std::cout << line << '\n';
    std::free(large);
    std::free(small);
}
```

Output on Linux 7.0 with glibc 2.43 and GCC 15.2, trimmed (libm, libstdc++, and libgcc_s mappings removed), with annotations added:

```text
main (.text)                 0x585ea115b3ff
string literal (.rodata)     0x585ea115d020
initialized_global (.data)   0x585ea115f010
zero_global (.bss)           0x585ea115f154
malloc(64) (heap/brk)        0x585ec66a6020
malloc(1 MiB) (mmap)         0x7ec1bbcff010
printf (libc.so .text)       0x7ec1bbe64080
tls_var (main thread TLS)    0x7ec1bc58877c
thread-stack local           0x7ec1bbcfdd54
local (main stack)           0x7ffcc45cfc04
vDSO (AT_SYSINFO_EHDR)       0x7ec1bc5ce000
585ea1159000-585ea115b000 r--p 00000000 00:24 3513340   /tmp/abi/vmmap     ELF headers, .dynsym, .rela
585ea115b000-585ea115d000 r-xp 00002000 00:24 3513340   /tmp/abi/vmmap     .text, .plt
585ea115d000-585ea115e000 r--p 00004000 00:24 3513340   /tmp/abi/vmmap     .rodata, .eh_frame
585ea115e000-585ea115f000 r--p 00005000 00:24 3513340   /tmp/abi/vmmap     RELRO: .data.rel.ro, .got
585ea115f000-585ea1160000 rw-p 00006000 00:24 3513340   /tmp/abi/vmmap     .data, .bss
585ec6694000-585ec66c7000 rw-p 00000000 00:00 0         [heap]             brk heap, random gap above .bss
7ec1b4000000-7ec1b4021000 rw-p 00000000 00:00 0                            2nd thread's malloc arena:
7ec1b4021000-7ec1b8000000 ---p 00000000 00:00 0                              64 MiB reserved, 132 KiB committed
7ec1bb4fe000-7ec1bbcff000 rw-p 00000000 00:00 0                            thread stack (8 MiB + guard page)
7ec1bbcff000-7ec1bbe00000 rw-p 00000000 00:00 0                            the 1 MiB malloc block
7ec1bbe00000-7ec1bbe28000 r--p 00000000 103:07 47856640 /usr/lib/x86_64-linux-gnu/libc.so.6
7ec1bbe28000-7ec1bbfc0000 r-xp 00028000 103:07 47856640 /usr/lib/x86_64-linux-gnu/libc.so.6
7ec1bbfc0000-7ec1bc00e000 r--p 001c0000 103:07 47856640 /usr/lib/x86_64-linux-gnu/libc.so.6
7ec1bc00e000-7ec1bc012000 r--p 0020e000 103:07 47856640 /usr/lib/x86_64-linux-gnu/libc.so.6
7ec1bc012000-7ec1bc014000 rw-p 00212000 103:07 47856640 /usr/lib/x86_64-linux-gnu/libc.so.6
7ec1bc588000-7ec1bc58d000 rw-p 00000000 00:00 0                            main thread's static TLS + TCB
7ec1bc5c8000-7ec1bc5cc000 r--p 00000000 00:00 0         [vvar]             kernel data the vDSO reads
7ec1bc5cc000-7ec1bc5ce000 r--p 00000000 00:00 0         [vvar_vclock]
7ec1bc5ce000-7ec1bc5d0000 r-xp 00000000 00:00 0         [vdso]
7ec1bc5d0000-7ec1bc5d1000 r--p 00000000 103:07 47856627 /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
...
7ffcc45b0000-7ffcc45d2000 rw-p 00000000 00:00 0         [stack]
ffffffffff600000-ffffffffff601000 --xp 00000000 00:00 0 [vsyscall]
```

How to read it:

- **Each ELF object appears as 4-5 mappings** with different permissions: the `PT_LOAD` segments from [13.6](#136-object-files-and-elf-sections). The `r--p` mapping just before `rw-p` is the RELRO region, which was writable while `ld.so` applied relocations and was then `mprotect`ed read-only ([13.8](#138-position-independent-code-the-pltgot-and-lazy-binding)). The fifth column is the file offset, which is how a profiler turns a sampled address into a file offset and then a symbol.
- **The heap is just one mapping.** `malloc(64)` came from the `brk` heap. `malloc(1 MiB)` got its own anonymous `mmap`, because it is above glibc's `M_MMAP_THRESHOLD`: 128 KiB initially, raised dynamically (up to 32 MiB on 64-bit) when such blocks are freed. When the new thread first called `malloc`, glibc created a separate **arena** for it: 64 MiB of address space reserved `---p`, with only the used part made `rw-p`. That is why VSZ jumps by 64 MiB for each new arena (glibc creates up to 8 per core, then threads share them), while RSS barely moves ([3.8](#38-production-allocators-tcmalloc-jemalloc-mimalloc)).
- **The mmap area has no fixed internal order.** Libraries, thread stacks, arenas, and large blocks are placed top-down into the first hole that fits, so their relative order changes with allocation order and from run to run. (In another run of this program the 1 MiB block landed above libc.)
- **Thread stacks are anonymous `mmap`s.** The new thread's 8 MiB stack is in the mmap area, near the libraries, not near `[stack]`. With glibc 2.42+ on Linux 6.13+, the guard page is installed with `madvise(MADV_GUARD_INSTALL)` instead of a separate `PROT_NONE` mapping, so it no longer appears as its own `---p` line: the stack and its guard show as one 8 MiB + 4 KiB `rw-p` region. Older systems show the extra `---p` line.
- **TLS.** On x86-64, `fs` points at the thread control block (TCB), and the static TLS block of each thread sits just below it ([12.13](#1213-once-only-init-lock-ordering-and-thread-local-storage)). For new threads the TCB and TLS live at the top of the thread's stack mapping. For the main thread `ld.so` allocates them separately, as here.
- **`[vdso]` and `[vvar]`.** The kernel maps a small ELF shared library (the virtual dynamic shared object) into every process, together with read-only kernel data pages. `clock_gettime`, `gettimeofday`, `time`, and `getcpu` run entirely in user mode by reading those pages, which takes tens of nanoseconds instead of a syscall's hundreds. That is why tracing timestamps are cheap. `[vsyscall]` is its fixed-address predecessor, kept only for very old binaries and now execute-only.
- **The top of `[stack]`** holds what `execve` set up: the argument and environment strings, the auxiliary vector (`AT_PHDR`, `AT_ENTRY`, `AT_RANDOM`, `AT_SYSINFO_EHDR`, ...), the `envp` and `argv` pointer arrays, and `argc` at the initial `rsp` that `_start` sees.

### ASLR

With `kernel.randomize_va_space = 2` (the default), the kernel randomizes the stack, the mmap base (and therefore every shared library and the vDSO), the `brk` heap start, and the load address of PIE executables. Exploits that need a known address must first leak one. Practical consequences for engineers:

- Raw addresses differ run to run, so profilers and crash reporters store **(module, offset)** pairs or build IDs, never absolute addresses.
- `gdb` disables ASLR for programs it starts (`set disable-randomization on`). That is why a PIE loads at `0x555555554000` under gdb, and why a bug that depends on addresses may vanish in the debugger. `setarch -R ./app` does the same outside gdb.
- A non-PIE executable (`-no-pie`) is linked at a fixed address (`0x400000` on x86-64). Only its libraries, heap, and stack move.

### Larger Address Spaces and GPUs

With 5-level paging (Intel LA57, AMD Zen 4 and later), virtual addresses grow to 57 bits (128 PiB for user space). Linux still hands out addresses below the 47-bit boundary unless the program passes a higher `mmap` hint, because some programs keep tags in the unused upper pointer bits.

On ROCm, host and device allocations share **one 64-bit virtual address space** (unified virtual addressing). Every `hipMalloc` pointer is a distinct process virtual address, so `hipPointerGetAttributes` can tell from the pointer alone whether it refers to host or device memory and on which GPU. The user-mode driver reserves large virtual ranges for GPU allocations, so a HIP process can report a very large VSZ that says nothing about real memory use. Look at RSS and the GPU memory counters instead. See [Parallel GPU Programming](../ml-gpu/Parallel_GPU_Programming.md) and [AMD GPU Architecture and Profiling](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md).

> **See also:** [CS Fundamentals: Linux Memory Management Internals](../computer-science/CS_Fundamentals.md#111-linux-memory-management-internals) (VMAs, lazy allocation, page cache) · [CS Fundamentals 1.9: fork, exec, and the process lifecycle](../computer-science/CS_Fundamentals.md#19-linux-process-lifecycle-signals-and-file-descriptors) · [Performance Engineering: TLB Effects and Huge Pages](../computer-science/Performance_Engineering.md#58-tlb-effects-and-huge-pages) · [Debugging and Profiling Tools: binutils and ELF inspection](../tools/Debugging_and_Profiling_Tools.md#13-binutils-and-elf-inspection)

## 13.17 Preprocessor

| Directive | Purpose | Example |
|---|---|---|
| `#include` | Insert file contents | `#include <vector>` / `#include "myfile.h"` |
| `#define` | Define macro | `#define MAX_SIZE 100` |
| `#undef` | Remove macro definition | `#undef MAX_SIZE` |
| `#ifdef` / `#ifndef` | Conditional on macro defined | `#ifdef DEBUG` |
| `#if` / `#elif` / `#else` / `#endif` | General conditional compilation | `#if VERSION >= 3` |
| `#pragma` | Implementation-defined directive | `#pragma once` |
| `#error` | Force compilation error | `#error "Not supported"` |
| `#line` | Change reported line number | `#line 100 "file.cpp"` |

**Macro pitfalls (prefer `constexpr`, `inline`, templates instead):**

```cpp
// BAD: macro has no type safety, no scope, double-evaluation bugs
#define SQUARE(x) ((x) * (x))
int a = 5;
SQUARE(a++);  // UB: ((a++) * (a++)) -- a incremented twice

// GOOD: constexpr function
constexpr int square(int x) { return x * x; }
```

## 13.18 Build Systems

### CMake (Industry Standard)

```cmake
cmake_minimum_required(VERSION 3.20)
project(MyProject LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(my_app
    src/main.cpp
    src/widget.cpp
)

target_include_directories(my_app PRIVATE include)
target_link_libraries(my_app PRIVATE pthread)

# Adding a library
add_library(mylib STATIC src/util.cpp)
target_link_libraries(my_app PRIVATE mylib)
```

```bash
mkdir build && cd build
cmake ..
cmake --build .
```

---

# 14. Exception Handling and Error Management

---

## 14.1 `try` / `catch` / `throw`

```cpp
#include <stdexcept>

double divide(double a, double b) {
    if (b == 0.0)
        throw std::invalid_argument("Division by zero");
    return a / b;
}

try {
    double result = divide(10.0, 0.0);
} catch (const std::invalid_argument& e) {
    std::cerr << "Error: " << e.what() << "\n";
} catch (const std::exception& e) {
    std::cerr << "General error: " << e.what() << "\n";
} catch (...) {
    std::cerr << "Unknown error\n";
}
```

**Rules:**
- Catch by `const` reference to avoid slicing
- Catch more specific exceptions first (derived before base)
- `catch(...)` catches everything (use as last resort)
- `throw;` (no operand) re-throws the current exception

## 14.2 Standard Exception Hierarchy

```
std::exception
├── std::logic_error
│   ├── std::invalid_argument
│   ├── std::domain_error
│   ├── std::length_error
│   ├── std::out_of_range
│   └── std::future_error
├── std::runtime_error
│   ├── std::range_error
│   ├── std::overflow_error
│   ├── std::underflow_error
│   └── std::system_error
├── std::bad_alloc          (from failed new)
├── std::bad_cast           (from failed dynamic_cast)
├── std::bad_typeid         (from typeid on null pointer)
└── std::bad_exception
```

| Category | When to Use |
|---|---|
| `logic_error` | Programmer error (violations of preconditions) |
| `runtime_error` | Errors detectable only at runtime (file not found, network down) |
| `bad_alloc` | Memory allocation failure |

### Custom Exception Classes

```cpp
class DatabaseError : public std::runtime_error {
    int error_code_;
public:
    DatabaseError(const std::string& msg, int code)
        : std::runtime_error(msg), error_code_(code) {}
    int code() const { return error_code_; }
};

throw DatabaseError("Connection refused", 1001);
```

## 14.3 Exception Safety Guarantees

Every function should provide one of these guarantees:

| Guarantee | Promise | Example |
|---|---|---|
| **No-throw** | Never throws; always succeeds | Destructors, `swap`, move operations |
| **Strong** | If exception thrown, state is unchanged (commit-or-rollback) | `std::vector::push_back` |
| **Basic** | If exception thrown, invariants preserved (no leaks, valid state) | Most STL operations |
| **No guarantee** | Anything can happen | Avoid this |

### Achieving Strong Guarantee: Copy-and-Swap

```cpp
class Widget {
    std::vector<int> data_;
public:
    Widget& operator=(Widget other) {   // copy made on the stack
        swap(*this, other);              // noexcept swap
        return *this;
    }   // if copy threw, *this is unchanged (strong guarantee)

    friend void swap(Widget& a, Widget& b) noexcept {
        using std::swap;
        swap(a.data_, b.data_);
    }
};
```

## 14.4 `noexcept`

### As a Specifier

Declares that a function does not throw. If it does throw, `std::terminate()` is called:

```cpp
void safe_operation() noexcept {
    // guaranteed not to throw (or program terminates)
}

// Conditional noexcept
template <typename T>
void swap_values(T& a, T& b) noexcept(noexcept(T(std::move(a)))) {
    // noexcept if T's move constructor is noexcept
}
```

### As an Operator

Tests whether an expression is `noexcept` at compile time:

```cpp
static_assert(noexcept(42 + 1));              // true: arithmetic is noexcept
static_assert(!noexcept(std::string("hi")));  // false: may allocate (throw)
```

**When to use `noexcept`:**
- Destructors (implicitly noexcept)
- Move constructors and move assignment operators
- `swap` functions
- Any function that logically cannot fail

## 14.5 RAII and Exception Safety

RAII ensures cleanup even when exceptions are thrown, because destructors run during stack unwinding:

```cpp
void process_file() {
    std::ifstream file("data.txt");         // RAII: file opened
    std::lock_guard lock(mutex);             // RAII: mutex locked
    auto ptr = std::make_unique<Widget>();   // RAII: memory managed

    might_throw();   // if this throws:
    // ~unique_ptr runs → deletes Widget
    // ~lock_guard runs → unlocks mutex
    // ~ifstream runs → closes file
}   // all resources cleaned up in reverse order of construction
```

## 14.6 Exceptions vs Error Codes

| Criterion | Exceptions | Error Codes / `std::expected` |
|---|---|---|
| Cannot be ignored | Propagate automatically | Can be silently discarded |
| Performance (happy path) | Near zero overhead | Zero overhead |
| Performance (error path) | Expensive (stack unwinding) | Cheap (just a branch) |
| Code clarity | Separates error handling from logic | Interspersed with logic |
| Composability | Stack unwinding handles nested calls | Must propagate manually |
| Binary size | Larger (exception tables) | Smaller |
| Deterministic timing | No (unwinding time varies) | Yes |
| Best for | Application code, rare errors | Libraries, hot paths, embedded/real-time |

```cpp
// C++23: std::expected -- combines return value with error info
#include <expected>

std::expected<double, std::string> safe_sqrt(double x) {
    if (x < 0) return std::unexpected("Negative input");
    return std::sqrt(x);
}

auto result = safe_sqrt(4.0);
if (result) {
    std::cout << *result;      // 2.0
} else {
    std::cout << result.error(); // "Negative input"
}
```

---

# 15. Undefined Behavior, Implementation-Defined, and Best Practices

---

## 15.1 Categories of Behavior

| Category | Definition | Example |
|---|---|---|
| **Defined** | Standard specifies exact behavior | `int x = 5 + 3;` → `x` is `8` |
| **Implementation-defined** | Compiler must document its choice | `sizeof(int)`: could be 2 or 4 |
| **Unspecified** | Multiple valid behaviors; compiler need not document | Order of argument evaluation (pre-C++17) |
| **Undefined (UB)** | No constraints -- anything can happen | Signed integer overflow, null dereference |

## 15.2 Common Sources of Undefined Behavior

| UB Category | Example | Why It's UB |
|---|---|---|
| **Signed integer overflow** | `INT_MAX + 1` | Wrapping is not guaranteed (unlike unsigned) |
| **Null pointer dereference** | `int* p = nullptr; *p;` | No valid object at address 0 |
| **Out-of-bounds access** | `int a[5]; a[10];` | Access beyond allocated memory |
| **Use-after-free** | `delete p; *p;` | Object's lifetime has ended |
| **Uninitialized read** | `int x; cout << x;` | Indeterminate value |
| **Data race** | Concurrent unsynchronized access | Conflicting operations without ordering |
| **Signed overflow in shift** | `1 << 33` (32-bit int) | Shift amount >= bit width |
| **Modifying a `const` object** | `const_cast` + write on true const | Object in read-only memory |
| **Infinite loop without side effects** | `while(true) {}` (no I/O, atomics) | Compiler may optimize it away |
| **ODR violation** | Different definitions of same entity | Linker picks one unpredictably |
| **Strict aliasing violation** | `float f; int i = *(int*)&f;` | Accessing object through wrong pointer type |

**The compiler is free to assume UB never happens** and optimize accordingly. This means UB can cause seemingly unrelated code to break.

## 15.3 Strict Aliasing Rule

You can only access an object through a pointer/reference to its actual type (or `char*`/`unsigned char*`/`std::byte*`):

```cpp
float f = 1.0f;

// WRONG: strict aliasing violation (UB)
int bits = *reinterpret_cast<int*>(&f);

// CORRECT: use memcpy (well-defined, typically optimized away)
int bits;
std::memcpy(&bits, &f, sizeof(bits));

// CORRECT (C++20): use std::bit_cast
int bits = std::bit_cast<int>(f);
```

## 15.4 Object Lifetime and Storage Duration

| Storage Duration | Keyword | Lifetime |
|---|---|---|
| **Automatic** | (local variables) | Block scope -- created on entry, destroyed on exit |
| **Static** | `static`, global | Program lifetime -- created before `main`, destroyed after |
| **Thread-local** | `thread_local` | Thread lifetime -- one instance per thread |
| **Dynamic** | `new` / `delete` | Manual -- from `new` until `delete` |

```cpp
int global = 0;                // static duration

void example() {
    int local = 1;              // automatic duration
    static int persistent = 2;  // static duration (survives function calls)
    thread_local int tl = 3;    // thread-local duration
    int* dyn = new int(4);      // dynamic duration
    delete dyn;
}
```

**Static initialization order fiasco:** the order of initialization of static variables across different translation units is undefined. Use the "construct on first use" idiom to avoid:

```cpp
// BAD: depends on init order of globals across TUs
// extern int global1;  // in file1.cpp
// int global2 = global1 + 1;  // in file2.cpp -- global1 may not be initialized yet

// GOOD: construct on first use
int& safe_global() {
    static int val = compute_initial_value();
    return val;  // guaranteed initialized on first call
}
```

## 15.5 `inline` Functions and Variables

`inline` originally hinted at inlining the function body. Today its primary effect is **relaxing the ODR**: an `inline` entity may be defined in multiple TUs (all definitions must be identical):

```cpp
// In a header -- OK because inline
inline int helper() { return 42; }

// C++17: inline variables
inline int global_config = 100;  // can be in a header without ODR violation

// All constexpr functions are implicitly inline
// All member functions defined inside the class body are implicitly inline
```

## 15.6 Namespaces and ADL

### Namespaces

```cpp
namespace graphics {
    namespace rendering {
        class Shader { /* ... */ };
    }
}

// C++17 nested namespace definition
namespace graphics::rendering {
    class Texture { /* ... */ };
}

// Anonymous namespace -- internal linkage (replaces static at file scope)
namespace {
    int internal_counter = 0;  // visible only in this TU
}

// using declarations
using graphics::rendering::Shader;     // single name
using namespace graphics::rendering;   // entire namespace (avoid in headers)
```

### Argument-Dependent Lookup (ADL / Koenig Lookup)

When calling an unqualified function, the compiler also searches the namespaces of the argument types:

```cpp
namespace math {
    struct Vec { double x, y; };
    Vec operator+(const Vec& a, const Vec& b) {
        return {a.x + b.x, a.y + b.y};
    }
}

math::Vec a{1, 2}, b{3, 4};
auto c = a + b;  // finds math::operator+ via ADL (a and b are in namespace math)
// No need to write math::operator+(a, b)
```

ADL is why `std::cout << x` works without `std::operator<<` -- the `std` namespace is searched because `cout` is in `std`.

## 15.7 `constexpr` vs `const` vs `#define`

| Feature | `#define` | `const` | `constexpr` |
|---|---|---|---|
| Type safety | No (textual substitution) | Yes | Yes |
| Scope | No (global macro) | Yes (follows scope rules) | Yes (follows scope rules) |
| Debuggable | No (replaced before compilation) | Yes | Yes |
| Evaluated when | Preprocessor | Compile or runtime | Compile time (if possible) |
| Usable in templates | No | Sometimes | Yes |
| Recommended | No | For runtime constants | For compile-time constants |

```cpp
// Prefer constexpr for compile-time constants
constexpr int MAX_SIZE = 1024;
constexpr double PI = 3.14159265358979;

// Use const for values determined at runtime that shouldn't change
const int screen_width = get_screen_width();

// Avoid #define for constants
// #define MAX_SIZE 1024  // no type, no scope, no debugger visibility
```

## 15.8 Evaluation Order (C++17)

Before C++17, the order of evaluation of function arguments was unspecified:

```cpp
int i = 0;
f(i++, i++);  // pre-C++17: UB (or at least unspecified order)

// C++17 guarantees:
// 1. Postfix expressions (a.b, a->b, a[b], a++) left-to-right
// 2. Assignment right-to-left
// 3. Shift operators left-to-right
// But function argument order is still unspecified!

// Safe version:
int a = i++;
int b = i++;
f(a, b);
```

---

## Common Interview Questions -- Compilation and Best Practices

**Q: What is undefined behavior and why is it dangerous?**

Undefined behavior (UB) means the C++ standard places no constraints on the program's behavior. The compiler is free to assume UB never occurs and optimize aggressively under that assumption. This means UB can cause crashes, produce wrong results, appear to work correctly in debug builds but fail in release, or even corrupt seemingly unrelated data. Common sources include signed overflow, null dereference, use-after-free, and data races.

**Q: What is the One Definition Rule?**

The ODR states that every entity (variable, function, class, template) must have exactly one definition in the entire program. Exceptions: `inline` functions/variables, template definitions, and class definitions may appear in multiple translation units but must be identical in all of them. Violating the ODR is undefined behavior, often manifesting as linker errors or subtle runtime bugs.

**Q: What is the difference between `#include <header>` and `#include "header"`?**

`<header>` searches implementation-defined system directories (standard library, installed libraries). `"header"` first searches the current file's directory (or project-specified paths), then falls back to system directories. Use `<>` for standard and third-party library headers; use `""` for your own project headers.

**Q: What is the static initialization order fiasco?**

Non-local static variables (globals, namespace-scope statics) in different translation units are initialized in an undefined order. If one static depends on another from a different TU, it may use an uninitialized value. The fix is the "construct on first use" idiom: wrap each static in a function that returns a reference to a local static variable, which is guaranteed to be initialized on first call (and is thread-safe in C++11+).

**Q: Why are macros discouraged in modern C++?**

Macros operate via textual substitution before compilation, so they bypass the type system, have no scope, are invisible to the debugger, can cause subtle bugs (double evaluation, unexpected operator precedence), and pollute the global namespace. Modern C++ provides type-safe, scoped alternatives for every common macro use case: `constexpr` for constants, `inline` functions for small functions, templates for generic code, and `enum class` for flag sets.

### Advanced Questions -- Linking, Loading, and ABI

**Q1.** Walk through what happens between typing `./app` and the first line of `main()` for a dynamically linked C++ program.

1. `execve`: the kernel reads the ELF header and program headers and maps the `PT_LOAD` segments (with ASLR for a PIE). It sees `PT_INTERP` (`/lib64/ld-linux-x86-64.so.2`), maps that too, and starts executing *the loader*, not the program.
2. `ld.so` reads `.dynamic`, then loads each `DT_NEEDED` library breadth-first: `LD_PRELOAD` libraries first, then each name located via RPATH, `LD_LIBRARY_PATH`, RUNPATH, `ld.so.cache`, and the default directories, each mapped with `mmap`.
3. Relocation: it fills GOT entries and data relocations, resolves symbols in global-scope order (interposition), applies copy relocations, and, with `BIND_NOW`, resolves every PLT slot now. RELRO pages are then made read-only.
4. Initialization: it runs `.init_array` of each library in dependency order (libstdc++ before your libraries). That covers static constructors, `__attribute__((constructor))`, and the iostreams init.
5. It jumps to the executable's entry `_start`, which calls `__libc_start_main`. That runs the executable's own `.init_array` (your globals' constructors) and then calls `main(argc, argv, envp)`. At exit, `atexit` handlers and `.fini_array` run in reverse order.

Debug any step with `LD_DEBUG=libs,bindings,reloc`, `strace -e openat,mmap`, and `readelf -l -d`.

**Q2.** What are the PLT and GOT, and why would you link with `-z now`?

The GOT is a per-process table of addresses in writable data that the dynamic loader fills in. Position-independent code reaches external functions and data indirectly through it, so the shared code pages never need patching. The PLT holds per-function stubs (`jmp *GOT[n]`). With lazy binding, the GOT entry first points at a resolver path, so the first call costs a symbol lookup in `_dl_runtime_resolve` and later calls cost one indirect jump. `-z now` (BIND_NOW) resolves everything at load. Benefits: missing symbols fail at startup instead of mid-run, there are no first-call latency spikes (they distort profiles and hurt tail latency), and combined with `-z relro` the whole GOT becomes read-only (full RELRO), which defeats GOT-overwrite exploits. The cost is slower startup for programs with thousands of imports they never call.

**Q3.** How would you count every `malloc` call in a binary you cannot recompile? What are the pitfalls?

Write a shared library that defines `malloc`/`free` (and `calloc`/`realloc`/`posix_memalign`/`aligned_alloc`/`memalign`), forwards to the real ones obtained with `dlsym(RTLD_NEXT, ...)`, and run with `LD_PRELOAD=./libspy.so ./app` ([13.10](#1310-symbol-interposition-and-ld_preload)). Pitfalls: (1) infinite recursion, because `dlsym`, `printf`, `new`, and lazy TLS can all call `malloc`; fix it with a static bootstrap buffer, a re-entrancy guard using initial-exec TLS, and `write(2)` for output. (2) Unwrapped variants make counts inconsistent, as with `free` > `malloc` in the Python run. (3) Thread safety: use atomics or per-thread counters. (4) Calls bound internally inside a library, static binaries, and setuid programs are not intercepted. (5) Reporting at exit must not depend on already-destroyed state. Alternatives: `ltrace -c -e malloc`, eBPF uprobes (`bpftrace -e 'uprobe:libc:malloc { @[ustack] = count(); }'`), heaptrack, or jemalloc stats.

**Q4.** How does a GPU profiler such as `rocprofv3` intercept HIP API calls without recompiling the application?

The ROCm runtimes are built for it. Every public HIP/HSA/ROCTx API function calls through a dispatch table of function pointers. At startup each runtime registers its table with rocprofiler-register, which detects a tool (a loaded library exporting `rocprofiler_configure`, or one named in `ROCP_TOOL_LIBRARIES`). rocprofiler-sdk then replaces table entries with wrappers that record timestamps, arguments, and correlation IDs, and call the saved originals. The kernel-dispatch and counter paths hook into HSA queue packet submission in a similar way. Compared with `LD_PRELOAD` wrappers, this catches calls the runtime makes internally, lets several tools chain, avoids depending on load order, and costs one extra indirect call. For legacy or third-party libraries without such tables, tools fall back to interposition, GOT patching, or binary instrumentation (Dyninst in rocprof-sys).

**Q5.** "undefined reference to `foo`" at link time vs "symbol lookup error: undefined symbol: foo" at run time. Causes and diagnosis?

Link time: the static linker found no definition. Check with `nm -C -A *.o *.a | grep foo`. Usual causes: the defining library is missing or comes *before* its user on the command line (archive order); the signature differs (const, namespace, parameter types, so the mangled name differs); `extern "C"` on one side only; the definition is a template not instantiated in any TU; it is hidden by `-fvisibility=hidden` without an export macro; or a dual-ABI mismatch (`std::__cxx11::basic_string` vs `std::string`). Run time: the binary linked against one version of a `.so` but loads another that lacks the symbol. Typical triggers are `LD_LIBRARY_PATH` pointing at an older ROCm, a stale copy in `ld.so.cache`, or an ABI break without a SONAME bump. Diagnose with `ldd`, `LD_DEBUG=libs,bindings`, `nm -D --defined-only /path/lib.so | grep foo`, and `readelf -V` for symbol versions.

**Q6.** Why build shared libraries with `-fvisibility=hidden`?

Five reasons. (1) A smaller dynamic symbol table, which loads and resolves faster. (2) The compiler may assume hidden functions are not interposed, so it can inline them and call them directly instead of through the PLT. (3) It prevents accidentally exporting internals that become de facto ABI. (4) It avoids symbol clashes when two libraries in one process contain different copies of the same dependency. (5) It makes the export list explicit and reviewable. Export the public API with a macro (`__attribute__((visibility("default")))`), and export whole classes whose `type_info` or vtable must be shared (exception types, polymorphic interfaces). The -O0 example above went from 93 exported symbols to 9 with `-fvisibility=hidden` plus `-fvisibility-inlines-hidden`. `-fvisibility=hidden` alone left 92, because the `std::` template instantiations inherit the default visibility that libstdc++ explicitly puts on `namespace std`.

**Q7.** RPATH vs RUNPATH, and what is `$ORIGIN`?

Both are search paths embedded in an ELF file's `.dynamic` section. `DT_RPATH` (legacy) is searched *before* `LD_LIBRARY_PATH` and applies to the whole dependency tree loaded on that object's behalf. `DT_RUNPATH` (the default with `--enable-new-dtags`) is searched *after* `LD_LIBRARY_PATH`, so users can override it, and applies only to the object's own direct dependencies. `$ORIGIN` expands at load time to the directory containing the object, so `-Wl,-rpath,'$ORIGIN/../lib'` makes a relocatable install tree such as `/opt/rocm-x.y`. Classic bug: the app's RUNPATH finds `liba.so`, but `liba.so` has no RUNPATH of its own and cannot find its sibling `libb.so`.

**Q8.** You maintain `libprof.so`, consumed as a binary by other teams. Which changes require a SONAME bump?

Any ABI break: adding, removing, or reordering data members of a public class (or changing their types); adding or reordering virtual functions; changing base classes; changing the signature or return type of an exported function; changing inline functions or templates whose old code is compiled into clients in an incompatible way; changing the size of an exported variable (copy relocations); and changing enum values or underlying types used in the API. These are safe without a bump: new free functions, new classes, new non-virtual members, and implementation-only changes behind pImpl. Enforce it with `abidiff` in CI against the last release, and design the API so most changes stay compatible: pImpl, a C API with opaque handles, size-prefixed structs, and symbol versioning.

**Q9.** What is `_GLIBCXX_USE_CXX11_ABI`, and how does a mismatch show up?

GCC 5's libstdc++ contains two versions of `std::string` and `std::list`: the pre-C++11 ones (copy-on-write string, O(n) `list::size`) and the C++11-conforming ones in inline namespace `std::__cxx11`. The macro selects which one your code uses (default 1 = new). Because the namespace is part of the mangled name, mixing code compiled with different settings gives link errors mentioning `std::__cxx11::basic_string` on one side and `std::string` (`Ss` in the mangling) on the other. A struct containing a `std::string` passed between them would silently have a different layout. Typical source: linking against prebuilt binaries built with `=0`, as with older PyTorch/libtorch wheels or RHEL 7 devtoolset toolchains. Fix: compile everything with the same value.

**Q10.** Two plugins loaded into one process each statically link a different version of LLVM (or protobuf). It crashes in odd places. Why, and how do you fix it?

Both `.so`s export the same global symbols (default visibility). The dynamic loader binds every reference to the *first* definition in the global scope, so plugin B's code calls plugin A's copy of some functions while using its own copy of others. Mismatched data layouts and duplicated singletons follow, which is an ODR violation across libraries. Fixes, roughly in order: build each plugin with `-fvisibility=hidden` and `-Wl,--exclude-libs,ALL` so the embedded copy is not exported; load plugins with `RTLD_LOCAL` (the default); use `-Wl,-Bsymbolic` so each library binds its own references internally; use symbol versioning or distinct namespaces for the bundled dependency; and as a last resort use `RTLD_DEEPBIND` or `dlmopen` (separate link-map namespaces). The cleanest fix is to share one copy of the dependency as its own shared library.

**Q11.** What runs first: a global constructor in your executable or one in a shared library it links? What can go wrong?

The shared libraries' constructors run first, in dependency order (a library's dependencies before it), because `ld.so` initializes all initially loaded objects before transferring control to the executable, whose own constructors run from `__libc_start_main`. A library constructor that registers itself into a registry *defined in the executable*, or uses a global from another unrelated library, may touch an object that has not been constructed yet. That is the cross-library static initialization order fiasco. Use function-local statics (construct on first use), explicit `init()` calls, or a registry owned by the lowest-level library. Destruction runs in reverse at exit, so a library's destructor must not use objects owned by its dependents.

**Q12.** What is a weak symbol, and give one legitimate use and one pitfall.

A weak *definition* is used only if no strong definition exists at static link time. A weak *undefined reference* resolves to null instead of failing the link. Legitimate use: a library ships a default `on_kernel_complete` hook marked weak, and applications override it by defining a strong one. A test framework can likewise provide a default `main`. Pitfalls: at *run time* the dynamic loader takes the first definition in search order regardless of weakness, so weak/strong overriding does not work across `.so` boundaries. A weak undefined reference does not pull members out of static archives, so the hook silently stays null. And calling a weak undefined function without checking `if (&fn)` jumps to address 0.

### Advanced Questions -- Calling Conventions, Stack Frames, and the Address Space

**Q13.** On Linux x86-64, where do the arguments of `double f(int a, double b, long c, Big d, float e)` go, where `Big` is a 24-byte struct of `long`s, and where does the result come back?

`a` goes in `edi` (1st integer register), `b` in `xmm0` (1st FP register), `c` in `rsi` (2nd integer register; integer and FP registers are counted separately). `d` is larger than 16 bytes, so it is MEMORY class and is copied into the caller's outgoing-argument area on the stack. `e` goes in `xmm1`. The result returns in `xmm0`. If `f` returned `Big`, the caller would pass a hidden result pointer in `rdi` (shifting `a` to `esi` and `c` to `rdx`), and `f` would return that pointer in `rax`. Follow-up: for a member function, `this` takes `rdi` first. For a 16-byte struct like `{long; double;}` the halves are classified separately and go in one integer and one SSE register ([13.14](#1314-calling-conventions-and-the-system-v-x86-64-abi)).

**Q14.** What is the difference between caller-saved and callee-saved registers, and how does it show up in generated code?

A call may freely overwrite caller-saved registers (`rax`, `rcx`, `rdx`, `rsi`, `rdi`, `r8`-`r11`, all vector registers), so a caller that needs a value in one of them after the call must spill it first. A function that uses a callee-saved register (`rbx`, `rbp`, `r12`-`r15`) must restore it before returning, which is the `push rbx` / `pop rbx` pair in the prologue and epilogue. Compilers put values that live across calls into callee-saved registers. The function then pays one save and restore in total instead of one spill and reload per call, which matters in a loop that calls a function each iteration. Corollary: a call to an opaque function destroys every vector register, so a vectorized loop that calls a non-inlined function per element spills its whole vector state. That is one reason inlining matters so much for SIMD code.

**Q15.** What is the red zone? Why does the Linux kernel compile with `-mno-red-zone`?

It is the 128 bytes below `rsp` that the System V ABI promises asynchronous events will not touch. A leaf function can store locals there without the `sub rsp`/`add rsp` pair. For user-space signals the kernel honors it by building the signal frame at least 128 bytes below `rsp`. Inside the kernel, a hardware interrupt arriving in kernel mode pushes its frame onto the current stack immediately below `rsp`, without skipping anything, so it would corrupt any red-zone data. The kernel therefore disables the red zone. The same applies to any code that can be interrupted without a stack switch (bare-metal code, some JIT trampolines). Windows x64 has no red zone at all.

**Q16.** Why can passing `std::unique_ptr<T>` by value be slower than passing `T*`, even though both are 8 bytes?

The Itanium C++ ABI treats a class with a non-trivial copy/move constructor or destructor as "non-trivial for the purposes of calls". Such an object must have a real address, so it cannot travel in a register. The caller materializes a temporary on its stack, passes its *address* in `rdi`, and the callee loads the pointer through it: one extra store and load. The caller also owns the temporary's destruction after the call, so it emits a null check, a `delete` path, and exception-cleanup code at every call site, even when the callee has already moved the pointer out. A raw pointer or `std::string_view` (trivially copyable) goes in registers. Remedies: pass `T*`/`T&` when no ownership transfer is intended, accept the cost when it is (it is small), or with Clang mark your own types `[[clang::trivial_abi]]`. You cannot fix `std::unique_ptr` itself without an ABI break, which is why libstdc++ has not done so.

**Q17.** Walk through a function prologue and epilogue. What does `-fomit-frame-pointer` change, and how do debuggers unwind without frame pointers?

With frame pointers: `push rbp` saves the caller's frame pointer, `mov rbp, rsp` establishes this frame's base, `push` of any callee-saved registers it uses, then `sub rsp, N` reserves locals, keeping `rsp` 16-byte aligned for calls. The epilogue reverses it: restore the callee-saved registers, `leave` (`mov rsp, rbp; pop rbp`), `ret`. Each frame then stores the caller's `rbp` at `[rbp]` and the return address at `[rbp+8]`, which forms a linked list that profilers can walk cheaply ([13.15](#1315-stack-frames-prologue-epilogue-and-unwinding)). `-fomit-frame-pointer`, the default at `-O1` and above on x86-64, drops the `rbp` setup, addresses locals relative to `rsp`, and uses `rbp` as a general register. Unwinding then relies on DWARF Call Frame Information (`.eh_frame`), generated from the `.cfi_*` directives. For each PC it says how to compute the CFA and where saved registers and the return address are. gdb, C++ exceptions, and `perf --call-graph dwarf` interpret these tables. The kernel cannot afford that at sample time, which is why frame-pointer builds matter for whole-system profiling.

**Q18.** Draw the virtual address space of a 64-bit Linux process. Where does each of these live: a global `int g = 1;`, a `static int z;`, a string literal, `new int[10]`, `new char[1 << 20]`, a local variable in a worker thread, and `printf`?

From low to high ([13.16](#1316-process-virtual-address-space-layout)): an unmapped region at 0 (null dereferences fault), then the PIE executable at a random `0x55...` base (headers, `.text` r-x, `.rodata` r--, RELRO r--, `.data`/`.bss` rw-), then the `brk` heap after a random gap, then a huge free gap, then the mmap area growing down from below the stack (shared libraries, `ld.so`, the vDSO, thread stacks, large malloc blocks, file mappings), then the main thread's stack at `0x7ffc...`, and the kernel half above the non-canonical hole. Answers: `g` in `.data`; `z` in `.bss`; the literal in `.rodata`; `new int[10]` from the `brk` heap (or a thread's arena); `new char[1 << 20]` from its own anonymous mmap (above the 128 KiB threshold); the thread's local in that thread's stack, an anonymous mmap near the libraries; and `printf` in libc's `r-xp` mapping. Follow-ups: ASLR randomizes each region's base, and `/proc/<pid>/maps` shows all of it.

**Q19.** What is the vDSO, and why does it matter for a profiler or tracer?

It is a small shared library that the kernel maps into every process (`[vdso]`, with the data pages in `[vvar]`) and announces through the auxiliary vector (`AT_SYSINFO_EHDR`). glibc routes `clock_gettime`, `gettimeofday`, `time`, and `getcpu` through it. These read kernel-maintained data from `[vvar]` and the TSC directly in user mode, so a call costs on the order of 20 ns instead of a real syscall's entry and exit. An API tracer that takes two timestamps per intercepted call depends on that being cheap. Pitfalls: if the kernel's clocksource is not the TSC (some VMs fall back to `hpet` or `acpi_pm`), vDSO calls silently become syscalls and timestamping gets 10x or more slower. Under `seccomp` or `strace`, vDSO calls do not show up, because they are not syscalls.

**Q20.** A recursive tree walk works on your workstation but crashes with `SIGSEGV` in a worker thread inside an Alpine-based container. What is going on?

Almost certainly stack overflow. On glibc, thread stacks default to `RLIMIT_STACK`, typically 8 MiB. musl, the C library of Alpine, defaults to **128 KiB**, 64 times less, so recursion depth or large local arrays that fit on glibc overflow on musl. The thread runs into its guard page and gets `SIGSEGV`, with a fault address just below the stack mapping. Fixes: give the thread an explicit stack size (`pthread_attr_setstacksize`; `std::thread` has no portable way, so use `pthread` attributes or a library thread type that accepts a size; Boost.Thread and Rust's `std::thread::Builder` do), raise musl's default at link time with `-Wl,-z,stack-size=N`, or turn the recursion into iteration with an explicit stack. Confirm with gdb (the backtrace shows thousands of identical frames) or by checking the fault address against `/proc/<pid>/maps`. The main thread is less affected, because its stack grows on demand up to `ulimit -s` on both libcs.

**Q21.** How does a userspace program make a Linux system call on x86-64, and how does that differ from a function call?

It puts the syscall number in `rax` and up to six arguments in `rdi`, `rsi`, `rdx`, `r10`, `r8`, `r9`, then executes `syscall`. The instruction switches to kernel mode at the address in the `LSTAR` MSR, saving the user `rip` in `rcx` and `rflags` in `r11`. That is why the 4th argument uses `r10` instead of `rcx`. The kernel returns the result in `rax`, with values from -4095 to -1 meaning `-errno`. The glibc wrapper stores `errno` and returns -1. Unlike a function call, nothing is pushed on the user stack, every register other than `rax`, `rcx`, and `r11` is preserved, and the cost is the privilege transition plus mitigations (on the order of 100 ns or more), compared with about 1 ns for a call. See [CS Fundamentals: System Calls](../computer-science/CS_Fundamentals.md#17-system-calls).

---

# Part 7: Practice

---

# 16. Implement-from-scratch Exercises

"Implement `X` from scratch" is a staple of systems C++ interviews. It tests ownership, exception safety, move semantics, and templates in one question, and the follow-ups ("make it thread-safe", "what if the copy throws?") probe depth. Each solution below is a **complete program with tests**. All of them compile cleanly with `g++ -std=c++20 -Wall -Wextra` and pass under `-fsanitize=address,undefined` (and `-fsanitize=thread` where threads are involved).

| # | Exercise | Core concepts tested | Typical time |
|---|---|---|---|
| [16.1](#161-uniqueptrt-exclusive-ownership) | `UniquePtr<T, D>` | Move-only types, `release`/`reset` ordering, `[[no_unique_address]]` deleter, converting moves | 15 to 20 min |
| [16.2](#162-sharedptrt-and-weakptrt-control-block-and-atomic-reference-counts) | `SharedPtr<T>` + `WeakPtr<T>` | Control block, atomic refcounts and memory orders, `lock()` CAS loop, `make_shared` single allocation | 30 to 45 min |
| [16.3](#163-vectort-placement-new-growth-and-the-strong-guarantee) | `Vector<T>` | Raw storage + placement new, growth, `move_if_noexcept`, strong guarantee, aliasing | 30 to 45 min |
| [16.4](#164-string-the-rule-of-five) | `String` | Rule of Five, copy-and-swap, self-assignment, self-append | 20 min |
| [16.5](#165-boundedqueuet-thread-safe-blocking-queue) | `BoundedQueue<T>` | Mutex + two condition variables, predicates, shutdown | 20 to 30 min |
| [16.6](#166-functionsig-type-erasure-with-small-buffer-optimization) | `Function<R(Args...)>` | Type erasure via a hand-made vtable, small-buffer optimization | 30 to 45 min |
| [16.7](#167-any-type-erasure-with-a-virtual-holder) | `Any` | OO type erasure, `clone()`, `typeid`-checked casts | 15 min |

How to practice: write each one from a blank file with a 30-minute timer, then compile with sanitizers and run the tests below. Say the invariants aloud as you go ("`weak_` counts the weak owners plus one for all strong owners together").

## 16.1 `UniquePtr<T>`: Exclusive Ownership

What the interviewer checks: copy deleted, move transfers and nulls the source, `reset` updates the pointer *before* deleting (re-entrancy), self-move safety, `UniquePtr<Derived>` → `UniquePtr<Base>`, and zero size overhead for a stateless deleter.

```cpp
// unique_ptr.cpp -- g++ -std=c++20 -Wall -Wextra -fsanitize=address,undefined unique_ptr.cpp
#include <cassert>
#include <cstdio>
#include <type_traits>
#include <utility>

template <class T>
struct DefaultDelete {
    DefaultDelete() = default;
    template <class U, class = std::enable_if_t<std::is_convertible_v<U*, T*>>>
    DefaultDelete(const DefaultDelete<U>&) noexcept {}          // Derived deleter -> Base deleter
    void operator()(T* p) const noexcept {
        static_assert(sizeof(T) > 0, "cannot delete an incomplete type");
        delete p;
    }
};

template <class T, class D = DefaultDelete<T>>
class UniquePtr {
public:
    using pointer = T*;
    using element_type = T;
    using deleter_type = D;

    constexpr UniquePtr() noexcept = default;
    constexpr UniquePtr(std::nullptr_t) noexcept {}
    explicit UniquePtr(T* p) noexcept : ptr_(p) {}
    UniquePtr(T* p, D d) noexcept : ptr_(p), del_(std::move(d)) {}

    UniquePtr(const UniquePtr&) = delete;                        // exclusive ownership
    UniquePtr& operator=(const UniquePtr&) = delete;

    UniquePtr(UniquePtr&& o) noexcept : ptr_(o.release()), del_(std::move(o.del_)) {}

    template <class U, class E,                                  // UniquePtr<Derived> -> UniquePtr<Base>
              class = std::enable_if_t<std::is_convertible_v<U*, T*> && std::is_convertible_v<E, D>>>
    UniquePtr(UniquePtr<U, E>&& o) noexcept : ptr_(o.release()), del_(std::move(o.get_deleter())) {}

    UniquePtr& operator=(UniquePtr&& o) noexcept {
        reset(o.release());                                      // self-move safe: release first
        del_ = std::move(o.del_);
        return *this;
    }
    UniquePtr& operator=(std::nullptr_t) noexcept { reset(); return *this; }

    ~UniquePtr() { reset(); }

    T* release() noexcept { return std::exchange(ptr_, nullptr); }
    void reset(T* p = nullptr) noexcept {
        T* old = std::exchange(ptr_, p);    // update state BEFORE calling the deleter:
        if (old) del_(old);                 // the deleter may (indirectly) touch *this
    }
    void swap(UniquePtr& o) noexcept { std::swap(ptr_, o.ptr_); std::swap(del_, o.del_); }

    T* get() const noexcept { return ptr_; }
    D& get_deleter() noexcept { return del_; }
    T& operator*() const noexcept { return *ptr_; }
    T* operator->() const noexcept { return ptr_; }
    explicit operator bool() const noexcept { return ptr_ != nullptr; }

private:
    T* ptr_ = nullptr;
    [[no_unique_address]] D del_{};         // stateless deleter costs 0 bytes (EBO for members)
};

template <class T, class... Args>
UniquePtr<T> make_unique_ptr(Args&&... args) {
    return UniquePtr<T>(new T(std::forward<Args>(args)...));
}

// ---------------- tests ----------------
struct Base { virtual ~Base() = default; virtual int id() const { return 1; } };
struct Derived : Base {
    static inline int alive = 0;
    Derived() { ++alive; }
    ~Derived() override { --alive; }
    int id() const override { return 2; }
};
struct FileCloser {                          // stateful deleter -> UniquePtr grows to 16 bytes
    int* closes;
    void operator()(int* p) const { ++*closes; delete p; }
};

int main() {
    static_assert(sizeof(UniquePtr<int>) == sizeof(int*), "zero overhead with a stateless deleter");
    static_assert(!std::is_copy_constructible_v<UniquePtr<int>>);
    static_assert(std::is_nothrow_move_constructible_v<UniquePtr<int>>);

    {
        UniquePtr<Base> b = make_unique_ptr<Derived>();      // converting move
        assert(b->id() == 2 && Derived::alive == 1);
        UniquePtr<Base> c = std::move(b);
        assert(!b && c && Derived::alive == 1);
        UniquePtr<Base>& alias = c;
        c = std::move(alias);                                // self-move: must not delete
        assert(c && Derived::alive == 1);
        c.reset();
        assert(Derived::alive == 0);
    }
    int closes = 0;
    {
        UniquePtr<int, FileCloser> f(new int(7), FileCloser{&closes});
        static_assert(sizeof(f) == 2 * sizeof(void*));
        int* raw = f.release();                              // caller now owns it
        f.reset(raw);
    }
    assert(closes == 1);
    std::puts("unique_ptr: all tests passed");
}
```

Follow-ups: **Why does `UniquePtr<Base>` delete a `Derived` correctly?** Only because `Base` has a virtual destructor. `std::unique_ptr` has the same requirement, unlike `shared_ptr`, whose deleter captures the original type. **Array form**: `unique_ptr<T[]>` uses `delete[]`, adds `operator[]`, and deliberately *forbids* `Derived[]` → `Base[]` conversion, because pointer arithmetic on the base type would be wrong. **Why `make_unique`?** Before C++17, `f(unique_ptr<A>(new A), g())` could leak if `g()` threw between `new A` and the constructor. C++17's sequencing rules fixed that, but `make_unique` is still shorter and never mentions `new`. **Incomplete types (pImpl)**: the `static_assert(sizeof(T) > 0)` forces the destructor to be instantiated where `T` is complete. That is why a pImpl class must declare its destructor in the header and define it (`= default`) in the `.cpp`.

## 16.2 `SharedPtr<T>` and `WeakPtr<T>`: Control Block and Atomic Reference Counts

What the interviewer checks: a separate control block with **strong** and **weak** counts; the object is destroyed at strong == 0 while the block survives until weak == 0; increments may be `relaxed` but the final decrement needs acquire/release; `lock()` must never resurrect a dead object (a CAS loop, not `fetch_add`); `make_shared` does one allocation; the deleter is type-erased.

```text
SharedPtr<T> { T* ptr; ControlBlock* cb; }        make_shared: one allocation
                         │                         ┌───────────────────────────────┐
                         └───────────────────────► │ vptr │ strong │ weak │ T obj  │
                                                   └───────────────────────────────┘
SharedPtr<T>(new T): two allocations   ┌──────────────────────────────────┐    ┌───────┐
                                       │ vptr │ strong │ weak │ T* │ del │───►│ T obj │
                                       └──────────────────────────────────┘    └───────┘
```

```cpp
// shared_ptr.cpp -- g++ -std=c++20 -Wall -Wextra -O2 -fsanitize=thread shared_ptr.cpp   (or address,undefined)
#include <atomic>
#include <cassert>
#include <cstdio>
#include <new>
#include <thread>
#include <type_traits>
#include <utility>
#include <vector>

// Control block. Invariant: weak_ = (#WeakPtr) + (strong_ > 0 ? 1 : 0).
// The "+1" held collectively by the strong owners means the block is freed by
// whoever drops weak_ to zero -- no separate "is anyone still looking" check.
class ControlBlock {
public:
    void add_strong() noexcept { strong_.fetch_add(1, std::memory_order_relaxed); }
    void add_weak() noexcept { weak_.fetch_add(1, std::memory_order_relaxed); }

    void release_strong() noexcept {
        // acq_rel: release publishes our writes to the object; acquire (on the
        // thread that hits zero) makes every other owner's writes visible before ~T.
        if (strong_.fetch_sub(1, std::memory_order_acq_rel) == 1) {
            dispose();          // destroy the managed object
            release_weak();     // drop the strong owners' collective weak reference
        }
    }
    void release_weak() noexcept {
        if (weak_.fetch_sub(1, std::memory_order_acq_rel) == 1) destroy();   // free the block
    }
    // weak_ptr::lock(): increment strong ONLY if it is not already zero.
    bool try_add_strong() noexcept {
        long n = strong_.load(std::memory_order_relaxed);
        while (n != 0) {
            if (strong_.compare_exchange_weak(n, n + 1, std::memory_order_acq_rel,
                                              std::memory_order_relaxed))
                return true;    // on failure n is reloaded; spurious failure just retries
        }
        return false;
    }
    long use_count() const noexcept { return strong_.load(std::memory_order_relaxed); }

protected:
    virtual ~ControlBlock() = default;
private:
    virtual void dispose() noexcept = 0;   // ~T (and free T if separately allocated)
    virtual void destroy() noexcept = 0;   // free the control block itself
    std::atomic<long> strong_{1};
    std::atomic<long> weak_{1};
};

// SharedPtr<T>(new T): object and block are two allocations. The deleter is
// type-erased inside the block, so SharedPtr<T>'s type does not depend on it.
template <class T, class D>
class PtrBlock final : public ControlBlock {
public:
    PtrBlock(T* p, D d) : p_(p), d_(std::move(d)) {}
private:
    void dispose() noexcept override { d_(p_); }
    void destroy() noexcept override { delete this; }
    T* p_;
    D d_;
};

// make_shared: ONE allocation holding block + object. Object storage is raw bytes,
// so dispose() can run ~T while the memory stays alive for outstanding weak_ptrs.
template <class T>
class InplaceBlock final : public ControlBlock {
public:
    template <class... Args>
    explicit InplaceBlock(Args&&... args) { ::new (static_cast<void*>(buf_)) T(std::forward<Args>(args)...); }
    T* get() noexcept { return std::launder(reinterpret_cast<T*>(buf_)); }
private:
    void dispose() noexcept override { get()->~T(); }
    void destroy() noexcept override { delete this; }
    alignas(T) unsigned char buf_[sizeof(T)];
};

template <class T> class WeakPtr;

template <class T>
class SharedPtr {
public:
    SharedPtr() noexcept = default;
    explicit SharedPtr(T* p) : SharedPtr(p, [](T* q) { delete q; }) {}
    template <class D>
    SharedPtr(T* p, D d) : ptr_(p) {
        try { cb_ = new PtrBlock<T, D>(p, d); }
        catch (...) { d(p); throw; }               // no leak if the block allocation throws
    }
    SharedPtr(const SharedPtr& o) noexcept : ptr_(o.ptr_), cb_(o.cb_) { if (cb_) cb_->add_strong(); }
    SharedPtr(SharedPtr&& o) noexcept : ptr_(std::exchange(o.ptr_, nullptr)), cb_(std::exchange(o.cb_, nullptr)) {}
    template <class U, class = std::enable_if_t<std::is_convertible_v<U*, T*>>>
    SharedPtr(const SharedPtr<U>& o) noexcept : ptr_(o.ptr_), cb_(o.cb_) { if (cb_) cb_->add_strong(); }

    SharedPtr& operator=(SharedPtr o) noexcept { swap(o); return *this; }   // copy/move-and-swap
    ~SharedPtr() { if (cb_) cb_->release_strong(); }

    void swap(SharedPtr& o) noexcept { std::swap(ptr_, o.ptr_); std::swap(cb_, o.cb_); }
    void reset() noexcept { SharedPtr().swap(*this); }
    T* get() const noexcept { return ptr_; }
    T& operator*() const noexcept { return *ptr_; }
    T* operator->() const noexcept { return ptr_; }
    long use_count() const noexcept { return cb_ ? cb_->use_count() : 0; }
    explicit operator bool() const noexcept { return ptr_ != nullptr; }

private:
    template <class U> friend class SharedPtr;
    template <class U> friend class WeakPtr;
    template <class U, class... Args> friend SharedPtr<U> make_shared_ptr(Args&&...);
    struct Adopt {};                                                    // tag: avoid overload clash
    SharedPtr(Adopt, T* p, ControlBlock* cb) noexcept : ptr_(p), cb_(cb) {}   // adopts one strong ref

    T* ptr_ = nullptr;           // may differ from the block's pointer (base subobject)
    ControlBlock* cb_ = nullptr;
};

template <class T, class... Args>
SharedPtr<T> make_shared_ptr(Args&&... args) {
    auto* blk = new InplaceBlock<T>(std::forward<Args>(args)...);
    return SharedPtr<T>(typename SharedPtr<T>::Adopt{}, blk->get(), blk);
}

template <class T>
class WeakPtr {
public:
    WeakPtr() noexcept = default;
    WeakPtr(const SharedPtr<T>& s) noexcept : ptr_(s.ptr_), cb_(s.cb_) { if (cb_) cb_->add_weak(); }
    WeakPtr(const WeakPtr& o) noexcept : ptr_(o.ptr_), cb_(o.cb_) { if (cb_) cb_->add_weak(); }
    WeakPtr& operator=(WeakPtr o) noexcept { std::swap(ptr_, o.ptr_); std::swap(cb_, o.cb_); return *this; }
    ~WeakPtr() { if (cb_) cb_->release_weak(); }

    SharedPtr<T> lock() const noexcept {
        if (cb_ && cb_->try_add_strong()) return SharedPtr<T>(typename SharedPtr<T>::Adopt{}, ptr_, cb_);
        return {};
    }
    bool expired() const noexcept { return !cb_ || cb_->use_count() == 0; }

private:
    T* ptr_ = nullptr;           // never dereferenced without a successful lock()
    ControlBlock* cb_ = nullptr;
};

// ---------------- tests ----------------
struct Tracked {
    static inline std::atomic<int> alive{0};
    int value;
    explicit Tracked(int v) : value(v) { ++alive; }
    ~Tracked() { --alive; }
};
struct Node {                     // cycle broken by a weak back-pointer
    SharedPtr<Node> next;
    WeakPtr<Node> prev;
};

int main() {
    {
        auto a = make_shared_ptr<Tracked>(1);
        WeakPtr<Tracked> w = a;
        {
            SharedPtr<Tracked> b = a;
            assert(a.use_count() == 2);
            SharedPtr<const Tracked> ro = b;           // converting copy (T* -> const T*)
            assert(ro->value == 1 && a.use_count() == 3);
        }
        assert(a.use_count() == 1 && !w.expired());
        a.reset();
        assert(Tracked::alive == 0 && w.expired() && !w.lock());   // object gone, block alive
    }   // w destroyed -> block freed (ASan would flag a leak or double free)

    {
        SharedPtr<Tracked> p(new Tracked(2), [](Tracked* t) { delete t; });
        std::vector<std::thread> ts;
        for (int i = 0; i < 8; ++i)                // concurrent copies/destructions of owners
            ts.emplace_back([p] { for (int k = 0; k < 10000; ++k) { SharedPtr<Tracked> c = p; (void)c; } });
        WeakPtr<Tracked> w = p;
        p.reset();                                 // threads still own copies
        for (auto& t : ts) t.join();
        assert(w.expired() && Tracked::alive == 0);
    }

    {
        auto n1 = make_shared_ptr<Node>();
        auto n2 = make_shared_ptr<Node>();
        n1->next = n2;
        n2->prev = n1;                             // weak: no cycle of strong refs
        assert(n2->prev.lock().get() == n1.get());
    }                                              // both freed

    {   // race lock() against the last release
        for (int round = 0; round < 1000; ++round) {
            auto s = make_shared_ptr<Tracked>(round);
            WeakPtr<Tracked> w = s;
            std::thread t([&w] { if (auto l = w.lock()) assert(l->value >= 0); });
            s.reset();
            t.join();
        }
        assert(Tracked::alive == 0);
    }
    std::puts("shared_ptr/weak_ptr: all tests passed");
}
```

Key points to say out loud:

- **Memory orders.** Increments can be `relaxed`: you already own a reference, so the count cannot hit zero underneath you, and nothing is published. The decrement must be `release` so this thread's writes to the object happen-before the destructor, and the thread that sees `1 → 0` needs `acquire` before running `~T`. `acq_rel` on every decrement is simplest, and it is what libstdc++ uses. Rust's `Arc` uses `release` on every decrement plus an `acquire` fence only on the last one. See [12.9](#129-the-c-memory-model).
- **`lock()` cannot be `fetch_add`.** Between "strong is 1" and the increment, another thread may drop it to 0 and start destroying the object. Incrementing 0 → 1 would resurrect a dead object. The CAS loop only increments a non-zero count.
- **The `weak_` + 1 trick** gives a single owner for freeing the block: the last strong release drops the collective weak reference, so whoever brings `weak_` to 0 deletes the block, with no race between "last strong" and "last weak" deciding who frees.
- **`make_shared` trade-off**: one allocation and better locality, but the object's *memory* lives until the last `weak_ptr` dies (only `~T` runs at strong == 0).
- **Thread-safety contract**: different `SharedPtr` objects sharing one block can be used concurrently, as tested above. *The same* `SharedPtr` object written and read concurrently is a data race, which is what `std::atomic<std::shared_ptr<T>>` (C++20) is for.
- Not implemented here (good follow-ups): the aliasing constructor (`SharedPtr<Member>(owner, &owner->m)`), `enable_shared_from_this` (a `WeakPtr` member set by the `SharedPtr` constructor), `std::allocate_shared`, and arrays.

## 16.3 `Vector<T>`: Placement New, Growth, and the Strong Guarantee

What the interviewer checks: separating **allocation** (`::operator new`, raw bytes) from **construction** (placement new) and destruction (`std::destroy`); geometric growth; `move_if_noexcept` during reallocation; the **strong exception guarantee** for `push_back` (if anything throws, the vector is unchanged); `v.push_back(v[0])` aliasing; over-aligned `T`.

```cpp
// vector.cpp -- g++ -std=c++20 -Wall -Wextra -fsanitize=address,undefined vector.cpp
#include <algorithm>
#include <cassert>
#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <initializer_list>
#include <memory>
#include <new>
#include <stdexcept>
#include <string>
#include <type_traits>
#include <utility>

template <class T>
class Vector {
public:
    using value_type = T;
    using iterator = T*;
    using const_iterator = const T*;

    Vector() noexcept = default;
    explicit Vector(std::size_t n, const T& value = T()) { reserve(n); while (size_ < n) push_back(value); }
    Vector(std::initializer_list<T> il) { reserve(il.size()); for (const T& x : il) push_back(x); }

    Vector(const Vector& o) : Vector() {
        reserve(o.size_);
        for (const T& x : o) push_back(x);   // if this throws, ~Vector() of the delegated-to
    }                                        // object cleans up (the delegating ctor completed)
    Vector(Vector&& o) noexcept
        : data_(std::exchange(o.data_, nullptr)), size_(std::exchange(o.size_, 0)),
          cap_(std::exchange(o.cap_, 0)) {}

    // One assignment operator for copy AND move: strong guarantee for copy
    // (the copy is made before *this is touched), noexcept-ish swap for move.
    Vector& operator=(Vector o) noexcept { swap(o); return *this; }

    ~Vector() { destroy_all(); deallocate(data_, cap_); }

    void swap(Vector& o) noexcept {
        std::swap(data_, o.data_); std::swap(size_, o.size_); std::swap(cap_, o.cap_);
    }

    // ---- element access ----
    T& operator[](std::size_t i) noexcept { return data_[i]; }
    const T& operator[](std::size_t i) const noexcept { return data_[i]; }
    T& at(std::size_t i) { if (i >= size_) throw std::out_of_range("Vector::at"); return data_[i]; }
    T& back() noexcept { return data_[size_ - 1]; }
    iterator begin() noexcept { return data_; }
    iterator end() noexcept { return data_ + size_; }
    const_iterator begin() const noexcept { return data_; }
    const_iterator end() const noexcept { return data_ + size_; }
    std::size_t size() const noexcept { return size_; }
    std::size_t capacity() const noexcept { return cap_; }
    bool empty() const noexcept { return size_ == 0; }

    // ---- modifiers ----
    void push_back(const T& x) { emplace_back(x); }
    void push_back(T&& x) { emplace_back(std::move(x)); }

    template <class... Args>
    T& emplace_back(Args&&... args) {
        if (size_ < cap_) {
            ::new (static_cast<void*>(data_ + size_)) T(std::forward<Args>(args)...);  // placement new
            return data_[size_++];
        }
        return realloc_emplace(std::forward<Args>(args)...);
    }

    void pop_back() noexcept { data_[--size_].~T(); }
    void clear() noexcept { destroy_all(); }

    void reserve(std::size_t n) {
        if (n <= cap_) return;
        T* nd = allocate(n);
        try { relocate_into(nd); }           // may throw (copying ctor): old buffer untouched
        catch (...) { deallocate(nd, n); throw; }
        destroy_all_keep_size();
        deallocate(data_, cap_);
        data_ = nd; cap_ = n;
    }

    void resize(std::size_t n) {
        if (n < size_) { while (size_ > n) pop_back(); return; }
        reserve(n);
        while (size_ < n) emplace_back();    // basic guarantee: earlier new elements stay
    }

private:
    static T* allocate(std::size_t n) {
        if (n > static_cast<std::size_t>(PTRDIFF_MAX) / sizeof(T)) throw std::length_error("Vector");
        if constexpr (alignof(T) > __STDCPP_DEFAULT_NEW_ALIGNMENT__)
            return static_cast<T*>(::operator new(n * sizeof(T), std::align_val_t{alignof(T)}));
        else
            return static_cast<T*>(::operator new(n * sizeof(T)));   // raw memory, NO constructors
    }
    static void deallocate(T* p, std::size_t n) noexcept {
        if (!p) return;
        if constexpr (alignof(T) > __STDCPP_DEFAULT_NEW_ALIGNMENT__)
            ::operator delete(p, n * sizeof(T), std::align_val_t{alignof(T)});
        else
            ::operator delete(p, n * sizeof(T));
    }
    void destroy_all() noexcept { destroy_all_keep_size(); size_ = 0; }
    void destroy_all_keep_size() noexcept { std::destroy(data_, data_ + size_); }

    // Move elements if T's move ctor is noexcept (or T is move-only); otherwise COPY,
    // so that a throw leaves the source intact (strong guarantee) -- std::move_if_noexcept.
    void relocate_into(T* nd) {
        std::size_t i = 0;
        try {
            for (; i < size_; ++i)
                ::new (static_cast<void*>(nd + i)) T(std::move_if_noexcept(data_[i]));
        } catch (...) {
            std::destroy(nd, nd + i);        // undo the partial copy; caller frees nd
            throw;
        }
    }

    template <class... Args>
    T& realloc_emplace(Args&&... args) {
        std::size_t new_cap = cap_ ? cap_ * 2 : 1;           // geometric growth -> amortized O(1)
        T* nd = allocate(new_cap);
        // 1) Construct the NEW element first: args may alias an existing element
        //    (v.push_back(v[0])), which must still be alive and unmoved.
        try {
            ::new (static_cast<void*>(nd + size_)) T(std::forward<Args>(args)...);
        } catch (...) { deallocate(nd, new_cap); throw; }
        // 2) Move/copy the old elements.
        try { relocate_into(nd); }
        catch (...) { nd[size_].~T(); deallocate(nd, new_cap); throw; }
        // 3) Commit: nothing below can throw.
        destroy_all_keep_size();
        deallocate(data_, cap_);
        data_ = nd; cap_ = new_cap;
        return data_[size_++];
    }

    T* data_ = nullptr;
    std::size_t size_ = 0;
    std::size_t cap_ = 0;
};

// ---------------- tests ----------------
struct Counted {                       // copy may throw; move is NOT noexcept
    static inline int alive = 0, copies = 0, moves = 0, throw_on_copy = -1;
    std::string s;
    explicit Counted(std::string v) : s(std::move(v)) { ++alive; }
    Counted(const Counted& o) : s(o.s) {
        if (throw_on_copy >= 0 && copies++ == throw_on_copy) throw std::runtime_error("copy");
        ++alive;
    }
    Counted(Counted&& o) : s(std::move(o.s)) { ++moves; ++alive; }   // no noexcept!
    ~Counted() { --alive; }
};
struct NothrowMove {
    static inline int copies = 0, moves = 0;
    NothrowMove() = default;
    NothrowMove(const NothrowMove&) { ++copies; }
    NothrowMove(NothrowMove&&) noexcept { ++moves; }
};
struct alignas(64) Line { double v[8]; };

int main() {
    {   // growth sequence and aliasing
        Vector<std::string> v;
        std::size_t last = 0;
        std::printf("capacities:");
        for (int i = 0; i < 20; ++i) {
            v.push_back(std::string(40, 'a' + i % 26));       // heap-allocated strings
            if (v.capacity() != last) std::printf(" %zu", last = v.capacity());
        }
        std::printf("\n");
        while (v.size() < v.capacity()) v.push_back("x");
        v.push_back(v[0]);                                     // aliasing exactly at reallocation
        assert(v.back() == std::string(40, 'a'));
    }
    {   // strong guarantee: a copy throws midway through reallocation
        Vector<Counted> v;
        v.reserve(4);
        for (int i = 0; i < 4; ++i) v.emplace_back("k" + std::to_string(i));
        Counted::copies = 0; Counted::throw_on_copy = 2;       // 3rd copy throws
        try { v.emplace_back("k4"); assert(false); }
        catch (const std::runtime_error&) {}
        assert(v.size() == 4 && v.capacity() == 4);
        for (int i = 0; i < 4; ++i) assert(v[i].s == "k" + std::to_string(i));   // unchanged
        assert(Counted::alive == 4 && Counted::moves == 0);    // copied, never moved
        Counted::throw_on_copy = -1;
    }
    assert(Counted::alive == 0);
    {   // noexcept move -> reallocation moves
        Vector<NothrowMove> v;
        for (int i = 0; i < 9; ++i) v.emplace_back();
        std::printf("NothrowMove: copies=%d moves=%d\n", NothrowMove::copies, NothrowMove::moves);
        assert(NothrowMove::copies == 0);
    }
    {   // move-only type, copy/move of the container, over-aligned type
        Vector<std::unique_ptr<int>> u;
        for (int i = 0; i < 5; ++i) u.push_back(std::make_unique<int>(i));
        Vector<std::unique_ptr<int>> u2 = std::move(u);
        assert(u.size() == 0 && *u2[4] == 4);

        Vector<int> a{1, 2, 3};
        Vector<int> b = a;
        b[0] = 9;
        a = b;
        assert(a[0] == 9 && a.size() == 3);
        a.resize(6);
        assert(a[5] == 0);

        Vector<Line> lines(3);
        assert(reinterpret_cast<std::uintptr_t>(&lines[0]) % 64 == 0);
    }
    std::puts("Vector: all tests passed");
}
```

```text
capacities: 1 2 4 8 16 32
NothrowMove: copies=0 moves=15
Vector: all tests passed
```

Why the order in `realloc_emplace` matters: (1) construct the new element **first**, because its argument may be a reference into the old buffer; (2) then relocate; (3) commit with only non-throwing operations (destroy, free, pointer swaps). If step 1 or 2 throws, the old buffer is untouched, so the strong guarantee holds. That works only because step 2 *copies* when the move constructor might throw: the `Counted` test throws on the third copy and verifies that nothing changed and nothing leaked (`alive == 4`). The `NothrowMove` count of 15 moves = 1 + 2 + 4 + 8 for growth to 16 capacity during 9 inserts. Follow-ups: `insert`/`erase` in the middle (shift with move assignment, only the basic guarantee unless nothrow), using `std::allocator_traits` instead of raw `operator new` (to support allocators), and `realloc`-based growth for trivially relocatable types (as `folly::fbvector` does).

## 16.4 `String`: The Rule of Five

What the interviewer checks: deep copy, a `noexcept` move that leaves the source valid (empty), self-assignment safety for copy *and* move, exception-safe copy assignment, and `a += a`.

```cpp
// string.cpp -- g++ -std=c++20 -Wall -Wextra -fsanitize=address,undefined string.cpp
#include <algorithm>
#include <cassert>
#include <cstddef>
#include <cstdio>
#include <cstring>
#include <ostream>
#include <iostream>
#include <utility>

class String {
public:
    String() noexcept = default;                         // empty: data_ == nullptr, c_str() returns ""
    String(const char* s) : String(s, std::strlen(s)) {}  // implicit, like std::string
    String(const char* s, std::size_t n) : size_(n), cap_(n) {
        if (n) {
            data_ = new char[n + 1];                     // +1 for the terminator
            std::memcpy(data_, s, n);
            data_[n] = '\0';
        }
    }

    // ---- Rule of Five ----
    ~String() { delete[] data_; }                                    // 1. destructor

    String(const String& o) : String(o.data_ ? o.data_ : "", o.size_) {}   // 2. copy ctor (deep copy)

    String(String&& o) noexcept                                       // 3. move ctor: steal
        : data_(std::exchange(o.data_, nullptr)),
          size_(std::exchange(o.size_, 0)),
          cap_(std::exchange(o.cap_, 0)) {}

    String& operator=(const String& o) {                              // 4. copy assignment
        if (this != &o) {
            String tmp(o);              // may throw -> *this untouched (strong guarantee)
            swap(tmp);                  // old buffer released by tmp's destructor
        }
        return *this;
    }
    String& operator=(String&& o) noexcept {                          // 5. move assignment
        if (this != &o) {
            delete[] data_;
            data_ = std::exchange(o.data_, nullptr);
            size_ = std::exchange(o.size_, 0);
            cap_ = std::exchange(o.cap_, 0);
        }
        return *this;
    }

    void swap(String& o) noexcept {
        std::swap(data_, o.data_); std::swap(size_, o.size_); std::swap(cap_, o.cap_);
    }

    String& operator+=(const String& rhs) {
        std::size_t rn = rhs.size_;                       // read BEFORE growing: rhs may be *this
        if (size_ + rn > cap_) {
            std::size_t nc = std::max(size_ + rn, cap_ * 2);   // geometric growth
            char* nd = new char[nc + 1];
            if (size_) std::memcpy(nd, data_, size_);
            if (rn) std::memcpy(nd + size_, rhs.data_, rn);    // rhs.data_ still valid here
            delete[] data_;
            data_ = nd; cap_ = nc;
        } else if (rn) {
            std::memmove(data_ + size_, rhs.data_, rn);
        }
        size_ += rn;
        if (data_) data_[size_] = '\0';
        return *this;
    }
    friend String operator+(String lhs, const String& rhs) { lhs += rhs; return lhs; }

    const char* c_str() const noexcept { return data_ ? data_ : ""; }
    std::size_t size() const noexcept { return size_; }
    std::size_t capacity() const noexcept { return cap_; }
    char& operator[](std::size_t i) noexcept { return data_[i]; }

    friend bool operator==(const String& a, const String& b) noexcept {
        return a.size_ == b.size_ && (a.size_ == 0 || std::memcmp(a.data_, b.data_, a.size_) == 0);
    }
    friend std::ostream& operator<<(std::ostream& os, const String& s) { return os << s.c_str(); }

private:
    char* data_ = nullptr;
    std::size_t size_ = 0;
    std::size_t cap_ = 0;
};

int main() {
    String a = "wave";
    String b = a;                         // copy ctor
    b[0] = 'W';
    assert(a == String("wave") && b == String("Wave"));

    String c = std::move(b);              // move ctor: b is now empty but valid
    assert(b.size() == 0 && std::strcmp(b.c_str(), "") == 0);

    b = c;                                // copy assignment into a moved-from object
    String& alias = b;
    b = alias;                            // self copy-assignment
    b = std::move(alias);                 // self move-assignment: must not free its own buffer
    assert(b == String("Wave"));

    a += a;                               // self-append across a reallocation
    assert(a == String("wavewave"));
    String d = a + "front" + String();    // temporaries + empty operand
    std::cout << d << " size=" << d.size() << "\n";
    std::puts("String: all tests passed");
}
```

Discussion points: the classic *broken* copy assignment is `delete[] data_; data_ = new char[...]; memcpy(..., o.data_ ...)`. It fails on self-assignment (copies from freed memory) and is not exception-safe (if `new` throws, `data_` dangles). The **copy-and-swap** form fixes both. A single by-value `operator=(String o)` can replace both assignment operators, at the cost of an extra move for move assignment. **Rule of Zero**: in production you would hold a `std::unique_ptr<char[]>` or a `std::vector<char>` and write none of the five. The exercise exists to show you know what they would have to do. Extensions: SSO (a union of `{char*, cap}` and `char buf[16]`, as in libstdc++, see [7.7](#77-container-internals)), and `operator<=>`.

## 16.5 `BoundedQueue<T>`: Thread-Safe Blocking Queue

What the interviewer checks: waiting with a **predicate** (handles spurious and lost wakeups), **two** condition variables (producers wait for "not full", consumers for "not empty"), notifying after unlocking, a clean shutdown that wakes everyone, and no data races (TSan-clean).

```cpp
// bounded_queue.cpp -- g++ -std=c++20 -Wall -Wextra -O2 -fsanitize=thread bounded_queue.cpp
#include <cassert>
#include <chrono>
#include <condition_variable>
#include <cstddef>
#include <cstdio>
#include <deque>
#include <mutex>
#include <optional>
#include <thread>
#include <vector>

template <class T>
class BoundedQueue {
public:
    explicit BoundedQueue(std::size_t capacity) : cap_(capacity) {}

    // Blocks while full. Returns false if the queue was closed (item not enqueued).
    bool push(T item) {
        {
            std::unique_lock lk(m_);
            not_full_.wait(lk, [&] { return q_.size() < cap_ || closed_; });   // predicate: no lost/spurious wakeups
            if (closed_) return false;
            q_.push_back(std::move(item));
        }                               // unlock BEFORE notify: the woken thread can grab the mutex at once
        not_empty_.notify_one();
        return true;
    }

    // Blocks while empty. Returns nullopt only when closed AND drained.
    std::optional<T> pop() {
        std::optional<T> out;
        {
            std::unique_lock lk(m_);
            not_empty_.wait(lk, [&] { return !q_.empty() || closed_; });
            if (q_.empty()) return std::nullopt;                // closed and drained
            out.emplace(std::move(q_.front()));
            q_.pop_front();
        }
        not_full_.notify_one();
        return out;
    }

    template <class Rep, class Period>
    std::optional<T> pop_for(std::chrono::duration<Rep, Period> timeout) {
        std::optional<T> out;
        {
            std::unique_lock lk(m_);
            if (!not_empty_.wait_for(lk, timeout, [&] { return !q_.empty() || closed_; }) || q_.empty())
                return std::nullopt;                           // timed out, or closed and drained
            out.emplace(std::move(q_.front()));
            q_.pop_front();
        }
        not_full_.notify_one();
        return out;
    }

    bool try_push(T item) {
        {
            std::lock_guard lk(m_);
            if (closed_ || q_.size() >= cap_) return false;
            q_.push_back(std::move(item));
        }
        not_empty_.notify_one();
        return true;
    }

    // Wake EVERYONE: blocked producers fail, consumers drain what is left then get nullopt.
    void close() {
        { std::lock_guard lk(m_); closed_ = true; }
        not_full_.notify_all();
        not_empty_.notify_all();
    }

private:
    std::mutex m_;
    std::condition_variable not_full_, not_empty_;   // two CVs: producers and consumers never wake each other's kind
    std::deque<T> q_;
    const std::size_t cap_;
    bool closed_ = false;
};

int main() {
    BoundedQueue<long> q(8);
    constexpr int kProducers = 4, kConsumers = 3, kPerProducer = 20000;
    std::vector<std::thread> producers, consumers;
    std::vector<long> sums(kConsumers, 0);

    for (int c = 0; c < kConsumers; ++c)
        consumers.emplace_back([&, c] { while (auto v = q.pop()) sums[c] += *v; });
    for (int p = 0; p < kProducers; ++p)
        producers.emplace_back([&] { for (long i = 1; i <= kPerProducer; ++i) q.push(i); });

    for (auto& t : producers) t.join();
    q.close();                                   // consumers exit after draining
    for (auto& t : consumers) t.join();

    long total = 0;
    for (long s : sums) total += s;
    long expected = kProducers * (long{kPerProducer} * (kPerProducer + 1) / 2);
    std::printf("total=%ld expected=%ld\n", total, expected);
    assert(total == expected);

    assert(!q.push(1));                          // closed: rejected
    BoundedQueue<int> empty(1);
    assert(!empty.pop_for(std::chrono::milliseconds(10)));   // timeout path
    std::puts("BoundedQueue: all tests passed");
}
```

Failure modes to mention: `if` instead of `while`/predicate (a spurious wakeup pops from an empty deque); a single CV with `notify_one` (a producer may wake another producer, and the consumer that should run sleeps forever, a lost wakeup); `close()` notifying only one side (threads stay blocked forever); and moving the item out while holding the lock is fine, but calling user callbacks under the lock invites deadlock. Where `T`'s move constructor can throw, `pop` moving into `optional` before `pop_front` keeps the queue intact if the move throws. More variants (LeetCode 1188, a lock-free SPSC ring buffer) are in [Concurrency Coding Problems](../computer-science/Concurrency_Coding_Problems.md#8-bounded-blocking-queue-leetcode-1188) and [12.11](#1211-lock-free-data-structures-and-memory-reclamation).

## 16.6 `Function<Sig>`: Type Erasure with Small-Buffer Optimization

What the interviewer checks: how one non-template class can hold *any* callable. The answer is a **type-erased** object (stored inline or on the heap) plus a pointer to a per-type table of operations (invoke, copy, move, destroy), generated by a template constructor. This is exactly what `std::function`, `std::any`, and `std::move_only_function` do. Small callables are stored **inline** (small-buffer optimization) to avoid a heap allocation.

```cpp
// function.cpp -- g++ -std=c++20 -Wall -Wextra -fsanitize=address,undefined function.cpp
#include <cassert>
#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <functional>   // std::bad_function_call, std::invoke
#include <memory>
#include <new>
#include <string>
#include <type_traits>
#include <utility>

template <class Sig> class Function;   // primary template: only R(Args...) is defined

template <class R, class... Args>
class Function<R(Args...)> {
    // Small-buffer optimization: callables up to 3 pointers live inline (no heap).
    static constexpr std::size_t kBufSize = 3 * sizeof(void*);
    struct alignas(std::max_align_t) Storage { unsigned char bytes[kBufSize]; };  // not aligned_storage (deprecated in C++23)

    // Hand-rolled "vtable": one static table of function pointers per erased type F.
    struct VTable {
        R (*invoke)(void* obj, Args&&... args);
        void (*copy)(const void* src, Storage& dst);   // copy-construct into dst
        void (*move)(void* src, Storage& dst) noexcept;// move-construct into dst, destroy src
        void (*destroy)(void* obj) noexcept;
        bool inline_storage;                           // kInline<F>, exposed for tests/diagnostics
    };

    template <class F>
    static constexpr bool kInline = sizeof(F) <= kBufSize && alignof(F) <= alignof(std::max_align_t) &&
                                    std::is_nothrow_move_constructible_v<F>;   // so our move can be noexcept

    template <class F>
    static F* target(void* storage) noexcept {
        if constexpr (kInline<F>) return std::launder(reinterpret_cast<F*>(storage));
        else return *std::launder(reinterpret_cast<F**>(storage));          // buffer holds an F*
    }

    template <class F>
    static constexpr VTable kTable{
        [](void* s, Args&&... a) -> R { return std::invoke(*target<F>(s), std::forward<Args>(a)...); },
        [](const void* s, Storage& d) {
            const F& src = *target<F>(const_cast<void*>(s));
            if constexpr (kInline<F>) ::new (static_cast<void*>(&d)) F(src);
            else ::new (static_cast<void*>(&d)) F*(new F(src));
        },
        [](void* s, Storage& d) noexcept {
            if constexpr (kInline<F>) {
                F* src = target<F>(s);
                ::new (static_cast<void*>(&d)) F(std::move(*src));
                src->~F();
            } else {
                ::new (static_cast<void*>(&d)) F*(target<F>(s));   // just steal the heap pointer
            }
        },
        [](void* s) noexcept {
            if constexpr (kInline<F>) target<F>(s)->~F();
            else delete target<F>(s);
        },
        kInline<F>};

public:
    Function() noexcept = default;
    Function(std::nullptr_t) noexcept {}

    template <class F, class D = std::decay_t<F>,
              class = std::enable_if_t<!std::is_same_v<D, Function> && std::is_invocable_r_v<R, D&, Args...>>>
    Function(F&& f) {
        if constexpr (kInline<D>) ::new (static_cast<void*>(&buf_)) D(std::forward<F>(f));
        else ::new (static_cast<void*>(&buf_)) D*(new D(std::forward<F>(f)));
        vt_ = &kTable<D>;
    }

    Function(const Function& o) { if (o.vt_) { o.vt_->copy(&o.buf_, buf_); vt_ = o.vt_; } }
    Function(Function&& o) noexcept {
        if (o.vt_) { o.vt_->move(&o.buf_, buf_); vt_ = std::exchange(o.vt_, nullptr); }
    }
    Function& operator=(Function o) noexcept {     // copy-and-swap via a temporary
        reset();
        if (o.vt_) { o.vt_->move(&o.buf_, buf_); vt_ = std::exchange(o.vt_, nullptr); }
        return *this;
    }
    ~Function() { reset(); }

    R operator()(Args... args) const {
        if (!vt_) throw std::bad_function_call();
        return vt_->invoke(const_cast<Storage*>(&buf_), std::forward<Args>(args)...);
    }
    explicit operator bool() const noexcept { return vt_ != nullptr; }
    bool stored_inline() const noexcept { return vt_ && vt_->inline_storage; }

private:
    void reset() noexcept { if (vt_) { vt_->destroy(&buf_); vt_ = nullptr; } }
    Storage buf_;
    const VTable* vt_ = nullptr;
};

// ---------------- tests ----------------
static int heap_allocs = 0;
void* operator new(std::size_t n) { ++heap_allocs; if (void* p = std::malloc(n)) return p; throw std::bad_alloc(); }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }

int add(int a, int b) { return a + b; }

int main() {
    Function<int(int, int)> f = add;                       // function pointer: inline
    assert(f(2, 3) == 5);

    int base = 10;
    heap_allocs = 0;
    Function<int(int)> small = [base](int x) { return base + x; };   // 4-byte capture: inline
    assert(small(5) == 15 && small.stored_inline() && heap_allocs == 0);

    struct Big { double a[8]; double operator()(double x) const { return a[0] + x; } };
    Function<double(double)> big = Big{{1.5}};             // 64 bytes: heap
    // Check the storage decision, not the allocation count: at -O1+ GCC may elide a
    // new/delete pair ([expr.new]/14), so the replaced operator new can see 0 calls.
    assert(!big.stored_inline() && heap_allocs <= 1 && big(1.0) == 2.5);

    auto counter = [n = 0]() mutable { return ++n; };      // stateful, copied by value
    Function<int()> c1 = counter;
    Function<int()> c2 = c1;                                // deep copy of the state
    c1(); c1();
    assert(c1() == 3 && c2() == 1);

    Function<int()> moved = std::move(c1);
    assert(!c1 && moved() == 4);

    Function<std::string(std::string)> up = [](std::string s) { for (auto& ch : s) ch -= 32; return s; };
    assert(up("lds") == "LDS");

    Function<void()> empty;
    try { empty(); assert(false); } catch (const std::bad_function_call&) {}

    big = small.operator bool() ? Function<double(double)>([](double x) { return x * 2; }) : nullptr;
    assert(big(4.0) == 8.0);
    std::puts("Function: all tests passed");
}
```

Design notes: the per-type `VTable` is a `static constexpr` variable template, so each callable type gets exactly one table in read-only data, and the object stores a single pointer to it (8 bytes) instead of a C++ vptr plus a heap-allocated derived object. Callables go inline only if they fit, are suitably aligned, **and** are nothrow-move-constructible, so that `Function`'s own move can be `noexcept`. libc++'s `std::function` uses a similar rule; libstdc++ is stricter and keeps only *trivially copyable* callables inline (measured: a 4-byte lambda capturing a type with a user-written copy constructor is heap-allocated). The `operator()` is `const` but invokes a possibly mutable target, the same const-correctness hole `std::function` has, and one reason C++23 added `std::move_only_function` with qualified signatures. Real implementations' SBO sizes: libstdc++ `std::function` stores 16 bytes inline (`sizeof` = 32), and libc++ 24 bytes (`sizeof` = 48). Compare the classic OO version in [Design Patterns: Type Erasure](../design-patterns/Design_Patterns_Cpp.md#31-type-erasure) and when to avoid `std::function` in hot paths in [8.5](#85-stdfunction-and-type-erasure).

## 16.7 `Any`: Type Erasure with a Virtual Holder

What the interviewer checks: the classic OO type-erasure pattern (an abstract `HolderBase` plus a templated `Holder<T>`), deep copy through `virtual clone()`, and type-checked retrieval. `any_cast<T>` matches the **exact** stored type: `any_cast<Base>` on a stored `Derived` fails, just as with `std::any`.

```cpp
// any.cpp -- g++ -std=c++20 -Wall -Wextra -fsanitize=address,undefined any.cpp
#include <cassert>
#include <cstdio>
#include <memory>
#include <string>
#include <type_traits>
#include <typeinfo>
#include <utility>
#include <vector>

class BadAnyCast : public std::bad_cast {
public:
    const char* what() const noexcept override { return "bad any cast"; }
};

class Any {
    struct HolderBase {                                  // classic OO type erasure
        virtual ~HolderBase() = default;
        virtual std::unique_ptr<HolderBase> clone() const = 0;
        virtual const std::type_info& type() const noexcept = 0;
    };
    template <class T>
    struct Holder final : HolderBase {
        T value;
        template <class U> explicit Holder(U&& v) : value(std::forward<U>(v)) {}
        std::unique_ptr<HolderBase> clone() const override { return std::make_unique<Holder>(value); }
        const std::type_info& type() const noexcept override { return typeid(T); }
    };

public:
    Any() noexcept = default;
    template <class T, class D = std::decay_t<T>,
              class = std::enable_if_t<!std::is_same_v<D, Any> && std::is_copy_constructible_v<D>>>
    Any(T&& v) : p_(std::make_unique<Holder<D>>(std::forward<T>(v))) {}

    Any(const Any& o) : p_(o.p_ ? o.p_->clone() : nullptr) {}   // deep copy through the virtual
    Any(Any&&) noexcept = default;
    Any& operator=(Any o) noexcept { p_ = std::move(o.p_); return *this; }

    bool has_value() const noexcept { return p_ != nullptr; }
    const std::type_info& type() const noexcept { return p_ ? p_->type() : typeid(void); }
    void reset() noexcept { p_.reset(); }

    template <class T> friend T* any_cast(Any* a) noexcept;
    template <class T> friend const T* any_cast(const Any* a) noexcept;

private:
    std::unique_ptr<HolderBase> p_;
};

// Pointer form: nullptr on mismatch (no exception). Exact type match only --
// any_cast<Base>(&any_holding_Derived) fails, just like std::any.
template <class T>
T* any_cast(Any* a) noexcept {
    if (!a || !a->p_ || a->p_->type() != typeid(T)) return nullptr;
    return &static_cast<Any::Holder<T>*>(a->p_.get())->value;
}
template <class T>
const T* any_cast(const Any* a) noexcept { return any_cast<T>(const_cast<Any*>(a)); }

// Value form: throws on mismatch.
template <class T>
T any_cast(const Any& a) {
    using U = std::remove_cvref_t<T>;
    if (const U* p = any_cast<U>(&a)) return static_cast<T>(*p);
    throw BadAnyCast();
}

int main() {
    std::vector<Any> row{42, std::string("gfx942"), 3.5, Any{}};
    assert(*any_cast<int>(&row[0]) == 42);
    assert(any_cast<std::string>(row[1]) == "gfx942");
    assert(any_cast<double>(&row[1]) == nullptr);       // wrong type -> nullptr
    assert(!row[3].has_value() && row[3].type() == typeid(void));

    Any copy = row[1];                                   // deep copy
    *any_cast<std::string>(&copy) += "-xnack";
    assert(any_cast<std::string>(row[1]) == "gfx942");

    try { (void)any_cast<int>(row[2]); assert(false); }
    catch (const std::bad_cast& e) { std::printf("caught: %s\n", e.what()); }

    row[0] = std::string("reassigned");                  // change the stored type
    assert(row[0].type() == typeid(std::string));
    std::puts("Any: all tests passed");
}
```

Follow-ups: **no RTTI** (`-fno-rtti`): replace `typeid` with a per-type tag such as the address of a `static` variable template, `template <class T> inline constexpr char type_tag = 0;`, and compare `&type_tag<T>`. That is unique per type within one binary. Across shared libraries it depends on symbol visibility: hidden copies in two `.so`s have different addresses, the same problem `type_info` comparisons have (see [13.9](#139-runtime-loading-dlopen-and-dlsym)). **SBO**: `std::any` implementations store small, nothrow-movable types inline, as in [16.6](#166-functionsig-type-erasure-with-small-buffer-optimization). **`any` vs `variant`**: `std::variant` is a closed set of types with no heap and no RTTI, and `std::visit` is checked at compile time; `std::any` is an open set, which suits property bags and plugin metadata ([10.4](#104-stdvariant), [10.5](#105-stdany)).

---

## Common Interview Questions -- Implement-from-scratch

**Q1.** In your `shared_ptr`, why is the reference-count increment `relaxed` but the decrement `acq_rel`?

An increment is done by a thread that already holds a reference, so the count cannot reach zero concurrently, and the increment publishes nothing, so no ordering is needed, only atomicity. The decrement is different. Each owner's writes to the object must be visible to whichever thread runs the destructor. That thread's decrement must *acquire* (synchronize with every other owner's *release* decrement, which works through the release sequence on the counter), and every decrement must *release*. Using `relaxed` for decrements would let `~T` run while another thread's last writes to `*ptr` are not yet visible to it, which is a data race and use-after-free territory. The optimized form is `if (fetch_sub(1, release) == 1) { atomic_thread_fence(acquire); delete; }`.

**Q2.** Your `Vector::push_back` takes `const T&`. What breaks if the argument refers to an element of the same vector, and how do you handle it?

`v.push_back(v[0])` at full capacity reallocates. If you move the old elements first and then copy from the reference, you read from a moved-from or already freed element. Fix: construct the new element in the *new* buffer first (while the old buffer is untouched), then relocate the rest, as `realloc_emplace` does. Alternatively, copy the argument into a local temporary before growing (costs one extra move). The same issue appears in `insert(pos, v[i])` and in `String::operator+=(*this)`.

**Q3.** What are the three exception-safety guarantees, and which does each of your containers provide?

*Basic*: no leaks and invariants hold, but the state may have changed. *Strong*: commit-or-rollback, so if it throws, nothing changed. *Nothrow*: never throws. `Vector::push_back`/`emplace_back`/`reserve` give the strong guarantee (construct into new storage, use copies when moves could throw, then commit with non-throwing operations). `resize` growing gives basic (elements already appended stay). Move constructor, `swap`, destructor, and `pop_back` are nothrow. `String` copy assignment is strong via copy-and-swap, and move operations are nothrow. `BoundedQueue::push` is strong: if `push_back` throws, the deque is unchanged.

**Q4.** How does `std::function` avoid a heap allocation for small lambdas, and what makes a lambda "too big"?

It reserves an inline buffer inside the `std::function` object (16 bytes in libstdc++, 24 in libc++) and placement-news the callable there when it fits, is suitably aligned, and meets the library's copy requirement: trivially copyable for libstdc++, nothrow-copy-constructible for libc++. Otherwise it heap-allocates. A lambda capturing three `std::string`s by value (96 bytes) or a `std::vector` and a `double` by value is heap-allocated. A capture-less lambda, a function pointer, or a lambda capturing one or two pointers or references stays inline. Measure by replacing `operator new` (as in 16.6) or with heaptrack. In hot code, prefer a template parameter (`template <class F> void run(F&& f)`) or `function_ref`-style non-owning views (C++26 `std::function_ref`).

**Q5.** Write the bounded queue's `pop` with a single condition variable. Why is that worse?

With one CV both producers and consumers wait on it, so `notify_one` can wake the *wrong kind* of thread: a producer notifying after a push may wake another producer that is waiting for space. That producer re-checks its predicate, goes back to sleep, and the notification is lost while a consumer stays asleep. You must switch to `notify_all`, which wakes every waiter on every operation (a thundering herd) and costs throughput. Two CVs make every notification targeted.

**Q6.** What is the Rule of Five, and when do you write zero of them instead?

If a class manages a resource directly, it needs a destructor, a copy constructor, copy assignment, a move constructor, and move assignment, because the compiler-generated memberwise versions would double-free or leak. Declaring any of the copy operations or the destructor suppresses the implicit move operations, so a class that declares only a destructor silently copies when you meant to move. The Rule of Zero says to wrap each resource in its own RAII member (`unique_ptr` with a custom deleter, `vector`, a handle class) so the containing class needs none of the five. The `String` exercise is a Rule-of-Five class only because it *is* the RAII wrapper.

**Q7.** Your interviewer asks you to make `UniquePtr` work with a `FILE*` and `fclose`. What changes, and what is the size?

Nothing in the class: pass a deleter type. `UniquePtr<FILE, decltype(&fclose)> f(fopen(...), &fclose);` stores a function pointer, so `sizeof` is 16. A stateless functor, `struct FClose { void operator()(FILE* f) const { fclose(f); } };`, or a captureless lambda type (`decltype([](FILE* f) { fclose(f); })`, valid in C++20 unevaluated contexts) occupies no space thanks to `[[no_unique_address]]`, so `sizeof` is 8. That is the reason `std::unique_ptr` takes the deleter as a template parameter, while `std::shared_ptr` type-erases it into the control block. Then `shared_ptr<T>` has one type regardless of deleter, at the cost of storing the deleter on the heap.

---
