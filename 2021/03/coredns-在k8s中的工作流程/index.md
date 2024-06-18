---
title: "CoreDNS 在k8s中的工作流程"
date: "2021-03-10"
categories: 
  - "k8s"
---

###### 要先了解k8s中使用的 **[CoreDNS](https://www.cnblogs.com/sandshell/p/12581309.html "CoreDNS")**

* * *

1. 创建pod
2. 根据pod创建svc
3. svc与所有pod的ip进行绑定
4. 将svc名称与svc对应的ClusterIP写入到CoreDNS中
5. 外部访问时，先访问**IngressController**，在转发到对应的svc，在由svc负载到pod里面的应用
6. pod内部向外部请求域名时，先找CoreDNS，查询到解析的地址后，通过网络插件找docker0虚拟网卡，docker0找主机(ens0, eth192)
