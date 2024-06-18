---
title: "nuxt.js 静态服务器 部署"
date: "2017-12-14"
categories: 
  - "vue"
---

###### 开发好的项目 部署到测试服务器

###### 在nuxt.js项目中执行如下命令 在项目根目录会生成 dist

```ruby
mao-siyu:/home$ npm run build
mao-siyu:/home$ npm run generate
```

* * *

###### 使用express 搭建 运行dist的 静态服务器

```ruby
mao-siyu:/home$ tree
.
├── app.js
├── bin
│   └── www
├── dist
├── package.json
└── routes
    └── index.js

3 directories, 4 files
mao-siyu:/home$
```

* * *

###### package.json

```json
{
  "name": "dist-server",
  "version": "0.0.0",
  "private": true,
  "scripts": {
    "start": "node ./bin/www"
  },
  "dependencies": {
    "body-parser": "~1.15.2",
    "debug": "~2.2.0",
    "express": "^4.14.1",
    "morgan": "~1.7.0"
  }
}
```

* * *

###### app.js

```ruby
const bodyParser = require('body-parser');
const express = require('express');
const logger = require('morgan');
const path = require('path');

// 模块引入
const index = require('./routes/index');

const app = express();
/*******************************************/
// 将html的渲染路径直接 指向dist 这样就方便多了
app.use(express.static(path.join(__dirname, '/dist')));
/*******************************************/
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));

app.use('/', index);

module.exports = app;
```

* * *

###### 将nuxt.js 项目的 dist文件 替换 express 中的 dist文件即可
