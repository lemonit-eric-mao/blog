---
title: "Helm3 推送文件到 Harbor仓库"
date: "2020-09-14"
categories: 
  - "helm"
  - "k8s"
---

###### **[安装 Helm3](http://www.dev-share.top/2020/07/16/helm-%e5%ae%89%e8%a3%85-%e4%bd%bf%e7%94%a8/ "安装 Helm3")**

###### **[安装 Harbor](http://www.dev-share.top/2019/06/06/docker-compose-%e5%ae%89%e8%a3%85-goharbor/ "安装 Harbor")**

* * *

###### 安装 helm3 推送插件

```ruby
[root@master01 ~]# helm plugin install https://github.com/chartmuseum/helm-push.git
Downloading and installing helm-push v0.10.4 ...
https://github.com/chartmuseum/helm-push/releases/download/v0.10.4/helm-push_0.10.4_linux_amd64.tar.gz
Installed plugin: cm-push

```

* * *

###### 关联 Harbor仓库

**helm repo add `给本地heml仓库起个名` http://`Harbor仓库IP地址`/chartrepo/`仓库名`/ --username `Harbor用户名` --password `Harbor密码`** `/chartrepo/` 是固定的

```ruby
[root@master01 ~]# helm repo add harbor-repo http://192.168.20.93/chartrepo/helm3/ --username admin --password Harbor12345
"harbor-repo" has been added to your repositories

# 查看加载
[root@master01 ~]# helm repo list
NAME            URL
harbor-repo     http://192.168.20.93/chartrepo/helm3/

```

* * *

###### 创建一个 Chart 模板

`helm create 模板名称`

```ruby
[root@master01 ~]# helm create 001-app-server && rm -rf 001-app-server/templates/*
Creating 001-app-server

```

* * *

###### 复制deploy-k8s/下的所有 yaml文件到指定的 templates/目录下

```ruby
[root@master01 ~]# cp deploy-k8s/* 001-app-server/templates/

# 查看
[root@master01 ~]# ll 001-app-server/templates/
configmap.yaml
deployment.yaml
destination-rule.yaml
namespace.yaml
service.yaml
virtual-service.yaml

```

* * *

###### 推送到仓库

**helm push `模板文件夹` `本地heml仓库名` --version=`指定上传的版本号`**

```ruby
[root@master01 ~]# helm cm-push 001-app-server harbor-repo --version=20200916
Pushing 001-app-server-20200916.tgz to harbor-repo...
Done.

```

* * *

* * *

* * *

###### 常见问题

**Error: this feature has been marked as experimental and is not enabled by default.`Please set HELM_EXPERIMENTAL_OCI=1` in your environment to use this feature**

```ruby
# 修改环境变量
[root@master01 ~]# export HELM_EXPERIMENTAL_OCI=1
```

* * *

* * *

* * *

###### 从Harbor私服仓库中下载

```ruby
# 关联仓库
[root@master01 ~]# helm repo add harbor-repo http://192.168.20.93/chartrepo/helm3/ --username admin --password Harbor12345

# 下载到本地
[root@master01 ~]# helm pull harbor-repo/007-specialroutes-service

```

* * *

* * *

* * *
