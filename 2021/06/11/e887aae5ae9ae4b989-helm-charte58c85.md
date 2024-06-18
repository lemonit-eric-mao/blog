---
title: '自定义 helm chart包'
date: '2021-06-11T04:26:38+00:00'
status: publish
permalink: /2021/06/11/%e8%87%aa%e5%ae%9a%e4%b9%89-helm-chart%e5%8c%85
author: 毛巳煜
excerpt: ''
type: post
id: 7322
category:
    - helm
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
###### **[Helm 安装/使用](http://www.dev-share.top/2020/07/16/helm-%e5%ae%89%e8%a3%85-%e4%bd%bf%e7%94%a8/ "Helm 安装/使用")**

- - - - - -

###### 创建 helm chart 模板文件

```ruby
[gitlab-runner@Gitlab-Runner ~]<span class="katex math inline">helm create demo
[gitlab-runner@Gitlab-Runner ~]</span> ll demo/
charts
Chart.yaml
templates
values.yaml ## 此文件用来设置默认值

```

- - - - - -

```ruby
rm -rf demo/templates/*

```

- - - - - -

###### 自定义 values.yaml

```ruby
[gitlab-runner@Gitlab-Runner ~]$ cat > demo/values.yaml 
```

- - - - - -

- - - - - -

- - - - - -

##### 创建部署k8s的模板文件

```ruby
[gitlab-runner@Gitlab-Runner ~]$ cat > demo/templates/deployment.yaml 
```

- - - - - -

- - - - - -

- - - - - -

###### 生成 chart包

```ruby
[gitlab-runner@Gitlab-Runner ~]$ helm package demo/ --version 0.0.1
Successfully packaged chart and saved it to: /home/gitlab-runner/test/demo-0.0.1.tgz


```

- - - - - -

- - - - - -

- - - - - -

###### 测试

```ruby
helm template mssp-web-temp ./demo-0.0.1.tgz --output-dir . \
    --namespace mssp \
    --set image.repository=nginx \
    --set image.tag=1.19.0 \
    --set deployment.serverIp=172.1.1.1 \
    --set deployment.serverPort=8088


```

- - - - - -

###### 参数对照

```ruby
helm template 这里是 .Release.Name ./demo-0.0.1.tgz --output-dir . \
    --namespace 这里是 .Release.Namespace \
    --set image.repository=这里是 .Values.image.repository \
    --set image.tag=这里是 .Values.image.tag \
    --set deployment.serverIp=这里是 .Values.deployment.serverIp \
    --set deployment.serverPort=这里是 .Values.deployment.serverPort

```

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

自定义父、子 Helm Chart 包
-------------------

<div style="overflow:hidden; clear:both; width: 100%; height: 40px; position: relative;">- - - - - -

 <span style="position: absolute;top: 50%;left: 50%; transform: translate(-50%, -50%); background-color: white;">以下为隐藏内容</span> </div> #### 创建父Chart

```shell
helm create parentchart
rm -rf parentchart/templates/*


```

#### 创建 `Chart.yaml`

```yaml
cat > parentchart/Chart.yaml 
```

#### 创建 `values.yaml`

```yaml
cat > parentchart/values.yaml 
```

#### 创建 `deployment.yaml`

```yaml
cat > parentchart/templates/deployment.yaml 
```

#### 创建 `ingress.yaml`

```yaml
{{- if .Values.ingress.enabled -}}
# 将.Release.Name存储在一个变量中, 避免在循环体调用.Release失败的问题
{{- <span class="katex math inline">releaseName := .Release.Name }}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  namespace: {{ .Release.Namespace }}
  name: {{</span>releaseName }}

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
cat > parentchart/charts/subchart/Chart.yaml 
```

#### 创建 `values.yaml`

```yaml
cat > parentchart/charts/subchart/values.yaml 
```

#### 创建 `deployment.yaml`

```yaml
cat > parentchart/charts/subchart/templates/deployment.yaml 
```

### 测试运行

```shell
helm install my-test-chart parentchart/ --dry-run --debug


```

- - - - - -

- - - - - -

- - - - - -

### **[Helm3 推送文件到 Harbor仓库](http://www.dev-share.top/2020/09/14/helm3-%e6%8e%a8%e9%80%81%e6%96%87%e4%bb%b6%e5%88%b0-harbor%e4%bb%93%e5%ba%93/ "Helm3 推送文件到 Harbor仓库")**