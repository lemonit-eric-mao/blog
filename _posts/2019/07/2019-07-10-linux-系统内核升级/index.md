---
title: "Linux 系统内核升级"
date: "2019-07-10"
categories: 
  - "docker"
---

##### CentOS7 内核升级

```ruby
[root@k8s-master ~]# uname -r
3.10.0-957.21.3.el7.x86_64
[root@k8s-master ~]#
```

###### 1\. 导入key

```ruby
[root@k8s-master ~]# rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org
```

###### 2\. 安装elrepo的yum源

```ruby
[root@k8s-master ~]# rpm -Uvh http://www.elrepo.org/elrepo-release-7.0-2.el7.elrepo.noarch.rpm
[root@k8s-master ~]#
```

###### 3\. 安装内核

```ruby
# 查看可安装的rpm软件包
[root@k8s-master ~]# yum --disablerepo="*" --enablerepo="elrepo-kernel" list available
可安装的软件包
kernel-lt.x86_64                                                                                4.4.207-1.el7.elrepo                                                                elrepo-kernel
kernel-lt-devel.x86_64                                                                          4.4.207-1.el7.elrepo                                                                elrepo-kernel
kernel-lt-doc.noarch                                                                            4.4.207-1.el7.elrepo                                                                elrepo-kernel
kernel-lt-headers.x86_64                                                                        4.4.207-1.el7.elrepo                                                                elrepo-kernel
kernel-lt-tools.x86_64                                                                          4.4.207-1.el7.elrepo                                                                elrepo-kernel
kernel-lt-tools-libs.x86_64                                                                     4.4.207-1.el7.elrepo                                                                elrepo-kernel
kernel-lt-tools-libs-devel.x86_64                                                               4.4.207-1.el7.elrepo                                                                elrepo-kernel
kernel-ml.x86_64                                                                                5.4.6-1.el7.elrepo                                                                  elrepo-kernel
kernel-ml-devel.x86_64                                                                          5.4.6-1.el7.elrepo                                                                  elrepo-kernel
kernel-ml-doc.noarch                                                                            5.4.6-1.el7.elrepo                                                                  elrepo-kernel
kernel-ml-headers.x86_64                                                                        5.4.6-1.el7.elrepo                                                                  elrepo-kernel
kernel-ml-tools.x86_64                                                                          5.4.6-1.el7.elrepo                                                                  elrepo-kernel
kernel-ml-tools-libs.x86_64                                                                     5.4.6-1.el7.elrepo                                                                  elrepo-kernel
kernel-ml-tools-libs-devel.x86_64                                                               5.4.6-1.el7.elrepo                                                                  elrepo-kernel
[root@k8s-master ~]#
[root@k8s-master ~]#
[root@k8s-master ~]#
# 安装 kernel-ml 版本内核
[root@k8s-master ~]# yum -y --enablerepo=elrepo-kernel install -y kernel-ml.x86_64 kernel-ml-devel.x86_64
```

> 在内核版本的命名中，"LT" 和 "ML" 分别代表不同的内核分支： "`LT`" 代表 `Long Term Support`（`长期支持`）内核。 这些内核版本的主要特点是它们经过更长时间的支持和维护，通常为几年甚至更长。 这意味着这些内核版本通常更加稳定和可靠，适用于需要长期运行的服务器和生产环境。 "`ML`" 代表 `Mainline`（`主线`）内核。 这些内核版本是 Linux 内核社区的最新开发版本，它们包含了最新的功能和改进。 ML 内核通常用于测试和开发，以便快速采用最新的内核功能，但它们的支持时间通常较短，因此不太适合长期生产环境。

###### 4\. 查看默认启动顺序

```ruby
[root@k8s-master ~]# awk -F\' '$1=="menuentry " {print $2}' /etc/grub2.cfg
CentOS Linux (5.4.6-1.el7.elrepo.x86_64) 7 (Core)
CentOS Linux (3.10.0-1062.9.1.el7.x86_64) 7 (Core)
CentOS Linux (3.10.0-957.el7.x86_64) 7 (Core)
CentOS Linux (0-rescue-47ba540c26214006b21749bb19a2eba9) 7 (Core)
[root@k8s-master ~]#
```

###### 查看原有设置的内核结果:

```ruby
[root@k8s-node1 ~]# grub2-editenv list
saved_entry=CentOS Linux (3.10.0-1062.9.1.el7.x86_64) 7 (Core)
[root@k8s-master ~]#
```

###### 默认启动的顺序是从0开始，新内核是从头插入（目前位置在0，而`3.10.0-1062.9.1.el7.x86_64`的是在1），所以需要选择0。

```ruby
[root@k8s-master ~]# grub2-set-default 0
# 查看设置的内核结果:
[root@k8s-master ~]# grub2-editenv list
saved_entry=0
[root@k8s-master ~]#

# 或者 指定相应的版本内核 (推荐)
[root@k8s-master ~]# grub2-set-default 'CentOS Linux (5.4.6-1.el7.elrepo.x86_64) 7 (Core)'
[root@k8s-master ~]#
[root@k8s-master ~]# grub2-editenv list
saved_entry=CentOS Linux (5.4.6-1.el7.elrepo.x86_64) 7 (Core)
[root@k8s-master ~]#


# 然后reboot重启，使用新的内核，下面是重启后使用的内核版本:
[root@k8s-master ~]# reboot
[root@k8s-master ~]#
[root@k8s-master ~]# uname -r
5.4.6-1.el7.elrepo.x86_64
[root@k8s-master ~]#
```

###### 5\. 删除旧的内核

```ruby
# 查看系统安装了哪些内核包
[root@k8s-master ~]# rpm -qa | grep kernelrpm -qa | grep kernel
kernel-3.10.0-1062.9.1.el7.x86_64
kernel-ml-5.4.6-1.el7.elrepo.x86_64
kernel-3.10.0-957.el7.x86_64
kernel-tools-libs-3.10.0-1062.9.1.el7.x86_64
kernel-tools-3.10.0-1062.9.1.el7.x86_64
kernel-headers-3.10.0-1062.9.1.el7.x86_64
kernel-ml-devel-5.4.6-1.el7.elrepo.x86_64
[root@k8s-master ~]#
# 删除无用内核
[root@k8s-master ~]# yum -y remove kernel
```

* * *

* * *

* * *

###### 将上面的命令写到一起执行

```ruby
rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org
rpm -Uvh http://www.elrepo.org/elrepo-release-7.0-2.el7.elrepo.noarch.rpm
yum -y --enablerepo=elrepo-kernel install -y kernel-ml.x86_64 kernel-ml-devel.x86_64
awk -F\' '$1=="menuentry " {print "grub2-set-default \"" $2 "\""}' /etc/grub2.cfg | head -1 | sh
# 重启系统

```

* * *
