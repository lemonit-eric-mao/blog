---
title: 'JavaScript 拖拽改变Dom元素宽度'
date: '2021-02-01T07:21:07+00:00'
status: private
permalink: /2021/02/01/javascript-%e6%8b%96%e6%8b%bd%e6%94%b9%e5%8f%98dom%e5%85%83%e7%b4%a0%e5%ae%bd%e5%ba%a6
author: 毛巳煜
excerpt: ''
type: post
id: 6858
category:
    - JavaScript
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
```javascript




    <meta charset="utf-8"></meta>
    <meta content="IE=edge" http-equiv="X-UA-Compatible"></meta>
    <title></title>
    <meta content="width=device-width, initial-scale=1" name="viewport"></meta>
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
            /* &#32477;&#23545;&#23450;&#20301;&#24773;&#20917; [&#19978; &#19979; &#24038; &#21491;]&#20805;&#28385;*/
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



<div class="layout">
    <div class="top">顶部导航</div>
    <div class="left-layout" id="leftLayout">
        <div id="menu">
            <span>待拖拽的div</span>
        </div>
        <div class="drap-line" id="drapLine"></div>
    </div>
    <div class="right-layout" id="rightLayout">
        右边的div
    </div>
</div>
<script>

    // &#33719;&#21462;dom
    let drapLine = document.getElementById('drapLine');
    let leftLayout = document.getElementById('leftLayout');
    let rightLayout = document.getElementById('rightLayout');

    window.onload = () => {

        // &#35745;&#31639;&#21491;&#20391;&#24067;&#23616;&#65292;&#21021;&#22987;&#30340;&#23485;&#24230;
        let rightOffsetWidth = rightLayout.clientWidth + leftLayout.clientWidth;

        // &#21021;&#22987;&#26102;&#35835;&#21462;localStorage&#20445;&#23384;&#30340;&#25968;&#25454;
        let layout = localStorage.getItem('layout');
        if (layout) {
            layout = JSON.parse(layout);
            leftLayout.style.width = layout.leftLayout;
            rightLayout.style.width = layout.rightLayout;
        }

        // &#32465;&#23450;&#40736;&#26631;&#25353;&#19979;&#20107;&#20214;
        drapLine.onmousedown = (ev) => {

            // &#38459;&#27490;&#40664;&#35748;&#20107;&#20214;
            ev.preventDefault();

            // &#25353;&#19979;&#26102;&#65292;&#30417;&#25511;&#30340;&#26159;document&#40736;&#26631;&#20107;&#20214;&#65292;&#19981;&#33021;&#20351;&#29992; cnLine&#23545;&#35937;&#32465;&#23450;&#65292;&#22240;&#20026;&#20107;&#20214;&#26377;&#25928;&#21306;&#22495;&#22826;&#23567;&#20102;
            document.onmousemove = (ev) => {
                let x = ev.clientX;
                // &#23454;&#26102;&#25913;&#21464;&#24038;&#20391;&#24067;&#23616;&#30340;&#23485;&#24230;
                leftLayout.style.width = `<span class="katex math inline">{x}px`;
                // &#23454;&#26102;&#25913;&#21464;&#21491;&#20391;&#24067;&#23616;&#30340;&#23485;&#24230;
                rightLayout.style.width = `{rightOffsetWidth - x}px`;
            };
            // &#40736;&#26631;&#25260;&#36215;&#26102;&#32456;&#27490;&#20107;&#20214;&#65292;&#20445;&#23384;&#25968;&#25454;
            document.onmouseup = () => {
                // &#32456;&#27490;&#20107;&#20214;
                document.onmousemove = null;
                document.onmouseup = null;

                // localStorage&#35774;&#32622;
                let layout = {
                    leftLayout: leftLayout.style.width,
                    rightLayout: rightLayout.style.width
                };
                localStorage.setItem('layout', JSON.stringify(layout));
            };
        }
    }

</script>





```