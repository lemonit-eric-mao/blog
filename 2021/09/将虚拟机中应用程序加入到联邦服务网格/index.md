---
title: "将虚拟机中应用程序加入到联邦服务网格"
date: "2021-09-03"
categories: 
  - "consul"
---

###### 前置条件

**[Docker-Compose 基于虚拟机环境下 部署Consul联邦从集群](http://www.dev-share.top/2021/02/18/docker-compose-%e5%9f%ba%e4%ba%8e%e8%99%9a%e6%8b%9f%e6%9c%ba%e7%8e%af%e5%a2%83%e4%b8%8b-%e9%83%a8%e7%bd%b2consul%e8%81%94%e9%82%a6%e4%bb%8e%e9%9b%86%e7%be%a4/ "Docker-Compose 基于虚拟机环境下 部署Consul联邦从集群")**

* * *

##### 注意

**`注意`：一个主机必须要有一个 Client， 提供给当前主机的所有应用程序注册使用** **`注意`：应用程序必使用`Consul Client`执行注册命令才能进行注册**

* * *

###### **`一`** 创建 **`static-server`** 应用程序的 docker-compose文件

```ruby
cat > docker-compose.yaml << ERIC
version: '3.6'

services:

  static-server:
    image: hashicorp/http-echo:latest
    container_name: static-server
    ports:
      - 8080:8080
    command: |
      -text="hello world dc6-static-server"
      -listen=:8080

  # 启动边车程序
  envoy-sidecar:
    depends_on:
      - static-server
    image: envoyproxy/envoy-alpine:v1.18.3
    container_name: envoy-sidecar
    restart: always
    network_mode: host
    volumes:
      # 偷个懒使用Consul Client目录下的consul二进制
      - ../consul/config/consul-bin:/consul-bin
      # 偷个懒使用Consul Client目录下的证书
      - ../consul/config/certs:/opt/certs
    environment:
      # bootstrap token
      CONSUL_HTTP_TOKEN: 98e4ede4-271b-383b-94b7-c085137188fe
      CONSUL_CACERT: /opt/certs/consul-agent-ca.pem
      CONSUL_HTTP_ADDR: https://127.0.0.1:8501
      CONSUL_GRPC_ADDR: https://127.0.0.1:8502
    # -admin-bind 127.0.0.1:19001  绑定边车程序的健康检查端口， 用来告诉Consul如何检查边车程序，此端口每个应用程序各一个，不可重复
    command: |
      /consul-bin/consul connect envoy -sidecar-for static-server-0 -admin-bind 127.0.0.1:19001

ERIC

```

* * *

###### **`二`启动应用程序与边车**

```ruby
docker-compose up -d
```

* * *

###### **`三`将应用程序注册到Consul注册中心**

- **curl -k https://`Consul-Client-IP地址`:8501/v1/agent/service/register**
- **X-Consul-Token: 98e4ede4-271b-383b-94b7-c085137188fe `# 它是Bootstrap Token`**

```ruby
curl -k https://127.0.0.1:8501/v1/agent/service/register \
     --header "X-Consul-Token: 98e4ede4-271b-383b-94b7-c085137188fe" \
     --request PUT \
     --data '{
              "id": "static-server-0",
              "name": "static-server",
              "port": 8080,
              "connect": {
                  "sidecar_service": {}
              },
              "check": {
                  "http": "http://127.0.0.1:8080/health",
                  "method": "GET",
                  "interval": "1s",
                  "timeout": "1s"
              }
            }
     '

```

* * *

* * *

* * *

###### 反注册

- **curl -k https://Consul-Client-IP地址:8501/v1/agent/service/deregister/`ServiceID`**

```ruby
curl -k https://127.0.0.1:8501/v1/agent/service/deregister/static-server-0 \
     --header "X-Consul-Token: 98e4ede4-271b-383b-94b7-c085137188fe" \
     --request PUT
```

* * *

* * *

* * *

* * *

* * *

* * *

* * *

* * *

* * *

###### **`一`** 创建 **`static-client`** 应用程序的 docker-compose文件

```ruby
cat > docker-compose.yaml << ERIC
version: '3.6'

services:

  static-client:
    image: nginx:1.20-alpine
    container_name: static-client
    extra_hosts:
      - static-server:127.0.0.1
    network_mode: host

  # 启动边车程序
  envoy-sidecar-client:
    depends_on:
      - static-client
    image: envoyproxy/envoy-alpine:v1.18.3
    container_name: envoy-sidecar-client
    restart: always
    network_mode: host
    volumes:
      # 偷个懒使用Consul Client目录下的consul二进制
      - ../consul/config/consul-bin:/consul-bin
      # 偷个懒使用Consul Client目录下的证书
      - ../consul/config/certs:/opt/certs
    environment:
      # bootstrap token
      CONSUL_HTTP_TOKEN: 98e4ede4-271b-383b-94b7-c085137188fe
      CONSUL_CACERT: /opt/certs/consul-agent-ca.pem
      CONSUL_HTTP_ADDR: https://127.0.0.1:8501
      CONSUL_GRPC_ADDR: https://127.0.0.1:8502
    # -admin-bind 127.0.0.1:19001  绑定边车程序的健康检查端口， 用来告诉Consul如何检查边车程序，此端口每个应用程序各一个，不可重复
    command: |
      /consul-bin/consul connect envoy -sidecar-for static-client-0 -admin-bind 127.0.0.1:19002

ERIC

```

* * *

###### **`二`启动应用程序与边车**

```ruby
docker-compose up -d
```

* * *

###### **`三`将应用程序注册到Consul注册中心**

```ruby
curl -k https://127.0.0.1:8501/v1/agent/service/register \
     --header "X-Consul-Token: 98e4ede4-271b-383b-94b7-c085137188fe" \
     --request PUT \
     --data '{
              "id": "static-client-0",
              "name": "static-client",
              "port": 80,
              "connect": {
                  "sidecar_service": {
                      "proxy": {
                         "upstreams": [
                          {
                            "destination_name": "static-server",
                            "local_bind_port": 5000
                          }
                        ]
                      }
                  }
              },
              "check": {
                  "http": "http://127.0.0.1:80",
                  "method": "GET",
                  "interval": "1s",
                  "timeout": "1s"
              }
            }
     '

```

* * *

###### data.json说明

```json
......
     --data '{
              "id": "static-client-0",                              // 当前应用程序自己的信息
              "name": "static-client",
              "port": 80,
              "connect": {
                  "sidecar_service": {
                      "proxy": {
                         "upstreams": [                             // 告诉当前应用程序，想要连通的服务有哪些
                          {
                            "destination_name": "static-server",    // 指定要连通的服务名
                            "local_bind_port": 5000                 // 跨服务网格访问时需要这个端口，每个配置各一个，不能重复; 例如： curl -sS http://static-server:5000 被代理到远程服务的 http://static-server:8080
                          },
                          {
                            "destination_name": "demo-two",         // 如果添加多个服务访问，就这样配置
                            "local_bind_port": 5001
                          }
                        ]
                      }
                  }
              },
              "check": {
                  "http": "http://127.0.0.1:80",                    // 当前应用程序自己的健康检查的地址，给个可以返回 200的http连接就可以
                  "method": "GET",
                  "interval": "1s",
                  "timeout": "1s"
              }
            }
     '
```

* * *

* * *

* * *

###### 使用API创建 ServiceIntentions开放服务访问权限

```ruby
curl -k https://127.0.0.1:8501/v1/connect/intentions \
   --header "X-Consul-Token: 98e4ede4-271b-383b-94b7-c085137188fe" \
   --request POST \
   --data '{
               "SourceName": "static-client",
               "DestinationName": "static-server",
               "Action": "allow"
           }
   '

```

* * *

* * *

###### 使用API创建 ServiceResolver切换路由

```ruby
curl -k https://127.0.0.1:8501/v1/config \
   --header "X-Consul-Token: 98e4ede4-271b-383b-94b7-c085137188fe" \
   --request PUT \
   --data '{
              "Kind": "service-resolver",
              "Name": "static-server",
              "Redirect": {
                  "Service": "static-server",
                  "Datacenter": "dc2"
              },
              "Meta": {
                  "consul.hashicorp.com/source-datacenter": "dc1",
                  "external-source": "kubernetes"
              }
          }
   '

```

* * *

* * *

###### 测试跨注册中心访问 **static-client --> static-server**

```ruby
docker exec -it static-client curl -sS http://127.0.0.1:5000
"hello world dc2-static-server"


docker exec -it static-client curl -sS http://static-server:5000
"hello world dc2-static-server"

```

* * *

* * *

* * *

* * *

* * *

* * *

##### 常用API

###### **注册空服务的做法**

**注册空服务的作用， 是为了解决跨不同数据中心， 进行服务访问， 因为跨数据中心访问当前集群的服务网格中， 必须要有一个对应的服务信息注册， 但本地并不需要一个真正的服务， 所以在本地可以注册一个空服务来满足路由的跳转功能**

```ruby
curl -k https://127.0.0.1:8501/v1/agent/service/register \
     --header "X-Consul-Token: 98e4ede4-271b-383b-94b7-c085137188fe" \
     --request PUT \
     --data '{
              "id": "static-server-0",
              "name": "static-server",
              "port": 8080,
              "connect": {
                  "sidecar_service": {}
              }
            }
     '

```

* * *

###### 反注册

```ruby
curl -k https://127.0.0.1:8501/v1/agent/service/deregister/static-client-0 \
     --header "X-Consul-Token: 98e4ede4-271b-383b-94b7-c085137188fe" \
     --request PUT
```

* * *

###### 删除ServiceResolver

```ruby
curl -k https://127.0.0.1:8501/v1/config/service-resolver/static-server \
   --header "X-Consul-Token: 98e4ede4-271b-383b-94b7-c085137188fe" \
   --request DELETE
```

* * *

###### 查看ServiceResolver

```ruby
curl -k https://127.0.0.1:8501/v1/config/service-resolver \
   --header "X-Consul-Token: 98e4ede4-271b-383b-94b7-c085137188fe" \
   --request GET
```

* * *

* * *

* * *

* * *

* * *

* * *
