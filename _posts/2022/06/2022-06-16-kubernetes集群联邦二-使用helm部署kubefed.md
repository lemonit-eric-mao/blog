---
title: "Kubernetes集群联邦(二)-使用Helm部署Kubefed"
date: "2022-06-16"
categories: 
  - "cloudnative"
  - "k8s"
---

##### 前置资料

1. **[Kubernetes集群联邦(一)-Federation V2 工作原理](kubernetes%e9%9b%86%e7%be%a4%e8%81%94%e9%82%a6%e4%b8%80-federation-v2-%e5%b7%a5%e4%bd%9c%e5%8e%9f%e7%90%86)**

**[官方文档安装Kubefed](https://github.com/kubernetes-sigs/kubefed/blob/master/docs/cluster-registration.md#joining-clusters)**

* * *

* * *

* * *

* * *

##### 前置条件

###### 集群01

> | 管理服务器 | IP地址 | 资源配置 | 功能 | 备注 |
> | --- | --- | --- | --- | --- |
> | k8s-master-01 | 12.3.4.11 | 4vCPU;8GB;100G+400G | k8s-v1.20.4 基于containerd部署 | CentOS7.9 内核：3.10以上 |
> | k8s-worker-01 | 12.3.4.12 | 4vCPU;8GB;100G+400G | k8s-v1.20.4 基于containerd部署 | CentOS7.9 内核：3.10以上 |
> | k8s-worker-02 | 12.3.4.13 | 4vCPU;8GB;100G+400G | k8s-v1.20.4 基于containerd部署 | CentOS7.9 内核：3.10以上 |
> | k8s-worker-03 | 12.3.4.14 | 4vCPU;8GB;100G+400G | k8s-v1.20.4 基于containerd部署 | CentOS7.9 内核：3.10以上 |

* * *

###### 集群02

> | 管理服务器 | IP地址 | 资源配置 | 功能 | 备注 |
> | --- | --- | --- | --- | --- |
> | k8s-master-01 | 12.3.4.15 | 4vCPU;8GB;100G+400G | k8s-v1.20.4 基于containerd部署 | CentOS7.9 内核：3.10以上 |
> | k8s-worker-01 | 12.3.4.16 | 4vCPU;8GB;100G+400G | k8s-v1.20.4 基于containerd部署 | CentOS7.9 内核：3.10以上 |
> | k8s-worker-02 | 12.3.4.17 | 4vCPU;8GB;100G+400G | k8s-v1.20.4 基于containerd部署 | CentOS7.9 内核：3.10以上 |
> | k8s-worker-03 | 12.3.4.18 | 4vCPU;8GB;100G+400G | k8s-v1.20.4 基于containerd部署 | CentOS7.9 内核：3.10以上 |

* * *

* * *

* * *

##### 使用Helm部署Kubefed

###### 首先，将 **KubeFed Chart** 存储库添加到本地存储库

```ruby
helm repo add kubefed-charts https://raw.githubusercontent.com/kubernetes-sigs/kubefed/master/charts

"kubefed-charts" has been added to your repositories
[root@k8s-master-01 siyu.mao]#

## 查看本地存储库列表
helm repo list
NAME            URL
kubefed-charts  https://raw.githubusercontent.com/kubernetes-sigs/kubefed/master/charts
[root@k8s-master-01 siyu.mao]#
```

* * *

###### 添加 repo 后，可以查看可用的**Chart**和版本

```ruby
helm search repo kubefed
NAME                    CHART VERSION   APP VERSION     DESCRIPTION
kubefed-charts/kubefed  0.9.2                           KubeFed helm chart
[root@k8s-master-01 siyu.mao]#
```

- 安装图表并使用`--version`参数指定要安装的版本。替换`<x.x.x>`为您想要的版本。
- 如果您不想安装 `CRD`，请在行尾添加`--skip-crds`。
- 为了方便调配，这里选择将**Chart**包下载到本地，也可以使用在线方式安装**[参考官方做法](https://github.com/kubernetes-sigs/kubefed/tree/master/charts/kubefed#installing-the-chart)**

* * *

###### 将**Chart**包下载到本地

```ruby
helm pull kubefed-charts/kubefed --version 0.9.2

## 查看下载成功后的文件
ll
kubefed-0.9.2.tgz

```

* * *

###### 基于**Chart**包部署，在`每个`集群上安装

```ruby
helm install kubefed ./kubefed-0.9.2.tgz \
    --namespace kube-federation-system \
    --create-namespace

```

**注：** `--set global.scope=` **[参考官方配置说明](https://github.com/kubernetes-sigs/kubefed/tree/master/charts/kubefed#configuration)**

| 参数 | 描述 | 默认值 |
| :-: | :-- | :-: |
| global.scope | KubeFed 命名空间是否将是控制平面的唯一目标。可选值为`Cluster`，`Namespaced`。  
经过初步测试，**k8s 1.20.x在使用`--set global.scope=Namespaced`时各个集群无法触发部署工作** | **Cluster** |

- 安装过程中，如果因镜像下载慢，可能会导致部署失败。
- 如果程序启动失败需要多等待一些时间，然后重新部署，这期间可能会反复部署。
    
    - 异常信息如：
        
        - `Stream closed EOF for kube-federation-system/kubefed-controller-manager-xxxxxx-xxx (controller-manager)`
        - `Stream closed EOF for kube-federation-system/kubefed-xxxxxx-xxx (post-install-job)`
- 成功后控制台会输出如下信息

```ruby
NAME: kubefed
LAST DEPLOYED: Thu Jun 16 11:11:57 2022
NAMESPACE: kube-federation-system
STATUS: deployed
REVISION: 1
TEST SUITE: None

```

**注：** 还可以通过 `helm show values kubefed-charts/kubefed` 命令查看具体的 **values** 配置方法

* * *

###### 标签确认

- 要确保你的命名空间已经添加了 **Label** `name: <namespace>`
    
    - 使用 `kubectl get ns 你的namespace --show-labels` 进行确认
- 这个标签对于获得对 KubeFed 核心 API 的正确验证**`是必要`**的。
- 如果命名空间尚不存在，该helm install命令将默认使用此标签创建命名空间。

```ruby
kubectl get ns kube-federation-system --show-labels

NAME                     STATUS   AGE   LABELS
kube-federation-system   Active   32m   name=kube-federation-system

```

* * *

* * *

* * *

##### 卸载**Chart**

**删除所有`KubeFed FederatedTypeConfig`**

```ruby
kubectl -n kube-federation-system delete FederatedTypeConfig --all

```

**删除与 Chart 关联的所有 Kubernetes 组件并删除版本**

```ruby
helm --namespace kube-federation-system uninstall kubefed

```

* * *

* * *

* * *

##### 最后

> - 到此，KubeFed 在集群中的安装部署已经完成，接下来，需要了解，我们如何去使用它 **[Kubernetes集群联邦(三)-使用kubefedctl注册集群联邦](kubernetes%e9%9b%86%e7%be%a4%e8%81%94%e9%82%a6%e4%b8%89-%e4%bd%bf%e7%94%a8kubefedctl%e6%b3%a8%e5%86%8c%e9%9b%86%e7%be%a4%e8%81%94%e9%82%a6)**

* * *

* * *

* * *

## 系列导航

1. **[Kubernetes集群联邦(一)-Federation V2 工作原理](kubernetes%e9%9b%86%e7%be%a4%e8%81%94%e9%82%a6%e4%b8%80-federation-v2-%e5%b7%a5%e4%bd%9c%e5%8e%9f%e7%90%86)**
2. **[Kubernetes集群联邦(二)-使用Helm部署Kubefed](kubernetes%e9%9b%86%e7%be%a4%e8%81%94%e9%82%a6%e4%ba%8c-%e4%bd%bf%e7%94%a8helm%e9%83%a8%e7%bd%b2kubefed)**
3. **[Kubernetes集群联邦(三)-使用kubefedctl注册集群联邦](kubernetes%e9%9b%86%e7%be%a4%e8%81%94%e9%82%a6%e4%b8%89-%e4%bd%bf%e7%94%a8kubefedctl%e6%b3%a8%e5%86%8c%e9%9b%86%e7%be%a4%e8%81%94%e9%82%a6)**
4. **[Kubernetes集群联邦(四)-使用kubefedctl统一管理联邦集群](kubernetes%e9%9b%86%e7%be%a4%e8%81%94%e9%82%a6%e5%9b%9b-%e4%bd%bf%e7%94%a8kubefedctl%e7%bb%9f%e4%b8%80%e7%ae%a1%e7%90%86%e8%81%94%e9%82%a6%e9%9b%86%e7%be%a4)**

* * *

* * *

* * *
