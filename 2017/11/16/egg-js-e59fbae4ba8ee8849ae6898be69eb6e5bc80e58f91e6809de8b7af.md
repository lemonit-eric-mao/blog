---
title: 'Egg.js 基于脚手架开发思路'
date: '2017-11-16T12:32:51+00:00'
status: publish
permalink: /2017/11/16/egg-js-%e5%9f%ba%e4%ba%8e%e8%84%9a%e6%89%8b%e6%9e%b6%e5%bc%80%e5%8f%91%e6%80%9d%e8%b7%af
author: 毛巳煜
excerpt: ''
type: post
id: 178
category:
    - node.js
tag: []
post_format: []
hestia_layout_select:
    - default
---
代码填充思路
------

由于使用 egg-init egg-example --type=simple 快速生成项目, 接下来就是靠自己去填充, 所以记录下填充代码的思路.

### 按顺序从上到下

```
  配置路由                         app/router.js
  拆分路由                         app/router/*.js
  添加controller                  app/controller/*,js
  添加service                     app/service/*.js
  配置中间件                       app/middleware/*.js
  激活中间件                       app/config/plugin.js
  默认配置                         app/config/config.default.js
  视图模板                         app/view/*.html
  静态资源                         app/public/
  添加数据库

```