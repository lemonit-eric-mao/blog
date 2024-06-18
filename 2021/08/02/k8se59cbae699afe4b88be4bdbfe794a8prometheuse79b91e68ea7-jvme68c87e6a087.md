---
title: 'K8S场景下使用prometheus监控 JVM指标'
date: '2021-08-02T02:59:09+00:00'
status: private
permalink: /2021/08/02/k8s%e5%9c%ba%e6%99%af%e4%b8%8b%e4%bd%bf%e7%94%a8prometheus%e7%9b%91%e6%8e%a7-jvm%e6%8c%87%e6%a0%87
author: 毛巳煜
excerpt: ''
type: post
id: 7621
category:
    - ELK
    - prometheus
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
##### 前置条件

**[Helm 安装Prometheus-Operator](http://www.dev-share.top/2021/07/30/helm-%e5%ae%89%e8%a3%85prometheus-operator/ "Helm 安装Prometheus-Operator")**

**[K8S 中使用 javaagent](http://www.dev-share.top/2021/06/30/k8s-%e4%b8%ad%e4%bd%bf%e7%94%a8-javaagent/ "K8S 中使用 javaagent")**

- - - - - -

- - - - - -

- - - - - -

###### 添加jmx-exporter的配置文件

```ruby
cat > jmx-exporter-configmap.yaml (\w+):'
      name: tomcat_<span class="katex math inline">3_total
      labels:
        port: "</span>2"
        protocol: "<span class="katex math inline">1"
      help: Tomcat global</span>3
      type: COUNTER
    - pattern: 'Catalina<j2eetype j2eeapplication="none," j2eeserver="none" name="([-a-zA-Z0-9+/$%~_-|!.]*)," webmodule="//([-a-zA-Z0-9+&@#/%?=~_|!:.,;]*[-a-zA-Z0-9+&@#/%=~_|]),">(requestCount|maxTime|processingTime|errorCount):'
      name: tomcat_servlet_<span class="katex math inline">3_total
      labels:
        module: "</span>1"
        servlet: "<span class="katex math inline">2"
      help: Tomcat servlet</span>3 total
      type: COUNTER
    - pattern: 'Catalina<type name="(\w+-\w+)-(\d+)">(currentThreadCount|currentThreadsBusy|keepAliveCount|pollerThreadCount|connectionCount):'
      name: tomcat_threadpool_<span class="katex math inline">3
      labels:
        port: "</span>2"
        protocol: "<span class="katex math inline">1"
      help: Tomcat threadpool</span>3
      type: GAUGE
    - pattern: 'Catalina<type context="([-a-zA-Z0-9+/$%~_-|!.]*)" host="([-a-zA-Z0-9+&@#/%?=~_|!:.,;]*[-a-zA-Z0-9+&@#/%=~_|]),">(processingTime|sessionCounter|rejectedSessions|expiredSessions):'
      name: tomcat_session_<span class="katex math inline">3_total
      labels:
        context: "</span>2"
        host: "<span class="katex math inline">1"
      help: Tomcat session</span>3 total
      type: COUNTER

ERIC


## 运行
kubectl -n default apply -f jmx-exporter-configmap.yaml

</type></type></j2eetype>
```

- - - - - -

###### 添加**[jmx-exporter](https://github.com/prometheus/jmx_exporter "jmx-exporter")**， 用来监控jvm

```ruby
cat > test-jvm.yaml 
```

- - - - - -

###### 创建service

```ruby
cat > test-jvm-svc.yaml 
```

- - - - - -

- - - - - -

- - - - - -

###### 把jmx-exporter告诉prometheus operator

```ruby
cat > test-jvm-service-monitor.yaml 
```

- - - - - -

- - - - - -

- - - - - -

###### 常用grafana dashboard ID

- 8563

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

###### 自定义镜像(可选)

```ruby
## 下载javaagent包
wget http://qiniu.dev-share.top/agent/jmx_prometheus_javaagent-0.16.1.jar


## 构建镜像
cat > Dockerfile 
```

- - - - - -

- - - - - -

- - - - - -