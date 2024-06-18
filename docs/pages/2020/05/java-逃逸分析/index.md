---
title: "Java 逃逸分析"
date: "2020-05-29"
categories: 
  - "java"
---

##### 资料

**[对象并不一定都是在堆上分配内存的](https://blog.csdn.net/w372426096/article/details/80333657 "对象并不一定都是在堆上分配内存的")**

**[Java虚拟机的锁优化技术](https://mp.weixin.qq.com/s?__biz=MzI3NzE0NjcwMg==&mid=2650121186&idx=1&sn=248d37be27d3bbeb103464b2a96a0ae4&chksm=f36bbec3c41c37d59277ac8539a616b65ec44637f341325056e98323e8780e09c6e4f7cc7a85&scene=21#wechat_redirect "Java虚拟机的锁优化技术")**

* * *

###### 创建测试文件

```ruby
[root@test2 eric]# cat > Test.java << ERIC
public class Test {

    public static void  main(String[] args) throws InterruptedException {
        for (int i = 0; i < 1000000; i++) {
            User user = alloc();
            //System.out.print(user);
        }
        // 为了方便查看堆内存中对象个数，线程sleep
        Thread.sleep(100000);
    }

    private static User alloc() {
        User user = new User();
        return user;
    }

    static class User {

    }

}

ERIC

```

* * *

###### **`关闭`** 逃逸分析测试

```ruby
[root@test2 eric]# java -Xmx4G -Xms4G -XX:-DoEscapeAnalysis -XX:+PrintGCDetails -XX:+HeapDumpOnOutOfMemoryError Test
```

###### 查看结果

```ruby
[root@test2 ~]# jps | grep Test | awk '{print $1}' | xargs jmap -histo | head

 num     #instances         #bytes  class name
----------------------------------------------
   1:           444       26530192  [I
   2:       1000000       16000000  Test$User            # 创建了100万个对象
   3:          1669         178848  [C
   4:           241          57200  [B
   5:           494          56648  java.lang.Class
   6:          1283          30792  java.lang.String
   7:           550          27672  [Ljava.lang.Object;
[root@test2 ~]#
```

* * *

* * *

###### **`开启`** 逃逸分析测试

```ruby
[root@test2 eric]# java -Xmx4G -Xms4G -XX:+DoEscapeAnalysis -XX:+PrintGCDetails -XX:+HeapDumpOnOutOfMemoryError Test
```

###### 查看结果

```ruby
[root@test2 ~]# jps | grep Test | awk '{print $1}' | xargs jmap -histo | head

 num     #instances         #bytes  class name
----------------------------------------------
   1:           444       39804912  [I
   2:        170330        2725280  Test$User            # 一部分对象在栈中
   3:          1669         178848  [C
   4:           241          57200  [B
   5:           494          56648  java.lang.Class
   6:          1283          30792  java.lang.String
   7:           550          27672  [Ljava.lang.Object;
[root@test2 ~]#
```

* * *
