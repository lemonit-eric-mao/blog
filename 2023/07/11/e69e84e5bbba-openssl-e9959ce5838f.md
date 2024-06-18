---
title: '构建 Openssl 镜像'
date: '2023-07-11T02:28:16+00:00'
status: private
permalink: /2023/07/11/%e6%9e%84%e5%bb%ba-openssl-%e9%95%9c%e5%83%8f
author: 毛巳煜
excerpt: ''
type: post
id: 10099
category:
    - Docker
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
构建openssl镜像
===========

### 创建Dockerfile文件

```yaml
cat > Dockerfile 
```

### 构建镜像

```shell
docker build -t cnagent/openssl:1.0.2 .

```

### 测试运行镜像

```shell
docker run --rm -it cnagent/openssl:1.0.2

```

### 登录 docker hub 推送镜像

```shell
docker login docker.io/cnagent

docker push cnagent/openssl:1.0.2

```

- - - - - -

- - - - - -

- - - - - -

基于 cnagent/openssl 构建生成证书镜像
---------------------------

### 编写脚本

```shell
cat > generate-cert.sh 
```

### 创建Dockerfile文件

```yaml
cat > Dockerfile 
```

### 构建镜像

```shell
docker build -t cnagent/generate-cert:1.0.2 .

```

### 测试运行镜像

```shell
docker run --rm -it \
    -e DOMAIN_NAME=test.keycloak.com \
    -e YOUR_PASSWORD=yourpasswd \
    -v ./cert:/cert \
    cnagent/generate-cert:1.0.2

```

### 登录 docker hub 推送镜像

```shell
docker login docker.io/cnagent

docker push cnagent/generate-cert:1.0.2

```