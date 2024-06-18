---
title: 'Centos7 安装 Gitlab Runner'
date: '2019-02-16T01:20:26+00:00'
status: publish
permalink: /2019/02/16/centos7-%e5%ae%89%e8%a3%85-gitlab-runner
author: 毛巳煜
excerpt: ''
type: post
id: 3442
category:
    - Git
    - Linux服务器
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
[官方安装教程](https://docs.gitlab.com/runner/install/linux-repository.html "官方安装教程")

 想法: 其实gitlab-runner 和 jenkins 是一样的作用，那么它也只是一个单独的 用来 build 项目的服务器，所以为了操作方便就不使用Docker 镜像来安装

- - - - - -

##### [持续集成 生产案例](http://www.dev-share.top/2019/07/10/gitlab-ci-%e6%8c%81%e7%bb%ad%e9%9b%86%e6%88%90-%e7%94%9f%e4%ba%a7%e6%a1%88%e4%be%8b/ "持续集成 生产案例")

- - - - - -

- - - - - -

- - - - - -

##### gitlab-runner 的工作能力

1. 它只是用来执行脚本、调度、协调的工作能力, 如果需要安装依赖环境(例如： docker) 需要使用 root 账户安装
2. 网上有很多文章说改变 gitlab-runner账户的权限改为root权限; 这个我已经试过了即使改了也是不被允许的gitlab-runner的组必须是 gitlab-runner:x:993:
3. 所以要记住，不要让gitlab-runner去安装依赖环境，它只负责执行脚本

- - - - - -

##### 一、 使用 root 用户 安装 gitlab-runner (不使用 Docker 镜像安装，不好控制)

**[官方地址](https://docs.gitlab.com/runner/install/linux-repository.html#installing-the-runner "官方地址")**

```ruby
# 添加GitLab的官方存储库
[root@master ~]# curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-ci-multi-runner/script.rpm.sh | sudo bash
# 安装
[root@master ~]# yum install -y gitlab-runner
# 查看安装版本
[root@master ~]# gitlab-runner -v
Version:      9.5.1
Git revision: 96b34cc
Git branch:   9-5-stable
GO version:   go1.8.3
Built:        Wed, 04 Oct 2017 16:26:27 +0000
OS/Arch:      linux/amd64
[root@master ~]#

```

- - - - - -

- - - - - -

- - - - - -

###### gitlab-runner用户设置root权限 (根据实际情况 **`可选`** )

```ruby
# 删除gitlab-runner
[root@master ~]# gitlab-runner uninstall

[root@master ~]# gitlab-runner install --working-directory /home/gitlab-runner --user root

[root@master ~]# systemctl restart gitlab-runner.service

[root@master ~]# ps aux | grep gitlab-runner


```

- - - - - -

- - - - - -

- - - - - -

##### 为gitlab-runner用户添加 sudo 免密

**`注`：安装完成后， 会在/home目录下，自动创建出 gitlab-runner 用户**

```ruby
[root@master ~]# visudo
gitlab-runner ALL=(ALL) NOPASSWD: ALL
[root@master ~]#

```

- - - - - -

##### 将 `gitlab-runner` 用户加入到 docker组

```ruby
[root@master ~]# su - gitlab-runner

[gitlab-runner@master ~]<span class="katex math inline">sudo gpasswd -a</span>{USER} docker
正在将用户"gitlab-runner"加入到"docker"组中
[gitlab-runner@master ~]$

```

- - - - - -

- - - - - -

- - - - - -

##### 二、 注册 gitlab-runner

###### 获取 runner 需要的注册信息

`导航 > 管理区域(扳手图标) > 概述 > Runners`  
1\. 安装一个与 GitLab CI 兼容的 Runner (如需了解更多的安装信息，请查看 GitLab Runner)  
2\. 在 Runner 设置时指定以下 URL： http://git.dev-share.top/  
3\. 在安装过程中使用以下注册令牌： 96JQ25HHmmC6n9Ez9Qzf  
4\. 启动 Runner!

###### 进行注册

```ruby
[gitlab-runner@master ~]# sudo gitlab-runner register
Running in system-mode.

Please enter the gitlab-ci coordinator URL (e.g. https://gitlab.com/):
http://git.dev-share.top/    # 手动输入 上面已经拿到了

Please enter the gitlab-ci token for this runner:
96JQ25HHmmC6n9Ez9Qzf         # 手动输入 上面已经拿到了

Please enter the gitlab-ci description for this runner:
[k8s-master]:                # 直接回车

Please enter the gitlab-ci tags for this runner (comma separated):
devops                       # 手动输入 为这个 runner 添加一个 标签
Whether to run untagged builds [true/false]:
[false]: true                # 手动输入
Whether to lock Runner to current project [true/false]:
[false]: true                # 手动输入
Registering runner... succeeded                     runner=96JQ25HH
# 注意这个 选择要应用的模板
Please enter the executor: shell, kubernetes, parallels, ssh, virtualbox, docker+machine, docker-ssh+machine, docker, docker-ssh:
shell                        # 手动输入 一般都选 shell
Runner registered successfully. Feel free to start it, but if it's running already the config should be automatically reloaded!

[gitlab-runner@master ~]#

```

- - - - - -

###### **[GitLab CI/CD 配置 .gitlab-ci.yml](http://www.dev-share.top/2019/06/14/gitlab-ci-cd-%e9%85%8d%e7%bd%ae-gitlab-ci-yml/ "GitLab CI/CD 配置 .gitlab-ci.yml")**

- - - - - -

##### gitlab-runner 常用命令

```ruby
[gitlab-runner@master ~]# sudo gitlab-runner status
gitlab-runner: Service is running!

[gitlab-runner@master ~]# sudo gitlab-runner stop
[gitlab-runner@master ~]# sudo gitlab-runner status
gitlab-runner: Service is not running.

[gitlab-runner@master ~]# sudo gitlab-runner start
[gitlab-runner@master ~]# sudo gitlab-runner status
gitlab-runner: Service is running!

[gitlab-runner@master ~]#

```

##### 常见问题及解决方法

`此作业被卡住，因为没有任何该项目指定标签的 runner 在线`  
这个原因就是在创建 .gitlab-ci.yml的时候没有给任务指定标签，或者指定的标签不存在而导致的

###### [常见问题](http://www.dev-share.top/2019/07/17/gitlab-runner%e7%94%a8%e6%88%b7%e6%89%a7%e8%a1%8c-docker-compose-%e5%91%bd%e4%bb%a4%e6%97%b6%e5%bc%82%e5%b8%b8/ "常见问题")

- - - - - -

- - - - - -

- - - - - -