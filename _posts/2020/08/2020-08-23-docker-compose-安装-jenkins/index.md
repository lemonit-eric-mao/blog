---
title: "docker-compose 安装 Jenkins"
date: "2020-08-23"
categories: 
  - "linux服务器"
---

###### **[官网](https://www.jenkins.io/zh/ "官网")**

###### **[官网推荐Docker 安装所有插件版](https://www.jenkins.io/doc/book/installing/#downloading-and-running-jenkins-in-docker "官网推荐Docker 安装所有插件版")**

* * *

###### 创建目录

```ruby
mkdir -p /home/deploy/jenkins/volumes/jenkins-certs/
mkdir -p /home/deploy/jenkins/volumes/jenkins-home/ && cd /home/deploy/jenkins/
```

* * *

###### 创建 compose文件

```ruby
cat > /home/deploy/jenkins/docker-compose.yaml << ERIC
version: '3.1'

services:

  jenkins:
    image: jenkinsci/blueocean:1.23.2
    restart: always
    privileged: true
    # 这里必须要指定root用户，否则它默认使用 jenkins用户执行，会导致权限不足，启动失败
    user: root
    container_name: jenkins
    ports:
      - 8866:8080 # 宿主机端口:容器内端口
    volumes:
      # 容器与宿主机时间同步
      - /etc/localtime:/etc/localtime
      - /var/run/docker.sock:/var/run/docker.sock
      - ./volumes/jenkins-certs:/certs/client
      - ./volumes/jenkins-home:/var/jenkins_home
    environment:
      TIME_ZONE: Asia/Shanghai

ERIC

```

* * *

###### 启动

```ruby
docker-compose up -d

# 等待程序成功启动后，获取登录密码
cat volumes/jenkins-home/secrets/initialAdminPassword

```

* * *

###### web访问

http://172.0.0.1:8866

* * *

###### 配置 shell 命令

```shell
# 跳过shell执行错误
set +e
npm i
npm run build:prod
docker build -t web:v1.0.0 .
docker stop web
docker run --rm -dit --name=web -p 8099:8080 web:v1.0.0

```

* * *

* * *

* * *

###### 问题

**使用docker安装的Jenkins 构建项目的执行命令肯定是在 docker容器中执行的，那么打好的包要怎么传出来？** 1 打docker镜像 可以通过`/var/run/docker.sock` 直接操作本地docker 2 打docker镜像 通过IP上传到远程的Harbor 3 打进制包 这个发送到其它服务器还可以，但是要在本机上运行进制包，就比较困难，因为拿不出来这个包

* * *

* * *

* * *
