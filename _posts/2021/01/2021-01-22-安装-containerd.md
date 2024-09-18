---
title: "安装 containerd"
date: "2021-01-22"
categories: 
  - "containerd"
---

###### 安装 containerd

```ruby
# 指定Containerd版本
export CONTAINERD_VERSION=1.6.4
```

```ruby
# 安装 containerd
# 参考文档如下
# https://kubernetes.io/docs/setup/production-environment/container-runtimes/#containerd

cat > /etc/modules-load.d/containerd.conf << ERIC
overlay
br_netfilter
ERIC

sudo modprobe overlay
sudo modprobe br_netfilter

# 设置必需的 sysctl 参数，这些参数在重新启动后仍然存在。
cat > /etc/sysctl.d/99-kubernetes-cri.conf << ERIC
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.bridge.bridge-nf-call-ip6tables = 1
ERIC

# 应用 sysctl 参数而无需重新启动
sudo sysctl --system

# 设置 yum repository
yum install -y yum-utils device-mapper-persistent-data lvm2
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# 安装 containerd
## yum update -y
sudo yum install -y containerd.io-${CONTAINERD_VERSION}

mkdir -p /etc/containerd
containerd config default > /etc/containerd/config.toml

# 修改Containerd配置文件，开启SystemdCgroup模式
sed -i "s/SystemdCgroup = false/SystemdCgroup = true/g" /etc/containerd/config.toml


systemctl daemon-reload
systemctl enable containerd
systemctl restart containerd


# 关闭 防火墙
systemctl stop firewalld
systemctl disable firewalld

# 关闭 SeLinux
setenforce 0
sed -i "s/SELINUX=enforcing/SELINUX=disabled/g" /etc/selinux/config

# 关闭 swap
swapoff -a
yes | cp /etc/fstab /etc/fstab_bak
cat /etc/fstab_bak | grep -v swap > /etc/fstab

```

* * *

* * *

* * *

##### **[containerd 常用命令](containerd-%e5%b8%b8%e7%94%a8%e5%91%bd%e4%bb%a4 "containerd 常用命令")**

* * *

* * *

* * *

##### **修改配置文件，添加Harbor私服仓库**

```ruby
vim /etc/containerd/config.toml

version = 2
# 用于存储containerd持久化数据
root = "/var/lib/containerd"
# 用于存储containerd临时性数据，设备重启后数据丢失。
state = "/run/containerd"
plugin_dir = ""
disabled_plugins = []
required_plugins = []
oom_score = 0

[grpc]
......

......
[plugins]
......
    [plugins."io.containerd.grpc.v1.cri".registry]
      [plugins."io.containerd.grpc.v1.cri".registry.mirrors]
-------------> 从这里开始是配置 Harbor的
        [plugins."io.containerd.grpc.v1.cri".registry.mirrors."172.16.15.183"]
          endpoint = ["http://172.16.15.183"]

      [plugins."io.containerd.grpc.v1.cri".registry.configs]
        [plugins."io.containerd.grpc.v1.cri".registry.configs."172.16.15.183".tls]
          insecure_skip_verify = true
        [plugins."io.containerd.grpc.v1.cri".registry.configs."172.16.15.183".auth]
          username = "admin"
          password = "Starcloud@2021"
<------------- End
......


## 重启配置
systemctl daemon-reload
systemctl enable containerd
systemctl restart containerd

```

* * *

###### 手动pull镜像, 强制使用 http协议

```ruby
ctr -n k8s.io i pull --plain-http 172.16.15.183/library/quay.io/tigera/operator:v1.15.1
```

* * *

* * *

* * *
