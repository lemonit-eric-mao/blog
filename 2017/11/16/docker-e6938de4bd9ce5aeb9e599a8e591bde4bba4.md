---
title: 'Docker 操作容器命令'
date: '2017-11-16T14:33:08+00:00'
status: publish
permalink: /2017/11/16/docker-%e6%93%8d%e4%bd%9c%e5%ae%b9%e5%99%a8%e5%91%bd%e4%bb%a4
author: 毛巳煜
excerpt: ''
type: post
id: 384
category:
    - Docker
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
#### 针对容器的操作

##### 在容器外面执行，容器内部命令

`docker exec 容器ID /bin/bash -c '要在容器内部执行的命令'`

```ruby
docker exec 237ed84f395b /bin/bash -c 'ls /var/log/apps/ | grep -E "2020-03-13.log"'

```

- - - - - -

- - - - - -

##### 获取docker容器的 环境变量

`docker exec -it [容器名 或 容器ID] env`

```ruby
[root@dev4 ~]# docker exec -it storage2 env
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=dev4
TERM=xterm
TRACKER_SERVER=172.160.180.9:22122
GROUP_NAME=group2
PORT=22222
FASTDFS_PATH=/opt/fdfs
FASTDFS_BASE_PATH=/var/fdfs
HOME=/root
[root@dev4 ~]#

```

- - - - - -

- - - - - -

##### 进入容器

`docker exec -it 容器id /bin/bash`

```ruby
[root@zhujiwu home]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                  NAMES
bf8397bba3bb        41e689eea0cd        "docker-entrypoint..."   2 weeks ago         Up 2 weeks          0.0.0.0:1888->80/tcp   thirsty_dubinsky
[root@zhujiwu home]# docker exec -it bf8397bba3bb bash
root@bf8397bba3bb:/var/www/html#

```

- - - - - -

- - - - - -

##### 将本地文件复制到 docker 容器中

`在宿主机上 docker cp 文件 容器id:容器内部的路径`

```ruby
[root@zhujiwu home]# ll
-rw-r--r--   1 root     root     10960 9月  19 15:46 wp4tozbp.php
[root@zhujiwu home]# docker cp wp4tozbp.php 13603:/var/www/html
Error response from daemon: No such container: 13603
[root@zhujiwu home]# docker cp wp4tozbp.php bf8397bba3bb:/var/www/html
[root@zhujiwu home]# docker exec -it bf8397bba3bb /bin/bash
root@bf8397bba3bb:/var/www/html# ls
wp4tozbp.php
root@bf8397bba3bb:/var/www/html#

```

- - - - - -

- - - - - -

##### Docker外网映射

`docker run -ti -p 宿主机端口:容器内部端口 镜像ID`

```ruby
[root@localhost maosiyu]# docker images
REPOSITORY               TAG                 IMAGE ID            CREATED             SIZE
das                      0.2                 e0823ecf5b59        2 hours ago         668 MB
das                      0.1                 16aca81758ac        2 hours ago         683.7 MB
mao                      0.2                 caf85778b164        2 hours ago         656.8 MB
newimage                 latest              5ae4c4bebdd7        23 hours ago        656.8 MB
docker.io/nano/node.js   0.10                a203b48dacfe        6 weeks ago         14.48 MB
daocloud.io/node         5                   12b4a63115bc        5 months ago        648 MB

[root@localhost maosiyu]# docker run -ti e0823ecf5b59                     ## 运行一个新docker容器

[root@localhost ~]# docker ps -a                                          ## 查看运行状态 PORTS=0.0.0.0:8000/tcp
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS                    NAMES
c50a9c160f93        e0823ecf5b59        "npm start"         10 minutes ago      Up 10 minutes       0.0.0.0:8000/tcp   kickass_bohr

[root@localhost ~]# netstat -untlp                                        ## 问题：本机中的8000端口并没有程序使用，外网肯定无法访问
Active Internet connections (only servers)
Proto   Recv-Q   Send-Q   Local Address           Foreign Address         State       PID/Program name
tcp          0        0   0.0.0.0:3306            0.0.0.0:*               LISTEN      3038/mysqld
tcp          0        0   0.0.0.0:22              0.0.0.0:*               LISTEN      1018/sshd
tcp          0        0   127.0.0.1:25            0.0.0.0:*               LISTEN      2420/master
tcp6         0        0   :::22                   :::*                    LISTEN      1018/sshd
tcp6         0        0   ::1:25                  :::*                    LISTEN      2420/master

[root@localhost maosiyu]# docker run -ti -p 8000:8000 e0823ecf5b59        ## 运行一个新docker容器并进行外网映射

[root@localhost ~]# docker ps -a                                          ## 查看运行状态 PORTS=0.0.0.0:8000->8000/tcp 这里变化了
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS                    NAMES
c50a9c160f93        e0823ecf5b59        "npm start"         10 minutes ago      Up 10 minutes       0.0.0.0:8000->8000/tcp   kickass_bohr

[root@localhost ~]# netstat -untlp                                        ## 解决：已经可以看到8000端口的存在了，外网可以访问了
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:3306            0.0.0.0:*               LISTEN      3038/mysqld
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      1018/sshd
tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN      2420/master
tcp6       0      0 :::22                   :::*                    LISTEN      1018/sshd
tcp6       0      0 ::1:25                  :::*                    LISTEN      2420/master
tcp6       0      0 :::8000                 :::*                    LISTEN      3965/docker-proxy-c

```

- - - - - -

- - - - - -

##### 将本地镜像发布到 Docker云服

```ruby
[root@localhost maosiyu]# docker images                                   ## 查看镜像
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
das                 0.1                 d126ed11f0cf        2 hours ago         681.3 MB
daocloud.io/node    5                   12b4a63115bc        5 months ago        648 MB
[root@localhost maosiyu]#


[root@localhost maosiyu]# docker tag das:0.1 maosiyu/das:0.1              ## 添加版本信息
[root@localhost maosiyu]# docker push maosiyu/das:0.1                     ## 将镜像发布到云服
The push refers to a repository [docker.io/maosiyu/das]
5b4bb8ba90b2: Pushed
832c14d617e3: Pushed
2715876fd822: Pushed
60e6c2d9d442: Pushed
2101d3c01933: Pushed
751f5d9ad6db: Pushed
17587239b3df: Pushed
9e63c5bce458: Pushed
0.1: digest: sha256:eefc63f0b8e0413a381f46516fa96814646b2e0ca894dfaf355127721e9fe835 size: 2009


```

- - - - - -

- - - - - -

##### **`容器`**导出

```
服务器1: 10.32.156.55
服务器2: 10.32.156.56

```

```ruby
服务器1:
[root@localhost maosiyu]# docker ps -a                                    ## 查看容器
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
9424ba9e9f72        05e8e4cd8e2b        "npm start"         13 minutes ago      Created                                 modest_jones
[root@localhost maosiyu]# docker export 9424ba9e9f72 > das-0.4.tar        ## 导出容器
[root@localhost maosiyu]# ls
das-0.4.tar
[root@localhost maosiyu]#                                                 ## 将文件推送到远程服务器
[root@localhost maosiyu]# scp -P 22 das-0.4.tar root@10.32.156.56:/home/mao_siyu/
root@10.32.156.56's password:
das-0.4.tar                                                   100%  655MB 218.5MB/s   00:03
[root@localhost maosiyu]#

```

- - - - - -

##### **`容器`**导入到镜像

```ruby
服务器2:
[root@localhost mao_siyu]# ls
das-0.4.tar
[root@localhost mao_siyu]# cat das-0.4.tar | docker import - das:0.4      ## 将容器导入到镜像
sha256:64cdba8483b608a2edbf209c2a86580162b741fbcb7a5ef67424303f42523e47
[root@localhost mao_siyu]# docker images                                  ## 这里会发现文件变小了, 原因是这个镜像只是个单纯的容器,
[root@localhost mao_siyu]#                                                ## 没有了之前容器中的项目(所以这种以容器导出的文件, 只能用在重新创建一个新的镜像)
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
das                 0.4                 64cdba8483b6        8 seconds ago       663.2 MB
[root@localhost mao_siyu]#


```

- - - - - -

- - - - - -

##### **`镜像`**[导出](https://docs.docker.com/engine/reference/commandline/save/#save-an-image-to-a-targz-file-using-gzip "导出")

**docker save -o 打包的文件名.tar 镜像名称:版本号**  
**将多个image 导出到一个压缩文件中： `docker save calico/cni:v3.15.1 mariadb:10.5.4 | gzip > eric.docker`**

```ruby
服务器1:
[root@localhost maosiyu]# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
das                 0.4                 05e8e4cd8e2b        About an hour ago   668.3 MB
daocloud.io/node    5                   12b4a63115bc        5 months ago        648 MB

[root@localhost maosiyu]# docker save -o das-0.4.tar das:0.4                 ## 保存镜像
# 或者
[root@localhost maosiyu]# docker das:0.4 > das-0.4.tar                       ## 保存镜像
[root@localhost maosiyu]#                                                    ## 将文件推送到远程服务器
[root@localhost maosiyu]# scp -P 22 das-0.4.tar root@10.32.156.56:/home/mao_siyu/
root@10.32.156.56's password:
das-0.4.tar                                                   100%  661MB 220.2MB/s   00:03
[root@localhost maosiyu]#

```

- - - - - -

##### **`镜像`**导入

**docker load -i 打包的文件名.tar**

```ruby
服务器2:
[root@localhost mao_siyu]# ls
das-0.4.tar
[root@localhost mao_siyu]# docker load -i das-0.4.tar
# 或者
[root@localhost maosiyu]# docker load ]   131 MB/131 MB
17587239b3df: Loading layer [==================================================>] 45.18 MB/45.18 MB
751f5d9ad6db: Loading layer [==================================================>] 126.6 MB/126.6 MB
2101d3c01933: Loading layer [==================================================>] 326.1 MB/326.1 MB
60e6c2d9d442: Loading layer [==================================================>] 86.02 kB/86.02 kB
2715876fd822: Loading layer [==================================================>] 40.07 MB/40.07 MB
7233651dc130: Loading layer [==================================================>]  23.6 MB/23.6 MB
Loaded image: das:0.4
[root@localhost mao_siyu]#

```

- - - - - -

- - - - - -

- - - - - -