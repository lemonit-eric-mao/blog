---
title: "Egg.js 基于脚手架开发思路"
date: "2017-11-16"
categories: 
  - "node-js"
---

## 代码填充思路

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
