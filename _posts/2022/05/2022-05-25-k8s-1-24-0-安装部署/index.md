---
title: "K8S 1.24.0 安装部署"
date: "2022-05-25"
categories: 
  - "k8s"
---

###### [最佳实践](https://kubernetes.io/zh/docs/setup/best-practices/ "最佳实践")

###### [支持](https://kubernetes.io/zh/docs/setup/best-practices/cluster-large/#%E6%94%AF%E6%8C%81 "支持")

在 v1.2x 版本中， Kubernetes 支持的最大节点数为 5000。更具体地说，我们支持满足以下所有条件的配置：

- 节点数不超过 `5000`
- 每个节点的 pod 数量不超过 `100`
- Pod 总数不超过 `150000`
- 容器总数不超过 `300000`

* * *

* * *

* * *

###### **[官方文档](https://kubernetes.io/zh/docs/setup/production-environment/container-runtimes/ "官方文档")**

###### **[国内教程](https://kuboard.cn/install/install-k8s.html "国内教程")**

* * *

###### **Container Runtime**

- Kubernetes v1.20 开始，默认移除 docker 的依赖，如果宿主机上安装了 docker 和 containerd，将优先使用 docker 作为容器运行引擎，如果宿主机上未安装 docker 只安装了 containerd，将使用 containerd 作为容器运行引擎；
- 本文使用 containerd 作为容器运行引擎；

###### **关于二进制安装**

- **kubeadm** 是 Kubernetes 官方支持的安装方式，**不是`二进制`** 。本文档采用 kubernetes.io 官方推荐的 **kubeadm** 工具安装 kubernetes 集群。

* * *

* * *

* * *

###### **`系统环境`**

```ruby
[root@master01 ~]# cat /etc/redhat-release
CentOS Linux release 7.9.2009 (Core)
[root@master01 ~]#
[root@master01 ~]#
[root@master01 ~]# cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6

10.22.12.61     master01
10.22.12.62     master02
10.22.12.63     master03
10.22.12.64     worker01
10.22.12.65     worker02
10.22.12.66     worker03
[root@master01 ~]#
```

* * *

* * *

* * *

###### 卸载旧版本依赖

```ruby
# 卸载旧版本， 根据实际情况不用每次都卸载
yum remove -y containerd.io
# 卸载旧版本， 根据实际情况不用每次都卸载
yum remove -y kubelet kubeadm kubectl
```

###### **[重新安装k8s](http://www.dev-share.top/2019/12/11/%e9%87%8d%e6%96%b0%e5%ae%89%e8%a3%85-k8s/ "重新安装k8s")**

* * *

##### **`安装 containerd`**

```ruby
# 在 master 节点和 worker 节点都要执行

# 指定k8s版本
export K8S_VERSION=1.24.0
# 指定Containerd版本
export CONTAINERD_VERSION=1.6.4
```

* * *

> - 关于初始化时用到的环境变量 **POD\_SUBNET** 所使用的网段不能与 **master节点/worker节点** 所在的网段重叠。该字段的取值为一个 **CIDR** 值，如果您对 **CIDR** 这个概念还不熟悉，请仍然执行 `export POD_SUBNET=10.100.0.1/16` 命令

###### 设置ApiServer的IP址

```ruby
# 单master节点时它为ApiServer的IP址，通常是master节点IP
# 高可用时它是负载均衡的虚IP(LOAD_BALANCER_IP)
export APISERVER_IP=10.22.12.61
# Kubernetes 容器组所在的网段，该网段安装完成后，由 kubernetes 创建，事先并不存在于您的物理网络中
export POD_SUBNET=10.100.0.1/16
```

* * *

###### **setup\_containerd.sh `在 master 节点和 worker 节点都要执行`**

```ruby
#!/bin/bash

# 在 master 节点和 worker 节点都要执行

if [[ ${K8S_VERSION} == '' ]]
  then
    echo -e "\033[31m 缺少环境变量: export K8S_VERSION=${K8S_VERSION} \033[0m"
    exit
  else
    echo -e "\033[32m export K8S_VERSION=${K8S_VERSION} \033[0m"
fi

if [[ ${CONTAINERD_VERSION} == ''  ]]
  then
    echo -e "\033[31m 缺少环境变量: export CONTAINERD_VERSION=${CONTAINERD_VERSION} \033[0m"
    exit
  else
    echo -e "\033[32m export CONTAINERD_VERSION=${CONTAINERD_VERSION} \033[0m"
fi

if [[ ${APISERVER_IP} == '' ]]
  then
    echo -e "\033[31m 缺少环境变量: export APISERVER_IP=${APISERVER_IP} \033[0m"
    exit
  else
    echo -e "\033[32m export APISERVER_IP=${APISERVER_IP} \033[0m"
fi

if [[ ${POD_SUBNET} == ''  ]]
  then
    echo -e "\033[31m 缺少环境变量: export POD_SUBNET=${POD_SUBNET} \033[0m"
    exit
  else
    echo -e "\033[32m export POD_SUBNET=${POD_SUBNET} \033[0m"
fi


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
sysctl --system

# 设置 yum repository
yum install -y yum-utils device-mapper-persistent-data lvm2

# 安装 containerd
## 添加下载源
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
## yum update -y
yum install -y containerd.io-${CONTAINERD_VERSION}

mkdir -p /etc/containerd
containerd config default > /etc/containerd/config.toml

# 修改Containerd配置文件，开启SystemdCgroup模式
sed -i "s/SystemdCgroup = false/SystemdCgroup = true/g" /etc/containerd/config.toml
# 根据实际版本
sed -i "s/pause:3.6/pause:3.7/g" /etc/containerd/config.toml


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

# 配置K8S的yum源
cat > /etc/yum.repos.d/kubernetes.repo << ERIC
[kubernetes]
name=Kubernetes
baseurl=http://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
repo_gpgcheck=0
gpgkey=http://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg
       http://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
ERIC

# 安装kubelet、kubeadm、kubectl
yum install -y kubelet-${K8S_VERSION} kubeadm-${K8S_VERSION} kubectl-${K8S_VERSION}

crictl config runtime-endpoint /run/containerd/containerd.sock

# 重启 docker，并启动 kubelet
systemctl daemon-reload
systemctl enable kubelet
systemctl start kubelet

containerd --version
kubelet --version

## ---------------------------------------------------------------------------------------------

# 生成 CNI 配置文件
cat > /etc/cni/net.d/10-containerd-net.conflist << ERIC
{
 "cniVersion": "1.0.0",
 "name": "containerd-net",
 "plugins": [
   {
     "type": "bridge",
     "bridge": "cni0",
     "isGateway": true,
     "ipMasq": true,
     "promiscMode": true,
     "ipam": {
       "type": "host-local",
       "ranges": [
         [{
           "subnet": "${POD_SUBNET}"
         }],
         [{
           "subnet": "2001:db8:4860::/64"
         }]
       ],
       "routes": [
         { "dst": "0.0.0.0/0" },
         { "dst": "::/0" }
       ]
     }
   },
   {
     "type": "portmap",
     "capabilities": {"portMappings": true}
   }
 ]
}
ERIC

## ---------------------------------------------------------------------------------------------

## 下载镜像
# 根据k8s的版本自动配置合适的镜像
images=$(kubeadm config images list --kubernetes-version=${K8S_VERSION})
# 转为数组
new_images=(${images//" "/})
for img in ${new_images[@]};
do
    # 下载阿里云镜像（因 1.20.与 1.23.x以后的coredns名称不一致，因此做了如下处理）
    if [[ $img != *coredns/* ]]
    then
        #echo ${img/k8s.gcr.io\//registry.cn-qingdao.aliyuncs.com\/cn-aliyun/}
        ctr -n k8s.io i pull ${img/k8s.gcr.io\//registry.cn-qingdao.aliyuncs.com\/cn-aliyun/}
        ctr -n k8s.io i tag ${img/k8s.gcr.io\//registry.cn-qingdao.aliyuncs.com\/cn-aliyun/} $img
    else
        #echo ${img/k8s.gcr.io\//registry.cn-qingdao.aliyuncs.com\/cn-aliyun/}
        ctr -n k8s.io i pull ${img/k8s.gcr.io\/coredns\//registry.cn-qingdao.aliyuncs.com\/cn-aliyun/}
        ctr -n k8s.io i tag ${img/k8s.gcr.io\/coredns\//registry.cn-qingdao.aliyuncs.com\/cn-aliyun/} $img
    fi
    echo '+----------------------------------------------------------------+'
    echo ''
done

echo ""
echo -e "\033[32m Kubernetes依赖安装完成 \033[0m"

```

* * *

* * *

* * *

##### **`初始化 master 节点`**

###### **init\_master.sh `只在 master 节点执行`**

```ruby
#!/bin/bash
# 只在第一个master节点上执行
# 脚本出错时终止执行
set -e

rm -rf ./kubeadm-config.yaml

cat > kubeadm-config.yaml << ERIC
---

apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
kubernetesVersion: ${K8S_VERSION}
controlPlaneEndpoint: ${APISERVER_IP}:6443          # "LOAD_BALANCER_IP:LOAD_BALANCER_PORT"

# 只在部署高可用时配置 apiServer
apiServer:
  # 生成的~/.kube/config证书，都允许使用哪些IP地址访问ApiServer，地址可以写多个，也可以写域名
  # 例如：你希望公网和内网都能支持访问，就可能会设置多个IP
  certSANs:
    - ${APISERVER_IP}                               #- "LOAD_BALANCER_IP"
#    - 178.177.27.25                                 #- "LOAD_BALANCER_IP"
#    - 178.137.22.26                                 #- "LOAD_BALANCER_IP"

# 修改etcd数据存储目录
#etcd:
#  local:
#    dataDir: /mnt/etcd-data

# 配置集群内部网段
networking:
  dnsDomain: cluster.local
  serviceSubnet: 10.96.0.0/16                       # 设定service 网段，不做修改
  podSubnet: ${POD_SUBNET}                          # 设定pod 网段

#---
#
#apiVersion: kubelet.config.k8s.io/v1beta1
#kind: KubeletConfiguration
#cgroupDriver: systemd
#
#---
#
#apiVersion: kubeproxy.config.k8s.io/v1alpha1
#kind: KubeProxyConfiguration
#mode: "ipvs"
#ipvs:
#  strictARP: true


ERIC

# kubeadm init
echo ""
echo -e "\033[32m 初始化 Master 节点 \033[0m"
kubeadm init --config=kubeadm-config.yaml --upload-certs

# 配置 kubectl
rm -rf /root/.kube/
mkdir -p $HOME/.kube
cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
chown $(id -u):$(id -g) $HOME/.kube/config

echo ""
echo -e "\033[32m Kubernetes初始化完成 \033[0m"

```

* * *

###### **安装网络插件, 只在 `master` 节点执行**

```ruby
wget http://qiniu.dev-share.top/cni/k8s-1.24.x-calico-3.20.5.yaml
kubectl apply -f k8s-1.24.x-calico-3.20.5.yaml

```

* * *

* * *

* * *
