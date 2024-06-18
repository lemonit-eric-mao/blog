---
title: 使用client-go中的informer机制，实时获取kubernetes信息
date: '2022-04-15T15:51:28+00:00'
status: publish
permalink: /2022/04/15/%e4%bd%bf%e7%94%a8client-go%e4%b8%ad%e7%9a%84informer%e6%9c%ba%e5%88%b6%ef%bc%8c%e5%ae%9e%e6%97%b6%e8%8e%b7%e5%8f%96kubernetes%e4%bf%a1%e6%81%af
author: 毛巳煜
excerpt: ''
type: post
id: 8535
category:
    - Go
    - Kubernetes
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
**[原文地址](https://andblog.cn/3049 "原文地址")**

- - - - - -

- - - - - -

- - - - - -

**[项目地址](https://gitee.com/eric-mao/gin-server "项目地址")**

##### client-go主要模块有：

- client 
  - restclient
  - clientset
  - dynamicclient
  - discoveryclient
- informer 
  - reflactor
  - deltafifo
  - indexer
- workqueue

- - - - - -

- - - - - -

- - - - - -

##### 运行原理

一个控制器每次需要获取对象的时候都要访问 APIServer，这会给系统带来很高的负载，Informers 的内存缓存就是来解决这个问题的，此外 Informers  
还可以几乎实时的监控对象的变化，而不需要轮询请求，这样就可以保证客户端的缓存数据和服务端的数据一致，就可以大大降低 APIServer 的压力了。

- - - - - -

##### informer在开发中的使用

```go
package main

import (
    "flag"
    "fmt"
    "path/filepath"
    "time"

    v1 "k8s.io/api/apps/v1"
    "k8s.io/apimachinery/pkg/labels"
    "k8s.io/client-go/informers"
    "k8s.io/client-go/kubernetes"
    "k8s.io/client-go/rest"
    "k8s.io/client-go/tools/cache"
    "k8s.io/client-go/tools/clientcmd"
    "k8s.io/client-go/util/homedir"
)

func main() {
    var err error
    var config *rest.Config

    var kubeconfig *string

    if home := homedir.HomeDir(); home != "" {
        kubeconfig = flag.String("kubeconfig", filepath.Join(home, ".kube", "config"), "[可选] kubeconfig 绝对路径")
    } else {
        kubeconfig = flag.String("kubeconfig", "", "kubeconfig 绝对路径")
    }
    // 初始化 rest.Config 对象
    if config, err = rest.InClusterConfig(); err != nil {
        if config, err = clientcmd.BuildConfigFromFlags("", *kubeconfig); err != nil {
            panic(err.Error())
        }
    }
    // 创建 Clientset 对象
    clientset, err := kubernetes.NewForConfig(config)
    if err != nil {
        panic(err.Error())
    }

    // ------------------------------------------------------------------------------------------

    // 初始化 informer factory（为了测试方便这里设置每30s重新 List 一次）
    informerFactory := informers.NewSharedInformerFactory(clientset, time.Second*30)
    // 对 Deployment 监听
    deployInformer := informerFactory.Apps().V1().Deployments()
    // 创建 Informer（相当于注册到工厂中去，这样下面启动的时候就会取 List & Watch 对应的资源）
    informer := deployInformer.Informer()
    // 创建 Lister
    deployLister := deployInformer.Lister()

    // 注册事件处理程序
    informer.AddEventHandler(cache.ResourceEventHandlerFuncs{
        AddFunc: func(obj interface{}) {
            deploy := obj.(*appsv1.Deployment)
            fmt.Println("add a deployment:", deploy.Name)
        },
        UpdateFunc: func(old, new interface{}) {
            oldDeploy := old.(*appsv1.Deployment)
            newDeploy := new.(*appsv1.Deployment)
            fmt.Println("update deployment:", oldDeploy.Name, newDeploy.Name)
        },
        DeleteFunc: func(obj interface{}) {
            deploy := obj.(*appsv1.Deployment)
            fmt.Println("delete a deployment:", deploy.Name)
        },
    })

    stopper := make(chan struct{})
    defer close(stopper)

    // 启动 informer，List & Watch
    informerFactory.Start(stopper)
    // 等待所有启动的 Informer 的缓存被同步
    informerFactory.WaitForCacheSync(stopper)

    // 从本地缓存中获取 default 中的所有 deployment 列表
    deployments, err := deployLister.Deployments("default").List(labels.Everything())
    if err != nil {
        panic(err)
    }
    for idx, deploy := range deployments {
        fmt.Printf("%d -> %s\\n", idx+1, deploy.Name)
    }
    
```

上面的代码运行可以获得 default 命名空间之下的所有 Deployment 信息以及整个集群的 Deployment 数据

- - - - - -

- - - - - -

- - - - - -

##### 也可以单独只使用 Watch

```go
package main

import (
    "flag"
    "fmt"
    "path/filepath"
    "time"

    v1 "k8s.io/api/apps/v1"
    "k8s.io/apimachinery/pkg/labels"
    "k8s.io/client-go/informers"
    "k8s.io/client-go/kubernetes"
    "k8s.io/client-go/rest"
    "k8s.io/client-go/tools/cache"
    "k8s.io/client-go/tools/clientcmd"
    "k8s.io/client-go/util/homedir"
)

func main() {
    var err error
    var config *rest.Config

    var kubeconfig *string

    if home := homedir.HomeDir(); home != "" {
        kubeconfig = flag.String("kubeconfig", filepath.Join(home, ".kube", "config"), "[可选] kubeconfig 绝对路径")
    } else {
        kubeconfig = flag.String("kubeconfig", "", "kubeconfig 绝对路径")
    }
    // 初始化 rest.Config 对象
    if config, err = rest.InClusterConfig(); err != nil {
        if config, err = clientcmd.BuildConfigFromFlags("", *kubeconfig); err != nil {
            panic(err.Error())
        }
    }
    // 创建 Clientset 对象
    clientset, err := kubernetes.NewForConfig(config)
    if err != nil {
        panic(err.Error())
    }

    // ------------------------------------------------------------------------------------------

    // 初始化 informer factory（为了测试方便这里设置每30s重新 List 一次）
    informerFactory := informers.NewSharedInformerFactory(clientset, time.Second*30)
    // 对 Deployment 监听
    deployInformer := informerFactory.Apps().V1().Deployments()
    // 创建 Informer
    informer := deployInformer.Informer()
    // 注册事件处理程序，
    informer.AddEventHandler(cache.ResourceEventHandlerFuncs{
        AddFunc: func(obj interface{}) {
            deploy := obj.(*appsv1.Deployment)
            fmt.Println("add a deployment:", deploy.Name)
        },
        UpdateFunc: func(old, new interface{}) {
            oldDeploy := old.(*appsv1.Deployment)
            newDeploy := new.(*appsv1.Deployment)
            fmt.Println("update deployment:", oldDeploy.Name, newDeploy.Name)
        },
        DeleteFunc: func(obj interface{}) {
            deploy := obj.(*appsv1.Deployment)
            fmt.Println("delete a deployment:", deploy.Name)
        },
    })


    stopper := make(chan struct{})
    defer close(stopper)
    // 启动 informer，List & Watch
    informerFactory.Start(stopper)
    // 等待所有启动的 Informer 的缓存被同步
    informerFactory.WaitForCacheSync(stopper)

    // 阻塞等待停止信号
    
```

- - - - - -

- - - - - -

- - - - - -

##### 也可以单独只使用 **`List`**

```go
package main

import (
    "flag"
    "fmt"
    "path/filepath"
    "time"

    v1 "k8s.io/api/apps/v1"
    "k8s.io/apimachinery/pkg/labels"
    "k8s.io/client-go/informers"
    "k8s.io/client-go/kubernetes"
    "k8s.io/client-go/rest"
    "k8s.io/client-go/tools/cache"
    "k8s.io/client-go/tools/clientcmd"
    "k8s.io/client-go/util/homedir"
)

func main() {
    var err error
    var config *rest.Config

    var kubeconfig *string

    if home := homedir.HomeDir(); home != "" {
        kubeconfig = flag.String("kubeconfig", filepath.Join(home, ".kube", "config"), "[可选] kubeconfig 绝对路径")
    } else {
        kubeconfig = flag.String("kubeconfig", "", "kubeconfig 绝对路径")
    }
    // 初始化 rest.Config 对象
    if config, err = rest.InClusterConfig(); err != nil {
        if config, err = clientcmd.BuildConfigFromFlags("", *kubeconfig); err != nil {
            panic(err.Error())
        }
    }
    // 创建 Clientset 对象
    clientset, err := kubernetes.NewForConfig(config)
    if err != nil {
        panic(err.Error())
    }

    // ------------------------------------------------------------------------------------------

    // 初始化 informer factory（为了测试方便这里设置每30s重新 List 一次）
    informerFactory := informers.NewSharedInformerFactory(clientset, time.Second*30)
    // 对 Deployment 监听
    deployInformer := informerFactory.Apps().V1().Deployments()
    // 创建 Lister
    deployLister := deployInformer.Lister()

    stopper := make(chan struct{})
    defer close(stopper)
    // 启动 informer，List & Watch
    informerFactory.Start(stopper)
    // 等待所有启动的 Informer 的缓存被同步
    informerFactory.WaitForCacheSync(stopper)

    // 从本地缓存中获取所有 deployment 列表
    deployments, err := deployLister.List(labels.Everything())
    if err != nil {
        panic(err)
    }
    for idx, deploy := range deployments {
        fmt.Printf("%d -> %s\\n", idx+1, deploy.Name)
    }
}


```

- - - - - -

- - - - - -

- - - - - -