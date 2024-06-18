---
title: 'Helm 安装 bitnami/mariadb 主从集群模式'
date: '2020-07-23T05:48:58+00:00'
status: publish
permalink: /2020/07/23/helm-%e5%ae%89%e8%a3%85-bitnami-mariadb-%e4%b8%bb%e4%bb%8e%e9%9b%86%e7%be%a4%e6%a8%a1%e5%bc%8f
author: 毛巳煜
excerpt: ''
type: post
id: 5380
category:
    - MySQL
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
##### **[官方地址](https://github.com/bitnami/charts/tree/master/bitnami/mariadb "官方地址")**

##### **[安装 Helm3](http://www.dev-share.top/2020/07/16/helm-%e5%ae%89%e8%a3%85-%e4%bd%bf%e7%94%a8/ "安装 Helm3")**

```ruby
# 添加库
helm repo add bitnami https://charts.bitnami.com/bitnami
helm search repo mariadb
NAME                    CHART VERSION   APP VERSION     DESCRIPTION
bitnami/mariadb         9.3.14          10.5.10         Fast, reliable, scalable, and easy to use open-...
bitnami/mariadb-cluster 1.0.2           10.2.14         DEPRECATED Chart to create a Highly available M...
bitnami/mariadb-galera  5.10.1          10.5.10         MariaDB Galera is a multi-master database clust...
bitnami/phpmyadmin      8.2.7           5.1.1           phpMyAdmin is an mysql administration frontend


# 下载
helm pull bitnami/mariadb --version=9.3.14

# 创建命名空间
kubectl create ns mariadb-ns

# 生成 相关yaml
helm template mariadb ./mariadb-9.3.14.tgz --output-dir . \
    --namespace mariadb-ns \
    --set rootUser.password=1qaz2wsx \
    --set replication.enabled=true \
    --set slave.replicas=1 \
    --set master.persistence.enabled=false \
    --set slave.persistence.enabled=false \
    --set image.debug=true

# 启动
kubectl apply -R -f mariadb/

# 停止
kubectl delete -R -f mariadb/

```

- - - - - -

###### 说明

```ruby
helm template mariadb ./mariadb-9.3.14.tgz --output-dir . \
    --namespace mariadb-ns \
    --set rootUser.password=1qaz2wsx \            # root 密码
    --set replication.enabled=true \              # 启用MariaDB复制
    --set master.persistence.enabled=false \      # 主节点是否使用 PVC 持久化数据，我这里做测试，所以选择关闭
    --set slave.persistence.enabled=false \       # 从节点是否使用 PVC 持久化数据，我这里做测试，所以选择关闭
    --set slave.replicas=1 \                      # 从节点 副本数
    --set image.debug=true                        # 开启 调试日志功能，生产环境，要关闭

```

- - - - - -

##### **[安装客户端](http://www.dev-share.top/2019/08/01/centos-7-%e5%8f%aa%e5%ae%89%e8%a3%85%e5%ae%a2%e6%88%b7%e7%ab%af/ "安装客户端")**

- - - - - -

###### 连接 测试链接

```ruby
mysql -h 任意节点IP -u root -P svc 暴露的端口 -p

```

- - - - - -

- - - - - -

- - - - - -