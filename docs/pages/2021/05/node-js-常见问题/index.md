---
title: "Node.Js 常见问题"
date: "2021-05-31"
categories: 
  - "node-js"
---

###### package.json 中的 main属性作用是什么？

**作用：`定位入口点`** 1. 首先，Node 查找package.json文件并检查它是否包含main属性。 2. 它将用于指向包目录中的一个文件，该文件将成为入口点。 3. 如果 main 属性不存在，则 Node 依次尝试index.js,index.json和index.node。

* * *

* * *

* * *

###### 无法加载文件xxx.ps1，因为在此系统上禁止运行脚本

```ruby
## 查看
E:\gitee-project\koa2-server> get-ExecutionPolicy
Restricted

## 修改
E:\gitee-project\koa2-server> Set-ExecutionPolicy -Scope CurrentUser
## 输入 RemoteSigned
ExecutionPolicy: RemoteSigned

## 再次查看
E:\gitee-project\koa2-server> get-ExecutionPolicy
RemoteSigned

```

* * *

* * *

* * *

###### 设置全局默认路径

```ruby
## 先创建文件夹
mkdir 'D:/Program Files/nodejs/npm_global' 'D:/Program Files/nodejs/npm_cache'

npm config set prefix "D:/Program Files/nodejs/npm_global"
npm config set cache "D:/Program Files/nodejs/npm_cache"


npm config ls
......
cache = "D:\\Program Files\\nodejs\\npm_cache"
prefix = "D:\\Program Files\\nodejs\\npm_global"
registry = "https://registry.npm.taobao.org/"
......

```

* * *

* * *

* * *

###### npm 设置私服

```ruby
## 设置淘宝源
[root@master01 ~]# npm config set registry https://registry.npm.taobao.org

[root@master01 ~]# npm config get registry
https://registry.npm.taobao.org


## 设置本地私服源
[root@master01 ~]# npm config set registry http://172.16.15.205:8081/repository/npm-public/

[root@master01 ~]# npm config get registry
http://172.16.15.205:8081/repository/npm-public/

```

* * *

* * *

* * *

###### yarn 设置私服

```ruby
[root@master01 ~]# yarn config set registry https://registry.npm.taobao.org

[root@master01 ~]# yarn config get registry
https://registry.npm.taobao.org

[root@master01 ~]# yarn config set registry http://172.16.15.205:8081/repository/npm-public/
yarn config v1.22.10

success Set "registry" to "http://172.16.15.205:8081/repository/npm-public/".
Done in 0.06s.
[gitlab-runner@Gitlab-Runner dist-server]$

```

* * *

###### .yarnrc

在项目根目录中添加 **`.yarnrc`** 文件

```ruby
cat > .yarnrc << ERIC
# 指定 nexus私服地址
registry "http://172.16.15.205:8081/repository/npm-public/"

ERIC

```

* * *

* * *

* * *

###### 踩坑 npm 或 yarn 安装依赖异常

**`self signed certificate in certificate chain`**

```ruby
## 关闭npm strict-ssl验证
npm config set strict-ssl false

## 关闭yarn strict-ssl验证
yarn config set strict-ssl false
```

* * *

* * *

* * *
