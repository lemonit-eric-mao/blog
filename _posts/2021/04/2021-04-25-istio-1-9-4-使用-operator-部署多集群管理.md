---
title: "Istio 1.9.4 使用 operator 部署多集群管理"
date: "2021-04-25"
categories: 
  - "istio"
---

##### 前置条件

###### **[安装K8S](ansible-playbook-%e6%8e%a7%e5%88%b6-kubeadm%e9%83%a8%e7%bd%b2k8s-%e5%a0%86%e5%8f%a0etcd "安装K8S")**

* * *

###### **[拉取k8s集群.kube/config](k8s-%e5%a4%9a%e9%9b%86%e7%be%a4%e5%88%87%e6%8d%a2 "拉取k8s集群.kube/config") 跳转链接**

```ruby
./generate-kube-config.sh \
    cluster1=192.168.103.227 \
    cluster2=192.168.103.231 \
    cluster3=192.168.103.235 \
    && source /etc/profile

cat >> /etc/profile << ERIC
export CTX_CLUSTER1=cluster1
export CTX_CLUSTER2=cluster2
export CTX_CLUSTER3=cluster3
ERIC

source /etc/profile

```

###### 查看

```ruby
[root@master01 ~]# kubectl config get-contexts
CURRENT   NAME       CLUSTER    AUTHINFO   NAMESPACE
*         cluster1   cluster1   cluster1
          cluster2   cluster2   cluster2
          cluster3   cluster3   cluster3
[root@master01 ~]#
```

* * *

###### **[安装 MetalLB](%e4%bd%bf%e7%94%a8metallb%e6%9d%a5%e8%a7%a3%e5%86%b3k8s-service-loadbalancer%e9%97%ae%e9%a2%98 "安装 MetalLB")**

```ruby
kubectl --context="${CTX_CLUSTER1}" apply -f - << ERIC

---
apiVersion: v1
kind: ConfigMap
metadata:
  namespace: metallb-system
  # 这个名称在 metallb.yaml中设定，改完以后ConfigMap会不启作用
  name: config
data:
  config: |
    address-pools:
    - name: my-ip-space
      protocol: layer2
      addresses:
      # 提供给外部访问的IP地址段
      - 192.168.103.251-192.168.103.252

ERIC


kubectl --context="${CTX_CLUSTER2}" apply -f - << ERIC

---
apiVersion: v1
kind: ConfigMap
metadata:
  namespace: metallb-system
  # 这个名称在 metallb.yaml中设定，改完以后ConfigMap会不启作用
  name: config
data:
  config: |
    address-pools:
    - name: my-ip-space
      protocol: layer2
      addresses:
      # 提供给外部访问的IP地址段
      - 192.168.103.253-192.168.103.254

ERIC



```

* * *

| 虚拟机名 | 内网IP | 用途 | CPU | 内存 | 硬盘01 | 硬盘02 | 操作系统 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Mao-k8s-v1.20.4-103.227 | 192.168.103.227 | **`master01`** | 8 | 8 | 100 | 100 | CentOS 7.9 |
| Mao-k8s-v1.20.4-103.228 | 192.168.103.228 | worker01 | 8 | 8 | 100 | 100 | CentOS 7.9 |
| Mao-k8s-v1.20.4-103.229 | 192.168.103.229 | worker02 | 8 | 8 | 100 | 100 | CentOS 7.9 |
| Mao-k8s-v1.20.4-103.230 | 192.168.103.230 | worker03 | 8 | 8 | 100 | 100 | CentOS 7.9 |
| Mao-k8s-v1.20.4-103.231 | 192.168.103.231 | **`master01`** | 8 | 8 | 100 | 100 | CentOS 7.9 |
| Mao-k8s-v1.20.4-103.232 | 192.168.103.232 | worker01 | 8 | 8 | 100 | 100 | CentOS 7.9 |
| Mao-k8s-v1.20.4-103.233 | 192.168.103.233 | worker02 | 8 | 8 | 100 | 100 | CentOS 7.9 |
| Mao-k8s-v1.20.4-103.234 | 192.168.103.234 | worker03 | 8 | 8 | 100 | 100 | CentOS 7.9 |
| Mao-k8s-v1.20.4-103.235 | 192.168.103.235 | **`master01`** | 8 | 8 | 100 | 100 | CentOS 7.9 |
| Mao-k8s-v1.20.4-103.236 | 192.168.103.236 | worker01 | 8 | 8 | 100 | 100 | CentOS 7.9 |
| Mao-k8s-v1.20.4-103.237 | 192.168.103.237 | worker02 | 8 | 8 | 100 | 100 | CentOS 7.9 |
| Mao-k8s-v1.20.4-103.238 | 192.168.103.238 | worker03 | 8 | 8 | 100 | 100 | CentOS 7.9 |

* * *

* * *

* * *

##### 安装 istioctl 可执行程序

```ruby
wget https://github.com/istio/istio/releases/download/1.9.4/istio-1.9.4-linux-amd64.tar.gz && tar -zxvf istio-1.9.4-linux-amd64.tar.gz && cp istio-1.9.4/bin/istioctl /usr/local/bin/
```

* * *

* * *

* * *

##### **[将证书和密钥插入集群](https://istio.io/latest/docs/tasks/security/cert-management/plugin-ca-cert/#plug-in-certificates-and-key-into-the-cluster "将证书和密钥插入集群")**

###### **`或者`** 使用istio默认提供的证书

```ruby
cd istio-1.9.4

kubectl --context="${CTX_CLUSTER1}" create namespace istio-system
kubectl --context="${CTX_CLUSTER2}" create namespace istio-system

kubectl --context="${CTX_CLUSTER1}" create secret generic cacerts -n istio-system \
      --from-file=samples/certs/ca-cert.pem \
      --from-file=samples/certs/ca-key.pem \
      --from-file=samples/certs/root-cert.pem \
      --from-file=samples/certs/cert-chain.pem

kubectl --context="${CTX_CLUSTER2}" create secret generic cacerts -n istio-system \
      --from-file=samples/certs/ca-cert.pem \
      --from-file=samples/certs/ca-key.pem \
      --from-file=samples/certs/root-cert.pem \
      --from-file=samples/certs/cert-chain.pem


```

* * *

* * *

* * *

###### **[官方文档 多集群安装](https://istio.io/latest/zh/docs/setup/install/multicluster/ "官方文档 多集群安装")**

* * *

###### 配置**`集群01`**的相关操作

```ruby
###### 创建命名空间
kubectl --context="${CTX_CLUSTER1}" create namespace istio-system


###### 为 cluster1 设置缺省网络 
kubectl --context="${CTX_CLUSTER1}" get namespace istio-system && \
  kubectl --context="${CTX_CLUSTER1}" label namespace istio-system topology.istio.io/network=network1


###### 将 cluster1 设为主集群
cat <<EOF > cluster1.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  values:
    global:
      meshID: mesh1
      multiCluster:
        clusterName: cluster1
      network: network1
EOF

istioctl install --context="${CTX_CLUSTER1}" -f cluster1.yaml

```

* * *

###### 配置**`集群02`**的相关操作

```ruby
###### 创建命名空间
kubectl --context="${CTX_CLUSTER2}" create namespace istio-system

###### 为 cluster2 设置缺省网络
kubectl --context="${CTX_CLUSTER2}" get namespace istio-system && \
  kubectl --context="${CTX_CLUSTER2}" label namespace istio-system topology.istio.io/network=network2


###### 将 cluster2 设为主集群
cat <<EOF > cluster2.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  values:
    global:
      meshID: mesh1
      multiCluster:
        clusterName: cluster2
      network: network2
EOF

istioctl install --context="${CTX_CLUSTER2}" -f cluster2.yaml

```

* * *

###### 启用端点发现

```ruby
###### 在 cluster2 中安装一个提供 cluster1 访问权限的远程 secret
istioctl x create-remote-secret \
  --context="${CTX_CLUSTER1}" \
  --name=cluster1 | \
  kubectl apply -f - --context="${CTX_CLUSTER2}"


###### 在 cluster1 中安装一个提供 cluster2 访问权限的远程 secret
istioctl x create-remote-secret \
  --context="${CTX_CLUSTER2}" \
  --name=cluster2 | \
  kubectl apply -f - --context="${CTX_CLUSTER1}"

```

* * *

* * *

* * *

* * *

* * *

* * *

##### 验证安装结果

###### 部署 HelloWorld Service

```ruby
kubectl create --context="${CTX_CLUSTER1}" namespace sample
kubectl create --context="${CTX_CLUSTER2}" namespace sample


kubectl label --context="${CTX_CLUSTER1}" namespace sample \
    istio-injection=enabled
kubectl label --context="${CTX_CLUSTER2}" namespace sample \
    istio-injection=enabled


kubectl apply --context="${CTX_CLUSTER1}" \
    -f samples/helloworld/helloworld.yaml \
    -l service=helloworld -n sample
kubectl apply --context="${CTX_CLUSTER2}" \
    -f samples/helloworld/helloworld.yaml \
    -l service=helloworld -n sample


```

* * *

###### 部署 V1 版的 HelloWorld

```ruby
kubectl apply --context="${CTX_CLUSTER1}" \
    -f samples/helloworld/helloworld.yaml \
    -l version=v1 -n sample

```

* * *

###### 部署 V2 版的 HelloWorld

```ruby
kubectl apply --context="${CTX_CLUSTER2}" \
    -f samples/helloworld/helloworld.yaml \
    -l version=v2 -n sample

```

* * *

###### 部署 Sleep

```ruby
kubectl apply --context="${CTX_CLUSTER1}" \
    -f samples/sleep/sleep.yaml -n sample
kubectl apply --context="${CTX_CLUSTER2}" \
    -f samples/sleep/sleep.yaml -n sample

```

* * *

* * *

* * *

###### 测试

```ruby
kubectl exec --context="${CTX_CLUSTER1}" -n sample -c sleep \
    "$(kubectl get pod --context="${CTX_CLUSTER1}" -n sample -l \
    app=sleep -o jsonpath='{.items[0].metadata.name}')" \
    -- curl -sS helloworld.sample:5000/hello


kubectl exec --context="${CTX_CLUSTER2}" -n sample -c sleep \
    "$(kubectl get pod --context="${CTX_CLUSTER2}" -n sample -l \
    app=sleep -o jsonpath='{.items[0].metadata.name}')" \
    -- curl -sS helloworld.sample:5000/hello

```
