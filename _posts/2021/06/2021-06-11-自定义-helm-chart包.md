---
title: "自定义 helm chart包"
date: "2021-06-11"
categories: 
  - "helm"
---

###### **[Helm 安装/使用](helm-%e5%ae%89%e8%a3%85-%e4%bd%bf%e7%94%a8 "Helm 安装/使用")**

* * *

###### 创建 helm chart 模板文件

```ruby
[gitlab-runner@Gitlab-Runner ~]$ helm create demo
[gitlab-runner@Gitlab-Runner ~]$ ll demo/
charts
Chart.yaml
templates
values.yaml ## 此文件用来设置默认值
```

* * *

```ruby
rm -rf demo/templates/*
```

* * *

###### 自定义 values.yaml

```ruby
[gitlab-runner@Gitlab-Runner ~]$ cat > demo/values.yaml << ERIC
replicaCount: 1
deployment:
  serverIp: ''
  serverPort: ''

image:
  repository: ''
  pullPolicy: Always
  tag: ''

annotations:
  id: ''

ERIC

```

* * *

* * *

* * *

##### 创建部署k8s的模板文件

```ruby
[gitlab-runner@Gitlab-Runner ~]$ cat > demo/templates/deployment.yaml << ERIC
kind: Deployment
apiVersion: apps/v1
metadata:
  namespace: {{ .Release.Namespace }}
  name: {{ .Release.Name }}
  labels:
    app: {{ .Release.Name }}
    version: v1

spec:
  replicas: {{ .Values.replicaCount }}
  minReadySeconds: 5
  selector:
    matchLabels:
      app: {{ .Release.Name }}
      version: v1

  template:
    metadata:
      labels:
        app: {{ .Release.Name }}
        version: v1
      annotations:
        id: "{{ .Values.annotations.id }}"

    spec:
      terminationGracePeriodSeconds: 60
      containers:
        - name: {{ .Release.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - containerPort: 8080
              protocol: TCP
          resources:
            limits:
              cpu: '2'
              memory: 2Gi
            requests:
              cpu: '2'
              memory: 2Gi
          env:
            - name: SERVER_IP
              value: '{{ .Values.deployment.serverIp }}'
            - name: SERVER_PORT
              value: '{{ .Values.deployment.serverPort }}'
ERIC

```

* * *

* * *

* * *

###### 生成 chart包

```ruby
[gitlab-runner@Gitlab-Runner ~]$ helm package demo/ --version 0.0.1
Successfully packaged chart and saved it to: /home/gitlab-runner/test/demo-0.0.1.tgz

```

* * *

* * *

* * *

###### 测试

```ruby
helm template mssp-web-temp ./demo-0.0.1.tgz --output-dir . \
    --namespace mssp \
    --set image.repository=nginx \
    --set image.tag=1.19.0 \
    --set deployment.serverIp=172.1.1.1 \
    --set deployment.serverPort=8088

```

* * *

###### 参数对照

```ruby
helm template 这里是 .Release.Name ./demo-0.0.1.tgz --output-dir . \
    --namespace 这里是 .Release.Namespace \
    --set image.repository=这里是 .Values.image.repository \
    --set image.tag=这里是 .Values.image.tag \
    --set deployment.serverIp=这里是 .Values.deployment.serverIp \
    --set deployment.serverPort=这里是 .Values.deployment.serverPort
```

* * *

* * *

* * *

* * *

* * *

* * *

## 自定义父、子 Helm Chart 包

#### 创建父Chart

```shell
helm create parentchart
rm -rf parentchart/templates/*

```

#### 创建 `Chart.yaml`

```yaml
cat > parentchart/Chart.yaml << ERIC
apiVersion: v2
name: parentchart
description: A Helm Chart for the main application using Nginx.
version: 1.0.0
appVersion: "1.0.0"

dependencies:
  - name: subchart                          # 子chart的名称，需要与【子chart】的【parentchart/charts/subchart/Chart.yaml】文件中的【name名】一致
    condition: enableCharts.subchart        # enable-charts.subchart 它必须是values.yaml文件中自定义的配置项

ERIC

```

#### 创建 `values.yaml`

```yaml
cat > parentchart/values.yaml << ERIC

# 设置父 Chart 的配置
nginx:
  image: "nginx:1.21.1"  # 使用 Nginx 的镜像

# 要启用的子chart
## 此功能要依赖于 parentchart/Chart.yaml文件中的 dependencies 配置
enableCharts:
  subchart: true

# 覆盖子 Chart 的values.yaml
## 子chart的名称，需要与子chart的目录名一致，就是parentchart/charts/subchart/
subchart:
  image: "httpd:alpine3.18"  # 使用 Apache HTTP Server 的镜像


ingress:
  enabled: true
  className: "nginx"
  #  annotations: {}
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
    nginx.ingress.kubernetes.io/proxy-body-size: "50m"
    nginx.ingress.kubernetes.io/cors-allow-headers: DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization
    nginx.ingress.kubernetes.io/cors-allow-methods: 'PUT, GET, POST, OPTIONS'
    nginx.ingress.kubernetes.io/cors-allow-origin: '*'
    nginx.ingress.kubernetes.io/enable-cors: 'true'

  hosts:
    - host: chart-example.local
      serviceName:
      paths:
        - path: /
          pathType: Prefix
  #  tls: []
  tls:
    - secretName: chart-example-tls
      hosts:
        - chart-example.local

ERIC

```

#### 创建 `deployment.yaml`

```yaml
cat > parentchart/templates/deployment.yaml << ERIC
apiVersion: apps/v1
kind: Deployment
metadata:
  name: parentchart-deployment
  labels:
    app: parentchart
spec:
  replicas: 1
  selector:  # 添加 selector 字段
    matchLabels:
      app: parentchart  # 与 Pod 模板的 metadata.labels 字段匹配
  template:
    metadata:
      labels:
        app: parentchart
    spec:
      containers:
        - name: nginx-container
          image: {{ .Values.nginx.image }}
          ports:
            - containerPort: 80

ERIC

```

#### 创建 `ingress.yaml`

```yaml
{{- if .Values.ingress.enabled -}}
# 将.Release.Name存储在一个变量中, 避免在循环体调用.Release失败的问题
{{- $releaseName := .Release.Name }}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  namespace: {{ .Release.Namespace }}
  name: {{ $releaseName }}

  {{- with .Values.ingress.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}

spec:
  ingressClassName: {{ .Values.ingress.className }}

  rules:
    {{- range .Values.ingress.hosts }}
    - host: {{ .host | quote }}
      http:
        paths:
          {{- range .paths }}
          - path: {{ .path }}
            pathType: {{ .pathType }}
            backend:
              service:
                name: {{ $releaseName }}
                port:
                  number: 80
          {{- end }}
    {{- end }}


  {{- if .Values.ingress.tls }}
  tls:
    {{- range .Values.ingress.tls }}
    - hosts:
        {{- range .hosts }}
        - {{ . | quote }}
        {{- end }}
      secretName: {{ .secretName }}
    {{- end }}
  {{- end }}

{{- end }}

```

#### 创建子chart

```shell
helm create parentchart/charts/subchart
rm -rf parentchart/charts/subchart/templates/*

```

#### 创建 `Chart.yaml`

```yaml
cat > parentchart/charts/subchart/Chart.yaml << ERIC
apiVersion: v2
name: subchart
description: A Helm Chart for the sub application using Apache HTTP Server (httpd).
version: 1.0.0
appVersion: "1.0.0"

ERIC

```

#### 创建 `values.yaml`

```yaml
cat > parentchart/charts/subchart/values.yaml << ERIC
# 设置子 Chart 的配置
image: "httpd:latest"  # 使用 Apache HTTP Server 的镜像

ERIC

```

#### 创建 `deployment.yaml`

```yaml
cat > parentchart/charts/subchart/templates/deployment.yaml << ERIC
apiVersion: apps/v1
kind: Deployment
metadata:
  name: subchart-deployment
  labels:
    app: subchart
spec:
  replicas: 1
  selector:  # 添加 selector 字段
    matchLabels:
      app: subchart  # 与 Pod 模板的 metadata.labels 字段匹配
  template:
    metadata:
      labels:
        app: subchart
    spec:
      containers:
        - name: subchart-container
          image: {{ .Values.image }}
          ports:
            - containerPort: 80

ERIC

```

### 测试运行

```shell
helm install my-test-chart parentchart/ --dry-run --debug

```

* * *

* * *

* * *

### **[Helm3 推送文件到 Harbor仓库](helm3-%e6%8e%a8%e9%80%81%e6%96%87%e4%bb%b6%e5%88%b0-harbor%e4%bb%93%e5%ba%93 "Helm3 推送文件到 Harbor仓库")**
