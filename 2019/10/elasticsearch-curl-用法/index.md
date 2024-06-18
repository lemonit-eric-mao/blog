---
title: "ElasticSearch curl 用法"
date: "2019-10-24"
categories: 
  - "elasticsearch"
---

##### **`注意说明`**

**新增数据异常**：`Root mapping definition has unsupported parameters` 出现这个的原因是，elasticsearch7默认不在支持指定索引类型，默认索引类型是`_doc`，如果想改变，则配置`include_type_name: true` 即可(这个没有测试，官方文档说的，无论是否可行，建议不要这么做，因为elasticsearch8后就不在提供该字段)。 官方文档：https://www.elastic.co/guide/en/elasticsearch/reference/current/removal-of-types.html

[Elasticsearch7.X为什么移除类型(Type)](https://www.cnblogs.com/wangzhen3798/p/10765202.html "Elasticsearch7.X为什么移除类型(Type)")

###### JSON 查询条件，理解

```json
// 例子
{
  "query": {
    "range": {
      "paasUpdateTime": {
        "gte": "2020-03-29",
        "lte": "2020-03-30"
      }
    }
  }
}

// 解释
{
  "动作[增|删|改|查]": {
    "命令[范围查询|全表查询|过滤|等等...]": {
      "属性": {
        "与属性相关的[条件|值]"
      }
    }
  }
}
```

* * *

* * *

###### 1\. 创建索引(创建数据库）, 默认类型为`_doc`

```ruby
[elasticsearch@test1 deploy]$ curl -X PUT http://172.160.180.47:9200/schema_1 -H "Content-Type: application/json" -d '
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 2
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "keyword"
      },
      "years": {
        "type": "keyword"
      },
      "author": {
        "type": "keyword"
      },
      "content": {
        "type": "text",
        "analyzer": "hanlp"
      }
    }
  }
}'
```

* * *

* * *

###### 2\. 新增数据

###### 2.1 新增数据(POST)，id由ES自动生成

```ruby
[elasticsearch@test1 deploy]$ curl -X POST http://172.160.180.47:9200/schema_1/_doc -H "Content-Type: application/json" -d '
{
  "title": "秋雨叹",
  "years": "唐代",
  "author": "杜甫",
  "content": "雨中百草秋烂死，阶下决明颜色鲜。著叶满枝翠羽盖，开花无数黄金钱。凉风萧萧吹汝急，恐汝后时难独立。堂上书生空白头，临风三嗅馨香泣。"
}'
```

* * *

###### 2.2 插入数据(PUT)，如果存在就替换

```ruby
[elasticsearch@test1 deploy]$ curl -X PUT http://172.160.180.47:9200/schema_1/_doc/id_1 -H "Content-Type: application/json" -d '
{
  "title": "临江仙",
  "years": "宋",
  "author": "苏轼",
  "content": "谁道东阳都瘦损，凝然点漆精神。瑶林终自隔风尘。试看披鹤氅，仍是谪仙人。省可清言挥玉尘，真须保器全真。风流何似道家纯。不应同蜀客，惟爱卓文君。"
}'
```

* * *

* * *

###### 3 查询带有分词器的列(POST)

```ruby
[elasticsearch@test1 deploy]$ curl -X POST http://172.160.180.47:9200/schema_1/_search -H "Content-Type: application/json" -d '
{
  "query": {
    "match_phrase": {
      "content": "阶下决明"
    }
  },
  "highlight": {
    "type": "unified",
    "number_of_fragments": 3,
    "fields": {
      "content": {}
    }
  }
}'
```

**在查询参数中添加 `highlight:{......}`，可以看到分词匹配的结果，程序使用时不需要添加**

* * *

###### 4 查询 某个字段为 null 的数据

查询索引为`schema_1`中，字段`userName`**为null**的数据

```ruby
curl -X POST http://172.160.180.35:9200/schema_1/_search -H "Content-Type: application/json" -d '
{
  "query": {
    "bool": {
      "must_not": {
        "exists": {
          "field": "userName"
        }
      }
    }
  }
}'
```

* * *

###### 5 查询索引为`schema_1`中，字段`userName`**不为null**的数据

```ruby
curl -X POST http://172.160.180.35:9200/schema_1/_search -H "Content-Type: application/json" -d '
{
  "query": {
    "bool": {
      "must": {
        "exists": {
          "field": "userName"
        }
      }
    }
  }
}'
```

* * *

###### 6 根据时间范围查询

```ruby
curl -X POST http://172.160.180.35:9200/schema_1/_search -H "Content-Type: application/json" -d '
{
  "query": {
    "range": {
      "paasUpdateTime": {
        "gte": "2020-03-29",
        "lte": "2020-03-30"
      }
    }
  }
}
```
