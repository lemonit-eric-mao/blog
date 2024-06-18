---
title: "Git配置多个SSH-Key"
date: "2018-06-04"
categories: 
  - "git"
  - "开发工具"
---

###### **Gitee**

- Gitee 服务器地址 gitee.com
- Gitee 已有邮箱 85785053@qq.com

###### **Gitlab**

- Gitlab 服务器地址 http://172.16.15.205:8016
- Gitlab 已有邮箱 siyu.mao@dhc.com.cn

* * *

###### 生成 SSH Key

```ruby
## 生成一个gitee用的SSH-Key
$ ssh-keygen -t rsa -C '85785053@qq.com' -f ~/.ssh/gitee_id_rsa

## 生成一个gitlab用的SSH-Key
$ ssh-keygen -t rsa -C 'siyu.mao@dhc.com.cn' -f ~/.ssh/gitlab_id_rsa
```

* * *

###### 生成统一配置文件

```ruby
cat > ~/.ssh/config << ERIC
## gitee
Host gitee.com
HostName gitee.com
PreferredAuthentications publickey
IdentityFile ~/.ssh/gitee_id_rsa

## gitlab
Host 172.16.15.205
HostName 172.16.15.205
## 这是因为gitab私服, 修改了默认的ssh端口
Port 8022
PreferredAuthentications publickey
IdentityFile ~/.ssh/gitlab_id_rsa

ERIC

```

* * *

###### 测试

```ruby
$ ssh -T git@gitee.com
Hi Eric! You've successfully authenticated, but GITEE.COM does not provide shell access.


$  ssh -T git@172.16.15.205
Welcome to GitLab, @siyu.mao!

```

* * *

* * *

* * *
