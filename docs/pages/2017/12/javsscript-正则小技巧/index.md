---
title: "JavsScript 正则小技巧"
date: "2017-12-15"
categories: 
  - "javascript"
---

### 在每一位字符后面添加一个回车

```javascript
var str = '甘井子区';
str.replace(/(.{1})/g,'$1\n');
"甘
井
子
区
"
```
