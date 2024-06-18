---
title: 'Mytabis 求和函数 null 转 0'
date: '2018-09-12T13:32:24+00:00'
status: publish
permalink: /2018/09/12/mytabis-%e6%b1%82%e5%92%8c%e5%87%bd%e6%95%b0-null-%e8%bd%ac-0
author: 毛巳煜
excerpt: ''
type: post
id: 2360
category:
    - MyBatis
tag: []
post_format: []
hestia_layout_select:
    - default
---
#### 示例

```
<pre data-language="XML">```markup

    <select id="selectScale" parametertype="java.lang.String" resulttype="double">
        SELECT
            COALESCE ( SUM( scale ), 0 )
        FROM
            bq_fund_achievement
        WHERE
            sale_time  LIKE CONCAT(#{date},'%');
    </select>

    
    <select id="selectRangeScale" parametertype="java.util.Map" resulttype="double">
        SELECT
            COALESCE ( SUM( scale ), 0 )
        FROM
            bq_fund_achievement
        WHERE
            sale_time  BETWEEN #{startDate} AND #{endDate};
    </select>


```
```