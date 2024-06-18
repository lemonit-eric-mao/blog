---
title: K8S-安装-Prometheus监控
date: '2019-06-19T05:49:28+00:00'
status: publish
permalink: /2019/06/19/k8s-%e5%ae%89%e8%a3%85-prometheus%e7%9b%91%e6%8e%a7
author: 毛巳煜
excerpt: ''
type: post
id: 4858
category:
    - Kubernetes
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
#### 使用 Prometheus监控 k8s

[转载 Prometheus部署篇](https://blog.csdn.net/ywq935/article/details/80818390 "转载 Prometheus部署篇")  
参考这篇文章，内容有些bug 已经被我改掉  
**想使用 Prometheus监控 k8s，当下是需要将 Prometheus安装到k8s中，让Prometheus具有rbac权限才可以对 k8s的相关组件进行抓取**

##### 必须的配置文件

- prometheus-configmap.yaml
- prometheus-deploy.yaml
- prometheus-ing.yaml (如果没有安装ingrees这个是不需要的)
- prometheus-svc.yaml
- rbac-setup.yaml
- node-exporter.yaml

##### 将文件都存放到 k8s\_prometheus/ 文件夹下

```ruby
[root@k8s-master ~]# mkdir -p /home/deploy/k8s_prometheus/

```

- - - - - -

##### prometheus-configmap.yaml

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: kube-system
data:
  prometheus.yml: |
    global:
      scrape_interval:     15s
      evaluation_interval: 15s
    rule_files:
    - /etc/prometheus/rules.yml
    alerting:
      alertmanagers:
        - static_configs:
          - targets: ["alertmanager:9093"]
    scrape_configs:

    - job_name: 'kubernetes-apiservers'
      kubernetes_sd_configs:
      - role: endpoints
      scheme: https
      tls_config:
        ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
      relabel_configs:
      - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
        action: keep
        regex: default;kubernetes;https

    - job_name: 'kubernetes-cadvisor'
      kubernetes_sd_configs:
      - role: node
      scheme: https
      tls_config:
        ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
      relabel_configs:
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)
      - target_label: __address__
        replacement: kubernetes.default.svc:443
      - source_labels: [__meta_kubernetes_node_name]
        regex: (.+)
        target_label: __metrics_path__
        replacement: /api/v1/nodes/<span class="katex math inline">{1}/proxy/metrics/cadvisor

    - job_name: 'kubernetes-service-endpoints'
      kubernetes_sd_configs:
      - role: endpoints
      relabel_configs:
      - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scheme]
        action: replace
        target_label: __scheme__
        regex: (https?)
      - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_service_annotation_prometheus_io_port]
        action: replace
        target_label: __address__
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement:</span>1:<span class="katex math inline">2
      - action: labelmap
        regex: __meta_kubernetes_service_label_(.+)
      - source_labels: [__meta_kubernetes_namespace]
        action: replace
        target_label: kubernetes_namespace
      - source_labels: [__meta_kubernetes_service_name]
        action: replace
        target_label: kubernetes_name

    - job_name: 'kubernetes-services'
      kubernetes_sd_configs:
      - role: service
      metrics_path: /probe
      params:
        module: [http_2xx]
      relabel_configs:
      - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_probe]
        action: keep
        regex: true
      - source_labels: [__address__]
        target_label: __param_target
      - target_label: __address__
        replacement: blackbox-exporter.example.com:9115
      - source_labels: [__param_target]
        target_label: instance
      - action: labelmap
        regex: __meta_kubernetes_service_label_(.+)
      - source_labels: [__meta_kubernetes_namespace]
        target_label: kubernetes_namespace
      - source_labels: [__meta_kubernetes_service_name]
        target_label: kubernetes_name

    - job_name: 'kubernetes-ingresses'
      kubernetes_sd_configs:
      - role: ingress
      relabel_configs:
      - source_labels: [__meta_kubernetes_ingress_annotation_prometheus_io_probe]
        action: keep
        regex: true
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement:</span>1:<span class="katex math inline">2
        target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_pod_label_(.+)
      - source_labels: [__meta_kubernetes_namespace]
        action: replace
        target_label: kubernetes_namespace
      - source_labels: [__meta_kubernetes_pod_name]
        action: replace
        target_label: kubernetes_pod_name

    - job_name: 'kubernetes_node'
      tls_config:
        ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
      kubernetes_sd_configs:
      # 基于endpoint的服务发现，不再经过service代理层面
      - role: endpoints
      relabel_configs:
      - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scrape, __meta_kubernetes_endpoint_port_name]
        regex: true;prometheus-node-exporter
        action: keep
      - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scheme]
        action: replace
        target_label: __scheme__
        regex: (https?)
      - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_service_annotation_prometheus_io_port]
        action: replace
        target_label: __address__
        regex: (.+)(?::\d+);(\d+)
        replacement:</span>1:<span class="katex math inline">2
      # 去掉label name中的前缀__meta_kubernetes_service_label_
      - action: labelmap
        regex: __meta_kubernetes_service_label_(.+)
      # 为了区分所属node,把instance 从node-exporter ep的实例，替换成ep所在node的ip
      - source_labels: [__meta_kubernetes_pod_host_ip]
        regex: '(.*)'
        replacement: '</span>{1}'
        target_label: instance


```

- - - - - -

##### prometheus-deploy.yaml

```yaml
apiVersion: apps/v1beta2
kind: Deployment
metadata:
  labels:
    name: prometheus-deployment
  name: prometheus
  namespace: kube-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      containers:
      - image: prom/prometheus:v2.0.0
        name: prometheus
        command:
        - "/bin/prometheus"
        args:
        - "--config.file=/etc/prometheus/prometheus.yml"
        - "--storage.tsdb.path=/prometheus"
        - "--storage.tsdb.retention=24h"
        ports:
        - containerPort: 9090
          protocol: TCP
        volumeMounts:
        - mountPath: "/prometheus"
          name: data
        - mountPath: "/etc/prometheus"
          name: config-volume
        resources:
          requests:
            cpu: 100m
            memory: 100Mi
          limits:
            cpu: 500m
            memory: 2500Mi
      serviceAccountName: prometheus
      volumes:
      - name: data
        emptyDir: {}
      - name: config-volume
        configMap:
          name: prometheus-config


```

- - - - - -

##### prometheus-svc.yaml

```yaml
kind: Service
apiVersion: v1
metadata:
  labels:
    app: prometheus
  name: prometheus
  namespace: kube-system
spec:
  # 这里有改动，我没有选择 ClusterIP，而是简单粗暴直接暴露 普罗米修斯
  type: NodePort
  ports:
  - port: 80
    protocol: TCP
    targetPort: 9090
    # 外部访问端口
    nodePort: 30909
  selector:
    app: prometheus


```

- - - - - -

##### prometheus-ing.yaml 因为我没有安装ingrees，service又是使用端口暴露，所以这个是不需要的

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: prometheus
  namespace: kube-system
  selfLink: /apis/extensions/v1beta1/namespaces/default/ingresses/prometheus
spec:
  rules:
  - host: k8s.dev-share.top
    http:
      paths:
      - backend:
          serviceName: prometheus
          servicePort: 80
        path: /


```

- - - - - -

##### rbac-setup.yaml

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: prometheus
rules:
- apiGroups: [""]
  resources:
  - nodes
  - nodes/proxy
  - services
  - endpoints
  - pods
  verbs: ["get", "list", "watch"]
- apiGroups:
  - extensions
  resources:
  - ingresses
  verbs: ["get", "list", "watch"]
- nonResourceURLs: ["/metrics"]
  verbs: ["get"]
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: prometheus
  namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: prometheus
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: prometheus
subjects:
- kind: ServiceAccount
  name: prometheus
  namespace: kube-system


```

- - - - - -

###### node-exporter.yaml

```yaml
apiVersion: extensions/v1beta1
kind: DaemonSet
metadata:
  labels:
    k8s-app: prometheus-node-exporter
  name: prometheus-node-exporter
  namespace: kube-system
spec:
  selector:
    matchLabels:
      k8s-app: prometheus-node-exporter
  template:
    metadata:
      creationTimestamp: null
      labels:
        k8s-app: prometheus-node-exporter
    spec:
      containers:
      - args:
        - -collector.procfs
        - /host/proc
        - -collector.sysfs
        - /host/sys
        - -collector.filesystem.ignored-mount-points
        - ^/(proc|sys|host|etc|dev)(<span class="katex math inline">|/)
        - -collector.filesystem.ignored-fs-types
        - ^(tmpfs|cgroup|configfs|debugfs|devpts|efivarfs|nsfs|overlay|sysfs|proc)</span>
        image: prom/node-exporter:v0.14.0
        imagePullPolicy: IfNotPresent
        name: node-exporter
        ports:
        - containerPort: 9100
          hostPort: 9101
          name: http
          protocol: TCP
        resources: {}
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /host/proc
          name: proc
        - mountPath: /host/sys
          name: sys
        - mountPath: /rootfs
          name: root
      dnsPolicy: ClusterFirst
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      terminationGracePeriodSeconds: 30
      volumes:
      - hostPath:
          path: /proc
          type: ""
        name: proc
      - hostPath:
          path: /sys
          type: ""
        name: sys
      - hostPath:
          path: /
          type: ""
        name: root
  templateGeneration: 17
  updateStrategy:
    type: OnDelete

---
apiVersion: v1
kind: Service
metadata:
  annotations:
    prometheus.io/scrape: 'true'
    prometheus.io/app-metrics: 'true'
    prometheus.io/app-metrics-path: '/metrics'
  name: prometheus-node-exporter
  namespace: kube-system
  labels:
    app: prometheus-node-exporter
spec:
  clusterIP: None
  ports:
    - name: prometheus-node-exporter
      port: 9100
      protocol: TCP
  selector:
    k8s-app: prometheus-node-exporter
  type: ClusterIP


```

- - - - - -

##### 启动 prometheus

```ruby
[root@k8s-master deploy]# kubectl apply -R -f k8s_prometheus/
[root@k8s-master deploy]#
[root@k8s-master deploy]# kubectl get svc prometheus -n kube-system -o wide
NAME         TYPE       CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE   SELECTOR
prometheus   NodePort   10.109.43.64   <none>        80:30909/TCP   32m   app=prometheus
[root@k8s-master deploy]#
</none>
```

###### 外网访问地址：http://k8s.dev-share.top:30909/targets

###### 接下来就是 将prometheus配置到 grafana中

###### [配置Grafana](http://www.dev-share.top/2019/06/25/%E4%BD%BF%E7%94%A8-docker-compose-%E5%AE%89%E8%A3%85-prometheusalertmanagergrafana/ "配置Grafana")

- - - - - -

- - - - - -

- - - - - -