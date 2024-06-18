---
title: '离线部署 K8S 高可用 外部etcd'
date: '2020-08-12T03:31:12+00:00'
status: private
permalink: /2020/08/12/%e7%a6%bb%e7%ba%bf%e9%83%a8%e7%bd%b2-k8s-%e9%ab%98%e5%8f%af%e7%94%a8-%e5%a4%96%e9%83%a8etcd
author: 毛巳煜
excerpt: ''
type: post
id: 5722
category:
    - Kubernetes
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### **[官网高可用部署方案](https://kubernetes.io/zh/docs/setup/production-environment/tools/kubeadm/ha-topology/ "官网高可用部署方案")**

###### **[为 kube-apiserver 选择负载均衡器](https://kubernetes.io/zh/docs/setup/production-environment/tools/kubeadm/high-availability/#%E4%B8%BA-kube-apiserver-%E5%88%9B%E5%BB%BA%E8%B4%9F%E8%BD%BD%E5%9D%87%E8%A1%A1%E5%99%A8 "为 kube-apiserver 选择负载均衡器")**

###### **[官方推荐高可用负载均衡选择](https://github.com/kubernetes/kubeadm/blob/master/docs/ha-considerations.md#options-for-software-load-balancing "官方推荐高可用负载均衡选择")**

###### **[Kuboard 提供的文档](https://kuboard.cn/install/install-kubernetes.html#%E5%AE%89%E8%A3%85kubernetes%E9%AB%98%E5%8F%AF%E7%94%A8 "Kuboard 提供的文档")**

- - - - - -

###### 环境

<table><thead><tr><th>IP地址</th><th>应用部署</th></tr></thead><tbody><tr><td>192.168.20.90</td><td>Control(主控机)</td></tr><tr><td>192.168.20.91</td><td>master1</td></tr><tr><td>192.168.20.92</td><td>master2</td></tr><tr><td>192.168.20.93</td><td>master3</td></tr><tr><td>192.168.20.91</td><td>etcd1</td></tr><tr><td>192.168.20.92</td><td>etcd2</td></tr><tr><td>192.168.20.93</td><td>etcd3</td></tr><tr><td>192.168.20.94</td><td>worker</td></tr><tr><td>192.168.20.95</td><td>HAProxy1</td></tr><tr><td>192.168.20.96</td><td>HAProxy2</td></tr><tr><td>192.168.20.97</td><td>Virtual IP</td></tr></tbody></table>

- - - - - -

###### **`创建目录`**

```ruby
[root@Control ~]# mkdir -p /home/deploy/offline_setup/

```

###### 提前准备所需要的 `rpm`、`docker image`

- 使用 `yumdownloader --resolve --downloadonly --downloaddir=$PWD 程序包名称` 工具 将 rpm包下载到本地
- 将k8s所需要的 镜像 `docker save  xxxx:vv > xxx-vv.docker` 到本地
- [修改主机名](http://www.dev-share.top/2018/10/10/linux-%E4%BF%AE%E6%94%B9%E4%B8%BB%E6%9C%BA%E5%90%8D/ "修改主机名")

**大概要这么多**

```ruby
[root@Control ~]# tree /home/deploy/offline_setup/
/home/deploy/offline_setup/
├── etcd
│   ├── etcdadm
│   └── etcd-v3.3.8-linux-amd64.tar.gz
├── images
│   ├── calico-cni-v3.15.1.docker
│   ├── calico-node-v3.15.1.docker
│   ├── calico-pod2daemon-flexvol-v3.15.1.docker
│   ├── calico/kube-controllers:v3.15.1
│   ├── flanneld-v0.11.0-amd64.docker
│   ├── k8s.gcr.io-coredns-1.6.2.docker
│   ├── k8s.gcr.io-kube-apiserver-v1.16.6.docker
│   ├── k8s.gcr.io-kube-controller-manager-v1.16.6.docker
│   ├── k8s.gcr.io-kube-proxy-v1.16.6.docker
│   ├── k8s.gcr.io-kube-scheduler-v1.16.6.docker
│   └── k8s.gcr.io-pause-3.1.docker
├── rpm-lib
│   ├── ansible
│   │   ├── ansible-2.9.10-1.el7.noarch.rpm
│   │   ├── libyaml-0.1.4-11.el7_0.x86_64.rpm
│   │   ├── python2-cryptography-1.7.2-2.el7.x86_64.rpm
│   │   ├── python2-httplib2-0.18.1-3.el7.noarch.rpm
│   │   ├── python2-jmespath-0.9.4-2.el7.noarch.rpm
│   │   ├── python2-pyasn1-0.1.9-7.el7.noarch.rpm
│   │   ├── python-babel-0.9.6-8.el7.noarch.rpm
│   │   ├── python-backports-1.0-8.el7.x86_64.rpm
│   │   ├── python-backports-ssl_match_hostname-3.5.0.1-1.el7.noarch.rpm
│   │   ├── python-cffi-1.6.0-5.el7.x86_64.rpm
│   │   ├── python-enum34-1.0.4-1.el7.noarch.rpm
│   │   ├── python-idna-2.4-1.el7.noarch.rpm
│   │   ├── python-ipaddress-1.0.16-2.el7.noarch.rpm
│   │   ├── python-jinja2-2.7.2-4.el7.noarch.rpm
│   │   ├── python-markupsafe-0.11-10.el7.x86_64.rpm
│   │   ├── python-paramiko-2.1.1-9.el7.noarch.rpm
│   │   ├── python-ply-3.4-11.el7.noarch.rpm
│   │   ├── python-pycparser-2.14-1.el7.noarch.rpm
│   │   ├── python-setuptools-0.9.8-7.el7.noarch.rpm
│   │   ├── python-six-1.9.0-2.el7.noarch.rpm
│   │   ├── PyYAML-3.10-11.el7.x86_64.rpm
│   │   └── sshpass-1.06-2.el7.x86_64.rpm
│   ├── docker
│   │   ├── audit-2.8.5-4.el7.x86_64.rpm
│   │   ├── audit-libs-2.8.5-4.el7.x86_64.rpm
│   │   ├── audit-libs-python-2.8.5-4.el7.x86_64.rpm
│   │   ├── checkpolicy-2.5-8.el7.x86_64.rpm
│   │   ├── containerd.io-1.2.13-3.2.el7.x86_64.rpm
│   │   ├── container-selinux-2.119.2-1.911c772.el7_8.noarch.rpm
│   │   ├── docker-ce-19.03.9-3.el7.x86_64.rpm
│   │   ├── docker-ce-cli-19.03.12-3.el7.x86_64.rpm
│   │   ├── libcgroup-0.41-21.el7.x86_64.rpm
│   │   ├── libseccomp-2.3.1-4.el7.x86_64.rpm
│   │   ├── libsemanage-python-2.5-14.el7.x86_64.rpm
│   │   ├── policycoreutils-2.5-34.el7.x86_64.rpm
│   │   ├── policycoreutils-python-2.5-34.el7.x86_64.rpm
│   │   ├── python-IPy-0.75-6.el7.noarch.rpm
│   │   └── setools-libs-3.3.8-4.el7.x86_64.rpm
│   ├── haproxy
│   │   ├── haproxy22-2.2.1-1.el7.ius.x86_64.rpm
│   │   └── pcre2-10.23-2.el7.x86_64.rpm
│   ├── k8s
│   │   ├── 029bc0d7b2112098bdfa3f4621f2ce325d7a2c336f98fa80395a3a112ab2a713-kubernetes-cni-0.8.6-0.x86_64.rpm
│   │   ├── 0bfd3f23e53d4663860cd89b9304fba5a7853d7b02a8985e4d3c240d10bf6587-kubectl-1.16.6-0.x86_64.rpm
│   │   ├── 0eeb459890b1c8f07c91a9771ce5f4df6c2b318ff2e8902ed9228bf01944cfd7-kubeadm-1.16.6-0.x86_64.rpm
│   │   └── 6f0d57f3271c856b9790f6628d0fa2f2d51e5e5c33faf2d826f3fc07a1907cde-kubelet-1.16.6-0.x86_64.rpm
│   ├── keepalived
│   │   ├── keepalived-1.3.5-16.el7.x86_64.rpm
│   │   ├── lm_sensors-libs-3.4.0-8.20160601gitf9185e5.el7.x86_64.rpm
│   │   ├── net-snmp-agent-libs-5.7.2-48.el7_8.1.x86_64.rpm
│   │   └── net-snmp-libs-5.7.2-48.el7_8.1.x86_64.rpm
│   ├── ntp
│   │   ├── autogen-libopts-5.18-5.el7.x86_64.rpm
│   │   ├── ntp-4.2.6p5-29.el7.centos.2.x86_64.rpm
│   │   └── ntpdate-4.2.6p5-29.el7.centos.2.x86_64.rpm
│   └── tools
│       ├── gpm-libs-1.20.7-6.el7.x86_64.rpm
│       ├── net-tools-2.0-0.25.20131004git.el7.x86_64.rpm
│       ├── perl-5.16.3-295.el7.x86_64.rpm
│       ├── perl-Carp-1.26-244.el7.noarch.rpm
│       ├── perl-constant-1.27-2.el7.noarch.rpm
│       ├── perl-Encode-2.51-7.el7.x86_64.rpm
│       ├── perl-Exporter-5.68-3.el7.noarch.rpm
│       ├── perl-File-Path-2.09-2.el7.noarch.rpm
│       ├── perl-File-Temp-0.23.01-3.el7.noarch.rpm
│       ├── perl-Filter-1.49-3.el7.x86_64.rpm
│       ├── perl-Getopt-Long-2.40-3.el7.noarch.rpm
│       ├── perl-HTTP-Tiny-0.033-3.el7.noarch.rpm
│       ├── perl-libs-5.16.3-295.el7.x86_64.rpm
│       ├── perl-macros-5.16.3-295.el7.x86_64.rpm
│       ├── perl-parent-0.225-244.el7.noarch.rpm
│       ├── perl-PathTools-3.40-5.el7.x86_64.rpm
│       ├── perl-Pod-Escapes-1.04-295.el7.noarch.rpm
│       ├── perl-podlators-2.5.1-3.el7.noarch.rpm
│       ├── perl-Pod-Perldoc-3.20-4.el7.noarch.rpm
│       ├── perl-Pod-Simple-3.28-4.el7.noarch.rpm
│       ├── perl-Pod-Usage-1.63-3.el7.noarch.rpm
│       ├── perl-Scalar-List-Utils-1.27-248.el7.x86_64.rpm
│       ├── perl-Socket-2.010-5.el7.x86_64.rpm
│       ├── perl-Storable-2.45-3.el7.x86_64.rpm
│       ├── perl-Text-ParseWords-3.29-4.el7.noarch.rpm
│       ├── perl-threads-1.87-4.el7.x86_64.rpm
│       ├── perl-threads-shared-1.43-6.el7.x86_64.rpm
│       ├── perl-Time-HiRes-1.9725-3.el7.x86_64.rpm
│       ├── perl-Time-Local-1.2300-2.el7.noarch.rpm
│       ├── vim-common-7.4.629-6.el7.x86_64.rpm
│       ├── vim-enhanced-7.4.629-6.el7.x86_64.rpm
│       └── vim-filesystem-7.4.629-6.el7.x86_64.rpm
└── yaml
    ├── 1_init.yaml
    ├── 2_deploy_ntp.yaml
    ├── 3_deploy_docker.yaml
    ├── 4_deploy.yaml
    ├── 5_start.yaml
    ├── 6_stop.yaml
    ├── 7_destory.yaml
    ├── ansible.cfg
    ├── canal.yaml
    ├── hosts.ini
    └── inventory.ini

[root@Control ~]#

```

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

###### 安装 ansible

```ruby
rpm -ivh --force --nodeps /home/deploy/offline_setup/rpm-lib/ansible/*

```

- - - - - -

###### ansible-playbook 设置 ssh

###### 主控机，需要提前执行 `ssh-keygen -t rsa`

```ruby
cat > init.yaml 
```

- - - - - -

###### 所有节点 NTP 同步 (使用 ansible-playbook)

```yaml
###################################################
# ansible-playbook -i hosts.ini deploy_ntp.yaml #
###################################################

- hosts: all
  tasks:
    - name: get facts
      setup:

    - name: '将本地文件拷贝至各主机'
      copy:
        src: '{{ deploy_dir }}/rpm-lib/ntp-client'
        dest: '{{ deploy_dir }}/rpm-lib/'

    - name: '离线安装NTP客户端'
      shell: rpm -ivh {{ deploy_dir }}/rpm-lib/ntp-client/* --force --nodeps

    - name: 启动 ntpdate
      service:
        name: ntpdate
        state: started
        enabled: yes

    - name: '同步'
      shell: ntpdate {{ ntp_server }}


```

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

###### [安装 HAProxy](http://www.dev-share.top/2020/08/12/centos-7-%e4%ba%8c%e8%bf%9b%e5%88%b6%e5%ae%89%e8%a3%85-haproxy/ "安装 HAProxy") **(`192.168.20.95`, `192.168.20.96`)**

```ruby
# 安装 HAProxy 必须要闭关 SELinux
setenforce 0
sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config

mkdir -p /home/deploy/haproxy && cd /home/deploy/haproxy

# 使用离线包 安装
rpm -ivh /home/deploy/offline_setup/rpm-lib/haproxy/* --force --nodeps

# 配置日志
echo 'local2=debug     /var/log/haproxy.log' > /etc/rsyslog.d/haproxy.conf

systemctl restart rsyslog

mv /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg-bak

# 创建文件
cat > /etc/haproxy/haproxy.cfg 
```

- - - - - -

- - - - - -

- - - - - -

###### 安装 Keepalived **(`192.168.20.95`, `192.168.20.96`)**

```ruby
# 使用离线包 安装
rpm -ivh /home/deploy/offline_setup/rpm-lib/keepalived/* --force --nodeps

cat > /etc/keepalived/scripts/check_haproxy.sh  /etc/keepalived/keepalived.conf 
```

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

###### **[使用 etcdadm 安装 etcd集群](http://www.dev-share.top/2020/08/12/%e4%bd%bf%e7%94%a8-etcdadm-%e5%ae%89%e8%a3%85-etcd%e9%9b%86%e7%be%a4/ "使用 etcdadm 安装 etcd集群")**

```ruby
ssh 192.168.20.91 yum -y install rsync
ssh 192.168.20.92 yum -y install rsync
ssh 192.168.20.93 yum -y install rsync

scp /home/deploy/offline_setup/etcd/etcdadm 192.168.20.91:/usr/local/bin/ && ssh 192.168.20.91 chmod +x /usr/local/bin/etcdadm
scp /home/deploy/offline_setup/etcd/etcdadm 192.168.20.92:/usr/local/bin/ && ssh 192.168.20.92 chmod +x /usr/local/bin/etcdadm
scp /home/deploy/offline_setup/etcd/etcdadm 192.168.20.93:/usr/local/bin/ && ssh 192.168.20.93 chmod +x /usr/local/bin/etcdadm

ssh 192.168.20.91 mkdir -p /var/cache/etcdadm/etcd/v3.3.8
ssh 192.168.20.92 mkdir -p /var/cache/etcdadm/etcd/v3.3.8
ssh 192.168.20.93 mkdir -p /var/cache/etcdadm/etcd/v3.3.8

scp /home/deploy/offline_setup/etcd/etcd-v3.3.8-linux-amd64.tar.gz 192.168.20.91:/var/cache/etcdadm/etcd/v3.3.8
scp /home/deploy/offline_setup/etcd/etcd-v3.3.8-linux-amd64.tar.gz 192.168.20.92:/var/cache/etcdadm/etcd/v3.3.8
scp /home/deploy/offline_setup/etcd/etcd-v3.3.8-linux-amd64.tar.gz 192.168.20.93:/var/cache/etcdadm/etcd/v3.3.8

ssh 192.168.20.91 etcdadm init
ssh 192.168.20.91 rsync -avR /etc/etcd/pki/ca.* 192.168.20.92:/
ssh 192.168.20.91 rsync -avR /etc/etcd/pki/ca.* 192.168.20.93:/

ssh 192.168.20.92 etcdadm join https://192.168.20.91:2379
ssh 192.168.20.93 etcdadm join https://192.168.20.91:2379

# 校验etcd集群
/opt/bin/etcdctl.sh member list


```

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

###### 离线安装 docker

```ruby
ssh 192.168.20.91 mkdir -p /home/deploy/offline_setup/rpm-lib/docker/
ssh 192.168.20.92 mkdir -p /home/deploy/offline_setup/rpm-lib/docker/
ssh 192.168.20.93 mkdir -p /home/deploy/offline_setup/rpm-lib/docker/
ssh 192.168.20.94 mkdir -p /home/deploy/offline_setup/rpm-lib/docker/

scp /home/deploy/offline_setup/rpm-lib/docker 192.168.20.91:/home/deploy/offline_setup/rpm-lib/
scp /home/deploy/offline_setup/rpm-lib/docker 192.168.20.92:/home/deploy/offline_setup/rpm-lib/
scp /home/deploy/offline_setup/rpm-lib/docker 192.168.20.93:/home/deploy/offline_setup/rpm-lib/
scp /home/deploy/offline_setup/rpm-lib/docker 192.168.20.94:/home/deploy/offline_setup/rpm-lib/

rpm -ivh /home/deploy/offline_setup/rpm-lib/docker/* --force --nodeps

systemctl start docker && systemctl enable docker && systemctl status docker

```

- - - - - -

###### 将本地镜像文件拷贝至各主机

```ruby
ssh 192.168.20.91 mkdir -p /home/deploy/offline_setup/images/
ssh 192.168.20.92 mkdir -p /home/deploy/offline_setup/images/
ssh 192.168.20.93 mkdir -p /home/deploy/offline_setup/images/
ssh 192.168.20.94 mkdir -p /home/deploy/offline_setup/images/

scp /home/deploy/offline_setup/images 192.168.20.91:/home/deploy/offline_setup/
scp /home/deploy/offline_setup/images 192.168.20.92:/home/deploy/offline_setup/
scp /home/deploy/offline_setup/images 192.168.20.93:/home/deploy/offline_setup/
scp /home/deploy/offline_setup/images 192.168.20.94:/home/deploy/offline_setup/


```

- - - - - -

- - - - - -

- - - - - -

###### 离线安装 kubeadm、kubelet、kubectl

```ruby
ssh 192.168.20.91 mkdir -p /home/deploy/offline_setup/rpm-lib/k8s/
ssh 192.168.20.92 mkdir -p /home/deploy/offline_setup/rpm-lib/k8s/
ssh 192.168.20.93 mkdir -p /home/deploy/offline_setup/rpm-lib/k8s/
ssh 192.168.20.94 mkdir -p /home/deploy/offline_setup/rpm-lib/k8s/

scp /home/deploy/offline_setup/rpm-lib/k8s 192.168.20.91:/home/deploy/offline_setup/rpm-lib/
scp /home/deploy/offline_setup/rpm-lib/k8s 192.168.20.92:/home/deploy/offline_setup/rpm-lib/
scp /home/deploy/offline_setup/rpm-lib/k8s 192.168.20.93:/home/deploy/offline_setup/rpm-lib/
scp /home/deploy/offline_setup/rpm-lib/k8s 192.168.20.95:/home/deploy/offline_setup/rpm-lib/

rpm -ivh /home/deploy/offline_setup/rpm-lib/k8s/* --force --nodeps

systemctl start kubelet && systemctl enable kubelet && systemctl status kubelet

```

- - - - - -

##### 在所有 master、worker 节点配置

```ruby
cat > /etc/sysctl.d/k8s.conf  /proc/sys/net/bridge/bridge-nf-call-iptables
echo 'KUBELET_EXTRA_ARGS=--fail-swap-on=false' > /etc/sysconfig/kubelet

```

- - - - - -

##### 安装 master

###### 创建`kubeadm`配置文件

```ruby
cat > kubeadm-init.yaml 
```

- - - - - -

###### 安装 k8s master, 它是先装好一个master，然后在用命令添加其它节点为master

`所有 master节点先上传所依赖的docker镜像`  
`kubeadm init --config=kubeadm-init.yaml`

```ruby
[root@master1 ~]# kubeadm init --config=kubeadm-init.yaml
[init] Using Kubernetes version: v1.16.6
...... 省略
[control-plane] Creating static Pod manifest for "kube-scheduler"
[wait-control-plane] Waiting for the kubelet to boot up the control plane as static Pods from directory "/etc/kubernetes/manifests". This can take up to 4m0s
[apiclient] All control plane components are healthy after 37.012487 seconds
...... 省略
[bootstrap-token] Creating the "cluster-info" ConfigMap in the "kube-public" namespace
[kubelet-check] Initial timeout of 40s passed.
[addons] Applied essential addon: CoreDNS
[addons] Applied essential addon: kube-proxy

Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p <span class="katex math inline">HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf</span>HOME/.kube/config
  sudo chown <span class="katex math inline">(id -u):</span>(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

You can now join any number of control-plane nodes by copying certificate authorities
and service account keys on each node and then running the following as root:

  # 使用此命令来添加 master (要先推送k8s证书)
  kubeadm join 192.168.20.97:6443 --token b100tp.p9851f68jrkqadx0 \
    --discovery-token-ca-cert-hash sha256:59606d87b0c9cb5020d1395cc8f1e9714f3a46c255993a1da76c9359d9b76c7e \
    --control-plane

Then you can join any number of worker nodes by running the following on each as root:

  # 使用此命令来添加 worker
  kubeadm join 192.168.20.97:6443 --token b100tp.p9851f68jrkqadx0 \
    --discovery-token-ca-cert-hash sha256:59606d87b0c9cb5020d1395cc8f1e9714f3a46c255993a1da76c9359d9b76c7e

[root@master1 ~]#


```

###### 添加master节点需要证书, 将证书发给其它 master节点

```ruby
ssh 192.168.20.91 rsync -avR /etc/kubernetes/pki/* 192.168.20.92:/
ssh 192.168.20.92 rm -rf /etc/kubernetes/pki/apiserver*

ssh 192.168.20.91 rsync -avR /etc/kubernetes/pki/* 192.168.20.93:/
ssh 192.168.20.93 rm -rf /etc/kubernetes/pki/apiserver*

```

- - - - - -

###### 添加 master节点

```ruby
[root@master2 ~]# kubeadm join 192.168.20.97:6443 --token b100tp.p9851f68jrkqadx0 \
    --discovery-token-ca-cert-hash sha256:59606d87b0c9cb5020d1395cc8f1e9714f3a46c255993a1da76c9359d9b76c7e \
    --control-plane


[root@master3 ~]# kubeadm join 192.168.20.97:6443 --token b100tp.p9851f68jrkqadx0 \
    --discovery-token-ca-cert-hash sha256:59606d87b0c9cb5020d1395cc8f1e9714f3a46c255993a1da76c9359d9b76c7e \
    --control-plane

```

- - - - - -

###### 安装 网络插件

```ruby
[root@master1 ~]# kubectl apply -f /home/deploy/offline_setup/yaml/canal.yaml

```

- - - - - -

###### 查看结果

```ruby
[root@master1 ~]# kubectl get nodes
NAME         STATUS   ROLES    AGE     VERSION
master1      Ready    master   7m39s   v1.16.6
master2      Ready    master   3m4s    v1.16.6
master3      Ready    master   2m54s   v1.16.6
[root@master1 ~]#

```

- - - - - -

- - - - - -

- - - - - -

###### 添加 worker节点

`所有 worker节点先上传所依赖的docker镜像`

```ruby
[root@worker ~]# kubeadm join 192.168.20.97:6443 --token b100tp.p9851f68jrkqadx0 \
    --discovery-token-ca-cert-hash sha256:59606d87b0c9cb5020d1395cc8f1e9714f3a46c255993a1da76c9359d9b76c7e


[root@worker ~]# kubectl get nodes
NAME         STATUS   ROLES    AGE     VERSION
master1      Ready    master   7m39s   v1.16.6
master2      Ready    master   3m4s    v1.16.6
master3      Ready    master   2m54s   v1.16.6
worker       Ready    <none>   15m     v1.16.6
[root@worker ~]#
</none>
```

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -