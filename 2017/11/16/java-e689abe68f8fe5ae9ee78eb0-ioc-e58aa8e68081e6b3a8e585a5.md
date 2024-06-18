---
title: 'Java 扫描实现 Ioc 动态注入'
date: '2017-11-16T13:11:29+00:00'
status: publish
permalink: /2017/11/16/java-%e6%89%ab%e6%8f%8f%e5%ae%9e%e7%8e%b0-ioc-%e5%8a%a8%e6%80%81%e6%b3%a8%e5%85%a5
author: 毛巳煜
excerpt: ''
type: post
id: 267
category:
    - Java
tag: []
post_format: []
---
实现思路
----

- 首先要通过 IO 去找到指定的路径下的所有的 class文件，
- 然后拿到这个文件的全路径，
- 通过反射机制 使用文件的全路径来 初始化对象，
- 接下来判断这个对象是否有使用了我自己定义的注解，如果有就保存到 classMap 中缓存起来，
- 类保存好以后在把方法的名称也 缓存到 methodMap中，方便反射调用。

### 扫描类

```
<pre class="line-numbers prism-highlight" data-start="1">```java
package main;

import java.io.File;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.net.URL;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import annotation.CustomAnnotationBean;
import annotation.CustomAnnotationMethod;

/**
 * 实现 java 扫描
 *
 * @author mao_siyu
 */
public class JavaScan {

    /**
     * 存放 文件根路径
     */
    private String classPath;

    /**
     * 存放结果
     */
    private List<string> classPathList = new ArrayList();

    /**
     * 使用类全名定义的bean容器
     */
    private Map<string class="">> beans = new HashMap();

    /**
     * 使用方法的注解的url属性定义的classes容器
     */
    private Map<string class="">> classes = new HashMap();

    /**
     * method 容器
     */
    private Map<string method=""> methods = new HashMap();

    /**
     * 初始化
     *
     * @return
     * @throws Exception
     */
    public void init(String path) throws Exception {

        if (null == path)
            throw new NullPointerException("JavaScan.init(String path) 参数不能为null");

        // 初始化 获取项目的 classPath 路径
        classPath = new File(getRootPath()).getPath() + File.separator;
        // 使用 IO扫描 指定路径下的所有文件
        getFileName(classPath + path);
        // 使用 所有类命名字符串来 初始化容器
        initContainer();
    }

    /**
     * 获取rootPath的相关的根路径<br></br>
     * getResources("") 如果放为空串儿，那么就是获取rootPath的相关的根路径
     *
     * @return rootPath的相关的根路径
     * @throws Exception
     */
    private String getRootPath() throws Exception {

        // 注： main方法启动 获取路径方式
        Enumeration<url> resources = this.getClass().getClassLoader().getResources("");
        // 注： servlet启动 获取路径方式
        //      Enumeration<url> resources = this.getClass().getClassLoader().getResources("/");
        URL url = resources.nextElement();
        return url.getPath();
    }

    /**
     * 使用 IO扫描 Class文件
     */
    private void getFileName(String rootPath) {

        File file = new File(rootPath);
        // 获取所有文件和文件夹
        File[] fileList = file.listFiles();
        for (int i = 0; null != fileList && i  forName = Class.forName(className);

            // 初始化限制，初始化的文件类型必须是 class文件
            if (!forName.isAnnotation() && !forName.isEnum() && !forName.isInterface()) {

                // 只初始化 实现了CustomAnnotationBean注解的类
                if (forName.isAnnotationPresent(CustomAnnotationBean.class)) {
                    // 初始化类对象 添加到容器中
                    if (!beans.containsKey(className))
                        beans.put(className, forName);
                }

                // 只初始化 实现了CustomAnnotationBean注解的类中的方法
                Method[] methodArray = forName.getDeclaredMethods();
                for (Method method : methodArray) {
                    // 初始化 实现了CustomAnnotationMethod注解的方法
                    if (method.isAnnotationPresent(CustomAnnotationMethod.class)) {
                        // 获取注解
                        CustomAnnotationMethod annotation = method.getAnnotation(CustomAnnotationMethod.class);
                        // 获取注解的属性
                        String attr = annotation.uri();
                        if (!methods.containsKey(attr)) {
                            // 初始化方法 添加到容器中
                            methods.put(attr, method);
                            // 将此方法对应的类 添加到容器中
                            classes.put(attr, forName);
                        }
                    }
                }

            }

        }
    }

    /**
     * 执行 method
     *
     * @param url
     * @return
     * @throws InvocationTargetException
     * @throws IllegalAccessException
     * @throws InstantiationException
     * @throws IllegalArgumentException
     */
    public Object executeMethod(String url, Object... args)
            throws InvocationTargetException, IllegalAccessException, IllegalArgumentException, InstantiationException {

        if (null == url || "".equals(url))
            throw new NullPointerException("ApiPool.executeMethod(String url)：参数不能为null");
        return methods.get(url).invoke(classes.get(url).newInstance(), args);
    }

    /**
     * 获取 使用类全名定义的bean容器
     *
     * @return
     */
    public Map<string class="">> getBeans() {

        return beans;
    }

    /**
     * 获取 使用类全名定义的bean
     *
     * @return
     */
    public Class> getBean(String key) {

        return beans.get(key);
    }

    /**
     * 获取 使用方法的注解的url属性定义的classes容器
     *
     * @return
     */
    public Map<string class="">> getClazzs() {

        return classes;
    }

    /**
     * 获取 使用方法的注解的url属性定义的classes
     *
     * @return
     */
    public Class> getClazz(String key) {

        return classes.get(key);
    }

    /**
     * 获取Method容器
     *
     * @return
     */
    public Map<string method=""> getMethods() {

        return methods;
    }

    /**
     * 获取Method
     *
     * @return
     */
    public Method getMethod(String key) {

        return methods.get(key);
    }

    /**
     * 测试
     *
     * @param args
     * @throws Exception
     */
    public static void main(String[] args) throws Exception {

        JavaScan javaScan = new JavaScan();
        // 在main 方法中调用传空串就可以
        javaScan.init("");

        for (String key : javaScan.getBeans().keySet()) {
            Object object = javaScan.getBean(key);
            System.out.println(object);
        }
    }
}
</string></string></string></url></url></string></string></string></string>
```
```

### 实体Bean的 注解类

```
<pre class="line-numbers prism-highlight" data-start="1">```java
package annotation;

import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * 自定义注解
 */
@Retention(RetentionPolicy.RUNTIME) /** 这种类型的Annotations将被JVM保留,所以他们能在运行时被JVM或其他使用反射机制的代码所读取和使用. */
@Target(ElementType.TYPE) /** 此注解应用于 类上. */
@Documented /** 注解表明这个注解应该被 javadoc工具记录. */
public @interface CustomAnnotationBean {

    /**
     * 描述
     */
    String description() default "";

}

```
```

### 实体Bean的 方法的 注解类

```
<pre class="line-numbers prism-highlight" data-start="1">```java
package annotation;

import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * 自定义注解
 */
@Retention(RetentionPolicy.RUNTIME) /** 这种类型的Annotations将被JVM保留,所以他们能在运行时被JVM或其他使用反射机制的代码所读取和使用. */
@Target(ElementType.METHOD) /** 此注解应用于 方法上. */
@Documented /** 注解表明这个注解应该被 javadoc工具记录. */
public @interface CustomAnnotationMethod {

    /**
     * 描述
     */
    String description() default "";

    /**
     * 访问路径
     *
     * @return
     */
    String uri();
}

```
```

### 实体Bean

```
<pre class="line-numbers prism-highlight" data-start="1">```java
package test1.t1;

import annotation.CustomAnnotationBean;
import annotation.CustomAnnotationMethod;

@CustomAnnotationBean()
public class T1 {

    private String id;

    private String name;

    @CustomAnnotationMethod(uri = "t1/getId")
    public String getId() {

        System.out.println("进入==========t1/getId=========方法");
        return id;
    }

    public void setId(String id) {

        this.id = id;
    }

    @CustomAnnotationMethod(uri = "t1/getName")
    public String getName() {

        System.out.println("进入==========t1/getName=========方法");
        return name;
    }

    public void setName(String name) {

        this.name = name;
    }
}

```
```