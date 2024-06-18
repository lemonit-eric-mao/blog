---
title: "TiDB 定时备份"
date: "2019-08-23"
categories: 
  - "tidb"
---

##### 编写定时任务要执行的脚本

```ruby
[tidb@dev10 bin]$ pwd
/home/tidb/tidb-tools/tidb-enterprise-tools-latest-linux-amd64/bin
[tidb@dev10 bin]$ cat > tidb_dev2_backup.sh << eric
#!/bin/bash

## 所有路径都要写绝对路径
# 执行数据库备份(解压时使用 gunzip *.gz)
/home/tidb/tidb-tools/tidb-enterprise-tools-latest-linux-amd64/bin/mydumper -h 172.160.180.33 -u root -p 数据库密码 -P 4000 -c -t 16 -r 5000 -x '^(?!(mysql|test|INFORMATION_SCHEMA|PERFORMANCE_SCHEMA|tidb_loader))' --skip-tz-utc -o /home/tidb/tidb-tools/tidb-enterprise-tools-latest-linux-amd64/bin/backup/tidb_dev2_backup_\$(date +%Y%m%d)/

# 删除5天前的备份文件
rm -rf /home/tidb/tidb-tools/tidb-enterprise-tools-latest-linux-amd64/bin/backup/tidb_dev2_backup_\$(date -d "5 days ago" +%Y%m%d)/
eric
[tidb@dev10 bin]$
[tidb@dev10 bin]$
[tidb@dev10 bin]$ chmod -R 755 tidb_dev2_backup.sh
[tidb@dev10 bin]$
[tidb@dev10 bin]$
```

* * *

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
[tidb@dev10 bin]$ crontab -e
# 每天凌晨一点钟执行一次这个脚本
00 01 * * * /home/tidb/tidb-tools/tidb-enterprise-tools-latest-linux-amd64/bin/tidb_dev2_backup.sh
:wq!

[tidb@dev10 bin]$
[tidb@dev10 bin]$
```

* * *

##### crontab 常用语句

```ruby
# 查看定时任务列表
[tidb@dev10 bin]$ crontab -l

# 查看crontab日志
[tidb@dev10 bin]$ tail -100f /var/log/cron

# 查看crontab服务状态：
[tidb@dev10 bin]$ systemctl status crond

# 手动启动crontab服务：
[tidb@dev10 bin]$ systemctl start crond

# 重启crontab服务
[tidb@dev10 bin]$ systemctl restart crond
```
