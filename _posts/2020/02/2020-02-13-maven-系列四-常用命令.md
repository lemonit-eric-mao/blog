---
title: "Maven 系列四 常用命令"
date: "2020-02-13"
categories: 
  - "maven"
---

* * *

###### Maven 常用命令

```ruby
# 查看maven版本
[root@dev1 ~]# mvn -v

# 如果没有修改默认的 settings.xml文件， 需要另外指定 settings.xml 文件，写法如下
[root@dev1 ~]# mvn -s F:/maven/settings.xml clean

# 打包
[root@dev1 ~]# mvn clean package -U -D maven.test.skip=true

# 清空并下载资源
[root@dev1 ~]# mvn clean install -D maven.test.skip=true

# 指定某个项目的pom.xml文件，清空、下载资源
[root@dev1 ~]# mvn -f /home/project/yihui-mid-platform/yihui-dependencies/pom.xml clean install -D maven.test.skip=true

# 指定某个项目的pom.xml文件，清空、下载资源、打包
[root@dev1 ~]# mvn -f /home/project/yihui-mid-platform/pom.xml clean install package -U -D maven.test.skip=true

# 将项目发布到仓库
[root@dev1 ~]# mvn deploy

# 强制清除 Maven本地库。
# mvn dependency:purge-local-repository
[root@dev1 ~]# mvn clean dependency:purge-local-repository package

```

* * *

* * *

* * *
