---
title: "Docker 学习笔记(四) Docker commit 将容器保存为一个新的镜像"
date: "2017-11-16"
categories: 
  - "docker"
---

### **docker commit -m `'注释'` `容器CONTAINER ID` `镜像名称`:`镜像版本`**

### 退出容器

```ruby
[root@23c18d958279 ~]# exit
exit
[root@localhost dockerImage]#
[root@localhost dockerImage]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                       PORTS                    NAMES
23c18d958279        4a5932cd5a14        "/bin/bash"              17 minutes ago      Exited (130) 9 minutes ago                            determined_sammet
[root@localhost dockerImage]#
```

### 将容器保存为一个新的镜像

```ruby
[root@localhost dockerImage]# docker commit 23c18d958279 bigdata:v0.2
[root@localhost dockerImage]#
[root@localhost dockerImage]# docker images
REPOSITORY                              TAG                 IMAGE ID            CREATED             SIZE
bigdata                                 v0.2                715bc4108155        8 minutes ago       1.64GB
bigdata                                 v0.1                4a5932cd5a14        4 hours ago         1.64GB
registry.docker-cn.com/library/centos   7                   d123f4e55e12        4 days ago          197MB
[root@localhost dockerImage]#
```

### 运行测试

```ruby
[root@localhost dockerImage]# docker run -d -p 3000:3000 715bc4108155 /home/bigdata/start.sh
[root@localhost dockerImage]#
[root@localhost dockerImage]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                       PORTS                    NAMES
60ebba65b023        715bc4108155        "/home/bigdata/sta..."   7 minutes ago       Up 7 minutes                 0.0.0.0:3000->3000/tcp   naughty_shannon
23c18d958279        4a5932cd5a14        "/bin/bash"              17 minutes ago      Exited (130) 9 minutes ago                            determined_sammet
[root@localhost dockerImage]#
```

#### **例如: 本机的IP地址是 10.32.156.51**

#### **测试地址为: http://10.32.156.51:3000**
