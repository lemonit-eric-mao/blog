---
title: "Docker In Docker (一) 入门篇"
date: "2020-03-23"
categories: 
  - "docker"
---

###### 资料

[参考资料](https://www.jianshu.com/p/43ffba076bc9 "参考资料")

  默认情况下，Docker守护进程会生成一个socket（`/var/run/docker.sock`）文件来进行本地进程通信，而不会监听任何端口，因此只能在本地使用docker客户端或者使用Docker API进行操作。   一般情况下，我们访问本机的服务往往通过 127.0.0.1:8080 这种IP：端口的网络地址方式进行通信，而sock文件是 UNIX 域套接字（`UNIX domain socket`），它可以通过文件系统（而非网络地址）进行寻址和访问的套接字。

  从表象上看，上面的命令似乎依然是在`Docker里面run docker`，其实这是个误区。 `docker run`提供了 `-v` 参数让我们将宿主的文件映射到docker里面。   如通过 `-v /var/run/docker.sock:/var/run/docker.sock`，将`宿主Docker的Docker Daemon的socket`映射到你的Docker容器里面；   当`Container里面的docker客户端`通过 `/var/run/docker.sock` 去操作`Docker Daemon`时，实际上操作的是`宿主的Docker Daemon`。

  直白的说，`Docker Daemon`默认监听的是`/var/run/docker.sock`这个文件，所以`Docker客户端`只要把请求发往这里，`Docker服务端`就能收到并且做出响应。

* * *

* * *

##### 通过案例来讲解 `/var/run/docker.sock` 的作用

###### 使用HTTP协议 来创建容器

```ruby
[root@test2 ~]# curl -X POST --unix-socket /var/run/docker.sock -d '{"Image":"docker:stable"}' -H 'Content-Type: application/json' http://localhost/containers/create
{"Id":"652bab373be749207828c7c8e306bb7412ab7ec5ca8fc2d4a72fdbaa379630b7","Warnings":null}
[root@test2 ~]#

[root@test2 ~]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
652bab373be7        docker:stable       "docker-entrypoint.s…"   7 seconds ago       Created                                 confident_brahmagupta
[root@test2 ~]#
```

###### 启动容器

`curl -X POST --unix-socket /var/run/docker.sock http://localhost/containers/容器ID/start`

```ruby
[root@test1 ~]# curl -X POST -D --unix-socket /var/run/docker.sock http://localhost/containers/652bab373be7/start
```

* * *

* * *

* * *

###### 使用Docker命令 创建`绑定Docker Daemon的`容器

```ruby
[root@test1 ~]# docker run -v /var/run/docker.sock:/var/run/docker.sock --name docker-dind -itd docker:stable
```

###### 在容器内部执行的 docker 命令都是用来操作宿主Docker的

```ruby
[root@test1 ~]# docker exec docker-dind 命令
```

* * *

* * *

* * *

##### 实际操作

###### 封装 部署程序脚本到 docker 镜像

```ruby
[root@test1 ~]# cat > Dockerfile << ERIC
# 构建方法  docker build -t deploy:1.0.0 .

# 应用哪个仓库 承载自己的应用程序
# 注：Dockerfile 配置文件中所有的路径都是以 Dockerfile文件所在的目录为根目录
# 指定 从Docker hub, 下载 centos:7.7.1908 镜像文件
# 在打包时相当于执行了 docker pull centos:7.7.1908
FROM centos:7.7.1908

# 设置该dockerfile的作者和联系邮箱
MAINTAINER mao_siyu@qq.com

# 复制本地文件到镜像
COPY rabbitmq.yml /rabbitmq.yml

# 给镜像中安装工具
RUN yum install -y epel-release net-tools vim htop && \
    curl -L https://get.daocloud.io/docker/compose/releases/download/1.24.1/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

ERIC

[root@test1 ~]#
```

```ruby
[root@test1 ~]# docker run \
                -v /var/run/docker.sock:/var/run/docker.sock \
                --name deploy-hengrui \
                -itd \
                deploy:1.0.0
```

```ruby
[root@test1 ~]# docker exec deploy-hengrui docker-compose -v
```

* * *

* * *

* * *

###### [Docker In Docker (二) Docker客户端，访问远程Docker主机](http://www.dev-share.top/2020/03/24/docker-in-docker-%E4%BA%8C-docker%E5%AE%A2%E6%88%B7%E7%AB%AF%EF%BC%8C%E8%AE%BF%E9%97%AE%E8%BF%9C%E7%A8%8Bdocker%E4%B8%BB%E6%9C%BA/ "Docker In Docker (二) Docker客户端，访问远程Docker主机")
