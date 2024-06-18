---
title: 'Maven 系列四 常用命令'
date: '2020-02-13T02:48:53+00:00'
status: publish
permalink: /2020/02/13/maven-%e7%b3%bb%e5%88%97%e5%9b%9b-%e5%b8%b8%e7%94%a8%e5%91%bd%e4%bb%a4
author: 毛巳煜
excerpt: ''
type: post
id: 5254
category:
    - Maven
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
- - - - - -

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

- - - - - -

- - - - - -

- - - - - -