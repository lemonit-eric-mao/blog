---
title: "Centos7 安装JDK"
date: "2018-03-15"
categories: 
  - "centos"
  - "java"
---

###### 下载

```ruby
mkdir -p /home/deploy/java/
wget -P /home/deploy/java/ http://qiniu.dev-share.top/jdk-8u261-linux-x64.tar.gz
#wget -P /home/deploy/java/ http://qiniu.dev-share.top/jdk-11.0.12_linux-x64_bin.tar.gz
#wget -P /home/deploy/java/ http://qiniu.dev-share.top/jdk-17_linux-x64_bin.tar.gz

cd /home/deploy/java/
tar -zxvf jdk-8u261-linux-x64.tar.gz
cd jdk1.8.0_261/
```

* * *

###### **`全局`** 用户添加 java 环境变量

```ruby
cat >> /etc/profile << ERIC
# Java 环境变量
export JAVA_HOME=$PWD/
export JRE_HOME=\$JAVA_HOME/jre
export CLASSPATH=.:\$JAVA_HOME/lib:\$JRE_HOME/lib
export PATH=\$PATH:\$JAVA_HOME/bin

ERIC

# 刷新
source /etc/profile

```

* * *

###### **`当前`** 用户添加 java 环境变量

```ruby
cat >> ~/.bashrc << ERIC
# Java 环境变量
export JAVA_HOME=$PWD/
export JRE_HOME=\$JAVA_HOME/jre
export CLASSPATH=.:\$JAVA_HOME/lib:\$JRE_HOME/lib
export PATH=\$PATH:\$JAVA_HOME/bin

ERIC

```

* * *
