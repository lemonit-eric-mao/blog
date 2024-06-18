---
title: "Java 导出堆信息"
date: "2019-09-10"
categories: 
  - "java"
---

##### 根据项目名，查看堆信息

```ruby
jps | grep 项目名 | awk '{print $1}' | xargs jmap -histo
```

* * *

##### 1.查看jmap 命令使用文档

```ruby
[root@dev15 ~]# docker exec -it 201-hrbm-hrbmweb bash
root@201-hrbm-hrbmweb-deploy:/#
root@201-hrbm-hrbmweb-deploy:/# jmap
Usage:
    jmap [option] <pid>
        (to connect to running process)
    jmap [option] <executable <core>
        (to connect to a core file)
    jmap [option] [server_id@]<remote server IP or hostname>
        (to connect to remote debug server)

where <option> is one of:
    <none>               to print same info as Solaris pmap
    -heap                to print java heap summary
    -histo[:live]        to print histogram of java object heap; if the "live"
                         suboption is specified, only count live objects
    -clstats             to print class loader statistics
    -finalizerinfo       to print information on objects awaiting finalization
    -dump:<dump-options> to dump java heap in hprof binary format
                         dump-options:
                           live         dump only live objects; if not specified,
                                        all objects in the heap are dumped.
                           format=b     binary format
                           file=<file>  dump heap to <file>
                         Example: jmap -dump:live,format=b,file=heap.bin <pid>
    -F                   force. Use with -dump:<dump-options> <pid> or -histo
                         to force a heap dump or histogram when <pid> does not
                         respond. The "live" suboption is not supported
                         in this mode.
    -h | -help           to print this help message
    -J<flag>             to pass <flag> directly to the runtime system
root@201-hrbm-hrbmweb-deploy:/#
```

##### 2.查看java程序的 pid

```ruby
root@201-hrbm-hrbmweb-deploy:/# jps
8 HrbmWebApplication
12879 Jps
root@201-hrbm-hrbmweb-deploy:/#
```

##### 3.进入docker容器内部，导出堆信息

```ruby
root@201-hrbm-hrbmweb-deploy:/# jmap -dump:format=b,file=heap.bin 8
Dumping heap to /heap.bin ...
Heap dump file created
root@201-hrbm-hrbmweb-deploy:/# ls | grep heap.bin
heap.bin
root@201-hrbm-hrbmweb-deploy:/#
```

##### 4.导出到本地

`docker cp 容器名:heap.bin .`

```ruby
[root@dev15 ~]# docker cp 201-hrbm-hrbmweb-deploy:heap.bin .
```

* * *

* * *

* * *

##### K8S 用法

###### 1 进入容器

`kubectl exec -it pod名 -n 命名空间 bash`

```ruby
[root@dev15 ~]# kubectl exec -it 412-pfizer-ftpbackup-deploy-6b79f844c6-hsqtc -n paas-app-dev2 bash
root@412-pfizer-ftpbackup-deploy-6b79f844c6-hsqtc:/# jps
9383 Jps
10 PfizerBackupApplication
root@412-pfizer-ftpbackup-deploy-6b79f844c6-hsqtc:/#
root@412-pfizer-ftpbackup-deploy-6b79f844c6-hsqtc:/# jmap -dump:format=b,file=heap.bin 10
root@412-pfizer-ftpbackup-deploy-6b79f844c6-hsqtc:/# ls | grep heap.bin
heap.bin
root@412-pfizer-ftpbackup-deploy-6b79f844c6-hsqtc:/#
```

###### 2 导出文件

`kubectl cp pod名:heap.bin ./ -n 命名空间 bash`

```ruby
[root@dev15 ~]# kubectl cp 412-pfizer-ftpbackup-deploy-6b79f844c6-hsqtc:heap.bin ./ -n paas-app-dev2 bash
```

* * *

* * *

* * *
