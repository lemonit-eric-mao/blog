---
title: 'CentOS 7 使用 npm 失败 npm: symbol SSL_set_cert_cb'
date: '2017-11-16T12:38:57+00:00'
status: publish
permalink: /2017/11/16/centos-7-%e4%bd%bf%e7%94%a8-npm-%e5%a4%b1%e8%b4%a5-npm-symbol-ssl_set_cert_cb
author: 毛巳煜
excerpt: ''
type: post
id: 187
category:
    - CentOS
tag: []
post_format: []
---
### **异常信息**

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@localhost client]# npm install -g cnpm --registry=https://registry.npm.taobao.org
npm: relocation error: npm: symbol SSL_set_cert_cb, version libssl.so.10 not defined in file libssl.so.10 with link time reference
[root@localhost client]#

```
```

### **安装yum工具包**

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@localhost ~]# yum -y install yum-utils
[root@localhost ~]#

```
```

### **启用**

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@localhost ~]# yum-config-manager --enable cr && yum update
[root@localhost ~]#

```
```

[原文链接](https://bugzilla.redhat.com/show_bug.cgi?id=1481470)