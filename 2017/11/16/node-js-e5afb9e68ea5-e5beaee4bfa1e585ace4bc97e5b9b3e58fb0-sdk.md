---
title: 'Node.js 对接 微信公众平台 SDK'
date: '2017-11-16T12:51:02+00:00'
status: publish
permalink: /2017/11/16/node-js-%e5%af%b9%e6%8e%a5-%e5%be%ae%e4%bf%a1%e5%85%ac%e4%bc%97%e5%b9%b3%e5%8f%b0-sdk
author: 毛巳煜
excerpt: ''
type: post
id: 214
category:
    - 移动端
tag: []
post_format: []
hestia_layout_select:
    - default
---
### 开发思路

[微信JS-SDK说明文档](https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421141115)

#### **JSSDK使用步骤**

**步骤一**：绑定域名  
先登录微信公众平台进入“公众号设置”的“功能设置”里填写“JS接口安全域名”。  
备注：登录后可在“开发者中心”查看对应的接口权限。

**步骤二**：引入JS文件  
在需要调用JS接口的页面引入如下JS文件，（支持https）：http://res.wx.qq.com/open/js/jweixin-1.2.0.js  
备注：支持使用 AMD/CMD 标准模块加载方法加载

**步骤三**：通过config接口注入权限验证配置

##### **所有需要使用JS-SDK的页面必须先注入配置信息，否则将无法调用（同一个url仅需调用一次，对于变化url的SPA的web app可在每次url变化时进行调用,目前Android微信客户端不支持pushState的H5新特性，所以使用pushState来实现web app的页面会导致签名失败，此问题会在Android6.2中修复）。**

```javascript
wx.config({
    debug: true, // 开启调试模式,调用的所有api的返回值会在客户端alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印。
    appId: '', // 必填，公众号的唯一标识
    timestamp: , // 必填，生成签名的时间戳
    nonceStr: '', // 必填，生成签名的随机串
    signature: '',// 必填，签名，见附录1
    jsApiList: [] // 必填，需要使用的JS接口列表，所有JS接口列表见附录2
});

```

**根据以上要求使用如下代码实现功能**

```javascript
/**
 * 这个文件 只是个示例 目前的应用方式是 将它放在Vue.js 里面一起打包的
 * Created by mao-siyu on 17-3-30.
 */
/* eslint-disable */
import axios from 'axios';
import urlFormat from 'url';
import sha1 from 'sha1'; // 安装sha1 加密模块
import wx from 'weixin-js-sdk'; // 安装微信SDK模块

const ticketUrl = 'http://www.private-blog.com/getJsApiTicket';

// 获取当前时间戳
var timestamp = new Date().getTime().toString().substr(0, 10);

/**
 * 自定义UUID
 * @returns {string}
 * @constructor
 */
let UUID = (len, radix) => {
    var chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'.split('');
    var uuid = [], i;
    radix = radix || chars.length;
    if (len) {
        // Compact form
        for (i = 0; i  {
    return new Promise((resolve, reject) => {
        axios.get(ticketUrl).then((response) => {
            resolve(response.data);
        });
    });
}

/**
 * 获取 sign Promise
 * @param ticket
 * @param uuid
 * @param timestamp
 * @param url
 * @returns {Promise}
 */
var getSign = (ticket, noncestr, timestamp, url) => {
    return new Promise((resolve, reject) => {
        var sign = {};
        sign.jsapi_ticket = ticket;
        sign.noncestr = noncestr;
        sign.timestamp = timestamp;
        var string1 = urlFormat.format({query: sign}) + '&url=' + url;
        // 使用 sha1 加密
        var signature = sha1(string1.replace(/^\?/gi, ''));
        resolve([noncestr, timestamp, signature]);
    });
}

/**
 * 获取 wxconfig Promise
 * @param debug 开启调试模式,调用的所有api的返回值会在客户端alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印。
 * @param appId 必填，公众号的唯一标识
 * @param noncestr 必填，生成签名的时间戳
 * @param timestamp 必填，生成签名的随机串
 * @param signature 必填，签名
 * @param jsApiList
 * @returns {Promise}
 */
let wxconfig = (debug, appId, noncestr, timestamp, signature, jsApiList) => {
    return new Promise((resolve, reject) => {
        wx.config({
            debug: debug,
            appId: appId,
            timestamp: timestamp,
            nonceStr: noncestr,
            signature: signature,
            jsApiList: jsApiList
        });
        resolve(wx);
    });
}

let weixinSDK = function () {
}

weixinSDK.config = (debug, appId, jsApiList, url, callback) => {
    getTicket().then((ticket) => {
        return getSign(ticket, UUID(16), timestamp, url);
    }).then((data) => {
        return wxconfig(debug, appId, data[0], data[1], data[2], jsApiList);
    }).then((wx) => {
        callback(wx);
    }).catch((err) => {
    });
}

// *#*# 使用方法 example #*#*
// <script>
// var jsApiList = [
//   'checkJsApi',
//   'onMenuShareTimeline',
//   'onMenuShareAppMessage',
//   'onMenuShareQQ',
//   'onMenuShareWeibo'
// ];
//
// // &#31614;&#21517;&#22320;&#22336;&#24517;&#39035;&#19982;&#24403;&#21069;&#39029;&#38754;&#22320;&#22336;&#19968;&#33268;&#65292;&#25165;&#33021;&#31614;&#21517;&#25104;&#21151;&#30340;, &#25152;&#20197;&#35201;&#21160;&#24577;&#30340;&#33719;&#21462;url&#22320;&#22336;
// var url = window.location.href;
//
// weixinSDK.config(true, 'wxc61466f393b037a1', jsApiList, url, (wx) => {
//
//   wx.ready(() => {
//     // &#20998;&#20139;&#21040;&#26379;&#21451;&#22280;
//     wx.onMenuShareTimeline({
//       title: '&#20998;&#20139;&#21040;&#26379;&#21451;&#22280;', // &#20998;&#20139;&#26631;&#39064;
//       link: 'http://www.itfactory.wang', // &#20998;&#20139;&#38142;&#25509;
//       imgUrl: 'http://pic6.huitu.com/res/20130116/84481_20130116142820494200_1.jpg', // &#20998;&#20139;&#22270;&#26631;
//       success: function () {
//         // &#29992;&#25143;&#30830;&#35748;&#20998;&#20139;&#21518;&#25191;&#34892;&#30340;&#22238;&#35843;&#20989;&#25968;
//       },
//       cancel: function () {
//         // &#29992;&#25143;&#21462;&#28040;&#20998;&#20139;&#21518;&#25191;&#34892;&#30340;&#22238;&#35843;&#20989;&#25968;
//       }
//     });
//
//     // &#20998;&#20139;&#32473;&#26379;&#21451;
//     wx.onMenuShareAppMessage({
//       title: '&#20998;&#20139;&#32473;&#26379;&#21451;', // &#20998;&#20139;&#26631;&#39064;
//       link: 'http://www.itfactory.wang', // &#20998;&#20139;&#38142;&#25509;
//       imgUrl: 'http://pic6.huitu.com/res/20130116/84481_20130116142820494200_1.jpg', // &#20998;&#20139;&#22270;&#26631;
//       desc: '&#20998;&#20139;&#25551;&#36848;', // &#20998;&#20139;&#25551;&#36848;
//       type: '', // &#20998;&#20139;&#31867;&#22411;,music&#12289;video&#25110;link&#65292;&#19981;&#22635;&#40664;&#35748;&#20026;link
//       dataUrl: '', // &#22914;&#26524;type&#26159;music&#25110;video&#65292;&#21017;&#35201;&#25552;&#20379;&#25968;&#25454;&#38142;&#25509;&#65292;&#40664;&#35748;&#20026;&#31354;
//       success: function () {
//         // &#29992;&#25143;&#30830;&#35748;&#20998;&#20139;&#21518;&#25191;&#34892;&#30340;&#22238;&#35843;&#20989;&#25968;
//       },
//       cancel: function () {
//         // &#29992;&#25143;&#21462;&#28040;&#20998;&#20139;&#21518;&#25191;&#34892;&#30340;&#22238;&#35843;&#20989;&#25968;
//       }
//     });
//
//     // &#20998;&#20139;&#32473;&#25163;&#26426;QQ
//     wx.onMenuShareQQ({
//       title: '&#20998;&#20139;&#32473;&#25163;&#26426;QQ', // &#20998;&#20139;&#26631;&#39064;
//       link: 'http://www.itfactory.wang', // &#20998;&#20139;&#38142;&#25509;
//       imgUrl: 'http://pic6.huitu.com/res/20130116/84481_20130116142820494200_1.jpg', // &#20998;&#20139;&#22270;&#26631;
//       desc: '&#20998;&#20139;&#25551;&#36848;', // &#20998;&#20139;&#25551;&#36848;
//       success: function () {
//         // &#29992;&#25143;&#30830;&#35748;&#20998;&#20139;&#21518;&#25191;&#34892;&#30340;&#22238;&#35843;&#20989;&#25968;
//       },
//       cancel: function () {
//         // &#29992;&#25143;&#21462;&#28040;&#20998;&#20139;&#21518;&#25191;&#34892;&#30340;&#22238;&#35843;&#20989;&#25968;
//       }
//     });
//   });
// });
// </script>

export default weixinSDK;


```