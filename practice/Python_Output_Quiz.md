# Python Output Quiz -- 49 "What Does This Print?" Puzzles

> Last reviewed: 2026-11 · Versions assumed: CPython 3.14 (default GIL build). Every snippet was run with `python3 -I` on CPython 3.14.4. Where 3.12 behaves differently, the answer says so. Behaviour that is a CPython implementation detail rather than a language guarantee is marked **[CPython-specific]**.

Each puzzle is a complete program. Write down the exact output (and any exception) before you open the [Answers](#answers). Every answer explains *why*, and most add the follow-up question an interviewer would ask next.

See also: [Python Fundamentals -- Common Gotchas](../languages/Python_Fundamentals.md#27-common-gotchas--best-practices) · [C++ Output Quiz](Cpp_Output_Quiz.md) · [Flashcards](Flashcards.csv)

## Table of Contents

1. [How to Use This Quiz](#1-how-to-use-this-quiz)
2. [Functions, Closures & Default Arguments](#2-functions-closures--default-arguments) (P1-P3)
3. [Lists, Tuples & Aliasing](#3-lists-tuples--aliasing) (P4-P9)
4. [Dicts, Sets & Unpacking](#4-dicts-sets--unpacking) (P10-P14)
5. [Copying, Sorting & Strings](#5-copying-sorting--strings) (P15-P17)
6. [Identity, Equality & Numbers](#6-identity-equality--numbers) (P18-P27)
7. [Control Flow & Exceptions](#7-control-flow--exceptions) (P28-P31)
8. [Iterators, Generators & Comprehensions](#8-iterators-generators--comprehensions) (P32-P36)
9. [Scope Rules](#9-scope-rules) (P37-P38)
10. [Classes, Attributes & the MRO](#10-classes-attributes--the-mro) (P39-P46)
11. [Concurrency & Async](#11-concurrency--async) (P47-P49)
12. [Topic Index](#12-topic-index)
- [Answers](#answers)

---

## 1. How to Use This Quiz

- **Predict first, then run.** Saying "it prints something like..." does not count. Interviewers expect the exact output, including brackets, quotes, and the order of lines.
- **Name the rule.** For each puzzle, be able to state the rule in one sentence (for example, "default values are evaluated once, when `def` runs"). That sentence is what the interviewer is really testing.
- **Know which facts are about CPython.** Small-int caching, string interning, `hash(-1)`, and how often the GIL switches threads are CPython details. Say so out loud in an interview. It shows you know the difference between the language specification and one implementation of it.
- **Scoring:** 40+ correct is strong. Below 30 means you should re-read [Python Fundamentals Part 1 and Part 2](../languages/Python_Fundamentals.md#1-python-data-model--object-system).

---

## 2. Functions, Closures & Default Arguments

### P1. Mutable default argument

```python
def append_to(x, bucket=[]):
    bucket.append(x)
    return bucket


a = append_to(1)
b = append_to(2)
print(a, b, a is b)
print(append_to(3, []))
print(append_to.__defaults__)
```

[Answer](#a1-mutable-default-argument)

### P2. Lambdas in a comprehension

```python
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])

funcs = [lambda i=i: i for i in range(3)]
print([f() for f in funcs])

funcs = [lambda x, k=k: x * k for k in (10, 20)]
print([f(2) for f in funcs])
```

[Answer](#a2-lambdas-in-a-comprehension)

### P3. Closures created in a for loop

```python
callbacks = []
for name in ["a", "b", "c"]:
    def cb():
        return name.upper()
    callbacks.append(cb)

print([cb() for cb in callbacks])
name = "z"
print([cb() for cb in callbacks])
print(callbacks[0].__closure__)
```

[Answer](#a3-closures-created-in-a-for-loop)

---

## 3. Lists, Tuples & Aliasing

### P4. `+=` versus `+` on a shared list

```python
a = [1, 2]
b = a
a += [3]
print(a, b)
a = a + [4]
print(a, b)

s = "ab"
t = s
s += "c"
print(s, t)
```

[Answer](#a4--versus--on-a-shared-list)

### P5. Grid built with list multiplication

```python
grid = [[0] * 3] * 3
grid[0][0] = 1
print(grid)
print(len({id(row) for row in grid}))

good = [[0] * 3 for _ in range(3)]
good[0][0] = 1
print(good)
```

[Answer](#a5-grid-built-with-list-multiplication)

### P6. Augmented assignment on a list inside a tuple

```python
t = (1, [2, 3])
try:
    t[1] += [4]
except TypeError as e:
    print("TypeError:", e)
print(t)

t[1].extend([5])
print(t)
```

[Answer](#a6-augmented-assignment-on-a-list-inside-a-tuple)

### P7. Removing from a list while iterating over it

```python
nums = [1, 2, 2, 3, 4]
for n in nums:
    if n % 2 == 0:
        nums.remove(n)
print(nums)

nums = [1, 2, 2, 3, 4]
nums = [n for n in nums if n % 2]
print(nums)
```

[Answer](#a7-removing-from-a-list-while-iterating-over-it)

### P8. In-place methods return None

```python
data = [3, 1, 2]
result = data.sort()
print(result, data)

data = data.append(4)
print(data)

print(sorted("cab"), "".join(reversed("cab")))
```

[Answer](#a8-in-place-methods-return-none)

### P9. Commas make tuples

```python
t = (1)
u = 1,
print(type(t).__name__, type(u).__name__, u)

x = 1, 2 == (1, 2)
print(x)

print(type(()).__name__, len(((),)))
```

[Answer](#a9-commas-make-tuples)

---

## 4. Dicts, Sets & Unpacking

### P10. Mutating a dict while iterating over it

```python
d = {"a": 1, "b": 2, "c": 3}
try:
    for k in d:
        if d[k] == 2:
            del d[k]
except RuntimeError as e:
    print("RuntimeError:", e)
print(d)

for k in d:
    d[k] *= 10
print(d)

for k in list(d):
    if d[k] > 10:
        del d[k]
print(d)
```

[Answer](#a10-mutating-a-dict-while-iterating-over-it)

### P11. Dict insertion order

```python
d = {"b": 1, "a": 2}
d["c"] = 3
d["b"] = 10
print(list(d))

del d["a"]
d["a"] = 0
print(d)

print({"x": 1, "y": 2} == {"y": 2, "x": 1})

from collections import OrderedDict
print(OrderedDict(x=1, y=2) == OrderedDict(y=2, x=1))
print(OrderedDict(x=1, y=2) == {"y": 2, "x": 1})
```

[Answer](#a11-dict-insertion-order)

### P12. defaultdict creates keys when you read them

```python
from collections import defaultdict

dd = defaultdict(list)
print("k" in dd)
dd["k"]
print("k" in dd, dict(dd))
print(dd.get("m"), len(dd))

counts = defaultdict(int)
for ch in "banana":
    counts[ch] += 1
print(dict(counts))
```

[Answer](#a12-defaultdict-creates-keys-when-you-read-them)

### P13. Set ordering

```python
print({3, 1, 2})
print({8, 1})
print({10, 2, 18})
print(sorted({"pear", "apple", "fig"}))
print({"pear", "apple", "fig"})
```

[Answer](#a13-set-ordering)

### P14. Star-unpacking

```python
first, *middle, last = range(5)
print(first, middle, last)

*a, b = "x"
print(a, b)

head, *tail = (1,)
print(head, tail)

print(*[1, 2], *"ab", sep="-")
print({**{"a": 1, "b": 2}, **{"a": 9}})

try:
    p, *q, r = [1]
except ValueError as e:
    print("ValueError:", e)
```

[Answer](#a14-star-unpacking)

---

## 5. Copying, Sorting & Strings

### P15. Shallow copy versus deep copy

```python
import copy

orig = {"nums": [1, 2], "tag": "t"}
shallow = copy.copy(orig)
deep = copy.deepcopy(orig)

shallow["nums"].append(3)
shallow["tag"] = "s"
deep["nums"].append(99)

print(orig)
print(shallow)
print(deep)

rows = [[0, 0]] * 2
cloned = copy.deepcopy(rows)
cloned[0][0] = 7
print(cloned)
```

[Answer](#a15-shallow-copy-versus-deep-copy)

### P16. Sort stability and reverse

```python
people = [("bob", 25), ("alice", 30), ("carol", 25), ("dave", 30)]

by_age = sorted(people, key=lambda p: p[1])
print([n for n, _ in by_age])

print([n for n, _ in sorted(people, key=lambda p: p[1], reverse=True)])
print([n for n, _ in reversed(by_age)])

# Two-pass sort: by age descending, then by name ascending within each age
step1 = sorted(people, key=lambda p: p[0])
step2 = sorted(step1, key=lambda p: p[1], reverse=True)
print([n for n, _ in step2])
```

[Answer](#a16-sort-stability-and-reverse)

### P17. String multiplication

```python
print("ab" * 3)
print("ab" * 0 == "", "ab" * -2 == "")
print([1, 2] * 2)
print(3 * "-" + ">")
print("5" + "5", int("5") * 2, "5" * 2)
try:
    print("3" * "3")
except TypeError as e:
    print("TypeError:", e)
```

[Answer](#a17-string-multiplication)

---

## 6. Identity, Equality & Numbers

### P18. `is` with small integers [CPython-specific]

```python
a = 256
b = 256
print(a is b)

x = int("257")
y = int("257")
print(x is y, x == y)

print(int("-5") is int("-5"), int("-6") is int("-6"))
```

[Answer](#a18-is-with-small-integers-cpython-specific)

### P19. `is` with strings [CPython-specific]

```python
import sys

a = "hello"
b = "hello"
print(a is b)

c = "".join(["hel", "lo"])
print(a is c, a == c)
print(sys.intern(c) is a)

ns1, ns2 = {}, {}
exec(compile('s = "hello world!"', "<one>", "exec"), ns1)
exec(compile('s = "hello world!"', "<two>", "exec"), ns2)
print(ns1["s"] is ns2["s"], ns1["s"] == ns2["s"])
```

[Answer](#a19-is-with-strings-cpython-specific)

### P20. NaN in containers

```python
nan = float("nan")
print(nan == nan, nan is nan)
print([nan] == [nan], nan in [nan])
print([float("nan")] == [float("nan")])
print(len({nan, nan}), len({float("nan"), float("nan")}))
```

[Answer](#a20-nan-in-containers)

### P21. Chained comparisons

```python
print(1 < 2 < 3)
print(3 > 2 > 1 == 1)
print(1 < 3 > 2)
print((1 < 2) < 3, 1 < (2 < 3))
print(False == False in [False])
x = 5
print(1 < x < 10 != x)
```

[Answer](#a21-chained-comparisons)

### P22. `and` / `or` return operands

```python
print(0 or "default")
print("" or [] or None)
print(3 and 4)
print([] and undefined_name)
print(None or 0 and 5)
print(not [], not [0])


def timeout(seconds=None):
    return seconds or 30


print(timeout(5), timeout(0), timeout())
```

[Answer](#a22-and--or-return-operands)

### P23. Floating-point precision

```python
import math
from decimal import Decimal

print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)
print(math.isclose(0.1 + 0.2, 0.3))
total = 0.0
for _ in range(10):
    total += 0.1
print(total, sum([0.1] * 10), math.fsum([0.1] * 10))
print(1e16 + 1 == 1e16)
print(Decimal("0.1") + Decimal("0.2"), Decimal(0.1) == Decimal("0.1"))
```

[Answer](#a23-floating-point-precision)

### P24. Integer division and modulo with negative numbers

```python
import math

print(7 // 2, -7 // 2, 7 // -2)
print(7 % 3, -7 % 3, 7 % -3)
print(divmod(-7, 3))
print(int(-7 / 2), -7 / 2)
print(math.fmod(-7, 3))
print(-7.5 // 2)
```

[Answer](#a24-integer-division-and-modulo-with-negative-numbers)

### P25. `round()` and banker's rounding

```python
print(round(0.5), round(1.5), round(2.5), round(-0.5), round(-1.5))
print(round(2.675, 2))
print(round(7.0), type(round(7.0)).__name__, type(round(7.0, 1)).__name__)
print(int(2.7), int(-2.7))
```

[Answer](#a25-round-and-bankers-rounding)

### P26. `bool` is a subclass of `int`

```python
print(True + True, True * 10, sum([True, False, True]))
print(isinstance(True, int), type(True) is int)
print(["no", "yes"][True])

d = {1: "int", True: "bool", 1.0: "float"}
print(d)
print(hash(True) == hash(1) == hash(1.0))
```

[Answer](#a26-bool-is-a-subclass-of-int)

### P27. `hash(-1)` [CPython-specific]

```python
print(hash(-1), hash(-2), hash(-1) == hash(-2))
print(hash(0), hash(1), hash(2**61 - 1), hash(2**61))
d = {-1: "minus one", -2: "minus two"}
print(len(d), d[-1])
```

[Answer](#a27-hash-1-cpython-specific)

---

## 7. Control Flow & Exceptions

### P28. `return` inside `finally`

```python
def f():
    try:
        return "try"
    finally:
        return "finally"


def g():
    try:
        1 / 0
    finally:
        return "swallowed"


def h():
    x = 1
    try:
        return x
    finally:
        x = 2


print(f(), g(), h())
```

[Answer](#a28-return-inside-finally)

### P29. `else` on loops and `try`

```python
for i in range(3):
    if i == 5:
        break
else:
    print("for-else: no break")

for i in []:
    pass
else:
    print("for-else: empty loop")

n = 0
while n < 3:
    n += 1
    if n == 2:
        break
else:
    print("while-else")
print("n =", n)

try:
    pass
except Exception:
    print("except")
else:
    print("try-else")
finally:
    print("finally")
```

[Answer](#a29-else-on-loops-and-try)

### P30. Exception chaining

```python
def load():
    try:
        {}["key"]
    except KeyError as e:
        raise ValueError("bad config") from e


try:
    load()
except ValueError as err:
    print(type(err.__cause__).__name__, err.__suppress_context__)
    print(repr(err.__context__))

try:
    try:
        1 / 0
    except ZeroDivisionError:
        raise RuntimeError("oops") from None
except RuntimeError as err:
    print(err.__cause__, err.__suppress_context__, type(err.__context__).__name__)

try:
    try:
        1 / 0
    except ZeroDivisionError:
        raise KeyError("during handling")
except KeyError as err:
    print(err.__cause__, type(err.__context__).__name__)
```

[Answer](#a30-exception-chaining)

### P31. The `except ... as` name is deleted

```python
e = "outer"
try:
    1 / 0
except ZeroDivisionError as e:
    pass

try:
    print(e)
except NameError as err:
    print("NameError:", err)
```

[Answer](#a31-the-except--as-name-is-deleted)

---

## 8. Iterators, Generators & Comprehensions

### P32. Generator exhaustion

```python
squares = (x * x for x in range(4))
print(sum(squares))
print(sum(squares))
print(list(squares))

nums = map(int, "123")
print(2 in nums, list(nums))
```

[Answer](#a32-generator-exhaustion)

### P33. Iterator versus iterable

```python
data = [1, 2, 3]
it = iter(data)
print(list(zip(it, it)))


class Countdown:
    def __init__(self, n):
        self.n = n

    def __iter__(self):
        while self.n > 0:
            yield self.n
            self.n -= 1


c = Countdown(3)
print(list(c), list(c))

r = range(3)
print(list(r), list(r))
print(iter(it) is it, iter(data) is iter(data))
```

[Answer](#a33-iterator-versus-iterable)

### P34. When does a generator expression bind its names?

```python
x = [1, 2, 3]
g = (i * 10 for i in x)
x = [7, 8]
print(list(g))

y = [1, 2]
g2 = (a + b for a in y for b in y)
y = [100]
print(list(g2))
```

[Answer](#a34-when-does-a-generator-expression-bind-its-names)

### P35. Comprehension scope

```python
x = "outer"
squares = [x for x in range(3)]
print(x, squares)


class Config:
    n = 3
    ok = [i for i in range(n)]
    try:
        bad = [n * i for i in range(2)]
    except NameError as e:
        bad = f"NameError: {e}"


print(Config.ok)
print(Config.bad)
```

[Answer](#a35-comprehension-scope)

### P36. Walrus operator scope

```python
data = [3, 8, 1, 9]
if any((big := v) > 5 for v in data):
    print("first big:", big)

print([y := 10, y ** 2])

total = 0
partial = [total := total + v for v in data]
print(partial, total)

try:
    print(v)
except NameError:
    print("v is not defined")
```

[Answer](#a36-walrus-operator-scope)

---

## 9. Scope Rules

### P37. UnboundLocalError

```python
count = 0


def bump():
    count += 1
    return count


try:
    bump()
except UnboundLocalError as e:
    print(type(e).__name__, "-", e)

x = 10


def show():
    print(x)
    x = 20


try:
    show()
except UnboundLocalError:
    print("show() failed before printing anything")
```

[Answer](#a37-unboundlocalerror)

### P38. `global` versus `nonlocal`

```python
x = "global"


def outer():
    x = "enclosing"

    def inner_nonlocal():
        nonlocal x
        x = "changed by nonlocal"

    def inner_global():
        global x
        x = "changed by global"

    inner_nonlocal()
    print("outer sees:", x)
    inner_global()
    print("outer sees:", x)


outer()
print("module sees:", x)
```

[Answer](#a38-global-versus-nonlocal)

---

## 10. Classes, Attributes & the MRO

### P39. Class attributes versus instance attributes

```python
class Dog:
    tricks = []
    kind = "canine"

    def add(self, trick):
        self.tricks.append(trick)


a, b = Dog(), Dog()
a.add("roll")
b.add("sit")
a.kind = "wolf"

print(a.tricks, b.tricks is a.tricks)
print(a.kind, b.kind, Dog.kind)
Dog.kind = "mammal"
print(a.kind, b.kind)
print("kind" in vars(a), "kind" in vars(b))
```

[Answer](#a39-class-attributes-versus-instance-attributes)

### P40. `self.n += 1` on a class attribute

```python
class Counter:
    n = 0

    def inc(self):
        self.n += 1


c1, c2 = Counter(), Counter()
c1.inc()
c1.inc()
c2.inc()
print(c1.n, c2.n, Counter.n)
```

[Answer](#a40-selfn--1-on-a-class-attribute)

### P41. Diamond inheritance and `super()`

```python
class A:
    def hello(self):
        print("A")


class B(A):
    def hello(self):
        print("B")
        super().hello()


class C(A):
    def hello(self):
        print("C")
        super().hello()


class D(B, C):
    def hello(self):
        print("D")
        super().hello()


D().hello()
print([k.__name__ for k in D.__mro__])
print("--")
B().hello()
```

[Answer](#a41-diamond-inheritance-and-super)

### P42. An MRO that cannot be built

```python
class A:
    pass


class B(A):
    pass


try:
    class E(A, B):
        pass
except TypeError as e:
    print("TypeError:", e)


class F(B, A):
    pass


print([k.__name__ for k in F.__mro__])
```

[Answer](#a42-an-mro-that-cannot-be-built)

### P43. Equality without hashing

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)


print(Point(1, 2) == Point(1, 2))
print(Point.__hash__)
try:
    {Point(1, 2)}
except TypeError as e:
    print("TypeError:", e)


class Plain:
    pass


print(Plain() == Plain(), len({Plain(), Plain()}))
```

[Answer](#a43-equality-without-hashing)

### P44. Name mangling

```python
class Base:
    def __init__(self):
        self.__secret = "base"
        self._hint = "protected"

    def reveal(self):
        return self.__secret


class Child(Base):
    def __init__(self):
        super().__init__()
        self.__secret = "child"


c = Child()
print(c.reveal())
print(sorted(vars(c)))
print(c._Base__secret, c._Child__secret)
try:
    print(c.__secret)
except AttributeError:
    print("AttributeError")
```

[Answer](#a44-name-mangling)

### P45. Descriptor precedence

```python
class DataDesc:
    def __get__(self, obj, objtype=None):
        return "data descriptor"

    def __set__(self, obj, value):
        print("__set__ called with", value)


class NonDataDesc:
    def __get__(self, obj, objtype=None):
        return "non-data descriptor"


class Obj:
    d = DataDesc()
    n = NonDataDesc()


o = Obj()
o.__dict__["d"] = "instance dict"
o.__dict__["n"] = "instance dict"
print(o.d)
print(o.n)
o.d = 42
print(o.__dict__)
del o.__dict__["n"]
print(o.n)
```

[Answer](#a45-descriptor-precedence)

### P46. `__getattr__` versus `__getattribute__`

```python
class Lazy:
    def __init__(self):
        self.real = 1

    def __getattr__(self, name):
        return f"fallback:{name}"


class Spy:
    def __init__(self):
        self.real = 1

    def __getattribute__(self, name):
        print("get", name)
        return super().__getattribute__(name)


lazy = Lazy()
print(lazy.real, lazy.missing)
print(getattr(lazy, "__len__", "nope"))
try:
    len(lazy)
except TypeError as e:
    print("TypeError:", e)

spy = Spy()
print(spy.real)
```

[Answer](#a46-__getattr__-versus-__getattribute__)

---

## 11. Concurrency & Async

### P47. Forgetting `await`

```python
import asyncio


async def fetch():
    return 42


async def main():
    r = fetch()
    print(type(r).__name__)
    print(await r)
    r2 = fetch()
    print(asyncio.iscoroutine(r2), r2 == 42)


asyncio.run(main())
print("done")
```

[Answer](#a47-forgetting-await)

### P48. A blocking call inside a coroutine

```python
import asyncio
import time


async def good(name, delay):
    await asyncio.sleep(delay)
    print(name)


async def bad(name, delay):
    time.sleep(delay)
    print(name)


async def main():
    t0 = time.perf_counter()
    await asyncio.gather(good("good-slow", 0.2), good("good-fast", 0.1))
    print(f"good took ~{time.perf_counter() - t0:.1f}s")
    t0 = time.perf_counter()
    await asyncio.gather(bad("bad-slow", 0.2), bad("bad-fast", 0.1))
    print(f"bad took ~{time.perf_counter() - t0:.1f}s")


asyncio.run(main())
```

[Answer](#a48-a-blocking-call-inside-a-coroutine)

### P49. `counter += 1` from four threads

```python
import threading

counter = 0


def work(n):
    global counter
    for _ in range(n):
        counter += 1


threads = [threading.Thread(target=work, args=(200_000,)) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(counter, counter == 800_000)
```

Question: what does it print, and is that output *guaranteed*?

[Answer](#a49-counter--1-from-four-threads)

---

## 12. Topic Index

| Topic | Puzzles | Background reading |
|-------|---------|--------------------|
| Mutable defaults, late binding, closures | P1, P2, P3 | [Functions In Depth](../languages/Python_Fundamentals.md#5-functions-in-depth), [Gotchas](../languages/Python_Fundamentals.md#27-common-gotchas--best-practices) |
| Aliasing, `+=`, list multiplication, tuples | P4, P5, P6, P9, P17 | [Data Model](../languages/Python_Fundamentals.md#1-python-data-model--object-system), [Built-in Types](../languages/Python_Fundamentals.md#2-built-in-data-types--structures) |
| Mutation during iteration | P7, P10 | [Control Flow & Looping](../languages/Python_Fundamentals.md#4-control-flow--looping) |
| Dict/set ordering, hashing, `defaultdict` | P11, P12, P13, P26, P27, P43 | [Built-in Types](../languages/Python_Fundamentals.md#2-built-in-data-types--structures) |
| Unpacking, copying, sorting | P8, P14, P15, P16 | [Copy Semantics](../languages/Python_Fundamentals.md#25-copy-semantics) |
| `is` vs `==`, interning, NaN | P18, P19, P20 | [Data Model](../languages/Python_Fundamentals.md#1-python-data-model--object-system), [CPython Internals](../languages/Python_Fundamentals.md#26-python-internals-cpython) |
| Operators and numerics | P21, P22, P23, P24, P25, P26 | [Built-in Types](../languages/Python_Fundamentals.md#2-built-in-data-types--structures) |
| Exceptions, `finally`, `else` | P28, P29, P30, P31 | [Error Handling](../languages/Python_Fundamentals.md#13-error-handling--exceptions) |
| Iterators, generators, comprehensions, walrus | P32, P33, P34, P35, P36 | [Comprehensions](../languages/Python_Fundamentals.md#6-comprehensions--generator-expressions), [Iterators & Generators](../languages/Python_Fundamentals.md#7-iterators--generators) |
| Scope (LEGB, `global`, `nonlocal`) | P3, P35, P37, P38 | [Functions In Depth](../languages/Python_Fundamentals.md#5-functions-in-depth) |
| Classes, MRO, mangling, descriptors, attribute lookup | P39-P46 | [Classes](../languages/Python_Fundamentals.md#8-classes--oop-fundamentals), [Inheritance & MRO](../languages/Python_Fundamentals.md#9-inheritance--mro), [Descriptors](../languages/Python_Fundamentals.md#12-descriptors--metaclasses) |
| asyncio, GIL, threads | P47, P48, P49 | [GIL & Threading](../languages/Python_Fundamentals.md#19-the-gil--threading), [Asyncio](../languages/Python_Fundamentals.md#21-asyncio--asyncawait) |

See also: [Concurrency Coding Problems](../computer-science/Concurrency_Coding_Problems.md) for lock-based fixes to P49-style races, and [C++ Output Quiz](Cpp_Output_Quiz.md) for the C++ version of P24 (C++ division truncates toward zero).

---

## Answers

Each answer gives the exact output on CPython 3.14.4, then the rule, then common follow-up questions. Lines written to stderr (warnings) are marked as such.

### A1. Mutable default argument

```text
[1, 2] [1, 2] True
[3]
([1, 2],)
```

Default values are evaluated **once, when the `def` statement runs**, and stored on the function object in `append_to.__defaults__`. Each call that omits `bucket` gets the *same* list object, so `a` and `b` are one list. Passing an explicit `[]` bypasses the shared default.

Fix: use a `None` sentinel.

```python
def append_to(x, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(x)
    return bucket


print(append_to(1), append_to(2))  # [1] [2]
```

**Follow-ups:** *When is a shared mutable default intentional?* It is sometimes used as a poor man's memo cache (`def fib(n, _cache={})`). Prefer `functools.cache`. *How do linters catch this?* flake8-bugbear B006 and Ruff B006 flag mutable defaults.

### A2. Lambdas in a comprehension

```text
[2, 2, 2]
[0, 1, 2]
[20, 40]
```

A closure captures the **variable**, not its value at creation time. All three lambdas refer to the one `i` of the comprehension, and they look it up only when called. By then the loop has finished and `i == 2`. A default argument (`i=i`) is evaluated when each lambda is *created*, which freezes the current value. The third line is the same trick with an extra parameter: `2 * 10` and `2 * 20`.

**Follow-ups:** Other fixes are `functools.partial(fn, i)` or a factory function `def make(i): return lambda: i`. CPython 3.12 inlined list comprehensions (PEP 709), but the closure semantics are unchanged. The lambdas still share one cell.

### A3. Closures created in a for loop

```text
['C', 'C', 'C']
['Z', 'Z', 'Z']
None
```

At module level, `name` is a **global** variable, and a `for` loop does not create a new scope. Every `cb` looks up the global `name` when called. After the loop, `name` is `"c"`. After the reassignment, it is `"z"`. `__closure__` is `None`, which proves there is no closure at all, only global lookups. Inside a function, `cb` would capture a cell for `name`, and the result would be the same late binding.

### A4. `+=` versus `+` on a shared list

```text
[1, 2, 3] [1, 2, 3]
[1, 2, 3, 4] [1, 2, 3]
abc ab
```

For a list, `a += [3]` calls `list.__iadd__`, which **extends in place** and returns the same object. `b` is an alias, so it sees the change. `a = a + [4]` builds a **new** list and rebinds only `a`. `str` is immutable and has no `__iadd__`, so `s += "c"` falls back to `s = s + "c"`, and `t` keeps the old string.

**Pitfall:** `def f(lst): lst += [1]` mutates the caller's list, but `lst = lst + [1]` does not. The same split applies to NumPy arrays (`arr += 1` is in place).

### A5. Grid built with list multiplication

```text
[[1, 0, 0], [1, 0, 0], [1, 0, 0]]
1
[[1, 0, 0], [0, 0, 0], [0, 0, 0]]
```

`seq * n` repeats **references**. It does not copy the elements. `[[0] * 3] * 3` is a list holding the *same* inner list three times, which is why the set of `id`s has one element. The inner `[0] * 3` is fine because ints are immutable. Rebinding `row[i] = 1` replaces a reference and never mutates a shared int. Build 2-D structures with a comprehension, which creates a new inner list on each iteration, or use `numpy.zeros((3, 3))`.

### A6. Augmented assignment on a list inside a tuple

```text
TypeError: 'tuple' object does not support item assignment
(1, [2, 3, 4])
(1, [2, 3, 4, 5])
```

It **both raises and mutates**. `t[1] += [4]` compiles to three steps: load `t[1]`, call `list.__iadd__` (which extends the list in place and returns it), then store the result back with `t[1] = result`. The third step fails because tuples do not support item assignment. By then the list has already been extended. The CPython 3.14 bytecode shows the order:

```text
BINARY_OP     26 ([])   # load t[1]
BINARY_OP     13 (+=)   # list.__iadd__ -> mutation happens here
STORE_SUBSCR            # t[1] = ... -> TypeError
```

Calling the method directly (`t[1].extend(...)` or `t[1].append(...)`) avoids the store, so it succeeds silently. This case is in the official Python FAQ ("Why does a_tuple[i] += ['item'] raise an exception when the addition works?").

### A7. Removing from a list while iterating over it

```text
[1, 2, 3]
[1, 3]
```

A list iterator is just an index that increments. Removing an element shifts later elements left, so **the element right after a removed one is skipped**:

| Step | Index | List before | Element seen | Action |
|------|-------|-------------|--------------|--------|
| 1 | 0 | `[1, 2, 2, 3, 4]` | 1 | keep |
| 2 | 1 | `[1, 2, 2, 3, 4]` | 2 | remove, giving `[1, 2, 3, 4]` |
| 3 | 2 | `[1, 2, 3, 4]` | 3 | the second `2` (now at index 1) was skipped |
| 4 | 3 | `[1, 2, 3, 4]` | 4 | remove, giving `[1, 2, 3]` |
| 5 | 4 | `[1, 2, 3]` | -- | stop |

Unlike dicts and sets, lists raise **no error**, so the bug is silent. Fixes: build a new list with a comprehension (shown), iterate over a copy (`for n in nums[:]`), or iterate backwards by index.

### A8. In-place methods return None

```text
None [1, 2, 3]
None
['a', 'b', 'c'] bac
```

`list.sort()`, `append`, `extend`, `reverse`, `dict.update`, and `random.shuffle` mutate in place and return `None`. This is deliberate: the `None` return signals that no new object was created. `data = data.append(4)` therefore replaces the list with `None`, a common bug that later surfaces as `AttributeError: 'NoneType' object has no attribute ...`. `sorted()` takes any iterable and returns a new **list**, so sorting a string gives a list of characters. `reversed()` returns an iterator, which `"".join` consumes.

### A9. Commas make tuples

```text
int tuple (1,)
(1, False)
tuple 1
```

Parentheses only group. The **comma** makes a tuple, so `(1)` is just `1` and `1,` is a 1-tuple. In `x = 1, 2 == (1, 2)`, the `==` binds tighter than the comma, so the right side is the tuple `(1, (2 == (1, 2)))`, which is `(1, False)`. The empty tuple `()` is the one tuple that needs no comma. `((),)` is a 1-tuple that contains it.

### A10. Mutating a dict while iterating over it

```text
RuntimeError: dictionary changed size during iteration
{'a': 1, 'c': 3}
{'a': 10, 'c': 30}
{'a': 10}
```

The dict iterator records the dict's size and checks it on every `next()`. The `del` itself succeeds. The **next** iteration step notices the size change and raises, so `'b'` is already gone when the error appears. Assigning to **existing** keys is allowed because the size does not change. Iterating over a snapshot (`list(d)`) is the standard fix, or you can build a new dict with a comprehension.

**Follow-ups:** A pop followed by an insert keeps the size the same. CPython 3.8+ often still catches this (`RuntimeError: dictionary keys changed during iteration`), but only when the iterator would yield more keys than the dict had at the start. For example, popping a key you have not reached yet and then inserting a new one finishes silently, and the popped key is simply never seen. Never rely on the check. Sets raise `Set changed size during iteration`. Lists raise nothing (see P7).

### A11. Dict insertion order

```text
['b', 'a', 'c']
{'b': 10, 'c': 3, 'a': 0}
True
False
True
```

Since Python 3.7, the **language** guarantees that dicts preserve insertion order. In 3.6 this was a CPython implementation detail. Updating an existing key keeps its position. Deleting a key and re-inserting it moves the key to the end. `dict == dict` **ignores order**. `OrderedDict == OrderedDict` is **order-sensitive**. `OrderedDict == dict` ignores order.

**Follow-up:** *Why does `OrderedDict` still exist?* It provides `move_to_end()`, `popitem(last=False)`, and order-sensitive equality, which makes it the textbook building block for an LRU cache (see [High-Level Design](../computer-science/High_Level_Design.md)).

### A12. defaultdict creates keys when you read them

```text
False
True {'k': []}
None 1
{'b': 1, 'a': 3, 'n': 2}
```

`dict.__getitem__` calls `__missing__` when a key is absent and the subclass defines that method. `defaultdict` defines `__missing__` to insert `default_factory()`, and only `d[key]` (`__getitem__`) triggers it. A bare `dd["k"]` expression therefore **inserts** `"k"` with value `list()`. `in` and `.get()` never call `__missing__`, so they do not create keys. Key order follows first insertion: `b`, `a`, `n`.

**Pitfall:** reading a `defaultdict` on a read-only path (for example, in a cache lookup or while iterating it) silently grows it, and can trigger the "changed size during iteration" error from P10.

### A13. Set ordering

```text
{1, 2, 3}
{8, 1}
{18, 10, 2}
['apple', 'fig', 'pear']
{'fig', 'apple', 'pear'}      <- varies from run to run
```

A set iterates in **hash-table slot order**, which is neither insertion order nor sorted order. In CPython, small ints hash to themselves, and the slot is `hash & (table_size - 1)`. That is why `{3, 1, 2}` *looks* sorted while `{8, 1}` does not: 8 lands in slot 0 of an 8-slot table. Collisions (10, 2, and 18 all map to slot 2) are resolved by probing, and the probing details are an implementation detail. CPython 3.12 prints `{2, 18, 10}` for the third line, but 3.14 prints `{18, 10, 2}`.

String and bytes hashes are **randomized per process** (on by default since Python 3.3, using SipHash since 3.4, to defeat hash-flooding denial-of-service attacks). The last line can therefore change between runs. Only `sorted(...)` is deterministic. Never write tests that depend on the order of a set's `repr`.

### A14. Star-unpacking

```text
0 [1, 2, 3] 4
[] x
1 []
1-2-a-b
{'a': 9, 'b': 2}
ValueError: not enough values to unpack (expected at least 2, got 1)
```

A starred target always collects into a **list**, even when the source is a tuple or a string, and the list may be empty. `print(*[1, 2], *"ab", sep="-")` spreads all four items as separate arguments. In dict unpacking, **later keys win**, but a key keeps the position where it first appeared. With `p, *q, r`, the two mandatory targets need at least two values.

### A15. Shallow copy versus deep copy

```text
{'nums': [1, 2, 3], 'tag': 't'}
{'nums': [1, 2, 3], 'tag': 's'}
{'nums': [1, 2, 99], 'tag': 't'}
[[7, 0], [7, 0]]
```

`copy.copy` creates a **new outer dict that holds the same value objects**. Appending through `shallow["nums"]` mutates the list that `orig` also holds. Rebinding `shallow["tag"]` only changes the copy. `deepcopy` recursively copies everything.

The last line is the subtle part. `deepcopy` uses a **memo dict** keyed by `id()`, which **preserves aliasing inside the copied structure**. In `rows`, both rows are one list, so the clone also has both rows as one (new) list. That is correct, because deepcopy reproduces the object graph, but it surprises people who expect it to fix P5. See [Copy Semantics](../languages/Python_Fundamentals.md#25-copy-semantics).

### A16. Sort stability and reverse

```text
['bob', 'carol', 'alice', 'dave']
['alice', 'dave', 'bob', 'carol']
['dave', 'alice', 'carol', 'bob']
['alice', 'dave', 'bob', 'carol']
```

Python's sort (Timsort, and Powersort-based merging since 3.11) is **stable**: elements with equal keys keep their original relative order. `reverse=True` **also preserves stability**. It sorts as if each comparison were reversed, so `alice` stays before `dave` and `bob` stays before `carol`. `reversed(sorted(...))` is different: it flips the equal elements too.

Stability is what makes **multi-key sorting by repeated passes** work. Sort by the least significant key first, then by the most significant. The two-pass result equals `sorted(people, key=lambda p: (-p[1], p[0]))`.

### A17. String multiplication

```text
ababab
True True
[1, 2, 1, 2]
--->
55 10 55
TypeError: can't multiply sequence by non-int of type 'str'
```

`sequence * n` repeats the sequence. When `n <= 0`, the result is an empty sequence, not an error. `*` binds tighter than `+`, so `3 * "-" + ">"` is `"---" + ">"`. Multiplying two strings is a `TypeError`. For lists, repetition copies references (see P5).


### A18. `is` with small integers [CPython-specific]

```text
True
False True
True False
```

CPython pre-allocates the integers **-5 through 256** and always returns those cached objects, so any two 256s are the same object. `int("257")` builds a new object on each call, so the two 257s are equal but not identical. The range -5..256 is a CPython implementation detail. PyPy, for example, behaves differently. The language guarantees nothing about `is` for ints.

**Why the puzzle uses `int("257")`:** writing `a = 257; b = 257` in one file usually prints `True`, because the compiler stores equal constants once per code object. The same lines typed one by one into the REPL print `False`, because each line is compiled separately. Comparing with a literal (`x is 257`) has emitted a `SyntaxWarning` since 3.8. In 3.14, the message is `"is" with 'int' literal. Did you mean "=="?`. **Rule:** use `is` only for singletons (`None`, `True`, `False`, `Ellipsis`, or sentinel objects you create yourself), and `==` for everything else.

### A19. `is` with strings [CPython-specific]

```text
True
False True
True
False True
```

CPython **interns** string constants that look like identifiers (letters, digits, and underscores) at compile time, so both `"hello"` literals are one object. A string built at runtime by `join`, concatenation of variables, or `input()` is a new object. `sys.intern(c)` returns the canonical interned object, which is `a`. `"hello world!"` contains a space and `!`, so it is not interned. Two **separately compiled** units therefore create two distinct objects. Inside one module, the two literals would still be one object because of constant deduplication, which is why the puzzle uses two `compile()` calls.

**Practical use of `sys.intern`:** it deduplicates millions of repeated keys (for example, column names parsed from a log), saving memory and making dict lookups faster, since equal interned strings compare by pointer first.

### A20. NaN in containers

```text
False True
True True
False
1 2
```

IEEE 754 says that NaN compares **unequal to everything, including itself**. Container operations (`in`, `list.__eq__`, `list.index`, `list.count`, and set and dict lookups), however, check **identity first** and only then call `==` (the `x is y or x == y` shortcut). The *same* NaN object is therefore "found". Two *different* NaN objects are not equal, so `[float("nan")] == [float("nan")]` is `False` and a set can hold both.

**Follow-up:** *How do you test for NaN?* Use `math.isnan(x)`, or `x != x`. In pandas, `NaN` marks missing data, and `df == np.nan` is always `False`. Use `isna()` instead.

### A21. Chained comparisons

```text
True
True
True
True False
True
True
```

`a op1 b op2 c` means `(a op1 b) and (b op2 c)`, with `b` evaluated only once. **`in`, `not in`, `is`, and `is not` are comparison operators and chain too**, so `False == False in [False]` means `(False == False) and (False in [False])`, which is `True`. Once you add explicit parentheses, there is no chain: `(1 < 2) < 3` is `True < 3`, which is `True`, and `1 < (2 < 3)` is `1 < True`, which is `1 < 1`, which is `False`. The last line is `1 < 5 and 5 < 10 and 10 != 5`.

### A22. `and` / `or` return operands

```text
default
None
4
[]
0
True False
5 30 30
```

`and` and `or` return **one of their operands**, not a bool. `x or y` returns `x` if `x` is truthy, otherwise `y`. `x and y` returns `x` if `x` is falsy, otherwise `y`. Evaluation short-circuits, so `undefined_name` is never evaluated and no `NameError` occurs. Precedence is `not` > `and` > `or`, so `None or 0 and 5` is `None or (0 and 5)`, which is `None or 0`, which is `0`.

**Bug pattern:** `seconds or 30` treats a legitimate `0` as "missing". Write `30 if seconds is None else seconds`.

### A23. Floating-point precision

```text
0.30000000000000004
False
True
0.9999999999999999 1.0 1.0
True
0.3 False
```

`0.1` has no exact binary representation. The stored double is `0.1000000000000000055511151231257827021181583404541015625`, so rounding errors accumulate. Compare floats with `math.isclose` (default `rel_tol=1e-9`), and pass `abs_tol` when comparing against values near zero.

- **Naive loop vs `sum`:** since **Python 3.12**, `sum()` of floats uses Neumaier compensated summation, so it returns `1.0`. Python 3.11 and earlier print `0.9999999999999999`, the same as the manual loop. `math.fsum` has always been correctly rounded.
- **`1e16 + 1 == 1e16`:** a double has a 53-bit significand, and 2^53 is about 9.007e15. Above that, adjacent doubles are 2 apart, so `1e16 + 1` lands exactly halfway between two doubles and rounds to even, which is `1e16`. This is why float32 accumulators lose small increments (see [Performance Engineering](../computer-science/Performance_Engineering.md)).
- **`Decimal(0.1)`** converts the binary double *exactly*, so it is not equal to `Decimal("0.1")`. Always construct a `Decimal` from a string.

### A24. Integer division and modulo with negative numbers

```text
3 -4 -4
1 2 -2
(-3, 2)
-3 -3.5
-1.0
-4.0
```

Python's `//` rounds **toward negative infinity (floor)**, and `%` takes the **sign of the divisor**. The invariant `a == (a // b) * b + a % b` always holds: `-7 == (-4) * 2 + 1` and `-7 == (-3) * 3 + 2`. C, C++, and Java **truncate toward zero**, giving `-7 / 2 == -3` and `-7 % 3 == -1`. `math.fmod` follows the C rule, and `int()` truncates. `//` on floats floors too, and the result is still a float.

**Practical consequence:** in Python, `i % n` is always in `[0, n)` for positive `n`, which is ideal for ring-buffer indices. In C++, you need `((i % n) + n) % n`.

### A25. `round()` and banker's rounding

```text
0 2 2 0 -2
2.67
7 int float
2 -2
```

`round()` uses **round-half-to-even** ("banker's rounding", the IEEE 754 default). Exact ties go to the even neighbour: 0.5 rounds to 0, 1.5 to 2, 2.5 to 2, -0.5 to 0, and -1.5 to -2. This avoids the upward bias that half-up rounding adds when summing many rounded values.

`round(2.675, 2) == 2.67` is **not** banker's rounding. The literal 2.675 is stored as `2.67499999999999982236431605997495353221893310546875`, which is below the tie, so it rounds down. `round(x)` returns an `int`, but `round(x, n)` returns a float. `int()` truncates toward zero.

**Follow-up:** for currency, use `Decimal("2.675").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)`, which gives `2.68`.

### A26. `bool` is a subclass of `int`

```text
2 10 2
True False
yes
{1: 'float'}
True
```

`True` and `False` are instances of `bool`, a subclass of `int`, with values 1 and 0. They work in arithmetic and as indexes. `1`, `True`, and `1.0` are equal and have equal hashes, so in a dict they are the **same key**. The dict **keeps the first key object** (`1`) and **the last value** (`'float'`).

**Pitfall:** `isinstance(x, int)` accepts `True`. A JSON or config validator that wants a real integer must exclude bools explicitly, or check `type(x) is int`.

### A27. `hash(-1)` [CPython-specific]

```text
-2 -2 True
0 1 0 1
2 minus one
```

In CPython's C API, a hash function returns `-1` to signal that an error occurred. A real hash value can therefore never be `-1`, so `hash(-1)` is mapped to `-2`. On 64-bit builds, an int's hash is `n mod (2**61 - 1)`, which `sys.hash_info.modulus` reports. That makes `2**61 - 1` hash to 0 and `2**61` hash to 1.

Hash collisions are **legal**. The only requirement is `a == b` implies `hash(a) == hash(b)`, not the converse. On a hash match, dict and set lookup still compare keys with `==`, so `d` holds both keys correctly.

### A28. `return` inside `finally`

stderr (CPython 3.14 only, emitted at compile time):

```text
P28.py:5: SyntaxWarning: 'return' in a 'finally' block
  return "finally"
P28.py:12: SyntaxWarning: 'return' in a 'finally' block
  return "swallowed"
```

stdout:

```text
finally swallowed 1
```

`finally` always runs on the way out of `try`. A `return` inside `finally` **replaces** the pending return value (`f`) and **discards an in-flight exception** (`g` silently swallows the `ZeroDivisionError`). In `h`, the return value `1` was already evaluated before `finally` ran. Rebinding `x` afterwards does not change it, though *mutating* a returned list would be visible to the caller.

Because these semantics hide bugs, **PEP 765 (Python 3.14)** emits a `SyntaxWarning` for `return`, `break`, or `continue` that exits a `finally` block. CPython 3.12 runs the same code silently. A `break` or `continue` in `finally` swallows exceptions in the same way.

### A29. `else` on loops and `try`

```text
for-else: no break
for-else: empty loop
n = 2
try-else
finally
```

A loop's `else` runs when the loop ends **without `break`**, which includes loops with zero iterations. Read it as "no break". The `while` loop broke, so its `else` was skipped. In `try`/`except`/`else`/`finally`, the `else` runs only if no exception was raised, and it runs before `finally`. Putting code in `else` instead of `try` keeps the `except` from catching exceptions it was not meant to catch.

The canonical use is a search loop:

```python
for item in [1, 3, 5]:
    if item % 2 == 0:
        print("found", item)
        break
else:
    print("no even item")
```

### A30. Exception chaining

```text
KeyError True
KeyError('key')
None True ZeroDivisionError
None ZeroDivisionError
```

| Form | `__cause__` | `__context__` | `__suppress_context__` | Traceback text |
|------|-------------|---------------|------------------------|----------------|
| `raise X from e` | `e` | `e` (set automatically) | `True` | "The above exception was the direct cause of the following exception" |
| `raise X from None` | `None` | still recorded | `True` | context hidden |
| `raise X` inside `except` | `None` | the handled exception | `False` | "During handling of the above exception, another exception occurred" |

`from None` hides the original error from the printed traceback, but `__context__` still holds it for debuggers. Use `from e` when translating a low-level error into a domain error. It keeps the root cause visible.

### A31. The `except ... as` name is deleted

```text
NameError: name 'e' is not defined
```

When an `except E as e:` block ends, Python runs `del e`. It does this even if `e` existed before the `try`, which is why the module-level `"outer"` is gone. The deletion breaks a reference cycle: the exception holds the traceback, the traceback holds the frame, and the frame holds `e`. Without the `del`, every local in the frame would stay alive until the cyclic garbage collector ran. To keep the exception, assign it to a different name inside the block (`saved = e`).

### A32. Generator exhaustion

```text
14
0
[]
True [3]
```

A generator is a **single-pass iterator**. The first `sum` consumes it (0 + 1 + 4 + 9 = 14). After that, it raises `StopIteration` immediately, so `sum` returns its start value `0` and `list` returns `[]`. No error is raised, which is why this bug is easy to miss. `in` on an iterator **consumes items up to and including the match**, so only `3` is left. In Python 3, `map`, `filter`, `zip`, `enumerate`, and file objects are single-pass iterators too. `dict.items()` is different: it returns a *view*, which can be iterated many times.

**Fix:** materialize the values once (`vals = list(gen)`), or use a function that returns a fresh generator for each pass.

### A33. Iterator versus iterable

```text
[(1, 2)]
[3, 2, 1] []
[0, 1, 2] [0, 1, 2]
True False
```

- **`zip(it, it)`** pulls alternately from the **same** iterator, so it pairs consecutive items: `(1, 2)`. Then `3` has no partner and is dropped silently. (`zip(..., strict=True)`, added in 3.10, would raise instead.) `zip(*[iter(s)] * n)` is the classic chunking idiom, and `itertools.batched(s, n)` (3.12+) is the readable replacement.
- **`Countdown`** is an *iterable* whose `__iter__` mutates `self.n`, so the second pass finds `n == 0`. A correct iterable keeps its iteration state in the iterator: `n = self.n` as a local variable inside `__iter__`.
- **`range`** is an iterable, so each `iter()` call gives a fresh iterator.
- By the iterator protocol, **`iter(iterator) is iterator`**, while `iter(list)` returns a new `list_iterator` each time.


### A34. When does a generator expression bind its names?

```text
[10, 20, 30]
[101, 102]
```

A generator expression evaluates its **outermost iterable immediately**, when the generator is created, and passes it in as an argument. **Everything else is evaluated lazily**, when the generator is consumed. `g` therefore iterates over the original `[1, 2, 3]` even after `x` is rebound. In `g2`, the outer `for a in y` captured `[1, 2]` at creation, but the inner `for b in y` looks up `y` only when it runs. By then `y` is `[100]`, which gives `1 + 100` and `2 + 100`. PEP 289 chose this design so that errors in the first iterable (such as a typo) surface right away.

### A35. Comprehension scope

```text
outer [0, 1, 2]
[0, 1, 2]
NameError: name 'n' is not defined
```

In Python 3, comprehension loop variables **do not leak** into the surrounding scope. (List comprehensions did leak in Python 2.) A **class body is not an enclosing scope** for nested functions, lambdas, or comprehensions, so `n` is invisible inside `[n * i for i in range(2)]`. The **outermost iterable** is evaluated in the class body itself (see A34), so `range(n)` works. PEP 709 (3.12) inlined comprehensions for speed but deliberately kept this behaviour.

Workaround: move the class variable into the outermost iterable, or compute the list outside the class.

```python
class Config:
    n = 3
    fixed = [k * i for k in (n,) for i in range(2)]


print(Config.fixed)  # [0, 3]
```

### A36. Walrus operator scope

```text
first big: 8
[10, 100]
[3, 11, 12, 21] 21
v is not defined
```

An assignment expression (`:=`, PEP 572) inside a comprehension or generator expression binds the name in the **containing** scope, not in the comprehension's scope. `big` is therefore visible after `any()`. `any()` short-circuits at the first true value, so `big` is `8`, not `9`. The ordinary loop variable `v` still does not leak. A list display evaluates left to right, so `y` is already 10 when `y ** 2` runs. The running total works because `total` is rebound in the enclosing (module) scope on each iteration.

**Restrictions:** you cannot use `:=` to rebind a comprehension's own iteration variable (SyntaxError), and you cannot use it inside a comprehension in a class body.

### A37. UnboundLocalError

```text
UnboundLocalError - cannot access local variable 'count' where it is not associated with a value
show() failed before printing anything
```

The compiler decides whether a name is local by scanning the **whole function body**. Any assignment to the name (`=`, `+=`, `for x in`, `import x`, `def x`, `except ... as x`) makes it local **everywhere in the function**, including lines *before* the assignment. `count += 1` reads the local `count` before it has a value. In `show()`, `print(x)` fails for the same reason. It does not fall back to the global `x`. The message shown is from 3.11 and later. Earlier versions said `local variable 'count' referenced before assignment`. `UnboundLocalError` is a subclass of `NameError`.

Fixes: declare `global count` (or `nonlocal`), or better, pass the value in and return the new value.

### A38. `global` versus `nonlocal`

```text
outer sees: changed by nonlocal
outer sees: changed by nonlocal
module sees: changed by global
```

`nonlocal x` rebinds `x` in the **nearest enclosing function scope**, which is `outer`'s local variable. `global x` rebinds the **module-level** `x` and skips every enclosing function, so `outer`'s local is unaffected by `inner_global`. Name lookup follows LEGB: Local, Enclosing, Global, Built-in. `nonlocal` requires an existing binding in an enclosing *function*. Writing `nonlocal x` when only a global `x` exists is a `SyntaxError`.

### A39. Class attributes versus instance attributes

```text
['roll', 'sit'] True
wolf canine canine
wolf mammal
True False
```

Attribute **reads** check the instance `__dict__` first, then the class (and its MRO). Attribute **assignment** always writes to the instance `__dict__`.

- `self.tricks.append(...)` *reads* `tricks`, finds the single class-level list, and mutates it. Both dogs share one list. Fix: create `self.tricks = []` in `__init__`.
- `a.kind = "wolf"` creates an instance attribute that **shadows** the class attribute for `a` only.
- Changing `Dog.kind` is visible through every instance that has no shadowing attribute (`b`).

### A40. `self.n += 1` on a class attribute

```text
2 1 0
```

`self.n += 1` means `self.n = self.n + 1`. The right side reads the class attribute (0). The assignment creates an **instance** attribute. After that, each instance counts independently, and `Counter.n` stays 0. To count across all instances, write `type(self).n += 1` or `Counter.n += 1`.

**Contrast with P39:** if the class attribute were a list, `self.items += [x]` would call `list.__iadd__` and mutate the shared class list. It would *also* create an instance attribute that points to that same list. Both behaviours are surprising.

### A41. Diamond inheritance and `super()`

```text
D
B
C
A
['D', 'B', 'C', 'A', 'object']
--
B
A
```

Python computes the MRO with **C3 linearization**: D, then B, then C, then A, then object. Each class appears before its bases, and the left-to-right order of bases is preserved. `super()` does **not** mean "my parent class". It means "the next class after this one in the MRO of `type(self)`". In `D().hello()`, `B`'s `super()` therefore goes to **C**, not to A, and `A` runs exactly once. When `self` is a plain `B`, the MRO is `B, A, object`, so `B`'s `super()` goes to A.

**Follow-up:** cooperative multiple inheritance requires *every* class in the chain to call `super()`, and constructors to accept and forward `**kwargs`. If any class in the chain skips `super()`, the classes after it in the MRO are skipped.

### A42. An MRO that cannot be built

```text
TypeError: Cannot create a consistent method resolution order (MRO) for bases A, B
['F', 'B', 'A', 'object']
```

C3 has two constraints here. `class E(A, B)` requires A to come before B (the order of the bases as listed). B is a subclass of A, so B must also come before A. The two constraints contradict each other, so class creation fails. `class F(B, A)` is consistent, though listing `A` is redundant. CPython 3.12 prints the same message wrapped across two lines.

### A43. Equality without hashing

```text
True
None
TypeError: cannot use 'Point' as a set element (unhashable type: 'Point')
False 2
```

When a class defines `__eq__` but not `__hash__`, Python sets **`__hash__ = None`**, so instances are unhashable. The default `object.__hash__` is based on identity. Keeping it would break the rule that `a == b` implies `hash(a) == hash(b)`: two equal points could land in different set buckets. The error message is new in 3.14. CPython 3.12 and 3.13 print `TypeError: unhashable type: 'Point'`. `Plain` uses the defaults: `==` falls back to identity and the hash is identity-based, so two separate instances are unequal and the set holds both.

Fix: define a `__hash__` that is consistent with `__eq__`, and keep the fields immutable. Or use `@dataclass(frozen=True)`, which generates both methods.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int


print(len({Point(1, 2), Point(1, 2)}))  # 1
```

Also, `__eq__` should `return NotImplemented` for foreign types. The puzzle's version raises `AttributeError` for `Point(1, 2) == 5`.

### A44. Name mangling

```text
base
['_Base__secret', '_Child__secret', '_hint']
base child
AttributeError
```

Inside a class body, an identifier that begins with **two underscores and does not end with two underscores** is rewritten at compile time to `_ClassName__name`. `Base.reveal` was compiled inside `Base`, so it reads `_Base__secret`. `Child.__init__` writes `_Child__secret`, so the two attributes coexist. `c.__secret` at module level is not mangled, so the lookup fails. The purpose is to **avoid accidental name clashes with subclasses**, not to provide privacy, since `c._Base__secret` is still reachable. A single underscore (`_hint`) is only a convention. Dunder names such as `__init__` are never mangled.

### A45. Descriptor precedence

```text
data descriptor
instance dict
__set__ called with 42
{'d': 'instance dict', 'n': 'instance dict'}
non-data descriptor
```

`object.__getattribute__` resolves `obj.attr` in this order:

| Priority | Source | Example |
|----------|--------|---------|
| 1 | **Data descriptor** on the type (defines `__set__` or `__delete__`) | `property`, `DataDesc`, `__slots__` members |
| 2 | Instance `__dict__` | `o.__dict__["n"]` |
| 3 | **Non-data descriptor** (only `__get__`) or a plain class attribute | functions (methods), `NonDataDesc`, `functools.cached_property` |
| 4 | `__getattr__`, if defined | -- |

Assignment goes through a data descriptor's `__set__`, so `o.d = 42` prints the message and leaves `__dict__` unchanged.

**Follow-ups:** `property` is a data descriptor **even without a setter**, because it always defines `__set__`, which raises `AttributeError`. You therefore cannot shadow a property through the instance. Functions are non-data descriptors, so assigning `obj.method = ...` shadows the method for that instance. `functools.cached_property` uses this: on first access it stores the computed value in the instance `__dict__`, and later lookups never reach the descriptor.

### A46. `__getattr__` versus `__getattribute__`

```text
1 fallback:missing
fallback:__len__
TypeError: object of type 'Lazy' has no len()
get real
1
```

- **`__getattr__`** is called **only when normal lookup fails**. `lazy.real` is found normally. `lazy.missing` and `getattr(lazy, "__len__")` fall through to it.
- **Built-ins look up special methods on the type**, not on the instance, and bypass both `__getattr__` and `__getattribute__`. `len(lazy)` therefore raises. This is why proxy and wrapper classes must define `__len__`, `__iter__`, `__eq__`, and similar methods explicitly.
- **`__getattribute__`** runs on **every** attribute access, so it must delegate to `super().__getattribute__`. Accessing `self.__dict__` inside it would recurse forever. `Spy.__init__` printed nothing because assignment uses `__setattr__`. `"get real"` prints before `1` because the argument is evaluated before `print` runs.

### A47. Forgetting `await`

stdout (on a terminal):

```text
coroutine
42
True False
done
```

stderr, printed when `r2` is garbage-collected at the end of `main()`, so on a terminal it appears between `True False` and `done`:

```text
.../asyncio/events.py:94: RuntimeWarning: coroutine 'fetch' was never awaited
  self._context.run(self._callback, *self._args)
RuntimeWarning: Enable tracemalloc to get the object allocation traceback
```

Calling an `async def` function **does not run its body**. It only creates a coroutine object. `r2 == 42` compares a coroutine object to an int, so it is `False`, and no exception is raised. This is the danger: forgetting `await` usually produces a wrong value, not a crash. The only signal is the `RuntimeWarning` when the never-awaited coroutine is destroyed. When stdout is piped, buffering can print the warning before the stdout lines.

**Catch it early:** run with `python -X dev` or `PYTHONASYNCIODEBUG=1`, enable `-W error::RuntimeWarning` in tests, or use type checkers (mypy flags an unused coroutine) and linters (Ruff RUF006 covers a related bug, an un-stored `asyncio.create_task`).

### A48. A blocking call inside a coroutine

```text
good-fast
good-slow
good took ~0.2s
bad-slow
bad-fast
bad took ~0.3s
```

asyncio is **cooperative multitasking on a single thread**. A coroutine yields control only at an `await` that actually suspends. `await asyncio.sleep` yields to the event loop, so the two `good` sleeps overlap and the total time is the maximum (0.2 s). `time.sleep` **blocks the whole event loop**, so `gather` runs the `bad` coroutines one after another in argument order, and the total is the sum (0.3 s). The same applies to `requests.get`, CPU-heavy loops, and blocking file or database I/O.

**Fixes:** use an async library (`aiohttp`, `asyncpg`), or offload the blocking call with `await asyncio.to_thread(blocking_fn)` (3.9+) or `loop.run_in_executor(...)`. In debug mode, asyncio logs any callback that runs longer than `loop.slow_callback_duration` (default 0.1 s).

### A49. `counter += 1` from four threads

```text
800000 True
```

This is what CPython 3.14 (default GIL build) prints in practice, but it is **not guaranteed**. `counter += 1` is four bytecodes (shown here with the loop's back-edge, which matters below):

```text
LOAD_GLOBAL      counter
LOAD_SMALL_INT   1
BINARY_OP        13 (+=)
STORE_GLOBAL     counter
JUMP_BACKWARD    (loop)
```

The GIL makes each **bytecode** atomic, not each Python **statement**. A thread switch between `LOAD_GLOBAL` and `STORE_GLOBAL` loses an update. Since CPython 3.10, the GIL build checks for a pending switch only at certain points, such as loop back-edges (`JUMP_BACKWARD`) and function entry. In this tight loop, the read-modify-write therefore happens never to be interrupted. On CPython 3.9 and earlier, the same program commonly printed less than 800000. It still loses updates today if any Python-level call sits between the read and the write. For example, if `counter` is a property:

```python
import sys
import threading

sys.setswitchinterval(1e-6)  # switch threads very often (default 0.005 s) to expose the race


class Box:
    def __init__(self):
        self._v = 0

    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, x):
        self._v = x


box = Box()


def work(n):
    for _ in range(n):
        box.v += 1  # getter call ... setter call: a switch can happen in between


threads = [threading.Thread(target=work, args=(200_000,)) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(box.v)  # varies: 346483, 338148, 366876 in three runs on 3.14.4
```

With the default 5 ms switch interval, the property version still loses updates in some runs (688692 and 799221 appeared in five runs). With the same 1 µs interval, plain `counter += 1` still printed 800000. On the **free-threaded build** (`python3.14t`, PEP 703), threads truly run in parallel, so plain `counter += 1` loses updates too.

**Correct fixes:** protect the update with a `threading.Lock` (`with lock: counter += 1`), or give each thread a local count and add the counts after `join()`. The second option has no contention and is faster. **Interview one-liner:** "The GIL protects the interpreter's internal state, not your invariants." See [Concurrency Coding Problems](../computer-science/Concurrency_Coding_Problems.md) and [GIL & Threading](../languages/Python_Fundamentals.md#19-the-gil--threading).
