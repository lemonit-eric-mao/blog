---
title: "Mytabis foreach 用法 与 适用"
date: "2018-09-12"
categories: 
  - "mybatis"
---

#### mapper 示例

```java
package com.bqhx.data.center.mapper;

import com.bqhx.data.center.entity.BqHuixinAchievement;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * 惠信业绩表 Mapper
 *
 * @author
 * @date 2018-09-11
 */
@Repository
public interface BqHuixinAchievementMapper {

    /**
     * 批量插入基金业绩
     *
     * @param huixinList
     * @return
     */
    int insertHuixinBatch(List<bqhuixinachievement> huixinList);

}
```

#### mapping 示例

```markup
<insert id="insertHuixinBatch" parametertype="java.util.List">
    INSERT INTO
    bq_huixin_achievement (
    bq_product_code,
    bq_product_name,
    sale_time
    ) VALUES
    <foreach collection="list" index="index" item="item" separator=",">
        (
        #{item.bqProductCode},
        #{item.bqProductName},
        #{item.saleTime}
        )
    </foreach>
</insert>
```

`上面的写法没有错, 问题会出在, 如果我现在需要做 从excel中导入 5000条数据到数据库时, 会引发一个异常` **`### Cause: com.mysql.jdbc.PacketTooBigException: Packet for query is too large (14353902 > 4194304).`** `所以上面这种写法, 只适用于数据量较少的情况下, 大概在3000条左右的数据量`
