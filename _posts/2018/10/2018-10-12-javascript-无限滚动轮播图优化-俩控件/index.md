---
title: "JavaScript 无限滚动轮播图优化 (俩控件)"
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
        for (let i = 0; i < 2; i++) {
            // 动态生成图片
            let imgTag = document.createElement('img');
            imgTag.src = urls[i];
            imgTag.style.position = 'absolute';
            imgTag.style.width = `${currentWidth}px`;
            imgTag.style.height = '500px';
            imgTag.style.left = `${currentWidth * i}px`;
            banner.appendChild(imgTag);
        }
    }

    init();

    /**
     * 向左移动
     */
    const leftMove = () => {

        // 将中间与辅助图片控件的位置, 每次向左移动 50px
        banner.children[0].style.left = `${parseInt(banner.children[0].style.left) - 50}px`;
        banner.children[1].style.left = `${parseInt(banner.children[1].style.left) - 50}px`;

        let temp;
        if (parseInt(banner.children[0].style.left) > -currentWidth) {
            // 执行H5动画事件
            temp = requestAnimationFrame(leftMove);
        } else {
            // 停止动画
            cancelAnimationFrame(temp);
            // 动画结束后，调换两个控件的位置
            banner.appendChild(banner.children[0]);
            // 动画结束后，辅助控件位置回归到右边
            banner.children[1].style.left = `${currentWidth}px`;

            // TODO 动画结束后，更新辅助控件的图片地址
            urls.push(urls.shift());
            banner.children[1].src = urls[1];
        }
    }

    /**
     * 左侧按钮点击事件
     */
    const leftBtnClick = () => {
        // 强制将辅助控件移到右边
        banner.children[1].style.left = `${currentWidth}px`;
        // 执行移动动画
        leftMove();
    }

    /**
     * 向右移动
     */
    const rightMove = () => {
        // 将辅助与中间图片控件的位置, 每次向右移动 50px
        banner.children[0].style.left = `${parseInt(banner.children[0].style.left) + 50}px`;
        banner.children[1].style.left = `${parseInt(banner.children[1].style.left) + 50}px`;

        let temp;
        if (parseInt(banner.children[1].style.left) < 0) {
            // 执行H5动画事件
            temp = requestAnimationFrame(rightMove);
        } else {
            // 停止动画
            cancelAnimationFrame(temp);
            // 动画结束后，调整控件顺序
            banner.appendChild(banner.children[0]);
            // 动画结束后，辅助控件位置回归到左边
            banner.children[1].style.left = `${-currentWidth}px`;
        }
    }

    /**
     * 右侧按钮点击事件
     */
    const rightBtnClick = () => {
        // 强制将辅助控件移到左边
        banner.children[1].style.left = `${-currentWidth}px`;

        // TODO 更新辅助控件的图片地址
        urls.unshift(urls.pop());
        banner.children[1].src = urls[0];

        // 执行移动动画
        rightMove();
    }
```

```markup
</script>
</body>
</html>
```
