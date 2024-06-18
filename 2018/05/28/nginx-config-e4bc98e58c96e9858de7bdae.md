---
title: 'Nginx config 优化配置'
date: '2018-05-28T15:23:50+00:00'
status: publish
permalink: /2018/05/28/nginx-config-%e4%bc%98%e5%8c%96%e9%85%8d%e7%bd%ae
author: 毛巳煜
excerpt: ''
type: post
id: 2119
category:
    - nginx
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
###### Nginx 请求追踪

**场景**： 几百台服务器集群，每天有上亿笔的交易， 其中只有10几笔交易存在问题，该如排查？，该如何定位异常发生在哪台服务器上?

**思路**： nginx 对每个请求都会产生一个唯一的ID, 唯一ID的变量是 **`$request_id`** ； 通过在 请求头中加入 **$request\_id** 变量，将nginx的唯一ID传输到每个服务器的日志中, 最后从日志中根据 唯一ID进行问题反查。

```ruby
server {
    listen 80;
    location / {
        proxy_pass          http://app_server;
        # 通过在 请求头中加入 <span class="katex math inline">request_id 变量，将nginx的唯一ID传输到每个服务器的日志中
        proxy_set_header    X-Request-ID</span>request_id;
        access_log          /var/log/nginx/access_trace.log    trace;
    }
}

```

- - - - - -

- - - - - -

- - - - - -

```ruby
[root@k8s-master ~]# cat nginx.conf

# 运行用户，默认是nginx，可不设置。作用：
user www www;
# nginx进程,一般设置为和cpu核数一样。作用：
worker_processes auto;
# 错误日志存放目录
error_log /usr/local/nginx/logs/error_nginx.log crit;
# 进程pid存放位置
pid /usr/local/nginx/nginx_pid/nginx.pid;
# 最大文件打开数（连接），可设置为系统优化后的ulimit -HSn的结果
worker_rlimit_nofile 51200;
# cpu亲和力配置，让不同的进程使用不同的cpu
worker_cpu_affinity 0001 0010 0100 1000 0001 00100100 1000;

# 工作模式及连接数上限
events {
  # epoll是多路复用IO(I/O Multiplexing)中的一种方式, 但是仅用于linux2.6以上内核。作用：可以大大提高nginx的性能
  use epoll;
  # 单个后台worker process进程的最大并发链接数
  worker_connections 51200;
  multi_accept on;
}

# ###########################################################

http {
  # 文件扩展名与类型映射表
  include mime.types;
  # 默认文件类型
  default_type application/octet-stream;
  # # limit模块。作用：可防范一定量的DDOS攻击
  # # 用来存储session会话的状态，如下是为session分配一个名为one的10M的内存存储区，限制了每秒只接受一个ip的一次请求 1r/s
  # limit_req_zone <span class="katex math inline">binary_remote_addr zone=one:10m rate=1r/s;
  # limit_conn_zone</span>binary_remote_addr zone=addr:10m;
  # include       mime.types;
  # default_type  application/octet-stream;

  # 设定请求缓存
  server_names_hash_bucket_size 128;
  client_header_buffer_size 32k;
  large_client_header_buffers 4 32k;
  client_max_body_size 1024m;
  client_body_buffer_size 10m;

  # 连接超时时间，单位是秒
  keepalive_timeout 120;

  # 隐藏响应header和错误通知中的版本号
  server_tokens off;
  # 开启高效传输模式
  sendfile on;

  # 激活tcp_nopush参数可以允许把httpresponse header和文件的开始放在一个文件里发布，积极的作用是减少网络报文段的数量
  tcp_nopush on;
  # 激活tcp_nodelay，内核会等待将更多的字节组成一个数据包，从而提高I/O性能
  tcp_nodelay on;

  # FastCGI相关参数。作用：为了改善网站性能, 减少资源占用，提高访问速度
  fastcgi_connect_timeout 300;
  fastcgi_send_timeout 300;
  fastcgi_read_timeout 300;
  fastcgi_buffer_size 64k;
  fastcgi_buffers 4 64k;
  fastcgi_busy_buffers_size 128k;
  fastcgi_temp_file_write_size 128k;
  fastcgi_intercept_errors on;

  # Gzip Compression
  # 开启gzip压缩功能
  gzip on;
  # 设置允许压缩的页面最小字节数，页面字节数从header头的Content-Length中获取。默认值是0，表示不管页面多大都进行压缩。建议设置成大于1K。如果小于1K可能会越压越大。
  gzip_min_length 256k;
  # 压缩缓冲区大小。表示申请16个单位为8K的内存作为压缩结果流缓存，默认值是申请与原始数据大小相同的内存空间来存储gzip压缩结果
  gzip_buffers 16 8k;
  # 压缩版本, 默认是1.1，目前大部分浏览器已经支持GZIP解压，使用默认即可
  gzip_http_version 1.1;
  # 压缩比率。用来指定GZIP压缩比，1压缩比最小，处理速度最快； 9压缩比最大，传输速度快，但处理最慢，也比较消耗cpu资源
  gzip_comp_level 6;
  gzip_proxied any;
  # vary header支持。该选项可以让前端的缓存服务器缓存经过GZIP压缩的页面。例如: 用Squid缓存经过Nginx压缩的数据
  gzip_vary on;
  # 用来指定压缩的类型，"text/html"类型总是会被压缩
  gzip_types
    text/xml application/xml application/atom+xml application/rss+xml application/xhtml+xml image/svg+xml
    text/javascript application/javascript application/x-javascript
    text/x-json application/json application/x-web-app-manifest+json
    text/css text/plain text/x-component
    font/opentype application/x-font-ttf application/vnd.ms-fontobject
    image/x-icon;
  gzip_disable "MSIE [1-6]\.(?!.*SV1)";

  #If you have a lot of static files to serve through Nginx then caching of the files' metadata (not the actual files' contents) can save some latency.
  open_file_cache max=1000 inactive=20s;
  open_file_cache_valid 30s;
  open_file_cache_min_uses 2;
  open_file_cache_errors on;

######################## default ############################
#  server {
#    listen 80;
#    server_name _;
#    access_log logs/access_nginx.log combined;
#    #root /data/wwwroot/default;
#    #index index.html index.htm index.jsp;
#    #error_page 404 /404.html;
#    #error_page 502 /502.html;
#    location /nginx_status {
#      stub_status on;
#      access_log off;
#      allow 127.0.0.1;
#      deny all;
#    }
#    location ~ .*\.(gif|jpg|jpeg|png|bmp|swf|flv|mp4|ico)<span class="katex math inline">{
#      expires 30d;
#      access_log off;
#    }
#    location ~ .*\.(js|css)?</span> {
#      expires 7d;
#      access_log off;
#    }
#    location ~ {
#      proxy_pass http://127.0.0.1:8080;
#      include proxy.conf;
#    }
#    location ~ /\.ht {
#      deny all;
#    }
#  }
########################## vhost #############################
  include vhost/*.conf;
}
[root@k8s-master ~]#


```