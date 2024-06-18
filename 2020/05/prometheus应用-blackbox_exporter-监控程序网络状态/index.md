---
title: "Prometheus应用 blackbox_exporter 监控程序网络状态"
date: "2020-05-18"
categories: 
  - "linux服务器"
---

###### [官网地址](https://prometheus.io/download/#blackbox_exporter "官网地址")

###### [gitlab](https://github.com/prometheus/blackbox_exporter "gitlab")

###### [安装 docker-compose](http://www.dev-share.top/2019/06/12/%E5%AE%89%E8%A3%85-docker-compose/ "安装 docker-compose")

* * *

##### 前置条件

**IP**: 192.168.180.32 **OS**: CentOS 7

* * *

##### 创建文件夹

```ruby
mkdir -p /home/monitor/blackbox/config
```

* * *

##### 创建配置文件

```ruby
cat > /home/monitor/blackbox/config/blackbox.yml << ERIC
modules:
  # http 监测模块(告诉blackbox要监控 http 协议)
  http_2xx:
    prober: http

#  # http post 监测模块
#  http_post_2xx:
#    prober: http
#    http:
#      method: POST
#
#  # tcp 监测模块
#  tcp_connect:
#    prober: tcp


#  pop3s_banner:
#    prober: tcp
#    tcp:
#      query_response:
#      - expect: "^+OK"
#      tls: true
#      tls_config:
#        insecure_skip_verify: false


#  ssh_banner:
#    prober: tcp
#    tcp:
#      query_response:
#      - expect: "^SSH-2.0-"


#  irc_banner:
#    prober: tcp
#    tcp:
#      query_response:
#      - send: "NICK prober"
#      - send: "USER prober prober prober :prober"
#      - expect: "PING :([^ ]+)"
#        send: "PONG \${1}"
#      - expect: "^:[^ ]+ 001"

#  # icmp 检测模块
#  icmp:
#    prober: icmp

ERIC

```

* * *

##### 创建 compose 文件

```ruby
cat > /home/monitor/blackbox/docker-compose.yml << ERIC
version: '3.1'
services:

  blackbox-exporter:
    container_name: blackbox-exporter
    image: prom/blackbox-exporter:v0.16.0
    ports:
      - 9115:9115
    restart: always
    volumes:
      # 将本地配置文件目录，映射到容器中的 /config 目录
      - ./config:/config
    # 重新指定容器中的配置文件，默认在 /etc/blackbox_exporter/config.yml
    command:
      - '--config.file=/config/blackbox.yml'

ERIC

```

* * *

* * *

* * *

##### 将blackbox模块添加到普罗米修斯中，在普罗米修斯配置文件中，添加关联

```yml
scrape_configs:

  - job_name: '博客-blackbox'
    metrics_path: /probe
    # 监听 response
    params:
      # 监听响应的状态码
      module: [http_2xx]  # Look for a HTTP 200 response.    对应 blackbox.yml 中的模块

    # 配置要监听的url
    static_configs:
      - targets:
        - http://baidu.com    # http
        - https://baidu.com   # https
        #- http://example.com:8080
        - http://www.dev-share.top

    relabel_configs:
      # __address__：当前Target实例的访问地址<host>:<port>
      # __scheme__：采集目标服务访问地址的HTTP Scheme，HTTP或者HTTPS
      # __metrics_path__：采集目标服务访问地址的访问路径
      # __param_<name>：采集任务目标服务的中包含的请求参数
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        # 指定 blackbox 服务模块的访问地址
        replacement: 192.168.180.32:9115  # The blackbox exporter's real hostname:port.

  - job_name: '七牛云-blackbox'
    metrics_path: /probe
    params:
      module: [http_2xx]
    static_configs:
      - targets:
        - http://qiniu.dev-share.top
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: 192.168.180.32:9115

```

* * *

##### 验证普罗米修斯，访问如下地址，确认是否有返回信息

http://192.168.180.32:9090/graph?g0.range\_input=1h&g0.expr=probe\_success&g0.tab=1

* * *
