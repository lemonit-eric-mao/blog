---
title: 'CentOS 7 磁盘挂载'
date: '2019-12-05T07:09:26+00:00'
status: private
permalink: /2019/12/05/centos-7-%e7%a3%81%e7%9b%98%e6%8c%82%e8%bd%bd
author: 毛巳煜
excerpt: ''
type: post
id: 5181
category:
    - CentOS
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
### mount\_disk.sh

> 关键字：磁盘、硬盘、挂载

```bash
#!/bin/bash

disk=""
dir=""

# 使用getopts解析参数
while getopts "d:i:" opt; do
  case <span class="katex math inline">opt in
    d)
      disk="</span>OPTARG"
      ;;
    i)
      dir="<span class="katex math inline">OPTARG"
      ;;
    \?)
      echo "无效选项: -</span>OPTARG" >&2
      exit 1
      ;;
  esac
done

# 检查参数是否为空
if [ -z "<span class="katex math inline">disk" ] || [ -z "</span>dir" ]; then
    echo "请提供磁盘设备名称和挂载目录作为参数。"
    echo "示例: <span class="katex math inline">0 -d /dev/sdb -i /data"
    exit 1
fi

# 检查挂载目录是否存在，如果不存在则创建
if [ ! -d "</span>dir" ]; then
    sudo mkdir -p "<span class="katex math inline">dir"
fi

# 检查磁盘是否已经挂载
if mountpoint -q "</span>dir"; then
    echo "磁盘已经挂载到 <span class="katex math inline">dir 目录。"
    exit 0
fi

# 分区、格式化磁盘
sudo parted</span>disk mklabel gpt
sudo parted <span class="katex math inline">disk mkpart primary ext4 0% 100%

# 格式化分区
sudo mkfs.ext4 -F "</span>disk"1

# 挂载磁盘到目标目录
sudo mount "<span class="katex math inline">disk"1 "</span>dir"

# 更新 /etc/fstab 以便启动时自动挂载
echo "<span class="katex math inline">disk"1 "</span>dir" ext4 defaults 0 0 | sudo tee -a /etc/fstab

echo "磁盘已成功挂载到 $dir 目录。"


```

**使用**

```bash
sh mount_disk.sh -d /dev/sdb -i /data

```