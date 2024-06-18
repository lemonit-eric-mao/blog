---
title: '大数据学习(四) Cloudera-Manager 安装'
date: '2017-11-16T15:41:44+00:00'
status: publish
permalink: /2017/11/16/%e5%a4%a7%e6%95%b0%e6%8d%ae%e5%ad%a6%e4%b9%a0%e5%9b%9b-cloudera-manager-%e5%ae%89%e8%a3%85
author: 毛巳煜
excerpt: ''
type: post
id: 493
category:
    - 大数据
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
### 本地浏览器打开 http://10.32.156.66:7180

账号: admin  
密码: admin  
![](http://qiniu.dev-share.top/image/cm_login.png)

### 进入群集管理界面

![](http://qiniu.dev-share.top/image/cm_sp_list.png)  
出现了两台, 因为我只配置了两台.  
全部勾选并继续  
`注意`: 如果这里的只有一台主机,  
\* 第一种可能是其它的主机没有启动  
\* 第二种可能是所有的主机和子节点的防火墙给拦截了

### 选择CDH

![](http://qiniu.dev-share.top/image/sm_cdh-version.png)  
默认并继续

### 自动安装

![](http://qiniu.dev-share.top/image/sm_cdh_setup_fail.png)

如果有这种情况 可以删除出问题的服务器中 /opt/cloudera-manager 与 /opt/cloudera/parcels 这两个文件夹, 重新配置, 然后在次尝试  
![](http://qiniu.dev-share.top/image/cm_succeeeeeeeeeeeee.png)

### 安装校验

![](http://qiniu.dev-share.top/image/cm-setup_jiaoyan.png)

按照警告信息去解决问题

#### 解决第一个警告

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@sp-66 CDHInstallFile]# sysctl vm.swappiness=10
vm.swappiness = 10
[root@sp-66 CDHInstallFile]# cat /proc/sys/vm/swappiness
10
[root@sp-66 CDHInstallFile]# echo vm.swappiness=10  >>  /etc/sysctl.conf
[root@sp-66 CDHInstallFile]# cat /etc/sysctl.conf
# System default settings live in /usr/lib/sysctl.d/00-system.conf.
# To override those settings, enter new settings here, or in an /etc/sysctl.d/<name>.conf file
#
# For more information, see sysctl.conf(5) and sysctl.d(5).
vm.swappiness=10
[root@sp-66 CDHInstallFile]#
</name>
```
```

#### 解决第二个警告

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@sp-66 CDHInstallFile]# echo never > /sys/kernel/mm/transparent_hugepage/defrag
[root@sp-66 CDHInstallFile]# echo never > /sys/kernel/mm/transparent_hugepage/enabled
[root@sp-66 CDHInstallFile]#

```
```

#### **每个节点都处理完成, 这个警告才会接触, 验证才会通过**

![](http://qiniu.dev-share.top/image/cm_setup_jiaoyan_ok.png)

### 选择服务

#### 选择 自定义 然后 安装如下顺序一个一个的装, `(不要一起装)`

HDFS  
YARN  
ZooKeeper  
HBase  
Hive  
Impala  
Spark  
Oozie  
Hue  
![](http://qiniu.dev-share.top/image/cm_setup_step.png)

### 角色分配

#### 默认直接继续

### 数据库设置

#### 点击测试后

![](http://qiniu.dev-share.top/image/cm_db_setting.png)

### 集群审核

#### 都默认的

![](http://qiniu.dev-share.top/image/cm_shenhe.png)

### 开始安装

![](http://qiniu.dev-share.top/image/cm_start_setup.png)

### 安装完成

![](http://qiniu.dev-share.top/image/cm_done.png)

### 常见问题

#### Hive 启动失败

![](http://qiniu.dev-share.top/image/cm_hive_error.png)  
解决方案:  
首先: mysql中重新创建一个数据库 hive  
其次: 为Hive添加mysql驱动

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@sp-66 CDHInstallFile]# cp mysql-connector-java-5.1.43-bin.jar /opt/cloudera/parcels/CDH/lib/hive/lib/

```
```

然后: 删除原来已经安装好的Hive插件以及相关的依赖插件.  
最后: 重新安装Hive插件.  
![](http://qiniu.dev-share.top/image/cm_hive_set_mysql.png)  
注意: 这里使用的是一个新数据库, 不要共用之前的数据库 !