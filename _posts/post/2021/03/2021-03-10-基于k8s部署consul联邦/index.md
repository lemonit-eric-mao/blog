---
title: "基于K8S部署Consul联邦"
date: "2021-03-10"
categories: 
  - "consul"
---

#### **前置条件**

* * *

###### 环境

| DataCenter | HostName | IP | CPU | MEM | 命令 |
| :-: | :-: | :-: | :-: | :-: | :-: |
| **DC1** | **`master01`** | 192.168.103.227 | 4 Core | 8G | hostnamectl set-hostname master01 |
| **DC1** | worker01 | 192.168.103.228 | 4 Core | 8G | hostnamectl set-hostname worker01 |
| **DC1** | worker02 | 192.168.103.229 | 4 Core | 8G | hostnamectl set-hostname worker02 |
| **DC1** | worker03 | 192.168.103.230 | 4 Core | 8G | hostnamectl set-hostname worker03 |
| **`DC2`** | **`master01`** | 192.168.103.231 | 4 Core | 8G | hostnamectl set-hostname master01 |
| **`DC2`** | worker01 | 192.168.103.232 | 4 Core | 8G | hostnamectl set-hostname worker01 |
| **`DC2`** | worker02 | 192.168.103.233 | 4 Core | 8G | hostnamectl set-hostname worker02 |
| **`DC2`** | worker03 | 192.168.103.234 | 4 Core | 8G | hostnamectl set-hostname worker03 |

* * *

###### **Consul联邦启动顺序**

> - k8s主集群： Helm安装
>     - 启动 **consul-tls-init** --> 启动 **consul-webhook-cert-manager** --> 启动 **consul-server-acl-init** --> 启动 **consul-server** --> 启动 **consul-connect-injector** --> 启动 **consul-controller** --> 启动 **consul-client** --> 启动 **consul-mesh-gateway** --> 启动**consul-ingress-gateway** --> 启动**consul-terminating-gateway**

* * *

> - k8s从集群： Helm安装 --> 启动时自动加入到主集群
>     - 启动 **consul-tls-init** --> 启动 **consul-webhook-cert-manager** --> 启动 **consul-server-acl-init** --> 启动 **consul-server** --> 启动 **consul-connect-injector** --> 启动 **consul-controller** --> 启动 **consul-client** --> 启动 **consul-mesh-gateway** --> 启动**consul-ingress-gateway** --> 启动**consul-terminating-gateway**

* * *

> - 虚机从集群： Docker-Compose安装
>     - 启动 **consul-server** --> **将`从`consul-server** 加入到 **`主`consul-server** --> 启动 **consul-client** 并加入到 **consul-server** --> 启动 **consul-mesh-gateway** --> 通过 **consul-client** 加入到Consul注册中心 --> 启动应用程序 --> 启动应用**envoy-sidecar** --> 将应用程序注册到Consul注册中心

* * *

###### **[相关资料](http://www.dev-share.top/2021/07/22/k8s%e9%83%a8%e7%bd%b2consul%e8%81%94%e9%82%a6%e7%9b%b8%e5%85%b3%e8%b5%84%e6%96%99%e6%95%b4%e7%90%86/ "相关资料")**

* * *

###### [安装MetalLB](http://www.dev-share.top/2020/08/14/%e4%bd%bf%e7%94%a8metallb%e6%9d%a5%e8%a7%a3%e5%86%b3k8s-service-loadbalancer%e9%97%ae%e9%a2%98/ "安装MetalLB")

* * *

###### [安装rook/ceph](http://www.dev-share.top/2020/09/24/%e4%bd%bf%e7%94%a8-rook-%e5%ae%89%e8%a3%85%e7%ae%a1%e7%90%86-k8s%e6%8c%81%e4%b9%85%e5%8c%96%e5%ad%98%e5%82%a8/ "安装rook/ceph")

* * *

###### [Helm 安装](http://www.dev-share.top/2020/07/16/helm-%e5%ae%89%e8%a3%85-%e4%bd%bf%e7%94%a8/ "Helm 安装")

```ruby
helm repo add hashicorp https://helm.releases.hashicorp.com


[root@master01 consul]# helm search repo consul
NAME                    CHART VERSION   APP VERSION     DESCRIPTION
hashicorp/consul        0.32.1          1.10.0          Official HashiCorp Consul Chart
[root@master01 consul]#

## 离线安装，下载到本地
helm pull hashicorp/consul --version "0.32.1"

```

* * *

###### 在本地安装 Consul， 目的是使用Consul命令创建证书

```ruby
yum install -y yum-utils

yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo

yum install -y consul-1.10.0-1.x86_64

```

* * *

* * *

* * *

* * *

* * *

* * *

###### 创建命名空间

```ruby
kubectl create ns dhc-consul
```

* * *

###### 导入企业证书（**`可选`**，如果使用企业版Consul，会需要这个key）

```ruby
kubectl -n dhc-consul create secret generic consul-license --from-literal=key=02MV4UU43BK5HGYYTOJZWFQMTMNNEWU33JJVWUK6SZK5LGUWTNJF2E43K2NRHFGMLLJ5KGQ2CMK5FGQWTKKF2E22TINFHVI232LEZFK522KRNGQSLJO5UVSM2WPJSEOOLULJMEUZTBK5IWST3JJF5E22THPBMVOUTNJZUTC2CPKRETKTCUJE2E6R2FORNFI3DJLJUTAMSNK5GTGWSEIU2E22SONBHVIVLJJRBUU4DCNZHDAWKXPBZVSWCSOBRDENLGMFLVC2KPNFEXCSLJO5UWCWCOPJSFOVTGMRDWY5C2KNETMSLKJF3U22SFORGUIY3UJVCGYVKNIRETMTSUM43E2VCNOVHFIZ32JZ5ECNKPKRHGCSLJO5UWGM2SNBRW4UTGMRDWY5C2KNETMSLKJF3U22SFORGUIY3UJVCGYVKNIRETMTSUM43E2VCOMFEWS53JLJMGQ53BLBFGQZCHNR3GE3BZGBQVOMLMJFVG62KNNJAXSTKTGB3U6QZQO5HUMULXJVVG6MKPIRXXQTJRN5UUYQ2KGBNFQSTUMFLTK2DEI5WHMYTMHEYGCVZRNREWU33JJVVEC6KNKMYHOT2DGB3U6VSRO5GWU3ZRJ5CG66CNGFXWSTCDJJ3WG3JZNNSFOTRQJFVG62KZGI4XKYZTKZZUS2LXNFNG26DILIZU22KPNZZWSYSXHFVWIV3YNRRXSSJWK54UU3TCI44WSWKXO52GI3LMPJQVOSTQMJDWYMDFKMYXSYRTKYYGCVZVNZGFQTTKLFLXQ3CJNF3WSWRSHEZFUWCKOVMVONLKLJJTC53CGJ4HAWJTNNUVQWBRHEXDI6DCHA2TEUZPIJIU6MCYIZLGKRSPIVFVKNKMNYZTCZLEJJZG65KRNRSGMS2ON5GGGQJPMQZFA5SSJFRVSVTNJIZHENZWI5GWUMTMJU4WYTSQLBMWIK3VGA4FETDEGIZVG5KNPJBVUMLEIFVWGYJUMRLDAMZTHBIHO3KWNRQXMSSQGRYEU6CJJE4UINSVIZGFKYKWKBVGWV2KORRUINTQMFWDM32PMZDW4SZSPJIEWSSSNVDUQVRTMVNHO4KGMUVW6N3LF5ZSWQKUJZUFAWTHKMXUWVSZM4XUWK3MI5IHOTBXNJBHQSJXI5HWC2ZWKVQWSYKIN5SWWMCSKRXTOMSEKE6T2
```

* * *

###### 导入Gossip-key（**`可选`**，如果开启Gossip，会需要这个key）

```ruby
kubectl -n dhc-consul create secret generic consul-gossip-encryption-key --from-literal=key=$(consul keygen)
```

* * *

###### **安装DC1**

```ruby
# 创建启动文件，配置启动参数
cat > dc1-values.yaml << ERIC
global:
  name: consul
  datacenter: dc1
  imageEnvoy: 'envoyproxy/envoy-alpine:v1.18.3'
  imageK8S: 'hashicorp/consul-k8s:0.26.0'
  # 开源版
  image: 'hashicorp/consul:1.10.0'
#  # 企业版
#  image: 'hashicorp/consul-enterprise:1.10-ent'

  # TLS配置consur组件是否使用TLS。
  tls:
    # 必须为Kubernetes中的联邦启用TLS。默认为 false
    enabled: true

  federation:
    enabled: true
    # 告诉Consul， 创建一个Kubernetes secret， 这会生成一个文件
    # 生成的文件是用来给从集群的数据中心使用， 该文件中描述了从集群要加入到哪个联邦。只在主数据中心配置
    createFederationSecret: true

  # ACL 通过要求每个 API 调用提供一个 ACL 令牌来保护 Consul，该令牌经过验证以确保它具有适当的权限。
  # 如果你只是在测试 Consul，这不是必需的。如想要禁用它，请将true改为false
  acls:
    manageSystemACLs: true
    # 如果已启用ACL，则必须为从集群ACL创建令牌
    # 复制ACL的数据中心。只在主数据中心配置
    createReplicationToken: true

  # Gossip 加密对用于发现集群中其他节点并报告故障的通信层进行加密。
  # 如果你只是在测试 Consul，这不是必需的。如想要禁用它，请注释掉或删除该gossipEncryption
  gossipEncryption:
    # Gossip用来加密保护Consul使用的协议，发现新节点并检测故障。
    secretName: consul-gossip-encryption-key
    secretKey: key


# 告诉Consul 在联邦场景下连接服务网格时， 必须启用 connectInject
connectInject:
  enabled: true
#  # 开启自动注入，自动将envoy-sidecar和consul-sidecar注入所有 pod
#  # 如果为 true，则注入器默认会将 Connect sidecar 注入所有 pod。否则，Pod 必须指定注入注释 ( https://consul.io/docs/k8s/connect#consul-hashicorp-com-connect-inject ) 以选择加入 Connect 注入。
#  default: true


controller:
  enabled: true


# 网格网关， 使 Consul Connect 能够跨 Consul 数据中心工作。
meshGateway:
  # 为保证Kubernetes 联邦场景下的多数据中心之间， 能够通过服务网格网关通信， 必须启用它
  enabled: true
#  replicas: 1


## 开启入口网关
#ingressGateways:
#  enabled: true
#  gateways:
#    - name: ingress-gateway
#  defaults:
#    replicas: 2
#    service:
#      # service 类型包括: LoadBalancer, ClusterIP or NodePort
#      type: LoadBalancer
#      ports:
#        - port: 8080
#          nodePort: null
#        - port: 8443
#          nodePort: null


## 终端网关
#terminatingGateways:
#  # 启用 terminating gateway 必须要设置 connectInject.enabled=true
#  # 与 client.enabled=true
#  enabled: true
#  gateways:
#    - name: terminating-gateway
#  defaults:
#    # 终端网关数量
#    replicas: 2


## 是否开启prometheus监控， 默认false
#prometheus:
#  enabled: false


# 启用Consul UI
ui:
  enabled: true
  service:
    type: 'NodePort'
    nodePort:
      https: 30443

client:
  enabled: true
#  # 默认为 true
#  grpc: true
  # 限制client在哪些 k8s节点中运行
  # 为k8s节点打标签 kubectl label node worker01 consul=client
#  nodeSelector: 'consul: client'

server:
  # 设置Consul Server至少要启动的服务量
  bootstrapExpect: 3
#  # 设置Consul Server数量，默认3个
#  replicas: 3
#  securityContext:
#    runAsNonRoot: false
#    runAsUser: 0
#  # 企业版注册码
#  enterpriseLicense:
#    secretName: 'consul-license'
#    secretKey: 'key'
  storageClass: rook-ceph-block
  disruptionBudget:
    enabled: true
    maxUnavailable: 0
  resources:
    requests:
      memory: "256Mi"
      cpu: "100m"
    limits:
      memory: "256Mi"
      cpu: "100m"

dns:
  enabled: false

#syncCatalog:
#  enabled: true
#  toConsul: true
#  toK8S: true
#  # 如果只想通过k8s注解同步特定服务，请将设置 default: false
#  default: true
#  resources:
#    requests:
#      memory: "500Mi"
#      cpu: "100m"
#    limits:
#      memory: "500Mi"
#      cpu: "100m"

ERIC

```

* * *

###### 安装

```ruby
## 使用本地包，离线安装
helm install -f dc1-values.yaml consul ./consul-0.32.1.tgz -n dhc-consul --version "0.32.1" --wait


## 在线安装
helm install -f dc1-values.yaml consul hashicorp/consul -n dhc-consul --version "0.32.1" --wait

```

* * *

* * *

* * *

###### **设置mesh-gateway[模式](https://www.consul.io/docs/connect/gateways/mesh-gateway#modes-of-operation "模式")**

- **`local`**: 如果设置为local，从**一个数据中心**到**另一个数据中心**的流量将**通过本地网状网关传出**。如果您希望所有跨集群**网络流量从相同位置流出**， 则选择local。**`默认`**，如图： ![](images/k8s-mesh-gateway.png)
- **`remote`**: 如果设置为remote，流量将直接从 pod 路由到远程网状网关， **`这样做能够减少一跳`** 。
- **`none`**: 在此模式下，不使用网关，Connect 代理直接与目标服务建立出站连接。

```ruby
cat > global-config.yaml << ERIC
---
## (不会影响，跨数据中心通信)
## 告诉mesh-gateway开启透明代理模式，跨中心服务通信必须项
apiVersion: consul.hashicorp.com/v1alpha1
kind: Mesh
metadata:
  name: mesh
spec:
  transparentProxy:
    meshDestinationsOnly: true

---
## (它会影响，跨数据中心通信，必须创建)
## 告诉mesh-gateway使用local模式，统一流量出口
apiVersion: consul.hashicorp.com/v1alpha1
kind: ProxyDefaults
metadata:
  ## 只能是global不能改
  name: global
spec:
  meshGateway:
    mode: local

ERIC

kubectl -n dhc-consul apply -f global-config.yaml

```

* * *

###### 查看 ProxyDefaults与Mesh

```ruby
[root@master01 new_test]# kubectl -n dhc-consul get -f global-config.yaml
NAME                             SYNCED   LAST SYNCED   AGE
mesh.consul.hashicorp.com/mesh   True     16s           16s

NAME                                        SYNCED   LAST SYNCED   AGE
proxydefaults.consul.hashicorp.com/global   True     15s           16s
[root@master01 new_test]#
```

* * *

* * *

* * *

###### 导出dc1的证书给其它集群使用， 从这开始dc1将成为主集群， 所有使用dc1证书的集群都将变成从集群

```ruby
kubectl --context dc1 -n dhc-consul get secret consul-federation -o yaml > consul-federation-secret.yaml
```

```ruby
## 查看/解释
cat consul-federation-secret.yaml
apiVersion: v1
data:
  caCert: ......
  caKey: ......
  # 开启 acls 才会有
  replicationToken: NDdhMDQyNjYtN2MyNS0yYTJlLWQ1MTEtZjhhMjEyZmJkMTQw
  # 开启 gossipEncryption 才会有
  gossipEncryptionKey: MndNTFJzMS8yT1RZdzdTeGxNODFXUEljVlI2ay9KM2VVcDFCVG1nY3RGcz0=
  # 使用 echo eyJwcmltYXJ5X2RhdGFjZW50ZXIiOiJkYzEiLCJwcmltYXJ5X2dhdGV3YXlzIjpbIjE5Mi4xNjguMTAzLjI1Mzo0NDMiXX0= | base64 -d
  # 可以得到 {"primary_datacenter":"dc1","primary_gateways":["192.168.103.253:443"]}
  # primary_datacenter 主数据中心名称， primary_gateways 主数据中心网关
  serverConfigJSON: eyJwcmltYXJ5X2RhdGFjZW50ZXIiOiJkYzEiLCJwcmltYXJ5X2dhdGV3YXlzIjpbIjE5Mi4xNjguMTAzLjI1Mzo0NDMiXX0=
kind: Secret
metadata:
  managedFields:
  - apiVersion: v1
    fieldsType: FieldsV1
    ......
    manager: consul-k8s
    operation: Update
  name: consul-federation
  namespace: dhc-consul
type: Opaque

```

* * *

* * *

* * *

* * *

* * *

* * *

###### 切换到 **`DC2`** 所在的集群

```ruby
[root@master01 ~]# kubectl config get-contexts
CURRENT   NAME         CLUSTER      AUTHINFO     NAMESPACE
*         dc1          dc1          dc1
          dc2          dc2          dc2
[root@master01 ~]#

## 切换到DC2所在的集群
kubectl config use-context dc2

```

* * *

###### 创建命名空间

```ruby
kubectl create ns dhc-consul

```

* * *

###### 导入企业证书（**`可选`**，如果使用企业版Consul，会需要这个key）

```ruby
kubectl -n dhc-consul create secret generic consul-license --from-literal=key=02MV4UU43BK5HGYYTOJZWFQMTMNNEWU33JJVWUK6SZK5LGUWTNJF2E43K2NRHFGMLLJ5KGQ2CMK5FGQWTKKF2E22TINFHVI232LEZFK522KRNGQSLJO5UVSM2WPJSEOOLULJMEUZTBK5IWST3JJF5E22THPBMVOUTNJZUTC2CPKRETKTCUJE2E6R2FORNFI3DJLJUTAMSNK5GTGWSEIU2E22SONBHVIVLJJRBUU4DCNZHDAWKXPBZVSWCSOBRDENLGMFLVC2KPNFEXCSLJO5UWCWCOPJSFOVTGMRDWY5C2KNETMSLKJF3U22SFORGUIY3UJVCGYVKNIRETMTSUM43E2VCNOVHFIZ32JZ5ECNKPKRHGCSLJO5UWGM2SNBRW4UTGMRDWY5C2KNETMSLKJF3U22SFORGUIY3UJVCGYVKNIRETMTSUM43E2VCOMFEWS53JLJMGQ53BLBFGQZCHNR3GE3BZGBQVOMLMJFVG62KNNJAXSTKTGB3U6QZQO5HUMULXJVVG6MKPIRXXQTJRN5UUYQ2KGBNFQSTUMFLTK2DEI5WHMYTMHEYGCVZRNREWU33JJVVEC6KNKMYHOT2DGB3U6VSRO5GWU3ZRJ5CG66CNGFXWSTCDJJ3WG3JZNNSFOTRQJFVG62KZGI4XKYZTKZZUS2LXNFNG26DILIZU22KPNZZWSYSXHFVWIV3YNRRXSSJWK54UU3TCI44WSWKXO52GI3LMPJQVOSTQMJDWYMDFKMYXSYRTKYYGCVZVNZGFQTTKLFLXQ3CJNF3WSWRSHEZFUWCKOVMVONLKLJJTC53CGJ4HAWJTNNUVQWBRHEXDI6DCHA2TEUZPIJIU6MCYIZLGKRSPIVFVKNKMNYZTCZLEJJZG65KRNRSGMS2ON5GGGQJPMQZFA5SSJFRVSVTNJIZHENZWI5GWUMTMJU4WYTSQLBMWIK3VGA4FETDEGIZVG5KNPJBVUMLEIFVWGYJUMRLDAMZTHBIHO3KWNRQXMSSQGRYEU6CJJE4UINSVIZGFKYKWKBVGWV2KORRUINTQMFWDM32PMZDW4SZSPJIEWSSSNVDUQVRTMVNHO4KGMUVW6N3LF5ZSWQKUJZUFAWTHKMXUWVSZM4XUWK3MI5IHOTBXNJBHQSJXI5HWC2ZWKVQWSYKIN5SWWMCSKRXTOMSEKE6T2
```

* * *

###### 将主集群(DC1)证书， 添加到DC2所在的集群

```ruby
kubectl apply -f consul-federation-secret.yaml

```

* * *

###### **安装DC2**

```ruby
## 创建启动文件，配置启动参数
cat > dc2-values.yaml << ERIC
global:
  name: consul
  datacenter: dc2
  imageEnvoy: 'envoyproxy/envoy-alpine:v1.18.3'
  imageK8S: 'hashicorp/consul-k8s:0.26.0'
  # 开源版
  image: 'hashicorp/consul:1.10.0'
#  # 企业版
#  image: 'hashicorp/consul-enterprise:1.10-ent'

  tls:
    enabled: true
    # 这里我们使用的是来自主服务器数据中心的共享证书
    # 通过主服务器的联邦secret导出的
    caCert:
      secretName: consul-federation
      secretKey: caCert
    caKey:
      secretName: consul-federation
      secretKey: caKey

  # 如果主集群启用了ACL， 这里才会启用。这里选择禁用它。如想要禁用它，请将true改为false
  acls:
    manageSystemACLs: true
    # 如果主集群启用了ACL， 这里才会启用。如想要禁用它，请注释掉或删除该replicationToken
    replicationToken:
      secretName: consul-federation
      secretKey: replicationToken

  federation:
    enabled: true

  # 如果主集群启用了Gossip， 这里才会启用。如想要禁用它，请注释掉或删除该gossipEncryption
  gossipEncryption:
    secretName: consul-federation
    secretKey: gossipEncryptionKey


connectInject:
  enabled: true


controller:
  enabled: true


meshGateway:
  enabled: true


#ingressGateways:
#  enabled: true
#  gateways:
#    - name: ingress-gateway
#  defaults:
#    replicas: 2
#    service:
#      type: LoadBalancer


#terminatingGateways:
#  enabled: true
#  gateways:
#    - name: terminating-gateway
#  defaults:
#    replicas: 2


client:
  enabled: true
#  nodeSelector: 'consul: client'

server:
#  replicas: 3
#  securityContext:
#    runAsNonRoot: false
#    runAsUser: 0
#  # 企业版注册码
#  enterpriseLicense:
#    secretName: 'consul-license'
#    secretKey: 'key'
  storageClass: rook-ceph-block
  bootstrapExpect: 3
  disruptionBudget:
    enabled: true
    maxUnavailable: 0
  resources:
    requests:
      memory: "256Mi"
      cpu: "100m"
    limits:
      memory: "256Mi"
      cpu: "100m"
  # 此配置包括主数据中心的网格网关的地址，以便Consul可以开始联邦。
  extraVolumes:
    - type: secret
      name: consul-federation
      items:
        - key: serverConfigJSON
          path: config.json
      load: true


dns:
  enabled: false


#syncCatalog:
#  enabled: true
#  toConsul: true
#  toK8S: true
#  default: true
#  resources:
#    requests:
#      memory: "500Mi"
#      cpu: "100m"
#    limits:
#      memory: "500Mi"
#      cpu: "100m"

ERIC

```

* * *

###### 安装

```ruby
## 使用本地包，离线安装
helm install -f dc2-values.yaml consul ./consul-0.32.1.tgz -n dhc-consul --version "0.32.1" --wait


## 在线安装
helm install -f dc2-values.yaml consul hashicorp/consul -n dhc-consul --version "0.32.1" --wait

```

* * *

* * *

* * *

###### 获取login token

```ruby
## Consul UI 访问端口 30443

## 获取login token
kubectl --context=dc1 -n dhc-consul get secret consul-bootstrap-acl-token --template={{.data.token}} | base64 -d

```

* * *

###### 验证集群

```ruby
[root@master01 consul]# kubectl --context dc1 -n dhc-consul exec statefulset/consul-server -- consul members -wan
Node                 Address             Status  Type    Build   Protocol  DC   Segment
consul-server-0.dc1  10.244.30.119:8302  alive   server  1.10.0  2         dc1  <all>
consul-server-0.dc2  10.244.19.66:8302   alive   server  1.10.0  2         dc2  <all>
consul-server-1.dc1  10.244.5.6:8302     alive   server  1.10.0  2         dc1  <all>
consul-server-1.dc2  10.244.30.113:8302  alive   server  1.10.0  2         dc2  <all>
consul-server-2.dc1  10.244.19.96:8302   alive   server  1.10.0  2         dc1  <all>
consul-server-2.dc2  10.244.5.25:8302    alive   server  1.10.0  2         dc2  <all>
[root@master01 consul]#


[root@master01 consul]# kubectl --context dc2 -n dhc-consul exec statefulset/consul-server -- consul members -wan
Node                 Address             Status  Type    Build   Protocol  DC   Segment
consul-server-0.dc1  10.244.30.119:8302  alive   server  1.10.0  2         dc1  <all>
consul-server-0.dc2  10.244.19.66:8302   alive   server  1.10.0  2         dc2  <all>
consul-server-1.dc1  10.244.5.6:8302     alive   server  1.10.0  2         dc1  <all>
consul-server-1.dc2  10.244.30.113:8302  alive   server  1.10.0  2         dc2  <all>
consul-server-2.dc1  10.244.19.96:8302   alive   server  1.10.0  2         dc1  <all>
consul-server-2.dc2  10.244.5.25:8302    alive   server  1.10.0  2         dc2  <all>
[root@master01 consul]#
```

* * *

* * *

* * *

###### DC1 部署测试程序

```ruby
cat > static-client.yaml << ERIC

---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: static-client

---
apiVersion: v1
kind: Service
metadata:
  name: static-client
spec:
  selector:
    app: static-client
  ports:
    - port: 80

---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: static-client
  name: static-client
spec:
  replicas: 1
  selector:
    matchLabels:
      app: static-client
  template:
    metadata:
      annotations:
        consul.hashicorp.com/connect-inject: 'true'
        ## 显示指定 'upstreams' 后可以通过 '127.0.0.1:8080' 直接访问远程服务器， 它不会走透明代理
        ## 如果想使用 'upstreams' 并且还想使用服务名访问， 可以通过hostAliases修改容器内的 '/etc/hosts' 文件
        #consul.hashicorp.com/connect-service-upstreams: 'static-server:8080:dc2'
        consul.hashicorp.com/service-tags: 'dc1-static-client'

      labels:
        app: static-client
    spec:
      serviceAccountName: static-client
      # 通过hostAliases修改容器内的 '/etc/hosts' 文件
      #hostAliases:
      #  - ip: "127.0.0.1"
      #    hostnames:
      #      - "static-server"
      containers:
        - name: static-client
          image: nginx:1.20-alpine
          securityContext:
            runAsUser: 0

ERIC


## 部署
kubectl --context=dc1 apply -f static-client.yaml

```

* * *

###### DC1 部署client应用程序依赖配置

```ruby
cat > static-client-config.yaml << ERIC

---
## (它会影响，跨数据中心通信，必须创建)
## 配置服务与服务之间的访问权限
apiVersion: consul.hashicorp.com/v1alpha1
kind: ServiceIntentions
metadata:
  name: client-to-server
spec:
  sources:
    ## 告诉Consul的ACL，允许static-client服务访问static-server服务
    - action: allow
      name: static-client
  destination:
    name: static-server

---
## (它会影响，跨数据中心通信)
## 创建服务解析器, 将另一个数据中心中的服务设置为虚拟服务
apiVersion: consul.hashicorp.com/v1alpha1
kind: ServiceResolver
metadata:
  ## 表明正在配置的服务的名称, 不能随意写, 指定另一个数据中心中实际存在的服务名
  name: static-server
spec:
  redirect:
    ## 需要要解析的服务而不是当前服务
    service: static-server
    ## 用于解析服务的数据中心，而不是当前的数据中心。
    datacenter: dc2

#---
### (不会影响，跨数据中心通信)
### 基于虚拟服务配置服务分流
#apiVersion: consul.hashicorp.com/v1alpha1
#kind: ServiceSplitter
#metadata:
#  ## 请求发起方，指定service名称不能随意写
#  name: static-client
#spec:
#  splits:
#    - weight: 100
#      ## 接收方，指定虚拟服务名称不能随意写
#      service: static-server

ERIC


## 部署
kubectl --context=dc1 apply -f static-client-config.yaml

```

* * *

* * *

* * *

###### DC2 部署测试程序

**创建一个 yaml 文件`static-server.yaml`来定义`static-server` 服务。请注意，该`static-server`服务还包括`consul.hashicorp.com/connect-inject` 注解。**

```ruby
cat > static-server.yaml << ERIC

---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: static-server

---
apiVersion: v1
kind: Service
metadata:
  name: static-server
spec:
  selector:
    app: static-server
  ports:
    - port: 80
      targetPort: 8080

---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: static-server
  name: static-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: static-server
  template:
    metadata:
      annotations:
        consul.hashicorp.com/connect-inject: 'true'
        consul.hashicorp.com/service-tags: 'dc2-static-server'
      labels:
        app: static-server
    spec:
      serviceAccountName: static-server
      containers:
        - name: static-server
          image: hashicorp/http-echo:latest
          args:
            - -text="hello world dc2-static-server"
            - -listen=:8080
          ports:
            - containerPort: 8080

ERIC


## 部署
kubectl --context=dc2 apply -f static-server.yaml

```

* * *

###### 查看

```ruby
[root@master01 consul]# kubectl --context dc1 -n dhc-consul exec statefulset/consul-server -- consul catalog services -datacenter dc1
consul
mesh-gateway
static-client
static-client-sidecar-proxy
[root@master01 consul]#


[root@master01 consul]# kubectl --context dc1 -n dhc-consul exec statefulset/consul-server -- consul catalog services -datacenter dc2
consul
mesh-gateway
static-server
static-server-sidecar-proxy
[root@master01 consul]#

```

* * *

###### 测试访问

```ruby
## 测试证明跨集群通信成功
[root@master01 consul]# kubectl exec deploy/static-client -c static-client -- curl -sS 127.0.0.1:8080
"hello world dc2-static-server"
[root@master01 consul]#


## 测试证明使用 service名称通信成功。
## 注意： 当下使用透明代理访问，需要在本集群部署与远程集群相同的服务，才能够通过透明代理+服务解析器，进行域名访问
[root@master01 consul]# kubectl exec deploy/static-client -c static-client -- curl -sS http://static-server:8080
"hello world dc2-static-server"
[root@master01 consul]#

```

* * *

* * *

* * *

###### **[接入IngressGateway](http://www.dev-share.top/2021/11/05/consul%e8%81%94%e9%82%a6%e9%9b%86%e7%be%a4-%e6%8e%a5%e5%85%a5ingressgateway/ "接入IngressGateway")**

###### **[接入TerminatingGateway](http://www.dev-share.top/2021/10/29/consul%e8%81%94%e9%82%a6%e9%9b%86%e7%be%a4-%e6%8e%a5%e5%85%a5terminatinggateway/ "接入TerminatingGateway")**

* * *

* * *

* * *

* * *

* * *

* * *

##### 常用命令

###### 卸载

```ruby
## 要先删除应用程序
## ......

helm uninstall consul hashicorp/consul -n dhc-consul
## 删除pvc，否则有缓存
kubectl -n dhc-consul delete pvc data-dhc-consul-consul-server-0
kubectl -n dhc-consul delete pvc data-dhc-consul-consul-server-1
kubectl -n dhc-consul delete pvc data-dhc-consul-consul-server-2
## 删除证书
kubectl delete secrets -n dhc-consul consul-gossip-encryption-key consul-acl-replication-acl-token consul-bootstrap-acl-token consul-client-acl-token consul-connect-inject-acl-token consul-controller-acl-token consul-federation consul-mesh-gateway-acl-token  consul-ingress-gateway-ingress-gateway-acl-token consul-catalog-sync-acl-token consul-enterprise-license-acl-token

kubectl delete ns dhc-consul

```

* * *

###### 强制删除命名空间

```ruby
NS_NAME=dhc-consul
kubectl get namespace $NS_NAME -o json | tr -d "\n" | sed "s/\"finalizers\": \[[^]]\+\]/\"finalizers\": []/" | kubectl replace --raw /api/v1/namespaces/$NS_NAME/finalize -f -

```

* * *

###### 更新

```ruby
## 使用在线更新
helm upgrade -f dc1-values.yaml consul hashicorp/consul -n dhc-consul

## 使用离线包更新
helm upgrade -f dc1-values.yaml consul ./consul-0.32.1.tgz -n dhc-consul
```

* * *

###### API删除 Consul service列表

**`X-Consul-Token`: 为bootstrap token**

```ruby
curl -k https://192.168.103.235:8501/v1/catalog/deregister \
--request PUT \
--header "X-Consul-Token: 98e4ede4-271b-383b-94b7-c085137188fe" \
--data '
{
  "Datacenter": "dc6",
  "Node": "consul-client-0",
  "ServiceID": "dc6-static-server-0"
}'

```

* * *

* * *

* * *

###### **[常见问题与解决方案](http://www.dev-share.top/2021/07/07/%e9%83%a8%e7%bd%b2consul%e8%81%94%e9%82%a6%e5%b8%b8%e8%a7%81%e9%97%ae%e9%a2%98/ "常见问题与解决方案")**

* * *

* * *

* * *
