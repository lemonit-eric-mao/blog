---
title: "Istio系列六 网络可视化"
date: "2020-09-17"
categories: 
  - "istio"
---

###### 加入 **`网络可视化`** 组件

**1.7 以后外部集成的组件的安装文件，放到了这个路径下了 `istio-1.7.0/samples/addons/`**

```ruby
[root@master01 istio]# ll istio-1.7.0/samples/addons/
总用量 460
drwxr-xr-x. 2 root root     57 8月  22 03:00 extras
-rw-r--r--. 1 root root 398854 8月  22 03:00 grafana.yaml
-rw-r--r--. 1 root root   1960 8月  22 03:00 jaeger.yaml
-rw-r--r--. 1 root root  38508 8月  22 03:00 kiali.yaml
-rw-r--r--. 1 root root  12951 8月  22 03:00 prometheus.yaml
-rw-r--r--. 1 root root   4892 8月  22 03:00 README.md
[root@master01 istio]#

# 修改端口为 nodePort: 32001
# 安装 kiali
[root@master01 istio]# kubectl apply -f istio-1.7.0/samples/addons/kiali.yaml
[root@master01 istio]# kubectl -n istio-system get svc kiali
NAME    TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)                          AGE
kiali   NodePort   10.222.156.11   <none>        20001:32001/TCP,9090:31122/TCP   12m
[root@master01 istio]#

# 启用 prometheus 因为kiali有些功能要依赖它
[root@master01 istio]# kubectl apply -f istio-1.7.0/samples/addons/prometheus.yaml
# 启用 grafana 因为kiali有些功能要依赖它
[root@master01 istio]# kubectl apply -f istio-1.7.0/samples/addons/grafana.yaml
# 启用 jaeger 因为kiali有些功能要依赖它
[root@master01 istio]# kubectl apply -f istio-1.7.0/samples/addons/jaeger.yaml

```

###### **访问: `http://192.168.20.94:32001/kiali`**

* * *

* * *

* * *
