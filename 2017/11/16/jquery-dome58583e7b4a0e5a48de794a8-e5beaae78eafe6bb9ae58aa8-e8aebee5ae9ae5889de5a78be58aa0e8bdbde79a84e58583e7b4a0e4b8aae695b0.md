---
title: 'JQuery DOM元素复用  &#8211;> 循环滚动 &#8211;> 设定初始加载的元素个数'
date: '2017-11-16T10:37:59+00:00'
status: publish
permalink: /2017/11/16/jquery-dom%e5%85%83%e7%b4%a0%e5%a4%8d%e7%94%a8-%e5%be%aa%e7%8e%af%e6%bb%9a%e5%8a%a8-%e8%ae%be%e5%ae%9a%e5%88%9d%e5%a7%8b%e5%8a%a0%e8%bd%bd%e7%9a%84%e5%85%83%e7%b4%a0%e4%b8%aa%e6%95%b0
author: 毛巳煜
excerpt: ''
type: post
id: 91
category:
    - JavaScript
tag: []
post_format: []
hestia_layout_select:
    - default
---
```
<pre data-language="HTML">```markup



    <meta charset="UTF-8"></meta>
    <title>DOM元素复用 --> 循环滚动 (JQuery)</title>
    <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>

<style>
    #parent {
        line-height: 30px;
        height: 30px;
        overflow: hidden;
    }

</style>


<div id="parent"></div>

<script>
    (function ($) {

        const jsonArray = [
            'QQ: 85785053',
            `<span style="color: #3399f3">&#22495;&#21517;&#21464;&#26356;&#65306; &#30001; <span style="color: #000">www.itfactory.wang &#21464;&#26356;&#20026; <a href="http://www.private-blog.com" style="color: #090">www.private-blog.com`,
            '<a href="http://www.private-blog.com" style="color: #090">&#31169;&#20154;&#21338;&#23458;',
            '<a href="http://www.baidu.com" style="color: #080">&#30334;&#24230;',
            '<a href="http://www.sina.com" style="color: #070">&#26032;&#28010;',
            '<a href="http://www.qq.com" style="color: #060">&#33150;&#35759;',
            '<a href="http://www.cctv.com" style="color: #050">&#22830;&#35270;&#32593;',
        ];

        let defaults = {
            speed: 666,
            easing: 'linear',
            time: 2500
        }

        // &#21019;&#24314;&#23376;&#20803;&#32032;
        const createElement = (text) => {
            let tempDiv = $(`<div class="myList">${text}`);
            return tempDiv;
        }

        // &#35774;&#23450;&#21021;&#22987;&#21152;&#36733;&#30340;&#20803;&#32032;&#20010;&#25968;
        let setItemNums = 3;
        for (let i = 0, len = setItemNums; i < len; i++) {
            $('#parent').append(createElement(jsonArray[i]));
        }

        // &#25509;&#30528;&#24050;&#32463;&#21152;&#36733;&#30340;&#25968;&#25454; &#32487;&#32493;&#21152;&#36733;
        let index = setItemNums;
        setInterval(() => {
            if (index >= jsonArray.length) {
                index = 0;
            }
            // &#33719;&#21462;&#31532;&#19968;&#20010;&#20803;&#32032;
            let temp = <span class="katex math inline">('.myList:eq(0)');
            temp.animate({
                    // &#21521;&#19978;&#31227;&#21160;&#30340;&#39640;&#24230;&#27491;&#22909;&#26159;div&#30340;&#21487;&#35265;&#39640;&#24230;
                    marginTop: -('#parent').height()
                },
                // &#21160;&#30011;&#25191;&#34892;&#36895;&#24230;
                defaults.speed,
                // &#21160;&#30011;&#25191;&#34892;&#32467;&#26463; &#22238;&#35843;&#20989;&#25968;
                () => {
                    // &#31227;&#38500;&#31532;&#19968;&#20010;&#23376;&#20803;&#32032;
                    temp.remove();
                    // &#20174;&#25968;&#25454;&#28304;&#20013;&#36861;&#21152;&#19968;&#26465;&#26032;&#30340;&#23376;&#20803;&#32032;
                    $('#parent').append(createElement(jsonArray[index]));
                    index++;
                });
            // &#27599; 2500 &#27627;&#31186;&#25191;&#34892;&#19968;&#27425;
        }, defaults.time);
    })(jQuery);
</script>



```
```