---
title: 'Docker镜像 多层构建'
date: '2020-05-26T03:33:30+00:00'
status: publish
permalink: /2020/05/26/docker%e9%95%9c%e5%83%8f-%e5%a4%9a%e5%b1%82%e6%9e%84%e5%bb%ba
author: 毛巳煜
excerpt: ''
type: post
id: 5337
category:
    - Docker
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### 相关资料

http://dockone.io/article/10353

https://www.cnblogs.com/ryanyangcs/p/12908986.html

- - - - - -

###### 编写 Dockerfile

```ruby
cat > Dockerfile 
```

- - - - - -

###### 测试文件

```ruby
cat > hello.go 
```

- - - - - -

###### 构建

```ruby
docker build -t tools-os:v1.0.0 .

```

- - - - - -

###### 查看镜像大小

```ruby
[root@test1 k8s]# docker images
REPOSITORY                           TAG                 IMAGE ID            CREATED              SIZE
tools-os                             v1.0.0              873902b8b571        2 minutes ago        7.68MB
golang                               alpine              459ae5e869df        9 days ago           370MB
alpine                               latest              f70734b6a266        4 weeks ago          5.61MB
[root@test1 k8s]#

```

- - - - - -

###### 运行

```ruby
[root@test1 k8s]# docker run --rm tools-os:v1.0.0
Hello, world!
[root@test1 k8s]#

```

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

##### golang 启动web服务器

###### 编写 Dockerfile

```ruby
cat > Dockerfile 
```

- - - - - -

###### 测试文件

```ruby
cat > hello.go 
```

- - - - - -

###### 构建

```ruby
docker build -t tools-web:v1.0.0 .

```

- - - - - -

###### 查看镜像大小

```ruby
[root@test1 k8s]# docker images
REPOSITORY                           TAG                 IMAGE ID            CREATED              SIZE
tools-web                            v1.0.0              7ad480f99b28        About a minute ago   13.1MB
tools-os                             v1.0.0              873902b8b571        2 minutes ago        7.68MB
golang                               alpine              459ae5e869df        9 days ago           370MB
alpine                               latest              f70734b6a266        4 weeks ago          5.61MB
[root@test1 k8s]#

```

- - - - - -

###### 运行

```ruby
[root@test1 k8s]# docker run -dti --name tools-web -p 9000:9000 tools-web:v1.0.0

```

- - - - - -

###### 测试访问

```ruby
[root@test1 k8s]# curl 127.0.0.1:9000
Hello, world!
[root@test1 k8s]#

```

- - - - - -

- - - - - -

- - - - - -

###### 总结

```
tools-web:v1.0.0          13.1MB
tools-os:v1.0.0           7.68MB

```

这两个打包后的小镜像，是可以独立运行的，  
`docker save tools-web:v1.0.0 > tools-web.tar`  
`docker save tools-os:v1.0.0 > tools-os.tar`  
可以将小镜像在任意环境下的docker容器中运行  
`docker load <br></br>`docker load ``

- - - - - -

- - - - - -

- - - - - -