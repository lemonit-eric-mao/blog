---
title: "docker-compose 安装kibana"
date: "2021-08-10"
categories: 
  - "elk"
---

###### kibana.yml

```yaml
cat > config/kibana.yml << ERIC
elasticsearch.hosts: http://172.16.15.162:9200
server.host: "0.0.0.0"
server.name: kibana
xpack.monitoring.ui.container.elasticsearch.enabled: true
# 中文
i18n.locale: zh-CN

ERIC

```

* * *

* * *

* * *

###### docker-compose.yaml

```ruby
cat > docker-compose.yaml << ERIC
version: "3.1"
services:
  kibana:
    image: kibana:7.9.2
    container_name: kibana
    restart: always
    volumes:
      - ./config/kibana.yml:/usr/share/kibana/config/kibana.yml:rw
      # 插件提前下载好，放到这个目录下./plugins
      - ./plugins:/plugins:rw
    ports:
      - 5601:5601
    environment:
      TZ: Asia/Shanghai

ERIC


docker-compoes up -d

```

* * *

###### **安装插件**

`插件的版本一定要与kibana版本一致` **示例中的logtrail插件在新版本中已经内置， 可在`Observability --> 日志`查看**

```ruby
## 进入容器
docker exec -it kibana bash

## 在容器内安装插件
bin/kibana-plugin install -d /usr/share/kibana/plugins file:///plugins/logtrail-7.9.2-0.1.31.zip
```

* * *

* * *

* * *
