---
title: "Node.js Express Web服务器 管理多目录静态资源文件"
date: "2018-02-11"
categories: 
  - "node-js"
---

### app.js

```javascript
var express = require('express');
var path = require('path');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');

var login = require('./routes/login');

var app = express();
//设置跨域访问
app.all('*', function (req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Content-Type,Content-Length, Authorization, Accept,X-Requested-With");
    res.header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS");
    res.header("X-Powered-By", ' 3.2.1')
    next();
});
// view engine setup
app.set('views', path.join(__dirname, 'views'));
// 让ejs能够识别后缀为 .html 的文件
app.engine('.html', require('ejs').__express);
// 在调用render函数时能自动为我们加上 .html 后缀。
// 如果不写，我们就得把res.render(‘users’)写成res.render(‘users.html’)，否则会报错。
app.set('view engine', 'html');

app.use(logger('dev'));
app.use(cookieParser());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));
// 指定多个目录为静态资源文件的访问目录
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.static(path.join(__dirname, 'public/libs')));

app.use('/', login);

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
