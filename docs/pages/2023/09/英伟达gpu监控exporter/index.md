---
title: "英伟达GPU监控Exporter"
date: "2023-09-05"
categories: 
  - "prometheus"
---

### 创建目录

```bash
mkdir -m 755 -p ./prometheus/config
```

### prometheus.yml

```yaml
cat > ./prometheus/config/prometheus.yml << ERIC
# 全局配置文件
global:
  # 默认设置为15秒的抓取间隔
  scrape_interval: 15s
  external_labels:
    monitor: 'line-monitor'

scrape_configs:
  - job_name: 'prometheus'
    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.
    static_configs:
      - targets: ['10.10.0.5:9090']

  # 节点监控
  - job_name: 'node-exporter'
    # 为Node Exporter设置20秒的抓取间隔
    scrape_interval: 20s
    static_configs:
      - targets: ['10.10.0.5:9100']

  # GPU监控
  - job_name: 'nvidia-gpu'
    # 为NVIDIA GPU Exporter设置3秒的抓取间隔
    scrape_interval: 3s
    static_configs:
      - targets: ['10.10.0.4:9835', '10.10.0.5:9835']
        labels:
          # 自定义标签
          tenant: 'tenant_01'

      - targets: ['10.10.0.2:9835']
        labels:
          # 自定义标签
          tenant: 'tenant_02'

ERIC

```

### 热更新

> curl -X POST 10.10.0.5:9090/-/reload

* * *

### docker-compose

```yaml
cat > docker-compose.yaml << ERIC
version: '3.6'
services:

  # 添加 普罗米修斯服务
  prometheus:
    image: prom/prometheus:v2.46.0
    container_name: prometheus
    hostname: prometheus
    restart: always
    privileged: true
    user: root
    ports:
      - 9090:9090
    volumes:
      - ./prometheus/config:/config
      - ./prometheus/data/prometheus:/prometheus/data
      # 容器与宿主机时间同步
      - /etc/localtime:/etc/localtime
    command:
      - '--config.file=/config/prometheus.yml'
      # 支持热更新
      - '--web.enable-lifecycle'

  # 添加监控可视化面板
  grafana:
    image: grafana/grafana:10.1.1
    container_name: grafana
    hostname: grafana
    restart: always
    privileged: true
    user: root
    ports:
      - 3000:3000
    volumes:
      - /etc/localtime:/etc/localtime
      - ./grafana/data:/var/lib/grafana

  # 虚拟机节点监控
  node_exporter:
    image: prom/node-exporter:v1.6.1
    container_name: node_exporter
    hostname: node_exporter
    volumes:
      # 容器与宿主机时间同步
      - /etc/localtime:/etc/localtime
    ports:
      - 9100:9100

  # 英伟达GPU监控
  nvidia_smi_exporter:
    image: utkuozdemir/nvidia_gpu_exporter:1.1.0
    container_name: nvidia_smi_exporter
    restart: unless-stopped
    devices:
      - /dev/nvidiactl:/dev/nvidiactl
      # 注意，你的主机中有几个nvidia*，这里就要配置几个
      - /dev/nvidia0:/dev/nvidia0
      - /dev/nvidia1:/dev/nvidia1
    volumes:
      - /usr/lib/x86_64-linux-gnu/libnvidia-ml.so:/usr/lib/x86_64-linux-gnu/libnvidia-ml.so
      - /usr/lib/x86_64-linux-gnu/libnvidia-ml.so.1:/usr/lib/x86_64-linux-gnu/libnvidia-ml.so.1
      - /usr/bin/nvidia-smi:/usr/bin/nvidia-smi
      # 容器与宿主机时间同步
      - /etc/localtime:/etc/localtime
    ports:
      - 9835:9835

ERIC

```

### 引入grafana面板：

Node Dashboard Id: 9894 GPU Dashboard Id: 14574
