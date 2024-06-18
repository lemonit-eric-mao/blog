---
title: "Istio系列四 路由管理"
date: "2020-08-06"
categories: 
  - "istio"
---

###### 测试 使用 Istio 自动注入 自己的应用程序 **[自动/手动注入Sidecar](https://istio.io/latest/zh/docs/setup/additional-setup/sidecar-injection/ "自动/手动注入Sidecar")**

  当使用 **kubectl apply** 来部署应用时，如果 **pod** 启动在标有 `istio-injection=enabled` 的命名空间中，那么，**Istio sidecar** 注入器将自动注入 **Envoy** 容器到应用的 **pod** 中：

```ruby
$ kubectl label namespace <namespace> istio-injection=enabled
$ kubectl create -n <namespace> -f <your-app-spec>.yaml
```

  在没有 **istio-injection** 标记的命名空间中，在部署前可以使用 `istioctl kube-inject` 命令将 **Envoy** 容器手动注入到应用的 **pod** 中：

```ruby
$ istioctl kube-inject -f <your-app-spec>.yaml | kubectl apply -f -
```

* * *

* * *

* * *

##### **前置条件**

###### **[部署SpringBoot应用程序到K8S](http://www.dev-share.top/2020/09/09/istio%e7%b3%bb%e5%88%97%e4%ba%8c-%e8%87%aa%e5%8a%a8%e5%8c%96%e9%83%a8%e7%bd%b2springboot%e5%ba%94%e7%94%a8%e7%a8%8b%e5%ba%8f%e5%88%b0k8s/ "部署SpringBoot应用程序到K8S")**

###### **[Istio 安装部署](http://www.dev-share.top/2020/08/03/istio%e7%b3%bb%e5%88%97%e4%b8%89-%e5%ae%89%e8%a3%85%e9%83%a8%e7%bd%b2/ "Istio 安装部署")**

* * *

###### 查看 istio 网关

```ruby
[root@master01 ~]# kubectl get svc -n istio-system -o wide
NAME                   TYPE           CLUSTER-IP      EXTERNAL-IP      PORT(S)                                                      AGE   SELECTOR
istio-ingressgateway   LoadBalancer   10.222.73.189   192.168.20.106   15021:31797/TCP,80:32578/TCP,443:31676/TCP,15443:31801/TCP    16h   app=istio-ingressgateway,istio=ingressgateway
istiod                 ClusterIP      10.222.18.230   <none>           15010/TCP,15012/TCP,443/TCP,15014/TCP,853/TCP                  16h   app=istiod,istio=pilot
[root@master01 ~]#

[root@master01 ~]# kubectl get pods -n istio-system -o wide
NAME                                    READY   STATUS    RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES
istio-ingressgateway-746548c687-fwpkl   1/1     Running   0          16h   10.244.3.29   worker03   <none>           <none>
istiod-6c5f6f55ff-cfrd7                 1/1     Running   0          16h   10.244.1.28   worker01   <none>           <none>
[root@master01 ~]#

```

* * *

###### 查看现有的 SpringBoot应用程序

```ruby
[root@master01 ~]# kubectl -n spring-boot get all -o wide
NAME                                                        READY   STATUS    RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES
pod/deployment-005-organization-service-6985967cb4-f4wsr    1/1     Running   0          14m   10.244.3.31   worker03   <none>           <none>
pod/deployment-006-orgservice-new-7d69f67c8f-mmqm9          1/1     Running   0          13m   10.244.3.32   worker03   <none>           <none>
pod/deployment-007-specialroutes-service-5468f556d8-z5759   1/1     Running   0          13m   10.244.2.24   worker02   <none>           <none>

NAME                                        TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE   SELECTOR
service/service-005-organization-service    ClusterIP   10.222.112.77    <none>        80/TCP    16h   app=pod-005-organization-service
service/service-006-orgservice-new          ClusterIP   10.222.133.201   <none>        80/TCP    16h   app=pod-006-orgservice-new
service/service-007-specialroutes-service   ClusterIP   10.222.168.192   <none>        80/TCP    16h   app=pod-007-specialroutes-service

NAME                                                   READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS                  IMAGES                                                     SELECTOR
deployment.apps/deployment-005-organization-service    1/1     1            1           20m   005-organization-service    192.168.20.93/library/005-organization-service:20200909    app=pod-005-organization-service,version=v1
deployment.apps/deployment-006-orgservice-new          1/1     1            1           19m   006-orgservice-new          192.168.20.93/library/006-orgservice-new:20200909          app=pod-006-orgservice-new
deployment.apps/deployment-007-specialroutes-service   1/1     1            1           19m   007-specialroutes-service   192.168.20.93/library/007-specialroutes-service:20200909   app=pod-007-specialroutes-service

NAME                                                              DESIRED   CURRENT   READY   AGE   CONTAINERS                  IMAGES                                                     SELECTOR
replicaset.apps/deployment-005-organization-service-6985967cb4    1         1         1       20m   005-organization-service    192.168.20.93/library/005-organization-service:20200909    app=pod-005-organization-service,pod-template-hash=6985967cb4,version=v1
replicaset.apps/deployment-006-orgservice-new-7d69f67c8f          1         1         1       19m   006-orgservice-new          192.168.20.93/library/006-orgservice-new:20200909          app=pod-006-orgservice-new,pod-template-hash=7d69f67c8f
replicaset.apps/deployment-007-specialroutes-service-5468f556d8   1         1         1       19m   007-specialroutes-service   192.168.20.93/library/007-specialroutes-service:20200909   app=pod-007-specialroutes-service,pod-template-hash=5468f556d8
[root@master01 ~]#
```

* * *

##### 将 Spring Boot 应用程序交给 Istio来管理

###### 告诉K8S SpringBoot应用程序所在的命名空间下，所有的应用程序都允许Istio自动注入

```ruby
kubectl label namespace spring-boot istio-injection=enabled
```

* * *

###### 重启Pod会发现 `READY 1/1` --> `READY 2/2`

```ruby
[root@master01 ~]# kubectl -n spring-boot get pod -o wide
NAME                                                    READY   STATUS    RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES
deployment-005-organization-service-6985967cb4-f4wsr    2/2     Running   0          16m   10.244.3.31   worker03   <none>           <none>
deployment-006-orgservice-new-7d69f67c8f-mmqm9          2/2     Running   0          15m   10.244.3.32   worker03   <none>           <none>
deployment-007-specialroutes-service-5468f556d8-z5759   2/2     Running   0          15m   10.244.2.24   worker02   <none>           <none>
[root@master01 ~]#
```

###### 查看Pod日志

`kubectl logs PODNAME -c 容器中的程序名 -n NAMESPACE`

```ruby
# 查看容器日志
kubectl logs -f deployment-007-specialroutes-service-5468f556d8-z5759 -c 007-specialroutes-service -n spring-boot

# 查看istio代理日志
kubectl logs -f deployment-007-specialroutes-service-5468f556d8-z5759 -c istio-proxy -n spring-boot
```

* * *

###### 创建SpringBoot应用程序，基于Istio的网关

**`每个命名空间下创建一个就可以`**

```yaml
cat > springboot-gateway.yaml  << ERIC

# 接入 Istio网关
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  namespace: spring-boot
  name: springboot-gateway
spec:
  selector:
    # 寻找 label 为 istio=ingressgateway 的 service, 没错它是个 Service 并不是真正的 Ingress
    # 使用 istion 默认网关
    istio: ingressgateway
  servers:
    - port:
        number: 80
        name: http
        protocol: HTTP
      hosts:
        - "*"


ERIC

kubectl apply -f springboot-gateway.yaml

```

* * *

###### 创建SpringBoot应用程序，基于Istio的路由

**`虚服务，一个项目创建一个`**

```yaml
cat > springboot-virtualservice.yaml  << ERIC

---
# 为通过 Istio网关 的入口流量配置路由
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  namespace: spring-boot
  name: virtualservice-005-organization-service
spec:
  hosts:
    - "*"
  gateways:
    - springboot-gateway
  http:
    # 允许流量流向路径 /organizations 和 /getall, 通过 springboot-gateway 网关。
    # 所有其他外部请求均被拒绝并返回 404 响应。
    - match:
        - uri:
            prefix: /organizations
        - uri:
            prefix: /getall
      route:
        # 将被允许的请求，转发到 service-005-organization-service的 80端口上
        - destination:
            # 告诉Istio 你的请求转发到哪个Service上
            host: service-005-organization-service
            # 并且告诉Istio， Service的端口
            port:
              number: 80


---
# 为通过 Istio网关 的入口流量配置路由
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  namespace: spring-boot
  name: virtualservice-007-specialroutes-service
spec:
  hosts:
    - "*"
  gateways:
    - springboot-gateway
  http:
    # 允许前缀为 /route 的流量流向路径, 通过 springboot-gateway 网关。
    # 所有其他外部请求均被拒绝并返回 404 响应。
    - match:
        - uri:
            # 通常设置为 @RequestMapping(value = "/route") 路径， 否则代理到SpringBoot应用程序时, 同样引发应用程序404
            prefix: /route
      route:
        # 将被允许的请求，转发到 service-007-specialroutes-service的 80端口上
        - destination:
            # 告诉Istio 你的请求转发到哪个Service上
            host: service-007-specialroutes-service
            # 并且告诉Istio， Service的端口
            port:
              number: 80

ERIC

kubectl apply -f springboot-virtualservice.yaml

```

* * *

###### `007-specialroutes-service` SpringBoot的应用程序Controller代码

```java
package com.app.cloud.specialroutes.controllers;


import com.app.cloud.specialroutes.model.AbTestingRoute;
import com.app.cloud.specialroutes.services.AbTestingRouteService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping(value = "/route")
public class SpecialRoutesServiceController {

    @Autowired
    AbTestingRouteService routeService;

    @GetMapping(value = "/result/{routeId}")
    public String result(@PathVariable("routeId") String routeId) {
        return "SUCCESS 007-specialroutes-service " + routeId;
    }

    @GetMapping("/getall/{routeId}/{age}")
    public String getAll(@PathVariable("routeId") String routeId, @PathVariable("age") String age) {
        return "SUCCESS 007-specialroutes-service " + routeId + " age: " + age;
    }

}
```

* * *

###### 测试请求

**curl** http://**`istio-ingressgateway`的`EXTERNAL-IP`/**被允许的流量流向路径**/**请求参数

```ruby
[root@master01 ~]# curl http://192.168.20.106/route/result/666
SUCCESS 007-specialroutes-service 666
[root@master01 ~]#

[root@master01 ~]# curl http://192.168.20.106/route/getall/111/333
SUCCESS 007-specialroutes-service 111 age: 333
[root@master01 ~]#

```

* * *

* * *

* * *

* * *

* * *

* * *

###### **[部署 Node.js 程序到 K8S](http://www.dev-share.top/2019/07/10/gitlab-ci-%e6%8c%81%e7%bb%ad%e9%9b%86%e6%88%90-%e7%94%9f%e4%ba%a7%e6%a1%88%e4%be%8b/ "部署 Node.js 程序到 K8S")**

##### 将 node.js 应用程序交给 Istio来管理

* * *

###### 查看现有的 node.js 应用程序

```ruby
[root@k8s-master node-web]# kubectl -n node-web-ns get svc
NAME       TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)    AGE
node-web   ClusterIP   10.96.64.68   <none>        8066/TCP   23h
[root@k8s-master node-web]#
```

* * *

###### 1\. 添加 node.js 应用程序 允许注入

```ruby
kubectl label namespace node-web-ns istio-injection=enabled

```

* * *

###### 2\. 创建 NodeWeb 网关 node-web-gateway.yaml

**每个命名空间下创建一个就可以**

```ruby
cat > node-web-gateway.yaml  << ERIC

apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  namespace: node-web-ns
  name: node-web-gateway
spec:
  selector:
    # 寻找 label 为 istio=ingressgateway 的 service, 没错它是个 Service 并不是真正的 Ingress
    # 使用 istion 默认网关
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "*"

---

apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  namespace: node-web-ns
  name: node-web
spec:
  hosts:
  - "*"
  gateways:
  - node-web-gateway
  http:
  - match:
    - uri:
        # 告诉 Istio 这个虚服务，要访问你的 node.js 应该程序的 url 路径是什么; 例如首页的路径
        prefix: /
    route:
    - destination:
        # 告诉 Istio 你的 node.js 应该程序的Service端口是什么
        port:
          number: 8066
        # 告诉 Istio 你的 node.js 应该程序的Service名叫什么
        host: node-web

ERIC

kubectl apply -f node-web-gateway.yaml

```

**浏览器访问：`http://192.168.20.92:30134`**

* * *

* * *

* * *

##### 总结

```ruby
                                [  互联网  ]
                                   --|--
                                     V
                         [ Istio Ingress Getaway ]  # 是个 Service
                          --|-----------------|--
                            V                 V
        [ Java的 Istio Gateway ]          [ NodeJs的 Istio Gateway ]
                 --|-----------------------------------|--
                   V                                   V
    [ Java的 Istio VirtualService ]     [ NodeJs的 Istio VirtualService ]
                 --|-----------------------------------|--
                   V                                   V
           [ Java的 Services ]               [ NodeJs的 Services ]
```

* * *

* * *

* * *
