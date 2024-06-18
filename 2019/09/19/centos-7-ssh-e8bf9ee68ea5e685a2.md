---
title: 'Centos 7 SSH 连接慢'
date: '2019-09-19T07:57:08+00:00'
status: publish
permalink: /2019/09/19/centos-7-ssh-%e8%bf%9e%e6%8e%a5%e6%85%a2
author: 毛巳煜
excerpt: ''
type: post
id: 5045
category:
    - CentOS
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
##### 修改 UseDNS

```ruby
[cloud@cloudserver ~]$ sudo su -
输入密码

[root@test1 ~]# vim /etc/ssh/sshd_config
......
#UseDNS yes
UseDNS no
......
[root@test1 ~]#
[root@test1 ~]# systemctl restart sshd
[root@test1 ~]#

```

或者

```ruby
[root@test1 ~]# sed -i 's/\#UseDNS yes/UseDNS no/g' /etc/ssh/sshd_config && systemctl restart sshd

```

- - - - - -

##### ansible 批量修改 UseDNS

```ruby
[root@test1 tidb]# ansible -i hosts.ini all -m shell -a "sed -i 's/\#UseDNS yes/UseDNS no/g' /etc/ssh/sshd_config" -b

[root@test1 tidb]# ansible -i hosts.ini all -m shell -a "systemctl restart sshd" -b


```

- - - - - -

- - - - - -

- - - - - -

##### 允许 SSH 使用 root账户远程登录

```ruby
# 先从内部进入root帐户下操作
su -

# 允许root用户远程登录
sed -i s/'PermitRootLogin no'/'PermitRootLogin yes'/g /etc/ssh/sshd_config

systemctl restart sshd

```

- - - - - -

- - - - - -

- - - - - -

##### SSH 超时 解决方法

```ruby
sed -i 's/\#ClientAliveInterval 0/ClientAliveInterval 120/g' /etc/ssh/sshd_config && systemctl restart sshd


```

- - - - - -

- - - - - -

- - - - - -