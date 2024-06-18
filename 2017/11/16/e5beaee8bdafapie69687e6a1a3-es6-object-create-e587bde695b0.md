---
title: '微软API文档 ES6 Object.create 函数'
date: '2017-11-16T10:02:29+00:00'
status: publish
permalink: /2017/11/16/%e5%be%ae%e8%bd%afapi%e6%96%87%e6%a1%a3-es6-object-create-%e5%87%bd%e6%95%b0
author: 毛巳煜
excerpt: ''
type: post
id: 38
category:
    - JavaScript
tag: []
post_format: []
---
### **Object.create 函数 (JavaScript)**

创建一个具有指定原型且可选择性地包含指定属性的对象。

#### **语法**

Object.create(prototype, descriptors)

#### **参数**

**prototype**  
必需。 要用作原型的对象。 可以为 null。

**descriptors**  
可选。 包含一个或多个属性描述符的 JavaScript 对象。  
“数据属性”是可获取且可设置值的属性。 数据属性描述符包含 value 特性，以及 writable、enumerable 和 configurable 特性。 如果未指定最后三个特性，则它们默认为 false。 只要检索或设置该值，“访问器属性”就会调用用户提供的函数。 访问器属性描述符包含 set 特性和/或 get 特性。 有关详细信息，请参阅 Object.defineProperty 函数 (JavaScript)。

#### **返回值**

一个具有指定的内部原型且包含指定的属性（如果有）的新对象。

#### **异常**

如果满足下列任一条件，则将引发 TypeError 异常：

- prototype 参数不是对象且不为 null。
- descriptors 参数中的描述符具有 value 或 writable 特性，并具有 get 或 set 特性。
- descriptors 参数中的描述符具有不为函数的 get 或 set 特性。

**详情** [查看微软API文档](https://msdn.microsoft.com/zh-cn/library/ff925952)