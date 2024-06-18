---
title: "JVM中的堆、栈都放了些什么？"
date: "2020-03-11"
categories: 
  - "java"
---

**[参考资料](https://www.cnblogs.com/iyangyuan/p/4631696.html "参考资料")**

![](http://qiniu.dev-share.top/JVM-%E5%86%85%E5%AD%98%E5%88%86%E5%B8%83%E5%9B%BE.png)

* * *

##### JVM中的堆、栈都放了些什么？

```java
/**
 * @author mao_siyu
 * @date 2020/3/10 23:17
 */
public class Test {

    public static void main(String[] args) {

        int num1 = 10;
        int num2 = 10;
        System.out.println(num1 == num2); // true

        String str1 = "mao";
        String str2 = "mao";
        System.out.println(str1 == str2); // true

        String stra = new String("mao");
        String strb = new String("mao");
        System.out.println(stra == strb); // false

    }
}
```

###### **上面的代码在内存中是如何搁置的**

![](http://qiniu.dev-share.top/%E5%A0%86-%E6%A0%88.gif)

###### **解释**

- `String str1 = "mao";` 与 `String stra = new String("mao");` 的区别是，值放在了不同的区域;
- `String str1 = "mao";` 的值放在了方法区的常量池中，这个`属于JVM特定优化`
- `String stra = new String("mao");` 的值放在了堆中
- 而对于栈来说，栈帧中放的都是`引用地址`, `String str1` 中存放的是常量池中的内存地址，`String stra` 中存放的是堆中的内存地址
- 在常量池中的相同值，地址也相同
- 在堆中每个对象的地址都不同
- `等号左边`都是放在栈中， `new`关键字表示在`堆`中开辟一块新的空间

* * *

###### **`小结一下：`**

- 我现在知道，在虚拟机中有 **`方法区`** 、**`栈`** 、**`堆`** ，我们`写程序的目的`就是操作数据，那么要如何去操作呢？
    
- 程序员先编写好操作数据的指令集(也就是代码)，放到方法区中，有了指令也有了数据要如何去执行呢，当然是 由线程来执行这些指令，那么线程是如何执行这些指令的呢？
    
- `线程`是将指令放到了栈中执行，按照栈的使用方式来`执行指令`，由此来实现控制数据的目的。
    
- 指令放在方法区中， 数据放在堆中， 执行指令的过程在栈中
