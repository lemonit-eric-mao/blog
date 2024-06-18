---
title: '什么是 TCP/IP'
date: '2017-11-16T14:52:54+00:00'
status: publish
permalink: /2017/11/16/%e4%bb%80%e4%b9%88%e6%98%af-tcpip
author: 毛巳煜
excerpt: ''
type: post
id: 422
category:
    - 网络基础
tag: []
post_format: []
---
什么是 TCP/IP
----------

**TCP/IP 是互联网相关的各类协议族的总称**

TCP/IP 协议族里重要的一点就是分层。TCP/IP 协议族按层次分别分  
为以下 4 层:应用层、传输层、网络层和数据链路层。

### **应用层** HTTP

TCP/IP 协议族内预存了各类通用的应用服务比如:  
`FTP` (File Transfer Protocol,文件传输协议)  
`DNS` (Domain Name System,域名系统)  
**FTP DNS 服务就是其中两类。**  
`HTTP` 协议也处于该层。

### **传输层** TCP

在传输层有两个性质不同的协议:  
\* TCP(Transmission Control Protocol,传输控制协议)  
\* UDP(User Data Protocol,用户数据报协议)。

### **网络层** IP

**(又名网络互连层)**  
 网络层用来处理在网络上流动的数据包。  
数据包是网络传输的最小数据单位。  
该层规定了通过怎样的路径(所谓的传输路线)到达对方计算机,并把数据包传送给对方。

### **链路层** 网络

**(又名数据链路层,网络接口层)**  
用来处理连接网络的硬件部分。  
包括控制操作系统、硬件的设备驱动、NIC(NetworkInterface Card,网络适配器,即网卡),及光纤等物理可见部分(还包括连接器等一切传输媒介)。  
硬件上的范畴均在链路层的作用范围之内。