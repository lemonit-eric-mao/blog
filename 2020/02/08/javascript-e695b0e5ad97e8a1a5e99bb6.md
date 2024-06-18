---
title: 'JavaScript 数字补零'
date: '2020-02-08T15:43:00+00:00'
status: publish
permalink: /2020/02/08/javascript-%e6%95%b0%e5%ad%97%e8%a1%a5%e9%9b%b6
author: 毛巳煜
excerpt: ''
type: post
id: 5248
category:
    - JavaScript
tag: []
post_format: []
---
##### 定义 zfill 函数，添加到String的原型链上，提供给所有字符串使用

```javascript
String.prototype.zfill = function (num) {
    // 大于补零数，直接返回结果
    if (this.length >= num)
        return this.toString();
    return Array(num + 1 - this.length).join(0) + this.toString();
}

```

###### 测试

```javascript
'16'.zfill(6)
输出："000016"

'168'.zfill(6)
输出："000168"

```

###### 解释

1. 创建空数组，数组长度为 `补零数 + 1 - 数字长度 + 数字本身`
2. 为什么 补零数 + 1，因为`jion(0)`函数起到`以0做拼接符`来拼接空数组的作用，生成的0比预期的少了一个  
  **例如：**

```javascript
// 期望6个0
Array(6).join(0)
// 实际5个0
"00000"

```