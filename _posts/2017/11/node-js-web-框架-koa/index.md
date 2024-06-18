---
title: "Node.js web 框架 KOA"
date: "2017-11-16"
categories: 
  - "node-js"
---

## **安装**

Koa 当前需要 node 0.11.x 并开启 --harmony (或--harmony-generators), 因为它依赖于 ES6 的 generator 特性. 如果你的当前 Node 版本小于 0.11, 可以通过 n (node 版本管理工具) 快速安装 0.11.x

```ruby
$ npm install -g n
$ n 0.11.12
$ node --harmony my-koa-app.js
```

为了方便，可以将 node 设置为默认启动 harmony 模式的别名：

```ruby
alias node='node --harmony'
```

还可以使用 gnode 运行程序, 但执行效率会较低.

## **Application**

Koa 应用是一个包含中间件 generator 方法数组的对象。当请求到来时, 这些方法会以 stack-like 的顺序执行, 从这个角度来看，Koa 和其他中间件系统（比如 Ruby Rack 或者 Connect/Express ）非常相似. 然而 Koa 的一大设计理念是: 通过其他底层中间件层提供高级「语法糖」，而不是Koa. 这大大提高了框架的互操作性和健壮性, 并让中间件开发变得简单有趣.

比如内容协商（content-negotation）、缓存控制（cache freshness）、反向代理（proxy support）重定向等常见功能都由中间件来实现. 将类似常见任务分离给中间件实现, Koa 实现了异常精简的代码.

一如既往的 Hello world:

```javascript
/**
 * Created by mao-siyu on 17-7-6.
 */
var koa = require('koa');
var app = new koa();

app.use(function *() {
    this.body = 'Hello World';
});

app.listen(3000);
```

### **启动脚本**

```ruby
mao-siyu@mao-siyu-PC:~/文档/code/koa-example$ alias koa='node --harmony'
mao-siyu@mao-siyu-PC:~/文档/code/koa-example$ koa app.js
koa deprecated Support for generators will be removed in v3. See the documentation for examples of how to convert old middleware https://github.com/koajs/koa/blob/master/docs/migration.md app.js:7:5
```

原文连接: [Node.js web 框架 KOA](http://koa.rednode.cn/)

### 使用 生成器创建项目

```ruby
mao-siyu@mao-siyu-PC:~$ sudo cnpm install koa-generator -g
mao-siyu@mao-siyu-PC:~$ koa my-koa
mao-siyu@mao-siyu-PC:~$ cd my-koa
mao-siyu@mao-siyu-PC:~/my-koa$ ll
总用量 32
drwxr-xr-x  6 mao-siyu mao-siyu 4096 3月  13 16:25 ./
drwxr-xr-x 77 mao-siyu mao-siyu 4096 3月  13 16:25 ../
-rw-rw-r-- 1 mao-siyu mao-siyu  900 3月  13 16:25 app.js
drwxr-xr-x  2 mao-siyu mao-siyu 4096 3月  13 16:25 bin/
-rw-rw-r-- 1 mao-siyu mao-siyu  613 3月  13 16:25 package.json
drwxr-xr-x  5 mao-siyu mao-siyu 4096 3月  13 16:25 public/
drwxr-xr-x  2 mao-siyu mao-siyu 4096 3月  13 16:25 routes/
drwxr-xr-x  2 mao-siyu mao-siyu 4096 3月  13 16:25 views/
mao-siyu@mao-siyu-PC:~/my-koa$
```
