---
title: "Mybatis 传参 List 集合"
date: "2017-11-16"
categories: 
  - "mybatis"
---

#### java 代码

```java
/**
 * 插入-批量添加上传文件信息
 */
int insertBatchSelective(List<P2pGuaranteeCertifyMaterial> cmlList);
```

#### 对应的XML

```sql
<!-- 批量添加上传文件信息 -->
<insert id="insertBatchSelective" parameterType="java.util.List">
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
    <foreach collection="list" item="item" index="index" separator=",">
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
