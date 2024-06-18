---
title: "Helm 安装 Istio"
date: "2021-05-08"
categories: 
  - "istio"
---

###### 安装 istioctl 可执行程序

```ruby
wget https://github.com/istio/istio/releases/download/1.9.4/istio-1.9.4-linux-amd64.tar.gz

tar -zxvf istio-1.9.4-linux-amd64.tar.gz && cp istio-1.9.4/bin/istioctl /usr/local/bin/

```

* * *

###### 为 Istio 组件，创建命名空间 istio-system

```ruby
kubectl create namespace istio-system

```

* * *

###### 安装 Istio base chart，它包含了 Istio 控制平面用到的集群范围的资源

```ruby
helm install istio-base istio-1.9.4/manifests/charts/base -n istio-system

```

* * *

###### 安装 Istio discovery chart，它用于部署 istiod 服务

如果尚未启用第三方令牌，则需要额外配置的参数 `--set global.jwtPolicy=first-party-jwt`

```ruby
helm install istiod istio-1.9.4/manifests/charts/istio-control/istio-discovery \
    --set global.hub="docker.io/istio" \
    --set global.tag="1.9.4" \
    --set global.jwtPolicy=first-party-jwt \
    -n istio-system

```

* * *

###### (可选项) 安装 Istio 的入站网关 chart，它包含入站网关组件

如果尚未启用第三方令牌，则需要额外配置的参数 `--set global.jwtPolicy=first-party-jwt`

```ruby
helm install istio-ingress istio-1.9.4/manifests/charts/gateways/istio-ingress \
    --set global.hub="docker.io/istio" \
    --set global.tag="1.9.4" \
    --set global.jwtPolicy=first-party-jwt \
    -n istio-system

```

* * *

###### (可选项) 安装 Istio 的出站网关 chart，它包含了出站网关组件

如果尚未启用第三方令牌，则需要额外配置的参数 `--set global.jwtPolicy=first-party-jwt`

```ruby
helm install istio-egress istio-1.9.4/manifests/charts/gateways/istio-egress \
    --set global.hub="docker.io/istio" \
    --set global.tag="1.9.4" \
    --set global.jwtPolicy=first-party-jwt \
    -n istio-system

```

* * *

* * *

* * *

###### 验证安装

```ruby
[root@master01 ~]#  kubectl get svc,pods -n istio-system
NAME                           TYPE           CLUSTER-IP     EXTERNAL-IP       PORT(S)                                                                      AGE
service/istio-egressgateway    ClusterIP      10.96.182.29   <none>            80/TCP,443/TCP,15443/TCP                                                     57m
service/istio-ingressgateway   LoadBalancer   10.96.12.165   192.168.103.251   15021:32733/TCP,80:31571/TCP,443:30799/TCP,15012:32184/TCP,15443:32629/TCP   57m
service/istiod                 ClusterIP      10.96.67.37    <none>            15010/TCP,15012/TCP,443/TCP,15014/TCP                                        58m

NAME                                        READY   STATUS    RESTARTS   AGE
pod/istio-egressgateway-688f85d6fb-gpfl7    1/1     Running   0          57m
pod/istio-ingressgateway-577854fd64-mdpcp   1/1     Running   0          57m
pod/istiod-5dc5c5df69-gbvs8                 1/1     Running   0          58m
[root@master01 ~]#
```

* * *

* * *

* * *

* * *

* * *

* * *

##### 卸载

###### 列出在命名空间 istio-system 中安装的所有 Istio chart

```ruby
helm ls -n istio-system

```

* * *

###### (可选项) 删除 Istio 的入/出站网关 chart

```ruby
helm delete istio-egress -n istio-system
helm delete istio-ingress -n istio-system

```

* * *

###### 删除 Istio discovery chart

```ruby
helm delete istiod -n istio-system

```

* * *

###### 删除 Istio base chart

###### 通过 Helm 删除 chart 并不会级联删除它安装的定制资源定义（CRD）

```ruby
helm delete istio-base -n istio-system

```

* * *

###### 删除命名空间 istio-system

```ruby
kubectl delete namespace istio-system

```

* * *

###### (可选项) 删除 Istio 安装的 CRD

永久删除 CRD， 会删除你在集群中创建的所有 Istio 资源。 用下面命令永久删除集群中安装的 Istio CRD

```ruby
kubectl get crd | grep --color=never 'istio.io' | awk '{print $1}' | xargs -n1 kubectl delete crd

```

* * *

* * *

* * *
