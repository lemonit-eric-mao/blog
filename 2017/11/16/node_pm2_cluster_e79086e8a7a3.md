---
title: Node_PM2_Cluster_理解
date: '2017-11-16T12:18:05+00:00'
status: publish
permalink: /2017/11/16/node_pm2_cluster_%e7%90%86%e8%a7%a3
author: 毛巳煜
excerpt: ''
type: post
id: 145
category:
    - node.js
tag: []
post_format: []
hestia_layout_select:
    - default
---
```javascript
// Node.js集群
var cluster = require('cluster');
//
var numCPUs = require('os').cpus().length;

var http = require('http');
http.createServer(function (req, res) {
    res.writeHead(200);
    res.end("hello world");
}).listen(8080);

```

```javascript
/**
 *  安装 pm2 模块; 因为nodeJs是单进程的，所以只能支持单核cpu。如果想充分利用多核cpu 那么需要借助 pm2模块来解决这个问题
 *  npm install pm2 -g 等待安装完成
 *  测试是否安装完成,直接在控制台输入 pm2 如果出现相关 pm2的信息,正明安装OK
 *  用法
 *  pm2 start Node_Cluster_理解.js -i max
 *  命令如下
 *   <span class="katex math inline">npm install pm2 -g                 // 命令行安装 pm2
 *</span> pm2 start app.js -i 4              // 后台运行pm2，启动4个app.js
 *                                        // 也可以把'max' 参数传递给 start
 *                                        // 正确的进程数目依赖于Cpu的核心数目
 *   <span class="katex math inline">pm2 start app.js --name my-api     // 命名进程
 *</span> pm2 list                           // 显示所有进程状态
 *   <span class="katex math inline">pm2 monit                          // 监视所有进程
 *</span> pm2 logs                           // 显示所有进程日志
 *   <span class="katex math inline">pm2 stop all                       // 停止所有进程
 *</span> pm2 restart all                    // 重启所有进程
 *   <span class="katex math inline">pm2 reload all                     // 0秒停机重载进程 (用于 NETWORKED 进程)
 *</span> pm2 stop 0                         // 停止指定的进程
 *   <span class="katex math inline">pm2 restart 0                      // 重启指定的进程
 *</span> pm2 startup                        // 产生 init 脚本 保持进程活着
 *   <span class="katex math inline">pm2 web                            // 运行健壮的 computer API endpoint (http://localhost:9615)
 *</span> pm2 delete 0                       // 杀死指定的进程
 *   <span class="katex math inline">pm2 delete all                     // 杀死全部进程
 *
 *   运行进程的不同方式：
 *</span> pm2 start app.js -i max                            // 根据有效CPU数目启动最大进程数目
 *   <span class="katex math inline">pm2 start app.js -i 3                              // 启动3个进程
 *</span> pm2 start app.js -x                                // 用fork模式启动 app.js 而不是使用 cluster
 *   <span class="katex math inline">pm2 start app.js -x -- -a 23                       // 用fork模式启动 app.js 并且传递参数 (-a 23)
 *</span> pm2 start app.js --name serverone                  // 启动一个进程并把它命名为 serverone
 *   <span class="katex math inline">pm2 stop serverone                                 // 停止 serverone 进程
 *</span> pm2 start app.json                                 // 启动进程, 在 app.json里设置选项
 *   <span class="katex math inline">pm2 start app.js -i max -- -a 23                   // 在--之后给 app.js 传递参数
 *</span> pm2 start app.js -i max -e err.log -o out.log      // 启动 并 生成一个配置文件
 *   你也可以执行用其他语言编写的app  ( fork 模式):
 *   <span class="katex math inline">pm2 start my-bash-script.sh    -x --interpreter bash
 *</span> pm2 start my-python-script.py -x --interpreter python
 *
 *   0秒停机重载:
 *   这项功能允许你重新载入代码而不用失去请求连接。
 *   注意：
 *   仅能用于web应用
 *   运行于Node 0.11.x版本
 *   运行于 cluster 模式（默认模式）
 *   $ pm2 reload all
 */

```

```ruby
# 使用apache 的 ab 进行并发测试
$ ab -n 2000 -c 1000 localhost:8080/
# -n 代表每次并发量，-c 代表总共发送的数量

```