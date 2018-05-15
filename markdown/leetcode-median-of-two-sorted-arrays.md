title: Leetcode 算法 －4. Median of Two Sorted Arrays
date: 2016-08-17 11:30:12
tags: 
- Leetcode
- Algorithms
- Python
---


> **问题链接**: [4. Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/)

> **问题描述**: There are two sorted arrays nums1 and nums2 of size m and n respectively.
> Find the median of the two sorted arrays. The overall run time complexity should be O(log (m+n)).

`Example 1:`

```python
nums1 = [1, 3]
nums2 = [2]

The median is 2.0
```
`Example 2:`

```python
nums1 = [1, 2]
nums2 = [3, 4]

The median is (2 + 3)/2 = 2.5
```
> **使用语言**: Python

解题思路:  先把列表碾平 , 由于两个列表元素类型相同直接相加即可. 然后排序. 计算中间位置, 可以通过判断奇偶数来分别处理开始index和结束index. 如果长度为奇数则直接返回最中间的， 如果为偶数则返回一个长度为2的list. 计算后返回. **注意:** 计算要使用float类型.


```python
class Solution(object):
    def findMedianSortedArrays(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """
        nums = sorted(nums1 + nums2)
        if len(nums) % 2:
            s = len(nums) / 2
        else:
            s = len(nums) / 2 - 1

        e = len(nums) / 2 + 1

        rs = nums[s:e]
        if len(rs) == 1:
            return rs[0]
        else:
            return sum(rs) / float(2)
```
