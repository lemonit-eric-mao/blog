---
title: "使用Charles抓包 解析https"
date: "2017-11-16"
categories: 
  - "网络基础"
---

Charles 版本： 4.1.4 [官方下载地址](https://www.charlesproxy.com/)

### **破解**

下载: [charles.jar](http://url.cn/5DKxnSs) **按照下面的路径找到 charles.jar文件并替换**

> 你的Charles安装目录\\Charles\\lib\\charles.jar

### **第一步 将 Charles 设置成系统代理**

windows系统选择: Proxy --> Windows Proxy **这样现在这台电脑中的部分请求就会被 Charles 监听**

### **为当前这台电脑安装证书**

> Help --> SSL Proxying --> Install Charles Root Certificate

### **安装证书**

安装证书 --> 下一步 --> 将所有的证书放入下列存储 --> 点击浏览按钮 --> 选择个人 --> 确定 --> 下一步 --> 完成

### **开始抓包**

> Proxy --> Start Recording

**注意 现在还不能解析https请求， 这个时候查看是乱码的， 需要在https://协议的连接地址上`点击右键鼠标 --> Enable SSL Proxying`然后点击上面的刷新按钮,然后在次查看解析成功！**

### **手机抓包**

Android 小米 WLAN

### **Charles 配置**

> Proxy --> Proxy Settings --> Proxies（选项卡） --> HTTP Proxy（区域） --> Port: 8888 --> 勾选 Enable transparent HTTP proxying --> 完成

手机连接上wifi，点击、查看网络详情 --> 将代理 设置为手动 --> 输入你的Charles 所在的地址， 端口： 8888

连接成功以后 Charles 会弹出一个提示框 ，让你选择 Allow Deny 选择Allow 允许连接

### **为手机安装证书**

> Help --> SSL Proxying --> Install Charles Root Certificate on a Mobile Device or Remote Browser

点击后会有一个提示是告诉你如何获取 Charles 证书的， 一般默认是 在手机的`QQ浏览器中输入 http://chls.pro/ssl`

Android手机我只试这QQ浏览器可以下载，默认自带的浏览器不行，无法安装证书。

接下来在使用手机发出的请求响应都会被监听到。

### **修改已经启用的 SSL Proxying**

> Proxy --> SSL Proxy Settings 它支持通配 常规写法 www.baidu.com m.baidu.com 通配写法 \*.baidu.com

### **删除手机中的CA**

> 系统安全 --> 信任的凭据 --> 用户 --> 点击相应的证书可以删除
