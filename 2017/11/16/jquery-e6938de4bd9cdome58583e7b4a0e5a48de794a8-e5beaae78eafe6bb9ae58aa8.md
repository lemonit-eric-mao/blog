---
title: 'JQuery 操作DOM元素复用 &#8211;> 循环滚动'
date: '2017-11-16T10:18:34+00:00'
status: publish
permalink: /2017/11/16/jquery-%e6%93%8d%e4%bd%9cdom%e5%85%83%e7%b4%a0%e5%a4%8d%e7%94%a8-%e5%be%aa%e7%8e%af%e6%bb%9a%e5%8a%a8
author: 毛巳煜
excerpt: ''
type: post
id: 85
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

        for (let i = 0, len = jsonArray.length; i < len; i++) {
            $('#parent').append(createElement(jsonArray[i]));
        }

        setInterval(() => {
            let temp = <span class="katex math inline">('.myList:eq(0)');
            temp.animate({
                    // &#21521;&#19978;&#31227;&#21160;&#30340;&#39640;&#24230;&#27491;&#22909;&#26159;div&#30340;&#39640;&#24230;
                    marginTop: -('#parent').height()
                },
                // &#21160;&#30011;&#25191;&#34892;&#36895;&#24230;
                defaults.speed,
                // &#21160;&#30011;&#25191;&#34892;&#32467;&#26463; &#22238;&#35843;&#20989;&#25968;
                () => {
                    $('#parent').append(temp.css({marginTop: '0px'}));
                });
            // &#27599; 2500 &#27627;&#31186;&#25191;&#34892;&#19968;&#27425;
        }, defaults.time);
    })(jQuery);
</script>



```
```