---
title: "docker-compose 安装  Neo4j"
date: "2020-10-20"
categories: 
  - "neo4j"
---

###### **[DockerHub](https://hub.docker.com/_/neo4j?tab=description "DockerHub")**

* * *

###### **[Neo4j应用场景](https://www.jianshu.com/p/500448f810c5?from=groupmessage "Neo4j应用场景")**

* * *

###### 创建文件夹

```ruby
mkdir -p /home/deploy/neo4j && cd /home/deploy/neo4j
```

* * *

###### docker-compose.yaml

```ruby
cat > docker-compose.yaml << ERIC

version: '3.1'
services:
  neo4j:
    image: neo4j:4.1.3
    restart: always
    container_name: neo4j
    ports:
      # 访问数据库用的端口
      - 7474:7474
      - 7687:7687
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - ./config/data:/data
      - ./config/logs:/logs

    environment:
      TIME_ZONE: Asia/Shanghai
      NEO4J_dbms_memory_heap_maxSize: 4G
      # 用户名/密码
      NEO4J_AUTH: neo4j/123456

ERIC

```

* * *

* * *

* * *

###### 测试查看

http://127.0.0.1:7474

* * *

* * *

* * *
