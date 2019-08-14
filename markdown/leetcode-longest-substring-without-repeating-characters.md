title: Leetcode 算法 －3. Longest Substring Without Repeating Characters
date: 2016-08-17 10:50:12
tags: 
- Leetcode
- Algorithms
- Python
---


> **问题链接**: [3. Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/)

> **问题描述**: Given a string, find the length of the longest substring without repeating characters.

> **Examples:**

> Given "abcabcbb", the answer is "abc", which the length is 3.

> Given "bbbbb", the answer is "b", with the length of 1.

> Given "pwwkew", the answer is "wke", with the length of 3. Note that the answer must be a substring, "pwke" is a subsequence and not a substring.

> **使用语言**: Python

此题有点饶, 需要一组hash表记录字符的索引. 

我们以`ababcbb`为例说明, 这里hash表的值-1是初始值, 这样在方便做+1操作. `index` 作为开始索引值, 起初index为0， 这是理所当然的。当遍历到第二个`a` `index`就成了2了, 同时把ab重置为初始值.   max_len为一个刷新最高值的变量. 通过当前索引 - index + 1计算(当再次迭代到c的时候, 此时i为4, index为2, 则: `4-2+1=3` ). 每次比上一次max_len大的时候更新此值. 保证max_len是最大的.

重置hash表初始值的逻辑是: 

- 当此字符在hash表中的值不是-1(即不是初始值)
- 此字符之前的所有字符hash表的值都会重置(比如上面遍历到第二个a是 0-2之间的ab都重置了 )
- 在重置之前的字符索引值的时候把index增加到当前索引位置数.

刷新max_len逻辑

- 当此字符在hash表中的值是-1
- 计算公式: **当前索引 - index + 1**

```python
class Solution(object):
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """

        index = 0
        max_len = 0
        d = {}

        for i in s:
            d[i] = -1

        for i in range(len(s)):
            # 重置hash表初始值的逻辑
            # 当此字符在hash表中的值不是-1
            if d[s[i]] != -1:
                while index <= d[s[i]]:
                    #此字符之前的所有字符hash表的值都会重置 
                    d[s[index]] = -1

                    #在重置之前的字符索引值的时候把index增加到当前索引位置数.
                    index += 1

            # 刷新max逻辑
            if i - index + 1 > max_len:
                max_len = i - index + 1

            d[s[i]] = i

        return max_len
```
