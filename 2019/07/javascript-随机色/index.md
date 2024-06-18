---
title: "Javascript 随机色"
date: "2019-07-29"
categories: 
  - "javascript"
---

##### 使用 js 生成随机色

```javascript
document.body.style.color = `#${Math.floor(Math.random() * 0xffffff).toString(16)}`;
```
