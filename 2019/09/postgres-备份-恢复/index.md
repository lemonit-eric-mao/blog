---
title: "Postgres 备份/恢复"
date: "2019-09-19"
categories: 
  - "postgresql"
---

##### 全量备份

`pg_dump -h 数据库IP -p 端口 -U 用户名 -C database > pgsql-backup.sql`

```ruby
[postgres@test1 ~]$ pg_dump -h 172.160.180.46 -p 5432 -U postgres -C dev2_dc_test > pgsql-backup.sql
```

##### 全量恢复

`psql -h 数据库IP -p 端口 -U 用户名 -C database < pgsql-backup.sql`

```ruby
[postgres@test1 ~]$ psql -h 172.160.180.46 -p 5432 -U postgres < pgsql-backup.sql
```
