---
title: '使用 pd-recover 恢复PD'
date: '2019-11-14T08:33:58+00:00'
status: publish
permalink: /2019/11/14/%e4%bd%bf%e7%94%a8-pd-recover-%e6%81%a2%e5%a4%8dpd
author: 毛巳煜
excerpt: ''
type: post
id: 5130
category:
    - TiDB
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### pd.log 获取 `alloc-id`

```ruby
......
[2019/11/14 09:08:24.852 +08:00] [INFO] [id.go:91] ["idAllocator allocates a new id"] [alloc-id=5000]
......

```

##### tidb.log 获取 `cluster-id`

```ruby
......
[2019/11/14 16:10:58.291 +08:00] [INFO] [client.go:163] ["[pd] init cluster id"] [cluster-id=6759063543423042264]
......

```

##### 根据官方文档操作有些不清楚

[PD Recover 使用文档](https://pingcap.com/docs-cn/dev/reference/tools/pd-recover/#pd-recover-%E4%BD%BF%E7%94%A8%E6%96%87%E6%A1%A3 "PD Recover 使用文档")  
**`工具的位置：`** `/home/tidb/tidb-ansible/resources/bin/pd-recover`

##### 参数说明

```
  -alloc-id uint
        指定比原集群已分配过的 ID 更大的数
        在指定 alloc-id 时需指定一个`比当前最大的 Alloc ID 更大的值`。
  -cluster-id uint
        指定原集群的 cluster ID
  -endpoints string
        指定 PD 的地址 (default "http://127.0.0.1:2379")

```

##### 执行恢复

```ruby
[tidb@test1 tidb-ansible]<span class="katex math inline">/home/tidb/tidb-ansible/resources/bin/pd-recover -cluster-id=6759063543423042264 -alloc-id=6000 -endpoints="http://172.160.181.18:2379"
recover success! please restart the PD cluster
[tidb@test1 tidb-ansible]</span>

```

##### 重启集群

```ruby
[tidb@test1 tidb-ansible]$ ansible-playbook stop.yml && ansible-playbook start.yml

```