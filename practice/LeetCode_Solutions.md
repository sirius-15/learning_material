# LeetCode Solutions -- Python and C++ Solutions for the 300-Problem Checklist

> Last reviewed: 2026-11 · Versions assumed: Python 3.10+, C++17; LeetCode problem numbers, titles, method signatures, and official difficulty labels as of 2026-11.

> This file has full solutions for the 111 problems on the [300-problem checklist](Coding_Problem_List.md#2-the-300-problem-checklist-by-pattern) that are not already worked in [LeetCode Patterns](../computer-science/LeetCode_Patterns.md). Between the two files, every checklist problem has a solution, and every checklist line links straight to its solution. Sections use the checklist's pattern numbering. Patterns that have no extra problems here (5 Cyclic Sort, 9 Two Heaps, 25 Line Sweep) are skipped. Within a section, problems follow checklist order (easier to harder).

---

## Table of Contents

- [How to Use This File](#how-to-use-this-file)
- [1. Two Pointers](#1-two-pointers)
- [2. Sliding Window](#2-sliding-window)
- [3. Fast and Slow Pointers](#3-fast-and-slow-pointers)
- [4. Merge Intervals](#4-merge-intervals)
- [6. In-place Linked List Reversal](#6-in-place-linked-list-reversal)
- [7. BFS (Breadth-First Search)](#7-bfs-breadth-first-search)
- [8. DFS (Depth-First Search)](#8-dfs-depth-first-search)
- [10. Subsets / Backtracking](#10-subsets--backtracking)
- [11. Modified Binary Search](#11-modified-binary-search)
- [12. Top K Elements](#12-top-k-elements)
- [13. K-way Merge](#13-k-way-merge)
- [14. Topological Sort](#14-topological-sort)
- [15. Monotonic Stack / Queue](#15-monotonic-stack--queue)
- [16. Union Find (Disjoint Set)](#16-union-find-disjoint-set)
- [17. Trie (Prefix Tree)](#17-trie-prefix-tree)
- [18. Dynamic Programming](#18-dynamic-programming)
- [19. Greedy](#19-greedy)
- [20. Bit Manipulation](#20-bit-manipulation)
- [21. Prefix Sum & Difference Array](#21-prefix-sum--difference-array)
- [22. Hashing & Array Classics](#22-hashing--array-classics)
- [23. Matrix Manipulation](#23-matrix-manipulation)
- [24. Stack-based Parsing](#24-stack-based-parsing)
- [26. Design Problems](#26-design-problems)

---

## How to Use This File

**Attempt first.** Each entry is meant to be read *after* a timed attempt, following the [attempt -> hint -> solution -> re-solve loop](Coding_Problem_List.md#62-the-attempt---hint---solution---re-solve-loop). If you are stuck, the first hint is the pattern name (the section heading). The second is the **Intuition** paragraph. Read the code only at the hard stop.

**Entry layout.**

| Part | What it contains |
|---|---|
| **Problem** | A short paraphrase. Check the LeetCode page for the exact constraints. |
| **Intuition** | The key observation or invariant, and why it gives the stated complexity |
| **Python** / **C++** | The same algorithm in both languages, using LeetCode's class and method signatures |
| **Complexity** | Time and space, with every variable defined |
| **Pitfalls** | The edge cases and bugs that most often cost a submission |

**Code conventions.** As on LeetCode, the solutions leave out the `ListNode`, `TreeNode`, and `Node` definitions. The C++ code assumes `#include <bits/stdc++.h>` and `using namespace std;`. To run a C++ solution locally, add that prelude, the node struct if needed, and a `main()` with asserts, then compile with the [practice flags](Coding_Problem_List.md#64-practice-environment-rules):

```bash
g++ -std=c++20 -O1 -g -Wall -Wextra -Wshadow -fsanitize=address,undefined sol.cpp -o sol && ./sol
```

**Verification.** Each Python solution was run against LeetCode's examples, at least one edge case, and, for many problems, a brute force on random small inputs. Each C++ solution was compiled with `-Wall -Wextra -fsanitize=address,undefined` and run on the same cases.

---

## 1. Two Pointers

Template and pitfalls: [LeetCode Patterns §1 Two Pointers](../computer-science/LeetCode_Patterns.md#1-two-pointers)

### LC 283 · Move Zeroes · Easy

> **Problem:** Given an integer array `nums`, move all `0`s to the end while maintaining the relative order of the non-zero elements. Must be done in-place without copying the array.

🔗 [https://leetcode.com/problems/move-zeroes/](https://leetcode.com/problems/move-zeroes/)

**Intuition:** Keep a write pointer `k` for the next slot of the non-zero prefix. Scan with a read pointer; each non-zero element is swapped into position `k`. Swapping (rather than copy-then-zero-fill) keeps the zeros behind the prefix automatically and minimizes writes when there are few zeros.

**Python**

```python
class Solution:
    def moveZeroes(self, nums: list[int]) -> None:
        k = 0  # nums[:k] holds the non-zeros in order
        for i in range(len(nums)):
            if nums[i] != 0:
                nums[k], nums[i] = nums[i], nums[k]
                k += 1
```

**C++**

```cpp
class Solution {
public:
    void moveZeroes(vector<int>& nums) {
        int k = 0;  // nums[0..k) holds the non-zeros in order
        for (int i = 0; i < (int)nums.size(); ++i)
            if (nums[i] != 0) swap(nums[k++], nums[i]);
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n) |
| **Space** | O(1) |

**Pitfalls:** Must modify in place and return nothing; arrays with no zeros or all zeros should be untouched in effect.

---

### LC 26 · Remove Duplicates from Sorted Array · Easy

> **Problem:** Given an integer array `nums` sorted in non-decreasing order, remove the duplicates in-place so each unique element appears once, keeping the relative order. Return `k`, the number of unique elements; the first `k` slots of `nums` must hold them.

🔗 [https://leetcode.com/problems/remove-duplicates-from-sorted-array/](https://leetcode.com/problems/remove-duplicates-from-sorted-array/)

**Intuition:** Because the array is sorted, duplicates are adjacent. Keep a write pointer `k` marking the end of the unique prefix and a read pointer scanning forward; whenever the read value differs from the last written value, copy it to `nums[k]` and advance `k`. One pass, no extra memory.

**Python**

```python
class Solution:
    def removeDuplicates(self, nums: list[int]) -> int:
        k = 1  # nums[:k] is the unique prefix
        for i in range(1, len(nums)):
            if nums[i] != nums[k - 1]:
                nums[k] = nums[i]
                k += 1
        return k
```

**C++**

```cpp
class Solution {
public:
    int removeDuplicates(vector<int>& nums) {
        int k = 1;  // nums[0..k) is the unique prefix
        for (int i = 1; i < (int)nums.size(); ++i)
            if (nums[i] != nums[k - 1]) nums[k++] = nums[i];
        return k;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n) |
| **Space** | O(1) |

**Pitfalls:** Compare against the last written value `nums[k - 1]`, not `nums[i - 1]` (both work here, but the former generalizes to "at most 2 copies"); `k` starts at 1 because `n >= 1`.

---

### LC 977 · Squares of a Sorted Array · Easy

> **Problem:** Given an integer array `nums` sorted in non-decreasing order (may contain negatives), return an array of the squares of each number, also sorted in non-decreasing order. Follow-up: do it in O(n).

🔗 [https://leetcode.com/problems/squares-of-a-sorted-array/](https://leetcode.com/problems/squares-of-a-sorted-array/)

**Intuition:** The largest square is always at one of the two ends (most negative or most positive). Put pointers at both ends, compare absolute values, write the larger square into the result from the back, and move that pointer inward. This avoids the O(n log n) square-then-sort brute force.

**Python**

```python
class Solution:
    def sortedSquares(self, nums: list[int]) -> list[int]:
        n = len(nums)
        res = [0] * n
        left, right = 0, n - 1
        for pos in range(n - 1, -1, -1):  # fill largest first
            if abs(nums[left]) > abs(nums[right]):
                res[pos] = nums[left] * nums[left]
                left += 1
            else:
                res[pos] = nums[right] * nums[right]
                right -= 1
        return res
```

**C++**

```cpp
class Solution {
public:
    vector<int> sortedSquares(vector<int>& nums) {
        int n = nums.size();
        vector<int> res(n);
        int left = 0, right = n - 1;
        for (int pos = n - 1; pos >= 0; --pos) {  // fill largest first
            if (abs(nums[left]) > abs(nums[right])) {
                res[pos] = nums[left] * nums[left];
                ++left;
            } else {
                res[pos] = nums[right] * nums[right];
                --right;
            }
        }
        return res;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n) |
| **Space** | O(1) extra (O(n) for the output) |

**Pitfalls:** Fill from the back (largest first); filling from the front would require finding the zero crossing first. All-negative and all-positive arrays must work.

---

### LC 680 · Valid Palindrome II · Easy

> **Problem:** Given a string `s` of lowercase letters, return `true` if it can be a palindrome after deleting at most one character.

🔗 [https://leetcode.com/problems/valid-palindrome-ii/](https://leetcode.com/problems/valid-palindrome-ii/)

**Intuition:** Walk two pointers inward while characters match. At the first mismatch `s[i] != s[j]`, the only possible fixes are deleting `s[i]` or deleting `s[j]`, so check whether `s[i+1..j]` or `s[i..j-1]` is a palindrome. Each check is linear, so the total is O(n) instead of the O(n^2) try-every-deletion brute force.

**Python**

```python
class Solution:
    def validPalindrome(self, s: str) -> bool:
        def is_pal(i: int, j: int) -> bool:
            while i < j:
                if s[i] != s[j]:
                    return False
                i, j = i + 1, j - 1
            return True

        i, j = 0, len(s) - 1
        while i < j:
            if s[i] != s[j]:
                return is_pal(i + 1, j) or is_pal(i, j - 1)
            i, j = i + 1, j - 1
        return True
```

**C++**

```cpp
class Solution {
public:
    bool validPalindrome(string s) {
        auto isPal = [&](int i, int j) {
            while (i < j)
                if (s[i++] != s[j--]) return false;
            return true;
        };
        int i = 0, j = (int)s.size() - 1;
        while (i < j) {
            if (s[i] != s[j]) return isPal(i + 1, j) || isPal(i, j - 1);
            ++i, --j;
        }
        return true;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n) |
| **Space** | O(1) |

**Pitfalls:** At the mismatch you must try both deletions (e.g. `"aab"` only works by deleting the right-hand `b`); do not recurse with another deletion allowed.

---

### LC 16 · 3Sum Closest · Medium

> **Problem:** Given an integer array `nums` of length `n >= 3` and an integer `target`, find three integers in `nums` whose sum is closest to `target` and return that sum. Exactly one answer exists.

🔗 [https://leetcode.com/problems/3sum-closest/](https://leetcode.com/problems/3sum-closest/)

**Intuition:** Sort, fix the first element `i`, then run a two-pointer scan on the suffix: if the triple sum is below target move `lo` right, otherwise move `hi` left, tracking the sum with the smallest `|sum - target|`. Each fixed `i` costs O(n), giving O(n^2) versus the O(n^3) brute force. Return immediately on an exact match.

**Python**

```python
class Solution:
    def threeSumClosest(self, nums: list[int], target: int) -> int:
        nums.sort()
        best = nums[0] + nums[1] + nums[2]
        for i in range(len(nums) - 2):
            lo, hi = i + 1, len(nums) - 1
            while lo < hi:
                s = nums[i] + nums[lo] + nums[hi]
                if abs(s - target) < abs(best - target):
                    best = s
                if s < target:
                    lo += 1
                elif s > target:
                    hi -= 1
                else:
                    return s
        return best
```

**C++**

```cpp
class Solution {
public:
    int threeSumClosest(vector<int>& nums, int target) {
        sort(nums.begin(), nums.end());
        int n = nums.size();
        int best = nums[0] + nums[1] + nums[2];
        for (int i = 0; i < n - 2; ++i) {
            int lo = i + 1, hi = n - 1;
            while (lo < hi) {
                int s = nums[i] + nums[lo] + nums[hi];
                if (abs(s - target) < abs(best - target)) best = s;
                if (s < target) ++lo;
                else if (s > target) --hi;
                else return s;
            }
        }
        return best;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n^2) |
| **Space** | O(1) extra (ignoring sort) |

**Pitfalls:** Initialize `best` with a real triple, not `INT_MAX` (then `best - target` can overflow); constraints keep sums within `int` (`|nums[i]| ≤ 1000`, `|target| ≤ 10^4`).

---

### LC 18 · 4Sum · Medium

> **Problem:** Given an integer array `nums` (length ≤ 200, `|nums[i]| ≤ 10^9`) and an integer `target`, return all unique quadruplets `[nums[a], nums[b], nums[c], nums[d]]` with distinct indices whose sum equals `target`, in any order.

🔗 [https://leetcode.com/problems/4sum/](https://leetcode.com/problems/4sum/)

**Intuition:** Extend 3Sum by one level: sort, fix the first two elements with nested loops, and find the remaining pair with a two-pointer scan on the suffix. Skipping equal values at every level (and after each match) guarantees unique quadruplets without a hash set. This is O(n^3) versus the O(n^4) brute force; the same pattern generalizes to kSum by recursion.

**Python**

```python
class Solution:
    def fourSum(self, nums: list[int], target: int) -> list[list[int]]:
        nums.sort()
        n, res = len(nums), []
        for i in range(n - 3):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            for j in range(i + 1, n - 2):
                if j > i + 1 and nums[j] == nums[j - 1]:
                    continue
                lo, hi = j + 1, n - 1
                while lo < hi:
                    s = nums[i] + nums[j] + nums[lo] + nums[hi]
                    if s < target:
                        lo += 1
                    elif s > target:
                        hi -= 1
                    else:
                        res.append([nums[i], nums[j], nums[lo], nums[hi]])
                        lo, hi = lo + 1, hi - 1
                        while lo < hi and nums[lo] == nums[lo - 1]:  # skip duplicate third values
                            lo += 1
        return res
```

**C++**

```cpp
class Solution {
public:
    vector<vector<int>> fourSum(vector<int>& nums, int target) {
        sort(nums.begin(), nums.end());
        int n = nums.size();
        vector<vector<int>> res;
        for (int i = 0; i < n - 3; ++i) {
            if (i > 0 && nums[i] == nums[i - 1]) continue;
            for (int j = i + 1; j < n - 2; ++j) {
                if (j > i + 1 && nums[j] == nums[j - 1]) continue;
                int lo = j + 1, hi = n - 1;
                while (lo < hi) {
                    long long s = (long long)nums[i] + nums[j] + nums[lo] + nums[hi];  // up to 4e9
                    if (s < target) ++lo;
                    else if (s > target) --hi;
                    else {
                        res.push_back({nums[i], nums[j], nums[lo], nums[hi]});
                        ++lo, --hi;
                        while (lo < hi && nums[lo] == nums[lo - 1]) ++lo;  // skip duplicate third values
                    }
                }
            }
        }
        return res;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n^3) |
| **Space** | O(1) extra (ignoring sort and output) |

**Pitfalls:** Sum of four values overflows 32-bit `int` in C++ (use `long long`); dedupe the second index with `j > i + 1`, not `j > 0`, or valid quadruplets like `[2,2,2,2]` are lost.

---

## 2. Sliding Window

Template and pitfalls: [LeetCode Patterns §2 Sliding Window](../computer-science/LeetCode_Patterns.md#2-sliding-window)

### LC 219 · Contains Duplicate II · Easy

> **Problem:** Given an integer array `nums` and an integer `k`, return `true` if there are two distinct indices `i` and `j` with `nums[i] == nums[j]` and `abs(i - j) ≤ k`.

🔗 [https://leetcode.com/problems/contains-duplicate-ii/](https://leetcode.com/problems/contains-duplicate-ii/)

**Intuition:** Maintain a hash set of the last `k` values (a fixed-size window). For each new element, if it is already in the set there is a duplicate within distance `k`; otherwise add it and evict the element that just fell out of range. Each element is inserted and removed once.

**Python**

```python
class Solution:
    def containsNearbyDuplicate(self, nums: list[int], k: int) -> bool:
        window = set()  # values at indices [i-k, i-1]
        for i, x in enumerate(nums):
            if x in window:
                return True
            window.add(x)
            if len(window) > k:
                window.remove(nums[i - k])
        return False
```

**C++**

```cpp
class Solution {
public:
    bool containsNearbyDuplicate(vector<int>& nums, int k) {
        unordered_set<int> window;  // values at indices [i-k, i-1]
        for (int i = 0; i < (int)nums.size(); ++i) {
            if (window.count(nums[i])) return true;
            window.insert(nums[i]);
            if ((int)window.size() > k) window.erase(nums[i - k]);
        }
        return false;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n) |
| **Space** | O(min(n, k)) |

**Pitfalls:** `k = 0` must always return `false` (the window evicts immediately); evicting by size works only because the set never holds duplicates (we return first).

---

### LC 438 · Find All Anagrams in a String · Medium

> **Problem:** Given strings `s` and `p` of lowercase letters, return all start indices of substrings of `s` that are anagrams of `p`, in any order.

🔗 [https://leetcode.com/problems/find-all-anagrams-in-a-string/](https://leetcode.com/problems/find-all-anagrams-in-a-string/)

**Intuition:** Every anagram has length `len(p)`, so slide a fixed-size window over `s` and maintain its 26-letter count. Adding the incoming character and removing the outgoing one is O(1); comparing the two count arrays is O(26). This beats re-counting each window from scratch (O(n·m)).

**Python**

```python
class Solution:
    def findAnagrams(self, s: str, p: str) -> list[int]:
        m = len(p)
        need, win = [0] * 26, [0] * 26
        for c in p:
            need[ord(c) - 97] += 1
        res = []
        for i, c in enumerate(s):
            win[ord(c) - 97] += 1
            if i >= m:
                win[ord(s[i - m]) - 97] -= 1  # drop char leaving the window
            if i >= m - 1 and win == need:
                res.append(i - m + 1)
        return res
```

**C++**

```cpp
class Solution {
public:
    vector<int> findAnagrams(string s, string p) {
        int m = p.size();
        array<int, 26> need{}, win{};
        for (char c : p) ++need[c - 'a'];
        vector<int> res;
        for (int i = 0; i < (int)s.size(); ++i) {
            ++win[s[i] - 'a'];
            if (i >= m) --win[s[i - m] - 'a'];  // drop char leaving the window
            if (i >= m - 1 && win == need) res.push_back(i - m + 1);
        }
        return res;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(26·n), n = len(s) |
| **Space** | O(1) (two 26-entry arrays) |

**Pitfalls:** `len(p) > len(s)` must return `[]`; only compare once the window is full (`i >= m - 1`). A "matches" counter can make the check O(1) but is easy to get wrong.

---

### LC 1004 · Max Consecutive Ones III · Medium

> **Problem:** Given a binary array `nums` and an integer `k`, return the maximum number of consecutive `1`s in the array if you can flip at most `k` `0`s.

🔗 [https://leetcode.com/problems/max-consecutive-ones-iii/](https://leetcode.com/problems/max-consecutive-ones-iii/)

**Intuition:** Rephrase as "longest subarray containing at most `k` zeros". Grow the window on the right, counting zeros; while there are more than `k`, shrink from the left. Each index enters and leaves once, so O(n).

**Python**

```python
class Solution:
    def longestOnes(self, nums: list[int], k: int) -> int:
        left = zeros = best = 0
        for right, x in enumerate(nums):
            zeros += x == 0
            while zeros > k:
                zeros -= nums[left] == 0
                left += 1
            best = max(best, right - left + 1)
        return best
```

**C++**

```cpp
class Solution {
public:
    int longestOnes(vector<int>& nums, int k) {
        int left = 0, zeros = 0, best = 0;
        for (int right = 0; right < (int)nums.size(); ++right) {
            zeros += nums[right] == 0;
            while (zeros > k) zeros -= nums[left++] == 0;
            best = max(best, right - left + 1);
        }
        return best;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n) |
| **Space** | O(1) |

**Pitfalls:** `k = 0` reduces to longest run of ones; `k` at least the number of zeros means the whole array. Update `best` after shrinking, not before.

---

## 3. Fast and Slow Pointers

Template and pitfalls: [LeetCode Patterns §3 Fast and Slow Pointers](../computer-science/LeetCode_Patterns.md#3-fast-and-slow-pointers)

### LC 160 · Intersection of Two Linked Lists · Easy

> **Problem:** Given the heads of two singly linked lists, return the node at which they intersect (by identity, not value), or `null` if they do not. The lists have no cycles and must keep their original structure. Follow-up: O(m + n) time, O(1) memory.

🔗 [https://leetcode.com/problems/intersection-of-two-linked-lists/](https://leetcode.com/problems/intersection-of-two-linked-lists/)

**Intuition:** Walk pointer `a` over A then B, and pointer `b` over B then A. Both travel `lenA + lenB` steps in total, so after switching lists they are aligned and meet at the first shared node; if there is none they both reach `null` at the same time. This removes the need to compute lengths or store visited nodes in a hash set.

**Python**

```python
class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        a, b = headA, headB
        while a is not b:
            a = a.next if a else headB
            b = b.next if b else headA
        return a  # shared node, or None
```

**C++**

```cpp
class Solution {
public:
    ListNode *getIntersectionNode(ListNode *headA, ListNode *headB) {
        ListNode *a = headA, *b = headB;
        while (a != b) {
            a = a ? a->next : headB;
            b = b ? b->next : headA;
        }
        return a;  // shared node, or nullptr
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(m + n), m and n are the list lengths |
| **Space** | O(1) |

**Pitfalls:** Compare node identity (`is` / pointer), not values; switch to the other head only after stepping onto `null`, otherwise non-intersecting lists loop forever.

---

### LC 19 · Remove Nth Node From End of List · Medium

> **Problem:** Given the head of a linked list, remove the `n`-th node from the end and return the head. `1 ≤ n ≤ size`. Follow-up: do it in one pass.

🔗 [https://leetcode.com/problems/remove-nth-node-from-end-of-list/](https://leetcode.com/problems/remove-nth-node-from-end-of-list/)

**Intuition:** Start both pointers at a dummy node before the head and move `fast` `n + 1` steps ahead. Then move both until `fast` falls off the end; `slow` is now just before the node to delete. The dummy makes removing the head itself uniform.

**Python**

```python
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        fast = slow = dummy
        for _ in range(n + 1):  # gap of n nodes between slow and fast
            fast = fast.next
        while fast:
            fast, slow = fast.next, slow.next
        slow.next = slow.next.next
        return dummy.next
```

**C++**

```cpp
class Solution {
public:
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        ListNode dummy(0, head);
        ListNode *fast = &dummy, *slow = &dummy;
        for (int i = 0; i <= n; ++i) fast = fast->next;  // gap of n nodes
        while (fast) {
            fast = fast->next;
            slow = slow->next;
        }
        slow->next = slow->next->next;
        return dummy.next;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(L), L = list length |
| **Space** | O(1) |

**Pitfalls:** Removing the head (`n == L`) and single-node lists are why the dummy node is needed; advance `n + 1` (not `n`) so `slow` stops before the target.

---

## 4. Merge Intervals

Template and pitfalls: [LeetCode Patterns §4 Merge Intervals](../computer-science/LeetCode_Patterns.md#4-merge-intervals)

### LC 1851 · Minimum Interval to Include Each Query · Hard

> **Problem:** Given `intervals[i] = [left_i, right_i]` (inclusive, size `right_i - left_i + 1`) and an array `queries`, answer each query `q` with the size of the smallest interval containing `q`, or `-1` if none does. Up to 10^5 intervals and 10^5 queries.

🔗 [https://leetcode.com/problems/minimum-interval-to-include-each-query/](https://leetcode.com/problems/minimum-interval-to-include-each-query/)

**Intuition:** Answer queries offline in increasing order. Sort intervals by left end; as `q` grows, push every interval with `left ≤ q` into a min-heap keyed by size, and lazily pop heap tops whose `right < q` (they can never contain a later, larger query either). The heap top is then the smallest interval containing `q`. Each interval is pushed and popped once, versus the O(n·q) scan-everything brute force.

**Python**

```python
import heapq


class Solution:
    def minInterval(self, intervals: list[list[int]], queries: list[int]) -> list[int]:
        intervals.sort()
        res = [-1] * len(queries)
        heap = []  # (size, right)
        i = 0
        for q, idx in sorted((q, idx) for idx, q in enumerate(queries)):
            while i < len(intervals) and intervals[i][0] <= q:
                l, r = intervals[i]
                heapq.heappush(heap, (r - l + 1, r))
                i += 1
            while heap and heap[0][1] < q:  # expired: ends before q
                heapq.heappop(heap)
            if heap:
                res[idx] = heap[0][0]
        return res
```

**C++**

```cpp
class Solution {
public:
    vector<int> minInterval(vector<vector<int>>& intervals, vector<int>& queries) {
        sort(intervals.begin(), intervals.end());
        int nq = queries.size();
        vector<int> order(nq), res(nq, -1);
        iota(order.begin(), order.end(), 0);
        sort(order.begin(), order.end(), [&](int a, int b) { return queries[a] < queries[b]; });
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> heap;  // (size, right)
        size_t i = 0;
        for (int idx : order) {
            int q = queries[idx];
            while (i < intervals.size() && intervals[i][0] <= q) {
                heap.push({intervals[i][1] - intervals[i][0] + 1, intervals[i][1]});
                ++i;
            }
            while (!heap.empty() && heap.top().second < q) heap.pop();  // expired
            if (!heap.empty()) res[idx] = heap.top().first;
        }
        return res;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n log n + q log q), n intervals, q queries |
| **Space** | O(n + q) |

**Pitfalls:** Results must go back in the original query order (sort indices, not values); interval size is inclusive (`+1`); popping expired intervals is safe only because queries are processed in increasing order.

---

## 6. In-place Linked List Reversal

Template and pitfalls: [LeetCode Patterns §6 In-place Linked List Reversal](../computer-science/LeetCode_Patterns.md#6-in-place-linked-list-reversal)

### LC 2 · Add Two Numbers · Medium

> **Problem:** Two non-empty linked lists represent non-negative integers with digits stored in reverse order (one digit per node). Return their sum as a linked list in the same format. No leading zeros except the number 0 itself.

🔗 [https://leetcode.com/problems/add-two-numbers/](https://leetcode.com/problems/add-two-numbers/)

**Intuition:** Reverse order means the head is the least significant digit, so this is grade-school addition walking both lists together. Keep a carry, emit `(a + b + carry) % 10` each step, and continue while either list or the carry remains. A dummy head avoids special-casing the first node.

**Python**

```python
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        tail = dummy = ListNode()
        carry = 0
        while l1 or l2 or carry:
            total = carry
            if l1:
                total += l1.val
                l1 = l1.next
            if l2:
                total += l2.val
                l2 = l2.next
            carry, digit = divmod(total, 10)
            tail.next = ListNode(digit)
            tail = tail.next
        return dummy.next
```

**C++**

```cpp
class Solution {
public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        ListNode dummy;
        ListNode* tail = &dummy;
        int carry = 0;
        while (l1 || l2 || carry) {
            int total = carry;
            if (l1) { total += l1->val; l1 = l1->next; }
            if (l2) { total += l2->val; l2 = l2->next; }
            carry = total / 10;
            tail->next = new ListNode(total % 10);
            tail = tail->next;
        }
        return dummy.next;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(max(m, n)), m and n are the list lengths |
| **Space** | O(1) extra (O(max(m, n)) for the output) |

**Pitfalls:** Do not forget the final carry (`5 + 5 → [0, 1]`); lists of different lengths; never convert to integers (up to 100 digits overflows in C++).

---

### LC 138 · Copy List with Random Pointer · Medium

> **Problem:** Each node of a linked list has `next` and a `random` pointer that may point to any node in the list or `null`. Return a deep copy: new nodes whose `next` and `random` pointers mirror the original structure, with no pointers into the original list.

🔗 [https://leetcode.com/problems/copy-list-with-random-pointer/](https://leetcode.com/problems/copy-list-with-random-pointer/)

**Intuition:** The straightforward solution maps old → new nodes in a hash map (O(n) extra space). To use O(1) extra space, weave each copy right after its original (`A → A' → B → B'`); then `A'.random = A.random.next`, because the copy of any node is its `next`. Finally unweave the two lists, restoring the original.

**Python**

```python
class Solution:
    def copyRandomList(self, head: "Optional[Node]") -> "Optional[Node]":
        if not head:
            return None
        cur = head
        while cur:  # weave: A -> A' -> B -> B'
            cur.next = Node(cur.val, cur.next)
            cur = cur.next.next
        cur = head
        while cur:  # copy of X.random is X.random.next
            if cur.random:
                cur.next.random = cur.random.next
            cur = cur.next.next
        new_head, cur = head.next, head
        while cur:  # unweave and restore the original
            copy = cur.next
            cur.next = copy.next
            copy.next = copy.next.next if copy.next else None
            cur = cur.next
        return new_head
```

**C++**

```cpp
class Solution {
public:
    Node* copyRandomList(Node* head) {
        if (!head) return nullptr;
        for (Node* cur = head; cur; cur = cur->next->next) {  // weave: A -> A' -> B -> B'
            Node* copy = new Node(cur->val);
            copy->next = cur->next;
            cur->next = copy;
        }
        for (Node* cur = head; cur; cur = cur->next->next)  // copy of X.random is X.random.next
            if (cur->random) cur->next->random = cur->random->next;
        Node* newHead = head->next;
        for (Node* cur = head; cur; cur = cur->next) {  // unweave and restore the original
            Node* copy = cur->next;
            cur->next = copy->next;
            copy->next = copy->next ? copy->next->next : nullptr;
        }
        return newHead;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n) |
| **Space** | O(1) extra (O(n) for the copy itself) |

**Pitfalls:** The original list must be restored (the judge checks it); `random` may be null or point to the node itself; set all `random`s before unweaving, since unweaving breaks the `X.next` = copy relation.

---

### LC 24 · Swap Nodes in Pairs · Medium

> **Problem:** Given a linked list, swap every two adjacent nodes and return the new head. You must swap the nodes themselves, not their values.

🔗 [https://leetcode.com/problems/swap-nodes-in-pairs/](https://leetcode.com/problems/swap-nodes-in-pairs/)

**Intuition:** With `prev` pointing just before a pair `a → b`, rewire `prev → b → a → (rest)` and then move `prev` to `a`, which is now the tail of the swapped pair. A dummy head makes the first pair the same as every other. Iterative, so O(1) extra space (the recursive version uses O(n) stack).

**Python**

```python
class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        prev = dummy
        while prev.next and prev.next.next:
            a, b = prev.next, prev.next.next
            a.next, b.next, prev.next = b.next, a, b  # prev -> b -> a -> rest
            prev = a
        return dummy.next
```

**C++**

```cpp
class Solution {
public:
    ListNode* swapPairs(ListNode* head) {
        ListNode dummy(0, head);
        ListNode* prev = &dummy;
        while (prev->next && prev->next->next) {
            ListNode *a = prev->next, *b = a->next;
            a->next = b->next;  // prev -> b -> a -> rest
            b->next = a;
            prev->next = b;
            prev = a;
        }
        return dummy.next;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n) |
| **Space** | O(1) |

**Pitfalls:** Empty list, single node, and odd length (last node stays put); save `b.next` before overwriting `b.next`.

---

### LC 61 · Rotate List · Medium

> **Problem:** Given the head of a linked list, rotate the list to the right by `k` places. `k` can be up to 2·10^9, far larger than the length (≤ 500).

🔗 [https://leetcode.com/problems/rotate-list/](https://leetcode.com/problems/rotate-list/)

**Intuition:** Rotating by `k` equals rotating by `k % n`. Find the length `n` and the tail, link the tail to the head to form a ring, then walk `n - k % n` steps from the old tail to reach the new tail and cut the ring after it. One length pass plus at most one more pass.

**Python**

```python
class Solution:
    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if not head or not head.next:
            return head
        n, tail = 1, head
        while tail.next:
            tail = tail.next
            n += 1
        tail.next = head  # close the ring
        for _ in range(n - k % n):
            tail = tail.next
        head, tail.next = tail.next, None  # cut after the new tail
        return head
```

**C++**

```cpp
class Solution {
public:
    ListNode* rotateRight(ListNode* head, int k) {
        if (!head || !head->next) return head;
        int n = 1;
        ListNode* tail = head;
        while (tail->next) {
            tail = tail->next;
            ++n;
        }
        tail->next = head;  // close the ring
        for (int steps = n - k % n; steps > 0; --steps) tail = tail->next;
        head = tail->next;  // cut after the new tail
        tail->next = nullptr;
        return head;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n) |
| **Space** | O(1) |

**Pitfalls:** Reduce `k` modulo `n` (huge `k`); `k % n == 0` must return the original list (the ring walk of `n` steps handles it); empty list guards the `% n` by zero.

---

### LC 82 · Remove Duplicates from Sorted List II · Medium

> **Problem:** Given the head of a sorted linked list, delete all nodes that have duplicate values, leaving only values that appeared exactly once. Return the list still sorted.

🔗 [https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/](https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/)

**Intuition:** Keep `prev` as the last node known to be unique (starting at a dummy, since the head itself may be deleted). When `cur` starts a run of equal values, skip to the end of the run and link `prev` past the whole run; otherwise `cur` is unique and `prev` advances. Single pass, relinking in place.

**Python**

```python
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        prev, cur = dummy, head
        while cur:
            if cur.next and cur.val == cur.next.val:
                while cur.next and cur.val == cur.next.val:
                    cur = cur.next
                prev.next = cur.next  # drop the whole run
            else:
                prev = cur
            cur = cur.next
        return dummy.next
```

**C++**

```cpp
class Solution {
public:
    ListNode* deleteDuplicates(ListNode* head) {
        ListNode dummy(0, head);
        ListNode *prev = &dummy, *cur = head;
        while (cur) {
            if (cur->next && cur->val == cur->next->val) {
                while (cur->next && cur->val == cur->next->val) cur = cur->next;
                prev->next = cur->next;  // drop the whole run
            } else {
                prev = cur;
            }
            cur = cur->next;
        }
        return dummy.next;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n) |
| **Space** | O(1) |

**Pitfalls:** Duplicates at the head (`[1,1,2]`) and at the tail, and an all-duplicate list (`[1,1]` → empty); do not advance `prev` after removing a run, because the next node may start another run.

---

### LC 148 · Sort List · Medium

> **Problem:** Given the head of a linked list (up to 5·10^4 nodes), return the list sorted in ascending order. Follow-up: O(n log n) time and O(1) memory.

🔗 [https://leetcode.com/problems/sort-list/](https://leetcode.com/problems/sort-list/)

**Intuition:** Merge sort fits linked lists: splitting at the middle (fast/slow pointers) and merging two sorted lists both relink nodes in place without extra arrays. Top-down recursion gives O(n log n) time with O(log n) stack. For the strict O(1)-space follow-up, run the same merge bottom-up, merging runs of size 1, 2, 4, ... iteratively.

**Python**

```python
class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head
        slow, fast = head, head.next  # slow ends at the last node of the left half
        while fast and fast.next:
            slow, fast = slow.next, fast.next.next
        mid, slow.next = slow.next, None
        left, right = self.sortList(head), self.sortList(mid)
        tail = dummy = ListNode()
        while left and right:
            if left.val <= right.val:
                tail.next, left = left, left.next
            else:
                tail.next, right = right, right.next
            tail = tail.next
        tail.next = left or right
        return dummy.next
```

**C++**

```cpp
class Solution {
public:
    ListNode* sortList(ListNode* head) {
        if (!head || !head->next) return head;
        ListNode *slow = head, *fast = head->next;  // slow ends at the last node of the left half
        while (fast && fast->next) {
            slow = slow->next;
            fast = fast->next->next;
        }
        ListNode* mid = slow->next;
        slow->next = nullptr;
        ListNode *left = sortList(head), *right = sortList(mid);
        ListNode dummy;
        ListNode* tail = &dummy;
        while (left && right) {
            if (left->val <= right->val) { tail->next = left; left = left->next; }
            else { tail->next = right; right = right->next; }
            tail = tail->next;
        }
        tail->next = left ? left : right;
        return dummy.next;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n log n) |
| **Space** | O(log n) recursion (O(1) with bottom-up merge) |

**Pitfalls:** Start `fast` at `head.next` so a two-node list splits into 1 + 1 (starting at `head` recurses forever); cut `slow.next` before recursing; `<=` keeps the sort stable.

---

## 7. BFS (Breadth-First Search)

Template and pitfalls: [LeetCode Patterns §7 BFS (Breadth-First Search)](../computer-science/LeetCode_Patterns.md#7-bfs-breadth-first-search)

### LC 199 · Binary Tree Right Side View · Medium

> **Problem:** Given the root of a binary tree, imagine standing on its right side and return the values of the nodes you can see, ordered from top to bottom (i.e. the rightmost node of every level).

🔗 [https://leetcode.com/problems/binary-tree-right-side-view/](https://leetcode.com/problems/binary-tree-right-side-view/)

**Intuition:** Level-order BFS keeps exactly one level in the queue at the start of each round; enqueuing left before right means the last node in the queue is the rightmost node of that level. Record it, then drain the level. A DFS that visits right before left and records the first node seen at each new depth works equally well.

**Python**

```python
from collections import deque

class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> list[int]:
        res = []
        q = deque([root] if root else [])
        while q:
            res.append(q[-1].val)  # rightmost node of the current level
            for _ in range(len(q)):
                node = q.popleft()
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
        return res
```

**C++**

```cpp
class Solution {
public:
    vector<int> rightSideView(TreeNode* root) {
        vector<int> res;
        if (!root) return res;
        queue<TreeNode*> q;
        q.push(root);
        while (!q.empty()) {
            res.push_back(q.back()->val);  // rightmost node of the current level
            for (int k = (int)q.size(); k > 0; --k) {
                TreeNode* node = q.front(); q.pop();
                if (node->left) q.push(node->left);
                if (node->right) q.push(node->right);
            }
        }
        return res;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n), n = number of nodes |
| **Space** | O(w), w = maximum level width (≤ n) |

**Pitfalls:** Empty tree returns `[]`; a left-subtree node is visible when the right subtree is shorter, so "follow right children only" is wrong.

---

### LC 542 · 01 Matrix · Medium

> **Problem:** Given an m×n binary matrix `mat`, return a matrix where each cell holds the distance to the nearest `0` (distance between adjacent cells is 1, 4-directional). At least one `0` exists.

🔗 [https://leetcode.com/problems/01-matrix/](https://leetcode.com/problems/01-matrix/)

**Intuition:** Instead of a BFS from every `1` (O((m·n)^2)), run one multi-source BFS seeded with every `0` at distance 0. BFS reaches cells in non-decreasing distance order, so the first time a cell is discovered its distance is final. (A two-pass DP, top-left then bottom-right, also works in O(1) extra space.)

**Python**

```python
from collections import deque

class Solution:
    def updateMatrix(self, mat: list[list[int]]) -> list[list[int]]:
        m, n = len(mat), len(mat[0])
        dist = [[-1] * n for _ in range(m)]
        q = deque()
        for i in range(m):
            for j in range(n):
                if mat[i][j] == 0:
                    dist[i][j] = 0
                    q.append((i, j))
        while q:
            i, j = q.popleft()
            for x, y in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if 0 <= x < m and 0 <= y < n and dist[x][y] == -1:
                    dist[x][y] = dist[i][j] + 1
                    q.append((x, y))
        return dist
```

**C++**

```cpp
class Solution {
public:
    vector<vector<int>> updateMatrix(vector<vector<int>>& mat) {
        int m = mat.size(), n = mat[0].size();
        vector<vector<int>> dist(m, vector<int>(n, -1));
        queue<pair<int, int>> q;
        for (int i = 0; i < m; ++i)
            for (int j = 0; j < n; ++j)
                if (mat[i][j] == 0) {
                    dist[i][j] = 0;
                    q.push({i, j});
                }
        int dirs[5] = {0, 1, 0, -1, 0};
        while (!q.empty()) {
            auto [i, j] = q.front(); q.pop();
            for (int d = 0; d < 4; ++d) {
                int x = i + dirs[d], y = j + dirs[d + 1];
                if (x >= 0 && x < m && y >= 0 && y < n && dist[x][y] == -1) {
                    dist[x][y] = dist[i][j] + 1;
                    q.push({x, y});
                }
            }
        }
        return dist;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(m·n), m×n matrix |
| **Space** | O(m·n) for the queue and output |

**Pitfalls:** BFS from each `1` separately is quadratic and TLEs; mark cells when enqueued (not when dequeued) or cells get enqueued multiple times.

---

### LC 130 · Surrounded Regions · Medium

> **Problem:** Given an m×n board of `'X'` and `'O'`, capture every region of `'O'` that is completely surrounded by `'X'` (4-directionally) by flipping it to `'X'` in place. Regions touching the border are never captured.

🔗 [https://leetcode.com/problems/surrounded-regions/](https://leetcode.com/problems/surrounded-regions/)

**Intuition:** Invert the question: an `'O'` survives exactly when it is connected to a border `'O'`. BFS from all border `'O'` cells and mark them safe (`'S'`); afterwards every remaining `'O'` is surrounded. One final sweep flips `'O'`→`'X'` and `'S'`→`'O'`. Each cell is processed a constant number of times.

**Python**

```python
from collections import deque

class Solution:
    def solve(self, board: list[list[str]]) -> None:
        m, n = len(board), len(board[0])
        q = deque()
        for i in range(m):
            for j in range(n):
                if (i in (0, m - 1) or j in (0, n - 1)) and board[i][j] == 'O':
                    board[i][j] = 'S'  # safe: connected to the border
                    q.append((i, j))
        while q:
            i, j = q.popleft()
            for x, y in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if 0 <= x < m and 0 <= y < n and board[x][y] == 'O':
                    board[x][y] = 'S'
                    q.append((x, y))
        for row in board:
            for j, c in enumerate(row):
                row[j] = 'O' if c == 'S' else 'X'
```

**C++**

```cpp
class Solution {
public:
    void solve(vector<vector<char>>& board) {
        int m = board.size(), n = board[0].size();
        queue<pair<int, int>> q;
        for (int i = 0; i < m; ++i)
            for (int j = 0; j < n; ++j)
                if ((i == 0 || i == m - 1 || j == 0 || j == n - 1) && board[i][j] == 'O') {
                    board[i][j] = 'S';  // safe: connected to the border
                    q.push({i, j});
                }
        int dirs[5] = {0, 1, 0, -1, 0};
        while (!q.empty()) {
            auto [i, j] = q.front(); q.pop();
            for (int d = 0; d < 4; ++d) {
                int x = i + dirs[d], y = j + dirs[d + 1];
                if (x >= 0 && x < m && y >= 0 && y < n && board[x][y] == 'O') {
                    board[x][y] = 'S';
                    q.push({x, y});
                }
            }
        }
        for (auto& row : board)
            for (char& c : row)
                c = (c == 'S') ? 'O' : 'X';
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(m·n), m×n board |
| **Space** | O(m·n) worst-case queue |

**Pitfalls:** Must modify `board` in place (no return); recursive DFS on a 200×200 board can overflow the Python stack, which is why BFS is used here.

---

### LC 433 · Minimum Genetic Mutation · Medium

> **Problem:** A gene is an 8-character string over `A`, `C`, `G`, `T`. One mutation changes a single character, and every intermediate gene (and `endGene`) must appear in `bank`. Return the minimum number of mutations from `startGene` to `endGene`, or `-1` if impossible.

🔗 [https://leetcode.com/problems/minimum-genetic-mutation/](https://leetcode.com/problems/minimum-genetic-mutation/)

**Intuition:** Genes are nodes and single-character mutations that stay in the bank are unweighted edges, so level-by-level BFS from `startGene` yields the minimum mutation count. Generate the 8 × 3 candidate neighbours of each gene and keep only those in a bank hash set rather than comparing against every bank entry. This is Word Ladder (LC 127) with a 4-letter alphabet.

**Python**

```python
from collections import deque

class Solution:
    def minMutation(self, startGene: str, endGene: str, bank: list[str]) -> int:
        valid = set(bank)
        if endGene not in valid:
            return -1
        seen = {startGene}
        q = deque([startGene])
        steps = 0
        while q:
            for _ in range(len(q)):
                gene = q.popleft()
                if gene == endGene:
                    return steps
                for i in range(len(gene)):
                    for ch in "ACGT":
                        nxt = gene[:i] + ch + gene[i + 1:]
                        if nxt in valid and nxt not in seen:
                            seen.add(nxt)
                            q.append(nxt)
            steps += 1
        return -1
```

**C++**

```cpp
class Solution {
public:
    int minMutation(string startGene, string endGene, vector<string>& bank) {
        unordered_set<string> valid(bank.begin(), bank.end());
        if (!valid.count(endGene)) return -1;
        unordered_set<string> seen{startGene};
        queue<string> q;
        q.push(startGene);
        for (int steps = 0; !q.empty(); ++steps) {
            for (int k = (int)q.size(); k > 0; --k) {
                string gene = q.front(); q.pop();
                if (gene == endGene) return steps;
                for (int i = 0; i < (int)gene.size(); ++i) {
                    char orig = gene[i];
                    for (char ch : string("ACGT")) {
                        gene[i] = ch;
                        if (valid.count(gene) && seen.insert(gene).second) q.push(gene);
                    }
                    gene[i] = orig;
                }
            }
        }
        return -1;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(B · L · 4 · L), B = bank size, L = 8 (each gene expands L·4 candidates of length L) |
| **Space** | O(B · L) |

**Pitfalls:** `startGene` need not be in the bank, but `endGene` must be (return `-1` early); an empty bank always gives `-1`; mark genes visited when enqueued to avoid duplicates.

---

### LC 934 · Shortest Bridge · Medium

> **Problem:** An n×n binary grid contains exactly two islands (4-directionally connected groups of `1`s). Return the minimum number of `0` cells that must be flipped to `1` to connect the two islands.

🔗 [https://leetcode.com/problems/shortest-bridge/](https://leetcode.com/problems/shortest-bridge/)

**Intuition:** Flood-fill one island, relabelling its cells to `2`, and seed a multi-source BFS with all of them. Expanding level by level across water, the first time the frontier touches a `1` the level number equals the number of water cells crossed, which is the minimum bridge length. Every cell is visited once in the fill and once in the BFS.

**Python**

```python
from collections import deque

class Solution:
    def shortestBridge(self, grid: list[list[int]]) -> int:
        n = len(grid)

        def neighbours(r: int, c: int):
            for x, y in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= x < n and 0 <= y < n:
                    yield x, y

        start = next((i, j) for i in range(n) for j in range(n) if grid[i][j] == 1)
        grid[start[0]][start[1]] = 2  # 2 = first island or water already reached
        stack, q = [start], deque([start])
        while stack:  # DFS flood fill; every island cell seeds the BFS
            r, c = stack.pop()
            for x, y in neighbours(r, c):
                if grid[x][y] == 1:
                    grid[x][y] = 2
                    stack.append((x, y))
                    q.append((x, y))
        steps = 0
        while q:  # multi-source BFS across water
            for _ in range(len(q)):
                r, c = q.popleft()
                for x, y in neighbours(r, c):
                    if grid[x][y] == 1:  # reached the second island
                        return steps
                    if grid[x][y] == 0:
                        grid[x][y] = 2
                        q.append((x, y))
            steps += 1
        return -1
```

**C++**

```cpp
class Solution {
public:
    int shortestBridge(vector<vector<int>>& grid) {
        int n = grid.size();
        int dirs[5] = {0, 1, 0, -1, 0};
        vector<pair<int, int>> stack;
        queue<pair<int, int>> q;
        for (int i = 0; i < n && stack.empty(); ++i)
            for (int j = 0; j < n; ++j)
                if (grid[i][j] == 1) {
                    grid[i][j] = 2;  // 2 = first island or water already reached
                    stack.push_back({i, j});
                    q.push({i, j});
                    break;
                }
        while (!stack.empty()) {  // DFS flood fill; every island cell seeds the BFS
            auto [r, c] = stack.back(); stack.pop_back();
            for (int d = 0; d < 4; ++d) {
                int x = r + dirs[d], y = c + dirs[d + 1];
                if (x >= 0 && x < n && y >= 0 && y < n && grid[x][y] == 1) {
                    grid[x][y] = 2;
                    stack.push_back({x, y});
                    q.push({x, y});
                }
            }
        }
        for (int steps = 0; !q.empty(); ++steps) {  // multi-source BFS across water
            for (int k = (int)q.size(); k > 0; --k) {
                auto [r, c] = q.front(); q.pop();
                for (int d = 0; d < 4; ++d) {
                    int x = r + dirs[d], y = c + dirs[d + 1];
                    if (x < 0 || x >= n || y < 0 || y >= n) continue;
                    if (grid[x][y] == 1) return steps;  // reached the second island
                    if (grid[x][y] == 0) {
                        grid[x][y] = 2;
                        q.push({x, y});
                    }
                }
            }
        }
        return -1;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n^2), n×n grid |
| **Space** | O(n^2) for the stack and queue |

**Pitfalls:** Seed the BFS with the whole first island, not one cell; the answer counts flipped water cells (adjacent islands would be 0, but they cannot be adjacent); break out of both loops after finding the first `1`; the grid is mutated.

---

### LC 310 · Minimum Height Trees · Medium

> **Problem:** Given a tree of `n` nodes labelled `0..n-1` as an undirected edge list, return all roots that produce a tree of minimum height (in any order).

🔗 [https://leetcode.com/problems/minimum-height-trees/](https://leetcode.com/problems/minimum-height-trees/)

**Intuition:** The optimal roots are the centre(s) of the tree's longest path, and there are at most two of them. Peel the tree like an onion: repeatedly remove all current leaves (degree 1) in one BFS layer, updating neighbour degrees; when at most 2 nodes remain, they are the answer. Brute force (BFS from every root) is O(n^2).

**Python**

```python
class Solution:
    def findMinHeightTrees(self, n: int, edges: list[list[int]]) -> list[int]:
        if n == 1:
            return [0]
        adj = [[] for _ in range(n)]
        deg = [0] * n
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)
            deg[a] += 1
            deg[b] += 1
        leaves = [i for i in range(n) if deg[i] == 1]
        remaining = n
        while remaining > 2:
            remaining -= len(leaves)
            nxt = []
            for u in leaves:
                for v in adj[u]:
                    deg[v] -= 1
                    if deg[v] == 1:  # v just became a leaf
                        nxt.append(v)
            leaves = nxt
        return leaves
```

**C++**

```cpp
class Solution {
public:
    vector<int> findMinHeightTrees(int n, vector<vector<int>>& edges) {
        if (n == 1) return {0};
        vector<vector<int>> adj(n);
        vector<int> deg(n, 0);
        for (auto& e : edges) {
            adj[e[0]].push_back(e[1]);
            adj[e[1]].push_back(e[0]);
            ++deg[e[0]];
            ++deg[e[1]];
        }
        vector<int> leaves;
        for (int i = 0; i < n; ++i)
            if (deg[i] == 1) leaves.push_back(i);
        int remaining = n;
        while (remaining > 2) {
            remaining -= leaves.size();
            vector<int> nxt;
            for (int u : leaves)
                for (int v : adj[u])
                    if (--deg[v] == 1) nxt.push_back(v);  // v just became a leaf
            leaves = move(nxt);
        }
        return leaves;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n) |
| **Space** | O(n) |

**Pitfalls:** `n == 1` has no edges and no leaves, so special-case it; stop at `remaining ≤ 2`, not when the leaf list is empty.

---

### LC 1514 · Path with Maximum Probability · Medium

> **Problem:** Given an undirected graph of `n` nodes where edge `i` has success probability `succProb[i]`, return the maximum probability of a path from `start_node` to `end_node`, or `0` if no path exists.

🔗 [https://leetcode.com/problems/path-with-maximum-probability/](https://leetcode.com/problems/path-with-maximum-probability/)

**Intuition:** Path probability is a product of factors in [0, 1], so extending a path never increases it; that monotonicity is exactly what Dijkstra needs. Run Dijkstra with a max-heap on probability: the first time `end_node` is popped its probability is optimal. (Equivalently, minimise the sum of `-log p`.)

**Python**

```python
import heapq

class Solution:
    def maxProbability(self, n: int, edges: list[list[int]], succProb: list[float],
                       start_node: int, end_node: int) -> float:
        adj = [[] for _ in range(n)]
        for (a, b), p in zip(edges, succProb):
            adj[a].append((b, p))
            adj[b].append((a, p))
        best = [0.0] * n
        best[start_node] = 1.0
        heap = [(-1.0, start_node)]  # negate for a max-heap
        while heap:
            p, u = heapq.heappop(heap)
            p = -p
            if u == end_node:
                return p
            if p < best[u]:  # stale entry
                continue
            for v, w in adj[u]:
                if p * w > best[v]:
                    best[v] = p * w
                    heapq.heappush(heap, (-best[v], v))
        return 0.0
```

**C++**

```cpp
class Solution {
public:
    double maxProbability(int n, vector<vector<int>>& edges, vector<double>& succProb,
                          int start_node, int end_node) {
        vector<vector<pair<int, double>>> adj(n);
        for (int i = 0; i < (int)edges.size(); ++i) {
            adj[edges[i][0]].push_back({edges[i][1], succProb[i]});
            adj[edges[i][1]].push_back({edges[i][0], succProb[i]});
        }
        vector<double> best(n, 0.0);
        best[start_node] = 1.0;
        priority_queue<pair<double, int>> pq;  // max-heap on probability
        pq.push({1.0, start_node});
        while (!pq.empty()) {
            auto [p, u] = pq.top(); pq.pop();
            if (u == end_node) return p;
            if (p < best[u]) continue;  // stale entry
            for (auto [v, w] : adj[u])
                if (p * w > best[v]) {
                    best[v] = p * w;
                    pq.push({best[v], v});
                }
        }
        return 0.0;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O((V + E) log E), V = n nodes, E = edges |
| **Space** | O(V + E) |

**Pitfalls:** The graph is undirected (add both directions); a min-heap or plain BFS gives wrong answers; Bellman-Ford style relaxation works but is O(V·E).

---

## 8. DFS (Depth-First Search)

Template and pitfalls: [LeetCode Patterns §8 DFS (Depth-First Search)](../computer-science/LeetCode_Patterns.md#8-dfs-depth-first-search)

### LC 100 · Same Tree · Easy

> **Problem:** Given the roots of two binary trees `p` and `q`, return whether they are structurally identical with equal node values.

🔗 [https://leetcode.com/problems/same-tree/](https://leetcode.com/problems/same-tree/)

**Intuition:** Two trees are equal iff their roots match and their left and right subtrees are pairwise equal. If either node is null, they are equal only when both are null. Each node pair is compared once.

**Python**

```python
class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if not p or not q:
            return p is q  # equal only if both are None
        return p.val == q.val and self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
```

**C++**

```cpp
class Solution {
public:
    bool isSameTree(TreeNode* p, TreeNode* q) {
        if (!p || !q) return p == q;  // equal only if both are null
        return p->val == q->val && isSameTree(p->left, q->left) && isSameTree(p->right, q->right);
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(min(n, m)), n and m = node counts |
| **Space** | O(h), h = height of the smaller tree |

**Pitfalls:** Comparing only in-order (or any single) traversal is wrong because different shapes can share a traversal; check nulls before touching `.val`.

---

### LC 101 · Symmetric Tree · Easy

> **Problem:** Given the root of a binary tree, return whether it is a mirror of itself (symmetric around its centre).

🔗 [https://leetcode.com/problems/symmetric-tree/](https://leetcode.com/problems/symmetric-tree/)

**Intuition:** A tree is symmetric iff its left and right subtrees are mirrors. Two trees `a`, `b` are mirrors iff their roots match, `a.left` mirrors `b.right`, and `a.right` mirrors `b.left`. The follow-up asks for an iterative version: push node pairs onto a queue in the same crossed order.

**Python**

```python
class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        def mirror(a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
            if not a or not b:
                return a is b
            return a.val == b.val and mirror(a.left, b.right) and mirror(a.right, b.left)
        return not root or mirror(root.left, root.right)
```

**C++**

```cpp
class Solution {
    bool mirror(TreeNode* a, TreeNode* b) {
        if (!a || !b) return a == b;
        return a->val == b->val && mirror(a->left, b->right) && mirror(a->right, b->left);
    }
public:
    bool isSymmetric(TreeNode* root) {
        return !root || mirror(root->left, root->right);
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n), n = number of nodes |
| **Space** | O(h), h = tree height |

**Pitfalls:** Comparing `a.left` with `b.left` checks equality, not mirroring; a tree with null in matching positions (e.g. `[1,2,2,null,3,null,3]`) is not symmetric.

---

### LC 110 · Balanced Binary Tree · Easy

> **Problem:** Given a binary tree, return whether it is height-balanced: for every node, the heights of its left and right subtrees differ by at most 1.

🔗 [https://leetcode.com/problems/balanced-binary-tree/](https://leetcode.com/problems/balanced-binary-tree/)

**Intuition:** Calling a separate `height()` from every node is O(n^2) on skewed trees. Instead compute heights bottom-up in one post-order pass and return a sentinel `-1` as soon as any subtree is unbalanced, short-circuiting the rest of the work.

**Python**

```python
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        def height(node: Optional[TreeNode]) -> int:  # -1 means "unbalanced"
            if not node:
                return 0
            left = height(node.left)
            if left < 0:
                return -1
            right = height(node.right)
            if right < 0 or abs(left - right) > 1:
                return -1
            return 1 + max(left, right)
        return height(root) >= 0
```

**C++**

```cpp
class Solution {
    int height(TreeNode* node) {  // -1 means "unbalanced"
        if (!node) return 0;
        int left = height(node->left);
        if (left < 0) return -1;
        int right = height(node->right);
        if (right < 0 || abs(left - right) > 1) return -1;
        return 1 + max(left, right);
    }
public:
    bool isBalanced(TreeNode* root) {
        return height(root) >= 0;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n), n = number of nodes |
| **Space** | O(h), h = tree height |

**Pitfalls:** Checking only the root's subtree heights misses deeper imbalance; a skewed tree of 5000 nodes recurses 5000 deep, beyond Python's default recursion limit of 1000.

---

### LC 572 · Subtree of Another Tree · Easy

> **Problem:** Given the roots of two binary trees `root` and `subRoot`, return whether `root` contains a subtree (a node and all its descendants) with the same structure and values as `subRoot`.

🔗 [https://leetcode.com/problems/subtree-of-another-tree/](https://leetcode.com/problems/subtree-of-another-tree/)

**Intuition:** DFS over `root`, and at each node run the Same Tree check against `subRoot`; mismatches usually fail within a few nodes, so this is the expected interview answer. For a guaranteed O(m + n), serialise both trees with explicit null markers and delimiters and run KMP (or compare Merkle-style subtree hashes).

**Python**

```python
class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        def same(a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
            if not a or not b:
                return a is b
            return a.val == b.val and same(a.left, b.left) and same(a.right, b.right)

        def dfs(node: Optional[TreeNode]) -> bool:
            if not node:
                return False
            return same(node, subRoot) or dfs(node.left) or dfs(node.right)

        return dfs(root)
```

**C++**

```cpp
class Solution {
    bool same(TreeNode* a, TreeNode* b) {
        if (!a || !b) return a == b;
        return a->val == b->val && same(a->left, b->left) && same(a->right, b->right);
    }
public:
    bool isSubtree(TreeNode* root, TreeNode* subRoot) {
        if (!root) return false;
        return same(root, subRoot) || isSubtree(root->left, subRoot) || isSubtree(root->right, subRoot);
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(m·n), m and n = node counts of `root` and `subRoot` |
| **Space** | O(h), h = height of `root` |

**Pitfalls:** A matching subtree must include all descendants (`[4,1,2,null,null,0]` does not contain `[4,1,2]`); naive string serialisation without null markers and delimiters gives false positives (`"12"` contains `"2"`).

---

### LC 235 · Lowest Common Ancestor of a Binary Search Tree · Medium

> **Problem:** Given a BST and two distinct nodes `p` and `q` that both exist in it, return their lowest common ancestor (a node may be a descendant of itself).

🔗 [https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/)

**Intuition:** BST ordering tells you which side each target is on. If both values are smaller than the current node, the LCA is in the left subtree; if both are larger, in the right. Otherwise the paths split here (or the current node is one of them), so it is the LCA. Walking one root-to-node path needs no recursion.

**Python**

```python
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        node = root
        while node:
            if p.val < node.val and q.val < node.val:
                node = node.left
            elif p.val > node.val and q.val > node.val:
                node = node.right
            else:
                return node  # p and q split here (or node is one of them)
        return None
```

**C++**

```cpp
class Solution {
public:
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        TreeNode* node = root;
        while (node) {
            if (p->val < node->val && q->val < node->val)
                node = node->left;
            else if (p->val > node->val && q->val > node->val)
                node = node->right;
            else
                return node;  // p and q split here (or node is one of them)
        }
        return nullptr;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(h), h = tree height |
| **Space** | O(1) |

**Pitfalls:** Do not use the general binary-tree LCA (O(n)) when BST order is available; when `p` is an ancestor of `q`, `p` itself is the answer.

---

### LC 417 · Pacific Atlantic Water Flow · Medium

> **Problem:** An m×n grid of heights borders the Pacific on its top and left edges and the Atlantic on its bottom and right edges. Water flows from a cell to a 4-directional neighbour of equal or lower height. Return all cells from which water can reach both oceans.

🔗 [https://leetcode.com/problems/pacific-atlantic-water-flow/](https://leetcode.com/problems/pacific-atlantic-water-flow/)

**Intuition:** Simulating flow from every cell is O((m·n)^2). Reverse the direction: DFS from each ocean's border cells moving only to neighbours of equal or greater height marks every cell that can drain into that ocean. The answer is the intersection of the two reachable sets, and each search visits every cell at most once.

**Python**

```python
class Solution:
    def pacificAtlantic(self, heights: list[list[int]]) -> list[list[int]]:
        m, n = len(heights), len(heights[0])

        def reach(starts: list[tuple[int, int]]) -> set[tuple[int, int]]:
            seen = set(starts)
            stack = list(seen)
            while stack:
                r, c = stack.pop()
                for x, y in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    # move uphill (reverse of water flow)
                    if 0 <= x < m and 0 <= y < n and (x, y) not in seen and heights[x][y] >= heights[r][c]:
                        seen.add((x, y))
                        stack.append((x, y))
            return seen

        pacific = reach([(0, j) for j in range(n)] + [(i, 0) for i in range(m)])
        atlantic = reach([(m - 1, j) for j in range(n)] + [(i, n - 1) for i in range(m)])
        return [[r, c] for r in range(m) for c in range(n) if (r, c) in pacific and (r, c) in atlantic]
```

**C++**

```cpp
class Solution {
public:
    vector<vector<int>> pacificAtlantic(vector<vector<int>>& heights) {
        int m = heights.size(), n = heights[0].size();
        int dirs[5] = {0, 1, 0, -1, 0};
        auto reach = [&](vector<pair<int, int>> stack) {
            vector<vector<char>> seen(m, vector<char>(n, 0));
            for (auto [r, c] : stack) seen[r][c] = 1;
            while (!stack.empty()) {
                auto [r, c] = stack.back(); stack.pop_back();
                for (int d = 0; d < 4; ++d) {
                    int x = r + dirs[d], y = c + dirs[d + 1];
                    // move uphill (reverse of water flow)
                    if (x >= 0 && x < m && y >= 0 && y < n && !seen[x][y] && heights[x][y] >= heights[r][c]) {
                        seen[x][y] = 1;
                        stack.push_back({x, y});
                    }
                }
            }
            return seen;
        };
        vector<pair<int, int>> pacStart, atlStart;
        for (int j = 0; j < n; ++j) {
            pacStart.push_back({0, j});
            atlStart.push_back({m - 1, j});
        }
        for (int i = 0; i < m; ++i) {
            pacStart.push_back({i, 0});
            atlStart.push_back({i, n - 1});
        }
        auto pacific = reach(pacStart), atlantic = reach(atlStart);
        vector<vector<int>> res;
        for (int r = 0; r < m; ++r)
            for (int c = 0; c < n; ++c)
                if (pacific[r][c] && atlantic[r][c]) res.push_back({r, c});
        return res;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(m·n), m×n grid |
| **Space** | O(m·n) |

**Pitfalls:** Flow condition is "equal or lower", so the reverse search uses `>=`; corner cells belong to both oceans' borders; recursive DFS on a 200×200 grid overflows Python's default stack.

---

### LC 133 · Clone Graph · Medium

> **Problem:** Given a reference to a node in a connected undirected graph (each node has `val` and a list of `neighbors`), return a deep copy of the graph. The input may be null.

🔗 [https://leetcode.com/problems/clone-graph/](https://leetcode.com/problems/clone-graph/)

**Intuition:** DFS the graph while keeping a map from each original node to its clone. Register the clone in the map before recursing into neighbours: cycles (every undirected edge is one) then resolve to the existing copy instead of looping forever, and every node is copied exactly once.

**Python**

```python
# Node: val, neighbors
class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        clones = {}

        def dfs(u: 'Node') -> 'Node':
            if u in clones:
                return clones[u]
            copy = Node(u.val)
            clones[u] = copy  # register before recursing so cycles terminate
            copy.neighbors = [dfs(v) for v in u.neighbors]
            return copy

        return dfs(node) if node else None
```

**C++**

```cpp
class Solution {
    unordered_map<Node*, Node*> clones;
public:
    Node* cloneGraph(Node* node) {
        if (!node) return nullptr;
        if (auto it = clones.find(node); it != clones.end()) return it->second;
        Node* copy = new Node(node->val);
        clones[node] = copy;  // register before recursing so cycles terminate
        for (Node* v : node->neighbors) copy->neighbors.push_back(cloneGraph(v));
        return copy;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(V + E), V nodes, E edges |
| **Space** | O(V) for the map and recursion |

**Pitfalls:** Inserting into the map after recursing causes infinite recursion; key the map by node identity, not `val`; return null for null input.

---

### LC 1448 · Count Good Nodes in Binary Tree · Medium

> **Problem:** A node X is good if no node on the path from the root to X has a value greater than X. Return the number of good nodes in the binary tree (up to 10^5 nodes).

🔗 [https://leetcode.com/problems/count-good-nodes-in-binary-tree/](https://leetcode.com/problems/count-good-nodes-in-binary-tree/)

**Intuition:** Carry the maximum value seen along the current root-to-node path down the DFS. A node is good iff its value is at least that maximum; it then becomes the new maximum for its children. An explicit stack of `(node, path_max)` pairs avoids recursion-depth limits on skewed trees.

**Python**

```python
class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        count = 0
        stack = [(root, root.val)]  # (node, max value on the path above it)
        while stack:
            node, best = stack.pop()
            if node.val >= best:
                count += 1
                best = node.val
            for child in (node.left, node.right):
                if child:
                    stack.append((child, best))
        return count
```

**C++**

```cpp
class Solution {
public:
    int goodNodes(TreeNode* root) {
        int count = 0;
        vector<pair<TreeNode*, int>> stack{{root, root->val}};  // (node, max value on the path above it)
        while (!stack.empty()) {
            auto [node, best] = stack.back(); stack.pop_back();
            if (node->val >= best) {
                ++count;
                best = node->val;
            }
            if (node->left) stack.push_back({node->left, best});
            if (node->right) stack.push_back({node->right, best});
        }
        return count;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n), n = number of nodes |
| **Space** | O(h), h = tree height (explicit stack) |

**Pitfalls:** Use `>=` (equal to the path max still counts); the root is always good; recursive Python DFS hits the recursion limit on a 10^5-node chain.

---

### LC 114 · Flatten Binary Tree to Linked List · Medium

> **Problem:** Flatten a binary tree in place into a "linked list" that uses `right` pointers in pre-order sequence, with every `left` pointer set to null.

🔗 [https://leetcode.com/problems/flatten-binary-tree-to-linked-list/](https://leetcode.com/problems/flatten-binary-tree-to-linked-list/)

**Intuition:** In pre-order, a node's right subtree comes right after the last node of its left subtree, which is the rightmost node of the left subtree. So for each node with a left child, splice the right subtree onto that rightmost node, move the left subtree to the right, and continue down `right`. This Morris-style walk meets the O(1)-extra-space follow-up; each right-spine edge is walked at most once in total.

**Python**

```python
class Solution:
    def flatten(self, root: Optional[TreeNode]) -> None:
        node = root
        while node:
            if node.left:
                tail = node.left
                while tail.right:  # last pre-order node of the left subtree
                    tail = tail.right
                tail.right = node.right
                node.right = node.left
                node.left = None
            node = node.right
```

**C++**

```cpp
class Solution {
public:
    void flatten(TreeNode* root) {
        TreeNode* node = root;
        while (node) {
            if (node->left) {
                TreeNode* tail = node->left;
                while (tail->right) tail = tail->right;  // last pre-order node of the left subtree
                tail->right = node->right;
                node->right = node->left;
                node->left = nullptr;
            }
            node = node->right;
        }
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n), n = number of nodes |
| **Space** | O(1) |

**Pitfalls:** Forgetting `node.left = None` leaves a cycle-like structure the judge rejects; the recursive "reverse post-order with a `prev` pointer" variant uses O(h) stack.

---

### LC 116 · Populating Next Right Pointers in Each Node · Medium

> **Problem:** Given a perfect binary tree (all leaves on the same level, every parent has two children) whose nodes have a `next` pointer, set each `next` to the node immediately to its right on the same level, or null if none. Follow-up: constant extra space (recursion stack is allowed).

🔗 [https://leetcode.com/problems/populating-next-right-pointers-in-each-node/](https://leetcode.com/problems/populating-next-right-pointers-in-each-node/)

**Intuition:** For a node with children, `left.next = right` always, and `right.next = node.next.left` when `node` has a right neighbour. Pre-order DFS guarantees `node.next` is already set before `node` is visited, because it was wired while visiting `node`'s parent. Recursion depth is the tree height, log n for a perfect tree; the iterative alternative walks each level via the `next` pointers of the level above.

**Python**

```python
# Node: val, left, right, next
class Solution:
    def connect(self, root: 'Optional[Node]') -> 'Optional[Node]':
        if root and root.left:
            root.left.next = root.right
            if root.next:  # wired when root's parent was visited
                root.right.next = root.next.left
            self.connect(root.left)
            self.connect(root.right)
        return root
```

**C++**

```cpp
class Solution {
public:
    Node* connect(Node* root) {
        if (root && root->left) {
            root->left->next = root->right;
            if (root->next)  // wired when root's parent was visited
                root->right->next = root->next->left;
            connect(root->left);
            connect(root->right);
        }
        return root;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n), n = number of nodes |
| **Space** | O(log n) recursion stack (perfect tree) |

**Pitfalls:** Relies on the tree being perfect (LC 117 drops that guarantee); handle `root == null`; a queue-based BFS works but uses O(n) space, failing the follow-up.

---

### LC 437 · Path Sum III · Medium

> **Problem:** Given a binary tree and `targetSum`, return the number of downward paths (from any node to any descendant, not necessarily root or leaf) whose values sum to `targetSum`. Node values can be negative and up to 10^9 in absolute value.

🔗 [https://leetcode.com/problems/path-sum-iii/](https://leetcode.com/problems/path-sum-iii/)

**Intuition:** Along the current root-to-node path, a downward path ending at the node sums to `target` iff some earlier prefix sum equals `cur - target`. Keep a hash map of prefix-sum counts for the active path only (increment on entry, decrement on exit), turning the O(n·h) "start a DFS from every node" brute force into one O(n) pass. It is Subarray Sum Equals K on root-to-node paths.

**Python**

```python
from collections import defaultdict

class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        prefix = defaultdict(int)
        prefix[0] = 1  # empty prefix, so paths starting at the root count

        def dfs(node: Optional[TreeNode], cur: int) -> int:
            if not node:
                return 0
            cur += node.val
            res = prefix[cur - targetSum]
            prefix[cur] += 1
            res += dfs(node.left, cur) + dfs(node.right, cur)
            prefix[cur] -= 1  # backtrack: node leaves the active path
            return res

        return dfs(root, 0)
```

**C++**

```cpp
class Solution {
    unordered_map<long long, int> prefix;
    long long target;

    int dfs(TreeNode* node, long long cur) {
        if (!node) return 0;
        cur += node->val;
        auto it = prefix.find(cur - target);
        int res = it == prefix.end() ? 0 : it->second;
        ++prefix[cur];
        res += dfs(node->left, cur) + dfs(node->right, cur);
        --prefix[cur];  // backtrack: node leaves the active path
        return res;
    }
public:
    int pathSum(TreeNode* root, int targetSum) {
        prefix = {{0, 1}};  // empty prefix, so paths starting at the root count
        target = targetSum;
        return dfs(root, 0);
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n), n = number of nodes |
| **Space** | O(n) for the map and recursion |

**Pitfalls:** Prefix sums overflow `int` in C++ (values up to 10^9 over 1000 nodes), so use `long long`; look up `cur - target` before inserting `cur` or `target == 0` counts empty paths; forgetting to decrement leaks sums into sibling subtrees.

---

### LC 450 · Delete Node in a BST · Medium

> **Problem:** Given the root of a BST and a `key`, delete the node with that key (if present) and return the possibly updated root, keeping the BST property.

🔗 [https://leetcode.com/problems/delete-node-in-a-bst/](https://leetcode.com/problems/delete-node-in-a-bst/)

**Intuition:** Search down by BST order. When the node is found: with zero or one child, replace it by that child; with two children, copy in the value of its in-order successor (the leftmost node of the right subtree) and recursively delete the successor from the right subtree, where it has no left child. The work is one root-to-leaf walk.

**Python**

```python
class Solution:
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        if not root:
            return None
        if key < root.val:
            root.left = self.deleteNode(root.left, key)
        elif key > root.val:
            root.right = self.deleteNode(root.right, key)
        else:
            if not root.left:
                return root.right
            if not root.right:
                return root.left
            succ = root.right  # in-order successor: leftmost of right subtree
            while succ.left:
                succ = succ.left
            root.val = succ.val
            root.right = self.deleteNode(root.right, succ.val)
        return root
```

**C++**

```cpp
class Solution {
public:
    TreeNode* deleteNode(TreeNode* root, int key) {
        if (!root) return nullptr;
        if (key < root->val) {
            root->left = deleteNode(root->left, key);
        } else if (key > root->val) {
            root->right = deleteNode(root->right, key);
        } else {
            if (!root->left) return root->right;
            if (!root->right) return root->left;
            TreeNode* succ = root->right;  // in-order successor: leftmost of right subtree
            while (succ->left) succ = succ->left;
            root->val = succ->val;
            root->right = deleteNode(root->right, succ->val);
        }
        return root;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(h), h = tree height |
| **Space** | O(h) recursion stack |

**Pitfalls:** Always reassign the returned subtree to `root.left` / `root.right`; deleting the root or a missing key must still work; a skewed 10^4-node BST exceeds Python's default recursion limit.

---

### LC 695 · Max Area of Island · Medium

> **Problem:** Given an m×n binary grid where `1` is land, return the area (cell count) of the largest 4-directionally connected island, or 0 if there is none.

🔗 [https://leetcode.com/problems/max-area-of-island/](https://leetcode.com/problems/max-area-of-island/)

**Intuition:** Scan every cell; each unvisited land cell starts a flood fill that counts its island's cells. Sinking cells to `0` as they are pushed doubles as the visited set, so every cell is touched O(1) times overall. An explicit stack avoids deep recursion on a 50×50 all-land grid.

**Python**

```python
class Solution:
    def maxAreaOfIsland(self, grid: list[list[int]]) -> int:
        m, n = len(grid), len(grid[0])
        best = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] != 1:
                    continue
                grid[i][j] = 0  # sink = mark visited
                stack, area = [(i, j)], 0
                while stack:
                    r, c = stack.pop()
                    area += 1
                    for x, y in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                        if 0 <= x < m and 0 <= y < n and grid[x][y] == 1:
                            grid[x][y] = 0
                            stack.append((x, y))
                best = max(best, area)
        return best
```

**C++**

```cpp
class Solution {
public:
    int maxAreaOfIsland(vector<vector<int>>& grid) {
        int m = grid.size(), n = grid[0].size(), best = 0;
        int dirs[5] = {0, 1, 0, -1, 0};
        for (int i = 0; i < m; ++i)
            for (int j = 0; j < n; ++j) {
                if (grid[i][j] != 1) continue;
                grid[i][j] = 0;  // sink = mark visited
                vector<pair<int, int>> stack{{i, j}};
                int area = 0;
                while (!stack.empty()) {
                    auto [r, c] = stack.back(); stack.pop_back();
                    ++area;
                    for (int d = 0; d < 4; ++d) {
                        int x = r + dirs[d], y = c + dirs[d + 1];
                        if (x >= 0 && x < m && y >= 0 && y < n && grid[x][y] == 1) {
                            grid[x][y] = 0;
                            stack.push_back({x, y});
                        }
                    }
                }
                best = max(best, area);
            }
        return best;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(m·n), m×n grid |
| **Space** | O(m·n) worst-case stack |

**Pitfalls:** Mark cells when pushing, not when popping, or a cell is counted twice; the solution mutates `grid` (copy it first if the caller needs it); diagonal neighbours do not connect.

---

### LC 863 · All Nodes Distance K in Binary Tree · Medium

> **Problem:** Given the root of a binary tree with unique values, a `target` node in it, and an integer `k`, return the values of all nodes exactly `k` edges away from `target`, in any order.

🔗 [https://leetcode.com/problems/all-nodes-distance-k-in-binary-tree/](https://leetcode.com/problems/all-nodes-distance-k-in-binary-tree/)

**Intuition:** Distance can go up through ancestors, so treat the tree as an undirected graph. One DFS records each node's parent; then a BFS from `target` over `left`, `right`, `parent` edges, `k` levels deep, yields the frontier at distance `k`. A visited set stops walking back the way you came.

**Python**

```python
class Solution:
    def distanceK(self, root: TreeNode, target: TreeNode, k: int) -> list[int]:
        parent = {root: None}
        stack = [root]
        while stack:  # DFS to record parent pointers
            node = stack.pop()
            for child in (node.left, node.right):
                if child:
                    parent[child] = node
                    stack.append(child)
        seen = {target}
        frontier = [target]
        for _ in range(k):  # BFS k levels outward
            nxt = []
            for node in frontier:
                for nb in (node.left, node.right, parent[node]):
                    if nb and nb not in seen:
                        seen.add(nb)
                        nxt.append(nb)
            frontier = nxt
        return [node.val for node in frontier]
```

**C++**

```cpp
class Solution {
public:
    vector<int> distanceK(TreeNode* root, TreeNode* target, int k) {
        unordered_map<TreeNode*, TreeNode*> parent{{root, nullptr}};
        vector<TreeNode*> stack{root};
        while (!stack.empty()) {  // DFS to record parent pointers
            TreeNode* node = stack.back(); stack.pop_back();
            for (TreeNode* child : {node->left, node->right})
                if (child) {
                    parent[child] = node;
                    stack.push_back(child);
                }
        }
        unordered_set<TreeNode*> seen{target};
        vector<TreeNode*> frontier{target};
        for (int step = 0; step < k; ++step) {  // BFS k levels outward
            vector<TreeNode*> nxt;
            for (TreeNode* node : frontier)
                for (TreeNode* nb : {node->left, node->right, parent[node]})
                    if (nb && seen.insert(nb).second) nxt.push_back(nb);
            frontier = move(nxt);
        }
        vector<int> res;
        for (TreeNode* node : frontier) res.push_back(node->val);
        return res;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n), n = number of nodes |
| **Space** | O(n) for parent map and visited set |

**Pitfalls:** `k == 0` returns `[target.val]`; without the visited set the BFS bounces between child and parent; `k` larger than the tree's reach returns `[]`.

---

## 10. Subsets / Backtracking

Template and pitfalls: [LeetCode Patterns §10 Subsets / Backtracking](../computer-science/LeetCode_Patterns.md#10-subsets--backtracking)

### LC 22 · Generate Parentheses · Medium

> **Problem:** Given `n` pairs of parentheses (1 ≤ n ≤ 8), generate all combinations of well-formed parentheses.

🔗 [https://leetcode.com/problems/generate-parentheses/](https://leetcode.com/problems/generate-parentheses/)

**Intuition:** Build the string left to right while tracking how many `(` and `)` are used. You may add `(` while `open < n` and `)` while `close < open`; these two rules keep every prefix valid, so no invalid string is ever generated. The number of results is the n-th Catalan number.

**Python**

```python
class Solution:
    def generateParenthesis(self, n: int) -> list[str]:
        res, path = [], []

        def dfs(open_: int, close: int) -> None:
            if len(path) == 2 * n:
                res.append("".join(path))
                return
            if open_ < n:
                path.append("(")
                dfs(open_ + 1, close)
                path.pop()
            if close < open_:
                path.append(")")
                dfs(open_, close + 1)
                path.pop()

        dfs(0, 0)
        return res
```

**C++**

```cpp
class Solution {
    vector<string> res;
    string path;

    void dfs(int n, int open, int close) {
        if ((int)path.size() == 2 * n) {
            res.push_back(path);
            return;
        }
        if (open < n) {
            path.push_back('(');
            dfs(n, open + 1, close);
            path.pop_back();
        }
        if (close < open) {
            path.push_back(')');
            dfs(n, open, close + 1);
            path.pop_back();
        }
    }

public:
    vector<string> generateParenthesis(int n) {
        dfs(n, 0, 0);
        return res;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(4^n / sqrt(n)): Catalan(n) results, each of length 2n |
| **Space** | O(n) recursion, excluding the output |

**Pitfalls:** The close condition is `close < open`, not `close < n`; generating all 2^(2n) strings and filtering works but is needlessly slow.

---

### LC 17 · Letter Combinations of a Phone Number · Medium

> **Problem:** Given a string of digits `2-9` (length 0 to 4), return all letter combinations the number could represent using the classic phone keypad mapping, in any order. An empty input yields an empty list.

🔗 [https://leetcode.com/problems/letter-combinations-of-a-phone-number/](https://leetcode.com/problems/letter-combinations-of-a-phone-number/)

**Intuition:** This is a Cartesian product: each position chooses one of 3-4 letters independently. Backtrack position by position, appending a letter, recursing, then popping it. Every leaf is a valid answer, so the work is proportional to the output size times its length.

**Python**

```python
class Solution:
    def letterCombinations(self, digits: str) -> list[str]:
        if not digits:
            return []
        keys = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
                "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
        res, path = [], []

        def dfs(i: int) -> None:
            if i == len(digits):
                res.append("".join(path))
                return
            for ch in keys[digits[i]]:
                path.append(ch)
                dfs(i + 1)
                path.pop()

        dfs(0)
        return res
```

**C++**

```cpp
class Solution {
    const vector<string> keys = {"", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"};
    vector<string> res;
    string path;

    void dfs(const string& digits, int i) {
        if (i == (int)digits.size()) {
            res.push_back(path);
            return;
        }
        for (char ch : keys[digits[i] - '0']) {
            path.push_back(ch);
            dfs(digits, i + 1);
            path.pop_back();
        }
    }

public:
    vector<string> letterCombinations(string digits) {
        if (digits.empty()) return {};
        dfs(digits, 0);
        return res;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(4^n · n), n = number of digits |
| **Space** | O(n) recursion, excluding the output |

**Pitfalls:** Empty `digits` must return `[]`, not `[""]`; digits 7 and 9 map to four letters, not three.

---

### LC 77 · Combinations · Medium

> **Problem:** Given integers `n` and `k` (1 ≤ k ≤ n ≤ 20), return all combinations of `k` numbers chosen from `1..n`, in any order.

🔗 [https://leetcode.com/problems/combinations/](https://leetcode.com/problems/combinations/)

**Intuition:** Choose numbers in increasing order so each combination is produced exactly once: after picking `i`, the next pick starts at `i + 1`. Prune when there are not enough numbers left: with `need = k - len(path)` still to pick, the current pick can be at most `n - need + 1`.

**Python**

```python
class Solution:
    def combine(self, n: int, k: int) -> list[list[int]]:
        res, path = [], []

        def dfs(start: int) -> None:
            need = k - len(path)
            if need == 0:
                res.append(path[:])
                return
            for i in range(start, n - need + 2):  # leave room for the rest
                path.append(i)
                dfs(i + 1)
                path.pop()

        dfs(1)
        return res
```

**C++**

```cpp
class Solution {
    vector<vector<int>> res;
    vector<int> path;

    void dfs(int n, int k, int start) {
        int need = k - (int)path.size();
        if (need == 0) {
            res.push_back(path);
            return;
        }
        for (int i = start; i <= n - need + 1; ++i) {  // leave room for the rest
            path.push_back(i);
            dfs(n, k, i + 1);
            path.pop_back();
        }
    }

public:
    vector<vector<int>> combine(int n, int k) {
        dfs(n, k, 1);
        return res;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(C(n, k) · k) |
| **Space** | O(k) recursion, excluding the output |

**Pitfalls:** Append a copy of `path` (Python `path[:]`), not the list itself; the pruning bound is off-by-one prone, so check it with `n = k`.

---

### LC 90 · Subsets II · Medium

> **Problem:** Given an integer array `nums` that may contain duplicates (length ≤ 10), return all possible subsets without duplicate subsets, in any order.

🔗 [https://leetcode.com/problems/subsets-ii/](https://leetcode.com/problems/subsets-ii/)

**Intuition:** Sort so equal values are adjacent. In the standard "every node is a subset" backtracking, at a given depth only the first copy of a value may be chosen as the next element (`i > start and nums[i] == nums[i-1]` is skipped); later copies would rebuild the same subsets. Deeper levels may still take the next copy, which is how `[2, 2]` arises.

**Python**

```python
class Solution:
    def subsetsWithDup(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        res, path = [], []

        def dfs(start: int) -> None:
            res.append(path[:])
            for i in range(start, len(nums)):
                if i > start and nums[i] == nums[i - 1]:
                    continue  # same value already tried at this depth
                path.append(nums[i])
                dfs(i + 1)
                path.pop()

        dfs(0)
        return res
```

**C++**

```cpp
class Solution {
    vector<vector<int>> res;
    vector<int> path;

    void dfs(const vector<int>& nums, int start) {
        res.push_back(path);
        for (int i = start; i < (int)nums.size(); ++i) {
            if (i > start && nums[i] == nums[i - 1]) continue;  // same value already tried at this depth
            path.push_back(nums[i]);
            dfs(nums, i + 1);
            path.pop_back();
        }
    }

public:
    vector<vector<int>> subsetsWithDup(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        dfs(nums, 0);
        return res;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n · 2^n), n = len(nums) |
| **Space** | O(n) recursion, excluding the output |

**Pitfalls:** Forgetting to sort; using `i > 0` instead of `i > start` wrongly drops subsets like `[2, 2]`.

---

### LC 40 · Combination Sum II · Medium

> **Problem:** Given `candidates` (may contain duplicates, values 1-50, length ≤ 100) and a `target` ≤ 30, return all unique combinations that sum to `target`, where each candidate is used at most once.

🔗 [https://leetcode.com/problems/combination-sum-ii/](https://leetcode.com/problems/combination-sum-ii/)

**Intuition:** Same skeleton as Subsets II: sort, recurse with `i + 1` (each element used once), and skip equal values at the same depth to avoid duplicate combinations. Because the array is sorted and values are positive, once `candidates[i]` exceeds the remaining target the whole rest of the loop can be cut with `break`.

**Python**

```python
class Solution:
    def combinationSum2(self, candidates: list[int], target: int) -> list[list[int]]:
        candidates.sort()
        res, path = [], []

        def dfs(start: int, remain: int) -> None:
            if remain == 0:
                res.append(path[:])
                return
            for i in range(start, len(candidates)):
                if i > start and candidates[i] == candidates[i - 1]:
                    continue
                if candidates[i] > remain:
                    break  # sorted: every later value is too big as well
                path.append(candidates[i])
                dfs(i + 1, remain - candidates[i])
                path.pop()

        dfs(0, target)
        return res
```

**C++**

```cpp
class Solution {
    vector<vector<int>> res;
    vector<int> path;

    void dfs(const vector<int>& c, int start, int remain) {
        if (remain == 0) {
            res.push_back(path);
            return;
        }
        for (int i = start; i < (int)c.size(); ++i) {
            if (i > start && c[i] == c[i - 1]) continue;
            if (c[i] > remain) break;  // sorted: every later value is too big as well
            path.push_back(c[i]);
            dfs(c, i + 1, remain - c[i]);
            path.pop_back();
        }
    }

public:
    vector<vector<int>> combinationSum2(vector<int>& candidates, int target) {
        sort(candidates.begin(), candidates.end());
        dfs(candidates, 0, target);
        return res;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(2^n · n) worst case, n = len(candidates); pruning makes it far smaller in practice |
| **Space** | O(n) recursion, excluding the output |

**Pitfalls:** Recursing with `i` instead of `i + 1` reuses elements (that is LC 39); deduplicating results with a set afterwards is correct but can time out.

---

### LC 131 · Palindrome Partitioning · Medium

> **Problem:** Given a string `s` (length ≤ 16, lowercase letters), partition it so that every substring of the partition is a palindrome, and return all such partitions.

🔗 [https://leetcode.com/problems/palindrome-partitioning/](https://leetcode.com/problems/palindrome-partitioning/)

**Intuition:** Backtrack over the cut position: from index `start`, try every end `j` such that `s[start..j]` is a palindrome, take it, and recurse from `j + 1`. Precompute `pal[i][j]` with interval DP (`s[i] == s[j]` and `pal[i+1][j-1]`) so each palindrome check is O(1).

**Python**

```python
class Solution:
    def partition(self, s: str) -> list[list[str]]:
        n = len(s)
        pal = [[False] * n for _ in range(n)]
        for i in range(n - 1, -1, -1):
            for j in range(i, n):
                pal[i][j] = s[i] == s[j] and (j - i < 2 or pal[i + 1][j - 1])

        res, path = [], []

        def dfs(start: int) -> None:
            if start == n:
                res.append(path[:])
                return
            for j in range(start, n):
                if pal[start][j]:
                    path.append(s[start:j + 1])
                    dfs(j + 1)
                    path.pop()

        dfs(0)
        return res
```

**C++**

```cpp
class Solution {
    vector<vector<string>> res;
    vector<string> path;
    vector<vector<char>> pal;

    void dfs(const string& s, int start) {
        int n = s.size();
        if (start == n) {
            res.push_back(path);
            return;
        }
        for (int j = start; j < n; ++j) {
            if (!pal[start][j]) continue;
            path.push_back(s.substr(start, j - start + 1));
            dfs(s, j + 1);
            path.pop_back();
        }
    }

public:
    vector<vector<string>> partition(string s) {
        int n = s.size();
        pal.assign(n, vector<char>(n, 0));
        for (int i = n - 1; i >= 0; --i)
            for (int j = i; j < n; ++j)
                pal[i][j] = s[i] == s[j] && (j - i < 2 || pal[i + 1][j - 1]);
        dfs(s, 0);
        return res;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n · 2^n), n = len(s) |
| **Space** | O(n^2) for the palindrome table, excluding the output |

**Pitfalls:** Fill the DP with `i` descending so `pal[i+1][j-1]` is ready; guard `j - i < 2` so length-1 and length-2 substrings never read an invalid cell.

---

### LC 37 · Sudoku Solver · Hard

> **Problem:** Fill the empty cells (`'.'`) of a 9×9 Sudoku board in place so that every row, column and 3×3 box contains digits 1-9 exactly once. The input has exactly one solution.

🔗 [https://leetcode.com/problems/sudoku-solver/](https://leetcode.com/problems/sudoku-solver/)

**Intuition:** Backtrack over the list of empty cells, keeping a 9-bit mask of used digits per row, column and box. The candidates for a cell are `~(row | col | box) & 0x1FF`, enumerated by repeatedly extracting the lowest set bit, so each check is O(1). On failure, undo the bits and try the next candidate; choosing the most-constrained cell first (MRV) is a well-known speedup but is not needed here.

**Python**

```python
class Solution:
    def solveSudoku(self, board: list[list[str]]) -> None:
        rows, cols, boxes = [0] * 9, [0] * 9, [0] * 9
        empty = []
        for r in range(9):
            for c in range(9):
                if board[r][c] == ".":
                    empty.append((r, c))
                else:
                    bit = 1 << (int(board[r][c]) - 1)
                    b = r // 3 * 3 + c // 3
                    rows[r] |= bit
                    cols[c] |= bit
                    boxes[b] |= bit

        def solve(k: int) -> bool:
            if k == len(empty):
                return True
            r, c = empty[k]
            b = r // 3 * 3 + c // 3
            free = ~(rows[r] | cols[c] | boxes[b]) & 0x1FF
            while free:
                bit = free & -free  # lowest candidate digit
                free ^= bit
                rows[r] |= bit
                cols[c] |= bit
                boxes[b] |= bit
                board[r][c] = str(bit.bit_length())
                if solve(k + 1):
                    return True
                rows[r] ^= bit
                cols[c] ^= bit
                boxes[b] ^= bit
            board[r][c] = "."
            return False

        solve(0)
```

**C++**

```cpp
class Solution {
    int rows[9] = {}, cols[9] = {}, boxes[9] = {};
    vector<pair<int, int>> empty;

    bool solve(vector<vector<char>>& board, int k) {
        if (k == (int)empty.size()) return true;
        auto [r, c] = empty[k];
        int b = r / 3 * 3 + c / 3;
        int free = ~(rows[r] | cols[c] | boxes[b]) & 0x1FF;
        while (free) {
            int bit = free & -free;  // lowest candidate digit
            free ^= bit;
            rows[r] |= bit, cols[c] |= bit, boxes[b] |= bit;
            board[r][c] = char('1' + __builtin_ctz(bit));
            if (solve(board, k + 1)) return true;
            rows[r] ^= bit, cols[c] ^= bit, boxes[b] ^= bit;
        }
        board[r][c] = '.';
        return false;
    }

public:
    void solveSudoku(vector<vector<char>>& board) {
        for (int r = 0; r < 9; ++r)
            for (int c = 0; c < 9; ++c) {
                if (board[r][c] == '.') {
                    empty.push_back({r, c});
                } else {
                    int bit = 1 << (board[r][c] - '1');
                    rows[r] |= bit, cols[c] |= bit, boxes[r / 3 * 3 + c / 3] |= bit;
                }
            }
        solve(board, 0);
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(9^m) worst case, m = number of empty cells (≤ 81); constraint masks prune heavily in practice |
| **Space** | O(m) for the empty-cell list and recursion |

**Pitfalls:** Undo all three masks on backtrack and reset the cell to `'.'` before returning false; the box index is `r / 3 * 3 + c / 3`, not `r / 3 + c / 3`.

---

## 11. Modified Binary Search

Template and pitfalls: [LeetCode Patterns §11 Modified Binary Search](../computer-science/LeetCode_Patterns.md#11-modified-binary-search)

### LC 35 · Search Insert Position · Easy

> **Problem:** Given a sorted array of distinct integers and a `target`, return the index of `target` if present, otherwise the index where it would be inserted to keep the order. Must run in O(log n).

🔗 [https://leetcode.com/problems/search-insert-position/](https://leetcode.com/problems/search-insert-position/)

**Intuition:** The answer is the lower bound: the first index whose value is `>= target`. Binary search on the half-open range `[lo, hi)` with `hi = n`, moving `lo = mid + 1` when `nums[mid] < target` and `hi = mid` otherwise; `lo` converges to the lower bound, which is `n` when every value is smaller.

**Python**

```python
class Solution:
    def searchInsert(self, nums: list[int], target: int) -> int:
        lo, hi = 0, len(nums)
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid
        return lo
```

**C++**

```cpp
class Solution {
public:
    int searchInsert(vector<int>& nums, int target) {
        int lo = 0, hi = nums.size();
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] < target)
                lo = mid + 1;
            else
                hi = mid;
        }
        return lo;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(log n) |
| **Space** | O(1) |

**Pitfalls:** Starting with `hi = n - 1` cannot return `n` when target is larger than every element; in C++ this is just `lower_bound(...) - begin()`.

---

### LC 278 · First Bad Version · Easy

> **Problem:** Versions `1..n` (n ≤ 2^31 - 1) are built in order, and every version after a bad one is also bad. Using the provided API `isBadVersion(version)`, find the first bad version while minimizing API calls.

🔗 [https://leetcode.com/problems/first-bad-version/](https://leetcode.com/problems/first-bad-version/)

**Intuition:** `isBadVersion` is monotone (false...false, true...true), so the answer is the first `true`. Binary search for that boundary: if `mid` is bad the answer is `mid` or earlier (`hi = mid`), otherwise it is later (`lo = mid + 1`). This takes O(log n) API calls versus O(n) for a linear scan.

**Python**

```python
# The isBadVersion(version: int) -> bool API is provided by LeetCode.
class Solution:
    def firstBadVersion(self, n: int) -> int:
        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if isBadVersion(mid):
                hi = mid  # mid may be the first bad one
            else:
                lo = mid + 1
        return lo
```

**C++**

```cpp
// The API bool isBadVersion(int version); is provided by LeetCode.
class Solution {
public:
    int firstBadVersion(int n) {
        int lo = 1, hi = n;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;  // (lo + hi) / 2 overflows near 2^31
            if (isBadVersion(mid))
                hi = mid;  // mid may be the first bad one
            else
                lo = mid + 1;
        }
        return lo;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(log n) API calls |
| **Space** | O(1) |

**Pitfalls:** In C++ `(lo + hi) / 2` overflows when `n` is near `2^31 - 1`; using `hi = mid - 1` on a bad `mid` can skip the answer.

---

### LC 153 · Find Minimum in Rotated Sorted Array · Medium

> **Problem:** A sorted array of unique integers was rotated between 1 and n times. Return its minimum element in O(log n) time.

🔗 [https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)

**Intuition:** Compare `nums[mid]` with `nums[hi]`. If `nums[mid] > nums[hi]` the rotation point (the minimum) lies strictly right of `mid`; otherwise `mid..hi` is sorted and the minimum is at `mid` or to its left. Shrinking `[lo, hi]` this way keeps the minimum inside until `lo == hi`.

**Python**

```python
class Solution:
    def findMin(self, nums: list[int]) -> int:
        lo, hi = 0, len(nums) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] > nums[hi]:
                lo = mid + 1  # minimum is right of mid
            else:
                hi = mid
        return nums[lo]
```

**C++**

```cpp
class Solution {
public:
    int findMin(vector<int>& nums) {
        int lo = 0, hi = (int)nums.size() - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] > nums[hi])
                lo = mid + 1;  // minimum is right of mid
            else
                hi = mid;
        }
        return nums[lo];
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(log n) |
| **Space** | O(1) |

**Pitfalls:** Compare against `nums[hi]`, not `nums[lo]` (comparing with `lo` fails for an unrotated array); use `hi = mid`, not `mid - 1`, since `mid` may be the minimum.

---

### LC 81 · Search in Rotated Sorted Array II · Medium

> **Problem:** A non-decreasing array (duplicates allowed) was rotated at an unknown pivot. Return `true` if `target` is in it, else `false`.

🔗 [https://leetcode.com/problems/search-in-rotated-sorted-array-ii/](https://leetcode.com/problems/search-in-rotated-sorted-array-ii/)

**Intuition:** As in LC 33, at least one half around `mid` is sorted; check whether `target` lies in that sorted half's range and discard the other half. Duplicates break this only when `nums[lo] == nums[mid] == nums[hi]`, where you cannot tell which side is sorted, so shrink both ends by one. That case makes the worst case O(n) (e.g. all 1s with one 2), which is unavoidable.

**Python**

```python
class Solution:
    def search(self, nums: list[int], target: int) -> bool:
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return True
            if nums[lo] == nums[mid] == nums[hi]:
                lo += 1  # cannot tell which half is sorted
                hi -= 1
            elif nums[lo] <= nums[mid]:  # left half sorted
                if nums[lo] <= target < nums[mid]:
                    hi = mid - 1
                else:
                    lo = mid + 1
            else:  # right half sorted
                if nums[mid] < target <= nums[hi]:
                    lo = mid + 1
                else:
                    hi = mid - 1
        return False
```

**C++**

```cpp
class Solution {
public:
    bool search(vector<int>& nums, int target) {
        int lo = 0, hi = (int)nums.size() - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] == target) return true;
            if (nums[lo] == nums[mid] && nums[mid] == nums[hi]) {
                ++lo;  // cannot tell which half is sorted
                --hi;
            } else if (nums[lo] <= nums[mid]) {  // left half sorted
                if (nums[lo] <= target && target < nums[mid])
                    hi = mid - 1;
                else
                    lo = mid + 1;
            } else {  // right half sorted
                if (nums[mid] < target && target <= nums[hi])
                    lo = mid + 1;
                else
                    hi = mid - 1;
            }
        }
        return false;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(log n) average, O(n) worst case with many duplicates |
| **Space** | O(1) |

**Pitfalls:** Without the triple-equality shrink, inputs like `[1,0,1,1,1]` pick the wrong half; `nums[lo] <= nums[mid]` must use `<=` so `lo == mid` counts as sorted.

---

## 12. Top K Elements

Template and pitfalls: [LeetCode Patterns §12 Top K Elements](../computer-science/LeetCode_Patterns.md#12-top-k-elements)

### LC 621 · Task Scheduler · Medium

> **Problem:** Given CPU tasks labeled `A`-`Z` and a cooldown `n`, identical tasks must be at least `n` intervals apart; each interval runs one task or idles. Return the minimum number of intervals to finish all tasks.

🔗 [https://leetcode.com/problems/task-scheduler/](https://leetcode.com/problems/task-scheduler/)

**Intuition:** The most frequent task (count `f`) forces `f - 1` full frames of length `n + 1`, plus a final partial frame holding every task that also has count `f` (say `m` of them): `(f - 1) * (n + 1) + m`. If there are enough other tasks to fill all idle slots, no idling is needed and the answer is just `len(tasks)`, so take the max. The heap simulation (pop up to `n + 1` most frequent per frame) also works in O(len · log 26) and is the "Top K" framing.

**Python**

```python
class Solution:
    def leastInterval(self, tasks: list[str], n: int) -> int:
        cnt = Counter(tasks).values()
        f = max(cnt)
        m = sum(1 for c in cnt if c == f)  # tasks tied for the max count
        return max(len(tasks), (f - 1) * (n + 1) + m)
```

**C++**

```cpp
class Solution {
public:
    int leastInterval(vector<char>& tasks, int n) {
        int cnt[26] = {};
        for (char t : tasks) ++cnt[t - 'A'];
        int f = *max_element(cnt, cnt + 26);
        int m = count(cnt, cnt + 26, f);  // tasks tied for the max count
        return max((int)tasks.size(), (f - 1) * (n + 1) + m);
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(T), T = len(tasks) |
| **Space** | O(1) (26 counters) |

**Pitfalls:** Forgetting the `max(len(tasks), ...)` undercounts when there are many distinct tasks; forgetting `m` (ties for the max count) undercounts the last frame.

---

### LC 767 · Reorganize String · Medium

> **Problem:** Rearrange the characters of `s` (lowercase, length ≤ 500) so that no two adjacent characters are equal; return any valid arrangement or `""` if impossible.

🔗 [https://leetcode.com/problems/reorganize-string/](https://leetcode.com/problems/reorganize-string/)

**Intuition:** It is impossible exactly when some character occurs more than `(n + 1) // 2` times. Otherwise greedily emit the most frequent remaining character that differs from the last one: pop the top of a max-heap, emit it, and hold it back for one step before pushing it back so it cannot repeat immediately. An O(n) alternative fills even indices with the most frequent character first, then the rest.

**Python**

```python
class Solution:
    def reorganizeString(self, s: str) -> str:
        cnt = Counter(s)
        if max(cnt.values()) > (len(s) + 1) // 2:
            return ""
        heap = [(-c, ch) for ch, c in cnt.items()]
        heapq.heapify(heap)
        res = []
        prev = None  # (negcount, char) held back for one step
        while heap:
            c, ch = heapq.heappop(heap)
            res.append(ch)
            if prev:
                heapq.heappush(heap, prev)
            prev = (c + 1, ch) if c + 1 < 0 else None
        return "".join(res)
```

**C++**

```cpp
class Solution {
public:
    string reorganizeString(string s) {
        int cnt[26] = {};
        for (char ch : s) ++cnt[ch - 'a'];
        int n = s.size();
        if (*max_element(cnt, cnt + 26) > (n + 1) / 2) return "";
        priority_queue<pair<int, char>> pq;
        for (int i = 0; i < 26; ++i)
            if (cnt[i]) pq.push({cnt[i], char('a' + i)});
        string res;
        pair<int, char> prev{0, 0};  // held back for one step
        while (!pq.empty()) {
            auto [c, ch] = pq.top();
            pq.pop();
            res += ch;
            if (prev.first > 0) pq.push(prev);
            prev = {c - 1, ch};
        }
        return res;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n log A), A ≤ 26 distinct letters, so effectively O(n) |
| **Space** | O(A) heap plus the O(n) output |

**Pitfalls:** The feasibility bound is `(n + 1) / 2`, not `n / 2` (odd lengths allow one extra); pushing the just-used character back immediately lets it be popped again and repeat.

---

### LC 1834 · Single-Threaded CPU · Medium

> **Problem:** `tasks[i] = [enqueueTime, processingTime]` (n ≤ 10^5, times ≤ 10^9). A single-threaded CPU, whenever idle, picks the available task with the shortest processing time (ties broken by smaller index) and runs it to completion; if none is available it waits for the next enqueue. Return the order in which task indices are processed.

🔗 [https://leetcode.com/problems/single-threaded-cpu/](https://leetcode.com/problems/single-threaded-cpu/)

**Intuition:** Sort task indices by enqueue time and simulate with a clock and a min-heap keyed by `(processingTime, index)`. Each time the CPU is free, push every task whose enqueue time has passed, then pop the heap top and advance the clock by its processing time. If the heap is empty, jump the clock straight to the next enqueue time instead of ticking, so each task is pushed and popped once.

**Python**

```python
class Solution:
    def getOrder(self, tasks: list[list[int]]) -> list[int]:
        order = sorted(range(len(tasks)), key=lambda i: tasks[i][0])
        heap, res = [], []  # heap of (processingTime, index)
        time, j = 0, 0
        while len(res) < len(tasks):
            if not heap:
                time = max(time, tasks[order[j]][0])  # CPU idle: jump ahead
            while j < len(order) and tasks[order[j]][0] <= time:
                i = order[j]
                heapq.heappush(heap, (tasks[i][1], i))
                j += 1
            proc, i = heapq.heappop(heap)
            time += proc
            res.append(i)
        return res
```

**C++**

```cpp
class Solution {
public:
    vector<int> getOrder(vector<vector<int>>& tasks) {
        int n = tasks.size();
        vector<int> order(n);
        iota(order.begin(), order.end(), 0);
        sort(order.begin(), order.end(), [&](int a, int b) { return tasks[a][0] < tasks[b][0]; });
        // min-heap of (processingTime, index)
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> pq;
        vector<int> res;
        long long time = 0;  // can reach about 10^5 · 10^9
        int j = 0;
        while ((int)res.size() < n) {
            if (pq.empty()) time = max(time, (long long)tasks[order[j]][0]);  // CPU idle: jump ahead
            while (j < n && tasks[order[j]][0] <= time) {
                pq.push({tasks[order[j]][1], order[j]});
                ++j;
            }
            auto [proc, i] = pq.top();
            pq.pop();
            time += proc;
            res.push_back(i);
        }
        return res;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n log n) |
| **Space** | O(n) |

**Pitfalls:** The clock overflows 32-bit ints in C++ (use `long long`); when idle, jump to the next enqueue time rather than incrementing by 1, and break ties by index, not by enqueue time.

---

### LC 355 · Design Twitter · Medium

> **Problem:** Design a simplified Twitter with `postTweet(userId, tweetId)`, `getNewsFeed(userId)` returning the 10 most recent tweet IDs from the user and the users they follow (most recent first), `follow(followerId, followeeId)` and `unfollow(followerId, followeeId)`.

🔗 [https://leetcode.com/problems/design-twitter/](https://leetcode.com/problems/design-twitter/)

**Intuition:** Stamp every tweet with a global increasing time and store each user's tweets as an append-only list (newest last). A news feed is a k-way merge of the relevant users' lists from the back: seed a max-heap with each user's newest tweet, pop the most recent, push that user's next-older tweet, and stop after 10. Feed cost depends only on the number of followees, not on total tweet volume.

**Python**

```python
class Twitter:
    def __init__(self):
        self.time = 0
        self.tweets = defaultdict(list)   # user -> [(time, tweetId)], newest last
        self.following = defaultdict(set)

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.tweets[userId].append((self.time, tweetId))
        self.time += 1

    def getNewsFeed(self, userId: int) -> list[int]:
        heap = []  # (-time, tweetId, user, index)
        for u in self.following[userId] | {userId}:
            if self.tweets[u]:
                i = len(self.tweets[u]) - 1
                t, tid = self.tweets[u][i]
                heap.append((-t, tid, u, i))
        heapq.heapify(heap)
        feed = []
        while heap and len(feed) < 10:
            _, tid, u, i = heapq.heappop(heap)
            feed.append(tid)
            if i > 0:
                t, nxt = self.tweets[u][i - 1]
                heapq.heappush(heap, (-t, nxt, u, i - 1))
        return feed

    def follow(self, followerId: int, followeeId: int) -> None:
        self.following[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.following[followerId].discard(followeeId)
```

**C++**

```cpp
class Twitter {
    int time = 0;
    unordered_map<int, vector<pair<int, int>>> tweets;  // user -> (time, tweetId), newest last
    unordered_map<int, unordered_set<int>> following;

public:
    Twitter() {}

    void postTweet(int userId, int tweetId) {
        tweets[userId].push_back({time++, tweetId});
    }

    vector<int> getNewsFeed(int userId) {
        priority_queue<tuple<int, int, int>> pq;  // (time, user, index), max-heap
        auto pushNewest = [&](int u) {
            auto& v = tweets[u];
            if (!v.empty()) pq.push({v.back().first, u, (int)v.size() - 1});
        };
        pushNewest(userId);
        for (int u : following[userId])
            if (u != userId) pushNewest(u);
        vector<int> feed;
        while (!pq.empty() && feed.size() < 10) {
            auto [t, u, i] = pq.top();
            pq.pop();
            feed.push_back(tweets[u][i].second);
            if (i > 0) pq.push({tweets[u][i - 1].first, u, i - 1});
        }
        return feed;
    }

    void follow(int followerId, int followeeId) {
        following[followerId].insert(followeeId);
    }

    void unfollow(int followerId, int followeeId) {
        following[followerId].erase(followeeId);
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | post/follow/unfollow O(1); getNewsFeed O(F + 10 log F), F = number of followees |
| **Space** | O(U + T + E), U users, T tweets, E follow edges |

**Pitfalls:** The user's own tweets belong in the feed even without self-follow, but must not appear twice if they also follow themselves; unfollowing someone not followed must be a no-op (`discard`, not `remove`).

---

## 13. K-way Merge

Template and pitfalls: [LeetCode Patterns §13 K-way Merge](../computer-science/LeetCode_Patterns.md#13-k-way-merge)

### LC 88 · Merge Sorted Array · Easy

> **Problem:** `nums1` has length `m + n` with its first `m` elements sorted and the last `n` set to 0; `nums2` has `n` sorted elements. Merge `nums2` into `nums1` in place so `nums1` is sorted.

🔗 [https://leetcode.com/problems/merge-sorted-array/](https://leetcode.com/problems/merge-sorted-array/)

**Intuition:** Merging from the front would overwrite unread `nums1` values, but the tail of `nums1` is free space. Fill from the back: compare the largest unplaced elements of each array and write the bigger one at position `k`. The write index never overtakes the unread part of `nums1`, so it is O(m + n) time and O(1) space; once `nums2` is exhausted, the remaining `nums1` prefix is already in place.

**Python**

```python
class Solution:
    def merge(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None:
        i, j, k = m - 1, n - 1, m + n - 1
        while j >= 0:  # leftover nums1 elements are already in place
            if i >= 0 and nums1[i] > nums2[j]:
                nums1[k] = nums1[i]
                i -= 1
            else:
                nums1[k] = nums2[j]
                j -= 1
            k -= 1
```

**C++**

```cpp
class Solution {
public:
    void merge(vector<int>& nums1, int m, vector<int>& nums2, int n) {
        int i = m - 1, j = n - 1, k = m + n - 1;
        while (j >= 0) {  // leftover nums1 elements are already in place
            if (i >= 0 && nums1[i] > nums2[j])
                nums1[k--] = nums1[i--];
            else
                nums1[k--] = nums2[j--];
        }
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(m + n) |
| **Space** | O(1) |

**Pitfalls:** Loop on `j >= 0`, not `i >= 0`, or leftover `nums2` elements are never copied; handle `m = 0` (check `i >= 0` before reading `nums1[i]`).

---

## 14. Topological Sort

Template and pitfalls: [LeetCode Patterns §14 Topological Sort](../computer-science/LeetCode_Patterns.md#14-topological-sort)

### LC 802 · Find Eventual Safe States · Medium

> **Problem:** Given a directed graph as an adjacency list `graph` (n ≤ 10^4 nodes), a node is safe if every path starting from it ends at a terminal node (no outgoing edges). Return all safe nodes in ascending order.

🔗 [https://leetcode.com/problems/find-eventual-safe-states/](https://leetcode.com/problems/find-eventual-safe-states/)

**Intuition:** Terminal nodes are safe, and a node is safe once all its successors are safe. That is Kahn's algorithm on the reversed graph keyed by out-degree: start from out-degree-0 nodes, and when a node is confirmed safe, decrement the out-degree of each predecessor, enqueueing those that reach 0. Nodes on or leading to a cycle never reach 0. DFS three-coloring works too but recursion can reach 10^4 deep.

**Python**

```python
class Solution:
    def eventualSafeNodes(self, graph: list[list[int]]) -> list[int]:
        n = len(graph)
        rev = [[] for _ in range(n)]
        outdeg = [len(nbrs) for nbrs in graph]
        for u, nbrs in enumerate(graph):
            for v in nbrs:
                rev[v].append(u)
        q = deque(u for u in range(n) if outdeg[u] == 0)
        safe = [False] * n
        while q:
            v = q.popleft()
            safe[v] = True
            for u in rev[v]:
                outdeg[u] -= 1
                if outdeg[u] == 0:
                    q.append(u)
        return [u for u in range(n) if safe[u]]
```

**C++**

```cpp
class Solution {
public:
    vector<int> eventualSafeNodes(vector<vector<int>>& graph) {
        int n = graph.size();
        vector<vector<int>> rev(n);
        vector<int> outdeg(n);
        for (int u = 0; u < n; ++u) {
            outdeg[u] = graph[u].size();
            for (int v : graph[u]) rev[v].push_back(u);
        }
        queue<int> q;
        for (int u = 0; u < n; ++u)
            if (outdeg[u] == 0) q.push(u);
        vector<bool> safe(n, false);
        while (!q.empty()) {
            int v = q.front();
            q.pop();
            safe[v] = true;
            for (int u : rev[v])
                if (--outdeg[u] == 0) q.push(u);
        }
        vector<int> res;
        for (int u = 0; u < n; ++u)
            if (safe[u]) res.push_back(u);
        return res;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(V + E) |
| **Space** | O(V + E) for the reversed graph |

**Pitfalls:** Use out-degree on the reversed graph, not in-degree on the original; collect results by scanning `0..n-1` so the output is sorted (queue order is not).

---

### LC 2115 · Find All Possible Recipes from Given Supplies · Medium

> **Problem:** Each `recipes[i]` needs all strings in `ingredients[i]`; an ingredient may be another recipe. Given infinite `supplies`, return every recipe that can be created, in any order. Recipes may depend on each other cyclically.

🔗 [https://leetcode.com/problems/find-all-possible-recipes-from-given-supplies/](https://leetcode.com/problems/find-all-possible-recipes-from-given-supplies/)

**Intuition:** Treat it as Kahn's algorithm: an edge goes from each ingredient to the recipe that needs it, and a recipe's in-degree is its ingredient count. Seed the queue with the supplies; each item popped decrements its dependent recipes, and a recipe reaching 0 is makeable and becomes a new available item. Ingredients that are neither supplies nor makeable recipes are never popped, so recipes needing them (or caught in a cycle) never reach 0.

**Python**

```python
class Solution:
    def findAllRecipes(self, recipes: list[str], ingredients: list[list[str]],
                       supplies: list[str]) -> list[str]:
        needed_by = defaultdict(list)  # ingredient -> recipes that need it
        indeg = {}
        for r, ings in zip(recipes, ingredients):
            indeg[r] = len(ings)
            for ing in ings:
                needed_by[ing].append(r)
        q = deque(supplies)
        res = []
        while q:
            item = q.popleft()
            for r in needed_by[item]:
                indeg[r] -= 1
                if indeg[r] == 0:
                    res.append(r)
                    q.append(r)
        return res
```

**C++**

```cpp
class Solution {
public:
    vector<string> findAllRecipes(vector<string>& recipes, vector<vector<string>>& ingredients,
                                  vector<string>& supplies) {
        unordered_map<string, vector<string>> neededBy;  // ingredient -> recipes that need it
        unordered_map<string, int> indeg;
        for (size_t i = 0; i < recipes.size(); ++i) {
            indeg[recipes[i]] = ingredients[i].size();
            for (auto& ing : ingredients[i]) neededBy[ing].push_back(recipes[i]);
        }
        queue<string> q;
        for (auto& s : supplies) q.push(s);
        vector<string> res;
        while (!q.empty()) {
            string item = q.front();
            q.pop();
            auto it = neededBy.find(item);
            if (it == neededBy.end()) continue;
            for (auto& r : it->second)
                if (--indeg[r] == 0) {
                    res.push_back(r);
                    q.push(r);
                }
        }
        return res;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(S + R + I) string-hash operations, S supplies, R recipes, I total ingredient entries |
| **Space** | O(R + I) |

**Pitfalls:** Ingredients within one recipe are distinct per the constraints, so counting by list length is safe; a recursive "can make" DFS needs explicit cycle detection, which Kahn's algorithm gets for free.

---

### LC 329 · Longest Increasing Path in a Matrix · Hard

> **Problem:** Given an `m × n` integer matrix (m, n ≤ 200), return the length of the longest strictly increasing path, moving only up, down, left or right.

🔗 [https://leetcode.com/problems/longest-increasing-path-in-a-matrix/](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/)

**Intuition:** Edges from each cell to strictly larger neighbors form a DAG, and the answer is its longest path in vertices. Run Kahn's algorithm level by level: start from cells with no smaller neighbor (in-degree 0), peel one BFS layer at a time, and the number of layers equals the longest path. DFS with memoization is the other standard O(m·n) answer, but its recursion can reach m·n = 40000 deep, so the iterative topological form is safer in Python.

**Python**

```python
class Solution:
    def longestIncreasingPath(self, matrix: list[list[int]]) -> int:
        m, n = len(matrix), len(matrix[0])
        dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))
        indeg = [[0] * n for _ in range(m)]  # number of strictly smaller neighbors
        for r in range(m):
            for c in range(n):
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] < matrix[r][c]:
                        indeg[r][c] += 1
        q = deque((r, c) for r in range(m) for c in range(n) if indeg[r][c] == 0)
        layers = 0
        while q:
            layers += 1
            for _ in range(len(q)):
                r, c = q.popleft()
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] > matrix[r][c]:
                        indeg[nr][nc] -= 1
                        if indeg[nr][nc] == 0:
                            q.append((nr, nc))
        return layers
```

**C++**

```cpp
class Solution {
public:
    int longestIncreasingPath(vector<vector<int>>& matrix) {
        int m = matrix.size(), n = matrix[0].size();
        const int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};
        vector<vector<int>> indeg(m, vector<int>(n, 0));  // number of strictly smaller neighbors
        for (int r = 0; r < m; ++r)
            for (int c = 0; c < n; ++c)
                for (int d = 0; d < 4; ++d) {
                    int nr = r + dr[d], nc = c + dc[d];
                    if (nr >= 0 && nr < m && nc >= 0 && nc < n && matrix[nr][nc] < matrix[r][c])
                        ++indeg[r][c];
                }
        queue<pair<int, int>> q;
        for (int r = 0; r < m; ++r)
            for (int c = 0; c < n; ++c)
                if (indeg[r][c] == 0) q.push({r, c});
        int layers = 0;
        while (!q.empty()) {
            ++layers;
            for (int s = q.size(); s > 0; --s) {
                auto [r, c] = q.front();
                q.pop();
                for (int d = 0; d < 4; ++d) {
                    int nr = r + dr[d], nc = c + dc[d];
                    if (nr >= 0 && nr < m && nc >= 0 && nc < n && matrix[nr][nc] > matrix[r][c])
                        if (--indeg[nr][nc] == 0) q.push({nr, nc});
                }
            }
        }
        return layers;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(m·n), m×n matrix |
| **Space** | O(m·n) |

**Pitfalls:** The increase must be strict, so equal neighbors are not edges (that is also what keeps the graph acyclic); count layers, not dequeued cells.

---

## 15. Monotonic Stack / Queue

Template and pitfalls: [LeetCode Patterns §15 Monotonic Stack / Queue](../computer-science/LeetCode_Patterns.md#15-monotonic-stack--queue)

### LC 853 · Car Fleet · Medium

> **Problem:** `n` cars at distinct `position[i]` drive toward `target` at `speed[i]`. A car cannot pass the one ahead; when it catches up they move together as one fleet at the slower speed. Return the number of fleets that arrive at `target` (catching up exactly at `target` counts as one fleet).

🔗 [https://leetcode.com/problems/car-fleet/](https://leetcode.com/problems/car-fleet/)

**Intuition:** Sort cars by position, closest to the target first, and compute each car's solo arrival time `(target - p) / s`. A car joins the fleet ahead if its time is `<=` that fleet's time; otherwise it starts a new, slower fleet. This is a monotonic stack of strictly increasing arrival times, collapsed to a counter plus the current slowest time.

**Python**

```python
class Solution:
    def carFleet(self, target: int, position: list[int], speed: list[int]) -> int:
        fleets, slowest = 0, 0.0
        for p, s in sorted(zip(position, speed), reverse=True):  # closest to target first
            t = (target - p) / s
            if t > slowest:  # cannot catch the fleet ahead -> new fleet
                fleets += 1
                slowest = t
        return fleets
```

**C++**

```cpp
class Solution {
public:
    int carFleet(int target, vector<int>& position, vector<int>& speed) {
        int n = position.size();
        vector<pair<int, int>> cars(n);
        for (int i = 0; i < n; ++i) cars[i] = {position[i], speed[i]};
        sort(cars.rbegin(), cars.rend());  // closest to target first
        int fleets = 0;
        double slowest = 0;
        for (auto& [p, s] : cars) {
            double t = double(target - p) / s;
            if (t > slowest) {  // cannot catch the fleet ahead -> new fleet
                ++fleets;
                slowest = t;
            }
        }
        return fleets;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n log n) for the sort |
| **Space** | O(n) |

**Pitfalls:** Integer division of times in C++; using `>=` instead of `>` splits cars that meet exactly at the target; iterating from the back of the road instead of the front.

---

### LC 402 · Remove K Digits · Medium

> **Problem:** Given a non-negative integer as a string `num` and an integer `k`, remove exactly `k` digits so the remaining number is as small as possible. Return it without leading zeros (`"0"` if nothing is left).

🔗 [https://leetcode.com/problems/remove-k-digits/](https://leetcode.com/problems/remove-k-digits/)

**Intuition:** The leftmost digit that is larger than its right neighbour is the best one to delete, since it lowers the most significant position. A non-decreasing monotonic stack does this greedily: pop larger digits while removals remain. Leftover removals come off the tail, which is non-decreasing; then strip leading zeros. O(n) versus O(n·k) for repeated rescans.

**Python**

```python
class Solution:
    def removeKdigits(self, num: str, k: int) -> str:
        stack = []
        for d in num:
            while k and stack and stack[-1] > d:
                stack.pop()
                k -= 1
            stack.append(d)
        stack = stack[:len(stack) - k]  # leftover removals come off the tail
        return ''.join(stack).lstrip('0') or '0'
```

**C++**

```cpp
class Solution {
public:
    string removeKdigits(string num, int k) {
        string st;
        for (char d : num) {
            while (k > 0 && !st.empty() && st.back() > d) {
                st.pop_back();
                --k;
            }
            st.push_back(d);
        }
        st.resize(st.size() - k);  // leftover removals come off the tail
        size_t i = st.find_first_not_of('0');
        return i == string::npos ? "0" : st.substr(i);
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n), n = len(num) |
| **Space** | O(n) |

**Pitfalls:** `stack[:-k]` with `k == 0` yields an empty list; forgetting leftover `k` on non-decreasing input like `"12345"`; returning `""` instead of `"0"`.

---

### LC 901 · Online Stock Span · Medium

> **Problem:** Design `StockSpanner` whose `next(price)` returns today's span: the number of consecutive days, ending today and going backwards, on which the price was less than or equal to today's price. Up to 10^4 calls.

🔗 [https://leetcode.com/problems/online-stock-span/](https://leetcode.com/problems/online-stock-span/)

**Intuition:** Keep a stack of `(price, span)` with strictly decreasing prices. A new price pops every entry `<=` it and absorbs their spans, because those days can never stop a future span earlier than today will. Each day is pushed and popped at most once, so calls are amortized O(1) instead of the O(n) backward scan.

**Python**

```python
class StockSpanner:
    def __init__(self):
        self.stack = []  # (price, span), prices strictly decreasing

    def next(self, price: int) -> int:
        span = 1
        while self.stack and self.stack[-1][0] <= price:
            span += self.stack.pop()[1]
        self.stack.append((price, span))
        return span
```

**C++**

```cpp
class StockSpanner {
    vector<pair<int, int>> st;  // (price, span), prices strictly decreasing
public:
    StockSpanner() {}

    int next(int price) {
        int span = 1;
        while (!st.empty() && st.back().first <= price) {
            span += st.back().second;
            st.pop_back();
        }
        st.emplace_back(price, span);
        return span;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(1) amortized per `next` (O(n) total for n calls) |
| **Space** | O(n) |

**Pitfalls:** Pop on `<=` (not `<`), otherwise equal prices are not merged; storing only prices loses the absorbed spans.

---

### LC 1019 · Next Greater Node In Linked List · Medium

> **Problem:** Given the `head` of a linked list with `n` nodes (n ≤ 10^4), return an array `answer` where `answer[i]` is the value of the first node after node `i` with a strictly larger value, or `0` if there is none.

🔗 [https://leetcode.com/problems/next-greater-node-in-linked-list/](https://leetcode.com/problems/next-greater-node-in-linked-list/)

**Intuition:** This is Next Greater Element on a list that can only be walked forward. Keep a stack of `(index, value)` for nodes still waiting for a larger value; their values are non-increasing from bottom to top. Each new node pops and resolves every waiting node smaller than it, then waits itself. Every node is pushed and popped at most once, so one pass is O(n) instead of the O(n^2) scan ahead from each node.

**Python**

```python
class Solution:
    def nextLargerNodes(self, head: Optional[ListNode]) -> list[int]:
        res, stack = [], []  # stack: (index, value) still waiting, values non-increasing
        while head:
            while stack and stack[-1][1] < head.val:
                res[stack.pop()[0]] = head.val
            stack.append((len(res), head.val))
            res.append(0)  # stays 0 if nothing larger follows
            head = head.next
        return res
```

**C++**

```cpp
class Solution {
public:
    vector<int> nextLargerNodes(ListNode* head) {
        vector<int> res;
        vector<pair<int, int>> st;  // (index, value) still waiting, values non-increasing
        for (; head; head = head->next) {
            while (!st.empty() && st.back().second < head->val) {
                res[st.back().first] = head->val;
                st.pop_back();
            }
            st.emplace_back((int)res.size(), head->val);
            res.push_back(0);  // stays 0 if nothing larger follows
        }
        return res;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n), n = number of nodes |
| **Space** | O(n) |

**Pitfalls:** Pop only on strictly smaller values (equal values are not "greater"); storing values without indices leaves no slot to write the answer to.

---

### LC 456 · 132 Pattern · Medium

> **Problem:** Given `nums` (length ≤ 2·10^5, values in [-10^9, 10^9]), return `true` if there exist `i < j < k` with `nums[i] < nums[k] < nums[j]`.

🔗 [https://leetcode.com/problems/132-pattern/](https://leetcode.com/problems/132-pattern/)

**Intuition:** Scan from the right while keeping a decreasing stack of candidates for the "3" (`nums[j]`). When a new `x` pops smaller values, `x` is a valid "3" for each of them, so the largest popped value becomes `third`, the best "2" (`nums[k]`) seen so far. Any later `x < third` completes a 132 pattern. Each element is pushed and popped once, so this is O(n) versus the O(n^2) approach of tracking the prefix minimum for each `j`.

**Python**

```python
class Solution:
    def find132pattern(self, nums: list[int]) -> bool:
        third = float('-inf')  # largest "2" that has a larger "3" to its left
        stack = []  # candidates for the "3", decreasing from bottom to top
        for x in reversed(nums):
            if x < third:
                return True  # x is the "1"
            while stack and stack[-1] < x:
                third = stack.pop()
            stack.append(x)
        return False
```

**C++**

```cpp
class Solution {
public:
    bool find132pattern(vector<int>& nums) {
        long long third = LLONG_MIN;  // largest "2" that has a larger "3" to its left
        vector<int> st;               // candidates for the "3", decreasing from bottom to top
        for (int i = (int)nums.size() - 1; i >= 0; --i) {
            if (nums[i] < third) return true;  // nums[i] is the "1"
            while (!st.empty() && st.back() < nums[i]) {
                third = st.back();
                st.pop_back();
            }
            st.push_back(nums[i]);
        }
        return false;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n) |
| **Space** | O(n) |

**Pitfalls:** All three comparisons are strict, so duplicates such as `[1, 2, 2]` or `[1, 1, 1]` give `false`; scanning left to right with a stack is much harder to get right.

---

### LC 85 · Maximal Rectangle · Hard

> **Problem:** Given an `m × n` binary matrix of characters `'0'`/`'1'`, return the area of the largest rectangle containing only `'1'`s.

🔗 [https://leetcode.com/problems/maximal-rectangle/](https://leetcode.com/problems/maximal-rectangle/)

**Intuition:** Treat each row as the floor of a histogram whose bar `j` is the number of consecutive `'1'`s ending at this row in column `j`. The best rectangle with its bottom on this row is LC 84 (Largest Rectangle in Histogram): an increasing stack gives each popped bar its widest span, bounded by the new top on the left and the current index on the right. One O(n) pass per row.

**Python**

```python
class Solution:
    def maximalRectangle(self, matrix: list[list[str]]) -> int:
        if not matrix:
            return 0
        n, best = len(matrix[0]), 0
        heights = [0] * (n + 1)  # heights[n] = 0 sentinel flushes the stack
        for row in matrix:
            for j in range(n):
                heights[j] = heights[j] + 1 if row[j] == '1' else 0
            stack = []
            for j in range(n + 1):
                while stack and heights[stack[-1]] >= heights[j]:
                    h = heights[stack.pop()]
                    left = stack[-1] if stack else -1
                    best = max(best, h * (j - left - 1))
                stack.append(j)
        return best
```

**C++**

```cpp
class Solution {
public:
    int maximalRectangle(vector<vector<char>>& matrix) {
        if (matrix.empty()) return 0;
        int n = matrix[0].size(), best = 0;
        vector<int> h(n + 1, 0);  // h[n] = 0 sentinel flushes the stack
        for (auto& row : matrix) {
            for (int j = 0; j < n; ++j) h[j] = row[j] == '1' ? h[j] + 1 : 0;
            vector<int> st;
            for (int j = 0; j <= n; ++j) {
                while (!st.empty() && h[st.back()] >= h[j]) {
                    int height = h[st.back()];
                    st.pop_back();
                    int left = st.empty() ? -1 : st.back();
                    best = max(best, height * (j - left - 1));
                }
                st.push_back(j);
            }
        }
        return best;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(m·n), m×n matrix |
| **Space** | O(n) |

**Pitfalls:** Comparing against integer `1` instead of the character `'1'`; forgetting the trailing 0 sentinel so the last bars are never popped; width is `j - left - 1`, not `j - popped`.

---

## 16. Union Find (Disjoint Set)

Template and pitfalls: [LeetCode Patterns §16 Union Find (Disjoint Set)](../computer-science/LeetCode_Patterns.md#16-union-find-disjoint-set)

### LC 261 · Graph Valid Tree · Medium

> **Problem:** Given `n` nodes labeled `0..n-1` and a list of undirected `edges`, return `true` if the edges form a valid tree (connected and acyclic).

🔗 [https://leetcode.com/problems/graph-valid-tree/](https://leetcode.com/problems/graph-valid-tree/)

**Intuition:** A graph on `n` nodes is a tree iff it has exactly `n - 1` edges and no cycle (those two imply connectivity). Check the edge count first, then union each edge; an edge whose endpoints already share a root closes a cycle. BFS/DFS from node 0 counting visited nodes works equally well.

**Python**

```python
class Solution:
    def validTree(self, n: int, edges: list[list[int]]) -> bool:
        if len(edges) != n - 1:
            return False
        parent, size = list(range(n)), [1] * n

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for a, b in edges:
            ra, rb = find(a), find(b)
            if ra == rb:
                return False  # edge closes a cycle
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]
        return True
```

**C++**

```cpp
class Solution {
    vector<int> parent, sz;
    int find(int x) {
        while (parent[x] != x) x = parent[x] = parent[parent[x]];
        return x;
    }
public:
    bool validTree(int n, vector<vector<int>>& edges) {
        if ((int)edges.size() != n - 1) return false;
        parent.resize(n);
        iota(parent.begin(), parent.end(), 0);
        sz.assign(n, 1);
        for (auto& e : edges) {
            int a = find(e[0]), b = find(e[1]);
            if (a == b) return false;  // edge closes a cycle
            if (sz[a] < sz[b]) swap(a, b);
            parent[b] = a;
            sz[a] += sz[b];
        }
        return true;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n·alpha(n)) |
| **Space** | O(n) |

**Pitfalls:** Checking only acyclicity (a forest passes) or only connectivity; `n = 1` with no edges is a valid tree.

---

### LC 1584 · Min Cost to Connect All Points · Medium

> **Problem:** Given `n` (≤ 1000) distinct points on a 2D plane, connecting two points costs their Manhattan distance. Return the minimum cost to make all points connected (exactly one simple path between any two).

🔗 [https://leetcode.com/problems/min-cost-to-connect-all-points/](https://leetcode.com/problems/min-cost-to-connect-all-points/)

**Intuition:** This is a minimum spanning tree over the complete graph. Kruskal: sort all `n(n-1)/2` edges by weight and take each edge that joins two different DSU components, stopping after `n - 1` edges. Because the graph is dense (E ~ n^2), array-based Prim (repeatedly pick the cheapest unvisited point and relax all others) is the asymptotic optimum at O(n^2) time and O(n) space with no edge list.

**Python**

```python
class Solution:
    def minCostConnectPoints(self, points: list[list[int]]) -> int:
        n = len(points)
        edges = []
        for i in range(n):
            xi, yi = points[i]
            for j in range(i + 1, n):
                edges.append((abs(xi - points[j][0]) + abs(yi - points[j][1]), i, j))
        edges.sort()
        parent = list(range(n))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        cost = used = 0
        for w, i, j in edges:
            if used == n - 1:
                break
            ri, rj = find(i), find(j)
            if ri != rj:
                parent[ri] = rj
                cost += w
                used += 1
        return cost
```

**C++**

```cpp
class Solution {
    vector<int> parent;
    int find(int x) {
        while (parent[x] != x) x = parent[x] = parent[parent[x]];
        return x;
    }
public:
    int minCostConnectPoints(vector<vector<int>>& points) {
        int n = points.size();
        vector<array<int, 3>> edges;  // (weight, i, j)
        edges.reserve(n * (n - 1) / 2);
        for (int i = 0; i < n; ++i)
            for (int j = i + 1; j < n; ++j)
                edges.push_back({abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1]), i, j});
        sort(edges.begin(), edges.end());
        parent.resize(n);
        iota(parent.begin(), parent.end(), 0);
        int cost = 0, used = 0;
        for (auto& [w, i, j] : edges) {
            if (used == n - 1) break;
            int a = find(i), b = find(j);
            if (a == b) continue;
            parent[a] = b;
            cost += w;
            ++used;
        }
        return cost;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n^2 log n) for sorting the n^2/2 edges (Prim: O(n^2)) |
| **Space** | O(n^2) edge list (Prim: O(n)) |

**Pitfalls:** Building a heap of all edges in Python is slow; skip the early exit and you scan every edge; a single point costs 0.

---

### LC 990 · Satisfiability of Equality Equations · Medium

> **Problem:** Each string in `equations` has the form `"a==b"` or `"a!=b"` with lowercase single-letter variables. Return `true` if integers can be assigned to the variables so that all equations hold.

🔗 [https://leetcode.com/problems/satisfiability-of-equality-equations/](https://leetcode.com/problems/satisfiability-of-equality-equations/)

**Intuition:** Equality is transitive, so process all `==` first by unioning their variables into classes, then check that no `!=` pair lands in the same class. Order matters: interleaving the two passes would miss an inequality that is contradicted by a later equality.

**Python**

```python
class Solution:
    def equationsPossible(self, equations: list[str]) -> bool:
        parent = list(range(26))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]  # path halving
                x = parent[x]
            return x

        for e in equations:
            if e[1] == '=':
                parent[find(ord(e[0]) - 97)] = find(ord(e[3]) - 97)
        return all(find(ord(e[0]) - 97) != find(ord(e[3]) - 97)
                   for e in equations if e[1] == '!')
```

**C++**

```cpp
class Solution {
    int parent[26];
    int find(int x) {
        while (parent[x] != x) x = parent[x] = parent[parent[x]];  // path halving
        return x;
    }
public:
    bool equationsPossible(vector<string>& equations) {
        iota(parent, parent + 26, 0);
        for (auto& e : equations)
            if (e[1] == '=') parent[find(e[0] - 'a')] = find(e[3] - 'a');
        for (auto& e : equations)
            if (e[1] == '!' && find(e[0] - 'a') == find(e[3] - 'a')) return false;
        return true;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n), n = number of equations (only 26 DSU nodes) |
| **Space** | O(1) |

**Pitfalls:** Handling `!=` before all `==` are merged; `"a!=a"` must return `false`.

---

### LC 1319 · Number of Operations to Make Network Connected · Medium

> **Problem:** `n` computers are linked by cable `connections[i] = [a, b]`. You may unplug any cable and reconnect it between any two computers. Return the minimum number of moves to connect all computers, or `-1` if impossible.

🔗 [https://leetcode.com/problems/number-of-operations-to-make-network-connected/](https://leetcode.com/problems/number-of-operations-to-make-network-connected/)

**Intuition:** Connecting `n` nodes needs at least `n - 1` cables, so fewer means `-1`. Otherwise there are always enough redundant cables (edges inside a component) to bridge components, and each move joins exactly two, so the answer is `components - 1`. Count components with DSU by decrementing on every successful union.

**Python**

```python
class Solution:
    def makeConnected(self, n: int, connections: list[list[int]]) -> int:
        if len(connections) < n - 1:
            return -1
        parent, size = list(range(n)), [1] * n

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        components = n
        for a, b in connections:
            ra, rb = find(a), find(b)
            if ra != rb:
                if size[ra] < size[rb]:
                    ra, rb = rb, ra
                parent[rb] = ra
                size[ra] += size[rb]
                components -= 1
        return components - 1
```

**C++**

```cpp
class Solution {
    vector<int> parent, sz;
    int find(int x) {
        while (parent[x] != x) x = parent[x] = parent[parent[x]];
        return x;
    }
public:
    int makeConnected(int n, vector<vector<int>>& connections) {
        if ((int)connections.size() < n - 1) return -1;
        parent.resize(n);
        iota(parent.begin(), parent.end(), 0);
        sz.assign(n, 1);
        int components = n;
        for (auto& c : connections) {
            int a = find(c[0]), b = find(c[1]);
            if (a == b) continue;
            if (sz[a] < sz[b]) swap(a, b);
            parent[b] = a;
            sz[a] += sz[b];
            --components;
        }
        return components - 1;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n + E·alpha(n)), E = number of connections |
| **Space** | O(n) |

**Pitfalls:** Counting redundant edges explicitly is unnecessary once the `E >= n - 1` check passes; the answer is `components - 1`, not `components`.

---

### LC 399 · Evaluate Division · Medium

> **Problem:** `equations[i] = [A, B]` with `values[i]` means `A / B = values[i]`. For each query `[C, D]` return `C / D`, or `-1.0` if it cannot be determined (including any unknown variable). Inputs are consistent and non-zero.

🔗 [https://leetcode.com/problems/evaluate-division/](https://leetcode.com/problems/evaluate-division/)

**Intuition:** Weighted union-find: store `w[x] = x / parent[x]`, so after path compression `w[x] = x / root`. To union `a / b = v`, attach `root(a)` under `root(b)` with weight `v · w[b] / w[a]` (from `a = w[a]·ra`, `b = w[b]·rb`). A query is answerable iff both variables share a root, and then `a / b = w[a] / w[b]`. BFS/DFS over a ratio graph per query also works but costs O(E) per query.

**Python**

```python
class Solution:
    def calcEquation(self, equations: list[list[str]], values: list[float],
                     queries: list[list[str]]) -> list[float]:
        parent, w = {}, {}  # w[x] = x / parent[x]

        def find(x: str) -> str:
            p = parent[x]
            if p != x:
                root = find(p)
                w[x] *= w[p]  # w[p] is now p / root
                parent[x] = root
            return parent[x]

        for (a, b), v in zip(equations, values):
            for x in (a, b):
                if x not in parent:
                    parent[x], w[x] = x, 1.0
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb
                w[ra] = v * w[b] / w[a]
        return [w[a] / w[b] if a in parent and b in parent and find(a) == find(b) else -1.0
                for a, b in queries]
```

**C++**

```cpp
class Solution {
    unordered_map<string, string> parent;
    unordered_map<string, double> w;  // w[x] = x / parent[x]
    string find(const string& x) {
        string p = parent[x];
        if (p != x) {
            string root = find(p);
            w[x] *= w[p];  // w[p] is now p / root
            parent[x] = root;
        }
        return parent[x];
    }
public:
    vector<double> calcEquation(vector<vector<string>>& equations, vector<double>& values,
                                vector<vector<string>>& queries) {
        for (int i = 0; i < (int)equations.size(); ++i) {
            const string &a = equations[i][0], &b = equations[i][1];
            for (const string& x : {a, b})
                if (!parent.count(x)) { parent[x] = x; w[x] = 1.0; }
            string ra = find(a), rb = find(b);
            if (ra != rb) {
                parent[ra] = rb;
                w[ra] = values[i] * w[b] / w[a];
            }
        }
        vector<double> res;
        for (auto& q : queries) {
            const string &a = q[0], &b = q[1];
            if (!parent.count(a) || !parent.count(b) || find(a) != find(b)) res.push_back(-1.0);
            else res.push_back(w[a] / w[b]);
        }
        return res;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O((E + Q)·log V) worst case, near-linear in practice; E equations, Q queries, V variables |
| **Space** | O(V) |

**Pitfalls:** `x / x` for an unknown `x` is `-1.0`, not `1.0`; updating `w[x]` before recursing on the parent gives the wrong product; the union weight is `v · w[b] / w[a]`, easy to invert.

---

### LC 827 · Making A Large Island · Hard

> **Problem:** In an `n × n` binary grid (n ≤ 500) you may change at most one `0` to `1`. Return the size of the largest 4-directionally connected island afterwards.

🔗 [https://leetcode.com/problems/making-a-large-island/](https://leetcode.com/problems/making-a-large-island/)

**Intuition:** Union every pair of adjacent land cells so each island is one DSU set with a known size. Flipping a `0` then yields `1 +` the sizes of its distinct neighbouring roots (deduplicate, since two sides may touch the same island). Take the max over all zeros and over existing islands, which covers the all-ones grid. O(n^2) instead of re-flooding the grid per zero (O(n^4)).

**Python**

```python
class Solution:
    def largestIsland(self, grid: list[list[int]]) -> int:
        n = len(grid)
        parent, size = list(range(n * n)), [1] * (n * n)

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            a, b = find(a), find(b)
            if a != b:
                if size[a] < size[b]:
                    a, b = b, a
                parent[b] = a
                size[a] += size[b]

        for r in range(n):
            for c in range(n):
                if grid[r][c]:
                    if r + 1 < n and grid[r + 1][c]:
                        union(r * n + c, (r + 1) * n + c)
                    if c + 1 < n and grid[r][c + 1]:
                        union(r * n + c, r * n + c + 1)
        best = max((size[find(i)] for i in range(n * n) if grid[i // n][i % n]), default=0)
        for r in range(n):
            for c in range(n):
                if not grid[r][c]:
                    roots = {find(nr * n + nc)
                             for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1))
                             if 0 <= nr < n and 0 <= nc < n and grid[nr][nc]}
                    best = max(best, 1 + sum(size[x] for x in roots))
        return best
```

**C++**

```cpp
class Solution {
    vector<int> parent, sz;
    int find(int x) {
        while (parent[x] != x) x = parent[x] = parent[parent[x]];
        return x;
    }
    void unite(int a, int b) {
        a = find(a);
        b = find(b);
        if (a == b) return;
        if (sz[a] < sz[b]) swap(a, b);
        parent[b] = a;
        sz[a] += sz[b];
    }
public:
    int largestIsland(vector<vector<int>>& grid) {
        int n = grid.size();
        parent.resize(n * n);
        iota(parent.begin(), parent.end(), 0);
        sz.assign(n * n, 1);
        for (int r = 0; r < n; ++r)
            for (int c = 0; c < n; ++c) {
                if (!grid[r][c]) continue;
                if (r + 1 < n && grid[r + 1][c]) unite(r * n + c, (r + 1) * n + c);
                if (c + 1 < n && grid[r][c + 1]) unite(r * n + c, r * n + c + 1);
            }
        int best = 0;
        for (int i = 0; i < n * n; ++i)
            if (grid[i / n][i % n]) best = max(best, sz[find(i)]);
        const int dr[] = {-1, 1, 0, 0}, dc[] = {0, 0, -1, 1};
        for (int r = 0; r < n; ++r)
            for (int c = 0; c < n; ++c) {
                if (grid[r][c]) continue;
                int roots[4], k = 0, total = 1;
                for (int d = 0; d < 4; ++d) {
                    int nr = r + dr[d], nc = c + dc[d];
                    if (nr < 0 || nr >= n || nc < 0 || nc >= n || !grid[nr][nc]) continue;
                    int root = find(nr * n + nc);
                    bool seen = false;
                    for (int t = 0; t < k; ++t) seen |= roots[t] == root;
                    if (!seen) { roots[k++] = root; total += sz[root]; }
                }
                best = max(best, total);
            }
        return best;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n^2·alpha(n^2)), n×n grid |
| **Space** | O(n^2) |

**Pitfalls:** Adding the same island twice when it touches the zero on two sides; returning 0 instead of `n^2` for an all-ones grid; an all-zeros grid answers 1.

---

## 17. Trie (Prefix Tree)

Template and pitfalls: [LeetCode Patterns §17 Trie (Prefix Tree)](../computer-science/LeetCode_Patterns.md#17-trie-prefix-tree)

### LC 14 · Longest Common Prefix · Easy

> **Problem:** Return the longest common prefix of an array of strings `strs` (1 ≤ length ≤ 200), or `""` if there is none.

🔗 [https://leetcode.com/problems/longest-common-prefix/](https://leetcode.com/problems/longest-common-prefix/)

**Intuition:** In trie terms, the LCP is the path from the root while each node has exactly one child and no word ends there. Vertical scanning walks that same path without building the trie: compare column `i` of every string against `strs[0]` and stop at the first mismatch or the end of any string. Building a real trie only pays off for the follow-up of many LCP queries against a fixed set.

**Python**

```python
class Solution:
    def longestCommonPrefix(self, strs: list[str]) -> str:
        first = strs[0]
        for i, ch in enumerate(first):
            for s in strs:
                if i == len(s) or s[i] != ch:
                    return first[:i]
        return first
```

**C++**

```cpp
class Solution {
public:
    string longestCommonPrefix(vector<string>& strs) {
        const string& first = strs[0];
        for (int i = 0; i < (int)first.size(); ++i)
            for (const string& s : strs)
                if (i == (int)s.size() || s[i] != first[i]) return first.substr(0, i);
        return first;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(S), S = total characters (stops at the first mismatch) |
| **Space** | O(1) extra |

**Pitfalls:** Indexing past a shorter string; an empty string in the input makes the answer `""`.

---

### LC 421 · Maximum XOR of Two Numbers in an Array · Medium

> **Problem:** Given `nums` (length ≤ 2·10^5, 0 ≤ `nums[i]` ≤ 2^31 - 1), return the maximum of `nums[i] XOR nums[j]` over all `0 ≤ i ≤ j < n`.

🔗 [https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/](https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/)

**Intuition:** Insert each number into a binary trie from the most significant bit down. To find the best partner for `x`, walk greedily from the top bit, taking the opposite bit whenever that child exists, since a 1 at a higher bit outweighs all lower bits together. Insert-then-query per number gives O(n·B) instead of the O(n^2) pair scan. An equivalent O(n·B) approach builds the answer bit by bit with a hash set of prefixes.

**Python**

```python
class Solution:
    def findMaximumXOR(self, nums: list[int]) -> int:
        H = max(nums).bit_length()  # higher bits are 0 everywhere
        trie = [[0, 0]]  # node -> [child for bit 0, child for bit 1]; 0 = absent
        best = 0
        for x in nums:
            node = 0
            for b in range(H - 1, -1, -1):
                bit = (x >> b) & 1
                if not trie[node][bit]:
                    trie[node][bit] = len(trie)
                    trie.append([0, 0])
                node = trie[node][bit]
            node, cur = 0, 0
            for b in range(H - 1, -1, -1):
                want = ((x >> b) & 1) ^ 1
                if trie[node][want]:
                    cur |= 1 << b
                    node = trie[node][want]
                else:
                    node = trie[node][want ^ 1]
            best = max(best, cur)
        return best
```

**C++**

```cpp
class Solution {
public:
    int findMaximumXOR(vector<int>& nums) {
        vector<array<int, 2>> trie(1, {0, 0});  // child index 0 = absent (root is never a child)
        trie.reserve(nums.size() * 31 + 1);
        int best = 0;
        for (int x : nums) {
            int node = 0;
            for (int b = 30; b >= 0; --b) {
                int bit = (x >> b) & 1;
                if (!trie[node][bit]) {
                    trie[node][bit] = trie.size();
                    trie.push_back({0, 0});
                }
                node = trie[node][bit];
            }
            node = 0;
            int cur = 0;
            for (int b = 30; b >= 0; --b) {
                int want = ((x >> b) & 1) ^ 1;
                if (trie[node][want]) {
                    cur |= 1 << b;
                    node = trie[node][want];
                } else {
                    node = trie[node][want ^ 1];
                }
            }
            best = max(best, cur);
        }
        return best;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n·B), B = 31 bits |
| **Space** | O(n·B) trie nodes |

**Pitfalls:** Starting from the least significant bit breaks the greedy; inserting before querying makes `x XOR x = 0` the floor, which is fine, but querying an empty trie would walk null children.

---

### LC 1268 · Search Suggestions System · Medium

> **Problem:** Given unique `products` and a `searchWord`, after typing each character of `searchWord` return up to three products that start with the typed prefix, in lexicographic order.

🔗 [https://leetcode.com/problems/search-suggestions-system/](https://leetcode.com/problems/search-suggestions-system/)

**Intuition:** Sort the products, then insert them into a trie in that order, storing at each node the first three words that pass through it; those are exactly the three smallest with that prefix. Answering is a single walk down `searchWord`, and once the walk falls off the trie every remaining answer is empty. Alternative: sort plus binary search for each prefix (`bisect_left`) and check the next three words.

**Python**

```python
class Solution:
    def suggestedProducts(self, products: list[str], searchWord: str) -> list[list[str]]:
        root = {}  # char -> child dict; key '#' holds up to 3 suggestions
        for p in sorted(products):
            node = root
            for ch in p:
                node = node.setdefault(ch, {})
                top = node.setdefault('#', [])
                if len(top) < 3:
                    top.append(p)
        res, node = [], root
        for ch in searchWord:
            node = node.get(ch, {})  # once off the trie, stays empty
            res.append(node.get('#', []))
        return res
```

**C++**

```cpp
class Solution {
    struct Node {
        int next[26];
        vector<int> top;  // indices of up to 3 smallest products with this prefix
        Node() { fill(begin(next), end(next), -1); }
    };
public:
    vector<vector<string>> suggestedProducts(vector<string>& products, string searchWord) {
        sort(products.begin(), products.end());
        vector<Node> trie(1);
        for (int i = 0; i < (int)products.size(); ++i) {
            int cur = 0;
            for (char ch : products[i]) {
                int c = ch - 'a';
                if (trie[cur].next[c] == -1) {
                    trie[cur].next[c] = trie.size();
                    trie.emplace_back();
                }
                cur = trie[cur].next[c];
                if (trie[cur].top.size() < 3) trie[cur].top.push_back(i);
            }
        }
        vector<vector<string>> res;
        int cur = 0;
        for (char ch : searchWord) {
            if (cur != -1) cur = trie[cur].next[ch - 'a'];  // -1 once off the trie
            vector<string> row;
            if (cur != -1)
                for (int i : trie[cur].top) row.push_back(products[i]);
            res.push_back(row);
        }
        return res;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(S log n + S) to sort and insert (S = total product characters, n = number of products), O(L) to answer, L = len(searchWord) |
| **Space** | O(S) trie nodes |

**Pitfalls:** Inserting unsorted products so the stored three are not the smallest; continuing to walk after a missing child (must return empty lists for the rest).

---

## 18. Dynamic Programming

Template and pitfalls: [LeetCode Patterns §18 Dynamic Programming](../computer-science/LeetCode_Patterns.md#18-dynamic-programming)

### LC 746 · Min Cost Climbing Stairs · Easy

> **Problem:** `cost[i]` is the cost of stepping on stair `i`; after paying it you may climb 1 or 2 stairs. You may start at stair 0 or 1. Return the minimum cost to reach the top (one past the last stair). `2 ≤ n ≤ 1000`.

🔗 [https://leetcode.com/problems/min-cost-climbing-stairs/](https://leetcode.com/problems/min-cost-climbing-stairs/)

**Intuition:** State: `dp[i]` = minimum cost to stand on position `i` (not yet paid `cost[i]`), with `dp[0] = dp[1] = 0`. Recurrence: `dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2])`, answer `dp[n]`. Each state looks back only two steps, so the full O(n) table collapses to two rolling variables.

**Python**

```python
class Solution:
    def minCostClimbingStairs(self, cost: list[int]) -> int:
        a = b = 0  # dp[i-2], dp[i-1]
        for i in range(2, len(cost) + 1):
            a, b = b, min(b + cost[i - 1], a + cost[i - 2])
        return b
```

**C++**

```cpp
class Solution {
public:
    int minCostClimbingStairs(vector<int>& cost) {
        int a = 0, b = 0;  // dp[i-2], dp[i-1]
        for (int i = 2; i <= (int)cost.size(); ++i) {
            int c = min(b + cost[i - 1], a + cost[i - 2]);
            a = b;
            b = c;
        }
        return b;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n) |
| **Space** | O(1) |

**Pitfalls:** The top is index `n`, not `n-1`; starting on stair 0 or 1 is free, so both base cases are 0 (not `cost[0]`/`cost[1]`).

---

### LC 518 · Coin Change II · Medium

> **Problem:** Given coin denominations `coins` (unlimited supply of each) and an `amount`, return the number of **combinations** (order does not matter) that make up `amount`. The answer fits in a signed 32-bit integer.

🔗 [https://leetcode.com/problems/coin-change-ii/](https://leetcode.com/problems/coin-change-ii/)

**Intuition:** State: `dp[c][a]` = ways to make `a` using only the first `c` coin types. Recurrence: `dp[c][a] = dp[c-1][a] + dp[c][a - coin_c]` (skip this coin entirely, or use it at least once more). Rolling over `c` gives a 1-D array where the **outer loop is over coins** and the inner loop goes upward over amounts, so each multiset is counted once in a fixed coin order -- contrast LC 377, whose swapped loops count ordered sequences.

**Python**

```python
class Solution:
    def change(self, amount: int, coins: list[int]) -> int:
        dp = [1] + [0] * amount
        for coin in coins:
            for a in range(coin, amount + 1):
                dp[a] += dp[a - coin]
        return dp[amount]
```

**C++**

```cpp
class Solution {
public:
    int change(int amount, vector<int>& coins) {
        // unsigned: intermediate counts can overflow int; wraparound is
        // defined and the final answer fits.
        vector<unsigned> dp(amount + 1, 0);
        dp[0] = 1;
        for (int coin : coins)
            for (int a = coin; a <= amount; ++a)
                dp[a] += dp[a - coin];
        return (int)dp[amount];
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n·A), n coins, A = amount |
| **Space** | O(A) |

**Pitfalls:** Swapping the loops counts permutations (wrong here); `amount = 0` → 1 (empty combination); signed overflow on intermediate `dp[a]` in C++.

---

### LC 152 · Maximum Product Subarray · Medium

> **Problem:** Given an integer array `nums` (values in `[-10, 10]`), return the largest product of a non-empty contiguous subarray. The answer fits in a 32-bit integer.

🔗 [https://leetcode.com/problems/maximum-product-subarray/](https://leetcode.com/problems/maximum-product-subarray/)

**Intuition:** State: `hi[i]` / `lo[i]` = maximum / minimum product of a subarray ending at `i`. Recurrence: `hi[i] = max(x, x·hi[i-1], x·lo[i-1])` and `lo[i] = min(x, x·hi[i-1], x·lo[i-1])` -- a negative `x` turns the smallest product into the largest, so both extremes must be carried (swap them when `x < 0`). Only the previous pair is needed, giving O(1) space; an equivalent trick is the max over prefix and suffix products, resetting at zeros.

**Python**

```python
class Solution:
    def maxProduct(self, nums: list[int]) -> int:
        hi = lo = best = nums[0]
        for x in nums[1:]:
            if x < 0:
                hi, lo = lo, hi
            hi = max(x, hi * x)
            lo = min(x, lo * x)
            best = max(best, hi)
        return best
```

**C++**

```cpp
class Solution {
public:
    int maxProduct(vector<int>& nums) {
        // double: the running minimum can exceed even 64-bit integers,
        // although the answer itself fits in int.
        double hi = nums[0], lo = nums[0], best = nums[0];
        for (size_t i = 1; i < nums.size(); ++i) {
            double x = nums[i];
            if (x < 0) swap(hi, lo);
            hi = max(x, hi * x);
            lo = min(x, lo * x);
            best = max(best, hi);
        }
        return (int)best;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n) |
| **Space** | O(1) |

**Pitfalls:** Tracking only the max fails on `[-2, 3, -4]`; zeros reset both extremes automatically via `max(x, ...)`; in C++ the running minimum can overflow `int` and `long long`, hence `double`.

---

### LC 62 · Unique Paths · Medium

> **Problem:** A robot starts at the top-left of an `m × n` grid and can only move right or down. Count the distinct paths to the bottom-right corner. `1 ≤ m, n ≤ 100`; the answer is ≤ 2·10^9.

🔗 [https://leetcode.com/problems/unique-paths/](https://leetcode.com/problems/unique-paths/)

**Intuition:** State: `dp[i][j]` = number of paths to cell `(i, j)`. Recurrence: `dp[i][j] = dp[i-1][j] + dp[i][j-1]`, with the first row and column all 1. Processing row by row, `dp[j]` still holds the value from the row above, so a single row of length `n` suffices (`dp[j] += dp[j-1]`). The closed form is `C(m+n-2, m-1)`, computable in O(min(m, n)).

**Python**

```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [1] * n
        for _ in range(1, m):
            for j in range(1, n):
                dp[j] += dp[j - 1]
        return dp[-1]
```

**C++**

```cpp
class Solution {
public:
    int uniquePaths(int m, int n) {
        vector<int> dp(n, 1);
        for (int i = 1; i < m; ++i)
            for (int j = 1; j < n; ++j)
                dp[j] += dp[j - 1];
        return dp[n - 1];
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(m·n) |
| **Space** | O(n) |

**Pitfalls:** Every intermediate count is ≤ the final answer (all cells reach the corner), so `int` is safe here; the combinatorial form needs care to avoid overflow (multiply then divide incrementally in `long long`).

---

### LC 63 · Unique Paths II · Medium

> **Problem:** Same as Unique Paths, but `obstacleGrid[i][j] == 1` marks a blocked cell that cannot be entered. Count paths from top-left to bottom-right. `1 ≤ m, n ≤ 100`; the answer is ≤ 2·10^9.

🔗 [https://leetcode.com/problems/unique-paths-ii/](https://leetcode.com/problems/unique-paths-ii/)

**Intuition:** State: `dp[i][j]` = number of paths to `(i, j)`. Recurrence: `dp[i][j] = 0` if the cell is an obstacle, else `dp[i-1][j] + dp[i][j-1]`, with `dp[0][0] = 1` iff the start is open. The same single-row rolling array as LC 62 works; obstacles simply zero their slot, which also handles a blocked first row/column without special cases.

**Python**

```python
class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: list[list[int]]) -> int:
        n = len(obstacleGrid[0])
        dp = [0] * n
        dp[0] = 1
        for row in obstacleGrid:
            for j in range(n):
                if row[j]:
                    dp[j] = 0
                elif j:
                    dp[j] += dp[j - 1]
        return dp[-1]
```

**C++**

```cpp
class Solution {
public:
    int uniquePathsWithObstacles(vector<vector<int>>& obstacleGrid) {
        int n = obstacleGrid[0].size();
        // unsigned: counts at cells that cannot reach the goal may exceed int;
        // wraparound is defined and the true answer fits.
        vector<unsigned> dp(n, 0);
        dp[0] = 1;
        for (auto& row : obstacleGrid)
            for (int j = 0; j < n; ++j) {
                if (row[j]) dp[j] = 0;
                else if (j) dp[j] += dp[j - 1];
            }
        return (int)dp[n - 1];
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(m·n), m×n grid |
| **Space** | O(n) |

**Pitfalls:** Obstacle on the start or goal → 0; unlike LC 62, intermediate counts at dead-end cells can overflow a signed `int` in C++.

---

### LC 64 · Minimum Path Sum · Medium

> **Problem:** Given an `m × n` grid of non-negative integers, find a path from top-left to bottom-right (moving only right or down) that minimizes the sum of the numbers along it, and return that sum.

🔗 [https://leetcode.com/problems/minimum-path-sum/](https://leetcode.com/problems/minimum-path-sum/)

**Intuition:** State: `dp[i][j]` = minimum path sum ending at `(i, j)`. Recurrence: `dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])`, where out-of-grid neighbours are +inf (so the first row/column are prefix sums). A single row rolls the table to O(n) space; overwriting `grid` in place gives O(1) extra if mutation is allowed.

**Python**

```python
class Solution:
    def minPathSum(self, grid: list[list[int]]) -> int:
        n = len(grid[0])
        dp = [float("inf")] * n
        dp[0] = 0
        for row in grid:
            dp[0] += row[0]
            for j in range(1, n):
                dp[j] = row[j] + min(dp[j], dp[j - 1])
        return dp[-1]
```

**C++**

```cpp
class Solution {
public:
    int minPathSum(vector<vector<int>>& grid) {
        int n = grid[0].size();
        vector<int> dp(n, INT_MAX);
        dp[0] = 0;
        for (auto& row : grid) {
            dp[0] += row[0];
            for (int j = 1; j < n; ++j)
                dp[j] = row[j] + min(dp[j], dp[j - 1]);
        }
        return dp[n - 1];
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(m·n), m×n grid |
| **Space** | O(n) |

**Pitfalls:** Initialize the first row as "unreachable from above" (+inf), not 0, or the first row takes free values; never add to `INT_MAX` (here `min` always picks the finite left neighbour first).

---

### LC 120 · Triangle · Medium

> **Problem:** Given a triangle array (row `i` has `i+1` numbers), return the minimum path sum from top to bottom, where from index `j` you may move to index `j` or `j+1` in the next row. Follow-up: O(n) extra space, n = number of rows.

🔗 [https://leetcode.com/problems/triangle/](https://leetcode.com/problems/triangle/)

**Intuition:** State: `dp[i][j]` = minimum path sum from `(i, j)` down to the bottom. Recurrence: `dp[i][j] = triangle[i][j] + min(dp[i+1][j], dp[i+1][j+1])`, base case the last row. Going bottom-up means the answer converges to `dp[0][0]` with no boundary checks, and since row `i` only reads row `i+1` at indices `>= j`, one array of length n updated left to right suffices.

**Python**

```python
class Solution:
    def minimumTotal(self, triangle: list[list[int]]) -> int:
        dp = triangle[-1][:]
        for i in range(len(triangle) - 2, -1, -1):
            for j in range(i + 1):
                dp[j] = triangle[i][j] + min(dp[j], dp[j + 1])
        return dp[0]
```

**C++**

```cpp
class Solution {
public:
    int minimumTotal(vector<vector<int>>& triangle) {
        vector<int> dp = triangle.back();
        for (int i = (int)triangle.size() - 2; i >= 0; --i)
            for (int j = 0; j <= i; ++j)
                dp[j] = triangle[i][j] + min(dp[j], dp[j + 1]);
        return dp[0];
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n^2), n rows |
| **Space** | O(n) |

**Pitfalls:** Top-down needs boundary handling at both row ends plus a final `min` over the last row; values can be negative, so do not prune early.

---

### LC 279 · Perfect Squares · Medium

> **Problem:** Return the least number of perfect squares (1, 4, 9, ...) that sum to `n`. `1 ≤ n ≤ 10^4`.

🔗 [https://leetcode.com/problems/perfect-squares/](https://leetcode.com/problems/perfect-squares/)

**Intuition:** State: `dp[i]` = fewest squares summing to `i`, `dp[0] = 0`. Recurrence: `dp[i] = 1 + min(dp[i - k^2])` over all `k^2 ≤ i` -- an unbounded knapsack over the square "coins". There are sqrt(i) choices per state, giving O(n·sqrt(n)). A math shortcut (Lagrange's four-square theorem plus Legendre's three-square condition) answers in O(sqrt(n)), but the DP is the expected interview solution.

**Python**

```python
class Solution:
    def numSquares(self, n: int) -> int:
        squares = [k * k for k in range(1, int(n**0.5) + 1)]
        dp = [0] + [n] * n  # n ones is always an upper bound
        for i in range(1, n + 1):
            for sq in squares:
                if sq > i:
                    break
                dp[i] = min(dp[i], dp[i - sq] + 1)
        return dp[n]
```

**C++**

```cpp
class Solution {
public:
    int numSquares(int n) {
        vector<int> dp(n + 1, n);  // n ones is always an upper bound
        dp[0] = 0;
        for (int i = 1; i <= n; ++i)
            for (int k = 1; k * k <= i; ++k)
                dp[i] = min(dp[i], dp[i - k * k] + 1);
        return dp[n];
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n·sqrt(n)) |
| **Space** | O(n) |

**Pitfalls:** Greedy (take the largest square first) is wrong: 12 = 4+4+4, not 9+1+1+1; Python's DP is slow near n = 10^4 -- precompute squares and `break` early, or use BFS / the math solution.

---

### LC 377 · Combination Sum IV · Medium

> **Problem:** Given an array of **distinct** positive integers `nums` and a `target`, return the number of possible **ordered** sequences (despite the name) of elements of `nums`, with repetition, that sum to `target`. The answer fits in a 32-bit integer.

🔗 [https://leetcode.com/problems/combination-sum-iv/](https://leetcode.com/problems/combination-sum-iv/)

**Intuition:** State: `dp[t]` = number of ordered sequences summing to `t`, `dp[0] = 1`. Recurrence: `dp[t] = sum(dp[t - x])` over all `x` in `nums` with `x ≤ t` -- condition on the **last** element of the sequence. Here the **outer loop is over the target** and the inner over `nums`, so every element may appear in every position; this is exactly LC 518 with the loops swapped, which turns combinations into permutations. Follow-up: negative numbers make the count infinite (cycles like `+1, -1`) unless sequence length is bounded.

**Python**

```python
class Solution:
    def combinationSum4(self, nums: list[int], target: int) -> int:
        dp = [1] + [0] * target
        for t in range(1, target + 1):
            for x in nums:
                if x <= t:
                    dp[t] += dp[t - x]
        return dp[target]
```

**C++**

```cpp
class Solution {
public:
    int combinationSum4(vector<int>& nums, int target) {
        // unsigned: intermediate dp[t] can exceed even 64-bit; wraparound is
        // defined and the final answer fits.
        vector<unsigned> dp(target + 1, 0);
        dp[0] = 1;
        for (int t = 1; t <= target; ++t)
            for (int x : nums)
                if (x <= t) dp[t] += dp[t - x];
        return (int)dp[target];
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(T·n), T = target, n = len(nums) |
| **Space** | O(T) |

**Pitfalls:** In C++ intermediate `dp[t]` for sums that cannot extend to `target` can overflow even `long long` (signed overflow is UB → use `unsigned`); loop order coins-outer would give LC 518's answer instead.

---

### LC 647 · Palindromic Substrings · Medium

> **Problem:** Return the number of palindromic substrings of `s` (substrings at different positions count separately). `1 ≤ |s| ≤ 1000`.

🔗 [https://leetcode.com/problems/palindromic-substrings/](https://leetcode.com/problems/palindromic-substrings/)

**Intuition:** State: `dp[i][j]` = whether `s[i..j]` is a palindrome. Recurrence: `dp[i][j] = s[i] == s[j] and (j - i < 2 or dp[i+1][j-1])`; count the true entries. Filling `i` from right to left and `j` from right to left lets one row hold the table: `dp[j-1]` is still row `i+1` when `dp[j]` is computed. Expand-around-center (2n-1 centers) achieves the same O(n^2) time with O(1) space; Manacher's is O(n).

**Python**

```python
class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        dp = [False] * n  # dp[j] = s[i..j] is a palindrome, for the current i
        count = 0
        for i in range(n - 1, -1, -1):
            for j in range(n - 1, i - 1, -1):  # descending keeps dp[j-1] = row i+1
                dp[j] = s[i] == s[j] and (j - i < 2 or dp[j - 1])
                count += dp[j]
        return count
```

**C++**

```cpp
class Solution {
public:
    int countSubstrings(string s) {
        int n = s.size(), count = 0;
        vector<char> dp(n, 0);  // dp[j] = s[i..j] is a palindrome, for the current i
        for (int i = n - 1; i >= 0; --i)
            for (int j = n - 1; j >= i; --j) {  // descending keeps dp[j-1] = row i+1
                dp[j] = s[i] == s[j] && (j - i < 2 || dp[j - 1]);
                count += dp[j];
            }
        return count;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n^2) |
| **Space** | O(n) |

**Pitfalls:** Iterating `j` ascending overwrites `dp[j-1]` with row `i` before it is read; the `j - i < 2` base case covers both single chars and equal pairs.

---

### LC 516 · Longest Palindromic Subsequence · Medium

> **Problem:** Return the length of the longest subsequence of `s` that reads the same forwards and backwards (characters need not be contiguous). `1 ≤ |s| ≤ 1000`.

🔗 [https://leetcode.com/problems/longest-palindromic-subsequence/](https://leetcode.com/problems/longest-palindromic-subsequence/)

**Intuition:** State: `dp[i][j]` = length of the longest palindromic subsequence of `s[i..j]`, with `dp[i][i] = 1`. Recurrence: if `s[i] == s[j]`, `dp[i][j] = dp[i+1][j-1] + 2` (wrap both ends around the inner answer); otherwise `dp[i][j] = max(dp[i+1][j], dp[i][j-1])` (drop one end). Filling `i` from right to left and `j` left to right, one row holds the table if a `prev` variable saves the old `dp[j-1]` (that is, `dp[i+1][j-1]`) before it is overwritten. Equivalently, the answer is the LCS of `s` and `reversed(s)`.

**Python**

```python
class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        n = len(s)
        dp = [0] * n  # dp[j] = LPS of s[i..j] for the current i
        for i in range(n - 1, -1, -1):
            dp[i] = 1
            prev = 0  # dp[i+1][j-1]; empty range when j == i+1
            for j in range(i + 1, n):
                below = dp[j]  # dp[i+1][j]
                dp[j] = prev + 2 if s[i] == s[j] else max(below, dp[j - 1])
                prev = below
        return dp[n - 1]
```

**C++**

```cpp
class Solution {
public:
    int longestPalindromeSubseq(string s) {
        int n = s.size();
        vector<int> dp(n, 0);  // dp[j] = LPS of s[i..j] for the current i
        for (int i = n - 1; i >= 0; --i) {
            dp[i] = 1;
            int prev = 0;  // dp[i+1][j-1]; empty range when j == i+1
            for (int j = i + 1; j < n; ++j) {
                int below = dp[j];  // dp[i+1][j]
                dp[j] = s[i] == s[j] ? prev + 2 : max(below, dp[j - 1]);
                prev = below;
            }
        }
        return dp[n - 1];
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n^2) |
| **Space** | O(n) (O(n^2) for the full table) |

**Pitfalls:** Subsequence, not substring (contrast LC 647 / LC 5); `prev` must start at 0 for each `i`, not at the stale `dp[i]` left over from the row below; `i` must run right to left so row `i+1` is ready.

---

### LC 97 · Interleaving String · Medium

> **Problem:** Return whether `s3` is formed by interleaving `s1` and `s2`, i.e. merging them while preserving the relative order of characters within each. Follow-up: O(|s2|) extra space.

🔗 [https://leetcode.com/problems/interleaving-string/](https://leetcode.com/problems/interleaving-string/)

**Intuition:** State: `dp[i][j]` = whether `s1[:i]` and `s2[:j]` interleave to `s3[:i+j]`. Recurrence: `dp[i][j] = (dp[i-1][j] and s1[i-1] == s3[i+j-1]) or (dp[i][j-1] and s2[j-1] == s3[i+j-1])` -- the last character of `s3[:i+j]` came from one of the two strings. Row `i` needs only row `i-1` and the current row's left neighbour, so a 1-D array of size `|s2|+1` meets the follow-up. Greedy matching fails when both strings offer the same next character.

**Python**

```python
class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        m, n = len(s1), len(s2)
        if m + n != len(s3):
            return False
        dp = [False] * (n + 1)
        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0 and j == 0:
                    dp[j] = True
                    continue
                from1 = i > 0 and dp[j] and s1[i - 1] == s3[i + j - 1]
                from2 = j > 0 and dp[j - 1] and s2[j - 1] == s3[i + j - 1]
                dp[j] = from1 or from2
        return dp[n]
```

**C++**

```cpp
class Solution {
public:
    bool isInterleave(string s1, string s2, string s3) {
        int m = s1.size(), n = s2.size();
        if (m + n != (int)s3.size()) return false;
        vector<char> dp(n + 1, 0);
        for (int i = 0; i <= m; ++i)
            for (int j = 0; j <= n; ++j) {
                if (i == 0 && j == 0) { dp[j] = 1; continue; }
                bool from1 = i > 0 && dp[j] && s1[i - 1] == s3[i + j - 1];
                bool from2 = j > 0 && dp[j - 1] && s2[j - 1] == s3[i + j - 1];
                dp[j] = from1 || from2;
            }
        return dp[n];
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(m·n), m = \|s1\|, n = \|s2\| |
| **Space** | O(n) |

**Pitfalls:** Check `m + n == |s3|` first (otherwise indices run off `s3`); all-empty strings → true; a two-pointer greedy is wrong (`s1="aabcc", s2="dbbca"`).

---

### LC 115 · Distinct Subsequences · Hard

> **Problem:** Return the number of distinct subsequences of `s` that equal `t` (i.e. the number of ways to delete characters from `s` to obtain `t`). `1 ≤ |s|, |t| ≤ 1000`; the answer fits in a 32-bit signed integer.

🔗 [https://leetcode.com/problems/distinct-subsequences/](https://leetcode.com/problems/distinct-subsequences/)

**Intuition:** State: `dp[i][j]` = number of ways `s[:i]` contains `t[:j]` as a subsequence, with `dp[i][0] = 1`. Recurrence: `dp[i][j] = dp[i-1][j] + (s[i-1] == t[j-1] ? dp[i-1][j-1] : 0)` -- either skip `s[i-1]` or use it to match `t[j-1]`. Rolling over `i` with `j` iterated **downward** lets `dp[j-1]` still hold the row `i-1` value, giving O(|t|) space.

**Python**

```python
class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        n = len(t)
        dp = [1] + [0] * n
        for ch in s:
            for j in range(n, 0, -1):  # descending: dp[j-1] is still the previous row
                if t[j - 1] == ch:
                    dp[j] += dp[j - 1]
        return dp[n]
```

**C++**

```cpp
class Solution {
public:
    int numDistinct(string s, string t) {
        int n = t.size();
        // unsigned: intermediate counts for prefixes of t can exceed even 64-bit;
        // wraparound is defined and the final answer fits.
        vector<unsigned> dp(n + 1, 0);
        dp[0] = 1;
        for (char ch : s)
            for (int j = n; j >= 1; --j)  // descending: dp[j-1] is still the previous row
                if (t[j - 1] == ch) dp[j] += dp[j - 1];
        return (int)dp[n];
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(m·n), m = \|s\|, n = \|t\| |
| **Space** | O(n) |

**Pitfalls:** Ascending `j` lets one `s` character match several `t` positions; `|t| > |s|` → 0; in C++ intermediate `dp[j]` can overflow even `long long`, so use `unsigned`.

---

### LC 10 · Regular Expression Matching · Hard

> **Problem:** Implement full-string matching of `s` against pattern `p`, where `.` matches any single character and `*` matches zero or more of the preceding element. `|s| ≤ 20`, `|p| ≤ 20`; every `*` is preceded by a valid character.

🔗 [https://leetcode.com/problems/regular-expression-matching/](https://leetcode.com/problems/regular-expression-matching/)

**Intuition:** State: `dp[i][j]` = whether suffix `s[i:]` matches suffix `p[j:]`, with `dp[m][n] = true`. Let `first = i < m and p[j] in {s[i], '.'}`. Recurrence: if `p[j+1] == '*'`, `dp[i][j] = dp[i][j+2]` (use `x*` zero times) `or (first and dp[i+1][j])` (consume one char, keep `x*`); otherwise `dp[i][j] = first and dp[i+1][j+1]`. The full table is clearest here; it can be rolled to two rows of length `n+1` since row `i` reads only rows `i` and `i+1`.

**Python**

```python
class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        m, n = len(s), len(p)
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[m][n] = True
        for i in range(m, -1, -1):  # i == m: empty suffix of s
            for j in range(n - 1, -1, -1):
                first = i < m and p[j] in (s[i], ".")
                if j + 1 < n and p[j + 1] == "*":
                    dp[i][j] = dp[i][j + 2] or (first and dp[i + 1][j])
                else:
                    dp[i][j] = first and dp[i + 1][j + 1]
        return dp[0][0]
```

**C++**

```cpp
class Solution {
public:
    bool isMatch(string s, string p) {
        int m = s.size(), n = p.size();
        vector<vector<char>> dp(m + 1, vector<char>(n + 1, 0));
        dp[m][n] = 1;
        for (int i = m; i >= 0; --i)  // i == m: empty suffix of s
            for (int j = n - 1; j >= 0; --j) {
                bool first = i < m && (p[j] == s[i] || p[j] == '.');
                if (j + 1 < n && p[j + 1] == '*')
                    dp[i][j] = dp[i][j + 2] || (first && dp[i + 1][j]);
                else
                    dp[i][j] = first && dp[i + 1][j + 1];
            }
        return dp[0][0];
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(m·n), m = \|s\|, n = \|p\| |
| **Space** | O(m·n) (O(n) with two rolling rows) |

**Pitfalls:** The row `i == m` must be computed (patterns like `a*b*` match the empty string); `*` binds to the previous element, so check `p[j+1]`, not `p[j]`; `first` must guard `i < m` before indexing `s`.

---

### LC 32 · Longest Valid Parentheses · Hard

> **Problem:** Given a string of `'('` and `')'`, return the length of the longest well-formed (valid) parentheses substring. `0 ≤ |s| ≤ 3·10^4`.

🔗 [https://leetcode.com/problems/longest-valid-parentheses/](https://leetcode.com/problems/longest-valid-parentheses/)

**Intuition:** State: `dp[i]` = length of the longest valid substring **ending at** `i` (0 if `s[i] == '('`). Recurrence for `s[i] == ')'`: if `s[i-1] == '('`, `dp[i] = dp[i-2] + 2`; else let `k = i - dp[i-1] - 1` (the char just before the valid block ending at `i-1`) and if `s[k] == '('`, `dp[i] = dp[i-1] + 2 + dp[k-1]` -- the trailing `dp[k-1]` glues on an adjacent valid block. Alternatives: a stack of indices (O(n) space), or two counter passes left→right and right→left for O(1) space.

**Python**

```python
class Solution:
    def longestValidParentheses(self, s: str) -> int:
        n = len(s)
        dp = [0] * n
        for i in range(1, n):
            if s[i] != ")":
                continue
            if s[i - 1] == "(":
                dp[i] = (dp[i - 2] if i >= 2 else 0) + 2
            else:
                k = i - dp[i - 1] - 1
                if k >= 0 and s[k] == "(":
                    dp[i] = dp[i - 1] + 2 + (dp[k - 1] if k >= 1 else 0)
        return max(dp, default=0)
```

**C++**

```cpp
class Solution {
public:
    int longestValidParentheses(string s) {
        int n = s.size(), best = 0;
        vector<int> dp(n, 0);
        for (int i = 1; i < n; ++i) {
            if (s[i] != ')') continue;
            if (s[i - 1] == '(') {
                dp[i] = (i >= 2 ? dp[i - 2] : 0) + 2;
            } else {
                int k = i - dp[i - 1] - 1;
                if (k >= 0 && s[k] == '(')
                    dp[i] = dp[i - 1] + 2 + (k >= 1 ? dp[k - 1] : 0);
            }
            best = max(best, dp[i]);
        }
        return best;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n) |
| **Space** | O(n) |

**Pitfalls:** In Python `dp[-1]` silently wraps (guard `i >= 2` / `k >= 1`); forgetting the `dp[k-1]` term misses `"()(())"` → 6; empty string → 0.

---

## 19. Greedy

Template and pitfalls: [LeetCode Patterns §19 Greedy](../computer-science/LeetCode_Patterns.md#19-greedy)

### LC 763 · Partition Labels · Medium

> **Problem:** Split string `s` (lowercase letters) into as many parts as possible so that each letter appears in at most one part, and return the sizes of the parts in order.

🔗 [https://leetcode.com/problems/partition-labels/](https://leetcode.com/problems/partition-labels/)

**Intuition:** A part that contains letter `c` must extend at least to the last occurrence of `c`. Record each letter's last index, then sweep left to right growing the current part's `end` to the max last-index seen; when `i == end`, nothing inside the part appears later, so cut there. Cutting as early as possible maximizes the number of parts, in one O(n) pass.

**Python**

```python
class Solution:
    def partitionLabels(self, s: str) -> list[int]:
        last = {c: i for i, c in enumerate(s)}
        res, start, end = [], 0, 0
        for i, c in enumerate(s):
            end = max(end, last[c])
            if i == end:  # every letter in s[start..i] ends by i
                res.append(end - start + 1)
                start = i + 1
        return res
```

**C++**

```cpp
class Solution {
public:
    vector<int> partitionLabels(string s) {
        int last[26] = {};
        for (int i = 0; i < (int)s.size(); ++i) last[s[i] - 'a'] = i;
        vector<int> res;
        int start = 0, end = 0;
        for (int i = 0; i < (int)s.size(); ++i) {
            end = max(end, last[s[i] - 'a']);
            if (i == end) {  // every letter in s[start..i] ends by i
                res.push_back(end - start + 1);
                start = i + 1;
            }
        }
        return res;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n), n = len(s) |
| **Space** | O(1) (26-letter table, excluding output) |

**Pitfalls:** Extend `end` before checking `i == end`; forgetting to reset `start = i + 1` gives cumulative instead of per-part sizes.

---

### LC 846 · Hand of Straights · Medium

> **Problem:** Given card values `hand` and an integer `groupSize`, return whether the cards can be rearranged into groups of `groupSize` consecutive values (every card used exactly once).

🔗 [https://leetcode.com/problems/hand-of-straights/](https://leetcode.com/problems/hand-of-straights/)

**Intuition:** The smallest remaining card can only be the start of a group, so greedily open as many groups at the smallest value as it has copies (`need`) and consume `need` copies of each of the next `groupSize - 1` values. Iterating distinct values in sorted order makes this a single sweep; each group start consumes `groupSize` cards, so the inner work totals O(n) after the O(n log n) sort.

**Python**

```python
from collections import Counter


class Solution:
    def isNStraightHand(self, hand: list[int], groupSize: int) -> bool:
        if len(hand) % groupSize:
            return False
        cnt = Counter(hand)
        for x in sorted(cnt):
            need = cnt[x]  # groups that must start at x
            if need == 0:
                continue
            for y in range(x, x + groupSize):
                if cnt[y] < need:
                    return False
                cnt[y] -= need
        return True
```

**C++**

```cpp
class Solution {
public:
    bool isNStraightHand(vector<int>& hand, int groupSize) {
        if (hand.size() % groupSize) return false;
        map<int, int> cnt;
        for (int x : hand) ++cnt[x];
        for (auto& [x, c] : cnt) {
            int need = c;  // groups that must start at x
            if (need == 0) continue;
            for (int y = x; y < x + groupSize; ++y) {
                auto it = cnt.find(y);
                if (it == cnt.end() || it->second < need) return false;
                it->second -= need;
            }
        }
        return true;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n log n), n = len(hand) |
| **Space** | O(n) |

**Pitfalls:** Copy the count into `need` before the inner loop (it zeroes `cnt[x]` itself); check `len % groupSize` early; `groupSize == 1` is always true.

---

### LC 678 · Valid Parenthesis String · Medium

> **Problem:** Given a string of `'('`, `')'` and `'*'`, where `'*'` may act as `'('`, `')'` or the empty string, return whether some interpretation makes it a valid parentheses string.

🔗 [https://leetcode.com/problems/valid-parenthesis-string/](https://leetcode.com/problems/valid-parenthesis-string/)

**Intuition:** Instead of branching on every `'*'` (exponential) or doing O(n^2) DP, track the range `[lo, hi]` of possible open-bracket counts. `'('` raises both, `')'` lowers both, `'*'` widens the range by one each way. If `hi < 0` even the most generous choice has too many `')'`; clamp `lo` at 0 since counts cannot go negative. The string is valid iff 0 is reachable at the end, i.e. `lo == 0`.

**Python**

```python
class Solution:
    def checkValidString(self, s: str) -> bool:
        lo = hi = 0  # min / max possible number of unmatched '('
        for c in s:
            if c == '(':
                lo, hi = lo + 1, hi + 1
            elif c == ')':
                lo, hi = lo - 1, hi - 1
            else:
                lo, hi = lo - 1, hi + 1
            if hi < 0:
                return False
            lo = max(lo, 0)
        return lo == 0
```

**C++**

```cpp
class Solution {
public:
    bool checkValidString(string s) {
        int lo = 0, hi = 0;  // min / max possible number of unmatched '('
        for (char c : s) {
            if (c == '(') { ++lo; ++hi; }
            else if (c == ')') { --lo; --hi; }
            else { --lo; ++hi; }
            if (hi < 0) return false;
            lo = max(lo, 0);
        }
        return lo == 0;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n) |
| **Space** | O(1) |

**Pitfalls:** Check `hi < 0` before clamping `lo`; without the clamp, testing `lo <= 0 <= hi` at the end wrongly accepts `"*)("`.

---

## 20. Bit Manipulation

Template and pitfalls: [LeetCode Patterns §20 Bit Manipulation](../computer-science/LeetCode_Patterns.md#20-bit-manipulation)

### LC 338 · Counting Bits · Easy

> **Problem:** Given `n`, return an array `ans` of length `n + 1` where `ans[i]` is the number of 1 bits in `i`.

🔗 [https://leetcode.com/problems/counting-bits/](https://leetcode.com/problems/counting-bits/)

**Intuition:** `i >> 1` drops the lowest bit of `i` and is smaller than `i`, so its answer is already known: `ans[i] = ans[i >> 1] + (i & 1)`. This gives the O(n) single-pass answer the follow-up asks for, versus O(n log n) for counting each number's bits separately. (Equivalent: `ans[i] = ans[i & (i - 1)] + 1`.)

**Python**

```python
class Solution:
    def countBits(self, n: int) -> list[int]:
        ans = [0] * (n + 1)
        for i in range(1, n + 1):
            ans[i] = ans[i >> 1] + (i & 1)
        return ans
```

**C++**

```cpp
class Solution {
public:
    vector<int> countBits(int n) {
        vector<int> ans(n + 1, 0);
        for (int i = 1; i <= n; ++i) ans[i] = ans[i >> 1] + (i & 1);
        return ans;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n) |
| **Space** | O(1) extra (O(n) output) |

**Pitfalls:** Output has `n + 1` entries (include 0); `n = 0` returns `[0]`.

---

### LC 190 · Reverse Bits · Easy

> **Problem:** Reverse the bits of a 32-bit integer `n` and return the result (bit 0 becomes bit 31, and so on).

🔗 [https://leetcode.com/problems/reverse-bits/](https://leetcode.com/problems/reverse-bits/)

**Intuition:** Pop the low bit of `n` and push it onto the low end of `res` 32 times; after the loop the first bit popped has been shifted all the way to bit 31. Always loop exactly 32 times so leading zeros of `n` become trailing zeros of `res`. Follow-up (called many times): reverse with five mask-and-swap steps (16, 8, 4, 2, 1 bits) or a 256-entry byte lookup table.

**Python**

```python
class Solution:
    def reverseBits(self, n: int) -> int:
        res = 0
        for _ in range(32):
            res = (res << 1) | (n & 1)
            n >>= 1
        return res
```

**C++**

```cpp
class Solution {
public:
    uint32_t reverseBits(uint32_t n) {
        uint32_t res = 0;
        for (int i = 0; i < 32; ++i) {
            res = (res << 1) | (n & 1);
            n >>= 1;
        }
        return res;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(32) = O(1) |
| **Space** | O(1) |

**Pitfalls:** Stopping when `n == 0` drops the trailing zeros; in C++ use an unsigned type so `res << 1` into bit 31 is well-defined (newer versions of the problem pass a signed `int` with `n` even, and the same loop works).

---

### LC 371 · Sum of Two Integers · Medium

> **Problem:** Given two integers `a` and `b` (`-1000 ≤ a, b ≤ 1000`), return their sum without using the `+` or `-` operators.

🔗 [https://leetcode.com/problems/sum-of-two-integers/](https://leetcode.com/problems/sum-of-two-integers/)

**Intuition:** `a ^ b` is the sum ignoring carries and `(a & b) << 1` is exactly the carries; repeat "sum = xor, carry = and-shift" until no carry remains (at most 32 rounds). In C++ do it on `unsigned` so shifting a carry into the sign bit is well-defined and wraparound emulates two's complement. Python integers are unbounded, so a negative operand's carry would ripple left forever: mask every step to 32 bits, then convert the 32-bit result back to a signed value (`~(a ^ mask)` sign-extends when bit 31 is set).

**Python**

```python
class Solution:
    def getSum(self, a: int, b: int) -> int:
        mask = 0xFFFFFFFF
        a, b = a & mask, b & mask  # view both as 32-bit two's complement
        while b:
            a, b = (a ^ b) & mask, ((a & b) << 1) & mask
        return a if a <= 0x7FFFFFFF else ~(a ^ mask)  # back to signed
```

**C++**

```cpp
class Solution {
public:
    int getSum(int a, int b) {
        unsigned x = a, y = b;  // unsigned: carry into bit 31 is well-defined
        while (y) {
            unsigned carry = (x & y) << 1;
            x ^= y;
            y = carry;
        }
        return (int)x;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(32) = O(1) |
| **Space** | O(1) |

**Pitfalls:** Python without the 32-bit mask loops forever on mixed signs (e.g. `-1 + 1`); left-shifting a negative `int` in C++ is undefined before C++20, hence the `unsigned` copies.

---

### LC 201 · Bitwise AND of Numbers Range · Medium

> **Problem:** Given `0 ≤ left ≤ right ≤ 2^31 - 1`, return the bitwise AND of all integers in `[left, right]`.

🔗 [https://leetcode.com/problems/bitwise-and-of-numbers-range/](https://leetcode.com/problems/bitwise-and-of-numbers-range/)

**Intuition:** Any bit below the highest position where `left` and `right` differ flips to 0 somewhere inside the range, so the answer is their common binary prefix followed by zeros. Brian Kernighan's trick finds it without iterating the range: keep clearing the lowest set bit of `right` (`right &= right - 1`) until `right ≤ left`; what remains is the common prefix. At most 31 iterations.

**Python**

```python
class Solution:
    def rangeBitwiseAnd(self, left: int, right: int) -> int:
        while left < right:
            right &= right - 1  # drop lowest set bit
        return right
```

**C++**

```cpp
class Solution {
public:
    int rangeBitwiseAnd(int left, int right) {
        while (left < right) right &= right - 1;  // drop lowest set bit
        return right;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(log right) ≤ 31 iterations |
| **Space** | O(1) |

**Pitfalls:** Looping `for i in range(left, right + 1)` is O(2^31) and TLEs; `left == right` must return `left` itself; `left = 0` gives 0.

---

### LC 7 · Reverse Integer · Medium

> **Problem:** Given a signed 32-bit integer `x`, return `x` with its digits reversed, or 0 if the result falls outside `[-2^31, 2^31 - 1]`. Assume 64-bit integers are not available.

🔗 [https://leetcode.com/problems/reverse-integer/](https://leetcode.com/problems/reverse-integer/)

**Intuition:** Peel digits off the end with `% 10` / `/ 10` and append them to `rev`. To respect the no-64-bit rule, check for overflow *before* `rev * 10 + d`: if `|rev| > 214748364` it must overflow. The equality case `|rev| == 214748364` cannot overflow, because it only happens on the 10th digit, which is the leading digit of `x` and therefore at most 2.

**Python**

```python
class Solution:
    def reverse(self, x: int) -> int:
        sign = -1 if x < 0 else 1
        x, rev = abs(x), 0
        while x:
            x, d = divmod(x, 10)
            if rev > (2**31 - 1) // 10:  # rev * 10 would already overflow
                return 0
            rev = rev * 10 + d
        return sign * rev
```

**C++**

```cpp
class Solution {
public:
    int reverse(int x) {
        int rev = 0;
        while (x != 0) {
            int d = x % 10;  // truncates toward zero, so d < 0 when x < 0
            x /= 10;
            if (rev > INT_MAX / 10 || rev < INT_MIN / 10) return 0;
            rev = rev * 10 + d;
        }
        return rev;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(log10 \|x\|) (at most 10 digits) |
| **Space** | O(1) |

**Pitfalls:** In C++ never take `abs(INT_MIN)` (overflow) -- work with the signed remainder instead; Python's `%` floors for negatives, so strip the sign first; trailing zeros vanish (`120 → 21`).

---

## 21. Prefix Sum & Difference Array

Template and pitfalls: [LeetCode Patterns §21 Prefix Sum & Difference Array](../computer-science/LeetCode_Patterns.md#21-prefix-sum--difference-array)

### LC 303 · Range Sum Query - Immutable · Easy

> **Problem:** Design `NumArray(nums)` with `sumRange(left, right)` returning the sum of `nums[left..right]` inclusive; `sumRange` is called many times on the unchanging array.

🔗 [https://leetcode.com/problems/range-sum-query-immutable/](https://leetcode.com/problems/range-sum-query-immutable/)

**Intuition:** Precompute `pre[i] = nums[0] + ... + nums[i-1]` with `pre[0] = 0`; then any range sum is `pre[right + 1] - pre[left]` in O(1). The leading zero removes the `left == 0` special case. (For updates too, see LC 307: Fenwick / segment tree.)

**Python**

```python
class NumArray:
    def __init__(self, nums: list[int]):
        self.pre = [0]
        for x in nums:
            self.pre.append(self.pre[-1] + x)

    def sumRange(self, left: int, right: int) -> int:
        return self.pre[right + 1] - self.pre[left]
```

**C++**

```cpp
class NumArray {
    vector<int> pre;  // pre[i] = sum of nums[0..i-1]
public:
    NumArray(vector<int>& nums) : pre(nums.size() + 1, 0) {
        for (size_t i = 0; i < nums.size(); ++i) pre[i + 1] = pre[i] + nums[i];
    }

    int sumRange(int left, int right) {
        return pre[right + 1] - pre[left];
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n) build, O(1) per query |
| **Space** | O(n) |

**Pitfalls:** Off-by-one between inclusive `right` and the shifted prefix (`pre[right + 1]`); summing the slice per query is O(n) and TLEs with 10^4 queries.

---

### LC 974 · Subarray Sums Divisible by K · Medium

> **Problem:** Given an integer array `nums` (values may be negative) and `k` (`2 ≤ k`), return the number of non-empty contiguous subarrays whose sum is divisible by `k`.

🔗 [https://leetcode.com/problems/subarray-sums-divisible-by-k/](https://leetcode.com/problems/subarray-sums-divisible-by-k/)

**Intuition:** A subarray sum `pre[j] - pre[i]` is divisible by `k` iff `pre[i] % k == pre[j] % k`. Sweep once, keeping a count of each prefix remainder seen (seeded with remainder 0 once for the empty prefix); each new prefix pairs with every earlier prefix of the same remainder. O(n) versus O(n^2) for checking all subarrays.

**Python**

```python
class Solution:
    def subarraysDivByK(self, nums: list[int], k: int) -> int:
        cnt = [0] * k
        cnt[0] = 1  # empty prefix
        mod = res = 0
        for x in nums:
            mod = (mod + x) % k  # Python % is already non-negative
            res += cnt[mod]
            cnt[mod] += 1
        return res
```

**C++**

```cpp
class Solution {
public:
    int subarraysDivByK(vector<int>& nums, int k) {
        vector<int> cnt(k, 0);
        cnt[0] = 1;  // empty prefix
        int mod = 0, res = 0;
        for (int x : nums) {
            mod = ((mod + x) % k + k) % k;  // normalize negative remainders
            res += cnt[mod];
            ++cnt[mod];
        }
        return res;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n) |
| **Space** | O(k) |

**Pitfalls:** C++ `%` can be negative for negative sums, so `-1` and `k - 1` would land in different buckets without the `+ k` fix; forgetting `cnt[0] = 1` misses subarrays that start at index 0.

---

## 22. Hashing & Array Classics

Template and pitfalls: [LeetCode Patterns §22 Hashing & Array Classics](../computer-science/LeetCode_Patterns.md#22-hashing--array-classics)

### LC 217 · Contains Duplicate · Easy

> **Problem:** Return `true` if any value appears at least twice in `nums`, otherwise `false`.

🔗 [https://leetcode.com/problems/contains-duplicate/](https://leetcode.com/problems/contains-duplicate/)

**Intuition:** Insert values into a hash set and stop at the first value already present: O(n) expected time. Alternatives: O(n^2) pairwise check, or sort in O(n log n) with O(1) extra space and compare neighbours.

**Python**

```python
class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        seen = set()
        for x in nums:
            if x in seen:
                return True
            seen.add(x)
        return False
```

**C++**

```cpp
class Solution {
public:
    bool containsDuplicate(vector<int>& nums) {
        unordered_set<int> seen;
        for (int x : nums)
            if (!seen.insert(x).second) return true;  // insert fails on repeat
        return false;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n) expected |
| **Space** | O(n) |

**Pitfalls:** `len(set(nums)) != len(nums)` is fine but cannot exit early; the sorting variant mutates the input.

---

### LC 242 · Valid Anagram · Easy

> **Problem:** Given strings `s` and `t` of lowercase English letters, return whether `t` is an anagram of `s` (same letters with the same multiplicities).

🔗 [https://leetcode.com/problems/valid-anagram/](https://leetcode.com/problems/valid-anagram/)

**Intuition:** Count letters with +1 for `s` and -1 for `t` in one 26-slot array; they are anagrams iff every slot ends at 0. O(n) versus O(n log n) for sorting both strings. Follow-up (Unicode input): use a hash map keyed by character instead of the fixed array.

**Python**

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        cnt = [0] * 26
        for a, b in zip(s, t):
            cnt[ord(a) - ord('a')] += 1
            cnt[ord(b) - ord('a')] -= 1
        return not any(cnt)
```

**C++**

```cpp
class Solution {
public:
    bool isAnagram(string s, string t) {
        if (s.size() != t.size()) return false;
        int cnt[26] = {};
        for (size_t i = 0; i < s.size(); ++i) {
            ++cnt[s[i] - 'a'];
            --cnt[t[i] - 'a'];
        }
        for (int c : cnt)
            if (c) return false;
        return true;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n) |
| **Space** | O(1) (26 counters) |

**Pitfalls:** Check lengths first (otherwise `zip` silently truncates); the fixed array breaks for Unicode -- switch to a map.

---

### LC 205 · Isomorphic Strings · Easy

> **Problem:** Given equal-length strings `s` and `t`, return whether characters of `s` can be replaced to get `t` under a one-to-one mapping (each character maps to exactly one character and no two characters map to the same one; a character may map to itself).

🔗 [https://leetcode.com/problems/isomorphic-strings/](https://leetcode.com/problems/isomorphic-strings/)

**Intuition:** The mapping must be a bijection, so checking only `s → t` misses cases like `"ab" → "aa"`. A compact way to check both directions: remember for each character the last position (1-based) where it was seen; at every index the two characters must have been last seen at the same position (both new, or both last seen together). One O(n) pass.

**Python**

```python
class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        ps, pt = {}, {}  # char -> last 1-based index where it appeared
        for i, (a, b) in enumerate(zip(s, t), 1):
            if ps.get(a, 0) != pt.get(b, 0):
                return False
            ps[a] = pt[b] = i
        return True
```

**C++**

```cpp
class Solution {
public:
    bool isIsomorphic(string s, string t) {
        int ps[256] = {}, pt[256] = {};  // char -> last 1-based index where it appeared
        for (int i = 0; i < (int)s.size(); ++i) {
            unsigned char a = s[i], b = t[i];
            if (ps[a] != pt[b]) return false;
            ps[a] = pt[b] = i + 1;
        }
        return true;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n) |
| **Space** | O(A), A = alphabet size (256 for ASCII) |

**Pitfalls:** A one-directional map accepts `"badc"/"baba"`; use 1-based positions so "never seen" (0) differs from index 0; index arrays with `unsigned char`.

---

### LC 271 · Encode and Decode Strings · Medium

> **Problem:** Design `Codec.encode(strs)` that turns a list of strings into one string, and `Codec.decode(s)` that recovers the original list exactly. Strings may contain any of the 256 ASCII characters, including any delimiter you might pick.

🔗 [https://leetcode.com/problems/encode-and-decode-strings/](https://leetcode.com/problems/encode-and-decode-strings/)

**Intuition:** A plain delimiter fails because it can appear inside a string. Length-prefix each string as `<len>#<payload>`: the decoder reads digits up to the first `'#'`, then takes exactly `len` characters, never inspecting the payload, so `'#'` or digits inside the data are harmless. Both directions are O(total length).

**Python**

```python
class Codec:
    def encode(self, strs: list[str]) -> str:
        return ''.join(f'{len(s)}#{s}' for s in strs)

    def decode(self, s: str) -> list[str]:
        res, i = [], 0
        while i < len(s):
            j = s.index('#', i)  # end of the length header
            n = int(s[i:j])
            res.append(s[j + 1:j + 1 + n])
            i = j + 1 + n
        return res
```

**C++**

```cpp
class Codec {
public:
    string encode(vector<string>& strs) {
        string out;
        for (auto& s : strs) out += to_string(s.size()) + '#' + s;
        return out;
    }

    vector<string> decode(string s) {
        vector<string> res;
        size_t i = 0;
        while (i < s.size()) {
            size_t j = s.find('#', i);  // end of the length header
            size_t n = stoul(s.substr(i, j - i));
            res.push_back(s.substr(j + 1, n));
            i = j + 1 + n;
        }
        return res;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(L), L = total characters across all strings |
| **Space** | O(L) |

**Pitfalls:** Must distinguish `[]` (encodes to `""`) from `[""]` (encodes to `"0#"`); search for `'#'` starting at `i`, not from the payload's end; splitting on a delimiter breaks when strings contain it.

---

### LC 36 · Valid Sudoku · Medium

> **Problem:** Given a partially filled 9×9 board (`'1'`-`'9'` or `'.'`), return whether the filled cells are valid: no digit repeats within any row, column, or 3×3 sub-box. The board need not be solvable.

🔗 [https://leetcode.com/problems/valid-sudoku/](https://leetcode.com/problems/valid-sudoku/)

**Intuition:** Single pass over the 81 cells, keeping a 9-bit "seen" mask per row, per column and per box. Cell `(r, c)` belongs to box `(r / 3) * 3 + c / 3`; a digit is invalid if its bit is already set in any of the three masks. Sets of digits work identically; bitmasks just avoid hashing.

**Python**

```python
class Solution:
    def isValidSudoku(self, board: list[list[str]]) -> bool:
        rows, cols, boxes = [0] * 9, [0] * 9, [0] * 9
        for r in range(9):
            for c in range(9):
                ch = board[r][c]
                if ch == '.':
                    continue
                bit = 1 << (ord(ch) - ord('1'))
                b = (r // 3) * 3 + c // 3
                if (rows[r] | cols[c] | boxes[b]) & bit:
                    return False
                rows[r] |= bit
                cols[c] |= bit
                boxes[b] |= bit
        return True
```

**C++**

```cpp
class Solution {
public:
    bool isValidSudoku(vector<vector<char>>& board) {
        int rows[9] = {}, cols[9] = {}, boxes[9] = {};
        for (int r = 0; r < 9; ++r)
            for (int c = 0; c < 9; ++c) {
                if (board[r][c] == '.') continue;
                int bit = 1 << (board[r][c] - '1');
                int b = (r / 3) * 3 + c / 3;
                if ((rows[r] | cols[c] | boxes[b]) & bit) return false;
                rows[r] |= bit;
                cols[c] |= bit;
                boxes[b] |= bit;
            }
        return true;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(81) = O(1) |
| **Space** | O(27) = O(1) |

**Pitfalls:** Wrong box index (`r / 3 + c / 3` collides boxes); skip `'.'` before computing the bit; do not try to solve the puzzle.

---

### LC 43 · Multiply Strings · Medium

> **Problem:** Given two non-negative integers as decimal strings `num1` and `num2` (up to 200 digits, no leading zeros except `"0"` itself), return their product as a string without converting the inputs to integers or using big-integer libraries.

🔗 [https://leetcode.com/problems/multiply-strings/](https://leetcode.com/problems/multiply-strings/)

**Intuition:** Grade-school multiplication: digit `num1[i]` times digit `num2[j]` contributes to result positions `i + j` (carry) and `i + j + 1` (ones) of an `m + n` digit buffer. Processing from the right, each position is normalized to a single digit by the time it is final. Strip leading zeros at the end, returning `"0"` if nothing remains.

**Python**

```python
class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        m, n = len(num1), len(num2)
        res = [0] * (m + n)
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                p = (ord(num1[i]) - 48) * (ord(num2[j]) - 48) + res[i + j + 1]
                res[i + j + 1] = p % 10
                res[i + j] += p // 10
        out = ''.join(map(str, res)).lstrip('0')
        return out or '0'
```

**C++**

```cpp
class Solution {
public:
    string multiply(string num1, string num2) {
        int m = num1.size(), n = num2.size();
        vector<int> res(m + n, 0);
        for (int i = m - 1; i >= 0; --i)
            for (int j = n - 1; j >= 0; --j) {
                int p = (num1[i] - '0') * (num2[j] - '0') + res[i + j + 1];
                res[i + j + 1] = p % 10;
                res[i + j] += p / 10;
            }
        string out;
        for (int d : res)
            if (!(out.empty() && d == 0)) out += char('0' + d);  // skip leading zeros
        return out.empty() ? "0" : out;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(m·n), m, n = digit counts |
| **Space** | O(m + n) |

**Pitfalls:** A zero operand yields all-zero digits -- return `"0"`, not `""`; carry goes to `i + j`, digit to `i + j + 1` (swapping them is the classic bug).

---

## 23. Matrix Manipulation

Template and pitfalls: [LeetCode Patterns §23 Matrix Manipulation](../computer-science/LeetCode_Patterns.md#23-matrix-manipulation)

### LC 867 · Transpose Matrix · Easy

> **Problem:** Given an `m × n` integer matrix, return its transpose (flip over the main diagonal, so entry `(i, j)` moves to `(j, i)`).

🔗 [https://leetcode.com/problems/transpose-matrix/](https://leetcode.com/problems/transpose-matrix/)

**Intuition:** Allocate an `n × m` result and copy `res[j][i] = matrix[i][j]`. In-place swapping only works for square matrices; a non-square transpose changes the shape, so a new matrix is required.

**Python**

```python
class Solution:
    def transpose(self, matrix: list[list[int]]) -> list[list[int]]:
        m, n = len(matrix), len(matrix[0])
        res = [[0] * m for _ in range(n)]
        for i in range(m):
            for j in range(n):
                res[j][i] = matrix[i][j]
        return res
```

**C++**

```cpp
class Solution {
public:
    vector<vector<int>> transpose(vector<vector<int>>& matrix) {
        int m = matrix.size(), n = matrix[0].size();
        vector<vector<int>> res(n, vector<int>(m));
        for (int i = 0; i < m; ++i)
            for (int j = 0; j < n; ++j) res[j][i] = matrix[i][j];
        return res;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(m·n), m×n matrix |
| **Space** | O(m·n) for the output |

**Pitfalls:** Result shape is `n × m`, not `m × n`; `[[0] * m] * n` aliases one row n times in Python. (One-liner: `[list(r) for r in zip(*matrix)]`.)

---

## 24. Stack-based Parsing

Template and pitfalls: [LeetCode Patterns §24 Stack-based Parsing](../computer-science/LeetCode_Patterns.md#24-stack-based-parsing)

### LC 1249 · Minimum Remove to Make Valid Parentheses · Medium

> **Problem:** Given a string `s` of `'('`, `')'` and lowercase letters, remove the minimum number of parentheses so the result is a valid parentheses string, and return any such result.

🔗 [https://leetcode.com/problems/minimum-remove-to-make-valid-parentheses/](https://leetcode.com/problems/minimum-remove-to-make-valid-parentheses/)

**Intuition:** Scan left to right with a stack of indices of unmatched `'('`. A `')'` with an empty stack can never be matched and must go; any `'('` still on the stack at the end has no partner and must go. Only those parentheses are removed, which is the minimum, in one O(n) pass. (O(1)-extra variant: drop bad `')'` left to right, then drop the last `open` excess `'('` scanning right to left.)

**Python**

```python
class Solution:
    def minRemoveToMakeValid(self, s: str) -> str:
        chars = list(s)
        stack = []  # indices of unmatched '('
        for i, c in enumerate(chars):
            if c == '(':
                stack.append(i)
            elif c == ')':
                if stack:
                    stack.pop()
                else:
                    chars[i] = ''  # unmatched ')'
        for i in stack:
            chars[i] = ''  # unmatched '('
        return ''.join(chars)
```

**C++**

```cpp
class Solution {
public:
    string minRemoveToMakeValid(string s) {
        vector<int> st;  // indices of unmatched '('
        for (int i = 0; i < (int)s.size(); ++i) {
            if (s[i] == '(') st.push_back(i);
            else if (s[i] == ')') {
                if (!st.empty()) st.pop_back();
                else s[i] = '*';  // unmatched ')'
            }
        }
        for (int i : st) s[i] = '*';  // unmatched '('
        s.erase(remove(s.begin(), s.end(), '*'), s.end());
        return s;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n) |
| **Space** | O(n) |

**Pitfalls:** Leftover `'('` must be removed too, not just stray `')'`; deleting characters one by one from a string in the loop is O(n^2) -- mark then compact; an all-invalid input like `"))(("` returns `""`.

---

### LC 1209 · Remove All Adjacent Duplicates in String II · Medium

> **Problem:** Repeatedly remove any `k` adjacent equal characters from `s` (the remaining parts join together) until no such group exists, and return the final string, which is unique.

🔗 [https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string-ii/](https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string-ii/)

**Intuition:** Keep a stack of `(char, run length)`. Each new character either extends the top run or pushes a new run; when a run reaches `k` it is popped, which automatically lets the runs on either side merge on the next push. Every character is pushed and popped at most once, so O(n) instead of O(n^2 / k) for repeated rescans.

**Python**

```python
class Solution:
    def removeDuplicates(self, s: str, k: int) -> str:
        stack = []  # [char, run length]
        for c in s:
            if stack and stack[-1][0] == c:
                stack[-1][1] += 1
                if stack[-1][1] == k:
                    stack.pop()
            else:
                stack.append([c, 1])
        return ''.join(c * n for c, n in stack)
```

**C++**

```cpp
class Solution {
public:
    string removeDuplicates(string s, int k) {
        vector<pair<char, int>> st;  // (char, run length)
        for (char c : s) {
            if (!st.empty() && st.back().first == c) {
                if (++st.back().second == k) st.pop_back();
            } else {
                st.push_back({c, 1});
            }
        }
        string out;
        for (auto& [c, n] : st) out.append(n, c);
        return out;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n) |
| **Space** | O(n) |

**Pitfalls:** Storing single characters and re-counting the top run each time is O(n·k); after a pop the newly exposed run must be able to keep growing (the stack handles this naturally).

---

## 26. Design Problems

Template and pitfalls: [LeetCode Patterns §26 Design Problems](../computer-science/LeetCode_Patterns.md#26-design-problems)

### LC 232 · Implement Queue using Stacks · Easy

> **Problem:** Implement a FIFO queue `MyQueue` with `push`, `pop`, `peek` and `empty` using only stack operations (push to top, peek/pop from top, size, is empty). All `pop`/`peek` calls are valid.

🔗 [https://leetcode.com/problems/implement-queue-using-stacks/](https://leetcode.com/problems/implement-queue-using-stacks/)

**Intuition:** Push onto an `in` stack; serve `pop`/`peek` from an `out` stack. Only when `out` is empty, pour all of `in` into it, which reverses the order so the oldest element is on top. Each element moves from `in` to `out` at most once, so every operation is amortized O(1) (the follow-up).

**Python**

```python
class MyQueue:
    def __init__(self):
        self.inbox, self.outbox = [], []

    def push(self, x: int) -> None:
        self.inbox.append(x)

    def pop(self) -> int:
        self.peek()
        return self.outbox.pop()

    def peek(self) -> int:
        if not self.outbox:  # refill only when empty to keep FIFO order
            while self.inbox:
                self.outbox.append(self.inbox.pop())
        return self.outbox[-1]

    def empty(self) -> bool:
        return not self.inbox and not self.outbox
```

**C++**

```cpp
class MyQueue {
    stack<int> in, out;

public:
    MyQueue() {}

    void push(int x) { in.push(x); }

    int pop() {
        int x = peek();
        out.pop();
        return x;
    }

    int peek() {
        if (out.empty())  // refill only when empty to keep FIFO order
            while (!in.empty()) { out.push(in.top()); in.pop(); }
        return out.top();
    }

    bool empty() { return in.empty() && out.empty(); }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(1) amortized per operation (O(n) worst case for a single refill) |
| **Space** | O(n) |

**Pitfalls:** Pouring `in` into `out` while `out` is non-empty breaks FIFO order; `empty()` must check both stacks.

---

### LC 622 · Design Circular Queue · Medium

> **Problem:** Implement `MyCircularQueue(k)`, a fixed-capacity FIFO ring buffer with `enQueue(value)` / `deQueue()` (return success as bool), `Front()` / `Rear()` (return -1 when empty), `isEmpty()` and `isFull()`.

🔗 [https://leetcode.com/problems/design-circular-queue/](https://leetcode.com/problems/design-circular-queue/)

**Intuition:** Store a fixed array, the `head` index and the element `count`. The tail slot is `(head + count) % k` and the rear element is at `(head + count - 1) % k`. Tracking `count` explicitly avoids the classic "head == tail means empty or full?" ambiguity without wasting a slot. All operations O(1).

**Python**

```python
class MyCircularQueue:
    def __init__(self, k: int):
        self.q = [0] * k
        self.head = 0
        self.count = 0

    def enQueue(self, value: int) -> bool:
        if self.isFull():
            return False
        self.q[(self.head + self.count) % len(self.q)] = value
        self.count += 1
        return True

    def deQueue(self) -> bool:
        if self.isEmpty():
            return False
        self.head = (self.head + 1) % len(self.q)
        self.count -= 1
        return True

    def Front(self) -> int:
        return -1 if self.isEmpty() else self.q[self.head]

    def Rear(self) -> int:
        return -1 if self.isEmpty() else self.q[(self.head + self.count - 1) % len(self.q)]

    def isEmpty(self) -> bool:
        return self.count == 0

    def isFull(self) -> bool:
        return self.count == len(self.q)
```

**C++**

```cpp
class MyCircularQueue {
    vector<int> q;
    int head = 0, count = 0;

public:
    MyCircularQueue(int k) : q(k) {}

    bool enQueue(int value) {
        if (isFull()) return false;
        q[(head + count) % q.size()] = value;
        ++count;
        return true;
    }

    bool deQueue() {
        if (isEmpty()) return false;
        head = (head + 1) % q.size();
        --count;
        return true;
    }

    int Front() { return isEmpty() ? -1 : q[head]; }

    int Rear() { return isEmpty() ? -1 : q[(head + count - 1) % q.size()]; }

    bool isEmpty() { return count == 0; }

    bool isFull() { return count == (int)q.size(); }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(1) per operation |
| **Space** | O(k) |

**Pitfalls:** Rear index must wrap (`(head + count - 1) % k`, never `tail - 1` going negative); `Front`/`Rear` on empty return -1; `deQueue` only moves `head`, no need to clear the slot.

---

### LC 1396 · Design Underground System · Medium

> **Problem:** Implement `UndergroundSystem` with `checkIn(id, stationName, t)`, `checkOut(id, stationName, t)` and `getAverageTime(startStation, endStation)`, which returns the average travel time over all completed trips that went directly from `startStation` to `endStation`. Calls are consistent (a customer is checked in at most once at a time, and `t` increases).

🔗 [https://leetcode.com/problems/design-underground-system/](https://leetcode.com/problems/design-underground-system/)

**Intuition:** Two hash maps: `id → (start station, check-in time)` for trips in progress, and `(start, end) → (total time, trip count)` for completed trips. Check-out moves the trip from the first map into the running totals, so the average is a single O(1) division instead of rescanning stored trips.

**Python**

```python
class UndergroundSystem:
    def __init__(self):
        self.active = {}  # id -> (start station, check-in time)
        self.totals = {}  # (start, end) -> [total time, trip count]

    def checkIn(self, id: int, stationName: str, t: int) -> None:
        self.active[id] = (stationName, t)

    def checkOut(self, id: int, stationName: str, t: int) -> None:
        start, t0 = self.active.pop(id)
        rec = self.totals.setdefault((start, stationName), [0, 0])
        rec[0] += t - t0
        rec[1] += 1

    def getAverageTime(self, startStation: str, endStation: str) -> float:
        total, count = self.totals[(startStation, endStation)]
        return total / count
```

**C++**

```cpp
class UndergroundSystem {
    unordered_map<int, pair<string, int>> active;        // id -> (start, check-in time)
    unordered_map<string, pair<long long, int>> totals;  // "start,end" -> (total, count)

public:
    UndergroundSystem() {}

    void checkIn(int id, string stationName, int t) {
        active[id] = {stationName, t};
    }

    void checkOut(int id, string stationName, int t) {
        auto [start, t0] = active[id];
        active.erase(id);
        auto& rec = totals[start + "," + stationName];  // names are alphanumeric, so ',' is safe
        rec.first += t - t0;
        ++rec.second;
    }

    double getAverageTime(string startStation, string endStation) {
        auto& rec = totals[startStation + "," + endStation];
        return (double)rec.first / rec.second;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(1) per call (plus O(L) hashing of station names of length L) |
| **Space** | O(P + S^2), P = customers in transit, S = stations |

**Pitfalls:** Trips are directional (`A→B` differs from `B→A`); integer division in C++ -- cast before dividing; keying by plain concatenation without a separator lets `"ab"+"c"` collide with `"a"+"bc"`.

---

### LC 895 · Maximum Frequency Stack · Hard

> **Problem:** Implement `FreqStack` with `push(val)` and `pop()`, where `pop` removes and returns the most frequent element, breaking ties by returning the one closest to the top (most recently pushed). `pop` is only called on a non-empty stack.

🔗 [https://leetcode.com/problems/maximum-frequency-stack/](https://leetcode.com/problems/maximum-frequency-stack/)

**Intuition:** Keep `freq[val]` and one stack per frequency level: when `val` reaches frequency `f`, push it onto `group[f]` (it stays in all lower groups too). The answer to `pop` is always the top of `group[maxFreq]`, which is the most recent element at the highest frequency. After popping, decrement its frequency and drop `maxFreq` when that group empties -- the copy at `f - 1` is already in place, so both operations are O(1) with no heap.

**Python**

```python
from collections import defaultdict


class FreqStack:
    def __init__(self):
        self.freq = defaultdict(int)
        self.group = defaultdict(list)  # f -> stack of values that reached frequency f
        self.max_freq = 0

    def push(self, val: int) -> None:
        self.freq[val] += 1
        f = self.freq[val]
        self.max_freq = max(self.max_freq, f)
        self.group[f].append(val)

    def pop(self) -> int:
        val = self.group[self.max_freq].pop()
        self.freq[val] -= 1
        if not self.group[self.max_freq]:
            self.max_freq -= 1
        return val
```

**C++**

```cpp
class FreqStack {
    unordered_map<int, int> freq;
    unordered_map<int, vector<int>> group;  // f -> stack of values that reached frequency f
    int maxFreq = 0;

public:
    FreqStack() {}

    void push(int val) {
        int f = ++freq[val];
        maxFreq = max(maxFreq, f);
        group[f].push_back(val);
    }

    int pop() {
        int val = group[maxFreq].back();
        group[maxFreq].pop_back();
        --freq[val];
        if (group[maxFreq].empty()) --maxFreq;
        return val;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(1) per operation |
| **Space** | O(n), n = number of pushes |

**Pitfalls:** A heap keyed by (freq, push time) works but is O(log n); do not remove `val` from lower-frequency groups on push -- those copies are what make pops after a frequency drop correct.
