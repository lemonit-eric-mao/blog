---
title: "K8S 部署 Java 程序"
date: "2020-08-05"
categories: 
  - "java"
  - "k8s"
  - "spring-boot"
---

###### 目录

```ruby
# 创建目录，并且将 java程序包上传到此目录, UserCenter.java
mkdir /home/deploy/spring-boot/ && cd /home/deploy/spring-boot/
```

* * *

###### 编写 Dockerfile

```ruby
cat > Dockerfile << ERIC
# 构建方法  docker build -t user-center:v1.0.0 .

# 在打包时相当于执行了 docker pull openjdk:8-jre-alpine
FROM openjdk:8-jre-alpine

# 设置该dockerfile的作者和联系邮箱
MAINTAINER mao_siyu@qq.com

# RUN mkdir -p 用于在Image里创建一个文件夹，将来用于保存我们的代码
RUN mkdir -p /app

# WORKDIR 是将我们创建的文件夹做为工作目录
WORKDIR /app

# 将Linux的一些常用工具，加入到镜像中
COPY . /app

# 配置服务器端口
EXPOSE 8080

CMD ["java", "-jar", "UserCenter.jar"]

ERIC

```

* * *

###### 打包、测试运行

```ruby
docker build -t user-center:v1.0.0 .

docker run -it --rm -p 8080:8080 user-center:v1.0.0

```

* * *

* * *

* * *

###### 将镜像上传到 Harbor 私有仓库

```ruby
docker tag user-certer:v1.0.0 192.168.20.94:8082/library/user-certer:v1.0.0

docker login http://192.168.20.94:8082 -u admin -p Harbor12345

docker push 192.168.20.94:8082/library/user-certer:v1.0.0

```

* * *

* * *

* * *

##### 部署到 K8S

###### 创建命名空间

```ruby
kubectl create ns user-center-ns
```

###### user-center-svc.yaml 文件

```ruby
cat > user-center-svc.yaml << ERIC

---

# Service
kind: Service
apiVersion: v1
metadata:
  namespace: user-center-ns
  name: user-center
  labels:
    name: user-center

# 容器的详细定义
spec:
  ports:
    - name: http
      protocol: TCP
      port: 8080
      targetPort: 8080

  selector:
    app: user-center

---

ERIC

```

* * *

###### user-center-deploy.yaml 文件

```ruby
cat > user-center-deploy.yaml << ERIC

---

# 创建要部署的容器
kind: Deployment
# 版本号 规定格式 apps/* 必须这么写
apiVersion: apps/v1
metadata:
  namespace: user-center-ns
  name: user-center

# 容器的详细定义
spec:
  replicas: 1
  minReadySeconds: 30
  selector:
    matchLabels:
      app: user-center



  template:
    metadata:
      labels:
        app: user-center
    spec:
      # k8s将会给应用发送SIGTERM信号，可以用来正确、优雅地关闭应用,默认为30秒
      terminationGracePeriodSeconds: 30

      # 配置 Docker容器
      containers:
        # Docker 容器名
        - name: user-center-ns
          image: 192.168.20.94:8082/library/user-certer:v1.0.0
          imagePullPolicy: Always
          ports:
            - containerPort: 80

---

ERIC

```

* * *

###### 查看集群 状态

```ruby
kubectl apply -f user-center-svc.yaml -f user-center-deploy.yaml
```
