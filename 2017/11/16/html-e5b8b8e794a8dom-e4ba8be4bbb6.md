---
title: 'HTML 常用DOM 事件'
date: '2017-11-16T16:44:56+00:00'
status: publish
permalink: /2017/11/16/html-%e5%b8%b8%e7%94%a8dom-%e4%ba%8b%e4%bb%b6
author: 毛巳煜
excerpt: ''
type: post
id: 567
category:
    - 前端开发
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 鼠标事件

<table><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td>onclick</td><td>当用户点击某个对象时调用的事件句柄。</td></tr><tr><td>oncontextmenu</td><td>在用户点击鼠标右键打开上下文菜单时触发</td></tr><tr><td>ondblclick</td><td>当用户双击某个对象时调用的事件句柄。</td></tr><tr><td>onmousedown</td><td>鼠标按钮被按下。</td></tr><tr><td>onmouseenter</td><td>当鼠标指针移动到元素上时触发。</td></tr><tr><td>onmouseleave</td><td>当鼠标指针移出元素时触发</td></tr><tr><td>onmousemove</td><td>鼠标被移动。</td></tr><tr><td>onmouseover</td><td>鼠标移到某元素之上。</td></tr><tr><td>onmouseout</td><td>鼠标从某元素移开。</td></tr><tr><td>onmouseup</td><td>鼠标按键被松开。</td></tr></tbody></table>

##### 框架/对象（Frame/Object）事件

<table><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td>onabort</td><td>图像的加载被中断。 ( <object>)</object></td></tr><tr><td>onbeforeunload</td><td>该事件在即将离开页面（刷新或关闭）时触发</td></tr><tr><td>onerror</td><td>在加载文档或图像时发生错误。 ( <object>, 和 <frameset>)</frameset></object></td></tr><tr><td>onhashchange</td><td>该事件在当前 URL 的锚部分发生修改时触发。</td></tr><tr><td>onload</td><td>一张页面或一幅图像完成加载。</td></tr><tr><td>onpageshow</td><td>该事件在用户访问页面时触发</td></tr><tr><td>onpagehide</td><td>该事件在用户离开当前网页跳转到另外一个页面时触发</td></tr><tr><td>onresize</td><td>窗口或框架被重新调整大小。</td></tr><tr><td>onscroll</td><td>当文档被滚动时发生的事件。</td></tr><tr><td>onunload</td><td>用户退出页面。 ( 和 <frameset>)</frameset></td></tr></tbody></table>

##### 拖拽事件

<table><thead><tr><th>事件</th><th>描述</th></tr></thead><tbody><tr><td>ondrag</td><td>该事件在元素正在拖动时触发</td></tr><tr><td>ondragend</td><td>该事件在用户完成元素的拖动时触发</td></tr><tr><td>ondragenter</td><td>该事件在拖动的元素进入放置目标时触发</td></tr><tr><td>ondragleave</td><td>该事件在拖动元素离开放置目标时触发</td></tr><tr><td>ondragover</td><td>该事件在拖动元素在放置目标上时触发</td></tr><tr><td>ondragstart</td><td>该事件在用户开始拖动元素时触发</td></tr><tr><td>ondrop</td><td>该事件在拖动元素放置在目标区域时触发</td></tr></tbody></table>

##### 动画事件

<table><thead><tr><th>事件</th><th>描述</th></tr></thead><tbody><tr><td>animationend</td><td>该事件在 CSS 动画结束播放时触发</td></tr><tr><td>animationiteration</td><td>该事件在 CSS 动画重复播放时触发</td></tr><tr><td>animationstart</td><td>该事件在 CSS 动画开始播放时触发</td></tr></tbody></table>

##### 过渡事件

<table><thead><tr><th>事件</th><th>描述</th></tr></thead><tbody><tr><td>transitionend</td><td>该事件在 CSS 完成过渡后触发。</td></tr></tbody></table>

##### 其他事件

<table><thead><tr><th>事件</th><th>描述</th></tr></thead><tbody><tr><td>onmessage</td><td>该事件通过或者从对象(WebSocket, Web Worker, Event Source 或者子 frame 或父窗口)接收到消息时触发</td></tr><tr><td>onmousewheel</td><td>已废弃。 使用 onwheel 事件替代</td></tr><tr><td>ononline</td><td>该事件在浏览器开始在线工作时触发。</td></tr><tr><td>onoffline</td><td>该事件在浏览器开始离线工作时触发。</td></tr><tr><td>onpopstate</td><td>该事件在窗口的浏览历史（history 对象）发生改变时触发。</td></tr><tr><td>onshow</td><td>该事件当 <menu> 元素在上下文菜单显示时触发</menu></td></tr><tr><td>onstorage</td><td>该事件在 Web Storage(HTML 5 Web 存储)更新时触发</td></tr><tr><td>ontoggle</td><td>该事件在用户打开或关闭 <details> 元素时触发</details></td></tr><tr><td>onwheel</td><td>该事件在鼠标滚轮在元素上下滚动时触发</td></tr></tbody></table>

[节选自菜鸟教程](http://www.runoob.com/jsref/dom-obj-event.html)