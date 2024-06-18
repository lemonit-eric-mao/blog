---
title: K8S部署Flink-Kubernetes-Operator
date: '2022-12-13T12:39:55+00:00'
status: private
permalink: /2022/12/13/k8s%e9%83%a8%e7%bd%b2flink-kubernetes-operator
author: 毛巳煜
excerpt: ''
type: post
id: 9552
category:
    - Flink
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
K8S部署Flink-Kubernetes-Operator
==============================

> - [Apache Flink Kubernetes Operator Github](https://github.com/apache/flink-kubernetes-operator)
> - [Flink-Kubernetes-Operator 官网](https://nightlies.apache.org/flink/flink-kubernetes-operator-docs-main/#flink-kubernetes-operator)

![flink-k8s-01.png](http://qiniu.dev-share.top/image/flink-k8s-01.png)

快速开始
----

> **资料**：在k8s中安装 [Apache Flink Kubernetes Operator Quick Start](https://nightlies.apache.org/flink/flink-kubernetes-operator-docs-main/docs/try-flink-kubernetes-operator/quick-start/)

1. 在 Kubernetes 集群上安装证书管理器以启用添加 webhook 组件（每个 Kubernetes 集群只需要一次）： [cert-manager.yaml](http://qiniu.dev-share.top/file/cert-manager.yaml)

- ```bash
  kubectl apply -f cert-manager.yaml
  
  ```

2. 使用 helm 部署

- ```shell
  export FLINK_VERSION_OPERATOR=1.3.0
  
  helm repo add flink-operator-repo https://downloads.apache.org/flink/flink-kubernetes-operator-<span class="katex math inline">FLINK_VERSION_OPERATOR
  
  helm repo update
  
  ## 将Chart包下载到本地
  helm pull flink-operator-repo/flink-kubernetes-operator --version</span>FLINK_VERSION_OPERATOR
  
  
  ```

3. 创建命名空间

- ```shell
  export FLINK_NAMESPACE=flink
  kubectl create ns $FLINK_NAMESPACE
  
  ```

4. 编写values.yaml

- ```shell
  cat > values.yaml 
  ```

5. 安装部署

- ```shell
  helm install flink-k8s-operator ./flink-kubernetes-operator-<span class="katex math inline">FLINK_VERSION-helm.tgz -f values.yaml -n</span>FLINK_NAMESPACE
  
  ## 安装成功，会出现如下提示
  NAME: flink-k8s-operator
  LAST DEPLOYED: Sat Dec 17 10:11:15 2022
  NAMESPACE: flink
  STATUS: deployed
  REVISION: 1
  TEST SUITE: None
  
  
  ```
- 卸载
  
  ```shell
  helm uninstall flink-k8s-operator -n <span class="katex math inline">FLINK_NAMESPACE
  # 不删除命名空间，会有些依赖删不干净
  kubectl delete ns</span>FLINK_NAMESPACE
  # 要删除证书管理器，否则重装以后，再启动程序，会出现证书错误
  kubectl delete -f cert-manager.yaml
  
  
  ```

### 测试

- 编写测试文件 ```yaml
  cat > basic.yaml 
  ```

部署你的应用程序
--------

> - **[官方模板](https://github.com/apache/flink-kubernetes-operator/tree/main/examples)**
> - **[官方文档](https://nightlies.apache.org/flink/flink-kubernetes-operator-docs-main/docs/custom-resource/overview/)**

### 【应用模式-部署】

#### 构建镜像

**官方参考资料**

> - **部署模式 [\#](https://nightlies.apache.org/flink/flink-docs-release-1.16/docs/deployment/resource-providers/native_kubernetes/#deployment-modes)**
>   - [对于生产使用，我们建议在应用程序模式下](https://nightlies.apache.org/flink/flink-docs-release-1.16/docs/deployment/overview/#application-mode)部署 Flink 应用程序，因为这些模式为应用程序提供了更好的隔离。
>   - [应用模式](https://nightlies.apache.org/flink/flink-docs-release-1.16/docs/deployment/overview/#application-mode)要求用户代码与 Flink 镜像捆绑在一起，因为它在集群上运行用户代码的方法`main()`。Application Mode 确保在应用程序终止后所有 Flink 组件都被正确清理。
> - Flink 社区提供了一个[基础 Docker 镜像](https://nightlies.apache.org/flink/flink-docs-release-1.16/docs/deployment/resource-providers/standalone/docker/#docker-hub-flink-images)，可用于捆绑用户代码：
>   
>   ```dockerfile
>   FROM flink
>   RUN mkdir -p <span class="katex math inline">FLINK_HOME/usrlib
>   COPY /path/of/my-flink-job.jar</span>FLINK_HOME/usrlib/my-flink-job.jar
>   
>   ```

##### 编写Dockerfile文件

1. ```shell
  cat > Dockerfile 
  ```
2. ```shell
  [root@centos01 build-image]# ll
  Dockerfile
  flink-connector-oracle-cdc-2.3.0.jar
  test-flink-cdc-jar-with-dependencies.jar.jar
  
  
  ## 构建你的镜像
  [root@centos01 build-image]# docker build -t test-flink-cdc:1.16 .
  
  ## 查看结果
  [root@centos01 build-image]# docker images test-flink-cdc
  REPOSITORY       TAG       IMAGE ID       CREATED          SIZE
  test-flink-cdc   1.16      b90b47946048   27 seconds ago   831MB
  
  
  ```
3. 将镜像上传到私服仓库 ```shell
  docker tag test-flink-cdc:1.16 192.168.101.23/library/test-flink-cdc:1.16
  
  docker push 192.168.101.23/library/test-flink-cdc:1.16
  
  
  ```

#### 编写k8s部署文件

1. ```shell
  cat > test-flink-cdc.yaml 
  ```
2. 开放Web页面访问 ```shell
  kubectl -n $FLINK_NAMESPACE port-forward svc/test-flink-cdc-rest --address 192.168.101.11  8081:8081
  ## 输出访问地址
  Forwarding from 192.168.101.11:8081 -> 8081
  
  
  ```

- 查看页面 ![flink-k8s-02](http://qiniu.dev-share.top/image/flink-k8s-02.png)
- 查看 Svc
  
  ![flink-k8s-0](http://qiniu.dev-share.top/image/flink-k8s-03.png)
- 查看 Pod
  
  ![flink-k8s-04](http://qiniu.dev-share.top/image/flink-k8s-04.png)

3. 总结
  
  > - 根据实际情况看来，在k8s中创建的应用模式指的是，**一个应用创建一套Flink**，是由 **Flink-Operator** 自动管理的
  > - 这种模式(【**应用模式**】)，它只**能实现高可用**，但是**不能实现分布式负载均衡**

### 【会话模式-部署】

#### 编写k8s部署文件

1. ```yaml
  cat > session-job.yaml 
  ```
2. 开放Web页面访问 ```shell
  kubectl -n $FLINK_NAMESPACE port-forward svc/session-deployment-flink-cdc-rest --address 192.168.101.11  8081:8081
  ## 输出访问地址
  Forwarding from 192.168.101.11:8081 -> 8081
  
  
  ```
3. 查看页面 ![flink-k8s-05](http://qiniu.dev-share.top/image/flink-k8s-05.png)
  
  ![flink-k8s-06](http://qiniu.dev-share.top/image/flink-k8s-06.png)
  
  ![flink-k8s-07](http://qiniu.dev-share.top/image/flink-k8s-07.png)
  
  > **与应用模式的区别**:
  > 
  > 
  > - 页面可以手动提交Jar文件了
  > - 提交的任务共享同一个Flink资源

常见问题
----

**JobManagers 的高可用，需要依赖K8s的高可用**

> - `Error from server: error when creating "basic.yaml": admission webhook "flinkoperator.flink.apache.org" denied the request: Kubernetes High availability should be enabled when starting standby JobManagers.`
> - 服务器错误：创建“basic.yaml”时出错：admission-webhook“flinkoperator.flink.apache.org”拒绝了请求：启动备用JobManagers时应启用Kubernetes高可用性。

**One or more fetchers have encountered exception**

> **异常信息**
> 
> ```
> org.apache.flink.runtime.JobException: Recovery is suppressed by NoRestartBackoffTimeStrategy
> 
>     ...
> 
> Caused by: java.lang.RuntimeException: One or more fetchers have encountered exception
> 
>     ...
> 
> Caused by: java.lang.RuntimeException: SplitFetcher thread 0 received unexpected exception while polling the records
> 
>     ...
> 
> Caused by: org.apache.kafka.connect.errors.RetriableException: An exception occurred in the change event producer. This  
> 
>     ...
> 
> Caused by: java.sql.SQLRecoverableException: No more data to read from socket
> 
>   ...
> 
> 
> ```
> 
>  **解决方法**
> 
>  **需要在代码中指定重启策略**
> 
> ```java
> // 指定重启策略
> // 不重启：
> // env.setRestartStrategy(RestartStrategies.noRestart());
> // 每隔10秒，尝试重启3次
> env.setRestartStrategy(RestartStrategies.fixedDelayRestart(3, Time.of(10, TimeUnit.SECONDS)));
> 
> ```

注意事项
----

### 部署模式详解

> - Flink 可以通过以下三种方式之一执行应用程序： 
>   - 在应用程序模式下，
>   - 在会话模式下，
>   - 在 Per-Job 模式下（已弃用）。
> - 上述模式的区别在于： 
>   - 集群生命周期和资源隔离保证
>   - 应用程序的`main()`方法是在客户端还是在集群上执行。
>   
>    ![flink-k8s-08](http://qiniu.dev-share.top/image/flink-k8s-08.png)
> - 【**[应用程序模式](https://nightlies.apache.org/flink/flink-docs-release-1.16/docs/deployment/overview/#application-mode)**】假定用户 jar 与 Flink 分发包捆绑在一起。
>   
>   
>   - 在集群上执行该`main()`方法可能会对您的代码产生其他影响，例如您在环境中注册的任何路径都`registerCachedFile()`必须可以由应用程序的 JobManager 访问。
>   - 应用程序模式允许多`execute()`应用程序，但在这些情况下不支持高可用性。
>   - 应用程序模式下的高可用性仅支持单个`execute()`应用程序。
>   - 此外，当应用程序模式下的多个正在运行的作业（例如使用 提交 `executeAsync()`）中的任何一个被取消时，所有作业都将停止并且 JobManager 将关闭。支持定期完成作业（通过关闭源）。
> - \[**[会话模式](https://nightlies.apache.org/flink/flink-docs-release-1.16/docs/deployment/overview/#session-mode)**】假定**一个已经在运行的集群**，并使用该集群的资源来执行，**任何提交的应用程序**。 
>   - 在同一（会话）集群中执行的应用程序使用并因此竞争相同的资源。
>   - 这样做的好处是您无需为每个提交的作业支付启动完整集群的资源开销。
>   - 但是，如果其中一个作业行为不当或导致 TaskManager 崩溃，则在该 TaskManager 上运行的所有作业都将受到故障的影响。
>   - 这除了对导致失败的作业产生负面影响外，还意味着一个潜在的大规模恢复过程，所有重新启动的作业同时访问文件系统并使其对其他服务不可用。
>   - 此外，让一个集群运行多个作业意味着 JobManager 有更多的负载，

### upgradeMode详解

> - upgradeMode 支持的值：`stateless`, `savepoint`,`last-state`
> - 该`upgradeMode`设置控制停止和恢复机制，如下表所述：
> - [官网地址](https://nightlies.apache.org/flink/flink-kubernetes-operator-docs-release-1.3/docs/custom-resource/job-management/#stateful-and-stateless-application-upgrades)

<table><thead><tr><th></th><th>**Stateless**</th><th>**Last State**</th><th>**Savepoint**</th></tr></thead><tbody><tr><td>配置要求</td><td>无</td><td>启用检查点（Checkpoint）和kubernetes的高可用（HA）</td><td>定义了checkpoint/savepoint目录</td></tr><tr><td>job 状态要求</td><td>无</td><td>具有可用的 HA 元数据（HA metadata）</td><td>job正在运行</td></tr><tr><td>暂停机制</td><td>取消/删除</td><td>删除 Flink 部署(保留 HA metadata)</td><td>取消并保存到savepoint</td></tr><tr><td>恢复机制</td><td>从空状态部署</td><td>使用 HA metadata 恢复最后的状态</td><td>从savepoint恢复</td></tr><tr><td>用于生产环境</td><td>不推荐</td><td>推荐</td><td>推荐</td></tr></tbody></table>

> - 启用 **Kubernetes HA** 后，`savepoint`升级模式可能会回退到`last-state`作业处于不健康状态时的行为。
> - 三种升级模式旨在支持不同的场景：
> - 1. **stateless**：
>   
>   
>   - 无状态应用程序从空状态升级 
>       2. **last-state**：
>   - 在任何应用程序状态下快速升级（即使是失败的作业），不需要健康的作业，因为它始终使用最新的检查点信息。
>   - 如果 HA 元数据丢失，可能需要手动恢复。 
>       3. **保存点**：
>   - 使用保存点进行升级，提供最大的安全性和作为备份/分叉点的可能性。
>   - 保存点将在升级过程中创建。请注意，Flink 作业需要运行才能创建保存点。
>   - 如果作业处于不健康状态，将使用最后一个检查点（除非`kubernetes.operator.job.upgrade.last-state-fallback.enabled`设置为`false`）。
>   - 如果最后一个检查点不可用，则作业升级将失败。