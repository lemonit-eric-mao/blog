---
title: 'Centos 7 磁盘分区/格式化/挂载'
date: '2018-09-26T05:42:22+00:00'
status: publish
permalink: /2018/09/26/%e9%98%bf%e9%87%8c%e4%ba%91-centos-7-%e6%95%b0%e6%8d%ae%e7%9b%98%e5%ba%94%e7%94%a8%ef%bc%8c-%e5%88%86%e5%8c%ba-%e6%a0%bc%e5%bc%8f%e5%8c%96
author: 毛巳煜
excerpt: ''
type: post
id: 3175
category:
    - CentOS
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### [学习资料](https://www.cnblogs.com/sparkdev/archive/2018/12/11/10095916.html "学习资料")

##### 我要做什么

将 **128G硬盘**，分为两个区，第一个区大小为**10G**，第二个区大小为**118G**

###### 1 查看可用磁盘

```ruby
[root@test1 ~]# fdisk -l

磁盘 /dev/sdb：128.8 GB, 128849018880 字节，251658240 个扇区
Units = 扇区 of 1 * 512 = 512 bytes
扇区大小(逻辑/物理)：512 字节 / 512 字节
I/O 大小(最小/最佳)：512 字节 / 512 字节


磁盘 /dev/sda：85.9 GB, 85899345920 字节，167772160 个扇区
Units = 扇区 of 1 * 512 = 512 bytes
扇区大小(逻辑/物理)：512 字节 / 512 字节
I/O 大小(最小/最佳)：512 字节 / 512 字节
磁盘标签类型：dos
磁盘标识符：0x000c8857

   设备 Boot      Start         End      Blocks   Id  System
/dev/sda1   *        2048    20973567    10485760   83  Linux
/dev/sda2        20973568   167772159    73399296   8e  Linux LVM

```

**一共有两块：**

1. /dev/sda：  
  容量：85.9 GB  
  有两个分区：`/dev/sda1` `/dev/sda2`
2. /dev/sdb：  
   容量：128.8 GB  
   无分区

- - - - - -

###### 2 给 磁盘 /dev/sdb 做分区

`fdisk 磁盘名`

```ruby
[root@test1 ~]# fdisk /dev/sdb
欢迎使用 fdisk (util-linux 2.23.2)。

更改将停留在内存中，直到您决定将更改写入磁盘。
使用写入命令前请三思。

Device does not contain a recognized partition table
使用磁盘标识符 0x37b71e86 创建新的 DOS 磁盘标签。

命令(输入 m 获取帮助)：n
Partition type:
   p   primary (0 primary, 0 extended, 4 free)
   e   extended

Select (default p): p                               # p为主分区

分区号 (1-4，默认 1)：1                              # 1表示第一个分区

起始 扇区 (2048-251658239，默认为 2048)：            # 第一个分区的起始位置
将使用默认值 2048
Last 扇区, +扇区 or +size{K,M,G} (2048-251658239，默认为 251658239)：10485760  # 第一个分区的结束位置
分区 1 已设置为 Linux 类型，大小设为 5 GiB

命令(输入 m 获取帮助)：w                              # 将分区信息写入磁盘
The partition table has been altered!

Calling ioctl() to re-read partition table.
正在同步磁盘。
[root@test1 ~]#

```

###### 查看磁盘信息

```ruby
[root@test1 ~]# fdisk -l

磁盘 /dev/sdb：128.8 GB, 128849018880 字节，251658240 个扇区
Units = 扇区 of 1 * 512 = 512 bytes
扇区大小(逻辑/物理)：512 字节 / 512 字节
I/O 大小(最小/最佳)：512 字节 / 512 字节
磁盘标签类型：dos
磁盘标识符：0x37b71e86

   设备 Boot      Start         End      Blocks   Id  System
/dev/sdb1            2048    10485760     5241856+  83  Linux

磁盘 /dev/sda：85.9 GB, 85899345920 字节，167772160 个扇区
Units = 扇区 of 1 * 512 = 512 bytes
扇区大小(逻辑/物理)：512 字节 / 512 字节
I/O 大小(最小/最佳)：512 字节 / 512 字节
磁盘标签类型：dos
磁盘标识符：0x000c8857

   设备 Boot      Start         End      Blocks   Id  System
/dev/sda1   *        2048    20973567    10485760   83  Linux
/dev/sda2        20973568   167772159    73399296   8e  Linux LVM

[root@test1 ~]#

```

发现 磁盘 `/dev/sdb` 多了一个新的分区 **/dev/sdb1**  
刚才只分了一个5G的分区，接下来把剩余的磁盘空间划分给新的分区

- - - - - -

###### 3 把剩余的磁盘空间划分给新的分区

```ruby
[root@test1 ~]# fdisk /dev/sdb
欢迎使用 fdisk (util-linux 2.23.2)。

更改将停留在内存中，直到您决定将更改写入磁盘。
使用写入命令前请三思。


命令(输入 m 获取帮助)：n
Partition type:
   p   primary (1 primary, 0 extended, 3 free)
   e   extended

Select (default p): p

分区号 (2-4，默认 2)：2

起始 扇区 (10485761-251658239，默认为 10487808)：
将使用默认值 10487808
Last 扇区, +扇区 or +size{K,M,G} (10487808-251658239，默认为 251658239)：
将使用默认值 251658239
分区 2 已设置为 Linux 类型，大小设为 115 GiB

命令(输入 m 获取帮助)：w
The partition table has been altered!

Calling ioctl() to re-read partition table.
正在同步磁盘。
[root@test1 ~]#

```

###### 查看磁盘信息

```ruby
[root@test1 ~]# fdisk -l

磁盘 /dev/sdb：128.8 GB, 128849018880 字节，251658240 个扇区
Units = 扇区 of 1 * 512 = 512 bytes
扇区大小(逻辑/物理)：512 字节 / 512 字节
I/O 大小(最小/最佳)：512 字节 / 512 字节
磁盘标签类型：dos
磁盘标识符：0x37b71e86

   设备 Boot      Start         End      Blocks   Id  System
/dev/sdb1            2048    10485760     5241856+  83  Linux
/dev/sdb2        10487808   251658239   120585216   83  Linux

磁盘 /dev/sda：85.9 GB, 85899345920 字节，167772160 个扇区
Units = 扇区 of 1 * 512 = 512 bytes
扇区大小(逻辑/物理)：512 字节 / 512 字节
I/O 大小(最小/最佳)：512 字节 / 512 字节
磁盘标签类型：dos
磁盘标识符：0x000c8857

   设备 Boot      Start         End      Blocks   Id  System
/dev/sda1   *        2048    20973567    10485760   83  Linux
/dev/sda2        20973568   167772159    73399296   8e  Linux LVM

[root@test1 ~]#

```

发现 磁盘 `/dev/sdb` 现在有两个新的分区 **/dev/sdb1** **/dev/sdb2**

- - - - - -

###### 4 修改磁盘类型

```ruby
[root@test1 ~]# fdisk /dev/sdb
欢迎使用 fdisk (util-linux 2.23.2)。

更改将停留在内存中，直到您决定将更改写入磁盘。
使用写入命令前请三思。

命令(输入 m 获取帮助)：m
命令操作
   a   toggle a bootable flag
   b   edit bsd disklabel
   c   toggle the dos compatibility flag
   d   delete a partition
   g   create a new empty GPT partition table
   G   create an IRIX (SGI) partition table
   l   list known partition types
   m   print this menu
   n   add a new partition
   o   create a new empty DOS partition table
   p   print the partition table
   q   quit without saving changes
   s   create a new empty Sun disklabel
   t   change a partition's system id
   u   change display/entry units
   v   verify the partition table
   w   write table to disk and exit
   x   extra functionality (experts only)

命令(输入 m 获取帮助)：t

分区号 (1,2，默认 2)：1

Hex 代码(输入 L 列出所有代码)：L

 0  空              24  NEC DOS         81  Minix / 旧 Linu bf  Solaris
 1  FAT12           27  隐藏的 NTFS Win 82  Linux 交换 / So c1  DRDOS/sec (FAT-
 2  XENIX root      39  Plan 9          83  Linux           c4  DRDOS/sec (FAT-
 3  XENIX usr       3c  PartitionMagic  84  OS/2 隐藏的 C:  c6  DRDOS/sec (FAT-
 4  FAT16 
```

###### 查看磁盘信息

```ruby
[root@test1 ~]# fdisk -l

磁盘 /dev/sdb：128.8 GB, 128849018880 字节，251658240 个扇区
Units = 扇区 of 1 * 512 = 512 bytes
扇区大小(逻辑/物理)：512 字节 / 512 字节
I/O 大小(最小/最佳)：512 字节 / 512 字节
磁盘标签类型：dos
磁盘标识符：0x37b71e86

   设备 Boot      Start         End      Blocks   Id  System
/dev/sdb1            2048    10485760     5241856+  8e  Linux LVM
/dev/sdb2        10487808   251658239   120585216   83  Linux

磁盘 /dev/sda：85.9 GB, 85899345920 字节，167772160 个扇区
Units = 扇区 of 1 * 512 = 512 bytes
扇区大小(逻辑/物理)：512 字节 / 512 字节
I/O 大小(最小/最佳)：512 字节 / 512 字节
磁盘标签类型：dos
磁盘标识符：0x000c8857

   设备 Boot      Start         End      Blocks   Id  System
/dev/sda1   *        2048    20973567    10485760   83  Linux
/dev/sda2        20973568   167772159    73399296   8e  Linux LVM

[root@test1 ~]#


```

- - - - - -

###### 5 格式化分区

将**/dev/sdb1**分区格式化为 `ext4`  
将**/dev/sdb2**分区格式化为 `ext4`  
mkfs -t xfs -f /dev/sdb1

```ruby
[root@test1 ~]# mkfs.ext4 /dev/sdb1
mke2fs 1.42.9 (28-Dec-2013)
文件系统标签=
OS type: Linux
块大小=4096 (log=2)
分块大小=4096 (log=2)
Stride=0 blocks, Stripe width=0 blocks
327680 inodes, 1310464 blocks
65523 blocks (5.00%) reserved for the super user
第一个数据块=0
Maximum filesystem blocks=1342177280
40 block groups
32768 blocks per group, 32768 fragments per group
8192 inodes per group
Superblock backups stored on blocks:
        32768, 98304, 163840, 229376, 294912, 819200, 884736

Allocating group tables: 完成
正在写入inode表: 完成
Creating journal (32768 blocks): 完成
Writing superblocks and filesystem accounting information: 完成

[root@test1 ~]#
[root@test1 ~]#
[root@test1 ~]#
[root@test1 ~]# mkfs.ext4 /dev/sdb2
mke2fs 1.42.9 (28-Dec-2013)
文件系统标签=
OS type: Linux
块大小=4096 (log=2)
分块大小=4096 (log=2)
Stride=0 blocks, Stripe width=0 blocks
7536640 inodes, 30146304 blocks
1507315 blocks (5.00%) reserved for the super user
第一个数据块=0
Maximum filesystem blocks=2178940928
920 block groups
32768 blocks per group, 32768 fragments per group
8192 inodes per group
Superblock backups stored on blocks:
        32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208,
        4096000, 7962624, 11239424, 20480000, 23887872

Allocating group tables: 完成
正在写入inode表: 完成
Creating journal (32768 blocks): 完成
Writing superblocks and filesystem accounting information: 完成

[root@test1 ~]#

```

###### 查看磁盘信息

```ruby
[root@test1 ~]# lsblk -f | grep sdb
sdb
├─sdb1          ext4              e1dbf51e-25dc-4c0d-bd72-d659257e7d24   /mnt
└─sdb2          ext4              d04ed152-9505-4852-a3a4-92dedccdcd1f   /home
[root@test1 ~]#

```

格式化为 xfs

```
将**/dev/sdb1**分区格式化为 `xfs`
mkfs -t xfs -f /dev/sdb1

将**/dev/sdb2**分区格式化为 `xfs`
mkfs -t xfs -f /dev/sdb2

```

- - - - - -

###### 6 将磁盘分区与挂载目录的信息加入到 系统引导文件

```ruby
[root@test1 ~]# echo '/dev/sdb1 /mnt ext4 defaults 0 0' >> /etc/fstab
[root@test1 ~]# echo '/dev/sdb2 /home ext4 defaults 0 0' >> /etc/fstab

```

- - - - - -

###### 7 挂载分区

```ruby
[root@test1 ~]# mount /dev/sdb1 /mnt
[root@test1 ~]# mount /dev/sdb2 /home

```

- - - - - -

###### 8 查看分区挂载的目录

```ruby
[root@test1 ~]# df -h | grep -E "/dev/sdb1|/dev/sdb2"
/dev/sdb1                4.8G   20M  4.6G    1% /mnt
/dev/sdb2                114G   61M  108G    1% /home
[root@test1 ~]#

```

```ruby
[root@test1 ~]# fdisk -l

磁盘 /dev/sda：85.9 GB, 85899345920 字节，167772160 个扇区
Units = 扇区 of 1 * 512 = 512 bytes
扇区大小(逻辑/物理)：512 字节 / 512 字节
I/O 大小(最小/最佳)：512 字节 / 512 字节
磁盘标签类型：dos
磁盘标识符：0x000c8857

   设备 Boot      Start         End      Blocks   Id  System
/dev/sda1   *        2048    20973567    10485760   83  Linux
/dev/sda2        20973568   167772159    73399296   8e  Linux LVM

磁盘 /dev/sdb：128.8 GB, 128849018880 字节，251658240 个扇区
Units = 扇区 of 1 * 512 = 512 bytes
扇区大小(逻辑/物理)：512 字节 / 512 字节
I/O 大小(最小/最佳)：512 字节 / 512 字节
磁盘标签类型：dos
磁盘标识符：0x37b71e86

   设备 Boot      Start         End      Blocks   Id  System
/dev/sdb1            2048    10485760     5241856+  8e  Linux LVM
/dev/sdb2        10487808   251658239   120585216   8e  Linux LVM

[root@test1 ~]#

```

- - - - - -

- - - - - -

###### 9 卸载分区

```ruby
[root@test1 ~]# umount /mnt
[root@test1 ~]# umount /home

```

- - - - - -

- - - - - -

- - - - - -

###### 总结 使用磁盘的思路

1. 将磁盘接入主机
2. 给磁盘分区
3. 在操作系统上创建文件夹，例如 `mkdir /home`
4. 将分区挂载到指定的目录上

- - - - - -

- - - - - -

- - - - - -

###### 知识扩展 LVM的磁盘管理

**[LVM的磁盘管理](https://blog.csdn.net/shardy0/article/details/86239616 "LVM的磁盘管理")**

<table><thead><tr><th align="center">序号</th><th align="center">缩写</th><th align="center">原词</th><th align="center">名词解释</th><th align="center">查询命令</th></tr></thead><tbody><tr><td align="center">①</td><td align="center">PE</td><td align="center">(Physical Extend)</td><td align="center">物理拓展</td><td align="center"></td></tr><tr><td align="center">②</td><td align="center">PV</td><td align="center">(Physical Volume)</td><td align="center">物理卷</td><td align="center">pvs</td></tr><tr><td align="center">③</td><td align="center">VG</td><td align="center">(Volume Group)</td><td align="center">卷组</td><td align="center">vgs</td></tr><tr><td align="center">④</td><td align="center">LV</td><td align="center">(Logical Volume)</td><td align="center">逻辑卷</td><td align="center">lvs</td></tr></tbody></table>

<table><thead><tr><th align="center">序号</th><th align="left">LVM的工作原理</th></tr></thead><tbody><tr><td align="center">(1)</td><td align="left">物理磁盘被格式化为PV，空间被划分为一个个的PE</td></tr><tr><td align="center">(2)</td><td align="left">不同的PV加入到同一个VG中，不同PV的PE全部进入到了VG的PE池内</td></tr><tr><td align="center">(3)</td><td align="left">LV基于PE创建，大小为PE的整数倍，组成LV的PE可能来自不同的物理磁盘</td></tr><tr><td align="center">(4)</td><td align="left">LV现在就直接可以格式化后挂载使用了</td></tr><tr><td align="center">(5)</td><td align="left">LV的扩充缩减实际上就是增加或减少组成该LV的PE数量，其过程不会丢失原始数据</td></tr></tbody></table>

- - - - - -