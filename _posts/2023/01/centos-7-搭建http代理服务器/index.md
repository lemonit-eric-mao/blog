---
title: "CentOS 7 搭建HTTP代理服务器"
date: "2023-01-28"
categories: 
  - "linux服务器"
---

# CentOS 7 搭建代理服务器

> TinyProxy 和 Squid 都是比较优秀的代理软件 TinyProxy比较小众，虽然没有Squid的功能丰富，但是小巧简单，也能满足普通用户的需求。 Squid 是一款优秀的代理软件，有很丰富的ACL管理功能，虽然squid很强大，但配置比较繁琐。

## TinyProxy

1. **安装 TinyProxy**
    
    - > 本机IP地址 172.16.15.205
        
    - ```shell
        yum -y install tinyproxy
        ```
        
2. **配置 TinyProxy**
    
    - ```shell
        vim /etc/tinyproxy/tinyproxy.conf
        
        # 默认端口为 8888
        Port 8888
        
        # 注释掉 Allow，表示允许所有人访问代理
        #Allow 127.0.0.1
        
        # 隐藏掉Via请求头部，去掉下面的注释
        DisableViaHeader Yes
        
        ```
        
3. **启动 TinyProxy**
    
    - ```shell
        systemctl start tinyproxy.service
        
        ## 查看
        netstat -lntp | grep -E "PID|*8888"
        (No info could be read for "-p": geteuid()=1001 but you should be root.)
        Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
        tcp        0      0 0.0.0.0:8888            0.0.0.0:*               LISTEN      -
        
        ```
        

## 测试 TinyProxy

- > 找一台不能访问外网的 CentOS 7 系统，做如下操作
    
- ```shell
    ## 在控制台临时执行，如果希望永久执行，可以把如下配置添加到 /etc/profile
    export PROXY="http://172.16.15.205:8888"
    # http代理
    export http_proxy=$PROXY
    # https代理
    export https_proxy=$PROXY
    # ftp代理
    export ftp_proxy=$PROXY
    # 不代理
    export no_proxy="localhost, 127.0.0.1, ::1"
    ```
    
- ```shell
    wget http://qiniu.dev-share.top/tools/k9s_Linux_x86_64.tar.gz
    ## 测试下载成功
    Connecting to 172.16.15.205:8888... connected.
    Proxy request sent, awaiting response... 200 OK
    Length: 15907988 (15M) [application/x-compressed]
    Saving to: ‘k9s_Linux_x86_64.tar.gz’
    
    100%[=================================================================================>] 15,907,988  3.40MB/s   in 4.4s
    
    2023-01-28 16:39:39 (3.47 MB/s) - ‘k9s_Linux_x86_64.tar.gz’ saved [15907988/15907988]
    
    ```
    

* * *

* * *

* * *

## Squid

1. **安装 Squid**
    
    - ```yaml
        cat > docker-compose.yaml << ERIC
        version: '3.6'
        services:
        
         squid-copy-file:
           container_name: squid-copy-file
           hostname: squid-copy-file
           #image: ubuntu/squid:5.6-22.10_edge
           image: registry.cn-qingdao.aliyuncs.com/cn-aliyun/squid:5.6-22.10_edge
           volumes:
             - /etc/localtime:/etc/localtime
             - ./config/conf.d/:/etc/squid/conf.d/
           entrypoint:
             - /bin/bash
             - -c
             - |
                 test -f /etc/squid/conf.d/snippet.conf || cp /etc/squid/squid.conf /etc/squid/conf.d/snippet.conf
                 sed -i "s/http_access deny all/http_access allow all/g" /etc/squid/conf.d/snippet.conf
        
         squid:
           network_mode: host
           depends_on:
             - squid-copy-file
           container_name: squid
           # 用你实际的公共主机名替换这里
           hostname: your-public-hostname
           restart: always
           image: registry.cn-qingdao.aliyuncs.com/cn-aliyun/squid:5.6-22.10_edge
           environment:
             TZ: Asia/Shanghai
           volumes:
             - /etc/localtime:/etc/localtime
             - ./config/conf.d/snippet.conf:/etc/squid/squid.conf
        
        ERIC
        ```
        
2. **启动 Squid**
    
    - ```shell
        docker-compose up -d
        ```
        

## 测试 Squid

- > 找一台不能访问外网的 CentOS 7 系统，做如下操作
    
- ```shell
    ## 在控制台临时执行，如果希望永久执行，可以把如下配置添加到 /etc/profile
    export PROXY="http://172.16.15.205:3128"
    # http代理
    export http_proxy=$PROXY
    # https代理
    export https_proxy=$PROXY
    # ftp代理
    export ftp_proxy=$PROXY
    # 不代理
    export no_proxy="localhost, 127.0.0.1, ::1"
    ```
    
- ```shell
    wget http://qiniu.dev-share.top/tools/k9s_Linux_x86_64.tar.gz
    ## 测试下载成功
    Connecting to 172.16.15.205:3128... connected.
    Proxy request sent, awaiting response... 200 OK
    Length: 15907988 (15M) [application/x-compressed]
    Saving to: ‘k9s_Linux_x86_64.tar.gz’
    
    100%[=================================================================================>] 15,907,988  3.40MB/s   in 4.4s
    
    2023-01-28 16:39:39 (3.47 MB/s) - ‘k9s_Linux_x86_64.tar.gz’ saved [15907988/15907988]
    
    ```
    

## Squid 配置参数优化（可选）

```shell
cat >> ./config/conf.d/snippet.conf << ERIC
memory_pools off
cache_mem 64 MB
visible_hostname www.dev-share.top
ERIC
```
