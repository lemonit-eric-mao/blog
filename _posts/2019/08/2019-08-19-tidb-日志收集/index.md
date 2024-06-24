---
title: "TiDB 日志收集"
date: "2019-08-19"
categories: 
  - "tidb"
---

##### 查看TiDB日志

通过ansible-playbook部署的TiDB日志位置，默认是在项目部署的目录下

```ruby
[tidb@test1 tidb-ansible]$ cat inventory.ini | grep deploy_dir
# 项目部署的目录
deploy_dir = /home/tidb/deploy
[tidb@test1 tidb-ansible]$
```

log的位置就在 `/home/tidb/deploy/log/`
