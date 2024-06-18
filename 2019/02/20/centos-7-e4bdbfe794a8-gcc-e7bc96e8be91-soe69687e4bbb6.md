---
title: 'CentOS 7  使用 gcc 编辑 .so文件'
date: '2019-02-20T15:33:05+00:00'
status: publish
permalink: /2019/02/20/centos-7-%e4%bd%bf%e7%94%a8-gcc-%e7%bc%96%e8%be%91-so%e6%96%87%e4%bb%b6
author: 毛巳煜
excerpt: ''
type: post
id: 3455
category:
    - CentOS
tag: []
post_format: []
---
#### 环境准备

**linux版 jdk**  
**找到如下文件：**  
1\. jdk1.8.0\_201/include/jni.h  
2\. jdk1.8.0\_201/include/linux/jni\_md.h  
3\. jdk1.8.0\_201/include/linux/jawt\_md.h

##### 将 jdk中的文件 与 自己的 .c文件 与 .h文件 放到一起，执行如下命令进行编译

```ruby
[root@shared-server source-code]# ll
total 96
-rw-r--r-- 1 root root   995 Feb 20 23:11 jawt_md.h
-rw-r--r-- 1 root root 73701 Feb 20 23:11 jni.h
-rw-r--r-- 1 root root   824 Feb 20 23:11 jni_md.h
-rw-r--r-- 1 root root  4475 Feb 20 22:58 SerialPort.c
-rw-r--r-- 1 root root   774 Feb 20 22:55 SerialPort.h

```

##### 将 .c文件 编译成 .o文件 (32位)

`注： 需要32 gcc`

```ruby
[root@shared-server source-code]# gcc -m32 -c -fPIC -o SerialPort.o SerialPort.c

```

##### 将 .c文件 编译成 .o文件 (64位)

```ruby
[root@shared-server source-code]# gcc -c -fPIC -o SerialPort.o SerialPort.c

```

##### 将 .o文件 编译成 .so文件

```ruby
[root@shared-server source-code]# gcc -shared -o libserial_port.so SerialPort.o

```