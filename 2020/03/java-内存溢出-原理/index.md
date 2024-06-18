---
title: "Java 内存溢出-原理"
date: "2020-03-10"
categories: 
  - "java"
---

##### **栈溢出 `StackOverflowError`**

```java
/**
 * VM Args: -Xss128k
 * 执行class: java -Xss128K JavaVMStackSOF
 */
public class JavaVMStackSOF {

    private int stackLength = 1;

    public void exec() {
        stackLength++;
        exec();
    }

    public static void main(String[] args) {

        JavaVMStackSOF jms = new JavaVMStackSOF();

        try {
            jms.exec();
        } catch (Throwable e) {
            System.out.println("stack length: " + jms.stackLength);
            System.out.println(e);
            return;
        }
    }
}
```

**执行结果**

```ruby
[root@test ~]# javac JavaVMStackSOF.java
[root@test ~]# java -Xss128K JavaVMStackSOF
stack length: 995
java.lang.StackOverflowError

[root@test ~]#
```

**`总结`** 每执行一个方法都会向`栈`中`加入一个栈帧`，当`栈帧`的`数量`超过了栈的长度就会引发`StackOverflowError`异常

* * *

##### **堆溢出 `OutOfMemoryError`**

```java
import java.util.ArrayList;
import java.util.List;

/**
 * VM Args: -Xms20m -Xmx20m -XX:+HeapDumpOnOutOfMemoryError
 * 执行class: java -Xms20m -Xmx20m -XX:+HeapDumpOnOutOfMemoryError HeapOOM
 */
public class HeapOOM {
    static class OOMObject {

    }

    public static void main(String[] args) {
        List<OOMObject> objects = new ArrayList<>();
        while (true) {
            objects.add(new OOMObject());
        }
    }
}
```

**执行结果**

```ruby
[root@test ~]# javac HeapOOM.java
[root@test ~]# java -Xms20m -Xmx20m -XX:+HeapDumpOnOutOfMemoryError HeapOOM
java.lang.OutOfMemoryError: Java heap space
Dumping heap to java_pid7680.hprof ...
Heap dump file created [28079887 bytes in 0.065 secs]
Exception in thread "main" java.lang.OutOfMemoryError: Java heap space
......以下省略......

[root@test ~]#
```
