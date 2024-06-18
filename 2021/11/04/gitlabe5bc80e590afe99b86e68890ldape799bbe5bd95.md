---
title: gitlab开启集成ldap登录
date: '2021-11-04T03:50:14+00:00'
status: private
permalink: /2021/11/04/gitlab%e5%bc%80%e5%90%af%e9%9b%86%e6%88%90ldap%e7%99%bb%e5%bd%95
author: 毛巳煜
excerpt: ''
type: post
id: 8108
category:
    - ldap
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### **前置条件**

###### **[安装gitlab-ce](http://www.dev-share.top/2017/11/18/docker-compose-%e5%ae%89%e8%a3%85-gitlab-ce/ "安装gitlab-ce")**

###### **[安装ldap](http://www.dev-share.top/2021/11/04/docker-compose-%e5%ae%89%e8%a3%85-ldap/ "安装ldap")**

###### **思路**

1. 先安装好gitlab与ldap， 然后在ldap中创建一个用户( **`注：`** 不让使用默认的管理员用户)
2. 接下来配置gitlab， 让gitlab能够与ldap进行连接， 并且能够读取到ldap中的用户列表
3. 使用ldap中创建的用户， 在gitlab中的LDAP页进行登录

- - - - - -

###### **修改gitlab-ce配置文件**

```ruby
cat >> /opt/deploy/gitlab-ce-13/config/gitlab.rb 
```

- - - - - -

###### 重新加载gitlab配置

```ruby
[root@gitlab gitlab-ce-13]# docker exec -it gitlab-ce  gitlab-ctl reconfigure

```

- - - - - -

###### 查看是否能正常获取ldap用户列表

```ruby
[root@gitlab gitlab-ce-13]# docker exec -it gitlab-ce  gitlab-rake gitlab:ldap:check
Checking LDAP ...

LDAP: ... Server: ldapmain
LDAP authentication... Success
LDAP users with access to your GitLab server (only showing the first 100 results)
        DN: cn=mao siyu,cn=dhcg,ou=dhc,dc=test,dc=com    uid: msiyu

Checking LDAP ... Finished

[root@gitlab gitlab-ce-13]#

```

###### 关注uid: 它的值`msiyu`就是gitlab登录的用户名

- - - - - -

- - - - - -

- - - - - -

###### LDAP的API

`ldap[s]://hostname:port/base_dn?attributes?scope?filter`

- base\_dn: 缺省是root DN
- attributes: 格式是逗号分开的属性名，例如"cn,mail,telephoneNumber"，缺省是所有属性。
- scope: 可以有三个选项，缺省是base
- base：只查询base\_dn指定的节点
- one：只查出base\_dn的直接子节点，且不包括base\_dn本身。
- sub：查询出base\_dn的所有各级子节点，还包括base\_dn本身。
- filter: 过滤条件，缺省是(objectClass=\*)

```ruby
## 查询所有子属性
curl -s \
    --user "cn=admin,dc=test,dc=com" \
    "ldap://172.16.15.205:389/dc=test,dc=com??sub"


## 查询所有子属性DN与UID
curl -s \
    --user "cn=admin,dc=test,dc=com" \
    "ldap://172.16.15.205:389/dc=test,dc=com?dn,uid?sub"

```

- - - - - -

- - - - - -

- - - - - -