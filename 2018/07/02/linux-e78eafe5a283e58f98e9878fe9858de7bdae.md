---
title: 'Linux 环境变量配置'
date: '2018-07-02T16:03:57+00:00'
status: publish
permalink: /2018/07/02/linux-%e7%8e%af%e5%a2%83%e5%8f%98%e9%87%8f%e9%85%8d%e7%bd%ae
author: 毛巳煜
excerpt: ''
type: post
id: 2186
category:
    - Linux服务器
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 环境变量 一句话总结：程序运行时所在的环境的全局变量

所有运行在操作系统中的程序，它们使用的全局变量，就是在操作系统中被叫做环境变量，这个环境变量是可以被所有程序识别共用

- - - - - -

###### 1 全局环境变量配置

```ruby
[root@dev1 ~]# vim /etc/profile

# java 环境变量
export JAVA_HOME=/mnt/SSD/java/jdk-8u172-linux-x64
export JRE_HOME=<span class="katex math inline">JAVA_HOME/jre
export CLASSPATH=.:</span>JAVA_HOME/lib:<span class="katex math inline">JRE_HOME/lib
export PATH=</span>PATH:<span class="katex math inline">JAVA_HOME/bin

# maven 环境变量
export MAVEN_HOME=/mnt/SSD/maven/apache-maven-3.5.3
export PATH=</span>PATH:<span class="katex math inline">MAVEN_HOME/bin

# Android 环境变量
export ANDROID_HOME=/mnt/1TB/Android/Sdk/android-sdk-linux
export PATH=</span>PATH:<span class="katex math inline">ANDROID_HOME/tools
export PATH=</span>PATH:<span class="katex math inline">ANDROID_HOME/tools/bin
export PATH=</span>PATH:<span class="katex math inline">ANDROID_HOME/platform-tools

# GO 环境变量
export GO_HOME=/mnt/SSD/go
export PATH=</span>PATH:$GO_HOME/bin

[root@dev1 ~]#
# 刷新环境变量
[root@dev1 ~]# source /etc/profile

```

- - - - - -

###### 2 只给当前用户，配置环境变量

```ruby
cat >>  ~/.bashrc 
```

`重新连接终端，测试是否配置成功`

- - - - - -