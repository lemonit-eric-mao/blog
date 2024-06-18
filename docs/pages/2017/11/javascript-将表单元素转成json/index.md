---
title: "JavaScript 将表单元素转成JSON"
date: "2017-11-16"
categories: 
  - "javascript"
---

```javascript
// 获取所有表单数据
var formElement = document.querySelectorAll('div>input');
// 将表单元素添加到JSON
var param = {};

for (var i = 0; i < formElement.length; i++) {
    // 以元素的ID做为json的key, 以元素的value做为json的值. 注意: 以这种方式添加时必须要赋值；例如: 错误的用法 param['key']; 正确的用法 param['key'] = 'value';
    param[formElement[i].id] = formElement[i].value;
}
```
