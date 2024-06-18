---
title: 简单记忆，位移运算
date: '2022-03-14T09:02:14+00:00'
status: private
permalink: /2022/03/14/%e7%ae%80%e5%8d%95%e8%ae%b0%e5%bf%86%ef%bc%8c%e4%bd%8d%e7%a7%bb%e8%bf%90%e7%ae%97
author: 毛巳煜
excerpt: ''
type: post
id: 8361
category:
    - 自学整理
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 个人总结

 程序开发中 左移符号： **``** 、 右移符号： **`>>`** ，要如何去简单的记忆？  
 位移运算，是针对 **二进制的`位数`** ，进行移动，所以左移可以记忆为 **乘以`2`的次数** ，右移可以记忆为 **除以`2`的次数** ，如: **`number  就是number要乘以3次2`** ，如下示例使用不同的语言进行测试

 这里有些注意事项，语言不同，计算的结果也不同，并且在做 **`右移`运算**时 ，**因为是`除法`，会有`精度问题`** 。

- - - - - -

##### 使用JavaScript与Node.js测试

```javascript
// 测试正数
// 左移
console.log(9 > 4)                                  // 6
console.log(100 / 2 / 2 / 2 / 2)                       // 6.25

// 测试负数
// 左移
console.log(-9 > 4)                                 // -7
console.log(-100 / 2 / 2 / 2 / 2)                      // -6.25

```

- - - - - -

##### 使用go语言测试

```go
package main

import (
    "fmt"
)

func main() {
    // 测试正数
    // 左移
    fmt.Println(9 > 4)                              // 6
    fmt.Println(100 / 2 / 2 / 2 / 2)                   // 6

    // 测试负数
    // 左移
    fmt.Println(-9 > 4)                             // -7
    fmt.Println(-100 / 2 / 2 / 2 / 2)                  // -6
}


```

- - - - - -

##### 使用Java语言测试

```java
public static void main(String[] args) {

    // 测试正数
    // 左移
    System.out.println(9 > 4);                      // 6
    System.out.println(100 / 2 / 2 / 2 / 2);           // 6

    // 测试负数
    // 左移
    System.out.println(-9 > 4);                     // -7
    System.out.println(-100 / 2 / 2 / 2 / 2);          // -6

}


```

- - - - - -

- - - - - -

- - - - - -