---
title: 'TiDB 定时备份'
date: '2019-08-23T02:40:56+00:00'
status: publish
permalink: /2019/08/23/tidb-%e5%ae%9a%e6%97%b6%e5%a4%87%e4%bb%bd
author: 毛巳煜
excerpt: ''
type: post
id: 5010
category:
    - TiDB
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 编写定时任务要执行的脚本

```ruby
[tidb@dev10 bin]<span class="katex math inline">pwd
/home/tidb/tidb-tools/tidb-enterprise-tools-latest-linux-amd64/bin
[tidb@dev10 bin]</span> cat > tidb_dev2_backup.sh 
```

- - - - - -

##### 添加/编辑 定时任务

```
# For details see man 4 crontabs

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name  command to be executed

```

```ruby
[tidb@dev10 bin]<span class="katex math inline">crontab -e
# 每天凌晨一点钟执行一次这个脚本
00 01 * * * /home/tidb/tidb-tools/tidb-enterprise-tools-latest-linux-amd64/bin/tidb_dev2_backup.sh
:wq!

[tidb@dev10 bin]</span>
[tidb@dev10 bin]$

```

- - - - - -

##### crontab 常用语句

```ruby
# 查看定时任务列表
[tidb@dev10 bin]<span class="katex math inline">crontab -l

# 查看crontab日志
[tidb@dev10 bin]</span> tail -100f /var/log/cron

# 查看crontab服务状态：
[tidb@dev10 bin]<span class="katex math inline">systemctl status crond

# 手动启动crontab服务：
[tidb@dev10 bin]</span> systemctl start crond

# 重启crontab服务
[tidb@dev10 bin]$ systemctl restart crond

```