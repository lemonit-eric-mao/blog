---
title: "Canvas 画钟表"
date: "2017-11-16"
categories: 
  - "javascript"
---

## **利用业余时间和哥们儿一起学习使用Canvas 画钟表, 风格很漂亮, 给燕老师点赞**

**这个小插件添加了一个小功能, 根据盒子大小自适应.**

```markup
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>画时钟</title>

    <style>
        * {
            margin: 0;
            padding: 0;
            list-style: none;
        }

        #box {
            width: 225px;
            margin: auto;
        }
    </style>

    <script>
        /**
         * 初始化 Context
         */
        var ctx;
        var mClientWidth;
        var mClientHeight;
        const initContext = () => {
            let canvas = document.getElementById('clock');
            mClientWidth = canvas.clientWidth;
            mClientHeight = canvas.clientHeight;
            ctx = canvas.getContext('2d');
        }
    </script>

    <script>

        /**
         * 背景
         */
            // 圆的半径
        let radius;
        const initClockBackground = () => {
            // 路径颜色
            ctx.strokeStyle = '#fff';
            // 路径宽度
            ctx.lineWidth = 10;
            let linegrad = ctx.createLinearGradient(150, 0, -150, 0);
            linegrad.addColorStop(0, '#242f37');
            linegrad.addColorStop(1, '#48585c');
            ctx.fillStyle = linegrad;
            // 画圆形路径
            // 参数： ctx.arc = (x坐标, y坐标, 半径, 起始角度, 结束角度, 逆时针);
            // 参数： ctx.arc = (x, y, radius, startAngle, endAngle, anticlockwise);
            ctx.beginPath();
            // 画布是正方形,
            // 画布宽度了一半做为 X轴坐标,
            // 画布高度了一半做为 Y轴坐标,
            // 因为画布是正方形所以 X轴Y轴坐标在同一点 即圆心点
            radius = mClientWidth / 2;
            ctx.arc(mClientWidth / 2, mClientHeight / 2, radius, 0, 2 * Math.PI, false);
            // 开始画路径
            ctx.stroke();
            ctx.closePath();
            ctx.clip();
            ctx.fill();
        }

        /**
         * 时刻度
         */
        const initClockHourScale = () => {
            for (var i = 0; i < 12; i++) {
                ctx.save();
                // 设置 X轴为radius, Y轴为radius 的位置为原始点
                ctx.translate(radius, radius);
                // 旋转
                ctx.rotate(30 * i * Math.PI / 180);
                // 注： moveTo 与 lineTo 它们的XY 0点位置，是从 ctx.translate(radius, radius) 设定的位置开始的
                ctx.beginPath();
                // 开始一条路径,
                // 将画笔移动到起始点为 x = 0, y = -(radius - radius * 0.15) 的位置,
                // 终点为 x = 0, y = -(radius - radius * 0.05) 的位置画一条线。
                // 注： (radius - radius * 0.05)是按照半径的百分比进行绘图
                ctx.moveTo(0, -(radius - radius * 0.15));
                ctx.lineTo(0, -(radius - radius * 0.05));
                // 结束画笔
                ctx.closePath();
                ctx.strokeStyle = '#DAA520';
                // 路径的宽度
                ctx.lineWidth = 3;
                ctx.stroke();
                ctx.restore();
            }
        }

        /**
         * 画字体时间
         */
        const initClockHourFont = () => {
            for (var i = 12; i > 0; i--) {
                ctx.save();
                ctx.translate(radius, radius);
                ctx.rotate(30 * i * Math.PI / 180);
                ctx.beginPath();
                ctx.font = 'bold 16px impack'
                ctx.fillStyle = '#ffffff';
                // 字符如果是个位数 就偏移5 反之偏移10
                // ctx.fillText = (文本, X坐标, Y坐标);
                // ctx.fillText = (text, x, y);
                ctx.fillText(i, (i > 9) ? -10 : -5, -(radius - radius * 0.27));
                ctx.closePath();
                ctx.lineWidth = 2;
                ctx.stroke();
                ctx.restore();
            }
        }

        /**
         * 分刻度
         */
        const initClockMinuteScale = () => {
            for (var i = 0; i < 60; i++) {
                ctx.save();
                ctx.translate(radius, radius);
                ctx.rotate(6 * i * Math.PI / 180);
                ctx.beginPath();
                ctx.moveTo(0, -(radius - radius * 0.1));
                ctx.lineTo(0, -(radius - radius * 0.05));
                ctx.closePath();
                ctx.strokeStyle = '#EEE8AA';
                ctx.lineWidth = 2;
                ctx.stroke();
                ctx.restore();
            }
        }

        /**
         * 时针
         * @param hour
         */
        const initClockHourNeedle = (hour) => {
            ctx.save();
            ctx.translate(radius, radius);// 把画布的原点移到圆的原点处
            let theta = 30 * hour * Math.PI / 180;
            ctx.rotate(theta);
            ctx.beginPath();
            ctx.moveTo(0, radius - radius * 0.9);
            ctx.lineTo(0, -(radius - radius * 0.5));
            ctx.closePath();
            ctx.strokeStyle = '#ffffff';
            ctx.lineWidth = 8;
            ctx.stroke();
            ctx.restore();
        }

        /**
         * 分针
         * @param minute
         */
        const initClockMinuteNeedle = (minute) => {
            ctx.save();
            ctx.translate(radius, radius);// 把画布的原点移到圆的原点处
            let theta = 6 * minute * Math.PI / 180;
            ctx.rotate(theta);
            ctx.beginPath();
            ctx.moveTo(0, radius - radius * 0.9);
            ctx.lineTo(0, -(radius - radius * 0.35));
            ctx.closePath();
            ctx.strokeStyle = '#ffffff';
            ctx.lineWidth = 3;
            ctx.stroke();
            ctx.restore();
        }

        /**
         * 秒针
         * @param seconds
         */
        const initClockSecondNeedle = (seconds) => {
            ctx.save();
            ctx.translate(radius, radius);
            let theta = 6 * seconds * Math.PI / 180;
            ctx.rotate(theta);
            ctx.beginPath();
            ctx.moveTo(0, radius - radius * 0.9);
            ctx.lineTo(0, -(radius - radius * 0.3));
            ctx.strokeStyle = '#ffffff';
            ctx.lineWidth = 1;
            ctx.stroke();
            ctx.closePath();
            // 秒针底部的圆圈
            ctx.beginPath();
            ctx.arc(0, 0, 8, 0, 2 * Math.PI, true);
            ctx.fillStyle = '#D01B5A';
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 3;
            ctx.stroke();
            ctx.fill();
            ctx.closePath();
            // 秒针顶部的圆
            ctx.beginPath();
            ctx.arc(0, -(radius - radius * 0.35), 4, 0, 2 * Math.PI, true);
            ctx.fillStyle = '#D859A1';
            ctx.strokeStyle = '#D01B5A';
            ctx.lineWidth = 3;
            ctx.stroke();
            ctx.fill();
            ctx.closePath();
            ctx.restore();
        }

        /**
         * 排序 初始化
         */
        const initStep = () => {
            initContext();
            initClock();
        }

        /**
         * 初始化 时钟
         */
        const initClock = () => {
            // 获取当前时间
            let date = new Date();
            let hours = date.getHours();
            let minutes = date.getMinutes();
            let seconds = date.getSeconds();
            hours = hours > 12 ? hours - 12 : hours;
            let hour = hours + minutes / 60;
            let minute = minutes + seconds / 60;

            // 清空画面准备重新画
            ctx.clearRect(0, 0, mClientWidth, mClientHeight);
            initClockBackground();
            initClockMinuteScale();
            initClockHourScale();
            initClockHourFont();
            initClockHourNeedle(hour);
            initClockMinuteNeedle(minute);
            initClockSecondNeedle(seconds);
        }

        // 每秒执行一次
        setInterval(initClock, 1000);

    </script>
</head>
<body onload="initStep()">
<div id="box">
    <canvas id="clock" width="225" height="225"></canvas>
</div>
</body>
</html>
```
