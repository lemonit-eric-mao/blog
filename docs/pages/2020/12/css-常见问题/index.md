---
title: "CSS 常见问题"
date: "2020-12-15"
categories: 
  - "css"
---

###### this is a box

```markup
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>this is a box</title>
    <style>
        div {
            width: 200px;
            border-radius: 15px;
            border-color: #0f9988 #0f9988 red #0f9988;
            border-width: 3px;
            box-shadow: 10px 10px 5px #888888;
            border-style: dotted solid dashed double;
            padding: 20px;
        }

        div:last-child {
            background-color: darkorange;
        }
    </style>
</head>
<body>
<div>this is a box</div>
<div></div>
<div></div>
</body>
</html>
```

* * *

* * *

* * *

###### 监听css3动画结束事件

```css
// 监听css3动画结束事件
dialog.addEventListener('webkitAnimationEnd', () => {
    console.log('动画结束');
});
```

* * *

* * *

* * *

###### 固定定位当前层居中，做法

```css
div {
            /*当前层大小*/
            width: 80vw;
            height: 80vh;
            /*固定定位*/
            position: fixed;
            top: 50%;
            left: 50%;
            /*当前层居中*/
            margin-top: -40vh;
            margin-left: -40vw;
}
```

* * *

* * *

* * *

###### 动画实现思路

```css
    <!-- 层缩放 动画 -->
    <style>
        @keyframes minimize {
            /*从当前正常的比例*/
            from {
                transform: scale(1, 1);
            }
            /*缩放到当前比例的1%*/
            to {
                /*transform属性它们的执行顺序是从后向前执行的， 先执行scale， 在执行 translate*/
                transform: translate(-55%, 55%) scale(0.1, 0.1);
            }
        }

        @keyframes recovery {
            /*从当前缩放的比例*/
            from {
                transform: translate(-55%, 55%) scale(0.1, 0.1);
            }
            /*恢复到正常的比例*/
            to {
                transform: scale(1, 1);
            }
        }
    </style>

    /*样式*/
    <style>
        /*对话框 初始样式*/
        .dl-foundation > .dl-wrapper > .dl-dialog {
            /*当前层大小*/
            width: 80vw;
            height: 80vh;
            /*固定定位*/
            position: fixed;
            top: 50%;
            left: 50%;
            /*当前层居中*/
            margin-top: -40vh;
            margin-left: -40vw;
            /*标识恢复元素鼠标事件*/
            pointer-events: auto;
            background-color: #FFF;
            display: flex;
            /**
             * 让子层垂直显示
             *     row                                 默认值。灵活的项目将水平显示，正如一个行一样
             *     row-reverse                与 row 相同，但是以相反的顺序
             *     column                         灵活的项目将垂直显示，正如一个列一样
             *     column-reverse        与 column 相同，但是以相反的顺序
             */
            flex-direction: column;
            /**
             * stretch： 标识子层全是100%
             * center： 标识子层用多少占多少并且居中
             */
            align-items: stretch;
        }

        /*对话框 最小化样式*/
        .dl-foundation > .dl-wrapper > .dl-dialog-minimize {
            /*最小化动画*/
            animation: minimize 1s;
            /*transform属性它们的执行顺序是从后向前执行的， 先执行scale， 在执行 translate*/
            transform: translate(-55%, 55%) scale(0.1, 0.1);
        }

        /*对话框 复原样式*/
        .dl-foundation > .dl-wrapper > .dl-dialog-recovery {
            /*复原动画*/
            animation: recovery 1s;
            transform: scale(1, 1);
        }
    </style>
```

* * *

* * *

* * *
