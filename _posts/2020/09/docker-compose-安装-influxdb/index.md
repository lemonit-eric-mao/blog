---
title: "docker-compose 安装 influxdb"
date: "2020-09-22"
categories: 
  - "influxdb"
---

###### 创建文件夹

```ruby
mkdir -p /home/deploy/influxdb/config
```

* * *

###### 修改默认配置文件

```ruby
cat > /home/deploy/influxdb/config/influxdb.conf << ERIC

### Welcome to the InfluxDB configuration file.

# Bind address to use for the RPC service for backup and restore.
# bind-address = "127.0.0.1:8088"
# 这个默认需要打开，否则 备份数据的时候会失败
bind-address = "0.0.0.0:8088"

[meta]
  # Where the metadata/raft database is stored
  dir = "/var/lib/influxdb/meta"


[data]
  # The directory where the TSM storage engine stores TSM files.
  dir = "/var/lib/influxdb/data"

  # The directory where the TSM storage engine stores WAL files.
  wal-dir = "/var/lib/influxdb/wal"

  # increase in cache size may lead to an increase in heap usage.
  series-id-set-cache-size = 100

[coordinator]

[retention]

[shard-precreation]

[monitor]

[http]
  # Determines whether user authentication is enabled over HTTP/HTTPS.
  # auth-enabled = false
  # 启用数据库认证功能
  auth-enabled = true

[logging]

[subscriber]

[[graphite]]

[[collectd]]

[[opentsdb]]

[[udp]]

[continuous_queries]

[tls]

ERIC

```

* * *

###### 创建 docker-compose.yaml

```ruby
cat > docker-compose.yaml << ERIC

version: '3.1'
services:
  influxdb:
    image: influxdb:1.8.2
    restart: always
    container_name: influxdb
    ports:
      # 访问数据库用的端口
      - 8086:8086
      # 备份数据库用的端口
      - 8088:8088
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - ./config/lib/:/var/lib/influxdb/
      - ./config/influxdb.conf:/etc/influxdb/influxdb.conf

    environment:
      TIME_ZONE: Asia/Shanghai

ERIC

```

* * *

* * *

* * *
