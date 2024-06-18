---
title: "docker-compose 安装FastDFS"
date: "2019-11-13"
categories: 
  - "fastdfs"
---

镜像地址：https://hub.docker.com/r/season/fastdfs

##### 【**前置条件**】

- CentOS Linux release 7.6.1810 (Core)
- 4.20.10-1.el7.elrepo.x86\_64
- 主机IP: 172.160.180.48
- 客户端语言: Python 2.7.5

* * *

##### `tracker的client.conf` 与 `storage的client.conf` 与 `客户端的client.conf` 配置文件内容是一样的

```yml
# connect timeout in seconds
# default value is 30s
connect_timeout=30

# network timeout in seconds
# default value is 30s
network_timeout=60

# the base path to store log files
base_path=/fastdfs/client

# tracker_server can ocur more than once, and tracker_server format is
#  "host:port", host can be hostname or ip address
tracker_server=172.160.180.48:22122

#standard log level as syslog, case insensitive, value list:
### emerg for emergency
### alert
### crit for critical
### error
### warn for warning
### notice
### info
### debug
log_level=info

# if use connection pool
# default value is false
# since V4.05
use_connection_pool = false

# connections whose the idle time exceeds this time will be closed
# unit: second
# default value is 3600
# since V4.05
connection_pool_max_idle_time = 3600

# if load FastDFS parameters from tracker server
# since V4.05
# default value is false
load_fdfs_parameters_from_tracker=false

# if use storage ID instead of IP address
# same as tracker.conf
# valid only when load_fdfs_parameters_from_tracker is false
# default value is false
# since V4.05
use_storage_id = false

# specify storage ids filename, can use relative or absolute path
# same as tracker.conf
# valid only when load_fdfs_parameters_from_tracker is false
# since V4.05
storage_ids_filename = storage_ids.conf


#HTTP settings
http.tracker_server_port=80

#use "#include" directive to include HTTP other settiongs
##include http.conf

```

* * *

##### docker-compose-tracker.yaml

```ruby
cat > /home/FastDFS/docker-compose-tracker.yaml << eric

# 使用方法 docker-compose -f docker-compose-tracker.yaml up -d
version: '3.1'

services:

  tracker:
    image: season/fastdfs:1.2
    restart: always
    network_mode: host
    container_name: tracker
    command: tracker
    volumes:
      # 容器与宿主机时间同步
      - /etc/localtime:/etc/localtime
      - ./tracker/data:/fastdfs/tracker/data
      - ./tracker/config/client.conf:/etc/fdfs/client.conf
    environment:
      TIME_ZONE: Asia/Shanghai
eric

```

##### docker-compose-storage.yaml

```ruby
cat > /home/FastDFS/docker-compose-storage.yaml << eric

# 使用方法 docker-compose -f docker-compose-storage.yaml up -d
version: '3.1'

services:

  storage:
    image: season/fastdfs:1.2
    restart: always
    network_mode: host
    container_name: storage
    command: storage
    volumes:
      # 容器与宿主机时间同步
      - /etc/localtime:/etc/localtime
      - ./storage/data:/fastdfs/storage/data
      - ./storage/config/client.conf:/etc/fdfs/client.conf
      - ./store/path:/fastdfs/store_path
    environment:
      TIME_ZONE: Asia/Shanghai
      # 指定主机IP与tracker的默认端口号
      TRACKER_SERVER: "172.160.180.48:22122"
eric

```

##### 测试client.conf是否配置成功

`docker exec -it tracker fdfs_monitor /etc/fdfs/client.conf` `docker exec -it storage fdfs_monitor /etc/fdfs/client.conf`

* * *

* * *

* * *

##### 使用 FastDFS Python客户端进行测试文件上传下载

###### 1 到python 仓库下回 FastDFS客户端

- [pip 仓库地址](https://pypi.org/ "pip 仓库地址")
- [FastDFS 客户端下载地址](https://files.pythonhosted.org/packages/b8/1d/d701dbd6830a5b7170655e62acb0977560c61bf4cc6a2185006c68b9e2ec/fdfs_client-4.0.7.tar.gz "FastDFS 客户端下载地址")

```ruby
[root@test4 ~]# yum list | grep python-devel
# 安装依赖
[root@test4 ~]# yum install -y python-devel.x86_64
[root@test4 ~]#
[root@test4 ~]# pip install mutagen requests
[root@test4 ~]#
# 安装客户端
[root@test4 ~]# pip install fdfs_client-4.0.7.tar.gz
[root@test4 ~]#
```

###### 2 编写客户端脚本

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/15 10:58
# @Author  : Eric.Mao
# @FileName: up_down_file.py
# @Software: PyCharm
# @Blog    ：https://msyblog.lemonit.cn

from fdfs_client.client import *


class FileUploadAndDownload(object):

    def __init__(self):
        self.client = Fdfs_client('./client.conf')

    def uploadFild(self, file_full_path):
        result = self.client.upload_by_filename(file_full_path)
        # 上传成功后，返回的数据结构
        # {
        #     'Status': 'Upload successed.',
        #     'Storage IP': '172.160.180.48',
        #     'Remote file_id': 'group1/M00/00/00/wKi0MF3ONP2AXBePEWHZUyKp6gE.tar.gz',
        #     'Group name': 'group1',
        #     'Local file name': '../elasticsearch-7.4.0-linux-x86_64.tar.gz',
        #     'Uploaded size': '278.00MB'
        # }
        print(result)
        # 获取已上传的远程文件ID
        print(result['Remote file_id'])

    def downloadFile(self, local_filename, remote_file_id):
        # 根据文件的
        result = self.client.download_to_file(local_filename, remote_file_id)
        # 下载成功后，返回的数据结构
        # {
        #     'Content': 'new-elasticsearch-7.4.0-linux-x86_64.tar.gz',
        #     'Remote file_id': 'group1/M00/00/00/wKi0MF3ONP2AXBePEWHZUyKp6gE.tar.gz',
        #     'Storage IP': '172.160.180.48',
        #     'Download size': '278.00MB'
        # }
        print(result)

    def deleteFile(self, remote_file_id):
        result = self.client.delete_file(remote_file_id)
        # 删除成功后，返回的数据结构
        # ('Delete file successed.', 'group1/M00/00/00/wKi0MF3ONP2AXBePEWHZUyKp6gE.tar.gz', '172.160.180.48')
        print(result)


if __name__ == '__main__':
    __this = FileUploadAndDownload()
    # 启动程序
    # 上传文件
    #  __this.uploadFild('../elasticsearch-7.4.0-linux-x86_64.tar.gz')

    # 下载文件
    # __this.downloadFile('./new-elasticsearch-7.4.0-linux-x86_64.tar.gz', 'group1/M00/00/00/wKi0MF3ONP2AXBePEWHZUyKp6gE.tar.gz')

    # 删除文件
    __this.deleteFile('group1/M00/00/00/wKi0MF3ONP2AXBePEWHZUyKp6gE.tar.gz')

```
