---
title: "Node.js express 心跳服务器"
date: "2017-11-16"
categories: 
  - "移动端"
---

### 项目功能

**因为公众平台获取 access\_token 和 api\_ticket 时，每天是的访问次数限制，因此，自己需要在写一个可以延长 access\_token 和 api\_ticket 使用次数的程序。**

```javascript
const url = require('url');
const express = require('express');
const router = express.Router();
const request = require('superagent');
const schedule = require('node-schedule');
const rule = new schedule.RecurrenceRule();

// 定义可全局访问的属性
global.accessToken;
global.jsApiTicket;

/**
 * 获取 token Promise
 * @param url
 * @returns {Promise}
 */
const getToken = () => {

    let tokenUrl = url.format({
        protocol: 'https:',
        hostname: 'api.weixin.qq.com',
        pathname: '/cgi-bin/token',
        query: {
            grant_type: 'client_credential',
            appid: 'your appid', // 只需要修改这里
            secret: 'your secret' // 只需要修改这里
        }
    });

    return new Promise((resolve, reject) => {
        request.get(tokenUrl).end((err, response) => {
            // 失败
            if (err)
                reject(err);
            // 成功
            resolve(JSON.parse(response.text).access_token);
        });
    });
}

/**
 * 获取 ticket Promise
 * @param accessToken
 * @returns {Promise}
 */
const getTicket = () => {

    let ticketUrl = url.format({
        protocol: 'https:',
        hostname: 'api.weixin.qq.com',
        pathname: '/cgi-bin/ticket/getticket',
        query: {
            access_token: accessToken,
            type: 'jsapi'
        }
    });

    return new Promise((resolve, reject) => {
        request.get(ticketUrl).end((err, response) => {
            if (err)
                reject(err);
            // 成功
            resolve(JSON.parse(response.text).ticket);
        });
    });
};

/**
 * 初始化
 */
const init = async () => {
    try {
        accessToken = await getToken();
        jsApiTicket = await getTicket();
    } catch (e) {
        throw '微信JS_SDK获取异常 ' + e;
    }
}

// 执行初始化
init();

/**
 * 定时器
 * @returns {Promise}
 */
rule.minute = [];
// 一小时取一次
rule.minute.push(59);

const startTimers = () => {
    // 每小时的 59分钟会调用一次
    schedule.scheduleJob(rule, (data) => {
        init();
    });
};
// 开启定时器
startTimers();

/* Get Access Token. */
router.get('/getAccessToken', (req, res, next) => {
    res.send(accessToken);
});

/* Get jsapi ticket. */
router.get('/getJsApiTicket', (req, res, next) => {
    res.send(jsApiTicket);
});

module.exports = router;
```

### app.js

```javascript
var express = require('express');
var path = require('path');
var logger = require('morgan');
var bodyParser = require('body-parser');

// 模块引入
var getWxJsSDK = require('./routes/get_WX_JS_SDK');

var app = express();
app.all('*', function (req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Content-Type,Content-Length, Authorization, Accept,X-Requested-With");
    res.header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS");
    res.header("X-Powered-By", ' 3.2.1')
    next();
});

app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));

app.use('/', getWxJsSDK);

// catch 404 and forward to error handler
app.use(function (req, res, next) {
    var err = new Error('Not Found');
    err.status = 404;
    next(err);
});

// error handler
app.use(function (err, req, res, next) {
    // set locals, only providing error in development
    res.locals.message = err.message;
    res.locals.error = req.app.get('env') === 'development' ? err : {};

    // render the error page
    res.status(err.status || 500);
    res.render('error');
});

module.exports = app;
```
