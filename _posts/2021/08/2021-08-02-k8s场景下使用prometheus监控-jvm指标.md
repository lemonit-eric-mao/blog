---
title: "K8S场景下使用prometheus监控 JVM指标"
date: "2021-08-02"
categories: 
  - "elk"
  - "prometheus"
---

##### 前置条件

**[Helm 安装Prometheus-Operator](helm-%e5%ae%89%e8%a3%85prometheus-operator "Helm 安装Prometheus-Operator")**

**[K8S 中使用 javaagent](k8s-%e4%b8%ad%e4%bd%bf%e7%94%a8-javaagent "K8S 中使用 javaagent")**

* * *

* * *

* * *

###### 添加jmx-exporter的配置文件

```ruby
cat > jmx-exporter-configmap.yaml << ERIC
apiVersion: v1
kind: ConfigMap
metadata:
  name: jmx-exporter-config
data:
  # 告诉k8s创建一个config.yaml文件
  config.yaml: |
    ---
    lowercaseOutputLabelNames: true
    lowercaseOutputName: true
    rules:
    - pattern: 'Catalina<type=GlobalRequestProcessor, name=\"(\w+-\w+)-(\d+)\"><>(\w+):'
      name: tomcat_$3_total
      labels:
        port: "$2"
        protocol: "$1"
      help: Tomcat global $3
      type: COUNTER
    - pattern: 'Catalina<j2eeType=Servlet, WebModule=//([-a-zA-Z0-9+&@#/%?=~_|!:.,;]*[-a-zA-Z0-9+&@#/%=~_|]), name=([-a-zA-Z0-9+/$%~_-|!.]*), J2EEApplication=none, J2EEServer=none><>(requestCount|maxTime|processingTime|errorCount):'
      name: tomcat_servlet_$3_total
      labels:
        module: "$1"
        servlet: "$2"
      help: Tomcat servlet $3 total
      type: COUNTER
    - pattern: 'Catalina<type=ThreadPool, name="(\w+-\w+)-(\d+)"><>(currentThreadCount|currentThreadsBusy|keepAliveCount|pollerThreadCount|connectionCount):'
      name: tomcat_threadpool_$3
      labels:
        port: "$2"
        protocol: "$1"
      help: Tomcat threadpool $3
      type: GAUGE
    - pattern: 'Catalina<type=Manager, host=([-a-zA-Z0-9+&@#/%?=~_|!:.,;]*[-a-zA-Z0-9+&@#/%=~_|]), context=([-a-zA-Z0-9+/$%~_-|!.]*)><>(processingTime|sessionCounter|rejectedSessions|expiredSessions):'
      name: tomcat_session_$3_total
      labels:
        context: "$2"
        host: "$1"
      help: Tomcat session $3 total
      type: COUNTER

ERIC


## 运行
kubectl -n default apply -f jmx-exporter-configmap.yaml

```

* * *

###### 添加**[jmx-exporter](https://github.com/prometheus/jmx_exporter "jmx-exporter")**， 用来监控jvm

```ruby
cat > test-jvm.yaml << ERIC
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: test-jvm
  name: test-jvm
spec:
  replicas: 1
  selector:
    matchLabels:
      app: test-jvm
  template:
    metadata:
      labels:
        app: test-jvm
    spec:

      volumes:
        - name: jmx-exporter-agent
          emptyDir: {}
        - name: jmx-exporter-config
          configMap:
            name: jmx-exporter-config

      initContainers:
        - name: jmx-exporter-agent-container
          image: mwendler/wget
          volumeMounts:
            - name: jmx-exporter-agent
              mountPath: /agent
          command: [ "/bin/sh" ]
          args: [ "-c", "wget -P /agent http://qiniu.dev-share.top/agent/jmx_prometheus_javaagent-0.16.1.jar" ]

      containers:
      - name: tomcat
        image: tomcat:8.5.69-jdk8-corretto
        ports:
          - containerPort: 8080
            name: tomcat-port
            protocol: TCP
          - containerPort: 8086
            name: test-jvm-port
            protocol: TCP
        volumeMounts:
          - name: jmx-exporter-agent
            mountPath: /agent
          - name: jmx-exporter-config
            # 此处含义为： 告诉k8s，将ConfigMap中的配置文件，放在当前容器中的/jmx-config目录下。
            mountPath: /jmx-config
        env:
          - name: JAVA_TOOL_OPTIONS
            value: "-javaagent:/agent/jmx_prometheus_javaagent-0.16.1.jar=8086:/jmx-config/config.yaml"

ERIC


## 运行
kubectl -n default apply -f test-jvm.yaml


```

* * *

###### 创建service

```ruby
cat > test-jvm-svc.yaml << ERIC
apiVersion: v1
kind: Service
metadata:
  labels:
    app: test-jvm
  name: test-jvm
spec:
  ports:
  - port: 8080
    name: tomcat-port
    protocol: TCP
    targetPort: 8080
  - port: 8086
    name: test-jvm-port
    protocol: TCP
    targetPort: 8086
  selector:
    app: test-jvm

ERIC


## 运行
kubectl -n default apply -f test-jvm-svc.yaml

```

* * *

* * *

* * *

###### 把jmx-exporter告诉prometheus operator

```ruby
cat > test-jvm-service-monitor.yaml << ERIC
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: test-jvm
  namespace: default
  labels:
    ## 通过 `kubectl -n dhc-prometheus get ServiceMonitor k8s-prometheus-stack-kube-prometheus --template={{.metadata.labels.release}}` 获取
    release: k8s-prometheus-stack
spec:
  namespaceSelector:                  # 监控的Service所在名称空间
    matchNames:
    - default
  selector:                           # 选择要监控的Service的标签
    ## 通过 `kubectl get svc test-jvm -o jsonpath={.metadata.labels}` 获取
    matchLabels:
      app: test-jvm
  endpoints:
  - port: test-jvm-port               # Service中对应的命名端口

ERIC


## 运行
kubectl -n default apply -f test-jvm-service-monitor.yaml

```

* * *

* * *

* * *

###### 常用grafana dashboard ID

- 8563

* * *

* * *

* * *

* * *

* * *

* * *

###### 自定义镜像(可选)

```ruby
## 下载javaagent包
wget http://qiniu.dev-share.top/agent/jmx_prometheus_javaagent-0.16.1.jar


## 构建镜像
cat > Dockerfile << ERIC
FROM alpine:latest
MAINTAINER siyu.mao@dhc.com.cn
RUN  mkdir /javaagent /agent
COPY jmx_prometheus_javaagent-0.16.1.jar /javaagent
CMD [ "sh", "-c", "mv /javaagent/jmx_prometheus_javaagent-0.16.1.jar /agent/" ]

ERIC

## 构建
docker build -t jmx_prometheus_javaagent:0.16.1 .


## 测试
docker run -it --rm -v /root/test:/agent jmx_prometheus_javaagent:0.16.1

```

* * *

* * *

* * *
