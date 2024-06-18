---
title: 'Nginx 多域名配置 (三)'
date: '2017-11-16T14:15:51+00:00'
status: publish
permalink: /2017/11/16/nginx-%e5%a4%9a%e5%9f%9f%e5%90%8d%e9%85%8d%e7%bd%ae-%e4%b8%89
author: 毛巳煜
excerpt: ''
type: post
id: 360
category:
    - nginx
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
### 多个域名，每个域名对应自己的服务器

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@localhost ~]# vim /etc/nginx.conf

# Load modular configuration files from the /etc/nginx/conf.d directory.
# See http://nginx.org/en/docs/ngx_core_module.html#include
# for more information.

... 以上省略
    include /etc/nginx/conf.d/*.conf;
    client_header_buffer_size    128k;
    large_client_header_buffers  10 128k;
... 以下省略

# Settings for a TLS enabled server.
#
#    server {
#        listen       443 ssl http2 default_server;
#        listen       [::]:443 ssl http2 default_server;
#        server_name  _;
#        root         /usr/share/nginx/html;

```
```

### 创建 manage.conf

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@localhost ~]# vim /etc/nginx/conf.d/manage.conf
     server {
            # 外网想要监听的端口
            listen 80;
            # 对应的域名
            server_name manage.private-blog.com;
            location / {
                # 指定http://127.0.0.1:port
                proxy_pass http://127.0.0.1:8080;
            }
     }

```
```

### 创建 service.conf

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@localhost ~]# vim /etc/nginx/conf.d/service.conf
     server {
            # 外网想要监听的端口
            listen 80;
            # 对应的域名
            server_name service.private-blog.com;
            location / {
                # 指定http://127.0.0.1:port
                proxy_pass http://127.0.0.1:8080;
            }
     }

```
```