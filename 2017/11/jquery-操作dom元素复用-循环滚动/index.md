---
title: "JQuery 操作DOM元素复用 --> 循环滚动"
date: "2017-11-16"
categories: 
  - "javascript"
---

```markup
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>DOM元素复用 --> 循环滚动 (JQuery)</title>
    <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
</head>
<style>
    #parent {
        line-height: 30px;
        height: 30px;
        overflow: hidden;
    }

</style>
<body>

<div id="parent"></div>

<script>
    (function ($) {
        const jsonArray = [
            'QQ: 85785053',
            `<span style="color: #3399f3">域名变更： 由 <span style="color: #000">www.itfactory.wang</span> 变更为 <a href="http://www.private-blog.com" style="color: #090">www.private-blog.com</a></span>`,
            '<a href="http://www.private-blog.com" style="color: #090">私人博客</a>',
        ];

        let defaults = {
            speed: 666,
            easing: 'linear',
            time: 2500
        }

        // 创建子元素
        const createElement = (text) => {
            let tempDiv = $(`<div class="myList">${text}</div>`);
            return tempDiv;
        }

        for (let i = 0, len = jsonArray.length; i < len; i++) {
            $('#parent').append(createElement(jsonArray[i]));
        }

        setInterval(() => {
            let temp = $('.myList:eq(0)');
            temp.animate({
                    // 向上移动的高度正好是div的高度
                    marginTop: -$('#parent').height()
                },
                // 动画执行速度
                defaults.speed,
                // 动画执行结束 回调函数
                () => {
                    $('#parent').append(temp.css({marginTop: '0px'}));
                });
            // 每 2500 毫秒执行一次
        }, defaults.time);
    })(jQuery);
</script>
</body>
</html>
```
