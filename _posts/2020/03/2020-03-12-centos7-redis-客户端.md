---
title: "CentOS 7 Redis 客户端"
date: "2020-03-12"
categories: 
  - "redis"
---

**[下载地址](http://qiniu.dev-share.top/redis-cli "下载地址")**

### 下载并添加到环境变量

首先注意 `usr` 指 **`Unix System Resource`**，而不是 **User** **`/usr/bin`** 下面的都是系统预装的可执行程序，会随着系统升级而改变。 **`/usr/local/bin`** 目录是给用户放置自己的可执行程序的地方，推荐放在这里，不会被系统升级而覆盖同名文件。

```ruby
[root@master ~]# wget http://qiniu.dev-share.top/redis-cli -P /usr/local/bin/ && chmod -R 755 /usr/local/bin/redis-cli
```

* * *

### 用法

`redis-cli -h host -p port -a password`

```ruby
[root@master ~]# redis-cli -h 192.168.2.10 -p 6379 -a 123456
192.168.2.10:6379> PING
PONG
192.168.2.10:6379>
```

* * *

#### [常用命令](https://www.runoob.com/redis/redis-commands.html "常用命令")

* * *

#### [只安装客户端](http://www.dev-share.top/2019/08/01/centos-7-%e5%8f%aa%e5%ae%89%e8%a3%85%e5%ae%a2%e6%88%b7%e7%ab%af/ "只安装客户端")

* * *

* * *

* * *

### Redis 图形化客户端

**[下载 RedisDesktopManager 2019](http://qiniu.dev-share.top/file/RedisDesktopManager%202019%20%E7%BB%BF%E8%89%B2%E7%89%88.zip "下载 RedisDesktopManager 2019")**

* * *

* * *

* * *

### **redis-full-check**

> 校验两个Redis中的数据是否一致

```shell
## 下载安装
wget https://github.com/alibaba/RedisFullCheck/releases/download/release-v1.4.8-20200212/redis-full-check-1.4.8.tar.gz
## 或 从七牛云下载
wget http://qiniu.dev-share.top/file/redis-full-check-1.4.8.tar.gz && \
     tar -zxvf redis-full-check-1.4.8.tar.gz && \
     mv redis-full-check-1.4.8/redis-full-check /usr/local/bin/


[root@centos01 ~]# redis-full-check -v
improve-1.4.8,8eb8326054a83dd91d1bbf55b455b4e730b612bf,go1.10.1,2020-02-12_18:32:51

```

**工具使用**

```shell
redis-full-check -s 192.168.101.21:6379 -p ****** \
                 -t 192.168.101.22:6379 -a ****** \
                 --log log \
                 --comparetimes=1 \
                 --interval=3 \
                 --comparemode=1 \
                 --result result

```

**输出结果如下**

```shell
[INFO 2022-10-10-10:41:56 main.go:65]: init log success

## 数据库信息
[INFO 2022-10-10-10:41:56 main.go:168]: configuration: {192.168.101.21:6379 ****** auth 0 -1 192.168.101.22:6379 ****** auth 0 -1 result.db result 1 1 unknown unknown unknown 15000 3 256 5 log  false 16384  20445 false}
[INFO 2022-10-10-10:41:56 main.go:170]: ---------
[INFO 2022-10-10-10:41:56 full_check.go:238]: sourceDbType=0, p.sourcePhysicalDBList=[meaningless]

## 将比较哪些 db
[INFO 2022-10-10-10:41:56 full_check.go:243]: db=1:keys=5
[INFO 2022-10-10-10:41:56 full_check.go:243]: db=0:keys=100

[INFO 2022-10-10-10:41:56 full_check.go:253]: ---------------- start 1th time compare

## 开始比较 db1
[INFO 2022-10-10-10:41:56 full_check.go:278]: start compare db 1
[INFO 2022-10-10-10:41:56 scan.go:20]: build connection[source redis addr: [192.168.101.21:6379]]
[INFO 2022-10-10-10:41:57 full_check.go:203]: stat:
times:1, db:1, dbkeys:5, finish:100%, finished:true
## 扫描到 5个key
KeyScan:{5 5 0}
## 源库与目的库的 key、value 完全相同的有2个
KeyEqualAtLast|string|equal|{2 2 0}
## 源库与目的库的 key相同，value不同的有1个
KeyConflictAtLast|string|value|{1 1 0}
## 目的库 缺少的key有2个
KeyConflictAtLast|string|lack_target|{2 2 0}

## 开始比较 db0
[INFO 2022-10-10-10:41:57 full_check.go:278]: start compare db 0
[INFO 2022-10-10-10:41:57 scan.go:20]: build connection[source redis addr: [192.168.101.21:6379]]
[INFO 2022-10-10-10:41:58 full_check.go:203]: stat:
times:1, db:0, dbkeys:100, finish:100%, finished:true
KeyScan:{100 100 0}
KeyEqualAtLast|string|equal|{18 18 0}
KeyConflictAtLast|string|value|{81 81 0}
KeyConflictAtLast|string|lack_target|{1 1 0}

## 比较完成
[INFO 2022-10-10-10:41:58 full_check.go:328]: --------------- finished! ----------------
all finish successfully, totally 85 key(s) and 0 field(s) conflict

```

**使用说明**

```shell
redis-full-check -s 源redis库:端口   -p 源redis库密码   \
                 -t 目的redis库:端口 -a 目的redis库密码 \
                 --log log \            将控制台日志，写入到本地
                 --comparetimes=3 \     比较轮数。             (默认值：3)
                 --interval=5 \         每轮之间的时间间隔。    (默认值：5秒)
                 --comparemode=2 \      比较模式：             (默认值：2)
                                                 1 表示全量比较
                                                 2 表示只对比value的长度
                                                 3 只对比key是否存在
                                                 4 全量比较的情况下，忽略大key的比较
                 --result result \      不一致结果记录到result文件中
```

**具体参数可查看** `redis-full-check -h` **[官方文档](https://developer.aliyun.com/article/690463?accounttraceid=d8ee62cf163c4a0d943e2088518410echsgp "官方文档")** **[稀土掘金解释](https://juejin.cn/post/6844904047569289223 "稀土掘金解释")**
