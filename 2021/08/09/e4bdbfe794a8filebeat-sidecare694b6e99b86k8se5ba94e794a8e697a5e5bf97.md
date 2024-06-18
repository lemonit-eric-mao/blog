---
title: '使用Filebeat Sidecar收集K8S应用日志'
date: '2021-08-09T13:31:28+00:00'
status: private
permalink: /2021/08/09/%e4%bd%bf%e7%94%a8filebeat-sidecar%e6%94%b6%e9%9b%86k8s%e5%ba%94%e7%94%a8%e6%97%a5%e5%bf%97
author: 毛巳煜
excerpt: ''
type: post
id: 7674
category:
    - ELK
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 资料

###### filebeat.yml文件常用字段解释

**[资料原文链接](https://blog.csdn.net/maott/article/details/112907602 "资料原文链接")**  
**input配置**  
**`1.` paths**: 指定采集的日志文件，可以支持通配符；  
**`2.` fields**: 是额外配置增加的字段，包括节点名、IP、主题名称等；  
**`3.` scan\_frequency**: 是采集频率，默认是10秒；  
**`4.` json**: 以Json格式匹配日志message内容，拆分为log、stream、time；  
**`5.` processors.rename**: 将字段名称重命名，如：log重命名为message；  
**`6.` multiline**: 将同一条日志的多行进行合并。

**output配置**  
**`1.` hosts**: 是 kafka 集群的 broker list;  
**`2.` topic**: `'%{[fields.log_topic]}'`:指定Kafka 集群的topic,引用了filed 字段；

**Logging配置**  
**`1.` logging.level**: 默认是注释的，即不会输出debug日志，调试时建议打开有助于分析，但上生产时切记关闭，避免加大性能开销。

- - - - - -

###### **[DockerHub](https://hub.docker.com/r/elastic/filebeat "DockerHub")**

###### **[github elastic/beats](https://github.com/elastic/beats "github elastic/beats")**

- - - - - -

- - - - - -

- - - - - -

###### filebeat-configmap.yaml

```yaml
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: filebeat-config
  labels:
    k8s-app: filebeat
data:
  filebeat.yml: |-

    #============================= Filebeat inputs ================================#

    filebeat.inputs:
    # container、log
    - type: log
      enabled: true
      symlinks: true

      # 告诉filebeat要收集日志在哪个路径下
      paths:
        # 应用程序的日志输出路径，需要Java应用程序与filebeat都使用volumes.emptyDir: {}挂载
        - /logs/*.log

      fields:
        nodename: <span class="katex math inline">{MY_NODE_NAME}
        namespace:</span>{MY_POD_NAMESPACE}
        appname: <span class="katex math inline">{MY_APP_NAME}
        # 我们的规范是， 使用项目名(如：客户公司名。 注：不是微服务的项目名)
        kafka_topic:</span>{MY_POD_NAMESPACE}

      # 采集频率，默认是10秒
      scan_frequency: 10
      tail_files: true

      json.message_key: log
      json.keys_under_root: true
      json.add_error_key: true
      json.overwrite_keys: true
      processors:
        - rename:
            fields:
             - from: "log"
               to: "message"
            ignore_missing: false
            fail_on_error: true

      # java多行日志合并
      multiline:
        # 设置指定与指定模式不匹配的任何行都属于上一行
        # filebeat抓取的日志中，从头匹配 key为message对应的内容
        pattern: '^\[|^[0-9]{4}-[0-9]{2}-[0-9]{2}|^[0-9]{1,3}\.[0-9]{1,3}'
        # 是否匹配 true为将匹配的内容追加到上一行
        negate: true
        # after表示 追加到文件后面
        match: after
        timeout: 15s

      # 日志tags， 我们的规范是， 使用运行环境如： dev、uat、prod
      tags: ['dev']
      # 排除空行
      exclude_lines: ['^<span class="katex math inline">']

    #================================ Outputs  ====================================#

    # kafka的配置
    output.kafka:
      hosts: ["172.16.15.162:9092","172.16.15.163:9092","172.16.15.214:9092"]
      # 我们的规范是， 使用项目名(如：客户公司名。 注：不是微服务的项目名)
      topic: '%{[fields.kafka_topic]}'
      partition.round_robin:
        reachable_only: false
      required_acks:</span>{ACKS:1}
      compression: gzip
      max_message_bytes: 1000000

    #================================ Logging =====================================#
    #logging.level: debug


```

- - - - - -

###### deployment.yaml

```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: test-filebeat
  name: test-filebeat
spec:
  replicas: 1
  selector:
    matchLabels:
      app: test-filebeat
  template:
    metadata:
      labels:
        app: test-filebeat
    spec:

      volumes:
        - name: filebeat-config
          configMap:
            defaultMode: 0755
            name: filebeat-config
        - name: app-logs
          emptyDir: {}

      containers:
        # 容器1
        - name: java-app
          image: 172.16.15.183/library/demo-consul:2.0
          ports:
            - containerPort: 8080
              name: tomcat-port
              protocol: TCP
          volumeMounts:
            - name: app-logs
              mountPath: /logs
          env:
            - name: TZ
              value: 'Asia/Shanghai'


        # 容器2
        - name: filebeat
          image: elastic/filebeat:7.14.0
          args: [
            "-c",
            "/etc/filebeat.yml",
            "-e"
          ]
          volumeMounts:
            - name: filebeat-config
              mountPath: /etc/filebeat.yml
              readOnly: true
              subPath: filebeat.yml
            - name: app-logs
              mountPath: /logs

          env:
            - name: MY_NODE_NAME
              valueFrom:
                fieldRef:
                  fieldPath: spec.nodeName
            - name: MY_POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
            - name: MY_APP_NAME
              value: java-app

          securityContext:
            runAsUser: 0
          resources:
            limits:
              memory: 200Mi
            requests:
              cpu: 100m
              memory: 100Mi


---
apiVersion: v1
kind: Service
metadata:
  labels:
    app: test-filebeat
  name: test-filebeat
spec:
  ports:
  - port: 8080
    name: test-filebeat
    protocol: TCP
    targetPort: 8080
  selector:
    app: test-filebeat


```

- - - - - -

- - - - - -

- - - - - -

###### 测试

```ruby
## 持续向svc发请求，查看filebeat是否能够收集到数据
while :; do sleep 3s; curl -sSk 10.96.118.50:8080/test; done

```

- - - - - -

- - - - - -

- - - - - -