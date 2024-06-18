---
title: 'K8S 中使用 javaagent'
date: '2021-06-30T16:45:29+00:00'
status: publish
permalink: /2021/06/30/k8s-%e4%b8%ad%e4%bd%bf%e7%94%a8-javaagent
author: 毛巳煜
excerpt: ''
type: post
id: 7391
category:
    - Skywalking
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 前置资料

###### **[initContainers](https://kubernetes.io/zh/docs/concepts/workloads/pods/init-containers/#%E4%BD%BF%E7%94%A8-init-%E5%AE%B9%E5%99%A8%E7%9A%84%E6%83%85%E5%86%B5 "initContainers")**

- - - - - -

###### **[Volumes.emptyDir](https://kubernetes.io/zh/docs/concepts/storage/volumes/#emptydir "Volumes.emptyDir")**

**emptyDir**  
 当 Pod 分派到某个 Node 上时，`emptyDir` 卷会被创建，并且在 Pod 在该节点上运行期间，卷一直存在。 就像其名称表示的那样，卷最初是空的。 尽管 Pod 中的容器挂载 `emptyDir` 卷的路径可能相同也可能不同，这些容器都可以读写 `emptyDir` 卷中相同的文件。 当 Pod 因为某些原因被从节点上删除时，`emptyDir` 卷中的数据也会被永久删除。

> **说明： 容器崩溃并不会导致 Pod 从节点上移除，因此容器崩溃期间 `emptyDir` 卷中的数据是安全的。**

**`emptyDir` 的一些用途：**

- 缓存空间，例如基于磁盘的归并排序。
- 为耗时较长的计算任务提供检查点，以便任务能方便地从崩溃前状态恢复执行。
- 在 Web 服务器容器服务数据时，保存内容管理器容器获取的文件。

 取决于你的环境，`emptyDir` 卷存储在该节点所使用的介质上；这里的介质可以是磁盘或 SSD 或网络存储。但是，你可以将 `emptyDir.medium` 字段设置为 `"Memory"`，以告诉 Kubernetes 为你挂载 tmpfs（基于 RAM 的文件系统）。 虽然 tmpfs 速度非常快，但是要注意它与磁盘不同。 tmpfs 在节点重启时会被清除，并且你所写入的所有文件都会计入容器的内存消耗，受容器内存限制约束。

- - - - - -

##### 参考`skywalking-java-agent`为例, **[链接](https://github.com/apache/skywalking-java/blob/74b130c8271a692a217e629f4126c1043b0204e3/docs/en/setup/service-agent/java-agent/containerization.md#kubernetes "链接")**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: agent-as-sidecar
spec:
  restartPolicy: Never

  volumes:
    - name: skywalking-agent
      emptyDir: {}

  initContainers:
    - name: agent-container
      image: apache/skywalking-java-agent:8.4.0-alpine
      volumeMounts:
        - name: skywalking-agent
          mountPath: /agent
      command: [ "/bin/sh" ]
      args: [ "-c", "cp -R /skywalking/agent /agent/" ]

  containers:
    - name: app-container
      image: springio/gs-spring-boot-docker
      volumeMounts:
        - name: skywalking-agent
          mountPath: /skywalking
      env:
        - name: JAVA_TOOL_OPTIONS
          value: "-javaagent:/skywalking/agent/skywalking-agent.jar"


```

- - - - - -

- - - - - -

- - - - - -

##### 了解javaagent的运行方式

- test-jvm.jar 业务应用程序
- jmx\_prometheus\_javaagent-0.16.1.jar javaagent应用程序

**`java -jar -javaagent:`你的javaagent应用程序.jar`=`配置信息 你的应用程序.jar**

```java
java -jar -javaagent:/agent/jmx_prometheus_javaagent-0.16.1.jar=8086:/jmx-config/config.yaml test-jvm.jar

```

- - - - - -

- - - - - -

- - - - - -

<div style="overflow:hidden; clear:both; width: 100%; height: 40px; position: relative;">- - - - - -

 <span style="position: absolute;top: 50%;left: 50%; transform: translate(-50%, -50%); background-color: white;">以下为隐藏内容</span> </div> ###### 自制测试镜像

```ruby
cat > Dockerfile 
```

- - - - - -

###### 使用

```yaml
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
      - name: test-jvm
        image: test-jvm:v1.0.0
        ports:
          - containerPort: 8080
            name: test-jvm-port
            protocol: TCP
          - containerPort: 8086
            name: jmx-exporter-port
            protocol: TCP
        volumeMounts:
          - name: jmx-exporter-agent
            mountPath: /agent
          - name: jmx-exporter-config
            # 此处含义为： 告诉k8s，将ConfigMap中的配置文件，放在当前容器中的/jmx-config目录下。
            mountPath: /jmx-config
        env:
            - name: TZ
              value: 'Asia/Shanghai'
            - name: ENV_OPTIONS
              value: "-javaagent:/agent/jmx_prometheus_javaagent-0.16.1.jar=8086:/jmx-config/config.yaml"


```

- - - - - -

- - - - - -

- - - - - -