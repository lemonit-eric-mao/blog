---
title: '使用Charles抓包 解析https Ubuntu 16.0.4'
date: '2017-11-16T16:36:57+00:00'
status: publish
permalink: /2017/11/16/%e4%bd%bf%e7%94%a8charles%e6%8a%93%e5%8c%85-%e8%a7%a3%e6%9e%90https-ubuntu-16-0-4
author: 毛巳煜
excerpt: ''
type: post
id: 549
category:
    - 网络基础
tag: []
post_format: []
---
Charles 版本： 4.1.4  
[官方下载地址](https://www.charlesproxy.com/)

##### 破解

下载地址: https://www.charlesproxy.com/assets/release/4.1.4/charles-proxy-4.1.4\_amd64.tar.gz  
**按照下面的路径找到 charles.jar文件并替换**

```
  你的Charles安装目录\Charles\lib\charles.jar

```

##### 解压

```ruby
mao-siyu@mao-siyu-PC:~<span class="katex math inline">mkdir charles
mao-siyu@mao-siyu-PC:~</span> cd charles/
mao-siyu@mao-siyu-PC:~/charles$ tar -xzvf charles-proxy-4.1.4_amd64.tar.gz

```

##### 使用root权限启动

```ruby
mao-siyu@mao-siyu-PC:~/charles<span class="katex math inline">cd charles/bin/
mao-siyu@mao-siyu-PC:~/charles/charles/bin</span> ll
总用量 12
drwxr-xr-x 2 mao-siyu mao-siyu 4096 8月  23 13:40 ./
drwxr-xr-x 7 mao-siyu mao-siyu 4096 7月  10 18:53 ../
-rwxr-xr-x 1 mao-siyu mao-siyu 1326 7月  10 18:53 charles*
mao-siyu@mao-siyu-PC:~/charles/charles/bin<span class="katex math inline">mao-siyu@mao-siyu-PC:~/charles/charles/bin</span> sudo ./charles
[sudo] mao-siyu 的密码：

```

##### 第一步 将 Charles 设置成系统代理

Ubuntu 系统选择: Proxy --&gt; Mozilla Firefox Proxy  
**这样现在这台电脑中的部分请求就会被 Charles 监听**

##### 为当前这台电脑安装证书

```
  Help --> SSL Proxying --> Install Charles Root Certificate

```

##### 安装证书

点击导入

##### 为Firefox 浏览器添加证书

```
  Help --> SSL Proxying --> Install Charles Root Certificate on a Mobile Device or Remote Browser
  根据Charles提示, 首先要为Firefox浏览器配置手动代理, 我的代理地址为 172.17.0.1:8888
  打开Firefox浏览器 --> 菜单 --> 首选项 --> 高级 --> 网络
  --> 点击连接选项中的设置按钮 --> 弹出连接设置窗体
  --> 选择手动代理
  --> 所有的代理IP 都填写为 172.17.0.1 端口为 8888
  --> 确定

```

然后在Firefox浏览器中输入 chls.pro/ssl 来安装证书

##### 开始抓包

```
  Proxy --> Start Recording

```

**注意 现在还不能解析https请求， 这个时候查看是乱码的，需要在https://协议的连接地址上`点击右键鼠标 --> Enable SSL Proxying`然后点击上面的刷新按钮, 在次查看解析成功!**