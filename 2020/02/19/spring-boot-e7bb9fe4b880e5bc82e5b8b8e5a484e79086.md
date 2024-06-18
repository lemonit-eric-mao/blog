---
title: 'Spring-Boot 统一异常处理'
date: '2020-02-19T17:30:36+00:00'
status: publish
permalink: /2020/02/19/spring-boot-%e7%bb%9f%e4%b8%80%e5%bc%82%e5%b8%b8%e5%a4%84%e7%90%86
author: 毛巳煜
excerpt: ''
type: post
id: 5259
category:
    - spring-boot
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### spring-boot 自定义异常 统一处理

###### 项目结构

```yml
oidc-auth-server\src\main\java\
cn.com.server.commons.exception.
├─capture
│      ExceptionHandle.java
│      ExceptionInfoEntity.java
│
└─custom
        AbstractBaseRuntimeException.java
        BusinessException.java
        CustomHttpStatus.java

```

- - - - - -

##### capture

###### ExceptionHandle.java

```java
/**
 * 此包中存放了spring boot 全局异常捕获的配置
 */
package cn.com.server.commons.exception.capture;

import cn.com.server.commons.exception.custom.AbstractBaseRuntimeException;
import cn.com.server.commons.exception.custom.CustomHttpStatus;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.ResponseStatus;

/**
 * 定义-全局异常捕获
 *
 * @author: Eric.Mao
 * @date: 2022-01-05
 */
@ControllerAdvice
@ResponseBody
public class ExceptionHandle {


    /**
     * 捕获系统 500异常
     *
     * @param exception 系统异常
     * @return 系统异常信息
     */
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR) // 返回给前端的http异常码
    @ExceptionHandler(Exception.class)
    public ExceptionInfoEntity doExcetion(Exception exception) {
        return getResultEntity(exception, HttpStatus.INTERNAL_SERVER_ERROR);
    }

    /**
     * 捕获 **自定义异常**
     *
     * @param exception
     * @return
     */
    @ResponseStatus(HttpStatus.BAD_REQUEST) // 返回给前端的http异常码
    @ExceptionHandler(AbstractBaseRuntimeException.class)
    public ExceptionInfoEntity doAbstractBaseRuntimeException(AbstractBaseRuntimeException exception) {
        return getResultEntity(exception, exception.getCustomHttpStatus());
    }

    /**
     * -----------------------------------------------------------------------------------------------------------------
     */

    /**
     * 此函数返回系统异常信息
     *
     * @param exception  系统异常
     * @param httpStatus code码
     * @return 系统异常信息
     */
    private ExceptionInfoEntity getResultEntity(Exception exception, Enum httpStatus) {

        String code = httpStatus.name();
        String description = httpStatus.toString();
        String type = exception.getClass().toString();
        String path = exception.getStackTrace()[0].toString();
        String message = exception.getCause() == null ? exception.getMessage() : exception.getCause().getMessage();

        // 输出到控制台
        outputConsulLog(code, description, type, path, message);

        // 返回给前端
        ExceptionInfoEntity infoEntity = new ExceptionInfoEntity();
        infoEntity.setCode(code);
        infoEntity.setDescription(description);
        infoEntity.setMessage(message);

        return infoEntity;
    }

    /**
     * 将异常信息输出到控制台
     *
     * @param errorInfo
     */
    private void outputConsulLog(String... errorInfo) {

        StringBuilder builder = new StringBuilder();
        builder.append(errorInfo[0]).append("\n")
                .append("\t").append(errorInfo[1]).append("\n")
                .append("\t").append(errorInfo[2]).append("\n")
                .append("\t").append(errorInfo[3]).append("\n")
                .append("\t").append(errorInfo[4]).append("\n");

        System.out.println(builder.toString());

    }

}


```

- - - - - -

###### ExceptionInfoEntity.java

```java
package cn.com.server.commons.exception.capture;

import lombok.Data;

/**
 * 定义-异常信息-实体类
 *
 * @author Eric.Mao
 * @date 2022-01-05
 */
@Data
public class ExceptionInfoEntity {

    /**
     * 异常码
     */
    private String code;

    /**
     * 异常信息
     */
    private String message;

    /**
     * 异常描述
     */
    private String description;

}


```

- - - - - -

##### custom

###### AbstractBaseRuntimeException.java

```java
package cn.com.server.commons.exception.custom;

/**
 * 定义-异常抽象基类
 *
 * @author: Eric.Mao
 * @date: 2022-01-05
 */
public abstract class AbstractBaseRuntimeException extends RuntimeException {

    /**
     * 有参数构造方法
     *
     * @param message 错误信息
     */
    public AbstractBaseRuntimeException(String message) {
        super(message);
    }

    /**
     * 异常状态码
     *
     * @return
     */
    public abstract CustomHttpStatus getCustomHttpStatus();

}


```

- - - - - -

###### BusinessException.java

```java
package cn.com.server.commons.exception.custom;

/**
 * 定义-业务逻辑异常-实现类
 *
 * @author: Eric.Mao
 * @date: 2022-01-05
 */
public class BusinessException extends AbstractBaseRuntimeException {

    public BusinessException(String message) {
        super(message);
    }

    /**
     * 异常状态码
     *
     * @return
     */
    @Override
    public CustomHttpStatus getCustomHttpStatus() {
        return CustomHttpStatus.BUSINESS_EXCEPTION;
    }

}


```

- - - - - -

###### CustomHttpStatus.java

```java
package cn.com.server.commons.exception.custom;

/**
 * @author Eric.Mao
 * @title: CustomHttpStatus
 * @description: 自定义Http状态码
 * @date 2022-01-05
 */
public enum CustomHttpStatus {

    BUSINESS_EXCEPTION("业务逻辑异常"),
    DB_EXCEPTION("数据库操作异常");

    private String message;

    CustomHttpStatus(String message) {
        this.message = message;

    }

    @Override
    public String toString() {
        return message;
    }

}


```

- - - - - -

- - - - - -

- - - - - -

###### 返回结果，异常JSON

```json
// 返回给前端的结果
{
  "code": "INTERNAL_SERVER_ERROR",
  "message": "/ by zero",
  "description": "500 INTERNAL_SERVER_ERROR"
}

// 服务端的控制台日志
INTERNAL_SERVER_ERROR
    500 INTERNAL_SERVER_ERROR
    class java.lang.ArithmeticException
    cn.com.server.controller.AuthoritiesController.deleteAuthoritiesById(AuthoritiesController.java:53)
    / by zero

```

- - - - - -

```json
// 返回给前端的结果
{
  "code": "BUSINESS_EXCEPTION",
  "message": "Test Error",
  "description": "业务逻辑异常"
}

// 服务端的控制台日志
BUSINESS_EXCEPTION
    业务逻辑异常
    class cn.com.server.commons.exception.custom.BusinessException
    cn.com.server.controller.AuthoritiesController.queryAuthoritiesById(AuthoritiesController.java:81)
    Test Error


```

- - - - - -

- - - - - -

- - - - - -