---
title: "JavaScript 去除数组中所有的空数据"
date: "2017-11-16"
categories: 
  - "javascript"
---

### 错误的写法

```javascript
var arr = [1, 23, 4, 5, "", 345, 34, "", 5, 4, "", "", "", "", 32, "", "", "", 666];
for (var i = 0; i < arr.length; i++) {
    if (!arr[i])
        console.log(arr.splice(i, 1));
}
arr; // (13) [1, 23, 4, 5, 345, 34, 5, 4, "", "", 32, "", 666]
```

### 正确的写法

```javascript
var arr = [1, 23, 4, 5, "", 345, 34, "", 5, 4, "", "", "", "", 32, "", "", "", 666];
var length = arr.length;
while (length > 0) {
    var temp = arr.shift();
    if (temp)
        arr.push(temp);
    length--;
}
arr; // (10) [1, 23, 4, 5, 345, 34, 5, 4, 32, 666]
```

### 原因

`使用splice(i, 1)方法删除数组元素时, 数组长度会改变, 导致for循环时, 索引与数组的元素位置错乱.`
