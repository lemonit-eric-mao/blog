---
title: 'docker-compose 安装kibana'
date: '2021-08-10T08:43:09+00:00'
status: private
permalink: /2021/08/10/docker-compose-%e5%ae%89%e8%a3%85kibana
author: 毛巳煜
excerpt: ''
type: post
id: 7691
category:
    - ELK
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### kibana.yml

```yaml
cat > config/kibana.yml 
```

- - - - - -

- - - - - -

- - - - - -

###### docker-compose.yaml

```ruby
cat > docker-compose.yaml 
```

- - - - - -

###### **安装插件**

`插件的版本一定要与kibana版本一致`  
**示例中的logtrail插件在新版本中已经内置， 可在`Observability --> 日志`查看**

```ruby
## 进入容器
docker exec -it kibana bash

## 在容器内安装插件
bin/kibana-plugin install -d /usr/share/kibana/plugins file:///plugins/logtrail-7.9.2-0.1.31.zip

```

- - - - - -

- - - - - -

- - - - - -