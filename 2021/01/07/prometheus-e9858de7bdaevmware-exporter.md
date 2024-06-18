---
title: 'prometheus 配置vmware-exporter'
date: '2021-01-07T05:16:05+00:00'
status: publish
permalink: /2021/01/07/prometheus-%e9%85%8d%e7%bd%aevmware-exporter
author: 毛巳煜
excerpt: ''
type: post
id: 6749
category:
    - prometheus
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### 创建工作目录

```ruby
mkdir -p /home/deploy/monitor/
mkdir -p /home/deploy/monitor/prometheus/config
mkdir -p /home/deploy/monitor/prometheus/data
mkdir -p /home/deploy/vmware_exporter

```

- - - - - -

###### docker-compose 安装部署 Prometheus

```ruby
cat > /home/deploy/monitor/docker-compose.yaml 
```

- - - - - -

###### Prometheus 配置文件，添加配置

```yaml
cat > /home/deploy/monitor/prometheus/config/prometheus.yml 
```

- - - - - -

- - - - - -

- - - - - -

###### **[安装 vmware-exporter](https://gitee.com/eric-mao/cn-vmware "安装 vmware-exporter")**

```yaml
cat > /home/deploy/vmware_exporter/docker-compose.yaml 
```

- - - - - -

- - - - - -

- - - - - -