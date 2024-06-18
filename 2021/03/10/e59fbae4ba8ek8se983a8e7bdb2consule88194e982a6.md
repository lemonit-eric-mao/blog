---
title: 基于K8S部署Consul联邦
date: '2021-03-10T06:09:43+00:00'
status: private
permalink: /2021/03/10/%e5%9f%ba%e4%ba%8ek8s%e9%83%a8%e7%bd%b2consul%e8%81%94%e9%82%a6
author: 毛巳煜
excerpt: ''
type: post
id: 7007
category:
    - Consul
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
#### **前置条件**

- - - - - -

###### 环境

<table><thead><tr><th align="center">DataCenter</th><th align="center">HostName</th><th align="center">IP</th><th align="center">CPU</th><th align="center">MEM</th><th align="center">命令</th></tr></thead><tbody><tr><td align="center">**DC1**</td><td align="center">**`master01`**</td><td align="center">192.168.103.227</td><td align="center">4 Core</td><td align="center">8G</td><td align="center">hostnamectl set-hostname master01</td></tr><tr><td align="center">**DC1**</td><td align="center">worker01</td><td align="center">192.168.103.228</td><td align="center">4 Core</td><td align="center">8G</td><td align="center">hostnamectl set-hostname worker01</td></tr><tr><td align="center">**DC1**</td><td align="center">worker02</td><td align="center">192.168.103.229</td><td align="center">4 Core</td><td align="center">8G</td><td align="center">hostnamectl set-hostname worker02</td></tr><tr><td align="center">**DC1**</td><td align="center">worker03</td><td align="center">192.168.103.230</td><td align="center">4 Core</td><td align="center">8G</td><td align="center">hostnamectl set-hostname worker03</td></tr><tr><td align="center">**`DC2`**</td><td align="center">**`master01`**</td><td align="center">192.168.103.231</td><td align="center">4 Core</td><td align="center">8G</td><td align="center">hostnamectl set-hostname master01</td></tr><tr><td align="center">**`DC2`**</td><td align="center">worker01</td><td align="center">192.168.103.232</td><td align="center">4 Core</td><td align="center">8G</td><td align="center">hostnamectl set-hostname worker01</td></tr><tr><td align="center">**`DC2`**</td><td align="center">worker02</td><td align="center">192.168.103.233</td><td align="center">4 Core</td><td align="center">8G</td><td align="center">hostnamectl set-hostname worker02</td></tr><tr><td align="center">**`DC2`**</td><td align="center">worker03</td><td align="center">192.168.103.234</td><td align="center">4 Core</td><td align="center">8G</td><td align="center">hostnamectl set-hostname worker03</td></tr></tbody></table>

- - - - - -

###### **Consul联邦启动顺序**

> - k8s主集群： Helm安装 
>   - 启动 **consul-tls-init** --&gt; 启动 **consul-webhook-cert-manager** --&gt; 启动 **consul-server-acl-init** --&gt; 启动 **consul-server** --&gt; 启动 **consul-connect-injector** --&gt; 启动 **consul-controller** --&gt; 启动 **consul-client** --&gt; 启动 **consul-mesh-gateway** --&gt; 启动**consul-ingress-gateway** --&gt; 启动**consul-terminating-gateway**

- - - - - -

> - k8s从集群： Helm安装 --&gt; 启动时自动加入到主集群 
>   - 启动 **consul-tls-init** --&gt; 启动 **consul-webhook-cert-manager** --&gt; 启动 **consul-server-acl-init** --&gt; 启动 **consul-server** --&gt; 启动 **consul-connect-injector** --&gt; 启动 **consul-controller** --&gt; 启动 **consul-client** --&gt; 启动 **consul-mesh-gateway** --&gt; 启动**consul-ingress-gateway** --&gt; 启动**consul-terminating-gateway**

- - - - - -

> - 虚机从集群： Docker-Compose安装 
>   - 启动 **consul-server** --&gt; **将`从`consul-server** 加入到 **`主`consul-server** --&gt; 启动 **consul-client** 并加入到 **consul-server** --&gt; 启动 **consul-mesh-gateway** --&gt; 通过 **consul-client** 加入到Consul注册中心 --&gt; 启动应用程序 --&gt; 启动应用**envoy-sidecar** --&gt; 将应用程序注册到Consul注册中心

- - - - - -

###### **[相关资料](http://www.dev-share.top/2021/07/22/k8s%e9%83%a8%e7%bd%b2consul%e8%81%94%e9%82%a6%e7%9b%b8%e5%85%b3%e8%b5%84%e6%96%99%e6%95%b4%e7%90%86/ "相关资料")**

- - - - - -

###### [安装MetalLB](http://www.dev-share.top/2020/08/14/%e4%bd%bf%e7%94%a8metallb%e6%9d%a5%e8%a7%a3%e5%86%b3k8s-service-loadbalancer%e9%97%ae%e9%a2%98/ "安装MetalLB")

- - - - - -

###### [安装rook/ceph](http://www.dev-share.top/2020/09/24/%e4%bd%bf%e7%94%a8-rook-%e5%ae%89%e8%a3%85%e7%ae%a1%e7%90%86-k8s%e6%8c%81%e4%b9%85%e5%8c%96%e5%ad%98%e5%82%a8/ "安装rook/ceph")

- - - - - -

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

- - - - - -

###### 在本地安装 Consul， 目的是使用Consul命令创建证书

```ruby
yum install -y yum-utils

yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo

yum install -y consul-1.10.0-1.x86_64


```

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

###### 创建命名空间

```ruby
kubectl create ns dhc-consul

```

- - - - - -

###### 导入企业证书（**`可选`**，如果使用企业版Consul，会需要这个key）

```ruby
kubectl -n dhc-consul create secret generic consul-license --from-literal=key=02MV4UU43BK5HGYYTOJZWFQMTMNNEWU33JJVWUK6SZK5LGUWTNJF2E43K2NRHFGMLLJ5KGQ2CMK5FGQWTKKF2E22TINFHVI232LEZFK522KRNGQSLJO5UVSM2WPJSEOOLULJMEUZTBK5IWST3JJF5E22THPBMVOUTNJZUTC2CPKRETKTCUJE2E6R2FORNFI3DJLJUTAMSNK5GTGWSEIU2E22SONBHVIVLJJRBUU4DCNZHDAWKXPBZVSWCSOBRDENLGMFLVC2KPNFEXCSLJO5UWCWCOPJSFOVTGMRDWY5C2KNETMSLKJF3U22SFORGUIY3UJVCGYVKNIRETMTSUM43E2VCNOVHFIZ32JZ5ECNKPKRHGCSLJO5UWGM2SNBRW4UTGMRDWY5C2KNETMSLKJF3U22SFORGUIY3UJVCGYVKNIRETMTSUM43E2VCOMFEWS53JLJMGQ53BLBFGQZCHNR3GE3BZGBQVOMLMJFVG62KNNJAXSTKTGB3U6QZQO5HUMULXJVVG6MKPIRXXQTJRN5UUYQ2KGBNFQSTUMFLTK2DEI5WHMYTMHEYGCVZRNREWU33JJVVEC6KNKMYHOT2DGB3U6VSRO5GWU3ZRJ5CG66CNGFXWSTCDJJ3WG3JZNNSFOTRQJFVG62KZGI4XKYZTKZZUS2LXNFNG26DILIZU22KPNZZWSYSXHFVWIV3YNRRXSSJWK54UU3TCI44WSWKXO52GI3LMPJQVOSTQMJDWYMDFKMYXSYRTKYYGCVZVNZGFQTTKLFLXQ3CJNF3WSWRSHEZFUWCKOVMVONLKLJJTC53CGJ4HAWJTNNUVQWBRHEXDI6DCHA2TEUZPIJIU6MCYIZLGKRSPIVFVKNKMNYZTCZLEJJZG65KRNRSGMS2ON5GGGQJPMQZFA5SSJFRVSVTNJIZHENZWI5GWUMTMJU4WYTSQLBMWIK3VGA4FETDEGIZVG5KNPJBVUMLEIFVWGYJUMRLDAMZTHBIHO3KWNRQXMSSQGRYEU6CJJE4UINSVIZGFKYKWKBVGWV2KORRUINTQMFWDM32PMZDW4SZSPJIEWSSSNVDUQVRTMVNHO4KGMUVW6N3LF5ZSWQKUJZUFAWTHKMXUWVSZM4XUWK3MI5IHOTBXNJBHQSJXI5HWC2ZWKVQWSYKIN5SWWMCSKRXTOMSEKE6T2

```

- - - - - -

###### 导入Gossip-key（**`可选`**，如果开启Gossip，会需要这个key）

```ruby
kubectl -n dhc-consul create secret generic consul-gossip-encryption-key --from-literal=key=$(consul keygen)

```

- - - - - -

###### **安装DC1**

```ruby
# 创建启动文件，配置启动参数
cat > dc1-values.yaml 
```

- - - - - -

###### 安装

```ruby
## 使用本地包，离线安装
helm install -f dc1-values.yaml consul ./consul-0.32.1.tgz -n dhc-consul --version "0.32.1" --wait


## 在线安装
helm install -f dc1-values.yaml consul hashicorp/consul -n dhc-consul --version "0.32.1" --wait


```

- - - - - -

- - - - - -

- - - - - -

###### **设置mesh-gateway[模式](https://www.consul.io/docs/connect/gateways/mesh-gateway#modes-of-operation "模式")**

- **`local`**: 如果设置为local，从**一个数据中心**到**另一个数据中心**的流量将**通过本地网状网关传出**。如果您希望所有跨集群**网络流量从相同位置流出**， 则选择local。**`默认`**，如图：  
  ![](http://qiniu.dev-share.top/consul/k8s-mesh-gateway.png)
- **`remote`**: 如果设置为remote，流量将直接从 pod 路由到远程网状网关， **`这样做能够减少一跳`** 。
- **`none`**: 在此模式下，不使用网关，Connect 代理直接与目标服务建立出站连接。

```ruby
cat > global-config.yaml 
```

- - - - - -

###### 查看 ProxyDefaults与Mesh

```ruby
[root@master01 new_test]# kubectl -n dhc-consul get -f global-config.yaml
NAME                             SYNCED   LAST SYNCED   AGE
mesh.consul.hashicorp.com/mesh   True     16s           16s

NAME                                        SYNCED   LAST SYNCED   AGE
proxydefaults.consul.hashicorp.com/global   True     15s           16s
[root@master01 new_test]#

```

- - - - - -

- - - - - -

- - - - - -

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

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

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

- - - - - -

###### 创建命名空间

```ruby
kubectl create ns dhc-consul


```

- - - - - -

###### 导入企业证书（**`可选`**，如果使用企业版Consul，会需要这个key）

```ruby
kubectl -n dhc-consul create secret generic consul-license --from-literal=key=02MV4UU43BK5HGYYTOJZWFQMTMNNEWU33JJVWUK6SZK5LGUWTNJF2E43K2NRHFGMLLJ5KGQ2CMK5FGQWTKKF2E22TINFHVI232LEZFK522KRNGQSLJO5UVSM2WPJSEOOLULJMEUZTBK5IWST3JJF5E22THPBMVOUTNJZUTC2CPKRETKTCUJE2E6R2FORNFI3DJLJUTAMSNK5GTGWSEIU2E22SONBHVIVLJJRBUU4DCNZHDAWKXPBZVSWCSOBRDENLGMFLVC2KPNFEXCSLJO5UWCWCOPJSFOVTGMRDWY5C2KNETMSLKJF3U22SFORGUIY3UJVCGYVKNIRETMTSUM43E2VCNOVHFIZ32JZ5ECNKPKRHGCSLJO5UWGM2SNBRW4UTGMRDWY5C2KNETMSLKJF3U22SFORGUIY3UJVCGYVKNIRETMTSUM43E2VCOMFEWS53JLJMGQ53BLBFGQZCHNR3GE3BZGBQVOMLMJFVG62KNNJAXSTKTGB3U6QZQO5HUMULXJVVG6MKPIRXXQTJRN5UUYQ2KGBNFQSTUMFLTK2DEI5WHMYTMHEYGCVZRNREWU33JJVVEC6KNKMYHOT2DGB3U6VSRO5GWU3ZRJ5CG66CNGFXWSTCDJJ3WG3JZNNSFOTRQJFVG62KZGI4XKYZTKZZUS2LXNFNG26DILIZU22KPNZZWSYSXHFVWIV3YNRRXSSJWK54UU3TCI44WSWKXO52GI3LMPJQVOSTQMJDWYMDFKMYXSYRTKYYGCVZVNZGFQTTKLFLXQ3CJNF3WSWRSHEZFUWCKOVMVONLKLJJTC53CGJ4HAWJTNNUVQWBRHEXDI6DCHA2TEUZPIJIU6MCYIZLGKRSPIVFVKNKMNYZTCZLEJJZG65KRNRSGMS2ON5GGGQJPMQZFA5SSJFRVSVTNJIZHENZWI5GWUMTMJU4WYTSQLBMWIK3VGA4FETDEGIZVG5KNPJBVUMLEIFVWGYJUMRLDAMZTHBIHO3KWNRQXMSSQGRYEU6CJJE4UINSVIZGFKYKWKBVGWV2KORRUINTQMFWDM32PMZDW4SZSPJIEWSSSNVDUQVRTMVNHO4KGMUVW6N3LF5ZSWQKUJZUFAWTHKMXUWVSZM4XUWK3MI5IHOTBXNJBHQSJXI5HWC2ZWKVQWSYKIN5SWWMCSKRXTOMSEKE6T2

```

- - - - - -

###### 将主集群(DC1)证书， 添加到DC2所在的集群

```ruby
kubectl apply -f consul-federation-secret.yaml


```

- - - - - -

###### **安装DC2**

```ruby
## 创建启动文件，配置启动参数
cat > dc2-values.yaml 
```

- - - - - -

###### 安装

```ruby
## 使用本地包，离线安装
helm install -f dc2-values.yaml consul ./consul-0.32.1.tgz -n dhc-consul --version "0.32.1" --wait


## 在线安装
helm install -f dc2-values.yaml consul hashicorp/consul -n dhc-consul --version "0.32.1" --wait


```

- - - - - -

- - - - - -

- - - - - -

###### 获取login token

```ruby
## Consul UI 访问端口 30443

## 获取login token
kubectl --context=dc1 -n dhc-consul get secret consul-bootstrap-acl-token --template={{.data.token}} | base64 -d


```

- - - - - -

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
</all></all></all></all></all></all></all></all></all></all></all></all>
```

- - - - - -

- - - - - -

- - - - - -

###### DC1 部署测试程序

```ruby
cat > static-client.yaml 
```

- - - - - -

###### DC1 部署client应用程序依赖配置

```ruby
cat > static-client-config.yaml 
```

- - - - - -

- - - - - -

- - - - - -

###### DC2 部署测试程序

**创建一个 yaml 文件`static-server.yaml`来定义`static-server` 服务。请注意，该`static-server`服务还包括`consul.hashicorp.com/connect-inject` 注解。**

```ruby
cat > static-server.yaml 
```

- - - - - -

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

- - - - - -

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

- - - - - -

- - - - - -

- - - - - -

###### **[接入IngressGateway](http://www.dev-share.top/2021/11/05/consul%e8%81%94%e9%82%a6%e9%9b%86%e7%be%a4-%e6%8e%a5%e5%85%a5ingressgateway/ "接入IngressGateway")**

###### **[接入TerminatingGateway](http://www.dev-share.top/2021/10/29/consul%e8%81%94%e9%82%a6%e9%9b%86%e7%be%a4-%e6%8e%a5%e5%85%a5terminatinggateway/ "接入TerminatingGateway")**

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

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

- - - - - -

###### 强制删除命名空间

```ruby
NS_NAME=dhc-consul
kubectl get namespace <span class="katex math inline">NS_NAME -o json | tr -d "\n" | sed "s/\"finalizers\": \[[^]]\+\]/\"finalizers\": []/" | kubectl replace --raw /api/v1/namespaces/</span>NS_NAME/finalize -f -


```

- - - - - -

###### 更新

```ruby
## 使用在线更新
helm upgrade -f dc1-values.yaml consul hashicorp/consul -n dhc-consul

## 使用离线包更新
helm upgrade -f dc1-values.yaml consul ./consul-0.32.1.tgz -n dhc-consul

```

- - - - - -

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

- - - - - -

- - - - - -

- - - - - -

###### **[常见问题与解决方案](http://www.dev-share.top/2021/07/07/%e9%83%a8%e7%bd%b2consul%e8%81%94%e9%82%a6%e5%b8%b8%e8%a7%81%e9%97%ae%e9%a2%98/ "常见问题与解决方案")**

- - - - - -

- - - - - -

- - - - - -