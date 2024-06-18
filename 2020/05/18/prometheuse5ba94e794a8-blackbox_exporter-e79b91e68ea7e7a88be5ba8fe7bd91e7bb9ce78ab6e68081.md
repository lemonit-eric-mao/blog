---
title: 'Prometheus应用 blackbox_exporter 监控程序网络状态'
date: '2020-05-18T07:05:55+00:00'
status: publish
permalink: /2020/05/18/prometheus%e5%ba%94%e7%94%a8-blackbox_exporter-%e7%9b%91%e6%8e%a7%e7%a8%8b%e5%ba%8f%e7%bd%91%e7%bb%9c%e7%8a%b6%e6%80%81
author: 毛巳煜
excerpt: ''
type: post
id: 5334
category:
    - Linux服务器
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### [官网地址](https://prometheus.io/download/#blackbox_exporter "官网地址")

###### [gitlab](https://github.com/prometheus/blackbox_exporter "gitlab")

###### [安装 docker-compose](http://www.dev-share.top/2019/06/12/%E5%AE%89%E8%A3%85-docker-compose/ "安装 docker-compose")

- - - - - -

##### 前置条件

**IP**: 192.168.180.32  
**OS**: CentOS 7

- - - - - -

##### 创建文件夹

```ruby
mkdir -p /home/monitor/blackbox/config

```

- - - - - -

##### 创建配置文件

```ruby
cat > /home/monitor/blackbox/config/blackbox.yml 
```

- - - - - -

##### 创建 compose 文件

```ruby
cat > /home/monitor/blackbox/docker-compose.yml 
```

- - - - - -

- - - - - -

- - - - - -

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

</name></port></host>
```

- - - - - -

##### 验证普罗米修斯，访问如下地址，确认是否有返回信息

http://192.168.180.32:9090/graph?g0.range\_input=1h&amp;g0.expr=probe\_success&amp;g0.tab=1

- - - - - -