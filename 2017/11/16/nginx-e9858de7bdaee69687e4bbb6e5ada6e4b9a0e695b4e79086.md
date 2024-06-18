---
title: 'Nginx 配置文件学习整理'
date: '2017-11-16T14:17:05+00:00'
status: publish
permalink: /2017/11/16/nginx-%e9%85%8d%e7%bd%ae%e6%96%87%e4%bb%b6%e5%ad%a6%e4%b9%a0%e6%95%b4%e7%90%86
author: 毛巳煜
excerpt: ''
type: post
id: 362
category:
    - nginx
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### /etc/nginx/nginx.conf 默认配置说明

```ruby
# nginx 的默认用户是 nginx
user                       nginx;
# worker进程的数量，可以设置为 固定数量 ，也可以配置为 auto 自动调整为可用的CPU内核数量
worker_processes           1;

# 告诉nginx 异常日志放在哪儿
error_log                  /var/log/nginx/error.log warn;
# 默认的pid, 注释掉也可以运行，仍然是这个目录
pid                        /var/run/nginx.pid;


events {
    # 单个worker可以允许同时建立外部连接的数量
    worker_connections     1024;
}


http {
    include                /etc/nginx/mime.types;
    default_type           application/octet-stream;

    # 告诉nginx 输出的日志格式是什么
    log_format             main  '<span class="katex math inline">remote_addr -</span>remote_user [<span class="katex math inline">time_local] "</span>request" '
                                 '<span class="katex math inline">status</span>body_bytes_sent "<span class="katex math inline">http_referer" '
                                 '"</span>http_user_agent" "$http_x_forwarded_for"';

    # 告诉nginx 正常的访问日志放在哪儿
    access_log            /var/log/nginx/access.log  main;

    sendfile              on;
    #tcp_nopush           on;

    keepalive_timeout     65;

    #gzip                 on;

    # 告诉nginx 扩展的配置文件放在哪儿
    include               /etc/nginx/conf.d/*.conf;
}


```

- - - - - -

- - - - - -

- - - - - -

###### 请求连接限制

```ruby
user                       nginx;
worker_processes           1;

error_log                  /var/log/nginx/error.log warn;
pid                        /var/run/nginx.pid;


events {
    worker_connections     1024;
}


http {
    include                /etc/nginx/mime.types;
    default_type           application/octet-stream;

    log_format             main  '<span class="katex math inline">remote_addr -</span>remote_user [<span class="katex math inline">time_local] "</span>request" '
                                 '<span class="katex math inline">status</span>body_bytes_sent "<span class="katex math inline">http_referer" '
                                 '"</span>http_user_agent" "<span class="katex math inline">http_x_forwarded_for"';

    access_log            /var/log/nginx/access.log  main;

    sendfile              on;
    #tcp_nopush           on;

    keepalive_timeout     65;

    #gzip                 on;

    include               /etc/nginx/conf.d/*.conf;

    ## 制定连接限制规则： 既是访问速率限制，有助于防范DDoS攻击，以及业务秒杀活动中的薅羊毛行为
    ## limit_req_zone [key] [shared memory zone] [rate]
    ## limit_req_zone [区分客户] [保存key状态名称的空间大小] [每秒r/s或每分r/m的请求数]
    ## 制定规则限制每秒内只能请求1次，否则返回 503
    limit_req_zone</span>binary_remote_addr zone=one:10m rate=1r/s;

    server {
        listen            80 default_server;
        location /search/ {
            # 告诉nginx，对/search/的请求，使用这个连接限制规则
            limit_req     zone=one;
        }
    }
}


```

- - - - - -

- - - - - -

- - - - - -