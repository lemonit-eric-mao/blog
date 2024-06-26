---
title: "Linux IDEA 错误: 代理抛出异常错误: java.net.MalformedURLException: Local host name unknown: java.net.UnknownHostException"
date: "2017-11-16"
categories: 
  - "开发工具"
---

- 开发工具: IDEA 2017.2
- 操作系统: Ubuntu 16.04

### **问题描述**

**使用 IDEA 开发spring boot 项目时, 把项目的名称改了, 然后在次运行 spring boot 时出现如下异常信息:**

`错误: 代理抛出异常错误: java.net.MalformedURLException: Local host name unknown: java.net.UnknownHostException: mao-siyu-PC: mao-siyu-PC: 未知的名称或服务 Process finished with exit code 1` 在网上搜索很多案例都未能解决这个问题, 首先声明这个异常 `与 IDEA 与 spring boot 无关`

### **排除方法:**

**打开自己的终端**

```ruby
mao-siyu@mao-siyu-PC:~$
mao-siyu@mao-siyu-PC:~$ hostname
mao-siyu-PC
mao-siyu@mao-siyu-PC:~$
```

接下来要确认 `/etc/hosts` 文件中 有没有你的这个 hostname , 基本上是没有, 要是有就不会出错了.

### **根据问题得出两个解决方案:**

**第一种方案:** 把自己的hostname 改成 `/etc/hosts` 文件中已有的hostname 需要重启

```ruby
mao-siyu@mao-siyu-PC:~$
mao-siyu@mao-siyu-PC:~$ hostname localhost
mao-siyu@mao-siyu-PC:~$ reboot
mao-siyu@localhost:~$
```

**第二种方案:** 将自己的hostname 添加到 `/etc/hosts` 文件中 不需要重启

```ruby
mao-siyu@mao-siyu-PC:~$ cat /etc/hosts
127.0.0.1       localhost mao-siyu-PC
::1             localhost ip6-localhost ip6-loopback
mao-siyu@mao-siyu-PC:~$

```
