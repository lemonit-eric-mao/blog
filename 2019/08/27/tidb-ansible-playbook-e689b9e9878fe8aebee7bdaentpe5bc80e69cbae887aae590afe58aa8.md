---
title: 'TiDB ansible-playbook 批量设置NTP开机自启动'
date: '2019-08-27T06:41:26+00:00'
status: publish
permalink: /2019/08/27/tidb-ansible-playbook-%e6%89%b9%e9%87%8f%e8%ae%be%e7%bd%aentp%e5%bc%80%e6%9c%ba%e8%87%aa%e5%90%af%e5%8a%a8
author: 毛巳煜
excerpt: ''
type: post
id: 5015
category:
    - TiDB
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### hosts.ini

```ruby
[tidb@test1 tidb-ansible]<span class="katex math inline">pwd
/home/tidb/tidb-ansible
[tidb@test1 tidb-ansible]</span> cat hosts.ini
[servers]
172.160.180.46
172.160.180.47
172.160.180.48
172.160.181.18

[all:vars]
username = tidb
ntp_server = pool.ntp.org
[tidb@test1 tidb-ansible]$

```

##### 时间同步脚本

```ruby
[tidb@test1 tidb-ansible]$ cat > /home/tidb/tidb-ansible/ntp_sync.yaml 
```