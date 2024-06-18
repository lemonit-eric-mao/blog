---
title: "Javascript String / Array   includes()"
date: "2018-09-06"
categories: 
  - "javascript"
---

###### 判断数组中是否包含 Array.prototype.includes()

###### includes() 方法用来判断一个数组是否包含一个指定的值，如果是返回 true，否则false。

```javascript
var arr = ['a', 'b', 'c'];

console.log(arr.includes('b'));             // true
console.log(arr.includes('c', 2));        // true
console.log(arr.includes('c', 3));         // false
console.log(arr.includes('c', 100));    // false
```

* * *

* * *

* * *

###### 判断字符串中是否包含 String.prototype.includes()

###### includes() 方法用来判断一个字符串中是否包含一个指定的字符串，如果是返回 true，否则false。

```javascript
var str = 'a1 b2 c3 d4';

console.log(str.includes('a1'));   // true
console.log(str.includes('1 b'));  // true
console.log(str.includes('1b'));   // false
```

* * *

* * *

* * *

###### 遍历数组中对象的某个值，生成新数组 map()

```javascript
var listObject = [
        {
            id: 1,
            name: 'a'
        },
        {
            id: 2,
            name: 'b'
        },
        {
            id: 3,
            name: 'c'
        }
    ];

var newArray = listObject.map((row) => row.name);

console.log(newArray)

// 输出 (3) ["a", "b", "c"]

```

* * *

* * *

* * *
