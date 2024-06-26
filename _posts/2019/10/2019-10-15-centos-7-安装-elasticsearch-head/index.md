---
title: "CentOS 7 安装 elasticsearch-head"
date: "2019-10-15"
categories: 
  - "elasticsearch"
---

##### 环境

- IP: 172.160.180.46
- 系统： CentOS 7.6

| 服务器 | IP | hostname |
| --- | --- | --- |
| ES-Master | 172.160.180.46 | test1 |
| ES-Node | 172.160.180.47 | test2 |
| ES-Node | 172.160.180.48 | test3 |
| ES-Node | 172.160.181.18 | test4 |

##### docker-compose部署

```ruby
cat > docker-compose.yaml << ERIC
version: '3.6'

services:
  es-head:
    image: mobz/elasticsearch-head:5
    container_name: es-head
    ports:
      - 9100:9100
    environment:
      TZ: Asia/Shanghai

ERIC


docker-compose up -d


docker exec es-head bash -c "sed -i 's/application\/x-www-form-urlencoded/application\/json;charset=UTF-8/g' /usr/src/app/_site/vendor.js"

```

* * *

* * *

* * *

* * *

* * *

* * *

##### 二进制安装

下载地址：https://github.com/mobz/elasticsearch-head

###### [安装node.js](http://www.dev-share.top/2017/11/16/node-js-%E5%AE%89%E8%A3%85/ "安装node.js")

##### 下载/解压

```ruby
[elasticsearch@test1 deploy]$ wget https://codeload.github.com/mobz/elasticsearch-head/zip/v5.0.0 -O es-head.zip
[elasticsearch@test1 deploy]$
[elasticsearch@test1 deploy]$ unzip -o es-head.zip
[elasticsearch@test1 deploy]$
```

##### 初始化

```ruby
[elasticsearch@test1 elasticsearch-head-5.0.0]$ pwd
/home/elasticsearch/deploy/elasticsearch-head-5.0.0
[elasticsearch@test1 elasticsearch-head-5.0.0]$
[elasticsearch@test1 elasticsearch-head-5.0.0]$ npm i
[elasticsearch@test1 elasticsearch-head-5.0.0]$
[elasticsearch@test1 elasticsearch-head-5.0.0]$ npm start
```

##### webURL: 172.160.180.46:9100

* * *

* * *

* * *

##### `常见问题`

`es7 Content-Type header [application/x-www-form-urlencoded] is not supported` 需要修改 es-head 中的文件\_site/vendor.js，替换解析头

```ruby
sed -i 's/application\/x-www-form-urlencoded/application\/json;charset=UTF-8/g' ./_site/vendor.js
```

* * *

* * *

* * *

* * *

* * *

* * *
