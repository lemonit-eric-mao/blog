---
title: "Linux 硬件测试"
date: "2019-10-09"
categories: 
  - "linux服务器"
---

##### 前置条件

| 名称 | 数值 |
| :-- | :-- |
| 操作系统 | CentOS Linux release 7.9.2009 (Core) |
| CPU | 16核 |
| 内存 | 32G |

* * *

* * *

* * *

##### **安装`stress`**

```ruby
[root@localhost ~]# yum install -y epel-release && yum install -y stress
```

##### 查看命令的使用文档

```ruby
[root@localhost ~]# stress
`stress' imposes certain types of compute stress on your system

Usage: stress [OPTION [ARG]] ...
 -?, --help         show this help statement
     --version      show version statement
 -v, --verbose      be verbose
 -q, --quiet        be quiet
 -n, --dry-run      show what would have been done
 -t, --timeout N    timeout after N seconds
     --backoff N    wait factor of N microseconds before work starts
 -c, --cpu N        spawn N workers spinning on sqrt()
 -i, --io N         spawn N workers spinning on sync()
 -m, --vm N         spawn N workers spinning on malloc()/free()
     --vm-bytes B   malloc B bytes per vm worker (default is 256MB)
     --vm-stride B  touch a byte every B bytes (default is 4096)
     --vm-hang N    sleep N secs before free (default none, 0 is inf)
     --vm-keep      redirty memory instead of freeing and reallocating
 -d, --hdd N        spawn N workers spinning on write()/unlink()
     --hdd-bytes B  write B bytes per hdd worker (default is 1GB)

Example: stress --cpu 8 --io 4 --vm 2 --vm-bytes 128M --timeout 10s

Note: Numbers may be suffixed with s,m,h,d,y (time) or B,K,M,G (size).

```

**注意**：数字可以加s，m，h，d，y（时间）或B，K，M，G（大小）作为后缀。

* * *

##### **对`CPU`进行压测**

> 使用 **stress -c `N`** 会让stress生成`N`个工作进程进行开方运算，以此对CPU产生负载。 比如你想保持3个CPU满负载工作 `stress -c 3` 比如你想保持3个CPU满负载工作，并且只测试120秒 `stress -c 3 -t 120s`
> 
> | 参数 | 说明 |
> | :-- | :-- |
> | `--cpu` 3 | 让3个CPU(`满负载工作`) |
> | `-t` 120s | 测试120S |

* * *

##### **对`内存`进行压测**

> 模拟产生6个进程，每个进程分配2G内存，持续消耗内存10秒后在释放，测试60S `stress --vm 6 --vm-bytes 2G --vm-hang 10 -t 60s`
> 
> | 参数 | 说明 |
> | :-- | :-- |
> | `--vm` 6 | 模拟产生6个进程 |
> | `--vm-bytes` 2G | 每个进程分配1个G内存 |
> | `--vm-keep` | 分配后不释放内存 |
> | `--vm-hang` 10 | 持续消耗内存10秒后在释放 |
> | `-t` 60s | 测试60S |

* * *

##### **对`磁盘`进行压测**

> `stress -d N --hdd-bytes B` 会产生`N`个进程，每个进程往当前目录中写入`B`大小的临时文件。 `stress -d 4 --hdd-bytes 2G -t 100s`
> 
> | 参数 | 说明 |
> | :-- | :-- |
> | `-d` 4 | 模拟产生4个io进程 |
> | `--hdd-bytes` 2G | 往当前目录中写入固定大小的临时文件 |
> | `-t` 100s | 测试100S |

* * *

* * *

* * *
