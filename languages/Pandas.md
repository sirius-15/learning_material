# Pandas -- Comprehensive Reference

> A deep, all-levels reference for the Pandas data-analysis library. Covers the foundations (Series, DataFrame, Index), the dtype system (including the modern PyArrow backend and nullable extension types), selection and filtering, cleaning and transformation, GroupBy and reshaping, combining and joining, time series, I/O, plotting and styling, performance and memory, and Pandas internals -- with comparison tables, code examples, common pitfalls, and interview questions throughout. Targets Pandas 2.x conventions including Copy-on-Write, `ArrowDtype`, nullable extension dtypes, and the new frequency aliases. Complements *Python Fundamentals* and the NumPy / PyQt sections of *Python Libraries*.

---

## Table of Contents

### Part 1: Foundations

1. [Pandas Overview, Setup, and Display Options](#1-pandas-overview-setup-and-display-options)
2. [Series](#2-series)
3. [DataFrame](#3-dataframe)
4. [Index and MultiIndex](#4-index-and-multiindex)

### Part 2: dtypes and Missing Data

5. [The Pandas dtype System](#5-the-pandas-dtype-system)
6. [Missing Data Semantics](#6-missing-data-semantics)
7. [PyArrow Backend](#7-pyarrow-backend)

### Part 3: Selecting and Filtering

8. [The Four Indexers](#8-the-four-indexers)
9. [Boolean Selection, query, eval, where, mask](#9-boolean-selection-query-eval-where-mask)
10. [MultiIndex Slicing Patterns](#10-multiindex-slicing-patterns)
11. [Copy-on-Write, Views, and SettingWithCopyWarning](#11-copy-on-write-views-and-settingwithcopywarning)

### Part 4: Cleaning and Transformation

12. [Sorting, Ranking, Duplicates](#12-sorting-ranking-duplicates)
13. [Type Conversion](#13-type-conversion)
14. [The .str Accessor](#14-the-str-accessor)
15. [The .dt Accessor](#15-the-dt-accessor)
16. [Categorical Deep Dive](#16-categorical-deep-dive)
17. [Transformation Toolkit](#17-transformation-toolkit)

### Part 5: Aggregation and Reshaping

18. [GroupBy: Split-Apply-Combine](#18-groupby-split-apply-combine)
19. [agg vs transform vs filter vs apply](#19-agg-vs-transform-vs-filter-vs-apply)
20. [Named Aggregations, crosstab, pivot_table](#20-named-aggregations-crosstab-pivot_table)
21. [Window Functions](#21-window-functions)
22. [Reshaping: pivot, melt, stack, unstack](#22-reshaping-pivot-melt-stack-unstack)

### Part 6: Combining DataFrames

23. [concat](#23-concat)
24. [merge and join](#24-merge-and-join)
25. [merge_asof, merge_ordered, compare, align](#25-merge_asof-merge_ordered-compare-align)

### Part 7: Time Series

26. [Timestamps, Periods, Timedeltas](#26-timestamps-periods-timedeltas)
27. [Date Ranges, Resampling, Shifting, Windows](#27-date-ranges-resampling-shifting-windows)
28. [Timezones, Business Days, Calendars](#28-timezones-business-days-calendars)

### Part 8: I/O, Visualization, Performance

29. [I/O Formats](#29-io-formats)
30. [Plotting and Styling](#30-plotting-and-styling)
31. [Performance](#31-performance)
32. [Memory Optimization](#32-memory-optimization)

### Part 9: Internals, Ecosystem, Pitfalls

33. [Pandas Internals and Testing](#33-pandas-internals-and-testing)
34. [Ecosystem and When to Switch](#34-ecosystem-and-when-to-switch)
35. [Idioms and Method Chaining Recipes](#35-idioms-and-method-chaining-recipes)
36. [Common Pitfalls and Interview Questions](#36-common-pitfalls-and-interview-questions)

---

# Part 1: Foundations

---

# 1. Pandas Overview, Setup, and Display Options

---

## 1.1 What Is Pandas?

Pandas is the de-facto Python library for **labeled, tabular data analysis**. It builds two primary structures -- **Series** (1-D) and **DataFrame** (2-D) -- on top of NumPy arrays (and, increasingly, Apache Arrow buffers). The "labeled axes" (index and columns) distinguish it from raw NumPy: every row and every column has a name, and operations align by label rather than by position.

| Layer | Provided By | Purpose |
|---|---|---|
| Compute kernels | NumPy / PyArrow / Cython / numexpr | Vectorized math, string ops, datetime arithmetic |
| Storage | NumPy ndarrays or Arrow ChunkedArrays | Contiguous typed buffers |
| Labeling | Pandas `Index` / `MultiIndex` | Row/column labels, alignment, joins |
| User API | `Series`, `DataFrame`, `GroupBy`, accessors | High-level data manipulation |

**Brief history (relevant to today's API):**

| Era | Pandas Version | Notable Change |
|---|---|---|
| Classic | 0.x -- 1.x | NumPy-only backing; `object` dtype for strings; `np.nan` everywhere |
| Modern | 2.0 (2023) | `ArrowDtype`, `dtype_backend='pyarrow'`, deprecation of `applymap` |
| CoW transition | 2.0 -- 2.2 | Copy-on-Write opt-in via `pd.options.mode.copy_on_write = True` |
| Future | 3.0 | Copy-on-Write becomes the default; `string` dtype defaults to PyArrow-backed |

## 1.2 Installation and Import Convention

```python
# pip install pandas pyarrow numpy

import pandas as pd
import numpy as np

print(pd.__version__)         # e.g. '2.2.3'
print(pd.show_versions())     # full environment dump
```

The `pd` alias is universal -- using anything else will confuse readers and tooling.

## 1.3 The Display Option System

Pandas ships with a hierarchical option registry that controls how DataFrames are printed and how some numerical operations behave. Four core helpers:

| Function | Purpose |
|---|---|
| `pd.set_option('opt', value)` | Set an option globally |
| `pd.get_option('opt')` | Read the current value |
| `pd.reset_option('opt')` | Restore default (use `'all'` to reset everything) |
| `pd.option_context('opt', value)` | Temporarily change inside a `with` block |

```python
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 200)
pd.set_option('display.precision', 4)

with pd.option_context('display.max_rows', 5):
    print(big_df)               # only inside this block

pd.reset_option('display.max_rows')
```

## 1.4 The Most Useful Display Options

| Option | Default | Effect |
|---|---|---|
| `display.max_rows` | 60 | Max rows shown before truncation |
| `display.min_rows` | 10 | Rows shown when truncated |
| `display.max_columns` | 0 (auto) | Max columns shown before truncation |
| `display.width` | 80 | Terminal width assumed for wrapping |
| `display.precision` | 6 | Decimal digits for floats |
| `display.float_format` | `None` | Custom format function (e.g. `'{:,.2f}'.format`) |
| `display.max_colwidth` | 50 | Truncate string cells beyond this width |
| `display.expand_frame_repr` | True | Wrap wide frames vs. truncate |
| `display.show_dimensions` | `'truncate'` | Show `[N rows x M cols]` footer |
| `display.notebook_repr_html` | True | Render rich HTML in Jupyter |
| `mode.chained_assignment` | `'warn'` | `None` / `'warn'` / `'raise'` for chained-assign warnings |
| `mode.copy_on_write` | False (2.x) | Enable CoW (default in 3.0) |
| `future.infer_string` | False | When True, infer `string[pyarrow]` for new string columns |

## 1.5 Future Flags

Pandas exposes opt-in previews under `pd.options.future.*`. Two are particularly important to know in 2.x:

```python
pd.options.future.infer_string = True       # PyArrow strings by default
pd.options.future.no_silent_downcasting = True  # stricter dtype handling
pd.options.mode.copy_on_write = True        # CoW preview
```

Set these once at the top of a notebook or in `~/.pdrc.py` style startup so the codebase migrates gradually before 3.0 lands.

---

# 2. Series

---

## 2.1 What Is a Series?

A **Series** is a 1-D, labeled, homogeneously-typed array. Conceptually it is a single column of a DataFrame plus the index attached to that column.

```
            Series
    ┌────────┬───────┐
    │ index  │ value │
    ├────────┼───────┤
    │  a     │  10   │
    │  b     │  20   │   ← labels live on the left
    │  c     │  30   │
    │  d     │  40   │
    └────────┴───────┘
       Name: 'demand', dtype: int64
```

```python
s = pd.Series([10, 20, 30, 40],
              index=['a', 'b', 'c', 'd'],
              name='demand',
              dtype='Int64')
```

## 2.2 Construction Methods

| Source | Example | Notes |
|---|---|---|
| Python list | `pd.Series([1, 2, 3])` | Default `RangeIndex` 0..n-1 |
| NumPy array | `pd.Series(np.arange(5))` | Zero-copy when possible |
| Dict | `pd.Series({'a': 1, 'b': 2})` | Keys become the index |
| Scalar + index | `pd.Series(0, index=range(5))` | Broadcasts the scalar |
| DataFrame column | `df['col']` | Returns a Series view |
| `pd.array` + dtype | `pd.Series(pd.array([1, None], dtype='Int64'))` | Nullable extension type |

```python
s_dict = pd.Series({'AAPL': 192.5, 'MSFT': 415.2, 'GOOG': 175.8})
s_dict.index    # Index(['AAPL', 'MSFT', 'GOOG'], dtype='object')

s_const = pd.Series(np.nan, index=pd.date_range('2024-01-01', periods=5))
```

## 2.3 Key Attributes

| Attribute | Description |
|---|---|
| `s.values` | Underlying ndarray (legacy) |
| `s.array` | Underlying `ExtensionArray` (preferred for extension dtypes) |
| `s.index` | The `Index` object |
| `s.name` | Series name (also becomes column name when added to a DataFrame) |
| `s.dtype` | Element type |
| `s.shape` | `(n,)` |
| `s.size` | Element count |
| `s.nbytes` | Memory used by the buffer (excludes index) |
| `s.hasnans` | True if any missing values |
| `s.is_unique` | All values distinct |
| `s.is_monotonic_increasing` | Sorted ascending |
| `s.empty` | True if length is 0 |

## 2.4 Index Alignment in Operations

This is the single most important Pandas concept that trips up NumPy users. Arithmetic on two Series **aligns on the index**, not on position.

```python
s1 = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
s2 = pd.Series([10, 20, 30], index=['b', 'c', 'd'])

s1 + s2
# a     NaN     ← 'a' missing in s2
# b    12.0
# c    23.0
# d     NaN     ← 'd' missing in s1
# dtype: float64
```

Use the `add(..., fill_value=0)` family to control the missing side:

```python
s1.add(s2, fill_value=0)
# a     1.0
# b    12.0
# c    23.0
# d    30.0
```

| Operator | Method Form (with `fill_value`) |
|---|---|
| `+` | `s1.add(s2, fill_value=0)` |
| `-` | `s1.sub(s2, fill_value=0)` |
| `*` | `s1.mul(s2, fill_value=1)` |
| `/` | `s1.div(s2, fill_value=1)` |
| `//` | `s1.floordiv(s2)` |
| `**` | `s1.pow(s2)` |

## 2.5 Series vs Python list vs NumPy array

| Feature | `list` | `np.ndarray` | `pd.Series` |
|---|---|---|---|
| Homogeneous dtype | No | Yes | Yes |
| Labeled axis | No | No | Yes |
| Vectorized math | No | Yes | Yes |
| Missing-value semantics | Manual | `np.nan` only | `NaN` / `NaT` / `pd.NA` |
| String accessor | No | No | Yes (`.str`) |
| Datetime accessor | No | Limited | Yes (`.dt`) |
| Memory overhead | High (per-element box) | Low (contiguous) | Low + small index |

## 2.6 Hashable Index Labels

Index labels must be **hashable** (so Pandas can build the lookup hash table). Strings, integers, tuples (used by MultiIndex), `pd.Timestamp`, and `pd.Period` all qualify; lists and dicts do not.

```python
pd.Series([1, 2], index=[(1, 'a'), (2, 'b')])    # OK -- tuples are hashable
pd.Series([1, 2], index=[[1], [2]])              # TypeError -- lists are not
```

---

# 3. DataFrame

---

## 3.1 What Is a DataFrame?

A **DataFrame** is a 2-D, labeled, column-typed table. Each column is internally a Series sharing the same row index. Different columns may have different dtypes (unlike a 2-D NumPy array).

```
            Columns →
            name      age   salary    hire_date
        ┌──────────┬───────┬────────┬──────────┐
   0    │  Alice   │  25   │ 50000  │ 2022-01-15│
Index   │  Bob     │  30   │ 60000  │ 2021-06-01│   ← rows have a label (index)
        │  Carol   │  35   │ 70000  │ 2019-09-20│
        └──────────┴───────┴────────┴──────────┘
          object   int64   int64   datetime64[ns]
```

## 3.2 Construction Patterns

| From | Example |
|---|---|
| Dict of lists | `pd.DataFrame({'a': [1,2], 'b': [3,4]})` |
| Dict of Series | `pd.DataFrame({'a': s1, 'b': s2})` -- aligns on index |
| List of dicts (records) | `pd.DataFrame([{'a': 1, 'b': 3}, {'a': 2, 'b': 4}])` |
| List of tuples | `pd.DataFrame([(1, 3), (2, 4)], columns=['a', 'b'])` |
| 2-D ndarray | `pd.DataFrame(arr, columns=cols, index=idx)` |
| `pd.DataFrame.from_records` | Specialized for structured arrays / namedtuples |
| `pd.DataFrame.from_dict` | With `orient='index'` for transposed dicts |

```python
df = pd.DataFrame({
    'name':      ['Alice', 'Bob', 'Carol'],
    'age':       [25, 30, 35],
    'salary':    [50000, 60000, 70000],
    'hire_date': pd.to_datetime(['2022-01-15', '2021-06-01', '2019-09-20']),
})

records = [
    {'name': 'Alice', 'age': 25},
    {'name': 'Bob',   'age': 30, 'extra': True},      # missing keys → NaN columns
]
pd.DataFrame(records)
#     name  age  extra
# 0  Alice   25    NaN
# 1    Bob   30   True
```

## 3.3 Key Attributes

| Attribute | Description |
|---|---|
| `df.index` | Row labels (`Index` or `MultiIndex`) |
| `df.columns` | Column labels (also an `Index`) |
| `df.dtypes` | Series of per-column dtypes |
| `df.shape` | `(rows, cols)` |
| `df.size` | Total cell count |
| `df.values` | 2-D ndarray (upcasts to common dtype -- avoid for mixed types) |
| `df.to_numpy(dtype=...)` | Preferred over `.values` |
| `df.axes` | `[index, columns]` |
| `df.empty` | True if zero rows |
| `df.ndim` | Always 2 |

## 3.4 Inspection: info, describe, memory_usage

```python
df.info()
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 3 entries, 0 to 2
# Data columns (total 4 columns):
#  #   Column     Non-Null Count  Dtype
# ---  ------     --------------  -----
#  0   name       3 non-null      object
#  1   age        3 non-null      int64
#  2   salary     3 non-null      int64
#  3   hire_date  3 non-null      datetime64[ns]
# memory usage: 224.0+ bytes

df.describe()                              # numeric columns only by default
df.describe(include='all')                 # include object/categorical
df.describe(include=[np.number])           # only numeric
df.describe(percentiles=[.05, .25, .75, .95])

df.memory_usage(deep=True)                 # deep=True follows object pointers
```

| Method | Returns | Use Case |
|---|---|---|
| `df.head(n)` / `df.tail(n)` | First/last n rows | Quick peek |
| `df.sample(n)` | Random n rows | Spot-check large data |
| `df.info()` | Prints schema | Audit dtypes and NA counts |
| `df.describe()` | Summary stats | Quick distribution sense |
| `df.nunique()` | Unique count per column | Cardinality |
| `df.value_counts()` | Per-row tuple frequency (DataFrame.value_counts in 1.1+) | Compound counts |

## 3.5 Adding and Removing Columns

```python
df['salary_k']    = df['salary'] / 1000             # in-place add
df['bonus']       = 0                                # broadcast scalar
df.insert(1, 'name_lower', df['name'].str.lower())   # insert at specific position

df = df.assign(
    monthly_salary=lambda d: d['salary'] / 12,       # method-chain friendly
    is_senior     =lambda d: d['age'] >= 30,
)

df = df.drop(columns=['bonus', 'name_lower'])
df = df.drop(columns=['x'], errors='ignore')         # silent if missing
```

`assign` returns a copy (good for chaining); `drop` does too unless you pass `inplace=True` (avoid).

## 3.6 Adding and Removing Rows

The legacy `df.append(...)` was removed in Pandas 2.0. Use `concat`:

```python
new_row = pd.DataFrame([{'name': 'Dave', 'age': 28, 'salary': 55000}])
df = pd.concat([df, new_row], ignore_index=True)

df = df.drop(index=[0, 2])                # drop by label
df = df.drop(df[df['age'] < 20].index)    # drop by condition
```

For high-frequency row appends, **build a list of dicts and construct once** -- repeated `concat` is O(n²).

```python
rows = []
for record in stream:
    rows.append({'a': record.x, 'b': record.y})
df = pd.DataFrame(rows)                   # O(n)
```

---

# 4. Index and MultiIndex

---

## 4.1 The Index Object

An `Index` is an immutable, ordered, typed container of labels -- conceptually a `set` plus an order plus a hash table. It sits on the row axis (`df.index`) and the column axis (`df.columns`).

```python
idx = df.index
type(idx)          # <class 'pandas.core.indexes.range.RangeIndex'>

idx[0]             # element access
idx.tolist()       # convert to plain list
idx.name           # axis name
idx.is_unique      # uniqueness check
idx.has_duplicates # opposite of is_unique
```

Indexes are **immutable**: `df.index[0] = 'new'` raises `TypeError`. To change labels, build a new index and reassign (`df.index = new_idx`) or use `df.rename(index=mapping)`.

## 4.2 Specialized Index Types

| Index Class | Element Type | Created By | Notes |
|---|---|---|---|
| `Index` | object / mixed | `pd.Index([...])` | Generic fallback |
| `RangeIndex` | int (lazy range) | Default for new DataFrames | O(1) memory |
| `Int64Index` / `Float64Index` (deprecated) | numeric | `pd.Index([1,2], dtype='int64')` | Now folded into `Index` |
| `DatetimeIndex` | `Timestamp` | `pd.date_range(...)`, `pd.to_datetime(...)` | Time-aware ops |
| `TimedeltaIndex` | `Timedelta` | `pd.timedelta_range(...)` | Durations |
| `PeriodIndex` | `Period` | `pd.period_range(...)` | Time spans |
| `CategoricalIndex` | category codes | `pd.CategoricalIndex(...)` | Memory-efficient labels |
| `IntervalIndex` | `Interval` | output of `pd.cut`/`pd.qcut` | Bins |
| `MultiIndex` | tuple-of-labels | `pd.MultiIndex.from_*` | Hierarchical |

## 4.3 Common Index Operations

```python
idx_a = pd.Index(['a', 'b', 'c', 'd'])
idx_b = pd.Index(['c', 'd', 'e', 'f'])

idx_a.union(idx_b)          # Index(['a','b','c','d','e','f'])
idx_a.intersection(idx_b)   # Index(['c','d'])
idx_a.difference(idx_b)     # Index(['a','b'])
idx_a.symmetric_difference(idx_b)  # Index(['a','b','e','f'])

idx_a.append(idx_b)         # Index(['a','b','c','d','c','d','e','f'])  (duplicates allowed)
idx_a.get_loc('b')          # 1  (positional lookup)
idx_a.get_indexer(['b','d']) # array([1, 3])
```

## 4.4 reset_index, set_index, reindex

| Method | Purpose |
|---|---|
| `set_index(col)` | Promote a column to be the row index |
| `reset_index()` | Demote the index back to a column (creates a `RangeIndex`) |
| `reindex(new_idx)` | Conform to a new index, inserting NaN for missing labels |
| `rename(index=..., columns=...)` | Relabel without restructuring |
| `rename_axis(name)` | Set the name attribute of an axis |

```python
df = pd.DataFrame({'id': [101, 102, 103], 'val': [10, 20, 30]})

df1 = df.set_index('id')          # 'id' becomes the row index
df2 = df1.reset_index()           # 'id' is back as a column
df3 = df1.reindex([101, 999, 102])  # 999 row gets NaN

df = df.rename(columns={'val': 'value'})
df = df.rename_axis('record_id')   # names the index axis
```

`set_index(col, drop=False)` keeps the column as a column too. `reset_index(drop=True)` discards the old index instead of demoting it.

## 4.5 MultiIndex Construction

A `MultiIndex` holds **tuples** of labels, one per row, organized into named **levels**. It enables hierarchical / panel data without resorting to wide tables.

| Constructor | Input |
|---|---|
| `from_arrays(arrays, names)` | Parallel arrays per level |
| `from_tuples(tuples, names)` | Explicit list of tuples |
| `from_product(iterables, names)` | Cartesian product |
| `from_frame(df)` | A DataFrame whose columns become levels |

```python
mi_arrays = pd.MultiIndex.from_arrays(
    [['NYC', 'NYC', 'LA',  'LA'],
     ['Q1',  'Q2',  'Q1',  'Q2']],
    names=['city', 'quarter']
)

mi_product = pd.MultiIndex.from_product(
    [['A', 'B'], [1, 2, 3]],
    names=['letter', 'number']
)
# 6 tuples: (A,1),(A,2),(A,3),(B,1),(B,2),(B,3)

df = pd.DataFrame({'sales': [100, 150, 200, 250]}, index=mi_arrays)
#                 sales
# city quarter
# NYC  Q1         100
#      Q2         150
# LA   Q1         200
#      Q2         250
```

## 4.6 MultiIndex Level Operations

| Method | Effect |
|---|---|
| `mi.get_level_values(level)` | Series of labels at one level |
| `mi.set_levels(new, level=)` | Replace the labels at a level |
| `mi.swaplevel(i, j)` | Swap two levels |
| `mi.reorder_levels(order)` | Arbitrary permutation |
| `mi.droplevel(level)` | Remove a level |
| `mi.sortlevel(level)` | Lexsort by a level |
| `df.sort_index(level=0)` | Sort the row axis by level 0 |
| `df.xs(key, level=)` | Cross-section: extract a slice for one level |

```python
df.index.get_level_values('city')   # Index(['NYC','NYC','LA','LA'])

df.swaplevel('city', 'quarter')     # quarter on top, city below
df.xs('Q1', level='quarter')        # all rows where quarter == 'Q1'
df.droplevel('quarter')              # collapse to a single-level index
```

## 4.7 Sorted vs Unsorted MultiIndex

Slicing a MultiIndex efficiently requires that it is **lexsorted** (sorted by the outer levels). Pandas raises `UnsortedIndexError` for some slice patterns on an unsorted MultiIndex, and others are slow.

```python
df.index.is_monotonic_increasing    # is the MultiIndex lex-sorted?
df = df.sort_index()                # ensure lex-sorted before complex slicing
```

| Operation | Sorted MI | Unsorted MI |
|---|---|---|
| `df.loc[outer_label]` | Fast | Works but slow |
| `df.loc[(outer, inner)]` | Fast | Works |
| `df.loc[outer_a:outer_b]` | Fast | **UnsortedIndexError** |
| `df.loc[pd.IndexSlice[:, inner]]` | Fast | **UnsortedIndexError** |

> Rule of thumb: after building or modifying a MultiIndexed DataFrame, call `sort_index()` once before doing any slicing.

---

# Part 2: dtypes and Missing Data

---

# 5. The Pandas dtype System

---

## 5.1 The Two dtype Families

Pandas supports two parallel dtype universes:

| Family | Backed By | Missing Sentinel | Typical Names |
|---|---|---|---|
| **NumPy-backed** (classic) | `np.ndarray` | `np.nan` (float), `NaT` (datetime), no NA for int/bool | `int64`, `float64`, `bool`, `object`, `datetime64[ns]` |
| **Extension** (modern) | `ExtensionArray` (Pandas or Arrow) | `pd.NA` | `Int64`, `Float64`, `boolean`, `string`, `category`, `ArrowDtype(...)` |

The capitalized names (`Int64`, `Float64`, `Boolean`, `String`) signal **nullable** extension types. They preserve their dtype when missing values are introduced -- unlike the lowercase NumPy versions, where adding an NA to an `int64` column upcasts it to `float64`.

```python
import pandas as pd

s_np  = pd.Series([1, 2, None])
print(s_np.dtype)              # float64   ← NaN forced int → float

s_ext = pd.Series([1, 2, None], dtype='Int64')
print(s_ext.dtype)             # Int64     ← stays integer
print(s_ext[2] is pd.NA)       # True
```

## 5.2 Full dtype Catalog

| Pandas dtype | Storage | NA Sentinel | Notes |
|---|---|---|---|
| `int8`/`int16`/`int32`/`int64` | NumPy | None (no NA) | Adding NA upcasts to float |
| `uint8`/`uint16`/`uint32`/`uint64` | NumPy | None | No negatives |
| `float32`/`float64` | NumPy | `np.nan` | Default for floats |
| `bool` | NumPy | None | Adding NA upcasts to object |
| `object` | NumPy + Python objects | mixed (`None`, `np.nan`) | Catch-all; slowest |
| `datetime64[ns]` | NumPy | `pd.NaT` | Nanosecond resolution |
| `datetime64[ns, tz]` | NumPy + tz info | `pd.NaT` | Timezone-aware |
| `timedelta64[ns]` | NumPy | `pd.NaT` | Durations |
| `Int8`/`Int16`/`Int32`/`Int64` | Extension | `pd.NA` | Nullable integer |
| `UInt8`..`UInt64` | Extension | `pd.NA` | Nullable unsigned |
| `Float32`/`Float64` | Extension | `pd.NA` | Nullable float |
| `boolean` | Extension | `pd.NA` | Nullable bool (lowercase!) |
| `string` | Extension (NumPy or PyArrow) | `pd.NA` | Replaces `object` for text |
| `category` | Extension (`Categorical`) | `pd.NA` | Codes + categories |
| `Sparse[dtype]` | Extension (`SparseArray`) | sparse fill value | Memory-efficient sparse |
| `interval[dtype]` | Extension | NaN-like | Output of `cut`/`qcut` |
| `period[freq]` | Extension | `pd.NaT` | Time spans |
| `ArrowDtype(pa.type)` | Extension (Arrow buffer) | `pd.NA` | PyArrow-backed; see section 7 |

## 5.3 Picking a dtype

| If you have... | Prefer dtype |
|---|---|
| Integers without missing values | `int64` (NumPy) |
| Integers with missing values | `Int64` (nullable) |
| Strings (any kind) | `string` (or `string[pyarrow]`) -- **never** plain `object` |
| Booleans without NA | `bool` |
| Booleans with NA | `boolean` |
| Low-cardinality strings (<10% unique) | `category` |
| Bins from `cut`/`qcut` | `interval` (automatic) |
| Timestamps | `datetime64[ns]` or `datetime64[ns, UTC]` |
| Durations | `timedelta64[ns]` |
| Nested / variable-length list values | `ArrowDtype(pa.list_(pa.int64()))` |

## 5.4 Inspecting and Casting

```python
df.dtypes                              # per-column dtypes
df.select_dtypes(include='number')     # subset by dtype
df.select_dtypes(include=['Int64', 'Float64'])
df.select_dtypes(exclude='object')

df['x'] = df['x'].astype('Int64')      # explicit cast
df = df.astype({'x': 'Int64', 'y': 'string'})

df_clean = df.convert_dtypes()         # auto-promote to nullable extension dtypes
df_obj   = df.infer_objects()           # downgrade object columns where possible
```

`convert_dtypes()` is the easiest way to migrate a legacy NumPy-backed frame to nullable types in one shot.

## 5.5 Type Promotion Rules

When mixing dtypes in arithmetic, Pandas promotes following NumPy plus a nullable layer:

```
bool   →  Int   →  Float   →  complex
                       ↘
                        object  (when any operand is object)

NumPy + Extension: result is the extension version when one side is nullable.
```

```python
pd.Series([1, 2], dtype='int64') + pd.Series([1.5, 2.5])      # → float64
pd.Series([1, 2], dtype='Int64') + pd.Series([1.5, 2.5])      # → Float64 (nullable)
pd.Series([True, False]) + pd.Series([1, 2])                   # → int64
```

---

# 6. Missing Data Semantics

---

## 6.1 The Three Sentinels

| Sentinel | Backed Type | Used For |
|---|---|---|
| `np.nan` | IEEE-754 float NaN | Missing value in NumPy-backed numeric columns |
| `pd.NaT` | "Not a Time" | Missing in datetime / timedelta / period |
| `pd.NA` | Singleton | Missing in nullable extension types |

```python
import numpy as np
import pandas as pd

s_float    = pd.Series([1.0, np.nan, 3.0])              # uses np.nan
s_dt       = pd.Series(pd.to_datetime(['2024-01-01', None]))   # uses NaT
s_nullable = pd.Series([1, None, 3], dtype='Int64')      # uses pd.NA
```

## 6.2 Detecting Missing Values

`==` does **not** detect missing values; always use `isna()` / `notna()`.

```python
np.nan == np.nan          # False  (IEEE-754 quirk)
pd.NA  == pd.NA           # pd.NA  (propagates rather than returning True)

s.isna()                   # boolean mask of missing
s.notna()                  # complement
df.isna().sum()            # missing count per column
df.isna().mean() * 100     # missing % per column
df.isna().any(axis=None)   # any missing anywhere?
```

Aliases: `isnull` / `notnull` are identical to `isna` / `notna`.

## 6.3 NA-Aware Operations

Most reduction and arithmetic operations skip NA by default:

```python
pd.Series([1, 2, np.nan]).sum()           # 3.0
pd.Series([1, 2, np.nan]).sum(skipna=False)  # NaN

pd.Series([1, 2, pd.NA], dtype='Int64').sum()  # 3
pd.Series([True, False, pd.NA], dtype='boolean').any()  # True
```

| Operator | `np.nan` Behavior | `pd.NA` Behavior |
|---|---|---|
| `1 + NaN` | NaN | NA |
| `NaN > 0` | False (silent!) | NA (correct three-valued logic) |
| `True \| NaN` | True | True (Kleene logic) |
| `False \| NaN` | False (wrong!) | NA |
| `True & NaN` | NaN | NA |
| `False & NaN` | NaN | False |

`pd.NA` implements proper three-valued (Kleene) logic; `np.nan` does not. This is one of the biggest reasons to prefer nullable dtypes when correctness matters.

## 6.4 Filling Missing Values

| Method | Effect |
|---|---|
| `df.fillna(value)` | Replace NA with a constant or per-column dict |
| `df.ffill(limit=n)` | Forward-fill (carry last observation forward) |
| `df.bfill(limit=n)` | Back-fill |
| `df.interpolate(method='linear')` | Numerical interpolation |
| `df.replace(np.nan, value)` | Generic replacement |
| `df.combine_first(other)` | Use `other`'s values where `df` is NA |

```python
df.fillna(0)
df.fillna({'price': 0, 'name': 'unknown'})        # column-specific
df.ffill().bfill()                                 # bidirectional fill
df['x'].interpolate(method='linear')               # 1.0, NaN, 3.0 → 1.0, 2.0, 3.0
df['x'].interpolate(method='time')                 # interpolation respecting datetime index

df = df.dropna(subset=['critical_col'])           # drop rows missing critical column
df = df.dropna(thresh=3)                          # keep rows with at least 3 non-NA
```

## 6.5 Pitfalls

```python
# 1. Comparing to NaN/NA never works
s == np.nan        # all False -- use s.isna()

# 2. NaN forces int → float
pd.Series([1, 2, None])              # float64
pd.Series([1, 2, None], dtype='Int64')  # Int64 (correct)

# 3. Boolean indexing with NA in the mask
mask = pd.Series([True, pd.NA, False], dtype='boolean')
df[mask]    # Pandas 2.x: raises if NAs are present -- coerce first:
df[mask.fillna(False)]

# 4. fillna on a categorical with a non-category value fails
cat = pd.Series(pd.Categorical(['a', 'b', None], categories=['a', 'b']))
cat.fillna('z')                         # ValueError  (z not in categories)
cat = cat.cat.add_categories(['z'])
cat.fillna('z')                         # OK
```

---

# 7. PyArrow Backend

---

## 7.1 Why PyArrow?

The PyArrow backend (Pandas 2.0+) replaces NumPy buffers with **Apache Arrow** columnar buffers. Benefits:

| Benefit | Impact |
|---|---|
| Native missing values for **all** dtypes | No more int → float on NA |
| First-class `string` storage | 10-100x faster string ops, 2-10x less memory |
| Nested types (`list`, `struct`, `map`) | First-class support inside cells |
| Zero-copy interop with Parquet, Polars, DuckDB, Spark | Cheap data exchange |
| Decimal, fixed-size binary, dictionary | Types NumPy never had |
| Modern compute kernels (Arrow C++ kernels) | Often faster than NumPy for strings, datetimes |

## 7.2 Three Ways to Opt In

```python
import pandas as pd
import pyarrow as pa

# 1. Per-column ArrowDtype
s = pd.Series([1, 2, 3], dtype=pd.ArrowDtype(pa.int64()))

# 2. Arrow-backed string globally
pd.options.future.infer_string = True
df = pd.read_csv('data.csv')        # text columns now string[pyarrow]

# 3. dtype_backend on read
df = pd.read_csv('data.csv', dtype_backend='pyarrow')
df = pd.read_parquet('data.parquet', dtype_backend='pyarrow')
df = pd.DataFrame({'a': [1, 2, 3]}).convert_dtypes(dtype_backend='pyarrow')
```

## 7.3 Common ArrowDtypes

| Arrow Type | `ArrowDtype` Form | Pandas Use Case |
|---|---|---|
| `pa.int64()` | `pd.ArrowDtype(pa.int64())` | Nullable int |
| `pa.float64()` | `pd.ArrowDtype(pa.float64())` | Nullable float |
| `pa.string()` | `pd.ArrowDtype(pa.string())` | Strings |
| `pa.bool_()` | `pd.ArrowDtype(pa.bool_())` | Nullable bool |
| `pa.timestamp('ns')` | `pd.ArrowDtype(pa.timestamp('ns'))` | Datetime |
| `pa.timestamp('ns', tz='UTC')` | `pd.ArrowDtype(...)` | Aware datetime |
| `pa.date32()` | `pd.ArrowDtype(pa.date32())` | Date only |
| `pa.duration('ns')` | `pd.ArrowDtype(...)` | Timedelta |
| `pa.decimal128(p, s)` | `pd.ArrowDtype(...)` | Exact decimal arithmetic |
| `pa.list_(pa.int64())` | `pd.ArrowDtype(...)` | List values per row |
| `pa.struct([('x', pa.int64()), ('y', pa.string())])` | `pd.ArrowDtype(...)` | Struct values |
| `pa.dictionary(pa.int32(), pa.string())` | `pd.ArrowDtype(...)` | Categorical-like |

## 7.4 NumPy vs PyArrow String Performance

```python
import pandas as pd, numpy as np, time

n = 1_000_000
words = np.random.choice(['apple', 'banana', 'cherry', 'date'], n)

s_obj   = pd.Series(words, dtype='object')
s_str   = pd.Series(words, dtype='string')                                 # PyArrow if available
s_arrow = pd.Series(words, dtype=pd.ArrowDtype(pa.string()))

for s in (s_obj, s_str, s_arrow):
    t = time.perf_counter()
    s.str.upper()
    print(s.dtype, f'{time.perf_counter() - t:.4f}s')

# Typical (Pandas 2.2):
#   object              0.180s
#   string              0.050s
#   string[pyarrow]     0.020s
```

| Operation | object | string[pyarrow] | Speedup |
|---|---|---|---|
| `.str.upper()` (1M rows) | ~180 ms | ~20 ms | 9x |
| `.str.contains('a')` | ~120 ms | ~15 ms | 8x |
| Equality filter | ~150 ms | ~10 ms | 15x |
| Memory (1M rows of 6-char strings) | ~80 MB | ~12 MB | 6.7x |

## 7.5 Caveats and Gotchas

- Some Pandas methods still convert PyArrow back to NumPy under the hood -- **if** you depend on strict `ArrowDtype` preservation, test with `print(df.dtypes)` after each step.
- `ArrowDtype(pa.list_(...))` cells contain `np.ndarray`-like Arrow lists, not Python lists. Use `.list` accessor (Pandas 2.1+) for vectorized access: `s.list.len()`, `s.list[0]`.
- A column declared `string` may resolve to `string[python]` or `string[pyarrow]` depending on whether `pyarrow` is installed and `pd.options.future.infer_string` is enabled.
- Arrow-backed datetimes use distinct dtypes from NumPy datetime64 -- some downstream libraries (older matplotlib, statsmodels) may not handle them yet.
- `dtype_backend='pyarrow'` on `read_csv` is significantly faster for wide string-heavy frames; benchmark before assuming.

---

# Part 3: Selecting and Filtering

---

# 8. The Four Indexers

---

## 8.1 At a Glance

Pandas exposes four primary ways to access data, plus the bracket operator. Each has distinct semantics that a working Pandas developer must internalize.

| Indexer | Lookup Type | Slice End | Returns | Best For |
|---|---|---|---|---|
| `df[...]` | Mixed (label for cols, position for row slices) | Position-exclusive | Series / DataFrame | Column selection, simple row slicing |
| `df.loc[row, col]` | **Label-based** | **Inclusive** | Series / DataFrame | Most general selection |
| `df.iloc[row, col]` | **Position-based** | Exclusive | Series / DataFrame | Ordinal position lookups |
| `df.at[row, col]` | Label, scalar only | N/A | Scalar | Single-cell read/write (fastest) |
| `df.iat[row, col]` | Position, scalar only | N/A | Scalar | Single-cell read/write (fastest) |

## 8.2 The Bracket Operator: `df[...]`

The `[]` operator is overloaded in ways that are convenient but inconsistent:

```python
df = pd.DataFrame({'a': [1,2,3,4], 'b': [5,6,7,8]}, index=['w','x','y','z'])

df['a']             # column 'a' as a Series
df[['a', 'b']]      # DataFrame with both columns
df[0:2]             # rows by **positional** slice → 'w','x' rows
df['w':'y']         # rows by **label** slice (inclusive)  → 'w','x','y' rows
df[df['a'] > 2]     # boolean row selection
df[lambda d: d['a'] > 2]  # callable row selection
```

Avoid `df[...]` for ambiguous cases (e.g. if your column labels happen to be integers); reach for `loc` / `iloc` instead.

## 8.3 `loc` -- Label-Based, Inclusive

```python
df.loc['x']                     # row 'x' as a Series
df.loc['x', 'a']                # scalar at ('x','a')
df.loc[['x', 'z'], 'a']         # subset rows, single column
df.loc['w':'y']                 # rows w..y inclusive
df.loc['w':'y', 'a':'b']        # row & column slices, both inclusive
df.loc[df['a'] > 2]             # boolean mask
df.loc[df['a'] > 2, 'b']        # boolean rows, single column
df.loc[lambda d: d['a'] > 2]    # callable
df.loc[:, 'a'] = 0               # assignment also works
```

Important: a slice in `.loc` includes **both** endpoints. This differs from Python and from `iloc`.

## 8.4 `iloc` -- Position-Based, Exclusive

```python
df.iloc[0]                # first row as a Series
df.iloc[-1]               # last row
df.iloc[0, 0]             # scalar at first row, first column
df.iloc[0:2]              # first two rows (exclusive end)
df.iloc[[0, 2]]           # fancy selection -- rows 0 and 2
df.iloc[:, 0:2]           # all rows, first two columns
df.iloc[lambda d: [0, 2]] # callable returning positions
```

## 8.5 `at` and `iat` -- Single-Cell Fast Path

When you only need to read or write **one** value, `at` / `iat` skip the general dispatch machinery and are several times faster than `loc` / `iloc`:

```python
df.at['x', 'a']        # label lookup, scalar
df.iat[0, 0]           # positional lookup, scalar
df.at['x', 'a'] = 99   # in-place scalar assignment
```

If you find yourself looping with `at` / `iat`, consider whether a vectorized expression would be faster overall. The fast path matters most inside event-driven code where cell access is unavoidable.

## 8.6 Common Pitfalls

```python
# 1. Slice endpoint differences
df = pd.DataFrame({'v': [10, 20, 30]}, index=[100, 200, 300])
df.loc[100:200]   # TWO rows  (label, inclusive)
df.iloc[0:1]      # ONE row   (position, exclusive)

# 2. Single-label loc returns a Series; double-bracket returns a DataFrame
df.loc[100]       # Series
df.loc[[100]]     # DataFrame

# 3. .loc assignment with a new column auto-creates it
df.loc[:, 'new_col'] = 0   # creates 'new_col' if absent

# 4. Chained indexing breaks for assignment
df[df['v'] > 0]['v'] = 99   # SettingWithCopyWarning -- may not modify df
df.loc[df['v'] > 0, 'v'] = 99  # always works

# 5. Boolean mask length must match
df.loc[[True, False]]   # IndexError -- mask shorter than df
```

---

# 9. Boolean Selection, query, eval, where, mask

---

## 9.1 Boolean Indexing Basics

```python
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Carol', 'Dave'],
    'age':  [25, 30, 35, 40],
    'dept': ['Eng', 'Sales', 'Eng', 'Sales'],
})

df[df['age'] > 28]
df[(df['age'] > 28) & (df['dept'] == 'Eng')]            # parentheses are required
df[~df['name'].isin(['Alice', 'Bob'])]
df[df['name'].str.startswith('C')]
df[df['age'].between(25, 35, inclusive='both')]
```

| Operator | Meaning |
|---|---|
| `&` | Logical AND (element-wise) |
| `\|` | Logical OR |
| `^` | Logical XOR |
| `~` | Logical NOT |
| `and` / `or` | **Wrong** -- raises `ValueError: truth value ambiguous` |

## 9.2 isin, between, notin patterns

```python
df['dept'].isin(['Eng', 'Ops'])               # boolean Series
df[~df['dept'].isin(['Sales'])]                # not-in
df[df['age'].between(30, 40, inclusive='left')]   # 30 <= age < 40
```

For multi-column membership, use `MultiIndex.isin` or merge-based filtering:

```python
keys = pd.DataFrame({'name': ['Alice', 'Carol'], 'dept': ['Eng', 'Eng']})
df.merge(keys, on=['name', 'dept'])           # inner-join filter
```

## 9.3 `query()` -- String Expression Filter

`query` parses a string into a vectorized expression evaluated by `numexpr` (when available) -- often faster on large frames and always more readable.

```python
df.query('age > 28 and dept == "Eng"')
df.query('name in ["Alice", "Bob"]')
df.query('age > @min_age')                # @ references a Python variable

threshold = 30
df.query('age >= @threshold')

df.query('`first name` == "Alice"')        # backticks for column names with spaces
```

| Capability | Supports |
|---|---|
| `==`, `!=`, `<`, `<=`, `>`, `>=` | Yes |
| `and`, `or`, `not` | Yes (Python words, not `&` `\|` `~`) |
| `in`, `not in` | Yes |
| `@variable` | Reference Python locals |
| Backticks ` ` ` for column names with spaces | Yes |
| String methods (`str.startswith`) | No -- fall back to `df[mask]` |

## 9.4 `eval()` -- Vectorized Expression Evaluation

`eval` lets you compute a new column or expression as a string, again with a `numexpr` fast path:

```python
df.eval('total = age * salary', inplace=False)
df.eval('young = age < 30')
df = df.eval('''
    salary_k     = salary / 1000
    high_earner  = salary > 60000
''')

s = df.eval('age + salary')              # returns a Series
df.eval('x + y * 2', engine='python')    # fallback if numexpr unavailable
```

For small DataFrames (< ~10K rows), plain Python expressions are typically just as fast or faster -- `eval`/`query` shine on large columnar workloads.

## 9.5 `where` and `mask` -- Conditional Replacement

| Method | Keep Where Condition Is | Replace Where Condition Is |
|---|---|---|
| `df.where(cond, other)` | True | False (replace with `other`) |
| `df.mask(cond, other)` | False | True (replace with `other`) |

```python
df['age'].where(df['age'] >= 18, other=0)        # zero out under-18
df['age'].mask(df['age'] >= 65, other=64)        # cap age at 64

df.where(df > 0)                                  # negatives → NaN
df.where(df > 0, other=df.median(numeric_only=True))   # negatives → column median
```

`where` and `mask` always return the **same shape** -- they replace, they do not filter rows out.

## 9.6 Performance Comparison

For a 10M-row DataFrame on a modern laptop (rough numbers):

| Approach | Time | When To Use |
|---|---|---|
| `df[df['x'] > 0]` | ~80 ms | General purpose |
| `df.query('x > 0')` (numexpr) | ~25 ms | Large numeric frames |
| `df.loc[mask]` (precomputed mask) | ~80 ms | When mask is reused |
| `df.where(df > 0)` | ~60 ms | Replace, not filter |
| `df['x'].clip(lower=0)` | ~30 ms | Vectorized clamping |

---

# 10. MultiIndex Slicing Patterns

---

## 10.1 Setup

```python
import pandas as pd
import numpy as np

mi = pd.MultiIndex.from_product(
    [['NYC', 'LA', 'CHI'], ['2023', '2024'], ['Q1', 'Q2', 'Q3', 'Q4']],
    names=['city', 'year', 'quarter']
)
df = pd.DataFrame({'sales': np.random.randint(50, 200, size=len(mi))}, index=mi)
df = df.sort_index()    # crucial: enables fast slicing on every level
```

## 10.2 The Five Slicing Patterns

| Pattern | Syntax | What It Does |
|---|---|---|
| **Single outer label** | `df.loc['NYC']` | Sub-DataFrame; outer level dropped |
| **Tuple of labels** | `df.loc[('NYC', '2024', 'Q1')]` | Single row (Series) |
| **Partial tuple** | `df.loc[('NYC', '2024')]` | Sub-DataFrame at the prefix |
| **Outer-level slice** | `df.loc['CHI':'NYC']` | Range across outer level (sorted!) |
| **Inner-level slice** | `df.loc[pd.IndexSlice[:, '2024', 'Q1':'Q2']]` | Slice across any levels |

```python
df.loc['NYC']                              # all NYC rows
df.loc[('NYC', '2024')]                    # NYC + 2024 → Q1..Q4
df.loc[('NYC', '2024', 'Q3')]              # one scalar row
df.loc['CHI':'NYC']                        # cities CHI..NYC
df.loc[pd.IndexSlice[:, '2024', :]]        # all cities, 2024 only
df.loc[pd.IndexSlice[:, '2024', 'Q1':'Q2']]  # 2024 first half
```

The `pd.IndexSlice` helper (often aliased as `idx = pd.IndexSlice`) is the only way to slice across multiple levels at once.

## 10.3 `.xs()` -- Cross-Section

`xs` is a more readable alternative to `IndexSlice` for fetching a single inner-level value:

```python
df.xs('Q1', level='quarter')               # all rows where quarter == 'Q1'
df.xs(('LA', 'Q1'), level=['city', 'quarter'])
df.xs('Q1', level='quarter', drop_level=False)  # keep the level in the index
```

| Method | Strength |
|---|---|
| `df.loc[outer]` | Cleanest for outer-only slices |
| `df.loc[pd.IndexSlice[...]]` | Most expressive; needed for ranges |
| `df.xs(key, level=)` | Most readable for single inner key |
| `df.query('level_name == ...')` | Works with any level by name |

## 10.4 Level Manipulation

```python
df.swaplevel('city', 'year')                # swap outer two levels (re-sort after!)
df.reorder_levels(['quarter', 'city', 'year'])

df.sort_index(level=['city', 'year'])
df.sort_index(level='quarter', sort_remaining=False)

df.droplevel('quarter')                    # collapse to (city, year) MultiIndex

df.unstack('quarter')                      # quarters become columns
df.stack('quarter')                        # reverse
```

## 10.5 Selecting Rows via Level Names

When level names are set, you can use them in `query`, `groupby`, and elsewhere:

```python
df.query('city == "NYC" and quarter in ["Q1","Q2"]')
df.groupby(level='city').sum()
df.groupby(['city', 'year']).sum()
```

## 10.6 Pitfalls

```python
# 1. Forgetting to sort_index() before slicing
df_unsorted.loc['CHI':'NYC']    # UnsortedIndexError or wrong rows

# 2. Tuple vs list semantics
df.loc[('NYC', '2024', 'Q1')]   # one row (tuple = full key)
df.loc[['NYC', 'LA']]           # multiple outer labels (list = collection)

# 3. Single-element tuple ambiguity
df.loc['NYC',]                  # deprecated -- use df.loc['NYC'] or df.loc[('NYC',)]

# 4. Slice over inner level requires IndexSlice or xs
df.loc[:, 'Q1':'Q2']            # WRONG -- this slices columns!
df.loc[pd.IndexSlice[:, :, 'Q1':'Q2']]   # right
```

---

# 11. Copy-on-Write, Views, and SettingWithCopyWarning

---

## 11.1 The Historical Problem

Pre-2.0 Pandas had ambiguous semantics for whether an indexed subset returned a view or a copy. This led to the infamous `SettingWithCopyWarning`:

```python
sub = df[df['x'] > 0]      # may be a view OR a copy -- depends on internals
sub['y'] = 0                # SettingWithCopyWarning: did this mutate df or not?
```

The warning exists because the answer was implementation-dependent and could change between versions.

## 11.2 Copy-on-Write (CoW)

Pandas 2.0 introduced **opt-in CoW**; Pandas 3.0 makes it the default. Under CoW:

- Every indexing operation conceptually returns an independent object.
- Internally, data is shared lazily (zero-copy) via reference counting.
- A copy is materialized **only on the first write** to the shared buffer.
- This makes behavior deterministic and eliminates `SettingWithCopyWarning`.

```python
pd.options.mode.copy_on_write = True       # opt-in for 2.x; default in 3.0

sub = df[df['x'] > 0]
sub['y'] = 0                                 # never mutates df, no warning
```

| Operation | Pre-CoW | CoW |
|---|---|---|
| `df2 = df` | Reference (mutating df2 mutates df) | Reference (same) |
| `df2 = df.copy()` | Independent copy | Independent copy |
| `s = df['col']` | View; mutating may or may not affect df | Effectively a copy on write |
| `sub = df.loc[mask]` | Sometimes view, sometimes copy | Always independent on write |
| Chained assignment | May silently fail | Raises `ChainedAssignmentError` |

## 11.3 Views vs Copies (Pre-CoW Recap)

Under the legacy model, **basic indexing** typically returns a view; **boolean / fancy indexing** returns a copy.

```python
s = pd.Series([1, 2, 3, 4, 5])

view  = s[1:4]            # view -- modifying view modifies s
copy  = s[[1, 2, 3]]      # copy -- fancy indexing
mask  = s[s > 2]          # copy -- boolean indexing

view[1] = 99              # s[2] is now 99
copy[1] = -1              # s unchanged
```

CoW makes all of these behave like copies on the first write -- read access remains zero-copy.

## 11.4 The Right Way to Modify

```python
# Always assign through .loc with the original frame
df.loc[df['x'] > 0, 'y'] = 0
df.loc[df['name'] == 'Alice', ['salary', 'bonus']] = [100_000, 5_000]

# Build a transformed copy and reassign
df = df.assign(scaled=lambda d: d['x'] * 100)

# Force an explicit copy when in doubt
sub = df[df['x'] > 0].copy()
sub['y'] = 0
```

## 11.5 ChainedAssignmentError

When CoW is on, the following patterns raise instead of silently misbehaving:

```python
pd.options.mode.copy_on_write = True

df['x'][0] = 99                         # ChainedAssignmentError
df[df['x'] > 0]['y'] = 99               # ChainedAssignmentError
df.loc[df['x'] > 0]['y'] = 99           # ChainedAssignmentError
```

The fix in every case is the single-step `loc` form:

```python
df.loc[0, 'x'] = 99
df.loc[df['x'] > 0, 'y'] = 99
```

## 11.6 Memory Implications

CoW does **not** force copies on read -- it preserves the zero-copy benefits of NumPy slicing. The `.copy()` method, in turn, is more important than ever as the explicit signal "I want my own data":

```python
# Read-only path -- no copy made under CoW
sub_for_inspection = df[df['x'] > 0]
print(sub_for_inspection.describe())
print(sub_for_inspection.head())

# Mutation path -- explicit copy is good practice
sub_for_mutation = df[df['x'] > 0].copy()
sub_for_mutation['new'] = 0
```

## 11.7 Migration Checklist

To prepare a codebase for CoW (and Pandas 3.0):

1. Enable `pd.options.mode.copy_on_write = True` in tests.
2. Replace all `df[mask][col] = value` with `df.loc[mask, col] = value`.
3. Stop relying on side effects from views: `s = df['col']; s[0] = 99` no longer mutates `df`.
4. Replace `df.fillna(..., inplace=True)` with `df = df.fillna(...)`.
5. Replace `df.append(...)` with `pd.concat([df, ...], ignore_index=True)`.
6. Run the suite under `-W error::FutureWarning` to surface deprecations early.

---

# Part 4: Cleaning and Transformation

---

# 12. Sorting, Ranking, Duplicates

---

## 12.1 sort_values and sort_index

| Method | Sorts By | Common Parameters |
|---|---|---|
| `sort_values(by, ...)` | Column values | `ascending`, `kind`, `na_position`, `key` |
| `sort_index(axis=, level=, ...)` | Index labels | `axis`, `level`, `ascending`, `sort_remaining`, `key` |

```python
df.sort_values('age')                         # ascending by 'age'
df.sort_values('age', ascending=False)
df.sort_values(['dept', 'age'], ascending=[True, False])

df.sort_values('name', key=lambda s: s.str.lower())     # case-insensitive
df.sort_values('age', na_position='first')              # NaNs first

df.sort_index()                               # by row index
df.sort_index(axis=1)                          # by column labels
df.sort_index(level='city')                    # MultiIndex by one level
```

## 12.2 Sort Algorithms

The `kind` parameter selects the underlying sort:

| `kind` | Stable | Time Complexity | Use Case |
|---|---|---|---|
| `'quicksort'` | No | O(n log n) avg | Default; fastest in practice |
| `'mergesort'` | **Yes** | O(n log n) | Need stability or sorting by multiple keys later |
| `'heapsort'` | No | O(n log n) | Rarely used |
| `'stable'` | Yes | O(n log n) | Alias for mergesort |

```python
df.sort_values('dept', kind='stable')         # preserves original order within ties
```

## 12.3 nlargest and nsmallest

For "top N" queries, these are faster than `sort_values().head()` because they avoid sorting the whole DataFrame:

```python
df.nlargest(5, 'salary')                       # top 5 highest-paid
df.nsmallest(3, 'age')                         # 3 youngest
df.nlargest(5, ['salary', 'age'], keep='all')  # break ties by 'age', keep all ties
```

| `keep` | Behavior on Ties |
|---|---|
| `'first'` | First occurrence wins (default) |
| `'last'` | Last occurrence wins |
| `'all'` | Keep all ties (may return more than n rows) |

## 12.4 Ranking

`rank` assigns ordinal ranks to values. Useful for percentiles, ordinal-scale features, and tie handling.

| `method` | Tie Handling |
|---|---|
| `'average'` (default) | Average of tied ranks |
| `'min'` | Lowest of the tied ranks |
| `'max'` | Highest of the tied ranks |
| `'first'` | Order of appearance |
| `'dense'` | Like `min`, but ranks always increase by 1 |

```python
s = pd.Series([10, 20, 20, 40, 50])
s.rank(method='average')   # [1, 2.5, 2.5, 4, 5]
s.rank(method='min')       # [1, 2, 2, 4, 5]
s.rank(method='dense')     # [1, 2, 2, 3, 4]
s.rank(pct=True)           # rank as a percentile (0..1)

df['percentile'] = df.groupby('dept')['salary'].rank(pct=True)
```

## 12.5 Duplicates

| Method | Returns |
|---|---|
| `df.duplicated(subset=None, keep='first')` | Boolean Series flagging duplicate rows |
| `df.drop_duplicates(subset=None, keep='first')` | DataFrame with duplicates removed |
| `df['col'].unique()` | NumPy array of distinct values |
| `df['col'].nunique(dropna=True)` | Count of distinct values |
| `df['col'].value_counts()` | Frequency table |
| `df.value_counts()` | Frequency table over rows (whole DataFrame) |

```python
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Alice', 'Bob'],
    'age':  [25, 30, 25, 31],
})

df.duplicated()                               # [False, False, True, False]
df.duplicated(subset='name')                  # [False, False, True, True]
df.duplicated(subset='name', keep='last')     # [True, True, False, False]
df.duplicated(subset='name', keep=False)      # all duplicates → True

df.drop_duplicates(subset='name', keep='last')

df['name'].value_counts(normalize=True)       # frequencies
df['name'].value_counts(dropna=False)         # include NaN bucket
```

---

# 13. Type Conversion

---

## 13.1 The `astype` Workhorse

```python
df['age']     = df['age'].astype('Int64')                # nullable int
df['name']    = df['name'].astype('string')               # PyArrow string if available
df['flag']    = df['flag'].astype('boolean')              # nullable bool
df['cat']     = df['cat'].astype('category')              # categorical
df['arr_int'] = df['arr_int'].astype(pd.ArrowDtype(pa.int64()))

df = df.astype({'age': 'Int64', 'name': 'string'})        # multi-column dict form
```

`astype` raises on invalid conversions by default; pass `errors='ignore'` to silently keep the original column.

## 13.2 The Specialized Converters

| Function | Input Domain | Special Behavior |
|---|---|---|
| `pd.to_numeric(s, errors='coerce')` | Strings, mixed | Bad values → `NaN` (or raise / ignore) |
| `pd.to_datetime(s, format=, utc=, errors=)` | Strings, ints, dicts | Format inference; supports `errors='coerce'` |
| `pd.to_timedelta(s, unit=)` | Strings, numbers | Parses `'5 days'`, `'00:30:00'`, etc. |

```python
pd.to_numeric(['1', '2', 'bad', '4'], errors='coerce')   # [1.0, 2.0, NaN, 4.0]
pd.to_numeric(['1', '2', '3'], downcast='integer')       # int8 if possible

pd.to_datetime(['2024-01-01', '2024-13-01'], errors='coerce')   # bad date → NaT
pd.to_datetime(['1/13/2024', '2/14/2024'], format='%m/%d/%Y')
pd.to_datetime(['2024-01-01 12:00'], utc=True)            # UTC-aware
pd.to_datetime(df[['year', 'month', 'day']])              # from a 3-column frame
pd.to_datetime(1_700_000_000, unit='s')                   # from epoch

pd.to_timedelta('2 days 3 hours')                          # → Timedelta
pd.to_timedelta(df['millis'], unit='ms')
```

## 13.3 `convert_dtypes` and `infer_objects`

| Method | Effect |
|---|---|
| `df.convert_dtypes()` | Promote everything to the best **nullable** extension dtype |
| `df.convert_dtypes(dtype_backend='pyarrow')` | Promote to PyArrow-backed types |
| `df.infer_objects()` | Downgrade `object` columns to inferred NumPy dtypes (best-effort) |

```python
df_old = pd.DataFrame({
    'a': pd.array([1, 2, None], dtype='object'),
    'b': pd.array(['x', 'y', None], dtype='object'),
    'c': [True, False, None],
})

df_old.dtypes
# a    object
# b    object
# c    object

df_old.convert_dtypes().dtypes
# a     Int64
# b    string
# c    boolean
```

## 13.4 Downcasting Numeric Columns

`pd.to_numeric` with `downcast=` shrinks columns to the smallest dtype that fits:

```python
df['user_id'] = pd.to_numeric(df['user_id'], downcast='unsigned')   # uint8/16/32
df['count']   = pd.to_numeric(df['count'],   downcast='integer')
df['ratio']   = pd.to_numeric(df['ratio'],   downcast='float')      # float32 if possible
```

| Original | Downcast Target |
|---|---|
| int64 fitting in int8 | int8 (8x memory savings) |
| int64 with negatives, fitting in int16 | int16 |
| float64 within float32 precision | float32 |

---

# 14. The .str Accessor

---

## 14.1 What It Is

`Series.str` is a vectorized string namespace. It dispatches to NumPy, PyArrow, or Python depending on the underlying dtype. All operations are NA-aware.

```python
s = pd.Series(['  Alice  ', 'BOB', None, 'carol-Jones'])
```

## 14.2 Cleanup Operations

| Method | Effect |
|---|---|
| `s.str.lower()` / `upper()` / `title()` / `capitalize()` / `swapcase()` | Case conversion |
| `s.str.strip()` / `lstrip()` / `rstrip()` | Whitespace removal |
| `s.str.normalize('NFKC')` | Unicode normalization |
| `s.str.pad(width, side, fillchar)` | Pad to width |
| `s.str.zfill(width)` | Zero-pad numbers |
| `s.str.center(width)` | Center within width |

```python
s.str.strip().str.lower()
# 0          alice
# 1            bob
# 2           <NA>
# 3    carol-jones
```

## 14.3 Search and Match

| Method | Returns | Notes |
|---|---|---|
| `s.str.contains(pat, regex=True)` | boolean | Regex by default |
| `s.str.startswith(prefix)` | boolean | No regex |
| `s.str.endswith(suffix)` | boolean | No regex |
| `s.str.match(pat)` | boolean | Anchored at start |
| `s.str.fullmatch(pat)` | boolean | Must match entire string |
| `s.str.find(sub)` | int (-1 if absent) | Position |
| `s.str.count(pat)` | int | Number of matches |

```python
s.str.contains(r'^[A-Z]')                # [False, True, NA, False]
s.str.contains('alice', case=False, na=False)   # NA → False
s.str.contains('alice', flags=re.IGNORECASE)
s.str.startswith('B')
```

## 14.4 Split, Slice, Replace

```python
s.str[0]                       # first character of each string
s.str[1:4]                     # slice each string
s.str.slice(0, 3)               # explicit form

s.str.split('-')               # returns lists per row
s.str.split('-', expand=True)  # returns a DataFrame -- one column per piece
s.str.split('-', n=1, expand=True)   # only first split

s.str.replace('o', '0')                  # literal (regex=False since pandas 2.x)
s.str.replace(r'\s+', '_', regex=True)
s.str.removeprefix('Mr. ')               # Pandas 1.4+
s.str.removesuffix('.csv')

s.str.cat(['a', 'b', 'c', 'd'], sep='-', na_rep='NA')   # concatenate
```

## 14.5 Regex Extraction

| Method | Output Shape |
|---|---|
| `s.str.extract(pat)` | DataFrame: one column per capture group |
| `s.str.extractall(pat)` | DataFrame: rows for **every** match (MultiIndex) |
| `s.str.findall(pat)` | Series of lists |
| `s.str.split(pat, regex=True, expand=True)` | DataFrame |

```python
s = pd.Series(['John 25', 'Jane 30', 'Joe', None])

s.str.extract(r'(?P<name>\w+)\s+(?P<age>\d+)')
#     name   age
# 0   John   25
# 1   Jane   30
# 2    NaN  NaN
# 3    NaN  NaN

s.str.extractall(r'(\d+)')        # all numbers as separate rows
```

## 14.6 Length and Membership

```python
s.str.len()                       # length of each string (NaN for NA)
s.str.isalpha()
s.str.isdigit()
s.str.isnumeric()
s.str.isalnum()
s.str.isspace()
s.str.isupper() / s.str.islower()
```

## 14.7 PyArrow String Performance Caveat

Operations executed against `string[pyarrow]` typically run via Arrow's compute kernels and are noticeably faster than against `object` strings, but a few methods (e.g. complex regex, `removesuffix` on older PyArrow versions) fall back to Python; benchmark in your hot path.

---

# 15. The .dt Accessor

---

## 15.1 What It Is

`Series.dt` exposes datetime-aware methods on Series of `datetime64[ns]`, `datetime64[ns, tz]`, `timedelta64[ns]`, and `period[freq]` dtypes.

```python
df['ts'] = pd.to_datetime(['2024-01-15 10:30',
                            '2024-06-30 23:59',
                            '2025-02-28 00:00'])
```

## 15.2 Component Access

| Property | Example |
|---|---|
| `s.dt.year` / `month` / `day` | 2024 / 6 / 30 |
| `s.dt.hour` / `minute` / `second` / `microsecond` / `nanosecond` | Time parts |
| `s.dt.dayofweek` (alias `weekday`) | 0=Monday .. 6=Sunday |
| `s.dt.dayofyear` | Day of year (1..366) |
| `s.dt.weekofyear` / `isocalendar()` | ISO week |
| `s.dt.quarter` | 1..4 |
| `s.dt.is_month_start` / `is_month_end` | Boolean |
| `s.dt.is_quarter_start` / `is_quarter_end` | Boolean |
| `s.dt.is_year_start` / `is_year_end` | Boolean |
| `s.dt.is_leap_year` | Boolean |
| `s.dt.days_in_month` | 28..31 |

```python
df['ts'].dt.year                    # [2024, 2024, 2025]
df['ts'].dt.month_name()            # ['January', 'June', 'February']
df['ts'].dt.day_name(locale='en_US')
df['ts'].dt.isocalendar()           # DataFrame with year, week, day
```

## 15.3 Rounding and Truncation

```python
df['ts'].dt.normalize()             # set time to 00:00:00
df['ts'].dt.floor('h')              # floor to the hour
df['ts'].dt.ceil('15min')           # ceil to the next 15-minute mark
df['ts'].dt.round('D')              # round to nearest day
```

| Method | Direction |
|---|---|
| `floor` | Down to boundary |
| `ceil` | Up to boundary |
| `round` | Nearest boundary (half to even) |

## 15.4 Conversion

```python
df['ts'].dt.to_period('M')          # PeriodIndex with monthly freq
df['ts'].dt.to_pydatetime()         # ndarray of Python datetime objects
df['ts'].dt.to_julian_date()
df['ts'].dt.tz_localize('UTC')      # naive → UTC-aware
df['ts'].dt.tz_convert('US/Eastern')

td = pd.to_timedelta(df['duration_str'])
td.dt.total_seconds()
td.dt.components                     # DataFrame of days/hours/minutes/...
```

## 15.5 Strftime Formatting

```python
df['ts'].dt.strftime('%Y-%m-%d')             # -> string Series
df['ts'].dt.strftime('%a, %b %d %H:%M')       # -> 'Mon, Jan 15 10:30'
```

For high-throughput formatting, prefer Arrow-backed strings:

```python
df['ts_str'] = df['ts'].dt.strftime('%Y-%m-%d').astype('string')
```

---

# 16. Categorical Deep Dive

---

## 16.1 What and Why

A **Categorical** is an integer-coded, dictionary-encoded array: a small set of unique values (the *categories*) plus an integer code per element pointing into that set. It saves memory and accelerates many operations on low-cardinality columns.

```
Original (object dtype):   ['low', 'low', 'high', 'mid', 'high', 'low', ...]
                              (1M strings stored as Python objects)

Categorical:
    categories: ['low', 'mid', 'high']
    codes:      [ 0,     0,     2,    1,    2,    0,   ... ]   (int8)
```

| Aspect | object | category |
|---|---|---|
| Memory (1M rows, 10 unique values) | ~60 MB | ~1 MB |
| GroupBy speed | Slower | Faster (works on int codes) |
| Sort speed | Slower | Faster |
| Custom ordering | Lexicographic only | Arbitrary (when `ordered=True`) |
| Adding a new value | Free | Must call `add_categories` |

## 16.2 Creating Categoricals

```python
s = pd.Series(['low', 'high', 'mid', 'low'], dtype='category')

s = pd.Series(pd.Categorical(['low', 'high', 'mid', 'low'],
                              categories=['low', 'mid', 'high'],
                              ordered=True))

# CategoricalDtype is reusable
ratings = pd.CategoricalDtype(categories=['F','D','C','B','A'], ordered=True)
df['grade'] = df['grade'].astype(ratings)
```

## 16.3 The .cat Accessor

| Method | Effect |
|---|---|
| `s.cat.categories` | Index of categories |
| `s.cat.codes` | Integer codes (-1 for NA) |
| `s.cat.ordered` | Boolean |
| `s.cat.set_categories(new)` | Replace category list (drops codes outside) |
| `s.cat.add_categories(new)` | Add categories (codes unchanged) |
| `s.cat.remove_categories(old)` | Remove categories (those become NaN) |
| `s.cat.remove_unused_categories()` | Drop categories with no rows |
| `s.cat.rename_categories(new)` | Relabel categories |
| `s.cat.reorder_categories(new, ordered=True)` | Reorder (and optionally make ordered) |
| `s.cat.as_ordered()` / `as_unordered()` | Toggle ordering |

```python
df['grade'].cat.categories        # Index(['F','D','C','B','A'], dtype='object')
df['grade'].cat.codes             # [0, 1, 2, 3, 4]
df['grade'].cat.add_categories(['A+'])
df['grade'].cat.rename_categories({'A': 'A-grade'})
```

## 16.4 Ordered Categoricals and Comparisons

```python
ratings = pd.CategoricalDtype(categories=['F','D','C','B','A'], ordered=True)
df['grade'] = df['grade'].astype(ratings)

df[df['grade'] >= 'C']            # comparison uses category order
df.sort_values('grade')           # sorts F → A
df['grade'].min(), df['grade'].max()
```

## 16.5 Pitfalls

```python
# 1. Setting a value not in categories raises (or warns then becomes NaN)
df.loc[0, 'grade'] = 'Z'                  # ValueError

# 2. Concatenating categoricals with different categories upcasts to object
pd.concat([s1, s2])
# Use union_categoricals to keep them categorical:
from pandas.api.types import union_categoricals
union_categoricals([s1.values, s2.values])

# 3. Categorical groupby includes empty categories by default
df.groupby('grade', observed=False).size()   # one row per category, even empty
df.groupby('grade', observed=True).size()    # only categories actually present (Pandas 2.x default)

# 4. value_counts on categorical respects category order
df['grade'].value_counts(sort=False)         # ordered by category, not frequency
```

---

# 17. Transformation Toolkit

---

## 17.1 The Big Picture

Pandas provides a family of element-wise / row-wise / group-wise transformation methods. The right choice depends on what you have and what you want.

| Method | Operates On | Input | Returns |
|---|---|---|---|
| `Series.map(func_or_dict)` | Each element | Function or dict/Series | Series of same length |
| `Series.apply(func)` | Each element | Function | Series (or DataFrame if function returns Series) |
| `DataFrame.apply(func, axis=)` | Each row or column | Function (gets a Series) | Series or DataFrame |
| `DataFrame.map(func)` | Each cell | Function | DataFrame (replaces deprecated `applymap`) |
| `DataFrame.transform(func)` | Each column | Function | DataFrame of same shape |
| `DataFrame.pipe(func)` | Whole frame | Function | Whatever `func` returns |
| `DataFrame.assign(**kwargs)` | Adds new columns | Scalars / callables | New DataFrame |

## 17.2 Series.map

```python
s = pd.Series(['alice', 'bob', 'carol'])

s.map(str.upper)                                  # function
s.map({'alice': 'A', 'bob': 'B'})                 # dict (missing → NaN)
s.map(lookup_series)                               # Series alignment
s.map(lambda x: x[0].upper() + x[1:], na_action='ignore')   # skip NaNs
```

## 17.3 Series.apply vs Series.map

`apply` is slightly more general: it can return non-scalars (lists, Series) per element, in which case the result expands to a DataFrame. `map` is faster for the common case.

```python
s = pd.Series(['Alice 25', 'Bob 30'])

s.apply(lambda x: pd.Series(x.split(), index=['name', 'age']))
#     name age
# 0  Alice  25
# 1    Bob  30
```

## 17.4 DataFrame.apply

The `axis` parameter specifies what slice the function receives:

```python
df.apply(np.sum)                  # axis=0 (default): function gets each column
df.apply(np.sum, axis=1)          # function gets each row

df.apply(lambda row: row['a'] + row['b'], axis=1)   # row-wise lambda

# Returning a Series broadcasts to a DataFrame
df.apply(lambda row: pd.Series({'min': row.min(), 'max': row.max()}), axis=1)
```

`apply` over rows is **slow** -- it is a Python-level loop. Whenever possible, use vectorized arithmetic (`df['a'] + df['b']`) instead.

## 17.5 DataFrame.map (formerly applymap)

```python
df.map(lambda x: f'{x:.2f}' if isinstance(x, float) else x)
df.select_dtypes('number').map(lambda x: x ** 2)
```

`DataFrame.applymap` was deprecated in 2.1 in favor of `DataFrame.map`.

## 17.6 transform

`transform` returns the **same shape** as the input -- crucial for vectorized "broadcast a per-group statistic back to rows" patterns.

```python
df['z']      = df.groupby('dept')['salary'].transform('mean')
df['zscore'] = df.groupby('dept')['salary'].transform(lambda s: (s - s.mean()) / s.std())
df[['a','b']] = df[['a','b']].transform(lambda c: c - c.mean())
```

## 17.7 pipe and assign for Chaining

`pipe` and `assign` make method chains readable end-to-end:

```python
result = (
    raw_df
    .pipe(load_extras, source='s3://bucket/extras.parquet')
    .assign(
        salary_k = lambda d: d['salary'] / 1000,
        is_senior = lambda d: d['age'] >= 30,
    )
    .query('salary_k > 30 and is_senior')
    .groupby('dept')
    .agg(avg_salary_k=('salary_k', 'mean'))
    .sort_values('avg_salary_k', ascending=False)
)
```

`pipe(func, *args, **kwargs)` is equivalent to `func(df, *args, **kwargs)` but reads left-to-right inside a chain.

## 17.8 cut and qcut -- Binning

| Function | Bin Boundaries | Returns |
|---|---|---|
| `pd.cut(s, bins)` | Explicit edges or count | Categorical of `Interval` |
| `pd.qcut(s, q)` | Quantile-based | Categorical of `Interval` |

```python
ages = pd.Series([5, 12, 17, 25, 40, 65, 80])

pd.cut(ages, bins=[0, 12, 18, 65, 120],
       labels=['child', 'teen', 'adult', 'senior'],
       include_lowest=True)
# 0     child
# 1     child
# 2      teen
# 3     adult
# 4     adult
# 5     adult
# 6    senior

pd.cut(ages, bins=4)             # 4 equal-width bins
pd.qcut(ages, q=4)               # 4 equal-frequency bins (quartiles)
pd.qcut(ages, q=[0, .25, .5, .75, 1.0], labels=['Q1','Q2','Q3','Q4'])
```

`pd.cut` with `retbins=True` also returns the chosen edges -- useful for replicating bins on test data.

## 17.9 Sampling

```python
df.sample(n=100, random_state=42)               # exactly 100 rows
df.sample(frac=0.1, random_state=42)             # 10% of rows
df.sample(n=10, weights='salary')                # weighted (column or array)
df.sample(n=5, replace=True)                     # bootstrap
df.sample(n=10, axis=1)                          # sample columns
```

`groupby(...).sample(n=)` performs stratified sampling -- N rows per group.

## 17.10 replace

`replace` is the swiss-army value substitution method:

```python
df.replace({'Y': True, 'N': False})                       # global
df.replace({'status': {'Y': True, 'N': False}})           # column-specific
df.replace(np.nan, 0)
df.replace(to_replace=r'^old_(.*)', value=r'new_\1', regex=True)
df.replace([1, 2, 3], 0)                                  # all of these → 0
df['email'].replace('', np.nan)                            # blank strings → NaN
```

## 17.11 explode

`explode` turns a column of lists into multiple rows -- one per element:

```python
df = pd.DataFrame({
    'id':   [1, 2, 3],
    'tags': [['py', 'pandas'], ['sql'], []],
})

df.explode('tags', ignore_index=False)
#    id    tags
# 0   1      py
# 0   1  pandas
# 1   2     sql
# 2   3     NaN

df.explode(['tags', 'scores'])    # multiple columns explode in lockstep
```

## 17.12 get_dummies and from_dummies

`get_dummies` is one-hot encoding; `from_dummies` is the inverse.

```python
pd.get_dummies(df['color'], prefix='c', dtype='int8')
#    c_blue  c_green  c_red
# 0       0        0      1
# 1       1        0      0
# 2       0        1      0

pd.get_dummies(df, columns=['color'], drop_first=True)    # drop one to avoid collinearity

dummies = pd.DataFrame({'c_red': [1,0,0], 'c_blue': [0,1,0], 'c_green': [0,0,1]})
pd.from_dummies(dummies, sep='_')                         # → DataFrame with single 'c' column
```

## 17.13 clip and abs

```python
df['x'].clip(lower=0)                    # negatives → 0
df['x'].clip(lower=0, upper=100)         # constrain to [0, 100]
df['x'].clip(lower=df['lo'], upper=df['hi'])   # vectorized bounds

df['x'].abs()                            # absolute value
```

---

# Part 5: Aggregation and Reshaping

---

# 18. GroupBy: Split-Apply-Combine

---

## 18.1 The Pattern

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
               ▼            ▼            ▼        ← APPLY (agg / transform / filter)
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
    'dept':   ['Sales', 'Sales', 'Eng', 'Eng', 'Eng', 'Ops'],
    'level':  ['Jr',    'Sr',    'Jr',  'Sr',  'Sr',  'Jr'],
    'name':   ['Alice', 'Bob',   'Carol','Dave','Eve', 'Faye'],
    'salary': [50, 60, 70, 80, 90, 55],
})

g = df.groupby('dept')
g['salary'].mean()
g[['salary']].mean()                # DataFrame result
g.size()                             # rows per group
g.ngroups                            # number of groups
g.groups                             # dict: group key → row labels
```

## 18.2 Group Keys

A `groupby` key can be any of the following (or a list mixing them):

| Key Form | Example | Notes |
|---|---|---|
| Column name | `df.groupby('dept')` | Most common |
| Multiple columns | `df.groupby(['dept', 'level'])` | Hierarchical groups |
| Series | `df.groupby(df['dept'].str.lower())` | Computed key |
| Function on index | `df.groupby(lambda label: label % 2)` | Function gets each index label |
| Index level (MultiIndex) | `df.groupby(level='city')` | By name or integer |
| `pd.Grouper(...)` | `df.groupby(pd.Grouper(key='ts', freq='D'))` | Time-based or labeled |

```python
df.groupby(['dept', 'level']).size()
df.groupby(pd.cut(df['salary'], bins=[0, 60, 80, 100])).size()
```

## 18.3 Important Parameters

| Parameter | Default | Effect |
|---|---|---|
| `dropna` | True | Whether NA group keys are excluded |
| `sort` | True | Whether output is sorted by group key (False = preserve order, faster) |
| `as_index` | True | Whether group keys become the index (False = stay as columns) |
| `observed` | True (Pandas 2.x) | For categorical keys: include only categories present in data |
| `group_keys` | True | Whether `apply` includes group keys in the result |

```python
df.groupby('dept', sort=False).mean()         # avoid sort overhead on huge frames
df.groupby('dept', as_index=False).agg({'salary': 'mean'})    # 'dept' stays a column
df.groupby('cat_col', observed=False).size()  # include empty categories
df.groupby('dept', dropna=False).size()       # NA keys get their own group
```

## 18.4 Iterating Over Groups

```python
for name, sub_df in df.groupby('dept'):
    print(f'--- {name} ({len(sub_df)} rows) ---')
    print(sub_df)

g.get_group('Eng')                # one specific group
```

Iteration is convenient but slow for huge group counts -- prefer `agg`/`apply` whenever you can.

## 18.5 Built-in Aggregations on a GroupBy

| Method | Description |
|---|---|
| `count`, `size` | Non-NA count vs row count |
| `sum`, `prod` | Reductions |
| `mean`, `median`, `std`, `var`, `sem` | Standard stats |
| `min`, `max`, `first`, `last`, `nth(n)` | Order-aware |
| `idxmin`, `idxmax` | Index label of min/max |
| `quantile(q)` | Percentile |
| `nunique`, `value_counts` | Distinct counts / frequencies |
| `cumsum`, `cumprod`, `cummin`, `cummax`, `cumcount` | Cumulative within group |
| `head(n)`, `tail(n)` | First/last n per group |
| `rank(method=)` | Rank within group |
| `diff(n)`, `pct_change(n)`, `shift(n)` | Lag/diff per group |

```python
g['salary'].agg(['mean', 'min', 'max', 'count'])
g.head(2)                          # first 2 rows per group (order in original DF)
g.cumcount()                       # 0, 1, 2, ... within each group
df['rank_in_dept'] = g['salary'].rank(method='dense', ascending=False)
```

---

# 19. agg vs transform vs filter vs apply

---

## 19.1 The Comparison

| Method | Output Shape | Function Receives | Function Returns | Use Case |
|---|---|---|---|---|
| `agg(func)` | One row per group | Series (one column at a time) | Scalar | Summary statistics |
| `transform(func)` | Same shape as input | Series (per group, per column) | Series of same length | Broadcast group stats back to rows |
| `filter(func)` | Subset of input rows | Sub-DataFrame (per group) | Boolean | Keep/remove entire groups |
| `apply(func)` | Flexible (depends on return) | Sub-DataFrame (per group) | Anything | Anything else |

## 19.2 agg

```python
g.agg({'salary': 'mean', 'name': 'count'})
g.agg(['mean', 'min', 'max'])                   # broadcast across all numeric cols

g.agg({'salary': ['mean', 'std'], 'level': 'nunique'})

# Custom aggregations
g['salary'].agg(lambda s: s.max() - s.min())
g['salary'].agg(spread=lambda s: s.max() - s.min(),
                p90=lambda s: s.quantile(.9))

# Named aggregations (recommended -- flat output, explicit names)
g.agg(
    avg_salary=('salary', 'mean'),
    max_salary=('salary', 'max'),
    headcount =('name', 'count'),
    seniors   =('level', lambda s: (s == 'Sr').sum()),
)
```

## 19.3 transform

`transform` is for "compute a per-group statistic, then broadcast it back row-by-row".

```python
df['dept_mean']    = g['salary'].transform('mean')
df['dept_zscore']  = g['salary'].transform(lambda s: (s - s.mean()) / s.std())
df['rank_in_dept'] = g['salary'].transform('rank', ascending=False)

# Transform with multiple functions returns a DataFrame
g['salary'].transform(['mean', 'std'])
```

`transform` requires that the function returns either a scalar (broadcast to the group) or a Series of the same length as the group.

## 19.4 filter

```python
big_depts = g.filter(lambda sub: len(sub) >= 3)            # keep depts with >=3 rows
high_avg  = g.filter(lambda sub: sub['salary'].mean() > 60)
```

`filter` returns the original rows from the surviving groups -- **not** the function's return value. The function must return a boolean.

## 19.5 apply -- The Escape Hatch

`apply` is the most flexible and the slowest. Reach for it only when `agg` / `transform` / `filter` cannot express what you want.

```python
g.apply(lambda sub: sub.nlargest(2, 'salary'))           # top-2 rows per group

g.apply(lambda sub: pd.Series({
    'salary_range': sub['salary'].max() - sub['salary'].min(),
    'top_earner':   sub.loc[sub['salary'].idxmax(), 'name'],
}))
```

| Pitfall | Mitigation |
|---|---|
| `apply` may execute the first group twice (it inspects the result shape) | Make the function side-effect-free |
| Slower than `agg`/`transform` (Python-level loop) | Use them when applicable |
| `group_keys` parameter affects the output index | Pass `group_keys=False` to drop them |

## 19.6 numeric_only Default

In Pandas 2.x, most aggregation methods default to `numeric_only=False` and will **raise** if non-numeric columns are present. Pass `numeric_only=True` to silently skip them, or select numeric columns first:

```python
g.mean(numeric_only=True)
df.select_dtypes('number').groupby(df['dept']).mean()
```

---

# 20. Named Aggregations, crosstab, pivot_table

---

## 20.1 Named Aggregations

The keyword form of `agg` produces a flat output with explicit column names -- preferred over the older list/dict forms:

```python
g.agg(
    avg_salary = ('salary', 'mean'),
    headcount  = ('name', 'count'),
    seniors    = ('level', lambda s: (s == 'Sr').sum()),
)
#         avg_salary  headcount  seniors
# dept
# Eng           80.0          3        2
# Ops           55.0          1        0
# Sales         55.0          2        1
```

Each value is a `pd.NamedAgg(column, aggfunc)` tuple (the tuple syntax is shorthand).

## 20.2 pivot_table

`pivot_table` is `groupby + reshape + aggregation` in one call. It's the right tool for "cross-tabulation with statistics".

```python
sales = pd.DataFrame({
    'date':    pd.date_range('2024-01-01', periods=8, freq='D'),
    'region':  ['NA', 'EU', 'NA', 'EU', 'NA', 'EU', 'NA', 'EU'],
    'product': ['A',  'A',  'B',  'B',  'A',  'A',  'B',  'B'],
    'units':   [10, 12, 8, 9, 11, 13, 7, 10],
    'revenue': [100, 130, 90, 95, 105, 140, 78, 110],
})

pd.pivot_table(sales,
    values='revenue', index='region', columns='product',
    aggfunc='sum',
    fill_value=0,
    margins=True,             # adds a 'All' row and column with totals
    margins_name='Total',
    observed=True,            # for categorical keys (Pandas 2.x default)
)
```

| Parameter | Effect |
|---|---|
| `index` | Row grouping(s) (string or list) |
| `columns` | Column grouping(s) |
| `values` | Column(s) to aggregate (omit to aggregate all numeric) |
| `aggfunc` | Function or dict per `values` (default `'mean'`) |
| `fill_value` | Replace NA in the result |
| `margins` | Add subtotals/total |
| `dropna` | Whether all-NA columns/rows are dropped |
| `observed` | Categorical: only include observed combinations |

Multiple aggregations:

```python
pd.pivot_table(sales,
    values='revenue', index='region', columns='product',
    aggfunc=['sum', 'mean', 'count'])
```

## 20.3 crosstab

`crosstab` is a thin wrapper that's more convenient for **simple frequency tables** (and accepts arrays directly, not only DataFrame columns):

```python
pd.crosstab(sales['region'], sales['product'])
# product  A  B
# region
# EU       2  2
# NA       2  2

pd.crosstab(sales['region'], sales['product'],
            values=sales['revenue'], aggfunc='sum')

pd.crosstab(sales['region'], sales['product'],
            normalize='index')     # row proportions

pd.crosstab(sales['region'], sales['product'], margins=True)
```

| `normalize` | Effect |
|---|---|
| `True` / `'all'` | Divide every cell by the grand total |
| `'index'` | Each row sums to 1 |
| `'columns'` | Each column sums to 1 |
| `False` (default) | Raw counts |

## 20.4 pivot vs pivot_table

| Aspect | `pivot` | `pivot_table` |
|---|---|---|
| Aggregation | None (one value per cell required) | Any aggfunc |
| Duplicates in (index, columns) | Raises `ValueError` | Aggregated |
| Multi-aggregation | No | Yes (list of aggfuncs) |
| Margins | No | Yes |

Use `pivot` when the source data is already unique on the (row, column) grid; use `pivot_table` when there may be duplicates or you need aggregation.

---

# 21. Window Functions

---

## 21.1 The Three Window Types

| Window | Method | Description |
|---|---|---|
| **Rolling** | `s.rolling(window=)` | Fixed-size sliding window over the last `window` rows |
| **Expanding** | `s.expanding()` | Growing window from start to current row |
| **Exponentially weighted** | `s.ewm(span=, alpha=, halflife=)` | Recent values weighted more |

```python
s = pd.Series([10, 12, 11, 13, 17, 16, 19, 21, 20])

s.rolling(3).mean()                   # 3-row trailing mean
s.expanding(min_periods=1).mean()     # cumulative mean
s.ewm(span=3, adjust=False).mean()    # EW mean
```

## 21.2 Rolling Windows

```python
s.rolling(window=5).mean()                       # trailing 5
s.rolling(window=5, min_periods=1).mean()        # accept partial windows
s.rolling(window=5, center=True).mean()          # centered (NaN at edges)
s.rolling(window='30D').mean()                   # time-based (requires DatetimeIndex)
s.rolling(window=5, win_type='triang').mean()    # triangular weights

s.rolling(5).agg(['mean', 'std', 'min', 'max'])

s.rolling(5).apply(lambda w: w.max() - w.min(), raw=True)   # raw=True passes ndarray, faster
s.rolling(5).apply(custom_func, engine='numba')              # JIT compile (Pandas 1.3+)
```

| Parameter | Effect |
|---|---|
| `window` | Int (rows) or offset string (`'30D'`, `'1h'`) |
| `min_periods` | Minimum rows required to emit a value |
| `center` | Place label at window center vs right edge |
| `win_type` | Apply weighting (e.g. `'triang'`, `'gaussian'`) |
| `closed` | `'right'` / `'left'` / `'both'` / `'neither'` for time windows |
| `step` | Stride between windows (Pandas 1.5+) |

## 21.3 Expanding Windows

```python
s.expanding().mean()             # cumulative average
s.expanding().sum()              # equivalent to cumsum
s.expanding().std()
s.expanding(min_periods=3).mean()  # don't emit until 3 observations
```

Useful for "growing baseline" features in time-series forecasting.

## 21.4 Exponentially Weighted (EWM)

EWM applies decaying weights so that older observations matter less.

| Parameter | Definition |
|---|---|
| `span` | EW span (analogous to N for SMA): `alpha = 2/(span+1)` |
| `halflife` | Time after which weight halves |
| `alpha` | Smoothing factor in (0, 1] -- direct |
| `com` | Center of mass: `alpha = 1/(com+1)` |
| `adjust` | Whether to normalize early values (True is the default; False = recursive form) |
| `ignore_na` | Skip missing values in the calculation |

```python
s.ewm(span=10).mean()                   # smooth trend
s.ewm(alpha=0.3, adjust=False).mean()
s.ewm(halflife='7D', times=df['ts']).mean()   # time-aware EWM
```

## 21.5 Group-Wise Windows

`rolling`, `expanding`, and `ewm` all play with `groupby`:

```python
df['ma_3'] = (
    df.sort_values('ts')
      .groupby('symbol')['price']
      .rolling(3).mean()
      .reset_index(level=0, drop=True)
)

# More concise via groupby.rolling (Pandas 1.0+):
df['ma_3'] = df.groupby('symbol')['price'].transform(lambda s: s.rolling(3).mean())
```

## 21.6 Numba Engine

For custom window functions on large data, the `numba` engine compiles the function to machine code:

```python
def custom(arr):
    return arr[-1] - arr[0]

s.rolling(100).apply(custom, raw=True, engine='numba')
```

The first call pays a JIT compilation cost (~1 s); subsequent calls are very fast. Numba helps most for large windows or millions of rows.

---

# 22. Reshaping: pivot, melt, stack, unstack

---

## 22.1 The Map

| Function | Direction | Aggregation? | Operates On |
|---|---|---|---|
| `pivot` | Long → Wide | No (errors on dupes) | Columns of a DataFrame |
| `pivot_table` | Long → Wide | Yes | Columns of a DataFrame |
| `melt` | Wide → Long | No | Columns → rows |
| `wide_to_long` | Wide → Long | No | Stub-named columns |
| `stack` | Wide → Long | No | Columns → inner index level |
| `unstack` | Long → Wide | No | Index level → columns |
| `transpose` (`.T`) | Swap axes | No | Whole DataFrame |

```
long format                                  wide format
                          ──────►   pivot
                          ◄──────   melt

date     product  sales        date         A    B
2024-01    A      100          2024-01    100  200
2024-01    B      200    ↔     2024-02    150  250
2024-02    A      150
2024-02    B      250
```

## 22.2 pivot

```python
long = pd.DataFrame({
    'date':    ['2024-01', '2024-01', '2024-02', '2024-02'],
    'product': ['A', 'B', 'A', 'B'],
    'sales':   [100, 200, 150, 250],
})

long.pivot(index='date', columns='product', values='sales')
# product       A    B
# date
# 2024-01     100  200
# 2024-02     150  250
```

If `(index, columns)` pairs are not unique, `pivot` raises -- use `pivot_table` instead.

## 22.3 melt

```python
wide = long.pivot(index='date', columns='product', values='sales').reset_index()

wide.melt(id_vars='date', var_name='product', value_name='sales')
#       date product  sales
# 0  2024-01       A    100
# 1  2024-02       A    150
# 2  2024-01       B    200
# 3  2024-02       B    250

wide.melt(id_vars='date', value_vars=['A'], var_name='product')
```

`melt` is the canonical "tidy data" transformation: every row becomes one observation.

## 22.4 wide_to_long

`pd.wide_to_long` handles the common pattern where wide column names share a stub:

```python
df = pd.DataFrame({
    'id':      [1, 2],
    'A_2023':  [100, 150],
    'A_2024':  [110, 160],
    'B_2023':  [200, 250],
    'B_2024':  [210, 260],
})

pd.wide_to_long(df, stubnames=['A', 'B'], i='id', j='year', sep='_').reset_index()
#    id  year    A    B
# 0   1  2023  100  200
# 1   1  2024  110  210
# 2   2  2023  150  250
# 3   2  2024  160  260
```

## 22.5 stack and unstack

`stack` pivots **column labels** down into the row index (making the frame longer); `unstack` is the inverse.

```python
df = wide.set_index('date')
#  product       A    B
#  date
#  2024-01     100  200
#  2024-02     150  250

stacked = df.stack()       # turns 'product' into an inner index level
# date     product
# 2024-01  A          100
#          B          200
# 2024-02  A          150
#          B          250
# dtype: int64

stacked.unstack()           # back to wide
stacked.unstack(level=0)    # 'date' becomes the columns instead

# stack with future_stack (Pandas 2.1+) gives the new behavior in advance:
df.stack(future_stack=True)
```

| `level` | Effect |
|---|---|
| Default (`-1`) | Innermost level moves |
| Integer `i` | Level at position `i` moves |
| String name | The named level moves |
| List | Multiple levels move at once |

## 22.6 Practical Recipes

```python
# 1. Long-form time series → wide for plotting
ts_wide = ts_long.pivot(index='ts', columns='symbol', values='price')

# 2. Wide observation → tidy for ML
tidy = obs_wide.melt(id_vars=['user_id'], var_name='feature', value_name='value')

# 3. MultiIndex columns → flat columns
df.columns = ['_'.join(map(str, c)).strip('_') for c in df.columns]

# 4. Cross-tab → tidy
ct = pd.crosstab(df['region'], df['product'])
ct.stack().rename('count').reset_index()
```

---

# Part 6: Combining DataFrames

---

# 23. concat

---

## 23.1 What concat Does

`pd.concat` glues DataFrames or Series together along an axis. There is no key-matching -- it is straight stacking, with optional alignment on the *other* axis.

```python
df1 = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
df2 = pd.DataFrame({'a': [5, 6], 'b': [7, 8]})

pd.concat([df1, df2])                          # vertical stack (default axis=0)
pd.concat([df1, df2], ignore_index=True)       # reset index to 0..n-1
pd.concat([df1, df2], axis=1)                  # horizontal stack
pd.concat([df1, df2], keys=['first', 'second'])  # outer index level
```

## 23.2 Parameters Cheat-Sheet

| Parameter | Effect |
|---|---|
| `axis` | 0 = stack rows (default), 1 = stack columns |
| `join` | `'outer'` (default, union of other axis) or `'inner'` (intersection) |
| `ignore_index` | Reset to a fresh `RangeIndex` |
| `keys` | Add an outer level to the index (`MultiIndex`) |
| `levels`, `names` | Customize the new level |
| `sort` | Sort the non-concat axis (default False; was True pre-2.0) |
| `verify_integrity` | Raise if the concatenated index has duplicates |

## 23.3 outer vs inner Join

```python
df1 = pd.DataFrame({'a': [1, 2]}, index=['x', 'y'])
df2 = pd.DataFrame({'b': [3, 4]}, index=['x', 'z'])

pd.concat([df1, df2], axis=1, join='outer')
#      a    b
# x  1.0  3.0
# y  2.0  NaN
# z  NaN  4.0

pd.concat([df1, df2], axis=1, join='inner')
#    a  b
# x  1  3
```

## 23.4 Hierarchical Indexing with keys

```python
result = pd.concat([df1, df2], keys=['Q1', 'Q2'], names=['quarter'])
#               a  b
# quarter
# Q1      0    1  3
#         1    2  4
# Q2      0    5  7
#         1    6  8

result.loc['Q1']        # back to original df1
```

## 23.5 Avoiding the Quadratic Append

A common anti-pattern is appending to a DataFrame inside a loop:

```python
# BAD: O(n^2) -- each concat copies the entire growing frame
df = pd.DataFrame()
for record in stream:
    df = pd.concat([df, pd.DataFrame([record])])

# GOOD: build a list, concat once
rows = []
for record in stream:
    rows.append(record)
df = pd.DataFrame(rows)

# OR for many small DataFrames:
parts = []
for chunk in chunks:
    parts.append(transform(chunk))
df = pd.concat(parts, ignore_index=True)
```

## 23.6 Concat with Different Columns

```python
df_a = pd.DataFrame({'x': [1], 'y': [2]})
df_b = pd.DataFrame({'y': [3], 'z': [4]})

pd.concat([df_a, df_b], ignore_index=True)
#      x  y    z
# 0  1.0  2  NaN
# 1  NaN  3  4.0
```

dtypes are upcast as needed (int → float to accommodate NaN). To avoid this, pre-align columns or use nullable dtypes.

---

# 24. merge and join

---

## 24.1 The Big Picture

`merge` is the SQL-style relational join. `join` is a thin wrapper around `merge` for the common index-on-index case.

```python
left = pd.DataFrame({'key': ['a','b','c','d'], 'val_l': [1, 2, 3, 4]})
right = pd.DataFrame({'key': ['c','d','e','f'], 'val_r': [30, 40, 50, 60]})

pd.merge(left, right, on='key', how='inner')
#   key  val_l  val_r
# 0   c      3     30
# 1   d      4     40
```

## 24.2 Join Types

| `how` | SQL Equivalent | Result |
|---|---|---|
| `'inner'` (default) | `INNER JOIN` | Only matching keys |
| `'left'` | `LEFT JOIN` | All left rows; right NaNs where no match |
| `'right'` | `RIGHT JOIN` | All right rows; left NaNs where no match |
| `'outer'` | `FULL OUTER JOIN` | All rows from either side |
| `'cross'` | `CROSS JOIN` | Cartesian product (use sparingly!) |

```
       LEFT                        OUTER                         INNER
    ┌────────┐                ┌─────────────┐                ┌────────┐
    │  Left  │                │             │                │        │
    │   ┌────┼─────┐          │  Left  ┌────┼─────┐          │  ┌─────┤
    │   │    │     │          │        │    │     │          │  │     │
    └───┼────┘     │          └────────┼────┘     │          └──┼─────┘
        │  Right   │                   │  Right   │             │
        └──────────┘                   └──────────┘             │
                                                                Right
                                                                (intersection)
```

## 24.3 Key Specification

| Form | Example |
|---|---|
| Single shared column | `pd.merge(left, right, on='key')` |
| Multiple shared columns | `pd.merge(left, right, on=['k1', 'k2'])` |
| Different column names | `pd.merge(left, right, left_on='lkey', right_on='rkey')` |
| Index on both sides | `pd.merge(left, right, left_index=True, right_index=True)` |
| Mix index + column | `pd.merge(left, right, left_on='key', right_index=True)` |

## 24.4 Useful Parameters

| Parameter | Effect |
|---|---|
| `suffixes` | Resolve overlapping non-key column names (default `('_x', '_y')`) |
| `indicator` | Add a `_merge` column (`'left_only'` / `'right_only'` / `'both'`) |
| `validate` | Assert the cardinality: `'1:1'`, `'1:m'`, `'m:1'`, `'m:m'` |
| `sort` | Lexsort the result on the join keys |
| `copy` | Avoid copying data (CoW makes this less important) |

```python
pd.merge(left, right, on='key', how='outer', indicator=True)
#   key  val_l  val_r      _merge
# 0   a    1.0    NaN   left_only
# 1   b    2.0    NaN   left_only
# 2   c    3.0   30.0        both
# 3   d    4.0   40.0        both
# 4   e    NaN   50.0  right_only
# 5   f    NaN   60.0  right_only

pd.merge(orders, customers, on='customer_id', validate='m:1')   # raises if not many-to-one
```

## 24.5 Suffixes for Overlapping Columns

```python
left  = pd.DataFrame({'k': [1, 2], 'val': [10, 20]})
right = pd.DataFrame({'k': [1, 2], 'val': [100, 200]})

pd.merge(left, right, on='k', suffixes=('_left', '_right'))
#    k  val_left  val_right
# 0  1        10        100
# 1  2        20        200
```

If you set `suffixes=(False, '_right')`, the left side keeps its original name and the right is renamed. Setting both to `False` raises if there are duplicates.

## 24.6 join

`DataFrame.join` joins on the index of the right frame by default and on the index (or specified column) of the left:

```python
left.set_index('k').join(right.set_index('k'), lsuffix='_l', rsuffix='_r')
# == merge(left, right, left_index=True, right_index=True, how='left')

left.join(right.set_index('k'), on='k')   # left's 'k' joins right's index
```

`join` accepts a list of frames for multi-way joins on the index:

```python
df.join([df_a, df_b, df_c], how='outer')   # joins them all on the index
```

## 24.7 Common Pitfalls

```python
# 1. Dtype mismatch silently produces no matches
left  = pd.DataFrame({'id': [1, 2, 3]})           # int64
right = pd.DataFrame({'id': ['1', '2', '3'],
                       'name': ['a', 'b', 'c']})    # object
pd.merge(left, right, on='id')                     # empty result!
left['id'] = left['id'].astype(str)                # fix
pd.merge(left, right, on='id')

# 2. Many-to-many silently explodes the result
left  = pd.DataFrame({'k': [1, 1], 'v': ['a','b']})
right = pd.DataFrame({'k': [1, 1], 'v': ['x','y']})
pd.merge(left, right, on='k')                      # 4 rows!

# 3. NaN keys do NOT match each other
pd.merge(left.assign(k=np.nan), right, on='k')     # 0 rows

# 4. Reordering keys silently OK -- order doesn't matter
pd.merge(left, right, on=['k1', 'k2'])
pd.merge(left, right, on=['k2', 'k1'])             # same result, only column order differs

# 5. Always validate when you think the merge is unique
pd.merge(orders, products, on='product_id', validate='m:1')   # fails fast on dup product_ids
```

---

# 25. merge_asof, merge_ordered, compare, align

---

## 25.1 merge_asof -- "As-Of" Merge

`merge_asof` is the swiss army knife for **time-series alignment**: for each row on the left, find the **nearest** key on the right that is `<=` (or `>=`) the left key. Heavily used in finance for matching trades to quotes.

```python
trades = pd.DataFrame({
    'ts':     pd.to_datetime(['09:30:00', '09:30:23', '09:30:30', '09:31:05']),
    'price':  [101.0, 101.5, 102.0, 102.3],
    'symbol': ['X', 'X', 'Y', 'X'],
})

quotes = pd.DataFrame({
    'ts':     pd.to_datetime(['09:30:00', '09:30:01', '09:30:25', '09:30:31', '09:31:00']),
    'bid':    [100.0, 100.5, 101.4, 101.9, 102.1],
    'symbol': ['X', 'X', 'X', 'Y', 'X'],
})

trades = trades.sort_values('ts')
quotes = quotes.sort_values('ts')

pd.merge_asof(trades, quotes, on='ts', by='symbol')
#         ts  price symbol    bid
# 0 09:30:00  101.0      X  100.0
# 1 09:30:23  101.5      X  100.5
# 2 09:30:30  102.0      Y    NaN
# 3 09:31:05  102.3      X  102.1

pd.merge_asof(trades, quotes,
              on='ts', by='symbol',
              direction='nearest',          # 'backward' (default) / 'forward' / 'nearest'
              tolerance=pd.Timedelta('5s'))  # only match if within 5 seconds
```

| Parameter | Effect |
|---|---|
| `on` | The "as-of" column (must be sorted on both sides) |
| `by` | Optional grouping column(s) -- match within group |
| `direction` | `'backward'` (default), `'forward'`, `'nearest'` |
| `tolerance` | Maximum distance allowed for a match |
| `allow_exact_matches` | Whether equal keys may match (default True) |

> Critical: both inputs must be sorted on the `on` column. Use `sort_values` first or `merge_asof` will raise.

## 25.2 merge_ordered

Like `merge`, but designed for **ordered** data (typically time series): supports forward-fill of missing values and preserves order. Useful when you want a left-merge behaviour with built-in `ffill`.

```python
left  = pd.DataFrame({'ts': [1, 2, 4],   'lv': [10, 20, 30]})
right = pd.DataFrame({'ts': [1, 3, 4, 5], 'rv': [100, 300, 400, 500]})

pd.merge_ordered(left, right, on='ts', fill_method='ffill')
#    ts    lv     rv
# 0   1  10.0  100.0
# 1   2  20.0  100.0      ← ffill from ts=1
# 2   3   NaN  300.0
# 3   4  30.0  400.0
# 4   5   NaN  500.0
```

## 25.3 compare

`compare` highlights differences between two DataFrames of identical shape -- useful for unit tests, pre/post-transformation diffs, and CDC pipelines.

```python
df1 = pd.DataFrame({'a': [1,2,3], 'b': ['x','y','z']})
df2 = pd.DataFrame({'a': [1,9,3], 'b': ['x','y','Z']})

df1.compare(df2)
#      a            b
#   self other  self other
# 1  2.0   9.0   NaN   NaN
# 2  NaN   NaN     z     Z

df1.compare(df2, align_axis=0)        # stack rather than side-by-side
df1.compare(df2, keep_shape=True)     # preserve original shape (NaN where equal)
df1.compare(df2, keep_equal=True)
df1.compare(df2, result_names=('before', 'after'))
```

## 25.4 align

`align` returns two frames padded so they share the same index/columns:

```python
a, b = df1.align(df2, join='outer', axis=None)
# Both a and b now have the union of indexes and columns
```

Used internally by every binary operation. Most user code only needs `align` when computing multiple expressions on differently-indexed inputs and wanting them on a common axis.

## 25.5 combine_first

`combine_first` is "use other's value where mine is NA". Common pattern for layering data sources by priority.

```python
primary = pd.DataFrame({'a': [1, np.nan, 3], 'b': [10, 20, np.nan]})
backup  = pd.DataFrame({'a': [9, 8, 7],     'b': [100, 200, 300]})

primary.combine_first(backup)
#      a      b
# 0  1.0   10.0
# 1  8.0   20.0     ← a came from backup
# 2  3.0  300.0     ← b came from backup
```

## 25.6 update

`df.update(other)` modifies `df` in place using non-NA values from `other`, **without** changing the index/columns of `df`:

```python
df = pd.DataFrame({'a': [1, 2, 3], 'b': [10, 20, 30]})
patch = pd.DataFrame({'a': [None, 99, None]}, index=[0, 1, 2])

df.update(patch)
#    a    b
# 0  1   10
# 1 99   20
# 2  3   30
```

| Method | Behaviour |
|---|---|
| `combine_first` | Returns new frame; fill *self*'s NAs from *other* |
| `update` | In-place; overwrite *self* with *other*'s non-NAs |
| `merge` | New frame; key-based join, may add columns |
| `concat` | New frame; stacking, may add rows |

---

# Part 7: Time Series

---

# 26. Timestamps, Periods, Timedeltas

---

## 26.1 The Time-Aware Type Family

| Type | Represents | Backed By | Example |
|---|---|---|---|
| `Timestamp` | A single point in time | `np.datetime64[ns]` | `2024-06-15 12:30:00` |
| `DatetimeIndex` | An array of timestamps | NumPy or PyArrow | hourly axis for a year |
| `Period` | A span of time at a fixed frequency | int + freq | "the month of 2024-06" |
| `PeriodIndex` | Array of periods | int array + freq | monthly index |
| `Timedelta` | A duration | `np.timedelta64[ns]` | `5 days 3:00:00` |
| `TimedeltaIndex` | Array of durations | NumPy | array of latencies |
| `DateOffset` | A calendar-aware offset | Object | `MonthEnd()`, `BusinessDay()` |

## 26.2 Timestamp

```python
ts = pd.Timestamp('2024-06-15 12:30:45')
ts = pd.Timestamp(year=2024, month=6, day=15, hour=12)
ts = pd.Timestamp.now()
ts = pd.Timestamp.utcnow()
ts = pd.Timestamp('2024-06-15', tz='US/Pacific')

# Conversion
ts = pd.to_datetime('2024-06-15 12:30')
ts = pd.to_datetime(1_700_000_000, unit='s')      # Unix epoch
ts = pd.to_datetime(1_700_000_000_000, unit='ms')

# Components and arithmetic
ts.year, ts.month, ts.day
ts.dayofweek          # 0 = Monday
ts.day_name()         # 'Saturday'
ts.is_month_end
ts + pd.Timedelta('1 day')
ts - pd.Timestamp('2024-01-01')   # Timedelta
```

## 26.3 Timedelta

```python
td = pd.Timedelta(days=2, hours=3, minutes=30)
td = pd.Timedelta('1 day 3 hours')
td = pd.Timedelta('00:30:15.500')
td = pd.to_timedelta(df['millis'], unit='ms')

# Arithmetic
td.days, td.seconds, td.microseconds, td.nanoseconds
td.total_seconds()         # 184215.5

ts1 - ts2                   # Timedelta
ts + td                     # Timestamp
2 * td                      # Timedelta
```

## 26.4 Period

```python
p = pd.Period('2024-06', freq='M')        # June 2024 (whole month)
p = pd.Period('2024Q2', freq='Q')          # Q2 2024
p = pd.Period('2024-06-15', freq='D')      # one day

p.start_time, p.end_time                   # actual Timestamps at boundaries
p + 1                                       # July 2024
p - pd.Period('2024-01', freq='M')         # 5 (months apart)

ts.to_period('M')                           # downcast Timestamp → Period
p.to_timestamp(how='start')                 # back to Timestamp at start
p.to_timestamp(how='end')                   # at end
```

| When to use | `Timestamp` | `Period` |
|---|---|---|
| Exact instant in time | Yes | No |
| "Belongs to month X" semantics | Awkward | Natural |
| Duration arithmetic | Yes | Yes |
| Timezone awareness | Yes | No |

## 26.5 DatetimeIndex, PeriodIndex, TimedeltaIndex

```python
dti = pd.DatetimeIndex(['2024-01-01', '2024-02-01', '2024-03-01'])
pdi = pd.PeriodIndex(['2024-01', '2024-02', '2024-03'], freq='M')
tdi = pd.TimedeltaIndex(['1 day', '2 days', '3 days'])

# Accessors
dti.year, dti.month, dti.dayofweek
dti.tz                          # None for naive
dti.is_monotonic_increasing
dti.freq                         # may be None if not regular
dti.inferred_freq                # detect frequency
```

---

# 27. Date Ranges, Resampling, Shifting, Windows

---

## 27.1 Generating Date Ranges

```python
pd.date_range('2024-01-01', '2024-12-31', freq='D')
pd.date_range('2024-01-01', periods=10,    freq='h')
pd.date_range(end='2024-12-31', periods=12, freq='ME')

pd.bdate_range('2024-01-01', periods=10)                    # business days
pd.period_range('2024-01', '2024-12', freq='M')
pd.timedelta_range(start='0s', end='1h', freq='5min')
```

## 27.2 Pandas 2.x Frequency Aliases

Pandas 2.2 renamed many "month/quarter/year end" aliases for clarity (e.g. `M` → `ME`). The old aliases still work but emit `FutureWarning`.

| Alias | Meaning | Aligns To |
|---|---|---|
| `D` | Calendar day | Midnight |
| `B` | Business day | Mon-Fri |
| `W` / `W-MON`..`W-SUN` | Weekly (default Sunday) | End of week |
| `ME` | Month End | Last day of month |
| `MS` | Month Start | First of month |
| `BME` / `BMS` | Business month end / start | |
| `QE` / `QE-MAR` | Quarter end (default Dec) | |
| `QS` | Quarter start | |
| `YE` / `YE-DEC` | Year end (default Dec) | |
| `YS` | Year start | |
| `h` | Hourly | Top of hour |
| `min` | Minutely | |
| `s` | Secondly | |
| `ms`, `us`, `ns` | Sub-second | |

```python
pd.date_range('2024-01-01', periods=4, freq='ME')
# ['2024-01-31', '2024-02-29', '2024-03-31', '2024-04-30']

pd.date_range('2024-01-01', periods=4, freq='QE-MAR')
# ['2024-03-31', '2024-06-30', '2024-09-30', '2024-12-31']

pd.date_range('2024-01-01', periods=4, freq='W-FRI')
# ['2024-01-05', '2024-01-12', '2024-01-19', '2024-01-26']
```

## 27.3 Resampling

`resample` is `groupby` for time. It changes the frequency of a time-indexed Series or DataFrame.

```python
ts = pd.Series(np.arange(365),
               index=pd.date_range('2024-01-01', periods=365, freq='D'),
               name='value')

ts.resample('ME').sum()                    # downsample to monthly
ts.resample('W-MON').mean()                # downsample to weekly (Mon-anchored)
ts.resample('h').mean()                    # upsample to hourly (NaN until filled)

ts.resample('ME').agg(['sum', 'mean', 'max', 'count'])

# DataFrame with non-index time column
df.resample('ME', on='ts')['value'].sum()
```

| Concept | Downsampling (high → low freq) | Upsampling (low → high freq) |
|---|---|---|
| Examples | daily → weekly | monthly → daily |
| Required step | Aggregation function | Fill (`ffill`, `bfill`, `interpolate`) |
| Methods | `.sum()`, `.mean()`, `.last()`, `.ohlc()` | `.ffill()`, `.bfill()`, `.interpolate()`, `.asfreq()` |

```python
monthly = ts.resample('ME').sum()
monthly.resample('D').ffill()
monthly.resample('D').interpolate(method='linear')
monthly.resample('D').asfreq()             # NaN where no data (no fill)
```

## 27.4 Resample Anchoring and origin

By default, resampling buckets are anchored to "natural" boundaries (midnight for `D`, Sunday for `W`). The `origin` parameter overrides this:

```python
ts.resample('h', origin='start').mean()         # bucket from first timestamp
ts.resample('h', origin='start_day').mean()     # from start of that day
ts.resample('h', offset='15min').mean()         # bucket boundaries shifted by 15 min
ts.resample('15min', closed='right', label='right').mean()
```

| `closed` | Effect |
|---|---|
| `'right'` | Right edge of bucket is included |
| `'left'` (default for most freqs) | Left edge included |

| `label` | Effect |
|---|---|
| `'right'` | Each bucket is labeled by its right edge |
| `'left'` (default for most freqs) | Labeled by left edge |

## 27.5 Shifting and Differencing

```python
s = pd.Series([100, 110, 105, 120, 130])

s.shift(1)            # [NaN, 100, 110, 105, 120]   -- previous value (lag)
s.shift(-1)           # [110, 105, 120, 130, NaN]   -- next value (lead)
s.shift(1, freq='D')  # for time-indexed Series, shifts the *index* by 1 day

s.diff(1)             # [NaN, 10, -5, 15, 10]
s.pct_change(1)       # [NaN, 0.1, -0.045..., 0.143, 0.083]
s.pct_change(periods=4, fill_method=None)
```

## 27.6 Group-Wise Resampling

```python
df.set_index('ts').groupby('symbol').resample('h')['price'].mean()

# Equivalent via pd.Grouper (preferred for chains):
df.groupby([
    'symbol',
    pd.Grouper(key='ts', freq='h')
])['price'].mean()
```

## 27.7 Time-Aware Rolling Windows

If your index is a `DatetimeIndex`, you can pass an offset string as the window:

```python
df.set_index('ts')['price'].rolling('30D').mean()        # 30-calendar-day window
df.set_index('ts')['price'].rolling('1h', closed='left').sum()
```

The window slides by row, but its **size in time** is fixed -- so irregular timestamps are handled correctly without resampling.

## 27.8 asfreq vs resample

`asfreq` simply re-indexes onto a new frequency without aggregation -- the inverse of "no aggregation needed":

```python
ts.asfreq('h')                  # introduces NaN where no observation
ts.asfreq('h', method='ffill')   # forward-fill
ts.asfreq('h', fill_value=0)
```

Use `asfreq` when you only want to align an existing series to a regular grid; use `resample` when you need bucketed aggregation.

---

# 28. Timezones, Business Days, Calendars

---

## 28.1 Naive vs Aware

A "naive" timestamp has no timezone (`tz is None`); an "aware" timestamp carries one. Mixing naive and aware in arithmetic raises `TypeError`. The convention is: **store everything as UTC**, convert only for display.

```python
naive = pd.Timestamp('2024-06-15 12:00')
aware = pd.Timestamp('2024-06-15 12:00', tz='UTC')

naive - aware    # TypeError: cannot subtract tz-naive and tz-aware
```

## 28.2 tz_localize and tz_convert

| Method | Purpose | Precondition |
|---|---|---|
| `tz_localize(tz)` | Attach a timezone (interpret naive timestamp as in that tz) | Currently naive |
| `tz_convert(tz)` | Convert to a different timezone | Currently aware |
| `tz_localize(None)` | Strip timezone (keep wall-clock time) | Currently aware |

```python
ts = pd.Timestamp('2024-06-15 09:00')

ts.tz_localize('US/Pacific')              # 09:00 PDT (UTC-7)
ts.tz_localize('UTC').tz_convert('Asia/Tokyo')   # → 18:00 JST

dti = pd.date_range('2024-06-15', periods=24, freq='h')
dti = dti.tz_localize('UTC').tz_convert('US/Eastern')

df['ts'] = df['ts'].dt.tz_localize('UTC')
df['ts_local'] = df['ts'].dt.tz_convert('Europe/Berlin')
```

## 28.3 Daylight Saving Errors

DST transitions create two error modes that you must handle explicitly:

| Error | Cause | Fix |
|---|---|---|
| `AmbiguousTimeError` | A wall-clock time happens twice (fall back) | `ambiguous='raise' / 'NaT' / 'infer'` or boolean array |
| `NonExistentTimeError` | A wall-clock time is skipped (spring forward) | `nonexistent='raise' / 'NaT' / 'shift_forward' / 'shift_backward' / Timedelta` |

```python
# US/Eastern fall-back: 2024-11-03 01:30 happens twice
pd.Timestamp('2024-11-03 01:30').tz_localize('US/Eastern')
# AmbiguousTimeError

pd.Timestamp('2024-11-03 01:30').tz_localize('US/Eastern', ambiguous='NaT')
pd.Timestamp('2024-11-03 01:30').tz_localize('US/Eastern', ambiguous='infer')

# US/Eastern spring-forward: 2024-03-10 02:30 doesn't exist
pd.Timestamp('2024-03-10 02:30').tz_localize('US/Eastern',
                                               nonexistent='shift_forward')
# → 2024-03-10 03:00-04:00
```

## 28.4 Common Timezone Names

| Region | Names |
|---|---|
| Coordinated Universal | `'UTC'`, `'Etc/UTC'` |
| North America | `'US/Eastern'`, `'US/Pacific'`, `'America/New_York'`, `'America/Los_Angeles'`, `'America/Chicago'` |
| Europe | `'Europe/London'`, `'Europe/Berlin'`, `'Europe/Paris'` |
| Asia | `'Asia/Tokyo'`, `'Asia/Shanghai'`, `'Asia/Kolkata'`, `'Asia/Singapore'` |
| Australia | `'Australia/Sydney'`, `'Australia/Melbourne'` |

Pandas uses the `zoneinfo` module (Python 3.9+) by default; older versions use `pytz`. Either way, the IANA tz database names are accepted.

## 28.5 Business Days and Custom Calendars

```python
from pandas.tseries.offsets import BDay, BMonthEnd, BusinessHour, CustomBusinessDay
from pandas.tseries.holiday import USFederalHolidayCalendar

ts = pd.Timestamp('2024-06-14 (Friday)')

ts + BDay(1)               # Monday 2024-06-17 (skips weekend)
ts + BMonthEnd(1)          # 2024-06-28 (last business day of June)
ts + BusinessHour(8)       # advance 8 business hours

cbd = CustomBusinessDay(calendar=USFederalHolidayCalendar())
pd.date_range('2024-06-01', '2024-07-31', freq=cbd)   # business days excl. US holidays
```

## 28.6 Holidays and Custom Calendars

```python
from pandas.tseries.holiday import (
    AbstractHolidayCalendar, Holiday, nearest_workday
)

class CompanyCalendar(AbstractHolidayCalendar):
    rules = [
        Holiday('NewYears',     month=1,  day=1, observance=nearest_workday),
        Holiday('CompanyDay',   month=6,  day=15),
        Holiday('Christmas',    month=12, day=25, observance=nearest_workday),
    ]

cal = CompanyCalendar()
cal.holidays('2024-01-01', '2024-12-31')
# DatetimeIndex(['2024-01-01', '2024-06-14', '2024-12-25'], dtype='datetime64[ns]')

cbd = CustomBusinessDay(calendar=cal)
pd.date_range('2024-06-01', '2024-12-31', freq=cbd)
```

## 28.7 DateOffset vs Timedelta

| Aspect | `Timedelta` | `DateOffset` |
|---|---|---|
| Magnitude | Fixed nanoseconds | Calendar-aware |
| `+ 1 month` | Not supported | Yes (preserves day-of-month) |
| `+ 1 day` | 24 hours exactly | One calendar day (DST-aware) |
| Backed by | `np.timedelta64[ns]` | Python object |
| Use for | Durations | Calendar arithmetic |

```python
ts = pd.Timestamp('2024-01-31')
ts + pd.Timedelta(days=30)               # 2024-03-01 (just adds 30*24h)
ts + pd.DateOffset(months=1)             # 2024-02-29 (clamped to month end)
ts + pd.tseries.offsets.MonthEnd()        # 2024-01-31 (already month end)
ts + pd.tseries.offsets.MonthEnd(1)       # 2024-02-29
```

## 28.8 Common Pitfalls

```python
# 1. Mixing tz-naive with tz-aware silently breaks merges and comparisons
left['ts']  = pd.to_datetime(left['ts'])             # naive
right['ts'] = pd.to_datetime(right['ts'], utc=True)  # aware
pd.merge_asof(left, right, on='ts')                  # TypeError

# 2. Forgetting to sort before resample
df['value'].resample('D').sum()                      # raises if not sorted by ts

# 3. tz_convert on naive throws
naive_dti.tz_convert('UTC')                          # TypeError -- localize first

# 4. DatetimeIndex with mixed timezones is impossible -- must store as UTC then convert for display

# 5. Pandas 2.2: 'M', 'Q', 'Y' aliases issue FutureWarning -- use 'ME', 'QE', 'YE'
pd.date_range('2024', periods=4, freq='M')           # FutureWarning
pd.date_range('2024', periods=4, freq='ME')          # OK
```

---

# Part 8: I/O, Visualization, Performance

---

# 29. I/O Formats

---

## 29.1 Format Comparison

| Format | Read | Write | Speed | Compression | Schema | Best For |
|---|---|---|---|---|---|---|
| **CSV** | `read_csv` | `to_csv` | Slow | gzip / bz2 / zip | None | Interchange, debugging |
| **Parquet** | `read_parquet` | `to_parquet` | **Fastest** | snappy / gzip / zstd | Strong | Analytics, archives |
| **Feather** | `read_feather` | `to_feather` | **Fastest** | lz4 / zstd | Strong | IPC, short-term cache |
| **HDF5** | `read_hdf` | `to_hdf` | Fast | blosc / zlib | Strong | Hierarchical large data |
| **Excel** | `read_excel` | `to_excel` | Slow | N/A | Weak | Business sharing |
| **JSON** | `read_json` | `to_json` | Medium | gzip | Weak | Web APIs |
| **SQL** | `read_sql` / `read_sql_table` | `to_sql` | Medium | DB-side | Strong | Production pipelines |
| **Pickle** | `read_pickle` | `to_pickle` | Fast | gzip / bz2 | Python | Quick local cache (unsafe across versions) |
| **HTML** | `read_html` | `to_html` | Slow | N/A | None | Scraping, reports |
| **XML** | `read_xml` | `to_xml` | Slow | N/A | DTD | Structured XML feeds |
| **Clipboard** | `read_clipboard` | `to_clipboard` | Manual | N/A | None | Quick interactive |
| **ORC** | `read_orc` | `to_orc` | Fast | zlib / snappy | Strong | Hive-style data lakes |

> Default recommendation: **Parquet** for analytics workflows, **CSV** only for exchange.

## 29.2 CSV

```python
df = pd.read_csv('data.csv')

df = pd.read_csv('data.csv',
    sep=',',
    header=0,                            # row index for column names; None for no header
    names=['a', 'b', 'c'],               # supply names (use with header=None)
    index_col='id',                      # column to use as the row index
    usecols=['id', 'name', 'value'],
    dtype={'id': 'Int64', 'name': 'string'},
    parse_dates=['ts', 'modified'],
    date_format='%Y-%m-%d %H:%M:%S',     # Pandas 2.0+ (replaces date_parser)
    na_values=['NA', 'missing', '-'],
    keep_default_na=True,
    nrows=1000,
    skiprows=[1, 2],
    skipfooter=0,
    comment='#',
    encoding='utf-8',
    encoding_errors='replace',
    chunksize=10_000,                    # iterator of chunks
    on_bad_lines='warn',                 # 'error' / 'warn' / 'skip'
    dtype_backend='pyarrow',             # use Arrow-backed dtypes
)

df.to_csv('out.csv',
    index=False,
    encoding='utf-8',
    compression='gzip',
    float_format='%.4f',
    date_format='%Y-%m-%d',
    quoting=1,                           # csv.QUOTE_ALL
    lineterminator='\n',
)
```

## 29.3 Parquet

```python
df.to_parquet('data.parquet',
    engine='pyarrow',                    # or 'fastparquet'
    compression='snappy',                # 'snappy' / 'gzip' / 'zstd' / 'brotli' / None
    index=False,
    partition_cols=['year', 'month'],     # writes a directory tree
)

df = pd.read_parquet('data.parquet',
    engine='pyarrow',
    columns=['ts', 'value'],             # read only needed columns (huge speed win)
    filters=[('year', '=', 2024)],       # row-group / partition pruning
    dtype_backend='pyarrow',
)

# Reading from a directory of partitioned files
df = pd.read_parquet('s3://bucket/sales/year=2024/')
```

| Parquet Strength | Why It Matters |
|---|---|
| Columnar | `columns=` reads only requested columns (~10x speed on wide data) |
| Compression | 5-10x smaller than CSV typical |
| Schema preserved | dtypes survive round-trips (unlike CSV) |
| Predicate pushdown | `filters=` skips entire row groups |
| Partitioning | Hive-style directory layout for big-data tools |

## 29.4 Feather (Arrow IPC)

```python
df.to_feather('cache.feather', compression='zstd')
df = pd.read_feather('cache.feather', columns=['a', 'b'])
```

Optimized for **fast read/write** between Python and R, and as a short-term local cache. Slightly less ecosystem support than Parquet for archival use.

## 29.5 Excel

```python
df = pd.read_excel('book.xlsx',
    sheet_name='Sheet1',                  # or 0; or list / None for all
    skiprows=2,
    usecols='A:E',
    converters={'phone': str},
    engine='openpyxl',                     # 'openpyxl' / 'calamine' (Pandas 2.2+, fast) / 'xlrd' (legacy .xls)
)

# Multiple sheets at once
sheets = pd.read_excel('book.xlsx', sheet_name=None)   # dict of DataFrames
sheets['Sheet1']

# Write multiple sheets with formatting
with pd.ExcelWriter('out.xlsx', engine='openpyxl') as w:
    df1.to_excel(w, sheet_name='Customers', index=False)
    df2.to_excel(w, sheet_name='Orders',    index=False)

# Append to existing workbook (Pandas 1.3+)
with pd.ExcelWriter('out.xlsx', mode='a', engine='openpyxl', if_sheet_exists='replace') as w:
    df3.to_excel(w, sheet_name='Items')
```

| Engine | Speed | Read .xlsx | Write .xlsx | Notes |
|---|---|---|---|---|
| `openpyxl` | Slow-medium | Yes | Yes | Default; supports formatting |
| `calamine` | **Fastest** | Yes | No | Pandas 2.2+; install `python-calamine` |
| `xlsxwriter` | Medium | No | Yes | Best formatting / charts on write |
| `xlrd` | Legacy | `.xls` only | No | Old binary format |

## 29.6 JSON and json_normalize

```python
df = pd.read_json('data.json', orient='records', lines=True)   # NDJSON
df.to_json('out.json', orient='records', lines=True, date_format='iso')

# orient options
# 'records':  [{'a': 1, 'b': 2}, ...]   ← most common
# 'columns':  {'a': {0: 1, 1: 2}, 'b': {0: 3, 1: 4}}
# 'index':    {0: {'a':1, 'b':3}, 1: {'a':2, 'b':4}}
# 'values':   [[1, 3], [2, 4]]
# 'split':    {'columns':[...], 'index':[...], 'data':[...]}
# 'table':    JSON Table Schema (preserves dtypes)

# Nested JSON → flat DataFrame
data = [
    {'id': 1, 'addr': {'city': 'NYC', 'zip': '10001'}, 'tags': ['py', 'pandas']},
    {'id': 2, 'addr': {'city': 'LA',  'zip': '90001'}, 'tags': ['js']},
]

pd.json_normalize(data, sep='_')
#    id  addr_city addr_zip          tags
# 0   1        NYC    10001  [py, pandas]
# 1   2         LA    90001          [js]

pd.json_normalize(data, record_path='tags', meta=['id', ['addr', 'city']])
#       0  id addr.city
# 0    py   1       NYC
# 1 pandas  1       NYC
# 2    js   2        LA
```

## 29.7 SQL

```python
import sqlalchemy as sa

engine = sa.create_engine('postgresql+psycopg2://user:pw@host:5432/db')

df = pd.read_sql('SELECT * FROM users WHERE age > 25', engine,
    params={'min_age': 25},
    parse_dates=['created_at'],
    dtype={'user_id': 'Int64'},
    chunksize=10_000,                   # iterator of chunks
)

df = pd.read_sql_table('users', engine, columns=['id', 'name', 'created_at'])

df.to_sql('users', engine,
    if_exists='replace',                # 'fail' / 'replace' / 'append'
    index=False,
    method='multi',                      # batch INSERTs
    chunksize=1000,
    dtype={'name': sa.types.String(100)},
)
```

For very large writes, prefer database-native bulk loaders (`COPY` for Postgres) over `to_sql`.

## 29.8 HDF5

```python
df.to_hdf('store.h5', key='df', mode='w', format='table', complevel=9, complib='blosc')

df = pd.read_hdf('store.h5', key='df', where='age > 25', columns=['name', 'age'])

# Persistent store object
with pd.HDFStore('store.h5') as store:
    store['users']  = users_df
    store['orders'] = orders_df
    store.keys()                         # ['/orders', '/users']
    store.select('users', where='age > 30')
```

| Format | Speed | Queryable? |
|---|---|---|
| `'fixed'` | Fastest write | No (read-all only) |
| `'table'` | Slower | **Yes** -- `where=` filters at read time |

## 29.9 Reading Large Files in Chunks

```python
parts = []
for chunk in pd.read_csv('big.csv', chunksize=100_000):
    chunk = chunk[chunk['value'] > 100]
    parts.append(chunk)
df = pd.concat(parts, ignore_index=True)

# Or with a callable transform
def load_filtered(path, predicate, chunksize=100_000):
    return pd.concat(
        (chunk.loc[predicate(chunk)] for chunk in pd.read_csv(path, chunksize=chunksize)),
        ignore_index=True,
    )
```

## 29.10 Pickle (Caveats)

```python
df.to_pickle('cache.pkl', compression='zstd')
df = pd.read_pickle('cache.pkl')
```

- Fast and preserves *every* dtype/object.
- **Not portable** across Pandas/Python versions and **not safe** to load from untrusted sources.
- Use only as a local-process cache.

---

# 30. Plotting and Styling

---

## 30.1 The .plot Accessor

`Series.plot` and `DataFrame.plot` wrap Matplotlib (default) and can also dispatch to alternative backends. Every chart kind is a method on `.plot`.

```python
import matplotlib.pyplot as plt

df.plot(x='ts', y='price')                       # line (default kind)
df.plot.bar(x='dept', y='headcount', stacked=True)
df.plot.barh()
df.plot.hist(bins=30, alpha=0.7)
df.plot.kde()
df.plot.box(by='dept')
df.plot.scatter(x='age', y='salary', c='dept_code', cmap='viridis')
df.plot.hexbin(x='lon', y='lat', gridsize=40)
df.plot.area(stacked=True)
df.plot.pie(y='share')
df['col'].plot.density()
```

| `kind` | Use |
|---|---|
| `'line'` | Default; time-series, trends |
| `'bar'` / `'barh'` | Categorical comparisons |
| `'hist'` | Distributions of continuous data |
| `'box'` / `'kde'` / `'density'` | Distribution shape |
| `'scatter'` | Two continuous vars, optional color/size dim |
| `'hexbin'` | Scatter alternative for very dense data |
| `'area'` | Stacked time series totals |
| `'pie'` | Whole-of-100% (use sparingly) |

## 30.2 Customization Without Leaving Pandas

```python
ax = df.plot(x='ts', y=['a', 'b', 'c'],
    figsize=(10, 6),
    title='Three signals',
    xlabel='time',
    ylabel='value',
    grid=True,
    color=['#0e639c', '#e68a00', '#4caf50'],
    style=['-', '--', ':'],
    legend=True,
    rot=45,                                # x-tick rotation
)
ax.set_ylim(0, 100)
plt.tight_layout()
```

## 30.3 Subplots

```python
df.plot(subplots=True, figsize=(8, 10), sharex=True)              # one subplot per column

axes = df.plot(subplots=[('a', 'b'), 'c'], figsize=(10, 8))       # group 'a' & 'b' together
```

## 30.4 Other Plotting Helpers

```python
from pandas.plotting import scatter_matrix, parallel_coordinates, andrews_curves

scatter_matrix(df[['a','b','c']], figsize=(8, 8), diagonal='kde')
parallel_coordinates(df, class_column='label')
andrews_curves(df, 'label')
pd.plotting.autocorrelation_plot(s)
pd.plotting.lag_plot(s)
```

## 30.5 Switching Plotting Backend

```python
pd.set_option('plotting.backend', 'plotly')         # requires plotly
df.plot(x='ts', y='price')                          # now an interactive plotly figure

pd.set_option('plotting.backend', 'matplotlib')     # back to default
```

Other supported backends include `pandas-bokeh`, `hvplot.pandas`, and `plotly`.

## 30.6 The Styler API (`df.style`)

`df.style` returns a `Styler` for **rich display** (HTML / Excel / LaTeX), with conditional formatting, gradient backgrounds, and column-wise number formatting. The data itself is not modified.

```python
styler = (
    df.style
      .format({'salary': '${:,.0f}', 'rate': '{:.1%}'})
      .background_gradient(cmap='RdYlGn', subset='salary')
      .bar(subset=['headcount'], color='#5fba7d')
      .highlight_max(subset='salary', color='lightgreen')
      .highlight_min(subset='salary', color='salmon')
      .highlight_null(color='lightgrey')
      .set_caption('Department Summary')
      .set_table_styles([
          {'selector': 'th', 'props': [('background-color', '#f0f0f0')]},
      ])
      .hide(axis='index')
)

styler                                       # rendered in Jupyter
styler.to_html('report.html')
styler.to_excel('report.xlsx', engine='openpyxl')
styler.to_latex()
```

| Method | Effect |
|---|---|
| `.format(spec, subset=)` | Number/date formatting |
| `.background_gradient(cmap=)` | Heatmap fill |
| `.bar(subset=, color=)` | In-cell bars |
| `.highlight_max` / `min` / `null` / `between` | Conditional highlights |
| `.applymap(style_func)` | Per-cell custom CSS |
| `.apply(style_func, axis=)` | Per-row or per-column custom CSS |
| `.set_caption` / `.set_table_styles` | Table-level CSS |
| `.hide(axis=, subset=)` | Hide rows/columns/index/level |
| `.to_html` / `.to_excel` / `.to_latex` | Export the styled output |

```python
# Custom row-wise styling
def color_negative_red(s):
    return ['color: red' if v < 0 else '' for v in s]

df.style.apply(color_negative_red, subset=['delta'])
```

---

# 31. Performance

---

## 31.1 Vectorize, Don't Iterate

The single biggest performance lever in Pandas: never write a Python `for` loop over rows when a vectorized expression exists.

```python
# SLOW: row-wise apply (Python loop)
df['total'] = df.apply(lambda row: row['price'] * row['qty'], axis=1)

# FAST: vectorized
df['total'] = df['price'] * df['qty']
```

| Approach | Relative Speed | Why |
|---|---|---|
| Python `for` over `iterrows` | 1x (baseline) | Per-row Python overhead |
| `itertuples` | ~5x | namedtuples are cheaper than Series |
| `df.apply(axis=1)` | ~5-10x | Internal loop, still Python-level |
| `df.apply(axis=0)` (per column) | ~50x | One call per column, vectorized inside |
| Pure vectorized arithmetic | ~100-500x | C-level loop, no Python |

## 31.2 eval and query for Large Frames

For DataFrames over a million rows, `eval` and `query` use `numexpr` to multi-thread expressions and avoid temporary arrays:

```python
df.eval('c = a + b * 2 - log(d)', inplace=True)
df.query('a > 10 and b < 50 and c.notnull()')
```

Crossover point: `eval`/`query` are slower than direct expressions for small frames (~10K rows) but pull ahead beyond ~100K rows.

## 31.3 Built-in Methods Beat apply

Pandas / NumPy ship **Cython-optimized** kernels for many common functions. If a built-in method exists, use it instead of `apply`:

| Instead of `apply(...)` | Use |
|---|---|
| `s.apply(lambda x: x ** 2 + 1)` | `s ** 2 + 1` |
| `s.apply(np.log)` | `np.log(s)` |
| `s.apply(lambda x: x.upper())` | `s.str.upper()` |
| `df.apply(lambda r: r.sum(), axis=1)` | `df.sum(axis=1)` |
| `df.groupby('k').apply(lambda g: g['x'].mean())` | `df.groupby('k')['x'].mean()` |
| `s.apply(lambda x: x in {'a','b'})` | `s.isin(['a','b'])` |

## 31.4 Cython-Optimized GroupBy Operations

These groupby methods run in compiled Cython and are dramatically faster than `apply`:

```
sum, mean, median, min, max, first, last, nth, count, size, std, var, sem,
prod, cumsum, cumprod, cummin, cummax, cumcount, ngroup, rank, idxmin, idxmax,
shift, diff, pct_change, fillna, bfill, ffill, head, tail
```

Whenever a problem can be expressed as one of these, prefer it over `g.apply(...)`.

## 31.5 The Numba Engine

Some methods accept `engine='numba'` to JIT-compile a custom function:

```python
df.groupby('k')['x'].transform(custom_func, engine='numba')
df['x'].rolling(100).apply(custom, engine='numba', raw=True)
```

| Engine | Compile Cost | Steady-state Speed |
|---|---|---|
| `'cython'` (default) | None | Fast, only built-ins |
| `'numba'` | ~1 s first call | Fast for **custom** functions, especially loops |

Use Numba when you need a **custom** reduction or rolling function over millions of rows.

## 31.6 Iteration Patterns (When You Truly Must)

```python
# iterrows -- slowest; returns (index, Series) tuples
for idx, row in df.iterrows():
    process(row['a'], row['b'])

# itertuples -- 3-10x faster; returns namedtuples
for row in df.itertuples(index=False, name='Row'):
    process(row.a, row.b)

# items / iteritems -- iterate over (column name, Series) pairs
for col_name, col in df.items():
    process(col_name, col)

# Plain ndarray iteration is fastest
arr = df[['a', 'b']].to_numpy()
for a, b in arr:
    process(a, b)
```

`itertuples(index=False, name=None)` is fastest among the named iterators. But as a rule, treat any explicit iteration as a code smell and rewrite vectorized.

## 31.7 Method Chaining and Lazy Construction

Chaining helps performance by letting Pandas avoid intermediate copies, and CoW makes this even more efficient:

```python
result = (
    raw_df
    .query('age >= 18')
    .assign(
        salary_k = lambda d: d['salary'] / 1000,
        bracket  = lambda d: pd.cut(d['salary_k'], bins=[0, 50, 100, np.inf]),
    )
    .groupby('bracket', observed=True)
    .agg(headcount=('name', 'count'), avg_age=('age', 'mean'))
    .sort_values('headcount', ascending=False)
)
```

## 31.8 inplace -- Don't

`inplace=True` does **not** save memory in most cases (Pandas often makes the change in a copy and reassigns internally) and breaks method chaining. It is being deprecated for many operations:

```python
# AVOID
df.drop(columns=['temp'], inplace=True)
df.fillna(0, inplace=True)
df.sort_values('a', inplace=True)

# PREFER
df = df.drop(columns=['temp'])
df = df.fillna(0)
df = df.sort_values('a')
```

## 31.9 Benchmarking Pattern

```python
import time

def bench(label, func, *args, repeat=3):
    times = []
    for _ in range(repeat):
        t = time.perf_counter()
        func(*args)
        times.append(time.perf_counter() - t)
    print(f'{label:30s}  {min(times)*1000:8.2f} ms')

bench('apply',      lambda: df.apply(lambda r: r.a + r.b, axis=1))
bench('vectorized', lambda: df['a'] + df['b'])
bench('eval',       lambda: df.eval('a + b'))
```

For deeper profiling: `%timeit` (IPython), `cProfile`, `line_profiler`, `py-spy`.

---

# 32. Memory Optimization

---

## 32.1 Profiling Memory

```python
df.info(memory_usage='deep')          # 'deep' follows object pointers
df.memory_usage(deep=True)            # Series of bytes per column
df.memory_usage(deep=True).sum()       # total
```

The `'deep'` flag is critical for `object` columns -- without it, you only see the size of the pointer array, not the actual strings.

## 32.2 Six Levers, in Order

| # | Lever | Typical Win |
|---|---|---|
| 1 | Convert `object` strings → `string[pyarrow]` | 5-10x |
| 2 | Convert low-cardinality strings → `category` | up to 100x |
| 3 | Downcast integers / floats | 2-8x |
| 4 | Use nullable `Int64` / `Float64` if NA present | Same as base + correctness |
| 5 | Use Parquet (`dtype_backend='pyarrow'`) on read | 5-10x |
| 6 | Use `SparseDtype` for very sparse columns | 10-100x |

## 32.3 Downcasting Numerics

```python
df['count'] = pd.to_numeric(df['count'], downcast='integer')   # int64 → int8 if fits
df['ratio'] = pd.to_numeric(df['ratio'], downcast='float')      # float64 → float32

# Manual control
df['user_id'] = df['user_id'].astype('uint32')
```

## 32.4 Categoricals for Strings

```python
df['status'] = df['status'].astype('category')
df['country'] = df['country'].astype('category')

before = df.memory_usage(deep=True).sum()
df['country'] = df['country'].astype('category')
after  = df.memory_usage(deep=True).sum()
print(f'{before / 2**20:.1f} MB → {after / 2**20:.1f} MB')
```

Best when distinct value count is much smaller than row count (rule of thumb: < 1% unique).

## 32.5 PyArrow Backend on Read

```python
df = pd.read_csv('big.csv', dtype_backend='pyarrow')
df = pd.read_parquet('big.parquet', dtype_backend='pyarrow')

df.dtypes
# id          int64[pyarrow]
# name        string[pyarrow]
# created_at  timestamp[ns][pyarrow]
```

PyArrow strings are **always** smaller than `object` strings; numeric Arrow columns are similar to NumPy but with first-class NA support. For wide string-heavy frames the savings are routinely 5-10x.

## 32.6 SparseDtype

For columns with a dominant fill value (e.g. one-hot encoded vectors), `SparseDtype` stores only the non-fill values:

```python
import pandas as pd, numpy as np

dense = pd.Series(np.zeros(10_000_000))
dense[::1000] = 1.0

sparse = dense.astype(pd.SparseDtype('float64', fill_value=0.0))

dense.memory_usage()    # 80,000,128 bytes
sparse.memory_usage()   # ~120,128 bytes (about 666x less)
```

Operations on sparse arrays are slower per-row but vastly cheaper to store and stream.

## 32.7 Chunked Reading

When the file simply does not fit in memory:

```python
agg = pd.Series(0, dtype='Int64')
for chunk in pd.read_csv('big.csv', chunksize=500_000, usecols=['user_id', 'amount']):
    agg = agg.add(chunk.groupby('user_id')['amount'].sum(), fill_value=0)
```

For SQL: `pd.read_sql(..., chunksize=N)`. For Parquet: read by partition or use Polars / DuckDB.

## 32.8 The convert_dtypes One-Shot

A pragmatic first step on a legacy frame:

```python
df_lean = df.convert_dtypes(dtype_backend='pyarrow')
df_lean.info(memory_usage='deep')
```

This single call typically converts `object` → `string[pyarrow]`, `int64` with NaNs → `Int64`, `float64` with no fractional parts → `Int64`, etc. -- a quick win before more targeted optimization.

---

# Part 9: Internals, Ecosystem, Pitfalls

---

# 33. Pandas Internals and Testing

---

## 33.1 The BlockManager Model (Legacy)

Historically, a Pandas DataFrame stored its data in a `BlockManager` -- a collection of **Blocks**, each containing a 2-D NumPy array of one dtype. Columns of the same dtype lived together in one block; mixed-dtype frames had multiple blocks.

```
DataFrame columns: ['a', 'b', 'c', 'd', 'e']
                    int64 int64 float64 object datetime64

BlockManager:
    Block(int64,        rows × 2)   ← columns 'a', 'b' co-located
    Block(float64,      rows × 1)   ← column 'c'
    Block(object,       rows × 1)   ← column 'd'
    Block(datetime64,   rows × 1)   ← column 'e'
```

Implications of this layout:

| Operation | Cost |
|---|---|
| `df['a'] + df['b']` (same dtype block) | Cheap (single C loop) |
| `df['a'] + df['c']` (cross-block) | Promotion + copy |
| Adding a new column | Cheap (new block) |
| Inserting a row | Expensive (rewrites all blocks) |
| `df.values` on mixed-dtype | Forces upcast to `object` (slow + memory) |

## 33.2 Toward Arrow-Native Storage

Pandas 2.x is steadily migrating toward **per-column** storage (one buffer per column) backed by either NumPy or PyArrow `ExtensionArray`. With `dtype_backend='pyarrow'` you get this layout today. Benefits:

| Benefit | Detail |
|---|---|
| No more cross-block surprises | Each column is its own buffer |
| First-class extension types | `string`, `category`, `ArrowDtype(...)` are not bolted on |
| Zero-copy interop | Arrow buffers can be shared with Polars, DuckDB, Spark |
| Better CoW semantics | Per-column reference counting is cleaner |

Code that depends on `df.values` returning a single 2-D array for mixed-dtype frames is fragile. Use `df.to_numpy(dtype='object')` if you really need that, or operate column-by-column instead.

## 33.3 The Index Hash Table

Every `Index` lazily builds a hash table on first lookup, giving O(1) expected `loc` access. This is why the **first** `df.loc[label]` on a fresh frame can be slower than subsequent ones -- the hash table is being constructed.

```python
df = pd.DataFrame(np.random.randn(1_000_000, 3), columns=['a','b','c'])
df.index.is_unique             # True

%timeit df.loc[500_000]        # first call slow (builds hash table)
%timeit df.loc[500_000]        # subsequent calls fast (~µs)
```

For very high-frequency single-row lookups, consider:

- Sorting + `.iloc[]` with a binary search via `searchsorted`.
- Switching to a dict for pure lookup workloads.
- Pre-building the index hash by accessing one element after construction.

## 33.4 Why Some Operations Are Slow

| Slow Operation | Underlying Cause | Faster Alternative |
|---|---|---|
| `df.iterrows()` | Boxes each row into a Series object | Vectorized expression / `itertuples` |
| `pd.concat` in a loop | Each call copies the entire growing frame | Build a list, concat once |
| `df.apply(axis=1)` | Python-level loop over rows | Vectorized arithmetic |
| `df.sort_values(...)` on object columns | Lexicographic compare in Python | Convert to category or numeric first |
| `df.groupby('cat_col').apply(...)` | Per-group Python call | `agg`/`transform` with built-ins |
| Repeated `loc` assignment | Each call allocates and copies | Precompute mask, assign once |

## 33.5 Testing with pd.testing

The `pandas.testing` namespace provides assertion helpers that handle dtype, NA, and ordering subtleties correctly. Use these in tests instead of plain `==`.

| Function | Compares |
|---|---|
| `pd.testing.assert_frame_equal(left, right, ...)` | Two DataFrames |
| `pd.testing.assert_series_equal(left, right, ...)` | Two Series |
| `pd.testing.assert_index_equal(left, right, ...)` | Two Indexes |
| `pd.testing.assert_extension_array_equal(left, right)` | Two ExtensionArrays |

```python
import pandas as pd
import pandas.testing as pdt

expected = pd.DataFrame({'a': [1, 2, 3]}, index=['x', 'y', 'z'])
actual   = my_func()

pdt.assert_frame_equal(actual, expected,
    check_dtype=True,
    check_exact=False,
    rtol=1e-5,
    atol=1e-8,
    check_like=False,        # if True, ignore row/column order
    check_names=True,
    check_freq=True,         # for time-indexed frames
    check_categorical=True,
    check_column_type=True,
)
```

Useful flags in practice:

- `check_dtype=False` when comparing an `Int64` result against an int literal column.
- `check_like=True` when the row/column order doesn't matter.
- `check_exact=False` with `rtol`/`atol` for floating point.

## 33.6 Property-Based Testing with hypothesis

`hypothesis` ships a `pandas` extra (`hypothesis[pandas]`) that generates DataFrames, Series, and indexes:

```python
from hypothesis import given
from hypothesis.extra.pandas import data_frames, columns, range_indexes

@given(data_frames(
    columns=columns(['a', 'b'], dtype=int),
    index=range_indexes(min_size=1, max_size=100),
))
def test_my_pipeline(df):
    out = my_pipeline(df)
    assert len(out) <= len(df)
```

This catches edge cases (empty frames, NaN columns, MultiIndexes) that hand-written tests miss.

## 33.7 Key Pandas Exceptions

| Exception | Raised When |
|---|---|
| `KeyError` | Label not found in `.loc[...]` |
| `IndexError` | Position out of range in `.iloc[...]` |
| `ValueError` | Shape / value mismatch (most common) |
| `TypeError` | Operation not supported between two dtypes |
| `pd.errors.MergeError` | `validate=` check fails on merge |
| `pd.errors.IndexingError` | Bad indexer (e.g. boolean array of wrong length) |
| `pd.errors.ParserError` | CSV parser failure |
| `pd.errors.DtypeWarning` | Mixed dtypes inferred during chunked read |
| `pd.errors.PerformanceWarning` | E.g. unsorted MultiIndex slicing |
| `pd.errors.ChainedAssignmentError` | CoW: chained assignment attempt |
| `pd.errors.SettingWithCopyWarning` | Pre-CoW: chained-assignment ambiguity |
| `pd.errors.UnsortedIndexError` | Slicing an unsorted MultiIndex |
| `pd.errors.AmbiguousTimeError` | tz_localize during DST fall-back |
| `pd.errors.NonExistentTimeError` | tz_localize during DST spring-forward |

---

# 34. Ecosystem and When to Switch

---

## 34.1 The Pandas Ecosystem Today

| Library | Niche | Strengths | Weaknesses vs Pandas |
|---|---|---|---|
| **NumPy** | Numeric arrays | Foundation for everything | No labels, no NA, no string ops |
| **PyArrow** | Columnar in-memory format | Compression, IPC, types | Lower-level than Pandas |
| **Polars** | DataFrames in Rust | 5-30x faster, lazy execution, multi-threaded by default | Different API, less ecosystem |
| **DuckDB** | In-process OLAP SQL | SQL on Pandas/Parquet, very fast joins | SQL surface; not Python-idiomatic |
| **Dask** | Parallel / out-of-core Pandas | Same Pandas API, scales to clusters | Python overhead, lazy semantics |
| **Modin** | Drop-in parallel Pandas | `import modin.pandas as pd` and you're done | Coverage gaps; varies by backend |
| **cuDF** (RAPIDS) | GPU-accelerated DataFrames | 10-100x on NVIDIA GPUs | Hardware requirement, narrower API |
| **Vaex** | Out-of-core, lazy | Memory-mapped, billions of rows | Less active; smaller ecosystem |
| **PySpark** | Distributed compute | JVM cluster scale | High overhead, JVM dependency |

## 34.2 When to Stay in Pandas

- Datasets that fit comfortably in RAM (rule of thumb: ≤ 5x available memory after compression).
- Heterogeneous data wrangling with lots of `apply`-style logic that has no vectorized form.
- Need for the **broadest** ecosystem (matplotlib, seaborn, scikit-learn, statsmodels, ...).
- Quick exploration in notebooks where ergonomics matter more than throughput.

## 34.3 When to Try Polars

- Datasets larger than a few GB but still single-node.
- Pipelines dominated by `groupby`, `join`, `filter`, `sort` -- where Polars routinely runs 10-30x faster.
- Want lazy execution and query-plan optimization (`pl.scan_csv(...).filter(...).collect()`).
- New project where API breakage from migration is a non-issue.

```python
import polars as pl

(
    pl.scan_parquet('big.parquet')
      .filter(pl.col('age') > 18)
      .group_by('dept')
      .agg(pl.col('salary').mean().alias('avg_salary'))
      .sort('avg_salary', descending=True)
      .collect()
)
```

`pl.from_pandas(df)` and `df.to_pandas()` make round-tripping cheap.

## 34.4 When to Use DuckDB Alongside Pandas

DuckDB runs SQL **directly against Pandas DataFrames and Parquet files**, often beating native Pandas on joins and aggregations -- without leaving the Python process:

```python
import duckdb

result = duckdb.sql('''
    SELECT region, AVG(revenue) AS avg_rev
    FROM df
    WHERE year = 2024
    GROUP BY region
    ORDER BY avg_rev DESC
''').df()
```

Particularly powerful when:

- You think in SQL.
- You need fast joins on multi-million-row tables.
- You want to query Parquet without loading it fully.

## 34.5 When to Reach for Dask / Modin

- Data is genuinely too large for RAM, OR you need to scale across CPU cores / machines.
- Existing Pandas code you'd rather not rewrite.
- Acceptable to deal with lazy semantics and occasional API gaps.

```python
import dask.dataframe as dd
ddf = dd.read_parquet('s3://bucket/year=*/')
ddf.groupby('region').revenue.mean().compute()
```

## 34.6 When to Use cuDF

- You have an NVIDIA GPU and a workload dominated by `groupby` / `join` over numeric columns.
- Acceptable to constrain to the cuDF subset of the Pandas API.

```python
import cudf
gdf = cudf.read_parquet('big.parquet')
gdf.groupby('region').revenue.sum().to_pandas()
```

## 34.7 Decision Cheat-Sheet

| Constraint | First Choice | Fallback |
|---|---|---|
| Fits in RAM, broad library coverage | Pandas | -- |
| Fits in RAM, fastest possible single-node | Polars | DuckDB |
| Heavy SQL-style joins / aggregations | DuckDB | Polars |
| Bigger than RAM, single node | Polars (lazy) / DuckDB | Dask |
| Distributed across cluster | Dask / PySpark | Ray + Modin |
| GPU available, numeric workload | cuDF | Pandas + numba |

---

# 35. Idioms and Method Chaining Recipes

---

## 35.1 The Idiomatic Pipeline

Idiomatic Pandas is **chained**, **lazy in spirit**, and **avoids `inplace`**. A typical end-to-end transformation reads top-to-bottom like a recipe:

```python
out = (
    pd.read_csv('orders.csv',
                parse_dates=['ts'],
                dtype_backend='pyarrow')
      .pipe(drop_obvious_bad_rows)
      .assign(
          revenue   = lambda d: d['price'] * d['qty'],
          ts_local  = lambda d: d['ts'].dt.tz_localize('UTC').dt.tz_convert('US/Eastern'),
          weekday   = lambda d: d['ts_local'].dt.day_name(),
          is_weekend= lambda d: d['ts_local'].dt.dayofweek.isin([5, 6]),
      )
      .query('revenue > 0 and qty < 1000')
      .merge(customers[['id', 'segment']], left_on='customer_id', right_on='id')
      .groupby(['segment', 'weekday'])
      .agg(
          orders   =('order_id', 'count'),
          revenue  =('revenue', 'sum'),
          aov      =('revenue', 'mean'),
      )
      .sort_values('revenue', ascending=False)
      .reset_index()
)
```

## 35.2 Recipe: Top-N per Group

```python
df.sort_values(['dept', 'salary'], ascending=[True, False]) \
  .groupby('dept').head(3)

# or with rank
df['rank'] = df.groupby('dept')['salary'].rank(method='dense', ascending=False)
top3 = df[df['rank'] <= 3].drop(columns='rank')
```

## 35.3 Recipe: Z-Score Within Group

```python
df['salary_z'] = (
    df.groupby('dept')['salary']
      .transform(lambda s: (s - s.mean()) / s.std(ddof=0))
)
```

## 35.4 Recipe: Forward-Fill Within Group

```python
df = df.sort_values(['user_id', 'ts'])
df['last_known_status'] = df.groupby('user_id')['status'].ffill()
```

## 35.5 Recipe: Pivot With Margins (Including a Total Row)

```python
pt = pd.pivot_table(
    sales, values='revenue',
    index='region', columns='product',
    aggfunc='sum', fill_value=0,
    margins=True, margins_name='Total',
)
```

## 35.6 Recipe: Conditional Column with np.select

```python
import numpy as np

conditions = [
    df['score'] >= 90,
    df['score'] >= 75,
    df['score'] >= 60,
]
choices = ['A', 'B', 'C']
df['grade'] = np.select(conditions, choices, default='F')
```

## 35.7 Recipe: Replace SettingWithCopyWarning

```python
# BAD
sub = df[df['x'] > 0]
sub['y'] = 0                                # SettingWithCopyWarning

# GOOD (write to original via .loc)
df.loc[df['x'] > 0, 'y'] = 0

# GOOD (work on an explicit copy)
sub = df[df['x'] > 0].copy()
sub['y'] = 0
```

## 35.8 Recipe: Joining with Validation

```python
# Always validate when you believe the right side is unique
out = pd.merge(
    orders, products,
    on='product_id',
    how='left',
    validate='m:1',
    indicator=True,
)
assert (out['_merge'] != 'left_only').all(), 'orders with no matching product'
out = out.drop(columns='_merge')
```

## 35.9 Recipe: Wide → Long → Pivot Round-Trip for Reshaping

```python
long = df.melt(id_vars=['id'], var_name='metric', value_name='value')
filtered = long.query('metric in ["sales", "cost"]')
wide = filtered.pivot(index='id', columns='metric', values='value')
wide['margin'] = wide['sales'] - wide['cost']
```

## 35.10 Recipe: Time-Series Resample + Group

```python
daily_per_symbol = (
    trades
      .sort_values('ts')
      .groupby('symbol')
      .resample('D', on='ts')['price']
      .agg(['first', 'max', 'min', 'last', 'count'])
      .rename(columns={'first': 'open', 'max': 'high',
                        'min': 'low', 'last': 'close', 'count': 'n_trades'})
)
```

## 35.11 Recipe: Fast Bulk Update with map

```python
# Lookup table pattern
mapping = pd.Series({'NYC': 'East', 'LA': 'West', 'CHI': 'Central'})
df['region'] = df['city'].map(mapping).fillna('Other')
```

## 35.12 Recipe: Building an Append-Only Dataset Without O(n²)

```python
parts = []
for path in sorted(paths):
    parts.append(
        pd.read_parquet(path, columns=['ts', 'symbol', 'price'])
          .assign(source=path.stem)
    )
combined = pd.concat(parts, ignore_index=True)
```

---

# 36. Common Pitfalls and Interview Questions

---

## 36.1 Common Pitfalls

**Pitfall 1: SettingWithCopyWarning / chained assignment**

```python
df[df['a'] > 5]['b'] = 10                # may modify a copy; warning
df.loc[df['a'] > 5, 'b'] = 10            # always works
```

**Pitfall 2: NaN forces int → float**

```python
pd.Series([1, 2, None]).dtype             # float64
pd.Series([1, 2, None], dtype='Int64').dtype   # Int64 (correct)
```

**Pitfall 3: Comparing with NaN/NA**

```python
np.nan == np.nan                          # False
pd.NA  == pd.NA                           # pd.NA (propagates)
s.isna()                                   # the right way
```

**Pitfall 4: merge silently produces no matches due to dtype mismatch**

```python
left['id']  = pd.array([1, 2, 3], dtype='Int64')
right['id'] = pd.array(['1','2','3'], dtype='string')
pd.merge(left, right, on='id')             # empty -- normalize dtypes first
```

**Pitfall 5: apply when vectorization exists**

```python
df['total'] = df.apply(lambda r: r['p'] * r['q'], axis=1)   # slow
df['total'] = df['p'] * df['q']                              # fast
```

**Pitfall 6: Logical operators in boolean masks**

```python
df[df['a'] > 0 and df['b'] < 5]           # ValueError: ambiguous truth value
df[(df['a'] > 0) & (df['b'] < 5)]         # parentheses + & required
```

**Pitfall 7: Forgetting to sort before resample / merge_asof**

```python
df.set_index('ts')['v'].resample('D').sum()      # needs sorted ts
pd.merge_asof(left, right, on='ts')               # both sides must be sorted
```

**Pitfall 8: Unsorted MultiIndex**

```python
df.loc[pd.IndexSlice[:, '2024', 'Q1':'Q2']]      # UnsortedIndexError if not sorted
df = df.sort_index()                              # fix
```

**Pitfall 9: Categorical fillna with non-category value**

```python
cat.fillna('z')                           # ValueError if 'z' not in categories
cat = cat.cat.add_categories(['z']); cat.fillna('z')   # OK
```

**Pitfall 10: Mixing tz-naive with tz-aware**

```python
naive  - aware                            # TypeError
df['ts'] = pd.to_datetime(df['ts'], utc=True)  # standardize early
```

**Pitfall 11: Pandas 2.x freq aliases**

```python
pd.date_range('2024', periods=4, freq='M')   # FutureWarning
pd.date_range('2024', periods=4, freq='ME')  # use the new alias
```

**Pitfall 12: applymap is deprecated**

```python
df.applymap(func)                         # DeprecationWarning in Pandas 2.1+
df.map(func)                               # use this instead
```

**Pitfall 13: `inplace=True` is rarely a win**

```python
df.fillna(0, inplace=True)                # internal copy + reassignment anyway
df = df.fillna(0)                          # cleaner, chainable, equally efficient
```

**Pitfall 14: Boolean mask with NA values**

```python
mask = pd.Series([True, pd.NA, False], dtype='boolean')
df[mask]                                   # raises in Pandas 2.x
df[mask.fillna(False)]                     # explicit handling
```

**Pitfall 15: Reading CSV without dtype hints**

```python
df = pd.read_csv('big.csv')                # may infer 'object' for everything
df = pd.read_csv('big.csv', dtype={'id': 'Int64', 'name': 'string'})
```

## 36.2 Interview Questions

**Q1. What is the difference between `loc` and `iloc`?**

`loc` is **label-based**; slices are **inclusive** of both endpoints. `iloc` is **position-based**; slices follow standard Python (exclusive end). `loc` raises `KeyError` for missing labels; `iloc` raises `IndexError` for out-of-range positions. Both accept booleans and callables; `loc` additionally accepts arbitrary label types (strings, datetimes, tuples for MultiIndex).

**Q2. Explain the GroupBy split-apply-combine pattern, including the differences between `agg`, `transform`, `filter`, and `apply`.**

`groupby` splits the frame on the group key and yields a `GroupBy` object. `agg` applies a reduction per group and returns one row per group. `transform` applies a function per group and returns the same shape as the input -- broadcasting per-group results back. `filter` returns the original rows from groups for which a boolean function returns True. `apply` is the catch-all: it accepts a function that takes a sub-DataFrame and returns anything, but it is the slowest and least predictable.

**Q3. What is the difference between `merge`, `join`, and `concat`?**

`merge` is SQL-style key-based join (inner / left / right / outer / cross). `join` is a thin wrapper for joining on the right's index (and optionally a column on the left). `concat` is non-key stacking along an axis -- it does not match on values, just glues frames together with optional alignment on the *other* axis.

**Q4. When should you use a Categorical dtype?**

Use it when a column has **low cardinality** -- the number of distinct values is much smaller than the number of rows. Benefits: dramatic memory savings (often >95%), faster `groupby` / `sort` / equality comparisons (operations on integer codes), and support for **custom ordering** via `pd.CategoricalDtype(ordered=True)`.

**Q5. How do you handle a CSV file that does not fit in memory?**

(1) `pd.read_csv(..., chunksize=N)` returns an iterator of chunks; aggregate per chunk and concat or accumulate. (2) Use `usecols=` to read only needed columns. (3) Specify `dtype=` to avoid the slow inference pass and shrink memory. (4) Switch to **Parquet** (columnar + compressed). (5) For repeated workloads, switch to **Polars** or **DuckDB** -- both can stream directly off Parquet.

**Q6. What is the difference between `pivot` and `pivot_table`?**

`pivot` is a pure shape transformation that requires unique `(index, columns)` pairs and raises `ValueError` if there are duplicates. `pivot_table` accepts duplicates by applying an `aggfunc` (default `mean`); it also supports `margins`, multiple aggregations, and `fill_value`.

**Q7. Explain Copy-on-Write (CoW) in Pandas 2.x / 3.0.**

Under CoW every indexing operation conceptually returns an independent object, but data buffers are shared lazily until the first write. The first mutation triggers a copy of the affected buffer, and the original frame is never modified by writing to a "subset" view. This eliminates `SettingWithCopyWarning` (replaced by a deterministic `ChainedAssignmentError`), preserves zero-copy reads, and makes Pandas semantics predictable. CoW is opt-in in 2.x via `pd.options.mode.copy_on_write = True` and the default in 3.0.

**Q8. Why is `apply(axis=1)` slow, and how do you avoid it?**

Because it executes a Python-level loop over rows, each iteration paying the cost of creating a Series (or namedtuple) and dispatching to a Python callback. Avoid it by: (1) expressing the row-level computation as vectorized column arithmetic; (2) using `np.where` / `np.select` for conditional logic; (3) using `s.map(dict)` for lookups; (4) using built-in groupby aggregations; (5) for a genuinely row-wise function on huge data, dropping to NumPy with `df.to_numpy()` and looping there, or using `numba` with `engine='numba'` on `apply`.

**Q9. What is the difference between `np.nan`, `pd.NaT`, and `pd.NA`?**

`np.nan` is IEEE-754 float NaN, used in NumPy-backed numeric columns; comparison with itself is False, and Boolean operations follow NumPy two-valued logic. `pd.NaT` is "Not-a-Time", the missing-value sentinel for datetime / timedelta / period dtypes. `pd.NA` is a singleton missing value used by **nullable extension dtypes** (`Int64`, `Float64`, `boolean`, `string`, `ArrowDtype`); it implements proper three-valued (Kleene) logic, so `True | NA == True`, `False | NA == NA`, etc. In all three cases `==` does not detect missing -- always use `isna()` / `notna()`.

**Q10. What are the advantages of the PyArrow backend over the legacy NumPy backend?**

(1) Native missing-value support for **all** dtypes (no more int → float on NA). (2) First-class string storage that is 5-10x smaller and 2-10x faster than `object`. (3) Native nested types (`list`, `struct`, `map`). (4) Decimal, fixed-size binary, and dictionary types unavailable in NumPy. (5) Zero-copy interop with Parquet, Feather, Polars, DuckDB, and Spark. (6) Modern compute kernels (Arrow C++) often outperform NumPy on strings and datetimes. Trade-off: some Pandas methods still convert back to NumPy internally, and a few downstream libraries don't yet handle Arrow-backed dtypes natively.

**Q11. Explain the difference between `merge_asof` and a regular `merge`.**

A regular `merge` requires **exact** key equality. `merge_asof` matches each left row to the **nearest** right row (by default, the most recent right row at or before the left key). Both inputs must be sorted on the join key. This is the canonical pattern for joining trades to quotes in finance, sensor readings to logs, or any time series where left and right have non-aligned timestamps. Parameters of interest: `direction` (`'backward'` / `'forward'` / `'nearest'`), `tolerance` (max allowed gap), and `by=` (group within which to as-of-merge, e.g. by symbol).

**Q12. How does `resample` differ from `groupby`?**

`resample` is `groupby` for time. It buckets a time-indexed Series/DataFrame into fixed-frequency bins (e.g. `'D'`, `'ME'`, `'h'`) and applies an aggregation. Unlike `groupby`, which uses arbitrary keys, `resample` understands time-bucket alignment, partial buckets, downsampling vs upsampling, and offers `closed` / `label` / `origin` / `offset` parameters to control bucket edges. Internally it can be expressed via `pd.Grouper(freq=...)`, which is what you reach for when combining time bucketing with other group keys.

**Q13. What is the right way to update a subset of rows in a DataFrame?**

Always assign through a single `loc` operation against the original frame:

```python
df.loc[df['x'] > 0, 'y'] = 0
df.loc[df['name'] == 'Alice', ['salary', 'bonus']] = [100_000, 5_000]
```

Avoid chained indexing (`df[mask][col] = value`), which under Pandas < 3.0 may silently mutate a copy and not the original; under CoW it raises `ChainedAssignmentError`.

**Q14. How would you optimize the memory of a 10-GB CSV?**

Step 1: read in chunks (`chunksize=`), or read once with `dtype=` hints to avoid the inference pass. Step 2: convert string columns to `string[pyarrow]` (often 5-10x smaller). Step 3: convert low-cardinality strings to `category` (often >95% smaller). Step 4: downcast numerics with `pd.to_numeric(..., downcast='integer')` / `'unsigned'` / `'float'`. Step 5: consider switching to Parquet with compression (`snappy` / `zstd`) -- both for storage and for `dtype_backend='pyarrow'` on read. Step 6: if the frame still doesn't fit, switch to Polars (lazy) or DuckDB.

**Q15. When would you prefer Polars or DuckDB over Pandas?**

Polars: large single-node workloads dominated by `groupby` / `join` / `filter` / `sort`; new projects where API breakage isn't a concern; pipelines that benefit from lazy execution and query-plan optimization. DuckDB: when you'd rather express the transformation in SQL; need fast joins on multi-million-row tables in-process; want to query Parquet without loading it. Both interoperate with Pandas (`pl.from_pandas` / `df.to_pandas`, `duckdb.sql(...).df()`), so they can be added incrementally for hot paths instead of as a wholesale migration.

---

*End of Pandas reference. This guide is designed as a comprehensive companion to the **Python Fundamentals**, **Python Libraries** (NumPy + PyQt sections), **DSA Fundamentals**, **LeetCode Patterns**, and **CS Fundamentals** guides.*








