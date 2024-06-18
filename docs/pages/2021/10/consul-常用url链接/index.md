---
title: "Consul 常用url链接"
date: "2021-10-26"
categories: 
  - "consul"
---

##### **[官方Api文档](https://www.consul.io/api-docs "官方Api文档")**

* * *

* * *

* * *

###### 添加全局环境变量， 设置Bootstrap Token

```ruby
export CONSUL_HTTP_TOKEN=c3dbc8f5-6234-8ccc-4bb5-69050a6a6b52
```

* * *

#### 如下请求需要在 Consul Client中执行

###### config 查询

```ruby
curl -sk https://127.0.0.1:8501/v1/config/service-resolver \
   --header "X-Consul-Token: $CONSUL_HTTP_TOKEN" \
   --request GET | jq
```

* * *

```ruby
## 查所有路由
curl -sk https://127.0.0.1:8501/v1/config/service-router \
   --header "X-Consul-Token: $CONSUL_HTTP_TOKEN" \
   --request GET | jq
```

* * *

```ruby
## 查指定路由
curl -sk https://127.0.0.1:8501/v1/config/service-router/static-server \
   --header "X-Consul-Token: $CONSUL_HTTP_TOKEN" \
   --request GET | jq
```

* * *

```ruby
## 查所有 service-defaults
curl -sk https://127.0.0.1:8501/v1/config/service-defaults \
   --header "X-Consul-Token: $CONSUL_HTTP_TOKEN" \
   --request GET | jq
```

* * *

```ruby
## 查指定 service-defaults
curl -sk https://127.0.0.1:8501/v1/config/service-defaults/static-server \
   --header "X-Consul-Token: $CONSUL_HTTP_TOKEN" \
   --request GET | jq
```

* * *

```ruby
curl -sk https://127.0.0.1:8501/v1/config/proxy-defaults \
   --header "X-Consul-Token: $CONSUL_HTTP_TOKEN" \
   --request GET | jq
```

* * *

```ruby
curl -sk https://127.0.0.1:8501/v1/config/mesh \
   --header "X-Consul-Token: $CONSUL_HTTP_TOKEN" \
   --request GET | jq
```

* * *

* * *

* * *

###### catalog 查询

```ruby
curl -sk https://127.0.0.1:8501/v1/catalog/services \
     --header "X-Consul-Token: $CONSUL_HTTP_TOKEN" \
     --request GET | jq
```

* * *

```ruby
## 查询应用程序信息
curl -sk https://127.0.0.1:8501/v1/catalog/service/static-client \
     --header "X-Consul-Token: $CONSUL_HTTP_TOKEN" \
     --request GET | jq
```

* * *

```ruby
## 查询应用程序边车的信息
curl -sk https://127.0.0.1:8501/v1/catalog/service/static-client-sidecar-proxy \
     --header "X-Consul-Token: $CONSUL_HTTP_TOKEN" \
     --request GET | jq
```

* * *

```ruby
## 向 Consul 注册服务
curl -sk https://127.0.0.1:8501/v1/catalog/register \
     --header "X-Consul-Token: $CONSUL_HTTP_TOKEN" \
     --request PUT \
     --data '{
               "Datacenter": "dc1",
               "Node": "terminating-gateway-test",
               "Address": "192.168.103.226",
               "NodeMeta": {
                 "external-node": "true",
                 "external-probe": "true"
               },
               "Service": {
                 "Address": "192.168.103.226",
                 "ID": "terminating-gateway-test",
                 "Service": "terminating-gateway-test",
                 "Port": 80
               },
               "Check": {
                 "Node": "terminating-gateway-test",
                 "Name": "terminating-gateway-test health check",
                 "Status": "passing",
                 "ServiceID": "terminating-gateway-test",
                 "Definition": {
                   "TCP": "192.168.103.226:80",
                   "Interval": "5s",
                   "Timeout": "1s",
                   "DeregisterCriticalServiceAfter": "30s"
                 }
               }
             }
     '
```

* * *

```ruby
## 反注册， 删除 Service
curl -sk https://127.0.0.1:8501/v1/catalog/deregister \
     --header "X-Consul-Token: $CONSUL_HTTP_TOKEN" \
     --request PUT \
     --data '{
               "Datacenter": "dc1",
               "Node": "worker04",
               "ServiceID": "terminating-gateway-test"
             }
     '
```

* * *

```ruby
## 反注册， 删除 Node
curl -sk https://127.0.0.1:8501/v1/catalog/deregister \
     --header "X-Consul-Token: $CONSUL_HTTP_TOKEN" \
     --request PUT \
     --data '{
               "Datacenter": "dc1",
               "Node": "worker04"
             }
     '
```

* * *

* * *

* * *

###### agent 查询

**`注意`:** 应用程序是注册到不同的 client, 所以要查看应用程序的agent, 还需要去相应的consul-client上去找, 不是每个consul-client上都可以找的到

```ruby
curl -sk https://127.0.0.1:8501/v1/agent/services \
     --header "X-Consul-Token: $CONSUL_HTTP_TOKEN" \
     --request GET | jq
```

* * *

```ruby
## 根据Service ID进行查询
curl -sk https://127.0.0.1:8501/v1/agent/service/static-server-01-6d4f8d997d-dxq9b-static-server-01-sidecar-proxy \
     --header "X-Consul-Token: $CONSUL_HTTP_TOKEN" \
     --request GET | jq
```

* * *

```ruby
curl -sk https://127.0.0.1:8501/v1/agent/checks \
     --header "X-Consul-Token: $CONSUL_HTTP_TOKEN" \
     --request GET | jq
```

* * *

```ruby
curl -sk https://127.0.0.1:8501/v1/catalog/service/learn \
     --header "X-Consul-Token: $CONSUL_HTTP_TOKEN" \
     --request GET | jq
```

* * *

* * *

* * *

##### acl

```ruby
## 创建 Policy
curl -sk https://127.0.0.1:8501/v1/acl/policy \
     --header "X-Consul-Token: $CONSUL_HTTP_TOKEN" \
     --request PUT \
     --data '{
               "Name": "terminating-gateway-test",
               "Description": "terminating-gateway-test Policy",
               "Datacenters": ["dc1"],
               "Rules": "service \"terminating-gateway-test\" { policy = \"write\" }"
             }
     '
```

* * *

```ruby
## 关联Policy，并创建 Token
curl -sk https://127.0.0.1:8501/v1/acl/token \
     --header "X-Consul-Token: $CONSUL_HTTP_TOKEN" \
     --request PUT \
     --data '{
               "Description": "terminating-gateway-test Policy Token",
               "Policies": [
                 {
                   "Name": "terminating-gateway-test"
                 }
               ],
               "Local": false
             }
     '
```

* * *

* * *

* * *

* * *

* * *

* * *

##### 如下请求需要在 xxx-gateway 的 consul-sidecar中执行

- consul-mesh-gateway --> consul-sidecar
- consul-ingress-gateway --> consul-sidecar
- consul-terminating-gateway --> consul-sidecar

###### 例如

```ruby
/ $ curl http://localhost:19000/help
admin commands are:
  /: Admin home page
  /certs: print certs on machine
  /clusters: upstream cluster status
  /config_dump: dump current Envoy configs (experimental)
  /contention: dump current Envoy mutex contention stats (if enabled)
  /cpuprofiler: enable/disable the CPU profiler
  /drain_listeners: drain listeners
  /healthcheck/fail: cause the server to fail health checks
  /healthcheck/ok: cause the server to pass health checks
  /heapprofiler: enable/disable the heap profiler
  /help: print out list of admin commands
  /hot_restart_version: print the hot restart compatibility version
  /init_dump: dump current Envoy init manager information (experimental)
  /listeners: print listener info
  /logging: query/change logging levels
  /memory: print current allocation/heap usage
  /quitquitquit: exit the server
  /ready: print server state, return 200 if LIVE, otherwise return 503
  /reopen_logs: reopen access logs
  /reset_counters: reset all counters to zero
  /runtime: print runtime values
  /runtime_modify: modify runtime values
  /server_info: print server version/status information
  /stats: print server stats
  /stats/prometheus: print server stats in prometheus format
  /stats/recentlookups: Show recent stat-name lookups
  /stats/recentlookups/clear: clear list of stat-name lookups and counter
  /stats/recentlookups/disable: disable recording of reset stat-name lookup names
  /stats/recentlookups/enable: enable recording of reset stat-name lookup names
/ $


curl http://localhost:19000/config_dump
```

* * *

* * *

* * *
