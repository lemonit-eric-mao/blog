---
title: '安装 Docker'
date: '2017-11-16T14:34:09+00:00'
status: publish
permalink: /2017/11/16/%e5%ae%89%e8%a3%85-docker
author: 毛巳煜
excerpt: ''
type: post
id: 386
category:
    - Docker
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
##### 为什么要使用 Docker容器技术？它的好处是什么？

**容器的优点： 容器具有很强的`应用可移植性`，它能够提供一致性的环境，脱离物理资源的限制，能够快速的实现，实时的业务访问**

- - - - - -

##### **[下载社区版 (Docker CE)](https://docs.docker.com/engine/install/centos "下载社区版 (Docker CE)")**

##### 卸载旧版本(Uninstall old versions)

```ruby
[root@localhost ~]#  yum remove -y docker*

```

- - - - - -

##### 使用存储库进行安装

1 安装所需的软件包 yum-utils提供了yum-config-manager 效用，并device-mapper-persistent-data和lvm2由需要 devicemapper存储驱动程序。

```ruby
[root@localhost ~]# yum install -y yum-utils

```

2 使用以下命令来设置稳定的存储库。

```ruby
[root@localhost ~]# yum-config-manager \
                        --add-repo \
                        https://download.docker.com/linux/centos/docker-ce.repo


```

- - - - - -

##### 在生产系统上，您应该安装特定版本的Docker CE，而不是始终使用最新版本。列出可用的版本。

**此示例使用该sort -r命令按版本号从最高到最低排序结果**

```ruby
[root@localhost docker]# yum list docker-ce --showduplicates | sort -r
docker-ce.x86_64            3:23.0.2-1.el7                      docker-ce-stable
docker-ce.x86_64            3:23.0.1-1.el7                      docker-ce-stable
docker-ce.x86_64            3:23.0.0-1.el7                      docker-ce-stable
docker-ce.x86_64            3:20.10.9-3.el7                     docker-ce-stable
docker-ce.x86_64            3:20.10.8-3.el7                     docker-ce-stable
docker-ce.x86_64            3:20.10.7-3.el7                     docker-ce-stable
docker-ce.x86_64            3:19.03.9-3.el7                     docker-ce-stable
docker-ce.x86_64            3:19.03.8-3.el7                     docker-ce-stable
docker-ce.x86_64            3:19.03.7-3.el7                     docker-ce-stable
docker-ce.x86_64            18.06.3.ce-3.el7                    docker-ce-stable
docker-ce.x86_64            18.06.2.ce-3.el7                    docker-ce-stable
docker-ce.x86_64            18.06.1.ce-3.el7                    docker-ce-stable


```

```ruby
# 安装 20.10.6 版本， 前面的 3: 删除
[root@localhost docker]# yum install -y docker-ce-23.0.2-1.el7
# 安装 18.03版本
[root@localhost docker]# yum install -y docker-ce-18.06.3.ce-3.el7

```

- - - - - -

##### 修改docker容器目录

```ruby
# 在大空间的硬盘上创建存储目录
mkdir -p /mnt/docker-data/

# 将docker目录软链接到 大空间硬盘上
ln -s /mnt/docker-data/ /var/lib/docker

```

- - - - - -

##### 启动Docker

```ruby
[root@localhost docker]# systemctl enable docker && systemctl start docker && systemctl status docker
● docker.service - Docker Application Container Engine
   Loaded: loaded (/usr/lib/systemd/system/docker.service; disabled; vendor preset: disabled)
   Active: active (running) since 二 2017-11-07 15:13:54 CST; 1s ago
     Docs: https://docs.docker.com
 Main PID: 14873 (dockerd)
   Memory: 21.6M
   CGroup: /system.slice/docker.service
           ├─14873 /usr/bin/dockerd
           └─14884 docker-containerd -l unix:///var/run/docker/libcontainerd/docker-containerd.sock --metrics-inter...

```

- - - - - -

##### 配置Docker镜像加速器

```ruby
[root@k8s-master ~]#
[root@k8s-master ~]# cat > /etc/docker/daemon.json 
```

- - - - - -

- - - - - -

- - - - - -

##### 常见问题

###### 1

```ruby
[root@k8s-master ~]# yum install -y docker-ce-17.03.2.ce-1.el7.centos
软件包 docker-ce-selinux 已经被 docker-ce 取代，但是取代的软件包并未满足需求
---> 软件包 libtool-ltdl.x86_64.0.2.4.2-22.el7_3 将被 安装
--> 解决依赖关系完成
错误：软件包：docker-ce-17.03.2.ce-1.el7.centos.x86_64 (docker-ce-stable)
          需要：docker-ce-selinux >= 17.03.2.ce-1.el7.centos
          可用: docker-ce-selinux-17.03.0.ce-1.el7.centos.noarch (docker-ce-stable)
              docker-ce-selinux = 17.03.0.ce-1.el7.centos
          可用: docker-ce-selinux-17.03.1.ce-1.el7.centos.noarch (docker-ce-stable)
              docker-ce-selinux = 17.03.1.ce-1.el7.centos
          可用: docker-ce-selinux-17.03.2.ce-1.el7.centos.noarch (docker-ce-stable)
              docker-ce-selinux = 17.03.2.ce-1.el7.centos
          可用: docker-ce-selinux-17.03.3.ce-1.el7.noarch (docker-ce-stable)
              docker-ce-selinux = 17.03.3.ce-1.el7
 您可以尝试添加 --skip-broken 选项来解决该问题
 您可以尝试执行：rpm -Va --nofiles --nodigest
[root@k8s-master ~]#
# 需要安装 docker-ce-selinux-*
[root@k8s-master ~]# yum install -y https://download.docker.com/linux/centos/7/x86_64/stable/Packages/docker-ce-selinux-17.03.2.ce-1.el7.centos.noarch.rpm

```

- - - - - -

###### 2

```ruby
[root@test1 ~]# systemctl status docker.service
● docker.service - Docker Application Container Engine
   Loaded: loaded (/usr/lib/systemd/system/docker.service; enabled; vendor preset: disabled)
   Active: failed (Result: exit-code) since 三 2019-12-11 11:39:25 CST; 6s ago
     Docs: https://docs.docker.com
  Process: 10018 ExecStart=/usr/bin/dockerd (code=exited, status=1/FAILURE)
 Main PID: 10018 (code=exited, status=1/FAILURE)

12月 11 11:39:24 test1 systemd[1]: Starting Docker Application Container Engine...
12月 11 11:39:24 test1 dockerd[10018]: time="2019-12-11T11:39:24.992222657+08:00" level=info msg="libcontainerd: new containerd process, pid: 10026"
12月 11 11:39:25 test1 dockerd[10018]: time="2019-12-11T11:39:25.997564912+08:00" level=error msg="[graphdriver] prior storage driver overlay2 failed: driver not supported"
12月 11 11:39:25 test1 dockerd[10018]: Error starting daemon: error initializing graphdriver: driver not supported
12月 11 11:39:25 test1 systemd[1]: docker.service: main process exited, code=exited, status=1/FAILURE
12月 11 11:39:26 test1 systemd[1]: Failed to start Docker Application Container Engine.
12月 11 11:39:26 test1 systemd[1]: Unit docker.service entered failed state.
12月 11 11:39:26 test1 systemd[1]: docker.service failed.

# 需要修改配置文件
[root@test1 ~]# vim /etc/docker/daemon.json
{
  "registry-mirrors": ["https://registry.cn-hangzhou.aliyuncs.com"],
  # 设置每个容器, 单个日志文件最大为1G, 最多保留三个日志文件
  "log-driver":"json-file",
  "log-opts": {"max-size":"1g", "max-file":"3"},
  # 加入如下两行
  "storage-driver": "overlay2",
  "storage-opts": [
    "overlay2.override_kernel_check=true"
  ]
}
[root@test1 ~]#
[root@test1 ~]# systemctl daemon-reload && systemctl restart docker

```

- - - - - -

###### 3 重启防火墙后，要重启 docker

```ruby
[root@dev2 gitlab]# docker-compose up
 Creating network "gitlab_default" with the default driver
ERROR: cannot create network
[root@dev2 gitlab]#
[root@dev2 gitlab]# systemctl restart docker

```

- - - - - -

- - - - - -

- - - - - -

Ubuntu 22.04安装Docker
====================

[替换阿里云源](http://www.dev-share.top/2019/11/06/linux-%e7%b3%bb%e7%bb%9f%e9%85%8d%e7%bd%ae%e9%98%bf%e9%87%8c%e4%ba%91%e6%ba%90/ "替换阿里云源")
--------------------------------------------------------------------------------------------------------------------------------------

安装 docker
---------

```bash
sudo apt install docker.io


```

- - - - - -

- - - - - -

- - - - - -