---
title: "MySQL 备份/数据批量指定恢复"
date: "2019-03-22"
categories: 
  - "mysql"
---

##### 备份脚本

`mysql -h IP地址 -u 用户名 -p'密码' -e "show databases" | grep -Ev "要过滤的数据库" | xargs mysqldump -h IP地址 -u 用户名 -p'密码' --single-transaction --databases | gzip > /保存的路径/$(用日期做文件名).sql.gz`

```shell
mysql -h 172.21.60.210 -u root -p'数据库密码' -e "show databases" | grep -Ev "Database|information_schema|mysql|performance_schema|tidb_loader|test"|xargs mysqldump -h 172.21.60.210 -u root -p'数据库密码' --single-transaction --databases | gzip > /home/mysql/backup/$(date +%Y%m%d).sql.gz
```

* * *

##### 恢复脚本

```ruby
[tidb@dev10 bin]$  cat > dump.sh << eric
#!/bin/bash

# 用法 /dump.sh 数据库名 ip port

mkdir -p dist/schema dist/sql

database=\$1
ip=\$2
port=\$3

# 批量恢复表
for file in \`ls dist/schema\`
do
  mysql -h \$ip -u root -P \$port -p'q1w2E#R\$' \${database} < "dist/schema/\$file"
  echo mysql -h \$ip -u root -P \$port \${database} \< "dist/schema/\$file"
  echo
done
echo '====================================='
echo '============ 表恢复完成! ============'
echo '====================================='
echo


# 批量恢复数据
for file in \`ls dist/sql\`
do
  mysql -h \$ip -u root -P \$port -p'q1w2E#R\$' \${database} < "dist/sql/\$file"
  echo mysql -h \$ip -u root -P \$port \${database} \< "dist/sql/\$file"
  echo
done

echo '======================================='
echo '============ 数据恢复完成! ============'
echo '======================================='
eric

[tidb@dev10 bin]$
```
