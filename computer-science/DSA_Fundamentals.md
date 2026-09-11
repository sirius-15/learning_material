# Data Structures & Algorithms -- Comprehensive Reference

> A foundational reference covering every major data structure and algorithm. Each topic includes internal mechanics, operation complexities, implementations in **Python** and **C++**, use cases, tradeoffs, and key interview problems. Complements the pattern-focused *LeetCode Patterns* guide.

---

## Table of Contents

### Part 1: Data Structures

1. [Arrays and Dynamic Arrays](#1-arrays-and-dynamic-arrays)
2. [Linked Lists](#2-linked-lists)
3. [Stacks](#3-stacks)
4. [Queues](#4-queues)
5. [Hash Tables](#5-hash-tables)
6. [Trees (Binary Trees & BSTs)](#6-trees-binary-trees--bsts)
7. [Balanced BSTs (AVL & Red-Black Trees)](#7-balanced-bsts-avl--red-black-trees)
8. [Heaps](#8-heaps)
9. [Graphs](#9-graphs)
10. [Tries (Prefix Trees)](#10-tries-prefix-trees)
11. [Segment Trees](#11-segment-trees)
12. [Fenwick Trees (Binary Indexed Trees)](#12-fenwick-trees-binary-indexed-trees)
13. [Disjoint Set Union (Union-Find)](#13-disjoint-set-union-union-find)

### Part 2: Algorithms

14. [Sorting Algorithms](#14-sorting-algorithms)
15. [Searching Algorithms](#15-searching-algorithms)
16. [Graph Traversals](#16-graph-traversals)
17. [Shortest Path Algorithms](#17-shortest-path-algorithms)
18. [Minimum Spanning Tree](#18-minimum-spanning-tree)
19. [String Algorithms](#19-string-algorithms)
20. [Dynamic Programming](#20-dynamic-programming)
21. [Divide and Conquer](#21-divide-and-conquer)
22. [Greedy Algorithms](#22-greedy-algorithms)
23. [Backtracking](#23-backtracking)
24. [Bit Manipulation](#24-bit-manipulation)

### Part 3: Reference Tables

25. [Master Complexity Cheat Sheet](#25-master-complexity-cheat-sheet)
26. [Which Data Structure Should I Use?](#26-which-data-structure-should-i-use)
27. [Space-Time Tradeoff Summary](#27-space-time-tradeoff-summary)

---

# Part 1: Data Structures

---

## 1. Arrays and Dynamic Arrays

### Overview

An **array** is a contiguous block of memory storing elements of the same type. Each element is accessed via an index computed as `base_address + index * element_size`, giving O(1) random access. This contiguity also makes arrays extremely cache-friendly.

A **static array** has a fixed size determined at allocation. A **dynamic array** (Python `list`, C++ `std::vector`) automatically grows when capacity is exceeded -- typically by doubling -- giving O(1) *amortized* appends despite occasional O(n) copy operations.

**Memory layout:**

```
Index:    0     1     2     3     4     5     6     7
        ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
Memory: │  10 │  20 │  30 │  40 │  50 │     │     │     │
        └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘
        size = 5                        capacity = 8
```

### Operations & Complexity

| Operation | Static Array | Dynamic Array (Amortized) | Notes |
|---|---|---|---|
| Access by index | O(1) | O(1) | Direct address calculation |
| Search (unsorted) | O(n) | O(n) | Linear scan |
| Search (sorted) | O(log n) | O(log n) | Binary search |
| Insert at end | N/A | **O(1) amortized** | Occasional O(n) resize |
| Insert at index i | O(n) | O(n) | Shift elements right |
| Delete at end | N/A | O(1) | Decrement size |
| Delete at index i | O(n) | O(n) | Shift elements left |
| Space | O(n) | O(n) | Up to 2n due to capacity |

### How Dynamic Array Resizing Works

When a dynamic array is full (size == capacity):
1. Allocate a new array of `2 * capacity`
2. Copy all existing elements to the new array
3. Free the old array
4. Insert the new element

Although a single resize costs O(n), it happens so rarely that across n insertions the total cost is O(n), giving **O(1) amortized** per insertion. The proof uses the **banker's method**: each insertion "pays" 3 units -- 1 for itself, 1 to copy itself later, and 1 to copy an element that was already present before the last resize.

### Implementation

**Python** -- Dynamic array from scratch:

```python
class DynamicArray:
    def __init__(self):
        self._capacity = 1
        self._size = 0
        self._data = [None] * self._capacity

    def __len__(self):
        return self._size

    def __getitem__(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("Index out of bounds")
        return self._data[index]

    def append(self, value):
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        self._data[self._size] = value
        self._size += 1

    def insert(self, index, value):
        if index < 0 or index > self._size:
            raise IndexError("Index out of bounds")
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]
        self._data[index] = value
        self._size += 1

    def delete(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("Index out of bounds")
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]
        self._data[self._size - 1] = None
        self._size -= 1
        if self._size > 0 and self._size == self._capacity // 4:
            self._resize(self._capacity // 2)

    def _resize(self, new_capacity):
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_capacity
```

**C++** -- Dynamic array from scratch:

```cpp
#include <stdexcept>

template <typename T>
class DynamicArray {
    T* data;
    int sz;
    int cap;

    void resize(int new_cap) {
        T* new_data = new T[new_cap];
        for (int i = 0; i < sz; i++)
            new_data[i] = data[i];
        delete[] data;
        data = new_data;
        cap = new_cap;
    }

public:
    DynamicArray() : sz(0), cap(1) { data = new T[cap]; }
    ~DynamicArray() { delete[] data; }

    int size() const { return sz; }

    T& operator[](int index) {
        if (index < 0 || index >= sz)
            throw std::out_of_range("Index out of bounds");
        return data[index];
    }

    void push_back(const T& value) {
        if (sz == cap) resize(2 * cap);
        data[sz++] = value;
    }

    void insert(int index, const T& value) {
        if (index < 0 || index > sz)
            throw std::out_of_range("Index out of bounds");
        if (sz == cap) resize(2 * cap);
        for (int i = sz; i > index; i--)
            data[i] = data[i - 1];
        data[index] = value;
        sz++;
    }

    void erase(int index) {
        if (index < 0 || index >= sz)
            throw std::out_of_range("Index out of bounds");
        for (int i = index; i < sz - 1; i++)
            data[i] = data[i + 1];
        sz--;
        if (sz > 0 && sz == cap / 4) resize(cap / 2);
    }
};
```

### Use Cases

- **Default choice** when you need indexed access and mostly append/read
- Storing collections where order matters and size is roughly known
- Building blocks for other structures (heaps, hash tables, stacks, queues)
- Matrix/grid representations (2D arrays)

### Tradeoffs

| Advantage | Disadvantage |
|---|---|
| O(1) random access | O(n) insert/delete in the middle |
| Cache-friendly (contiguous memory) | Wasted space when capacity >> size |
| Simple and efficient | Fixed-size arrays can't grow |
| Great for iteration | Insertions shift many elements |

### Key Interview Problems

| Problem | Difficulty | Core Idea |
|---|---|---|
| Rotate Array (LC 189) | Medium | Reverse sub-sections in-place |
| Product of Array Except Self (LC 238) | Medium | Prefix and suffix products |
| Merge Sorted Array (LC 88) | Easy | Fill from the end to avoid overwrites |

---

## 2. Linked Lists

### Overview

A **linked list** is a linear collection of nodes where each node contains data and a pointer (reference) to the next node. Unlike arrays, elements are not stored contiguously -- each node can be anywhere in memory, connected by pointers.

**Variants:**

| Type | Structure | Key Difference |
|---|---|---|
| **Singly linked** | Each node has `next` | One-way traversal only |
| **Doubly linked** | Each node has `prev` and `next` | Two-way traversal |
| **Circular** | Last node points back to head | No null terminator |

**Visual:**

```
Singly:  [10|→] → [20|→] → [30|→] → [40|∅]
          head                          tail

Doubly:  ∅←[10]⇄[20]⇄[30]⇄[40]→∅
           head                tail

Circular: [10|→] → [20|→] → [30|→] → [40|→] ─┐
            ↑                                    │
            └────────────────────────────────────┘
```

### Operations & Complexity

| Operation | Singly Linked | Doubly Linked | Notes |
|---|---|---|---|
| Access by index | O(n) | O(n) | Must traverse from head |
| Search | O(n) | O(n) | Linear scan |
| Insert at head | **O(1)** | **O(1)** | Update head pointer |
| Insert at tail | O(n) / O(1)* | **O(1)** | *O(1) if tail pointer maintained |
| Insert after given node | O(1) | O(1) | Pointer manipulation |
| Delete head | **O(1)** | **O(1)** | Update head pointer |
| Delete tail | O(n) | **O(1)** | Singly: must find prev of tail |
| Delete given node | O(n) | **O(1)** | Singly: must find prev |
| Space | O(n) | O(n) | Extra pointer overhead per node |

### Implementation

**Python** -- Singly Linked List:

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def prepend(self, val):
        self.head = ListNode(val, self.head)
        self.size += 1

    def append(self, val):
        new_node = ListNode(val)
        if not self.head:
            self.head = new_node
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = new_node
        self.size += 1

    def delete(self, val):
        if not self.head:
            return False
        if self.head.val == val:
            self.head = self.head.next
            self.size -= 1
            return True
        curr = self.head
        while curr.next:
            if curr.next.val == val:
                curr.next = curr.next.next
                self.size -= 1
                return True
            curr = curr.next
        return False

    def search(self, val):
        curr = self.head
        while curr:
            if curr.val == val:
                return curr
            curr = curr.next
        return None

    def reverse(self):
        prev, curr = None, self.head
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        self.head = prev

    def to_list(self):
        result, curr = [], self.head
        while curr:
            result.append(curr.val)
            curr = curr.next
        return result
```

**Python** -- Doubly Linked List:

```python
class DListNode:
    def __init__(self, val=0, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next

class DoublyLinkedList:
    def __init__(self):
        self.head = DListNode()  # sentinel head
        self.tail = DListNode()  # sentinel tail
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def _insert_between(self, val, predecessor, successor):
        new_node = DListNode(val, predecessor, successor)
        predecessor.next = new_node
        successor.prev = new_node
        self.size += 1
        return new_node

    def _remove_node(self, node):
        predecessor = node.prev
        successor = node.next
        predecessor.next = successor
        successor.prev = predecessor
        self.size -= 1
        return node.val

    def prepend(self, val):
        return self._insert_between(val, self.head, self.head.next)

    def append(self, val):
        return self._insert_between(val, self.tail.prev, self.tail)

    def delete_first(self):
        if self.size == 0:
            raise IndexError("List is empty")
        return self._remove_node(self.head.next)

    def delete_last(self):
        if self.size == 0:
            raise IndexError("List is empty")
        return self._remove_node(self.tail.prev)
```

**C++** -- Singly Linked List:

```cpp
template <typename T>
struct ListNode {
    T val;
    ListNode* next;
    ListNode(T v, ListNode* n = nullptr) : val(v), next(n) {}
};

template <typename T>
class SinglyLinkedList {
    ListNode<T>* head;
    int sz;

public:
    SinglyLinkedList() : head(nullptr), sz(0) {}

    ~SinglyLinkedList() {
        while (head) {
            ListNode<T>* tmp = head;
            head = head->next;
            delete tmp;
        }
    }

    void prepend(T val) {
        head = new ListNode<T>(val, head);
        sz++;
    }

    void append(T val) {
        auto* node = new ListNode<T>(val);
        if (!head) { head = node; }
        else {
            auto* curr = head;
            while (curr->next) curr = curr->next;
            curr->next = node;
        }
        sz++;
    }

    bool remove(T val) {
        if (!head) return false;
        if (head->val == val) {
            auto* tmp = head;
            head = head->next;
            delete tmp;
            sz--;
            return true;
        }
        auto* curr = head;
        while (curr->next) {
            if (curr->next->val == val) {
                auto* tmp = curr->next;
                curr->next = tmp->next;
                delete tmp;
                sz--;
                return true;
            }
            curr = curr->next;
        }
        return false;
    }

    void reverse() {
        ListNode<T>* prev = nullptr;
        auto* curr = head;
        while (curr) {
            auto* nxt = curr->next;
            curr->next = prev;
            prev = curr;
            curr = nxt;
        }
        head = prev;
    }

    int size() const { return sz; }
};
```

### Use Cases

- Implementing stacks and queues with O(1) insertion/deletion
- **LRU Cache** -- doubly linked list + hash map
- Undo functionality in editors (doubly linked for forward/backward)
- Polynomial representation and arithmetic
- Memory allocation (free lists in OS memory management)

### Tradeoffs

| Advantage | Disadvantage |
|---|---|
| O(1) insertion/deletion at known position | O(n) access by index (no random access) |
| No wasted capacity (exact memory usage) | Extra memory for pointers (8 bytes each on 64-bit) |
| Easy to grow/shrink | Poor cache locality (nodes scattered in memory) |
| Natural for ordered insertion/removal | Cannot do binary search efficiently |

### Key Interview Problems

| Problem | Difficulty | Core Idea |
|---|---|---|
| Reverse Linked List (LC 206) | Easy | Three-pointer technique: prev, curr, next |
| Linked List Cycle (LC 141) | Easy | Fast and slow pointers |
| Merge Two Sorted Lists (LC 21) | Easy | Compare heads, build merged list |
| LRU Cache (LC 146) | Medium | Doubly linked list + hash map for O(1) ops |
| Reverse Nodes in k-Group (LC 25) | Hard | Reverse sublists, reconnect |

---

## 3. Stacks

### Overview

A **stack** is a Last-In-First-Out (LIFO) data structure. The last element added is the first one removed, like a stack of plates. Only the **top** element is accessible at any time.

Two primary implementations exist: **array-based** (using a dynamic array) and **linked-list-based** (pushing/popping at the head).

```
        ┌─────┐
  top → │  50 │  ← push() / pop() happen here
        ├─────┤
        │  40 │
        ├─────┤
        │  30 │
        ├─────┤
        │  20 │
        ├─────┤
        │  10 │
        └─────┘
```

### Operations & Complexity

| Operation | Time | Space | Notes |
|---|---|---|---|
| push(x) | O(1) | O(1) | Add to top |
| pop() | O(1) | O(1) | Remove from top |
| peek() / top() | O(1) | O(1) | View top without removing |
| isEmpty() | O(1) | O(1) | Check if stack is empty |
| size() | O(1) | O(1) | Return number of elements |
| Overall space | -- | O(n) | For n elements |

### Implementation

**Python** -- Array-based stack:

```python
class Stack:
    def __init__(self):
        self._data = []

    def push(self, val):
        self._data.append(val)

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._data.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)
```

**Python** -- Linked-list-based stack:

```python
class StackNode:
    def __init__(self, val, below=None):
        self.val = val
        self.below = below

class LinkedStack:
    def __init__(self):
        self._top = None
        self._size = 0

    def push(self, val):
        self._top = StackNode(val, self._top)
        self._size += 1

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        val = self._top.val
        self._top = self._top.below
        self._size -= 1
        return val

    def peek(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._top.val

    def is_empty(self):
        return self._top is None

    def size(self):
        return self._size
```

**C++** -- Array-based stack:

```cpp
#include <vector>
#include <stdexcept>

template <typename T>
class Stack {
    std::vector<T> data;

public:
    void push(const T& val) { data.push_back(val); }

    T pop() {
        if (empty()) throw std::runtime_error("Stack is empty");
        T val = data.back();
        data.pop_back();
        return val;
    }

    T& top() {
        if (empty()) throw std::runtime_error("Stack is empty");
        return data.back();
    }

    bool empty() const { return data.empty(); }
    int size() const { return data.size(); }
};
```

### Use Cases

- **Expression evaluation**: infix to postfix, postfix evaluation
- **Parentheses matching**: validate balanced brackets
- **Function call stack**: recursion management (the OS uses a stack)
- **Undo/redo**: each action pushed; undo pops from action stack
- **DFS traversal**: iterative DFS uses an explicit stack
- **Monotonic stack**: next greater/smaller element problems
- **Browser history**: back button traversal

### Tradeoffs

| Array-based | Linked-list-based |
|---|---|
| Better cache locality | No wasted capacity |
| Amortized O(1) push (occasional resize) | Guaranteed O(1) push (no resize) |
| Less memory overhead per element | Extra pointer per node |
| Standard library default (`std::stack`) | Useful when memory is fragmented |

### Key Interview Problems

| Problem | Difficulty | Core Idea |
|---|---|---|
| Valid Parentheses (LC 20) | Easy | Push openers, pop and match closers |
| Min Stack (LC 155) | Medium | Auxiliary stack tracking current minimum |
| Evaluate Reverse Polish Notation (LC 150) | Medium | Push operands, pop two on operator |
| Daily Temperatures (LC 739) | Medium | Monotonic decreasing stack |
| Largest Rectangle in Histogram (LC 84) | Hard | Monotonic increasing stack |

---

## 4. Queues

### Overview

A **queue** is a First-In-First-Out (FIFO) data structure. Elements are added at the **rear** (enqueue) and removed from the **front** (dequeue), like a line of people waiting.

**Variants:**

| Type | Description |
|---|---|
| **Simple Queue** | Basic FIFO with enqueue at rear, dequeue at front |
| **Circular Queue** | Array-based with wrap-around to avoid wasted space |
| **Deque (Double-ended)** | Insert/remove from both ends in O(1) |
| **Priority Queue** | Elements dequeued by priority, not insertion order (see Heaps) |

```
  dequeue ←  ┌────┬────┬────┬────┬────┐  ← enqueue
    front →  │ 10 │ 20 │ 30 │ 40 │ 50 │  ← rear
             └────┴────┴────┴────┴────┘
```

### Operations & Complexity

| Operation | Queue | Deque | Notes |
|---|---|---|---|
| enqueue(x) / push_back(x) | O(1) | O(1) | Add to rear |
| dequeue() / pop_front() | O(1) | O(1) | Remove from front |
| push_front(x) | N/A | O(1) | Add to front (deque only) |
| pop_back() | N/A | O(1) | Remove from rear (deque only) |
| peek_front() | O(1) | O(1) | View front element |
| peek_back() | N/A | O(1) | View rear element |
| isEmpty() | O(1) | O(1) | Check if empty |
| Overall space | O(n) | O(n) | For n elements |

### Implementation

**Python** -- Circular Queue (array-based):

```python
class CircularQueue:
    def __init__(self, capacity):
        self._data = [None] * capacity
        self._front = 0
        self._size = 0
        self._capacity = capacity

    def enqueue(self, val):
        if self._size == self._capacity:
            raise OverflowError("Queue is full")
        rear = (self._front + self._size) % self._capacity
        self._data[rear] = val
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        val = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        return val

    def peek(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._data[self._front]

    def is_empty(self):
        return self._size == 0

    def is_full(self):
        return self._size == self._capacity
```

**Python** -- Deque (doubly-linked list based):

```python
from collections import deque

# Python's collections.deque is a high-performance doubly-linked list.
# All operations below are O(1).

dq = deque()
dq.append(10)       # push_back
dq.appendleft(5)    # push_front
dq.pop()             # pop_back  → 10
dq.popleft()         # pop_front → 5
```

**C++** -- Circular Queue:

```cpp
#include <vector>
#include <stdexcept>

template <typename T>
class CircularQueue {
    std::vector<T> data;
    int front_idx, sz, cap;

public:
    CircularQueue(int capacity)
        : data(capacity), front_idx(0), sz(0), cap(capacity) {}

    void enqueue(const T& val) {
        if (sz == cap) throw std::overflow_error("Queue is full");
        int rear = (front_idx + sz) % cap;
        data[rear] = val;
        sz++;
    }

    T dequeue() {
        if (empty()) throw std::runtime_error("Queue is empty");
        T val = data[front_idx];
        front_idx = (front_idx + 1) % cap;
        sz--;
        return val;
    }

    T& front() {
        if (empty()) throw std::runtime_error("Queue is empty");
        return data[front_idx];
    }

    bool empty() const { return sz == 0; }
    bool full() const { return sz == cap; }
    int size() const { return sz; }
};
```

### Circular Queue Mechanics

A circular queue avoids the problem of "phantom full" in a naive array queue (where front moves right, leaving unusable space behind it). By wrapping indices modulo capacity, every slot is reusable.

```
Capacity = 5
After enqueue(10,20,30,40,50) and dequeue() twice:

Array:  [ _ , _ , 30, 40, 50]
         ↑              ↑
       front=2         rear wraps to index 0 for next enqueue

After enqueue(60):
Array:  [60, _ , 30, 40, 50]
              ↑   ↑
            rear  front=2
```

### Use Cases

- **BFS traversal** -- level-order traversal of trees and graphs
- **Task scheduling** -- round-robin CPU scheduling, print queues
- **Buffering** -- I/O buffers, network packet queues
- **Sliding window maximum** -- deque-based approach
- **Rate limiting** -- track request timestamps in a queue

### Tradeoffs

| Advantage | Disadvantage |
|---|---|
| O(1) enqueue/dequeue | No random access by index |
| Natural for FIFO processing | Fixed capacity (circular) or pointer overhead (linked) |
| Simple and well-understood | Not suitable for priority-based processing |
| Deque offers flexibility at both ends | Slightly more complex than stack |

### Key Interview Problems

| Problem | Difficulty | Core Idea |
|---|---|---|
| Implement Queue using Stacks (LC 232) | Easy | Two stacks simulate FIFO |
| Implement Stack using Queues (LC 225) | Easy | Two queues simulate LIFO |
| Sliding Window Maximum (LC 239) | Hard | Monotonic deque maintains max |
| Design Circular Queue (LC 622) | Medium | Array with modular arithmetic |

---

## 5. Hash Tables

### Overview

A **hash table** (hash map) stores key-value pairs and provides near-O(1) average-case access by mapping keys to array indices via a **hash function**. It is arguably the most important data structure in software engineering -- used whenever you need fast lookups, insertions, or deletions by key.

**How it works:**

1. A **hash function** `h(key)` converts the key into an integer.
2. The integer is mapped to an array index: `index = h(key) % capacity`.
3. The value is stored at that index.
4. **Collisions** (two keys mapping to the same index) are resolved using one of several strategies.

```
  key "apple"  →  h("apple") = 394  →  394 % 8 = 2  →  table[2] = ("apple", 5)
  key "banana" →  h("banana") = 710  →  710 % 8 = 6  →  table[6] = ("banana", 3)
  key "cherry" →  h("cherry") = 402  →  402 % 8 = 2  →  COLLISION with "apple"!
```

### Collision Resolution

#### 1. Separate Chaining

Each bucket holds a linked list (or another collection) of all entries that hash to that index.

```
Index 0: → ∅
Index 1: → ∅
Index 2: → ("apple",5) → ("cherry",7) → ∅
Index 3: → ∅
Index 4: → ∅
Index 5: → ∅
Index 6: → ("banana",3) → ∅
Index 7: → ∅
```

#### 2. Open Addressing

All entries are stored directly in the array. On collision, we **probe** for the next available slot.

| Probing Strategy | Formula | Pros | Cons |
|---|---|---|---|
| **Linear probing** | `(h + i) % cap` | Cache-friendly, simple | Primary clustering |
| **Quadratic probing** | `(h + i²) % cap` | Reduces primary clustering | Secondary clustering |
| **Double hashing** | `(h₁ + i·h₂) % cap` | Minimal clustering | More computation |

### Load Factor and Rehashing

- **Load factor** `α = n / capacity` (number of entries / number of buckets)
- When `α` exceeds a threshold (typically 0.7-0.75), **rehash**: allocate a larger array (usually 2x) and re-insert all entries
- Good hash tables maintain `α < 0.75` for chaining or `α < 0.7` for open addressing

### Operations & Complexity

| Operation | Average | Worst Case | Notes |
|---|---|---|---|
| put(key, val) | **O(1)** | O(n) | Worst case when all keys collide |
| get(key) | **O(1)** | O(n) | Worst case: degenerate chain |
| delete(key) | **O(1)** | O(n) | Must handle probing carefully |
| containsKey(key) | **O(1)** | O(n) | Same as get |
| Space | O(n) | O(n) | Plus overhead for buckets |

### Implementation

**Python** -- Hash table with separate chaining:

```python
class HashTable:
    def __init__(self, capacity=8):
        self._capacity = capacity
        self._size = 0
        self._buckets = [[] for _ in range(capacity)]
        self._load_factor_threshold = 0.75

    def _hash(self, key):
        return hash(key) % self._capacity

    def put(self, key, value):
        if self._size / self._capacity >= self._load_factor_threshold:
            self._rehash()
        idx = self._hash(key)
        bucket = self._buckets[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1

    def get(self, key):
        idx = self._hash(key)
        for k, v in self._buckets[idx]:
            if k == key:
                return v
        raise KeyError(key)

    def delete(self, key):
        idx = self._hash(key)
        bucket = self._buckets[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self._size -= 1
                return v
        raise KeyError(key)

    def _rehash(self):
        old_buckets = self._buckets
        self._capacity *= 2
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0
        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)

    def __len__(self):
        return self._size

    def __contains__(self, key):
        idx = self._hash(key)
        return any(k == key for k, _ in self._buckets[idx])
```

**C++** -- Hash table with separate chaining:

```cpp
#include <vector>
#include <list>
#include <stdexcept>
#include <functional>

template <typename K, typename V>
class HashTable {
    struct Entry { K key; V value; };
    std::vector<std::list<Entry>> buckets;
    int sz;
    int cap;
    double load_threshold = 0.75;

    int hash_index(const K& key) const {
        return std::hash<K>{}(key) % cap;
    }

    void rehash() {
        auto old = std::move(buckets);
        cap *= 2;
        buckets.assign(cap, std::list<Entry>());
        sz = 0;
        for (auto& chain : old)
            for (auto& entry : chain)
                put(entry.key, entry.value);
    }

public:
    HashTable(int capacity = 8)
        : cap(capacity), sz(0), buckets(capacity) {}

    void put(const K& key, const V& value) {
        if ((double)sz / cap >= load_threshold) rehash();
        int idx = hash_index(key);
        for (auto& entry : buckets[idx]) {
            if (entry.key == key) { entry.value = value; return; }
        }
        buckets[idx].push_back({key, value});
        sz++;
    }

    V& get(const K& key) {
        int idx = hash_index(key);
        for (auto& entry : buckets[idx])
            if (entry.key == key) return entry.value;
        throw std::runtime_error("Key not found");
    }

    bool contains(const K& key) const {
        int idx = hash_index(key);
        for (auto& entry : buckets[idx])
            if (entry.key == key) return true;
        return false;
    }

    bool erase(const K& key) {
        int idx = hash_index(key);
        auto& chain = buckets[idx];
        for (auto it = chain.begin(); it != chain.end(); ++it) {
            if (it->key == key) { chain.erase(it); sz--; return true; }
        }
        return false;
    }

    int size() const { return sz; }
};
```

### Hash Function Design

A good hash function must be:
- **Deterministic**: same key always produces same hash
- **Uniform**: distributes keys evenly across buckets
- **Fast**: O(1) computation for fixed-size keys

Common approaches:
- **Integers**: `h(k) = k` (identity), or multiply by a prime and shift
- **Strings**: polynomial rolling hash `h(s) = Σ s[i] * p^i mod m` (Rabin fingerprint)
- **Objects**: combine hashes of fields using XOR and prime multiplication

### Use Cases

- **Frequency counting** -- count occurrences of elements
- **Caching / memoization** -- store computed results
- **Set operations** -- fast membership testing (hash sets)
- **Indexing** -- database indices, symbol tables in compilers
- **Deduplication** -- detect duplicates in O(n)
- **Graph adjacency** -- adjacency list as `{node: [neighbors]}`

### Tradeoffs

| Advantage | Disadvantage |
|---|---|
| O(1) average-case for all operations | O(n) worst case (all keys collide) |
| Extremely versatile | No ordered iteration |
| Simple API | Hash function quality matters |
| Excellent for counting/lookup | Space overhead (load factor < 1) |
| Built into every modern language | Not cache-friendly (chaining follows pointers) |

### Key Interview Problems

| Problem | Difficulty | Core Idea |
|---|---|---|
| Two Sum (LC 1) | Easy | Map each value to its index |
| Group Anagrams (LC 49) | Medium | Sorted string or char count as key |
| Longest Consecutive Sequence (LC 128) | Medium | Hash set, expand from sequence starts |
| LRU Cache (LC 146) | Medium | Hash map + doubly linked list |
| Subarray Sum Equals K (LC 560) | Medium | Prefix sum frequency map |

---

## 6. Trees (Binary Trees & BSTs)

### Overview

A **tree** is a hierarchical data structure consisting of nodes connected by edges. Each tree has a **root** node, and every other node has exactly one parent. Nodes with no children are called **leaves**.

A **binary tree** is a tree where each node has at most two children (left and right). A **binary search tree (BST)** is a binary tree with an ordering invariant: for every node, all values in the left subtree are smaller and all values in the right subtree are larger.

```
       Binary Tree:              BST:
           1                       8
          / \                    /   \
         2   3                  3     10
        / \   \                / \      \
       4   5   6              1   6     14
                                 / \   /
                                4   7 13
```

**BST invariant**: `left.val < node.val < right.val` for every node.

### Tree Terminology

| Term | Definition |
|---|---|
| **Root** | The topmost node (no parent) |
| **Leaf** | A node with no children |
| **Height** | Longest path from node to a leaf (root height = tree height) |
| **Depth** | Distance from root to the node (root depth = 0) |
| **Level** | Set of nodes at the same depth |
| **Subtree** | A node and all its descendants |
| **Complete** | Every level fully filled except possibly the last, which fills left-to-right |
| **Full** | Every node has 0 or 2 children |
| **Perfect** | Full + complete; all leaves at same level; has 2^h+1 - 1 nodes |
| **Balanced** | Heights of left and right subtrees differ by at most 1 |

### Tree Traversals

| Traversal | Order | Use Case |
|---|---|---|
| **Inorder** (LNR) | Left → Node → Right | BST gives **sorted order** |
| **Preorder** (NLR) | Node → Left → Right | Serialize/copy tree structure |
| **Postorder** (LRN) | Left → Right → Node | Delete tree, evaluate expressions |
| **Level-order** (BFS) | Level by level | Shortest path, level sums |

### Operations & Complexity

| Operation | BST Average | BST Worst | Notes |
|---|---|---|---|
| Search | O(log n) | O(n) | Degenerate tree = linked list |
| Insert | O(log n) | O(n) | Always insert at a leaf |
| Delete | O(log n) | O(n) | Three cases (see below) |
| Find min/max | O(log n) | O(n) | Go all-left / all-right |
| Inorder traversal | O(n) | O(n) | Visit every node |
| Space | O(n) | O(n) | One node per element |

### BST Deletion -- Three Cases

1. **Leaf node**: simply remove it
2. **One child**: replace node with its child
3. **Two children**: replace with **inorder successor** (smallest in right subtree) or **inorder predecessor** (largest in left subtree), then delete that successor/predecessor

### Implementation

**Python** -- BST:

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class BST:
    def __init__(self):
        self.root = None

    def insert(self, val):
        self.root = self._insert(self.root, val)

    def _insert(self, node, val):
        if not node:
            return TreeNode(val)
        if val < node.val:
            node.left = self._insert(node.left, val)
        elif val > node.val:
            node.right = self._insert(node.right, val)
        return node

    def search(self, val):
        return self._search(self.root, val)

    def _search(self, node, val):
        if not node or node.val == val:
            return node
        if val < node.val:
            return self._search(node.left, val)
        return self._search(node.right, val)

    def delete(self, val):
        self.root = self._delete(self.root, val)

    def _delete(self, node, val):
        if not node:
            return None
        if val < node.val:
            node.left = self._delete(node.left, val)
        elif val > node.val:
            node.right = self._delete(node.right, val)
        else:
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            successor = self._find_min(node.right)
            node.val = successor.val
            node.right = self._delete(node.right, successor.val)
        return node

    def _find_min(self, node):
        while node.left:
            node = node.left
        return node

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.val)
            self._inorder(node.right, result)

    def preorder(self):
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node, result):
        if node:
            result.append(node.val)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def postorder(self):
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node, result):
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.val)

    def level_order(self):
        if not self.root:
            return []
        result, queue = [], [self.root]
        while queue:
            level = []
            next_queue = []
            for node in queue:
                level.append(node.val)
                if node.left:
                    next_queue.append(node.left)
                if node.right:
                    next_queue.append(node.right)
            result.append(level)
            queue = next_queue
        return result
```

**C++** -- BST:

```cpp
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int v) : val(v), left(nullptr), right(nullptr) {}
};

class BST {
    TreeNode* root = nullptr;

    TreeNode* insert(TreeNode* node, int val) {
        if (!node) return new TreeNode(val);
        if (val < node->val) node->left = insert(node->left, val);
        else if (val > node->val) node->right = insert(node->right, val);
        return node;
    }

    TreeNode* findMin(TreeNode* node) {
        while (node->left) node = node->left;
        return node;
    }

    TreeNode* remove(TreeNode* node, int val) {
        if (!node) return nullptr;
        if (val < node->val) node->left = remove(node->left, val);
        else if (val > node->val) node->right = remove(node->right, val);
        else {
            if (!node->left) {
                auto* tmp = node->right;
                delete node;
                return tmp;
            }
            if (!node->right) {
                auto* tmp = node->left;
                delete node;
                return tmp;
            }
            TreeNode* succ = findMin(node->right);
            node->val = succ->val;
            node->right = remove(node->right, succ->val);
        }
        return node;
    }

    void inorder(TreeNode* node, std::vector<int>& res) {
        if (!node) return;
        inorder(node->left, res);
        res.push_back(node->val);
        inorder(node->right, res);
    }

public:
    void insert(int val) { root = insert(root, val); }
    void remove(int val) { root = remove(root, val); }

    TreeNode* search(int val) {
        auto* curr = root;
        while (curr && curr->val != val)
            curr = (val < curr->val) ? curr->left : curr->right;
        return curr;
    }

    std::vector<int> inorder() {
        std::vector<int> res;
        inorder(root, res);
        return res;
    }
};
```

### Use Cases

- **BST**: ordered data with fast search, insert, delete
- **Expression trees**: represent arithmetic expressions
- **File systems**: directory structures
- **Decision trees**: machine learning classifiers
- **Syntax trees**: compiler parse trees (ASTs)

### Tradeoffs

| Advantage | Disadvantage |
|---|---|
| O(log n) operations when balanced | Degenerates to O(n) when unbalanced |
| Inorder gives sorted output | No O(1) random access |
| Flexible structure | Pointer overhead per node |
| Foundation for balanced trees | Must handle deletion carefully |

### Key Interview Problems

| Problem | Difficulty | Core Idea |
|---|---|---|
| Validate BST (LC 98) | Medium | Inorder must be strictly increasing |
| Lowest Common Ancestor of BST (LC 235) | Medium | Exploit BST ordering to branch |
| Binary Tree Level Order Traversal (LC 102) | Medium | BFS with queue |
| Serialize and Deserialize Binary Tree (LC 297) | Hard | Preorder with null markers |
| Kth Smallest Element in a BST (LC 230) | Medium | Inorder traversal, stop at k |

---

## 7. Balanced BSTs (AVL & Red-Black Trees)

### Overview

A standard BST can degenerate into a linked list (O(n) operations) if elements are inserted in sorted order. **Balanced BSTs** maintain logarithmic height through automatic restructuring after insertions and deletions.

The two most important balanced BSTs are:

| Tree | Balance Invariant | Max Height | Used By |
|---|---|---|---|
| **AVL Tree** | Height difference of left/right subtrees ≤ 1 | 1.44 log₂(n) | Databases, in-memory lookups |
| **Red-Black Tree** | Color invariant (see below) | 2 log₂(n+1) | `std::map`/`std::set` (C++), `TreeMap` (Java) |

### AVL Trees

**Balance factor** of a node = `height(left) - height(right)`. An AVL tree requires every node's balance factor to be in `{-1, 0, 1}`.

When an insertion or deletion violates this, **rotations** restore balance:

#### AVL Rotations

```
Right Rotation (LL case):       Left Rotation (RR case):
      z                              z
     / \                            / \
    y   T4      →                 T1   y
   / \                                / \
  x   T3                            T2   x
 / \                                    / \
T1  T2                                T3   T4

     becomes:                      becomes:
        y                             y
       / \                           / \
      x   z                        z   x
     / \ / \                       / \ / \
    T1 T2 T3 T4                  T1 T2 T3 T4
```

There are four cases:

| Case | Condition | Fix |
|---|---|---|
| **LL** (Left-Left) | Inserted in left subtree of left child | Right rotation |
| **RR** (Right-Right) | Inserted in right subtree of right child | Left rotation |
| **LR** (Left-Right) | Inserted in right subtree of left child | Left rotation on child, then right rotation |
| **RL** (Right-Left) | Inserted in left subtree of right child | Right rotation on child, then left rotation |

### Red-Black Trees

A Red-Black tree is a BST with the following invariants:

1. Every node is either **red** or **black**
2. The **root** is always black
3. Every **null leaf** (NIL) is black
4. If a node is **red**, both its children must be **black** (no two consecutive reds)
5. Every path from any node to its descendant NIL leaves has the **same number of black nodes** (black-height)

These properties ensure the tree height is at most `2 log₂(n+1)`.

### Operations & Complexity (Both AVL and Red-Black)

| Operation | Time | Space | Notes |
|---|---|---|---|
| Search | **O(log n)** | O(1) | Guaranteed, never O(n) |
| Insert | **O(log n)** | O(1) | Plus at most 2 rotations (AVL) or 3 recolorings + 2 rotations (RB) |
| Delete | **O(log n)** | O(1) | Plus at most 2 rotations (AVL) or 3 rotations (RB) |
| Find min/max | **O(log n)** | O(1) | Follow leftmost/rightmost |
| Inorder traversal | O(n) | O(log n) | Stack space proportional to height |
| Space | O(n) | -- | One node per element |

### Implementation

**Python** -- AVL Tree:

```python
class AVLNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def _height(self, node):
        return node.height if node else 0

    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right) if node else 0

    def _update_height(self, node):
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _rotate_right(self, z):
        y = z.left
        t3 = y.right
        y.right = z
        z.left = t3
        self._update_height(z)
        self._update_height(y)
        return y

    def _rotate_left(self, z):
        y = z.right
        t2 = y.left
        y.left = z
        z.right = t2
        self._update_height(z)
        self._update_height(y)
        return y

    def _rebalance(self, node):
        self._update_height(node)
        bf = self._balance_factor(node)

        if bf > 1:  # left-heavy
            if self._balance_factor(node.left) < 0:  # LR case
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)  # LL case

        if bf < -1:  # right-heavy
            if self._balance_factor(node.right) > 0:  # RL case
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)  # RR case

        return node

    def insert(self, root, val):
        if not root:
            return AVLNode(val)
        if val < root.val:
            root.left = self.insert(root.left, val)
        elif val > root.val:
            root.right = self.insert(root.right, val)
        else:
            return root
        return self._rebalance(root)

    def delete(self, root, val):
        if not root:
            return None
        if val < root.val:
            root.left = self.delete(root.left, val)
        elif val > root.val:
            root.right = self.delete(root.right, val)
        else:
            if not root.left:
                return root.right
            if not root.right:
                return root.left
            successor = root.right
            while successor.left:
                successor = successor.left
            root.val = successor.val
            root.right = self.delete(root.right, successor.val)
        return self._rebalance(root)

    def search(self, root, val):
        if not root or root.val == val:
            return root
        if val < root.val:
            return self.search(root.left, val)
        return self.search(root.right, val)
```

**C++** -- AVL Tree:

```cpp
struct AVLNode {
    int val, height;
    AVLNode *left, *right;
    AVLNode(int v) : val(v), height(1), left(nullptr), right(nullptr) {}
};

class AVLTree {
    int height(AVLNode* n) { return n ? n->height : 0; }

    int bf(AVLNode* n) { return n ? height(n->left) - height(n->right) : 0; }

    void updateHeight(AVLNode* n) {
        n->height = 1 + std::max(height(n->left), height(n->right));
    }

    AVLNode* rotateRight(AVLNode* z) {
        AVLNode* y = z->left;
        z->left = y->right;
        y->right = z;
        updateHeight(z);
        updateHeight(y);
        return y;
    }

    AVLNode* rotateLeft(AVLNode* z) {
        AVLNode* y = z->right;
        z->right = y->left;
        y->left = z;
        updateHeight(z);
        updateHeight(y);
        return y;
    }

    AVLNode* rebalance(AVLNode* node) {
        updateHeight(node);
        int b = bf(node);
        if (b > 1) {
            if (bf(node->left) < 0) node->left = rotateLeft(node->left);
            return rotateRight(node);
        }
        if (b < -1) {
            if (bf(node->right) > 0) node->right = rotateRight(node->right);
            return rotateLeft(node);
        }
        return node;
    }

public:
    AVLNode* insert(AVLNode* node, int val) {
        if (!node) return new AVLNode(val);
        if (val < node->val) node->left = insert(node->left, val);
        else if (val > node->val) node->right = insert(node->right, val);
        else return node;
        return rebalance(node);
    }

    AVLNode* remove(AVLNode* node, int val) {
        if (!node) return nullptr;
        if (val < node->val) node->left = remove(node->left, val);
        else if (val > node->val) node->right = remove(node->right, val);
        else {
            if (!node->left || !node->right) {
                AVLNode* child = node->left ? node->left : node->right;
                delete node;
                return child;
            }
            AVLNode* succ = node->right;
            while (succ->left) succ = succ->left;
            node->val = succ->val;
            node->right = remove(node->right, succ->val);
        }
        return rebalance(node);
    }
};
```

### AVL vs Red-Black: When to Use

| Criterion | AVL | Red-Black |
|---|---|---|
| **Search speed** | Faster (stricter balance) | Slightly slower |
| **Insertion speed** | Slower (more rotations) | Faster (fewer rotations) |
| **Deletion speed** | Slower | Faster |
| **Height** | ≤ 1.44 log n | ≤ 2 log n |
| **Best for** | Read-heavy workloads | Write-heavy workloads |
| **Used in** | Databases, in-memory indices | `std::map`, `std::set`, Linux kernel |

### Key Interview Problems

| Problem | Difficulty | Core Idea |
|---|---|---|
| Balanced Binary Tree (LC 110) | Easy | Check height difference at every node |
| Convert Sorted Array to BST (LC 108) | Easy | Choose middle as root, recurse |
| Count of Smaller Numbers After Self (LC 315) | Hard | Augmented BST or merge sort |

---

## 8. Heaps

### Overview

A **heap** is a complete binary tree that satisfies the **heap property**:

- **Min-heap**: every parent ≤ its children (root is minimum)
- **Max-heap**: every parent ≥ its children (root is maximum)

Heaps are typically implemented as **arrays** (not pointer-based trees), which makes them extremely cache-friendly and space-efficient.

**Array representation** of a complete binary tree (0-indexed):

```
         1              Index:  0  1  2  3  4  5  6
        / \             Array: [1, 3, 5, 7, 9, 8, 6]
       3   5
      / \ / \           Parent of i:       (i - 1) // 2
     7  9 8  6          Left child of i:   2*i + 1
                        Right child of i:  2*i + 2
```

### Operations & Complexity

| Operation | Time | Notes |
|---|---|---|
| find_min / find_max | **O(1)** | Root element |
| insert (push) | **O(log n)** | Add at end, sift up |
| extract_min / extract_max | **O(log n)** | Remove root, sift down |
| heapify (build heap) | **O(n)** | Bottom-up sift-down (NOT O(n log n)) |
| decrease/increase key | O(log n) | Update value, then sift up or down |
| delete arbitrary | O(log n) | Swap with last, sift up or down |
| merge two heaps | O(n) | Build new heap from combined arrays |
| Space | O(n) | Array storage, no pointers |

### Why Build Heap is O(n), not O(n log n)

Building a heap by sifting down from the last internal node to the root is O(n). Intuitively, most nodes are near the bottom and need very few sifts. Formally: `Σ (n/2^(h+1)) * h` from h=0 to log(n) converges to O(n).

### Implementation

**Python** -- Min-Heap:

```python
class MinHeap:
    def __init__(self):
        self.data = []

    def _parent(self, i):
        return (i - 1) // 2

    def _left(self, i):
        return 2 * i + 1

    def _right(self, i):
        return 2 * i + 2

    def _swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]

    def _sift_up(self, i):
        while i > 0 and self.data[i] < self.data[self._parent(i)]:
            self._swap(i, self._parent(i))
            i = self._parent(i)

    def _sift_down(self, i):
        n = len(self.data)
        while True:
            smallest = i
            left, right = self._left(i), self._right(i)
            if left < n and self.data[left] < self.data[smallest]:
                smallest = left
            if right < n and self.data[right] < self.data[smallest]:
                smallest = right
            if smallest == i:
                break
            self._swap(i, smallest)
            i = smallest

    def push(self, val):
        self.data.append(val)
        self._sift_up(len(self.data) - 1)

    def pop(self):
        if not self.data:
            raise IndexError("Heap is empty")
        self._swap(0, len(self.data) - 1)
        val = self.data.pop()
        if self.data:
            self._sift_down(0)
        return val

    def peek(self):
        if not self.data:
            raise IndexError("Heap is empty")
        return self.data[0]

    def size(self):
        return len(self.data)

    @staticmethod
    def heapify(arr):
        heap = MinHeap()
        heap.data = arr[:]
        for i in range(len(arr) // 2 - 1, -1, -1):
            heap._sift_down(i)
        return heap
```

**Python** -- Using the standard library:

```python
import heapq

nums = [5, 3, 8, 1, 9, 2]
heapq.heapify(nums)        # O(n) -- in-place min-heap
heapq.heappush(nums, 4)    # O(log n)
smallest = heapq.heappop(nums)  # O(log n) -- returns 1

# For max-heap, negate values:
max_heap = [-x for x in [5, 3, 8, 1, 9, 2]]
heapq.heapify(max_heap)
largest = -heapq.heappop(max_heap)  # returns 9

# Top K smallest:
top3 = heapq.nsmallest(3, [5, 3, 8, 1, 9, 2])  # [1, 2, 3]
```

**C++** -- Min-Heap:

```cpp
#include <vector>
#include <algorithm>
#include <stdexcept>

class MinHeap {
    std::vector<int> data;

    void siftUp(int i) {
        while (i > 0 && data[i] < data[(i - 1) / 2]) {
            std::swap(data[i], data[(i - 1) / 2]);
            i = (i - 1) / 2;
        }
    }

    void siftDown(int i) {
        int n = data.size();
        while (true) {
            int smallest = i;
            int left = 2 * i + 1, right = 2 * i + 2;
            if (left < n && data[left] < data[smallest]) smallest = left;
            if (right < n && data[right] < data[smallest]) smallest = right;
            if (smallest == i) break;
            std::swap(data[i], data[smallest]);
            i = smallest;
        }
    }

public:
    void push(int val) {
        data.push_back(val);
        siftUp(data.size() - 1);
    }

    int pop() {
        if (data.empty()) throw std::runtime_error("Heap is empty");
        int val = data[0];
        data[0] = data.back();
        data.pop_back();
        if (!data.empty()) siftDown(0);
        return val;
    }

    int top() const {
        if (data.empty()) throw std::runtime_error("Heap is empty");
        return data[0];
    }

    int size() const { return data.size(); }
    bool empty() const { return data.empty(); }
};

// Using the standard library:
// std::priority_queue<int> maxHeap;                           // max-heap (default)
// std::priority_queue<int, vector<int>, greater<int>> minHeap; // min-heap
```

### Use Cases

- **Priority queues** -- process highest/lowest priority first
- **Heap sort** -- O(n log n) in-place sorting
- **Top K elements** -- maintain heap of size K
- **Median finding** -- two heaps (max-heap for lower half, min-heap for upper half)
- **Dijkstra's algorithm** -- min-heap as priority queue
- **Merge K sorted lists** -- min-heap of K list heads
- **Event-driven simulation** -- events ordered by time

### Tradeoffs

| Advantage | Disadvantage |
|---|---|
| O(1) access to min/max | Cannot search for arbitrary elements efficiently |
| O(log n) insert and extract | Not sorted (only root is guaranteed min/max) |
| O(n) build time | Merging two heaps is O(n) |
| Array-based = cache-friendly | No efficient decrease-key without index tracking |
| Simple implementation | |

### Key Interview Problems

| Problem | Difficulty | Core Idea |
|---|---|---|
| Kth Largest Element in Array (LC 215) | Medium | Min-heap of size K |
| Find Median from Data Stream (LC 295) | Hard | Two heaps: max-heap + min-heap |
| Merge K Sorted Lists (LC 23) | Hard | Min-heap of K list heads |
| Top K Frequent Elements (LC 347) | Medium | Frequency map + heap of size K |
| Task Scheduler (LC 621) | Medium | Max-heap for greedy scheduling |

---

## 9. Graphs

### Overview

A **graph** G = (V, E) consists of a set of **vertices** (nodes) V and a set of **edges** (connections) E. Graphs model relationships: social networks, maps, dependencies, web links, circuits, and much more.

**Key classifications:**

| Property | Options |
|---|---|
| **Direction** | Undirected (edges are bidirectional) vs Directed (edges have direction) |
| **Weights** | Unweighted vs Weighted (edges carry a cost/distance) |
| **Cycles** | Acyclic (no cycles) vs Cyclic |
| **Connectivity** | Connected (path between every pair) vs Disconnected |
| **Density** | Sparse (\|E\| ≈ \|V\|) vs Dense (\|E\| ≈ \|V\|²) |
| **Special types** | DAG (directed acyclic), bipartite, tree (connected acyclic undirected) |

### Representations

#### 1. Adjacency List

Each vertex stores a list of its neighbors. Best for **sparse** graphs.

```
0: [1, 2]           0 --- 1
1: [0, 2, 3]        |   / |
2: [0, 1]           | /   |
3: [1]              2     3
```

#### 2. Adjacency Matrix

A 2D matrix where `matrix[i][j] = 1` (or weight) if edge (i, j) exists. Best for **dense** graphs.

```
    0  1  2  3
0 [ 0, 1, 1, 0 ]
1 [ 1, 0, 1, 1 ]
2 [ 1, 1, 0, 0 ]
3 [ 0, 1, 0, 0 ]
```

#### 3. Edge List

A list of all edges as (u, v, weight) tuples. Used by Kruskal's algorithm.

```
[(0,1), (0,2), (1,2), (1,3)]
```

### Representation Comparison

| Operation | Adjacency List | Adjacency Matrix | Edge List |
|---|---|---|---|
| Space | O(V + E) | O(V²) | O(E) |
| Check if edge exists | O(degree) | **O(1)** | O(E) |
| Get all neighbors | **O(degree)** | O(V) | O(E) |
| Add edge | O(1) | O(1) | O(1) |
| Remove edge | O(degree) | O(1) | O(E) |
| Best for | Sparse graphs | Dense graphs | Kruskal's MST |

### Implementation

**Python** -- Graph with adjacency list:

```python
from collections import defaultdict

class Graph:
    def __init__(self, directed=False):
        self.adj = defaultdict(list)
        self.directed = directed

    def add_edge(self, u, v, weight=1):
        self.adj[u].append((v, weight))
        if not self.directed:
            self.adj[v].append((u, weight))

    def remove_edge(self, u, v):
        self.adj[u] = [(node, w) for node, w in self.adj[u] if node != v]
        if not self.directed:
            self.adj[v] = [(node, w) for node, w in self.adj[v] if node != u]

    def has_edge(self, u, v):
        return any(node == v for node, _ in self.adj[u])

    def neighbors(self, u):
        return [node for node, _ in self.adj[u]]

    def vertices(self):
        return list(self.adj.keys())
```

**Python** -- Graph with adjacency matrix:

```python
class GraphMatrix:
    def __init__(self, num_vertices):
        self.n = num_vertices
        self.matrix = [[0] * num_vertices for _ in range(num_vertices)]

    def add_edge(self, u, v, weight=1):
        self.matrix[u][v] = weight
        self.matrix[v][u] = weight  # remove for directed

    def has_edge(self, u, v):
        return self.matrix[u][v] != 0

    def neighbors(self, u):
        return [v for v in range(self.n) if self.matrix[u][v] != 0]
```

**C++** -- Graph with adjacency list:

```cpp
#include <vector>
#include <unordered_map>

class Graph {
    std::unordered_map<int, std::vector<std::pair<int, int>>> adj;
    bool directed;

public:
    Graph(bool directed = false) : directed(directed) {}

    void addEdge(int u, int v, int weight = 1) {
        adj[u].push_back({v, weight});
        if (!directed) adj[v].push_back({u, weight});
    }

    const std::vector<std::pair<int, int>>& neighbors(int u) {
        return adj[u];
    }

    bool hasEdge(int u, int v) {
        for (auto& [node, w] : adj[u])
            if (node == v) return true;
        return false;
    }
};
```

### Graph Properties

| Property | How to Check | Application |
|---|---|---|
| **Connected** | BFS/DFS reaches all vertices | Network reliability |
| **Bipartite** | BFS/DFS 2-coloring succeeds | Task assignment, matching |
| **Has cycle** | DFS back edge (directed: gray node revisit) | Deadlock detection |
| **DAG** | Directed + no cycle | Topological sort, scheduling |
| **Strongly connected** | Tarjan's or Kosaraju's algorithm | Compiler optimization |

### Use Cases

- **Social networks** -- friends, followers, connections
- **Maps / navigation** -- cities as nodes, roads as edges
- **Dependencies** -- build systems, course prerequisites (DAG)
- **Web crawling** -- pages as nodes, links as edges
- **Network routing** -- routers and connections
- **Recommendation systems** -- user-item bipartite graphs

### Key Interview Problems

| Problem | Difficulty | Core Idea |
|---|---|---|
| Number of Islands (LC 200) | Medium | BFS/DFS on grid (implicit graph) |
| Clone Graph (LC 133) | Medium | BFS/DFS with hash map for visited |
| Course Schedule (LC 207) | Medium | Cycle detection in directed graph |
| Pacific Atlantic Water Flow (LC 417) | Medium | Multi-source BFS/DFS from borders |
| Word Ladder (LC 127) | Hard | BFS shortest path in implicit graph |

---

## 10. Tries (Prefix Trees)

### Overview

A **trie** (pronounced "try", from re**trie**val) is a tree-like data structure used to store strings where each node represents a character. Shared prefixes share the same path from the root, making tries extremely efficient for prefix-based operations.

```
Insert: "cat", "car", "card", "dog", "do"

          (root)
         /      \
        c        d
        |        |
        a        o
       / \       |  \
      t   r      g   ∅ ← "do" ends here
     ∅    |     ∅
          d
         ∅

∅ = end-of-word marker
```

### Operations & Complexity

| Operation | Time | Space | Notes |
|---|---|---|---|
| Insert word | O(L) | O(L) | L = length of word |
| Search word | O(L) | O(1) | Exact match |
| Search prefix | O(L) | O(1) | Check if any word has this prefix |
| Delete word | O(L) | O(1) | Remove end-marker, prune if needed |
| Autocomplete | O(L + K) | O(K) | L = prefix length, K = results |
| Space (total) | -- | O(ALPHABET × N × L) | N words of avg length L |

### Implementation

**Python** -- Trie:

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word):
        node = self._find_node(word)
        return node is not None and node.is_end

    def starts_with(self, prefix):
        return self._find_node(prefix) is not None

    def _find_node(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def delete(self, word):
        self._delete(self.root, word, 0)

    def _delete(self, node, word, depth):
        if depth == len(word):
            if not node.is_end:
                return False
            node.is_end = False
            return len(node.children) == 0
        ch = word[depth]
        if ch not in node.children:
            return False
        should_delete = self._delete(node.children[ch], word, depth + 1)
        if should_delete:
            del node.children[ch]
            return not node.is_end and len(node.children) == 0
        return False

    def autocomplete(self, prefix):
        node = self._find_node(prefix)
        if not node:
            return []
        results = []
        self._collect(node, list(prefix), results)
        return results

    def _collect(self, node, path, results):
        if node.is_end:
            results.append("".join(path))
        for ch, child in sorted(node.children.items()):
            path.append(ch)
            self._collect(child, path, results)
            path.pop()
```

**C++** -- Trie:

```cpp
#include <string>
#include <unordered_map>
#include <vector>

struct TrieNode {
    std::unordered_map<char, TrieNode*> children;
    bool is_end = false;
};

class Trie {
    TrieNode* root;

    TrieNode* findNode(const std::string& prefix) {
        auto* node = root;
        for (char ch : prefix) {
            if (node->children.find(ch) == node->children.end())
                return nullptr;
            node = node->children[ch];
        }
        return node;
    }

public:
    Trie() : root(new TrieNode()) {}

    void insert(const std::string& word) {
        auto* node = root;
        for (char ch : word) {
            if (node->children.find(ch) == node->children.end())
                node->children[ch] = new TrieNode();
            node = node->children[ch];
        }
        node->is_end = true;
    }

    bool search(const std::string& word) {
        auto* node = findNode(word);
        return node && node->is_end;
    }

    bool startsWith(const std::string& prefix) {
        return findNode(prefix) != nullptr;
    }
};
```

### Trie Variants

| Variant | Description | Use Case |
|---|---|---|
| **Compressed Trie (Radix Tree)** | Merge chains of single-child nodes into one | Reduce space for sparse tries |
| **Suffix Trie / Suffix Tree** | Trie of all suffixes of a string | Substring search, pattern matching |
| **Ternary Search Tree** | 3 children per node (less, equal, greater) | Space-efficient alternative |

### Use Cases

- **Autocomplete / type-ahead** -- efficiently find all words with a prefix
- **Spell checking** -- check if word exists, suggest corrections
- **IP routing** -- longest prefix matching in network routers
- **Word games** -- Boggle, Scrabble (validate words during backtracking)
- **Dictionary lookup** -- faster than hash map for prefix queries
- **DNA sequence matching** -- alphabet = {A, C, G, T}

### Tradeoffs

| Advantage | Disadvantage |
|---|---|
| O(L) operations independent of n | High space usage (pointer per character per node) |
| Natural prefix operations | Hash map often faster for exact lookup |
| Alphabetical ordering for free | Implementation more complex than hash map |
| No hash collisions | Not cache-friendly (pointer chasing) |

### Key Interview Problems

| Problem | Difficulty | Core Idea |
|---|---|---|
| Implement Trie (LC 208) | Medium | Basic insert/search/startsWith |
| Word Search II (LC 212) | Hard | Trie + backtracking on grid |
| Design Add and Search Words (LC 211) | Medium | Trie with wildcard DFS |
| Longest Word in Dictionary (LC 720) | Medium | Trie + BFS/DFS for buildable words |

---

## 11. Segment Trees

### Overview

A **segment tree** is a binary tree used for efficient **range queries** (sum, min, max, GCD, etc.) and **point updates** on an array. Each node stores the aggregate value for a contiguous segment of the array.

For an array of n elements, the segment tree has O(n) nodes and supports both range queries and point updates in O(log n).

```
Array: [2, 1, 5, 3, 4]

Segment Tree (sum):
                [15]           range [0,4]
               /    \
           [8]       [7]      [0,2] and [3,4]
          /   \     /   \
        [3]  [5]  [3]  [4]   [0,1],[2,2],[3,3],[4,4]
       / \
     [2] [1]                  [0,0] and [1,1]
```

### Operations & Complexity

| Operation | Time | Space | Notes |
|---|---|---|---|
| Build | O(n) | O(n) | Bottom-up construction |
| Range query | **O(log n)** | O(log n) | Sum/min/max over [l, r] |
| Point update | **O(log n)** | O(1) | Change a single element |
| Range update (lazy) | **O(log n)** | O(n) | Deferred propagation |
| Space | -- | O(4n) | Array-based, 4n is safe upper bound |

### Implementation

**Python** -- Segment Tree (range sum + point update):

```python
class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        if self.n > 0:
            self._build(arr, 1, 0, self.n - 1)

    def _build(self, arr, node, start, end):
        if start == end:
            self.tree[node] = arr[start]
            return
        mid = (start + end) // 2
        self._build(arr, 2 * node, start, mid)
        self._build(arr, 2 * node + 1, mid + 1, end)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def update(self, idx, val):
        self._update(1, 0, self.n - 1, idx, val)

    def _update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = val
            return
        mid = (start + end) // 2
        if idx <= mid:
            self._update(2 * node, start, mid, idx, val)
        else:
            self._update(2 * node + 1, mid + 1, end, idx, val)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def query(self, left, right):
        return self._query(1, 0, self.n - 1, left, right)

    def _query(self, node, start, end, left, right):
        if right < start or end < left:
            return 0
        if left <= start and end <= right:
            return self.tree[node]
        mid = (start + end) // 2
        left_sum = self._query(2 * node, start, mid, left, right)
        right_sum = self._query(2 * node + 1, mid + 1, end, left, right)
        return left_sum + right_sum
```

**Python** -- Segment Tree with Lazy Propagation (range update):

```python
class LazySegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        if self.n > 0:
            self._build(arr, 1, 0, self.n - 1)

    def _build(self, arr, node, start, end):
        if start == end:
            self.tree[node] = arr[start]
            return
        mid = (start + end) // 2
        self._build(arr, 2 * node, start, mid)
        self._build(arr, 2 * node + 1, mid + 1, end)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def _push_down(self, node, start, end):
        if self.lazy[node] != 0:
            mid = (start + end) // 2
            self._apply(2 * node, start, mid, self.lazy[node])
            self._apply(2 * node + 1, mid + 1, end, self.lazy[node])
            self.lazy[node] = 0

    def _apply(self, node, start, end, val):
        self.tree[node] += val * (end - start + 1)
        self.lazy[node] += val

    def range_update(self, left, right, val):
        self._range_update(1, 0, self.n - 1, left, right, val)

    def _range_update(self, node, start, end, left, right, val):
        if right < start or end < left:
            return
        if left <= start and end <= right:
            self._apply(node, start, end, val)
            return
        self._push_down(node, start, end)
        mid = (start + end) // 2
        self._range_update(2 * node, start, mid, left, right, val)
        self._range_update(2 * node + 1, mid + 1, end, left, right, val)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def query(self, left, right):
        return self._query(1, 0, self.n - 1, left, right)

    def _query(self, node, start, end, left, right):
        if right < start or end < left:
            return 0
        if left <= start and end <= right:
            return self.tree[node]
        self._push_down(node, start, end)
        mid = (start + end) // 2
        return (self._query(2 * node, start, mid, left, right) +
                self._query(2 * node + 1, mid + 1, end, left, right))
```

**C++** -- Segment Tree:

```cpp
#include <vector>

class SegmentTree {
    std::vector<int> tree;
    int n;

    void build(const std::vector<int>& arr, int node, int start, int end) {
        if (start == end) { tree[node] = arr[start]; return; }
        int mid = (start + end) / 2;
        build(arr, 2 * node, start, mid);
        build(arr, 2 * node + 1, mid + 1, end);
        tree[node] = tree[2 * node] + tree[2 * node + 1];
    }

    void update(int node, int start, int end, int idx, int val) {
        if (start == end) { tree[node] = val; return; }
        int mid = (start + end) / 2;
        if (idx <= mid) update(2 * node, start, mid, idx, val);
        else update(2 * node + 1, mid + 1, end, idx, val);
        tree[node] = tree[2 * node] + tree[2 * node + 1];
    }

    int query(int node, int start, int end, int l, int r) {
        if (r < start || end < l) return 0;
        if (l <= start && end <= r) return tree[node];
        int mid = (start + end) / 2;
        return query(2 * node, start, mid, l, r) +
               query(2 * node + 1, mid + 1, end, l, r);
    }

public:
    SegmentTree(const std::vector<int>& arr) : n(arr.size()), tree(4 * arr.size()) {
        if (n > 0) build(arr, 1, 0, n - 1);
    }

    void update(int idx, int val) { update(1, 0, n - 1, idx, val); }
    int query(int l, int r) { return query(1, 0, n - 1, l, r); }
};
```

### Use Cases

- **Range sum / min / max queries** with updates
- **Counting inversions** in arrays
- **Rectangle union area** (coordinate compression + sweep line)
- **Interval scheduling** with dynamic updates
- **Competitive programming** -- extremely common

### Tradeoffs

| Advantage | Disadvantage |
|---|---|
| O(log n) queries and updates | More complex than simple prefix sums |
| Handles dynamic updates | 4x space overhead |
| Generalizable (sum, min, max, GCD) | Overkill for static arrays (use prefix sums) |
| Lazy propagation enables range updates | Implementation is error-prone |

### Key Interview Problems

| Problem | Difficulty | Core Idea |
|---|---|---|
| Range Sum Query - Mutable (LC 307) | Medium | Basic segment tree |
| Count of Smaller Numbers After Self (LC 315) | Hard | Segment tree on value space |
| Falling Squares (LC 699) | Hard | Coordinate compression + range max |

---

## 12. Fenwick Trees (Binary Indexed Trees)

### Overview

A **Fenwick tree** (Binary Indexed Tree, BIT) is a data structure that efficiently supports **prefix sum queries** and **point updates** in O(log n). It is simpler and more space-efficient than a segment tree, but less general (primarily handles prefix sums and point updates).

The key insight is using the **lowest set bit** of the index to determine the range each position is responsible for.

```
Array:   [0, 1, 3, 2, 5, 1, 4, 3]   (1-indexed: ignore index 0)
BIT:     [0, 1, 4, 2, 10, 1, 5, 3, 29]

Index i covers the range of the last lowbit(i) elements:
  i=1 (001): covers [1,1]    → 1
  i=2 (010): covers [1,2]    → 1+3 = 4
  i=3 (011): covers [3,3]    → 2
  i=4 (100): covers [1,4]    → 1+3+2+5 = 10 (wrong, should be sum)
  ...

lowbit(i) = i & (-i)
```

### Operations & Complexity

| Operation | Time | Space | Notes |
|---|---|---|---|
| Build | O(n) | O(n) | Initialize from array |
| Point update | **O(log n)** | O(1) | Add delta to index |
| Prefix sum query | **O(log n)** | O(1) | Sum of [1..i] |
| Range sum query | **O(log n)** | O(1) | prefix(r) - prefix(l-1) |
| Space | -- | O(n) | Just one array |

### Implementation

**Python** -- Fenwick Tree:

```python
class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)  # 1-indexed

    @classmethod
    def from_array(cls, arr):
        bit = cls(len(arr))
        for i, val in enumerate(arr):
            bit.update(i + 1, val)  # 1-indexed
        return bit

    def update(self, i, delta):
        """Add delta to index i (1-indexed)."""
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)

    def prefix_sum(self, i):
        """Sum of elements [1..i] (1-indexed)."""
        total = 0
        while i > 0:
            total += self.tree[i]
            i -= i & (-i)
        return total

    def range_sum(self, left, right):
        """Sum of elements [left..right] (1-indexed)."""
        return self.prefix_sum(right) - self.prefix_sum(left - 1)
```

**C++** -- Fenwick Tree:

```cpp
#include <vector>

class FenwickTree {
    std::vector<int> tree;
    int n;

public:
    FenwickTree(int n) : n(n), tree(n + 1, 0) {}

    void update(int i, int delta) {
        for (; i <= n; i += i & (-i))
            tree[i] += delta;
    }

    int prefixSum(int i) {
        int sum = 0;
        for (; i > 0; i -= i & (-i))
            sum += tree[i];
        return sum;
    }

    int rangeSum(int l, int r) {
        return prefixSum(r) - prefixSum(l - 1);
    }
};
```

### How the Index Arithmetic Works

The operation `i & (-i)` extracts the **lowest set bit** of i:

| i (decimal) | i (binary) | i & (-i) | Range covered |
|---|---|---|---|
| 1 | 0001 | 1 | [1, 1] |
| 2 | 0010 | 2 | [1, 2] |
| 3 | 0011 | 1 | [3, 3] |
| 4 | 0100 | 4 | [1, 4] |
| 5 | 0101 | 1 | [5, 5] |
| 6 | 0110 | 2 | [5, 6] |
| 7 | 0111 | 1 | [7, 7] |
| 8 | 1000 | 8 | [1, 8] |

- **Query** (prefix sum): walk *down* by removing the lowest set bit: `i -= i & (-i)`
- **Update**: walk *up* by adding the lowest set bit: `i += i & (-i)`

### Fenwick Tree vs Segment Tree

| Criterion | Fenwick Tree | Segment Tree |
|---|---|---|
| **Space** | O(n) | O(4n) |
| **Code complexity** | ~15 lines | ~50+ lines |
| **Prefix queries** | Natural | Requires adaptation |
| **Range queries** | Sum only (via prefix difference) | Any associative operation |
| **Range updates** | Possible (with two BITs) | Natural with lazy propagation |
| **Constant factor** | Smaller (faster in practice) | Larger |

### Use Cases

- **Prefix sums with updates** -- the primary use case
- **Counting inversions** -- how many pairs are out of order
- **Coordinate compression + counting** -- count elements in ranges
- **2D prefix sums with updates** -- extend to 2D BIT

### Key Interview Problems

| Problem | Difficulty | Core Idea |
|---|---|---|
| Range Sum Query - Mutable (LC 307) | Medium | BIT as alternative to segment tree |
| Count of Smaller Numbers After Self (LC 315) | Hard | BIT on value range, process right to left |
| Reverse Pairs (LC 493) | Hard | BIT + coordinate compression |

---

## 13. Disjoint Set Union (Union-Find)

### Overview

**Union-Find** (Disjoint Set Union, DSU) manages a collection of non-overlapping sets and supports two operations efficiently:

- **Find(x)**: determine which set element x belongs to (returns the root/representative)
- **Union(x, y)**: merge the sets containing x and y

With **path compression** and **union by rank**, both operations run in **O(α(n))** amortized time, where α is the inverse Ackermann function -- effectively O(1) for all practical inputs (α(n) ≤ 4 for n ≤ 10^80).

```
Initially:  {0}, {1}, {2}, {3}, {4}

Union(0,1): {0,1}, {2}, {3}, {4}
Union(2,3): {0,1}, {2,3}, {4}
Union(1,3): {0,1,2,3}, {4}

Find(2) → root of {0,1,2,3}
```

### Operations & Complexity

| Operation | Time (Amortized) | Notes |
|---|---|---|
| MakeSet(x) | O(1) | Initialize element as its own set |
| Find(x) | **O(α(n))** | With path compression |
| Union(x, y) | **O(α(n))** | With union by rank/size |
| Connected(x, y) | **O(α(n))** | Find(x) == Find(y) |
| Space | O(n) | Two arrays: parent and rank |

### Path Compression

When calling Find(x), make every node on the path point directly to the root:

```
Before Find(4):     After Find(4):
    0                   0
    |                 / | \
    1               1   2   4
    |                   |
    2                   3
    |
    3
    |
    4
```

### Union by Rank

Always attach the shorter tree under the root of the taller tree. This keeps the tree height logarithmic.

### Implementation

**Python** -- Union-Find:

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n  # number of connected components

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x, y):
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y:
            return False
        # union by rank
        if self.rank[root_x] < self.rank[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_y] = root_x
        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_x] += 1
        self.count -= 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)

    def components(self):
        return self.count
```

**C++** -- Union-Find:

```cpp
#include <vector>
#include <numeric>

class UnionFind {
    std::vector<int> parent, rank_;
    int count;

public:
    UnionFind(int n) : parent(n), rank_(n, 0), count(n) {
        std::iota(parent.begin(), parent.end(), 0);
    }

    int find(int x) {
        if (parent[x] != x)
            parent[x] = find(parent[x]);
        return parent[x];
    }

    bool unite(int x, int y) {
        int rx = find(x), ry = find(y);
        if (rx == ry) return false;
        if (rank_[rx] < rank_[ry]) std::swap(rx, ry);
        parent[ry] = rx;
        if (rank_[rx] == rank_[ry]) rank_[rx]++;
        count--;
        return true;
    }

    bool connected(int x, int y) { return find(x) == find(y); }
    int components() const { return count; }
};
```

### Union by Size (Alternative to Rank)

Instead of rank, track the **size** of each tree. Always merge the smaller tree into the larger one. This gives the same asymptotic complexity and is sometimes more useful (e.g., when you need component sizes).

```python
class UnionFindBySize:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.size[rx] < self.size[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        self.size[rx] += self.size[ry]
        return True

    def get_size(self, x):
        return self.size[self.find(x)]
```

### Use Cases

- **Connected components** -- count or check connectivity in undirected graphs
- **Kruskal's MST** -- merge components edge by edge
- **Cycle detection** -- in undirected graphs (union returns false = cycle)
- **Network connectivity** -- dynamic "are these two nodes connected?"
- **Accounts merge** -- group items by equivalence
- **Percolation** -- physics simulation (does top connect to bottom?)

### Tradeoffs

| Advantage | Disadvantage |
|---|---|
| Nearly O(1) find and union | Cannot efficiently split sets (no un-union) |
| Simple implementation | Only answers connectivity, not path queries |
| Space-efficient (two arrays) | Not suitable for ordered/sorted operations |
| Handles dynamic connectivity | Offline only (no undo without rollback DSU) |

### Key Interview Problems

| Problem | Difficulty | Core Idea |
|---|---|---|
| Number of Connected Components (LC 323) | Medium | Union edges, count remaining components |
| Redundant Connection (LC 684) | Medium | Union edges; first edge that creates a cycle |
| Accounts Merge (LC 721) | Medium | Union emails, group by root |
| Longest Consecutive Sequence (LC 128) | Medium | Union adjacent values |
| Number of Islands II (LC 305) | Hard | Dynamic union as land is added |

---

# Part 2: Algorithms

---

## 14. Sorting Algorithms

### Overview

Sorting is the process of arranging elements in a specific order (ascending/descending). It is one of the most fundamental operations in computer science -- many algorithms require sorted input, and sorting itself is a common interview topic.

**Key properties:**

| Property | Definition |
|---|---|
| **Stable** | Preserves relative order of equal elements |
| **In-place** | Uses O(1) extra space (excluding input) |
| **Comparison-based** | Only uses comparisons between elements |
| **Adaptive** | Faster on partially sorted input |

**Theoretical lower bound**: Any comparison-based sorting algorithm requires **Ω(n log n)** comparisons in the worst case. Non-comparison sorts (counting, radix, bucket) can beat this under specific constraints.

### Comparison of All Sorting Algorithms

| Algorithm | Best | Average | Worst | Space | Stable | In-place | Notes |
|---|---|---|---|---|---|---|---|
| **Bubble Sort** | O(n) | O(n²) | O(n²) | O(1) | Yes | Yes | Adaptive with early-stop |
| **Selection Sort** | O(n²) | O(n²) | O(n²) | O(1) | No | Yes | Minimum swaps (n-1) |
| **Insertion Sort** | O(n) | O(n²) | O(n²) | O(1) | Yes | Yes | Best for small/nearly-sorted |
| **Merge Sort** | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes | No | Guaranteed performance |
| **Quick Sort** | O(n log n) | O(n log n) | O(n²) | O(log n) | No | Yes | Fastest in practice |
| **Heap Sort** | O(n log n) | O(n log n) | O(n log n) | O(1) | No | Yes | Guaranteed + in-place |
| **Counting Sort** | O(n + k) | O(n + k) | O(n + k) | O(k) | Yes | No | k = range of values |
| **Radix Sort** | O(d(n + k)) | O(d(n + k)) | O(d(n + k)) | O(n + k) | Yes | No | d = digits, k = base |
| **Bucket Sort** | O(n + k) | O(n + k) | O(n²) | O(n + k) | Yes | No | Uniform distribution |

### Bubble Sort

Repeatedly swap adjacent elements if they are in the wrong order. After each pass, the largest unsorted element "bubbles" to its correct position.

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
```

```cpp
void bubbleSort(std::vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n; i++) {
        bool swapped = false;
        for (int j = 0; j < n - 1 - i; j++) {
            if (arr[j] > arr[j + 1]) {
                std::swap(arr[j], arr[j + 1]);
                swapped = true;
            }
        }
        if (!swapped) break;
    }
}
```

### Selection Sort

Find the minimum element in the unsorted portion and swap it with the first unsorted element. Simple but always O(n²).

```python
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
```

```cpp
void selectionSort(std::vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n; i++) {
        int minIdx = i;
        for (int j = i + 1; j < n; j++)
            if (arr[j] < arr[minIdx]) minIdx = j;
        std::swap(arr[i], arr[minIdx]);
    }
}
```

### Insertion Sort

Build the sorted portion one element at a time by inserting each new element into its correct position in the already-sorted prefix. Excellent for small arrays and nearly-sorted data.

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
```

```cpp
void insertionSort(std::vector<int>& arr) {
    for (int i = 1; i < (int)arr.size(); i++) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}
```

### Merge Sort

Divide the array in half, recursively sort both halves, then merge the two sorted halves. Guaranteed O(n log n) but requires O(n) extra space.

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

```cpp
void merge(std::vector<int>& arr, int left, int mid, int right) {
    std::vector<int> L(arr.begin() + left, arr.begin() + mid + 1);
    std::vector<int> R(arr.begin() + mid + 1, arr.begin() + right + 1);
    int i = 0, j = 0, k = left;
    while (i < (int)L.size() && j < (int)R.size())
        arr[k++] = (L[i] <= R[j]) ? L[i++] : R[j++];
    while (i < (int)L.size()) arr[k++] = L[i++];
    while (j < (int)R.size()) arr[k++] = R[j++];
}

void mergeSort(std::vector<int>& arr, int left, int right) {
    if (left >= right) return;
    int mid = left + (right - left) / 2;
    mergeSort(arr, left, mid);
    mergeSort(arr, mid + 1, right);
    merge(arr, left, mid, right);
}
```

### Quick Sort

Choose a **pivot**, partition the array so elements less than the pivot go left and greater go right, then recursively sort both sides. Fastest in practice due to cache efficiency, despite O(n²) worst case (mitigated by random pivot).

```python
import random

def quick_sort(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low < high:
        pivot_idx = partition(arr, low, high)
        quick_sort(arr, low, pivot_idx - 1)
        quick_sort(arr, pivot_idx + 1, high)

def partition(arr, low, high):
    pivot_idx = random.randint(low, high)
    arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

```cpp
#include <cstdlib>

int partition(std::vector<int>& arr, int low, int high) {
    int pivotIdx = low + rand() % (high - low + 1);
    std::swap(arr[pivotIdx], arr[high]);
    int pivot = arr[high];
    int i = low - 1;
    for (int j = low; j < high; j++) {
        if (arr[j] <= pivot)
            std::swap(arr[++i], arr[j]);
    }
    std::swap(arr[i + 1], arr[high]);
    return i + 1;
}

void quickSort(std::vector<int>& arr, int low, int high) {
    if (low < high) {
        int p = partition(arr, low, high);
        quickSort(arr, low, p - 1);
        quickSort(arr, p + 1, high);
    }
}
```

### Heap Sort

Build a max-heap from the array, then repeatedly extract the maximum and place it at the end. O(n log n) guaranteed, in-place, but not stable and has poor cache behavior.

```python
def heap_sort(arr):
    n = len(arr)

    def sift_down(i, size):
        while True:
            largest = i
            left, right = 2 * i + 1, 2 * i + 2
            if left < size and arr[left] > arr[largest]:
                largest = left
            if right < size and arr[right] > arr[largest]:
                largest = right
            if largest == i:
                break
            arr[i], arr[largest] = arr[largest], arr[i]
            i = largest

    for i in range(n // 2 - 1, -1, -1):
        sift_down(i, n)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        sift_down(0, i)
```

```cpp
void heapSort(std::vector<int>& arr) {
    int n = arr.size();
    auto siftDown = [&](int i, int size) {
        while (true) {
            int largest = i, l = 2*i+1, r = 2*i+2;
            if (l < size && arr[l] > arr[largest]) largest = l;
            if (r < size && arr[r] > arr[largest]) largest = r;
            if (largest == i) break;
            std::swap(arr[i], arr[largest]);
            i = largest;
        }
    };
    for (int i = n/2 - 1; i >= 0; i--) siftDown(i, n);
    for (int i = n - 1; i > 0; i--) {
        std::swap(arr[0], arr[i]);
        siftDown(0, i);
    }
}
```

### Counting Sort

Count occurrences of each value, then reconstruct the sorted array. Only works when the range of values `k` is small.

```python
def counting_sort(arr):
    if not arr:
        return arr
    min_val, max_val = min(arr), max(arr)
    count = [0] * (max_val - min_val + 1)
    for x in arr:
        count[x - min_val] += 1
    result = []
    for i, c in enumerate(count):
        result.extend([i + min_val] * c)
    return result
```

```cpp
std::vector<int> countingSort(std::vector<int>& arr) {
    if (arr.empty()) return arr;
    int mn = *min_element(arr.begin(), arr.end());
    int mx = *max_element(arr.begin(), arr.end());
    std::vector<int> count(mx - mn + 1, 0);
    for (int x : arr) count[x - mn]++;
    std::vector<int> result;
    for (int i = 0; i < (int)count.size(); i++)
        for (int j = 0; j < count[i]; j++)
            result.push_back(i + mn);
    return result;
}
```

### Radix Sort

Sort integers digit by digit, from least significant to most significant, using a stable subroutine (typically counting sort) for each digit.

```python
def radix_sort(arr):
    if not arr:
        return arr
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        counting_sort_by_digit(arr, exp)
        exp *= 10

def counting_sort_by_digit(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    for x in arr:
        digit = (x // exp) % 10
        count[digit] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % 10
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1
    for i in range(n):
        arr[i] = output[i]
```

### Bucket Sort

Distribute elements into buckets (ranges), sort each bucket individually, then concatenate. Works best when input is **uniformly distributed**.

```python
def bucket_sort(arr):
    if not arr:
        return arr
    n = len(arr)
    min_val, max_val = min(arr), max(arr)
    if min_val == max_val:
        return arr
    bucket_range = (max_val - min_val) / n
    buckets = [[] for _ in range(n + 1)]
    for x in arr:
        idx = int((x - min_val) / bucket_range)
        buckets[idx].append(x)
    result = []
    for bucket in buckets:
        bucket.sort()  # insertion sort for small buckets
        result.extend(bucket)
    return result
```

### When to Use Which Sort

| Scenario | Best Sort | Why |
|---|---|---|
| Small array (n ≤ 50) | Insertion sort | Low overhead, adaptive |
| Nearly sorted data | Insertion sort | O(n) best case |
| Need guaranteed O(n log n) | Merge sort or Heap sort | No O(n²) worst case |
| General purpose, fastest average | Quick sort | Cache-friendly, low constant |
| Need stability | Merge sort | Stable O(n log n) |
| Integers with small range | Counting sort | O(n + k) |
| Fixed-width integers | Radix sort | O(d·n) |
| Uniform float distribution | Bucket sort | O(n) average |
| In-place + guaranteed | Heap sort | O(1) space, O(n log n) |

### Key Interview Problems

| Problem | Difficulty | Core Idea |
|---|---|---|
| Sort Colors (LC 75) | Medium | Dutch National Flag (3-way partition) |
| Kth Largest Element (LC 215) | Medium | Quickselect (partial quick sort) |
| Merge Intervals (LC 56) | Medium | Sort by start, then merge |
| Sort an Array (LC 912) | Medium | Implement merge sort or quick sort |
| Maximum Gap (LC 164) | Medium | Radix sort or bucket sort |

---

## 15. Searching Algorithms

### Overview

Searching is the process of finding a specific element or determining its presence in a data structure. The choice of algorithm depends heavily on whether the data is **sorted** and the required **time complexity**.

### Linear Search

Scan each element sequentially until found or exhausted. Works on any data, sorted or not.

**Time**: O(n) | **Space**: O(1)

```python
def linear_search(arr, target):
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1
```

```cpp
int linearSearch(const std::vector<int>& arr, int target) {
    for (int i = 0; i < (int)arr.size(); i++)
        if (arr[i] == target) return i;
    return -1;
}
```

### Binary Search

Halve the search space each step by comparing with the middle element. Requires **sorted** input.

**Time**: O(log n) | **Space**: O(1)

**Three common templates:**

#### Template 1: Basic (find exact match)

```python
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

#### Template 2: Lower bound (first element >= target)

```python
def lower_bound(arr, target):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

#### Template 3: Upper bound (first element > target)

```python
def upper_bound(arr, target):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

**C++** -- All three:

```cpp
int binarySearch(const std::vector<int>& arr, int target) {
    int lo = 0, hi = (int)arr.size() - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}

int lowerBound(const std::vector<int>& arr, int target) {
    int lo = 0, hi = (int)arr.size();
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (arr[mid] < target) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}

int upperBound(const std::vector<int>& arr, int target) {
    int lo = 0, hi = (int)arr.size();
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (arr[mid] <= target) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}

// STL: std::lower_bound(arr.begin(), arr.end(), target)
// STL: std::upper_bound(arr.begin(), arr.end(), target)
```

### Binary Search on Answer Space

Many problems don't search an array but instead binary search on the **answer** itself. If you can write a predicate `feasible(x)` that is monotonic (false...false...true...true), then binary search finds the transition point.

```python
def binary_search_on_answer(lo, hi, feasible):
    """Find the smallest x in [lo, hi] where feasible(x) is True."""
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

### Interpolation Search

Estimates the position of the target based on its value relative to the min and max of the search range. Very effective when data is **uniformly distributed**.

**Time**: O(log log n) average for uniform data, O(n) worst case | **Space**: O(1)

```python
def interpolation_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi and arr[lo] <= target <= arr[hi]:
        if arr[lo] == arr[hi]:
            return lo if arr[lo] == target else -1
        pos = lo + ((target - arr[lo]) * (hi - lo)) // (arr[hi] - arr[lo])
        if arr[pos] == target:
            return pos
        elif arr[pos] < target:
            lo = pos + 1
        else:
            hi = pos - 1
    return -1
```

### Exponential Search

Find a range where the target might be, then binary search within that range. Useful when the array is unbounded or very large.

**Time**: O(log n) | **Space**: O(1)

```python
def exponential_search(arr, target):
    if not arr:
        return -1
    if arr[0] == target:
        return 0
    bound = 1
    while bound < len(arr) and arr[bound] <= target:
        bound *= 2
    lo = bound // 2
    hi = min(bound, len(arr) - 1)
    return binary_search_range(arr, target, lo, hi)

def binary_search_range(arr, target, lo, hi):
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

### Search Algorithm Comparison

| Algorithm | Time (Avg) | Time (Worst) | Requires Sorted | Best For |
|---|---|---|---|---|
| **Linear** | O(n) | O(n) | No | Unsorted data, small arrays |
| **Binary** | O(log n) | O(log n) | Yes | General sorted data |
| **Interpolation** | O(log log n) | O(n) | Yes | Uniformly distributed data |
| **Exponential** | O(log n) | O(log n) | Yes | Unbounded/very large arrays |

### Key Interview Problems

| Problem | Difficulty | Core Idea |
|---|---|---|
| Binary Search (LC 704) | Easy | Standard binary search |
| Search in Rotated Sorted Array (LC 33) | Medium | Modified binary search with rotation |
| Find First and Last Position (LC 34) | Medium | Lower bound + upper bound |
| Search a 2D Matrix (LC 74) | Medium | Treat as flattened sorted array |
| Koko Eating Bananas (LC 875) | Medium | Binary search on answer space |
| Median of Two Sorted Arrays (LC 4) | Hard | Binary search on partition position |

---

## 16. Graph Traversals

### Overview

Graph traversals visit all vertices reachable from a source. The two fundamental strategies are **Breadth-First Search (BFS)** and **Depth-First Search (DFS)**, which differ in the order they explore vertices.

| Property | BFS | DFS |
|---|---|---|
| **Strategy** | Explore level by level (closest first) | Explore as deep as possible first |
| **Data structure** | Queue | Stack (explicit or call stack) |
| **Shortest path** | Yes (unweighted graphs) | No |
| **Space** | O(V) (width of graph) | O(V) (depth of graph) |
| **Time** | O(V + E) | O(V + E) |
| **Use case** | Shortest path, level order | Cycle detection, topological sort, connected components |

### BFS (Breadth-First Search)

Explores vertices in order of their distance from the source. Uses a **queue** (FIFO).

```
Graph:  0 -- 1 -- 3
        |    |
        2 -- 4

BFS from 0: Visit order = 0, 1, 2, 3, 4
  Level 0: {0}
  Level 1: {1, 2}
  Level 2: {3, 4}
```

**Python:**

```python
from collections import deque

def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order

def bfs_shortest_path(graph, start, end):
    """Returns shortest path in unweighted graph."""
    visited = {start}
    queue = deque([(start, [start])])

    while queue:
        node, path = queue.popleft()
        if node == end:
            return path
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None
```

**C++:**

```cpp
#include <vector>
#include <queue>
#include <unordered_set>

std::vector<int> bfs(const std::vector<std::vector<int>>& graph, int start) {
    std::vector<int> order;
    std::unordered_set<int> visited = {start};
    std::queue<int> q;
    q.push(start);

    while (!q.empty()) {
        int node = q.front(); q.pop();
        order.push_back(node);
        for (int neighbor : graph[node]) {
            if (visited.find(neighbor) == visited.end()) {
                visited.insert(neighbor);
                q.push(neighbor);
            }
        }
    }
    return order;
}
```

### DFS (Depth-First Search)

Explores as deep as possible along each branch before backtracking. Can be implemented recursively or iteratively with a stack.

```
Graph:  0 -- 1 -- 3
        |    |
        2 -- 4

DFS from 0 (one possible order): 0, 1, 3, 4, 2
```

**Python** -- Recursive and Iterative:

```python
def dfs_recursive(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    order = [start]
    for neighbor in graph[start]:
        if neighbor not in visited:
            order.extend(dfs_recursive(graph, neighbor, visited))
    return order

def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    order = []

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        for neighbor in reversed(graph[node]):
            if neighbor not in visited:
                stack.append(neighbor)
    return order
```

**C++** -- Iterative:

```cpp
std::vector<int> dfs(const std::vector<std::vector<int>>& graph, int start) {
    std::vector<int> order;
    std::unordered_set<int> visited;
    std::stack<int> stk;
    stk.push(start);

    while (!stk.empty()) {
        int node = stk.top(); stk.pop();
        if (visited.count(node)) continue;
        visited.insert(node);
        order.push_back(node);
        for (int i = graph[node].size() - 1; i >= 0; i--) {
            if (!visited.count(graph[node][i]))
                stk.push(graph[node][i]);
        }
    }
    return order;
}
```

### DFS Applications

| Application | Technique |
|---|---|
| **Cycle detection (undirected)** | Back edge to visited node (not parent) |
| **Cycle detection (directed)** | Node in current recursion stack (gray node) |
| **Topological sort** | Post-order DFS on DAG, reverse the result |
| **Connected components** | DFS/BFS from each unvisited node |
| **Strongly connected components** | Kosaraju's (two-pass DFS) or Tarjan's |
| **Bipartite check** | 2-color DFS/BFS |
| **Articulation points / bridges** | Tarjan's algorithm with discovery/low times |

### Topological Sort (Kahn's BFS-based)

For DAGs (directed acyclic graphs), topological sort produces a linear ordering where every edge (u, v) has u before v.

```python
from collections import deque

def topological_sort(graph, num_nodes):
    in_degree = [0] * num_nodes
    for u in range(num_nodes):
        for v in graph[u]:
            in_degree[v] += 1

    queue = deque([u for u in range(num_nodes) if in_degree[u] == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != num_nodes:
        return None  # cycle detected
    return order
```

### Key Interview Problems

| Problem | Difficulty | Core Idea |
|---|---|---|
| Number of Islands (LC 200) | Medium | BFS/DFS flood fill on grid |
| Clone Graph (LC 133) | Medium | BFS/DFS + hash map |
| Course Schedule (LC 207) | Medium | Topological sort / cycle detection |
| Word Ladder (LC 127) | Hard | BFS shortest path in word graph |
| Surrounded Regions (LC 130) | Medium | DFS from border O's |

---

## 17. Shortest Path Algorithms

### Overview

Shortest path algorithms find the minimum-cost path between vertices in a weighted graph. The choice of algorithm depends on graph properties:

| Algorithm | Graph Type | Negative Weights | Time | Space |
|---|---|---|---|---|
| **BFS** | Unweighted | N/A | O(V + E) | O(V) |
| **Dijkstra** | Non-negative weights | No | O((V + E) log V) | O(V) |
| **Bellman-Ford** | Any weights | Yes | O(V · E) | O(V) |
| **Floyd-Warshall** | All-pairs | Yes (no neg cycles) | O(V³) | O(V²) |
| **A*** | Non-negative + heuristic | No | O(E) best case | O(V) |

### Dijkstra's Algorithm

Finds shortest paths from a single source to all other vertices. Uses a **min-heap** (priority queue) to always process the closest unvisited vertex. Requires **non-negative** edge weights.

**How it works:**
1. Initialize distances: source = 0, all others = infinity
2. Push source into min-heap
3. Pop minimum-distance vertex, relax all its edges
4. Repeat until heap is empty

```python
import heapq

def dijkstra(graph, start, n):
    """
    graph: adjacency list {u: [(v, weight), ...]}
    Returns: distances array from start to all nodes
    """
    dist = [float('inf')] * n
    dist[start] = 0
    heap = [(0, start)]  # (distance, node)

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue  # stale entry
        for v, weight in graph[u]:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                heapq.heappush(heap, (dist[v], v))
    return dist
```

```cpp
#include <vector>
#include <queue>
#include <climits>

std::vector<int> dijkstra(
    const std::vector<std::vector<std::pair<int,int>>>& graph, int start, int n
) {
    std::vector<int> dist(n, INT_MAX);
    dist[start] = 0;
    // min-heap: (distance, node)
    std::priority_queue<std::pair<int,int>,
                        std::vector<std::pair<int,int>>,
                        std::greater<>> pq;
    pq.push({0, start});

    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;
        for (auto& [v, w] : graph[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}
```

### Bellman-Ford Algorithm

Handles **negative edge weights** and detects **negative cycles**. Relaxes all edges V-1 times.

**How it works:**
1. Initialize distances: source = 0, all others = infinity
2. Repeat V-1 times: for each edge (u, v, w), if dist[u] + w < dist[v], update dist[v]
3. One more pass: if any edge can still be relaxed, a negative cycle exists

```python
def bellman_ford(edges, start, n):
    """
    edges: list of (u, v, weight)
    Returns: (distances, has_negative_cycle)
    """
    dist = [float('inf')] * n
    dist[start] = 0

    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # check for negative cycles
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            return dist, True  # negative cycle

    return dist, False
```

```cpp
#include <vector>
#include <climits>
#include <tuple>

std::pair<std::vector<int>, bool> bellmanFord(
    const std::vector<std::tuple<int,int,int>>& edges, int start, int n
) {
    std::vector<int> dist(n, INT_MAX);
    dist[start] = 0;

    for (int i = 0; i < n - 1; i++) {
        for (auto& [u, v, w] : edges) {
            if (dist[u] != INT_MAX && dist[u] + w < dist[v])
                dist[v] = dist[u] + w;
        }
    }

    for (auto& [u, v, w] : edges) {
        if (dist[u] != INT_MAX && dist[u] + w < dist[v])
            return {dist, true};
    }
    return {dist, false};
}
```

### Floyd-Warshall Algorithm

Computes shortest paths between **all pairs** of vertices. Uses dynamic programming with V³ time.

**Recurrence**: `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])` for each intermediate vertex k.

```python
def floyd_warshall(graph_matrix, n):
    """
    graph_matrix: n×n matrix, graph_matrix[i][j] = weight (inf if no edge)
    Returns: n×n distance matrix
    """
    dist = [row[:] for row in graph_matrix]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist
```

```cpp
#include <vector>
#include <climits>

std::vector<std::vector<int>> floydWarshall(std::vector<std::vector<int>>& dist, int n) {
    for (int k = 0; k < n; k++)
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                if (dist[i][k] != INT_MAX && dist[k][j] != INT_MAX)
                    dist[i][j] = std::min(dist[i][j], dist[i][k] + dist[k][j]);
    return dist;
}
```

### A* Search Algorithm

An informed search that uses a **heuristic** function h(n) to estimate the remaining cost to the goal. Combines Dijkstra's shortest path with a heuristic to search towards the goal first.

**f(n) = g(n) + h(n)** where g(n) = actual cost from start, h(n) = estimated cost to goal.

The heuristic must be **admissible** (never overestimates) for A* to find optimal paths.

```python
import heapq

def a_star(graph, start, goal, heuristic):
    """
    heuristic(node): estimated cost from node to goal
    Returns: shortest path cost
    """
    open_set = [(heuristic(start), 0, start)]  # (f, g, node)
    g_score = {start: 0}

    while open_set:
        f, g, current = heapq.heappop(open_set)
        if current == goal:
            return g
        if g > g_score.get(current, float('inf')):
            continue
        for neighbor, weight in graph[current]:
            tentative_g = g + weight
            if tentative_g < g_score.get(neighbor, float('inf')):
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor)
                heapq.heappush(open_set, (f_score, tentative_g, neighbor))
    return float('inf')
```

### When to Use Which

| Scenario | Algorithm |
|---|---|
| Unweighted graph, shortest path | BFS |
| Non-negative weights, single source | Dijkstra |
| Negative weights possible | Bellman-Ford |
| Detect negative cycles | Bellman-Ford (Vth iteration) |
| All-pairs shortest paths, small V | Floyd-Warshall |
| Grid/map with good heuristic | A* |

### Key Interview Problems

| Problem | Difficulty | Core Idea |
|---|---|---|
| Network Delay Time (LC 743) | Medium | Dijkstra from source, return max dist |
| Cheapest Flights Within K Stops (LC 787) | Medium | Modified Bellman-Ford (K+1 iterations) |
| Path With Minimum Effort (LC 1631) | Medium | Dijkstra on grid with max-diff cost |
| Shortest Path in Binary Matrix (LC 1091) | Medium | BFS on grid |

---

## 18. Minimum Spanning Tree

### Overview

A **Minimum Spanning Tree (MST)** of a connected, undirected, weighted graph is a subset of edges that:
1. Connects all vertices (spanning)
2. Forms a tree (no cycles, exactly V-1 edges)
3. Has minimum total edge weight

Two classic algorithms: **Kruskal's** (edge-centric) and **Prim's** (vertex-centric).

| Algorithm | Approach | Time | Space | Best For |
|---|---|---|---|---|
| **Kruskal's** | Sort edges, add if no cycle (Union-Find) | O(E log E) | O(V) | Sparse graphs |
| **Prim's** | Grow tree from a vertex (min-heap) | O(E log V) | O(V) | Dense graphs |

### Kruskal's Algorithm

1. Sort all edges by weight
2. For each edge (in order), if it connects two different components, add it to MST
3. Use Union-Find to track components

```python
def kruskal(edges, n):
    """
    edges: list of (weight, u, v)
    n: number of vertices
    Returns: (MST edges, total weight)
    """
    edges.sort()
    uf = UnionFind(n)  # from section 13
    mst = []
    total_weight = 0

    for weight, u, v in edges:
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            mst.append((u, v, weight))
            total_weight += weight
            if len(mst) == n - 1:
                break
    return mst, total_weight
```

```cpp
#include <vector>
#include <algorithm>
#include <tuple>

// Uses UnionFind class from section 13
std::pair<std::vector<std::tuple<int,int,int>>, int>
kruskal(std::vector<std::tuple<int,int,int>>& edges, int n) {
    std::sort(edges.begin(), edges.end());  // sort by weight
    UnionFind uf(n);
    std::vector<std::tuple<int,int,int>> mst;
    int totalWeight = 0;

    for (auto& [w, u, v] : edges) {
        if (uf.find(u) != uf.find(v)) {
            uf.unite(u, v);
            mst.push_back({u, v, w});
            totalWeight += w;
            if ((int)mst.size() == n - 1) break;
        }
    }
    return {mst, totalWeight};
}
```

### Prim's Algorithm

1. Start from any vertex, add it to the MST set
2. Add all its edges to a min-heap
3. Pop the minimum edge; if the other endpoint is not in MST, add it
4. Repeat until all vertices are in MST

```python
import heapq

def prim(graph, n):
    """
    graph: adjacency list {u: [(v, weight), ...]}
    Returns: (MST edges, total weight)
    """
    in_mst = [False] * n
    heap = [(0, 0, -1)]  # (weight, vertex, parent)
    mst = []
    total_weight = 0

    while heap and len(mst) < n:
        weight, u, parent = heapq.heappop(heap)
        if in_mst[u]:
            continue
        in_mst[u] = True
        total_weight += weight
        if parent != -1:
            mst.append((parent, u, weight))
        for v, w in graph[u]:
            if not in_mst[v]:
                heapq.heappush(heap, (w, v, u))

    return mst, total_weight
```

```cpp
#include <vector>
#include <queue>
#include <tuple>

std::pair<std::vector<std::tuple<int,int,int>>, int>
prim(const std::vector<std::vector<std::pair<int,int>>>& graph, int n) {
    std::vector<bool> inMST(n, false);
    // min-heap: (weight, vertex, parent)
    std::priority_queue<std::tuple<int,int,int>,
                        std::vector<std::tuple<int,int,int>>,
                        std::greater<>> pq;
    pq.push({0, 0, -1});
    std::vector<std::tuple<int,int,int>> mst;
    int totalWeight = 0;

    while (!pq.empty() && (int)mst.size() < n) {
        auto [w, u, parent] = pq.top(); pq.pop();
        if (inMST[u]) continue;
        inMST[u] = true;
        totalWeight += w;
        if (parent != -1) mst.push_back({parent, u, w});
        for (auto& [v, weight] : graph[u])
            if (!inMST[v]) pq.push({weight, v, u});
    }
    return {mst, totalWeight};
}
```

### Kruskal's vs Prim's

| Criterion | Kruskal's | Prim's |
|---|---|---|
| **Approach** | Edge-centric (global sort) | Vertex-centric (grow from seed) |
| **Time** | O(E log E) | O(E log V) |
| **Best for** | Sparse graphs (E ≈ V) | Dense graphs (E ≈ V²) |
| **Data structure** | Union-Find | Min-heap |
| **Implementation** | Simpler | Slightly more complex |
| **Parallelizable** | Yes (Boruvka's variant) | Not easily |

### Key Interview Problems

| Problem | Difficulty | Core Idea |
|---|---|---|
| Min Cost to Connect All Points (LC 1584) | Medium | Prim's or Kruskal's on complete graph |
| Connecting Cities With Minimum Cost (LC 1135) | Medium | Direct MST application |
| Optimize Water Distribution (LC 1168) | Hard | Virtual node + MST |

---

## 19. String Algorithms

### Overview

String algorithms solve problems related to pattern matching, substring searching, and string manipulation. While brute-force string matching is O(n·m), specialized algorithms achieve O(n + m) by preprocessing the pattern or text.

| Algorithm | Purpose | Preprocessing | Search Time | Total |
|---|---|---|---|---|
| **Brute Force** | Pattern matching | None | O(n·m) | O(n·m) |
| **KMP** | Pattern matching | O(m) | O(n) | O(n + m) |
| **Rabin-Karp** | Pattern matching (rolling hash) | O(m) | O(n) avg, O(n·m) worst | O(n + m) avg |
| **Z-Algorithm** | All occurrences / prefix matching | O(n) | -- | O(n) |
| **Manacher's** | Longest palindromic substring | -- | O(n) | O(n) |

Where n = text length, m = pattern length.

### KMP (Knuth-Morris-Pratt)

KMP avoids redundant comparisons by precomputing a **failure function** (also called the prefix function or partial match table). When a mismatch occurs, the failure function tells us the longest proper prefix of the pattern that is also a suffix of the matched portion, allowing us to skip ahead.

**Failure function** `lps[i]` = length of the longest proper prefix of `pattern[0..i]` that is also a suffix.

```
Pattern: A B A B A C
Index:   0 1 2 3 4 5
LPS:     0 0 1 2 3 0

Explanation:
  lps[0] = 0  (single char, no proper prefix)
  lps[1] = 0  ("AB" -- no prefix = suffix)
  lps[2] = 1  ("ABA" -- "A" is both prefix and suffix)
  lps[3] = 2  ("ABAB" -- "AB" is both prefix and suffix)
  lps[4] = 3  ("ABABA" -- "ABA" is both prefix and suffix)
  lps[5] = 0  ("ABABAC" -- no prefix = suffix)
```

**Python:**

```python
def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length > 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps

def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0:
        return []
    lps = compute_lps(pattern)
    matches = []
    j = 0
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = lps[j - 1]
        if text[i] == pattern[j]:
            j += 1
        if j == m:
            matches.append(i - m + 1)
            j = lps[j - 1]
    return matches
```

**C++:**

```cpp
#include <vector>
#include <string>

std::vector<int> computeLPS(const std::string& pattern) {
    int m = pattern.size();
    std::vector<int> lps(m, 0);
    int len = 0, i = 1;
    while (i < m) {
        if (pattern[i] == pattern[len]) {
            lps[i++] = ++len;
        } else if (len > 0) {
            len = lps[len - 1];
        } else {
            lps[i++] = 0;
        }
    }
    return lps;
}

std::vector<int> kmpSearch(const std::string& text, const std::string& pattern) {
    int n = text.size(), m = pattern.size();
    std::vector<int> lps = computeLPS(pattern);
    std::vector<int> matches;
    int j = 0;
    for (int i = 0; i < n; i++) {
        while (j > 0 && text[i] != pattern[j])
            j = lps[j - 1];
        if (text[i] == pattern[j]) j++;
        if (j == m) {
            matches.push_back(i - m + 1);
            j = lps[j - 1];
        }
    }
    return matches;
}
```

### Rabin-Karp Algorithm

Uses a **rolling hash** to compare the pattern hash with substrings of the text. If hashes match, verify character by character (to handle collisions).

**Rolling hash**: `hash(s[i..i+m-1]) = Σ s[k] * p^(m-1-k) mod M`

When sliding the window, update the hash in O(1) by removing the contribution of the leftmost character and adding the new character.

```python
def rabin_karp(text, pattern):
    n, m = len(text), len(pattern)
    if m > n:
        return []
    base, mod = 256, 10**9 + 7
    pattern_hash = 0
    text_hash = 0
    highest_pow = pow(base, m - 1, mod)

    for i in range(m):
        pattern_hash = (pattern_hash * base + ord(pattern[i])) % mod
        text_hash = (text_hash * base + ord(text[i])) % mod

    matches = []
    for i in range(n - m + 1):
        if pattern_hash == text_hash:
            if text[i:i + m] == pattern:
                matches.append(i)
        if i < n - m:
            text_hash = ((text_hash - ord(text[i]) * highest_pow) * base
                         + ord(text[i + m])) % mod
    return matches
```

```cpp
std::vector<int> rabinKarp(const std::string& text, const std::string& pattern) {
    int n = text.size(), m = pattern.size();
    if (m > n) return {};
    long long base = 256, mod = 1e9 + 7;
    long long patHash = 0, txtHash = 0, highPow = 1;

    for (int i = 0; i < m - 1; i++) highPow = highPow * base % mod;
    for (int i = 0; i < m; i++) {
        patHash = (patHash * base + pattern[i]) % mod;
        txtHash = (txtHash * base + text[i]) % mod;
    }

    std::vector<int> matches;
    for (int i = 0; i <= n - m; i++) {
        if (patHash == txtHash && text.substr(i, m) == pattern)
            matches.push_back(i);
        if (i < n - m)
            txtHash = ((txtHash - text[i] * highPow % mod + mod) * base + text[i + m]) % mod;
    }
    return matches;
}
```

### Z-Algorithm

The Z-array `Z[i]` stores the length of the longest substring starting at position i that matches a prefix of the string.

To find pattern P in text T, concatenate as `P$T` ($ is a character not in P or T) and compute the Z-array. Any `Z[i] == len(P)` indicates a match at position `i - len(P) - 1` in T.

```python
def z_function(s):
    n = len(s)
    z = [0] * n
    z[0] = n
    l, r = 0, 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z

def z_search(text, pattern):
    combined = pattern + "$" + text
    z = z_function(combined)
    m = len(pattern)
    return [i - m - 1 for i in range(m + 1, len(combined)) if z[i] == m]
```

### Manacher's Algorithm

Finds the **longest palindromic substring** in O(n) by exploiting symmetry of palindromes.

The key idea: if we know palindromes centered at earlier positions, we can skip comparisons for later positions by using mirror properties.

```python
def manacher(s):
    """Returns the longest palindromic substring."""
    # Transform: "abc" → "^#a#b#c#$"
    t = "^#" + "#".join(s) + "#$"
    n = len(t)
    p = [0] * n  # p[i] = radius of palindrome centered at i
    center = right = 0

    for i in range(1, n - 1):
        mirror = 2 * center - i
        if i < right:
            p[i] = min(right - i, p[mirror])
        while t[i + p[i] + 1] == t[i - p[i] - 1]:
            p[i] += 1
        if i + p[i] > right:
            center, right = i, i + p[i]

    max_len, max_center = max((v, i) for i, v in enumerate(p))
    start = (max_center - max_len) // 2
    return s[start:start + max_len]
```

### Use Cases

| Algorithm | Use Case |
|---|---|
| **KMP** | Single pattern search, string periodicity |
| **Rabin-Karp** | Multiple pattern search, plagiarism detection |
| **Z-Algorithm** | All pattern occurrences, string period finding |
| **Manacher's** | Longest palindromic substring |

### Key Interview Problems

| Problem | Difficulty | Core Idea |
|---|---|---|
| Implement strStr (LC 28) | Easy | KMP or Rabin-Karp |
| Longest Palindromic Substring (LC 5) | Medium | Manacher's or expand-around-center |
| Repeated Substring Pattern (LC 459) | Easy | KMP failure function check |
| Shortest Palindrome (LC 214) | Hard | KMP on reverse + original |
| Longest Happy Prefix (LC 1392) | Hard | KMP prefix function / Z-function |

---

## 20. Dynamic Programming

### Overview

**Dynamic Programming (DP)** solves complex problems by breaking them into overlapping subproblems, solving each subproblem once, and storing results to avoid redundant computation. It applies when a problem has:

1. **Optimal substructure**: optimal solution can be built from optimal solutions of subproblems
2. **Overlapping subproblems**: the same subproblems are solved multiple times

**Two approaches:**

| Approach | Strategy | Direction | Data Structure |
|---|---|---|---|
| **Top-down (Memoization)** | Recursive + cache | From original problem down | Hash map / array |
| **Bottom-up (Tabulation)** | Iterative, fill table | From base cases up | Array / matrix |

### DP Problem-Solving Framework

1. **Define the state**: what information do we need to describe a subproblem?
2. **Write the recurrence**: how does the current state relate to smaller states?
3. **Identify base cases**: what are the smallest subproblems with known answers?
4. **Determine computation order**: ensure dependencies are computed first
5. **Optimize space** (optional): often only need previous row/state

### Classic DP Problems

#### Fibonacci Numbers

The simplest DP example -- each number is the sum of the two preceding ones.

```python
# Top-down (memoization)
def fib_memo(n, memo={}):
    if n <= 1:
        return n
    if n not in memo:
        memo[n] = fib_memo(n - 1) + fib_memo(n - 2)
    return memo[n]

# Bottom-up (tabulation)
def fib_tab(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]

# Space-optimized
def fib_opt(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

#### 0/1 Knapsack

Given n items with weights and values, maximize total value without exceeding capacity W.

**State**: `dp[i][w]` = max value using first i items with capacity w

**Recurrence**: `dp[i][w] = max(dp[i-1][w], dp[i-1][w - weight[i]] + value[i])`

```python
def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]  # don't take item i
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w],
                               dp[i - 1][w - weights[i - 1]] + values[i - 1])
    return dp[n][capacity]

# Space-optimized (1D array, iterate capacity backwards)
def knapsack_opt(weights, values, capacity):
    n = len(weights)
    dp = [0] * (capacity + 1)
    for i in range(n):
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    return dp[capacity]
```

```cpp
int knapsack(const std::vector<int>& weights,
             const std::vector<int>& values, int capacity) {
    int n = weights.size();
    std::vector<int> dp(capacity + 1, 0);
    for (int i = 0; i < n; i++)
        for (int w = capacity; w >= weights[i]; w--)
            dp[w] = std::max(dp[w], dp[w - weights[i]] + values[i]);
    return dp[capacity];
}
```

#### Longest Common Subsequence (LCS)

Find the longest subsequence common to two strings.

**State**: `dp[i][j]` = LCS length of `s1[0..i-1]` and `s2[0..j-1]`

**Recurrence**:
- If `s1[i-1] == s2[j-1]`: `dp[i][j] = dp[i-1][j-1] + 1`
- Else: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`

```python
def lcs(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]
```

```cpp
int lcs(const std::string& s1, const std::string& s2) {
    int m = s1.size(), n = s2.size();
    std::vector<std::vector<int>> dp(m + 1, std::vector<int>(n + 1, 0));
    for (int i = 1; i <= m; i++)
        for (int j = 1; j <= n; j++)
            dp[i][j] = (s1[i-1] == s2[j-1])
                ? dp[i-1][j-1] + 1
                : std::max(dp[i-1][j], dp[i][j-1]);
    return dp[m][n];
}
```

#### Longest Increasing Subsequence (LIS)

Find the length of the longest strictly increasing subsequence.

**O(n²) DP**: `dp[i]` = length of LIS ending at index i.

**O(n log n)** (patience sorting): maintain a sorted array of smallest tail elements.

```python
# O(n²)
def lis_dp(nums):
    n = len(nums)
    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)

# O(n log n)
import bisect
def lis_fast(nums):
    tails = []
    for x in nums:
        pos = bisect.bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    return len(tails)
```

```cpp
#include <algorithm>
int lisFast(const std::vector<int>& nums) {
    std::vector<int> tails;
    for (int x : nums) {
        auto it = std::lower_bound(tails.begin(), tails.end(), x);
        if (it == tails.end()) tails.push_back(x);
        else *it = x;
    }
    return tails.size();
}
```

#### Edit Distance (Levenshtein Distance)

Minimum operations (insert, delete, replace) to transform one string into another.

**State**: `dp[i][j]` = edit distance between `s1[0..i-1]` and `s2[0..j-1]`

```python
def edit_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],      # delete
                                   dp[i][j - 1],      # insert
                                   dp[i - 1][j - 1])  # replace
    return dp[m][n]
```

#### Coin Change

Find the minimum number of coins to make a given amount.

**State**: `dp[a]` = min coins to make amount a

**Recurrence**: `dp[a] = min(dp[a - coin] + 1)` for each coin

```python
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a and dp[a - coin] + 1 < dp[a]:
                dp[a] = dp[a - coin] + 1
    return dp[amount] if dp[amount] != float('inf') else -1
```

```cpp
int coinChange(const std::vector<int>& coins, int amount) {
    std::vector<int> dp(amount + 1, amount + 1);
    dp[0] = 0;
    for (int a = 1; a <= amount; a++)
        for (int coin : coins)
            if (coin <= a) dp[a] = std::min(dp[a], dp[a - coin] + 1);
    return dp[amount] > amount ? -1 : dp[amount];
}
```

### DP Categories

| Category | Pattern | Example Problems |
|---|---|---|
| **Linear DP** | dp[i] depends on dp[i-1], dp[i-2], ... | Fibonacci, Climbing Stairs, House Robber |
| **Grid DP** | dp[i][j] on 2D grid | Unique Paths, Min Path Sum, Dungeon Game |
| **String DP** | dp[i][j] on two strings | LCS, Edit Distance, Longest Palindromic Subseq |
| **Knapsack** | Take or skip items | 0/1 Knapsack, Coin Change, Partition Equal Subset |
| **Interval DP** | dp[i][j] on subarray [i..j] | Matrix Chain, Burst Balloons, Palindrome Partitioning |
| **Tree DP** | dp on tree structure | House Robber III, Binary Tree Max Path Sum |
| **Bitmask DP** | dp[mask] where mask is a bitmask | TSP, Shortest Superstring |
| **Digit DP** | Count numbers with property in range | Numbers with digits summing to K |

### Key Interview Problems

| Problem | Difficulty | Core Idea |
|---|---|---|
| Climbing Stairs (LC 70) | Easy | dp[i] = dp[i-1] + dp[i-2] |
| House Robber (LC 198) | Medium | Linear DP: take or skip |
| Coin Change (LC 322) | Medium | Unbounded knapsack |
| Longest Common Subsequence (LC 1143) | Medium | String DP |
| Edit Distance (LC 72) | Medium | String DP with 3 operations |
| Longest Increasing Subsequence (LC 300) | Medium | O(n log n) with patience sorting |
| Partition Equal Subset Sum (LC 416) | Medium | 0/1 knapsack variant |
| Unique Paths (LC 62) | Medium | Grid DP |
| Burst Balloons (LC 312) | Hard | Interval DP |
| Word Break (LC 139) | Medium | dp[i] = can s[0..i-1] be segmented |

---

## 21. Divide and Conquer

### Overview

**Divide and Conquer** solves problems by:
1. **Divide** the problem into smaller subproblems of the same type
2. **Conquer** each subproblem recursively (base case: trivially solvable)
3. **Combine** the subproblem solutions into the overall solution

The key difference from DP: divide-and-conquer subproblems **do not overlap** -- each subproblem is independent. This makes recursion without memoization efficient.

### Master Theorem

For recurrences of the form **T(n) = a·T(n/b) + O(n^d)**:

| Case | Condition | Result |
|---|---|---|
| **Case 1** | d < log_b(a) | T(n) = O(n^(log_b(a))) |
| **Case 2** | d = log_b(a) | T(n) = O(n^d · log n) |
| **Case 3** | d > log_b(a) | T(n) = O(n^d) |

**Examples:**
- Merge sort: T(n) = 2T(n/2) + O(n) → a=2, b=2, d=1 → Case 2 → **O(n log n)**
- Binary search: T(n) = T(n/2) + O(1) → a=1, b=2, d=0 → Case 2 → **O(log n)**
- Karatsuba multiplication: T(n) = 3T(n/2) + O(n) → a=3, b=2, d=1 → Case 1 → **O(n^1.585)**

### Classic Algorithms

#### Merge Sort

Divide array in half, sort each half, merge sorted halves.
- Time: O(n log n) | Space: O(n) | Stable: Yes

(See Section 14 for full implementation.)

#### Quick Select

Find the k-th smallest element without fully sorting. Uses the partition step of quicksort.
- Time: O(n) average, O(n²) worst | Space: O(1)

```python
import random

def quickselect(arr, k):
    """Find the k-th smallest element (0-indexed)."""
    if len(arr) == 1:
        return arr[0]

    pivot = random.choice(arr)
    lows = [x for x in arr if x < pivot]
    highs = [x for x in arr if x > pivot]
    pivots = [x for x in arr if x == pivot]

    if k < len(lows):
        return quickselect(lows, k)
    elif k < len(lows) + len(pivots):
        return pivot
    else:
        return quickselect(highs, k - len(lows) - len(pivots))
```

```cpp
int quickselect(std::vector<int>& arr, int lo, int hi, int k) {
    if (lo == hi) return arr[lo];
    int pivotIdx = lo + rand() % (hi - lo + 1);
    std::swap(arr[pivotIdx], arr[hi]);
    int pivot = arr[hi], i = lo - 1;
    for (int j = lo; j < hi; j++)
        if (arr[j] <= pivot) std::swap(arr[++i], arr[j]);
    std::swap(arr[i + 1], arr[hi]);
    int pos = i + 1;
    if (k == pos) return arr[pos];
    return (k < pos) ? quickselect(arr, lo, pos - 1, k)
                     : quickselect(arr, pos + 1, hi, k);
}
```

#### Closest Pair of Points

Find the two closest points in a 2D plane.
- Brute force: O(n²)
- Divide and conquer: **O(n log n)**

**Algorithm:**
1. Sort points by x-coordinate
2. Divide into left and right halves
3. Recursively find closest pair in each half
4. Check across the dividing line (only points within distance δ of the line)
5. The cross-strip check is O(n) because each point needs to compare with at most 7 neighbors

```python
def closest_pair(points):
    points.sort()
    return _closest(points)

def _closest(pts):
    n = len(pts)
    if n <= 3:
        return brute_force(pts)

    mid = n // 2
    mid_x = pts[mid][0]
    dl = _closest(pts[:mid])
    dr = _closest(pts[mid:])
    d = min(dl, dr)

    strip = [p for p in pts if abs(p[0] - mid_x) < d]
    strip.sort(key=lambda p: p[1])

    for i in range(len(strip)):
        j = i + 1
        while j < len(strip) and strip[j][1] - strip[i][1] < d:
            d = min(d, dist(strip[i], strip[j]))
            j += 1
    return d

def dist(p1, p2):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2) ** 0.5

def brute_force(pts):
    min_d = float('inf')
    for i in range(len(pts)):
        for j in range(i+1, len(pts)):
            min_d = min(min_d, dist(pts[i], pts[j]))
    return min_d
```

#### Maximum Subarray (Divide and Conquer approach)

Find max contiguous subarray sum by dividing in half and checking left, right, and cross sums.

```python
def max_subarray_dc(arr, lo, hi):
    if lo == hi:
        return arr[lo]
    mid = (lo + hi) // 2
    left_max = max_subarray_dc(arr, lo, mid)
    right_max = max_subarray_dc(arr, mid + 1, hi)

    # max crossing sum
    left_sum = float('-inf')
    total = 0
    for i in range(mid, lo - 1, -1):
        total += arr[i]
        left_sum = max(left_sum, total)
    right_sum = float('-inf')
    total = 0
    for i in range(mid + 1, hi + 1):
        total += arr[i]
        right_sum = max(right_sum, total)

    return max(left_max, right_max, left_sum + right_sum)
```

### Key Interview Problems

| Problem | Difficulty | Core Idea |
|---|---|---|
| Merge Sort (LC 912) | Medium | Classic divide and conquer |
| Kth Largest Element (LC 215) | Medium | Quickselect |
| Count of Range Sum (LC 327) | Hard | Merge sort with counting |
| Median of Two Sorted Arrays (LC 4) | Hard | Binary search / D&C on partition |
| Maximum Subarray (LC 53) | Medium | D&C or Kadane's |

---

## 22. Greedy Algorithms

### Overview

A **greedy algorithm** makes the **locally optimal choice** at each step, hoping to find the global optimum. Greedy works when:

1. **Greedy choice property**: a locally optimal choice leads to a globally optimal solution
2. **Optimal substructure**: optimal solution contains optimal solutions to subproblems

Greedy is often simpler and faster than DP, but only works for specific problem structures. If the greedy choice property doesn't hold, DP is needed.

### Proof Techniques

To prove a greedy algorithm is correct, use one of:

| Technique | Approach |
|---|---|
| **Exchange argument** | Show that swapping any non-greedy choice for the greedy choice doesn't worsen the solution |
| **Greedy stays ahead** | Show by induction that the greedy solution is at least as good as any other at each step |
| **Structural argument** | Show the problem structure guarantees greedy works |

### Classic Greedy Algorithms

#### Activity Selection

Given activities with start and end times, select the maximum number of non-overlapping activities.

**Greedy strategy**: always pick the activity that **finishes earliest**.

```python
def activity_selection(activities):
    """activities: list of (start, end) tuples"""
    activities.sort(key=lambda x: x[1])
    selected = [activities[0]]
    for start, end in activities[1:]:
        if start >= selected[-1][1]:
            selected.append((start, end))
    return selected
```

```cpp
std::vector<std::pair<int,int>> activitySelection(
    std::vector<std::pair<int,int>>& acts
) {
    std::sort(acts.begin(), acts.end(),
              [](auto& a, auto& b) { return a.second < b.second; });
    std::vector<std::pair<int,int>> selected = {acts[0]};
    for (int i = 1; i < (int)acts.size(); i++)
        if (acts[i].first >= selected.back().second)
            selected.push_back(acts[i]);
    return selected;
}
```

#### Huffman Coding

Build an optimal prefix-free binary code by repeatedly combining the two lowest-frequency symbols.

```python
import heapq

class HuffmanNode:
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def huffman_coding(freq_map):
    """freq_map: {'a': 5, 'b': 9, ...}"""
    heap = [HuffmanNode(ch, f) for ch, f in freq_map.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq, left, right)
        heapq.heappush(heap, merged)

    root = heap[0]
    codes = {}
    _build_codes(root, "", codes)
    return codes

def _build_codes(node, current_code, codes):
    if node.char is not None:
        codes[node.char] = current_code or "0"
        return
    if node.left:
        _build_codes(node.left, current_code + "0", codes)
    if node.right:
        _build_codes(node.right, current_code + "1", codes)
```

#### Fractional Knapsack

Unlike 0/1 knapsack (DP), items can be divided. Greedy by **value-to-weight ratio** is optimal.

```python
def fractional_knapsack(items, capacity):
    """items: list of (value, weight)"""
    items.sort(key=lambda x: x[0] / x[1], reverse=True)
    total_value = 0
    remaining = capacity
    for value, weight in items:
        if weight <= remaining:
            total_value += value
            remaining -= weight
        else:
            total_value += value * (remaining / weight)
            break
    return total_value
```

#### Jump Game

Can you reach the last index if each element is the max jump length?

```python
def can_jump(nums):
    max_reach = 0
    for i in range(len(nums)):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + nums[i])
    return True
```

### When Greedy Fails -- Use DP Instead

| Problem | Greedy Works? | Why/Why Not |
|---|---|---|
| Activity selection | Yes | Earliest finish leaves most room |
| Fractional knapsack | Yes | Best ratio first is optimal |
| 0/1 knapsack | **No** | Can't take fractions; need DP |
| Coin change (arbitrary) | **No** | Greedy may miss optimal (e.g., coins=[1,3,4], amount=6) |
| Coin change (US coins) | Yes | Special structure of US denominations |

### Key Interview Problems

| Problem | Difficulty | Core Idea |
|---|---|---|
| Jump Game (LC 55) | Medium | Track max reachable index |
| Jump Game II (LC 45) | Medium | BFS-style greedy (max reach per level) |
| Gas Station (LC 134) | Medium | If total gas ≥ total cost, start from first feasible |
| Task Scheduler (LC 621) | Medium | Schedule most frequent tasks first |
| Non-overlapping Intervals (LC 435) | Medium | Activity selection (sort by end) |
| Partition Labels (LC 763) | Medium | Greedy merge by last occurrence |

---

## 23. Backtracking

### Overview

**Backtracking** systematically explores all possible solutions by building candidates incrementally and abandoning ("backtracking") candidates that fail to satisfy constraints. It's essentially a refined brute-force that prunes the search space.

**Pattern**: Choose → Explore → Unchoose

```
                          []
                   /      |       \
                 [1]     [2]     [3]
                / \       |
             [1,2] [1,3] [2,3]
              |
           [1,2,3]
```

### General Template

```python
def backtrack(candidates, path, result, start=0):
    if is_solution(path):
        result.append(path[:])
        return

    for i in range(start, len(candidates)):
        if not is_valid(candidates[i], path):
            continue
        # choose
        path.append(candidates[i])
        # explore
        backtrack(candidates, path, result, i + 1)  # i+1 for combinations, i for reuse
        # unchoose
        path.pop()
```

```cpp
void backtrack(std::vector<int>& candidates, std::vector<int>& path,
               std::vector<std::vector<int>>& result, int start) {
    if (isSolution(path)) {
        result.push_back(path);
        return;
    }
    for (int i = start; i < (int)candidates.size(); i++) {
        if (!isValid(candidates[i], path)) continue;
        path.push_back(candidates[i]);
        backtrack(candidates, path, result, i + 1);
        path.pop_back();
    }
}
```

### Backtracking vs. Related Techniques

| Technique | Differences |
|---|---|
| **Brute force** | Tries everything; backtracking prunes invalid branches early |
| **DFS** | Backtracking is DFS on an implicit state-space tree |
| **DP** | DP stores and reuses subproblem results; backtracking explores all paths |
| **Greedy** | Greedy makes one choice; backtracking tries all choices |

### Classic Backtracking Problems

#### Subsets

Generate all subsets of a set.

```python
def subsets(nums):
    result = []
    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    backtrack(0, [])
    return result
```

#### Permutations

Generate all permutations of a set.

```python
def permutations(nums):
    result = []
    def backtrack(path, used):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path, used)
            path.pop()
            used[i] = False
    backtrack([], [False] * len(nums))
    return result
```

#### N-Queens

Place N queens on an N×N board so no two attack each other.

```python
def solve_n_queens(n):
    result = []
    cols = set()
    diag1 = set()  # row - col
    diag2 = set()  # row + col

    def backtrack(row, board):
        if row == n:
            result.append(["".join(r) for r in board])
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            board[row][col] = 'Q'

            backtrack(row + 1, board)

            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
            board[row][col] = '.'

    board = [['.' for _ in range(n)] for _ in range(n)]
    backtrack(0, board)
    return result
```

#### Sudoku Solver

```python
def solve_sudoku(board):
    def is_valid(row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        box_r, box_c = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_r, box_r + 3):
            for j in range(box_c, box_c + 3):
                if board[i][j] == num:
                    return False
        return True

    def backtrack():
        for i in range(9):
            for j in range(9):
                if board[i][j] == '.':
                    for num in '123456789':
                        if is_valid(i, j, num):
                            board[i][j] = num
                            if backtrack():
                                return True
                            board[i][j] = '.'
                    return False
        return True

    backtrack()
```

### Pruning Strategies

| Strategy | Description | Effect |
|---|---|---|
| **Constraint checking** | Skip choices violating constraints early | Avoids dead-end branches |
| **Sorting** | Sort candidates to enable early termination | Skip remaining if current too large |
| **Duplicate skipping** | Skip duplicate candidates at the same level | Avoid duplicate solutions |
| **Bound checking** | If remaining elements can't form a valid solution, prune | Reduces search space dramatically |

### Time Complexity of Backtracking

| Problem | Time | Notes |
|---|---|---|
| Subsets | O(2^n) | Each element: include or exclude |
| Permutations | O(n!) | n choices, then n-1, then n-2, ... |
| N-Queens | O(n!) | Roughly n! with pruning |
| Sudoku | O(9^(empty cells)) | Heavy pruning in practice |
| Combinations(n, k) | O(C(n,k)) | Binomial coefficient |

### Key Interview Problems

| Problem | Difficulty | Core Idea |
|---|---|---|
| Subsets (LC 78) | Medium | Backtrack: include or skip |
| Permutations (LC 46) | Medium | Backtrack with used array |
| Combination Sum (LC 39) | Medium | Backtrack with reuse (start = i, not i+1) |
| N-Queens (LC 51) | Hard | Row-by-row placement with constraint sets |
| Word Search (LC 79) | Medium | DFS/backtrack on grid |
| Palindrome Partitioning (LC 131) | Medium | Backtrack, check palindrome at each cut |
| Sudoku Solver (LC 37) | Hard | Constraint-based backtracking |

---

## 24. Bit Manipulation

### Overview

**Bit manipulation** operates directly on the binary representation of integers using bitwise operators. It enables O(1) tricks for operations that would otherwise require loops or extra space, and is fundamental for bitmask DP, flags, and low-level optimizations.

### Bitwise Operators

| Operator | Symbol | Description | Example (5=101, 3=011) |
|---|---|---|---|
| **AND** | `&` | 1 if both bits are 1 | `5 & 3 = 001 = 1` |
| **OR** | `\|` | 1 if either bit is 1 | `5 \| 3 = 111 = 7` |
| **XOR** | `^` | 1 if bits differ | `5 ^ 3 = 110 = 6` |
| **NOT** | `~` | Flip all bits | `~5 = ...11111010` |
| **Left shift** | `<<` | Shift bits left (multiply by 2) | `5 << 1 = 1010 = 10` |
| **Right shift** | `>>` | Shift bits right (divide by 2) | `5 >> 1 = 10 = 2` |

### Essential Bit Tricks

| Operation | Code | Explanation |
|---|---|---|
| Check if n is even | `n & 1 == 0` | Last bit is 0 for even |
| Check if n is power of 2 | `n > 0 and (n & (n-1)) == 0` | Powers of 2 have exactly one set bit |
| Get i-th bit | `(n >> i) & 1` | Shift right and mask |
| Set i-th bit | `n \| (1 << i)` | OR with mask |
| Clear i-th bit | `n & ~(1 << i)` | AND with inverted mask |
| Toggle i-th bit | `n ^ (1 << i)` | XOR with mask |
| Clear lowest set bit | `n & (n - 1)` | Fundamental trick |
| Isolate lowest set bit | `n & (-n)` | Used in Fenwick trees |
| Count set bits (popcount) | See below | Brian Kernighan's algorithm |
| Swap two numbers | `a ^= b; b ^= a; a ^= b` | No temp variable needed |
| Check if two ints have opposite signs | `(a ^ b) < 0` | Sign bit differs |

### Counting Set Bits (Brian Kernighan's Algorithm)

Each iteration of `n = n & (n-1)` clears the lowest set bit. The number of iterations equals the number of set bits.

```python
def count_bits(n):
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count
```

```cpp
int countBits(int n) {
    int count = 0;
    while (n) { n &= n - 1; count++; }
    return count;
    // Or use __builtin_popcount(n) in GCC
}
```

### XOR Properties

XOR is the most versatile bitwise operation for interview problems:

| Property | Formula | Implication |
|---|---|---|
| **Identity** | `a ^ 0 = a` | XOR with 0 preserves value |
| **Self-inverse** | `a ^ a = 0` | XOR with self cancels |
| **Commutative** | `a ^ b = b ^ a` | Order doesn't matter |
| **Associative** | `(a ^ b) ^ c = a ^ (b ^ c)` | Grouping doesn't matter |

**Application**: Find the single unique element in an array where every other element appears twice → XOR all elements. All pairs cancel, leaving the unique one.

```python
def single_number(nums):
    result = 0
    for n in nums:
        result ^= n
    return result
```

### Bitmask DP

Use an integer's bits to represent a subset of elements. With n elements, there are 2^n possible subsets representable as integers from 0 to 2^n - 1.

```python
# Enumerate all subsets: 0 to 2^n - 1
n = 4
for mask in range(1 << n):  # 0 to 15
    subset = []
    for i in range(n):
        if mask & (1 << i):
            subset.append(i)
    # process subset

# Enumerate all subsets of a given set (mask)
sub = mask
while sub:
    # process sub
    sub = (sub - 1) & mask
```

**Example**: Traveling Salesman Problem (TSP)

```python
def tsp(dist, n):
    """dist[i][j] = distance from city i to city j"""
    INF = float('inf')
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0  # start at city 0

    for mask in range(1 << n):
        for u in range(n):
            if dp[mask][u] == INF:
                continue
            for v in range(n):
                if mask & (1 << v):
                    continue  # already visited
                new_mask = mask | (1 << v)
                dp[new_mask][v] = min(dp[new_mask][v], dp[mask][u] + dist[u][v])

    full_mask = (1 << n) - 1
    return min(dp[full_mask][u] + dist[u][0] for u in range(n))
```

### Common Bit Manipulation Patterns

```python
# Power of two check
def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0

# Next power of two
def next_power_of_two(n):
    if n <= 1:
        return 1
    n -= 1
    n |= n >> 1
    n |= n >> 2
    n |= n >> 4
    n |= n >> 8
    n |= n >> 16
    return n + 1

# Reverse bits of a 32-bit integer
def reverse_bits(n):
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result

# Generate all subsets of size k from n elements
from itertools import combinations
def subsets_of_size_k(n, k):
    return list(combinations(range(n), k))
```

```cpp
// Power of two
bool isPowerOfTwo(int n) { return n > 0 && (n & (n - 1)) == 0; }

// Count bits
int popcount(int n) { return __builtin_popcount(n); }

// Reverse bits
uint32_t reverseBits(uint32_t n) {
    uint32_t result = 0;
    for (int i = 0; i < 32; i++) {
        result = (result << 1) | (n & 1);
        n >>= 1;
    }
    return result;
}
```

### Use Cases

- **Flags and permissions**: file permissions (rwx), feature flags
- **Subset enumeration**: bitmask DP, combinatorial optimization
- **Space optimization**: represent boolean arrays as single integers
- **Cryptography**: XOR ciphers, hash functions
- **Low-level optimization**: multiply/divide by powers of 2 using shifts
- **Error detection**: parity bits, checksums

### Key Interview Problems

| Problem | Difficulty | Core Idea |
|---|---|---|
| Single Number (LC 136) | Easy | XOR all elements; pairs cancel |
| Number of 1 Bits (LC 191) | Easy | Brian Kernighan's n &= n-1 |
| Counting Bits (LC 338) | Easy | dp[i] = dp[i & (i-1)] + 1 |
| Power of Two (LC 231) | Easy | n & (n-1) == 0 |
| Reverse Bits (LC 190) | Easy | Shift and build |
| Single Number III (LC 260) | Medium | XOR all, split by any differing bit |
| Maximum XOR of Two Numbers (LC 421) | Medium | Trie on bits, greedy from MSB |
| Subsets (LC 78) | Medium | Iterate all masks 0..2^n-1 |

---

# Part 3: Reference Tables

---

## 25. Master Complexity Cheat Sheet

### Data Structure Operations

| Data Structure | Access | Search | Insert | Delete | Space | Notes |
|---|---|---|---|---|---|---|
| **Array** | **O(1)** | O(n) | O(n) | O(n) | O(n) | O(1) access is the key advantage |
| **Dynamic Array** | **O(1)** | O(n) | O(1)* | O(n) | O(n) | *Amortized append |
| **Singly Linked List** | O(n) | O(n) | **O(1)** | **O(1)** | O(n) | Insert/delete at known position |
| **Doubly Linked List** | O(n) | O(n) | **O(1)** | **O(1)** | O(n) | O(1) delete at known node |
| **Stack** | O(n) | O(n) | **O(1)** | **O(1)** | O(n) | Push/pop at top only |
| **Queue** | O(n) | O(n) | **O(1)** | **O(1)** | O(n) | Enqueue rear, dequeue front |
| **Hash Table** | N/A | **O(1)** | **O(1)** | **O(1)** | O(n) | Average case; O(n) worst |
| **BST (balanced)** | O(log n) | **O(log n)** | **O(log n)** | **O(log n)** | O(n) | AVL / Red-Black tree |
| **BST (unbalanced)** | O(n) | O(n) | O(n) | O(n) | O(n) | Degenerates to linked list |
| **Min/Max Heap** | O(n) | O(n) | **O(log n)** | **O(log n)** | O(n) | O(1) find-min/max |
| **Trie** | O(L) | **O(L)** | **O(L)** | **O(L)** | O(A·N·L) | L = key length, A = alphabet |
| **Segment Tree** | N/A | **O(log n)** | **O(log n)** | N/A | O(n) | Range query + point update |
| **Fenwick Tree (BIT)** | N/A | **O(log n)** | **O(log n)** | N/A | O(n) | Prefix sums + point update |
| **Union-Find** | N/A | **O(α(n))** | **O(α(n))** | N/A | O(n) | α ≈ O(1) in practice |
| **Graph (adj list)** | N/A | O(V+E) | **O(1)** | O(E) | O(V+E) | Edge add is O(1) |
| **Graph (adj matrix)** | N/A | **O(1)** | **O(1)** | **O(1)** | O(V²) | Edge check is O(1) |

### Sorting Algorithms

| Algorithm | Best | Average | Worst | Space | Stable | In-place | Comparison |
|---|---|---|---|---|---|---|---|
| **Bubble Sort** | O(n) | O(n²) | O(n²) | O(1) | Yes | Yes | Yes |
| **Selection Sort** | O(n²) | O(n²) | O(n²) | O(1) | No | Yes | Yes |
| **Insertion Sort** | O(n) | O(n²) | O(n²) | O(1) | Yes | Yes | Yes |
| **Merge Sort** | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes | No | Yes |
| **Quick Sort** | O(n log n) | O(n log n) | O(n²) | O(log n) | No | Yes | Yes |
| **Heap Sort** | O(n log n) | O(n log n) | O(n log n) | O(1) | No | Yes | Yes |
| **Counting Sort** | O(n+k) | O(n+k) | O(n+k) | O(k) | Yes | No | No |
| **Radix Sort** | O(d(n+k)) | O(d(n+k)) | O(d(n+k)) | O(n+k) | Yes | No | No |
| **Bucket Sort** | O(n+k) | O(n+k) | O(n²) | O(n+k) | Yes | No | No |
| **Tim Sort** | O(n) | O(n log n) | O(n log n) | O(n) | Yes | No | Yes |

### Graph Algorithms

| Algorithm | Time | Space | Use Case |
|---|---|---|---|
| **BFS** | O(V + E) | O(V) | Shortest path (unweighted), level-order |
| **DFS** | O(V + E) | O(V) | Cycle detection, topological sort, connected components |
| **Dijkstra** | O((V+E) log V) | O(V) | Shortest path (non-negative weights) |
| **Bellman-Ford** | O(V · E) | O(V) | Shortest path (negative weights), detect negative cycles |
| **Floyd-Warshall** | O(V³) | O(V²) | All-pairs shortest paths |
| **A*** | O(E) to O(V²) | O(V) | Shortest path with heuristic |
| **Kruskal's MST** | O(E log E) | O(V) | MST for sparse graphs |
| **Prim's MST** | O(E log V) | O(V) | MST for dense graphs |
| **Topological Sort** | O(V + E) | O(V) | DAG ordering, dependency resolution |
| **Tarjan's SCC** | O(V + E) | O(V) | Strongly connected components |
| **Kosaraju's SCC** | O(V + E) | O(V) | Strongly connected components |

---

## 26. Which Data Structure Should I Use?

### Decision Flowchart

```
START: What operation do you need most?
│
├─ Fast LOOKUP by key?
│   └─ Yes ──► Hash Table (O(1) avg)
│       ├─ Need ordered iteration too? ──► Balanced BST (TreeMap/std::map)
│       └─ Need prefix-based lookup? ──► Trie
│
├─ Fast ACCESS by index?
│   └─ Yes ──► Array / Dynamic Array (O(1))
│       ├─ Fixed size known? ──► Static Array
│       └─ Size changes? ──► Dynamic Array (vector/list)
│
├─ Fast INSERT/DELETE?
│   ├─ Only at ends?
│   │   ├─ One end only (LIFO)? ──► Stack
│   │   ├─ Both ends? ──► Deque
│   │   └─ One end in, other end out (FIFO)? ──► Queue
│   ├─ At arbitrary positions?
│   │   ├─ Need ordered data? ──► Balanced BST
│   │   └─ Don't need order? ──► Linked List or Hash Table
│   └─ Frequent insert + need min/max?
│       └─ ──► Heap / Priority Queue
│
├─ Need to find MIN/MAX quickly?
│   └─ Yes ──► Heap (O(1) find, O(log n) extract)
│       ├─ Need both min and max? ──► Two Heaps
│       └─ Need k-th element? ──► Heap of size k
│
├─ Need RANGE QUERIES with updates?
│   ├─ Sum/min/max over range?
│   │   ├─ Only point updates? ──► Fenwick Tree (simpler)
│   │   └─ Range updates too? ──► Segment Tree (lazy propagation)
│   └─ Static data (no updates)? ──► Prefix Sum Array
│
├─ Need to track CONNECTED COMPONENTS?
│   └─ Yes ──► Union-Find (DSU)
│       ├─ Dynamic connectivity (edges added)? ──► Union-Find
│       └─ Static graph? ──► BFS/DFS also works
│
├─ Working with STRINGS?
│   ├─ Prefix matching / autocomplete? ──► Trie
│   ├─ Pattern matching? ──► KMP / Rabin-Karp
│   └─ All substrings? ──► Suffix Array / Suffix Tree
│
└─ Need SORTED data with fast operations?
    ├─ Static (no modifications)? ──► Sorted Array + Binary Search
    └─ Dynamic (insertions/deletions)? ──► Balanced BST (AVL/Red-Black)
```

### Quick Selection Guide

| Requirement | First Choice | Second Choice |
|---|---|---|
| Key-value lookup | Hash Map | Balanced BST |
| Ordered key-value lookup | Balanced BST (TreeMap) | Skip List |
| FIFO processing | Queue | Linked List |
| LIFO processing | Stack | Array |
| Priority-based processing | Heap | Balanced BST |
| Duplicate detection | Hash Set | Sorted Array |
| Frequency counting | Hash Map | Array (if keys are small ints) |
| Sorted iteration | Balanced BST | Sorted Array |
| Range sum/min/max queries | Segment Tree / BIT | Sparse Table (static) |
| Dynamic connectivity | Union-Find | -- |
| Shortest path (unweighted) | BFS | -- |
| Shortest path (weighted) | Dijkstra / Bellman-Ford | A* (with heuristic) |
| Topological ordering | Kahn's BFS / DFS | -- |
| Minimum spanning tree | Kruskal's / Prim's | -- |

---

## 27. Space-Time Tradeoff Summary

### The Fundamental Tradeoff

Almost every optimization in computer science involves trading space for time or time for space:

| Strategy | Space | Time | Example |
|---|---|---|---|
| **Brute force** | O(1) extra | Slow | Two Sum with nested loops: O(n²) time, O(1) space |
| **Hash-based** | O(n) extra | Fast | Two Sum with hash map: O(n) time, O(n) space |
| **Precompute** | O(n) table | O(1) query | Prefix sums: O(n) build, O(1) range query |
| **Memoization** | O(states) cache | Avoid recompute | DP: store all subproblem results |
| **Space-optimized DP** | O(row) | Same | Keep only previous row of DP table |

### Common Space-Time Tradeoffs in Practice

| Problem | Time-Optimized | Space-Optimized |
|---|---|---|
| **Two Sum** | O(n) time, O(n) space (hash map) | O(n log n) time, O(1) space (sort + two pointers) |
| **Fibonacci** | O(n) time, O(n) space (memo array) | O(n) time, O(1) space (two variables) |
| **Knapsack** | O(n·W) time, O(n·W) space (2D table) | O(n·W) time, O(W) space (1D array) |
| **LCS** | O(m·n) time, O(m·n) space (2D table) | O(m·n) time, O(min(m,n)) space (two rows) |
| **Range sum queries** | O(1) query, O(n) space (prefix sum) | O(n) query, O(1) space (linear scan) |
| **Graph shortest path** | O(V²) space (adj matrix), O(1) edge check | O(V+E) space (adj list), O(deg) edge check |
| **Duplicate detection** | O(n) time, O(n) space (hash set) | O(n log n) time, O(1) space (sort in-place) |

### Constraint-Based Complexity Targets

Use problem constraints to determine the expected time complexity:

| Constraint (n ≤ ...) | Target Complexity | Typical Approach |
|---|---|---|
| 10 - 12 | O(n!) or O(2^n) | Brute-force backtracking, bitmask |
| 20 | O(2^n · n) | Bitmask DP, meet-in-the-middle |
| 100 | O(n³) or O(n² log n) | Triple loop DP, Floyd-Warshall |
| 500 | O(n³) | DP with O(n) transition |
| 1,000 | O(n²·log n) | DP + binary search |
| 5,000 - 10,000 | O(n²) | Two-pointer with nesting, 2D DP |
| 100,000 | O(n log n) | Sort, binary search, heap, segment tree |
| 1,000,000 | O(n) | Two pointers, sliding window, greedy, hash |
| 10,000,000 | O(n) | Linear scan, in-place |
| 10^9+ | O(log n) or O(1) | Binary search, math formula, bit tricks |

### Memory Estimation

| Data Type | Size (typical) | 10^6 Elements | 10^7 Elements |
|---|---|---|---|
| int (32-bit) | 4 bytes | ~4 MB | ~40 MB |
| long/int64 | 8 bytes | ~8 MB | ~80 MB |
| double | 8 bytes | ~8 MB | ~80 MB |
| bool (C++ vector) | 1 bit* | ~125 KB | ~1.25 MB |
| Pointer (64-bit) | 8 bytes | ~8 MB | ~80 MB |
| Python int | ~28 bytes | ~28 MB | ~280 MB |
| Python list entry | ~8 bytes (ref) | ~8 MB | ~80 MB |
| std::string (short) | ~32 bytes | ~32 MB | ~320 MB |

*`std::vector<bool>` is a special case that packs bits.

**Rule of thumb**: Competitive programming typically allows ~256 MB memory. An int array of size 10^7 (~40 MB) is safe; 10^8 (~400 MB) is risky.

### Amortized Analysis Summary

| Operation | Individual Cost | Amortized Cost | Data Structure |
|---|---|---|---|
| Dynamic array append | O(n) worst case | **O(1)** amortized | vector, list |
| Hash table insert | O(n) worst case | **O(1)** amortized | dict, HashMap |
| Union-Find (find/union) | O(log n) worst case | **O(α(n))** amortized | DSU |
| Splay tree (all ops) | O(n) worst case | **O(log n)** amortized | Splay tree |

---

*End of Data Structures & Algorithms Comprehensive Reference.*
