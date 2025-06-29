---
title: "Leetcode Hot 100 Part 1"
date: 2024-10-14 16:02:24 +0800
categories: [Algorithm]
tags: [leetcode]
pin: false
---

## H1-5

### 1.哈希:两数之和

[https://leetcode.cn/problems/two-sum/description/?envType=study-plan-v2&envId=top-100-liked](https://leetcode.cn/problems/two-sum/description/?envType=study-plan-v2&envId=top-100-liked)

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        hashtable = dict()
        for i,num in enumerate(nums):
            if target-num in hashtable:
                return [hashtable[target-num], i]
            hashtable[num] = i
        return []
```

时间On, 空间On

### 2.哈希:字母异位词分组

[https://leetcode.cn/problems/group-anagrams/description/?envType=study-plan-v2&envId=top-100-liked](https://leetcode.cn/problems/group-anagrams/description/?envType=study-plan-v2&envId=top-100-liked)

```python
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        d= defaultdict(list)
        for s in strs:
            d[''.join(sorted(s))].append(s)
        return list(d.values())
```

题解:[https://leetcode.cn/problems/group-anagrams/?envType=study-plan-v2&envId=top-100-liked](https://leetcode.cn/problems/group-anagrams/?envType=study-plan-v2&envId=top-100-liked)

时间O(*nm*log*m*), 空间O(*nm*)

### 3.哈希:最长连续序列

[https://leetcode.cn/problems/longest-consecutive-sequence/description/?envType=study-plan-v2&envId=top-100-liked](https://leetcode.cn/problems/longest-consecutive-sequence/description/?envType=study-plan-v2&envId=top-100-liked)

```python
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        res = 0
        st = set(nums)
        for l in st:
            if l- 1 in st:
                continue
            r = l +1
            while r in st:
                r += 1
            res = max(res, r-l)
        return res
```

题解:[https://leetcode.cn/problems/longest-consecutive-sequence/solutions/3005726/ha-xi-biao-on-zuo-fa-pythonjavacgojsrust-whop/?envType=study-plan-v2&envId=top-100-liked](https://leetcode.cn/problems/longest-consecutive-sequence/solutions/3005726/ha-xi-biao-on-zuo-fa-pythonjavacgojsrust-whop/?envType=study-plan-v2&envId=top-100-liked)

时间On, 空间On
