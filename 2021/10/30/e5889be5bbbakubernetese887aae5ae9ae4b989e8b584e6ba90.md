---
title: 创建Kubernetes自定义资源
date: '2021-10-30T08:03:31+00:00'
status: private
permalink: /2021/10/30/%e5%88%9b%e5%bb%bakubernetes%e8%87%aa%e5%ae%9a%e4%b9%89%e8%b5%84%e6%ba%90
author: 毛巳煜
excerpt: ''
type: post
id: 8090
category:
    - Kubernetes
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
##### 资料

###### **[使用 CustomResourceDefinition 扩展 Kubernetes API](https://kubernetes.io/zh/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/ "使用 CustomResourceDefinition 扩展 Kubernetes API")**

- - - - - -

###### 自定义CRD

```ruby
cat > custom-resource-definition.yaml .'
  name: maosiyus.cloud.dhc.com
spec:
  # 可以是 Namespaced 或 Cluster
  scope: Namespaced
  # 名称
  names:
    # 名称的复数形式，用于 URL：/apis///
    plural: maosiyus
    # 名称的单数形式，作为命令行使用时和显示时的别名
    singular: maosiyu
    # kind 通常是单数形式的驼峰编码（PascalCased）形式。你的资源清单会使用这一形式。
    kind: Maosiyu
    # shortNames 允许你在命令行使用较短的字符串来匹配资源(就是起个别名)
    shortNames:
      - msy
    # categories 是定制资源所归属的分类资源列表
    categories:
      - all

  # 组名称，用于 REST API: /apis//
  group: cloud.dhc.com

  # 列举此 CustomResourceDefinition 所支持的版本
  versions:
    - name: v1
      # 每个版本都可以通过 served 标志来独立启用或禁止
      served: true
      # 其中一个且只有一个版本必需被标记为存储版本
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          # 自定义属性
          properties:
            spec:
              type: object
              properties:
                showMessage:
                  type: string
                  # nullable默认值为 false
                  # 它表示如果传给showMessage的值是空值, 就会使用default中的值做为填充
                  nullable: false
                  default: "default message!"
                info:
                  # 它表示传给info的值是什么，就保留什么
                  nullable: true
                  type: string
                image:
                  type: string
                replicas:
                  type: integer

      # 添加额外的打印列
      #    列的 type 字段可以是以下值之一 （比较 OpenAPI v3 数据类型）：
      #    integer – 非浮点数字
      #    number – 浮点数字
      #    string – 字符串
      #    boolean – true 或 false
      #    date – 显示为以自此时间戳以来经过的时长
      additionalPrinterColumns:
        - name: Eric-Message
          type: string
          description: ''
          jsonPath: .spec.showMessage
        - name: Eri-cInfo
          type: string
          description: ''
          jsonPath: .spec.info
        - name: Image
          type: string
          jsonPath: .spec.image
        - name: Replicas
          type: integer
          jsonPath: .spec.replicas
        - name: Age
          type: date
          jsonPath: .metadata.creationTimestamp

ERIC


```

- - - - - -

###### 查看CRD

```ruby
[root@master01 ~]# kubectl apply -f custom-resource-definition.yaml
customresourcedefinition.apiextensions.k8s.io/maosiyus.cloud.dhc.com created


[root@master01 ~]# kubectl get -f custom-resource-definition.yaml
NAME                     CREATED AT
maosiyus.cloud.dhc.com   2021-10-30T07:14:34Z


[root@master01 ~]# kubectl get crd maosiyus.cloud.dhc.com
NAME                     CREATED AT
maosiyus.cloud.dhc.com   2021-10-30T07:14:34Z


```

- - - - - -

###### 测试使用CRD

```ruby
kubectl apply -f - 
```

- - - - - -

###### 查看CRD对象

```ruby
[root@master01 crd]# kubectl get msy
NAME                    ERIC-MESSAGE       ERI-CINFO      IMAGE   REPLICAS   AGE
my-new-maosiyu-object   default message!   Hello world!   nginx   1          5s


[root@master01 crd]# kubectl get Maosiyu
NAME                    ERIC-MESSAGE       ERI-CINFO      IMAGE   REPLICAS   AGE
my-new-maosiyu-object   default message!   Hello world!   nginx   1          13s



```

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

###### 定制资源相关思考与如何实际应用

现在知道如何进行自定义CRD了，那么创建后它又有什么作用呢？ 我要如何使用自定义的CRD？

- - - - - -

###### 定制控制器

 就定制资源本身而言，它只能用来存取结构化的数据。 当你将定制资源与 **[定制控制器（Custom Controller）](https://kubernetes.io/zh/docs/concepts/extend-kubernetes/api-extension/custom-resources/#custom-controllers "定制控制器（Custom Controller）")** 相结合时，定制资源就能够 提供真正的 声明式 API（Declarative API）。

- - - - - -

###### **[编写你自己的 Operator](https://kubernetes.io/zh/docs/concepts/extend-kubernetes/operator/#writing-operator "编写你自己的 Operator")**

- - - - - -

- - - - - -

- - - - - -