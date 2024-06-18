---
title: Git配置多个SSH-Key
date: '2018-06-04T17:48:02+00:00'
status: private
permalink: /2018/06/04/git%e9%85%8d%e7%bd%ae%e5%a4%9a%e4%b8%aassh-key
author: 毛巳煜
excerpt: ''
type: post
id: 2138
category:
    - Git
    - 开发工具
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
###### **Gitee**

- Gitee 服务器地址 gitee.com
- Gitee 已有邮箱 85785053@qq.com

###### **Gitlab**

- Gitlab 服务器地址 http://172.16.15.205:8016
- Gitlab 已有邮箱 siyu.mao@dhc.com.cn

- - - - - -

###### 生成 SSH Key

```ruby
## 生成一个gitee用的SSH-Key
<span class="katex math inline">ssh-keygen -t rsa -C '85785053@qq.com' -f ~/.ssh/gitee_id_rsa

## 生成一个gitlab用的SSH-Key</span> ssh-keygen -t rsa -C 'siyu.mao@dhc.com.cn' -f ~/.ssh/gitlab_id_rsa

```

- - - - - -

###### 生成统一配置文件

```ruby
cat > ~/.ssh/config 
```

- - - - - -

###### 测试

```ruby
$ ssh -T git@gitee.com
Hi Eric! You've successfully authenticated, but GITEE.COM does not provide shell access.


$  ssh -T git@172.16.15.205
Welcome to GitLab, @siyu.mao!


```

- - - - - -

- - - - - -

- - - - - -