---
title: 'Maven 系列二 Docker-Compose 部署Nexus私服仓库'
date: '2018-11-29T07:29:24+00:00'
status: publish
permalink: /2018/11/29/maven-%e7%b3%bb%e5%88%97%e4%ba%8c-docker-compose-%e9%83%a8%e7%bd%b2nexus%e7%a7%81%e6%9c%8d%e4%bb%93%e5%ba%93
author: 毛巳煜
excerpt: ''
type: post
id: 3332
category:
    - Docker
    - Maven
    - Nexus
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### **[DockerHub](https://hub.docker.com/r/sonatype/nexus3/tags "DockerHub")**

- - - - - -

###### Docker-Compose 部署Nexus私服

```ruby
mkdir -p /home/deploy/nexus/ && cd /home/deploy/nexus/

cat > docker-compose.yaml 
```

- - - - - -

###### 访问 web页面

http://192.168.20.91:8081/  
admin  
管理员密码在这个文件目录下 `./nexus-data/admin.password`

- - - - - -

###### **`重点`： 让Maven 优先使用本地Nexus私服， 然后在Nexus私服中配置如何访问阿里云镜像仓库**

**步骤如下：**  
Repository --&gt; Repositories --&gt; Select Recipe --&gt; Create Repository: maven2 (proxy)

![](http://qiniu.dev-share.top/image/maven-aliyun-proxy.png)

- - - - - -

- - - - - -

- - - - - -

###### 修改maven 配置文件settings.xml

```
<pre data-language="XML">```markup
<?xml version="1.0" encoding="UTF-8"??>

<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemalocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd">

    
    <servers>
        <server>
            <id>local-nexus-userid</id>
            <username>admin</username>
            <password>rd123456</password>
        </server>
    </servers>

    
    <mirrors>

        
        <mirror>
            
            <id>local-nexus-userid</id>
            <mirrorof>nexus-snapashots,nexus-releases,central</mirrorof>
            <name>Local Nexus aliyun</name>
            
            <url>http://192.168.20.91:8081/repository/aliyun-proxy/</url>
        </mirror>

    </mirrors>

    
    <localrepository>/home/deploy/maven/repository</localrepository>

</settings>


```
```

- - - - - -

- - - - - -

- - - - - -