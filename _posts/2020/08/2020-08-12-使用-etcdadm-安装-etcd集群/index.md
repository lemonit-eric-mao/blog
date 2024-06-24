---
title: "使用 etcdadm 安装 etcd集群"
date: "2020-08-12"
categories: 
  - "k8s"
---

##### 前置资料

**[ETCD中文官网](https://etcd.cn/ "ETCD中文官网")**

##### **etcd是什么?**

- **`etcd`** 是用Go语言编写的，它具有出色的跨平台支持，小的二进制文件和强大的社区。
    
    - etcd机器之间的通信通过 **`Raft`共识算法** 处理。

  

- **`etcd`** 是一个**高度一致**的**分布式键值存储**
    
    - 它提供了一种可靠的方式来存储需要由分布式系统或机器集群访问的数据。它可以优雅地处理网络分区期间的领导者选举，即使在领导者节点中也可以容忍机器故障。

  

- 从简单应用程序到Kubernetes到任何复杂性的应用程序都可以从etcd中读写数据。

  

- 您的应用程序可以读取和写入etcd中的数据。
    
    - 一个简单的用例是将数据库连接详细信息或功能标志存储在etcd中作为键值对。
    - 可以观察这些值，使您的应用在更改时可以重新配置自己。
    - 高级用途**利用etcd的一致性**保证来实施 **数据库`领导者选举`** 或跨一组工作人员执行**分布式`锁`**定。

  

- etcd是开源的，可在GitHub上获得。

* * *

* * *

* * *

###### **[官方建议使用 etcdadm 安装etcd](https://kubernetes.io/zh/docs/setup/production-environment/tools/kubeadm/setup-ha-etcd-with-kubeadm/ "官方建议使用 etcdadm 安装etcd")**

###### **[官方 github](https://github.com/kubernetes-sigs/etcdadm "官方 github")**

* * *

###### **[安装 go 环境](http://www.dev-share.top/2018/09/20/go-%e8%af%ad%e8%a8%80%e5%85%a5%e9%97%a8/ "安装 go 环境")**

* * *

###### 机器环境

| IP地址 | 节点 |
| --- | --- |
| 192.168.2.11 | etcd1 |
| 192.168.2.12 | etcd2 |
| 192.168.2.13 | etcd3 |

* * *

###### go的资源包默认在`谷歌云`上面

**默认使用的是`proxy.golang.org`，在国内无法访问** **使用国内代理地址：`https://goproxy.cn`**

```ruby
[root@k8s-etcd1 etcdadm-0.1.3]# go env -w GOPROXY=https://goproxy.cn
```

**然后在`重新执行命令`即可**

* * *

###### 安装依赖工具 所有节点 **(`etcd1、etcd2、etcd3`)**

```ruby
yum -y install rsync
```

* * *

###### 下载

```ruby
wget https://github.com/kubernetes-sigs/etcdadm/archive/v0.1.3.zip

unzip v0.1.3.zip

cd /etcdadm-0.1.3

```

* * *

###### 制作 `etcdadm`, 在哪台机器上制作都可以

```ruby
# 需要有git 脚本中有依赖
[root@dev etcdadm-0.1.3]# yum -y install git

# 在主机上构建 etcdadm
[root@dev etcdadm-0.1.3]# make etcdadm
```

* * *

###### 复制`etcdadm`到 **(`etcd1、etcd2、etcd3`)** 节点机的`/usr/local/bin/` 目录中并授权

```ruby
[root@dev etcdadm-0.1.3]# scp etcdadm 192.168.2.11:/usr/local/bin/
[root@dev etcdadm-0.1.3]# scp etcdadm 192.168.2.12:/usr/local/bin/
[root@dev etcdadm-0.1.3]# scp etcdadm 192.168.2.13:/usr/local/bin/
```

###### 或者使用这里有打包好的上传到七牛云的: **[etcdadm-0.1.3版本](http://qiniu.dev-share.top/etcdadm "etcdadm-0.1.3版本")**

```ruby
wget http://qiniu.dev-share.top/etcdadm -P /usr/local/bin/ && chmod +x /usr/local/bin/etcdadm

etcdadm version

```

* * *

* * *

* * *

##### 安装

###### 下载 etcd到每个节点机 **(`etcd1、etcd2、etcd3`)** 两种做法

`etcdadm download --help`

```ruby
# 第1种 使用 `etcdadm download --version 指定版本` 它会自动从 https://github.com/coreos/etcd/releases/download 下载
[root@k8s-etcd1 ~]# etcdadm download --version 3.3.8

# 第2种 从自己的云存储下载
[root@k8s-etcd1 ~]# mkdir -p /var/cache/etcdadm/etcd/v3.3.8
[root@k8s-etcd1 ~]# wget http://qiniu.dev-share.top/etcd-v3.3.8-linux-amd64.tar.gz -P /var/cache/etcdadm/etcd/v3.3.8
```

* * *

###### 随意选择一个etcd节点创建一个新的etcd服务，我这里选择在 **`etcd1`** 节点上面安装

```ruby
[root@k8s-etcd1 ~]# etcdadm init
INFO[0801] [install] extracting etcd archive /var/cache/etcdadm/etcd/v3.3.8/etcd-v3.3.8-linux-amd64.tar.gz to /tmp/etcd359496206
INFO[0801] [install] verifying etcd 3.3.8 is installed in /opt/bin/
INFO[0801] [certificates] creating PKI assets
INFO[0801] creating a self signed etcd CA certificate and key files
[certificates] Generated ca certificate and key.
INFO[0801] creating a new server certificate and key files for etcd
[certificates] Generated server certificate and key.
[certificates] server serving cert is signed for DNS names [k8s-etcd1] and IPs [192.168.2.11 127.0.0.1]
INFO[0802] creating a new certificate and key files for etcd peering
[certificates] Generated peer certificate and key.
[certificates] peer serving cert is signed for DNS names [k8s-etcd1] and IPs [192.168.2.11]
INFO[0802] creating a new client certificate for the etcdctl
[certificates] Generated etcdctl-etcd-client certificate and key.
INFO[0803] creating a new client certificate for the apiserver calling etcd
[certificates] Generated apiserver-etcd-client certificate and key.
[certificates] valid certificates and keys now exist in "/etc/etcd/pki"
INFO[0804] [health] Checking local etcd endpoint health
INFO[0804] [health] Local etcd endpoint is healthy
INFO[0804] To add another member to the cluster, copy the CA cert/key to its certificate dir and run:
INFO[0804]      etcdadm join https://192.168.2.11:2379
[root@k8s-etcd1 ~]#
```

* * *

###### 查看

```ruby
[root@k8s-etcd1 ~]# etcdadm info
{
  "ID": 15137820488843840845,
  "name": "k8s-etcd1",
  "peerURLs": [
    "https://192.168.2.11:2380"
  ],
  "clientURLs": [
    "https://192.168.2.11:2379"
  ]
}
```

* * *

###### 将etcd证书

`rsync -avR /etc/etcd/pki/ca.* <Member IP address>:/`

```ruby
[root@k8s-etcd1 ~]# rsync -avR /etc/etcd/pki/ca.* 192.168.2.12:/
root@192.168.2.12's password:
sending incremental file list
/etc/
/etc/etcd/
/etc/etcd/pki/
/etc/etcd/pki/ca.crt
/etc/etcd/pki/ca.key

[root@k8s-etcd1 ~]#



[root@k8s-etcd1 ~]# rsync -avR /etc/etcd/pki/ca.* 192.168.2.13:/
root@192.168.2.13's password:
sending incremental file list
/etc/
/etc/etcd/
/etc/etcd/pki/
/etc/etcd/pki/ca.crt
/etc/etcd/pki/ca.key

[root@k8s-etcd1 ~]#
```

* * *

###### 将 **`etcd2、etcd3`** 加入到集群中

```ruby
[root@k8s-etcd2 ~]# etcdadm join https://192.168.2.11:2379
INFO[0000] [certificates] creating PKI assets
INFO[0000] creating a self signed etcd CA certificate and key files
[certificates] Using the existing ca certificate and key.
INFO[0000] creating a new server certificate and key files for etcd
[certificates] Generated server certificate and key.
[certificates] server serving cert is signed for DNS names [k8s-etcd2] and IPs [192.168.2.12 127.0.0.1]
INFO[0000] creating a new certificate and key files for etcd peering
[certificates] Generated peer certificate and key.
[certificates] peer serving cert is signed for DNS names [k8s-etcd2] and IPs [192.168.2.12]
INFO[0001] creating a new client certificate for the etcdctl
[certificates] Generated etcdctl-etcd-client certificate and key.
INFO[0001] creating a new client certificate for the apiserver calling etcd
[certificates] Generated apiserver-etcd-client certificate and key.
[certificates] valid certificates and keys now exist in "/etc/etcd/pki"
INFO[0001] [membership] Checking if this member was added
INFO[0001] [membership] Member was not added
INFO[0001] Removing existing data dir "/var/lib/etcd"
INFO[0001] [membership] Adding member
INFO[0001] [membership] Checking if member was started
INFO[0001] [membership] Member was not started
INFO[0001] [membership] Removing existing data dir "/var/lib/etcd"
INFO[0001] [install] extracting etcd archive /var/cache/etcdadm/etcd/v3.3.8/etcd-v3.3.8-linux-amd64.tar.gz to /tmp/etcd355553877
INFO[0002] [install] verifying etcd 3.3.8 is installed in /opt/bin/
INFO[0002] [health] Checking local etcd endpoint health
INFO[0002] [health] Local etcd endpoint is healthy
[root@k8s-etcd2 ~]#



[root@k8s-etcd3 ~]# etcdadm join https://192.168.2.11:2379
INFO[0000] [certificates] creating PKI assets
INFO[0000] creating a self signed etcd CA certificate and key files
[certificates] Using the existing ca certificate and key.
INFO[0000] creating a new server certificate and key files for etcd
[certificates] Generated server certificate and key.
[certificates] server serving cert is signed for DNS names [k8s-etcd3] and IPs [192.168.2.13 127.0.0.1]
INFO[0000] creating a new certificate and key files for etcd peering
[certificates] Generated peer certificate and key.
[certificates] peer serving cert is signed for DNS names [k8s-etcd3] and IPs [192.168.2.13]
INFO[0001] creating a new client certificate for the etcdctl
[certificates] Generated etcdctl-etcd-client certificate and key.
INFO[0002] creating a new client certificate for the apiserver calling etcd
[certificates] Generated apiserver-etcd-client certificate and key.
[certificates] valid certificates and keys now exist in "/etc/etcd/pki"
INFO[0002] [membership] Checking if this member was added
INFO[0002] [membership] Member was not added
INFO[0002] Removing existing data dir "/var/lib/etcd"
INFO[0002] [membership] Adding member
INFO[0002] [membership] Checking if member was started
INFO[0002] [membership] Member was not started
INFO[0002] [membership] Removing existing data dir "/var/lib/etcd"
INFO[0002] [install] extracting etcd archive /var/cache/etcdadm/etcd/v3.3.8/etcd-v3.3.8-linux-amd64.tar.gz to /tmp/etcd303228048
INFO[0003] [install] verifying etcd 3.3.8 is installed in /opt/bin/
INFO[0003] [health] Checking local etcd endpoint health
INFO[0003] [health] Local etcd endpoint is healthy
[root@k8s-etcd3 ~]#
```

* * *

###### 验证

查看集群信息： `/opt/bin/etcdctl.sh member list` 查看etcd数据： `/opt/bin/etcdctl.sh get / --prefix --keys-only=true`

```ruby
[root@k8s-etcd1 bin]# /opt/bin/etcdctl.sh member list
261d38484d58b4ba, started, k8s-etcd1, https://192.168.2.11:2380, https://192.168.2.11:2379
d4a6ddd4490365cf, started, k8s-etcd2, https://192.168.2.12:2380, https://192.168.2.12:2379
41d704bff512e934, started, k8s-etcd3, https://192.168.2.13:2380, https://192.168.2.13:2379
[root@k8s-etcd1 bin]#
```

* * *

* * *

* * *

###### 卸载

```ruby
etcdadm reset
```
