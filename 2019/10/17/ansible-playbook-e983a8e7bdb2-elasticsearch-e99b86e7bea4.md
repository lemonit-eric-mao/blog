---
title: 'Ansible-playbook 部署 ElasticSearch 集群'
date: '2019-10-17T07:54:21+00:00'
status: publish
permalink: /2019/10/17/ansible-playbook-%e9%83%a8%e7%bd%b2-elasticsearch-%e9%9b%86%e7%be%a4
author: 毛巳煜
excerpt: ''
type: post
id: 5080
category:
    - ElasticSearch
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### [国内镜像下载](https://thans.cn/mirror/elasticsearch.html "国内镜像下载")

##### 环境

<table><thead><tr><th>HostName</th><th>IP</th><th>DES</th></tr></thead><tbody><tr><td>test1</td><td>172.160.180.46</td><td>主控机</td></tr><tr><td>test2</td><td>172.160.180.47</td><td>node-1</td></tr><tr><td>test3</td><td>172.160.180.48</td><td>node-2</td></tr><tr><td>test4</td><td>172.160.181.18</td><td>node-3</td></tr></tbody></table>

**注意： 主控机不参加作业**

##### 1.在主控机上创建 elasticsearch 用户

```ruby
[root@test1]~# useradd -m -d /home/elasticsearch elasticsearch
[root@test1]~# passwd elasticsearch
输入elasticsearch用户密码
[root@test1]~#
# 追加 sudo 免密
[root@test1]~# cat >> /etc/sudoers 
```

##### 2.生成SSH Key

```ruby
[root@test1]~# su - elasticsearch
[elasticsearch@test1 ~]<span class="katex math inline">[elasticsearch@test1 ~]</span> ssh-keygen -t rsa
[elasticsearch@test1 ~]$

```

##### 3.配置SSH免密

###### 3.1 添加集群 配置文件

```ruby
[elasticsearch@test1 ~]<span class="katex math inline">mkdir -p /home/elasticsearch/deploy
[elasticsearch@test1 ~]</span>
[elasticsearch@test1 ~]$ cat > /home/elasticsearch/deploy/hosts.ini 
```

###### 3.2 修改ansible默认配置, 跳过 ssh 首次连接提示验证

```ruby
[elasticsearch@test1 ~]$ cat > /home/elasticsearch/deploy/ansible.cfg 
```

###### 3.3 添加 create\_users.yml 配置文件

```ruby
[elasticsearch@test1 ~]$ cat > /home/elasticsearch/deploy/create_users.yml 
```

###### 3.4 批量执行 SSH免密

```ruby
[elasticsearch@test1 deploy]$ ansible-playbook -i hosts.ini create_users.yml -u root -k

```

###### 3.5 测试互信是否成功

```ruby
[elasticsearch@test1 deploy]<span class="katex math inline">[elasticsearch@test1 deploy]</span> ansible -i hosts.ini all -m shell -a 'whoami'
[elasticsearch@test1 deploy]<span class="katex math inline">[elasticsearch@test1 deploy]</span> ansible -i hosts.ini all -m shell -a 'whoami' -b
[elasticsearch@test1 deploy]$

```

###### 3.6 添加hostname映射

```ruby
[elasticsearch@test1 deploy]$ cat > /home/elasticsearch/deploy/modify_hosts.yml 
```

##### 4.安装部署

###### 4.1 修改节点机配置

```ruby
[elasticsearch@test1 deploy]$ cat > /home/elasticsearch/deploy/bootstrap.yml 
```

`ansible-playbook -i hosts.ini bootstrap.yml -b`

###### 4.2 [安装JDK](https://www.lemonit.cn/2019/10/14/centos7-%E9%80%9A%E8%BF%87%E4%BA%8C%E8%BF%9B%E5%88%B6%E5%8C%85%E5%AE%89%E8%A3%85-java-13/ "安装JDK")

```ruby
[elasticsearch@test1 deploy]$ cat > /home/elasticsearch/deploy/deploy-jdk.yml 
```

`ansible-playbook -i hosts.ini deploy-jdk.yml`

###### 4.3 下载elasticsearch

```ruby
# 下载到  /home/elasticsearch/deploy/ 目录
[elasticsearch@test1 deploy]<span class="katex math inline">pwd
/home/elasticsearch/deploy
[elasticsearch@test1 deploy]</span>
[elasticsearch@test1 ~]<span class="katex math inline">curl -L -O https://elasticsearch.thans.cn/downloads/elasticsearch/elasticsearch-7.3.2-linux-x86_64.tar.gz
[elasticsearch@test1 deploy]</span>
[elasticsearch@test1 deploy]$ tar -zxvf elasticsearch-7.3.2-linux-x86_64.tar.gz

```

###### 4.4 部署到节点机

```ruby
[elasticsearch@test1 deploy]$ cat > /home/elasticsearch/deploy/deploy.yml 
```

`ansible-playbook -i hosts.ini deploy.yml`

###### 4.5 启动 elasticsearch

```ruby
[elasticsearch@test1 deploy]$ cat > /home/elasticsearch/deploy/start.yml 
```

`ansible-playbook -i hosts.ini start.yml`

###### 4.6 停止 elasticsearch

```ruby
[elasticsearch@test1 deploy]$ cat > /home/elasticsearch/deploy/stop.yml 
```

`ansible-playbook -i hosts.ini stop.yml`

##### 5 访问集群

172.160.180.47:9200