---
title: Node.js-安装
date: '2017-11-16T11:14:45+00:00'
status: publish
permalink: /2017/11/16/node-js-%e5%ae%89%e8%a3%85
author: 毛巳煜
excerpt: ''
type: post
id: 117
category:
    - node.js
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
> - **[CentOS 7 安装教程](https://github.com/nodesource/distributions/blob/master/README.md#installation-instructions-1 "CentOS 7 安装教程")**
> - **[Ubuntu 安装教程](https://github.com/nodesource/distributions/blob/master/README.md#installation-instructions "Ubuntu 安装教程")**
> - **[官网](https://nodejs.org/en/download/ "官网")**
> - **[官方中文网](http://nodejs.cn/download/ "官方中文网")**

- - - - - -

- - - - - -

- - - - - -

CentOS 7 安装 Node.js
-------------------

### 安装源

```ruby
[root@master ~]# curl -sL https://rpm.nodesource.com/setup_16.x | bash -

## Installing the NodeSource Node.js 16.x repo...
## Inspecting system...
.........省略
## Run `sudo yum install -y nodejs` to install Node.js 16.x and npm.
## You may run dnf if yum is not available:
     sudo dnf install -y nodejs
## You may also need development tools to build native addons:
     sudo yum install gcc-c++ make
## To install the Yarn package manager, run:
     curl -sL https://dl.yarnpkg.com/rpm/yarn.repo | sudo tee /etc/yum.repos.d/yarn.repo
     sudo yum install yarn


```

### 安装 Node.js

```ruby
sudo yum install -y nodejs

```

```ruby
[root@master ~]# node -v
v14.5.0
[root@master ~]#
[root@master ~]#
[root@master ~]# npm -v
6.14.5
[root@master ~]#

```

### 安装 Yarn

```ruby
curl -sL https://dl.yarnpkg.com/rpm/yarn.repo | sudo tee /etc/yum.repos.d/yarn.repo
     sudo yum install yarn

```

> - **[Yarn官网](https://yarnpkg.com/zh-Hans/docs/install "Yarn官网")**
> - **[设置私服地址](http://www.dev-share.top/2021/05/31/node-js-%e5%b8%b8%e8%a7%81%e9%97%ae%e9%a2%98/ "设置私服地址")**

**yarn 常用命令**

```ruby
# 升级指定依赖包
yarn upgrade element-ui@2.14.1

# 添加依赖
yarn add vue-quill-editor -S

```

- - - - - -

- - - - - -

- - - - - -

### Ubuntu 安装方法

```ruby
## 安装
sudo apt update
sudo apt install -y curl
sudo curl -sL https://deb.nodesource.com/setup_16.x | sudo -E bash  -
sudo apt-get install -y nodejs


## 卸载
sudo apt remove nodejs
sudo apt purge nodejs
sudo apt autoremove


```