---
title: Javaagent简单应用
date: '2022-04-25T09:21:41+00:00'
status: publish
permalink: /2022/04/25/javaagent%e7%ae%80%e5%8d%95%e5%ba%94%e7%94%a8
author: 毛巳煜
excerpt: ''
type: post
id: 8555
category:
    - Java
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
##### 前置资料

- **windowns 10**
- **JDK 1.8.0**

- - - - - -

###### **[了解Jar命令怎么使用](http://www.dev-share.top/2020/02/26/java-%e5%b8%b8%e8%a7%81%e9%97%ae%e9%a2%98/ "了解Jar命令怎么使用")**

- - - - - -

###### **`Javaagent` 是什么？**

> - **`Javaagent` 又叫做 `Java 探针`** ，该功能是 Java 虚拟机提供的一整套后门，通过这套后门可以对虚拟机方方面面进行监控与分析，甚至干预虚拟机的运行。
> - **`Javaagent`** ，是在 JDK1.5 引入的一种可以 **`动态修改 Java 字节码`** 的技术。Java 类编译之后形成字节码被 **JVM** 执行，在 **JVM** 在执行这些字节码之前获取这些字节码信息，并且通过字节码转换器对这些字节码进行修改，来完成一些额外的功能。
> - **`Javaagent`，是java命令的一个参数。参数 `javaagent` 可以用于指定一个 `jar` 包，并且对该 `java` 包有2个要求** ： 
>   - jar包的 `MANIFEST.MF` 文件必须指定`Premain-Class`项。
>   - `Premain-Class` 指定的那个类必须实现 `premain()` 方法。 
>       - **premain** 方法，从字面上理解，就是运行在 **main** 函数之前的的类。
>       - 当**Java 虚拟机**启动时，在执行 **main** 函数之前，**JVM** 会先运行`-javaagent`所指定 `jar` 包内 `Premain-Class` 这个类的 `premain` 方法 。

- - - - - -

- - - - - -

- - - - - -

##### 实现思路

1. 首先模拟业务程序
2. 为业务程序开发一个agent程序
3. 测试

- - - - - -

###### 1. 模拟业务程序，创建`TestJavaApp.java`文件

```java
public class TestJavaApp {

    public static void main(String[] args) {
        System.out.println("我是业务程序:---> test-java-app");
    }
}


```

###### 1.1 编译、打包、执行

```ruby
## 编译
E:\gitee-project\javaagent-example\src> javac TestJavaApp.java -encoding utf-8

## 打包
E:\gitee-project\javaagent-example\src> jar cfe TestJavaApp.jar TestJavaApp TestJavaApp.class

## 测试执行
E:\gitee-project\javaagent-example\src> java -jar TestJavaApp.jar
我是业务程序:---> test-java-app


```

- - - - - -

- - - - - -

- - - - - -

##### 2. 编写 javaagent程序

**使用 javaagent 需要几个步骤：**

> 1. 定义一个 `MANIFEST.MF` 文件，必须包含 `Premain-Class` 选项，通常也会加入`Can-Redefine-Classes` 和 `Can-Retransform-Classes` 选项。
> 2. 创建一个`Premain-Class` 指定的类，类中包含 `premain` 方法，方法逻辑由用户自己确定。
> 3. 将 `premain` 的类和 `MANIFEST.MF` 文件打成 jar 包。
> 4. 使用参数 `-javaagent:<jar>[=]</jar>`

###### 2.1 创建`TestJavaAgent.java`文件

```java
import java.lang.instrument.Instrumentation;

public class TestJavaAgent {

    /**
     * 该方法在main方法之前运行，与main方法运行在同一个JVM中
     * 并被同一个System ClassLoader装载
     * 被统一的安全策略(security policy)和上下文(context)管理
     * <p>
     * 在这个 premain 函数中，开发者可以进行对类的各种操作。
     * 1、agentArgs 是 premain 函数得到的程序参数，随同 “– javaagent”一起传入。与 main 函数不同的是，
     * 这个参数是一个字符串而不是一个字符串数组，如果程序参数有多个，程序将自行解析这个字符串。
     * 2、inst 是一个 java.lang.instrument.Instrumentation 的实例，由 JVM 自动传入。
     * java.lang.instrument.Instrumentation 是 instrument 包中定义的一个接口，也是这个包的核心部分，
     * 集中了其中几乎所有的功能方法，例如类定义的转换和操作等等。
     *
     * @param agentArgs
     * @param inst
     */
    public static void premain(String agentArgs, Instrumentation inst) {
        System.out.println("=========premain方法执行1========");
        System.out.println(agentArgs);
    }

    /**
     * 如果不存在 premain(String agentArgs, Instrumentation inst)
     * 则会执行 premain(String agentArgs)
     *
     * @param agentArgs
     */
    public static void premain(String agentArgs) {
        System.out.println("=========premain方法执行2========");
        System.out.println(agentArgs);
    }
}

</p>
```

###### 2.2 创建`MANIFEST.MF`文件

```yaml
Manifest-Version: 1.0
Can-Redefine-Classes: true
Can-Retransform-Classes: true
Premain-Class: TestJavaAgent


```

**`注意`**：`MANIFEST.MF`文件的最后一行是空行，不能省略

###### 2.3 编译、打包、执行

```ruby
## 编译 -encoding utf-8 防止中文注释乱码
E:\gitee-project\javaagent-example\src> javac TestJavaAgent.java -encoding utf-8

## 打包，使用 m 选项，把指定文件名的manifest文件传入
E:\gitee-project\javaagent-example\src> jar cvfm TestJavaAgent.jar MANIFEST.MF TestJavaAgent.class

## 测试执行
E:\gitee-project\javaagent-example\src> java -jar -javaagent:TestJavaAgent.jar=TestParamStr TestJavaApp.jar
=========premain1========
TestParamStr
我是业务程序:---> test-java-app


```

- - - - - -

- - - - - -

- - - - - -

##### 3. 注意事项

1. 如果你把 `-javaagent:TestJavaAgent.jar` 放在 `TestJavaApp.jar` 后面，则不会生效。也就是说，放在主程序后面的 `agent` 是无效的。
2. 使用命令行打jar包时，如果要使用`MANIFEST.MF`文件，需要使用 **jar -cvf`m`** 参数

- - - - - -

- - - - - -

- - - - - -

#### 4. **`思考一下`**

> 通过之前的学习，我们了解到 **premain()** 在JVM启动时加载的 `JavaAgent`，也就是在业务程序执行 **main方法执行之前** 运行该`agent`，那么如果期望在`main`方法之后运行应该如何实现呢？

- **premain**: 【**`静态`Instrument**】 在JVM启动时加载的`Java Agent`，例如使用`java -jar`命令启动jar文件时，添加`-javaagent`命令添加 `JavaAgent`；通俗来说就是在JVM初始化之后，**main方法`之前`运行该agent**```java
  public static void premain(String agentArgs, Instrumentation inst) {}
  public static void premain(String agentArgs) {}
  
  ```
- **有一个问题** 静态 `Instrument` 需要把 `Agent` 程序提前写好，与应用实例一并启动，所作的 `Instrumentation` 也仅限于 `main` 函数执行前，这样的方式存在一定的局限性。  
  所以在**JavaSE6以后**的 `Instrumentation` 当中，提供了一个新的代理操作方法：`agentmain`，可以在 `main` 函数开始运行之后再运行。
- **agentmain**: 【**`动态`Instrument**】 使用`Java Attach API`将`Java Agent`动态加载到`JVM`中，在`JVM`初始化之后运行，可以在我们的**main方法`执行时`通过Attach API`调用`该agent**
  
  ```java
  public static void agentmain(String agentArgs, Instrumentation inst) {}
  public static void agentmain(String agentArgs) {}
  
  ```

- - - - - -

###### **详解`java.lang.instrument`**

`java.lang.instrument`包是基于JVMTI机制实现的

> - **JVMTI**（**Java Virtual Machine Tool Interface**）是一套由 Java 虚拟机提供的了一套代理程序机制，可以支持第三方工具程序以代理的方式连接和访问 JVM。  
>    **JVMTI** 的功能非常丰富，包括虚拟机中线程、内存/堆/栈，类/方法/变量，事件/定时器处理等等。  
>    使用 **JVMTI** 一个基本的方式就是设置回调函数，在某些事件发生的时候触发并作出相应的动作，这些事件包括虚拟机初始化、开始运行、结束，类的加载，方法出入，线程始末等等。

**Instrument** 就是一个基于 **JVMTI** 接口的，以代理方式连接和访问 **JVM** 的一个 **Agent**。这样的特性实际上提供了一种虚拟机级别的 **AOP** 实现。

- - - - - -

###### 那么应用程序是如何识别Java Agent的呢？

答案就是`MANIFEST.MF`文件，该文件作为JAR文件的一部分包含jar文件的元数据信息，其中关于`Java Agent`的属性如下：

<table><thead><tr><th>属性</th><th align="left">说明</th></tr></thead><tbody><tr><td>**Premain-Class**</td><td align="left">包含 `premain` 方法的类（类的全路径名）；  
如果在JVM启动时指定Java Agent则**必须定义该属性**</td></tr><tr><td>**Agent-Class**</td><td align="left">包含 `agentmain` 方法的类（类的全路径名）；</td></tr><tr><td>**Can-Readefine-Classes**</td><td align="left">定义`Java Agent`是否能够重定义Java类，其值为**true or false**，**默认false**</td></tr><tr><td>**Can-Retransform-Classes**</td><td align="left">定义`Java Agent`能否重转换Java类，其值为**true or false**，**默认false**</td></tr><tr><td>**Can-Set-Native-Method-Prefix**</td><td align="left">定义`Java Agent`能否设置所需的本机方法前缀，**默认false**</td></tr><tr><td>**Boot-Class-Path**</td><td align="left">设置启动类加载器搜索的路径列表；  
查找类的特定于平台的机制失败后，引导类加载器会搜索这些路径；  
按列出的顺序搜索路径，列表中的路径由一个或多个空格分开；  
路径使用分层 URI 的路径组件语法；  
如果该路径以斜杠字符（"/"）开头，则为绝对路径，否则为相对路径；  
相对路径根据代理 JAR 文件的绝对路径解析，忽略格式不正确的路径和不存在的路径，如果代理是在 VM 启动之后某一时刻启动的，则忽略不表示 JAR 文件的路径</td></tr></tbody></table>

- - - - - -

###### **详解 agentmain()**

> - **agentmain** 为JVM启动后加载的`Java Agent`，主要通过`attach api`实现；`attach api`主要通过`VirtualMachine`和`VirtualMachineDescriptor`两个类来实现其加载`Java Agent`的功能。 
>   - **VirtualMachine** ：该类代表当前JVM连接的目标JVM进程；应用程序通过`VirtualMachine`将`Java Agent`加载到目标JVM中；
>   - 例如，用Java语言编写的探查器工具可能会连接到正在运行的应用程序，并加载其探查器代理来评测正在运行的应用程序。此外，`VirtualMachine`提供了访问目标JVM系统属性的权限。
>   - 该类允许我们通过给`attach`方法传入一个jvm的pid(`进程id`)，远程连接到jvm上；代理类注入操作只是它众多功能中的一个，通过`loadAgent`方法向jvm注册一个代理程序`agent`，在该agent的代理程序中会得到一个`Instrumentation`实例，该实例可以在`class加载前`改变class的字节码，也可以在`class加载后`重新加载。在调用`Instrumentation`实例的方法时，这些方法会使用`ClassFileTransformer`接口中提供的方法进行处理。
>   - **VirtualMachineDescriptor** ：该类是一个用于描述JVM的容器类，配合`VirtualMachine`类完成各种功能

- - - - - -

> - **attach动态注入的原理则非常简单：**
>   - 通过 **VirtualMachine.attach(pid)** 方法，可以远程连接一个正在运行的JVM进程
>   - 通过 **loadAgent(agent)** 将Java Agent的jar包注入到对应的进程中，然后对应的进程会调用`agentmain`方法
>   - 通过 **attach api** 和`agentmain`方法，我们可以很方便地在运行过程中动态设置加载代理类，在main函数开始运行之后再运行`agent`，以达到`instrumentation`的目的；相较于之前只能使用`-javaagent`参数在`main`方法之前运行的`premain`方法有了更大的扩展性，让我们修改正在运行的程序成为了可能

- - - - - -

- - - - - -

- - - - - -

##### 实战 agentmain() 的使用方法

<div style="overflow:hidden; clear:both; width: 100%; height: 40px; position: relative;">- - - - - -

 <span style="position: absolute;top: 50%;left: 50%; transform: translate(-50%, -50%); background-color: white;">以下为隐藏内容</span> </div> ###### 1. 模拟业务程序，创建`TestJavaApp.java`文件

```java
import com.sun.tools.attach.VirtualMachine;
import com.sun.tools.attach.VirtualMachineDescriptor;

import java.util.List;

public class TestJavaApp {

    public static void main(String[] args) throws Exception {

        System.out.println("我是业务程序:---> test-java-app");

        // 获取当前系统中所有 运行中的 虚拟机列表
        List<virtualmachinedescriptor> list = VirtualMachine.list();
        // 遍历所有虚拟机
        for (VirtualMachineDescriptor vmd : list) {
            // 获取虚拟机名称(也用是我们程序的名称)
            String displayName = vmd.displayName();
            // 通过虚拟机的名字来区分，要获取哪个正在运行的虚拟机
            //   使用IDEA启动的时候虚拟机的名字是 Java类名
            //   当使用 java -jar test-java-app.jar 启动的时候虚拟机的名是 test-java-app.jar文件名
            if (args.length > 0 && displayName.startsWith("test-java-app") || displayName.startsWith("TestJavaApp")) {
                // 这里的意思是，通过虚拟机的ID获取虚拟机对象
                // vmd.id() 就是我们平时使用 jps -l 查看的那个ID
                //
                // 这里有个误区，我一开始以为是只能获取当前自己的这个虚拟机，
                //   其实 VirtualMachine.attach(vmd.id()) 这个命令是能够获取当前操作系统中所有正在运行中的虚拟机，
                //   并且可以动态注入 test-java-agent.jar 中的逻辑
                VirtualMachine virtualMachine = VirtualMachine.attach(vmd.id());
                // 动态注入 test-java-agent.jar 中的逻辑，注意在测试过程中这里必须要使用绝对路径；所以考虑用参数将agent.jar的路径传进来
                // 例如：virtualMachine.loadAgent("E:/java-project/test-java-app/src/test-java-agent.jar");
                virtualMachine.loadAgent(args[0]);
                virtualMachine.detach();
            }
        }
    }
}

</virtualmachinedescriptor>
```

###### 1.1 编译、打包、执行

```ruby
## 编译 && 打包
E:\gitee-project\javaagent-example\src> javac -encoding utf-8 TestJavaApp.java && jar cfe test-java-app.jar TestJavaApp TestJavaApp.class

## 测试执行，因为引用了tools.jar所以要指定依赖工具包 -Djava.ext.dirs="%JAVA_HOME%\lib"
E:\gitee-project\javaagent-example\src> java -Djava.ext.dirs="%JAVA_HOME%\lib" -jar test-java-app.jar
我是业务程序:---> test-java-app


```

- - - - - -

###### 2.1 创建`TestJavaAgent.java`文件

```java
import java.lang.instrument.Instrumentation;

public class TestJavaAgent {

    /**
     * 该方法在业务主程序main方法之前运行，与main方法运行在同一个JVM中
     *
     * @param agentArgs
     * @param inst
     */
    public static void premain(String agentArgs, Instrumentation inst) {
        System.out.println("TestJavaAgent -------------> PRE_Main");
//        inst.addTransformer((loader, className, classBeingRedefined, protectionDomain, classfileBuffer) -> {
//            System.out.printf("TestJavaAgent_PRE_Main -------------> %s \n", className);
//            return new byte[0];
//        });
    }

    /**
     * 在业务主程序main方法执行时，可通过attach api调用该方法，与main方法运行在同一个JVM中
     *
     * @param agentArgs
     * @param inst
     */
    public static void agentmain(String agentArgs, Instrumentation inst) {
        System.out.println("TestJavaAgent ============> Agent_Main");
//        inst.addTransformer((loader, className, classBeingRedefined, protectionDomain, classfileBuffer) -> {
//            System.out.printf("TestJavaAgent_Agent_Main ============> %s \n", className);
//            return new byte[0];
//        });
    }
}


```

###### 2.2 创建`MANIFEST.MF`文件

```yaml
Manifest-Version: 1.0
Premain-Class: TestJavaAgent
Agent-Class: TestJavaAgent
Can-Redefine-Classes: true
Can-Retransform-Classes: true


```

###### 2.3 编译、打包 agent

```ruby
E:\gitee-project\javaagent-example\src> javac -encoding utf-8 TestJavaAgent.java && jar cvfm test-java-agent.jar MANIFEST.MF TestJavaAgent.class


```

- - - - - -

- - - - - -

- - - - - -

> ###### 测试执行，**静态agent**， 使用`-javaagent:`指定`agent.jar`，现象是在main函数`启动前`执行

```ruby
E:\gitee-project\javaagent-example\src> java -Djava.ext.dirs="%JAVA_HOME%\lib" -jar -javaagent:test-java-agent.jar test-java-app.jar
TestJavaAgent -------------> PRE_Main
我是业务程序:---> test-java-app


```

- - - - - -

> ###### 测试执行，**动态agent**， 使用`virtualMachine.loadAgent(args[0])`去加载`agent.jar`，现象是在main函数`启动中`执行；**注意这里不需要`-javaagent:`**

```ruby
E:\gitee-project\javaagent-example\src> java -Djava.ext.dirs="%JAVA_HOME%\lib" -jar test-java-app.jar "E:\gitee-project\javaagent-example\src\test-java-agent.jar"
我是业务程序:---> test-java-app
TestJavaAgent ============> Agent_Main


```

- - - - - -

> ###### 测试执行，**动态、静态agent** 同时使用

```ruby
E:\gitee-project\javaagent-example\src> java -Djava.ext.dirs="%JAVA_HOME%\lib" -jar -javaagent:test-java-agent.jar test-java-app.jar "E:\gitee-project\javaagent-example\src\test-java-agent.jar"
TestJavaAgent -------------> PRE_Main
我是业务程序:---> test-java-app
TestJavaAgent ============> Agent_Main

```

- - - - - -

###### **[项目地址](https://gitee.com/eric-mao/javaagent-example "项目地址")**

- - - - - -

- - - - - -

- - - - - -