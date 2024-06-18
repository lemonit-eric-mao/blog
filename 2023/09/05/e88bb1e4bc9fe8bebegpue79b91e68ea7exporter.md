---
title: 英伟达GPU监控Exporter
date: '2023-09-05T04:23:42+00:00'
status: private
permalink: /2023/09/05/%e8%8b%b1%e4%bc%9f%e8%be%begpu%e7%9b%91%e6%8e%a7exporter
author: 毛巳煜
excerpt: ''
type: post
id: 10263
category:
    - prometheus
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
### 创建目录

```bash
mkdir -m 755 -p ./prometheus/config

```

### prometheus.yml

```yaml
cat > ./prometheus/config/prometheus.yml 
```

### 热更新

> curl -X POST 10.10.0.5:9090/-/reload

- - - - - -

### docker-compose

```yaml
cat > docker-compose.yaml 
```

### 引入grafana面板：

Node Dashboard Id: 9894  
GPU Dashboard Id: 14574