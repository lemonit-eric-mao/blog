---
title: 'K8s 安装部署(node)'
date: '2019-05-23T11:40:04+00:00'
status: private
permalink: /2019/05/23/k8s-%e5%ae%89%e8%a3%85%e9%83%a8%e7%bd%b2node
author: 毛巳煜
excerpt: ''
type: post
id: 4650
category:
    - Kubernetes
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
#### 1、前置条件

###### [安装主节点](http://www.dev-share.top/2019/05/21/k8s-%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2/ "安装主节点")

[修改主机名](http://www.dev-share.top/2018/10/10/linux-%E4%BF%AE%E6%94%B9%E4%B8%BB%E6%9C%BA%E5%90%8D/ "修改主机名")

[安装 Docker](http://www.dev-share.top/2017/11/16/%E5%AE%89%E8%A3%85-docker/ "安装 Docker")

###### 关闭防火墙

```ruby
systemctl stop firewalld && systemctl disable firewalld

```

- - - - - -

#### 2、环境、软件准备

查看操作系统 more /etc/redhat-release  
1\. CentOS Linux release 7.5.1804 (Core)  
2\. 每台机器最少1GB+内存  
3\. 集群中所有机器之间网络连接正常

<table><thead><tr><th>HostName</th><th>IP</th><th>CPU</th><th>MEM</th><th>DES</th></tr></thead><tbody><tr><td>k8s-master</td><td>172.26.48.4</td><td>2 Core</td><td>2G</td><td>k8s master 节点</td></tr><tr><td>k8s-node1</td><td>172.26.48.5</td><td>1 Core</td><td>2G</td><td>应用节点</td></tr><tr><td>k8s-node2</td><td>172.26.135.94</td><td>1 Core</td><td>2G</td><td>应用节点</td></tr></tbody></table>

`不要忘记修改本地/etc/hosts文件`

```ruby
# 将以下内容追加(>>)到 /etc/hosts文件
[root@k8s-node1 ~]# cat >> /etc/hosts 
```

#### 3、目标

##### 3.1 CentOS 7 配置国内阿里云镜像源

```ruby
# 将以下内容替换(>)到 /etc/yum.repos.d/kubernetes.repo文件
[root@k8s-node1 ~]# cat > /etc/yum.repos.d/kubernetes.repo 
```

##### 3.2 关闭 SELinux，目的为了允许容器能够与本机文件系统交互。

```ruby
[root@k8s-node1 ~]# setenforce 0
setenforce: SELinux is disabled
[root@k8s-node1 ~]# systemctl daemon-reload
# 查看结果
[root@k8s-node1 ~]# cat /etc/selinux/config

```

##### 3.3 修改网络开启桥接网络支持，`只针对（RHEL/CentOS 7）系统`

```ruby
[root@k8s-node1 ~]# cat > /etc/sysctl.d/k8s.conf 
```

##### 3.4 安装 ebtables ethtool，否则后边执行 kubeadm init 的时候会报错

```ruby
[root@k8s-node1 ~]# yum install ebtables ethtool -y
# 然后修改当前内核状态 这个文件是在 Docker安装成功后才出现的
[root@k8s-node1 ~]# echo 1 > /proc/sys/net/bridge/bridge-nf-call-iptables

```

##### 3.5 安装kubelet、kubeadm、kubectl `要与主节点版本一致`

```ruby
[root@k8s-node1 ~]# yum install -y kubelet-1.14.2 kubeadm-1.14.2 kubectl-1.14.2 kubernetes-cni-0.7.5
# 或者默认安装最新版
[root@k8s-node1 ~]# yum install -y kubelet kubeadm kubectl kubernetes-cni
[root@k8s-node1 ~]#
[root@k8s-node1 ~]#
[root@k8s-node1 ~]# systemctl start kubelet && systemctl status kubelet && systemctl enable kubelet

```

##### 3.6 创建文件 download\_image.sh 编写脚本批量下载镜像，并修改镜像tag与google的k8s镜像名称一致

```bash
[root@k8s-master ~]# mkdir -p /home/deploy/k8s/ && cd /home/deploy/k8s/

[root@k8s-master k8s]# cat > /home/deploy/k8s/download_image.sh 
```

##### 3.7 查看下载好的镜像

```ruby
[root@k8s-node1 ~]# docker images
REPOSITORY                           TAG                 IMAGE ID            CREATED             SIZE
k8s.gcr.io/kube-proxy                v1.14.2             5c24210246bb        7 days ago          82.1MB
k8s.gcr.io/pause                     3.1                 da86e6ba6ca1        17 months ago       742kB
quay.io/coreos/flannel               v0.10.0-amd64       f0fad859c909        22 months ago       44.6 MB
[root@k8s-node1 ~]#

```

##### 3.9 将node节点挂载到master上

```ruby
[root@k8s-node1 ~]# kubeadm join 172.26.48.4:6443 --token qc1eie.tviq9mcibgdssqgm \
    --discovery-token-ca-cert-hash sha256:4502298f771b00714e6f65e9a34a8f5651094aac917f1d42e9bcaf20658525bf

```

##### 3.10 回到主节点查看，子节点是否挂载成功

```ruby
[root@k8s-master ~]# kubectl get node
NAME         STATUS     ROLES    AGE    VERSION
k8s-master   Ready      master   9m8s   v1.14.2
k8s-node1    Ready      <none>   8m     v1.14.2
</none>
```

- - - - - -

- - - - - -

- - - - - -

##### 如果 K8s装错了 可以重置

```ruby
[root@k8s-node1 ~]# kubeadm reset

```

##### 如果 token 失效了

```ruby
[root@k8s-node1 ~]# kubeadm token create --print-join-command
kubeadm join 172.26.48.4:6443 --token kfu77t.0hrua2gremv09p1i     --discovery-token-ca-cert-hash sha256:4502298f771b00714e6f65e9a34a8f5651094aac917f1d42e9bcaf20658525bf
[root@k8s-node1 ~]#

```