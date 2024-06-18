---
title: "docker-compose 构建项目"
date: "2019-07-16"
categories: 
  - "linux服务器"
---

##### docker-compose.yml

```yaml
version: "2"
services:
  resource-manage-server:
    # 容器启名
    container_name: resource-manage-server
    # 镜像名:镜像TAG
    image: resource-manage-server:v20190716-1616
    build:
      # 打包 Dockerfile 文件所在的当前目录下所有文件
      context: .
      # 默认不写 dockerfile, 文件位置会指定 docker-compose.yml文件所在目录进行查找
      dockerfile: ./Dockerfile
      args:
        - port=8086
```

##### 运行

```ruby
[root@k8s-master resource-manage-server]# docker-compose build
Building resource-manage-server
Step 1/8 : FROM node:slim
 ---> d9bfca6c7741
Step 2/8 : MAINTAINER mao_siyu@qq.com
 ---> Using cache
 ---> 4bafed5a29b4
Step 3/8 : RUN mkdir -p /usr/src/app
 ---> Using cache
 ---> 16ba3ab59bb7
Step 4/8 : WORKDIR /usr/src/app
 ---> Using cache
 ---> 24c4fa22c2b5
Step 5/8 : COPY . /usr/src/app
 ---> 12bfa82661d8
Step 6/8 : EXPOSE 8066
 ---> Running in 4ccc02fc138b
Removing intermediate container 4ccc02fc138b
 ---> a7fbaf4fe84e
Step 7/8 : RUN npm install
 ---> Running in a874b25dde2e
added 119 packages from 105 contributors and audited 256 packages in 7.671s
found 0 vulnerabilities

Removing intermediate container a874b25dde2e
 ---> ef225fbc8495
Step 8/8 : CMD ["npm", "start"]
 ---> Running in 05f20893254a
Removing intermediate container 05f20893254a
 ---> a9fb9b465bd2
[Warning] One or more build-args [port] were not consumed
Successfully built a9fb9b465bd2
Successfully tagged resource-manage-server:v20190716-1616

[root@k8s-master resource-manage-server]#
```

##### 查看镜像

```ruby
[root@k8s-master resource-manage-server]# docker images
REPOSITORY                              TAG                        IMAGE ID            CREATED             SIZE
resource-manage-server                  v20190716-1616             a9fb9b465bd2        29 seconds ago      163MB

[root@k8s-master resource-manage-server]#
```
