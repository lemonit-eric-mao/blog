---
title: 'Mybatis 使用 foreach 做批量更新 写法'
date: '2017-11-16T13:07:24+00:00'
status: publish
permalink: /2017/11/16/mybatis-%e4%bd%bf%e7%94%a8-foreach-%e5%81%9a%e6%89%b9%e9%87%8f%e6%9b%b4%e6%96%b0-%e5%86%99%e6%b3%95
author: 毛巳煜
excerpt: ''
type: post
id: 257
category:
    - MyBatis
tag: []
post_format: []
---
```
<pre class="line-numbers prism-highlight" data-start="1">```sql

<update flushcache="true" id="deleteMember" parametertype="GroupMemberDTO">
    UPDATE GROUP_MEMBER
    <set>
        DEL_FLAG = 1
    </set>
    WHERE GROUP_ID = #{groupId}
        AND DEL_FLAG = 0
        AND USER_ID IN
    
    <foreach close=")" collection="userIdArray" item="userId" open="(" separator=",">
        #{userId}
    </foreach>
</update>

```
```