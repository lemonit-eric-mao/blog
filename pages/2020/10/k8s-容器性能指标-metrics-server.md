---
title: "K8S 容器性能指标 metrics-server"
date: "2020-10-25"
categories: 
  - "k8s"
---

###### **[官方文档](https://kubernetes.io/zh/docs/tasks/debug-application-cluster/resource-metrics-pipeline/#metrics-server "官方文档")**

###### **[github](https://github.com/kubernetes-sigs/metrics-server "github")**

###### **[tags](https://github.com/kubernetes-sigs/metrics-server/tags "tags")**

##### **[Helm部署](https://artifacthub.io/packages/helm/metrics-server/metrics-server)**

* * *

###### 兼容性矩阵

| **指标服务器** | **指标 API 组/版本** | **支持的 Kubernetes 版本** |
| :-: | :-: | :-: |
| 0.6.x | metrics.k8s.io/v1beta1 | `1.19+` |
| 0.5.x | metrics.k8s.io/v1beta1 | `*1.8+` |

* * *

##### 使用七牛云资源安装

```ruby
kubectl apply -f http://qiniu.dev-share.top/kubernetes/metrics-server-v0.5.0-components.yaml
kubectl apply -f http://qiniu.dev-share.top/kubernetes/metrics-server-v0.6.0-components.yaml
```

* * *

###### 启动

```ruby
kubectl apply -f metrics-server-v0.5.0-components.yaml
kubectl apply -f metrics-server-v0.6.0-components.yaml
```

* * *

###### 测试

```ruby
###### 查看集群节点资源使用情况（CPU，MEM）
[root@master01 ~]# kubectl top nodes
NAME       CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
master01   813m         20%    3994Mi          51%
worker01   252m         6%     1896Mi          24%
worker02   281m         7%     1183Mi          15%
worker03   281m         7%     2321Mi          30%


###### 查看kube-system下所有pods资源使用情况
[root@master01 ~]# kubectl -n kube-system top pods
NAME                                       CPU(cores)   MEMORY(bytes)
calico-kube-controllers-59d85c5c84-qcvc4   3m           37Mi
canal-98rbx                                72m          89Mi
canal-d8ndx                                121m         42Mi
canal-hs244                                82m          76Mi
canal-k7pwb                                72m          87Mi
coredns-5644d7b6d9-45zxs                   15m          13Mi
coredns-5644d7b6d9-dbwkw                   22m          10Mi
etcd-master01                              83m          304Mi
kube-apiserver-master01                    293m         749Mi
kube-controller-manager-master01           144m         86Mi
kube-proxy-jj5ch                           1m           23Mi
kube-proxy-pshn8                           11m          26Mi
kube-proxy-rrsmp                           1m           24Mi
kube-proxy-tlwh7                           5m           20Mi
kube-scheduler-master01                    5m           25Mi
metrics-server-84894bf59c-bfb72            2m           13Mi
[root@master01 ~]#


###### 查看指定pod资源使用情况
[root@master01 ~]# kubectl -n kube-system top pods etcd-master01
NAME            CPU(cores)   MEMORY(bytes)
etcd-master01   100m         304Mi
[root@master01 ~]#
```

* * *

* * *

* * *

###### `解释说明 metrics-server-v0.x.x-components.yaml 文件`

对官方原有文件`components.yaml`做了如下修改

```yaml
......
    spec:
      containers:
      - args:
        - --cert-dir=/tmp
        - --secure-port=443
        - --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
        - --kubelet-use-node-status-port
        - --metric-resolution=15s

        # 加入以下改变，其它都没改。1.20.x以下使用
        # - --logtostderr
        # 不验证Kubelet提供的服务证书
        - --kubelet-insecure-tls
        #image: k8s.gcr.io/metrics-server/metrics-server:v0.5.0
        # 使用阿里云源
        image: registry.cn-qingdao.aliyuncs.com/cn-aliyun/metrics-server:v0.5.0
......

```

* * *

* * *

* * *
