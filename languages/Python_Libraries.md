# Python Libraries -- Comprehensive Reference

> Last reviewed: 2026-11 · Versions assumed: Python 3.12+, NumPy 2.x (examples tested on 2.5), SciPy 1.18, matplotlib 3.11, Numba 0.68, CuPy 14 / AMD CuPy (ROCm 7.x), pydantic 2.14, click 8 / typer, httpx 0.28

> A thorough reference covering NumPy (fundamentals, advanced operations, vectorization exercises, and the GPU array ecosystem: CuPy, Numba, DLPack, array API), a pandas quick reference (the canonical deep dive is [Pandas.md](Pandas.md)), SciPy, matplotlib, pydantic, CLI and HTTP libraries, and PyQt. Each section includes conceptual explanations, comparison tables, code examples, common pitfalls, and interview questions with detailed answers. Complements the *Python Fundamentals*, *DSA Fundamentals*, and *CS Fundamentals* guides.
>
> Code blocks run with NumPy alone unless the first line says `# Requires: ...` (SciPy, Numba, CuPy, PyTorch, ml_dtypes, pydantic, typer, httpx) or `# fragment`.

---

## Table of Contents

### Part 1: NumPy

1. [ndarray Fundamentals](#1-ndarray-fundamentals)
2. [Indexing and Slicing](#2-indexing-and-slicing)
3. [Reshaping and Manipulating](#3-reshaping-and-manipulating)
4. [Broadcasting](#4-broadcasting)
5. [Vectorized Operations and ufuncs](#5-vectorized-operations-and-ufuncs)
6. [Linear Algebra](#6-linear-algebra)
7. [Random Module](#7-random-module)
8. [Performance and Memory](#8-performance-and-memory)
9. [NumPy Common Pitfalls and Interview Questions](#9-numpy-common-pitfalls-and-interview-questions)
10. [Advanced NumPy Operations](#10-advanced-numpy-operations)
11. [NumPy Vectorization Exercise Set](#11-numpy-vectorization-exercise-set)
12. [GPU Array Ecosystem and Zero-Copy Interop](#12-gpu-array-ecosystem-and-zero-copy-interop)

### Part 2: Pandas

13. [Pandas Quick Reference (Summary of Pandas.md)](#13-pandas-quick-reference-summary-of-pandasmd)

### Part 3: SciPy, Plotting, and Tooling Libraries

14. [SciPy Essentials](#14-scipy-essentials)
15. [matplotlib Essentials](#15-matplotlib-essentials)
16. [pydantic v2 -- Data Validation](#16-pydantic-v2----data-validation)
17. [Command-Line Interfaces: click and typer](#17-command-line-interfaces-click-and-typer)
18. [HTTP Clients: requests and httpx](#18-http-clients-requests-and-httpx)

### Part 4: PyQt

19. [Qt Architecture and Core Concepts](#19-qt-architecture-and-core-concepts)
20. [Widgets](#20-widgets)
21. [Layouts](#21-layouts)
22. [Signals and Slots](#22-signals-and-slots)
23. [Dialogs and Menus](#23-dialogs-and-menus)
24. [Model/View Architecture](#24-modelview-architecture)
25. [Custom Widgets and Painting](#25-custom-widgets-and-painting)
26. [Threading in Qt](#26-threading-in-qt)
27. [Styling](#27-styling)
28. [PyQt Common Patterns and Interview Questions](#28-pyqt-common-patterns-and-interview-questions)

---

# Part 1: NumPy

---

# 1. ndarray Fundamentals

---

## 1.1 What Is NumPy?

NumPy (Numerical Python) is the foundational library for numerical computing in Python. Its core object is the **ndarray** -- a fixed-size, homogeneous, multidimensional array stored in a contiguous block of memory. This design enables:

- Vectorized operations (no Python-level loops)
- Cache-friendly memory access patterns
- Direct interop with C/C++/Fortran libraries (BLAS, LAPACK)

```python
import numpy as np
```

## 1.2 Array Creation

| Function | Description | Example |
|---|---|---|
| `np.array(obj)` | Create from list/tuple | `np.array([1, 2, 3])` |
| `np.zeros(shape)` | All zeros | `np.zeros((3, 4))` |
| `np.ones(shape)` | All ones | `np.ones((2, 3))` |
| `np.full(shape, val)` | Fill with value | `np.full((2, 2), 7)` |
| `np.empty(shape)` | Uninitialized (fast) | `np.empty((3, 3))` |
| `np.arange(start, stop, step)` | Evenly spaced (by step) | `np.arange(0, 10, 2)` → `[0, 2, 4, 6, 8]` |
| `np.linspace(start, stop, num)` | Evenly spaced (by count) | `np.linspace(0, 1, 5)` → `[0, 0.25, 0.5, 0.75, 1.0]` |
| `np.eye(n)` | Identity matrix | `np.eye(3)` |
| `np.diag(v)` | Diagonal matrix from vector | `np.diag([1, 2, 3])` |
| `np.zeros_like(a)` | Zeros matching shape/dtype of `a` | `np.zeros_like(existing)` |
| `np.fromfunction(fn, shape)` | From function of indices | `np.fromfunction(lambda i, j: i + j, (3, 3))` |

```python
a = np.array([[1, 2, 3],
              [4, 5, 6]])

print(a)
# [[1 2 3]
#  [4 5 6]]
```

## 1.3 ndarray Attributes

| Attribute | Description | Example (for 2x3 int64 array) |
|---|---|---|
| `ndim` | Number of dimensions (axes) | `2` |
| `shape` | Tuple of dimension sizes | `(2, 3)` |
| `size` | Total number of elements | `6` |
| `dtype` | Data type of elements | `dtype('int64')` |
| `itemsize` | Bytes per element | `8` |
| `nbytes` | Total bytes (`size * itemsize`) | `48` |
| `strides` | Bytes to step in each dimension | `(24, 8)` |
| `flags` | Memory layout info | C_CONTIGUOUS, F_CONTIGUOUS, etc. |

```python
a = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float64)

print(a.ndim)      # 2
print(a.shape)     # (2, 3)
print(a.size)      # 6
print(a.dtype)     # float64
print(a.itemsize)  # 8
print(a.nbytes)    # 48
print(a.strides)   # (24, 8) -- 24 bytes to next row, 8 bytes to next column
```

## 1.4 The dtype System

NumPy provides fixed-size types that map directly to C types for performance:

| Category | Types | Notes |
|---|---|---|
| **Integers** | `int8`, `int16`, `int32`, `int64` | Signed; overflow wraps silently |
| **Unsigned** | `uint8`, `uint16`, `uint32`, `uint64` | No negatives |
| **Floats** | `float16`, `float32`, `float64` | `float64` is default for floats |
| **Complex** | `complex64`, `complex128` | Real + imaginary |
| **Boolean** | `bool_` | 1 byte per element |
| **Strings** | `U<n>` (Unicode), `S<n>` (bytes) | Fixed-length |
| **Object** | `object` | Arbitrary Python objects (loses performance benefits) |

```python
a = np.array([1, 2, 3])           # default int64 (on Windows, int32 only with NumPy < 2.0)
b = np.array([1.0, 2.0, 3.0])     # default float64
c = np.array([1, 2], dtype=np.float32)

d = a.astype(np.float64)          # explicit cast (always returns a copy)
print(d.dtype)                     # float64
```

**Type promotion rules** (upcasting): when mixing dtypes, NumPy promotes to the "largest" type:

```python
np.array([1, 2]) + np.array([1.5, 2.5])  # int64 + float64 → float64
np.array([True, False]) + np.array([1, 2])  # bool + int64 → int64
```

## 1.5 Memory Layout and Strides

ndarray data is stored in a **flat, contiguous buffer**. The `strides` tuple tells NumPy how many bytes to skip to move along each axis.

```
For a 2x3 float64 array (8 bytes per element):

Memory:  [ 1.0 | 2.0 | 3.0 | 4.0 | 5.0 | 6.0 ]
          row 0              row 1

Row-major (C order):     strides = (24, 8)   -- 3*8=24 to next row, 8 to next col
Column-major (F order):  strides = (8, 16)   -- 8 to next row, 2*8=16 to next col
```

| Order | Name | Strides | Used By |
|---|---|---|---|
| `C` (default) | Row-major | Rightmost index varies fastest | C, C++, Python |
| `F` | Column-major | Leftmost index varies fastest | Fortran, MATLAB, R |

```python
c_arr = np.array([[1, 2, 3], [4, 5, 6]], order='C')
f_arr = np.array([[1, 2, 3], [4, 5, 6]], order='F')

print(c_arr.strides)  # (24, 8)
print(f_arr.strides)  # (8, 16)

print(c_arr.flags['C_CONTIGUOUS'])  # True
print(f_arr.flags['F_CONTIGUOUS'])  # True
```

Strides enable **zero-copy views**: slicing, transposing, and reshaping often just create new strides without copying data.

---

# 2. Indexing and Slicing

---

## 2.1 Basic Indexing (Returns Views)

Basic indexing uses integers and slices. It **returns a view** -- modifications to the result affect the original array.

```python
a = np.arange(12).reshape(3, 4)
# [[ 0,  1,  2,  3],
#  [ 4,  5,  6,  7],
#  [ 8,  9, 10, 11]]

a[1, 2]       # 6         -- single element
a[0]          # [0, 1, 2, 3]  -- entire row (view)
a[:, 1]       # [1, 5, 9]     -- entire column (view)
a[0:2, 1:3]   # [[1, 2], [5, 6]]  -- subarray (view)
a[::2, ::2]   # [[ 0,  2], [ 8, 10]]  -- every other row and col
```

**View semantics -- critical to understand:**

```python
a = np.array([10, 20, 30, 40, 50])
b = a[1:4]       # b is a VIEW of a
b[0] = 999       # modifying b also modifies a
print(a)          # [10, 999, 30, 40, 50]
```

## 2.2 Fancy Indexing (Returns Copies)

Fancy indexing uses **integer arrays** or **lists** as indices. It **always returns a copy**.

```python
a = np.arange(12).reshape(3, 4)

a[[0, 2]]             # rows 0 and 2 → [[0,1,2,3], [8,9,10,11]]
a[[0, 1, 2], [1, 2, 3]]  # elements (0,1), (1,2), (2,3) → [1, 6, 11]
a[np.ix_([0, 2], [1, 3])]  # submatrix rows [0,2] x cols [1,3] → [[1,3],[9,11]]
```

## 2.3 Boolean Indexing (Returns Copies)

Uses a boolean array as a mask. Returns a **1-D copy** of matching elements.

```python
a = np.array([10, 20, 30, 40, 50])
mask = a > 25
print(mask)       # [False, False,  True,  True,  True]
print(a[mask])    # [30, 40, 50]

a[a < 30] = 0     # in-place modification via boolean mask
print(a)           # [ 0,  0, 30, 40, 50]
```

## 2.4 Indexing Summary

| Method | Syntax | Returns | Copy or View? |
|---|---|---|---|
| Single element | `a[i, j]` | Scalar | N/A (scalar) |
| Slice | `a[i:j]`, `a[:, k]` | ndarray | **View** |
| Integer array | `a[[0, 2]]` | ndarray | **Copy** |
| Boolean mask | `a[a > 5]` | ndarray (1-D) | **Copy** |

## 2.5 np.where and np.select

`np.where` is a vectorized ternary operator:

```python
a = np.array([1, -2, 3, -4, 5])

np.where(a > 0, a, 0)      # [1, 0, 3, 0, 5]  -- replace negatives with 0
np.where(a > 0)             # (array([0, 2, 4]),)  -- indices where True
```

`np.select` handles multiple conditions:

```python
a = np.array([15, 25, 35, 45, 55])

conditions = [a < 20, a < 40, a >= 40]
choices     = ["low", "mid", "high"]

np.select(conditions, choices, default="unknown")
# ['low', 'mid', 'mid', 'high', 'high']
```

---

# 3. Reshaping and Manipulating

---

## 3.1 Reshaping

| Function | Description | Copy? |
|---|---|---|
| `a.reshape(shape)` | New shape, same data | View if possible, copy otherwise |
| `a.ravel()` | Flatten to 1-D | View if possible |
| `a.flatten()` | Flatten to 1-D | **Always a copy** |
| `a.T` / `a.transpose()` | Transpose | View (new strides) |
| `a.squeeze()` | Remove axes of length 1 | View |
| `np.expand_dims(a, axis)` | Add axis of length 1 | View |

```python
a = np.arange(12)

b = a.reshape(3, 4)     # view (if contiguous)
c = a.reshape(2, -1)    # -1 infers the dimension → shape (2, 6)

print(b)
# [[ 0,  1,  2,  3],
#  [ 4,  5,  6,  7],
#  [ 8,  9, 10, 11]]
```

**ravel vs flatten:**

```python
a = np.array([[1, 2], [3, 4]])

r = a.ravel()     # view when possible -- changes to r affect a
f = a.flatten()   # always a copy -- independent of a

r[0] = 99
print(a[0, 0])    # 99  (ravel returned a view)
```

## 3.2 Transpose

```python
a = np.arange(6).reshape(2, 3)
# [[0, 1, 2],
#  [3, 4, 5]]

print(a.T)
# [[0, 3],
#  [1, 4],
#  [2, 5]]

print(a.T.strides)   # (8, 24) -- swapped from (24, 8); no data copy
```

For higher dimensions, `transpose` accepts an axis permutation:

```python
a = np.zeros((2, 3, 4))
b = a.transpose(1, 2, 0)   # shape becomes (3, 4, 2)
```

## 3.3 Concatenation and Splitting

| Function | Description |
|---|---|
| `np.concatenate([a, b], axis)` | Join along existing axis |
| `np.vstack([a, b])` | Stack vertically (row-wise) = `concatenate` axis=0 |
| `np.hstack([a, b])` | Stack horizontally (column-wise) = `concatenate` axis=1 |
| `np.stack([a, b], axis)` | Join along **new** axis |
| `np.split(a, indices, axis)` | Split into sub-arrays |
| `np.array_split(a, n, axis)` | Split into `n` (allows unequal sizes) |

```python
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6]])

np.vstack([a, b])            # [[1,2],[3,4],[5,6]]  shape (3,2)
np.hstack([a, b.T])          # [[1,2,5],[3,4,6]]    shape (2,3)
np.concatenate([a, b], axis=0)  # same as vstack

c = np.stack([a[0], a[1]])   # [[1,2],[3,4]]  new axis=0
```

## 3.4 np.newaxis and expand_dims

Both add a length-1 axis (useful for broadcasting):

```python
a = np.array([1, 2, 3])    # shape (3,)

a[np.newaxis, :]   # shape (1, 3) -- row vector
a[:, np.newaxis]   # shape (3, 1) -- column vector

np.expand_dims(a, axis=0)  # shape (1, 3)
np.expand_dims(a, axis=1)  # shape (3, 1)
```

---

# 4. Broadcasting

---

## 4.1 What Is Broadcasting?

Broadcasting is NumPy's mechanism for performing element-wise operations on arrays with **different shapes** without explicitly copying data. It follows strict rules to determine compatibility.

## 4.2 Broadcasting Rules

1. **Align shapes from the right** (trailing dimensions).
2. Dimensions are compatible if they are **equal** or one of them is **1**.
3. If one array has fewer dimensions, it is padded with 1s on the left.
4. Size-1 dimensions are **stretched** to match the other array's size.

```
Shape alignment examples:

  A:      (3, 4)
  B:         (4,)  → treated as (1, 4) → broadcast to (3, 4)  ✓

  A:   (2, 3, 4)
  B:      (3, 1)  → treated as (1, 3, 1) → broadcast to (2, 3, 4)  ✓

  A:      (3, 4)
  B:      (3,)    → treated as (1, 3) → dimensions: 4 vs 3 → INCOMPATIBLE  ✗
```

## 4.3 Compatibility Table

| Shape A | Shape B | Result Shape | Compatible? |
|---|---|---|---|
| `(5,)` | `(5,)` | `(5,)` | Yes |
| `(5,)` | `(1,)` | `(5,)` | Yes |
| `(3, 4)` | `(4,)` | `(3, 4)` | Yes |
| `(3, 4)` | `(3, 1)` | `(3, 4)` | Yes |
| `(3, 4)` | `(3,)` | Error | **No** (trailing: 4 vs 3) |
| `(2, 1, 4)` | `(3, 4)` | `(2, 3, 4)` | Yes |
| `(2, 3)` | `(3, 2)` | Error | **No** (2 vs 3 and 3 vs 2) |
| `(15, 3, 5)` | `(15, 1, 5)` | `(15, 3, 5)` | Yes |

## 4.4 Common Broadcasting Patterns

```python
a = np.arange(12).reshape(4, 3)  # shape (4, 3)

a + 10                            # scalar broadcast to (4, 3)

row_means = a.mean(axis=1, keepdims=True)  # shape (4, 1)
a - row_means                     # center each row: (4, 3) - (4, 1) → (4, 3)

col = np.array([1, 2, 3, 4])[:, np.newaxis]  # shape (4, 1)
row = np.array([10, 20, 30])                  # shape (3,)
col + row   # outer addition: shape (4, 3)
# [[11, 21, 31],
#  [12, 22, 32],
#  [13, 23, 33],
#  [14, 24, 34]]
```

**Outer product via broadcasting:**

```python
x = np.array([1, 2, 3])
y = np.array([10, 20])

x[:, np.newaxis] * y[np.newaxis, :]   # shape (3, 2)
# [[10, 20],
#  [20, 40],
#  [30, 60]]
```

---

# 5. Vectorized Operations and ufuncs

---

## 5.1 Element-Wise Arithmetic

All standard operators are element-wise on ndarrays:

```python
a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])

a + b    # [11, 22, 33, 44]
a * b    # [10, 40, 90, 160]
a ** 2   # [ 1,  4,  9, 16]
a / b    # [0.1, 0.1, 0.1, 0.1]
a // 2   # [0, 1, 1, 2]
a % 2    # [1, 0, 1, 0]
```

Each operator maps to a **ufunc** (universal function):

| Operator | ufunc | Description |
|---|---|---|
| `+` | `np.add` | Addition |
| `-` | `np.subtract` | Subtraction |
| `*` | `np.multiply` | Multiplication |
| `/` | `np.true_divide` | Division |
| `//` | `np.floor_divide` | Floor division |
| `**` | `np.power` | Exponentiation |
| `%` | `np.mod` | Modulus |
| `>`, `<`, `==` | `np.greater`, `np.less`, `np.equal` | Comparison (returns bool array) |

## 5.2 Aggregation Functions

| Function | Description | Notes |
|---|---|---|
| `np.sum(a, axis)` | Sum | `axis=None` sums all elements |
| `np.prod(a, axis)` | Product | |
| `np.mean(a, axis)` | Arithmetic mean | |
| `np.std(a, axis)` | Standard deviation | `ddof=0` by default (population) |
| `np.var(a, axis)` | Variance | |
| `np.min(a, axis)` | Minimum | |
| `np.max(a, axis)` | Maximum | |
| `np.argmin(a, axis)` | Index of minimum | |
| `np.argmax(a, axis)` | Index of maximum | |
| `np.cumsum(a, axis)` | Cumulative sum | |
| `np.cumprod(a, axis)` | Cumulative product | |
| `np.any(a, axis)` | True if any element is truthy | |
| `np.all(a, axis)` | True if all elements are truthy | |

**Understanding the `axis` parameter:**

```python
a = np.array([[1, 2, 3],
              [4, 5, 6]])   # shape (2, 3)

np.sum(a)           # 21        -- sum everything
np.sum(a, axis=0)   # [5, 7, 9] -- collapse rows → one row (sum down columns)
np.sum(a, axis=1)   # [6, 15]   -- collapse columns → one column (sum across rows)
```

The `axis` parameter specifies which axis is **collapsed** (reduced). The result has that axis removed.

```
axis=0: collapse along rows     (2, 3) → (3,)    result has shape of remaining axes
axis=1: collapse along columns  (2, 3) → (2,)
```

Use `keepdims=True` to preserve the collapsed axis as size 1 (useful for broadcasting):

```python
np.sum(a, axis=1, keepdims=True)   # [[6], [15]]  shape (2, 1)
```

## 5.3 Math Functions (ufuncs)

| Function | Description |
|---|---|
| `np.sqrt(a)` | Square root |
| `np.exp(a)` | e^x |
| `np.log(a)` / `np.log2` / `np.log10` | Logarithms |
| `np.sin`, `np.cos`, `np.tan` | Trigonometric |
| `np.abs(a)` | Absolute value |
| `np.clip(a, lo, hi)` | Clamp values to range |
| `np.round(a, decimals)` | Round |
| `np.sign(a)` | Sign (-1, 0, +1) |
| `np.floor`, `np.ceil` | Floor / ceiling |

## 5.4 np.apply_along_axis

Applies a **Python function** along one axis. Useful for non-vectorized functions but much slower than true vectorized operations.

```python
a = np.array([[1, 2, 3],
              [4, 5, 6]])

def my_func(row):
    return row[0] + row[-1]

np.apply_along_axis(my_func, axis=1, arr=a)   # [4, 10]
```

## 5.5 Performance: Vectorized vs Python Loops

```python
import time

n = 1_000_000
a = np.random.rand(n)
b = np.random.rand(n)

# Python loop
start = time.time()
c = [a[i] + b[i] for i in range(n)]
loop_time = time.time() - start

# Vectorized
start = time.time()
c = a + b
vec_time = time.time() - start

# Vectorized is typically 50-100x faster
```

| Approach | Relative Speed | Why |
|---|---|---|
| Python `for` loop | 1x (baseline) | Per-element Python overhead, type checking |
| `np.vectorize` | ~1-2x | Syntactic sugar; still Python loop underneath |
| True vectorized op | ~50-100x | C loop, no Python overhead, cache-friendly |

---

# 6. Linear Algebra

---

## 6.1 Matrix Multiplication

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

A @ B              # preferred syntax (Python 3.5+)
np.dot(A, B)       # equivalent for 2-D arrays
np.matmul(A, B)    # equivalent for 2-D arrays

# All produce:
# [[19, 22],
#  [43, 50]]
```

**Key distinction** -- `np.dot` vs `@` vs `*`:

| Operation | Syntax | Description |
|---|---|---|
| Element-wise multiply | `A * B` | `[[5,12],[21,32]]` |
| Matrix multiply | `A @ B` | `[[19,22],[43,50]]` |
| Dot product (1-D) | `np.dot(a, b)` | Scalar result |
| Outer product | `np.outer(a, b)` | Matrix result |

## 6.2 np.linalg Module

| Function | Description | Example |
|---|---|---|
| `np.linalg.inv(A)` | Matrix inverse | A^(-1) |
| `np.linalg.det(A)` | Determinant | Scalar |
| `np.linalg.eig(A)` | Eigenvalues and eigenvectors | `(values, vectors)` |
| `np.linalg.eigh(A)` | Eigendecomposition (symmetric) | Faster, numerically stable |
| `np.linalg.svd(A)` | Singular Value Decomposition | `(U, S, Vt)` |
| `np.linalg.solve(A, b)` | Solve Ax = b | More stable than `inv(A) @ b` |
| `np.linalg.norm(a, ord)` | Vector/matrix norm | `ord=2` (default), `ord=1`, `ord=np.inf` |
| `np.linalg.matrix_rank(A)` | Rank | Integer |
| `np.linalg.qr(A)` | QR decomposition | `(Q, R)` |
| `np.linalg.cholesky(A)` | Cholesky decomposition | Lower triangular `L` where A = L @ L.T |
| `np.trace(A)` | Sum of diagonal elements | Scalar |

```python
A = np.array([[2, 1], [1, 3]])
b = np.array([5, 7])

x = np.linalg.solve(A, b)   # Ax = b → x = [1.6, 1.8]
print(A @ x)                 # [5., 7.] -- verifies solution

vals, vecs = np.linalg.eig(A)
print(vals)   # eigenvalues
print(vecs)   # eigenvectors (columns)

U, S, Vt = np.linalg.svd(A)
# A ≈ U @ np.diag(S) @ Vt
```

## 6.3 Norms

| Norm | `ord` | Formula (vector) | Formula (matrix) |
|---|---|---|---|
| L1 | `1` | Σ\|x_i\| | max column sum |
| L2 (Euclidean) | `2` (default) | √(Σx_i²) | largest singular value |
| L∞ | `np.inf` | max\|x_i\| | max row sum |
| Frobenius | `'fro'` | N/A | √(ΣΣa_ij²) |

```python
v = np.array([3, -4])

np.linalg.norm(v)          # 5.0 (L2)
np.linalg.norm(v, ord=1)   # 7.0 (L1)
np.linalg.norm(v, ord=np.inf)  # 4.0 (L∞)
```

---

# 7. Random Module

---

## 7.1 Modern API (Recommended)

NumPy's modern random API uses `Generator` objects via `np.random.default_rng()`. This replaces the legacy `np.random.rand()` style.

```python
rng = np.random.default_rng(seed=42)
```

## 7.2 Common Functions

| Method | Description | Example |
|---|---|---|
| `rng.random(shape)` | Uniform [0, 1) | `rng.random((3, 4))` |
| `rng.integers(lo, hi, size)` | Random ints in [lo, hi) | `rng.integers(0, 10, size=5)` |
| `rng.normal(loc, scale, size)` | Gaussian distribution | `rng.normal(0, 1, size=1000)` |
| `rng.uniform(lo, hi, size)` | Uniform [lo, hi) | `rng.uniform(-1, 1, size=5)` |
| `rng.choice(a, size, replace, p)` | Random sample from array | `rng.choice([1,2,3], size=2)` |
| `rng.shuffle(a)` | In-place shuffle | Modifies `a` |
| `rng.permutation(a)` | Shuffled copy | Returns new array |
| `rng.binomial(n, p, size)` | Binomial distribution | |
| `rng.poisson(lam, size)` | Poisson distribution | |
| `rng.exponential(scale, size)` | Exponential distribution | |

```python
rng = np.random.default_rng(42)

data = rng.normal(loc=100, scale=15, size=1000)  # IQ-like distribution
print(data.mean())   # ≈ 100
print(data.std())    # ≈ 15

sample = rng.choice(np.arange(100), size=10, replace=False)  # 10 unique from 0-99
```

## 7.3 Legacy vs Modern API

| Legacy (avoid) | Modern (prefer) | Notes |
|---|---|---|
| `np.random.seed(42)` | `rng = np.random.default_rng(42)` | Global state vs local |
| `np.random.rand(3, 4)` | `rng.random((3, 4))` | Uniform [0,1) |
| `np.random.randn(3, 4)` | `rng.standard_normal((3, 4))` | Standard normal |
| `np.random.randint(0, 10, 5)` | `rng.integers(0, 10, size=5)` | Random integers |
| `np.random.shuffle(a)` | `rng.shuffle(a)` | In-place |

The legacy API uses **global state**, making reproducibility fragile in multi-threaded code. The modern API is **instance-based** and thread-safe.

---

# 8. Performance and Memory

---

## 8.1 Why NumPy Is Fast

1. **Contiguous memory**: data sits in a single block; CPU caches are utilized efficiently.
2. **C loops**: operations run in compiled C/Fortran, not interpreted Python.
3. **No per-element type checks**: homogeneous dtype means no Python object overhead.
4. **BLAS/LAPACK**: linear algebra operations call optimized vendor libraries (OpenBLAS, MKL, etc.).

## 8.2 Memory Efficiency

```python
import sys

py_list = list(range(1000))
np_arr  = np.arange(1000, dtype=np.int64)

sys.getsizeof(py_list)    # ~8056 bytes (pointers + object overhead)
np_arr.nbytes              # 8000 bytes (raw data, no per-element overhead)
```

## 8.3 np.vectorize -- A Common Misconception

`np.vectorize` does **not** produce true vectorized code. It is syntactic sugar for a Python loop and provides **no performance benefit**.

```python
def my_func(x):
    return x ** 2 + 1

vfunc = np.vectorize(my_func)
result = vfunc(np.arange(1000))   # still a Python loop internally
```

Use it for convenience (broadcasting support) but never for performance.

## 8.4 Structured Arrays

Arrays where each element is a record (like a C struct):

```python
dt = np.dtype([('name', 'U10'), ('age', 'i4'), ('weight', 'f8')])
people = np.array([('Alice', 25, 55.0), ('Bob', 30, 70.5)], dtype=dt)

print(people['name'])     # ['Alice' 'Bob']
print(people['age'])      # [25 30]
print(people[0])          # ('Alice', 25, 55.)
```

## 8.5 Memory-Mapped Files

For arrays too large to fit in RAM:

```python
large = np.memmap('data.bin', dtype='float64', mode='w+', shape=(10000, 10000))
large[0, :] = np.arange(10000)
del large  # flushes to disk

loaded = np.memmap('data.bin', dtype='float64', mode='r', shape=(10000, 10000))
print(loaded[0, :5])   # [0. 1. 2. 3. 4.]
```

---

# 9. NumPy Common Pitfalls and Interview Questions

---

## 9.1 Common Pitfalls

**Pitfall 1: View vs Copy confusion**

```python
a = np.array([1, 2, 3, 4, 5])
b = a[1:4]       # VIEW -- shares memory
b[0] = 99
print(a)          # [1, 99, 3, 4, 5] -- a was modified!

c = a[[1, 2, 3]]  # COPY -- fancy indexing
c[0] = -1
print(a)           # [1, 99, 3, 4, 5] -- a is unchanged
```

**Pitfall 2: Integer overflow wraps silently**

```python
a = np.array([100], dtype=np.int8)   # int8 range is [-128, 127]
print(a + a)                          # [-56] -- 200 wraps modulo 256, no error!
# np.array([200], dtype=np.int8) itself raises OverflowError in NumPy 2 (see 10.6)
```

**Pitfall 3: Chained indexing does not work for assignment**

```python
a = np.zeros((3, 3))
a[a > 0][0] = 1       # does nothing! intermediate copy is modified and discarded
a[a > 0] = 1           # correct: single indexing operation
```

**Pitfall 4: Floating-point comparison**

```python
a = np.array([0.1 + 0.2])
print(a == 0.3)           # [False]
print(np.isclose(a, 0.3)) # [True]
np.allclose(a, 0.3)       # True
```

**Pitfall 5: Modifying array during iteration**

```python
a = np.array([1, 2, 3])
for x in a:
    x = x * 2       # does nothing -- x is a temporary copy
# a is still [1, 2, 3]
a *= 2               # correct vectorized approach: [2, 4, 6]
```

## 9.2 Interview Questions

**Q1: What is the difference between a view and a copy in NumPy?**

A view shares the same underlying data buffer as the original array -- modifying one modifies the other. A copy allocates new memory. Basic indexing (slices) produces views; fancy indexing (integer/boolean arrays) produces copies. Use `np.shares_memory(a, b)` to check. Use `.copy()` to force a copy.

**Q2: Explain broadcasting rules.**

Broadcasting aligns shapes from the trailing (rightmost) dimension. Two dimensions are compatible if they are equal or one is 1. Missing dimensions are padded with 1 on the left. The smaller array is conceptually "stretched" (without actual memory duplication) to match the larger array's shape.

**Q3: Why is `np.linalg.solve(A, b)` preferred over `np.linalg.inv(A) @ b`?**

`solve` uses LU decomposition directly and is: (1) faster (avoids explicit inversion), (2) more numerically stable (fewer floating-point operations), and (3) more memory-efficient. Matrix inversion amplifies rounding errors, especially for ill-conditioned matrices.

**Q4: What happens when you add a float64 array and an int32 array?**

NumPy performs **type promotion** (upcasting). The int32 array is implicitly cast to float64 before the operation. The result dtype is float64. The promotion follows a hierarchy: bool → int → float → complex.

**Q5: How does NumPy achieve its performance advantage over Python lists?**

1. Homogeneous data stored contiguously in memory (cache-friendly)
2. Operations execute in compiled C code, not the Python interpreter
3. No per-element type checking or boxing/unboxing overhead
4. Leverages BLAS/LAPACK for linear algebra
5. Vectorized operations process entire arrays in a single C function call

**Q6: What is the difference between `np.dot`, `@`, `*`, and `np.multiply`?**

- `*` and `np.multiply`: element-wise multiplication
- `@` and `np.matmul`: matrix multiplication (2-D: standard, higher-D: batch)
- `np.dot`: for 2-D arrays same as `@`; for 1-D arrays computes the inner product; for mixed dimensions follows different rules than `@` (no batch behavior)

**Q7: How does `axis` work in aggregation functions?**

The `axis` parameter specifies which dimension is **collapsed**. For a shape `(m, n)` array: `axis=0` collapses rows (result shape `(n,)`), `axis=1` collapses columns (result shape `(m,)`). Think of it as: "sum **along** axis 0" means the axis-0 index varies while we sum.

---

# 10. Advanced NumPy Operations

---

## 10.1 einsum -- Einstein Summation

`np.einsum(subscripts, *operands)` expresses almost any multiply-and-sum over array axes in one string. The rules:

1. Each operand gets one letter per axis (`'ij'` = a 2-D operand).
2. A letter that appears in the inputs but **not** in the output (after `->`) is **summed over**.
3. A letter that appears in several inputs multiplies those axes element-wise (they must have equal length, or length 1 for broadcasting with `...`).
4. The output order follows the letters after `->`. Without `->` (implicit mode), the output is the letters that appear exactly once, in **alphabetical** order. That implicit ordering is a common bug, so always write `->` explicitly.

| Operation | einsum | Equivalent |
|---|---|---|
| Transpose | `'ij->ji'` | `A.T` |
| Sum of all elements | `'ij->'` | `A.sum()` |
| Column sums | `'ij->j'` | `A.sum(axis=0)` |
| Trace | `'ii->'` | `np.trace(A)` |
| Diagonal | `'ii->i'` | `np.diag(A)` |
| Inner product | `'i,i->'` | `a @ b` (1-D) |
| Outer product | `'i,j->ij'` | `np.outer(a, b)` |
| Matrix multiply | `'ik,kj->ij'` | `A @ B` |
| Batched matmul | `'bik,bkj->bij'` | `A @ B` (3-D) |
| Row-wise dot | `'ij,ij->i'` | `(A * B).sum(axis=1)` |
| Bilinear form xᵀMy | `'i,ij,j->'` | `x @ M @ y` |
| Attention scores | `'bhqd,bhkd->bhqk'` | `Q @ K.swapaxes(-1, -2)` |

```python
import numpy as np

rng = np.random.default_rng(0)
A = rng.standard_normal((3, 4))
B = rng.standard_normal((4, 5))
x = rng.standard_normal(3)
M = rng.standard_normal((3, 3))

assert np.allclose(np.einsum('ik,kj->ij', A, B), A @ B)
assert np.allclose(np.einsum('ii->', M), np.trace(M))
assert np.allclose(np.einsum('ij,ij->i', A, A), (A * A).sum(axis=1))
assert np.allclose(np.einsum('i,ij,j->', x, M, x), x @ M @ x)

# Multi-head attention scores: batch b, heads h, query q, key k, head dim d
Q = rng.standard_normal((2, 4, 8, 16))
K = rng.standard_normal((2, 4, 10, 16))
S = np.einsum('bhqd,bhkd->bhqk', Q, K) / np.sqrt(16)
print(S.shape)                         # (2, 4, 8, 10)
assert np.allclose(S, Q @ K.swapaxes(-1, -2) / 4.0)

# Implicit-mode trap: output letters are sorted alphabetically
print(np.einsum('ij,jh', A, B).shape)     # (5, 3) -- implicit output is 'hi' (alphabetical), i.e. (A @ B).T, not A @ B
print(np.einsum('ij,jh->ih', A, B).shape) # (3, 5) -- explicit '->' fixes the output order
# note: np.einsum('ji', A) is A.T, because 'ji' -> 'ij' (sorted output labels)
```

**Performance and contraction order.** With three or more operands, the order of pairwise contractions changes the FLOP count dramatically (the same problem as matrix-chain ordering). `np.einsum` defaults to `optimize=False`, which can evaluate the whole expression as one large nested loop. Pass `optimize=True` (or `'greedy'` / `'optimal'`) to let NumPy pick an order and route pairwise contractions to `tensordot`/BLAS.

```python
import numpy as np

rng = np.random.default_rng(1)
a, b, c = (rng.standard_normal((60, 60)) for _ in range(3))

path, report = np.einsum_path('ij,jk,kl->il', a, b, c, optimize='optimal')
print(path)          # ['einsum_path', (0, 1), (0, 1)] -- contract pairwise
print(report)        # Naive scaling: 4, Optimized scaling: 3, Theoretical speedup: 45.000
r1 = np.einsum('ij,jk,kl->il', a, b, c, optimize=True)
assert np.allclose(r1, a @ b @ c)
```

For three 60×60 matrices, `einsum_path` reports a naive FLOP count of 3.9e7 vs 8.6e5 optimized, a theoretical 45x speedup. That is O(n⁴) vs O(n³), so the gap grows with n.

## 10.2 Stride Tricks: sliding_window_view and as_strided

Recall from section 1.5 that an ndarray is `(buffer pointer, dtype, shape, strides)`. Changing only shape and strides yields a **view** with no data copy. Repeated or overlapping windows can therefore be "materialized" for free by giving an axis a stride smaller than its extent, or a **zero stride** (broadcasting is exactly a zero stride).

```python
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

x = np.arange(8, dtype=np.int64)          # strides (8,)
w = sliding_window_view(x, window_shape=3)
print(w)
# [[0 1 2]
#  [1 2 3]
#  ...
#  [5 6 7]]
print(w.shape, w.strides)                  # (6, 3) (8, 8) -- both axes step 8 bytes
print(np.shares_memory(w, x))              # True -- no copy
print(w.flags.writeable)                   # False -- read-only by default

print(w.mean(axis=1))                      # moving average: [1. 2. 3. 4. 5. 6.]

# 2-D patches (the core of im2col / convolution)
img = np.arange(16).reshape(4, 4)
patches = sliding_window_view(img, (3, 3))
print(patches.shape)                       # (2, 2, 3, 3) -- 2x2 grid of 3x3 patches

# Zero strides: broadcast_to repeats a row without copying
row = np.arange(4)
tiled = np.broadcast_to(row, (1000, 4))
print(tiled.strides, tiled.flags.writeable)   # (0, 8) False
```

`numpy.lib.stride_tricks.as_strided(x, shape, strides)` is the low-level tool underneath. It does **no bounds checking**:

| Danger | What happens | Mitigation |
|---|---|---|
| Wrong shape/strides | View reads memory past the buffer: garbage values or a segfault | Prefer `sliding_window_view` / `broadcast_to`, which compute safe strides |
| Writing through overlapping windows | One memory cell appears in many elements; `w[0, 1] = 9` also changes `w[1, 0]`; in-place ufuncs give order-dependent results | Pass `writeable=False`; copy before mutating |
| Base array freed or resized | Dangling view (only possible if you bypass NumPy's base-object tracking) | Keep a reference to the base array |
| Memory blow-up on `.copy()` or arithmetic | `w * 2` materializes `n × k` elements | Reduce first (`w.sum(axis=-1)`) or use cumsum tricks |

```python
import numpy as np
from numpy.lib.stride_tricks import as_strided, sliding_window_view

x = np.arange(6, dtype=np.int64)
# Safe equivalent of sliding_window_view(x, 3), written by hand:
w = as_strided(x, shape=(4, 3), strides=(8, 8), writeable=False)
assert (w == sliding_window_view(x, 3)).all()
# BUG (don't run): as_strided(x, shape=(10, 3), strides=(8, 8)) reads 6 int64s past the buffer
```

Interview angle: a sliding window of size k over n elements as a view is O(1) memory. `w.sum(axis=1)` is still O(n·k) time; the `cumsum` difference trick (exercise 2 in section 11) is O(n).

## 10.3 Sorting, Selection, and Searching

| Function | What it returns | Complexity | Notes |
|---|---|---|---|
| `np.sort(a, axis)` | Sorted copy | O(n log n) | `kind='stable'` → radix sort for ints ≤ 16-bit, timsort/merge otherwise |
| `np.argsort(a, axis)` | Indices that would sort `a` | O(n log n) | Default quicksort (introsort), **not stable**; use `kind='stable'` for ties |
| `np.partition(a, k)` | Array where `a[k]` is in its sorted position, smaller left, larger right | O(n) average | Introselect; left/right halves are unordered |
| `np.argpartition(a, k)` | Indices version of `partition` | O(n) average | Top-k: O(n + k log k) after sorting just the k winners |
| `np.searchsorted(sorted_a, v, side)` | Insertion indices keeping order | O(m log n) | `side='left'` → first position ≥ v; `'right'` → first position > v |
| `np.lexsort((secondary, primary))` | Multi-key sort indices | O(n log n) | **Last** key is the primary key |
| `np.unique(a, return_index, return_inverse, return_counts)` | Sorted unique values (+ extras) | O(n log n) | `return_inverse` gives dense integer codes |

```python
import numpy as np

a = np.array([30, 10, 50, 20, 40])
order = np.argsort(a)                 # [1 3 0 4 2]
print(a[order])                       # [10 20 30 40 50]
print(np.argsort(-a)[:2])             # indices of top-2: [2 4]

# Top-k with argpartition: O(n) selection, then sort only the k winners
k = 2
idx = np.argpartition(a, -k)[-k:]               # top-2 indices, unordered
idx = idx[np.argsort(a[idx])[::-1]]             # order them descending
print(idx, a[idx])                    # [2 4] [50 40]

# searchsorted: binning, rank lookup, merging sorted arrays
edges = np.array([0, 10, 20, 30])
vals = np.array([5, 10, 25, 30])
print(np.searchsorted(edges, vals, side='left'))    # [1 1 3 3]
print(np.searchsorted(edges, vals, side='right'))   # [1 2 3 4]

# Counting elements in [lo, hi) of a sorted array in O(log n)
s = np.sort(np.array([1, 3, 3, 3, 7, 9]))
lo, hi = np.searchsorted(s, [3, 8])                 # 1, 5
print(hi - lo)                                      # 4 elements in [3, 8)

# unique with inverse = label encoding
labels = np.array(['b', 'a', 'c', 'a', 'b'])
uniq, codes, counts = np.unique(labels, return_inverse=True, return_counts=True)
print(uniq, codes, counts)            # ['a' 'b' 'c'] [1 0 2 0 1] [2 2 1]

# lexsort: sort by last name, then first name (primary key is LAST)
first = np.array(['bo', 'al', 'cy'])
last = np.array(['li', 'li', 'ng'])
print(np.lexsort((first, last)))      # [1 0 2]
```

## 10.4 Counting: bincount, histogram, digitize

```python
import numpy as np

x = np.array([0, 1, 1, 3, 3, 3])
print(np.bincount(x))                     # [1 2 0 3]  counts for 0..max(x)
print(np.bincount(x, minlength=6))        # [1 2 0 3 0 0]

# Weighted bincount = vectorized group-by sum
group = np.array([0, 1, 0, 2, 1])
value = np.array([10., 20., 30., 40., 50.])
sums = np.bincount(group, weights=value)              # [40. 70. 40.]
means = sums / np.bincount(group)                     # [20. 35. 40.]
print(sums, means)

# histogram: bins are half-open [e_i, e_{i+1}) EXCEPT the last, which is closed
data = np.array([0.0, 0.5, 1.0, 1.5, 2.0])
counts, edges = np.histogram(data, bins=2, range=(0, 2))
print(counts, edges)                      # [2 3] [0. 1. 2.]  -- 2.0 lands in last bin

# digitize: which bin each value falls in (1-based against the edges)
print(np.digitize(data, bins=[0.0, 1.0, 2.0]))   # [1 1 2 2 3]
```

| Tool | Input | Use when |
|---|---|---|
| `np.bincount` | Non-negative ints | Dense small integer keys (labels, group IDs); fastest, O(n + max) |
| `np.histogram` | Floats + edges or bin count | Continuous data; uniform bins use a fast path |
| `np.digitize` / `searchsorted` | Floats + edges | You need the per-element bin index, not just counts |
| `np.unique(return_counts=True)` | Any sortable values | Sparse or large keys, O(n log n) |

Pitfall: `np.bincount` raises on negative values, and its output length is `max(x) + 1`. One stray large ID (e.g. 10⁹) allocates an 8-GB array, so remap keys with `np.unique(..., return_inverse=True)` first.

## 10.5 ufunc Methods: reduce, accumulate, outer, reduceat, at

Every binary ufunc (`np.add`, `np.maximum`, `np.logical_or`, ...) carries methods that generalize it:

| Method | Meaning | Example | Result |
|---|---|---|---|
| `reduce(a, axis)` | Fold along an axis | `np.add.reduce([1,2,3,4])` | `10` |
| `accumulate(a)` | Running fold (scan) | `np.maximum.accumulate([1,3,2,5])` | `[1 3 3 5]` |
| `outer(a, b)` | Apply to all pairs | `np.subtract.outer([1,2],[10,20])` | `[[-9 -19] [-8 -18]]` |
| `reduceat(a, idx)` | Reduce over segments starting at `idx` | `np.add.reduceat([1,2,3,4,5], [0,2])` | `[3 12]` |
| `at(a, idx, b)` | **Unbuffered** in-place `a[idx] op= b` | `np.add.at(a, [0,0], 1)` | adds 2 to `a[0]` |

```python
import numpy as np

print(np.add.reduce(np.arange(1, 5)))                  # 10
print(np.multiply.accumulate([1, 2, 3, 4]))            # [ 1  2  6 24]
print(np.maximum.accumulate([1, 3, 2, 5, 4]))          # [1 3 3 5 5] -- running max
print(np.subtract.outer([1, 2], [10, 20]))             # [[ -9 -19] [ -8 -18]]
print(np.add.reduceat(np.arange(1, 6), [0, 2]))        # [ 3 12] -> 1+2, 3+4+5

# Running max drawdown in one line (finance / perf-regression tracking)
series = np.array([100, 120, 90, 130, 80])
drawdown = series / np.maximum.accumulate(series) - 1
print(drawdown.round(3))                                # [ 0.  0. -0.25  0. -0.385]
```

### The `a[idx] += 1` vs `np.add.at` pitfall

```python
import numpy as np

idx = np.array([0, 0, 1, 0])

a = np.zeros(3)
a[idx] += 1
print(a)            # [1. 1. 0.]  -- duplicates in idx are applied ONCE

b = np.zeros(3)
np.add.at(b, idx, 1)
print(b)            # [3. 1. 0.]  -- every occurrence counted

c = np.bincount(idx, minlength=3).astype(float)
print(c)            # [3. 1. 0.]  -- fastest for pure counting / summing
```

**Why:** `a[idx] += 1` is syntactic sugar for `a.__setitem__(idx, a.__getitem__(idx) + 1)`. The gather `a[idx]` produces the **buffered** temporary `[0, 0, 0, 0]`. Adding 1 gives `[1, 1, 1, 1]`. The scatter then writes `a[0] = 1` three times, and the last write wins. `ufunc.at` performs the read-modify-write for each index in order without a temporary buffer. This is the NumPy equivalent of a GPU **scatter-add with atomics** vs. a **racy scatter**.

| Approach | Duplicates handled? | Speed | Use |
|---|---|---|---|
| `a[idx] += v` | No (last write wins) | Fast | Only when `idx` is known unique |
| `np.add.at(a, idx, v)` | Yes | Historically slow (~10-50x slower than bincount); much faster since NumPy 1.25 | General scatter with any ufunc (`np.maximum.at`, ...) |
| `np.bincount(idx, weights=v, minlength=n)` | Yes | Fastest | Scatter-**add** into a dense 1-D target |

### Avoiding temporaries: `out=` and `where=`

```python
import numpy as np

x = np.arange(1_000_000, dtype=np.float64)
y = np.empty_like(x)
np.multiply(x, 2.0, out=y)        # no temporary allocation
np.add(y, 1.0, out=y)             # in place
np.sqrt(x, out=y, where=x > 10)   # only writes where mask is True; other slots keep old y
```

`y = 2 * x + 1` allocates two temporaries of 8 MB each. With `out=`, each pass streams through memory once with no allocator traffic. This matters when arrays approach cache or RAM limits.

## 10.6 dtype Precision: float16, bfloat16, float32, and Integer Overflow

| dtype | Bits (sign/exp/mantissa) | Max | Machine eps | Largest contiguous exact integer |
|---|---|---|---|---|
| `float16` (IEEE half) | 1/5/10 | 65,504 | 9.77e-4 (2⁻¹⁰) | 2,048 (2¹¹) |
| `bfloat16` (brain float) | 1/8/7 | ~3.39e38 | 7.81e-3 (2⁻⁷) | 256 (2⁸) |
| `float32` | 1/8/23 | ~3.40e38 | 1.19e-7 (2⁻²³) | 16,777,216 (2²⁴) |
| `float64` | 1/11/52 | ~1.80e308 | 2.22e-16 (2⁻⁵²) | 2⁵³ ≈ 9.0e15 |

- **float16** has more precision but tiny range: activations or gradients above 65,504 overflow to `inf`, and small gradients underflow. That is why fp16 training needs **loss scaling**.
- **bfloat16** keeps float32's 8-bit exponent (same range, so no loss scaling needed) but has only 8 significant bits. It is the default training dtype on modern GPUs (AMD MI200/MI300, NVIDIA A100+). NumPy has **no native bfloat16**; use the `ml_dtypes` package (the one JAX uses), which registers `bfloat16`, `float8_e4m3fn`, `float8_e5m2`, `int4`, and others as NumPy dtypes.

```python
import numpy as np

print(np.float32(16_777_217))                    # 1.6777216e+07 -- 2**24 + 1 is not representable, rounds to 2**24
print(np.float16(2049))                          # 2.048e+03 (2049 rounds to 2048)
print(np.float16(70000))                         # inf (overflow; may emit RuntimeWarning)
print(np.finfo(np.float16).eps, np.finfo(np.float16).max)   # 0.000977 6.55e+04

# Accumulating in low precision stalls: once the sum hits 2048, adding 1 rounds away
ones = np.ones(5000, dtype=np.float16)
print(np.cumsum(ones)[-1])                       # 2.048e+03 -- sequential accumulation stalls at 2048
print(ones.sum())                                # 5e+03   -- pairwise summation saves it here...
print(np.ones(100_000, dtype=np.float16).sum())  # inf     -- ...but not past float16's max
print(np.ones(100_000, dtype=np.float16).sum(dtype=np.float32))  # 100000.0 -- accumulate wide
```

```python
# Requires: pip install ml_dtypes
import numpy as np
import ml_dtypes

bf16 = ml_dtypes.bfloat16
x = np.array([1.0, 256.0, 257.0, 70000.0], dtype=bf16)
print(x)                                   # [1 256 256 70144] -- 257 rounds to 256; no overflow
print(ml_dtypes.finfo(bf16).eps)           # 0.0078125
w = np.random.default_rng(0).standard_normal((4, 4)).astype(np.float32)
err = np.abs(w - w.astype(bf16).astype(np.float32)).max()
print(err < 0.02)                          # True -- ~3 significant decimal digits
```

**Integer overflow (NumPy 2 semantics, NEP 50):**

```python
import numpy as np

a = np.array([100], dtype=np.int8)
print(a + a)                       # [-56] -- array arithmetic wraps silently (mod 256)
print(a.sum(), a.sum().dtype)      # 100 int64 -- sum/prod of small ints accumulate in the platform int
try:
    np.array([200], dtype=np.int8) # Python int out of range for the dtype
except OverflowError as e:
    print('OverflowError:', e)
try:
    np.int8(100) + 200             # NEP 50: Python scalar 200 does not fit int8 -> error
except OverflowError as e:
    print('OverflowError:', e)
print(np.iinfo(np.int32).max)      # 2147483647 -- e.g. byte counters > 2 GiB overflow int32
```

Pitfalls that come up in interviews:

- **Index arithmetic in int32** (`rows * cols` for a 50k × 50k matrix = 2.5e9) overflows. This is the same bug class as 32-bit offsets in GPU kernels.
- NumPy 2 changed promotion (NEP 50). `np.float32(3) + 3.0` is now `float32` (it was `float64` in NumPy 1.x), because Python scalars are "weak" and do not upcast.
- Mixed `uint64` + `int64` promotes to `float64` and silently loses precision above 2⁵³.

## 10.7 The Random Generator API in Depth

Section 7 covered the basics of `default_rng`. Production and HPC code also needs **independent parallel streams** and an understanding of reproducibility guarantees.

```python
import numpy as np

rng = np.random.default_rng(12345)          # Generator wrapping a PCG64 BitGenerator
print(type(rng.bit_generator).__name__)     # PCG64

# Independent child streams for workers (NumPy >= 1.25)
children = rng.spawn(4)
print([int(c.integers(0, 100)) for c in children])   # four independent streams

# Equivalent lower-level form via SeedSequence (works on older NumPy too)
ss = np.random.SeedSequence(12345)
streams = [np.random.default_rng(s) for s in ss.spawn(4)]

# Pass Generators into functions (dependency injection) instead of global seeding
def noisy(x, rng=None):
    rng = np.random.default_rng(rng)        # accepts None, int seed, or an existing Generator
    return x + rng.normal(scale=0.1, size=x.shape)

print(noisy(np.zeros(3), rng=42).round(3))

# Counter-based generator: cheap to jump, good for GPU-style parallel streams
philox = np.random.Generator(np.random.Philox(key=7))
print(philox.random(2))
```

| Concept | Detail |
|---|---|
| `Generator` vs `RandomState` | `RandomState` (the legacy `np.random.*` functions) is frozen: its stream is stable across NumPy versions. `Generator` may change streams across versions when algorithms improve, so pin the NumPy version if bit-exact reproducibility matters. |
| Default BitGenerator | `PCG64` (128-bit state, period 2¹²⁸). `PCG64DXSM` is recommended for very large numbers of parallel streams. |
| Parallel streams | Use `SeedSequence.spawn` / `Generator.spawn`. **Never** seed workers with `seed + rank`: correlated seeds are a classic bug, while `SeedSequence` hashes the entropy so children are statistically independent. |
| Thread safety | A `Generator` has an internal lock (`bit_generator.lock`), so sharing one across threads is memory-safe. But it serializes the threads, and the draw order between threads is nondeterministic. Give each thread its own spawned `Generator` for speed and reproducibility. |
| Counter-based (`Philox`) | State = (counter, key); can jump to any position in O(1). Same family as cuRAND/rocRAND Philox, so it is a good mental model for GPU RNG. |
| Speed | `Generator.standard_normal` uses the ziggurat method, several times faster than legacy `randn`. |

## 10.8 Views vs Copies Quiz

For each line, decide whether `b` is a **view** of `a` (shares memory) or a **copy**. Answers follow; every one is checked with `np.shares_memory` in the code below.

```text
a = np.arange(12).reshape(3, 4)          # C-contiguous int64

 1. b = a[1:, ::2]
 2. b = a[[0, 2]]
 3. b = a[a > 5]
 4. b = a.T
 5. b = a.T.reshape(-1)
 6. b = a.ravel()
 7. b = a.flatten()
 8. b = a[:, None, :]
 9. b = a.astype(np.int64)
10. b = a.astype(np.int64, copy=False)
11. b = a.view(np.float64)
12. b = np.asarray(a)
13. b = np.array(a)
14. b = a[..., 0]
15. b = a.T.ravel()
```

| # | Answer | Why |
|---|---|---|
| 1 | View | Basic slicing (start:stop:step) only changes offset/strides |
| 2 | Copy | Integer-array (fancy) indexing gathers arbitrary rows |
| 3 | Copy | Boolean indexing gathers a data-dependent number of elements |
| 4 | View | Transpose just swaps strides `(32, 8)` → `(8, 32)` |
| 5 | **Copy** | The transposed data is not contiguous in C order, so no single stride can walk it |
| 6 | View | `ravel` returns a view when possible (C-contiguous `a`) |
| 7 | Copy | `flatten` **always** copies |
| 8 | View | `None`/`np.newaxis` inserts a length-1 axis (any stride) |
| 9 | Copy | `astype` copies by default, even for the same dtype |
| 10 | View (same object) | `copy=False` skips the copy when no conversion is needed; `b is a` is True |
| 11 | View | Reinterprets the same bytes (int64 bit patterns as float64) |
| 12 | View (same object) | `asarray` never copies an ndarray of a matching dtype |
| 13 | Copy | `np.array` copies by default (`copy=True`) |
| 14 | View | Integer index on one axis plus slices is still basic indexing |
| 15 | Copy | Same reason as #5 (`ravel` must copy non-C-contiguous data) |

```python
import numpy as np

a = np.arange(12).reshape(3, 4)
cases = {
    1: a[1:, ::2], 2: a[[0, 2]], 3: a[a > 5], 4: a.T, 5: a.T.reshape(-1),
    6: a.ravel(), 7: a.flatten(), 8: a[:, None, :], 9: a.astype(np.int64),
    10: a.astype(np.int64, copy=False), 11: a.view(np.float64),
    12: np.asarray(a), 13: np.array(a), 14: a[..., 0], 15: a.T.ravel(),
}
expected_view = {1, 4, 6, 8, 10, 11, 12, 14}
for k, b in cases.items():
    assert np.shares_memory(a, b) == (k in expected_view), k
print("all quiz answers verified")
```

Rules of thumb: (1) *basic indexing → view, advanced indexing → copy*; (2) *reshape/ravel give a view only if a single stride pattern can describe the result*; (3) to **require** a view, use `a.reshape(-1, copy=False)` (NumPy 2.1+), which raises `ValueError` instead of silently copying. The older idiom of assigning `b.shape = (12,)` also refuses to copy, but it is deprecated as of NumPy 2.5.

## 10.9 Interview Questions

**Q1.** What does `np.einsum('bij,bjk->bik', A, B)` compute, and when would you use `optimize=True`?

A batched matrix multiply: for each batch index `b`, `C[b] = A[b] @ B[b]`. `j` is summed because it is missing from the output, while `b`, `i`, `k` are kept. Use `optimize=True` whenever there are three or more operands (or large operands). The default `optimize=False` may evaluate the expression as a single nested loop (e.g. O(n⁴) for a 3-matrix chain) instead of pairwise BLAS contractions (O(n³)). `np.einsum_path` shows the chosen order and the FLOP savings. For two-operand matmul, `@` is usually equal or faster because it maps directly to BLAS.

**Q2.** Why can `a[idx] += 1` give a different result from `np.add.at(a, idx, 1)`?

Augmented assignment with fancy indexing is a buffered gather → add → scatter. When `idx` contains duplicates, every duplicate reads the same original value, and the scatter writes are last-write-wins, so each distinct index is incremented only once. `np.add.at` is unbuffered: it performs the read-modify-write for each index occurrence in sequence. For scatter-add into a 1-D array, `np.bincount(idx, weights=v, minlength=n)` is the fastest correct choice. The GPU analogue is a non-atomic scatter vs. `atomicAdd`.

**Q3.** Implement top-k per row efficiently. What is the complexity?

Use `np.argpartition(-X, k-1, axis=1)[:, :k]` to select the k largest per row in O(n) average per row. Then sort just those k with `np.take_along_axis` + `argsort`, which costs O(k log k). Total O(m·(n + k log k)) for an m×n matrix, versus O(m·n log n) for a full `argsort`. See exercise 4 in section 11.

**Q4.** What does `sliding_window_view` return, and what is dangerous about `as_strided`?

It returns a read-only **view** whose new trailing axis has the same stride as the windowed axis, so overlapping windows cost no memory. `as_strided` lets you set any shape/strides with no bounds checks. A mistake reads past the buffer (garbage or segfault), and because overlapping windows alias the same memory, writing through such a view corrupts many logical elements at once. Use `sliding_window_view`/`broadcast_to`, or pass `writeable=False`.

**Q5.** Why is bfloat16 preferred over float16 for training, and how do you use bfloat16 in NumPy?

bfloat16 has float32's 8-bit exponent, so its dynamic range (~1e-38 to ~3e38) matches float32. Gradients don't underflow or overflow, and loss scaling is unnecessary. The cost is precision: 8 significant bits (eps 2⁻⁷ ≈ 0.0078) vs float16's 11 (eps ≈ 0.00098). float16 tops out at 65,504. NumPy has no native bfloat16; install `ml_dtypes` and use `dtype=ml_dtypes.bfloat16`. Always **accumulate** reductions in float32 (`sum(dtype=np.float32)`), the same way GPU matrix units accumulate bf16 products into fp32.

**Q6.** How do you generate reproducible random numbers across 64 parallel worker processes?

Create one root `np.random.SeedSequence(seed)` (or a `Generator`) and call `.spawn(64)`. Each child seeds its own `Generator`. Never use `seed + worker_id` or share one Generator across threads or processes. Record the root seed and the NumPy version, because `Generator` streams are not guaranteed identical across NumPy releases (legacy `RandomState` is).

**Q7.** `np.histogram(data, bins=10)` -- which bin does the maximum value land in, and how would you count values per integer label faster?

All bins are half-open `[left, right)` except the last, which is closed `[left, right]`, so the max lands in bin 9 rather than being dropped. For non-negative integer labels, `np.bincount(labels, minlength=K)` is O(n + K) with no edge search, much faster than `histogram` with K bins. With `weights=` it also gives a group-by sum.

**Q8.** Common follow-up: `a.T.reshape(-1)` -- view or copy, and how do you make NumPy fail loudly instead of copying?

It is a copy. A transposed C-contiguous array is F-contiguous, so its C-order flattening cannot be described by a single stride. To forbid a silent copy, use `reshape(-1, copy=False)` (NumPy 2.1+), which raises `ValueError` when a view is impossible. Assigning to `.shape` did the same, but it is deprecated in NumPy 2.5. Check with `np.shares_memory` or `b.base is a`.

**See also:** [Floating-Point Numerics and Reproducibility](../computer-science/Performance_Engineering.md#9-floating-point-numerics-and-reproducibility) · [SIMD and Vectorization](../computer-science/Performance_Engineering.md#6-simd-and-vectorization) · [Memory Optimization on GPUs](../ml-gpu/Parallel_GPU_Programming.md#20-memory-optimization) · [Tensor Fundamentals (PyTorch dtypes, einsum)](../ml-gpu/ML_AI_Frameworks.md#1-tensor-fundamentals)

---

# 11. NumPy Vectorization Exercise Set

---

These are the "no Python loops allowed" questions that ML-infra, HPC, and quant screens ask. Try each one before reading the answer. For every answer, be ready to state the **time complexity**, the **peak extra memory**, and one **numerical pitfall**.

## 11.1 Problems

**E1. Pairwise Euclidean distances.** Given `X` of shape `(n, d)` and `Y` of shape `(m, d)`, return `D` of shape `(n, m)` with `D[i, j] = ||X[i] - Y[j]||₂`. Do it without materializing an `(n, m, d)` tensor.

**E2. Moving average.** Given a 1-D array `x` and window `k`, return the `len(x) - k + 1` means of each full window in O(n) time.

**E3. One-hot encoding.** Given integer labels `y` of shape `(n,)` with values in `[0, C)`, return a `(n, C)` float array with a single 1 per row.

**E4. Top-k per row.** Given `S` of shape `(m, n)`, return the indices and values of the k largest entries of each row, sorted descending, in better than O(m · n log n).

**E5. Histogram without np.histogram.** Given floats `x` and `B` equal-width bins over `[lo, hi)`, return the counts per bin using one vectorized call (values outside the range are dropped).

**E6. Numerically stable softmax.** Row-wise softmax of `Z` of shape `(m, n)` that does not overflow for large logits (e.g. 1000).

**E7. 2-D convolution (valid, single channel) via im2col.** Given image `I` `(H, W)` and kernel `K` `(kh, kw)`, compute the valid cross-correlation without Python loops.

**E8. Group-by mean.** Given `keys` (arbitrary integers, possibly large like 10⁹) and `vals`, return the unique keys and the mean value per key.

## 11.2 Answers

```python
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

rng = np.random.default_rng(0)

# ---------- E1: pairwise distances via ||x||^2 + ||y||^2 - 2 x.y ----------
def pairwise_dist(X, Y):
    xx = np.einsum('ij,ij->i', X, X)[:, None]       # (n, 1)
    yy = np.einsum('ij,ij->i', Y, Y)[None, :]       # (1, m)
    d2 = xx + yy - 2.0 * (X @ Y.T)                  # (n, m) -- one GEMM
    np.maximum(d2, 0.0, out=d2)                     # cancellation can give -1e-12
    return np.sqrt(d2)

X, Y = rng.standard_normal((50, 8)), rng.standard_normal((40, 8))
ref = np.sqrt(((X[:, None, :] - Y[None, :, :]) ** 2).sum(-1))   # (n, m, d) broadcast: memory-hungry
assert np.allclose(pairwise_dist(X, Y), ref)

# ---------- E2: moving average with cumsum, O(n) ----------
def moving_average(x, k):
    c = np.cumsum(np.concatenate(([0.0], x)))       # c[i] = sum(x[:i])
    return (c[k:] - c[:-k]) / k

x = rng.standard_normal(1000)
assert np.allclose(moving_average(x, 5), sliding_window_view(x, 5).mean(axis=1))
assert np.allclose(moving_average(x, 5), np.convolve(x, np.ones(5) / 5, mode='valid'))

# ---------- E3: one-hot ----------
def one_hot(y, C):
    out = np.zeros((y.size, C))
    out[np.arange(y.size), y] = 1.0                 # paired fancy indexing
    return out                                      # alt: np.eye(C)[y]

y = np.array([2, 0, 1, 2])
print(one_hot(y, 3))
assert (one_hot(y, 3) == np.eye(3)[y]).all()

# ---------- E4: top-k per row with argpartition ----------
def topk_rows(S, k):
    part = np.argpartition(-S, k - 1, axis=1)[:, :k]          # unordered top-k, O(n) per row
    vals = np.take_along_axis(S, part, axis=1)
    order = np.argsort(-vals, axis=1)                         # sort only k items
    idx = np.take_along_axis(part, order, axis=1)
    return idx, np.take_along_axis(S, idx, axis=1)

S = rng.standard_normal((6, 100))
idx, vals = topk_rows(S, 3)
assert np.array_equal(vals, -np.sort(-S, axis=1)[:, :3])

# ---------- E5: histogram via bincount ----------
def hist(x, B, lo, hi):
    x = x[(x >= lo) & (x < hi)]
    bins = ((x - lo) * (B / (hi - lo))).astype(np.int64)
    np.minimum(bins, B - 1, out=bins)               # guard float rounding at the top edge
    return np.bincount(bins, minlength=B)

data = rng.uniform(-1, 3, size=10_000)
ref_counts, _ = np.histogram(data[data < 2], bins=4, range=(0, 2))
assert np.array_equal(hist(data, 4, 0.0, 2.0), ref_counts)

# ---------- E6: stable softmax ----------
def softmax(Z, axis=-1):
    Z = Z - Z.max(axis=axis, keepdims=True)         # exp of <= 0 never overflows
    E = np.exp(Z)
    return E / E.sum(axis=axis, keepdims=True)

Z = np.array([[1000.0, 1001.0, 1002.0], [1.0, 2.0, 3.0]])
P = softmax(Z)
print(P.round(4))                                   # both rows: [0.09 0.2447 0.6652]
assert np.allclose(P.sum(axis=1), 1) and np.isfinite(P).all()

# ---------- E7: conv2d (valid cross-correlation) via im2col ----------
def conv2d_valid(I, K):
    patches = sliding_window_view(I, K.shape)       # (H-kh+1, W-kw+1, kh, kw) view
    return np.einsum('ijkl,kl->ij', patches, K)

I = rng.standard_normal((6, 7)); K = rng.standard_normal((3, 3))
ref = np.array([[(I[i:i+3, j:j+3] * K).sum() for j in range(5)] for i in range(4)])
assert np.allclose(conv2d_valid(I, K), ref)

# ---------- E8: group-by mean with unique + bincount ----------
def groupby_mean(keys, vals):
    uniq, codes = np.unique(keys, return_inverse=True)       # dense codes 0..G-1
    sums = np.bincount(codes, weights=vals)
    counts = np.bincount(codes)
    return uniq, sums / counts

keys = np.array([10**9, 7, 10**9, 7, 3])
vals = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
print(groupby_mean(keys, vals))     # (array([3, 7, 1000000000]), array([5., 3., 2.]))
print("all exercises verified")
```

## 11.3 Discussion of the Answers

| # | Time | Extra memory | Key insight / pitfall |
|---|---|---|---|
| E1 | O(n·m·d), dominated by one GEMM | O(n·m) | Naive broadcast allocates n·m·d floats (n = m = 10⁴, d = 512 → ~410 GB in float64). The expansion trick can produce tiny **negative** values from cancellation, so clamp before `sqrt`. For high accuracy on near-duplicate points, use `scipy.spatial.distance.cdist` |
| E2 | O(n) | O(n) | `cumsum` on long float32 inputs accumulates error; use float64 for the prefix sum. `sliding_window_view(...).mean` is O(n·k) but memory-free |
| E3 | O(n·C) | O(n·C) | `np.eye(C)[y]` is concise but builds a C×C identity first, which is bad for C = 10⁶. Out-of-range labels raise `IndexError`; negative labels silently wrap (`-1` → last class) |
| E4 | O(m·(n + k log k)) | O(m·k) | `argpartition` kth is 0-based; pass `k - 1` to put the k-th largest in position. `take_along_axis` is the general "gather by per-row indices" tool |
| E5 | O(n + B) | O(n) | `np.histogram` puts `x == hi` in the last bin (closed right edge). This version drops it, so state the convention. Float rounding can map a value just below `hi` to bin `B`; clamp |
| E6 | O(m·n) | O(m·n) | Subtracting the row max keeps `exp` ≤ 1. Use `scipy.special.logsumexp` for log-probabilities. Common follow-up: the same max-subtraction is what fused attention kernels do online (FlashAttention keeps a running max and sum) |
| E7 | O(H·W·kh·kw) | O(H·W) output only | The patches tensor is a stride view. The `einsum` contracts it without copying, while `patches.reshape(-1, kh*kw) @ K.ravel()` forces an im2col **copy** of kh·kw× the image size. That copy is exactly what GPU im2col+GEMM convolution pays for |
| E8 | O(n log n) for `unique` | O(n) | `np.bincount(keys)` directly on 10⁹-sized keys would allocate a 10⁹-length array; compress keys first. pandas `groupby` does the same factorize → bincount internally |

**Follow-ups interviewers ask:**

- *"Make E1 cosine similarity."* Normalize rows (`X / np.linalg.norm(X, axis=1, keepdims=True)`) and compute `Xn @ Yn.T`.
- *"E2 with a weighted (exponential) moving average?"* An EMA is a recurrence `y[t] = a·x[t] + (1-a)·y[t-1]`, which doesn't vectorize with plain ufuncs. Use `scipy.signal.lfilter([a], [1, a-1], x)`, Numba, or pandas `ewm`.
- *"E4 over the whole matrix instead of per row?"* `np.argpartition(S.ravel(), -k)[-k:]`, then `np.unravel_index`.
- *"E6 when n is 10⁶ and doesn't fit in one block?"* Use an online/streaming softmax: keep a running max `m` and running sum `s`, rescaling `s *= exp(m_old - m_new)` when the max changes.

**See also:** [Coding Problem List](../practice/Coding_Problem_List.md) · [Key Triton Kernels: MatMul, Attention, Softmax](../ml-gpu/ML_AI_Frameworks.md#27-key-triton-kernels-matmul-attention-softmax) · [GPU Kernel Case Studies](../ml-gpu/GPU_Kernel_Case_Studies.md)

---

# 12. GPU Array Ecosystem and Zero-Copy Interop

---

> Snippets marked `# Requires: ...` need that package (and, for GPU code, a CUDA or ROCm GPU). Everything else runs with NumPy alone. See also: [HIP Fundamentals and Portability](../ml-gpu/Parallel_GPU_Programming.md#25-hip-fundamentals-and-portability), [ROCm Ecosystem and Libraries](../ml-gpu/Parallel_GPU_Programming.md#31-rocm-ecosystem-and-libraries), [Tensor Fundamentals (PyTorch)](../ml-gpu/ML_AI_Frameworks.md#1-tensor-fundamentals), [JAX Fundamentals](../ml-gpu/ML_AI_Frameworks.md#18-jax-fundamentals).

## 12.1 The Landscape

| Library | What it is | Devices | When to reach for it |
|---|---|---|---|
| NumPy | Reference CPU ndarray | CPU | Default; everything interoperates with it |
| CuPy | NumPy/SciPy-compatible arrays on GPU | NVIDIA (CUDA), AMD (ROCm, experimental) | Port NumPy code to GPU with minimal edits; custom kernels in CUDA/HIP C++ |
| Numba | LLVM JIT for a numeric subset of Python | CPU (`@njit`), GPU (CUDA via `numba-cuda`; AMD via `numba-hip`) | Loops that don't vectorize (recurrences, early exit, state machines) |
| PyTorch | Tensors + autograd + NN | CPU, CUDA, ROCm (the `cuda` device name is reused on ROCm) | ML; also a general GPU array library |
| JAX | NumPy API + `jit`/`grad`/`vmap` via XLA | CPU, CUDA, ROCm, TPU | Functional, compiled numerics; research ML |
| Triton | Python DSL for GPU kernels | NVIDIA, AMD | Fused custom kernels inside PyTorch |
| cuDF / Dask / Polars | DataFrames | GPU / cluster / CPU | See [Pandas Ecosystem](Pandas.md#35-ecosystem-and-when-to-switch) |

The glue that lets these share memory **without copies** is a small set of protocols: the buffer protocol and `__array_interface__` (CPU), `__cuda_array_interface__` (GPU), and DLPack (CPU and GPU, vendor-neutral). Dispatch between libraries is handled by the Python **array API standard**.

## 12.2 CuPy

CuPy mirrors the NumPy API (`cupy.ndarray`, ufuncs, `cupy.linalg`, `cupy.fft`, `cupy.random`) and much of SciPy (`cupyx.scipy.sparse`, `.signal`, `.ndimage`). It calls vendor libraries underneath: cuBLAS/cuFFT/cuSPARSE on NVIDIA, and hipBLAS/rocBLAS, hipFFT/rocFFT, hipSPARSE/rocSPARSE on AMD.

```python
# Requires: cupy (CUDA or ROCm build) and a GPU
import numpy as np
import cupy as cp

x_cpu = np.random.default_rng(0).standard_normal((4096, 4096), dtype=np.float32)
x = cp.asarray(x_cpu)                 # host -> device copy (H2D)
y = x @ x.T                           # rocBLAS/cuBLAS GEMM, launched asynchronously
s = cp.linalg.norm(y)                 # still on device
print(float(s))                       # float() forces device -> host copy AND synchronization
y_cpu = cp.asnumpy(y)                 # or y.get(); D2H copy

# CPU/GPU-agnostic code
def normalize(a):
    xp = cp.get_array_module(a)       # numpy or cupy depending on input
    return (a - xp.mean(a, axis=0)) / xp.std(a, axis=0)

# Custom element-wise kernel (code generated and compiled with NVRTC / hipRTC on first call)
squared_diff = cp.ElementwiseKernel(
    'float32 a, float32 b', 'float32 out',
    'out = (a - b) * (a - b)', 'squared_diff')
z = squared_diff(x, x.T)

# Raw kernel: you write the CUDA C++ / HIP source; the same source works on ROCm builds
add_kernel = cp.RawKernel(r'''
extern "C" __global__ void add(const float* a, const float* b, float* c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) c[i] = a[i] + b[i];
}''', 'add')
n = 1 << 20
a = cp.ones(n, dtype=cp.float32); b = cp.ones(n, dtype=cp.float32); c = cp.empty_like(a)
add_kernel(((n + 255) // 256,), (256,), (a, b, c, cp.int32(n)))   # grid, block, args

# Correct GPU timing: events on the stream, not time.time()
start, end = cp.cuda.Event(), cp.cuda.Event()
start.record(); y = x @ x.T; end.record(); end.synchronize()
print(cp.cuda.get_elapsed_time(start, end), 'ms')

# Or the built-in benchmark helper (handles warmup and syncs)
from cupyx.profiler import benchmark
print(benchmark(lambda m: m @ m.T, (x,), n_repeat=20))
```

**CuPy on ROCm (AMD).** ROCm support is labelled *experimental* upstream, and the packaging has changed several times, so check the [CuPy install guide](https://docs.cupy.dev/en/stable/install.html) for the current state. As of late 2026 there are three routes:

| Route | Command / notes |
|---|---|
| Upstream wheel (CuPy v14) | `pip install cupy-rocm-7-0` (wheel name encodes the ROCm major-minor; needs a matching ROCm install) |
| AMD-hosted build | `pip install amd-cupy --extra-index-url=https://pypi.amd.com/simple` (AMD's fork, wheels for ROCm 7.x) |
| From source | `export CUPY_INSTALL_USE_HIP=1 ROCM_HOME=/opt/rocm HCC_AMDGPU_TARGET=gfx942` then `pip install cupy` (take the `gfx` target from `rocminfo`; requires hipBLAS, rocSPARSE, rocRAND, rocThrust, rocPRIM, etc.) |

On ROCm, the Python namespaces keep their CUDA names (`cp.cuda.Device`, `cp.cuda.Stream`, `__cuda_array_interface__`); they map to HIP underneath. Kernels compile through hipRTC, and some CUDA-only features (e.g. certain cuTENSOR/cuDNN paths) are unavailable.

**CuPy pitfalls:**

| Pitfall | Explanation |
|---|---|
| Hidden synchronization | `print(x)`, `float(x)`, `x.get()`, `if x.any():`, and Python control flow on device values all copy to host and block until the stream drains |
| First-call latency | Each new kernel/dtype combination is compiled and cached (`~/.cupy/kernel_cache`); time the second call |
| Memory pool | CuPy caches freed blocks, so `rocm-smi`/`nvidia-smi` show memory as "used" after arrays die. Use `cp.get_default_memory_pool().free_all_blocks()` to release it |
| Small arrays | Kernel launch overhead (~5-20 µs) dominates for small arrays; NumPy on CPU can be faster below ~10⁴-10⁵ elements |
| Mixing with NumPy | `np.sum(cupy_array)` dispatches back to CuPy via `__array_function__`, but `np.asarray(cupy_array)` raises (implicit D2H is refused). Use `.get()` explicitly |

## 12.3 Numba

Numba compiles a numeric subset of Python (NumPy arrays, scalars, tuples, typed containers, most of `math` and many NumPy functions) to machine code through LLVM. Compilation happens on the first call for each argument-type signature.

```python
# Requires: pip install numba
import numpy as np
from numba import njit, prange, vectorize

@njit(cache=True)                       # nopython mode; cache=True stores machine code on disk
def ema(x, alpha):                      # a recurrence: cannot be vectorized with ufuncs
    out = np.empty_like(x)
    out[0] = x[0]
    for t in range(1, x.size):
        out[t] = alpha * x[t] + (1 - alpha) * out[t - 1]
    return out

@njit(parallel=True, fastmath=True)
def row_norms(A):
    out = np.empty(A.shape[0])
    for i in prange(A.shape[0]):        # iterations distributed over threads
        s = 0.0
        for j in range(A.shape[1]):
            s += A[i, j] * A[i, j]
        out[i] = np.sqrt(s)
    return out

@njit(parallel=True)
def parallel_sum(x):
    total = 0.0
    for i in prange(x.size):            # scalar += inside prange is recognized as a REDUCTION
        total += x[i]
    return total

@vectorize(['float64(float64, float64)'])   # builds a real NumPy ufunc (broadcasting, out=, reduce)
def huber(r, d):
    a = abs(r)
    return 0.5 * r * r if a <= d else d * (a - 0.5 * d)

x = np.random.default_rng(0).standard_normal(1_000_000)
A = x.reshape(1000, 1000)
print(ema(x[:5], 0.5).round(3))
assert np.allclose(row_norms(A), np.linalg.norm(A, axis=1))
assert np.isclose(parallel_sum(x), x.sum())
print(huber(np.array([0.5, 3.0]), 1.0))     # [0.125 2.5  ]
```

| Option | Effect | Caveat |
|---|---|---|
| `@njit` / `@jit` | nopython compilation (the default for `@jit` since Numba 0.59) | Unsupported Python objects (pandas, arbitrary classes, most of the stdlib) fail to compile |
| `cache=True` | Persist compiled code to `__pycache__` | Invalidated by source or Numba-version changes |
| `parallel=True` + `prange` | Multithreaded loops, plus automatic fusion of array expressions | Writes to a shared element from different iterations are a **race**; only simple scalar `+=`/`*=` reductions are handled |
| `fastmath=True` | Lets LLVM reassociate floating point ops (enables SIMD reductions) | Results can differ in the last bits; NaN/Inf handling relaxed |
| `nogil=True` | Releases the GIL inside the compiled function | Enables real parallelism from Python threads |
| `@vectorize` / `@guvectorize` | Create true ufuncs / generalized ufuncs | Must declare signatures for eager compile |

**GPU targets:**

- **NVIDIA**: `from numba import cuda` with `@cuda.jit` kernels, `cuda.grid(1)`, and `cuda.shared.array`. The built-in CUDA target is **deprecated since Numba 0.61**; development moved to NVIDIA's separate `numba-cuda` package (`pip install numba-cuda`), which keeps the same `numba.cuda` API.
- **AMD**: Numba's old built-in `numba.roc` (HSA) target was removed years ago. The current route is AMD's **Numba HIP** (`ROCm/numba-hip`, now distributed alongside `hip-python`): `from numba import hip`, `@hip.jit`, `hip.grid(1)`. `hip.pose_as_cuda()` lets unmodified `@cuda.jit` code run on AMD GPUs. It is still young; check the repo for supported ROCm versions.

```python
# Requires: numba-hip (AMD GPU) -- or replace `hip` with `cuda` on NVIDIA with numba-cuda
import numpy as np
from numba import hip

@hip.jit
def saxpy(a, x, y, out):
    i = hip.grid(1)                     # blockIdx.x * blockDim.x + threadIdx.x
    if i < x.size:                      # guard: grid is rounded up to a block multiple
        out[i] = a * x[i] + y[i]

n = 1 << 20
x = np.ones(n, np.float32); y = np.ones(n, np.float32); out = np.empty_like(x)
threads = 256
blocks = (n + threads - 1) // threads
saxpy[blocks, threads](np.float32(2.0), x, y, out)   # host arrays are copied implicitly (slow path)
print(out[:3])                                       # [3. 3. 3.]
```

## 12.4 Array Interfaces: Buffer Protocol, `__array_interface__`, `__cuda_array_interface__`

| Protocol | Level | Describes | Consumers |
|---|---|---|---|
| Buffer protocol (PEP 3118) | C-API | Host pointer, shape, strides, format | `memoryview`, NumPy, `bytes`, Cython, PIL |
| `__array_interface__` | Python dict | Host pointer + shape/typestr/strides (version 3) | `np.asarray`, and libraries that read NumPy-like objects |
| `__array__()` method | Python method | "Convert me to an ndarray" (may copy) | `np.asarray` fallback |
| `__cuda_array_interface__` (CAI, v3) | Python dict | **Device** pointer + shape/typestr/strides + `stream` | CuPy, Numba, PyTorch, cuDF, JAX, and others; ROCm builds keep the name |
| DLPack (`__dlpack__`, `__dlpack_device__`) | C struct in a capsule | Pointer + device (type, id) + shape/strides/dtype + deleter | NumPy, CuPy, PyTorch, JAX, TensorFlow, MXNet, cuDF, ... |

```python
import numpy as np

a = np.arange(6, dtype=np.float32).reshape(2, 3)
print(a.__array_interface__)
# {'data': (<address>, False), 'strides': None, 'descr': [('', '<f4')],
#  'typestr': '<f4', 'shape': (2, 3), 'version': 3}
# strides None => C-contiguous; data = (pointer, read_only_flag)

# Any object exposing __array_interface__ can be wrapped zero-copy by NumPy
class ForeignBuffer:
    def __init__(self, owner):
        self._owner = owner                       # keep the memory alive!
        self.__array_interface__ = owner.__array_interface__

b = np.asarray(ForeignBuffer(a))
b[0, 0] = 42
print(a[0, 0], np.shares_memory(a, b))            # 42.0 True

m = memoryview(a)                                  # buffer protocol
print(m.format, m.shape, m.strides)                # f (2, 3) (12, 4)
```

`__cuda_array_interface__` has the same keys but `data[0]` is a **device** pointer. Version 3 adds `stream`: the producer's stream on which the data is (or will be) ready. The consumer must synchronize with that stream before reading. `None` means no synchronization is needed, 1 is the legacy default stream, 2 is the per-thread default stream, and any other integer is a stream handle. Getting this wrong produces intermittent garbage reads, the classic "works with `CUDA_LAUNCH_BLOCKING=1`" bug.

## 12.5 DLPack: Zero-Copy Exchange Between Frameworks

DLPack is a tiny C ABI (`DLManagedTensor` / `DLManagedTensorVersioned` in DLPack 1.x) that describes a tensor (data pointer, `DLDevice{device_type, device_id}`, ndim, dtype, shape, strides, byte offset) plus a **deleter** callback that the consumer calls when done. Modern exchange goes through two methods on the producer:

- `x.__dlpack_device__()` → `(device_type, device_id)`. Device type codes include `kDLCPU = 1`, `kDLCUDA = 2`, `kDLCUDAHost = 3`, `kDLROCM = 10`, `kDLROCMHost = 11`.
- `x.__dlpack__(stream=None, ...)` → a PyCapsule. The **consumer** passes its stream so the producer can make the data safe to use there, usually by enqueueing a wait on an event.

The consumer calls `from_dlpack(x)`: `np.from_dlpack`, `torch.from_dlpack`, `cp.from_dlpack`, `jax.dlpack.from_dlpack`.

```python
import numpy as np

a = np.arange(5.0)
print(a.__dlpack_device__())          # (1, 0) -> kDLCPU, device 0
b = np.from_dlpack(a)                 # zero-copy; NumPy >= 1.22
b[0] = 100.0
print(a[0], np.shares_memory(a, b))   # 100.0 True
```

```python
# Requires: torch (and cupy for the GPU half)
import numpy as np
import torch

t = torch.arange(4, dtype=torch.float32)
n = np.from_dlpack(t)                 # CPU tensor -> ndarray, zero-copy
n[0] = 9.0
print(t[0].item())                    # 9.0 -- shared memory

back = torch.from_dlpack(n)           # ndarray -> tensor, zero-copy

import cupy as cp
g = torch.ones(3, device='cuda')      # 'cuda' is also the device name on ROCm PyTorch
c = cp.from_dlpack(g)                 # GPU tensor -> CuPy, zero-copy, stream-safe
t2 = torch.from_dlpack(c * 2)         # and back
```

| Question | Answer |
|---|---|
| Is it really zero-copy? | Yes. Only the descriptor moves. The consumer holds a reference so the producer's memory stays alive until the deleter runs |
| Cross-device? | No. DLPack never moves data between devices; `np.from_dlpack(gpu_tensor)` raises. NumPy 2.1+ / DLPack 1.0 add a `device=`/`copy=` negotiation that lets a producer copy when explicitly asked |
| Read-only arrays? | DLPack 1.0 has a read-only flag; older producers refuse to export read-only arrays (`BufferError`) |
| Vs `torch.from_numpy`? | `from_numpy` is NumPy-specific (uses the NumPy C API; requires an ndarray -- `torch.frombuffer` is the buffer-protocol path) and CPU-only; DLPack is the vendor-neutral standard that also covers GPUs |
| Gotchas | Non-contiguous or negative-stride arrays may be rejected by some consumers. Exporting a tensor that requires grad needs `.detach()`. Both sides now alias, so in-place writes on one are visible on the other |

## 12.6 The Python Array API Standard

The [Consortium for Python Data API Standards](https://data-apis.org/array-api/) defines a common array API (creation, elementwise, linear algebra, sorting, statistics, indexing) so that library code can be written once and run on NumPy, CuPy, PyTorch, JAX, or Dask arrays.

- NumPy 2.0 made its main namespace compliant (the experimental `numpy.array_api` module was removed). `np.__array_api_version__` reports the supported revision; it was `'2023.12'` in NumPy 2.1 and is newer in later releases.
- `x.__array_namespace__()` returns the module implementing the standard for that array. The `array_api_compat` package wraps libraries that are not fully compliant (e.g. PyTorch) and provides `array_namespace(*arrays)`.
- `array_api_strict` is a minimal implementation for testing that your code uses only the standard.
- Adopters: SciPy (set `SCIPY_ARRAY_API=1`), scikit-learn (`sklearn.set_config(array_api_dispatch=True)`) for a growing set of estimators.

```python
import numpy as np

def logsumexp(x, axis=-1):
    xp = x.__array_namespace__()          # works for any array-API-compliant array
    m = xp.max(x, axis=axis, keepdims=True)
    return xp.squeeze(m, axis=axis) + xp.log(xp.sum(xp.exp(x - m), axis=axis))

x = np.array([[1000.0, 1000.0], [0.0, 0.0]])
print(logsumexp(x))                       # [1.00069315e+03 6.93147181e-01]
print(np.__array_api_version__)
```

Standard vs NumPy-only differences to know: the standard uses `xp.concat` (not `concatenate`), `xp.permute_dims` (not `transpose`), `xp.astype(x, dtype)` as a function, and has no in-place `sort`, no `np.matrix`, and no object dtype. Boolean-mask indexing and data-dependent output shapes are optional, because they cannot be traced by compilers like JAX.

## 12.7 Threads, the GIL, and BLAS

- Most NumPy ufunc loops, sorting, and BLAS calls **release the GIL** for non-object dtypes, so Python threads can overlap large array operations. Small-array overhead (dispatch while holding the GIL) still serializes.
- BLAS (OpenBLAS / MKL / AOCL-BLAS / BLIS) is itself multithreaded. Combining it with `multiprocessing`, Numba `parallel=True`, or Dask workers causes **oversubscription**: N processes × M BLAS threads > cores. Cap it with `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS`, or `threadpoolctl.threadpool_limits(1)`.
- `np.show_config()` shows which BLAS/LAPACK NumPy was built against.
- See [Python Fundamentals](Python_Fundamentals.md) for the GIL and free-threaded CPython.

## 12.8 Interview Questions

**Q1.** You have a CuPy array and need it as a PyTorch tensor on the same GPU without a copy. How, and what can go wrong?

Use `torch.from_dlpack(cupy_arr)` (or `cupy_arr.toDlpack()` on older versions). The capsule carries the device pointer, shape, strides, and dtype, and a deleter keeps CuPy's buffer alive while PyTorch holds it. Pitfalls: (1) **stream ordering**. PyTorch passes its current stream to `__dlpack__`, and the producer must make pending writes visible on it; with the older CAI path, ignoring the `stream` key causes races. (2) **Aliasing**: in-place ops on either side mutate both. (3) Memory-pool interplay: the memory returns to CuPy's pool only after PyTorch releases it. (4) Non-contiguous layouts may be rejected or force a copy.

**Q2.** When would you use Numba instead of vectorized NumPy?

When the algorithm has a loop-carried dependency (EMA, cumulative state machines, dynamic programming), early exits, or would need large temporaries in NumPy (e.g. fusing `a*b + c*d - e` without allocating three intermediates). Numba compiles the loop to native code at near-C speed, can multithread with `prange`, and releases the GIL with `nogil=True`. Don't use it when the work is already one BLAS call or a single ufunc, or when you need pandas/objects inside the hot loop. Remember to exclude the first call (compilation) from timings.

**Q3.** What does `parallel=True` actually do, and what is a race in `prange`?

Numba's parallel accelerator fuses array expressions and distributes `prange` iterations across a thread pool (TBB, OpenMP, or workqueue backend). Simple scalar accumulations (`total += x[i]`) are recognized as reductions and given per-thread partials. Writing to a shared array element from different iterations (e.g. `hist[x[i]] += 1`) is a data race that silently loses updates, the same bug as a non-atomic GPU histogram. Fix it with per-thread private histograms merged at the end, or restructure the loop so each iteration owns its output.

**Q4.** What is the difference between `__cuda_array_interface__` and DLPack?

CAI is a Python-level dict (pointer, shape, typestr, strides, stream) that is CUDA-specific by name (ROCm builds reuse it). It has no ownership semantics: the consumer must keep the producer object alive. DLPack is a C ABI with an explicit device type (CPU, CUDA, ROCm, oneAPI, Metal, ...), a deleter for ownership transfer, and a stream-negotiation protocol (`__dlpack__(stream=...)`). DLPack is the standard used by `from_dlpack` across NumPy, PyTorch, JAX, and CuPy and by the array API standard; CAI predates it and is still common in the Numba/RAPIDS world.

**Q5.** How do you time a CuPy (or any GPU) operation correctly?

GPU launches are asynchronous, so `time.time()` around `y = x @ x` measures only the launch. Record events on the stream before and after, then synchronize on the end event and read `get_elapsed_time` (or call `cp.cuda.Device().synchronize()` around wall-clock timing). Warm up first to exclude JIT/kernel-cache compilation and memory-pool growth. Repeat and report the median and spread. `cupyx.profiler.benchmark` does this, reporting CPU and GPU times separately. For kernel-level detail, use `rocprofv3` / `rocprof-compute` on AMD or Nsight on NVIDIA.

**Q6.** What is the array API standard and why do SciPy and scikit-learn care?

It is a library-neutral specification of array functions and semantics. Code that obtains `xp = array_namespace(x)` and uses only standard functions runs unchanged on NumPy (CPU), CuPy/PyTorch (GPU), or JAX. SciPy and scikit-learn adopt it so that passing a GPU array keeps the computation on the GPU instead of silently converting to NumPy. The trade-off is a smaller API surface: no object dtype, optional data-dependent shapes, and function-style `astype`/`concat`/`permute_dims`.

**Q7.** Your Python app uses `multiprocessing.Pool(32)` on a 32-core node, and each worker calls `np.linalg.svd`. It is slower than expected. Why?

Each worker's BLAS/LAPACK spawns ~32 threads, giving 1,024 threads on 32 cores. Context switching and cache thrashing follow. Set `OMP_NUM_THREADS=1` (or `threadpoolctl`) in the workers, or use fewer processes with more BLAS threads each.

**See also:** [AMD GPU Architecture and Profiling](../ml-gpu/AMD_GPU_Architecture_and_Profiling.md) · [HIP Streams, Events, and Synchronization](../ml-gpu/Parallel_GPU_Programming.md#28-hip-streams-events-and-synchronization) · [Triton Fundamentals](../ml-gpu/ML_AI_Frameworks.md#25-triton-fundamentals) · [NUMA](../computer-science/Performance_Engineering.md#7-numa) · [Debugging and Profiling Tools](../tools/Debugging_and_Profiling_Tools.md)

---

# Part 2: Pandas

---

# 13. Pandas Quick Reference (Summary of Pandas.md)

---

> **Canonical source:** [Pandas -- Comprehensive Reference](Pandas.md) covers all of this in depth, with 37 sections, the pandas 2.x/3.0 Copy-on-Write and PyArrow changes, and 15 interview questions. This section is a one-page refresher; follow the links for detail. Practice: [SQL and Pandas Exercises](../practice/SQL_and_Pandas_Exercises.md).

## 13.1 Core Objects

| Object | What it is | Key facts | Deep dive |
|---|---|---|---|
| `Series` | 1-D labeled array (values + `Index`) | Arithmetic **aligns by label**, not position; mismatched labels produce NaN | [§2 Series](Pandas.md#2-series) |
| `DataFrame` | 2-D table: dict of column Series sharing one row `Index` | Columns can have different dtypes; storage is per-column blocks (NumPy or Arrow) | [§3 DataFrame](Pandas.md#3-dataframe) |
| `Index` / `MultiIndex` | Immutable, hashable labels with a hash table for O(1) lookup | Drives alignment, joins, and `groupby` keys | [§4 Index and MultiIndex](Pandas.md#4-index-and-multiindex) |
| dtypes | NumPy (`int64`, `float64`, `object`, `datetime64[ns]`) vs extension (`Int64`, `string`, `category`, `ArrowDtype`) | Capitalized nullable dtypes use `pd.NA`; PyArrow strings are far smaller than `object` | [§5 dtypes](Pandas.md#5-the-pandas-dtype-system), [§7 PyArrow](Pandas.md#7-pyarrow-backend) |
| `GroupBy` | Lazy split object returned by `df.groupby(keys)` | Nothing is computed until `agg`/`transform`/`filter`/`apply` | [§18 GroupBy](Pandas.md#18-groupby-split-apply-combine) |

## 13.2 Top 15 Operations

| # | Task | Idiom | See |
|---|---|---|---|
| 1 | Inspect | `df.info(memory_usage='deep')`, `df.describe()`, `df.dtypes` | [§3](Pandas.md#3-dataframe) |
| 2 | Select by label | `df.loc[row_mask, ['a', 'b']]` (slices **inclusive**) | [§8](Pandas.md#8-the-four-indexers) |
| 3 | Select by position | `df.iloc[:10, 0:2]` (slices exclusive) | [§8](Pandas.md#8-the-four-indexers) |
| 4 | Filter rows | `df[(df.a > 1) & (df.b == 'x')]` or `df.query('a > 1 and b == "x"')` | [§9](Pandas.md#9-boolean-selection-query-eval-where-mask) |
| 5 | Missing data | `isna()`, `fillna({'a': 0})`, `dropna(subset=['a'])`, `ffill()` | [§6](Pandas.md#6-missing-data-semantics) |
| 6 | Convert types | `astype({'id': 'Int64'})`, `pd.to_numeric(errors='coerce')`, `pd.to_datetime` | [§13](Pandas.md#13-type-conversion) |
| 7 | String ops | `s.str.strip().str.lower()`, `s.str.extract(r'(\d+)')` | [§14](Pandas.md#14-the-str-accessor) |
| 8 | Low-cardinality strings | `astype('category')` (or ordered `CategoricalDtype`) | [§16](Pandas.md#16-categorical-deep-dive) |
| 9 | Derived columns | `df.assign(c=lambda d: d.a * 2)`, `np.where`, `np.select` | [§17](Pandas.md#17-transformation-toolkit) |
| 10 | Aggregate per group | `df.groupby('k').agg(total=('v', 'sum'), n=('v', 'size'))` | [§20](Pandas.md#20-named-aggregations-crosstab-pivot_table) |
| 11 | Broadcast group stat to rows | `df.groupby('k')['v'].transform('mean')` | [§19](Pandas.md#19-agg-vs-transform-vs-filter-vs-apply) |
| 12 | Join tables | `pd.merge(l, r, on='id', how='left', validate='m:1', indicator=True)` | [§24](Pandas.md#24-merge-and-join) |
| 13 | Stack frames | `pd.concat(list_of_dfs, ignore_index=True)` (collect, then concat once) | [§23](Pandas.md#23-concat) |
| 14 | Reshape | `pivot_table(index, columns, values, aggfunc)`, `melt(id_vars=...)` | [§22](Pandas.md#22-reshaping-pivot-melt-stack-unstack) |
| 15 | Time series | `s.resample('ME').sum()`, `s.rolling(7).mean()`, `s.shift(1)` | [§28](Pandas.md#28-date-ranges-resampling-shifting-windows), [§21](Pandas.md#21-window-functions) |

I/O in one line: prefer Parquet (`read_parquet(columns=...)`) over CSV. For CSVs larger than memory, use `read_csv(usecols=, dtype=, chunksize=)` ([§30 I/O Formats](Pandas.md#30-io-formats)).

## 13.3 Key Pitfalls

1. **Chained assignment.** `df[mask]['b'] = 0` may silently do nothing. Under Copy-on-Write (default in pandas 3.0) it never modifies `df`. Write `df.loc[mask, 'b'] = 0`. See [§11 Copy-on-Write](Pandas.md#11-copy-on-write-views-and-settingwithcopywarning).
2. **NaN turns int columns into float.** Use nullable `Int64` or `dtype_backend='pyarrow'`.
3. **`NaN != NaN`.** Never test missing values with `==`; use `isna()`.
4. **Merge key dtype mismatch** (`int64` vs `object`) returns zero matches with no error. Many-to-many keys silently explode the row count, so use `validate=`.
5. **`apply(axis=1)` is a Python loop.** Use vectorized column math, `np.select`, `map(dict)`, or built-in groupby aggregations ([§32 Performance](Pandas.md#32-performance)).
6. **`df = pd.concat([df, row])` in a loop is O(n²).** Accumulate a list, then call `concat` once.
7. **`inplace=True` saves no memory** and breaks chaining. Reassign instead.
8. **`loc` slices include the end label**; `iloc` slices exclude the end.
9. **pandas 2.2 frequency aliases:** `'M'`/`'Q'`/`'Y'` → `'ME'`/`'QE'`/`'YE'`, and `'H'`/`'T'`/`'S'` → `'h'`/`'min'`/`'s'`.
10. **`object` string columns are memory hogs.** Use `string[pyarrow]` or `category` ([§33 Memory Optimization](Pandas.md#33-memory-optimization)).

Interview questions on pandas (loc vs iloc, split-apply-combine, merge/join/concat, Categorical, out-of-core CSV, pivot vs pivot_table, Copy-on-Write, NaN vs NA, merge_asof, resample) are answered in [Pandas.md §37.2](Pandas.md#372-interview-questions).

---

# Part 3: SciPy, Plotting, and Tooling Libraries

---

# 14. SciPy Essentials

---

SciPy builds on NumPy with compiled algorithms (Fortran/C/C++) for sparse linear algebra, optimization, statistics, signal processing, interpolation, integration, and spatial queries. Interviews mostly probe **sparse formats**, `optimize`, and `stats`.

## 14.1 scipy.sparse -- Formats

A matrix with nnz non-zeros out of n×m entries is worth storing sparsely when nnz/(n·m) is roughly below 5-10%. Below that density, the index overhead is outweighed by skipping zeros.

| Format | Storage | Strengths | Weaknesses | Typical use |
|---|---|---|---|---|
| **COO** (coordinate) | `row[nnz]`, `col[nnz]`, `data[nnz]` | Fastest to build; duplicates allowed (summed on conversion) | No efficient slicing or arithmetic | Assemble from triplets, then convert |
| **CSR** (compressed sparse row) | `indptr[n_rows+1]`, `indices[nnz]`, `data[nnz]` | Fast row slicing, fast SpMV `A @ x`, fast row-wise ops | Changing the sparsity pattern is O(nnz); column slicing is slow | Default compute format; ML feature matrices |
| **CSC** (compressed sparse column) | `indptr[n_cols+1]`, `indices[nnz]`, `data[nnz]` | Fast column slicing, `A.T @ x`; preferred by direct solvers (SuperLU) | Row slicing slow | `spsolve`, column-oriented algorithms |
| **LIL** / **DOK** | Row lists / dict of keys | O(1)-ish incremental element insertion | Slow arithmetic, high memory | Building incrementally, then `.tocsr()` |
| **DIA** | Diagonals × offsets | Compact for banded matrices | Only banded patterns | Finite-difference stencils |
| **BSR** | Dense r×c blocks in CSR layout | Uses dense block kernels | Wasted space if blocks aren't dense | FEM with multiple DOF per node |

**Worked CSR example.**

```text
A = [[10, 0, 0, 2],
     [ 0, 0, 3, 0],
     [ 0, 4, 0, 0]]

data    = [10, 2, 3, 4]      # non-zeros, row by row
indices = [ 0, 3, 2, 1]      # column of each non-zero
indptr  = [ 0, 2, 3, 4]      # row i occupies data[indptr[i]:indptr[i+1]]
```

Memory with float64 values and int32 indices: `12·nnz + 4·(n_rows + 1)` bytes. For a 10⁶ × 10⁶ matrix with 10⁷ non-zeros that is ~124 MB, vs 8 TB dense.

```python
import numpy as np
from scipy import sparse

# Build from COO triplets (duplicates are summed when converting)
row = np.array([0, 0, 1, 2, 0])
col = np.array([0, 3, 2, 1, 0])
val = np.array([4.0, 2.0, 3.0, 4.0, 6.0])        # (0,0) appears twice: 4 + 6 = 10
A = sparse.coo_array((val, (row, col)), shape=(3, 4)).tocsr()
print(A.data, A.indices, A.indptr)                # [10. 2. 3. 4.] [0 3 2 1] [0 2 3 4]
print(A.toarray())

x = np.ones(4)
print(A @ x)                                      # SpMV: [12.  3.  4.]
print(A[1].toarray(), A.nnz)                      # row slice is cheap in CSR

# Sparse arrays (csr_array, SciPy >= 1.8) follow NumPy semantics: * is element-wise, @ is matmul.
# Legacy csr_matrix uses * for matmul -- a frequent source of bugs when mixing the two.
print((A * A).toarray()[0])                       # element-wise square: [100. 0. 0. 4.]

# Solve a sparse linear system (tridiagonal Poisson matrix)
from scipy.sparse.linalg import spsolve
n = 5
T = sparse.diags_array([-1.0, 2.0, -1.0], offsets=[-1, 0, 1], shape=(n, n), format='csc')
b = np.ones(n)
u = spsolve(T, b)
assert np.allclose(T @ u, b)
print(u)                                          # [2.5 4.  4.5 4.  2.5]
```

Other workhorses: `scipy.sparse.linalg.cg` / `gmres` (iterative solvers for huge systems), `eigsh` (a few eigenpairs of a large symmetric matrix), and `scipy.sparse.csgraph` (shortest paths, connected components on adjacency matrices). GPU equivalents live in `cupyx.scipy.sparse` (backed by rocSPARSE/cuSPARSE).

## 14.2 scipy.optimize

```python
import numpy as np
from scipy import optimize

# Unconstrained / bound-constrained minimization
def rosen(p):
    x, y = p
    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2

res = optimize.minimize(rosen, x0=[-1.2, 1.0], method='L-BFGS-B',
                        bounds=[(-2, 2), (-2, 2)])
print(res.success, res.x.round(4))                # True [1. 1.]

# Scalar root finding with a bracket (Brent's method: guaranteed convergence)
r = optimize.root_scalar(lambda x: x ** 3 - 2 * x - 5, bracket=[2, 3], method='brentq')
print(round(r.root, 6))                           # 2.094551

# Curve fitting: fit y = a * exp(-b * x) + c
rng = np.random.default_rng(0)
xs = np.linspace(0, 4, 50)
ys = 2.5 * np.exp(-1.3 * xs) + 0.5 + rng.normal(scale=0.02, size=xs.size)
popt, pcov = optimize.curve_fit(lambda x, a, b, c: a * np.exp(-b * x) + c, xs, ys, p0=[1, 1, 0])
print(popt.round(2))                              # ~[2.5 1.3 0.5]
print(np.sqrt(np.diag(pcov)).round(3))            # 1-sigma parameter uncertainties

# Linear programming (HiGHS solver): maximize x + 2y s.t. x + y <= 4, x <= 3, y <= 3
lp = optimize.linprog(c=[-1, -2], A_ub=[[1, 1]], b_ub=[4], bounds=[(0, 3), (0, 3)], method='highs')
print(lp.x, -lp.fun)                              # [1. 3.] 7.0
```

| Need | Function | Notes |
|---|---|---|
| Smooth minimization, many variables | `minimize(method='L-BFGS-B')` | Supply `jac=` for speed and accuracy; supports bounds |
| Constraints (eq/ineq) | `minimize(method='SLSQP' or 'trust-constr')` | |
| Noisy or non-smooth objective | `method='Nelder-Mead'`, `differential_evolution` | Derivative-free; slower |
| 1-D root | `root_scalar(method='brentq', bracket=...)` | Needs a sign change in the bracket |
| Nonlinear least squares | `least_squares`, `curve_fit` | `curve_fit` returns the covariance of the parameters |
| LP / MILP | `linprog(method='highs')`, `milp` | HiGHS is the default backend |

## 14.3 scipy.stats

Relevant for benchmark analysis: "is kernel B really faster than kernel A?"

```python
import numpy as np
from scipy import stats

print(stats.norm.cdf(1.96).round(4), stats.norm.ppf(0.975).round(4))   # 0.975 1.96

rng = np.random.default_rng(1)
a = rng.normal(10.0, 0.5, size=30)                 # runtimes (ms) of kernel A
b = rng.normal(9.7, 0.8, size=30)                  # kernel B

t = stats.ttest_ind(a, b, equal_var=False)         # Welch's t-test (unequal variances)
u = stats.mannwhitneyu(a, b)                       # rank-based; robust to outliers/skew
print(t.pvalue < 0.05, u.pvalue < 0.05)            # False True -- tests can disagree on borderline data

# Bootstrap a 95% confidence interval for the median speedup
res = stats.bootstrap((a, b), lambda x, y: np.median(x) / np.median(y),
                      n_resamples=2000, paired=False, random_state=0)
ci = res.confidence_interval
print(round(ci.low, 3), round(ci.high, 3))         # ~1.004 1.078 -> CI excludes 1.0: B is faster

print(stats.describe(a).mean.round(2), stats.iqr(a).round(3))
```

| Distribution method | Meaning |
|---|---|
| `pdf` / `pmf` | Density / mass at x |
| `cdf` / `sf` | P(X ≤ x) / P(X > x) (`sf` is more accurate in the far tail than `1 - cdf`) |
| `ppf` / `isf` | Inverse cdf (quantiles) / inverse sf |
| `rvs(size, random_state)` | Sample |
| `fit(data)` | Maximum-likelihood parameter estimates |

Benchmark-statistics rule of thumb: timing distributions are right-skewed with outliers (interrupts, clock ramps), so report the median and IQR and prefer rank tests or bootstrap CIs over a plain t-test. See [Performance Engineering -- Benchmarking Rigor](../computer-science/Performance_Engineering.md#8-benchmarking-rigor).

## 14.4 Interview Questions

**Q1.** CSR vs CSC vs COO -- which do you use when?

Build in COO (or LIL/DOK for incremental inserts) because it is cheap to append triplets, and duplicates get summed. Convert once to CSR for row slicing and `A @ x` (SpMV streams `data`/`indices` contiguously per row), or to CSC for column access and direct solvers. Never change the sparsity pattern of a CSR/CSC matrix in a loop: each insertion shifts the arrays (O(nnz)), and SciPy warns with `SparseEfficiencyWarning`.

**Q2.** Why is SpMV memory-bound, and what is its arithmetic intensity?

Per non-zero, CSR SpMV reads one value (8 B), one column index (4 B), and one gathered `x[j]` (8 B, often a cache miss), then does 2 FLOPs (multiply + add). That is ≈ 2 FLOP / 20 B = 0.1 FLOP/byte, far left of the [roofline](../computer-science/Performance_Engineering.md#3-roofline-model) ridge point on any CPU or GPU, so performance is set by memory bandwidth and the locality of `x`. Reordering (RCM), blocking (BSR), or formats like ELL/SELL-C-σ on GPUs improve it.

**Q3.** `csr_matrix * csr_matrix` and `csr_array * csr_array` give different results. Why?

The legacy `*_matrix` classes mimic `np.matrix`, where `*` is matrix multiplication. The newer `*_array` classes (SciPy ≥ 1.8; preferred) follow ndarray semantics, where `*` is element-wise and `@` is matmul. Use `@` everywhere to be unambiguous.

**Q4.** How would you decide whether a 3% runtime improvement between two kernel versions is real?

Collect many runs of each, interleaved to cancel drift, after warmup, with fixed clocks if possible. Look at the distributions (median, IQR). Test with Mann-Whitney U, or compute a bootstrap CI of the median ratio. If the CI of the ratio excludes 1.0 and the effect exceeds run-to-run noise, it's real. A t-test assumes approximately normal means; with skewed timings and n ≈ 30 it is less reliable.

---

# 15. matplotlib Essentials

---

## 15.1 The Object Model: Figure, Axes, Artists

| Object | What it is |
|---|---|
| `Figure` | The whole canvas (size, DPI, saving); contains one or more Axes |
| `Axes` | One plot area with its own x/y `Axis`, title, legend, and data artists |
| `Axis` | The tick/label machinery of one dimension (`ax.xaxis`) |
| `Artist` | Everything drawn: `Line2D`, `Text`, `Patch`, `Collection`, ... |

There are two APIs:

- **pyplot (implicit, state machine):** `plt.plot(...)`, `plt.title(...)` act on the "current" figure/axes. Fine for a quick look in a notebook, confusing with multiple subplots.
- **Object-oriented (explicit):** `fig, ax = plt.subplots()` then `ax.plot(...)`, `ax.set(...)`. **Use this in scripts, libraries, and interviews.**

```python
import matplotlib
matplotlib.use('Agg')                        # headless backend: servers, CI, containers
import matplotlib.pyplot as plt
import numpy as np

# Roofline model: attainable = min(peak_compute, bandwidth * arithmetic_intensity)
peak_tflops, bw_tbs = 100.0, 5.0              # illustrative machine: 100 TFLOP/s, 5 TB/s
ridge = peak_tflops / bw_tbs                  # 20 FLOP/byte
ai = np.logspace(-2, 3, 200)                  # FLOP/byte
roof = np.minimum(peak_tflops, bw_tbs * ai)

kernels = {'SpMV': 0.1, 'stencil': 0.5, 'GEMM': 150.0}
measured = {'SpMV': 0.4, 'stencil': 2.0, 'GEMM': 78.0}

fig, ax = plt.subplots(figsize=(6, 4), layout='constrained')
ax.loglog(ai, roof, linewidth=2, label='roofline')
for name, x in kernels.items():
    ax.plot(x, measured[name], marker='o', markersize=8, linestyle='none')
    ax.annotate(name, (x, measured[name]), textcoords='offset points', xytext=(6, -12))
ax.axvline(ridge, linestyle=':', color='gray')
ax.set(xlabel='Arithmetic intensity (FLOP/byte)', ylabel='Performance (TFLOP/s)',
       title=f'Roofline (ridge point = {ridge:.0f} FLOP/byte)')
ax.grid(True, which='major', alpha=0.3)
ax.legend(loc='lower right')
fig.savefig('roofline.png', dpi=150)
plt.close(fig)                               # free memory when generating many figures
print('saved roofline.png')
```

```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Small multiples share axes so panels are comparable
fig, axes = plt.subplots(2, 2, figsize=(8, 6), sharex=True, sharey=True, layout='constrained')
x = np.linspace(0, 2 * np.pi, 100)
for ax, k in zip(axes.flat, range(1, 5)):
    ax.plot(x, np.sin(k * x))
    ax.set_title(f'sin({k}x)')
fig.supxlabel('x'); fig.supylabel('amplitude')
fig.savefig('grid.png')
plt.close(fig)

# Heatmap with a single-hue sequential colormap and a labeled colorbar
data = np.random.default_rng(0).random((8, 12))
fig, ax = plt.subplots(layout='constrained')
im = ax.imshow(data, cmap='Blues', aspect='auto')
fig.colorbar(im, ax=ax, label='utilization')
fig.savefig('heatmap.png')
plt.close(fig)
```

## 15.2 Practical Rules

| Rule | Why |
|---|---|
| Use `fig, ax = plt.subplots()` and call methods on `ax` | Explicit, composable, works with many subplots |
| `matplotlib.use('Agg')` (or `MPLBACKEND=Agg`) on servers | No display needed; avoids Tk/Qt errors in CI |
| `plt.close(fig)` in loops | pyplot keeps references to every open figure (memory leak, warning after 20) |
| `layout='constrained'` (or `bbox_inches='tight'` when saving) | Prevents clipped labels |
| Log scales for spans over orders of magnitude | Rooflines, latency distributions, scaling plots |
| One y-axis per chart; avoid `ax.twinx()` | Dual axes imply false correlations; use two panels or index both series |
| Sequential data → single-hue colormap (`Blues`, `viridis`); signed data → diverging (`RdBu`) centered at 0 | Rainbow colormaps (`jet`) create false boundaries and fail for colorblind readers |
| Vector (`.svg`, `.pdf`) for documents, PNG at 150-300 dpi for slides | Crisp text at any zoom |
| Many points (≥ 10⁵) → `ax.hexbin` / `hist2d` or `rasterized=True` | Scatter of millions of points is slow and saturates |

The roofline example above is explained in [Performance Engineering -- Roofline Model](../computer-science/Performance_Engineering.md#3-roofline-model).

pandas `.plot` is a thin wrapper that returns an `Axes`, so you can keep customizing it with the same API ([Pandas §31](Pandas.md#31-plotting-and-styling)).

## 15.3 Interview Questions

**Q1.** What is the difference between `plt.plot` and `ax.plot`?

`plt.plot` uses pyplot's global "current axes" (creating a figure if none exists). `ax.plot` targets a specific `Axes` object. In library or multi-panel code, the implicit state leads to drawing on the wrong subplot and to leaked figures, so the OO API is the recommended style. Everything pyplot does is ultimately a method call on a `Figure` or `Axes`.

**Q2.** A report-generation service that renders thousands of PNGs slowly runs out of memory. Likely cause?

Figures created through `plt.subplots()`/`plt.figure()` are registered with pyplot's figure manager and are never garbage-collected until `plt.close(fig)` (or `plt.close('all')`). Close each figure after `savefig`, or create figures with `matplotlib.figure.Figure()` directly (not registered with pyplot) and use the Agg backend.

---

# 16. pydantic v2 -- Data Validation

---

pydantic parses and validates data using Python type hints. v2 (2023+) rewrote the core in Rust (`pydantic-core`), making validation roughly 5-50x faster than v1, and renamed most of the API.

```python
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator

class KernelRun(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)    # reject unknown keys; immutable

    name: str = Field(min_length=1)
    arch: Literal['gfx90a', 'gfx942', 'gfx950']
    grid: tuple[int, int, int]
    block: int = Field(gt=0, le=1024)
    duration_ns: float = Field(ge=0)
    tags: list[str] = []                                       # mutable defaults are copied per instance

    @field_validator('name')
    @classmethod
    def strip_name(cls, v: str) -> str:
        return v.strip()

    @model_validator(mode='after')
    def check_block_multiple_of_wavefront(self):
        if self.block % 64:
            raise ValueError('block size must be a multiple of the 64-wide wavefront')
        return self

run = KernelRun.model_validate(
    {'name': ' gemm ', 'arch': 'gfx942', 'grid': ['128', 1, 1], 'block': 256, 'duration_ns': '1530.5'})
print(run.name, run.grid, run.duration_ns)       # gemm (128, 1, 1) 1530.5  -- lax mode coerced '128'
print(run.model_dump_json())

try:
    KernelRun(name='x', arch='sm_90', grid=(1, 1, 1), block=100, duration_ns=-1, extra=1)
except ValidationError as e:
    print(e.error_count(), sorted({err['type'] for err in e.errors()}))
    # 3 ['extra_forbidden', 'greater_than_equal', 'literal_error']

# Strict mode disables coercion ('128' is no longer accepted for int)
class Strict(BaseModel):
    model_config = ConfigDict(strict=True)
    n: int
try:
    Strict(n='5')
except ValidationError as e:
    print(e.errors()[0]['type'])                 # int_type

# Validate non-model types with TypeAdapter
from pydantic import TypeAdapter
ta = TypeAdapter(list[int])
print(ta.validate_json('[1, "2", 3]'))           # [1, 2, 3]
```

The `ValidationError` lists 3 errors, and the `block=100` wavefront violation is **not** among them. All field errors are collected in one pass, but a `model_validator(mode='after')` runs only when every field validated successfully. Fix the field errors and resubmit, and the cross-field error appears.

| v1 | v2 |
|---|---|
| `class Config:` | `model_config = ConfigDict(...)` |
| `parse_obj(d)` / `parse_raw(s)` | `model_validate(d)` / `model_validate_json(s)` |
| `.dict()` / `.json()` | `.model_dump()` / `.model_dump_json()` |
| `@validator` / `@root_validator` | `@field_validator` / `@model_validator` |
| `orm_mode = True` | `from_attributes=True` |
| `copy(update=...)` | `model_copy(update=...)` |
| `BaseSettings` in pydantic | Separate package `pydantic-settings` |
| `__fields__` | `model_fields` |

| Concept | Detail |
|---|---|
| Lax vs strict | Default (lax) coerces `'5'` → `5`, `'true'` → `True`; `strict=True` (per model or `Field(strict=True)`) rejects them |
| `mode='before'` vs `'after'` validators | `before` sees raw input (normalize strings, unwrap envelopes); `after` sees typed values |
| `model_validate_json` | Parses JSON in Rust directly; faster than `json.loads` + `model_validate` |
| `model_construct()` | Skips validation (trusted data only) |
| Dataclasses | `pydantic.dataclasses.dataclass` validates standard dataclasses |
| Alternatives | `attrs`/`cattrs`, `msgspec` (very fast; struct + JSON/MsgPack), plain `dataclasses` (no validation) |

## 16.1 Interview Questions

**Q1.** Where should validation happen in a service, and why pydantic over hand-written checks?

At the **trust boundary**: HTTP request bodies, config files, CLI args, and messages from queues. Inside the boundary, code can assume typed, valid objects ("parse, don't validate"). pydantic derives validation, coercion, JSON-schema generation (`model_json_schema()`), and precise error reports from type hints, so the schema lives in one place. FastAPI uses it for request/response models and OpenAPI docs.

**Q2.** What is the difference between `field_validator` and `model_validator(mode='after')`?

A field validator runs per field (before or after type coercion) and can only see that field (plus previously validated fields via `info.data`). A model validator in `after` mode runs once all fields have validated and sees the whole instance, so it is the place for cross-field invariants (e.g. `start < end`, block size vs wavefront). It doesn't run if any field failed.

---

# 17. Command-Line Interfaces: click and typer

---

| Library | Style | Strengths | Notes |
|---|---|---|---|
| `argparse` (stdlib) | Imperative parser objects | No dependency | Verbose for nested subcommands; see [Python Fundamentals](Python_Fundamentals.md) |
| `click` | Decorators | Composable command groups, env-var support, prompts, testing via `CliRunner` | Mature; used by Flask, many tools |
| `typer` | Type hints (built on click) | Least boilerplate; `Annotated` metadata; shell completion | Same click machinery underneath |

```python
import click
from click.testing import CliRunner

@click.group()
@click.option('--verbose', '-v', count=True, help='Repeat for more output.')
@click.pass_context
def cli(ctx, verbose):
    """Toy profiler CLI."""
    ctx.obj = {'verbose': verbose}

@cli.command()
@click.argument('kernel')
@click.option('--iterations', '-n', default=10, show_default=True, type=click.IntRange(1, 10_000))
@click.option('--arch', type=click.Choice(['gfx90a', 'gfx942']), envvar='PROF_ARCH', required=True)
@click.pass_context
def run(ctx, kernel, iterations, arch):
    """Profile KERNEL for N iterations."""
    if ctx.obj['verbose']:
        click.echo(f'[debug] arch={arch}', err=True)
    click.echo(f'profiling {kernel} x{iterations} on {arch}')

runner = CliRunner()
result = runner.invoke(cli, ['run', 'gemm', '-n', '5', '--arch', 'gfx942'])
print(result.exit_code, result.output.strip())         # 0 profiling gemm x5 on gfx942
result = runner.invoke(cli, ['run', 'gemm'], env={'PROF_ARCH': 'gfx90a'})
print(result.output.strip())                            # profiling gemm x10 on gfx90a
result = runner.invoke(cli, ['run', 'gemm', '-n', '0', '--arch', 'gfx942'])
print(result.exit_code)                                 # 2 -- usage error (out of range)
```

```python
# Requires: pip install typer
from typing import Annotated
import typer
from typer.testing import CliRunner

app = typer.Typer()

@app.command()
def run(kernel: str,
        iterations: Annotated[int, typer.Option('--iterations', '-n', min=1)] = 10,
        dry_run: bool = False):
    """Profile KERNEL for N iterations."""
    typer.echo(f"{'would profile' if dry_run else 'profiling'} {kernel} x{iterations}")

@app.command()
def report(path: str):
    typer.echo(f'report for {path}')

result = CliRunner().invoke(app, ['run', 'gemm', '-n', '3', '--dry-run'])
print(result.exit_code, result.output.strip())          # 0 would profile gemm x3
```

With **two or more** `@app.command()` functions, typer creates subcommands. With exactly one, the app *is* that command (no subcommand name). That surprise trips people up. `bool` parameters become `--flag/--no-flag` pairs.

**CLI design checklist (frequent interview/design-review topic):** exit code 0 on success, non-zero on failure (click uses 2 for usage errors); data on stdout, diagnostics on stderr (`click.echo(..., err=True)`); `--help` text from docstrings; config precedence CLI flag > env var > config file > default; `--json` output mode for scripting; never prompt when stdin is not a TTY.

## 17.1 Interview Questions

**Q1.** How do you unit-test a CLI without spawning subprocesses?

Use `click.testing.CliRunner` (or `typer.testing.CliRunner`). `invoke(cli, args, env=..., input=...)` runs the command in-process with captured stdout/stderr, an isolated environment, and simulated stdin, and returns `exit_code`, `output`, and `exception`. `runner.isolated_filesystem()` gives a temp CWD for file-producing commands. Keep the business logic in plain functions and test those directly; test the CLI layer only for parsing and wiring.

**Q2.** click vs typer vs argparse -- what would you pick for a new internal tool?

argparse when zero dependencies matter (system scripts, minimal containers). typer for new tools: type hints double as parsing and validation, and you get completion and rich help for free. click when you need fine control (custom parameter types, lazy-loaded plugin subcommands, complex context passing). typer is built on click, so you can drop down when needed.

---

# 18. HTTP Clients: requests and httpx

---

| Feature | `requests` | `httpx` |
|---|---|---|
| Sync API | Yes | Yes (`httpx.get`, `httpx.Client`) |
| Async API | No | Yes (`httpx.AsyncClient`) |
| HTTP/2 | No | Yes (`pip install 'httpx[http2]'`, `http2=True`) |
| Default timeout | **None: waits forever** | 5 seconds |
| Redirects | Followed by default | **Not** followed by default (`follow_redirects=True`) |
| Connection pooling | `requests.Session` | `httpx.Client` / `AsyncClient` |
| Retries | `HTTPAdapter(max_retries=urllib3.Retry(...))` | `HTTPTransport(retries=n)` (connection errors only) or `tenacity` |
| Testing | `responses`, `requests-mock` | `httpx.MockTransport`, `respx` |

```python
# fragment -- needs network access
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()                      # reuses TCP/TLS connections (keep-alive)
retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[429, 502, 503, 504],
              allowed_methods=['GET', 'PUT', 'DELETE'])    # only retry idempotent methods
session.mount('https://', HTTPAdapter(max_retries=retry))

resp = session.get('https://api.example.com/runs', params={'limit': 10},
                   timeout=(3.05, 10))            # (connect, read) seconds -- ALWAYS set
resp.raise_for_status()                           # turn 4xx/5xx into exceptions
runs = resp.json()
```

```python
# Requires: pip install httpx  (runs offline thanks to MockTransport)
import asyncio
import httpx

def handler(request: httpx.Request) -> httpx.Response:
    run_id = request.url.path.rsplit('/', 1)[-1]
    if run_id == '404':
        return httpx.Response(404, json={'error': 'not found'})
    return httpx.Response(200, json={'id': run_id, 'status': 'done'})

transport = httpx.MockTransport(handler)

# Sync client
with httpx.Client(transport=transport, base_url='https://api.example.com', timeout=5.0) as client:
    r = client.get('/runs/7')
    print(r.status_code, r.json())                 # 200 {'id': '7', 'status': 'done'}
    try:
        client.get('/runs/404').raise_for_status()
    except httpx.HTTPStatusError as e:
        print('error:', e.response.status_code)    # error: 404

# Async client: bounded concurrency with a semaphore
async def fetch_all(ids, limit=10):
    sem = asyncio.Semaphore(limit)
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler),
                                 base_url='https://api.example.com') as client:
        async def one(i):
            async with sem:
                resp = await client.get(f'/runs/{i}')
                return resp.json()['id']
        return await asyncio.gather(*(one(i) for i in ids))

print(asyncio.run(fetch_all(range(5))))            # ['0', '1', '2', '3', '4']
```

## 18.1 Interview Questions

**Q1.** What are the most common production bugs with `requests`?

(1) **No timeout**: the default is to wait forever, so one hung server stalls a worker thread indefinitely. Always pass `timeout=(connect, read)`. (2) Not using a `Session`, so each call pays a new TCP + TLS handshake (tens of ms). (3) Forgetting `raise_for_status()`, so 500 pages get parsed as data. (4) Retrying non-idempotent POSTs, which duplicates side effects; retry only idempotent methods, or use idempotency keys. (5) Retrying without backoff or jitter, which causes thundering herds on 429/503. (6) Calling `requests` inside `async` code, which blocks the event loop; use `httpx.AsyncClient` or `aiohttp`.

**Q2.** You need to call an API 10,000 times. How do you make it fast but polite?

Use one pooled client (`httpx.AsyncClient` with `limits=httpx.Limits(max_connections=N)`, or a `requests.Session` in a thread pool). Bound concurrency with a semaphore sized to the server's rate limit, enable HTTP/2 if supported (multiplexing over one connection), honor `Retry-After` on 429 with exponential backoff and jitter, set timeouts, and stream results to disk incrementally. Batch endpoints, if the API offers them, beat all of the above.

---

# Part 4: PyQt

---

# 19. Qt Architecture and Core Concepts

---

## 19.1 What Is PyQt?

PyQt is a set of Python bindings for the **Qt** application framework (C++). It provides tools for building cross-platform desktop applications with native look and feel.

| Binding | Qt Version | License | Maintained By |
|---|---|---|---|
| PyQt5 | Qt 5 | GPL / Commercial | Riverbank Computing |
| PyQt6 | Qt 6 | GPL / Commercial | Riverbank Computing |
| PySide2 | Qt 5 | LGPL | Qt Company |
| PySide6 | Qt 6 | LGPL | Qt Company |

The APIs are nearly identical. Key PyQt6/PySide6 differences from PyQt5/PySide2:

| Change | PyQt5/PySide2 | PyQt6/PySide6 |
|---|---|---|
| Enums | `Qt.AlignCenter` | `Qt.AlignmentFlag.AlignCenter` |
| `exec_()` | `app.exec_()` | `app.exec()` |
| Signal/slot syntax | Same | Same (minor import differences) |

## 19.2 The Event Loop

Every Qt application requires exactly one `QApplication` instance and an event loop:

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow

app = QApplication(sys.argv)    # exactly one per process

window = QMainWindow()
window.setWindowTitle('Hello PyQt')
window.setGeometry(100, 100, 800, 600)  # x, y, width, height
window.show()

sys.exit(app.exec())   # start event loop -- blocks until app quits
```

```
Event Loop Flow:

  ┌─────────────────────────────────┐
  │         Event Queue             │
  │  [mouse click] [key press] ... │
  └───────────────┬─────────────────┘
                  │ dequeue
                  ▼
          ┌───────────────┐
          │ Event Dispatch│
          └───────┬───────┘
                  │ deliver to target widget
                  ▼
          ┌───────────────┐
          │ Event Handler │──▶ Signals emitted
          └───────────────┘      │
                                 ▼
                          ┌─────────────┐
                          │ Slot Called  │
                          └─────────────┘
```

## 19.3 Widget Hierarchy and Ownership

Qt uses a **parent-child** ownership model:

- Setting a parent (`QWidget(parent=self)`) transfers ownership
- When a parent is deleted, all children are automatically deleted
- Top-level widgets (no parent) become independent windows
- Children are drawn within their parent's coordinate space

```python
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        central = QWidget(self)       # parent = self → owned by MainWindow
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        label = QLabel('Hello', central)    # parent = central
        button = QPushButton('Click', central)

        layout.addWidget(label)
        layout.addWidget(button)
```

---

# 20. Widgets

---

## 20.1 Common Widgets Reference

| Widget | Purpose | Key Properties/Methods |
|---|---|---|
| `QLabel` | Display text or image | `setText()`, `setPixmap()`, `setAlignment()` |
| `QPushButton` | Clickable button | `clicked` signal, `setText()`, `setIcon()`, `setEnabled()` |
| `QLineEdit` | Single-line text input | `text()`, `setText()`, `textChanged` signal, `setPlaceholderText()` |
| `QTextEdit` | Multi-line rich text | `toPlainText()`, `setHtml()`, `append()` |
| `QPlainTextEdit` | Multi-line plain text | Faster than QTextEdit for large documents |
| `QComboBox` | Dropdown selector | `addItems()`, `currentText()`, `currentIndexChanged` signal |
| `QCheckBox` | Toggleable checkbox | `isChecked()`, `stateChanged` signal |
| `QRadioButton` | Mutually exclusive option | Group with `QButtonGroup` |
| `QSlider` | Slider control | `setValue()`, `value()`, `valueChanged` signal |
| `QSpinBox` | Integer selector with arrows | `setRange()`, `value()`, `valueChanged` signal |
| `QDoubleSpinBox` | Float selector with arrows | `setDecimals()`, `setSingleStep()` |
| `QProgressBar` | Progress indicator | `setValue()`, `setRange()` |
| `QTableWidget` | Editable table | `setItem()`, `item()`, `setRowCount()` |
| `QTreeWidget` | Tree view | `addTopLevelItem()`, `QTreeWidgetItem` |
| `QListWidget` | List of items | `addItem()`, `currentItem()`, `itemClicked` signal |
| `QTabWidget` | Tabbed pages | `addTab(widget, title)`, `currentChanged` signal |
| `QGroupBox` | Labeled grouping frame | `setTitle()`, contains layout with children |
| `QSplitter` | Resizable split panes | `addWidget()`, `setSizes()` |

## 20.2 Widget Construction Pattern

```python
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QComboBox, QCheckBox, QVBoxLayout
)
from PyQt6.QtCore import Qt

class FormWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Enter name...')

        self.combo = QComboBox()
        self.combo.addItems(['Option A', 'Option B', 'Option C'])

        self.check = QCheckBox('I agree to terms')

        self.submit = QPushButton('Submit')
        self.submit.setEnabled(False)

        self.check.stateChanged.connect(
            lambda state: self.submit.setEnabled(bool(state))
        )

        layout.addWidget(QLabel('Name:'))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel('Choose:'))
        layout.addWidget(self.combo)
        layout.addWidget(self.check)
        layout.addWidget(self.submit)
```

## 20.3 QTableWidget

```python
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem

table = QTableWidget(3, 2)   # 3 rows, 2 columns
table.setHorizontalHeaderLabels(['Name', 'Age'])

table.setItem(0, 0, QTableWidgetItem('Alice'))
table.setItem(0, 1, QTableWidgetItem('25'))
table.setItem(1, 0, QTableWidgetItem('Bob'))
table.setItem(1, 1, QTableWidgetItem('30'))

item = table.item(0, 0)
print(item.text())   # 'Alice'

table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # read-only
```

---

# 21. Layouts

---

## 21.1 Layout Types

| Layout | Description | Use Case |
|---|---|---|
| `QHBoxLayout` | Horizontal row | Toolbar, button row |
| `QVBoxLayout` | Vertical column | Form fields, stacked items |
| `QGridLayout` | Row-column grid | Complex forms, dashboards |
| `QFormLayout` | Label-field pairs | Settings, data entry forms |
| `QStackedLayout` | Overlapping pages | Wizard, tabbed content |

## 21.2 Layout Examples

```python
from PyQt6.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QGridLayout, QFormLayout,
    QPushButton, QLineEdit, QLabel
)

# Horizontal
h_layout = QHBoxLayout()
h_layout.addWidget(QPushButton('Left'))
h_layout.addWidget(QPushButton('Center'))
h_layout.addWidget(QPushButton('Right'))

# Vertical
v_layout = QVBoxLayout()
v_layout.addWidget(QLabel('Top'))
v_layout.addWidget(QLabel('Bottom'))

# Grid
grid = QGridLayout()
grid.addWidget(QLabel('Row 0, Col 0'), 0, 0)
grid.addWidget(QLabel('Row 0, Col 1'), 0, 1)
grid.addWidget(QLabel('Row 1, Col 0-1'), 1, 0, 1, 2)  # spans 2 columns

# Form
form = QFormLayout()
form.addRow('Name:', QLineEdit())
form.addRow('Email:', QLineEdit())
form.addRow('Age:', QLineEdit())
```

## 21.3 Stretch and Spacing

```python
layout = QHBoxLayout()
layout.addWidget(QPushButton('Fixed'))
layout.addStretch(1)                    # expandable space
layout.addWidget(QPushButton('Right-aligned'))

layout.setSpacing(10)         # space between widgets
layout.setContentsMargins(20, 10, 20, 10)  # left, top, right, bottom
```

## 21.4 Size Policies

Size policies control how widgets behave when the layout has extra or insufficient space:

| Policy | Description |
|---|---|
| `Fixed` | Widget cannot grow or shrink beyond sizeHint |
| `Minimum` | sizeHint is minimum; can grow |
| `Maximum` | sizeHint is maximum; can shrink |
| `Preferred` | sizeHint is preferred; can grow or shrink |
| `Expanding` | Can grow; wants extra space |
| `MinimumExpanding` | sizeHint is minimum; wants extra space |
| `Ignored` | sizeHint is ignored; takes as much as possible |

```python
from PyQt6.QtWidgets import QSizePolicy

button = QPushButton('Click')
button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
```

## 21.5 Nesting Layouts

```python
main_layout = QVBoxLayout()

top_bar = QHBoxLayout()
top_bar.addWidget(QLabel('Title'))
top_bar.addStretch()
top_bar.addWidget(QPushButton('Settings'))

content = QGridLayout()
content.addWidget(QLabel('Cell 1'), 0, 0)
content.addWidget(QLabel('Cell 2'), 0, 1)

main_layout.addLayout(top_bar)
main_layout.addLayout(content)
```

---

# 22. Signals and Slots

---

## 22.1 Core Concept

Signals and slots are Qt's mechanism for communication between objects. A **signal** is emitted when something happens; a **slot** is a function that gets called in response.

```
  ┌──────────┐   signal emitted    ┌──────────┐
  │  Sender  │ ──────────────────▶ │ Receiver │
  │  Widget  │   (e.g. clicked)    │  (Slot)  │
  └──────────┘                     └──────────┘
```

## 22.2 Connection Syntax

```python
button = QPushButton('Click me')

button.clicked.connect(self.on_button_clicked)

def on_button_clicked(self):
    print('Button was clicked!')
```

**Connecting with lambda (for passing arguments):**

```python
for i in range(5):
    btn = QPushButton(f'Button {i}')
    btn.clicked.connect(lambda checked, num=i: self.handle_click(num))
```

**Connecting to multiple slots:**

```python
button.clicked.connect(self.update_label)
button.clicked.connect(self.log_action)
button.clicked.connect(self.play_sound)
```

**Disconnecting:**

```python
button.clicked.disconnect(self.on_button_clicked)
button.clicked.disconnect()   # disconnect all slots
```

## 22.3 Custom Signals

```python
from PyQt6.QtCore import pyqtSignal, QObject

class Worker(QObject):
    progress = pyqtSignal(int)              # emits an int
    finished = pyqtSignal()                 # no arguments
    result = pyqtSignal(str, int)           # multiple arguments
    data_ready = pyqtSignal(object)         # any Python object

    def do_work(self):
        for i in range(100):
            self.progress.emit(i)
        self.result.emit("done", 42)
        self.finished.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = Worker()
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.on_complete)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def on_complete(self):
        print('Work finished!')
```

## 22.4 Built-in Signals Reference

| Widget | Signal | Emitted When |
|---|---|---|
| `QPushButton` | `clicked` | Button clicked |
| `QLineEdit` | `textChanged(str)` | Text modified |
| `QLineEdit` | `returnPressed` | Enter key pressed |
| `QComboBox` | `currentIndexChanged(int)` | Selection changes |
| `QComboBox` | `currentTextChanged(str)` | Selection text changes |
| `QCheckBox` | `stateChanged(int)` | Check state changes |
| `QSlider` | `valueChanged(int)` | Value changes |
| `QSpinBox` | `valueChanged(int)` | Value changes |
| `QTabWidget` | `currentChanged(int)` | Active tab changes |
| `QListWidget` | `itemClicked(QListWidgetItem)` | Item clicked |
| `QTableWidget` | `cellChanged(int, int)` | Cell content changes |

---

# 23. Dialogs and Menus

---

## 23.1 Standard Dialogs

```python
from PyQt6.QtWidgets import QMessageBox, QFileDialog, QInputDialog, QColorDialog

# Message Box
QMessageBox.information(self, 'Title', 'This is informational.')
QMessageBox.warning(self, 'Warning', 'Something went wrong.')
QMessageBox.critical(self, 'Error', 'Fatal error occurred.')

reply = QMessageBox.question(self, 'Confirm', 'Are you sure?',
    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
if reply == QMessageBox.StandardButton.Yes:
    print('Confirmed')

# File Dialog
path, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'CSV Files (*.csv);;All (*)')
path, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'PNG (*.png)')
directory = QFileDialog.getExistingDirectory(self, 'Select Directory')

# Input Dialog
text, ok = QInputDialog.getText(self, 'Input', 'Enter your name:')
number, ok = QInputDialog.getInt(self, 'Input', 'Enter age:', min=0, max=150)
item, ok = QInputDialog.getItem(self, 'Input', 'Pick one:', ['A', 'B', 'C'])

# Color Dialog
color = QColorDialog.getColor()
if color.isValid():
    print(color.name())   # '#ff0000'
```

## 23.2 Custom Dialog

```python
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QFormLayout

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Settings')

        layout = QFormLayout(self)

        self.name_edit = QLineEdit()
        self.age_spin = QSpinBox()
        self.age_spin.setRange(0, 150)

        layout.addRow('Name:', self.name_edit)
        layout.addRow('Age:', self.age_spin)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

# Usage:
dialog = SettingsDialog(self)
if dialog.exec() == QDialog.DialogCode.Accepted:
    name = dialog.name_edit.text()
    age = dialog.age_spin.value()
```

## 23.3 Menus and Toolbars

```python
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QAction, QIcon, QKeySequence

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Menu Bar
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('&File')

        open_action = QAction('&Open', self)
        open_action.setShortcut(QKeySequence('Ctrl+O'))
        open_action.setStatusTip('Open a file')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction('&Save', self)
        save_action.setShortcut(QKeySequence('Ctrl+S'))
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        exit_action = QAction('E&xit', self)
        exit_action.setShortcut(QKeySequence('Ctrl+Q'))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Toolbar
        toolbar = self.addToolBar('Main')
        toolbar.addAction(open_action)
        toolbar.addAction(save_action)

        # Status Bar
        self.statusBar().showMessage('Ready')

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open')
        if path:
            self.statusBar().showMessage(f'Opened: {path}')

    def save_file(self):
        self.statusBar().showMessage('Saved')
```

---

# 24. Model/View Architecture

---

## 24.1 Overview

Qt's Model/View separates data (Model) from presentation (View). This allows the same data to be displayed in multiple views and swapping models without changing view code.

```
  ┌─────────┐     ┌──────────┐     ┌──────────┐
  │  Model  │◀───▶│ Delegate │◀───▶│   View   │
  │ (data)  │     │(rendering│     │(display) │
  │         │     │ & editing)│     │          │
  └─────────┘     └──────────┘     └──────────┘
```

| Component | Role | Examples |
|---|---|---|
| **Model** | Stores/manages data | `QStandardItemModel`, `QSqlTableModel`, custom `QAbstractItemModel` |
| **View** | Displays data | `QTableView`, `QListView`, `QTreeView` |
| **Delegate** | Customizes rendering/editing | `QStyledItemDelegate`, custom delegates |

## 24.2 QStandardItemModel

```python
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QTableView

model = QStandardItemModel(4, 3)   # 4 rows, 3 columns
model.setHorizontalHeaderLabels(['Name', 'Age', 'City'])

model.setItem(0, 0, QStandardItem('Alice'))
model.setItem(0, 1, QStandardItem('25'))
model.setItem(0, 2, QStandardItem('NYC'))

view = QTableView()
view.setModel(model)
```

## 24.3 Custom Model (QAbstractTableModel)

```python
from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex

class PandasModel(QAbstractTableModel):
    def __init__(self, df):
        super().__init__()
        self._df = df

    def rowCount(self, parent=QModelIndex()):
        return len(self._df)

    def columnCount(self, parent=QModelIndex()):
        return len(self._df.columns)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._df.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._df.columns[section]
            return str(self._df.index[section])
        return None

# Usage:
import pandas as pd
df = pd.DataFrame({'Name': ['Alice', 'Bob'], 'Age': [25, 30]})
model = PandasModel(df)
view = QTableView()
view.setModel(model)
```

## 24.4 Proxy Models (Sorting and Filtering)

```python
from PyQt6.QtCore import QSortFilterProxyModel

proxy = QSortFilterProxyModel()
proxy.setSourceModel(model)
proxy.setFilterKeyColumn(0)
proxy.setFilterFixedString('Alice')   # filter by name

view.setModel(proxy)
view.setSortingEnabled(True)          # click headers to sort

proxy.setFilterRegularExpression('A.*')  # regex filtering
```

## 24.5 Custom Delegate

```python
from PyQt6.QtWidgets import QStyledItemDelegate, QSpinBox

class SpinBoxDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QSpinBox(parent)
        editor.setRange(0, 150)
        return editor

    def setEditorData(self, editor, index):
        value = int(index.data())
        editor.setValue(value)

    def setModelData(self, editor, model, index):
        model.setData(index, str(editor.value()))

view.setItemDelegateForColumn(1, SpinBoxDelegate())   # age column uses spinbox
```

---

# 25. Custom Widgets and Painting

---

## 25.1 QPainter Basics

All custom drawing happens inside the `paintEvent` method using `QPainter`:

```python
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont
from PyQt6.QtCore import Qt, QRect

class CustomWidget(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Pen controls outlines
        pen = QPen(QColor('#333333'), 2)
        painter.setPen(pen)

        # Brush controls fills
        brush = QBrush(QColor('#4CAF50'))
        painter.setBrush(brush)

        # Draw shapes
        painter.drawRect(10, 10, 100, 60)          # rectangle
        painter.drawEllipse(120, 10, 80, 60)        # ellipse
        painter.drawLine(10, 90, 200, 90)           # line
        painter.drawRoundedRect(10, 100, 100, 60, 10, 10)  # rounded rect

        # Draw text
        painter.setFont(QFont('Arial', 14))
        painter.drawText(10, 190, 'Hello QPainter!')

        painter.end()
```

## 25.2 Coordinate System

```
(0,0) ────────────────▶ x (width)
  │
  │    Widget area
  │
  ▼
  y (height)
```

- Origin is top-left corner
- x increases rightward
- y increases downward
- `self.width()` and `self.height()` give the current widget dimensions

## 25.3 Drawing Primitives

| Method | Description |
|---|---|
| `drawPoint(x, y)` | Single pixel |
| `drawLine(x1, y1, x2, y2)` | Line segment |
| `drawRect(x, y, w, h)` | Rectangle |
| `drawRoundedRect(x, y, w, h, rx, ry)` | Rounded rectangle |
| `drawEllipse(x, y, w, h)` | Ellipse/circle |
| `drawArc(rect, startAngle, spanAngle)` | Arc (angles in 1/16 degree) |
| `drawPolygon(points)` | Polygon |
| `drawText(x, y, text)` | Text |
| `drawPixmap(x, y, pixmap)` | Image |
| `drawPath(QPainterPath)` | Complex path |

## 25.4 Custom Widget Example: Gauge

```python
from PyQt6.QtCore import pyqtSignal

class GaugeWidget(QWidget):
    valueChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0
        self._min = 0
        self._max = 100
        self.setMinimumSize(200, 200)

    def setValue(self, val):
        self._value = max(self._min, min(self._max, val))
        self.valueChanged.emit(self._value)
        self.update()   # triggers repaint

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        side = min(self.width(), self.height())
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200, side / 200)

        # Background arc
        painter.setPen(QPen(QColor('#E0E0E0'), 12, Qt.PenStyle.SolidLine,
                            Qt.PenCapStyle.RoundCap))
        painter.drawArc(QRect(-80, -80, 160, 160), 225 * 16, -270 * 16)

        # Value arc
        ratio = (self._value - self._min) / (self._max - self._min)
        span = int(-270 * ratio)
        painter.setPen(QPen(QColor('#4CAF50'), 12, Qt.PenStyle.SolidLine,
                            Qt.PenCapStyle.RoundCap))
        painter.drawArc(QRect(-80, -80, 160, 160), 225 * 16, span * 16)

        # Value text
        painter.setPen(QColor('#333333'))
        painter.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        painter.drawText(QRect(-50, -20, 100, 40),
                         Qt.AlignmentFlag.AlignCenter, str(self._value))

        painter.end()
```

---

# 26. Threading in Qt

---

## 26.1 The Golden Rule

**Never modify GUI widgets from any thread other than the main thread.** Qt widgets are not thread-safe. All GUI updates must happen on the main thread.

## 26.2 Worker Thread Pattern (Recommended)

The recommended approach: create a `QObject` worker, move it to a `QThread`, and communicate via signals/slots.

```python
from PyQt6.QtCore import QThread, QObject, pyqtSignal

class Worker(QObject):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def run(self):
        try:
            for i in range(100):
                import time
                time.sleep(0.05)
                self.progress.emit(i + 1)
            self.finished.emit('Done!')
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.thread = None
        self.worker = None

    def start_work(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def on_finished(self, result):
        self.statusBar().showMessage(result)
```

## 26.3 QThread Subclass Pattern (Simpler but Less Flexible)

```python
class DownloadThread(QThread):
    progress = pyqtSignal(int)
    result = pyqtSignal(bytes)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        import urllib.request
        response = urllib.request.urlopen(self.url)
        data = response.read()
        self.result.emit(data)

thread = DownloadThread('https://example.com/data')
thread.result.connect(self.handle_data)
thread.start()
```

## 26.4 Worker Pattern vs Subclass Pattern

| Aspect | Worker + moveToThread | QThread Subclass |
|---|---|---|
| Separation of concerns | Worker logic is decoupled | Logic mixed with thread management |
| Reusability | Worker can be moved to any thread | Tied to specific QThread subclass |
| Multiple tasks | Easy to have multiple workers | One task per thread class |
| Qt recommendation | **Preferred** | Acceptable for simple cases |
| Event loop in thread | Yes (can receive signals) | Only if `exec()` is called in `run()` |

## 26.5 QTimer

For periodic or delayed operations on the main thread (no threading needed):

```python
from PyQt6.QtCore import QTimer

timer = QTimer()
timer.timeout.connect(self.update_display)
timer.start(1000)   # fires every 1000ms

QTimer.singleShot(5000, self.delayed_action)   # one-shot after 5s
```

## 26.6 Thread Safety Rules

1. **GUI updates**: only from the main thread -- use signals to communicate results back
2. **Shared data**: protect with `QMutex` or `QReadWriteLock`
3. **Signal/slot connections**: cross-thread connections are automatically queued (thread-safe)
4. **QTimer**: must be started/stopped from the thread that created it

---

# 27. Styling

---

## 27.1 Qt Style Sheets (QSS)

QSS is similar to CSS and allows customizing widget appearance:

```python
button = QPushButton('Styled')
button.setStyleSheet('''
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
    QPushButton:pressed {
        background-color: #3d8b40;
    }
    QPushButton:disabled {
        background-color: #cccccc;
        color: #666666;
    }
''')
```

## 27.2 Selectors

| Selector | Syntax | Example |
|---|---|---|
| Type | `WidgetClass` | `QPushButton { ... }` |
| Object name | `#objectName` | `#submitBtn { ... }` |
| Class | `.className` | `.QPushButton { ... }` (exact type, no subclasses) |
| Descendant | `Parent Child` | `QDialog QPushButton { ... }` |
| Child | `Parent > Child` | `QFrame > QLabel { ... }` |
| Property | `[property="value"]` | `QPushButton[flat="true"] { ... }` |

```python
widget.setObjectName('submitBtn')
```

## 27.3 Pseudo-States

| Pseudo-State | Triggers When |
|---|---|
| `:hover` | Mouse is over the widget |
| `:pressed` | Widget is being clicked |
| `:checked` | Checkbox/radio is checked |
| `:unchecked` | Checkbox/radio is unchecked |
| `:disabled` | Widget is disabled |
| `:focus` | Widget has keyboard focus |
| `:selected` | Item is selected (list/tree/table) |
| `:open` | Combo box or menu is open |
| `:closed` | Combo box or menu is closed |

## 27.4 Application-Wide Styling

```python
app = QApplication(sys.argv)
app.setStyleSheet('''
    QMainWindow {
        background-color: #f5f5f5;
    }
    QLabel {
        color: #333333;
        font-family: "Segoe UI", Arial;
    }
    QLineEdit {
        border: 1px solid #cccccc;
        border-radius: 3px;
        padding: 5px;
    }
    QLineEdit:focus {
        border-color: #4CAF50;
    }
''')
```

## 27.5 Dark Theme Example

```python
DARK_THEME = '''
    QWidget {
        background-color: #1e1e1e;
        color: #d4d4d4;
        font-family: "Segoe UI", sans-serif;
        font-size: 13px;
    }
    QMainWindow {
        background-color: #1e1e1e;
    }
    QMenuBar {
        background-color: #2d2d2d;
        border-bottom: 1px solid #3d3d3d;
    }
    QMenuBar::item:selected {
        background-color: #094771;
    }
    QMenu {
        background-color: #2d2d2d;
        border: 1px solid #454545;
    }
    QMenu::item:selected {
        background-color: #094771;
    }
    QPushButton {
        background-color: #0e639c;
        color: white;
        border: none;
        padding: 6px 14px;
        border-radius: 3px;
    }
    QPushButton:hover {
        background-color: #1177bb;
    }
    QPushButton:pressed {
        background-color: #094771;
    }
    QLineEdit, QTextEdit, QPlainTextEdit {
        background-color: #3c3c3c;
        border: 1px solid #3c3c3c;
        border-radius: 3px;
        padding: 4px;
        color: #d4d4d4;
    }
    QLineEdit:focus, QTextEdit:focus {
        border-color: #007acc;
    }
    QTableView {
        background-color: #1e1e1e;
        alternate-background-color: #252525;
        gridline-color: #3d3d3d;
        selection-background-color: #094771;
    }
    QHeaderView::section {
        background-color: #2d2d2d;
        border: 1px solid #3d3d3d;
        padding: 4px;
    }
    QScrollBar:vertical {
        background-color: #1e1e1e;
        width: 12px;
    }
    QScrollBar::handle:vertical {
        background-color: #424242;
        border-radius: 6px;
        min-height: 20px;
    }
    QScrollBar::handle:vertical:hover {
        background-color: #555555;
    }
    QProgressBar {
        border: none;
        background-color: #3c3c3c;
        border-radius: 3px;
        text-align: center;
    }
    QProgressBar::chunk {
        background-color: #0e639c;
        border-radius: 3px;
    }
'''

app.setStyleSheet(DARK_THEME)
```

---

# 28. PyQt Common Patterns and Interview Questions

---

## 28.1 Common Patterns

**Pattern 1: Main Window Skeleton**

```python
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QPushButton, QStatusBar
)
from PyQt6.QtGui import QAction, QKeySequence

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('My Application')
        self.setMinimumSize(800, 600)

        self._create_menu_bar()
        self._create_central_widget()
        self._create_status_bar()

    def _create_menu_bar(self):
        menu = self.menuBar()
        file_menu = menu.addMenu('&File')

        exit_action = QAction('E&xit', self)
        exit_action.setShortcut(QKeySequence('Ctrl+Q'))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def _create_central_widget(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.addWidget(QLabel('Welcome!'))

    def _create_status_bar(self):
        self.statusBar().showMessage('Ready')

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
```

**Pattern 2: Settings Persistence with QSettings**

```python
from PyQt6.QtCore import QSettings

settings = QSettings('MyCompany', 'MyApp')

settings.setValue('window/geometry', self.saveGeometry())
settings.setValue('recent_files', ['/path/a', '/path/b'])

geometry = settings.value('window/geometry')
if geometry:
    self.restoreGeometry(geometry)

recent = settings.value('recent_files', defaultValue=[])
```

**Pattern 3: Drag and Drop**

```python
class DropWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            print(f'Dropped: {file_path}')
```

**Pattern 4: Undo/Redo with QUndoStack**

```python
from PyQt6.QtGui import QUndoStack, QUndoCommand

class ChangeTextCommand(QUndoCommand):
    def __init__(self, widget, old_text, new_text):
        super().__init__(f'Change text to "{new_text}"')
        self.widget = widget
        self.old_text = old_text
        self.new_text = new_text

    def redo(self):
        self.widget.setText(self.new_text)

    def undo(self):
        self.widget.setText(self.old_text)

undo_stack = QUndoStack()
undo_stack.push(ChangeTextCommand(label, 'old', 'new'))
undo_stack.undo()   # reverts to 'old'
undo_stack.redo()   # applies 'new' again
```

## 28.2 Interview Questions

**Q1: What is the difference between signals/slots and direct function calls?**

Signals and slots provide **loose coupling**: the emitter does not need to know about the receiver. Multiple slots can connect to one signal. Cross-thread connections are automatically queued for thread safety. Direct function calls create tight coupling and are not thread-safe by default.

**Q2: Why should you never update the GUI from a worker thread?**

Qt widgets are not thread-safe. Accessing them from multiple threads causes undefined behavior (crashes, corrupted state). The correct pattern is to emit signals from the worker thread, which are delivered to slots on the main thread via Qt's event queue (queued connections).

**Q3: Explain the Model/View architecture. Why is it better than item-based widgets?**

Model/View separates data management (model) from visual presentation (view). Benefits: (1) Multiple views can display the same model. (2) Models can be swapped without changing views. (3) Proxy models add sorting/filtering without modifying data. (4) Scales better for large datasets (views only request visible data). Item-based widgets (QTableWidget, QListWidget) combine model and view, making them simpler but less flexible.

**Q4: What is the difference between QThread subclassing and the worker pattern?**

Subclassing `QThread` and overriding `run()` puts the work logic inside the thread object itself. The worker pattern creates a separate `QObject`, moves it to a `QThread` with `moveToThread()`, and triggers work via signals. The worker pattern is preferred because it provides better separation of concerns, allows the worker to receive signals (has an event loop), and is more reusable.

**Q5: How does Qt handle memory management?**

Qt uses a parent-child ownership tree. When a parent `QObject` is deleted, it automatically deletes all its children. This eliminates most manual memory management. Top-level widgets (no parent) must be managed explicitly. Python's garbage collector handles the Python wrapper objects, but the C++ objects follow Qt's ownership rules.

**Q6: What is the difference between `QWidget.update()` and `QWidget.repaint()`?**

`update()` schedules a paint event that will be processed in the next event loop iteration. Multiple `update()` calls may be coalesced into a single `paintEvent`. `repaint()` forces an immediate repaint, bypassing the event loop. Prefer `update()` in almost all cases -- `repaint()` can cause performance issues and recursive paint events.

**Q7: How do you apply consistent styling across an application?**

Use `QApplication.setStyleSheet()` with Qt Style Sheets (QSS), which is CSS-like syntax supporting selectors, pseudo-states, and sub-controls. For more complex theming, use `QPalette` to set system colors, or create a custom `QStyle` subclass. Object names (`setObjectName`) and properties allow targeted styling with `#name` and `[property]` selectors.

---

*End of Python Libraries reference. This guide is designed to be a comprehensive companion to the [Python Fundamentals](Python_Fundamentals.md), [Pandas](Pandas.md), [DSA Fundamentals](../computer-science/DSA_Fundamentals.md), [LeetCode Patterns](../computer-science/LeetCode_Patterns.md), and [CS Fundamentals](../computer-science/CS_Fundamentals.md) guides.*
