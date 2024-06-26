---
title: "Node.js 对接 微信公众平台 SDK"
date: "2017-11-16"
categories: 
  - "移动端"
---

### 开发思路

[微信JS-SDK说明文档](https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421141115)

#### **JSSDK使用步骤**

**步骤一**：绑定域名 先登录微信公众平台进入“公众号设置”的“功能设置”里填写“JS接口安全域名”。 备注：登录后可在“开发者中心”查看对应的接口权限。

**步骤二**：引入JS文件 在需要调用JS接口的页面引入如下JS文件，（支持https）：http://res.wx.qq.com/open/js/jweixin-1.2.0.js 备注：支持使用 AMD/CMD 标准模块加载方法加载

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
        for (i = 0; i < len; i++) uuid[i] = chars[0 | Math.random() * radix];
    } else {
        // rfc4122, version 4 form
        var r;
        // rfc4122 requires these characters
        uuid[8] = uuid[13] = uuid[18] = uuid[23] = '-';
        uuid[14] = '4';
        // Fill in random data.  At i==19 set the high bits of clock sequence as
        // per rfc4122, sec. 4.1.5
        for (i = 0; i < 36; i++) {
            if (!uuid[i]) {
                r = 0 | Math.random() * 16;
                uuid[i] = chars[(i == 19) ? (r & 0x3) | 0x8 : r];
            }
        }
    }
    return uuid.join('');
}

/**
 * 获取 ticket Promise
 * @param accessToken
 * @returns {Promise}
 */
let getTicket = () => {
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
// // 签名地址必须与当前页面地址一致，才能签名成功的, 所以要动态的获取url地址
// var url = window.location.href;
//
// weixinSDK.config(true, 'wxc61466f393b037a1', jsApiList, url, (wx) => {
//
//   wx.ready(() => {
//     // 分享到朋友圈
//     wx.onMenuShareTimeline({
//       title: '分享到朋友圈', // 分享标题
//       link: 'http://www.itfactory.wang', // 分享链接
//       imgUrl: 'http://pic6.huitu.com/res/20130116/84481_20130116142820494200_1.jpg', // 分享图标
//       success: function () {
//         // 用户确认分享后执行的回调函数
//       },
//       cancel: function () {
//         // 用户取消分享后执行的回调函数
//       }
//     });
//
//     // 分享给朋友
//     wx.onMenuShareAppMessage({
//       title: '分享给朋友', // 分享标题
//       link: 'http://www.itfactory.wang', // 分享链接
//       imgUrl: 'http://pic6.huitu.com/res/20130116/84481_20130116142820494200_1.jpg', // 分享图标
//       desc: '分享描述', // 分享描述
//       type: '', // 分享类型,music、video或link，不填默认为link
//       dataUrl: '', // 如果type是music或video，则要提供数据链接，默认为空
//       success: function () {
//         // 用户确认分享后执行的回调函数
//       },
//       cancel: function () {
//         // 用户取消分享后执行的回调函数
//       }
//     });
//
//     // 分享给手机QQ
//     wx.onMenuShareQQ({
//       title: '分享给手机QQ', // 分享标题
//       link: 'http://www.itfactory.wang', // 分享链接
//       imgUrl: 'http://pic6.huitu.com/res/20130116/84481_20130116142820494200_1.jpg', // 分享图标
//       desc: '分享描述', // 分享描述
//       success: function () {
//         // 用户确认分享后执行的回调函数
//       },
//       cancel: function () {
//         // 用户取消分享后执行的回调函数
//       }
//     });
//   });
// });
// </script>

export default weixinSDK;

```
