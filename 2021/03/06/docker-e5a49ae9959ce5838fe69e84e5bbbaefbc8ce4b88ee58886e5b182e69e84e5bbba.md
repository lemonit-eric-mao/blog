---
title: 'Docker  多镜像构建，与分层构建'
date: '2021-03-06T15:41:28+00:00'
status: private
permalink: /2021/03/06/docker-%e5%a4%9a%e9%95%9c%e5%83%8f%e6%9e%84%e5%bb%ba%ef%bc%8c%e4%b8%8e%e5%88%86%e5%b1%82%e6%9e%84%e5%bb%ba
author: 毛巳煜
excerpt: ''
type: post
id: 6990
category:
    - Docker
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### Dockerfile

```ruby
# 制作基础镜像，镜像内容基本不改变的放在这层
FROM ubuntu:18.04 AS base-cn-ansible

# 替换镜像中的官方下载源，将它指向国内源
RUN sed -i s/'archive.ubuntu.com'/'mirrors.aliyun.com'/g /etc/apt/sources.list

LABEL MAINTAINER="Eric Mao"
LABEL NAME=cn-ansible

RUN apt-get update \
    && apt-get install -y software-properties-common \
    && add-apt-repository ppa:ansible/ansible \
    && apt-get install -y python3.7 python3-pip \
    && apt-get install -y python3-distutils python3-setuptools

##################################################

# 基于基础镜像，构建应用程序，镜像内容改变较少的放在这层
FROM base-cn-ansible AS req-cn-ansible

LABEL MAINTAINER="Eric Mao"
LABEL NAME=cn-ansible

WORKDIR /cn-ansible/
COPY requirements.txt /cn-ansible/

RUN pip3 install -r requirements.txt -i https://pypi.douban.com/simple

##################################################

# 基于基础镜像，构建应用程序，镜像内容经常变化放在最下层
FROM req-cn-ansible AS app-cn-ansible
COPY . /cn-ansible/

EXPOSE 8000

# 设置python的stdout为无缓存模式, 即时输出日志
ENV PYTHONUNBUFFERED=1

CMD [ "python3", "main.py" ]


```

- - - - - -

###### 正常分层构建

```ruby
docker build -t cn-ansible:v0.0.1 .

```

- - - - - -

###### 多镜像构建

```ruby
docker build --target base-cn-ansible -t base-cn-ansible .
docker build --target req-cn-ansible -t req-cn-ansible .
docker build --target app-cn-ansible -t cn-ansible:v0.0.1 .

```

- - - - - -

- - - - - -

- - - - - -

###### `弊端`

 多镜像分层构建好处是加快了构建速度，但相对的问题是，镜像的包如果非常大，那构建的速度的侧重点就变为其次，因此：首要考虑的是 **`镜像的大小`** ，然后是构建的速度。 镜像变大的原因大部分原因是在构建镜像时，更新的依赖库很大，这些依赖库的作用多半是用在构建时机，应用程序构建成功后就没有作用了，所以删除这些无用的依赖包很重要。 **`删除依赖包` 要在同一层进行** ，因为Docker镜像的每一层都是只读的，不能在下一层对上一层的文件进行删除，Dockerfile配置方法如下

- - - - - -

###### 正确做法 Dockerfile

```yaml
# 制作基础镜像，镜像内容基本不改变的放在这层
FROM ubuntu:18.04 AS base-cn-ansible

# 替换镜像中的官方下载源，将它指向国内源
RUN sed -i s/'archive.ubuntu.com'/'mirrors.aliyun.com'/g /etc/apt/sources.list

LABEL MAINTAINER="Eric Mao"
LABEL NAME=cn-ansible

WORKDIR /cn-ansible/

COPY . /cn-ansible/

RUN apt-get update \
    && apt-get install -y software-properties-common \
    && add-apt-repository ppa:ansible/ansible \
    && apt-get install -y python3.7 python3-pip python3-distutils python3-setuptools\
    && pip3 install -r requirements.txt -i https://pypi.douban.com/simple \
    && apt-get clean \
    && apt-get remove --auto-remove -y python3-pip python3-distutils python3-setuptools \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

# 设置python的stdout为无缓存模式, 即时输出日志
ENV PYTHONUNBUFFERED=1

CMD [ "python3", "main.py" ]

```

- - - - - -

- - - - - -

- - - - - -