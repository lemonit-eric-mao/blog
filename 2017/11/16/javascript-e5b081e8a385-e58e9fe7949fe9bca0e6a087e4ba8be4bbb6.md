---
title: 'JavaScript 封装 原生鼠标事件'
date: '2017-11-16T10:38:40+00:00'
status: publish
permalink: /2017/11/16/javascript-%e5%b0%81%e8%a3%85-%e5%8e%9f%e7%94%9f%e9%bc%a0%e6%a0%87%e4%ba%8b%e4%bb%b6
author: 毛巳煜
excerpt: ''
type: post
id: 93
category:
    - JavaScript
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
### **前言**

**封装事件之前有一件事必须搞清楚，那就是回调函数，回调函数的用法与设计思路！**

**为什么要用回调函数？它又适用在哪儿呢？**

**我们正常做开发写代码，都是先自己定义好一个函数，然后在去调用；回调函数的思想正好是相反的，是先调用一个抽象的函数（`也就是不存在的方法`）函数内具体的逻辑代码由使用者来实现（`函数的声明权交由使用者来处理`）！**

**那么这么做有什么好处呢？**  
 **举个例子：我想给某元素添加一个动画效果，当这个动画的效果结束以后我才能做`某些事情`，为什么说是`某些事情`？因为具体做什么事情，设计动画的人是不知道的，也是不需要关心的，具体的事情`由使用者来决定`这个时候最适合使用回调函数了！**

### **mouse-event.js**

```javascript
    /**
     * H5 浏览器中鼠标移动事件
     * Created by mao-siyu on 2021-01-28
     * 使用方法:
     *        const element = document.getElementById("elementId");
     *        const mouseEvent = new MouseEvent(element);
     *        mouseEvent.mousemove = (x, y) => {
     *            console.log(x, y)
     *        };
     *        mouseEvent.mouseup = () => {
     *            console.info(111111);
     *            mouseEvent.removeEvent();
     *        };
     */
    class MouseEvent {
        constructor(obj) {
            this.objEvent = obj;
            this.objEvent.addEventListener('mousedown', this.listener, false);
            this.objEvent.addEventListener('mouseup', this.listener, false);
            this.objEvent.addEventListener('mousemove', this.listener, false);
            this.objEvent.addEventListener('contextmenu', this.listener, false);
            /**
             * down 按下
             * up 抬起
             * @type {string}
             */
            this.state = 'up';
        }

        /**
         * 如何监听鼠标在控件的位置
         * 默认是监听 DOM的
         * @param event 回调事件
         */
        listener = (event) => {

            event.preventDefault();
            switch (event.type) {
                case 'mousemove':
                    if (this.state === 'down')
                        this.mousemove(event.clientX, event.clientY, event);
                    break;
                case 'mousedown':
                    this.state = 'down';
                    this.mousedown(event.clientX, event.clientY, this.state, event);
                    break;
                case 'mouseup':
                    this.state = 'up';
                    this.mouseup(event.clientX, event.clientY, this.state, event);
                    break;
                // 鼠标右键
                case 'contextmenu':
                    // event.button (0: 左键, 1: 滚轮, 2: 右键)
                    this.contextmenu(event);
                    break;
            }

        };


        /**
         * 移除鼠标事件
         */
        removeEvent() {
            this.objEvent.removeEventListener('mousedown', this.listener, false);
            this.objEvent.removeEventListener('mouseup', this.listener, false);
            this.objEvent.removeEventListener('mousemove', this.listener, false);
            this.objEvent.removeEventListener('contextmenu', this.listener, false);
        }

        /**
         * 鼠标移动事件
         */
        mousemove(x, y, event) {
        }


        /**
         * 鼠标按下事件
         */
        mousedown(x, y, state, event) {
        }

        /**
         * 鼠标抬起事件
         */
        mouseup(x, y, state, event) {
        }

        /**
         * 鼠标右键
         */
        contextmenu(event) {
        }

    }


```