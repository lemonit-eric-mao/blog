---
title: 'Linux 常见问题'
date: '2020-11-06T07:04:27+00:00'
status: publish
permalink: /2020/11/06/linux-%e5%b8%b8%e8%a7%81%e9%97%ae%e9%a2%98
author: 毛巳煜
excerpt: ''
type: post
id: 6518
category:
    - Ubuntu
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
#### Linux删除带横杠的文件或文件夹

```ruby
## 查看目录，这样的文件在Linux系统中是无法直接 rm的
[root@k8s-master-01 siyu.mao]# ll
-rw-r--r-- 1 root root      0 Jun 17 11:47 --create-namespace

## 正确的删除方法
[root@k8s-master-01 siyu.mao]# rm -rf -- --create-namespace


```

- - - - - -

- - - - - -

- - - - - -

#### CentOS 7 常见问题

###### 误操作移除了 `/usr/bin`目录, 修复方法。

```ruby
# 误操作； 注：此时不要重启电脑，否则无法在登录用户系统
mv /usr/bin/ /home/deploy/backup/

# 解决方法：移回来
cd /home/deploy/backup/
/home/deploy/backup/bin/mv bin/ /usr/bin/

```

###### **[无法在登录用户系统，需要进入单用户模式操作](http://www.dev-share.top/2021/02/25/linux-%e8%bf%9b%e5%85%a5%e5%8d%95%e7%94%a8%e6%88%b7%e6%a8%a1%e5%bc%8f/ "无法在登录用户系统，需要进入单用户模式操作")**

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

#### Ubuntu 常见问题

###### sudo apt-get update由于没有公钥，无法验证下列签名： NO\_PUBKEY 93C4A3FD7BB9C367

```ruby
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367

```

- - - - - -

- - - - - -

- - - - - -

###### Ubuntu18.04 安装 chrome

```ruby
sudo wget http://www.linuxidc.com/files/repo/google-chrome.list -P /etc/apt/sources.list.d/

wget -q -O - https://dl.google.com/linux/linux_signing_key.pub  | sudo apt-key add -

sudo apt update

sudo apt install google-chrome-stable


```

- - - - - -

- - - - - -

- - - - - -