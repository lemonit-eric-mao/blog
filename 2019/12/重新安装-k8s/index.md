---
title: "重新安装 K8S"
date: "2019-12-11"
categories: 
  - "k8s"
---

### 一、彻底删除 k8s

```ruby
kubeadm reset -f
systemctl stop kubelet
yum remove -y kubelet kubeadm kubectl
systemctl daemon-reload

modprobe -r ipip
rm -rf ~/.kube/
rm -rf /etc/kubernetes/
rm -rf /etc/systemd/system/kubelet.service.d
rm -rf /etc/systemd/system/kubelet.service
rm -rf /etc/cni
rm -rf /opt/cni
rm -rf /usr/bin/kube*
rm -rf /var/lib/etcd
rm -rf /var/lib/kubelet/
rm -rf /var/lib/dockershim
rm -rf /var/lib/cni
rm -rf /var/run/kubernetes
rm -rf /var/etcd

```

* * *

###### 如果是使用etcdadm安装的外部etcd

```ruby
etcdadm reset
```

卸载完成后，在次安装时需要重新推送证书

* * *

### 二、[K8s 1.26.0 安装部署](http://www.dev-share.top/2023/02/22/k8s-1-26-0-%e5%ae%89%e8%a3%85%e9%83%a8%e7%bd%b2/ "K8s 1.26.0 安装部署")
