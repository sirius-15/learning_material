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
21. [Pattern Selection Flowchart](#pattern-selection-flowchart)
22. [Quick Reference Cheat Sheet](#quick-reference-cheat-sheet)

---

## How to Use This Guide

Most LeetCode problems map to one or more recurring **patterns**. Instead of memorising hundreds of individual solutions, learn the ~20 core patterns and you will be able to recognise and solve the vast majority of interview problems.

**For each pattern you will find:**

| Section | What it contains |
|---|---|
| **Overview** | Core idea in plain language |
| **When to Use** | Signals in the problem statement that hint at this pattern |
| **Template Code** | Copy-paste-ready skeleton (Python + C++) |
| **Variations** | Sub-patterns or alternate forms |
| **Common Mistakes** | Pitfalls and how to avoid them |
| **Related Patterns** | Cross-references to complementary patterns |
| **Example Problems** | 4-5 problems graded Easy → Hard, each with intuition, full solution, and complexity analysis |

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

### Common Mistakes

- **Not correctly shrinking the window** — forgetting to advance `left` or using a wrong shrink condition leads to infinite loops or wrong answers.
- **Off-by-one when calculating window size** — the size of a window from index `left` to `right` inclusive is `right - left + 1`, not `right - left`.
- **Forgetting to update state when shrinking** — when `left` advances, the hashmap/counter/sum must be updated to remove the element at the old `left`.
- **Confusing expand vs. shrink conditions** — expanding happens unconditionally each iteration; shrinking happens only while a constraint is violated (use `while`, not `if`).

### Related Patterns

- **Two Pointers** — Sliding Window is a specialized form of two pointers where both move in the same direction.
- **Monotonic Queue** — Used inside a sliding window to track min/max efficiently.
- **Hashing** — Hashmaps are frequently used inside the window to count frequencies.

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

## Pattern Selection Flowchart

Use this decision tree when you encounter a new problem and need to identify which pattern to apply.

```
START: Read the problem statement
│
├─ Does it involve a SORTED array or searching?
│   ├─ Yes: Need to find a specific element? ──► Binary Search (Pattern 11)
│   ├─ Yes: Need to find a pair/triplet summing to target? ──► Two Pointers (Pattern 1)
│   └─ Yes: Array is rotated? ──► Modified Binary Search (Pattern 11)
│
├─ Does it involve CONTIGUOUS subarrays or substrings?
│   ├─ Yes: Fixed window size? ──► Sliding Window - Fixed (Pattern 2)
│   └─ Yes: Variable window / longest / shortest? ──► Sliding Window - Dynamic (Pattern 2)
│
├─ Does it involve a LINKED LIST?
│   ├─ Detect cycle or find middle? ──► Fast & Slow Pointers (Pattern 3)
│   └─ Reverse all or part? ──► In-place Linked List Reversal (Pattern 6)
│
├─ Does it involve INTERVALS (time ranges, schedules)?
│   └─ Yes ──► Merge Intervals (Pattern 4)
│
├─ Does it involve numbers in range [0,n] or [1,n]?
│   └─ Find missing/duplicate? ──► Cyclic Sort (Pattern 5) or Bit Manipulation (Pattern 20)
│
├─ Does it involve a TREE?
│   ├─ Level-order / layer-by-layer? ──► BFS (Pattern 7)
│   ├─ Path / depth / traversal? ──► DFS (Pattern 8)
│   └─ Find median / balanced partition? ──► Two Heaps (Pattern 9)
│
├─ Does it involve a GRAPH?
│   ├─ Shortest path (unweighted)? ──► BFS (Pattern 7)
│   ├─ Ordering / dependencies / DAG? ──► Topological Sort (Pattern 14)
│   ├─ Connected components? ──► Union Find (Pattern 16) or DFS (Pattern 8)
│   └─ Explore all paths? ──► DFS (Pattern 8) or Backtracking (Pattern 10)
│
├─ Does it ask for ALL subsets / permutations / combinations?
│   └─ Yes ──► Backtracking (Pattern 10)
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
│   └─ Otherwise ──► Dynamic Programming (Pattern 18)
│
└─ Does it involve UNIQUE elements, XOR tricks, or bit-level operations?
    └─ Yes ──► Bit Manipulation (Pattern 20)
```

**Tips for pattern identification:**

1. **Read the constraints.** Array size hints at expected complexity: n <= 20 suggests backtracking/bitmask DP, n <= 10^4 suggests O(n^2), n <= 10^5 suggests O(n log n), n <= 10^7 suggests O(n).
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

### Complexity Quick Guide

| If n <= ... | Target complexity | Likely pattern |
|---|---|---|
| 10-12 | O(n! or 2^n) | Backtracking, Bitmask DP |
| 20 | O(2^n * n) | Bitmask DP |
| 500 | O(n^3) | DP (3D or n^2 with n transitions) |
| 5,000 | O(n^2) | DP, Two Pointers (nested) |
| 100,000 | O(n log n) | Sorting, Binary Search, Heap |
| 1,000,000 | O(n) | Two Pointers, Sliding Window, Greedy |
| 10^9+ | O(log n) or O(1) | Binary Search, Math, Bit Manipulation |

---

*End of LeetCode Patterns Comprehensive Guide.*
