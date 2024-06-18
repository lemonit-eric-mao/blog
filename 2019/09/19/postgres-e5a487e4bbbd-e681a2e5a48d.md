---
title: 'Postgres 备份/恢复'
date: '2019-09-19T08:09:06+00:00'
status: publish
permalink: /2019/09/19/postgres-%e5%a4%87%e4%bb%bd-%e6%81%a2%e5%a4%8d
author: 毛巳煜
excerpt: ''
type: post
id: 5048
category:
    - PostgreSQL
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 全量备份

`pg_dump -h 数据库IP -p 端口 -U 用户名 -C database > pgsql-backup.sql`

```ruby
[postgres@test1 ~]$ pg_dump -h 172.160.180.46 -p 5432 -U postgres -C dev2_dc_test > pgsql-backup.sql

```

##### 全量恢复

`psql -h 数据库IP -p 端口 -U 用户名 -C database `

```ruby
[postgres@test1 ~]$ psql -h 172.160.180.46 -p 5432 -U postgres 
```