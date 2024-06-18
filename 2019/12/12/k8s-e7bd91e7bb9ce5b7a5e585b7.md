---
title: 'K8S 网络工具'
date: '2019-12-12T03:28:06+00:00'
status: publish
permalink: /2019/12/12/k8s-%e7%bd%91%e7%bb%9c%e5%b7%a5%e5%85%b7
author: 毛巳煜
excerpt: ''
type: post
id: 5192
category:
    - Kubernetes
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
###### **使用 `busybox` 网络工具包**

```ruby
###### Docker 用法
docker run --rm busybox:1.28 nslookup baidu.com

```

- - - - - -

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

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

##### 一 构建镜像 **(`自己做一个`)**

###### 1 配置 Dockerfile

```ruby
[root@test1 ~]# mkdir -p /home/deploy/build-tools && cd /home/deploy/build-tools
[root@test1 ~]#
[root@test1 build-tools]# cat > Dockerfile 
```

- - - - - -

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

- - - - - -

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

- - - - - -

- - - - - -

- - - - - -

##### 二 在k8s中应用

###### 1.0 配置 k8s-tools-ns-svc.yaml 文件

```ruby
cat > k8s-tools-ns-svc.yaml 
```

###### 1.1 配置 k8s-tools-deploy.yaml 文件

```ruby
cat > k8s-tools-deploy.yaml 
```

- - - - - -

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
</none></none></none>
```