---
title: 'Ubuntu 18.04 下载安装 wps'
date: '2018-06-05T16:40:52+00:00'
status: publish
permalink: /2018/06/05/ubuntu-18-04-%e4%b8%8b%e8%bd%bd%e5%ae%89%e8%a3%85-wps
author: 毛巳煜
excerpt: ''
type: post
id: 2147
category:
    - Ubuntu
tag: []
post_format: []
hestia_layout_select:
    - default
---
### 官网下载wps

```
<pre data-language="">```ruby
mao-siyu@pc:/mnt/1TB/download<span class="katex math inline">wget http://kdl.cc.ksosoft.com/wps-community/download/a21/wps-office_10.1.0.5672~a21_amd64.deb
--2018-06-05 16:07:32--  http://kdl.cc.ksosoft.com/wps-community/download/a21/wps-office_10.1.0.5672~a21_amd64.deb
正在解析主机 kdl.cc.ksosoft.com (kdl.cc.ksosoft.com)... 118.143.207.152, 106.48.14.8
正在连接 kdl.cc.ksosoft.com (kdl.cc.ksosoft.com)|118.143.207.152|:80... 已连接。
已发出 HTTP 请求，正在等待回应... 200 OK
长度： 82319222 (79M) [application/octet-stream]
正在保存至: “wps-office_10.1.0.5672~a21_amd64.deb”

wps-office_10.1.0.5672~a21_amd64.deb          100%[=================================================================================================>]  78.50M   232KB/s    用时 4m 50s

2018-06-05 16:12:23 (277 KB/s) - 已保存 “wps-office_10.1.0.5672~a21_amd64.deb” [82319222/82319222])

mao-siyu@pc:/mnt/1TB/download</span>

```
```

### 安装

```
<pre data-language="">```ruby
mao-siyu@pc:/mnt/1TB/download<span class="katex math inline">sudo dpkg -i wps-office_10.1.0.5672~a21_amd64.deb 
正在选中未选择的软件包 wps-office。
(正在读取数据库 ... 系统当前共安装有 175545 个文件和目录。)
正准备解包 wps-office_10.1.0.5672~a21_amd64.deb  ...
正在解包 wps-office (10.1.0.5672~a21) ...
dpkg: 依赖关系问题使得 wps-office 的配置工作不能继续：
 wps-office 依赖于 libpng12-0；然而：
  未安装软件包 libpng12-0。

dpkg: 处理软件包 wps-office (--install)时出错：
 依赖关系问题 - 仍未被配置
正在处理用于 gnome-menus (3.13.3-11ubuntu1) 的触发器 ...
正在处理用于 desktop-file-utils (0.23-1ubuntu3) 的触发器 ...
正在处理用于 mime-support (3.60ubuntu1) 的触发器 ...
正在处理用于 shared-mime-info (1.9-2) 的触发器 ...
正在处理用于 hicolor-icon-theme (0.17-2) 的触发器 ...
在处理时有错误发生：
 wps-office
mao-siyu@pc:/mnt/1TB/download</span>

```
```

### 解决异常

```
<pre data-language="">```ruby
# 下载缺少的库
mao-siyu@pc:/mnt/1TB/download<span class="katex math inline">wget http://kr.archive.ubuntu.com/ubuntu/pool/main/libp/libpng/libpng12-0_1.2.54-1ubuntu1_amd64.deb
--2018-06-05 16:34:31--  http://kr.archive.ubuntu.com/ubuntu/pool/main/libp/libpng/libpng12-0_1.2.54-1ubuntu1_amd64.deb
正在解析主机 kr.archive.ubuntu.com (kr.archive.ubuntu.com)... 103.22.220.133
正在连接 kr.archive.ubuntu.com (kr.archive.ubuntu.com)|103.22.220.133|:80... 已连接。
已发出 HTTP 请求，正在等待回应... 200 OK
长度： 116466 (114K) [application/vnd.debian.binary-package]
正在保存至: “libpng12-0_1.2.54-1ubuntu1_amd64.deb”

libpng12-0_1.2.54-1 100%[===================>] 113.74K   616KB/s    用时 0.2s 

2018-06-05 16:34:32 (616 KB/s) - 已保存 “libpng12-0_1.2.54-1ubuntu1_amd64.deb” [116466/116466])

mao-siyu@pc:/mnt/1TB/download</span> ll
总用量 241596
drwxrwxrwx  2 mao-siyu mao-siyu      4096 6月   5 16:34 ./
drwxrwxrwx 12 mao-siyu mao-siyu      4096 6月   5 16:14 ../
-rw-r--r--  1 mao-siyu mao-siyu    116466 1月   7  2016 libpng12-0_1.2.54-1ubuntu1_amd64.deb
-rw-r--r--  1 mao-siyu mao-siyu  82319222 6月  24  2016 wps-office_10.1.0.5672~a21_amd64.deb

```
```

### 重新安装

```
<pre data-language="">```ruby
# 安装缺少的库
mao-siyu@pc:/mnt/1TB/download<span class="katex math inline">sudo dpkg -i libpng12-0_1.2.54-1ubuntu1_amd64.deb
正在选中未选择的软件包 libpng12-0:amd64。
(正在读取数据库 ... 系统当前共安装有 178008 个文件和目录。)
正准备解包 libpng12-0_1.2.54-1ubuntu1_amd64.deb  ...
正在解包 libpng12-0:amd64 (1.2.54-1ubuntu1) ...
正在设置 libpng12-0:amd64 (1.2.54-1ubuntu1) ...
正在处理用于 libc-bin (2.27-3ubuntu1) 的触发器 ...
# 重新安装wps
mao-siyu@pc:/mnt/1TB/download</span> sudo dpkg -i wps-office_10.1.0.5672~a21_amd64.deb
(正在读取数据库 ... 系统当前共安装有 178020 个文件和目录。)
正准备解包 wps-office_10.1.0.5672~a21_amd64.deb  ...
正在将 wps-office (10.1.0.5672~a21) 解包到 (10.1.0.5672~a21) 上 ...
正在设置 wps-office (10.1.0.5672~a21) ...
正在处理用于 gnome-menus (3.13.3-11ubuntu1) 的触发器 ...
正在处理用于 desktop-file-utils (0.23-1ubuntu3) 的触发器 ...
正在处理用于 mime-support (3.60ubuntu1) 的触发器 ...
正在处理用于 shared-mime-info (1.9-2) 的触发器 ...
正在处理用于 hicolor-icon-theme (0.17-2) 的触发器 ...
mao-siyu@pc:/mnt/1TB/download$

```
```