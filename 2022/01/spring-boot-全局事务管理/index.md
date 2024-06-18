---
title: "Spring-Boot 全局事务管理"
date: "2022-01-05"
categories: 
  - "spring-boot"
---

###### 全局事务管理器

```java
package cn.com.server.commons.aop;

import org.aspectj.lang.annotation.Aspect;
import org.springframework.aop.Advisor;
import org.springframework.aop.aspectj.AspectJExpressionPointcut;
import org.springframework.aop.support.DefaultPointcutAdvisor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.transaction.TransactionDefinition;
import org.springframework.transaction.TransactionManager;
import org.springframework.transaction.interceptor.NameMatchTransactionAttributeSource;
import org.springframework.transaction.interceptor.RollbackRuleAttribute;
import org.springframework.transaction.interceptor.RuleBasedTransactionAttribute;
import org.springframework.transaction.interceptor.TransactionAttribute;
import org.springframework.transaction.interceptor.TransactionInterceptor;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

/**
 * 全局事务管理器
 *
 * @author: Eric.Mao
 * @date: 2022-01-05
 */
@Aspect
@Configuration
public class TransactionConfig {

    /**
     * 配置事务过期时间，默认-1,永不超时
     */
    private final static int METHOD_TIME_OUT = 5000;

    /**
     * 配置切入点表达式
     * <p>
     * 1.execution(): 表达式主体
     * 2.第一个*号:表示返回类型，*号表示所有的类型
     * 3.com.test.lee.service表示切入点的包名
     * 4.第二个*号:表示实现包
     * 5.*(..)表示所有方法名,..表示所有类型的参数
     */
    private static final String POINTCUT_EXPRESSION = "execution(* cn.com.server.service..*.*(..))";

    /**
     * 事务管理器
     */
    @Autowired
    private TransactionManager transactionManager;

    /**
     * 全局事务配置
     * <p>
     * REQUIRED ：如果当前存在事务，则加入该事务；如果当前没有事务，则创建一个新的事务。
     * SUPPORTS ：如果当前存在事务，则加入该事务；如果当前没有事务，则以非事务的方式继续运行。
     * MANDATORY ：如果当前存在事务，则加入该事务；如果当前没有事务，则抛出异常。
     * REQUIRES_NEW ：创建一个新的事务，如果当前存在事务，则把当前事务挂起。
     * NOT_SUPPORTED ：以非事务方式运行，如果当前存在事务，则把当前事务挂起。
     * NEVER ：以非事务方式运行，如果当前存在事务，则抛出异常。
     * NESTED ：如果当前存在事务，则创建一个事务作为当前事务的嵌套事务来运行；如果当前没有事务，则该取值等价于 REQUIRED 。
     * 指定方法：通过使用 propagation 属性设置，例如：@Transactional(propagation = Propagation.REQUIRED)
     */
    @Bean
    public TransactionInterceptor txAdvice() {

        // 事务管理规则，声明具备事务管理的方法名
        NameMatchTransactionAttributeSource source = new NameMatchTransactionAttributeSource();

        // 当前存在事务就使用当前事务，当前不存在事务就创建一个新的事务
        RuleBasedTransactionAttribute required = new RuleBasedTransactionAttribute();
        // 抛出异常后执行切点回滚,这边你可以更换异常的类型
        required.setRollbackRules(Collections.singletonList(new RollbackRuleAttribute(Exception.class)));
        // PROPAGATION_REQUIRED:事务隔离性为1，若当前存在事务，则加入该事务；如果当前没有事务，则创建一个新的事务。这是默认值
        required.setPropagationBehavior(TransactionDefinition.PROPAGATION_REQUIRED);
        // 设置事务失效时间，如果超过5秒，则回滚事务
        required.setTimeout(METHOD_TIME_OUT);

        // 只读事务，不做更新操作
        RuleBasedTransactionAttribute readOnly = new RuleBasedTransactionAttribute();
        readOnly.setReadOnly(true);
        readOnly.setPropagationBehavior(TransactionDefinition.PROPAGATION_NOT_SUPPORTED);

        Map<String, TransactionAttribute> attributesMap = new HashMap<>(30);
        // 设置增删改上传等使用事务
        attributesMap.put("save*", required);
        attributesMap.put("remove*", required);
        attributesMap.put("update*", required);
        attributesMap.put("batch*", required);
        attributesMap.put("clear*", required);
        attributesMap.put("add*", required);
        attributesMap.put("append*", required);
        attributesMap.put("modify*", required);
        attributesMap.put("edit*", required);
        attributesMap.put("insert*", required);
        attributesMap.put("delete*", required);
        attributesMap.put("do*", required);
        attributesMap.put("create*", required);
        attributesMap.put("import*", required);

        // 其他方法无事务，全部设为只读
        attributesMap.put("*", readOnly);
//        attributesMap.put("select*", readOnly);
//        attributesMap.put("get*", readOnly);
//        attributesMap.put("valid*", readOnly);
//        attributesMap.put("list*", readOnly);
//        attributesMap.put("count*", readOnly);
//        attributesMap.put("find*", readOnly);
//        attributesMap.put("load*", readOnly);
//        attributesMap.put("search*", readOnly);

        source.setNameMap(attributesMap);

        return new TransactionInterceptor(transactionManager, source);
    }

    /**
     * 设置切面=切点pointcut+通知TxAdvice
     */
    @Bean
    public Advisor txAdviceAdvisor() {
        // 声明切点的面：切面就是通知和切入点的结合。通知和切入点共同定义了关于切面的全部内容——它的功能、在何时和何地完成其功能
        AspectJExpressionPointcut pointcut = new AspectJExpressionPointcut();
        // 声明和设置需要拦截的方法,用切点语言描写
        pointcut.setExpression(POINTCUT_EXPRESSION);
        // 设置切面=切点pointcut+通知TxAdvice
        return new DefaultPointcutAdvisor(pointcut, txAdvice());
    }

}

```

* * *

###### 注意：开启事务支持

事务使用之前，要在启动类`ServerApplication.java`里面引入注解 `@EnableTransactionManagement`

* * *

* * *

* * *
