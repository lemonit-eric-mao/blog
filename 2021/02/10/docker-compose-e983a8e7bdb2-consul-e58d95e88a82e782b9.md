---
title: 'docker-compose 部署 Consul 单节点'
date: '2021-02-10T03:52:41+00:00'
status: publish
permalink: /2021/02/10/docker-compose-%e9%83%a8%e7%bd%b2-consul-%e5%8d%95%e8%8a%82%e7%82%b9
author: 毛巳煜
excerpt: ''
type: post
id: 6904
category:
    - Consul
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### Consul 环境配置

<table><thead><tr><th>用途</th><th>IP</th><th>操作系统</th></tr></thead><tbody><tr><td>Consul服务端</td><td>10.249.58.10</td><td>CentOS 7.8</td></tr><tr><td>Consul客户端</td><td>10.249.58.9</td><td>CentOS 7.8</td></tr></tbody></table>

- - - - - -

- - - - - -

- - - - - -

###### **[安装 DockerCompose](http://www.dev-share.top/2019/06/12/%e5%ae%89%e8%a3%85-docker-compose/ "安装 DockerCompose")**

- - - - - -

##### Consul 安装部署

**[配置参数官方文档](https://www.consul.io/docs/agent/options "配置参数官方文档")**

**`-bootstrap`** 此标志用于控制服务器是否处于“引导”模式。。在此模式下， **每个** 数据中心最多只能运行一台服务器，这一点很重要。从技术上讲，引导模式下的服务器可以自动选择为Raft领导者。重要的是，只有单个节点处于此模式。否则，由于多个节点能够自行选择，因此无法保证一致性。 **`不建议在引导群集后使用此标志`** 。

**`-bootstrap-expect`** 此标志提供数据中心中预期的服务器数量， **`1`表示单节点** 。要么不提供此值，要么该值必须与集群中的其他服务器一致。如果提供，Consul会一直等到指定数量的服务器可用为止，然后引导群集。这样可以自动选出最初的领导者。不能与旧 **`-bootstrap`** 标志一起使用。该标志需要 **`-server`** 模式。

**`-bind=`** 绑定内部集群通信的地址。 **`通常是当前服务器的内网IP地址`** 。这是群集中所有其它节点可访问的IP地址。

**`-client=`** Consul将客户端接口（包括HTTP和DNS服务器）绑定到的地址； `0.0.0.0` 表示任何地址可以访问。

**`-datacenter=`** 告诉Agent在哪个数据中心运行。这里的数据中心只是给Consul集群加上一个标识，标明这些主机的所属集群。

**`-server`** 告诉Agent是以服务器的模式运行，还是以客户端模式运行。

**`-retry-join=`** 作用有二： 其一，告诉Agent客户端要关联的服务端地址； 其二，告诉Agent服务端要关联的 **`Leader`** 服务端地址。在局域网中使用 **`LAN`**

**`-retry-join-wan=`** 作用与 `-retry-join` 相同。在 **`跨`** 局域网时使用 **`WAN`**

**`-join-wan=`** 作用将一个集群加入到另一个集群， 实现多集群统一管理

**`-ui`** 提供web管理功能，客户端与服务端皆可启用：http://{ip}:8500/

- - - - - -

###### 创建服务端配置文件 ACL\_SERVER.json

```json
cat > ./config/ACL_SERVER.json 
```

- - - - - -

###### 安装服务端 docker-compose.yaml

```yaml
cat > docker-compose.yaml 
```

- - - - - -

- - - - - -

- - - - - -

###### 创建客户端配置文件 ACL\_CLIENT.json

```json
cat > ./config/ACL_CLIENT.json 
```

- - - - - -

###### 安装客户端 docker-compose.yaml

```yaml
cat > docker-compose.yaml 
```

- - - - - -

- - - - - -

- - - - - -