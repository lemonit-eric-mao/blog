---
title: "JavaScript 无限滚动轮播图优化 (仨控件)"
date: "2018-10-12"
categories: 
  - "javascript"
---

##### JavaScript无限滚动轮播图优化

`为保留思路， 代码未优化！`

```markup
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>无限滚动轮播图优化</title>
    <style>
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

```markup
    </style>
</head>

<body>

<div class="container">
    <!--这里面会动态放图片-->
    <div class="banner" id="banner"></div>
    <div class="left-button" onclick="leftBtnClick()">左侧按钮</div>
    <div class="right-button" onclick="rightBtnClick()">右侧按钮</div>
</div>
<script>
```

```javascript
    let urls = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.png'];
    // 当前屏幕宽/高
    let currentWidth = document.body.offsetWidth;
    // banner容器
    let banner = document.getElementById('banner');

    /**
     * 初始化
     */
    function init() {
        // 循环创建图片
        for (let i = 0; i < 3; i++) {
            // 动态生成图片
            let imgTag = document.createElement('img');
            imgTag.setAttribute('index', i);
            imgTag.src = urls[i];
            imgTag.style.position = 'absolute';
            imgTag.style.width = `${currentWidth}px`;
            imgTag.style.height = '500px';
            imgTag.style.left = `${currentWidth * i - currentWidth}px`;
            banner.appendChild(imgTag);
        }
    }

    init();

    /**
     * 向左移动
     */
    let leftMove = () => {

        // 将中间与右侧图片控件的位置, 每次向左移动 50px
        banner.children[1].style.left = `${parseInt(banner.children[1].style.left) - 50}px`;
        banner.children[2].style.left = `${parseInt(banner.children[2].style.left) - 50}px`;

        let temp;
        if (parseInt(banner.children[1].style.left) > -currentWidth) {
            // 执行H5动画事件
            temp = requestAnimationFrame(leftMove);
        } else {
            // 停止动画
            cancelAnimationFrame(temp);
            // 重置所有图片位置
            banner.children[0].style.left = `${currentWidth}px`;
            banner.children[1].style.left = `${-currentWidth}px`;
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
        banner.children[0].style.left = `${parseInt(banner.children[0].style.left) + 50}px`;
        banner.children[1].style.left = `${parseInt(banner.children[1].style.left) + 50}px`;

        let temp;
        if (parseInt(banner.children[0].style.left) < 0) {
            // 执行H5动画事件
            temp = requestAnimationFrame(rightMove);
        } else {
            // 停止动画
            cancelAnimationFrame(temp);
            // 重置所有图片位置
            banner.children[0].style.left = `0px`;
            banner.children[1].style.left = `${currentWidth}px`;
            banner.children[2].style.left = `${-currentWidth}px`;
            // 删除并返回数组的最后一个元素， 将其添加到开头
            urls.unshift(urls.pop());
            // 更新右侧控件的图片地址
            banner.children[2].src = urls[0];
            // 调整控件顺序
            banner.insertBefore(banner.children[2], banner.childNodes[0]);
        }
    }

    /**
     * 左侧按钮点击事件
     */
    const leftBtnClick = () => {
        leftMove();
    }

    /**
     * 右侧按钮点击事件
     */
    const rightBtnClick = () => {
        rightMove();
    }
```

```markup
</script>
</body>
</html>
```
