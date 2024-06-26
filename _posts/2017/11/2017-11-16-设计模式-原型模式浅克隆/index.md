---
title: "设计模式: 原型模式(浅克隆)"
date: "2017-11-16"
categories: 
  - "java"
---

## Android 应用场景;

- Users对象 与 页面的交互 使用了双向绑定功能,
- 页面有 保存与返回 两个功能,
- 当点击保存时, 保留修改后的数据,
- 当点击返回时, 要恢复之前的数据,
- 问题: 因为双向绑定的原因, 导致 Users对象中的数据被实时修改, 不能还原到之前的数据状态
- 因此: clone 是一个最好的办法

#### JavaCloneExample 测试类

```java
package main;

import java.util.ArrayList;
import java.util.Arrays;

/**
 * Created by mao-siyu on 17-3-28.
 */
public class JavaCloneExample {

    public static void main(String[] args) throws CloneNotSupportedException {

        // 原始对象(被双向绑定的对象)
        Users users = new Users();
        users.id = "1";
        users.name = "mao_siyu";
        users.age = 30;
        users.sex = "男";
        users.hobbys = new ArrayList<>(Arrays.asList("打游戏", "看电影", "钓鱼"));

        // 克隆后的对象(缓存对象)
        Users cloneUsers = (Users) users.clone();
        cloneUsers.id = "2";
        cloneUsers.name = "zhang_su";
        cloneUsers.age = 28;
        cloneUsers.sex = "男";
        cloneUsers.hobbys = new ArrayList<>(Arrays.asList("钓鱼", "打游戏", "看电影"));

        System.out.println(users.hobbys.get(0));
        System.out.println(cloneUsers.hobbys.get(0));
    }
}
```

### Users 用户实体类

```java
package main;

import java.util.List;

/**
 * 添加 Cloneable 标识接口
 * 让Users对象可以被克隆
 */
public class Users implements Cloneable {

    public String id;
    public String name;
    public Integer age;
    public String sex;
    public List<String> hobbys;

    /**
     * 重写 Object 基类的clone方法
     * 让这个类支持克隆功能
     *
     * @return
     * @throws CloneNotSupportedException
     */
    @Override
    protected Object clone() throws CloneNotSupportedException {
        return super.clone();
    }
}
```

## **简单说说`浅克隆`与`深克隆`的区别**

### **浅克隆**

被复制对象的所有变量都含有与原来的对象相同的值, 而所有的`对其他对象的引用都仍然指向原来的对象`. 换言之,浅复制仅仅复制所考虑的对象, 而`不复制它所引用的对象`.

### **深克隆**

深复制是`把要复制的对象所引用的对象都复制了一遍`, 而这种对被引用到的对象的复制叫做间接复制. 深复制要深入到多少层, 是一个不易确定的问题. 在决定使用深复制的时候需要决定多深才算深. 此处, 在深复制的过程中, `很可能会出现循环引用`的问题, 必须小心处理.
