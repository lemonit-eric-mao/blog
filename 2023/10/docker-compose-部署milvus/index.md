---
title: "docker-compose 部署 Milvus"
date: "2023-10-11"
categories: 
  - "milvus"
---

### 前置条件

[部署 Milvus GPU版本](https://milvus.io/docs/install_standalone-docker-compose-gpu.md#Install-Milvus-Standalone-with-Docker-Compose "部署 Milvus GPU版本") [部署 Milvus CPU版本](https://milvus.io/docs/install_standalone-docker.md#Install-Milvus-Standalone-with-Docker-Compose-CPU "部署 Milvus CPU版本")

### docker-compose.yaml

```yaml
tee docker-compose.yaml << ERIC

version: '3.6'

services:
  etcd:
    container_name: milvus-etcd
    image: quay.io/coreos/etcd:v3.5.5
    restart: always
    environment:
      - ETCD_AUTO_COMPACTION_MODE=revision
      - ETCD_AUTO_COMPACTION_RETENTION=1000
      - ETCD_QUOTA_BACKEND_BYTES=4294967296
      - ETCD_SNAPSHOT_COUNT=50000
    volumes:
      - ./volumes/etcd:/etcd
    command: etcd -advertise-client-urls=http://127.0.0.1:2379 -listen-client-urls http://0.0.0.0:2379 --data-dir /etcd
    healthcheck:
      test: ["CMD", "etcdctl", "endpoint", "health"]
      interval: 30s
      timeout: 20s
      retries: 3

  minio:
    container_name: milvus-minio
    image: minio/minio:RELEASE.2023-03-20T20-16-18Z
    restart: always
    environment:
      MINIO_ACCESS_KEY: minioadmin
      MINIO_SECRET_KEY: minioadmin
    ports:
      - "9001:9001"
      - "9000:9000"
    volumes:
      - ./volumes/minio:/minio_data
    command: minio server /minio_data --console-address ":9001"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3

  milvusdb:
    container_name: milvus-standalone
    image: milvusdb/milvus:v2.3.0
    restart: always
    command: ["milvus", "run", "standalone"]
    environment:
      ETCD_ENDPOINTS: etcd:2379
      MINIO_ADDRESS: minio:9000
    volumes:
      - ./volumes/milvus:/var/lib/milvus
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9091/healthz"]
      interval: 30s
      start_period: 90s
      timeout: 20s
      retries: 3
    ports:
      - "19530:19530"
      - "9091:9091"
    depends_on:
      - "etcd"
      - "minio"

  attu:
    container_name: attu
    image: zilliz/attu:v2.3.1
    restart: always
    ports:
      - "8000:3000"
    depends_on:
      - "milvusdb"
    environment:
      MILVUS_URL: milvusdb:19530

networks:
  default:
    name: milvus

ERIC

```
