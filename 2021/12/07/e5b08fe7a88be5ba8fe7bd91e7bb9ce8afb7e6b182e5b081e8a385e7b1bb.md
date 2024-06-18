---
title: 小程序网络请求封装类
date: '2021-12-07T09:12:09+00:00'
status: private
permalink: /2021/12/07/%e5%b0%8f%e7%a8%8b%e5%ba%8f%e7%bd%91%e7%bb%9c%e8%af%b7%e6%b1%82%e5%b0%81%e8%a3%85%e7%b1%bb
author: 毛巳煜
excerpt: ''
type: post
id: 8196
category:
    - 移动端
tag: []
post_format: []
---
```javascript
/**
 * 小程序网络请求封装类
 *
 * 2021-12-07
 * author 毛巳煜
 */
class <span class="katex math inline">axios {

    constructor() {
        this.baseUrl = 'http://172.16.15.217:8088'
    }

    GET(urlPath, data) {
        return new Promise((resolve, reject) => {
            let url = `</span>{this.baseUrl}/<span class="katex math inline">{urlPath || ''}`;
            this.request('GET', url, data, resolve, reject);
        });
    }

    POST(urlPath, data) {
        return new Promise((resolve, reject) => {
            let url = `</span>{this.baseUrl}/<span class="katex math inline">{urlPath || ''}`;
            this.request('POST', url, data, resolve, reject);
        });
    }

    PUT(urlPath, data) {
        return new Promise((resolve, reject) => {
            let url = `</span>{this.baseUrl}/<span class="katex math inline">{urlPath || ''}`;
            this.request('PUT', url, data, resolve, reject);
        });
    }

    DELETE(urlPath, data) {
        return new Promise((resolve, reject) => {
            let url = `</span>{this.baseUrl}/<span class="katex math inline">{urlPath || ''}`;
            this.request('DELETE', url, data, resolve, reject);
        });
    }

    /**
     * 微信原生请求
     * @param {*} method
     * @param {*} url
     * @param {*} data
     * @param {*} resolve
     * @param {*} reject
     */
    request(method, url, data, resolve, reject) {

        wx.request({
            url: url,
            data: data,
            method: method,
            dataType: 'json',
            responseType: 'text',
            header: {
                'content-type': 'application/json'
            },
            // 接口调用成功的回调函数
            success(data) {
                resolve(data)
            },
            // 接口调用失败的回调函数
            fail(err) {
                reject(err)
            }
        })
    }

}

module.exports = new</span>axios();

/**
 * 使用示例:
 *
 * // 请求参数
 * let data = {
 *     appId: 'wx2cce45912ba3d550',
 *     appSecret: '1b42f60535509150aa0daa5710341c98',
 *     code: res.code
 * }
 *
 * // 向服务端请求
 * let result = await $axios.GET('weixin/jscode2session', data)
 */


```