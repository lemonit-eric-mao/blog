---
title: "理解 java 反射基础使用方法"
date: "2017-11-16"
categories: 
  - "java"
---

```java
public void methodDemo(Object obj) throws Exception {

/** 以下两种方式取得结果一样  */
// 第一种方式 获得传入的类对象
Class<?> clazz = obj.getClass();
// 第二种方式 根据类对象的全路径 获得
Class<?> clazzForName = Class.forName("jp.co.hitachi.lcs.common.util.BeanUtils");

// 第一种方式 取得这个对象的实例
Object objClazz = clazz.newInstance();
// 第二种方式 取得这个对象的实例
Object objClazzForName = clazzForName.newInstance();

/**
 * 除此之外还有第三种 获取方式就是直接 类名.class  例如：Bean.class;
 * 第一种是  调用任意类对象
 * 第二种是  根据类全名选择性调用
 * 第三种是  直接调用。
 */


// 待执行的方法名称注意没有（）
String methodName = "objectMethodName";


/**
 * 先获取相应的 method 对象
 * getMethod第一个参数是方法名，
 * getMethod第二个参数是该方法的参数类型，
 *因为存在同方法名不同参数这种情况，
 *所以只有同时指定方法名和参数类型才能唯一确定一个方法.
 */
Method method = clazz.getMethod(methodName, new Class[0]);
/**
 * 第一个参数是具体调用该方法的对象
 * 第二个参数是执行该方法的具体参数
 */
System.out.print(method.invoke(objClazz, new Object[0]));


/**
 * 先获取相应的method对象
 * getMethod第一个参数是方法名，
 * getMethod第二个参数是该方法的参数类型，
 *（例如：如果 new Class[3] 那么这个方法有 3 个 Class 类型的参数）
 *因为存在同方法名不同参数这种情况，
 *所以只有同时指定方法名和参数类型才能唯一确定一个方法.
 */
Method methodForName = clazzForName.getDeclaredMethod(methodName, new Class[0]);
/**
 * 第一个参数是具体调用该方法的对象
 * 第二个参数是执行该方法的具体参数，
 *（例如：如果 new Object[5] 那么这个方法有 5 个 Object 类型的参数）
 */
System.out.print(methodForName.invoke(objClazzForName, new Object[0]));


/**
 * 以下是 getDeclaredMethod 与 getMethod 的区别详解 API 文档
 *
 * Method getDeclaredMethod(String name, Class… parameterTypes)d
 *返回一个 Method 对象，
 *该对象反映此 Class 对象所表示的类或接口的指定已声明方法。
 *
 * Method[] getDeclaredMethods()
 *返回 Method 对象的一个数组，
 *这些对象反映此 Class 对象表示的类或接口声明的所有方法，
 *包括公共、保护、默认（包）访问和私有方法，但不包括继承的方法。
 *
 * Method getMethod(String name, Class… parameterTypes)
 *返回一个 Method 对象，
 *它反映此 Class 对象所表示的类或接口的指定公共成员方法。
 *
 * Method[] getMethods()
 *返回一个包含某些 Method 对象的数组，
 *这些对象反映此 Class 对象所表示的类或接口
 *（包括那些由该类或接口声明的以及从超类和超接口继承的那些的类或接口）
 *的公共 member 方法。
 *
 * getDeclaredField(String name)
 *返回一个 Field 对象，
 *该对象反映此 Class 对象所表示的类或接口的指定已声明字段。
 *
 * Field[] getDeclaredFields()
 *返回 Field 对象的一个数组，
 *这些对象反映此 Class 对象所表示的类或接口所声明的所有字段，
 *包括公共、保护、默认（包）访问和私有字段，但不包括继承的字段。
 */
}
```

* * *

###### 反射简写, 获取某个属性值

```java
public class Test {

    private String testId;

    public String getTestId() {
        return testId;
    }

    public void setTestId(String testId) {
        this.testId = testId;
    }


    public static void main(String[] args) throws Exception {
        Test test = new Test();
        test.setTestId("1234");

        Object result = Test.class.getDeclaredMethod("getTestId").invoke(test);
        System.out.println(result); // 1234
    }

}
```

* * *
