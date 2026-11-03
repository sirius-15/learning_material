# LeetCode Patterns -- Comprehensive Guide

> A pattern-based approach to mastering coding interviews. Each pattern includes template code in **Python** and **C++**, variations, common mistakes, related patterns, and graded example problems with full solutions.

---

## Table of Contents

1. [Two Pointers](#1-two-pointers)
2. [Sliding Window](#2-sliding-window)
3. [Fast and Slow Pointers](#3-fast-and-slow-pointers)
4. [Merge Intervals](#4-merge-intervals)
5. [Cyclic Sort](#5-cyclic-sort)
6. [In-place Linked List Reversal](#6-in-place-linked-list-reversal)
7. [BFS (Breadth-First Search)](#7-bfs-breadth-first-search)
8. [DFS (Depth-First Search)](#8-dfs-depth-first-search)
9. [Two Heaps](#9-two-heaps)
10. [Subsets / Backtracking](#10-subsets--backtracking)
11. [Modified Binary Search](#11-modified-binary-search)
12. [Top K Elements](#12-top-k-elements)
13. [K-way Merge](#13-k-way-merge)
14. [Topological Sort](#14-topological-sort)
15. [Monotonic Stack / Queue](#15-monotonic-stack--queue)
16. [Union Find (Disjoint Set)](#16-union-find-disjoint-set)
17. [Trie (Prefix Tree)](#17-trie-prefix-tree)
18. [Dynamic Programming](#18-dynamic-programming)
19. [Greedy](#19-greedy)
20. [Bit Manipulation](#20-bit-manipulation)
21. [Prefix Sum & Difference Array](#21-prefix-sum--difference-array)
22. [Hashing & Array Classics](#22-hashing--array-classics)
23. [Matrix Manipulation](#23-matrix-manipulation)
24. [Stack-based Parsing](#24-stack-based-parsing)
25. [Line Sweep & Advanced Intervals](#25-line-sweep--advanced-intervals)
26. [Design Problems](#26-design-problems)
27. [Weighted Shortest Path Patterns](#27-weighted-shortest-path-patterns)
28. [Binary Search on the Answer](#28-binary-search-on-the-answer)
29. [Ordered Containers](#29-ordered-containers)
30. [String Hashing & Matching in Practice](#30-string-hashing--matching-in-practice)
31. [Randomized Algorithms](#31-randomized-algorithms)
32. [Math & Number Theory](#32-math--number-theory)
33. [Meet-in-the-Middle & Bidirectional BFS](#33-meet-in-the-middle--bidirectional-bfs)
34. [Pattern Selection Flowchart](#pattern-selection-flowchart)
35. [Quick Reference Cheat Sheet](#quick-reference-cheat-sheet)

---

## How to Use This Guide

> **Companion material.** For a checklist of what to practise (150 problems by pattern, timed protocol, spaced repetition, unsolved sets), use [Coding Problem List](../practice/Coding_Problem_List.md). For how to *perform* in the round (clarify, brute force first, optimise, dry-run, test out loud, time management), use [The Coding-Round Communication Framework](../career/Interview_Loops_and_Logistics.md#7-the-coding-round-communication-framework). Algorithm theory and proofs live in [DSA Fundamentals](DSA_Fundamentals.md).

Most LeetCode problems map to one or more recurring **patterns**. Instead of memorising hundreds of individual solutions, learn the 33 patterns in this guide and you will be able to recognise and solve the vast majority of interview problems.

**For each pattern you will find:**

| Section | What it contains |
|---|---|
| **Overview** | Core idea in plain language |
| **When to Use** | Signals in the problem statement that hint at this pattern |
| **Template Code** | Copy-paste-ready skeleton (Python + C++) |
| **Variations** | Sub-patterns or alternate forms |
| **Common Mistakes** | Pitfalls and how to avoid them |
| **Related Patterns** | Cross-references to complementary patterns |
| **Example Problems** | 4-13 problems graded Easy → Hard, each with intuition, full solution, and complexity analysis |
| **Interview Q&A** | Follow-up questions interviewers ask, with model answers |

**Recommended workflow:**

1. Read the pattern overview and template.
2. Solve the Easy example on your own first.
3. Compare with the provided solution.
4. Progress to Medium and Hard examples.
5. Revisit the "Common Mistakes" section after each attempt.

---

## 1. Two Pointers

### Overview

The Two Pointers technique uses two pointers that move through the data structure (usually an array or linked list) in a coordinated way -- either towards each other (**converging**), away from each other (**diverging**), or in the same direction at different speeds. By restricting how the pointers advance, we eliminate the need to examine every pair of elements, turning O(n²) brute-force approaches into O(n) solutions.

### When to Use

- Sorted array/list and you need to find pairs/triplets that satisfy a condition
- Need to compare elements from both ends (palindrome checks, container problems)
- Need to remove duplicates in-place from sorted data
- Partitioning arrays (e.g., Dutch National Flag)
- Merging two sorted arrays

### Template Code

#### 1. Converging Pointers (opposite ends → center)

**Python**

```python
def two_pointer_converge(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        current = arr[left] + arr[right]
        if current == target:
            return [left, right]
        elif current < target:
            left += 1
        else:
            right -= 1
    return []
```

**C++**

```cpp
vector<int> twoPointerConverge(vector<int>& arr, int target) {
    int left = 0, right = (int)arr.size() - 1;
    while (left < right) {
        int current = arr[left] + arr[right];
        if (current == target)
            return {left, right};
        else if (current < target)
            ++left;
        else
            --right;
    }
    return {};
}
```

#### 2. Same-Direction Pointers (slow / fast both start at 0)

**Python**

```python
def two_pointer_same_direction(arr):
    write = 0
    for read in range(len(arr)):
        if arr[read] != 0:          # example condition
            arr[write] = arr[read]
            write += 1
    # fill remaining positions if needed
    while write < len(arr):
        arr[write] = 0
        write += 1
    return arr
```

**C++**

```cpp
void twoPointerSameDirection(vector<int>& arr) {
    int write = 0;
    for (int read = 0; read < (int)arr.size(); ++read) {
        if (arr[read] != 0) {       // example condition
            arr[write++] = arr[read];
        }
    }
    while (write < (int)arr.size())
        arr[write++] = 0;
}
```

### Variations

| Variation | Description |
|---|---|
| **Converging (opposite ends)** | Start at both ends and move inward. Used for pair-sum in sorted arrays, palindromes, container problems. |
| **Same-direction (read/write)** | Both pointers move left to right. The *read* pointer scans every element; the *write* pointer only advances when a "keep" condition is met. Used for in-place removal / deduplication. |
| **Three pointers** | Fix one pointer with an outer loop; use a converging pair inside. Used for triplet problems (3Sum) and Dutch National Flag partitioning. |

### Common Mistakes

- **Forgetting to handle duplicates** -- causes TLE or wrong answers on triplet problems. After finding a valid result, skip over duplicate values before continuing.
- **Off-by-one errors with while conditions** -- `< ` vs `<=`. Use `left < right` for pair searches (you need two distinct elements) and `left <= right` when a single-element check is valid.
- **Not sorting the array first** when the algorithm requires sorted input. Two-pointer convergence only works on sorted data.
- **Modifying the array while iterating** without adjusting pointers -- can skip elements or process the same element twice.

### Related Patterns

- **Sliding Window** -- also uses two pointers, but both move in the same direction to maintain a contiguous window.
- **Fast & Slow Pointers** -- a special case where pointers move at different *speeds* (commonly used for cycle detection in linked lists).
- **Binary Search** -- another technique that leverages sorted input; sometimes combined with two pointers.

### Example Problems

---

#### Problem 1 · Easy -- Two Sum II (LeetCode 167)

> **Problem:** Given a **1-indexed** sorted array `numbers` and an integer `target`, find two numbers that add up to `target`. Return their indices `[index1, index2]` (1-indexed). Exactly one solution is guaranteed.

🔗 [https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)

**Intuition:** Because the array is sorted, place one pointer at the start and one at the end. If the sum is too small, move the left pointer right to increase it; if too large, move the right pointer left to decrease it. Each step eliminates at least one candidate, giving O(n) time.

**Python**

```python
class Solution:
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        left, right = 0, len(numbers) - 1
        while left < right:
            s = numbers[left] + numbers[right]
            if s == target:
                return [left + 1, right + 1]
            elif s < target:
                left += 1
            else:
                right -= 1
        return []  # guaranteed to have a solution
```

**C++**

```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& numbers, int target) {
        int left = 0, right = (int)numbers.size() - 1;
        while (left < right) {
            int s = numbers[left] + numbers[right];
            if (s == target)
                return {left + 1, right + 1};
            else if (s < target)
                ++left;
            else
                --right;
        }
        return {};
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n) |
| **Space** | O(1) |

---

#### Problem 2 · Easy -- Valid Palindrome (LeetCode 125)

> **Problem:** Given a string `s`, determine if it is a palindrome considering only alphanumeric characters and ignoring case.

🔗 [https://leetcode.com/problems/valid-palindrome/](https://leetcode.com/problems/valid-palindrome/)

**Intuition:** Use converging pointers from both ends. Skip any character that is not alphanumeric. Compare the lowercased characters at each pointer; if they ever differ, the string is not a palindrome. This avoids creating a filtered copy of the string, keeping space at O(1).

**Python**

```python
class Solution:
    def isPalindrome(self, s: str) -> bool:
        left, right = 0, len(s) - 1
        while left < right:
            while left < right and not s[left].isalnum():
                left += 1
            while left < right and not s[right].isalnum():
                right -= 1
            if s[left].lower() != s[right].lower():
                return False
            left += 1
            right -= 1
        return True
```

**C++**

```cpp
class Solution {
public:
    bool isPalindrome(string s) {
        int left = 0, right = (int)s.size() - 1;
        while (left < right) {
            while (left < right && !isalnum(s[left]))
                ++left;
            while (left < right && !isalnum(s[right]))
                --right;
            if (tolower(s[left]) != tolower(s[right]))
                return false;
            ++left;
            --right;
        }
        return true;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n) |
| **Space** | O(1) |

---

#### Problem 3 · Medium -- 3Sum (LeetCode 15)

> **Problem:** Given an integer array `nums`, return all unique triplets `[nums[i], nums[j], nums[k]]` such that `i != j != k` and `nums[i] + nums[j] + nums[k] == 0`. The solution set must not contain duplicate triplets.

🔗 [https://leetcode.com/problems/3sum/](https://leetcode.com/problems/3sum/)

**Intuition:** Sort the array first. For each element `nums[i]`, use two converging pointers on the subarray to the right to find pairs that sum to `-nums[i]`. After finding a valid triplet, skip duplicate values for all three positions to avoid repeated results. The outer loop is O(n) and the inner two-pointer scan is O(n), giving O(n²) overall.

**Python**

```python
class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        result = []
        for i in range(len(nums) - 2):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            left, right = i + 1, len(nums) - 1
            while left < right:
                total = nums[i] + nums[left] + nums[right]
                if total < 0:
                    left += 1
                elif total > 0:
                    right -= 1
                else:
                    result.append([nums[i], nums[left], nums[right]])
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1
        return result
```

**C++**

```cpp
class Solution {
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        vector<vector<int>> result;
        for (int i = 0; i < (int)nums.size() - 2; ++i) {
            if (i > 0 && nums[i] == nums[i - 1])
                continue;
            int left = i + 1, right = (int)nums.size() - 1;
            while (left < right) {
                int total = nums[i] + nums[left] + nums[right];
                if (total < 0) {
                    ++left;
                } else if (total > 0) {
                    --right;
                } else {
                    result.push_back({nums[i], nums[left], nums[right]});
                    while (left < right && nums[left] == nums[left + 1])
                        ++left;
                    while (left < right && nums[right] == nums[right - 1])
                        --right;
                    ++left;
                    --right;
                }
            }
        }
        return result;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n²) |
| **Space** | O(1) ignoring output storage |

---

#### Problem 4 · Medium -- Container With Most Water (LeetCode 11)

> **Problem:** Given `n` non-negative integers `height[0..n-1]` where each represents a vertical line at position `i`, find two lines that together with the x-axis form a container that holds the most water.

🔗 [https://leetcode.com/problems/container-with-most-water/](https://leetcode.com/problems/container-with-most-water/)

**Intuition:** Start with the widest container (pointers at both ends). The area is limited by the shorter line, so moving the taller line inward can never increase the area (width shrinks and height can't improve). Always move the pointer pointing to the shorter line. This greedy choice guarantees we never skip the optimal pair.

**Python**

```python
class Solution:
    def maxArea(self, height: list[int]) -> int:
        left, right = 0, len(height) - 1
        max_area = 0
        while left < right:
            w = right - left
            h = min(height[left], height[right])
            max_area = max(max_area, w * h)
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        return max_area
```

**C++**

```cpp
class Solution {
public:
    int maxArea(vector<int>& height) {
        int left = 0, right = (int)height.size() - 1;
        int maxArea = 0;
        while (left < right) {
            int w = right - left;
            int h = min(height[left], height[right]);
            maxArea = max(maxArea, w * h);
            if (height[left] < height[right])
                ++left;
            else
                --right;
        }
        return maxArea;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n) |
| **Space** | O(1) |

---

#### Problem 5 · Hard -- Trapping Rain Water (LeetCode 42)

> **Problem:** Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

🔗 [https://leetcode.com/problems/trapping-rain-water/](https://leetcode.com/problems/trapping-rain-water/)

**Intuition:** Water above position `i` equals `min(leftMax, rightMax) - height[i]`. Instead of precomputing both max arrays, maintain `leftMax` and `rightMax` with two pointers. Process whichever side has the smaller max: if `leftMax < rightMax`, the water at `left` is determined solely by `leftMax` (anything on the right is at least as tall), so we add `leftMax - height[left]` and advance `left`. Symmetrically for the right side. This gives a single-pass O(n) solution with O(1) space.

**Python**

```python
class Solution:
    def trap(self, height: list[int]) -> int:
        if not height:
            return 0
        left, right = 0, len(height) - 1
        left_max, right_max = height[left], height[right]
        water = 0
        while left < right:
            if left_max < right_max:
                left += 1
                left_max = max(left_max, height[left])
                water += left_max - height[left]
            else:
                right -= 1
                right_max = max(right_max, height[right])
                water += right_max - height[right]
        return water
```

**C++**

```cpp
class Solution {
public:
    int trap(vector<int>& height) {
        if (height.empty()) return 0;
        int left = 0, right = (int)height.size() - 1;
        int leftMax = height[left], rightMax = height[right];
        int water = 0;
        while (left < right) {
            if (leftMax < rightMax) {
                ++left;
                leftMax = max(leftMax, height[left]);
                water += leftMax - height[left];
            } else {
                --right;
                rightMax = max(rightMax, height[right]);
                water += rightMax - height[right];
            }
        }
        return water;
    }
};
```

| Complexity | Value |
|---|---|
| **Time** | O(n) |
| **Space** | O(1) |

---

## 2. Sliding Window

### Overview

The Sliding Window pattern maintains a "window" — a contiguous subarray or substring — that expands or contracts as it slides over the data. Instead of recalculating results from scratch for every possible subarray, it reuses computation from the previous window position. This reduces brute-force nested loops from O(n²) or O(n·k) down to O(n) by adding the new element entering the window and removing the element leaving it.

### When to Use

- Finding the longest or shortest subarray/substring satisfying a condition
- Finding a subarray with a given sum or product
- String problems involving character frequency constraints
- Fixed-size window aggregation (e.g., max sum of subarray of size k)
- Problems mentioning "contiguous subarray" or "contiguous substring"

### Template Code

#### Fixed-Size Window (Python)

```python
def fixed_window(nums, k):
    n = len(nums)
    window_sum = sum(nums[:k])
    best = window_sum

    for right in range(k, n):
        window_sum += nums[right] - nums[right - k]
        best = max(best, window_sum)

    return best
```

#### Fixed-Size Window (C++)

```cpp
int fixedWindow(vector<int>& nums, int k) {
    int n = nums.size();
    int windowSum = 0;
    for (int i = 0; i < k; i++)
        windowSum += nums[i];

    int best = windowSum;
    for (int right = k; right < n; right++) {
        windowSum += nums[right] - nums[right - k];
        best = max(best, windowSum);
    }
    return best;
}
```

#### Variable-Size (Dynamic) Window (Python)

```python
def variable_window(nums):
    left = 0
    window_state = ...  # e.g., current sum, hashmap, etc.
    best = ...

    for right in range(len(nums)):
        # Expand: add nums[right] to window state
        ...

        # Shrink: while window violates the constraint
        while condition_violated(window_state):
            # Remove nums[left] from window state
            ...
            left += 1

        # Update answer with current valid window
        best = optimize(best, right - left + 1)

    return best
```

#### Variable-Size (Dynamic) Window (C++)

```cpp
int variableWindow(vector<int>& nums) {
    int left = 0;
    int best = ...;
    // window_state: e.g., current sum, unordered_map, etc.

    for (int right = 0; right < (int)nums.size(); right++) {
        // Expand: add nums[right] to window state

        // Shrink: while window violates the constraint
        while (conditionViolated(windowState)) {
            // Remove nums[left] from window state
            left++;
        }

        // Update answer with current valid window
        best = optimize(best, right - left + 1);
    }
    return best;
}
```

### Variations

| Variation | Description |
|---|---|
| **Fixed-size window** | Window length is constant (k). Slide by adding right and removing left. |
| **Dynamic / variable-size window** | Window grows by advancing `right`; shrinks by advancing `left` when a constraint is violated. |
| **Window with hashmap** | Track character or element frequencies inside the window using a hashmap/counter. |
| **Window with deque** | Use a monotonic deque to efficiently track the min or max within the current window. |
| **At most K "bad" things** | Shrink while the window has more than K distinct values / replacements / zeros. Fruit Into Baskets (LC 904), Max Consecutive Ones III (LC 1004), Longest Repeating Character Replacement (LC 424). |
| **Exactly K** | Count with `atMost(K) - atMost(K - 1)`: windows with exactly K are those with at most K minus those with at most K - 1. Subarrays with K Different Integers (LC 992), Binary Subarrays With Sum (LC 930), Count Number of Nice Subarrays (LC 1248). |
| **Non-shrinking window** | When only the maximum length matters, slide the window (move `left` by one) instead of shrinking it, so its size never decreases. LC 424. |
| **Prefix sums + monotonic deque** | Negative values break the shrink rule; keep an increasing deque of prefix-sum indices instead. Shortest Subarray with Sum at Least K (LC 862). |

### Common Mistakes

- **Not correctly shrinking the window** — forgetting to advance `left` or using a wrong shrink condition leads to infinite loops or wrong answers.
- **Off-by-one when calculating window size** — the size of a window from index `left` to `right` inclusive is `right - left + 1`, not `right - left`.
- **Forgetting to update state when shrinking** — when `left` advances, the hashmap/counter/sum must be updated to remove the element at the old `left`.
- **Confusing expand vs. shrink conditions** — expanding happens unconditionally each iteration; shrinking happens only while a constraint is violated (use `while`, not `if`).

### Related Patterns

- **Two Pointers** — Sliding Window is a specialized form of two pointers where both move in the same direction.
- **Monotonic Queue** — Used inside a sliding window to track min/max efficiently.
- **Hashing** — Hashmaps are frequently used inside the window to count frequencies.
- **Prefix Sum** ([Pattern 21](#21-prefix-sum--difference-array)) — replaces the window when values can be negative (sum equals K), or pairs with a deque (Problem 9).
- **Ordered Containers** ([Pattern 29](#29-ordered-containers)) — when the window needs a median, a nearest value, or both min and max with deletions.

---

### Example Problems

#### Problem 1: Maximum Average Subarray I (LeetCode 643) — Easy

**Link:** https://leetcode.com/problems/maximum-average-subarray-i/

**Problem:** Given an integer array `nums` and an integer `k`, find the contiguous subarray of length `k` that has the maximum average value. Return the maximum average.

**Intuition:** This is a textbook fixed-size sliding window. Compute the sum of the first `k` elements, then slide the window one step at a time — add the incoming element and subtract the outgoing element. Track the maximum sum seen, then divide by `k`.

**Python:**

```python
class Solution:
    def findMaxAverage(self, nums: list[int], k: int) -> float:
        window_sum = sum(nums[:k])
        max_sum = window_sum

        for right in range(k, len(nums)):
            window_sum += nums[right] - nums[right - k]
            max_sum = max(max_sum, window_sum)

        return max_sum / k
```

**C++:**

```cpp
class Solution {
public:
    double findMaxAverage(vector<int>& nums, int k) {
        int windowSum = 0;
        for (int i = 0; i < k; i++)
            windowSum += nums[i];

        int maxSum = windowSum;
        for (int right = k; right < (int)nums.size(); right++) {
            windowSum += nums[right] - nums[right - k];
            maxSum = max(maxSum, windowSum);
        }
        return (double)maxSum / k;
    }
};
```

**Complexity:** Time O(n), Space O(1).

---

#### Problem 2: Longest Substring Without Repeating Characters (LeetCode 3) — Medium

**Link:** https://leetcode.com/problems/longest-substring-without-repeating-characters/

**Problem:** Given a string `s`, find the length of the longest substring without repeating characters.

**Intuition:** Use a dynamic sliding window with a hashset (or hashmap storing the last index of each character). Expand `right` one character at a time. If `s[right]` is already in the window, shrink from the left until the duplicate is removed. The answer is the maximum value of `right - left + 1` across all valid windows.

**Python:**

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        char_set = set()
        left = 0
        max_len = 0

        for right in range(len(s)):
            while s[right] in char_set:
                char_set.remove(s[left])
                left += 1
            char_set.add(s[right])
            max_len = max(max_len, right - left + 1)

        return max_len
```

**C++:**

```cpp
class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        unordered_set<char> charSet;
        int left = 0, maxLen = 0;

        for (int right = 0; right < (int)s.size(); right++) {
            while (charSet.count(s[right])) {
                charSet.erase(s[left]);
                left++;
            }
            charSet.insert(s[right]);
            maxLen = max(maxLen, right - left + 1);
        }
        return maxLen;
    }
};
```

**Complexity:** Time O(n), Space O(min(n, m)) where m is the character set size.

---

#### Problem 3: Minimum Size Subarray Sum (LeetCode 209) — Medium

**Link:** https://leetcode.com/problems/minimum-size-subarray-sum/

**Problem:** Given an array of positive integers `nums` and a positive integer `target`, return the minimal length of a contiguous subarray whose sum is greater than or equal to `target`. If no such subarray exists, return `0`.

**Intuition:** Because all values are positive, use a dynamic sliding window. Expand `right` to grow the sum. Whenever `window_sum >= target`, the window is valid — record its length and shrink from the left to try to find a shorter valid window. The monotonicity of prefix sums guarantees correctness.

**Python:**

```python
class Solution:
    def minSubArrayLen(self, target: int, nums: list[int]) -> int:
        left = 0
        window_sum = 0
        min_len = float('inf')

        for right in range(len(nums)):
            window_sum += nums[right]

            while window_sum >= target:
                min_len = min(min_len, right - left + 1)
                window_sum -= nums[left]
                left += 1

        return min_len if min_len != float('inf') else 0
```

**C++:**

```cpp
class Solution {
public:
    int minSubArrayLen(int target, vector<int>& nums) {
        int left = 0, windowSum = 0;
        int minLen = INT_MAX;

        for (int right = 0; right < (int)nums.size(); right++) {
            windowSum += nums[right];

            while (windowSum >= target) {
                minLen = min(minLen, right - left + 1);
                windowSum -= nums[left];
                left++;
            }
        }
        return minLen == INT_MAX ? 0 : minLen;
    }
};
```

**Complexity:** Time O(n), Space O(1).

---

#### Problem 4: Permutation in String (LeetCode 567) — Medium

**Link:** https://leetcode.com/problems/permutation-in-string/

**Problem:** Given two strings `s1` and `s2`, return `true` if `s2` contains a permutation of `s1` (i.e., one of `s1`'s permutations is a substring of `s2`).

**Intuition:** A permutation of `s1` has the same character frequencies and the same length. Slide a fixed-size window of length `len(s1)` over `s2`. Maintain a frequency count for the window and compare it against `s1`'s frequency count. To avoid comparing full maps each step, track how many characters have matching counts (`matches`) and update it incrementally.

**Python:**

```python
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2):
            return False

        s1_count = [0] * 26
        window_count = [0] * 26

        for c in s1:
            s1_count[ord(c) - ord('a')] += 1
        for i in range(len(s1)):
            window_count[ord(s2[i]) - ord('a')] += 1

        matches = sum(1 for i in range(26) if s1_count[i] == window_count[i])

        for right in range(len(s1), len(s2)):
            if matches == 26:
                return True

            idx = ord(s2[right]) - ord('a')
            window_count[idx] += 1
            if window_count[idx] == s1_count[idx]:
                matches += 1
            elif window_count[idx] == s1_count[idx] + 1:
                matches -= 1

            idx = ord(s2[right - len(s1)]) - ord('a')
            window_count[idx] -= 1
            if window_count[idx] == s1_count[idx]:
                matches += 1
            elif window_count[idx] == s1_count[idx] - 1:
                matches -= 1

        return matches == 26
```

**C++:**

```cpp
class Solution {
public:
    bool checkInclusion(string s1, string s2) {
        int n1 = s1.size(), n2 = s2.size();
        if (n1 > n2) return false;

        vector<int> s1Count(26, 0), winCount(26, 0);
        for (char c : s1)
            s1Count[c - 'a']++;
        for (int i = 0; i < n1; i++)
            winCount[s2[i] - 'a']++;

        int matches = 0;
        for (int i = 0; i < 26; i++)
            if (s1Count[i] == winCount[i]) matches++;

        for (int right = n1; right < n2; right++) {
            if (matches == 26) return true;

            int idx = s2[right] - 'a';
            winCount[idx]++;
            if (winCount[idx] == s1Count[idx]) matches++;
            else if (winCount[idx] == s1Count[idx] + 1) matches--;

            idx = s2[right - n1] - 'a';
            winCount[idx]--;
            if (winCount[idx] == s1Count[idx]) matches++;
            else if (winCount[idx] == s1Count[idx] - 1) matches--;
        }
        return matches == 26;
    }
};
```

**Complexity:** Time O(n) where n = len(s2), Space O(1) (fixed 26-element arrays).

---

#### Problem 5: Minimum Window Substring (LeetCode 76) — Hard

**Link:** https://leetcode.com/problems/minimum-window-substring/

**Problem:** Given two strings `s` and `t`, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window. If no such substring exists, return `""`.

**Intuition:** Use a dynamic sliding window with two frequency maps: one for `t` and one for the current window. Track how many distinct characters have met their required frequency (`formed`). Expand `right` to include more characters. Whenever `formed` equals the number of unique characters in `t`, the window is valid — try shrinking from the left to minimize it. Record the shortest valid window found.

**Python:**

```python
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not s or not t:
            return ""

        from collections import Counter

        t_count = Counter(t)
        required = len(t_count)

        left = 0
        formed = 0
        window_counts = {}
        best = (float('inf'), 0, 0)  # (length, left, right)

        for right in range(len(s)):
            ch = s[right]
            window_counts[ch] = window_counts.get(ch, 0) + 1

            if ch in t_count and window_counts[ch] == t_count[ch]:
                formed += 1

            while formed == required:
                if right - left + 1 < best[0]:
                    best = (right - left + 1, left, right)

                leaving = s[left]
                window_counts[leaving] -= 1
                if leaving in t_count and window_counts[leaving] < t_count[leaving]:
                    formed -= 1
                left += 1

        return "" if best[0] == float('inf') else s[best[1]:best[2] + 1]
```

**C++:**

```cpp
class Solution {
public:
    string minWindow(string s, string t) {
        if (s.empty() || t.empty()) return "";

        unordered_map<char, int> tCount, winCount;
        for (char c : t) tCount[c]++;

        int required = tCount.size();
        int formed = 0;
        int left = 0;
        int bestLen = INT_MAX, bestLeft = 0;

        for (int right = 0; right < (int)s.size(); right++) {
            char ch = s[right];
            winCount[ch]++;

            if (tCount.count(ch) && winCount[ch] == tCount[ch])
                formed++;

            while (formed == required) {
                if (right - left + 1 < bestLen) {
                    bestLen = right - left + 1;
                    bestLeft = left;
                }

                char leaving = s[left];
                winCount[leaving]--;
                if (tCount.count(leaving) && winCount[leaving] < tCount[leaving])
                    formed--;
                left++;
            }
        }
        return bestLen == INT_MAX ? "" : s.substr(bestLeft, bestLen);
    }
};
```

**Complexity:** Time O(n + m) where n = len(s) and m = len(t), Space O(m) for the frequency maps.

---

#### Problem 6: Longest Repeating Character Replacement (LeetCode 424) — Medium

**Link:** https://leetcode.com/problems/longest-repeating-character-replacement/

**Problem:** `s` has uppercase letters. You may change at most `k` characters. Return the length of the longest substring that can be made of one repeated letter.

**Intuition:** A window is fixable when `window_length - count_of_most_frequent_letter ≤ k` (change everything that is not the majority letter). The textbook trick is the **non-shrinking window**: keep `max_freq` as the highest count seen so far (never decreased), and when the window becomes invalid, slide it right by one instead of shrinking it. The window's length is then always the best answer found so far.

Why a stale `max_freq` is safe: the window only **grows** when `length - max_freq ≤ k` with the new character included. Once the window has slid at least once, `length - max_freq == k` holds, so growth requires `max_freq` to increase. `max_freq` only increases when the character just added reaches that count inside the current window, so every growth corresponds to a genuinely valid window. Between growths, the window keeps its size while sliding; it may be invalid then, but it is never reported as a larger answer.

**Python:**

```python
class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        count = [0] * 26
        left = max_freq = 0
        for right, ch in enumerate(s):
            idx = ord(ch) - ord('A')
            count[idx] += 1
            max_freq = max(max_freq, count[idx])
            if (right - left + 1) - max_freq > k:     # invalid: slide, don't shrink
                count[ord(s[left]) - ord('A')] -= 1
                left += 1
        return len(s) - left                            # final window size = best size
```

**C++:**

```cpp
#include <algorithm>
#include <string>
using namespace std;

class Solution {
public:
    int characterReplacement(string s, int k) {
        int count[26] = {0};
        int left = 0, maxFreq = 0;
        for (int right = 0; right < static_cast<int>(s.size()); ++right) {
            maxFreq = max(maxFreq, ++count[s[right] - 'A']);
            if (right - left + 1 - maxFreq > k) {      // slide the window by one
                --count[s[left] - 'A'];
                ++left;
            }
        }
        return static_cast<int>(s.size()) - left;
    }
};
```

**Complexity:** Time O(n), Space O(1) (26 counters). The "honest" version that shrinks with `while` and recomputes `max(count)` each time is O(26n), which is equally acceptable in an interview; mention the trick as an optimisation.

---

#### Problem 7: Fruit Into Baskets (LeetCode 904) — Medium

**Link:** https://leetcode.com/problems/fruit-into-baskets/

**Problem:** `fruits[i]` is the fruit type of tree `i`. With two baskets, each holding a single type, collect from a contiguous run of trees. Return the maximum number of fruits.

**Intuition:** Strip the story away and this is the "longest subarray with **at most 2 distinct** values" problem. Keep a count per type in the window. When a third type enters, shrink from the left until one type's count reaches zero and it is removed from the map. Replacing 2 with K gives the general at-most-K-distinct template (Longest Substring with At Most K Distinct Characters, LC 340).

**Python:**

```python
from collections import defaultdict

class Solution:
    def totalFruit(self, fruits: list[int]) -> int:
        count = defaultdict(int)
        left = best = 0
        for right, f in enumerate(fruits):
            count[f] += 1
            while len(count) > 2:
                count[fruits[left]] -= 1
                if count[fruits[left]] == 0:
                    del count[fruits[left]]       # len(count) must equal #distinct in window
                left += 1
            best = max(best, right - left + 1)
        return best
```

**C++:**

```cpp
#include <algorithm>
#include <unordered_map>
#include <vector>
using namespace std;

class Solution {
public:
    int totalFruit(vector<int>& fruits) {
        unordered_map<int, int> count;
        int left = 0, best = 0;
        for (int right = 0; right < static_cast<int>(fruits.size()); ++right) {
            ++count[fruits[right]];
            while (count.size() > 2) {
                if (--count[fruits[left]] == 0) count.erase(fruits[left]);
                ++left;
            }
            best = max(best, right - left + 1);
        }
        return best;
    }
};
```

**Complexity:** Time O(n), Space O(1) (at most 3 map entries).

---

#### Problem 8: Subarrays with K Different Integers (LeetCode 992) — Hard

**Link:** https://leetcode.com/problems/subarrays-with-k-different-integers/

**Problem:** Count the subarrays of `nums` with **exactly** `k` distinct integers.

**Intuition:** "Exactly K" is not monotone: extending a window can move it from 2 distinct to 3 distinct, so a single window cannot count all valid subarrays. "At most K" **is** monotone, and for each `right` the valid starts form a contiguous range `[left, right]`, so `atMost(K)` adds `right - left + 1` at each step. Then:

```text
exactly(K) = atMost(K) - atMost(K - 1)
```

Example: `nums = [1, 2, 1, 2, 3]`, `k = 2`: `atMost(2) = 12`, `atMost(1) = 5`, answer 7.

**Python:**

```python
from collections import defaultdict

class Solution:
    def subarraysWithKDistinct(self, nums: list[int], k: int) -> int:
        def at_most(k: int) -> int:
            count = defaultdict(int)
            left = total = 0
            for right, x in enumerate(nums):
                if count[x] == 0:
                    k -= 1                        # a new distinct value enters
                count[x] += 1
                while k < 0:
                    count[nums[left]] -= 1
                    if count[nums[left]] == 0:
                        k += 1
                    left += 1
                total += right - left + 1         # all subarrays ending at right with <= k distinct
            return total

        return at_most(k) - at_most(k - 1)
```

**C++:**

```cpp
#include <vector>
using namespace std;

class Solution {
    long long atMost(const vector<int>& nums, int k) {
        vector<int> count(nums.size() + 1, 0);    // 1 <= nums[i] <= n
        long long total = 0;
        int left = 0;
        for (int right = 0; right < static_cast<int>(nums.size()); ++right) {
            if (count[nums[right]]++ == 0) --k;
            while (k < 0) {
                if (--count[nums[left]] == 0) ++k;
                ++left;
            }
            total += right - left + 1;
        }
        return total;
    }

public:
    int subarraysWithKDistinct(vector<int>& nums, int k) {
        return static_cast<int>(atMost(nums, k) - atMost(nums, k - 1));
    }
};
```

**Complexity:** Time O(n) (two linear passes), Space O(n). The same subtraction counts "exactly K ones" (LC 930 with sum K over a binary array) and "exactly K odd numbers" (LC 1248).

---

#### Problem 9: Shortest Subarray with Sum at Least K (LeetCode 862) — Hard

**Link:** https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/

**Problem:** Return the length of the shortest non-empty subarray with sum ≥ `k`, or `-1`. Values can be **negative**.

**Intuition:** With negatives, the plain window fails: shrinking can increase the sum, and growing can decrease it. Use prefix sums `P` (see [Prefix Sum](#21-prefix-sum--difference-array)): we want `j - i` minimal with `P[j] - P[i] ≥ k`, `i < j`. Keep a deque of candidate start indices `i` with **increasing** `P[i]`:

1. **Front pops**: while `P[j] - P[front] ≥ k`, record `j - front` and pop the front. Any later `j' > j` would give a longer subarray from that start, so the start is never needed again.
2. **Back pops**: while `P[back] ≥ P[j]`, pop the back. Index `j` is a later start with a smaller or equal prefix, so it is at least as good for every future end.

**Python:**

```python
from collections import deque

class Solution:
    def shortestSubarray(self, nums: list[int], k: int) -> int:
        prefix = [0]
        for x in nums:
            prefix.append(prefix[-1] + x)
        best = len(nums) + 1
        dq: deque[int] = deque()                  # indices into prefix, increasing prefix values
        for j, pj in enumerate(prefix):
            while dq and pj - prefix[dq[0]] >= k:
                best = min(best, j - dq.popleft())
            while dq and prefix[dq[-1]] >= pj:
                dq.pop()
            dq.append(j)
        return best if best <= len(nums) else -1
```

**C++:**

```cpp
#include <algorithm>
#include <deque>
#include <vector>
using namespace std;

class Solution {
public:
    int shortestSubarray(vector<int>& nums, int k) {
        int n = nums.size();
        vector<long long> prefix(n + 1, 0);
        for (int i = 0; i < n; ++i) prefix[i + 1] = prefix[i] + nums[i];
        int best = n + 1;
        deque<int> dq;
        for (int j = 0; j <= n; ++j) {
            while (!dq.empty() && prefix[j] - prefix[dq.front()] >= k) {
                best = min(best, j - dq.front());
                dq.pop_front();
            }
            while (!dq.empty() && prefix[dq.back()] >= prefix[j]) dq.pop_back();
            dq.push_back(j);
        }
        return best <= n ? best : -1;
    }
};
```

**Complexity:** Time O(n): each index is pushed and popped at most once. Space O(n).

---

### Interview Q&A

**Q1.** When is a sliding window valid, and how do you check quickly?

The window technique needs **monotone validity**: if a window is valid, every sub-window obtained by shrinking it from the left is also valid (for "at most" constraints), or every window that extends a valid window is also valid, so shrinking never repairs an invalid one (for "at least" constraints such as sum >= k with non-negative values). Then for each `right`, the valid `left` positions form a contiguous range, and `left` only moves forward, so the whole scan is O(n). Quick check: does adding an element only make the constraint harder (sum of non-negatives, number of distinct values, count of zeros)? If adding an element can make it easier (negative numbers in a sum constraint), the window breaks; use prefix sums with a hash map or a deque.

**Q2.** Why does `exactly(K) = atMost(K) - atMost(K - 1)` work, and where else is the trick useful?

The sets are nested: every subarray with at most `K - 1` distinct values also has at most `K`. The difference is exactly the subarrays with `K` distinct values. The trick turns a non-monotone "exactly" condition into two monotone "at most" conditions, each countable with one window pass. It applies to any count-based constraint that is monotone in window size: exactly K odd numbers, exactly K ones, sum exactly K over a binary array. It does not apply to sums with negative values, which are not monotone; use prefix sum + hash map there.

**Q3.** Contrast LC 209 (Minimum Size Subarray Sum, positives) with LC 862 (negatives allowed).

LC 209: all values positive, so the sum is monotone in window size. Shrink while `sum ≥ target`, O(n) with O(1) space. LC 862: negatives break that. The prefix-sum view still works: minimise `j - i` subject to `P[j] - P[i] ≥ k`. A monotonic deque keeps only start indices that could still be optimal (increasing prefix values), and each index is popped at most once, so it is still O(n) but needs O(n) space. A Fenwick tree or sorted structure over prefix sums gives O(n log n) as a fallback.

**Q4.** The interviewer asks for the same answer on an unbounded stream. What changes?

Fixed-size windows become ring buffers of the last `k` elements, which is O(k) memory and O(1) per element. Variable windows over a stream need the window contents (a deque) and the summary state (counts, sum, monotonic deque for max). "Longest so far" stays O(1) extra. If the window is time-based (last 60 seconds), evict by timestamp from the front of a deque. If even the window does not fit in memory, use approximations: exponential histograms (DGIM) for counts over a sliding window, or Count-Min sketches per time bucket for frequencies.

**Q5.** Your window code passes the examples but fails on a hidden test. What do you check first?

(1) The shrink loop is `while`, not `if` (unless you are deliberately using the non-shrinking trick). (2) State is updated on **both** sides: increment on enter, decrement on leave, and delete zero counts if you use `len(map)`. (3) The answer is recorded at the right moment: after shrinking for "longest valid", inside the shrink loop for "shortest valid". (4) Off-by-one in the length `right - left + 1`. (5) Empty input and `k = 0`. (6) Overflow of the running sum in C++.

---
## 3. Fast and Slow Pointers

### Overview

Also known as the **"Tortoise and Hare"** algorithm, this pattern uses two pointers that move through a data structure at different speeds. Typically, the **slow** pointer advances one step at a time while the **fast** pointer advances two steps. If a cycle exists, the fast pointer will eventually "lap" the slow pointer, and they will meet inside the cycle. Beyond cycle detection, this technique elegantly finds the middle element of a linked list in a single pass and forms the basis of **Floyd's cycle-finding algorithm**, which can also locate the exact start of a cycle.

### When to Use

- Detecting cycles in a linked list or array
- Finding the middle of a linked list
- Finding the start (entry point) of a cycle
- Detecting if a number is a "happy number"
- Finding the duplicate number in an array with values in `[1, n]`

### Template Code

#### 1. Cycle Detection

**Python:**

```python
def has_cycle(head: ListNode) -> bool:
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

**C++:**

```cpp
bool hasCycle(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return true;
    }
    return false;
}
```

#### 2. Find Middle of Linked List

**Python:**

```python
def find_middle(head: ListNode) -> ListNode:
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow  # for even-length lists, returns the second middle node
```

**C++:**

```cpp
ListNode* findMiddle(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    return slow;
}
```

#### 3. Find Cycle Start (Floyd's Algorithm — Phase 2)

After detecting a meeting point inside the cycle, reset one pointer to the head. Move both pointers one step at a time — they meet at the cycle's entry node.

**Python:**

```python
def find_cycle_start(head: ListNode) -> ListNode:
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            # Phase 2: find entry point
            entry = head
            while entry != slow:
                entry = entry.next
                slow = slow.next
            return entry
    return None
```

**C++:**

```cpp
ListNode* findCycleStart(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) {
            ListNode* entry = head;
            while (entry != slow) {
                entry = entry->next;
                slow = slow->next;
            }
            return entry;
        }
    }
    return nullptr;
}
```

### Variations

| Variation | Description |
|---|---|
| **Basic cycle detection** | Fast and slow meet → cycle exists. If fast reaches `null` → no cycle. |
| **Cycle start finding** | Floyd's complete algorithm: Phase 1 finds meeting point, Phase 2 finds entry. |
| **Middle finding** | When fast reaches the end, slow is at the middle. |
| **Rearranging linked lists** | Use middle-finding to split the list into two halves, then merge/reverse as needed. |

### Common Mistakes

1. **Not checking for null before advancing the fast pointer** — Both `fast` AND `fast.next` must be non-null before calling `fast.next.next`. Missing either check causes a null-pointer dereference.
2. **Confusing the two phases of Floyd's algorithm** — Phase 1 (detecting the meeting point inside the cycle) and Phase 2 (finding the cycle entry) are distinct steps with different movement rules.
3. **Using wrong initialization** — For cycle detection both pointers typically start at `head`. For some problems (e.g., finding first middle in even-length lists) you might start `fast` at `head.next`; mixing these up changes the result.
4. **Forgetting edge cases** — Empty list (`head is None`), single-node list, or a list with no cycle must all be handled before entering the loop.

### Related Patterns

- **Two Pointers** — Same family of techniques; Fast & Slow is a specialization where pointers move at different rates rather than from opposite ends.
- **Linked List Reversal** — Often combined with middle-finding to solve problems like palindrome checking or list reordering.

---

### Example Problems

---

### Problem 1: Linked List Cycle (LeetCode 141) — Easy

**Link:** https://leetcode.com/problems/linked-list-cycle/

**Problem Statement:**
Given `head`, the head of a linked list, determine if the linked list has a cycle in it. Return `true` if there is a cycle, `false` otherwise.

**Intuition / Approach:**
Use two pointers: `slow` moves one step, `fast` moves two steps. If the list has a cycle, the fast pointer will eventually catch up to the slow pointer (they will occupy the same node). If the list has no cycle, the fast pointer will reach the end (`null`).

**Python:**

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
        return False
```

**C++:**

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
    bool hasCycle(ListNode* head) {
        ListNode* slow = head;
        ListNode* fast = head;
        while (fast && fast->next) {
            slow = slow->next;
            fast = fast->next->next;
            if (slow == fast) return true;
        }
        return false;
    }
};
```

**Complexity:**
- **Time:** O(n) — each node is visited at most twice.
- **Space:** O(1) — only two pointers used.

---

### Problem 2: Middle of the Linked List (LeetCode 876) — Easy

**Link:** https://leetcode.com/problems/middle-of-the-linked-list/

**Problem Statement:**
Given the `head` of a singly linked list, return the middle node. If there are two middle nodes, return the **second** middle node.

**Intuition / Approach:**
`slow` moves one step, `fast` moves two steps. When `fast` reaches the end, `slow` is at the middle. For an even-length list `[1,2,3,4]`, `fast` runs out after `slow` passes the first middle, so `slow` lands on the second middle node — exactly what the problem asks for.

**Python:**

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow
```

**C++:**

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    ListNode* middleNode(ListNode* head) {
        ListNode* slow = head;
        ListNode* fast = head;
        while (fast && fast->next) {
            slow = slow->next;
            fast = fast->next->next;
        }
        return slow;
    }
};
```

**Complexity:**
- **Time:** O(n) — single pass through the list.
- **Space:** O(1) — two pointers.

---

### Problem 3: Linked List Cycle II (LeetCode 142) — Medium

**Link:** https://leetcode.com/problems/linked-list-cycle-ii/

**Problem Statement:**
Given the `head` of a linked list, return the node where the cycle begins. If there is no cycle, return `null`.

**Intuition / Approach:**
This is Floyd's complete cycle-finding algorithm in two phases:

- **Phase 1 — Detect the meeting point:** Move `slow` by 1 and `fast` by 2. If they meet, a cycle exists.
- **Phase 2 — Find the entry:** Place a new pointer `entry` at `head`. Move `entry` and `slow` both by 1 step at a time. The node where they meet is the cycle start.

*Why does Phase 2 work?* Let the distance from head to cycle start be `a`, cycle start to meeting point be `b`, and the remaining cycle length be `c`. At the meeting point, slow traveled `a + b` and fast traveled `a + b + k(b + c)` for some `k ≥ 1`. Since fast travels twice as far: `2(a + b) = a + b + k(b + c)`, giving `a = (k-1)(b + c) + c`. This means walking `a` steps from the meeting point lands exactly at the cycle start — the same distance as walking from the head.

**Python:**

```python
class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                entry = head
                while entry != slow:
                    entry = entry.next
                    slow = slow.next
                return entry
        return None
```

**C++:**

```cpp
class Solution {
public:
    ListNode* detectCycle(ListNode* head) {
        ListNode* slow = head;
        ListNode* fast = head;
        while (fast && fast->next) {
            slow = slow->next;
            fast = fast->next->next;
            if (slow == fast) {
                ListNode* entry = head;
                while (entry != slow) {
                    entry = entry->next;
                    slow = slow->next;
                }
                return entry;
            }
        }
        return nullptr;
    }
};
```

**Complexity:**
- **Time:** O(n) — both phases combined visit each node a constant number of times.
- **Space:** O(1) — only pointer variables.

---

### Problem 4: Happy Number (LeetCode 202) — Medium

**Link:** https://leetcode.com/problems/happy-number/

**Problem Statement:**
A **happy number** is defined by the following process: Starting with any positive integer, replace the number by the sum of the squares of its digits. Repeat until the number equals `1` (it is happy) or it loops endlessly in a cycle (it is not happy). Return `true` if `n` is a happy number.

**Intuition / Approach:**
The sequence of sum-of-squares values either reaches `1` or enters a cycle. This is equivalent to cycle detection in an implicit linked list where each number points to the sum of squares of its digits. Apply fast and slow pointers: `slow` computes one step, `fast` computes two steps. If they meet at `1`, the number is happy. If they meet at any other value, a cycle exists and the number is not happy.

**Python:**

```python
class Solution:
    def isHappy(self, n: int) -> bool:
        def get_next(num: int) -> int:
            total = 0
            while num > 0:
                num, digit = divmod(num, 10)
                total += digit * digit
            return total

        slow, fast = n, get_next(n)
        while fast != 1 and slow != fast:
            slow = get_next(slow)
            fast = get_next(get_next(fast))
        return fast == 1
```

**C++:**

```cpp
class Solution {
public:
    int getNext(int n) {
        int total = 0;
        while (n > 0) {
            int digit = n % 10;
            total += digit * digit;
            n /= 10;
        }
        return total;
    }

    bool isHappy(int n) {
        int slow = n;
        int fast = getNext(n);
        while (fast != 1 && slow != fast) {
            slow = getNext(slow);
            fast = getNext(getNext(fast));
        }
        return fast == 1;
    }
};
```

**Complexity:**
- **Time:** O(log n) — the number of digits is O(log n), and the sequence converges or cycles quickly.
- **Space:** O(1) — no extra data structures.

---

### Problem 5: Find the Duplicate Number (LeetCode 287) — Hard

**Link:** https://leetcode.com/problems/find-the-duplicate-number/

**Problem Statement:**
Given an array of integers `nums` containing `n + 1` integers where each integer is in the range `[1, n]` inclusive, there is exactly one repeated number. Find and return this duplicate. You must solve it **without modifying** the array and using only **O(1)** extra space.

**Intuition / Approach:**
Treat the array as an implicit linked list: index `i` has a "next pointer" to index `nums[i]`. Since values are in `[1, n]` and the array has `n + 1` elements, there must be a cycle, and the duplicate value is the entry point of the cycle.

- **Phase 1:** Start both `slow` and `fast` at index `0`. Move `slow = nums[slow]` and `fast = nums[nums[fast]]` until they meet inside the cycle.
- **Phase 2:** Reset one pointer to `0`. Move both one step at a time. The index where they meet is the duplicate number.

This is a direct application of Floyd's algorithm on an implicit graph.

**Python:**

```python
class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        # Phase 1: find meeting point inside the cycle
        slow, fast = nums[0], nums[nums[0]]
        while slow != fast:
            slow = nums[slow]
            fast = nums[nums[fast]]

        # Phase 2: find the cycle entry (the duplicate value)
        slow = 0
        while slow != fast:
            slow = nums[slow]
            fast = nums[fast]
        return slow
```

**C++:**

```cpp
class Solution {
public:
    int findDuplicate(vector<int>& nums) {
        // Phase 1: find meeting point inside the cycle
        int slow = nums[0];
        int fast = nums[nums[0]];
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[nums[fast]];
        }

        // Phase 2: find the cycle entry (the duplicate value)
        slow = 0;
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[fast];
        }
        return slow;
    }
};
```

**Complexity:**
- **Time:** O(n) — each element is visited at most a constant number of times.
- **Space:** O(1) — no additional data structures; the array is not modified.

---
## 4. Merge Intervals

### Overview

The Merge Intervals pattern deals with overlapping intervals. The key insight is to **sort intervals by start time**, then iterate and merge overlapping ones. Two intervals `[a, b]` and `[c, d]` overlap if `a <= d` and `c <= b` (assuming `a <= c` after sorting). After sorting, the merge condition simplifies to: the current interval overlaps with the previous if `current.start <= previous.end`.

### When to Use

- Merging overlapping intervals
- Inserting a new interval into a sorted list
- Finding intersections of interval lists
- Minimum number of meeting rooms / platforms
- Problems involving time ranges, schedules, or ranges on a number line

### Template Code

**Python:**

```python
def merge_intervals(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged
```

**C++:**

```cpp
vector<vector<int>> mergeIntervals(vector<vector<int>>& intervals) {
    sort(intervals.begin(), intervals.end());
    vector<vector<int>> merged = {intervals[0]};
    for (int i = 1; i < intervals.size(); i++) {
        if (intervals[i][0] <= merged.back()[1]) {
            merged.back()[1] = max(merged.back()[1], intervals[i][1]);
        } else {
            merged.push_back(intervals[i]);
        }
    }
    return merged;
}
```

### Variations

| Variation | Key Difference |
|---|---|
| Merge overlapping intervals | Standard template — merge when `current.start <= prev.end` |
| Insert interval | Find the correct position, then merge surrounding overlaps |
| Interval intersection | Two pointers across two sorted interval lists |
| Meeting rooms (count overlaps) | Sweep line with start/end events, or sort + min-heap |

### Common Mistakes

- Forgetting to sort intervals first
- Using wrong merge condition (`>` vs `>=`)
- Not updating the end of the merged interval with `max(end1, end2)` — a later interval can be entirely contained within an earlier one
- Confusing "merge" with "intersection" — merge produces the union, intersection produces the overlap

### Related Patterns

Sorting, Greedy, Two Pointers

---

### Example Problems

---

### 4.1 Easy — Meeting Rooms (LeetCode 252)

> **Problem**: Given an array of meeting time intervals `[start, end]`, determine if a person could attend all meetings (i.e., no two meetings overlap).

[LeetCode 252 — Meeting Rooms](https://leetcode.com/problems/meeting-rooms/)

**Intuition / Approach**:
Sort intervals by start time. If any meeting starts before the previous one ends, there is a conflict. A single linear scan after sorting is sufficient.

**Python:**

```python
class Solution:
    def canAttendMeetings(self, intervals: list[list[int]]) -> bool:
        intervals.sort(key=lambda x: x[0])
        for i in range(1, len(intervals)):
            if intervals[i][0] < intervals[i - 1][1]:
                return False
        return True
```

**C++:**

```cpp
class Solution {
public:
    bool canAttendMeetings(vector<vector<int>>& intervals) {
        sort(intervals.begin(), intervals.end());
        for (int i = 1; i < (int)intervals.size(); i++) {
            if (intervals[i][0] < intervals[i - 1][1]) {
                return false;
            }
        }
        return true;
    }
};
```

| Complexity | Value |
|---|---|
| Time | O(n log n) — dominated by sorting |
| Space | O(1) extra (O(log n) for sort stack) |

---

### 4.2 Medium — Merge Intervals (LeetCode 56)

> **Problem**: Given an array of intervals where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals and return an array of the non-overlapping intervals that cover all the intervals in the input.

[LeetCode 56 — Merge Intervals](https://leetcode.com/problems/merge-intervals/)

**Intuition / Approach**:
Sort by start time. Iterate through intervals: if the current interval's start is ≤ the last merged interval's end, extend the last merged interval's end to `max(last.end, current.end)`. Otherwise, push the current interval as a new entry.

**Python:**

```python
class Solution:
    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        intervals.sort(key=lambda x: x[0])
        merged = [intervals[0]]
        for start, end in intervals[1:]:
            if start <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], end)
            else:
                merged.append([start, end])
        return merged
```

**C++:**

```cpp
class Solution {
public:
    vector<vector<int>> merge(vector<vector<int>>& intervals) {
        sort(intervals.begin(), intervals.end());
        vector<vector<int>> merged = {intervals[0]};
        for (int i = 1; i < (int)intervals.size(); i++) {
            if (intervals[i][0] <= merged.back()[1]) {
                merged.back()[1] = max(merged.back()[1], intervals[i][1]);
            } else {
                merged.push_back(intervals[i]);
            }
        }
        return merged;
    }
};
```

| Complexity | Value |
|---|---|
| Time | O(n log n) |
| Space | O(n) for the output array |

---

### 4.3 Medium — Insert Interval (LeetCode 57)

> **Problem**: You are given an array of non-overlapping intervals `intervals` sorted by start, and a new interval `newInterval`. Insert `newInterval` into `intervals` such that the result is still sorted and non-overlapping (merge if necessary).

[LeetCode 57 — Insert Interval](https://leetcode.com/problems/insert-interval/)

**Intuition / Approach**:
Three-phase linear scan:
1. Add all intervals that end before the new interval starts (no overlap).
2. Merge all intervals that overlap with the new interval by expanding the new interval's bounds.
3. Add all remaining intervals that start after the new interval ends.

**Python:**

```python
class Solution:
    def insert(self, intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:
        result = []
        i = 0
        n = len(intervals)

        # Phase 1: intervals that come entirely before newInterval
        while i < n and intervals[i][1] < newInterval[0]:
            result.append(intervals[i])
            i += 1

        # Phase 2: merge overlapping intervals with newInterval
        while i < n and intervals[i][0] <= newInterval[1]:
            newInterval[0] = min(newInterval[0], intervals[i][0])
            newInterval[1] = max(newInterval[1], intervals[i][1])
            i += 1
        result.append(newInterval)

        # Phase 3: intervals that come entirely after newInterval
        while i < n:
            result.append(intervals[i])
            i += 1

        return result
```

**C++:**

```cpp
class Solution {
public:
    vector<vector<int>> insert(vector<vector<int>>& intervals, vector<int>& newInterval) {
        vector<vector<int>> result;
        int i = 0, n = intervals.size();

        // Phase 1
        while (i < n && intervals[i][1] < newInterval[0]) {
            result.push_back(intervals[i]);
            i++;
        }

        // Phase 2
        while (i < n && intervals[i][0] <= newInterval[1]) {
            newInterval[0] = min(newInterval[0], intervals[i][0]);
            newInterval[1] = max(newInterval[1], intervals[i][1]);
            i++;
        }
        result.push_back(newInterval);

        // Phase 3
        while (i < n) {
            result.push_back(intervals[i]);
            i++;
        }

        return result;
    }
};
```

| Complexity | Value |
|---|---|
| Time | O(n) — single pass through sorted intervals |
| Space | O(n) for the output array |

---

### 4.4 Medium — Non-overlapping Intervals (LeetCode 435)

> **Problem**: Given an array of intervals, return the minimum number of intervals you need to remove to make the rest non-overlapping.

[LeetCode 435 — Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/)

**Intuition / Approach**:
This is the classic **interval scheduling maximization** problem. Sort by **end time**. Greedily keep the interval that ends earliest (it leaves the most room for future intervals). Whenever an interval overlaps with the last kept one, remove it (increment count). The answer is `n - (max non-overlapping intervals)`.

**Python:**

```python
class Solution:
    def eraseOverlapIntervals(self, intervals: list[list[int]]) -> int:
        intervals.sort(key=lambda x: x[1])
        removals = 0
        prev_end = float('-inf')
        for start, end in intervals:
            if start >= prev_end:
                prev_end = end
            else:
                removals += 1
        return removals
```

**C++:**

```cpp
class Solution {
public:
    int eraseOverlapIntervals(vector<vector<int>>& intervals) {
        sort(intervals.begin(), intervals.end(),
             [](const vector<int>& a, const vector<int>& b) {
                 return a[1] < b[1];
             });
        int removals = 0;
        int prevEnd = INT_MIN;
        for (auto& iv : intervals) {
            if (iv[0] >= prevEnd) {
                prevEnd = iv[1];
            } else {
                removals++;
            }
        }
        return removals;
    }
};
```

| Complexity | Value |
|---|---|
| Time | O(n log n) |
| Space | O(1) extra (O(log n) for sort stack) |

---

### 4.5 Hard — Employee Free Time (LeetCode 759)

> **Problem**: We are given a list of `schedule` where `schedule[i]` is the list of working intervals for employee `i` (each interval is `[start, end]`, sorted and non-overlapping per employee). Return the list of finite intervals representing the **common free time** for all employees, sorted in order.

[LeetCode 759 — Employee Free Time](https://leetcode.com/problems/employee-free-time/)

**Intuition / Approach**:
Flatten all intervals into one list, sort by start time, and merge them. The gaps between consecutive merged intervals are the common free times. Alternatively, use a min-heap to merge-sort the per-employee sorted lists.

**Python:**

```python
class Interval:
    def __init__(self, start: int = 0, end: int = 0):
        self.start = start
        self.end = end

class Solution:
    def employeeFreeTime(self, schedule: list[list['Interval']]) -> list['Interval']:
        # Flatten all intervals
        all_intervals = []
        for emp in schedule:
            for iv in emp:
                all_intervals.append((iv.start, iv.end))

        all_intervals.sort()

        merged = [all_intervals[0]]
        for start, end in all_intervals[1:]:
            if start <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))
            else:
                merged.append((start, end))

        # Gaps between merged intervals are free times
        free = []
        for i in range(1, len(merged)):
            free.append(Interval(merged[i - 1][1], merged[i][0]))

        return free
```

**C++ (using the LeetCode `Interval` class):**

```cpp
/*
class Interval {
public:
    int start;
    int end;
    Interval() {}
    Interval(int _start, int _end) : start(_start), end(_end) {}
};
*/

class Solution {
public:
    vector<Interval> employeeFreeTime(vector<vector<Interval>> schedule) {
        vector<pair<int,int>> all;
        for (auto& emp : schedule) {
            for (auto& iv : emp) {
                all.push_back({iv.start, iv.end});
            }
        }
        sort(all.begin(), all.end());

        // Merge intervals
        vector<pair<int,int>> merged = {all[0]};
        for (int i = 1; i < (int)all.size(); i++) {
            if (all[i].first <= merged.back().second) {
                merged.back().second = max(merged.back().second, all[i].second);
            } else {
                merged.push_back(all[i]);
            }
        }

        // Gaps are free times
        vector<Interval> result;
        for (int i = 1; i < (int)merged.size(); i++) {
            result.emplace_back(merged[i - 1].second, merged[i].first);
        }
        return result;
    }
};
```

| Complexity | Value |
|---|---|
| Time | O(n log n) where n = total number of intervals across all employees |
| Space | O(n) for the flattened and merged arrays |

---

## 5. Cyclic Sort

### Overview

Cyclic Sort is used when dealing with arrays containing numbers in a given range (usually `1` to `n` or `0` to `n`). The core idea: **for each index `i`, place the element at its correct position** — `nums[i]` should go to index `nums[i] - 1` (for 1-indexed values). After one pass of swapping every element into its correct slot, any element that is *not* at its expected position reveals a **missing** or **duplicate** number.

The technique achieves O(n) time and O(1) space because each element is swapped at most once to its correct position.

### When to Use

- Array contains numbers in range `[1, n]` or `[0, n]`
- Find missing number(s)
- Find duplicate number(s)
- Find the first missing positive
- Constant space requirement for the above problems

### Template Code

**Python:**

```python
def cyclic_sort(nums):
    i = 0
    while i < len(nums):
        correct = nums[i] - 1  # where nums[i] should be (1-indexed values)
        if nums[i] != nums[correct]:
            nums[i], nums[correct] = nums[correct], nums[i]
        else:
            i += 1
```

**C++:**

```cpp
void cyclicSort(vector<int>& nums) {
    int i = 0;
    while (i < (int)nums.size()) {
        int correct = nums[i] - 1;  // 1-indexed values
        if (nums[i] != nums[correct]) {
            swap(nums[i], nums[correct]);
        } else {
            i++;
        }
    }
}
```

### Variations

| Variation | Key Difference |
|---|---|
| Find one missing number | After sort, find index where `nums[i] != i + 1` |
| Find all missing numbers | Collect all indices where `nums[i] != i + 1` |
| Find duplicate | After sort, element not at its correct index is the duplicate |
| Find all duplicates | Collect all elements not at their correct indices |
| First missing positive | Only sort positive numbers in range `[1, n]` into correct positions |

### Common Mistakes

- **Using a `for` loop instead of `while`**: After swapping, the new element at index `i` must also be checked — a `for` loop would skip it
- **Infinite loop with duplicates**: If `nums[i] == nums[correct]` but `i != correct`, the swap is pointless and loops forever — always check `nums[i] != nums[correct]` (not `nums[i] != correct + 1`)
- **Off-by-one between 0-indexed and 1-indexed**: For values in `[1, n]`, correct index = `nums[i] - 1`. For values in `[0, n]`, correct index = `nums[i]`
- **Forgetting that the swapped-in element needs checking**: This is why `i` only advances when no swap occurs

### Related Patterns

In-place Operations, Bit Manipulation

---

### Example Problems

---

### 5.1 Easy — Missing Number (LeetCode 268)

> **Problem**: Given an array `nums` containing `n` distinct numbers in the range `[0, n]`, return the one number in the range that is missing from the array.

[LeetCode 268 — Missing Number](https://leetcode.com/problems/missing-number/)

**Intuition / Approach**:
Place each number at index equal to its value (value `v` goes to index `v`). Since numbers are in `[0, n]` but the array has only `n` slots (indices `0` to `n-1`), values equal to `n` have no valid position and are skipped. After sorting, the index whose value doesn't match is the answer. If all match, `n` is missing.

**Python:**

```python
class Solution:
    def missingNumber(self, nums: list[int]) -> int:
        n = len(nums)
        i = 0
        while i < n:
            correct = nums[i]
            if nums[i] < n and nums[i] != nums[correct]:
                nums[i], nums[correct] = nums[correct], nums[i]
            else:
                i += 1

        for i in range(n):
            if nums[i] != i:
                return i
        return n
```

**C++:**

```cpp
class Solution {
public:
    int missingNumber(vector<int>& nums) {
        int n = nums.size();
        int i = 0;
        while (i < n) {
            int correct = nums[i];
            if (nums[i] < n && nums[i] != nums[correct]) {
                swap(nums[i], nums[correct]);
            } else {
                i++;
            }
        }
        for (int i = 0; i < n; i++) {
            if (nums[i] != i) return i;
        }
        return n;
    }
};
```

| Complexity | Value |
|---|---|
| Time | O(n) |
| Space | O(1) |

---

### 5.2 Easy — Find All Numbers Disappeared in an Array (LeetCode 448)

> **Problem**: Given an array `nums` of `n` integers where `nums[i]` is in the range `[1, n]`, return an array of all the integers in `[1, n]` that do not appear in `nums`.

[LeetCode 448 — Find All Numbers Disappeared in an Array](https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/)

**Intuition / Approach**:
Cyclic sort with 1-indexed values: value `v` belongs at index `v - 1`. After sorting, scan for positions where `nums[i] != i + 1` — those missing values (`i + 1`) are the answer.

**Python:**

```python
class Solution:
    def findDisappearedNumbers(self, nums: list[int]) -> list[int]:
        i = 0
        while i < len(nums):
            correct = nums[i] - 1
            if nums[i] != nums[correct]:
                nums[i], nums[correct] = nums[correct], nums[i]
            else:
                i += 1

        result = []
        for i in range(len(nums)):
            if nums[i] != i + 1:
                result.append(i + 1)
        return result
```

**C++:**

```cpp
class Solution {
public:
    vector<int> findDisappearedNumbers(vector<int>& nums) {
        int i = 0;
        while (i < (int)nums.size()) {
            int correct = nums[i] - 1;
            if (nums[i] != nums[correct]) {
                swap(nums[i], nums[correct]);
            } else {
                i++;
            }
        }

        vector<int> result;
        for (int i = 0; i < (int)nums.size(); i++) {
            if (nums[i] != i + 1) {
                result.push_back(i + 1);
            }
        }
        return result;
    }
};
```

| Complexity | Value |
|---|---|
| Time | O(n) |
| Space | O(1) extra (output not counted) |

---

### 5.3 Medium — Find the Duplicate Number (LeetCode 287)

> **Problem**: Given an array of integers `nums` containing `n + 1` integers where each integer is in the range `[1, n]` inclusive, there is exactly one repeated number. Return this repeated number. You must solve it **without modifying** the array and using only **constant extra space**.

[LeetCode 287 — Find the Duplicate Number](https://leetcode.com/problems/find-the-duplicate-number/)

**Intuition / Approach**:
The strict constraint says "without modifying the array," making Floyd's Tortoise and Hare (cycle detection) the intended approach. However, if modification is allowed, cyclic sort works beautifully: place each value at its correct index; when you encounter a value that's already at its correct position, that's the duplicate.

Below we show both approaches. The **cyclic sort approach** modifies the array. The **Floyd's cycle detection** approach satisfies the strict constraints.

**Python (Cyclic Sort — modifies array):**

```python
class Solution:
    def findDuplicate(self, nums: list[int]) -> int:
        i = 0
        while i < len(nums):
            correct = nums[i] - 1
            if nums[i] != nums[correct]:
                nums[i], nums[correct] = nums[correct], nums[i]
            else:
                if i != correct:
                    return nums[i]
                i += 1
        return -1
```

**Python (Floyd's Cycle Detection — no modification):**

```python
class Solution:
    def findDuplicate(self, nums: list[int]) -> int:
        slow = fast = nums[0]
        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break

        slow = nums[0]
        while slow != fast:
            slow = nums[slow]
            fast = nums[fast]
        return slow
```

**C++ (Cyclic Sort — modifies array):**

```cpp
class Solution {
public:
    int findDuplicate(vector<int>& nums) {
        int i = 0;
        while (i < (int)nums.size()) {
            int correct = nums[i] - 1;
            if (nums[i] != nums[correct]) {
                swap(nums[i], nums[correct]);
            } else {
                if (i != correct) return nums[i];
                i++;
            }
        }
        return -1;
    }
};
```

**C++ (Floyd's Cycle Detection — no modification):**

```cpp
class Solution {
public:
    int findDuplicate(vector<int>& nums) {
        int slow = nums[0], fast = nums[0];
        do {
            slow = nums[slow];
            fast = nums[nums[fast]];
        } while (slow != fast);

        slow = nums[0];
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[fast];
        }
        return slow;
    }
};
```

| Complexity | Cyclic Sort | Floyd's Cycle Detection |
|---|---|---|
| Time | O(n) | O(n) |
| Space | O(1) | O(1) |
| Modifies input? | Yes | No |

---

### 5.4 Medium — Find All Duplicates in an Array (LeetCode 442)

> **Problem**: Given an integer array `nums` of length `n` where all integers are in the range `[1, n]` and each integer appears **once or twice**, return an array of all integers that appear twice. You must solve it in O(n) time and O(1) extra space.

[LeetCode 442 — Find All Duplicates in an Array](https://leetcode.com/problems/find-all-duplicates-in-an-array/)

**Intuition / Approach**:
Cyclic sort: place each value at index `value - 1`. After sorting, any position where `nums[i] != i + 1` means `nums[i]` is a duplicate (it couldn't go to its correct position because the correct value was already there).

**Python:**

```python
class Solution:
    def findDuplicates(self, nums: list[int]) -> list[int]:
        i = 0
        while i < len(nums):
            correct = nums[i] - 1
            if nums[i] != nums[correct]:
                nums[i], nums[correct] = nums[correct], nums[i]
            else:
                i += 1

        result = []
        for i in range(len(nums)):
            if nums[i] != i + 1:
                result.append(nums[i])
        return result
```

**C++:**

```cpp
class Solution {
public:
    vector<int> findDuplicates(vector<int>& nums) {
        int i = 0;
        while (i < (int)nums.size()) {
            int correct = nums[i] - 1;
            if (nums[i] != nums[correct]) {
                swap(nums[i], nums[correct]);
            } else {
                i++;
            }
        }

        vector<int> result;
        for (int i = 0; i < (int)nums.size(); i++) {
            if (nums[i] != i + 1) {
                result.push_back(nums[i]);
            }
        }
        return result;
    }
};
```

| Complexity | Value |
|---|---|
| Time | O(n) |
| Space | O(1) extra (output not counted) |

---

### 5.5 Hard — First Missing Positive (LeetCode 41)

> **Problem**: Given an unsorted integer array `nums`, return the smallest positive integer that is not present in `nums`. You must implement an algorithm that runs in O(n) time and uses O(1) auxiliary space.

[LeetCode 41 — First Missing Positive](https://leetcode.com/problems/first-missing-positive/)

**Intuition / Approach**:
The answer must be in the range `[1, n+1]` (where `n = len(nums)`). Use cyclic sort to place each value `v` in `[1, n]` at index `v - 1`. Ignore values ≤ 0 or > n (they can't be the answer's placeholder). After sorting, the first index `i` where `nums[i] != i + 1` gives the answer `i + 1`. If all positions are correct, the answer is `n + 1`.

**Python:**

```python
class Solution:
    def firstMissingPositive(self, nums: list[int]) -> int:
        n = len(nums)
        i = 0
        while i < n:
            correct = nums[i] - 1
            if 0 < nums[i] <= n and nums[i] != nums[correct]:
                nums[i], nums[correct] = nums[correct], nums[i]
            else:
                i += 1

        for i in range(n):
            if nums[i] != i + 1:
                return i + 1
        return n + 1
```

**C++:**

```cpp
class Solution {
public:
    int firstMissingPositive(vector<int>& nums) {
        int n = nums.size();
        int i = 0;
        while (i < n) {
            int correct = nums[i] - 1;
            if (nums[i] > 0 && nums[i] <= n && nums[i] != nums[correct]) {
                swap(nums[i], nums[correct]);
            } else {
                i++;
            }
        }

        for (int i = 0; i < n; i++) {
            if (nums[i] != i + 1) return i + 1;
        }
        return n + 1;
    }
};
```

| Complexity | Value |
|---|---|
| Time | O(n) — each element is swapped at most once to its final position |
| Space | O(1) auxiliary |

---
## 6. In-place Linked List Reversal

### Overview

Reversing a linked list in-place means manipulating the existing node pointers rather than creating new nodes. The canonical technique uses three pointers — **prev**, **current**, and **next** — to walk through the list and flip each link:

1. **Save** `next = current.next` (so we don't lose the rest of the list).
2. **Reverse** the link: `current.next = prev`.
3. **Advance**: `prev = current`, `current = next`.

After the loop, `prev` points to the new head.

| Aspect | Value |
|--------|-------|
| **Time** | O(n) — single pass |
| **Space** | O(1) — pointer manipulation only |

This primitive is a building block for dozens of linked list problems: partial reversal, palindrome checking, list reordering, k-group reversal, and rotation.

---

### When to Use

| Signal | Example |
|--------|---------|
| Reverse an entire linked list | LC 206 |
| Reverse a sub-portion between positions `left` and `right` | LC 92 |
| Check if a linked list is a palindrome | LC 234 — reverse second half, compare |
| Reorder a linked list | LC 143 — split, reverse second half, merge alternating |
| Rotate a linked list by k positions | LC 61 — form cycle, break at new tail |

---

### Template Code

#### Full Reversal

**Python**

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head: ListNode) -> ListNode:
    prev, curr = None, head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev
```

**C++**

```cpp
struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x) : val(x), next(nullptr) {}
};

ListNode* reverseList(ListNode* head) {
    ListNode* prev = nullptr;
    ListNode* curr = head;
    while (curr) {
        ListNode* nxt = curr->next;
        curr->next = prev;
        prev = curr;
        curr = nxt;
    }
    return prev;
}
```

#### Partial Reversal (Reverse Between Positions)

**Python**

```python
def reverse_between(head: ListNode, left: int, right: int) -> ListNode:
    dummy = ListNode(0, head)
    before = dummy

    for _ in range(left - 1):
        before = before.next

    prev, curr = None, before.next
    for _ in range(right - left + 1):
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt

    # Reconnect
    before.next.next = curr   # tail of reversed portion -> node after right
    before.next = prev        # node before left -> new head of reversed portion
    return dummy.next
```

**C++**

```cpp
ListNode* reverseBetween(ListNode* head, int left, int right) {
    ListNode dummy(0);
    dummy.next = head;
    ListNode* before = &dummy;

    for (int i = 0; i < left - 1; ++i)
        before = before->next;

    ListNode* prev = nullptr;
    ListNode* curr = before->next;
    for (int i = 0; i < right - left + 1; ++i) {
        ListNode* nxt = curr->next;
        curr->next = prev;
        prev = curr;
        curr = nxt;
    }

    before->next->next = curr;
    before->next = prev;
    return dummy.next;
}
```

---

### Variations

| Variation | Key Idea |
|-----------|----------|
| **Full reversal** | Walk entire list with prev/curr/next |
| **Partial reversal** | Isolate sub-range [left, right]; reverse only that segment; reconnect head and tail of the segment to the surrounding list |
| **Reverse in groups of k** | Count k nodes, reverse them as a batch, recurse/iterate on the remainder; leave a short tail (< k) as-is or reversed depending on the problem |
| **Recursive reversal** | Base case: single node or null → return it as new head. Recursive step: `reverse(head.next)` then `head.next.next = head; head.next = None`. Elegant but O(n) stack space |

---

### Common Mistakes

1. **Losing the next pointer** — Reassigning `curr.next = prev` before saving `nxt = curr.next` orphans the rest of the list.
2. **Off-by-one in partial reversal** — Using 0-indexed vs 1-indexed positions for `left`/`right` causes the reversal window to shift.
3. **Not reconnecting the reversed segment** — After reversing a sub-portion, you must stitch the reversed segment back: `before.next.next = nodeAfterRight` and `before.next = newSubHead`.
4. **Forgetting to return the new head** — After full reversal, `prev` (not `head`) is the new head. With partial reversal inside a dummy-node setup, return `dummy.next`.

---

### Related Patterns

- **Fast & Slow Pointers** — Often used together (find the middle before reversing the second half).
- **Two Pointers** — Used for merging two lists after a reversal step.

---

### Example Problems

---

#### Problem 1 — Reverse Linked List (LC 206) [Easy]

**Link**: [https://leetcode.com/problems/reverse-linked-list/](https://leetcode.com/problems/reverse-linked-list/)

**Problem**: Given the head of a singly linked list, reverse the list and return the reversed list.

**Intuition**: Walk through the list once, flipping each `next` pointer to point backwards. Keep `prev` as the already-reversed portion. When `curr` becomes `None`, `prev` is the new head. An alternative recursive approach reverses the rest of the list first, then fixes up the current node.

**Python (Iterative)**

```python
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev, curr = None, head
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        return prev
```

**Python (Recursive)**

```python
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head
        new_head = self.reverseList(head.next)
        head.next.next = head
        head.next = None
        return new_head
```

**C++ (Iterative)**

```cpp
class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        ListNode* prev = nullptr;
        ListNode* curr = head;
        while (curr) {
            ListNode* nxt = curr->next;
            curr->next = prev;
            prev = curr;
            curr = nxt;
        }
        return prev;
    }
};
```

**C++ (Recursive)**

```cpp
class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        if (!head || !head->next) return head;
        ListNode* newHead = reverseList(head->next);
        head->next->next = head;
        head->next = nullptr;
        return newHead;
    }
};
```

**Complexity**: O(n) time, O(1) space iterative / O(n) space recursive (call stack).

---

#### Problem 2 — Reverse Linked List II (LC 92) [Medium]

**Link**: [https://leetcode.com/problems/reverse-linked-list-ii/](https://leetcode.com/problems/reverse-linked-list-ii/)

**Problem**: Given the head of a singly linked list and two integers `left` and `right` where `left <= right`, reverse the nodes from position `left` to position `right` and return the reversed list. Positions are 1-indexed.

**Intuition**: Use a dummy node to simplify edge cases (reversing from position 1). Walk to the node just before position `left` (`before`). Then perform a standard reversal for `right - left + 1` nodes. After reversing, stitch the reversed segment back: the original first node of the segment (now the tail) points to the node after position `right`, and `before.next` points to the new head of the reversed segment.

**Python**

```python
class Solution:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        before = dummy

        for _ in range(left - 1):
            before = before.next

        prev, curr = None, before.next
        for _ in range(right - left + 1):
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt

        before.next.next = curr
        before.next = prev
        return dummy.next
```

**C++**

```cpp
class Solution {
public:
    ListNode* reverseBetween(ListNode* head, int left, int right) {
        ListNode dummy(0);
        dummy.next = head;
        ListNode* before = &dummy;

        for (int i = 0; i < left - 1; ++i)
            before = before->next;

        ListNode* prev = nullptr;
        ListNode* curr = before->next;
        for (int i = 0; i < right - left + 1; ++i) {
            ListNode* nxt = curr->next;
            curr->next = prev;
            prev = curr;
            curr = nxt;
        }

        before->next->next = curr;
        before->next = prev;
        return dummy.next;
    }
};
```

**Complexity**: O(n) time, O(1) space.

---

#### Problem 3 — Palindrome Linked List (LC 234) [Medium]

**Link**: [https://leetcode.com/problems/palindrome-linked-list/](https://leetcode.com/problems/palindrome-linked-list/)

**Problem**: Given the head of a singly linked list, return `true` if it is a palindrome, or `false` otherwise. Do it in O(n) time and O(1) space.

**Intuition**: A palindrome reads the same forwards and backwards. Use the **fast & slow pointer** technique to find the middle of the list. Reverse the second half in-place. Then compare the first half and the reversed second half node by node. If all values match, it's a palindrome. Optionally restore the list by reversing the second half again.

**Python**

```python
class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        prev = None
        while slow:
            nxt = slow.next
            slow.next = prev
            prev = slow
            slow = nxt

        left, right = head, prev
        while right:
            if left.val != right.val:
                return False
            left = left.next
            right = right.next
        return True
```

**C++**

```cpp
class Solution {
public:
    bool isPalindrome(ListNode* head) {
        ListNode* slow = head;
        ListNode* fast = head;
        while (fast && fast->next) {
            slow = slow->next;
            fast = fast->next->next;
        }

        ListNode* prev = nullptr;
        while (slow) {
            ListNode* nxt = slow->next;
            slow->next = prev;
            prev = slow;
            slow = nxt;
        }

        ListNode* left = head;
        ListNode* right = prev;
        while (right) {
            if (left->val != right->val) return false;
            left = left->next;
            right = right->next;
        }
        return true;
    }
};
```

**Complexity**: O(n) time, O(1) space.

---

#### Problem 4 — Reorder List (LC 143) [Medium]

**Link**: [https://leetcode.com/problems/reorder-list/](https://leetcode.com/problems/reorder-list/)

**Problem**: Given the head of a singly linked list `L0 → L1 → … → Ln-1 → Ln`, reorder it to `L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → …`. You may not modify the values in the list's nodes — only the nodes themselves may be changed.

**Intuition**: Three steps:

1. **Find the middle** using fast & slow pointers.
2. **Reverse the second half** in-place.
3. **Merge** the two halves by alternating nodes from the first half and the reversed second half.

**Python**

```python
class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        if not head or not head.next:
            return

        slow, fast = head, head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next

        second = slow.next
        slow.next = None

        prev = None
        while second:
            nxt = second.next
            second.next = prev
            prev = second
            second = nxt
        second = prev

        first = head
        while second:
            tmp1, tmp2 = first.next, second.next
            first.next = second
            second.next = tmp1
            first = tmp1
            second = tmp2
```

**C++**

```cpp
class Solution {
public:
    void reorderList(ListNode* head) {
        if (!head || !head->next) return;

        ListNode* slow = head;
        ListNode* fast = head;
        while (fast->next && fast->next->next) {
            slow = slow->next;
            fast = fast->next->next;
        }

        ListNode* second = slow->next;
        slow->next = nullptr;

        ListNode* prev = nullptr;
        while (second) {
            ListNode* nxt = second->next;
            second->next = prev;
            prev = second;
            second = nxt;
        }
        second = prev;

        ListNode* first = head;
        while (second) {
            ListNode* tmp1 = first->next;
            ListNode* tmp2 = second->next;
            first->next = second;
            second->next = tmp1;
            first = tmp1;
            second = tmp2;
        }
    }
};
```

**Complexity**: O(n) time, O(1) space.

---

#### Problem 5 — Reverse Nodes in k-Group (LC 25) [Hard]

**Link**: [https://leetcode.com/problems/reverse-nodes-in-k-group/](https://leetcode.com/problems/reverse-nodes-in-k-group/)

**Problem**: Given the head of a linked list, reverse the nodes of the list `k` at a time and return the modified list. `k` is a positive integer less than or equal to the length of the linked list. If the number of nodes is not a multiple of `k`, the remaining nodes at the end should stay as they are. You may not alter the values of the nodes — only the nodes themselves may be changed.

**Intuition**: Process the list in chunks of `k`:

1. **Count** ahead to check that at least `k` nodes remain. If fewer remain, stop.
2. **Reverse** the next `k` nodes using the standard three-pointer technique.
3. **Reconnect**: the tail of the previously reversed group points to the new head of the just-reversed group. The tail of the just-reversed group (originally its head) will be connected to the next group in the following iteration.
4. **Repeat** until fewer than `k` nodes remain.

A dummy node simplifies reconnection at the head of the list.

**Python**

```python
class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        group_prev = dummy

        while True:
            kth = group_prev
            for _ in range(k):
                kth = kth.next
                if not kth:
                    return dummy.next

            group_next = kth.next
            prev, curr = kth.next, group_prev.next
            for _ in range(k):
                nxt = curr.next
                curr.next = prev
                prev = curr
                curr = nxt

            tmp = group_prev.next
            group_prev.next = prev
            group_prev = tmp
```

**C++**

```cpp
class Solution {
public:
    ListNode* reverseKGroup(ListNode* head, int k) {
        ListNode dummy(0);
        dummy.next = head;
        ListNode* groupPrev = &dummy;

        while (true) {
            ListNode* kth = groupPrev;
            for (int i = 0; i < k; ++i) {
                kth = kth->next;
                if (!kth) return dummy.next;
            }

            ListNode* groupNext = kth->next;
            ListNode* prev = groupNext;
            ListNode* curr = groupPrev->next;
            for (int i = 0; i < k; ++i) {
                ListNode* nxt = curr->next;
                curr->next = prev;
                prev = curr;
                curr = nxt;
            }

            ListNode* tmp = groupPrev->next;
            groupPrev->next = prev;
            groupPrev = tmp;
        }
    }
};
```

**Complexity**: O(n) time, O(1) space.

---
## 7. BFS (Breadth-First Search)

### Overview

BFS explores nodes **level by level** using a queue (FIFO). For trees this is called **level-order traversal**: visit every node at depth *d* before any node at depth *d + 1*. For graphs BFS guarantees the **shortest path in unweighted graphs** because it naturally discovers nodes in increasing order of distance from the source. The algorithm processes all nodes at the current depth before moving deeper, making it ideal for "minimum steps" and "nearest" problems.

### When to Use

| Signal | Example |
|---|---|
| Level-order traversal | Print tree level by level |
| Shortest path in unweighted graph | Word Ladder, Shortest Bridge |
| Minimum steps / moves | Rotting Oranges, Jump Game |
| Finding connected components | Number of Provinces |
| Multi-source BFS | 01-Matrix, Walls and Gates |
| Expanding frontier uniformly | Surrounded Regions |

### Template Code

#### Tree BFS (Level-Order Traversal)

**Python**

```python
from collections import deque
from typing import List, Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def level_order(root: Optional[TreeNode]) -> List[List[int]]:
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level_size = len(queue)
        level = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result
```

**C++**

```cpp
#include <vector>
#include <queue>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

vector<vector<int>> levelOrder(TreeNode* root) {
    vector<vector<int>> result;
    if (!root) return result;
    queue<TreeNode*> q;
    q.push(root);
    while (!q.empty()) {
        int levelSize = q.size();
        vector<int> level;
        for (int i = 0; i < levelSize; ++i) {
            TreeNode* node = q.front();
            q.pop();
            level.push_back(node->val);
            if (node->left)  q.push(node->left);
            if (node->right) q.push(node->right);
        }
        result.push_back(level);
    }
    return result;
}
```

#### Graph BFS (Shortest Path in Unweighted Graph)

**Python**

```python
from collections import deque
from typing import List

def bfs_graph(graph: List[List[int]], start: int, target: int) -> int:
    """Return shortest distance from start to target (-1 if unreachable)."""
    n = len(graph)
    visited = [False] * n
    visited[start] = True
    queue = deque([(start, 0)])  # (node, distance)
    while queue:
        node, dist = queue.popleft()
        if node == target:
            return dist
        for neighbor in graph[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append((neighbor, dist + 1))
    return -1
```

**C++**

```cpp
#include <vector>
#include <queue>
using namespace std;

int bfsGraph(vector<vector<int>>& graph, int start, int target) {
    int n = graph.size();
    vector<bool> visited(n, false);
    visited[start] = true;
    queue<pair<int,int>> q;  // {node, distance}
    q.push({start, 0});
    while (!q.empty()) {
        auto [node, dist] = q.front();
        q.pop();
        if (node == target) return dist;
        for (int nei : graph[node]) {
            if (!visited[nei]) {
                visited[nei] = true;
                q.push({nei, dist + 1});
            }
        }
    }
    return -1;
}
```

### Variations

| Variation | Key Idea |
|---|---|
| **Standard level-order** | Process each level with `for _ in range(len(queue))` |
| **Zigzag level-order** | Alternate appending to front/back of level list |
| **Right side view** | Take the last node of each level |
| **Shortest path (unweighted)** | BFS distance equals number of edges |
| **Multi-source BFS** | Seed the queue with *all* sources at once (e.g., all rotten oranges) |
| **0-1 BFS** | Edge weights 0 or 1: deque, push 0-edges to the front ([Pattern 27](#27-weighted-shortest-path-patterns)) |
| **State-space BFS** | Vertex = `(position, extra state)` such as a visited bitmask or remaining budget ([Pattern 27](#27-weighted-shortest-path-patterns)) |
| **Bidirectional BFS** | Search from start and goal, expand the smaller frontier ([Pattern 33](#33-meet-in-the-middle--bidirectional-bfs)) |
| **Weighted edges** | BFS no longer gives shortest paths; use Dijkstra or Bellman-Ford ([Pattern 27](#27-weighted-shortest-path-patterns)) |

### Common Mistakes

1. **Not tracking visited nodes** — causes infinite loops in graphs with cycles. Always mark a node visited *when you enqueue it*, not when you dequeue it.
2. **Confusing level boundaries** — forget to snapshot `len(queue)` at the start of each level, so nodes from different levels mix together.
3. **Not using `len(queue)` for level-size processing** — iterating `while queue` inside the level loop consumes future levels.
4. **Revisiting nodes in grid BFS** — mark cells visited immediately upon adding to the queue, not upon popping.

### Related Patterns

- **DFS** — alternative traversal strategy; often interchangeable for reachability but not for shortest path.
- **Topological Sort** — BFS variant (Kahn's algorithm) using in-degree counting.

---

### Example Problems

### Problem 1 — Binary Tree Level Order Traversal (LC 102) [Easy]

**Link:** [https://leetcode.com/problems/binary-tree-level-order-traversal/](https://leetcode.com/problems/binary-tree-level-order-traversal/)

**Problem Statement:** Given the root of a binary tree, return the level order traversal of its nodes' values (i.e., from left to right, level by level).

**Intuition:** This is the textbook BFS application on a tree. Use a queue and process one full level per iteration by capturing the queue length at the start. Collect each level into a sub-list.

**Python Solution**

```python
from collections import deque
from typing import List, Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        result = []
        queue = deque([root])
        while queue:
            level_size = len(queue)
            level = []
            for _ in range(level_size):
                node = queue.popleft()
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            result.append(level)
        return result
```

**C++ Solution**

```cpp
#include <vector>
#include <queue>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Solution {
public:
    vector<vector<int>> levelOrder(TreeNode* root) {
        vector<vector<int>> result;
        if (!root) return result;
        queue<TreeNode*> q;
        q.push(root);
        while (!q.empty()) {
            int size = q.size();
            vector<int> level;
            for (int i = 0; i < size; ++i) {
                TreeNode* node = q.front();
                q.pop();
                level.push_back(node->val);
                if (node->left)  q.push(node->left);
                if (node->right) q.push(node->right);
            }
            result.push_back(level);
        }
        return result;
    }
};
```

**Complexity:** Time O(n) — every node visited once. Space O(n) — queue holds at most one full level (up to n/2 nodes in a complete tree).

---

### Problem 2 — Binary Tree Zigzag Level Order Traversal (LC 103) [Medium]

**Link:** [https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/](https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/)

**Problem Statement:** Given the root of a binary tree, return the zigzag level order traversal of its nodes' values. (i.e., first level left-to-right, next level right-to-left, alternating.)

**Intuition:** Perform standard BFS level-order traversal. After collecting each level, reverse the list for odd-numbered levels (0-indexed). Alternatively, use a deque for the level list and append left or right depending on the direction flag.

**Python Solution**

```python
from collections import deque
from typing import List, Optional

class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        result = []
        queue = deque([root])
        left_to_right = True
        while queue:
            level_size = len(queue)
            level = deque()
            for _ in range(level_size):
                node = queue.popleft()
                if left_to_right:
                    level.append(node.val)
                else:
                    level.appendleft(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            result.append(list(level))
            left_to_right = not left_to_right
        return result
```

**C++ Solution**

```cpp
#include <vector>
#include <queue>
#include <deque>
#include <algorithm>
using namespace std;

class Solution {
public:
    vector<vector<int>> zigzagLevelOrder(TreeNode* root) {
        vector<vector<int>> result;
        if (!root) return result;
        queue<TreeNode*> q;
        q.push(root);
        bool leftToRight = true;
        while (!q.empty()) {
            int size = q.size();
            deque<int> level;
            for (int i = 0; i < size; ++i) {
                TreeNode* node = q.front();
                q.pop();
                if (leftToRight)
                    level.push_back(node->val);
                else
                    level.push_front(node->val);
                if (node->left)  q.push(node->left);
                if (node->right) q.push(node->right);
            }
            result.push_back(vector<int>(level.begin(), level.end()));
            leftToRight = !leftToRight;
        }
        return result;
    }
};
```

**Complexity:** Time O(n). Space O(n).

---

### Problem 3 — Rotting Oranges (LC 994) [Medium]

**Link:** [https://leetcode.com/problems/rotting-oranges/](https://leetcode.com/problems/rotting-oranges/)

**Problem Statement:** You are given an `m x n` grid where each cell can have one of three values: `0` (empty), `1` (fresh orange), `2` (rotten orange). Every minute, any fresh orange 4-directionally adjacent to a rotten orange becomes rotten. Return the minimum number of minutes until no fresh orange remains. If impossible, return `-1`.

**Intuition:** This is **multi-source BFS**. Seed the queue with *all* initially rotten oranges. Each BFS level represents one minute. After BFS completes, if any fresh orange remains the answer is `-1`; otherwise return the number of levels processed.

**Python Solution**

```python
from collections import deque
from typing import List

class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        queue = deque()
        fresh = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 2:
                    queue.append((r, c))
                elif grid[r][c] == 1:
                    fresh += 1
        if fresh == 0:
            return 0
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        minutes = 0
        while queue and fresh > 0:
            minutes += 1
            for _ in range(len(queue)):
                r, c = queue.popleft()
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                        grid[nr][nc] = 2
                        fresh -= 1
                        queue.append((nr, nc))
        return minutes if fresh == 0 else -1
```

**C++ Solution**

```cpp
#include <vector>
#include <queue>
using namespace std;

class Solution {
public:
    int orangesRotting(vector<vector<int>>& grid) {
        int rows = grid.size(), cols = grid[0].size();
        queue<pair<int,int>> q;
        int fresh = 0;
        for (int r = 0; r < rows; ++r)
            for (int c = 0; c < cols; ++c) {
                if (grid[r][c] == 2) q.push({r, c});
                else if (grid[r][c] == 1) ++fresh;
            }
        if (fresh == 0) return 0;
        int dirs[4][2] = {{0,1},{0,-1},{1,0},{-1,0}};
        int minutes = 0;
        while (!q.empty() && fresh > 0) {
            ++minutes;
            int size = q.size();
            for (int i = 0; i < size; ++i) {
                auto [r, c] = q.front();
                q.pop();
                for (auto& d : dirs) {
                    int nr = r + d[0], nc = c + d[1];
                    if (nr >= 0 && nr < rows && nc >= 0 && nc < cols
                        && grid[nr][nc] == 1) {
                        grid[nr][nc] = 2;
                        --fresh;
                        q.push({nr, nc});
                    }
                }
            }
        }
        return fresh == 0 ? minutes : -1;
    }
};
```

**Complexity:** Time O(m * n) — each cell enqueued at most once. Space O(m * n) — queue size.

---

### Problem 4 — Word Ladder (LC 127) [Medium]

**Link:** [https://leetcode.com/problems/word-ladder/](https://leetcode.com/problems/word-ladder/)

**Problem Statement:** Given two words `beginWord` and `endWord`, and a word list, return the number of words in the shortest transformation sequence from `beginWord` to `endWord` (each step changes exactly one letter and the intermediate word must exist in the word list). Return `0` if no such sequence exists.

**Intuition:** Model each word as a node. Two nodes share an edge if they differ by exactly one character. BFS from `beginWord` finds the shortest path. To efficiently find neighbors, use generic states: for the word "hot", the generic states are `*ot`, `h*t`, `ho*`. Pre-build a map from generic state to all matching words, then BFS over this implicit graph.

**Python Solution**

```python
from collections import deque, defaultdict
from typing import List

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        word_set = set(wordList)
        if endWord not in word_set:
            return 0
        L = len(beginWord)
        # Build adjacency via generic patterns
        pattern_map = defaultdict(list)
        for word in word_set:
            for i in range(L):
                pattern = word[:i] + '*' + word[i+1:]
                pattern_map[pattern].append(word)

        visited = {beginWord}
        queue = deque([(beginWord, 1)])
        while queue:
            word, length = queue.popleft()
            for i in range(L):
                pattern = word[:i] + '*' + word[i+1:]
                for neighbor in pattern_map[pattern]:
                    if neighbor == endWord:
                        return length + 1
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, length + 1))
                pattern_map[pattern] = []  # clear to avoid revisits
        return 0
```

**C++ Solution**

```cpp
#include <string>
#include <vector>
#include <queue>
#include <unordered_set>
#include <unordered_map>
using namespace std;

class Solution {
public:
    int ladderLength(string beginWord, string endWord, vector<string>& wordList) {
        unordered_set<string> wordSet(wordList.begin(), wordList.end());
        if (wordSet.find(endWord) == wordSet.end()) return 0;

        int L = beginWord.size();
        unordered_map<string, vector<string>> patternMap;
        for (const string& word : wordSet) {
            for (int i = 0; i < L; ++i) {
                string pattern = word.substr(0, i) + '*' + word.substr(i + 1);
                patternMap[pattern].push_back(word);
            }
        }

        unordered_set<string> visited;
        visited.insert(beginWord);
        queue<pair<string, int>> q;
        q.push({beginWord, 1});

        while (!q.empty()) {
            auto [word, length] = q.front();
            q.pop();
            for (int i = 0; i < L; ++i) {
                string pattern = word.substr(0, i) + '*' + word.substr(i + 1);
                for (const string& neighbor : patternMap[pattern]) {
                    if (neighbor == endWord) return length + 1;
                    if (visited.find(neighbor) == visited.end()) {
                        visited.insert(neighbor);
                        q.push({neighbor, length + 1});
                    }
                }
                patternMap[pattern].clear();
            }
        }
        return 0;
    }
};
```

**Complexity:** Time O(M² * N) where M is word length and N is the number of words — building the pattern map is O(M * N) and each BFS step checks M patterns. Space O(M² * N) for the pattern map.

**Follow-up:** "Can you make it faster?" The standard answer is **bidirectional BFS**: search from both `beginWord` and `endWord` and always expand the smaller frontier, which cuts the explored states from about `b^d` to `2 · b^(d/2)`. Full solution and analysis: [Pattern 33, Word Ladder](#problem-1-word-ladder-lc-127--hard-bidirectional).

---

### Problem 5 — Shortest Path in Binary Matrix (LC 1091) [Hard]

**Link:** [https://leetcode.com/problems/shortest-path-in-binary-matrix/](https://leetcode.com/problems/shortest-path-in-binary-matrix/)

**Problem Statement:** Given an `n x n` binary matrix `grid`, return the length of the shortest clear path from top-left `(0,0)` to bottom-right `(n-1,n-1)`. A clear path consists of cells with value `0`, and you may move in 8 directions. Return `-1` if no such path exists.

**Intuition:** Standard BFS on a grid with 8-directional movement. Start from `(0,0)`, enqueue neighbors that are `0` and unvisited. The first time we reach `(n-1,n-1)` gives the shortest path length. Mark cells visited by setting them to `1`.

**Python Solution**

```python
from collections import deque
from typing import List

class Solution:
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        n = len(grid)
        if grid[0][0] != 0 or grid[n-1][n-1] != 0:
            return -1
        directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        queue = deque([(0, 0, 1)])  # (row, col, path_length)
        grid[0][0] = 1  # mark visited
        while queue:
            r, c, dist = queue.popleft()
            if r == n - 1 and c == n - 1:
                return dist
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                    grid[nr][nc] = 1
                    queue.append((nr, nc, dist + 1))
        return -1
```

**C++ Solution**

```cpp
#include <vector>
#include <queue>
using namespace std;

class Solution {
public:
    int shortestPathBinaryMatrix(vector<vector<int>>& grid) {
        int n = grid.size();
        if (grid[0][0] != 0 || grid[n-1][n-1] != 0) return -1;
        int dirs[8][2] = {{-1,-1},{-1,0},{-1,1},{0,-1},{0,1},{1,-1},{1,0},{1,1}};
        queue<tuple<int,int,int>> q;
        q.push({0, 0, 1});
        grid[0][0] = 1;
        while (!q.empty()) {
            auto [r, c, dist] = q.front();
            q.pop();
            if (r == n - 1 && c == n - 1) return dist;
            for (auto& d : dirs) {
                int nr = r + d[0], nc = c + d[1];
                if (nr >= 0 && nr < n && nc >= 0 && nc < n && grid[nr][nc] == 0) {
                    grid[nr][nc] = 1;
                    q.push({nr, nc, dist + 1});
                }
            }
        }
        return -1;
    }
};
```

**Complexity:** Time O(n²) — each cell visited at most once. Space O(n²) — queue size in the worst case.

---

## 8. DFS (Depth-First Search)

### Overview

DFS explores as **deep as possible** along each branch before **backtracking**. It can be implemented recursively (using the call stack) or iteratively (with an explicit stack). For trees, DFS yields three classic traversals — **preorder** (root-left-right), **inorder** (left-root-right), and **postorder** (left-right-root). For graphs, DFS is the backbone for detecting cycles, computing connected components, topological ordering, and exploring all paths.

### When to Use

| Signal | Example |
|---|---|
| Tree traversals (pre/in/postorder) | Serialize tree, validate BST |
| Path finding / all paths | Root-to-leaf paths |
| Detecting cycles | Course Schedule |
| Connected components | Number of Islands |
| Flood fill | Surrounded Regions |
| Generating all combinations/paths | Subsets, Permutations |
| Problems needing post-order aggregation | Diameter, Max Path Sum |

### Template Code

#### Tree DFS (Recursive)

**Python**

```python
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def dfs_preorder(root: Optional[TreeNode]) -> None:
    if not root:
        return
    # process root
    print(root.val)
    dfs_preorder(root.left)
    dfs_preorder(root.right)

def dfs_inorder(root: Optional[TreeNode]) -> None:
    if not root:
        return
    dfs_inorder(root.left)
    print(root.val)       # process root
    dfs_inorder(root.right)

def dfs_postorder(root: Optional[TreeNode]) -> None:
    if not root:
        return
    dfs_postorder(root.left)
    dfs_postorder(root.right)
    print(root.val)       # process root
```

**C++**

```cpp
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

void dfsPreorder(TreeNode* root) {
    if (!root) return;
    // process root
    dfsPreorder(root->left);
    dfsPreorder(root->right);
}

void dfsInorder(TreeNode* root) {
    if (!root) return;
    dfsInorder(root->left);
    // process root
    dfsInorder(root->right);
}

void dfsPostorder(TreeNode* root) {
    if (!root) return;
    dfsPostorder(root->left);
    dfsPostorder(root->right);
    // process root
}
```

#### Iterative Tree Traversals (Explicit Stack)

Interviewers often ask for traversals "without recursion", either to avoid stack overflow on skewed trees (depth up to `n`) or to build an iterator that can pause between elements (BST Iterator, Kth Smallest).

- **Preorder**: pop a node, visit it, push **right then left** so left is processed first.
- **Inorder**: walk left pushing ancestors; pop, visit, then move to the right child. The stack always holds the nodes whose left subtree is in progress.
- **Postorder**: like inorder, but a node is visited only when its right subtree is finished. Track the last visited node to tell whether you are coming back from the right child. (Shortcut: a preorder with **left then right** pushed, i.e. root-right-left order, reversed at the end, is postorder.)

**Python**

```python
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def preorder_iterative(root: Optional[TreeNode]) -> list[int]:
    out, stack = [], [root] if root else []
    while stack:
        node = stack.pop()
        out.append(node.val)
        if node.right:
            stack.append(node.right)     # pushed first, processed last
        if node.left:
            stack.append(node.left)
    return out

def inorder_iterative(root: Optional[TreeNode]) -> list[int]:
    out, stack, node = [], [], root
    while stack or node:
        while node:                      # go as far left as possible
            stack.append(node)
            node = node.left
        node = stack.pop()               # leftmost unvisited node
        out.append(node.val)
        node = node.right                # then its right subtree
    return out

def postorder_iterative(root: Optional[TreeNode]) -> list[int]:
    out, stack, node, last = [], [], root, None
    while stack or node:
        if node:
            stack.append(node)
            node = node.left
        else:
            top = stack[-1]
            if top.right and last is not top.right:
                node = top.right         # right subtree not done yet
            else:
                out.append(top.val)      # both subtrees done
                last = stack.pop()
    return out

#        4
#      /   \
#     2     6
#    / \   /
#   1   3 5
t = TreeNode(4, TreeNode(2, TreeNode(1), TreeNode(3)), TreeNode(6, TreeNode(5)))
assert preorder_iterative(t) == [4, 2, 1, 3, 6, 5]
assert inorder_iterative(t) == [1, 2, 3, 4, 5, 6]
assert postorder_iterative(t) == [1, 3, 2, 5, 6, 4]
```

**C++**

```cpp
#include <cassert>
#include <stack>
#include <vector>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

vector<int> inorderIterative(TreeNode* root) {
    vector<int> out;
    stack<TreeNode*> st;
    TreeNode* node = root;
    while (node || !st.empty()) {
        while (node) {
            st.push(node);
            node = node->left;
        }
        node = st.top();
        st.pop();
        out.push_back(node->val);
        node = node->right;
    }
    return out;
}

vector<int> postorderIterative(TreeNode* root) {
    vector<int> out;
    stack<TreeNode*> st;
    TreeNode* node = root;
    TreeNode* last = nullptr;
    while (node || !st.empty()) {
        if (node) {
            st.push(node);
            node = node->left;
        } else {
            TreeNode* top = st.top();
            if (top->right && last != top->right) {
                node = top->right;
            } else {
                out.push_back(top->val);
                last = top;
                st.pop();
            }
        }
    }
    return out;
}

int main() {
    TreeNode n1(1), n3(3), n5(5), n2(2, &n1, &n3), n6(6, &n5), root(4, &n2, &n6);
    assert((inorderIterative(&root) == vector<int>{1, 2, 3, 4, 5, 6}));
    assert((postorderIterative(&root) == vector<int>{1, 3, 2, 5, 6, 4}));
}
```

#### Graph DFS (with Visited Set)

**Python**

```python
from typing import List

def dfs_graph(graph: List[List[int]], start: int) -> List[int]:
    """Return all nodes reachable from start."""
    visited = set()
    result = []

    def dfs(node: int) -> None:
        visited.add(node)
        result.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)

    dfs(start)
    return result
```

**C++**

```cpp
#include <vector>
using namespace std;

class GraphDFS {
    vector<vector<int>>& graph;
    vector<bool> visited;
    vector<int> result;

    void dfs(int node) {
        visited[node] = true;
        result.push_back(node);
        for (int nei : graph[node]) {
            if (!visited[nei]) {
                dfs(nei);
            }
        }
    }

public:
    vector<int> reachable(vector<vector<int>>& g, int start) {
        graph = g;
        visited.assign(g.size(), false);
        result.clear();
        dfs(start);
        return result;
    }
};
```

### Variations

| Variation | Key Idea |
|---|---|
| **Preorder** | Process node before children — useful for copying/serializing |
| **Inorder** | Process node between children — yields sorted order in BSTs |
| **Postorder** | Process node after children — useful for computing subtree properties |
| **Iterative DFS** | Use an explicit stack instead of recursion to avoid stack overflow |
| **Graph DFS with visited** | Track visited set to handle cycles and prevent infinite recursion |
| **Bounds passed down** | Each call receives the open interval its subtree must lie in (Validate BST, Recover BST, BST from preorder) |
| **Return a summary up** | Post-order returns a small tuple (height, best-through-node, rob/skip) and updates a global answer (Diameter, Max Path Sum, House Robber III) |
| **Search returning a node** | Return the found node or `None`; the first node receiving non-null from both sides is the answer (LCA) |
| **Divide by index map** | Recursive construction from traversal arrays using a value → inorder-index map (Construct from Preorder + Inorder) |
| **Discovery time / low-link** | Record DFS entry time and the earliest reachable time via back edges to find bridges, articulation points and SCCs (Tarjan) |
| **Morris traversal** | Temporarily thread right pointers to predecessors for O(1)-space inorder |

### Common Mistakes

1. **Stack overflow on deep recursion** — for very deep trees or large graphs, switch to iterative DFS with an explicit stack or increase the recursion limit.
2. **Not marking visited before recursive call (graph)** — leads to infinite loops in cyclic graphs. Mark a node visited *before* recursing into its neighbors.
3. **Not handling base cases properly** — forgetting `if not root: return` causes `NoneType` errors.
4. **Modifying shared state incorrectly during backtracking** — when building paths, remember to pop from the path after returning from a recursive call; failing to do so corrupts results for sibling branches.

### Related Patterns

- **BFS** — alternative traversal; preferred for shortest-path in unweighted graphs.
- **Backtracking** — DFS + pruning; used for constraint-satisfaction and combinatorial problems.
- **Topological Sort** — DFS-based post-order on DAGs.

---

### Example Problems

### Problem 1 — Maximum Depth of Binary Tree (LC 104) [Easy]

**Link:** [https://leetcode.com/problems/maximum-depth-of-binary-tree/](https://leetcode.com/problems/maximum-depth-of-binary-tree/)

**Problem Statement:** Given the root of a binary tree, return its maximum depth. Maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

**Intuition:** Classic recursive DFS. The depth of a tree is `1 + max(depth(left), depth(right))`. Base case: a null node has depth 0.

**Python Solution**

```python
from typing import Optional

class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
```

**C++ Solution**

```cpp
class Solution {
public:
    int maxDepth(TreeNode* root) {
        if (!root) return 0;
        return 1 + max(maxDepth(root->left), maxDepth(root->right));
    }
};
```

**Complexity:** Time O(n) — visit every node. Space O(h) — recursion stack where h is tree height (O(n) worst case for a skewed tree).

---

### Problem 2 — Invert Binary Tree (LC 226) [Easy]

**Link:** [https://leetcode.com/problems/invert-binary-tree/](https://leetcode.com/problems/invert-binary-tree/)

**Problem Statement:** Given the root of a binary tree, invert the tree (mirror it) and return its root.

**Intuition:** DFS: at each node, swap its left and right children, then recursively invert each subtree. This is a preorder traversal where the "processing" step is swapping children.

**Python Solution**

```python
from typing import Optional

class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None
        root.left, root.right = root.right, root.left
        self.invertTree(root.left)
        self.invertTree(root.right)
        return root
```

**C++ Solution**

```cpp
class Solution {
public:
    TreeNode* invertTree(TreeNode* root) {
        if (!root) return nullptr;
        swap(root->left, root->right);
        invertTree(root->left);
        invertTree(root->right);
        return root;
    }
};
```

**Complexity:** Time O(n). Space O(h) recursion stack.

---

### Problem 3 — Number of Islands (LC 200) [Medium]

**Link:** [https://leetcode.com/problems/number-of-islands/](https://leetcode.com/problems/number-of-islands/)

**Problem Statement:** Given an `m x n` 2D grid of `'1'`s (land) and `'0'`s (water), return the number of islands. An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.

**Intuition:** Iterate through every cell. When we find an unvisited `'1'`, increment the island count and launch a DFS/BFS to mark all connected land cells as visited (sink them to `'0'`). Each DFS flood-fills one complete island.

**Python Solution**

```python
from typing import List

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid:
            return 0
        rows, cols = len(grid), len(grid[0])
        count = 0

        def dfs(r: int, c: int) -> None:
            if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
                return
            grid[r][c] = '0'  # mark visited
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1':
                    count += 1
                    dfs(r, c)
        return count
```

**C++ Solution**

```cpp
#include <vector>
using namespace std;

class Solution {
    int rows, cols;
    void dfs(vector<vector<char>>& grid, int r, int c) {
        if (r < 0 || r >= rows || c < 0 || c >= cols || grid[r][c] != '1')
            return;
        grid[r][c] = '0';
        dfs(grid, r + 1, c);
        dfs(grid, r - 1, c);
        dfs(grid, r, c + 1);
        dfs(grid, r, c - 1);
    }
public:
    int numIslands(vector<vector<char>>& grid) {
        if (grid.empty()) return 0;
        rows = grid.size();
        cols = grid[0].size();
        int count = 0;
        for (int r = 0; r < rows; ++r)
            for (int c = 0; c < cols; ++c)
                if (grid[r][c] == '1') {
                    ++count;
                    dfs(grid, r, c);
                }
        return count;
    }
};
```

**Complexity:** Time O(m * n) — each cell visited at most once. Space O(m * n) — recursion stack in worst case (all land).

---

### Problem 4 — Path Sum II (LC 113) [Medium]

**Link:** [https://leetcode.com/problems/path-sum-ii/](https://leetcode.com/problems/path-sum-ii/)

**Problem Statement:** Given the root of a binary tree and an integer `targetSum`, return all root-to-leaf paths where the sum of the node values equals `targetSum`. Each path should be returned as a list of node values.

**Intuition:** DFS with path tracking (backtracking). Maintain a running path list. At each node, add its value to the path and subtract from the remaining sum. When we reach a leaf and the remaining sum equals the leaf's value, record a copy of the current path. After processing both children, pop the last element (backtrack).

**Python Solution**

```python
from typing import List, Optional

class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        result = []

        def dfs(node: Optional[TreeNode], remaining: int, path: List[int]) -> None:
            if not node:
                return
            path.append(node.val)
            if not node.left and not node.right and remaining == node.val:
                result.append(list(path))
            else:
                dfs(node.left, remaining - node.val, path)
                dfs(node.right, remaining - node.val, path)
            path.pop()  # backtrack

        dfs(root, targetSum, [])
        return result
```

**C++ Solution**

```cpp
#include <vector>
using namespace std;

class Solution {
    vector<vector<int>> result;
    vector<int> path;

    void dfs(TreeNode* node, int remaining) {
        if (!node) return;
        path.push_back(node->val);
        if (!node->left && !node->right && remaining == node->val) {
            result.push_back(path);
        } else {
            dfs(node->left, remaining - node->val);
            dfs(node->right, remaining - node->val);
        }
        path.pop_back();  // backtrack
    }

public:
    vector<vector<int>> pathSum(TreeNode* root, int targetSum) {
        result.clear();
        path.clear();
        dfs(root, targetSum);
        return result;
    }
};
```

**Complexity:** Time O(n²) — visit every node and copying a path takes O(n) in the worst case. Space O(n) — recursion depth + path storage.

---

### Problem 5 — Binary Tree Maximum Path Sum (LC 124) [Hard]

**Link:** [https://leetcode.com/problems/binary-tree-maximum-path-sum/](https://leetcode.com/problems/binary-tree-maximum-path-sum/)

**Problem Statement:** A path in a binary tree is a sequence of nodes where each pair of adjacent nodes has an edge. The path does not need to pass through the root. Given the root, return the maximum path sum of any non-empty path.

**Intuition:** Use **post-order DFS**. At each node, compute the maximum "gain" that the node can contribute to a path passing through its parent: `node.val + max(left_gain, right_gain, 0)` (we take at most one child branch going upward). Meanwhile, consider the path that *bends* through this node: `node.val + left_gain + right_gain` — update the global maximum with this value. The key insight is separating the value we *return* to the parent (single branch) from the value we *record* (full path through current node).

**Python Solution**

```python
from typing import Optional

class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        self.max_sum = float('-inf')

        def gain(node: Optional[TreeNode]) -> int:
            if not node:
                return 0
            left = max(gain(node.left), 0)
            right = max(gain(node.right), 0)
            # Path through this node as the "bend" point
            self.max_sum = max(self.max_sum, node.val + left + right)
            # Return the max gain if we continue upward (only one branch)
            return node.val + max(left, right)

        gain(root)
        return self.max_sum
```

**C++ Solution**

```cpp
#include <algorithm>
#include <climits>
using namespace std;

class Solution {
    int maxSum;

    int gain(TreeNode* node) {
        if (!node) return 0;
        int left = max(gain(node->left), 0);
        int right = max(gain(node->right), 0);
        maxSum = max(maxSum, node->val + left + right);
        return node->val + max(left, right);
    }

public:
    int maxPathSum(TreeNode* root) {
        maxSum = INT_MIN;
        gain(root);
        return maxSum;
    }
};
```

**Complexity:** Time O(n) — visit every node once. Space O(h) — recursion stack depth, where h is tree height.

---

### Problem 6 — Validate Binary Search Tree (LC 98) [Medium]

**Link:** [https://leetcode.com/problems/validate-binary-search-tree/](https://leetcode.com/problems/validate-binary-search-tree/)

**Problem Statement:** Return `true` if every node's left subtree holds only smaller values and its right subtree only larger values (strictly), recursively.

**Intuition:** Checking only `left.val < node.val < right.val` is the classic wrong answer: in `5 → (left 4, right 6 → (left 3, right 7))`, every parent–child pair is fine, but 3 sits in the right subtree of 5. The constraint is **inherited**: pass down the open interval `(low, high)` that the subtree must fit in. Going left tightens `high` to `node.val`; going right tightens `low`. (Equivalent: an inorder traversal must be strictly increasing.)

**Python Solution**

```python
from typing import Optional

class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def valid(node: Optional[TreeNode], low: float, high: float) -> bool:
            if not node:
                return True
            if not (low < node.val < high):
                return False
            return valid(node.left, low, node.val) and valid(node.right, node.val, high)

        return valid(root, float('-inf'), float('inf'))
```

**C++ Solution**

```cpp
#include <climits>

class Solution {
    // long long bounds: node values span the full int range, so INT_MIN/INT_MAX can't be sentinels
    bool valid(TreeNode* node, long long low, long long high) {
        if (!node) return true;
        if (node->val <= low || node->val >= high) return false;
        return valid(node->left, low, node->val) && valid(node->right, node->val, high);
    }

public:
    bool isValidBST(TreeNode* root) { return valid(root, LLONG_MIN, LLONG_MAX); }
};
```

**Complexity:** Time O(n). Space O(h).

---

### Problem 7 — Lowest Common Ancestor of a Binary Tree (LC 236) [Medium]

**Link:** [https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/)

**Problem Statement:** Given two nodes `p` and `q` that both exist in the tree, return their lowest common ancestor (a node may be its own ancestor).

**Intuition:** Define `lca(node)` = "`p` or `q` or their LCA if found in this subtree, else `None`". If `node` is `p` or `q`, return it: either the other target is below it (so `node` is the LCA) or it is elsewhere (and an ancestor will combine the results). Otherwise recurse. If **both** sides return non-null, `p` and `q` are split across `node`, so `node` is the LCA. If only one side is non-null, pass it up.

**Python Solution**

```python
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if root is None or root is p or root is q:
            return root
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if left and right:
            return root              # p and q are in different subtrees
        return left or right         # both in one subtree (or neither here)
```

**C++ Solution**

```cpp
class Solution {
public:
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        if (!root || root == p || root == q) return root;
        TreeNode* left = lowestCommonAncestor(root->left, p, q);
        TreeNode* right = lowestCommonAncestor(root->right, p, q);
        if (left && right) return root;
        return left ? left : right;
    }
};
```

**Complexity:** Time O(n). Space O(h).

**Follow-ups:** (1) **BST** (LC 235): walk down from the root; go left if both values are smaller, right if both are larger, else stop. O(h), O(1) space. (2) **Parent pointers** (LC 1650): the two upward paths are like two linked lists that meet, so use the Intersection of Two Linked Lists two-pointer trick. (3) **Nodes may be missing** (LC 1644): also count how many targets were actually found. (4) **Many queries**: preprocess with **binary lifting** (`up[k][v]` = 2^k-th ancestor, O(n log n)) to answer each query in O(log n), or an Euler tour plus a sparse-table RMQ for O(1) per query.

---

### Problem 8 — Construct Binary Tree from Preorder and Inorder Traversal (LC 105) [Medium]

**Link:** [https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/)

**Problem Statement:** Given the preorder and inorder traversals of a tree with **unique** values, rebuild the tree.

**Intuition:** The next unused preorder value is the root of the current subtree. Its position `mid` in inorder splits the inorder range into the left subtree `[lo, mid-1]` and the right subtree `[mid+1, hi]`. Building left before right consumes preorder values in exactly the right order. A hash map from value to inorder index makes each split O(1), so the total is O(n) instead of O(n^2) with `inorder.index()`.

Example: `preorder = [3, 9, 20, 15, 7]`, `inorder = [9, 3, 15, 20, 7]`. Root 3 splits inorder into `[9]` and `[15, 20, 7]`; the next preorder value 9 is the left subtree's root; then 20 roots the right subtree, with 15 and 7 as its children.

**Python Solution**

```python
from typing import Optional

class Solution:
    def buildTree(self, preorder: list[int], inorder: list[int]) -> Optional[TreeNode]:
        index = {v: i for i, v in enumerate(inorder)}
        next_root = iter(preorder)

        def build(lo: int, hi: int) -> Optional[TreeNode]:   # inorder[lo..hi], inclusive
            if lo > hi:
                return None
            val = next(next_root)
            node = TreeNode(val)
            mid = index[val]
            node.left = build(lo, mid - 1)                     # must build left first
            node.right = build(mid + 1, hi)
            return node

        return build(0, len(inorder) - 1)
```

**C++ Solution**

```cpp
#include <unordered_map>
#include <vector>
using namespace std;

class Solution {
    unordered_map<int, int> index;
    int pre = 0;

    TreeNode* build(const vector<int>& preorder, int lo, int hi) {
        if (lo > hi) return nullptr;
        int val = preorder[pre++];
        TreeNode* node = new TreeNode(val);
        int mid = index[val];
        node->left = build(preorder, lo, mid - 1);
        node->right = build(preorder, mid + 1, hi);
        return node;
    }

public:
    TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {
        for (int i = 0; i < static_cast<int>(inorder.size()); ++i) index[inorder[i]] = i;
        pre = 0;
        return build(preorder, 0, static_cast<int>(inorder.size()) - 1);
    }
};
```

**Complexity:** Time O(n). Space O(n) for the map plus O(h) recursion.

**Follow-ups:** Inorder + postorder (LC 106): consume postorder from the **end** and build the **right** subtree first. Preorder + postorder (LC 889) does not determine the tree uniquely when a node has one child. Duplicate values make every pairing ambiguous, which is why the problem guarantees unique values.

---

### Problem 9 — Serialize and Deserialize Binary Tree (LC 297) [Hard]

**Link:** [https://leetcode.com/problems/serialize-and-deserialize-binary-tree/](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/)

**Problem Statement:** Design `serialize(root) -> str` and `deserialize(str) -> root` so that a round trip reproduces the tree.

**Intuition:** A single traversal is ambiguous unless **null children are written explicitly**. With null markers, either preorder or level order is enough on its own:

- **Preorder with `#` for null** (the C++ solution): `1,2,#,#,3,4,#,#,5,#,#`. Deserialisation reads tokens in the same recursive order.
- **Level order with `#`** (the Python solution; level order like LeetCode's display format, except that trailing null markers are kept): `1,2,3,#,#,4,5,#,#,#,#`. It is iterative in both directions, so a skewed tree of 10^4 nodes does not hit Python's default recursion limit of 1000.

**Python Solution**

```python
from collections import deque
from typing import Optional

class Codec:
    def serialize(self, root: Optional[TreeNode]) -> str:
        if not root:
            return ""
        out, q = [], deque([root])
        while q:
            node = q.popleft()
            if node:
                out.append(str(node.val))
                q.append(node.left)
                q.append(node.right)
            else:
                out.append("#")
        return ",".join(out)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        if not data:
            return None
        tokens = data.split(",")
        root = TreeNode(int(tokens[0]))
        q, i = deque([root]), 1
        while q:
            node = q.popleft()
            for side in ("left", "right"):     # every real node wrote exactly two child tokens
                if tokens[i] != "#":
                    child = TreeNode(int(tokens[i]))
                    setattr(node, side, child)
                    q.append(child)
                i += 1
        return root
```

**C++ Solution**

```cpp
#include <sstream>
#include <string>
using namespace std;

class Codec {
    void write(TreeNode* node, string& out) {
        if (!node) {
            out += "#,";
            return;
        }
        out += to_string(node->val) + ',';
        write(node->left, out);
        write(node->right, out);
    }

    TreeNode* read(istringstream& in) {
        string tok;
        getline(in, tok, ',');
        if (tok == "#") return nullptr;
        TreeNode* node = new TreeNode(stoi(tok));
        node->left = read(in);
        node->right = read(in);
        return node;
    }

public:
    string serialize(TreeNode* root) {
        string out;
        write(root, out);
        return out;
    }

    TreeNode* deserialize(string data) {
        istringstream in(data);
        return read(in);
    }
};
```

**Complexity:** Time O(n) both ways. Space O(n) for the string; O(h) recursion (C++) or O(width) queue (Python).

**Follow-up:** For a **BST** (LC 449) no null markers are needed: preorder alone determines the tree, because the bounds trick from Validate BST tells you where each subtree ends. That makes the encoding more compact; a binary encoding with fixed 4-byte integers is more compact still than decimal text.

---

### Problem 10 — Kth Smallest Element in a BST (LC 230) [Medium]

**Link:** [https://leetcode.com/problems/kth-smallest-element-in-a-bst/](https://leetcode.com/problems/kth-smallest-element-in-a-bst/)

**Problem Statement:** Return the `k`-th smallest value (1-indexed) in a BST.

**Intuition:** Inorder traversal of a BST visits values in sorted order. Use the **iterative** inorder so you can stop after `k` pops: O(h + k) instead of O(n).

**Python Solution**

```python
from typing import Optional

class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        stack, node = [], root
        while True:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            k -= 1
            if k == 0:
                return node.val
            node = node.right
```

**C++ Solution**

```cpp
#include <stack>
using namespace std;

class Solution {
public:
    int kthSmallest(TreeNode* root, int k) {
        stack<TreeNode*> st;
        TreeNode* node = root;
        while (true) {
            while (node) {
                st.push(node);
                node = node->left;
            }
            node = st.top();
            st.pop();
            if (--k == 0) return node->val;
            node = node->right;
        }
    }
};
```

**Complexity:** Time O(h + k). Space O(h).

**Follow-up:** "The BST is modified often and you query k-th often." Store `size` (subtree node count) in every node and maintain it on insert and delete. Then descend: if `size(left) ≥ k` go left; if `size(left) + 1 == k` return the node; otherwise go right with `k -= size(left) + 1`. That is O(h) per query, O(log n) in a balanced tree: an **order-statistic tree** (see [Ordered Containers](#29-ordered-containers)).

---

### Problem 11 — Diameter of Binary Tree (LC 543) [Easy]

**Link:** [https://leetcode.com/problems/diameter-of-binary-tree/](https://leetcode.com/problems/diameter-of-binary-tree/)

**Problem Statement:** Return the number of **edges** on the longest path between any two nodes.

**Intuition:** Same shape as Max Path Sum (Problem 5): the longest path bends at some node, using that node's left height plus right height. Post-order returns the **height** (one branch) to the parent and updates a global best with `left + right` (both branches).

**Python Solution**

```python
from typing import Optional

class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        best = 0

        def height(node: Optional[TreeNode]) -> int:     # number of nodes on the longest downward path
            nonlocal best
            if not node:
                return 0
            left, right = height(node.left), height(node.right)
            best = max(best, left + right)               # edges through node = left + right
            return 1 + max(left, right)

        height(root)
        return best
```

**C++ Solution**

```cpp
#include <algorithm>
using namespace std;

class Solution {
    int best = 0;

    int height(TreeNode* node) {
        if (!node) return 0;
        int left = height(node->left), right = height(node->right);
        best = max(best, left + right);
        return 1 + max(left, right);
    }

public:
    int diameterOfBinaryTree(TreeNode* root) {
        best = 0;
        height(root);
        return best;
    }
};
```

**Complexity:** Time O(n). Space O(h).

**Follow-up:** For a general tree or graph with no root (LC 1245, Tree Diameter), use **two BFS passes**: BFS from any node to find the farthest node `u`, then BFS from `u`; the farthest distance from `u` is the diameter.

---

### Problem 12 — Critical Connections in a Network (LC 1192) [Hard]

**Link:** [https://leetcode.com/problems/critical-connections-in-a-network/](https://leetcode.com/problems/critical-connections-in-a-network/)

**Problem Statement:** In an undirected connected graph of `n ≤ 10^5` servers, return every edge whose removal disconnects the graph (the **bridges**).

**Intuition (Tarjan's bridge algorithm):** Run one DFS and record for each node:

- `disc[u]`: the time `u` was first visited.
- `low[u]`: the smallest `disc` reachable from `u`'s DFS subtree using tree edges downward plus **at most one back edge**.

A tree edge `u → v` is a bridge exactly when `low[v] > disc[u]`: nothing in `v`'s subtree has a back edge reaching `u` or above, so removing the edge cuts the subtree off. When ignoring the edge back to the parent, skip it by **edge id**, not by parent node, so that parallel edges are handled correctly. Theory and articulation points: [DSA Fundamentals: Discovery Times and Low-Link Values](DSA_Fundamentals.md#dfs-discovery-times-and-low-link-values).

Example: a triangle 0–1–2 with a tail 1–3. DFS from 0: disc 0→0, 1→1, 2→2; the back edge 2–0 gives `low[2] = 0`, so `low[1] = 0`. Node 3 has `disc = 3`, `low = 3 > disc[1] = 1`, so edge 1–3 is the only bridge.

**Python Solution** (iterative, because a path graph of 10^5 nodes would exceed the recursion limit)

```python
class Solution:
    def criticalConnections(self, n: int, connections: list[list[int]]) -> list[list[int]]:
        adj = [[] for _ in range(n)]
        for eid, (u, v) in enumerate(connections):
            adj[u].append((v, eid))
            adj[v].append((u, eid))
        disc, low = [-1] * n, [0] * n
        timer, bridges = 0, []
        for root in range(n):
            if disc[root] != -1:
                continue
            disc[root] = low[root] = timer
            timer += 1
            stack = [(root, -1, 0)]                # (node, id of the edge we arrived by, next neighbour index)
            while stack:
                u, parent_edge, i = stack[-1]
                if i < len(adj[u]):
                    stack[-1] = (u, parent_edge, i + 1)
                    v, eid = adj[u][i]
                    if eid == parent_edge:
                        continue                   # don't use the tree edge back to the parent
                    if disc[v] == -1:              # tree edge: descend
                        disc[v] = low[v] = timer
                        timer += 1
                        stack.append((v, eid, 0))
                    else:                          # back edge
                        low[u] = min(low[u], disc[v])
                else:                              # u finished: report to its parent
                    stack.pop()
                    if stack:
                        p = stack[-1][0]
                        low[p] = min(low[p], low[u])
                        if low[u] > disc[p]:
                            bridges.append(connections[parent_edge])
        return bridges
```

**C++ Solution**

```cpp
#include <algorithm>
#include <utility>
#include <vector>
using namespace std;

class Solution {
    vector<vector<pair<int, int>>> adj;   // (neighbour, edge id)
    vector<int> disc, low;
    vector<vector<int>> bridges;
    int timer = 0;

    void dfs(int u, int parentEdge) {
        disc[u] = low[u] = timer++;
        for (auto [v, id] : adj[u]) {
            if (id == parentEdge) continue;
            if (disc[v] == -1) {
                dfs(v, id);
                low[u] = min(low[u], low[v]);
                if (low[v] > disc[u]) bridges.push_back({u, v});
            } else {
                low[u] = min(low[u], disc[v]);
            }
        }
    }

public:
    vector<vector<int>> criticalConnections(int n, vector<vector<int>>& connections) {
        adj.assign(n, {});
        for (int i = 0; i < static_cast<int>(connections.size()); ++i) {
            adj[connections[i][0]].push_back({connections[i][1], i});
            adj[connections[i][1]].push_back({connections[i][0], i});
        }
        disc.assign(n, -1);
        low.assign(n, 0);
        for (int i = 0; i < n; ++i)
            if (disc[i] == -1) dfs(i, -1);
        return bridges;
    }
};
```

**Complexity:** Time O(V + E). Space O(V + E). The recursive C++ version reaches depth 10^5 on a path graph; that fits LeetCode's stack, but production code should use the iterative form or run on a thread with a larger stack.

**Follow-up (articulation points):** A non-root vertex `u` is a cut vertex if some child `v` has `low[v] ≥ disc[u]` (note `≥`, not `>`: the subtree may reach `u` itself but nothing above it). The DFS root is a cut vertex if it has two or more DFS children.

---

### Interview Q&A

**Q1.** What are the common wrong answers for Validate BST, and how do you avoid them?

(1) Comparing only with direct children, which misses violations deeper down (the `5 → 6 → 3` example). Fix: pass bounds down. (2) Using `INT_MIN`/`INT_MAX` as sentinels in C++, which fails when a node actually holds `INT_MIN`. Fix: use `long long` bounds, `nullptr`-able pointers, or `std::optional`. (3) Allowing duplicates when the problem says strictly less/greater: use `<` and `>` consistently and ask which side duplicates go to if the problem allows them. (4) The inorder approach comparing with a `prev` value initialised to a sentinel has the same sentinel issue; store `prev` as a node pointer instead.

**Q2.** How do you traverse a tree in O(1) extra space?

**Morris traversal.** For each node with a left child, find its inorder predecessor (the rightmost node of the left subtree). If the predecessor's right pointer is null, point it at the current node (a temporary thread) and go left. If it already points at the current node, the left subtree is finished: remove the thread, visit the node, and go right. Each edge is walked at most a few times, so it is O(n) time and O(1) space. The tree is temporarily modified, which matters for concurrent readers, and the code is easy to get wrong, so mention it as a follow-up and code the stack version unless asked.

```python
def morris_inorder(root) -> list[int]:
    out, node = [], root
    while node:
        if node.left is None:
            out.append(node.val)
            node = node.right
        else:
            pred = node.left
            while pred.right and pred.right is not node:
                pred = pred.right
            if pred.right is None:
                pred.right = node          # create the thread, descend left
                node = node.left
            else:
                pred.right = None          # remove the thread, visit, go right
                out.append(node.val)
                node = node.right
    return out
```

**Q3.** Recursion or iteration for tree DFS in production code?

Recursion depth equals tree height. For balanced trees (`log n`) recursion is fine and clearer. For trees that can degenerate (unbalanced BSTs, parse trees of long expressions, linked-list-shaped inputs) the depth can reach `n`. CPython's default recursion limit is 1000, and raising it with `sys.setrecursionlimit` can crash the interpreter if the C stack runs out. In C++, each frame uses tens to hundreds of bytes, so 10^6 frames can exceed a typical 8 MiB main-thread stack (and worker threads often have smaller stacks). Iterative traversals with an explicit heap-allocated stack avoid both problems.

**Q4.** Explain `low[]` in Tarjan's algorithm to someone who has never seen it.

Number the nodes in DFS visit order (`disc`). `low[u]` asks: "starting inside `u`'s DFS subtree and using a single back edge at the end, how far back in visit order can I jump?" If a child's subtree cannot jump to `u` or earlier (`low[v] > disc[u]`), the only connection between that subtree and the rest of the graph is the edge `u–v`, so it is a bridge. If it cannot jump **above** `u` (`low[v] ≥ disc[u]`), then removing `u` disconnects it, so `u` is an articulation point. The same `low` values, with a stack of the current path, also give strongly connected components in directed graphs (Tarjan's SCC).

**Q5.** Where do bridges and articulation points matter in real systems?

They are single points of failure. In a network topology, a bridge is a link whose failure partitions the network; an articulation point is a router or switch whose failure does. In a service dependency graph, an articulation point is a service that every path between two groups depends on. In a GPU cluster interconnect, finding cut links tells you which cable failure would split a job's ranks into partitions that cannot communicate. Bridge-finding in O(V + E) makes it practical to re-check after every topology change.

---
## 9. Two Heaps

### Overview

The Two Heaps pattern maintains two heaps to efficiently track the median (or similar order-statistic queries) of a dynamic data set:

- **Max-heap** — stores the **lower half** of the elements (so its top is the largest of the small elements).
- **Min-heap** — stores the **upper half** of the elements (so its top is the smallest of the large elements).

**Key invariant:** the max-heap's size is either equal to the min-heap's size (when the total count is even) or exactly one greater (when the total count is odd). This lets us read the median in **O(1)** and insert a new element in **O(log n)**.

| Operation | Time | Space |
|-----------|------|-------|
| Insert | O(log n) | O(n) |
| Find Median | O(1) | — |

### When to Use

- Find the **median** of a data stream.
- **Sliding window median** problems.
- **Balance partitioning** — split a set into two halves with a target property.
- **IPO / scheduling** problems that pair a cost heap with a profit heap.

### Template Code

#### Python

Python's `heapq` is a **min-heap only**, so we simulate a max-heap by negating values.

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.lo = []  # max-heap (negate values)
        self.hi = []  # min-heap

    def addNum(self, num: int) -> None:
        heapq.heappush(self.lo, -num)
        # Ensure every element in lo <= every element in hi
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        # Maintain size property: len(lo) >= len(hi)
        if len(self.lo) < len(self.hi):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self) -> float:
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2.0
```

#### C++

```cpp
#include <queue>

class MedianFinder {
    std::priority_queue<int> lo;                             // max-heap
    std::priority_queue<int, std::vector<int>,
                        std::greater<int>> hi;               // min-heap
public:
    void addNum(int num) {
        lo.push(num);
        hi.push(lo.top()); lo.pop();
        if (lo.size() < hi.size()) {
            lo.push(hi.top()); hi.pop();
        }
    }

    double findMedian() {
        if (lo.size() > hi.size()) return lo.top();
        return (lo.top() + hi.top()) / 2.0;
    }
};
```

### Variations

| Variation | Key Idea |
|-----------|----------|
| Basic Median Finder | Two heaps, rebalance after every insert |
| Sliding Window Median | Two heaps + **lazy deletion** with a hash-map of invalidated entries |
| Maximize Capital (IPO) | Min-heap sorted by cost, max-heap sorted by profit; greedily pick highest-profit affordable project |

### Common Mistakes

1. **Forgetting to rebalance** after insertion — sizes can diverge by more than 1.
2. **Python negation errors** — forgetting to negate on push *and* on pop from the max-heap.
3. **Even/odd confusion** — returning the wrong value when total count is even vs. odd.
4. **Off-by-one** — allowing sizes to differ by 2+ before noticing.

### Related Patterns

- **Top K Elements** — also heap-based, but uses a single heap of bounded size.
- **Sorting** — heaps are partial-sort structures; full sort gives median trivially but at higher cost.

### Example Problems

#### 1. Last Stone Weight (LC 1046) — Easy

> We have a collection of stones, each with a positive integer weight. Each turn, we choose the two heaviest stones and smash them. If they have equal weight both are destroyed; otherwise the lighter one is destroyed and the heavier one has its weight reduced by the lighter's weight. Return the weight of the last remaining stone (or 0).

[LeetCode 1046](https://leetcode.com/problems/last-stone-weight/)

**Intuition:** Use a single max-heap. Pop the two largest, push back their difference (if non-zero). Repeat until ≤ 1 stone remains.

**Python:**

```python
import heapq

class Solution:
    def lastStoneWeight(self, stones: list[int]) -> int:
        heap = [-s for s in stones]
        heapq.heapify(heap)

        while len(heap) > 1:
            a = -heapq.heappop(heap)
            b = -heapq.heappop(heap)
            if a != b:
                heapq.heappush(heap, -(a - b))

        return -heap[0] if heap else 0
```

**C++:**

```cpp
#include <queue>
#include <vector>

class Solution {
public:
    int lastStoneWeight(std::vector<int>& stones) {
        std::priority_queue<int> pq(stones.begin(), stones.end());

        while (pq.size() > 1) {
            int a = pq.top(); pq.pop();
            int b = pq.top(); pq.pop();
            if (a != b) pq.push(a - b);
        }

        return pq.empty() ? 0 : pq.top();
    }
};
```

**Complexity:** Time O(n log n) — each of n stones is pushed/popped at most once. Space O(n).

---

#### 2. Find Median from Data Stream (LC 295) — Medium

> Design a data structure that supports `addNum(int num)` and `findMedian() -> double` for a stream of integers.

[LeetCode 295](https://leetcode.com/problems/find-median-from-data-stream/)

**Intuition:** Classic two-heap approach. Keep a max-heap for the lower half and a min-heap for the upper half. After every insertion, rebalance so the max-heap is at most one element larger.

**Python:**

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.lo = []  # max-heap (negated)
        self.hi = []  # min-heap

    def addNum(self, num: int) -> None:
        heapq.heappush(self.lo, -num)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        if len(self.lo) < len(self.hi):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self) -> float:
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2.0
```

**C++:**

```cpp
#include <queue>

class MedianFinder {
    std::priority_queue<int> lo;
    std::priority_queue<int, std::vector<int>, std::greater<int>> hi;
public:
    void addNum(int num) {
        lo.push(num);
        hi.push(lo.top()); lo.pop();
        if (lo.size() < hi.size()) {
            lo.push(hi.top()); hi.pop();
        }
    }

    double findMedian() {
        if (lo.size() > hi.size()) return lo.top();
        return (lo.top() + hi.top()) / 2.0;
    }
};
```

**Complexity:** Insert O(log n), Find Median O(1). Space O(n).

---

#### 3. Kth Largest Element in a Stream (LC 703) — Medium

> Design a class that finds the k-th largest element in a stream. `KthLargest(int k, int[] nums)` initializes with `k` and a stream `nums`. `int add(int val)` appends `val` and returns the k-th largest element.

[LeetCode 703](https://leetcode.com/problems/kth-largest-element-in-a-stream/)

**Intuition:** Maintain a **min-heap of size k**. The top of the heap is always the k-th largest. When a new number arrives, push it; if the heap exceeds size k, pop the smallest.

**Python:**

```python
import heapq

class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.heap = nums
        heapq.heapify(self.heap)
        while len(self.heap) > k:
            heapq.heappop(self.heap)

    def add(self, val: int) -> int:
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]
```

**C++:**

```cpp
#include <queue>
#include <vector>

class KthLargest {
    int k;
    std::priority_queue<int, std::vector<int>, std::greater<int>> minHeap;
public:
    KthLargest(int k, std::vector<int>& nums) : k(k) {
        for (int n : nums) {
            minHeap.push(n);
            if ((int)minHeap.size() > k) minHeap.pop();
        }
    }

    int add(int val) {
        minHeap.push(val);
        if ((int)minHeap.size() > k) minHeap.pop();
        return minHeap.top();
    }
};
```

**Complexity:** Constructor O(n log k). `add` O(log k). Space O(k).

---

#### 4. Sliding Window Median (LC 480) — Hard

> Given an array of integers `nums` and an integer `k`, return the median of each window of size `k` as the window slides from left to right.

[LeetCode 480](https://leetcode.com/problems/sliding-window-median/)

**Intuition:** Use two heaps (like the Median Finder) plus **lazy deletion**. When an element leaves the window, record it in a hash-map of "to-delete" counts rather than immediately removing it from the heap. Before reading the heap tops, purge any invalidated entries. Rebalance after each add/remove cycle.

**Python:**

```python
import heapq
from collections import defaultdict

class Solution:
    def medianSlidingWindow(self, nums: list[int], k: int) -> list[float]:
        lo = []   # max-heap (negated)
        hi = []   # min-heap
        delayed = defaultdict(int)
        lo_size = hi_size = 0

        def prune(heap):
            while heap and delayed[heap[0] if heap is hi else -heap[0]] > 0:
                val = heap[0] if heap is hi else -heap[0]
                delayed[val] -= 1
                if delayed[val] == 0:
                    del delayed[val]
                heapq.heappop(heap)

        def rebalance():
            nonlocal lo_size, hi_size
            if lo_size > hi_size + 1:
                val = -heapq.heappop(lo)
                heapq.heappush(hi, val)
                lo_size -= 1
                hi_size += 1
                prune(lo)
            elif hi_size > lo_size:
                val = heapq.heappop(hi)
                heapq.heappush(lo, -val)
                hi_size -= 1
                lo_size += 1
                prune(hi)

        def add(num):
            nonlocal lo_size, hi_size
            if not lo or num <= -lo[0]:
                heapq.heappush(lo, -num)
                lo_size += 1
            else:
                heapq.heappush(hi, num)
                hi_size += 1
            rebalance()

        def remove(num):
            nonlocal lo_size, hi_size
            delayed[num] += 1
            if num <= -lo[0]:
                lo_size -= 1
            else:
                hi_size -= 1
            rebalance()
            prune(lo)
            prune(hi)

        def get_median():
            if k % 2 == 1:
                return float(-lo[0])
            return (-lo[0] + hi[0]) / 2.0

        result = []
        for i, num in enumerate(nums):
            add(num)
            if i >= k:
                remove(nums[i - k])
            if i >= k - 1:
                result.append(get_median())
        return result
```

**C++:**

```cpp
#include <vector>
#include <queue>
#include <unordered_map>

class Solution {
public:
    std::vector<double> medianSlidingWindow(std::vector<int>& nums, int k) {
        std::priority_queue<int> lo;
        std::priority_queue<int, std::vector<int>, std::greater<int>> hi;
        std::unordered_map<int, int> delayed;
        int loSz = 0, hiSz = 0;

        auto prune = [&](auto& heap) {
            while (!heap.empty() && delayed.count(heap.top()) && delayed[heap.top()] > 0) {
                if (--delayed[heap.top()] == 0) delayed.erase(heap.top());
                heap.pop();
            }
        };

        auto rebalance = [&]() {
            if (loSz > hiSz + 1) {
                hi.push(lo.top()); lo.pop();
                --loSz; ++hiSz;
                prune(lo);
            } else if (hiSz > loSz) {
                lo.push(hi.top()); hi.pop();
                --hiSz; ++loSz;
                prune(hi);
            }
        };

        auto addNum = [&](int num) {
            if (lo.empty() || num <= lo.top()) { lo.push(num); ++loSz; }
            else { hi.push(num); ++hiSz; }
            rebalance();
        };

        auto removeNum = [&](int num) {
            ++delayed[num];
            if (num <= lo.top()) --loSz;
            else --hiSz;
            rebalance();
            prune(lo);
            prune(hi);
        };

        auto getMedian = [&]() -> double {
            if (k & 1) return lo.top();
            return ((double)lo.top() + hi.top()) / 2.0;
        };

        std::vector<double> result;
        for (int i = 0; i < (int)nums.size(); ++i) {
            addNum(nums[i]);
            if (i >= k) removeNum(nums[i - k]);
            if (i >= k - 1) result.push_back(getMedian());
        }
        return result;
    }
};
```

**Complexity:** Time O(n log n) — each element is pushed/popped once; lazy deletion amortises. Space O(n).

---

#### 5. IPO (LC 502) — Hard

> You are given `k` projects to select, an initial capital `w`, arrays `profits[]` and `capital[]`. To start project `i` you need at least `capital[i]`; upon completion you gain `profits[i]`. Maximize your total capital after finishing at most `k` projects.

[LeetCode 502](https://leetcode.com/problems/ipo/)

**Intuition:** Sort projects by capital. Use a **min-heap** (or just a sorted pointer) to feed affordable projects into a **max-heap** sorted by profit. Greedily pick the most profitable affordable project each round, add its profit to your capital, then unlock newly affordable projects.

**Python:**

```python
import heapq

class Solution:
    def findMaximizedCapital(self, k: int, w: int, profits: list[int],
                             capital: list[int]) -> int:
        projects = sorted(zip(capital, profits))
        max_profit = []  # max-heap (negated)
        idx = 0

        for _ in range(k):
            while idx < len(projects) and projects[idx][0] <= w:
                heapq.heappush(max_profit, -projects[idx][1])
                idx += 1
            if not max_profit:
                break
            w += -heapq.heappop(max_profit)

        return w
```

**C++:**

```cpp
#include <vector>
#include <queue>
#include <algorithm>

class Solution {
public:
    int findMaximizedCapital(int k, int w,
                             std::vector<int>& profits,
                             std::vector<int>& capital) {
        int n = profits.size();
        std::vector<std::pair<int,int>> projects(n);
        for (int i = 0; i < n; ++i)
            projects[i] = {capital[i], profits[i]};
        std::sort(projects.begin(), projects.end());

        std::priority_queue<int> maxProfit;
        int idx = 0;

        for (int i = 0; i < k; ++i) {
            while (idx < n && projects[idx].first <= w) {
                maxProfit.push(projects[idx].second);
                ++idx;
            }
            if (maxProfit.empty()) break;
            w += maxProfit.top(); maxProfit.pop();
        }

        return w;
    }
};
```

**Complexity:** Time O(n log n) for sorting + O(k log n) for heap operations. Space O(n).

---

## 10. Subsets / Backtracking

### Overview

Backtracking is a systematic way to explore **all candidate solutions** by building them incrementally. At each step, the algorithm:

1. **Chooses** — extends the current partial solution.
2. **Explores** — recurses to build further.
3. **Un-chooses (backtracks)** — undoes the last choice and tries the next alternative.

A candidate is abandoned ("pruned") as soon as it is determined that it **cannot** lead to a valid complete solution. This makes backtracking far more efficient than brute-force enumeration in practice, even though worst-case complexity is often exponential.

Backtracking is the engine behind generating all subsets, permutations, combinations, and solving constraint-satisfaction problems like N-Queens and Sudoku.

### When to Use

- Generate **all subsets** (power set).
- Generate **all combinations** of a given size.
- Generate **all permutations**.
- **Constraint satisfaction**: N-Queens, Sudoku, crossword filling.
- **Partition problems**: partition into k equal-sum subsets.
- **Word search** on a grid.
- Any problem that asks *"find all valid configurations."*

### Template Code

#### Subsets Template

**Python:**

```python
def subsets(nums: list[int]) -> list[list[int]]:
    result = []

    def backtrack(start: int, path: list[int]):
        result.append(path[:])  # record current subset
        for i in range(start, len(nums)):
            path.append(nums[i])       # choose
            backtrack(i + 1, path)     # explore
            path.pop()                 # un-choose

    backtrack(0, [])
    return result
```

**C++:**

```cpp
#include <vector>

class Solution {
public:
    std::vector<std::vector<int>> subsets(std::vector<int>& nums) {
        std::vector<std::vector<int>> result;
        std::vector<int> path;
        backtrack(nums, 0, path, result);
        return result;
    }

private:
    void backtrack(std::vector<int>& nums, int start,
                   std::vector<int>& path,
                   std::vector<std::vector<int>>& result) {
        result.push_back(path);
        for (int i = start; i < (int)nums.size(); ++i) {
            path.push_back(nums[i]);
            backtrack(nums, i + 1, path, result);
            path.pop_back();
        }
    }
};
```

#### Combinations Template

**Python:**

```python
def combine(n: int, k: int) -> list[list[int]]:
    result = []

    def backtrack(start: int, path: list[int]):
        if len(path) == k:
            result.append(path[:])
            return
        for i in range(start, n + 1):
            path.append(i)
            backtrack(i + 1, path)
            path.pop()

    backtrack(1, [])
    return result
```

**C++:**

```cpp
#include <vector>

class Solution {
public:
    std::vector<std::vector<int>> combine(int n, int k) {
        std::vector<std::vector<int>> result;
        std::vector<int> path;
        backtrack(1, n, k, path, result);
        return result;
    }

private:
    void backtrack(int start, int n, int k,
                   std::vector<int>& path,
                   std::vector<std::vector<int>>& result) {
        if ((int)path.size() == k) {
            result.push_back(path);
            return;
        }
        for (int i = start; i <= n; ++i) {
            path.push_back(i);
            backtrack(i + 1, n, k, path, result);
            path.pop_back();
        }
    }
};
```

#### Permutations Template

**Python:**

```python
def permute(nums: list[int]) -> list[list[int]]:
    result = []

    def backtrack(path: list[int], used: list[bool]):
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

**C++:**

```cpp
#include <vector>

class Solution {
public:
    std::vector<std::vector<int>> permute(std::vector<int>& nums) {
        std::vector<std::vector<int>> result;
        std::vector<int> path;
        std::vector<bool> used(nums.size(), false);
        backtrack(nums, used, path, result);
        return result;
    }

private:
    void backtrack(std::vector<int>& nums, std::vector<bool>& used,
                   std::vector<int>& path,
                   std::vector<std::vector<int>>& result) {
        if (path.size() == nums.size()) {
            result.push_back(path);
            return;
        }
        for (int i = 0; i < (int)nums.size(); ++i) {
            if (used[i]) continue;
            used[i] = true;
            path.push_back(nums[i]);
            backtrack(nums, used, path, result);
            path.pop_back();
            used[i] = false;
        }
    }
};
```

### Variations

| Variation | Key Idea |
|-----------|----------|
| Subsets (power set) | Include/exclude each element; `start` index avoids duplicates |
| Subsets with duplicates | Sort first; skip `nums[i] == nums[i-1]` at the same recursion level |
| Combinations | Like subsets but stop when `path` reaches size k |
| Combination Sum (reuse allowed) | Recurse with `i` (not `i+1`) to allow reuse; prune when remainder < 0 |
| Combination Sum (no reuse) | Recurse with `i+1`; sort + skip duplicates |
| Permutations | Use a `used[]` boolean array; every element can appear at every position |
| Permutations with duplicates | Sort + skip `nums[i] == nums[i-1]` when `!used[i-1]` |
| Constraint satisfaction | Place queens/digits, validate constraints, backtrack on violation |

### Common Mistakes

1. **Not sorting before handling duplicates** — duplicate-skipping logic (`nums[i] == nums[i-1]`) requires a sorted array.
2. **Not restoring state on backtrack** — forgetting `path.pop()` or resetting `used[i] = false`.
3. **Wrong index management** — using `i` instead of `i+1` (or vice-versa) when reuse is/isn't allowed.
4. **Not pruning early enough** — continuing to recurse when the remaining sum is already negative or the remaining elements can't fill the required slots.

### Related Patterns

- **DFS** — backtracking is DFS on an implicit decision tree.
- **Dynamic Programming** — when subproblems overlap, memoisation (top-down DP) can replace pure backtracking.

### Example Problems

#### 1. Subsets (LC 78) — Medium

> Given an integer array `nums` of unique elements, return all possible subsets (the power set). The solution must not contain duplicate subsets.

[LeetCode 78](https://leetcode.com/problems/subsets/)

**Intuition:** At each index, decide to include or exclude the element. Using a `start` parameter ensures each subset is generated exactly once without duplicates.

**Python:**

```python
class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        result = []

        def backtrack(start: int, path: list[int]):
            result.append(path[:])
            for i in range(start, len(nums)):
                path.append(nums[i])
                backtrack(i + 1, path)
                path.pop()

        backtrack(0, [])
        return result
```

**C++:**

```cpp
#include <vector>

class Solution {
public:
    std::vector<std::vector<int>> subsets(std::vector<int>& nums) {
        std::vector<std::vector<int>> result;
        std::vector<int> path;
        backtrack(nums, 0, path, result);
        return result;
    }

private:
    void backtrack(std::vector<int>& nums, int start,
                   std::vector<int>& path,
                   std::vector<std::vector<int>>& result) {
        result.push_back(path);
        for (int i = start; i < (int)nums.size(); ++i) {
            path.push_back(nums[i]);
            backtrack(nums, i + 1, path, result);
            path.pop_back();
        }
    }
};
```

**Complexity:** Time O(n · 2^n) — 2^n subsets, each copied in O(n). Space O(n) recursion depth (output excluded).

---

#### 2. Permutations (LC 46) — Medium

> Given an array `nums` of distinct integers, return all possible permutations in any order.

[LeetCode 46](https://leetcode.com/problems/permutations/)

**Intuition:** Unlike subsets, every element can appear at every position. Track which elements are already used with a boolean array. When the path length equals `n`, we have a complete permutation.

**Python:**

```python
class Solution:
    def permute(self, nums: list[int]) -> list[list[int]]:
        result = []
        used = [False] * len(nums)

        def backtrack(path: list[int]):
            if len(path) == len(nums):
                result.append(path[:])
                return
            for i in range(len(nums)):
                if used[i]:
                    continue
                used[i] = True
                path.append(nums[i])
                backtrack(path)
                path.pop()
                used[i] = False

        backtrack([])
        return result
```

**C++:**

```cpp
#include <vector>

class Solution {
public:
    std::vector<std::vector<int>> permute(std::vector<int>& nums) {
        std::vector<std::vector<int>> result;
        std::vector<int> path;
        std::vector<bool> used(nums.size(), false);
        backtrack(nums, used, path, result);
        return result;
    }

private:
    void backtrack(std::vector<int>& nums, std::vector<bool>& used,
                   std::vector<int>& path,
                   std::vector<std::vector<int>>& result) {
        if (path.size() == nums.size()) {
            result.push_back(path);
            return;
        }
        for (int i = 0; i < (int)nums.size(); ++i) {
            if (used[i]) continue;
            used[i] = true;
            path.push_back(nums[i]);
            backtrack(nums, used, path, result);
            path.pop_back();
            used[i] = false;
        }
    }
};
```

**Complexity:** Time O(n · n!) — n! permutations, each copied in O(n). Space O(n).

---

#### 3. Combination Sum (LC 39) — Medium

> Given an array of distinct integers `candidates` and a target integer `target`, return all unique combinations where the chosen numbers sum to `target`. The same number may be chosen an **unlimited** number of times.

[LeetCode 39](https://leetcode.com/problems/combination-sum/)

**Intuition:** Backtrack with a running remainder. At index `i`, we can use `candidates[i]` again (recurse with `i`, not `i+1`). Prune when the remainder goes below zero. Sorting enables early termination: if `candidates[i] > remain`, all subsequent candidates are too large.

**Python:**

```python
class Solution:
    def combinationSum(self, candidates: list[int],
                       target: int) -> list[list[int]]:
        candidates.sort()
        result = []

        def backtrack(start: int, remain: int, path: list[int]):
            if remain == 0:
                result.append(path[:])
                return
            for i in range(start, len(candidates)):
                if candidates[i] > remain:
                    break
                path.append(candidates[i])
                backtrack(i, remain - candidates[i], path)
                path.pop()

        backtrack(0, target, [])
        return result
```

**C++:**

```cpp
#include <vector>
#include <algorithm>

class Solution {
public:
    std::vector<std::vector<int>> combinationSum(
            std::vector<int>& candidates, int target) {
        std::sort(candidates.begin(), candidates.end());
        std::vector<std::vector<int>> result;
        std::vector<int> path;
        backtrack(candidates, 0, target, path, result);
        return result;
    }

private:
    void backtrack(std::vector<int>& cands, int start, int remain,
                   std::vector<int>& path,
                   std::vector<std::vector<int>>& result) {
        if (remain == 0) {
            result.push_back(path);
            return;
        }
        for (int i = start; i < (int)cands.size(); ++i) {
            if (cands[i] > remain) break;
            path.push_back(cands[i]);
            backtrack(cands, i, remain - cands[i], path, result);
            path.pop_back();
        }
    }
};
```

**Complexity:** Time O(n^(T/M)) where T = target, M = min candidate (upper bound on recursion tree size). Space O(T/M) recursion depth.

---

#### 4. Word Search (LC 79) — Medium

> Given an `m × n` grid of characters and a string `word`, return `true` if `word` exists in the grid. The word can be constructed from sequentially adjacent cells (horizontal/vertical), and each cell may be used at most once.

[LeetCode 79](https://leetcode.com/problems/word-search/)

**Intuition:** From every cell that matches `word[0]`, run DFS/backtracking. Mark visited cells (e.g., overwrite with `'#'`), explore four directions, then restore the cell.

**Python:**

```python
class Solution:
    def exist(self, board: list[list[str]], word: str) -> bool:
        rows, cols = len(board), len(board[0])

        def backtrack(r: int, c: int, idx: int) -> bool:
            if idx == len(word):
                return True
            if (r < 0 or r >= rows or c < 0 or c >= cols
                    or board[r][c] != word[idx]):
                return False

            saved = board[r][c]
            board[r][c] = '#'

            for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                if backtrack(r + dr, c + dc, idx + 1):
                    return True

            board[r][c] = saved
            return False

        for r in range(rows):
            for c in range(cols):
                if backtrack(r, c, 0):
                    return True
        return False
```

**C++:**

```cpp
#include <vector>
#include <string>

class Solution {
public:
    bool exist(std::vector<std::vector<char>>& board,
               std::string word) {
        int rows = board.size(), cols = board[0].size();

        auto backtrack = [&](auto& self, int r, int c, int idx) -> bool {
            if (idx == (int)word.size()) return true;
            if (r < 0 || r >= rows || c < 0 || c >= cols
                || board[r][c] != word[idx])
                return false;

            char saved = board[r][c];
            board[r][c] = '#';

            int dirs[] = {0,1,0,-1,0};
            for (int d = 0; d < 4; ++d) {
                if (self(self, r + dirs[d], c + dirs[d+1], idx + 1))
                    return true;
            }

            board[r][c] = saved;
            return false;
        };

        for (int r = 0; r < rows; ++r)
            for (int c = 0; c < cols; ++c)
                if (backtrack(backtrack, r, c, 0))
                    return true;
        return false;
    }
};
```

**Complexity:** Time O(m · n · 3^L) where L = word length (3 directions after the first step since we don't revisit the previous cell). Space O(L) recursion depth.

---

#### 5. N-Queens (LC 51) — Hard

> Place `n` queens on an `n × n` chessboard so that no two queens threaten each other (no shared row, column, or diagonal). Return all distinct solutions.

[LeetCode 51](https://leetcode.com/problems/n-queens/)

**Intuition:** Place queens row by row. For each row, try every column. Track attacked columns, diagonals (`row - col`), and anti-diagonals (`row + col`) in sets. If a column/diagonal is already occupied, skip it. When all `n` rows are filled, record the board.

**Python:**

```python
class Solution:
    def solveNQueens(self, n: int) -> list[list[str]]:
        result = []
        cols = set()
        diag = set()       # row - col
        anti_diag = set()   # row + col
        board = [['.' ] * n for _ in range(n)]

        def backtrack(row: int):
            if row == n:
                result.append([''.join(r) for r in board])
                return
            for col in range(n):
                if col in cols or (row - col) in diag or (row + col) in anti_diag:
                    continue
                cols.add(col)
                diag.add(row - col)
                anti_diag.add(row + col)
                board[row][col] = 'Q'

                backtrack(row + 1)

                board[row][col] = '.'
                cols.remove(col)
                diag.remove(row - col)
                anti_diag.remove(row + col)

        backtrack(0)
        return result
```

**C++:**

```cpp
#include <vector>
#include <string>
#include <unordered_set>

class Solution {
public:
    std::vector<std::vector<std::string>> solveNQueens(int n) {
        std::vector<std::vector<std::string>> result;
        std::vector<std::string> board(n, std::string(n, '.'));
        std::unordered_set<int> cols, diag, antiDiag;
        backtrack(0, n, cols, diag, antiDiag, board, result);
        return result;
    }

private:
    void backtrack(int row, int n,
                   std::unordered_set<int>& cols,
                   std::unordered_set<int>& diag,
                   std::unordered_set<int>& antiDiag,
                   std::vector<std::string>& board,
                   std::vector<std::vector<std::string>>& result) {
        if (row == n) {
            result.push_back(board);
            return;
        }
        for (int col = 0; col < n; ++col) {
            if (cols.count(col) || diag.count(row - col)
                || antiDiag.count(row + col))
                continue;

            cols.insert(col);
            diag.insert(row - col);
            antiDiag.insert(row + col);
            board[row][col] = 'Q';

            backtrack(row + 1, n, cols, diag, antiDiag, board, result);

            board[row][col] = '.';
            cols.erase(col);
            diag.erase(row - col);
            antiDiag.erase(row + col);
        }
    }
};
```

**Complexity:** Time O(n!) — at most n choices in row 0, n−1 in row 1, etc. (with pruning). Space O(n²) for the board + O(n) for tracking sets.

---
## 11. Modified Binary Search

### Overview

Binary search divides the search space in half each iteration, achieving **O(log n)** time complexity. The "modified" version adapts this elegant idea to non-standard scenarios: searching in **rotated sorted arrays**, finding **boundaries** (first/last occurrence), searching in **2D matrices**, or **binary search on the answer** (searching the result space rather than the input). The key insight is that binary search works whenever you can define a predicate that partitions the search space into two halves — one where the predicate is true and one where it is false.

### When to Use

- Sorted array (even partially sorted)
- Finding the first or last occurrence of a target
- Rotated sorted array
- Searching in a sorted 2D matrix
- Minimizing or maximizing a value subject to a constraint (binary search on answer)
- Peak finding in an unsorted array
- Any problem where the search space can be halved based on a condition

### Template Code

#### 1. Standard Binary Search

**Python:**

```python
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

**C++:**

```cpp
int binarySearch(vector<int>& nums, int target) {
    int lo = 0, hi = nums.size() - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) return mid;
        else if (nums[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}
```

#### 2. Find Leftmost (First) Occurrence

**Python:**

```python
def find_left(nums, target):
    lo, hi = 0, len(nums) - 1
    result = -1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            result = mid
            hi = mid - 1        # keep searching left
        elif nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return result
```

**C++:**

```cpp
int findLeft(vector<int>& nums, int target) {
    int lo = 0, hi = nums.size() - 1, result = -1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) {
            result = mid;
            hi = mid - 1;       // keep searching left
        } else if (nums[mid] < target) {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    return result;
}
```

#### 3. Search in Rotated Sorted Array

**Python:**

```python
def search_rotated(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:           # left half is sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                                # right half is sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
```

**C++:**

```cpp
int searchRotated(vector<int>& nums, int target) {
    int lo = 0, hi = nums.size() - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) return mid;
        if (nums[lo] <= nums[mid]) {        // left half sorted
            if (nums[lo] <= target && target < nums[mid])
                hi = mid - 1;
            else
                lo = mid + 1;
        } else {                             // right half sorted
            if (nums[mid] < target && target <= nums[hi])
                lo = mid + 1;
            else
                hi = mid - 1;
        }
    }
    return -1;
}
```

### Variations

| Variation | Description |
|-----------|-------------|
| **Standard** | Classic binary search for exact match in a sorted array |
| **Find boundaries** | `bisect_left` / `bisect_right` — find first or last position of target |
| **Rotated array** | Determine which half is sorted, then decide which half to search |
| **2D matrix search** | Treat an m×n matrix as a virtual 1D array of length m*n |
| **Binary search on answer** | Search the result space; use a feasibility check as the predicate |

### Common Mistakes

1. **Infinite loops** — Wrong mid calculation or wrong pointer update. Always ensure the search space shrinks (e.g., `lo = mid + 1`, not `lo = mid`).
2. **Integer overflow in mid** — Use `lo + (hi - lo) / 2` instead of `(lo + hi) / 2`.
3. **Off-by-one with inclusive vs exclusive bounds** — Be consistent: if `hi = len - 1` (inclusive), use `lo <= hi`; if `hi = len` (exclusive), use `lo < hi`.
4. **Not handling duplicates** — When duplicates exist (e.g., rotated sorted array II), worst case degrades to O(n).

### Related Patterns

- **Two Pointers** — both narrow a search range, but two pointers works on unsorted data with different conditions
- **Sorting** — binary search requires sorted input; sometimes you sort first then binary search

---

### Example Problems

### Problem 1: Binary Search (LC 704) — Easy

**Problem**: Given a sorted array of integers `nums` and a target value, return the index of the target if found, otherwise return -1.

**Link**: [https://leetcode.com/problems/binary-search/](https://leetcode.com/problems/binary-search/)

**Intuition**: This is the textbook binary search. Compare the middle element to the target: if equal, return; if target is larger, search right half; if smaller, search left half. Each step cuts the search space in half.

**Python:**

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = lo + (hi - lo) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1
```

**C++:**

```cpp
class Solution {
public:
    int search(vector<int>& nums, int target) {
        int lo = 0, hi = nums.size() - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] == target) return mid;
            else if (nums[mid] < target) lo = mid + 1;
            else hi = mid - 1;
        }
        return -1;
    }
};
```

**Complexity**: Time O(log n), Space O(1).

---

### Problem 2: Find First and Last Position of Element in Sorted Array (LC 34) — Medium

**Problem**: Given a sorted array of integers and a target, find the starting and ending position of the target. Return `[-1, -1]` if not found.

**Link**: [https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/)

**Intuition**: Run two binary searches — one to find the leftmost occurrence (when you find the target, record it and keep searching left) and one for the rightmost (record and keep searching right). Each search is O(log n).

**Python:**

```python
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        def find_bound(is_left):
            lo, hi = 0, len(nums) - 1
            result = -1
            while lo <= hi:
                mid = lo + (hi - lo) // 2
                if nums[mid] == target:
                    result = mid
                    if is_left:
                        hi = mid - 1    # search left for first
                    else:
                        lo = mid + 1    # search right for last
                elif nums[mid] < target:
                    lo = mid + 1
                else:
                    hi = mid - 1
            return result

        return [find_bound(True), find_bound(False)]
```

**C++:**

```cpp
class Solution {
public:
    vector<int> searchRange(vector<int>& nums, int target) {
        return {findBound(nums, target, true), findBound(nums, target, false)};
    }

private:
    int findBound(vector<int>& nums, int target, bool isLeft) {
        int lo = 0, hi = nums.size() - 1, result = -1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] == target) {
                result = mid;
                if (isLeft) hi = mid - 1;
                else lo = mid + 1;
            } else if (nums[mid] < target) {
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
        return result;
    }
};
```

**Complexity**: Time O(log n), Space O(1).

---

### Problem 3: Search in Rotated Sorted Array (LC 33) — Medium

**Problem**: A sorted array has been rotated at an unknown pivot. Given the rotated array and a target, return the index of the target or -1. All elements are unique.

**Link**: [https://leetcode.com/problems/search-in-rotated-sorted-array/](https://leetcode.com/problems/search-in-rotated-sorted-array/)

**Intuition**: At each step, one half of the array (left or right of mid) is always sorted. Determine which half is sorted by comparing `nums[lo]` with `nums[mid]`. Then check if the target falls within the sorted half — if yes, search there; otherwise, search the other half.

**Python:**

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = lo + (hi - lo) // 2
            if nums[mid] == target:
                return mid
            if nums[lo] <= nums[mid]:               # left half is sorted
                if nums[lo] <= target < nums[mid]:
                    hi = mid - 1
                else:
                    lo = mid + 1
            else:                                    # right half is sorted
                if nums[mid] < target <= nums[hi]:
                    lo = mid + 1
                else:
                    hi = mid - 1
        return -1
```

**C++:**

```cpp
class Solution {
public:
    int search(vector<int>& nums, int target) {
        int lo = 0, hi = nums.size() - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] == target) return mid;

            if (nums[lo] <= nums[mid]) {             // left half sorted
                if (nums[lo] <= target && target < nums[mid])
                    hi = mid - 1;
                else
                    lo = mid + 1;
            } else {                                  // right half sorted
                if (nums[mid] < target && target <= nums[hi])
                    lo = mid + 1;
                else
                    hi = mid - 1;
            }
        }
        return -1;
    }
};
```

**Complexity**: Time O(log n), Space O(1).

---

### Problem 4: Find Peak Element (LC 162) — Medium

**Problem**: Given an integer array where `nums[i] ≠ nums[i+1]`, find a peak element (strictly greater than its neighbors) and return its index. The array may have multiple peaks; return any one. Assume `nums[-1] = nums[n] = -∞`.

**Link**: [https://leetcode.com/problems/find-peak-element/](https://leetcode.com/problems/find-peak-element/)

**Intuition**: Binary search works here because if `nums[mid] < nums[mid + 1]`, then a peak must exist to the right (the values are rising, and the boundary is -∞). Conversely, if `nums[mid] > nums[mid + 1]`, a peak exists at mid or to its left. This guarantees convergence toward a peak.

**Python:**

```python
class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        lo, hi = 0, len(nums) - 1
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if nums[mid] < nums[mid + 1]:
                lo = mid + 1        # peak is to the right
            else:
                hi = mid            # peak is at mid or to the left
        return lo
```

**C++:**

```cpp
class Solution {
public:
    int findPeakElement(vector<int>& nums) {
        int lo = 0, hi = nums.size() - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] < nums[mid + 1])
                lo = mid + 1;       // peak is to the right
            else
                hi = mid;           // peak is at mid or left
        }
        return lo;
    }
};
```

**Complexity**: Time O(log n), Space O(1).

---

### Problem 5: Median of Two Sorted Arrays (LC 4) — Hard

**Problem**: Given two sorted arrays `nums1` (size m) and `nums2` (size n), find the median of the combined sorted array. The overall runtime must be O(log(m + n)).

**Link**: [https://leetcode.com/problems/median-of-two-sorted-arrays/](https://leetcode.com/problems/median-of-two-sorted-arrays/)

**Intuition**: Binary search on the shorter array to find a partition that splits the combined elements into two equal halves. At a valid partition, every element on the left side is ≤ every element on the right side. We binary search the partition position `i` in the smaller array; the corresponding partition `j` in the larger array is `(m + n + 1) // 2 - i`. We check the cross-boundary conditions: `maxLeft1 <= minRight2` and `maxLeft2 <= minRight1`.

**Python:**

```python
class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1
        m, n = len(nums1), len(nums2)
        half = (m + n + 1) // 2

        lo, hi = 0, m
        while lo <= hi:
            i = lo + (hi - lo) // 2     # partition in nums1
            j = half - i                 # partition in nums2

            left1  = nums1[i - 1] if i > 0 else float('-inf')
            right1 = nums1[i]     if i < m else float('inf')
            left2  = nums2[j - 1] if j > 0 else float('-inf')
            right2 = nums2[j]     if j < n else float('inf')

            if left1 <= right2 and left2 <= right1:
                if (m + n) % 2 == 1:
                    return max(left1, left2)
                return (max(left1, left2) + min(right1, right2)) / 2.0
            elif left1 > right2:
                hi = i - 1
            else:
                lo = i + 1

        return 0.0
```

**C++:**

```cpp
class Solution {
public:
    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
        if (nums1.size() > nums2.size()) swap(nums1, nums2);
        int m = nums1.size(), n = nums2.size();
        int half = (m + n + 1) / 2;

        int lo = 0, hi = m;
        while (lo <= hi) {
            int i = lo + (hi - lo) / 2;
            int j = half - i;

            int left1  = (i > 0) ? nums1[i - 1] : INT_MIN;
            int right1 = (i < m) ? nums1[i]     : INT_MAX;
            int left2  = (j > 0) ? nums2[j - 1] : INT_MIN;
            int right2 = (j < n) ? nums2[j]     : INT_MAX;

            if (left1 <= right2 && left2 <= right1) {
                if ((m + n) % 2 == 1)
                    return max(left1, left2);
                return (max(left1, left2) + min(right1, right2)) / 2.0;
            } else if (left1 > right2) {
                hi = i - 1;
            } else {
                lo = i + 1;
            }
        }
        return 0.0;
    }
};
```

**Complexity**: Time O(log(min(m, n))), Space O(1).

---

## 12. Top K Elements

### Overview

Finding the **top or bottom K elements** from a collection is a recurring theme in coding interviews. The optimal approach uses a **heap of size K**:

- **Top K largest** → use a **min-heap** of size K. The smallest element among the K largest sits at the heap's top. When a new element arrives that is larger than the heap's top, replace it. At the end, the heap contains exactly the K largest elements.
- **Top K smallest** → use a **max-heap** of size K (same logic, inverted).

This gives **O(n log k)** time, which is better than sorting at O(n log n) when k ≪ n. For the special case of finding exactly the Kth element (not all K elements), **Quick Select** achieves O(n) average time.

### When to Use

- Kth largest or smallest element
- K most frequent elements
- K closest points to origin (or any reference)
- Top K frequent words
- Sorting characters by frequency
- Any problem asking for a ranking of top/bottom K items

### Template Code

**Min-heap of size K for finding K largest elements:**

**Python:**

```python
import heapq

def top_k_largest(nums, k):
    heap = []                          # min-heap
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)        # evict the smallest
    return heap                        # contains K largest elements
```

**C++:**

```cpp
#include <queue>
#include <vector>

vector<int> topKLargest(vector<int>& nums, int k) {
    // min-heap (default priority_queue is max-heap, so use greater<>)
    priority_queue<int, vector<int>, greater<int>> minHeap;
    for (int num : nums) {
        minHeap.push(num);
        if ((int)minHeap.size() > k)
            minHeap.pop();             // evict the smallest
    }
    vector<int> result;
    while (!minHeap.empty()) {
        result.push_back(minHeap.top());
        minHeap.pop();
    }
    return result;
}
```

### Variations

| Variation | Heap Type | Description |
|-----------|-----------|-------------|
| **K largest** | Min-heap of size K | Evict smallest when heap exceeds K; remaining are K largest |
| **K smallest** | Max-heap of size K | Evict largest when heap exceeds K; remaining are K smallest |
| **K most frequent** | Min-heap + HashMap | Count frequencies, then push `(freq, element)` into min-heap of size K |
| **Quick Select** | — (partitioning) | Average O(n) for finding exact Kth element; worst case O(n²) |

### Common Mistakes

1. **Using wrong heap type** — For K largest, use a min-heap (not max-heap). The min-heap lets you efficiently evict the smallest of the K candidates.
2. **Not maintaining heap size at K** — Pop after every push when size exceeds K; don't let the heap grow to size n.
3. **Forgetting to handle ties** — When multiple elements have the same value/frequency, define a consistent tiebreaker (e.g., lexicographic order for words).
4. **Using sort when heap is more efficient** — Sorting is O(n log n); a heap of size K is O(n log k). When k ≪ n, the heap approach is significantly faster.

### Related Patterns

- **Two Heaps** — uses a max-heap and min-heap together (e.g., running median)
- **Sorting** — an alternative approach when k ≈ n
- **Quick Select** — O(n) average for finding the exact Kth element

---

### Example Problems

### Problem 1: Kth Largest Element in an Array (LC 215) — Medium

**Problem**: Given an integer array `nums` and an integer `k`, return the kth largest element in the array (not the kth distinct element).

**Link**: [https://leetcode.com/problems/kth-largest-element-in-an-array/](https://leetcode.com/problems/kth-largest-element-in-an-array/)

**Intuition**: Maintain a min-heap of size K. Iterate through the array: push each element, and pop whenever the heap exceeds size K. After processing all elements, the heap's top is the Kth largest. Alternatively, Quick Select can find it in O(n) average time by partitioning around a pivot (like quicksort but only recursing into the relevant half).

**Python (Heap):**

```python
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        heap = []
        for num in nums:
            heapq.heappush(heap, num)
            if len(heap) > k:
                heapq.heappop(heap)
        return heap[0]
```

**Python (Quick Select):**

```python
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        target = len(nums) - k  # index in sorted order

        def quickselect(lo, hi):
            pivot = nums[hi]
            store = lo
            for i in range(lo, hi):
                if nums[i] <= pivot:
                    nums[store], nums[i] = nums[i], nums[store]
                    store += 1
            nums[store], nums[hi] = nums[hi], nums[store]

            if store == target:
                return nums[store]
            elif store < target:
                return quickselect(store + 1, hi)
            else:
                return quickselect(lo, store - 1)

        return quickselect(0, len(nums) - 1)
```

**C++ (Heap):**

```cpp
class Solution {
public:
    int findKthLargest(vector<int>& nums, int k) {
        priority_queue<int, vector<int>, greater<int>> minHeap;
        for (int num : nums) {
            minHeap.push(num);
            if ((int)minHeap.size() > k)
                minHeap.pop();
        }
        return minHeap.top();
    }
};
```

**C++ (Quick Select):**

```cpp
class Solution {
public:
    int findKthLargest(vector<int>& nums, int k) {
        int target = nums.size() - k;
        return quickselect(nums, 0, nums.size() - 1, target);
    }

private:
    int quickselect(vector<int>& nums, int lo, int hi, int target) {
        int pivot = nums[hi], store = lo;
        for (int i = lo; i < hi; ++i) {
            if (nums[i] <= pivot)
                swap(nums[store++], nums[i]);
        }
        swap(nums[store], nums[hi]);

        if (store == target) return nums[store];
        if (store < target) return quickselect(nums, store + 1, hi, target);
        return quickselect(nums, lo, store - 1, target);
    }
};
```

**Complexity**: Heap — Time O(n log k), Space O(k). Quick Select — Time O(n) average / O(n²) worst, Space O(1).

---

### Problem 2: Top K Frequent Elements (LC 347) — Medium

**Problem**: Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. The answer is guaranteed to be unique.

**Link**: [https://leetcode.com/problems/top-k-frequent-elements/](https://leetcode.com/problems/top-k-frequent-elements/)

**Intuition**: First, count the frequency of each element using a hash map. Then use a min-heap of size K keyed by frequency: iterate through the frequency map, push each `(frequency, element)` pair, and pop when the heap exceeds K. The heap retains the K elements with the highest frequencies.

**Python:**

```python
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        freq = Counter(nums)
        heap = []
        for num, count in freq.items():
            heapq.heappush(heap, (count, num))
            if len(heap) > k:
                heapq.heappop(heap)
        return [num for count, num in heap]
```

**C++:**

```cpp
class Solution {
public:
    vector<int> topKFrequent(vector<int>& nums, int k) {
        unordered_map<int, int> freq;
        for (int n : nums) freq[n]++;

        // min-heap of (frequency, element)
        using pii = pair<int, int>;
        priority_queue<pii, vector<pii>, greater<pii>> minHeap;

        for (auto& [num, count] : freq) {
            minHeap.push({count, num});
            if ((int)minHeap.size() > k)
                minHeap.pop();
        }

        vector<int> result;
        while (!minHeap.empty()) {
            result.push_back(minHeap.top().second);
            minHeap.pop();
        }
        return result;
    }
};
```

**Complexity**: Time O(n log k), Space O(n) for the frequency map.

---

### Problem 3: K Closest Points to Origin (LC 973) — Medium

**Problem**: Given an array of points on the X-Y plane, return the `k` closest points to the origin `(0, 0)`. Distance is Euclidean (but we can compare squared distances to avoid floating point).

**Link**: [https://leetcode.com/problems/k-closest-points-to-origin/](https://leetcode.com/problems/k-closest-points-to-origin/)

**Intuition**: Use a max-heap of size K. For "K smallest distances," we want to evict the farthest point whenever the heap exceeds K — so the heap root should be the maximum distance. Push `(-distance, point)` into a min-heap (to simulate a max-heap in Python) or use a max-heap directly in C++.

**Python:**

```python
class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        heap = []
        for x, y in points:
            dist = x * x + y * y
            heapq.heappush(heap, (-dist, x, y))   # negate for max-heap behavior
            if len(heap) > k:
                heapq.heappop(heap)
        return [[x, y] for _, x, y in heap]
```

**C++:**

```cpp
class Solution {
public:
    vector<vector<int>> kClosest(vector<vector<int>>& points, int k) {
        // max-heap by distance
        auto cmp = [](const pair<int, int>& a, const pair<int, int>& b) {
            return (a.first * a.first + a.second * a.second)
                 < (b.first * b.first + b.second * b.second);
        };
        priority_queue<pair<int,int>, vector<pair<int,int>>, decltype(cmp)> maxHeap(cmp);

        for (auto& p : points) {
            maxHeap.push({p[0], p[1]});
            if ((int)maxHeap.size() > k)
                maxHeap.pop();
        }

        vector<vector<int>> result;
        while (!maxHeap.empty()) {
            auto [x, y] = maxHeap.top();
            maxHeap.pop();
            result.push_back({x, y});
        }
        return result;
    }
};
```

**Complexity**: Time O(n log k), Space O(k).

---

### Problem 4: Sort Characters By Frequency (LC 451) — Medium

**Problem**: Given a string `s`, sort it in decreasing order based on the frequency of the characters. Characters with the same frequency can be in any order.

**Link**: [https://leetcode.com/problems/sort-characters-by-frequency/](https://leetcode.com/problems/sort-characters-by-frequency/)

**Intuition**: Count character frequencies with a hash map, then use a max-heap to extract characters in decreasing frequency order. Alternatively, bucket sort by frequency is O(n). With a heap approach: push all `(frequency, char)` pairs into a max-heap, then pop in order and build the result string by repeating each character by its frequency.

**Python:**

```python
class Solution:
    def frequencySort(self, s: str) -> str:
        freq = Counter(s)
        # max-heap: negate frequency for min-heap trick
        heap = [(-count, ch) for ch, count in freq.items()]
        heapq.heapify(heap)

        result = []
        while heap:
            count, ch = heapq.heappop(heap)
            result.append(ch * (-count))
        return ''.join(result)
```

**C++:**

```cpp
class Solution {
public:
    string frequencySort(string s) {
        unordered_map<char, int> freq;
        for (char c : s) freq[c]++;

        // max-heap of (frequency, character)
        priority_queue<pair<int, char>> maxHeap;
        for (auto& [ch, count] : freq)
            maxHeap.push({count, ch});

        string result;
        while (!maxHeap.empty()) {
            auto [count, ch] = maxHeap.top();
            maxHeap.pop();
            result.append(count, ch);
        }
        return result;
    }
};
```

**Complexity**: Time O(n log k) where k is the number of distinct characters (at most 62 for alphanumeric), Space O(n).

---

### Problem 5: Find Median from Data Stream (LC 295) — Hard

**Problem**: Design a data structure that supports adding integers from a data stream and finding the median of all elements seen so far. Implement `addNum(int num)` and `findMedian() -> float`.

**Link**: [https://leetcode.com/problems/find-median-from-data-stream/](https://leetcode.com/problems/find-median-from-data-stream/)

**Intuition**: Maintain two heaps that split the data into a lower half and an upper half:
- **Max-heap** (`lo`): stores the smaller half, with the largest of the small elements at the top.
- **Min-heap** (`hi`): stores the larger half, with the smallest of the large elements at the top.

Balance rule: `lo` can have at most one more element than `hi`. When adding a number, push to `lo` first (via `hi` to ensure ordering), then rebalance. The median is either the top of `lo` (odd total) or the average of the tops of both heaps (even total).

*(Cross-reference: this is the Two Heaps pattern — Pattern 9.)*

**Python:**

```python
class MedianFinder:
    def __init__(self):
        self.lo = []    # max-heap (negate values)
        self.hi = []    # min-heap

    def addNum(self, num: int) -> None:
        heapq.heappush(self.lo, -num)
        # move the largest from lo to hi
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        # rebalance: lo should have >= elements as hi
        if len(self.lo) < len(self.hi):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self) -> float:
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2.0
```

**C++:**

```cpp
class MedianFinder {
    priority_queue<int> lo;                                // max-heap
    priority_queue<int, vector<int>, greater<int>> hi;     // min-heap

public:
    void addNum(int num) {
        lo.push(num);
        hi.push(lo.top());
        lo.pop();
        if (lo.size() < hi.size()) {
            lo.push(hi.top());
            hi.pop();
        }
    }

    double findMedian() {
        if (lo.size() > hi.size())
            return lo.top();
        return (lo.top() + hi.top()) / 2.0;
    }
};
```

**Complexity**: `addNum` — Time O(log n), Space O(n). `findMedian` — Time O(1).

---
## 13. K-way Merge

### Overview

K-way Merge efficiently merges **K sorted lists/arrays** into one sorted output. The core idea uses a **min-heap of size K**, initialized with the first element from each list. At each step, pop the smallest element from the heap, add it to the result, and push the next element from the same list that the popped element came from. Because the heap never exceeds size K, each push/pop is O(log K), and we process N total elements, giving **O(N log K)** time where N is the total number of elements across all lists.

**Key Insight**: A brute-force merge of K lists would require repeatedly scanning all K lists to find the minimum, costing O(N·K). The min-heap reduces each "find minimum" step from O(K) to O(log K).

### When to Use

| Signal | Example |
|---|---|
| Merge K sorted sequences | Merge K sorted linked lists, merge K sorted arrays |
| Kth smallest across sorted collections | Kth smallest element in a sorted matrix, K pairs with smallest sums |
| Smallest range covering K sources | Smallest range that includes at least one element from each of K sorted lists |
| Merge K sorted streams | External sort merge phase, merging log files by timestamp |

### Template Code

**Python**

```python
import heapq
from typing import List

def k_way_merge(lists: List[List[int]]) -> List[int]:
    min_heap = []  # (value, list_index, element_index)
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(min_heap, (lst[0], i, 0))

    result = []
    while min_heap:
        val, list_idx, elem_idx = heapq.heappop(min_heap)
        result.append(val)
        next_idx = elem_idx + 1
        if next_idx < len(lists[list_idx]):
            heapq.heappush(min_heap, (lists[list_idx][next_idx], list_idx, next_idx))

    return result
```

**C++**

```cpp
#include <vector>
#include <queue>
using namespace std;

vector<int> kWayMerge(vector<vector<int>>& lists) {
    // (value, list_index, element_index) — use greater<> for min-heap
    using Entry = tuple<int, int, int>;
    priority_queue<Entry, vector<Entry>, greater<Entry>> minHeap;

    for (int i = 0; i < (int)lists.size(); i++) {
        if (!lists[i].empty()) {
            minHeap.push({lists[i][0], i, 0});
        }
    }

    vector<int> result;
    while (!minHeap.empty()) {
        auto [val, listIdx, elemIdx] = minHeap.top();
        minHeap.pop();
        result.push_back(val);
        int nextIdx = elemIdx + 1;
        if (nextIdx < (int)lists[listIdx].size()) {
            minHeap.push({lists[listIdx][nextIdx], listIdx, nextIdx});
        }
    }
    return result;
}
```

### Variations

| Variation | Key Difference |
|---|---|
| **Merge K sorted linked lists** | Heap stores `(node.val, index, node)` — advance via `node.next` instead of array index |
| **Merge K sorted arrays** | Classic template above — advance via element index |
| **Kth smallest in sorted matrix** | Treat each row (or column) as a sorted list; stop after K pops |
| **Smallest range covering K lists** | Maintain a min-heap and track the current max; shrink the window by advancing the min |
| **K pairs with smallest sums** | Heap of `(nums1[i]+nums2[j], i, j)` — lazy expansion avoids generating all pairs |

### Common Mistakes

1. **Not initializing the heap with the first element from every list** — missing a list means its elements never enter the merge.
2. **Forgetting to check if a list is exhausted** before pushing the next element — causes index-out-of-bounds.
3. **Not handling empty lists** — pushing from an empty list crashes; always guard with `if lst:` or `if !list.empty()`.
4. **Wrong comparison for custom objects in the heap** — in C++ the default `priority_queue` is a max-heap; use `greater<>` for min-heap. In Python, `heapq` is always a min-heap but tuples must be comparable.
5. **Using O(N·K) approach** when K is large — always consider the heap-based O(N log K) approach.

### Related Patterns

- **Top K Elements** — also uses heaps, but for finding largest/smallest K items from one collection.
- **Two Heaps** — uses a max-heap and min-heap together (e.g., median finding).
- **Sorting** — K-way merge is the merge phase of external merge sort.

---

### Example Problems

---

### Problem 1: Merge Two Sorted Lists (LC 21) — Medium

**Problem Statement**: Given the heads of two sorted linked lists, merge them into one sorted linked list and return the head. The merged list should be made by splicing together the nodes of the two input lists.

**LeetCode Link**: [https://leetcode.com/problems/merge-two-sorted-lists/](https://leetcode.com/problems/merge-two-sorted-lists/)

**Intuition**: This is the base case of K-way merge with K=2. Use a dummy head and a tail pointer. At each step, compare the current nodes of both lists and attach the smaller one to the tail. When one list is exhausted, attach the remainder of the other. No heap is needed for K=2 — a simple two-pointer merge suffices.

**Python Solution**:

```python
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        tail = dummy

        while list1 and list2:
            if list1.val <= list2.val:
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next

        tail.next = list1 if list1 else list2
        return dummy.next
```

**C++ Solution**:

```cpp
struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x) : val(x), next(nullptr) {}
};

class Solution {
public:
    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
        ListNode dummy(0);
        ListNode* tail = &dummy;

        while (list1 && list2) {
            if (list1->val <= list2->val) {
                tail->next = list1;
                list1 = list1->next;
            } else {
                tail->next = list2;
                list2 = list2->next;
            }
            tail = tail->next;
        }

        tail->next = list1 ? list1 : list2;
        return dummy.next;
    }
};
```

**Complexity**:
- **Time**: O(n + m) where n and m are the lengths of the two lists.
- **Space**: O(1) — only pointer manipulation, no extra storage.

---

### Problem 2: Merge K Sorted Lists (LC 23) — Hard

**Problem Statement**: Given an array of K linked lists, each sorted in ascending order, merge all the linked lists into one sorted linked list and return it.

**LeetCode Link**: [https://leetcode.com/problems/merge-k-sorted-lists/](https://leetcode.com/problems/merge-k-sorted-lists/)

**Intuition**: This is the classic K-way merge problem. Initialize a min-heap with the head node of each non-empty list. Repeatedly pop the smallest node, attach it to the result, and push that node's `next` (if it exists) back into the heap. The heap always holds at most K elements, so each operation is O(log K). We process all N nodes, giving O(N log K) total.

**Python Solution**:

```python
import heapq
from typing import List, Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        min_heap = []
        for i, node in enumerate(lists):
            if node:
                heapq.heappush(min_heap, (node.val, i, node))

        dummy = ListNode(0)
        tail = dummy

        while min_heap:
            val, idx, node = heapq.heappop(min_heap)
            tail.next = node
            tail = tail.next
            if node.next:
                heapq.heappush(min_heap, (node.next.val, idx, node.next))

        return dummy.next
```

> **Note**: The `idx` (list index) is included in the heap tuple to break ties when two nodes have the same value. Without it, Python would try to compare `ListNode` objects, which are not comparable.

**C++ Solution**:

```cpp
#include <vector>
#include <queue>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x) : val(x), next(nullptr) {}
};

class Solution {
public:
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        auto cmp = [](ListNode* a, ListNode* b) {
            return a->val > b->val;  // min-heap
        };
        priority_queue<ListNode*, vector<ListNode*>, decltype(cmp)> minHeap(cmp);

        for (auto* node : lists) {
            if (node) minHeap.push(node);
        }

        ListNode dummy(0);
        ListNode* tail = &dummy;

        while (!minHeap.empty()) {
            ListNode* node = minHeap.top();
            minHeap.pop();
            tail->next = node;
            tail = tail->next;
            if (node->next) {
                minHeap.push(node->next);
            }
        }

        return dummy.next;
    }
};
```

**Complexity**:
- **Time**: O(N log K) where N is the total number of nodes across all lists and K is the number of lists.
- **Space**: O(K) for the heap.

---

### Problem 3: Kth Smallest Element in a Sorted Matrix (LC 378) — Medium

**Problem Statement**: Given an `n x n` matrix where each row and each column is sorted in ascending order, return the kth smallest element in the matrix.

**LeetCode Link**: [https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/)

**Intuition**: Treat each row as a sorted list and apply K-way merge, but stop after the kth pop — no need to merge everything. Initialize the heap with the first element of each row. Pop the smallest and push the next element from the same row. The kth popped element is the answer. Alternatively, binary search on the value range [matrix\[0\]\[0\], matrix\[n-1\]\[n-1\]] and count elements ≤ mid using the sorted structure.

**Python Solution (Heap approach)**:

```python
import heapq
from typing import List

class Solution:
    def kthSmallest(self, matrix: List[List[int]], k: int) -> int:
        n = len(matrix)
        min_heap = []
        for i in range(min(n, k)):  # at most k rows matter
            heapq.heappush(min_heap, (matrix[i][0], i, 0))

        result = 0
        for _ in range(k):
            result, row, col = heapq.heappop(min_heap)
            if col + 1 < n:
                heapq.heappush(min_heap, (matrix[row][col + 1], row, col + 1))

        return result
```

**Python Solution (Binary Search approach)**:

```python
from typing import List

class Solution:
    def kthSmallest(self, matrix: List[List[int]], k: int) -> int:
        n = len(matrix)

        def count_less_equal(mid: int) -> int:
            count = 0
            row, col = n - 1, 0  # start from bottom-left
            while row >= 0 and col < n:
                if matrix[row][col] <= mid:
                    count += row + 1  # all elements above in this column qualify
                    col += 1
                else:
                    row -= 1
            return count

        lo, hi = matrix[0][0], matrix[n - 1][n - 1]
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if count_less_equal(mid) < k:
                lo = mid + 1
            else:
                hi = mid
        return lo
```

**C++ Solution (Heap approach)**:

```cpp
#include <vector>
#include <queue>
using namespace std;

class Solution {
public:
    int kthSmallest(vector<vector<int>>& matrix, int k) {
        int n = matrix.size();
        using Entry = tuple<int, int, int>;  // (value, row, col)
        priority_queue<Entry, vector<Entry>, greater<Entry>> minHeap;

        for (int i = 0; i < min(n, k); i++) {
            minHeap.push({matrix[i][0], i, 0});
        }

        int result = 0;
        for (int i = 0; i < k; i++) {
            auto [val, row, col] = minHeap.top();
            minHeap.pop();
            result = val;
            if (col + 1 < n) {
                minHeap.push({matrix[row][col + 1], row, col + 1});
            }
        }
        return result;
    }
};
```

**C++ Solution (Binary Search approach)**:

```cpp
#include <vector>
using namespace std;

class Solution {
public:
    int kthSmallest(vector<vector<int>>& matrix, int k) {
        int n = matrix.size();
        int lo = matrix[0][0], hi = matrix[n - 1][n - 1];

        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            int count = countLessEqual(matrix, mid, n);
            if (count < k)
                lo = mid + 1;
            else
                hi = mid;
        }
        return lo;
    }

private:
    int countLessEqual(vector<vector<int>>& matrix, int mid, int n) {
        int count = 0;
        int row = n - 1, col = 0;
        while (row >= 0 && col < n) {
            if (matrix[row][col] <= mid) {
                count += row + 1;
                col++;
            } else {
                row--;
            }
        }
        return count;
    }
};
```

**Complexity**:
- **Heap approach**: Time O(K log K), Space O(K) — we do at most K pops and the heap holds at most K elements.
- **Binary Search approach**: Time O(N · log(max − min)), Space O(1) — each binary search step does an O(N) scan.

---

### Problem 4: Find K Pairs with Smallest Sums (LC 373) — Medium

**Problem Statement**: Given two sorted arrays `nums1` and `nums2`, and an integer `k`, find the `k` pairs `(u, v)` with the smallest sums where `u` is from `nums1` and `v` is from `nums2`. Return a list of pairs in sorted order of their sums.

**LeetCode Link**: [https://leetcode.com/problems/find-k-pairs-with-smallest-sums/](https://leetcode.com/problems/find-k-pairs-with-smallest-sums/)

**Intuition**: Think of it as K sorted lists where list `i` contains pairs `(nums1[i], nums2[0]), (nums1[i], nums2[1]), ...` — each list is sorted by sum because `nums2` is sorted. Initialize the heap with `(nums1[i] + nums2[0], i, 0)` for each `i` (up to min(k, len(nums1))). Pop the smallest sum, record the pair, and push the next pair from the same row `(nums1[i] + nums2[j+1], i, j+1)`. Stop after K pops.

**Python Solution**:

```python
import heapq
from typing import List

class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        if not nums1 or not nums2:
            return []

        min_heap = []
        for i in range(min(k, len(nums1))):
            heapq.heappush(min_heap, (nums1[i] + nums2[0], i, 0))

        result = []
        while min_heap and len(result) < k:
            total, i, j = heapq.heappop(min_heap)
            result.append([nums1[i], nums2[j]])
            if j + 1 < len(nums2):
                heapq.heappush(min_heap, (nums1[i] + nums2[j + 1], i, j + 1))

        return result
```

**C++ Solution**:

```cpp
#include <vector>
#include <queue>
using namespace std;

class Solution {
public:
    vector<vector<int>> kSmallestPairs(vector<int>& nums1, vector<int>& nums2, int k) {
        if (nums1.empty() || nums2.empty()) return {};

        using Entry = tuple<int, int, int>;  // (sum, idx_in_nums1, idx_in_nums2)
        priority_queue<Entry, vector<Entry>, greater<Entry>> minHeap;

        for (int i = 0; i < min(k, (int)nums1.size()); i++) {
            minHeap.push({nums1[i] + nums2[0], i, 0});
        }

        vector<vector<int>> result;
        while (!minHeap.empty() && (int)result.size() < k) {
            auto [sum, i, j] = minHeap.top();
            minHeap.pop();
            result.push_back({nums1[i], nums2[j]});
            if (j + 1 < (int)nums2.size()) {
                minHeap.push({nums1[i] + nums2[j + 1], i, j + 1});
            }
        }
        return result;
    }
};
```

**Complexity**:
- **Time**: O(K log K) — we do at most K pops and K pushes, each O(log K) since the heap never exceeds size K.
- **Space**: O(K) for the heap and result list.

---

### Problem 5: Smallest Range Covering Elements from K Lists (LC 632) — Hard

**Problem Statement**: Given `K` sorted lists of integers, find the smallest range `[a, b]` such that at least one element from each list is included in the range. Return the range as a list `[a, b]`.

**LeetCode Link**: [https://leetcode.com/problems/smallest-range-covering-elements-from-k-lists/](https://leetcode.com/problems/smallest-range-covering-elements-from-k-lists/)

**Intuition**: Initialize a min-heap with the first element from each list, and track the current maximum across all elements in the heap. The range is `[heap_min, current_max]`. This range always covers at least one element from every list because the heap contains exactly one element per list. To shrink the range, pop the minimum (which increases the lower bound) and push the next element from that same list (which might increase the max). Update the best range whenever `current_max - heap_min` is smaller than the previous best. Stop when any list is exhausted (we can no longer cover all K lists).

**Python Solution**:

```python
import heapq
from typing import List
import math

class Solution:
    def smallestRange(self, nums: List[List[int]]) -> List[int]:
        min_heap = []
        current_max = -math.inf

        for i, lst in enumerate(nums):
            heapq.heappush(min_heap, (lst[0], i, 0))
            current_max = max(current_max, lst[0])

        best_range = [-math.inf, math.inf]

        while True:
            current_min, list_idx, elem_idx = heapq.heappop(min_heap)

            if current_max - current_min < best_range[1] - best_range[0]:
                best_range = [current_min, current_max]

            next_idx = elem_idx + 1
            if next_idx >= len(nums[list_idx]):
                break  # one list exhausted — can't cover all K lists anymore

            next_val = nums[list_idx][next_idx]
            heapq.heappush(min_heap, (next_val, list_idx, next_idx))
            current_max = max(current_max, next_val)

        return best_range
```

**C++ Solution**:

```cpp
#include <vector>
#include <queue>
#include <climits>
using namespace std;

class Solution {
public:
    vector<int> smallestRange(vector<vector<int>>& nums) {
        using Entry = tuple<int, int, int>;  // (value, list_index, element_index)
        priority_queue<Entry, vector<Entry>, greater<Entry>> minHeap;

        int currentMax = INT_MIN;
        for (int i = 0; i < (int)nums.size(); i++) {
            minHeap.push({nums[i][0], i, 0});
            currentMax = max(currentMax, nums[i][0]);
        }

        int bestLeft = 0, bestRight = INT_MAX;

        while (true) {
            auto [currentMin, listIdx, elemIdx] = minHeap.top();
            minHeap.pop();

            if (currentMax - currentMin < bestRight - bestLeft) {
                bestLeft = currentMin;
                bestRight = currentMax;
            }

            int nextIdx = elemIdx + 1;
            if (nextIdx >= (int)nums[listIdx].size()) {
                break;
            }

            int nextVal = nums[listIdx][nextIdx];
            minHeap.push({nextVal, listIdx, nextIdx});
            currentMax = max(currentMax, nextVal);
        }

        return {bestLeft, bestRight};
    }
};
```

**Complexity**:
- **Time**: O(N log K) where N is the total number of elements across all K lists. Each element is pushed and popped from the heap at most once, and each heap operation is O(log K).
- **Space**: O(K) for the heap which holds exactly one element per list.

---
## 14. Topological Sort

### Overview

Topological Sort produces a **linear ordering** of vertices in a Directed Acyclic Graph (DAG) such that for every directed edge `(u, v)`, vertex `u` appears before vertex `v` in the ordering. Two main algorithmic approaches exist:

| Approach | Mechanism | Key Data Structures |
|---|---|---|
| **Kahn's Algorithm (BFS)** | Repeatedly remove zero-in-degree nodes | Queue + in-degree array |
| **DFS-based** | Reverse post-order traversal | Recursion stack + visited set |

**Core Invariant**: Every node is processed only after all its prerequisites have been processed.

**Applications**: Course scheduling, build systems (Make/Gradle), dependency resolution (package managers), spreadsheet cell evaluation order, instruction scheduling in compilers.

### When to Use

- Course scheduling with prerequisites
- Build order / dependency resolution
- Detecting cycles in a directed graph
- Task ordering with constraints
- Alien dictionary (deriving character order)
- Longest/shortest path in a DAG
- Parallel task scheduling with dependency constraints

### Template Code

**Kahn's Algorithm (BFS-based) — Python**

```python
from collections import deque, defaultdict

def topological_sort(num_nodes, edges):
    """
    num_nodes: number of vertices (0-indexed)
    edges: list of [u, v] meaning u -> v (u must come before v)
    Returns: valid topological ordering, or empty list if cycle exists
    """
    adj = defaultdict(list)
    in_degree = [0] * num_nodes

    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1

    queue = deque()
    for node in range(num_nodes):
        if in_degree[node] == 0:
            queue.append(node)

    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != num_nodes:
        return []  # cycle detected
    return order
```

**Kahn's Algorithm (BFS-based) — C++**

```cpp
#include <vector>
#include <queue>
using namespace std;

vector<int> topologicalSort(int numNodes, vector<vector<int>>& edges) {
    vector<vector<int>> adj(numNodes);
    vector<int> inDegree(numNodes, 0);

    for (auto& e : edges) {
        adj[e[0]].push_back(e[1]);
        inDegree[e[1]]++;
    }

    queue<int> q;
    for (int i = 0; i < numNodes; i++) {
        if (inDegree[i] == 0) q.push(i);
    }

    vector<int> order;
    while (!q.empty()) {
        int node = q.front(); q.pop();
        order.push_back(node);
        for (int nei : adj[node]) {
            if (--inDegree[nei] == 0) q.push(nei);
        }
    }

    if ((int)order.size() != numNodes) return {}; // cycle
    return order;
}
```

### Variations

| Variation | Key Difference |
|---|---|
| **Kahn's (BFS)** | Queue-based, naturally detects cycles via count check |
| **DFS-based with stack** | Post-order + reverse; uses coloring (white/gray/black) for cycle detection |
| **Cycle detection** | If topological sort cannot include all nodes → cycle exists |
| **Lexicographically smallest ordering** | Replace `queue` with `min-heap` (`priority_queue` / `heapq`) |
| **Longest path / critical path in a DAG** | DP in topological order: `finish[v] = max(finish[u]) + time[v]` (Parallel Courses III) |
| **Euler path (use every edge once)** | Hierholzer: DFS emitting nodes in post-order, then reverse (Reconstruct Itinerary) |

### Common Mistakes

1. **Not detecting cycles** — If the final ordering contains fewer nodes than the total count, a cycle exists. Always verify `len(order) == num_nodes`.
2. **Building adjacency list in the wrong direction** — `[a, b]` meaning "a is prerequisite of b" means edge `a → b`, not `b → a`.
3. **Forgetting initial zero-in-degree nodes** — All nodes with `in_degree == 0` must seed the queue.
4. **Ignoring disconnected components** — The initial scan over all nodes handles this, but custom implementations sometimes miss isolated nodes.
5. **Confusing BFS topological sort with shortest path BFS** — Topological sort BFS processes by in-degree, not by distance levels.

### Related Patterns

- **BFS** — Kahn's algorithm is fundamentally BFS
- **DFS** — Alternative topological sort approach
- **Graph Algorithms** — Shortest path in DAG, critical path analysis

### Example Problems

#### Problem 1: Course Schedule (LC 207) — Medium

**Problem**: There are `numCourses` courses labeled `0` to `numCourses - 1`. You are given `prerequisites` where `prerequisites[i] = [a, b]` means you must take course `b` before course `a`. Return `true` if you can finish all courses (i.e., no cycle exists).

**Link**: [https://leetcode.com/problems/course-schedule/](https://leetcode.com/problems/course-schedule/)

**Intuition**: Model courses as nodes and prerequisites as directed edges. If a valid topological ordering exists (covers all nodes), there is no cycle and all courses can be finished. Use Kahn's algorithm — if the resulting order has fewer nodes than `numCourses`, a cycle prevents completion.

**Python Solution**:

```python
from collections import deque, defaultdict

class Solution:
    def canFinish(self, numCourses: int, prerequisites: list[list[int]]) -> bool:
        adj = defaultdict(list)
        in_degree = [0] * numCourses

        for course, prereq in prerequisites:
            adj[prereq].append(course)
            in_degree[course] += 1

        queue = deque(i for i in range(numCourses) if in_degree[i] == 0)
        count = 0

        while queue:
            node = queue.popleft()
            count += 1
            for nei in adj[node]:
                in_degree[nei] -= 1
                if in_degree[nei] == 0:
                    queue.append(nei)

        return count == numCourses
```

**C++ Solution**:

```cpp
class Solution {
public:
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
        vector<vector<int>> adj(numCourses);
        vector<int> inDeg(numCourses, 0);

        for (auto& p : prerequisites) {
            adj[p[1]].push_back(p[0]);
            inDeg[p[0]]++;
        }

        queue<int> q;
        for (int i = 0; i < numCourses; i++)
            if (inDeg[i] == 0) q.push(i);

        int count = 0;
        while (!q.empty()) {
            int node = q.front(); q.pop();
            count++;
            for (int nei : adj[node])
                if (--inDeg[nei] == 0) q.push(nei);
        }

        return count == numCourses;
    }
};
```

**Complexity**: Time `O(V + E)` — each node and edge processed once. Space `O(V + E)` — adjacency list and in-degree array.

---

#### Problem 2: Course Schedule II (LC 210) — Medium

**Problem**: Given `numCourses` and `prerequisites`, return a valid ordering in which you can take all courses. If impossible (cycle exists), return an empty array.

**Link**: [https://leetcode.com/problems/course-schedule-ii/](https://leetcode.com/problems/course-schedule-ii/)

**Intuition**: Direct application of Kahn's algorithm. Instead of just counting processed nodes, collect them into an order array. If the array length doesn't match `numCourses`, a cycle exists — return empty.

**Python Solution**:

```python
from collections import deque, defaultdict

class Solution:
    def findOrder(self, numCourses: int, prerequisites: list[list[int]]) -> list[int]:
        adj = defaultdict(list)
        in_degree = [0] * numCourses

        for course, prereq in prerequisites:
            adj[prereq].append(course)
            in_degree[course] += 1

        queue = deque(i for i in range(numCourses) if in_degree[i] == 0)
        order = []

        while queue:
            node = queue.popleft()
            order.append(node)
            for nei in adj[node]:
                in_degree[nei] -= 1
                if in_degree[nei] == 0:
                    queue.append(nei)

        return order if len(order) == numCourses else []
```

**C++ Solution**:

```cpp
class Solution {
public:
    vector<int> findOrder(int numCourses, vector<vector<int>>& prerequisites) {
        vector<vector<int>> adj(numCourses);
        vector<int> inDeg(numCourses, 0);

        for (auto& p : prerequisites) {
            adj[p[1]].push_back(p[0]);
            inDeg[p[0]]++;
        }

        queue<int> q;
        for (int i = 0; i < numCourses; i++)
            if (inDeg[i] == 0) q.push(i);

        vector<int> order;
        while (!q.empty()) {
            int node = q.front(); q.pop();
            order.push_back(node);
            for (int nei : adj[node])
                if (--inDeg[nei] == 0) q.push(nei);
        }

        return (int)order.size() == numCourses ? order : vector<int>{};
    }
};
```

**Complexity**: Time `O(V + E)`. Space `O(V + E)`.

---

#### Problem 3: Course Schedule IV (LC 1462) — Medium

**Problem**: Given `numCourses`, `prerequisites`, and `queries` where `queries[j] = [u, v]`, answer whether course `u` is a (direct or indirect) prerequisite of course `v`.

**Link**: [https://leetcode.com/problems/course-schedule-iv/](https://leetcode.com/problems/course-schedule-iv/)

**Intuition**: Process nodes in topological order. For each node, maintain a set of all its ancestors (transitive prerequisites). When processing node `u`, for each neighbor `v`, propagate `u`'s prerequisite set plus `u` itself to `v`. After processing, answering each query is an `O(1)` set lookup.

**Python Solution**:

```python
from collections import deque, defaultdict

class Solution:
    def checkIfPrerequisite(self, numCourses: int, prerequisites: list[list[int]],
                            queries: list[list[int]]) -> list[bool]:
        adj = defaultdict(list)
        in_degree = [0] * numCourses
        reachable = [set() for _ in range(numCourses)]

        for u, v in prerequisites:
            adj[u].append(v)
            in_degree[v] += 1

        queue = deque(i for i in range(numCourses) if in_degree[i] == 0)

        while queue:
            node = queue.popleft()
            for nei in adj[node]:
                reachable[nei].add(node)
                reachable[nei] |= reachable[node]
                in_degree[nei] -= 1
                if in_degree[nei] == 0:
                    queue.append(nei)

        return [u in reachable[v] for u, v in queries]
```

**C++ Solution**:

```cpp
class Solution {
public:
    vector<bool> checkIfPrerequisite(int numCourses, vector<vector<int>>& prerequisites,
                                     vector<vector<int>>& queries) {
        vector<vector<int>> adj(numCourses);
        vector<int> inDeg(numCourses, 0);
        // isPrereq[i][j] = true means i is a prerequisite of j
        vector<vector<bool>> isPrereq(numCourses, vector<bool>(numCourses, false));

        for (auto& p : prerequisites) {
            adj[p[0]].push_back(p[1]);
            inDeg[p[1]]++;
        }

        queue<int> q;
        for (int i = 0; i < numCourses; i++)
            if (inDeg[i] == 0) q.push(i);

        while (!q.empty()) {
            int node = q.front(); q.pop();
            for (int nei : adj[node]) {
                isPrereq[node][nei] = true;
                for (int i = 0; i < numCourses; i++)
                    if (isPrereq[i][node]) isPrereq[i][nei] = true;
                if (--inDeg[nei] == 0) q.push(nei);
            }
        }

        vector<bool> result;
        for (auto& qr : queries)
            result.push_back(isPrereq[qr[0]][qr[1]]);
        return result;
    }
};
```

**Complexity**: Time `O(V³ + Q)` — propagating reachability takes `O(V)` per edge in the worst case, with `O(V²)` edges possible; each query is `O(1)`. Space `O(V²)` — reachability matrix/sets.

---

#### Problem 4: Alien Dictionary (LC 269) — Hard

**Problem**: Given a list of words sorted lexicographically by the rules of an alien language, derive the order of characters. Return a string of the unique characters in the alien language sorted in the alien order. If no valid ordering exists, return `""`.

**Link**: [https://leetcode.com/problems/alien-dictionary/](https://leetcode.com/problems/alien-dictionary/)

**Intuition**: Compare adjacent words character by character. The first position where they differ gives us a directed edge: `word1[i] → word2[i]` (meaning `word1[i]` comes before `word2[i]`). After extracting all such edges, run topological sort on the character graph. Edge case: if a longer word appears before its prefix (e.g., `"abc"` before `"ab"`), the ordering is invalid.

**Python Solution**:

```python
from collections import deque, defaultdict

class Solution:
    def alienOrder(self, words: list[str]) -> str:
        adj = defaultdict(set)
        in_degree = {c: 0 for word in words for c in word}

        for i in range(len(words) - 1):
            w1, w2 = words[i], words[i + 1]
            min_len = min(len(w1), len(w2))

            if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
                return ""  # invalid: prefix comes after longer word

            for j in range(min_len):
                if w1[j] != w2[j]:
                    if w2[j] not in adj[w1[j]]:
                        adj[w1[j]].add(w2[j])
                        in_degree[w2[j]] += 1
                    break

        queue = deque(c for c in in_degree if in_degree[c] == 0)
        result = []

        while queue:
            c = queue.popleft()
            result.append(c)
            for nei in adj[c]:
                in_degree[nei] -= 1
                if in_degree[nei] == 0:
                    queue.append(nei)

        if len(result) != len(in_degree):
            return ""  # cycle detected

        return "".join(result)
```

**C++ Solution**:

```cpp
class Solution {
public:
    string alienOrder(vector<string>& words) {
        unordered_map<char, unordered_set<char>> adj;
        unordered_map<char, int> inDeg;

        for (auto& w : words)
            for (char c : w)
                inDeg[c] = 0;  // register all characters

        for (int i = 0; i < (int)words.size() - 1; i++) {
            string& w1 = words[i];
            string& w2 = words[i + 1];
            int minLen = min(w1.size(), w2.size());

            if (w1.size() > w2.size() && w1.substr(0, minLen) == w2.substr(0, minLen))
                return "";

            for (int j = 0; j < minLen; j++) {
                if (w1[j] != w2[j]) {
                    if (!adj[w1[j]].count(w2[j])) {
                        adj[w1[j]].insert(w2[j]);
                        inDeg[w2[j]]++;
                    }
                    break;
                }
            }
        }

        queue<char> q;
        for (auto& [c, deg] : inDeg)
            if (deg == 0) q.push(c);

        string result;
        while (!q.empty()) {
            char c = q.front(); q.pop();
            result += c;
            for (char nei : adj[c])
                if (--inDeg[nei] == 0) q.push(nei);
        }

        return result.size() == inDeg.size() ? result : "";
    }
};
```

**Complexity**: Time `O(C)` where `C` is total number of characters across all words (each character and edge is processed once). Space `O(U + E)` where `U` is unique characters and `E` is number of edges.

---

#### Problem 5: Parallel Courses III (LC 2050) — Hard

**Problem**: You are given `n` courses and `relations` where `relations[j] = [prev, next]` means course `prev` must be completed before course `next`. Each course `i` takes `time[i]` months. Courses can run in parallel. Return the minimum number of months to complete all courses.

**Link**: [https://leetcode.com/problems/parallel-courses-iii/](https://leetcode.com/problems/parallel-courses-iii/)

**Intuition**: This is the **longest path in a DAG** problem, equivalent to finding the critical path. Process nodes in topological order. For each node, track the earliest time it can start (which is the maximum finish time among all its prerequisites). The answer is the maximum finish time across all nodes. `finish[node] = earliest_start[node] + time[node]`.

**Python Solution**:

```python
from collections import deque, defaultdict

class Solution:
    def minimumTime(self, n: int, relations: list[list[int]], time: list[int]) -> int:
        adj = defaultdict(list)
        in_degree = [0] * (n + 1)

        for prev, nxt in relations:
            adj[prev].append(nxt)
            in_degree[nxt] += 1

        dist = [0] * (n + 1)  # earliest finish time for each course
        queue = deque()

        for i in range(1, n + 1):
            if in_degree[i] == 0:
                queue.append(i)
                dist[i] = time[i - 1]

        while queue:
            node = queue.popleft()
            for nei in adj[node]:
                dist[nei] = max(dist[nei], dist[node] + time[nei - 1])
                in_degree[nei] -= 1
                if in_degree[nei] == 0:
                    queue.append(nei)

        return max(dist)
```

**C++ Solution**:

```cpp
class Solution {
public:
    int minimumTime(int n, vector<vector<int>>& relations, vector<int>& time) {
        vector<vector<int>> adj(n + 1);
        vector<int> inDeg(n + 1, 0);
        vector<int> dist(n + 1, 0);

        for (auto& r : relations) {
            adj[r[0]].push_back(r[1]);
            inDeg[r[1]]++;
        }

        queue<int> q;
        for (int i = 1; i <= n; i++) {
            if (inDeg[i] == 0) {
                q.push(i);
                dist[i] = time[i - 1];
            }
        }

        while (!q.empty()) {
            int node = q.front(); q.pop();
            for (int nei : adj[node]) {
                dist[nei] = max(dist[nei], dist[node] + time[nei - 1]);
                if (--inDeg[nei] == 0) q.push(nei);
            }
        }

        return *max_element(dist.begin(), dist.end());
    }
};
```

**Complexity**: Time `O(V + E)` — standard topological sort. Space `O(V + E)`.

---

#### Problem 6: Reconstruct Itinerary (LC 332) — Hard

**Problem**: `tickets[i] = [from, to]`. Use **every ticket exactly once**, starting from `"JFK"`. If several itineraries are valid, return the lexicographically smallest. At least one valid itinerary is guaranteed.

**Link**: [https://leetcode.com/problems/reconstruct-itinerary/](https://leetcode.com/problems/reconstruct-itinerary/)

**Intuition**: "Use every edge exactly once" is an **Euler path**, not a topological order, but the algorithm has the same shape as DFS-based topological sort: emit a node in **post-order** and reverse at the end. That is **Hierholzer's algorithm**. Walk greedily along the smallest unused ticket. When the current airport has no tickets left, it must be the end of whatever remains, so append it to the route and back up. Reversing the post-order gives the itinerary.

Why greedy "smallest first" is not enough on its own: with `JFK→KUL`, `JFK→NRT`, `NRT→JFK`, the smallest first move is `KUL`, which is a dead end with tickets still unused. Hierholzer handles it: `KUL` is emitted first (so it ends up **last**), the DFS backs up to `JFK`, takes `NRT → JFK`, and the reversed post-order is `JFK, NRT, JFK, KUL`.

**Python Solution**:

```python
from collections import defaultdict

class Solution:
    def findItinerary(self, tickets: list[list[str]]) -> list[str]:
        graph = defaultdict(list)
        for src, dst in sorted(tickets, reverse=True):
            graph[src].append(dst)            # reverse-sorted, so pop() yields the smallest
        route, stack = [], ["JFK"]
        while stack:
            if graph[stack[-1]]:
                stack.append(graph[stack[-1]].pop())   # follow the smallest unused ticket
            else:
                route.append(stack.pop())              # dead end: emit in post-order
        return route[::-1]
```

**C++ Solution**:

```cpp
#include <algorithm>
#include <functional>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;

class Solution {
public:
    vector<string> findItinerary(vector<vector<string>>& tickets) {
        sort(tickets.begin(), tickets.end(), greater<vector<string>>());   // reverse lexicographic
        unordered_map<string, vector<string>> graph;
        for (const auto& t : tickets) graph[t[0]].push_back(t[1]);          // back() = smallest
        vector<string> route, stack{"JFK"};
        while (!stack.empty()) {
            vector<string>& out = graph[stack.back()];
            if (!out.empty()) {
                string next = out.back();
                out.pop_back();
                stack.push_back(next);
            } else {
                route.push_back(stack.back());
                stack.pop_back();
            }
        }
        reverse(route.begin(), route.end());
        return route;
    }
};
```

**Complexity**: Time O(E log E) for sorting, O(E) for the walk. Space O(E). Euler-path theory (existence conditions, undirected version) is in [DSA Fundamentals: Euler Paths and Circuits](DSA_Fundamentals.md#euler-paths-and-circuits-hierholzers-algorithm).

---

### Interview Q&A

**Q1.** Kahn's algorithm or DFS-based topological sort: which do you choose?

Both are O(V + E). **Kahn's** (in-degree queue) detects cycles naturally (fewer than V nodes output), gives a level structure for free (process the queue layer by layer to get "semesters" or parallel stages), and makes it easy to get the lexicographically smallest order (swap the queue for a min-heap). **DFS post-order** is shorter when you already have a DFS, and it is the basis for SCC algorithms and Hierholzer; cycle detection needs three colours (unvisited, on the stack, done), since a back edge to an "on the stack" node is a cycle. Kahn's is iterative, so it avoids recursion-depth limits on long chains.

**Q2.** When does an Euler path exist, and why is Hierholzer O(E)?

**Directed**: all vertices with edges are in one weakly connected component, and either every vertex has in-degree = out-degree (Euler circuit) or exactly one vertex has `out - in = 1` (the start) and one has `in - out = 1` (the end). **Undirected**: connected, with 0 (circuit) or 2 (path, between those two) odd-degree vertices. Hierholzer consumes each edge exactly once (it is popped from the adjacency list and never revisited), and each vertex push or pop corresponds to an edge, so the walk is O(V + E). The lexicographic requirement in LC 332 only adds sorting.

**Q3.** How does topological sort relate to performance analysis of GPU workloads?

A GPU application is a DAG of kernels, memory copies, and synchronisation events across streams (or an explicit HIP/CUDA graph). The longest path through that DAG, weighted by duration, is the **critical path**, as in Parallel Courses III: it lower-bounds the end-to-end time no matter how many streams run concurrently. Speeding up a kernel that is not on the critical path does not reduce wall time. Profiling tools that show a timeline let you read this off visually; computing it is a topological sort plus a DP of `finish = max(finish of dependencies) + duration`.

**Q4.** You need the order in which to rebuild targets after one source file changes. How?

Build systems (Make, Ninja, CMake-generated graphs) keep a dependency DAG. Mark the changed node dirty, find everything reachable from it along "is used by" edges (BFS or DFS), and topologically sort only that subgraph. Kahn's levels give batches that can be built in parallel. Cycles are configuration errors, so report the cycle itself (from the DFS stack when you hit a node that is still "on the stack") rather than just "cycle detected".

---

## 15. Monotonic Stack / Queue

### Overview

A **monotonic stack** maintains elements in a strictly increasing or decreasing order from bottom to top. When a new element arrives, all elements that violate the monotonic property are popped before the new element is pushed. This structure efficiently answers "next greater element" and "next smaller element" queries in **O(n)** total time because each element is pushed and popped **at most once**.

A **monotonic deque** extends this concept to support efficient sliding window minimum/maximum queries, maintaining the deque invariant while also removing expired elements from the front.

| Structure | Maintained Order (bottom → top) | Solves |
|---|---|---|
| **Decreasing stack** | Large → Small | Next **greater** element |
| **Increasing stack** | Small → Large | Next **smaller** element |
| **Monotonic deque** | Depends on variant | Sliding window min/max |

**Key Insight**: The amortized time is `O(n)` because across the entire iteration, each element enters and leaves the stack/deque exactly once.

### When to Use

- Next greater / next smaller element problems
- Previous greater / previous smaller element problems
- Largest rectangle in histogram
- Daily temperatures / stock span
- Sliding window maximum or minimum
- Trapping rain water
- Sum of subarray minimums/maximums
- Removing digits to make smallest/largest number

### Template Code

**Monotonic Decreasing Stack (Next Greater Element) — Python**

```python
def next_greater_element(nums):
    n = len(nums)
    result = [-1] * n
    stack = []  # stores indices; values at indices are in decreasing order

    for i in range(n):
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)

    return result
```

**Monotonic Decreasing Stack (Next Greater Element) — C++**

```cpp
#include <vector>
#include <stack>
using namespace std;

vector<int> nextGreaterElement(vector<int>& nums) {
    int n = nums.size();
    vector<int> result(n, -1);
    stack<int> stk; // indices with decreasing values

    for (int i = 0; i < n; i++) {
        while (!stk.empty() && nums[i] > nums[stk.top()]) {
            result[stk.top()] = nums[i];
            stk.pop();
        }
        stk.push(i);
    }

    return result;
}
```

**Monotonic Deque (Sliding Window Maximum) — Python**

```python
from collections import deque

def sliding_window_max(nums, k):
    dq = deque()  # stores indices; values at indices are in decreasing order
    result = []

    for i in range(len(nums)):
        # remove indices outside the window
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # maintain decreasing order
        while dq and nums[i] >= nums[dq[-1]]:
            dq.pop()

        dq.append(i)

        if i >= k - 1:
            result.append(nums[dq[0]])

    return result
```

**Monotonic Deque (Sliding Window Maximum) — C++**

```cpp
#include <vector>
#include <deque>
using namespace std;

vector<int> slidingWindowMax(vector<int>& nums, int k) {
    deque<int> dq;
    vector<int> result;

    for (int i = 0; i < (int)nums.size(); i++) {
        while (!dq.empty() && dq.front() < i - k + 1)
            dq.pop_front();

        while (!dq.empty() && nums[i] >= nums[dq.back()])
            dq.pop_back();

        dq.push_back(i);

        if (i >= k - 1)
            result.push_back(nums[dq.front()]);
    }

    return result;
}
```

### Variations

| Variation | Stack Order (bottom→top) | Typical Use |
|---|---|---|
| **Monotonic increasing stack** | Small → Large | Next **smaller** element |
| **Monotonic decreasing stack** | Large → Small | Next **greater** element |
| **Monotonic deque (max)** | Decreasing | Sliding window maximum |
| **Monotonic deque (min)** | Increasing | Sliding window minimum |
| **Circular array** | Iterate `2n` times with `i % n` indexing | Circular next greater element |

### Common Mistakes

1. **Confusing increasing vs decreasing** — A "monotonic decreasing stack" has the largest element at the bottom and pops when a new element is **greater**. This finds the **next greater** element. Double-check the comparison direction.
2. **Storing values instead of indices** — Most problems need indices (for distance calculations, result placement). Always store indices and look up values via `nums[stack[-1]]`.
3. **Forgetting leftover elements** — After the loop, elements remaining in the stack have no next greater/smaller element. They should stay as `-1` (or handle per problem requirements).
4. **Off-by-one with circular arrays** — When iterating `2n` times, only record results for `i < n` and index elements with `i % n`.
5. **Incorrect inequality (strict vs non-strict)** — Using `>=` vs `>` in the while-loop condition matters. `>=` ensures strict monotonicity; `>` allows equal elements to coexist.

### Related Patterns

- **Sliding Window** — Monotonic deque is the optimal data structure for sliding window min/max
- **Stack** — Monotonic stack is a constrained stack usage
- **Two Pointers** — Some histogram problems combine both approaches

### Example Problems

#### Problem 1: Next Greater Element I (LC 496) — Easy

**Problem**: You are given two arrays `nums1` and `nums2` where `nums1` is a subset of `nums2`. For each element in `nums1`, find the next greater element in `nums2` (i.e., the first element to the right that is larger). Return `-1` if no such element exists.

**Link**: [https://leetcode.com/problems/next-greater-element-i/](https://leetcode.com/problems/next-greater-element-i/)

**Intuition**: First, compute the next greater element for every element in `nums2` using a monotonic decreasing stack and store results in a hash map. Then, for each element in `nums1`, look up the answer in `O(1)`.

**Python Solution**:

```python
class Solution:
    def nextGreaterElement(self, nums1: list[int], nums2: list[int]) -> list[int]:
        nge = {}
        stack = []

        for num in nums2:
            while stack and num > stack[-1]:
                nge[stack.pop()] = num
            stack.append(num)

        return [nge.get(num, -1) for num in nums1]
```

**C++ Solution**:

```cpp
class Solution {
public:
    vector<int> nextGreaterElement(vector<int>& nums1, vector<int>& nums2) {
        unordered_map<int, int> nge;
        stack<int> stk;

        for (int num : nums2) {
            while (!stk.empty() && num > stk.top()) {
                nge[stk.top()] = num;
                stk.pop();
            }
            stk.push(num);
        }

        vector<int> result;
        for (int num : nums1)
            result.push_back(nge.count(num) ? nge[num] : -1);

        return result;
    }
};
```

**Complexity**: Time `O(n + m)` where `n = len(nums1)`, `m = len(nums2)`. Space `O(m)` for the hash map and stack.

---

#### Problem 2: Daily Temperatures (LC 739) — Medium

**Problem**: Given an array `temperatures`, return an array `answer` such that `answer[i]` is the number of days you have to wait after the `i`-th day to get a warmer temperature. If there is no future day with a warmer temperature, set `answer[i] = 0`.

**Link**: [https://leetcode.com/problems/daily-temperatures/](https://leetcode.com/problems/daily-temperatures/)

**Intuition**: Use a monotonic decreasing stack of indices. When we encounter a temperature warmer than the temperature at the top index, we pop and compute the distance `i - stack.pop()`. This gives the number of days waited.

**Python Solution**:

```python
class Solution:
    def dailyTemperatures(self, temperatures: list[int]) -> list[int]:
        n = len(temperatures)
        answer = [0] * n
        stack = []  # indices with decreasing temperatures

        for i in range(n):
            while stack and temperatures[i] > temperatures[stack[-1]]:
                prev = stack.pop()
                answer[prev] = i - prev
            stack.append(i)

        return answer
```

**C++ Solution**:

```cpp
class Solution {
public:
    vector<int> dailyTemperatures(vector<int>& temperatures) {
        int n = temperatures.size();
        vector<int> answer(n, 0);
        stack<int> stk;

        for (int i = 0; i < n; i++) {
            while (!stk.empty() && temperatures[i] > temperatures[stk.top()]) {
                int prev = stk.top(); stk.pop();
                answer[prev] = i - prev;
            }
            stk.push(i);
        }

        return answer;
    }
};
```

**Complexity**: Time `O(n)` — each index is pushed and popped at most once. Space `O(n)` for the stack.

---

#### Problem 3: Next Greater Element II (LC 503) — Medium

**Problem**: Given a circular integer array `nums`, return the next greater number for every element. The next greater number of `nums[i]` is the first greater number traversing circularly. If none exists, return `-1`.

**Link**: [https://leetcode.com/problems/next-greater-element-ii/](https://leetcode.com/problems/next-greater-element-ii/)

**Intuition**: To handle the circular nature, iterate through the array **twice** (total `2n` iterations) using `i % n` for indexing. Use a monotonic decreasing stack of indices. Only record results when popped indices are `< n` (first pass). The second pass ensures elements that wrap around are covered.

**Python Solution**:

```python
class Solution:
    def nextGreaterElements(self, nums: list[int]) -> list[int]:
        n = len(nums)
        result = [-1] * n
        stack = []

        for i in range(2 * n):
            while stack and nums[i % n] > nums[stack[-1]]:
                result[stack.pop()] = nums[i % n]
            if i < n:
                stack.append(i)

        return result
```

**C++ Solution**:

```cpp
class Solution {
public:
    vector<int> nextGreaterElements(vector<int>& nums) {
        int n = nums.size();
        vector<int> result(n, -1);
        stack<int> stk;

        for (int i = 0; i < 2 * n; i++) {
            while (!stk.empty() && nums[i % n] > nums[stk.top()]) {
                result[stk.top()] = nums[i % n];
                stk.pop();
            }
            if (i < n) stk.push(i);
        }

        return result;
    }
};
```

**Complexity**: Time `O(n)` — `2n` iterations, each element pushed/popped at most once. Space `O(n)` for the stack and result.

---

#### Problem 4: Largest Rectangle in Histogram (LC 84) — Hard

**Problem**: Given an array `heights` representing a histogram where bar width is `1`, find the area of the largest rectangle that can be formed within the histogram.

**Link**: [https://leetcode.com/problems/largest-rectangle-in-histogram/](https://leetcode.com/problems/largest-rectangle-in-histogram/)

**Intuition**: Use a **monotonic increasing stack** of indices. For each bar, we want to know how far left and right it can extend (i.e., the nearest shorter bars on both sides). When we pop a bar from the stack because the current bar is shorter, the popped bar's rectangle extends from the new stack top (left boundary) to the current index (right boundary). Append a sentinel height `0` to flush remaining bars.

**Python Solution**:

```python
class Solution:
    def largestRectangleArea(self, heights: list[int]) -> int:
        stack = []
        max_area = 0
        heights.append(0)  # sentinel to flush the stack

        for i in range(len(heights)):
            while stack and heights[i] < heights[stack[-1]]:
                h = heights[stack.pop()]
                w = i if not stack else i - stack[-1] - 1
                max_area = max(max_area, h * w)
            stack.append(i)

        heights.pop()  # restore original array
        return max_area
```

**C++ Solution**:

```cpp
class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        stack<int> stk;
        int maxArea = 0;
        heights.push_back(0); // sentinel

        for (int i = 0; i < (int)heights.size(); i++) {
            while (!stk.empty() && heights[i] < heights[stk.top()]) {
                int h = heights[stk.top()]; stk.pop();
                int w = stk.empty() ? i : i - stk.top() - 1;
                maxArea = max(maxArea, h * w);
            }
            stk.push(i);
        }

        heights.pop_back(); // restore
        return maxArea;
    }
};
```

**Complexity**: Time `O(n)` — each bar is pushed and popped at most once. Space `O(n)` for the stack.

---

#### Problem 5: Sliding Window Maximum (LC 239) — Hard

**Problem**: Given an integer array `nums` and a sliding window of size `k` moving from left to right, return the maximum value in each window position.

**Link**: [https://leetcode.com/problems/sliding-window-maximum/](https://leetcode.com/problems/sliding-window-maximum/)

**Intuition**: Use a **monotonic decreasing deque** storing indices. The front of the deque always holds the index of the current window's maximum. Two maintenance operations: (1) Remove from the front if the index falls outside the window. (2) Remove from the back while the new element is greater than or equal to the back element (they can never be a future window maximum). After the first `k-1` elements, start recording `nums[dq[0]]` as the window maximum.

**Python Solution**:

```python
from collections import deque

class Solution:
    def maxSlidingWindow(self, nums: list[int], k: int) -> list[int]:
        dq = deque()  # indices, values in decreasing order
        result = []

        for i in range(len(nums)):
            while dq and dq[0] < i - k + 1:
                dq.popleft()

            while dq and nums[i] >= nums[dq[-1]]:
                dq.pop()

            dq.append(i)

            if i >= k - 1:
                result.append(nums[dq[0]])

        return result
```

**C++ Solution**:

```cpp
class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        deque<int> dq;
        vector<int> result;

        for (int i = 0; i < (int)nums.size(); i++) {
            while (!dq.empty() && dq.front() < i - k + 1)
                dq.pop_front();

            while (!dq.empty() && nums[i] >= nums[dq.back()])
                dq.pop_back();

            dq.push_back(i);

            if (i >= k - 1)
                result.push_back(nums[dq.front()]);
        }

        return result;
    }
};
```

**Complexity**: Time `O(n)` — each element enters and leaves the deque at most once. Space `O(k)` for the deque.

---
## 16. Union Find (Disjoint Set)

### Overview

Union-Find (also called Disjoint Set Union, DSU) manages a collection of disjoint sets with two primary operations:

- **Find**: Determine which set an element belongs to (returns the root/representative of the set).
- **Union**: Merge two sets into one.

With **path compression** and **union by rank**, both operations run in nearly O(1) amortized time — formally O(α(n)), where α is the inverse Ackermann function, which grows so slowly it is effectively constant for all practical input sizes.

Union-Find is the go-to structure for connected component problems, cycle detection in undirected graphs, and dynamic connectivity queries.

### When to Use

- Finding connected components in an undirected graph
- Detecting cycles in undirected graphs
- Kruskal's Minimum Spanning Tree algorithm
- Number of islands (union-find alternative to BFS/DFS)
- Accounts merge / grouping by equivalence
- Redundant connections / finding the extra edge
- Dynamic connectivity (online edge additions)

### Template Code

**Python**

```python
class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # path compression
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        self.components -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)
```

**C++**

```cpp
class UnionFind {
    vector<int> parent, rank_;
    int components;
public:
    UnionFind(int n) : parent(n), rank_(n, 0), components(n) {
        iota(parent.begin(), parent.end(), 0);
    }

    int find(int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]]; // path compression
            x = parent[x];
        }
        return x;
    }

    bool unite(int x, int y) {
        int rx = find(x), ry = find(y);
        if (rx == ry) return false;
        if (rank_[rx] < rank_[ry]) swap(rx, ry);
        parent[ry] = rx;
        if (rank_[rx] == rank_[ry]) rank_[rx]++;
        components--;
        return true;
    }

    bool connected(int x, int y) {
        return find(x) == find(y);
    }

    int count() const { return components; }
};
```

### Variations

| Variation | Description |
|---|---|
| **Basic (no optimizations)** | Naive parent array, find walks to root — O(n) worst case |
| **Path compression only** | Flattens tree during find — amortized O(log n) |
| **Union by rank/size** | Always attach smaller tree under larger — O(log n) without compression |
| **Rank + path compression** | Both optimizations — O(α(n)) amortized |
| **Weighted union-find** | Stores relative weights on edges; used in problems like "Evaluate Division" |
| **Parity union-find** | Stores XOR parity to the parent; detects odd cycles online (Is Graph Bipartite, Possible Bipartition) |
| **Union neighbours together** | All neighbours of `u` must share a set; `u` joining that set means an odd cycle (Is Graph Bipartite) |

### Common Mistakes

1. **Not implementing path compression** — degrades find to O(n) in the worst case.
2. **Union by rank vs union by size confusion** — rank tracks tree height (increment only when equal), size tracks node count (always add).
3. **Forgetting to decrement component count** after a successful union.
4. **Not checking if already in the same set** before performing union (leads to incorrect component counts).
5. **Off-by-one on node indexing** — problems may use 1-indexed nodes while your DSU is 0-indexed.

### Related Patterns

- BFS / DFS (alternative approaches for connected components)
- Graph Algorithms (Kruskal's MST)

### Example Problems

#### Problem 1: Number of Provinces (LC 547) — Medium

**Link**: [https://leetcode.com/problems/number-of-provinces/](https://leetcode.com/problems/number-of-provinces/)

**Statement**: Given an `n x n` adjacency matrix `isConnected` where `isConnected[i][j] = 1` means city `i` and city `j` are directly connected, return the total number of provinces (connected components).

**Intuition**: Each city starts as its own component. For every edge `(i, j)` where `isConnected[i][j] == 1`, union cities `i` and `j`. The final component count is the answer.

**Python Solution**

```python
class Solution:
    def findCircleNum(self, isConnected: list[list[int]]) -> int:
        n = len(isConnected)
        uf = UnionFind(n)
        for i in range(n):
            for j in range(i + 1, n):
                if isConnected[i][j] == 1:
                    uf.union(i, j)
        return uf.components
```

**C++ Solution**

```cpp
class Solution {
public:
    int findCircleNum(vector<vector<int>>& isConnected) {
        int n = isConnected.size();
        UnionFind uf(n);
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++)
                if (isConnected[i][j] == 1)
                    uf.unite(i, j);
        return uf.count();
    }
};
```

**Complexity**: Time O(n² · α(n)), Space O(n).

---

#### Problem 2: Redundant Connection (LC 684) — Medium

**Link**: [https://leetcode.com/problems/redundant-connection/](https://leetcode.com/problems/redundant-connection/)

**Statement**: Given a graph that started as a tree with `n` nodes and had one extra edge added, find the edge that can be removed so the result is a tree. If there are multiple answers, return the one that occurs last in the input.

**Intuition**: Process edges one by one. The first edge that connects two already-connected nodes creates the cycle — that's our redundant edge. Since we process in order, the last such edge found is the answer (the problem guarantees exactly one extra edge, so only one union will fail).

**Python Solution**

```python
class Solution:
    def findRedundantConnection(self, edges: list[list[int]]) -> list[int]:
        n = len(edges)
        uf = UnionFind(n + 1)  # 1-indexed nodes
        for u, v in edges:
            if not uf.union(u, v):
                return [u, v]
        return []
```

**C++ Solution**

```cpp
class Solution {
public:
    vector<int> findRedundantConnection(vector<vector<int>>& edges) {
        int n = edges.size();
        UnionFind uf(n + 1); // 1-indexed
        for (auto& e : edges) {
            if (!uf.unite(e[0], e[1]))
                return {e[0], e[1]};
        }
        return {};
    }
};
```

**Complexity**: Time O(n · α(n)), Space O(n).

---

#### Problem 3: Accounts Merge (LC 721) — Medium

**Link**: [https://leetcode.com/problems/accounts-merge/](https://leetcode.com/problems/accounts-merge/)

**Statement**: Given a list of accounts where each account is `[name, email1, email2, ...]`, merge accounts that share at least one common email. Return merged accounts with emails sorted.

**Intuition**: Map each email to a unique integer ID. For each account, union all emails in that account together (union the first email's ID with every subsequent email's ID). After all unions, group emails by their root representative, then reconstruct sorted results.

**Python Solution**

```python
from collections import defaultdict

class Solution:
    def accountsMerge(self, accounts: list[list[str]]) -> list[list[str]]:
        email_to_id = {}
        email_to_name = {}
        idx = 0

        for account in accounts:
            name = account[0]
            for email in account[1:]:
                if email not in email_to_id:
                    email_to_id[email] = idx
                    idx += 1
                email_to_name[email] = name

        uf = UnionFind(idx)
        for account in accounts:
            first_id = email_to_id[account[1]]
            for email in account[2:]:
                uf.union(first_id, email_to_id[email])

        groups = defaultdict(list)
        for email, eid in email_to_id.items():
            groups[uf.find(eid)].append(email)

        result = []
        for root, emails in groups.items():
            emails.sort()
            name = email_to_name[emails[0]]
            result.append([name] + emails)
        return result
```

**C++ Solution**

```cpp
class Solution {
public:
    vector<vector<string>> accountsMerge(vector<vector<string>>& accounts) {
        unordered_map<string, int> emailToId;
        unordered_map<string, string> emailToName;
        int idx = 0;

        for (auto& acc : accounts) {
            string& name = acc[0];
            for (int i = 1; i < acc.size(); i++) {
                if (emailToId.find(acc[i]) == emailToId.end())
                    emailToId[acc[i]] = idx++;
                emailToName[acc[i]] = name;
            }
        }

        UnionFind uf(idx);
        for (auto& acc : accounts) {
            int firstId = emailToId[acc[1]];
            for (int i = 2; i < acc.size(); i++)
                uf.unite(firstId, emailToId[acc[i]]);
        }

        unordered_map<int, vector<string>> groups;
        for (auto& [email, eid] : emailToId)
            groups[uf.find(eid)].push_back(email);

        vector<vector<string>> result;
        for (auto& [root, emails] : groups) {
            sort(emails.begin(), emails.end());
            string name = emailToName[emails[0]];
            vector<string> merged = {name};
            merged.insert(merged.end(), emails.begin(), emails.end());
            result.push_back(merged);
        }
        return result;
    }
};
```

**Complexity**: Time O(n · α(n) + n log n) where n is total number of emails (sorting dominates), Space O(n).

---

#### Problem 4: Number of Islands (LC 200) — Medium

**Link**: [https://leetcode.com/problems/number-of-islands/](https://leetcode.com/problems/number-of-islands/)

**Statement**: Given an `m x n` 2D grid of `'1'`s (land) and `'0'`s (water), count the number of islands. An island is surrounded by water and formed by connecting adjacent lands horizontally or vertically.

**Intuition**: Flatten the 2D grid to 1D indices. Initialize a union-find where only land cells are active. For each land cell, union it with its right and down neighbors if they are also land. The number of remaining components among land cells is the answer.

**Python Solution**

```python
class Solution:
    def numIslands(self, grid: list[list[str]]) -> int:
        if not grid:
            return 0
        m, n = len(grid), len(grid[0])
        uf = UnionFind(m * n)

        water_count = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == '0':
                    water_count += 1
                else:
                    idx = i * n + j
                    if j + 1 < n and grid[i][j + 1] == '1':
                        uf.union(idx, idx + 1)
                    if i + 1 < m and grid[i + 1][j] == '1':
                        uf.union(idx, idx + n)

        return uf.components - water_count
```

**C++ Solution**

```cpp
class Solution {
public:
    int numIslands(vector<vector<char>>& grid) {
        int m = grid.size(), n = grid[0].size();
        UnionFind uf(m * n);

        int waterCount = 0;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == '0') {
                    waterCount++;
                } else {
                    int idx = i * n + j;
                    if (j + 1 < n && grid[i][j + 1] == '1')
                        uf.unite(idx, idx + 1);
                    if (i + 1 < m && grid[i + 1][j] == '1')
                        uf.unite(idx, idx + n);
                }
            }
        }
        return uf.count() - waterCount;
    }
};
```

**Complexity**: Time O(m · n · α(m · n)), Space O(m · n).

---

#### Problem 5: Swim in Rising Water (LC 778) — Hard

**Link**: [https://leetcode.com/problems/swim-in-rising-water/](https://leetcode.com/problems/swim-in-rising-water/)

**Statement**: You are given an `n x n` grid where `grid[i][j]` represents the elevation at position `(i, j)`. At time `t`, you can swim to any adjacent cell if both cells have elevation ≤ `t`. Starting at `(0, 0)`, find the minimum time to reach `(n-1, n-1)`.

**Intuition**: Collect all cells as edges sorted by `max(elevation of cell, elevation of neighbor)`. Process edges in increasing order of elevation. At each step, union the two cells. Once `(0,0)` and `(n-1,n-1)` are connected, the current elevation is the answer. This is essentially finding the minimum bottleneck path.

**Python Solution**

```python
class Solution:
    def swimInWater(self, grid: list[list[int]]) -> int:
        n = len(grid)
        edges = []
        for i in range(n):
            for j in range(n):
                idx = i * n + j
                if j + 1 < n:
                    w = max(grid[i][j], grid[i][j + 1])
                    edges.append((w, idx, idx + 1))
                if i + 1 < n:
                    w = max(grid[i][j], grid[i + 1][j])
                    edges.append((w, idx, idx + n))

        edges.sort()
        uf = UnionFind(n * n)
        for w, u, v in edges:
            uf.union(u, v)
            if uf.connected(0, n * n - 1):
                return w
        return 0
```

**C++ Solution**

```cpp
class Solution {
public:
    int swimInWater(vector<vector<int>>& grid) {
        int n = grid.size();
        vector<tuple<int,int,int>> edges;

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                int idx = i * n + j;
                if (j + 1 < n)
                    edges.push_back({max(grid[i][j], grid[i][j+1]), idx, idx + 1});
                if (i + 1 < n)
                    edges.push_back({max(grid[i][j], grid[i+1][j]), idx, idx + n});
            }
        }

        sort(edges.begin(), edges.end());
        UnionFind uf(n * n);
        for (auto& [w, u, v] : edges) {
            uf.unite(u, v);
            if (uf.connected(0, n * n - 1))
                return w;
        }
        return 0;
    }
};
```

**Complexity**: Time O(n² log n), Space O(n²).

---

#### Problem 6: Is Graph Bipartite? (LC 785) — Medium

**Problem**: `graph[u]` lists the neighbours of `u` in an undirected graph (possibly disconnected). Return `true` if the nodes can be split into two sets so that every edge goes between the sets.

**Link**: [https://leetcode.com/problems/is-graph-bipartite/](https://leetcode.com/problems/is-graph-bipartite/)

**Intuition**: A graph is bipartite exactly when it has **no odd-length cycle**. Two standard checks:

1. **BFS/DFS 2-colouring**: colour a start node 0, give every neighbour the opposite colour, and fail if an edge ever joins two nodes of the same colour. Restart from every uncoloured node, because the graph may be disconnected.
2. **Union-Find**: all neighbours of `u` must share one colour (the one opposite to `u`), so union them together. If `u` ever ends up in the same set as one of its neighbours, there is an odd cycle.

**Python Solution** (BFS colouring):

```python
from collections import deque

class Solution:
    def isBipartite(self, graph: list[list[int]]) -> bool:
        color = [-1] * len(graph)
        for start in range(len(graph)):
            if color[start] != -1:
                continue
            color[start] = 0
            q = deque([start])
            while q:
                u = q.popleft()
                for v in graph[u]:
                    if color[v] == -1:
                        color[v] = color[u] ^ 1
                        q.append(v)
                    elif color[v] == color[u]:
                        return False          # edge inside one colour class: odd cycle
        return True
```

**Python Solution** (Union-Find):

```python
class Solution:
    def isBipartite(self, graph: list[list[int]]) -> bool:
        parent = list(range(len(graph)))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]     # path halving
                x = parent[x]
            return x

        for u, nbrs in enumerate(graph):
            for v in nbrs:
                if find(u) == find(v):
                    return False
                parent[find(v)] = find(nbrs[0])   # every neighbour of u gets the same colour
        return True
```

**C++ Solution** (BFS colouring):

```cpp
#include <queue>
#include <vector>
using namespace std;

class Solution {
public:
    bool isBipartite(vector<vector<int>>& graph) {
        int n = graph.size();
        vector<int> color(n, -1);
        for (int start = 0; start < n; ++start) {
            if (color[start] != -1) continue;
            color[start] = 0;
            queue<int> q;
            q.push(start);
            while (!q.empty()) {
                int u = q.front();
                q.pop();
                for (int v : graph[u]) {
                    if (color[v] == -1) {
                        color[v] = color[u] ^ 1;
                        q.push(v);
                    } else if (color[v] == color[u]) {
                        return false;
                    }
                }
            }
        }
        return true;
    }
};
```

**Complexity**: BFS: O(V + E) time, O(V) space. Union-Find: O(E · α(V)) time, O(V) space. More on bipartite graphs and matching: [DSA Fundamentals: Bipartite Check](DSA_Fundamentals.md#bipartite-check-bfs-2-coloring).

---

### Interview Q&A

**Q1.** Edges arrive one at a time, and after each one you must say whether the graph is still bipartite. What do you use?

BFS colouring would have to recolour after every edge. Use a **parity (weighted) Union-Find**: each node stores the parity of its path to its parent, and `find` returns `(root, parity to root)` while compressing paths and accumulating parities with XOR. Adding edge `u–v` requires `parity(u) ≠ parity(v)`. If they are in different sets, union the roots with the parity that makes the constraint hold. If they are in the same set with equal parity, the new edge closes an odd cycle. Each edge costs O(α(n)) amortised. The same structure solves Possible Bipartition (LC 886) and, with multiplicative weights instead of XOR, Evaluate Division (LC 399).

**Q2.** When do you pick Union-Find over BFS/DFS for connectivity?

Union-Find wins when edges arrive **incrementally** and you query connectivity in between (online), or when you process edges in sorted order and stop at a threshold (Kruskal's MST, Swim in Rising Water). BFS/DFS is simpler for a static graph and also gives paths and distances, which Union-Find does not. Union-Find cannot delete edges. If deletions are known in advance, process the operations **in reverse** so deletions become insertions (the offline trick). Otherwise you need a dynamic-connectivity structure, which is beyond interview scope.

**Q3.** What does O(α(n)) mean in practice?

`α` is the inverse Ackermann function. It is at most 4 for every input size that could arise in practice (the threshold where it reaches 5 is a tower of exponentials), so with **both** path compression and union by rank or size, each operation is effectively constant time. With only one of the two optimisations the amortised bound is O(log n). Without either, a chain of unions can make `find` O(n). In interviews, state "amortised O(α(n)), effectively constant", and mention that path halving (`parent[x] = parent[parent[x]]`) gives the same bound without recursion.

---

## 17. Trie (Prefix Tree)

### Overview

A **Trie** (pronounced "try") is a tree-shaped data structure used for efficiently storing and searching strings by their prefixes. Each node represents a single character, and paths from the root to marked nodes represent stored words.

Key properties:

- **Insert**: Add a word character by character, creating nodes as needed — O(L).
- **Search**: Check if a complete word exists by traversing and verifying the end-of-word flag — O(L).
- **StartsWith**: Check if any word starts with a given prefix — O(L).

Where L is the length of the word/prefix. Tries excel at prefix-based queries, autocomplete systems, word validation on boards, and dictionary lookups.

### When to Use

- Autocomplete / typeahead suggestions
- Spell checker
- Prefix matching and counting
- Word search in a grid with a dictionary
- Longest common prefix
- Counting words with a given prefix
- IP routing (longest prefix match)
- Word break problems

### Template Code

**Python**

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self._find(word)
        return node is not None and node.is_end

    def startsWith(self, prefix: str) -> bool:
        return self._find(prefix) is not None

    def _find(self, prefix: str) -> TrieNode | None:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node
```

**C++**

```cpp
struct TrieNode {
    TrieNode* children[26] = {};
    bool isEnd = false;

    ~TrieNode() {
        for (auto child : children)
            delete child;
    }
};

class Trie {
    TrieNode* root;
public:
    Trie() : root(new TrieNode()) {}
    ~Trie() { delete root; }

    void insert(const string& word) {
        TrieNode* node = root;
        for (char ch : word) {
            int idx = ch - 'a';
            if (!node->children[idx])
                node->children[idx] = new TrieNode();
            node = node->children[idx];
        }
        node->isEnd = true;
    }

    bool search(const string& word) {
        TrieNode* node = find(word);
        return node && node->isEnd;
    }

    bool startsWith(const string& prefix) {
        return find(prefix) != nullptr;
    }

private:
    TrieNode* find(const string& prefix) {
        TrieNode* node = root;
        for (char ch : prefix) {
            int idx = ch - 'a';
            if (!node->children[idx]) return nullptr;
            node = node->children[idx];
        }
        return node;
    }
};
```

### Variations

| Variation | Description |
|---|---|
| **Standard trie** | HashMap or array-based children, boolean end-of-word marker |
| **Compressed trie (Radix tree)** | Merges single-child chains into one node, reducing memory |
| **Trie with wildcard search** | DFS at wildcard characters to explore all 26 branches |
| **Trie for word break** | Mark valid prefixes in the trie, use DP to check segmentation |
| **Counting trie** | Store prefix count and word count at each node for frequency queries |

### Common Mistakes

1. **Not initializing children properly** — Python dict vs fixed-size array; C++ null pointer array must be zero-initialized.
2. **Forgetting the `is_end` flag** — without it, you cannot distinguish "app" from "apple" when "apple" is stored.
3. **Confusing `search` vs `startsWith`** — `search` requires `is_end == True` at the final node; `startsWith` only checks existence of the path.
4. **Memory overhead** — each node may hold up to 26 children pointers; consider hash-map children for sparse tries.
5. **Not pruning during deletion** — if implementing delete, must clean up nodes that no longer lead to any word.

### Related Patterns

- DFS (trie traversal, word search on grid)
- Backtracking (word search with trie pruning)
- Hashing (alternative for exact match, but lacks prefix queries)

### Example Problems

#### Problem 1: Implement Trie (LC 208) — Medium

**Link**: [https://leetcode.com/problems/implement-trie-prefix-tree/](https://leetcode.com/problems/implement-trie-prefix-tree/)

**Statement**: Implement a trie with `insert`, `search`, and `startsWith` methods.

**Intuition**: This is the direct application of the template. Build the trie character by character. `search` verifies the complete path exists AND the final node is marked as end-of-word. `startsWith` only verifies the path exists.

**Python Solution**

```python
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def startsWith(self, prefix: str) -> bool:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True
```

**C++ Solution**

```cpp
class Trie {
    struct Node {
        Node* children[26] = {};
        bool isEnd = false;
    };
    Node* root;

public:
    Trie() : root(new Node()) {}

    void insert(string word) {
        Node* cur = root;
        for (char c : word) {
            int i = c - 'a';
            if (!cur->children[i])
                cur->children[i] = new Node();
            cur = cur->children[i];
        }
        cur->isEnd = true;
    }

    bool search(string word) {
        Node* cur = root;
        for (char c : word) {
            int i = c - 'a';
            if (!cur->children[i]) return false;
            cur = cur->children[i];
        }
        return cur->isEnd;
    }

    bool startsWith(string prefix) {
        Node* cur = root;
        for (char c : prefix) {
            int i = c - 'a';
            if (!cur->children[i]) return false;
            cur = cur->children[i];
        }
        return true;
    }
};
```

**Complexity**: Time O(L) per operation where L is the word/prefix length, Space O(total characters inserted × 26) for array-based or O(total characters) for hashmap-based.

---

#### Problem 2: Design Add and Search Words Data Structure (LC 211) — Medium

**Link**: [https://leetcode.com/problems/design-add-and-search-words-data-structure/](https://leetcode.com/problems/design-add-and-search-words-data-structure/)

**Statement**: Design a data structure that supports `addWord(word)` and `search(word)`. The `search` method can match `.` which represents any single letter.

**Intuition**: `addWord` is standard trie insertion. For `search`, when we encounter a `.`, we must try all 26 possible children via DFS/backtracking. For normal characters, follow the standard trie path. Return true if any branch leads to a valid end-of-word node.

**Python Solution**

```python
class WordDictionary:
    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        def dfs(node: TrieNode, i: int) -> bool:
            if i == len(word):
                return node.is_end
            ch = word[i]
            if ch == '.':
                for child in node.children.values():
                    if dfs(child, i + 1):
                        return True
                return False
            if ch not in node.children:
                return False
            return dfs(node.children[ch], i + 1)

        return dfs(self.root, 0)
```

**C++ Solution**

```cpp
class WordDictionary {
    struct Node {
        Node* children[26] = {};
        bool isEnd = false;
    };
    Node* root;

    bool dfs(Node* node, const string& word, int i) {
        if (i == word.size()) return node->isEnd;
        if (word[i] == '.') {
            for (int k = 0; k < 26; k++) {
                if (node->children[k] && dfs(node->children[k], word, i + 1))
                    return true;
            }
            return false;
        }
        int idx = word[i] - 'a';
        if (!node->children[idx]) return false;
        return dfs(node->children[idx], word, i + 1);
    }

public:
    WordDictionary() : root(new Node()) {}

    void addWord(string word) {
        Node* cur = root;
        for (char c : word) {
            int i = c - 'a';
            if (!cur->children[i])
                cur->children[i] = new Node();
            cur = cur->children[i];
        }
        cur->isEnd = true;
    }

    bool search(string word) {
        return dfs(root, word, 0);
    }
};
```

**Complexity**: Time O(L) for addWord, O(26^L) worst case for search with all dots (practically much faster), Space O(total characters × 26).

---

#### Problem 3: Replace Words (LC 648) — Medium

**Link**: [https://leetcode.com/problems/replace-words/](https://leetcode.com/problems/replace-words/)

**Statement**: Given a `dictionary` of root words and a `sentence`, replace every word in the sentence with the shortest root that is a prefix of that word. If no root is a prefix, keep the word unchanged.

**Intuition**: Insert all roots into a trie. For each word in the sentence, traverse the trie character by character. As soon as we hit a node where `is_end == True`, we've found the shortest prefix root — replace the word with the path so far. If we exhaust the word or fall off the trie, keep the original word.

**Python Solution**

```python
class Solution:
    def replaceWords(self, dictionary: list[str], sentence: str) -> str:
        trie = Trie()
        for root in dictionary:
            trie.insert(root)

        def find_root(word: str) -> str:
            node = trie.root
            for i, ch in enumerate(word):
                if ch not in node.children:
                    break
                node = node.children[ch]
                if node.is_end:
                    return word[:i + 1]
            return word

        words = sentence.split()
        return ' '.join(find_root(w) for w in words)
```

**C++ Solution**

```cpp
class Solution {
    struct Node {
        Node* children[26] = {};
        bool isEnd = false;
    };
    Node* root = new Node();

    void insert(const string& word) {
        Node* cur = root;
        for (char c : word) {
            int i = c - 'a';
            if (!cur->children[i])
                cur->children[i] = new Node();
            cur = cur->children[i];
        }
        cur->isEnd = true;
    }

    string findRoot(const string& word) {
        Node* cur = root;
        for (int i = 0; i < word.size(); i++) {
            int idx = word[i] - 'a';
            if (!cur->children[idx]) break;
            cur = cur->children[idx];
            if (cur->isEnd)
                return word.substr(0, i + 1);
        }
        return word;
    }

public:
    string replaceWords(vector<string>& dictionary, string sentence) {
        for (auto& w : dictionary) insert(w);

        istringstream iss(sentence);
        string word, result;
        while (iss >> word) {
            if (!result.empty()) result += ' ';
            result += findRoot(word);
        }
        return result;
    }
};
```

**Complexity**: Time O(D·L + W·L) where D is dictionary size, W is number of words in sentence, L is average word length, Space O(D·L) for the trie.

---

#### Problem 4: Word Search II (LC 212) — Hard

**Link**: [https://leetcode.com/problems/word-search-ii/](https://leetcode.com/problems/word-search-ii/)

**Statement**: Given an `m x n` board of characters and a list of words, find all words that can be formed by sequentially adjacent cells (horizontal or vertical). The same cell cannot be used more than once per word.

**Intuition**: Insert all target words into a trie. Perform DFS from every cell on the board, simultaneously traversing the trie. If the current trie node marks end-of-word, we found a match. The trie lets us prune the DFS early — if no trie child exists for the current character, we stop exploring that path. To avoid finding the same word twice, remove the `is_end` flag once a word is found. Mark visited cells by temporarily changing their value.

**Python Solution**

```python
class Solution:
    def findWords(self, board: list[list[str]], words: list[str]) -> list[str]:
        root = TrieNode()
        for word in words:
            node = root
            for ch in word:
                if ch not in node.children:
                    node.children[ch] = TrieNode()
                node = node.children[ch]
            node.word = word  # store full word at leaf

        m, n = len(board), len(board[0])
        result = []

        def dfs(i: int, j: int, node: TrieNode) -> None:
            ch = board[i][j]
            if ch not in node.children:
                return

            child = node.children[ch]
            if hasattr(child, 'word') and child.word:
                result.append(child.word)
                child.word = None  # avoid duplicates

            board[i][j] = '#'
            for di, dj in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and board[ni][nj] != '#':
                    dfs(ni, nj, child)
            board[i][j] = ch

            if not child.children:
                del node.children[ch]

        for i in range(m):
            for j in range(n):
                dfs(i, j, root)

        return result
```

**C++ Solution**

```cpp
class Solution {
    struct Node {
        Node* children[26] = {};
        string word;
    };

    int m, n;
    vector<vector<char>>* boardPtr;
    vector<string> result;

    void dfs(int i, int j, Node* node) {
        char ch = (*boardPtr)[i][j];
        int idx = ch - 'a';
        if (!node->children[idx]) return;

        Node* child = node->children[idx];
        if (!child->word.empty()) {
            result.push_back(child->word);
            child->word.clear();
        }

        (*boardPtr)[i][j] = '#';
        int dirs[] = {0, 1, 0, -1, 0};
        for (int d = 0; d < 4; d++) {
            int ni = i + dirs[d], nj = j + dirs[d + 1];
            if (ni >= 0 && ni < m && nj >= 0 && nj < n && (*boardPtr)[ni][nj] != '#')
                dfs(ni, nj, child);
        }
        (*boardPtr)[i][j] = ch;

        bool empty = true;
        for (auto c : child->children)
            if (c) { empty = false; break; }
        if (empty) {
            delete child;
            node->children[idx] = nullptr;
        }
    }

public:
    vector<string> findWords(vector<vector<char>>& board, vector<string>& words) {
        Node* root = new Node();
        for (auto& w : words) {
            Node* cur = root;
            for (char c : w) {
                int i = c - 'a';
                if (!cur->children[i])
                    cur->children[i] = new Node();
                cur = cur->children[i];
            }
            cur->word = w;
        }

        m = board.size(); n = board[0].size();
        boardPtr = &board;
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                dfs(i, j, root);

        delete root;
        return result;
    }
};
```

**Complexity**: Time O(m · n · 4^L) where L is the max word length (trie pruning makes this much faster in practice), Space O(W · L) for the trie where W is the number of words.

---

#### Problem 5: Palindrome Pairs (LC 336) — Hard

**Link**: [https://leetcode.com/problems/palindrome-pairs/](https://leetcode.com/problems/palindrome-pairs/)

**Statement**: Given a list of unique words, find all pairs of distinct indices `(i, j)` such that the concatenation `words[i] + words[j]` is a palindrome.

**Intuition**: Insert the **reverse** of every word into a trie, tagging each node with the word's index. For each word, traverse the trie character by character. At each step, two cases can produce a palindrome:

1. **Word is longer than the trie path**: We reach a node marked as end-of-word (some reversed word ended here). If the remaining suffix of our current word is itself a palindrome, then concatenation forms a palindrome.
2. **Word is shorter than or equal to the trie path**: We exhaust our word inside the trie. Any descendant end-of-word node whose remaining reversed-word prefix is a palindrome gives a valid pair.

We precompute at each trie node the list of word indices whose remaining suffix (below that node) is a palindrome.

**Python Solution**

```python
class Solution:
    def palindromePairs(self, words: list[str]) -> list[list[int]]:
        def is_palindrome(s: str, lo: int, hi: int) -> bool:
            while lo < hi:
                if s[lo] != s[hi]:
                    return False
                lo += 1
                hi -= 1
            return True

        root = {}
        for i, word in enumerate(words):
            node = root
            rev = word[::-1]
            for j, ch in enumerate(rev):
                if 'end' in node and is_palindrome(rev, j, len(rev) - 1):
                    node.setdefault('palins', []).append(i)
                node = node.setdefault(ch, {})
            node['end'] = i
            node.setdefault('palins', []).append(i)

        result = []
        for i, word in enumerate(words):
            node = root
            for j, ch in enumerate(word):
                if 'end' in node and node['end'] != i and is_palindrome(word, j, len(word) - 1):
                    result.append([i, node['end']])
                if ch not in node:
                    break
                node = node[ch]
            else:
                if 'palins' in node:
                    for k in node['palins']:
                        if k != i:
                            result.append([i, k])

        return result
```

**C++ Solution**

```cpp
class Solution {
    struct Node {
        int children[26] = {};
        int wordIdx = -1;
        vector<int> palins;
        Node() { fill(children, children + 26, 0); }
    };

    vector<Node> trie;

    void addNode() {
        trie.push_back(Node());
    }

    bool isPalin(const string& s, int lo, int hi) {
        while (lo < hi)
            if (s[lo++] != s[hi--]) return false;
        return true;
    }

public:
    vector<vector<int>> palindromePairs(vector<string>& words) {
        trie.clear();
        addNode(); // root = 0

        int n = words.size();
        for (int i = 0; i < n; i++) {
            string rev(words[i].rbegin(), words[i].rend());
            int cur = 0;
            for (int j = 0; j < (int)rev.size(); j++) {
                if (trie[cur].wordIdx >= 0 && isPalin(rev, j, rev.size() - 1))
                    trie[cur].palins.push_back(i);
                int idx = rev[j] - 'a';
                if (!trie[cur].children[idx]) {
                    addNode();
                    trie[cur].children[idx] = trie.size() - 1;
                }
                cur = trie[cur].children[idx];
            }
            trie[cur].wordIdx = i;
            trie[cur].palins.push_back(i);
        }

        vector<vector<int>> result;
        for (int i = 0; i < n; i++) {
            int cur = 0;
            const string& w = words[i];
            int j;
            for (j = 0; j < (int)w.size(); j++) {
                if (trie[cur].wordIdx >= 0 && trie[cur].wordIdx != i
                    && isPalin(w, j, w.size() - 1))
                    result.push_back({i, trie[cur].wordIdx});
                int idx = w[j] - 'a';
                if (!trie[cur].children[idx]) { cur = -1; break; }
                cur = trie[cur].children[idx];
            }
            if (cur >= 0 && j == (int)w.size()) {
                for (int k : trie[cur].palins) {
                    if (k != i)
                        result.push_back({i, k});
                }
            }
        }
        return result;
    }
};
```

**Complexity**: Time O(n · L²) where n is the number of words and L is the average word length (palindrome checks at each node), Space O(n · L) for the trie.

---
## 18. Dynamic Programming

### Overview

Dynamic Programming (DP) solves problems by breaking them into **overlapping subproblems**, solving each subproblem exactly once, and storing its result for future lookups. DP applies when a problem exhibits two properties:

1. **Optimal Substructure** — the optimal solution to the problem can be constructed from optimal solutions of its subproblems.
2. **Overlapping Subproblems** — the same subproblems are solved repeatedly during a naive recursive approach.

There are two implementation strategies:

| Approach | Also Called | Direction | Mechanism |
|---|---|---|---|
| **Top-Down** | Memoization | Starts from the original problem, recurses into subproblems | Recursion + hash map / array cache |
| **Bottom-Up** | Tabulation | Starts from the smallest subproblems, builds up | Iterative loop filling a DP table |

Top-down is often easier to write (mirrors the recurrence directly) but carries recursion overhead. Bottom-up avoids stack overflow, is generally faster in practice, and opens the door to **space optimization** (rolling arrays).

---

### When to Use

- **Optimization problems** — find the minimum cost, maximum profit, shortest path, etc.
- **Counting problems** — number of ways to reach a target, number of distinct subsequences, etc.
- **Decision / feasibility problems** — can we partition into equal subsets? Is a string match possible?
- **Sequence problems** — longest increasing subsequence, longest common subsequence, edit distance.
- **Knapsack variants** — 0/1 knapsack, unbounded knapsack, subset sum.
- **String matching** — regex matching, wildcard matching, palindrome partitioning.
- **Grid traversal** — unique paths, minimum path sum, dungeon game.

**Quick litmus test:** If a brute-force recursion re-computes the same state many times, DP can help. Draw the recursion tree — if you see repeated nodes, memoize.

---

### Template Code

#### Top-Down (Memoization) — Climbing Stairs

**Python**

```python
def climb_stairs(n: int) -> int:
    memo = {}

    def dp(i):
        if i <= 1:
            return 1
        if i in memo:
            return memo[i]
        memo[i] = dp(i - 1) + dp(i - 2)
        return memo[i]

    return dp(n)
```

**C++**

```cpp
class Solution {
    unordered_map<int, int> memo;

    int dp(int i) {
        if (i <= 1) return 1;
        if (memo.count(i)) return memo[i];
        return memo[i] = dp(i - 1) + dp(i - 2);
    }

public:
    int climbStairs(int n) {
        return dp(n);
    }
};
```

#### Bottom-Up (Tabulation) — Climbing Stairs

**Python**

```python
def climb_stairs(n: int) -> int:
    if n <= 1:
        return 1
    dp = [0] * (n + 1)
    dp[0], dp[1] = 1, 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

**C++**

```cpp
class Solution {
public:
    int climbStairs(int n) {
        if (n <= 1) return 1;
        vector<int> dp(n + 1);
        dp[0] = dp[1] = 1;
        for (int i = 2; i <= n; i++)
            dp[i] = dp[i - 1] + dp[i - 2];
        return dp[n];
    }
};
```

#### Space-Optimized Bottom-Up — Climbing Stairs

Since each state depends only on the previous two, we can reduce space to O(1):

**Python**

```python
def climb_stairs(n: int) -> int:
    a, b = 1, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

**C++**

```cpp
class Solution {
public:
    int climbStairs(int n) {
        int a = 1, b = 1;
        for (int i = 2; i <= n; i++) {
            int tmp = b;
            b = a + b;
            a = tmp;
        }
        return b;
    }
};
```

---

### Sub-Patterns / Variations

#### 1. 0/1 Knapsack

Each item can be used **at most once**. Given `n` items with weights and values, and a capacity `W`, maximize total value without exceeding capacity.

**Recurrence:**
```
dp[i][w] = max(dp[i-1][w],                        # skip item i
               dp[i-1][w - weight[i]] + value[i])  # take item i
```

**Space optimization:** Since row `i` only depends on row `i-1`, use a 1D array and iterate `w` **right-to-left** to avoid using an item twice.

**Classic problems:** Subset Sum, Partition Equal Subset Sum (LC 416), Target Sum (LC 494).

#### 2. Unbounded Knapsack

Items can be **reused** any number of times. The key difference: when taking an item, stay at the same item index (or iterate `w` **left-to-right** in 1D).

**Recurrence:**
```
dp[w] = max(dp[w], dp[w - weight[i]] + value[i])   # iterate w left-to-right
```

**Classic problems:** Coin Change (LC 322), Coin Change II (LC 518), Rod Cutting.

#### 3. Longest Common Subsequence (LCS)

Given two strings `s1` and `s2`, find the length of their longest common subsequence.

**Recurrence:**
```
dp[i][j] = dp[i-1][j-1] + 1                      if s1[i-1] == s2[j-1]
dp[i][j] = max(dp[i-1][j], dp[i][j-1])           otherwise
```

**Base case:** `dp[0][j] = dp[i][0] = 0`.

**Classic problems:** LCS (LC 1143), Longest Common Substring, Shortest Common Supersequence (LC 1092).

#### 4. Longest Increasing Subsequence (LIS)

Find the length of the longest strictly increasing subsequence.

**O(n²) DP:**
```
dp[i] = max(dp[j] + 1) for all j < i where nums[j] < nums[i]
```

**O(n log n) with patience sorting:** Maintain a `tails` array where `tails[k]` is the smallest tail element of all increasing subsequences of length `k+1`. Binary search for the insertion point of each element.

**Classic problems:** LIS (LC 300), Russian Doll Envelopes (LC 354), Number of LIS (LC 673).

#### 5. DP on Grids

Traverse a 2D grid, typically moving right or down, computing values cell by cell.

**Recurrence (e.g., minimum path sum):**
```
dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])
```

**Space optimization:** Only need the previous row, so use a 1D array of width `n`.

**Classic problems:** Unique Paths (LC 62), Minimum Path Sum (LC 64), Dungeon Game (LC 174), Maximal Square (LC 221).

#### 6. DP on Strings

Compare, transform, or partition strings using 2D DP tables.

**Common recurrence (edit distance):**
```
dp[i][j] = dp[i-1][j-1]                                          if s1[i-1] == s2[j-1]
dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])        otherwise (delete, insert, replace)
```

**Classic problems:** Edit Distance (LC 72), Regular Expression Matching (LC 10), Wildcard Matching (LC 44), Palindrome Partitioning II (LC 132), Distinct Subsequences (LC 115).

#### 7. Bitmask DP

Use an integer bitmask to represent which elements from a set have been used. Bit `k` is set if element `k` is included.

**State:** `dp[mask]` — optimal value achievable when the subset of used elements is described by `mask`.

**Transitions:** Enumerate unset bits to decide which element to add next.

```python
for mask in range(1 << n):
    for j in range(n):
        if not (mask & (1 << j)):
            new_mask = mask | (1 << j)
            dp[new_mask] = min(dp[new_mask], dp[mask] + cost(mask, j))
```

**Complexity:** O(2^n × n), feasible for n ≤ 20.

**Classic problems:** Travelling Salesman (Held–Karp), Partition to K Equal Sum Subsets (LC 698), Shortest Path Visiting All Nodes (LC 847).

#### 8. Interval DP

The state is a contiguous range `[i, j]`, and the answer for a range combines answers for smaller ranges split at some `k`. Fill the table **by increasing length**, so every sub-range is ready when needed.

**Recurrence (Burst Balloons, open interval `(l, r)`, `k` = last balloon burst):**
```
dp[l][r] = max over l < k < r of  dp[l][k] + dp[k][r] + a[l] * a[k] * a[r]
```

**Complexity:** O(n^3) time, O(n^2) space (n ≤ 300–500).

**Classic problems:** Burst Balloons (LC 312), Minimum Cost to Cut a Stick (LC 1547), Matrix Chain Multiplication, Longest Palindromic Subsequence (LC 516), Strange Printer (LC 664), Minimum Score Triangulation of Polygon (LC 1039).

#### 9. Tree DP

Each node returns a small tuple describing its subtree, computed in **post-order** from its children's tuples. The answer is read at the root (or tracked globally when the best structure can bend through any node).

**Recurrence (House Robber III):**
```
rob(v)  = v.val + skip(left) + skip(right)
skip(v) = max(rob(left), skip(left)) + max(rob(right), skip(right))
```

**Classic problems:** House Robber III (LC 337), Binary Tree Maximum Path Sum (LC 124), Diameter of Binary Tree (LC 543), Binary Tree Cameras (LC 968), Sum of Distances in Tree (LC 834, "rerooting").

#### 10. State-Machine DP (Stock Problems)

Model each day's situation as a small set of states (holding / not holding / cooling down / transactions used) and write the transitions between consecutive days. Each state is a running maximum, so space is O(states).

**Recurrence (unlimited transactions, with fee):**
```
cash = max(cash, hold + price - fee)      # sell today or keep cash
hold = max(hold, cash - price)            # buy today or keep holding
```

**Classic problems:** Best Time to Buy and Sell Stock I–IV (LC 121, 122, 123, 188), with Cooldown (LC 309), with Transaction Fee (LC 714). Also: Paint House (LC 256), Delete and Earn (LC 740).

#### 11. Partition / Subset-Sum DP

A 0/1 knapsack where the "value" is feasibility or a count. The key move is turning the question into "is there a subset with sum `S`?" for some derived `S`.

**Transforms:**
```
Partition Equal Subset Sum:  S = total / 2               (total must be even)
Target Sum (+/- signs):      P - N = target, P + N = total  ->  S = (total + target) / 2
Last Stone Weight II:        minimise |total - 2 * S| over reachable S <= total / 2
```

**Recurrence (counting):** `ways[s] += ways[s - x]`, with `s` iterated **downwards** so each number is used once.

**Classic problems:** Partition Equal Subset Sum (LC 416), Target Sum (LC 494), Last Stone Weight II (LC 1049), Ones and Zeroes (LC 474, 2D capacity).

#### 12. Digit DP

Count integers in `[0, N]` whose digits satisfy a property, when `N` is up to 10^18 so enumerating is impossible. Walk the digits of `N` from the most significant. The state is `(position, tight, property_state)`, where `tight` means "the prefix so far equals `N`'s prefix, so the next digit is capped at `N`'s digit". Ranges `[L, R]` are `count(R) - count(L - 1)`.

```
f(pos, tight, st) = sum over d in [0, (digit[pos] if tight else 9)] of
                    f(pos + 1, tight and d == digit[pos], update(st, d))
```

Add a `started` flag when leading zeros would affect the property (for example "no repeated digits").

**Classic problems:** Number of Digit One (LC 233), Numbers At Most N Given Digit Set (LC 902), Numbers With Repeated Digits (LC 1012), Count Special Integers (LC 2376), Non-negative Integers without Consecutive Ones (LC 600).

#### 13. 1D Linear DP (Take/Skip and Prefix Segmentation)

The state `dp[i]` is the answer for the **prefix of length `i`**: items `0..i-1`, or characters `s[0..i-1]`. Most 1D classics take one of three shapes. They differ only in how the last item or last piece is chosen:

```text
Take/skip with adjacency rule:  dp[i] = max(dp[i-1], dp[i-2] + a[i-1])                      House Robber
Fixed-width last piece:         dp[i] = [s[i-1] valid]·dp[i-1] + [s[i-2..i-1] valid]·dp[i-2]   Decode Ways, Climbing Stairs
Variable-width last piece:      dp[i] = OR / sum / min over j < i of  dp[j] (+) cost(s[j..i-1])   Word Break, Perfect Squares,
                                                                                              Palindrome Partitioning II
```

Use `dp[0]` for the **empty prefix**. It is 1 for counting, `True` for feasibility, and 0 for max/min sums, and it removes most special cases. When `dp[i]` reads only a constant number of earlier entries, keep two rolling variables instead of an array: O(1) space. In the variable-width case, cap `j` at `i - maxPieceLen`. That cuts the scan from O(n^2) to O(n·L).

**Classic problems:** House Robber (LC 198, 213), Delete and Earn (LC 740, House Robber over values), Decode Ways (LC 91, 639), Word Break (LC 139, 140), Maximum Product Subarray (LC 152, which tracks both the max and the min ending at `i`), Perfect Squares (LC 279), Min Cost Climbing Stairs (LC 746). Longest Palindromic Substring (LC 5) is formally a 2D interval DP on `[i, j]`, but interviews expect expand-around-center (see Problem 17).

---

### Common Mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Wrong subproblem definition | Entire DP is incorrect | Clearly define what `dp[i]` (or `dp[i][j]`) represents before writing code |
| Incorrect base case | Off-by-one errors, wrong answers | Manually verify the smallest inputs (n=0, n=1, empty string) |
| Missing transitions | Skipping valid choices | Enumerate all decisions at each state (take/skip, insert/delete/replace, etc.) |
| Forgetting to memoize | TLE — exponential time despite correct recurrence | Always store result before returning in top-down |
| Index out of bounds in 2D DP | Runtime error | Size the table as `(m+1) × (n+1)` when using 1-indexed recurrence |
| Not optimizing space | MLE on large inputs | If row `i` depends only on row `i-1`, use a rolling 1D array |
| Confusing 0/1 vs. unbounded knapsack | Items used incorrectly | 0/1: iterate capacity right-to-left; Unbounded: left-to-right |

---

### Related Patterns

- **Greedy** — When the greedy choice property holds, greedy is simpler and faster. DP is the fallback when greedy fails (e.g., Coin Change with arbitrary denominations).
- **Backtracking** — DP can be viewed as optimized backtracking: instead of exploring all paths and pruning, DP caches overlapping states.
- **Divide and Conquer** — Both break problems into subproblems, but D&C subproblems don't overlap (merge sort), while DP subproblems do.
- **DFS** ([Pattern 8](#8-dfs-depth-first-search)) — tree DP is a post-order DFS that returns a tuple per node.
- **Binary Search on the Answer** ([Pattern 28](#28-binary-search-on-the-answer)) — often beats a partition DP (Split Array Largest Sum).
- **Meet-in-the-Middle** ([Pattern 33](#33-meet-in-the-middle--bidirectional-bfs)) — the alternative to subset-sum DP when values are huge but n ≤ 40.
- **See also:** [DSA Fundamentals: Dynamic Programming](DSA_Fundamentals.md#20-dynamic-programming) for the category table and theory.

---

### Example Problems

---

#### Problem 1: Climbing Stairs (LC 70) — Easy

**Link:** https://leetcode.com/problems/climbing-stairs/

**Statement:** You are climbing a staircase with `n` steps. Each time you can climb 1 or 2 steps. In how many distinct ways can you reach the top?

**Intuition:** Let `dp[i]` = number of ways to reach step `i`. You can arrive from step `i-1` (one step) or step `i-2` (two steps), so `dp[i] = dp[i-1] + dp[i-2]`. This is the Fibonacci sequence. Base cases: `dp[0] = 1` (one way to stay at ground), `dp[1] = 1`.

**Python Solution:**

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        a, b = 1, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
```

**C++ Solution:**

```cpp
class Solution {
public:
    int climbStairs(int n) {
        int a = 1, b = 1;
        for (int i = 2; i <= n; i++) {
            int tmp = b;
            b = a + b;
            a = tmp;
        }
        return b;
    }
};
```

**Complexity:** Time O(n), Space O(1).

---

#### Problem 2: Coin Change (LC 322) — Medium

**Link:** https://leetcode.com/problems/coin-change/

**Statement:** Given an array `coins` of coin denominations and a target `amount`, return the fewest number of coins needed to make up that amount. Return -1 if it cannot be made.

**Intuition:** This is an **unbounded knapsack** variant. Let `dp[a]` = minimum coins to make amount `a`. For each amount, try every coin: `dp[a] = min(dp[a - coin] + 1)` for all valid coins. Initialize `dp[0] = 0` and all others to infinity. Iterate amounts left-to-right since coins are reusable.

**Python Solution:**

```python
class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0
        for a in range(1, amount + 1):
            for coin in coins:
                if coin <= a and dp[a - coin] + 1 < dp[a]:
                    dp[a] = dp[a - coin] + 1
        return dp[amount] if dp[amount] != float('inf') else -1
```

**C++ Solution:**

```cpp
class Solution {
public:
    int coinChange(vector<int>& coins, int amount) {
        vector<int> dp(amount + 1, amount + 1);
        dp[0] = 0;
        for (int a = 1; a <= amount; a++) {
            for (int coin : coins) {
                if (coin <= a)
                    dp[a] = min(dp[a], dp[a - coin] + 1);
            }
        }
        return dp[amount] > amount ? -1 : dp[amount];
    }
};
```

**Complexity:** Time O(n × amount) where n = number of coin types, Space O(amount).

---

#### Problem 3: Longest Common Subsequence (LC 1143) — Medium

**Link:** https://leetcode.com/problems/longest-common-subsequence/

**Statement:** Given two strings `text1` and `text2`, return the length of their longest common subsequence. A subsequence is derived by deleting some (or no) characters without changing relative order.

**Intuition:** Classic 2D DP. Let `dp[i][j]` = LCS length of `text1[0..i-1]` and `text2[0..j-1]`. If the current characters match, extend the LCS from `dp[i-1][j-1]`. Otherwise, take the better of skipping a character from either string.

**Recurrence:**
- If `text1[i-1] == text2[j-1]`: `dp[i][j] = dp[i-1][j-1] + 1`
- Else: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`

**Python Solution:**

```python
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp[m][n]
```

**C++ Solution:**

```cpp
class Solution {
public:
    int longestCommonSubsequence(string text1, string text2) {
        int m = text1.size(), n = text2.size();
        vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (text1[i - 1] == text2[j - 1])
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                else
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
        return dp[m][n];
    }
};
```

**Complexity:** Time O(m × n), Space O(m × n). Can be optimized to O(min(m, n)) space using a rolling array.

---

#### Problem 4: Longest Increasing Subsequence (LC 300) — Medium

**Link:** https://leetcode.com/problems/longest-increasing-subsequence/

**Statement:** Given an integer array `nums`, return the length of the longest strictly increasing subsequence.

**Intuition:**

*Approach 1 — O(n²) DP:* Let `dp[i]` = length of the LIS ending at index `i`. For each `i`, check all `j < i`: if `nums[j] < nums[i]`, then `dp[i] = max(dp[i], dp[j] + 1)`. Answer is `max(dp)`.

*Approach 2 — O(n log n) patience sorting:* Maintain a `tails` array. For each number, binary search for the first element in `tails` that is ≥ the current number. If found, replace it; otherwise, append. The length of `tails` is the LIS length. (`tails` is not the actual LIS, but its length is correct.)

**Python Solution (O(n²)):**

```python
class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        n = len(nums)
        dp = [1] * n
        for i in range(1, n):
            for j in range(i):
                if nums[j] < nums[i]:
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)
```

**Python Solution (O(n log n)):**

```python
import bisect

class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        tails = []
        for num in nums:
            pos = bisect.bisect_left(tails, num)
            if pos == len(tails):
                tails.append(num)
            else:
                tails[pos] = num
        return len(tails)
```

**C++ Solution (O(n log n)):**

```cpp
class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        vector<int> tails;
        for (int num : nums) {
            auto it = lower_bound(tails.begin(), tails.end(), num);
            if (it == tails.end())
                tails.push_back(num);
            else
                *it = num;
        }
        return tails.size();
    }
};
```

**Complexity:**
- O(n²) DP: Time O(n²), Space O(n).
- Patience sorting: Time O(n log n), Space O(n).

---

#### Problem 5: Edit Distance (LC 72) — Hard

**Link:** https://leetcode.com/problems/edit-distance/

**Statement:** Given two strings `word1` and `word2`, return the minimum number of operations (insert, delete, replace a character) required to convert `word1` into `word2`.

**Intuition:** Let `dp[i][j]` = edit distance between `word1[0..i-1]` and `word2[0..j-1]`. If the last characters match, no operation is needed: `dp[i][j] = dp[i-1][j-1]`. Otherwise, choose the cheapest among three operations:
- **Insert** a character into `word1`: `dp[i][j-1] + 1`
- **Delete** a character from `word1`: `dp[i-1][j] + 1`
- **Replace** the character in `word1`: `dp[i-1][j-1] + 1`

**Base cases:** `dp[i][0] = i` (delete all of `word1`), `dp[0][j] = j` (insert all of `word2`).

**Python Solution:**

```python
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(
                        dp[i - 1][j],      # delete
                        dp[i][j - 1],      # insert
                        dp[i - 1][j - 1]   # replace
                    )
        return dp[m][n]
```

**C++ Solution:**

```cpp
class Solution {
public:
    int minDistance(string word1, string word2) {
        int m = word1.size(), n = word2.size();
        vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
        for (int i = 0; i <= m; i++) dp[i][0] = i;
        for (int j = 0; j <= n; j++) dp[0][j] = j;
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (word1[i - 1] == word2[j - 1]) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = 1 + min({dp[i - 1][j],
                                         dp[i][j - 1],
                                         dp[i - 1][j - 1]});
                }
            }
        }
        return dp[m][n];
    }
};
```

**Complexity:** Time O(m × n), Space O(m × n). Can be optimized to O(min(m, n)) space with a rolling array and one extra variable to track the diagonal value.

---

#### Problem 6: House Robber III (LC 337) — Medium (Tree DP)

**Link:** https://leetcode.com/problems/house-robber-iii/

**Statement:** Houses form a binary tree. Robbing two directly linked houses (parent and child) alerts the police. Return the maximum amount you can rob.

**Intuition:** A greedy "rob alternate levels" fails (the best set can skip two levels in a row). Each node returns two numbers: the best total for its subtree **if it is robbed** (then its children must be skipped) and **if it is skipped** (then each child is free to be robbed or skipped, whichever is better). One post-order pass, no memo table needed, because each node is visited once.

**Python Solution:**

```python
from typing import Optional

class Solution:
    def rob(self, root: Optional[TreeNode]) -> int:
        def dfs(node: Optional[TreeNode]) -> tuple[int, int]:   # (rob this node, skip this node)
            if not node:
                return 0, 0
            left_rob, left_skip = dfs(node.left)
            right_rob, right_skip = dfs(node.right)
            rob = node.val + left_skip + right_skip
            skip = max(left_rob, left_skip) + max(right_rob, right_skip)
            return rob, skip

        return max(dfs(root))
```

**C++ Solution:**

```cpp
#include <algorithm>
#include <utility>
using namespace std;

class Solution {
    pair<int, int> dfs(TreeNode* node) {           // {rob, skip}
        if (!node) return {0, 0};
        auto [lRob, lSkip] = dfs(node->left);
        auto [rRob, rSkip] = dfs(node->right);
        int rob = node->val + lSkip + rSkip;
        int skip = max(lRob, lSkip) + max(rRob, rSkip);
        return {rob, skip};
    }

public:
    int rob(TreeNode* root) {
        auto [r, s] = dfs(root);
        return max(r, s);
    }
};
```

**Complexity:** Time O(n), Space O(h). The naive recursion "rob me + grandchildren vs. children" without returning pairs re-solves subtrees and is exponential unless memoized by node.

---

#### Problem 7: Best Time to Buy and Sell Stock I–IV, Cooldown, Fee (LC 121, 122, 123, 188, 309, 714) (State Machine)

**Link:** https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/ (and siblings)

**Statement:** `prices[i]` is the price on day `i`. You may hold at most one share at a time. The variants change the rules: one transaction (121), unlimited (122), at most 2 (123) or `k` (188), a one-day cooldown after selling (309), a fee per transaction (714).

**Intuition:** All six are the same state machine with different states. Track, for each state, the best **balance** (cash) achievable after today:

```text
               buy (-p)                       sell (+p)
   [not holding] ──────────► [holding] ──────────────► [not holding]
        ▲  rest                  rest                       │
        └───────────────────────────────────────────────────┘
   cooldown (309): selling leads to a "sold" state that must rest one day before buying
   fee (714): subtract the fee on sell
   k transactions (188): one (holding, not holding) pair per transaction count j = 1..k
```

If `k ≥ n/2`, the limit can never bind (a profitable transaction needs at least 2 days), so 188 reduces to 122. That shortcut avoids an O(nk) table when `k` is huge.

**Python Solution:**

```python
def max_profit_one(prices: list[int]) -> int:                     # LC 121
    best, low = 0, float('inf')
    for p in prices:
        low = min(low, p)
        best = max(best, p - low)
    return best

def max_profit_unlimited(prices: list[int]) -> int:               # LC 122
    cash, hold = 0, float('-inf')
    for p in prices:
        cash, hold = max(cash, hold + p), max(hold, cash - p)
    return cash

def max_profit_k(k: int, prices: list[int]) -> int:               # LC 188 (LC 123 is k = 2)
    if k >= len(prices) // 2:
        return max_profit_unlimited(prices)
    buy = [float('-inf')] * (k + 1)    # buy[j]: best balance while holding, j-th buy made
    sell = [0] * (k + 1)               # sell[j]: best balance after j completed transactions
    for p in prices:
        for j in range(1, k + 1):
            buy[j] = max(buy[j], sell[j - 1] - p)
            sell[j] = max(sell[j], buy[j] + p)
    return sell[k]

def max_profit_cooldown(prices: list[int]) -> int:                # LC 309
    hold, sold, rest = float('-inf'), 0, 0   # rest = not holding and allowed to buy
    for p in prices:
        hold, sold, rest = max(hold, rest - p), hold + p, max(rest, sold)
    return max(sold, rest)

def max_profit_fee(prices: list[int], fee: int) -> int:           # LC 714
    cash, hold = 0, float('-inf')
    for p in prices:
        cash, hold = max(cash, hold + p - fee), max(hold, cash - p)
    return cash

assert max_profit_one([7, 1, 5, 3, 6, 4]) == 5
assert max_profit_unlimited([7, 1, 5, 3, 6, 4]) == 7
assert max_profit_k(2, [3, 3, 5, 0, 0, 3, 1, 4]) == 6
assert max_profit_k(2, [3, 2, 6, 5, 0, 3]) == 7
assert max_profit_cooldown([1, 2, 3, 0, 2]) == 3
assert max_profit_fee([1, 3, 2, 8, 4, 9], 2) == 8
```

**C++ Solution:**

```cpp
#include <algorithm>
#include <climits>
#include <vector>
using namespace std;

int maxProfitK(int k, const vector<int>& prices) {                 // LC 188 / 123
    int n = prices.size();
    if (k >= n / 2) {                                              // unlimited (LC 122)
        int profit = 0;
        for (int i = 1; i < n; ++i) profit += max(0, prices[i] - prices[i - 1]);
        return profit;
    }
    vector<int> buy(k + 1, INT_MIN / 2), sell(k + 1, 0);           // INT_MIN/2: no overflow on + p
    for (int p : prices) {
        for (int j = 1; j <= k; ++j) {
            buy[j] = max(buy[j], sell[j - 1] - p);
            sell[j] = max(sell[j], buy[j] + p);
        }
    }
    return sell[k];
}

int maxProfitCooldown(const vector<int>& prices) {                 // LC 309
    int hold = INT_MIN / 2, sold = 0, rest = 0;
    for (int p : prices) {
        int prevSold = sold;
        sold = hold + p;
        hold = max(hold, rest - p);
        rest = max(rest, prevSold);
    }
    return max(sold, rest);
}

int maxProfitFee(const vector<int>& prices, int fee) {             // LC 714
    int cash = 0, hold = INT_MIN / 2;
    for (int p : prices) {
        int prevCash = cash;
        cash = max(cash, hold + p - fee);
        hold = max(hold, prevCash - p);
    }
    return cash;
}
```

**Complexity:** O(n) time and O(1) space for 121, 122, 309, 714. O(n · k) time and O(k) space for 188. The unlimited case also has the greedy form "sum every positive day-to-day difference", which is what the C++ shortcut uses.

---

#### Problem 8: Burst Balloons (LC 312) — Hard (Interval DP)

**Link:** https://leetcode.com/problems/burst-balloons/

**Statement:** Bursting balloon `i` earns `nums[i-1] * nums[i] * nums[i+1]` using its **current** neighbours (out-of-range neighbours count as 1). Burst all balloons; maximise the total.

**Intuition:** Choosing the **first** balloon to burst does not split the problem, because its neighbours change. Choosing the **last** balloon `k` to burst inside an open interval `(l, r)` does: when `k` goes last, its neighbours are exactly `l` and `r`, and the balloons on each side are burst independently before it. Pad with 1s at both ends so `dp[0][n+1]` covers everything.

**Python Solution:**

```python
class Solution:
    def maxCoins(self, nums: list[int]) -> int:
        a = [1] + nums + [1]
        n = len(a)
        dp = [[0] * n for _ in range(n)]          # dp[l][r]: best for balloons strictly inside (l, r)
        for length in range(2, n):                # r - l
            for l in range(n - length):
                r = l + length
                best = 0
                for k in range(l + 1, r):         # k is the LAST balloon burst in (l, r)
                    best = max(best, dp[l][k] + dp[k][r] + a[l] * a[k] * a[r])
                dp[l][r] = best
        return dp[0][n - 1]
```

**C++ Solution:**

```cpp
#include <algorithm>
#include <vector>
using namespace std;

class Solution {
public:
    int maxCoins(vector<int>& nums) {
        vector<int> a{1};
        a.insert(a.end(), nums.begin(), nums.end());
        a.push_back(1);
        int n = a.size();
        vector<vector<int>> dp(n, vector<int>(n, 0));
        for (int len = 2; len < n; ++len) {
            for (int l = 0; l + len < n; ++l) {
                int r = l + len;
                for (int k = l + 1; k < r; ++k)
                    dp[l][r] = max(dp[l][r], dp[l][k] + dp[k][r] + a[l] * a[k] * a[r]);
            }
        }
        return dp[0][n - 1];
    }
};
```

**Complexity:** Time O(n^3) (about n^3/6 ≈ 4.5 · 10^6 inner steps for n = 300: fast in C++, a few seconds in Python). Space O(n^2). Example: `[3, 1, 5, 8]` → 167.

---

#### Problem 9: Partition Equal Subset Sum (LC 416) — Medium (Partition DP)

**Link:** https://leetcode.com/problems/partition-equal-subset-sum/

**Statement:** Can `nums` be split into two subsets with equal sums?

**Intuition:** Equal halves exist exactly when some subset sums to `total / 2` (and `total` is even). This is a 0/1 knapsack feasibility table `can[s]`. Iterate `s` **downwards** so each number is used at most once. Systems-style speed-up: the whole table is a bitset, and adding number `x` is `reach |= reach << x`, which processes 64 sums per machine word.

**Python Solution:**

```python
class Solution:
    def canPartition(self, nums: list[int]) -> bool:
        total = sum(nums)
        if total % 2:
            return False
        target = total // 2
        can = [True] + [False] * target
        for x in nums:
            for s in range(target, x - 1, -1):    # downwards: each x used once
                can[s] = can[s] or can[s - x]
        return can[target]


def can_partition_bitset(nums: list[int]) -> bool:
    total = sum(nums)
    if total % 2:
        return False
    reach = 1                                     # bit s set <=> some subset sums to s
    for x in nums:
        reach |= reach << x
    return (reach >> (total // 2)) & 1 == 1

assert can_partition_bitset([1, 5, 11, 5]) and not can_partition_bitset([1, 2, 3, 5])
```

**C++ Solution:**

```cpp
#include <bitset>
#include <numeric>
#include <vector>
using namespace std;

class Solution {
public:
    bool canPartition(vector<int>& nums) {
        int total = accumulate(nums.begin(), nums.end(), 0);
        if (total % 2) return false;
        bitset<10001> reach;                      // n <= 200, nums[i] <= 100 -> target <= 10000
        reach[0] = 1;
        for (int x : nums) reach |= reach << x;   // bits shifted past 10000 are irrelevant
        return reach[total / 2];
    }
};
```

**Complexity:** Time O(n · target) for the table, O(n · target / 64) for the bitset. Space O(target).

---

#### Problem 10: Target Sum (LC 494) — Medium (Partition DP)

**Link:** https://leetcode.com/problems/target-sum/

**Statement:** Put `+` or `-` before every number in `nums` (non-negative) so the expression equals `target`. Count the assignments.

**Intuition:** Let `P` be the sum of numbers with `+` and `N` the sum with `-`. Then `P - N = target` and `P + N = total`, so `P = (total + target) / 2`. The answer is the number of subsets with sum `P`, a counting knapsack. If `total + target` is odd or `|target| > total`, the answer is 0. Zeros are handled automatically: each zero doubles the count (`ways[s] += ways[s]`), matching its two sign choices.

**Python Solution:**

```python
class Solution:
    def findTargetSumWays(self, nums: list[int], target: int) -> int:
        total = sum(nums)
        if abs(target) > total or (total + target) % 2:
            return 0
        want = (total + target) // 2
        ways = [1] + [0] * want
        for x in nums:
            for s in range(want, x - 1, -1):
                ways[s] += ways[s - x]
        return ways[want]
```

**C++ Solution:**

```cpp
#include <cstdlib>
#include <numeric>
#include <vector>
using namespace std;

class Solution {
public:
    int findTargetSumWays(vector<int>& nums, int target) {
        int total = accumulate(nums.begin(), nums.end(), 0);
        if (abs(target) > total || (total + target) % 2 != 0) return 0;
        int want = (total + target) / 2;
        vector<long long> ways(want + 1, 0);
        ways[0] = 1;
        for (int x : nums)
            for (int s = want; s >= x; --s) ways[s] += ways[s - x];
        return static_cast<int>(ways[want]);
    }
};
```

**Complexity:** Time O(n · want). Space O(want). Example: `[1, 1, 1, 1, 1]`, `target = 3` → `want = 4` → 5 ways.

---

#### Problem 11: Partition to K Equal Sum Subsets (LC 698) — Medium (Bitmask DP)

**Link:** https://leetcode.com/problems/partition-to-k-equal-sum-subsets/

**Statement:** Can `nums` (`n ≤ 16`) be split into `k` non-empty subsets with equal sums?

**Intuition:** Fill buckets one at a time. If a set of used numbers `mask` is reachable, the partially filled current bucket holds exactly `sum(mask) % target`, so the only question is **which masks are reachable**. Store `fill[mask]` (or -1 if unreachable) and extend by any unused number that still fits in the current bucket. Sorting lets the inner loop `break` at the first number that does not fit. The answer is whether the full mask is reachable. This is O(2^n · n), about 10^6 steps for n = 16, compared with the k^n worst case of naive backtracking.

**Python Solution:**

```python
class Solution:
    def canPartitionKSubsets(self, nums: list[int], k: int) -> bool:
        total = sum(nums)
        if total % k:
            return False
        target = total // k
        nums.sort()
        if nums[-1] > target:
            return False
        n = len(nums)
        fill = [-1] * (1 << n)          # fill[mask]: amount in the current bucket, -1 = unreachable
        fill[0] = 0
        for mask in range(1 << n):
            if fill[mask] < 0:
                continue
            for i in range(n):
                if mask >> i & 1:
                    continue
                if fill[mask] + nums[i] > target:
                    break               # sorted: every later number is too big as well
                nxt = mask | (1 << i)
                if fill[nxt] < 0:
                    fill[nxt] = (fill[mask] + nums[i]) % target   # a full bucket resets to 0
        return fill[(1 << n) - 1] == 0
```

**C++ Solution:**

```cpp
#include <algorithm>
#include <numeric>
#include <vector>
using namespace std;

class Solution {
public:
    bool canPartitionKSubsets(vector<int>& nums, int k) {
        int total = accumulate(nums.begin(), nums.end(), 0);
        if (total % k) return false;
        int target = total / k, n = nums.size();
        sort(nums.begin(), nums.end());
        if (nums.back() > target) return false;
        vector<int> fill(1 << n, -1);
        fill[0] = 0;
        for (int mask = 0; mask < (1 << n); ++mask) {
            if (fill[mask] < 0) continue;
            for (int i = 0; i < n; ++i) {
                if (mask >> i & 1) continue;
                if (fill[mask] + nums[i] > target) break;
                int nxt = mask | (1 << i);
                if (fill[nxt] < 0) fill[nxt] = (fill[mask] + nums[i]) % target;
            }
        }
        return fill[(1 << n) - 1] == 0;
    }
};
```

**Complexity:** Time O(2^n · n). Space O(2^n).

---

#### Problem 12: Travelling Salesman, Held–Karp (Bitmask DP)

**Statement:** Given an `n x n` distance matrix (`n ≤ 16–20`), find the shortest tour that starts at city 0, visits every city exactly once, and returns to 0. (LeetCode variants: Find the Shortest Superstring (LC 943), Shortest Path Visiting All Nodes (LC 847, which is TSP on BFS distances).)

**Intuition:** Brute force tries `(n-1)!` orders: 19! ≈ 1.2 · 10^17. But the cost of finishing a tour depends only on **which** cities are visited and **where** you are, not the order. So `dp[mask][j]` = shortest path that starts at 0, visits exactly the cities in `mask`, and ends at `j`. Transition by appending an unvisited city `k`. There are `2^n · n` states with `n` transitions each.

**Python Solution:**

```python
def held_karp(dist: list[list[int]]) -> int:
    n = len(dist)
    INF = float('inf')
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0                                   # only city 0 visited, standing at 0
    for mask in range(1 << n):
        if not mask & 1:
            continue                               # every path starts at city 0
        for j in range(n):
            cur = dp[mask][j]
            if cur == INF:
                continue
            for k in range(n):
                if mask >> k & 1:
                    continue
                nm = mask | (1 << k)
                if cur + dist[j][k] < dp[nm][k]:
                    dp[nm][k] = cur + dist[j][k]
    full = (1 << n) - 1
    return min(dp[full][j] + dist[j][0] for j in range(n))

assert held_karp([[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]) == 80
```

**C++ Solution:**

```cpp
#include <algorithm>
#include <climits>
#include <vector>
using namespace std;

int heldKarp(const vector<vector<int>>& dist) {
    int n = dist.size();
    const int INF = INT_MAX / 2;
    vector<vector<int>> dp(1 << n, vector<int>(n, INF));
    dp[1][0] = 0;
    for (int mask = 1; mask < (1 << n); mask += 2) {     // odd masks: city 0 included
        for (int j = 0; j < n; ++j) {
            if (dp[mask][j] >= INF) continue;
            for (int k = 0; k < n; ++k) {
                if (mask >> k & 1) continue;
                int nm = mask | (1 << k);
                dp[nm][k] = min(dp[nm][k], dp[mask][j] + dist[j][k]);
            }
        }
    }
    int best = INF, full = (1 << n) - 1;
    for (int j = 0; j < n; ++j) best = min(best, dp[full][j] + dist[j][0]);
    return best;
}
```

**Complexity:** Time O(2^n · n^2): about 4 · 10^8 basic steps at n = 20, feasible in C++ but not in Python. Space O(2^n · n): 2^20 × 20 × 4 bytes ≈ 80 MiB at n = 20, so a flat array is better than nested vectors.

---

#### Problem 13: Number of Digit One (LC 233) — Hard (Digit DP)

**Link:** https://leetcode.com/problems/number-of-digit-one/

**Statement:** Count the total number of digit `1`s appearing in all integers from 0 to `n` (`n ≤ 10^9`).

**Intuition:** Walk `n`'s digits from the left with state `(pos, ones_so_far, tight)`. At each position try every digit `d` up to the cap (`digit[pos]` if tight, else 9). When the last position is passed, the number is complete and contributes `ones_so_far`. Leading zeros do not matter here, since they are not 1s. Only **non-tight** states repeat (a tight state is visited once, along `n`'s own prefix), so memoising non-tight states is enough: about 10 positions × 10 counts.

**Python Solution:**

```python
from functools import lru_cache

class Solution:
    def countDigitOne(self, n: int) -> int:
        digits = list(map(int, str(n)))

        @lru_cache(maxsize=None)
        def dp(pos: int, ones: int, tight: bool) -> int:
            if pos == len(digits):
                return ones
            limit = digits[pos] if tight else 9
            return sum(dp(pos + 1, ones + (d == 1), tight and d == limit) for d in range(limit + 1))

        return dp(0, 0, True)
```

**C++ Solution:**

```cpp
#include <cstring>
#include <string>
using namespace std;

class Solution {
    string digits;
    long long memo[11][11];
    bool seen[11][11];

    long long dp(int pos, int ones, bool tight) {
        if (pos == static_cast<int>(digits.size())) return ones;
        if (!tight && seen[pos][ones]) return memo[pos][ones];
        int limit = tight ? digits[pos] - '0' : 9;
        long long total = 0;
        for (int d = 0; d <= limit; ++d)
            total += dp(pos + 1, ones + (d == 1), tight && d == limit);
        if (!tight) {
            seen[pos][ones] = true;
            memo[pos][ones] = total;
        }
        return total;
    }

public:
    int countDigitOne(int n) {
        digits = to_string(n);
        memset(seen, 0, sizeof(seen));
        return static_cast<int>(dp(0, 0, true));
    }
};
```

**Complexity:** O(D^2 · 10) states × transitions, with D = number of digits (10). Effectively constant. Example: `n = 13` → 6 (from 1, 10, 11 (two), 12, 13).

---

#### Problem 14: House Robber I and II (LC 198, 213) — Medium (1D Take/Skip)

**Link:** https://leetcode.com/problems/house-robber/ and https://leetcode.com/problems/house-robber-ii/

**Statement:** `nums[i] ≥ 0` is the cash in house `i`. You cannot rob two adjacent houses. Return the maximum you can rob. In LC 213 the houses form a **circle**, so the first and last houses are also adjacent.

**Intuition:** Let `dp[i]` be the best total using houses `0..i-1`. For the last house `i-1` there are two choices. **Skip** it and keep `dp[i-1]`. **Take** it, which forbids house `i-2`, giving `dp[i-2] + nums[i-1]`. So `dp[i] = max(dp[i-1], dp[i-2] + nums[i-1])`, with `dp[0] = 0`. The recurrence reads only two earlier values, so two variables suffice.

Greedy approaches fail. "Take the largest available house" on `[2, 3, 2]` takes 3, but the optimum is 2 + 2 = 4. "Take all even or all odd indices" on `[2, 1, 1, 2]` gives 3, but the optimum is 2 + 2 = 4 (indices 0 and 3, which skips two houses in a row).

**Circular variant:** In any valid plan, house 0 or house n-1 (or both) is left unrobbed. Solve the line problem twice, once on `nums[1:]` and once on `nums[:-1]`, and take the max. Handle `n == 1` separately, since both slices are then empty.

**Worked example** `nums = [2, 7, 9, 3, 1]`:

| i (house) | x | take = prev2 + x | skip = prev1 | new prev1 |
|---|---|---|---|---|
| 0 | 2 | 0 + 2 = 2 | 0 | 2 |
| 1 | 7 | 0 + 7 = 7 | 2 | 7 |
| 2 | 9 | 2 + 9 = 11 | 7 | 11 |
| 3 | 3 | 7 + 3 = 10 | 11 | 11 |
| 4 | 1 | 11 + 1 = 12 | 11 | **12** |

The answer is 12 = 2 + 9 + 1. Under the circular rule, `[2, 3, 2]` gives `max(rob([3, 2]), rob([2, 3])) = 3`.

**Python Solution:**

```python
class Solution:
    def rob(self, nums: list[int]) -> int:                 # LC 198
        prev2, prev1 = 0, 0          # best for houses [0..i-2], [0..i-1]
        for x in nums:
            prev2, prev1 = prev1, max(prev1, prev2 + x)    # skip i  vs  take i
        return prev1

    def rob_circle(self, nums: list[int]) -> int:          # LC 213
        if len(nums) == 1:
            return nums[0]
        return max(self.rob(nums[1:]), self.rob(nums[:-1]))   # exclude first or exclude last
```

**C++ Solution:**

```cpp
#include <algorithm>
#include <vector>
using namespace std;

class Solution {
    static int robLine(const vector<int>& a, int lo, int hi) {   // houses [lo, hi)
        int prev2 = 0, prev1 = 0;
        for (int i = lo; i < hi; ++i) {
            int cur = max(prev1, prev2 + a[i]);    // skip i  vs  take i
            prev2 = prev1;
            prev1 = cur;
        }
        return prev1;
    }

public:
    int rob(vector<int>& nums) {                   // LC 198
        return robLine(nums, 0, static_cast<int>(nums.size()));
    }

    int robCircle(vector<int>& nums) {             // LC 213
        int n = nums.size();
        if (n == 1) return nums[0];
        return max(robLine(nums, 0, n - 1), robLine(nums, 1, n));
    }
};
```

**Complexity:** Time O(n), Space O(1). The circular version is two passes, still O(n).

**Follow-ups:**
- *Which houses were robbed?* Keep the full `dp` array and walk back from `i = n`. If `dp[i] == dp[i-1]`, house `i-1` was skipped, so step to `i-1`. Otherwise it was taken, so record it and step to `i-2`.
- *Delete and Earn (LC 740):* taking value `v` deletes every `v-1` and `v+1`. Bucket the input as `points[v] = v · count(v)` and run House Robber over `v = 0..max`. That is O(n + maxV).
- *Tree-shaped houses:* see [Problem 6](#problem-6-house-robber-iii-lc-337--medium-tree-dp). Each node returns a `(rob, skip)` pair instead of reading `dp[i-2]`.

---

#### Problem 15: Decode Ways (LC 91) — Medium (1D Fixed-Width Segmentation)

**Link:** https://leetcode.com/problems/decode-ways/

**Statement:** Letters are encoded as `'A' → "1"`, ..., `'Z' → "26"`. Given a digit string `s`, count the ways to decode it. `"06"` is **not** a valid encoding of `F`, because a code never has a leading zero.

**Intuition:** Let `dp[i]` be the number of decodings of the prefix `s[0..i-1]`, with `dp[0] = 1` (the empty prefix has one decoding). The last letter covers either:
- **one digit** `s[i-1]`, valid when it is `'1'..'9'`, contributing `dp[i-1]`; or
- **two digits** `s[i-2..i-1]`, valid when the value is `10..26` (which rules out a leading `'0'`), contributing `dp[i-2]`.

`dp[i]` is the sum of the valid options. This is Climbing Stairs (steps of 1 or 2) with a validity gate on each step. Every bug in this problem comes from zeros:

| Input | Answer | Why |
|---|---|---|
| `"12"` | 2 | `1 2` (AB), `12` (L) |
| `"226"` | 3 | `2 2 6`, `22 6`, `2 26` |
| `"06"` | 0 | `'0'` alone is invalid, and `"06"` is not in 10..26 |
| `"10"` | 1 | only `10` |
| `"100"` | 0 | the final `'0'` cannot stand alone, and `"00"` is invalid |
| `"27"` | 1 | 27 > 26 |

**Worked example** `s = "2101"`: `dp[0] = 1`, `dp[1] = 1` (`2`). At `i = 2`, `'1'` alone gives +1 and `"21"` gives +1, so `dp[2] = 2`. At `i = 3`, `'0'` alone is invalid and `"10"` gives `+dp[1]`, so `dp[3] = 1`. At `i = 4`, `'1'` gives `+dp[3]` and `"01"` is invalid, so `dp[4] = 1`. The only decoding is `2 10 1` (BJA).

**Python Solution:**

```python
class Solution:
    def numDecodings(self, s: str) -> int:
        prev2, prev1 = 1, 1          # dp[i-2], dp[i-1]; dp[0] = 1 (empty prefix)
        for i in range(1, len(s) + 1):
            cur = 0
            if s[i - 1] != '0':                          # last char decoded alone
                cur += prev1
            if i >= 2 and 10 <= int(s[i - 2:i]) <= 26:  # last two chars as one letter
                cur += prev2
            prev2, prev1 = prev1, cur
        return prev1
```

At `i = 1` the variables read as `prev1 = dp[0] = 1`, and `prev2` is unused because of the `i >= 2` guard. A leading `'0'` therefore yields `dp[1] = 0` and the result is 0, as required.

**C++ Solution:**

```cpp
#include <string>
using namespace std;

class Solution {
public:
    int numDecodings(string s) {
        int prev2 = 1, prev1 = 1;                  // dp[i-2], dp[i-1]; dp[0] = 1
        for (size_t i = 1; i <= s.size(); ++i) {
            int cur = 0;
            if (s[i - 1] != '0') cur += prev1;     // single digit 1..9
            if (i >= 2) {
                int two = (s[i - 2] - '0') * 10 + (s[i - 1] - '0');
                if (two >= 10 && two <= 26) cur += prev2;   // two digits 10..26
            }
            prev2 = prev1;
            prev1 = cur;
        }
        return prev1;
    }
};
```

**Complexity:** Time O(n), Space O(1). LC 91 guarantees the answer fits in 32 bits (`n ≤ 100`). The count grows like Fibonacci, about 1.618^n for an all-`'1'` string, so longer inputs need a modulus or big integers.

**Follow-up — Decode Ways II (LC 639):** `'*'` stands for any digit `1..9`, and the answer is taken mod 10^9 + 7. The recurrence stays the same and only the multipliers change. As a single character, `'*'` gives 9 ways and a nonzero digit gives 1. As a pair, `"**"` gives 15 (11–19 and 21–26), `"*d"` gives 2 if `d ≤ 6` and 1 otherwise, `"1*"` gives 9, `"2*"` gives 6, and any other `"x*"` gives 0.

---

#### Problem 16: Word Break (LC 139) — Medium (1D Variable-Width Segmentation)

**Link:** https://leetcode.com/problems/word-break/

**Statement:** Given a string `s` and a dictionary `wordDict`, return `true` if `s` can be split into a sequence of one or more dictionary words. Words may be reused.

**Intuition:** Let `dp[i]` be `True` when `s[0..i-1]` can be segmented, with `dp[0] = True`. The last word is some `s[j..i-1]`, so `dp[i] = OR over j < i of (dp[j] and s[j:i] in dict)`. The last word is at most `L = max word length` long, so only `j ≥ i - L` needs checking. Without that bound the scan is O(n^2) substrings, each costing O(n) to hash, which is O(n^3).

Plain recursion "try every prefix word, recurse on the rest" is exponential. On `s = "aaaa...ab"` with `dict = {"a", "aa", "aaa"}`, the same suffix is re-explored through every split. Memoising on the start index turns it into this same DP.

**Worked example** `s = "catsandog"`, `dict = {cats, dog, sand, and, cat}`: `dp[0] = T`. `dp[3] = T` (`cat`), `dp[4] = T` (`cats`), `dp[7] = T` (`sand` from 3, or `and` from 4). Reaching 9 needs `dog = s[6:9]` with `dp[6]`, but `dp[6] = F`. Also `og` is not a word, so `dp[9] = F` and the answer is `false`.

**Python Solution:**

```python
class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> bool:
        words = set(wordDict)
        max_len = max(map(len, words))
        n = len(s)
        dp = [True] + [False] * n                        # dp[i]: s[:i] can be segmented
        for i in range(1, n + 1):
            for j in range(max(0, i - max_len), i):      # last word is s[j:i]
                if dp[j] and s[j:i] in words:
                    dp[i] = True
                    break
        return dp[n]
```

**C++ Solution:**

```cpp
#include <algorithm>
#include <string>
#include <string_view>
#include <unordered_set>
#include <vector>
using namespace std;

class Solution {
public:
    bool wordBreak(string s, vector<string>& wordDict) {
        // The string_views point into wordDict and s, which stay alive for the whole call.
        unordered_set<string_view> words(wordDict.begin(), wordDict.end());
        size_t maxLen = 0;
        for (const string& w : wordDict) maxLen = max(maxLen, w.size());

        string_view sv(s);
        int n = s.size();
        vector<char> dp(n + 1, 0);                 // dp[i]: s[0, i) can be segmented
        dp[0] = 1;
        for (int i = 1; i <= n; ++i) {
            int lo = max(0, i - static_cast<int>(maxLen));
            for (int j = i - 1; j >= lo && !dp[i]; --j)   // last word is s[j, i)
                if (dp[j] && words.count(sv.substr(j, i - j))) dp[i] = 1;
        }
        return dp[n];
    }
};
```

`string_view` keys avoid allocating a new `std::string` for every candidate substring. `vector<char>` is used instead of `vector<bool>` so each element is a real byte and access avoids bit masking.

**Complexity:** Time O(n · L^2) with hashing: n end positions, up to L start positions each, and O(L) to hash each candidate. Space O(n) plus the dictionary. With `n ≤ 300` and `L ≤ 20` (LC limits) that is about 10^5 character operations.

**Follow-ups:**
- *Huge dictionary or long words:* put the words in a **trie** ([Pattern 17](#17-trie-prefix-tree)) and run the DP **forward**. From every `j` with `dp[j] = True`, walk the trie along `s[j:]` and set `dp[j + len] = True` at each end-of-word node. That costs O(n · L) total character steps with no substring allocation or hashing. Rolling hashes ([Pattern 30](#30-string-hashing--matching-in-practice)) are the other way to get O(1) substring lookups.
- *Word Break II (LC 140), return all sentences:* memoise `start → list of sentences for s[start:]`. The **output** can be exponential: `s = "aaaa"` with `{a, aa, aaa, aaaa}` has 2^(n-1) = 8 sentences. No algorithm beats output size, so first run the boolean DP above and return `[]` immediately when `dp[n]` is false. That avoids building huge partial lists on unsolvable inputs.

```python
# fragment: Word Break II (LC 140)
from functools import lru_cache

def word_break_all(s: str, word_dict: list[str]) -> list[str]:
    words = set(word_dict)

    @lru_cache(maxsize=None)
    def go(start: int) -> list[str]:                     # all sentences for s[start:]
        if start == len(s):
            return [""]
        out = []
        for end in range(start + 1, len(s) + 1):
            w = s[start:end]
            if w in words:
                for rest in go(end):
                    out.append(w + (" " + rest if rest else ""))
        return out

    return go(0)
```

- *BFS view:* the indices `0..n` are nodes, and there is an edge `j → i` when `s[j:i]` is a word. LC 139 asks whether `n` is reachable from `0`. Minimum number of words is the same graph with BFS or a min-DP.

---

#### Problem 17: Longest Palindromic Substring (LC 5) — Medium (Interval DP vs. Expand-Around-Center)

**Link:** https://leetcode.com/problems/longest-palindromic-substring/

**Statement:** Return the longest **contiguous** palindromic substring of `s` (`1 ≤ n ≤ 1000`). If several have the maximal length, any one is accepted.

**Intuition (DP view):** Let `pal[i][j]` be true when `s[i..j]` is a palindrome. Then `pal[i][j] = (s[i] == s[j]) and (j - i < 2 or pal[i+1][j-1])`. That is an interval DP: each cell depends on the strictly shorter interval inside it, so fill the table **by increasing length**, or with `i` descending and `j` ascending. It takes O(n^2) time and O(n^2) space, which is 10^6 cells for `n = 1000`.

**Intuition (expand-around-center):** Every palindrome is symmetric around a center. There are `2n - 1` centers: `n` characters for odd lengths and `n - 1` gaps for even lengths. From each center, expand while `s[lo] == s[hi]`. This visits the same `(i, j)` pairs the DP would mark true, but needs no table. The worst case is still O(n^2) (`"aaaa…a"`), but space drops to O(1) and the constant is small. This is the solution interviewers usually expect.

**Worked example** `s = "babad"`: the odd center at index 1 (`a`) expands to `bab`. The odd center at index 2 (`b`) expands to `aba`. Neither can grow further, so the answer is `bab` (or `aba`, both have length 3). For `s = "cbbd"`, no odd center yields more than 1, and the even center between indices 1 and 2 gives `bb`. Forgetting the even centers is the classic bug: it returns `"c"` here.

**Python Solution (expand-around-center):**

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        def expand(lo: int, hi: int) -> tuple[int, int]:
            while lo >= 0 and hi < len(s) and s[lo] == s[hi]:
                lo -= 1
                hi += 1
            return lo + 1, hi                            # palindrome is s[lo+1:hi]

        best_lo, best_hi = 0, 0
        for c in range(len(s)):
            for lo, hi in (expand(c, c), expand(c, c + 1)):   # odd centre, even centre
                if hi - lo > best_hi - best_lo:
                    best_lo, best_hi = lo, hi
        return s[best_lo:best_hi]
```

**Python Solution (interval DP table, for comparison):**

```python
def longest_palindrome_dp(s: str) -> str:
    n = len(s)
    if n == 0:
        return ""
    pal = [[False] * n for _ in range(n)]                # pal[i][j]: s[i..j] is a palindrome
    best_i, best_len = 0, 1
    for length in range(1, n + 1):                       # fill by increasing length
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and (length <= 2 or pal[i + 1][j - 1]):
                pal[i][j] = True
                if length > best_len:
                    best_i, best_len = i, length
    return s[best_i:best_i + best_len]
```

**C++ Solution (expand-around-center):**

```cpp
#include <string>
using namespace std;

class Solution {
public:
    string longestPalindrome(string s) {
        int n = s.size(), bestLo = 0, bestLen = 0;
        auto expand = [&](int lo, int hi) {
            while (lo >= 0 && hi < n && s[lo] == s[hi]) { --lo; ++hi; }
            int len = hi - lo - 1;                 // palindrome is s[lo+1, hi)
            if (len > bestLen) { bestLen = len; bestLo = lo + 1; }
        };
        for (int c = 0; c < n; ++c) {
            expand(c, c);                          // odd length, centre at c
            expand(c, c + 1);                      // even length, centre between c and c+1
        }
        return s.substr(bestLo, bestLen);
    }
};
```

**Complexity:**

| Approach | Time | Space | When to use |
|---|---|---|---|
| Brute force (check every substring) | O(n^3) | O(1) | Never. Mention it only as the baseline |
| Interval DP table | O(n^2) | O(n^2) | When the table is reused, e.g. Palindrome Partitioning II (LC 132) needs `pal[i][j]` for every pair |
| Expand-around-center | O(n^2) worst, near O(n) on random text | O(1) | Default interview answer |
| Hashing + binary search on length | O(n log n) expected | O(n) | Follow-up. Search odd and even lengths **separately**, because "a palindrome of length k exists" is monotone only within one parity (a length-k palindrome contains one of length k-2) |
| Manacher | O(n) | O(n) | When asked for linear time. See [DSA Fundamentals: Manacher's Algorithm](DSA_Fundamentals.md#manachers-algorithm) |

**Related:** Palindromic Substrings (LC 647) counts palindromes with the same expansion, adding 1 for every successful step. Longest Palindromic **Subsequence** (LC 516) is a different problem, because characters need not be contiguous. Its interval DP is `dp[i][j] = dp[i+1][j-1] + 2` if `s[i] == s[j]`, else `max(dp[i+1][j], dp[i][j-1])` ([sub-pattern 8](#8-interval-dp)). It also equals `LCS(s, reverse(s))`.

---

### Interview Q&A

**Q1.** How do you recognise interval DP, and why is "which balloon goes last" the key in Burst Balloons?

Signals: the input is a sequence, an operation **merges or removes** adjacent elements, and its cost depends on the current neighbours or on the merged segment (matrix chain, merging stones, polygon triangulation, palindromic subsequence). The state is a range `[l, r]`. The split choice must make the two sides **independent**. Choosing the first balloon to burst does not, because afterwards its neighbours become adjacent and interact. Choosing the last one does: until it bursts, it separates the left and right sides, and when it bursts, its neighbours are exactly the fixed boundaries `l` and `r`. Whenever a "first choice" formulation creates interaction, try the "last choice" view.

**Q2.** Derive the stock state machine for "at most k transactions with a cooldown". How big is the state?

States per day: for each `j = 0..k` completed transactions, `{not holding & free, holding, just sold (cooldown)}`. Transitions: `hold[j] = max(hold[j], free[j] - p)`, `sold[j+1] = hold[j] + p`, `free[j] = max(free[j], sold[j])`, using the previous day's values for all of them. That is O(k) states per day, O(nk) time, O(k) space. Draw the state diagram first, label each arrow with its cash change, then translate each arrow into one `max` term. That method extends to any new rule (fees, a maximum holding period) without memorising formulas.

**Q3.** Coin Change II (LC 518) counts combinations, while Combination Sum IV (LC 377) counts ordered sequences. How does the loop order produce each?

Combinations: **outer loop over coins**, inner loop over amounts upward (unbounded): `for c in coins: for s in range(c, amount+1): ways[s] += ways[s-c]`. Each combination is built in a fixed coin order, so it is counted once. Permutations: **outer loop over amounts**, inner loop over coins: `for s in range(1, amount+1): for c in coins: ways[s] += ways[s-c]`. The last coin can be any coin, so different orders are counted separately. For 0/1 (each item once), keep the item loop outside and iterate the amount **downwards**.

**Q4.** When is bitmask DP feasible, and how do you keep it fast?

States are `2^n × (extra)`. Rough limits: `2^n · n` works up to n ≈ 20–23 in C++ (2^20 · 20 ≈ 2 · 10^7), and `2^n · n^2` (TSP) up to n ≈ 16–20. Memory matters as much as time: `2^20 × 20` ints is 80 MiB. Tips: use flat arrays indexed `mask * n + j`; iterate masks in increasing order (every transition adds bits, so sources come first); enumerate submasks with `sub = (sub - 1) & mask` when transitions remove a subset, which gives O(3^n) total; and prune unreachable states as in LC 698.

**Q5.** Why does digit DP need the `tight` flag, and why memoise only non-tight states?

`tight` records whether the digits chosen so far equal `N`'s prefix. If so, the next digit is capped at `N`'s digit; otherwise any digit 0–9 is allowed, and the rest of the count no longer depends on `N`. That is why non-tight states with the same `(pos, property_state)` share one answer. Tight states lie on a single path (exactly `N`'s prefix), so each is visited once and memoising them gains nothing. Many solutions memoise without `tight` in the key **and** only when not tight, which is exactly this observation. For ranges use `count(R) - count(L - 1)`. Add a `started` flag when leading zeros would change the property (for example "all digits distinct": `007` is really `7`).

**Q6.** What is "rerooting" in tree DP?

Some questions ask for an answer **for every node as the root** (LC 834 Sum of Distances in Tree: for each node, the sum of distances to all others). Running a tree DP from each root is O(n^2). Rerooting does two passes: a post-order pass computes subtree sizes and the answer for root 0; then a pre-order pass moves the root from parent `p` to child `c` with an O(1) formula. For LC 834, `ans[c] = ans[p] - size[c] + (n - size[c])`: the `size[c]` nodes in `c`'s subtree get one step closer, and the other `n - size[c]` nodes one step farther. Total O(n).

**Q7.** For a 1D DP like House Robber, how do you derive the recurrence on the spot instead of recalling it, and how do the variants change it?

Define the state as the answer for a **prefix**. Then ask what the last element's decision can be. For House Robber, the last house is either skipped, giving `dp[i-1]`, or taken, giving `dp[i-2] + a[i-1]`, because taking it forbids its neighbour. Check the base cases on the smallest inputs: `dp[0] = 0` and `dp[1] = a[0]`. Then spot that only two previous values are read, so two variables suffice. The variants each change one piece:
- **Circular (LC 213):** the first and last houses cannot both be taken, so solve two line problems, `a[1:]` and `a[:-1]`.
- **Delete and Earn (LC 740):** values become positions. Set `points[v] = v · count(v)` and rob over `v`.
- **Tree (LC 337):** "previous" means children, and each node returns a `(rob, skip)` pair.

Greedy fails on small inputs (`[2, 3, 2]`, `[2, 1, 1, 2]`). Showing one counterexample is how you justify using DP in an interview.

**Q8.** What is Word Break's real complexity, and what changes for a 10^5-word dictionary or for "return all segmentations"?

With a hash set and the start index capped at `i - L`, there are n · L candidate substrings, each costing O(L) to hash: O(n · L^2). Without the cap, a careless solution is O(n^3). For a large dictionary, the dictionary size does not enter the DP cost; it costs memory and O(total chars) to build the set. A **trie** with forward propagation brings the DP to O(n · L) character steps and avoids substring allocation. Word Break II has exponential **output** (`"aaaa…"` with `{a, aa, …}` has 2^(n-1) sentences). Memoise sentence lists per start index, and run the boolean DP first so unsolvable inputs return immediately. If only the **number** of segmentations is needed, switch from OR to `+` (taken modulo a prime if the count is large) and keep the same O(n · L^2).

**Q9.** Longest Palindromic Substring: DP table, expand-around-center, or Manacher — which do you code, and how do you justify it?

Code **expand-around-center**. It has the same O(n^2) worst case as the DP table, uses O(1) space instead of an n^2 table (10^6 booleans at n = 1000), and has about 15 lines with one subtle point: the `2n - 1` centers, which include even ones. Mention the DP recurrence `pal[i][j] = s[i] == s[j] and pal[i+1][j-1]` to show you see the interval structure, and say you would build the table when it is **reused**. Palindrome Partitioning II (LC 132), for example, needs `pal[i][j]` for every pair to drive `cuts[j] = min(cuts[i-1] + 1 for pal[i][j])`. If asked for better, there are two options. Hashing with a binary search per parity gives O(n log n) expected time. Manacher gives O(n): it reuses the mirror radius inside the rightmost known palindrome, so the right boundary only moves forward. Do not confuse LC 5 (substring, contiguous) with LC 516 (subsequence, interval DP, equal to the LCS of `s` and its reverse).

**Q10.** Decode Ways keeps failing hidden tests. What are the usual bugs?

(1) Treating `'0'` as a valid single digit. It is valid only as the second digit of `10` or `20`. (2) Checking `s[i-2] != '0'` and `int(two) <= 26` but forgetting the lower bound, so `"06"` is wrongly counted. Using `10 <= two <= 26` covers both checks. (3) A wrong `dp[0]`. The empty prefix has exactly **1** decoding, and setting it to 0 zeroes every answer. (4) Returning early on a zero when the string can still recover (`"10"` is valid). An answer becomes 0 only when **both** options are invalid at some `i`, for example `"100"` or `"30"`. Test with `"0"`, `"10"`, `"100"`, `"27"`, `"226"`, `"2101"`, and a long run of `'1'`s for overflow (Fibonacci growth).

---
## 19. Greedy

### Overview

Greedy algorithms make **locally optimal choices at each step**, hoping to reach a globally optimal solution. Unlike dynamic programming, greedy doesn't consider future consequences or revisit decisions — once a choice is made, it's final.

Greedy works when the problem exhibits two properties:

1. **Greedy Choice Property** — a locally optimal choice at each step leads to a globally optimal solution. You never need to reconsider a past decision.
2. **Optimal Substructure** — an optimal solution to the problem contains optimal solutions to its subproblems (shared with DP).

Proving a greedy algorithm is correct typically requires one of:

- **Exchange Argument**: assume an optimal solution differs from greedy's solution, then show you can "exchange" a decision in the optimal solution for the greedy decision without making things worse.
- **Greedy Stays Ahead**: show by induction that after each step, the greedy solution is at least as good as any other solution.

**Key insight**: greedy is a special case of DP where only one subproblem needs to be solved at each step and backtracking is never necessary.

### When to Use

- Activity / interval selection and scheduling
- Minimum coins (with canonical coin systems like US denominations)
- Jump game variants
- Task scheduling with deadlines
- Huffman coding (optimal prefix codes)
- Fractional knapsack
- Gas station / circular route problems
- Minimum platforms at a station
- Assigning cookies / resources to consumers
- Any problem where sorting + single-pass scan produces the answer

### Template Code

**General Greedy Template** — sort the input by the criterion that enables locally optimal choices, then iterate making the best choice at each step:

```python
# Python — General Greedy Template
def greedy_solve(items):
    items.sort(key=lambda x: sorting_criterion(x))

    result = initial_value
    for item in items:
        if can_choose(item, result):
            result = update(result, item)
    return result
```

```cpp
// C++ — General Greedy Template
#include <algorithm>
#include <vector>
using namespace std;

int greedySolve(vector<pair<int,int>>& items) {
    sort(items.begin(), items.end(), [](auto& a, auto& b) {
        return sortingCriterion(a) < sortingCriterion(b);
    });

    int result = initialValue;
    for (auto& item : items) {
        if (canChoose(item, result)) {
            result = update(result, item);
        }
    }
    return result;
}
```

**Canonical Example — Interval Scheduling (Maximum Non-Overlapping Intervals)**:

Sort intervals by **end time**. Greedily pick the interval that finishes earliest, then skip all intervals that overlap with it.

```python
# Python — Interval Scheduling (max non-overlapping intervals)
def max_non_overlapping(intervals):
    intervals.sort(key=lambda x: x[1])  # sort by end time

    count = 0
    last_end = float('-inf')
    for start, end in intervals:
        if start >= last_end:  # no overlap
            count += 1
            last_end = end
    return count
```

```cpp
// C++ — Interval Scheduling (max non-overlapping intervals)
#include <algorithm>
#include <vector>
using namespace std;

int maxNonOverlapping(vector<vector<int>>& intervals) {
    sort(intervals.begin(), intervals.end(), [](auto& a, auto& b) {
        return a[1] < b[1];  // sort by end time
    });

    int count = 0;
    int lastEnd = INT_MIN;
    for (auto& iv : intervals) {
        if (iv[0] >= lastEnd) {
            count++;
            lastEnd = iv[1];
        }
    }
    return count;
}
```

### Variations

| Variation | Key Idea | Example |
|-----------|----------|---------|
| **Interval Scheduling** | Sort by end time, pick earliest-finishing | Activity Selection, Non-overlapping Intervals |
| **Greedy with Sorting** | Sort by a custom criterion, then scan | Assign Cookies, Boats to Save People |
| **Greedy with Heaps** | Use a priority queue to always pick the best available | Task Scheduler, Reorganize String |
| **Two-Pass Greedy** | Scan left-to-right then right-to-left | Candy, Trapping Rain Water |
| **Greedy Counting** | Count or track a running quantity | Gas Station, Jump Game |

### Common Mistakes

1. **Applying greedy when DP is needed** — if the problem lacks the greedy choice property (e.g., 0/1 Knapsack, general coin change), greedy gives wrong answers. Always verify correctness.
2. **Wrong sorting criterion** — sorting by start time instead of end time in interval scheduling, or sorting by the wrong attribute in multi-attribute problems.
3. **Not proving correctness** — "it seems right" isn't a proof. Use exchange argument or greedy-stays-ahead for rigorous validation.
4. **Ignoring edge cases** — empty arrays, single-element inputs, all-identical elements, negative numbers.
5. **Confusing fractional vs 0/1 problems** — fractional knapsack is greedy, 0/1 knapsack requires DP.

### Related Patterns

- **Dynamic Programming** — when greedy fails, DP considers all subproblems
- **Sorting** — most greedy algorithms start with sorting
- **Merge Intervals** — interval-based greedy problems overlap heavily

### Example Problems

#### 1. Assign Cookies (LC 455) — Easy

**Problem**: You are a parent with cookies of various sizes and children with various greed factors. Each child `i` has a greed factor `g[i]` — the minimum cookie size that will make them content. Each cookie `j` has size `s[j]`. If `s[j] >= g[i]`, you can assign cookie `j` to child `i` and the child becomes content. Maximize the number of content children.

**LeetCode**: [https://leetcode.com/problems/assign-cookies/](https://leetcode.com/problems/assign-cookies/)

**Intuition**: Sort both arrays. Use the smallest cookie that can satisfy the least greedy child first. This way we preserve larger cookies for greedier children, maximizing total assignments.

```python
# Python — Assign Cookies
class Solution:
    def findContentChildren(self, g: list[int], s: list[int]) -> int:
        g.sort()
        s.sort()

        child = 0
        cookie = 0
        while child < len(g) and cookie < len(s):
            if s[cookie] >= g[child]:
                child += 1  # child is content
            cookie += 1      # move to next cookie either way
        return child
```

```cpp
// C++ — Assign Cookies
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int findContentChildren(vector<int>& g, vector<int>& s) {
        sort(g.begin(), g.end());
        sort(s.begin(), s.end());

        int child = 0, cookie = 0;
        while (child < (int)g.size() && cookie < (int)s.size()) {
            if (s[cookie] >= g[child]) {
                child++;
            }
            cookie++;
        }
        return child;
    }
};
```

**Complexity**: Time O(n log n + m log m) for sorting. Space O(1) ignoring sort internals.

---

#### 2. Jump Game (LC 55) — Medium

**Problem**: Given an integer array `nums` where each element represents the maximum jump length from that position, determine if you can reach the last index starting from index 0.

**LeetCode**: [https://leetcode.com/problems/jump-game/](https://leetcode.com/problems/jump-game/)

**Intuition**: Track the farthest index reachable so far. Iterate through the array; at each position, if the current index is beyond the farthest reachable, we're stuck. Otherwise, update the farthest reachable as `max(farthest, i + nums[i])`.

```python
# Python — Jump Game
class Solution:
    def canJump(self, nums: list[int]) -> bool:
        farthest = 0
        for i in range(len(nums)):
            if i > farthest:
                return False
            farthest = max(farthest, i + nums[i])
        return True
```

```cpp
// C++ — Jump Game
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    bool canJump(vector<int>& nums) {
        int farthest = 0;
        for (int i = 0; i < (int)nums.size(); i++) {
            if (i > farthest) return false;
            farthest = max(farthest, i + nums[i]);
        }
        return true;
    }
};
```

**Complexity**: Time O(n). Space O(1).

---

#### 3. Jump Game II (LC 45) — Medium

**Problem**: Given an array `nums` where each element represents the maximum jump length, return the **minimum number of jumps** to reach the last index. You can always reach the last index.

**LeetCode**: [https://leetcode.com/problems/jump-game-ii/](https://leetcode.com/problems/jump-game-ii/)

**Intuition**: Think of it like BFS by levels. Maintain a "current level end" and a "farthest reachable." When you reach the current level end, you must take another jump — increment jumps and set the new level end to the farthest reachable.

```python
# Python — Jump Game II
class Solution:
    def jump(self, nums: list[int]) -> int:
        jumps = 0
        current_end = 0
        farthest = 0

        for i in range(len(nums) - 1):  # don't need to jump from last index
            farthest = max(farthest, i + nums[i])
            if i == current_end:
                jumps += 1
                current_end = farthest
        return jumps
```

```cpp
// C++ — Jump Game II
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int jump(vector<int>& nums) {
        int jumps = 0, currentEnd = 0, farthest = 0;
        for (int i = 0; i < (int)nums.size() - 1; i++) {
            farthest = max(farthest, i + nums[i]);
            if (i == currentEnd) {
                jumps++;
                currentEnd = farthest;
            }
        }
        return jumps;
    }
};
```

**Complexity**: Time O(n). Space O(1).

---

#### 4. Gas Station (LC 134) — Medium

**Problem**: There are `n` gas stations along a circular route. Station `i` has `gas[i]` fuel and costs `cost[i]` to travel to the next station. Starting with an empty tank, find the starting station index to complete the circuit, or return -1 if impossible.

**LeetCode**: [https://leetcode.com/problems/gas-station/](https://leetcode.com/problems/gas-station/)

**Intuition**: If total gas ≥ total cost, a solution exists (and it's unique). To find the starting station: scan once, tracking the current tank. Whenever the tank goes negative, the start must be *after* this station — reset tank to 0 and set the candidate start to the next station.

```python
# Python — Gas Station
class Solution:
    def canCompleteCircuit(self, gas: list[int], cost: list[int]) -> int:
        if sum(gas) < sum(cost):
            return -1

        tank = 0
        start = 0
        for i in range(len(gas)):
            tank += gas[i] - cost[i]
            if tank < 0:
                start = i + 1
                tank = 0
        return start
```

```cpp
// C++ — Gas Station
#include <vector>
using namespace std;

class Solution {
public:
    int canCompleteCircuit(vector<int>& gas, vector<int>& cost) {
        int totalSurplus = 0, tank = 0, start = 0;
        for (int i = 0; i < (int)gas.size(); i++) {
            int diff = gas[i] - cost[i];
            totalSurplus += diff;
            tank += diff;
            if (tank < 0) {
                start = i + 1;
                tank = 0;
            }
        }
        return totalSurplus >= 0 ? start : -1;
    }
};
```

**Complexity**: Time O(n). Space O(1).

---

#### 5. Candy (LC 135) — Hard

**Problem**: There are `n` children standing in a line, each with a rating. You must give each child at least one candy. Children with a higher rating than their neighbor must get more candies than that neighbor. Return the minimum total candies needed.

**LeetCode**: [https://leetcode.com/problems/candy/](https://leetcode.com/problems/candy/)

**Intuition**: Two-pass greedy. First pass left-to-right: if `ratings[i] > ratings[i-1]`, give one more candy than the left neighbor. Second pass right-to-left: if `ratings[i] > ratings[i+1]`, ensure at least one more candy than the right neighbor (take max with current assignment). Each pass handles one direction of the constraint.

```python
# Python — Candy
class Solution:
    def candy(self, ratings: list[int]) -> int:
        n = len(ratings)
        candies = [1] * n

        # Left-to-right: satisfy right-neighbor-greater constraint
        for i in range(1, n):
            if ratings[i] > ratings[i - 1]:
                candies[i] = candies[i - 1] + 1

        # Right-to-left: satisfy left-neighbor-greater constraint
        for i in range(n - 2, -1, -1):
            if ratings[i] > ratings[i + 1]:
                candies[i] = max(candies[i], candies[i + 1] + 1)

        return sum(candies)
```

```cpp
// C++ — Candy
#include <vector>
#include <numeric>
#include <algorithm>
using namespace std;

class Solution {
public:
    int candy(vector<int>& ratings) {
        int n = ratings.size();
        vector<int> candies(n, 1);

        for (int i = 1; i < n; i++) {
            if (ratings[i] > ratings[i - 1]) {
                candies[i] = candies[i - 1] + 1;
            }
        }

        for (int i = n - 2; i >= 0; i--) {
            if (ratings[i] > ratings[i + 1]) {
                candies[i] = max(candies[i], candies[i + 1] + 1);
            }
        }

        return accumulate(candies.begin(), candies.end(), 0);
    }
};
```

**Complexity**: Time O(n). Space O(n) for the candies array.

---

## 20. Bit Manipulation

### Overview

Bit manipulation uses **bitwise operators** — AND (`&`), OR (`|`), XOR (`^`), NOT (`~`), left shift (`<<`), and right shift (`>>`) — to solve problems in **O(1) space** and often **O(n)** or **O(log n)** time. It exploits the binary representation of numbers for extremely efficient computation.

**Essential Properties and Identities**:

| Property | Expression | Result |
|----------|-----------|--------|
| XOR with itself | `x ^ x` | `0` |
| XOR with zero | `x ^ 0` | `x` |
| XOR is commutative & associative | `a ^ b ^ c = c ^ a ^ b` | order doesn't matter |
| AND with (n-1) | `n & (n-1)` | removes lowest set bit |
| AND to isolate lowest set bit | `n & (-n)` | lowest set bit only |
| Left shift by k | `x << k` | `x × 2^k` |
| Right shift by k | `x >> k` | `x ÷ 2^k` (floor) |
| Check if power of 2 | `n > 0 && (n & (n-1)) == 0` | `true` if power of 2 |
| Get i-th bit | `(n >> i) & 1` | 0 or 1 |
| Set i-th bit | `n \| (1 << i)` | sets bit i to 1 |
| Clear i-th bit | `n & ~(1 << i)` | sets bit i to 0 |
| Toggle i-th bit | `n ^ (1 << i)` | flips bit i |

### When to Use

- Finding single/unique number(s) in arrays where all others appear k times
- Power of 2 checks
- Counting set bits (Hamming weight)
- Reversing bits
- Generating all subsets via bitmask enumeration
- Detecting missing or duplicate numbers without extra space
- XOR-based tricks for swapping, toggling, and cancellation
- Problems requiring O(1) space with O(n) time

### Template Code

**1. XOR to Find Single Number**:

```python
# Python — Single Number via XOR
def single_number(nums):
    result = 0
    for num in nums:
        result ^= num
    return result
```

```cpp
// C++ — Single Number via XOR
int singleNumber(vector<int>& nums) {
    int result = 0;
    for (int num : nums) {
        result ^= num;
    }
    return result;
}
```

**2. Brian Kernighan's Algorithm — Count Set Bits**:

Each iteration `n &= (n - 1)` removes the lowest set bit. Count iterations until n becomes 0.

```python
# Python — Brian Kernighan's Algorithm
def count_set_bits(n):
    count = 0
    while n:
        n &= (n - 1)  # remove lowest set bit
        count += 1
    return count
```

```cpp
// C++ — Brian Kernighan's Algorithm
int countSetBits(unsigned int n) {
    int count = 0;
    while (n) {
        n &= (n - 1);
        count++;
    }
    return count;
}
```

**3. Check if Power of 2**:

A power of 2 has exactly one set bit. `n & (n-1)` clears that bit, leaving 0.

```python
# Python — Power of Two Check
def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0
```

```cpp
// C++ — Power of Two Check
bool isPowerOfTwo(int n) {
    return n > 0 && (n & (n - 1)) == 0;
}
```

### Variations

| Variation | Technique | Example |
|-----------|-----------|---------|
| **Single Number (XOR all)** | XOR cancels pairs | LC 136 |
| **Two Single Numbers** | XOR all → split by distinguishing bit → XOR each group | LC 260 |
| **Count Bits Modulo k** | Track bit counts across all numbers mod k | LC 137 (k=3) |
| **Counting Bits** | DP with `dp[i] = dp[i & (i-1)] + 1` | LC 338 |
| **Bitmask for Subsets** | Enumerate `0` to `2^n - 1`, check each bit | Subset generation |
| **Bit Tricks** | Lowest set bit `n & (-n)`, highest set bit via shifts | Various |

### Common Mistakes

1. **Signed vs unsigned confusion in C++** — right shift on signed integers is **arithmetic** (preserves sign bit), on unsigned it's **logical** (fills with 0). Use `unsigned int` or `uint32_t` when shifting right on negative numbers.
2. **Python's arbitrary-precision integers** — Python integers have unlimited width, so `~x` gives `-(x+1)` rather than a 32-bit complement. Mask with `& 0xFFFFFFFF` for 32-bit behavior.
3. **Operator precedence in C++** — `&`, `|`, `^` have **lower precedence than `==` and `!=`**. Write `(n & (n-1)) == 0`, not `n & (n-1) == 0` (the latter checks `n & 0` or `n & 1`).
4. **Not handling negative numbers** — two's complement representation can cause unexpected behavior with shifts and masks. Be explicit about bit width.
5. **Overflow with left shifts** — `1 << 31` in C++ with a signed 32-bit int is undefined behavior. Use `1u << 31` or `1LL << 31`.

### Related Patterns

- **Math** — many bit tricks are algebraic identities in disguise
- **Cyclic Sort** — finding missing/duplicate numbers can also use XOR
- **Bitmask DP** — using bitmasks to represent state in dynamic programming

### Example Problems

#### 1. Single Number (LC 136) — Easy

**Problem**: Given a non-empty array of integers `nums` where every element appears exactly **twice** except for one element that appears once, find that single element. You must use O(1) extra space.

**LeetCode**: [https://leetcode.com/problems/single-number/](https://leetcode.com/problems/single-number/)

**Intuition**: XOR all elements together. Since `a ^ a = 0` and `a ^ 0 = a`, all pairs cancel out, leaving only the unique number. XOR is commutative and associative, so order doesn't matter.

```python
# Python — Single Number
class Solution:
    def singleNumber(self, nums: list[int]) -> int:
        result = 0
        for num in nums:
            result ^= num
        return result
```

```cpp
// C++ — Single Number
#include <vector>
using namespace std;

class Solution {
public:
    int singleNumber(vector<int>& nums) {
        int result = 0;
        for (int num : nums) {
            result ^= num;
        }
        return result;
    }
};
```

**Complexity**: Time O(n). Space O(1).

---

#### 2. Number of 1 Bits (LC 191) — Easy

**Problem**: Write a function that takes the binary representation of a positive integer and returns the number of set bits (1s) it has (also known as the Hamming weight).

**LeetCode**: [https://leetcode.com/problems/number-of-1-bits/](https://leetcode.com/problems/number-of-1-bits/)

**Intuition**: Use Brian Kernighan's algorithm. Each `n & (n - 1)` operation removes exactly one set bit (the lowest). Count how many operations it takes until `n` becomes 0. This runs in O(k) where k is the number of set bits — at most O(log n) = O(32) for 32-bit integers.

```python
# Python — Number of 1 Bits
class Solution:
    def hammingWeight(self, n: int) -> int:
        count = 0
        while n:
            n &= (n - 1)
            count += 1
        return count
```

```cpp
// C++ — Number of 1 Bits
class Solution {
public:
    int hammingWeight(int n) {
        int count = 0;
        while (n) {
            n &= (n - 1);
            count++;
        }
        return count;
    }
};
```

**Complexity**: Time O(log n), specifically O(number of set bits) ≤ 32. Space O(1).

---

#### 3. Power of Two (LC 231) — Easy

**Problem**: Given an integer `n`, return `true` if it is a power of two, otherwise return `false`. A power of two has exactly one `1` bit in binary (e.g., 1=`1`, 2=`10`, 4=`100`, 8=`1000`).

**LeetCode**: [https://leetcode.com/problems/power-of-two/](https://leetcode.com/problems/power-of-two/)

**Intuition**: A power of 2 in binary is `100...0` (a single 1 followed by zeros). Subtracting 1 flips all bits below that 1: `011...1`. ANDing them gives 0. So `n & (n - 1) == 0` for powers of 2. We also need `n > 0` since 0 is not a power of 2.

```python
# Python — Power of Two
class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        return n > 0 and (n & (n - 1)) == 0
```

```cpp
// C++ — Power of Two
class Solution {
public:
    bool isPowerOfTwo(int n) {
        return n > 0 && (n & (n - 1)) == 0;
    }
};
```

**Complexity**: Time O(1). Space O(1).

---

#### 4. Single Number II (LC 137) — Medium

**Problem**: Given an integer array `nums` where every element appears exactly **three times** except for one element that appears once, find that single element. You must use O(1) extra space.

**LeetCode**: [https://leetcode.com/problems/single-number-ii/](https://leetcode.com/problems/single-number-ii/)

**Intuition**: For each bit position (0 to 31), count how many numbers have that bit set. If a number appears 3 times, its contribution to each bit count is a multiple of 3. Taking count modulo 3 for each bit position gives the bits of the unique number.

Alternative (state machine): Use two variables `ones` and `twos` to track bit counts modulo 3. `ones` holds bits that have appeared 1 mod 3 times, `twos` holds bits that have appeared 2 mod 3 times.

```python
# Python — Single Number II (bit counting approach)
class Solution:
    def singleNumber(self, nums: list[int]) -> int:
        result = 0
        for i in range(32):
            bit_sum = 0
            for num in nums:
                bit_sum += (num >> i) & 1
            remainder = bit_sum % 3
            if i == 31:
                result -= remainder * (1 << i)  # handle sign bit
            else:
                result |= remainder << i
        return result
```

```python
# Python — Single Number II (state machine approach)
class Solution:
    def singleNumber(self, nums: list[int]) -> int:
        ones, twos = 0, 0
        for num in nums:
            ones = (ones ^ num) & ~twos
            twos = (twos ^ num) & ~ones
        return ones
```

```cpp
// C++ — Single Number II (bit counting approach)
#include <vector>
using namespace std;

class Solution {
public:
    int singleNumber(vector<int>& nums) {
        int result = 0;
        for (int i = 0; i < 32; i++) {
            int bitSum = 0;
            for (int num : nums) {
                bitSum += (num >> i) & 1;
            }
            if (bitSum % 3 != 0) {
                result |= (1 << i);
            }
        }
        return result;
    }
};
```

```cpp
// C++ — Single Number II (state machine approach)
#include <vector>
using namespace std;

class Solution {
public:
    int singleNumber(vector<int>& nums) {
        int ones = 0, twos = 0;
        for (int num : nums) {
            ones = (ones ^ num) & ~twos;
            twos = (twos ^ num) & ~ones;
        }
        return ones;
    }
};
```

**Complexity**: Time O(n) — the bit counting approach iterates 32 × n but 32 is constant. Space O(1).

---

#### 5. Single Number III (LC 260) — Medium

**Problem**: Given an integer array `nums` where exactly **two** elements appear only once and all other elements appear exactly twice, find the two unique elements. Return them in any order. You must use O(1) extra space.

**LeetCode**: [https://leetcode.com/problems/single-number-iii/](https://leetcode.com/problems/single-number-iii/)

**Intuition**: XOR all elements. Pairs cancel, leaving `xor_all = a ^ b` where `a` and `b` are the two unique numbers. Since `a ≠ b`, at least one bit in `xor_all` is set — this bit differs between `a` and `b`. Use it to partition all numbers into two groups: one group has that bit set, the other doesn't. XOR within each group to isolate `a` and `b` separately.

To find a distinguishing bit efficiently, use `xor_all & (-xor_all)` which isolates the lowest set bit.

```python
# Python — Single Number III
class Solution:
    def singleNumber(self, nums: list[int]) -> list[int]:
        xor_all = 0
        for num in nums:
            xor_all ^= num

        diff_bit = xor_all & (-xor_all)  # lowest set bit

        a, b = 0, 0
        for num in nums:
            if num & diff_bit:
                a ^= num
            else:
                b ^= num

        return [a, b]
```

```cpp
// C++ — Single Number III
#include <vector>
using namespace std;

class Solution {
public:
    vector<int> singleNumber(vector<int>& nums) {
        long long xorAll = 0;  // use long long to avoid overflow on INT_MIN
        for (int num : nums) {
            xorAll ^= num;
        }

        long long diffBit = xorAll & (-xorAll);

        int a = 0, b = 0;
        for (int num : nums) {
            if (num & diffBit) {
                a ^= num;
            } else {
                b ^= num;
            }
        }

        return {a, b};
    }
};
```

**Complexity**: Time O(n) — two passes through the array. Space O(1) not counting the output.

---

## 21. Prefix Sum & Difference Array

### Overview

A **prefix sum** array `P` stores running totals so that any contiguous range sum is answered in **O(1)** after **O(n)** preprocessing:

```text
P[0] = 0
P[i+1] = P[i] + a[i]            (P has n+1 entries)
sum(a[l..r]) = P[r+1] - P[l]    (inclusive l..r)
```

The **difference array** is the inverse operation. To add `v` to every element of `a[l..r]`, do `D[l] += v; D[r+1] -= v` in O(1). After all updates, one prefix-sum pass over `D` rebuilds the final array. This means **prefix sum turns range queries into O(1) point lookups, and the difference array turns range updates into O(1) point updates.**

The most interview-relevant form is **prefix sum + hash map**. A subarray `a[j..i]` sums to `k` exactly when `P[i+1] - P[j] = k`, i.e. `P[j] = P[i+1] - k`. While scanning left to right, keep a map from each prefix value seen so far to how many times it occurred (or the first index where it occurred). Each step does one O(1) lookup.

**Worked example** (`nums = [1, 2, 3]`, `k = 3`):

| i | x | running prefix | need `prefix - k` | count found | map after step |
|---|---|---|---|---|---|
| — | — | 0 | — | — | `{0:1}` (seed) |
| 0 | 1 | 1 | -2 | 0 | `{0:1, 1:1}` |
| 1 | 2 | 3 | 0 | 1 → `[1,2]` | `{0:1, 1:1, 3:1}` |
| 2 | 3 | 6 | 3 | 1 → `[3]` | `{0:1, 1:1, 3:1, 6:1}` |

Answer = 2. The seed `{0: 1}` stands for the empty prefix and is what lets subarrays that start at index 0 be counted.

**2D prefix sum** (inclusion–exclusion), with `P` of size `(m+1) x (n+1)`:

```text
P[i+1][j+1] = a[i][j] + P[i][j+1] + P[i+1][j] - P[i][j]
sum(r1..r2, c1..c2) = P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]
```

### When to Use

- "Sum of subarray `[l, r]`" asked many times on a **static** array
- "Count / longest subarrays with sum == k" when values can be **negative** (sliding window fails)
- "Subarray sum divisible by k" → prefix **mod** k with a hash map
- "Equal number of 0s and 1s" → map 0 to -1, then look for prefix balance 0
- "Add v to range [l, r]" many times, then read the final array → difference array
- Capacity checks over a timeline (passengers, bookings, bandwidth) → difference array + running sum
- Sub-rectangle sums in a matrix → 2D prefix sum

### Template Code

**1D prefix sum and range query**

```python
# Python — 1D prefix sum
from itertools import accumulate

def build_prefix(a: list[int]) -> list[int]:
    return [0] + list(accumulate(a))          # P[0] = 0

def range_sum(P: list[int], l: int, r: int) -> int:
    return P[r + 1] - P[l]                    # inclusive l..r

P = build_prefix([3, -1, 4, 1, 5])
assert range_sum(P, 1, 3) == 4                # -1 + 4 + 1
```

```cpp
// C++ — 1D prefix sum
#include <numeric>
#include <vector>
using namespace std;

vector<long long> buildPrefix(const vector<int>& a) {
    vector<long long> P(a.size() + 1, 0);     // long long: sums overflow int quickly
    for (size_t i = 0; i < a.size(); ++i) P[i + 1] = P[i] + a[i];
    return P;
}

long long rangeSum(const vector<long long>& P, int l, int r) {
    return P[r + 1] - P[l];                   // inclusive l..r
}
```

**Prefix sum + hash map (count subarrays with sum k)**

```python
# Python — prefix + hashmap template
from collections import defaultdict

def count_subarrays_with_sum(nums: list[int], k: int) -> int:
    seen = defaultdict(int)
    seen[0] = 1                    # empty prefix
    prefix = count = 0
    for x in nums:
        prefix += x
        count += seen[prefix - k]  # query BEFORE inserting the current prefix
        seen[prefix] += 1
    return count

assert count_subarrays_with_sum([1, 2, 3], 3) == 2
```

```cpp
// C++ — prefix + hashmap template
#include <unordered_map>
#include <vector>
using namespace std;

int countSubarraysWithSum(const vector<int>& nums, int k) {
    unordered_map<long long, int> seen{{0, 1}};
    long long prefix = 0;
    int count = 0;
    for (int x : nums) {
        prefix += x;
        auto it = seen.find(prefix - k);
        if (it != seen.end()) count += it->second;
        ++seen[prefix];
    }
    return count;
}
```

**Difference array (range add, then rebuild)**

```python
# Python — difference array
def apply_range_adds(n: int, updates: list[tuple[int, int, int]]) -> list[int]:
    diff = [0] * (n + 1)                 # extra slot absorbs r + 1 == n
    for l, r, v in updates:
        diff[l] += v
        diff[r + 1] -= v
    out, running = [], 0
    for i in range(n):
        running += diff[i]
        out.append(running)
    return out

assert apply_range_adds(5, [(1, 3, 2), (2, 4, 3), (0, 2, -2)]) == [-2, 0, 3, 5, 3]
```

```cpp
// C++ — difference array
#include <array>
#include <vector>
using namespace std;

vector<long long> applyRangeAdds(int n, const vector<array<int, 3>>& updates) {
    vector<long long> diff(n + 1, 0);
    for (const auto& [l, r, v] : updates) {
        diff[l] += v;
        diff[r + 1] -= v;
    }
    vector<long long> out(n);
    long long running = 0;
    for (int i = 0; i < n; ++i) out[i] = (running += diff[i]);
    return out;
}
```

### Variations

| Variation | Map / Array stores | Example Problems |
|---|---|---|
| **Static 1D range sum** | `P[i]` | Range Sum Query - Immutable (LC 303) |
| **Static 2D range sum** | `P[i][j]` (inclusion–exclusion) | Range Sum Query 2D (LC 304), Matrix Block Sum (LC 1314) |
| **Count subarrays with sum k** | prefix → count | Subarray Sum Equals K (LC 560), Binary Subarrays With Sum (LC 930), Count Number of Nice Subarrays (LC 1248) |
| **Longest subarray with property** | prefix → **first** index | Contiguous Array (LC 525), Maximum Size Subarray Sum Equals k (LC 325) |
| **Divisibility** | prefix mod k → count / first index | Continuous Subarray Sum (LC 523), Subarray Sums Divisible by K (LC 974) |
| **Prefix XOR** | `X[i] = a[0] ^ ... ^ a[i-1]` | XOR Queries of a Subarray (LC 1310) |
| **1D difference array** | `D[l] += v, D[r+1] -= v` | Car Pooling (LC 1094), Corporate Flight Bookings (LC 1109), Range Addition (LC 370) |
| **2D difference array** | four corner updates, then 2D prefix | Increment Submatrices by One (LC 2536) |
| **Prefix + binary search** | cumulative weights | Random Pick with Weight (LC 528) |
| **Prefix + monotonic deque** | increasing deque of prefix indices | Shortest Subarray with Sum at Least K (LC 862) |
| **Dynamic updates + queries** | Fenwick tree / segment tree | Range Sum Query - Mutable (LC 307) |

### Common Mistakes

1. **Forgetting the seed.** Counting needs `{0: 1}`; longest-length needs `{0: -1}`. Without it, subarrays starting at index 0 are missed.
2. **Inserting before querying.** With `k = 0`, inserting the current prefix first makes every position match itself and counts empty subarrays.
3. **Off-by-one in `P`.** Use size `n + 1` with `P[0] = 0` so that `sum(l..r) = P[r+1] - P[l]` has no special cases.
4. **Overwriting the first index** in "longest" problems. Store an index only if the key is absent; later indices give shorter subarrays.
5. **Negative modulo in C++.** `-7 % 3 == -1` in C++ but `2` in Python. Normalize with `((x % k) + k) % k`.
6. **Overflow.** `n = 10^5` values of `10^9` sum to `10^14`; use `long long`.
7. **Using a sliding window with negative numbers.** Shrinking the window no longer guarantees a smaller sum, so the two-pointer invariant breaks. Use prefix + hash map instead.
8. **Difference-array bounds.** Allocate `n + 1` (or `n + 2` for 1-indexed input) so `D[r+1]` never goes out of range.

### Related Patterns

- **Sliding Window** ([Pattern 2](#2-sliding-window)) — the O(1)-space alternative when all values are non-negative
- **Line Sweep** ([Pattern 25](#25-line-sweep--advanced-intervals)) — a difference array over a sparse or huge coordinate range is a sorted list of +v / -v events
- **Dynamic Programming** ([Pattern 18](#18-dynamic-programming)) — prefix sums speed up DP transitions that sum over a window
- **See also:** [Fenwick Trees](DSA_Fundamentals.md#12-fenwick-trees-binary-indexed-trees) and [Segment Trees](DSA_Fundamentals.md#11-segment-trees) for prefix sums with point updates; [MPI_Scan](../ml-gpu/Parallel_GPU_Programming.md#mpi_scan-prefix-scan) and [GPU kernel case studies](../ml-gpu/GPU_Kernel_Case_Studies.md) for parallel scan

### Example Problems

#### Problem 1: Subarray Sum Equals K (LC 560) — Medium

**Problem**: Given an integer array `nums` (values may be negative) and an integer `k`, return the total number of contiguous subarrays whose sum equals `k`.

**Link**: [https://leetcode.com/problems/subarray-sum-equals-k/](https://leetcode.com/problems/subarray-sum-equals-k/)

**Intuition**: The brute force checks all O(n^2) subarrays. With prefix sums, a subarray ending at `i` sums to `k` exactly when some earlier prefix equals `prefix_i - k`. The number of such subarrays is the number of earlier prefixes with that value, so keep a frequency map.

**Python Solution**:

```python
from collections import defaultdict

class Solution:
    def subarraySum(self, nums: list[int], k: int) -> int:
        seen = defaultdict(int)
        seen[0] = 1
        prefix = count = 0
        for x in nums:
            prefix += x
            count += seen[prefix - k]
            seen[prefix] += 1
        return count
```

**C++ Solution**:

```cpp
#include <unordered_map>
#include <vector>
using namespace std;

class Solution {
public:
    int subarraySum(vector<int>& nums, int k) {
        unordered_map<int, int> seen{{0, 1}};
        seen.reserve(nums.size() * 2);
        int prefix = 0, count = 0;   // |sum| <= 2*10^4 * 1000 fits in int
        for (int x : nums) {
            prefix += x;
            auto it = seen.find(prefix - k);
            if (it != seen.end()) count += it->second;
            ++seen[prefix];
        }
        return count;
    }
};
```

**Complexity**: Time O(n) expected (hash map). Space O(n).

**Follow-up**: "What if all numbers are positive?" Then a sliding window gives O(1) space. "Return the longest such subarray?" Store the first index of each prefix instead of a count.

---

#### Problem 2: Contiguous Array (LC 525) — Medium

**Problem**: Given a binary array `nums`, return the maximum length of a contiguous subarray with an equal number of `0`s and `1`s.

**Link**: [https://leetcode.com/problems/contiguous-array/](https://leetcode.com/problems/contiguous-array/)

**Intuition**: Treat `0` as `-1`. Then "equal counts" means "sum is 0", i.e. two equal prefix balances. To maximize length, store the **first** index at which each balance appears. Seed balance `0` at index `-1`.

**Python Solution**:

```python
class Solution:
    def findMaxLength(self, nums: list[int]) -> int:
        first = {0: -1}
        balance = best = 0
        for i, x in enumerate(nums):
            balance += 1 if x == 1 else -1
            if balance in first:
                best = max(best, i - first[balance])
            else:
                first[balance] = i
        return best
```

**C++ Solution**:

```cpp
#include <algorithm>
#include <vector>
using namespace std;

class Solution {
public:
    int findMaxLength(vector<int>& nums) {
        int n = nums.size();
        // balance is in [-n, n]; an array indexed by balance + n beats a hash map
        vector<int> first(2 * n + 1, -2);
        first[n] = -1;                       // balance 0 at index -1
        int balance = 0, best = 0;
        for (int i = 0; i < n; ++i) {
            balance += nums[i] == 1 ? 1 : -1;
            int& f = first[balance + n];
            if (f != -2) best = max(best, i - f);
            else f = i;
        }
        return best;
    }
};
```

**Complexity**: Time O(n). Space O(n).

---

#### Problem 3: Continuous Subarray Sum (LC 523) — Medium

**Problem**: Given `nums` (non-negative) and `k >= 1`, return `true` if there is a subarray of **length at least 2** whose sum is a multiple of `k`.

**Link**: [https://leetcode.com/problems/continuous-subarray-sum/](https://leetcode.com/problems/continuous-subarray-sum/)

**Intuition**: `sum(j+1..i)` is a multiple of `k` exactly when `P[i] mod k == P[j] mod k`. Store the first index of each remainder (seed `0 → -1`). If the same remainder appears again at least 2 positions later, the answer is yes. Keeping the **first** index maximizes the length, so the "length >= 2" test is as easy as possible to pass.

**Python Solution**:

```python
class Solution:
    def checkSubarraySum(self, nums: list[int], k: int) -> bool:
        first = {0: -1}
        rem = 0
        for i, x in enumerate(nums):
            rem = (rem + x) % k
            if rem in first:
                if i - first[rem] >= 2:
                    return True
            else:
                first[rem] = i
        return False
```

**C++ Solution**:

```cpp
#include <unordered_map>
#include <vector>
using namespace std;

class Solution {
public:
    bool checkSubarraySum(vector<int>& nums, int k) {
        unordered_map<int, int> first{{0, -1}};
        int rem = 0;
        for (int i = 0; i < (int)nums.size(); ++i) {
            rem = (rem + nums[i] % k) % k;   // values are non-negative here
            auto it = first.find(rem);
            if (it != first.end()) {
                if (i - it->second >= 2) return true;
            } else {
                first[rem] = i;
            }
        }
        return false;
    }
};
```

**Complexity**: Time O(n). Space O(min(n, k)).

**Pitfall**: `[5, 0, 0]` with `k = 3` → `true` because the subarray `[0, 0]` has sum 0, which is a multiple of every k. If the input could be negative, normalize the remainder in C++ with `((x % k) + k) % k`.

---

#### Problem 4: Range Sum Query 2D - Immutable (LC 304) — Medium

**Problem**: Given a matrix, answer many queries `sumRegion(row1, col1, row2, col2)` (inclusive corners) in O(1) each.

**Link**: [https://leetcode.com/problems/range-sum-query-2d-immutable/](https://leetcode.com/problems/range-sum-query-2d-immutable/)

**Intuition**: Build a padded `(m+1) x (n+1)` prefix table. Each query adds and subtracts four rectangles anchored at the origin (inclusion–exclusion).

**Python Solution**:

```python
class NumMatrix:
    def __init__(self, matrix: list[list[int]]):
        m, n = len(matrix), len(matrix[0]) if matrix else 0
        self.P = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m):
            row_sum = 0
            for j in range(n):
                row_sum += matrix[i][j]
                self.P[i + 1][j + 1] = self.P[i][j + 1] + row_sum

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        P = self.P
        return (P[row2 + 1][col2 + 1] - P[row1][col2 + 1]
                - P[row2 + 1][col1] + P[row1][col1])
```

**C++ Solution**:

```cpp
#include <vector>
using namespace std;

class NumMatrix {
    vector<vector<int>> P;
public:
    NumMatrix(vector<vector<int>>& matrix) {
        int m = matrix.size(), n = m ? matrix[0].size() : 0;
        P.assign(m + 1, vector<int>(n + 1, 0));
        for (int i = 0; i < m; ++i)
            for (int j = 0; j < n; ++j)
                P[i + 1][j + 1] = matrix[i][j] + P[i][j + 1] + P[i + 1][j] - P[i][j];
    }

    int sumRegion(int row1, int col1, int row2, int col2) {
        return P[row2 + 1][col2 + 1] - P[row1][col2 + 1]
             - P[row2 + 1][col1] + P[row1][col1];
    }
};
```

**Complexity**: Build O(mn) time and space. Each query O(1).

---

#### Problem 5: Car Pooling (LC 1094) — Medium

**Problem**: `trips[i] = [numPassengers, from, to]`. The car only drives east and has `capacity` seats. Passengers board at `from` and leave at `to`. Return whether every trip can be served. Locations are in `[0, 1000]`.

**Link**: [https://leetcode.com/problems/car-pooling/](https://leetcode.com/problems/car-pooling/)

**Intuition**: Each trip is a range update `+p` on `[from, to)`. The interval is half-open because passengers have left by `to`. Use a difference array over the small coordinate range, then do one running sum and check it against capacity.

**Python Solution**:

```python
class Solution:
    def carPooling(self, trips: list[list[int]], capacity: int) -> bool:
        diff = [0] * 1001
        for p, start, end in trips:
            diff[start] += p
            diff[end] -= p          # half-open: seat is free again at `end`
        load = 0
        for delta in diff:
            load += delta
            if load > capacity:
                return False
        return True
```

**C++ Solution**:

```cpp
#include <vector>
using namespace std;

class Solution {
public:
    bool carPooling(vector<vector<int>>& trips, int capacity) {
        int diff[1001] = {0};
        for (const auto& t : trips) {
            diff[t[1]] += t[0];
            diff[t[2]] -= t[0];
        }
        int load = 0;
        for (int d : diff) {
            load += d;
            if (load > capacity) return false;
        }
        return true;
    }
};
```

**Complexity**: Time O(n + L) with `L = 1001`. Space O(L). If coordinates were up to `10^9`, sort the `2n` events instead (line sweep, O(n log n)) or use an ordered map.

---

#### Problem 6: Corporate Flight Bookings (LC 1109) — Medium

**Problem**: There are `n` flights labelled `1..n`. `bookings[i] = [first, last, seats]` reserves `seats` on every flight from `first` to `last` inclusive. Return the total number of seats reserved for each flight.

**Link**: [https://leetcode.com/problems/corporate-flight-bookings/](https://leetcode.com/problems/corporate-flight-bookings/)

**Intuition**: This is the textbook difference array. Convert to 0-indexed `[first-1, last-1]`, so the "end + 1" index is `last`.

**Python Solution**:

```python
class Solution:
    def corpFlightBookings(self, bookings: list[list[int]], n: int) -> list[int]:
        diff = [0] * (n + 1)
        for first, last, seats in bookings:
            diff[first - 1] += seats
            diff[last] -= seats
        answer, running = [], 0
        for i in range(n):
            running += diff[i]
            answer.append(running)
        return answer
```

**C++ Solution**:

```cpp
#include <vector>
using namespace std;

class Solution {
public:
    vector<int> corpFlightBookings(vector<vector<int>>& bookings, int n) {
        vector<int> diff(n + 1, 0);
        for (const auto& b : bookings) {
            diff[b[0] - 1] += b[2];
            diff[b[1]] -= b[2];
        }
        vector<int> answer(n);
        int running = 0;
        for (int i = 0; i < n; ++i) answer[i] = (running += diff[i]);
        return answer;
    }
};
```

**Complexity**: Time O(n + b) instead of the naive O(n · b). Space O(n).

### Interview Q&A

**Q1.** Why does a sliding window fail for Subarray Sum Equals K, and what replaces it?

A sliding window relies on monotonicity: expanding the right edge must not decrease the sum and shrinking the left edge must not increase it. That only holds when every value is non-negative. With negative values, a window that is too large can still become valid after adding more elements, so you can't decide to shrink safely. The prefix + hash map method avoids that decision. Every subarray ending at `i` matches exactly one earlier prefix value, `prefix_i - k`, and a single lookup counts all of them. The cost is O(n) extra memory instead of O(1).

**Q2.** When do you seed the map with `{0: 1}` and when with `{0: -1}`?

Both seeds represent the empty prefix before index 0. When you count subarrays, the map stores how many times each prefix occurred, so the empty prefix counts once: `{0: 1}`. When you look for the longest subarray, the map stores the first index where each prefix appears. The empty prefix is "at index -1", so a full prefix `nums[0..i]` has length `i - (-1) = i + 1`.

**Q3.** The array now gets point updates between range-sum queries. What changes?

A plain prefix array costs O(n) per update because every later prefix shifts. Use a **Fenwick tree** (BIT): O(log n) per point update and per prefix query, n + 1 integers, about 10 lines of code. Use a **segment tree** if you also need range updates with lazy propagation or non-invertible operations such as min and max. A Fenwick tree needs an invertible operation to answer range queries as `prefix(r) - prefix(l-1)`. If updates are rare and queries are frequent, rebuilding the prefix array lazily (mark it dirty, rebuild on the next query) is a valid engineering answer. See [Fenwick Trees](DSA_Fundamentals.md#12-fenwick-trees-binary-indexed-trees).

**Q4.** How is prefix sum computed in parallel, for example on a GPU?

The sequential loop has an O(n) dependency chain. Parallel **scan** algorithms break it. Hillis–Steele does O(n log n) work in O(log n) steps. Blelloch's work-efficient scan uses an up-sweep (reduce) and a down-sweep, doing O(n) work in O(log n) depth. On GPUs the standard structure has three levels: scan within a wavefront or warp (using cross-lane shuffle/DPP operations), scan block-level partial sums in shared memory (LDS on AMD), then propagate block totals with a second pass or a decoupled look-back. Stream compaction, radix sort, and histogram-based allocators all use scan as a building block. See [GPU kernel case studies](../ml-gpu/GPU_Kernel_Case_Studies.md).

**Q5.** Derive the 2D query formula and give its failure modes.

`P[r][c]` is the sum of the rectangle from `(0,0)` to `(r-1,c-1)`. The target rectangle equals the large rectangle `P[r2+1][c2+1]` minus the strip above it (`P[r1][c2+1]`) and the strip to its left (`P[r2+1][c1]`). The top-left corner `P[r1][c1]` was subtracted twice, so add it back once. Failure modes: (a) forgetting the padding row and column, which forces `if r1 > 0` branches everywhere; (b) overflow, since a 1000 x 1000 matrix of values up to `10^6` sums to `10^12`, which needs 64-bit; (c) mixing up inclusive and exclusive corner conventions.

**Q6.** Car Pooling with locations up to `10^9` and `10^5` trips?

A dense difference array would need `10^9` slots. Convert each trip into two events instead, `(from, +p)` and `(to, -p)`, and sort them. At equal coordinates, process `-p` before `+p` because the intervals are half-open. Then sweep with a running sum. That is O(n log n) time and O(n) space. In C++ the alternative is a `std::map<int,int>` difference map. See [Line Sweep](#25-line-sweep--advanced-intervals).

---

## 22. Hashing & Array Classics

### Overview

Many of the most frequently asked Easy and Medium problems come down to one of two ideas:

1. **Hashing / counting.** Replace an inner O(n) search with an O(1) expected hash lookup, turning O(n^2) into O(n). The core question is **what is the key?** It might be the value, its complement (`target - x`), a canonical form (sorted string, count signature), or a prefix value (Pattern 21).
2. **In-place array invariants.** Solve the problem in O(1) extra space by keeping an invariant over index regions: Dutch national flag partitioning, the reversal trick for rotation, a running best for Kadane, a candidate/counter pair for Boyer–Moore, or the array itself used as a hash table for First Missing Positive.

| Idea | Key / invariant | Turns | Into |
|---|---|---|---|
| Complement lookup | `target - x` seen earlier? | O(n^2) pair scan | O(n) |
| Canonical key grouping | `sorted(s)` or 26-count tuple | O(n^2) pairwise compare | O(n · k) |
| Membership set | "is `x-1` present?" | sort O(n log n) | O(n) |
| Prefix/suffix products | `left[i] * right[i]` | division (breaks on 0) | O(n), no division |
| Boyer–Moore vote | `(candidate, count)` | hash map O(n) space | O(1) space |
| Kadane | best sum ending here | O(n^2) all subarrays | O(n) |
| Dutch flag | `[0,lo)=0, [lo,mid)=1, (hi,n)=2` | sort / counting | one pass, O(1) |
| Triple reversal | `rev(all), rev(:k), rev(k:)` | O(n) extra array | O(1) space |
| Array as hash table | value `v` lives at index `v-1` | set O(n) space | O(1) space |

### When to Use

- "Find a pair / two indices with sum, difference, or XOR equal to X" on an **unsorted** array → complement map
- "Group items that are equivalent under some transformation" (anagrams, shifted strings, isomorphic) → canonical key
- "Is there an O(n) solution?" for a problem that seems to need sorting → hash set for membership
- "Without using division", "O(1) extra space", "in-place" → prefix/suffix passes, reversal, partitioning
- "Element appearing more than n/2 (n/3) times" → Boyer–Moore
- "Maximum sum contiguous subarray" → Kadane
- "Next lexicographic arrangement" → Next Permutation algorithm
- Values bounded by `n` and O(1) space required → treat indices as buckets (see [Cyclic Sort](#5-cyclic-sort))

### Template Code

**Counting and complement lookup**

```python
# Python — hashing templates
from collections import Counter, defaultdict

def first_pair_with_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    index_of = {}                         # value -> index of an earlier occurrence
    for i, x in enumerate(nums):
        if target - x in index_of:        # check BEFORE inserting x
            return index_of[target - x], i
        index_of[x] = i
    return None

def group_by_key(items: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    for s in items:
        groups["".join(sorted(s))].append(s)   # canonical key
    return list(groups.values())

freq = Counter("mississippi")             # Counter({'i': 4, 's': 4, 'p': 2, 'm': 1})
assert freq.most_common(1)[0][1] == 4
assert first_pair_with_sum([3, 2, 4], 6) == (1, 2)
```

```cpp
// C++ — hashing templates (including a hash for pair keys)
#include <cstdint>
#include <functional>
#include <optional>
#include <unordered_map>
#include <utility>
#include <vector>
using namespace std;

optional<pair<int, int>> firstPairWithSum(const vector<int>& nums, int target) {
    unordered_map<int, int> indexOf;
    indexOf.reserve(nums.size() * 2);     // avoid rehashing; matters in tight loops
    for (int i = 0; i < (int)nums.size(); ++i) {
        auto it = indexOf.find(target - nums[i]);
        if (it != indexOf.end()) return pair{it->second, i};
        indexOf[nums[i]] = i;
    }
    return nullopt;
}

// std::hash has no specialization for pair; supply one for grid cells etc.
struct PairHash {
    size_t operator()(const pair<int, int>& p) const noexcept {
        uint64_t key = (uint64_t(uint32_t(p.first)) << 32) | uint32_t(p.second);
        return hash<uint64_t>{}(key);
    }
};
unordered_map<pair<int, int>, int, PairHash> cellCount;
```

### Variations

| Variation | Technique | Example Problems |
|---|---|---|
| **Complement lookup** | map value → index | Two Sum (LC 1), Two Sum II sorted → two pointers (LC 167), 4Sum II (LC 454) |
| **Canonical key** | sorted string / count tuple | Group Anagrams (LC 49), Group Shifted Strings (LC 249), Valid Anagram (LC 242) |
| **Membership set** | start-of-run detection | Longest Consecutive Sequence (LC 128), Contains Duplicate (LC 217) |
| **Frequency + bucket** | count → bucket by frequency | Top K Frequent Elements (LC 347), Sort Characters By Frequency (LC 451) |
| **Prefix / suffix pass** | left and right products | Product of Array Except Self (LC 238), Trapping Rain Water (LC 42) |
| **Voting** | candidate + counter | Majority Element (LC 169), Majority Element II (LC 229) |
| **Kadane** | best ending here | Maximum Subarray (LC 53), Maximum Product Subarray (LC 152), Maximum Sum Circular Subarray (LC 918) |
| **Permutation step** | pivot, successor swap, reverse suffix | Next Permutation (LC 31), Permutation Sequence (LC 60) |
| **3-way partition** | lo / mid / hi pointers | Sort Colors (LC 75), Wiggle Sort II (LC 324) |
| **Reversal tricks** | reverse pieces | Rotate Array (LC 189), Reverse Words in a String (LC 151) |
| **Index as hash** | sign marking / cyclic placement | First Missing Positive (LC 41), Find All Duplicates (LC 442) |

### Common Mistakes

1. **Two Sum: inserting before checking.** With `target = 6` and `x = 3`, inserting first lets 3 pair with itself.
2. **Hash map worst cases.** `unordered_map` is O(1) **expected**. Adversarial keys can collide and make it O(n) per operation, which is a known way to fail competitive-programming tests. Call `reserve()`, and use a randomized hash if inputs are hostile. Python's `str` hashing is randomized per process (`PYTHONHASHSEED`), but small `int`s hash to themselves.
3. **Longest Consecutive: starting a scan from every element.** That is O(n^2) on a long run. Only start counting when `x - 1` is **not** in the set.
4. **Product Except Self: dividing by the total product.** This fails with zeros, and the problem forbids division anyway.
5. **Kadane with all-negative arrays.** Initializing `best = 0` returns 0 for `[-3, -1]`. Initialize with `nums[0]`.
6. **Sort Colors: advancing `mid` after swapping with `hi`.** The element swapped in from `hi` has not been examined yet.
7. **Rotate Array: forgetting `k %= n`.** With `k > n`, the slices are wrong or the indices go out of range.
8. **Boyer–Moore without verification.** The vote only guarantees the right answer **if** a majority exists. If existence is not promised, do a second counting pass.

### Related Patterns

- **Prefix Sum** ([Pattern 21](#21-prefix-sum--difference-array)) — hashing of prefix values
- **Two Pointers** ([Pattern 1](#1-two-pointers)) — the O(1)-space alternative once data is sorted
- **Cyclic Sort** ([Pattern 5](#5-cyclic-sort)) — First Missing Positive via index placement (Problem 5.5)
- **Top K Elements** ([Pattern 12](#12-top-k-elements)) — counting followed by heap or bucket selection
- **See also:** [Hash Tables](DSA_Fundamentals.md#5-hash-tables) for load factor, open addressing vs chaining, and rehash cost

### Example Problems

#### Problem 1: Two Sum (LC 1) — Easy

**Problem**: Return the indices of the two numbers in `nums` that add up to `target`. Exactly one solution exists, and you may not use the same element twice.

**Link**: [https://leetcode.com/problems/two-sum/](https://leetcode.com/problems/two-sum/)

**Intuition**: For each `x`, the partner must be `target - x`. A map from value to index answers "have I seen the partner?" in O(1). Checking before inserting prevents pairing an element with itself, and duplicates such as `[3, 3]` still work because the earlier 3 is already in the map.

**Python Solution**:

```python
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        index_of = {}
        for i, x in enumerate(nums):
            j = index_of.get(target - x)
            if j is not None:
                return [j, i]
            index_of[x] = i
        return []
```

**C++ Solution**:

```cpp
#include <unordered_map>
#include <vector>
using namespace std;

class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> indexOf;
        for (int i = 0; i < (int)nums.size(); ++i) {
            auto it = indexOf.find(target - nums[i]);
            if (it != indexOf.end()) return {it->second, i};
            indexOf[nums[i]] = i;
        }
        return {};
    }
};
```

**Complexity**: Time O(n) expected. Space O(n).

**Follow-ups**: If the array is sorted, use two pointers (O(1) space, LC 167). If you need all pairs, map value → count. If the input is a stream with many queries, keep a count map so that `add` is O(1) and `find` is O(distinct) (LC 170). The alternative keeps a set of all pair sums, giving O(1) `find` but O(n) per `add`.

---

#### Problem 2: Group Anagrams (LC 49) — Medium

**Problem**: Group the strings in `strs` that are anagrams of each other.

**Link**: [https://leetcode.com/problems/group-anagrams/](https://leetcode.com/problems/group-anagrams/)

**Intuition**: Anagrams share a canonical form. A sorted string costs O(k log k) per word. A 26-letter count signature costs O(k) per word and works when the alphabet is fixed.

**Python Solution**:

```python
from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        groups = defaultdict(list)
        for s in strs:
            counts = [0] * 26
            for ch in s:
                counts[ord(ch) - ord('a')] += 1
            groups[tuple(counts)].append(s)   # lists are unhashable; tuples are
        return list(groups.values())
```

**C++ Solution**:

```cpp
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;

class Solution {
public:
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        unordered_map<string, vector<string>> groups;
        for (const string& s : strs) {
            string key(26, '\0');            // count signature as a 26-char string
            for (char c : s) ++key[c - 'a']; // fine while counts < 128 (len <= 100 here)
            groups[key].push_back(s);
        }
        vector<vector<string>> out;
        out.reserve(groups.size());
        for (auto& [_, g] : groups) out.push_back(std::move(g));
        return out;
    }
};
```

**Complexity**: Time O(n · k), where k is the maximum string length. Space O(n · k).

---

#### Problem 3: Longest Consecutive Sequence (LC 128) — Medium

**Problem**: Given an unsorted array, return the length of the longest run of consecutive integers (for example, `[100, 4, 200, 1, 3, 2]` → 4 for `1,2,3,4`). The solution must run in O(n).

**Link**: [https://leetcode.com/problems/longest-consecutive-sequence/](https://leetcode.com/problems/longest-consecutive-sequence/)

**Intuition**: Put everything in a set. A number `x` starts a run only if `x - 1` is absent. Only from such starts, walk `x+1, x+2, ...`. Each element is visited by at most one walk, so the total work is O(n). Sorting would be O(n log n).

**Python Solution**:

```python
class Solution:
    def longestConsecutive(self, nums: list[int]) -> int:
        values = set(nums)
        best = 0
        for x in values:                     # iterate the set: duplicates skipped
            if x - 1 not in values:
                y = x
                while y + 1 in values:
                    y += 1
                best = max(best, y - x + 1)
        return best
```

**C++ Solution**:

```cpp
#include <algorithm>
#include <climits>
#include <unordered_set>
#include <vector>
using namespace std;

class Solution {
public:
    int longestConsecutive(vector<int>& nums) {
        unordered_set<int> values(nums.begin(), nums.end());
        int best = 0;
        for (int x : values) {
            // Guards avoid signed overflow (UB) of x - 1 at INT_MIN and y + 1 at INT_MAX.
            // LC 128 bounds |nums[i]| <= 1e9, so they never fire there, but keep them.
            if (x != INT_MIN && values.count(x - 1)) continue;   // not a run start
            int y = x;
            while (y != INT_MAX && values.count(y + 1)) ++y;
            best = max(best, y - x + 1);   // run length <= n, so no overflow
        }
        return best;
    }
};
```

**Complexity**: Time O(n) expected. Space O(n).

**Pitfall**: Iterating over the original array instead of the set is still O(n) for distinct values. With many duplicates of a run start, though, it repeats the same walk, e.g. `[0]*n + list(range(n))` becomes O(n^2): 0 is a run start because -1 is absent, so each of the n duplicate 0s repeats the n-step walk. (`[1]*n + list(range(n))` would not work as an attack: 0 is present, so 1 is never a run start.) Iterate the set.

---

#### Problem 4: Product of Array Except Self (LC 238) — Medium

**Problem**: Return `answer[i]` = the product of all elements except `nums[i]`, in O(n) and without division.

**Link**: [https://leetcode.com/problems/product-of-array-except-self/](https://leetcode.com/problems/product-of-array-except-self/)

**Intuition**: `answer[i] = (product of everything left of i) × (product of everything right of i)`. The first pass writes left products into `answer`. The second pass walks from the right with a running suffix product. The output array does not count as extra space, so extra space is O(1).

**Python Solution**:

```python
class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        n = len(nums)
        answer = [1] * n
        for i in range(1, n):
            answer[i] = answer[i - 1] * nums[i - 1]   # prefix product
        suffix = 1
        for i in range(n - 1, -1, -1):
            answer[i] *= suffix
            suffix *= nums[i]
        return answer
```

**C++ Solution**:

```cpp
#include <vector>
using namespace std;

class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        int n = nums.size();
        vector<int> answer(n, 1);
        for (int i = 1; i < n; ++i) answer[i] = answer[i - 1] * nums[i - 1];
        int suffix = 1;
        for (int i = n - 1; i >= 0; --i) {
            answer[i] *= suffix;
            suffix *= nums[i];
        }
        return answer;
    }
};
```

**Complexity**: Time O(n). Space O(1) extra.

**Why not divide?** With one zero, every other position should be 0 and the zero's position should be the product of the rest. With two zeros, everything is 0. Division breaks in both cases, and integer division can also overflow. The two-pass version handles all of these without special cases.

---

#### Problem 5: Majority Element (LC 169) — Easy (Boyer–Moore Voting)

**Problem**: Return the element that appears more than `⌊n/2⌋` times. It is guaranteed to exist. Follow-up: O(1) space.

**Link**: [https://leetcode.com/problems/majority-element/](https://leetcode.com/problems/majority-element/)

**Intuition**: Pair each majority element with a different element and cancel both. Because the majority has more than n/2 copies, it cannot be fully cancelled. The algorithm keeps a `candidate` and a `count`: matching elements increment the count, different ones decrement it, and when the count reaches 0 the next element becomes the candidate.

**Python Solution**:

```python
class Solution:
    def majorityElement(self, nums: list[int]) -> int:
        candidate, count = None, 0
        for x in nums:
            if count == 0:
                candidate = x
            count += 1 if x == candidate else -1
        return candidate   # if existence is NOT guaranteed: verify nums.count(candidate) > len(nums)//2
```

**C++ Solution**:

```cpp
#include <vector>
using namespace std;

class Solution {
public:
    int majorityElement(vector<int>& nums) {
        int candidate = 0, count = 0;
        for (int x : nums) {
            if (count == 0) candidate = x;
            count += (x == candidate) ? 1 : -1;
        }
        return candidate;
    }
};
```

**Complexity**: Time O(n). Space O(1).

**Generalization (LC 229, > n/3)**: At most `k - 1` elements can appear more than `n/k` times, so keep `k - 1` candidate/count pairs. When a new element matches none of them and all counts are non-zero, decrement every count. A **verification pass is mandatory** because the candidates are only possibilities. This is the same idea as the Misra–Gries heavy-hitters sketch used in streaming analytics.

---

#### Problem 6: Maximum Subarray (LC 53) — Medium (Kadane)

**Problem**: Find the contiguous non-empty subarray with the largest sum.

**Link**: [https://leetcode.com/problems/maximum-subarray/](https://leetcode.com/problems/maximum-subarray/)

**Intuition**: DP state `best_ending_here[i] = max(nums[i], best_ending_here[i-1] + nums[i])`. A negative running sum can only hurt any subarray that extends it, so drop it and restart. The answer is the maximum over all `i`. Only the previous state is needed, which gives O(1) space.

Worked example on `[-2, 1, -3, 4, -1, 2, 1, -5, 4]`:

| x | -2 | 1 | -3 | 4 | -1 | 2 | 1 | -5 | 4 |
|---|---|---|---|---|---|---|---|---|---|
| ending here | -2 | 1 | -2 | 4 | 3 | 5 | **6** | 1 | 5 |
| best | -2 | 1 | 1 | 4 | 4 | 5 | **6** | 6 | 6 |

**Python Solution**:

```python
class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        cur = best = nums[0]                 # NOT 0: handles all-negative input
        for x in nums[1:]:
            cur = max(x, cur + x)
            best = max(best, cur)
        return best
```

**C++ Solution**:

```cpp
#include <algorithm>
#include <vector>
using namespace std;

class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        int cur = nums[0], best = nums[0];
        for (size_t i = 1; i < nums.size(); ++i) {
            cur = max(nums[i], cur + nums[i]);
            best = max(best, cur);
        }
        return best;
    }
};
```

**Complexity**: Time O(n). Space O(1).

**Follow-ups**: To return the indices, record `start` whenever you restart and save `(start, i)` whenever `best` improves. For a circular array (LC 918), the answer is `max(maxSubarray, total - minSubarray)`, unless every element is negative, in which case it is `maxSubarray`. For a maximum *product* (LC 152), track both the max and the min ending here, because a negative factor swaps them. A divide-and-conquer O(n log n) version exists, and the same idea gives an O(log n) segment-tree query.

---

#### Problem 7: Next Permutation (LC 31) — Medium

**Problem**: Rearrange `nums` in place into the next lexicographically greater permutation. If none exists, rearrange it into ascending order.

**Link**: [https://leetcode.com/problems/next-permutation/](https://leetcode.com/problems/next-permutation/)

**Intuition**:
1. Scan from the right for the first `i` with `nums[i] < nums[i+1]` (the **pivot**). Everything to its right is non-increasing, which means that suffix is already at its largest arrangement.
2. If there is no pivot, the whole array is the last permutation. Reverse it and stop.
3. Otherwise, find the rightmost `j > i` with `nums[j] > nums[i]` (the smallest element in the suffix that is larger than the pivot) and swap.
4. Reverse the suffix after `i`, turning it from non-increasing into non-decreasing, which is its smallest arrangement.

Example: `[1, 3, 5, 4, 2]` → pivot `3` (index 1) → swap with `4` → `[1, 4, 5, 3, 2]` → reverse the suffix → `[1, 4, 2, 3, 5]`.

**Python Solution**:

```python
class Solution:
    def nextPermutation(self, nums: list[int]) -> None:
        n = len(nums)
        i = n - 2
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1
        if i >= 0:
            j = n - 1
            while nums[j] <= nums[i]:
                j -= 1
            nums[i], nums[j] = nums[j], nums[i]
        nums[i + 1:] = reversed(nums[i + 1:])
```

**C++ Solution**:

```cpp
#include <algorithm>
#include <vector>
using namespace std;

class Solution {
public:
    void nextPermutation(vector<int>& nums) {
        int n = nums.size(), i = n - 2;
        while (i >= 0 && nums[i] >= nums[i + 1]) --i;
        if (i >= 0) {
            int j = n - 1;
            while (nums[j] <= nums[i]) --j;
            swap(nums[i], nums[j]);
        }
        reverse(nums.begin() + i + 1, nums.end());
        // Equivalent library call: std::next_permutation(nums.begin(), nums.end());
    }
};
```

**Complexity**: Time O(n). Space O(1).

---

#### Problem 8: Sort Colors (LC 75) — Medium (Dutch National Flag)

**Problem**: Sort an array of 0s, 1s, and 2s in place in one pass.

**Link**: [https://leetcode.com/problems/sort-colors/](https://leetcode.com/problems/sort-colors/)

**Intuition**: Maintain this invariant:

```text
[0, lo)      all 0
[lo, mid)    all 1
[mid, hi]    unexamined
(hi, n-1]    all 2
```

If `nums[mid]` is 0, swap it to `lo` and advance both pointers. The element swapped back is known to be 1 because it came from `[lo, mid)`. If it is 1, advance `mid`. If it is 2, swap with `hi` and decrement `hi` **without** advancing `mid`, because the incoming element has not been examined.

**Python Solution**:

```python
class Solution:
    def sortColors(self, nums: list[int]) -> None:
        lo, mid, hi = 0, 0, len(nums) - 1
        while mid <= hi:
            if nums[mid] == 0:
                nums[lo], nums[mid] = nums[mid], nums[lo]
                lo += 1
                mid += 1
            elif nums[mid] == 1:
                mid += 1
            else:
                nums[mid], nums[hi] = nums[hi], nums[mid]
                hi -= 1
```

**C++ Solution**:

```cpp
#include <utility>
#include <vector>
using namespace std;

class Solution {
public:
    void sortColors(vector<int>& nums) {
        int lo = 0, mid = 0, hi = (int)nums.size() - 1;
        while (mid <= hi) {
            if (nums[mid] == 0)      swap(nums[lo++], nums[mid++]);
            else if (nums[mid] == 1) ++mid;
            else                     swap(nums[mid], nums[hi--]);
        }
    }
};
```

**Complexity**: Time O(n), single pass. Space O(1).

**Why it matters beyond the puzzle**: 3-way partitioning is how quicksort and quickselect handle many duplicate keys. Without it, an array of identical elements degrades to O(n^2).

---

#### Problem 9: Rotate Array (LC 189) — Medium

**Problem**: Rotate `nums` to the right by `k` steps, in place.

**Link**: [https://leetcode.com/problems/rotate-array/](https://leetcode.com/problems/rotate-array/)

**Intuition**: Right rotation by k moves the last k elements to the front. Reverse the whole array (the last k are now first but backwards), then reverse the first k and the remaining `n-k` separately. Each element is moved a constant number of times.

`[1,2,3,4,5,6,7], k=3` → reverse all `[7,6,5,4,3,2,1]` → reverse first 3 `[5,6,7,4,3,2,1]` → reverse rest `[5,6,7,1,2,3,4]`.

**Python Solution**:

```python
class Solution:
    def rotate(self, nums: list[int], k: int) -> None:
        n = len(nums)
        k %= n

        def reverse(lo: int, hi: int) -> None:
            while lo < hi:
                nums[lo], nums[hi] = nums[hi], nums[lo]
                lo += 1
                hi -= 1

        reverse(0, n - 1)
        reverse(0, k - 1)
        reverse(k, n - 1)
```

**C++ Solution**:

```cpp
#include <algorithm>
#include <vector>
using namespace std;

class Solution {
public:
    void rotate(vector<int>& nums, int k) {
        int n = nums.size();
        k %= n;
        reverse(nums.begin(), nums.end());
        reverse(nums.begin(), nums.begin() + k);
        reverse(nums.begin() + k, nums.end());
        // Library equivalent: std::rotate(nums.begin(), nums.end() - k, nums.end());
    }
};
```

**Complexity**: Time O(n). Space O(1). Other approaches: an extra array (O(n) space), or cyclic replacements following `gcd(n, k)` cycles (O(1) space but easy to get wrong).

---

#### Problem 10: First Missing Positive (LC 41) — Hard (sign-marking variant)

**Problem**: Return the smallest missing positive integer in O(n) time and O(1) extra space.

**Link**: [https://leetcode.com/problems/first-missing-positive/](https://leetcode.com/problems/first-missing-positive/)

**Intuition**: The answer is always in `[1, n+1]`, so the array itself can serve as a presence bitmap over `1..n`. [Problem 5.5](#55-hard--first-missing-positive-leetcode-41) solves this with cyclic placement. The sign-marking variant has three steps: (1) replace every value outside `[1, n]` with `n + 1`, a harmless placeholder; (2) for each `|v|` in `[1, n]`, make `nums[|v| - 1]` negative; (3) the first index that is still positive gives the answer `i + 1`, and if there is none, the answer is `n + 1`.

**Python Solution**:

```python
class Solution:
    def firstMissingPositive(self, nums: list[int]) -> int:
        n = len(nums)
        for i in range(n):
            if not 1 <= nums[i] <= n:
                nums[i] = n + 1
        for i in range(n):
            v = abs(nums[i])
            if v <= n:
                nums[v - 1] = -abs(nums[v - 1])   # abs(): idempotent for duplicates
        for i in range(n):
            if nums[i] > 0:
                return i + 1
        return n + 1
```

**C++ Solution**:

```cpp
#include <cstdlib>
#include <vector>
using namespace std;

class Solution {
public:
    int firstMissingPositive(vector<int>& nums) {
        int n = nums.size();
        for (int& x : nums)
            if (x <= 0 || x > n) x = n + 1;
        for (int i = 0; i < n; ++i) {
            int v = abs(nums[i]);
            if (v <= n) nums[v - 1] = -abs(nums[v - 1]);
        }
        for (int i = 0; i < n; ++i)
            if (nums[i] > 0) return i + 1;
        return n + 1;
    }
};
```

**Complexity**: Time O(n), three passes. Space O(1). The input is mutated, so say so in the interview, or restore the signs afterwards.

### Interview Q&A

**Q1.** `unordered_map` is "O(1)". When is it not, and what do you do?

It is O(1) *expected* given a good hash and a bounded load factor. The worst case is O(n) per operation when many keys collide. libstdc++ uses `std::hash<int>` = identity with bucket count = a prime, so an adversary who knows the bucket sequence can force every key into one bucket. Rehashing is O(n), but amortized over insertions it costs O(1). Mitigations: `reserve(n)` up front to skip rehash cascades; a randomized or splitmix64 hash for untrusted input; an open-addressing table (e.g. `absl::flat_hash_map`) for cache-friendliness, since chained `unordered_map` costs a heap allocation and a pointer chase per node; or a sorted vector with binary search when the key set is built once and queried many times.

**Q2.** Prove Boyer–Moore voting returns the majority.

Each time `count` decrements, one occurrence of the current candidate cancels against one different element. View the run as disjoint cancelled pairs plus the surviving count. Every pair contains at most one copy of the majority element `m`, so cancellation removes at most as many copies of `m` as non-`m` elements. There are more than n/2 copies of `m` and fewer than n/2 other elements, so `m` cannot be fully cancelled and must be the surviving candidate. Without the "> n/2" guarantee the survivor can be anything (for example `[1,2,3]` → 3), which is why a verification pass is needed.

**Q3.** How does Kadane relate to DP and to prefix sums?

The DP form: `f(i) = max(nums[i], f(i-1) + nums[i])` is the best sum of a subarray ending exactly at `i`. The prefix-sum form: the best sum ending at `i` is `P[i+1] - min(P[0..i])`, so keep a running minimum prefix. Both are O(n). The prefix form extends to constraints like "length at least L" (keep the minimum of `P[0..i+1-L]`), and the DP form extends to products (track min and max).

**Q4.** In Group Anagrams, what is the tradeoff between a sorted-string key and a count key, and what if the input is Unicode?

A sorted key costs O(k log k) per word but works for any alphabet. A count key costs O(k) per word plus a fixed O(26) to build, and is better for long words over a small alphabet. For Unicode, use a `Counter` frozen into a sorted tuple of `(char, count)` pairs, or just the sorted string. Normalize first (NFC) and decide whether case matters, since "é" can be one code point or two.

**Q5.** Next Permutation: why is the suffix reversed instead of sorted?

After the pivot scan, the suffix is non-increasing. Swapping the pivot with the rightmost element larger than it keeps the suffix non-increasing: the new element at position `j` is the old pivot, which is less than or equal to its left neighbour and greater than or equal to its right neighbour. Reversing a non-increasing sequence makes it non-decreasing, which is its sorted order, in O(n) instead of O(n log n). Choosing the *rightmost* larger element matters when there are duplicates, because it keeps the suffix property intact.

**Q6.** Where do these array tricks show up in systems work?

3-way partitioning appears in `std::sort` implementations (introsort) and quickselect for percentile metrics. Kadane-style running state appears when finding the longest stretch of high utilization in a counter timeline. Misra–Gries / Boyer–Moore generalizations find heavy hitters in streams, such as the hottest kernels or most frequent call sites, using bounded memory. Rotating via reversal is how ring buffers are linearized in place.

---

## 23. Matrix Manipulation

### Overview

Matrix problems that are not graph searches mostly test whether you can **control indices precisely**: walking boundaries, mapping `(r, c)` to a rotated or flattened position, grouping cells by diagonal, and modifying the matrix **in place** without losing information you still need. The recurring tools:

| Tool | Formula / idea | Used by |
|---|---|---|
| **Direction vectors** | `DIRS = [(0,1),(1,0),(0,-1),(-1,0)]` (right, down, left, up) | Spiral, BFS/DFS on grids, Game of Life (8 dirs) |
| **Bounds check** | `0 <= r < m and 0 <= c < n` | every grid problem |
| **Shrinking boundaries** | `top, bottom, left, right` that close in after each side | Spiral Matrix I/II |
| **Rotation = transpose + reflect** | 90° clockwise: `(r, c) → (c, n-1-r)` | Rotate Image |
| **Diagonal keys** | same `r + c` = anti-diagonal; same `r - c` = main diagonal | Diagonal Traverse, Sort Matrix Diagonally, N-Queens |
| **Flattening** | `idx = r * n + c`, `r = idx // n`, `c = idx % n` | Search a 2D Matrix, Union-Find on grids |
| **In-place markers** | first row/column as flags, or spare bits for the next state | Set Matrix Zeroes, Game of Life |
| **Staircase search** | start at a corner where one move increases and the other decreases | Search a 2D Matrix II, Kth Smallest in Sorted Matrix |

### When to Use

- "Return the elements in spiral / zigzag / diagonal order"
- "Rotate / transpose / flip the image **in place**"
- "Modify the matrix in place based on its *original* values" (zeroes, Game of Life) → markers or encoding
- "Rows and columns are sorted" → staircase or binary search
- Neighbour-based updates on a fixed grid (cellular automata, blur, stencil)

### Template Code

**Direction vectors and bounds**

```python
# Python — grid neighbour iteration
DIRS4 = [(0, 1), (1, 0), (0, -1), (-1, 0)]
DIRS8 = [(dr, dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1) if (dr, dc) != (0, 0)]

def neighbours(grid: list[list[int]], r: int, c: int, dirs=DIRS4):
    m, n = len(grid), len(grid[0])
    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        if 0 <= nr < m and 0 <= nc < n:
            yield nr, nc

g = [[1, 2], [3, 4]]
assert sorted(neighbours(g, 0, 0)) == [(0, 1), (1, 0)]
assert len(list(neighbours(g, 0, 0, DIRS8))) == 3
```

```cpp
// C++ — grid neighbour iteration
#include <array>
#include <utility>
#include <vector>
using namespace std;

constexpr array<pair<int, int>, 4> DIRS4{{{0, 1}, {1, 0}, {0, -1}, {-1, 0}}};
constexpr array<pair<int, int>, 8> DIRS8{{{-1, -1}, {-1, 0}, {-1, 1}, {0, -1},
                                          {0, 1},   {1, -1}, {1, 0},  {1, 1}}};

template <class F>
void forEachNeighbour(int m, int n, int r, int c, F&& visit) {
    for (auto [dr, dc] : DIRS4) {
        int nr = r + dr, nc = c + dc;
        if (nr >= 0 && nr < m && nc >= 0 && nc < n) visit(nr, nc);
    }
}
```

**Layer-by-layer boundary walk (spiral skeleton)**

```python
# Python — shrinking-boundary skeleton
def walk_layers(m: int, n: int):
    top, bottom, left, right = 0, m - 1, 0, n - 1
    while top <= bottom and left <= right:
        yield (top, bottom, left, right)      # process the ring at this layer
        top, bottom, left, right = top + 1, bottom - 1, left + 1, right - 1

assert list(walk_layers(3, 4)) == [(0, 2, 0, 3), (1, 1, 1, 2)]
```

### Variations

| Variation | Technique | Example Problems |
|---|---|---|
| **Spiral order** | shrinking boundaries, or direction vector + turn on visited/out of bounds | Spiral Matrix (LC 54), Spiral Matrix II (LC 59) |
| **Rotation / reflection** | transpose + reverse rows (CW) / reverse columns (CCW) | Rotate Image (LC 48), Transpose Matrix (LC 867), Flipping an Image (LC 832) |
| **In-place flags** | first row/col markers | Set Matrix Zeroes (LC 73) |
| **In-place state encoding** | bit 0 = current, bit 1 = next | Game of Life (LC 289) |
| **Sorted matrix search** | flatten + binary search; staircase | Search a 2D Matrix (LC 74), Search a 2D Matrix II (LC 240) |
| **Kth in sorted matrix** | binary search on value + staircase count, or heap | Kth Smallest Element in a Sorted Matrix (LC 378) |
| **Diagonals** | group by `r + c` or `r - c` | Diagonal Traverse (LC 498), Sort the Matrix Diagonally (LC 1329), Toeplitz Matrix (LC 766) |
| **Box index** | `(r // 3) * 3 + c // 3` | Valid Sudoku (LC 36) |
| **Matrix prefix sums** | 2D prefix | Range Sum Query 2D (LC 304) — see [Pattern 21](#21-prefix-sum--difference-array) |

### Common Mistakes

1. **Spiral: double-visiting the middle row or column.** After walking right and down, re-check `top <= bottom` before walking left and `left <= right` before walking up. Non-square inputs like `3 x 1` or `1 x 4` expose this.
2. **Rotate Image: transposing the full matrix.** Loop `j` from `i + 1` only. Swapping every `(i, j)` pair twice gives back the original.
3. **Set Matrix Zeroes: zeroing while scanning.** New zeros then cascade into rows and columns that should stay untouched. Record first, apply second. Also handle row 0 and column 0 **last**, because they hold the markers.
4. **Game of Life: reading updated neighbours.** Every cell must see the *old* generation. Read only bit 0 (`cell & 1`) until the final shift.
5. **`m` vs `n` confusion** in flattening. The divisor is the number of **columns**: `r = idx // n`.
6. **Empty matrix / empty row.** `matrix[0]` throws on `[]`. Guard it when the constraints allow an empty input.

### Related Patterns

- **BFS / DFS** ([Pattern 7](#7-bfs-breadth-first-search), [Pattern 8](#8-dfs-depth-first-search)) — connectivity on grids uses the same direction vectors
- **Modified Binary Search** ([Pattern 11](#11-modified-binary-search)) — Search a 2D Matrix is binary search over a flattened index
- **Prefix Sum** ([Pattern 21](#21-prefix-sum--difference-array)) — 2D range sums
- **See also:** [Global Memory Coalescing](../ml-gpu/Parallel_GPU_Programming.md#201-global-memory-coalescing) — row- vs column-major access and why a tiled transpose goes through shared memory

### Example Problems

#### Problem 1: Spiral Matrix (LC 54) — Medium

**Problem**: Return all elements of an `m x n` matrix in clockwise spiral order.

**Link**: [https://leetcode.com/problems/spiral-matrix/](https://leetcode.com/problems/spiral-matrix/)

**Intuition**: Walk the outer ring in four legs (right along `top`, down along `right`, left along `bottom`, up along `left`), shrinking each boundary after its leg. The two guards stop a single remaining row or column from being walked twice.

**Python Solution**:

```python
class Solution:
    def spiralOrder(self, matrix: list[list[int]]) -> list[int]:
        out = []
        top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
        while top <= bottom and left <= right:
            for c in range(left, right + 1):
                out.append(matrix[top][c])
            top += 1
            for r in range(top, bottom + 1):
                out.append(matrix[r][right])
            right -= 1
            if top <= bottom:
                for c in range(right, left - 1, -1):
                    out.append(matrix[bottom][c])
                bottom -= 1
            if left <= right:
                for r in range(bottom, top - 1, -1):
                    out.append(matrix[r][left])
                left += 1
        return out
```

**C++ Solution**:

```cpp
#include <vector>
using namespace std;

class Solution {
public:
    vector<int> spiralOrder(vector<vector<int>>& matrix) {
        vector<int> out;
        int top = 0, bottom = (int)matrix.size() - 1;
        int left = 0, right = (int)matrix[0].size() - 1;
        out.reserve(matrix.size() * matrix[0].size());
        while (top <= bottom && left <= right) {
            for (int c = left; c <= right; ++c) out.push_back(matrix[top][c]);
            ++top;
            for (int r = top; r <= bottom; ++r) out.push_back(matrix[r][right]);
            --right;
            if (top <= bottom) {
                for (int c = right; c >= left; --c) out.push_back(matrix[bottom][c]);
                --bottom;
            }
            if (left <= right) {
                for (int r = bottom; r >= top; --r) out.push_back(matrix[r][left]);
                ++left;
            }
        }
        return out;
    }
};
```

**Complexity**: Time O(mn). Space O(1) besides the output.

**Alternative**: Keep a direction index `d` into `DIRS4` and turn (`d = (d + 1) % 4`) when the next cell is out of bounds or already visited. This is simpler to get right under pressure but needs O(mn) visited marks unless you overwrite the matrix with a sentinel. Spiral Matrix II (LC 59) is the same walk, writing `1..n²` instead of reading.

---

#### Problem 2: Rotate Image (LC 48) — Medium

**Problem**: Rotate an `n x n` matrix 90° clockwise **in place**.

**Link**: [https://leetcode.com/problems/rotate-image/](https://leetcode.com/problems/rotate-image/)

**Intuition**: Clockwise rotation maps `(r, c) → (c, n-1-r)`. That is a transpose, `(r, c) → (c, r)`, followed by a horizontal flip, `(c, r) → (c, n-1-r)`. Both steps are easy to do in place.

| Rotation | Recipe |
|---|---|
| 90° clockwise | transpose, then reverse each row |
| 90° counter-clockwise | transpose, then reverse each column (or reverse each row first, then transpose) |
| 180° | reverse each row, then reverse the row order |

**Python Solution**:

```python
class Solution:
    def rotate(self, matrix: list[list[int]]) -> None:
        n = len(matrix)
        for i in range(n):
            for j in range(i + 1, n):            # upper triangle only
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        for row in matrix:
            row.reverse()
```

**C++ Solution**:

```cpp
#include <algorithm>
#include <vector>
using namespace std;

class Solution {
public:
    void rotate(vector<vector<int>>& matrix) {
        int n = matrix.size();
        for (int i = 0; i < n; ++i)
            for (int j = i + 1; j < n; ++j)
                swap(matrix[i][j], matrix[j][i]);
        for (auto& row : matrix) reverse(row.begin(), row.end());
    }
};
```

**Complexity**: Time O(n²). Space O(1).

**Alternative**: The 4-way cyclic swap, layer by layer, uses `tmp = top; top = left; left = bottom; bottom = right; right = tmp` for each of the `n/2` layers. It does one pass instead of two, but the index arithmetic is error-prone.

---

#### Problem 3: Set Matrix Zeroes (LC 73) — Medium

**Problem**: If an element is 0, set its entire row and column to 0, in place. Follow-up: O(1) extra space.

**Link**: [https://leetcode.com/problems/set-matrix-zeroes/](https://leetcode.com/problems/set-matrix-zeroes/)

**Intuition**: The O(m + n) solution keeps a boolean per row and per column. For O(1) space, store those booleans **in row 0 and column 0**. Row 0 and column 0 then need their own two flags, captured before they are overwritten.

**Python Solution**:

```python
class Solution:
    def setZeroes(self, matrix: list[list[int]]) -> None:
        m, n = len(matrix), len(matrix[0])
        first_row_zero = any(matrix[0][j] == 0 for j in range(n))
        first_col_zero = any(matrix[i][0] == 0 for i in range(m))

        for i in range(1, m):                    # record markers
            for j in range(1, n):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0
                    matrix[0][j] = 0
        for i in range(1, m):                    # apply markers to the interior
            for j in range(1, n):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0
        if first_row_zero:                       # marker row/col last
            for j in range(n):
                matrix[0][j] = 0
        if first_col_zero:
            for i in range(m):
                matrix[i][0] = 0
```

**C++ Solution**:

```cpp
#include <vector>
using namespace std;

class Solution {
public:
    void setZeroes(vector<vector<int>>& matrix) {
        int m = matrix.size(), n = matrix[0].size();
        bool firstRowZero = false, firstColZero = false;
        for (int j = 0; j < n; ++j) if (matrix[0][j] == 0) firstRowZero = true;
        for (int i = 0; i < m; ++i) if (matrix[i][0] == 0) firstColZero = true;

        for (int i = 1; i < m; ++i)
            for (int j = 1; j < n; ++j)
                if (matrix[i][j] == 0) matrix[i][0] = matrix[0][j] = 0;
        for (int i = 1; i < m; ++i)
            for (int j = 1; j < n; ++j)
                if (matrix[i][0] == 0 || matrix[0][j] == 0) matrix[i][j] = 0;
        if (firstRowZero) for (int j = 0; j < n; ++j) matrix[0][j] = 0;
        if (firstColZero) for (int i = 0; i < m; ++i) matrix[i][0] = 0;
    }
};
```

**Complexity**: Time O(mn). Space O(1).

---

#### Problem 4: Game of Life (LC 289) — Medium

**Problem**: Compute the next generation of Conway's Game of Life on an `m x n` board, in place. A live cell with 2 or 3 live neighbours survives. A dead cell with exactly 3 becomes live. All other cells die or stay dead.

**Link**: [https://leetcode.com/problems/game-of-life/](https://leetcode.com/problems/game-of-life/)

**Intuition**: Every update must read the *old* state. Cells hold only 0 or 1, so bit 1 is free. Store the next state in bit 1, count neighbours using only bit 0 (`cell & 1`), and finish with `cell >>= 1`.

**Python Solution**:

```python
class Solution:
    def gameOfLife(self, board: list[list[int]]) -> None:
        m, n = len(board), len(board[0])
        for r in range(m):
            for c in range(n):
                live = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if (dr or dc) and 0 <= r + dr < m and 0 <= c + dc < n:
                            live += board[r + dr][c + dc] & 1   # old state only
                alive = board[r][c] & 1
                if live == 3 or (alive and live == 2):
                    board[r][c] |= 2                            # next state in bit 1
        for r in range(m):
            for c in range(n):
                board[r][c] >>= 1
```

**C++ Solution**:

```cpp
#include <vector>
using namespace std;

class Solution {
public:
    void gameOfLife(vector<vector<int>>& board) {
        int m = board.size(), n = board[0].size();
        for (int r = 0; r < m; ++r) {
            for (int c = 0; c < n; ++c) {
                int live = 0;
                for (int dr = -1; dr <= 1; ++dr)
                    for (int dc = -1; dc <= 1; ++dc) {
                        if (dr == 0 && dc == 0) continue;
                        int nr = r + dr, nc = c + dc;
                        if (nr >= 0 && nr < m && nc >= 0 && nc < n) live += board[nr][nc] & 1;
                    }
                bool alive = board[r][c] & 1;
                if (live == 3 || (alive && live == 2)) board[r][c] |= 2;
            }
        }
        for (auto& row : board)
            for (int& cell : row) cell >>= 1;
    }
};
```

**Complexity**: Time O(8 · mn). Space O(1).

**Follow-ups**: For an **infinite board**, store only live cells in a hash set. Count neighbours by adding each live cell's 8 neighbours to a `Counter`, then apply the rules to the counted cells. The cost is O(live cells) per generation. For a board that does not fit in memory, process it in row strips, keeping one row of halo on each side: this is the same halo/ghost-cell idea used in GPU stencil kernels and MPI domain decomposition.

---

#### Problem 5: Search a 2D Matrix (LC 74) — Medium

**Problem**: Each row is sorted, and the first element of each row is greater than the last element of the previous row. Determine whether `target` exists, in O(log(mn)).

**Link**: [https://leetcode.com/problems/search-a-2d-matrix/](https://leetcode.com/problems/search-a-2d-matrix/)

**Intuition**: Read in row-major order, the matrix is a single sorted array of length `mn`. Binary search on the flattened index and map back with `divmod(idx, n)`.

**Python Solution**:

```python
class Solution:
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        m, n = len(matrix), len(matrix[0])
        lo, hi = 0, m * n - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            r, c = divmod(mid, n)
            if matrix[r][c] == target:
                return True
            if matrix[r][c] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return False
```

**C++ Solution**:

```cpp
#include <vector>
using namespace std;

class Solution {
public:
    bool searchMatrix(vector<vector<int>>& matrix, int target) {
        int m = matrix.size(), n = matrix[0].size();
        int lo = 0, hi = m * n - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            int v = matrix[mid / n][mid % n];
            if (v == target) return true;
            if (v < target) lo = mid + 1;
            else hi = mid - 1;
        }
        return false;
    }
};
```

**Complexity**: Time O(log(mn)). Space O(1).

---

#### Problem 6: Search a 2D Matrix II (LC 240) — Medium

**Problem**: Rows are sorted left to right and columns are sorted top to bottom, but rows do **not** continue into each other. Determine whether `target` exists.

**Link**: [https://leetcode.com/problems/search-a-2d-matrix-ii/](https://leetcode.com/problems/search-a-2d-matrix-ii/)

**Intuition**: Start at the **top-right** corner. Moving left decreases the value and moving down increases it, so each comparison discards a whole row or a whole column. If `v > target`, everything below in this column is larger, so move left. If `v < target`, everything left in this row is smaller, so move down. The bottom-left corner works symmetrically. The top-left and bottom-right corners do **not**, because both moves go in the same direction.

**Python Solution**:

```python
class Solution:
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        r, c = 0, len(matrix[0]) - 1
        while r < len(matrix) and c >= 0:
            v = matrix[r][c]
            if v == target:
                return True
            if v > target:
                c -= 1            # discard column c
            else:
                r += 1            # discard row r
        return False
```

**C++ Solution**:

```cpp
#include <vector>
using namespace std;

class Solution {
public:
    bool searchMatrix(vector<vector<int>>& matrix, int target) {
        int m = matrix.size(), r = 0, c = (int)matrix[0].size() - 1;
        while (r < m && c >= 0) {
            int v = matrix[r][c];
            if (v == target) return true;
            if (v > target) --c;
            else ++r;
        }
        return false;
    }
};
```

**Complexity**: Time O(m + n). Space O(1). Binary searching each row costs O(m log n), which is better only when `m` is much smaller than `n`.

---

#### Problem 7: Diagonal Traverse (LC 498) — Medium

**Problem**: Return all elements of an `m x n` matrix in zigzag diagonal order: `[[1,2,3],[4,5,6],[7,8,9]] → [1,2,4,7,5,3,6,8,9]`.

**Link**: [https://leetcode.com/problems/diagonal-traverse/](https://leetcode.com/problems/diagonal-traverse/)

**Intuition**: The cells of anti-diagonal `d` satisfy `r + c = d`, for `d = 0 .. m+n-2`. On diagonal `d`, row `r` ranges over `[max(0, d-n+1), min(d, m-1)]`. Even diagonals go **up**, with `r` decreasing, and odd diagonals go **down**, with `r` increasing. Iterating that row range directly avoids the error-prone "bounce off the wall" simulation.

**Python Solution**:

```python
class Solution:
    def findDiagonalOrder(self, mat: list[list[int]]) -> list[int]:
        m, n = len(mat), len(mat[0])
        out = []
        for d in range(m + n - 1):
            r_lo, r_hi = max(0, d - n + 1), min(d, m - 1)
            rows = range(r_hi, r_lo - 1, -1) if d % 2 == 0 else range(r_lo, r_hi + 1)
            for r in rows:
                out.append(mat[r][d - r])
        return out
```

**C++ Solution**:

```cpp
#include <algorithm>
#include <vector>
using namespace std;

class Solution {
public:
    vector<int> findDiagonalOrder(vector<vector<int>>& mat) {
        int m = mat.size(), n = mat[0].size();
        vector<int> out;
        out.reserve(m * n);
        for (int d = 0; d < m + n - 1; ++d) {
            int rLo = max(0, d - n + 1), rHi = min(d, m - 1);
            if (d % 2 == 0)
                for (int r = rHi; r >= rLo; --r) out.push_back(mat[r][d - r]);
            else
                for (int r = rLo; r <= rHi; ++r) out.push_back(mat[r][d - r]);
        }
        return out;
    }
};
```

**Complexity**: Time O(mn). Space O(1) besides the output.

### Interview Q&A

**Q1.** Why does traversal order matter for performance, and how does that relate to GPUs?

C/C++ arrays are **row-major**: `a[r][c]` and `a[r][c+1]` are adjacent in memory. Walking along rows uses every byte of each 64-byte cache line and lets the hardware prefetcher stream. Walking down columns of a large matrix touches a new line on every access, which can be 5–10x slower once the matrix exceeds cache. (Fortran, MATLAB, and the default column-major layout in BLAS/LAPACK APIs reverse this.) On a GPU the analogous rule is **coalescing**: adjacent threads should access adjacent addresses. A naive transpose has to read or write with a stride, so efficient transpose kernels load a tile into shared memory (LDS), synchronize, and write it back transposed, padding the tile (e.g. `TILE x (TILE+1)`) to avoid bank conflicts.

**Q2.** Rotate a non-square `m x n` matrix 90° clockwise. Can it be done in place?

The result is `n x m`, with `out[c][m-1-r] = in[r][c]`, so a separate output array is simplest. True in-place rotation of a non-square matrix requires following permutation cycles in the flattened buffer, the same problem as in-place transpose of a rectangular matrix. It is possible in O(1) extra space, but cycle detection is subtle. Interviewers usually only want you to recognize that the square in-place trick does not carry over.

**Q3.** Why does the staircase search start at the top-right?

From the top-right, the two possible moves change the value in **opposite** directions: left decreases it and down increases it. One comparison therefore tells you which move can still reach the target, and the other row or column is eliminated. Each step removes a row or a column, so there are at most `m + n` steps. From the top-left, both moves increase the value, so a comparison cannot rule either one out.

**Q4.** Kth Smallest Element in a Sorted Matrix (LC 378): sketch two approaches.

(a) Min-heap over the first element of each row, popping k times: O(k log m). (b) Binary search on the **value** range `[matrix[0][0], matrix[-1][-1]]`, counting how many elements are `<= mid` with the staircase walk in O(m + n): O((m + n) log(max - min)). Approach (b) is "binary search on the answer". The predicate "count(≤ mid) ≥ k" is monotone in `mid`, and the smallest value satisfying it is guaranteed to be in the matrix.

**Q5.** How would you parallelize Game of Life?

Each cell's next state depends only on the 3x3 neighbourhood of the old generation, so the update is a **stencil** and is embarrassingly parallel if you double-buffer (read `old`, write `new`, swap pointers). On a GPU, each workgroup loads a tile plus a 1-cell halo into shared memory, then each thread computes one cell. The in-place bit trick also parallelizes safely: the first pass reads only bit 0, and each thread writes only bit 1 of its own cell. It does cost a second full pass for the shift, though, so double buffering is the standard design.

---

## 24. Stack-based Parsing

### Overview

Any input with **nesting** (brackets, parenthesized sub-expressions, `k[...]` repetitions, directory levels) or **deferred decisions** (an operator that cannot be applied until a higher-precedence operator to its right is resolved) is naturally processed with a stack. The stack holds the **saved context of the enclosing level**. On an opening token you push the current context and start fresh. On a closing token you pop and combine.

| Problem shape | What the stack holds | Pop when |
|---|---|---|
| Bracket matching | expected closing bracket | a closing bracket arrives |
| Postfix (RPN) evaluation | operand values | an operator arrives (pop 2, push 1) |
| Infix with `* /` precedence | pending `+/-` terms | never mid-scan; sum at the end |
| Infix with parentheses | `(result_so_far, sign)` of the outer level | `)` arrives |
| Nested repetition `k[...]` | `(outer_string, k)` | `]` arrives |
| Path canonicalization | directory names | `..` arrives |
| Collisions / cancellations | survivors moving right | a left-mover destroys them |

For general expressions, the systematic tool is a **recursive-descent parser** with one function per precedence level. The call stack does the stacking.

```text
expr   := term   (('+' | '-') term)*        lowest precedence, left-assoc
term   := factor (('*' | '/') factor)*
factor := NUMBER | '(' expr ')' | ('+' | '-') factor     unary binds tightest
```

### When to Use

- "Valid / balanced" brackets, tags, or quotes
- "Evaluate the expression" (infix, postfix, prefix) or "implement a calculator"
- Encoded or nested strings: `3[a2[c]]`, nested lists `[1,[2,[3]]]`, mini-JSON
- Unix path normalization, undo/back history
- "Process from left to right; a new item may cancel earlier ones" (asteroids, removing adjacent duplicates, backspace strings)

### Template Code

**Bracket matching**

```python
# Python — bracket matching template
PAIRS = {')': '(', ']': '[', '}': '{'}

def balanced(s: str) -> bool:
    stack = []
    for ch in s:
        if ch in '([{':
            stack.append(ch)
        elif ch in PAIRS:
            if not stack or stack.pop() != PAIRS[ch]:
                return False
    return not stack                      # leftover openers are unbalanced

assert balanced("{[()()]}") and not balanced("(]") and not balanced("((")
```

**Recursive-descent evaluator** (`+ - * / ( )`, unary signs, integer division truncating toward zero)

```python
# Python — recursive-descent expression evaluator
def trunc_div(a: int, b: int) -> int:
    q = abs(a) // abs(b)                  # Python // floors; C/C++/Java truncate
    return q if (a >= 0) == (b > 0) else -q

class ExprParser:
    def __init__(self, text: str):
        self.s = text.replace(" ", "")
        self.i = 0

    def _peek(self) -> str:
        return self.s[self.i] if self.i < len(self.s) else ""

    def parse(self) -> int:
        value = self._expr()
        if self.i != len(self.s):
            raise ValueError(f"unexpected {self._peek()!r} at {self.i}")
        return value

    def _expr(self) -> int:
        value = self._term()
        while self._peek() in ("+", "-"):
            op = self.s[self.i]
            self.i += 1
            rhs = self._term()
            value = value + rhs if op == "+" else value - rhs
        return value

    def _term(self) -> int:
        value = self._factor()
        while self._peek() in ("*", "/"):
            op = self.s[self.i]
            self.i += 1
            rhs = self._factor()
            value = value * rhs if op == "*" else trunc_div(value, rhs)
        return value

    def _factor(self) -> int:
        ch = self._peek()
        if ch in ("+", "-"):
            self.i += 1
            v = self._factor()
            return v if ch == "+" else -v
        if ch == "(":
            self.i += 1
            v = self._expr()
            if self._peek() != ")":
                raise ValueError(f"expected ')' at {self.i}")
            self.i += 1
            return v
        start = self.i
        while self._peek().isdigit():
            self.i += 1
        if start == self.i:
            raise ValueError(f"expected number at {self.i}")
        return int(self.s[start:self.i])

assert ExprParser("2*(3+4) - -6/4").parse() == 15     # 14 - (-1): -6/4 truncates to -1
assert ExprParser("1 - 2 - 3").parse() == -4           # left-associative
```

```cpp
// C++ — recursive-descent expression evaluator
#include <cctype>
#include <stdexcept>
#include <string>
#include <string_view>
using namespace std;

class ExprParser {
    string_view s;
    size_t i = 0;

    void skipSpaces() { while (i < s.size() && s[i] == ' ') ++i; }
    char peek() { skipSpaces(); return i < s.size() ? s[i] : '\0'; }

    long long expr() {
        long long v = term();
        for (char op = peek(); op == '+' || op == '-'; op = peek()) {
            ++i;
            long long rhs = term();
            v = (op == '+') ? v + rhs : v - rhs;
        }
        return v;
    }
    long long term() {
        long long v = factor();
        for (char op = peek(); op == '*' || op == '/'; op = peek()) {
            ++i;
            long long rhs = factor();
            if (op == '/' && rhs == 0) throw runtime_error("division by zero");
            v = (op == '*') ? v * rhs : v / rhs;     // C++ '/' truncates toward zero
        }
        return v;
    }
    long long factor() {
        char c = peek();
        if (c == '+' || c == '-') { ++i; long long v = factor(); return c == '-' ? -v : v; }
        if (c == '(') {
            ++i;
            long long v = expr();
            if (peek() != ')') throw runtime_error("expected ')'");
            ++i;
            return v;
        }
        if (!isdigit(static_cast<unsigned char>(c))) throw runtime_error("expected number");
        long long v = 0;
        while (i < s.size() && isdigit(static_cast<unsigned char>(s[i]))) v = v * 10 + (s[i++] - '0');
        return v;
    }

public:
    explicit ExprParser(string_view text) : s(text) {}
    long long parse() {
        long long v = expr();
        if (peek() != '\0') throw runtime_error("trailing input at " + to_string(i));
        return v;
    }
};
```

### Variations

| Variation | Technique | Example Problems |
|---|---|---|
| **Bracket validation** | stack of openers; counter if only one type | Valid Parentheses (LC 20), Minimum Remove to Make Valid Parentheses (LC 1249), Valid Parenthesis String (LC 678, greedy lo/hi) |
| **Longest valid substring** | stack of indices with a sentinel `-1` | Longest Valid Parentheses (LC 32) |
| **Postfix evaluation** | operand stack | Evaluate Reverse Polish Notation (LC 150) |
| **Infix, no parens** | stack of signed terms (or O(1) `last` term) | Basic Calculator II (LC 227) |
| **Infix, `+ -` and parens** | push `(result, sign)` on `(` | Basic Calculator (LC 224) |
| **Full infix** | recursive descent, or shunting-yard to RPN | Basic Calculator III (LC 772) |
| **Nested decoding** | push `(outer, k)` on `[` | Decode String (LC 394), Number of Atoms (LC 726) |
| **Nested structures** | recursive parser / stack of containers | Mini Parser (LC 385), Flatten Nested List Iterator (LC 341) |
| **Path normalization** | stack of names | Simplify Path (LC 71) |
| **Cancellation** | stack of survivors | Asteroid Collision (LC 735), Remove All Adjacent Duplicates in String II (LC 1209), Backspace String Compare (LC 844) |

### Common Mistakes

1. **Division semantics.** Python `//` **floors** (`-7 // 2 == -4`), while C/C++/Java `/` **truncates** (`-7 / 2 == -3`). LeetCode calculators specify truncation, so in Python use `int(a / b)` (fine for 32-bit operands) or an exact helper like `trunc_div`.
2. **Operand order in RPN.** Pop `b` first, then `a`, and compute `a - b` and `a / b`, not `b - a`.
3. **Multi-digit numbers.** Accumulate `num = num * 10 + digit`. Do not treat each digit as a token.
4. **Flushing the last number.** In single-pass calculators the last operand is applied either at the final character or after the loop. Forgetting it gives `"3+2*2" → 3`.
5. **Unary minus.** `-(2+3)` and `1-(-2)` break parsers that assume a binary operator always has a left operand. Handle it in `factor` or seed `result = 0`.
6. **Simplify Path: treating `...` as special.** Only `.` and `..` are special. `...` is a valid directory name.
7. **Recursion depth.** Python's default recursion limit is about 1000, so a recursive parser on a deeply nested input such as `((((...))))` 10^4 levels deep raises `RecursionError`. Use an explicit stack, or raise the limit with care.
8. **Integer overflow in C++.** Intermediate products in a calculator can exceed 32 bits even when the final answer fits. Use `long long`.

### Related Patterns

- **Monotonic Stack** ([Pattern 15](#15-monotonic-stack--queue)) — also a stack, but popping is driven by value order rather than nesting
- **DFS** ([Pattern 8](#8-dfs-depth-first-search)) — recursive parsing *is* a DFS over the implicit parse tree
- **Design Problems** ([Pattern 26](#26-design-problems)) — Min Stack and Flatten Nested List Iterator reuse these ideas
- **See also:** [Stacks](DSA_Fundamentals.md#3-stacks) for array vs linked-list implementations and amortized analysis

### Example Problems

#### Problem 1: Valid Parentheses (LC 20) — Easy

**Problem**: Given a string of `()[]{}`, determine whether it is valid: every opener is closed by the same type, in the correct order.

**Link**: [https://leetcode.com/problems/valid-parentheses/](https://leetcode.com/problems/valid-parentheses/)

**Intuition**: The most recent unmatched opener must be closed first (LIFO). Pushing the *expected closer* instead of the opener makes the comparison a single equality check.

**Python Solution**:

```python
class Solution:
    def isValid(self, s: str) -> bool:
        closer = {'(': ')', '[': ']', '{': '}'}
        stack = []
        for ch in s:
            if ch in closer:
                stack.append(closer[ch])
            elif not stack or stack.pop() != ch:
                return False
        return not stack
```

**C++ Solution**:

```cpp
#include <string>
#include <vector>
using namespace std;

class Solution {
public:
    bool isValid(string s) {
        vector<char> stack;
        for (char ch : s) {
            if (ch == '(') stack.push_back(')');
            else if (ch == '[') stack.push_back(']');
            else if (ch == '{') stack.push_back('}');
            else if (stack.empty() || stack.back() != ch) return false;
            else stack.pop_back();
        }
        return stack.empty();
    }
};
```

**Complexity**: Time O(n). Space O(n). An odd-length string can be rejected up front.

---

#### Problem 2: Evaluate Reverse Polish Notation (LC 150) — Medium

**Problem**: Evaluate an expression in postfix notation, e.g. `["2","1","+","3","*"] → 9`. Division truncates toward zero.

**Link**: [https://leetcode.com/problems/evaluate-reverse-polish-notation/](https://leetcode.com/problems/evaluate-reverse-polish-notation/)

**Intuition**: Postfix needs no precedence rules or parentheses. Every operator applies to the two most recent values. Push numbers. On an operator, pop `b`, then `a`, and push `a op b`.

**Python Solution**:

```python
class Solution:
    def evalRPN(self, tokens: list[str]) -> int:
        stack = []
        for tok in tokens:
            if tok in ("+", "-", "*", "/"):
                b = stack.pop()
                a = stack.pop()
                if tok == "+":
                    stack.append(a + b)
                elif tok == "-":
                    stack.append(a - b)
                elif tok == "*":
                    stack.append(a * b)
                else:
                    stack.append(int(a / b))   # truncate toward zero (32-bit operands)
            else:
                stack.append(int(tok))         # handles "-11"
        return stack[0]
```

**C++ Solution**:

```cpp
#include <string>
#include <vector>
using namespace std;

class Solution {
public:
    int evalRPN(vector<string>& tokens) {
        vector<long long> st;
        for (const string& t : tokens) {
            if (t.size() == 1 && (t[0] == '+' || t[0] == '-' || t[0] == '*' || t[0] == '/')) {
                long long b = st.back(); st.pop_back();
                long long a = st.back(); st.pop_back();
                switch (t[0]) {
                    case '+': st.push_back(a + b); break;
                    case '-': st.push_back(a - b); break;
                    case '*': st.push_back(a * b); break;
                    default:  st.push_back(a / b); break;
                }
            } else {
                st.push_back(stoll(t));
            }
        }
        return (int)st.back();
    }
};
```

**Complexity**: Time O(n). Space O(n).

**Pitfall**: In C++, testing `t[0] == '-'` alone misclassifies negative numbers like `"-11"` as operators. Check `t.size() == 1` first.

---

#### Problem 3: Basic Calculator II (LC 227) — Medium

**Problem**: Evaluate a string with non-negative integers, `+ - * /`, and spaces (no parentheses). Division truncates toward zero.

**Link**: [https://leetcode.com/problems/basic-calculator-ii/](https://leetcode.com/problems/basic-calculator-ii/)

**Intuition**: Keep the **previous operator** `op`. When a number is complete, apply `op`. For `+` / `-`, push `±num` as a new term. For `*` / `/`, combine with the top term right away, because those operators bind tighter. The answer is the sum of the stack. Only the top term is ever modified, so the stack can be replaced by a `last` variable plus a running `result` for O(1) space.

`"3+2*2"`: push 3, push 2, see `*` with next 2 → top = 2*2 = 4 → sum = 7.

**Python Solution**:

```python
class Solution:
    def calculate(self, s: str) -> int:
        stack, num, op = [], 0, "+"
        for i, ch in enumerate(s):
            if ch.isdigit():
                num = num * 10 + int(ch)
            if (not ch.isdigit() and ch != " ") or i == len(s) - 1:
                if op == "+":
                    stack.append(num)
                elif op == "-":
                    stack.append(-num)
                elif op == "*":
                    stack.append(stack.pop() * num)
                else:
                    stack.append(int(stack.pop() / num))   # truncate toward zero
                op, num = ch, 0
        return sum(stack)
```

**C++ Solution** (O(1)-space variant):

```cpp
#include <string>
using namespace std;

class Solution {
public:
    int calculate(string s) {
        long long result = 0, last = 0, num = 0;
        char op = '+';
        for (size_t i = 0; i < s.size(); ++i) {
            char ch = s[i];
            if (isdigit(static_cast<unsigned char>(ch))) num = num * 10 + (ch - '0');
            if ((!isdigit(static_cast<unsigned char>(ch)) && ch != ' ') || i + 1 == s.size()) {
                if (op == '+' || op == '-') {
                    result += last;                  // commit the finished term
                    last = (op == '+') ? num : -num;
                } else if (op == '*') {
                    last *= num;
                } else {
                    last /= num;                     // truncates toward zero
                }
                op = ch;
                num = 0;
            }
        }
        return (int)(result + last);
    }
};
```

**Complexity**: Time O(n). Space O(n) in the stack version, O(1) in the variant.

---

#### Problem 4: Basic Calculator (LC 224) — Hard

**Problem**: Evaluate a string with non-negative integers, `+`, `-`, parentheses, and spaces. `-` may be unary (`"-(2+3)"`). There is no `*` or `/`.

**Link**: [https://leetcode.com/problems/basic-calculator/](https://leetcode.com/problems/basic-calculator/)

**Intuition**: With only `+` and `-`, the value is a signed sum. Track the running `result` and the `sign` that applies to the next number. On `(`, push `(result, sign)` and start a fresh sub-expression. On `)`, finish the sub-expression, multiply it by the saved sign, and add it to the saved result. A leading `-` works because it simply sets `sign = -1` with `result = 0`.

**Python Solution**:

```python
class Solution:
    def calculate(self, s: str) -> int:
        result, sign, num = 0, 1, 0
        stack = []
        for ch in s:
            if ch.isdigit():
                num = num * 10 + int(ch)
            elif ch in "+-":
                result += sign * num
                num = 0
                sign = 1 if ch == "+" else -1
            elif ch == "(":
                stack.append((result, sign))
                result, sign = 0, 1
            elif ch == ")":
                result += sign * num
                num = 0
                prev_result, prev_sign = stack.pop()
                result = prev_result + prev_sign * result
        return result + sign * num
```

**C++ Solution**:

```cpp
#include <string>
#include <utility>
#include <vector>
using namespace std;

class Solution {
public:
    int calculate(string s) {
        long long result = 0, num = 0;
        int sign = 1;
        vector<pair<long long, int>> stack;
        for (char ch : s) {
            if (isdigit(static_cast<unsigned char>(ch))) {
                num = num * 10 + (ch - '0');
            } else if (ch == '+' || ch == '-') {
                result += sign * num;
                num = 0;
                sign = (ch == '+') ? 1 : -1;
            } else if (ch == '(') {
                stack.push_back({result, sign});
                result = 0;
                sign = 1;
            } else if (ch == ')') {
                result += sign * num;
                num = 0;
                auto [prevResult, prevSign] = stack.back();
                stack.pop_back();
                result = prevResult + prevSign * result;
            }
        }
        return (int)(result + sign * num);
    }
};
```

**Complexity**: Time O(n). Space O(depth of nesting).

**Basic Calculator III (LC 772)**, which combines `* /` with parentheses, is exactly the recursive-descent template above. The iterative alternative is **shunting-yard**: convert to RPN with an operator stack that respects precedence and associativity, then evaluate the RPN.

---

#### Problem 5: Decode String (LC 394) — Medium

**Problem**: Decode `k[encoded]` (repeat `encoded` k times) with arbitrary nesting: `"3[a2[c]]" → "accaccacc"`.

**Link**: [https://leetcode.com/problems/decode-string/](https://leetcode.com/problems/decode-string/)

**Intuition**: On `[`, the current partial string and the pending repeat count belong to the **outer** level, so push both and start fresh. On `]`, pop `(outer, k)` and set `current = outer + current * k`. Accumulate pieces in a list (Python) or `string` (C++) to avoid quadratic concatenation.

**Python Solution**:

```python
class Solution:
    def decodeString(self, s: str) -> str:
        stack = []                 # (outer_parts, repeat)
        parts, k = [], 0
        for ch in s:
            if ch.isdigit():
                k = k * 10 + int(ch)
            elif ch == "[":
                stack.append((parts, k))
                parts, k = [], 0
            elif ch == "]":
                outer, repeat = stack.pop()
                outer.append("".join(parts) * repeat)
                parts = outer
            else:
                parts.append(ch)
        return "".join(parts)
```

**C++ Solution**:

```cpp
#include <string>
#include <utility>
#include <vector>
using namespace std;

class Solution {
public:
    string decodeString(string s) {
        vector<pair<string, int>> stack;
        string cur;
        int k = 0;
        for (char ch : s) {
            if (isdigit(static_cast<unsigned char>(ch))) {
                k = k * 10 + (ch - '0');
            } else if (ch == '[') {
                stack.push_back({std::move(cur), k});
                cur.clear();
                k = 0;
            } else if (ch == ']') {
                auto [outer, repeat] = std::move(stack.back());
                stack.pop_back();
                outer.reserve(outer.size() + cur.size() * repeat);
                for (int i = 0; i < repeat; ++i) outer += cur;
                cur = std::move(outer);
            } else {
                cur += ch;
            }
        }
        return cur;
    }
};
```

**Complexity**: Time O(output length), which can be exponential in the input length for deep nesting (`9[9[9[a]]]`). Space O(output length).

---

#### Problem 6: Simplify Path (LC 71) — Medium

**Problem**: Convert an absolute Unix path to canonical form: collapse `//`, drop `.`, resolve `..` (going up from the root stays at the root), and remove the trailing slash. `"/a/./b/../../c/" → "/c"`.

**Link**: [https://leetcode.com/problems/simplify-path/](https://leetcode.com/problems/simplify-path/)

**Intuition**: Split on `/`. Empty pieces (from `//`) and `.` do nothing. `..` pops if possible. Anything else, including `...`, is a directory name and gets pushed.

**Python Solution**:

```python
class Solution:
    def simplifyPath(self, path: str) -> str:
        stack = []
        for part in path.split("/"):
            if part == "..":
                if stack:
                    stack.pop()
            elif part and part != ".":
                stack.append(part)
        return "/" + "/".join(stack)
```

**C++ Solution**:

```cpp
#include <sstream>
#include <string>
#include <vector>
using namespace std;

class Solution {
public:
    string simplifyPath(string path) {
        vector<string> stack;
        stringstream ss(path);
        string part;
        while (getline(ss, part, '/')) {
            if (part == "..") {
                if (!stack.empty()) stack.pop_back();
            } else if (!part.empty() && part != ".") {
                stack.push_back(part);
            }
        }
        string out;
        for (const string& p : stack) out += "/" + p;
        return out.empty() ? "/" : out;
    }
};
```

**Complexity**: Time O(n). Space O(n).

**Follow-up**: A real `realpath()` also resolves **symlinks**, which needs filesystem access because `a/link/..` is not necessarily `a`. The string-only algorithm corresponds to `os.path.normpath` (Python) and `std::filesystem::path::lexically_normal` (C++17). Both are purely lexical.

---

#### Problem 7: Asteroid Collision (LC 735) — Medium

**Problem**: Positive values move right and negative values move left, with the absolute value as size. When two collide, the smaller one explodes, and if they are equal both explode. Return the final state.

**Link**: [https://leetcode.com/problems/asteroid-collision/](https://leetcode.com/problems/asteroid-collision/)

**Intuition**: A collision only happens when a **left-mover** meets a **right-mover already on the stack**. While the incoming asteroid is negative and the top is positive, compare sizes: pop smaller tops, destroy both if equal, and stop if the top is larger. Push the incoming asteroid if it survives.

**Python Solution**:

```python
class Solution:
    def asteroidCollision(self, asteroids: list[int]) -> list[int]:
        stack = []
        for a in asteroids:
            alive = True
            while alive and a < 0 and stack and stack[-1] > 0:
                if stack[-1] < -a:
                    stack.pop()            # top explodes; keep checking
                elif stack[-1] == -a:
                    stack.pop()            # both explode
                    alive = False
                else:
                    alive = False          # incoming explodes
            if alive:
                stack.append(a)
        return stack
```

**C++ Solution**:

```cpp
#include <vector>
using namespace std;

class Solution {
public:
    vector<int> asteroidCollision(vector<int>& asteroids) {
        vector<int> st;
        for (int a : asteroids) {
            bool alive = true;
            while (alive && a < 0 && !st.empty() && st.back() > 0) {
                if (st.back() < -a) st.pop_back();
                else { if (st.back() == -a) st.pop_back(); alive = false; }
            }
            if (alive) st.push_back(a);
        }
        return st;
    }
};
```

**Complexity**: Time O(n), since each asteroid is pushed and popped at most once. Space O(n).

### Interview Q&A

**Q1.** Why does `int(a / b)` work for truncating division in Python, and when does it break?

`a / b` is float division, and `int()` truncates toward zero, which matches C semantics. A double represents integers exactly up to 2^53. For 32-bit operands the quotient is correctly rounded and cannot round across an integer boundary, so the result is exact. For arbitrary-precision operands (e.g. `10**30 // 7`) the float loses precision and the result is wrong. Use the exact form `q = abs(a) // abs(b)`, then negate `q` if the signs differ. Also remember that `//` and `%` in Python satisfy `a == (a // b) * b + a % b` with the remainder taking the sign of `b`, while in C++ it takes the sign of `a`.

**Q2.** Compare recursive descent, shunting-yard, and Pratt parsing.

**Recursive descent** uses one function per precedence level. It is easy to write and to extend with new constructs such as function calls and variables, and it gives good error messages. Its drawbacks are deep recursion on nested input and one level of call per precedence tier. **Shunting-yard** (Dijkstra) is iterative. It uses an operator stack plus an output queue to produce RPN, encodes precedence and associativity as table lookups, and needs no recursion. Its downside is that error handling for malformed input is fiddlier. **Pratt / precedence climbing** keeps recursive descent's structure but drives it from a binding-power table, so adding an operator is a table entry. Most production expression languages use recursive descent or Pratt. Right-associative operators like `^` are handled by recursing with the *same* precedence on the right-hand side, not one higher.

**Q3.** A profiler lets users define derived metrics as formula strings over hardware counters, e.g. `100 * (SQ_INSTS_VALU / SQ_WAVES)`. How do you evaluate them safely and efficiently?

Never call `eval()` on user or config strings, because that is arbitrary code execution. Instead: (1) **tokenize** into numbers, identifiers, operators, and parentheses; (2) **parse** into an AST, either with recursive descent or with Python's `ast.parse(expr, mode="eval")` plus a whitelist of node types (`BinOp`, `UnaryOp`, `Name`, `Constant`, a few `Call`s like `max`/`min`); (3) **validate** that every identifier is a known counter or previously defined metric, and detect cycles among metric definitions with a topological sort; (4) **evaluate** the AST over whole columns (numpy/pandas vectors), so one tree walk handles all kernels or dispatches; (5) define semantics for division by zero (return NaN/None rather than crash) and for missing counters. Cache the parsed AST per formula. Parse once, evaluate many times.

**Q4.** Valid Parentheses with only `(` and `)`: can you do better than O(n) space? And what about `*` wildcards?

With one bracket type you only need a **counter**: increment on `(`, decrement on `)`, fail if it goes negative, and succeed if it ends at 0. That is O(1) space. With `*` wildcards that can be `(`, `)`, or empty (LC 678), track the **range** `[lo, hi]` of possible open counts. `(` increments both, `)` decrements both, and `*` does `lo -= 1, hi += 1`. Clamp `lo` at 0, fail if `hi < 0`, and the string is valid if `lo == 0` at the end. That is O(n) time and O(1) space.

**Q5.** How do you avoid `RecursionError` for deeply nested input like Decode String with 10^4 levels?

The stack-based iterative versions shown above use heap memory and have no depth limit. For recursive-descent parsers, either convert to an explicit stack (shunting-yard), raise the limit via `sys.setrecursionlimit` (which risks a C-stack segfault, so pair it with `threading.stack_size`), or reject input nesting deeper than a sane maximum. Rejecting is what hardened JSON parsers do, to resist stack-exhaustion denial of service.

---

## 25. Line Sweep & Advanced Intervals

### Overview

[Pattern 4](#4-merge-intervals) covers sort-and-merge. **Line sweep** generalizes it. Turn every interval into **events** (a start event and an end event), sort the events by coordinate, and move an imaginary vertical line across them while maintaining an **active set**. The active set can be a counter, a heap, a multiset, or a balanced BST. Each question becomes "what does the active set look like at this x?"

```text
intervals:  [1,4) [2,5) [7,9)
events:     (1,+1) (2,+1) (4,-1) (5,-1) (7,+1) (9,-1)
active:        1      2      1      0      1      0     → max overlap = 2
```

**Tie-breaking is the key detail.** With **half-open** intervals `[s, e)` (meetings: one ending at 10 and one starting at 10 do not conflict), process the end before the start at equal coordinates, so sort `(x, -1)` before `(x, +1)`. With **closed** intervals `[s, e]` (balloons: touching at a point counts), process starts first.

| Active-set structure | Answers | Example |
|---|---|---|
| Integer counter | max overlap, "is capacity ever exceeded" | Meeting Rooms II, Car Pooling |
| Min-heap of end times | rooms needed + which room is free | Meeting Rooms II (heap form) |
| Max-heap / multiset of heights | current maximum among active intervals | The Skyline Problem |
| Ordered map `start → end` | insert/query disjoint intervals online | My Calendar I, Range Module |
| Ordered map `x → delta` | online overlap count | My Calendar III |
| Segment tree over compressed coordinates | covered length, range max with updates | Rectangle Area II, Falling Squares |

### When to Use

- "Minimum number of rooms / platforms / servers so that nothing overlaps"
- "Maximum number of concurrent ..." at any point in time
- "Intersection of two sorted interval lists"
- "Minimum points (arrows) to hit every interval" → greedy by end
- Online booking: "reject if it would cause a (double/triple) booking"
- Outline or union of rectangles: skyline, covered area
- Trace analysis: concurrency over time, busy vs idle time, overlap of GPU kernels with memory copies

### Template Code

**Event sweep: maximum concurrent intervals (half-open)**

```python
# Python — event sweep template
def max_concurrent(intervals: list[tuple[int, int]]) -> int:
    events = []
    for s, e in intervals:
        events.append((s, 1))
        events.append((e, -1))
    events.sort()                       # (x, -1) sorts before (x, +1): end before start
    active = best = 0
    for _, delta in events:
        active += delta
        best = max(best, active)
    return best

assert max_concurrent([(1, 4), (2, 5), (7, 9)]) == 2
assert max_concurrent([(1, 2), (2, 3)]) == 1         # touching is not overlapping
```

```cpp
// C++ — event sweep template
#include <algorithm>
#include <utility>
#include <vector>
using namespace std;

int maxConcurrent(const vector<pair<int, int>>& intervals) {
    vector<pair<int, int>> events;
    events.reserve(intervals.size() * 2);
    for (auto [s, e] : intervals) {
        events.emplace_back(s, +1);
        events.emplace_back(e, -1);
    }
    sort(events.begin(), events.end());   // pair compare: -1 before +1 at equal x
    int active = 0, best = 0;
    for (auto [x, d] : events) best = max(best, active += d);
    return best;
}
```

**Ordered-map difference sweep (online)** — `std::map<int,int>` in C++. Python has no built-in balanced BST, so use `sortedcontainers.SortedDict` where it is allowed, or `bisect` on a sorted key list (O(n) insert).

```cpp
// C++ — online overlap counter with an ordered map
#include <algorithm>
#include <map>
using namespace std;

struct OverlapCounter {
    map<int, int> delta;                      // x -> net change at x
    int add(int start, int end) {             // returns the max overlap after adding [start, end)
        ++delta[start];
        --delta[end];
        int active = 0, best = 0;
        for (auto& [x, d] : delta) best = max(best, active += d);
        return best;
    }
};
```

### Variations

| Variation | Technique | Example Problems |
|---|---|---|
| **Max overlap / resources** | +1/-1 events, or heap of ends | Meeting Rooms II (LC 253), Minimum Number of Platforms, Car Pooling (LC 1094) |
| **Overlap with weights** | +w/-w events | Maximum Population Year (LC 1854), Describe the Painting (LC 1943) |
| **Two sorted lists** | two pointers on ends | Interval List Intersections (LC 986) |
| **Greedy stabbing** | sort by end, shoot at end | Minimum Number of Arrows to Burst Balloons (LC 452), Non-overlapping Intervals (LC 435) |
| **Online disjoint booking** | ordered map neighbours | My Calendar I (LC 729) |
| **Online k-booking** | overlap list, or ordered-map sweep | My Calendar II (LC 731), My Calendar III (LC 732) |
| **Dynamic interval set** | ordered map with merge/split | Range Module (LC 715), Data Stream as Disjoint Intervals (LC 352) |
| **Max over active set** | multiset / lazy-deletion heap | The Skyline Problem (LC 218) |
| **Covered length / area** | sweep + segment tree (coordinate compression) | Rectangle Area II (LC 850) |
| **Free time** | merge then gaps | Employee Free Time (LC 759) — see [4.5](#45-hard--employee-free-time-leetcode-759) |

### Common Mistakes

1. **Wrong tie-break.** For half-open meetings `[1,2)` and `[2,3)`, processing the start first reports 2 rooms. For closed balloons `[1,2]` and `[2,3]`, one arrow at 2 bursts both. Decide whether the intervals are closed or half-open before writing the comparator.
2. **Comparator overflow in C++.** `return a[1] - b[1] < 0` overflows for values near ±2^31 (LC 452 includes them). Compare directly with `a[1] < b[1]`.
3. **Sorting by start when the greedy needs end.** Arrow and activity-selection greedies sort by **end**. Sorting by start requires extra `min(end)` bookkeeping.
4. **Skyline: emitting duplicate heights or duplicate x.** Only output a key point when the current max height **changes**. Process all events at the same x before comparing (or order them so that intermediate states cannot change the max).
5. **Python heap "removal".** `heapq` cannot delete arbitrary elements. Use lazy deletion (store the end coordinate and pop from the top while the top has expired) and never assume the top is valid without checking.
6. **Mutating a `std::map` while iterating** without using the iterator returned by `erase`.

### Related Patterns

- **Merge Intervals** ([Pattern 4](#4-merge-intervals)) — the static, sort-once special case
- **Prefix Sum & Difference Array** ([Pattern 21](#21-prefix-sum--difference-array)) — a dense-coordinate sweep *is* a difference array
- **Two Heaps / Top K** ([Pattern 9](#9-two-heaps), [Pattern 12](#12-top-k-elements)) — heap-maintained active sets
- **Greedy** ([Pattern 19](#19-greedy)) — interval scheduling by earliest end
- **See also:** [Segment Trees](DSA_Fundamentals.md#11-segment-trees) for sweep + range-update structures

### Example Problems

#### Problem 1: Meeting Rooms II (LC 253) — Medium

**Problem**: Given meeting intervals `[start, end)`, return the minimum number of conference rooms required.

**Link**: [https://leetcode.com/problems/meeting-rooms-ii/](https://leetcode.com/problems/meeting-rooms-ii/)

**Intuition**: The answer equals the **maximum number of meetings in progress at once**. Two standard solutions:

- **Min-heap of end times.** Process meetings by start. If the earliest-ending room is free (`heap[0] <= start`), reuse it by replacing its end. Otherwise open a new room. The heap size is the answer. This form can also report **which** room each meeting uses.
- **Sweep with two sorted arrays.** Sort starts and ends separately. Walk the starts. If the current start is at or after the earliest unconsumed end, a room was released, so advance the end pointer. Otherwise a new room is needed.

**Python Solution** (heap and sweep):

```python
import heapq

class Solution:
    def minMeetingRooms(self, intervals: list[list[int]]) -> int:
        intervals.sort(key=lambda iv: iv[0])
        ends = []                                  # min-heap of end times
        for start, end in intervals:
            if ends and ends[0] <= start:
                heapq.heapreplace(ends, end)       # reuse the room that frees first
            else:
                heapq.heappush(ends, end)          # need a new room
        return len(ends)

    def minMeetingRoomsSweep(self, intervals: list[list[int]]) -> int:
        starts = sorted(s for s, _ in intervals)
        ends = sorted(e for _, e in intervals)
        rooms = j = 0
        for s in starts:
            if s >= ends[j]:
                j += 1                             # a meeting ended: reuse its room
            else:
                rooms += 1
        return rooms
```

**C++ Solution** (heap and sweep):

```cpp
#include <algorithm>
#include <functional>
#include <queue>
#include <vector>
using namespace std;

class Solution {
public:
    int minMeetingRooms(vector<vector<int>>& intervals) {
        sort(intervals.begin(), intervals.end(),
             [](const auto& a, const auto& b) { return a[0] < b[0]; });
        priority_queue<int, vector<int>, greater<int>> ends;   // min-heap
        for (const auto& iv : intervals) {
            if (!ends.empty() && ends.top() <= iv[0]) ends.pop();
            ends.push(iv[1]);
        }
        return ends.size();
    }

    int minMeetingRoomsSweep(vector<vector<int>>& intervals) {
        vector<int> starts, ends;
        for (const auto& iv : intervals) { starts.push_back(iv[0]); ends.push_back(iv[1]); }
        sort(starts.begin(), starts.end());
        sort(ends.begin(), ends.end());
        int rooms = 0;
        size_t j = 0;
        for (int s : starts) {
            if (s >= ends[j]) ++j;
            else ++rooms;
        }
        return rooms;
    }
};
```

**Complexity**: Both are O(n log n) time and O(n) space.

**Why the sweep is correct**: Once sorted separately, starts and ends lose their pairing, but the number of meetings active at time `t` is still `#starts ≤ t − #ends ≤ t`. Pairing does not matter for counting. It does matter if you must output room assignments, which is why the heap form exists.

---

#### Problem 2: Interval List Intersections (LC 986) — Medium

**Problem**: Given two lists of **closed**, pairwise-disjoint, sorted intervals, return their intersection.

**Link**: [https://leetcode.com/problems/interval-list-intersections/](https://leetcode.com/problems/interval-list-intersections/)

**Intuition**: The intersection of `[a1, a2]` and `[b1, b2]` is `[max(a1, b1), min(a2, b2)]` if that range is non-empty. After comparing, advance the interval that **ends first**. It cannot intersect anything later in the other list, because those later intervals start after the current one in that list.

**Python Solution**:

```python
class Solution:
    def intervalIntersection(self, A: list[list[int]], B: list[list[int]]) -> list[list[int]]:
        i = j = 0
        out = []
        while i < len(A) and j < len(B):
            lo = max(A[i][0], B[j][0])
            hi = min(A[i][1], B[j][1])
            if lo <= hi:                       # closed intervals: touching counts
                out.append([lo, hi])
            if A[i][1] < B[j][1]:
                i += 1
            else:
                j += 1
        return out
```

**C++ Solution**:

```cpp
#include <algorithm>
#include <vector>
using namespace std;

class Solution {
public:
    vector<vector<int>> intervalIntersection(vector<vector<int>>& A, vector<vector<int>>& B) {
        vector<vector<int>> out;
        size_t i = 0, j = 0;
        while (i < A.size() && j < B.size()) {
            int lo = max(A[i][0], B[j][0]);
            int hi = min(A[i][1], B[j][1]);
            if (lo <= hi) out.push_back({lo, hi});
            (A[i][1] < B[j][1]) ? ++i : ++j;
        }
        return out;
    }
};
```

**Complexity**: Time O(m + n). Space O(1) besides the output.

---

#### Problem 3: Minimum Number of Arrows to Burst Balloons (LC 452) — Medium

**Problem**: Balloons are **closed** intervals `[xstart, xend]` on the x-axis. An arrow shot at `x` bursts every balloon with `xstart <= x <= xend`. Return the minimum number of arrows. Coordinates span the full 32-bit range.

**Link**: [https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/)

**Intuition**: Sort by **end**. The balloon that ends first must be hit by some arrow at or before its end. Shooting exactly **at** its end hits the most other balloons, an exchange argument: moving the arrow right up to that end never loses a balloon. Skip every balloon that starts at or before the arrow. The first one starting after it needs a new arrow at its own end.

**Python Solution**:

```python
class Solution:
    def findMinArrowShots(self, points: list[list[int]]) -> int:
        points.sort(key=lambda p: p[1])
        arrows, arrow_x = 0, None
        for start, end in points:
            if arrow_x is None or start > arrow_x:   # closed: start == arrow_x is hit
                arrows += 1
                arrow_x = end
        return arrows
```

**C++ Solution**:

```cpp
#include <algorithm>
#include <cstdint>
#include <vector>
using namespace std;

class Solution {
public:
    int findMinArrowShots(vector<vector<int>>& points) {
        sort(points.begin(), points.end(),
             [](const auto& a, const auto& b) { return a[1] < b[1]; });   // no subtraction: overflow
        int arrows = 0;
        long long arrowX = (long long)INT32_MIN - 1;                       // below any coordinate
        for (const auto& p : points) {
            if (p[0] > arrowX) {
                ++arrows;
                arrowX = p[1];
            }
        }
        return arrows;
    }
};
```

**Complexity**: Time O(n log n). Space O(1) besides the sort.

**Relation to LC 435**: The number of arrows equals the maximum number of pairwise non-overlapping balloons, so `Non-overlapping Intervals = n − (max non-overlapping set)` is solved by the same greedy. LC 435 uses half-open semantics, where touching does **not** overlap, so its comparison is `start >= last_end`.

---

#### Problem 4: My Calendar I (LC 729) and My Calendar III (LC 732)

**Problem (I, Medium)**: Implement `book(start, end)` for half-open `[start, end)`. Return `true` and record the booking if it does not overlap any existing booking, otherwise return `false`.

**Problem (III, Hard)**: `book` always succeeds and returns the maximum `k` such that some moment is covered by `k` bookings.

**Links**: [https://leetcode.com/problems/my-calendar-i/](https://leetcode.com/problems/my-calendar-i/) · [https://leetcode.com/problems/my-calendar-iii/](https://leetcode.com/problems/my-calendar-iii/)

**Intuition (I)**: The existing bookings are disjoint, so sorting them by start also sorts them by end. A new interval can only collide with its **predecessor** (the last booking starting at or before `start`) or its **successor** (the first booking starting after `start`). In an ordered map that is O(log n).

**Intuition (III)**: Keep a difference map `x → delta` (+1 at start, −1 at end) and sweep it in key order to find the maximum running sum. That is O(n) per booking, which is fine for LC's 400 calls. The O(log C) alternative is a dynamic segment tree with range add and range max.

**Python Solution**:

```python
import bisect

class MyCalendar:
    def __init__(self):
        self.starts: list[int] = []      # parallel sorted lists (bookings are disjoint)
        self.ends: list[int] = []

    def book(self, start: int, end: int) -> bool:
        i = bisect.bisect_right(self.starts, start)
        if i > 0 and self.ends[i - 1] > start:          # predecessor overlaps
            return False
        if i < len(self.starts) and self.starts[i] < end:   # successor overlaps
            return False
        self.starts.insert(i, start)                     # O(n) list insert
        self.ends.insert(i, end)
        return True


class MyCalendarThree:
    def __init__(self):
        self.delta: dict[int, int] = {}
        self.keys: list[int] = []        # sorted coordinates

    def book(self, start: int, end: int) -> int:
        for x, d in ((start, 1), (end, -1)):
            if x not in self.delta:
                bisect.insort(self.keys, x)
                self.delta[x] = 0
            self.delta[x] += d
        active = best = 0
        for x in self.keys:
            active += self.delta[x]
            best = max(best, active)
        return best
```

**C++ Solution**:

```cpp
#include <algorithm>
#include <iterator>
#include <map>
using namespace std;

class MyCalendar {
    map<int, int> booked;                      // start -> end, disjoint
public:
    bool book(int start, int end) {
        auto next = booked.lower_bound(start);  // first booking with s >= start
        if (next != booked.end() && next->first < end) return false;
        if (next != booked.begin() && prev(next)->second > start) return false;
        booked.emplace(start, end);
        return true;
    }
};

class MyCalendarThree {
    map<int, int> delta;
public:
    int book(int start, int end) {
        ++delta[start];
        --delta[end];
        int active = 0, best = 0;
        for (const auto& [x, d] : delta) best = max(best, active += d);
        return best;
    }
};
```

**Complexity**: My Calendar I is O(log n) per `book` in C++ (`std::map`), and O(n) per `book` in Python because of the list insert, which is fast in practice since it is a `memmove`. My Calendar III is O(n) per `book` with the sweep.

---

#### Problem 5: The Skyline Problem (LC 218) — Hard

**Problem**: Buildings are `[left, right, height]`. Return the skyline as key points `[x, height]` wherever the outline's height changes. The last point has height 0.

**Link**: [https://leetcode.com/problems/the-skyline-problem/](https://leetcode.com/problems/the-skyline-problem/)

**Intuition**: Sweep x from left to right. The outline height at x is the **maximum height of the buildings active at x**. Maintain the active heights in a structure that supports insert, delete, and max:

- **C++**: `multiset<int>` (a balanced BST, so duplicates are allowed). Insert on start, erase *one* copy on end, and take the max with `*rbegin()`.
- **Python**: a max-heap of `(-height, right)` with **lazy deletion**. Before reading the top, pop entries whose `right <= x`. Entries buried below the top may also be expired. That is harmless, because they get popped once they reach the top.

Event order at equal x: starts before ends, taller starts first, and among ends the shorter first. This ordering prevents spurious intermediate key points. In C++, encoding a start as `(x, -h)` and an end as `(x, +h)` and sorting the pairs gives exactly this order.

**Python Solution**:

```python
import heapq

class Solution:
    def getSkyline(self, buildings: list[list[int]]) -> list[list[int]]:
        events = []
        for left, right, height in buildings:
            events.append((left, -height, right))   # start event (taller first)
            events.append((right, 0, 0))            # end marker: just triggers cleanup
        events.sort()

        result = []
        heap = [(0, float("inf"))]                  # (-height, right); ground never expires
        for x, neg_h, right in events:
            while heap[0][1] <= x:                  # lazy deletion of expired buildings
                heapq.heappop(heap)
            if neg_h:
                heapq.heappush(heap, (neg_h, right))
            height = -heap[0][0]
            if not result or result[-1][1] != height:
                result.append([x, height])
        return result
```

**C++ Solution**:

```cpp
#include <algorithm>
#include <set>
#include <utility>
#include <vector>
using namespace std;

class Solution {
public:
    vector<vector<int>> getSkyline(vector<vector<int>>& buildings) {
        vector<pair<int, int>> events;              // (x, -h) start, (x, +h) end
        for (const auto& b : buildings) {
            events.emplace_back(b[0], -b[2]);
            events.emplace_back(b[1], b[2]);
        }
        sort(events.begin(), events.end());

        multiset<int> active{0};                    // ground level
        vector<vector<int>> result;
        int prevHeight = 0;
        for (auto [x, h] : events) {
            if (h < 0) active.insert(-h);
            else active.erase(active.find(h));      // erase ONE copy, not all equal heights
            int cur = *active.rbegin();
            if (cur != prevHeight) {
                result.push_back({x, cur});
                prevHeight = cur;
            }
        }
        return result;
    }
};
```

**Complexity**: Time O(n log n). Space O(n).

**Pitfall**: `active.erase(h)` with a value erases **all** copies, which breaks when two buildings share a height. Always use `erase(find(h))`.

### Interview Q&A

**Q1.** Meeting Rooms II: when do you prefer the heap over the sweep?

Both are O(n log n). The **sweep** has better constants: two sorts plus a linear scan over flat arrays, which is cache-friendly. It answers "how many". The **heap** processes meetings in start order and knows *which* room frees up, so it can output an assignment (store `(end, room_id)`). It also extends to streaming input sorted by start, where it keeps O(max concurrent) memory instead of O(n). If the input is huge and the times are small integers (minutes in a day), a difference array over 1440 slots is O(n + 1440).

**Q2.** You have a trace of GPU kernel dispatches as `(queue_id, start_ns, end_ns)` across several hardware queues. How do you compute (a) total GPU busy time, (b) the peak number of concurrent kernels, and (c) the idle gaps?

(a) **Busy time** is the length of the *union* of all intervals. Sort by start, merge overlaps (Pattern 4), and sum the merged lengths. Do not sum the raw durations, because concurrent kernels would be double counted. (b) **Peak concurrency** is the event sweep with +1/−1 and ends before starts at equal timestamps. Record the timestamp where the maximum occurs. (c) **Idle gaps** are the complements between consecutive merged intervals, often filtered by a threshold such as gaps > 10 µs, which point to launch overhead or host-side synchronization. All three are O(n log n), dominated by the sort. If each queue's records are already time-ordered, a k-way merge of the queues is O(n log k). The same sweep with per-category counters (kernel vs memcpy) answers "how much copy time overlapped with compute".

**Q3.** Why does the Python skyline solution remain correct even though expired buildings can stay buried in the heap?

The output only depends on the **maximum** active height. An expired entry matters only if it is at the top. The `while heap[0][1] <= x` loop guarantees the top is live before every read. Buried expired entries are popped later when they surface. Each building is pushed once and popped at most once, so the total work stays O(n log n). The heap can grow to O(n) with stale entries, the usual tradeoff of lazy deletion.

**Q4.** My Calendar III gets `10^5` calls instead of 400. What changes?

The O(n)-per-call map sweep becomes O(n²) = 10^10 operations, which is too slow. Use a **segment tree with lazy propagation** supporting range add on `[start, end)` and a global max. The coordinates go up to `10^9`, so either build it **dynamically** (create children on demand, O(log C) nodes per update) or compress coordinates offline if all queries are known up front. Each `book` is then O(log C) with C = 10^9, so about 30 levels.

**Q5.** Closed vs half-open: how do you derive the tie-break instead of memorizing it?

Ask: "if one interval ends at x and another starts at x, are both active at x?" For **half-open** `[s, e)`, the first is not active at x, so its −1 must be applied before the second's +1. For **closed** `[s, e]`, both are active at x, so apply the +1 first (or, in greedy form, test with `start > arrow` rather than `>=`). Write the rule in a comment next to the comparator. Off-by-one errors at shared endpoints are the most common bug in interval code.

---

## 26. Design Problems

### Overview

"Design a class" problems such as LRU Cache, Min Stack, and Time Based Key-Value Store give you an API plus a **complexity target per operation**. No single textbook structure meets every target, so the answer is nearly always a **composite**: two or more structures kept in sync, each providing one operation cheaply. Interviewers grade (1) picking the right combination, (2) keeping the invariants consistent across **every** mutating method, and (3) clean, bug-free code. Big-tech phone screens ask LRU Cache more than almost any other problem.

| Requirement | Composite structure | Problems |
|---|---|---|
| O(1) lookup **and** O(1) recency reordering / eviction | hash map → node in a **doubly linked list** | LRU Cache (LC 146) |
| O(1) eviction of least-frequent, ties by recency | key map + `freq → ordered list` buckets + `min_freq` | LFU Cache (LC 460) |
| O(1) insert / delete / **uniform random** | dynamic array + `value → index` map (swap with last on delete) | Insert Delete GetRandom O(1) (LC 380, 381) |
| O(1) `getMin` on a stack | stack of `(value, min_so_far)` | Min Stack (LC 155), Max Stack (LC 716) |
| "value as of time t" | per-key list sorted by time + binary search | Time Based Key-Value Store (LC 981), Snapshot Array (LC 1146) |
| counts over a sliding time window | circular buffer of buckets, or deque | Design Hit Counter (LC 362), Logger Rate Limiter (LC 359) |
| lazy traversal of a nested structure or tree | explicit stack | Flatten Nested List Iterator (LC 341), BST Iterator (LC 173), Peeking Iterator (LC 284) |
| streaming median / top-k | two heaps / heap + map | Find Median from Data Stream (LC 295) — see [Pattern 9](#9-two-heaps) |

**Interview recipe for design problems:**

1. **Restate the API and pin down the semantics.** What happens at capacity 0? Does `put` on an existing key count as a "use"? Are timestamps strictly increasing? Is `getRandom` called on an empty set?
2. **Write the complexity target next to each method**, then pick one structure per requirement.
3. **State the invariants** in one line each, e.g. "every key in the map has exactly one node in the list, and vice versa".
4. **Factor the shared mutations into private helpers** (`_remove(node)`, `_push_front(node)`, `_touch(key)`) so each invariant is maintained in one place.
5. **Walk through a call sequence** that exercises eviction, an update of an existing key, and the empty and full boundaries.

### When to Use

- The problem statement is a class with several methods and per-method complexity constraints ("`get` and `put` must each run in O(1) average time")
- "Implement an iterator" (`next` / `hasNext`) over a structure that should not be materialized up front
- "Return the value at time t / at snapshot s" → versioned storage + binary search
- "Count events in the last N seconds" → bucketed ring buffer

### Template Code

**Doubly linked list with sentinels** (the building block for LRU, LFU, and many O(1) "move to front" designs)

```python
# Python — doubly linked list with sentinel head/tail
class Node:
    __slots__ = ("key", "val", "prev", "next")

    def __init__(self, key: int = 0, val: int = 0):
        self.key, self.val = key, val
        self.prev: "Node | None" = None
        self.next: "Node | None" = None

class DList:
    """head <-> ... <-> tail; sentinels mean no None checks in insert/remove."""

    def __init__(self):
        self.head, self.tail = Node(), Node()
        self.head.next, self.tail.prev = self.tail, self.head
        self.size = 0

    def push_front(self, node: Node) -> None:
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node
        self.size += 1

    def remove(self, node: Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1

    def pop_back(self) -> Node:
        node = self.tail.prev
        self.remove(node)
        return node

d = DList()
a, b = Node(1, 1), Node(2, 2)
d.push_front(a); d.push_front(b)          # list: b, a
assert d.pop_back() is a and d.size == 1
```

In C++, use `std::list` and keep `std::list<...>::iterator` handles in the hash map. `list::splice` moves a node to another position **in O(1) without invalidating any iterators**, which makes it the idiomatic choice for LRU.

### Variations

| Variation | Key idea | Example Problems |
|---|---|---|
| **Recency cache** | map + DLL; `OrderedDict` / `std::list::splice` | LRU Cache (LC 146) |
| **Frequency cache** | per-frequency LRU lists + `min_freq` | LFU Cache (LC 460) |
| **Randomized set** | array + index map, swap-with-last | Insert Delete GetRandom O(1) (LC 380), with duplicates (LC 381) |
| **Augmented stack/queue** | carry aggregate with each element | Min Stack (LC 155), Max Stack (LC 716), Implement Queue using Stacks (LC 232) |
| **Versioned values** | append `(version, value)`, binary search on read | Time Based Key-Value Store (LC 981), Snapshot Array (LC 1146) |
| **Time-window counters** | ring buffer of `(timestamp, count)` buckets | Design Hit Counter (LC 362), Logger Rate Limiter (LC 359) |
| **Lazy iterators** | explicit stack; `hasNext` does the work and is idempotent | Flatten Nested List Iterator (LC 341), BST Iterator (LC 173), Peeking Iterator (LC 284), Zigzag Iterator (LC 281) |
| **Circular buffer** | head/tail indices modulo capacity | Design Circular Queue (LC 622), Design Circular Deque (LC 641) |
| **Prefix-structured store** | trie + values | Implement Trie (LC 208), Map Sum Pairs (LC 677) — see [Pattern 17](#17-trie-prefix-tree) |

### Common Mistakes

1. **LRU: forgetting that `put` on an existing key is a use.** Update the value **and** move the node to the front, and do not evict.
2. **LRU: not storing the key in the node.** On eviction you have the list tail and must delete its map entry, so the node needs to know its key.
3. **LFU: not updating `min_freq`.** When a key leaves the `min_freq` bucket and the bucket becomes empty, `min_freq` increases by exactly 1. A new key always resets `min_freq = 1`.
4. **RandomizedSet: updating the index map in the wrong order.** When the removed element *is* the last element, writing `idx[last] = i` after `del idx[val]` re-inserts it. Pop the map entry first and only move `last` if `i` is still in range.
5. **Iterators: doing work in `next()` that `hasNext()` depends on.** `hasNext()` must be **idempotent**, so calling it twice must not skip elements. Put the "advance to the next integer" logic in `hasNext()` and have `next()` call it.
6. **C++ iterator invalidation.** `vector::push_back` invalidates iterators and references on reallocation. `unordered_map` rehash invalidates iterators but **not** references or pointers to elements. `list` iterators survive everything except erasing that element.
7. **Capacity 0.** LFU on LeetCode includes `capacity = 0`, where `put` must be a no-op. Guard against it.

### Related Patterns

- **Two Heaps** ([Pattern 9](#9-two-heaps)) — Find Median from Data Stream is also a design problem
- **Modified Binary Search** ([Pattern 11](#11-modified-binary-search)) — versioned lookups
- **Stack-based Parsing** ([Pattern 24](#24-stack-based-parsing)) — iterators over nested input
- **Trie** ([Pattern 17](#17-trie-prefix-tree)) — autocomplete and prefix-sum design problems
- **See also:** [Worked Design: Cache](../design-patterns/Low_Level_Design_Interview_Prep.md#11-worked-design-cache) for the object-oriented LLD version (eviction policy interface, TTL), and [Concurrency Coding Problems](Concurrency_Coding_Problems.md) for a thread-safe LRU

### Example Problems

#### Problem 1: LRU Cache (LC 146) — Medium

**Problem**: Implement `LRUCache(capacity)`, `get(key)` (return -1 if absent), and `put(key, value)`. When inserting a new key at capacity, evict the **least recently used** key. Both operations must be O(1) average.

**Link**: [https://leetcode.com/problems/lru-cache/](https://leetcode.com/problems/lru-cache/)

**Intuition**: The hash map gives O(1) lookup but has no order. A list kept in recency order gives O(1) eviction from the tail, but finding a key in it is O(n). Combine them: the map stores a **pointer to the list node**, so `get` can locate the node in O(1) and unlink and relink it at the front in O(1). This requires `prev` pointers, so the list must be **doubly** linked.

**Invariants**: (1) `map` and the list contain exactly the same keys; (2) the list is ordered from most recent (front) to least recent (back); (3) `len(map) <= capacity`.

**Worked trace** (`capacity = 2`):

| Call | List (MRU → LRU) | Returns |
|---|---|---|
| `put(1, 1)` | 1 | — |
| `put(2, 2)` | 2, 1 | — |
| `get(1)` | 1, 2 | 1 |
| `put(3, 3)` | 3, 1 (evict 2) | — |
| `get(2)` | 3, 1 | -1 |
| `put(4, 4)` | 4, 3 (evict 1) | — |
| `get(1)` / `get(3)` / `get(4)` | 4, 3 → 3, 4 → 4, 3 | -1 / 3 / 4 |

**Python Solution** (explicit doubly linked list, which is what interviewers usually want):

```python
class _Node:
    __slots__ = ("key", "val", "prev", "next")

    def __init__(self, key: int = 0, val: int = 0):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.nodes: dict[int, _Node] = {}
        self.head, self.tail = _Node(), _Node()     # head.next = MRU, tail.prev = LRU
        self.head.next, self.tail.prev = self.tail, self.head

    def _unlink(self, node: _Node) -> None:
        node.prev.next, node.next.prev = node.next, node.prev

    def _push_front(self, node: _Node) -> None:
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        node = self.nodes.get(key)
        if node is None:
            return -1
        self._unlink(node)
        self._push_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        node = self.nodes.get(key)
        if node is not None:                         # update counts as a use
            node.val = value
            self._unlink(node)
            self._push_front(node)
            return
        if len(self.nodes) == self.capacity:
            lru = self.tail.prev
            self._unlink(lru)
            del self.nodes[lru.key]                  # why the node stores its key
        node = _Node(key, value)
        self.nodes[key] = node
        self._push_front(node)
```

**Python Solution** (`OrderedDict`, worth mentioning but expect "now do it without OrderedDict"):

```python
from collections import OrderedDict

class LRUCacheOD:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.data: OrderedDict[int, int] = OrderedDict()   # last = most recent

    def get(self, key: int) -> int:
        if key not in self.data:
            return -1
        self.data.move_to_end(key)                         # O(1)
        return self.data[key]

    def put(self, key: int, value: int) -> None:
        if key in self.data:
            self.data.move_to_end(key)
        self.data[key] = value
        if len(self.data) > self.capacity:
            self.data.popitem(last=False)                  # O(1): pop the LRU end
```

**C++ Solution** (`std::list` + `splice`):

```cpp
#include <list>
#include <unordered_map>
#include <utility>
using namespace std;

class LRUCache {
    using Item = pair<int, int>;                       // (key, value)
    size_t capacity;
    list<Item> items;                                  // front = MRU, back = LRU
    unordered_map<int, list<Item>::iterator> where;

public:
    explicit LRUCache(int cap) : capacity(cap) { where.reserve(cap); }

    int get(int key) {
        auto it = where.find(key);
        if (it == where.end()) return -1;
        items.splice(items.begin(), items, it->second); // O(1), iterator stays valid
        return it->second->second;
    }

    void put(int key, int value) {
        auto it = where.find(key);
        if (it != where.end()) {
            it->second->second = value;
            items.splice(items.begin(), items, it->second);
            return;
        }
        if (items.size() == capacity) {
            where.erase(items.back().first);
            items.pop_back();
        }
        items.emplace_front(key, value);
        where[key] = items.begin();
    }
};
```

**Complexity**: O(1) average for `get` and `put`. Space O(capacity).

**Follow-ups**: See the Interview Q&A below for thread safety, TTL expiry, and the approximations real systems use.

---

#### Problem 2: LFU Cache (LC 460) — Hard

**Problem**: Like LRU, but evict the key with the **lowest use count**, breaking ties by least recently used. `get` and `put` must be O(1). Both a `get` and an update-`put` increment the count. A new key starts at count 1.

**Link**: [https://leetcode.com/problems/lfu-cache/](https://leetcode.com/problems/lfu-cache/)

**Intuition**: Group keys into **buckets by frequency**. Each bucket is an LRU-ordered list. Keep `min_freq`. To touch a key, move it from bucket `f` to bucket `f+1`, and if bucket `f` empties and `f == min_freq`, increment `min_freq`. Frequencies only rise by 1 at a time, so `min_freq` never needs a search. To evict, pop the LRU end of bucket `min_freq`. Inserting a new key sets `min_freq = 1`.

**Python Solution**:

```python
from collections import OrderedDict, defaultdict

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.vals: dict[int, int] = {}
        self.freq: dict[int, int] = {}
        self.buckets: defaultdict[int, OrderedDict] = defaultdict(OrderedDict)  # freq -> keys (LRU first)
        self.min_freq = 0

    def _touch(self, key: int) -> None:
        f = self.freq[key]
        del self.buckets[f][key]
        if not self.buckets[f]:
            del self.buckets[f]
            if self.min_freq == f:
                self.min_freq = f + 1
        self.freq[key] = f + 1
        self.buckets[f + 1][key] = None

    def get(self, key: int) -> int:
        if key not in self.vals:
            return -1
        self._touch(key)
        return self.vals[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
        if key in self.vals:
            self.vals[key] = value
            self._touch(key)
            return
        if len(self.vals) == self.capacity:
            victim, _ = self.buckets[self.min_freq].popitem(last=False)
            if not self.buckets[self.min_freq]:
                del self.buckets[self.min_freq]
            del self.vals[victim]
            del self.freq[victim]
        self.vals[key] = value
        self.freq[key] = 1
        self.buckets[1][key] = None
        self.min_freq = 1
```

**C++ Solution**:

```cpp
#include <list>
#include <unordered_map>
using namespace std;

class LFUCache {
    struct Entry {
        int value;
        int freq;
        list<int>::iterator pos;                      // position inside buckets[freq]
    };
    int capacity, minFreq = 0;
    unordered_map<int, Entry> entries;
    unordered_map<int, list<int>> buckets;            // freq -> keys, front = most recent

    void touch(int key, Entry& e) {
        auto bucket = buckets.find(e.freq);
        bucket->second.erase(e.pos);
        if (bucket->second.empty()) {
            buckets.erase(bucket);
            if (minFreq == e.freq) ++minFreq;
        }
        ++e.freq;
        auto& next = buckets[e.freq];
        next.push_front(key);
        e.pos = next.begin();
    }

public:
    explicit LFUCache(int cap) : capacity(cap) {}

    int get(int key) {
        auto it = entries.find(key);
        if (it == entries.end()) return -1;
        touch(key, it->second);
        return it->second.value;
    }

    void put(int key, int value) {
        if (capacity <= 0) return;
        auto it = entries.find(key);
        if (it != entries.end()) {
            it->second.value = value;
            touch(key, it->second);
            return;
        }
        if ((int)entries.size() == capacity) {
            auto bucket = buckets.find(minFreq);
            int victim = bucket->second.back();       // LRU within the min frequency
            bucket->second.pop_back();
            if (bucket->second.empty()) buckets.erase(bucket);
            entries.erase(victim);
        }
        auto& ones = buckets[1];
        ones.push_front(key);
        entries[key] = Entry{value, 1, ones.begin()};
        minFreq = 1;
    }
};
```

**Complexity**: O(1) average per operation. Space O(capacity).

---

#### Problem 3: Insert Delete GetRandom O(1) (LC 380) — Medium

**Problem**: Implement a set with `insert(val)`, `remove(val)` (each returns whether it changed the set), and `getRandom()` returning a uniformly random element, all in O(1) average.

**Link**: [https://leetcode.com/problems/insert-delete-getrandom-o1/](https://leetcode.com/problems/insert-delete-getrandom-o1/)

**Intuition**: Uniform random choice needs **contiguous indexing**, so use a dynamic array. Fast delete from an array needs **no holes**: move the last element into the deleted slot and pop the tail. A `value → index` map finds the slot and must be updated for the moved element.

**Python Solution**:

```python
import random

class RandomizedSet:
    def __init__(self):
        self.vals: list[int] = []
        self.index: dict[int, int] = {}

    def insert(self, val: int) -> bool:
        if val in self.index:
            return False
        self.index[val] = len(self.vals)
        self.vals.append(val)
        return True

    def remove(self, val: int) -> bool:
        i = self.index.pop(val, None)
        if i is None:
            return False
        last = self.vals.pop()
        if i < len(self.vals):          # val was not the last element: move `last` into slot i
            self.vals[i] = last
            self.index[last] = i
        return True

    def getRandom(self) -> int:
        return random.choice(self.vals)
```

**C++ Solution**:

```cpp
#include <random>
#include <unordered_map>
#include <vector>
using namespace std;

class RandomizedSet {
    vector<int> vals;
    unordered_map<int, int> index;
    mt19937 rng{random_device{}()};

public:
    bool insert(int val) {
        if (index.count(val)) return false;
        index[val] = vals.size();
        vals.push_back(val);
        return true;
    }

    bool remove(int val) {
        auto it = index.find(val);
        if (it == index.end()) return false;
        int i = it->second, last = vals.back();
        vals[i] = last;                 // safe even when i is the last slot
        index[last] = i;
        vals.pop_back();
        index.erase(val);               // erase AFTER updating `last` (they may be equal)
        return true;
    }

    int getRandom() {
        uniform_int_distribution<size_t> pick(0, vals.size() - 1);
        return vals[pick(rng)];
    }
};
```

**Complexity**: O(1) average for all three operations. Space O(n).

**Pitfall**: `rand() % n` is slightly biased when `RAND_MAX + 1` is not a multiple of `n`, and `RAND_MAX` can be as small as 32767. Use `<random>` with `uniform_int_distribution`.

---

#### Problem 4: Min Stack (LC 155) — Medium

**Problem**: A stack supporting `push`, `pop`, `top`, and `getMin`, all in O(1).

**Link**: [https://leetcode.com/problems/min-stack/](https://leetcode.com/problems/min-stack/)

**Intuition**: The minimum of the stack only changes at push and pop, and after a pop it reverts to the minimum *at the time of the corresponding push*. Store that minimum alongside each element.

**Python Solution**:

```python
class MinStack:
    def __init__(self):
        self.stack: list[tuple[int, int]] = []   # (value, min including this value)

    def push(self, val: int) -> None:
        current_min = min(val, self.stack[-1][1]) if self.stack else val
        self.stack.append((val, current_min))

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]
```

**C++ Solution**:

```cpp
#include <algorithm>
#include <utility>
#include <vector>
using namespace std;

class MinStack {
    vector<pair<int, int>> st;                    // (value, min so far)
public:
    void push(int val) {
        st.emplace_back(val, st.empty() ? val : min(val, st.back().second));
    }
    void pop() { st.pop_back(); }
    int top() { return st.back().first; }
    int getMin() { return st.back().second; }
};
```

**Complexity**: O(1) per operation. Space O(n).

**Space optimization**: A second stack that only receives values `<= current min` saves memory when the minimum rarely changes. Use `<=`, not `<`, so that duplicates of the minimum are popped correctly. A third variant stores `val - min` differences in one stack for O(1) extra space, but it needs 64-bit arithmetic to avoid overflow. Mention it, but do not lead with it.

---

#### Problem 5: Time Based Key-Value Store (LC 981) — Medium

**Problem**: `set(key, value, timestamp)` and `get(key, timestamp)`. `get` returns the value set with the largest `timestamp_prev <= timestamp`, or `""`. Timestamps passed to `set` are **strictly increasing**.

**Link**: [https://leetcode.com/problems/time-based-key-value-store/](https://leetcode.com/problems/time-based-key-value-store/)

**Intuition**: Because timestamps arrive in increasing order, appending to a per-key list keeps it **sorted for free**. `get` becomes "rightmost entry with time `<= t`", which is `bisect_right(t) - 1`.

**Python Solution**:

```python
import bisect
from collections import defaultdict

class TimeMap:
    def __init__(self):
        self.times: defaultdict[str, list[int]] = defaultdict(list)
        self.values: defaultdict[str, list[str]] = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.times[key].append(timestamp)       # strictly increasing -> stays sorted
        self.values[key].append(value)

    def get(self, key: str, timestamp: int) -> str:
        times = self.times.get(key)
        if not times:
            return ""
        i = bisect.bisect_right(times, timestamp) - 1
        return self.values[key][i] if i >= 0 else ""
```

**C++ Solution**:

```cpp
#include <algorithm>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>
using namespace std;

class TimeMap {
    unordered_map<string, vector<pair<int, string>>> history;
public:
    void set(string key, string value, int timestamp) {
        history[key].emplace_back(timestamp, std::move(value));
    }

    string get(string key, int timestamp) {
        auto it = history.find(key);
        if (it == history.end()) return "";
        const auto& h = it->second;
        auto pos = upper_bound(h.begin(), h.end(), timestamp,
                               [](int t, const pair<int, string>& p) { return t < p.first; });
        return pos == h.begin() ? "" : prev(pos)->second;
    }
};
```

**Complexity**: `set` O(1) amortized. `get` O(log m), where m is the number of versions for that key. Space O(total sets).

**Follow-up**: If timestamps can arrive out of order, use a per-key `std::map<int, string>` (`upper_bound` then step back) or `bisect.insort` (O(m) insert). This is the core of MVCC storage, where reads at snapshot timestamp T see the latest version `<= T`.

---

#### Problem 6: Snapshot Array (LC 1146) — Medium

**Problem**: `SnapshotArray(length)` starts as all zeros. Support `set(index, val)`, `snap()` (returns `snap_id`, starting at 0, then increments), and `get(index, snap_id)`.

**Link**: [https://leetcode.com/problems/snapshot-array/](https://leetcode.com/problems/snapshot-array/)

**Intuition**: Copying the whole array on every `snap` costs O(length) per snap. Instead, store **per-index change history** as `(snap_id, value)` pairs. Multiple sets within the same snapshot overwrite the last pair. `get` binary-searches for the last pair with `snap_id' <= snap_id`.

**Python Solution**:

```python
import bisect

class SnapshotArray:
    def __init__(self, length: int):
        self.history = [[(0, 0)] for _ in range(length)]   # (snap_id, value)
        self.snap_id = 0

    def set(self, index: int, val: int) -> None:
        h = self.history[index]
        if h[-1][0] == self.snap_id:
            h[-1] = (self.snap_id, val)                    # overwrite within the same snapshot
        else:
            h.append((self.snap_id, val))

    def snap(self) -> int:
        self.snap_id += 1
        return self.snap_id - 1

    def get(self, index: int, snap_id: int) -> int:
        h = self.history[index]
        # (snap_id, inf) sorts after every (snap_id, value): rightmost entry with id <= snap_id
        i = bisect.bisect_right(h, (snap_id, float("inf"))) - 1
        return h[i][1]
```

**C++ Solution**:

```cpp
#include <algorithm>
#include <iterator>
#include <utility>
#include <vector>
using namespace std;

class SnapshotArray {
    vector<vector<pair<int, int>>> history;     // per index: (snap_id, value)
    int snapId = 0;
public:
    explicit SnapshotArray(int length) : history(length, vector<pair<int, int>>{{0, 0}}) {}

    void set(int index, int val) {
        auto& h = history[index];
        if (h.back().first == snapId) h.back().second = val;
        else h.emplace_back(snapId, val);
    }

    int snap() { return snapId++; }

    int get(int index, int snap_id) {
        const auto& h = history[index];
        auto pos = upper_bound(h.begin(), h.end(), snap_id,
                               [](int s, const pair<int, int>& p) { return s < p.first; });
        return prev(pos)->second;               // h[0] has snap 0 <= snap_id, so pos != begin
    }
};
```

**Complexity**: `set` O(1), `snap` O(1), `get` O(log k), where k is the number of changes at that index. Space O(length + sets).

**Systems analogy**: This is copy-on-write versioning. Filesystem snapshots (ZFS, btrfs) and MVCC databases keep only the changed blocks or rows per version instead of full copies.

---

#### Problem 7: Design Hit Counter (LC 362) — Medium

**Problem**: `hit(timestamp)` records a hit. `getHits(timestamp)` returns the number of hits in the past 300 seconds, i.e. in `(timestamp - 300, timestamp]`. Timestamps are in seconds and non-decreasing. Follow-up: what if there are very many hits per second?

**Link**: [https://leetcode.com/problems/design-hit-counter/](https://leetcode.com/problems/design-hit-counter/)

**Intuition**: A deque of raw timestamps uses O(hits in window) memory, which is bad for the follow-up. Use a **ring buffer of 300 one-second buckets** instead. Bucket `t % 300` stores `(time, count)`. If the stored time is stale (not equal to `t`), reset the bucket. `getHits` sums the buckets whose time is still within the window. Memory is O(300) regardless of traffic.

**Python Solution**:

```python
class HitCounter:
    WINDOW = 300

    def __init__(self):
        self.times = [0] * self.WINDOW
        self.counts = [0] * self.WINDOW

    def hit(self, timestamp: int) -> None:
        b = timestamp % self.WINDOW
        if self.times[b] != timestamp:      # bucket holds an old second: recycle it
            self.times[b] = timestamp
            self.counts[b] = 0
        self.counts[b] += 1

    def getHits(self, timestamp: int) -> int:
        return sum(c for t, c in zip(self.times, self.counts)
                   if timestamp - t < self.WINDOW)
```

**C++ Solution**:

```cpp
#include <array>
using namespace std;

class HitCounter {
    static constexpr int WINDOW = 300;
    array<int, WINDOW> times{};
    array<int, WINDOW> counts{};
public:
    void hit(int timestamp) {
        int b = timestamp % WINDOW;
        if (times[b] != timestamp) { times[b] = timestamp; counts[b] = 0; }
        ++counts[b];
    }

    int getHits(int timestamp) {
        int total = 0;
        for (int i = 0; i < WINDOW; ++i)
            if (timestamp - times[i] < WINDOW) total += counts[i];
        return total;
    }
};
```

**Complexity**: `hit` O(1). `getHits` O(W) with W = 300, independent of the number of hits. Space O(W). The deque alternative has O(1) amortized `hit` and O(expired) `getHits`, but O(hits) memory. A deque of `(second, count)` pairs combines the two benefits.

---

#### Problem 8: Flatten Nested List Iterator (LC 341) — Medium

**Problem**: Given a nested list of integers (each element is an integer or a list), implement an iterator with `next()` and `hasNext()` that yields the integers in order: `[[1,1],2,[1,1]] → 1,1,2,1,1`.

**Link**: [https://leetcode.com/problems/flatten-nested-list-iterator/](https://leetcode.com/problems/flatten-nested-list-iterator/)

**Intuition**: Eager flattening in the constructor works, but it uses O(N) memory and does all the work up front. The **lazy** version keeps an explicit stack of positions (the DFS state) and, in `hasNext()`, expands lists until an integer is on top. Empty lists like `[[]]` are why `hasNext()` must loop, and doing the expansion there keeps it idempotent.

**Python Solution** (includes a minimal stand-in for LeetCode's `NestedInteger` interface so the code runs):

```python
class NestedInteger:
    """Minimal stand-in for LeetCode's interface."""

    def __init__(self, value):
        self._value = value if isinstance(value, int) else [
            v if isinstance(v, NestedInteger) else NestedInteger(v) for v in value]

    def isInteger(self) -> bool:
        return isinstance(self._value, int)

    def getInteger(self) -> int:
        return self._value

    def getList(self) -> list["NestedInteger"]:
        return self._value


class NestedIterator:
    def __init__(self, nestedList: list[NestedInteger]):
        self.stack = [(nestedList, 0)]                 # (list, next index) = DFS frames

    def hasNext(self) -> bool:
        while self.stack:
            lst, i = self.stack[-1]
            if i == len(lst):
                self.stack.pop()
                continue
            if lst[i].isInteger():
                return True
            self.stack[-1] = (lst, i + 1)              # step past the sub-list...
            self.stack.append((lst[i].getList(), 0))   # ...and descend into it
        return False

    def next(self) -> int:
        self.hasNext()                                 # ensure an integer is on top
        lst, i = self.stack[-1]
        self.stack[-1] = (lst, i + 1)
        return lst[i].getInteger()


it = NestedIterator(NestedInteger([[1, 1], 2, [[]], [1, [1]]]).getList())
out = []
while it.hasNext():
    out.append(it.next())
assert out == [1, 1, 2, 1, 1]
```

**C++ Solution** (with a minimal `NestedInteger` stand-in):

```cpp
#include <utility>
#include <vector>
using namespace std;

// Minimal stand-in for LeetCode's NestedInteger interface.
class NestedInteger {
    bool isInt_;
    int value_ = 0;
    vector<NestedInteger> list_;
public:
    NestedInteger(int v) : isInt_(true), value_(v) {}
    NestedInteger(vector<NestedInteger> l) : isInt_(false), list_(std::move(l)) {}
    bool isInteger() const { return isInt_; }
    int getInteger() const { return value_; }
    const vector<NestedInteger>& getList() const { return list_; }
};

class NestedIterator {
    using It = vector<NestedInteger>::const_iterator;
    vector<pair<It, It>> stack;                        // (current, end) per nesting level
public:
    NestedIterator(vector<NestedInteger>& nestedList) {
        stack.emplace_back(nestedList.cbegin(), nestedList.cend());
    }

    bool hasNext() {
        while (!stack.empty()) {
            auto& [cur, end] = stack.back();
            if (cur == end) { stack.pop_back(); continue; }
            if (cur->isInteger()) return true;
            const auto& inner = cur->getList();
            ++cur;                                     // step past the sub-list first...
            stack.emplace_back(inner.cbegin(), inner.cend());  // ...(this may reallocate)
        }
        return false;
    }

    int next() {
        hasNext();
        return (stack.back().first++)->getInteger();
    }
};
```

**Complexity**: O(1) amortized per `next`/`hasNext` (each element is pushed and popped once). Space O(depth), compared with O(N) for eager flattening.

**Pitfall (C++)**: `auto& [cur, end] = stack.back()` is a reference into the vector. After `emplace_back` reallocates, it dangles. The code above increments `cur` *before* the `emplace_back` and does not touch the reference afterwards.

---

#### Problem 9: Binary Search Tree Iterator (LC 173) — Medium

**Problem**: Implement an iterator over a BST's in-order sequence with `next()` and `hasNext()` in O(1) **amortized** time and **O(h)** memory.

**Link**: [https://leetcode.com/problems/binary-search-tree-iterator/](https://leetcode.com/problems/binary-search-tree-iterator/)

**Intuition**: This is iterative in-order traversal paused between steps. The stack holds the "left spine" of nodes whose left subtrees are fully explored but which have not been emitted. `next()` pops the top (the smallest remaining), then pushes the left spine of its right child. Each node is pushed and popped once, so n calls cost O(n) total.

**Python Solution**:

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

class BSTIterator:
    def __init__(self, root: TreeNode | None):
        self.stack: list[TreeNode] = []
        self._push_left(root)

    def _push_left(self, node: TreeNode | None) -> None:
        while node:
            self.stack.append(node)
            node = node.left

    def next(self) -> int:
        node = self.stack.pop()
        self._push_left(node.right)
        return node.val

    def hasNext(self) -> bool:
        return bool(self.stack)


root = TreeNode(7, TreeNode(3), TreeNode(15, TreeNode(9), TreeNode(20)))
it = BSTIterator(root)
assert [it.next() for _ in range(5)] == [3, 7, 9, 15, 20] and not it.hasNext()
```

**C++ Solution**:

```cpp
#include <stack>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

class BSTIterator {
    stack<TreeNode*> st;
    void pushLeft(TreeNode* node) {
        for (; node; node = node->left) st.push(node);
    }
public:
    explicit BSTIterator(TreeNode* root) { pushLeft(root); }

    int next() {
        TreeNode* node = st.top();
        st.pop();
        pushLeft(node->right);
        return node->val;
    }

    bool hasNext() { return !st.empty(); }
};
```

**Complexity**: `next` is O(1) amortized and O(h) worst case for a single call. `hasNext` is O(1). Space O(h).

**Follow-ups**: For a reverse iterator, mirror left and right. For **Two Sum IV on a BST** in O(h) space, run a forward and a backward iterator as two pointers. To achieve O(1) space, use Morris traversal, which temporarily threads right pointers but mutates the tree while iterating.

### Interview Q&A

**Q1.** Make the LRU cache thread-safe. What are the options and their costs?

(a) **One mutex around `get` and `put`.** This is correct and simple. Note that `get` *mutates* the recency list, so a reader–writer lock does not help: every operation is a writer. Under contention this lock serializes all threads. (b) **Sharding**: N independent LRU caches selected by `hash(key) % N`, each with its own lock. Contention drops roughly N-fold, and eviction becomes per-shard, which is approximately global LRU. This is what most in-process caches do. (c) **Defer recency updates**: record hits in a lock-free per-thread buffer and apply them to the list in batches under the lock (Caffeine's approach in Java). (d) **Approximate LRU**: the CLOCK algorithm keeps a reference bit per entry, so hits only set a bit with no list manipulation. Redis evicts by sampling a few keys and evicting the oldest among them. See [Concurrency Coding Problems](Concurrency_Coding_Problems.md).

**Q2.** Where does LRU fall short, and what do real systems use instead?

LRU is vulnerable to **scans**: one sequential pass over a large dataset evicts the entire working set. LFU resists scans but suffers from **stale popularity**, since items that were hot long ago never leave unless counts decay. Real systems use hybrids. The Linux page cache keeps active and inactive lists, so a page must be touched twice to be promoted (and newer kernels offer multi-generational LRU). Databases use LRU-K or 2Q-style policies. ARC adapts between recency and frequency. Caffeine uses W-TinyLFU, an admission filter backed by a Count-Min sketch. CPU caches use pseudo-LRU (tree bits) because true LRU state is too expensive in hardware at high associativity.

**Q3.** Why must the LRU list be doubly linked, and why use sentinel nodes?

Removing an arbitrary node in O(1) means updating its predecessor's `next` pointer. A singly linked list would need an O(n) search to find the predecessor. (There is a trick of storing a pointer to the *predecessor* in the map, but it needs fixups on every move and is error-prone.) Sentinels (dummy head and tail) guarantee that every real node has non-null neighbours, which removes four or five `if` branches from `_unlink` and `_push_front`. Those branches are where most bugs live.

**Q4.** Add TTL expiry to the LRU cache. How do you expire efficiently?

Store `expires_at` in each node. **Lazy expiry**: on `get`, if the node has expired, delete it and return a miss. This is O(1) but leaves dead entries using memory until they are touched or evicted. **Active expiry**: keep a min-heap (or timer wheel) keyed by `expires_at` and remove expired entries on each operation or from a background sweeper. Heap entries for keys that were since updated are handled with lazy deletion: check that the heap entry's version matches the node. Redis combines lazy expiry with periodic random sampling of keys that have TTLs.

**Q5.** Insert Delete GetRandom with duplicates allowed (LC 381): what changes?

Map each value to a **set of indices** instead of one index. `remove(val)` picks any index `i` from `index[val]`, moves `last = vals[-1]` into slot `i`, and updates `index[last]` by removing `len - 1` and adding `i`. The order of these updates matters when `last == val`: update the `last` mapping first, then remove `i` from `val`'s set, and handle `i == len - 1` without re-adding it. `getRandom` still picks a uniform index, so each value is returned with probability proportional to its multiplicity, which is what the problem asks for.

**Q6.** How would the hit counter work across many servers at very high QPS?

Each server keeps local per-second buckets using **atomic counters** (no lock on the hot path). A bucket is reset with a compare-and-swap on its timestamp. An aggregator periodically pulls the bucket arrays, or the servers push them, and sums them. That tolerates a few seconds of staleness in exchange for no cross-server coordination per hit. For exact global counts, partition by key to a single owner. For approximate counts with bounded memory over many keys, use a Count-Min sketch per time bucket. Out-of-order timestamps within the window are fine with buckets: add to `bucket[t % W]` if `t` is still within the window, and otherwise drop or account for the late hit separately.

---

## 27. Weighted Shortest Path Patterns

### Overview

Plain BFS finds shortest paths only when every edge costs the same. Once edges carry **weights**, a **hop limit**, or the "position" includes extra **state** (keys collected, obstacles removed, nodes visited), you need a variant. The algorithms themselves (Dijkstra, Bellman-Ford, Floyd-Warshall, A*) are derived in [DSA Fundamentals: Shortest Path Algorithms](DSA_Fundamentals.md#17-shortest-path-algorithms). This section is about **recognising which variant an interview problem wants** and writing it without bugs.

| Edge weights / constraint | Algorithm | Time | Why this one |
|---|---|---|---|
| All equal (unweighted) | BFS | O(V + E) | FIFO order = distance order |
| Only 0 and 1 | **0-1 BFS** (deque) | O(V + E) | Push 0-edges to the front, 1-edges to the back; deque stays sorted |
| Non-negative | **Dijkstra** (binary heap) | O((V + E) log V) | Greedy: the smallest tentative distance is final |
| Path cost = max (or min) edge on the path | Dijkstra with `max` instead of `+` | O(E log V) | Cost is still monotone along a path |
| Negative edges, or "at most K edges/stops" | **Bellman-Ford** (K rounds) | O(K · E) | Round `i` = best paths with at most `i` edges |
| Small V, all pairs | Floyd-Warshall | O(V^3) | Three loops, handles negatives |
| Position + extra state, unit steps | **BFS over (node, state)** | O(states · transitions) | Turn the state into part of the vertex |

**Worked trace (Dijkstra with lazy deletion)**: edges `A→B 4`, `A→C 1`, `C→B 2`, `B→D 1`, source `A`.

| Pop | dist after relaxing | Heap after step |
|---|---|---|
| — | A=0, B=∞, C=∞, D=∞ | (0,A) |
| (0,A) | B=4, C=1 | (1,C) (4,B) |
| (1,C) | B=3 (improved via C) | (3,B) (4,B) |
| (3,B) | D=4 | (4,B) (4,D) |
| (4,B) | stale: 4 > dist[B]=3, skip | (4,D) |
| (4,D) | — | empty |

The stale `(4,B)` entry is the price of **lazy deletion**: instead of a decrease-key operation (which `heapq` and `std::priority_queue` do not offer), push a new entry and skip outdated ones on pop.

### When to Use

- "Minimum time / cost / delay from a source" with **weighted** edges → Dijkstra
- "Minimize the **maximum** step / effort / height on the path" → Dijkstra with `max`, or binary search on the answer + BFS, or Union-Find over sorted edges
- "At most **K** stops / edges / transfers" → Bellman-Ford with K+1 rounds, or BFS over `(node, stops)`
- Grid where some moves are **free** and others cost 1 (follow the arrow vs change it, walk vs break a wall) → 0-1 BFS
- "Visit **all** nodes / collect all keys / with up to **k** eliminations" → BFS on `(position, extra state)`
- Small `n` (≤ 12–20) together with a "visit all" requirement → the state is a bitmask

### Template Code

**Dijkstra (lazy deletion)**

```python
# Python — Dijkstra with a binary heap
import heapq

def dijkstra(adj: list[list[tuple[int, int]]], src: int) -> list[float]:
    """adj[u] = [(v, w), ...] with w >= 0. Returns dist[] (inf = unreachable)."""
    dist = [float('inf')] * len(adj)
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:                  # stale entry: u was already settled cheaper
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist

adj = [[(1, 4), (2, 1)], [(3, 1)], [(1, 2)], []]   # the trace above: A=0, B=1, C=2, D=3
assert dijkstra(adj, 0) == [0, 3, 1, 4]
```

```cpp
// C++ — Dijkstra with a binary heap
#include <functional>
#include <limits>
#include <queue>
#include <utility>
#include <vector>
using namespace std;

vector<long long> dijkstra(const vector<vector<pair<int, int>>>& adj, int src) {
    const long long INF = numeric_limits<long long>::max();
    vector<long long> dist(adj.size(), INF);
    using State = pair<long long, int>;                        // (dist, node)
    priority_queue<State, vector<State>, greater<State>> pq;   // min-heap
    dist[src] = 0;
    pq.push({0, src});
    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d > dist[u]) continue;                             // stale entry
        for (auto [v, w] : adj[u]) {
            if (d + w < dist[v]) {
                dist[v] = d + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}
```

**0-1 BFS**

```python
# Python — 0-1 BFS: weights are 0 or 1
from collections import deque

def zero_one_bfs(adj: list[list[tuple[int, int]]], src: int) -> list[float]:
    dist = [float('inf')] * len(adj)
    dist[src] = 0
    dq = deque([src])
    while dq:
        u = dq.popleft()
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                if w == 0:
                    dq.appendleft(v)     # same distance as u: process next
                else:
                    dq.append(v)         # distance + 1: process after this layer
    return dist

assert zero_one_bfs([[(1, 1), (2, 0)], [], [(1, 0)]], 0) == [0, 0, 0]
```

**Bellman-Ford limited to K edges**

```python
# Python — best cost using at most max_edges edges
def bellman_ford_k(n: int, edges: list[tuple[int, int, int]], src: int, max_edges: int) -> list[float]:
    dist = [float('inf')] * n
    dist[src] = 0
    for _ in range(max_edges):
        nxt = dist[:]                    # COPY: each round may extend a path by one edge only
        for u, v, w in edges:
            if dist[u] + w < nxt[v]:
                nxt[v] = dist[u] + w
        dist = nxt
    return dist

assert bellman_ford_k(3, [(0, 1, 1), (1, 2, 1), (0, 2, 5)], 0, 1) == [0, 1, 5]
assert bellman_ford_k(3, [(0, 1, 1), (1, 2, 1), (0, 2, 5)], 0, 2) == [0, 1, 2]
```

**BFS over an augmented state**

```python
# Python — state-space BFS skeleton
from collections import deque

def state_bfs(start, is_goal, neighbors) -> int:
    """start: hashable state such as (r, c, keys_mask); neighbors(state) yields next states."""
    seen = {start}
    q = deque([start])
    steps = 0
    while q:
        for _ in range(len(q)):          # one BFS layer = one step
            s = q.popleft()
            if is_goal(s):
                return steps
            for t in neighbors(s):
                if t not in seen:
                    seen.add(t)
                    q.append(t)
        steps += 1
    return -1

assert state_bfs(0, lambda s: s == 5, lambda s: (s + 1, s + 2)) == 3
```

### Variations

| Variation | Key change | Example Problems |
|---|---|---|
| **Single-source, non-negative** | Standard Dijkstra | Network Delay Time (LC 743), Path with Maximum Probability (LC 1514, multiply and use a max-heap) |
| **Bottleneck (minimax) path** | Combine with `max(cost, edge)` | Path With Minimum Effort (LC 1631), Swim in Rising Water (LC 778) |
| **Hop-limited** | Bellman-Ford K+1 rounds, or Dijkstra/BFS on `(node, hops)` | Cheapest Flights Within K Stops (LC 787) |
| **0/1 weights** | Deque instead of heap | Minimum Cost to Make at Least One Valid Path (LC 1368), Minimum Obstacle Removal to Reach Corner (LC 2290) |
| **Bitmask state** | Vertex = `(node, visited_mask)` | Shortest Path Visiting All Nodes (LC 847), Shortest Path to Get All Keys (LC 864) |
| **Resource state** | Vertex = `(cell, remaining_budget)` with dominance pruning | Shortest Path in a Grid with Obstacles Elimination (LC 1293) |
| **Count shortest paths** | Keep `ways[v]`; reset on strict improvement, add on tie | Number of Ways to Arrive at Destination (LC 1976) |
| **Multi-source** | Seed the heap/queue with all sources at distance 0 | Walls and Gates (LC 286), As Far from Land as Possible (LC 1162) |
| **Second-best / k-th path** | Allow each node to be popped up to k times | Second Minimum Time to Reach Destination (LC 2045) |

### Common Mistakes

1. **Running Dijkstra with negative edges.** A settled node can later be improved through a negative edge, so the greedy "pop = final" assumption breaks. Use Bellman-Ford.
2. **Forgetting the stale check** (`if d > dist[u]: continue`). The answer stays correct, but each stale pop re-relaxes all of `u`'s edges, which can blow up to O(E^2) work on dense graphs.
3. **Relaxing in place during hop-limited Bellman-Ford.** Without the copy, one round can chain several edges and silently exceed K stops.
4. **Pruning `(node, stops)` states by cost alone.** In LC 787, a cheaper path that used more stops does not dominate a costlier path with fewer stops.
5. **Marking visited on pop in plain BFS but on push in Dijkstra (or vice versa).** BFS marks on push. Dijkstra marks (or checks staleness) on pop, because a node's first push may not carry its best distance.
6. **`int` overflow** when `dist[u] + w` uses an `INT_MAX` sentinel. Guard with `dist[u] != INF` or use `long long`.
7. **Forgetting 1-indexed nodes** (LC 743 uses `1..n`).
8. **State explosion.** Estimate `#states = positions × state values` before coding: 40 × 40 grid × 2^6 key masks = 102,400 states is fine; 2^20 masks × 400 cells is not.

### Related Patterns

- **BFS** ([Pattern 7](#7-bfs-breadth-first-search)) — the unweighted special case; state-space BFS is BFS on a bigger graph
- **Binary Search on the Answer** ([Pattern 28](#28-binary-search-on-the-answer)) — minimax problems can also be solved as "is there a path using only edges ≤ X?"
- **Union Find** ([Pattern 16](#16-union-find-disjoint-set)) — Swim in Rising Water and Path With Minimum Effort via Kruskal-style edge sorting
- **Bitmask DP** ([Pattern 18](#18-dynamic-programming)) — Shortest Path Visiting All Nodes is TSP on an unweighted graph
- **Bidirectional BFS** ([Pattern 33](#33-meet-in-the-middle--bidirectional-bfs)) — halves the search depth when both endpoints are known
- **See also:** [Dijkstra](DSA_Fundamentals.md#dijkstras-algorithm) and [Bellman-Ford](DSA_Fundamentals.md#bellman-ford-algorithm) theory and proofs; [Coding Problem List: shortest paths](../practice/Coding_Problem_List.md#4-bonus-lists-concurrency-strings-shortest-paths)

### Example Problems

#### Problem 1: Network Delay Time (LC 743) — Medium

**Problem**: `times[i] = (u, v, w)` is a directed edge taking `w` time. A signal starts at node `k` (nodes are `1..n`). Return the time for all nodes to receive it, or `-1` if some node is unreachable.

**Link**: [https://leetcode.com/problems/network-delay-time/](https://leetcode.com/problems/network-delay-time/)

**Intuition**: Every node receives the signal at its shortest-path distance from `k`, so the answer is the maximum distance. Weights are non-negative, so use Dijkstra. This version uses the "finalize on first pop" style: the first time a node leaves the heap, its distance is final, so it can be stored in a `dist` map and ignored afterwards.

**Python Solution**:

```python
import heapq
from collections import defaultdict

class Solution:
    def networkDelayTime(self, times: list[list[int]], n: int, k: int) -> int:
        adj = defaultdict(list)
        for u, v, w in times:
            adj[u].append((v, w))
        dist: dict[int, int] = {}
        pq = [(0, k)]
        while pq:
            d, u = heapq.heappop(pq)
            if u in dist:                     # already finalized with a smaller d
                continue
            dist[u] = d
            for v, w in adj[u]:
                if v not in dist:
                    heapq.heappush(pq, (d + w, v))
        return max(dist.values()) if len(dist) == n else -1
```

**C++ Solution**:

```cpp
#include <algorithm>
#include <climits>
#include <functional>
#include <queue>
#include <utility>
#include <vector>
using namespace std;

class Solution {
public:
    int networkDelayTime(vector<vector<int>>& times, int n, int k) {
        vector<vector<pair<int, int>>> adj(n + 1);
        for (const auto& t : times) adj[t[0]].push_back({t[1], t[2]});
        vector<int> dist(n + 1, INT_MAX);
        using State = pair<int, int>;                            // (dist, node)
        priority_queue<State, vector<State>, greater<State>> pq;
        dist[k] = 0;
        pq.push({0, k});
        while (!pq.empty()) {
            auto [d, u] = pq.top();
            pq.pop();
            if (d > dist[u]) continue;                           // stale entry
            for (auto [v, w] : adj[u]) {
                if (d + w < dist[v]) {
                    dist[v] = d + w;
                    pq.push({dist[v], v});
                }
            }
        }
        int ans = *max_element(dist.begin() + 1, dist.end());   // skip unused index 0
        return ans == INT_MAX ? -1 : ans;
    }
};
```

**Complexity**: Time O((V + E) log E), which is O((V + E) log V) because E ≤ V^2. Space O(V + E).

**Follow-up**: "The graph is dense (E ≈ V^2)." Then the O(V^2) array-based Dijkstra (scan for the minimum unsettled node, no heap) beats the heap version's O(V^2 log V).

---

#### Problem 2: Path With Minimum Effort (LC 1631) — Medium

**Problem**: `heights` is a `rows x cols` grid. Moving between 4-neighbours costs `|h1 - h2|`, and a route's **effort** is the maximum single step on it. Return the minimum effort from top-left to bottom-right.

**Link**: [https://leetcode.com/problems/path-with-minimum-effort/](https://leetcode.com/problems/path-with-minimum-effort/)

**Intuition**: This is a **bottleneck** shortest path. Dijkstra works for any path cost that never decreases when the path is extended, and `max(cost, step)` has that property. So use Dijkstra, replacing `d + w` with `max(d, w)`. The first time the target is popped, its effort is optimal.

Two other accepted approaches are worth naming: (1) **binary search on the effort** `X` plus a BFS that only uses steps ≤ `X`, O(RC log H) ([Pattern 28](#28-binary-search-on-the-answer)); (2) **Union-Find**: sort all edges by weight and union them until the corners connect, O(RC log RC) ([Pattern 16](#16-union-find-disjoint-set), same as Swim in Rising Water).

**Python Solution**:

```python
import heapq

class Solution:
    def minimumEffortPath(self, heights: list[list[int]]) -> int:
        rows, cols = len(heights), len(heights[0])
        effort = [[float('inf')] * cols for _ in range(rows)]
        effort[0][0] = 0
        pq = [(0, 0, 0)]                                  # (effort, r, c)
        while pq:
            e, r, c = heapq.heappop(pq)
            if r == rows - 1 and c == cols - 1:
                return e
            if e > effort[r][c]:
                continue
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    ne = max(e, abs(heights[nr][nc] - heights[r][c]))
                    if ne < effort[nr][nc]:
                        effort[nr][nc] = ne
                        heapq.heappush(pq, (ne, nr, nc))
        return 0
```

**C++ Solution**:

```cpp
#include <climits>
#include <cstdlib>
#include <functional>
#include <queue>
#include <tuple>
#include <vector>
using namespace std;

class Solution {
public:
    int minimumEffortPath(vector<vector<int>>& heights) {
        int rows = heights.size(), cols = heights[0].size();
        vector<vector<int>> effort(rows, vector<int>(cols, INT_MAX));
        using State = tuple<int, int, int>;                      // (effort, r, c)
        priority_queue<State, vector<State>, greater<State>> pq;
        effort[0][0] = 0;
        pq.emplace(0, 0, 0);
        const int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
        while (!pq.empty()) {
            auto [e, r, c] = pq.top();
            pq.pop();
            if (r == rows - 1 && c == cols - 1) return e;
            if (e > effort[r][c]) continue;
            for (int d = 0; d < 4; ++d) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                int ne = max(e, abs(heights[nr][nc] - heights[r][c]));
                if (ne < effort[nr][nc]) {
                    effort[nr][nc] = ne;
                    pq.emplace(ne, nr, nc);
                }
            }
        }
        return 0;
    }
};
```

**Complexity**: Time O(RC log(RC)). Space O(RC).

---

#### Problem 3: Cheapest Flights Within K Stops (LC 787) — Medium

**Problem**: `flights[i] = (from, to, price)`. Return the cheapest price from `src` to `dst` with **at most `k` stops**, or `-1`.

**Link**: [https://leetcode.com/problems/cheapest-flights-within-k-stops/](https://leetcode.com/problems/cheapest-flights-within-k-stops/)

**Intuition**: `k` stops means at most `k + 1` edges. After round `i` of Bellman-Ford, `dist[v]` is the cheapest cost using at most `i` edges, **provided each round reads only the previous round's values**. Run `k + 1` rounds over a copy of the array.

**Why the copy matters**, on `flights = [(0,1,100), (1,2,100), (0,2,500)]`, `k = 0`: the correct answer is 500 (direct). Relaxing in place in edge order, round 1 sets `dist[1] = 100` and then, in the same round, `dist[2] = 200` via `1`. That path has one stop, which is not allowed.

**Python Solution**:

```python
class Solution:
    def findCheapestPrice(self, n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
        INF = float('inf')
        dist = [INF] * n
        dist[src] = 0
        for _ in range(k + 1):                 # k stops = k + 1 edges
            nxt = dist[:]
            for u, v, w in flights:
                if dist[u] + w < nxt[v]:
                    nxt[v] = dist[u] + w
            dist = nxt
        return -1 if dist[dst] == INF else dist[dst]
```

**C++ Solution**:

```cpp
#include <climits>
#include <vector>
using namespace std;

class Solution {
public:
    int findCheapestPrice(int n, vector<vector<int>>& flights, int src, int dst, int k) {
        const int INF = INT_MAX;
        vector<int> dist(n, INF);
        dist[src] = 0;
        for (int round = 0; round <= k; ++round) {
            vector<int> next = dist;
            for (const auto& f : flights) {
                int u = f[0], v = f[1], w = f[2];
                if (dist[u] != INF && dist[u] + w < next[v]) next[v] = dist[u] + w;
            }
            dist.swap(next);
        }
        return dist[dst] == INF ? -1 : dist[dst];
    }
};
```

**Complexity**: Time O(k · E). Space O(n).

**Alternative**: Dijkstra on states `(cost, node, stops)`. Because a cheaper arrival with more stops does not dominate a costlier one with fewer stops, prune with `best_stops[node]`: skip a popped state only if the node was already reached with **fewer or equal stops** (it was reached at lower or equal cost too, since pops are in cost order). That runs in O(E · k · log(E · k)) worst case but is usually faster in practice.

---

#### Problem 4: Minimum Cost to Make at Least One Valid Path in a Grid (LC 1368) — Hard

**Problem**: Each cell holds an arrow: 1 right, 2 left, 3 down, 4 up. Following the arrow costs 0. Changing a cell's arrow costs 1 (each cell at most once). Return the minimum cost to create a path from `(0,0)` to `(m-1,n-1)`.

**Link**: [https://leetcode.com/problems/minimum-cost-to-make-at-least-one-valid-path-in-a-grid/](https://leetcode.com/problems/minimum-cost-to-make-at-least-one-valid-path-in-a-grid/)

**Intuition**: Each cell has 4 outgoing edges: weight 0 in the arrow's direction, weight 1 otherwise. With only 0/1 weights, **0-1 BFS** gives Dijkstra's answer in O(V + E): a 0-edge keeps the same distance, so push its target to the **front**; a 1-edge goes to the **back**. The deque always holds distances `d` then `d + 1`, which is the sorted order Dijkstra's heap would give.

**Python Solution**:

```python
from collections import deque

class Solution:
    def minCost(self, grid: list[list[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]          # index i <-> arrow i + 1
        dist = [[float('inf')] * cols for _ in range(rows)]
        dist[0][0] = 0
        dq = deque([(0, 0)])
        while dq:
            r, c = dq.popleft()
            for i, (dr, dc) in enumerate(dirs):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    w = 0 if grid[r][c] == i + 1 else 1
                    if dist[r][c] + w < dist[nr][nc]:
                        dist[nr][nc] = dist[r][c] + w
                        if w == 0:
                            dq.appendleft((nr, nc))
                        else:
                            dq.append((nr, nc))
        return dist[rows - 1][cols - 1]
```

**C++ Solution**:

```cpp
#include <climits>
#include <deque>
#include <utility>
#include <vector>
using namespace std;

class Solution {
public:
    int minCost(vector<vector<int>>& grid) {
        int rows = grid.size(), cols = grid[0].size();
        const int dr[] = {0, 0, 1, -1}, dc[] = {1, -1, 0, 0};   // arrows 1..4
        vector<vector<int>> dist(rows, vector<int>(cols, INT_MAX));
        deque<pair<int, int>> dq;
        dist[0][0] = 0;
        dq.push_back({0, 0});
        while (!dq.empty()) {
            auto [r, c] = dq.front();
            dq.pop_front();
            for (int i = 0; i < 4; ++i) {
                int nr = r + dr[i], nc = c + dc[i];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                int w = (grid[r][c] == i + 1) ? 0 : 1;
                if (dist[r][c] + w < dist[nr][nc]) {
                    dist[nr][nc] = dist[r][c] + w;
                    if (w == 0) dq.push_front({nr, nc});
                    else dq.push_back({nr, nc});
                }
            }
        }
        return dist[rows - 1][cols - 1];
    }
};
```

**Complexity**: Time O(RC). A cell's tentative distance is first set to `d + 1` or `d` relative to the current front, and can then only drop from `d + 1` to `d`, so each cell is assigned at most twice and each edge is relaxed a constant number of times. Space O(RC).

---

#### Problem 5: Shortest Path Visiting All Nodes (LC 847) — Hard

**Problem**: An undirected connected graph has `n ≤ 12` nodes. Return the length of the shortest walk that visits every node. You may start and end anywhere and revisit nodes and edges.

**Link**: [https://leetcode.com/problems/shortest-path-visiting-all-nodes/](https://leetcode.com/problems/shortest-path-visiting-all-nodes/)

**Intuition**: Where you are is not enough; you also need to know **which nodes you have already seen**. Make the BFS vertex `(node, mask)`. There are `n · 2^n = 12 · 4096 = 49,152` states, and each edge costs 1, so plain BFS works. Start from every `(i, 1 << i)` at once (multi-source), because the start is free.

**Python Solution**:

```python
from collections import deque

class Solution:
    def shortestPathLength(self, graph: list[list[int]]) -> int:
        n = len(graph)
        full = (1 << n) - 1
        q = deque((i, 1 << i) for i in range(n))
        seen = {(i, 1 << i) for i in range(n)}
        steps = 0
        while q:
            for _ in range(len(q)):
                u, mask = q.popleft()
                if mask == full:
                    return steps
                for v in graph[u]:
                    nm = mask | (1 << v)
                    if (v, nm) not in seen:
                        seen.add((v, nm))
                        q.append((v, nm))
            steps += 1
        return -1
```

**C++ Solution**:

```cpp
#include <queue>
#include <utility>
#include <vector>
using namespace std;

class Solution {
public:
    int shortestPathLength(vector<vector<int>>& graph) {
        int n = graph.size(), full = (1 << n) - 1;
        vector<vector<char>> seen(n, vector<char>(1 << n, 0));
        queue<pair<int, int>> q;
        for (int i = 0; i < n; ++i) {
            q.push({i, 1 << i});
            seen[i][1 << i] = 1;
        }
        for (int steps = 0; !q.empty(); ++steps) {
            for (int sz = q.size(); sz > 0; --sz) {
                auto [u, mask] = q.front();
                q.pop();
                if (mask == full) return steps;
                for (int v : graph[u]) {
                    int nm = mask | (1 << v);
                    if (!seen[v][nm]) {
                        seen[v][nm] = 1;
                        q.push({v, nm});
                    }
                }
            }
        }
        return -1;
    }
};
```

**Complexity**: Time O(2^n · n^2) in the worst case (each of the `n · 2^n` states scans up to `n` neighbours). Space O(n · 2^n).

---

#### Problem 6: Shortest Path in a Grid with Obstacles Elimination (LC 1293) — Hard

**Problem**: `grid` is 0 (empty) / 1 (obstacle). Moving to a 4-neighbour costs one step. You may eliminate at most `k` obstacles. Return the minimum steps from top-left to bottom-right, or `-1`.

**Link**: [https://leetcode.com/problems/shortest-path-in-a-grid-with-obstacles-elimination/](https://leetcode.com/problems/shortest-path-in-a-grid-with-obstacles-elimination/)

**Intuition**: The state is `(r, c, eliminations_left)`. Two optimisations make it fast:

1. **Shortcut**: if `k ≥ rows + cols - 2`, the Manhattan path is always possible; return it.
2. **Dominance pruning**: BFS reaches states in non-decreasing step order. A state at a cell with **fewer or equal** eliminations left than an earlier visit is dominated: it has used at least as many steps and has no more budget. So store `best[r][c]` = most eliminations left on any visit, and only enqueue a strictly better one. This reduces `R · C · (k+1)` states to far fewer in practice.

**Python Solution**:

```python
from collections import deque

class Solution:
    def shortestPath(self, grid: list[list[int]], k: int) -> int:
        rows, cols = len(grid), len(grid[0])
        if k >= rows + cols - 2:
            return rows + cols - 2
        best = [[-1] * cols for _ in range(rows)]      # max eliminations left on arrival
        best[0][0] = k
        q = deque([(0, 0, k)])
        steps = 0
        while q:
            for _ in range(len(q)):
                r, c, rem = q.popleft()
                if r == rows - 1 and c == cols - 1:
                    return steps
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        nrem = rem - grid[nr][nc]      # -1 means "cannot enter"
                        if nrem > best[nr][nc]:
                            best[nr][nc] = nrem
                            q.append((nr, nc, nrem))
            steps += 1
        return -1
```

**C++ Solution**:

```cpp
#include <queue>
#include <tuple>
#include <vector>
using namespace std;

class Solution {
public:
    int shortestPath(vector<vector<int>>& grid, int k) {
        int rows = grid.size(), cols = grid[0].size();
        if (k >= rows + cols - 2) return rows + cols - 2;
        vector<vector<int>> best(rows, vector<int>(cols, -1));
        queue<tuple<int, int, int>> q;
        best[0][0] = k;
        q.emplace(0, 0, k);
        const int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
        for (int steps = 0; !q.empty(); ++steps) {
            for (int sz = q.size(); sz > 0; --sz) {
                auto [r, c, rem] = q.front();
                q.pop();
                if (r == rows - 1 && c == cols - 1) return steps;
                for (int d = 0; d < 4; ++d) {
                    int nr = r + dr[d], nc = c + dc[d];
                    if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                    int nrem = rem - grid[nr][nc];
                    if (nrem > best[nr][nc]) {
                        best[nr][nc] = nrem;
                        q.emplace(nr, nc, nrem);
                    }
                }
            }
        }
        return -1;
    }
};
```

**Complexity**: Time O(R · C · k) worst case (each cell can be improved at most `k + 1` times). Space O(R · C · k) for the queue in the worst case, O(R · C) for `best`.

### Interview Q&A

**Q1.** Why does Dijkstra fail with negative edges? Give a concrete counterexample.

Dijkstra assumes that once a node is popped with distance `d`, no later path can be cheaper, because every other path continues from a node with distance ≥ `d` and only adds non-negative weight. A negative edge breaks that. Example: `A→B 2`, `A→C 3`, `C→B -2`. Dijkstra pops `B` at 2 and finalises it, but `A→C→B` costs 1. The "finalize on first pop" version (Problem 1's Python) returns the wrong answer. The lazy re-push version happens to stay correct when there is no negative cycle, because an improved node is pushed and expanded again, but a node can be re-expanded many times, so the O(E log V) bound is lost and adversarial graphs take exponential time. Use Bellman-Ford (O(VE), detects negative cycles with one extra round), SPFA (Bellman-Ford with a queue, same worst case), or Johnson's reweighting for all-pairs on sparse graphs.

**Q2.** Lazy deletion vs decrease-key: what are the complexities, and which do you use?

With lazy deletion the heap can hold up to E entries, so each push/pop is O(log E) = O(log V) (since E ≤ V^2, log E ≤ 2 log V), giving O((V + E) log V). A binary heap with decrease-key (an indexed heap) keeps at most V entries: same asymptotics, a smaller heap, but more code. A Fibonacci heap gives O(E + V log V) in theory but has large constants and is rarely faster in practice. For dense graphs (E ≈ V^2), the array-scan version is O(V^2) and beats any heap. In interviews, use lazy deletion with the stale check and mention the others.

**Q3.** In Cheapest Flights Within K Stops, why can't you run Dijkstra on nodes alone?

Dijkstra settles a node at its globally cheapest cost, but that cheapest path may use too many stops. A more expensive path with fewer stops may be the only one that can still reach `dst` within the limit, and node-only Dijkstra would have thrown it away. The fix is to make stops part of the state, i.e. vertex = `(node, stops_used)`, or use Bellman-Ford, whose round number is exactly the hop count.

**Q4.** Prove that 0-1 BFS is correct.

Invariant: the deque, read front to back, holds nodes whose tentative distances are non-decreasing and span at most two consecutive values `d, d+1`. Popping the front gives a minimum-distance node, exactly what Dijkstra would pop. Relaxing a 0-edge produces distance `d`, which belongs at the front; relaxing a 1-edge produces `d + 1`, which belongs at the back. Both keep the invariant. Hence the pop order matches Dijkstra's, without a heap: O(V + E). A node may be pushed twice (once via a 1-edge, later improved via a 0-edge); the second, better copy is processed first, and the outdated copy just re-relaxes edges with no improvement.

**Q5.** When can Dijkstra be used with a non-additive path cost like `max`?

The algorithm needs the path cost to be **monotone**: extending a path never makes it cheaper (`cost(P + e) ≥ cost(P)`). It also needs comparisons to be consistent under extension: if `cost(P1) ≤ cost(P2)` for two paths to the same node, then `cost(P1 + e) ≤ cost(P2 + e)`. Both `+` with non-negative weights and `max` satisfy this. So do `min` with a max-heap (widest path), and multiplication of probabilities in `[0, 1]` with a max-heap (LC 1514). Subtraction or negative weights do not.

**Q6.** How do you size a state-space BFS before writing it?

Multiply the dimensions: positions × extra state values. LC 864 (Shortest Path to Get All Keys): 30 × 30 cells × 2^6 key masks = 57,600 states, each with 4 transitions, so trivial. LC 847: 12 × 4,096 = 49,152. LC 1293: 40 × 40 × 1,601 (k ≤ 1600) is about 2.6M in theory, which is why the shortcut and the dominance pruning matter. Memory: a `visited` bitset of 2.6M bits is about 320 KB; a Python `set` of tuples is roughly 100+ bytes per entry, so 2.6M tuples would take hundreds of MB. Use flat arrays indexed by `(r * C + c) * (k + 1) + rem` when the state count is large.

**Q7.** What is A*, and when is it a good choice?

A* is Dijkstra with priority `g(v) + h(v)`, where `g` is the known cost from the source and `h` is a heuristic estimate to the goal. If `h` is **admissible** (never overestimates), A* returns an optimal path. If `h` is also **consistent** (`h(u) ≤ w(u,v) + h(v)`), each node is settled at most once, like Dijkstra. On grids, Manhattan distance (4-way moves) or Chebyshev distance (8-way) are standard heuristics. With `h = 0`, A* is exactly Dijkstra. It pays off for a single source–target pair in a large, geometric space (maps, games). It gives no benefit when you need distances to all nodes.

**Q8.** How do you also count the number of shortest paths (LC 1976)?

Keep `ways[v]` next to `dist[v]`. When relaxing `u → v`: if `d + w < dist[v]`, set `dist[v] = d + w` and `ways[v] = ways[u]` (a strictly better path resets the count); if `d + w == dist[v]`, do `ways[v] += ways[u]`. Because Dijkstra pops in distance order, `ways[u]` is final when `u` is popped (skip stale pops). Take the count mod 1e9+7. Pitfall: with floating-point weights, "equal" needs a tolerance; with integers it is exact.

---

## 28. Binary Search on the Answer

### Overview

Sometimes the array is not sorted, but the **answer space is**. If you can write a predicate `feasible(x)` ("can the task be done with speed / capacity / distance `x`?") that is **monotone**, meaning once true it stays true as `x` grows, then the answer is the boundary between false and true:

```text
x:          1  2  3  4  5  6  7 ...
feasible:   F  F  F  T  T  T  T      → smallest feasible x = 4   ("first true")

x:          1  2  3  4  5  6  7 ...
feasible:   T  T  T  F  F  F  F      → largest feasible x = 3    ("last true")
```

Binary search finds the boundary with O(log(hi - lo)) calls to `feasible`. Each call is usually an O(n) greedy simulation, so the total is **O(n log V)**, where V is the size of the answer range. With V = 10^9 that is about 30 checks. The theory and a lower-bound loop are in [DSA Fundamentals: Binary Search on Answer Space](DSA_Fundamentals.md#binary-search-on-answer-space). This section adds the two templates and worked problems.

**Worked example (Koko, `piles = [3, 6, 7, 11]`, `h = 8`)**: hours needed at speed `k` is `sum(ceil(p / k))`.

| k | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| hours | 27 | 15 | 10 | 8 | 8 | 6 |
| ≤ 8? | F | F | F | **T** | T | T |

Search on `[1, 11]`: mid=6 T → hi=6; mid=3 F → lo=4; mid=5 T → hi=5; mid=4 T → hi=4; stop, answer 4.

### When to Use

- "Minimize the **maximum**…" or "maximize the **minimum**…" (load, distance, time, sum)
- "Find the **smallest** speed / capacity / time / size such that the task fits within a limit"
- The answer is a number in a known range, and checking one candidate is easy (greedy, BFS, prefix count) while constructing the optimum directly is hard
- Constraints like `n ≤ 10^5` with values up to `10^9`: O(n log V) fits; O(n · V) does not
- Real-valued answers with a tolerance ("within 10^-6") → binary search on doubles for a fixed number of iterations

### Template Code

```python
# Python — first true / last true over integers
from typing import Callable

def first_true(lo: int, hi: int, feasible: Callable[[int], bool]) -> int:
    """Smallest x in [lo, hi] with feasible(x). Requires F..F T..T and feasible(hi) == True."""
    while lo < hi:
        mid = lo + (hi - lo) // 2       # rounds down: mid < hi, so hi = mid always shrinks
        if feasible(mid):
            hi = mid                    # mid may be the answer: keep it
        else:
            lo = mid + 1                # mid is infeasible: drop it
    return lo

def last_true(lo: int, hi: int, feasible: Callable[[int], bool]) -> int:
    """Largest x in [lo, hi] with feasible(x). Requires T..T F..F and feasible(lo) == True."""
    while lo < hi:
        mid = lo + (hi - lo + 1) // 2   # rounds UP: otherwise lo = mid loops forever when hi = lo + 1
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo

assert first_true(1, 11, lambda k: sum((p + k - 1) // k for p in [3, 6, 7, 11]) <= 8) == 4
assert last_true(0, 100, lambda x: x * x <= 50) == 7
```

```cpp
// C++ — first true / last true over integers
#include <cassert>
#include <functional>

long long firstTrue(long long lo, long long hi, const std::function<bool(long long)>& feasible) {
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;          // no overflow, unlike (lo + hi) / 2
        if (feasible(mid)) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}

long long lastTrue(long long lo, long long hi, const std::function<bool(long long)>& feasible) {
    while (lo < hi) {
        long long mid = lo + (hi - lo + 1) / 2;      // round up
        if (feasible(mid)) lo = mid;
        else hi = mid - 1;
    }
    return lo;
}

int main() {
    assert(lastTrue(0, 100, [](long long x) { return x * x <= 50; }) == 7);
    assert(firstTrue(0, 100, [](long long x) { return x * x >= 50; }) == 8);
}
```

**Recipe**: (1) define what `x` means; (2) write `feasible(x)` and argue monotonicity in one sentence; (3) choose `lo` = smallest possible answer and `hi` = a value that is certainly feasible; (4) pick `first_true` or `last_true`.

### Variations

| Variation | Predicate | Bounds | Example Problems |
|---|---|---|---|
| **Min rate to finish in time** | `sum(ceil(a_i / x)) ≤ limit` | `[1, max(a)]` | Koko Eating Bananas (LC 875), Minimum Speed to Arrive on Time (LC 1870) |
| **Min capacity, contiguous groups** | greedy packing uses ≤ `limit` groups | `[max(a), sum(a)]` | Capacity To Ship Packages (LC 1011), Split Array Largest Sum (LC 410) |
| **Max of min distance** | greedy placement fits ≥ `m` items | `[1, span / (m-1)]` | Magnetic Force Between Two Balls (LC 1552), Aggressive Cows (classic) |
| **Min of max gap (real-valued)** | `sum(ceil(gap / x) - 1) ≤ k` | `[0, max gap]` | Minimize Max Distance to Gas Station (LC 774) |
| **Earliest day** | count of ready items by day `x` ≥ need | `[min(day), max(day)]` | Minimum Number of Days to Make m Bouquets (LC 1482) |
| **K-th smallest in an implicit sorted set** | `count(values ≤ x) ≥ k` | `[min, max]` | Kth Smallest in Sorted Matrix (LC 378), Kth Smallest in Multiplication Table (LC 668), Find K-th Smallest Pair Distance (LC 719) |
| **Threshold on a grid path** | BFS using only cells/edges ≤ `x` reaches the target | `[0, max]` | Path With Minimum Effort (LC 1631), Swim in Rising Water (LC 778) |
| **Fractional / ratio** | `sum(a_i - x · b_i) ≥ 0` (Dinkelbach-style) | real range | Maximum Average Subarray II (LC 644) |

### Common Mistakes

1. **Non-monotone predicate.** "Throughput at batch size `x` ≥ T" is not monotone in general; "memory at batch size `x` ≤ M" is. If you cannot state why `feasible(x) ⇒ feasible(x + 1)`, binary search is not valid.
2. **`hi` not feasible.** `first_true` returns `hi` even if `feasible(hi)` is false. Either pick a provably feasible `hi` or check the result afterwards.
3. **Infinite loop in `last_true`.** With `mid = (lo + hi) // 2` and `lo = mid`, the range `[lo, lo + 1]` never shrinks. Round up.
4. **Overflow.** `(lo + hi) / 2` overflows `int` near 2^31. In Koko, `(p + k - 1) / k` overflows `int` for `p, k ≈ 10^9`; use 64-bit. The total hours `sum(ceil(p / k))` reaches 10^13 at `k = 1`.
5. **Wrong lower bound.** For shipping, a capacity below `max(weights)` makes the greedy loop count days incorrectly (a single package never fits). Start at `max(weights)`.
6. **Floating-point loop on `hi - lo > eps`.** With large magnitudes, `eps` can be smaller than the spacing between doubles, and the loop never ends. Run a fixed number of iterations (60–100) instead.

### Related Patterns

- **Modified Binary Search** ([Pattern 11](#11-modified-binary-search)) — searching a sorted array is the special case `feasible(i) = a[i] ≥ target`
- **Greedy** ([Pattern 19](#19-greedy)) — almost every `feasible` check is a greedy simulation
- **Weighted Shortest Path** ([Pattern 27](#27-weighted-shortest-path-patterns)) — minimax path problems can be solved either way
- **Dynamic Programming** ([Pattern 18](#18-dynamic-programming)) — Split Array Largest Sum also has an O(k · n^2) DP; binary search is O(n log sum)

### Example Problems

#### Problem 1: Koko Eating Bananas (LC 875) — Medium

**Problem**: `piles[i]` bananas, `h` hours. Each hour Koko picks one pile and eats up to `k` bananas from it. Return the minimum integer `k` that finishes within `h` hours (`len(piles) ≤ h`).

**Link**: [https://leetcode.com/problems/koko-eating-bananas/](https://leetcode.com/problems/koko-eating-bananas/)

**Intuition**: Hours needed `sum(ceil(p / k))` never increases as `k` grows, so `feasible(k) = hours(k) ≤ h` is F..F T..T. `k = max(piles)` always works (one hour per pile, and `len(piles) ≤ h`).

**Python Solution**:

```python
class Solution:
    def minEatingSpeed(self, piles: list[int], h: int) -> int:
        def hours(k: int) -> int:
            return sum((p + k - 1) // k for p in piles)   # integer ceil

        lo, hi = 1, max(piles)
        while lo < hi:
            mid = (lo + hi) // 2
            if hours(mid) <= h:
                hi = mid
            else:
                lo = mid + 1
        return lo
```

**C++ Solution**:

```cpp
#include <algorithm>
#include <vector>
using namespace std;

class Solution {
public:
    int minEatingSpeed(vector<int>& piles, int h) {
        auto hours = [&](long long k) {
            long long total = 0;
            for (int p : piles) total += (p + k - 1) / k;   // 64-bit: p + k overflows int
            return total;
        };
        int lo = 1, hi = *max_element(piles.begin(), piles.end());
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (hours(mid) <= h) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }
};
```

**Complexity**: Time O(n log max(piles)) ≈ 30n. Space O(1).

---

#### Problem 2: Capacity To Ship Packages Within D Days (LC 1011) — Medium

**Problem**: Packages `weights` must ship **in order**. Each day the ship carries a contiguous run whose total is ≤ its capacity. Return the least capacity that ships everything within `days` days.

**Link**: [https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/)

**Intuition**: For a fixed capacity, **greedy packing** (fill each day until the next package would overflow) uses the fewest days: delaying a package to a later day can never reduce the count. More capacity never needs more days, so the predicate is monotone. Bounds: at least `max(weights)` (the heaviest package must fit), at most `sum(weights)` (one day).

**Python Solution**:

```python
class Solution:
    def shipWithinDays(self, weights: list[int], days: int) -> int:
        def days_needed(cap: int) -> int:
            used, load = 1, 0
            for w in weights:
                if load + w > cap:
                    used += 1
                    load = 0
                load += w
            return used

        lo, hi = max(weights), sum(weights)
        while lo < hi:
            mid = (lo + hi) // 2
            if days_needed(mid) <= days:
                hi = mid
            else:
                lo = mid + 1
        return lo
```

**C++ Solution**:

```cpp
#include <algorithm>
#include <numeric>
#include <vector>
using namespace std;

class Solution {
public:
    int shipWithinDays(vector<int>& weights, int days) {
        auto daysNeeded = [&](int cap) {
            int used = 1, load = 0;
            for (int w : weights) {
                if (load + w > cap) {
                    ++used;
                    load = 0;
                }
                load += w;
            }
            return used;
        };
        int lo = *max_element(weights.begin(), weights.end());
        int hi = accumulate(weights.begin(), weights.end(), 0);
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (daysNeeded(mid) <= days) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }
};
```

**Complexity**: Time O(n log(sum)). Space O(1). Example: `[1..10]`, `days = 5` → 15 (`[1-5] [6,7] [8] [9] [10]`).

---

#### Problem 3: Split Array Largest Sum (LC 410) — Hard

**Problem**: Split `nums` (non-negative) into `k` non-empty contiguous subarrays to minimise the largest subarray sum.

**Link**: [https://leetcode.com/problems/split-array-largest-sum/](https://leetcode.com/problems/split-array-largest-sum/)

**Intuition**: This is LC 1011 in disguise: "largest sum ≤ X" is "capacity X", and "k pieces" is "k days". One subtlety: the greedy check finds the **minimum** number of pieces `p` for cap `X`. If `p ≤ k`, you can always split some pieces further to get exactly `k` (since `n ≥ k`), and splitting never increases the largest sum. So `pieces(X) ≤ k` is the right predicate.

**Python Solution**:

```python
class Solution:
    def splitArray(self, nums: list[int], k: int) -> int:
        def pieces(cap: int) -> int:
            count, running = 1, 0
            for x in nums:
                if running + x > cap:
                    count += 1
                    running = 0
                running += x
            return count

        lo, hi = max(nums), sum(nums)
        while lo < hi:
            mid = (lo + hi) // 2
            if pieces(mid) <= k:
                hi = mid
            else:
                lo = mid + 1
        return lo
```

**C++ Solution**:

```cpp
#include <algorithm>
#include <numeric>
#include <vector>
using namespace std;

class Solution {
public:
    int splitArray(vector<int>& nums, int k) {
        auto pieces = [&](long long cap) {
            int count = 1;
            long long running = 0;
            for (int x : nums) {
                if (running + x > cap) {
                    ++count;
                    running = 0;
                }
                running += x;
            }
            return count;
        };
        long long lo = *max_element(nums.begin(), nums.end());
        long long hi = accumulate(nums.begin(), nums.end(), 0LL);
        while (lo < hi) {
            long long mid = lo + (hi - lo) / 2;
            if (pieces(mid) <= k) hi = mid;
            else lo = mid + 1;
        }
        return static_cast<int>(lo);
    }
};
```

**Complexity**: Time O(n log(sum)). Space O(1). Example: `[7,2,5,10,8]`, `k = 2` → 18 (`[7,2,5] [10,8]`).

**Follow-up**: The DP `dp[i][j] = min over p of max(dp[p][j-1], sum(p..i-1))` is O(k · n^2). Mention it, then explain why binary search wins: n = 1000, k = 50 gives 5 · 10^7 DP steps vs about 1000 · 30 = 3 · 10^4.

---

#### Problem 4: Magnetic Force Between Two Balls (LC 1552) — Medium

**Problem**: Place `m` balls at distinct `position`s to **maximise the minimum** distance between any two balls.

**Link**: [https://leetcode.com/problems/magnetic-force-between-two-balls/](https://leetcode.com/problems/magnetic-force-between-two-balls/)

**Intuition**: "Can we keep every gap ≥ `d`?" Sort, put a ball at the first position, then greedily at each next position at least `d` past the last ball. Placing as early as possible leaves the most room, so greedy maximises the count. A larger `d` is harder, so the predicate is T..T F..F: use **last true**. Upper bound: the minimum gap is at most the average gap, `span / (m - 1)`.

**Python Solution**:

```python
class Solution:
    def maxDistance(self, position: list[int], m: int) -> int:
        position.sort()

        def can_place(d: int) -> bool:
            count, last = 1, position[0]
            for p in position[1:]:
                if p - last >= d:
                    count += 1
                    last = p
                    if count == m:
                        return True
            return count >= m

        lo, hi = 1, (position[-1] - position[0]) // (m - 1)
        while lo < hi:
            mid = (lo + hi + 1) // 2           # round up for last-true
            if can_place(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo
```

**C++ Solution**:

```cpp
#include <algorithm>
#include <vector>
using namespace std;

class Solution {
public:
    int maxDistance(vector<int>& position, int m) {
        sort(position.begin(), position.end());
        auto canPlace = [&](int d) {
            int count = 1, last = position[0];
            for (size_t i = 1; i < position.size() && count < m; ++i) {
                if (position[i] - last >= d) {
                    ++count;
                    last = position[i];
                }
            }
            return count >= m;
        };
        int lo = 1, hi = (position.back() - position.front()) / (m - 1);
        while (lo < hi) {
            int mid = lo + (hi - lo + 1) / 2;
            if (canPlace(mid)) lo = mid;
            else hi = mid - 1;
        }
        return lo;
    }
};
```

**Complexity**: Time O(n log n + n log(span)). Space O(1) beyond sorting. Example: `[1,2,3,4,7]`, `m = 3` → 3 (balls at 1, 4, 7).

---

#### Problem 5: Minimize Max Distance to Gas Station (LC 774) — Hard

**Problem**: Sorted integer `stations` on a line. Add `k` new stations anywhere (real positions) to minimise the maximum distance between adjacent stations. Answers within `10^-6` are accepted.

**Link**: [https://leetcode.com/problems/minimize-max-distance-to-gas-station/](https://leetcode.com/problems/minimize-max-distance-to-gas-station/) (premium)

**Intuition**: For a target max gap `D`, a gap of length `g` needs `ceil(g / D) - 1` new stations. The total is non-increasing in `D`, so binary search **over reals**. Run a fixed 100 iterations: each halves the interval, and 100 halvings of 10^8 reach below double precision.

A greedy max-heap ("always split the currently largest gap") is O(k log n). That is fine for small `k` but too slow for k = 10^6, and it is easy to get wrong because adding a station to a gap divides it evenly into `parts + 1` pieces rather than halving it.

**Python Solution**:

```python
import math

class Solution:
    def minmaxGasDist(self, stations: list[int], k: int) -> float:
        gaps = [b - a for a, b in zip(stations, stations[1:])]

        def needed(d: float) -> int:
            return sum(math.ceil(g / d) - 1 for g in gaps)

        lo, hi = 0.0, float(max(gaps))
        for _ in range(100):
            mid = (lo + hi) / 2
            if needed(mid) <= k:
                hi = mid                 # feasible: try a smaller max gap
            else:
                lo = mid
        return hi
```

**C++ Solution**:

```cpp
#include <algorithm>
#include <cmath>
#include <vector>
using namespace std;

class Solution {
public:
    double minmaxGasDist(vector<int>& stations, int k) {
        double lo = 0, hi = 0;
        for (size_t i = 1; i < stations.size(); ++i)
            hi = max(hi, double(stations[i] - stations[i - 1]));
        for (int iter = 0; iter < 100; ++iter) {
            double mid = (lo + hi) / 2;
            long long need = 0;
            for (size_t i = 1; i < stations.size(); ++i)
                need += static_cast<long long>(ceil((stations[i] - stations[i - 1]) / mid)) - 1;
            if (need <= k) hi = mid;
            else lo = mid;
        }
        return hi;
    }
};
```

**Complexity**: Time O(100 · n). Space O(n) in Python for `gaps`, O(1) in C++. Example: `stations = [1..10]`, `k = 9` → 0.5.

### Interview Q&A

**Q1.** How do you convince an interviewer that the predicate is monotone?

Give a one-line dominance argument: any solution that works for `x` also works for `x + 1`. For shipping, the same day assignment that fits capacity `x` fits `x + 1`. For Koko, `ceil(p / k)` is non-increasing in `k`. For ball placement, any placement whose minimum gap is ≥ `d + 1` also has minimum gap ≥ `d`. If there is no such argument (for example, "throughput at batch size x ≥ T", which can rise and then fall), binary search is invalid. For a unimodal function, use ternary search or golden-section search instead.

**Q2.** Walk through the loop invariant of `first_true`.

Invariant: the answer is in `[lo, hi]`. Initially true because `feasible(hi)` holds and nothing below `lo` is possible. If `feasible(mid)`, the first true is at `mid` or earlier, so `hi = mid` keeps it. If not, everything ≤ `mid` is false (monotonicity), so `lo = mid + 1` is safe. Because `mid < hi` (rounding down), the interval strictly shrinks each step, so the loop ends with `lo == hi` after ⌈log2(hi - lo + 1)⌉ iterations. For `last_true` the mirror image needs `mid > lo`, which is why it rounds up.

**Q3.** How many iterations does a real-valued search need?

Each iteration halves the interval. To go from width `W` to tolerance `ε` takes `log2(W / ε)` steps: `W = 10^8`, `ε = 10^-6` gives log2(10^14) ≈ 47. 100 iterations shrink a width of 10^8 to about 10^8 / 2^100 ≈ 8 · 10^-23, below the spacing of doubles near any answer ≥ 10^-6, so the result has converged to full double precision. Extra iterations are harmless: once `lo` and `hi` are adjacent doubles, `mid` equals one of them and nothing changes. Avoid `while hi - lo > eps`: if `eps` is smaller than the spacing between adjacent doubles near the answer (about 1.5 · 10^-8 at 10^8), the loop never terminates.

**Q4.** Why is the greedy check in Split Array Largest Sum optimal?

Exchange argument: take any valid split with all sums ≤ `cap`. Move the first boundary right as far as the greedy would (as long as the first piece stays ≤ `cap`). The rest of the array is now a suffix of what it was, so it needs no more pieces than before. Repeat for each boundary. The greedy split therefore uses the minimum number of pieces for that cap, so `pieces(cap) ≤ k` is exactly the feasibility condition.

**Q5.** Where does this pattern show up outside LeetCode?

`git bisect` is first-true binary search over commits with the predicate "this commit has the regression" (monotone if the bug, once introduced, stays). Capacity planning: "smallest number of replicas that keeps p99 latency under the SLO" when the load test is monotone in replicas. GPU work: "largest batch size that fits in device memory" (memory use is monotone in batch size), or "largest tile size whose LDS/shared-memory use fits the per-workgroup limit". In each case, the expensive step is the feasibility check, so the log-factor count of checks matters.

**Q6.** What changes if `feasible` is expensive or noisy (for example a benchmark run)?

Noise breaks monotonicity at the boundary. Mitigations: repeat each check and take the median, add a margin (search for the smallest `x` whose result is under the threshold by at least δ), or switch to a few points of exponential search followed by a coarse binary search with confidence intervals. When each check costs minutes, also consider galloping search (1, 2, 4, 8, ...) to find a feasible `hi` without guessing a huge upper bound.

---

## 29. Ordered Containers

### Overview

A hash map answers "is `x` here?" in O(1), but it cannot answer "what is the **closest** key to `x`?", "what is the **k-th smallest**?", or "what is the **min and max** of a set that changes?". A **balanced BST** container answers all of these in O(log n) while supporting inserts and deletes. Interview problems that need **sorted order under updates** ("nearest value within a window", "median of a sliding window", "booking that does not overlap its neighbours", "count of smaller elements seen so far") are ordered-container problems.

| Language | Container | Implementation | Notes |
|---|---|---|---|
| C++ | `std::set`, `std::multiset`, `std::map`, `std::multimap` | Red-black tree | Member `lower_bound`/`upper_bound` are O(log n); no O(log n) rank or k-th |
| C++ (GCC) | `__gnu_pbds::tree<..., tree_order_statistics_node_update>` | RB tree with subtree sizes | Adds `find_by_order(k)` and `order_of_key(x)` in O(log n); GCC-only |
| Python | `sortedcontainers.SortedList` / `SortedDict` | List of sorted sublists | Third-party (available on LeetCode). Documented as about O(log n) per add/remove; indexing `sl[k]` is supported |
| Python | `bisect` on a plain `list` | Array | O(log n) search but **O(n) insert/delete** (a `memmove`); fine up to about 10^4–10^5 operations |
| Java | `TreeMap`, `TreeSet` | Red-black tree | `floorKey`, `ceilingKey`, `lowerKey`, `higherKey` |

**Neighbour queries**: the four you need, in each language:

| Query | C++ `std::set<int> s` | Python `SortedList sl` |
|---|---|---|
| smallest ≥ x (ceiling) | `auto it = s.lower_bound(x); it != s.end()` | `i = sl.bisect_left(x); i < len(sl) → sl[i]` |
| smallest > x (higher) | `s.upper_bound(x)` | `sl[sl.bisect_right(x)]` |
| largest ≤ x (floor) | `it = s.upper_bound(x); it != s.begin() → *prev(it)` | `i = sl.bisect_right(x); i > 0 → sl[i - 1]` |
| largest < x (lower) | `it = s.lower_bound(x); it != s.begin() → *prev(it)` | `i = sl.bisect_left(x); i > 0 → sl[i - 1]` |
| min / max | `*s.begin()`, `*s.rbegin()` | `sl[0]`, `sl[-1]` |
| remove one copy of x (multiset) | `ms.erase(ms.find(x))` | `sl.remove(x)` |
| rank of x (# elements < x) | O(n) `distance`, or pb_ds `order_of_key` | `sl.bisect_left(x)` |
| k-th smallest | O(k) `next(begin, k)`, or pb_ds `find_by_order` | `sl[k]` |

### When to Use

- "Find a value within distance `t` of `x` among the last `k` elements" → window kept in an ordered set; query the ceiling of `x - t`
- "Median / k-th / min and max of a **sliding window** or a stream with deletions" → multiset or SortedList (or two heaps with lazy deletion)
- "Does a new interval overlap any existing one?" → predecessor and successor in an ordered map
- "For each element, how many later (or earlier) elements are smaller?" → insert as you scan and ask for the rank, or use a Fenwick tree over compressed values
- "Next free slot / smallest available id ≥ x" → ordered set of free ids
- Values up to 10^9 but you need order statistics → ordered container, or coordinate compression plus a Fenwick tree

### Template Code

```cpp
// fragment — C++ ordered-set idioms
#include <iterator>
#include <set>

std::set<int> s = {10, 20, 30};
auto it = s.lower_bound(25);                       // -> 30 (first >= 25)
if (it != s.end()) { /* successor-or-equal: *it */ }
if (it != s.begin()) { int pred = *std::prev(it); /* largest < 25: 20 */ }

std::multiset<int> ms = {5, 5, 7};
ms.erase(ms.find(5));                              // removes ONE 5 -> {5, 7}
// ms.erase(5);                                    // would remove ALL 5s

// WRONG: std::lower_bound(s.begin(), s.end(), x) is O(n) on a set
// (bidirectional iterators). Always call the member s.lower_bound(x).
```

```python
# Python — SortedList essentials (pip install sortedcontainers; preinstalled on LeetCode)
from sortedcontainers import SortedList

sl = SortedList([30, 10, 20])
sl.add(20)                                  # [10, 20, 20, 30]
assert sl.bisect_left(20) == 1              # rank of 20 = # elements < 20
assert sl.bisect_right(20) == 3
assert sl[0] == 10 and sl[-1] == 30 and sl[2] == 20   # k-th smallest by index
sl.remove(20)                               # removes ONE copy; raises ValueError if absent
assert list(sl) == [10, 20, 30]
i = sl.bisect_left(25)
assert sl[i] == 30 and sl[i - 1] == 20      # ceiling and lower of 25
```

```cpp
// C++ (GCC only) — order-statistic tree from policy-based data structures
#include <cassert>
#include <ext/pb_ds/assoc_container.hpp>
#include <ext/pb_ds/tree_policy.hpp>
#include <functional>
#include <utility>
using namespace __gnu_pbds;

// Multiset trick: store (value, unique_id) pairs so duplicates stay distinct.
using OrderedSet = tree<std::pair<int, int>, null_type, std::less<std::pair<int, int>>,
                        rb_tree_tag, tree_order_statistics_node_update>;

int main() {
    OrderedSet os;
    int id = 0;
    for (int x : {5, 1, 5, 3}) os.insert({x, id++});
    assert(os.order_of_key({5, -1}) == 2);              // # elements < 5
    assert(os.find_by_order(2)->first == 5);            // 0-based k-th smallest
    os.erase(os.lower_bound({5, -1}));                  // erase one copy of 5
    assert(os.size() == 3);
}
```

### Variations

| Variation | Structure | Example Problems |
|---|---|---|
| **Window + nearest value** | ordered set of the last k values | Contains Duplicate III (LC 220) |
| **Window order statistics** | multiset with a middle iterator, or SortedList | Sliding Window Median (LC 480), Longest Continuous Subarray With Absolute Diff ≤ Limit (LC 1438) |
| **Interval booking** | map `start → end`, check predecessor and successor | My Calendar I (LC 729), Count Integers in Intervals (LC 2276) |
| **Rank queries while scanning** | SortedList / Fenwick over compressed values / merge sort | Count of Smaller Numbers After Self (LC 315), Reverse Pairs (LC 493), Count of Range Sum (LC 327) |
| **Greedy that needs "smallest ≥ x" with deletion** | multiset | Hand of Straights (LC 846), Avoid Flood in The City (LC 1488) |
| **Ordered map as a sweep structure** | map coordinate → delta | My Calendar III (LC 732), Skyline (LC 218) |
| **Stock / leaderboard with updates** | map price → count plus hash map time → price | Stock Price Fluctuation (LC 2034) |

### Common Mistakes

1. **`multiset::erase(value)` removes every copy.** Use `erase(find(value))` to remove one.
2. **`std::lower_bound` on set iterators** compiles but runs in O(n), since it has to step through a bidirectional iterator. Use the member function.
3. **Dereferencing `end()` or `prev(begin())`.** Always check `it != s.end()` before `*it` and `it != s.begin()` before `prev(it)`.
4. **`int` overflow in `x - t` or `x + t`** (Contains Duplicate III has values near ±2^31). Use `long long`.
5. **`bisect.insort` in a loop on a Python list.** Each insert is O(n), so n = 10^5 inserts cost about 5 · 10^9 element moves in the worst case. Use `SortedList`.
6. **`SortedList.remove(x)` on a missing value** raises `ValueError`; `discard(x)` does not.
7. **Mutating a key in place.** Elements of a `std::set` are const for a reason: changing the ordering key breaks the tree invariant. Erase and re-insert.

### Related Patterns

- **Two Heaps** ([Pattern 9](#9-two-heaps)) — the heap version of Sliding Window Median needs lazy deletion; a multiset deletes directly
- **Line Sweep** ([Pattern 25](#25-line-sweep--advanced-intervals)) — My Calendar I/III are solved there with `std::map`
- **Sliding Window** ([Pattern 2](#2-sliding-window)) and **Monotonic Queue** ([Pattern 15](#15-monotonic-stack--queue)) — a deque gives O(1) window max/min; use an ordered container when you need more than min/max
- **See also:** [Balanced BSTs (AVL and Red-Black Trees)](DSA_Fundamentals.md#7-balanced-bsts-avl--red-black-trees) for how the containers stay balanced, and [Fenwick Trees](DSA_Fundamentals.md#12-fenwick-trees-binary-indexed-trees) for rank counting

### Example Problems

#### Problem 1: Contains Duplicate III (LC 220) — Hard

**Problem**: Return `true` if there are indices `i != j` with `|i - j| ≤ indexDiff` and `|nums[i] - nums[j]| ≤ valueDiff`.

**Link**: [https://leetcode.com/problems/contains-duplicate-iii/](https://leetcode.com/problems/contains-duplicate-iii/)

**Intuition**: Keep the last `indexDiff` values in an ordered set. For the new value `x`, a partner exists if the smallest value ≥ `x - valueDiff` is also ≤ `x + valueDiff`. That is one `lower_bound` per element. A plain `set` is enough: if a value repeats inside the window, its difference is 0 and we have already returned `true`.

**Python Solution**:

```python
from sortedcontainers import SortedList

class Solution:
    def containsNearbyAlmostDuplicate(self, nums: list[int], indexDiff: int, valueDiff: int) -> bool:
        window = SortedList()
        for i, x in enumerate(nums):
            j = window.bisect_left(x - valueDiff)          # ceiling of x - t
            if j < len(window) and window[j] <= x + valueDiff:
                return True
            window.add(x)
            if i >= indexDiff:
                window.remove(nums[i - indexDiff])         # keep only the last indexDiff values
        return False
```

**C++ Solution**:

```cpp
#include <set>
#include <vector>
using namespace std;

class Solution {
public:
    bool containsNearbyAlmostDuplicate(vector<int>& nums, int indexDiff, int valueDiff) {
        set<long long> window;
        for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
            long long x = nums[i];
            auto it = window.lower_bound(x - valueDiff);
            if (it != window.end() && *it <= x + valueDiff) return true;
            window.insert(x);
            if (i >= indexDiff) window.erase(nums[i - indexDiff]);
        }
        return false;
    }
};
```

**Complexity**: Time O(n log k) with `k = indexDiff`. Space O(k).

**Follow-up (O(n) buckets)**: Use buckets of width `w = valueDiff + 1`, keyed by `x // w`. Two values in the same bucket are within `valueDiff`, so each bucket holds at most one live value; otherwise we would have returned already. A partner can only be in the same bucket or the two adjacent ones.

```python
class Solution:
    def containsNearbyAlmostDuplicate(self, nums: list[int], indexDiff: int, valueDiff: int) -> bool:
        width = valueDiff + 1
        buckets: dict[int, int] = {}
        for i, x in enumerate(nums):
            b = x // width                      # floor division handles negatives correctly
            if b in buckets:
                return True
            if b - 1 in buckets and x - buckets[b - 1] <= valueDiff:
                return True
            if b + 1 in buckets and buckets[b + 1] - x <= valueDiff:
                return True
            buckets[b] = x
            if i >= indexDiff:
                del buckets[nums[i - indexDiff] // width]
        return False
```

In C++, `x / w` truncates toward zero, so `-1 / 2 == 0` puts -1 and 1 in the same bucket. Use `x >= 0 ? x / w : (x + 1) / w - 1`.

---

#### Problem 2: My Calendar I (LC 729) — Medium, revisited with SortedList

**Problem**: `book(start, end)` on half-open intervals succeeds only if it overlaps no existing booking.

**Link**: [https://leetcode.com/problems/my-calendar-i/](https://leetcode.com/problems/my-calendar-i/)

**Intuition**: The C++ `std::map` solution and the predecessor/successor argument are in [Pattern 25, Problem 4](#problem-4-my-calendar-i-lc-729-and-my-calendar-iii-lc-732). The plain-list Python version there is O(n) per booking because of `list.insert`. With `SortedList` of `(start, end)` tuples, each booking is about O(log n).

**Python Solution**:

```python
from sortedcontainers import SortedList

class MyCalendar:
    def __init__(self):
        self.booked = SortedList()                      # (start, end), pairwise disjoint

    def book(self, start: int, end: int) -> bool:
        i = self.booked.bisect_left((start, end))
        if i < len(self.booked) and self.booked[i][0] < end:   # successor overlaps
            return False
        if i > 0 and self.booked[i - 1][1] > start:            # predecessor overlaps
            return False
        self.booked.add((start, end))
        return True
```

**Complexity**: About O(log n) per `book`. Space O(n).

---

#### Problem 3: Sliding Window Median (LC 480) — Hard

**Problem**: Return the median of every window of size `k`.

**Link**: [https://leetcode.com/problems/sliding-window-median/](https://leetcode.com/problems/sliding-window-median/)

**Intuition**: The two-heap solution with lazy deletion is in [Pattern 9](#4-sliding-window-median-lc-480--hard). An ordered multiset is simpler. In Python, index the middle directly with `SortedList`. In C++, keep an iterator `mid` to element `k / 2` and nudge it by one step on each insert and erase:

- Insert `x`: if `x < *mid`, the new element lands before `mid`, so `mid` must move one step left to stay at position `k / 2`. (`multiset::insert` places equal keys after existing ones, so `x == *mid` lands after `mid`.)
- Erase `y`: if `y <= *mid`, an element at or before `mid` disappears, so move `mid` one step right **before** erasing. That also protects `mid` from being the erased node.

**Python Solution**:

```python
from sortedcontainers import SortedList

class Solution:
    def medianSlidingWindow(self, nums: list[int], k: int) -> list[float]:
        window = SortedList(nums[:k])
        medians = []
        for i in range(k, len(nums) + 1):
            medians.append((window[k // 2] + window[(k - 1) // 2]) / 2)
            if i == len(nums):
                break
            window.remove(nums[i - k])
            window.add(nums[i])
        return medians
```

**C++ Solution**:

```cpp
#include <iterator>
#include <set>
#include <vector>
using namespace std;

class Solution {
public:
    vector<double> medianSlidingWindow(vector<int>& nums, int k) {
        multiset<int> window(nums.begin(), nums.begin() + k);
        auto mid = next(window.begin(), k / 2);
        vector<double> medians;
        for (int i = k;; ++i) {
            // odd k: (mid + mid) / 2; even k: (lower middle + upper middle) / 2
            medians.push_back((static_cast<double>(*mid) + *prev(mid, 1 - k % 2)) / 2.0);
            if (i == static_cast<int>(nums.size())) return medians;
            window.insert(nums[i]);
            if (nums[i] < *mid) --mid;
            if (nums[i - k] <= *mid) ++mid;
            window.erase(window.lower_bound(nums[i - k]));
        }
    }
};
```

**Complexity**: Time O(n log k). Space O(k). The `double` cast before adding avoids `int` overflow when both middles are near 2^31.

---

#### Problem 4: Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit (LC 1438) — Medium

**Problem**: Return the length of the longest subarray in which `max - min ≤ limit`.

**Link**: [https://leetcode.com/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/](https://leetcode.com/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/)

**Intuition**: A sliding window whose validity depends on the window's min and max. A multiset gives both at its ends. (Two monotonic deques give O(n); see [Pattern 15](#15-monotonic-stack--queue). The multiset version is quicker to write correctly under pressure.)

**Python Solution**:

```python
from sortedcontainers import SortedList

class Solution:
    def longestSubarray(self, nums: list[int], limit: int) -> int:
        window = SortedList()
        left = best = 0
        for right, x in enumerate(nums):
            window.add(x)
            while window[-1] - window[0] > limit:
                window.remove(nums[left])
                left += 1
            best = max(best, right - left + 1)
        return best
```

**C++ Solution**:

```cpp
#include <algorithm>
#include <set>
#include <vector>
using namespace std;

class Solution {
public:
    int longestSubarray(vector<int>& nums, int limit) {
        multiset<int> window;
        int left = 0, best = 0;
        for (int right = 0; right < static_cast<int>(nums.size()); ++right) {
            window.insert(nums[right]);
            while (*window.rbegin() - *window.begin() > limit)
                window.erase(window.find(nums[left++]));   // erase ONE copy
            best = max(best, right - left + 1);
        }
        return best;
    }
};
```

**Complexity**: Time O(n log n). Space O(n).

---

#### Problem 5: Count of Smaller Numbers After Self (LC 315) — Hard

**Problem**: Return `counts` where `counts[i]` is the number of `j > i` with `nums[j] < nums[i]`.

**Link**: [https://leetcode.com/problems/count-of-smaller-numbers-after-self/](https://leetcode.com/problems/count-of-smaller-numbers-after-self/)

**Intuition**: Scan from the right, keeping every value seen so far in a sorted structure. For `nums[i]`, the answer is the **rank** of `nums[i]` among them (how many are strictly smaller). `SortedList.bisect_left` gives the rank directly. In C++, `std::set` has no O(log n) rank, so compress values to ranks `0..m-1` and use a **Fenwick tree** of counts: the answer is the prefix count of ranks `< rank(nums[i])`. A third option is merge sort that counts how many right-half elements jump ahead of each left-half element.

**Python Solution**:

```python
from sortedcontainers import SortedList

class Solution:
    def countSmaller(self, nums: list[int]) -> list[int]:
        seen = SortedList()
        out = []
        for x in reversed(nums):
            out.append(seen.bisect_left(x))     # # of seen values strictly less than x
            seen.add(x)
        return out[::-1]
```

**C++ Solution**:

```cpp
#include <algorithm>
#include <vector>
using namespace std;

class Solution {
    vector<int> bit;                                    // Fenwick tree, 1-indexed
    void add(int rank) {
        for (int i = rank + 1; i < static_cast<int>(bit.size()); i += i & -i) ++bit[i];
    }
    int countBelow(int rank) {                          // # inserted with rank < `rank`
        int s = 0;
        for (int i = rank; i > 0; i -= i & -i) s += bit[i];
        return s;
    }

public:
    vector<int> countSmaller(vector<int>& nums) {
        vector<int> vals(nums);
        sort(vals.begin(), vals.end());
        vals.erase(unique(vals.begin(), vals.end()), vals.end());   // coordinate compression
        bit.assign(vals.size() + 1, 0);
        vector<int> out(nums.size());
        for (int i = static_cast<int>(nums.size()) - 1; i >= 0; --i) {
            int r = lower_bound(vals.begin(), vals.end(), nums[i]) - vals.begin();
            out[i] = countBelow(r);
            add(r);
        }
        return out;
    }
};
```

**Complexity**: Time O(n log n). Space O(n). Example: `[5, 2, 6, 1]` → `[2, 1, 1, 0]`.

### Interview Q&A

**Q1.** Why are `std::set` and `std::map` red-black trees rather than AVL trees, and what does a node cost?

Red-black trees allow height up to about 2 log2(n), compared with about 1.44 log2(n) for AVL. In exchange they need at most two rotations per insert and three per delete, plus O(1) amortized recolouring. AVL can rotate O(log n) times on delete. The standard requires iterator stability and O(log n) worst case for insert and erase, and red-black trees meet both with cheaper updates. Cost: in libstdc++ each node has a 32-byte header (colour plus parent, left and right pointers on 64-bit) before the value, so a `std::set<int>` node is 40 bytes and with `malloc` overhead about 48 bytes per element, which is 12 times a `vector<int>`. Every lookup is a chain of dependent pointer loads, each a likely cache miss once the tree outgrows cache.

**Q2.** When would you use a sorted `vector` (or C++23 `std::flat_set`) instead of `std::set`?

When the data is built once and then mostly read. Binary search on a contiguous array has the same O(log n) comparisons but far fewer cache misses, uses 4 bytes per `int` instead of about 48, and iteration is a linear scan the prefetcher handles well. Inserts are O(n) element moves, which is acceptable for small `n` (a few thousand) or batch inserts (append everything, then sort once). C++23 added `std::flat_set` and `std::flat_map` (adaptors over sorted sequence containers), and Boost has had `flat_set` for years. A B-tree is the middle ground for large, mutable data.

**Q3.** Compare the three Sliding Window Median approaches.

(a) **Two heaps with lazy deletion**: O(n log n) because stale entries can pile up, more bookkeeping (balance counts that ignore pending deletions), but works in any language with a heap. (b) **Multiset with a middle iterator**: O(n log k), shortest correct C++ code, but the iterator nudging must be exactly right with duplicates. (c) **SortedList**: O(n log k) in practice, simplest code, but needs a third-party package. An O(n log k) Fenwick tree over compressed values with a "find k-th" descent is a fourth option when values are known in advance.

**Q4.** What does `multiset::insert` do with equal keys, and why does the median code depend on it?

Since C++11, `insert(value)` places the new element at the **upper bound** of the equal range, after the existing equal elements, and `insert(hint, value)` places it as close to the hint as possible. The median code relies on the first rule: inserting `x == *mid` puts it after `mid`, so `mid` does not need to move. If an implementation inserted before, the `x < *mid` test would have to become `x <= *mid`.

**Q5.** What is the iterator-invalidation story for node-based containers, and why does it matter here?

For `set`, `map`, `multiset` and `list`, insert never invalidates iterators, and erase invalidates only iterators to the erased element. That is why the median solution can keep `mid` across inserts and must move it **before** erasing the element it may point to. `vector` and `deque` have much broader invalidation: a `vector` reallocation invalidates everything.

**Q6.** How do you do rank and k-th queries in C++ without pb_ds?

(1) Coordinate-compress all values that will ever appear (offline), then use a Fenwick tree of counts: rank = prefix sum, k-th = binary-lifting descent over the tree in O(log n). (2) A segment tree over value ranks with counts supports the same plus range updates. (3) An augmented treap or RB tree that stores subtree sizes. (4) For a static array, merge sort counting or a wavelet tree. In interviews, (1) is the expected answer; mention pb_ds as a GCC-only shortcut that may not be allowed.

---

## 30. String Hashing & Matching in Practice

### Overview

Two tools cover most "substring" interview problems that brute force cannot handle:

1. **Polynomial rolling hash (Rabin-Karp)** turns any substring into a number in O(1) after O(n) preprocessing, so "have I seen this substring before?" becomes a hash-set lookup.
2. **KMP prefix function** `pi[i]` = length of the longest proper prefix of `s[0..i]` that is also a suffix of it. It gives linear-time pattern search and answers "longest prefix that is also a suffix", which is the core of several palindrome and periodicity problems.

The algorithms (with Z-function and Manacher) are derived in [DSA Fundamentals: String Algorithms](DSA_Fundamentals.md#19-string-algorithms). This section shows how they are applied.

**Rolling hash formulas** (base `B`, prime modulus `M`, prefix hashes `h`, powers `p`):

```text
h[0] = 0,  h[i+1] = (h[i] · B + s[i]) mod M,  p[i] = B^i mod M
hash(s[l:r]) = (h[r] - h[l] · p[r-l]) mod M              (half-open, O(1))
slide window of length L right by one:
    H' = (H · B - s[i] · B^L + s[i+L]) mod M
```

**How likely is a collision?** For two different strings of length `L` and a random base, the hashes collide with probability at most `(L - 1) / M`, because their difference is a non-zero polynomial in `B` of degree < L with at most L - 1 roots. Comparing many substrings is a birthday problem: `N` distinct substrings produce about `N^2 / (2M)` colliding pairs.

| Modulus | N = 10^5 substrings: expected colliding pairs | Verdict |
|---|---|---|
| 10^9 + 7 | 10^10 / (2 · 10^9) ≈ 5 | Unsafe alone: verify matches or use two moduli |
| two independent ~10^9 primes | ≈ 5 · 10^-9 | Safe |
| 2^61 - 1 (Mersenne prime) | 10^10 / 4.6 · 10^18 ≈ 2 · 10^-9 | Safe; one 128-bit multiply per step in C++ |
| 2^64 via unsigned overflow | — | **Breakable**: Thue–Morse strings collide for every base (see Q2) |

**KMP prefix function, worked example** for `s = "aabaaab"`:

| i | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| s[i] | a | a | b | a | a | a | b |
| pi[i] | 0 | 1 | 0 | 1 | 2 | 2 | 3 |

At `i = 5`, the candidate `j = pi[4] = 2` fails (`s[5] = a` vs `s[2] = b`), so fall back to `j = pi[1] = 1`, then `s[5] == s[1]` gives `pi[5] = 2`.

### When to Use

- "Find all repeated substrings of length L" / "does any substring appear twice?" → rolling hash into a set
- "**Longest** substring with property P" where P is monotone in length (if length L works, L - 1 works) → binary search on L + rolling hash check
- "First occurrence of a pattern", "count occurrences", "pattern in a stream" → KMP (or `str.find` if allowed)
- "Longest palindromic **prefix**", "shortest palindrome by adding characters in front" → KMP on `s + '#' + reverse(s)`
- "Is the string a repetition of a block?", "smallest period" → `n - pi[n-1]`
- Comparing substrings of two strings many times → prefix hashes for both, O(1) per comparison

### Template Code

```python
# Python — prefix hashes with the Mersenne prime 2^61 - 1
import random

class PrefixHash:
    MOD = (1 << 61) - 1

    def __init__(self, s: str, base: int | None = None):
        self.base = base or random.randrange(256, self.MOD - 1)   # random base defeats crafted inputs
        n = len(s)
        self.h = [0] * (n + 1)
        self.p = [1] * (n + 1)
        for i, ch in enumerate(s):
            self.h[i + 1] = (self.h[i] * self.base + ord(ch)) % self.MOD
            self.p[i + 1] = self.p[i] * self.base % self.MOD

    def get(self, l: int, r: int) -> int:
        """Hash of s[l:r] (half-open) in O(1)."""
        return (self.h[r] - self.h[l] * self.p[r - l]) % self.MOD

ph = PrefixHash("abcabc")
assert ph.get(0, 3) == ph.get(3, 6)          # "abc" == "abc"
assert ph.get(0, 2) != ph.get(1, 3)          # "ab" vs "bc" (fails with negligible probability)


def prefix_function(s: str) -> list[int]:
    """pi[i] = length of the longest proper prefix of s[:i+1] that is also its suffix."""
    pi = [0] * len(s)
    for i in range(1, len(s)):
        j = pi[i - 1]
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]                    # fall back to the next shorter border
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    return pi

assert prefix_function("aabaaab") == [0, 1, 0, 1, 2, 2, 3]
```

```cpp
// C++ — prefix function and a 2^61 - 1 multiply
#include <cassert>
#include <cstdint>
#include <string>
#include <vector>
using namespace std;

vector<int> prefixFunction(const string& s) {
    vector<int> pi(s.size(), 0);
    for (size_t i = 1; i < s.size(); ++i) {
        int j = pi[i - 1];
        while (j > 0 && s[i] != s[j]) j = pi[j - 1];
        if (s[i] == s[j]) ++j;
        pi[i] = j;
    }
    return pi;
}

constexpr uint64_t MOD61 = (1ULL << 61) - 1;

uint64_t mulmod61(uint64_t a, uint64_t b) {         // a, b < MOD61
    __uint128_t prod = static_cast<__uint128_t>(a) * b;
    uint64_t r = static_cast<uint64_t>(prod & MOD61) + static_cast<uint64_t>(prod >> 61);
    return r >= MOD61 ? r - MOD61 : r;              // 2^61 ≡ 1 (mod 2^61 - 1)
}

int main() {
    assert((prefixFunction("aabaaab") == vector<int>{0, 1, 0, 1, 2, 2, 3}));
    assert(mulmod61(MOD61 - 1, MOD61 - 1) == 1);    // (-1)(-1) = 1
}
```

### Variations

| Variation | Technique | Example Problems |
|---|---|---|
| **Fixed-length repeats** | Rolling hash or bit-packed window in a set | Repeated DNA Sequences (LC 187) |
| **Longest repeat** | Binary search on length + rolling hash | Longest Duplicate Substring (LC 1044), Longest Repeating Substring (LC 1062) |
| **Longest common substring of two strings** | Binary search on length + hash sets of both | Maximum Length of Repeated Subarray (LC 718; DP also works) |
| **Pattern search** | KMP / Z-function / `find` | Find the Index of the First Occurrence (LC 28), Repeated String Match (LC 686) |
| **Border / period** | Prefix function on `s` | Repeated Substring Pattern (LC 459), Longest Happy Prefix (LC 1392) |
| **Palindromic prefix** | Prefix function on `s + '#' + rev(s)` | Shortest Palindrome (LC 214) |
| **Count distinct substrings** | Hash all O(n^2) substrings, or suffix automaton | Distinct Echo Substrings (LC 1316) |
| **2D pattern** | Hash rows, then roll over columns | (classic contest problem) |

### Common Mistakes

1. **Negative values after subtraction.** In C++, `(h - x) % M` can be negative; add `M` before taking the modulus. Python's `%` is always non-negative for a positive modulus.
2. **Overflow in `h * B`.** With `M ≈ 10^9`, the product fits in 64 bits. With `M = 2^61 - 1` it does not; use `__uint128_t`.
3. **Single 32-bit modulus with many substrings**, which collides (see the table). Verify the actual characters on a hash match, or use two moduli.
4. **Mapping characters to 0.** If `'a' → 0`, then `"a"`, `"aa"` and `"aaa"` all hash to 0 at different lengths. Map to `1..26` or use the raw code point, and compare only same-length windows.
5. **Off-by-one in the KMP fallback.** It is `j = pi[j - 1]`, not `pi[j]`.
6. **Forgetting the separator** in `s + '#' + rev(s)`. Without it the border can extend past the original string.
7. **Saturating counters**: counting occurrences in a `uint8_t` array wraps at 256 and can report the same sequence twice.

### Related Patterns

- **Binary Search on the Answer** ([Pattern 28](#28-binary-search-on-the-answer)) — longest-repeat problems search over the length
- **Hashing & Array Classics** ([Pattern 22](#22-hashing--array-classics)) — rolling hash is a hash key you can update in O(1)
- **Trie** ([Pattern 17](#17-trie-prefix-tree)) — for many patterns at once (Aho-Corasick is a trie with KMP-style failure links)
- **Sliding Window** ([Pattern 2](#2-sliding-window)) — the fixed-length rolling hash is a fixed-size window
- **See also:** [KMP](DSA_Fundamentals.md#kmp-knuth-morris-pratt) and [Rabin-Karp](DSA_Fundamentals.md#rabin-karp-algorithm) derivations

### Example Problems

#### Problem 1: Repeated DNA Sequences (LC 187) — Medium

**Problem**: `s` contains only `A`, `C`, `G`, `T`. Return every 10-letter substring that occurs more than once.

**Link**: [https://leetcode.com/problems/repeated-dna-sequences/](https://leetcode.com/problems/repeated-dna-sequences/)

**Intuition**: Hashing all `n - 9` windows into a set works and is O(10n). The systems-flavoured version uses the 4-letter alphabet: each base is 2 bits, so a 10-letter window is a **20-bit integer**. Slide it with `code = ((code << 2) | base) & 0xFFFFF`. This is a perfect rolling hash with no collisions, and the "set" can be a flat array of 2^20 counters (1 MiB as bytes).

**Python Solution**:

```python
class Solution:
    def findRepeatedDnaSequences(self, s: str) -> list[str]:
        seen, repeated = set(), set()
        for i in range(len(s) - 9):
            seq = s[i:i + 10]
            if seq in seen:
                repeated.add(seq)
            else:
                seen.add(seq)
        return list(repeated)
```

**C++ Solution**:

```cpp
#include <cstdint>
#include <string>
#include <vector>
using namespace std;

class Solution {
public:
    vector<string> findRepeatedDnaSequences(string s) {
        auto code = [](char c) {
            switch (c) {
                case 'A': return 0;
                case 'C': return 1;
                case 'G': return 2;
                default:  return 3;   // 'T'
            }
        };
        vector<uint8_t> count(1 << 20, 0);
        vector<string> out;
        int window = 0;
        for (int i = 0; i < static_cast<int>(s.size()); ++i) {
            window = ((window << 2) | code(s[i])) & ((1 << 20) - 1);
            if (i >= 9 && count[window] < 2 && ++count[window] == 2)   // saturate at 2
                out.push_back(s.substr(i - 9, 10));
        }
        return out;
    }
};
```

**Complexity**: Python O(10n) time and space. C++ O(n) time, O(2^20) bytes of counters plus the output.

---

#### Problem 2: Find the Index of the First Occurrence in a String (LC 28) — Easy

**Problem**: Return the first index where `needle` occurs in `haystack`, or `-1`.

**Link**: [https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/)

**Intuition**: The naive scan is O(nm) on inputs like `haystack = "aaaa...ab"`, `needle = "aa...ab"`. KMP never moves backwards in `haystack`: on a mismatch it falls back in the **needle** using `pi`, reusing the characters it already matched.

**Python Solution**:

```python
class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        m = len(needle)
        pi = [0] * m
        j = 0
        for i in range(1, m):
            while j > 0 and needle[i] != needle[j]:
                j = pi[j - 1]
            if needle[i] == needle[j]:
                j += 1
            pi[i] = j
        j = 0
        for i, ch in enumerate(haystack):
            while j > 0 and ch != needle[j]:
                j = pi[j - 1]
            if ch == needle[j]:
                j += 1
            if j == m:
                return i - m + 1
        return -1
```

**C++ Solution**:

```cpp
#include <string>
#include <vector>
using namespace std;

class Solution {
public:
    int strStr(string haystack, string needle) {
        int m = needle.size();
        if (m == 0) return 0;
        vector<int> pi(m, 0);
        for (int i = 1, j = 0; i < m; ++i) {
            while (j > 0 && needle[i] != needle[j]) j = pi[j - 1];
            if (needle[i] == needle[j]) ++j;
            pi[i] = j;
        }
        for (int i = 0, j = 0; i < static_cast<int>(haystack.size()); ++i) {
            while (j > 0 && haystack[i] != needle[j]) j = pi[j - 1];
            if (haystack[i] == needle[j]) ++j;
            if (j == m) return i - m + 1;
        }
        return -1;
    }
};
```

**Complexity**: Time O(n + m). Space O(m).

---

#### Problem 3: Repeated Substring Pattern (LC 459) — Easy

**Problem**: Return `true` if `s` is some substring repeated two or more times.

**Link**: [https://leetcode.com/problems/repeated-substring-pattern/](https://leetcode.com/problems/repeated-substring-pattern/)

**Intuition**: Let `b = pi[n-1]` be the longest border. The smallest period of `s` is `p = n - b`. `s` is a whole number of copies of its first `p` characters exactly when `b > 0` and `p` divides `n`. (The well-known one-liner `s in (s + s)[1:-1]` is the same fact stated through string search.)

**Python Solution**:

```python
class Solution:
    def repeatedSubstringPattern(self, s: str) -> bool:
        n = len(s)
        pi = [0] * n
        for i in range(1, n):
            j = pi[i - 1]
            while j > 0 and s[i] != s[j]:
                j = pi[j - 1]
            if s[i] == s[j]:
                j += 1
            pi[i] = j
        border = pi[-1]
        return border > 0 and n % (n - border) == 0
```

**C++ Solution**:

```cpp
#include <string>
#include <vector>
using namespace std;

class Solution {
public:
    bool repeatedSubstringPattern(string s) {
        int n = s.size();
        vector<int> pi(n, 0);
        for (int i = 1; i < n; ++i) {
            int j = pi[i - 1];
            while (j > 0 && s[i] != s[j]) j = pi[j - 1];
            if (s[i] == s[j]) ++j;
            pi[i] = j;
        }
        int border = pi[n - 1];
        return border > 0 && n % (n - border) == 0;
    }
};
```

**Complexity**: Time O(n). Space O(n). Example: `"abcabcabc"` has border 6, period 3, and 9 % 3 == 0, so `true`. `"abcab"` has border 2, period 3, and 5 % 3 ≠ 0, so `false`.

---

#### Problem 4: Shortest Palindrome (LC 214) — Hard

**Problem**: Add characters only to the **front** of `s` to make the shortest palindrome.

**Link**: [https://leetcode.com/problems/shortest-palindrome/](https://leetcode.com/problems/shortest-palindrome/)

**Intuition**: Keep the longest palindromic **prefix** `s[:L]` and mirror the rest in front: the answer is `reverse(s[L:]) + s`. A prefix `s[:L]` is a palindrome exactly when it equals a suffix of `reverse(s)`. So the longest border of `t = s + '#' + reverse(s)` is `L`. The `#` stops the border from growing longer than `s`.

Example: `s = "aacecaaa"`, longest palindromic prefix `"aacecaa"` (L = 7), answer `"a" + "aacecaaa"` = `"aaacecaaa"`.

**Python Solution**:

```python
class Solution:
    def shortestPalindrome(self, s: str) -> str:
        t = s + "#" + s[::-1]
        pi = [0] * len(t)
        for i in range(1, len(t)):
            j = pi[i - 1]
            while j > 0 and t[i] != t[j]:
                j = pi[j - 1]
            if t[i] == t[j]:
                j += 1
            pi[i] = j
        keep = pi[-1]                       # length of the longest palindromic prefix
        return s[keep:][::-1] + s
```

**C++ Solution**:

```cpp
#include <string>
#include <vector>
using namespace std;

class Solution {
public:
    string shortestPalindrome(string s) {
        string rev(s.rbegin(), s.rend());
        string t = s + "#" + rev;
        vector<int> pi(t.size(), 0);
        for (size_t i = 1; i < t.size(); ++i) {
            int j = pi[i - 1];
            while (j > 0 && t[i] != t[j]) j = pi[j - 1];
            if (t[i] == t[j]) ++j;
            pi[i] = j;
        }
        int keep = pi.back();
        return rev.substr(0, s.size() - keep) + s;   // rev[0 : n-keep] == reverse(s[keep:])
    }
};
```

**Complexity**: Time O(n). Space O(n). The O(n^2) "try every prefix" approach times out at n = 5 · 10^4.

---

#### Problem 5: Longest Duplicate Substring (LC 1044) — Hard

**Problem**: Return any longest substring that occurs at least twice (occurrences may overlap), or `""`. `n ≤ 3 · 10^4`.

**Link**: [https://leetcode.com/problems/longest-duplicate-substring/](https://leetcode.com/problems/longest-duplicate-substring/)

**Intuition**: If some substring of length `L` repeats, so does its prefix of length `L - 1`. So "a duplicate of length L exists" is monotone (T..T F..F), and you can **binary search on L** ([Pattern 28](#28-binary-search-on-the-answer), last-true). For one `L`, roll a hash across all `n - L + 1` windows and look for a repeat: O(n). Total O(n log n). On a hash match, compare the actual characters so a collision cannot produce a wrong answer.

**Python Solution**:

```python
import random

class Solution:
    def longestDupSubstring(self, s: str) -> str:
        MOD = (1 << 61) - 1
        base = random.randrange(256, MOD - 1)
        a = [ord(c) for c in s]
        n = len(s)

        def find_dup(L: int) -> int:
            """Start index of a substring of length L that occurs twice, else -1."""
            h = 0
            for i in range(L):
                h = (h * base + a[i]) % MOD
            power = pow(base, L, MOD)                 # B^L, the weight of the outgoing char
            seen = {h: [0]}
            for i in range(1, n - L + 1):
                h = (h * base - a[i - 1] * power + a[i + L - 1]) % MOD
                for j in seen.get(h, ()):
                    if s[j:j + L] == s[i:i + L]:      # verify: rules out collisions
                        return i
                seen.setdefault(h, []).append(i)
            return -1

        lo, hi, start = 0, n - 1, 0                   # answer length in [0, n-1]
        while lo < hi:
            mid = (lo + hi + 1) // 2                  # last-true: round up
            idx = find_dup(mid)
            if idx != -1:
                lo, start = mid, idx
            else:
                hi = mid - 1
        return s[start:start + lo]
```

**C++ Solution**:

```cpp
#include <cstdint>
#include <random>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;

class Solution {
    static constexpr uint64_t MOD = (1ULL << 61) - 1;

    static uint64_t mulmod(uint64_t a, uint64_t b) {
        __uint128_t prod = static_cast<__uint128_t>(a) * b;
        uint64_t r = static_cast<uint64_t>(prod & MOD) + static_cast<uint64_t>(prod >> 61);
        return r >= MOD ? r - MOD : r;
    }

    static int findDup(const string& s, int L, uint64_t base) {
        uint64_t h = 0, power = 1;
        for (int i = 0; i < L; ++i) {
            h = (mulmod(h, base) + static_cast<unsigned char>(s[i])) % MOD;
            power = mulmod(power, base);
        }
        unordered_map<uint64_t, vector<int>> seen;
        seen[h].push_back(0);
        for (int i = 1; i + L <= static_cast<int>(s.size()); ++i) {
            uint64_t out = mulmod(static_cast<unsigned char>(s[i - 1]), power);
            h = (mulmod(h, base) + MOD - out + static_cast<unsigned char>(s[i + L - 1])) % MOD;
            auto& bucket = seen[h];
            for (int j : bucket)
                if (s.compare(j, L, s, i, L) == 0) return i;   // verify on hash match
            bucket.push_back(i);
        }
        return -1;
    }

public:
    string longestDupSubstring(string s) {
        mt19937_64 rng(random_device{}());
        uint64_t base = rng() % (MOD - 256) + 256;
        int lo = 0, hi = static_cast<int>(s.size()) - 1, start = 0;
        while (lo < hi) {
            int mid = lo + (hi - lo + 1) / 2;
            int idx = findDup(s, mid, base);
            if (idx != -1) {
                lo = mid;
                start = idx;
            } else {
                hi = mid - 1;
            }
        }
        return s.substr(start, lo);
    }
};
```

**Complexity**: Time O(n log n) expected. Space O(n). Example: `"banana"` → `"ana"`.

**Follow-up**: A **suffix array** with the LCP array solves this deterministically: the answer is the maximum LCP between adjacent suffixes in sorted order. That is O(n log n) to build (O(n) with SA-IS), but much harder to write in 45 minutes. Mention it; code the hash.

### Interview Q&A

**Q1.** Your rolling hash uses `M = 10^9 + 7`. The interviewer asks whether you can get a wrong answer.

Yes. With `N` windows the expected number of colliding pairs is about `N^2 / (2M)`. For `N = 3 · 10^4` that is about 0.45, so a collision is quite likely somewhere in a run. Three fixes: (1) **verify** on every hash hit by comparing characters, which makes the algorithm always correct, with expected O(1) extra comparisons per window; (2) **double hashing** with two independent moduli and bases (collision probability multiplies to about 10^-18 per pair); (3) one large modulus, `2^61 - 1`, with 128-bit multiplication. A **random base** chosen at runtime matters too: with a fixed, public base, an adversary can construct colliding inputs (anti-hash tests on competitive programming sites do exactly this).

**Q2.** Why not just let `uint64_t` overflow, i.e. hash mod 2^64?

Because the modulus is not prime, the "at most L - 1 roots" argument fails, and there are explicit collisions. With an even base, multiplying by the base shifts bits out of the 64-bit word, so after 64 characters the first character no longer affects the hash. With an odd base, the Thue–Morse string and its bitwise complement collide once the length is a few thousand characters, for **every** odd base, so even a random base does not help. Use a prime modulus.

**Q3.** Why is KMP O(n) even though there is a `while` loop inside the `for` loop?

Amortisation. `j` increases by at most 1 per character, so it increases at most `n` times overall. Each iteration of the inner `while` strictly decreases `j` and `j` never goes below 0, so the total number of inner iterations over the whole run is at most the total increase: ≤ n. Prefix-function construction plus the search is therefore O(n + m), with at most about 2(n + m) character comparisons.

**Q4.** KMP, Z-function, Rabin-Karp, Boyer-Moore: when would you pick each?

**KMP**: worst-case linear, streaming (never re-reads the text), also gives borders and periods. **Z-function**: same power, often easier to reason about for "match the prefix at each position" (Z of `pattern + '$' + text`). **Rabin-Karp**: many patterns of the same length at once, 2D matching, and binary search on length (LC 1044), where KMP does not apply. **Boyer-Moore(-Horspool)**: fastest in practice for long patterns over large alphabets, because it can skip ahead by up to `m` characters, which is why `grep`-style tools use variants of it. In production C++, `std::string::find` in common implementations is a simple scan (worst case O(nm)), and C++17 adds `std::boyer_moore_searcher` and `std::boyer_moore_horspool_searcher` for `std::search`.

**Q5.** How would you find the longest substring common to two strings `a` and `b`?

Binary search on the length `L`. For a candidate `L`, put every length-`L` window hash of `a` into a set, then roll over `b` and check membership (verifying on hits). O((|a| + |b|) log min(|a|, |b|)). The DP alternative `dp[i][j] = dp[i-1][j-1] + 1 if a[i-1] == b[j-1]` is O(|a| · |b|), fine for 1000 × 1000 but not 10^5 × 10^5. A generalised suffix automaton or suffix array of `a + '#' + b` gives the optimal linear or n log n solution.

**Q6.** Where do rolling hashes appear in real systems?

**Content-defined chunking** in rsync, backup and dedup systems: a rolling hash (Rabin fingerprint, Buzhash, Gear) over a small sliding window declares a chunk boundary when the hash matches a bit pattern, so inserting a byte only changes nearby chunks. **rsync's** weak rolling checksum finds matching blocks at any offset. **Plagiarism detection** (winnowing) and **genome k-mer counting** hash fixed-length windows. In profiling tools, hashing and interning repeated strings such as kernel names or call-stack frames turns string comparisons into integer comparisons when aggregating millions of samples.

---

## 31. Randomized Algorithms

### Overview

Randomized interview problems test two things: that you can produce the **exact distribution** asked for (uniform, weighted, without replacement), and that you can **prove** it in a few lines. Three building blocks cover almost all of them:

| Building block | Produces | Cost | Proof idea |
|---|---|---|---|
| **Fisher-Yates shuffle** | Uniform random permutation | O(n) time, in place | Position `i` gets each remaining element with probability `1/(i+1)`; product = `1/n!` |
| **Reservoir sampling** | Uniform k-sample from a stream of unknown length | O(n) time, O(k) space | Induction: after `t` items each is kept with probability `k/t` |
| **Prefix sums + binary search** | Weighted pick | O(n) build, O(log n) per pick | Index `i` owns an interval of `w[i]` integers out of `sum(w)` |

Two vocabulary words interviewers like: a **Las Vegas** algorithm is always correct and only its running time is random (randomized quicksort, quickselect, treaps, the verified rolling hash in [Pattern 30](#30-string-hashing--matching-in-practice)). A **Monte Carlo** algorithm has bounded running time but may be wrong with small probability (Miller-Rabin primality, Bloom filters, Count-Min sketches, an unverified hash comparison).

More theory, including randomized quickselect analysis, is in [DSA Fundamentals: Randomized Algorithms](DSA_Fundamentals.md#30-randomized-algorithms).

### When to Use

- "Return a random element / index with probability proportional to `w[i]`" → prefix sums + binary search (or the alias method for O(1) picks)
- "Each element equally likely", but the size is unknown or the data is a stream or linked list → reservoir sampling
- "Shuffle", "random permutation", "deal cards" → Fisher-Yates
- "Pick uniformly from a range with exclusions" → remap excluded values to allowed ones
- "O(1) insert, delete **and** getRandom" → array + hash map of indices (see [Design Problems, Insert Delete GetRandom](#problem-3-insert-delete-getrandom-o1-lc-380--medium))
- "Expected O(n) k-th element" → randomized quickselect ([Pattern 12](#12-top-k-elements))

### Template Code

```python
# Python — the three building blocks
import bisect
import itertools
import random

def fisher_yates(a: list) -> None:
    for i in range(len(a) - 1, 0, -1):
        j = random.randint(0, i)              # inclusive on both ends: j in [0, i]
        a[i], a[j] = a[j], a[i]

def reservoir_sample(stream, k: int) -> list:
    """Uniform sample of k items from an iterable of unknown length (Algorithm R)."""
    sample = []
    for i, x in enumerate(stream):            # x is item number i + 1
        if i < k:
            sample.append(x)
        else:
            j = random.randint(0, i)          # P(j < k) = k / (i + 1)
            if j < k:
                sample[j] = x                 # evict a uniformly chosen current member
    return sample

def weighted_picker(w: list[int]):
    prefix = list(itertools.accumulate(w))    # w = [1, 3, 2] -> [1, 4, 6]
    def pick() -> int:
        target = random.randint(1, prefix[-1])
        return bisect.bisect_left(prefix, target)   # 1 -> 0; 2..4 -> 1; 5..6 -> 2
    return pick

a = list(range(10)); fisher_yates(a); assert sorted(a) == list(range(10))
assert len(reservoir_sample(range(1000), 5)) == 5
assert weighted_picker([0, 5, 0])() == 1
```

```cpp
// C++ — use <random>, never rand() % n
#include <algorithm>
#include <random>
#include <utility>
#include <vector>

std::mt19937 rng{std::random_device{}()};       // seed once, reuse

void fisherYates(std::vector<int>& a) {
    for (int i = static_cast<int>(a.size()) - 1; i > 0; --i) {
        std::uniform_int_distribution<int> dist(0, i);   // closed range [0, i]
        std::swap(a[i], a[dist(rng)]);
    }
    // Equivalent library call: std::shuffle(a.begin(), a.end(), rng);
}

int main() {
    std::vector<int> v{1, 2, 3, 4, 5};
    fisherYates(v);
    std::sort(v.begin(), v.end());
    return v == std::vector<int>{1, 2, 3, 4, 5} ? 0 : 1;
}
```

### Variations

| Variation | Technique | Example Problems |
|---|---|---|
| **Weighted index** | Prefix sums + `bisect_left` on a random integer in `[1, total]` | Random Pick with Weight (LC 528) |
| **Weighted area** | Prefix sums of rectangle areas, then a uniform point inside | Random Point in Non-overlapping Rectangles (LC 497) |
| **Uniform from stream / list** | Reservoir, k = 1 | Linked List Random Node (LC 382), Random Pick Index (LC 398) |
| **Uniform permutation** | Fisher-Yates | Shuffle an Array (LC 384) |
| **Range minus blacklist** | Remap blacklisted values below `n - |B|` to allowed values above it | Random Pick with Blacklist (LC 710) |
| **Uniform point in a circle** | Radius `R · sqrt(u)` (not `R · u`), angle `2πv` | Generate Random Point in a Circle (LC 478) |
| **Build a distribution from another** | Rejection sampling | Implement Rand10() Using Rand7() (LC 470) |
| **O(1) weighted pick** | Alias method (Vose) | Follow-up to LC 528 |

### Common Mistakes

1. **Naive shuffle** `swap(a[i], a[rand(0, n-1)])` for every `i`. It produces `n^n` equally likely execution paths, which cannot map evenly onto `n!` permutations (for n = 3: 27 paths, 6 permutations, and 27 is not divisible by 6). Draw `j` from `[0, i]`.
2. **Modulo bias**: `rand() % n` favours small values unless `n` divides `RAND_MAX + 1`, and `RAND_MAX` can be as small as 32767 (it is on MSVC). Use `std::uniform_int_distribution`.
3. **Off-by-one in the weighted pick**: drawing from `[0, total)` and then calling `bisect_left` gives weight-0 items a chance. Either draw from `[1, total]` with `bisect_left`, or from `[0, total)` with `bisect_right`.
4. **Re-seeding inside a hot function** (`mt19937 rng(time(0))` per call). Calls in the same second return the same sequence. Seed once.
5. **Uniform radius in a circle**: points cluster at the centre, because area grows with r^2. Use `sqrt(u)`.
6. **Floating-point weights**: cumulative sums drift; the last bucket can be unreachable or overweighted. Use integer weights when possible, or clamp the index to `n - 1`.

### Related Patterns

- **Prefix Sum** ([Pattern 21](#21-prefix-sum--difference-array)) and **Binary Search** ([Pattern 11](#11-modified-binary-search)) — the weighted pick is a prefix sum plus `bisect`
- **Design Problems** ([Pattern 26](#26-design-problems)) — Insert Delete GetRandom O(1) combines an array with a hash map
- **Top K Elements** ([Pattern 12](#12-top-k-elements)) — randomized quickselect for the k-th element
- **See also:** [Fisher-Yates](DSA_Fundamentals.md#fisher-yates-shuffle), [Reservoir Sampling](DSA_Fundamentals.md#reservoir-sampling), and [Randomized Quickselect](DSA_Fundamentals.md#randomized-quickselect----expected-on) in DSA Fundamentals

### Example Problems

#### Problem 1: Random Pick with Weight (LC 528) — Medium

**Problem**: Given positive weights `w`, implement `pickIndex()` returning `i` with probability `w[i] / sum(w)`.

**Link**: [https://leetcode.com/problems/random-pick-with-weight/](https://leetcode.com/problems/random-pick-with-weight/)

**Intuition**: Lay the weights end to end on a number line: `w = [1, 3, 2]` covers `1 | 2 3 4 | 5 6`. Draw a uniform integer in `[1, 6]`. The index whose segment contains it is the first prefix sum ≥ the draw, which is `bisect_left`. Index `i` owns exactly `w[i]` of the `total` integers.

**Python Solution**:

```python
import bisect
import itertools
import random

class Solution:
    def __init__(self, w: list[int]):
        self.prefix = list(itertools.accumulate(w))

    def pickIndex(self) -> int:
        target = random.randint(1, self.prefix[-1])    # uniform integer in [1, total]
        return bisect.bisect_left(self.prefix, target)
```

**C++ Solution**:

```cpp
#include <algorithm>
#include <random>
#include <vector>
using namespace std;

class Solution {
    vector<long long> prefix;
    mt19937 rng{random_device{}()};

public:
    Solution(vector<int>& w) {
        long long running = 0;
        for (int x : w) prefix.push_back(running += x);
    }

    int pickIndex() {
        uniform_int_distribution<long long> dist(1, prefix.back());
        return lower_bound(prefix.begin(), prefix.end(), dist(rng)) - prefix.begin();
    }
};
```

**Complexity**: O(n) construction, O(log n) per pick. Space O(n).

**Follow-up (O(1) per pick, the alias method)**: Scale weights so the average is 1. Repeatedly pair an under-full column (`< 1`) with an over-full one: the small column keeps its own probability and its remaining space is "aliased" to the large one. Each of the `n` columns ends up holding at most two outcomes. Sampling: pick a column uniformly, then flip a biased coin. O(n) build, O(1) sample. It pays off when the same distribution is sampled millions of times, for example in random-walk graph embedding pipelines.

```python
import random

class AliasSampler:
    def __init__(self, w: list[float]):
        n, total = len(w), sum(w)
        scaled = [x * n / total for x in w]           # average becomes 1
        self.prob = [1.0] * n
        self.alias = list(range(n))
        small = [i for i, p in enumerate(scaled) if p < 1.0]
        large = [i for i, p in enumerate(scaled) if p >= 1.0]
        while small and large:
            s, l = small.pop(), large.pop()
            self.prob[s], self.alias[s] = scaled[s], l  # column s: s w.p. scaled[s], else l
            scaled[l] -= 1.0 - scaled[s]               # l donated that much to column s
            (small if scaled[l] < 1.0 else large).append(l)
        # leftovers are 1.0 up to rounding error: prob stays 1.0

    def sample(self) -> int:
        i = random.randrange(len(self.prob))
        return i if random.random() < self.prob[i] else self.alias[i]

counts = [0, 0, 0]
sampler = AliasSampler([1, 3, 2])
for _ in range(60_000):
    counts[sampler.sample()] += 1
assert all(abs(c - e) < 1_500 for c, e in zip(counts, [10_000, 30_000, 20_000]))
```

---

#### Problem 2: Linked List Random Node (LC 382) — Medium

**Problem**: Return a uniformly random node value from a singly linked list. Follow-up: the list is very long and its length is unknown; use O(1) extra space.

**Link**: [https://leetcode.com/problems/linked-list-random-node/](https://leetcode.com/problems/linked-list-random-node/)

**Intuition**: Reservoir sampling with `k = 1`: when visiting the `i`-th node (1-based), make it the current choice with probability `1/i`.

**Proof**: The `i`-th node is chosen at step `i` with probability `1/i` and survives every later step `j` with probability `1 - 1/j = (j-1)/j`. The product telescopes:

```text
P(node i is the answer) = 1/i · i/(i+1) · (i+1)/(i+2) · ... · (n-1)/n = 1/n
```

**Python Solution**:

```python
import random
from typing import Optional

class Solution:
    def __init__(self, head: Optional[ListNode]):
        self.head = head

    def getRandom(self) -> int:
        chosen, node, i = 0, self.head, 0
        while node:
            i += 1
            if random.randrange(i) == 0:          # probability 1 / i
                chosen = node.val
            node = node.next
        return chosen
```

**C++ Solution**:

```cpp
#include <random>
using namespace std;

class Solution {
    ListNode* head;
    mt19937 rng{random_device{}()};

public:
    Solution(ListNode* head) : head(head) {}

    int getRandom() {
        int chosen = 0, i = 0;
        for (ListNode* node = head; node; node = node->next) {
            ++i;
            if (uniform_int_distribution<int>(0, i - 1)(rng) == 0) chosen = node->val;
        }
        return chosen;
    }
};
```

**Complexity**: O(n) per call, O(1) space. If the list is static and calls are frequent, copying values into an array once gives O(1) per call; say so, then explain that the reservoir is the answer to the streaming follow-up.

---

#### Problem 3: Shuffle an Array (LC 384) — Medium

**Problem**: Implement `reset()` (return the original array) and `shuffle()` (return a uniformly random permutation).

**Link**: [https://leetcode.com/problems/shuffle-an-array/](https://leetcode.com/problems/shuffle-an-array/)

**Intuition**: Fisher-Yates from the back: for `i = n-1 .. 1`, swap `a[i]` with `a[j]` for uniform `j ∈ [0, i]`. Position `n-1` receives each element with probability `1/n`; position `n-2` receives each remaining element with probability `1/(n-1)`; and so on. Each permutation has probability `1/n · 1/(n-1) · ... · 1 = 1/n!`.

**Python Solution**:

```python
import random

class Solution:
    def __init__(self, nums: list[int]):
        self.original = nums[:]

    def reset(self) -> list[int]:
        return self.original[:]

    def shuffle(self) -> list[int]:
        a = self.original[:]
        for i in range(len(a) - 1, 0, -1):
            j = random.randint(0, i)
            a[i], a[j] = a[j], a[i]
        return a
```

**C++ Solution**:

```cpp
#include <random>
#include <utility>
#include <vector>
using namespace std;

class Solution {
    vector<int> original;
    mt19937 rng{random_device{}()};

public:
    Solution(vector<int>& nums) : original(nums) {}

    vector<int> reset() { return original; }

    vector<int> shuffle() {
        vector<int> a = original;
        for (int i = static_cast<int>(a.size()) - 1; i > 0; --i) {
            int j = uniform_int_distribution<int>(0, i)(rng);
            swap(a[i], a[j]);
        }
        return a;
    }
};
```

**Complexity**: O(n) per shuffle. Space O(n) for the copy of the original.

---

#### Problem 4: Random Pick with Blacklist (LC 710) — Hard

**Problem**: Pick uniformly from `[0, n)` excluding the values in `blacklist`. `n` can be 10^9, so the allowed values cannot be listed.

**Link**: [https://leetcode.com/problems/random-pick-with-blacklist/](https://leetcode.com/problems/random-pick-with-blacklist/)

**Intuition**: There are `m = n - |B|` allowed values. Draw uniformly from `[0, m)`. Most draws are allowed as they are. A blacklisted value `b < m` must be redirected, and there are exactly as many allowed values in `[m, n)` as there are blacklisted values in `[0, m)`, so pair them up once in the constructor. The map has at most `|B|` entries.

**Python Solution**:

```python
import random

class Solution:
    def __init__(self, n: int, blacklist: list[int]):
        self.m = n - len(blacklist)
        black = set(blacklist)
        self.remap: dict[int, int] = {}
        w = self.m                                 # scan allowed values in [m, n)
        for b in blacklist:
            if b < self.m:
                while w in black:
                    w += 1
                self.remap[b] = w
                w += 1

    def pick(self) -> int:
        x = random.randrange(self.m)
        return self.remap.get(x, x)
```

**C++ Solution**:

```cpp
#include <random>
#include <unordered_map>
#include <unordered_set>
#include <vector>
using namespace std;

class Solution {
    int m;
    unordered_map<int, int> remap;
    mt19937 rng{random_device{}()};

public:
    Solution(int n, vector<int>& blacklist) : m(n - static_cast<int>(blacklist.size())) {
        unordered_set<int> black(blacklist.begin(), blacklist.end());
        int w = m;
        for (int b : blacklist) {
            if (b < m) {
                while (black.count(w)) ++w;
                remap[b] = w++;
            }
        }
    }

    int pick() {
        int x = uniform_int_distribution<int>(0, m - 1)(rng);
        auto it = remap.find(x);
        return it == remap.end() ? x : it->second;
    }
};
```

**Complexity**: O(|B|) construction, O(1) per pick. Space O(|B|).

### Interview Q&A

**Q1.** Prove Algorithm R (reservoir of size k) is uniform.

By induction on the number of items seen, `t`. Claim: after `t ≥ k` items, each one is in the reservoir with probability `k/t`. Base `t = k`: all are in, with probability 1. Step to `t + 1`: the new item enters with probability `k/(t+1)`. An item already in the reservoir stays unless the new item enters **and** evicts it: `1 - (k/(t+1)) · (1/k) = t/(t+1)`. So it is present with probability `(k/t) · (t/(t+1)) = k/(t+1)`. The sample is also uniform as a set, not just per item, by the same argument applied to subsets.

**Q2.** How do you reservoir-sample with weights, or across many machines?

**Weighted (Efraimidis–Spirakis, A-Res)**: give each item the key `u^(1/w)` with `u` uniform in (0, 1) and keep the `k` largest keys in a min-heap of size `k`. Each item is included with the correct sequential weighted probability. (Use `log(u) / w` to avoid underflow.) **Distributed**: give every item an independent uniform random tag, keep the `k` smallest tags on each shard, then merge the shards' samples and keep the global `k` smallest. That is exactly a uniform k-subset of the union, and it parallelises because "k smallest" is mergeable. A per-shard Algorithm R followed by naive concatenation would over-represent small shards.

**Q3.** Where does reservoir sampling show up in profiling and observability tools?

Whenever you want a bounded, unbiased sample from a stream of unknown length: keeping `k` representative kernel dispatches or API calls from a trace that may run for hours, choosing which slow requests to keep full traces for, or sampling log lines for a histogram preview. The alternative of "keep every N-th event" is biased when events are periodic (it can phase-lock with a loop) and needs the stream length in advance. Hardware sampling profilers face the same issue, which is why they randomise (dither) the sampling interval.

**Q4.** What exactly is wrong with `rand() % n`?

Two problems. (1) **Modulo bias**: if `RAND_MAX + 1 = 32768` and `n = 10000`, values 0–2767 can be produced four ways and 2768–9999 only three ways, a 33% skew. (2) **Quality**: `rand()` is often a weak linear congruential generator whose low bits have short periods, and it uses hidden global state that is not thread-safe. Use `std::mt19937` (or `std::mt19937_64`) with `std::uniform_int_distribution`, which removes bias by rejection. In Python, `random.randrange`/`randint` are already unbiased; use the `secrets` module for anything security-related.

**Q5.** What is the expected running time of randomized quickselect, and why?

Expected O(n). A pivot is "good" with probability 1/2 if it lands in the middle half, which leaves at most 3/4 of the elements. So it takes an expected 2 partitions (2 linear passes) to shrink the problem by a factor of 3/4, and the total is at most `2(n + 3n/4 + 9n/16 + ...) = 8n`. The exact expected comparison count for finding the median is `2(1 + ln 2) n ≈ 3.39 n`. The worst case is still O(n^2); median-of-medians makes it worst-case O(n) with a larger constant, and introselect (`std::nth_element`) falls back to a guaranteed method when recursion gets too deep.

**Q6.** How do you test code that is supposed to be random?

(1) Make the RNG **injectable** and seed it in tests, so a failure is reproducible. (2) Test **invariants deterministically**: a shuffle is a permutation of the input; a pick is a valid index. (3) Test the **distribution statistically**: draw many samples and run a chi-square test, with a threshold chosen so the false-failure rate is acceptable (say 10^-6). For Shuffle an Array with n = 3, count all 6 permutations over 60,000 trials and expect about 10,000 each. (4) Keep a regression test for known-bad algorithms: the naive shuffle visibly fails the chi-square test at n = 3.

---

## 32. Math & Number Theory

### Overview

A small toolkit covers nearly every math-flavoured interview question. The common thread is replacing an O(n) loop with an O(log n) or O(sqrt n) idea, and doing arithmetic without overflow or precision loss.

| Tool | Idea | Cost |
|---|---|---|
| **Euclid's GCD** | `gcd(a, b) = gcd(b, a mod b)` | O(log min(a, b)) |
| **LCM** | `a / gcd(a, b) * b` (divide first to avoid overflow) | O(log) |
| **Fast exponentiation** | Square-and-multiply over the bits of the exponent | O(log e) multiplications |
| **Modular arithmetic** | Reduce after every `+`, `-`, `*`; divide via the modular inverse | O(1) per op |
| **Modular inverse** | Fermat: `a^(p-2) mod p` for prime `p`; extended Euclid in general | O(log p) |
| **Sieve of Eratosthenes** | Cross out multiples starting at `i*i` | O(n log log n) time, O(n) bits/bytes |
| **Integer square root** | Binary search on `r*r ≤ x`, or Newton's method | O(log x) or O(log log x) iterations |
| **nCr mod p** | Precompute factorials and inverse factorials | O(n) build, O(1) per query |

Proofs and extra material (extended Euclid, Chinese Remainder Theorem, Lucas) are in [DSA Fundamentals: Number Theory and Modular Arithmetic](DSA_Fundamentals.md#29-number-theory-and-modular-arithmetic).

**Why `10^9 + 7`?** It is prime, so every non-zero residue has an inverse. It is below 2^30, so the sum of two residues fits in a signed 32-bit `int` (2 · 10^9 < 2^31 - 1 ≈ 2.147 · 10^9). And the product of two residues (< 10^18) fits in a signed 64-bit integer (< 9.22 · 10^18).

**Fast exponentiation trace**, `3^13` with `13 = 0b1101`:

| bit (LSB first) | 1 | 0 | 1 | 1 |
|---|---|---|---|---|
| base before step | 3 | 9 | 81 | 6561 |
| result after step | 3 | 3 | 243 | 1,594,323 |

Four squarings instead of twelve multiplications; `3^13 = 1,594,323`.

### When to Use

- "Return the answer modulo 10^9 + 7" → reduce after every operation; use modpow for huge exponents and inverses for division
- `n` up to 10^9 or 10^18 in a counting problem → there is a formula or an O(log n) exponentiation; a loop to `n` will not finish
- "Count primes / smallest prime factor / factorise many numbers" → sieve (store the smallest prime factor for O(log n) factorisation)
- GCD/LCM wording: "largest block that tiles both", "measure exactly with two jugs", "cycle alignment", "simplify fractions" → Euclid and Bézout
- `sqrt`, `pow`, `log` on integers → integer binary search or `math.isqrt`, never a float cast
- "Is this sequence eventually periodic?" (Happy Number) → bound the values, then use cycle detection

### Template Code

```python
# Python — number-theory toolkit
import math

MOD = 10**9 + 7

def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a                                  # same as math.gcd; math.lcm in 3.9+

def mod_pow(base: int, exp: int, mod: int = MOD) -> int:
    result, base = 1, base % mod
    while exp:
        if exp & 1:
            result = result * base % mod
        base = base * base % mod
        exp >>= 1
    return result                             # built-in: pow(base, exp, mod)

def sieve(n: int) -> bytearray:
    """is_prime[i] for 0 <= i <= n."""
    is_prime = bytearray([1]) * (n + 1)
    is_prime[:2] = bytes(min(2, n + 1))       # 0 and 1 are not prime
    for i in range(2, math.isqrt(n) + 1):
        if is_prime[i]:
            is_prime[i * i::i] = bytes(len(range(i * i, n + 1, i)))
    return is_prime

class Binomial:
    """nCr mod a prime, O(n_max) precomputation, O(1) queries."""
    def __init__(self, n_max: int, mod: int = MOD):
        self.mod = mod
        self.fact = [1] * (n_max + 1)
        for i in range(1, n_max + 1):
            self.fact[i] = self.fact[i - 1] * i % mod
        self.inv_fact = [1] * (n_max + 1)
        self.inv_fact[n_max] = pow(self.fact[n_max], mod - 2, mod)   # Fermat's little theorem
        for i in range(n_max, 0, -1):
            self.inv_fact[i - 1] = self.inv_fact[i] * i % mod

    def C(self, n: int, k: int) -> int:
        if k < 0 or k > n:
            return 0
        return self.fact[n] * self.inv_fact[k] % self.mod * self.inv_fact[n - k] % self.mod

assert gcd(84, 36) == 12 and mod_pow(3, 13) == 1_594_323
assert sum(sieve(100)) == 25
assert Binomial(10).C(10, 3) == 120
```

```cpp
// C++ — number-theory toolkit
#include <cassert>
#include <cstdint>
#include <numeric>     // std::gcd, std::lcm (C++17)
#include <vector>

constexpr int64_t MOD = 1'000'000'007;

int64_t modPow(int64_t base, int64_t exp, int64_t mod = MOD) {
    int64_t result = 1;
    base %= mod;
    if (base < 0) base += mod;                 // C++ % keeps the sign of the dividend
    while (exp > 0) {
        if (exp & 1) result = result * base % mod;   // < 10^18: fits in int64_t
        base = base * base % mod;
        exp >>= 1;
    }
    return result;
}

int64_t modInverse(int64_t a) { return modPow(a, MOD - 2); }   // MOD must be prime

std::vector<bool> sieve(int n) {
    std::vector<bool> isPrime(n + 1, true);
    isPrime[0] = false;
    if (n >= 1) isPrime[1] = false;
    for (int64_t i = 2; i * i <= n; ++i)
        if (isPrime[i])
            for (int64_t j = i * i; j <= n; j += i) isPrime[j] = false;
    return isPrime;
}

int main() {
    assert(std::gcd(84, 36) == 12 && std::lcm(4, 6) == 12);
    assert(modPow(3, 13) == 1'594'323);
    assert(modInverse(2) * 2 % MOD == 1);
    auto p = sieve(100);
    int count = 0;
    for (bool b : p) count += b;
    assert(count == 25);
}
```

### Variations

| Variation | Technique | Example Problems |
|---|---|---|
| **Fast power** | Square-and-multiply; negative exponent → reciprocal | Pow(x, n) (LC 50), Super Pow (LC 372), Count Good Numbers (LC 1922) |
| **Integer root** | Binary search / Newton | Sqrt(x) (LC 69), Valid Perfect Square (LC 367) |
| **Primes** | Sieve, trial division up to `sqrt(n)` | Count Primes (LC 204), Closest Prime Numbers in Range (LC 2523) |
| **GCD / Bézout** | `gcd`, `ax + by = c` solvable iff `gcd(a, b) | c` | Greatest Common Divisor of Strings (LC 1071), Water and Jug Problem (LC 365), X of a Kind in a Deck (LC 914) |
| **Combinatorics mod p** | Factorials + inverse factorials, Pascal's triangle for small n | Unique Paths (LC 62), Count Sorted Vowel Strings (LC 1641) |
| **Catalan numbers** | `C(2n, n) / (n + 1)` | Unique Binary Search Trees (LC 96), Generate Parentheses count (LC 22) |
| **Overflow-safe parsing** | Check before multiply-and-add | Reverse Integer (LC 7), String to Integer (atoi) (LC 8) |
| **Digit manipulation / cycles** | Bound the value range, then detect the cycle | Happy Number (LC 202), Add Digits (LC 258, digital root `1 + (n - 1) % 9`) |
| **Big-number arithmetic on strings** | Schoolbook digit arrays | Multiply Strings (LC 43), Add Strings (LC 415) |

### Common Mistakes

1. **Reducing too late.** `a * b * c % MOD` overflows 64 bits before the `%`. Reduce after every multiplication.
2. **Taking `max`/`min` of reduced values.** Residues do not preserve order. If a DP needs both "max" and "mod", the problem is mis-stated or the max must be computed on exact values.
3. **Dividing a residue.** `(a / b) % MOD` is wrong once `a` has been reduced. Multiply by `modInverse(b)` instead (and `b` must not be a multiple of `MOD`).
4. **Negative results in C++.** `(a - b) % MOD` can be negative; write `((a - b) % MOD + MOD) % MOD`.
5. **`-n` overflow.** In Pow(x, n), `n = INT_MIN` makes `-n` overflow `int`. Widen to `long long` first.
6. **Float square roots.** `int(math.sqrt(10**18 - 1))` returns 1,000,000,000, but the true floor is 999,999,999. Use `math.isqrt` or an integer binary search.
7. **Sieve bounds.** "Primes **less than** n" (LC 204) vs "≤ n" differ by one element. Start crossing out at `i * i`, which in C++ needs a 64-bit `i * i` to avoid overflow near 2^31.
8. **LCM overflow.** `a * b / gcd(a, b)` overflows even when the LCM fits; compute `a / gcd(a, b) * b`.

### Related Patterns

- **Binary Search on the Answer** ([Pattern 28](#28-binary-search-on-the-answer)) — integer square root and "k-th number with property" problems
- **Fast and Slow Pointers** ([Pattern 3](#3-fast-and-slow-pointers)) — Happy Number's cycle detection
- **Bit Manipulation** ([Pattern 20](#20-bit-manipulation)) — fast exponentiation walks the exponent's bits
- **Dynamic Programming** ([Pattern 18](#18-dynamic-programming)) — counting DPs return answers mod 10^9 + 7
- **See also:** [Math, Probability and Estimation](Math_Probability_Estimation.md) for probability puzzles and back-of-the-envelope estimation

### Example Problems

#### Problem 1: Pow(x, n) (LC 50) — Medium

**Problem**: Compute `x^n` for a double `x` and a 32-bit integer `n`, which can be negative.

**Link**: [https://leetcode.com/problems/powx-n/](https://leetcode.com/problems/powx-n/)

**Intuition**: `x^n = (x^2)^(n/2)` if `n` is even, and `x · x^(n-1)` if it is odd. Iteratively: walk the bits of `n`, squaring `x` at each step and multiplying it into the result when the bit is 1. For negative `n`, compute `(1/x)^(-n)`, widening `n` first because `-(-2^31)` does not fit in an `int`.

**Python Solution**:

```python
class Solution:
    def myPow(self, x: float, n: int) -> float:
        if n < 0:
            x, n = 1 / x, -n               # Python ints don't overflow
        result = 1.0
        while n:
            if n & 1:
                result *= x
            x *= x
            n >>= 1
        return result
```

**C++ Solution**:

```cpp
class Solution {
public:
    double myPow(double x, int n) {
        long long e = n;                   // -INT_MIN overflows int; widen first
        if (e < 0) {
            x = 1 / x;
            e = -e;
        }
        double result = 1.0;
        while (e > 0) {
            if (e & 1) result *= x;
            x *= x;
            e >>= 1;
        }
        return result;
    }
};
```

**Complexity**: O(log |n|) multiplications. Space O(1).

---

#### Problem 2: Sqrt(x) (LC 69) — Easy

**Problem**: Return `floor(sqrt(x))` for `0 ≤ x ≤ 2^31 - 1` without using a built-in power or square-root function.

**Link**: [https://leetcode.com/problems/sqrtx/](https://leetcode.com/problems/sqrtx/)

**Intuition**: The answer is the **last** `r` with `r * r ≤ x`, a last-true binary search on `[0, x]` ([Pattern 28](#28-binary-search-on-the-answer)). In C++, test `mid <= x / mid` instead of `mid * mid <= x` to avoid overflow (safe because `mid ≥ 1` inside the loop). The bounds also need 64 bits: with `int`, the round-up step `hi - lo + 1` overflows when `x = INT_MAX`, which UBSan catches on the very first iteration.

**Python Solution**:

```python
class Solution:
    def mySqrt(self, x: int) -> int:
        lo, hi = 0, x
        while lo < hi:
            mid = (lo + hi + 1) // 2          # last-true: round up
            if mid * mid <= x:
                lo = mid
            else:
                hi = mid - 1
        return lo


def isqrt_newton(x: int) -> int:
    """Integer Newton's method: converges quadratically from above."""
    if x < 2:
        return x
    r = x
    while r * r > x:
        r = (r + x // r) // 2
    return r

assert all(isqrt_newton(v) == Solution().mySqrt(v) for v in range(2000))
```

**C++ Solution**:

```cpp
class Solution {
public:
    int mySqrt(int x) {
        long long lo = 0, hi = x;               // 64-bit: hi - lo + 1 overflows int at x = INT_MAX
        while (lo < hi) {
            long long mid = lo + (hi - lo + 1) / 2;   // mid >= 1 here
            if (mid <= x / mid) lo = mid;       // mid * mid <= x without forming the product
            else hi = mid - 1;
        }
        return static_cast<int>(lo);
    }
};
```

**Complexity**: Binary search O(log x), about 31 iterations. Newton's method takes O(log log x) iterations once it is close, plus a few halving steps at the start from `r = x`.

---

#### Problem 3: Count Primes (LC 204) — Medium

**Problem**: Count the primes strictly less than `n` (`n ≤ 5 · 10^6`).

**Link**: [https://leetcode.com/problems/count-primes/](https://leetcode.com/problems/count-primes/)

**Intuition**: Sieve of Eratosthenes. For each prime `i`, cross out `i*i, i*i + i, ...`. Smaller multiples `k·i` with `k < i` were already crossed out by `k`'s prime factors. Stop when `i*i ≥ n`. The total work is `sum over primes p ≤ sqrt(n) of n/p ≈ n ln ln n`.

**Python Solution**:

```python
import math

class Solution:
    def countPrimes(self, n: int) -> int:
        if n < 3:
            return 0
        is_prime = bytearray([1]) * n             # indices 0..n-1
        is_prime[0] = is_prime[1] = 0
        for i in range(2, math.isqrt(n - 1) + 1):
            if is_prime[i]:
                is_prime[i * i::i] = bytes(len(range(i * i, n, i)))   # C-speed slice assignment
        return sum(is_prime)
```

**C++ Solution**:

```cpp
#include <algorithm>
#include <vector>
using namespace std;

class Solution {
public:
    int countPrimes(int n) {
        if (n < 3) return 0;
        vector<char> isPrime(n, 1);              // char, not vector<bool>: faster byte writes
        isPrime[0] = isPrime[1] = 0;
        for (long long i = 2; i * i < n; ++i)
            if (isPrime[i])
                for (long long j = i * i; j < n; j += i) isPrime[j] = 0;
        return count(isPrime.begin(), isPrime.end(), 1);
    }
};
```

**Complexity**: Time O(n log log n). Space O(n) bytes. A sieve over odd numbers only halves both. A **segmented sieve** processes cache-sized blocks (for example 32 KiB to fit in L1), which is several times faster for `n ≥ 10^8` and needs only O(sqrt n) memory for the base primes.

---

#### Problem 4: Greatest Common Divisor of Strings (LC 1071) — Easy

**Problem**: Return the largest string `x` such that both `str1` and `str2` are concatenations of copies of `x`.

**Link**: [https://leetcode.com/problems/greatest-common-divisor-of-strings/](https://leetcode.com/problems/greatest-common-divisor-of-strings/)

**Intuition**: If a common divisor string exists, then `str1 + str2 == str2 + str1` (both sides are copies of `x`). The converse also holds: two strings commute under concatenation only if both are powers of a common string (Lyndon–Schützenberger). Once a common base exists, the largest common divisor has length `gcd(len1, len2)`, by the same reasoning as integer GCD.

**Python Solution**:

```python
import math

class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        if str1 + str2 != str2 + str1:
            return ""
        return str1[:math.gcd(len(str1), len(str2))]
```

**C++ Solution**:

```cpp
#include <numeric>
#include <string>
using namespace std;

class Solution {
public:
    string gcdOfStrings(string str1, string str2) {
        if (str1 + str2 != str2 + str1) return "";
        return str1.substr(0, gcd(str1.size(), str2.size()));
    }
};
```

**Complexity**: Time O(n + m). Space O(n + m) for the concatenations.

---

#### Problem 5: Water and Jug Problem (LC 365) — Medium

**Problem**: Jugs of capacity `x` and `y`, unlimited water. You can fill, empty, or pour one into the other. Can you end with exactly `target` litres in total across both jugs?

**Link**: [https://leetcode.com/problems/water-and-jug-problem/](https://leetcode.com/problems/water-and-jug-problem/)

**Intuition**: Every operation changes the total by a multiple of `x` or `y`, so reachable totals are of the form `ax + by`. By **Bézout's identity**, the integers expressible as `ax + by` are exactly the multiples of `gcd(x, y)`, and the pouring moves can realise any such total between 0 and `x + y`. So the answer is `target ≤ x + y` and `target % gcd(x, y) == 0`. A BFS over `(a, b)` states also works but is O(x · y).

**Python Solution**:

```python
import math

class Solution:
    def canMeasureWater(self, x: int, y: int, target: int) -> bool:
        if target > x + y:
            return False
        return target % math.gcd(x, y) == 0
```

**C++ Solution**:

```cpp
#include <numeric>

class Solution {
public:
    bool canMeasureWater(int x, int y, int target) {
        if (static_cast<long long>(x) + y < target) return false;
        return target % std::gcd(x, y) == 0;
    }
};
```

**Complexity**: O(log min(x, y)). Space O(1).

---

#### Problem 6: Count Good Numbers (LC 1922) — Medium

**Problem**: A digit string of length `n` is good if digits at even indices are even (0, 2, 4, 6, 8) and digits at odd indices are prime (2, 3, 5, 7). Count good strings of length `n ≤ 10^15`, mod 10^9 + 7.

**Link**: [https://leetcode.com/problems/count-good-numbers/](https://leetcode.com/problems/count-good-numbers/)

**Intuition**: Positions are independent: `ceil(n/2)` even indices with 5 choices and `floor(n/2)` odd indices with 4 choices. The answer is `5^ceil(n/2) · 4^floor(n/2) mod p`. With `n = 10^15`, only fast modular exponentiation (about 50 squarings) works.

**Python Solution**:

```python
class Solution:
    def countGoodNumbers(self, n: int) -> int:
        MOD = 10**9 + 7
        return pow(5, (n + 1) // 2, MOD) * pow(4, n // 2, MOD) % MOD
```

**C++ Solution**:

```cpp
class Solution {
    static constexpr long long MOD = 1'000'000'007;

    static long long modPow(long long base, long long exp) {
        long long result = 1;
        base %= MOD;
        while (exp > 0) {
            if (exp & 1) result = result * base % MOD;
            base = base * base % MOD;
            exp >>= 1;
        }
        return result;
    }

public:
    int countGoodNumbers(long long n) {
        return static_cast<int>(modPow(5, (n + 1) / 2) * modPow(4, n / 2) % MOD);
    }
};
```

**Complexity**: O(log n). Space O(1). Checks: `n = 1` → 5, `n = 4` → 400.

---

#### Problem 7: Happy Number (LC 202), the math view

The two-pointer solution is in [Pattern 3, Problem 4](#problem-4-happy-number-leetcode-202--medium). The math explains **why** the loop must end: a number with `d ≥ 4` digits maps to at most `81d`, which has fewer digits (for example 9,999 → 324). So every sequence drops to 999 or below within a few steps, after which every value is at most `3 · 81 = 243`. A sequence confined to a finite set must repeat. Checking all starting values up to 243 shows there is exactly one cycle besides the fixed point 1:

```text
4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4
```

So `n` is unhappy exactly when the sequence reaches 4, which gives an O(1)-memory solution without Floyd:

```python
class Solution:
    def isHappy(self, n: int) -> bool:
        while n != 1 and n != 4:
            n = sum(int(d) ** 2 for d in str(n))
        return n == 1
```

Say in the interview that this relies on a precomputed fact. Floyd's algorithm is the general method that needs no such knowledge.

### Interview Q&A

**Q1.** Which operations can you apply "mod p" to, and which not?

Addition, subtraction and multiplication commute with reduction: `(a op b) mod p = ((a mod p) op (b mod p)) mod p`. Exponentiation with a reduced **base** is fine, but the **exponent** cannot be reduced mod p. It can be reduced mod `p - 1` when `p` is prime and the base is not a multiple of `p` (Fermat). Division needs the modular inverse. Comparisons, `min`, `max`, floor division and square roots do not survive reduction, so any step that needs them must work on exact values (Python big ints) or the problem must be restructured.

**Q2.** How do you compute a modular inverse when the modulus is not prime?

Extended Euclid: find `x, y` with `a·x + m·y = gcd(a, m)`. If the gcd is 1, then `x mod m` is the inverse; otherwise no inverse exists. It runs in O(log m). Fermat's `a^(p-2)` only works for prime moduli. For all inverses of `1..n` modulo a prime, there is an O(n) recurrence: `inv[i] = -(p // i) · inv[p % i] mod p`, which is how factorial tables are built quickly. Python 3.8+ provides `pow(a, -1, m)`, which raises `ValueError` if no inverse exists.

**Q3.** What is the complexity of Euclid's algorithm, and what is the worst case?

O(log min(a, b)) iterations. After two steps the larger argument at least halves (if `b ≤ a/2`, then `a mod b < b ≤ a/2`; otherwise `a mod b = a - b < a/2`). Lamé's theorem identifies the worst case as consecutive Fibonacci numbers, where every quotient is 1. The number of steps is at most about 5 times the number of decimal digits of the smaller input.

**Q4.** How do you detect overflow in Reverse Integer or atoi without 64-bit integers?

Check **before** updating: if `rev > INT_MAX / 10`, or `rev == INT_MAX / 10` and `digit > 7`, the next `rev * 10 + digit` overflows (mirror the check for negatives: `INT_MIN / 10` and digit `-8`). In C++, GCC and Clang also offer `__builtin_mul_overflow` and `__builtin_add_overflow`, and C++26 adds `std::add_sat`/`std::mul_sat` for saturating arithmetic. Signed overflow in C++ is undefined behaviour, so checking afterwards (`if (rev < 0)`) is wrong: the optimiser may delete the check.

**Q5.** What precision traps show up with `double` in integer problems?

A `double` has a 53-bit mantissa, so integers above 2^53 ≈ 9 · 10^15 are not all representable. `int(math.sqrt(10**18 - 1))` returns 10^9 (one too high) because the input rounds up to 10^18 when converted. `math.pow`, `math.log2` and `math.ceil(a / b)` have similar problems near exact values. Integer-only alternatives: `math.isqrt`, `n.bit_length()` for `floor(log2 n) + 1`, and `(a + b - 1) // b` for ceiling division. In C++, `std::sqrt` on a 64-bit integer needs a correction step (`while (r * r > x) --r; while ((r+1)*(r+1) <= x) ++r;`).

**Q6.** How do you recognise a Catalan-number problem?

The structure splits into a "first element/root/matching pair" and two independent sub-structures whose sizes add to `n - 1`: `C(n) = sum over i of C(i) · C(n-1-i)`, with `C(0) = 1`. Typical cases: the number of BSTs on `n` keys (LC 96), valid parenthesis strings with `n` pairs, triangulations of an `(n+2)`-gon, and monotonic lattice paths that do not cross the diagonal. Closed form `C(n) = C(2n, n) / (n + 1)`: 1, 1, 2, 5, 14, 42, 132. With a modulus, compute `C(2n, n) · inv(n + 1)`.

---

## 33. Meet-in-the-Middle & Bidirectional BFS

### Overview

Both techniques split an exponential search into two halves that are each **square-root sized**, then combine them cheaply.

**Meet-in-the-middle (MITM)**: with `n` items, enumerating all subsets costs 2^n. Split the items into two halves of `n/2`, enumerate each half's 2^(n/2) subset sums, sort one side, and combine with binary search or two pointers.

| n | 2^n (brute force) | 2 · 2^(n/2) (MITM) |
|---|---|---|
| 30 | 1.1 · 10^9 | 65,536 |
| 40 | 1.1 · 10^12 (hours) | 2.1 · 10^6 (milliseconds) |

The tell is the constraint **`n ≤ 40`** on a subset problem with **large values** (so a DP over sums, O(n · S), is impossible).

**Bidirectional BFS**: with branching factor `b` and shortest distance `d`, one-sided BFS explores about `b^d` states. Searching from both ends until the frontiers touch explores about `2 · b^(d/2)`. Word Ladder with 5-letter words has up to 25 · 5 = 125 neighbours per word: at `d = 6`, `125^6 ≈ 3.8 · 10^12` vs `2 · 125^3 ≈ 3.9 · 10^6` in the worst case. (A real dictionary prunes most candidates, so the practical gain is smaller, but still large.)

### When to Use

- `n ≤ 40` (or `2n ≤ 30`) items, "choose a subset" with a sum or XOR target, values up to 10^7 – 10^9 → MITM
- "Closest subset sum to a goal", "split into two groups minimising the difference", "count 4-tuples summing to 0" → MITM
- Shortest path where **both the start and the single goal are known**, edges are reversible (or reverse edges are available), and the branching factor is large → bidirectional BFS
- Puzzles with huge state spaces and an explicit goal state (sliding puzzles, lock combinations, word transformations) → bidirectional BFS

### Template Code

```python
# Python — MITM subset sums and bidirectional BFS
from bisect import bisect_left

def subset_sums(arr: list[int]) -> list[int]:
    """All 2^len(arr) subset sums, built by doubling."""
    sums = [0]
    for x in arr:
        sums += [s + x for s in sums]
    return sums

def closest_subset_sum(nums: list[int], goal: int) -> int:
    half = len(nums) // 2
    left, right = subset_sums(nums[:half]), sorted(subset_sums(nums[half:]))
    best = abs(goal)                                  # empty subset
    for s in left:
        i = bisect_left(right, goal - s)
        for j in (i - 1, i):                          # neighbours of the insertion point
            if 0 <= j < len(right):
                best = min(best, abs(s + right[j] - goal))
    return best

def bidirectional_bfs(start, goal, neighbors) -> int:
    """Fewest edges between start and goal in an undirected graph, or -1."""
    if start == goal:
        return 0
    dist_f, dist_b = {start: 0}, {goal: 0}
    front, back = [start], [goal]
    while front and back:
        if len(front) > len(back):                    # always expand the smaller frontier
            front, back, dist_f, dist_b = back, front, dist_b, dist_f
        nxt = []
        for u in front:
            for v in neighbors(u):
                if v in dist_b:                       # the two searches touch
                    return dist_f[u] + 1 + dist_b[v]
                if v not in dist_f:
                    dist_f[v] = dist_f[u] + 1
                    nxt.append(v)
        front = nxt
    return -1

assert closest_subset_sum([5, -7, 3, 5], 6) == 0
assert bidirectional_bfs(0, 10, lambda u: [u - 1, u + 1]) == 10
```

Why returning at the first touch is optimal: before the current layer is expanded, the forward search knows every node within distance `a` of the start and the backward search every node within `b` of the goal, and no node is known to both (that would have been detected). So the true distance `D` is greater than `a + b`. Any touch found while expanding the forward frontier gives a path of length `a + 1 + dist_b[v] ≤ a + 1 + b`. Since `D ≥ a + b + 1`, that path has length exactly `D`.

### Variations

| Variation | Combine step | Example Problems |
|---|---|---|
| **Closest subset sum** | Sort one half, binary search or two pointers | Closest Subsequence Sum (LC 1755) |
| **Equal-size split** | Group subset sums by subset size `k`, pair size `k` with size `n - k` | Partition Array Into Two Arrays to Minimize Sum Difference (LC 2035) |
| **Count k-tuples with target sum** | Hash map of pair sums | 4Sum II (LC 454) |
| **Subset count with sum ≤ S** | Sort one half, count with two pointers | Classic "knapsack with n ≤ 40" |
| **Bidirectional word / state search** | Expand the smaller frontier | Word Ladder (LC 127), Open the Lock (LC 752), Minimum Genetic Mutation (LC 433) |
| **Bidirectional Dijkstra** | Stop when `top_f + top_b ≥ best` | Road-network routing (not usually coded in interviews) |

### Common Mistakes

1. **Generating subsets recursively in Python for 2^20 items.** Function-call overhead dominates. Use the doubling loop or bitmask DP over sums.
2. **Checking only one neighbour of the insertion point.** The closest value can be just below or just above; check `i - 1` and `i`.
3. **Ignoring the size constraint** in LC 2035. Both arrays must have exactly `n` elements, so subset sums must be grouped by size.
4. **Bidirectional BFS on a directed graph without reverse edges.** The backward search must follow edges **into** nodes.
5. **Expanding both frontiers fully every round** instead of only the smaller one. Expanding the smaller side keeps the work near `2 · b^(d/2)` when the two sides grow at different rates.
6. **Returning at the first meeting in weighted bidirectional Dijkstra.** The first node settled by both sides is not necessarily on a shortest path; you must continue until the stopping condition holds.

### Related Patterns

- **BFS** ([Pattern 7](#7-bfs-breadth-first-search)) — the one-sided Word Ladder solution is Problem 4 there
- **Backtracking / Subsets** ([Pattern 10](#10-subsets--backtracking)) — MITM is subset enumeration done twice at half size
- **Two Pointers** ([Pattern 1](#1-two-pointers)) and **Binary Search** ([Pattern 11](#11-modified-binary-search)) — the combine step
- **Bitmask DP** ([Pattern 18](#18-dynamic-programming)) — for `n ≤ 20` with interaction between items, bitmask DP is usually the better fit; MITM needs the halves to be independent

### Example Problems

#### Problem 1: Word Ladder (LC 127) — Hard, bidirectional

**Problem**: Transform `beginWord` into `endWord` by changing one letter at a time, with every intermediate word in `wordList`. Return the number of **words** in the shortest sequence, or 0.

**Link**: [https://leetcode.com/problems/word-ladder/](https://leetcode.com/problems/word-ladder/)

**Intuition**: The one-sided BFS is [Pattern 7, Problem 4](#problem-4--word-ladder-lc-127-medium). Both endpoints are known and the "differ by one letter" relation is symmetric, so search from both ends and always expand the smaller frontier. Removing words from the dictionary when they are discovered acts as a shared visited set. Counting: `steps` is the number of words on a path from the start to the current front frontier plus the words from the goal to the back frontier, minus one for the overlap, so a touch means `steps + 1` words in total.

**Python Solution**:

```python
class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: list[str]) -> int:
        words = set(wordList)
        if endWord not in words:
            return 0
        front, back = {beginWord}, {endWord}
        words.discard(beginWord)
        words.discard(endWord)
        steps = 1
        while front and back:
            if len(front) > len(back):
                front, back = back, front          # expand the smaller side
            nxt = set()
            for w in front:
                for i in range(len(w)):
                    for ch in "abcdefghijklmnopqrstuvwxyz":
                        cand = w[:i] + ch + w[i + 1:]
                        if cand in back:
                            return steps + 1
                        if cand in words:
                            words.remove(cand)     # visited
                            nxt.add(cand)
            front = nxt
            steps += 1
        return 0
```

**C++ Solution**:

```cpp
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>
using namespace std;

class Solution {
public:
    int ladderLength(string beginWord, string endWord, vector<string>& wordList) {
        unordered_set<string> words(wordList.begin(), wordList.end());
        if (!words.count(endWord)) return 0;
        unordered_set<string> front{beginWord}, back{endWord};
        words.erase(beginWord);
        words.erase(endWord);
        for (int steps = 1; !front.empty() && !back.empty(); ++steps) {
            if (front.size() > back.size()) swap(front, back);   // O(1) swap
            unordered_set<string> next;
            for (string w : front) {                             // copy: mutated in place below
                for (size_t i = 0; i < w.size(); ++i) {
                    char orig = w[i];
                    for (char c = 'a'; c <= 'z'; ++c) {
                        if (c == orig) continue;
                        w[i] = c;
                        if (back.count(w)) return steps + 1;
                        if (words.count(w)) {
                            words.erase(w);
                            next.insert(w);
                        }
                    }
                    w[i] = orig;
                }
            }
            front.swap(next);
        }
        return 0;
    }
};
```

**Complexity**: Worst case the same as one-sided BFS, O(N · L · 26) candidate checks with string hashing O(L) each, but typically explores far fewer words. Space O(N · L).

---

#### Problem 2: Closest Subsequence Sum (LC 1755) — Hard

**Problem**: `nums` has `n ≤ 40` integers in `[-10^7, 10^7]`. Choose a subsequence (any subset) whose sum is as close as possible to `goal`; return `|sum - goal|`.

**Link**: [https://leetcode.com/problems/closest-subsequence-sum/](https://leetcode.com/problems/closest-subsequence-sum/)

**Intuition**: Sums span about 8 · 10^8 values, so a DP over sums is out, and 2^40 subsets is too many. Split into halves of at most 20: each has at most 2^20 ≈ 10^6 sums. Sort both, then walk them with two pointers: `left` ascending and `right` descending. If the pair sum is below `goal`, a larger left sum is needed; if above, a smaller right sum.

**Python Solution**:

```python
class Solution:
    def minAbsDifference(self, nums: list[int], goal: int) -> int:
        def subset_sums(arr: list[int]) -> list[int]:
            sums = [0]
            for x in arr:
                sums += [s + x for s in sums]
            return sums

        half = len(nums) // 2
        left = sorted(subset_sums(nums[:half]))
        right = sorted(subset_sums(nums[half:]))
        i, j = 0, len(right) - 1
        best = abs(goal)
        while i < len(left) and j >= 0:
            s = left[i] + right[j]
            best = min(best, abs(s - goal))
            if s < goal:
                i += 1
            elif s > goal:
                j -= 1
            else:
                return 0
        return best
```

**C++ Solution**:

```cpp
#include <algorithm>
#include <climits>
#include <cstdlib>
#include <vector>
using namespace std;

class Solution {
    static vector<int> subsetSums(const vector<int>& a) {
        vector<int> sums{0};
        sums.reserve(size_t{1} << a.size());
        for (int x : a) {
            size_t sz = sums.size();
            for (size_t i = 0; i < sz; ++i) sums.push_back(sums[i] + x);
        }
        return sums;
    }

public:
    int minAbsDifference(vector<int>& nums, int goal) {
        size_t half = nums.size() / 2;
        vector<int> left = subsetSums(vector<int>(nums.begin(), nums.begin() + half));
        vector<int> right = subsetSums(vector<int>(nums.begin() + half, nums.end()));
        sort(left.begin(), left.end());
        sort(right.begin(), right.end());
        long long best = llabs(static_cast<long long>(goal));
        int i = 0, j = static_cast<int>(right.size()) - 1;
        while (i < static_cast<int>(left.size()) && j >= 0) {
            long long s = static_cast<long long>(left[i]) + right[j];
            best = min(best, llabs(s - goal));
            if (s < goal) ++i;
            else if (s > goal) --j;
            else return 0;
        }
        return static_cast<int>(best);
    }
};
```

**Complexity**: Time O(2^(n/2) · n) (sorting 2^20 values dominates). Space O(2^(n/2)), about 4 MiB per half as 32-bit ints.

---

#### Problem 3: Partition Array Into Two Arrays to Minimize Sum Difference (LC 2035) — Hard

**Problem**: `nums` has `2n` integers (`n ≤ 15`). Split it into two arrays of exactly `n` elements each, minimising the absolute difference of their sums.

**Link**: [https://leetcode.com/problems/partition-array-into-two-arrays-to-minimize-sum-difference/](https://leetcode.com/problems/partition-array-into-two-arrays-to-minimize-sum-difference/)

**Intuition**: Choose the first array; its sum `A` determines the difference `|total - 2A|`. Split `nums` into a left and right half of `n` each. If the first array takes `k` elements from the left half, it takes `n - k` from the right half. So group each half's subset sums **by subset size**, sort the right groups, and for each left sum `a` of size `k`, binary-search the right group of size `n - k` for the `b` that brings `2(a + b)` closest to `total`.

**Python Solution**:

```python
from bisect import bisect_left

class Solution:
    def minimumDifference(self, nums: list[int]) -> int:
        n = len(nums) // 2
        total = sum(nums)

        def sums_by_size(arr: list[int]) -> list[list[int]]:
            m = len(arr)
            sums = [0] * (1 << m)
            groups = [[] for _ in range(m + 1)]
            for mask in range(1 << m):
                if mask:
                    low = mask & -mask                         # lowest set bit
                    sums[mask] = sums[mask ^ low] + arr[low.bit_length() - 1]
                groups[mask.bit_count()].append(sums[mask])    # int.bit_count: Python 3.10+
            return groups

        left, right = sums_by_size(nums[:n]), sums_by_size(nums[n:])
        for g in right:
            g.sort()
        best = float('inf')
        for k in range(n + 1):
            r = right[n - k]
            for a in left[k]:
                i = bisect_left(r, total / 2 - a)              # b closest to total/2 - a
                for j in (i - 1, i):
                    if 0 <= j < len(r):
                        best = min(best, abs(total - 2 * (a + r[j])))
        return best
```

**C++ Solution**:

```cpp
#include <algorithm>
#include <climits>
#include <cstdlib>
#include <numeric>
#include <vector>
using namespace std;

class Solution {
public:
    int minimumDifference(vector<int>& nums) {
        int n = nums.size() / 2;
        long long total = accumulate(nums.begin(), nums.end(), 0LL);
        vector<vector<int>> left(n + 1), right(n + 1);
        for (int mask = 0; mask < (1 << n); ++mask) {
            int sl = 0, sr = 0;
            for (int i = 0; i < n; ++i) {
                if (mask >> i & 1) {
                    sl += nums[i];
                    sr += nums[n + i];
                }
            }
            int k = __builtin_popcount(mask);                  // GCC/Clang; std::popcount in C++20
            left[k].push_back(sl);
            right[k].push_back(sr);
        }
        for (auto& g : right) sort(g.begin(), g.end());
        long long best = LLONG_MAX;
        for (int k = 0; k <= n; ++k) {
            const vector<int>& r = right[n - k];
            for (int a : left[k]) {
                // first b with 2(a + b) >= total; the best b is it or its predecessor
                auto it = lower_bound(r.begin(), r.end(), a, [&](int b, int av) {
                    return 2LL * (av + b) < total;
                });
                if (it != r.end()) best = min(best, llabs(total - 2LL * (a + *it)));
                if (it != r.begin()) best = min(best, llabs(total - 2LL * (a + *prev(it))));
            }
        }
        return static_cast<int>(best);
    }
};
```

**Complexity**: Time O(2^n · n) for generation (O(2^n) in the Python version) plus O(2^n log 2^n) = O(2^n · n) for sorting and searching. With n = 15 that is about 5 · 10^5 operations. Space O(2^n).

### Interview Q&A

**Q1.** Derive the speed-up of bidirectional BFS, and say when it disappears.

One-sided BFS to depth `d` with branching `b` touches `1 + b + ... + b^d ≈ b^d` nodes. Two searches to depth `d/2` touch `2 · b^(d/2)`. The ratio is `b^(d/2) / 2`, so the gain grows exponentially with depth. It disappears when (a) the graph is narrow (b ≈ 1–2, like a path or grid corridor), (b) one side's frontier explodes much faster than the other, which expanding the smaller frontier mitigates, (c) the goal is a **set** or a predicate rather than a single state, so you cannot start a backward search (unless the goal set is small enough to seed a multi-source backward BFS), or (d) predecessors are expensive to generate (a directed implicit graph).

**Q2.** How do you know a problem wants meet-in-the-middle rather than DP?

Look at the constraints. Subset problems with small values (sum ≤ about 10^5) want the knapsack DP, O(n · S). Problems with `n ≤ 20` and interactions between chosen items want bitmask DP. Problems with `n` in the 30–40 range and values up to 10^7–10^9, where the two halves contribute independently (sum, XOR, product), want MITM. If `n ≤ 40` appears in a subset problem, MITM is almost certainly intended.

**Q3.** 4Sum II (LC 454) is MITM too. How?

Count tuples `(i, j, k, l)` with `A[i] + B[j] + C[k] + D[l] = 0` over four arrays of length `n ≤ 200`. Brute force is O(n^4) = 1.6 · 10^9. Split into (A, B) and (C, D): store the counts of every `A[i] + B[j]` in a hash map (n^2 = 40,000 entries), then for every `C[k] + D[l]` add `count[-(C[k] + D[l])]`. That is O(n^2) time and space. The same idea, "enumerate half, look up the complement", is the heart of every MITM solution.

**Q4.** What does MITM cost in memory, and how can you reduce it?

Each half stores 2^(n/2) sums: 2^20 × 4 bytes = 4 MiB as C++ `int`, 8 MiB as `int64`. A Python list of 2^20 ints costs 8 bytes per pointer plus about 28 bytes per int object (small ints are cached, larger ones are not), so roughly 30–40 MB. If memory is tight, store only one half and enumerate the other half's sums on the fly (binary-searching the stored half for each), or use an unbalanced split: store 2^(n/3) sums and enumerate 2^(2n/3), trading time for memory. Separately, generating each half's sums **already sorted** by merging `S` with `S + x` for each element (O(2^(n/2)) total) removes the sort's log factor.

**Q5.** Does the Word Ladder one-sided BFS ever beat the bidirectional version?

When `endWord` is not in the dictionary, both return immediately. When the answer is very short (1–2 steps), the bidirectional bookkeeping is pure overhead. When the dictionary is tiny, both are fast. The asymptotic win appears with long ladders in dense dictionaries. For **Word Ladder II** (LC 126, all shortest sequences), bidirectional BFS is used to build the layered DAG of shortest-path edges, and a DFS then enumerates paths. Doing it one-sided often exceeds the time limit because the DAG becomes too large.

**Q6.** For weighted graphs, what is the correct stopping rule for bidirectional Dijkstra?

Run a forward Dijkstra from `s` and a backward Dijkstra from `t` (on reversed edges), alternating. Maintain `μ` = the best `dist_f[u] + w(u, v) + dist_b[v]` seen over any edge relaxed between the two searched regions. Stop when `top_f + top_b ≥ μ`, where `top_f` and `top_b` are the current minimum keys of the two heaps. Stopping at the first node settled by both sides can return a non-shortest path. Road-routing engines combine this with preprocessing (contraction hierarchies, landmarks/ALT) to answer continental queries in milliseconds.

---

## Pattern Selection Flowchart

Use this decision tree when you encounter a new problem and need to identify which pattern to apply.

```text
START: Read the problem statement
│
├─ Does it involve a SORTED array or searching?
│   ├─ Yes: Need to find a specific element? ──► Binary Search (Pattern 11)
│   ├─ Yes: Need to find a pair/triplet summing to target? ──► Two Pointers (Pattern 1)
│   └─ Yes: Array is rotated? ──► Modified Binary Search (Pattern 11)
│
├─ Does it involve CONTIGUOUS subarrays or substrings?
│   ├─ Yes: Fixed window size? ──► Sliding Window - Fixed (Pattern 2)
│   ├─ Yes: Variable window / longest / shortest (non-negative values)? ──► Sliding Window - Dynamic (Pattern 2)
│   ├─ Yes: Count windows with EXACTLY K distinct / K odd? ──► atMost(K) - atMost(K-1) (Pattern 2)
│   ├─ Yes: Shortest with sum >= K, negatives allowed? ──► Prefix Sum + Monotonic Deque (Pattern 2)
│   ├─ Yes: Window needs median / nearest value / k-th? ──► Ordered Containers (Pattern 29)
│   ├─ Yes: Repeated / duplicate substrings, longest repeat? ──► Rolling Hash (+ binary search on length) (Pattern 30)
│   ├─ Yes: Pattern search, period, palindromic prefix? ──► KMP prefix function (Pattern 30)
│   ├─ Yes: Sum == k / divisible by k / equal counts, negatives allowed? ──► Prefix Sum + HashMap (Pattern 21)
│   ├─ Yes: Many range queries on a static array? ──► Prefix Sum (Pattern 21)
│   └─ Yes: Many range updates, then read the result? ──► Difference Array (Pattern 21)
│
├─ Does it involve a LINKED LIST?
│   ├─ Detect cycle or find middle? ──► Fast & Slow Pointers (Pattern 3)
│   └─ Reverse all or part? ──► In-place Linked List Reversal (Pattern 6)
│
├─ Does it involve INTERVALS (time ranges, schedules)?
│   ├─ Merge / insert / remove overlaps? ──► Merge Intervals (Pattern 4)
│   └─ Max concurrency / rooms / skyline / online booking? ──► Line Sweep (Pattern 25)
│
├─ Does it involve numbers in range [0,n] or [1,n]?
│   └─ Find missing/duplicate? ──► Cyclic Sort (Pattern 5) or Bit Manipulation (Pattern 20)
│
├─ Does it involve a TREE?
│   ├─ Level-order / layer-by-layer? ──► BFS (Pattern 7)
│   ├─ Path / depth / traversal? ──► DFS (Pattern 8)
│   ├─ Validate BST / k-th smallest / iterator? ──► Inorder DFS, bounds, explicit stack (Pattern 8)
│   ├─ LCA / construct from traversals / serialize? ──► DFS returning nodes or index ranges (Pattern 8)
│   ├─ Best value with "parent and child can't both..."? ──► Tree DP (Pattern 18)
│   └─ Find median / balanced partition? ──► Two Heaps (Pattern 9)
│
├─ Does it involve a GRAPH?
│   ├─ Shortest path (unweighted)? ──► BFS (Pattern 7)
│   ├─ Shortest path, non-negative weights / minimax effort? ──► Dijkstra (Pattern 27)
│   ├─ Shortest path, weights only 0 or 1? ──► 0-1 BFS (Pattern 27)
│   ├─ Shortest path with at most K edges / negative edges? ──► Bellman-Ford (Pattern 27)
│   ├─ Shortest path where the state includes keys / visited set / budget? ──► State-space BFS (Pattern 27)
│   ├─ Start AND goal known, huge branching factor? ──► Bidirectional BFS (Pattern 33)
│   ├─ Ordering / dependencies / DAG / critical path? ──► Topological Sort (Pattern 14)
│   ├─ Use every edge exactly once? ──► Hierholzer / Euler path (Pattern 14)
│   ├─ Connected components? ──► Union Find (Pattern 16) or DFS (Pattern 8)
│   ├─ Two-colouring / odd cycle? ──► Bipartite check: BFS colouring or Union Find (Pattern 16)
│   ├─ Edges or nodes whose removal disconnects the graph? ──► Tarjan low-link (Pattern 8)
│   └─ Explore all paths? ──► DFS (Pattern 8) or Backtracking (Pattern 10)
│
├─ Does it ask for ALL subsets / permutations / combinations?
│   └─ Yes ──► Backtracking (Pattern 10)
│
├─ Subset choice with n <= 40 and LARGE values (sum DP impossible)?
│   └─ Yes ──► Meet-in-the-Middle (Pattern 33)
│
├─ "Minimize the maximum" / "maximize the minimum" / "smallest X such that ..."?
│   └─ Yes, and feasible(X) is monotone ──► Binary Search on the Answer (Pattern 28)
│
├─ Does it ask for TOP K or KTH element?
│   ├─ From single collection? ──► Top K Elements (Pattern 12)
│   └─ From K sorted collections? ──► K-way Merge (Pattern 13)
│
├─ Does it involve NEXT GREATER / SMALLER element?
│   └─ Yes ──► Monotonic Stack (Pattern 15)
│
├─ Does it involve STRING PREFIXES or dictionary lookup?
│   └─ Yes ──► Trie (Pattern 17)
│
├─ Does it ask for OPTIMAL VALUE (min/max/count ways)?
│   ├─ Can you make locally optimal choices that guarantee global optimum? ──► Greedy (Pattern 19)
│   └─ Otherwise ──► Dynamic Programming (Pattern 18), then pick the family:
│       ├─ Merge/remove adjacent items, cost depends on neighbours ──► Interval DP
│       ├─ Tree-shaped input ──► Tree DP (post-order tuples)
│       ├─ Few modes per step (holding / cooldown / k used) ──► State-machine DP
│       ├─ Split into groups with target sums / +- signs ──► Partition (subset-sum) DP
│       ├─ n <= 20 and "visit all / assign all" ──► Bitmask DP
│       └─ Count integers up to 10^18 with a digit property ──► Digit DP
│
├─ Does it involve UNIQUE elements, XOR tricks, or bit-level operations?
│   └─ Yes ──► Bit Manipulation (Pattern 20)
│
├─ Pair / complement / grouping / membership on UNSORTED data, or an O(n) in-place array trick?
│   └─ Yes ──► Hashing & Array Classics (Pattern 22)
│
├─ Does it transform a 2D MATRIX (spiral, rotate, in-place zeroes, sorted-matrix search)?
│   └─ Yes ──► Matrix Manipulation (Pattern 23)
│
├─ Does it involve NESTED brackets, expressions, encoded strings, or paths?
│   └─ Yes ──► Stack-based Parsing (Pattern 24)
│
├─ Does it ask you to DESIGN a class with per-operation complexity targets?
│   └─ Yes ──► Design Problems (Pattern 26)
│
├─ Need sorted order under inserts/deletes (predecessor, successor, rank)?
│   └─ Yes ──► Ordered Containers (Pattern 29)
│
├─ Random pick / shuffle / sample from a stream / weighted choice?
│   └─ Yes ──► Randomized Algorithms (Pattern 31)
│
└─ Huge n (10^9+), primes, GCD, powers, "answer mod 10^9 + 7"?
    └─ Yes ──► Math & Number Theory (Pattern 32)
```

**Tips for pattern identification:**

1. **Read the constraints.** Array size hints at expected complexity: n <= 20 suggests backtracking/bitmask DP, n <= 40 suggests meet-in-the-middle, n <= 10^4 suggests O(n^2), n <= 10^5 suggests O(n log n), n <= 10^7 suggests O(n). Values up to 10^9 with n <= 10^5 and a min/max objective often mean binary search on the answer.
2. **Look for keywords.** "Subarray" = sliding window. "Sorted" = binary search or two pointers. "All/every" = backtracking. "Minimum/maximum/how many" = DP or greedy.
3. **Multiple patterns often combine.** For example, "find middle of linked list" (Fast & Slow) + "reverse second half" (Reversal) + "compare" (Two Pointers) = Palindrome Linked List.
4. **When in doubt between Greedy and DP**, start with greedy (simpler). If you can find a counter-example where the greedy choice fails, switch to DP.

---

## Quick Reference Cheat Sheet

| # | Pattern | Core Idea | Typical Time | Typical Space | Key Data Structure |
|---|---------|-----------|-------------|---------------|-------------------|
| 1 | **Two Pointers** | Converging/diverging pointers on sorted data | O(n) | O(1) | Array |
| 2 | **Sliding Window** | Maintain contiguous window, expand/shrink | O(n) | O(1) to O(k) | Array, HashMap |
| 3 | **Fast & Slow Pointers** | Two speeds detect cycles or find midpoints | O(n) | O(1) | Linked List |
| 4 | **Merge Intervals** | Sort by start, merge overlapping | O(n log n) | O(n) | Array of intervals |
| 5 | **Cyclic Sort** | Place each number at its correct index | O(n) | O(1) | Array with values in [0,n] |
| 6 | **Linked List Reversal** | Three pointers: prev, curr, next | O(n) | O(1) | Linked List |
| 7 | **BFS** | Level-order traversal via queue | O(V + E) | O(V) | Queue |
| 8 | **DFS** | Explore depth-first via recursion/stack | O(V + E) | O(V) | Stack / Recursion |
| 9 | **Two Heaps** | Max-heap (lower half) + min-heap (upper half) | O(n log n) | O(n) | Two Priority Queues |
| 10 | **Backtracking** | Choose → explore → unchoose | O(k^n) or O(n!) | O(n) | Recursion |
| 11 | **Modified Binary Search** | Halve search space each step | O(log n) | O(1) | Sorted Array |
| 12 | **Top K Elements** | Heap of size K | O(n log k) | O(k) | Min/Max Heap |
| 13 | **K-way Merge** | Min-heap of K list heads | O(N log K) | O(K) | Min Heap |
| 14 | **Topological Sort** | Process zero-indegree nodes first (Kahn's) | O(V + E) | O(V + E) | Queue + Adjacency List |
| 15 | **Monotonic Stack** | Maintain increasing/decreasing order on stack | O(n) | O(n) | Stack |
| 16 | **Union Find** | Find root + union with path compression & rank | O(n * a(n)) | O(n) | Parent + Rank arrays |
| 17 | **Trie** | Prefix tree for string operations | O(L) per op | O(ALPHABET * N * L) | Tree of TrieNodes |
| 18 | **Dynamic Programming** | Store subproblem results, build up solution | varies | varies | Array / HashMap |
| 19 | **Greedy** | Locally optimal choice at each step | O(n log n) | O(1) to O(n) | Sorted Array / Heap |
| 20 | **Bit Manipulation** | XOR, AND, OR, shifts for O(1) space tricks | O(n) | O(1) | Integers |
| 21 | **Prefix Sum & Difference Array** | `sum(l..r) = P[r+1] - P[l]`; range add via `D[l] += v, D[r+1] -= v` | O(n) build, O(1) query | O(n) | Array, HashMap of prefixes |
| 22 | **Hashing & Array Classics** | Hash the complement / canonical key; in-place invariants (Kadane, Dutch flag, Boyer–Moore) | O(n) | O(1) to O(n) | HashMap / HashSet |
| 23 | **Matrix Manipulation** | Boundaries, direction vectors, transpose + reflect, in-place markers | O(mn) | O(1) | 2D Array |
| 24 | **Stack-based Parsing** | Push the enclosing context on open, combine on close | O(n) | O(depth) | Stack |
| 25 | **Line Sweep** | Sort +1/-1 events, maintain an active set | O(n log n) | O(n) | Sorted events, Heap, Ordered Map |
| 26 | **Design Problems** | Composite structures kept in sync per operation | O(1) / O(log n) per op | O(n) | HashMap + DLL, Array + Map, Stack |
| 27 | **Weighted Shortest Path** | Dijkstra (non-negative), 0-1 BFS (deque), Bellman-Ford (K hops), BFS on (node, state) | O(E log V) / O(V + E) / O(K·E) | O(V + E) | Min-heap, Deque, Visited over states |
| 28 | **Binary Search on the Answer** | Monotone `feasible(x)`; find first true / last true | O(n log V) | O(1) | Greedy check + binary search |
| 29 | **Ordered Containers** | Balanced BST for predecessor/successor, window order statistics, rank | O(log n) per op | O(n) | `std::set`/`multiset`/`map`, `SortedList`, Fenwick |
| 30 | **String Hashing & Matching** | Rolling hash (verify on match, 2^61-1); KMP prefix function for borders | O(n) / O(n log n) with length search | O(n) | Prefix hashes, `pi` array |
| 31 | **Randomized** | Fisher-Yates, reservoir sampling, prefix sums + bisect, remapping | O(n) build, O(1)–O(log n) per pick | O(1)–O(n) | RNG, Prefix array, Hash map |
| 32 | **Math & Number Theory** | Euclid, fast power, mod 10^9+7 with inverses, sieve, integer sqrt | O(log n) / O(n log log n) | O(1) / O(n) | Integers, Bytearray sieve |
| 33 | **Meet-in-the-Middle & Bidirectional BFS** | Split into halves (2^(n/2) each) and combine; search from both ends | O(2^(n/2) · n) / O(b^(d/2)) | O(2^(n/2)) / O(b^(d/2)) | Sorted sums, Two sets of frontiers |

### Complexity Quick Guide

| If n <= ... | Target complexity | Likely pattern |
|---|---|---|
| 10-12 | O(n! or 2^n) | Backtracking, Bitmask DP |
| 20 | O(2^n * n) | Bitmask DP |
| 40 | O(2^(n/2) * n) | Meet-in-the-Middle |
| 500 | O(n^3) | DP (3D or n^2 with n transitions) |
| 5,000 | O(n^2) | DP, Two Pointers (nested) |
| 100,000 | O(n log n) | Sorting, Binary Search, Heap |
| 1,000,000 | O(n) | Two Pointers, Sliding Window, Greedy |
| 10^9+ | O(log n) or O(1) | Binary Search, Math, Bit Manipulation |
| 10^18 (value of N, count with digit property) | O(digits · states) | Digit DP |
| Values up to 10^9, n up to 10^5, min/max objective | O(n log V) | Binary Search on the Answer |

---

*End of LeetCode Patterns Comprehensive Guide.*
