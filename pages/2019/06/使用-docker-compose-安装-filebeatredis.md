---
title: "使用 docker-compose 安装 filebeat+redis"
date: "2019-06-27"
categories: 
  - "elk"
---

[安装 docker-compose](https://www.lemonit.cn/2019/06/12/%E5%AE%89%E8%A3%85-docker-compose/ "安装 docker-compose")

##### 准备 创建文件夹

```ruby
[root@k8s-master ~]# mkdir -p /home/deploy/filebeat/config/data
[root@k8s-master ~]# mkdir -p /home/deploy/filebeat/config/redis
```

##### 配置 docker-compose.yml

```ruby
[root@k8s-master filebeat]# pwd
/home/deploy/filebeat
[root@k8s-master filebeat]# cat > docker-compose.yml << eric
version: '3'

services:

  filebeat:
    image: prima/filebeat:5.6.1
    hostname: filebeat
    container_name: filebeat
    restart: always
    volumes:
      - './config/filebeat.yml:/filebeat.yml'
      - '~/dockerdata/filebeat:/data'
      - '/var/lib/docker/containers:/var/lib/docker/containers'

  redis:
    image: redis:latest
    hostname: redis
    container_name: redis
    restart: always
    ports:
      # 端口映射
      - '6379:6379'
    volumes:
      # 目录映射
      - './config/redis/redis.conf:/usr/local/etc/redis/redis.conf'
      - './config/data:/data'
    # 在容器中执行的命令
    command: redis-server /usr/local/etc/redis/redis.conf
eric

[root@k8s-master filebeat]#
```

##### 添加 redis 配置 redis.conf

```ruby
[root@k8s-master redis]# pwd
/home/deploy/filebeat/config/redis
[root@k8s-master redis]# cat > redis.conf << eric
# 给redis添加密码
requirepass maosiyu1987
eric
[root@k8s-master redis]#
```

##### 添加 filebeat.yml

```ruby
[root@k8s-master config]# pwd
/home/deploy/filebeat/config
[root@k8s-master config]# cat > filebeat.yml << eric
filebeat.prospectors:

- input_type: log

  paths:
    - /var/log/messages
    - /var/log/*.log
    - /var/log/containers/*.log
    - /var/lib/docker/containers/*/*.log
  tags: ["sinoeyes-io-dev1"]
  # 因为docker使用的log driver是json-file，因此采集到的日志格式是json格式，设置为true之后，filebeat会将日志进行json_decode处理
  json.add_error_key: true
  #如果启用此设置，则在出现JSON解组错误或配置中定义了message_key但无法使用的情况下，Filebeat将添加“error.message”和“error.type：json”键。
  json.message_key: log
  #一个可选的配置设置，用于指定应用行筛选和多行设置的JSON密钥。 如果指定，键必须位于JSON对象的顶层，且与键关联的值必须是字符串，否则不会发生过滤或多行聚合。
  tail_files: true
  # 将error日志合并到一行
  multiline.pattern: '^([0-9]{4}|[0-9]{2})-[0-9]{2}'
  multiline.negate: true
  multiline.match: after
  bulk_max_size: 1024

output.redis:
  # Array of hosts to connect to.
   hosts: ["k8s.dev-share.top"]
   port: 6379
   password: "sinoeyes"
   key: "sinoeyes-io"
   db: 4
   dataytpe: "list"
   # filebeat向redis的推送超时时间
   timeout: 60
eric

[root@k8s-master config]#
```

##### 启动

```ruby
[root@k8s-master filebeat]# pwd
/home/deploy/filebeat
[root@k8s-master filebeat]# ll
total 8
drwxr-xr-x 4 root root 4096 Jun 27 17:08 config
-rwxr-xr-x 1 root root  987 Jun 27 16:05 docker-compose.yml
[root@k8s-master filebeat]#
[root@k8s-master filebeat]# docker-compose up -d
```
