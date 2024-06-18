---
title: "HTML 常用DOM 事件"
date: "2017-11-16"
categories: 
  - "前端开发"
---

##### 鼠标事件

| 属性 | 描述 |
| --- | --- |
| onclick | 当用户点击某个对象时调用的事件句柄。 |
| oncontextmenu | 在用户点击鼠标右键打开上下文菜单时触发 |
| ondblclick | 当用户双击某个对象时调用的事件句柄。 |
| onmousedown | 鼠标按钮被按下。 |
| onmouseenter | 当鼠标指针移动到元素上时触发。 |
| onmouseleave | 当鼠标指针移出元素时触发 |
| onmousemove | 鼠标被移动。 |
| onmouseover | 鼠标移到某元素之上。 |
| onmouseout | 鼠标从某元素移开。 |
| onmouseup | 鼠标按键被松开。 |

##### 框架/对象（Frame/Object）事件

| 属性 | 描述 |
| --- | --- |
| onabort | 图像的加载被中断。 ( ) |
| onbeforeunload | 该事件在即将离开页面（刷新或关闭）时触发 |
| onerror | 在加载文档或图像时发生错误。 ( , 和 ) |
| onhashchange | 该事件在当前 URL 的锚部分发生修改时触发。 |
| onload | 一张页面或一幅图像完成加载。 |
| onpageshow | 该事件在用户访问页面时触发 |
| onpagehide | 该事件在用户离开当前网页跳转到另外一个页面时触发 |
| onresize | 窗口或框架被重新调整大小。 |
| onscroll | 当文档被滚动时发生的事件。 |
| onunload | 用户退出页面。 ( 和 ) |

##### 拖拽事件

| 事件 | 描述 |
| --- | --- |
| ondrag | 该事件在元素正在拖动时触发 |
| ondragend | 该事件在用户完成元素的拖动时触发 |
| ondragenter | 该事件在拖动的元素进入放置目标时触发 |
| ondragleave | 该事件在拖动元素离开放置目标时触发 |
| ondragover | 该事件在拖动元素在放置目标上时触发 |
| ondragstart | 该事件在用户开始拖动元素时触发 |
| ondrop | 该事件在拖动元素放置在目标区域时触发 |

##### 动画事件

| 事件 | 描述 |
| --- | --- |
| animationend | 该事件在 CSS 动画结束播放时触发 |
| animationiteration | 该事件在 CSS 动画重复播放时触发 |
| animationstart | 该事件在 CSS 动画开始播放时触发 |

##### 过渡事件

| 事件 | 描述 |
| --- | --- |
| transitionend | 该事件在 CSS 完成过渡后触发。 |

##### 其他事件

| 事件 | 描述 |
| --- | --- |
| onmessage | 该事件通过或者从对象(WebSocket, Web Worker, Event Source 或者子 frame 或父窗口)接收到消息时触发 |
| onmousewheel | 已废弃。 使用 onwheel 事件替代 |
| ononline | 该事件在浏览器开始在线工作时触发。 |
| onoffline | 该事件在浏览器开始离线工作时触发。 |
| onpopstate | 该事件在窗口的浏览历史（history 对象）发生改变时触发。 |
| onshow | 该事件当
元素在上下文菜单显示时触发

 |
| onstorage | 该事件在 Web Storage(HTML 5 Web 存储)更新时触发 |
| ontoggle | 该事件在用户打开或关闭 元素时触发 |
| onwheel | 该事件在鼠标滚轮在元素上下滚动时触发 |

[节选自菜鸟教程](http://www.runoob.com/jsref/dom-obj-event.html)
