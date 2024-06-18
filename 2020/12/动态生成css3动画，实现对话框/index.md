---
title: "动态生成CSS3动画，实现对话框"
date: "2020-12-15"
categories: 
  - "css"
---

###### 动态生成CSS3动画

```javascript
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title></title>

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
            /*子层居中*/
            align-items: center;
            justify-content: center;
        }

        /*对话框*/
        .dl-foundation > .dl-dialog {
            /*当前层大小*/
            width: 80vw;
            height: 80vh;
            /*!*固定定位*!*/
            position: fixed;
            /*标识恢复元素鼠标事件*/
            pointer-events: auto;
            background-color: #FFF;
            display: flex;
        }

        .dl-foundation > .dl-dialog > .dl-wrapper {
            flex: 1;
            display: flex;
            flex-direction: column;
            /**
             * stretch： 标识子层全是100%
             * center： 标识子层用多少占多少并且居中
             */
            align-items: stretch;
        }

        /*标题栏*/
        .dl-foundation > .dl-dialog > .dl-wrapper > .dl-title {
            background-color: #26b58f;
            display: flex;
            /**
             * space-between: 标识子层两端对齐
             */
            justify-content: space-between;
        }

        /*标题栏文字*/
        .dl-foundation > .dl-dialog > .dl-wrapper > .dl-title > .dl-text {
        }

        /*正文*/
        .dl-foundation > .dl-dialog > .dl-wrapper > .dl-content {
            background-color: green;
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        /*按钮*/
        .dl-foundation > .dl-dialog > .dl-wrapper > .dl-buttons {
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
<input type="button" value="测试弹窗" onclick="openDialog()"/>
<!--地基-->
<div class="dl-foundation" id="foundation"></div>
</body>
<script>

    /**
     * 打开对话框
     */
    function openDialog() {
        let template = `
            <div class="dl-wrapper">
                <div class="dl-title">
                    <div class="dl-text">标题栏</div>
                    <div>
                        <svg class="icon dl-minimize" width="20px" height="20px" viewBox="0 0 1024 1024" version="1.1"
                             xmlns="http://www.w3.org/2000/svg">
                            <path fill="#333333" d="M76.8 563.2h819.2a51.2 51.2 0 0 0 0-102.4h-819.2a51.2 51.2 0 0 0 0 102.4z"/>
                        </svg>
                    </div>
                </div>
                <div class="dl-content">正文</div>
                <div class="dl-buttons">
                    <div class="dl-close">关闭</div>
                    <div>确定</div>
                </div>
            </div>
        `;

        /* ------------------------------------------------------ */

        // 地基 父层
        let foundation = document.getElementById('foundation');
        let dialog = document.createElement('div');
        dialog.classList.add('dl-dialog');
        dialog.innerHTML = template;

        /* ------------------------------------------------------ */

        // 获取对话框种的容器
        let wrapper = dialog.querySelector('.dl-wrapper');
        // 获取正文
        let content = dialog.querySelector('.dl-content');
        // 获取最小化按钮
        let minimizeBtn = dialog.querySelector('.dl-minimize');
        // 获取关闭按钮
        let closeBtn = dialog.querySelector('.dl-close');

        /** ======================== 添加属性 ======================== */

        // 让容器内元素事件生效
        wrapper.style.pointerEvents = 'auto';

        // 为了差异效果，让正文背景，随机色
        content.style.backgroundColor = `#${Math.floor(Math.random() * 0xffffff).toString(16)}`;

        // 设置z-index, 通过获取 foundation 父层的子节点数量
        let index = foundation.children.length;
        dialog.setAttribute('index', index);
        dialog.style.zIndex = index;

        /** ======================== 添加事件 ======================== */

        /**
         * 最小化按钮， 添加点击事件， 注意 () => {} 与 function() {} 的使用区别
         */
        minimizeBtn.onclick = () => {
            this.event.stopPropagation();
            // 让容器内元素事件无效；
            wrapper.style.pointerEvents = 'none';
            // 获取当前窗体的索引
            let index = dialog.getAttribute('index');

            /* ------------------------------------------------------ */

            // 添加动画 缩放+位移
            let translate = `translate(-55%, ${55 - index * 10}%) scale(0.1, 0.1)`;
            dialog.animate([
                {transform: `scale(1, 1)`},
                {transform: translate}
            ], {
                duration: 500
            });
            // 设置动画停止后的便宜量
            dialog.style.transform = translate;
        };

        /**
         * 还原， 添加点击事件， 注意 () => {} 与 function() {} 的使用区别
         */
        dialog.onclick = function () {
            // 通过事件的值来区分当前窗体的状态，如果当前状态不是最小化，直接返回
            if ('auto' === wrapper.style.pointerEvents) {
                return;
            }
            // 让容器内元素事件生效
            wrapper.style.pointerEvents = 'auto';
            // 获取当前窗体的索引
            let index = this.getAttribute('index');

            /* ------------------------------------------------------ */

            // 添加动画 缩放+位移
            let translate = `translate(-55%, ${55 - index * 10}%) scale(0.1, 0.1)`;
            this.animate([
                {transform: translate},
                {transform: `scale(1, 1)`}
            ], {
                duration: 500
            });
            // 设置动画停止后的偏移量
            dialog.style.transform = `scale(1, 1)`;

            /* ------------------------------------------------------ */

            // 将 HTMLCollection 转化为数组
            let items = Array.from(foundation.children);
            // 重置 z-index
            items.forEach((itemDialog) => {
                // 【1】每次点击恢复，都让所有元素自己减一层
                itemDialog.style.zIndex = --itemDialog.style.zIndex;
            });
            // 【2】然后让当前选中的元素恢复到最上层
            dialog.style.zIndex = items.length;
        };

        /**
         * 关闭按钮， 添加点击事件
         */
        closeBtn.onclick = () => {

            dialog.remove();

            /* ------------------------------------------------------ */

            // 将 HTMLCollection 转化为数组
            let items = Array.from(foundation.children);
            items.forEach((itemDialog, index) => {
                let wrapper = itemDialog.querySelector('.dl-wrapper');
                itemDialog.setAttribute('index', index);

                // 对话框状态处于打开的，不进行位移
                if ('none' === wrapper.style.pointerEvents) {
                    // 设置每层的偏移量
                    itemDialog.style.transform = `translate(-55%, ${55 - index * 10}%) scale(0.1, 0.1)`;
                }
            });
        };

        // 加入到父层
        foundation.appendChild(dialog);
    }

</script>
</html>
```
