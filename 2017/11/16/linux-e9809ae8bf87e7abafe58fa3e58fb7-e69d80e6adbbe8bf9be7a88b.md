---
title: 'Linux 通过端口号 杀死进程'
date: '2017-11-16T13:51:43+00:00'
status: publish
permalink: /2017/11/16/linux-%e9%80%9a%e8%bf%87%e7%ab%af%e5%8f%a3%e5%8f%b7-%e6%9d%80%e6%ad%bb%e8%bf%9b%e7%a8%8b
author: 毛巳煜
excerpt: ''
type: post
id: 333
category:
    - Linux服务器
tag: []
post_format: []
---
### **应用方法**

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@localhost javaServer]# netstat -antp | grep 8080 | awk '{print <span class="katex math inline">7}' | awk -F '/' '{print</span>1}' | xargs kill -9

```
```

### **命令解析**

**根据端口号查找进程**

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@localhost javaServer]# netstat -antp | grep 8080
tcp6       0      0 :::8080                 :::*                    LISTEN      6193/java
[root@localhost javaServer]#

```
```

**根据端口号查找进程中第7组参数**

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@localhost javaServer]# netstat -antp | grep 8080 | awk '{print $7}'
6193/java
[root@localhost javaServer]#

```
```

**使用 awk -F '/' '{print $1}' 拆分 6193/java 来获取PID**

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@localhost javaServer]# netstat -antp | grep 8080 | awk '{print <span class="katex math inline">7}' | awk -F '/' '{print</span>1}'
6193
[root@localhost javaServer]#

```
```

**杀死获取到的PID进程**

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@localhost javaServer]# netstat -antp | grep 8080 | awk '{print <span class="katex math inline">7}' | awk -F '/' '{print</span>1}' | xargs kill -9
[root@localhost javaServer]#
[root@localhost javaServer]# netstat -antp | grep 8080
[1]+  已杀死               nohup java -jar dlfc-framework-bigdata-statistical-1.0-SNAPSHOT.jar
[root@localhost javaServer]#

```
```