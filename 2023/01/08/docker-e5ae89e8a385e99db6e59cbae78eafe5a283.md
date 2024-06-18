---
title: 'Docker 安装靶场环境'
date: '2023-01-08T07:12:49+00:00'
status: private
permalink: /2023/01/08/docker-%e5%ae%89%e8%a3%85%e9%9d%b6%e5%9c%ba%e7%8e%af%e5%a2%83
author: 毛巳煜
excerpt: ''
type: post
id: 9656
category:
    - 自学整理
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
第一种：DVWA
--------

### 启动服务

- ```shell
  docker run --rm -itd -p 80:80 \
    registry.cn-qingdao.aliyuncs.com/cn-aliyun/dvwa:1.0
  
  ```

1. web浏览器 打开查看 http://192.168.101.30/setup.php 
  - [![dvwa-01](http://qiniu.dev-share.top/image/linux/dvwa-01.png)](http://qiniu.dev-share.top/image/linux/dvwa-01.png)
2. 点击 **Create/Reset Database**
  - 稍等一会，就会跳转到一个 登陆页面
  - [![dvwa-02](http://qiniu.dev-share.top/image/linux/dvwa-02.png)](http://qiniu.dev-share.top/image/linux/dvwa-02.png)
3. 输入用户密码 **admin/password**
  - [![dvwa-03](http://qiniu.dev-share.top/image/linux/dvwa-03.png)](http://qiniu.dev-share.top/image/linux/dvwa-03.png)

第二种：pikachu
-----------

### 启动服务

- ```shell
  docker run --rm -itd -p 81:80 \
    registry.cn-qingdao.aliyuncs.com/cn-aliyun/pikachu:1.0
  
  ```

1. web浏览器 打开查看 http://192.168.101.30:81

- [![dvwa-04](http://qiniu.dev-share.top/image/linux/dvwa-04.png)](http://qiniu.dev-share.top/image/linux/dvwa-04.png)