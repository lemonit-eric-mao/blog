---
title: 'TiDB3.0.2 Grafana 配置 SMTP'
date: '2019-08-22T01:51:19+00:00'
status: publish
permalink: /2019/08/22/tidb3-0-2-grafana-%e9%85%8d%e7%bd%ae-smtp
author: 毛巳煜
excerpt: ''
type: post
id: 5006
category:
    - TiDB
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### grafana 默认读取的配置文件位置

```ruby
[tidb@test1 templates]<span class="katex math inline">pwd
/home/tidb/tidb-ansible/roles/grafana/templates
[tidb@test1 templates]</span>
[tidb@test1 templates]$ vim grafana.ini.j2

```

##### 找到smtp 替换如下内容

```yaml
......
#################################### SMTP / Emailing ##########################
[smtp]
enabled = true
# 发件服务器
host = smtp.exmail.qq.com:465
# smtp 密码
password = 你的SMTP密码
# smtp账号
user = test@163.com
# 发信邮箱
from_address = test@163.com
# 发信人
from_name = TiDB-Grafana

;enabled = false
;host = localhost:25
;user =
;password =
;cert_file =
;key_file =
;skip_verify = false
;from_address = admin@grafana.localhost

[emails]
;welcome_email_on_sign_up = false
......

```

##### 滚动更新 grafana

```ruby
[tidb@test1 tidb-ansible]<span class="katex math inline">ansible-playbook rolling_update_monitor.yml --tags=grafana
......
Congrats! All goes well. :-)
[tidb@test1 tidb-ansible]</span>

```

##### 重启 grafana(如果滚动更新不起作用，就重启一下)

```ruby
[tidb@dev10 tidb-ansible]<span class="katex math inline">ansible-playbook stop.yml --tag=grafana && ansible-playbook start.yml --tag=grafana
......
Congrats! All goes well. :-)
[tidb@test1 tidb-ansible]</span>

```

###### 进入安装grafana的节点机，查看它的配置文件是否被改变

```ruby
[tidb@test1 ~]$ vim /home/tidb/deploy/opt/grafana/conf/grafana.ini

```

##### 总结

直接修改grafana.ini 当执行 rolling\_update\_monitor.yml 就会恢复成默认，所以只要找到它的默认的配置文件就可以了，能定位这个文件是因为我解压了 download/grafana.6.1.6.tar.gz 这个文件，查看它的项目文件中默认的配置与TiDB的默认配置并不一样，因此我猜想TiDB肯定是对它做了重新的整改，在tidb-ansible/ 下查找所有grafana.ini\* 文件，一个一个的试出来的，虽然办法比较粗略，但也是没有办法的办法。