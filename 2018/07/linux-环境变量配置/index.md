---
title: "Linux 环境变量配置"
date: "2018-07-02"
categories: 
  - "linux服务器"
---

##### 环境变量 一句话总结：程序运行时所在的环境的全局变量

所有运行在操作系统中的程序，它们使用的全局变量，就是在操作系统中被叫做环境变量，这个环境变量是可以被所有程序识别共用

* * *

###### 1 全局环境变量配置

```ruby
[root@dev1 ~]# vim /etc/profile

# java 环境变量
export JAVA_HOME=/mnt/SSD/java/jdk-8u172-linux-x64
export JRE_HOME=$JAVA_HOME/jre
export CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib
export PATH=$PATH:$JAVA_HOME/bin

# maven 环境变量
export MAVEN_HOME=/mnt/SSD/maven/apache-maven-3.5.3
export PATH=$PATH:$MAVEN_HOME/bin

# Android 环境变量
export ANDROID_HOME=/mnt/1TB/Android/Sdk/android-sdk-linux
export PATH=$PATH:$ANDROID_HOME/tools
export PATH=$PATH:$ANDROID_HOME/tools/bin
export PATH=$PATH:$ANDROID_HOME/platform-tools

# GO 环境变量
export GO_HOME=/mnt/SSD/go
export PATH=$PATH:$GO_HOME/bin

[root@dev1 ~]#
# 刷新环境变量
[root@dev1 ~]# source /etc/profile
```

* * *

###### 2 只给当前用户，配置环境变量

```ruby
cat >>  ~/.bashrc << ERIC

# java 环境变量
export JAVA_HOME=/home/deploy/java/jdk1.8.0_261
export JRE_HOME=\$JAVA_HOME/jre
export CLASSPATH=.:\$JAVA_HOME/lib:\$JRE_HOME/lib
export PATH=\$PATH:\$JAVA_HOME/bin

ERIC

[elasticsearch@test1 ~]$
```

`重新连接终端，测试是否配置成功`

* * *
