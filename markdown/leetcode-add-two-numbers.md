title: Leetcode 算法 － 2. Add Two Numbers
date: 2016-08-16 17:30:01
tags: 
- Leetcode
- Algorithms
- Python
---


> **问题链接**: [2. Add Two Numbers](https://leetcode.com/problems/add-two-numbers/)

> **问题描述**: You are given two linked lists representing two non-negative numbers. The digits are stored in reverse order and each of their nodes contain a single digit. Add the two numbers and return it as a linked list.

> Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)

> Output: 7 -> 0 -> 8

> **使用语言**: Python

需要注意的是: 这里使用的ListNode不是Python内置的list对象, 而是传统(计算机科学)意义上的列表, 通常叫做**Linked list**(链表), 通常由一系列节点实现, 其每个节点中都持有一个指向下一个节点的引用. 这里就是next属性. 链表分为单向链表和双向链表. 双向链表持有一个指向前一节点的引用.


```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        x1, x2 = l1, l2
        results = ListNode(0)
        p = results
        while True:
            if not x1 and not x2 and not p.next:
                break
        
            if p.next:
                c = getattr(x1, 'val', 0) + getattr(x2, 'val', 0) + flag.next.val
            else:
                c = getattr(x1, 'val', 0) + getattr(x2, 'val', 0)
        
            flag = ListNode(c % 10)
        
            if c >= 10:
                flag.next = ListNode(c / 10)
        
            p.next = flag
            p = flag
        
            x1 = x1.next if isinstance(x1, ListNode) else None
            x2 = x2.next if isinstance(x2, ListNode) else None
        
        return results.next        
```
