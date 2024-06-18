---
title: "使用 Helm 3 安装 Kong Ingress Controller"
date: "2022-08-09"
categories: 
  - "kong"
  - "k8s"
---

##### 前提条件

###### **[详解 Ingress](http://www.dev-share.top/2019/03/15/k8s-%e9%85%8d%e7%bd%ae-ingress%e5%ae%9a%e4%b9%89%e7%9a%84%e8%b7%af%e7%94%b1%e8%a7%84%e5%88%99%e9%9b%86/ "详解 Ingress")**

###### **[安装 Helm](http://www.dev-share.top/2020/07/16/helm-%e5%ae%89%e8%a3%85-%e4%bd%bf%e7%94%a8/ "安装 Helm")**

###### **[官方安装 Kong Ingress Controller](https://github.com/Kong/kubernetes-ingress-controller#get-started "官方安装 Kong Ingress Controller")**

* * *

* * *

* * *

###### 添加Chart源

```ruby
helm repo add kong https://charts.konghq.com
helm repo update

## 查看
[root@k8s-master ~]# helm search repo kong
NAME            CHART VERSION   APP VERSION     DESCRIPTION
bitnami/kong    6.3.31          2.8.1           Kong is an open source Microservice API gateway...
kong/kong       2.11.0          2.8             The Cloud-Native Ingress and API-management
stable/kong     0.36.7          1.4             DEPRECATED The Cloud-Native Ingress and API-man...
[root@k8s-master ~]#
```

* * *

##### **使用 Helm 3 安装 `Kong Ingress Controller`**

```ruby
export KONG_CHART_VERSION=2.11.0
## 将Chart包下载到本地
helm pull kong/kong --version $KONG_CHART_VERSION

## 为 Kong Ingress Controller 创建命名空间
export KONG_ING_NAMESPACE=kong-ingress-ns

## 安装部署
helm install kong-ingress-controller ./kong-$KONG_CHART_VERSION.tgz \
  -n $KONG_ING_NAMESPACE \
  --create-namespace \
  --set ingressController.installCRDs=false


## 卸载
helm uninstall kong-ingress-controller -n $KONG_ING_NAMESPACE

```

* * *

###### 查看 运行情况

```ruby
[root@k8s-master ~]# kubectl -n $KONG_ING_NAMESPACE get all -o wide


NAME                                                READY   STATUS    RESTARTS   AGE   IP              NODE            NOMINATED NODE   READINESS GATES
pod/kong-ingress-controller-kong-6fdc89846d-qp4nx   2/2     Running   0          45s   10.100.78.201   k8s-worker-04   <none>           <none>


NAME                                         TYPE           CLUSTER-IP      EXTERNAL-IP      PORT(S)                      AGE   SELECTOR
service/kong-ingress-controller-kong-proxy   LoadBalancer   10.96.106.189   192.168.101.30   80:32085/TCP,443:31299/TCP   45s   app.kubernetes.io/component=app,app.kubernetes.io/instance=kong-ingress-controller,app.kubernetes.io/name=kong


NAME                                           READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS                 IMAGES                                            SELECTOR
deployment.apps/kong-ingress-controller-kong   1/1     1            1           45s   ingress-controller,proxy   kong/kubernetes-ingress-controller:2.5,kong:2.8   app.kubernetes.io/component=app,app.kubernetes.io/instance=kong-ingress-controller,app.kubernetes.io/name=kong


NAME                                                      DESIRED   CURRENT   READY   AGE   CONTAINERS                 IMAGES                                            SELECTOR
replicaset.apps/kong-ingress-controller-kong-6fdc89846d   1         1         1       45s   ingress-controller,proxy   kong/kubernetes-ingress-controller:2.5,kong:2.8   app.kubernetes.io/component=app,app.kubernetes.io/instance=kong-ingress-controller,app.kubernetes.io/name=kong,pod-template-hash=6fdc89846d





## 查看 输出如下信息表示安装成功
[root@k8s-master ~]# curl 192.168.101.30
{"message":"no Route matched with those values"}

```

* * *

* * *

* * *

###### **将 https 证书， 添加到k8s中**

```ruby
# 为 要发布的程序 创建命名空间
export APP_TEST_KONG_NS=app-test-kong-ns
kubectl create namespace $APP_TEST_KONG_NS

openssl genrsa -out tls.key 2048
openssl req -new -x509 -key tls.key  -out tls.crt -subj /C=CN/ST=Beijing/O=DevOps/CN=kong.dev-share.top

# 创建 secret tls   通过 secret 把证书注入到 pod中
kubectl -n $APP_TEST_KONG_NS create secret tls tls-ingress \
  --cert=tls.crt \
  --key=tls.key

```

* * *

* * *

* * *

###### **创建 Ingress**

```ruby
cat > app-test-kong-ingress.yaml << ERIC

---

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  namespace: $APP_TEST_KONG_NS
  # Ingress 名称
  name: app-test-kong-ingress
  annotations:
    # 告诉k8s要用到的ingress-controller是kong, 而不是Traefik、Envoy、Nginx
    kubernetes.io/ingress.class: "kong"
    # 如果希望http的强制转到https，把ingress.kubernetes.io/ssl-redirect设为true
    ingress.kubernetes.io/ssl-redirect: "false"

spec:

  rules:
  - host: "kong.dev-share.top"
    http:
      paths:
      - path: "/"
        pathType: Prefix
        backend:
          service:
            name: app-test-kong-svc
            port:
              number: 80


  tls:
  - hosts:
    - kong.dev-share.top
    secretName: tls-ingress
---

ERIC

```

* * *

* * *

* * *

##### 创建测试程序

app-test-kong-svc.yaml 文件

```ruby
cat > app-test-kong-svc.yaml << ERIC

---
kind: Service
apiVersion: v1
metadata:
  namespace: $APP_TEST_KONG_NS
  name: app-test-kong-svc
  labels:
    name: app-test-kong-svc-label
spec:
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 80
  selector:
    app: app-test-kong-pod-label

---

ERIC

```

* * *

app-test-kong-deploy.yaml 文件

```ruby
cat > app-test-kong-deploy.yaml << ERIC

---

kind: Deployment
apiVersion: apps/v1
metadata:
  namespace: $APP_TEST_KONG_NS
  name: app-test-kong

spec:
  replicas: 1
  minReadySeconds: 30
  selector:
    matchLabels:
      app: app-test-kong-pod-label

  template:
    metadata:
      labels:
        app: app-test-kong-pod-label
    spec:
      terminationGracePeriodSeconds: 30
      containers:
        - name: $APP_TEST_KONG_NS
          image: nginx:1.21.0
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 80

---

ERIC

```

```ruby
## 启动
kubectl apply -f app-test-kong-ingress.yaml -f app-test-kong-svc.yaml -f app-test-kong-deploy.yaml

```

* * *

###### 查看集群状态

```ruby
[root@k8s-master ~]# kubectl get -f app-test-kong-ingress.yaml -f app-test-kong-svc.yaml -f app-test-kong-deploy.yaml

## Ingress 信息
NAME                                              CLASS    HOSTS                ADDRESS          PORTS     AGE
ingress.networking.k8s.io/app-test-kong-ingress   <none>   kong.dev-share.top   192.168.101.30   80, 443   13s

## Service 信息
NAME                        TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
service/app-test-kong-svc   ClusterIP   10.96.57.145   <none>        80/TCP    13s

## Deployment 信息
NAME                            READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/app-test-kong   1/1     1            0           13s




[root@k8s-master ~]# kubectl -n $APP_TEST_KONG_NS describe ing
Name:             app-test-kong-ingress
Namespace:        app-test-kong-ns
Address:          192.168.101.30
Default backend:  default-http-backend:80 (<error: endpoints "default-http-backend" not found>)
TLS:
  tls-ingress terminates kong.dev-share.top
Rules:
  Host                Path  Backends
  ---- ---- --------
  kong.dev-share.top
                      /   app-test-kong-svc:80 (10.100.78.205:80)
Annotations:          ingress.kubernetes.io/ssl-redirect: false
                      kubernetes.io/ingress.class: kong
Events:               <none>

```

* * *

* * *

* * *

##### 测试 http 请求

```ruby
[root@k8s-master ~]# curl -svk -H "Host: kong.dev-share.top" http://192.168.101.30 | grep -E "title"

* About to connect() to 192.168.101.30 port 80 (#0)
*   Trying 192.168.101.30...
* Connected to 192.168.101.30 (192.168.101.30) port 80 (#0)
> GET / HTTP/1.1
> User-Agent: curl/7.29.0
> Accept: */*
> Host: kong.dev-share.top
>
< HTTP/1.1 200 OK
< Content-Type: text/html; charset=UTF-8
< Content-Length: 612
< Connection: keep-alive
< Server: nginx/1.21.0
< Date: Wed, 10 Aug 2022 06:15:50 GMT
< Last-Modified: Tue, 25 May 2021 12:28:56 GMT
< ETag: "60aced88-264"
< Accept-Ranges: bytes
< X-Kong-Upstream-Latency: 1
< X-Kong-Proxy-Latency: 0
< Via: kong/2.8.1
<
{ [data not shown]
* Connection #0 to host 192.168.101.30 left intact
<title>Welcome to nginx!</title>

```

* * *

##### 测试 https 请求

```ruby
[root@k8s-master ~]# curl -svk -H "Host: kong.dev-share.top" https://192.168.101.30 | grep -E "title"

* About to connect() to 192.168.101.30 port 443 (#0)
*   Trying 192.168.101.30...
* Connected to 192.168.101.30 (192.168.101.30) port 443 (#0)
* Initializing NSS with certpath: sql:/etc/pki/nssdb
* skipping SSL peer certificate verification
* SSL connection using TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384
* Server certificate:
*       subject: CN=localhost,OU=IT Department,O=Kong,L=San Francisco,ST=California,C=US
*       start date: Aug 10 06:07:12 2022 GMT
*       expire date: Jan 19 03:14:08 2038 GMT
*       common name: localhost
*       issuer: CN=localhost,OU=IT Department,O=Kong,L=San Francisco,ST=California,C=US
> GET / HTTP/1.1
> User-Agent: curl/7.29.0
> Accept: */*
> Host: kong.dev-share.top
>
< HTTP/1.1 200 OK
< Content-Type: text/html; charset=UTF-8
< Content-Length: 612
< Connection: keep-alive
< Server: nginx/1.21.0
< Date: Wed, 10 Aug 2022 06:16:15 GMT
< Last-Modified: Tue, 25 May 2021 12:28:56 GMT
< ETag: "60aced88-264"
< Accept-Ranges: bytes
< X-Kong-Upstream-Latency: 0
< X-Kong-Proxy-Latency: 1
< Via: kong/2.8.1
<
{ [data not shown]
* Connection #0 to host 192.168.101.30 left intact
<title>Welcome to nginx!</title>

```

* * *

* * *

* * *
