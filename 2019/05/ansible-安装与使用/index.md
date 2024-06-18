---
title: "Ansible 安装与使用"
date: "2019-05-21"
categories: 
  - "ansible"
---

[Ansible中文权威指南](http://www.ansible.com.cn/index.html "Ansible中文权威指南")

##### 服务器

| HostName | IP | CPU | MEM | DES |
| --- | --- | --- | --- | --- |
| k8s-master | 172.26.48.4 | 2 Core | 2G | k8s master 节点 |
| k8s-node1 | 172.26.48.5 | 1 Core | 2G | 应用节点 |
| k8s-node2 | 172.26.135.94 | 1 Core | 2G | 应用节点 |

`不要忘记修改本地/etc/hosts文件`

```ruby
# 将以下内容追加(>>)到 /etc/hosts文件
[root@k8s-master ~]# cat <<EOF >> /etc/hosts
172.26.48.4    k8s-master
172.26.48.5    k8s-node1
172.26.135.94  k8s-node2
EOF
```

#### CentOS 7 安装 ansible

```ruby
[root@k8s-master home]# yum install -y http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
......
[root@k8s-master home]# yum install ansible -y
......
[root@k8s-master home]# ansible --version
ansible 2.7.10
  config file = /etc/ansible/ansible.cfg
  configured module search path = [u'/root/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/site-packages/ansible
  executable location = /usr/bin/ansible
  python version = 2.7.5 (default, Jul 13 2018, 13:06:57) [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
[root@k8s-master home]#
[root@k8s-master home]#
[root@k8s-master home]# ansible-playbook --version
ansible 2.7.10
  config file = /etc/ansible/ansible.cfg
  configured module search path = [u'/root/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/site-packages/ansible
  executable location = /usr/bin/ansible
  python version = 2.7.5 (default, Jul 13 2018, 13:06:57) [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
[root@k8s-master home]#
```

#### 配置 ansible hosts

```ruby
root@k8s-master deploy]# cat <<EOF >> /etc/ansible/hosts
[all]
172.26.48.4
172.26.48.5
172.26.135.94
[nodes]
172.26.48.5
172.26.135.94
EOF
```

#### 创建 SSH key

```ruby
[root@k8s-master ansible]# pwd
/etc/ansible
[root@k8s-master ansible]# ssh-keygen -t rsa
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /root/.ssh/id_rsa.
Your public key has been saved in /root/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:VJQenTc40F0FahV6wa+c/ftajF9JhT/le050ERYLOBc root@k8s-master
The key's randomart image is:
+---[RSA 2048]----+
|         .+=.E*B=|
|         .oo*=Boo|
|        .. .*oo=o|
|       .  .. . o=|
|        S    . *=|
|              =+*|
|              .oB|
|               =+|
|              .o*|
+----[SHA256]-----+
[root@k8s-master ansible]#
```

#### ansible 批量配置ssh免密

```ruby
[root@k8s-master ansible]# ansible nodes -m authorized_key -a "user=root key='{{ lookup('file','/root/.ssh/id_rsa.pub')}}' path='/root/.ssh/authorized_keys' manage_dir=no" --ask-pass -c paramiko
SSH password:
......
[root@k8s-master ansible]#
```

```bash
#因为密码都一样，所以只需要输入一次密码即可，如果密码不同  需要自定义

# 说明：
# 将秘钥推送到远程主机的哪个用户下
user=root
# 指定要推送的秘钥文件所在的路径
key='{{ lookup('file','/root/.ssh/id_rsa.pub')}}'
# 将秘钥推送到远程主机的哪个目录下并重命名
path='/root/.ssh/authorized_keys'
# 指定模块是否应该管理authorized_keys文件所在的目录，如果设置为yes,模块会创建目录，以及设置一个已存在目录的拥有者和权限。如果通过 path 选项，重新指定了一个 authorized key 文件所在目录，那么应该将该选项设置为 no
manage_dir=no
# 是否移除 authorized_keys 文件中其它非指定 key
exclusive [default: no]：
# present 添加指定 key 到 authorized_keys 文件中；absent 从 authorized_keys 文件中移除指定 key
state (Choices: present, absent) [Default: present]：
```

#### 测试 SSH 免密是否成功, 查看所有节点的内核版本

```ruby
[root@k8s-master ansible]# ansible nodes -m shell -a 'uname -r'
172.26.48.5 | CHANGED | rc=0 >>
3.10.0-862.14.4.el7.x86_64

172.26.135.94 | CHANGED | rc=0 >>
3.10.0-862.14.4.el7.x86_64

[root@k8s-master ansible]#
```

* * *

* * *

* * *

##### **hosts.ini**

```ini
[servers]
172.26.48.4
172.26.48.5
172.26.135.94
```

* * *

##### 复制文件

```ruby
ansible servers -i hosts.ini -m ping

```

* * *

##### 复制文件

```ruby
ansible servers -i hosts.ini -m copy -a "src=/etc/hosts dest=/etc/hosts"

```

* * *

* * *

* * *
