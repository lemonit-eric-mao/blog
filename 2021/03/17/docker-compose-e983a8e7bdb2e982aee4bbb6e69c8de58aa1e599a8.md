---
title: 'docker-compose 部署邮件服务器'
date: '2021-03-17T00:10:07+00:00'
status: publish
permalink: /2021/03/17/docker-compose-%e9%83%a8%e7%bd%b2%e9%82%ae%e4%bb%b6%e6%9c%8d%e5%8a%a1%e5%99%a8
author: 毛巳煜
excerpt: ''
type: post
id: 7042
category:
    - 运维
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### 前置条件

本机IP： 124.93.26.39

- - - - - -

###### docker-compose文件

```ruby
cat > docker-compose.yaml 
```

- - - - - -

- 邮箱管理后台: http://124.93.26.39:8081
- 默认用户: admin
- 默认密码: ewomail123

- - - - - -

- Rainloop 管理端: http://124.93.26.39:1080/?admin
- 默认用户: admin
- 默认密码: 12345

- - - - - -

- Rainloop 用户端: http://124.93.26.39:1080

- - - - - -