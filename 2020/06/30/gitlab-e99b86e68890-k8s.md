---
title: 'k8s 配置文件详解'
date: '2020-06-30T11:41:21+00:00'
status: private
permalink: /2020/06/30/gitlab-%e9%9b%86%e6%88%90-k8s
author: 毛巳煜
excerpt: ''
type: post
id: 5358
category:
    - Kubernetes
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
###### **PersistentVolumeClaim** storageClass

`持久卷申领（PersistentVolumeClaim，PVC）`

```yaml
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  namespace: dhc-ns
  name: claim-pvc
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 60Gi

  # 告诉PVC 要绑定到哪个StorageClass
  storageClassName: rook-ceph-block

```

- - - - - -

##### **[从私有仓库拉取镜像](https://kubernetes.io/zh-cn/docs/tasks/configure-pod-container/pull-image-private-registry/#create-a-secret-by-providing-credentials-on-the-command-line)**

> 在命令行上提供凭据来创建 Secret  
>  创建 Secret，命名为 private-library：
> 
> ```bash
> kubectl -n nocalhost-ns create secret docker-registry private-library \
>   --docker-server= \
>   --docker-username= \
>   --docker-password=
> 
> ```
> 
> ```bash
> kubectl -n nocalhost-ns create secret docker-registry private-library \
>   --docker-server=192.168.101.23 \
>   --docker-username=admin \
>   --docker-password=Harbor12345
> 
> 
> ```
> 
> ###### 查看yaml
> 
> ```bash
> kubectl -n nocalhost-ns get secret private-library --output=yaml
> 
> apiVersion: v1
> data:
>   .dockerconfigjson: eyJhdXRocyI6eyIxOTIuMTY4LjEwMS4yMyI6eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiJIYXJib3IxMjM0NSIsImF1dGgiOiJZV1J0YVc0NlNHRnlZbTl5TVRJek5EVT0ifX19
> kind: Secret
> metadata:
>   creationTimestamp: "2023-08-03T01:02:26Z"
>   name: private-library
>   namespace: nocalhost-ns
>   resourceVersion: "28153418"
>   uid: c9834189-8abc-4cce-9e5e-069585a16ab0
> type: kubernetes.io/dockerconfigjson
> 
> 
> ```
> 
> ###### 解密查看
> 
> ```bash
> kubectl -n nocalhost-ns get secret private-library --output="jsonpath={.data.\.dockerconfigjson}" | base64 --decode
> 
> {"auths":{"192.168.101.23":{"username":"admin","password":"Harbor12345","auth":"YWRtaW46SGFyYm9yMTIzNDU="}}}
> 
> ```

- - - - - -

##### **ServiceAccount**

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  namespace: '{{ .Release.Namespace }}'
  name: {{ .Release.Name }}
# (可选) 将镜像拉取 Secret 添加到服务账号
imagePullSecrets:
  - name: private-library


```

- - - - - -

##### **Deployment**

```yaml
---
# 创建要部署的容器
# 种类：告诉 k8s 下面这些配置的含义(常用的包括：Namespace, Deployment, Service)
kind: Deployment
# 版本号 规定格式 apps/* 必须这么写
apiVersion: apps/v1
metadata:
  # Deployment 的所属的命名空间，不可以使用 下划线
  namespace: dhc-ns
  # Deployment 名称
  name: <span class="katex math inline">{CI_PROJECT_NAME}
  labels:
    # 给Deployment打个标签。
    app:</span>{CI_PROJECT_NAME}
    # 给Deployment打个标签。
    version: v1

spec:
  # 告诉 K8s 启动几个Pod
  replicas: 1
  # 当新的pod启动 5s后，再kill掉旧的pod
  minReadySeconds: 5
  # 通过标签告诉Deployment， 管理的是哪个Pod
  selector:
    matchLabels:
      # 选择下面模板中, Pod 的label名
      app: <span class="katex math inline">{CI_PROJECT_NAME}
      version: v1

  # 定义 Pod模板
  template:
    metadata:
      # Pod模板的标签
      labels:
        # Pod的label
        app:</span>{CI_PROJECT_NAME}
        version: v1
      # 配置 ConfigMap 触发热更新
      #   如果使用ConfigMap的subPath挂载为Container的Volume，Kubernetes不会对Pod做自动热更新
      #   可以通过修改ConfigMap的 pod的 annotations的方式强制触发滚动更新
      annotations:
        # 随意写个注解，需要滚动更新pod时，改一下注解的值即可
        eric.mao: "<span class="katex math inline">{CI_JOB_ID}"

    spec:
      # 可以定义优雅退出的宽限期，即在收到停止请求后，有多少时间来进行资源释放或者做其它操作，
      # 如果到了最大时间还没有停止，会被强制结束，默认值：30
      terminationGracePeriodSeconds: 60
      # 告诉 k8s 根据设置的节点名称，将这个pod部署到哪个节点机器上（默认不指定，k8s会自动分配）;
      # 因为 nodeName(节点的名称不可以重复，因此使用nodeName只能指定一台节点服务)
      # nodeName: k8s-node1
      # 告诉 k8s 根据设置的节点标签，将这个pod部署到哪个节点机器上（默认不指定，k8s会自动分配）;
      # 因为 nodeLabels(节点的标签可以重复，因此使用nodeSelector是可以指定同一个标签的多个节点服务)
      # nodeSelector:
      #   app: "label"


      volumes:
          # 挂载空目录，适用于没有持久卷的场景
        - name: app-empty
          emptyDir: {}

          # 为这个挂载起个名
        - name: app-pvc
          # 指定PVC
          persistentVolumeClaim:
            claimName: claim-pvc

          # 为这个引入起个名
        - name: config-volume
          configMap:
            # 告诉k8s，引入哪个ConfigMap
            name:</span>{CI_PROJECT_NAME}

          # 让容器时间与主机操作系统时间同步
        - name: etc-localtime
          # 映射到主机
          hostPath:
            path: /etc/localtime

      # 在Pod模板中的，容器重启策略( Always、OnFailure 和 Never )
      # 在Deployment模板中的，容器重启策略( 只能是 Always )
      restartPolicy: Always

      # (可选) 将镜像拉取 Secret 添加到 Pod
      # 创建新 Pod 并使用 ServiceAccount 时， 新 Pod 的 spec.imagePullSecrets 会被自动设置。
      imagePullSecrets:
        - name: private-library

      # (可选) 使用 ServiceAccount 时
      serviceAccountName: '{{ .Release.Name }}'

      # 配置容器
      containers:
        # 容器名
        - name: <span class="katex math inline">{CI_PROJECT_NAME}
          # 告诉 K8s 要部署的镜像名:Tag
          image: 192.168.20.93/library/</span>{CI_PROJECT_NAME}:${CI_COMMIT_TAG}
          ## 配置后， 将以root用户权限进入容器
          securityContext:
            runAsUser: 0
          # 告诉 K8s 如果本地没有这个镜像
          # 总是拉取 pull
          imagePullPolicy: Always
          # 只使用本地镜像，从不拉取
          # imagePullPolicy: Never
          # 默认值,本地有则使用本地镜像,不拉取
          # imagePullPolicy: IfNotPresent
          # 告诉 K8s 容器对外开放几个端口
          ports:
            - containerPort: 8066
              protocol: TCP

          # 应用资源限制
          # 1. 如果 Pod 运行所在的节点具有足够的可用资源，容器可能（且可以）使用超出对应资源 request 属性所设置的资源量
          #   1.1 例如，如果你将容器的 memory 的请求量设置为 256 MiB，而该容器所处的 Pod 被调度到一个具有 8 GiB 内存的节点上，并且该节点上没有其他 Pods 运行，那么该容器就可以尝试使用更多的内存。
          # 2. 不过，容器不可以使用超出其资源 limit 属性所设置的资源量。
          #   2.1 如果你将某容器的 memory 约束设置为 4 GiB，kubelet （和 容器运行时） 就会确保该约束生效。 容器运行时会禁止容器使用超出所设置资源约束的资源。
          #   2.2 例如，当容器中进程尝试使用超出所允许内存量的资源时，系统内核会将尝试申请内存的进程终止，并引发内存不足（OOMKilled）错误。
          # 具体参考官网: https://kubernetes.io/zh-cn/docs/concepts/configuration/manage-resources-containers/#requests-and-limits
          resources:
            # 你可以认为该 Pod 的资源请求为 0.5 CPU 和 256 MiB 内存
            requests:
              memory: "256MiB"
              cpu: "500m"
            # 你可以认为该 Pod 的资源限制为 1 CPU 和 4 Gi 内存。
            limits:
              # 如果容器中进程尝试使用的内存超出限制， 将会引发 OOMKilled 错误，并重启 Pod。
              memory: "4Gi"
              # 限制该应用中无论有多少个进程，都只能使用1个CPU的资源量
              cpu: "1000m"

          # 自定义系统环境变量
          env:
              # 改变程序获取的时间，这与容器内的系统时间无关
            - name: TZ
              value: 'Asia/Shanghai'

          # 告诉容器中的应用程序，使用哪个配置文件
          volumeMounts:
              # 使用 空目录
            - name: app-empty
              mountPath: /var/lib/mysql

              # 使用 PVC
            - name: app-pvc
              mountPath: /var/www/html

              # 使用 ConfigMap
            - name: config-volume
              # 此处含义为： 告诉k8s，将ConfigMap中的配置文件，放在当前容器中的哪个目录下。
              #### 此处含义为将文件放到前容器中的/app目录下
              mountPath: /app

              # 使用 宿主机文件
              # 让容器时间与主机操作系统时间同步
            - name: etc-localtime
              mountPath: /etc/localtime

```

- - - - - -

#### **对于`subPath`和`mountPath`**的理解

> - **mountPath（挂载路径）**
>   - 是指`在容器内部`将卷挂载到`文件系统`的路径。
>   - 它表示`容器内部`的`目录`或`文件`路径，用于`访问挂载的卷数据`。
> - **subPath（子路径）**
>   - 是指将`卷`的`一部分内容`挂载到`容器内部`的`路径`。
>   - 它允许在`容器中`指定`挂载`路径的`子路径`，以限制对卷的访问范围。
>   - 通常，`subPath` 与 `mountPath` 结合使用，以指定`卷挂载的位置`和在`该位置上的子路径`。
> 
>  例如，假设有一个名为 `/data` 的持久卷，其中包含**文件 `/data/file.txt`** 和**目录 `/data/subdir`**。  
>  在容器的定义中，可以将该卷挂载到 `/mnt` 目录，并使用 `subPath` 指定子路径。
> 
> ```yaml
> volumes:
>   - name: data-volume
>     persistentVolumeClaim:
>       claimName: claim-pvc
> 
> containers:
>   # 容器名
>   - name: <span class="katex math inline">{CI_PROJECT_NAME}
>     # 告诉 K8s 要部署的镜像名:Tag
>     image: 192.168.20.93/library/</span>{CI_PROJECT_NAME}:${CI_COMMIT_TAG}
>     volumeMounts:
>       - name: data-volume
>         mountPath: /mnt
>         subPath: subdir
> 
> ```
> 
>  在上述示例中，`mountPath` 设置为 `/mnt`，表示将持久卷挂载到容器内的 `/mnt` 路径。  
>  而 `subPath` 设置为 `subdir`，表示只挂载 `/data/subdir` 子路径下的内容，容器内部`只能访问`该`子路径`下的文件和目录，而`无法访问` `/data/file.txt` 或其他 **`/data/subdir` 之外** 的内容。
> 
>  通过使用 `subPath`，可以将卷的特定部分挂载到容器内，以满足特定的应用程序需求或限制容器对卷的访问权限。

- - - - - -

- - - - - -

- - - - - -

###### **Service**

```yaml
---
# 为部署的容器开放端口
# Service
kind: Service
apiVersion: v1
metadata:
  # 所属的命名空间
  namespace: dhc-ns
  # Service 名称
  name: dhc-service-name
  # Service 标签
  labels:
    app: service-label

# 容器的详细定义
spec:
  # 告诉 K8s Docker容器对外开放几个端口
  # 如果指定为 NodePort 则这个service的端口可以被外界访问
  type: NodePort
  ports:
    - name: http
      protocol: TCP
      # port 是service的端口
      port: 80
      # targetPort 是pod的端口
      targetPort: 8066
      # 可以被外网访问的端口
      nodePort: 30808

  # 选择 Pod的label
  selector:
    # Pod的label
    app: ${CI_PROJECT_NAME}

```

- - - - - -

- - - - - -

- - - - - -

###### **[HPA](https://kubernetes.io/zh-cn/docs/tasks/run-application/horizontal-pod-autoscale/ "HPA")**

```yaml
apiVersion: autoscaling/v2beta2
kind: HorizontalPodAutoscaler
metadata:
  name: pressure-test
spec:
  # 告诉k8s你要指定的缩放目标是谁
  scaleTargetRef:
    apiVersion: apps/v1
    # 缩放目标是名为container-pressure-test的Deployment
    kind: Deployment
    # 比较要有一个已经存在的缩放目标
    name: container-pressure-test

  # 至少1个pod
  minReplicas: 1
  # 最多不超过3个pod
  maxReplicas: 3
  # 根据监控指标执行动态扩缩容
  metrics:
  - type: Resource
    resource:
      # 针对CPU的监控
      name: cpu
#      # 按利用率(百分比)
#      target:
#        type: Utilization
#        averageUtilization: 50
      # 按数值
      target:
        type: AverageValue
        averageValue: 3m
#  - type: Resource
#    resource:
#      # 针对内存的监控
#      name: memory
#      # 按资源使用率(百分比)
#      target:
#        type: Utilization
#        # HPA控制器会维持扩缩目标中的 Pods 的平均资源利用率在 70%
#        # 这个值的百分比，取的是 Pod的资源请求阈值，所设定的值。就是如下这两个值，对应的百分比
#        # Pod的 .containers.resources.requests.memory
#        # Pod的 .containers.resources.requests.cpu
#        averageUtilization: 70


```

- - - - - -

- - - - - -

- - - - - -

###### **[Job](https://kubernetes.io/zh/docs/concepts/workloads/controllers/job/ "Job")**

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: job-mq-consumer
spec:
  # 可容忍的失败次数。
  # 在任务失败时尝试进行重试（当整个节点出现异常时，K8S 可以将容器调度到其他节点上重试执行，拥有更好的容错能力），而这个字段可以理解为重试的次数
  backoffLimit: 4
  # 并行的数量。
  #   如果你的批处理任务需要并发能力，那么 K8S 会按照这个字段的数字同时启动多个容器来并发的执行。
  # 告诉k8s，job启动时，默认启动几个Pod，多个Pod同时工作。（注意：如果pod中有http服务启动，那么有可能会变成同时只有一个pod在工作）
  parallelism: 2
  # 任务成功执行 N 次后结束任务。
  #   这个参数设定为 8 代表当重复运行了 8 次后就结束本次的批处理任务。
  # Job 用来代表整个任务，当成功的 Pod 个数达到 .spec.completions 时，Job 被视为完成。
  completions: 8
  template:
    metadata:
      name: job-mq-consumer
    spec:
      # OnFailure: 只在容器 异常时才自动重启容器
      # Never: 不重启容器
      restartPolicy: OnFailure
      containers:
      - image: 172.16.15.183/tools/iris-server-mq-consumer:0.1.0
        name: iris-server-mq-consumer
        ports:
        - containerPort: 8080
        env:
        # 配置链接地址
        - name: MQ_USER
          value: 'mao_siyu'
        - name: MQ_PASSWORD
          value: '******'
        - name: MQ_HOST
          value: 'rabbitmq-rabbitmq-ha.rabbitmq-cluster'
        - name: MQ_PORT
          value: '15672'
        - name: MQ_VHOST
          value: 'eric_vhost'


```

- - - - - -

##### Job的用法

```shell
cat > app-job.yaml 
```

- - - - - -

- - - - - -

- - - - - -