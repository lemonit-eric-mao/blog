---
title: "Mytabis 求和函数 null 转 0"
date: "2018-09-12"
categories: 
  - "mybatis"
---

#### 示例

```markup
<!--查询规模-->
    <select id="selectScale" parameterType="java.lang.String" resultType="double">
        SELECT
            COALESCE ( SUM( scale ), 0 )
        FROM
            bq_fund_achievement
        WHERE
            sale_time  LIKE CONCAT(#{date},'%');
    </select>

    <!--范围查询规模-->
    <select id="selectRangeScale" parameterType="java.util.Map" resultType="double">
        SELECT
            COALESCE ( SUM( scale ), 0 )
        FROM
            bq_fund_achievement
        WHERE
            sale_time  BETWEEN #{startDate} AND #{endDate};
    </select>

```
