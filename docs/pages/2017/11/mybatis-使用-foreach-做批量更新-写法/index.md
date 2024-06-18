---
title: "Mybatis 使用 foreach 做批量更新 写法"
date: "2017-11-16"
categories: 
  - "mybatis"
---

```sql
<!-- deleteGroupMember -->
<update id="deleteMember" parameterType="GroupMemberDTO" flushCache="true">
    UPDATE GROUP_MEMBER
    <set>
        DEL_FLAG = 1
    </set>
    WHERE GROUP_ID = #{groupId}
        AND DEL_FLAG = 0
        AND USER_ID IN
    <!-- userIdArray 是 GroupMemberDTO 中的数组类型属性 -->
    <foreach item="userId" collection="userIdArray" open="(" separator="," close=")">
        #{userId}
    </foreach>
</update>
```
