---
title: 'docker-compose 安装 SVN'
date: '2020-08-28T07:33:20+00:00'
status: publish
permalink: /2020/08/28/docker-compose-%e5%ae%89%e8%a3%85-svn
author: 毛巳煜
excerpt: ''
type: post
id: 5981
category:
    - Linux服务器
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### 服务器地址: 192.168.2.10

- - - - - -

###### docker-compose.yaml

```ruby
cat > docker-compose.yaml 
```

- - - - - -

###### 创建空文件

```ruby
mkdir -p ./config/subversion/repo/

echo "" > ./config/subversion/subversion-access-control
echo "" > ./config/subversion/passwd

# 必须 777 权限
chmod -R 777 ./config/

# 启动
docker-compose up -d


```

- - - - - -

###### **访问管理页面**

`http://192.168.2.10:8090/svnadmin`  
`admin/admin`

- - - - - -

###### 初始化配置, 创建配置文件、创建仓库目录

```ruby
/etc/subversion/subversion-access-control
/etc/subversion/passwd
/home/svn
/usr/bin/svn
/usr/bin/svnadmin

```

[![](http://qiniu.dev-share.top/svn-setting.png)](http://qiniu.dev-share.top/svn-setting.png)

- - - - - -

###### 为路径授权

[![](http://qiniu.dev-share.top/svn-auth.png)](http://qiniu.dev-share.top/svn-auth.png)

- - - - - -

###### **SVN Checkout 地址**

**`http://192.168.2.10:8090/svn`/data/**  
`admin/admin`

- - - - - -

- - - - - -

- - - - - -