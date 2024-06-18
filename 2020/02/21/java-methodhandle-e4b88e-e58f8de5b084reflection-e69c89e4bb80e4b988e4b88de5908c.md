---
title: 'Java MethodHandle 与 反射(Reflection ) 有什么不同?'
date: '2020-02-21T07:59:26+00:00'
status: private
permalink: /2020/02/21/java-methodhandle-%e4%b8%8e-%e5%8f%8d%e5%b0%84reflection-%e6%9c%89%e4%bb%80%e4%b9%88%e4%b8%8d%e5%90%8c
author: 毛巳煜
excerpt: ''
type: post
id: 5262
category:
    - Java
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
 仅站在Java语言的角度看，**`MethodHandle`** 在使用方法和效果上与 **`Reflection`** 有众多相似之  
处。不过，它们也有以下这些区别：

- **`Reflection`** 和 **`MethodHandle`** 机制本质上都是在模拟方法调用，但是`Reflection`是在**`模拟Java代码`** 层次的方法调用，而`MethodHandle`是在 **`模拟字节码`** 层次的方法调用。在`MethodHandles.Lookup`上的3个方法`findStatic()`、`findVirtual()`、`findSpecial()`正是为了对应于`invokestatic`、`invokevirtual`（以及`invokeinterface`和`invokespecial`）这几条字节码指令的执行权限校验行为，而这些底层细节，在使用Reflection API时是不需要关心的。
- **`Reflection`** 中的`java.lang.reflect.Method`对象远比`MethodHandle`机制中的`java.lang.invoke.MethodHandle`对象所包含的信息来得多。前者是方法在Java端的全面映像，包含了方法  
  的签名、描述符以及方法属性表中各种属性的Java端表示方式，还包含执行权限等的运行期信息。而后者仅包含执行该方法的相关信息。**用开发人员通俗的话来讲，Reflection是`重量级`，而MethodHandle是`轻量级`。**
- **`MethodHandle`** 是对字节码的方法指令调用的模拟，那理论上虚拟机在这方面做的各种优化（如方法内联），在MethodHandle上也应当可以采用类似思路去支持（但目前实现还在继续完善中），而通过`反射`去`调用方法`则`几乎不可能`直接去`实施`各类`调用点优化`措施。
- **`Reflection`** 和 **`MethodHandle`** 除了上面列举的区别外，最关键的一点还在于去掉前面讨论施加的前提 **`仅站在Java语言的角度看`** 之后  
   `Reflection API`的设计目标是`只为Java语言服务`的，而`MethodHandle`则设计为可服务于`所有Java虚拟机之`上的语言，其中也包括了Java语言而已，而且Java在这里并不是主  
  角。

```java
import java.lang.invoke.MethodHandle;
import java.lang.invoke.MethodHandles;
import java.lang.invoke.MethodType;

public class MethodHandleTest {
    static class ClassA {
        public void println(String s) {
            System.out.println(s);
        }
    }

    public static void main(String[] args) throws Throwable {
        Object obj = System.currentTimeMillis() % 2 == 0 ? System.out : new ClassA();
        // 无论obj最终是哪个实现类，下面这句都能正确调用到println方法。
        getPrintlnMH(obj).invokeExact("icyfenix=====" + obj.getClass());
    }

    private static MethodHandle getPrintlnMH(Object reveiver) throws Throwable {
        // MethodType：代表“方法类型”，包含了方法的返回值（methodType()的第一个参数）和
        // 具体参数（methodType() 第二个及以后的参数）。
        MethodType mt = MethodType.methodType(void.class, String.class);
        // lookup()方法来自于MethodHandles.lookup，这句的作用是在指定类中查找符合给定的方法
        // 名称、方法类型，并且符合调用权限的方法句柄。
        // 因为这里调用的是一个虚方法，按照Java语言的规则，方法第一个参数是隐式的，代表该方法的接收者
        // ，也即this指向的对象，这个参数以前是放在参数列表中进行传递，现在提供了bindTo()方法来完成这件事情。
        return MethodHandles.lookup().findVirtual(reveiver.getClass(), "println", mt).bindTo(reveiver);
    }
}

```

- - - - - -