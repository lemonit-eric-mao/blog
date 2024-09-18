---
title: "Istio系列二 自动化部署SpringBoot应用程序到K8S"
date: "2020-09-09"
categories: 
  - "istio"
---

#### 迁移过程使用 **[gitlab-runner ci/cd](gitlab-ci-%e6%8c%81%e7%bb%ad%e9%9b%86%e6%88%90-%e7%94%9f%e4%ba%a7%e6%a1%88%e4%be%8b "gitlab-runner ci/cd")** 自动化部署 SpringBoot 到 k8s集群

* * *

###### Dockerfile写法

```ruby
FROM openjdk:8-jre-alpine
MAINTAINER mao_siyu@qq.com
WORKDIR /app
COPY ./target/${CI_PROJECT_NAME}.jar /app
EXPOSE 8066
# 说明一下为什么要添加 "-Dspring.config.location=bootstrap.yml"
#    因为我把 bootstrap.yml文件放到了 K8S的ConfigMap中
#    然后在部署Deployment时会将 ConfigMap中的bootstrap.yml文件，在映射到容器中的 /app目录下， 就是这行代码： mountPath: /app/bootstrap.yml
CMD ["java", "-jar", "-Dspring.config.location=bootstrap.yml", "${CI_PROJECT_NAME}.jar"]
```

* * *

###### SpringBoot 自动化部署 .gitlab-ci.yml写法

```yaml
my_tag:
  script:
    - mvn clean install package -U -D maven.test.skip=true
    # 相当于: docker build -t harbor.software.com/library/${CI_PROJECT_NAME}:${CI_COMMIT_TAG} -f ./Dockerfile .
    - envsubst < Dockerfile | docker build -t harbor.software.com/library/${CI_PROJECT_NAME}:${CI_COMMIT_TAG} -f - .
    - docker login harbor.software.com -u admin -p Harbor12345
    - docker push harbor.software.com/library/${CI_PROJECT_NAME}:${CI_COMMIT_TAG}

    # http://192.168.20.93/chartrepo    chartrepo为关键字
    - helm repo add harbor-repo http://192.168.20.93/chartrepo/helm3/ --username admin --password Harbor12345

    # 推送到Harbor
    - helm create ${CI_PROJECT_NAME} && rm -rf ${CI_PROJECT_NAME}/templates/*
    - envsubst < deploy-k8s/service.yaml > ${CI_PROJECT_NAME}/templates/service.yaml
    - envsubst < deploy-k8s/deployment.yaml > ${CI_PROJECT_NAME}/templates/deployment.yaml
    - helm push ${CI_PROJECT_NAME} harbor-repo --version=${CI_COMMIT_TAG}

    # 在k8s上运行
    - envsubst < deploy-k8s/namespace.yaml  | kubectl apply -f -
    - envsubst < deploy-k8s/service.yaml    | kubectl apply -f -
    - envsubst < deploy-k8s/deployment.yaml | kubectl apply -f -

  after_script:
    - docker system prune -f
  only:
    - tags
  stage: build
  tags:
    - devops
```

* * *

###### namespace.yaml

```yaml
---
kind: Namespace
apiVersion: v1
metadata:
  name: spring-boot
  labels:
    name: spring-boot

```

* * *

###### configmap.yaml

```yaml
---
apiVersion: v1
kind: ConfigMap
metadata:
  namespace: spring-boot
  name: configmap-${CI_PROJECT_NAME}
data:
  bootstrap.yml: |
    spring:
      application:
        name: ${CI_PROJECT_NAME}

    server:
      port: 8066

    logging:
      level:
        com.netflix: WARN
        org.springframework.web: WARN
        com.app.cloud: DEBUG

```

* * *

###### deployment.yaml

**[Istio对Pod 和 Service的要求](https://istio.io/latest/zh/docs/ops/deployment/requirements/ "Istio对Pod 和 Service的要求")**

```yaml
---
kind: Deployment
apiVersion: apps/v1
metadata:
  namespace: spring-boot
  name: ${CI_PROJECT_NAME}
  labels:
    # 这个标签用于Istio 在分布式追踪中添加上下文信息。
    app: ${CI_PROJECT_NAME}
    # 这个标签用于Istio 在特定方式部署的应用中表示版本
    version: v1

spec:
  replicas: 1
  # 当新的pod启动 5s后，再kill掉旧的pod
  minReadySeconds: 5
  selector:
    matchLabels:
      # 这个标签用于Istio 在分布式追踪中添加上下文信息。
      app: ${CI_PROJECT_NAME}
      # 这个标签用于Istio 在特定方式部署的应用中表示版本
      version: v1

  template:
    metadata:
      labels:
        # 这个标签用于Istio 在分布式追踪中添加上下文信息。
        app: ${CI_PROJECT_NAME}
        # 这个标签用于Istio 在特定方式部署的应用中表示版本
        version: v1
      # 配置 ConfigMap 触发热更新
      #   如果使用ConfigMap的subPath挂载为Container的Volume，Kubernetes不会对Pod做自动热更新
      #   可以通过修改ConfigMap的 pod的 annotations的方式强制触发滚动更新
      annotations:
        # 随意写个注解，需要滚动更新pod时，改一下注解的值即可
        eric.mao: "6"

    spec:
      # 可以定义优雅退出的宽限期，即在收到停止请求后，有多少时间来进行资源释放或者做其它操作，如果到了最大时间还没有停止，会被强制结束，默认值：30
      terminationGracePeriodSeconds: 60
      # 引入 ConfigMap 配置文件
      volumes:
        # 为这个引入起个名
        - name: config-volume
          configMap:
            # 告诉k8s，引入哪个ConfigMap
            name: ${CI_PROJECT_NAME}
      #
      containers:
        - name: ${CI_PROJECT_NAME}
          image: 192.168.20.93/library/${CI_PROJECT_NAME}:${CI_COMMIT_TAG}
          imagePullPolicy: Always
          ports:
            - containerPort: 8066
              protocol: TCP
          # 告诉容器中的应用程序，使用哪个配置文件
          volumeMounts:
            - name: config-volume
              # /app 是docker打包时，指定的工作目录，在Dockerfile文件中
              # 此处含义为： 告诉k8s，将ConfigMap中的配置文件，替换容器中的 /app/bootstrap.yml 文件
              mountPath: /app/bootstrap.yml
              # 告诉k8s，使用ConfigMap中的哪个配置文件
              subPath: bootstrap.yml

```

* * *

###### service.yaml

```yaml
---
kind: Service
apiVersion: v1
metadata:
  namespace: spring-boot
  name: ${CI_PROJECT_NAME}
  labels:
    name: ${CI_PROJECT_NAME}

spec:
  type: NodePort
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 8066
      nodePort: 30001

  selector:
    app: ${CI_PROJECT_NAME}

```

* * *

###### 构建成功后，查看应用程序

```ruby
[root@master01 ~]# kubectl -n spring-boot get all
NAME                                               READY   STATUS    RESTARTS   AGE
pod/organization-service-6985967cb4-5ghtk          1/1     Running   0          2m25s
pod/-orgservice-new-7d69f67c8f-wcwvs               1/1     Running   0          102s
pod/specialroutes-service-5468f556d8-xxf7x         1/1     Running   0          55s

NAME                            TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
service/organization-service    ClusterIP   10.222.112.77    <none>        80/TCP    16h
service/orgservice-new          ClusterIP   10.222.133.201   <none>        80/TCP    16h
service/specialroutes-service   ClusterIP   10.222.168.192   <none>        80/TCP    16h

NAME                                               READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/organization-service               1/1     1            1           2m26s
deployment.apps/orgservice-new                     1/1     1            1           102s
deployment.apps/specialroutes-service              1/1     1            1           55s

NAME                                               DESIRED   CURRENT   READY   AGE
replicaset.apps/organization-service-6985967cb4    1         1         1       2m26s
replicaset.apps/orgservice-new-7d69f67c8f          1         1         1       102s
replicaset.apps/specialroutes-service-5468f556d8   1         1         1       55s
[root@master01 ~]#
```

* * *

* * *

* * *
