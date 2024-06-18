---
title: 'Helm 安装/使用'
date: '2020-07-16T00:59:44+00:00'
status: publish
permalink: /2020/07/16/helm-%e5%ae%89%e8%a3%85-%e4%bd%bf%e7%94%a8
author: 毛巳煜
excerpt: ''
type: post
id: 5368
category:
    - helm
    - Kubernetes
    - 运维
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
学习Helm的使用
=========

前置资料
----

- **[Helm 官方Github](https://github.com/helm/helm "Helm 官方Github")**
- **[Helm3 推送文件到 Harbor仓库](http://www.dev-share.top/2020/09/14/helm3-%e6%8e%a8%e9%80%81%e6%96%87%e4%bb%b6%e5%88%b0-harbor%e4%bb%93%e5%ba%93/ "Helm3 推送文件到 Harbor仓库")**
- **[自定义 helm chart包](http://www.dev-share.top/2021/06/11/%e8%87%aa%e5%ae%9a%e4%b9%89-helm-chart%e5%8c%85/ "自定义 helm chart包")**

仓库安装/管理
-------

### 下载Helm安装包

- ```shell
  # 官网下载慢
  # wget https://get.helm.sh/helm-v3.10.3-linux-amd64.tar.gz
  [root@k8s-master ~]# wget http://qiniu.dev-share.top/helm-v3.10.3-linux-amd64.tar.gz
  
  [root@k8s-master ~]# tar -zxvf helm-v3.10.3-linux-amd64.tar.gz && cp linux-amd64/helm /usr/local/bin
  
  
  ```
- ```shell
  # 查看helm client版本
  [root@k8s-master ~]# helm version
  version.BuildInfo{Version:"v3.10.3", GitCommit:"835b7334cfe2e5e27870ab3ed4135f136eecc704", GitTreeState:"clean", GoVersion:"go1.18.9"}
  
  
  ```

### 添加/移除仓库地址

- **helm repo add `给仓库起个名` `仓库地址`**
  - ```shell
      ## 添加bitnami仓库地址
      [root@k8s-master ~]# helm repo add bitnami https://charts.bitnami.com/bitnami
      "bitnami" has been added to your repositories
      
      
      ```
- **helm repo remove `仓库名`**
  - ```shell
      helm repo remove bitnami
      "bitnami" has been removed from your repositories
      
      
      ```

### 查看仓库地址列表

- **helm repo list**
  - ```shell
      ## 查看所有被管理的仓库地址
      [root@k8s-master ~]# helm repo list
      NAME                            URL
      bitnami                         https://charts.bitnami.com/bitnami
      
      
      ```

### 更新仓库

- **helm repo update**
  - ```shell
      ## 更新仓库
      [root@k8s-master ~]# helm repo update
      ...Successfully got an update from the "bitnami" chart repository
      Update Complete. ⎈Happy Helming!⎈
      
      
      ```

### 列出源仓库中，所有程序包

- **helm search repo `仓库名`**
  - ```shell
      ## 查看源仓库中，所有的程序包
      [root@k8s-master ~]# helm search repo bitnami
      NAME                    CHART VERSION   APP VERSION     DESCRIPTION
      bitnami/apache          9.2.9           2.4.54          Apache HTTP Server is an open-source HTTP serve...
      bitnami/cert-manager    0.8.10          1.10.1          cert-manager is a Kubernetes add-on to automate...
      bitnami/grafana         8.2.21          9.3.2           Grafana is an open source metric analytics and ...
      bitnami/kong            8.0.28          3.1.1           Kong is an open source Microservice API gateway...
      bitnami/logstash        5.1.9           8.5.3           Logstash is an open source data processing engi...
      bitnami/mariadb         11.4.2          10.6.11         MariaDB is an open source, community-developed ...
      bitnami/metallb         4.1.13          0.13.7          MetalLB is a load-balancer implementation for b...
      bitnami/mysql           9.4.5           8.0.31          MySQL is a fast, reliable, scalable, and easy t...
      bitnami/nginx           13.2.21         1.23.3          NGINX Open Source is a web server that can be a...
      ## 省略......
      
      
      ```
- **helm search repo `仓库具体名`**
  - ```shell
      ## 查看源仓库中，bitnami/kafka 程序包当前最新版本
      NAME            CHART VERSION   APP VERSION     DESCRIPTION
      bitnami/kafka   20.0.2          3.3.1           Apache Kafka is a distributed streaming platfor...
      
      
      ```
- **helm search repo `仓库具体名` -l**
  - ```shell
      ## 查看源仓库中，所有 bitnami/kafka 程序包的版本
      [root@k8s-master ~]# helm search repo bitnami/kafka -l
      NAME            CHART VERSION   APP VERSION     DESCRIPTION
      bitnami/kafka   20.0.2          3.3.1           Apache Kafka is a distributed streaming platfor...
      bitnami/kafka   19.1.5          3.3.1           Apache Kafka is a distributed streaming platfor...
      bitnami/kafka   18.5.0          3.2.3           Apache Kafka is a distributed streaming platfor...
      bitnami/kafka   17.2.6          3.2.0           Apache Kafka is a distributed streaming platfor...
      ## 省略......
      
      
      ```

使用Helm部署应用程序
------------

### 将压缩包下载到本地

- **helm pull `仓库名` --version `指定Chart版本`**
  - ```shell
      [root@k8s-master ~]# helm pull bitnami/kafka --version 19.1.5
      
      ```

### 两种安装方式

#### **`第一种`** 离线安装

- **helm install `给软件起个名` `指定本地压缩文件` --namespace `相当于在执行时给模板传参`**
  - ```shell
      ## 将压缩包下载到本地
      [root@k8s-master ~]# helm pull bitnami/kafka --version 19.1.5
      
      ## 安装
      [root@k8s-master ~]# helm install kafka-19-1-5 ./kafka-19.1.5.tgz \
      --namespace kafka-ns \
      --set replicaCount=3 \
      --set global.storageClass='rook-ceph-block' \
      --set persistence.storageClass='rook-ceph-block'
      
      
      ```
- 更新配置 
  - **helm upgrade `指定软件名` `指定本地压缩文件` --namespace `指定命名空间`**
      - ```shell
            [root@k8s-master ~]# helm upgrade kafka-19-1-5 ./kafka-19.1.5.tgz --namespace kafka-ns
            
            ```
- 卸载 
  - **helm uninstall `指定软件名` --namespace `指定命名空间`**
      - ```shell
            [root@k8s-master ~]# helm uninstall kafka-19-1-5 --namespace kafka-ns
            
            ```

#### **`第二种`** 提取yaml文件安装

- **helm template `指定软件名` `指定本地压缩包` --namespace `指定命名空间` --set `传入需要的各种参数`**
  - ```shell
      ## 将压缩包下载到本地
      [root@k8s-master ~]# helm pull bitnami/kafka --version 19.1.5
      
      ## 提取
      [root@k8s-master ~]# helm template kafka-19-1-5 ./kafka-19.1.5.tgz --output-dir . \
      --namespace kafka-ns \
      --set replicaCount=3 \
      --set global.storageClass='rook-ceph-block' \
      --set persistence.storageClass='rook-ceph-block'
      
      # 启动执行
      [root@k8s-master ~]# kubectl apply -R -f ./kafka
      
      ```

常用命令
----

- **helm show values `指定仓库具体名`**
  - ```shell
      ## 查看 values.yaml
      [root@k8s-master ~]# helm show values bitnami/kafka
      
      ## 写到本地
      [root@k8s-master ~]# helm show values bitnami/kafka > values.yaml
      
      
      ```