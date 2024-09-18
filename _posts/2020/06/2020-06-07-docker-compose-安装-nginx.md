---
title: "docker-compose 安装 Nginx"
date: "2020-06-07"
categories: 
  - "nginx"
---

# 安装 带用户名密码的 Nginx

### 创建目录

```bash
mkdir -p nginx/conf/conf.d
mkdir -p nginx/conf/logs
cd nginx/
```

### 创建配置文件

```bash
tee > conf/nginx.conf << ERIC
user                        nginx;
worker_processes            1;

error_log                   /var/log/nginx/error.log warn;
pid                         /var/run/nginx.pid;

events {
    worker_connections      1024;
}

http {
    include                 /etc/nginx/mime.types;
    default_type            application/octet-stream;

    log_format              main  '\$remote_addr - \$remote_user [\$time_local] "\$request" '
                                  '\$status \$body_bytes_sent "\$http_referer" '
                                  '"\$http_user_agent" "\$http_x_forwarded_for"';

    access_log              /var/log/nginx/access.log  main;

    sendfile                on;
    #tcp_nopush             on;

    keepalive_timeout       65;

    #gzip                   on;

    include                 /etc/nginx/conf.d/*.conf;
    # 文件上传限制大小， 10M: 限制10M；   0: 为不限制
    client_max_body_size             0;
    client_header_buffer_size        128k;
    large_client_header_buffers  10  128k;
}
ERIC
```

### 创建密码文件

```bash
htpasswd -c conf/conf.d/passwdfile mao_siyu
```

_输入密码:_ `Qazwsx@1234`

### 配置Nginx`支持长链接`

```bash
tee > conf/conf.d/default.conf << ERIC
server {
    listen          8901;
    server_name     10.200.10.2:8901;

    location / {
        proxy_pass http://10.200.10.2:8902;  # 将请求代理到后端服务地址，也是WebSocket后端服务地址
        proxy_http_version 1.1;             # 设置HTTP版本为1.1
        proxy_set_header Upgrade \$http_upgrade;  # 识别WebSocket升级请求
        proxy_set_header Connection "upgrade";    # 升级连接为WebSocket
        proxy_set_header Host \$host;              # 传递原始主机头信息

        auth_basic "Restricted Access";  # 认证提示信息
        auth_basic_user_file /etc/nginx/conf.d/passwdfile;  # 密码文件路径

        expires -1; # 确保每次请求都不使用缓存
    }

    error_page      500 502 503 504  /50x.html;
    location = /50x.html {
        root        /usr/share/nginx/html;
    }
}
ERIC
```

### 创建docker-compose

```bash
tee > docker-compose.yaml << ERIC

version: '3.6'

services:

  nginx:
    image: nginx:1.19.0
    container_name: nginx
    network_mode: host
    restart: always
    ports:
      - 8901:8901
    volumes:
      - /etc/localtime:/etc/localtime
      - ./conf/nginx.conf:/etc/nginx/nginx.conf
      - ./conf/conf.d:/etc/nginx/conf.d
      - ./logs:/var/log/nginx

ERIC

```

* * *

* * *

* * *

# 默认方式安装部署Nginx

##### **[安装 Docker-Compose](%e5%ae%89%e8%a3%85-docker-compose "安装 Docker-Compose")**

* * *

##### 创建目录

```ruby
mkdir -p ./nginx/conf/conf.d
mkdir -p ./nginx/conf/logs
```

* * *

##### 创建配置文件

```ruby
cat > ./nginx/conf/nginx.conf << ERIC

user                        nginx;
worker_processes            1;

error_log                   /var/log/nginx/error.log warn;
pid                         /var/run/nginx.pid;


events {
    worker_connections      1024;
}


http {
    include                 /etc/nginx/mime.types;
    default_type            application/octet-stream;

    log_format              main  '\$remote_addr - \$remote_user [\$time_local] "\$request" '
                                  '\$status \$body_bytes_sent "\$http_referer" '
                                  '"\$http_user_agent" "\$http_x_forwarded_for"';

    access_log              /var/log/nginx/access.log  main;

    sendfile                on;
    #tcp_nopush             on;

    keepalive_timeout       65;

    #gzip                   on;

    include                 /etc/nginx/conf.d/*.conf;
    # 文件上传限制大小， 10M: 限制10M；   0: 为不限制
    client_max_body_size             0;
    client_header_buffer_size        128k;
    large_client_header_buffers  10  128k;
}

ERIC

```

* * *

##### 创建域名反响代理文件(**`可选`**)

```ruby
cat > ./nginx/conf/conf.d/gitlab.conf << ERIC

server {
    # 外网想要监听的端口
    listen          80;
    # 对应的 gitlab私服 域名
    server_name     gitlab.software.com;
    location / {
        # 指定 此域名根路径，要转发的 内网IP地址:端口
        proxy_pass  http://127.0.0.1:8080;
    }
}

ERIC

```

##### 创建default.conf文件(**`可选`**)

```ruby
cat > ./nginx/conf/conf.d/default.conf << ERIC

server {
    listen          80;
    server_name     localhost;

    #charset koi8-r;
    #access_log  /var/log/nginx/host.access.log  main;

    location / {
        root        /usr/share/nginx/html;
        index       index.html index.htm;
    }

    #error_page  404              /404.html;

    # redirect server error pages to the static page /50x.html
    #
    error_page      500 502 503 504  /50x.html;
    location = /50x.html {
        root        /usr/share/nginx/html;
    }

    # proxy the PHP scripts to Apache listening on 127.0.0.1:80
    #
    #location ~ \.php\$ {
    #    proxy_pass   http://127.0.0.1;
    #}

    # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
    #
    #location ~ \.php\$ {
    #    root           html;
    #    fastcgi_pass   127.0.0.1:9000;
    #    fastcgi_index  index.php;
    #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
    #    include        fastcgi_params;
    #}

    # deny access to .htaccess files, if Apache's document root
    # concurs with nginx's one
    #
    #location ~ /\.ht {
    #    deny  all;
    #}
}

ERIC

```

* * *

##### 创建 docker-compose 文件

```ruby
cat > ./nginx/docker-compose.yml << ERIC

version: '3.1'

services:

  nginx:
    image: nginx:1.19.0
    container_name: nginx
    network_mode: host
    restart: always
    ports:
      - 80:80
    volumes:
      # 容器与宿主机时间同步
      - /etc/localtime:/etc/localtime
      - ./conf/nginx.conf:/etc/nginx/nginx.conf
      - ./conf/conf.d:/etc/nginx/conf.d
      - ./logs:/var/log/nginx

ERIC

```

* * *

##### 启停

```ruby
cd ./nginx/
# 启动
docker-compose up -d
# 停止
docker-compose down
```

* * *
