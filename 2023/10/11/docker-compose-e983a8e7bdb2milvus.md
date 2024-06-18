---
title: 'docker-compose 部署 Milvus'
date: '2023-10-11T09:03:32+00:00'
status: publish
permalink: /2023/10/11/docker-compose-%e9%83%a8%e7%bd%b2milvus
author: 毛巳煜
excerpt: ''
type: post
id: 10350
category:
    - Milvus
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
### 前置条件

[部署 Milvus GPU版本](https://milvus.io/docs/install_standalone-docker-compose-gpu.md#Install-Milvus-Standalone-with-Docker-Compose "部署 Milvus GPU版本")  
[部署 Milvus CPU版本](https://milvus.io/docs/install_standalone-docker.md#Install-Milvus-Standalone-with-Docker-Compose-CPU "部署 Milvus CPU版本")

### docker-compose.yaml

```yaml
tee docker-compose.yaml 
```