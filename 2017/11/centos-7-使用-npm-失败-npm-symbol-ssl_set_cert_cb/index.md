---
title: "CentOS 7 使用 npm 失败 npm: symbol SSL_set_cert_cb"
date: "2017-11-16"
categories: 
  - "centos"
---

### **异常信息**

```ruby
[root@localhost client]# npm install -g cnpm --registry=https://registry.npm.taobao.org
npm: relocation error: npm: symbol SSL_set_cert_cb, version libssl.so.10 not defined in file libssl.so.10 with link time reference
[root@localhost client]#
```

### **安装yum工具包**

```ruby
[root@localhost ~]# yum -y install yum-utils
[root@localhost ~]#
```

### **启用**

```ruby
[root@localhost ~]# yum-config-manager --enable cr &amp;&amp; yum update
[root@localhost ~]#
```

[原文链接](https://bugzilla.redhat.com/show_bug.cgi?id=1481470)
