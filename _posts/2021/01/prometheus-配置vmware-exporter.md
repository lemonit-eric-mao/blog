---
title: "prometheus 配置vmware-exporter"
date: "2021-01-07"
categories: 
  - "prometheus"
---

###### 创建工作目录

```ruby
mkdir -p /home/deploy/monitor/
mkdir -p /home/deploy/monitor/prometheus/config
mkdir -p /home/deploy/monitor/prometheus/data
mkdir -p /home/deploy/vmware_exporter
```

* * *

###### docker-compose 安装部署 Prometheus

```ruby
cat > /home/deploy/monitor/docker-compose.yaml << ERIC
# 指定 docker-compose 编译版本，这个很重要
version: '3.1'
services:
  # 添加 普罗米修斯服务
  prometheus:
    # Docker Hub 镜像
    image: prom/prometheus:latest
    # 容器名称
    container_name: prometheus
    # 容器内部 hostname
    hostname: prometheus
    # 容器支持自启动
    restart: always
    # 容器与宿主机 端口映射
    ports:
      - '9090:9090'
    # 将宿主机中的config文件夹，挂载到容器中/config文件夹
    volumes:
      - './prometheus/config:/config'
      - './prometheus/data:/prometheus/data'
    # 指定容器中的配置文件
    command:
      - '--config.file=/config/prometheus.yml'
      # 支持热更新
      - '--web.enable-lifecycle'

ERIC

```

* * *

###### Prometheus 配置文件，添加配置

```yaml
cat > /home/deploy/monitor/prometheus/config/prometheus.yml << ERIC
# 全局配置文件（可替换）
global:
  # 指定Prometheus抓取应用程序数据的间隔为15秒。
  scrape_interval:     15s

  # 配置项external_labels是用于外部系统标签的，不是用于metrics数据。
  # 当使用thanos作为prometheus集群时，external_labels是必填项。
  external_labels:
    monitor: 'line-monitor'

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:

  - job_name: 'vmware_vcenter'
    metrics_path: '/metrics'
    static_configs:
      - targets:
        - 'vcenter'
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        # vmware_exporter 服务地址，注意不要使用 localhost，因为它指向的是容器中的网络
        replacement: 192.168.20.94:9272

ERIC

```

* * *

* * *

* * *

###### **[安装 vmware-exporter](https://gitee.com/eric-mao/cn-vmware "安装 vmware-exporter")**

```yaml
cat > /home/deploy/vmware_exporter/docker-compose.yaml << ERIC
version: '3.1'
services:
  vmware_exporter:
    image: cn-vmware-exporter:v0.0.1
    container_name: cn-vmware-exporter
    ports:
      - 9293:9293
    environment:
      # VMware vSphere  https协议的IP地址
      VSPHERE_HOST: '127.0.0.1'
      VSPHERE_PORT: '443'
      VSPHERE_USER: 'username'
      VSPHERE_PASSWORD: 'passwd'
    restart: always

ERIC

```

* * *

* * *

* * *
