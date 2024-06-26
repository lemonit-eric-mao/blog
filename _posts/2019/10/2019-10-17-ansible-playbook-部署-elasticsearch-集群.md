---
title: "Ansible-playbook 部署 ElasticSearch 集群"
date: "2019-10-17"
categories: 
  - "elasticsearch"
---

###### [国内镜像下载](https://thans.cn/mirror/elasticsearch.html "国内镜像下载")

##### 环境

| HostName | IP | DES |
| --- | --- | --- |
| test1 | 172.160.180.46 | 主控机 |
| test2 | 172.160.180.47 | node-1 |
| test3 | 172.160.180.48 | node-2 |
| test4 | 172.160.181.18 | node-3 |

**注意： 主控机不参加作业**

##### 1.在主控机上创建 elasticsearch 用户

```ruby
[root@test1]~# useradd -m -d /home/elasticsearch elasticsearch
[root@test1]~# passwd elasticsearch
输入elasticsearch用户密码
[root@test1]~#
# 追加 sudo 免密
[root@test1]~# cat >> /etc/sudoers << eric
elasticsearch ALL=(ALL) NOPASSWD: ALL
eric
[root@test1]~#
```

##### 2.生成SSH Key

```ruby
[root@test1]~# su - elasticsearch
[elasticsearch@test1 ~]$
[elasticsearch@test1 ~]$ ssh-keygen -t rsa
[elasticsearch@test1 ~]$
```

##### 3.配置SSH免密

###### 3.1 添加集群 配置文件

```ruby
[elasticsearch@test1 ~]$ mkdir -p /home/elasticsearch/deploy
[elasticsearch@test1 ~]$
[elasticsearch@test1 ~]$ cat > /home/elasticsearch/deploy/hosts.ini << eric
[servers]
node-1 ansible_ssh_host=172.160.180.47
node-2 ansible_ssh_host=172.160.180.48
node-3 ansible_ssh_host=172.160.181.18

# 全局变量
[all:vars]
username = elasticsearch
cluster_name = eric-es-cluster
deploy_dir = /home/elasticsearch/deploy
version = 7.3.2
eric

[elasticsearch@test1 ~]$
```

###### 3.2 修改ansible默认配置, 跳过 ssh 首次连接提示验证

```ruby
[elasticsearch@test1 ~]$ cat > /home/elasticsearch/deploy/ansible.cfg << eric
[defaults]
# 跳过 ssh 首次连接提示验证
host_key_checking=False
# 关闭警告提示
command_warnings=False
deprecation_warnings=False
eric

[elasticsearch@test1 ~]$
```

###### 3.3 添加 create\_users.yml 配置文件

```ruby
[elasticsearch@test1 ~]$ cat > /home/elasticsearch/deploy/create_users.yml << eric
# 使用方法 ansible-playbook -i hosts.ini create_users.yml -u root -k
---
- hosts: all

  tasks:
    - name: create user
      user: name={{ username }} shell=/bin/bash createhome=yes

    - name: set authorized key
      authorized_key:
        user: "{{ username }}"
        key: "{{ lookup('file', '/home/{{ username }}/.ssh/id_rsa.pub') }}"
        state: present

    - name: update sudoers file
      lineinfile:
        # 必须参数，指定要操作的文件。
        dest: /etc/sudoers
        # 使用此参数指定文本内容。
        line: '{{ username }} ALL=(ALL) NOPASSWD: ALL'
        # 借助insertafter参数可以将文本插入到“指定的行”之后，
        # insertafter参数的值可以设置为EOF或者正则表达式，EOF为End Of File之意，
        # 表示插入到文档的末尾，默认情况下insertafter的值为EOF，
        # 如果将insertafter的值设置为正则表达式，表示将文本插入到匹配到正则的行之后，
        # 如果正则没有匹配到任何行，则插入到文件末尾，当使用backrefs参数时，此参数会被忽略。
        insertafter: EOF
        # 使用正则表达式匹配对应的行，当替换文本时，如果有多行文本都能被匹配，则只有最后面被匹配到的那行文本才会被替换，
        # 当删除文本时，如果有多行文本都能被匹配，这么这些行都会被删除。
        regexp: '^{{ username }} .*'
        # 当想要删除对应的文本时，需要将state参数的值设置为absent，absent为缺席之意，表示删除，state的默认值为present。
        state: present
eric

[elasticsearch@test1 ~]$
```

###### 3.4 批量执行 SSH免密

```ruby
[elasticsearch@test1 deploy]$ ansible-playbook -i hosts.ini create_users.yml -u root -k
```

###### 3.5 测试互信是否成功

```ruby
[elasticsearch@test1 deploy]$
[elasticsearch@test1 deploy]$ ansible -i hosts.ini all -m shell -a 'whoami'
[elasticsearch@test1 deploy]$
[elasticsearch@test1 deploy]$ ansible -i hosts.ini all -m shell -a 'whoami' -b
[elasticsearch@test1 deploy]$
```

###### 3.6 添加hostname映射

```ruby
[elasticsearch@test1 deploy]$ cat > /home/elasticsearch/deploy/modify_hosts.yml << eric
# 使用方法 ansible-playbook -i hosts.ini modify_hosts.yml -b
---
- hosts: servers
  tasks:
    - name: 配置 hosts 映射
      sudo: yes
      lineinfile:
        dest: '/etc/hosts'
        line: '{{ item.key }} {{ item.value }}'
        regexp: '{{ item.key }} {{ item.value }}'
        state: present
      # 定义集合，并循环执行所在的模块
      with_items:
        - { key: "172.160.180.47", value: "node-1" }
        - { key: "172.160.180.48", value: "node-2" }
        - { key: "172.160.181.18", value: "node-3" }
eric

[elasticsearch@test1 deploy]$
```

##### 4.安装部署

###### 4.1 修改节点机配置

```ruby
[elasticsearch@test1 deploy]$ cat > /home/elasticsearch/deploy/bootstrap.yml << eric
# 使用方法 ansible-playbook -i hosts.ini bootstrap.yml -b
---
- hosts: servers
  tasks:
    - name: 修改配置文件 limits.conf
      lineinfile:
        dest: '/etc/security/limits.conf'
        line: '*       {{ item.value }}'
        regexp: '.*{{ item.value }}.*'
        state: present
      # 定义集合，并循环执行所在的模块
      with_items:
        - { value: 'soft     nofile         65536' }
        - { value: 'hard     nofile         65536' }
        - { value: 'soft     nproc          2048' }
        - { value: 'hard     nproc          4096' }

    - name: 修改配置文件 sysctl.conf
      lineinfile:
        dest: '/etc/sysctl.conf'
        line: '{{ item.value }}'
        regexp: '^{{ item.value }}.*'
        state: present
      # 定义集合，并循环执行所在的模块
      with_items:
        - { value: 'vm.max_map_count = 655360' }

    - name: 让内核参数立即生效
      shell: 'sysctl -p'
eric

[elasticsearch@test1 deploy]$
```

`ansible-playbook -i hosts.ini bootstrap.yml -b`

###### 4.2 [安装JDK](https://www.lemonit.cn/2019/10/14/centos7-%E9%80%9A%E8%BF%87%E4%BA%8C%E8%BF%9B%E5%88%B6%E5%8C%85%E5%AE%89%E8%A3%85-java-13/ "安装JDK")

```ruby
[elasticsearch@test1 deploy]$ cat > /home/elasticsearch/deploy/deploy-jdk.yml << eric
# 使用方法 ansible-playbook -i hosts.ini deploy-jdk.yml
---
- hosts: servers
  tasks:
    - name: 创建deploy目录
      shell: 'mkdir -p {{ deploy_dir }}'

    - name: '上传文件'
      # 将本地文件复制到远程服务器
      copy:
        src: '{{ item.src }}'
        dest: '{{ item.dest }}'
      with_items:
        - { src: '{{ deploy_dir }}/jdk-13_linux-x64_bin.tar.gz', dest: '{{ deploy_dir }}/jdk-13_linux-x64_bin.tar.gz' }

    - name: 解压
      shell: cd {{ deploy_dir }} && tar -zxvf jdk-13_linux-x64_bin.tar.gz

    - name: 添加环境变量
      lineinfile:
        dest: ~/.bashrc
        line: '{{ item.key }}={{item.value}}'
        regexp: '^{{ item.key }}.*'
        state: present
      # 定义集合，并循环执行所在的模块
      with_items:
        - { key: 'export JAVA_HOME', value: '{{ deploy_dir }}/jdk-13' }
        - { key: 'export JRE_HOME', value: '\$JAVA_HOME/jre' }
        - { key: 'export CLASSPATH', value: '.:\$JAVA_HOME/lib:\$JRE_HOME/lib' }
        - { key: 'export PATH', value: '\$PATH:\$JAVA_HOME/bin' }
eric

[elasticsearch@test1 deploy]$
```

`ansible-playbook -i hosts.ini deploy-jdk.yml`

###### 4.3 下载elasticsearch

```ruby
# 下载到  /home/elasticsearch/deploy/ 目录
[elasticsearch@test1 deploy]$ pwd
/home/elasticsearch/deploy
[elasticsearch@test1 deploy]$
[elasticsearch@test1 ~]$ curl -L -O https://elasticsearch.thans.cn/downloads/elasticsearch/elasticsearch-7.3.2-linux-x86_64.tar.gz
[elasticsearch@test1 deploy]$
[elasticsearch@test1 deploy]$ tar -zxvf elasticsearch-7.3.2-linux-x86_64.tar.gz
```

###### 4.4 部署到节点机

```ruby
[elasticsearch@test1 deploy]$ cat > /home/elasticsearch/deploy/deploy.yml << eric
# 使用方法 ansible-playbook -i hosts.ini deploy.yml
---
- hosts: servers
  tags:
    - es
  tasks:
    - name: 创建deploy目录
      shell: 'mkdir -p {{ deploy_dir }}'

    - name: '上传文件'
      # 将本地文件复制到远程服务器
      copy:
        src: '{{ item.src }}'
        dest: '{{ item.dest }}'
      with_items:
        - { src: '{{ deploy_dir }}/elasticsearch-{{ version }}-linux-x86_64.tar.gz', dest: '{{ deploy_dir }}/elasticsearch-{{ version }}-linux-x86_64.tar.gz' }

    - name: 解压
      shell: 'tar -zxvf {{ deploy_dir }}/elasticsearch-{{ version }}-linux-x86_64.tar.gz -C {{ deploy_dir }}/'

- hosts: servers
  tags:
    - config
  tasks:
    - name: 修改配置文件
      lineinfile:
        dest: '{{ deploy_dir }}/elasticsearch-{{ version }}/config/elasticsearch.yml'
        line: '{{ item.key }}: {{ item.value }}'
        regexp: '^{{ item.key }}.*'
        state: present
      # 定义集合，并循环执行所在的模块
      with_items:
        - { key: "cluster.name", value: "{{ cluster_name }}" }
        - { key: "node.name", value: "{{ inventory_hostname }}" }
        - { key: "network.host", value: "{{ inventory_hostname }}" }
        - { key: "http.port", value: "9200" }
        - { key: "http.cors.enabled", value: "true" }
        - { key: "http.cors.allow-origin", value: "'*'" }
        - { key: "discovery.seed_hosts", value: "['node-1', 'node-2', 'node-3']" }
        - { key: "cluster.initial_master_nodes", value: "['node-1']" }
        - { key: "discovery.zen.minimum_master_nodes", value: "1" }
        - { key: "indices.memory.index_buffer_size", value: "20%" }
        - { key: "indices.query.bool.max_clause_count", value: "100000000" }
eric

[elasticsearch@test1 deploy]$
```

`ansible-playbook -i hosts.ini deploy.yml`

###### 4.5 启动 elasticsearch

```ruby
[elasticsearch@test1 deploy]$ cat > /home/elasticsearch/deploy/start.yml << eric
# 使用方法 ansible-playbook -i hosts.ini start.yml
---
- hosts: servers
  tasks:
    - name: 启动 elasticsearch
      shell: nohup {{ deploy_dir }}/elasticsearch-{{ version }}/bin/elasticsearch &
eric

[elasticsearch@test1 deploy]$
```

`ansible-playbook -i hosts.ini start.yml`

###### 4.6 停止 elasticsearch

```ruby
[elasticsearch@test1 deploy]$ cat > /home/elasticsearch/deploy/stop.yml << eric
# 使用方法 ansible-playbook -i hosts.ini stop.yml
---
- hosts: servers
  tasks:
    - name: 停止 elasticsearch
      shell: kill -9 \$(jps | grep Elasticsearch | awk '{print \$1}')
      ignore_errors: yes
eric

[elasticsearch@test1 deploy]$
```

`ansible-playbook -i hosts.ini stop.yml`

##### 5 访问集群

172.160.180.47:9200
