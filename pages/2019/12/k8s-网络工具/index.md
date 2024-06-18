---
title: "K8S 网络工具"
date: "2019-12-12"
categories: 
  - "k8s"
---

###### **使用 `busybox` 网络工具包**

```ruby
###### Docker 用法
docker run --rm busybox:1.28 nslookup baidu.com
```

* * *

```ruby
## K8S用法 添加工具，直接使用pod创建，不使用deployment
#### 注意：这里只使用 busybox:1.28 版本，高版本busybox里面的nslookup工具不好用
kubectl run busybox --image=busybox:1.28 --command -- sleep 36000


###### 使用工具
kubectl exec busybox -- traceroute 10.244.30.65
kubectl exec busybox -- nslookup baidu.com

Server:    10.96.0.10
Address 1: 10.96.0.10 kube-dns.kube-system.svc.cluster.local

Name:      baidu.com
Address 1: 39.156.69.79
Address 2: 220.181.38.148


###### wget 将结果输出到终端
kubectl exec busybox -- wget -qO - test-headless-server

```

**也可以使用后直接删除工具**

```shell
kubectl run busybox --image=busybox:1.28 -i --rm --restart=Never -- nslookup baidu.com


If you don't see a command prompt, try pressing enter.
Server:    10.96.0.10
Address 1: 10.96.0.10 kube-dns.kube-system.svc.cluster.local

Name:      baidu.com
Address 1: 39.156.66.10
Address 2: 110.242.68.66
pod "busybox" deleted

```

* * *

* * *

* * *

* * *

* * *

* * *

##### 一 构建镜像 **(`自己做一个`)**

###### 1 配置 Dockerfile

```ruby
[root@test1 ~]# mkdir -p /home/deploy/build-tools && cd /home/deploy/build-tools
[root@test1 ~]#
[root@test1 build-tools]# cat > Dockerfile << ERIC
# 构建方法  docker build -t tools-os:v1.0.0 .

# 应用哪个仓库 承载自己的应用程序
# 注：Dockerfile 配置文件中所有的路径都是以 Dockerfile文件所在的目录为根目录
# 指定 从Docker hub, 下载 centos:7.7.1908 镜像文件
# 在打包时相当于执行了 docker pull centos:7.7.1908
FROM centos:7.7.1908

# 设置该dockerfile的作者和联系邮箱
MAINTAINER mao_siyu@qq.com

# 将Linux的一些常用工具，加入到镜像中
RUN yum install -y epel-release telnet wget nmap net-tools httpd vim htop && \
    wget http://qiniu.dev-share.top/redis-cli -P /usr/local/bin/ && \
    chmod -R 755 /usr/local/bin/redis-cli

# 配置服务器端口
EXPOSE 80

CMD ["/usr/sbin/httpd", "-D", "FOREGROUND"]

ERIC

```

* * *

###### 2 构建

```ruby
[root@test1 build-tools]#
[root@test1 build-tools]# docker build -t tools-os:v1.0.0 .
[root@test1 build-tools]#
[root@test1 build-tools]# docker images
REPOSITORY                           TAG                 IMAGE ID            CREATED             SIZE
tools-os                             v1.0.0              7b3d382fc9ae        16 seconds ago      354 MB
[root@test1 build-tools]#
# 测试
[root@test1 build-tools]# docker run -dti --name tools-os -p 80:80 tools-os:v1.0.0
```

* * *

###### 3 推送到 harbor 私服上

```ruby
[root@test1 build-tools]#
[root@test1 build-tools]# docker tag tools-os:v1.0.0 harbor.software.com/library/tools-os:v1.0.0
[root@test1 build-tools]#
[root@test1 build-tools]# docker images
REPOSITORY                                           TAG                        IMAGE ID            CREATED             SIZE
tools-os                                             v1.0.0                     2b4e8b592d92        13 minutes ago      391MB
harbor.software.com/library/tools-os                 v1.0.0                     2b4e8b592d92        13 minutes ago      391MB
[root@test1 build-tools]#
[root@test1 build-tools]# docker push harbor.software.com/library/tools-os:v1.0.0
```

* * *

* * *

* * *

##### 二 在k8s中应用

###### 1.0 配置 k8s-tools-ns-svc.yaml 文件

```ruby
cat > k8s-tools-ns-svc.yaml << ERIC

---

# 创建命名空间
kind: Namespace
apiVersion: v1
metadata:
  # 不可以使用 下划线，
  name: k8s-tools-os
  labels:
    name: k8s-tools-os

---

# 为部署的容器开放端口
# Service
kind: Service
apiVersion: v1
metadata:
  # 所属的命名空间
  namespace: k8s-tools-os
  # Service 名称
  name: tools-service-name
  # Service 标签
  labels:
    name: tools-service-label

# 容器的详细定义
spec:
  # 告诉 K8s Docker容器对外开放几个端口
  # 如果指定为 NodePort 则这个service的端口可以被外界访问
  type: NodePort
  ports:
    - name: http
      protocol: TCP

      # port 是service的端口，只允许 k8s集群内访问
      # 此端口只有使用 Service的IP:80 才能够访问; 只允许 k8s集群内访问
      port: 80

      # targetPort 是pod的端口
      # 此端口只有使用 Pod的IP:80 才能够访问; 只允许 k8s集群内访问
      targetPort: 80

      # nodePort 是外网端口
      # 此端口只有使用 宿主机IP:30880 才能够访问; 可以被所有网络访问
      nodePort: 30880

  # 选择 Pod的label名
  selector:
    # Pod的label名, Service与Pod绑定
    app: tools-pod-label

---

ERIC

```

###### 1.1 配置 k8s-tools-deploy.yaml 文件

```ruby
cat > k8s-tools-deploy.yaml << ERIC

---

# 创建要部署的容器
# 种类：告诉 k8s 下面这些配置模板的含义(常用的包括：Namespace, Deployment, Service, Pod, ......)
kind: Deployment
# 版本号 规定格式 apps/* 必须这么写
apiVersion: apps/v1
# deploy
metadata:
  # deploy 的所属的命名空间
  namespace: k8s-tools-os
  # deploy 名称
  name: tools-deploy-name

# 容器的详细定义
spec:
  # 告诉 K8s 启动几个节点
  replicas: 1
  # 滚动升级时，容器准备就绪时间最少为30s
  minReadySeconds: 30
  # 选择模板
  selector:
    # 根据模板的labels来选择
    matchLabels:
      # 匹配下面模板中, Pod 的label名, Deploy与Pod绑定
      app: tools-pod-label



  # 定义 Pod模板
  template:
    metadata:
      # Pod模板的labels
      labels:
        # Pod的label名
        app: tools-pod-label
    spec:
      # k8s将会给应用发送SIGTERM信号，可以用来正确、优雅地关闭应用,默认为30秒
      terminationGracePeriodSeconds: 30

      # 告诉 k8s 根据设置的节点名称，将这个pod部署到哪个节点机器上（默认不指定，k8s会自动分配）;
      # 因为 nodeName(节点的名称不可以重复，因此使用nodeName只能指定一台节点服务)
      # nodeName: k8s-node1
      # 告诉 k8s 根据设置的节点标签，将这个pod部署到哪个节点机器上（默认不指定，k8s会自动分配）;
      # 因为 nodeLabels(节点的标签可以重复，因此使用nodeSelector是可以指定同一个标签的多个节点服务)
      nodeSelector:
        type: "test"

      # 配置 Docker容器
      containers:
        # Docker 镜像名
        - name: k8s-tools-os
          # 告诉 K8s 要部署的 Docker 镜像名:Tag
          image: harbor.software.com/library/tools-os:v1.0.0
          # 告诉 K8s 如果本地没有这个镜像
          # 总是拉取 pull
          # imagePullPolicy: Always
          # 只使用本地镜像，从不拉取
          # imagePullPolicy: Never
          # 默认值,本地有则使用本地镜像,不拉取
          imagePullPolicy: IfNotPresent
          ## 告诉 K8s Docker容器对外开放几个端口
          ports:
            - containerPort: 80
              #protocol: TCP
          #  #env:
          #  #  - name:
          #  #  value:

---

ERIC

```

* * *

###### 2 添加到 k8s 集群

```ruby
# 查看 pod, 想要工具在哪个节点上做测试
kubectl get pod -A -o wide
# 在test2节点机上，创建 名为(type=test) 的 label
kubectl label node test2 type=test
# 查看 label
kubectl get node --show-labels
# 启动
kubectl apply -f k8s-tools-ns-svc.yaml -f k8s-tools-deploy.yaml
```

###### 查看 service 与 pod 是否启动成功

```ruby
[root@test1 ~]# kubectl get svc,pod -n k8s-tools-os -o wide
NAME                         TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)         AGE   SELECTOR
service/tools-service-name   NodePort   10.102.223.214   <none>        80:30880/TCP    6d    app=tools-pod-label

NAME                                  READY   STATUS    RESTARTS   AGE   IP            NODE    NOMINATED NODE   READINESS GATES
pod/tools-pod-name-5bbf7d86df-h5b9b   1/1     Running   0          6d    10.244.2.18   test2   <none>           <none>
[root@test1 ~]#

# 查看详情
[root@test1 ~]# kubectl describe pod tools-pod-name-5bbf7d86df-h5b9b -n k8s-tools-os
```
