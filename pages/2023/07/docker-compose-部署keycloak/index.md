---
title: "docker-compose 部署 keycloak"
date: "2023-07-11"
categories: 
  - "linux服务器"
---

## 生产模式：docker-compose 部署keycloak

```yaml
cat > docker-compose.yaml << ERIC

version: '3.6'

# 定义全局字符串
x-str:
  &domain
  "test.keycloak.com"

x-str-timezone:
  &timezone
  "Asia/Shanghai"

services:

  # 自动生成证书
  generate-cert:
    container_name: generate-cert
    image: cnagent/generate-cert:1.0.2
    volumes:
      - ./config/cert:/cert
    # 环境变量
    environment:
      TIME_ZONE: *timezone
      DOMAIN_NAME: *domain
      YOUR_PASSWORD: yourpasswd

  # 复制文件
  copy-file:
    depends_on:
      - generate-cert
    privileged: true
    user: root
    container_name: copy-file
    image: mariadb:10.6.0
    volumes:
      - ./config/mariadb-config:/file
    # 判断文件不存在时，在执行
    entrypoint: /bin/bash -c "test -f /file/50-server.cnf || cp /etc/mysql/mariadb.conf.d/50-server.cnf /file/50-server.cnf"

  # 数据库
  mariadb:
    depends_on:
      - copy-file
    image: mariadb:10.6.0
    restart: always
    container_name: mariadb
    ports:
      # 端口映射
      - 3306:3306
    volumes:
      # 容器与宿主机时间同步
      - /etc/localtime:/etc/localtime
      # 数据库目录映射
      - ./config/mariadb:/var/lib/mysql
      # 数据库配置文件映射
      - ./config/mariadb-config/:/etc/mysql/conf.d/
    environment:
      TIME_ZONE: *timezone
      MYSQL_ROOT_PASSWORD: your-passwd
      MYSQL_DATABASE: keycloak


  # keycloak容器
  keycloak:
    depends_on:
      - mariadb
    image: quay.io/keycloak/keycloak:22.0.0
    restart: always
    container_name: keycloak
    environment:
      TIME_ZONE: *timezone
      # 设置管理员账号密码
      KEYCLOAK_ADMIN: admin
      KEYCLOAK_ADMIN_PASSWORD: admin
      # 配置域名
      KC_HOSTNAME: *domain
      # 配置HTTPS，禁用http
      KC_HTTP_ENABLED: 'false'
      KC_HTTPS_PORT: 443                                     # 默认 8443
      KC_HTTPS_CERTIFICATE_FILE: /cert/tls.crt               # 证书名默认采用你的域名
      KC_HTTPS_CERTIFICATE_KEY_FILE: /cert/tls.key
      # 数据库配置
      KC_DB: mariadb
      KC_DB_USERNAME: root
      KC_DB_PASSWORD: your-passwd
      KC_DB_URL: jdbc:mariadb://mariadb:3306/keycloak
      quarkus.transaction-manager.enable-recovery: "true"    # 可选
    ports:
      - 443:443
      - 80:80
    volumes:
      - ./config/cert:/cert
      - ./config/keycloak/conf/quarkus.properties:/opt/keycloak/conf/quarkus.properties
      - ./config/keycloak/themes:/opt/keycloak/themes
      # 容器与宿主机时间同步
      - /etc/localtime:/etc/localtime
    command: start

ERIC

```

* * *

* * *

* * *

## 测试模式：docker-compose 部署keycloak

```yaml
cat > docker-compose.yaml << ERIC

version: '3.6'

# 定义全局字符串
x-str:
  &domain
  "test.keycloak.com"

x-str-timezone:
  &timezone
  "Asia/Shanghai"

services:

  # 自动生成证书
  generate-cert:
    container_name: generate-cert
    image: cnagent/generate-cert:1.0.2
    volumes:
      - ./config/cert:/cert
    # 环境变量
    environment:
      TIME_ZONE: *timezone
      DOMAIN_NAME: *domain
      YOUR_PASSWORD: yourpasswd

  # 复制文件
  copy-file:
    depends_on:
      - generate-cert
    privileged: true
    user: root
    container_name: copy-file
    image: mariadb:10.6.0
    volumes:
      - ./config/mariadb-config:/file
    # 判断文件不存在时，在执行
    entrypoint: /bin/bash -c "test -f /file/50-server.cnf || cp /etc/mysql/mariadb.conf.d/50-server.cnf /file/50-server.cnf"

  # 数据库
  mariadb:
    depends_on:
      - copy-file
    image: mariadb:10.6.0
    restart: always
    container_name: mariadb
    ports:
      # 端口映射
      - 3306:3306
    volumes:
      # 容器与宿主机时间同步
      - /etc/localtime:/etc/localtime
      # 数据库目录映射
      - ./config/mariadb:/var/lib/mysql
      # 数据库配置文件映射
      - ./config/mariadb-config/:/etc/mysql/conf.d/
    environment:
      TIME_ZONE: *timezone
      MYSQL_ROOT_PASSWORD: your-passwd
      MYSQL_DATABASE: keycloak


  # keycloak容器
  keycloak:
    depends_on:
      - mariadb
    image: quay.io/keycloak/keycloak:22.0.0
    restart: always
    container_name: keycloak
    environment:
      TIME_ZONE: *timezone
      # 设置管理员账号密码
      KEYCLOAK_ADMIN: admin
      KEYCLOAK_ADMIN_PASSWORD: admin
      # 配置HTTP，启用http
      KC_HTTPS_PORT: 80                                      # 默认 8080
      # 数据库配置
      KC_DB: mariadb
      KC_DB_USERNAME: root
      KC_DB_PASSWORD: your-passwd
      KC_DB_URL: jdbc:mariadb://mariadb:3306/keycloak
    ports:
      - 80:80
    volumes:
      - ./config/cert:/cert
      - ./config/keycloak/conf/quarkus.properties:/opt/keycloak/conf/quarkus.properties
      - ./config/keycloak/themes:/opt/keycloak/themes
      # 容器与宿主机时间同步
      - /etc/localtime:/etc/localtime
    command: start-dev

ERIC

```
