---
title: "JavaScript 拖拽改变Dom元素宽度"
date: "2021-02-01"
categories: 
  - "javascript"
---

```javascript
<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title></title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        html, body {
            padding: 0;
            margin: 0;
            border: 0;
            font-size: 14px;
            width: 100%;
            height: 100%;
        }

        .layout {
            position: relative;
            width: 100%;
            height: 100%;
        }

        .left-layout {
            background-color: #a6a9ff;
            position: absolute;
            /* 绝对定位情况 [上 下 左 右]充满*/
            top: 0;
            bottom: 0;
            left: 0;
            right: 0;
            width: 10%;
        }

        .drap-line {
            background-color: #999;
            position: absolute;
            top: 0;
            bottom: 0;
            right: 0;
            width: 4px;
            z-index: 7;
            cursor: ew-resize;
        }

        .right-layout {
            background-color: #26b58f;
            position: absolute;
            top: 0;
            bottom: 0;
            right: 0;
            width: 90%;
        }
    </style>
</head>

<body>
<div class="layout">
    <div class="top">顶部导航</div>
    <div id="leftLayout" class="left-layout">
        <div id="menu">
            <span>待拖拽的div</span>
        </div>
        <div id="drapLine" class="drap-line"></div>
    </div>
    <div id="rightLayout" class="right-layout">
        右边的div
    </div>
</div>
<script>

    // 获取dom
    let drapLine = document.getElementById('drapLine');
    let leftLayout = document.getElementById('leftLayout');
    let rightLayout = document.getElementById('rightLayout');

    window.onload = () => {

        // 计算右侧布局，初始的宽度
        let rightOffsetWidth = rightLayout.clientWidth + leftLayout.clientWidth;

        // 初始时读取localStorage保存的数据
        let layout = localStorage.getItem('layout');
        if (layout) {
            layout = JSON.parse(layout);
            leftLayout.style.width = layout.leftLayout;
            rightLayout.style.width = layout.rightLayout;
        }

        // 绑定鼠标按下事件
        drapLine.onmousedown = (ev) => {

            // 阻止默认事件
            ev.preventDefault();

            // 按下时，监控的是document鼠标事件，不能使用 cnLine对象绑定，因为事件有效区域太小了
            document.onmousemove = (ev) => {
                let x = ev.clientX;
                // 实时改变左侧布局的宽度
                leftLayout.style.width = `${x}px`;
                // 实时改变右侧布局的宽度
                rightLayout.style.width = `${rightOffsetWidth - x}px`;
            };
            // 鼠标抬起时终止事件，保存数据
            document.onmouseup = () => {
                // 终止事件
                document.onmousemove = null;
                document.onmouseup = null;

                // localStorage设置
                let layout = {
                    leftLayout: leftLayout.style.width,
                    rightLayout: rightLayout.style.width
                };
                localStorage.setItem('layout', JSON.stringify(layout));
            };
        }
    }

</script>
</body>

</html>

```
