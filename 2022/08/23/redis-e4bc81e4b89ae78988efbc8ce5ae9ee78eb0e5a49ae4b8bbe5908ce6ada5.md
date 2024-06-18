---
title: 'Redis 企业版，实现多主数据同步'
date: '2022-08-23T02:50:01+00:00'
status: publish
permalink: /2022/08/23/redis-%e4%bc%81%e4%b8%9a%e7%89%88%ef%bc%8c%e5%ae%9e%e7%8e%b0%e5%a4%9a%e4%b8%bb%e5%90%8c%e6%ad%a5
author: 毛巳煜
excerpt: ''
type: post
id: 9173
category:
    - Redis
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
##### 前提条件

- CentOS 7.9
- CPU 8核
- MEM 16G
- 硬盘 400G
- **主机01**：192.168.101.21
- **主机02**：192.168.101.22

**这里测试中使用了 `2个主机` ，多个主机的配置方式除了 `FQDN` 的配置方式不同，其它都没区别**

- - - - - -

- - - - - -

- - - - - -

##### 在**主机01**安装第一个 **`主Redis`**

> - 使用docker-compose部署

```ruby
cat > docker-compose.yaml 
```

- - - - - -

- - - - - -

- - - - - -

##### 在**主机02**安装第二个 **`主Redis`**

> - 使用docker-compose部署

```ruby
cat > docker-compose.yaml 
```

- - - - - -

- - - - - -

- - - - - -

##### [参考官网](https://docs.redis.com/latest/rs/databases/active-active/get-started-active-active/ "参考官网")配置集群

- - - - - -

- - - - - -

- - - - - -

##### 测试

###### 在**主机01**上执行

```ruby
docker-compose exec rp1_node1  redis-cli -p 12000

127.0.0.1:12000> set key1 123
OK

127.0.0.1:12000> get key1
"123"


```

###### 在**主机02**上执行

```ruby
docker-compose exec rp2_node2  redis-cli -p 12000

127.0.0.1:12000> get key1
"123"


```

- - - - - -

- - - - - -

- - - - - -

##### **多主网络图**

<div style="overflow:hidden; clear:both; width: 100%; height: 40px; position: relative;">- - - - - -

 <span style="position: absolute;top: 50%;left: 50%; transform: translate(-50%, -50%); background-color: white;">以下为隐藏内容</span> </div> [![](http://qiniu.dev-share.top/image/png/RedisLabs-Active-Active.png)](http://qiniu.dev-share.top/image/png/RedisLabs-Active-Active.png)

**容器内域名映射**  
[![](http://qiniu.dev-share.top/image/png/RedisLabs-Active-Active-hosts.png)](http://qiniu.dev-share.top/image/png/RedisLabs-Active-Active-hosts.png)

- - - - - -

- - - - - -

- - - - - -