---
title: 'JavaScript 无限滚动轮播图优化 (仨控件)'
date: '2018-10-12T14:48:04+00:00'
status: publish
permalink: /2018/10/12/javascript-%e6%97%a0%e9%99%90%e6%bb%9a%e5%8a%a8%e8%bd%ae%e6%92%ad%e5%9b%be%e4%bc%98%e5%8c%96
author: 毛巳煜
excerpt: ''
type: post
id: 3210
category:
    - JavaScript
tag: []
post_format: []
---
##### JavaScript无限滚动轮播图优化

`为保留思路， 代码未优化！`

```
<pre data-language="HTML">```markup



    <meta charset="UTF-8"></meta>
    <title>无限滚动轮播图优化</title>
    <style>
</style>
```
```

```css
        html, body, div, img, ul, li {
            margin: 0px;
            padding: 0px;
        }

        .container {
        }

        .left-button {
            position: absolute;
            width: 20px;
            float: left;
        }

        .banner {
            position: absolute;
        }

        .right-button {
            position: absolute;
            width: 20px;
            left: 98%;
            float: right;
        }

```

```
<pre data-language="HTML">```markup
    




<div class="container">
    
    <div class="banner" id="banner"></div>
    <div class="left-button" onclick="leftBtnClick()">左侧按钮</div>
    <div class="right-button" onclick="rightBtnClick()">右侧按钮</div>
</div>
<script>
</script>
```
```

```javascript
<br></br>    let urls = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.png'];
    // 当前屏幕宽/高
    let currentWidth = document.body.offsetWidth;
    // banner容器
    let banner = document.getElementById('banner');

    /**
     * 初始化
     */
    function init() {
        // 循环创建图片
        for (let i = 0; i  {

        // 将中间与右侧图片控件的位置, 每次向左移动 50px
        banner.children[1].style.left = `<span class="katex math inline">{parseInt(banner.children[1].style.left) - 50}px`;
        banner.children[2].style.left = `</span>{parseInt(banner.children[2].style.left) - 50}px`;

        let temp;
        if (parseInt(banner.children[1].style.left) > -currentWidth) {
            // 执行H5动画事件
            temp = requestAnimationFrame(leftMove);
        } else {
            // 停止动画
            cancelAnimationFrame(temp);
            // 重置所有图片位置
            banner.children[0].style.left = `<span class="katex math inline">{currentWidth}px`;
            banner.children[1].style.left = `</span>{-currentWidth}px`;
            banner.children[2].style.left = `0px`;
            // 删除并返回数组的第一个元素， 将其添加到末尾
            urls.push(urls.shift());
            // 更新左侧控件的图片地址
            banner.children[0].src = urls[2];
            // 调整控件顺序
            banner.appendChild(banner.children[0]);
        }
    }

    /**
     * 向右移动
     */
    const rightMove = () => {
        // 将左侧与中间图片控件的位置, 每次向右移动 50px
        banner.children[0].style.left = `<span class="katex math inline">{parseInt(banner.children[0].style.left) + 50}px`;
        banner.children[1].style.left = `</span>{parseInt(banner.children[1].style.left) + 50}px`;

        let temp;
        if (parseInt(banner.children[0].style.left)  {
        leftMove();
    }

    /**
     * 右侧按钮点击事件
     */
    const rightBtnClick = () => {
        rightMove();
    }

```

```
<pre data-language="HTML">```markup




```
```