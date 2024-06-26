---
title: "TiDB ansible-playbook 批量设置NTP开机自启动"
date: "2019-08-27"
categories: 
  - "tidb"
---

##### hosts.ini

```ruby
[tidb@test1 tidb-ansible]$ pwd
/home/tidb/tidb-ansible
[tidb@test1 tidb-ansible]$ cat hosts.ini
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
[tidb@test1 tidb-ansible]$ cat > /home/tidb/tidb-ansible/ntp_sync.yaml << eric
# 使用方法 ansible-playbook ntp_sync.yaml -i hosts.ini -u tidb -b
# 说明 ansible-playbook 要执行的命令的配置文件 -i 远程机器的IP地址配置文件 -u 用户 -b:表示执行命令时不会输入密码
# servers 是指 /home/tidb/tidb-ansible/hosts.ini 中的属性，在我执行 ansible-playbook的时候我会指定这个配置文件
- hosts: servers

  tasks:
    - name: '设置NTP开机自启动'
      shell: systemctl enable ntpd.service
    - name: '启动NTP'
      shell: systemctl start ntpd.service
eric

[tidb@test1 tidb-ansible]$
```
