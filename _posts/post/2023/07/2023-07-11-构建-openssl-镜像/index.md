---
title: "构建 Openssl 镜像"
date: "2023-07-11"
categories: 
  - "docker"
---

# 构建openssl镜像

### 创建Dockerfile文件

```yaml
cat > Dockerfile << ERIC

# 使用Alpine作为基础镜像
# alpine:3.15    openssl版本为 1.1.1u-r1
# alpine:3.18.2  openssl版本为 3.1.1-r1
# alpine:3.5     openssl版本为 1.0.2q
FROM alpine:3.5

# 安装OpenSSL
RUN apk --no-cache add openssl

# 设置工作目录
WORKDIR /app

# 声明镜像的启动命令或入口点
#CMD ["openssl"]

ERIC

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

* * *

* * *

* * *

## 基于 cnagent/openssl 构建生成证书镜像

### 编写脚本

```shell
cat > generate-cert.sh << ERIC

#!/bin/bash -e

# 主域名
#DOMAIN_NAME="test.keycloak.com"

# 存储证书的目录
CERT_DIR="./cert"

# 证书名称
CERT_NAME="tls"

# 用于加密私钥的密码
#YOUR_PASSWORD="yourpasswd"

# 创建存储证书的目录（如果不存在）
mkdir -p \$CERT_DIR

# 生成私钥文件
openssl genrsa -out "\$CERT_DIR/\$CERT_NAME.key" 4096

# 生成证书签发请求 (CSR)
openssl req -new -subj "/CN=\$DOMAIN_NAME" -key "\$CERT_DIR/\$CERT_NAME.key" -out "\$CERT_DIR/\$CERT_NAME.csr"

# 生成自签名证书
openssl x509 -req -days 365 -signkey "\$CERT_DIR/\$CERT_NAME.key" -in "\$CERT_DIR/\$CERT_NAME.csr" -out "\$CERT_DIR/\$CERT_NAME.crt"

# 生成一个包含私钥和证书的PFX（也是P12）文件，并设置密码
openssl pkcs12 -export -inkey "\$CERT_DIR/\$CERT_NAME.key" -in "\$CERT_DIR/\$CERT_NAME.crt" -out "\$CERT_DIR/\$CERT_NAME.p12" -passout pass:\$YOUR_PASSWORD

# 输出成功信息
echo "自签名证书已创建完毕：\$CERT_DIR/\$CERT_NAME.crt"

ERIC

```

### 创建Dockerfile文件

```yaml
cat > Dockerfile << ERIC

# 使用Alpine作为基础镜像
FROM cnagent/openssl:1.0.2

# 设置工作目录
WORKDIR /

# 安装OpenSSL
COPY generate-cert.sh /

# 声明镜像的启动命令或入口点
CMD ["sh", "generate-cert.sh"]

ERIC

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
