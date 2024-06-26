---
title: "Node.js 内存益处 检测方法,  查看内存快照"
date: "2017-11-16"
categories: 
  - "node-js"
---

**开发环境: ubuntu 16 开发工具: webstorm 2017 Node.js : 8.0.0 ECMAScript : 2015 2016**

### \==========分析 Node.js 中的内存泄漏=========

PS：安装 heapdump 在某些 Node.js 版本上可能出错，建议使用 npm install heapdump -target=Node.js版本来安装。 例如:

```ruby
$ node -v
v8.0.0
```

执行的命令是:

```ruby
$ npm install heapdump -target=v8.0.0
```

首先使用 `node --expose-gc index.js` 运行代码，将会得到两个内存快照，之后打开 chrome的devtool，点击 profile，载入内存快照。 打开对比，Delta 会显示对象的变化情况，如果对象 Delta 一直增长，就很有可能是内存泄漏了。 执行的命令是:

```ruby
node --expose-gc index.js
```

### **index.js**

```javascript
const {EventEmitter} = require('events');
const heapdump = require('heapdump');

global.test = new EventEmitter();
heapdump.writeSnapshot('./' + Date.now() + '.heapsnapshot');

function run3() {
    const innerData = new Buffer(100);
    const outClosure3 = function () {
        void innerData;
    };
    test.on('error', () => {
        console.log('error');
    });
    outClosure3();
}

for (let i = 0; i < 10; i++) {
    run3();
}
gc();

heapdump.writeSnapshot('./' + Date.now() + '.heapsnapshot');
```

### **package.json**

```json
{
  "name": "analyzingmemoryleaksinnode",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "start": "node --expose-gc index.js"
  },
  "author": "",
  "license": "ISC",
  "dependencies": {
    "heapdump": "^0.3.9"
  }
}
```

### **package-lock.json** 自动生成
