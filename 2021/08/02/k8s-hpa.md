---
title: 'K8S HPA'
date: '2021-08-02T08:27:57+00:00'
status: publish
permalink: /2021/08/02/k8s-hpa
author: 毛巳煜
excerpt: ''
type: post
id: 7635
category:
    - Kubernetes
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
#### 前置条件

###### **[创建 Horizontal Pod Autoscaler](https://kubernetes.io/zh/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/#create-horizontal-pod-autoscaler "创建 Horizontal Pod Autoscaler")**

> - 需要注意的是，`targetCPUUtilizationPercentage` 字段已经被名为 `metrics` 的数组所取代。 `CPU` 利用率这个度量指标是一个 `resource metric`（资源度量指标），因为它表示容器上指定资源的百分比。 除 `CPU` 外，你还可以指定其他资源度量指标。默认情况下，目前唯一支持的其他资源度量指标为内存。 只要 `metrics.k8s.io API` 存在，这些资源度量指标就是可用的，并且他们不会在不同的 `Kubernetes` 集群中改变名称。

###### **[Pod水平自动伸缩](https://kubernetes.io/zh/docs/tasks/run-application/horizontal-pod-autoscale/ "Pod水平自动伸缩")**

> - **水平扩缩意味着对`增加的负载`的响应**是部署更多的 Pods。 **这与 `垂直（Vertical）` 扩缩不同**，对于 Kubernetes， 垂直扩缩意味着将更多资源（例如：内存或 CPU）分配给已经为工作负载运行的 Pod。
> - Kubernetes 将水平 Pod 自动扩缩实现为一个间歇运行的控制回路（它不是一个连续的过程）。  
>    间隔由 **`kube-controller-manager`** 的 **`--horizontal-pod-autoscaler-sync-period`** 参数设置（默认间隔为 **`15`** 秒）。

###### **必须依赖： [K8S 容器性能指标 metrics-server](http://www.dev-share.top/2020/10/25/k8s-%e5%ae%b9%e5%99%a8%e6%80%a7%e8%83%bd%e6%8c%87%e6%a0%87-metrics-server/ "K8S 容器性能指标 metrics-server")**

###### **Kubernetes v1.23: [可配置的扩缩行为](https://kubernetes.io/zh/docs/tasks/run-application/horizontal-pod-autoscale/#configurable-scaling-behavior "可配置的扩缩行为")**

- - - - - -

- - - - - -

- - - - - -

#### 通过**压测`CPU`**来验证**HPA**

###### 1. 创建部署压测程序的yaml文件

```ruby
cat > php-apache.yaml 
```

- - - - - -

###### 2. 创建部署HPA的yaml文件

```ruby
cat > php-apache-autoscale.yaml 
```

- - - - - -

###### 3. 开始测试，执行测试命令

```ruby
kubectl run -i --tty load-generator --rm --image=busybox:1.28 --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://php-apache; done"

```

- - - - - -

- - - - - -

- - - - - -

#### 通过**压测`内存`**来验证**HPA**

###### 1. 创建部署压测程序的yaml文件

```ruby
cat > iris-server-stress.yaml 
```

- - - - - -

###### 2. 创建部署HPA的yaml文件

```ruby
cat > iris-server-stress-autoscale.yaml 
```

- - - - - -

###### 3. 开始测试，执行测试命令

```ruby
## 不会触发扩容
curl http://localhost:30808/v1/stressMEM?mem=512

## 会触发扩容
curl http://localhost:30808/v1/stressMEM?mem=1433

```

- - - - - -

###### 结论

> - 从测试结果可以确定，**HPA**的扩容指标是参照容器资源.资源请求限制的数值，做为百分比的参考；
> - 因此我们运行应用程序的虚拟机的资源限制，不要小于 **containers.resources.`requests.memory`** 这个数值，更不能超出 **containers.resources.`limits.memory`** 这个数值，否则会 **`内存溢出`** 。

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

#### **`教学`** 自定义，创建测试程序

###### 可以使用kubectl命令生成`Deployment`模板(`新手学习`)

```ruby
kubectl create deploy container-pressure-test --image=polinux/stress:1.0.4 --dry-run=client -o yaml > container-pressure-test.yaml

```

- - - - - -

###### 还可以直接创建**`Deployment`**模板(`推荐使用`)

```ruby
cat > container-pressure-test.yaml 
```

- - - - - -

- - - - - -

- - - - - -

##### 创建`HPA`

###### 可以使用kubectl命令生成HPA模板(`新手学习`)

```ruby
kubectl autoscale deployment container-pressure-test --cpu-percent=5 --min=1 --max=10 --dry-run -o yaml > pressure-test-hpa.yaml

## 生成的文件内容如下
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  creationTimestamp: null
  name: container-pressure-test
spec:
  maxReplicas: 10
  minReplicas: 1
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: container-pressure-test
  targetCPUUtilizationPercentage: 5
status:
  currentReplicas: 0
  desiredReplicas: 0


```

- - - - - -

###### 还可以直接创建**`HPA`**模板(`推荐使用`)

**提示`HPA`**是要与你的工作负载进行绑定使用的

```ruby
cat > pressure-test-hpa.yaml 
```

- - - - - -

- - - - - -

- - - - - -

###### 说明

- 测试程序启动以后，它会执行一条CPU的压测命令，会给工作节点的CPU增加压力
- 之后启动HPA去监控这个工作负载，它会根据 `metrics-server` 返回的监控数据，自动调整测试程序的副本数

- - - - - -

- - - - - -

- - - - - -