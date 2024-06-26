---
title: "axios.defaults.headers.common 引发的异常"
date: "2017-11-16"
categories: 
  - "vue"
---

#### 请求Node.js 服务器地址 http://10.32.159.219:3100/getJsApiTicket 出现如下异常:

> XMLHttpRequest cannot load http://10.32.159.219:3100/getJsApiTicket. Request header field MyToken is not allowed by Access-Control-Allow-Headers in preflight response.

### axios 的请求代码

```javascript
        axios.defaults.headers.common['MyToken'] = '123456789';
        axios.get('http://10.32.159.219:3100/getJsApiTicket').then(function (response) {
            console.log(response.data);
        }).catch(function (error) {
            console.log(error);
            return false;
        });
```

### app.js 服务器已经做了请求的跨域 处理

```javascript
var app = express();
app.all('*', function (req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Content-Type,Content-Length, Authorization, Accept,X-Requested-With,");
    res.header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS");
    res.header("X-Powered-By", '3.2.1');
    res.header("Content-Type", "application/json;charset=utf-8");
    next();
});
```

### 根据异常信息做对应修改

```javascript
var app = express();
app.all('*', function (req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "*");
    res.header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS");
    res.header("X-Powered-By", '3.2.1');
    res.header("Content-Type", "application/json;charset=utf-8");
    next();
});

//  修改为: Access-Control-Allow-Headers 改为 * 星号 变为通配, 结果还是不对
```

###

```javascript
var app = express();
app.all('*', function (req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Content-Type,Content-Length, Authorization, Accept,X-Requested-With, MyToken");
    res.header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS");
    res.header("X-Powered-By", '3.2.1');
    res.header("Content-Type", "application/json;charset=utf-8");
    next();
});

// 在 Access-Control-Allow-Headers 中添加 MyToken 问题解决
// 也可以写成这样
res.header("Access-Control-Allow-Headers", "*, MyToken");

```

### 总结 :

**我认为 星号的通配是指所有内置的匹配参数, 而并不上真正的匹配所有, 所以自己定义的headers参数, 需要明确指定**\]>
