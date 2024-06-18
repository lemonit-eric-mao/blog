---
title: 'JavaScript 拦截所有请求实现数据加密解密 思路代码'
date: '2018-04-20T14:41:09+00:00'
status: publish
permalink: /2018/04/20/javascript-%e6%8b%a6%e6%88%aa%e6%89%80%e6%9c%89%e8%af%b7%e6%b1%82%e5%ae%9e%e7%8e%b0%e6%95%b0%e6%8d%ae%e5%8a%a0%e5%af%86%e8%a7%a3%e5%af%86-%e6%80%9d%e8%b7%af%e4%bb%a3%e7%a0%81
author: 毛巳煜
excerpt: ''
type: post
id: 2097
category:
    - JavaScript
tag: []
post_format: []
hestia_layout_select:
    - default
---
```
<pre class="line-numbers prism-highlight" data-start="1">```javascript
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
        if (this.level 
```
```