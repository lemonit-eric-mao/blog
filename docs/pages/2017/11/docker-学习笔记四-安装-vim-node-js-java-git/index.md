---
title: "Docker 学习笔记(三) 构建简单系统，并安装常用工具"
date: "2017-11-16"
categories: 
  - "docker"
---

###### 配置 Dockerfile

```ruby
[root@test1 build]# cat > Dockerfile << eric
# 构建方法  docker build -t tools-os:v1.0.0 .

# 应用哪个仓库 承载自己的应用程序
# 注：Dockerfile 配置文件中所有的路径都是以 Dockerfile文件所在的目录为根目录
# 指定 从Docker hub, 下载 centos:7.7.1908 镜像文件
# 在打包时相当于执行了 docker pull centos:7.7.1908
FROM centos:7.7.1908

# 设置该dockerfile的作者和联系邮箱
MAINTAINER mao_siyu@qq.com

# 将Linux的一些常用工具，加入到镜像中
RUN yum install -y telnet nmap net-tools httpd

# 配置服务器端口
EXPOSE 80

CMD ["/usr/sbin/httpd", "-D", "FOREGROUND"]

eric

```

###### 构建

```ruby
[root@test1 build]# docker build -t tools-os:v1.0.0 .
[root@test1 build]#
[root@test1 build]# docker images
REPOSITORY                           TAG                 IMAGE ID            CREATED             SIZE
tools-os                             v1.0.0              7b3d382fc9ae        16 seconds ago      354 MB
[root@test1 build]#
# 测试
[root@test1 build]# docker run -dti --name tools-os -p 80:80 tools-os:v1.0.0
```
