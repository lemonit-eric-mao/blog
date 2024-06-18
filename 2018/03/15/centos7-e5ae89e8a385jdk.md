---
title: 'Centos7 安装JDK'
date: '2018-03-15T15:38:42+00:00'
status: publish
permalink: /2018/03/15/centos7-%e5%ae%89%e8%a3%85jdk
author: 毛巳煜
excerpt: ''
type: post
id: 2003
category:
    - CentOS
    - Java
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
###### 下载

```ruby
mkdir -p /home/deploy/java/
wget -P /home/deploy/java/ http://qiniu.dev-share.top/jdk-8u261-linux-x64.tar.gz
#wget -P /home/deploy/java/ http://qiniu.dev-share.top/jdk-11.0.12_linux-x64_bin.tar.gz
#wget -P /home/deploy/java/ http://qiniu.dev-share.top/jdk-17_linux-x64_bin.tar.gz

cd /home/deploy/java/
tar -zxvf jdk-8u261-linux-x64.tar.gz
cd jdk1.8.0_261/

```

- - - - - -

###### **`全局`** 用户添加 java 环境变量

```ruby
cat >> /etc/profile 
```

- - - - - -

###### **`当前`** 用户添加 java 环境变量

```ruby
cat >> ~/.bashrc 
```

- - - - - -