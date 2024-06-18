---
title: 'Docker 常用命令'
date: '2017-11-16T14:30:51+00:00'
status: publish
permalink: /2017/11/16/docker-%e5%b8%b8%e7%94%a8%e5%91%bd%e4%bb%a4
author: 毛巳煜
excerpt: ''
type: post
id: 382
category:
    - Docker
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### docker volume

```ruby
docker volume
Usage:  docker volume COMMAND
Commands:
  create      Create a volume
  inspect     Display detailed information on one or more volumes
  ls          List volumes
  prune       Remove all unused local volumes
  rm          Remove one or more volumes


```

- - - - - -

###### 获取`容器`或`镜像`的详细配置信息

**docker inspect `容器名|镜像名`或`容器ID|镜像ID`**  
**docker inspect 容器名 `-f {{.一级属性}}`**  
**docker inspect 容器名 `-f {{.一级属性.二级属性 ......}}`**  
**docker inspect 容器名 `-f '{{.属性}} {{.属性}}'`**  
**docker inspect 容器名 `-f {{ range .可迭代的属性}}`**  
**通常情况下，容器突然死掉，我们在想使用 `docker logs` 是无法查到容器的死亡原因，要想知道容器的死亡原因，我们可以通过 `docker inspect` 命令对死掉的容器进行解剖，找到容器生成到宿主机上的日志文件来确认宕机原因**

```ruby
# 查看容器生成的日志路径
[root@test1 ~]# docker inspect ceph-mon -f {{.LogPath}}
/var/lib/docker/containers/94649ce21c55bf718979baab95c78d3bf8a0d75d86307637bc9636043eeaa039/94649ce21c55bf718979baab95c78d3bf8a0d75d86307637bc9636043eeaa039-json.log
[root@test1 ~]#

# 查看容器启停时间
[root@test1 ~]# docker inspect ceph-mon -f '容器启动时间:{{.State.StartedAt}}  容器停止时间:{{.State.FinishedAt}}'
容器启动时间:2019-12-27T01:07:03.101063017Z  容器停止时间:0001-01-01T00:00:00Z
[root@test1 ~]#

```

`0001-01-01T00:00:00Z`表示容器正在运行中

- - - - - -

###### 查看镜像分层

```ruby
[root@test1 build]# docker images tools-os:v1.0.0
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
tools-os            v1.0.0              aade7c80d010        14 minutes ago      410MB
[root@test1 build]#
[root@test1 build]#
[root@test1 build]# docker history tools-os:v1.0.0
IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
aade7c80d010        13 minutes ago      /bin/sh -c #(nop)  CMD ["/usr/sbin/httpd" ...   0B
c19128d7a3bf        13 minutes ago      /bin/sh -c #(nop)  EXPOSE 80/tcp                0B
406b392be6a8        13 minutes ago      /bin/sh -c yum install -y epel-release tel...   207MB
ed793d100ca2        14 minutes ago      /bin/sh -c #(nop)  MAINTAINER mao_siyu@qq.com   0B
08d05d1d5859        6 weeks ago         /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B
<missing>           6 weeks ago         /bin/sh -c #(nop)  LABEL org.label-schema....   0B
<missing>           6 weeks ago         /bin/sh -c #(nop) ADD file:3e2a127b44ed01a...   204MB
[root@test1 build]#
</missing></missing>
```

###### 查看镜像分层详细信息

命令默认显示省略符号来代表被修剪的文本  
`--no-trunc` 字面意思不进行修剪

```ruby
[root@test1 build]# docker images tools-os:v1.0.0
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
tools-os            v1.0.0              aade7c80d010        14 minutes ago      410MB
[root@test1 build]#
[root@test1 build]#
[root@test1 build]# docker history --no-trunc tools-os:v1.0.0
IMAGE                                                                     CREATED             CREATED BY                                                                                                                                                                                                SIZE                COMMENT
sha256:aade7c80d01099cc9122034041c39fe78cd23bb3c48f3a233fbd5b993e6b9576   15 minutes ago      /bin/sh -c #(nop)  CMD ["/usr/sbin/httpd" "-D" "FOREGROUND"]                                                                                                                                              0B
sha256:c19128d7a3bfa6ef210689af03bd5c16c200def9aac70a3a2ac2f18b6aaa2faf   15 minutes ago      /bin/sh -c #(nop)  EXPOSE 80/tcp                                                                                                                                                                          0B
sha256:406b392be6a89ac2e8001382bc78ce829c1d86421b59cc1151788cb5955e0300   15 minutes ago      /bin/sh -c yum install -y epel-release telnet nmap net-tools httpd vim htop                                                                                                                               207MB
sha256:ed793d100ca20701399112d9a6b3867b3e75a5a1868d4ea2a42c355e8e56948b   16 minutes ago      /bin/sh -c #(nop)  MAINTAINER mao_siyu@qq.com                                                                                                                                                             0B
sha256:08d05d1d5859ebcfb3312d246e2082e46cb307f0e896c9ac097185f0b0b19e56   6 weeks ago         /bin/sh -c #(nop)  CMD ["/bin/bash"]                                                                                                                                                                      0B
<missing>                                                                 6 weeks ago         /bin/sh -c #(nop)  LABEL org.label-schema.schema-version=1.0 org.label-schema.name=CentOS Base Image org.label-schema.vendor=CentOS org.label-schema.license=GPLv2 org.label-schema.build-date=20191024   0B
<missing>                                                                 6 weeks ago         /bin/sh -c #(nop) ADD file:3e2a127b44ed01afc6e3ee70b4bdaff81d5d9df67a07740debb5c9e7760cd15b in /                                                                                                          204MB
[root@test1 build]#
</missing></missing>
```

- - - - - -

###### 查看Docker 运行内存状态

```ruby
[root@k8s-master deploy]# docker stats
CONTAINER ID        NAME                                                                                                            CPU %               MEM USAGE / LIMIT     MEM %               NET I/O             BLOCK I/O           PIDS

```

###### 查看磁盘使用空间

```ruby
[root@k8s-master deploy]# docker system df -v
# 镜像空间使用情况
Images space usage:

REPOSITORY                           TAG                 IMAGE ID            CREATED ago         SIZE                SHARED SIZE         UNIQUE SiZE         CONTAINERS
k8s.gcr.io/kube-proxy                v1.15.1             89a062da739d        3 weeks ago ago     82.41MB             42.32MB             40.09MB             1
k8s.gcr.io/etcd                      3.3.10              2c4adeb21b4f        8 months ago ago    258.1MB             0B                  258.1MB             1
k8s.gcr.io/pause                     3.1                 da86e6ba6ca1        20 months ago ago   742.5kB             0B                  742.5kB             8

# 容器空间使用情况
Containers space usage:

CONTAINER ID        IMAGE                  COMMAND                  LOCAL VOLUMES       SIZE                CREATED ago         STATUS                     NAMES
63e4b6bdba7b        ff281650a721           "cp -f /etc/kube-fla…"   0                   0B                  7 minutes ago ago   Exited (0) 7 minutes ago   k8s_install-cni_kube-flannel-ds-amd64-zfvjb_kube-system_29d93808-932c-4672-a51a-73538d874680_0
bab6bbf98bf7        eb516548c180           "/coredns -conf /etc…"   0                   0B                  2 weeks ago ago     Up 2 weeks                 k8s_coredns_coredns-5c98db65d4-2wqgw_kube-system_b6c64f3d-a933-475d-8640-c4e4a5a8c39c_1
bd0fe5a3e6c9        eb516548c180           "/coredns -conf /etc…"   0                   0B                  2 weeks ago ago     Up 2 weeks                 k8s_coredns_coredns-5c98db65d4-f7z9j_kube-system_8ce80897-9680-41fb-aff2-48cb4f9fadd8_1

# 本地卷使用情况
Local Volumes space usage:

VOLUME NAME         LINKS               SIZE

Build cache usage: 0B

[root@k8s-master deploy]#

```

###### 空间清理

Docker内置自动清理：  
通过 Docker 内置的 CLI 指令docker system prune来进行自动空间清理。

```ruby
[root@k8s-master deploy]# docker system prune --help

Usage:  docker system prune [OPTIONS]

Remove unused data

Options:
  -a, --all             Remove all unused images not just dangling ones
      --filter filter   Provide filter values (e.g. 'label=<key>=<value>')
  -f, --force           Do not prompt for confirmation
      --volumes         Prune volumes
[root@k8s-master deploy]#
[root@k8s-master deploy]#
[root@k8s-master deploy]#
[root@k8s-master deploy]#
[root@k8s-master deploy]# docker system prune
# 或
[root@k8s-master deploy]# docker system prune --all
WARNING! This will remove:
        - all stopped containers
        - all networks not used by at least one container
        - all images without at least one container associated to them
        - all build cache
Are you sure you want to continue? [y/N] y
Deleted Containers:
63e4b6bdba7bf47bb2cf64e2422a55de0f9361c1c161b1a6179e45fb36c65e1f

Total reclaimed space: 0B
[root@k8s-master deploy]#
</value></key>
```

- - - - - -

###### 删除所有为 `<none></none>` 的镜像

**`<none>:<none></none></none>`** 这种镜像在Docker官方文档中被称作 **`dangling images`** ，指的是没有标签并且没有被容器使用的镜像。

```ruby
[gitlab-runner@k8s-master ~]<span class="katex math inline">docker rmi</span>( docker images -q -f dangling=true )

```

###### 删除指定容器 为 `<none></none>` 的镜像

```ruby
[gitlab-runner@k8s-master ~]<span class="katex math inline">docker rmi</span>(docker images | grep 你的容器名 | grep none)
# 或
[gitlab-runner@k8s-master ~]$ docker images | grep 你的容器名 | grep none | xargs docker rmi

```

- - - - - -

###### Docker run 命令

**OPTIONS说明：**

1. `-a stdin`: 指定标准输入输出内容类型，可选 STDIN/STDOUT/STDERR 三项；
2. `-d`: 后台运行容器，并返回容器ID；
3. `-i`: 以交互模式运行容器，通常与 -t 同时使用；
4. `-p`: 端口映射，格式为：主机(宿主)端口:容器端口
5. `-t`: 为容器重新分配一个伪输入终端，通常与 -i 同时使用；
6. `--name="nginx-lb"`: 为容器指定一个名称；
7. `--dns 8.8.8.8`: 指定容器使用的DNS服务器，默认和宿主一致；
8. `--dns-search example.com`: 指定容器DNS搜索域名，默认和宿主一致；
9. `-h "mars"`: 指定容器的hostname；
10. `-e username="ritchie"`: 设置环境变量；
11. `--env-file=[]`: 从指定文件读入环境变量；
12. `--cpuset="0-2" or --cpuset="0,1,2"`: 绑定容器到指定CPU运行；
13. `-m`: 设置容器使用内存最大值；
14. `--net="bridge"`: 指定容器的网络连接类型，支持 bridge/host/none/container: 四种类型；
15. `--link=[]`: 添加链接到另一个容器；
16. `--expose=[]`: 开放一个端口或一组端口；

###### 语法

`docker run [OPTIONS] IMAGE [COMMAND] [ARG...]`

**实例**  
使用docker镜像nginx:latest以后台模式启动一个容器,并将容器命名为mynginx。  
`docker run --name mynginx -d nginx:latest`  
使用镜像nginx:latest以后台模式启动一个容器,并将容器的80端口映射到主机随机端口。  
`docker run -P -d nginx:latest`  
使用镜像 nginx:latest，以后台模式启动一个容器,将容器的 80 端口映射到主机的 80 端口,主机的目录 /data 映射到容器的 /data。  
`docker run -p 80:80 -v /data:/data -d nginx:latest`  
绑定容器的 8080 端口，并将其映射到本地主机 127.0.0.1 的 80 端口上。  
`docker run -p 127.0.0.1:80:8080/tcp ubuntu bash`  
使用镜像nginx:latest以交互模式启动一个容器,在容器内执行/bin/bash命令。  
`runoob@runoob:~$ docker run -it nginx:latest /bin/bash<br></br>root@b8573233d675:/#`

```ruby
[root@zhujiwu ~]# docker images
REPOSITORY                                 TAG                 IMAGE ID            CREATED             SIZE
ZE
registry.docker-cn.com/library/wordpress   l   latest              ca0fefec932b        6 days ago          409MB
[root@zhujiwu ~]# docker run -p 1888:80 -d --name="msy-wordpress" ca0fefec932b
864e11c92f1332703c6b284bc66e6bc59d50edf31005f8f35c70ecaff5763560
[root@zhujiwu ~]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                  NAMES
864e11c92f13        ca0fefec932b        "docker-entrypoint..."   5 seconds ago       Up 3 seconds        0.0.0.0:1888->80/tcp   msy-wordpress
[root@zhujiwu ~]#

```

**--------------------------------------------------------------------------------------**

##### Docker start/stop/restart 命令

docker start :启动一个或多少已经被停止的容器  
docker stop :停止一个运行中的容器  
docker restart :重启容器

###### 语法

`docker start [OPTIONS] CONTAINER [CONTAINER...]`  
`docker stop [OPTIONS] CONTAINER [CONTAINER...]`  
`docker restart [OPTIONS] CONTAINER [CONTAINER...]`

**OPTIONS说明：**  
容器名称 或 容器ID

**实例**  
启动已被停止的容器myrunoob  
`docker start myrunoob`  
停止运行中的容器myrunoob  
`docker stop myrunoob`  
重启容器myrunoob  
`docker restart myrunoob`

**--------------------------------------------------------------------------------------**

##### Docker kill 命令

docker kill :杀掉一个运行中的容器。

###### 语法

`docker kill [OPTIONS] CONTAINER [CONTAINER...]`

**OPTIONS说明：**  
1\. `-s` :向容器发送一个信号

**实例**  
杀掉运行中的容器mynginx  
`runoob@runoob:~$ docker kill -s KILL mynginx<br></br>mynginx`

**--------------------------------------------------------------------------------------**

##### Docker rm 命令

docker rm ：删除一个或多少容器

###### 语法

`docker rm [OPTIONS] CONTAINER [CONTAINER...]`

**OPTIONS说明：**  
1\. `-f` :通过SIGKILL信号强制删除一个运行中的容器  
2\. `-l` :移除容器间的网络连接，而非容器本身  
3\. `-v` :-v 删除与容器关联的卷

**实例**  
强制删除容器db01、db02  
`docker rm -f db01 db02`  
移除容器nginx01对容器db01的连接，连接名db  
`docker rm -l db`  
删除容器nginx01,并删除容器挂载的数据卷  
`docker rm -v nginx01`

**--------------------------------------------------------------------------------------**

##### Docker pause/unpause 命令

docker pause :暂停容器中所有的进程。  
docker unpause :恢复容器中所有的进程。

###### 语法

`docker pause [OPTIONS] CONTAINER [CONTAINER...]`  
`docker unpause [OPTIONS] CONTAINER [CONTAINER...]`

**实例**  
暂停数据库容器db01提供服务。  
`docker pause db01`  
恢复数据库容器db01提供服务。  
`docker unpause db01`

**--------------------------------------------------------------------------------------**

##### Docker create 命令

docker create ：创建一个新的容器但不启动它  
用法同 docker run

###### 语法

`docker create [OPTIONS] IMAGE [COMMAND] [ARG...]`  
语法同 docker run

**实例**  
使用docker镜像nginx:latest创建一个容器,并将容器命名为myrunoob  
`runoob@runoob:~$ docker create  --name myrunoob  nginx:latest<br></br>09b93464c2f75b7b69f83d56a9cfc23ceb50a48a9db7652ee4c27e3e2cb1961f`

**--------------------------------------------------------------------------------------**

##### Docker exec 命令

docker exec ：在运行的容器中执行命令

###### 语法

`docker exec [OPTIONS] CONTAINER COMMAND [ARG...]`

**OPTIONS说明：**  
1\. `-d` :分离模式: 在后台运行  
2\. `-i` :即使没有附加也保持STDIN 打开  
3\. `-t` :分配一个伪终端

**实例**  
在容器mynginx中以交互模式执行容器内/root/runoob.sh脚本  
`runoob@runoob:~$ docker exec -it mynginx /bin/sh /root/runoob.sh<br></br>http://www.runoob.com/`  
在容器mynginx中开启一个交互模式的终端  
`runoob@runoob:~$ docker exec -i -t  mynginx /bin/bash<br></br>root@b1a0703e41e7:/#`

**--------------------------------------------------------------------------------------**