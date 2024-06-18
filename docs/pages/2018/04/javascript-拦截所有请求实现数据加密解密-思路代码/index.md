---
title: "JavaScript 拦截所有请求实现数据加密解密 思路代码"
date: "2018-04-20"
categories: 
  - "javascript"
---

```javascript
/**
 * 数组扩展： 判断数组是否包含某一个元素
 * @param needle
 * @returns {boolean}
 */
;Array.prototype.contains = function (needle) {
    for (i in this) {
        if (this[i] === needle)
            return true;
    }
    return false;
}

/**
 * 字符串扩展： 判断字符串中是否包含某个字符
 * @param needle
 * @returns {boolean}
 */
;String.prototype.contains = function (str) {
    return new RegExp(this).test(str);
}

/** ============================================================================ */

/**
 * 拦截所有 http请求
 * ajaxhook.js 三方插件
 */
;!function (obj) {
    obj.hookAjax = function (funs) {
        window._ahrealxhr = window._ahrealxhr || XMLHttpRequest
        XMLHttpRequest = function () {
            this.xhr = new window._ahrealxhr;
            for (var attr in this.xhr) {
                var type = '';
                try {
                    type = typeof this.xhr[attr]
                } catch (e) {
                    console.log(e);
                }
                if (type === 'function') {
                    this[attr] = hookfun(attr);
                } else {
                    Object.defineProperty(this, attr, {
                        get: getFactory(attr),
                        set: setFactory(attr)
                    })
                }
            }
        }

        function getFactory(attr) {
            return function () {
                return this.hasOwnProperty(attr + '_') ? this[attr + '_'] : this.xhr[attr];
            }
        }

        function setFactory(attr) {
            return function (f) {
                var xhr = this.xhr;
                var that = this;
                if (attr.indexOf('on') != 0) {
                    this[attr + '_'] = f;
                    return;
                }
                if (funs[attr]) {
                    xhr[attr] = function () {
                        funs[attr](that) || f.apply(xhr, arguments);
                    }
                } else {
                    xhr[attr] = f;
                }
            }
        }

        function hookfun(fun) {
            return function () {
                var args = [].slice.call(arguments)
                if (funs[fun] && funs[fun].call(this, args, this.xhr)) {
                    return;
                }
                return this.xhr[fun].apply(this.xhr, args);
            }
        }

        return window._ahrealxhr;
    }
    obj.unHookAjax = function () {
        if (window._ahrealxhr) XMLHttpRequest = window._ahrealxhr;
        window._ahrealxhr = undefined;
    }
}(window);

/** ============================================================================ */

/**
 * 自定义 日志
 * @type {{level: number, debug: Logger.debug, info: Logger.info, warn: Logger.warn, error: Logger.error}}
 */
var Logger = {
    level: 1,
    debug: function (message) {
        if (this.level <= 1)
            console.log('%c ' + message, 'font-size:12px;color:rgba(65,105,225,255)');
    },
    info: function (message) {
        if (this.level <= 2)
            console.log('%c ' + message, 'font-size:12px;color:rgba(60,179,113,255)');
    },
    warn: function (message) {
        if (this.level <= 3)
            console.log('%c ' + message, 'font-size:12px;color:rgba(218,165,32,255)');
    },
    error: function (message) {
        if (this.level <= 4)
            console.log('%c ' + message, 'font-size:12px;color:rgba(255,0,0,255)');
    },
};

/** ============================================================================ */

/**
 * Http 所有请求的过滤器
 * @constructor
 */
;!function HttpFilters() {

    // 自动拦截所有请求数据，重写 XMLHttpRequest.prototype.send 方法
    (function (send) {
        XMLHttpRequest.prototype.send = function (data) {
            Logger.debug('URL: ' + this.getUrl());
            Logger.debug('Method: ' + this.getMethod());
            Logger.debug('Data: ' + data);
            // 在这里对所有请求数据进行拦截，做相应的处理
            send.call(this, encryption(this.getUrl(), this.getMethod(), data));
        };
    })(XMLHttpRequest.prototype.send);

    /**
     * 使用三方插件拦截请求
     */
    hookAjax({
        // 在这里可以实现自动追加签名
        open: function (arg, xhr) {
            /**
             * 将获取Url 并存放到 XHR对象中
             * @returns {*}
             */
            xhr.getUrl = function () {
                return arg[1];
            }
            /**
             * 将获取Url 请求类型 并存放到 XHR对象中
             * @returns {*}
             */
            xhr.getMethod = function () {
                return arg[0];
            }
        },
        onload: function (xhr) {
            xhr.responseText = decryption(xhr.xhr.getUrl(), xhr.xhr.getMethod(), xhr.response);
        },
    });
}();

/**
 * 加密处理
 * @param url 请求地址
 * @param method 请求类型
 * @param data 所有请求的数据
 */
function encryption(url, method, data) {
    Logger.info('进入数据加密方法！');
    // 根据 请求类型 判断数据是否需要AES加密
    switch (method) {
        case 'GET':
        case 'DELETE':
            Logger.info('该请求类型，数据不需要AES加密！');
            return data;
    }

    // 白名单
    var whiteList = ['/getPublicKey'];

    // 根据 url 判断数据是否需要AES加密
    // /getPublicKey 是获取服务端公钥请求 不需要AES加密
    if (url.contains('/getPublicKey')) {
        Logger.debug('获取服务端公钥请求 不需要AES加密！');
        return data;
    }
    // /uploadShareKey 是将共享密钥与浏览器唯一标识上传给服务器的请求 不需要AES加密 但需要RSA加密
    else if (url.contains('/uploadShareKey')) {
        Logger.debug('将共享密钥与浏览器唯一标识上传给服务器的请求 不需要AES加密 但需要RSA加密！');
        var encrypted = RSAUtil.encryption(data, 'publicKey');
        return encrypted;
    }
    // 判断是否是白名单中的请求 如果是也不需要进行AES加密
    else if (whiteList.contains(url)) {
        Logger.debug('该请求为白名单中地址 不需要AES加密！');
        return data;
    }
    // 其它的数据都需要AES加密
    else {
        Logger.debug('其它请求数据需要进行AES加密！');
        // 数据加密之前需要使用 encodeURIComponent 进行编码 防止数据出现意外问题
        // data = encodeURIComponent(data);
        // var encrypted = AESUtil.encryption(data, localStorage.getItem('shareKey'));
        return data;
    }
}

/**
 * 解密处理
 * @param url 请求地址
 * @param method 请求类型
 * @param data 所有请求的数据
 */
function decryption(url, method, data) {
    Logger.info('进入数据解密方法！');
    // 根据 请求类型 判断数据是否需要AES解密
    switch (method) {
        case 'GET':
        case 'DELETE':
            Logger.info('该请求类型，数据不需要AES解密！');
            return data;
    }

    // 白名单
    var whiteList = ['/getPublicKey'];

    // 根据 url 判断数据是否需要AES解密
    // /getPublicKey 是获取服务端公钥请求 该响应不需要AES解密
    if (url.contains('/getPublicKey')) {
        Logger.debug('获取服务端公钥请求 该响应不需要AES解密！');
        return data;
    }
    // /uploadShareKey 是将共享密钥与浏览器唯一标识上传给服务器的请求 该响应不需要AES解密
    else if (url.contains('/uploadShareKey')) {
        Logger.debug('将共享密钥与浏览器唯一标识上传给服务器的请求 该响应不需要AES解密！');
        var encrypted = RSAUtil.encryption(data, 'publicKey');
        return encrypted;
    }
    // 判断是否是白名单中的请求 如果是也不需要进行AES解密
    else if (whiteList.contains(url)) {
        Logger.debug('该请求为白名单中地址 该响应不需要AES解密！');
        return data;
    }
    // 其它的数据都需要AES解密
    else {
        Logger.debug('其它响应数据需要进行AES解密！');
        // 数据解密之前需要使用 decodeURIComponent 进行编码 防止数据出现意外问题
        // data = decodeURIComponent(data);
        // var encrypted = AESUtil.encryption(data, localStorage.getItem('shareKey'));
        return data;
    }
}

/** ============================================================================ */


```
