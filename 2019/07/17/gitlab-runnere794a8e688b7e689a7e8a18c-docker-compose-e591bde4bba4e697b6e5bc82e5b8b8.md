---
title: 'gitlab-runner 常见问题'
date: '2019-07-17T09:05:23+00:00'
status: publish
permalink: /2019/07/17/gitlab-runner%e7%94%a8%e6%88%b7%e6%89%a7%e8%a1%8c-docker-compose-%e5%91%bd%e4%bb%a4%e6%97%b6%e5%bc%82%e5%b8%b8
author: 毛巳煜
excerpt: ''
type: post
id: 4966
category:
    - Git
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### **Gitlab-Runner设置并发数**

```ruby
[root@Gitlab-Runner ~]# vim /etc/gitlab-runner/config.toml

## 并发数，默认1
concurrent = 10
check_interval = 0

[[runners]]
  name = "Gitlab-Runner"
  url = "http://172.16.15.35"
  token = "23391af58ee066e57008808e893aa3"
  executor = "shell"
  [runners.cache]


[root@Gitlab-Runner ~]# gitlab-runner restart


```

- - - - - -

- - - - - -

- - - - - -

##### **第`一`种情况** gitlab-runner用户执行 docker-compose 命令时异常

```ruby
[gitlab-runner@master ~]<span class="katex math inline">docker-compose build
ERROR: Couldn’t connect to Docker daemon at http+docker://localunixsocket - is it running?

If it’s at a non-standard location, specify the URL with the DOCKER_HOST environment variable.
[gitlab-runner@master ~]</span>

```

- - - - - -

##### **第`二`种情况** 执行 docker 命令没有权限

```ruby
[gitlab-runner@master ~]<span class="katex math inline">docker images
Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get http://%2Fvar%2Frun%2Fdocker.sock/v1.27/images/json: dial unix /var/run/docker.sock: connect: permission denied
[gitlab-runner@master ~]</span>

```

- - - - - -

##### **`原因`** 是gitlab-runner用户没有执行docker命令的权限，解决办法是将gitlab-runner用户加入到docker用户组

```ruby
[gitlab-runner@master ~]<span class="katex math inline">sudo gpasswd -a</span>{USER} docker
正在将用户"gitlab-runner"加入到"docker"组中
[gitlab-runner@master ~]$
# 重新连接终端

```

- - - - - -