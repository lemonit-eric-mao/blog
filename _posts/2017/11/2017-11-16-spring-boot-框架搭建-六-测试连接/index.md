---
title: "spring-boot 框架搭建 六 (测试连接)"
date: "2017-11-16"
categories: 
  - "spring-boot"
---

### 测试多数据源

### 添加 com.my.springboot.controller.UsersController.java 文件

```java
package com.my.springboot.controller;

import com.my.springboot.entity.Users;
import com.my.springboot.service.UsersService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
/**
 *  Controller
 */
@RestController
@RequestMapping("/users")
public class UsersController {

    @Autowired
    private UsersService usersServiceImpl;

    /**
     * 新增
     * @param users
     * @return 成功数量
     */
    @ResponseBody
    @RequestMapping(value = "/add", method = RequestMethod.POST)
    public int addUsers(Users users) {

        return usersServiceImpl.addUsers(users);
    }

    /**
     * 删除
     * @param id ID
     * @return 成功数量
     */
    @ResponseBody
    @RequestMapping(value = "/delete", method = RequestMethod.DELETE)
    public int deleteUsersById(String id) {

        return usersServiceImpl.deleteUsersById(id);
    }

    /**
     * 修改
     * @param users
     * @return 成功数量
     */
    @ResponseBody
    @RequestMapping(value = "/modify", method = RequestMethod.PUT)
    public int modifyUsers(Users users) {

        return usersServiceImpl.modifyUsers(users);
    }

    /**
     * 查询
     * @param users
     * @return 集合
     */
    @ResponseBody
    @RequestMapping(value = "/query", method = RequestMethod.GET)
    public List<Users> queryUsers(Users users) {

        return usersServiceImpl.queryUsers(users);
    }

}
```

### 添加 com.my.springboot.service.UsersService.java 接口

```java
package com.my.springboot.service;

import com.my.springboot.entity.Users;

import java.util.List;

/**
 * Service
 */
public interface UsersService {

    /**
     * 新增
     *
     * @param users
     * @return 成功数量
     */
    int addUsers(Users users);

    /**
     * 删除
     *
     * @param id ID
     * @return 成功数量
     */
    int deleteUsersById(String id);

    /**
     * 修改
     *
     * @param users
     * @return 成功数量
     */
    int modifyUsers(Users users);

    /**
     * 查询
     *
     * @param users
     * @return 集合
     */
    List<Users> queryUsers(Users users);

}
```

### 添加 com.my.springboot.service.serviceImpl.UsersServiceImpl.java 文件

```java
package com.my.springboot.service.serviceImpl;

import com.my.springboot.common.dbconfig.MysqlConfig;
import com.my.springboot.entity.Users;
import com.my.springboot.mapper.UsersMapper;
import com.my.springboot.service.UsersService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * ServiceImpl
 */
@Service("usersServiceImpl")
public class UsersServiceImpl implements UsersService {

    @Autowired
    private UsersMapper usersMapper;

    /**
     * 新增
     *
     * @param users
     * @return 成功数量
     */
    public int addUsers(Users users) {

        return usersMapper.insertUsers(users);
    }

    /**
     * 删除
     *
     * @param id ID
     * @return 成功数量
     */
    public int deleteUsersById(String id) {

        return usersMapper.deleteUsersById(id);
    }

    /**
     * 修改
     *
     * @param users
     * @return 成功数量
     */
    public int modifyUsers(Users users) {

        return usersMapper.updateUsers(users);
    }

    /**
     * 查询
     *
     * @param users
     * @return 集合
     */
    public List<Users> queryUsers(Users users) {

        if ("111".equalsIgnoreCase(users.getUId()))
            MysqlConfig.DatabaseContextHolder.setDatabaseType(MysqlConfig.DatabaseType.MASTER);
        else if ("222".equalsIgnoreCase(users.getUId()))
            MysqlConfig.DatabaseContextHolder.setDatabaseType(MysqlConfig.DatabaseType.SLAVE1);

        return usersMapper.selectUsers(users);
    }

}
```

### 添加 com.my.springboot.entity.Users.java 文件

```java
package com.my.springboot.entity;

import lombok.Getter;
import lombok.Setter;

/**
 *
 */
@Getter
@Setter
public class Users {

    /**
     *
     */
    private String uId;

    /**
     * 姓名
     */
    private String uName;

    /**
     * 年龄
     */
    private String uAge;

    /**
     * 性别
     */
    private String uSex;

}
```

### 添加 com.my.springboot.mapper.UsersMapper.java 接口

```java
package com.my.springboot.mapper;

import com.my.springboot.entity.Users;

import java.util.List;

/**
 * Mapper
 */
 @Repository
public interface UsersMapper {

    /**
     * 新增
     *
     * @param users
     * @return 成功数量
     */
    int insertUsers(Users users);

    /**
     * 删除
     *
     * @param id ID
     * @return 成功数量
     */
    int deleteUsersById(String id);

    /**
     * 修改
     *
     * @param users
     * @return 成功数量
     */
    int updateUsers(Users users);

    /**
     * 查询
     *
     * @param users
     * @return 集合
     */
    List<Users> selectUsers(Users users);

}
```

### 添加 mapping/UsersMapping.xml 文件

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.my.springboot.mapper.UsersMapper" >
    <!-- 新增  -->
    <insert id="insertUsers" parameterType="com.my.springboot.entity.Users" >
        INSERT INTO
        users (
            u_id,
            u_name,
            u_age,
            u_sex
        ) VALUES (
            #{uId},
            #{uName},
            #{uAge},
            #{uSex}
        )
    </insert>

    <!-- 删除  -->
    <delete id="deleteUsersById" parameterType="String" >
        DELETE
        FROM
            users
        WHERE
            u_id = #{uId}
    </delete>

    <!-- 修改  -->
    <update id="updateUsers" parameterType="com.my.springboot.entity.Users" >
        UPDATE
            users
        SET
        <trim suffixOverrides="," >
            <if test="uName != null">
                u_name = #{uName},
            </if>
            <if test="uAge != null">
                u_age = #{uAge},
            </if>
            <if test="uSex != null">
                u_sex = #{uSex},
            </if>
        </trim>
        WHERE
            u_id = #{uId}
    </update>

    <!-- 查询  -->
    <select id="selectUsers" parameterType="com.my.springboot.entity.Users" resultType="com.my.springboot.entity.Users">
        SELECT
            u_id AS uId,
            u_name AS uName,
            u_age AS uAge,
            u_sex AS uSex
        FROM
            users
        WHERE
            1 = 1
            <if test="uId != null">
                AND u_id = #{uId}
            </if>
            <if test="uName != null">
                AND u_name = #{uName}
            </if>
            <if test="uAge != null">
                AND u_age = #{uAge}
            </if>
            <if test="uSex != null">
                AND u_sex = #{uSex}
            </if>
    </select>

</mapper>
```

### 在postman 中使用get 请求

http://localhost:8080/users/query?uId=111

```json
[
    {
        "uid": "111",
        "uname": "毛巳煜",
        "uage": "30",
        "usex": "男"
    }
]
```

http://localhost:8080/users/query?uId=222

```json
[
    {
        "uid": "222",
        "uname": "燕大神",
        "uage": "666",
        "usex": "泰国人"
    }
]
```
