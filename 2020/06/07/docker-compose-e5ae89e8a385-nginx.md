---
title: 'docker-compose 安装 Nginx'
date: '2020-06-07T03:48:59+00:00'
status: publish
permalink: /2020/06/07/docker-compose-%e5%ae%89%e8%a3%85-nginx
author: 毛巳煜
excerpt: ''
type: post
id: 5349
category:
    - nginx
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
安装 带用户名密码的 Nginx
================

### 创建目录

```bash
mkdir -p nginx/conf/conf.d
mkdir -p nginx/conf/logs
cd nginx/

```

### 创建配置文件

```bash
tee > conf/nginx.conf 
```

### 创建密码文件

```bash
htpasswd -c conf/conf.d/passwdfile mao_siyu

```

*输入密码:* `Qazwsx@1234`

### 配置Nginx`支持长链接`

```bash
tee > conf/conf.d/default.conf 
```

### 创建docker-compose

```bash
tee > docker-compose.yaml 
```

- - - - - -

- - - - - -

- - - - - -

默认方式安装部署Nginx
=============

##### **[安装 Docker-Compose](http://www.dev-share.top/2019/06/12/%e5%ae%89%e8%a3%85-docker-compose/ "安装 Docker-Compose")**

- - - - - -

##### 创建目录

```ruby
mkdir -p ./nginx/conf/conf.d
mkdir -p ./nginx/conf/logs

```

- - - - - -

##### 创建配置文件

```ruby
cat > ./nginx/conf/nginx.conf 
```

- - - - - -

##### 创建域名反响代理文件(**`可选`**)

```ruby
cat > ./nginx/conf/conf.d/gitlab.conf 
```

##### 创建default.conf文件(**`可选`**)

```ruby
cat > ./nginx/conf/conf.d/default.conf 
```

- - - - - -

##### 创建 docker-compose 文件

```ruby
cat > ./nginx/docker-compose.yml 
```

- - - - - -

##### 启停

```ruby
cd ./nginx/
# 启动
docker-compose up -d
# 停止
docker-compose down

```

- - - - - -