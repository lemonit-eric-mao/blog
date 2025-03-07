---
title: "Xinference-部署脚本"
date: "2025-01-08"
categories: 
  - "Xinference"
---





### 安装环境

``` bash
conda create -n xinference python==3.10

conda activate xinference

pip install "xinference[transformers]" -i https://pypi.tuna.tsinghua.edu.cn/simple

```



#### start_inference.sh

``` bash
#!/bin/bash

# 启用错误检查，任何命令失败都终止脚本
set -e

# 定义 IP 地址变量
IP="172.17.0.204"
PORT="9997"

# 启动 supervisor 并将输出重定向到 log 文件
nohup xinference-supervisor -H "$IP" -p "$PORT" > xinference-supervisor.log 2>&1 &

# 等待 supervisor 启动并且监听端口 9997
echo "Waiting for supervisor to start..."
while ! nc -z "$IP" "$PORT"; do
  sleep 1
done

# 一旦 supervisor 启动成功，启动 worker
echo "Supervisor started successfully. Starting worker..."
nohup xinference-worker -e "http://$IP:$PORT" -H "$IP" > xinference-worker01.log 2>&1 &

```



#### stop_inference.sh

``` bash
#!/bin/bash

# 查找并停止 supervisor 进程
echo "Stopping supervisor..."
supervisor_pid=$(ps aux | grep 'xinference-supervisor' | grep -v 'grep' | awk '{print $2}')
if [ -n "$supervisor_pid" ]; then
  kill -9 $supervisor_pid
  echo "Supervisor stopped."
else
  echo "Supervisor is not running."
fi

# 查找并停止 worker 进程
echo "Stopping worker..."
worker_pid=$(ps aux | grep 'xinference-worker' | grep -v 'grep' | awk '{print $2}')
if [ -n "$worker_pid" ]; then
  kill -9 $worker_pid
  echo "Worker stopped."
else
  echo "Worker is not running."
fi

```

