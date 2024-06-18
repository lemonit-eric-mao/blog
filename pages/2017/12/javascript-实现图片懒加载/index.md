---
title: "JavaScript 实现图片懒加载"
date: "2017-12-01"
categories: 
  - "javascript"
---

```javascript
/**
 * 思路: 获取当前img的相对于文档顶的偏移距离减去 pageYOffset 的距离，
 * 然后和浏览器窗口高度在进行比较，
 * 如果小于浏览器窗口则出现在了可视区域内了，
 * 反之，则没有。
 * Created by mao-siyu on 17-3-9.
 */

// 浏览器窗口高度
var clientHeight;
var modules;
var imageStatus = [];

/**
 * @constructor
 */
var ITF_lazyload = function () {
}

/**
 * 载入要加载的图片所在模块
 * @param lazyId
 */
ITF_lazyload.images = function (moduleClass) {
    modules = document.getElementsByClassName(moduleClass);
}

/**
 * 监听滚动条滚动事件
 */
ITF_lazyload.scroll = function () {
    clientHeight = document.documentElement.clientHeight;
    for (var i = 0, len = modules.length; i < len; i++) {
        // 如果小于浏览器窗口则出现在了可视区域内了
        var result = modules[i].offsetTop - this.pageYOffset;
        // 反之, 则没有显示
        if (result > clientHeight)
            return;
        // 判断元素的位置是否未记录
        if (!imageStatus.contains(i)) {
            var images = modules[i].querySelectorAll('img');
            for (var j = 0, len = images.length; j < len; j++) {
                var src = images[j].getAttribute('data-src');
                images[j].setAttribute('src', src);
            }
            // 记录元素位置
            imageStatus.push(i);
        }
    }


}
// 监听滚动条滚动事件
window.addEventListener('scroll', ITF_lazyload.scroll, false);

Array.prototype.contains = function (obj) {
    var i = this.length;
    while (i--) {
        if (this[i] === obj) {
            return true;
        }
    }
    return false;
}

/**
 * 应用案例
 * moduleClass 包裹图片的模块
 * ITF_lazyload.images('moduleClass');
 */
```
