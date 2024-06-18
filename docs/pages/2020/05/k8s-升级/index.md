---
title: "K8S 升级"
date: "2020-05-01"
categories: 
  - "k8s"
---

##### **v`1.13.0` --> v`1.14.2`**

* * *

K8S 升级可以跨小版本，但是不能跨大版本升级，只能一个大版本一个大版本的升级 **v`1.13.0` --> v`1.14.2`** **正确** **v`1.13.0` --> v`1.17.0`** **`错误`**

* * *

###### 安全版本

- v1.16.11+
- v1.17.7+
- v1.18.4+

* * *

* * *

* * *

##### 1 升级 kubeadm (所有节点都执行kubeadm升级)

```ruby
# 查看当前集群版本
[root@test1 ~]# kubectl get nodes
NAME    STATUS   ROLES    AGE   VERSION
test1   Ready    master   11d   v1.13.0
test2   Ready    <none>   10d   v1.13.0
test3   Ready    <none>   10d   v1.13.0
test4   Ready    <none>   10d   v1.13.0
[root@test1 ~]#

# 查看当前 k8s 版本
[root@test1 ~]# kubeadm version
kubeadm version: &version.Info{Major:"1", Minor:"13", GitVersion:"v1.13.0", GitCommit:"ddf47ac13c1a9483ea035a79cd7c10005ff21a6d", GitTreeState:"clean", BuildDate:"2018-12-03T21:02:01Z", GoVersion:"go1.11.2", Compiler:"gc", Platform:"linux/amd64"}
[root@test1 ~]#

# 查看仓库集群版本
[root@test1 ~]# yum list --showduplicates kubeadm --disableexcludes=kubernetes
[root@test1 ~]#

# 升级kubeadm版本及查看集群是否满足升级需求
[root@test1 ~]# yum install -y kubeadm-1.14.2
[root@test1 ~]#

# 查看升级后的 kubeadm 版本
[root@test1 ~]# kubeadm version
kubeadm version: &version.Info{Major:"1", Minor:"14", GitVersion:"v1.14.2", GitCommit:"641856db18352033a0d96dbc99153fa3b27298e5", GitTreeState:"clean", BuildDate:"2019-03-25T15:51:21Z", GoVersion:"go1.12.1", Compiler:"gc", Platform:"linux/amd64"}
[root@test1 ~]#
```

* * *

##### 2 检查集群是否可升级

```ruby
# 查看集群是否可以升级，升级后各组件的版本信息
[root@test1 ~]# kubeadm upgrade plan 1.14.2
"[preflight] Running pre-flight checks.
[upgrade] Making sure the cluster is healthy:
[upgrade/config] Making sure the configuration is correct:
[upgrade/config] Reading configuration from the cluster...
[upgrade/config] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -oyaml'
[upgrade] Fetching available versions to upgrade to
[upgrade/versions] Cluster version: v1.13.0
[upgrade/versions] kubeadm version: v1.14.2

Components that must be upgraded manually after you have upgraded the control plane with 'kubeadm upgrade apply':
COMPONENT   CURRENT       AVAILABLE
Kubelet     4 x v1.13.0   1.14.2

Upgrade to the latest version in the v1.13 series:

# 注意，这里是将要替换的 镜像版本
COMPONENT            CURRENT   AVAILABLE
API Server           v1.13.0   1.14.2
Controller Manager   v1.13.0   1.14.2
Scheduler            v1.13.0   1.14.2
Kube Proxy           v1.13.0   1.14.2
CoreDNS              1.2.6     1.3.1
Etcd                 3.2.24    3.3.10

You can now apply the upgrade by executing the following command:

        kubeadm upgrade apply 1.14.2

_____________________________________________________________________

[root@test1 ~]#
```

* * *

##### 3 根据 上面给出的提示信息，下载相应的镜像

```ruby
cat > download_image.sh << eric
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

eric

```

```ruby
# 执行脚本 下载镜像
[root@test1 ~]# ./download_image.sh
```

##### 4 升级 k8s Server

```ruby
[root@test1 ~]# kubeadm upgrade apply 1.14.2 -y

...... 此处省略

[upgrade/successful] SUCCESS! Your cluster was upgraded to "v1.14.2". Enjoy!

[upgrade/kubelet] Now that your control plane is upgraded, please proceed with upgrading your kubelets if you haven't already done so.
[root@test1 ~]#

```

* * *

##### 5 升级 kubeadm、kubelet、kubectl (**`所有node节点`**)

```ruby
yum install -y kubeadm-1.14.2 kubelet-1.14.2 kubectl-1.14.2
# 重新加载
systemctl daemon-reload && systemctl restart kubelet
```

###### 升级**`所有node节点`**的相关镜像

```ruby
cat > download_image.sh << eric
#!/bin/bash
# 定义镜像集合数组
images=(
    kube-proxy:v1.14.2
    pause:3.1
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

eric

```

```ruby
# 执行脚本 下载镜像
[root@test1 ~]# ./download_image.sh
```

* * *

###### 查看升级后的集群

```ruby
[root@test1 ~]# kubectl get nodes
NAME    STATUS     ROLES    AGE   VERSION
test1   Ready      master   11d   v1.14.2
test2   Ready      <none>   10d   v1.14.2
test3   Ready      <none>   10d   v1.14.2
test4   Ready      <none>   10d   v1.14.2
[root@test1 ~]#
[root@test1 ~]#
[root@test1 ~]#
[root@test1 ~]# kubectl version
Client Version: version.Info{Major:"1", Minor:"14", GitVersion:"v1.14.2", GitCommit:"66049e3b21efe110454d67df4fa62b08ea79a19b", GitTreeState:"clean", BuildDate:"2019-05-16T16:23:09Z", GoVersion:"go1.12.5", Compiler:"gc", Platform:"linux/amd64"}
Server Version: version.Info{Major:"1", Minor:"14", GitVersion:"v1.14.2", GitCommit:"66049e3b21efe110454d67df4fa62b08ea79a19b", GitTreeState:"clean", BuildDate:"2019-05-16T16:14:56Z", GoVersion:"go1.12.5", Compiler:"gc", Platform:"linux/amd64"}
[root@test1 ~]#
```

* * *

* * *

* * *

###### 常见问题

```ruby
# 查看当前 k8s 版本
[root@test1 ~]# kubectl version
Client Version: version.Info{Major:"1", Minor:"13", GitVersion:"v1.13.0", GitCommit:"ddf47ac13c1a9483ea035a79cd7c10005ff21a6d", GitTreeState:"clean", BuildDate:"2018-12-03T21:04:45Z", GoVersion:"go1.11.2", Compiler:"gc", Platform:"linux/amd64"}
Server Version: version.Info{Major:"1", Minor:"13", GitVersion:"v1.13.0", GitCommit:"ddf47ac13c1a9483ea035a79cd7c10005ff21a6d", GitTreeState:"clean", BuildDate:"2018-12-03T20:56:12Z", GoVersion:"go1.11.2", Compiler:"gc", Platform:"linux/amd64"}
[root@test1 ~]#
[root@test1 ~]#
# 检查当前 版本的 k8s 是否可以升级到 指定的版本 （1.17.0）
[root@test1 ~]# kubeadm upgrade plan 1.17.0
[preflight] Running pre-flight checks.
[upgrade] Making sure the cluster is healthy:
[upgrade/config] Making sure the configuration is correct:
[upgrade/config] Reading configuration from the cluster...
[upgrade/config] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -oyaml'
[upgrade] Fetching available versions to upgrade to
[upgrade/versions] Cluster version: v1.13.0
[upgrade/versions] kubeadm version: v1.13.0
[upgrade/versions] WARNING: No recommended etcd for requested Kubernetes version (1.17.0)

Components that must be upgraded manually after you have upgraded the control plane with 'kubeadm upgrade apply':
COMPONENT   CURRENT       AVAILABLE
Kubelet     4 x v1.13.0   1.17.0

Upgrade to the latest version in the v1.13 series:

COMPONENT            CURRENT   AVAILABLE
API Server           v1.13.0   1.17.0
Controller Manager   v1.13.0   1.17.0
Scheduler            v1.13.0   1.17.0
Kube Proxy           v1.13.0   1.17.0
CoreDNS              1.2.6     1.2.6
Etcd                 3.2.24    N/A

You can now apply the upgrade by executing the following command:

        kubeadm upgrade apply 1.17.0

Note: Before you can perform this upgrade, you have to update kubeadm to 1.17.0.

_____________________________________________________________________

[root@test1 ~]#
[root@test1 ~]#
# 根据提示，进行升级
[root@test1 ~]# kubeadm upgrade apply 1.17.0[preflight] Running pre-flight checks.
[upgrade] Making sure the cluster is healthy:
[upgrade/config] Making sure the configuration is correct:
[upgrade/config] Reading configuration from the cluster...
[upgrade/config] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -oyaml'
[upgrade/apply] Respecting the --cri-socket flag that is set with higher priority than the config file.
[upgrade/version] You have chosen to change the cluster version to "v1.17.0"
[upgrade/versions] Cluster version: v1.13.0
[upgrade/versions] kubeadm version: v1.13.0
[upgrade/version] FATAL: the --version argument is invalid due to these fatal errors:

        # -升级到“ v1.17.0”的指定版本太高； kubeadm一次只能升级1个次要版本
        - Specified version to upgrade to "v1.17.0" is too high; kubeadm can upgrade only 1 minor version at a time

        # -升级到“ v1.17.0”的指定版本至少比kubeadm次要版本（17> 13）高一个次要版本。不支持这种升级
        - Specified version to upgrade to "v1.17.0" is at least one minor release higher than the kubeadm minor release (17 > 13). Such an upgrade is not supported

Please fix the misalignments highlighted above and try upgrading again
[root@test1 ~]#
```

* * *

* * *

* * *

##### kubelet 版本突然升级到最高

```ruby
[root@test1 ~]# kubectl get nodes
NAME    STATUS     ROLES    AGE   VERSION
test1   NotReady   master   11d   v1.18.2
test2   Ready      <none>   10d   v1.14.2
test3   Ready      <none>   10d   v1.14.2
test4   Ready      <none>   10d   v1.14.2
[root@test1 ~]#

# 删除原 kubelet
[root@test1 ~]# yum remove -y kubelet
[root@test1 ~]#
[root@test1 ~]#
# 重新安装
[root@test1 ~]# yum install -y kubelet-1.14.2 kubeadm-1.14.2 kubectl-1.14.2
[root@test1 ~]#
[root@test1 ~]#
# 重新启动
[root@test1 ~]# systemctl start kubelet && systemctl status kubelet && systemctl enable kubelet

```

* * *
