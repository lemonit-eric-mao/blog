---
title: '使用 Helm 3 安装 Nginx Ingress Controller'
date: '2020-07-17T09:03:20+00:00'
status: publish
permalink: /2020/07/17/%e4%bd%bf%e7%94%a8-helm-3-%e5%ae%89%e8%a3%85-nginx-ingress-controller
author: 毛巳煜
excerpt: ''
type: post
id: 5374
category:
    - Kubernetes
    - nginx
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
资料
--

- **[详解 Ingress](http://www.dev-share.top/2019/03/15/k8s-%e9%85%8d%e7%bd%ae-ingress%e5%ae%9a%e4%b9%89%e7%9a%84%e8%b7%af%e7%94%b1%e8%a7%84%e5%88%99%e9%9b%86/ "详解 Ingress")**
- **[K8s官网 Ingress 控制器](https://kubernetes.io/zh-cn/docs/concepts/services-networking/ingress-controllers/ "K8s官网 Ingress 控制器")**
- **[安装 Helm](http://www.dev-share.top/2020/07/16/helm-%e5%ae%89%e8%a3%85-%e4%bd%bf%e7%94%a8/ "安装 Helm")**
- **[官网安装 Nginx Ingress Controller](https://kubernetes.github.io/ingress-nginx/deploy/#quick-start "官网安装 Nginx Ingress Controller")**
- **[Github charts 源码（含values配置参数）](https://github.com/kubernetes/ingress-nginx/tree/main/charts/ingress-nginx)**
- **[K8s和ingress-controller版本对照关系](https://github.com/kubernetes/ingress-nginx#supported-versions-table)**

<table><thead><tr><th>**Ingress-NGINX version**</th><th>**k8s supported version**</th><th>**Alpine Version**</th><th>**Nginx Version**</th></tr></thead><tbody><tr><td>v1.5.1</td><td>1.25, 1.24, 1.23</td><td>3.16.2</td><td>1.21.6</td></tr><tr><td>v1.4.0</td><td>1.25, 1.24, 1.23, 1.22</td><td>3.16.2</td><td>1.19.10†</td></tr><tr><td>**`v1.3.1`**</td><td>**1.24, 1.23, 1.22, 1.21, `1.20`**</td><td>**3.16.2**</td><td>**1.19.10†**</td></tr><tr><td>v1.3.0</td><td>1.24, 1.23, 1.22, 1.21, 1.20</td><td>3.16.0</td><td>1.19.10†</td></tr></tbody></table>

**前置条件依赖**
----------

### **[安装MetalLB](http://www.dev-share.top/2020/08/14/%e4%bd%bf%e7%94%a8metallb%e6%9d%a5%e8%a7%a3%e5%86%b3k8s-service-loadbalancer%e9%97%ae%e9%a2%98/ "安装MetalLB")**

**安装**
------

### **使用 Helm 3 安装 `Nginx Ingress Controller`**

**`注意`：Ingress Controller它也是个应用程序，也有 service、deployment、pod 进行工作**

```shell
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update


## 查看确认
[root@k8s-master k8s]# helm search repo ingress-nginx -l | grep -E "1.5.1|1.4.0|1.3.1"

ingress-nginx/ingress-nginx     4.4.2           1.5.1           Ingress controller for Kubernetes using NGINX a...
ingress-nginx/ingress-nginx     4.4.0           1.5.1           Ingress controller for Kubernetes using NGINX a...
ingress-nginx/ingress-nginx     4.3.0           1.4.0           Ingress controller for Kubernetes using NGINX a...
ingress-nginx/ingress-nginx     4.2.5           1.3.1           Ingress controller for Kubernetes using NGINX a...
ingress-nginx/ingress-nginx     4.2.4           1.3.1           Ingress controller for Kubernetes using NGINX a...




## 添加环境变量统一管理ingress-nginx 版本与工作命令空间；当前K8s集群版本为 v1.20.6
export NGINX_CHART_VERSION=4.2.5
helm pull ingress-nginx/ingress-nginx --version <span class="katex math inline">NGINX_CHART_VERSION


## 为 NGINX Ingress Controller 创建命名空间
export NGINX_ING_NAMESPACE=ingress-nginx-ns

# 在</span>NGINX_ING_NAMESPACE 命名空间下创建， Ingress Controller是可以独立部署在自己的命名空间中

-----------------------------------------------------------------------------------

## 如果希望动态更改Ingress控制器副本的数量，请使用 Deployment。
## --set controller.kind=deployment
## 如果希望在所有节点上部署Ingress控制器，  请使用 DaemonSet。
## --set controller.kind=daemonset

##  是Pod的副本数
## --set controller.replicaCount

## Service 类型： NodePort            例如  443:30443    可以 通过宿主机 443 端口访问， 还可以通过 30443 端口进行访问
## Service 类型： LoadBalancer        例如  443:30443    只能 通过宿主机 443 端口访问， 并且30xxx端口是随机生成的

## LoadBalancer 类型的 Service，可以自动调用云服务商在 IaaS 层面的接口(宿主机的接口)，并自动创建 LoadBalancer，将其指向该 Service
## 通俗的讲， 需要有外接的硬件设备，在通过设备访问80|443端口实现负载均衡访问；  或者使用 MetalLB实现软的负载均衡
## 安装MetalLB来解决K8S service LoadBalancer问题
##   http://www.dev-share.top/2020/08/14/%e4%bd%bf%e7%94%a8metallb%e6%9d%a5%e8%a7%a3%e5%86%b3k8s-service-loadbalancer%e9%97%ae%e9%a2%98/
## --set controller.service.type=LoadBalancer


```

**创建 values.yaml**

```yaml
## Default 404 backend
## 默认不启动
defaultBackend:
  ## 默认不启动
  #enabled: false
  enabled: true
  name: defaultbackend
  image:
    #registry: registry.k8s.io
    #image: defaultbackend-amd64
    registry: cnagent
    image: defaultbackend-amd64
    tag: "1.5"
    pullPolicy: IfNotPresent
    # nobody user -> uid 65534
    runAsUser: 65534
    runAsNonRoot: true
    readOnlyRootFilesystem: true
    allowPrivilegeEscalation: false


controller:
  name: controller
  # -- Use a `DaemonSet` or `Deployment`
  kind: DaemonSet
  replicaCount: 1

  image:
    #registry: registry.k8s.io
    #image: ingress-nginx/controller
    registry: cnagent
    image: ingress-nginx-controller
    tag: "v1.3.1"
    # 必须要用，否则拉取镜像会失败
    digest: sha256:d3642f55a6a7a102a9a579b3382fe73869c73890de4c94f28e36ba5e07925944
    pullPolicy: IfNotPresent

  # -- Configures the controller container name
  containerName: controller
  # -- Configures the ports that the nginx-controller listens on
  containerPort:
    http: 80
    https: 443

  service:
    enabled: true
    type: LoadBalancer

    ## type: NodePort
    ## nodePorts:
    ##   http: 32080
    ##   https: 32443
    ##   tcp:
    ##     8080: 32808
    nodePorts:
      http: ""
      https: ""
      tcp: {}
      udp: {}


    enableHttp: true
    enableHttps: true
    ports:
      http: 80
      https: 443

    targetPorts:
      http: http
      https: https

  ## web钩子
  admissionWebhooks:
    patch:
      enabled: true
      image:
        #registry: registry.k8s.io
        #image: ingress-nginx/kube-webhook-certgen
        registry: cnagent
        image: ingress-nginx-kube-webhook-certgen
        tag: v1.3.0
        digest: sha256:fe821886866f174069dbb1e3af741662efb44952e39d66488d1fb811673440b7
        pullPolicy: IfNotPresent



# -- TCP service key-value pairs
## Ref: https://github.com/kubernetes/ingress-nginx/blob/main/docs/user-guide/exposing-tcp-udp-services.md
## 开启TCP代理功能
tcp: {}
#tcp:
#  8080: "default/example-tcp-svc:9000"
#tcp:
#  9094: "kafka-ns/kafka-3-2-3-0-external:9094"
#  9095: "kafka-ns/kafka-3-2-3-1-external:9094"
#  9096: "kafka-ns/kafka-3-2-3-2-external:9094"

# -- UDP service key-value pairs
## Ref: https://github.com/kubernetes/ingress-nginx/blob/main/docs/user-guide/exposing-tcp-udp-services.md
## 开启UDP代理功能
udp: {}
#udp:
#  53: "kube-system/kube-dns:53"


```

**部署/卸载**

```shell
## 启动
helm install gateway ./ingress-nginx-<span class="katex math inline">NGINX_CHART_VERSION.tgz -f values.yaml -n</span>NGINX_ING_NAMESPACE --create-namespace

## 更新（要强制更新）
helm upgrade gateway ./ingress-nginx-<span class="katex math inline">NGINX_CHART_VERSION.tgz -f values.yaml -n</span>NGINX_ING_NAMESPACE --force

# 卸载
helm uninstall gateway -n $NGINX_ING_NAMESPACE


```

**查看 运行情况**

```ruby
[root@k8s-master k8s]# kubectl -n $NGINX_ING_NAMESPACE get all


NAME                                                      READY   STATUS    RESTARTS   AGE
pod/gateway-ingress-nginx-controller-2b8l5                1/1     Running   0          102s
pod/gateway-ingress-nginx-controller-2s8ww                1/1     Running   0          102s
pod/gateway-ingress-nginx-controller-mzb45                1/1     Running   0          102s
pod/gateway-ingress-nginx-controller-q4d9z                1/1     Running   0          102s
pod/gateway-ingress-nginx-controller-z67gq                1/1     Running   0          102s
pod/gateway-ingress-nginx-defaultbackend-bf75d4b5-ktttz   1/1     Running   0          102s


NAME                                                 TYPE           CLUSTER-IP      EXTERNAL-IP       PORT(S)                                                                   AGE
service/gateway-ingress-nginx-controller             LoadBalancer   10.96.179.94    192.168.101.100   80:30368/TCP,443:30275/TCP,9094:31895/TCP,9095:31808/TCP,9096:32339/TCP   102s
service/gateway-ingress-nginx-controller-admission   ClusterIP      10.96.135.75    <none>            443/TCP                                                                   102s
service/gateway-ingress-nginx-defaultbackend         ClusterIP      10.96.150.240   <none>            80/TCP                                                                    102s


NAME                                              DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
daemonset.apps/gateway-ingress-nginx-controller   5         5         5       5            5           kubernetes.io/os=linux   102s


NAME                                                   READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/gateway-ingress-nginx-defaultbackend   1/1     1            1           102s


NAME                                                            DESIRED   CURRENT   READY   AGE
replicaset.apps/gateway-ingress-nginx-defaultbackend-bf75d4b5   1         1         1       102s


</none></none>
```

**测试链接**

```shell
## 返回 html，表示链接成功，因为没有程序，所以返回 404
## 请求的IP地址， 必须是 pod/gateway-ingress-nginx Pod所在的节点的地址
[root@k8s-master ~]# curl 192.168.101.100
## 因为开启了 defaultBackend 所以会返回这样的信息
default backend - 404


```

**<div style="overflow:hidden; clear:both; width: 100%; height: 40px; position: relative;">- - - - - -

 <span style="position: absolute;top: 50%;left: 50%; transform: translate(-50%, -50%); background-color: white;">以下为隐藏内容</span> </div>**

### **[将 https 证书， 添加到k8s中](http://www.dev-share.top/2020/07/19/%e4%bd%bf%e7%94%a8-openssl-%e7%ad%be%e5%8f%91-https-%e5%9f%9f%e5%90%8d%e8%af%81%e4%b9%a6%ef%bc%8c-%e5%b9%b6%e6%b7%bb%e5%8a%a0%e5%88%b0k8s%e4%b8%ad/ "将 https 证书， 添加到k8s中")**

**给域名`nginx.dev-share.top`生成自签证书**

**`注意`：证书的`命名空间`，一定要和`发布的程序`的`Deployment、Service`处于同一个名称空间**

```ruby
# 为 要发布的程序 创建命名空间
export APP_NS=app-test-nginx-ns
kubectl create namespace <span class="katex math inline">APP_NS

openssl genrsa -out tls.key 2048
openssl req -new -x509 -key tls.key  -out tls.crt -subj /C=CN/ST=Beijing/O=DevOps/CN=nginx.dev-share.top

# 创建 secret tls   通过 secret 把证书注入到 pod中
kubectl -n</span>APP_NS create secret tls tls-ingress \
  --cert=tls.crt \
  --key=tls.key


```

- - - - - -

- - - - - -

- - - - - -

### **创建 Ingress**

**创建 Ingress， 配置 `域名` 与 k8s集群中 `Service` 的映射规则**

**`注意`：Ingress的`命名空间`，一定要和`发布的程序`的`Deployment、Service`处于同一个名称空间**

```ruby
cat > app-test-ingress.yaml 
```

- - - - - -

- - - - - -

- - - - - -

### **创建测试程序**

#### **[创建测试程序镜像](http://www.dev-share.top/2019/12/12/k8s-%e4%bd%bf%e7%94%a8centos-7-%e9%95%9c%e5%83%8f%ef%bc%8c%e6%9e%84%e5%bb%bak8s%e7%bd%91%e7%bb%9c%e6%b5%8b%e8%af%95%e5%ae%b9%e5%99%a8/ "创建测试程序镜像")**

#### **app-test-nginx-svc.yaml 文件**

```ruby
cat > app-test-nginx-svc.yaml 
```

- - - - - -

#### **app-test-nginx-deploy.yaml 文件**

```ruby
cat > app-test-nginx-deploy.yaml 
```

```ruby
## 启动
[root@k8s-master tls]# kubectl apply -f app-test-ingress.yaml -f app-test-nginx-svc.yaml -f app-test-nginx-deploy.yaml


```

- - - - - -

#### **查看集群 状态**

```ruby
[root@k8s-master k8s]# kubectl get -f app-test-ingress.yaml -f app-test-nginx-svc.yaml -f app-test-nginx-deploy.yaml


## Ingress 信息
NAME                                         CLASS    HOSTS                 ADDRESS   PORTS     AGE
ingress.networking.k8s.io/app-test-ingress   <none>   nginx.dev-share.top             80, 443   28s

## Service 信息
NAME                         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
service/app-test-nginx-svc   ClusterIP   10.96.235.66   <none>        80/TCP    28s

## Deployment 信息
NAME                             READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/app-test-nginx   1/1     1            0           28s





[root@k8s-master k8s]# kubectl -n $APP_NS describe ing
Name:             app-test-ingress
Namespace:        app-test-nginx-ns
Address:          192.168.101.100
Default backend:  default-http-backend:80 (<error: endpoints="" found="" not="">)
TLS:
  tls-ingress terminates nginx.dev-share.top
Rules:
  Host                 Path  Backends
  ----                 ----  --------
  nginx.dev-share.top
                       /   app-test-nginx-svc:80 (10.100.116.99:80)
Annotations:           ingress.kubernetes.io/ssl-redirect: false
                       kubernetes.io/ingress.class: nginx
                       nginx.ingress.kubernetes.io/Access-Control-Allow-Origin: *
                       nginx.ingress.kubernetes.io/cors-allow-headers:
                         DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization
                       nginx.ingress.kubernetes.io/cors-allow-methods: PUT, GET, POST, OPTIONS
                       nginx.ingress.kubernetes.io/cors-allow-origin: *
                       nginx.ingress.kubernetes.io/enable-cors: true
                       nginx.ingress.kubernetes.io/proxy-body-size: 50m
                       nginx.ingress.kubernetes.io/service-weight:
Events:
  Type    Reason  Age                From                      Message
  ----    ------  ----               ----                      -------
  Normal  Sync    17s (x2 over 25s)  nginx-ingress-controller  Scheduled for sync
  Normal  Sync    17s (x2 over 25s)  nginx-ingress-controller  Scheduled for sync
  Normal  Sync    17s (x2 over 25s)  nginx-ingress-controller  Scheduled for sync
  Normal  Sync    17s (x2 over 25s)  nginx-ingress-controller  Scheduled for sync
  Normal  Sync    1s (x2 over 9s)    nginx-ingress-controller  Scheduled for sync


</error:></none></none>
```

- - - - - -

- - - - - -

- - - - - -

#### **测试 http 请求**

```ruby
# 因为 Ingress 中配置的是域名， 所以不能使用IP地址直接访问
[root@k8s-master ~]# curl -svk -H "Host: nginx.dev-share.top" http://192.168.101.100 | grep -E "title"

* About to connect() to 192.168.101.100 port 80 (#0)
*   Trying 192.168.101.100...
* Connected to 192.168.101.100 (192.168.101.100) port 80 (#0)
> GET / HTTP/1.1
> User-Agent: curl/7.29.0
> Accept: */*
> Host: nginx.dev-share.top
>
<title>308 Permanent Redirect</title>



```

- - - - - -

#### **测试 https 请求**

```ruby
# 因为 Ingress 中配置的是域名， 所以不能使用IP地址直接访问
[root@k8s-master ~]# curl -svk -H "Host: nginx.dev-share.top" https://192.168.101.100 | grep -E "title"

* About to connect() to 192.168.101.100 port 443 (#0)
*   Trying 192.168.101.100...
* Connected to 192.168.101.100 (192.168.101.100) port 443 (#0)
* Initializing NSS with certpath: sql:/etc/pki/nssdb
* skipping SSL peer certificate verification
* SSL connection using TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
* Server certificate:
*       subject: CN=Kubernetes Ingress Controller Fake Certificate,O=Acme Co
*       start date: Feb 11 07:27:30 2023 GMT
*       expire date: Feb 11 07:27:30 2024 GMT
*       common name: Kubernetes Ingress Controller Fake Certificate
*       issuer: CN=Kubernetes Ingress Controller Fake Certificate,O=Acme Co
> GET / HTTP/1.1
> User-Agent: curl/7.29.0
> Accept: */*
> Host: nginx.dev-share.top
>
Welcome to nginx!



```

- - - - - -

- - - - - -

- - - - - -

**总结**
------

1. **`Ingress Controller` 开启 `NodePort` 提供 K8S 集群的外网访问入口**
2. **使用 `Ingress` 将集群中的 `Service` 与 `域名` 绑定在一起**
3. **`Ingress Controller` 会搜集所有 `Ingress` 中配置的 `域名`**
4. **最后通过 `Ingress Controller`的端口 加上 `Ingress`的域名 进行访问**

- - - - - -

- - - - - -

- - - - - -