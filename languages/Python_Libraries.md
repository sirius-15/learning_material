# Python Libraries -- Comprehensive Reference

> A thorough reference covering NumPy, Pandas, and PyQt -- the core libraries for numerical computing, data manipulation, and GUI development in Python. Each section includes conceptual explanations, comparison tables, code examples, common pitfalls, and interview questions with detailed answers. Complements the *Python Fundamentals*, *DSA Fundamentals*, and *CS Fundamentals* guides.

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

### Part 2: Pandas

10. [Series and DataFrame](#10-series-and-dataframe)
11. [Indexing and Selection](#11-indexing-and-selection)
12. [Data Cleaning and Transformation](#12-data-cleaning-and-transformation)
13. [GroupBy and Aggregation](#13-groupby-and-aggregation)
14. [Merging, Joining, and Reshaping](#14-merging-joining-and-reshaping)
15. [Time Series](#15-time-series)
16. [I/O Operations](#16-io-operations)
17. [Pandas Performance](#17-pandas-performance)
18. [Pandas Common Pitfalls and Interview Questions](#18-pandas-common-pitfalls-and-interview-questions)

### Part 3: PyQt

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
a = np.array([1, 2, 3])           # default int64 (or int32 on Windows)
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
a = np.array([200], dtype=np.int8)   # max is 127
print(a + np.int8(100))               # [-156] -- wraps around, no error!
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

# Part 2: Pandas

---

# 10. Series and DataFrame

---

## 10.1 Core Data Structures

Pandas is built on two primary structures:

| Structure | Dimensionality | Analogy |
|---|---|---|
| `Series` | 1-D labeled array | A single column with an index |
| `DataFrame` | 2-D labeled table | A spreadsheet / SQL table |

Both are built on top of NumPy arrays but add **labeled axes** (index and columns).

```python
import pandas as pd
import numpy as np
```

## 10.2 Series

A Series is a 1-D array with an associated index.

```python
s = pd.Series([10, 20, 30, 40], index=['a', 'b', 'c', 'd'], name='values')

print(s)
# a    10
# b    20
# c    30
# d    40
# Name: values, dtype: int64

s['b']           # 20 (label-based access)
s[1]             # 20 (positional access -- deprecated for ambiguous cases)
s[['a', 'c']]    # Series with a=10, c=30
s[s > 15]        # Series with b=20, c=30, d=40
```

**Series from dict:**

```python
d = {'x': 100, 'y': 200, 'z': 300}
s = pd.Series(d)    # keys become index
```

**Key attributes:**

| Attribute | Description |
|---|---|
| `s.index` | Index labels |
| `s.values` | Underlying NumPy array |
| `s.dtype` | Data type |
| `s.name` | Series name |
| `s.shape` | Tuple (n,) |
| `s.is_unique` | True if all values are unique |

## 10.3 DataFrame

A DataFrame is a 2-D table with labeled rows (index) and columns.

```python
df = pd.DataFrame({
    'name':   ['Alice', 'Bob', 'Carol'],
    'age':    [25, 30, 35],
    'salary': [50000, 60000, 70000]
})

print(df)
#     name  age  salary
# 0  Alice   25   50000
# 1    Bob   30   60000
# 2  Carol   35   70000
```

**Construction methods:**

| Method | Example |
|---|---|
| Dict of lists | `pd.DataFrame({'a': [1,2], 'b': [3,4]})` |
| List of dicts | `pd.DataFrame([{'a': 1, 'b': 3}, {'a': 2, 'b': 4}])` |
| 2-D NumPy array | `pd.DataFrame(np.zeros((3,4)), columns=['a','b','c','d'])` |
| From Series | `pd.DataFrame({'col': some_series})` |

**Key attributes:**

| Attribute | Description |
|---|---|
| `df.index` | Row labels |
| `df.columns` | Column labels |
| `df.dtypes` | Series of column dtypes |
| `df.shape` | Tuple (rows, cols) |
| `df.values` | Underlying 2-D NumPy array |
| `df.info()` | Memory usage, dtypes, non-null counts |
| `df.describe()` | Summary statistics for numeric columns |
| `df.head(n)` / `df.tail(n)` | First/last n rows |

## 10.4 Pandas dtype System

| dtype | Description | NumPy Equivalent | Notes |
|---|---|---|---|
| `int64` | Integer | `np.int64` | No NaN support (use `Int64` nullable) |
| `float64` | Float | `np.float64` | Default when NaN present in int column |
| `bool` | Boolean | `np.bool_` | `boolean` for nullable |
| `object` | Mixed/string | N/A | Catch-all; slow; avoid when possible |
| `category` | Categorical | N/A | Memory-efficient for low-cardinality |
| `datetime64[ns]` | Timestamps | `np.datetime64` | Nanosecond resolution |
| `timedelta64[ns]` | Durations | `np.timedelta64` | |
| `string` | String (Arrow) | N/A | Pandas 1.0+ nullable string type |
| `Int64` / `Float64` | Nullable integer/float | N/A | Capital letter = nullable extension type |

```python
df = pd.DataFrame({'a': [1, 2, None]})
print(df['a'].dtype)   # float64 -- NaN forced int→float

df = pd.DataFrame({'a': pd.array([1, 2, None], dtype='Int64')})
print(df['a'].dtype)   # Int64 -- nullable integer, NaN preserved
```

---

# 11. Indexing and Selection

---

## 11.1 The Four Indexers

| Indexer | Type | Usage | Speed |
|---|---|---|---|
| `[]` (bracket) | Label or positional | Column selection, row slicing | Fast |
| `.loc[row, col]` | **Label-based** | Explicit label indexing | Fast |
| `.iloc[row, col]` | **Position-based** | Integer position indexing | Fast |
| `.at[row, col]` | Label (scalar) | Single value access | Fastest |
| `.iat[row, col]` | Position (scalar) | Single value access | Fastest |

## 11.2 Bracket Operator `[]`

```python
df = pd.DataFrame({'a': [1,2,3], 'b': [4,5,6], 'c': [7,8,9]})

df['a']        # Series (single column)
df[['a','b']]  # DataFrame (multiple columns)
df[0:2]        # Rows by slice (positional, not label-based here)
df[df['a'] > 1]  # Boolean row selection
```

## 11.3 loc -- Label-Based

Inclusive on both ends of slice.

```python
df = pd.DataFrame(
    {'x': [10, 20, 30], 'y': [40, 50, 60]},
    index=['a', 'b', 'c']
)

df.loc['a']              # Series (row 'a')
df.loc['a', 'x']         # 10 (scalar)
df.loc['a':'b']          # rows 'a' AND 'b' (inclusive!)
df.loc['a':'b', 'x']    # Series: a=10, b=20
df.loc[df['x'] > 15]    # boolean selection
df.loc[:, 'x':'y']      # all rows, columns 'x' through 'y'
```

## 11.4 iloc -- Position-Based

Standard Python slicing (exclusive end).

```python
df.iloc[0]            # first row (Series)
df.iloc[0, 1]         # element at row 0, col 1
df.iloc[0:2]          # first two rows (exclusive end)
df.iloc[:, 0:2]       # all rows, first two columns
df.iloc[[0, 2], [1]]  # fancy positional indexing
```

## 11.5 loc vs iloc Comparison

| Feature | `loc` | `iloc` |
|---|---|---|
| Indexing type | Label-based | Position-based |
| Slice end | **Inclusive** | **Exclusive** |
| Accepts | Labels, boolean arrays, callables | Integers, boolean arrays, callables |
| Error on missing | KeyError | IndexError |
| Use when | Index has meaningful labels | Need ordinal position |

```python
df = pd.DataFrame({'val': [10, 20, 30]}, index=[100, 200, 300])

df.loc[100]    # val=10 (label 100)
df.iloc[0]     # val=10 (position 0)

df.loc[100:200]   # TWO rows (inclusive)
df.iloc[0:1]      # ONE row (exclusive end)
```

## 11.6 MultiIndex

A hierarchical index with multiple levels:

```python
arrays = [['A', 'A', 'B', 'B'], [1, 2, 1, 2]]
idx = pd.MultiIndex.from_arrays(arrays, names=['letter', 'number'])
df = pd.DataFrame({'val': [10, 20, 30, 40]}, index=idx)

#                val
# letter number
# A      1       10
#        2       20
# B      1       30
#        2       40

df.loc['A']           # sub-DataFrame for letter='A'
df.loc[('A', 1)]      # Series for specific combo
df.xs(1, level='number')   # cross-section: all rows where number=1
```

## 11.7 query()

String-based expression filtering (uses `numexpr` for speed on large DataFrames):

```python
df = pd.DataFrame({'age': [25, 30, 35], 'salary': [50000, 60000, 70000]})

df.query('age > 28 and salary < 65000')
# equivalent to: df[(df['age'] > 28) & (df['salary'] < 65000)]

threshold = 30
df.query('age >= @threshold')   # @ references local variable
```

---

# 12. Data Cleaning and Transformation

---

## 12.1 Missing Data

Pandas uses `NaN` (float), `NaT` (datetime), and `pd.NA` (nullable) as missing value sentinels.

| Function | Description |
|---|---|
| `df.isna()` / `df.isnull()` | Boolean mask of missing values |
| `df.notna()` | Boolean mask of non-missing values |
| `df.dropna(axis, how, subset, thresh)` | Remove rows/cols with missing values |
| `df.fillna(value, method)` | Fill missing values |
| `df.interpolate(method)` | Fill by interpolation |
| `df.bfill()` / `df.ffill()` | Back-fill / forward-fill |

```python
df = pd.DataFrame({'a': [1, np.nan, 3], 'b': [4, 5, np.nan]})

df.isna()
#        a      b
# 0  False  False
# 1   True  False
# 2  False   True

df.dropna()                    # rows where ALL values present → only row 0
df.dropna(subset=['a'])        # drop rows where 'a' is NaN
df.fillna(0)                   # replace NaN with 0
df.fillna({'a': 0, 'b': 99})   # per-column fill values
df['a'].interpolate()          # [1.0, 2.0, 3.0] -- linear interpolation
```

## 12.2 Duplicates

```python
df = pd.DataFrame({'a': [1, 1, 2], 'b': [3, 3, 4]})

df.duplicated()                # [False, True, False]
df.duplicated(keep='last')     # [True, False, False]
df.drop_duplicates()           # keep first occurrence
df.drop_duplicates(subset=['a'], keep='last')
```

## 12.3 Type Conversion

```python
df['age'] = df['age'].astype(int)
df['salary'] = pd.to_numeric(df['salary'], errors='coerce')   # invalid → NaN
df['date'] = pd.to_datetime(df['date_str'])
```

## 12.4 map, apply, applymap

| Method | Operates On | Input | Use Case |
|---|---|---|---|
| `Series.map(func_or_dict)` | Element-wise on Series | Dict, function, or Series | Transform values via mapping |
| `Series.apply(func)` | Element-wise on Series | Function | More flexible than map |
| `DataFrame.apply(func, axis)` | Row or column (Series) | Function taking a Series | Column/row-level operations |
| `DataFrame.map(func)` | Element-wise on DataFrame | Function | Transform every cell (was `applymap` pre-2.0) |

```python
df = pd.DataFrame({'name': ['alice', 'bob'], 'age': [25, 30]})

df['name'].map(str.upper)           # ['ALICE', 'BOB']
df['name'].map({'alice': 'A', 'bob': 'B'})  # ['A', 'B']

df['age'].apply(lambda x: 'young' if x < 30 else 'senior')  # ['young', 'senior']

df.apply(lambda row: f"{row['name']}-{row['age']}", axis=1)  # row-wise

df[['age']].map(lambda x: x * 2)   # element-wise on DataFrame
```

## 12.5 String Accessor (.str)

Series with string dtype exposes vectorized string operations via `.str`:

```python
s = pd.Series(['  Alice  ', 'BOB', 'carol'])

s.str.lower()          # ['  alice  ', 'bob', 'carol']
s.str.strip()          # ['Alice', 'BOB', 'carol']
s.str.contains('o')    # [False, True, True]
s.str.replace('o', '0')  # ['  Alice  ', 'B0B', 'car0l']
s.str.split('a')       # splits each string
s.str.len()            # [9, 3, 5]
s.str[0:3]             # slicing each string
s.str.startswith('A')  # [False, False, False] (whitespace!)
```

## 12.6 replace

```python
df = pd.DataFrame({'status': ['Y', 'N', 'Y', 'N']})

df['status'].replace({'Y': True, 'N': False})
df.replace({'status': {'Y': 1, 'N': 0}})   # column-specific
df.replace(to_replace=r'^old_.*', value='new', regex=True)  # regex
```

## 12.7 pd.Categorical

For columns with a small number of distinct values (low cardinality), `Categorical` dtype saves memory and enables ordered operations:

```python
df['grade'] = pd.Categorical(df['grade'], categories=['F','D','C','B','A'], ordered=True)

df.sort_values('grade')           # sorts by custom order
df[df['grade'] > 'C']            # comparison uses category order
print(df['grade'].cat.codes)      # integer codes: [0, 1, 2, 3, 4]
```

| Aspect | object dtype | category dtype |
|---|---|---|
| Memory (1M rows, 100 unique) | ~60 MB | ~1 MB |
| Comparison | Lexicographic | Custom order supported |
| Groupby speed | Slower | Faster (integer codes) |

---

# 13. GroupBy and Aggregation

---

## 13.1 Split-Apply-Combine

The GroupBy pattern:

```
                    ┌────────────────┐
                    │  Original DF   │
                    └───────┬────────┘
                            │ .groupby('key')
               ┌────────────┼────────────┐
               ▼            ▼            ▼
          ┌─────────┐ ┌─────────┐ ┌─────────┐
          │ Group A │ │ Group B │ │ Group C │    ← SPLIT
          └────┬────┘ └────┬────┘ └────┬────┘
               │ .agg()    │           │
               ▼            ▼            ▼        ← APPLY
          ┌─────────┐ ┌─────────┐ ┌─────────┐
          │ Result  │ │ Result  │ │ Result  │
          └────┬────┘ └────┬────┘ └────┬────┘
               │            │           │
               └────────────┼───────────┘
                            ▼                     ← COMBINE
                    ┌────────────────┐
                    │  Result DF     │
                    └────────────────┘
```

```python
df = pd.DataFrame({
    'dept':   ['Sales', 'Sales', 'Eng', 'Eng', 'Eng'],
    'name':   ['Alice', 'Bob', 'Carol', 'Dave', 'Eve'],
    'salary': [50000, 60000, 70000, 80000, 90000]
})

grouped = df.groupby('dept')

grouped.mean(numeric_only=True)      # mean salary per dept
grouped.size()                        # count per group
grouped['salary'].sum()               # sum of salary per dept
```

## 13.2 Aggregation with agg

```python
grouped['salary'].agg(['mean', 'min', 'max', 'count'])
#        mean    min    max  count
# dept
# Eng   80000  70000  90000      3
# Sales 55000  50000  60000      2

grouped.agg(
    avg_salary=('salary', 'mean'),
    max_salary=('salary', 'max'),
    headcount=('name', 'count')
)

grouped['salary'].agg([
    ('Average', 'mean'),
    ('Total', 'sum'),
    ('Spread', lambda x: x.max() - x.min())
])
```

## 13.3 transform

Returns a Series with the **same index** as the input (broadcasts the group result back):

```python
df['dept_mean'] = df.groupby('dept')['salary'].transform('mean')
# Each row gets its department's mean salary

df['salary_zscore'] = df.groupby('dept')['salary'].transform(
    lambda x: (x - x.mean()) / x.std()
)
```

| Method | Output Shape | Use Case |
|---|---|---|
| `agg()` | One row per group | Summary statistics |
| `transform()` | Same shape as input | Broadcast group stat back to rows |
| `filter()` | Subset of original rows | Keep/remove entire groups |
| `apply()` | Flexible | Arbitrary group-wise operations |

## 13.4 filter

Keeps or removes entire groups based on a condition:

```python
df.groupby('dept').filter(lambda g: g['salary'].mean() > 55000)
# Keeps only Engineering group (mean 80000 > 55000)
```

## 13.5 pipe

Method chaining helper:

```python
(df
 .groupby('dept')
 .pipe(lambda g: g.agg({'salary': 'mean'}))
 .pipe(lambda d: d.rename(columns={'salary': 'avg_salary'}))
)
```

## 13.6 pd.crosstab

Frequency table shortcut:

```python
pd.crosstab(df['dept'], df['level'])
# level    Junior  Senior
# dept
# Eng           1       2
# Sales         2       0

pd.crosstab(df['dept'], df['level'], values=df['salary'], aggfunc='mean')
```

---

# 14. Merging, Joining, and Reshaping

---

## 14.1 merge (SQL-style Joins)

```python
left = pd.DataFrame({'key': ['a','b','c'], 'val_l': [1, 2, 3]})
right = pd.DataFrame({'key': ['b','c','d'], 'val_r': [4, 5, 6]})

pd.merge(left, right, on='key', how='inner')
#   key  val_l  val_r
# 0   b      2      4
# 1   c      3      5
```

| `how` | SQL Equivalent | Result |
|---|---|---|
| `inner` | `INNER JOIN` | Only matching keys |
| `left` | `LEFT JOIN` | All left rows, match right where possible |
| `right` | `RIGHT JOIN` | All right rows, match left where possible |
| `outer` | `FULL OUTER JOIN` | All rows from both |
| `cross` | `CROSS JOIN` | Cartesian product |

**Common parameters:**

| Parameter | Description |
|---|---|
| `on` | Column(s) to join on (must exist in both) |
| `left_on` / `right_on` | Different column names in each DataFrame |
| `left_index` / `right_index` | Join on index instead of column |
| `suffixes` | Suffix for overlapping column names (default `('_x', '_y')`) |
| `indicator` | Add `_merge` column showing join source |
| `validate` | Check merge type: `'one_to_one'`, `'one_to_many'`, etc. |

```python
result = pd.merge(left, right, on='key', how='outer', indicator=True)
#   key  val_l  val_r      _merge
# 0   a    1.0    NaN   left_only
# 1   b    2.0    4.0        both
# 2   c    3.0    5.0        both
# 3   d    NaN    6.0  right_only
```

## 14.2 join (Index-Based)

```python
df1 = pd.DataFrame({'a': [1, 2]}, index=['x', 'y'])
df2 = pd.DataFrame({'b': [3, 4]}, index=['x', 'z'])

df1.join(df2, how='outer')
#      a    b
# x  1.0  3.0
# y  2.0  NaN
# z  NaN  4.0
```

## 14.3 concat

Stacks DataFrames along an axis:

```python
df1 = pd.DataFrame({'a': [1, 2]})
df2 = pd.DataFrame({'a': [3, 4]})

pd.concat([df1, df2], ignore_index=True)    # vertical stack
pd.concat([df1, df2], axis=1)               # horizontal stack
pd.concat([df1, df2], keys=['first', 'second'])  # hierarchical index
```

| Parameter | Description |
|---|---|
| `axis` | 0 = stack rows (default), 1 = stack columns |
| `join` | `'outer'` (default) or `'inner'` |
| `ignore_index` | Reset index to 0, 1, 2, ... |
| `keys` | Add hierarchical index level |

## 14.4 Reshaping: pivot, pivot_table, melt, stack/unstack

| Function | Direction | Description |
|---|---|---|
| `pivot` | Long → Wide | Reshape (no aggregation, must be unique) |
| `pivot_table` | Long → Wide | Reshape with aggregation |
| `melt` | Wide → Long | Unpivot columns into rows |
| `stack` | Wide → Long | Pivot columns into index level |
| `unstack` | Long → Wide | Pivot index level into columns |

```python
df = pd.DataFrame({
    'date':    ['2024-01', '2024-01', '2024-02', '2024-02'],
    'product': ['A', 'B', 'A', 'B'],
    'sales':   [100, 200, 150, 250]
})

# pivot -- requires unique index/column pairs
df.pivot(index='date', columns='product', values='sales')
# product      A    B
# date
# 2024-01    100  200
# 2024-02    150  250

# pivot_table -- handles duplicates with aggregation
pd.pivot_table(df, values='sales', index='date', columns='product', aggfunc='sum')

# melt -- reverse of pivot
wide = df.pivot(index='date', columns='product', values='sales')
wide.reset_index().melt(id_vars='date', var_name='product', value_name='sales')
```

**stack / unstack:**

```python
df_multi = df.set_index(['date', 'product'])

df_multi.unstack()     # 'product' level → columns
df_multi.unstack().stack()  # reverse
```

---

# 15. Time Series

---

## 15.1 Core Types

| Type | Description | Example |
|---|---|---|
| `pd.Timestamp` | Single point in time | `pd.Timestamp('2024-01-15')` |
| `pd.DatetimeIndex` | Index of timestamps | `pd.date_range(...)` |
| `pd.Timedelta` | Duration | `pd.Timedelta('5 days')` |
| `pd.Period` | Time span (month, quarter) | `pd.Period('2024-01', freq='M')` |

## 15.2 Creating Date Ranges

```python
pd.date_range('2024-01-01', periods=5, freq='D')
# DatetimeIndex(['2024-01-01', '2024-01-02', ..., '2024-01-05'])

pd.date_range('2024-01-01', '2024-12-31', freq='ME')   # month-end dates
pd.date_range('2024-01-01', periods=4, freq='QE')      # quarter-end
pd.bdate_range('2024-01-01', periods=5)                 # business days only
```

| Freq Alias | Meaning |
|---|---|
| `D` | Calendar day |
| `B` | Business day |
| `W` | Weekly |
| `ME` | Month end |
| `MS` | Month start |
| `QE` | Quarter end |
| `YE` | Year end |
| `h` | Hourly |
| `min` | Minute |
| `s` | Second |

## 15.3 Resampling

Change the frequency of a time series (analogous to `groupby` for time):

```python
ts = pd.Series(
    range(365),
    index=pd.date_range('2024-01-01', periods=365, freq='D')
)

ts.resample('ME').sum()     # monthly totals
ts.resample('QE').mean()    # quarterly averages
ts.resample('W').agg(['sum', 'mean', 'max'])  # multiple aggregations
```

Downsampling (high freq → low freq) requires aggregation.
Upsampling (low freq → high freq) requires fill:

```python
monthly = ts.resample('ME').sum()
monthly.resample('D').ffill()    # forward-fill to daily
monthly.resample('D').interpolate()  # interpolate
```

## 15.4 Shifting and Differencing

| Method | Description | Use Case |
|---|---|---|
| `shift(n)` | Shift values by n periods | Lag/lead features |
| `diff(n)` | Difference with nth prior value | First differences |
| `pct_change(n)` | Percentage change | Returns/growth rates |

```python
s = pd.Series([100, 110, 105, 120])

s.shift(1)       # [NaN, 100, 110, 105]   -- previous value
s.diff(1)        # [NaN, 10, -5, 15]      -- change from previous
s.pct_change(1)  # [NaN, 0.1, -0.0455, 0.1429]  -- % change
```

## 15.5 Rolling and Expanding Windows

```python
s = pd.Series([1, 3, 5, 7, 9, 11])

s.rolling(window=3).mean()      # [NaN, NaN, 3.0, 5.0, 7.0, 9.0]
s.rolling(window=3).std()       # rolling standard deviation
s.expanding().mean()            # cumulative mean: [1, 2, 3, 4, 5, 6]
s.ewm(span=3).mean()           # exponentially weighted mean
```

| Method | Window | Description |
|---|---|---|
| `rolling(n)` | Fixed-size sliding | Last n values |
| `expanding()` | Growing from start | All values up to current |
| `ewm(span=n)` | Exponentially weighted | Recent values weighted more |

## 15.6 Datetime Components

```python
df['date'] = pd.to_datetime(df['date_str'])

df['date'].dt.year
df['date'].dt.month
df['date'].dt.day
df['date'].dt.day_name()     # 'Monday', 'Tuesday', ...
df['date'].dt.quarter
df['date'].dt.is_month_end
df['date'].dt.dayofweek      # 0=Monday, 6=Sunday
```

## 15.7 Timezone Handling

```python
ts = pd.Timestamp('2024-06-15 12:00')

ts_utc = ts.tz_localize('UTC')
ts_est = ts_utc.tz_convert('US/Eastern')

idx = pd.date_range('2024-01-01', periods=3, freq='D', tz='UTC')
```

---

# 16. I/O Operations

---

## 16.1 CSV

```python
df = pd.read_csv('data.csv')
df = pd.read_csv('data.csv',
    sep=',',
    header=0,
    index_col='id',
    usecols=['id', 'name', 'value'],
    dtype={'id': int, 'name': str},
    parse_dates=['date_col'],
    na_values=['NA', 'missing', '-'],
    nrows=1000,
    skiprows=[1, 2],
    encoding='utf-8'
)

df.to_csv('output.csv', index=False)
```

## 16.2 I/O Format Comparison

| Format | Read | Write | Speed | Human-Readable | Size |
|---|---|---|---|---|---|
| CSV | `read_csv` | `to_csv` | Slow | Yes | Large |
| Excel | `read_excel` | `to_excel` | Slow | Yes (with app) | Medium |
| JSON | `read_json` | `to_json` | Medium | Yes | Large |
| Parquet | `read_parquet` | `to_parquet` | **Fast** | No | **Small** |
| Feather | `read_feather` | `to_feather` | **Fast** | No | Small |
| HDF5 | `read_hdf` | `to_hdf` | Fast | No | Small |
| SQL | `read_sql` | `to_sql` | Varies | No | Varies |
| Pickle | `read_pickle` | `to_pickle` | Fast | No | Small |

## 16.3 Reading Large Files in Chunks

```python
chunks = pd.read_csv('large.csv', chunksize=10000)
result = pd.DataFrame()

for chunk in chunks:
    filtered = chunk[chunk['value'] > 100]
    result = pd.concat([result, filtered])

# Or using iterator:
reader = pd.read_csv('large.csv', iterator=True)
chunk = reader.get_chunk(5000)
```

## 16.4 SQL

```python
import sqlite3

conn = sqlite3.connect('database.db')

df = pd.read_sql('SELECT * FROM users WHERE age > 25', conn)
df = pd.read_sql_table('users', conn)

df.to_sql('users', conn, if_exists='replace', index=False)

conn.close()
```

## 16.5 Parquet (Recommended for Analytics)

```python
df.to_parquet('data.parquet', engine='pyarrow')
df = pd.read_parquet('data.parquet', columns=['col1', 'col2'])  # read only needed cols
```

Parquet advantages: columnar storage, compression, schema preservation, fast I/O, type safety.

---

# 17. Pandas Performance

---

## 17.1 Vectorized vs apply

```python
# SLOW: apply with Python function
df['result'] = df['col'].apply(lambda x: x ** 2 + 1)

# FAST: vectorized
df['result'] = df['col'] ** 2 + 1
```

**Rule of thumb**: if you can write it without `apply`, do so. Vectorized Pandas/NumPy operations are 10-100x faster.

## 17.2 eval() and query()

For complex expressions on large DataFrames, `eval` avoids creating intermediate arrays:

```python
df.eval('c = a + b * 2', inplace=True)

df.query('a > 10 and b < 50')
```

Both use `numexpr` under the hood for multi-threaded evaluation.

## 17.3 Categorical for Memory

```python
df['status'] = df['status'].astype('category')
```

| Scenario | object dtype | category dtype | Savings |
|---|---|---|---|
| 1M rows, 10 unique strings | ~60 MB | ~1 MB | ~98% |
| 1M rows, 100K unique strings | ~60 MB | ~55 MB | ~8% |

Use `category` when the number of unique values is small relative to the total number of rows.

## 17.4 The inplace Debate

`inplace=True` does **not** save memory in most cases -- Pandas still creates a copy internally and reassigns. It also breaks method chaining and is being deprecated for many operations.

```python
# Avoid:
df.drop(columns=['temp'], inplace=True)

# Prefer:
df = df.drop(columns=['temp'])
```

## 17.5 Method Chaining

```python
result = (
    df
    .query('age > 18')
    .assign(salary_k=lambda d: d['salary'] / 1000)
    .groupby('dept')
    .agg(avg_salary_k=('salary_k', 'mean'))
    .sort_values('avg_salary_k', ascending=False)
    .head(10)
)
```

## 17.6 copy() Semantics

```python
df2 = df              # reference -- same object
df3 = df.copy()       # deep copy -- independent

df2['a'] = 999        # modifies df too!
df3['a'] = 999        # does not affect df
```

As of Pandas 2.0+, indexing operations return copies by default (Copy-on-Write behavior), reducing the risk of `SettingWithCopyWarning`.

---

# 18. Pandas Common Pitfalls and Interview Questions

---

## 18.1 Common Pitfalls

**Pitfall 1: SettingWithCopyWarning**

```python
# BAD: chained indexing may modify a copy
df[df['a'] > 5]['b'] = 10   # SettingWithCopyWarning -- may not work

# GOOD: use loc
df.loc[df['a'] > 5, 'b'] = 10
```

**Pitfall 2: NaN breaks integer dtype**

```python
s = pd.Series([1, 2, None])
print(s.dtype)   # float64 -- NaN forces float

# Fix: use nullable integer
s = pd.Series([1, 2, None], dtype='Int64')
print(s.dtype)   # Int64 (nullable)
```

**Pitfall 3: merge key mismatches due to dtype**

```python
# left['id'] is int64, right['id'] is object → merge finds no matches
left['id'] = left['id'].astype(str)   # convert to match
```

**Pitfall 4: apply is slow**

```python
# Slow: Python-level loop
df['result'] = df.apply(lambda row: row['a'] + row['b'], axis=1)

# Fast: vectorized
df['result'] = df['a'] + df['b']
```

**Pitfall 5: Comparing with None/NaN**

```python
np.nan == np.nan       # False!
pd.Series([np.nan]).isna()  # True -- use isna(), never ==
```

## 18.2 Interview Questions

**Q1: What is the difference between loc and iloc?**

`loc` is label-based and slices are inclusive on both ends. `iloc` is position-based and uses standard Python slice semantics (exclusive end). `loc` raises `KeyError` for missing labels; `iloc` raises `IndexError` for out-of-range positions.

**Q2: Explain the GroupBy split-apply-combine pattern.**

`groupby()` splits the DataFrame into groups based on key values. An operation (aggregation, transformation, or filter) is applied to each group independently. The results are then combined back into a single DataFrame. Key methods: `agg()` (one row per group), `transform()` (same shape as input), `filter()` (keep/remove entire groups).

**Q3: What is the difference between merge, join, and concat?**

- `merge`: SQL-style joins on columns or index. Supports inner, left, right, outer, and cross joins. Most flexible.
- `join`: Convenience method that joins on index by default (equivalent to `merge` with `left_index=True`/`right_index=True`).
- `concat`: Stacks DataFrames along an axis (rows or columns) without matching on keys. Used for appending data.

**Q4: When should you use Categorical dtype?**

When a column has **low cardinality** (few unique values relative to total rows). Benefits: 98%+ memory reduction, faster groupby/sort (operates on integer codes), and support for custom ordering. Not beneficial when cardinality approaches the number of rows.

**Q5: How do you handle a CSV file that does not fit in memory?**

1. Read in chunks: `pd.read_csv('file.csv', chunksize=N)` returns an iterator
2. Select only needed columns: `usecols` parameter
3. Specify dtypes on read to reduce memory: `dtype` parameter
4. Use Parquet format instead (columnar, compressed)
5. Use Dask or Polars for out-of-core computation

**Q6: What is the difference between pivot and pivot_table?**

`pivot` simply reshapes data from long to wide format and raises an error if there are duplicate index/column pairs. `pivot_table` handles duplicates by applying an aggregation function (default `mean`). `pivot_table` also supports margins (subtotals) via `margins=True`.

**Q7: Explain Copy-on-Write in Pandas 2.0+.**

Copy-on-Write (CoW) is a memory optimization where indexing operations return views that share memory with the parent. A copy is only made when the view is mutated. This eliminates `SettingWithCopyWarning` and makes the behavior deterministic: any indexed subset behaves like an independent copy on write but shares memory on read.

---

# Part 3: PyQt

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

*End of Python Libraries reference. This guide is designed to be a comprehensive companion to the Python Fundamentals, DSA Fundamentals, LeetCode Patterns, and CS Fundamentals guides.*
