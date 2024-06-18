---
title: "二进制 安装 influxdb"
date: "2020-09-22"
categories: 
  - "influxdb"
---

###### **[官方地址](https://portal.influxdata.com/downloads/ "官方地址")**

* * *

###### 下载安装

```ruby
# 官网下载
wget https://dl.influxdata.com/influxdb/releases/influxdb-1.8.2.x86_64.rpm

# 七牛云下载
wget http://qiniu.dev-share.top/influxdb-1.8.2.x86_64.rpm

# 安装
rpm -ivh influxdb-1.8.2.x86_64.rpm
```

* * *

###### 启动

**`注意` 启动之前，要确定`是否需要调整`数据存储的目录到更大的硬盘下**

```ruby
vim /etc/influxdb/influxdb.conf
### Welcome to the InfluxDB configuration file.

###
### [meta]
###
[meta]
  # 用于存储数据库的一些元数据，meta 目录下有一个 meta.db 文件
  dir = "/var/lib/influxdb/meta"


###
### [data]
###

[data]
  # 存放实际存储的数据文件，以 .tsm 结尾。
  dir = "/var/lib/influxdb/data"

  # 存放预写日志文件，以 .wal 结尾
  wal-dir = "/var/lib/influxdb/wal"

  #
  series-id-set-cache-size = 100


###
### [http]
###

[http]
  # Determines whether HTTP endpoint is enabled.
  # enabled = true

  # Determines whether the Flux query endpoint is enabled.
  # flux-enabled = false

  # Determines whether the Flux query logging is enabled.
  # flux-log-enabled = false

  # 修改端口 需要 enabled = true
  # bind-address = ":8086"

  # 是否启用 用户身份验证
  # auth-enabled = false


#### 以下为使用属性已经删除 。。。。。。

```

```ruby
systemctl start influxdb && systemctl enable influxdb && systemctl status influxdb

# 查看
[root@mao-controllor ~]# influx
Connected to http://localhost:8086 version 1.8.2
InfluxDB shell version: 1.8.2
>
> show users
user admin
---- -----
>
```

* * *

* * *

* * *

##### 建立root用户

```ruby
##### 删除用户语句
> DROP USER root
>

##### 创建root用户并授权
> CREATE USER "root" with PASSWORD '123456' WITH ALL privileges
>

> show users
user admin
---- -----
root true
>

```

* * *

###### 修改配置文件, 开启身份验证

```ruby
sed -i s/'# auth-enabled = false'/'auth-enabled = true'/g /etc/influxdb/influxdb.conf && systemctl restart influxdb
```

* * *

###### 连接数据库

```ruby
influx -host 192.168.2.10 -username root -password 123456 -port 8086
```

* * *

* * *

* * *

###### 只安装客户端，不安装数据库

```ruby
# 七牛云下载
wget http://qiniu.dev-share.top/influx -P /usr/local/bin && chmod -R 755 /usr/local/bin/influx

# 测试运程连接
[root@mao-controllor ~]# influx -host 192.168.2.10 -port 8086
Connected to http://192.168.2.10:8086 version 1.8.2
InfluxDB shell version: 1.8.2
>
```

* * *

* * *

* * *

##### [Node.js 操作InfluxDB 代码](https://gitee.com/eric-mao/node-js-server.git "Node.js 操作InfluxDB 代码")

* * *

* * *

* * *
