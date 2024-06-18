---
title: 'Nginx 配置文件常用模块作用 (二)'
date: '2017-11-16T14:13:57+00:00'
status: publish
permalink: /2017/11/16/nginx-%e9%85%8d%e7%bd%ae%e6%96%87%e4%bb%b6%e5%b8%b8%e7%94%a8%e6%a8%a1%e5%9d%97%e4%bd%9c%e7%94%a8-%e4%ba%8c
author: 毛巳煜
excerpt: ''
type: post
id: 358
category:
    - nginx
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### nginx.conf 模块结构图

```ruby
Main
├── events
│
├── http
│   ├── server
│   │   └── location
│   └── upstream
│
└── stream
    ├── server
    └── upstream

```

- - - - - -

###### NGINX 主配置文件 nginx.conf

```ruby
#user  nobody;
worker_processes  1;
#pid        logs/nginx.pid;


events {
    worker_connections  1024;
}


# http模块： 主要是定义，NGINX如何处理，HTTP/HTTPS连接
http {

    # server模块： 主要是定义 "虚拟服务器" 和 "虚拟主机", 用来处理http请求
    # 作用： 配置入口
    server {

        # location模块： 是http模块中 "独有的模块"， 它用可以更进一步的对http流量做 "URI的分类"
        # 常用location修饰器：
        #     ~* 不区分大小写正则表达式
        #     ~  区分大小写正则表达式
        #     ^~ 不使用正则表达式
        #     =  精确匹配
        # 作用： 拦截URI
        location / {
            # 作用： 配置转发
            proxy_pass http://127.0.0.1/8066
            # ......
        }

    }

    # upstream模块： 定义后端服务器组
    # 作用： 负载均衡
    upstream {
        server 127.0.0.1:8000 weight=3;
        server 127.0.0.1:8001;
        server 127.0.0.1:8002;
        # ......
    }

}


# stream块 主要是以处理 "TCP/UDP流量" 为主
stream {

    server {
        # ......
    }

    upstream {
        # ......
    }

}

```

- - - - - -

- - - - - -

- - - - - -

##### proxy\_pass主要用于实现 **`反向代理`**

**客户端请求: http://www.example.com/application1/user1/index.html**

```ruby
    server {
        listen 80 default_server;
        server_name www.example.com;

        # 带路径的 proxy_pass
        location /application1/ {
            # 此操作会替换 "原始请求" 的URL路径, 例如：
            proxy_pass http://192.168.2.10:8080/otherapp/
            # 实际结果
            # 原始请求URL:       http://www.example.com/application1/user1/index.html
            # 服务端收到的URL:    http://192.168.2.10:8080/otherapp/user1/index.html
        }

        # 不带路径的 proxy_pass
        location /application1/ {
            proxy_pass http://192.168.2.10:8080
            # 实际结果
            # 原始请求URL:       http://www.example.com/application1/user1/index.html
            # 服务端收到的URL:    http://192.168.2.10:8080/application1/user1/index.html
        }

    }


```

- - - - - -

- - - - - -

- - - - - -

##### NGINX 访问限制指令 `allow、deny、satisfy`

 Nginx 处理请求的过程一共划分为 11 个阶段，按照执行顺序依次是 post-read、server-rewrite、find-config、rewrite、post-rewrite、preaccess、access、post-access、try-files、content 以及 log。  
![](http://qiniu.dev-share.top/nginx-11.png)

- **allow** 允许ip
- **deny** 限制ip
- **satisfy** 在Nginx处理请求的11个阶段中的`access阶段`的模块的限制指令

```ruby
http {

    server {

        location / {
            # 屏蔽单个IP
            deny 192.168.1.1
            # 封整个IP段 从123.0.0.1到123.255.255.254的命令
            deny 123.0.0.0/8
            # 封IP段 从123.177.0.1到123.177.255.254的命令
            deny 123.177.0.0/16

            # 允许IP段 从123.177.22.1到123.177.22.254的命令是
            allow 123.177.22.0/24

            # satisfy  all | any ;
            # 如果在一个字段中同时使用了Access模块和Auth Basic模块的指令，可以使用这个指令确定一种验证方式：
            # all - 必须同时匹配Access和Auth Basic中指令指定的权限。
            # any - 具有Access 或 Auth Basic指令任一权限即可通过匹配
            satisfy any;
            auth_basic "closed site";
            auth_basic_user_file conf/htpasswd;
        }

    }
}


```

- - - - - -

- - - - - -

- - - - - -

##### 流量限制指令

- **limit\_req\_zone** 限流量， 用来限制单位时间内的请求数，即速率限制。
- **limit\_req\_conn** 限并发， 用来限制同一时间连接数，即并发限制。

###### **limit\_req\_zone** 限流量

```ruby
http {
    # 第一个参数： <span class="katex math inline">binary_remote_addr   表示通过remote_addr这个标识来做限制，"binary_"的目的是缩写内存占用量，是限制同一客户端ip地址。
    # 第二个参数： zone=one:10m          表示生成一个大小为10M，名字为one的内存区域，用来存储访问的频次信息。
    # 第三个参数： rate=1r/s             表示允许相同标识的客户端的访问频次，这里限制的是每秒1次，还可以有比如30r/m的。
    limit_req_zone</span>binary_remote_addr zone=one:10m rate=1r/s;

    server {
        location /search/ {
            # 第一个参数： zone=one      设置使用哪个配置区域来做限制，与上面limit_req_zone 里的name对应。
            # 第二个参数： burst=5       burst爆发的意思，这个配置的意思是设置一个大小为5的缓冲区当有大量请求（爆发）过来时，超过了访问频次限制的请求可以先放到这个缓冲区内。
            # 第三个参数： nodelay       如果设置，超过访问频次而且缓冲区也满了的时候就会直接返回503，如果没有设置，则所有请求会等待排队。
            limit_req zone=one burst=5 nodelay;
        }
    }
}

```

- - - - - -

- - - - - -

- - - - - -