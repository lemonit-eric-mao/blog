---
title: 'docker-compose 安装 gitlab-ce'
date: '2017-11-18T09:43:24+00:00'
status: publish
permalink: /2017/11/18/docker-compose-%e5%ae%89%e8%a3%85-gitlab-ce
author: 毛巳煜
excerpt: ''
type: post
id: 577
category:
    - Docker
    - Git
tag: []
post_format: []
cwp_meta_box_check:
    - 'No'
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
###### **[安装 docker-compose](http://www.dev-share.top/2019/06/12/%e5%ae%89%e8%a3%85-docker-compose/ "安装 docker-compose")**

###### **[DockerHub](https://hub.docker.com/r/gitlab/gitlab-ce "DockerHub")**

###### docker-compose 使用域名配置

```ruby
[root@gitlab ~]# mkdir -p /home/deploy/gitlab-ce-13 && cd /home/deploy/gitlab-ce-13
[root@gitlab gitlab-ce-13]# cat > docker-compose.yml 
```

- - - - - -

###### docker-compose 使用IP配置 并且修改 **`git clone 端口`**

```ruby
[root@gitlab ~]# mkdir -p /home/deploy/gitlab-ce-13 && cd /home/deploy/gitlab-ce-13
[root@gitlab gitlab-ce-13]# cat > docker-compose.yml 
```

- - - - - -

###### 设置中文

登录后输入 **http://192.168.2.10:8016`/-/profile/preferences`** 修改语言为中文

- - - - - -

###### **[数据备份与恢复](http://www.dev-share.top/2019/03/06/gitlab-%e6%95%b0%e6%8d%ae%e5%a4%87%e4%bb%bd%e4%b8%8e%e6%81%a2%e5%a4%8d/ "数据备份与恢复")**

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

### **常见问题**

###### 使用命令行重置管理员密码

> `gitlab-rake "gitlab:password:reset[root]"`

```bash
┌──(root@harbor-new 17:11:34) - [/data/gitlab-ce]
└─# docker-compose exec gitlab-ce /bin/bash gitlab-rake "gitlab:password:reset[root]"
Enter password:
Confirm password:
Password successfully updated for user with username root.


```

- - - - - -

- - - - - -

- - - - - -

**如果在容器启动时 不指定 `--hostname='你的域名'` 就会出现如下问题**

gitlab服务器启动后, 新建一个项目, 但项目的地址是这样的, 本来应该是域名位置确变成了 Docker容器的ID  
http://eac9d06da1f7/Groups-SmallPrograms/test.git

##### 以下是非Docker安装的服务器的修改方法

**在gitlab的安装目录下找到 `gitlab-rails/etc/gitlab.yml`**

```ruby
[root@shared-server etc]# pwd
/mnt/gitlab/data/gitlab-rails/etc
[root@shared-server etc]# ll
total 52
-rw-r--r-- 1 root root   507 Oct 13 23:25 database.yml
-rw-r--r-- 1 root root   129 Oct 13 23:25 gitlab_shell_secret
-rw-r--r-- 1 root root    45 Oct 13 23:25 gitlab_workhorse_secret
-rw-r--r-- 1 root root 16781 Oct 19 13:41 gitlab.yml
-rw-r--r-- 1 root root  1383 Oct 13 23:25 rack_attack.rb
-rw-r--r-- 1 root root    59 Oct 13 23:25 resque.yml
-rw-r--r-- 1 root root  4103 Oct 13 23:25 secrets.yml
-rw-r--r-- 1 root root  1732 Oct 13 23:28 unicorn.rb
[root@shared-server etc]# vim gitlab.yml

```

###### 将 host: eac9d06da1f7 改为 自己的域名

```
  ## GitLab settings
  gitlab:
    ## Web server settings (note: host is the FQDN, do not include http://)
    # host: eac9d06da1f7
    host: git.dev-share.top
    port: 80
    https: false

```

###### 重启 Docker 容器

```ruby
[root@shared-server etc]# docker restart eac9d06da1f7

```

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

###### gitlab 规范使用

[![](http://qiniu.dev-share.top/gitlab-layer.png)](http://qiniu.dev-share.top/gitlab-layer.png)

[![](http://qiniu.dev-share.top/gitlab-tree.png)](http://qiniu.dev-share.top/gitlab-tree.png)

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -