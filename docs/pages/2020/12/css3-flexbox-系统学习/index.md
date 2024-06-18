---
title: "CSS3 FlexBox 系统学习"
date: "2020-12-14"
categories: 
  - "css"
---

###### **思路** 就像盖楼一样

1. 先买块儿地(`定位`)
2. 打地基(`设置基础空间大小`)
3. 在屋内添加隔断(`布局`)
4. 在一层一层的向上添砖加瓦(`添加子层`)
5. 在室外装修(`美化样式、添加动画效果`)

* * *

###### 1 先买块儿地(`定位`)

```markup
<body>
<!--地基-->
<div class="dl-foundation">
</div>
</body>
```

* * *

###### 2 打地基(`设置基础空间大小`)

```markup
<body>
<!--地基-->
<div class="dl-foundation">
    <div class="dl-wrapper">
    </div>
</div>
</body>
```

* * *

###### 3 在屋内添加隔断(`布局`)

```markup
<body>
<!--地基-->
<div class="dl-foundation">
    <div class="dl-wrapper">
        <!-- 遮罩-->
        <div class="dl-mask">
            <!-- 对话框 -->
            <div class="dl-dialog" onclick="recovery(this)">
                <!-- 标题栏 -->
                <div class="dl-title">
                </div>
                <!-- 正文 -->
                <div class="dl-content"></div>
                <!-- 按钮 -->
                <div class="dl-buttons">
                </div>
            </div>
        </div>
    </div>
</div>
</body>
```

* * *

###### 4 在一层一层的向上发展(`添加子层`)

```markup
<body>
<!--地基-->
<div class="dl-foundation">
    <div class="dl-wrapper">
        <!-- 遮罩-->
        <div class="dl-mask">
            <!-- 对话框 -->
            <div class="dl-dialog" onclick="recovery(this)">
                <!-- 标题栏 -->
                <div class="dl-title">
                    <div class="dl-text">标题栏</div>
                    <div>
                        <!-- 最小化-->
                        <svg onclick="minimize(this)" class="icon" width="20px" height="20px" viewBox="0 0 1024 1024" version="1.1"
                             xmlns="http://www.w3.org/2000/svg">
                            <path fill="#333333" d="M76.8 563.2h819.2a51.2 51.2 0 0 0 0-102.4h-819.2a51.2 51.2 0 0 0 0 102.4z"/>
                        </svg>
                    </div>
                </div>
                <!-- 正文 -->
                <div class="dl-content">正文</div>
                <!-- 按钮 -->
                <div class="dl-buttons">
                    <div>关闭</div>
                    <div>确定</div>
                </div>
            </div>
        </div>
    </div>
</div>
</body>
```

* * *

* * *

* * *

###### 5 在室外装修(`美化样式、添加动画效果`) **`完整代码`**

```css
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title></title>

    <!-- 动画 -->
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

    <!-- 样式 -->
    <style>
        html, body {
            padding: 0;
            margin: 0;
            border: 0;
        }

        /*地基*/
        .dl-foundation {
            /*固定定位*/
            position: fixed;
            top: 0;
            left: 0;
            /*标识背景透明，并且不影响子层的透明度*/
            background: rgba(0, 0, 0, 0);
            /*标识元素没有鼠标事件，并且事件可以穿透*/
            pointer-events: none;
            /*充满屏幕*/
            width: 100vw;
            height: 100vh;
            /*使用flexbox布局，要想使用flexbox每一层都得写display: flex;，子层不会继承父层的flexbox*/
            display: flex;
        }

        .dl-foundation > .dl-wrapper {
            /*标识背景透明，并且不影响子层的透明度*/
            background: rgba(0, 0, 0, 0);
            /*表示子层的空间占比， 父层必须是flexbox才起作用*/
            flex: 1;
            display: flex;
        }

        /*遮罩*/
        .dl-foundation > .dl-wrapper > .dl-mask {
            background: rgba(189, 189, 189, 0.5);
            flex: 1;
            display: flex;
            /*让子层水平垂直居中*/
            justify-content: center;
            align-items: center;
        }

        /*对话框*/
        .dl-foundation > .dl-wrapper > .dl-mask > .dl-dialog {
            /*阴影*/
            /*
             * box-shadow: x轴偏移量允许负值   y轴偏移量允许负值   阴影的模糊距离   阴影的尺寸   #1e90ff70;
             * box-shadow:              1px                                   1px                               10px                     10px       #1e90ff70;
            */
            box-shadow: 1px 1px 10px 10px #1e90ff70;
            /*当前层大小*/
            width: 80vw;
            height: 80vh;
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

        /*对话框 最小化*/
        .dl-foundation > .dl-wrapper > .dl-mask > .dl-dialog-minimize {
            animation: minimize 1s;
            /*transform属性它们的执行顺序是从后向前执行的， 先执行scale， 在执行 translate*/
            transform: translate(-55%, 55%) scale(0.1, 0.1);
        }

        /*对话框 复原*/
        .dl-foundation > .dl-wrapper > .dl-mask > .dl-dialog-recovery {
            animation: recovery 1s;
            transform: scale(1, 1);
        }

        /*标题栏*/
        .dl-foundation > .dl-wrapper > .dl-mask > .dl-dialog > .dl-title {
            background-color: #26b58f;
            display: flex;
            /**
             * space-between: 标识子层两端对齐
             */
            justify-content: space-between;
        }

        /*标题栏文字*/
        .dl-foundation > .dl-wrapper > .dl-mask > .dl-dialog > .dl-title > .dl-text {
        }

        /*正文*/
        .dl-foundation > .dl-wrapper > .dl-mask > .dl-dialog > .dl-content {
            background-color: green;
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        /*按钮*/
        .dl-foundation > .dl-wrapper > .dl-mask > .dl-dialog > .dl-buttons {
            background-color: #0077c5;
            display: flex;
            /**
             * space-around: 标识子层先平分，后居中
             */
            justify-content: space-around;
            align-items: center;
        }
    </style>
</head>
<body>
<input type="button" value="测试弹窗" onclick="alert('测试鼠标事件穿透')"/>
<!--地基-->
<div class="dl-foundation">
    <div class="dl-wrapper">
        <!-- 遮罩-->
        <div class="dl-mask">
            <!-- 对话框 -->
            <div class="dl-dialog" onclick="recovery(this)">
                <!-- 标题栏 -->
                <div class="dl-title">
                    <div class="dl-text">标题栏</div>
                    <div>
                        <!-- 最小化-->
                        <svg onclick="minimize(this)" class="icon" width="20px" height="20px" viewBox="0 0 1024 1024" version="1.1"
                             xmlns="http://www.w3.org/2000/svg">
                            <path fill="#333333" d="M76.8 563.2h819.2a51.2 51.2 0 0 0 0-102.4h-819.2a51.2 51.2 0 0 0 0 102.4z"/>
                        </svg>
                    </div>
                </div>
                <!-- 正文 -->
                <div class="dl-content">正文</div>
                <!-- 按钮 -->
                <div class="dl-buttons">
                    <div>关闭</div>
                    <div>确定</div>
                </div>
            </div>
        </div>
    </div>
</div>
</body>
<script>
    /**
     * 最小化
     * @param obj
     */
    function minimize(obj) {

        this.event.stopPropagation();

        // 父层
        let parent = obj.parentElement.parentElement.parentElement;

        parent.classList.remove('dl-dialog-recovery');
        parent.classList.add('dl-dialog-minimize');
    }

    /**
     * 复原
     * @param obj
     */
    function recovery(obj) {

        // 判断，如果当前状态不是最小化，直接返回
        if (!obj.classList.contains('dl-dialog-minimize')) {
            return;
        }

        obj.classList.remove('dl-dialog-minimize');
        obj.classList.add('dl-dialog-recovery');
    }
</script>
</html>
```
