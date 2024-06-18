---
title: "JavaScript 判断对象中是否存在 相匹配的属性"
date: "2018-08-25"
categories: 
  - "javascript"
---

#### 判断对象中是否存在 相匹配的属性

```javascript
var errorMsg =  {
    '400': '用户名或密码不存在!',
    '401': '用户名或密码不存在!'
}

errorMsg.hasOwnProperty(401);
true
errorMsg.hasOwnProperty(402);
false

401 in errorMsg
true
402 in errorMsg
false
```
