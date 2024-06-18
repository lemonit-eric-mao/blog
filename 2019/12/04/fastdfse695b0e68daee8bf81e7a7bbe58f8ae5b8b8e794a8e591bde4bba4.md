---
title: FastDFS数据迁移及常用命令
date: '2019-12-04T02:26:08+00:00'
status: publish
permalink: /2019/12/04/fastdfs%e6%95%b0%e6%8d%ae%e8%bf%81%e7%a7%bb%e5%8f%8a%e5%b8%b8%e7%94%a8%e5%91%bd%e4%bb%a4
author: 毛巳煜
excerpt: ''
type: post
id: 5177
category:
    - FastDFS
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
前提：所用镜像image: luhuiguo/fastdfs  
其他镜像命令自行修改  
思维流程导向：old-tracker storage ——&gt;加一个新的storage做同步用——&gt;查看状态等待数据同步完成——&gt;断开连接——&gt;修改tracker为新的地址——&gt;修改`storage0/data/.data_init_flag`配置文件（sync\_src\_server=）置为空——&gt;重新启动storage——&gt;成功！！！

###### 1、[安装fastdfs](https://blog.csdn.net/jiangbenchu/article/details/99425585)（开始）

旧tracker：172.160.180.46  
新tracker：172.160.180.48  
eg：存储一个文件返回路径为-做为后续查找使用：http://172.160.180.46/group1/M00/00/00/wKi0Ll3bji6AKxJiAAAABncc3SA697\_big.txt

###### 2、修改新的Storage配置文件，部署在新的服务器②172.160.180.48上（只安装storage，tracker先用旧的tracker）

vim leo\_docker-compose.yaml

```yml
version: '3.0'

services:
   fastdfs:
     image: luhuiguo/fastdfs
     container_name: tracker
     network_mode: host
     command: tracker
     volumes:
     - ./fdfs/tracker:/var/fdfs

   storage0:
     container_name: storage0
     image: luhuiguo/fastdfs
     command: storage
     network_mode: host
     environment:
       - TRACKER_SERVER=172.160.180.46:22122
       - GROUP_NAME=group1
     volumes:
     - ./fdfs/storage0:/var/fdfs

```

**注：TRACKER\_SERVER配置为旧的tracker**

###### 3、启动storage和新的tracker

```ruby
docker-compose -f leo_docker-compose.yaml up -d

```

###### 4、查看监控状态

新的storage节点已经加进来了  
且ip\_addr = 172.160.180.48 (test3) ACTIVE  
如果ip\_addr = 172.160.180.48 (test3) SYNCING表示正在同步数据  
ip\_addr = 172.160.180.48 (test3) WAIT\_SYNC等待同步

```ruby
docker exec -it storage0 fdfs_monitor /etc/fdfs/client.conf

```

```ruby
[root@test1 luhuiguo_fastdfs]# docker exec -it storage0 fdfs_monitor /etc/fdfs/client.conf
[2019-11-25 08:31:31] DEBUG - base_path=/var/fdfs, connect_timeout=30, network_timeout=60, tracker_server_count=1, anti_steal_token=0, anti_steal_secret_key length=0, use_connection_pool=0, g_connection_pool_max_idle_time=3600s, use_storage_id=0, storage server id count: 0

server_count=1, server_index=0

tracker server is 172.160.180.46:22122

group count: 2

Group 1:
group name = group1
disk total space = 120819 MB
disk free space = 100004 MB
trunk free space = 0 MB
storage server count = 2
active server count = 2
storage server port = 23000
storage HTTP port = 8888
store path count = 1
subdir count per path = 256
current write server index = 0
current trunk file id = 0

        Storage 1:
                id = 172.160.180.46
                ip_addr = 172.160.180.46 (test1)  ACTIVE
                ……
        Storage 2:
                id = 172.160.180.48
                ip_addr = 172.160.180.48 (test3)  ACTIVE
               ……

Group 2:
group name = group2
disk total space = 120819 MB
disk free space = 100004 MB
trunk free space = 0 MB
storage server count = 1
active server count = 1
storage server port = 22222
storage HTTP port = 8888
store path count = 1
subdir count per path = 256
current write server index = 0
current trunk file id = 0

        Storage 1:
                id = 172.160.180.46
                ip_addr = 172.160.180.46 (test1)  ACTIVE
                ……


```

###### 5、这时我们在新的服务器上查看之前在旧的fastdfs上传的文件（根据之前存储的返回路径http://172.160.180.46/group1/M00/00/00/wKi0Ll3bji6AKxJiAAAABncc3SA697\_big.txt）

```ruby
[root@test3 data]# cat 00/00/wKi0Ll3bji6AKxJiAAAABncc3SA697_big.txt
hello

```

可以看到已经同步到这台新的服务器上了

###### 6、同步完成后,停掉新的Storage服务器进程

```ruby
docker-compose -f leo_docker-compose.yaml stop storage0

```

再次查看状态

```ruby
docker exec -it storage0 fdfs_monitor /etc/fdfs/client.conf

# 可以看到已经下线了ip_addr = 172.160.180.48 (test3) OFFLINE

[2019-11-25 08:31:31] DEBUG - base_path=/var/fdfs, connect_timeout=30, network_timeout=60, tracker_server_count=1, anti_steal_token=0, anti_steal_secret_key length=0, use_connection_pool=0, g_connection_pool_max_idle_time=3600s, use_storage_id=0, storage server id count: 0

server_count=1, server_index=0

tracker server is 172.160.180.46:22122

group count: 2

Group 1:
group name = group1
disk total space = 120819 MB
disk free space = 100004 MB
trunk free space = 0 MB
storage server count = 2
active server count = 2
storage server port = 23000
storage HTTP port = 8888
store path count = 1
subdir count per path = 256
current write server index = 0
current trunk file id = 0

        Storage 1:
                id = 172.160.180.46
                ip_addr = 172.160.180.46 (test1)  ACTIVE
                ……
        Storage 2:
                id = 172.160.180.48
                ip_addr = 172.160.180.48 (test3)  OFFLINE
               ……

Group 2:
group name = group2
disk total space = 120819 MB
disk free space = 100004 MB
trunk free space = 0 MB
storage server count = 1
active server count = 1
storage server port = 22222
storage HTTP port = 8888
store path count = 1
subdir count per path = 256
current write server index = 0
current trunk file id = 0

        Storage 1:
                id = 172.160.180.46
                ip_addr = 172.160.180.46 (test1)  ACTIVE
                ……


```

###### 7、（docker-compose启动不用执行此步骤，二进制需要）修改.data\_init\_flag文件，将文件中sync\_src\_server配置项留空，其它配置项不变

sync\_src\_server=

```ruby
[root@test3 data]# pwd
/home/fastdfs/fdfs/storage0/data
[root@test3 data]# ll -a
[root@test3 data]# vim .data_init_flag
storage_join_time=1574668867
sync_old_done=1
sync_src_server=
sync_until_timestamp=1574668870
last_ip_addr=172.160.180.48
last_server_port=23000
last_http_port=8888
current_trunk_file_id=0
trunk_last_compress_time=0


```

###### 8、重新启动storage

`docker-compose -f leo_docker-compose.yaml up -d storage0`

###### 9、查看状态已经切换到了新的tracker（结束）

```ruby
docker exec -it storage0 fdfs_monitor /etc/fdfs/client.conf

```

```ruby
[root@test3 fastdfs]# docker exec -it storage0 fdfs_monitor /etc/fdfs/client.conf
[2019-11-25 09:46:45] DEBUG - base_path=/var/fdfs, connect_timeout=30, network_timeout=60, tracker_server_count=1, anti_steal_token=0, anti_steal_secret_key length=0, use_connection_pool=0, g_connection_pool_max_idle_time=3600s, use_storage_id=0, storage server id count: 0

server_count=1, server_index=0

tracker server is 172.160.180.48:22122

group count: 1

Group 1:
group name = group1
disk total space = 120819 MB
disk free space = 107597 MB
trunk free space = 0 MB
storage server count = 1
active server count = 1
storage server port = 23000
storage HTTP port = 8888
store path count = 1
subdir count per path = 256
current write server index = 0
current trunk file id = 0

        Storage 1:
                id = 172.160.180.48
                ip_addr = 172.160.180.48 (test3)  ACTIVE
                http domain =


```

**验证1**、如果想要再次验证，就再找一台服务器创建storage连接新的tracker。  
查看连接状态（ip\_addr = 172.160.180.47 (test2) ACTIVE ）为验证的服务器

```
[root@test3 fastdfs]# docker exec -it storage0 fdfs_monitor /etc/fdfs/client.conf
[2019-11-25 09:53:30] DEBUG - base_path=/var/fdfs, connect_timeout=30, network_timeout=60, tracker_server_count=1, anti_steal_token=0, anti_steal_secret_key length=0, use_connection_pool=0, g_connection_pool_max_idle_time=3600s, use_storage_id=0, storage server id count: 0

server_count=1, server_index=0

tracker server is 172.160.180.48:22122

group count: 1

Group 1:
group name = group1
disk total space = 120819 MB
disk free space = 101093 MB
trunk free space = 0 MB
storage server count = 2
active server count = 2
storage server port = 23000
storage HTTP port = 8888
store path count = 1
subdir count per path = 256
current write server index = 0
current trunk file id = 0

        Storage 1:
                id = 172.160.180.47
                ip_addr = 172.160.180.47 (test2)  ACTIVE
                ……
        Storage 2:
                id = 172.160.180.48
                ip_addr = 172.160.180.48 (test3)  ACTIVE
                http domain =
                version = 5.11
                ……


```

1.1、在新加的storage上查看我们迁移过来的数据——因为是同一个group所以是同步的，根据之前返回的数据路径，在新加的storage服务器上查看。

```
[root@test2 cluster]# cat fdfs/storage0/data/00/00/wKi0Ll3bji6AKxJiAAAABncc3SA697_big.txt
hello

```

可以看到数据已经同步过来了！  
**使用备注**：

```
docker-compose修改配置文件需要重启其中一个service需要
docker-compose -f leo_docker-compose.yaml stop
docker-compose -f leo_docker-compose.yaml up -d storage0 #不能用start启动

```

**验证2**、

①、上传  
eg：  
/root@localhost:/# usr/bin/fdfs\_test /etc/fdfs/client.conf upload a.txt

②、下载  
eg：\[root@test1 fastdfs\]# /usr/bin/fdfs\_test /etc/fdfs/client.conf download group1 M00/00/00/wKi0Ll3bji6AKxJiAAAABncc3SA697\_big.txt

```
Usage: /usr/bin/fdfs_test <config_file> download <group_name> <remote_filename>
</remote_filename></group_name></config_file>
```

③、删除（所有storage中的文件都会删除）  
eg：\[root@test1 fastdfs\]# /usr/bin/fdfs\_test /etc/fdfs/client.conf delete group1 M00/00/00/wKi0Ll3cwVCAHq1oAAAADj9UaMQ484.txt

```
Usage: /usr/bin/fdfs_test <config_file> delete <group_name> <remote_filename>
</remote_filename></group_name></config_file>
```

**验证3**、不同情况下同步合并验证

```
===========46===========
①上传example file url: http://172.160.180.46/group1/M00/00/00/wKi0Ll3c2tGACRe1AAAACfdYteI663_big.txt
leojiang

②上传example file url: http://172.160.180.46/group1/M00/00/00/wKi0Ll3c4vGAeuJnAAAACBgItVc245_big.txt
maosiyu

③同步lihongbao

④上传example file url: http://172.160.180.46/group1/M00/00/00/wKi0Ll3c6C2AUFlvAAAAA7UVEzU990_big.txt
46
④同步48

===========48===========
①同步leojiang

②同步maosiyu

③上传example file url: http://172.160.180.48/group1/M00/00/00/wKi0MF3c5R2AA5oKAAAACit7gaU604_big.txt
lihongbao

④上传example file url: http://172.160.180.48/group1/M00/00/00/wKi0MF3c52SAVkcXAAAAA9SWPrs177_big.txt
48
④同步46

```

### **命令参考**：

```
查看tracker的配置
docker exec -it tracker fdfs_monitor /etc/fdfs/client.conf
参数说明：
tracker_server_count：2 --表示2个Tracker Server
tracker server is 198.168.1.121:22122 --表示Leader Tracker
group count: 1  --表示有1个group
group name = group1 --组名称是group1
storage server count = 2    --组内有2个storage
active server count = 2 --活动的storage有2个
storage server port = 23002 --storage的端口
storage HTTP port = 9101    --storage的文件访问端口
store path count = 1    --storage只挂了一个存储目录
total_upload_count = 11 --总共上传了多少个文件
total_upload_bytes = 691405 --总共上传了多少字节
success_upload_bytes = 691405 --成功上传了多少字节
total_download_count = 2    --总共下载了多少文件（使用java客户端）

```

```
查看状态：
docker exec -it storage0 fdfs_monitor /etc/fdfs/client.conf
创建文件：
root@localhost:/# echo hello>a.txt
上传文件：
/usr/bin/fdfs_test /etc/fdfs/client.conf upload a.txt
/usr/bin/fdfs_test /etc/fdfs/client.conf download group1 M00/02/32/CgAUD1s6716ATKtBAAMd3jd5Lxc105.png

1）wKjyglxkBuSAbT8iAAAAAc3XBpM982.txt 是主文件 。
2）wKjyglxkBuSAbT8iAAAAAc3XBpM982_big.txt 是从文件。
3)wKjyglxkBuSAbT8iAAAAAc3XBpM982.txt-m 文件 是 wKjyglxkBuSAbT8iAAAAAc3XBpM982.txt文件 属性文件，意思就是：wKjyglxkBuSAbT8iAAAAAc3XBpM982.txt-m中存放的是wKjyglxkBuSAbT8iAAAAAc3XBpM982.txt文件的各项属性的信息，比如文件的类型，高度和宽度等等属性的信息。


upload：上传普通文件，包括主文件
upload_appender：上传appender文件，后续可以对其进行append、modify和truncate操作
upload_slave：上传从文件
download：下载文件
delete：删除文件
append：在appender文件后追加内容
modify：appender文件修改
set_metadata：设置文件附加属性
get_metadata：获取文件附加属性

重启跟踪器：
/usr/bin/restart.sh /usr/bin/fdfs_trackerd /etc/fdfs/tracker.conf

重启存储器
/usr/bin/restart.sh /usr/bin/fdfs_storaged /etc/fdfs/storage.conf

```

```
参数形式如下：
volume0/M00/00/02/Cs8b8lFJIIyAH841AAAbpQt7xVI4715674

volume0：组名
M00：磁盘名
00/02：目录
Cs8b8lFJIIyAH841AAAbpQt7xVI4715674：文件名，采用base64编码，信息包含源storage server Ip、文件创建时间、文件大小、文件CRC32效验码和随机数

```

##### （以上是个人验证的结果，仅供参考）