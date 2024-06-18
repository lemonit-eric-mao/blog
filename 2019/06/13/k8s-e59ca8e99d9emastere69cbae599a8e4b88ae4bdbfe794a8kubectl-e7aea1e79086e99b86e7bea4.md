---
title: 'K8s 在非master机器上使用kubectl 管理集群'
date: '2019-06-13T02:03:53+00:00'
status: publish
permalink: /2019/06/13/k8s-%e5%9c%a8%e9%9d%9emaster%e6%9c%ba%e5%99%a8%e4%b8%8a%e4%bd%bf%e7%94%a8kubectl-%e7%ae%a1%e7%90%86%e9%9b%86%e7%be%a4
author: 毛巳煜
excerpt: ''
type: post
id: 4805
category:
    - Kubernetes
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
> 在准备的虚拟机上安装配置kubectl，注意版本需要与k8s版本保持一致

```shell
# 配置k8s的yum源
cat > /etc/yum.repos.d/kubernetes.repo 
```