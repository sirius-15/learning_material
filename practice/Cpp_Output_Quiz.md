# C++ Output Quiz -- 55 "What Does This Print?" Puzzles and a Timed C++/CMake/Testing Mock Interview

> Last reviewed: 2026-11 · Versions assumed: GCC 15.2 with libstdc++, x86-64 Linux (LP64, 32-bit `int`, IEEE 754 floating point), `g++ -std=c++20 -Wall`; Section 12 also assumes CMake 4.2, Ninja 1.13, and GoogleTest 1.17. Every program below was compiled and run with that toolchain. Where a result depends on the compiler, ABI, or optimization level, the answer says so. For programs with undefined behavior, the answer reports what we observed only as an illustration, never as "the" output.

Each puzzle is a short, complete program. For each one, answer two questions before opening the [Answers](#answers): **(1) Is the program well-defined?** It may be well-defined, implementation-defined, unspecified, undefined behavior (UB), or ill-formed. **(2) If it is well-defined, what exactly does it print?** Every answer explains *why*, names the rule, and lists the follow-ups an interviewer is likely to ask. [Section 12](#12-timed-mock-interview-c-cmake-and-testing) then puts it all together in a timed 60-minute mock interview covering C++, CMake, and testing: a warm-up, a code review, follow-up chains, and live coding.

See also: [C++ Fundamentals](../languages/Cpp_Fundamentals.md) · [C++ Fundamentals 15: Undefined Behavior](../languages/Cpp_Fundamentals.md#15-undefined-behavior-implementation-defined-and-best-practices) · [Sanitizers with GoogleTest](../languages/CPP_Testing.md#33-sanitizers-with-googletest) · [Debugging and Profiling Tools](../tools/Debugging_and_Profiling_Tools.md) · [Python Output Quiz](Python_Output_Quiz.md) · [Flashcards](Flashcards.csv)

## Table of Contents

1. [How to Use This Quiz](#1-how-to-use-this-quiz)
2. [Object Model, Inheritance, and Layout](#2-object-model-inheritance-and-layout) (P1-P11)
3. [Initialization, Parsing, and Evaluation Order](#3-initialization-parsing-and-evaluation-order) (P12-P18)
4. [Integers, Characters, and Floating Point](#4-integers-characters-and-floating-point) (P19-P29)
5. [Overload Resolution, Templates, and `constexpr`](#5-overload-resolution-templates-and-constexpr) (P30-P34)
6. [Lifetime, Temporaries, and Dangling](#6-lifetime-temporaries-and-dangling) (P35-P41)
7. [Move Semantics and Copy Elision](#7-move-semantics-and-copy-elision) (P42-P45)
8. [Containers and Iterators](#8-containers-and-iterators) (P46-P50)
9. [Smart Pointers and Exceptions](#9-smart-pointers-and-exceptions) (P51-P53)
10. [Aliasing and the One Definition Rule](#10-aliasing-and-the-one-definition-rule) (P54-P55)
11. [Topic Index](#11-topic-index)
12. [Timed Mock Interview: C++, CMake, and Testing](#12-timed-mock-interview-c-cmake-and-testing)
    - [12.1 Format and Timer Checkpoints](#121-format-and-timer-checkpoints)
    - [12.2 Round A: Rapid-Fire Warm-Up (W1-W15)](#122-round-a-rapid-fire-warm-up-w1-w15)
    - [12.3 Round B: Code Review](#123-round-b-code-review)
    - [12.4 Round C: Follow-Up Chains](#124-round-c-follow-up-chains)
    - [12.5 Round D: Live Coding -- A Scoped Timer Registry](#125-round-d-live-coding----a-scoped-timer-registry)
    - [12.6 Scoring Rubric and Debrief](#126-scoring-rubric-and-debrief)
    - [12.7 Interview Questions](#127-interview-questions)
- [Answers](#answers)
  - [Mock Interview Model Answers](#mock-interview-model-answers)

---

## 1. How to Use This Quiz

- **Classify first, then predict.** In a C++ interview, "it prints 1" is the wrong answer to a UB program, even if it does print 1 on your machine. Say "this is undefined behavior because ...", then explain what a typical compiler might do and how you would detect it (sanitizers, warnings).
- **Know the categories.**
  - *Well-defined*: the standard fixes the result.
  - *Implementation-defined*: the implementation must choose a behavior and document it, for example whether `char` is signed or the value of `sizeof(int)`.
  - *Unspecified*: one of several allowed outcomes, not documented, for example the order in which function arguments are evaluated.
  - *Undefined (UB)*: no requirements at all, and the optimizer may assume it never happens.
  - *Ill-formed, no diagnostic required (NDR)*: the program is broken, but the toolchain is not required to tell you, for example ODR violations.
- **Reproduce it.** Every single-file program builds with `g++ -std=c++20 -Wall p.cpp -o p && ./p`. For the UB puzzles, also try `-O2`, `-fsanitize=address,undefined`, and `-Wextra`. Watching the output change with the optimization level is the best way to understand why UB matters.
- **Warnings.** Several programs deliberately trigger `-Wall` warnings (`-Wreorder`, `-Wvexing-parse`, `-Wsign-compare`, `-Wterminate`, `-Wpessimizing-move`, ...). The answers mention them, because "the compiler warns about this" is a good thing to say in an interview. Ignore `-Wunused-but-set-variable` noise.
- **Scoring.** Count a puzzle as correct only if you get both the classification and the exact output. 45+ is strong. Below 35, re-read [C++ Fundamentals](../languages/Cpp_Fundamentals.md) Parts 1, 4, and 6.

---

## 2. Object Model, Inheritance, and Layout

### P1. Virtual calls from a constructor and destructor

```cpp
#include <iostream>

struct Base {
    Base() { hello(); }
    virtual ~Base() { hello(); }
    virtual void hello() const { std::cout << "Base "; }
};

struct Derived : Base {
    Derived() { hello(); }
    ~Derived() override { hello(); }
    void hello() const override { std::cout << "Derived "; }
};

int main() {
    { Derived d; }
    std::cout << '\n';
}
```

[Answer](#a1-virtual-calls-during-construction-and-destruction)

### P2. A constructor that reaches a pure virtual function

```cpp
#include <iostream>

struct Shape {
    Shape() { init(); }
    void init() { std::cout << area() << '\n'; }
    virtual double area() const = 0;
    virtual ~Shape() = default;
};

struct Square : Shape {
    double side = 2.0;
    double area() const override { return side * side; }
};

int main() {
    Square s;
    std::cout << "done\n";
}
```

[Answer](#a2-a-pure-virtual-call-during-construction)

### P3. Passing a Dog where an Animal is expected

```cpp
#include <iostream>
#include <string>
#include <vector>

struct Animal {
    virtual std::string name() const { return "Animal"; }
    virtual ~Animal() = default;
};
struct Dog : Animal {
    std::string name() const override { return "Dog"; }
};

void byValue(Animal a) { std::cout << a.name() << ' '; }
void byRef(const Animal& a) { std::cout << a.name() << ' '; }

int main() {
    Dog d;
    byValue(d);
    byRef(d);
    std::vector<Animal> zoo;
    zoo.push_back(d);
    std::cout << zoo[0].name() << ' ';
    Animal& r = d;
    Animal copy = r;
    std::cout << copy.name() << '\n';
}
```

[Answer](#a3-object-slicing)

### P4. Assigning through a base reference

```cpp
#include <iostream>

struct B {
    int b = 0;
    virtual ~B() = default;
};
struct D : B {
    int d = 0;
};

int main() {
    D d1, d2;
    d1.b = 1; d1.d = 10;
    d2.b = 2; d2.d = 20;
    B& r = d1;
    r = d2;
    std::cout << d1.b << ' ' << d1.d << '\n';
}
```

[Answer](#a4-partial-assignment-through-a-base-reference)

### P5. Default arguments on an override

```cpp
#include <iostream>

struct Base {
    virtual void f(int x = 1) const { std::cout << "Base " << x << '\n'; }
    virtual ~Base() = default;
};
struct Derived : Base {
    void f(int x = 2) const override { std::cout << "Derived " << x << '\n'; }
};

int main() {
    Derived d;
    Base& b = d;
    b.f();
    d.f();
}
```

[Answer](#a5-default-arguments-are-bound-statically)

### P6. Overloads split across base and derived

```cpp
#include <iostream>

struct Base {
    void f(int) { std::cout << "Base::f(int)\n"; }
    void g(int) { std::cout << "Base::g(int)\n"; }
};
struct Derived : Base {
    void f(double) { std::cout << "Derived::f(double)\n"; }
    using Base::g;
    void g(double) { std::cout << "Derived::g(double)\n"; }
};

int main() {
    Derived d;
    d.f(1);
    d.g(1);
}
```

[Answer](#a6-name-hiding-across-scopes)

### P7. Deleting through a base pointer

```cpp
#include <iostream>
#include <string>

struct Base {
    ~Base() { std::cout << "~Base\n"; }
};
struct Derived : Base {
    std::string payload = "a string long enough to live on the heap";
    ~Derived() { std::cout << "~Derived\n"; }
};

int main() {
    Base* p = new Derived;
    delete p;
}
```

[Answer](#a7-deleting-through-a-base-pointer-without-a-virtual-destructor)

### P8. Which special member function runs?

```cpp
#include <iostream>
#include <utility>

struct T {
    T() { std::cout << "ctor "; }
    T(const T&) { std::cout << "copy-ctor "; }
    T(T&&) noexcept { std::cout << "move-ctor "; }
    T& operator=(const T&) { std::cout << "copy-assign "; return *this; }
    T& operator=(T&&) noexcept { std::cout << "move-assign "; return *this; }
};

int main() {
    T a;
    T b = a;
    T c;
    c = a;
    T d(a);
    T e{std::move(a)};
    e = T{};
    std::cout << '\n';
}
```

[Answer](#a8-copy-initialization-is-construction-not-assignment)

### P9. Member initializer list order

```cpp
#include <iostream>

struct Tracer {
    explicit Tracer(const char* n) { std::cout << n << ' '; }
};

struct S {
    Tracer a;
    Tracer b;
    S() : b("b"), a("a") {}
};

int main() {
    S s;
    std::cout << '\n';
}
```

[Answer](#a9-members-are-initialized-in-declaration-order)

### P10. `sizeof` an empty class

```cpp
#include <iostream>

struct Empty {};
struct Holder { Empty e; int x; };
struct UsesEbo : Empty { int x; };
struct NoUnique { [[no_unique_address]] Empty e; int x; };
struct SameTypeTwice : Empty { Empty e; int x; };

int main() {
    std::cout << sizeof(Empty) << ' '
              << sizeof(Holder) << ' '
              << sizeof(UsesEbo) << ' '
              << sizeof(NoUnique) << ' '
              << sizeof(SameTypeTwice) << '\n';
}
```

[Answer](#a10-empty-classes-and-the-empty-base-optimization-ebo)

### P11. Padding, vptr, and array parameters

```cpp
#include <iostream>

struct A { char c; int i; char d; };
struct B { int i; char c; char d; };
struct V { virtual void f() {} char c; };

void param(int arr[10]) { std::cout << sizeof(arr) << ' '; }

int main() {
    int arr[10];
    std::cout << sizeof(A) << ' ' << sizeof(B) << ' ' << sizeof(V) << ' ';
    param(arr);
    std::cout << sizeof(arr) << '\n';
}
```

[Answer](#a11-padding-vptr-and-array-to-pointer-decay)

---

## 3. Initialization, Parsing, and Evaluation Order

### P12. Constructing a Widget from a Timer

```cpp
#include <iostream>

struct Timer {
    Timer() { std::cout << "Timer() "; }
};
struct Widget {
    explicit Widget(Timer) { std::cout << "Widget(Timer) "; }
};

int main() {
    Widget w(Timer());
    Widget w2{Timer{}};
    std::cout << "done\n";
}
```

[Answer](#a12-the-most-vexing-parse)

### P13. `auto` with braces

```cpp
#include <initializer_list>
#include <iostream>
#include <type_traits>

int main() {
    auto a = {1};
    auto b{1};
    auto c = {1, 2};
    auto d(1);
    std::cout << std::is_same_v<decltype(a), std::initializer_list<int>>
              << std::is_same_v<decltype(b), int>
              << std::is_same_v<decltype(c), std::initializer_list<int>>
              << std::is_same_v<decltype(d), int> << '\n';
}
```

[Answer](#a13-auto-with-braced-initializers)

### P14. Parentheses versus braces with containers

```cpp
#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<int> v1(3, 5);
    std::vector<int> v2{3, 5};
    std::vector<std::string> v3{3, "x"};
    std::string s1(3, 'a');
    std::string s2{3, 'a'};
    std::cout << v1.size() << ' ' << v2.size() << ' ' << v3.size() << ' '
              << s1.size() << ' ' << s2.size() << '\n';
}
```

[Answer](#a14-parentheses-versus-braces-with-initializer_list-constructors)

### P15. Several side effects in one statement

```cpp
#include <iostream>

int main() {
    int i = 0;
    std::cout << i++ << ' ' << i++ << ' ';

    int a[3] = {};
    int j = 0;
    a[j] = j++ + 10;
    std::cout << a[0] << a[1] << ' ';

    int k = 0;
    k = k++ + 1;
    std::cout << k << '\n';
}
```

[Answer](#a15-c17-sequencing-rules)

### P16. Two calls as function arguments

```cpp
#include <iostream>

int counter = 0;
int next() { return ++counter; }
void show(int a, int b) { std::cout << a << ' ' << b << '\n'; }

int main() {
    show(next(), next());
}
```

[Answer](#a16-order-of-evaluation-of-function-arguments)

### P17. Globals and function-local statics

```cpp
#include <iostream>
#include <string>

struct Tracer {
    std::string name;
    explicit Tracer(std::string n) : name(std::move(n)) { std::cout << name << ' '; }
    ~Tracer() { std::cout << '~' << name << ' '; }
};

Tracer global("global");

Tracer& local() {
    static Tracer t("local");
    return t;
}

int main() {
    std::cout << "main ";
    local();
    local();
    std::cout << "end ";
}
```

[Answer](#a17-static-initialization-and-destruction-order)

### P18. Globals in two translation units

Two translation units:

```cpp
// a.cpp
#include <string>
std::string greeting = "hello, this string is longer than the SSO buffer";
```

```cpp
// b.cpp
#include <iostream>
#include <string>

extern std::string greeting;
std::string message = greeting + "!";   // reads another TU's global

int main() {
    std::cout << '[' << message << "]\n";
}
```

Build it twice, once with each link order. What does each build print?

```bash
g++ -std=c++20 -Wall b.cpp a.cpp -o fiasco_ba && ./fiasco_ba
g++ -std=c++20 -Wall a.cpp b.cpp -o fiasco_ab && ./fiasco_ab
```

[Answer](#a18-static-initialization-order-fiasco)

---

## 4. Integers, Characters, and Floating Point

### P19. Mixed signed and unsigned comparisons

```cpp
#include <iostream>
#include <vector>

int main() {
    int i = -1;
    unsigned int u = 1;
    std::cout << (i < u) << ' ';

    short s = -1;
    unsigned short us = 1;
    std::cout << (s < us) << ' ';

    unsigned char a = 200, b = 100;
    std::cout << a + b << ' ';
    unsigned char c = a + b;
    std::cout << int(c) << ' ';

    std::vector<int> v;
    std::cout << (v.size() - 1 > 0) << '\n';
}
```

[Answer](#a19-integer-promotion-and-the-usual-arithmetic-conversions)

### P20. Adding to chars and strings

```cpp
#include <iostream>
#include <string>

int main() {
    std::string s = "id:";
    s += 'a' + 1;
    std::cout << s << ' ';
    s = 65;
    std::cout << s << ' ';
    std::cout << 'a' + 1 << ' ' << "abc" + 1 << '\n';
}
```

[Answer](#a20-char-arithmetic-and-stdstring-assignment-from-an-integer)

### P21. A string literal and an overload set

```cpp
#include <iostream>
#include <string>
#include <variant>

void f(bool) { std::cout << "bool "; }
void f(const std::string&) { std::cout << "string "; }

int main() {
    f("hello");
    f(std::string("hello"));
    using namespace std::string_literals;
    f("hello"s);
    std::variant<bool, std::string> v = "hello";
    std::cout << v.index() << '\n';
}
```

[Answer](#a21-const-char-prefers-bool-over-stdstring)

### P22. Is `char` signed?

```cpp
#include <iostream>

int main() {
    char c = '\xff';
    std::cout << static_cast<int>(c) << ' ' << (c == '\xff') << ' ' << (c < 0) << '\n';
}
```

[Answer](#a22-signedness-of-plain-char)

### P23. Printing fixed-width integers

```cpp
#include <cstdint>
#include <iostream>

int main() {
    std::uint8_t n = 65;
    std::int8_t m = 66;
    std::cout << n << ' ' << +n << ' ' << m << ' ' << static_cast<int>(m) << '\n';
}
```

[Answer](#a23-uint8_t-and-int8_t-are-character-types)

### P24. Negative division, modulo, and shift

```cpp
#include <iostream>

int main() {
    std::cout << -7 / 2 << ' ' << -7 % 2 << ' ' << 7 % -2 << ' ' << (-7 >> 1) << '\n';
}
```

[Answer](#a24-negative-division-modulo-and-right-shift)

### P25. Unsigned arithmetic below zero

```cpp
#include <cstddef>
#include <cstdint>
#include <iostream>

int main() {
    unsigned u = 0;
    --u;
    std::cout << u << ' ';

    std::uint8_t b = 255;
    ++b;
    std::cout << int(b) << ' ';

    std::size_t n = 0;
    std::cout << (n - 1 < 10) << ' ';

    unsigned x = 3, y = 5;
    std::cout << x - y << ' ' << static_cast<int>(x - y) << '\n';
}
```

[Answer](#a25-unsigned-wraparound)

### P26. Checking for overflow after the fact

```cpp
#include <climits>
#include <iostream>

bool plusOneIsBigger(int x) { return x + 1 > x; }

int main() {
    std::cout << plusOneIsBigger(INT_MAX) << '\n';
}
```

[Answer](#a26-signed-overflow-lets-the-optimizer-assume-it-never-happens)

### P27. Shifting negative numbers in C++20

```cpp
#include <iostream>

int main() {
    std::cout << (1 << 31) << ' ' << (-1 >> 1) << ' ' << (-1 << 1) << ' ' << (-8 >> 1) << '\n';
}
```

[Answer](#a27-shifts-of-negative-and-boundary-values-in-c20)

### P28. Shifting by the full width

```cpp
#include <iostream>

int main(int argc, char**) {
    int shift = 31 + argc;          // 32 when run with no arguments
    unsigned x = 1;
    std::cout << (x << shift) << '\n';
}
```

[Answer](#a28-shift-count-greater-than-or-equal-to-the-bit-width)

### P29. Floating-point equality

```cpp
#include <cmath>
#include <iomanip>
#include <iostream>
#include <limits>

int main() {
    double nan = std::numeric_limits<double>::quiet_NaN();
    std::cout << (0.1 + 0.2 == 0.3) << ' '
              << (0.1f + 0.2f == 0.3f) << ' '
              << (0.1f == 0.1) << ' '
              << (nan == nan) << ' '
              << (-0.0 == 0.0) << ' '
              << (1e16 + 1 == 1e16) << '\n';
    std::cout << std::setprecision(17) << 0.1 + 0.2 << '\n';
}
```

[Answer](#a29-floating-point-equality)

---

## 5. Overload Resolution, Templates, and `constexpr`

### P30. `0`, `nullptr`, and `NULL`

```cpp
#include <cstddef>
#include <iostream>

void f(int) { std::cout << "int "; }
void f(char*) { std::cout << "char* "; }

void g(long) { std::cout << "long "; }
void g(char*) { std::cout << "char* "; }

int main() {
    f(0);
    f(nullptr);
    g(NULL);
    std::cout << '\n';
}
```

[Answer](#a30-overloading-on-0-nullptr-and-null)

### P31. Template versus non-template overloads

```cpp
#include <iostream>
#include <string>

void g(double) { std::cout << "g(double) "; }
template <class T> void g(T) { std::cout << "g<T> "; }

void h(const std::string&) { std::cout << "h(const string&) "; }
template <class T> void h(T&&) { std::cout << "h(T&&) "; }

int main() {
    g(1);
    g(1.0);
    std::string s = "x";
    const std::string cs = "y";
    h(s);
    h(cs);
    std::cout << '\n';
}
```

[Answer](#a31-template-versus-non-template-overloads-and-greedy-forwarding-references)

### P32. What does `T` deduce to?

```cpp
#include <iostream>
#include <type_traits>

template <class T> void byVal(T)  { std::cout << sizeof(T) << std::is_const_v<T> << ' '; }
template <class T> void byRef(T&) { std::cout << sizeof(T) << std::is_const_v<T> << ' '; }
template <class T> void fwd(T&&)  { std::cout << std::is_reference_v<T> << ' '; }

int main() {
    const int ci = 1;
    int arr[3] = {};
    byVal(ci);
    byRef(ci);
    byVal(arr);
    byRef(arr);
    byVal("hi");
    byRef("hi");
    fwd(ci);
    fwd(1);
    std::cout << '\n';
}
```

[Answer](#a32-template-argument-deduction-decay-const-and-references)

### P33. A static local in a function template

```cpp
#include <iostream>

template <class T>
int counter() {
    static int n = 0;
    return ++n;
}

int main() {
    std::cout << counter<int>() << counter<int>() << counter<double>()
              << counter<const int>() << counter<int>() << '\n';
}
```

[Answer](#a33-each-template-specialization-has-its-own-statics)

### P34. `std::is_constant_evaluated`

```cpp
#include <iostream>
#include <type_traits>

constexpr int where() { return std::is_constant_evaluated() ? 1 : 2; }

int main() {
    constexpr int a = where();
    int b = where();
    const int c = where();
    static int d = where();
    int e = where() + b;
    std::cout << a << b << c << d << e << '\n';
}
```

[Answer](#a34-stdis_constant_evaluated-and-manifestly-constant-evaluated-contexts)

---

## 6. Lifetime, Temporaries, and Dangling

### P35. Binding temporaries to references

```cpp
#include <iostream>

struct Noisy {
    int v;
    explicit Noisy(int x) : v(x) { std::cout << "ctor" << v << ' '; }
    ~Noisy() { std::cout << "dtor" << v << ' '; }
};

Noisy make(int v) { return Noisy(v); }

int main() {
    const Noisy& r1 = make(1);
    std::cout << "use" << r1.v << ' ';
    Noisy&& r2 = make(2);
    std::cout << "use" << r2.v << ' ';
    make(3);
    std::cout << "end ";
}
```

[Answer](#a35-lifetime-extension-of-temporaries)

### P36. References returned from functions

```cpp
#include <algorithm>
#include <iostream>
#include <string>

const std::string& pick(const std::string& s) { return s; }

int main() {
    const std::string& r = pick(std::string("a temporary long enough to be heap allocated"));
    const int& m = std::max(1, 2);
    std::cout << r << ' ' << m << '\n';
}
```

[Answer](#a36-references-returned-from-functions-do-not-extend-lifetime)

### P37. Range-`for` over a temporary

```cpp
#include <iostream>
#include <vector>

struct Holder {
    std::vector<int> v{1, 2, 3};
    const std::vector<int>& get() const { return v; }
};

Holder make() { return {}; }

int main() {
    for (int x : make().v) std::cout << x << ' ';      // (a)
    std::cout << "| ";
    for (int x : make().get()) std::cout << x << ' ';  // (b)
    std::cout << '\n';
}
```

[Answer](#a37-range-for-over-a-temporary)

### P38. Where does a `string_view` point?

```cpp
#include <iostream>
#include <string>
#include <string_view>

std::string_view firstWord(const std::string& s) {
    return std::string_view(s).substr(0, s.find(' '));
}

int main() {
    std::string_view lit = "a string literal";                      // (a)
    std::string owner = "owned string that lives on";
    std::string_view ok = firstWord(owner);                          // (b)
    std::string_view bad = std::string("temporary string, long enough for the heap");  // (c)
    std::string_view bad2 = firstWord("hello world");               // (d)
    std::cout << lit << '|' << ok << '|' << bad << '|' << bad2 << '\n';
}
```

[Answer](#a38-stdstring_view-outliving-its-buffer)

### P39. A counter factory

```cpp
#include <functional>
#include <iostream>

std::function<int()> makeCounter() {
    int count = 0;
    return [&] { return ++count; };
}

int main() {
    auto next = makeCounter();
    std::cout << next() << ' ' << next() << '\n';
}
```

[Answer](#a39-capturing-a-local-by-reference-in-an-escaping-lambda)

### P40. Copying a mutable lambda

```cpp
#include <iostream>

int main() {
    int x = 1;
    auto byVal = [x]() mutable { return ++x; };
    auto byRef = [&x] { return x; };
    auto copy = byVal;
    byVal();
    byVal();
    x = 10;
    std::cout << x << ' ' << byVal() << ' ' << copy() << ' ' << byRef() << '\n';
}
```

[Answer](#a40-value-captures-mutable-and-copying-closures)

### P41. Structured bindings: copies or references?

```cpp
#include <iostream>
#include <map>
#include <string>
#include <utility>

int main() {
    std::pair<int, std::string> p{1, "one"};
    auto [n, s] = p;
    n = 2; s = "two";
    std::cout << p.first << p.second << ' ';

    auto& [rn, rs] = p;
    rn = 3;
    std::cout << p.first << ' ';

    std::map<int, int> m{{1, 10}};
    for (auto [k, v] : m) v = 99;
    std::cout << m[1] << ' ';
    for (auto& [k, v] : m) v = 99;
    std::cout << m[1] << '\n';
}
```

[Answer](#a41-structured-bindings-copy-unless-you-ask-for-a-reference)

---

## 7. Move Semantics and Copy Elision

### P42. `std::move` on a const object

```cpp
#include <iostream>
#include <string>
#include <utility>

struct S {
    S() = default;
    S(const S&) { std::cout << "copy "; }
    S(S&&) noexcept { std::cout << "move "; }
};

int main() {
    const S a{};
    S b = std::move(a);

    const std::string cs = "a string long enough to be heap allocated";
    std::string t = std::move(cs);
    std::cout << cs.size() << ' ' << t.size() << '\n';
}
```

[Answer](#a42-stdmove-on-a-const-object-copies)

### P43. When does `std::move` move?

```cpp
#include <iostream>
#include <utility>
#include <vector>

void take(std::vector<int>&& v) { std::cout << v.size() << ' '; }

int main() {
    std::vector<int> v{1, 2, 3};
    auto&& r = std::move(v);
    std::cout << v.size() << ' ';
    take(std::move(v));
    std::cout << v.size() << ' ';
    std::vector<int> w = std::move(v);
    std::cout << v.size() << ' ' << w.size() << '\n';
    (void)r;
}
```

[Answer](#a43-stdmove-does-not-move-anything)

### P44. Returning objects from functions

```cpp
#include <iostream>

struct T {
    T() { std::cout << "ctor "; }
    T(const T&) { std::cout << "copy "; }
    T(T&&) noexcept { std::cout << "move "; }
    ~T() { std::cout << "dtor "; }
};

T rvo() { return T{}; }
T nrvo() { T t; return t; }
T either(bool b) {
    T x, y;
    if (b) return x;
    return y;
}

int main() {
    T a = rvo();
    std::cout << "| ";
    T b = nrvo();
    std::cout << "| ";
    T c = either(true);
    std::cout << "| ";
}
```

[Answer](#a44-rvo-nrvo-and-implicit-move)

### P45. `return std::move` and a non-movable type

```cpp
#include <iostream>
#include <utility>

struct T {
    T() { std::cout << "ctor "; }
    T(const T&) { std::cout << "copy "; }
    T(T&&) noexcept { std::cout << "move "; }
};

struct Pinned {
    explicit Pinned(int) { std::cout << "pinned "; }
    Pinned(const Pinned&) = delete;
    Pinned(Pinned&&) = delete;
};

T pessimized() { T t; return std::move(t); }
Pinned makePinned() { return Pinned{42}; }

int main() {
    T a = pessimized();
    Pinned p = makePinned();
    std::cout << '\n';
}
```

[Answer](#a45-return-stdmove-and-returning-non-movable-types)

---

## 8. Containers and Iterators

### P46. `auto` with `vector<bool>`

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<bool> vb{true, false};
    auto x = vb[0];
    x = false;
    std::cout << vb[0] << ' ';

    std::vector<int> vi{1, 0};
    auto y = vi[0];
    y = 0;
    std::cout << vi[0] << '\n';
}
```

[Answer](#a46-vectorbool-returns-a-proxy)

### P47. push_back during range-for

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v{1, 2, 3, 4, 5};
    for (int x : v) {
        if (x == 2) v.push_back(6);
        std::cout << x << ' ';
    }
    std::cout << '\n';
}
```

[Answer](#a47-push_back-while-iterating)

### P48. Erasing inside a for loop

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v{2, 4, 5};
    for (auto it = v.begin(); it != v.end(); ++it) {
        if (*it % 2 == 0) it = v.erase(it);
    }
    for (int x : v) std::cout << x << ' ';
    std::cout << '\n';
}
```

[Answer](#a48-erasing-inside-a-for-loop-skips-elements)

### P49. Looking up keys in a `std::map`

```cpp
#include <cstddef>
#include <iostream>
#include <map>
#include <string>

int main() {
    std::map<std::string, int> m{{"a", 1}};
    if (m["b"] == 0) std::cout << "zero ";
    std::cout << m.size() << ' ';
    std::cout << m.count("c") << ' ' << m.contains("c") << ' ' << m.size() << ' ';

    std::map<std::string, std::size_t> sizes;
    sizes["x"] = sizes.size();
    std::cout << sizes["x"] << '\n';
}
```

[Answer](#a49-stdmapoperator-inserts)

### P50. Vector growth and `noexcept`

```cpp
#include <iostream>
#include <vector>

struct A {
    A() = default;
    A(const A&) { std::cout << "copy "; }
    A(A&&) { std::cout << "move "; }
};
struct B {
    B() = default;
    B(const B&) { std::cout << "copy "; }
    B(B&&) noexcept { std::cout << "move "; }
};

int main() {
    std::vector<A> va;
    va.reserve(1);
    va.emplace_back();
    va.emplace_back();
    std::cout << "| ";
    std::vector<B> vb;
    vb.reserve(1);
    vb.emplace_back();
    vb.emplace_back();
    std::cout << '\n';
}
```

[Answer](#a50-vector-reallocation-copies-unless-the-move-constructor-is-noexcept)

---

## 9. Smart Pointers and Exceptions

### P51. Two nodes pointing at each other

```cpp
#include <iostream>
#include <memory>
#include <string>

struct Node {
    std::string name;
    std::shared_ptr<Node> next;
    std::weak_ptr<Node> prev;
    explicit Node(std::string n) : name(std::move(n)) {}
    ~Node() { std::cout << '~' << name << ' '; }
};

int main() {
    {
        auto a = std::make_shared<Node>("a");
        auto b = std::make_shared<Node>("b");
        a->next = b;
        b->next = a;
        std::cout << a.use_count() << ' ';
    }
    std::cout << "| ";
    {
        auto c = std::make_shared<Node>("c");
        auto d = std::make_shared<Node>("d");
        c->next = d;
        d->prev = c;
        std::cout << c.use_count() << ' ';
    }
    std::cout << "| end\n";
}
```

[Answer](#a51-shared_ptr-cycles-leak-weak_ptr-breaks-them)

### P52. Throwing from a destructor

```cpp
#include <iostream>
#include <stdexcept>

struct Bad {
    ~Bad() { throw std::runtime_error("boom"); }
};

int main() {
    try {
        Bad b;
    } catch (const std::exception& e) {
        std::cout << "caught " << e.what() << '\n';
    }
    std::cout << "after\n";
}
```

[Answer](#a52-throwing-out-of-an-implicitly-noexcept-destructor)

### P53. `noexcept(false)` destructors and unwinding

```cpp
#include <exception>
#include <iostream>
#include <stdexcept>

struct Loud {
    ~Loud() noexcept(false) {
        if (std::uncaught_exceptions() > 0) std::cout << "unwinding" << std::endl;
        throw std::runtime_error("from dtor");
    }
};

int main() {
    try {
        Loud l;
    } catch (const std::exception& e) {
        std::cout << "caught: " << e.what() << std::endl;
    }
    try {
        Loud l;
        throw std::runtime_error("original");
    } catch (const std::exception& e) {
        std::cout << "caught: " << e.what() << std::endl;
    }
}
```

[Answer](#a53-a-second-exception-during-stack-unwinding)

---

## 10. Aliasing and the One Definition Rule

### P54. Writing an `int` through a `float*`

```cpp
#include <iostream>

int store(int* i, float* f) {
    *i = 1;
    *f = 0.0f;
    return *i;
}

int main() {
    int x = 0;
    std::cout << store(&x, reinterpret_cast<float*>(&x)) << '\n';
}
```

[Answer](#a54-strict-aliasing)

### P55. Two definitions of an inline function

Two translation units:

```cpp
// a.cpp
inline int value() { return 1; }
int fromA() { return value(); }
```

```cpp
// b.cpp
#include <iostream>
inline int value() { return 2; }
int fromA();

int main() {
    std::cout << value() << fromA() << '\n';
}
```

What does it print at `-O0` and at `-O2`, and does the link order matter?

```bash
g++ -std=c++20 -Wall -O0 a.cpp b.cpp -o odr && ./odr
g++ -std=c++20 -Wall -O0 b.cpp a.cpp -o odr && ./odr
g++ -std=c++20 -Wall -O2 a.cpp b.cpp -o odr && ./odr
```

[Answer](#a55-one-definition-rule-violation)

---

## 11. Topic Index

Spoiler warning: this table names the concept each puzzle tests.

| # | Concept | Read more |
|---|---|---|
| [P1](#p1-virtual-calls-from-a-constructor-and-destructor) | Virtual calls during construction and destruction | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#48-virtual-function-table-vtable-internals) |
| [P2](#p2-a-constructor-that-reaches-a-pure-virtual-function) | A pure virtual call during construction | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#49-abstract-classes-and-pure-virtual-functions) |
| [P3](#p3-passing-a-dog-where-an-animal-is-expected) | Object slicing | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#47-polymorphism) |
| [P4](#p4-assigning-through-a-base-reference) | Partial assignment through a base reference | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#44-copy-semantics) |
| [P5](#p5-default-arguments-on-an-override) | Default arguments are bound statically | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#47-polymorphism) |
| [P6](#p6-overloads-split-across-base-and-derived) | Name hiding across scopes | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#46-inheritance) |
| [P7](#p7-deleting-through-a-base-pointer) | Deleting through a base pointer without a virtual destructor | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#virtual-destructors) |
| [P8](#p8-which-special-member-function-runs) | Copy-initialization is construction, not assignment | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#44-copy-semantics) |
| [P9](#p9-member-initializer-list-order) | Members are initialized in declaration order | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#member-initializer-list) |
| [P10](#p10-sizeof-an-empty-class) | Empty classes and the empty base optimization (EBO) | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#4-object-oriented-programming) |
| [P11](#p11-padding-vptr-and-array-parameters) | Padding, vptr, and array-to-pointer decay | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#48-virtual-function-table-vtable-internals) |
| [P12](#p12-constructing-a-widget-from-a-timer) | The most vexing parse | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#94-uniform-initialization-brace-initialization) |
| [P13](#p13-auto-with-braces) | `auto` with braced initializers | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#91-auto-and-decltype) |
| [P14](#p14-parentheses-versus-braces-with-containers) | Parentheses versus braces with `initializer_list` constructors | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#99-stdinitializer_list) |
| [P15](#p15-several-side-effects-in-one-statement) | C++17 sequencing rules | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#158-evaluation-order-c17) |
| [P16](#p16-two-calls-as-function-arguments) | Order of evaluation of function arguments | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#158-evaluation-order-c17) |
| [P17](#p17-globals-and-function-local-statics) | Static initialization and destruction order | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#154-object-lifetime-and-storage-duration) |
| [P18](#p18-globals-in-two-translation-units) | Static initialization order fiasco | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#117-consteval-and-constinit) |
| [P19](#p19-mixed-signed-and-unsigned-comparisons) | Integer promotion and the usual arithmetic conversions | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#11-fundamental-types) |
| [P20](#p20-adding-to-chars-and-strings) | `char` arithmetic and `std::string` assignment from an integer | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#14-type-casting) |
| [P21](#p21-a-string-literal-and-an-overload-set) | `const char*` prefers `bool` over `std::string` | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#14-type-casting) |
| [P22](#p22-is-char-signed) | Signedness of plain `char` | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#151-categories-of-behavior) |
| [P23](#p23-printing-fixed-width-integers) | `uint8_t` and `int8_t` are character types | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#11-fundamental-types) |
| [P24](#p24-negative-division-modulo-and-shift) | Negative division, modulo, and right shift | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#11-fundamental-types) |
| [P25](#p25-unsigned-arithmetic-below-zero) | Unsigned wraparound | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#152-common-sources-of-undefined-behavior) |
| [P26](#p26-checking-for-overflow-after-the-fact) | Signed overflow lets the optimizer assume it never happens | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#152-common-sources-of-undefined-behavior) |
| [P27](#p27-shifting-negative-numbers-in-c20) | Shifts of negative and boundary values in C++20 | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#152-common-sources-of-undefined-behavior) |
| [P28](#p28-shifting-by-the-full-width) | Shift count greater than or equal to the bit width | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#152-common-sources-of-undefined-behavior) |
| [P29](#p29-floating-point-equality) | Floating-point equality | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#11-fundamental-types) |
| [P30](#p30-0-nullptr-and-null) | Overloading on `0`, `nullptr`, and `NULL` | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#null-pointers-nullptr-vs-null-vs-0) |
| [P31](#p31-template-versus-non-template-overloads) | Template versus non-template overloads, and greedy forwarding references | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#6-templates) |
| [P32](#p32-what-does-t-deduce-to) | Template argument deduction: decay, const, and references | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#6-templates) |
| [P33](#p33-a-static-local-in-a-function-template) | Each template specialization has its own statics | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#6-templates) |
| [P34](#p34-stdis_constant_evaluated) | `std::is_constant_evaluated` and manifestly constant-evaluated contexts | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#117-consteval-and-constinit) |
| [P35](#p35-binding-temporaries-to-references) | Lifetime extension of temporaries | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#154-object-lifetime-and-storage-duration) |
| [P36](#p36-references-returned-from-functions) | References returned from functions do not extend lifetime | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#154-object-lifetime-and-storage-duration) |
| [P37](#p37-range-for-over-a-temporary) | Range-`for` over a temporary | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#92-range-based-for-loop) |
| [P38](#p38-where-does-a-string_view-point) | `std::string_view` outliving its buffer | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#106-stdstring_view) |
| [P39](#p39-a-counter-factory) | Capturing a local by reference in an escaping lambda | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#84-lambda-expressions) |
| [P40](#p40-copying-a-mutable-lambda) | Value captures, mutable, and copying closures | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#84-lambda-expressions) |
| [P41](#p41-structured-bindings-copies-or-references) | Structured bindings copy unless you ask for a reference | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#101-structured-bindings) |
| [P42](#p42-stdmove-on-a-const-object) | `std::move` on a const object copies | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#5-move-semantics-and-perfect-forwarding) |
| [P43](#p43-when-does-stdmove-move) | `std::move` does not move anything | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#5-move-semantics-and-perfect-forwarding) |
| [P44](#p44-returning-objects-from-functions) | RVO, NRVO, and implicit move | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#5-move-semantics-and-perfect-forwarding) |
| [P45](#p45-return-stdmove-and-a-non-movable-type) | `return std::move`, and returning non-movable types | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#5-move-semantics-and-perfect-forwarding) |
| [P46](#p46-auto-with-vectorbool) | `vector<bool>` returns a proxy | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#72-sequence-containers) |
| [P47](#p47-push_back-during-range-for) | push_back while iterating | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#82-iterator-invalidation-rules) |
| [P48](#p48-erasing-inside-a-for-loop) | Erasing inside a for loop skips elements | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#82-iterator-invalidation-rules) |
| [P49](#p49-looking-up-keys-in-a-stdmap) | `std::map::operator[]` inserts | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#73-associative-containers-ordered) |
| [P50](#p50-vector-growth-and-noexcept) | `vector` reallocation copies unless the move constructor is `noexcept` | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#144-noexcept) |
| [P51](#p51-two-nodes-pointing-at-each-other) | `shared_ptr` cycles leak; `weak_ptr` breaks them | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#34-smart-pointers) |
| [P52](#p52-throwing-from-a-destructor) | Throwing out of an implicitly `noexcept` destructor | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#144-noexcept) |
| [P53](#p53-noexceptfalse-destructors-and-unwinding) | A second exception during stack unwinding | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#14-exception-handling-and-error-management) |
| [P54](#p54-writing-an-int-through-a-float) | Strict aliasing | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#153-strict-aliasing-rule) |
| [P55](#p55-two-definitions-of-an-inline-function) | One Definition Rule violation | [Cpp_Fundamentals](../languages/Cpp_Fundamentals.md#132-translation-units-and-the-one-definition-rule-odr) |

---

## 12. Timed Mock Interview: C++, CMake, and Testing

Sections 2-10 test whether you can *read* C++. This section tests whether you can *talk* about C++, CMake, and testing for 60 minutes under a clock, the way a systems C++ or GPU tooling loop does it: a rapid-fire warm-up, a code review, two "and then what?" follow-up chains, and a short live-coding exercise with tests. It plays the same role for C++ that [HLD Mock Interviews](HLD_Mock_Interviews.md) plays for system design and [CS Fundamentals Drills, Part 4](CS_Fundamentals_Drills.md#4-follow-up-drill-chains) plays for OS and networking. All model answers are in [Mock Interview Model Answers](#mock-interview-model-answers).

See also: [C++ Fundamentals: Common Interview Questions -- Compilation and Best Practices](../languages/Cpp_Fundamentals.md#common-interview-questions----compilation-and-best-practices) · [C++ Testing 39: Interview Questions and Answers](../languages/CPP_Testing.md#39-interview-questions-and-answers) · [CMake 72: Interview Questions and Answers](../tools/CMake_Fundamentals.md#72-interview-questions-and-answers) · [Debugging and Profiling Tools 21](../tools/Debugging_and_Profiling_Tools.md#21-cross-cutting-interview-questions) · [Project Deep Dive: rocprof-compute](../career/Project_Deep_Dive_rocprof-compute.md)

### 12.1 Format and Timer Checkpoints

Run the mock alone with a timer and a voice recorder, or with a partner who reads the questions and the model answers. Answer **out loud**. Silent "I know this" does not count, because the skill being trained is a clear spoken explanation under time pressure.

| Clock | Round | What you do | Pass signal |
|---|---|---|---|
| 0:00-0:08 | **A. Warm-up** ([12.2](#122-round-a-rapid-fire-warm-up-w1-w15)) | 15 one-liners in random order, about 30 s each | 12/15 correct, each with the *why* in one sentence |
| 0:08-0:20 | **B. Code review** ([12.3](#123-round-b-code-review)) | 7 min on the C++ program, 5 min on the `CMakeLists.txt`. List defects, rank by severity, propose fixes | At least 5 C++ and 7 CMake findings, the top 3 of each ranked correctly |
| 0:20-0:45 | **C. Follow-up chains** ([12.4](#124-round-c-follow-up-chains)) | Two chains picked at random, about 12 min each. Go as deep as the clock allows | Reach level 6+ of each chain without a factual error |
| 0:45-1:00 | **D. Live coding** ([12.5](#125-round-d-live-coding----a-scoped-timer-registry)) | Implement a scoped timer registry and its GoogleTest tests in a plain editor | Compiles on the first try after the timer, all tests pass, TSan clean |
| 1:00-1:10 | Debrief ([12.6](#126-scoring-rubric-and-debrief)) | Score yourself, log every miss | An error log entry for each miss |

**Rules.**
- No compiler, documentation, or search during Rounds A-C. In Round D, write the code in a plain editor; compile and run it only after the 15 minutes are up, then count the compile errors.
- When you are unsure, say so and reason toward an answer ("I believe `FILE_SET` arrived in 3.23; I'd check the docs before relying on it"). The rubric rewards calibrated uncertainty and penalizes confident errors.
- Partner mode: the partner may interrupt with "why?" or "how would you check that?" at any point. Those interruptions are the most realistic part of the mock.

The randomizer picks the warm-up order and the two chains. Pass a seed to replay the same mock later:

```python
import random
import sys

CHAINS = [
    "M1 Designing an owning device buffer",
    "M2 Green at -O0, red at -O2 in CI",
    "M3 Works in build/, broken after install",
    "M4 Testing a profiler's analysis pipeline",
    "M5 A header change rebuilds everything",
]

seed = int(sys.argv[1]) if len(sys.argv) > 1 else None
rng = random.Random(seed)
warmups = rng.sample(range(1, 16), 15)          # all 15 warm-ups, shuffled
chains = rng.sample(CHAINS, 2)                  # 2 of the 5 chains
print("Warm-up order:", " ".join(f"W{i}" for i in warmups))
print("Chains:", " | ".join(chains))
```

### 12.2 Round A: Rapid-Fire Warm-Up (W1-W15)

Answer each in one or two sentences, and always include the *reason*. Answers: [Round A Answers](#round-a-answers-warm-up).

| # | Question |
|---|---|
| W1 | What does `std::move` actually do at runtime? |
| W2 | Why should a move constructor be `noexcept`? Name the standard library code path that cares. |
| W3 | On x86-64 Linux with libstdc++, what are `sizeof(std::unique_ptr<int>)`, `sizeof(std::shared_ptr<int>)`, and `sizeof(std::unique_ptr<int, void(*)(int*)>)`? Why? |
| W4 | Define a data race in standard C++ terms. What does the standard say about a program that has one? |
| W5 | Why can `std::map::operator[]` not be called on a `const` map, and what silent bug does it cause in lookups? |
| W6 | `ASSERT_EQ` versus `EXPECT_EQ`: what is the difference, and why does `ASSERT_*` not compile in a function that returns `int`? |
| W7 | Stub, fake, and mock: one sentence each, with an example from a GPU profiler. |
| W8 | Can you build one binary with both ASan and TSan? What do you do in CI instead? |
| W9 | `PUBLIC`, `PRIVATE`, and `INTERFACE` in `target_link_libraries`: what does each propagate? |
| W10 | Why is `file(GLOB SRCS src/*.cpp)` discouraged, and what does `CONFIGURE_DEPENDS` change? |
| W11 | Why does `if(CMAKE_BUILD_TYPE STREQUAL "Debug")` silently do nothing with Visual Studio or Ninja Multi-Config, and what do you write instead? |
| W12 | `gtest_discover_tests` versus `add_test(NAME all COMMAND unit_tests)`: what changes for `ctest`? |
| W13 | What does the keyword `inline` mean for a function in modern C++? |
| W14 | `DT_RPATH` versus `DT_RUNPATH` in one sentence each. Which one does your linker emit by default? |
| W15 | What does building a shared library with `-fvisibility=hidden` buy you? |

### 12.3 Round B: Code Review

You are reviewing a pull request. Find the defects, **rank them by severity** (crash or UB > wrong results > maintainability), and propose a fix for each. Say which tool or test would have caught each one. Answers: [Round B Answers](#round-b-answers-code-review).

**B1. C++ (7 minutes).** It compiles with `g++ -std=c++20 -Wall -pthread` and prints plausible output. Target: at least 5 findings.

```cpp
// Code-review exercise: compiles with g++ -std=c++20 -Wall -pthread, but has deliberate bugs.
#include <iostream>
#include <map>
#include <string>
#include <string_view>
#include <thread>
#include <vector>

struct Sample {
    std::string kernel;
    double duration_us;
};

class KernelStats {
public:
    void add(const Sample& s) {
        totals_[s.kernel] += s.duration_us;
        if (s.duration_us > slowest_us_) {
            slowest_us_ = s.duration_us;
            slowest_ = s.kernel;
        }
    }
    std::string_view slowest() const { return slowest_; }
    double total(const std::string& kernel) { return totals_[kernel]; }

private:
    std::map<std::string, double> totals_;
    std::string_view slowest_;
    double slowest_us_;
};

int main() {
    std::vector<Sample> samples;
    for (int i = 0; i < 1000; ++i)
        samples.push_back({"gemm_" + std::to_string(i % 4), i * 0.5});

    KernelStats stats;
    std::vector<std::thread> workers;
    for (int t = 0; t < 4; ++t)
        workers.emplace_back([&] {
            for (int i = t; i < samples.size(); i += 4) stats.add(samples[i]);
        });
    for (auto& w : workers) w.join();

    samples.clear();
    std::cout << "slowest: " << stats.slowest() << '\n';
    std::cout << "gemm_9 total: " << stats.total("gemm_9") << '\n';
}
```

**B2. CMake (5 minutes).** The project is a shared library `kstats` that will be installed and consumed by other projects with `find_package(kstats)`. It configures without errors on CMake 4.2. Target: at least 7 findings.

```cmake
# Code-review exercise: configures with CMake 4.2, but contains deliberate defects.
cmake_minimum_required(VERSION 3.10)
project(kstats)

set(CMAKE_CXX_FLAGS "-std=c++17 -O2 -Wall")
include_directories(${CMAKE_SOURCE_DIR}/include)
include_directories(/opt/rocm/include)
link_directories(/opt/rocm/lib)

file(GLOB SRCS src/*.cpp)
add_library(kstats SHARED ${SRCS})
target_link_libraries(kstats pthread amdhip64)

if(CMAKE_BUILD_TYPE STREQUAL "Debug")
  target_compile_definitions(kstats PUBLIC KSTATS_DEBUG)
endif()

add_executable(kstats_test test/test_stats.cpp)
target_link_libraries(kstats_test kstats gtest gtest_main)
add_test(kstats_test kstats_test)

install(TARGETS kstats DESTINATION lib)
```

### 12.4 Round C: Follow-Up Chains

Each chain opens with a broad question and then drills down. Indented items are the follow-ups an interviewer asks after your previous answer. Answer each level completely before moving on, and expect "how would you check that?" at any level. Model answers: [Round C Answers](#round-c-answers-follow-up-chains).

#### Chain M1: Designing an Owning Device Buffer

> Theory: [C++ 4.5 Rule of Zero/Three/Five](../languages/Cpp_Fundamentals.md#45-the-rule-of-zero--three--five) · [C++ 5.2 Move Constructor and Move Assignment](../languages/Cpp_Fundamentals.md#52-move-constructor-and-move-assignment) · [C++ 16.1 `UniquePtr<T>`](../languages/Cpp_Fundamentals.md#161-uniqueptrt-exclusive-ownership) · [C++ 16.2 `SharedPtr<T>`](../languages/Cpp_Fundamentals.md#162-sharedptrt-and-weakptrt-control-block-and-atomic-reference-counts)

- **M1.1** Design a `DeviceBuffer` class that owns memory from `hipMalloc`. Which special member functions do you write, and which do you delete?
  - **M1.2** Write the move constructor. What state is the moved-from object in, and what may a caller still do with it?
  - **M1.3** Why must the move constructor be `noexcept`? What exactly happens in `std::vector<DeviceBuffer>::push_back` growth if it is not, given that copying is deleted?
  - **M1.4** Write the move assignment operator. What about self-move-assignment?
  - **M1.5** `hipFree` returns an error code. The destructor cannot return it. What do you do?
  - **M1.6** Could you skip the hand-written class and use `std::unique_ptr` with a custom deleter? What does the choice of deleter type do to `sizeof`?
  - **M1.7** Two streams need to share one buffer and the last user frees it. `shared_ptr`? What does it cost, and what is the aliasing constructor good for here?
  - **M1.8** Kernels need a non-owning view. Design it. What goes wrong if the view outlives the buffer, and what must be true of a type passed to a kernel by value?
  - **M1.9** How do you test that the class never leaks or double-frees device memory, given that host ASan cannot see it?

#### Chain M2: Green at -O0, Red at -O2 in CI

> Theory: [C++ 15.2 Common Sources of Undefined Behavior](../languages/Cpp_Fundamentals.md#152-common-sources-of-undefined-behavior) · [C++ Testing 33 Sanitizers](../languages/CPP_Testing.md#33-sanitizers-with-googletest) · [C++ Testing 40 Testing Concurrent Code](../languages/CPP_Testing.md#40-testing-concurrent-code) · [Debugging 18 Scientific Debugging and Bisecting](../tools/Debugging_and_Profiling_Tools.md#18-scientific-debugging-and-bisecting)

- **M2.1** A unit test passes on your laptop in a Debug build and fails in CI, which builds Release. What are your first three steps?
  - **M2.2** List the kinds of bugs whose symptoms change with the optimization level, and say why each one does.
  - **M2.3** Which tool catches which kind? Be specific about what each one cannot see.
  - **M2.4** The failure happens about once in 50 runs. How do you make it reproducible?
  - **M2.5** `--gtest_shuffle` makes it fail every time with one particular seed. What does that tell you, and what are the usual causes?
  - **M2.6** The bug appeared sometime in the last 300 commits. How do you find the commit without reading them?
  - **M2.7** It turns out to be an `EXPECT_EQ` on a `double` computed by a reduction. Why did it pass at `-O0` and fail at `-O2`, and how should the test compare?
  - **M2.8** What do you change in CI so this class of bug is caught before merge next time?

#### Chain M3: Works in build/, Broken After Install

> Theory: [CMake 65 RPATH and RUNPATH](../tools/CMake_Fundamentals.md#65-rpath-and-runpath) · [CMake 38 Exporting Targets](../tools/CMake_Fundamentals.md#38-exporting-targets-and-generating-config-files) · [C++ 13.11 Symbol Visibility](../languages/Cpp_Fundamentals.md#1311-symbol-visibility-and-export-control) · [C++ 13.13 ABI and the Dual ABI](../languages/Cpp_Fundamentals.md#1313-abi-stability-and-the-libstdc-dual-abi)

- **M3.1** `./build/kstats_cli` runs. After `cmake --install build --prefix /opt/kstats`, running `/opt/kstats/bin/kstats_cli` fails with `libkstats.so.1: cannot open shared object file`. Why?
  - **M3.2** Fix it so the install tree can be moved anywhere. Where in the `CMakeLists.txt` must the fix go?
  - **M3.3** Which commands do you run to confirm the diagnosis instead of guessing?
  - **M3.4** A user sets `LD_LIBRARY_PATH` to an old ROCm and your tool loads the wrong `libamdhip64`. Explain the search order. Why does the answer depend on RPATH versus RUNPATH?
  - **M3.5** A downstream project's `find_package(kstats REQUIRED)` fails with "Could not find a package configuration file". What must your project install, and how does the consumer point CMake at it?
  - **M3.6** Now `find_package` succeeds, but configuring the consumer fails with `Imported target "kstats::kstats" includes non-existent path "/home/me/kstats/include"`. Why?
  - **M3.7** The consumer links and gets `undefined reference to kstats::Collector::start(std::string const&)`, although `nm` shows a `start` symbol in your library. Give four possible causes and the command that tells them apart.
  - **M3.8** `kstats` links `Threads::Threads` and the consumer now fails with "The link interface of target "kstats::kstats" contains: Threads::Threads but the target was not found." Fix it.
  - **M3.9** What do `libkstats.so`, `libkstats.so.1`, and `libkstats.so.1.2.0` each exist for? When do you bump the SOVERSION?

#### Chain M4: Testing a Profiler's Analysis Pipeline

> Theory: [C++ Testing 37 Designing for Testability](../languages/CPP_Testing.md#37-designing-for-testability) · [C++ Testing 41 Testing GPU / HIP Code](../languages/CPP_Testing.md#41-testing-gpu--hip-code) · [C++ Testing 42 Golden-File Testing](../languages/CPP_Testing.md#42-golden-file-snapshot-and-approval-testing) · [C++ Testing 43 Microbenchmarking](../languages/CPP_Testing.md#43-microbenchmarking-with-google-benchmark)

- **M4.1** Your tool collects GPU hardware counters, derives metrics such as achieved HBM bandwidth and VALU utilization, and writes CSV reports. How do you structure its test suite?
  - **M4.2** How do you unit-test the metric derivation on a CI machine with no GPU?
  - **M4.3** The derived metrics are `double`s. How do you compare them, and why does a purely relative tolerance fail?
  - **M4.4** How do you golden-file test the CSV report when it contains timestamps, PIDs, absolute paths, and GPU names?
  - **M4.5** Some tests need a real GPU. How do you keep them from failing on CPU-only runners, and from oversubscribing a 2-GPU runner under `ctest -j16`?
  - **M4.6** Write the test plan for one HIP kernel the tool injects. Which inputs and checks do you include?
  - **M4.7** A change made the tool's per-kernel overhead 10% worse and nobody noticed for a month. How do you catch that automatically, and why not just time a test in CI?
  - **M4.8** Your manager says "we have 92% line coverage, so testing is done." How do you respond?

#### Chain M5: A Header Change Rebuilds Everything

> Theory: [C++ 13.1 Compilation Pipeline](../languages/Cpp_Fundamentals.md#131-the-c-compilation-pipeline) · [CMake 26 Compiler Caches](../tools/CMake_Fundamentals.md#26-compiler-caches-ccache-and-sccache) · [C++ 11.4 Modules](../languages/Cpp_Fundamentals.md#114-modules)

- **M5.1** Touching `common/types.hpp` rebuilds 1,800 translation units, which takes 20 minutes. Why, and how do you find the headers that hurt most?
  - **M5.2** Which source-level techniques cut the coupling?
  - **M5.3** Explain pimpl. What does it buy, what does it cost, and what is the classic compile error when combining it with `std::unique_ptr`?
  - **M5.4** Which build-system-level levers help, and what is the pitfall of each?
  - **M5.5** After all that, the *link* takes 90 seconds on every change. What now?
  - **M5.6** Would C++20 modules fix this? What is the state of support in CMake?
  - **M5.7** How do you stop build times from regressing again?

### 12.5 Round D: Live Coding -- A Scoped Timer Registry

**Prompt (read aloud, then start the 15-minute timer).** Implement, in one header:

1. `TimerRegistry`: thread-safe; `record(name, duration)` accumulates per-name **count**, **total**, and **max**; `snapshot()` returns a consistent copy of all stats.
2. `ScopedTimer`: an RAII object that measures the time from its construction to its destruction and records it under a name.
3. The clock must be **injectable**, so tests are deterministic.
4. Write GoogleTest tests: count, total, and max over two scopes; nested scopes; a scope exited by an exception; exact counts with 8 threads.
5. Write a `CMakeLists.txt` that fetches GoogleTest and registers the tests with CTest.

Say your design choices out loud as you go: clock type, lock granularity, what the destructor does if recording fails, and copy/move semantics of `ScopedTimer`.

**Follow-ups the interviewer asks once the code works** (answers in [Round D Answers](#round-d-answers-live-coding-model-solution)):

- **D1.** What does one `ScopedTimer` cost, and how would you cut that cost to a few nanoseconds for a timer that fires millions of times per second?
- **D2.** Why `steady_clock` and not `system_clock` or `high_resolution_clock`?
- **D3.** Why does the destructor contain a `try`/`catch`?
- **D4.** Should a scope that exits by exception be recorded? How would you tag it?
- **D5.** You add a global registry `TimerRegistry& timers()`. What can go wrong at program exit, and how do you avoid it?
- **D6.** Someone wraps a HIP kernel launch in a `ScopedTimer`. What does the number mean?
- **D7.** The 8-thread test passes. Does that prove the registry is race-free?
- **D8.** Why is `ScopedTimer` non-copyable, and what would it take to make it movable?

### 12.6 Scoring Rubric and Debrief

Score each dimension from 1 to 4 right after the mock, before you read the model answers, then re-score after reading them. The gap between the two scores is your calibration error.

| Dimension | 1: Below bar | 2: Borderline | 3: Hire | 4: Strong hire (senior) |
|---|---|---|---|---|
| **Correctness** | States UB programs' "output"; wrong facts stated confidently | Mostly right, some confident errors | Right, and says "UB" or "implementation-defined" precisely | Right, and names the rule, the exact failure mode, and an edge case |
| **Depth (the why)** | Recites rules | Explains one level down | Explains mechanisms: `move_if_noexcept`, the loader search order, why `-O2` exposes UB | Connects mechanisms across layers (ABI, linker, build system, test infra) |
| **Tooling** | "I'd add prints" | Names a tool | Picks the right tool per bug class and knows its blind spots | Gives exact commands (`readelf -d`, `LD_DEBUG=libs`, `ctest --repeat until-fail:200`, `git bisect run`) |
| **Code (Round D)** | Does not compile, or races | Compiles, misses an edge (destructor throwing, injectable clock) | Correct, tested, TSan clean | Also discusses overhead, the global-registry lifetime, and GPU timing semantics unprompted |
| **Testing mindset** | No tests or only the happy path | Happy path plus one edge | Deterministic tests (fake clock, seeds), right comparisons for floats | Test pyramid, golden files, perf gating, and what coverage does not tell you |
| **Communication** | Silent, or rambles | Answers, but unstructured | Structured: claim, mechanism, example, tradeoff | Also drives: proposes what to check next and asks clarifying questions |

**Debrief checklist.**
- For every warm-up answer you missed or hedged, write a flashcard (see [Flashcards](Flashcards.csv)).
- For every chain level where you stalled, note the level number and the missing fact in an error log, together with the deep-dive link from the chain header. Re-run the same seed after one week; the stall should be gone.
- For Round D, count compile errors and test failures on the first build. More than two compile errors means you need more practice writing C++ without an IDE.
- If most of your Round B C++ misses were concurrency bugs, do [Concurrency Coding Problems](../computer-science/Concurrency_Coding_Problems.md) before the next mock.

### 12.7 Interview Questions

**Q1.** In a code-review round, how do you structure what you say so that you do not just list issues in reading order?

Do a fast pass for the bug classes that matter most, in this order: **lifetime and ownership** (dangling views, captured references, raw `new`), **concurrency** (shared mutable state, captures, joins), **undefined behavior** (uninitialized reads, overflow, aliasing), **correctness of the API** (`const`, accidental insertion, error reporting), then **maintainability**. Then *report* by severity, not by line number: "The two crash-class bugs are X and Y; then a wrong-result bug Z; then cleanups." For each one, name the tool or test that would have caught it (TSan, ASan, `-Wall -Werror`, a unit test). That turns a list into a review and shows you think about preventing the next bug, not only this one.

**Q2.** The interviewer asks about a CMake feature and you are not sure which version introduced it. What do you say?

Give the mechanism, then hedge the version honestly: "`FetchContent_Declare` can try `find_package` first with `FIND_PACKAGE_ARGS`; I believe that arrived in 3.24, so I would set `cmake_minimum_required` to at least that and confirm in the release notes." Interviewers care that you know version floors exist and that `cmake_minimum_required` controls policies, not that you memorized every release. A confident wrong number is worse than a calibrated guess.

**Q3.** You are asked "what does this print?" about a program in which 4 threads each increment a plain `int` counter 1000 times without synchronization. The interviewer pushes: "but in practice it prints 4000, right?" How do you answer?

Hold the line on the classification and then be practical: "It's undefined behavior, so the standard places no requirement on it. On x86 with GCC at `-O0` it will probably print a number at or below 4000, because increments are lost when two threads read the same old value. At `-O2`, GCC 15 collapses each thread's loop into a single non-atomic `addl $1000` to memory, so it usually prints 4000, but a lost update would now drop a whole 1000. Either way the number tells you nothing about correctness. TSan reports the race deterministically, which is how I'd prove it, and the fix is `std::atomic<int>` or per-thread counts summed after `join`." That shows you know the standard *and* the hardware, and that you do not confuse "observed once" with "defined".

**Q4.** Round D has no compiler. How do you avoid compile errors and still demonstrate testing?

Write the includes first, from the types you plan to use. Keep signatures simple (`std::chrono::nanoseconds` rather than templates on `Duration`). Use `std::lock_guard` with CTAD so you do not mistype template arguments. Compile in your head at the end of each function: return types, `const` on accessors, `mutable` on the mutex. Write the tests *as* the specification. Even without running them, a test named `RecordsEvenWhenScopeExitsByException` shows you thought about that case. Finally, say what you would run: "I'd build this with `-fsanitize=thread` and run the contention test 100 times."

**Q5.** How do you bring your own work (for example, rocprof-compute) into these answers without sounding rehearsed?

Use it as **evidence for a claim you just made**, in one or two sentences, then return to the question. For example, in Chain M4 the shape is: claim ("golden-file the analysis CSVs, but compare numeric columns with a tolerance"), then one sentence of evidence from your own work ("on rocprof-compute, ..." followed by a real incident where a textual diff or a missing tolerance caused trouble), then back to the question. Use a real incident you can defend under follow-up questions; never invent one. Do not open with the project. Let the interviewer pull on it, and keep the full story in [Project Deep Dive: rocprof-compute](../career/Project_Deep_Dive_rocprof-compute.md) for when they do.

---

## Answers

### A1. Virtual calls during construction and destruction

[Back to P1](#p1-virtual-calls-from-a-constructor-and-destructor) · **Verdict:** Well-defined.

```text
Base Derived Derived Base
```

**Why.** While `Base::Base()` runs, the `Derived` part of the object does not exist yet, so the object's dynamic type is `Base`. Inside a constructor or destructor, a virtual call resolves to the class whose constructor or destructor is running, not to the most-derived override. If the call dispatched to `Derived::hello()`, it could read `Derived` members that have not been constructed yet.

Mechanically, on the Itanium ABI (GCC/Clang), each constructor stores its own class's vtable pointer in the object after the base constructors return. The order is:

1. `Base()` sets vptr = Base vtable, then prints `Base`.
2. `Derived()` sets vptr = Derived vtable, then prints `Derived`.
3. `~Derived()` body runs with vptr = Derived vtable and prints `Derived`.
4. `~Base()` resets vptr = Base vtable and prints `Base`.

**Follow-ups.**
- *How do you get derived-specific behavior during construction?* Use a factory function that constructs the object and then calls `init()`. Alternatively, pass the information up to the base constructor as an argument, or use CRTP so the base knows the derived type at compile time.
- `typeid(*this)` and `dynamic_cast` inside a constructor follow the same rule. They see the class that is currently being constructed.

### A2. A pure virtual call during construction

[Back to P2](#p2-a-constructor-that-reaches-a-pure-virtual-function) · **Verdict:** Undefined behavior.

The standard says that a virtual call to a pure virtual function from a constructor or destructor of an abstract class is **undefined behavior** ([class.abstract]). Do not predict an output. Here is what GCC 15 actually did:

```text
pure virtual method called
terminate called without an active exception
```

Both lines go to stderr, then the process aborts with exit status 134, so `done` is never printed.

**Why.** `init()` is an ordinary member function, so the compiler cannot see that it runs during construction. It makes a normal virtual call through the vptr. At that moment the vptr points to `Shape`'s vtable, and that slot holds `__cxa_pure_virtual`, a runtime stub that prints the message and calls `std::terminate`.

If the constructor calls `area()` **directly**, GCC treats it as a non-virtual call to `Shape::area`. It warns `pure virtual ... called from constructor`, and the build then fails at link time with `undefined reference to Shape::area()`. The indirect call through a helper is the dangerous version, because nothing catches it at build time.

**Follow-up.** A pure virtual function *can* have a definition (`double Shape::area() const { ... }` outside the class). A qualified call `Shape::area()` then works. A virtual call during construction is still UB.

### A3. Object slicing

[Back to P3](#p3-passing-a-dog-where-an-animal-is-expected) · **Verdict:** Well-defined.

```text
Animal Dog Animal Animal
```

**Why.** Each of `byValue(d)`, `zoo.push_back(d)`, and `Animal copy = r` runs `Animal`'s copy constructor on the `Animal` subobject of `d`. The new object really is an `Animal`, and its vptr points to `Animal`'s vtable. The `Dog` part is "sliced off". Only `byRef` keeps the original object, so only `byRef` dispatches to `Dog::name`. Copying through a reference (`Animal copy = r`) still slices, because the declared type of `copy` decides what gets constructed.

**Fixes and follow-ups.**
- Pass polymorphic objects by reference or pointer. Store them as `std::vector<std::unique_ptr<Animal>>`.
- C++ Core Guidelines C.67: a polymorphic class should suppress public copy and move. If you delete or protect the copy operations, slicing becomes a compile error.
- If you need copies, add `virtual std::unique_ptr<Animal> clone() const`.

### A4. Partial assignment through a base reference

[Back to P4](#p4-assigning-through-a-base-reference) · **Verdict:** Well-defined.

```text
2 10
```

**Why.** `r = d2` calls `B::operator=(const B&)`. That operator is chosen from the static type `B`, and the implicitly generated one is not virtual. It copies only the `B` subobject. `d1` ends up with `b` from `d2` and `d` from its old self, which is a mixed state that no constructor ever produced. This is the assignment version of slicing.

Making `operator=` virtual does not really fix it. The override would have to take `const B&`, so it still cannot safely copy `D`'s fields. The fix is the same as in the previous puzzle: make copy assignment on polymorphic bases deleted or `protected`.

### A5. Default arguments are bound statically

[Back to P5](#p5-default-arguments-on-an-override) · **Verdict:** Well-defined.

```text
Derived 1
Derived 2
```

**Why.** The function body is chosen **at run time** from the dynamic type, but default arguments are filled in **at compile time** from the static type of the call expression. `b.f()` has static type `Base&`, so the compiler rewrites it as `b.f(1)`, and the call still goes to `Derived::f`. `d.f()` has static type `Derived`, so it becomes `d.f(2)`.

**Guideline.** Never redefine default arguments in an override (Effective C++, Item 37). clang-tidy's `google-default-arguments` check flags default arguments on virtual functions. A clean pattern is the Non-Virtual Interface (NVI): a public non-virtual function holds the defaults and forwards to a private virtual function.

### A6. Name hiding across scopes

[Back to P6](#p6-overloads-split-across-base-and-derived) · **Verdict:** Well-defined.

```text
Derived::f(double)
Base::g(int)
```

**Why.** Name lookup happens before overload resolution. It stops at the first scope that declares the name. `Derived` declares `f`, so lookup never reaches `Base::f(int)`. The only candidate is `f(double)`, and `1` converts to `double`. For `g`, the declaration `using Base::g;` brings `Base::g(int)` into `Derived`'s scope, so both overloads are candidates and the exact match `g(int)` wins.

**Follow-up.** The same trap applies to virtual overload sets. If you override only `f(int)` out of `f(int)` and `f(double)`, then `d.f(1.5)` silently calls `f(int)`. GCC's `-Woverloaded-virtual=2` warns about this. The default level enabled by `-Wall` is narrower.

### A7. Deleting through a base pointer without a virtual destructor

[Back to P7](#p7-deleting-through-a-base-pointer) · **Verdict:** Undefined behavior.

`delete p` where `p` has static type `Base*`, the object is a `Derived`, and `Base` has no virtual destructor is **undefined behavior** ([expr.delete]). GCC printed only:

```text
~Base
```

`~Derived` did not run, so `payload`'s heap buffer leaked. The wrong size was also passed to sized `operator delete`. AddressSanitizer reports `new-delete-type-mismatch` with "size of the allocated type: 32 bytes; size of the deallocated type: 1 bytes".

**Fixes.**
- `virtual ~Base() = default;` if the class is meant to be deleted polymorphically.
- A `protected` non-virtual destructor if it is not, so `delete p` does not compile.

**Follow-up.** `std::shared_ptr<Base> p = std::make_shared<Derived>();` destroys the object correctly even without a virtual destructor, because the control block records the deleter for `Derived`. `std::unique_ptr<Base>` does not; it calls `delete` on a `Base*`.

### A8. Copy-initialization is construction, not assignment

[Back to P8](#p8-which-special-member-function-runs) · **Verdict:** Well-defined.

```text
ctor copy-ctor ctor copy-assign copy-ctor move-ctor ctor move-assign
```

**Why.**
- `T b = a;` declares a new object, so it is copy-*initialization* and calls the copy **constructor**. The `=` does not mean assignment here.
- `c = a;` assigns to an object that already exists, so it calls copy assignment.
- `T d(a);` uses the copy constructor.
- `T e{std::move(a)};` uses the move constructor.
- `e = T{};` first creates the temporary (`ctor`), then move-assigns from it because the temporary is an rvalue.

(The `-Wunused-but-set-variable` warning for `b` is noise.)

### A9. Members are initialized in declaration order

[Back to P9](#p9-member-initializer-list-order) · **Verdict:** Well-defined.

```text
a b
```

**Why.** Non-static members are initialized in the order they are **declared** in the class. The order of the mem-initializer list does not matter. `-Wreorder` (part of `-Wall`) warns when the two orders differ. Destruction runs in reverse declaration order (`b`, then `a`). Base classes are initialized before members, virtual bases first, and then the direct bases in the order they appear in the base-specifier list.

**The dangerous variant.** `struct S { int a; int b; S(int x) : b(x), a(b + 1) {} };` reads `b` before it is initialized, which is UB because it reads an indeterminate value. Always write initializer lists in declaration order, and never make one member's initializer depend on a member declared later.

### A10. Empty classes and the empty base optimization (EBO)

[Back to P10](#p10-sizeof-an-empty-class) · **Verdict:** Implementation-specific sizes (Itanium ABI shown).

```text
1 8 4 4 8
```

**Why.**
- `sizeof(Empty) == 1`. Every complete object needs a size of at least 1 so that two distinct objects have distinct addresses.
- `Holder`: an `Empty` *member* takes 1 byte, then 3 bytes of padding, then the `int`, for 8 bytes total.
- `UsesEbo`: an empty *base* may take zero bytes. This is the **empty base optimization (EBO)**, so the size is 4.
- `NoUnique`: since C++20, `[[no_unique_address]]` lets a member overlap other members, so the size is 4. MSVC ignores the standard attribute; use `[[msvc::no_unique_address]]` there.
- `SameTypeTwice`: two subobjects of the **same type** must have different addresses. The base `Empty` sits at offset 0, so the member `e` moves to offset 1, `x` to offset 4, and the size is 8.

**Where it matters.** EBO is why `sizeof(std::unique_ptr<T>) == sizeof(T*)` with the default deleter. Standard containers also use it to store stateless allocators and comparators for free.

### A11. Padding, vptr, and array-to-pointer decay

[Back to P11](#p11-padding-vptr-and-array-parameters) · **Verdict:** Implementation-specific sizes (LP64 shown).

```text
12 8 16 8 40
```

**Why.**
- `A`: `c` at offset 0, 3 bytes of padding, `i` at 4, `d` at 8, then 3 bytes of tail padding. The size must be a multiple of `alignof(A) == 4`, so it is 12.
- `B`: `i` at 0, `c` at 4, `d` at 5, then 2 bytes of padding, for 8. Ordering members from largest to smallest alignment removes most padding.
- `V`: the vptr takes 8 bytes at offset 0, `c` sits at 8, then 7 bytes of padding, for 16. Any class with a virtual function pays for one pointer per object (more with multiple inheritance).
- `param(int arr[10])`: the parameter is really an `int*`, so `sizeof(arr)` is 8. GCC warns with `-Wsizeof-array-argument`. The real array in `main` is 40 bytes.

**Follow-ups.** Pass arrays as `std::span<int>` or as `int (&a)[N]` in a template, and use `std::size`. `offsetof` and `alignof` let you check layouts with `static_assert`. Padding in hot structs wastes cache lines (see [Performance Engineering](../computer-science/Performance_Engineering.md)).

### A12. The most vexing parse

[Back to P12](#p12-constructing-a-widget-from-a-timer) · **Verdict:** Well-defined.

```text
Timer() Widget(Timer) done
```

**Why.** `Widget w(Timer());` is parsed as a **function declaration**. It declares a function `w` that returns `Widget` and takes one parameter: a pointer to a function that takes nothing and returns `Timer`. The rule is that anything that can be parsed as a declaration is a declaration. Nothing is constructed, so that line prints nothing. GCC warns with `-Wvexing-parse` (on by default). The next line, `Widget w2{Timer{}};`, uses braces, which cannot be parsed as a declaration, so it constructs both objects.

**Fixes.** Use brace initialization (`Widget w{Timer{}}`), extra parentheses (`Widget w((Timer()))`), or `auto w = Widget(Timer());`. The simplest form of the trap is `Timer t();`, which declares a function and does not create a `Timer`.

### A13. `auto` with braced initializers

[Back to P13](#p13-auto-with-braces) · **Verdict:** Well-defined.

```text
1111
```

**Why (C++17 rules, from N3922):**

| Declaration | Deduced type |
|---|---|
| `auto a = {1};` | `std::initializer_list<int>` (copy-list-init) |
| `auto b{1};` | `int` (direct-list-init, single element) |
| `auto c = {1, 2};` | `std::initializer_list<int>` |
| `auto d(1);` | `int` |
| `auto e{1, 2};` | ill-formed |
| `auto f = {1, 2.0};` | ill-formed (elements have different types) |

C++11/14 as published deduced `initializer_list<int>` for `auto b{1}`. Compilers apply N3922 retroactively.

**Follow-up.** Template deduction does **not** deduce `initializer_list`. With `template<class T> void f(T); f({1, 2});` the call fails to compile. That is the one place where `auto` deduction and template deduction differ. A lambda also cannot `return {1, 2};` with a deduced return type.

### A14. Parentheses versus braces with `initializer_list` constructors

[Back to P14](#p14-parentheses-versus-braces-with-containers) · **Verdict:** Well-defined.

```text
3 2 3 3 2
```

**Why.** Brace initialization strongly prefers an `initializer_list` constructor whenever one is viable.

- `v1(3, 5)` uses the (count, value) constructor and holds three 5s.
- `v2{3, 5}` uses the initializer_list constructor and holds two elements, 3 and 5.
- `v3{3, "x"}`: `initializer_list<std::string>` is not viable because `3` does not convert to `std::string`. Overload resolution falls back to (count, value) and creates three `"x"`.
- `s1(3, 'a')` is `"aaa"`.
- `s2{3, 'a'}` is `initializer_list<char>{'\x03', 'a'}`, so its size is 2.

**Pitfall.** Generic code that writes `T{args...}` and generic code that writes `T(args...)` can construct different things. That is why `std::make_unique` and `emplace_back` use parentheses. C++20 also allows aggregates to be initialized with parentheses.

### A15. C++17 sequencing rules

[Back to P15](#p15-several-side-effects-in-one-statement) · **Verdict:** Well-defined since C++17 (UB before).

```text
0 1 010 1
```

**Why.** P0145 (C++17) added sequencing guarantees:

- `E1 << E2` and `E1 >> E2`, including overloaded ones: E1 is sequenced before E2. The `cout` chain is evaluated left to right, so it prints `0` and then `1`.
- `E1 = E2` and compound assignments: E2 is sequenced before E1. In `a[j] = j++ + 10`, the right side runs first: it yields 10 and sets `j` to 1. Then `a[j]` refers to `a[1]`, so `a` becomes `{0, 10, 0}` and the program prints `010`.
- `k = k++ + 1`: the right side, including the increment, finishes before the assignment. Its value is `0 + 1`, so `k` ends up as 1.
- Also sequenced since C++17: `E1[E2]` and the left operand of `.*` and `->*`.

Before C++17, all three statements were UB because they modified the same scalar twice without sequencing. GCC's `-Wsequence-point` still warns "may be undefined" even with `-std=c++20`; the warning is conservative here.

See [Cpp_Fundamentals 15.8 Evaluation Order](../languages/Cpp_Fundamentals.md#158-evaluation-order-c17).

### A16. Order of evaluation of function arguments

[Back to P16](#p16-two-calls-as-function-arguments) · **Verdict:** Unspecified (not UB).

GCC 15 on x86-64 printed:

```text
2 1
```

**Why.** The order in which function arguments are evaluated is **unspecified**. C++17 made them *indeterminately sequenced*: each argument is evaluated completely, with no interleaving, but in any order. GCC often evaluates right to left, and Clang usually evaluates left to right, so the same program can print `1 2` with another compiler. The result is not UB, but code that depends on it is non-portable.

**Fix.** Evaluate the arguments into named locals first.

**Classic follow-up.** Before C++17, `f(std::unique_ptr<T>(new T), g())` could leak. The compiler was allowed to run `new T`, then `g()` (which throws), and only then construct the `unique_ptr`. C++17 forbids that interleaving, but `std::make_unique` is still the idiomatic fix.

### A17. Static initialization and destruction order

[Back to P17](#p17-globals-and-function-local-statics) · **Verdict:** Well-defined.

```text
global main local end ~local ~global
```

(There is no trailing newline, because the destructors print after `main` returns.)

**Why.**
- Globals with dynamic initialization in one translation unit are initialized before `main` (in practice), in definition order.
- A function-local `static` is initialized the first time control passes through its declaration, and only once. Since C++11 this initialization is thread-safe ("magic statics"). The second `local()` call prints nothing.
- Objects with static storage are destroyed in **reverse order of completed construction**. `local` finished constructing after `global`, so it is destroyed first.

**Follow-up.** A destructor of one static that uses another static that has already been destroyed is the *static destruction order fiasco*. A common workaround is a deliberately leaked singleton: `static T& t = *new T;`.

### A18. Static initialization order fiasco

[Back to P18](#p18-globals-in-two-translation-units) · **Verdict:** Unspecified order, so UB here.

The order of dynamic initialization of globals in **different translation units** is unspecified. If `message` is initialized first, it reads `greeting` before `greeting`'s constructor has run, and that is UB. GCC 15 with GNU ld runs the initializers in link order:

```text
$ g++ -std=c++20 b.cpp a.cpp && ./a.out
[!]
$ g++ -std=c++20 a.cpp b.cpp && ./a.out
[hello, this string is longer than the SSO buffer!]
```

In the first build, `greeting` was still zero-initialized storage, not a constructed `std::string`. With libstdc++ that storage happens to look like an empty string, so the program printed `[!]` instead of crashing. Another library or another build could crash.

**Fixes.**
- *Construct on first use*: `const std::string& greeting() { static const std::string s = "..."; return s; }`.
- Make the dependency constant-initialized. Constant initialization happens before any dynamic initialization, for example `constexpr std::string_view greeting = "...";`. C++20 `constinit` makes the compiler reject the code if the variable is not constant-initialized.
- Avoid non-trivial globals altogether. Clang's `-Wglobal-constructors` flags them.

### A19. Integer promotion and the usual arithmetic conversions

[Back to P19](#p19-mixed-signed-and-unsigned-comparisons) · **Verdict:** Well-defined.

```text
0 1 300 44 1
```

**Why.**
- `i < u`: `int` and `unsigned int` have the same rank, so the `int` is converted to `unsigned`. -1 becomes 4294967295, and `4294967295 < 1` is false. `-Wsign-compare` (in `-Wall` for C++) warns.
- `s < us`: `short` and `unsigned short` are first **promoted to `int`** because all their values fit in an `int`. Then `-1 < 1` is true.
- `a + b`: both `unsigned char` values are promoted to `int`, so the sum is 300 and does not wrap.
- `unsigned char c = a + b;` converts 300 to unsigned modulo 256, which gives 44. This is well-defined.
- `v.size() - 1` is `size_t(0) - 1 == SIZE_MAX`, which is greater than 0.

**Fixes.** C++20's `std::cmp_less(i, u)` compares by mathematical value and returns true here. Use `std::ssize(v)` for signed sizes, and enable `-Wsign-compare` and `-Wconversion`.

### A20. `char` arithmetic and `std::string` assignment from an integer

[Back to P20](#p20-adding-to-chars-and-strings) · **Verdict:** Well-defined.

```text
id:b A 98 bc
```

**Why.**
- `'a' + 1` is an `int` (98) because `char` promotes. `s += 98` picks `operator+=(char)`, converts 98 back to `char`, and appends `'b'`.
- `s = 65;` compiles. `std::string::operator=(char)` accepts the `int` through an implicit conversion and replaces the contents with `"A"`. This is a well-known trap: `s = 3.7;` compiles too.
- Streaming `'a' + 1` prints the `int` 98.
- `"abc" + 1` is pointer arithmetic on the decayed `const char*`, so it prints `"bc"`. Clang warns with `-Wstring-plus-int`; GCC does not.

### A21. `const char*` prefers `bool` over `std::string`

[Back to P21](#p21-a-string-literal-and-an-overload-set) · **Verdict:** Well-defined.

```text
bool string string 1
```

**Why.** `"hello"` decays to `const char*`. Converting a pointer to `bool` is a *standard* conversion. Converting it to `std::string` is a *user-defined* conversion through a constructor. Any standard conversion sequence beats any user-defined one, so `f(bool)` wins. Passing a real `std::string` (or a `"hello"s` literal) is an exact match for `f(const std::string&)`.

**Variant follow-up.** In C++17 as first published, `std::variant<bool, std::string> v = "hello";` chose `bool` for the same reason. P0608R3 and P1957R2 changed the converting constructor so that it rejects narrowing and pointer-to-bool conversions. Current libstdc++ therefore picks `std::string`, which is index 1.

**Fix.** Add an overload for `const char*` or `std::string_view`, or make the `bool` overload a template constrained to exactly `bool`.

### A22. Signedness of plain `char`

[Back to P22](#p22-is-char-signed) · **Verdict:** Implementation-defined.

On x86-64 Linux (GCC):

```text
-1 1 1
```

On AArch64 **Linux**, PowerPC, and other ABIs where plain `char` is unsigned, the same program prints `255 1 0`. Apple arm64 and Windows keep `char` signed.

**Why.** `char`, `signed char`, and `unsigned char` are three distinct types, and whether plain `char` is signed is up to the ABI. `c == '\xff'` is true either way, because both sides have the same type and promote the same way. GCC lets you override the default with `-funsigned-char` or `-fsigned-char`.

**Real bugs this causes.**
- `table[c]` with a negative index.
- `std::isalpha(c)` with a negative `c` other than EOF is UB. Cast to `unsigned char` first.
- Hashing or checksum code that gives different results on x86 and ARM.
- Mishandled UTF-8 bytes that are 0x80 or higher.

### A23. `uint8_t` and `int8_t` are character types

[Back to P23](#p23-printing-fixed-width-integers) · **Verdict:** Well-defined (given the usual typedefs).

```text
A 65 B 66
```

**Why.** On all mainstream platforms, `std::uint8_t` is a typedef for `unsigned char` and `std::int8_t` for `signed char`. `operator<<` has overloads for both that print a **character**. Unary `+` promotes to `int`, so `+n` prints the number.

**Follow-ups.**
- `std::cin >> u8` reads one character, not a number.
- `std::format("{}", n)` prints `65`, because `std::format` formats `signed char` and `unsigned char` as integers and only `char` as a character.

### A24. Negative division, modulo, and right shift

[Back to P24](#p24-negative-division-modulo-and-shift) · **Verdict:** Well-defined (C++11 for `/` and `%`, C++20 for `>>`).

```text
-3 -1 1 -4
```

**Why.**
- Since C++11, integer division **truncates toward zero**, and `(a/b)*b + a%b == a` always holds. So `-7 / 2 == -3`, and the remainder takes the sign of the dividend: `-7 % 2 == -1`, `7 % -2 == 1`.
- `-7 >> 1`: C++20 defines right shift of a negative number as an arithmetic shift, which rounds toward negative infinity. The result is -4, not -3. Before C++20 it was implementation-defined, although every mainstream compiler already did this.

**Pitfalls.**
- `x % 2 == 1` is false for negative odd numbers. Use `x % 2 != 0`.
- `hash % buckets` with a signed negative hash gives a negative index.
- Python rounds down instead (`-7 // 2 == -4`, `-7 % 2 == 1`). See the [Python Output Quiz](Python_Output_Quiz.md).

### A25. Unsigned wraparound

[Back to P25](#p25-unsigned-arithmetic-below-zero) · **Verdict:** Well-defined.

```text
4294967295 0 0 4294967294 -2
```

**Why.** Unsigned arithmetic is defined as arithmetic **modulo 2^N**.
- `--u` from 0 gives `UINT_MAX`.
- `++b` on `uint8_t`: `b` promotes to `int` 256, and converting back to `uint8_t` wraps to 0.
- `n - 1` is `SIZE_MAX`, which is not less than 10.
- `x - y` is 2^32 - 2. Converting it to `int` gives -2. C++20 defines that conversion as modular; before C++20 the result was implementation-defined, but every compiler gave -2.

**The classic bug.** `for (std::size_t i = v.size() - 1; i >= 0; --i)` never ends, and it starts at a huge `i` when `v` is empty. `-Wextra` (`-Wtype-limits`) flags `i >= 0` as always true. The idiomatic reverse loop is `for (std::size_t i = v.size(); i-- > 0; )`.

### A26. Signed overflow lets the optimizer assume it never happens

[Back to P26](#p26-checking-for-overflow-after-the-fact) · **Verdict:** Undefined behavior.

Signed integer overflow is **UB**, so the program has no defined output. GCC 15 printed `1` at both `-O0` and `-O2`. It folded `x + 1 > x` to `true` because, with no overflow allowed, that comparison is always true. Some other compiler or flag set could print `0`.

**Why compilers exploit this.** It lets them widen loop induction variables (`for (int i = 0; i < n; ++i) a[i]` can use a 64-bit index without wrap checks) and simplify comparisons. C++20 made two's complement the required *representation*, but overflow is still UB.

**Fixes.**
- Test before the operation: `x < INT_MAX` or `x > INT_MAX - y`.
- Use `__builtin_add_overflow(x, 1, &r)` (GCC/Clang). C++26 adds saturating `std::add_sat`.
- Use unsigned types when you want wrapping, or GCC's `-fwrapv`.
- `-fsanitize=undefined` catches overflow that actually happens at run time. In this program the comparison was removed at compile time, so there was nothing left for UBSan to report.

### A27. Shifts of negative and boundary values in C++20

[Back to P27](#p27-shifting-negative-numbers-in-c20) · **Verdict:** Well-defined since C++20.

```text
-2147483648 -1 -2 -4
```

**Why.** C++20 (P0907/P1236) requires two's complement and redefines the shift operators:

| Expression | C++20 | Before C++20 |
|---|---|---|
| `1 << 31` | `INT_MIN` (result is congruent to 2^31 mod 2^32) | UB in C++11; C++14 allowed it (implementation-defined result) |
| `-1 << 1` | -2 | UB (negative left operand) |
| `-1 >> 1` | -1 (arithmetic shift) | implementation-defined |
| `-8 >> 1` | -4 | implementation-defined |

Still UB in C++20: a negative shift count, or a count greater than or equal to the bit width (see the next puzzle).

### A28. Shift count greater than or equal to the bit width

[Back to P28](#p28-shifting-by-the-full-width) · **Verdict:** Undefined behavior.

Shifting a 32-bit `unsigned` by 32 is **UB**, even though unsigned arithmetic otherwise wraps. GCC 15 on x86-64 printed `1` at `-O0` and at `-O2`. The x86 `SHL` instruction masks the count to 5 bits, so 32 acts like 0. 32-bit ARM (A32) uses the low 8 bits of the count, so it would give 0. AArch64, like x86, reduces the count modulo the register width, so it would also give 1. Because real hardware disagrees, the standard makes it UB rather than defining a wraparound rule. If the count is a compile-time constant, the optimizer can produce anything. UBSan reports it:

```text
shift_ub.cpp:6:21: runtime error: shift exponent 32 is too large for 32-bit type 'unsigned int'
```

**Fixes.** Guard the shift (`s >= 32 ? 0u : x << s`), widen to 64-bit, or use `std::rotl`/`std::rotr` when you want a rotate. This bug often shows up in bitmask code like `(1u << nbits) - 1` when `nbits == 32`.

### A29. Floating-point equality

[Back to P29](#p29-floating-point-equality) · **Verdict:** Well-defined (IEEE 754 binary32/binary64).

```text
0 1 0 0 1 1
0.30000000000000004
```

**Why.**
- `0.1 + 0.2 == 0.3` is false. Neither 0.1 nor 0.2 is exactly representable in binary. Their `double` sum rounds to 0.3000000000000000444, while `0.3` is stored as 0.2999999999999999889.
- In `float`, the rounding happens to land on the same value as `0.3f`, so the comparison is true. That is luck, not a rule.
- `0.1f == 0.1` is false. The `float` is promoted to `double`, but it has already lost the extra bits.
- `NaN == NaN` is false. NaN compares unequal to everything, itself included. Use `std::isnan`.
- `-0.0 == 0.0` is true, but `std::signbit` differs and `1.0 / -0.0` is `-inf`.
- `1e16 + 1 == 1e16` is true. A `double` has a 53-bit significand, so adjacent doubles near 1e16 are 2 apart. Adding 1 is an exact tie, and ties round to even, which is back to 1e16.

**How to compare.** Combine an absolute and a relative tolerance: `std::fabs(a - b) <= std::max(abs_eps, rel_eps * std::max(std::fabs(a), std::fabs(b)))`. You can also compare by ULP distance. In GPU and HPC code, floating-point addition is not associative. A parallel reduction can differ from a serial one in the last bits, and so can FMA contraction (`-ffp-contract`). `-ffast-math` lets the compiler assume no NaNs, which can break `std::isnan` checks. When you compare GPU and CPU results in tests, use tolerances.

### A30. Overloading on `0`, `nullptr`, and `NULL`

[Back to P30](#p30-0-nullptr-and-null) · **Verdict:** Well-defined (with GCC's `NULL`).

```text
int char* long
```

**Why.**
- `f(0)`: the literal `0` has type `int`, so `f(int)` is an exact match. The null pointer conversion to `char*` ranks lower.
- `f(nullptr)`: `std::nullptr_t` converts only to pointer types, so `f(char*)` is the only candidate.
- `g(NULL)`: in GCC, `NULL` is `__null`, a null pointer constant with an integer type (`long` on LP64). `g(long)` is an exact match. GCC warns `passing NULL to non-pointer argument` (`-Wconversion-null`).

Two related calls fail to compile with GCC 15: `f(NULL)` with overloads `f(int)` and `f(char*)` is **ambiguous**, and so is `f(0L)`. In both cases `long` to `int` and null-pointer to `char*` are both "Conversion" rank.

**Lessons.** The type of `NULL` is implementation-defined (`0`, `0L`, or `__null`), so always use `nullptr`. Also, perfect forwarding loses the "null pointer constant" property of `0` or `NULL`: `std::make_shared<T>(NULL)` forwards an integer. `nullptr` survives forwarding because its type is `std::nullptr_t`.

### A31. Template versus non-template overloads, and greedy forwarding references

[Back to P31](#p31-template-versus-non-template-overloads) · **Verdict:** Well-defined.

```text
g<T> g(double) h(T&&) h(const string&)
```

**Why.** Overload resolution compares conversion sequences first. "Prefer the non-template" is only a **tie-breaker**.
- `g(1)`: `g<int>(int)` is an exact match, which beats the int-to-double conversion, so the template wins.
- `g(1.0)`: both candidates are exact matches, so the tie-breaker picks the non-template.
- `h(s)` with a non-const lvalue: the template deduces `T = std::string&`, giving a `std::string&` parameter. Binding to that needs no added `const`, so it beats `const std::string&` and the template wins.
- `h(cs)`: the template deduces `const std::string&`, which ties with the non-template, so the non-template wins.

**Interview follow-up.** This is why a constructor like `template<class T> Person(T&&)` hijacks copying from a non-const `Person` lvalue (Effective Modern C++, Item 26). Constrain it with `requires (!std::is_same_v<std::remove_cvref_t<T>, Person>)`.

### A32. Template argument deduction: decay, const, and references

[Back to P32](#p32-what-does-t-deduce-to) · **Verdict:** Well-defined.

```text
40 41 80 120 80 31 1 0
```

Each pair below is `sizeof(T)` followed by `is_const_v<T>`.

| Call | Deduced `T` | Output |
|---|---|---|
| `byVal(ci)` | `int` (top-level const dropped) | `40` |
| `byRef(ci)` | `const int` (const kept behind a reference) | `41` |
| `byVal(arr)` | `int*` (array decays) | `80` |
| `byRef(arr)` | `int[3]` (no decay) | `120` |
| `byVal("hi")` | `const char*` (the pointer itself is not const) | `80` |
| `byRef("hi")` | `const char[3]` (includes the `'\0'`) | `31` |
| `fwd(ci)` | `const int&` (lvalue, so reference collapsing) | `1` |
| `fwd(1)` | `int` (rvalue) | `0` |

**Follow-ups.**
- `auto` follows the by-value rules: `auto x = ci;` gives `int`, and `auto& y = ci;` gives `const int&`.
- `template<class T> T maxOf(T, T); maxOf(1, 2.0)` fails to compile, because the two arguments deduce conflicting types for `T`. Fix it with `maxOf<double>(1, 2.0)` or with two template parameters and `std::common_type_t`.
- `template<std::size_t N> void f(int (&)[N])` is how you keep an array's length.

### A33. Each template specialization has its own statics

[Back to P33](#p33-a-static-local-in-a-function-template) · **Verdict:** Well-defined.

```text
12113
```

**Why.** `counter<int>`, `counter<double>`, and `counter<const int>` are three different functions, and each has its own `static int n`. `const int` is a distinct template argument from `int`. The calls run left to right, which C++17 guarantees for `<<`: int gives 1, int gives 2, double gives 1, const int gives 1, int gives 3.

**Follow-up.** Within one program, a template's static is shared across translation units. The definitions have vague linkage and the linker merges them. Across **shared libraries** loaded with `RTLD_LOCAL` or built with hidden visibility, you can end up with one copy per library. That causes "two singletons" bugs in plugin architectures. Class-template static data members behave the same way.

### A34. `std::is_constant_evaluated` and manifestly constant-evaluated contexts

[Back to P34](#p34-stdis_constant_evaluated) · **Verdict:** Well-defined.

```text
12114
```

**Why.** `std::is_constant_evaluated()` returns true only when the evaluation is *manifestly constant-evaluated*. It does not report whether the compiler happened to fold the expression.
- `constexpr int a`: the initializer must be a constant expression, so `a` is 1.
- `int b`: an ordinary runtime initialization, so `b` is 2, even though the optimizer could fold it.
- `const int c`: a const integral variable with a constant initializer is usable in constant expressions, so the initializer is first tried as a constant expression. `c` is 1, which surprises many people.
- `static int d`: static storage, and the initializer qualifies for constant initialization, so `d` is 1.
- `int e = where() + b`: `b` is not a constant, so the whole expression runs at run time. `where()` returns 2, and `e` is 4.

**Pitfalls and related keywords.**
- `if constexpr (std::is_constant_evaluated())` is always true, and GCC warns about it. C++23's `if consteval` avoids the mistake.
- `consteval` forces compile-time evaluation. `constinit` requires static initialization without making the variable const.
- Constant evaluation must diagnose core-language UB. `constexpr int x = INT_MAX + 1;` is a compile error, so `static_assert` on a `constexpr` test can serve as a UB detector.

### A35. Lifetime extension of temporaries

[Back to P35](#p35-binding-temporaries-to-references) · **Verdict:** Well-defined.

```text
ctor1 use1 ctor2 use2 ctor3 dtor3 end dtor2 dtor1
```

**Why.**
- Binding a prvalue **directly** to a `const T&` or `T&&` local extends the temporary's lifetime to match the reference.
- `make(3)` is not bound to anything, so its temporary dies at the end of that full-expression.
- At the end of scope, extended temporaries are destroyed in reverse order: `dtor2`, then `dtor1`.
- Since C++17, `make(1)` returns a prvalue that is materialized only once, so no copies occur.

**Extension applies to:** direct binding, including through member access (`const int& x = make(1).v;` keeps the whole temporary alive), parentheses, and a conditional expression whose result is a prvalue.

**Extension does NOT apply to:**
- A reference returned from a function (next puzzle).
- A temporary bound to a function parameter. It lives until the end of the full-expression.
- A temporary bound to a reference member in a constructor's mem-initializer list. Since C++17 (CWG 1696, applied as a defect report) that is ill-formed, but GCC 15 still accepts it and only warns under `-Wextra` ('a temporary bound to ... only persists until the constructor exits').
- A temporary in a `new`-initializer.

### A36. References returned from functions do not extend lifetime

[Back to P36](#p36-references-returned-from-functions) · **Verdict:** Undefined behavior.

Both `r` and `m` **dangle**, so using them is UB. Lifetime extension only works when the temporary binds *directly* to the reference. Here the temporaries bind to the *function parameters*, and the functions return references to those parameters. The temporaries die at the end of the full-expression.

In our run, the string printed as garbage bytes followed by the tail of the text, and `m` printed `2` because its stack slot had not been reused yet. That "looks fine" result is the danger. AddressSanitizer reports `heap-use-after-free`.

GCC 13 added `-Wdangling-reference`. In GCC 13 and 14 it is part of `-Wall`. GCC 15 moved it to `-Wextra` because of false positives, so with the `-Wall`-only build used here it stays silent. Add `-Wextra` and it flags both lines.

**Fix.** Hold the result by value: `std::string r = pick(...)` and `int m = std::max(1, 2)`. The same trap appears as `const auto& x = std::max(a, b + 1);` and as `for (auto& e : getObject().items())` (see the next puzzle).

### A37. Range-`for` over a temporary

[Back to P37](#p37-range-for-over-a-temporary) · **Verdict:** (a) well-defined; (b) UB in C++20, well-defined in C++23.

Observed with `-std=c++20`:

```text
1 2 3 | <garbage> <garbage> <garbage>
```

GCC 15 with `-std=c++23`:

```text
1 2 3 | 1 2 3
```

**Why.** A range-for loop expands to `auto&& __range = <range-init>; for (auto it = begin(__range); ...)`.
- (a) `make().v` is a member of a prvalue. `__range` binds directly to the member subobject, so the **whole** `Holder` temporary gets lifetime extension.
- (b) `make().get()` returns a reference. `__range` binds to that returned reference, so no lifetime extension happens. The `Holder` temporary is destroyed at the end of the range-init, before the loop body runs. Under ASan this is `stack-use-after-scope`.

**C++23 fix.** P2718R0 extends **all** temporaries in the range-initializer to the end of the loop. GCC 15 implements it. It is on by default with `-std=c++23` and controlled by `-frange-for-ext-temps`; GCC 15 does not enable it by default in C++20 mode.

**Portable fix.** Use the C++20 init-statement: `for (auto h = make(); int x : h.get())`.

### A38. `std::string_view` outliving its buffer

[Back to P38](#p38-where-does-a-string_view-point) · **Verdict:** Undefined behavior (lines c and d).

- (a) is fine, because string literals have static storage duration.
- (b) is fine, because the view points into `owner`, which lives on.
- (c) is **UB**. The temporary `std::string` is destroyed at the end of the full-expression, so `bad` points to freed heap memory. ASan reports `heap-use-after-free`.
- (d) is **UB**. `"hello world"` is converted to a temporary `std::string` to bind to the `const std::string&` parameter, and the returned view points into that temporary.

In our run, (c) printed garbage, and (d) happened to print `hello`. The short string sat in the SSO buffer on the stack and had not been overwritten yet. Code that seems to work is the usual way this bug ships.

**Rules.** A `string_view` is a non-owning pointer plus length. Take `string_view` *parameters*. Return an owning `std::string` unless the referenced storage clearly outlives the caller. Watch out for `std::string_view v = a + b;` and for `string_view` members in classes. The same rules apply to `std::span`.

### A39. Capturing a local by reference in an escaping lambda

[Back to P39](#p39-a-counter-factory) · **Verdict:** Undefined behavior.

The closure holds a reference to `count`, a local of `makeCounter`. That local dies when `makeCounter` returns, so every call through `next` uses a dangling reference. In our run the program crashed with SIGSEGV (exit status 139). ASan reports `stack-use-after-return`. Do not predict an output.

**Fix.** Capture by value and make the lambda mutable: `return [count]() mutable { return ++count; };`. It prints `1 2`.

**Related traps.**
- A callback stored in an event loop or thread pool that captures `this` and outlives the object.
- `[=]` inside a member function captures `this`, not the members by value. C++20 deprecates the implicit `this` capture with `[=]`. Use `[*this]` or `[self = shared_from_this()]` when the callback may outlive the object.

### A40. Value captures, mutable, and copying closures

[Back to P40](#p40-copying-a-mutable-lambda) · **Verdict:** Well-defined.

```text
10 4 2 10
```

**Why.**
- `[x]` copies `x` (1) into the closure when the lambda is created. `mutable` lets the closure change its *own* copy, and the outer `x` is never affected.
- `copy = byVal` copies the closure object, including its captured `x`, which is still 1 at that point.
- Two calls to `byVal()` raise its copy to 3, and the call inside the print statement returns 4.
- `copy()` starts from its own 1 and returns 2.
- `byRef` reads the live `x`, which is 10.
- C++17's left-to-right sequencing of `<<` makes the order well-defined.

**Follow-ups.** Init-capture (`[v = std::move(vec)]`) moves objects into a lambda. Lambdas can capture structured bindings only since C++20.

### A41. Structured bindings copy unless you ask for a reference

[Back to P41](#p41-structured-bindings-copies-or-references) · **Verdict:** Well-defined.

```text
1one 3 10 99
```

**Why.**
- `auto [n, s] = p;` creates a hidden **copy** of `p`, and `n` and `s` name the members of that copy. Assigning to them does not touch `p`.
- `auto& [rn, rs] = p;` makes the hidden object a reference to `p`, so `rn = 3` changes `p.first`.
- In the map loop, `auto [k, v]` copies each `pair<const int, int>`, so the write to `v` is lost. `auto& [k, v]` writes into the map.

**Follow-ups.**
- `for (auto [k, v] : m)` over a map with `std::string` values copies every string on every iteration. Use `const auto&` for read-only loops.
- `decltype(n)` is `int`, not `int&`, even though `n` names a member of the hidden object.

### A42. `std::move` on a const object copies

[Back to P42](#p42-stdmove-on-a-const-object) · **Verdict:** Well-defined.

```text
copy 41 41
```

**Why.** `std::move` is only `static_cast<T&&>`. On a `const S`, it produces `const S&&`. The move constructor takes `S&&`, which cannot bind to a const rvalue. The copy constructor's `const S&` can bind, so a copy happens silently with no error. For the same reason, `cs` still holds all 41 characters after the "move".

**Related.**
- clang-tidy's `performance-move-const-arg` catches this.
- Do not declare by-value return types `const` (`const std::string f();`), because that blocks moving from the result.
- A `const` local that is returned can still get NRVO, but if NRVO does not happen, it is copied instead of moved.

### A43. `std::move` does not move anything

[Back to P43](#p43-when-does-stdmove-move) · **Verdict:** Well-defined.

```text
3 3 3 0 3
```

**Why.** `std::move` is a cast to an rvalue reference.
- `auto&& r = std::move(v);` only binds a reference.
- `take(std::move(v))` binds the `std::vector<int>&&` parameter, but `take` never moves from it, so `v` keeps its elements.
- Only `std::vector<int> w = std::move(v);` runs the move constructor, which takes over `v`'s buffer.

After the move, `v.size()` was 0. libstdc++, libc++, and MSVC STL all leave a moved-from vector empty. In general, the standard only promises that moved-from library objects are *valid but unspecified*. Call `clear()` or assign a new value before you reuse one.

### A44. RVO, NRVO, and implicit move

[Back to P44](#p44-returning-objects-from-functions) · **Verdict:** Well-defined (NRVO is permitted, not required).

```text
ctor | ctor | ctor ctor move dtor dtor | dtor dtor dtor
```

**Why.**
- `rvo()`: `return T{};` returns a prvalue. Since C++17, **guaranteed copy elision** means `T{}` initializes `a` directly, so there is no copy or move and not even a requirement that one exist.
- `nrvo()`: returning a named local permits **NRVO** but does not require it. GCC and Clang perform it even at `-O0`, so only `ctor` is printed. With `-fno-elide-constructors` this segment becomes `ctor move dtor`. In C++17 that flag only disables the *non*-mandatory elisions.
- `either(true)`: the compiler cannot construct both `x` and `y` in the return slot, so NRVO is impossible. A returned local is treated as an rvalue (implicit move), so the result is `move`, followed by `dtor dtor` for `x` and `y`.
- At the end of `main`, `c`, `b`, and `a` are destroyed.

Five constructions (four `ctor` and one `move`) match five `dtor` lines.

### A45. `return std::move`, and returning non-movable types

[Back to P45](#p45-return-stdmove-and-a-non-movable-type) · **Verdict:** Well-defined.

```text
ctor move pinned
```

**Why.**
- `return std::move(t);` returns an expression that is not just the name of a local, so NRVO is not allowed. The move constructor runs. GCC's `-Wpessimizing-move` (in `-Wall`) warns. Plain `return t;` would elide the move, or at worst move implicitly.
- `Pinned` has deleted copy and move constructors, but `return Pinned{42};` still compiles in C++17. Guaranteed elision means that no copy or move constructor is ever called, so none is needed. This is how factories can return `std::mutex`- or `std::atomic`-like types. `Pinned p{1}; return p;` would **not** compile, because NRVO is optional and the copy or move must still be available.

**When `std::move` on return IS right:** returning a data member or another subobject (`return std::move(this->buf_);`), or anything that is not a plain local or parameter name. Before C++20, `return p;` for an rvalue-reference parameter `T&& p` copied; C++20's P1825 made that an implicit move too, so even fewer cases need an explicit `std::move`.

### A46. `vector<bool>` returns a proxy

[Back to P46](#p46-auto-with-vectorbool) · **Verdict:** Well-defined.

```text
0 1
```

**Why.** `std::vector<bool>` is a space-optimized specialization that stores bits. `operator[]` returns a proxy object, `std::vector<bool>::reference`, not a `bool&`. `auto x = vb[0];` deduces the proxy type, and the proxy still refers to the bit inside `vb`, so `x = false` writes through to the vector. With `vector<int>`, `auto y` is a plain copy.

**Consequences.**
- `bool& r = vb[0];` does not compile.
- `&vb[0]` is not a `bool*`.
- There is no `data()`.
- Two threads writing *different* elements can race, because neighboring bits share a word.
- `auto b = std::vector<bool>{true}[0];` dangles.

**Alternatives.** Write `bool x = vb[0];`, or use `std::vector<char>`, `std::deque<bool>`, `std::bitset<N>`, or `boost::dynamic_bitset`.

### A47. push_back while iterating

[Back to P47](#p47-push_back-during-range-for) · **Verdict:** Undefined behavior.

A range-for loop caches `begin()` and `end()` once. In libstdc++, a vector built from a five-element `initializer_list` has capacity 5, so `push_back(6)` reallocates and every iterator now points into freed memory. Our run printed `1 2` followed by garbage and then `5`. ASan reports `heap-use-after-free`.

Even without reallocation, the cached `end` is stale, so the new element would not be visited.

**Fixes.** Loop by index (`for (std::size_t i = 0; i < v.size(); ++i)`), or collect the new elements in a separate vector and append them after the loop.

**Invalidation cheat sheet.**

| Container | Insert | Erase |
|---|---|---|
| `vector` | All iterators if it reallocates; otherwise those at or after the insertion point | At or after the erased element |
| `deque` | All iterators, but references stay valid when inserting at either end | All, except when erasing at either end |
| `list` / `map` / `set` | None | Only the erased element |
| `unordered_*` | Iterators on rehash; references stay valid | Only the erased element |

See [Cpp_Fundamentals 8.2](../languages/Cpp_Fundamentals.md#82-iterator-invalidation-rules).

### A48. Erasing inside a for loop skips elements

[Back to P48](#p48-erasing-inside-a-for-loop) · **Verdict:** Well-defined here (but buggy).

```text
4 5
```

**Trace.**
1. `it` points to 2. `erase` returns an iterator to 4. Then `++it` moves to 5, so 4 is **skipped**.
2. 5 is odd. `++it` reaches `end()`, and the loop stops.

If the last element were even, `erase` would return `end()`, the loop's `++it` would step past the end, and the program would have **UB**. For example, `{2, 4, 6}` erases 2, skips 4, erases 6, and increments past `end()`.

**Fixes.**
- `std::erase_if(v, [](int x) { return x % 2 == 0; });` (C++20). It is O(n) and returns the number erased.
- The erase-remove idiom.
- A manual loop that increments only when nothing is erased: `if (pred(*it)) it = v.erase(it); else ++it;`. This is O(n^2) on a vector.

### A49. `std::map::operator[]` inserts

[Back to P49](#p49-looking-up-keys-in-a-stdmap) · **Verdict:** Well-defined.

```text
zero 2 0 0 2 0
```

**Why.**
- `m["b"]` inserts a value-initialized `int` (0) when the key is missing, so the size becomes 2.
- `count`, `contains` (C++20), and `find` never insert.
- `operator[]` is non-const, so it does not compile on a `const std::map`, and it requires the mapped type to be default-constructible.
- `sizes["x"] = sizes.size();`: C++17 sequences the right operand of `=` first, so `size()` is 0 and only then does `operator[]` insert. Before C++17 the order was unspecified, and the result could be 1.

**Use instead:** `at()` (throws `std::out_of_range`), `find`, `contains`, `try_emplace`, or `insert_or_assign`. The same rules apply to `unordered_map`.

### A50. `vector` reallocation copies unless the move constructor is `noexcept`

[Back to P50](#p50-vector-growth-and-noexcept) · **Verdict:** Well-defined.

```text
copy | move
```

**Why.** `push_back` and `emplace_back` give the **strong exception guarantee**: if anything throws, the vector is unchanged. During reallocation the old elements are relocated with `std::move_if_noexcept`. If the move constructor might throw (it is not `noexcept`) and a copy constructor exists, the vector copies. A move that threw halfway through would leave the old buffer partly moved-from with no way back. `A`'s move constructor is not `noexcept`, so `A` is copied. `B` is moved.

**Practical impact.** A user type with a hand-written move constructor that is not `noexcept` gets *copied* on every reallocation, which can be a large hidden cost. Defaulted move constructors are `noexcept` automatically when all members' moves are. Check with `static_assert(std::is_nothrow_move_constructible_v<T>)`. If the copy constructor is deleted, vector moves anyway and gives up the strong guarantee.

### A51. `shared_ptr` cycles leak; `weak_ptr` breaks them

[Back to P51](#p51-two-nodes-pointing-at-each-other) · **Verdict:** Well-defined (but the first block leaks).

```text
2 | 1 ~c ~d | end
```

**Why.**
- `a` and `b` own each other. When the locals go out of scope, each strong count drops from 2 to 1 and never reaches 0. The destructors never run, and the memory leaks. LeakSanitizer reports it.
- In the second block, `d->prev` is a `weak_ptr`, which does not add to the strong count, so `c.use_count()` is 1.
- At scope exit, `d` is destroyed first, and `d`'s count drops from 2 to 1. Then `c` drops from 1 to 0, which prints `~c`. Destroying `c`'s member `next` releases the last owner of `d`, which prints `~d`.

**Design rule.** Ownership edges use `unique_ptr` or `shared_ptr`. Back-edges (parent pointers, observers, caches) use `weak_ptr`, or raw pointers when the lifetime is otherwise guaranteed. Access through a `weak_ptr` with `lock()`.

**Follow-up.** With `make_shared`, the object and the control block share one allocation. The object is destroyed when the strong count hits 0, but the memory is freed only when the weak count also hits 0.

### A52. Throwing out of an implicitly `noexcept` destructor

[Back to P52](#p52-throwing-from-a-destructor) · **Verdict:** Well-defined: `std::terminate`.

`catch` never runs and `after` is never printed. stderr shows:

```text
terminate called after throwing an instance of 'std::runtime_error'
  what():  boom
```

The process then aborts with exit status 134.

**Why.** Since C++11, destructors are implicitly `noexcept(true)`, unless a base or member destructor is `noexcept(false)`. An exception that leaves a `noexcept` function calls `std::terminate`, and stack unwinding is not even guaranteed. GCC warns at compile time: `'throw' will always call 'terminate'` (`-Wterminate`).

### A53. A second exception during stack unwinding

[Back to P53](#p53-noexceptfalse-destructors-and-unwinding) · **Verdict:** Well-defined: `std::terminate` in the second block.

stdout:

```text
caught: from dtor
unwinding
```

stderr shows `terminate called after throwing an instance of 'std::runtime_error'` with `what():  from dtor`, and then the process aborts.

**Why.**
- First block: no exception is active, so the `noexcept(false)` destructor's exception propagates normally and is caught.
- Second block: `"original"` is propagating. During unwinding, `~Loud` throws again. Two exceptions cannot propagate at once, so `std::terminate` is called. `std::uncaught_exceptions()` (C++17) let the destructor detect the unwinding; scope guards such as `scope_fail` and `scope_success` use the same check.

**Why the program uses `std::endl`.** On `abort()`, buffered stdout is **lost**. With `'\n'` and stdout redirected to a pipe or file, neither line appears. This is a real debugging trap: flush, or log crash breadcrumbs to `std::cerr`.

**Rule.** Do not throw from destructors. Expose an explicit `close()`, `commit()`, or `flush()` that can report errors, and have the destructor swallow and log them.

### A54. Strict aliasing

[Back to P54](#p54-writing-an-int-through-a-float) · **Verdict:** Undefined behavior.

Writing the `int` object `x` through a `float*` violates the strict aliasing rule ([basic.lval]), so the program is **UB**. GCC 15 printed `0` at `-O0` and `1` at `-O2`. At `-O2`, the compiler assumes an `int*` and a `float*` never point to the same object, so `return *i` becomes `return 1` and ignores the `float` store.

**What may alias what:**
- the same type, including cv-qualified versions;
- the signed or unsigned version of the type;
- `char`, `unsigned char`, and `std::byte`, which can inspect the bytes of any object.

**Correct type punning** (verified to print `3f800000 3f800000`):

```cpp
// fragment
float f = 1.0f;
auto a = std::bit_cast<std::uint32_t>(f);   // C++20, constexpr-friendly
std::uint32_t b;
std::memcpy(&b, &f, sizeof b);              // pre-C++20; compiles to a single mov
```

**Notes.**
- Union type punning is UB in C++, although it is allowed in C. GCC documents it as a supported extension.
- `-fno-strict-aliasing` turns off the optimization; the Linux kernel builds with it.
- GPU kernels often `reinterpret_cast` to `float4*` for vectorized loads. That code relies on compiler behavior and also needs correct alignment.

See [Cpp_Fundamentals 15.3](../languages/Cpp_Fundamentals.md#153-strict-aliasing-rule).

### A55. One Definition Rule violation

[Back to P55](#p55-two-definitions-of-an-inline-function) · **Verdict:** Ill-formed, no diagnostic required.

Two different definitions of the inline function `value()` in two translation units violate the ODR, so the program is ill-formed, no diagnostic required (NDR). Observed with GCC 15:

| Build | Output |
|---|---|
| `-O0`, `a.cpp b.cpp` | `11` |
| `-O0`, `b.cpp a.cpp` | `22` |
| `-O2`, either order | `21` |

**Why.** At `-O0`, each TU emits an out-of-line copy of `value()` as a weak (COMDAT) symbol. The linker keeps the first one it sees and both TUs call it. At `-O2`, each TU inlines its own definition. The output depends on link order and optimization level, which is a typical sign of an ODR violation.

**Where this happens in practice.**
- The same header compiled with different `-D` flags or `NDEBUG`, so a struct layout or inline function differs between libraries.
- Two versions of a header-only library in one binary.
- Helper functions or classes with the same name in two `.cpp` files that should have had internal linkage.

**Prevention and detection.**
- Put TU-local helpers in an anonymous namespace or mark them `static`.
- Use consistent build flags across all targets.
- `-flto -Wodr` catches mismatched *type* definitions across TUs. It did not flag this inline-function case.
- ASan's `detect_odr_violation` catches duplicate global *variables*.

See [Cpp_Fundamentals 13.2](../languages/Cpp_Fundamentals.md#132-translation-units-and-the-one-definition-rule-odr).

### Mock Interview Model Answers

[Back to Section 12](#12-timed-mock-interview-c-cmake-and-testing). Verified with GCC 15.2, CMake 4.2.3, Ninja 1.13, and GoogleTest 1.17.0 on x86-64 Linux.

#### Round A Answers: Warm-Up

[Back to 12.2](#122-round-a-rapid-fire-warm-up-w1-w15)

| # | Model answer |
|---|---|
| W1 | Nothing at runtime. It is `static_cast<std::remove_reference_t<T>&&>(x)`, a cast to an xvalue, so overload resolution *can* pick a move constructor or move assignment. Whether anything moves depends on the overload chosen; a `const` object still copies ([P42](#p42-stdmove-on-a-const-object)). |
| W2 | `std::vector` reallocation uses `std::move_if_noexcept` to keep the strong exception guarantee: if the move constructor may throw *and* the type is copyable, it copies instead. A missing `noexcept` silently turns every growth into a deep copy ([P50](#p50-vector-growth-and-noexcept)). |
| W3 | 8, 16, and 16 bytes (verified). `unique_ptr` with a stateless deleter is one pointer (the empty deleter takes no space). `shared_ptr` is two pointers: the object and the control block. A function-pointer deleter is state, so it adds 8 bytes. For comparison, `std::function<void()>` and `std::string` are 32 bytes each in libstdc++. |
| W4 | Two conflicting accesses to the same memory location (at least one is a write) from different threads, where at least one is not atomic and neither *happens before* the other. A program with a data race has **undefined behavior**, not merely an unpredictable value. |
| W5 | `operator[]` inserts a value-initialized element when the key is missing, so it must be non-`const`. In lookups it silently adds keys: the map grows, iteration later shows phantom entries, and "missing" cannot be told apart from "zero". Use `find`, `contains` (C++20), or `at` ([P49](#p49-looking-up-keys-in-a-stdmap)). |
| W6 | `EXPECT_*` records a failure and continues; `ASSERT_*` records it and **returns from the current function**. The macro expands to a `return` of a `void` expression, so it only compiles in functions returning `void`. In helpers, return `void` and check `HasFatalFailure()` in the caller, or return `::testing::AssertionResult`. |
| W7 | A **stub** returns canned answers (a counter source that always returns 1000 cycles). A **fake** is a working lightweight implementation (an in-memory counter source that replays a recorded session). A **mock** verifies interactions (expects `begin_pass()` to be called exactly 3 times with these counter groups). |
| W8 | No. ASan and TSan both need their own shadow-memory layout and runtime, and the compiler rejects the combination. CI runs separate jobs: ASan+UBSan (+LSan, which is part of ASan on Linux) and TSan. MSan (Clang only) is a third job if you need it. |
| W9 | `PRIVATE`: used to build this target only. `INTERFACE`: not used by this target, but propagated to consumers. `PUBLIC`: both. Rule: a dependency that appears in your *public headers* is `PUBLIC`; one used only in `.cpp` files is `PRIVATE`. |
| W10 | The glob is evaluated at configure time. Adding a file does not rerun CMake, so the new file is silently not compiled until someone reconfigures. `CONFIGURE_DEPENDS` makes the generated build re-check the glob on every build, which costs time on large trees, and CMake's documentation still recommends listing sources explicitly. |
| W11 | Multi-config generators pick the configuration at *build* time (`cmake --build . --config Debug`), so `CMAKE_BUILD_TYPE` is empty during configure and the `if` is false. Use a generator expression: `target_compile_definitions(t PRIVATE $<$<CONFIG:Debug>:KSTATS_DEBUG>)`. Even with single-config generators, `CMAKE_BUILD_TYPE` is empty by default, which means no `-O` and no `-g` at all. |
| W12 | `add_test` registers the whole binary as **one** CTest test: one pass/fail, no per-test parallelism, `ctest -R` cannot select individual tests. `gtest_discover_tests` runs the binary with `--gtest_list_tests` after the build (or just before the tests, with `DISCOVERY_MODE PRE_TEST`, CMake 3.18+) and registers **one CTest test per GoogleTest test**, including parameterized and typed tests. |
| W13 | It means "multiple identical definitions across translation units are allowed" (an ODR exemption), which is what lets you define functions and, since C++17, variables in headers. It is only a hint for inlining; the optimizer decides that independently. |
| W14 | `DT_RPATH` is searched *before* `LD_LIBRARY_PATH` and applies to libraries loaded on the object's behalf too. `DT_RUNPATH` is searched *after* `LD_LIBRARY_PATH` and only for the object's own direct dependencies. Most current distros configure the linker with `--enable-new-dtags`, so `-Wl,-rpath` emits `RUNPATH`. |
| W15 | Only symbols you explicitly mark (`__attribute__((visibility("default")))` or a generated export macro) are exported. That gives a smaller dynamic symbol table and faster loading, calls within the library that need no PLT indirection and can be inlined, no accidental interposition, and an explicit, reviewable ABI surface. In CMake: `CMAKE_CXX_VISIBILITY_PRESET hidden` plus `CMAKE_VISIBILITY_INLINES_HIDDEN ON`. |

#### Round B Answers: Code Review

[Back to 12.3](#123-round-b-code-review)

**B1. C++ findings, by severity.**

| # | Defect | Consequence | Caught by | Fix |
|---|---|---|---|---|
| 1 | `[&]` captures the loop variable `t` **by reference** | Threads read `t` while `main` increments it (a data race), and after `t`'s lifetime ends when the loop exits. Threads may process the same slice, or start at 4 and do nothing | ASan: `stack-use-after-scope` on the `for (int i = t; ...)` line (observed). TSan: race on `t` | Capture `t` by value: `[&samples, &stats, t]` |
| 2 | Unsynchronized `add()` from 4 threads: `totals_` (a `std::map`), `slowest_`, `slowest_us_` | Data race, which is UB. Concurrent inserts can corrupt the red-black tree and crash | TSan: data-race reports on lines 17-19 of `KernelStats::add` (observed) | Lock a mutex, or better, aggregate per thread and merge once (below) |
| 3 | `slowest_us_` is never initialized | Reading an indeterminate `double` is UB. If the garbage happens to be large, `slowest_` is never set | Not `-Wall`, even at `-O2` (GCC 15 printed nothing). Valgrind memcheck or Clang MSan | `double slowest_us_ = -1.0;` (a default member initializer) |
| 4 | `std::string_view slowest_` points into `samples[i].kernel` | Dangles after `samples.clear()`. Our runs still printed a valid-looking name (`gemm_3`, or `gemm_2` when the race on `t` skipped a slice): the string is short enough for SSO, so its characters live inside the `Sample` object in the vector's buffer, and `clear()` keeps the capacity. ASan stays silent. Add `samples.shrink_to_fit()` and ASan reports `heap-use-after-free` (observed) | ASan only when the memory is really freed; code review | Store a `std::string`; return it **by value** so no reference to internal state escapes a lock |
| 5 | `total()` uses `operator[]` | Inserts `"gemm_9"` with value 0, cannot distinguish "missing" from "zero", is non-`const`, and races if called concurrently | Code review; a test that checks the key set after a lookup | `find` and return `std::optional<double>`; make it `const` with a `mutable` mutex |
| 6 | If `workers.emplace_back` throws (thread creation fails with `std::system_error`, or the vector reallocation throws `bad_alloc`) | Destroying a joinable `std::thread` calls `std::terminate` | Code review | `std::vector<std::jthread>` (C++20) joins in its destructor |
| 7 | `int i < samples.size()` | `-Wsign-compare` warning; `int` overflow past 2^31 elements | `-Wall` (observed) | `std::size_t` |

**Fixed version.** Prints `slowest: gemm_3`, `gemm_1 total: 62375`, `gemm_9 present: 0`. Clean under TSan and ASan+UBSan. (Check: the `gemm_1` samples are i = 1, 5, ..., 997, which is 250 values summing to 124,750, times 0.5.)

```cpp
#include <cstddef>
#include <iostream>
#include <map>
#include <mutex>
#include <optional>
#include <string>
#include <thread>
#include <vector>

struct Sample {
    std::string kernel;
    double duration_us;
};

class KernelStats {
public:
    void add(const Sample& s) {
        std::lock_guard lock(mu_);
        totals_[s.kernel] += s.duration_us;
        if (s.duration_us > slowest_us_) {
            slowest_us_ = s.duration_us;
            slowest_ = s.kernel;                   // owning copy, not a view
        }
    }
    // Merge a per-thread partial result under one lock acquisition.
    void merge(const KernelStats& other) {
        std::scoped_lock lock(mu_, other.mu_);
        for (const auto& [k, v] : other.totals_) totals_[k] += v;
        if (other.slowest_us_ > slowest_us_) {
            slowest_us_ = other.slowest_us_;
            slowest_ = other.slowest_;
        }
    }
    std::string slowest() const {
        std::lock_guard lock(mu_);
        return slowest_;                           // return by value: no reference escapes the lock
    }
    std::optional<double> total(const std::string& kernel) const {
        std::lock_guard lock(mu_);
        if (auto it = totals_.find(kernel); it != totals_.end()) return it->second;
        return std::nullopt;                       // lookup must not insert
    }

private:
    mutable std::mutex mu_;
    std::map<std::string, double> totals_;
    std::string slowest_;
    double slowest_us_ = -1.0;                     // initialized
};

int main() {
    std::vector<Sample> samples;
    for (int i = 0; i < 1000; ++i)
        samples.push_back({"gemm_" + std::to_string(i % 4), i * 0.5});

    constexpr std::size_t kThreads = 4;
    KernelStats stats;
    std::vector<std::thread> workers;
    for (std::size_t t = 0; t < kThreads; ++t)
        workers.emplace_back([&samples, &stats, t] {          // t by value
            KernelStats local;                                 // no contention in the hot loop
            for (std::size_t i = t; i < samples.size(); i += kThreads) local.add(samples[i]);
            stats.merge(local);
        });
    for (auto& w : workers) w.join();

    samples.clear();
    std::cout << "slowest: " << stats.slowest() << '\n';
    std::cout << "gemm_1 total: " << stats.total("gemm_1").value_or(0.0) << '\n';
    std::cout << "gemm_9 present: " << stats.total("gemm_9").has_value() << '\n';
}
```

**Follow-ups to expect.**
- *Why per-thread aggregation instead of just a mutex in `add`?* With one lock per sample, 4 threads serialize on one cache line and the mutex ping-pongs between cores. Local aggregation does 250 lock-free adds per thread and takes the lock once. This is the same idea as per-thread histograms in profilers and the per-block partial sums of a GPU reduction.
- *`merge(*this)` deadlocks.* `std::scoped_lock` on the same mutex twice is UB (in practice a self-deadlock). Guard it with `if (&other == this) return;` if self-merge is possible.
- *I kept `std::thread` here for the one-to-one diff; in new code I'd use `std::jthread`* (finding 6).

**B2. CMake findings.**

| # | Defect | Why it matters | Fix |
|---|---|---|---|
| R1 | `cmake_minimum_required(VERSION 3.10)` | Sets every policy newer than 3.10 to OLD behavior. CMake 4.x rejects versions below 3.5 outright (verified on 4.2: "Compatibility with CMake < 3.5 has been removed"), and 3.31+ deprecates versions below 3.10 | A range: `cmake_minimum_required(VERSION 3.24...4.2)`, with the floor set by the newest feature you use |
| R2 | `project(kstats)` | No `LANGUAGES`, so C is enabled and probed too, and no `VERSION` for the package version file or SOVERSION | `project(kstats VERSION 1.2.0 LANGUAGES CXX)` |
| R3 | `set(CMAKE_CXX_FLAGS "-std=c++17 -O2 -Wall")` | Overwrites the flags users and CI pass in (`-DCMAKE_CXX_FLAGS=-fsanitize=address` disappears), forces `-O2` into Debug builds, is GCC/Clang-only syntax, and the language standard does not propagate to consumers | `target_compile_features(kstats PUBLIC cxx_std_20)` and `target_compile_options(kstats PRIVATE $<$<CXX_COMPILER_ID:GNU,Clang>:-Wall -Wextra>)` |
| R4 | `include_directories(...)` (directory scope) | Applies to every target in the directory and below, including tests; not part of `kstats`'s usage requirements, so the installed package has no include directory | `target_include_directories` with `$<BUILD_INTERFACE:...>`/`$<INSTALL_INTERFACE:...>`, or a `FILE_SET HEADERS` (3.23+) |
| R5 | Hardcoded `/opt/rocm/include`, `link_directories(/opt/rocm/lib)`, raw `amdhip64` | Breaks for ROCm installed elsewhere (nightlies under `$HOME`, `ROCM_PATH`), mixes ROCm versions silently, and misses the compile definitions and flags that `hip::host` carries | `find_package(hip REQUIRED)` with `-DCMAKE_PREFIX_PATH=/opt/rocm`, then `target_link_libraries(kstats PRIVATE hip::host)` |
| R6 | `file(GLOB SRCS src/*.cpp)` | New files are not built until the next reconfigure (W10) | List sources explicitly |
| R7 | `target_link_libraries(kstats pthread amdhip64)` (plain signature) | No `PUBLIC`/`PRIVATE`: with the plain signature, dependencies are transitive by default, so everything leaks to consumers. Once one call on a target uses the plain signature, a later keyword call on the same target is an error. `pthread` by name is not portable and does not add `-pthread` for compiling | `find_package(Threads REQUIRED)` and `target_link_libraries(kstats PRIVATE Threads::Threads)` |
| R8 | `if(CMAKE_BUILD_TYPE STREQUAL "Debug")` with a `PUBLIC` definition | Never true with multi-config generators (W11). `PUBLIC` leaks `KSTATS_DEBUG` into consumers; if it changes a struct layout in a header, consumers and the library disagree on the layout, which is an ODR/ABI break | `target_compile_definitions(kstats PRIVATE $<$<CONFIG:Debug>:KSTATS_DEBUG>)` |
| R9 | `target_link_libraries(kstats_test kstats gtest gtest_main)` | Raw library names depend on a system GTest in the default paths, with no include directories and no threads. Tests are also built when `kstats` is consumed as a subproject | `FetchContent` or `find_package(GTest)`, link `GTest::gtest_main`, and guard with an option defaulting to `PROJECT_IS_TOP_LEVEL` (3.21+) |
| R10 | `add_test(kstats_test kstats_test)` with no `enable_testing()` | `ctest` prints "No test configuration file found!" (verified) and runs nothing. The old two-argument signature also does not support generator expressions | `enable_testing()` (or `include(CTest)`), then `gtest_discover_tests(kstats_test)` |
| R11 | `install(TARGETS kstats DESTINATION lib)` | No `EXPORT`, so no `kstatsTargets.cmake` and no `find_package(kstats)` support. Headers are not installed. `lib` is hardcoded (Fedora/RHEL use `lib64`). The installed binaries get an empty RPATH, and the library has no SOVERSION | `GNUInstallDirs`, `install(TARGETS ... EXPORT ... FILE_SET HEADERS)`, `install(EXPORT ...)`, a config file and a version file, `CMAKE_INSTALL_RPATH`, `VERSION`/`SOVERSION` |
| R12 | No visibility control | Every symbol is exported (W15) | `CMAKE_CXX_VISIBILITY_PRESET hidden` plus an export macro on the public API |

**Fixed `CMakeLists.txt`.** Verified with CMake 4.2: it configures, builds, the test passes, `cmake --install` produces `lib/libkstats.so{,.1,.1.2.0}`, the headers, and `lib/cmake/kstats/*`, and a separate consumer project with `find_package(kstats 1.0 REQUIRED)` builds and runs. It also configures and builds with `-DKSTATS_USE_HIP=ON` against a ROCm install.

```cmake
cmake_minimum_required(VERSION 3.24...4.2)
project(kstats VERSION 1.2.0 LANGUAGES CXX)

include(GNUInstallDirs)
option(KSTATS_USE_HIP "Build the HIP-backed collector" OFF)
option(KSTATS_BUILD_TESTS "Build unit tests" ${PROJECT_IS_TOP_LEVEL})

# Relocatable install: bin/ and lib/ find siblings via $ORIGIN (set before targets exist).
set(CMAKE_INSTALL_RPATH "$ORIGIN/../${CMAKE_INSTALL_LIBDIR}")
set(CMAKE_CXX_VISIBILITY_PRESET hidden)
set(CMAKE_VISIBILITY_INLINES_HIDDEN ON)

find_package(Threads REQUIRED)

add_library(kstats SHARED src/kernel_stats.cpp)
add_library(kstats::kstats ALIAS kstats)
target_sources(kstats PUBLIC
  FILE_SET HEADERS BASE_DIRS include FILES include/kstats/kernel_stats.hpp)
target_compile_features(kstats PUBLIC cxx_std_20)
target_compile_options(kstats PRIVATE
  $<$<CXX_COMPILER_ID:GNU,Clang>:-Wall -Wextra>)
target_compile_definitions(kstats PRIVATE $<$<CONFIG:Debug>:KSTATS_DEBUG>)
target_link_libraries(kstats PRIVATE Threads::Threads)
set_target_properties(kstats PROPERTIES
  VERSION ${PROJECT_VERSION} SOVERSION ${PROJECT_VERSION_MAJOR})

if(KSTATS_USE_HIP)
  find_package(hip REQUIRED)               # found via CMAKE_PREFIX_PATH=/opt/rocm
  target_link_libraries(kstats PRIVATE hip::host)
endif()

if(KSTATS_BUILD_TESTS)
  enable_testing()
  include(FetchContent)
  FetchContent_Declare(googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG        v1.17.0
    FIND_PACKAGE_ARGS NAMES GTest)         # prefer an installed GTest (3.24+)
  set(INSTALL_GTEST OFF CACHE BOOL "" FORCE) # do not ship GTest in our package
  FetchContent_MakeAvailable(googletest)
  add_executable(kstats_test test/test_stats.cpp)
  target_link_libraries(kstats_test PRIVATE kstats::kstats GTest::gtest_main)
  include(GoogleTest)
  gtest_discover_tests(kstats_test)
endif()

install(TARGETS kstats EXPORT kstatsTargets FILE_SET HEADERS)
install(EXPORT kstatsTargets NAMESPACE kstats::
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/kstats)
include(CMakePackageConfigHelpers)
configure_package_config_file(cmake/kstatsConfig.cmake.in
  ${CMAKE_CURRENT_BINARY_DIR}/kstatsConfig.cmake
  INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/kstats)
write_basic_package_version_file(${CMAKE_CURRENT_BINARY_DIR}/kstatsConfigVersion.cmake
  COMPATIBILITY SameMajorVersion)
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/kstatsConfig.cmake
              ${CMAKE_CURRENT_BINARY_DIR}/kstatsConfigVersion.cmake
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/kstats)
```

```cmake
# cmake/kstatsConfig.cmake.in
@PACKAGE_INIT@
include(CMakeFindDependencyMacro)
find_dependency(Threads)
include("${CMAKE_CURRENT_LIST_DIR}/kstatsTargets.cmake")
check_required_components(kstats)
```

Two details interviewers like:
- **`INSTALL_GTEST OFF`.** Without it, `cmake --install` also installs GoogleTest's headers, libraries, and `GTestConfig.cmake` into *your* package, because GoogleTest's own install rules come along with `FetchContent` (observed before the line was added).
- **`find_dependency(Threads)`.** It is harmless here because `Threads::Threads` is `PRIVATE` to a *shared* library, so it does not appear in the exported link interface. If `kstats` were static, or the dependency `PUBLIC`, the exported target would reference `Threads::Threads` and consumers would fail without it (Chain M3.8).

#### Round C Answers: Follow-Up Chains

[Back to 12.4](#124-round-c-follow-up-chains)

##### Chain M1 Answers: Owning Device Buffer

**M1.1** Rule of Five with copying deleted. Members: a `void*` (or `T*`) and a byte count. Write a constructor that calls `hipMalloc` and throws on failure, a destructor that calls `hipFree`, a move constructor and a move assignment operator, and `= delete` the copy constructor and copy assignment. A deep copy would need a stream and a device-to-device copy, and an implicit one would hide an expensive operation. If someone needs a copy, give them an explicit `clone(hipStream_t)`.

**M1.2** `DeviceBuffer(DeviceBuffer&& o) noexcept : ptr_(std::exchange(o.ptr_, nullptr)), bytes_(std::exchange(o.bytes_, 0)) {}`. The moved-from object is **valid but empty**. Its destructor must be safe (`hipFree(nullptr)` is a no-op, but checking `if (ptr_)` is clearer), and callers may assign to it or destroy it. Document whether `size()` and `data()` are meaningful on it.

**M1.3** `vector` growth uses `std::move_if_noexcept`, which yields an lvalue (so a copy) only if the move may throw **and** the type is copyable. Copying is deleted here, so the vector uses the throwing move anyway and the **strong guarantee is lost**: if a move throws halfway through reallocation, some elements are already moved and the vector cannot roll back. For a copyable type without `noexcept`, you instead pay a full deep copy on every growth. Either way, mark it `noexcept`. Moving two words cannot fail.

**M1.4** The simplest correct form is "release mine, then steal":

```cpp
// fragment
DeviceBuffer& operator=(DeviceBuffer&& o) noexcept {
    if (this != &o) {
        reset();                                   // frees the current allocation
        ptr_ = std::exchange(o.ptr_, nullptr);
        bytes_ = std::exchange(o.bytes_, 0);
    }
    return *this;
}
```

Alternatively, swap with the source and let its destructor free the old allocation, which delays the free. Without the `this != &o` check, `x = std::move(x)` would free the buffer and then "steal" the null pointer it just stored, leaving `x` empty. The standard library only requires a self-moved object to be valid, which it would be, but silently losing the data is a nasty surprise, and the check costs one comparison.

**M1.5** Destructors are implicitly `noexcept`, so throwing calls `std::terminate`. Log the error (with the HIP error string) and continue, or count it in a metric. If callers need to observe free errors, provide an explicit `reset()` or `release_or_throw()` that reports the error, and have the destructor only log. Note that `hipFree` can fail because the device is already in an error state after an earlier asynchronous kernel fault, so the log line is often the first hint of a crash elsewhere.

**M1.6** Yes: `std::unique_ptr<void, HipFree>` with `struct HipFree { void operator()(void* p) const noexcept { (void)hipFree(p); } };`. That is the Rule of Zero, with correct moves for free. A **stateless functor** deleter keeps `sizeof` at 8 bytes (no storage for an empty class). A **function-pointer** deleter (`unique_ptr<void, hipError_t(*)(void*)>`) is state, so `sizeof` is 16 (verified with libstdc++) and every deletion is an indirect call. You still need to store the size separately, which is why many codebases wrap the `unique_ptr` in a small class anyway.

**M1.7** `std::shared_ptr<DeviceBuffer>` works, but it costs a control block allocation (one combined allocation with `make_shared`), two pointers per handle, and atomic reference-count updates on every copy, which hurts when handles are copied per launch. Shared ownership also does not solve **stream ordering**. The last owner must not free while a kernel on another stream still uses the memory, so free on a stream (`hipFreeAsync`) or synchronize with events first. The **aliasing constructor**, `shared_ptr<float>(owner, owner->data<float>() + offset)`, hands out sub-buffer pointers that keep the whole allocation alive.

**M1.8** A view is a pointer plus a length, like `std::span`: `template <class T> struct DeviceSpan { T* data; std::size_t size; };`, created by `buffer.span<T>()`. It is trivially copyable, so it can be passed to a kernel **by value**. HIP copies kernel arguments byte-wise into the kernarg segment, so argument types must be trivially copyable (no `std::string`, no virtual functions, no reference counting). If the buffer dies before the kernel runs, the kernel reads freed memory. That is especially easy with asynchronous launches, because the host-side scope can end long before the kernel executes. Lifetime must outlast stream completion, not just the launch call.

**M1.9** Wrap the allocator behind an interface or a function-pointer table and inject a **counting fake** in unit tests: assert that allocations equal frees, and that no pointer is freed twice. On a real GPU, compare `hipMemGetInfo` free memory before and after a loop of 10,000 create/destroy cycles. Run the host code under ASan for the host-side logic. Host ASan does not track `hipMalloc` memory; ROCm's GPU-side address sanitizer is a separate build mode that requires an XNACK-enabled target. A static-analysis or review check that every `hipMalloc` goes through the RAII type is the cheapest guard of all.

##### Chain M2 Answers: Green at -O0, Red at -O2

**M2.1**
1. **Reproduce CI exactly**: the same container image, compiler version, and flags. CMake's defaults are `Release` = `-O3 -DNDEBUG` and `RelWithDebInfo` = `-O2 -g -DNDEBUG` for GCC.
2. **Check `NDEBUG` first**: an `assert(do_setup())` with a side effect disappears in Release.
3. Rebuild the failing configuration with **`-g` and sanitizers** and rerun only the failing test (`--gtest_filter=Suite.Name`).

**M2.2**
- **Uninitialized reads**: the stack contents differ with register allocation.
- **Signed overflow**: the optimizer assumes it cannot happen, so overflow checks after the fact are deleted ([P26](#p26-checking-for-overflow-after-the-fact)).
- **Strict-aliasing violations**: loads are reordered or cached ([P54](#p54-writing-an-int-through-a-float)).
- **Out-of-bounds access**: the stack layout and padding change.
- **Dangling references and views**: freed memory is reused differently.
- **Data races**: values stay in registers and loops are merged.
- **A missing `return`** in a non-void function: control flows into whatever comes next.
- **ODR violations**: inlining picks a different definition ([P55](#p55-two-definitions-of-an-inline-function)).
- **Not UB but also optimization-dependent**: floating-point contraction and vectorized reductions reorder arithmetic.

**M2.3**

| Tool | Catches | Blind spots |
|---|---|---|
| ASan (+LSan) | Heap, stack, and global out-of-bounds; use-after-free; use-after-scope; leaks | Uninitialized reads; races; memory still inside a live allocation (the SSO case in [B1](#round-b-answers-code-review)) |
| UBSan | Signed overflow, invalid shifts, misaligned access, null dereference, bad enum/bool values | Most memory errors; strict aliasing |
| TSan | Data races and lock-order inversions | Only races on paths that actually execute; about 5-15x slowdown; cannot be combined with ASan |
| MSan (Clang only) | Uninitialized reads | Requires every library, including libc++, to be instrumented |
| Valgrind memcheck | Uninitialized reads that affect control flow, invalid accesses, leaks, with no rebuild | About 20-30x slower; does not detect stack-array overruns |
| `-D_GLIBCXX_ASSERTIONS` | Bounds checks in `vector::operator[]`, null `unique_ptr` dereference, and similar | Raw arrays and pointers |
| `-Wall -Wextra -Werror` | Many cases at compile time | Anything that needs runtime values |

**M2.4** Repeat at volume and perturb the timing:
- `ctest -R name --repeat until-fail:500` (CMake 3.17+), or `./tests --gtest_filter=... --gtest_repeat=1000 --gtest_break_on_failure` so it stops in a debugger.
- Add load (`stress-ng --cpu 0`), pin to fewer cores (`taskset -c 0`), or run under TSan, which changes the scheduling.
- Record it with `rr record --chaos`, which randomizes scheduling, then replay the failing run deterministically and step backward from the failure.

See [Debugging 18](../tools/Debugging_and_Profiling_Tools.md#18-scientific-debugging-and-bisecting).

**M2.5** It is an **order dependency**: one test leaves state that another depends on. Usual causes are function-local statics and singletons, global configuration or environment variables changed and not restored, a fixed temp-file path, a mock or registry not reset, and a locale or `std::cout` format flag left set. Reproduce it with `--gtest_shuffle --gtest_random_seed=<seed>`, bisect the test list with `--gtest_filter` to find the polluting test, then make the tests hermetic: fixtures that save and restore, a unique temp directory per test, and injected dependencies instead of globals.

**M2.6** `git bisect start <bad> <good>`, then `git bisect run ./check.sh`. The script builds, runs the test about 200 times, and exits 0 for good, 1-124 for bad, and **125 to skip** commits that do not build. With 300 commits that is about 9 steps (log2 of 300 is about 8.2). Make the script's repeat count high enough that "good" really means good, or the bisect converges on the wrong commit.

**M2.7** Floating-point addition is not associative. At `-O2` and above, GCC and Clang may vectorize a reduction only when allowed to reassociate (`-ffast-math` or `-fassociative-math`), and they may fuse `a*b + c` into an FMA instruction when the target has one, under `-ffp-contract` (whose default differs between GCC and Clang and by language mode). Both change the last bits. A different summation order on another machine, thread count, or GPU block size does the same. `EXPECT_EQ` on doubles is almost always wrong. Use `EXPECT_DOUBLE_EQ` (within 4 ULPs) only for results of a single operation. For reductions, use `EXPECT_NEAR` with a tolerance derived from the problem: the error of a naive sum of n terms grows roughly with n times machine epsilon times the sum of absolute values. Or use a combined `|a - b| <= atol + rtol * |b|` check.

**M2.8**
- A CI matrix with an ASan+UBSan job and a TSan job, plus a **Release-with-assertions** job (`-O2` without `-DNDEBUG`), since that is where optimization-sensitive bugs show up.
- `-Wall -Wextra -Werror` on project code.
- A nightly job running the suite with `--gtest_shuffle --gtest_repeat=20` that files tickets with the seed.
- A quarantine policy for flaky tests (tracked, with an owner and a deadline) instead of automatic retries that hide real races.

##### Chain M3 Answers: Broken After Install

**M3.1** In the build tree, CMake links with a **build RPATH** containing the absolute build directory, which is why `./build/kstats_cli` works. At install time CMake rewrites the RPATH to the **install RPATH, which is empty by default**. The installed binary has no path to `/opt/kstats/lib`, which is not a system directory, so `ld.so` fails. See [CMake 65.2](../tools/CMake_Fundamentals.md#652-cmakes-model-build-rpath-vs-install-rpath).

**M3.2** Set `CMAKE_INSTALL_RPATH "$ORIGIN/../${CMAKE_INSTALL_LIBDIR}"` **before** any `add_library` or `add_executable` call, because it initializes each target's `INSTALL_RPATH` property when the target is created. `$ORIGIN` expands at load time to the directory of the binary, so the tree is relocatable. Libraries that depend on sibling libraries need their own `$ORIGIN` entry, because `RUNPATH` is not inherited.

**M3.3**
- `readelf -d /opt/kstats/bin/kstats_cli | grep -E 'NEEDED|RPATH|RUNPATH'` shows what the binary asks for and where it looks.
- `ldd` shows the resolution result and which entry is "not found".
- `LD_DEBUG=libs ./kstats_cli 2>&1 | grep kstats` shows the loader's actual search, path by path.
- For transitive failures, run `readelf -d` on the *intermediate* library.

See [CMake 65.4](../tools/CMake_Fundamentals.md#654-diagnosing-cannot-open-shared-object-file).

**M3.4** The search order is `DT_RPATH` (only if there is no `DT_RUNPATH`), then `LD_LIBRARY_PATH`, then `DT_RUNPATH`, then `/etc/ld.so.cache`, then the default directories. Modern linkers emit `RUNPATH`, so **`LD_LIBRARY_PATH` wins** and the stale ROCm is loaded. Diagnose with `LD_DEBUG=libs`, and fix the user's environment or ship a launcher script that sanitizes it. Switching back to `RPATH` would also override `LD_LIBRARY_PATH`, but it removes the user's escape hatch and is deprecated. On machines with several ROCm installs, this is one of the most common causes of "works for me".

**M3.5** Install a **package configuration**:
- `install(TARGETS kstats EXPORT kstatsTargets ...)`, then `install(EXPORT kstatsTargets NAMESPACE kstats:: DESTINATION lib/cmake/kstats)`.
- `kstatsConfig.cmake`, generated with `configure_package_config_file`.
- `kstatsConfigVersion.cmake`, generated with `write_basic_package_version_file`.

The consumer passes `-DCMAKE_PREFIX_PATH=/opt/kstats`, or `-Dkstats_DIR=/opt/kstats/lib/cmake/kstats`. `find_package` searches `<prefix>/lib/cmake/<name>/` among other locations. See [CMake 38](../tools/CMake_Fundamentals.md#38-exporting-targets-and-generating-config-files).

**M3.6** The library's include directory was given as an absolute **source-tree** path (for example `target_include_directories(kstats PUBLIC ${CMAKE_SOURCE_DIR}/include)`), and that path was exported verbatim. It exists on the developer's machine, not on the consumer's. Wrap the paths with `$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>` and `$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>`, or use `FILE_SET HEADERS`, which handles both. See [CMake 19](../tools/CMake_Fundamentals.md#19-build_interface-vs-install_interface).

**M3.7** Causes, and how to tell them apart:
1. **Hidden visibility.** The library is built with `-fvisibility=hidden` and `Collector::start` lacks the export macro. `nm -C` shows the symbol (it is in `.symtab`), but `nm -D -C --defined-only libkstats.so` does not (it is not in `.dynsym`).
2. **Dual-ABI mismatch.** One side was built with `_GLIBCXX_USE_CXX11_ABI=0`, so the library exports `start(std::string const&)` while the consumer wants `start(std::__cxx11::basic_string<...> const&)`. `nm -D libkstats.so | c++filt | grep start` shows the exact signature.
3. **Signature or namespace drift.** The header and the library are from different versions (for example a stale header in `/usr/local/include`). Compare the mangled names.
4. **Link order or a missing library** when linking static archives with GNU ld: the archive is listed before the object that needs it, or not at all. Check the actual link line with `ninja -v` or `make VERBOSE=1`.

Also possible: a C/C++ linkage mismatch (`extern "C"` on one side only) shows up as a mangled versus unmangled name. See [C++ 13.11](../languages/Cpp_Fundamentals.md#1311-symbol-visibility-and-export-control) and [C++ 13.13](../languages/Cpp_Fundamentals.md#1313-abi-stability-and-the-libstdc-dual-abi).

**M3.8** The exported `kstatsTargets.cmake` references `Threads::Threads`, but nothing in the consumer created that imported target. In `kstatsConfig.cmake.in`, before including the targets file, add `include(CMakeFindDependencyMacro)` and `find_dependency(Threads)`, with one `find_dependency` per package that appears in the exported link interface. This happens when the dependency is `PUBLIC`/`INTERFACE`, or when `kstats` is a static library (its `PRIVATE` dependencies are exported as `$<LINK_ONLY:...>`).

**M3.9**
- `libkstats.so.1.2.0` is the **real file**.
- `libkstats.so.1` is the **SONAME** link. The linker records it in consumers' `DT_NEEDED`, and the loader uses it at runtime.
- `libkstats.so` is the **development link** that `-lkstats` finds at link time (shipped in `-dev` packages).

Bump the SOVERSION on every **ABI break**: removing or changing an exported function's signature, changing the layout of a public struct or class (members, base classes, the virtual function list or order), or changing an inline function's behavior that consumers compiled in. Adding new exported functions is compatible, so bump only the minor version.

##### Chain M4 Answers: Testing a Profiler's Analysis Pipeline

**M4.1** Use a test pyramid that mirrors the pipeline stages:
- **Many fast unit tests** for pure functions: metric formulas, unit conversions, counter-name parsing, CSV escaping.
- **Component tests** that feed *recorded* raw counter dumps from real runs into the analysis stage.
- **Golden-file tests** on the generated reports.
- **A few end-to-end tests** on real GPUs that run a known kernel (for example a STREAM-like copy whose bandwidth is predictable) and check that the metrics land in a plausible range.

Keep GPU-dependent code behind a thin interface so 90%+ of the tests run anywhere. See [C++ Testing 37](../languages/CPP_Testing.md#37-designing-for-testability).

**M4.2** Use **dependency injection**. The analysis stage depends on a `CounterSource` interface, not on the runtime. Tests pass a **fake** that replays recorded values, or a GoogleMock **mock** when the *interaction* matters, for example that the counters are split into passes so that no pass exceeds the hardware's counter-slot limit. The metric functions themselves should be pure (counters in, metric out) and tested with hand-computed cases, such as: bytes = 4 GiB in time = 1 ms, so bandwidth = 4 GiB / 1 ms, which is about 4.29 TB/s.

**M4.3** Use `EXPECT_NEAR(actual, expected, tol)` or a custom `|a - b| <= atol + rtol * |b|` check. A purely relative tolerance fails **near zero**: when `expected` is 0 (an idle unit, a 0% stall metric), any nonzero rounding error is an infinite relative error. A purely absolute tolerance fails for **large magnitudes**: an `atol` of 1e-6 on a value of 1e12 asks for more precision than a `double` has (the spacing between adjacent doubles near 1e12 is about 1.2e-4). Choose `rtol` from the computation (for example 1e-9 for a few arithmetic operations, looser for reductions), and `atol` from the meaningful resolution of the metric.

**M4.4** **Normalize, then compare structurally.**
- Normalize: replace timestamps, PIDs, hostnames, absolute paths, and GPU marketing names with placeholders (`<TS>`, `<PID>`, `<PATH>`), and sort rows whose order is not part of the contract.
- Compare: parse both CSVs and compare text columns exactly and numeric columns with a tolerance, rather than diffing bytes.
- Update workflow: an environment variable (for example `UPDATE_GOLDEN=1`) rewrites the golden files, and the diff is reviewed in the pull request like code.

See [C++ Testing 42](../languages/CPP_Testing.md#42-golden-file-snapshot-and-approval-testing).

**M4.5**
- **Skip, don't fail**: check `hipGetDeviceCount` in `SetUpTestSuite` or a helper and call `GTEST_SKIP() << "no GPU"`. CTest can map a skip string to a "skipped" status with the `SKIP_REGULAR_EXPRESSION` property.
- **Label** the GPU tests (`LABELS gpu`) so CPU runners can use `ctest -LE gpu`.
- **Do not oversubscribe**: use CTest **resource groups** (CMake 3.16+). Give each GPU test a `RESOURCE_GROUPS "gpus:1"` property and pass `--resource-spec-file` describing 2 GPUs. CTest then runs at most two GPU tests at a time and tells each one which GPU to use through `CTEST_RESOURCE_GROUP_*` environment variables, which the test maps to `HIP_VISIBLE_DEVICES`.

**M4.6**
- Compare against a **CPU reference** implementation, with tolerances chosen as in M4.3.
- Sizes: 0, 1, one less than, equal to, and one more than the block size; not a multiple of the wavefront size (64 on CDNA); and large enough to need many workgroups.
- Fixed **seeds** for random inputs, and log the seed on failure.
- Edge values: NaN, Inf, denormals, and negative zero when the kernel does arithmetic.
- **Error checks**: `hipGetLastError()` right after the launch (catches launch-configuration errors) and the return value of `hipDeviceSynchronize()` or `hipStreamSynchronize()` (catches execution faults).
- Guard buffers: allocate extra padding, fill it with a sentinel, and check it is untouched, to catch out-of-bounds writes.

**M4.7**
- Use a **microbenchmark** with Google Benchmark: `benchmark::DoNotOptimize` and `ClobberMemory` so the work is not optimized away, warm-up and repetitions, and the **median** with its variance reported.
- Run it on a **dedicated, quiet runner**: fixed CPU frequency (performance governor, turbo off), pinned cores, and fixed GPU clocks where possible.
- Compare against a stored baseline with a **statistical test** (Google Benchmark's `compare.py` supports a Mann-Whitney U test) and a threshold larger than the measured noise, for example fail at a slowdown above 5% with p < 0.05.

Timing a unit test on shared CI VMs fails because noisy neighbors and frequency scaling produce 10-30% jitter, so the gate either flakes or is set so loose that it catches nothing. See [C++ Testing 43](../languages/CPP_Testing.md#43-microbenchmarking-with-google-benchmark).

**M4.8** Coverage says which lines **ran**, not whether any assertion would **notice** if they were wrong. A test that calls the metric function and asserts nothing gets 100% coverage. It also misses untested *combinations* (branch coverage helps a bit) and code that is missing entirely, such as an unhandled error path. Measure test strength with **mutation testing** (Mull for C++): it injects small bugs, for example turning `+` into `-` or `<` into `<=`, and reports the mutants that no test catches. Then target those gaps, especially the metric formulas, where a silent wrong answer is the worst failure a profiler can have.

##### Chain M5 Answers: A Header Change Rebuilds Everything

**M5.1** Every translation unit that transitively includes `types.hpp` depends on it, so the build system must recompile all of them. A widely included header with frequently edited content is the worst case. To find the offenders:
- `ninja -t deps <obj>` lists the headers each object depends on, and `ninja -d explain` shows why something rebuilds.
- GCC `-H` prints the include tree with depth.
- Clang `-ftime-trace` with ClangBuildAnalyzer ranks headers by total parse time across the build.
- include-what-you-use suggests removable includes.

Rank by (number of includers) times (parse cost), and by how often the header changes.

**M5.2**
- **Forward-declare** instead of including when you only use pointers or references.
- **Split** large headers: a `fwd.hpp`, plus types separate from functions.
- Keep heavy headers (`<iostream>`, `<regex>`, `<ranges>`, big template libraries) out of public headers.
- Move function bodies and non-template code to `.cpp` files.
- Use **`extern template`** declarations so common instantiations are compiled once.
- Prefer **pimpl** for classes with heavy private members.
- Separate rarely changing interfaces from frequently changing implementation details.

**M5.3** The class holds `std::unique_ptr<Impl>` and declares `struct Impl;` only in the header; all private members live in `Impl` in the `.cpp`. Benefits: a **compilation firewall** (private changes do not recompile clients) and a **stable ABI** (the object's layout is one pointer). Costs: a heap allocation per object, an extra indirection on every access, worse locality, and more boilerplate. The classic error is "invalid application of `sizeof` to incomplete type `Impl`": the implicitly defined destructor (and move assignment) is generated **in the header**, where `Impl` is incomplete, so `unique_ptr`'s deleter cannot be instantiated. Fix it by *declaring* `~Widget();` (and the move operations) in the header and defining them as `= default` in the `.cpp` after `Impl` is complete.

**M5.4**

| Lever | Helps | Pitfall |
|---|---|---|
| Ninja instead of Makefiles | Faster no-op and incremental builds, better parallelism | None worth mentioning; use `-G Ninja` |
| ccache or sccache (`CMAKE_CXX_COMPILER_LAUNCHER`) | Clean rebuilds, CI, branch switching | Misses when flags, absolute paths (set `CCACHE_BASEDIR`), or `__DATE__`/`__TIME__` differ; does not help a genuinely changed header |
| Precompiled headers (`target_precompile_headers`, 3.16+) | Heavy, stable headers parsed once | Putting a frequently changing header in the PCH rebuilds everything, which is the opposite of the goal |
| Unity builds (`CMAKE_UNITY_BUILD`, 3.16+) | Fewer TUs, so less repeated header parsing | Anonymous-namespace and `static` name collisions between merged files, leaking macros and `using` directives, coarser incremental rebuilds |
| Distributed builds (sccache dist, distcc, icecream) | Wide parallelism | Network and toolchain-consistency overhead |

**M5.5** Link time: switch to **lld** or **mold** (`-fuse-ld=mold`, or `CMAKE_LINKER_TYPE` in CMake 3.29+), which are several times faster than GNU ld on large binaries. Use **`-gsplit-dwarf`**, which keeps debug info out of the link, so the linker processes far fewer bytes. Use **shared libraries in developer builds**, so a change relinks one `.so` instead of the whole executable. Keep **LTO** for release builds only, or use ThinLTO with a cache.

**M5.6** In principle yes: a module interface is compiled once into a binary module interface, and importers do not re-parse its text, so the cost of the header model goes away. CMake has supported named modules non-experimentally since **3.28**, with the Ninja generator (1.11+) and GCC 14+, Clang 16+, or MSVC (VS 2022 17.4+). In practice:
- Header units and `import std;` support are still uneven across toolchains.
- Third-party libraries mostly ship headers.
- Module dependencies force a scanning step and serialize some compilation.
- Changing a module *interface* still rebuilds all its importers.

So it is a migration project, not a flag. See [C++ 11.4](../languages/Cpp_Fundamentals.md#114-modules).

**M5.7** Treat build time as a tracked metric:
- CI records clean and incremental build times (and the ccache hit rate) per commit and alerts on regressions.
- A check limits what may be included from public headers (an include-what-you-use job, or a script that fails if `<iostream>` appears in `include/`).
- New dependencies get a build-time review.
- Run ClangBuildAnalyzer periodically and fix the top three offenders.

#### Round D Answers: Live Coding Model Solution

[Back to 12.5](#125-round-d-live-coding----a-scoped-timer-registry)

Verified with GCC 15.2, CMake 4.2.3, and GoogleTest 1.17.0: 4/4 tests pass, with no `-Wall -Wextra` warnings in the project code and no reports under `-fsanitize=thread`.

```cpp
// timer_registry.hpp
#pragma once
#include <chrono>
#include <cstdint>
#include <functional>
#include <map>
#include <mutex>
#include <string>
#include <utility>

struct TimerStat {
    std::uint64_t count = 0;
    std::chrono::nanoseconds total{0};
    std::chrono::nanoseconds max{0};
};

class TimerRegistry {
public:
    using Clock = std::function<std::chrono::nanoseconds()>;

    static std::chrono::nanoseconds steady_now() {
        return std::chrono::steady_clock::now().time_since_epoch();
    }

    explicit TimerRegistry(Clock now = &TimerRegistry::steady_now) : now_(std::move(now)) {}

    std::chrono::nanoseconds now() const { return now_(); }

    void record(const std::string& name, std::chrono::nanoseconds d) {
        std::lock_guard lock(mu_);
        TimerStat& s = stats_[name];
        ++s.count;
        s.total += d;
        if (d > s.max) s.max = d;
    }

    std::map<std::string, TimerStat> snapshot() const {
        std::lock_guard lock(mu_);
        return stats_;                    // copy under the lock; caller owns the result
    }

private:
    Clock now_;
    mutable std::mutex mu_;
    std::map<std::string, TimerStat> stats_;
};

class ScopedTimer {
public:
    ScopedTimer(TimerRegistry& reg, std::string name)
        : reg_(reg), name_(std::move(name)), start_(reg.now()) {}

    ~ScopedTimer() {                      // implicitly noexcept
        try {
            reg_.record(name_, reg_.now() - start_);
        } catch (...) {
            // record() can throw std::bad_alloc; a destructor must not let it escape.
        }
    }

    ScopedTimer(const ScopedTimer&) = delete;
    ScopedTimer& operator=(const ScopedTimer&) = delete;

private:
    TimerRegistry& reg_;
    std::string name_;
    std::chrono::nanoseconds start_;
};
```

```cpp
// timer_registry_test.cpp
#include "timer_registry.hpp"

#include <gtest/gtest.h>

#include <chrono>
#include <stdexcept>
#include <thread>
#include <vector>

using namespace std::chrono_literals;

class TimerRegistryTest : public ::testing::Test {
protected:
    std::chrono::nanoseconds fake_now_{0};
    TimerRegistry reg_{[this] { return fake_now_; }};   // injected fake clock
};

TEST_F(TimerRegistryTest, RecordsCountTotalAndMax) {
    {
        ScopedTimer t(reg_, "parse");
        fake_now_ += 30ns;
    }
    {
        ScopedTimer t(reg_, "parse");
        fake_now_ += 70ns;
    }
    const auto snap = reg_.snapshot();
    ASSERT_EQ(snap.count("parse"), 1u);
    const TimerStat& s = snap.at("parse");
    EXPECT_EQ(s.count, 2u);
    EXPECT_EQ(s.total, 100ns);
    EXPECT_EQ(s.max, 70ns);
}

TEST_F(TimerRegistryTest, NestedScopesAreIndependent) {
    {
        ScopedTimer outer(reg_, "outer");
        fake_now_ += 10ns;
        {
            ScopedTimer inner(reg_, "inner");
            fake_now_ += 5ns;
        }
    }
    const auto snap = reg_.snapshot();
    EXPECT_EQ(snap.at("outer").total, 15ns);
    EXPECT_EQ(snap.at("inner").total, 5ns);
}

TEST_F(TimerRegistryTest, RecordsEvenWhenScopeExitsByException) {
    EXPECT_THROW(
        {
            ScopedTimer t(reg_, "failing");
            fake_now_ += 42ns;
            throw std::runtime_error("boom");
        },
        std::runtime_error);
    EXPECT_EQ(reg_.snapshot().at("failing").total, 42ns);
}

TEST(TimerRegistryConcurrency, CountsAreExactUnderContention) {
    TimerRegistry reg;                    // real steady clock
    constexpr int kThreads = 8;
    constexpr int kIters = 10'000;
    std::vector<std::thread> threads;
    for (int t = 0; t < kThreads; ++t)
        threads.emplace_back([&reg] {
            for (int i = 0; i < kIters; ++i) ScopedTimer s(reg, "hot");
        });
    for (auto& th : threads) th.join();
    EXPECT_EQ(reg.snapshot().at("hot").count, std::uint64_t{kThreads} * kIters);
}
```

```cmake
cmake_minimum_required(VERSION 3.24)
project(timer_registry LANGUAGES CXX)

enable_testing()

include(FetchContent)
FetchContent_Declare(googletest
  GIT_REPOSITORY https://github.com/google/googletest.git
  GIT_TAG        v1.17.0)
FetchContent_MakeAvailable(googletest)

find_package(Threads REQUIRED)

add_library(timer_registry INTERFACE)
target_include_directories(timer_registry INTERFACE ${CMAKE_CURRENT_SOURCE_DIR})
target_compile_features(timer_registry INTERFACE cxx_std_20)
target_link_libraries(timer_registry INTERFACE Threads::Threads)

add_executable(timer_registry_test timer_registry_test.cpp)
target_link_libraries(timer_registry_test PRIVATE timer_registry GTest::gtest_main)

include(GoogleTest)
gtest_discover_tests(timer_registry_test)
```

```bash
cmake -S . -B build -G Ninja && cmake --build build && ctest --test-dir build --output-on-failure
# Race check: a separate TSan build of the same tests
cmake -S . -B build-tsan -G Ninja -DCMAKE_CXX_FLAGS="-fsanitize=thread -g" && cmake --build build-tsan
./build-tsan/timer_registry_test --gtest_repeat=20
```

Design points worth saying while you code:
- **The fake clock is a member of the fixture**, declared *before* `reg_` so it is initialized first. The lambda captures `this` and reads the current value at each call.
- **`ScopedTimer` holds a reference** to the registry, so the registry must outlive every timer. That is the contract of RAII guards such as `std::lock_guard`.
- **`snapshot()` returns by value**, so callers never hold references into a map that another thread is modifying.
- GoogleTest 1.17 requires C++17 or later; the `cxx_std_20` requirement on the interface target covers that.

**Follow-up answers.**

**D1.** Per scope you pay for:
- two clock reads (`clock_gettime(CLOCK_MONOTONIC)` through the vDSO, typically a few tens of nanoseconds each);
- two indirect calls through `std::function`;
- a `std::string` construction (free for names of up to 15 characters thanks to SSO, a heap allocation otherwise);
- a mutex lock (cheap when uncontended, microseconds when threads fight over it);
- an `O(log n)` map lookup with string comparisons.

To get to a few nanoseconds:
- make the clock a template parameter so the call inlines;
- register names once and use small integer IDs (`static const auto id = reg.intern("parse");`);
- accumulate in **`thread_local`** per-thread arrays with no locks, merged in `snapshot()`;
- optionally read the TSC directly (`rdtsc`, invariant TSC) and convert to time once.

This is how production tracers keep their probe effect small, and why profilers report their own overhead.

**D2.** `steady_clock` is monotonic: NTP adjustments and manual clock changes cannot make it jump, so a duration is never negative or inflated. `system_clock` is wall time and can jump either way. In libstdc++, `high_resolution_clock` is an alias of `system_clock` (verified with a `static_assert` on GCC 15), so it has the same problem. Use `system_clock` only to timestamp events for humans or for correlation across machines.

**D3.** Destructors are implicitly `noexcept`. `record()` can throw `std::bad_alloc` (the map node or the string copy), and an exception escaping a `noexcept` function calls `std::terminate`. If the destructor runs *during* stack unwinding from another exception, a second exception terminates no matter what ([P52](#p52-throwing-from-a-destructor), [P53](#p53-noexceptfalse-destructors-and-unwinding)). Swallowing, plus incrementing a "dropped samples" counter, is the right tradeoff for telemetry.

**D4.** Usually yes: the time was spent, and hiding failing paths biases the profile. To distinguish them, capture `std::uncaught_exceptions()` in the constructor and compare in the destructor. If the count went up, the scope is exiting by exception, so record under `name + "/failed"` or set a flag in the stat. That is the same mechanism `scope_fail` and `scope_success` guards use.

**D5.** **Static destruction order.** A global or function-local static registry is destroyed at exit, in reverse order of construction. A `ScopedTimer` running in another static object's destructor, or in a detached thread still running at exit, would then use a destroyed registry, which is UB. Fixes:
- **Intentionally leak** it: `TimerRegistry& timers() { static auto* r = new TimerRegistry; return *r; }`. Construction is thread-safe (a function-local static), and it is never destroyed.
- Flush the results explicitly from `main` (or an `atexit` handler registered after construction) before shutdown.

**D6.** It measures **enqueue time** only, typically a few microseconds: kernel launches are asynchronous, so the host returns as soon as the dispatch packet is written. To time the kernel itself:
- record `hipEventRecord` before and after on the same stream and read `hipEventElapsedTime`;
- or synchronize before stopping the timer, which serializes the pipeline and perturbs what you measure;
- or, best for analysis, use **rocprofv3** kernel tracing, which reports GPU begin and end timestamps per dispatch without changing the code.

The first launch also includes code-object loading, so warm up before timing. See [CS Fundamentals Drills, Chain 3](CS_Fundamentals_Drills.md#chain-3-what-happens-when-you-launch-a-hip-kernel).

**D7.** No. A passing stress test only shows that this run, on this machine, with this scheduling, produced the right count. Races can hide behind timing, and x86's strong memory ordering hides missing barriers that weaker architectures would expose. Evidence comes from **TSan** (which flags the race even when the result happened to be right), plus code review of what the mutex protects. Run the stress test under TSan with repeats in CI ([C++ Testing 40.6](../languages/CPP_Testing.md#406-tsan-in-ci-repeat-and-shuffle)).

**D8.** Copying would make two timers record the same interval twice. Moving needs a "disengaged" state: hold a `TimerRegistry*` instead of a reference, null it in the moved-from object, and have the destructor skip recording when the pointer is null. Moving is rarely needed. Since C++17, guaranteed copy elision lets a factory like `ScopedTimer make_timer(...)` return a prvalue of a non-movable type, so deleting both operations costs nothing.
