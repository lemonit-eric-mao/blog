---
title: 'CentOS 7 安装 elasticsearch-head'
date: '2019-10-15T08:22:27+00:00'
status: publish
permalink: /2019/10/15/centos-7-%e5%ae%89%e8%a3%85-elasticsearch-head
author: 毛巳煜
excerpt: ''
type: post
id: 5077
category:
    - ElasticSearch
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 环境

- IP: 172.160.180.46
- 系统： CentOS 7.6

<table><thead><tr><th>服务器</th><th>IP</th><th>hostname</th></tr></thead><tbody><tr><td>ES-Master</td><td>172.160.180.46</td><td>test1</td></tr><tr><td>ES-Node</td><td>172.160.180.47</td><td>test2</td></tr><tr><td>ES-Node</td><td>172.160.180.48</td><td>test3</td></tr><tr><td>ES-Node</td><td>172.160.181.18</td><td>test4</td></tr></tbody></table>

##### docker-compose部署

```ruby
cat > docker-compose.yaml 
```

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

##### 二进制安装

下载地址：https://github.com/mobz/elasticsearch-head

###### [安装node.js](http://www.dev-share.top/2017/11/16/node-js-%E5%AE%89%E8%A3%85/ "安装node.js")

##### 下载/解压

```ruby
[elasticsearch@test1 deploy]<span class="katex math inline">wget https://codeload.github.com/mobz/elasticsearch-head/zip/v5.0.0 -O es-head.zip
[elasticsearch@test1 deploy]</span>
[elasticsearch@test1 deploy]<span class="katex math inline">unzip -o es-head.zip
[elasticsearch@test1 deploy]</span>

```

##### 初始化

```ruby
[elasticsearch@test1 elasticsearch-head-5.0.0]<span class="katex math inline">pwd
/home/elasticsearch/deploy/elasticsearch-head-5.0.0
[elasticsearch@test1 elasticsearch-head-5.0.0]</span>
[elasticsearch@test1 elasticsearch-head-5.0.0]<span class="katex math inline">npm i
[elasticsearch@test1 elasticsearch-head-5.0.0]</span>
[elasticsearch@test1 elasticsearch-head-5.0.0]$ npm start

```

##### webURL: 172.160.180.46:9100

- - - - - -

- - - - - -

- - - - - -

##### `常见问题`

`es7 Content-Type header [application/x-www-form-urlencoded] is not supported`  
需要修改 es-head 中的文件\_site/vendor.js，替换解析头

```ruby
sed -i 's/application\/x-www-form-urlencoded/application\/json;charset=UTF-8/g' ./_site/vendor.js

```

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -