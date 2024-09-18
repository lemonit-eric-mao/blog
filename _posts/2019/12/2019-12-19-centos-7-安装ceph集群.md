---
title: "CentOS 7 安装Ceph集群"
date: "2019-12-19"
categories: 
  - "linux服务器"
---

###### [ceph工作原理](https://www.cnblogs.com/wangyanqiang/p/12070008.html "ceph工作原理")

###### [参考资料](https://www.cnblogs.com/lianshuiwuyi/p/11345083.html "参考资料")

###### [ceph学习资料](https://www.jianshu.com/p/19a9a9312c81 "ceph学习资料")

###### 块存储、文件存储、对象存储这三者的本质差别是什么？

简单来说块存储读写快，不利于共享，文件存储读写慢，利于共享。能否弄一个读写快，利 于共享的出来呢。于是就有了对象存储。

##### 一 前置条件

###### 1 hosts 添加别名

```ruby
[root@test1 ~]# cat >> /etc/hosts << eric
172.160.180.46 test1
172.160.180.47 test2
172.160.180.48 test3
eric

[root@test1 ~]#
```

###### 2 在中控机上创建 postgres 用户

```ruby
[root@test1 ~]# userdel -r ceph
[root@test1 ~]#
[root@test1 ~]# useradd -m -d /home/ceph ceph
[root@test1 ~]#
[root@test1 ~]# cat >> /etc/sudoers << eric
ceph ALL=(ALL) NOPASSWD: ALL
eric

[root@test1 ~]#
```

###### 3 配置 ssh

```ruby
[root@test1 ~]# su - ceph
[ceph@test1 ~]$
[ceph@test1 ~]$ ssh-keygen -t rsa
[ceph@test1 ~]$
[ceph@test1 ~]$ mkdir -p /home/ceph/deploy
[ceph@test1 ~]$
[ceph@test1 ~]$ cat > /home/ceph/deploy/ansible.cfg << eric
[defaults]
# 跳过 ssh 首次连接提示验证
host_key_checking=False
# 关闭警告提示
command_warnings=False
deprecation_warnings=False
eric

[ceph@test1 deploy]$
```

###### 4 使用 ansible 批量创建用户

```ruby
[ceph@test1 deploy]$ cat > /home/ceph/deploy/hosts.ini << eric
[servers]
172.160.180.47
172.160.180.48

[all:vars]
username = ceph
deploy_dir = /home/ceph/deploy
eric
[ceph@test1 deploy]$
```

###### 4.1

```ruby
[ceph@test1 deploy]$ ansible-playbook -i hosts.ini create_users.yml -u root -k
[ceph@test1 deploy]$
[ceph@test1 deploy]$ ansible -i hosts.ini all -m shell -a 'whoami'
172.160.180.48 | CHANGED | rc=0 >>
ceph

172.160.180.47 | CHANGED | rc=0 >>
ceph

[ceph@test1 deploy]$ ansible -i hosts.ini all -m shell -a 'whoami' -b
172.160.180.48 | CHANGED | rc=0 >>
root

172.160.180.47 | CHANGED | rc=0 >>
root

[ceph@test1 deploy]$
```

* * *

* * *

* * *

##### 二 下载、添加镜像源

###### 1 (切换到root账户每个节点都得配置) [配置阿里云源](centos-7-yum-%e9%85%8d%e7%bd%ae%e9%98%bf%e9%87%8c%e4%ba%91%e6%ba%90 "配置阿里云源")

###### 2 配置Ceph安装源 (每个节点都得配置) 安装的ceph版本是`mimic`

**注意：** 执行ceph-deploy命令后 会自动生成 ceph.repo, 这个源的地址太慢了，因些将里面的地址修改为，国内阿里云源 `sed -i -e 's/download.ceph.com/mirrors.aliyun.com\/ceph/g' -e 's/http\:/https\:/g' /etc/yum.repos.d/ceph.repo` 加上 --no-adjust-repos 这个参数,执行ceph-deploy install时就不会替换已经修改过的 ceph.repo 源了 替换后的效果如下， 也可以直接手动创建这个文件

```ruby
cat > /etc/yum.repos.d/ceph.repo << eric
[Ceph]
name=Ceph packages for \$basearch
baseurl=https://mirrors.aliyun.com/ceph/rpm-mimic/el7/\$basearch
enabled=1
gpgcheck=1
type=rpm-md
gpgkey=https://mirrors.aliyun.com/ceph/keys/release.asc
priority=1

[Ceph-noarch]
name=Ceph noarch packages
baseurl=https://mirrors.aliyun.com/ceph/rpm-mimic/el7/noarch
enabled=1
gpgcheck=1
type=rpm-md
gpgkey=https://mirrors.aliyun.com/ceph/keys/release.asc
priority=1

[ceph-source]
name=Ceph source packages
baseurl=https://mirrors.aliyun.com/ceph/rpm-mimic/el7/SRPMS
enabled=1
gpgcheck=1
type=rpm-md
gpgkey=https://mirrors.aliyun.com/ceph/keys/release.asc
priority=1

eric

```

###### 2.1 添加到缓存

```ruby
[root@test1 yum.repos.d]# yum makecache && yum update -y

```

* * *

* * *

* * *

##### 三 安装部署集群

官网地址：https://docs.ceph.com/docs/master/start/quick-ceph-deploy/

###### 0 安装ceph-deploy

```ruby
[root@test1 ~]# yum install -y https://mirrors.aliyun.com/ceph/rpm-nautilus/el7/noarch/ceph-deploy-2.0.1-0.noarch.rpm
[root@test1 ~]#
[root@test1 ~]# ceph-deploy --version
2.0.1
[root@test1 ~]#
```

###### 1 如果是首次安装`可以跳过此步骤`

```ruby
sudo ceph-deploy purge test1 test2 test3
sudo ceph-deploy purgedata test1 test2 test3
sudo ceph-deploy forgetkeys
sudo rm ceph*
```

###### 2 创建monitor节点

```ruby
[ceph@test1 deploy]$ mkdir ceph-cluster
[ceph@test1 ceph-cluster]$ pwd
/home/ceph/deploy/ceph-cluster
[ceph@test1 ceph-cluster]$
[ceph@test1 ceph-cluster]$ sudo ceph-deploy new --public-network 172.160.180.46/26 test1
[ceph@test1 ceph-cluster]$
[ceph@test1 ceph-cluster]$ cat ceph.conf
[global]
fsid = e07cd388-3d61-4480-89e7-3061121faf15
pubwp_network = 172.160.180.46/26
mon_initial_members = test1
mon_host = 172.160.180.46
auth_cluster_required = cephx
auth_service_required = cephx
auth_client_required = cephx

[ceph@test1 ceph-cluster]$
```

###### 3 安装Ceph 版本为`mimic`集群 `--no-adjust-repos 表示安装时不改变已有的ceph.repo`

```ruby
[ceph@test1 ceph-cluster]$ sudo ceph-deploy install --release mimic test1 test2 test3 --no-adjust-repos
[ceph@test1 ceph-cluster]$

# 查看各节点安装的版本
[ceph@test1 ceph-cluster]$ sudo ansible -i ../hosts.ini servers -m shell -a 'ceph --version'
172.160.180.48 | CHANGED | rc=0 >>
ceph version 13.2.8 (5579a94fafbc1f9cc913a0f5d362953a5d9c3ae0) mimic (stable)

172.160.180.47 | CHANGED | rc=0 >>
ceph version 13.2.8 (5579a94fafbc1f9cc913a0f5d362953a5d9c3ae0) mimic (stable)

[ceph@test1 ceph-cluster]$
```

###### 4 部署MON

```ruby
[ceph@test1 ceph-cluster]$ sudo ceph-deploy mon create-initial
......
[ceph_deploy.gatherkeys][INFO  ] Storing ceph.client.admin.keyring
[ceph_deploy.gatherkeys][INFO  ] Storing ceph.bootstrap-mds.keyring
[ceph_deploy.gatherkeys][INFO  ] Storing ceph.bootstrap-mgr.keyring
[ceph_deploy.gatherkeys][INFO  ] Storing ceph.mon.keyring
[ceph_deploy.gatherkeys][INFO  ] Storing ceph.bootstrap-osd.keyring
[ceph_deploy.gatherkeys][INFO  ] Storing ceph.bootstrap-rgw.keyring
[ceph_deploy.gatherkeys][INFO  ] Destroy temp directory /tmp/tmp3fa33l
[ceph@test1 ceph-cluster]$

# 将keyring文件分发到各个节点
[ceph@test1 ceph-cluster]$ sudo ceph-deploy admin test1 test2 test3
```

###### 5 创建OSD节点

```ruby
# 查看分区
[ceph@test1 ceph-cluster]$ sudo lvs
  LV   VG     Attr       LSize    Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
  home centos -wi-a----- 5.00g
  root centos -wi-ao---- <57.00g
  swap centos -wi-ao---- 8.00g
  lv1  vg1    -wi-ao---- <120.00g
[ceph@test1 ceph-cluster]$

```

命令用法：**ceph-deploy osd create --data /dev/`VG`/`LV` `hostsname`**

```ruby
[ceph@test1 ceph-cluster]$ sudo ceph-deploy osd create --data /dev/centos/home test1
[ceph@test1 ceph-cluster]$ sudo ceph-deploy osd create --data /dev/centos/home test2
[ceph@test1 ceph-cluster]$ sudo ceph-deploy osd create --data /dev/centos/home test3
```

OSD 学习资料： https://www.jianshu.com/p/b08e66536981 https://www.zhihu.com/question/21718731

* * *

* * *

* * *

##### **`常见问题`**

###### 1.0 安装ceph问题

```ruby
[test1][DEBUG ]
[test1][DEBUG ] 失败:
[test1][DEBUG ]   python-urllib3.noarch 0:1.10.2-7.el7
[test1][DEBUG ]
[test1][DEBUG ] 完毕！
[test1][ERROR ] RuntimeError: command returned non-zero exit status: 1
[ceph_deploy][ERROR ] RuntimeError: Failed to execute command: yum -y install ceph ceph-radosgw

[root@test1 ~]#
# 手动安装查看问题
[root@test1 ~]# yum install -y python-urllib3.noarch
...... 省略
                                                                                                                                   1/1
  正在安装    : python-urllib3-1.10.2-7.el7.noarch                                                                                 1/1
Error unpacking rpm package python-urllib3-1.10.2-7.el7.noarch
error: unpacking of archive failed on file /usr/lib/python2.7/site-packages/urllib3/packages/ssl_match_hostname: cpio: rename
  验证中      : python-urllib3-1.10.2-7.el7.noarch                                                                                 1/1

失败:
  python-urllib3.noarch 0:1.10.2-7.el7

完毕！
[root@test1 ~]#
```

###### 1.1 问题原因与解决方案

`PIP已经安装了对应的版本包，此时yum安装的rpm包与pip里的冲突，先把pip里的包卸载掉再用yum重新安装`

```ruby
# 卸载掉pip冲突包
[root@test1 ~]# pip uninstall -y urllib3
[root@test1 ~]#

# 重新安装
[root@test1 ~]# yum install -y python-urllib3.noarch
[root@test1 ~]#
```

* * *

* * *

###### 2.0

```ruby
[ceph@test1 ceph-cluster]$ sudo ceph-deploy mon create-initial
......
[test1][DEBUG ] write cluster configuration to /etc/ceph/{cluster}.conf
[ceph_deploy.mon][ERROR ] RuntimeError: config file /etc/ceph/ceph.conf exists with different content; use --overwrite-conf to overwrite
[ceph_deploy][ERROR ] GenericError: Failed to create 1 monitors

[ceph@test1 ceph-cluster]$
```

###### 2.1 问题原因与解决方案

`修改了ceph用户里的ceph.conf文件内容，但是没有把这个文件里的最新消息发送给其他节点，所有要推送消息`

```ruby
[ceph@test1 ceph-cluster]$ sudo ceph-deploy --overwrite-conf config push test1 test2 test3
```

* * *

* * *

###### 3.0

```ruby
[ceph@test1 ceph-cluster]$ sudo ceph-deploy mon create-initial
......
[ceph1][INFO  ] Running command: ceph --cluster=ceph --admin-daemon /var/run/ceph/ceph-mon.ceph1.asok mon_status
[ceph1][ERROR ] admin_socket: exception getting command descriptions: [Errno 2] No such file or directory
......
[ceph_deploy][ERROR ] KeyboardInterrupt

[ceph@test1 ceph-cluster]$ 
```

###### 3.0

**查看路径下的文件发现，文件名使用的是hostname, 我的hostname 定义了多个 `172.160.180.46 test1 ceph1` 所以它生成的文件名是错的**

```ruby
[ceph@test1 ceph-cluster]$ ll  /var/run/ceph/
总用量 0
srwxr-xr-x 1 ceph ceph 0 12月 23 16:23 ceph-mon.test1.asok
[ceph@test1 ceph-cluster]$

```

* * *

* * *

* * *

###### 卸载

https://www.cnblogs.com/nulige/articles/8475907.html

```
uninstall:
    Remove Ceph packages from remote hosts.(仅仅会卸载ceph软件包)
purge:
    Remove Ceph packages from remote hosts and purge allData.(卸载ceph软件包而且还会清除所有数据)
purgedata:
    Purge (delete, destroy, discard, shred) any Ceph data from /var/lib/ceph(删除所有关于ceph的数据文件位于/var/lib/ceph下)
forgetkeys:
    Remove authentication keys from the local directory.(将卸载节点的认证密钥从本地目录移除)<br><br><br>示例：
```
