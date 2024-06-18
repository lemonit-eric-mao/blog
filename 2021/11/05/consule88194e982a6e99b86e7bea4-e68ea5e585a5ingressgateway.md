---
title: Consul联邦集群-接入IngressGateway
date: '2021-11-05T03:31:33+00:00'
status: private
permalink: /2021/11/05/consul%e8%81%94%e9%82%a6%e9%9b%86%e7%be%a4-%e6%8e%a5%e5%85%a5ingressgateway
author: 毛巳煜
excerpt: ''
type: post
id: 8118
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

##### 接入IngressGateway， 两种配置方法

###### 第一种 让IngressGateway配置 **`多个`** 域名， 直接明确指向后端 **`services`**

```ruby
cat > ingress-gateway-config.yaml 
```

- - - - - -

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

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

###### 第二种 让IngressGateway配置 **`一个`** 域名指向路由， 让路由根据url指向不同的后端 **`services`**

```ruby
cat > ingress-gateway-config.yaml 
```

- - - - - -

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

- - - - - -

- - - - - -

- - - - - -