---
title: "Egg.js 为企业级框架和应用而生"
date: "2017-11-16"
categories: 
  - "node-js"
---

## 开发环境

操作系统：Linux ubuntu 16.04 开发工具：webstrom 运行环境：node v8.0.0

## 快速初始化

```ruby
$ sudo cnpm i egg-init -g
$ sudo egg-init egg-example --type=simple
$ cd egg-example
$ sudo cnpm i

#### 启动项目
$ sudo npm run dev
```

#### **遇到的问题:**

以上这种创建方式只有root才能开发操作, 这是因为 使用 egg-init 的时候使用的root权限, 会linux系统的都知道, 接下来就会有一堆的权限问题了, 所以项目创建完成后, 需要改变项目工程的访问权限.

#### **Linux ubuntu 16.04 设置root 密码, ubuntu系统默认是随机的root密码, 需要在每次开机时重新设置root密码**

```ruby
mao-siyu@mao-siyu-PC:~$ sudo passwd root
[sudo] mao-siyu 的密码：
输入新的 UNIX 密码：
重新输入新的 UNIX 密码：
passwd：已成功更新密码
mao-siyu@mao-siyu-PC:~$ su
密码：
root@mao-siyu-PC:/home/mao-siyu#
```

#### 接下来 修改项目的访问权限

```ruby
# 查看项目访问权限
root@mao-siyu-PC:/home/mao-siyu/文档/code# ll
总用量 3
drwxrwxr-x 16 mao-siyu mao-siyu 4096 7月  18 10:51 ./
drwxr-xr-x 12 mao-siyu mao-siyu 4096 7月  14 18:01 ../
drwxr-xr-x  9 root     root     4096 7月  18 10:53 egg-example/

# 开放文件夹权限
root@mao-siyu-PC:/home/mao-siyu/文档/code# chmod -R 777 egg-example/

# 更改项目所属用户
root@mao-siyu-PC:/home/mao-siyu/文档/code# chown  mao-siyu egg-example/
root@mao-siyu-PC:/home/mao-siyu/文档/code# ll
总用量 3
drwxrwxr-x 16 mao-siyu mao-siyu 4096 7月  18 10:51 ./
drwxr-xr-x 12 mao-siyu mao-siyu 4096 7月  14 18:01 ../
drwxrwxrwx  9 mao-siyu root     4096 7月  18 10:53 egg-example/

# 更改项目所属组
root@mao-siyu-PC:/home/mao-siyu/文档/code# chgrp  mao-siyu egg-example/
root@mao-siyu-PC:/home/mao-siyu/文档/code# ll
总用量 3
drwxrwxr-x 16 mao-siyu mao-siyu 4096 7月  18 10:51 ./
drwxr-xr-x 12 mao-siyu mao-siyu 4096 7月  14 18:01 ../
drwxrwxrwx  9 mao-siyu mao-siyu 4096 7月  18 10:53 egg-example/

```

# example

## 快速入门

如需进一步了解，参见 [egg 文档](https://eggjs.org)。

### 本地开发

```ruby
$ npm install
$ npm run dev
$ open http://localhost:7001/news
```

### 部署

线上正式环境用 `EGG_SERVER_ENV=prod` 来启动。

```ruby
$ EGG_SERVER_ENV=prod npm start
```

### 单元测试

- \[egg-bin\] 内置了 \[mocha\], \[thunk-mocha\], \[power-assert\], \[istanbul\] 等框架，让你可以专注于写单元测试，无需理会配套工具。
- 断言库非常推荐使用 \[power-assert\]。
- 具体参见 [egg 文档 -单元测试](https://eggjs.org/zh-cn/core/unittest)。

### 内置指令

- 使用 \`npm run lint\` 来做代码风格检查。
- 使用 \`npm test\` 来执行单元测试。
- 使用 \`npm run autod\` 来自动检测依赖更新，详细参见 [autod](https://www.npmjs.com/package/autod) 。
