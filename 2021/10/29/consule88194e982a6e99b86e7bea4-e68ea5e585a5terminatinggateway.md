---
title: Consul联邦集群-接入TerminatingGateway
date: '2021-10-29T07:08:12+00:00'
status: private
permalink: /2021/10/29/consul%e8%81%94%e9%82%a6%e9%9b%86%e7%be%a4-%e6%8e%a5%e5%85%a5terminatinggateway
author: 毛巳煜
excerpt: ''
type: post
id: 8072
category:
    - Consul
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### **前置条件**

###### **[基于K8S部署Consul联邦](http://www.dev-share.top/2021/03/10/%e5%9f%ba%e4%ba%8ek8s%e9%83%a8%e7%bd%b2consul%e8%81%94%e9%82%a6/ "基于K8S部署Consul联邦")**

- - - - - -

###### **[Terminating Gateways on Kubernetes](https://www.consul.io/docs/k8s/connect/terminating-gateways "Terminating Gateways on Kubernetes")**

- - - - - -

###### 环境

<table><thead><tr><th align="center">DataCenter</th><th align="center">HostName</th><th align="center">IP</th><th align="center">CPU</th><th align="center">MEM</th><th align="center">命令</th></tr></thead><tbody><tr><td align="center">**DC1**</td><td align="center">**`master01`**</td><td align="center">192.168.103.227</td><td align="center">4 Core</td><td align="center">8G</td><td align="center">hostnamectl set-hostname master01</td></tr><tr><td align="center">**DC1**</td><td align="center">worker01</td><td align="center">192.168.103.228</td><td align="center">4 Core</td><td align="center">8G</td><td align="center">hostnamectl set-hostname worker01</td></tr><tr><td align="center">**DC1**</td><td align="center">worker02</td><td align="center">192.168.103.229</td><td align="center">4 Core</td><td align="center">8G</td><td align="center">hostnamectl set-hostname worker02</td></tr><tr><td align="center">**DC1**</td><td align="center">worker03</td><td align="center">192.168.103.230</td><td align="center">4 Core</td><td align="center">8G</td><td align="center">hostnamectl set-hostname worker03</td></tr><tr><td align="center">---</td><td align="center">---</td><td align="center">---</td><td align="center">---</td><td align="center">---</td><td align="center">---</td></tr><tr><td align="center">虚拟机</td><td align="center">worker04</td><td align="center">192.168.103.226</td><td align="center">4 Core</td><td align="center">8G</td><td align="center">hostnamectl set-hostname worker04</td></tr></tbody></table>

- - - - - -

###### 将 Consul Bootstrap ACL Token 放到虚拟机worker04的全局变量中

```ruby
export CONSUL_HTTP_TOKEN=c3dbc8f5-6234-8ccc-4bb5-69050a6a6b52


```

- - - - - -

- - - - - -

- - - - - -

###### 1. 在k8s集群 `master01`节点上，**`执行端口转发命令`**

```ruby
[root@master01 ~]# kubectl -n dhc-consul port-forward consul-server-0 --address=192.168.103.227 8501

Forwarding from 192.168.103.227:8501 -> 8501


## 或者选择后台运行
[root@master01 ~]# nohup kubectl -n dhc-consul port-forward consul-server-0 --address=192.168.103.227 8501 &


```

- - - - - -

###### 2. 在虚拟机`worker04`上，测试k8s集群master01节点的8501端口是否可以通信

```ruby
[root@worker04 ~]# nc -v 192.168.103.227 8501

Ncat: Version 7.50 ( https://nmap.org/ncat )
Ncat: Connected to 192.168.103.227:8501.


```

- - - - - -

###### 3. 在虚拟机`worker04`上，执行curl命令，向Consul注册服务，并且它会在Consul中自动创建一个名为worker04的Nodes

```ruby
## 服务的名称是随便起的，但通常是用来描述你虚拟机上运行的服务的名称
curl -k https://192.168.103.227:8501/v1/catalog/register \
     --header "X-Consul-Token: $CONSUL_HTTP_TOKEN" \
     --request PUT \
     --data '{
               "Datacenter": "dc1",
               "Node": "worker04",
               "Address": "192.168.103.226",
               "NodeMeta": {
                 "external-node": "true",
                 "external-probe": "true"
               },
               "Service": {
                 "Address": "192.168.103.226",
                 "ID": "terminating-gateway-test",
                 "Service": "terminating-gateway-test",
                 "Port": 8080
               }
             }
     '


```

- - - - - -

###### 4. 在虚拟机`worker04`上，执行curl命令，为terminating-gateway-test服务，创建Policy

```ruby
curl -k https://192.168.103.227:8501/v1/acl/policy \
     --header "X-Consul-Token: $CONSUL_HTTP_TOKEN" \
     --request PUT \
     --data '{
               "Datacenters": ["dc1"],
               "Name": "terminating-gateway-test",
               "Description": "terminating-gateway-test Policy",
               "Rules": "service \"terminating-gateway-test\" { policy = \"write\" }"
             }
     ' | jq


```

###### 5. 在k8s集群 `master01`节点上执行，获取 terminating-gateway网关的Token

```ruby
[root@master01 ~]# kubectl -n dhc-consul exec -it daemonset/consul -- sh -c \
                        "consul acl token list --token=$CONSUL_HTTP_TOKEN | \
                         grep -B 6 -- '- terminating-gateway-terminating-gateway-token' | \
                         grep AccessorID"

## 输出如下信息
AccessorID:       4041bd8f-e806-5b0a-4d71-358ada42b231
[root@master01 ~]#

```

- - - - - -

###### 6. 在k8s集群 `master01`节点上执行，更新terminating-gateway网关的Token，加入上面创建的叫做`terminating-gateway-test`的Policy

```ruby
[root@master01 ~]# kubectl -n dhc-consul exec -it daemonset/consul -- sh -c \
                        "consul acl token update \
                          --token=$CONSUL_HTTP_TOKEN -id 4041bd8f-e806-5b0a-4d71-358ada42b231 \
                          -policy-name terminating-gateway-test \
                          -merge-policies \
                          -merge-roles \
                          -merge-service-identities"

## 输出如下信息
AccessorID:       4041bd8f-e806-5b0a-4d71-358ada42b231
SecretID:         a72ab856-b8a1-d368-f85a-e0add25ce63f
Description:      terminating-gateway-terminating-gateway-token Token
Local:            true
Create Time:      2021-11-01 07:06:29.86788872 +0000 UTC
Policies:
   78153ee3-362a-b601-38d0-b7c5cd82b7d9 - terminating-gateway-terminating-gateway-token
   c6b3d084-fd37-9386-bff5-ba492c5db518 - terminating-gateway-test


```

- - - - - -

###### 7. 在k8s集群 `master01`节点上执行，配置TerminatingGateway

```ruby
cat > terminating-gateway.yaml 
```

- - - - - -

###### 8. 在虚拟机`worker04`上，启动服务端，创建docker-compose.yaml

```ruby
cat > docker-compose.yaml 
```

- - - - - -

- - - - - -

- - - - - -

###### 9. 在k8s集群 `master01`节点上，创建客户端用来测试

```ruby
cat > static-client.yaml 
```

- - - - - -

###### 10. 在k8s集群 `master01`节点上，测试连通

```ruby
[root@master01 new_test]# kubectl exec deploy/static-client -- curl -sS -H "Host: terminating-gateways-test" http://127.0.0.1:8080
hello world VM-terminating-gateways-test


[root@master01 new_test]# kubectl exec deploy/static-client -- curl -sS http://127.0.0.1:8080
hello world VM-terminating-gateways-test


```

- - - - - -

- - - - - -

- - - - - -

##### **常用命令**

###### 反注册

```ruby
## 删除 Service
curl -k https://192.168.103.227:8501/v1/catalog/deregister \
     --header "X-Consul-Token: $CONSUL_HTTP_TOKEN" \
     --request PUT \
     --data '{
               "Datacenter": "dc1",
               "Node": "worker04",
               "ServiceID": "terminating-gateway-test"
             }
     '

```

- - - - - -

```ruby
## 删除 Node
curl -k https://192.168.103.227:8501/v1/catalog/deregister \
     --header "X-Consul-Token: $CONSUL_HTTP_TOKEN" \
     --request PUT \
     --data '{
               "Datacenter": "dc1",
               "Node": "worker04"
             }
     '

```

- - - - - -

- - - - - -

- - - - - -