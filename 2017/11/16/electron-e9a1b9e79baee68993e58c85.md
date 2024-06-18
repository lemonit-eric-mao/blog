---
title: 'Electron 项目打包'
date: '2017-11-16T12:47:37+00:00'
status: publish
permalink: /2017/11/16/electron-%e9%a1%b9%e7%9b%ae%e6%89%93%e5%8c%85
author: 毛巳煜
excerpt: ''
type: post
id: 211
category:
    - Electron
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
当一个electron应用程序开发完成以后, 包装成正式使用的产品, 总不能给人家用源码 启动吧

**一** 使用 electron-packager 将项目打包  
**二** 使用 asar 为源码添加保护

开发环境: ubuntu 16  
开发工具: webstorm  
ECMAScript: 6

###### 安装插件 (全局比较省事)

```ruby
npm install -g electron

npm install -g electron-prebuilt

npm install -g electron-packager

npm install -g asar

```

###### **electron-packager 用法**

```
  命令解释
  electron-packager     

```

```ruby
// 在项目根目录 打开终端 执行以下命令
electron-packager ./ myApp -all --out ../outputPackage --electron-version=1.4.13 --overwrite --icon=./favicon.ico

```

如果每次打包都要写这么长一串代码那也太麻烦了, 因此将命令保存在 package.json 中只要执行 **npm run package** 这样就方便多了

###### package.json

```json
..........
  "scripts": {
    "start": "electron .",
    "debug": "electron --debug=5858 .",
    "sandbox": "electron . --enable-sandbox",
    "package": "electron-packager ./ myApp -all --out ../outputPackage --electron-version=1.4.13 --overwrite --icon=./favicon.ico"
  },
..........

```

###### **asar用法**

```
  命令解释:  这个命令会把指定目录下的所有文件都给打包成 .asar文件；这个文件使用 electron 可以直接运行.
  asar pack  

```

```ruby
// 在源码项目目录 打开终端 执行以下命令
"asar": "asar pack ../outputPackage/myApp-linux-x64/resources/app ../outputPackage/myApp-linux-x64/resources/app.asar"

```

###### package.json

```json
..........
  "scripts": {
    "start": "electron .",
    "debug": "electron --debug=5858 .",
    "sandbox": "electron . --enable-sandbox",
    "package": "electron-packager ./ myApp -all --out ../outputPackage --electron-version=1.4.13 --overwrite --icon=./favicon.ico",
    "asar": "asar pack ../outputPackage/myApp-linux-x64/resources/app ../outputPackage/myApp-linux-x64/resources/app.asar"
  },
..........

```

继上一条命令后 执行 npm run asar 命令  
这条命令执行完成后, 会把上面的打包后的源码转成 app.asar 文件,然后在删除源文件测试, 项目会执行这个 app.asar文件

###### 完整的 package.json

```json
{
  "name": "data-acquisition-new",
  "version": "1.0.0",
  "description": "",
  "main": "main.js",
  "scripts": {
    "start": "electron .",
    "debug": "electron --debug=5858 .",
    "sandbox": "electron . --enable-sandbox",
    "package": "electron-packager ./ myApp -all --out ../outputPackage --electron-version=1.4.13 --overwrite --icon=./favicon.ico",
    "asar": "asar pack ../outputPackage/myApp-linux-x64/resources/app ../outputPackage/myApp-linux-x64/resources/app.asar"
  },
  "author": "",
  "license": "ISC",
  "dependencies": {
    "electron-prebuilt": "^1.4.13",
    "moment": "^2.18.1",
    "mysql": "^2.13.0"
  }
}

```

###### 注意两条命令填写的目录, 一定要写对路径.