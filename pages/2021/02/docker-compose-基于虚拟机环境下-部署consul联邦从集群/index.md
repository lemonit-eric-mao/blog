---
title: "docker-compose 基于虚拟机环境下 部署Consul联邦从集群"
date: "2021-02-18"
categories: 
  - "consul"
---

###### **[单节点部署及说明](http://www.dev-share.top/2021/02/10/docker-compose-%e9%83%a8%e7%bd%b2-consul-%e5%8d%95%e8%8a%82%e7%82%b9/ "单节点部署及说明")**

* * *

* * *

* * *

###### 前置条件

| 集群 | 服务名 | IP |
| --- | --- | --- |
| 联邦 **K8s`主`** 集群 | primary\_gateways | 192.168.103.253:443 |
| 联邦 **虚机`从`** 集群 | consul-server-0 | 192.168.103.235 |
| 联邦 **虚机`从`** 集群 | consul-server-1 | 192.168.103.236 |
| 联邦 **虚机`从`** 集群 | consul-server-2 | 192.168.103.237 |
| 联邦 **虚机`从`** 集群 | consul-client-0 | 192.168.103.238 |

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

* * *

* * *

* * *

##### 创建文件夹

```ruby
mkdir -p /home/deploy/consul/config/certs/ /home/deploy/consul/config/hcls

cd /home/deploy/consul/

```

* * *

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

* * *

#### **部署从集群的 consul-server-`0`**

```ruby
hostnamectl set-hostname consul-server-0
```

* * *

###### 从集群的 consul-server-0配置文件

```ruby
cat > config/hcls/consul.hcl << ERIC
# From above
cert_file = "/opt/certs/dc6-server-consul-0.pem"
key_file = "/opt/certs/dc6-server-consul-0-key.pem"
ca_file = "/opt/certs/consul-agent-ca.pem"
primary_datacenter = "dc1"
primary_gateways = ["192.168.103.253:443"]
acl {
  enabled = true
  default_policy = "deny"
  down_policy = "extend-cache"
  tokens {
    # 联邦主集群的consul-server-0的agent-token
    agent = "c15001f7-ee9f-d277-bd67-588d1e5d7cdd"
    # 这个Token必须有，它是从联邦主集群中获取到的，用于同步联邦主集群中的Token、Policies
    replication = "17744abc-7008-5278-5525-9c37df7ee2ae"
  }
}
encrypt = "PQbbZH+XboiMdkF7K8Dv3ZENe+15UIcEdVg/twLnYFo="


# Other server settings
server = true
datacenter = "dc6"
data_dir = "/opt/consul"
enable_central_service_config = true
connect {
  enabled = true
  enable_mesh_gateway_wan_federation = true
}
verify_incoming_rpc = true
verify_outgoing = true
verify_server_hostname = true
ports {
  https = 8501
  http = -1
  grpc = 8502
}


bind_addr = "192.168.103.235"
client_addr = "0.0.0.0"
ui_config {
    enabled = true
}
# 主集群独有
bootstrap_expect = 3


ERIC

```

* * *

###### 从集群的 consul-server-0

```ruby
cat > docker-compose.yaml << ERIC
version: '3.6'

services:
  # 启动 consul 服务端
  consul-server-0:
    image: hashicorp/consul:1.10.0
    container_name: consul-server-0
    restart: always
    network_mode: host
    volumes:
      - ./config/certs:/opt/certs
      - ./config/hcls:/opt/hcls
    environment:
      # bootstrap token
      CONSUL_HTTP_TOKEN: 98e4ede4-271b-383b-94b7-c085137188fe
      CONSUL_CACERT: /opt/certs/consul-agent-ca.pem
      CONSUL_HTTP_ADDR: https://127.0.0.1:8501
      CONSUL_GRPC_ADDR: https://127.0.0.1:8502
    command: |
      agent
        -config-dir=/opt/hcls/consul.hcl

ERIC


docker-compose up -d

```

* * *

* * *

* * *

* * *

* * *

* * *

#### **部署从集群的 consul-server-`1`**

```ruby
hostnamectl set-hostname consul-server-1
```

* * *

##### 创建文件夹

```ruby
mkdir -p /home/deploy/consul/config/certs/ /home/deploy/consul/config/hcls

cd /home/deploy/consul/

```

* * *

###### 将consul-server-0的config/certs/\*.pem 复制到当前config/certs/

```ruby
scp 192.168.103.235:/home/deploy/consul/config/certs/*.pem  config/certs/
```

* * *

##### 从集群的 consul-server-1配置文件

```ruby
cat > config/hcls/consul.hcl << ERIC
# From above
cert_file = "/opt/certs/dc6-server-consul-1.pem"
key_file = "/opt/certs/dc6-server-consul-1-key.pem"
ca_file = "/opt/certs/consul-agent-ca.pem"
primary_datacenter = "dc1"
primary_gateways = ["192.168.103.253:443"]
acl {
  enabled = true
  default_policy = "deny"
  down_policy = "extend-cache"
  tokens {
    # 联邦主集群的consul-server-1的agent-token
    agent = "50fd947f-ddaf-ba24-7106-b4c462d747cf"
    replication = "17744abc-7008-5278-5525-9c37df7ee2ae"
  }
}
encrypt = "PQbbZH+XboiMdkF7K8Dv3ZENe+15UIcEdVg/twLnYFo="


# Other server settings
server = true
datacenter = "dc6"
data_dir = "/opt/consul"
enable_central_service_config = true
connect {
  enabled = true
  enable_mesh_gateway_wan_federation = true
}
verify_incoming_rpc = true
verify_outgoing = true
verify_server_hostname = true
ports {
  https = 8501
  http = -1
  grpc = 8502
}


bind_addr = "192.168.103.236"
client_addr = "0.0.0.0"
ui_config {
    enabled = false
}


# 从集群独有
retry_join = ["192.168.103.235"]


ERIC

```

* * *

##### 从集群的 consul-server-1

```ruby
cat > docker-compose.yaml << ERIC
version: '3.6'

services:
  consul-server-1:
    image: hashicorp/consul:1.10.0
    container_name: consul-server-1
    restart: always
    network_mode: host
    volumes:
      - ./config/certs:/opt/certs
      - ./config/hcls:/opt/hcls
    environment:
      # bootstrap token
      CONSUL_HTTP_TOKEN: 98e4ede4-271b-383b-94b7-c085137188fe
      CONSUL_CACERT: /opt/certs/consul-agent-ca.pem
      CONSUL_HTTP_ADDR: https://127.0.0.1:8501
      CONSUL_GRPC_ADDR: https://127.0.0.1:8502
    command: |
      agent
        -config-dir=/opt/hcls/consul.hcl

ERIC


docker-compose up -d

```

* * *

* * *

* * *

* * *

* * *

* * *

#### **部署从集群的 consul-server-`2`**

```ruby
hostnamectl set-hostname consul-server-2
```

* * *

##### 创建文件夹

```ruby
mkdir -p /home/deploy/consul/config/certs/ /home/deploy/consul/config/hcls

cd /home/deploy/consul/

```

* * *

###### 将consul-server-0的config/certs/\*.pem 复制到当前config/certs/

```ruby
scp 192.168.103.235:/home/deploy/consul/config/certs/*.pem  config/certs/
```

* * *

##### 从集群的 consul-server-2配置文件

```ruby
cat > config/hcls/consul.hcl << ERIC
# From above
cert_file = "/opt/certs/dc6-server-consul-2.pem"
key_file = "/opt/certs/dc6-server-consul-2-key.pem"
ca_file = "/opt/certs/consul-agent-ca.pem"
primary_datacenter = "dc1"
primary_gateways = ["192.168.103.253:443"]
acl {
  enabled = true
  default_policy = "deny"
  down_policy = "extend-cache"
  tokens {
    # 联邦主集群的consul-server-2的agent-token
    agent = "b61e2014-44d1-8b3b-d376-91537d210491"
    replication = "17744abc-7008-5278-5525-9c37df7ee2ae"
  }
}
encrypt = "PQbbZH+XboiMdkF7K8Dv3ZENe+15UIcEdVg/twLnYFo="


# Other server settings
server = true
datacenter = "dc6"
data_dir = "/opt/consul"
enable_central_service_config = true
connect {
  enabled = true
  enable_mesh_gateway_wan_federation = true
}
verify_incoming_rpc = true
verify_outgoing = true
verify_server_hostname = true
ports {
  https = 8501
  http = -1
  grpc = 8502
}


bind_addr = "192.168.103.237"
client_addr = "0.0.0.0"
ui_config {
    enabled = false
}


# 从集群独有
retry_join = ["192.168.103.235"]


ERIC

```

* * *

##### 从集群的 consul-server-2

```ruby
cat > docker-compose.yaml << ERIC
version: '3.6'

services:
  consul-server-2:
    image: hashicorp/consul:1.10.0
    container_name: consul-server-2
    restart: always
    network_mode: host
    volumes:
      - ./config/certs:/opt/certs
      - ./config/hcls:/opt/hcls
    environment:
      # bootstrap token
      CONSUL_HTTP_TOKEN: 98e4ede4-271b-383b-94b7-c085137188fe
      CONSUL_CACERT: /opt/certs/consul-agent-ca.pem
      CONSUL_HTTP_ADDR: https://127.0.0.1:8501
      CONSUL_GRPC_ADDR: https://127.0.0.1:8502
    command: |
      agent
        -config-dir=/opt/hcls/consul.hcl

ERIC


docker-compose up -d

```

* * *

* * *

* * *

#### 在任意consul-server端为consul-clinet创建(Policy 与 Token)

###### 创建Policy文件

```hcl
cat > config/hcls/client-token.hcl << ERIC
node_prefix "" {
  policy = "write"
}
service_prefix "" {
  policy = "read"
}

ERIC

```

* * *

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

* * *

* * *

* * *

* * *

* * *

* * *

#### **部署从集群的 consul-client-`0`**

```ruby
hostnamectl set-hostname consul-client-0
```

* * *

##### 创建文件夹

```ruby
mkdir -p /home/deploy/consul/config/consul-bin/ /home/deploy/consul/config/certs/ /home/deploy/consul/config/hcls

cd /home/deploy/consul/

```

* * *

###### 将consul-server-0的`config/certs/*.pem` 复制到当前`config/certs/`

```ruby
scp 192.168.103.235:/home/deploy/consul/config/certs/*.pem  config/certs/
```

* * *

##### 从集群的 consul-client-0配置文件

```ruby
cat > config/hcls/consul.hcl << ERIC
# From above
cert_file = "/opt/certs/dc6-client-consul-0.pem"
key_file = "/opt/certs/dc6-client-consul-0-key.pem"
ca_file = "/opt/certs/consul-agent-ca.pem"
primary_datacenter = "dc1"
acl {
  enabled = true
  default_policy = "deny"
  down_policy = "extend-cache"
  tokens {
    # 由上面consul-server-2手动创建出来的，创建一次即可，所有client共用
    agent = "2796b1d7-f05b-8106-f735-da7cd07e584a"
    replication = "17744abc-7008-5278-5525-9c37df7ee2ae"
  }
}
encrypt = "PQbbZH+XboiMdkF7K8Dv3ZENe+15UIcEdVg/twLnYFo="


# Other server settings
datacenter = "dc6"
data_dir = "/opt/consul"
enable_central_service_config = true
connect {
  enabled = true
}
verify_incoming_rpc = true
verify_outgoing = true
verify_server_hostname = true
ports {
  https = 8501
  http = -1
  grpc = 8502
}


bind_addr = "192.168.103.238"
client_addr = "0.0.0.0"
ui_config {
    enabled = true
}


retry_join = ["192.168.103.235"]

ERIC

```

* * *

##### 从集群的 consul-client-0并且加入mesh-gateway

```ruby
cat > docker-compose.yaml << ERIC
version: '3.6'

services:

  # 复制consul给envoy用
  copy-consul-bin:
    image: hashicorp/consul:1.10.0
    container_name: copy-consul-bin
    volumes:
      - ./config/consul-bin:/consul-bin
    command: |
      cp
        /bin/consul
        /consul-bin/consul

  consul-client-0:
    depends_on:
      - copy-consul-bin
    image: hashicorp/consul:1.10.0
    container_name: consul-client-0
    restart: always
    network_mode: host
    volumes:
      - ./config/certs:/opt/certs
      - ./config/hcls:/opt/hcls
    environment:
      # bootstrap token
      CONSUL_HTTP_TOKEN: 98e4ede4-271b-383b-94b7-c085137188fe
      CONSUL_CACERT: /opt/certs/consul-agent-ca.pem
      CONSUL_HTTP_ADDR: https://127.0.0.1:8501
      CONSUL_GRPC_ADDR: https://127.0.0.1:8502
    command:  |
      agent -config-dir=/opt/hcls/consul.hcl

  # 启动 服务网格
  mesh-gateway:
    depends_on:
      - consul-client-0
    image: envoyproxy/envoy-alpine:v1.18.3
    container_name: mesh-gateway
    restart: always
    network_mode: host
    volumes:
      - ./config/consul-bin:/consul-bin
      - ./config/certs:/opt/certs
    environment:
      # bootstrap token
      CONSUL_HTTP_TOKEN: 98e4ede4-271b-383b-94b7-c085137188fe
      CONSUL_CACERT: /opt/certs/consul-agent-ca.pem
      CONSUL_HTTP_ADDR: https://127.0.0.1:8501
      CONSUL_GRPC_ADDR: https://127.0.0.1:8502
    # 这里必须要覆盖entrypoint，覆盖它原始的启动命令
    entrypoint: |
      /consul-bin/consul connect envoy
        -mesh-gateway
        -register
        -expose-servers
        -service mesh-gateway
        -address 192.168.103.238:8443
        -wan-address 192.168.103.238:443
        -admin-bind 127.0.0.1:19000

ERIC


docker-compose up -d

```

* * *

* * *

* * *

* * *

* * *

* * *

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

```

* * *

* * *

* * *

###### **[测试](http://www.dev-share.top/2021/09/03/%e5%b0%86%e8%99%9a%e6%8b%9f%e6%9c%ba%e4%b8%ad%e5%ba%94%e7%94%a8%e7%a8%8b%e5%ba%8f%e5%8a%a0%e5%85%a5%e5%88%b0%e8%81%94%e9%82%a6%e6%9c%8d%e5%8a%a1%e7%bd%91%e6%a0%bc/ "测试")**

* * *

* * *

* * *
