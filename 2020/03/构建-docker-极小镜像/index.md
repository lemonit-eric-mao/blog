---
title: "构建 Docker 极小镜像"
date: "2020-03-25"
categories: 
  - "docker"
---

##### 创建脚本

```ruby
cat > start.sh << ERIC
#!/bin/sh

echo hello_\$TEMP

ERIC

```

* * *

##### Dockerfile 构建镜像

```ruby
cat > Dockerfile << ERIC

## 构建
# docker build -t tools:1.0.0 .
## 运行
# docker run --rm -it tools:1.0.0 /bin/sh
# 使用最小 Docker 镜像来构建新的镜像

FROM alpine:latest

# 在容器中创建一个文件夹
RUN mkdir -p /app

# WORKDIR 将创建的文件夹做为工作目录
#   ，也就是进入容器后默认进入的目录
WORKDIR /app

# 将脚本程序复制到容器中
COPY start.sh /app/

# 授权
RUN chmod 755 start.sh

# 保持运行
CMD [ "sh", "-c", "tail -f /dev/null" ]

ERIC

```

* * *

##### 构建

```ruby
## 构建
docker build -t tools:1.0.0 .

## 查看
docker images tools
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
tools        1.0.0     2f3c597df221   56 seconds ago   5.54MB

```

* * *

##### 运行以后会自动删除容器(--rm)

```ruby
## 容器内脚本
docker run --rm -it -e TEMP=world! tools:1.0.0 /bin/sh
/app # ./start.sh
hello_world!


## 在容器外直接执行脚本
docker run --rm -it -e TEMP=world! tools:1.0.0 /bin/sh ./start.sh
hello_world!

```
