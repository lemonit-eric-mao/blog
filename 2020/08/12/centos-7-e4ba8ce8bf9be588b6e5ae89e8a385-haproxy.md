---
title: 'CentOS 7 二进制安装 HAProxy'
date: '2020-08-12T02:40:36+00:00'
status: publish
permalink: /2020/08/12/centos-7-%e4%ba%8c%e8%bf%9b%e5%88%b6%e5%ae%89%e8%a3%85-haproxy
author: 毛巳煜
excerpt: ''
type: post
id: 5719
category:
    - HAProxy
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### 禁用 **`SELinux`**

```ruby
setenforce 0
sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config


```

###### 如果不禁用 **`SELinux`** ，程序启动时会抛出 `Starting proxy stats: cannot bind socket [0.0.0.0:1080]` 也可以执行如下命令来解决

```ruby
setsebool -P haproxy_connect_any=1

```

- - - - - -

###### 添加 yum 源

```ruby
cat > /etc/yum.repos.d/ius-7.repo 
```

- - - - - -

###### 查看

```ruby
# 更新源
yum makecache fast

# 查看
[root@k8s-master ~]# yum list | grep haproxy
haproxy.x86_64                            1.5.18-9.el7                   base
haproxy16u.x86_64                         1.6.15-1.el7.ius               ius
haproxy17u.x86_64                         1.7.12-1.el7.ius               ius
haproxy18u.x86_64                         1.8.25-1.el7.ius               ius
haproxy20.x86_64                          2.0.16-1.el7.ius               ius
haproxy22.x86_64                          2.2.1-1.el7.ius                ius
pcp-pmda-haproxy.x86_64                   4.3.2-7.el7_8                  updates
[root@k8s-master ~]#

```

- - - - - -

###### 安装

```ruby
[root@k8s-master ~]# yum install -y haproxy22

[root@k8s-master ~]# haproxy -v
HA-Proxy version 2.2.1 2020/07/23 - https://haproxy.org/
Status: long-term supported branch - will stop receiving fixes around Q2 2025.
Known bugs: http://www.haproxy.org/bugs/bugs-2.2.1.html
Running on: Linux 5.8.0-1.el7.elrepo.x86_64 #1 SMP Sun Aug 2 18:18:16 EDT 2020 x86_64
[root@k8s-master deploy]#

```

- - - - - -

###### 配置日志

```ruby
cat > /etc/rsyslog.d/haproxy.conf 
```

- - - - - -

###### 添加配置文件， 使用 k8s master 高可用配置来举例

```ruby
# 备份默认配置文件
mv /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg-bak

# 创建文件
cat > /etc/haproxy/haproxy.cfg 
```

- - - - - -

###### 启动

```ruby
systemctl start haproxy && systemctl enable haproxy && systemctl status haproxy

```

- - - - - -

- - - - - -

- - - - - -