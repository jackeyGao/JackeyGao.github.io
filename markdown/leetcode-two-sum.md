title: Leetcode 算法 － 1. Two Sum
date: 2016-08-16 09:50:45
tags:
- Leetcode
- Algorithms
- Python
---


> **问题链接**: [1. Two Sum](https://leetcode.com/problems/two-sum/)

> **问题描述**: Given an array of integers, return indices of the two numbers such that they add up to a specific target.

> You may assume that each input would have exactly one solution.

**Example:**

```python
Given nums = [2, 7, 11, 15], target = 9,

Because nums[0] + nums[1] = 2 + 7 = 9,
return [0, 1].
```

> **UPDATE (2016/2/13)**: The return format had been changed to zero-based indices. Please read the above updated description carefully.


这是我解的第一道题， 当时就懵比了, 写了若干方法均超时了. 最后到网上搜索的答案. 需要用哈希表, python 字典其实就是哈希表的实现. **感受下哈希表的使用场景， 后面更多的解题都需要哈希表来完成.**

```python
class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        d = {}
        for i, _ in enumerate(nums):
            x = nums[i]
            if target - x in d:
                return i, d[target - x]
            d[x] = i
```