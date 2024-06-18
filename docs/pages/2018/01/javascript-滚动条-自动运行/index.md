---
title: "JavaScript 滚动条 自动运行"
date: "2018-01-29"
categories: 
  - "javascript"
---

### 写爬虫时经常遇到懒加载的网站, 所以需要先加载完所有页面数据.

```javascript
var intervalId = setInterval(() => {
    let scrollTop = document.documentElement.scrollTop += 1000;
    let scrollHeight = document.documentElement.scrollHeight;

    if(scrollTop >= scrollHeight) {
        window.clearInterval(intervalId);
        console.log('======到底了!======');
    }
}, 1000);
```
