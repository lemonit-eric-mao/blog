---
title: 'docker-compose 安装 HAProxy 做反向代理'
date: '2020-08-23T01:50:25+00:00'
status: publish
permalink: /2020/08/23/docker-compose-%e5%ae%89%e8%a3%85-haproxy-%e5%81%9a%e5%8f%8d%e5%90%91%e4%bb%a3%e7%90%86
author: 毛巳煜
excerpt: ''
type: post
id: 5907
category:
    - HAProxy
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### 创建目录

```ruby
mkdir -p /home/haproxy/config

```

- - - - - -

###### 创建配置文件 haproxy.cfg

**`/home/deploy/haproxy/config/haproxy.cfg`**

```ruby
global
  maxconn 10000                 # 最大同时10000连接
  daemon                        # 以daemon方式在后台运行

defaults
  log  127.0.0.1 local0 info    # [emerg, alert, crit, err, warning, notice, info, debug]
  # mode http                   # 默认的模式mode { tcp|http|health }，tcp是4层，http是7层，health只会返回OK
  retries         3             # 连接后端服务器失败重试次数，超过3次后会将失败的后端服务器标记为不可用。
  timeout client  1h            # 客户端响应超时             1小时
  timeout server  1h            # server端响应超时           1小时
  timeout connect 1h            # 连接server端超时           1小时
  timeout check   10s           # 对后端服务器的检测超时时间 10秒

listen stats                    # 定义监控页面
  mode  http
  bind  *:1080                  # 绑定Docker容器内的1080端口
  stats refresh 1s              # 每1秒更新监控数据
  stats uri /stats              # 访问监控页面的uri
  stats realm HAProxy\ Stats    # 监控页面的认证提示
  stats auth admin:654321       # 监控页面的用户名和密码

# 80 端口请求拦截
frontend main_front
  bind  *:80                    # 监听Docker容器内的80端口

  # 定义 ACL规则
  acl web     hdr_dom(host)     -i www.twibao.top
  acl manage  hdr_dom(host)     -i manage.twibao.top
  acl manage  path_beg          -i /static /images /javascript /stylesheets
  acl manage  path_end          -i .jpg .gif .png .css .js

  # 应用 ACL规则 对接收到的http请求进行匹配
  use_backend web_back          if   web
  use_backend manage_back       if   manage

  # 如果前面的ACL都没有匹配成功就访问默认的ACL
  default_backend default_back

# 转发到 web服务器
backend web_back
  option    tcp-check
  balance   roundrobin
  # 注意：这里不能使用 127.0.0.1来访问同服务器的应用程序，因为这是在Docker容器中的访问， 所以我们要使用宿主机的IP来访问
  server    web_server      192.168.2.10:8080 check inter 10s rise 3 fall 3 weight 1

# 转发到 web后台管理服务器
backend manage_back
  option    tcp-check
  balance   roundrobin
  server    manage_server   192.168.2.10:8099 check inter 10s rise 3 fall 3 weight 1

# 都匹配不上的默认转发
backend default_back
  option    tcp-check
  balance   roundrobin
  server    default_server  192.168.2.10:8080 check inter 10s rise 3 fall 3 weight 1


```

- - - - - -

###### 创建compose文件

```ruby
cat > /home/deploy/haproxy/docker-compose.yaml 
```

- - - - - -

**外网请求**: `http://www.twibao.top` 会被转发到 web前端服务器  
**外网请求**: `http://mysql.twibao.top` 会被转发到 数据库

- - - - - -

- - - - - -

- - - - - -

###### **什么是 ACL?** (`访问控制列表`)

**acl**：  
 对接收到的报文进行匹配和过滤，基于请求报文头部中的源地址、源端口、目标地址、目标端口、请求方法、URL、文件后缀等信息内容进行匹配并执行进一步操作。

**ACL语法如下**:  
 acl <aclname> <criterion> \[flags\] \[operator\] \[<value>\] ...  
 acl 名称 条件 条件标记位 具体操作符 操作对象类型</value></criterion></aclname>

**示例** :  
 acl web hdr\_dom(host) -i www.twibao.top

**`hdr <string></string>`: 用于匹配URL的规则**

```
hdr_dom(host):
　　请求的host名称，如www.yinzhengjie.org.cn
hdr_beg(host):
　　请求的host开头，如www. img. video. download. ftp.
hdr_end(host):
　　请求的host结尾，如.com .net .cn
path_beg:
　　请求的URL开头，如/static、/images、/img、/css
path_end:
　　请求的URL中资源的结尾，如.gif .png .css .js .jpg .jpeg

```

- - - - - -

- - - - - -

- - - - - -