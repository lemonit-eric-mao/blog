---
title: "CentOS 7 搭建 ElasticSearch"
date: "2019-10-14"
categories: 
  - "elasticsearch"
---

##### [ElasticSearch官网](https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started-install.html "ElasticSearch官网")

###### [国内镜像下载](https://thans.cn/mirror/elasticsearch.html "国内镜像下载")

##### 环境

- IP: 172.160.180.46
- 系统： CentOS 7.6

| HostName | IP | DES |
| --- | --- | --- |
| test1 | 172.160.180.46 | 主控机 |
| test2 | 172.160.180.47 | node-1 |
| test3 | 172.160.180.48 | node-2 |
| test4 | 172.160.181.18 | node-3 |

###### 修改hosts

```ruby
[root@test1 ~]# cat >> /etc/hosts << eric
172.160.180.47  node-1
eric

[root@test1 ~]#
```

##### 1\. 创建用户

```ruby
[root@test1 ~]# useradd -m -d /home/elasticsearch elasticsearch
[root@test1 ~]# passwd elasticsearch
输入密码
passwd：所有的身份验证令牌已经成功更新。
[root@test1 ~]#
[root@test1 ~]# visudo
elasticsearch ALL=(ALL) NOPASSWD: ALL
[root@test1 ~]#
[root@test1 ~]# su - elasticsearch
[elasticsearch@test1 ~]$
```

##### 2\. 下载/解压

```ruby
[elasticsearch@test1 ~]$ export ES_VERSION=7.12.1

[elasticsearch@test1 ~]$ mkdir -p /home/elasticsearch/deploy && cd /home/elasticsearch/deploy


[elasticsearch@test1 deploy]$ wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-$ES_VERSION-linux-x86_64.tar.gz


[elasticsearch@test1 deploy]$ tar -zxvf elasticsearch-$ES_VERSION-linux-x86_64.tar.gz
```

##### 3\. 替换配置文件中如下部分属性

**注意：** 不修改配置，是不可以外网访问的，如下属性都是必须要配置的

```ruby
[elasticsearch@test1 deploy]$ cat > /home/elasticsearch/deploy/elasticsearch-$ES_VERSION/config/elasticsearch.yml << ERIC
#node.name: node-1
node.name: node-1

#network.host: 172.160.0.1
network.host: node-1

#http.port: 9200
http.port: 9200

# 允许跨域访问
http.cors.enabled: true
http.cors.allow-origin: "*"

path.data: /home/elasticsearch/deploy/elasticsearch-$ES_VERSION/data
path.logs: /home/elasticsearch/deploy/elasticsearch-$ES_VERSION/logs

# 快照路径
path.repo: /home/elasticsearch/deploy/elasticsearch-$ES_VERSION/snapshots

cluster.initial_master_nodes: ['node-1']

##优化参数
indices.memory.index_buffer_size: 20%
indices.query.bool.max_clause_count: 100000000

ERIC

```

##### 4\. 将 ElasticSearch 启动交给操作系统管理

###### 创建启动文件

```ruby
[root@test1 ~]# cat > /etc/systemd/system/elasticsearch.service << ERIC

[Unit]
Description=elasticsearch

[Service]
LimitNOFILE=1000000
LimitNPROC=1000000
LimitSTACK=10485760

User=elasticsearch

ExecStart=/home/elasticsearch/deploy/elasticsearch-$ES_VERSION/bin/elasticsearch
Restart=always
RestartSec=15s


[Install]
WantedBy=multi-user.target

ERIC

```

```ruby
# 授权
[elasticsearch@test1 ~]$ sudo chmod -R 777 /etc/systemd/system/elasticsearch.service

# 重新加载systemd 守护线程
[elasticsearch@test1 ~]$ sudo systemctl daemon-reload

# 开机自启动
## 开机前最后先测试一下能不能启动成功
### 测试执行启动 export ES_VERSION=7.12.1 && /home/elasticsearch/deploy/elasticsearch-$ES_VERSION/bin/elasticsearch
[elasticsearch@test1 ~]$ sudo systemctl start elasticsearch && sudo systemctl enable elasticsearch && systemctl status elasticsearch
```

* * *

##### 5\. 查看启动是否成功

```ruby
[elasticsearch@test1 ~]$ curl node-1:9200
{
  "name" : "node-1",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "GwWYck6bRTyyMgXFxZW9Ew",
  "version" : {
    "number" : "7.12.1",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "22e1767283e61a198cb4db791ea66e3f11ab9910",
    "build_date" : "2019-09-27T08:36:48.569419Z",
    "build_snapshot" : false,
    "lucene_version" : "8.2.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
[elasticsearch@test1 ~]$
```

* * *

##### 常见问题

###### 1 bootstrap checks failed

```ruby
ERROR: [3] bootstrap checks failed
[1]: max file descriptors [4096] for elasticsearch process is too low, increase to at least [65535]
[2]: max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]
[3]: the default discovery settings are unsuitable for production use; at least one of [discovery.seed_hosts, discovery.seed_providers, cluster.initial_master_nodes] must be configured
```

**原因**：虚拟机限制用户的执行内存 **解决问题\[1\]\[3\]**：在文件末尾追加配置

```ruby
[elasticsearch@test1 deploy]$ sudo cat >> /etc/security/limits.conf << ERIC

# BEGIN ES
*        soft     nofile         65536
*        hard     nofile         65536
*        soft     nproc          2048
*        hard     nproc          4096
# END ES

ERIC

[elasticsearch@test1 deploy]$
# 需要重新连接用户
```

**解决问题\[2\]**：在文件末尾追加配置

```ruby
[elasticsearch@test1 deploy]$ sudo cat >> /etc/sysctl.conf << ERIC

# BEGIN ES
vm.max_map_count = 262144
# END ES

ERIC

[elasticsearch@test1 deploy]$ sudo sysctl -p
# 需要重新连接用户
```

* * *

* * *

* * *

###### [ElasticSearch 安装插件](https://lemonit-eric-mao.github.io/blog/elasticsearch-%E5%AE%89%E8%A3%85%E6%8F%92%E4%BB%B6 "ElasticSearch 安装插件")

###### [部署 ElasticSearch 集群](https://lemonit-eric-mao.github.io/blog/ansible-playbook-%E9%83%A8%E7%BD%B2-elasticsearch-%E9%9B%86%E7%BE%A4 "部署 ElasticSearch 集群")

###### [安装 elasticsearch-head](https://lemonit-eric-mao.github.io/blog/centos-7-%E5%AE%89%E8%A3%85-elasticsearch-head "安装 elasticsearch-head")

###### [安装 ElasticHD](https://lemonit-eric-mao.github.io/blog/centos-7-%E5%AE%89%E8%A3%85-elastichd "安装 ElasticHD")

###### [安装 kibana](https://lemonit-eric-mao.github.io/blog/centos-7-%E5%AE%89%E8%A3%85-kibana "安装 kibana")

* * *

* * *

* * *

##### **`相关资料`**

[ES图解](http://developer.51cto.com/art/201904/594615.htm "ES图解")

[ES这个说的很明白](http://developer.51cto.com/art/201904/594615.htm "ES 这个说的很明白")

[ES数据存储](https://elasticsearch.cn/article/6178 "ES数据存储")

[ES官方 JavaAPI](https://www.elastic.co/guide/en/elasticsearch/client/java-rest/7.3/java-rest-high-document-index.html "ES 官方 JavaAPI")

[Elasticsearch7.X为什么移除类型(Type)](https://www.cnblogs.com/wangzhen3798/p/10765202.html "Elasticsearch7.X为什么移除类型(Type)")


---

---

---

## 使用docker-compose部署`单节点`
``` yaml
cat docker-compose.yaml
version: '3.6'
services:
  es01:
    image: elasticsearch:7.17.23
    container_name: es01
    environment:
      - node.name=es01
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    volumes:
      - ./data01:/usr/share/elasticsearch/data
    ports:
      - 9200:9200

```
