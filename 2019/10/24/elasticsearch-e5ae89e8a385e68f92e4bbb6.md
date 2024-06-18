---
title: 'ElasticSearch 安装插件'
date: '2019-10-24T02:51:53+00:00'
status: publish
permalink: /2019/10/24/elasticsearch-%e5%ae%89%e8%a3%85%e6%8f%92%e4%bb%b6
author: 毛巳煜
excerpt: ''
type: post
id: 5087
category:
    - ElasticSearch
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 离线安装分词器

###### [官网地址](https://github.com/KennFalcon/elasticsearch-analysis-hanlp "官网地址") 这个是HanLP为了支持ES，开发的插件

###### [官方下载地址](https://github.com/KennFalcon/elasticsearch-analysis-hanlp/releases "官方下载地址")

###### [官方收录](https://github.com/hankcs/HanLP/wiki/%E8%A1%8D%E7%94%9F%E9%A1%B9%E7%9B%AE#elasticsearch-analysis-hanlpkennfalcon "官方收录")

###### 1. 下载分词器

```ruby
[elasticsearch@test1 download]<span class="katex math inline">pwd
/home/elasticsearch/download
[elasticsearch@test1 download]</span> wget https://github.com/KennFalcon/elasticsearch-analysis-hanlp/releases/download/v7.3.2/elasticsearch-analysis-hanlp-7.3.2.zip

```

###### 2.安装到ES

###### 2.1 **`单机`**安装到ES

```ruby
[elasticsearch@test1 elasticsearch-7.3.2]$ /home/elasticsearch/deploy/elasticsearch-7.3.2/bin/elasticsearch-plugin install file:///home/elasticsearch/download/elasticsearch-analysis-hanlp-7.3.2.zip
-> Downloading file:///home/elasticsearch/download/elasticsearch-analysis-hanlp-7.3.2.zip
[=================================================] 100%
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@     WARNING: plugin requires additional permissions     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
* java.io.FilePermission > read,write,delete
* java.lang.RuntimePermission getClassLoader
* java.lang.RuntimePermission setContextClassLoader
* java.net.SocketPermission * connect,resolve
* java.util.PropertyPermission * read,write
See http://docs.oracle.com/javase/8/docs/technotes/guides/security/permissions.html
for descriptions of what these permissions allow and the associated risks.

Continue with installation? [y/N]y
-> Installed analysis-hanlp
[elasticsearch@test1 elasticsearch-7.3.2]$

```

###### 2.1.1 修改配置文件

1. 修改配置文件 `/home/elasticsearch/deploy/elasticsearch-7.3.2/config/jvm.options` 在文件末尾追加如下文件路径  
  `-Djava.security.policy=/home/elasticsearch/deploy/elasticsearch-7.3.2/plugins/analysis-hanlp/plugin-security.policy`
2. 修改配置文件 `/home/elasticsearch/deploy/elasticsearch-7.3.2/config/analysis-hanlp/hanlp.properties` 将root=的值改为绝对路径  
  `root=/home/elasticsearch/deploy/elasticsearch-7.3.2/plugins/analysis-hanlp/`

###### 2.2 **`集群安装`**使用ansible-playbook

```ruby
[elasticsearch@test1 deploy]$ cat > setup-plugins.yml 
```

###### 3. 重启ES

###### 4. 查看安装是否成功

```ruby
curl -X GET "http://172.160.180.47:9200/_analyze" -H "Content-Type: application/json" -d '
{
    "text": "我们大家的中华人民共和国"
}'

# 默认不使用分词器的查询结果
{
  "tokens": [
    {
      "token": "我",
      "start_offset": 0,
      "end_offset": 1,
      "type": "<ideographic>",
      "position": 0
    },
    {
      "token": "们",
      "start_offset": 1,
      "end_offset": 2,
      "type": "<ideographic>",
      "position": 1
    },
    {
      "token": "大",
      "start_offset": 2,
      "end_offset": 3,
      "type": "<ideographic>",
      "position": 2
    },
    {
      "token": "家",
      "start_offset": 3,
      "end_offset": 4,
      "type": "<ideographic>",
      "position": 3
    },
    {
      "token": "的",
      "start_offset": 4,
      "end_offset": 5,
      "type": "<ideographic>",
      "position": 4
    },
    {
      "token": "中",
      "start_offset": 5,
      "end_offset": 6,
      "type": "<ideographic>",
      "position": 5
    },
    {
      "token": "华",
      "start_offset": 6,
      "end_offset": 7,
      "type": "<ideographic>",
      "position": 6
    },
    {
      "token": "人",
      "start_offset": 7,
      "end_offset": 8,
      "type": "<ideographic>",
      "position": 7
    },
    {
      "token": "民",
      "start_offset": 8,
      "end_offset": 9,
      "type": "<ideographic>",
      "position": 8
    },
    {
      "token": "共",
      "start_offset": 9,
      "end_offset": 10,
      "type": "<ideographic>",
      "position": 9
    },
    {
      "token": "和",
      "start_offset": 10,
      "end_offset": 11,
      "type": "<ideographic>",
      "position": 10
    },
    {
      "token": "国",
      "start_offset": 11,
      "end_offset": 12,
      "type": "<ideographic>",
      "position": 11
    }
  ]
}
</ideographic></ideographic></ideographic></ideographic></ideographic></ideographic></ideographic></ideographic></ideographic></ideographic></ideographic></ideographic>
```

```ruby
curl -X GET "http://172.160.180.47:9200/_analyze" -H "Content-Type: application/json" -d '
{
    "text": "我们大家的中华人民共和国",
    "analyzer": "hanlp"
}'
# 使用分词器后的查询结果
{
  "tokens": [
    {
      "token": "我们",
      "start_offset": 0,
      "end_offset": 2,
      "type": "rr",
      "position": 0
    },
    {
      "token": "大家",
      "start_offset": 2,
      "end_offset": 4,
      "type": "rr",
      "position": 1
    },
    {
      "token": "的",
      "start_offset": 4,
      "end_offset": 5,
      "type": "ude1",
      "position": 2
    },
    {
      "token": "中华人民共和国",
      "start_offset": 5,
      "end_offset": 12,
      "type": "ns",
      "position": 3
    }
  ]
}



```