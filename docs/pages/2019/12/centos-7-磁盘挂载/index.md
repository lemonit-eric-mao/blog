---
title: "CentOS 7 磁盘挂载"
date: "2019-12-05"
categories: 
  - "centos"
---

### mount\_disk.sh

> 关键字：磁盘、硬盘、挂载

```bash
#!/bin/bash

disk=""
dir=""

# 使用getopts解析参数
while getopts "d:i:" opt; do
  case $opt in
    d)
      disk="$OPTARG"
      ;;
    i)
      dir="$OPTARG"
      ;;
    \?)
      echo "无效选项: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

# 检查参数是否为空
if [ -z "$disk" ] || [ -z "$dir" ]; then
    echo "请提供磁盘设备名称和挂载目录作为参数。"
    echo "示例: $0 -d /dev/sdb -i /data"
    exit 1
fi

# 检查挂载目录是否存在，如果不存在则创建
if [ ! -d "$dir" ]; then
    sudo mkdir -p "$dir"
fi

# 检查磁盘是否已经挂载
if mountpoint -q "$dir"; then
    echo "磁盘已经挂载到 $dir 目录。"
    exit 0
fi

# 分区、格式化磁盘
sudo parted $disk mklabel gpt
sudo parted $disk mkpart primary ext4 0% 100%

# 格式化分区
sudo mkfs.ext4 -F "$disk"1

# 挂载磁盘到目标目录
sudo mount "$disk"1 "$dir"

# 更新 /etc/fstab 以便启动时自动挂载
echo "$disk"1 "$dir" ext4 defaults 0 0 | sudo tee -a /etc/fstab

echo "磁盘已成功挂载到 $dir 目录。"

```

**使用**

```bash
sh mount_disk.sh -d /dev/sdb -i /data
```
