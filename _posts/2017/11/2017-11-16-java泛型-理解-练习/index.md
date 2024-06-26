---
title: "Java泛型 理解 练习"
date: "2017-11-16"
categories: 
  - "java"
---

```java
/**
 * 共同业务 service.
 *
 * @author 毛 巳煜
 * @version 1.0
 * @since 2014/08/20
 *
 * @Service 用于标注业务层组件
 *
 * 泛型中 <T>的含意： 这种是jdk1.5引入的泛型机制，T是根据你输入的来动态匹配类型。
 * 假如泛型设定为 String 类型，然后代码中所有出现 T 的地方都是 String 类型。
 */
@Service
public class GlobalService<T> {

    /**
     * 通过范型来控制传入的类型.
     * 并使用 protected 来控制访问权限
     *
     * @param       entity          输入的类型
     * @return       T
     */
    protected T insert(T entity) {

        return entity;
    }

    /**
     * 通过范型来控制传入的类型.
     *
     * @param       entity          输入的类型
     * @return       T
     */
    protected T delete(T entity) {

        return entity;
    }

    /**
     * 通过范型来控制传入的类型.
     *
     * @param       entity          输入的类型
     * @return       T
     */
    protected T update(T entity) {

        return entity;
    }

    /**
     * 通过范型来控制传入的类型.
     *
     * @param       entity          输入的类型
     * @return       T
     */
    protected T select(T entity) {

        return entity;
    }

}


/**
 * 用户 service
 *
 * @author 毛 巳煜
 * @version 1.0
 * @since 2014/08/20
 *
 *@Service 用于标注业务层组件
 */
@Service
public class UsersService extends GlobalService<Users>{

    public Users getLoginUser(Users users) {

            users.setUserId("mao_siyu@sina.com");
            users.setUserName("毛巳煜");

        try {

            return super.insert(users);

        } catch (Exception e) {
            e.printStackTrace();
        }

        return users;

    }
 }
```
