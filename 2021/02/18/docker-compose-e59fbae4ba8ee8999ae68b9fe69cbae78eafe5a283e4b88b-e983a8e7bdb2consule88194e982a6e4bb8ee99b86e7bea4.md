---
title: 'docker-compose 基于虚拟机环境下 部署Consul联邦从集群'
date: '2021-02-18T03:20:30+00:00'
status: private
permalink: /2021/02/18/docker-compose-%e5%9f%ba%e4%ba%8e%e8%99%9a%e6%8b%9f%e6%9c%ba%e7%8e%af%e5%a2%83%e4%b8%8b-%e9%83%a8%e7%bd%b2consul%e8%81%94%e9%82%a6%e4%bb%8e%e9%9b%86%e7%be%a4
author: 毛巳煜
excerpt: ''
type: post
id: 6916
category:
    - Consul
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### **[单节点部署及说明](http://www.dev-share.top/2021/02/10/docker-compose-%e9%83%a8%e7%bd%b2-consul-%e5%8d%95%e8%8a%82%e7%82%b9/ "单节点部署及说明")**

- - - - - -

- - - - - -

- - - - - -

###### 前置条件

<table><thead><tr><th>集群</th><th>服务名</th><th>IP</th></tr></thead><tbody><tr><td>联邦 **K8s`主`** 集群</td><td>primary\_gateways</td><td>192.168.103.253:443</td></tr><tr><td>联邦 **虚机`从`** 集群</td><td>consul-server-0</td><td>192.168.103.235</td></tr><tr><td>联邦 **虚机`从`** 集群</td><td>consul-server-1</td><td>192.168.103.236</td></tr><tr><td>联邦 **虚机`从`** 集群</td><td>consul-server-2</td><td>192.168.103.237</td></tr><tr><td>联邦 **虚机`从`** 集群</td><td>consul-client-0</td><td>192.168.103.238</td></tr></tbody></table>

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

###### 在Consul联邦主集群中获取相关依赖文件

```ruby
##
kubectl -n dhc-consul get secrets/consul-ca-cert --template='{{index .data "tls.crt" }}' | base64 -d > consul-agent-ca.pem

## CA授权签名
kubectl -n dhc-consul get secrets/consul-ca-key --template='{{index .data "tls.key" }}' | base64 -d > consul-agent-ca-key.pem




## 获取 Gossip Key
kubectl -n dhc-consul get secrets/consul-gossip-encryption-key --template='{{.data.key}}' | base64 -d
PQbbZH+XboiMdkF7K8Dv3ZENe+15UIcEdVg/twLnYFo=




## 获取 ACL Token，用于实现从集群拉取同步联邦主集群中的Token、Policies
kubectl -n dhc-consul get secrets/consul-acl-replication-acl-token --template='{{.data.token}}' | base64 -d
17744abc-7008-5278-5525-9c37df7ee2ae




## 获取login token、bootstrap token
kubectl --context=dc1 -n dhc-consul get secret consul-bootstrap-acl-token --template={{.data.token}} | base64 -d
98e4ede4-271b-383b-94b7-c085137188fe



```

- - - - - -

- - - - - -

- - - - - -

##### 创建文件夹

```ruby
mkdir -p /home/deploy/consul/config/certs/ /home/deploy/consul/config/hcls

cd /home/deploy/consul/


```

- - - - - -

###### 将联邦主集群的`consul-agent-key.pem` `consul-agent-ca-key.pem`文件放到从集群的`/home/deploy/consul/config/certs`目录下

```ruby
## 在联邦主集群执行
scp *.pem 192.168.103.235:/home/deploy/consul/config/certs

## 在联邦从集群执行
cd /home/deploy/consul/config/certs

## 生成新的从集群 server证书
consul tls cert create -server -dc=dc6 -node consul-server-0
consul tls cert create -server -dc=dc6 -node consul-server-1
consul tls cert create -server -dc=dc6 -node consul-server-2

## 生成新的从集群 client证书
consul tls cert create -client -dc=dc6


```

- - - - - -

#### **部署从集群的 consul-server-`0`**

```ruby
hostnamectl set-hostname consul-server-0

```

- - - - - -

###### 从集群的 consul-server-0配置文件

```ruby
cat > config/hcls/consul.hcl 
```

- - - - - -

###### 从集群的 consul-server-0

```ruby
cat > docker-compose.yaml 
```

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

#### **部署从集群的 consul-server-`1`**

```ruby
hostnamectl set-hostname consul-server-1

```

- - - - - -

##### 创建文件夹

```ruby
mkdir -p /home/deploy/consul/config/certs/ /home/deploy/consul/config/hcls

cd /home/deploy/consul/


```

- - - - - -

###### 将consul-server-0的config/certs/\*.pem 复制到当前config/certs/

```ruby
scp 192.168.103.235:/home/deploy/consul/config/certs/*.pem  config/certs/

```

- - - - - -

##### 从集群的 consul-server-1配置文件

```ruby
cat > config/hcls/consul.hcl 
```

- - - - - -

##### 从集群的 consul-server-1

```ruby
cat > docker-compose.yaml 
```

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

#### **部署从集群的 consul-server-`2`**

```ruby
hostnamectl set-hostname consul-server-2

```

- - - - - -

##### 创建文件夹

```ruby
mkdir -p /home/deploy/consul/config/certs/ /home/deploy/consul/config/hcls

cd /home/deploy/consul/


```

- - - - - -

###### 将consul-server-0的config/certs/\*.pem 复制到当前config/certs/

```ruby
scp 192.168.103.235:/home/deploy/consul/config/certs/*.pem  config/certs/

```

- - - - - -

##### 从集群的 consul-server-2配置文件

```ruby
cat > config/hcls/consul.hcl 
```

- - - - - -

##### 从集群的 consul-server-2

```ruby
cat > docker-compose.yaml 
```

- - - - - -

- - - - - -

- - - - - -

#### 在任意consul-server端为consul-clinet创建(Policy 与 Token)

###### 创建Policy文件

```hcl
cat > config/hcls/client-token.hcl 
```

- - - - - -

###### client端 创建 `Client Token` 与 `Client Policy`

```ruby
## 创建 Client Policy
docker exec -it consul-server-2 \
       consul acl policy create -name "client-token-dc6" \
                                -description "client-token-dc6 Token Policy" \
                                -valid-datacenter "dc6" \
                                -datacenter "dc6" \
                                -rules @/opt/hcls/client-token.hcl

## 根据Policy 创建 Client Token
docker exec -it consul-server-2 \
       consul acl token create -policy-name "client-token-dc6" \
                               -datacenter "dc6" \
                               -description "client-token-dc6 Token"

## 输出结果
AccessorID:       2537033e-506f-e428-fe13-e0dc293d9322
SecretID:         2796b1d7-f05b-8106-f735-da7cd07e584a    ## 此Token是给所有client的agent使用的
Description:      client-token-dc6 Token
Local:            false
Create Time:      2021-09-02 03:03:24.553944727 +0000 UTC
Policies:
   159d7bf8-f5fd-381d-505e-2f26d2df5239 - client-token



```

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

#### **部署从集群的 consul-client-`0`**

```ruby
hostnamectl set-hostname consul-client-0

```

- - - - - -

##### 创建文件夹

```ruby
mkdir -p /home/deploy/consul/config/consul-bin/ /home/deploy/consul/config/certs/ /home/deploy/consul/config/hcls

cd /home/deploy/consul/


```

- - - - - -

###### 将consul-server-0的`config/certs/*.pem` 复制到当前`config/certs/`

```ruby
scp 192.168.103.235:/home/deploy/consul/config/certs/*.pem  config/certs/

```

- - - - - -

##### 从集群的 consul-client-0配置文件

```ruby
cat > config/hcls/consul.hcl 
```

- - - - - -

##### 从集群的 consul-client-0并且加入mesh-gateway

```ruby
cat > docker-compose.yaml 
```

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

###### 测试是否成功

```ruby
## "agent": "98e4ede4-271b-383b-94b7-c085137188fe"
docker exec -it consul-server-0 \
  consul acl token list



## 查看WAN池，集群联邦都是通过 WAN口进行通信的
docker exec -it consul-server-0 \
  consul members -wan

Node                 Address               Status  Type    Build   Protocol  DC   Segment
consul-server-0.dc1  10.244.30.79:8302     alive   server  1.10.0  2         dc1  <all>
consul-server-0.dc6  192.168.103.235:8302  alive   server  1.10.0  2         dc6  <all>
consul-server-1.dc1  10.244.5.12:8302      alive   server  1.10.0  2         dc1  <all>
consul-server-1.dc6  192.168.103.236:8302  alive   server  1.10.0  2         dc6  <all>
consul-server-2.dc1  10.244.19.115:8302    alive   server  1.10.0  2         dc1  <all>
consul-server-2.dc6  192.168.103.237:8302  alive   server  1.10.0  2         dc6  <all>



## 查看Consul Services
docker exec -it consul-server-0 \
  consul catalog services

consul
mesh-gateway



## 查看Consul Nodes
docker exec -it consul-server-0 \
  consul catalog nodes

Node             ID        Address          DC
consul-server-0  50e9ba85  192.168.103.235  dc6
consul-server-1  285606a4  192.168.103.236  dc6
consul-server-2  96dc6f10  192.168.103.237  dc6
consul-client-0  d409e7a0  192.168.103.238  dc6




## 查看Server选举
docker exec -it consul-server-0 \
  consul operator raft list-peers

Node             ID                                    Address               State     Voter  RaftProtocol
consul-server-0  50e9ba85-0f0f-cd69-c0dc-55cacab5dbe5  192.168.103.235:8300  leader    true   3
consul-server-1  285606a4-df80-5f9d-a84f-b9090f5f0c1e  192.168.103.236:8300  follower  true   3
consul-server-2  96dc6f10-778b-93d2-d1e8-cd84b8440085  192.168.103.237:8300  follower  true   3




## 查看 mesh-gateway
curl -sk https://localhost:8501/v1/catalog/service/mesh-gateway | jq ".[].ServiceTaggedAddresses.wan"
{
  "Address": "192.168.103.238",
  "Port": 443
}

</all></all></all></all></all></all>
```

- - - - - -

- - - - - -

- - - - - -

###### **[测试](http://www.dev-share.top/2021/09/03/%e5%b0%86%e8%99%9a%e6%8b%9f%e6%9c%ba%e4%b8%ad%e5%ba%94%e7%94%a8%e7%a8%8b%e5%ba%8f%e5%8a%a0%e5%85%a5%e5%88%b0%e8%81%94%e9%82%a6%e6%9c%8d%e5%8a%a1%e7%bd%91%e6%a0%bc/ "测试")**

- - - - - -

- - - - - -

- - - - - -