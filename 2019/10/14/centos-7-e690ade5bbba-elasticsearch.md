---
title: 'CentOS 7 搭建 ElasticSearch'
date: '2019-10-14T09:51:44+00:00'
status: publish
permalink: /2019/10/14/centos-7-%e6%90%ad%e5%bb%ba-elasticsearch
author: 毛巳煜
excerpt: ''
type: post
id: 5071
category:
    - ElasticSearch
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### [ElasticSearch官网](https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started-install.html "ElasticSearch官网")

###### [国内镜像下载](https://thans.cn/mirror/elasticsearch.html "国内镜像下载")

##### 环境

- IP: 172.160.180.46
- 系统： CentOS 7.6

<table><thead><tr><th>HostName</th><th>IP</th><th>DES</th></tr></thead><tbody><tr><td>test1</td><td>172.160.180.46</td><td>主控机</td></tr><tr><td>test2</td><td>172.160.180.47</td><td>node-1</td></tr><tr><td>test3</td><td>172.160.180.48</td><td>node-2</td></tr><tr><td>test4</td><td>172.160.181.18</td><td>node-3</td></tr></tbody></table>

###### 修改hosts

```ruby
[root@test1 ~]# cat >> /etc/hosts 
```

##### 1. 创建用户

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

##### 2. 下载/解压

```ruby
[elasticsearch@test1 ~]<span class="katex math inline">export ES_VERSION=7.12.1

[elasticsearch@test1 ~]</span> mkdir -p /home/elasticsearch/deploy && cd /home/elasticsearch/deploy


[elasticsearch@test1 deploy]<span class="katex math inline">wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-</span>ES_VERSION-linux-x86_64.tar.gz


[elasticsearch@test1 deploy]<span class="katex math inline">tar -zxvf elasticsearch-</span>ES_VERSION-linux-x86_64.tar.gz

```

##### 3. 替换配置文件中如下部分属性

**注意：** 不修改配置，是不可以外网访问的，如下属性都是必须要配置的

```ruby
[elasticsearch@test1 deploy]<span class="katex math inline">cat > /home/elasticsearch/deploy/elasticsearch-</span>ES_VERSION/config/elasticsearch.yml 
```

##### 4. 将 ElasticSearch 启动交给操作系统管理

###### 创建启动文件

```ruby
[root@test1 ~]# cat > /etc/systemd/system/elasticsearch.service 
```

```ruby
# 授权
[elasticsearch@test1 ~]<span class="katex math inline">sudo chmod -R 777 /etc/systemd/system/elasticsearch.service

# 重新加载systemd 守护线程
[elasticsearch@test1 ~]</span> sudo systemctl daemon-reload

# 开机自启动
## 开机前最后先测试一下能不能启动成功
### 测试执行启动 export ES_VERSION=7.12.1 && /home/elasticsearch/deploy/elasticsearch-<span class="katex math inline">ES_VERSION/bin/elasticsearch
[elasticsearch@test1 ~]</span> sudo systemctl start elasticsearch && sudo systemctl enable elasticsearch && systemctl status elasticsearch

```

- - - - - -

##### 5. 查看启动是否成功

```ruby
[elasticsearch@test1 ~]<span class="katex math inline">curl node-1:9200
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
[elasticsearch@test1 ~]</span>

```

- - - - - -

##### 常见问题

###### 1 bootstrap checks failed

```ruby
ERROR: [3] bootstrap checks failed
[1]: max file descriptors [4096] for elasticsearch process is too low, increase to at least [65535]
[2]: max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]
[3]: the default discovery settings are unsuitable for production use; at least one of [discovery.seed_hosts, discovery.seed_providers, cluster.initial_master_nodes] must be configured

```

**原因**：虚拟机限制用户的执行内存  
**解决问题\[1\]\[3\]**：在文件末尾追加配置

```ruby
[elasticsearch@test1 deploy]$ sudo cat >> /etc/security/limits.conf 
```

**解决问题\[2\]**：在文件末尾追加配置

```ruby
[elasticsearch@test1 deploy]$ sudo cat >> /etc/sysctl.conf 
```

- - - - - -

- - - - - -

- - - - - -

###### [ElasticSearch 安装插件](http://www.dev-share.top/2019/10/24/elasticsearch-%E5%AE%89%E8%A3%85%E6%8F%92%E4%BB%B6/ "ElasticSearch 安装插件")

###### [部署 ElasticSearch 集群](http://www.dev-share.top/2019/10/17/ansible-playbook-%E9%83%A8%E7%BD%B2-elasticsearch-%E9%9B%86%E7%BE%A4/ "部署 ElasticSearch 集群")

###### [安装 elasticsearch-head](http://www.dev-share.top/2019/10/15/centos-7-%E5%AE%89%E8%A3%85-elasticsearch-head/ "安装 elasticsearch-head")

###### [安装 ElasticHD](http://www.dev-share.top/2019/10/15/centos-7-%E5%AE%89%E8%A3%85-elastichd/ "安装 ElasticHD")

###### [安装 kibana](http://www.dev-share.top/2019/10/15/centos-7-%E5%AE%89%E8%A3%85-kibana/ "安装 kibana")

- - - - - -

- - - - - -

- - - - - -

##### **`相关资料`**

[ES图解](http://developer.51cto.com/art/201904/594615.htm "ES图解")

[ES这个说的很明白](http://developer.51cto.com/art/201904/594615.htm "ES 这个说的很明白")

[ES数据存储](https://elasticsearch.cn/article/6178 "ES数据存储")

[ES官方 JavaAPI](https://www.elastic.co/guide/en/elasticsearch/client/java-rest/7.3/java-rest-high-document-index.html "ES 官方 JavaAPI")

[Elasticsearch7.X为什么移除类型(Type)](https://www.cnblogs.com/wangzhen3798/p/10765202.html "Elasticsearch7.X为什么移除类型(Type)")