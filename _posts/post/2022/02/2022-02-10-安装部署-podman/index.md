---
title: "安装部署 Podman"
date: "2022-02-10"
categories: 
  - "podman"
---

##### 简介

###### **[Podman官方文档](https://podman.io/getting-started/installation "Podman官方文档")**

###### **[Podman官方Github](https://github.com/containers/podman/tags "Podman官方Github")**

* * *

##### **`CentOS 8`默认用`Podman`**

Docker 的一个缺点是它有一个中央守护进程，它以 root 用户的身份运行，这对安全有影响。但这正是 Podman 的用武之地。

Podman 是一个 无守护进程容器引擎，用于开发、管理和在你的 Linux 系统上以 root 或无 root 模式运行 OCI 容器

相比于docker，podman的主要区别是：podman不需要守护进程，所有容器也不再是同一个父进程，而且可以用普通用户操作；

对于系统管理员，podman命令行与docker一致，给podman设置一个名为docker的别名或软链接，用起来几乎没有区别。

* * *

经过实际检验，在CentOS7中只支持运行低版本Podman，可从CentOS默认的软件包仓库去查证，https://pkgs.org/search/?q=podman 因此要想使用高版本的Podman仍需替换高版本的操作系统

* * *

* * *

* * *

###### CentOS 7 安装部署

```ruby
yum install -y subscription-manager

subscription-manager repos --enable=rhel-7-server-extras-rpms

yum -y install podman

```

**查看结果**

```ruby
[root@localhost podman]# podman -v
podman version 1.6.4
[root@localhost podman]#
```

* * *

###### 配置文件所在目录

```ruby
[root@localhost containers]# pwd
/etc/containers

[root@localhost containers]# ll
certs.d
oci
policy.json
registries.conf
registries.d
storage.conf

```

**查看默认的配置文件内容**

```ruby
[root@localhost containers]# cat registries.conf

## 配置仓库地址
[registries.search]
## 拉取镜像时会按照数组中的链接地址，按顺序进行尝试
registries = ['registry.access.redhat.com', 'registry.redhat.io', 'docker.io']


[registries.insecure]
registries = []


[registries.block]
registries = []


```

* * *

* * *

* * *

###### 使用 podman

```ruby
## 拉取镜像
podman pull nginx:latest

## 运行一个容器
podman run -p 80:80 --rm -it docker.io/library/nginx:latest

```

* * *

* * *

* * *

##### **配置私有仓库 Harbor**

```ruby
[root@localhost containers]# vim registries.conf

......省略

[registries.search]
#registries = ['www.xxxxxxxxxxxx.com', 'registry.access.redhat.com', 'registry.redhat.io', 'docker.io']
## Harbor仓库地址，端口使用的是80
registries = ['192.168.103.226']

......省略

```

**测试，注意：使用http协议时需要关闭tls验证`--tls-verify=false`**

```ruby
## 登录
[root@localhost podman]# podman login 192.168.103.226 -u admin -p Harbor12345 --tls-verify=false
Login Succeeded!
[root@localhost podman]#

## 查看原有镜像
[root@localhost podman]# podman images
REPOSITORY                TAG      IMAGE ID       CREATED       SIZE
docker.io/library/nginx   latest   c316d5a335a5   2 weeks ago   146 MB

## 将tag改为私服名称
[root@localhost podman]# podman tag docker.io/library/nginx:latest 192.168.103.226/library/nginx:latest

## 在次查看镜像
[root@localhost podman]# podman images
REPOSITORY                      TAG      IMAGE ID       CREATED       SIZE
docker.io/library/nginx         latest   c316d5a335a5   2 weeks ago   146 MB
192.168.103.226/library/nginx   latest   c316d5a335a5   2 weeks ago   146 MB

## 推送镜像到私服
[root@localhost podman]# podman push 192.168.103.226/library/nginx:latest --tls-verify=false


```

* * *

* * *

* * *

* * *

* * *

* * *

###### 命令

```ruby
[root@localhost podman]# podman -h
manage pods and images

Usage:
  podman [flags]
  podman [command]

Available Commands:
  attach      Attach to a running container
  build       Build an image using instructions from Containerfiles
  commit      Create new image based on the changed container
  container   Manage Containers
  cp          Copy files/folders between a container and the local filesystem
  create      Create but do not start a container
  diff        Inspect changes on container's file systems
  events      Show podman events
  exec        Run a process in a running container
  export      Export container's filesystem contents as a tar archive
  generate    Generated structured data
  healthcheck Manage Healthcheck
  help        Help about any command
  history     Show history of a specified image
  image       Manage images
  images      List images in local storage
  import      Import a tarball to create a filesystem image
  info        Display podman system information
  init        Initialize one or more containers
  inspect     Display the configuration of a container or image
  kill        Kill one or more running containers with a specific signal
  load        Load an image from container archive
  login       Login to a container registry
  logout      Logout of a container registry
  logs        Fetch the logs of a container
  mount       Mount a working container's root filesystem
  network     Manage Networks
  pause       Pause all the processes in one or more containers
  play        Play a pod
  pod         Manage pods
  port        List port mappings or a specific mapping for the container
  ps          List containers
  pull        Pull an image from a registry
  push        Push an image to a specified destination
  restart     Restart one or more containers
  rm          Remove one or more containers
  rmi         Removes one or more images from local storage
  run         Run a command in a new container
  save        Save image to an archive
  search      Search registry for image
  start       Start one or more containers
  stats       Display a live stream of container resource usage statistics
  stop        Stop one or more containers
  system      Manage podman
  tag         Add an additional name to a local image
  top         Display the running processes of a container
  umount      Unmounts working container's root filesystem
  unpause     Unpause the processes in one or more containers
  unshare     Run a command in a modified user namespace
  varlink     Run varlink interface
  version     Display the Podman Version Information
  volume      Manage volumes
  wait        Block on one or more containers

Flags:
      --cgroup-manager string     Cgroup manager to use (cgroupfs or systemd) (default "systemd")
      --cni-config-dir string     Path of the configuration directory for CNI networks
      --config string             Path of a libpod config file detailing container server configuration options
      --conmon string             Path of the conmon binary
      --cpu-profile string        Path for the cpu profiling results
      --events-backend string     Events backend to use
      --help                      Help for podman
      --hooks-dir strings         Set the OCI hooks directory path (may be set multiple times)
      --log-level string          Log messages above specified level: debug, info, warn, error, fatal or panic (default "error")
      --namespace string          Set the libpod namespace, used to create separate views of the containers and pods on the system
      --network-cmd-path string   Path to the command for configuring the network
      --root string               Path to the root directory in which data, including images, is stored
      --runroot string            Path to the 'run directory' where all state information is stored
      --runtime string            Path to the OCI-compatible binary used to run containers, default is /usr/bin/runc
      --storage-driver string     Select which storage driver is used to manage storage of images and containers (default is overlay)
      --storage-opt stringArray   Used to pass an option to the storage driver
      --syslog                    Output logging information to syslog as well as the console
      --tmpdir string             Path to the tmp directory
      --trace                     Enable opentracing output
  -v, --version                   Version of podman

Use "podman [command] --help" for more information about a command.
[root@localhost podman]#

```

* * *

* * *

* * *

##### 配置 podman-compose

官方github地址：https://github.com/containers/podman-compose

```ruby
## 官方github下载
curl -o /usr/local/bin/podman-compose https://raw.githubusercontent.com/containers/podman-compose/v1.0.3/podman_compose.py
chmod +x /usr/local/bin/podman-compose


## 或者七牛云下载
curl -o /usr/local/bin/podman-compose http://qiniu.dev-share.top/file/podman_compose_v1.0.3.py
chmod +x /usr/local/bin/podman-compose


[root@localhost ~]# podman-compose -v
['podman', '--version', '']
using podman version: 1.6.4
podman-composer version  1.0.3
podman --version
podman version 1.6.4
exit code: 0
[root@localhost ~]#

```

* * *

* * *

* * *
