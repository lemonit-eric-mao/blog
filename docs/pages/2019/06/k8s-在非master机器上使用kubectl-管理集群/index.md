---
title: "K8s 在非master机器上使用kubectl 管理集群"
date: "2019-06-13"
categories: 
  - "k8s"
---

> 在准备的虚拟机上安装配置kubectl，注意版本需要与k8s版本保持一致

```shell
# 配置k8s的yum源
cat > /etc/yum.repos.d/kubernetes.repo << EOF
[kubernetes]
name=Kubernetes
baseurl=http://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
repo_gpgcheck=0
gpgkey=http://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg
       http://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF

# 安装kubectl
yum install -y kubectl-1.24.0

# 配置kubectl
mkdir $HOME/.kube
scp root@xxx.xxx.xxx.xxx:/root/.kube/config $HOME/.kube

```
