---
title: "nw整合socket.io"
date: "2017-11-16"
categories: 
  - "窗体应用程序开发"
---

## Mysql逆向工程整合

#### 运行环境

```
node_WebKit
node.js
socket.io模块
mysql模块
```

#### 业务需求

```
使用nw实现桌面应用程序
node做服务器
使用socket.io做数据交互
通过访问指定的数据库中的所有表 生成对应的java项目 包括 entity mapper mapping 等等。。。
要生成的文件可以自定义扩展，也可以指定相要生成的 文件类型 比如 只要 entity
```

#### login.html

```markup
<!DOCTYPE html>
<html lang="zh-cmn-Hans">
<head>
    <meta charset="UTF-8">
    <title>小蜜蜂数据库逆向生成工具-登入页面</title>
</head>
<body class="scroll-all">
<div class="db-body">
    <div class="login-box">
        <div class="login-banner"></div>
        <div class="login-honeycomb"></div>
        <div class="db-cl"></div>
    </div>
    <div class="db-content-progress-box">
        <div class="db-content-progress">
            <span class="db-progress"></span>
        </div>
    </div>
    <div class="commons-wrap">
        <div class="logo-box">
            <div class="db-shaozi db-fl"></div>
            <div class="db-guanzi db-fl"></div>
            <span class="db-cl"></span>
        </div>
    </div>
    <div class="db-article">
        <div class="db-title"></div>
        <div class="db-context-box db-font">
            <form>
                <ul>
                    <li>
                        测试连接:
                        <div id="testInfo"></div>
                    </li>
                    <li><input class="db-font" type="text" id="host" value="111.67.192.10" placeholder="输入数据库IP地址"></li>
                    <li><input class="db-font" type="text" id="port" value="30005" placeholder="请输入端口号"></li>
                    <li><input class="db-font" type="text" id="database" value="sign" placeholder="请输入端库名"></li>
                    <li><input class="db-font" type="text" id="user" value="mao_siyu" placeholder="数据库用户名"></li>
                    <li><input class="db-font" type="text" id="password" value="yan8636396" placeholder="数据库密码"></li>

                    <li><input class="db-font" type="button" id="test" value="测试连接"></li>
                    <li><input class="db-font" type="reset" value="重置"></li>
                </ul>
            </form>
        </div>
    </div>
</div>
<!-- 这个js是引用了 node服务器中存在的js文件 -->
<script src="./LK_DBGenerateMyBatis/node_modules/socket.io-client/dist/socket.io.js"></script>
<script>
    // 切记 一定要加上 http:// 请求协议否则在浏览器中可以访问，在nw中就访问不到
    var socket = io.connect('http://127.0.0.1:10086');
    var test = document.getElementById('test');
    var testInfo = document.getElementById('testInfo');
    // 当点击测试连接按钮时，将输入的信息传给mysql模块进行连接测试
    test.onclick = function () {
        var settings = {
            host: document.getElementById('host').value,
            port: document.getElementById('port').value,
            user: document.getElementById('user').value,
            database: document.getElementById('database').value,
            password: document.getElementById('password').value
        }
        // 调用socket中已经绑定的事件，这个事件在mysql模块中已经绑定;
        socket.emit('testConnection', settings);
    }

    // 监听socket是否连接成功
    socket.on('connect', function () {
        console.log('connect');
    });

    // 接收mysql回调的连接信息
    socket.on('mysqlInfo', function (data) {
        testInfo.innerHTML = data;
    });
</script>
</body>
</html>
```

#### nw.js的 package.json

```javascript
{
  /* 必填项 main (string) : node-webkit启动的时候默认打开的页面 */
  "main": "./login.html",
  /* 必填项 nam(string):package文件的名称，唯一值，不允许有空格，允许'.'或者'-','_'字符 */
  "name": "nw-demo",
  "description": "demo app of node-webkit",
  /* nodejs(boolean): 设置是否在webkit内核中启动nodejs,false的时候会禁用掉nodejs */
  "nodejs": true,
  /* node-main(string):指定项目启动的时候，启用node.js文件的地址 */
  "node-main": "./LK_DBGenerateMyBatis/bin/www",
  "version": "0.1.0",
  "keywords": [
    "demo",
    "node-webkit"
  ],
  /* window(object): 控制主窗口的显示风格 */
  "window": {
    /* show(boolean):默认为true,当为false的时候，窗口会隐藏在任务栏 */
    "show": true,
    /* kiosk(boolean): 是否使用kiosk模式，（对于kiosk模式，是全屏显示，且阻止用户关闭应用（确保一种方式去离开kiosk模式）。这个模式用于保护在正常途径关闭应用。） */
    "kiosk": false,
    /* title(string):窗口的标题 */
    "title": "node-webkit demo",
    /* frame(boolean):是否显示窗口的最外层的框架 */
    "frame": true,
    /* toolbar(boolean): 是否显示导航工具栏 */
    "toolbar": true,
    /* positon(string): (null/center/mouse) 窗口的显示位置 */
    "position": "center",
    /* resizeable(boolean): 设置窗口是否可调整大小 */
    "resizeable": true,
    /* fullscreen(boolean):是否全屏显示 */
    "fullscreen": false,
    /* always-on-top(boolean):是否设置窗口一直在最前端 */
    "always-on-top": true,
    /* show_in_taskbar(boolean):默认为true: 是否显示任务栏 */
    "show_in_taskbar": true,
    "width": 1100,
    "height": 1024,
    "min_width": 1100,
    "min_height": 0,
    "max_width": 1100,
    "max_height": 0
  },
  /* webkit(object): 控制 webkit的特性的开/关 */
  "webkit": {
    "plugin": true
    /* plugin(boolean):默认为false 是否允许加载额外的浏览器插件：flase等
       java(boolean):默认为false,是否允许加载 java应用。
       page-cache(boolean):默认为false,是否允许页面缓存。
       user-agent(string):重写http 请求的 User-Agent头
       1.%name: 替换name字段（配置文件里面配置的）
       2.%ver:替换version字段（配置文件里面配置的）
       3.%nwver:替换node-webkit的版本号
       4.%webkit_ver:替换webkit引擎的版本号
       5.%osinfo:替换在user agent 中的OS和CPU信息。
       node-remote(string): 启动远程调用节点页面。
       chrominum-args(string): 设置 chromium参数。
       js-flags(string): 给js引擎传递特殊指令
       inject-js-start/inject-js-end: js文件注入
       snapshot(string):指定路径快照。
       dom_storage_quota(int):dom存储。
       no_edit_menu(boolean): 只作用于MAC ,默认为false, 是否不显示 编辑菜单。
       其他属性：
       description(string):描述。
       version(string): 版本号
       keywords(array/string):关键字
       maintainers(array):
     */
  }
}

```

#### 关键模块 长连接 socketIO.js

```javascript
/**
 * Created by mao_siyu on 2016/11/30.
 * socket.io服务
 */
var EventEmitter = require('events').EventEmitter;
var emitter = new EventEmitter();
// 创建http服务器并监听 10086 端口
var http = require('http');
var server = http.createServer().listen(10086);
// 长连接监听http服务器(如果有向服务器发送的长连接事件请求，将会被捕获)
var sio = require('socket.io');
var sc = sio.listen(server);
// 绑定一个事件 每次调用的时候进行连接,这样做是为了保证每次的调用都不会受到异步的影响而获取不到已经连接的socket
emitter.on('getSocket', function (callback) {
    sc.on('connection', function (socket) {
        console.log('客户端已经连接');
        callback(socket);
        // 监听是否断开事件
        socket.on('disconnect', function () {
            console.log('客户端断开连接');
        });
    });
});
//
var socket = function (callback) {
    emitter.emit('getSocket', callback);
};
module.exports = socket;
```

#### mysql.js 模块

```javascript
/* =-=-=-=-=-=-=-=-=-= 此文件是链接 mysql 的配置文件 =-=-=-=-=-=-=-=-=-=-= */
var EventEmitter = require('events').EventEmitter;
var socket = require('../public/config/socketIO');
var emitter = new EventEmitter();
var mysql = require('mysql');
var pool;

/**
 * 测试数据库链接
 */
socket(function (sc) {
    /**
     * testConnection 给页面调用的测试事件
     *
     * 通过页面传入的配置项
     *   settings = {
     *       host: document.getElementById('host').value,
     *       port: document.getElementById('port').value,
     *       user: document.getElementById('user').value,
     *       database: document.getElementById('database').value,
     *       password: document.getElementById('password').value
     *   }
     */
    sc.on('testConnection', function (settings) {

        /**
         * 配置连接池
         */
        var testPool = mysql.createPool(settings);
        // 链接数据库
        testPool.getConnection(function (err, connection) {
            if (err) {
                sc.emit('mysqlInfo', 'mysql 数据库链接 FAIL!' + err);
                return;
            }
            // 测试连接
            sc.emit('mysqlInfo', 'mysql 数据库链接 SUCCESS!');
            connection.release();
        });
    });

    /**
     * 登录数据库
     * testConnection 给页面调用的登录事件
     */
    sc.on('connection', function (settings) {
        /**
         * 配置连接池
         */
        pool = mysql.createPool(settings);
    });
});


/**
 * 注册连接池事件
 */
emitter.on('connection', function (sql, callback) {
    pool.getConnection(function (err, connection) {
        connection.query(sql, function (err, rows) {
            // 还是得释放链接
            connection.release();
            callback(err, rows);
        });
    });
});

var query = function (sql, callback) {
    emitter.emit('connection', sql, callback);
};

module.exports = query;
```

#### app.js

```javascript
// 在www文件或者app.js文件中 需要初始化mysql模块, 因为项目中主要是为了配置mysql，所以把它放在了第一位，
// 在加载mysql模块时也同时加载了 socket.io模块，这些都是必备的。
// 引入 mysql 模块
require('./db_connection/mysql');
```

接下来就可以启动 nw了， 通过nw渲染的界面来加载socket.io模块与node服务器进行交互
