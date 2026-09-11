# C++ Fundamentals -- Comprehensive Reference

> A deep-dive reference covering every major C++ topic from core language mechanics to modern features. Each section includes conceptual explanations, comparison tables, code examples, and common interview questions with detailed answers. Complements the *CS Fundamentals*, *DSA Fundamentals*, and *LeetCode Patterns* guides.

---

## Table of Contents

### Part 1: Core Language

1. [Type System and Fundamentals](#1-type-system-and-fundamentals)
2. [Pointers, References, and Const Correctness](#2-pointers-references-and-const-correctness)
3. [Memory Management](#3-memory-management)
4. [Object-Oriented Programming](#4-object-oriented-programming)
5. [Move Semantics and Perfect Forwarding](#5-move-semantics-and-perfect-forwarding)

### Part 2: Templates and Generic Programming

6. [Templates](#6-templates)

### Part 3: Standard Template Library

7. [STL Containers](#7-stl-containers)
8. [Iterators, Algorithms, and Lambdas](#8-iterators-algorithms-and-lambdas)

### Part 4: Modern C++ Features

9. [C++11/14 Features](#9-c1114-features)
10. [C++17 Features](#10-c17-features)
11. [C++20 Features](#11-c20-features)

### Part 5: Concurrency

12. [Multithreading and Concurrency](#12-multithreading-and-concurrency)

### Part 6: Compilation and Runtime

13. [Compilation, Linking, and the Preprocessor](#13-compilation-linking-and-the-preprocessor)
14. [Exception Handling and Error Management](#14-exception-handling-and-error-management)
15. [Undefined Behavior, Implementation-Defined, and Best Practices](#15-undefined-behavior-implementation-defined-and-best-practices)

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

## 8.2 Iterator Invalidation Rules

| Container | Insert | Erase |
|---|---|---|
| `vector` | All iterators if reallocation; past-insertion-point otherwise | At and after erased element |
| `deque` | All iterators (always) | All iterators (always, except erasing at front/back) |
| `list` | None | Only the erased element's iterator |
| `set`/`map` | None | Only the erased element's iterator |
| `unordered_set/map` | All if rehash; none otherwise | Only the erased element's iterator |

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
| `std::counting_semaphore` | Semaphore synchronization primitive |
| `std::latch` / `std::barrier` | Thread coordination primitives |
| `std::source_location` | Replacement for `__FILE__`, `__LINE__` |
| `constexpr` containers | `std::vector` and `std::string` in constexpr contexts |
| `std::bit_cast` | Type-safe reinterpretation of bit patterns |
| `using enum` | Import enum values into current scope |
| Designated initializers | `Point{.x = 1, .y = 2}` |
| `char8_t` | UTF-8 character type |
| Template lambdas | `[]<typename T>(T x) { ... }` |

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

---

## Common Interview Questions -- Concurrency

**Q: What is the difference between a mutex and an atomic?**

A mutex provides exclusive access to a critical section of code -- any number of operations between lock and unlock are protected. An `std::atomic` provides atomic (indivisible) access to a single variable without locking. Atomics are faster (often lock-free hardware instructions) but only protect individual operations on a single variable. Use a mutex when multiple variables must be updated consistently; use atomics for simple counters, flags, and lock-free data structures.

**Q: What is a deadlock and how do you prevent it?**

A deadlock occurs when two or more threads are each waiting for a lock held by another, forming a circular dependency. Prevention strategies: (1) always acquire locks in the same order, (2) use `std::scoped_lock` which acquires multiple locks atomically using a deadlock-avoidance algorithm, (3) use `try_lock` with timeout and retry, (4) minimize the scope and duration of locks.

**Q: What is `std::async` and how does it differ from `std::thread`?**

`std::async` is a higher-level abstraction that returns a `std::future` for getting the result. It can run the task on a new thread (`launch::async`) or defer it (`launch::deferred`). `std::thread` gives lower-level control but requires manual result passing (via shared state, promises, etc.) and explicit `join()` or `detach()`. `std::async` also propagates exceptions through the future.

**Q: What are memory orderings and why do they matter?**

Memory orderings control how atomic operations are seen by other threads. The default `seq_cst` (sequentially consistent) provides the strongest guarantee: all threads observe operations in the same order. Relaxed orderings (`acquire`, `release`, `relaxed`) provide weaker but faster guarantees. They matter because modern CPUs and compilers reorder instructions for performance; memory orderings define which reorderings are visible across threads.

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

```bash
# Static library
g++ -c util.cpp -o util.o
ar rcs libutil.a util.o
g++ main.cpp -L. -lutil -o program    # links statically

# Dynamic library (shared object)
g++ -fPIC -shared util.cpp -o libutil.so
g++ main.cpp -L. -lutil -o program    # links dynamically
# Must set LD_LIBRARY_PATH or install to system path
```

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

## 13.6 Preprocessor

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

## 13.7 Build Systems

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

---
