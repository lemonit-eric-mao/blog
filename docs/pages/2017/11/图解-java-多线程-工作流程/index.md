---
title: "图解 java 多线程 工作流程"
date: "2017-11-16"
categories: 
  - "java"
---

### **单线程**

![](http://qiniu.dev-share.top/image/danxiancheng.png)

### **多线程**

![](http://qiniu.dev-share.top/image/multread.png)

**示例代码如下:**

```java
package itfactor;

public class Test {

    static int index = 0;

    public static void main(String[] args) {
        // 上图以 3个线程为例, 这里为了测试效果明显, 启用 1000个线程.
        for (int i = 0; i < 1000; i++) {

            new Thread(new Runnable() {
                @Override
                public void run() {
                    index++;
                    System.out.println(index);
                }
            }).start();

        }
    }
}
```

**第二种写法**

```java
package itfactor;

public class Test {

    public static void main(String[] args) {

        int index = 0;

        for (int i = 0; i < 1000; i++) {
            // 这里投机取巧了, 性能特别差, 不要这么干
            int[] indexs = {index++};

            new Thread(new Runnable() {

                @Override
                public void run() {

                    System.out.println(indexs[0]);
                }
            }).start();

        }
    }
}
```

**便于理解 提个问: 如下代码 结果是什么?, 根据下面的注释说出两个结果**

```java
package itfactor;

public class Test {

    public static void main(String[] args) {

        final StringBuffer stringBuffer = new StringBuffer();

        for (int i = 0; i < 1000; i++) {

            new Thread(new Runnable() {

                @Override
                public void run() {

                    stringBuffer.append(1);
                    // 如果将下面的代码注释取消结果是什么?
                    // stringBuffer.append(66);
                    System.out.println(stringBuffer.length());
                }
            }).start();

        }
    }
}
```

### **synchronized**

![](http://qiniu.dev-share.top/image/synchronized.png)

答案: (1) length等于1000; (2) length等于3000;
