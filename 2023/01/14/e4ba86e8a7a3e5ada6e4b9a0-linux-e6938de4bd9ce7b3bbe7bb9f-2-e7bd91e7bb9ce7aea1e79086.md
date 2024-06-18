---
title: '了解学习 Linux 操作系统-2. 网络管理'
date: '2023-01-14T07:47:24+00:00'
status: private
permalink: /2023/01/14/%e4%ba%86%e8%a7%a3%e5%ad%a6%e4%b9%a0-linux-%e6%93%8d%e4%bd%9c%e7%b3%bb%e7%bb%9f-2-%e7%bd%91%e7%bb%9c%e7%ae%a1%e7%90%86
author: 毛巳煜
excerpt: ''
type: post
id: 9685
category:
    - 自学整理
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
网络管理
----

### CentOS 7

- **常用命令**
  - `ip a`
  - `ping ip/域名`
  - `telnet ip:port`
  - `route add -net 192.168.0.0/24 gw 192.168.0.1`
  - `route del -net 192.168.0.0/24 gw 192.168.0.1`
- **常见的IP与端口**
  - `255.255.255.0` 子网掩码，用来划分网段的
  - `0.0.0.0/0` 表示所有网络，任意网段
  - `21 22 23 25 80 443 3306 3389 1521 6379 等`
- **常用DNS地址**
  - `114.114.114.114`
  - `223.5.5.5`
  - `223.6.6.6`
  - `1.2.4.8`
  - `8.8.8.8` Google的
  - `8.8.4.4` Google的
  - `202.106.0.20` 联通的
- 网关(通常就是你的路由)
- 防火墙
  
  
  - `iptables`
  - `firewalld`
- VPN服务器/客户端 
  - > 访问Google查点儿技术文章
  - 如果不使用VPN设备可能会这样实现 
      - [![](http://qiniu.dev-share.top/image/linux/VPN01.png)](http://qiniu.dev-share.top/image/linux/VPN01.png)
  - 当下最新的简单的理解工作原理 
      - [![](http://qiniu.dev-share.top/image/linux/VPN02.png)](http://qiniu.dev-share.top/image/linux/VPN02.png)