---
title: 'Mybatis 传参 List 集合'
date: '2017-11-16T13:06:50+00:00'
status: publish
permalink: /2017/11/16/mybatis-%e4%bc%a0%e5%8f%82-list-%e9%9b%86%e5%90%88
author: 毛巳煜
excerpt: ''
type: post
id: 252
category:
    - MyBatis
tag: []
post_format: []
---
#### java 代码

```
<pre class="line-numbers prism-highlight" data-start="1">```java
/**
 * 插入-批量添加上传文件信息
 */
int insertBatchSelective(List<p2pguaranteecertifymaterial> cmlList);
</p2pguaranteecertifymaterial>
```
```

#### 对应的XML

```
<pre class="line-numbers prism-highlight" data-start="1">```sql

<insert id="insertBatchSelective" parametertype="java.util.List">
    insert into p2p_td_guarantee_certify_material
    (
        ID
      , C_GUARANTEE_ID
      , C_NAME
      , C_FILE_IDENTIFY
      , C_FILE_NAME
      , C_ORDER
      , C_CREATE_TIME
      , C_UPDATE_TIME
    )
    values
    <foreach collection="list" index="index" item="item" separator=",">
        (
             #{item.id}
           , #{item.cGuaranteeId}
           , #{item.cName}
           , #{item.cFileIdentify}
           , #{item.cFileName}
           , #{item.cOrder}
           , #{item.cCreateTime}
           , #{item.cUpdateTime}
        )
    </foreach>
</insert>

```
```