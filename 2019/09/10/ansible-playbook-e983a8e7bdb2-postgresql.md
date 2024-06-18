---
title: 'Ansible-playbook 部署 PostgreSQL'
date: '2019-09-10T02:33:29+00:00'
status: publish
permalink: /2019/09/10/ansible-playbook-%e9%83%a8%e7%bd%b2-postgresql
author: 毛巳煜
excerpt: ''
type: post
id: 5033
category:
    - PostgreSQL
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 环境

<table><thead><tr><th>HostName</th><th>IP</th><th>DES</th></tr></thead><tbody><tr><td>test1</td><td>172.160.180.46</td><td>主控机</td></tr><tr><td>test2</td><td>172.160.180.47</td><td>工作节点 GTM</td></tr><tr><td>test3</td><td>172.160.180.48</td><td>工作节点 (GTM\_Proxy, Coordinator, DataNode)</td></tr><tr><td>test4</td><td>172.160.181.18</td><td>工作节点 (GTM\_Proxy, Coordinator, DataNode)</td></tr></tbody></table>

**注意： 主控机不参加作业**

##### 1.在中控机上创建 postgres 用户

```ruby
[root@test1]~# useradd -m -d /home/postgres postgres
[root@test1]~# passwd postgres
输入postgres用户密码
[root@test1]~#
# 追加 sudo 免密
[root@test1]~# cat >> /etc/sudoers 
```

##### 2.生成SSH Key

```ruby
[root@test1]~# su - postgres
[postgres@test1 ~]<span class="katex math inline">[postgres@test1 ~]</span> ssh-keygen -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/home/postgres/.ssh/id_rsa):
Created directory '/home/postgres/.ssh'.
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/postgres/.ssh/id_rsa.
Your public key has been saved in /home/postgres/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:g7tMJtyN6F4/QsUjQb5QQnf9QdbeNhDfflc39+BMB48 postgres@test1
The key's randomart image is:
+---[RSA 2048]----+
|   .o.+ .. .ooo  |
|     =..  ....o+.|
|    . .o   . oE+B|
|     ..o+   .+.=O|
|      ooS.    o.*|
|   . o.+ .      o|
|    +.B .        |
|   . *.o.        |
|   .o o...       |
+----[SHA256]-----+
[postgres@test1 ~]<span class="katex math inline">[postgres@test1 ~]</span>

```

##### 3.配置SSH免密

###### 3.1 添加集群 配置文件

```ruby
<br></br>[postgres@test1 ~]<span class="katex math inline">mkdir -p /home/postgres/deploy
[postgres@test1 ~]</span>
[postgres@test1 ~]$ cat > /home/postgres/deploy/hosts.ini 
```

###### 3.2 修改ansible默认配置, 跳过 ssh 首次连接提示验证

```ruby
[postgres@test1 ~]$ cat > /home/postgres/deploy/ansible.cfg 
```

###### 3.3 添加 ansible-playbook 配置文件

```ruby
[postgres@test1 ~]$ cat > /home/postgres/deploy/create_users.yml 
```

###### 3.4 批量执行 SSH免密

```ruby
[postgres@test1 deploy]<span class="katex math inline">ansible-playbook -i hosts.ini create_users.yml -u root -k
SSH password:

PLAY [all] *****************************************************************************************************************************

TASK [Gathering Facts] *****************************************************************************************************************
ok: [172.160.180.48]
ok: [172.160.180.47]
ok: [172.160.181.18]

TASK [create user] *********************************************************************************************************************
ok: [172.160.180.48]
ok: [172.160.180.47]
changed: [172.160.181.18]

TASK [set authorized key] **************************************************************************************************************
ok: [172.160.180.48]
changed: [172.160.181.18]
ok: [172.160.180.47]

TASK [update sudoers file] *************************************************************************************************************
ok: [172.160.180.48]
ok: [172.160.180.47]
changed: [172.160.181.18]

PLAY RECAP *****************************************************************************************************************************
172.160.180.47             : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
172.160.180.48             : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
172.160.181.18             : ok=4    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[postgres@test1 deploy]</span>

```

###### 3.5 测试互信是否成功

```ruby
[postgres@test1 deploy]<span class="katex math inline">[postgres@test1 deploy]</span> ansible -i hosts.ini all -m shell -a 'whoami'
172.160.180.47 | CHANGED | rc=0 >>
postgres

172.160.180.48 | CHANGED | rc=0 >>
postgres

172.160.181.18 | CHANGED | rc=0 >>
postgres

[postgres@test1 deploy]<span class="katex math inline">[postgres@test1 deploy]</span>
[postgres@test1 deploy]<span class="katex math inline">ansible -i hosts.ini all -m shell -a 'whoami' -b
172.160.181.18 | CHANGED | rc=0 >>
root

172.160.180.48 | CHANGED | rc=0 >>
root

172.160.180.47 | CHANGED | rc=0 >>
root

[postgres@test1 deploy]</span>

```

###### 3.6 添加hostname映射

```ruby
[postgres@test1 deploy]$ cat > /home/postgres/deploy/modify_hosts.yml 
```

##### 4.安装部署

###### 4.1 下载

官网：https://www.postgres-xl.org/  
官网下载地址：https://www.postgres-xl.org/downloads/

```ruby
# 下载到  /home/postgres/deploy/ 目录
[postgres@test1 deploy]<span class="katex math inline">wget https://www.postgres-xl.org/downloads/postgres-xl-10r1.1.tar.gz -P /home/postgres/deploy/
[postgres@test1 deploy]</span>

```

###### 或者使用bz2文件

下载\*.tar.bz2：wget https://www.postgres-xl.org/downloads/postgres-xl-9.5r1.6.tar.bz2

```ruby
# 安装转换工具
[postgres@test1 deploy]<span class="katex math inline">yum install -y bzip2
# bz2 转换 tar
[postgres@test1 deploy]</span> bunzip2 postgres-xl-9.5r1.6.tar.bz2
[postgres@test1 deploy]<span class="katex math inline">[postgres@test1 deploy]</span> tar -xf postgres-xl-9.5r1.6.tar

```

**`注意`** `如果使用bz2文件，需要修改deploy.yml中压缩包的名称`

###### 4.2 部署到节点机

```ruby
[postgres@test1 deploy]$ cat > /home/postgres/deploy/deploy.yml 
```

`ansible-playbook -i hosts.ini deploy.yml`

###### 4.3 初始化

```ruby
[postgres@test1 deploy]$ cat > /home/postgres/deploy/init.yml 
```

`ansible-playbook -i hosts.ini init.yml`

###### 4.4 启动

```ruby
[postgres@test1 deploy]$ cat > /home/postgres/deploy/start.yml 
```

`ansible-playbook -i hosts.ini start.yml`

###### 4.5 停止

```ruby
[postgres@test1 deploy]$ cat > /home/postgres/deploy/stop.yml 
```

`ansible-playbook -i hosts.ini stop.yml`

###### 4.6 清除

```ruby
[postgres@test1 deploy]$ cat > /home/postgres/deploy/cleanup_data.yml 
```

`ansible-playbook -i hosts.ini cleanup_data.yml`

###### 4.7 执行注册

**4.7.1 node1 上执行**

```ruby
psql -p 15432 -c "CREATE NODE datanode2 WITH (TYPE='datanode',HOST='node2',PORT=15432)"
psql -p 15432 -c "CREATE NODE coordinator1 WITH (TYPE='coordinator',HOST='node1',PORT=5432)"
psql -p 15432 -c "CREATE NODE coordinator2 WITH (TYPE='coordinator',HOST='node2',PORT=5432)"
psql -p 15432 -c "select pgxc_pool_reload()" # 重新加载
psql -p 15432 -c "select * from pgxc_node" # 查看结果

psql -p 5432 -c "CREATE NODE coordinator2 WITH (TYPE='coordinator',HOST='node2',PORT=5432)"
psql -p 5432 -c "CREATE NODE datanode1 WITH (TYPE='datanode',HOST='node1',PORT=15432)"
psql -p 5432 -c "CREATE NODE datanode2 WITH (TYPE='datanode',HOST='node2',PORT=15432)"
psql -p 5432 -c "select pgxc_pool_reload()" # 重新加载
psql -p 5432 -c "select * from pgxc_node" # 查看结果

```

**4.7.2 node2 上执行**

```ruby
psql -p 15432 -c "CREATE NODE datanode1 WITH (TYPE='datanode',HOST='node1',PORT=15432)"
psql -p 15432 -c "CREATE NODE coordinator1 WITH (TYPE='coordinator',HOST='node1',PORT=5432)"
psql -p 15432 -c "CREATE NODE coordinator2 WITH (TYPE='coordinator',HOST='node2',PORT=5432)"
psql -p 15432 -c "select pgxc_pool_reload()" # 重新加载
psql -p 15432 -c "select * from pgxc_node" # 查看结果

psql -p 5432 -c "CREATE NODE coordinator1 WITH (TYPE='coordinator',HOST='node1',PORT=5432)"
psql -p 5432 -c "CREATE NODE datanode1 WITH (TYPE='datanode',HOST='node1',PORT=15432)"
psql -p 5432 -c "CREATE NODE datanode2 WITH (TYPE='datanode',HOST='node2',PORT=15432)"
psql -p 5432 -c "select pgxc_pool_reload()" # 重新加载
psql -p 5432 -c "select * from pgxc_node" # 查看结果

```

###### 4.8 连接数据库

**随意选择一个节点机的IP地址进行连接**

```ruby
[postgres@test1 ~]$  psql -h 172.160.180.47 -p 5432 -U postgres
psql (PGXL 10r1.1, based on PG 10.6 (Postgres-XL 10r1.1))
Type "help" for help.

postgres=#


```

- - - - - -

**启动集群的顺序:**

1. gtm
2. gtm\_proxy
3. datanode
4. coordinator

**关闭集群的顺序:**

1. coordinator
2. datanode
3. gtm\_proxy
4. gtm