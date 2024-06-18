---
title: 'JavaScript  Blob'
date: '2020-12-27T07:36:35+00:00'
status: publish
permalink: /2020/12/27/javascript-blob
author: 毛巳煜
excerpt: ''
type: post
id: 6696
category:
    - JavaScript
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### [Blob 权威解释](https://developer.mozilla.org/zh-CN/docs/Web/API/Blob "Blob 权威解释")

###### 创建Blob对象，内容为一个json字符串

```javascript
var blob = new Blob(['{hello: "world"}'], {type : 'application/json'});

```

- - - - - -

###### js脚本中提取blob

```javascript
var text = await (new Response(blob)).text();
console.log(text);

// 输出： {hello: "world"}

```

- - - - - -

###### 在浏览器URL中直接打开，如果是图片也可用在dom的 `<img src="blob:%E5%9F%9F%E5%90%8D/%E9%9A%8F%E6%9C%BA%E7%94%9F%E6%88%90"></img>`

**[URL.createObjectURL()](https://developer.mozilla.org/zh-CN/docs/Web/API/URL/createObjectURL "URL.createObjectURL()")**

```javascript
// URL.createObjectURL() 静态方法会创建一个 DOMString，其中包含一个表示参数中给出的对象的URL。
// 这个 URL 的生命周期和创建它的窗口中的 document 绑定。
// 这个新的URL 对象表示指定的 File 对象或 Blob 对象。
var url = URL.createObjectURL(blob);
console.log(url);

// 输出： blob:null/e7272916-d870-4659-9d43-9d4a1f872a85
// 有效期为页面的存活期或者手动调用 URL.revokeObjectURL 回收数据，当数据回收之后，文件就会被删除。

// URL.revokeObjectURL() 静态方法用来释放一个之前已经存在的、通过调用 URL.createObjectURL() 创建的 URL 对象。
// 调用此方法后 blob:null/e7272916-d870-4659-9d43-9d4a1f872a85 的生命将被终结。
// 例如： window.URL.revokeObjectURL(url);

```

**[释放URL.createObjectURL() 创建的 URL 对象](https://developer.mozilla.org/zh-CN/docs/Web/API/URL/revokeObjectURL "释放URL.createObjectURL() 创建的 URL 对象")**

- - - - - -

- - - - - -

- - - - - -

###### 拦截 createObjectURL 创建销毁事件

```javascript
/**
 * 保留原始 createObjectURL 功能
 */
let <span class="katex math inline">createObjectURL = window.URL.createObjectURL;
/**
 * 重写 createObjectURL 对当前浏览器页面创建blob行为进行拦截
 * @param obj
 */
window.URL.createObjectURL = function (obj) {
    let url =</span>createObjectURL(obj);

    // console.log("createObjectURL obj:", obj);
    console.log("createObjectURL url:", url);
    return url
}

/**
 * 重写销毁事件，让它不能注销。也就是不能删除原来blob数据
 * @param url
 */
window.URL.revokeObjectURL = function (url) {
    // console.log("revokeObjectURL:", url)
}

```

- - - - - -

###### 拦截blob媒体流 `其实要实现视频流拦截，只需要重写这个事件就可以了， 要注意的是， 要在视频加载之前运行这段代码。`

```javascript
/**
 * 保留原始 addSourceBuffer 功能
 */
let <span class="katex math inline">addSourceBuffer = window.MediaSource.prototype.addSourceBuffer;
/**
 * 重写添加媒体资源事件，用来获取媒体的二进制数据。
 * @type {(function(*=))|*}
 */
window.MediaSource.prototype.addSourceBuffer = function (mimeCodec) {
    // console.log("MediaSource.addSourceBuffer ", mimeCodec);
    let sourceBuffer =</span>addSourceBuffer.call(this, mimeCodec);
    // 保留原始appendBuffer功能
    let <span class="katex math inline">appendBuffer = sourceBuffer.appendBuffer;
    // 重写 appendBuffer 拦截视频流
    sourceBuffer.appendBuffer = function (buffer) {
        // 输出视频流
        console.log(mimeCodec, buffer);</span>appendBuffer.call(this, buffer)
    }
    return sourceBuffer
}

```

- - - - - -

- - - - - -

- - - - - -