---
title: docker、kubernetes安装部署fastdfs文件集群系统
date: '2019-12-04T02:06:33+00:00'
status: publish
permalink: /2019/12/04/docker%e3%80%81kubernetes%e5%ae%89%e8%a3%85%e9%83%a8%e7%bd%b2fastdfs%e6%96%87%e4%bb%b6%e9%9b%86%e7%be%a4%e7%b3%bb%e7%bb%9f
author: 毛巳煜
excerpt: ''
type: post
id: 5176
category:
    - FastDFS
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
[fastdfs简介](https://blog.csdn.net/jiangbenchu/article/details/103372585)  
[转载](https://blog.csdn.net/jiangbenchu/article/details/99425585 "转载")

##### 一、docker部署fastdfs

fastdfs 的Dockerfile

```ruby
FROM centos:7

LABEL maintainer "luhuiguo@gmail.com"

ENV FASTDFS_PATH=/opt/fdfs \
    FASTDFS_BASE_PATH=/var/fdfs \
    PORT= \
    GROUP_NAME= \
    TRACKER_SERVER=



#get all the dependences
RUN yum install -y git gcc make

#create the dirs to store the files downloaded from internet
RUN mkdir -p <span class="katex math inline">{FASTDFS_PATH}/libfastcommon \
 && mkdir -p</span>{FASTDFS_PATH}/fastdfs \
 && mkdir <span class="katex math inline">{FASTDFS_BASE_PATH}

#compile the libfastcommon
WORKDIR</span>{FASTDFS_PATH}/libfastcommon

RUN git clone --branch V1.0.36 --depth 1 https://github.com/happyfish100/libfastcommon.git <span class="katex math inline">{FASTDFS_PATH}/libfastcommon \
 && ./make.sh \
 && ./make.sh install \
 && rm -rf</span>{FASTDFS_PATH}/libfastcommon

#compile the fastdfs
WORKDIR <span class="katex math inline">{FASTDFS_PATH}/fastdfs

RUN git clone --branch V5.11 --depth 1 https://github.com/happyfish100/fastdfs.git</span>{FASTDFS_PATH}/fastdfs \
 && ./make.sh \
 && ./make.sh install \
 && rm -rf <span class="katex math inline">{FASTDFS_PATH}/fastdfs


EXPOSE 22122 23000 8080 8888
VOLUME ["</span>FASTDFS_BASE_PATH", "/etc/fdfs"]

COPY conf/*.* /etc/fdfs/

COPY start.sh /usr/bin/

#make the start.sh executable
RUN chmod 777 /usr/bin/start.sh

ENTRYPOINT ["/usr/bin/start.sh"]
CMD ["tracker"]

```

1、创建docker-compose.yml

```ruby
version: '3.0'
services:
  tracker:
    container_name: tracker
    image: luhuiguo/fastdfs
    command: tracker # 覆盖容器启动后默认执行的命令, 支持 shell 格式和 [] 格式
    network_mode: host # 指定网络模式 (等同于 docker run --net 的作用, 在使用 swarm 部署时将忽略该选项)
    volumes:
      - /var/fdfs/tracker:/var/fdfs
  storage0:
    container_name: storage0
    image: luhuiguo/fastdfs
    command: storage
    network_mode: host
    environment: # 设置环境变量， environment 的值可以覆盖 env_file 的值 (等同于 docker run --env 的作用)
      - TRACKER_SERVER=10.1.5.85:22122
    volumes:
      - /var/fdfs/storage0:/var/fdfs
  # storage1:
  #   container_name: storage1
  #   image: luhuiguo/fastdfs
  #   command: storage
  #   network_mode: host
  #   environment:
  #     - TRACKER_SERVER=10.1.5.85:22122
  #   volumes:
  #     - /var/fdfs/storage1:/var/fdfs
  #  storage2:
  #   container_name: storage2
  #   image: luhuiguo/fastdfs
  #   command: storage
  #   network_mode: host
  #   environment:
  #     - TRACKER_SERVER=10.1.5.85:22122
  #     - GROUP_NAME=group2
  #     - PORT=24000
  #   volumes:
  #     - /var/fdfs/storage2:/var/fdfs

```

2、查看配置

```ruby
docker exec -it tracker fdfs_monitor /etc/fdfs/client.conf

```

3、验证

```ruby
root@localhost:/# echo hello>a.txt

/root@localhost:/# usr/bin/fdfs_test /etc/fdfs/client.conf upload a.txt
This is FastDFS client test program v5.11

Copyright (C) 2008, Happy Fish / YuQing

FastDFS may be copied only under the terms of the GNU General
Public License V3, which may be found in the FastDFS source kit.
Please visit the FastDFS Home Page http://www.csource.org/
for more detail.

[2019-11-13 09:16:54] DEBUG - base_path=/var/fdfs, connect_timeout=30, network_timeout=60, tracker_server_count=1, anti_steal_token=0, anti_steal_secret_key length=0, use_connection_pool=0, g_connection_pool_max_idle_time=3600s, use_storage_id=0, storage server id count: 0

tracker_query_storage_store_list_without_group:
        server 1. group_name=, ip_addr=172.160.180.46, port=23000

group_name=group1, ip_addr=172.160.180.46, port=23000
storage_upload_by_filename
group_name=group1, remote_filename=M00/00/00/wKi0Ll3LygaACOgwAAAABncc3SA568.txt
source ip address: 172.160.180.46
file timestamp=2019-11-13 09:16:54
file size=6
file crc32=1998380320
example file url: http://172.160.180.46/group1/M00/00/00/wKi0Ll3LygaACOgwAAAABncc3SA568.txt
storage_upload_slave_by_filename
group_name=group1, remote_filename=M00/00/00/wKi0Ll3LygaACOgwAAAABncc3SA568_big.txt
source ip address: 172.160.180.46
file timestamp=2019-11-13 09:16:54
file size=6
file crc32=1998380320
example file url: http://172.160.180.46/group1/M00/00/00/wKi0Ll3LygaACOgwAAAABncc3SA568_big.txt


```

查看本地文件的位置  
http://172.160.180.46/group1/M00/00/00/wKi0Ll3bji6AKxJiAAAABncc3SA697\_big.txt

```
[root@localhost ~]# cd /var/fdfs/storage0/data/00/00/wKi0Ll3bji6AKxJiAAAABncc3SA697_big.txt

```

##### 二、kubernetes部署fastdfs

fastdfs-deploy.yaml

```yml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
    name: tracker-deploy
    namespace: paas-basic
    labels:
        name: tracker-deploy
spec:
    replicas: 1
    template:
        metadata:
            labels:
                app: tracker
        spec:
            nodeSelector:
              fastdfs: "tracker"
            terminationGracePeriodSeconds: 0
            containers:
            - name: tracker
              image: luhuiguo/fastdfs
              imagePullPolicy: Always
              ports:
              - containerPort: 22122
              - containerPort: 23000
              - containerPort: 8080
              - containerPort: 8888
              volumeMounts:
              - name: tracker-volume
                mountPath: /var/fdfs
              command: ["/usr/bin/start.sh","tracker"]
            volumes:
            - name: tracker-volume
              hostPath:
                path: /home/data/fastdfs/tracker

---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
    name: storage0-deploy
    namespace: paas-basic
    labels:
        name: storage0-deploy
spec:
    replicas: 1
    template:
        metadata:
            labels:
                app: storage0
        spec:
            nodeSelector:
              fastdfs: "storage0"
            terminationGracePeriodSeconds: 0
            containers:
            - name: storage0
              image: luhuiguo/fastdfs
              imagePullPolicy: Always
              ports:
              - containerPort: 22122
              - containerPort: 23000
              - containerPort: 8080
              - containerPort: 8888
              volumeMounts:
              - name: storage0-volume
                mountPath: /var/fdfs
              env:
              - name: TRACKER_SERVER
                value: 10.96.0.110:22122
              command: ["/usr/bin/start.sh","storage"]
            volumes:
            - name: storage0-volume
              hostPath:
                path: /home/data/fastdfs/storage0

```

fastdfs-service.yaml

```yml
apiVersion: v1
kind: Service
metadata:
    name: tracker
    labels:
        app: tracker
    namespace: paas-basic
spec:
    selector:
        app: tracker
    type: NodePort
    clusterIP: 10.96.0.110
    ports:
    - name: "22122"
      port: 22122
      targetPort: 22122
      protocol: TCP
    - name: "23000"
      port: 23000
      targetPort: 23000
      protocol: TCP
    - name: "8080"
      port: 8080
      targetPort: 8080
      protocol: TCP
    - name: "8888"
      port: 8888
      targetPort: 8888
      protocol: TCP


```

[storage.conf配置文件](https://blog.csdn.net/jiangbenchu/article/details/103255600)  
[tracker.conf配置文件](https://blog.csdn.net/jiangbenchu/article/details/103255576)  
l[uhuiguo/fastdfs镜像参考](https://github.com/luhuiguo/fastdfs-docker/blob/master/docker-compose.yml)  
[season/fastdfs镜像参考](https://blog.csdn.net/wufewu/article/details/84801600)  
[其他参考1](https://blog.csdn.net/jk418756/article/details/94454337)