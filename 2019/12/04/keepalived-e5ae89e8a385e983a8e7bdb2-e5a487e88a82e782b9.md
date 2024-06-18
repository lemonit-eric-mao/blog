---
title: 'KeepAlived 安装部署-备节点'
date: '2019-12-04T06:00:18+00:00'
status: publish
permalink: /2019/12/04/keepalived-%e5%ae%89%e8%a3%85%e9%83%a8%e7%bd%b2-%e5%a4%87%e8%8a%82%e7%82%b9
author: 毛巳煜
excerpt: ''
type: post
id: 5178
category:
    - KeepAlived
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### [主节点安装](http://www.dev-share.top/2019/12/03/keepalived-%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2-%E4%B8%BB%E8%8A%82%E7%82%B9/ "主节点安装")

##### 环境

```ruby
[root@test2 ~]# keepalived -v
Keepalived v1.3.5 (03/19,2017)

```

<table><thead><tr><th>HostName</th><th>IP</th><th>DES</th></tr></thead><tbody><tr><td>test1</td><td>172.160.180.46</td><td>master</td></tr><tr><td>test2</td><td>172.160.180.47</td><td>node-1</td></tr><tr><td>test3</td><td>172.160.180.48</td><td>node-2</td></tr><tr><td>test4</td><td>172.160.181.18</td><td>node-3</td></tr></tbody></table>

###### 一、安装部署

```ruby
[root@test2 ~]# yum install -y keepalived

```

###### 二、配置文件

###### 查看当前要指定虚IP的网卡

```ruby
[root@test2 ~]# ip add show ens160
2: ens160: <broadcast> mtu 1500 qdisc mq state UP group default qlen 1000
    inet 172.160.180.47/24 brd 172.160.180.255 scope global noprefixroute ens160
[root@test2 ~]#
</broadcast>
```

```ruby
cat > /etc/keepalived/keepalived.conf 
```

###### 三、启动

```ruby
[root@test2 ~]# systemctl start keepalived.service && systemctl enable keepalived.service && systemctl status keepalived.service

```

###### 四、查看是否创建成功

**备节点与主节点不同，需要停掉主节点，备节点才可以查到虚拟IP；**  
**由此可见**，`KeepAlived 高可用是通过动态切换生成虚拟IP地址来达到的高可用！`

```ruby
[root@test2 ~]# ip addr show ens160
2: ens160: <broadcast> mtu 1500 qdisc mq state UP group default qlen 1000
    inet 172.160.180.47/24 brd 172.160.180.255 scope global noprefixroute ens160
    # 发现多了一个虚拟IP就是成功了
    inet 172.160.180.168/24 scope global secondary ens160
[root@test2 ~]#

</broadcast>
```