---
title: "Linux 通过端口号 杀死进程"
date: "2017-11-16"
categories: 
  - "linux服务器"
---

### **应用方法**

```ruby
[root@localhost javaServer]# netstat -antp | grep 8080 | awk '{print $7}' | awk -F '/' '{print $1}' | xargs kill -9
```

### **命令解析**

**根据端口号查找进程**

```ruby
[root@localhost javaServer]# netstat -antp | grep 8080
tcp6       0      0 :::8080                 :::*                    LISTEN      6193/java
[root@localhost javaServer]#
```

**根据端口号查找进程中第7组参数**

```ruby
[root@localhost javaServer]# netstat -antp | grep 8080 | awk '{print $7}'
6193/java
[root@localhost javaServer]#
```

**使用 awk -F '/' '{print $1}' 拆分 6193/java 来获取PID**

```ruby
[root@localhost javaServer]# netstat -antp | grep 8080 | awk '{print $7}' | awk -F '/' '{print $1}'
6193
[root@localhost javaServer]#
```

**杀死获取到的PID进程**

```ruby
[root@localhost javaServer]# netstat -antp | grep 8080 | awk '{print $7}' | awk -F '/' '{print $1}' | xargs kill -9
[root@localhost javaServer]#
[root@localhost javaServer]# netstat -antp | grep 8080
[1]+  已杀死               nohup java -jar dlfc-framework-bigdata-statistical-1.0-SNAPSHOT.jar
[root@localhost javaServer]#
```
