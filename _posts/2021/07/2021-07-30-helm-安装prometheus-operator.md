---
title: "Helm 安装Prometheus-Operator"
date: "2021-07-30"
categories: 
  - "elk"
  - "prometheus"
---

###### **[官方github](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack#kube-prometheus-stack "官方github")**

###### **[K8S-配置文件安装-Prometheus监控](k8s-%e5%ae%89%e8%a3%85-prometheus%e7%9b%91%e6%8e%a7 "K8S-配置文件安装-Prometheus监控")**

* * *

###### 添加helm chart仓库

```ruby
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

helm repo update && helm search repo

## 安装包下载到本地
helm pull prometheus-community/kube-prometheus-stack --version "17.0.3"

```

* * *

###### 安装

```ruby
kubectl create ns dhc-prometheus


## 使用本地包，离线安装
helm install k8s-prometheus-stack ./kube-prometheus-stack-17.0.3.tgz \
  -n dhc-prometheus \
  --set grafana.adminPassword='prom-operator' \
  --version "17.0.3" \
  --wait


## 在线安装
helm install k8s-prometheus-stack prometheus-community/kube-prometheus-stack \
  -n dhc-prometheus \
  --set grafana.adminPassword='prom-operator' \
  --version "17.0.3" \
  --wait

```

* * *

###### 删除

```ruby
helm uninstall k8s-prometheus-stack
kubectl delete crd alertmanagerconfigs.monitoring.coreos.com
kubectl delete crd alertmanagers.monitoring.coreos.com
kubectl delete crd podmonitors.monitoring.coreos.com
kubectl delete crd probes.monitoring.coreos.com
kubectl delete crd prometheuses.monitoring.coreos.com
kubectl delete crd prometheusrules.monitoring.coreos.com
kubectl delete crd servicemonitors.monitoring.coreos.com
kubectl delete crd thanosrulers.monitoring.coreos.com
```

* * *

* * *

* * *

###### 开放 Prometheus

```ruby
kubectl -n dhc-prometheus patch svc k8s-prometheus-stack-kube-prometheus -p '{
    "spec": {
        "ports": [
            {
                "nodePort": 30090,
                "port": 9090,
                "protocol": "TCP",
                "targetPort": 9090
            }
        ],
        "type": "NodePort"
    }
}'

```

* * *

###### 开放 Grafana

```ruby
kubectl -n dhc-prometheus patch svc k8s-prometheus-stack-grafana -p '{
    "spec": {
        "ports": [
            {
                "nodePort": 30080,
                "port": 80,
                "protocol": "TCP",
                "targetPort": 3000
            }
        ],
        "type": "NodePort"
    }
}'

```

* * *

* * *

* * *

**[K8S场景下使用prometheus监控 JVM指标](k8s%e5%9c%ba%e6%99%af%e4%b8%8b%e4%bd%bf%e7%94%a8prometheus%e7%9b%91%e6%8e%a7-jvm%e6%8c%87%e6%a0%87 "K8S场景下使用prometheus监控 JVM指标")**

* * *

* * *

* * *
