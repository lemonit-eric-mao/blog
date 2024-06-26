---
title: "K8s 安装部署(master)"
date: "2019-05-21"
categories: 
  - "k8s"
---

#### 1、kubeadm 介绍

```
Kubernetes 是 Google 开源的基于 Docker 的容器集群管理系统，通过 yaml 语言写的配置文件，简单快速的就能自动部署好应用环境，支持应用横向扩展，并且可以组织、编排、管理和迁移这些容器化的应用。Kubeadm 是一个可以快速帮助我们创建稳定集群服务的工具，通过它，我们可以在虚拟机、实体机或者云端快速部署一个高可用的集群服务。
```

###### [K8S 国内教程](https://kuboard.cn/learning/k8s-basics/kubernetes-basics.html "K8S 国内教程")

###### [修改主机名](http://www.dev-share.top/2018/10/10/linux-%E4%BF%AE%E6%94%B9%E4%B8%BB%E6%9C%BA%E5%90%8D/ "修改主机名")

###### [安装 Docker](http://www.dev-share.top/2017/11/16/%E5%AE%89%E8%A3%85-docker/ "安装 Docker")

* * *

###### 关闭防火墙

```ruby
systemctl stop firewalld && systemctl disable firewalld
```

* * *

* * *

* * *

#### 2、环境、软件准备

查看操作系统 more /etc/redhat-release 1. CentOS Linux release 7.5.1804 (Core) 2. 每台机器最少1GB+内存 3. 集群中所有机器之间网络连接正常

| HostName | IP | CPU | MEM | DES |
| --- | --- | --- | --- | --- |
| k8s-master | 172.26.48.4 | 2 Core | 2G | k8s master 节点 |
| k8s-node1 | 172.26.48.5 | 1 Core | 2G | 应用节点 |
| k8s-node2 | 172.26.135.94 | 1 Core | 2G | 应用节点 |

`不要忘记修改本地/etc/hosts文件`

```ruby
# 将以下内容追加(>>)到 /etc/hosts文件
[root@k8s-master ~]# cat >> /etc/hosts << ERIC
172.26.48.4    k8s-master
172.26.48.5    k8s-node1
172.26.135.94  k8s-node2

ERIC

```

* * *

* * *

* * *

#### 3、目标

在您的机器上安装一个安全的Kubernetes集群 在群集上安装pod网络，以便应用组件（pod）可以相互通信 在集群上安装一个微服务应用示例

* * *

##### 3.1 CentOS 7 配置国内阿里云镜像源

```ruby
# 将以下内容替换(>)到 /etc/yum.repos.d/kubernetes.repo文件
[root@k8s-master ~]# cat > /etc/yum.repos.d/kubernetes.repo << ERIC

[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
enabled=1
# 如果改成 0，yum update 时 k8s就不会自动升级了
# enabled=0
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg

ERIC

[root@k8s-master ~]#
```

* * *

##### 3.2 关闭 SELinux，目的为了允许容器能够与本机文件系统交互。

```ruby
[root@k8s-master ~]# setenforce 0
setenforce: SELinux is disabled
[root@k8s-master ~]# systemctl daemon-reload
# 查看结果
[root@k8s-master ~]# cat /etc/selinux/config
```

* * *

##### 3.3 修改网络开启桥接网络支持，只针对（RHEL/CentOS 7）系统

```ruby
[root@k8s-master ~]# cat >  /etc/sysctl.d/k8s.conf << EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
[root@k8s-master ~]# sysctl -p /etc/sysctl.d/k8s.conf
[root@k8s-master ~]#
[root@k8s-master ~]# sysctl --system
[root@k8s-master ~]#
```

* * *

##### 3.4 安装 ebtables ethtool，否则后边执行 kubeadm init 的时候会报错

```ruby
[root@k8s-master ~]# yum install ebtables ethtool -y
# 然后修改当前内核状态 这个文件是在 Docker安装成功后才出现的
[root@k8s-master ~]# echo 1 > /proc/sys/net/bridge/bridge-nf-call-iptables
```

* * *

##### 3.5 安装kubelet、kubeadm、kubectl

```ruby
[root@k8s-master ~]# yum install -y kubelet-1.14.2 kubeadm-1.14.2 kubectl-1.14.2 kubernetes-cni-0.7.5
# 或者默认安装最新版
[root@k8s-master ~]# yum install -y kubelet kubeadm kubectl kubernetes-cni
[root@k8s-master ~]#
[root@k8s-master ~]#
[root@k8s-master ~]# systemctl start kubelet && systemctl status kubelet && systemctl enable kubelet
```

* * *

##### 3.6 镜像准备

**kubernetes 服务启动依赖很多镜像，但是这些镜像要是在国内没有翻墙的话，是下载不下来的。这里我们可以去 [Docker Hub](https://hub.docker.com "Docker Hub") 下载指定版本的镜像替代，下载完成后，通过 docker tag ... 命令修改成指定名称的镜像即可。** `查看 kubeadm 版本为1.14.2所需要的依赖镜像`

```ruby
[root@k8s-master deploy]# kubeadm config images list
I0524 22:03:10.774681   19610 version.go:96] could not fetch a Kubernetes version from the internet: unable to get URL "https://dl.k8s.io/release/stable-1.txt": Get https://dl.k8s.io/release/stable-1.txt: net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)
I0524 22:03:10.774766   19610 version.go:97] falling back to the local client version: v1.14.2
k8s.gcr.io/kube-apiserver:v1.14.2
k8s.gcr.io/kube-controller-manager:v1.14.2
k8s.gcr.io/kube-scheduler:v1.14.2
k8s.gcr.io/kube-proxy:v1.14.2
k8s.gcr.io/pause:3.1
k8s.gcr.io/etcd:3.3.10
k8s.gcr.io/coredns:1.3.1
[root@k8s-master deploy]#
# 查看镜像数
[root@k8s-master deploy]# kubeadm config images list | grep k8s.gcr.io | wc -l
7
[root@k8s-master deploy]#

```

* * *

##### 3.7 创建文件 download\_image.sh 编写脚本批量下载镜像，并修改镜像tag与google的k8s镜像名称一致

```bash
[root@k8s-master ~]# mkdir -p /home/deploy/k8s/ && cd /home/deploy/k8s/

[root@k8s-master k8s]# cat > /home/deploy/k8s/download_image.sh << ERIC
#!/bin/bash
# 定义镜像集合数组
images=(
    kube-apiserver:v1.14.2
    kube-controller-manager:v1.14.2
    kube-scheduler:v1.14.2
    kube-proxy:v1.14.2
    pause:3.1
    etcd:3.3.10
    coredns:1.3.1
)
# 循环从 registry.cn-hangzhou.aliyuncs.com 中下载镜像

echo '+----------------------------------------------------------------+'
for img in \${images[@]};
do
    # 从国内源下载镜像
    docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/\$img
    # 改变镜像名称
    docker tag  registry.cn-hangzhou.aliyuncs.com/google_containers/\$img k8s.gcr.io/\$img
    # 删除源始镜像
    docker rmi  registry.cn-hangzhou.aliyuncs.com/google_containers/\$img
    #
    echo '+----------------------------------------------------------------+'
    echo ''
done

# 下载网络插件
# 官网地址：https://quay.io/repository/coreos/flannel?tag=latest&tab=tags
docker pull quay.io/coreos/flannel:v0.10.0-amd64

ERIC

[root@k8s-master k8s]#
[root@k8s-master k8s]# ll
total 4
-rw-r--r-- 1 root root 719 Jul 22 11:53 download_image.sh
[root@k8s-master k8s]#
[root@k8s-master k8s]# chmod -R 777 download_image.sh
[root@k8s-master k8s]#
[root@k8s-master k8s]# ./download_image.sh
```

* * *

##### 3.8 查看下载好的镜像

```ruby
[root@k8s-master k8s]# docker images
REPOSITORY                           TAG                 IMAGE ID            CREATED             SIZE
k8s.gcr.io/kube-proxy                v1.14.2             5c24210246bb        7 days ago          82.1MB
k8s.gcr.io/kube-apiserver            v1.14.2             5eeff402b659        7 days ago          210MB
k8s.gcr.io/kube-controller-manager   v1.14.2             8be94bdae139        7 days ago          158MB
k8s.gcr.io/kube-scheduler            v1.14.2             ee18f350636d        7 days ago          81.6MB
k8s.gcr.io/coredns                   1.3.1               eb516548c180        4 months ago        40.3MB
k8s.gcr.io/etcd                      3.3.10              2c4adeb21b4f        5 months ago        258MB
k8s.gcr.io/pause                     3.1                 da86e6ba6ca1        17 months ago       742kB
quay.io/coreos/flannel               v0.10.0-amd64       f0fad859c909        22 months ago       44.6 MB
[root@k8s-master k8s]#
# 查看镜像数
[root@k8s-master k8s]# docker images | grep -E "k8s.gcr.io|quay.io" | wc -l
8
[root@k8s-master k8s]#
```

* * *

##### 3.9 初始化 master

**kubeadm init --pod-network-cidr=<pod网络IP地址/子网掩码> --kubernetes-version=<k8s版本>**

```ruby
[root@k8s-master k8s]# kubeadm init --pod-network-cidr=10.244.0.0/16 --kubernetes-version=v1.14.2
......

Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:
  # 注意：想要操作k8s的用户，必须在当前用户环境下生成 ~/.kube文件
  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 172.26.48.4:6443 --token yx9yza.rcb08m1giup70y63 \
    --discovery-token-ca-cert-hash sha256:f6548aa3508014ac5dab129231b54f5085f37fe8e6fc5d362f787be70a1a8a6e
[root@k8s-master k8s]#
```

* * *

##### 3.10 安装 pod 网络附加组件

**kubernetes 提供了很多种网络组件选择，有 Calia、Canal、Flannel、Kube-router、Romana、Weave Net 可以使用，具体使用可以参考 [（3/4）安装pod网络](http://docs.kubernetes.org.cn/459.html#34pod "（3/4）安装pod网络") 来操作**

###### 安装 **`Calico`** 网络插件 **(`二选一`)** 待补充

**[官网 使用 canal](https://docs.projectcalico.org/getting-started/kubernetes/flannel/flannel "官网 使用 canal")**

```ruby
[root@k8s-master k8s]# curl https://docs.projectcalico.org/manifests/canal.yaml -O
[root@k8s-master k8s]#
[root@k8s-master k8s]# kubectl apply -f canal.yaml
[root@k8s-master k8s]#
```

###### 安装 **`Flannel`** 网络插件 **(`二选一`)**

**注意： 为了使Flannel正常工作，执行kubeadm init命令时需要增加--pod-network-cidr=10.244.0.0/16参数。Flannel适用于amd64，arm，arm64和ppc64le上工作，但使用除amd64平台得其他平台，你必须手动下载并替换amd64。**

[Flannel Github](https://github.com/coreos/flannel/tree/master/Documentation "Flannel Github")

```ruby
# 安装 redhat-lsb 工具
[root@k8s-master deploy]# yum install -y redhat-lsb
# 查看当前系统的发行版信息
[root@k8s-master deploy]# lsb_release -a
LSB Version:    :core-4.1-amd64:core-4.1-noarch
Distributor ID: CentOS
Description:    CentOS Linux release 7.5.1804 (Core)
Release:        7.5.1804
Codename:       Core
[root@k8s-master k8s]#
[root@k8s-master k8s]#
[root@k8s-master k8s]#
# 下载指定tag版本下载
[root@k8s-master k8s]# curl -L -O https://raw.githubusercontent.com/coreos/flannel/v0.11.0/Documentation/k8s-manifests/kube-flannel-rbac.yml
[root@k8s-master k8s]#
[root@k8s-master k8s]# kubectl apply -f kube-flannel-rbac.yml
[root@k8s-master k8s]#
[root@k8s-master k8s]#
[root@k8s-master k8s]#
# 下载指定tag版本下载
[root@k8s-master k8s]# curl -L -O https://raw.githubusercontent.com/coreos/flannel/v0.11.0/Documentation/kube-flannel.yml
[root@k8s-master k8s]#
[root@k8s-master k8s]# kubectl apply -f kube-flannel.yml
[root@k8s-master k8s]#
[root@k8s-master k8s]#
[root@k8s-master k8s]#
# 需要等待一小会儿，在查看运行状态就都是 Running 了
[root@k8s-master k8s]# kubectl get pod -A
NAMESPACE     NAME                                 READY   STATUS    RESTARTS   AGE
kube-system   coredns-fb8b8dccf-8xbcf              1/1     Running   0          2m8s
kube-system   coredns-fb8b8dccf-ztxxg              1/1     Running   0          2m8s
kube-system   etcd-k8s-master                      1/1     Running   0          81s
kube-system   kube-apiserver-k8s-master            1/1     Running   0          81s
kube-system   kube-controller-manager-k8s-master   1/1     Running   0          74s
kube-system   kube-flannel-ds-amd64-hk4wt          1/1     Running   0          51s
kube-system   kube-proxy-kcvph                     1/1     Running   0          2m7s
kube-system   kube-scheduler-k8s-master            1/1     Running   0          69s
[root@k8s-master k8s]#
```

* * *

##### 3.10 查看主节点是否安装成功

```ruby
[root@k8s-master k8s]# kubectl get node
NAME         STATUS     ROLES    AGE    VERSION
k8s-master   Ready      master   9m8s   v1.14.2
```

* * *

* * *

* * *

###### [安装子节点](http://www.dev-share.top/2019/05/23/k8s-%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2node/ "安装子节点")

###### 教程

[腾讯云社区](https://cloud.tencent.com/developer/article/1010569 "腾讯云社区") [k8s中文网](http://docs.kubernetes.org.cn/459.html "k8s中文网")

* * *

* * *

* * *

##### **`常见问题`**

###### 1 k8s 1核CPU 安装的常见问题

```ruby
[root@k8s-master k8s]# kubeadm init  --pod-network-cidr=10.244.0.0/16 --kubernetes-version=v1.14.2
[init] Using Kubernetes version: v1.14.2
[preflight] Running pre-flight checks
        [WARNING IsDockerSystemdCheck]: detected "cgroupfs" as the Docker cgroup driver. The recommended driver is "systemd". Please follow the guide at https://kubernetes.io/docs/setup/cri/
        [WARNING SystemVerification]: this Docker version is not on the list of validated versions: 19.03.0-beta5. Latest validated version: 18.09
error execution phase preflight: [preflight] Some fatal errors occurred:
        [ERROR NumCPU]: the number of available CPUs 1 is less than the required 2
[preflight] If you know what you are doing, you can make a check non-fatal with `--ignore-preflight-errors=...`
[root@k8s-master k8s]#
# 忽略掉即可
[root@k8s-master k8s]# kubeadm init  --pod-network-cidr=10.244.0.0/16 --kubernetes-version=v1.14.2 --ignore-preflight-errors=NumCPU
```

###### 2 装好了初始化 Master 完成后，我们使用命令 kubectl get node 查看集群节点信息，但是你会发现并没有出现 Node 信息，反而报错如下：

```ruby
[root@k8s-master k8s]# kubectl get pods
The connection to the server localhost:8080 was refused - did you specify the right host or port?
```

###### 2.1 上面的问题原因是缺少步骤

```ruby
[root@k8s-master k8s]# mkdir -p $HOME/.kube
[root@k8s-master k8s]# cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
[root@k8s-master k8s]# chown $(id -u):$(id -g) $HOME/.kube/config
[root@k8s-master k8s]#
[root@k8s-master k8s]# kubectl get node
NAME         STATUS     ROLES    AGE    VERSION
k8s-master   NotReady   master   9m8s   v1.14.2
[root@k8s-master k8s]#
[root@k8s-master k8s]# kubectl get pod -A
NAMESPACE     NAME                      READY   STATUS    RESTARTS   AGE
kube-system   coredns-fb8b8dccf-8xbcf   0/1     Pending   0          10s
kube-system   coredns-fb8b8dccf-ztxxg   0/1     Pending   0          10s
kube-system   kube-proxy-kcvph          1/1     Running   0          9s
[root@k8s-master k8s]#
```

* * *

* * *

* * *
