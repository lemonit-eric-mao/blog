---
title: "OpenEuler 系统环境安装部署指南"
date: "2026-02-06"
categories: 
  - "linux"
---


# OpenEuler 系统环境安装部署指南

本指南适用于 **openEuler 22.03 LTS SP4 (aarch64)** 环境，包含：

- Docker 二进制安装（29.1.3）
- 数据目录迁移到 `/data/docker-data`
- Docker Compose v5.0.0 安装

---

## 1. 系统信息确认

```bash
uname -a
```

示例输出：

```
Linux localhost.localdomain 5.10.0-216.0.0.115.oe2203sp4.aarch64 #1 SMP Thu Jun 27 15:22:10 CST 2024 aarch64 aarch64 aarch64 GNU/Linux
```

---

## 2. 配置 DNF 源（如有需要）

```bash
dnf clean all
dnf makecache
```

若提示 DNS 无法解析，请检查：

```bash
cat /etc/resolv.conf
ping 8.8.8.8
ping repo.openeuler.org
```

---

## 3. Docker 29.1.3 二进制安装

### 3.1 上传 Docker 安装包

将文件上传至服务器，例如：

```
https://download.docker.com/linux/static/stable/aarch64/docker-29.1.3.tgz

docker-29.1.3.tgz
```

---

### 3.2 安装脚本

创建脚本：

```bash
vim install-docker.sh
```

内容如下：

```bash
#!/bin/bash

TGZ="docker-29.1.3.tgz"
DATA_DIR="/data/docker-data"

echo "======================================"
echo " Docker 29.1.3 安装(openEuler ARM64)"
echo " 数据目录: $DATA_DIR"
echo "======================================"

# 检查安装包
if [ ! -f "$TGZ" ]; then
    echo "❌ 找不到 $TGZ"
    exit 1
fi

# 安装依赖（不启动 containerd）
echo "==> 安装依赖..."
dnf install -y iptables tar

# 创建数据目录 + 软链接
echo "==> 创建 Docker 数据目录..."
mkdir -p $DATA_DIR
mkdir -p /var/lib
rm -rf /var/lib/docker
ln -s $DATA_DIR /var/lib/docker

# 解压 Docker
echo "==> 解压 Docker..."
rm -rf docker
tar -xvf $TGZ

# 安装二进制
echo "==> 安装 Docker 到 /usr/bin ..."
cp -f docker/* /usr/bin/

# 创建 systemd 服务
echo "==> 写入 systemd 服务..."
cat > /etc/systemd/system/docker.service <<'SERVICE'
[Unit]
Description=Docker Engine
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/bin/dockerd
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
SERVICE

# 启动 Docker
echo "==> 启动 Docker..."
systemctl daemon-reload
systemctl enable --now docker

echo "======================================"
echo "🎉 Docker 安装完成!"
docker -v
echo "数据目录软链接："
ls -l /var/lib/docker
echo "======================================"

```

执行：

```bash
chmod +x install-docker.sh
./install-docker.sh
```

---

## 4. Docker Compose v5.0.0 安装

### 4.1 一键安装脚本

下载包

```bash
COMPOSE_VERSION="v5.0.0"
https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-linux-aarch64
```

创建脚本：

```bash
vim install-compose.sh
```

install-compose.sh（离线版）

```bash
#!/bin/bash
set -e

COMPOSE_BIN="./docker-compose-linux-aarch64"

echo "==> 检查本地文件..."

if [ ! -f "$COMPOSE_BIN" ]; then
    echo "❌ 找不到文件: $COMPOSE_BIN"
    echo "请确认 docker-compose-linux-aarch64 已上传到当前目录"
    exit 1
fi

echo "==> 安装 Docker Compose 到 /usr/local/bin ..."

cp $COMPOSE_BIN /usr/local/bin/docker-compose

echo "==> 赋予执行权限..."
chmod +x /usr/local/bin/docker-compose

echo "==> 创建软链接到 /usr/bin ..."
ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose

echo "==> 验证安装..."
docker-compose version

echo "======================================"
echo "🎉 Docker Compose 离线安装完成!"
echo "路径: $(which docker-compose)"
echo "版本: $(docker-compose version)"
echo "======================================"

```

执行：

```bash
chmod +x install-compose.sh
./install-compose.sh
```

---

## 5. 验证最终效果

```bash
docker -v
docker-compose version
docker info | grep "Docker Root Dir"
```

输出应类似：

```
Docker version 29.1.3
Docker Compose version v5.0.0
Docker Root Dir: /var/lib/docker -> /data/docker-data
```

---

# 🎉 部署完成

至此，openEuler ARM64 环境下：

- Docker Engine 29.1.3 已安装
- 镜像与容器数据全部存储在 `/data/docker-data`
- Docker Compose v5.0.0 已安装

---

---

---

# 安装uv

> 下载地址：https://github.com/astral-sh/uv/releases/tag/0.11.7

下载包

``` bash
wget https://releases.astral.sh/github/uv/releases/download/0.11.7/uv-aarch64-unknown-linux-gnu.tar.gz
```

创建脚本：

```bash
vim install-uv.sh
```

install-uv.sh（离线版）

``` bash
#!/bin/bash
set -e

UV_ARCHIVE="./uv-aarch64-unknown-linux-gnu.tar.gz"
UV_DIR="./uv-aarch64-unknown-linux-gnu"

echo "==> 检查本地文件..."
if [ ! -f "$UV_ARCHIVE" ]; then
    echo "❌ 找不到文件: $UV_ARCHIVE"
    exit 1
fi

echo "==> 解压 uv..."
tar -xzf "$UV_ARCHIVE"

if [ ! -d "$UV_DIR" ]; then
    echo "❌ 解压后未找到目录: $UV_DIR"
    exit 1
fi

UV_EXEC="$UV_DIR/uv"
if [ ! -f "$UV_EXEC" ]; then
    echo "❌ 解压后未找到 uv 可执行文件!"
    exit 1
fi

echo "==> 安装 uv 到 /usr/local/bin ..."
sudo cp "$UV_EXEC" /usr/local/bin/uv

echo "==> 赋予执行权限..."
sudo chmod +x /usr/local/bin/uv

echo "==> 创建软链接到 /usr/bin ..."
sudo ln -sf /usr/local/bin/uv /usr/bin/uv

echo "==> 刷新环境变量..."
hash -r

echo "==> 验证安装..."
uv --version

echo "======================================"
echo "🎉 uv 离线安装完成!"
echo "路径: $(which uv)"
echo "版本: $(uv --version)"
echo "======================================"
```

执行：

```bash
chmod +x install-uv.sh
./install-uv.sh
```

效果
``` bash
======================================
 uv 离线安装完成!
路径: /usr/local/bin/uv
版本: uv 0.11.7 (aarch64-unknown-linux-gnu)
======================================
```
