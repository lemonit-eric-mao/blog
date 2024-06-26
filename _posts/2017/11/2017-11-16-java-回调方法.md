---
title: "Java 回调方法"
date: "2017-11-16"
categories: 
  - "java"
---

```java
package callBack;

/**
 * <pre>
 * 第一步
 * 回调接口 (定义这个接口 就相当于定义一条通道)
 *
 * author maosy E-mail:
 * version 创建时间：2016年2月26日 下午2:52:36
 * </pre>
 */
public interface CallBack {

    /**
     * 回调方法 (这里指的是传输通道)
     *
     * @param message
     */
    public void callBackTransport(String message);
}
```

```java
package callBack;

/**
 * <pre>
 * 第二步
 * 接收者 类
 *
 * author maosy E-mail:
 * version 创建时间：2016年2月26日 下午2:52:36
 * </pre>
 */
public class Recipient implements CallBack {

    @Override
    public void callBackTransport(String message) {

        System.out.printf("%s", message);
    }

}
```

```java
package callBack;

/**
 * <pre>
 * 第三步
 * 推送者 类
 *
 * author maosy E-mail:
 * version 创建时间：2016年2月26日 下午2:52:36
 * </pre>
 */
public class Push {

    /** 准备传输通道 (被推送者) */
    private CallBack callBack;

    public Push(CallBack callBack) {
        this.callBack = callBack;
    }
```

```java
    /**
     * 推送信息
     *
     * @param message
     */
    public void pushMessage(String message) {

        callBack.callBackTransport(message);
    }

    public static void main(String[] args) {

        Push push = new Push(new Recipient());
        push.pushMessage("java的回调思想就是,把实现了 这个回调接口的对象,拿到自己的类中进行操作。也是多态的一种形式!");
    }
}
```
