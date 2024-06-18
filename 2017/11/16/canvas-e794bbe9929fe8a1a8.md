---
title: 'Canvas 画钟表'
date: '2017-11-16T16:44:17+00:00'
status: publish
permalink: /2017/11/16/canvas-%e7%94%bb%e9%92%9f%e8%a1%a8
author: 毛巳煜
excerpt: ''
type: post
id: 565
category:
    - JavaScript
tag: []
post_format: []
hestia_layout_select:
    - default
---
**利用业余时间和哥们儿一起学习使用Canvas 画钟表, 风格很漂亮, 给燕老师点赞**
---------------------------------------------

**这个小插件添加了一个小功能, 根据盒子大小自适应.**

```
<pre data-language="HTML">```markup



    <meta charset="UTF-8"></meta>
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
         * &#21021;&#22987;&#21270; Context
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
         * &#32972;&#26223;
         */
            // &#22278;&#30340;&#21322;&#24452;
        let radius;
        const initClockBackground = () => {
            // &#36335;&#24452;&#39068;&#33394;
            ctx.strokeStyle = '#fff';
            // &#36335;&#24452;&#23485;&#24230;
            ctx.lineWidth = 10;
            let linegrad = ctx.createLinearGradient(150, 0, -150, 0);
            linegrad.addColorStop(0, '#242f37');
            linegrad.addColorStop(1, '#48585c');
            ctx.fillStyle = linegrad;
            // &#30011;&#22278;&#24418;&#36335;&#24452;
            // &#21442;&#25968;&#65306; ctx.arc = (x&#22352;&#26631;, y&#22352;&#26631;, &#21322;&#24452;, &#36215;&#22987;&#35282;&#24230;, &#32467;&#26463;&#35282;&#24230;, &#36870;&#26102;&#38024;);
            // &#21442;&#25968;&#65306; ctx.arc = (x, y, radius, startAngle, endAngle, anticlockwise);
            ctx.beginPath();
            // &#30011;&#24067;&#26159;&#27491;&#26041;&#24418;,
            // &#30011;&#24067;&#23485;&#24230;&#20102;&#19968;&#21322;&#20570;&#20026; X&#36724;&#22352;&#26631;,
            // &#30011;&#24067;&#39640;&#24230;&#20102;&#19968;&#21322;&#20570;&#20026; Y&#36724;&#22352;&#26631;,
            // &#22240;&#20026;&#30011;&#24067;&#26159;&#27491;&#26041;&#24418;&#25152;&#20197; X&#36724;Y&#36724;&#22352;&#26631;&#22312;&#21516;&#19968;&#28857; &#21363;&#22278;&#24515;&#28857;
            radius = mClientWidth / 2;
            ctx.arc(mClientWidth / 2, mClientHeight / 2, radius, 0, 2 * Math.PI, false);
            // &#24320;&#22987;&#30011;&#36335;&#24452;
            ctx.stroke();
            ctx.closePath();
            ctx.clip();
            ctx.fill();
        }

        /**
         * &#26102;&#21051;&#24230;
         */
        const initClockHourScale = () => {
            for (var i = 0; i < 12; i++) {
                ctx.save();
                // &#35774;&#32622; X&#36724;&#20026;radius, Y&#36724;&#20026;radius &#30340;&#20301;&#32622;&#20026;&#21407;&#22987;&#28857;
                ctx.translate(radius, radius);
                // &#26059;&#36716;
                ctx.rotate(30 * i * Math.PI / 180);
                // &#27880;&#65306; moveTo &#19982; lineTo &#23427;&#20204;&#30340;XY 0&#28857;&#20301;&#32622;&#65292;&#26159;&#20174; ctx.translate(radius, radius) &#35774;&#23450;&#30340;&#20301;&#32622;&#24320;&#22987;&#30340;
                ctx.beginPath();
                // &#24320;&#22987;&#19968;&#26465;&#36335;&#24452;,
                // &#23558;&#30011;&#31508;&#31227;&#21160;&#21040;&#36215;&#22987;&#28857;&#20026; x = 0, y = -(radius - radius * 0.15) &#30340;&#20301;&#32622;,
                // &#32456;&#28857;&#20026; x = 0, y = -(radius - radius * 0.05) &#30340;&#20301;&#32622;&#30011;&#19968;&#26465;&#32447;&#12290;
                // &#27880;&#65306; (radius - radius * 0.05)&#26159;&#25353;&#29031;&#21322;&#24452;&#30340;&#30334;&#20998;&#27604;&#36827;&#34892;&#32472;&#22270;
                ctx.moveTo(0, -(radius - radius * 0.15));
                ctx.lineTo(0, -(radius - radius * 0.05));
                // &#32467;&#26463;&#30011;&#31508;
                ctx.closePath();
                ctx.strokeStyle = '#DAA520';
                // &#36335;&#24452;&#30340;&#23485;&#24230;
                ctx.lineWidth = 3;
                ctx.stroke();
                ctx.restore();
            }
        }

        /**
         * &#30011;&#23383;&#20307;&#26102;&#38388;
         */
        const initClockHourFont = () => {
            for (var i = 12; i > 0; i--) {
                ctx.save();
                ctx.translate(radius, radius);
                ctx.rotate(30 * i * Math.PI / 180);
                ctx.beginPath();
                ctx.font = 'bold 16px impack'
                ctx.fillStyle = '#ffffff';
                // &#23383;&#31526;&#22914;&#26524;&#26159;&#20010;&#20301;&#25968; &#23601;&#20559;&#31227;5 &#21453;&#20043;&#20559;&#31227;10
                // ctx.fillText = (&#25991;&#26412;, X&#22352;&#26631;, Y&#22352;&#26631;);
                // ctx.fillText = (text, x, y);
                ctx.fillText(i, (i > 9) ? -10 : -5, -(radius - radius * 0.27));
                ctx.closePath();
                ctx.lineWidth = 2;
                ctx.stroke();
                ctx.restore();
            }
        }

        /**
         * &#20998;&#21051;&#24230;
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
         * &#26102;&#38024;
         * @param hour
         */
        const initClockHourNeedle = (hour) => {
            ctx.save();
            ctx.translate(radius, radius);// &#25226;&#30011;&#24067;&#30340;&#21407;&#28857;&#31227;&#21040;&#22278;&#30340;&#21407;&#28857;&#22788;
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
         * &#20998;&#38024;
         * @param minute
         */
        const initClockMinuteNeedle = (minute) => {
            ctx.save();
            ctx.translate(radius, radius);// &#25226;&#30011;&#24067;&#30340;&#21407;&#28857;&#31227;&#21040;&#22278;&#30340;&#21407;&#28857;&#22788;
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
         * &#31186;&#38024;
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
            // &#31186;&#38024;&#24213;&#37096;&#30340;&#22278;&#22280;
            ctx.beginPath();
            ctx.arc(0, 0, 8, 0, 2 * Math.PI, true);
            ctx.fillStyle = '#D01B5A';
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 3;
            ctx.stroke();
            ctx.fill();
            ctx.closePath();
            // &#31186;&#38024;&#39030;&#37096;&#30340;&#22278;
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
         * &#25490;&#24207; &#21021;&#22987;&#21270;
         */
        const initStep = () => {
            initContext();
            initClock();
        }

        /**
         * &#21021;&#22987;&#21270; &#26102;&#38047;
         */
        const initClock = () => {
            // &#33719;&#21462;&#24403;&#21069;&#26102;&#38388;
            let date = new Date();
            let hours = date.getHours();
            let minutes = date.getMinutes();
            let seconds = date.getSeconds();
            hours = hours > 12 ? hours - 12 : hours;
            let hour = hours + minutes / 60;
            let minute = minutes + seconds / 60;

            // &#28165;&#31354;&#30011;&#38754;&#20934;&#22791;&#37325;&#26032;&#30011;
            ctx.clearRect(0, 0, mClientWidth, mClientHeight);
            initClockBackground();
            initClockMinuteScale();
            initClockHourScale();
            initClockHourFont();
            initClockHourNeedle(hour);
            initClockMinuteNeedle(minute);
            initClockSecondNeedle(seconds);
        }

        // &#27599;&#31186;&#25191;&#34892;&#19968;&#27425;
        setInterval(initClock, 1000);

    </script>


<div id="box">
    <canvas height="225" id="clock" width="225"></canvas>
</div>



```
```