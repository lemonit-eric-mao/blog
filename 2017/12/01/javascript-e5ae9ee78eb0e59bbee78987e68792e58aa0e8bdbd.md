---
title: 'JavaScript 实现图片懒加载'
date: '2017-12-01T14:04:33+00:00'
status: publish
permalink: /2017/12/01/javascript-%e5%ae%9e%e7%8e%b0%e5%9b%be%e7%89%87%e6%87%92%e5%8a%a0%e8%bd%bd
author: 毛巳煜
excerpt: ''
type: post
id: 1704
category:
    - JavaScript
tag: []
post_format: []
hestia_layout_select:
    - default
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
    for (var i = 0, len = modules.length; i  clientHeight)
            return;
        // 判断元素的位置是否未记录
        if (!imageStatus.contains(i)) {
            var images = modules[i].querySelectorAll('img');
            for (var j = 0, len = images.length; j 
```