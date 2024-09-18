---
title: "Consul联邦集群-接入IngressGateway"
date: "2021-11-05"
categories: 
  - "consul"
---

###### **前置条件**

###### **[基于K8S部署Consul联邦](%e5%9f%ba%e4%ba%8ek8s%e9%83%a8%e7%bd%b2consul%e8%81%94%e9%82%a6 "基于K8S部署Consul联邦")**

* * *

##### 接入IngressGateway， 两种配置方法

###### 第一种 让IngressGateway配置 **`多个`** 域名， 直接明确指向后端 **`services`**

```ruby
cat > ingress-gateway-config.yaml << ERIC

---
## (不会影响，跨数据中心通信)
apiVersion: consul.hashicorp.com/v1alpha1
kind: IngressGateway
metadata:
  name: ingress-gateway
spec:
  listeners:
#    - port: 80
#      protocol: http
#      services:
#        # 80端口通配所有服务
#        - name: '*'
    - port: 8080
      protocol: http
      # 配置8080端口，将不同的域名解析到相应的服务端
      services:
        - name: static-server
          hosts: ['static-server.com']
        - name: static-server-01
        - name: static-server-02
        - name: static-server-03
        - name: static-server-04
          hosts: ['static-server-04.com']
        - name: static-server-05

ERIC

```

* * *

###### 测试使用ingress-gateway后。 **不要忘记为`ingress-gateway`与`各service`添加`Intentions`**

```ruby
[root@master01 new_test]# kubectl --context dc2 -n dhc-consul get svc consul-ingress-gateway
NAME                     TYPE           CLUSTER-IP     EXTERNAL-IP       PORT(S)                         AGE
consul-ingress-gateway   LoadBalancer   10.96.109.69   192.168.103.254   8080:30285/TCP,8443:32684/TCP   158m
[root@master01 new_test]#


[root@master01 new_test]# curl -H "Host: static-server.com" "http://192.168.103.254:8080"
"hello world dc2-static-server"
[root@master01 new_test]#

[root@master01 new_test]# curl -H "Host: static-server-01.ingress.consul" "http://192.168.103.254:8080"
"hello world dc2-static-server"
[root@master01 new_test]#

```

* * *

* * *

* * *

* * *

* * *

* * *

###### 第二种 让IngressGateway配置 **`一个`** 域名指向路由， 让路由根据url指向不同的后端 **`services`**

```ruby
cat > ingress-gateway-config.yaml << ERIC

---
apiVersion: consul.hashicorp.com/v1alpha1
kind: IngressGateway
metadata:
  name: ingress-gateway
spec:
  listeners:
    - port: 8080
      protocol: http
      services:
        # 该virtual-router服务不是实际的注册服务，它仅作为 L7 配置的 "虚拟" 服务存在。
        # 它是将域名static-server.com指向了下面的ServiceRouter。
        # 使用下面的ServiceRouter基于URL路径， 路由到不同的后端服务
        - name: virtual-router
          hosts: ['static-server.com']

---
apiVersion: consul.hashicorp.com/v1alpha1
kind: ServiceRouter
metadata:
  name: virtual-router
spec:
  routes:
    - match:
        http:
          # URL地址(因为url的定义通常都会自定义前缀)
          pathPrefix: '/dhc0/time'
      destination:
        # 服务端实际地址
        prefixRewrite: '/time'
        # 服务请求超时时间
        requestTimeout: '10000s'
        # 服务
        service: static-server
    - match:
        http:
          pathPrefix: '/dhc1'
      destination:
        service: static-server-01
    - match:
        http:
          pathPrefix: '/dhc2'
      destination:
        service: static-server-02
    - match:
        http:
          pathPrefix: '/dhc3'
      destination:
        service: static-server-03
    - match:
        http:
          pathPrefix: '/dhc4'
      destination:
        service: static-server-04
    - match:
        http:
          pathPrefix: '/dhc5'
      destination:
        service: static-server-05
    - match:
        http:
          pathPrefix: '/dhc6'
      destination:
        service: static-server-06

ERIC

```

* * *

###### 测试

```ruby
[root@master01 new_test]# curl -H "Host: static-server.com" "http://192.168.103.253:8080"
no healthy upstream

[root@master01 new_test]# curl -H "Host: static-server.com" "http://192.168.103.253:8080/dhc0/time?timeout=16"
延迟时间：16

[root@master01 new_test]# curl -H "Host: static-server.com" "http://192.168.103.253:8080/dhc1"
"hello world 01"

[root@master01 new_test]# curl -H "Host: static-server.com" "http://192.168.103.253:8080/dhc2"
"hello world 02"

[root@master01 new_test]# curl -H "Host: static-server.com" "http://192.168.103.253:8080/dhc3"
"hello world 03"

[root@master01 new_test]# curl -H "Host: static-server.com" "http://192.168.103.253:8080/dhc4"
"hello world 04"

[root@master01 new_test]# curl -H "Host: static-server.com" "http://192.168.103.253:8080/dhc5"
"hello world 05"

[root@master01 new_test]# curl -H "Host: static-server.com" "http://192.168.103.253:8080/dhc6"
"hello world 06"

```

* * *

* * *

* * *
