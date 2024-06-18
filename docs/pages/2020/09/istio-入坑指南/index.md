---
title: "Istio 入坑指南"
date: "2020-09-11"
categories: 
  - "istio"
---

###### `upstream connect error or disconnect/reset before headers. reset reason: connection failure`

###### 解决方法， 为 Deployment 添加探测

###### **[配置Liveness和Readiness探测](https://k8smeetup.github.io/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/ "配置Liveness和Readiness探测")**

```yaml
---
kind: Deployment
apiVersion: apps/v1
metadata:
  namespace: spring-boot
  name: deployment-${CI_PROJECT_NAME}-v11
  labels:
    app: deployment-${CI_PROJECT_NAME}
    version: v11
spec:
  replicas: 1
  minReadySeconds: 30
  selector:
    matchLabels:
      app: pod-${CI_PROJECT_NAME}
      version: v11

  template:
    metadata:
      labels:
        app: pod-${CI_PROJECT_NAME}
        version: v11
      annotations:
        eric.mao: "6"

    spec:
      terminationGracePeriodSeconds: 60
      volumes:
        - name: config-volume
          configMap:
            name: configmap-${CI_PROJECT_NAME}
      containers:
        - name: ${CI_PROJECT_NAME}
          image: 192.168.20.93/library/${CI_PROJECT_NAME}:${CI_COMMIT_TAG}
          imagePullPolicy: Always
          ports:
            - containerPort: 8071
              protocol: TCP
          volumeMounts:
            - name: config-volume
              mountPath: /app/bootstrap.yml
              subPath: bootstrap.yml
          # 探测
          livenessProbe:
            httpGet:
              # 这个路径是存在 k8s源码中的
              path: /healthz
              port: 8071
              httpHeaders:
            # 首次执行探测时等待10秒
            initialDelaySeconds: 10
            # 每隔3秒执行一次探测
            periodSeconds: 3

```

* * *

###### 说明

   livenessProbe 指定 kubelet 需要`每隔3秒执行一次` liveness probe。`initialDelaySeconds` 指定 kubelet 在该执行`第一次探测之前需要等待10秒钟`。该探针将向容器中的 server 的8071端口发送一个`HTTP GET 请求`。如果server的`/healthz`路径的 handler 返回一个成功的返回码，kubelet 就会认定该容器是活着的并且很健康。如果返回失败的返回码，kubelet 将杀掉该容器并重启它。    任何大于200小于400的返回码都会认定是成功的返回码。其他返回码都会被认为是失败的返回码。

###### 注意

   如果探测的时候设置的过短，而程序启动时间又比较长，这时要注意适当的调整时间，否则会无限重启

* * *

* * *

* * *

###### **[Istio CNI 插件](https://istio.io/latest/zh/docs/setup/additional-setup/cni/ "Istio CNI 插件")**

   默认情况下，Istio 会在网格中部署的 pods 上注入一个 initContainer：istio-init。 istio-init 容器会将 pod 的网络流量劫持到 Istio sidecar 代理上。 这需要用户或部署 pods 的 Service Account 具有足够的部署 NET\_ADMIN 容器的 Kubernetes RBAC 权限。 Istio 用户权限的提升，对于某些组织的安全政策来说，可能是难以接受的。 Istio CNI 插件就是一个能够替代 istio-init 容器来实现相同的网络功能但却不需要 Istio 用户申请额外的 Kubernetes RBAC 授权的方案。

   Istio CNI 插件会在 Kubernetes pod 生命周期的网络设置阶段完成 Istio 网格的 pod 流量转发设置工作，因此用户在部署 pods 到 Istio 网格中时，不再需要配置 NET\_ADMIN 功能需求了。 Istio CNI 插件代替了 istio-init 容器所实现的功能。

* * *

* * *

* * *
