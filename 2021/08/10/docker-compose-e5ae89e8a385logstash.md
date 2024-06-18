---
title: 'docker-compose 安装logstash'
date: '2021-08-10T08:16:02+00:00'
status: private
permalink: /2021/08/10/docker-compose-%e5%ae%89%e8%a3%85logstash
author: 毛巳煜
excerpt: ''
type: post
id: 7688
category:
    - ELK
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
### 工作原理图

[![](http://qiniu.dev-share.top/image/Logstash.png)](http://qiniu.dev-share.top/image/Logstash.png)

> [Logstash 目前版本没有集群这一概念](https://elasticsearch.cn/question/5399)
> 
>  因为logstash至少到目前为止，都是一个无状态的流处理软件。如果问logstash怎么集群配置，就好比问nginx怎么集群配置一样——横向扩展，自己用配置管理工具分发就是了，他们内部并没有交流。
> 
> - **`Logstash`** 的 **`消息输入`** 支持两种模式：**`推模式`和`拉模式`**。 
>   - **`推模式`** 是指 Logstash `被动`等待其它组件向它发送消息。常用的推送协议有 Beats、Syslog、TCP/UDP 等。
>   - **`拉模式`** 是指 Logstash `主动`从消息来源拉取消息。常用的拉取协议有 Kafka、JMS、RabbitMQ 等。
> - **`推模式`**，可以基于HAProxy+Keepalive实现`负载均衡+高可用`实现
> - **`拉模式`**，目前只能独立拉取数据源信息。

- - - - - -

- - - - - -

- - - - - -

### logstash.conf

```yaml
# 输入
input {

  kafka {
    # kafka集群节点列表
    bootstrap_servers => "172.16.15.162:9092,172.16.15.163:9092,172.16.15.214:9092"
    # 精确写法，订阅名为test-mssp,uat-mssp的topic，它会自己在kafka中创建topic
    topics => ["test-mssp","uat-mssp"]
    # 正则写法
    #topics_pattern => "*-mssp"

    # 设置组为logstash
    group_id => "logstash"
    # 转换为json
    codec => json
  }
}

# 过滤分词等都在这里配置，暂时未配置
filter {

}

# 输出
output {

  elasticsearch {
    # ES地址
    hosts => ["172.16.15.162:9200","172.16.15.163:9200","172.16.15.214:9200"]
    # 输出到es的索引名称，这里是每天一个索引
    index => "%{[fields][namespace]}-logs-%{+YYYY.MM.dd}"
    #user => "elastic"
    #password => "elastic password"
  }

  stdout {
    codec => rubydebug
  }
}


```

- - - - - -

- - - - - -

- - - - - -

### logstash.yml

```yaml
http.host: "0.0.0.0"

```

- - - - - -

- - - - - -

- - - - - -

### docker-compose.yaml

```ruby
cat > docker-compose.yaml 
```

- - - - - -

- - - - - -

- - - - - -