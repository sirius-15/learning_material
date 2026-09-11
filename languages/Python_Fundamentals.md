# Python Fundamentals -- Comprehensive Reference

> A thorough, interview-focused reference covering every important Python topic from language basics to advanced internals. Each section includes key concepts, code examples, comparison tables, common pitfalls, and interview-relevant explanations. Complements the *DSA Fundamentals*, *LeetCode Patterns*, and *CS Fundamentals* guides.

---

## Table of Contents

### Part 1: Language Core

1. [Python Data Model & Object System](#1-python-data-model--object-system)
2. [Built-in Data Types & Structures](#2-built-in-data-types--structures)
3. [Strings & Text Processing](#3-strings--text-processing)
4. [Control Flow & Looping](#4-control-flow--looping)
5. [Functions In Depth](#5-functions-in-depth)
6. [Comprehensions & Generator Expressions](#6-comprehensions--generator-expressions)
7. [Iterators & Generators](#7-iterators--generators)

### Part 2: Object-Oriented Python

8. [Classes & OOP Fundamentals](#8-classes--oop-fundamentals)
9. [Inheritance & MRO](#9-inheritance--mro)
10. [Magic (Dunder) Methods](#10-magic-dunder-methods)
11. [Abstract Base Classes & Protocols](#11-abstract-base-classes--protocols)
12. [Descriptors & Metaclasses](#12-descriptors--metaclasses)

### Part 3: Intermediate & Advanced

13. [Error Handling & Exceptions](#13-error-handling--exceptions)
14. [Context Managers](#14-context-managers)
15. [Decorators](#15-decorators)
16. [Functional Programming](#16-functional-programming)
17. [Type Hints & Static Typing](#17-type-hints--static-typing)
18. [Modules, Packages & Import System](#18-modules-packages--import-system)

### Part 4: Concurrency & Performance

19. [The GIL & Threading](#19-the-gil--threading)
20. [Multiprocessing](#20-multiprocessing)
21. [Asyncio & Async/Await](#21-asyncio--asyncawait)
22. [concurrent.futures](#22-concurrentfutures)
23. [Performance & Optimization](#23-performance--optimization)

### Part 5: Memory, Internals & Best Practices

24. [Memory Management & Garbage Collection](#24-memory-management--garbage-collection)
25. [Copy Semantics](#25-copy-semantics)
26. [Python Internals (CPython)](#26-python-internals-cpython)
27. [Common Gotchas & Best Practices](#27-common-gotchas--best-practices)
28. [Testing](#28-testing)

### Part 6: Quick Reference

29. [Built-in Functions Cheat Sheet](#29-built-in-functions-cheat-sheet)
30. [Standard Library Highlights](#30-standard-library-highlights)

---

# Part 1: Language Core

---

## 1. Python Data Model & Object System

---

### 1.1 Everything Is an Object

In Python, **every value is an object** -- integers, strings, functions, classes, modules, even `None`. Every object has three fundamental properties:

| Property | Accessor | Description |
|---|---|---|
| **Identity** | `id(obj)` | Unique integer (memory address in CPython) that never changes during the object's lifetime |
| **Type** | `type(obj)` | The class of the object; determines what operations it supports |
| **Value** | The object itself | May or may not be changeable (mutable vs immutable) |

```python
x = 42
print(id(x))       # e.g. 140735278617424 (memory address in CPython)
print(type(x))     # <class 'int'>
print(x)           # 42

def greet():
    return "hello"

print(type(greet))  # <class 'function'> -- functions are objects too
print(id(greet))    # functions have identity like any other object
```

### 1.2 Identity vs Equality

| Operator | Tests | Meaning |
|---|---|---|
| `is` | Identity | Are these the **same object** in memory? (`id(a) == id(b)`) |
| `==` | Equality | Do these objects have the **same value**? (calls `__eq__`) |

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

a == b   # True  -- same value
a is b   # False -- different objects in memory
a is c   # True  -- c is an alias for the same object

# Common pitfall: use 'is' only for singletons
x = None
if x is None:      # correct -- None is a singleton
    pass
if x == None:      # works but discouraged
    pass
```

### 1.3 Mutability

| Mutable | Immutable |
|---|---|
| `list` | `int` |
| `dict` | `float` |
| `set` | `bool` |
| `bytearray` | `str` |
| User-defined classes (by default) | `tuple` |
| | `frozenset` |
| | `bytes` |
| | `None` |

**Why it matters:**

- Immutable objects can be used as dict keys and set elements (they are *hashable* by default).
- Mutable objects passed to functions can be modified in place (aliasing side effects).
- Immutable objects enable safe sharing between threads without locks.

```python
# Immutable -- "changing" creates a new object
s = "hello"
print(id(s))   # e.g. 140220948305648
s += " world"
print(id(s))   # different id -- new string object created

# Mutable -- modification happens in place
lst = [1, 2, 3]
print(id(lst))  # e.g. 140220947824576
lst.append(4)
print(id(lst))  # same id -- same object modified
```

### 1.4 Variable Binding Model

Python variables are **names** (labels/references) that point to objects, not boxes that contain values. Assignment binds a name to an object; it never copies data.

```
            ┌────────────┐
  x ──────▶ │  [1, 2, 3] │
             └────────────┘
  y ──────▶ same object (after y = x)
```

```python
x = [1, 2, 3]
y = x           # y is a reference to the SAME list
y.append(4)
print(x)        # [1, 2, 3, 4] -- x sees the change

# Reassignment breaks the link
y = [10, 20]    # y now points to a different object
print(x)        # [1, 2, 3, 4] -- x is unaffected
```

### 1.5 Interning and Caching

CPython caches certain immutable objects for performance:

| What is cached | Range / Rule |
|---|---|
| Small integers | -5 to 256 (pre-allocated at interpreter startup) |
| Strings | Single-character strings; identifier-like strings are interned automatically |
| `None`, `True`, `False` | Always singletons |

```python
a = 256
b = 256
a is b    # True -- cached small integer

a = 257
b = 257
a is b    # False (in general) -- outside cache range

a = "hello"
b = "hello"
a is b    # True -- identifier-like strings are interned

a = "hello world"
b = "hello world"
a is b    # False -- spaces prevent automatic interning
```

**Interview tip:** Never rely on interning for correctness. Always use `==` for value comparison and `is` only for singletons (`None`, `True`, `False`).

### 1.6 `None`

`None` is Python's null/nil value. It is a **singleton** -- there is exactly one `None` object.

```python
type(None)    # <class 'NoneType'>
bool(None)    # False -- None is falsy

def f():
    pass
print(f())    # None -- functions without return implicitly return None
```

### 1.7 Truthiness (Boolean Evaluation)

Any object can be evaluated in a boolean context. The rules:

| Evaluates to `False` (falsy) | Evaluates to `True` (truthy) |
|---|---|
| `None` | Everything else |
| `False` | |
| `0`, `0.0`, `0j`, `Decimal(0)`, `Fraction(0)` | |
| `""` (empty string) | |
| `[]`, `()`, `{}`, `set()`, `frozenset()` (empty containers) | |
| Objects with `__bool__()` returning `False` | |
| Objects with `__len__()` returning `0` | |

```python
# Pythonic -- use truthiness directly
if my_list:           # truthy if non-empty
    process(my_list)

# Unpythonic
if len(my_list) > 0:  # unnecessarily verbose
    process(my_list)
```

### 1.8 Type Checking

```python
isinstance(42, int)             # True -- preferred way to check types
isinstance(42, (int, float))    # True -- can check multiple types

type(42) == int                 # True -- exact type match only (ignores inheritance)
type(42) is int                 # True -- same, using identity

# isinstance respects inheritance
class Animal: pass
class Dog(Animal): pass

d = Dog()
isinstance(d, Animal)   # True
type(d) == Animal        # False -- type is Dog, not Animal
```

---

## 2. Built-in Data Types & Structures

---

### 2.1 Numeric Types

| Type | Description | Examples |
|---|---|---|
| `int` | Arbitrary-precision integers | `42`, `-7`, `0xFF`, `0b1010`, `0o17` |
| `float` | IEEE 754 double-precision (64-bit) | `3.14`, `1e-5`, `float('inf')`, `float('nan')` |
| `complex` | Complex numbers | `3+4j`, `complex(3, 4)` |
| `bool` | Subclass of `int`; `True` is `1`, `False` is `0` | `True`, `False` |

```python
# int is arbitrary precision
2 ** 1000       # works fine, produces a very large integer

# Float precision issues
0.1 + 0.2       # 0.30000000000000004
0.1 + 0.2 == 0.3  # False!

# Use decimal for exact arithmetic
from decimal import Decimal
Decimal('0.1') + Decimal('0.2') == Decimal('0.3')  # True

# Integer division vs true division
7 / 2    # 3.5  (true division -- always returns float)
7 // 2   # 3    (floor division -- truncates toward negative infinity)
-7 // 2  # -4   (not -3! floors toward negative infinity)
7 % 2    # 1    (modulo)

# Built-in numeric functions
abs(-5)         # 5
round(3.14159, 2)  # 3.14
divmod(7, 2)    # (3, 1) -- (quotient, remainder)
pow(2, 10)      # 1024
pow(2, 10, 1000)  # 24 -- modular exponentiation (2^10 % 1000)
```

### 2.2 Lists

A **list** is a mutable, ordered, dynamically-sized sequence implemented as a contiguous array of pointers to objects.

| Operation | Time Complexity | Notes |
|---|---|---|
| `lst[i]` | O(1) | Index access |
| `lst[i] = x` | O(1) | Index assignment |
| `lst.append(x)` | O(1) amortized | Add to end |
| `lst.pop()` | O(1) | Remove from end |
| `lst.pop(i)` | O(n) | Remove at index (shifts elements) |
| `lst.insert(i, x)` | O(n) | Insert at index (shifts elements) |
| `lst.remove(x)` | O(n) | Find and remove first occurrence |
| `x in lst` | O(n) | Linear search |
| `lst.sort()` | O(n log n) | Timsort (in-place, stable) |
| `lst.reverse()` | O(n) | In-place reversal |
| `len(lst)` | O(1) | Stored attribute |
| `lst.extend(iterable)` | O(k) | k = length of iterable |
| `lst + lst2` | O(n + m) | Creates new list |
| `lst[a:b]` | O(b - a) | Slice creates a new list (shallow copy) |

```python
# Creation
lst = [1, 2, 3]
lst = list(range(10))     # [0, 1, 2, ..., 9]
lst = [0] * 5             # [0, 0, 0, 0, 0]

# Slicing
lst = [0, 1, 2, 3, 4, 5]
lst[1:4]     # [1, 2, 3]       -- start inclusive, end exclusive
lst[:3]      # [0, 1, 2]       -- from beginning
lst[3:]      # [3, 4, 5]       -- to end
lst[-2:]     # [4, 5]          -- last two
lst[::2]     # [0, 2, 4]       -- every other element
lst[::-1]    # [5, 4, 3, 2, 1, 0]  -- reversed copy

# Useful methods
lst.index(3)          # 3 -- index of first occurrence (raises ValueError if absent)
lst.count(2)          # 1 -- number of occurrences
lst.copy()            # shallow copy (same as lst[:])
lst.clear()           # remove all items

# Sorting
nums = [3, 1, 4, 1, 5]
sorted(nums)          # [1, 1, 3, 4, 5] -- returns new list
nums.sort()           # sorts in-place, returns None
nums.sort(reverse=True)
nums.sort(key=lambda x: -x)  # custom sort key
```

### 2.3 Tuples

A **tuple** is an immutable, ordered sequence. Commonly used for fixed collections, function return values, and as dict keys.

```python
# Creation
t = (1, 2, 3)
t = 1, 2, 3         # parentheses are optional
t = (42,)            # single-element tuple NEEDS trailing comma
t = tuple([1, 2, 3]) # from iterable

# Operations (same as list, except mutation)
t[0]          # 1
t[1:3]        # (2, 3)
len(t)        # 3
3 in t        # True
t + (4, 5)    # (1, 2, 3, 4, 5) -- new tuple
t * 2         # (1, 2, 3, 1, 2, 3)  -- new tuple

# Tuple unpacking
a, b, c = (1, 2, 3)
first, *rest = [1, 2, 3, 4]    # first=1, rest=[2, 3, 4]
first, *mid, last = [1, 2, 3, 4]  # first=1, mid=[2, 3], last=4

# Named tuples for readability
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(3, 4)
print(p.x, p.y)    # 3 4
print(p[0])         # 3 -- also supports indexing
```

### List vs Tuple

| Aspect | List | Tuple |
|---|---|---|
| Mutability | Mutable | Immutable |
| Syntax | `[1, 2, 3]` | `(1, 2, 3)` |
| Hashable | No | Yes (if all elements are hashable) |
| Use as dict key | No | Yes |
| Performance | Slightly slower (overhead of mutation support) | Slightly faster, less memory |
| Semantic meaning | Homogeneous collection (variable-length) | Heterogeneous record (fixed-length) |

### 2.4 Dictionaries

A **dict** is a mutable, unordered (insertion-ordered since Python 3.7+) mapping of hashable keys to arbitrary values. Implemented as a hash table.

| Operation | Average | Worst | Notes |
|---|---|---|---|
| `d[key]` | O(1) | O(n) | Lookup; raises `KeyError` if missing |
| `d.get(key, default)` | O(1) | O(n) | Safe lookup with default |
| `d[key] = val` | O(1) | O(n) | Insert / update |
| `del d[key]` | O(1) | O(n) | Delete; raises `KeyError` if missing |
| `key in d` | O(1) | O(n) | Membership test |
| `len(d)` | O(1) | O(1) | Stored attribute |
| `d.keys()` / `d.values()` / `d.items()` | O(1) | O(1) | Returns a *view* (iteration is O(n)) |
| `d.pop(key)` | O(1) | O(n) | Remove and return |
| `d.update(other)` | O(k) | O(k*n) | Merge k items from other |

Worst case O(n) occurs with hash collisions (extremely rare with good hash functions).

```python
# Creation
d = {'a': 1, 'b': 2}
d = dict(a=1, b=2)
d = dict([('a', 1), ('b', 2)])
d = {x: x**2 for x in range(5)}   # {0:0, 1:1, 2:4, 3:9, 4:16}

# Access
d['a']              # 1
d.get('z', 0)       # 0 (default if key missing)

# Iteration
for key in d:                       # iterate over keys
    print(key, d[key])
for key, val in d.items():          # iterate over key-value pairs
    print(key, val)

# Useful methods
d.setdefault('c', 3)   # returns d['c'] if exists; else sets d['c']=3 and returns 3
d.pop('a')              # removes 'a' and returns its value
d.popitem()             # removes and returns last inserted (key, value)
d1 = {**d, 'x': 10}    # merge/unpack into new dict
d1 = d | {'x': 10}     # merge operator (Python 3.9+)
d |= {'x': 10}         # in-place merge (Python 3.9+)
```

### 2.5 Sets

A **set** is a mutable, unordered collection of unique hashable elements. Implemented as a hash table (like a dict with keys only).

| Operation | Average | Notes |
|---|---|---|
| `x in s` | O(1) | Membership test |
| `s.add(x)` | O(1) | Add element |
| `s.remove(x)` | O(1) | Remove element (raises `KeyError` if missing) |
| `s.discard(x)` | O(1) | Remove element (no error if missing) |
| `s \| t` (union) | O(n + m) | New set with elements from both |
| `s & t` (intersection) | O(min(n, m)) | New set with elements in both |
| `s - t` (difference) | O(n) | New set with elements in s but not t |
| `s ^ t` (symmetric difference) | O(n + m) | New set with elements in exactly one |
| `s <= t` (subset) | O(n) | Is s a subset of t? |
| `s >= t` (superset) | O(m) | Is s a superset of t? |

```python
# Creation
s = {1, 2, 3}
s = set([1, 2, 2, 3])      # {1, 2, 3} -- duplicates removed
s = set()                    # empty set (NOT {} which is an empty dict)

# frozenset -- immutable, hashable set
fs = frozenset([1, 2, 3])
d = {fs: "value"}           # can be used as dict key

# Set operations
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
a | b    # {1, 2, 3, 4, 5, 6}   union
a & b    # {3, 4}                intersection
a - b    # {1, 2}                difference
a ^ b    # {1, 2, 5, 6}          symmetric difference
a <= b   # False                  subset
{3, 4} <= a  # True

# Common use: removing duplicates while preserving order
def dedupe_ordered(lst):
    seen = set()
    result = []
    for x in lst:
        if x not in seen:
            seen.add(x)
            result.append(x)
    return result
```

### 2.6 The `collections` Module

| Class | Description |
|---|---|
| `defaultdict` | Dict with a factory for missing keys |
| `Counter` | Dict subclass for counting hashable objects |
| `OrderedDict` | Dict that remembers insertion order (mostly superseded by regular dict in 3.7+) |
| `deque` | Double-ended queue with O(1) append/pop on both ends |
| `namedtuple` | Tuple subclass with named fields |
| `ChainMap` | Groups multiple dicts into a single mapping |

```python
from collections import defaultdict, Counter, deque, namedtuple, ChainMap

# defaultdict -- no KeyError for missing keys
word_count = defaultdict(int)
for word in "the cat sat on the mat".split():
    word_count[word] += 1
# {'the': 2, 'cat': 1, 'sat': 1, 'on': 1, 'mat': 1}

graph = defaultdict(list)
graph['a'].append('b')   # no need to check if 'a' exists

# Counter
c = Counter("abracadabra")
# Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})
c.most_common(2)        # [('a', 5), ('b', 2)]
c['a']                  # 5
c + Counter("aab")      # combine counts
c - Counter("aab")      # subtract counts (drops zero/negative)

# deque -- O(1) operations on both ends
dq = deque([1, 2, 3])
dq.appendleft(0)        # deque([0, 1, 2, 3])
dq.popleft()            # 0
dq.append(4)            # deque([1, 2, 3, 4])
dq.rotate(1)            # deque([4, 1, 2, 3])
dq.rotate(-1)           # deque([1, 2, 3, 4])
# Fixed-size deque (sliding window)
dq = deque(maxlen=3)
dq.extend([1, 2, 3, 4, 5])  # deque([3, 4, 5]) -- oldest dropped

# namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(3, 4)
p.x, p.y               # 3, 4
p._asdict()             # {'x': 3, 'y': 4}
p._replace(x=10)        # Point(x=10, y=4) -- returns new tuple

# ChainMap -- layered lookup
defaults = {'color': 'red', 'size': 10}
user_prefs = {'color': 'blue'}
config = ChainMap(user_prefs, defaults)
config['color']   # 'blue'  (found in user_prefs first)
config['size']    # 10      (falls through to defaults)
```

### 2.7 `heapq` and `bisect`

```python
import heapq

# heapq -- min-heap operations on a regular list
heap = []
heapq.heappush(heap, 5)
heapq.heappush(heap, 1)
heapq.heappush(heap, 3)
heapq.heappop(heap)          # 1 (smallest)
heapq.heappushpop(heap, 2)   # push 2, then pop smallest → 2
heapq.nlargest(2, [5, 1, 8, 3])   # [8, 5]
heapq.nsmallest(2, [5, 1, 8, 3])  # [1, 3]

# Max-heap trick: negate values
max_heap = []
heapq.heappush(max_heap, -5)
heapq.heappush(max_heap, -1)
-heapq.heappop(max_heap)     # 5 (largest)

import bisect

# bisect -- binary search on sorted lists
sorted_list = [1, 3, 5, 7, 9]
bisect.bisect_left(sorted_list, 5)    # 2 (insertion point, left of existing 5)
bisect.bisect_right(sorted_list, 5)   # 3 (insertion point, right of existing 5)
bisect.insort(sorted_list, 4)         # [1, 3, 4, 5, 7, 9] -- insert maintaining order
```

---

## 3. Strings & Text Processing

---

### 3.1 String Fundamentals

Strings are **immutable** sequences of Unicode code points. Any operation that appears to modify a string actually creates a new one.

```python
s = "Hello, World!"
s[0]          # 'H'
s[-1]         # '!'
s[0:5]        # 'Hello'
len(s)        # 13
'World' in s  # True

# Strings are immutable
s[0] = 'h'   # TypeError: 'str' object does not support item assignment
s = 'h' + s[1:]  # creates new string "hello, World!"
```

### 3.2 String Methods Quick Reference

| Category | Methods |
|---|---|
| **Case** | `upper()`, `lower()`, `title()`, `capitalize()`, `swapcase()`, `casefold()` |
| **Search** | `find(sub)`, `rfind(sub)`, `index(sub)`, `rindex(sub)`, `count(sub)` |
| **Test** | `startswith(p)`, `endswith(s)`, `isalpha()`, `isdigit()`, `isalnum()`, `isspace()`, `isupper()`, `islower()` |
| **Transform** | `strip()`, `lstrip()`, `rstrip()`, `replace(old, new)`, `translate()` |
| **Split/Join** | `split(sep)`, `rsplit(sep)`, `splitlines()`, `join(iterable)`, `partition(sep)` |
| **Align** | `center(w)`, `ljust(w)`, `rjust(w)`, `zfill(w)` |
| **Encode** | `encode(encoding)` |

```python
# split and join
"a,b,c".split(",")         # ['a', 'b', 'c']
",".join(['a', 'b', 'c'])  # 'a,b,c'

# strip
"  hello  ".strip()        # 'hello'
"xxxhelloxxx".strip('x')   # 'hello'

# find vs index
"hello".find("ll")         # 2  (returns -1 if not found)
"hello".index("ll")        # 2  (raises ValueError if not found)

# replace
"hello world".replace("world", "Python")  # 'hello Python'

# partition
"user@example.com".partition("@")   # ('user', '@', 'example.com')
```

### 3.3 String Formatting

Python offers three formatting approaches:

```python
name = "Alice"
age = 30
gpa = 3.856

# f-strings (Python 3.6+) -- preferred
f"Name: {name}, Age: {age}"
f"GPA: {gpa:.2f}"          # 'GPA: 3.86'
f"{'centered':^20}"        # '      centered      '
f"{1_000_000:,}"           # '1,000,000'
f"{255:#x}"                # '0xff'
f"{name!r}"                # "'Alice'" (calls repr)
f"{2 + 3 = }"              # '2 + 3 = 5' (Python 3.8+ debug format)

# .format() method
"Name: {}, Age: {}".format(name, age)
"Name: {name}, Age: {age}".format(name=name, age=age)
"{0:.2f}".format(gpa)

# %-formatting (old style, C-like)
"Name: %s, Age: %d" % (name, age)
"GPA: %.2f" % gpa
```

| Format Spec | Meaning | Example | Output |
|---|---|---|---|
| `:.2f` | 2 decimal places | `f"{3.14159:.2f}"` | `'3.14'` |
| `:,` | Thousands separator | `f"{1000000:,}"` | `'1,000,000'` |
| `:>10` | Right-align, width 10 | `f"{'hi':>10}"` | `'        hi'` |
| `:<10` | Left-align, width 10 | `f"{'hi':<10}"` | `'hi        '` |
| `:^10` | Center, width 10 | `f"{'hi':^10}"` | `'    hi    '` |
| `:010d` | Zero-padded integer | `f"{42:010d}"` | `'0000000042'` |
| `:b` | Binary | `f"{10:b}"` | `'1010'` |
| `:#x` | Hex with prefix | `f"{255:#x}"` | `'0xff'` |

### 3.4 Encoding and Decoding

```python
# str (Unicode text) <--> bytes (raw data)
text = "café"
encoded = text.encode('utf-8')     # b'caf\xc3\xa9'
decoded = encoded.decode('utf-8')  # 'café'

# Byte literals
b = b"hello"          # bytes literal (ASCII only)
type(b)               # <class 'bytes'>
b[0]                  # 104 (integer, not 'h')

# Common encodings
text.encode('ascii')           # UnicodeEncodeError (é not in ASCII)
text.encode('ascii', 'ignore') # b'caf' (drops non-ASCII)
text.encode('ascii', 'replace')# b'caf?' (replaces with ?)
```

### 3.5 Regular Expressions (`re` Module)

```python
import re

# Basic matching
re.search(r'\d+', 'Order 42 shipped')     # <Match '42'>
re.match(r'\d+', 'Order 42')              # None (match checks start only)
re.match(r'\d+', '42 orders')             # <Match '42'>
re.findall(r'\d+', 'a1 b2 c3')            # ['1', '2', '3']
re.sub(r'\d+', 'X', 'a1 b2')             # 'aX bX'

# Groups
m = re.search(r'(\w+)@(\w+\.\w+)', 'user@example.com')
m.group(0)    # 'user@example.com'  (entire match)
m.group(1)    # 'user'
m.group(2)    # 'example.com'

# Named groups
m = re.search(r'(?P<user>\w+)@(?P<domain>\w+\.\w+)', 'user@example.com')
m.group('user')    # 'user'

# Compile for reuse
pattern = re.compile(r'\d{3}-\d{4}')
pattern.findall('Call 555-1234 or 555-5678')  # ['555-1234', '555-5678']
```

| Pattern | Meaning |
|---|---|
| `.` | Any character except newline |
| `\d`, `\D` | Digit / non-digit |
| `\w`, `\W` | Word character `[a-zA-Z0-9_]` / non-word |
| `\s`, `\S` | Whitespace / non-whitespace |
| `^`, `$` | Start / end of string |
| `*`, `+`, `?` | 0+, 1+, 0 or 1 |
| `{n,m}` | Between n and m repetitions |
| `[]` | Character class |
| `()` | Capturing group |
| `(?:...)` | Non-capturing group |
| `\|` | Alternation (or) |
| `(?P<name>...)` | Named group |

### 3.6 Raw Strings

```python
# Regular string -- backslash is an escape character
path = "C:\\Users\\name"     # need double backslash
regex = "\\d+\\.\\d+"       # hard to read

# Raw string -- backslash is literal
path = r"C:\Users\name"     # much cleaner
regex = r"\d+\.\d+"         # standard for regex patterns

# Note: raw strings cannot end with an odd number of backslashes
# r"C:\Users\" is a SyntaxError
```

---

## 4. Control Flow & Looping

---

### 4.1 Conditional Statements

```python
if condition:
    pass
elif other_condition:
    pass
else:
    pass

# Ternary (conditional expression)
result = "even" if x % 2 == 0 else "odd"

# Chained comparisons
if 0 < x < 10:        # equivalent to: 0 < x and x < 10
    pass
if a == b == c:        # all three equal
    pass
```

### 4.2 `for` and `while` Loops

```python
# for loop -- iterates over any iterable
for item in iterable:
    process(item)

# Useful built-ins for looping
for i, val in enumerate(lst):           # index + value
    print(i, val)

for a, b in zip(list1, list2):          # parallel iteration
    print(a, b)

for a, b in zip(list1, list2, strict=True):  # Python 3.10+, raises if lengths differ

for key, val in sorted(d.items()):      # sorted dict iteration

for i in range(start, stop, step):      # numeric range

for item in reversed(lst):              # reverse iteration
```

### 4.3 `else` on Loops

The `else` clause on `for`/`while` executes when the loop completes **without** hitting `break`. Think of it as "no break."

```python
# Practical use: searching
for item in collection:
    if matches(item):
        result = item
        break
else:
    # executed only if loop completed without break
    result = None
    print("Not found")

# Equivalent to:
found = False
for item in collection:
    if matches(item):
        result = item
        found = True
        break
if not found:
    result = None
```

### 4.4 Structural Pattern Matching (`match`/`case`, Python 3.10+)

```python
def http_status(status):
    match status:
        case 200:
            return "OK"
        case 301 | 302:
            return "Redirect"
        case 404:
            return "Not Found"
        case int(x) if x >= 500:
            return f"Server Error ({x})"
        case _:
            return "Unknown"

# Destructuring patterns
match point:
    case (0, 0):
        print("Origin")
    case (x, 0):
        print(f"On x-axis at {x}")
    case (0, y):
        print(f"On y-axis at {y}")
    case (x, y):
        print(f"Point at ({x}, {y})")

# Class patterns
match event:
    case Click(position=(x, y)):
        handle_click(x, y)
    case KeyPress(key_name="q"):
        quit()
```

### 4.5 Walrus Operator (`:=`, Python 3.8+)

The assignment expression `:=` assigns a value to a variable as part of an expression.

```python
# Without walrus
line = input()
while line != "quit":
    process(line)
    line = input()

# With walrus
while (line := input()) != "quit":
    process(line)

# Useful in comprehensions
results = [y for x in data if (y := expensive(x)) > threshold]

# Useful with regex
if m := re.search(pattern, text):
    process(m.group())
```

### 4.6 Short-Circuit Evaluation

```python
# 'and' returns first falsy value or last value
0 and 1         # 0
1 and 2         # 2
1 and 2 and 3   # 3

# 'or' returns first truthy value or last value
0 or 1          # 1
0 or "" or []   # []  (all falsy, returns last)
1 or 2          # 1

# Practical uses
name = user_input or "default"     # default if empty string
result = x and x.method()          # safe attribute access if x might be None/0
```

---

## 5. Functions In Depth

---

### 5.1 Function Basics & First-Class Functions

Functions in Python are **first-class objects**: they can be assigned to variables, passed as arguments, returned from other functions, and stored in data structures.

```python
def greet(name):
    return f"Hello, {name}"

# Assign to variable
say_hi = greet
say_hi("Alice")       # "Hello, Alice"

# Pass as argument
def apply(func, value):
    return func(value)

apply(greet, "Bob")   # "Hello, Bob"
apply(len, [1, 2, 3]) # 3

# Store in data structure
operations = {
    'add': lambda a, b: a + b,
    'mul': lambda a, b: a * b,
}
operations['add'](3, 4)  # 7

# Return from function
def make_multiplier(n):
    def multiplier(x):
        return x * n
    return multiplier

double = make_multiplier(2)
double(5)   # 10
```

### 5.2 Parameters & Arguments

```python
# Positional and keyword arguments
def func(a, b, c):
    pass

func(1, 2, 3)           # all positional
func(1, c=3, b=2)       # mix of positional and keyword
func(a=1, b=2, c=3)     # all keyword

# Default values
def func(a, b=10, c=20):
    return a + b + c

func(1)           # 31
func(1, 2)        # 23
func(1, c=5)      # 16

# *args -- variable positional arguments (collected into a tuple)
def func(*args):
    print(args)    # (1, 2, 3)

func(1, 2, 3)

# **kwargs -- variable keyword arguments (collected into a dict)
def func(**kwargs):
    print(kwargs)  # {'a': 1, 'b': 2}

func(a=1, b=2)

# Combined
def func(a, b, *args, **kwargs):
    pass

# Keyword-only arguments (after *)
def func(a, b, *, key=False, verbose=False):
    pass

func(1, 2, key=True)        # OK
func(1, 2, True)             # TypeError -- key must be keyword

# Positional-only arguments (before /, Python 3.8+)
def func(a, b, /, c, d):
    pass

func(1, 2, 3, d=4)          # OK
func(a=1, b=2, c=3, d=4)    # TypeError -- a and b are positional-only

# Full signature
def func(pos_only, /, normal, *, kw_only):
    pass
```

**Argument passing order: `positional-only / normal *args keyword-only **kwargs`**

### 5.3 Scope Rules (LEGB)

Python resolves names using the LEGB rule, checking each scope in order:

```
┌─────────────────────────────────────────┐
│ Built-in (B)                            │
│  ┌───────────────────────────────────┐  │
│  │ Global / Module (G)               │  │
│  │  ┌─────────────────────────────┐  │  │
│  │  │ Enclosing function (E)      │  │  │
│  │  │  ┌───────────────────────┐  │  │  │
│  │  │  │ Local (L)             │  │  │  │
│  │  │  └───────────────────────┘  │  │  │
│  │  └─────────────────────────────┘  │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

| Scope | Description | Example |
|---|---|---|
| **L**ocal | Inside the current function | Function parameters, local variables |
| **E**nclosing | In enclosing functions (closures) | Variables in outer function |
| **G**lobal | Module level | Top-level variables |
| **B**uilt-in | Python built-in names | `len`, `print`, `range` |

```python
x = "global"

def outer():
    x = "enclosing"
    
    def inner():
        x = "local"
        print(x)       # "local"
    
    inner()
    print(x)           # "enclosing"

outer()
print(x)               # "global"

# global and nonlocal keywords
counter = 0

def increment():
    global counter     # refers to module-level counter
    counter += 1

def outer():
    count = 0
    def inner():
        nonlocal count  # refers to enclosing function's count
        count += 1
    inner()
    print(count)        # 1
```

### 5.4 Closures

A **closure** is a function that captures variables from its enclosing scope, retaining access even after the outer function has returned.

```python
def make_counter(start=0):
    count = start
    def counter():
        nonlocal count
        count += 1
        return count
    return counter

c = make_counter()
c()  # 1
c()  # 2
c()  # 3

# Inspecting closure variables
c.__closure__                         # tuple of cell objects
c.__closure__[0].cell_contents        # current value of 'count'
```

### 5.5 Lambda Functions

```python
# Anonymous functions for simple expressions
square = lambda x: x ** 2
add = lambda x, y: x + y

# Common use: sort keys
pairs = [(1, 'b'), (2, 'a'), (3, 'c')]
sorted(pairs, key=lambda p: p[1])   # [(2, 'a'), (1, 'b'), (3, 'c')]

# Limitations: single expression only, no statements, no annotations
```

### 5.6 Mutable Default Arguments (Classic Pitfall)

```python
# BUG: mutable default is shared across all calls
def append_to(element, target=[]):
    target.append(element)
    return target

append_to(1)   # [1]
append_to(2)   # [1, 2] -- NOT [2]! Same list object reused

# FIX: use None sentinel
def append_to(element, target=None):
    if target is None:
        target = []
    target.append(element)
    return target

append_to(1)   # [1]
append_to(2)   # [2] -- fresh list each time
```

**Why this happens:** Default arguments are evaluated **once** when the function is defined, not on each call. Since lists are mutable, the same list object is reused.

---

## 6. Comprehensions & Generator Expressions

---

### 6.1 List Comprehensions

```python
# Basic: [expression for item in iterable]
squares = [x**2 for x in range(10)]

# With filter: [expression for item in iterable if condition]
evens = [x for x in range(20) if x % 2 == 0]

# Nested loops (equivalent to nested for loops, left to right)
pairs = [(x, y) for x in range(3) for y in range(3)]
# same as:
# for x in range(3):
#     for y in range(3):
#         pairs.append((x, y))

# Flatten a 2D list
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [x for row in matrix for x in row]   # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Nested comprehension (list of lists)
transposed = [[row[i] for row in matrix] for i in range(3)]
```

### 6.2 Dict and Set Comprehensions

```python
# Dict comprehension
squares = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Invert a dict
original = {'a': 1, 'b': 2, 'c': 3}
inverted = {v: k for k, v in original.items()}

# Set comprehension
unique_lengths = {len(word) for word in ["hello", "world", "hi", "hey"]}
# {2, 3, 5}
```

### 6.3 Generator Expressions

A generator expression looks like a list comprehension but uses parentheses instead of brackets. It produces values **lazily**, one at a time, without storing the entire sequence in memory.

```python
# Generator expression (lazy)
gen = (x**2 for x in range(1_000_000))  # no memory allocated for results
sum(gen)   # consumes one element at a time

# List comprehension (eager)
lst = [x**2 for x in range(1_000_000)]  # entire list in memory
sum(lst)

# Generator expression is exhausted after one pass
gen = (x for x in range(5))
list(gen)   # [0, 1, 2, 3, 4]
list(gen)   # [] -- already exhausted

# No extra parentheses needed when sole argument to a function
sum(x**2 for x in range(10))        # OK
max(len(word) for word in words)     # OK
```

| Feature | List Comprehension | Generator Expression |
|---|---|---|
| Syntax | `[expr for ...]` | `(expr for ...)` |
| Returns | `list` | `generator` object |
| Memory | O(n) -- stores all elements | O(1) -- one element at a time |
| Reusable | Yes (list persists) | No (single pass, then exhausted) |
| Speed | Slightly faster for small data | Better for large data / pipelines |

---

## 7. Iterators & Generators

---

### 7.1 The Iterator Protocol

An **iterator** is any object that implements two methods:

| Method | Purpose |
|---|---|
| `__iter__()` | Returns the iterator object itself |
| `__next__()` | Returns the next value; raises `StopIteration` when exhausted |

An **iterable** is any object whose `__iter__()` returns an iterator (or that implements `__getitem__`).

```python
# How a for loop works under the hood
# for item in iterable:
#     process(item)
#
# is equivalent to:
iterator = iter(iterable)        # calls iterable.__iter__()
while True:
    try:
        item = next(iterator)    # calls iterator.__next__()
        process(item)
    except StopIteration:
        break
```

```python
# Custom iterator
class Countdown:
    def __init__(self, start):
        self.current = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

list(Countdown(5))   # [5, 4, 3, 2, 1]
```

### 7.2 Generator Functions

A **generator function** uses `yield` to produce a sequence of values lazily. Each call to `next()` resumes execution right after the last `yield`.

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

gen = countdown(5)
next(gen)   # 5
next(gen)   # 4
list(gen)   # [3, 2, 1] -- remaining values

# Generator for Fibonacci
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

from itertools import islice
list(islice(fibonacci(), 10))   # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

**Memory comparison:**

```python
# This stores ALL values in memory
def get_squares_list(n):
    return [x**2 for x in range(n)]

# This yields one value at a time -- O(1) memory
def get_squares_gen(n):
    for x in range(n):
        yield x**2

# Processing 10 million numbers:
# get_squares_list(10_000_000)  # ~80 MB of memory
# get_squares_gen(10_000_000)   # ~100 bytes of memory
```

### 7.3 `yield from` (Delegation)

```python
def chain(*iterables):
    for it in iterables:
        yield from it      # delegates to sub-iterator

list(chain([1, 2], [3, 4], [5]))  # [1, 2, 3, 4, 5]

# Recursive tree traversal
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

list(flatten([1, [2, [3, 4], 5], 6]))  # [1, 2, 3, 4, 5, 6]
```

### 7.4 Generator Methods: `send()`, `throw()`, `close()`

```python
# send() -- send a value INTO the generator
def accumulator():
    total = 0
    while True:
        value = yield total
        if value is None:
            break
        total += value

gen = accumulator()
next(gen)          # 0 (prime the generator)
gen.send(10)       # 10
gen.send(20)       # 30
gen.send(5)        # 35

# close() -- terminate the generator
gen.close()        # raises GeneratorExit inside the generator

# throw() -- raise an exception inside the generator
gen.throw(ValueError, "invalid")
```

### 7.5 The `itertools` Module

| Function | Description | Example |
|---|---|---|
| `chain(*its)` | Concatenate iterables | `chain([1,2], [3,4])` → `1 2 3 4` |
| `chain.from_iterable(it)` | Flatten one level | `chain.from_iterable([[1,2],[3]])` → `1 2 3` |
| `islice(it, stop)` | Slice an iterator | `islice(count(), 5)` → `0 1 2 3 4` |
| `count(start, step)` | Infinite counter | `count(10, 2)` → `10 12 14 ...` |
| `cycle(it)` | Repeat endlessly | `cycle('AB')` → `A B A B ...` |
| `repeat(x, n)` | Repeat x n times | `repeat(0, 3)` → `0 0 0` |
| `product(*its)` | Cartesian product | `product('AB', '12')` → `A1 A2 B1 B2` |
| `permutations(it, r)` | r-length permutations | `permutations('ABC', 2)` → `AB AC BA ...` |
| `combinations(it, r)` | r-length combinations | `combinations('ABC', 2)` → `AB AC BC` |
| `combinations_with_replacement` | With repetition | `cwr('AB', 2)` → `AA AB BB` |
| `groupby(it, key)` | Group consecutive equal items | see below |
| `accumulate(it, func)` | Running accumulation | `accumulate([1,2,3])` → `1 3 6` |
| `zip_longest(*its)` | Zip with fill value | `zip_longest('AB', '1234', fillvalue='-')` |
| `starmap(func, it)` | Apply func to unpacked tuples | `starmap(pow, [(2,3),(3,2)])` → `8 9` |
| `takewhile(pred, it)` | Take while predicate true | `takewhile(lambda x: x<5, [1,3,6,2])` → `1 3` |
| `dropwhile(pred, it)` | Drop while predicate true | `dropwhile(lambda x: x<5, [1,3,6,2])` → `6 2` |
| `filterfalse(pred, it)` | Opposite of filter | `filterfalse(lambda x: x%2, range(6))` → `0 2 4` |
| `tee(it, n)` | Duplicate iterator n times | `a, b = tee(iter([1,2,3]))` |
| `pairwise(it)` | Overlapping pairs (3.10+) | `pairwise('ABCD')` → `AB BC CD` |
| `batched(it, n)` | Groups of n (3.12+) | `batched('ABCDE', 2)` → `AB CD E` |

```python
from itertools import groupby

# groupby requires sorted input for expected grouping
data = sorted([(1, 'a'), (1, 'b'), (2, 'c'), (2, 'd')])
for key, group in groupby(data, key=lambda x: x[0]):
    print(key, list(group))
# 1 [(1, 'a'), (1, 'b')]
# 2 [(2, 'c'), (2, 'd')]
```

---

# Part 2: Object-Oriented Python

---

## 8. Classes & OOP Fundamentals

---

### 8.1 Class Definition

```python
class Dog:
    species = "Canis familiaris"     # class variable (shared by all instances)
    
    def __init__(self, name, age):   # initializer (NOT constructor -- __new__ is)
        self.name = name             # instance variable
        self.age = age               # instance variable
    
    def bark(self):                  # instance method
        return f"{self.name} says woof!"
    
    def __repr__(self):
        return f"Dog(name={self.name!r}, age={self.age})"

d = Dog("Rex", 5)
d.bark()           # "Rex says woof!"
d.species          # "Canis familiaris"
Dog.species        # "Canis familiaris"
```

### 8.2 Instance vs Class vs Static Methods

| Decorator | First Argument | Access | Use Case |
|---|---|---|---|
| *(none)* | `self` (instance) | Instance + class attributes | Most methods |
| `@classmethod` | `cls` (class) | Class attributes only | Alternate constructors, class-level logic |
| `@staticmethod` | *(none)* | No implicit access | Utility functions logically related to the class |

```python
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    
    def __repr__(self):
        return f"Date({self.year}, {self.month}, {self.day})"
    
    @classmethod
    def from_string(cls, date_string):
        """Alternate constructor from 'YYYY-MM-DD' string."""
        year, month, day = map(int, date_string.split('-'))
        return cls(year, month, day)  # cls, not Date -- supports subclassing
    
    @staticmethod
    def is_valid_date(year, month, day):
        """Pure utility -- doesn't need instance or class."""
        return 1 <= month <= 12 and 1 <= day <= 31

d = Date.from_string("2025-03-15")  # classmethod as alternate constructor
Date.is_valid_date(2025, 13, 1)     # False
```

### 8.3 Properties

`@property` turns a method into a managed attribute with getter/setter/deleter.

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius       # convention: _ prefix for "private"
    
    @property
    def radius(self):
        """Getter -- accessed as circle.radius"""
        return self._radius
    
    @radius.setter
    def radius(self, value):
        """Setter -- assigned as circle.radius = 5"""
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value
    
    @property
    def area(self):
        """Read-only computed property."""
        import math
        return math.pi * self._radius ** 2

c = Circle(5)
c.radius           # 5       (calls getter)
c.radius = 10      # OK      (calls setter)
c.radius = -1      # ValueError
c.area             # 314.159... (computed, read-only)
c.area = 100       # AttributeError (no setter defined)
```

### 8.4 `__slots__`

By default, Python stores instance attributes in a per-instance `__dict__` (a dictionary). `__slots__` replaces this with a fixed-size struct, saving memory and providing faster attribute access.

```python
class PointDict:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class PointSlots:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y

import sys
pd = PointDict(1, 2)
ps = PointSlots(1, 2)
sys.getsizeof(pd.__dict__)   # ~104 bytes (dict overhead)
# PointSlots has no __dict__ at all

ps.z = 3   # AttributeError -- cannot add attributes not in __slots__
```

| Feature | `__dict__` (default) | `__slots__` |
|---|---|---|
| Memory per instance | Higher (dict overhead) | Lower (fixed struct) |
| Attribute access speed | Slightly slower (dict lookup) | Slightly faster (index lookup) |
| Dynamic attributes | Yes -- can add any attribute | No -- fixed set only |
| `__dict__` available | Yes | No (unless you add `'__dict__'` to slots) |
| Inheritance | Always available | Must be declared in each subclass |
| `__weakref__` | Yes | Only if included in `__slots__` |

### 8.5 Class Variables vs Instance Variables

```python
class Student:
    school = "MIT"              # class variable
    all_students = []           # class variable (shared mutable -- careful!)
    
    def __init__(self, name):
        self.name = name        # instance variable
        Student.all_students.append(self)

s1 = Student("Alice")
s2 = Student("Bob")

s1.school            # "MIT" (looked up on class)
Student.school       # "MIT"

s1.school = "Stanford"  # creates INSTANCE variable, shadows class variable
s1.school            # "Stanford" (instance)
s2.school            # "MIT" (still the class variable)
Student.school       # "MIT"
```

### 8.6 Name Mangling

```python
class MyClass:
    def __init__(self):
        self.public = 1          # public
        self._protected = 2      # protected by convention (not enforced)
        self.__private = 3       # name-mangled to _MyClass__private

obj = MyClass()
obj.public              # 1
obj._protected          # 2 (accessible, but convention says don't)
obj.__private           # AttributeError
obj._MyClass__private   # 3 (still accessible if you know the mangled name)
```

Name mangling exists to prevent accidental override in subclasses, not for security.

---

## 9. Inheritance & MRO

---

### 9.1 Single Inheritance

```python
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        raise NotImplementedError

class Dog(Animal):
    def speak(self):
        return f"{self.name} says Woof!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says Meow!"

d = Dog("Rex")
d.speak()              # "Rex says Woof!"
isinstance(d, Animal)  # True
isinstance(d, Dog)     # True
issubclass(Dog, Animal)  # True
```

### 9.2 Multiple Inheritance and the Diamond Problem

```python
class A:
    def method(self):
        print("A.method")

class B(A):
    def method(self):
        print("B.method")
        super().method()

class C(A):
    def method(self):
        print("C.method")
        super().method()

class D(B, C):
    def method(self):
        print("D.method")
        super().method()
```

```
         A
        / \
       B   C      ← Diamond problem: which path to A?
        \ /
         D
```

### 9.3 Method Resolution Order (C3 Linearization)

Python uses **C3 linearization** to determine the order in which base classes are searched. You can inspect it:

```python
D.__mro__
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)

D.mro()   # same as above, as a list

d = D()
d.method()
# D.method
# B.method
# C.method
# A.method
# Each class's method is called exactly ONCE, in MRO order
```

**C3 linearization rules:**
1. The class itself comes first.
2. Then its bases, in the order they are listed.
3. A class appears before its parents.
4. If there are multiple parents, the order respects the local precedence (left-to-right listing in the class statement).

### 9.4 `super()` and Cooperative Multiple Inheritance

`super()` doesn't call the "parent" -- it calls the **next class in the MRO**. This enables cooperative multiple inheritance.

```python
class Base:
    def __init__(self, **kwargs):
        pass  # absorb remaining kwargs

class X(Base):
    def __init__(self, x, **kwargs):
        self.x = x
        super().__init__(**kwargs)

class Y(Base):
    def __init__(self, y, **kwargs):
        self.y = y
        super().__init__(**kwargs)

class Z(X, Y):
    def __init__(self, z, **kwargs):
        self.z = z
        super().__init__(**kwargs)

obj = Z(z=1, x=2, y=3)
obj.x, obj.y, obj.z   # 2, 3, 1
```

### 9.5 Mixins

A **mixin** is a class that provides methods to other classes through multiple inheritance but is not intended to stand on its own.

```python
class JsonMixin:
    import json
    def to_json(self):
        return JsonMixin.json.dumps(self.__dict__)
    
    @classmethod
    def from_json(cls, json_str):
        return cls(**JsonMixin.json.loads(json_str))

class LoggableMixin:
    def log(self, message):
        print(f"[{self.__class__.__name__}] {message}")

class User(JsonMixin, LoggableMixin):
    def __init__(self, name, email):
        self.name = name
        self.email = email

u = User("Alice", "alice@example.com")
u.to_json()       # '{"name": "Alice", "email": "alice@example.com"}'
u.log("created")  # [User] created
```

---

## 10. Magic (Dunder) Methods

---

### 10.1 Lifecycle Methods

| Method | When Called |
|---|---|
| `__new__(cls, ...)` | Creates a new instance (before `__init__`). Rarely overridden; used for singletons, immutable types. |
| `__init__(self, ...)` | Initializes the instance (the "constructor" in common usage). |
| `__del__(self)` | Called when the object is garbage collected. Avoid relying on this; use context managers instead. |

```python
class Singleton:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, value):
        self.value = value

a = Singleton(1)
b = Singleton(2)
a is b        # True -- same instance
a.value       # 2    -- __init__ ran again on the same instance
```

### 10.2 Representation Methods

| Method | Purpose | Called By |
|---|---|---|
| `__repr__(self)` | Unambiguous representation (for developers) | `repr(obj)`, interactive shell, debugger |
| `__str__(self)` | Readable representation (for users) | `str(obj)`, `print(obj)` |
| `__format__(self, spec)` | Custom format spec | `format(obj, spec)`, f-strings |

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    
    def __str__(self):
        return f"({self.x}, {self.y})"

p = Point(3, 4)
repr(p)    # "Point(3, 4)"
str(p)     # "(3, 4)"
print(p)   # (3, 4)
f"{p}"     # "(3, 4)"       (uses __str__)
f"{p!r}"   # "Point(3, 4)"  (uses __repr__)
```

**Rule of thumb:** Always implement `__repr__`. If `__str__` is not defined, Python falls back to `__repr__`.

### 10.3 Comparison Methods

| Method | Operator |
|---|---|
| `__eq__(self, other)` | `==` |
| `__ne__(self, other)` | `!=` (defaults to `not __eq__` if not defined) |
| `__lt__(self, other)` | `<` |
| `__le__(self, other)` | `<=` |
| `__gt__(self, other)` | `>` |
| `__ge__(self, other)` | `>=` |

```python
from functools import total_ordering

@total_ordering    # fills in __gt__, __ge__, __ne__ from __eq__ and __lt__
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius
    
    def __eq__(self, other):
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.celsius == other.celsius
    
    def __lt__(self, other):
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.celsius < other.celsius
    
    def __hash__(self):
        return hash(self.celsius)

t1 = Temperature(100)
t2 = Temperature(50)
t1 > t2   # True (auto-generated by @total_ordering)
```

**Important:** If you define `__eq__`, the default `__hash__` is set to `None` (making instances unhashable). Define `__hash__` explicitly if you need your objects in sets/dicts.

### 10.4 Arithmetic Operator Methods

| Method | Operator | Reflected |
|---|---|---|
| `__add__` | `+` | `__radd__` |
| `__sub__` | `-` | `__rsub__` |
| `__mul__` | `*` | `__rmul__` |
| `__truediv__` | `/` | `__rtruediv__` |
| `__floordiv__` | `//` | `__rfloordiv__` |
| `__mod__` | `%` | `__rmod__` |
| `__pow__` | `**` | `__rpow__` |
| `__matmul__` | `@` | `__rmatmul__` |

In-place variants: `__iadd__`, `__isub__`, etc. (for `+=`, `-=`, etc.)

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar):
        return self.__mul__(scalar)
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v = Vector(1, 2) + Vector(3, 4)   # Vector(4, 6)
v = Vector(1, 2) * 3              # Vector(3, 6)
v = 3 * Vector(1, 2)              # Vector(3, 6) -- calls __rmul__
```

### 10.5 Container Protocol

| Method | Enables |
|---|---|
| `__len__(self)` | `len(obj)` |
| `__getitem__(self, key)` | `obj[key]`, iteration, slicing |
| `__setitem__(self, key, val)` | `obj[key] = val` |
| `__delitem__(self, key)` | `del obj[key]` |
| `__contains__(self, item)` | `item in obj` |
| `__iter__(self)` | `for item in obj` |
| `__reversed__(self)` | `reversed(obj)` |

```python
class Deck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = '♠ ♥ ♦ ♣'.split()
    
    def __init__(self):
        self._cards = [(rank, suit) for suit in self.suits
                                    for rank in self.ranks]
    
    def __len__(self):
        return len(self._cards)
    
    def __getitem__(self, position):
        return self._cards[position]
    
    def __contains__(self, card):
        return card in self._cards

deck = Deck()
len(deck)             # 52
deck[0]               # ('2', '♠')
deck[-1]              # ('A', '♣')
deck[::13]            # every 13th card
('A', '♠') in deck    # True

for card in deck:     # iteration works via __getitem__
    pass
```

### 10.6 Callable Objects

```python
class Adder:
    def __init__(self, n):
        self.n = n
    
    def __call__(self, x):
        return self.n + x

add5 = Adder(5)
add5(10)        # 15
callable(add5)  # True
```

### 10.7 Attribute Access Methods

| Method | When Called |
|---|---|
| `__getattr__(self, name)` | When normal attribute lookup fails (fallback) |
| `__getattribute__(self, name)` | On **every** attribute access (use with extreme caution) |
| `__setattr__(self, name, value)` | On every `obj.name = value` |
| `__delattr__(self, name)` | On every `del obj.name` |

```python
class DynamicAttributes:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
    
    def __getattr__(self, name):
        return f"'{name}' not found"

obj = DynamicAttributes(x=1, y=2)
obj.x     # 1 (found in __dict__, __getattr__ not called)
obj.z     # "'z' not found" (__getattr__ called as fallback)
```

---

## 11. Abstract Base Classes & Protocols

---

### 11.1 Abstract Base Classes (`abc` Module)

An ABC defines an interface that subclasses **must** implement.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        pass
    
    def describe(self):
        return f"Area: {self.area():.2f}, Perimeter: {self.perimeter():.2f}"

# Cannot instantiate an ABC
# shape = Shape()   # TypeError: Can't instantiate abstract class

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        import math
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        import math
        return 2 * math.pi * self.radius

c = Circle(5)
c.describe()  # "Area: 78.54, Perimeter: 31.42"
```

### 11.2 Virtual Subclasses

You can register a class as a "virtual subclass" of an ABC without actual inheritance:

```python
from abc import ABC, abstractmethod

class Drawable(ABC):
    @abstractmethod
    def draw(self):
        pass

class ThirdPartyWidget:
    def draw(self):
        print("Drawing widget")

Drawable.register(ThirdPartyWidget)

isinstance(ThirdPartyWidget(), Drawable)   # True
issubclass(ThirdPartyWidget, Drawable)     # True
```

### 11.3 Structural Subtyping with `Protocol` (Python 3.8+)

`Protocol` defines structural (duck) typing -- a class matches if it has the right methods, no inheritance required.

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Renderable(Protocol):
    def render(self) -> str: ...

class HtmlPage:
    def render(self) -> str:
        return "<html>...</html>"

class JsonResponse:
    def render(self) -> str:
        return '{"key": "value"}'

def display(obj: Renderable):
    print(obj.render())

display(HtmlPage())      # works -- HtmlPage has render()
display(JsonResponse())  # works -- JsonResponse has render()

isinstance(HtmlPage(), Renderable)  # True (thanks to @runtime_checkable)
```

| Feature | ABC | Protocol |
|---|---|---|
| Subtyping style | Nominal (explicit inheritance or `register`) | Structural (duck typing) |
| Requires inheritance | Yes (or registration) | No |
| Runtime `isinstance` | Always | Only with `@runtime_checkable` |
| Static type checking | Yes | Yes (with mypy/pyright) |
| Best for | Framework APIs, enforced interfaces | Lightweight interfaces, third-party compatibility |

---

## 12. Descriptors & Metaclasses

---

### 12.1 The Descriptor Protocol

A descriptor is any object that defines `__get__`, `__set__`, or `__delete__`. Descriptors power `property`, `classmethod`, `staticmethod`, and bound methods.

| Method | Called When |
|---|---|
| `__get__(self, obj, objtype=None)` | Attribute accessed on an instance or class |
| `__set__(self, obj, value)` | Attribute set on an instance |
| `__delete__(self, obj)` | Attribute deleted on an instance |

| Type | Has | Precedence |
|---|---|---|
| **Data descriptor** | `__get__` + `__set__` (or `__delete__`) | Overrides instance `__dict__` |
| **Non-data descriptor** | `__get__` only | Instance `__dict__` takes precedence |

```python
# Attribute lookup order:
# 1. Data descriptors on the class (and its MRO)
# 2. Instance __dict__
# 3. Non-data descriptors / class __dict__
```

```python
class Validated:
    """A data descriptor that validates on set."""
    def __init__(self, min_val=None, max_val=None):
        self.min_val = min_val
        self.max_val = max_val
    
    def __set_name__(self, owner, name):
        self.name = name            # called automatically when class is created
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self             # accessed on the class itself
        return obj.__dict__.get(self.name)
    
    def __set__(self, obj, value):
        if self.min_val is not None and value < self.min_val:
            raise ValueError(f"{self.name} must be >= {self.min_val}")
        if self.max_val is not None and value > self.max_val:
            raise ValueError(f"{self.name} must be <= {self.max_val}")
        obj.__dict__[self.name] = value

class Student:
    grade = Validated(min_val=0, max_val=100)
    age = Validated(min_val=0, max_val=150)
    
    def __init__(self, name, grade, age):
        self.name = name
        self.grade = grade   # triggers Validated.__set__
        self.age = age

s = Student("Alice", 95, 20)
s.grade           # 95 (triggers Validated.__get__)
s.grade = 105     # ValueError: grade must be <= 100
```

### 12.2 How `property` Works Under the Hood

`property` is simply a data descriptor:

```python
# This:
class C:
    @property
    def x(self):
        return self._x

# Is equivalent to:
class C:
    def get_x(self):
        return self._x
    x = property(get_x)

# property is roughly:
class property:
    def __init__(self, fget=None, fset=None, fdel=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.fget(obj)
    
    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)
```

### 12.3 Metaclasses

A **metaclass** is the "class of a class." Just as an object is an instance of a class, a class is an instance of its metaclass. The default metaclass is `type`.

```
┌─────────┐  is instance of  ┌──────────┐  is instance of  ┌──────┐
│ my_obj  │ ───────────────▶ │ MyClass  │ ───────────────▶ │ type │
└─────────┘                  └──────────┘                  └──────┘
  (object)                     (class)                    (metaclass)
```

```python
# type is the metaclass of all classes
type(int)        # <class 'type'>
type(str)        # <class 'type'>
type(type)       # <class 'type'>  -- type is its own metaclass

# Creating a class dynamically with type
Dog = type('Dog', (object,), {
    'species': 'canine',
    'bark': lambda self: 'Woof!'
})
d = Dog()
d.bark()   # 'Woof!'
```

```python
# Custom metaclass
class Meta(type):
    def __new__(mcs, name, bases, namespace):
        # Runs when a class using this metaclass is DEFINED
        cls = super().__new__(mcs, name, bases, namespace)
        cls.created_by = "Meta"
        return cls

class MyClass(metaclass=Meta):
    pass

MyClass.created_by   # "Meta"
```

### 12.4 `__init_subclass__` (Simpler Alternative, Python 3.6+)

For most use cases, `__init_subclass__` is preferred over metaclasses:

```python
class Plugin:
    _registry = {}
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Plugin._registry[cls.__name__] = cls

class AudioPlugin(Plugin):
    pass

class VideoPlugin(Plugin):
    pass

Plugin._registry
# {'AudioPlugin': <class 'AudioPlugin'>, 'VideoPlugin': <class 'VideoPlugin'>}
```

---

# Part 3: Intermediate & Advanced

---

## 13. Error Handling & Exceptions

---

### 13.1 Exception Hierarchy (Simplified)

```
BaseException
├── SystemExit
├── KeyboardInterrupt
├── GeneratorExit
└── Exception
    ├── StopIteration
    ├── ArithmeticError
    │   ├── ZeroDivisionError
    │   ├── OverflowError
    │   └── FloatingPointError
    ├── AttributeError
    ├── EOFError
    ├── ImportError
    │   └── ModuleNotFoundError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── NameError
    │   └── UnboundLocalError
    ├── OSError
    │   ├── FileNotFoundError
    │   ├── PermissionError
    │   └── FileExistsError
    ├── RuntimeError
    │   └── RecursionError
    ├── TypeError
    ├── ValueError
    │   └── UnicodeError
    └── Warning
```

**Key point:** `except Exception` catches nearly everything except `SystemExit`, `KeyboardInterrupt`, and `GeneratorExit` -- which is usually what you want.

### 13.2 `try` / `except` / `else` / `finally`

```python
try:
    result = risky_operation()
except ValueError as e:
    # Runs if ValueError is raised
    print(f"Value error: {e}")
except (TypeError, KeyError) as e:
    # Can catch multiple types
    print(f"Error: {e}")
except Exception as e:
    # Catch-all for remaining exceptions (avoid bare except)
    print(f"Unexpected: {e}")
    raise    # re-raise to preserve the traceback
else:
    # Runs ONLY if no exception was raised in try
    process(result)
finally:
    # ALWAYS runs (cleanup), even if exception or return
    cleanup()
```

**Execution flow:**

```
try block succeeds:    try → else → finally
try block fails:       try → except → finally
return in try:         try → finally → return
exception in except:   try → except → finally → propagate
```

### 13.3 Custom Exceptions

```python
class AppError(Exception):
    """Base exception for the application."""
    pass

class ValidationError(AppError):
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

class NotFoundError(AppError):
    pass

# Usage
try:
    raise ValidationError("email", "invalid format")
except ValidationError as e:
    print(e.field, e.message)   # email invalid format
```

### 13.4 Exception Chaining

```python
try:
    int("not_a_number")
except ValueError as e:
    raise RuntimeError("Failed to parse config") from e
# RuntimeError: Failed to parse config
#   caused by: ValueError: invalid literal for int()

# Suppress the chain
raise RuntimeError("clean message") from None
```

### 13.5 LBYL vs EAFP

| Style | Meaning | Approach |
|---|---|---|
| **LBYL** | Look Before You Leap | Check conditions before acting |
| **EAFP** | Easier to Ask Forgiveness than Permission | Try it and handle the exception |

```python
# LBYL (common in C/Java)
if key in dictionary:
    value = dictionary[key]
else:
    value = default

# EAFP (Pythonic)
try:
    value = dictionary[key]
except KeyError:
    value = default

# Even more Pythonic:
value = dictionary.get(key, default)
```

Python favors EAFP because:
- It avoids race conditions (check-then-act is not atomic).
- It's often faster when the common case is success.
- It follows Python's duck typing philosophy.

### 13.6 `ExceptionGroup` (Python 3.11+)

```python
# Group multiple exceptions together
eg = ExceptionGroup("multiple errors", [
    ValueError("bad value"),
    TypeError("wrong type"),
    KeyError("missing key"),
])

try:
    raise eg
except* ValueError as e:
    print(f"Value errors: {e.exceptions}")
except* TypeError as e:
    print(f"Type errors: {e.exceptions}")
# except* uses the new syntax for handling exception groups
```

---

## 14. Context Managers

---

### 14.1 The `with` Statement

A context manager guarantees that setup and teardown code runs, even if an exception occurs. The most common use is file handling.

```python
# Without context manager -- must manually close
f = open('file.txt')
try:
    data = f.read()
finally:
    f.close()

# With context manager -- close is automatic
with open('file.txt') as f:
    data = f.read()
# f.close() called automatically, even if an exception occurred
```

### 14.2 Writing a Context Manager (Class-Based)

Implement `__enter__` and `__exit__`:

```python
class Timer:
    import time as _time
    
    def __enter__(self):
        self.start = Timer._time.perf_counter()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = Timer._time.perf_counter() - self.start
        print(f"Elapsed: {self.elapsed:.4f}s")
        return False  # do not suppress exceptions

with Timer() as t:
    sum(range(1_000_000))
# Elapsed: 0.0234s
```

`__exit__` receives exception info. If it returns `True`, the exception is suppressed.

```python
class Suppress:
    def __init__(self, *exceptions):
        self.exceptions = exceptions
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        return exc_type is not None and issubclass(exc_type, self.exceptions)

with Suppress(FileNotFoundError):
    open('nonexistent.txt')
# No error raised
```

### 14.3 Writing a Context Manager (Generator-Based)

```python
from contextlib import contextmanager

@contextmanager
def timer():
    import time
    start = time.perf_counter()
    try:
        yield    # code inside 'with' block runs here
    finally:
        elapsed = time.perf_counter() - start
        print(f"Elapsed: {elapsed:.4f}s")

with timer():
    sum(range(1_000_000))

# With a yielded value
@contextmanager
def temp_directory():
    import tempfile, shutil
    path = tempfile.mkdtemp()
    try:
        yield path
    finally:
        shutil.rmtree(path)

with temp_directory() as tmpdir:
    print(tmpdir)  # /tmp/tmpXXXXXX
# directory deleted after with block
```

### 14.4 `contextlib` Utilities

| Utility | Purpose |
|---|---|
| `@contextmanager` | Create context manager from a generator function |
| `suppress(*exceptions)` | Suppress specified exceptions |
| `redirect_stdout(target)` | Redirect `sys.stdout` to target |
| `redirect_stderr(target)` | Redirect `sys.stderr` to target |
| `ExitStack` | Manage a dynamic number of context managers |
| `closing(thing)` | Call `thing.close()` on exit |
| `nullcontext(value)` | No-op context manager (returns value) |

```python
from contextlib import ExitStack

# Managing a dynamic number of files
filenames = ['a.txt', 'b.txt', 'c.txt']
with ExitStack() as stack:
    files = [stack.enter_context(open(fn)) for fn in filenames]
    # all files are open here
# all files closed here, even if one raised an exception
```

---

## 15. Decorators

---

### 15.1 Function Decorators

A decorator is a function that takes a function and returns a modified function.

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result
    return wrapper

@my_decorator
def say_hello(name):
    print(f"Hello, {name}!")

say_hello("Alice")
# Before
# Hello, Alice!
# After

# @ syntax is syntactic sugar for:
# say_hello = my_decorator(say_hello)
```

### 15.2 Preserving Metadata with `@wraps`

Without `@wraps`, the decorated function loses its name, docstring, etc.

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)    # preserves func.__name__, __doc__, __module__, etc.
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def my_function():
    """My docstring."""
    pass

my_function.__name__   # 'my_function'  (without @wraps: 'wrapper')
my_function.__doc__    # 'My docstring.' (without @wraps: None)
```

### 15.3 Decorators with Arguments

```python
def repeat(n):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)        # repeat(3) returns the actual decorator
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
# Hello, Alice!
# Hello, Alice!
# Hello, Alice!
```

### 15.4 Class Decorators

```python
# Decorator that adds methods to a class
def add_repr(cls):
    def __repr__(self):
        attrs = ', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())
        return f'{cls.__name__}({attrs})'
    cls.__repr__ = __repr__
    return cls

@add_repr
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

repr(Point(3, 4))   # "Point(x=3, y=4)"
```

### 15.5 Stacking Decorators

Decorators are applied bottom-up (innermost first):

```python
@decorator_a
@decorator_b
@decorator_c
def func():
    pass

# Equivalent to: func = decorator_a(decorator_b(decorator_c(func)))
```

### 15.6 Common Standard Library Decorators

| Decorator | Module | Purpose |
|---|---|---|
| `@property` | built-in | Managed attribute (getter/setter/deleter) |
| `@staticmethod` | built-in | Method that doesn't receive `self` or `cls` |
| `@classmethod` | built-in | Method that receives `cls` as first argument |
| `@functools.wraps` | `functools` | Preserve wrapped function metadata |
| `@functools.lru_cache` | `functools` | Memoization with LRU eviction |
| `@functools.cache` | `functools` | Unbounded memoization (Python 3.9+) |
| `@functools.singledispatch` | `functools` | Single-dispatch generic function |
| `@functools.total_ordering` | `functools` | Fill in comparison methods |
| `@dataclasses.dataclass` | `dataclasses` | Auto-generate `__init__`, `__repr__`, `__eq__`, etc. |
| `@abc.abstractmethod` | `abc` | Mark method as abstract |
| `@contextlib.contextmanager` | `contextlib` | Create context manager from generator |
| `@typing.overload` | `typing` | Declare function overloads for type checkers |

```python
import functools

@functools.lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

fibonacci(100)   # instant (memoized)
fibonacci.cache_info()
# CacheInfo(hits=98, misses=101, maxsize=128, currsize=101)
fibonacci.cache_clear()
```

### 15.7 Practical Decorator Examples

```python
# Timing decorator
import time
from functools import wraps

def timing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

# Retry decorator
def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def fetch_data(url):
    pass

# Authorization decorator
def require_auth(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionError("Authentication required")
        return func(request, *args, **kwargs)
    return wrapper
```

---

## 16. Functional Programming

---

### 16.1 `map`, `filter`, `reduce`

```python
# map -- apply function to each element
list(map(str.upper, ["hello", "world"]))   # ['HELLO', 'WORLD']
list(map(lambda x: x**2, [1, 2, 3]))      # [1, 4, 9]
list(map(pow, [2, 3], [3, 2]))             # [8, 9]  (multiple iterables)

# filter -- keep elements where predicate is True
list(filter(lambda x: x > 0, [-1, 0, 1, 2]))  # [1, 2]
list(filter(None, [0, 1, '', 'a', [], [1]]))   # [1, 'a', [1]]  (truthy values)

# reduce -- fold left
from functools import reduce
reduce(lambda a, b: a + b, [1, 2, 3, 4])      # 10
reduce(lambda a, b: a * b, [1, 2, 3, 4])      # 24
reduce(lambda a, b: a if a > b else b, [3, 1, 4, 1, 5])  # 5 (max)

# Prefer comprehensions/generators over map/filter for readability:
[x**2 for x in range(10)]           # better than list(map(lambda x: x**2, range(10)))
[x for x in data if x > 0]          # better than list(filter(lambda x: x > 0, data))
```

### 16.2 `functools` Module

| Function | Purpose |
|---|---|
| `partial(func, *args, **kwargs)` | Create a new function with some arguments pre-filled |
| `reduce(func, iterable)` | Left fold |
| `lru_cache(maxsize)` | Memoization with LRU eviction |
| `cache` | Unbounded memoization (3.9+) |
| `wraps(func)` | Copy metadata in decorators |
| `total_ordering` | Fill in comparison methods from `__eq__` + one of `<`, `>`, `<=`, `>=` |
| `singledispatch` | Generic function with dispatch on first argument type |
| `cached_property` | One-time computed property (3.8+) |

```python
from functools import partial, singledispatch

# partial -- freeze some arguments
def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)
square(5)    # 25
cube(3)      # 27

# singledispatch -- function overloading by argument type
@singledispatch
def process(data):
    raise TypeError(f"Unsupported type: {type(data)}")

@process.register(str)
def _(data):
    return data.upper()

@process.register(list)
def _(data):
    return sorted(data)

@process.register(int)
def _(data):
    return data * 2

process("hello")     # 'HELLO'
process([3, 1, 2])   # [1, 2, 3]
process(5)           # 10
```

### 16.3 `operator` Module

Provides function versions of Python's operators -- useful with `map`, `reduce`, `sorted`.

```python
import operator

# Instead of lambda
sorted(pairs, key=operator.itemgetter(1))     # same as key=lambda x: x[1]
sorted(objects, key=operator.attrgetter('name'))

reduce(operator.add, [1, 2, 3, 4])     # 10
reduce(operator.mul, [1, 2, 3, 4])     # 24

# Method caller
upcase = operator.methodcaller('upper')
upcase("hello")    # 'HELLO'
list(map(operator.methodcaller('strip'), ['  a  ', ' b ', 'c']))  # ['a', 'b', 'c']
```

---

## 17. Type Hints & Static Typing

---

### 17.1 Basic Annotations

```python
# Variable annotations
name: str = "Alice"
age: int = 30
scores: list[int] = [90, 85, 92]

# Function annotations
def greet(name: str, excited: bool = False) -> str:
    if excited:
        return f"Hello, {name}!!!"
    return f"Hello, {name}"

# Annotations are NOT enforced at runtime
def add(a: int, b: int) -> int:
    return a + b

add("hello", " world")   # works at runtime -- no TypeError
```

### 17.2 `typing` Module

```python
from typing import (
    List, Dict, Tuple, Set, Optional, Union, Any,
    Callable, Iterator, Generator, Sequence, Mapping,
    TypeVar, Generic, Protocol, Literal, TypeAlias,
    ClassVar, Final
)

# Modern syntax (Python 3.9+): use built-in types directly
def func(items: list[int]) -> dict[str, int]:
    pass

# Optional = Union[X, None]
def find(name: str) -> Optional[str]:     # str | None
    pass

# Python 3.10+ union syntax
def find(name: str) -> str | None:
    pass

# Callable
def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

# Literal
def set_direction(direction: Literal['north', 'south', 'east', 'west']) -> None:
    pass

# TypeAlias
Vector: TypeAlias = list[float]
Matrix: TypeAlias = list[list[float]]

# Final
MAX_SIZE: Final = 100    # cannot be reassigned (enforced by type checker)
```

### 17.3 Generics

```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []
    
    def push(self, item: T) -> None:
        self._items.append(item)
    
    def pop(self) -> T:
        return self._items.pop()
    
    def peek(self) -> T:
        return self._items[-1]

stack: Stack[int] = Stack()
stack.push(1)
stack.push(2)
stack.pop()     # type checker knows this returns int

# Bounded TypeVar
from typing import TypeVar
Comparable = TypeVar('Comparable', bound='SupportsLessThan')

# Python 3.12+ syntax (no need for TypeVar)
def first[T](items: list[T]) -> T:
    return items[0]
```

### 17.4 `dataclasses`

```python
from dataclasses import dataclass, field

@dataclass
class Point:
    x: float
    y: float

# Auto-generates: __init__, __repr__, __eq__
p = Point(3.0, 4.0)
print(p)             # Point(x=3.0, y=4.0)
p == Point(3.0, 4.0) # True

@dataclass(frozen=True)    # immutable, hashable
class FrozenPoint:
    x: float
    y: float

@dataclass(order=True)     # auto-generates comparison methods
class Student:
    name: str = field(compare=False)   # excluded from comparisons
    gpa: float = 0.0
    courses: list[str] = field(default_factory=list)  # mutable default
    
    def __post_init__(self):
        if self.gpa < 0 or self.gpa > 4.0:
            raise ValueError("GPA must be between 0 and 4.0")
```

| `@dataclass` Parameter | Effect |
|---|---|
| `init=True` | Generate `__init__` |
| `repr=True` | Generate `__repr__` |
| `eq=True` | Generate `__eq__` (and `__ne__`) |
| `order=False` | Generate `__lt__`, `__le__`, `__gt__`, `__ge__` |
| `frozen=False` | Make instances immutable |
| `slots=False` | Use `__slots__` (Python 3.10+) |
| `kw_only=False` | All fields are keyword-only (Python 3.10+) |

### 17.5 `NamedTuple` (Typed)

```python
from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float
    label: str = "origin"

p = Point(3, 4)
p.x, p.y         # 3, 4
x, y, label = p  # unpacking works
p[0]              # 3 (indexing works)
```

| Feature | `dataclass` | `NamedTuple` |
|---|---|---|
| Mutable | Yes (unless `frozen=True`) | No (tuples are immutable) |
| Inheritance | Yes | Limited |
| Memory | Higher (dict-based, unless `slots=True`) | Lower (tuple-based) |
| Indexing | No | Yes |
| Unpacking | No (unless you add `__iter__`) | Yes |
| Default values | Yes | Yes |
| Type checking | Yes | Yes |

---

## 18. Modules, Packages & Import System

---

### 18.1 Module Basics

A **module** is any `.py` file. A **package** is a directory containing modules and an `__init__.py` file (or a namespace package without one).

```
my_package/
├── __init__.py          # makes this directory a package
├── module_a.py
├── module_b.py
└── sub_package/
    ├── __init__.py
    └── module_c.py
```

```python
# Importing
import my_package.module_a
from my_package import module_a
from my_package.module_a import some_function
from my_package.sub_package.module_c import SomeClass

# Aliasing
import numpy as np
from collections import defaultdict as dd
```

### 18.2 Import Search Order

When you write `import foo`, Python searches in this order:

1. **`sys.modules`** -- cache of already-imported modules
2. **Built-in modules** -- compiled into the interpreter (e.g., `sys`, `os`)
3. **`sys.path`** -- list of directories, in order:
   - Directory of the script being run (or current directory)
   - `PYTHONPATH` environment variable entries
   - Installation-dependent defaults (site-packages, etc.)

```python
import sys
print(sys.path)       # shows the search path
print(sys.modules)    # shows all loaded modules
```

### 18.3 Relative vs Absolute Imports

```python
# Absolute import (preferred in most cases)
from my_package.sub_package import module_c

# Relative import (only works inside packages)
from . import module_b           # same package
from .. import module_a          # parent package
from ..sub_package import module_c  # sibling package
```

### 18.4 `__init__.py`

The `__init__.py` file runs when the package is first imported. Common uses:

```python
# my_package/__init__.py

# Re-export public API
from .module_a import ClassA
from .module_b import function_b

# Define __all__ for 'from my_package import *'
__all__ = ['ClassA', 'function_b']

# Package-level initialization
print("my_package initialized")
```

### 18.5 Circular Imports

```python
# a.py
from b import func_b    # tries to import b, which imports a → circular!

def func_a():
    return "A"

# b.py
from a import func_a    # ImportError (or partially initialized module)

def func_b():
    return func_a()
```

**Solutions:**
1. **Move import inside function** (deferred import):
   ```python
   def func_b():
       from a import func_a
       return func_a()
   ```
2. **Restructure** to eliminate the cycle (best approach).
3. **Import the module, not the name:**
   ```python
   import a
   def func_b():
       return a.func_a()
   ```

### 18.6 `__all__`

Controls what is exported by `from module import *`:

```python
# my_module.py
__all__ = ['public_func', 'PublicClass']

def public_func():
    pass

class PublicClass:
    pass

def _private_helper():  # not in __all__, excluded from star import
    pass
```

### 18.7 Virtual Environments

```bash
# Create a virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Unix/macOS)
source .venv/bin/activate

# Install packages
pip install requests flask

# Freeze dependencies
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt

# Deactivate
deactivate
```

---

# Part 4: Concurrency & Performance

---

## 19. The GIL & Threading

---

### 19.1 The Global Interpreter Lock (GIL)

The **GIL** is a mutex in CPython that allows only **one thread** to execute Python bytecode at a time, even on multi-core machines.

```
Thread 1:   ████░░░░████░░░░████
Thread 2:   ░░░░████░░░░████░░░░
            ────────────────────▶ time
            Only one thread runs Python bytecode at any instant
```

**Why the GIL exists:**
- Simplifies CPython's memory management (reference counting is not thread-safe without it).
- Makes C extensions easier to write.
- Single-threaded performance is not penalized.

**Implications:**

| Workload Type | Threads Help? | Why |
|---|---|---|
| **I/O-bound** (network, disk, DB) | Yes | GIL is released during I/O waits |
| **CPU-bound** (computation) | No | GIL prevents true parallelism |

For CPU-bound parallelism, use `multiprocessing`, `concurrent.futures.ProcessPoolExecutor`, or C extensions that release the GIL.

### 19.2 `threading` Module

```python
import threading
import time

def worker(name, duration):
    print(f"{name} starting")
    time.sleep(duration)         # GIL is released during sleep
    print(f"{name} done")

# Create and start threads
t1 = threading.Thread(target=worker, args=("Thread-1", 2))
t2 = threading.Thread(target=worker, args=("Thread-2", 1))

t1.start()
t2.start()

t1.join()    # wait for t1 to finish
t2.join()    # wait for t2 to finish
print("All done")
```

### 19.3 Synchronization Primitives

| Primitive | Purpose |
|---|---|
| `Lock` | Mutual exclusion (binary lock) |
| `RLock` | Reentrant lock (same thread can acquire multiple times) |
| `Semaphore` | Allow up to N threads into a section |
| `Event` | One thread signals, others wait |
| `Condition` | Wait for a condition to become true |
| `Barrier` | All threads wait until N arrive |

```python
import threading

# Lock -- prevent race conditions
counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(100_000):
        with lock:
            counter += 1

threads = [threading.Thread(target=increment) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(counter)   # 400000 (correct with lock, would be < 400000 without)
```

```python
# Event -- signaling between threads
event = threading.Event()

def waiter():
    print("Waiting for event...")
    event.wait()          # blocks until event is set
    print("Event received!")

def setter():
    import time
    time.sleep(2)
    print("Setting event")
    event.set()           # all waiters unblock

threading.Thread(target=waiter).start()
threading.Thread(target=setter).start()
```

```python
# Semaphore -- limit concurrent access
semaphore = threading.Semaphore(3)   # allow 3 concurrent threads

def limited_resource(name):
    with semaphore:
        print(f"{name} acquired")
        import time
        time.sleep(1)
    print(f"{name} released")
```

### 19.4 Daemon Threads

A daemon thread is killed when all non-daemon threads have finished.

```python
t = threading.Thread(target=background_task, daemon=True)
t.start()
# program can exit without waiting for t
```

### 19.5 Thread-Safe Data Structures

```python
import queue

q = queue.Queue()        # FIFO, thread-safe
q.put("item")
item = q.get()           # blocks until an item is available
q.task_done()

q = queue.LifoQueue()    # LIFO (stack)
q = queue.PriorityQueue()  # priority queue

# Producer-consumer pattern
def producer(q):
    for i in range(10):
        q.put(i)
    q.put(None)  # sentinel

def consumer(q):
    while True:
        item = q.get()
        if item is None:
            break
        process(item)
        q.task_done()
```

---

## 20. Multiprocessing

---

### 20.1 Basics

`multiprocessing` creates separate OS processes, each with its own Python interpreter and GIL. True parallelism for CPU-bound tasks.

```python
from multiprocessing import Process
import os

def worker(name):
    print(f"{name} running in PID {os.getpid()}")

if __name__ == '__main__':
    processes = []
    for i in range(4):
        p = Process(target=worker, args=(f"Worker-{i}",))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
```

**Important:** Always guard multiprocessing code with `if __name__ == '__main__':` on Windows to prevent infinite subprocess spawning.

### 20.2 `Pool` for Parallel Map

```python
from multiprocessing import Pool

def square(x):
    return x ** 2

if __name__ == '__main__':
    with Pool(processes=4) as pool:
        results = pool.map(square, range(10))
        # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
        
        # Async variant
        async_result = pool.apply_async(square, (42,))
        print(async_result.get())   # 1764
        
        # imap for lazy results
        for result in pool.imap(square, range(100)):
            process(result)
        
        # imap_unordered for faster throughput when order doesn't matter
        for result in pool.imap_unordered(square, range(100)):
            process(result)
```

### 20.3 Inter-Process Communication

```python
from multiprocessing import Queue, Pipe

# Queue (thread/process-safe)
def producer(q):
    q.put([1, 2, 3])

def consumer(q):
    data = q.get()
    print(data)

q = Queue()

# Pipe (bidirectional, two endpoints)
parent_conn, child_conn = Pipe()
parent_conn.send("hello")
child_conn.recv()  # "hello"
```

### 20.4 Shared Memory

```python
from multiprocessing import Value, Array, Manager

# Value and Array -- shared between processes (with locks)
counter = Value('i', 0)     # 'i' = signed int
shared_array = Array('d', [0.0] * 10)  # 'd' = double

# Manager -- provides shared dicts, lists, etc. (slower, uses proxies)
with Manager() as manager:
    shared_dict = manager.dict()
    shared_list = manager.list()
```

### 20.5 When to Use What

| Criterion | `threading` | `multiprocessing` |
|---|---|---|
| Best for | I/O-bound tasks | CPU-bound tasks |
| GIL | Shared (limits CPU parallelism) | Separate GIL per process |
| Memory | Shared (lightweight) | Separate (heavier) |
| Communication | Shared variables (with locks) | IPC (Queue, Pipe, shared memory) |
| Startup cost | Low | High (fork/spawn process) |
| Data sharing | Easy (same address space) | Hard (must serialize) |
| Fault isolation | No (thread crash = process crash) | Yes (process crash is isolated) |

---

## 21. Asyncio & Async/Await

---

### 21.1 Core Concepts

**Asyncio** provides cooperative multitasking via an **event loop** that runs **coroutines**. While one coroutine is waiting for I/O, the event loop runs another.

```
Event Loop (single thread):

    Task A: ████░░░░░░████░░░░████
    Task B: ░░░░████░░░░░░████░░░░
    Task C: ░░░░░░░░████░░░░░░░░░░
                    │
                    └── "░" = awaiting I/O (yielded control)
                         "█" = running Python code
```

### 21.2 Coroutines

```python
import asyncio

async def fetch_data(url):
    print(f"Fetching {url}")
    await asyncio.sleep(1)     # simulates I/O wait (non-blocking)
    return f"Data from {url}"

async def main():
    result = await fetch_data("https://example.com")
    print(result)

asyncio.run(main())   # entry point -- creates and runs the event loop
```

### 21.3 Concurrent Tasks

```python
import asyncio

async def fetch(url, delay):
    await asyncio.sleep(delay)
    return f"Data from {url}"

async def main():
    # Run concurrently with gather
    results = await asyncio.gather(
        fetch("url1", 1),
        fetch("url2", 2),
        fetch("url3", 1),
    )
    # Takes ~2 seconds (not 4) -- tasks run concurrently
    print(results)  # ["Data from url1", "Data from url2", "Data from url3"]

    # Create individual tasks for more control
    task1 = asyncio.create_task(fetch("url1", 1))
    task2 = asyncio.create_task(fetch("url2", 2))
    
    result1 = await task1
    result2 = await task2

asyncio.run(main())
```

### 21.4 `TaskGroup` (Python 3.11+, Structured Concurrency)

```python
async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(fetch("url1", 1))
        task2 = tg.create_task(fetch("url2", 2))
    
    # All tasks are guaranteed complete here
    print(task1.result(), task2.result())
```

### 21.5 Async Iteration and Context Managers

```python
# Async iterator
async def async_range(n):
    for i in range(n):
        await asyncio.sleep(0.1)
        yield i

async def main():
    async for value in async_range(5):
        print(value)

# Async context manager
class AsyncConnection:
    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

async def main():
    async with AsyncConnection() as conn:
        await conn.query("SELECT ...")
```

### 21.6 Async Queue

```python
import asyncio

async def producer(queue):
    for i in range(5):
        await asyncio.sleep(0.5)
        await queue.put(i)
    await queue.put(None)  # sentinel

async def consumer(queue):
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"Consumed: {item}")
        queue.task_done()

async def main():
    queue = asyncio.Queue()
    await asyncio.gather(
        producer(queue),
        consumer(queue),
    )

asyncio.run(main())
```

### 21.7 When to Use Asyncio

| Use Asyncio When | Don't Use Asyncio When |
|---|---|
| Many concurrent I/O operations (HTTP, DB, files) | CPU-bound work (use multiprocessing) |
| Web servers / API clients | Simple scripts with sequential I/O |
| WebSockets, streaming protocols | Libraries don't support async |
| Chat servers, real-time applications | Small number of connections |

---

## 22. `concurrent.futures`

---

### 22.1 High-Level Interface

`concurrent.futures` provides a unified API for both threading and multiprocessing.

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# ThreadPoolExecutor -- for I/O-bound tasks
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(fetch_url, url) for url in urls]
    
    for future in futures:
        result = future.result()     # blocks until done
        print(result)

# ProcessPoolExecutor -- for CPU-bound tasks
with ProcessPoolExecutor(max_workers=4) as executor:
    results = executor.map(cpu_intensive_func, data)
    for result in results:
        print(result)
```

### 22.2 `Future` Objects

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def slow_task(n):
    import time
    time.sleep(n)
    return n * 10

with ThreadPoolExecutor() as executor:
    futures = {executor.submit(slow_task, n): n for n in [3, 1, 2]}
    
    # as_completed -- yields futures in completion order
    for future in as_completed(futures):
        n = futures[future]
        try:
            result = future.result()
            print(f"Task {n} returned {result}")
        except Exception as e:
            print(f"Task {n} failed: {e}")

# Output (order may vary):
# Task 1 returned 10
# Task 2 returned 20
# Task 3 returned 30
```

### 22.3 `executor.map` vs `executor.submit`

| Feature | `map(func, *iterables)` | `submit(func, *args, **kwargs)` |
|---|---|---|
| Returns | Iterator of results (in order) | `Future` object |
| Exception handling | Raised on iteration | Via `future.result()` |
| Flexibility | Simple parallel map | Full control (cancellation, callbacks) |
| Multiple args | Multiple iterables (like `map()`) | Any args/kwargs |

```python
# Callbacks on futures
future = executor.submit(slow_task, 5)
future.add_done_callback(lambda f: print(f"Done: {f.result()}"))
future.cancel()        # attempt to cancel
future.cancelled()     # check if cancelled
future.done()          # check if finished
future.running()       # check if running
```

---

## 23. Performance & Optimization

---

### 23.1 Profiling Tools

| Tool | Purpose | Granularity |
|---|---|---|
| `timeit` | Microbenchmark expressions/statements | Single line |
| `cProfile` | Function-level CPU profiler | Per function call |
| `profile` | Pure Python profiler (slower, more portable) | Per function call |
| `line_profiler` | Line-by-line profiling (third-party) | Per line |
| `memory_profiler` | Line-by-line memory profiling (third-party) | Per line |
| `tracemalloc` | Track memory allocations | Per allocation |

```python
# timeit -- quick benchmarks
import timeit

timeit.timeit('sum(range(1000))', number=10_000)
# returns total time in seconds

# From command line:
# python -m timeit "sum(range(1000))"

# cProfile
import cProfile

cProfile.run('my_function()')

# Detailed profiling to file
cProfile.run('my_function()', 'output.prof')
import pstats
p = pstats.Stats('output.prof')
p.sort_stats('cumulative').print_stats(10)  # top 10 by cumulative time
```

### 23.2 Common Optimizations

| Slow | Fast | Why |
|---|---|---|
| `for` loop with string concatenation | `''.join(parts)` | String concat creates new object each time |
| `list.insert(0, x)` | `collections.deque.appendleft(x)` | O(n) vs O(1) |
| `if x in list` | `if x in set` | O(n) vs O(1) |
| Global variable access in loop | Local variable (assign before loop) | Local lookups are faster |
| `range(len(lst))` | `enumerate(lst)` | More Pythonic and often faster |
| Multiple `if`/`elif` | `dict` dispatch | O(1) lookup vs O(n) comparisons |
| `**` for squaring | `x * x` | Avoids function call overhead |
| Repeated attribute access `obj.method` | `method = obj.method` then call `method` | Cache the lookup |

```python
# String concatenation
# Slow: O(n²)
result = ""
for s in strings:
    result += s

# Fast: O(n)
result = "".join(strings)

# Membership testing
# Slow: O(n) per check
if item in my_list:
    pass

# Fast: O(1) per check
my_set = set(my_list)
if item in my_set:
    pass

# Dict dispatch vs if/elif
def handle_a(): pass
def handle_b(): pass
def handle_c(): pass

# Slow
if action == 'a':
    handle_a()
elif action == 'b':
    handle_b()
elif action == 'c':
    handle_c()

# Fast
dispatch = {'a': handle_a, 'b': handle_b, 'c': handle_c}
dispatch[action]()
```

### 23.3 `__slots__` for Memory Optimization

```python
import sys

class WithDict:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class WithSlots:
    __slots__ = ('x', 'y', 'z')
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

# Memory comparison (approximate)
wd = WithDict(1, 2, 3)
ws = WithSlots(1, 2, 3)
sys.getsizeof(wd) + sys.getsizeof(wd.__dict__)  # ~200 bytes
sys.getsizeof(ws)                                 # ~64 bytes
```

### 23.4 When to Optimize

1. **Profile first** -- don't guess where the bottleneck is.
2. **Algorithmic improvements** first (O(n²) → O(n log n) beats any micro-optimization).
3. **Use built-in functions** -- they are implemented in C and heavily optimized.
4. **Consider numpy** for numeric work -- vectorized operations avoid Python loops.
5. **Use C extensions** (Cython, ctypes, pybind11) for truly CPU-critical sections.

---

# Part 5: Memory, Internals & Best Practices

---

## 24. Memory Management & Garbage Collection

---

### 24.1 Reference Counting

CPython's primary garbage collection mechanism is **reference counting**. Each object has a count of references pointing to it. When the count drops to zero, the object is immediately deallocated.

```python
import sys

a = [1, 2, 3]
sys.getrefcount(a)   # 2 (a + temporary reference from getrefcount itself)

b = a
sys.getrefcount(a)   # 3 (a + b + temporary)

del b
sys.getrefcount(a)   # 2

# Reference count increases:
# - Assignment (b = a)
# - Passed as argument
# - Added to a container (list, dict, etc.)
# - A new name/alias is created

# Reference count decreases:
# - del statement
# - Name goes out of scope
# - Name is reassigned
# - Object is removed from container
```

### 24.2 The Cyclic Garbage Collector

Reference counting cannot handle **reference cycles**:

```python
a = []
b = []
a.append(b)  # a → b
b.append(a)  # b → a → cycle!

del a, b     # refcount of both is 1 (from the other list), never reaches 0
```

CPython has a **cyclic garbage collector** (`gc` module) that detects and collects cycles. It uses a **generational** approach:

| Generation | Contains | Collected |
|---|---|---|
| Generation 0 | Newly created objects | Frequently |
| Generation 1 | Survived 1 collection | Less frequently |
| Generation 2 | Survived 2+ collections | Rarely |

```python
import gc

gc.get_count()          # (gen0_count, gen1_count, gen2_count)
gc.get_threshold()      # (700, 10, 10) -- defaults
gc.collect()            # force a collection cycle
gc.disable()            # disable automatic collection (not recommended)
gc.enable()

gc.set_debug(gc.DEBUG_LEAK)  # debug reference leaks
```

### 24.3 Weak References

A **weak reference** does not increase the reference count, allowing the object to be garbage collected.

```python
import weakref

class ExpensiveObject:
    def __init__(self, name):
        self.name = name

obj = ExpensiveObject("important")
weak = weakref.ref(obj)

weak()           # <ExpensiveObject object> (the object, still alive)
del obj
weak()           # None (object was garbage collected)

# WeakValueDictionary -- cache that doesn't prevent garbage collection
cache = weakref.WeakValueDictionary()
obj = ExpensiveObject("data")
cache['key'] = obj
cache['key']     # <ExpensiveObject object>
del obj
cache.get('key') # None (collected)
```

### 24.4 Memory Profiling

```python
import sys
import tracemalloc

# sys.getsizeof -- size of a single object (not including referenced objects)
sys.getsizeof([])        # 56 bytes (empty list)
sys.getsizeof([1, 2, 3]) # 88 bytes (list object, not the ints themselves)
sys.getsizeof({})        # 64 bytes (empty dict)
sys.getsizeof("")        # 49 bytes (empty string)

# tracemalloc -- trace memory allocations
tracemalloc.start()

data = [list(range(100)) for _ in range(1000)]

snapshot = tracemalloc.take_snapshot()
stats = snapshot.statistics('lineno')
for stat in stats[:5]:
    print(stat)  # shows top memory-consuming lines
```

### 24.5 Small Integer and String Caching

```python
# Small integers [-5, 256] are pre-allocated singletons
a = 256
b = 256
a is b    # True

a = 257
b = 257
a is b    # False (may vary in interactive mode vs scripts)

# String interning
a = "hello"
b = "hello"
a is b    # True (identifier-like strings are interned)

import sys
a = sys.intern("hello world")  # manually intern a string
b = sys.intern("hello world")
a is b    # True
```

---

## 25. Copy Semantics

---

### 25.1 Assignment Is Not Copying

```python
original = [[1, 2], [3, 4]]
alias = original       # NOT a copy -- same object

alias[0][0] = 99
print(original)        # [[99, 2], [3, 4]] -- modified!
```

### 25.2 Shallow Copy

A shallow copy creates a new outer container but does **not** copy nested objects.

```python
import copy

original = [[1, 2], [3, 4]]

# Three ways to shallow copy a list:
shallow1 = original.copy()
shallow2 = original[:]
shallow3 = list(original)
shallow4 = copy.copy(original)

shallow1[0][0] = 99
print(original)   # [[99, 2], [3, 4]] -- inner list shared!

shallow1.append([5, 6])
print(original)   # [[99, 2], [3, 4]] -- outer list not affected
```

```
original: ──▶ [ ref₁, ref₂ ]
                │       │
shallow:  ──▶ [ ref₁, ref₂ ]    ← new outer list, same inner refs
                │       │
              [1, 2]  [3, 4]     ← shared inner lists
```

### 25.3 Deep Copy

A deep copy recursively copies all nested objects.

```python
import copy

original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)

deep[0][0] = 99
print(original)   # [[1, 2], [3, 4]] -- unaffected
```

```
original: ──▶ [ ref₁, ref₂ ]
                │       │
              [1, 2]  [3, 4]

deep:     ──▶ [ ref₃, ref₄ ]    ← new outer list
                │       │
              [1, 2]  [3, 4]     ← new inner lists (independent copies)
```

### 25.4 Copy Summary

| Operation | Creates New Outer Object | Copies Inner Objects | Handles Cycles |
|---|---|---|---|
| `=` (assignment) | No | No | N/A |
| Shallow copy | Yes | No (shared references) | No |
| Deep copy | Yes | Yes (recursive) | Yes (tracks seen objects) |

**When to use which:**
- Assignment: when you want an alias (intentional sharing).
- Shallow copy: when the container has only immutable elements (ints, strings, tuples).
- Deep copy: when the container has mutable elements and you need full independence.

---

## 26. Python Internals (CPython)

---

### 26.1 Compilation Pipeline

Python is not purely interpreted. CPython compiles source code to **bytecode**, which is then interpreted by the **Python Virtual Machine (PVM)**.

```
Source Code (.py)
       │
       ▼
    Lexer / Tokenizer
       │
       ▼
    Parser → AST (Abstract Syntax Tree)
       │
       ▼
    Compiler → Bytecode (.pyc)
       │
       ▼
    PVM (Python Virtual Machine) → Execution
```

### 26.2 Bytecode and the `dis` Module

```python
import dis

def add(a, b):
    return a + b

dis.dis(add)
#   2           0 LOAD_FAST                0 (a)
#               2 LOAD_FAST                1 (b)
#               4 BINARY_ADD
#               6 RETURN_VALUE

# Code object attributes
add.__code__.co_consts       # constants used
add.__code__.co_varnames     # local variable names
add.__code__.co_stacksize    # max stack depth
```

### 26.3 `__pycache__` and `.pyc` Files

When a module is imported, CPython compiles it to bytecode and caches it in `__pycache__/` as a `.pyc` file (e.g., `module.cpython-312.pyc`). On subsequent imports, if the source hasn't changed, the `.pyc` is loaded directly (faster startup).

```python
# Prevent .pyc generation:
# python -B script.py
# or set PYTHONDONTWRITEBYTECODE=1
```

### 26.4 Frame Objects

Each function call creates a **frame object** on the call stack. Frames are inspectable:

```python
import sys

def outer():
    def inner():
        frame = sys._getframe(0)    # current frame
        print(frame.f_lineno)       # current line number
        print(frame.f_locals)       # local variables
        print(frame.f_back)         # caller's frame
        print(frame.f_code.co_name) # function name
    inner()

outer()
```

### 26.5 How Closures Work (Cell Variables)

When a nested function references a variable from an enclosing scope, CPython stores that variable in a **cell object**. Both the inner and outer functions share a reference to this cell.

```python
def outer():
    x = 10           # stored in a cell object
    def inner():
        return x     # LOAD_DEREF (load from cell)
    return inner

f = outer()
f.__closure__                    # (<cell object>,)
f.__closure__[0].cell_contents   # 10

import dis
dis.dis(f)
# LOAD_DEREF  0 (x)    ← loads from closure cell, not local scope
```

### 26.6 Object Header and Memory Layout

Every CPython object has at minimum:

```
┌────────────────────────────┐
│ ob_refcnt  (Py_ssize_t)   │  reference count (8 bytes on 64-bit)
├────────────────────────────┤
│ ob_type    (PyTypeObject*) │  pointer to type object (8 bytes)
├────────────────────────────┤
│ ... object-specific data   │  varies by type
└────────────────────────────┘
```

This is why even a simple `int` occupies 28 bytes in CPython:
- 8 bytes for `ob_refcnt`
- 8 bytes for `ob_type`
- 4 bytes for `ob_size` (number of digits)
- 4+ bytes for the actual integer value (variable length for big ints)

---

## 27. Common Gotchas & Best Practices

---

### 27.1 Mutable Default Arguments

```python
# WRONG
def add_item(item, items=[]):
    items.append(item)
    return items

add_item(1)   # [1]
add_item(2)   # [1, 2] -- NOT [2]!

# CORRECT
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### 27.2 Late-Binding Closures

```python
# WRONG -- all lambdas capture the same variable i
funcs = [lambda: i for i in range(5)]
[f() for f in funcs]   # [4, 4, 4, 4, 4] -- all return final value of i

# CORRECT -- default argument captures current value
funcs = [lambda i=i: i for i in range(5)]
[f() for f in funcs]   # [0, 1, 2, 3, 4]

# Also applies to closures in loops
def create_funcs():
    funcs = []
    for i in range(5):
        def f(x=i):     # capture current i via default arg
            return x
        funcs.append(f)
    return funcs
```

### 27.3 `is` vs `==`

```python
# Use 'is' ONLY for:
x is None
x is True
x is False
x is NotImplemented

# Use '==' for everything else
a == b        # value comparison
a != b        # value comparison

# Common mistake:
if x is 0:     # WRONG -- may fail for large integers
if x == 0:     # CORRECT
```

### 27.4 Integer Caching Surprises

```python
a = 256; b = 256; a is b   # True (cached)
a = 257; b = 257; a is b   # May be True or False depending on context

# In the REPL, each line is compiled separately:
>>> a = 257
>>> b = 257
>>> a is b   # False

# In a script or same expression, the compiler may optimize:
a = 257; b = 257; a is b   # Often True (compiler constant folding)
```

### 27.5 Variable Scoping in Loops

```python
# Variables are NOT scoped to loops
for i in range(10):
    pass
print(i)   # 9 -- i is still accessible

# List comprehension variables ARE scoped (Python 3)
[x for x in range(10)]
print(x)   # NameError (in Python 3; would be 9 in Python 2)
```

### 27.6 Tuple "Immutability" with Mutable Elements

```python
t = ([1, 2], [3, 4])
t[0].append(5)          # works! t is now ([1, 2, 5], [3, 4])
t[0] = [10]             # TypeError -- can't reassign tuple element

# The tuple is immutable (its slots can't be reassigned),
# but the objects it references can be mutable.
```

### 27.7 Chained Assignment and Augmented Assignment

```python
# Chained assignment -- all point to same object
a = b = c = []
a.append(1)
print(b)    # [1] -- same list!

# Augmented assignment with mutables
a = [1, 2]
b = a
a += [3]     # list.__iadd__ -- mutates in place
print(b)     # [1, 2, 3] -- b sees the change

a = (1, 2)
b = a
a += (3,)    # tuple.__add__ -- creates new tuple
print(b)     # (1, 2) -- b doesn't see the change
```

### 27.8 Pythonic Idioms

```python
# Swap variables
a, b = b, a

# Multiple assignment
x, y, z = 1, 2, 3

# Unpack with *
first, *rest = [1, 2, 3, 4]

# Check emptiness
if not my_list:        # Pythonic
if len(my_list) == 0:  # not Pythonic

# Use enumerate
for i, item in enumerate(items):
    pass

# Use zip for parallel iteration
for a, b in zip(list1, list2):
    pass

# Dictionary .get() with default
value = d.get(key, default_value)

# Conditional expression
x = a if condition else b

# String joining
result = ', '.join(items)

# List/dict/set comprehension over map/filter
squares = [x**2 for x in range(10)]

# Context managers for resource management
with open('file.txt') as f:
    pass

# Use collections.Counter for counting
from collections import Counter
counts = Counter(items)

# any() and all()
if any(x > 0 for x in numbers):
    pass
if all(x > 0 for x in numbers):
    pass

# Chained comparisons
if 0 < x < 10:
    pass
```

### 27.9 PEP 8 Highlights

| Guideline | Rule |
|---|---|
| Indentation | 4 spaces (no tabs) |
| Max line length | 79 characters (72 for docstrings) |
| Blank lines | 2 between top-level definitions; 1 between methods |
| Imports | One per line; at top of file; grouped (stdlib, third-party, local) |
| Naming: modules | `lowercase_underscore` |
| Naming: classes | `CapitalizedWords` (PascalCase) |
| Naming: functions/variables | `lowercase_underscore` (snake_case) |
| Naming: constants | `UPPER_CASE_WITH_UNDERSCORES` |
| Naming: private | `_single_leading_underscore` |
| Naming: name mangling | `__double_leading_underscore` |
| Comparisons | `if x is None:` not `if x == None:` |
| Boolean tests | `if flag:` not `if flag == True:` |

---

## 28. Testing

---

### 28.1 `unittest` Framework

```python
import unittest

class TestMathOperations(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Runs once before all tests in this class."""
        cls.data = load_test_data()
    
    def setUp(self):
        """Runs before each test method."""
        self.calculator = Calculator()
    
    def test_add(self):
        self.assertEqual(self.calculator.add(2, 3), 5)
    
    def test_divide(self):
        self.assertAlmostEqual(self.calculator.divide(1, 3), 0.333, places=3)
    
    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calculator.divide(1, 0)
    
    def test_negative(self):
        self.assertTrue(self.calculator.is_negative(-1))
        self.assertFalse(self.calculator.is_negative(1))
    
    def tearDown(self):
        """Runs after each test method."""
        pass
    
    @classmethod
    def tearDownClass(cls):
        """Runs once after all tests in this class."""
        pass

if __name__ == '__main__':
    unittest.main()
```

**Common assert methods:**

| Method | Checks |
|---|---|
| `assertEqual(a, b)` | `a == b` |
| `assertNotEqual(a, b)` | `a != b` |
| `assertTrue(x)` | `bool(x) is True` |
| `assertFalse(x)` | `bool(x) is False` |
| `assertIs(a, b)` | `a is b` |
| `assertIsNone(x)` | `x is None` |
| `assertIn(a, b)` | `a in b` |
| `assertIsInstance(a, b)` | `isinstance(a, b)` |
| `assertRaises(exc)` | Context manager for exception checking |
| `assertAlmostEqual(a, b)` | `round(a-b, 7) == 0` |
| `assertGreater(a, b)` | `a > b` |
| `assertRegex(text, regex)` | `re.search(regex, text)` |

### 28.2 `pytest` Framework

```python
# test_math.py
import pytest

def test_add():
    assert 2 + 3 == 5

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        1 / 0

# Parametrize -- run the same test with different inputs
@pytest.mark.parametrize("input,expected", [
    (1, 1),
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_square(input, expected):
    assert input ** 2 == expected

# Fixtures -- setup/teardown
@pytest.fixture
def database():
    db = connect_to_test_db()
    yield db              # test runs here
    db.close()            # teardown

def test_query(database):
    result = database.query("SELECT 1")
    assert result == 1

# Fixture with scope
@pytest.fixture(scope="module")     # once per module (not per test)
def expensive_resource():
    resource = create_resource()
    yield resource
    resource.cleanup()

# Temporary directory fixture (built-in)
def test_file_creation(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("hello")
    assert file.read_text() == "hello"
```

### 28.3 Mocking

```python
from unittest.mock import Mock, patch, MagicMock

# Basic Mock
mock = Mock()
mock.method(1, 2, 3)
mock.method.assert_called_once_with(1, 2, 3)
mock.method.call_count    # 1

# Mock return values
mock.method.return_value = 42
mock.method()   # 42

# Mock side effects
mock.method.side_effect = ValueError("boom")
mock.method()   # raises ValueError

mock.method.side_effect = [1, 2, 3]
mock.method()   # 1
mock.method()   # 2
mock.method()   # 3

# patch -- temporarily replace an object
# file: my_module.py
# import requests
# def fetch(url):
#     return requests.get(url).text

from unittest.mock import patch

@patch('my_module.requests.get')
def test_fetch(mock_get):
    mock_get.return_value.text = "mocked response"
    result = my_module.fetch("http://example.com")
    assert result == "mocked response"
    mock_get.assert_called_once_with("http://example.com")

# Context manager form
def test_fetch():
    with patch('my_module.requests.get') as mock_get:
        mock_get.return_value.text = "mocked"
        result = my_module.fetch("http://example.com")
        assert result == "mocked"

# MagicMock -- supports magic methods
mock = MagicMock()
mock.__len__.return_value = 5
len(mock)   # 5
mock[0]     # returns another MagicMock (auto-created)
```

### 28.4 Test Design Patterns

| Pattern | Description |
|---|---|
| **Arrange-Act-Assert (AAA)** | Setup → Execute → Verify |
| **Given-When-Then** | Preconditions → Action → Expected result (BDD) |
| **Test doubles** | Mock, Stub, Fake, Spy, Dummy |
| **Fixture** | Shared setup/teardown |
| **Parametrized tests** | Same test, different data |
| **Property-based testing** | Generate random inputs (Hypothesis library) |

```python
# AAA pattern
def test_user_login():
    # Arrange
    user = User(username="alice", password="secret")
    auth_service = AuthService()
    
    # Act
    result = auth_service.login(user.username, "secret")
    
    # Assert
    assert result.is_authenticated
    assert result.username == "alice"
```

---

# Part 6: Quick Reference

---

## 29. Built-in Functions Cheat Sheet

---

| Function | Description | Example |
|---|---|---|
| `abs(x)` | Absolute value | `abs(-5)` → `5` |
| `all(it)` | `True` if all elements truthy | `all([1, 2, 3])` → `True` |
| `any(it)` | `True` if any element truthy | `any([0, 0, 1])` → `True` |
| `bin(n)` | Integer to binary string | `bin(10)` → `'0b1010'` |
| `bool(x)` | Convert to boolean | `bool(0)` → `False` |
| `breakpoint()` | Enter debugger (3.7+) | `breakpoint()` |
| `callable(obj)` | Check if object is callable | `callable(len)` → `True` |
| `chr(n)` | Unicode code point to character | `chr(65)` → `'A'` |
| `classmethod(f)` | Convert to class method | `@classmethod` |
| `complex(r, i)` | Create complex number | `complex(3, 4)` → `(3+4j)` |
| `delattr(obj, name)` | Delete attribute | `delattr(obj, 'x')` |
| `dict()` | Create dictionary | `dict(a=1, b=2)` |
| `dir(obj)` | List attributes/methods | `dir([])` |
| `divmod(a, b)` | `(a // b, a % b)` | `divmod(7, 2)` → `(3, 1)` |
| `enumerate(it, start=0)` | Index + value iterator | `enumerate(['a','b'])` |
| `eval(expr)` | Evaluate string expression | `eval('2+3')` → `5` |
| `exec(code)` | Execute string as code | `exec('x = 1')` |
| `filter(f, it)` | Filter elements by predicate | `filter(bool, [0,1,2])` |
| `float(x)` | Convert to float | `float('3.14')` → `3.14` |
| `format(val, spec)` | Format a value | `format(3.14, '.1f')` → `'3.1'` |
| `frozenset(it)` | Create immutable set | `frozenset([1,2,3])` |
| `getattr(obj, name, default)` | Get attribute | `getattr(obj, 'x', 0)` |
| `globals()` | Global symbol table (dict) | `globals()['x']` |
| `hasattr(obj, name)` | Check attribute exists | `hasattr(obj, 'x')` |
| `hash(obj)` | Hash value | `hash('hello')` |
| `hex(n)` | Integer to hex string | `hex(255)` → `'0xff'` |
| `id(obj)` | Object identity | `id(x)` |
| `input(prompt)` | Read from stdin | `input('Name: ')` |
| `int(x, base=10)` | Convert to integer | `int('ff', 16)` → `255` |
| `isinstance(obj, cls)` | Type check (with inheritance) | `isinstance(1, int)` → `True` |
| `issubclass(cls, cls)` | Subclass check | `issubclass(bool, int)` → `True` |
| `iter(obj)` | Get iterator | `iter([1,2,3])` |
| `len(obj)` | Length | `len([1,2,3])` → `3` |
| `list(it)` | Create list | `list(range(3))` → `[0,1,2]` |
| `locals()` | Local symbol table (dict) | `locals()` |
| `map(f, *its)` | Apply function to elements | `map(str, [1,2])` |
| `max(it)` / `max(a,b,...)` | Maximum value | `max([3,1,2])` → `3` |
| `min(it)` / `min(a,b,...)` | Minimum value | `min([3,1,2])` → `1` |
| `next(it, default)` | Next item from iterator | `next(iter([1,2]))` → `1` |
| `oct(n)` | Integer to octal string | `oct(8)` → `'0o10'` |
| `open(file, mode)` | Open file | `open('f.txt', 'r')` |
| `ord(c)` | Character to Unicode code point | `ord('A')` → `65` |
| `pow(b, e, mod=None)` | Power (optional modulo) | `pow(2, 10, 100)` → `24` |
| `print(*args)` | Print to stdout | `print('hello')` |
| `property(fget)` | Managed attribute | `@property` |
| `range(start, stop, step)` | Integer range | `range(0, 10, 2)` |
| `repr(obj)` | Developer string | `repr('hi')` → `"'hi'"` |
| `reversed(seq)` | Reverse iterator | `reversed([1,2,3])` |
| `round(n, digits=0)` | Round to digits | `round(3.14, 1)` → `3.1` |
| `set(it)` | Create set | `set([1,1,2])` → `{1, 2}` |
| `setattr(obj, name, val)` | Set attribute | `setattr(obj, 'x', 1)` |
| `slice(start, stop, step)` | Slice object | `s = slice(1, 5, 2)` |
| `sorted(it, key, reverse)` | Sorted list | `sorted([3,1,2])` → `[1,2,3]` |
| `staticmethod(f)` | Convert to static method | `@staticmethod` |
| `str(obj)` | Convert to string | `str(42)` → `'42'` |
| `sum(it, start=0)` | Sum of elements | `sum([1,2,3])` → `6` |
| `super()` | Proxy to parent class | `super().__init__()` |
| `tuple(it)` | Create tuple | `tuple([1,2,3])` → `(1,2,3)` |
| `type(obj)` | Object's type | `type(42)` → `<class 'int'>` |
| `vars(obj)` | `__dict__` of object | `vars(obj)` |
| `zip(*its)` | Parallel iterator | `zip([1,2], ['a','b'])` |

---

## 30. Standard Library Highlights

---

### 30.1 File System & OS

| Module | Purpose | Key Functions/Classes |
|---|---|---|
| `os` | OS interface | `os.getcwd()`, `os.listdir()`, `os.environ`, `os.path.join()`, `os.makedirs()` |
| `os.path` | Path manipulation (legacy) | `exists()`, `join()`, `split()`, `basename()`, `dirname()`, `isfile()`, `isdir()` |
| `pathlib` | OOP path manipulation (preferred) | `Path.cwd()`, `Path.home()`, `p.exists()`, `p.read_text()`, `p.glob('*.py')` |
| `shutil` | High-level file operations | `copy2()`, `copytree()`, `rmtree()`, `move()`, `make_archive()` |
| `glob` | File pattern matching | `glob.glob('*.py')`, `glob.iglob('**/*.py', recursive=True)` |
| `tempfile` | Temporary files/directories | `NamedTemporaryFile()`, `mkdtemp()`, `TemporaryDirectory()` |

```python
from pathlib import Path

p = Path('data') / 'output' / 'results.csv'
p.parent            # PosixPath('data/output')
p.name              # 'results.csv'
p.stem              # 'results'
p.suffix            # '.csv'
p.exists()          # True/False
p.read_text()       # read entire file as string
p.write_text('...')  # write string to file
list(Path('.').glob('**/*.py'))   # recursive file search
p.mkdir(parents=True, exist_ok=True)  # create directory tree
```

### 30.2 Data Serialization

| Module | Purpose | Key Functions |
|---|---|---|
| `json` | JSON encoding/decoding | `dumps()`, `loads()`, `dump()`, `load()` |
| `csv` | CSV reading/writing | `reader()`, `writer()`, `DictReader()`, `DictWriter()` |
| `pickle` | Python object serialization | `dumps()`, `loads()`, `dump()`, `load()` |

```python
import json

# JSON
data = {'name': 'Alice', 'scores': [90, 85, 92]}
json_str = json.dumps(data, indent=2)     # to string
parsed = json.loads(json_str)              # from string

with open('data.json', 'w') as f:
    json.dump(data, f, indent=2)           # to file
with open('data.json') as f:
    data = json.load(f)                    # from file

import csv

# CSV
with open('data.csv', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row['name'], row['age'])

with open('output.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'age'])
    writer.writeheader()
    writer.writerow({'name': 'Alice', 'age': 30})
```

### 30.3 Date & Time

```python
from datetime import datetime, date, timedelta, timezone

now = datetime.now()                      # local time
utc = datetime.now(timezone.utc)          # UTC time
d = date(2025, 3, 15)                     # specific date
dt = datetime(2025, 3, 15, 10, 30, 0)    # specific datetime

# Formatting
dt.strftime('%Y-%m-%d %H:%M:%S')         # '2025-03-15 10:30:00'
dt.isoformat()                            # '2025-03-15T10:30:00'

# Parsing
datetime.strptime('2025-03-15', '%Y-%m-%d')

# Arithmetic
tomorrow = date.today() + timedelta(days=1)
diff = datetime(2025, 12, 31) - datetime(2025, 1, 1)
diff.days     # 364
```

### 30.4 Logging

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log',
)

logger = logging.getLogger(__name__)

logger.debug("Detailed debugging info")
logger.info("Informational message")
logger.warning("Warning message")
logger.error("Error occurred")
logger.critical("Critical failure")

# Log levels: DEBUG < INFO < WARNING < ERROR < CRITICAL
```

### 30.5 Regular Expressions

```python
import re

# See Section 3.5 for full reference
pattern = re.compile(r'\b\w+@\w+\.\w+\b')
emails = pattern.findall(text)
```

### 30.6 Subprocess

```python
import subprocess

# Run a command and capture output
result = subprocess.run(
    ['ls', '-la'],
    capture_output=True,
    text=True,            # return str instead of bytes
    check=True,           # raise CalledProcessError on non-zero exit
)
print(result.stdout)
print(result.returncode)  # 0

# With shell=True (be careful with untrusted input)
result = subprocess.run('echo hello | wc -w', shell=True, capture_output=True, text=True)
```

### 30.7 `enum` Module

```python
from enum import Enum, auto, IntEnum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

Color.RED              # Color.RED
Color.RED.name         # 'RED'
Color.RED.value        # 1
Color(1)               # Color.RED
Color['RED']           # Color.RED
list(Color)            # [Color.RED, Color.GREEN, Color.BLUE]

class Direction(Enum):
    NORTH = auto()     # auto-assigns 1
    SOUTH = auto()     # auto-assigns 2
    EAST = auto()      # auto-assigns 3
    WEST = auto()      # auto-assigns 4

class Status(IntEnum):     # can be compared with ints
    OK = 200
    NOT_FOUND = 404

Status.OK == 200           # True (because IntEnum)
```

### 30.8 `argparse` for CLI

```python
import argparse

parser = argparse.ArgumentParser(description='Process some data')
parser.add_argument('filename', help='Input file')
parser.add_argument('-o', '--output', default='out.txt', help='Output file')
parser.add_argument('-n', '--count', type=int, default=10, help='Number of items')
parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose')

args = parser.parse_args()
print(args.filename, args.output, args.count, args.verbose)

# Usage: python script.py data.csv -o results.txt -n 20 -v
```

### 30.9 Module Quick Reference Table

| Module | Category | One-Line Description |
|---|---|---|
| `os` | System | OS interface (env vars, process, paths) |
| `sys` | System | Interpreter config (argv, path, stdin/stdout, exit) |
| `pathlib` | File I/O | Object-oriented file system paths |
| `json` | Serialization | JSON encoding and decoding |
| `csv` | Serialization | CSV file reading and writing |
| `pickle` | Serialization | Python object serialization (binary) |
| `logging` | Diagnostics | Flexible logging framework |
| `argparse` | CLI | Command-line argument parsing |
| `datetime` | Date/Time | Date and time manipulation |
| `enum` | Data Types | Enumeration support |
| `dataclasses` | Data Types | Auto-generate class boilerplate |
| `typing` | Type Hints | Type annotation support |
| `collections` | Data Structures | Specialized container types |
| `itertools` | Iteration | Iterator building blocks |
| `functools` | Functions | Higher-order functions and caching |
| `re` | Text | Regular expressions |
| `subprocess` | System | Spawn external processes |
| `threading` | Concurrency | Thread-based parallelism |
| `multiprocessing` | Concurrency | Process-based parallelism |
| `asyncio` | Concurrency | Async I/O framework |
| `concurrent.futures` | Concurrency | High-level parallel execution |
| `unittest` | Testing | Unit testing framework |
| `copy` | Utilities | Shallow and deep copy operations |
| `math` | Math | Mathematical functions (sqrt, sin, log, pi, e) |
| `random` | Math | Random number generation |
| `statistics` | Math | Statistical functions (mean, median, stdev) |
| `hashlib` | Security | Secure hash functions (SHA, MD5) |
| `secrets` | Security | Cryptographically strong random numbers |
| `sqlite3` | Database | SQLite database interface |
| `socket` | Networking | Low-level networking |
| `http.server` | Networking | Simple HTTP server |
| `urllib` | Networking | URL handling and HTTP client |
| `pdb` | Debugging | Interactive debugger |
| `traceback` | Debugging | Print/format stack traces |
| `gc` | Memory | Garbage collector interface |
| `weakref` | Memory | Weak reference support |
| `abc` | OOP | Abstract base classes |
| `contextlib` | Utilities | Context manager utilities |
| `operator` | Functions | Function versions of operators |
| `textwrap` | Text | Text wrapping and filling |
| `string` | Text | String constants and templates |

---

*End of Python Fundamentals reference. This guide is designed to be a comprehensive companion to the DSA Fundamentals, LeetCode Patterns, and CS Fundamentals guides.*
