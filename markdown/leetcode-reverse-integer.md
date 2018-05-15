title: Leetcode 算法 － 7. Reverse Integer
date: 2016-08-17 13:50:45
tags:
- Leetcode
- Algorithms
- Python
---


> **问题链接**: [7. Reverse Integer](https://leetcode.com/problems/reverse-integer/)

> **问题描述**: Reverse digits of an integer.

> Example1: `x = 123, return 321`

> Example2: `x = -123, return -321`

> **Update (2014-11-10)**: Test cases had been added to test the overflow behavior.


**注意点:** 此问题在2014-11-10有更新， 加入了对溢出的控制, 当出现溢出则返回为0. 而Python中没有溢出的行为, 所以为了Accepted, 加入了bit_length 判断. 长度为32或以上直接返回为0

```python
class Solution(object):
    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        
        answer = 0
        sign = 1 if x > 0 else -1
        x = abs(x)
        while x > 0:
            answer = answer * 10 + x % 10
            x /= 10
            
            # update 2014-11-10
            if answer.bit_length() >= 32:
                return 0
                
        return sign * answer

```

起初我用的是转成字符串然后转成list倒序拼接, 虽然可以Accepted, 但总觉得开销大, 而且不规范, 后来两个解法速度测试后的确这个解法开销大. 顺便附上起初我的错误解答. 大家可以感受下.

```python
class Solution(object):
    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
		value = ''.join([ str(abs(x))[i] for i in range(len(str(abs(x))) - 1, -1, -1) ])
        if x > 0:
            number = int(value)
        else:
            number = -int(value)
            
        if number.bit_length() >= 32:
            return 0
        else:
            return number

```