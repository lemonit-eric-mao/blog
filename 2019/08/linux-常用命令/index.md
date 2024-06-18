---
title: "Linux 常用命令"
date: "2019-08-27"
categories: 
  - "linux服务器"
---

### 52\. screen 创建多个虚拟会话

1. **启动一个新的 screen 会话**:
    
    - `screen` - 启动一个普通的 screen 会话。
    - `screen -S session_name` - 启动一个新的命名 screen 会话。
2. **附加到已存在的 screen 会话**:
    
    - `screen -r` - 重新附加到最近的会话。
    - `screen -r session_name_or_pid` - 重新附加到一个指定的会话。
3. **在后台运行 screen 会话**:
    
    - `screen -dmS session_name command` - 在后台以守护进程方式启动一个会话，并执行 `command`。
4. **会话管理**:
    
    - `Ctrl+a, c` - 创建一个新的窗口。
    - `Ctrl+a, n` 或 `Ctrl+a, p` - 切换到下一个或上一个窗口。
    - `Ctrl+a, w` - 显示所有窗口列表。
    - `Ctrl+a, k` - 杀死当前窗口。
5. **日志和记录**:
    
    - `screen -L` - 启用日志记录。
    - `screen -Logfile filename` - 指定日志文件名。
6. **调整屏幕设置**:
    
    - `screen -h lines` - 设置历史缓冲区的大小为 `lines` 行。
    - `screen -s shell` - 指定一个不同的 shell 来运行。
7. **查看和清理会话**:
    
    - `screen -ls` - 列出所有会话。
    - `screen -wipe` - 清理已死掉的会话。
8. **退出 screen 会话**:
    
    - `Ctrl+a, d` - detach 当前 screen 会话。
    - `exit` - 在窗口中输入 `exit` 来结束当前窗口的会话。
9. **其他选项**:
    
    - `-x` - Attach to a not detached screen。这允许在一个屏幕内显示多个会话。
    - `-U` - 告诉 screen 使用 UTF-8 编码。

#### 实际使用

```bash
# 创建一个名为 siyu 的回话
screen -S  siyu

# 之后会有一个全新的回话，在新回话中运行你的程序

# 离开当前会话，运行的程序不会退出
# 快捷键操作
Ctrl+a, d
# 会提示
[detached from 56118.siyu]


# 查看会话列表
[cloud@AI (19:24:16) ~]
└─$ screen -ls
There is a screen on:
        56118.siyu (2024年04月26日 19时22分12秒)   (Detached)
1 Socket in /run/screen/S-cloud.


# 进入一个已经存在的会话
screen -r siyu

```

* * *

* * *

### 51\. traceroute 路由追踪

```bash
# windows 系统使用命令
tracert -d -w 1 111.45.201.154

通过最多 30 个跃点跟踪到 111.45.201.154 的路由

  1     1 ms    <1 毫秒   <1 毫秒 192.168.2.1
  2     5 ms     *        6 ms  116.3.88.1
  3     *        *        *     请求超时。
  4     *       19 ms    19 ms  113.230.175.201
  5    14 ms    14 ms    14 ms  219.158.119.90
  6     *       10 ms    15 ms  221.183.95.89
  7     *        *        *     请求超时。
  8     *        *        *     请求超时。
  9    17 ms    17 ms    17 ms  111.45.201.154

跟踪完成。
```

```bash
# linux 系统使用命令
traceroute -n -w 1 116.3.88.230


traceroute to 116.3.88.230 (116.3.88.230), 30 hops max, 60 byte packets
 1  * * *
 2  * * *
 3  10.162.66.141  1.472 ms * 10.162.66.181  1.435 ms
 4  10.200.66.101  2.598 ms 10.200.66.125  3.074 ms 10.196.95.177  1.457 ms
 5  220.196.197.162  2.613 ms 220.196.197.173  2.863 ms 220.196.197.170  2.978 ms
 6  220.196.197.161  3.400 ms  3.128 ms  3.089 ms
 7  211.95.32.25  4.091 ms 219.158.112.62  32.095 ms  32.621 ms
 8  113.230.187.222  34.797 ms 219.158.112.62  32.217 ms 113.230.167.242  35.901 ms
 9  113.230.166.210  35.727 ms 113.230.181.62  35.892 ms *
10  116.3.88.230  38.001 ms 61.189.82.162  39.201 ms *

```

* * *

* * *

### 50\. alias 别名

```bash
echo 'alias ll="ls -lh"' >> ~/.bashrc
```

* * *

* * *

### 49\. `tee` 命令有许多用法，下面是一些常见用法的示例：

1. **将命令的标准输出写入文件**：
    
    ```bash
    command | tee filename.txt
    ```
    
    这会将命令的标准输出写入 `filename.txt` 文件，并将其同时输出到终端。
    
2. **追加到文件**：
    
    ```bash
    echo 'hello world!' | tee -a filename.txt
    ```
    
    使用 `-a` 选项可以将命令的标准输出追加到文件而不覆盖文件内容。
    
3. **将输出发送到多个文件**：
    
    ```bash
    echo 'hello world!' | tee file1.txt file2.txt file3.txt
    ```
    
    这会将命令的标准输出分别写入 `file1.txt`、`file2.txt` 和 `file3.txt` 文件，并将其同时输出到终端。
    
4. **使用输入重定向和 `tee` 创建文件**：
    
    ```bash
    tee filename.txt <<EOF
    This is line 1.
    This is line 2.
    EOF
    ```
    
    这会创建一个名为 `filename.txt` 的文件，并将文本块中的内容写入文件。
    
5. **输出到 `/dev/null`（丢弃输出）**：
    
    ```bash
    ls -l | tee /dev/null
    ```
    
    这会将命令的标准输出丢弃，不写入文件也不显示在终端上。
    

* * *

* * *

### 48\. SSH 隧道

> - **SSH 端口转发（SSH Port Forwarding），也称 SSH 隧道（SSH Tunneling）**

```shell
ssh -fNL [本地主机内网IP]:[内网端口]:[远程主机内网IP]:[内网端口]  [远程主机SSH用户名]@[远程主机SSH外网IP] -p [外网端口]

## 此命令可以使用任何端口的转发映射如：
# ssh -fNL 172.18.10.62:10022:192.168.0.15:22 root@12.73.6.108 -p 32222
# ssh -fNL 172.18.10.62:10080:192.168.0.15:80 root@12.73.6.108 -p 32222
# ssh -fNL 172.18.10.62:16443:192.168.0.15:6443 root@12.73.6.108 -p 32222
```

> - 这个命令将会在`本地主机`将内网端口`10022`转发到`远程`主机内网`192.168.0.15`的`22`端口，
>     - 远程主机的外网`IP`地址为 `12.73.6.108`
>     - 远程主机的外网SSH连接的`用户名`为`root`
>     - 远程主机的外网SSH连接的`端口`为`32222`

```shell
## 测试
[root@centos-01 (11:56:57) ~]
└─# ssh -fNL 172.18.10.62:10022:192.168.0.15:22 root@12.73.6.108 -p 32222
# 省略信息 ......
root@12.73.6.108's password: # 输入远程主机SSH密码


## 查看是否成功
[root@centos-01 (11:56:57) ~]
└─# ps -ef | grep 'ssh -fNL'
root       493     1  0 14:39 ?        00:00:00 ssh -fNL 172.18.10.62:10022:192.168.0.15:22 root@12.73.6.108 -p 32222

```

```shell
## 测试内网端口转发是否成功
[root@centos-01 (11:59:57) ~]
└─# ssh 172.18.10.62 -p 10022
# 省略信息 ......
root@172.18.10.62's password: # 输入远程主机SSH密码
# 省略信息 ......
[root@k8s-master ~]# ip a show ens192 | grep inet | awk '{print $2}'
192.168.0.15/24

```

* * *

* * *

### 47\. 获得当前操作系统架构类型

```shell
## 代码解释
## case $(uname -m) in
##     x86_64)
##         echo -n amd64
##         ;;
##     aarch64)
##         echo -n arm64
##         ;;
##     *)
##         echo -n $(uname -m)
##         ;;
## esac
export ARCH=$(case $(uname -m) in x86_64) echo -n amd64 ;; aarch64) echo -n arm64 ;; *) echo -n $(uname -m) ;; esac)
export OS=$(uname | awk '{print tolower($0)}')

```

* * *

* * *

### 46\. Linux make命令入门

- **make**
    
    > - 制作、创造、构建
    > - 在Linux中用来将shell脚本进行打包，并按需执行
    
- **Makefile**
    
    > - 构建脚本时使用的清单文件
    
- **案例**
    
- ```makefile
    cat > Makefile << ERIC
    TEMP='定义一个变量'
    
    # 注意事项:
    #     编写指令时，前面的空行必须是 【制表符】Tab
    #     在指令前使用@符号，在指令执行的过程中，不会输出执行的指令
    #       或者执行指令时加上 -s 参数  【make -s】
    
    
    # 第一个标签可以不用指定，默认执行 make -s 就会执行第一个标签
    stpe_main: step_1 step_2 step_3
    
    # 可以使用 make step_1 单独执行这一组指令
    step_1:
          @echo "hello world!" > file.log
          @cat file.log
    
    step_2:
          echo "开始编写第2类脚本"
          uname -r
    
    step_3:
          echo ${TEMP}
    
    # 如果执行 make -s step_all 会按照配置顺序执行指令
    step_all: step_3 step_2 step_1
    
    ERIC
    
    ```
    

* * *

* * *

### 45\. Linux 创建指纹

```shell
## 创建测试文件
[root@eric-mao (18:04:15) ~]# echo '123456' > test.log

## 给测试文件，添加指纹 【注：指纹文件，必须要和原文件在同一个目录中】
[root@eric-mao (18:05:34) ~]# md5sum test.log > test-md5

## 使用指纹，验证测试文件
[root@eric-mao (18:09:55) ~]# md5sum -c test-md5
test.log: OK

## 修改测试文件
[root@eric-mao (18:10:27) ~]# echo 'abcde123456' > test.log

## 再次使用指纹，验证测试文件
[root@eric-mao (18:10:33) ~]# md5sum -c test-md5
test.log: 失败
md5sum: 警告：1 个校验和不匹配

```

* * *

* * *

### 44\. 批量替换文件内容

1. 第一个`^`表示`行首位置`，`[^#]`表示`非#号`，合起来就表示**要匹配`不以#号`开头的行**。
2. 后面用`&`来引用前面匹配到的行内容，**并在其前面加上`#号`**。

```shell
sed -i 's/^[^#]/#&/' /usr/lib/systemd/system/ctrl-alt-del.target
```

* * *

* * *

### 43\. **防止程序退出，通常用于容器中运行程序时测试使用**

```ruby
cat > docker-entrypoint.sh << ERIC
#!/bin/bash

tail -f /dev/null

ERIC

```

* * *

* * *

### 42\. **route** net-tools中的路由命令

> - 从网络的角度出发，每个主机都必须要有一个自己的**网卡**，它的作用是主机与外界通信的**唯一出入口**，网卡的信息会在路由表中以 **`接口`** 的形式展示。
> - 我们每次发送的网络请求都会通过这个 **`网卡接口`** ，那么在系统中是如何使用这个 **`网卡接口`** 的？
> - 系统中有一个 **`路由表`** ，通过如下命令 **`route`** 可以查看。

```ruby
[root@master01 ~]# route
Kernel IP routing table
Destination     Gateway          Genmask         Flags   Metric   Ref    Use   Iface
default         gateway          0.0.0.0         UG      100      0        0   ens192

## 以ip的方式查看数据
[root@master01 ~]# route -n
Kernel IP routing table
Destination     Gateway          Genmask         Flags   Metric   Ref    Use   Iface
0.0.0.0         132.116.15.64    0.0.0.0         UG      100      0        0   ens192

```

> - 路由表里面初始的默认数据，这里先关注3个属性：
>     
>     | **Destination**  
>     **`目标IP`** | **Gateway**  
>     **`网关`**  
>     你要去的 **`目标IP`** 由哪个网关进行**解析、转发** | **Iface**  
>     当前主机中的 **`网卡接口`** |
>     | :-: | :-: | :-: |
>     | 0.0.0.0  
>     表示任意目标IP | 132.116.15.64 | ens192 |
>     

* * *

> - 例如：`ping 187.65.43.2`
> 
> 1. 先从路由表中查看**Destination**中是否有相匹配的IP，如果没有匹配就会找到 **default**，也就是**0.0.0.0**
> 2. 然后找到**0.0.0.0**所对应的网卡**Iface**，也就是**ens192**，我们的请求将从这个网卡出去
> 3. 根据**ens192**对应的网关**Gateway**，也就是**132.116.15.64**，请求出去后会找到这个网关进行**解析、转发**

* * *

### 路由表的信息是人为的

路由表的作用就是，我要到达的 **目标IP** 在离开主机以后，由谁来告诉我怎么走。

```ruby
[root@master01 ~]# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags   Metric   Ref    Use   Iface
0.0.0.0         172.16.15.64    0.0.0.0         UG      100      0        0   ens192
172.16.15.0     0.0.0.0         255.255.255.0   U       100      0        0   ens192   # 目标IP是由某些程序自动添加，它会优先于0.0.0.0匹配
172.17.0.0      0.0.0.0         255.255.0.0     U       0        0        0   docker0  # 目标IP是由某些程序自动添加，它会优先于0.0.0.0匹配

```

* * *

* * *

### 41\. **echo** 常用命令

```ruby
str=maosiyu

## 输入字符串长度
echo ${#str}
7

```

* * *

* * *

### 40\. **while** 循环

```ruby
while :; do sleep 3s; curl -sSk 10.96.173.102:8080/test; done

```

* * *

* * *

### 39\. **id** 查看当前用户

```ruby
/ $ id -un
consul

/ $ id
uid=100(consul) gid=1000(consul) groups=1000(consul)

```

* * *

* * *

### 38\. **alternatives** 切换版本

| 常用命令 | 作用 | 用法 |
| --- | --- | --- |
| **install** | 生成软连接 | `alternatives --install <链接> <名称> <路径> <优先度>` |
| **remove** | 删除软连接 | `alternatives --remove <名称> <路径>` |
| **config** | 选择软连接 | `alternatives --config <名称>` |
| **display** | 显示软连接 | `alternatives --display <名称>` |
| **list** | 显示所有软连接 | `alternatives --list` |

```ruby
## 添加 java
sudo alternatives --install /usr/bin/java java /home/gitlab-runner/deploy/jdk181/jdk1.8.0_181/bin/java 0
sudo alternatives --install /usr/bin/java java /home/gitlab-runner/deploy/jdk11/jdk-11.0.12/bin/java 1

## 查看 java
sudo alternatives --config java
  Selection    Command
-----------------------------------------------
*+ 1           /home/gitlab-runner/deploy/jdk181/jdk1.8.0_181/bin/java
   2           /home/gitlab-runner/deploy/jdk11/jdk-11.0.12/bin/java


## 选择 java8
echo 1 | sudo alternatives --config java
## 选择 java11
echo 2 | sudo alternatives --config java

## 删除 java
sudo alternatives --remove java /home/gitlab-runner/deploy/jdk181/jdk1.8.0_181/bin/java
sudo alternatives --remove java /home/gitlab-runner/deploy/jdk11/jdk-11.0.12/bin/java

```

* * *

* * *

### 37\. **pushd/popd**

```ruby
## 当前所在目录
[gitlab-runner@Gitlab-Runner deploy]$ dirs -v
 0  ~/deploy

## 向栈顶压入一个目录
[gitlab-runner@Gitlab-Runner deploy]$ pushd dist-server/
~/deploy/dist-server ~/deploy

## 在看
[gitlab-runner@Gitlab-Runner dist-server]$ dirs -v
 0  ~/deploy/dist-server
 1  ~/deploy
[gitlab-runner@Gitlab-Runner dist-server]$

## 删除栈顶数据
[gitlab-runner@Gitlab-Runner dist-server]$ popd
~/deploy

## 查看
[gitlab-runner@Gitlab-Runner deploy]$  dirs -v
 0  ~/deploy

```

* * *

* * *

### 36\. 当前都有谁在登录 `w` 或者 `who` 系统内置命令

```ruby
[root@shared-server ~]# w
 20:44:49 up 335 days,  6:38,  2 users,  load average: 0.07, 0.05, 0.05
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
mao_siyu pts/0    60.20.143.175    20:39    2:09   0.15s  0.08s -zsh
root     pts/1    60.20.143.175    20:26    1.00s  0.02s  0.00s w
[root@shared-server ~]#
[root@shared-server ~]# who
root     pts/0        2019-08-28 14:48 (124.93.194.249)
[root@shared-server ~]#
```

* * *

* * *

### 35\. `whois` IP地址 查看IP信息， 三方工具

```ruby
[root@shared-server ~]# yum install -y whois
[root@shared-server ~]#
[root@shared-server ~]# whois 220.181.38.150
```

* * *

* * *

### 34\. 谁曾经登录过 `last` 系统内置命令

```ruby
# 只查看包含 root reboot 用户的最近 6 行
[root@test1 ~]# last root reboot -n 6
用户     tty设备号                      登录时间            离开时间       持续时间(小时:分钟)
root     pts/7        111.93.191.200   Wed May 13 09:43 - 09:59          (00:15)
                                                          (正在使用)
root     pts/3        111.93.191.200   Wed May 13 09:23   still          logged in
root     pts/2        111.93.191.200   Wed May 13 09:21 - 11:09          (01:47)
root     pts/0        111.93.191.200   Wed May 13 09:21 - 11:09          (01:47)
root     pts/1        111.93.191.200   Wed May 13 09:19 - 11:09          (01:50)
reboot   system boot  4.16.13-1.el7.el Wed May 13 00:54 - 11:29          (10:35)
root     pts/3        111.93.191.200   Sat May  9 09:44 - 09:53          (00:08)
root     pts/1        111.93.191.200   Thu Apr 23 00:50 - 00:50          (1+07:40)
root     pts/4        111.93.191.200   Wed Apr 22 10:13 - 10:26          (4+19:55)
                                                          (崩溃)
root     pts/4        111.93.191.200   Tue Apr 21 16:20 - crash          (7+00:48)

[root@test1 ~]#

```

* * *

* * *

### 33\. uptime

```ruby
[root@test1 ~]# uptime
 当前系统时间  系统运行时间               已登录用户数        系统的负载
              (4天,20小时:38分)                             分别代表着      4%,     31%,    32%
                                                           分别代过去    1分钟,   5分钟,  15分钟  系统的平均负载量
 11:39:39     up 4 days, 20:38,         2 users,           load average: 0.04,   0.31,    0.32
[root@test1 ~]#

```

* * *

* * *

### 32\. 检查所有的系统进程 `ps` 系统内置命令

```ruby
[root@shared-server ~]# ps auxf
# 查看进程的线程数
[root@shared-server ~]# ps -T -p <pid> | wc -l
```

* * *

* * *

### 31\. 踢出用户 `fuser -k /dev/pts/用户编号`

```ruby
# 查看登录的用户
[root@shared-server ~]# w
 20:44:49 up 335 days,  6:38,  2 users,  load average: 0.07, 0.05, 0.05
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
mao_siyu pts/0    60.20.143.175    20:39    2:09   0.15s  0.08s -zsh
root     pts/1    60.20.143.175    20:26    1.00s  0.02s  0.00s w

# 踢出用户
[root@shared-server ~]# fuser -k /dev/pts/1

# 给用户发信息
[root@shared-server ~]# echo "你好我是管理员" > /dev/pts/1

# 发信息再关闭
[root@shared-server ~]# echo "你被管理员踢出了" > /dev/pts/1 && fuser -k /dev/pts/1
```

* * *

* * *

### 30\. watch

`watch指令可以间歇性的执行程序，将输出结果以全屏的方式显示，默认是2s执行一次。watch将一直运行，直到被中断。`

```ruby
[root@dev11 ~]# watch free -h
Every 2.0s: free -h                                                                                                                                             Tue Sep 24 16:31:58 2019

              total        used        free      shared  buff/cache   available
Mem:            62G         47G         14G        9.2M        657M         18G
Swap:            0B          0B          0B
```

* * *

* * *

### 29\. 清空操作系统缓存

手动释放内存的命令 先sync一下防止数据丢失（如果必须停止系统，则运行 sync 命令以确保文件系统的完整性。sync 命令将所有未写的系统缓冲区写到磁盘中，包含已修改的 i-node、已延迟的块 I/O 和读写映射文件)） `drop_caches` 的值可以是0-3之间的数字，代表不同的含义： 0：不释放（系统默认值） 1：释放页缓存 2：释放dentries和inodes 3：释放所有缓存

```ruby
[root@dev11 ~]# echo 3 > /proc/sys/vm/drop_caches
```

* * *

* * *

### 28\. 查看文件占用磁盘的空间，并排序; 查询大文件

```ruby
# 查看占用空间大小
[root@shared-server ~]# du -m
# 查看占用空间大小 并 排序倒序
[root@shared-server ~]# du -ah | sort -nr
# 查看占用空间大小 并倒排序 并选出前10
[root@shared-server ~]# du -ah | sort -nr | head
# 例如：查看docker占用空间大小 并倒排序 并选出前 10
[root@shared-server ~]# du -ah /var/lib/docker/* | sort -nr | head -10
# 按照文件大小 排序当前目录下所有文件 选出前 5
[root@shared-server ~]# ll -hS | head -n 5
```

* * *

* * *

### 27\. 过滤筛选

`执行的命令 | grep 要过滤的关键字 | awk '{print $要筛选的列(默认按空格拆分)}'`

```ruby
[root@dev4 ~]# docker ps | grep storage
3e732e2563fb        luhuiguo/fastdfs    "/usr/bin/start.sh s…"   8 months ago        Up 20 hours                             storage2
06e1671727c9        luhuiguo/fastdfs    "/usr/bin/start.sh s…"   8 months ago        Up 20 hours                             storage0
[root@dev4 ~]# docker ps | grep storage | awk '{print $11}'
storage2
storage0
[root@dev4 ~]#
[root@dev4 ~]#
[root@dev4 ~]# ls /var/lib/ceph/ | grep -v bootstrap-*
[root@dev4 ~]#
# 删除 /var/lib/ceph/ 目录下所有不包含 bootstrap- 的文件与文件夹
[root@dev4 ~]# ls /var/lib/ceph/ | grep -v bootstrap-* | awk '{print "/var/lib/ceph/"$0}' | xargs rm -rf
[root@dev4 ~]#

# 同时排除多个关键字
kubectl get pods --all-namespaces -o wide | grep -v 'Running\|Completed'
```

* * *

* * *

### 26\. 查看系统邮件

```ruby
[tidb@dev10 bin]$ tail -10 /var/spool/mail/tidb
......
```

* * *

* * *

### 25\. DD 添加swap交换文件

**`sysctl vm.swappiness=60`解释：**   `是Linux/UNIX系统下的一个非常有用的命令，作用是用指定大小的块拷贝一个文件，并在拷贝的同时进行指定的转换。`   调整swap空间使用的优先级如果内存够大，应当告诉 linux 不必太多的使用 SWAP 分区， 可以通过修改 `swappiness` 的数值。   `swappiness=0`的时候`表示最大限度使用物理内存`，`然后才是swap空间`   `swappiness＝100`的时候表示`积极的使用swap分区`，并且`把内存`上的`数据`及时的`搬运到swap空间`里面。

```
dd if=/dev/zero 创建空文件
of=/swapfile    文件名
bs=1024M        单个块的大小
count=32        多少个块
```

```ruby
# 创建文件夹
[tidb@dev10 swap]$ mkdir /home/swap/
# 创建一个 32G的 /home/swap/swapfile文件
[tidb@dev10 swap]$ dd if=/dev/zero of=/home/swap/swapfile bs=1024M count=32
# 磁盘写性能
记录了32+0 的读入
记录了32+0 的写出
34359738368字节(34 GB)已复制，42.7829 秒，803 MB/秒
[tidb@dev10 swap]$

# 启用交换文件
[tidb@dev10 swap]$ chmod 600 /home/swap/swapfile

# 设置交换空间
[tidb@dev10 swap]$ mkswap /home/swap/swapfile
正在设置交换空间版本 1，大小 = 33554428 KiB
无标签，UUID=8ed63b08-4722-43d9-be17-c1760fadc143
[tidb@dev10 swap]$

# 查看空间
[tidb@dev10 swap]$ free -h
              total        used        free      shared  buff/cache   available
Mem:            31G        1.4G         24G         32M        5.9G         29G
Swap:            0B          0B          0B
[tidb@dev10 swap]$

# 启用交换空间
[tidb@dev10 swap]$ swapon /home/swap/swapfile

# 在次查看空间
[tidb@dev10 swap]$ free -h
              total        used        free      shared  buff/cache   available
Mem:            31G        264M         25G         32M        5.8G         30G
Swap:           31G          0B         31G
[tidb@dev10 swap]$

# 设置物理内存剩余百分比(即时生效，重启失效)，如下为物理内存剩余10%时，开始交换
[tidb@dev10 swap]$ sysctl vm.swappiness=10

# 设置优先级(永久生效，需要重启)
[tidb@dev10 swap]$ sed -i "s/vm.swappiness=0/vm.swappiness=10/g" /etc/sysctl.conf


####################################################################


[tidb@dev10 swap]$ dd if=/home/swap/swapfile  of=/dev/null
# 磁盘读性能
记录了67108864+0 的读入
记录了67108864+0 的写出
34359738368字节(34 GB)已复制，51.4949 秒，667 MB/秒
[tidb@dev10 swap]$
```

**执行所有脚本**

```ruby
mkdir -p /home/swap && \
dd if=/dev/zero of=/home/swap/swapfile bs=1024M count=32 && \
chmod 600 /home/swap/swapfile && \
mkswap /home/swap/swapfile && \
swapon /home/swap/swapfile && \
sysctl vm.swappiness=10 && \
sed -i "s/vm.swappiness=0/vm.swappiness=10/g" /etc/sysctl.conf && \
cat /etc/sysctl.conf
```

* * *

#### 永久关闭 swap, 缺点是在同一个主机中其它的程序也无法使用swap进行交换

```ruby
swapoff -a && sed -ri 's/.*swap.*/#&/' /etc/fstab
```

* * *

* * *

### 24\. wget 重命名

`wget -O /新路径/新文件名 下载地址` **下载文件 到指定目录** `wget -P 指定目录 下载地址`

```ruby
[elasticsearch@test1 download]$ wget -O /home/download/HanLP.zip https://github.com/hankcs/HanLP/archive/master.zip
[elasticsearch@test1 download]$ wget -P /home/download/ https://github.com/hankcs/HanLP/archive/master.zip
```

**wget 将结果输出到终端** **`wget -O -`URL** **\-q**: quiet模式，屏蔽request header信息的回显 **\-O**: 指定输出文件，后面加 **`-`** ，就定向为 **`console`** 了 **\--proxy**: 指定代理服务器地址

```ruby
kubectl exec busybox -- wget -qO - test-headless-server
```

* * *

* * *

### 23\. curl 下载

`curl -o 新名称 下载地址` [参考-curl 的用法指南](https://www.ruanyifeng.com/blog/2019/09/curl-reference.html)

```shell
-A/--user-agent <string>          设置用户代理发送给服务器
-b/--cookie <name=string/file>    cookie字符串或文件读取位置
-c/--cookie-jar <file>            操作结束后把cookie写入到这个文件中
-C/--continue-at <offset>         断点续转
-D/--dump-header <file>           把header信息写入到该文件中
-e/--referer                      来源网址
-f/--fail                         连接失败时不显示http错误
-o/--output                       把输出写到该文件中
-O/--remote-name                  把输出写到该文件中，保留远程文件的文件名
-r/--range <range>                检索来自HTTP/1.1或FTP服务器字节范围
-s/--silent                       静音模式。不输出任何东西
-T/--upload-file <file>           上传文件
-u/--user <user[:password]>       设置服务器的用户和密码
-w/--write-out [format]           什么输出完成后
-x/--proxy <host[:port]>          在给定的端口上使用HTTP代理
-#/--progress-bar                 进度条显示当前的传送状态
```

```ruby
[elasticsearch@test1 download]$  curl -o a.yml https://raw.githubusercontent.com/coreos/flannel/v0.11.0/Documentation/kube-flannel.yml
```

**只查看HTTP状态码** **\-x**: 指定代理服务器地址

```shell
#!/bin/sh

# -I 仅测试HTTP头
# -o /dev/null 屏蔽原有输出信息
# -s silent 模式，不输出任何东西
# -w %{http_code} 控制额外输出

curl -o /dev/null -s -w %{http_code} www.baidu.com
```

* * *

* * *

### 22\. tar 解压到指定目录下

`tar -zxvf tar包 -C 目录`

```ruby
[elasticsearch@test1 deploy]$ tar -zxvf elasticsearch-7.3.2-linux-x86_64.tar.gz -C /home/elasticsearch/deploy
```

* * *

* * *

### 21\. grep 命令用于查找文件里符合条件的字符串

`grep -i '字符串' 文件路径` `多条件过滤 grep -E "条件1|条件2|......"` `排除 grep -v '排除的关键字'` `同时排除多个关键字 grep -v '排除的关键字01\|排除的关键字02'`

```ruby
# 查看文件中包含 oom_kill 的字符串
[root@dev10 ~]# grep -i 'oom_kill' /var/log/messages

# 查看指定路径下，所有包含 oom_kill 文件中的字符串
[root@dev10 ~]# grep -i 'oom_kill' /var/log/*

# 搜索目录里所有文件，包括子目录，并且在结果中显示行号
## r 所有目录  n 显示行号
[root@dev10 ~]# grep -rn 查看内容 ./
```

* * *

* * *

### 20\. 显示/设置用户可以使用的资源的限制

`ulimit [参数] [值|无限制(unlimited)]`

```ruby
# 此命令用来处理如下问题的
-bash: fork: retry: 没有子进程
-bash: fork: retry: 没有子进程
-bash: fork: retry: 没有子进程
-bash: fork: retry: 资源暂时不可用
```

```ruby
[root@dev10 ~]# ulimit -a
core file size          (blocks, -c) 0
data seg size           (kbytes, -d) unlimited
scheduling priority             (-e) 0
file size               (blocks, -f) unlimited
pending signals                 (-i) 128527
max locked memory       (kbytes, -l) 64
max memory size         (kbytes, -m) unlimited
open files                      (-n) 655360
pipe size            (512 bytes, -p) 8
POSIX message queues     (bytes, -q) 819200
real-time priority              (-r) 0
stack size              (kbytes, -s) 8192
cpu time               (seconds, -t) unlimited
max user processes              (-u) 128527
virtual memory          (kbytes, -v) unlimited
file locks                      (-x) unlimited
[root@dev10 ~]#
[root@dev10 ~]#

# 例如设置 max user processes
[root@dev10 ~]# ulimit -u 10000

# 修改打开文件最大数量, 即时生效，重启失效
[root@dev10 ~]# ulimit -n 102400
# 修改打开文件最大数量, 重启生效
[root@dev10 ~]# echo "* soft nofile 102400" >> /etc/security/limits.conf
[root@dev10 ~]# echo "* hard nofile 102400" >> /etc/security/limits.conf
# 查看是否修改成功
[root@dev10 ~]# cat /etc/security/limits.conf

```

* * *

* * *

### 19\. sysctl

`sysctl`命令用于运行时配置内核参数

```ruby
# 手动配置
vim /etc/sysctl.conf
```

```ruby
# 通过命令来配置
sysctl -w variable=value
# 使配置生效
sysctl -p
# 查看所有配置
sysctl -a
```

* * *

* * *

### 18\. scp

1 从本地复制到远程 复制本地文件 到 远程某个文件夹下 `scp local_file remote_username@remote_ip:remote_folder`

```ruby
[root@dev10 ~]# scp 2019-11-21.log root@172.160.180.3:/home/
```

复制本地文件夹 到 远程某个文件夹下 `scp -r local_folder remote_username@remote_ip:remote_folder`

```ruby
[root@dev10 ~]# scp src/ root@172.160.180.3:/home/src/
```

2 从远程复制到本地 `scp remote_username@remote_ip:remote_file local_file`

```ruby
[root@dev10 ~]# scp root@172.160.180.3:/home/2019-11-21.log 2019-11-21.log
```

* * *

* * *

### 17\. date

```ruby
# 查看系统当前时间
[root@dev10 ~]# date
# 设置系统当前时间
[root@dev10 ~]# date -s '2019-11-06 11:06:16'
```

* * *

* * *

### 16\. timedatectl

```ruby
01.查看当前时间/日期/时区
[root@aliyun ~]# timedatectl
Warning: Ignoring the TZ variable. Reading the system's time zone setting only.

      Local time: Fri 2019-12-13 10:45:45 CST
  Universal time: Fri 2019-12-13 02:45:45 UTC
        RTC time: Fri 2019-12-13 02:45:45
       Time zone: Asia/Shanghai (CST, +0800)
     NTP enabled: yes
NTP synchronized: yes
 RTC in local TZ: no
      DST active: n/a
[root@aliyun ~]#
```

```ruby
02.查看所有可用时区
timedatectl list-timezones
```

```ruby
03.设置时区 为上海
timedatectl set-timezone "Asia/Shanghai"
```

```ruby
04.设置时间
timedatectl set-time HH:MM:SS
```

```ruby
05.设置日期
timedatectl set-time YYYY-MM-DD
```

```ruby
06.设置日期时间
timedatectl set-time "YYYY-MM-DD HH:MM:SS"
```

```ruby
07.设置硬件时钟为本地时间
timedatectl set-local-rtc 1
```

```ruby
08.设置硬件时钟为UTC时间
timedatectl set-local-rtc 0
```

```ruby
09.启动NTP时间同步校准
timedatectl set-ntp true
```

```ruby
10.禁用NTP时间同步校准(使用 date -s 命令会自动触发这个命令)
timedatectl set-ntp false
```

* * *

* * *

### 15\. ln 链接命令（link）

`Linux ln命令是一个非常重要命令，它的功能是为某一个文件在另外一个位置建立一个同步的链接。 当我们需要在不同的目录，用到相同的文件时，我们不需要在每一个需要的目录下都放一个必须相同的文件，我们只要在某个固定的目录，放上该文件，然后在 其它的目录下用ln命令链接（link）它就可以，不必重复的占用磁盘空间。`

**软链接：**

1. 软链接，以路径的形式存在。类似于Windows操作系统中的快捷方式
2. 软链接可以 跨文件系统 ，硬链接不可以
3. 软链接可以对一个不存在的文件名进行链接
4. 软链接可以对目录进行链接

**硬链接：**

1. 硬链接，以文件副本的形式存在。但不占用实际空间。
2. 不允许给目录创建硬链接
3. 硬链接只有在同一个文件系统中才能创建

**常用参数：**

**\-b** 删除，覆盖以前建立的链接 **\-f** 强制执行 **\-i** 交互模式，文件存在则提示用户是否覆盖 **\-s** 软链接(符号链接) **\-v** 显示详细的处理过程

[菜鸟详解](https://www.runoob.com/linux/linux-comm-ln.html "菜鸟详解")

* * *

* * *

### 14\. lsblk

- **lsblk** 查看的是`block device`,也就是逻辑磁盘大小。

```ruby
[root@test1 ~]# lsblk
NAME            MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sdb               8:16   0  120G  0 disk # disk 表示磁盘
├─sdb2            8:18   0  115G  0 part /home
└─sdb1            8:17   0    5G  0 part # part 表示主分区
sr0              11:0    1 1024M  0 rom
fd0               2:0    1    4K  0 disk
sda               8:0    0   80G  0 disk
├─sda2            8:2    0   70G  0 part
│ ├─centos-swap 253:1    0    8G  0 lvm # lvm 逻辑卷 LV
│ ├─centos-home 253:2    0    5G  0 lvm
│ └─centos-root 253:0    0   57G  0 lvm  /
└─sda1            8:1    0   10G  0 part /boot
[root@test1 ~]#

# 查看更多的内容
[tidb@test1 ~]$ lsblk -fm
NAME            FSTYPE      LABEL UUID                                   MOUNTPOINT NAME             SIZE OWNER GROUP MODE
sdb                                                                                 sdb              120G root  disk  brw-rw----
├─sdb2          ext4              d04ed152-9505-4852-a3a4-92dedccdcd1f   /home      ├─sdb2           115G root  disk  brw-rw----
└─sdb1          xfs               00df76fa-86a4-43b3-a6be-4f20216ea6c9              └─sdb1             5G root  disk  brw-rw----
sr0                                                                                 sr0             1024M root  cdrom brw-rw----
fd0                                                                                 fd0                4K root  disk  brw-rw----
sda                                                                                 sda               80G root  disk  brw-rw----
├─sda2          LVM2_member       miDtM6-xhfw-cAKd-tcZL-3mPa-ShfJ-NeuHoS            ├─sda2            70G root  disk  brw-rw----
│ ├─centos-swap swap              5df5770f-ebe4-4d0f-88b5-3032f8c05cb1              │ ├─centos-swap    8G root  disk  brw-rw----
│ ├─centos-home xfs               1335a6ec-9993-4f90-b0e7-607138c4d6e0              │ ├─centos-home    5G root  disk  brw-rw----
│ └─centos-root xfs               bf264188-ae9c-40f5-bb5b-722a8e2e05db   /          │ └─centos-root   57G root  disk  brw-rw----
└─sda1          xfs               ddd0be93-ca35-4ce1-b320-e2c5ac06e62d   /boot      └─sda1            10G root  disk  brw-rw----
[tidb@test1 ~]$
```

* * *

* * *

### 13\. df

- **df** 查看的是`file system`, 也就是文件系统层的磁盘大小。

```ruby
[root@test1 ~]# df -h
文件系统                 容量  已用  可用 已用% 挂载点
devtmpfs                 7.9G     0  7.9G    0% /dev
tmpfs                    7.9G     0  7.9G    0% /dev/shm
tmpfs                    7.9G  9.9M  7.9G    1% /run
tmpfs                    7.9G     0  7.9G    0% /sys/fs/cgroup
/dev/mapper/centos-root   57G  6.0G   51G   11% /
/dev/sdb2                114G   61M  108G    1% /home
/dev/sda1                 10G  221M  9.8G    3% /boot
[root@test1 ~]#
```

* * *

* * *

### 12\. swapon

**查看 swap 是否开启**

- NAME 设备文件或分区路径
- TYPE 设备的类型
- SIZE 交换区大小
- USED 已使用字节数
- PRIO 交换优先级

`swapon` 或 `cat /proc/swaps`

```ruby
[root@dev1 ~]# swapon
NAME      TYPE      SIZE   USED PRIO
/dev/dm-1 partition  20G 154.8M   -2
[root@dev1 ~]#
```

**关闭 swap**

```ruby
[root@dev1 ~]# swapoff -a
```

* * *

* * *

### 11\. 查看当前操作系统版本

```ruby
[root@dev1 deploy]# cat /etc/redhat-release
CentOS Linux release 7.6.1810 (Core)
[root@dev1 deploy]#
```

* * *

* * *

### 10\. 修改文件夹所属用户、所属权限

**[参考资料](https://www.runoob.com/linux/linux-comm-chown.html "参考资料")** `-R` : 处理指定目录以及其子目录下的所有文件 `chown -R 用户名 文件夹`

```ruby
# 修改文件夹所属用户
[root@dev1 deploy]# chown -R elasticsearch download/
```

`chgrp -R 用户名 文件夹`

```ruby
# 修改文件夹所属组
[root@dev1 deploy]# chgrp -R elasticsearch download/
```

* * *

* * *

### 9\. 压缩、解压 gz文件

```ruby
# 批量sql文件
gzip *.sql

# 批量解压gz文件
gunzip *.gz
```

* * *

> 经过实际检验，在Linux操作系统当中，对大文件进行`分卷压缩`时，只有`7z`能够`支持的最好`，在解压时不丢文件，`unzip`会丢失很多的文件 **安装 7z**

```bash
yum install epel-release

yum install p7zip p7zip-plugins

```

**执行分卷压缩**

```bash
7z a -v3g -sfx filename.7z file_dir/
```

> `7z a`：添加文件到7z压缩包。 `-v3g`：每个分卷最大3GB。 `-sfx`：创建自解压格式的压缩文件。 `filename.7z`：输出文件名。 `file_dir/`：要压缩的目录。

* * *

**加密、分卷压缩**

```bash
# 加密、分卷压缩
[root@localhost ~]# 7z a -p'123456' -v500k -sfx filename.7z 7z_rpm/

7-Zip [64] 16.02 : Copyright (c) 1999-2016 Igor Pavlov : 2016-05-21
p7zip Version 16.02 (locale=en_US.UTF-8,Utf16=on,HugeFiles=on,64 bits,8 CPUs Intel(R) Xeon(R) Gold 6342 CPU @ 2.80GHz (606A6),ASM,AES-NI)

Scanning the drive:
1 folder, 2 files, 1611478 bytes (1574 KiB)

Creating archive: filename.7z

Items to compress: 3

Write SFX: /usr/libexec/p7zip/7zCon.sfx : 408728 bytes (400 KiB)

Files read from disk: 2
Archive size: 1589054 bytes (1552 KiB)
Everything is Ok

# 查看
[root@localhost ~]# ll -h
total 2.0M
drwxr-xr-x 2 root root   88 May 14 10:33 7z_rpm
-rwx------ 1 root root 400K May 14 10:38 filename.7z
-rw-r--r-- 1 root root 500K May 14 10:38 filename.7z.001
-rw-r--r-- 1 root root 500K May 14 10:38 filename.7z.002
-rw-r--r-- 1 root root 500K May 14 10:38 filename.7z.003
-rw-r--r-- 1 root root  52K May 14 10:38 filename.7z.004

```

**解密**

```bash
[root@localhost ~]# 7z x -p'123456' filename.7z.001

7-Zip [64] 16.02 : Copyright (c) 1999-2016 Igor Pavlov : 2016-05-21
p7zip Version 16.02 (locale=en_US.UTF-8,Utf16=on,HugeFiles=on,64 bits,8 CPUs Intel(R) Xeon(R) Gold 6342 CPU @ 2.80GHz (606A6),ASM,AES-NI)

Scanning the drive for archives:
1 file, 512000 bytes (500 KiB)

Extracting archive: filename.7z.001
--
Path = filename.7z.001
Type = Split
Physical Size = 512000
Volumes = 4
Total Physical Size = 1589054
----
Path = filename.7z
Size = 1589054
--
Path = filename.7z
Type = 7z
Physical Size = 1589054
Headers Size = 254
Method = LZMA2:21 7zAES
Solid = +
Blocks = 1

Everything is Ok

Folders: 1
Files: 2
Size:       1611478
Compressed: 1589054


# 查看
[root@localhost ~]# ll -h 7z_rpm
total 1.6M
-rw-r--r-- 1 root root 605K Apr 23  2021 p7zip-16.02-20.el7.x86_64.rpm
-rw-r--r-- 1 root root 969K Apr 23  2021 p7zip-plugins-16.02-20.el7.x86_64.rpm
[root@localhost ~]#

```

* * *

* * *

### 8\. init 级别

init 0:关机 init 1:单用户模式 init 3:完全多用户模式，标准的运行级 init 5:启动可进入X-window系统 init 6:重启

* * *

* * *

### 7\. lscpu 查看cpu参数

```ruby
[root@test1 ~]# lscpu
Architecture:          x86_64
CPU op-mode(s):        32-bit, 64-bit
Byte Order:            Little Endian
CPU(s):                4
On-line CPU(s) list:   0-3
Thread(s) per core:    1
Core(s) per socket:    2
座：                 2
NUMA 节点：         1
厂商 ID：           GenuineIntel
CPU 系列：          6
型号：              79
型号名称：        Intel(R) Xeon(R) CPU E5-2650 v4 @ 2.20GHz
步进：              1
CPU MHz：             2194.917
BogoMIPS：            4389.83
超管理器厂商：  VMware
虚拟化类型：     完全
L1d 缓存：          32K
L1i 缓存：          32K
L2 缓存：           256K
L3 缓存：           30720K
NUMA 节点0 CPU：    0-3
Flags:                 fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts nopl xtopology tsc_reliable nonstop_tsc cpuid pni pclmulqdq ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand hypervisor lahf_lm abm 3dnowprefetch cpuid_fault invpcid_single pti fsgsbase tsc_adjust bmi1 hle avx2 smep bmi2 invpcid rtm rdseed adx smap xsaveopt arat
[root@test1 ~]#
```

* * *

* * *

### 6\. envsubst 将环境变量传递给文件

```ruby
# 添加全局环境变量 ERIC
[root@master ~]# export ERIC=maosiyu
# 查看
[root@master ~]# echo ${ERIC}
maosiyu
[root@master ~]#

# 创建测试文件
[root@master ~]# cat > test.txt << EOF
hello, \${ERIC}
EOF

# 测试
[root@master ~]# envsubst < test.txt
hello, maosiyu

# 查看文件
[root@master ~]# cat test.txt
hello, ${ERIC}

```

* * *

* * *

### 5\. awk

AWK 是一种处理文本文件的语言，是一个强大的文本分析工具。 **[命令学习](https://www.runoob.com/linux/linux-comm-awk.html "命令学习")**

```ruby
# 拼接结果
awk -F\' '$1=="menuentry " {print "grub2-set-default \"" $2 "\""}' /etc/grub2.cfg
```

* * *

* * *

### 4\. vim 多行注释，批量注释

```ruby
# 1  进行命令行模式
vim shift + :

# 2 显示行号
: set nu

# 3 起始行号,结束行号s/^/注释符/g
## 例如：注释16行 ～ 32行
: 16,32s/^/#/g

# 4 取消16行 ～ 32行的注释
: 16,32s/^#//g

# 5 :%s/原字符串/新字符串/g 替换每一行中所有 hello 为 helloworld
# 参考网址：https://blog.csdn.net/nitweihong/article/details/7221930
:%s/hello/helloworld/g

```

* * *

* * *

### 3\. base64转换

```ruby
[root@master01 ~]# echo Hello,World | base64
SGVsbG8sV29ybGQK
[root@master01 ~]#

[root@master01 ~]# echo SGVsbG8sV29ybGQK | base64 -d
Hello,World
[root@master01 ~]#

```

* * *

* * *

### 2\. diff | vimdiff 比较文件的差异

```ruby
[root@master01 ~]# diff -s a.json b.txt
1c1
< aaa
---
> bbb
[root@master01 ~]#

## 可视化
vimdiff a.json b.txt
```

* * *

* * *

### 1\. mount 挂载硬盘

```ruby
## 将硬盘 /dev/vdb1 挂载到/opt/目录
mount /dev/vdb1 /opt/

## 将硬盘添加到引导文件
blkid | grep vdb1 | awk '{print $2 " /                       ext4    defaults        0 0"}' | sed s/\"//g >> /etc/fstab
```

* * *

* * *
