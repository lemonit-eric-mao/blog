---
title: "JavaScript 事件冒泡"
date: "2017-11-27"
categories: 
  - "javascript"
---

## 引发的问题

**条件1: 父div默认样式点击后会变色; 条件2: 分享div点击后触分享事件; 当点击分享时, 父div的样式也会被触发, 这当然不是期望的结果, 所以解决这个问题就是需要用法javaScript的 事件冒泡函数.**

```markup
<div class="parent">
    <div class="ui inverted right floated violet button" onclick="quesShare()">分享</div>
</div>
```

```javascript
    /**
     * 分享问卷
     * @param obj
     */
    const quesShare = () => {
        // 禁止事件冒泡
        this.event.stopPropagation();
    }
```
