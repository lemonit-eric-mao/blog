---
title: 'Docker 、kubernetes 分别部署zookeeper集群的方法'
date: '2019-08-23T07:44:28+00:00'
status: publish
permalink: /2019/08/23/docker-%e3%80%81kubernetes-%e5%88%86%e5%88%ab%e9%83%a8%e7%bd%b2zookeeper%e9%9b%86%e7%be%a4%e7%9a%84%e6%96%b9%e6%b3%95
author: 毛巳煜
excerpt: ''
type: post
id: 5013
category:
    - Kubernetes
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
#### 方法一、docker部署zookeeper

##### 创建docker-compose.yaml文件

```yaml
version: '2'
services:
    zoo1:
        image: zookeeper
        restart: always
        ports:
            - 2181:2181
        environment:
            ZOO_MY_ID: 1
            ZOO_SERVERS: server.1=zoo1:2888:3888 server.2=zoo2:2888:3888 server.3=zoo3:2888:3888

    zoo2:
        image: zookeeper
        restart: always
        ports:
            - 2182:2181
        environment:
            ZOO_MY_ID: 2
            ZOO_SERVERS: server.1=zoo1:2888:3888 server.2=zoo2:2888:3888 server.3=zoo3:2888:3888

    zoo3:
        image: zookeeper
        restart: always
        ports:
            - 2183:2181
        environment:
            ZOO_MY_ID: 3
            ZOO_SERVERS: server.1=zoo1:2888:3888 server.2=zoo2:2888:3888 server.3=zoo3:2888:3888


```

#### 方法二、kubernetes 部署zookeeper

##### 创建zk-deployment.yaml文件

```yaml
---
apiVersion: v1
kind: Namespace
metadata:
   name: paas-cloud-dev2
   labels:
     name: paas-cloud-dev2
---
kind: Deployment
apiVersion: extensions/v1beta1
metadata:
  name: zk-pod-0
  namespace: paas-cloud-dev2
  labels:
    name: zk-pod-0
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: zk-pod0
    spec:
      hostname: zk-0
      nodeSelector:
        zknode0: "true"
      volumes:
        - name: zk-data
          hostPath:
            path: /data/zk-cluster/zk-data-0
        - name: zk-logs
          hostPath:
            path: /data/zk-cluster/zk-logs-0
      containers:
      - name: zk-0
        image: zookeeper
        imagePullPolicy: IfNotPresent
        volumeMounts:
        - name: zk-data
          readOnly: false
          mountPath: "/data/zk-data"
        - name: zk-logs
          readOnly: false
          mountPath: "/data/zk-logs"
        ports:
        - containerPort: 2181
        - containerPort: 2888
        - containerPort: 3888
        #command: ['tail', '-f', '/etc/hosts']
        env:
        - name: ZOO_MY_ID
          value: '0'
        - name: ZOO_SERVERS
          # 注意！！k8s使用到virtual ip，因此，本机必须使用0.0.0.0 ip地址，否则本机zk启动会异常：
          # ERROR [zk1/10.0.0.251:3888:QuorumCnxManager<span class="katex math inline">Listener@547] - Exception while listening
          # java.net.BindException: Address not available (Bind failed)错误
          value: server.0=0.0.0.0:2888:3888;2181  server.1=zk-svc-1:2888:3888;2181  server.2=zk-svc-2:2888:3888;2181
        - name: ZOO_DATA_DIR
          value: '/data/zk-data'
        - name: ZOO_DATA_LOG_DIR
          value: '/data/zk-logs'

---
kind: Deployment
apiVersion: extensions/v1beta1
metadata:
  name: zk-pod-1
  namespace: paas-cloud-dev2
  labels:
    name: zk-pod-1
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: zk-pod1
    spec:
      hostname: zk-1
      nodeSelector:
        zknode1: "true"
      volumes:
        - name: zk-data
          hostPath:
            path: /data/zk-cluster/zk-data-1
        - name: zk-logs
          hostPath:
            path: /data/zk-cluster/zk-logs-1
      containers:
      - name: zk-1
        image: zookeeper
        imagePullPolicy: IfNotPresent
        volumeMounts:
        - name: zk-data
          readOnly: false
          mountPath: "/data/zk-data"
        - name: zk-logs
          readOnly: false
          mountPath: "/data/zk-logs"
        ports:
        - containerPort: 2181
        - containerPort: 2888
        - containerPort: 3888
        #command: ['tail', '-f', '/etc/hosts']
        env:
        - name: ZOO_MY_ID
          value: '1'
        - name: ZOO_SERVERS
          # 注意！！k8s使用到virtual ip，因此，本机必须使用0.0.0.0 ip地址，否则本机zk启动会异常：
          # ERROR [zk1/10.0.0.251:3888:QuorumCnxManager</span>Listener@547] - Exception while listening
          # java.net.BindException: Address not available (Bind failed)错误
          value: server.0=zk-svc-0:2888:3888;2181  server.1=0.0.0.0:2888:3888;2181  server.2=zk-svc-2:2888:3888;2181
        - name: ZOO_DATA_DIR
          value: '/data/zk-data'
        - name: ZOO_DATA_LOG_DIR
          value: '/data/zk-logs'

---
kind: Deployment
apiVersion: extensions/v1beta1
metadata:
  name: zk-pod-2
  namespace: paas-cloud-dev2
  labels:
    name: zk-pod-2
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: zk-pod2
    spec:
      hostname: zk-2
      nodeSelector:
        zknode2: "true"
      volumes:
        - name: zk-data
          hostPath:
            path: /data/zk-cluster/zk-data-2
        - name: zk-logs
          hostPath:
            path: /data/zk-cluster/zk-logs-2
      containers:
      - name: zk-2
        image: zookeeper
        imagePullPolicy: IfNotPresent
        volumeMounts:
        - name: zk-data
          readOnly: false
          mountPath: "/data/zk-data"
        - name: zk-logs
          readOnly: false
          mountPath: "/data/zk-logs"
        ports:
        - containerPort: 2181
        - containerPort: 2888
        - containerPort: 3888
        #command: ['tail', '-f', '/etc/hosts']
        env:
        - name: ZOO_MY_ID
          value: '2'
        - name: ZOO_SERVERS
          # 注意！！k8s使用到virtual ip，因此，本机必须使用0.0.0.0 ip地址，否则本机zk启动会异常：
          # ERROR [zk1/10.0.0.251:3888:QuorumCnxManager$Listener@547] - Exception while listening
          # java.net.BindException: Address not available (Bind failed)错误
          value: server.0=zk-svc-0:2888:3888;2181  server.1=zk-svc-1:2888:3888;2181  server.2=0.0.0.0:2888:3888;2181
        - name: ZOO_DATA_DIR
          value: '/data/zk-data'
        - name: ZOO_DATA_LOG_DIR
          value: '/data/zk-logs'

```

##### 创建zk-service.yaml文件

```yaml
---
kind: Service
apiVersion: v1
metadata:
  name: zk-svc-0
  namespace: paas-cloud-dev2
  labels:
    app: zk-svc-node0
spec:
  type: NodePort
  ports:
  - name: port-2181
    port: 2181
  - name: port-2888
    port: 2888
  - name: port-3888
    port: 3888
  selector:
    app: zk-pod0

---
kind: Service
apiVersion: v1
metadata:
  name: zk-svc-1
  namespace: paas-cloud-dev2
  labels:
    app: zk-svc-node1
spec:
  type: NodePort
  ports:
  - name: port-2181
    port: 2181
  - name: port-2888
    port: 2888
  - name: port-3888
    port: 3888
  selector:
    app: zk-pod1

---
kind: Service
apiVersion: v1
metadata:
  name: zk-svc-2
  namespace: paas-cloud-dev2
  labels:
    app: zk-svc-node2
spec:
  type: NodePort
  ports:
  - name: port-2181
    port: 2181
  - name: port-2888
    port: 2888
  - name: port-3888
    port: 3888
  selector:
    app: zk-pod2

```