---
title: "jquery 实现图片呼吸效果"
date: "2017-11-16"
categories: 
  - "javascript"
---

```markup
<html>

<head>
    <title>实现多个元素呼吸效果相对布局 悬停效果 长时间悬停会停止所有</title>
    <style>
        body {
            TEXT-ALIGN: center;
        }

        .center {
            MARGIN-RIGHT: auto;
            MARGIN-LEFT: auto;
            background-image: url('image/bg_01.jpg');
            vertical-align: middle;
        }
    </style>
    <script type="text/javascript" src="jquery-3.1.0.min.js"></script>

    <script>
        /**
         * 获取 父元素宽
         * @param parentObj
         */
        var get_parent_widht = function () {
            return $('.center').width();
        }

        /**
         * 获取 父元素高
         * @param parentObj
         */
        var get_parent_height = function () {
            return $('.center').height();
        }
        /**
         * 获取 父元素top位置
         * @param parentObj
         */
        var get_parent_top = function () {
            return $('.center').offset().top;
        }

        /**
         * 获取 父元素left位置
         * @param parentObj
         */
        var get_parent_left = function () {
            return $('.center').offset().left;
        }

        /**
         * 初始化 图片
         * @param _src
         * @returns {*|jQuery|HTMLElement}
         */
        var init_image = function (_src) {
            var img = $('<image class="breathImgId" timeoutId="" style="width:100px;height:100px"/>');
            img.attr('src', _src);
            return img;
        }

        /**
         * 设定 传入的图片大小
         * @param _obj
         */
        var set_size = function (_obj, width, height) {
            _obj.width(width);
            _obj.height(height);
        }

        var initLoad = function () {

            $('.center').html('');
            var array = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg', '7.jpg', '8.jpg', '9.jpg', '10.jpg', '11.jpg', '12.jpg', '13.jpg', '14.jpg', '15.jpg', '16.jpg'];
            // 总宽度
            var totalWidth = get_parent_widht();
            // 总高度
            var totalHeight = get_parent_height();
            // 图片的宽
            var imgWidth = 100;
            // 图片的高
            var imgHeight = 100;

            for (var i = 0; i < array.length; i++) {
                var imgObj = init_image('image/' + array[i]);
                // 设置位置
                set_position(imgObj, (Math.floor(i * imgHeight / totalWidth) * imgHeight) + get_parent_top(), i * imgWidth % totalWidth + get_parent_left());
                // 追加动画
                animate_breath(imgObj, getRandom(1000, 3000));
                // 鼠标进入
                imgObj.hover(function () {
                    if ($(this).is(':animated')) {
                        $(this).stop(true, true).css('opacity', 1);
                        animate_breath_stop = true;
                    }
                    // 鼠标移出
                }, function () {
                    animate_breath_stop = false;
                    // 为样式为 breathImgId 的元素重新添加动画
                    $('.breathImgId').each(function () {
                        // 追加动画
                        animate_breath($(this), getRandom(1000, 3000));
                    });
                });

                $('.center').append(imgObj);
            }
        }

        $(function () {
            initLoad();
        });
        /******************************** 以下共通是工具 *********************************/
        /**
         * 获取随机数
         * @returns {number}
         */
        function getRandom(n, n1) {
            if (n &amp;&amp; n1) {
                // 获取100-999的随机数——getRandom(100, 999);
                return Math.floor(n + Math.random() * n1);
            } else if (n) {
                // 获取0-999的随机数——getRandom(999);
                return Math.floor(Math.random() * n);
            } else {
                // 默认 0.0 ~ 1.0 之间的一个伪随机数;
                return Math.random();
            }
        }

        /**
         * 添加元素的 呼吸效果
         */
        var animate_breath = function (obj, speed) {
            // 因为这里是 深度递归，使用clearTimeout() 是无法清除的，所以自己先预留个开关
            if (animate_breath_stop)
                return;
            obj.animate({opacity: 0}, speed).animate({opacity: 1}, speed);
            setTimeout(animate_breath, speed * 2, obj, speed);
        }

        /**
         * 停止 呼吸效果
         */
        var animate_breath_stop = false;

        /**
         * 设定 元素的位置
         * @param _obj
         */
        var set_position = function (_obj, _top, _left) {
            _obj.css({position: 'absolute', 'top': _top, 'left': _left, 'z-index': 0});
        }

    </script>
</head>

<body>
<div class="center" style="width: 600px; height: 500px;"></div>
</body>

</html>
```
