---
title: 'K8s 部署node.js'
date: '2019-05-28T05:46:09+00:00'
status: publish
permalink: /2019/05/28/k8s-%e9%83%a8%e7%bd%b2node-js
author: 毛巳煜
excerpt: ''
type: post
id: 4693
category:
    - Kubernetes
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### node.js 服务器 resource-manage-server

```ruby
.
├── app.js
├── bin
│   └── www
├── common
│   ├── DynamicRouter.js
│   └── Tools.js
├── database
│   └── Mysql.js
├── Dockerfile
├── exception-log
│   └── ExceptionLog.js
├── package.json
├── package-lock.json
├── public
│   └── favicon.ico
├── routes
│   ├── index.js
│   ├── RouteCourt.js
│   ├── RouteCourtReserve.js
│   └── RouteLogin.js
├── server-api
│   ├── court-page
│   │   ├── court.js
│   │   └── courtReserve.js
│   └── login-page
│       └── login.js
└── views
    ├── error.html
    └── index.html

10 directories, 19 files
[root@k8s-master resource-manage-server]#

```

##### 构建Dockerfile

```ruby
# 进入 Node.js项目根目录
[root@k8s-master resource-manage-server]# pwd
/home/deploy/resource-manage-server
# 创建 Dockerfile文件
[root@k8s-master resource-manage-server]# vim Dockerfile

```

```bash
# 应用哪个仓库 承载自己的应用程序
# 注：Dockerfile 配置文件中所有的路径都是以 Dockerfile文件所在的目录为根目录
# 指定 从Docker hub, 下载 node:lts-alpine 镜像文件
# 在打包时相当于执行了 docker pull node:lts-alpine
FROM node:lts-alpine

# 设置该dockerfile的作者和联系邮箱
MAINTAINER mao_siyu@qq.com

# RUN mkdir -p 用于在Image里创建一个文件夹，将来用于保存我们的代码
RUN mkdir -p /usr/src/app

# WORKDIR 是将我们创建的文件夹做为工作目录
WORKDIR /usr/src/app

# COPY是把本机当前目录下的所有文件拷贝到Image的工作目录下
COPY . /usr/src/app

# 配置服务器端口
EXPOSE 8066

# 初始化项目
RUN npm install

# 最后 配置启动项目的命令
CMD ["npm", "start"]

```

##### 将程序构建成镜像

```ruby
[root@k8s-master resource-manage-server]# docker build -t resource-manage-server:v1.0 .
Sending build context to Docker daemon  260.6kB
Step 1/7 : FROM registry.docker-cn.com/library/node:lts-alpine
Get https://registry.docker-cn.com/v2/: net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)
[root@k8s-master resource-manage-server]# vim Dockerfile
[root@k8s-master resource-manage-server]# docker build -t resource-manage-server:v1.0 .
Sending build context to Docker daemon  260.6kB
Step 1/7 : FROM node:lts-alpine
lts-alpine: Pulling from library/node
743f2d6c1f65: Pull complete
89252b028f01: Pull complete
eb3d04625da7: Pull complete
28c10f68f928: Pull complete
Digest: sha256:27632ad2313c749e0faa02f1ce8bb1e5cb691fd607899c90eeb0477a52e94330
Status: Downloaded newer image for node:lts-alpine
 ---> fb3f89cc0eb5
Step 2/7 : RUN mkdir -p /usr/src/app
 ---> Running in 2bf88a75ea44
Removing intermediate container 2bf88a75ea44
 ---> 0b7f22a24857
Step 3/7 : WORKDIR /usr/src/app
Removing intermediate container 0cca14215626
 ---> c5e01cf9b59b
Step 4/7 : COPY . /usr/src/app
 ---> 04b25e5421e6
Step 5/7 : EXPOSE 8066
 ---> Running in 73dfe14b1ef9
Removing intermediate container 73dfe14b1ef9
 ---> aa0bd315b8f7
Step 6/7 : RUN npm install
 ---> Running in 8e1de30029c7
added 119 packages from 105 contributors and audited 256 packages in 4.613s
found 0 vulnerabilities

Removing intermediate container 8e1de30029c7
 ---> 16756403bc3d
Step 7/7 : CMD ["npm", "start"]
 ---> Running in 92508738f344
Removing intermediate container 92508738f344
 ---> 7be1c94836f0
Successfully built 7be1c94836f0
Successfully tagged resource-manage-server:v1.0
[root@k8s-master resource-manage-server]# docker images
REPOSITORY                           TAG                 IMAGE ID            CREATED             SIZE
resource-manage-server               v1.0                7be1c94836f0        30 minutes ago      164MB
node                                 lts-alpine                fb3f89cc0eb5        4 days ago          152MB
......
[root@k8s-master resource-manage-server]#

```

##### 将打好的镜像同步的工作节点的 本地 Docker中

```ruby
[root@k8s-master deploy]# docker save -o node-server.tar resource-manage-server:v1.0
[root@k8s-master deploy]#
[root@k8s-master deploy]# ansible nodes -m copy -a 'src=/home/deploy/node-server.tar dest=/home/deploy'
[root@k8s-master deploy]#
[root@k8s-master deploy]# ansible nodes -m shell -a 'docker load -i /home/deploy/node-server.tar'

```

##### yaml文件的放置目录

```ruby
[root@k8s-master node-server-yaml]# mkdir -p /home/deploy/node-server-yaml
[root@k8s-master node-server-yaml]#

```

##### 创建名称空间 node-namespace.yaml

```ruby
[root@k8s-master node-server-yaml]# cat > node-namespace.yaml 
```

##### 创建Pod的 yaml文件 node-deployment.yaml

```ruby
[root@k8s-master node-server-yaml]# cat > node-deployment.yaml 
```

##### 创建 Service的 yaml文件 node-service.yaml

```ruby
[root@k8s-master node-server-yaml]# cat > node-service.yaml 
```

##### 容器部署

```ruby
# 注意这里执行的可是 node-server-yaml/文件夹下所有的 yaml文件
[root@k8s-master deploy]# kubectl apply -f node-server-yaml/
namespace/resource-manage-server created
deployment.apps/nodejs-pod-name created
service/nodejs-service-name created

[root@k8s-master deploy]#

```

##### 容器删除

```ruby
# 注意这里执行的可是 node-server-yaml/文件夹下所有的 yaml文件
[root@k8s-master deploy]# kubectl delete -f node-server-yaml/
namespace "resource-manage-server" deleted
deployment.apps "nodejs-pod-name" deleted
service "nodejs-service-name" deleted
[root@k8s-master deploy]#

```

##### 查看运行状态

```ruby
[root@k8s-master deploy]# kubectl describe service -n resource-manage-server
Name:                     nodejs-service-name
Namespace:                resource-manage-server
Labels:                   name=nodejs-service-label
Annotations:              kubectl.kubernetes.io/last-applied-configuration:
                            {"apiVersion":"v1","kind":"Service","metadata":{"annotations":{},"labels":{"name":"nodejs-service-label"},"name":"nodejs-service-name","na...
Selector:                 app=nodejs-pod-label
Type:                     NodePort
IP:                       10.108.72.192
Port:                     http  80/TCP
TargetPort:               8066/TCP
NodePort:                 http  31542/TCP
Endpoints:                10.244.1.10:8066,10.244.2.9:8066
Session Affinity:         None
External Traffic Policy:  Cluster
Events:                   <none>

[root@k8s-master deploy]
# 通过Service访问服务器
[root@k8s-master deploy]# curl 10.98.213.234:30808
curl 10.108.72.192



    <meta charset="UTF-8"></meta>
    <title>测试页面</title>
    <style>
        body {
            margin: 0px;
            padding: 0px;
            display: flex;
            /*&#27700;&#24179;&#23621;&#20013;*/
            justify-content: center;
            /*&#22402;&#30452;&#23621;&#20013;*/
            align-items: center;
            /*&#22402;&#30452;&#26041;&#21521;&#25490;&#21015;*/
            flex-direction: column;
        }
    </style>


<h1>1024 Hello world!</h1>
<img decoding="async" src="favicon.ico"></img>


[root@k8s-master deploy]#
</none>
```