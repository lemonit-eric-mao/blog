---
title: 'K8S 部署 Java 程序'
date: '2020-08-05T03:26:33+00:00'
status: publish
permalink: /2020/08/05/k8s-%e9%83%a8%e7%bd%b2-java-%e7%a8%8b%e5%ba%8f
author: 毛巳煜
excerpt: ''
type: post
id: 5643
category:
    - Java
    - Kubernetes
    - spring-boot
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### 目录

```ruby
# 创建目录，并且将 java程序包上传到此目录, UserCenter.java
mkdir /home/deploy/spring-boot/ && cd /home/deploy/spring-boot/

```

- - - - - -

###### 编写 Dockerfile

```ruby
cat > Dockerfile 
```

- - - - - -

###### 打包、测试运行

```ruby
docker build -t user-center:v1.0.0 .

docker run -it --rm -p 8080:8080 user-center:v1.0.0


```

- - - - - -

- - - - - -

- - - - - -

###### 将镜像上传到 Harbor 私有仓库

```ruby
docker tag user-certer:v1.0.0 192.168.20.94:8082/library/user-certer:v1.0.0

docker login http://192.168.20.94:8082 -u admin -p Harbor12345

docker push 192.168.20.94:8082/library/user-certer:v1.0.0


```

- - - - - -

- - - - - -

- - - - - -

##### 部署到 K8S

###### 创建命名空间

```ruby
kubectl create ns user-center-ns

```

###### user-center-svc.yaml 文件

```ruby
cat > user-center-svc.yaml 
```

- - - - - -

###### user-center-deploy.yaml 文件

```ruby
cat > user-center-deploy.yaml 
```

- - - - - -

###### 查看集群 状态

```ruby
kubectl apply -f user-center-svc.yaml -f user-center-deploy.yaml

```